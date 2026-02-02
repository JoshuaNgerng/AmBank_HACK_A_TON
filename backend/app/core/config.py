from functools import lru_cache
from typing import Optional
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "app"
    API_PREFIX: str = "/api"

    # POSTGRES
    POSTGRES_DB: str 
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = 5432
    DB_POOL_SIZE: int = 20  # Increased from 10
    DB_MAX_OVERFLOW: int = 40  # Increased from 20
    DB_POOL_RECYCLE: int = 3600  # Add connection recycling (1 hour)
    DB_POOL_PRE_PING: bool = True  # Verify connections before use

    # JWT
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis settings
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "False").lower() in ("true", "1", "t")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost") 
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    REDIS_TIMEOUT: int = int(os.getenv("REDIS_TIMEOUT", "5"))
    REDIS_POOL_SIZE: int = int(os.getenv("REDIS_POOL_SIZE", "10"))

    # Celery settings
    CELERY_ENABLED: bool = os.getenv("CELERY_ENABLED", "False").lower() in ("true", "1", "t")
    CELERY_CONCURRENCY: int = int(os.getenv("CELERY_CONCURRENCY", "2"))
    CELERY_TASK_RETRY_MAX: int = int(os.getenv("CELERY_TASK_RETRY_MAX", "3"))
    CELERY_TASK_RETRY_DELAY: int = int(os.getenv("CELERY_TASK_RETRY_DELAY", "5"))

    LOG_LEVEL: str = "INFO"
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore auto parse in .env file


settings = get_settings()
