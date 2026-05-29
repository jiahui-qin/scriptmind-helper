"""Analysis API endpoints for script analysis."""
import logging
import traceback
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models.script import Script
from app.models.role import Role
from app.models.line import Line
from app.services.file_parser import parse_script_content, extract_roles
from app.services.role_analyzer import analyze_roles
from app.services.emotion_tagger import tag_emotions

logger = logging.getLogger("scriptmind.analysis")
router = APIRouter()


def _update_progress(db: Session, script_id: int, status_val: str, progress: int, error: str = None):
    """Update script analysis progress in DB."""
    script = db.query(Script).filter(Script.id == script_id).first()
    if script:
        script.status = status_val
        script.progress = progress
        if error:
            script.error_message = error
            script.status = "failed"
        db.commit()


def _run_analysis(script_id: int):
    """Run full analysis pipeline in background."""
    db = SessionLocal()
    try:
        logger.info(f"[script:{script_id}] Analysis started")

        # Step 1: Load script
        script = db.query(Script).filter(Script.id == script_id).first()
        if not script:
            logger.error(f"[script:{script_id}] Script not found")
            return
        _update_progress(db, script_id, "parsing", 5)
        logger.info(f"[script:{script_id}] Loaded: {script.filename} ({len(script.content)} chars)")

        # Step 2: Parse
        lines_dict = parse_script_content(script.content)
        role_names = extract_roles(lines_dict)
        _update_progress(db, script_id, "parsing", 15)
        logger.info(f"[script:{script_id}] Parsed {len(lines_dict)} lines, {len(role_names)} roles: {role_names}")

        # Step 3: Analyze roles via MiMo
        _update_progress(db, script_id, "analyzing_roles", 25)
        logger.info(f"[script:{script_id}] Calling MiMo API for role analysis...")
        roles_data = analyze_roles(script.content, role_names)
        logger.info(f"[script:{script_id}] MiMo returned {len(roles_data)} roles")
        for r in roles_data:
            logger.info(f"[script:{script_id}]   Role: {r.get('name')} ({r.get('gender')}, age={r.get('age')}, voice={r.get('voice_type')})")

        # Step 4: Save roles
        role_map = {}
        for r in roles_data:
            db_role = Role(
                script_id=script_id,
                name=r["name"],
                gender=r.get("gender", "未知"),
                age=r.get("age", 0),
                voice_type=r.get("voice_type", ""),
                personality=r.get("personality", ""),
                description=r.get("description", ""),
                tone_style=r.get("tone_style"),
                voice_color=r.get("voice_color"),
                persona_accent=r.get("persona_accent"),
                dialect=r.get("dialect"),
                roleplay=r.get("roleplay"),
                singing=r.get("singing"),
            )
            db.add(db_role)
            db.flush()
            role_map[r["name"]] = db_role.id
        db.commit()
        _update_progress(db, script_id, "analyzing_roles", 50)
        logger.info(f"[script:{script_id}] Saved {len(roles_data)} roles to DB")

        # Step 5: Save lines
        for ld in lines_dict:
            role_id = role_map.get(ld["role"]) if ld["role"] else None
            db_line = Line(
                script_id=script_id,
                role_id=role_id,
                line_number=ld["line_number"],
                content=ld["content"],
            )
            db.add(db_line)
        db.commit()
        _update_progress(db, script_id, "tagging_emotions", 60)
        logger.info(f"[script:{script_id}] Saved {len(lines_dict)} lines to DB")

        # Step 6: Tag emotions via MiMo
        lines_for_tagging = db.query(Line).filter(Line.script_id == script_id).all()
        lines_for_tagging.sort(key=lambda l: l.line_number)
        lines_dict_for_tagging = [
            {
                "line_number": l.line_number,
                "role": db.query(Role).filter(Role.id == l.role_id).first().name if l.role_id else None,
                "content": l.content,
            }
            for l in lines_for_tagging
        ]
        _update_progress(db, script_id, "tagging_emotions", 70)
        logger.info(f"[script:{script_id}] Calling MiMo API for emotion tagging ({len(lines_for_tagging)} lines)...")
        tagged = tag_emotions(script.content, lines_dict_for_tagging, roles_data)
        logger.info(f"[script:{script_id}] MiMo returned {len(tagged)} emotion tags")

        # Step 7: Update lines with emotion tags
        for t in tagged:
            line = db.query(Line).filter(
                Line.script_id == script_id, Line.line_number == t["line_number"]
            ).first()
            if line:
                line.emotion_tag = t.get("emotion_tag", "中性")
                line.emotion_intensity = t.get("emotion_intensity", 0.5)
                line.complex_emotion = t.get("complex_emotion")
        _update_progress(db, script_id, "completed", 100)
        script.is_analyzed = True
        db.commit()
        logger.info(f"[script:{script_id}] Analysis completed successfully")

    except Exception:
        logger.error(f"[script:{script_id}] Analysis FAILED:\n{traceback.format_exc()}")
        try:
            _update_progress(db, script_id, "failed", 0, error=traceback.format_exc()[-500:])
        except Exception:
            pass
    finally:
        db.close()


@router.post("/{script_id}/analyze", status_code=status.HTTP_202_ACCEPTED)
async def trigger_analysis(script_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail=f"Script {script_id} not found")
    script.status = "queued"
    script.progress = 0
    db.commit()
    logger.info(f"[script:{script_id}] Queued for analysis")
    background_tasks.add_task(_run_analysis, script_id)
    return {"script_id": script_id, "status": "queued", "message": "Analysis queued"}


@router.get("/{script_id}")
async def get_analysis(script_id: int, db: Session = Depends(get_db)):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail=f"Script {script_id} not found")
    roles = db.query(Role).filter(Role.script_id == script_id).all()
    lines = db.query(Line).filter(Line.script_id == script_id).order_by(Line.line_number).all()
    has_narration = any(l.role_id is None for l in lines)
    return {
        "script_id": script_id,
        "is_analyzed": script.is_analyzed,
        "status": script.status,
        "progress": script.progress,
        "error_message": script.error_message,
        "roles": [
            # 旁白作为系统角色始终排在最前（id=0 为虚拟ID，不与真实角色冲突）
            *([{
                "id": 0, "name": "旁白", "gender": "未知", "age": 0,
                "voice_type": "冰糖", "personality": "叙述",
                "tone_style": None, "voice_color": None, "persona_accent": None,
                "dialect": None, "roleplay": None, "singing": None,
            }] if has_narration else []),
            *[{
                "id": r.id, "name": r.name, "gender": r.gender,
                "age": r.age, "voice_type": r.voice_type, "personality": r.personality,
                "tone_style": r.tone_style,
                "voice_color": r.voice_color,
                "persona_accent": r.persona_accent,
                "dialect": r.dialect,
                "roleplay": r.roleplay,
                "singing": r.singing,
            } for r in roles],
        ],
        "lines": [
            {
                "id": l.id, "line_number": l.line_number, "content": l.content,
                "role_id": l.role_id, "emotion_tag": l.emotion_tag,
                "complex_emotion": l.complex_emotion,
            }
            for l in lines
        ],
        "total_lines": len(lines),
    }
