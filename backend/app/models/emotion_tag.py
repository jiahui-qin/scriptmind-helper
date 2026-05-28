"""EmotionTag model - represents emotion labels for lines."""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class EmotionTag(Base):
    """EmotionTag table model for line emotion annotations."""
    
    __tablename__ = "emotion_tags"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True, comment="Emotion name")
    description = Column(Text, nullable=True, comment="Emotion description")
    category = Column(String(50), nullable=True, comment="Emotion category")
    intensity = Column(String(20), nullable=True, comment="Intensity level (low/medium/high)")
    color_code = Column(String(7), nullable=True, comment="Display color (hex)")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lines = relationship("Line", back_populates="emotion_tag")
    
    def __repr__(self) -> str:
        return f"<EmotionTag(id={self.id}, name='{self.name}')>"
