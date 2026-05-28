"""Config API endpoints for application configuration."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.config import get_settings, settings

router = APIRouter()


@router.get("/status")
async def get_config_status():
    """
    Get application configuration status (non-sensitive).
    
    Returns:
        Dict: Configuration status information
    """
    return {
        "mimo_api_configured": bool(settings.MIMO_API_KEY),
        "database_type": "sqlite",
        "redis_configured": bool(settings.REDIS_URL),
        "max_file_size_mb": settings.MAX_FILE_SIZE // 1024 // 1024,
        "features": {
            "upload": True,
            "analysis": bool(settings.MIMO_API_KEY),
            "tts": bool(settings.MIMO_API_KEY),
            "celery": bool(settings.CELERY_BROKER_URL)
        }
    }


@router.get("/limits")
async def get_config_limits():
    """
    Get application limits and constraints.
    
    Returns:
        Dict: Application limits
    """
    return {
        "max_file_size_bytes": settings.MAX_FILE_SIZE,
        "max_file_size_mb": settings.MAX_FILE_SIZE // 1024 // 1024,
        "supported_file_types": [".txt"],
        "max_concurrent_tts_tasks": 3,
        "rate_limits": {
            "upload_per_minute": 10,
            "analysis_per_minute": 5,
            "tts_per_minute": 3
        }
    }
