from app.models.base import TableBase
from enum import Enum, auto
from typing import Any
from sqlalchemy import Integer, Float, String, Numeric, JSON, ForeignKey, Enum as ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProgressState(Enum):
    classify = auto()
    statement = auto()
    analysis = auto()

class TaskProgress(TableBase):
    celery_task_id: Mapped[int] = mapped_column(Integer)
    progress: Mapped[ProgressState] = mapped_column(ENUM)
    index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    immediatory_state: Mapped[Any | None] = mapped_column(JSON, nullable=True)
    ocr_result: Mapped[Any] = mapped_column(JSON, nullable=True)
