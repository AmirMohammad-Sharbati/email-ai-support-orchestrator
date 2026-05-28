from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    groq_api_key: str
    gemini_api_key: Optional[str] = None
    environment: str = "development"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Allow extra env vars

settings = Settings()