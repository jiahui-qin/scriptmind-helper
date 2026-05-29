"""TTS API endpoints for MiMo text-to-speech synthesis."""
import json
import logging
import traceback
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session
from typing import Dict, Any
import os

from app.database import get_db, SessionLocal
from app.models.tts_task import TTSTask
from app.models.script import Script
from app.services.tts_service import synthesize_full_script, preview_voice, MIMO_VOICES

logger = logging.getLogger("scriptmind.tts")
router = APIRouter()


def _run_tts(script_id: int, role_voice_map: Dict[int, str], include_narration: bool = True,
             narration_voice: str = "冰糖", line_gap_ms: int = 0):
    db = SessionLocal()
    task_id = None
    try:
        script = db.query(Script).filter(Script.id == script_id).first()
        if not script:
            return
        task = db.query(TTSTask).filter(TTSTask.script_id == script_id).order_by(TTSTask.id.desc()).first()
        if task:
            task_id = task.id
            task.status = "processing"
            task.progress = 0
            db.commit()

        from app.models.line import Line
        lines = db.query(Line).filter(Line.script_id == script_id).order_by(Line.line_number).all()
        actual_role_voice_map = {int(k): v for k, v in role_voice_map.items()}
        actual_role_voice_map[0] = narration_voice
        lines_dict = [
            {
                "id": l.id, "line_number": l.line_number, "content": l.content,
                "role_id": l.role_id, "emotion_tag": l.emotion_tag,
                "speech_rate": 1.0, "emotion_intensity": l.emotion_intensity or 0.5,
            }
            for l in lines
        ]
        output_dir = os.path.join("data", "output")
        if not include_narration:
            lines_dict = [l for l in lines_dict if l["role_id"] is not None]

        total = len(lines_dict)
        logger.info(f"[tts:{script_id}] Synthesizing {total} lines (gap={line_gap_ms}ms)")

        def update_progress(done: int, t: int, failed: list):
            """Progress callback — updates DB after each line."""
            nonlocal task_id
            if task_id:
                dbu = SessionLocal()
                try:
                    tsk = dbu.query(TTSTask).filter(TTSTask.id == task_id).first()
                    if tsk:
                        tsk.progress = int(done / t * 100) if t > 0 else 0
                        tsk.error_message = json.dumps({"failed_lines": failed}) if failed else None
                        dbu.commit()
                finally:
                    dbu.close()

        result = synthesize_full_script(
            lines_dict, actual_role_voice_map, output_dir, script_id,
            line_gap_ms, progress_callback=update_progress,
        )
        failed_lines = result.get("failed_lines", [])

        if task_id:
            dbu = SessionLocal()
            try:
                tsk = dbu.query(TTSTask).filter(TTSTask.id == task_id).first()
                if tsk:
                    tsk.status = "completed"
                    tsk.progress = 100
                    tsk.audio_url = result["audio_path"]
                    tsk.subtitle_url = result["srt_path"]
                    tsk.voice_config = json.dumps({
                        "voice_map": {str(k): v for k, v in actual_role_voice_map.items()},
                        "line_gap_ms": line_gap_ms,
                        "include_narration": include_narration,
                        "total_lines": total,
                        "failed_lines": failed_lines,
                    })
                    if failed_lines:
                        tsk.error_message = json.dumps({"failed_lines": failed_lines})
                    dbu.commit()
            finally:
                dbu.close()

        logger.info(f"[tts:{script_id}] Completed (failed={len(failed_lines)})")
    except Exception:
        logger.error(f"[tts:{script_id}] Failed:\n{traceback.format_exc()}")
        dbu = SessionLocal()
        try:
            tsk = dbu.query(TTSTask).filter(TTSTask.id == task_id).first()
            if tsk:
                tsk.status = "failed"
                tsk.error_message = traceback.format_exc()[-500:]
                dbu.commit()
        except Exception:
            pass
        finally:
            dbu.close()
    finally:
        db.close()


# ── Preview endpoint ──────────────────────────────────────────────

@router.get("/preview")
async def get_voice_preview(voice: str = Query(default="冰糖")):
    """Return a short WAV preview for the given voice."""
    if voice not in MIMO_VOICES:
        raise HTTPException(status_code=400, detail=f"Unknown voice: {voice}")
    try:
        wav = preview_voice(voice)
        return Response(content=wav, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Synthesize ────────────────────────────────────────────────────

@router.post("/{script_id}/synthesize", status_code=status.HTTP_202_ACCEPTED)
async def trigger_tts(script_id: int, body: Dict[str, Any], background_tasks: BackgroundTasks,
                      db: Session = Depends(get_db)):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail=f"Script {script_id} not found")
    if not script.is_analyzed:
        raise HTTPException(status_code=400, detail="请先完成角色分析后再生成语音")
    role_voice_map = body.get("role_voice_map", {})
    include_narration = body.get("include_narration", True)
    narration_voice = body.get("narration_voice", "冰糖")
    line_gap_ms = body.get("line_gap_ms", 0)
    task = TTSTask(script_id=script_id, status="pending", progress=0)
    db.add(task)
    db.commit()
    db.refresh(task)
    background_tasks.add_task(_run_tts, script_id, role_voice_map, include_narration, narration_voice, line_gap_ms)
    logger.info(f"[tts:{script_id}] Task {task.id} queued")
    return {"script_id": script_id, "task_id": task.id, "status": "pending"}


# ── Status / Download ─────────────────────────────────────────────

@router.get("/tasks/{task_id}")
async def get_tts_status(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TTSTask).filter(TTSTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"TTS task {task_id} not found")

    failed_info = None
    if task.error_message:
        try:
            parsed = json.loads(task.error_message)
            if isinstance(parsed, dict) and "failed_lines" in parsed:
                failed_info = parsed
        except (json.JSONDecodeError, TypeError):
            pass

    return {
        "task_id": task.id, "script_id": task.script_id,
        "status": task.status, "progress": task.progress or 0,
        "audio_url": task.audio_url,
        "subtitle_url": task.subtitle_url,
        "voice_config": json.loads(task.voice_config) if task.voice_config else None,
        "error_message": task.error_message if not failed_info else None,
        "failed_lines": failed_info.get("failed_lines", []) if failed_info else [],
    }


@router.get("/tasks/{task_id}/download")
async def download_tts_file(task_id: int, type: str = "audio", db: Session = Depends(get_db)):
    task = db.query(TTSTask).filter(TTSTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != "completed":
        raise HTTPException(status_code=400, detail="TTS task not completed yet")
    file_path = task.audio_url if type == "audio" else task.subtitle_url
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    suffix = "wav" if type == "audio" else "srt"
    filename = f"script_{task.script_id}_{'audio' if type == 'audio' else 'subtitle'}.{suffix}"
    return FileResponse(file_path, filename=filename, media_type="application/octet-stream")
