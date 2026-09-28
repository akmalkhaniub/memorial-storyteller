from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Memorial Storyteller API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security & Guardian Gate
    JWT_SECRET_KEY: str = "development-secret-key-change-in-production"
    GUARDIAN_DEFAULT_PIN_HASH: str = ""
    
    # Cloud Storage (Cloudflare R2 / AWS S3)
    STORAGE_ENDPOINT_URL: Optional[str] = None
    STORAGE_ACCESS_KEY_ID: Optional[str] = None
    STORAGE_SECRET_ACCESS_KEY: Optional[str] = None
    STORAGE_BUCKET_NAME: str = "memorial-vault"
    
    # Task Queue (Redis)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Generative AI Providers
    ELEVENLABS_API_KEY: Optional[str] = None
    HEDRA_API_KEY: Optional[str] = None
    HEYGEN_API_KEY: Optional[str] = None
    
    # Self-Hosted Worker URLs (Modal / RunPod)
    MODAL_LIVEPORTRAIT_URL: Optional[str] = None
    MODAL_F5TTS_URL: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
