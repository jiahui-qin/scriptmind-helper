"""TTS API endpoints for MiMo text-to-speech synthesis."""
import logging
import traceback
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any
import os

from app.database import get_db, SessionLocal
from app.models.tts_task import TTSTask
from app.models.script import Script
from app.services.tts_service import synthesize_full_script

logger = logging.getLogger("scriptmind.tts")
router = APIRouter()


def _run_tts(script_id: int, role_voice_map: Dict[int, str]):
    db = SessionLocal()
    try:
        script = db.query(Script).filter(Script.id == script_id).first()
        if not script:
            return
        from app.models.line import Line
        lines = db.query(Line).filter(Line.script_id == script_id).order_by(Line.line_number).all()
        lines_dict = [
            {
                "id": l.id, "line_number": l.line_number, "content": l.content,
                "role_id": l.role_id, "emotion_tag": l.emotion_tag,
                "speech_rate": 1.0, "emotion_intensity": l.emotion_intensity or 0.5,
            }
            for l in lines
        ]
        actual_role_voice_map = {int(k): v for k, v in role_voice_map.items()}
        output_dir = os.path.join("data", "output")
        logger.info(f"[tts:{script_id}] Synthesizing {len(lines_dict)} lines with {len(actual_role_voice_map)} voices")
        result = synthesize_full_script(lines_dict, actual_role_voice_map, output_dir, script_id)
        task = db.query(TTSTask).filter(TTSTask.script_id == script_id).order_by(TTSTask.id.desc()).first()
        if task:
            task.status = "completed"
            task.audio_url = result["audio_path"]
            task.subtitle_url = result["srt_path"]
            db.commit()
            logger.info(f"[tts:{script_id}] Completed: {result['audio_path']}")
    except Exception:
        logger.error(f"[tts:{script_id}] Failed:/n{traceback.format_exc()}")
        db.rollback()
        task = db.query(TTSTask).filter(TTSTask.script_id == script_id).order_by(TTSTask.id.desc()).first()
        if task:
            task.status = "failed"
            task.error_message = traceback.format_exc()[-500:]
            db.commit()
    finally:
        db.close()


@router.post("/{script_id}/synthesize", status_code=status.HTTP_202_ACCEPTED)
async def trigger_tts(script_id: int, body: Dict[str, Any], background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail=f"Script {script_id} not found")
    if not script.is_analyzed:
        raise HTTPException(status_code=400, detail="请先完成角色分析后再生成语音")
    role_voice_map = body.get("role_voice_map", {})
    task = TTSTask(script_id=script_id, status="pending")
    db.add(task)
    db.commit()
    db.refresh(task)
    background_tasks.add_task(_run_tts, script_id, role_voice_map)
    logger.info(f"[tts:{script_id}] Task {task.id} queued")
    return {"script_id": script_id, "task_id": task.id, "status": "pending"}


@router.get("/tasks/{task_id}")
async def get_tts_status(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TTSTask).filter(TTSTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"TTS task {task_id} not found")
    return {
        "task_id": task.id, "script_id": task.script_id,
        "status": task.status, "audio_url": task.audio_url,
        "subtitle_url": task.subtitle_url, "error_message": task.error_message,
    }


@router.get("/tasks/{task_id}/download")
async def download_tts_file(task_id: int, type: str = "audio", db: Session = Depends(get_db)):
    """Download generated audio or SRT file."""
    from fastapi.responses import FileResponse
    task = db.query(TTSTask).filter(TTSTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != "completed":
        raise HTTPException(status_code=400, detail="TTS task not completed yet")
    file_path = task.audio_url if type == "audio" else task.subtitle_url
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    filename = f"script_{task.script_id}_{'audio' if type == 'audio' else 'subtitle'}.{'wav' if type == 'audio' else 'srt'}"
    return FileResponse(file_path, filename=filename, media_type="application/octet-stream")
