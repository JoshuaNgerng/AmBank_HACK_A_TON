from models.base import TableBase
from typing import Any, TYPE_CHECKING
from sqlalchemy import Integer, String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.statements import IncomeStatement, BalanceSheet, CashFlowStatement

class ClassificationInfo(TableBase):
    page_number: Mapped[int] = mapped_column(Integer)
    text_content: Mapped[str] = mapped_column(String)
    table_content: Mapped[Any] = mapped_column(JSON, nullable=True)

    report_analysis_id: Mapped[int] = mapped_column(
        ForeignKey("report_analysis.id")
    )

    report_analysis: Mapped["ReportAnalysis"] = relationship(
        back_populates="classification"
    )

class ReportAnalysis(TableBase):
    pages: Mapped[int] = mapped_column(Integer)

    # One-to-many
    classification: Mapped[list["ClassificationInfo"]] = relationship(
        back_populates="report_analysis",
        cascade="all, delete-orphan"
    )

    # One-to-one
    income_statement: Mapped["IncomeStatement"] = relationship(
        back_populates="report_analysis",
        uselist=False,
        cascade="all, delete-orphan"
    )

    balance_sheet: Mapped["BalanceSheet"] = relationship(
        back_populates="report_analysis",
        uselist=False,
        cascade="all, delete-orphan"
    )

    cash_flow: Mapped["CashFlowStatement"] = relationship(
        back_populates="report_analysis",
        uselist=False,
        cascade="all, delete-orphan"
    )
