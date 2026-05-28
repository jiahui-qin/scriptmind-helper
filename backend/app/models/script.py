"""Script model - represents uploaded script files."""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Script(Base):
    """Script table model."""
    
    __tablename__ = "scripts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(255), nullable=False, comment="Original filename")
    file_path = Column(String(500), nullable=False, comment="Storage path")
    content = Column(Text, nullable=True, comment="Raw script content")
    file_size = Column(Integer, nullable=False, comment="File size in bytes")
    encoding = Column(String(50), default="utf-8", comment="File encoding")
    is_analyzed = Column(Boolean, default=False, comment="Analysis status")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Script(id={self.id}, filename='{self.filename}')>"
