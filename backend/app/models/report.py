from models.base import TableBase
from typing import Any, TYPE_CHECKING
from sqlalchemy import Integer, String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.statements import IncomeStatement, BalanceSheet, CashFlowStatement
    from models.analysis import BusinessStrategy, RiskAnalysis, QualitativePerformance, GrowthPotential

class ClassificationInfo(TableBase):
    __tablename__ = "classification_info"
    page_number: Mapped[int] = mapped_column(Integer)
    text_content: Mapped[str] = mapped_column(String)
    table_content: Mapped[Any] = mapped_column(JSON, nullable=True)
    category: Mapped[Any] = mapped_column(JSON, nullable=True)

    report_analysis_id: Mapped[int] = mapped_column(
        ForeignKey("report_analysis.id")
    )

    report_analysis: Mapped["ReportAnalysis"] = relationship(
        back_populates="classification"
    )

class ReportAnalysis(TableBase):
    __tablename__ = "report_analysis"
    company_name: Mapped[str] = mapped_column(String)
    pages: Mapped[int] = mapped_column(Integer)

    # One-to-many
    classification: Mapped[list["ClassificationInfo"]] = relationship(
        back_populates="report_analysis",
        cascade="all, delete-orphan"
    )

    # Finicial Statements
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

    # Finicial Analysis

    business_strategy: Mapped["BusinessStrategy"] = relationship(
        back_populates="report_analysis",
        uselist=False,
        cascade="all, delete-orphan"
    )

    risk_analysis: Mapped["RiskAnalysis"] = relationship(
        back_populates="report_analysis",
        uselist=False,
        cascade="all, delete-orphan"
    )

    qualitative_performance: Mapped["QualitativePerformance"] = relationship(
        back_populates="report_analysis",
        uselist=False,
        cascade="all, delete-orphan"
    )

    growth_potential: Mapped["GrowthPotential"] = relationship(
        back_populates="report_analysis",
        uselist=False,
        cascade="all, delete-orphan"
    )

