"""Config API endpoints for application configuration."""
from fastapi import APIRouter
from typing import Dict, Any
import os
from app.config import settings

router = APIRouter()


@router.get("/status")
async def get_config_status():
    key_ok = bool(settings.MIMO_API_KEY)
    return {
        "mimo_api_configured": key_ok,
        "database_type": "sqlite",
        "redis_configured": bool(settings.REDIS_URL),
        "max_file_size_mb": settings.MAX_FILE_SIZE // 1024 // 1024,
        "features": {
            "upload": True,
            "analysis": key_ok,
            "tts": key_ok,
        }
    }


@router.post("/")
async def update_config(body: Dict[str, Any]):
    key = body.get("mimo_api_key", "")
    env_path = ".env"
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith("MIMO_API_KEY="):
            lines[i] = f"MIMO_API_KEY={key}\n"
            found = True
            break
    if not found:
        lines.append(f"MIMO_API_KEY={key}\n")
    with open(env_path, "w") as f:
        f.writelines(lines)
    return {"status": "ok", "mimo_api_configured": bool(key)}
