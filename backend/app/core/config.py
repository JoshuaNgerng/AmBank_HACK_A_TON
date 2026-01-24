from functools import lru_cache
from typing import Optional
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "app"
    API_PREFIX: str = "/api"

    POSTGRES_DB: str 
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = 5432
    DB_POOL_SIZE: int = 20  # Increased from 10
    DB_MAX_OVERFLOW: int = 40  # Increased from 20
    DB_POOL_RECYCLE: int = 3600  # Add connection recycling (1 hour)
    DB_POOL_PRE_PING: bool = True  # Verify connections before use

    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

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
