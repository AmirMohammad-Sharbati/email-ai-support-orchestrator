from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Ollama local (no API key)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"
    
    environment: str = "development"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()