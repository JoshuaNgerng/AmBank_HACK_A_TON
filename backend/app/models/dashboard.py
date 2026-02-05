from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any
from app.models.base import TableBase
from app.models.report import Company

class CompanyDashboard(TableBase): # act as a caching for company dashboard
    __tablename__ = "company_dashboard"
    summary: Mapped[Any] = mapped_column(JSON, nullable=True)
    details: Mapped[Any] = mapped_column(JSON, nullable=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('company.id'))
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="company_dashboard",
        uselist=False
    )
