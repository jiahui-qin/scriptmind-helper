"""Application configuration — MiMo (Xiaomi) API."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MIMO_API_KEY: str = ""
    MIMO_API_BASE: str = "https://api.xiaomimimo.com/v1"
    MIMO_CHAT_MODEL: str = "mimo-v2.5-pro"
    MIMO_TTS_MODEL: str = "mimo-v2.5-tts"
    SQLITE_DB: str = "scriptmind.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024

    class Config:
        env_file = ".env"


settings = Settings()
