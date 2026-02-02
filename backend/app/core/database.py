"""Database connection and session management (sync version)."""

from contextlib import contextmanager
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, class_mapper
from collections.abc import Mapping
from typing import Generator
from app.core.config import get_settings

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
def get_db_session_instance() -> Session:
    """Get a new session for manual connection management."""
    return SessionLocal()

# Recommended to use context as much as possible
@contextmanager
def get_db_session():
    db = get_db_session_instance()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def from_dict(model_class, data: dict):
    """
    Create a SQLAlchemy model instance from a dict.
    Uses __table__ and class_mapper instead of sqlalchemy.inspect.
    Supports nested relationships.
    """
    if data is None:
        return None

    obj = model_class()

    # ---- Columns ----
    column_names = {c.name for c in model_class.__table__.columns}

    for name in column_names:
        if name in data:
            setattr(obj, name, data[name])

    # ---- Relationships ----
    mapper = class_mapper(model_class)

    for rel in mapper.relationships:
        key = rel.key
        if key not in data:
            continue

        value = data[key]
        target = rel.mapper.class_

        # one-to-many / many-to-many
        if rel.uselist:
            if isinstance(value, list):
                children = [
                    from_dict(target, item) # type: ignore
                    for item in value
                    if isinstance(item, Mapping)
                ]
                setattr(obj, key, children)

        # many-to-one / one-to-one
        else:
            if isinstance(value, Mapping):
                setattr(obj, key, from_dict(target, value)) # type: ignore

    return obj