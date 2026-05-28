"""TTSTask model - represents TTS synthesis tasks."""
from sqlalchemy import Column, Integer, String, Text, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class TTSTask(Base):
    """TTSTask table model for TTS synthesis tasks."""
    
    __tablename__ = "tts_tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    script_id = Column(Integer, ForeignKey("scripts.id"), nullable=False, index=True)
    task_id = Column(String(100), unique=True, nullable=False, index=True, comment="Celery task ID")
    status = Column(String(50), default="pending", comment="Task status (pending/processing/completed/failed)")
    audio_url = Column(String(500), nullable=True, comment="Generated audio file URL/path")
    subtitle_url = Column(String(500), nullable=True, comment="Generated subtitle file URL/path")
    voice_config = Column(Text, nullable=True, comment="JSON string of voice configurations")
    progress = Column(Integer, default=0, comment="Progress percentage (0-100)")
    error_message = Column(Text, nullable=True, comment="Error message if failed")
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    script = relationship("Script")
    
    def __repr__(self) -> str:
        return f"<TTSTask(id={self.id}, task_id='{self.task_id}', status='{self.status}')>"
