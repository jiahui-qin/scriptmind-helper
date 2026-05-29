"""Roles API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from pydantic import BaseModel

from app.database import get_db
from app.models.role import Role

router = APIRouter()


class RoleCreate(BaseModel):
    """Schema for creating a new role."""
    name: str
    gender: Optional[str] = "未知"
    age: Optional[int] = 0
    personality: Optional[str] = ""
    tone_style: Optional[str] = None
    voice_color: Optional[str] = None
    persona_accent: Optional[str] = None
    dialect: Optional[str] = None
    roleplay: Optional[str] = None
    singing: Optional[str] = None


@router.put("/{role_id}")
async def update_role(role_id: int, body: Dict[str, Any], db: Session = Depends(get_db)):
    """Update role properties (voice_type, name, personality, etc.)."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    for field in ["name", "gender", "age", "voice_type", "personality", "description",
                  "tone_style", "voice_color", "persona_accent", "dialect", "roleplay", "singing"]:
        if field in body:
            setattr(role, field, body[field])
    db.commit()
    db.refresh(role)
    return {
        "id": role.id, "name": role.name, "gender": role.gender,
        "age": role.age, "voice_type": role.voice_type,
        "personality": role.personality, "description": role.description,
        "tone_style": role.tone_style, "voice_color": role.voice_color,
        "persona_accent": role.persona_accent, "dialect": role.dialect,
        "roleplay": role.roleplay, "singing": role.singing,
    }


@router.post("/scripts/{script_id}/roles", status_code=status.HTTP_201_CREATED)
async def create_role(script_id: int, body: RoleCreate, db: Session = Depends(get_db)):
    """Create a new role for a script."""
    role = Role(script_id=script_id, **body.model_dump())
    db.add(role)
    db.commit()
    db.refresh(role)
    return {
        "id": role.id, "name": role.name, "gender": role.gender,
        "age": role.age, "voice_type": role.voice_type,
        "personality": role.personality, "description": role.description,
        "tone_style": role.tone_style, "voice_color": role.voice_color,
        "persona_accent": role.persona_accent, "dialect": role.dialect,
        "roleplay": role.roleplay, "singing": role.singing,
    }
