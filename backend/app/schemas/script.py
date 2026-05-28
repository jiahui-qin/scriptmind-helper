"""Pydantic schemas for Script model."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ScriptBase(BaseModel):
    """Base schema for Script."""
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")


class ScriptCreate(ScriptBase):
    """Schema for creating a new Script."""
    file_path: str = Field(..., description="Storage path")
    content: Optional[str] = Field(None, description="Raw script content")
    encoding: str = Field(default="utf-8", description="File encoding")


class ScriptResponse(ScriptBase):
    """Schema for Script response."""
    id: int
    file_path: str
    content: Optional[str] = None
    encoding: str = "utf-8"
    is_analyzed: bool = False
    status: str = "uploaded"
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ScriptAnalysisResponse(BaseModel):
    """Schema for script analysis results."""
    script_id: int
    is_analyzed: bool
    roles_count: int
    lines_count: int
    roles: List[dict] = []
    
    class Config:
        from_attributes = True
