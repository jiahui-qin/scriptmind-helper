"""Line model - represents individual script lines."""
from sqlalchemy import Column, Integer, Text, Integer, String, DateTime, ForeignKey
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
    context = Column(Text, nullable=True, comment="Surrounding context")
    emotion_tag_id = Column(Integer, ForeignKey("emotion_tags.id"), nullable=True)
    order_index = Column(Integer, default=0, comment="Display order within script")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    script = relationship("Script", back_populates="lines")
    role = relationship("Role", back_populates="lines")
    emotion_tag = relationship("EmotionTag", back_populates="lines")
    
    def __repr__(self) -> str:
        return f"<Line(id={self.id}, line_number={self.line_number}, role_id={self.role_id})>"
