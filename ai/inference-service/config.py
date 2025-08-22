import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    DB_CONN_STRING: str = os.getenv("DB_CONN_STRING", "")
    
    # External APIs
    NASA_API_KEY: str = os.getenv("NASA_API_KEY", "DEMO_KEY")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    
    # Model Paths
    MODEL_DIR: str = os.getenv("MODEL_DIR", "/app/models")
    
    # Redis for caching and task queue
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    
    # CORS
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

settings = Settings()