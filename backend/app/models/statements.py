from decimal import Decimal
from typing import Any, TYPE_CHECKING
from sqlalchemy import Integer, Float, String, Numeric, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import TableBase
from models.report import ReportAnalysis

class IncomeStatement(TableBase):
    __tablename__ = "income_statements"

    revenue: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True)
    cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True)
    gross_profit: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True)

    operating_expenses: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True)
    operating_income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True)

    finance_costs: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True)
    profit_before_tax: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True)

    tax: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True)
    net_income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True)

    eps: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=True)

    period: Mapped[str] = mapped_column(String, nullable=True)

    sources: Mapped[Any] = mapped_column(JSON, nullable=True)

    report_analysis_id: Mapped[int] = mapped_column(
        ForeignKey("report_analysis.id"),
        unique=True   # enforces one-to-one in DB
    )

    report_analysis: Mapped["ReportAnalysis"] = relationship(
        back_populates="income_statement"
    )

class BalanceSheet(TableBase):
    __tablename__ = "balance_sheets"

    current_assets: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )
    non_current_assets: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )
    total_assets: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )

    current_liabilities: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )
    non_current_liabilities: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )
    total_liabilities: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )

    equity: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )

    period: Mapped[str] = mapped_column(String, nullable=True)

    sources: Mapped[Any] = mapped_column(JSON, nullable=True)

    report_analysis_id: Mapped[int] = mapped_column(
        ForeignKey("report_analysis.id"),
        unique=True
    )

    report_analysis: Mapped["ReportAnalysis"] = relationship(
        back_populates="balance_sheet"
    )

class CashFlowStatement(TableBase):
    __tablename__ = "cash_flow_statements"

    operating_cash_flow: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )
    investing_cash_flow: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )
    financing_cash_flow: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )

    net_change_in_cash: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )
    beginning_cash: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )
    ending_cash: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=True
    )

    period: Mapped[str] = mapped_column(String, nullable=True)

    sources: Mapped[Any] = mapped_column(JSON, nullable=True)

    report_analysis_id: Mapped[int] = mapped_column(
        ForeignKey("report_analysis.id"),
        unique=True
    )

    report_analysis: Mapped["ReportAnalysis"] = relationship(
        back_populates="cash_flow"
    )