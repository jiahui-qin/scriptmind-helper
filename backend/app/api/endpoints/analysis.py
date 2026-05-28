"""Analysis API endpoints for script analysis."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import json

from app.database import get_db
from app.models.script import Script
from app.models.role import Role
from app.models.line import Line
from app.schemas.script import ScriptAnalysisResponse

router = APIRouter()


@router.post("/{script_id}/analyze", status_code=status.HTTP_202_ACCEPTED)
async def trigger_analysis(
    script_id: int,
    db: Session = Depends(get_db)
):
    """
    Trigger AI analysis for a script.
    
    Args:
        script_id: Script ID to analyze
        db: Database session
        
    Returns:
        Dict: Analysis initiation status
        
    Raises:
        HTTPException: If script not found
    """
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Script with ID {script_id} not found"
        )
    
    # TODO: Implement actual AI analysis with MiMo API
    # For now, return a placeholder response
    return {
        "script_id": script_id,
        "status": "pending",
        "message": "Analysis task has been queued"
    }


@router.get("/{script_id}", response_model=ScriptAnalysisResponse)
async def get_analysis(
    script_id: int,
    db: Session = Depends(get_db)
):
    """
    Get analysis results for a script.
    
    Args:
        script_id: Script ID
        db: Database session
        
    Returns:
        ScriptAnalysisResponse: Analysis results with roles and lines
        
    Raises:
        HTTPException: If script not found
    """
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Script with ID {script_id} not found"
        )
    
    # Get roles
    roles = db.query(Role).filter(Role.script_id == script_id).all()
    
    # Get lines
    lines = db.query(Line).filter(Line.script_id == script_id).all()
    
    return {
        "script_id": script_id,
        "is_analyzed": script.is_analyzed,
        "roles_count": len(roles),
        "lines_count": len(lines),
        "roles": [
            {
                "id": role.id,
                "name": role.name,
                "description": role.description,
                "personality": role.personality,
                "gender": role.gender,
                "age_range": role.age_range,
                "line_count": role.line_count
            }
            for role in
            roles
        ],
        "lines": [
            {
                "id": line.id,
                "line_number": line.line_number,
                "content": line.content,
                "role_id": line.role_id,
                "order_index": line.order_index
            }
            for line in
            lines
        ]
    }
