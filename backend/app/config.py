"""Application configuration settings."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""
    
    # MiMo API Configuration
    MIMO_API_KEY: str = ""
    MIMO_API_BASE: str = "https://api.moonshot.cn/v1"
    MIMO_TTS_URL: str = "https://api.moonshot.cn/v1/audio/speech"
    
    # Database
    SQLITE_DB: str = "scriptmind.db"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Celery
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"
    
    class Config:
        """Pydantic settings configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
