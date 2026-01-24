from models.base import TableBase
from typing import Any, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Integer, String, JSON, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.statements import IncomeStatement, BalanceSheet, CashFlowStatement
    from models.analysis import BusinessStrategy, RiskAnalysis, QualitativePerformance, GrowthPotential

class SourceFragment(TableBase):
    __tablename__ = "source_fragment"

    signal_type: Mapped[str] = mapped_column(String)
    page_number: Mapped[int] = mapped_column(Integer)
    file_key: Mapped[str] = mapped_column(String)

    text: Mapped[str] = mapped_column(String)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

    report_id: Mapped[int] = mapped_column(ForeignKey("company_report.id"))
    company_report: Mapped["CompanyReport"] = relationship(
        back_populates="report_sources", uselist=False,
    )

class ReportingPeriod(TableBase):
    __tablename__ = "reporting_period"

    # e.g. 2024, 2023, "5_year_summary", "historical"
    period_label: Mapped[str] = mapped_column(String)

    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
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

    cash_flow: Mapped["CashFlowStatement"] = relationship(
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


    report_id: Mapped[int] = mapped_column(ForeignKey("company_report.id"))
    company_report: Mapped["CompanyReport"] = relationship(back_populates="periods")

class CompanyReport(TableBase):
    __tablename__ = "company_report"

    report_type: Mapped[str] = mapped_column(String)  
    # "annual", "quarterly", "prospectus", etc.
    report_year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    total_pages: Mapped[int] = mapped_column(Integer)
    file_key: Mapped[str] = mapped_column(String)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company : Mapped["Company"] = relationship(back_populates="reports")

    periods: Mapped[list["ReportingPeriod"]] = relationship(
        back_populates="company_report",
        cascade="all, delete-orphan"
    )
    report_sources: Mapped[list["SourceFragment"]] = relationship(
        back_populates="company_report",
        cascade="all, delete-orphan"
    )

class Company(TableBase):
    __tablename__ = "company"

    company_id: Mapped[str] = mapped_column(String(100), unique=True)  
    # ticker, registration number, etc.

    company_name: Mapped[str] = mapped_column(String(200))

    reports: Mapped[list["CompanyReport"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )

"""
Association table

class SourceLink(TableBase):
    __tablename__ = "source_link"

    source_fragment_id: Mapped[int] = mapped_column(
        ForeignKey("source_fragment.id", ondelete="CASCADE"),
        primary_key=True,
    )

    owner_id: Mapped[int] = mapped_column(primary_key=True)
    owner_type: Mapped[str] = mapped_column(primary_key=True)


class CompanyReport(TableBase):
    __tablename__ = "company_report"

    id: Mapped[int] = mapped_column(primary_key=True)

    report_sources: Mapped[list["SourceFragment"]] = relationship(
        secondary="source_link",
        primaryjoin=(
            "and_(CompanyReport.id == foreign(SourceLink.owner_id), "
            "SourceLink.owner_type == 'company_report')"
        ),
        secondaryjoin="SourceFragment.id == SourceLink.source_fragment_id",
        viewonly=False,
    )

"""