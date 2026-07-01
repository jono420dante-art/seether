import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "production"
    APP_NAME: str = "seether"
    
    # YouTube Revenue Engine IDs
    YOUTUBE_CHANNEL_ID: str = "UCadswi1Ru84isQ6G7zrwGHQ"
    YOUTUBE_USER_ID: str = "adswi1Ru84isQ6G7zrwGHQ"
    
    # Trend Spike Thresholds
    TREND_SPIKE_VIEWS_24H: int = 5000
    
    # Secret keys
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tpd-super-secret-key-12345")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "jwt-secret-98765")

    class Config:
        env_file = ".env"

settings = Settings()
