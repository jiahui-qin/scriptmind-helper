"""StylePreset model - stores custom style preset values."""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class StylePreset(Base):
    """StylePreset table model for custom style preset values."""

    __tablename__ = "style_presets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(String(50), nullable=False, index=True)
    value = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<StylePreset(id={self.id}, category='{self.category}', value='{self.value}')>"
