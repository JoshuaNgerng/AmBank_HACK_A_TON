from decimal import Decimal
from typing import Any, TYPE_CHECKING
from sqlalchemy import Integer, Float, String, Numeric, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declared_attr
from app.models.source import FinicialElementBase 

class IncomeStatement(FinicialElementBase):
    __tablename__ = "income_statement"

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

class BalanceSheet(FinicialElementBase):
    __tablename__ = "balance_sheet"

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


class CashFlowStatement(FinicialElementBase):
    __tablename__ = "cash_flow_statement"

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
