from xmlrpc.client import Boolean
from app.models.base import TableBase
from enum import Enum, auto
from typing import Any
from sqlalchemy import Integer, Float, String, Numeric, JSON, Boolean, Enum as ENUM, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProgressState(Enum):
    classify = auto()
    statement = auto()
    analysis = auto()

class TaskProgress(TableBase):
    __tablename__ = "task_progress"

    celery_task_id: Mapped[str] = mapped_column(String)
    report_id: Mapped[int] = mapped_column(Integer)
    complete: Mapped[bool] = mapped_column(Boolean, default=False, server_default=false())
    progress: Mapped[ProgressState | None] = mapped_column(
        ENUM(
            ProgressState,
            name="progress_state_enum",
            native_enum=True,     # use PostgreSQL ENUM
            create_constraint=True,
        ),
        nullable= True
    )
    index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    immediatory_state: Mapped[Any | None] = mapped_column(JSON, nullable=True)
