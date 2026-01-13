from datetime import date
from decimal import Decimal
from typing import Any, TYPE_CHECKING
from sqlalchemy import Integer, Float, Date, Numeric, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import TableBase

if TYPE_CHECKING:
    from models.report import ReportAnalysis

class IncomeStatement(TableBase):
    __tablename__ = "income_statements"

    revenue: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    gross_profit: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    operating_expenses: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    operating_income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    finance_costs: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    profit_before_tax: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    tax: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    net_income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    eps: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)

    period: Mapped[date] = mapped_column(Date, nullable=False)

    metadata: Mapped[Any] = mapped_column(JSON, nullable=True)

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
        Numeric(15, 2), nullable=False
    )
    non_current_assets: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )
    total_assets: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )

    current_liabilities: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )
    non_current_liabilities: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )
    total_liabilities: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )

    equity: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )

    period: Mapped[date] = mapped_column(Date, nullable=False)

    metadata: Mapped[Any] = mapped_column(JSON, nullable=True)

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
        Numeric(15, 2), nullable=False
    )
    investing_cash_flow: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )
    financing_cash_flow: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )

    net_change_in_cash: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )
    beginning_cash: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )
    ending_cash: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )

    period: Mapped[date] = mapped_column(Date, nullable=False)

    metadata: Mapped[Any] = mapped_column(JSON, nullable=True)

    report_analysis_id: Mapped[int] = mapped_column(
        ForeignKey("report_analysis.id"),
        unique=True
    )

    report_analysis: Mapped["ReportAnalysis"] = relationship(
        back_populates="cash_flow"
    )