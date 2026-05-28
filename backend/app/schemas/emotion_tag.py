"""Pydantic schemas for EmotionTag model."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class EmotionTagBase(BaseModel):
    """Base schema for EmotionTag."""
    name: str = Field(..., description="Emotion name")


class EmotionTagCreate(EmotionTagBase):
    """Schema for creating a new EmotionTag."""
    description: Optional[str] = Field(None, description="Emotion description")
    category: Optional[str] = Field(None, description="Emotion category")
    intensity: Optional[str] = Field(None, description="Intensity level")
    color_code: Optional[str] = Field(None, description="Display color (hex)")


class EmotionTagResponse(EmotionTagBase):
    """Schema for EmotionTag response."""
    id: int
    description: Optional[str] = None
    category: Optional[str] = None
    intensity: Optional[str] = None
    color_code: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
