"""Pydantic schemas for Role model."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class RoleBase(BaseModel):
    """Base schema for Role."""
    name: str = Field(..., description="Character name")
    script_id: int = Field(..., description="Associated script ID")


class RoleCreate(RoleBase):
    """Schema for creating a new Role."""
    description: Optional[str] = Field(None, description="Character description")
    personality: Optional[str] = Field(None, description="Personality traits")
    gender: Optional[str] = Field(None, description="Gender")
    age_range: Optional[str] = Field(None, description="Age range")
    voice_profile: Optional[str] = Field(None, description="Voice characteristics")


class RoleResponse(RoleBase):
    """Schema for Role response."""
    id: int
    description: Optional[str] = None
    personality: Optional[str] = None
    gender: Optional[str] = None
    age_range: Optional[str] = None
    voice_profile: Optional[str] = None
    line_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RoleAnalysis(BaseModel):
    """Schema for AI-generated role analysis."""
    name: str
    description: str
    personality: str
    gender: Optional[str] = None
    age_range: Optional[str] = None
    voice_profile: Optional[str] = None
    line_count: int = 0
