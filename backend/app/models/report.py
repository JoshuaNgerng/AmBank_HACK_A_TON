from typing import Any, TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy import Integer, String, Enum, ForeignKey, Float, DateTime, ARRAY, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from app.models.base import TableBase

if TYPE_CHECKING:
    from app.models.statements import IncomeStatement, BalanceSheet, CashFlowStatement
    from app.models.analysis import BusinessStrategy, RiskAnalysis, QualitativePerformance, GrowthPotential
    from app.models.source import Source, PossibleStatement, PossibleSignal



class ReportingPeriod(TableBase):
    __tablename__ = "reporting_period"

    # must be the same as the CompanyReport its from never change it after creation
    report_date: Mapped[datetime] = mapped_column(DateTime)
    # e.g. 2024, 2023, "5_year_summary", "historical"
    period_label: Mapped[str] = mapped_column(String)
    fiscal_year: Mapped[int] = mapped_column(Integer)
    period_type: Mapped[str] = mapped_column(String)
    # "annual", "historical_summary", "quarterly", "unknown"

    # Finicial Statements
    income_statement: Mapped["IncomeStatement"] = relationship(
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )

    balance_sheet: Mapped["BalanceSheet"] = relationship(
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )

    cash_flow_statement: Mapped["CashFlowStatement"] = relationship(
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Finicial Analysis

    business_strategy: Mapped["BusinessStrategy"] = relationship(
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )

    risk_analysis: Mapped["RiskAnalysis"] = relationship(
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )

    qualitative_performance: Mapped["QualitativePerformance"] = relationship(
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )

    growth_potential: Mapped["GrowthPotential"] = relationship(
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company: Mapped["Company"] = relationship(
        back_populates="reporting_period",
        uselist=False,
    )

class CompanyReport(TableBase):
    __tablename__ = "company_report"

    file_key: Mapped[str] = mapped_column(String, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    celery_task_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    report_type: Mapped[str | None] = mapped_column(String, nullable=True)
    # "annual", "quarterly", "prospectus", etc.
    report_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_pages: Mapped[int] = mapped_column(Integer, default=0)

    company_id: Mapped[int | None] = mapped_column(ForeignKey("company.id"), nullable=True)
    company: Mapped["Company"] = relationship(back_populates="company_reports")

    report_sources: Mapped[list["Source"]] = relationship(
        back_populates="company_report",
        cascade="all, delete-orphan"
    )

class Company(TableBase):
    __tablename__ = "company"

    company_id: Mapped[str] = mapped_column(String(100), unique=True)  
    # ticker, registration number, etc.
    company_name: Mapped[str] = mapped_column(String(200))

    company_reports: Mapped[list["CompanyReport"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    reporting_period: Mapped[list["ReportingPeriod"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )

    def get_report_by_year(self, year: int) -> Optional["ReportingPeriod"]:
        for report in self.reporting_period:
            if report.fiscal_year == year:
                return report
        return None