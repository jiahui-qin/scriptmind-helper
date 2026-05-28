"""Upload API endpoints for script file uploads."""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os
import uuid

from app.database import get_db
from app.models.script import Script
from app.schemas.script import ScriptResponse, ScriptCreate

router = APIRouter()


@router.post("/script", response_model=ScriptResponse, status_code=status.HTTP_201_CREATED)
async def upload_script(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a script file for analysis.
    
    Args:
        file: Uploaded script file (.txt)
        db: Database session
        
    Returns:
        ScriptResponse: Created script record
        
    Raises:
        HTTPException: If file validation fails
    """
    # Validate file extension
    if not file.filename.endswith('.txt'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .txt files are supported"
        )
    
    # Read file content
    content = await file.read()
    file_size = len(content)
    
    # Validate file size
    from app.config import settings
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE // 1024 // 1024}MB"
        )
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    stored_filename = f"{file_id}{file_extension}"
    file_path = os.path.join("data", "uploads", stored_filename)
    
    # Ensure upload directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Decode content
    try:
        content_str = content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            content_str = content.decode('gbk')
        except UnicodeDecodeError:
            content_str = content.decode('utf-8', errors='ignore')
    
    # Create database record
    db_script = Script(
        filename=file.filename,
        file_path=file_path,
        content=content_str,
        file_size=file_size,
        encoding='utf-8'
    )
    
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    
    return db_script


@router.get("/scripts", response_model=List[ScriptResponse])
async def list_scripts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all uploaded scripts.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List[ScriptResponse]: List of scripts
    """
    scripts = db.query(Script).offset(skip).limit(limit).all()
    return scripts


@router.get("/script/{script_id}", response_model=ScriptResponse)
async def get_script(
    script_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific script by ID.
    
    Args:
        script_id: Script ID
        db: Database session
        
    Returns:
        ScriptResponse: Script details
        
    Raises:
        HTTPException: If script not found
    """
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Script with ID {script_id} not found"
        )
    return script
