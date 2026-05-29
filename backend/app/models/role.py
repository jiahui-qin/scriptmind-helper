"""Role model - represents characters in scripts."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Role(Base):
    """Role table model for script characters."""
    
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    script_id = Column(Integer, ForeignKey("scripts.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False, comment="Character name")
    gender = Column(String(20), nullable=True, comment="Gender (male/female/unknown)")
    age = Column(Integer, default=0, comment="Age")
    voice_type = Column(String(100), nullable=True, comment="Voice type")
    personality = Column(Text, nullable=True, comment="Personality traits")
    description = Column(Text, nullable=True, comment="Character description")
    tone_style = Column(String(50), nullable=True, comment="整体语调")
    voice_color = Column(String(50), nullable=True, comment="音色定位")
    persona_accent = Column(String(50), nullable=True, comment="人设腔调")
    dialect = Column(String(50), nullable=True, comment="方言")
    roleplay = Column(String(50), nullable=True, comment="角色扮演")
    singing = Column(String(50), nullable=True, comment="唱歌风格")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    script = relationship("Script", back_populates="roles")
    lines = relationship("Line", back_populates="role", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}', script_id={self.script_id})>"
