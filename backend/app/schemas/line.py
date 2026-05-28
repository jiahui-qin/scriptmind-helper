"""Pydantic schemas for Line model."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.emotion_tag import EmotionTagResponse


class LineBase(BaseModel):
    """Base schema for Line."""
    script_id: int = Field(..., description="Associated script ID")
    line_number: int = Field(..., description="Line number in script")
    content: str = Field(..., description="Line content")


class LineCreate(LineBase):
    """Schema for creating a new Line."""
    role_id: Optional[int] = Field(None, description="Associated role ID")
    context: Optional[str] = Field(None, description="Surrounding context")
    emotion_tag_id: Optional[int] = Field(None, description="Associated emotion tag ID")
    order_index: int = Field(default=0, description="Display order")


class LineResponse(LineBase):
    """Schema for Line response."""
    id: int
    role_id: Optional[int] = None
    context: Optional[str] = None
    emotion_tag_id: Optional[int] = None
    order_index: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class LineWithEmotion(LineResponse):
    """Schema for Line with emotion tag details."""
    emotion_tag: Optional[EmotionTagResponse] = None
    role_name: Optional[str] = None
