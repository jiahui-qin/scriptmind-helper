"""Roles API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.models.role import Role

router = APIRouter()


@router.put("/{role_id}")
async def update_role(role_id: int, body: Dict[str, Any], db: Session = Depends(get_db)):
    """Update role properties (voice_type, name, personality, etc.)."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    for field in ["name", "gender", "age", "voice_type", "personality", "description"]:
        if field in body:
            setattr(role, field, body[field])
    db.commit()
    db.refresh(role)
    return {
        "id": role.id, "name": role.name, "gender": role.gender,
        "age": role.age, "voice_type": role.voice_type,
        "personality": role.personality, "description": role.description,
    }
