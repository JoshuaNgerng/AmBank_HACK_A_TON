"""Database connection and session management (sync version)."""

from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.config import get_settings
from typing import Generator

settings = get_settings()

# URL-encode password in case it contains special characters
password = quote_plus(settings.POSTGRES_PASSWORD)

DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:"
    f"{password}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)

# Create the engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    # echo=settings.ENVIRONMENT == "development",
)

# Create a session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# FastAPI dependency
def get_db() -> Generator[Session, None, None]:
    """Dependency for getting a database session."""
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()

# For manual session usage
def get_session() -> Session:
    """Get a new session for manual connection management."""
    return SessionLocal()
