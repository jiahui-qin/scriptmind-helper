"""Config API endpoints for application configuration."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import os
from pydantic_settings import BaseSettings

router = APIRouter()


class ConfigUpdate(BaseSettings):
    moonshot_api_key: str = ""


@router.get("/status")
async def get_config_status():
    from app.config import settings
    return {
        "moonshot_api_configured": bool(os.getenv("MOONSHOT_API_KEY") or getattr(settings, "MOONSHOT_API_KEY", "")),
        "database_type": "sqlite",
        "redis_configured": bool(getattr(settings, "REDIS_URL", "")),
        "max_file_size_mb": getattr(settings, "MAX_FILE_SIZE", 10 * 1024 * 1024) // 1024 // 1024,
        "features": {
            "upload": True,
            "analysis": bool(os.getenv("MOONSHOT_API_KEY") or getattr(settings, "MOONSHOT_API_KEY", "")),
            "tts": bool(os.getenv("MOONSHOT_API_KEY") or getattr(settings, "MOONSHOT_API_KEY", "")),
        }
    }


@router.post("/")
async def update_config(body: Dict[str, Any]):
    from app.config import settings
    key = body.get("moonshot_api_key", "")
    # Write to .env file
    env_path = ".env"
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith("MOONSHOT_API_KEY="):
            lines[i] = f"MOONSHOT_API_KEY={key}\n"
            found = True
            break
    if not found:
        lines.append(f"MOONSHOT_API_KEY={key}\n")
    with open(env_path, "w") as f:
        f.writelines(lines)
    return {"status": "ok", "moonshot_api_configured": bool(key)}
