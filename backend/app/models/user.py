from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import TableBase

class User(TableBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    
