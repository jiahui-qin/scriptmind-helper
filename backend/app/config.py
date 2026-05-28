"""Application configuration settings."""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""
    
    # Moonshot API Configuration (MiMo)
    MOONSHOT_API_KEY: str = ""
    MIMO_API_BASE: str = "https://api.moonshot.cn/v1"
    MIMO_TTS_URL: str = "https://api.moonshot.cn/v1/audio/speech"
    
    # Database
    SQLITE_DB: str = "scriptmind.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    class Config:
        """Pydantic settings configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
