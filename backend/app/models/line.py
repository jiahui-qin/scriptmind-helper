"""Line model - represents individual script lines."""
from sqlalchemy import Column, Integer, Text, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Line(Base):
    """Line table model for individual script lines."""
    
    __tablename__ = "lines"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    script_id = Column(Integer, ForeignKey("scripts.id"), nullable=False, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True, index=True)
    line_number = Column(Integer, nullable=False, comment="Line number in script")
    content = Column(Text, nullable=False, comment="Line content/text")
    emotion_tag = Column(String(50), nullable=True, comment="Emotion tag")
    emotion_intensity = Column(Float, nullable=True, comment="Emotion intensity 0-1")
    complex_emotion = Column(String(50), nullable=True, comment="复合情绪")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    script = relationship("Script", back_populates="lines")
    role = relationship("Role", back_populates="lines")
    
    def __repr__(self) -> str:
        return f"<Line(id={self.id}, line_number={self.line_number}, role_id={self.role_id})>"
