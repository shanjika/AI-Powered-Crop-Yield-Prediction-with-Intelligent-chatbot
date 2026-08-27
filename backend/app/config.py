import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Powered Crop Yield Prediction - Tamil Nadu"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("JWT_SECRET", "tamilnadu-crop-yield-prediction-super-secret-key-2026-agri-ai")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Default to SQLite for easy zero-setup out of the box, with PostgreSQL support via DATABASE_URL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./agri_crop_prediction.db"
    )
    
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    
    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
