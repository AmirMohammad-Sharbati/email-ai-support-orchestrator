from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"
    ollama_timeout: int = 300
    ollama_temperature: float = 0.1
    ollama_retries: int = 3
    
    # Application Configuration
    environment: str = "development"
    log_level: str = "DEBUG"
    max_email_length: int = 10000
    max_email_preview: int = 100
    default_confidence: float = 0.7


    @field_validator('ollama_base_url')
    def validate_ollama_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError(f"Ollama URL must start with http:// or https://, got: {v}")
        return v
    
    @field_validator('ollama_model')
    def validate_model(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("Model name cannot be empty")
        return v
    
    @field_validator('max_email_length')
    def validate_max_length(cls, v):
        if v < 100 or v > 100000:
            raise ValueError("max_email_length must be between 100 and 100000")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

settings = Settings()