"""TTS API endpoints for text-to-speech synthesis."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.models.tts_task import TTSTask
from app.schemas.tts_task import TTSTaskResponse, TTSTaskStatus

router = APIRouter()


@router.post("/{script_id}/synthesize", status_code=status.HTTP_202_ACCEPTED)
async def trigger_tts(
    script_id: int,
    db: Session = Depends(get_db)
):
    """
    Trigger TTS synthesis for a script.
    
    Args:
        script_id: Script ID to synthesize
        db: Database session
        
    Returns:
        Dict: TTS task initiation status
        
    Raises:
        HTTPException: If script not found or not analyzed
    """
    from app.models.script import Script
    
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Script with ID {script_id} not found"
        )
    
    if not script.is_analyzed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Script must be analyzed before TTS synthesis"
        )
    
    # TODO: Implement actual TTS task creation with Celery
    # For now, return a placeholder response
    return {
        "script_id": script_id,
        "task_id": "placeholder-task-id",
        "status": "pending",
        "message": "TTS task has been queued"
    }


@router.get("/tasks/{task_id}", response_model=TTSTaskStatus)
async def get_tts_status(
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    Get TTS task status.
    
    Args:
        task_id: Celery task ID
        db: Database session
        
    Returns:
        TTSTaskStatus: Task status details
        
    Raises:
        HTTPException: If task not found
    """
    task = db.query(TTSTask).filter(TTSTask.task_id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TTS task with ID {task_id} not found"
        )
    
    return {
        "task_id": task.task_id,
        "status": task.status,
        "progress": task.progress,
        "audio_url": task.audio_url,
        "subtitle_url": task.subtitle_url,
        "error_message": task.error_message
    }


@router.get("/tasks", response_model=list[TTSTaskResponse])
async def list_tts_tasks(
    script_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List TTS tasks.
    
    Args:
        script_id: Optional filter by script ID
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List[TTSTaskResponse]: List of TTS tasks
    """
    query = db.query(TTSTask)
    
    if script_id:
        query = query.filter(TTSTask.script_id == script_id)
    
    tasks = query.offset(skip).limit(limit).all()
    return tasks
