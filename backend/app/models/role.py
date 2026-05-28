"""Role model - represents characters in scripts."""
from sqlalchemy import Column, Integer, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Role(Base):
    """Role table model for script characters."""
    
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    script_id = Column(Integer, ForeignKey("scripts.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False, comment="Character name")
    description = Column(Text, nullable=True, comment="AI-generated character description")
    personality = Column(Text, nullable=True, comment="Personality traits")
    gender = Column(String(20), nullable=True, comment="Gender (male/female/unknown)")
    age_range = Column(String(50), nullable=True, comment="Age range description")
    voice_profile = Column(String(200), nullable=True, comment="Voice characteristics")
    line_count = Column(Integer, default=0, comment="Number of lines for this role")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    script = relationship("Script", back_populates="roles")
    lines = relationship("Line", back_populates="role", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}', script_id={self.script_id})>"
