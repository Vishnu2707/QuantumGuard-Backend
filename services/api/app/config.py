
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017/quantumguard"
    DB_NAME: str = "quantumguard"
    JWT_SECRET: str = "changeme"
    JWT_EXPIRE_MINUTES: int = 30
    APIKEY_KDF_SALT: str = "changeme_salt"
    APP_ENV: str = "development"
    CORS_ORIGINS: str = "http://localhost:3000"
    RATE_LIMITS_PQC: str = "10/second,2000/day"

    class Config:
        env_file = ".env"

settings = Settings()
ALLOWED_ORIGINS: List[str] = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
