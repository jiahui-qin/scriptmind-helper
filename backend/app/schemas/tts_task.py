"""Pydantic schemas for TTSTask model."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    """TTS task status enum."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TTSTaskBase(BaseModel):
    """Base schema for TTSTask."""
    script_id: int = Field(..., description="Associated script ID")


class TTSTaskCreate(TTSTaskBase):
    """Schema for creating a new TTSTask."""
    voice_config: Optional[str] = Field(None, description="JSON string of voice configurations")


class TTSTaskResponse(TTSTaskBase):
    """Schema for TTSTask response."""
    id: int
    task_id: str = Field(..., description="Celery task ID")
    status: str = "pending"
    audio_url: Optional[str] = None
    subtitle_url: Optional[str] = None
    voice_config: Optional[str] = None
    progress: int = 0
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class TTSTaskStatus(BaseModel):
    """Schema for TTS task status check."""
    task_id: str
    status: str
    progress: int = 0
    audio_url: Optional[str] = None
    subtitle_url: Optional[str] = None
    error_message: Optional[str] = None
