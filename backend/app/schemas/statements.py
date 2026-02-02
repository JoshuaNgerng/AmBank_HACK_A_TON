from pydantic import BaseModel, Field
from app.schemas.shared_identifier import IdentifierBase, DataListBase

class IncomeStatement(IdentifierBase):
    revenue: float = Field(
        ...,
        description="Total revenue or sales for the period"
    )
    cost: float = Field(
        ...,
        description="Total cost of goods sold or cost of revenue for the period"
    )
    gross_profit: float = Field(
        ...,
        description="Revenue minus cost of goods sold"
    )

    operating_expenses: float = Field(
        ...,
        description="Total operating expenses excluding cost of goods sold"
    )
    operating_income: float = Field(
        ...,
        description="Operating profit after deducting operating expenses from gross profit"
    )

    finance_costs: float = Field(
        ...,
        description="Interest and other financing-related expenses"
    )
    profit_before_tax: float = Field(
        ...,
        description="Earnings before income tax expense"
    )

    tax: float = Field(
        ...,
        description="Income tax expense for the period"
    )
    net_income: float = Field(
        ...,
        description="Final profit or loss attributable to the company after tax"
    )

    eps: float = Field(
        ...,
        description="Earnings per share for the period"
    )

class IncomeStatements(DataListBase[IncomeStatement]):
    data: list[IncomeStatement] = Field(default_factory=list)

class BalanceSheet(IdentifierBase):
    current_assets: float = Field(
        ...,
        description="Total assets expected to be converted to cash or used within one year"
    )
    non_current_assets: float = Field(
        ...,
        description="Total long-term assets not expected to be converted to cash within one year"
    )
    total_assets: float = Field(
        ...,
        description="Sum of current and non-current assets"
    )

    current_liabilities: float = Field(
        ...,
        description="Total obligations due to be settled within one year"
    )
    non_current_liabilities: float = Field(
        ...,
        description="Total long-term obligations due after one year"
    )
    total_liabilities: float = Field(
        ...,
        description="Sum of current and non-current liabilities"
    )

    equity: float = Field(
        ...,
        description="Total shareholders’ equity, representing assets minus liabilities"
    )

class BalanceSheets(DataListBase[BalanceSheet]):
    data: list[BalanceSheet] = Field(default_factory=list)

class CashFlowStatement(IdentifierBase):
    operating_cash_flow: float = Field(
        ...,
        description="Net cash generated from or used in core operating activities"
    )
    investing_cash_flow: float = Field(
        ...,
        description="Net cash used in or generated from investing activities such as asset purchases or sales"
    )
    financing_cash_flow: float = Field(
        ...,
        description="Net cash generated from or used in financing activities such as debt, equity, or dividends"
    )

    net_change_in_cash: float = Field(
        ...,
        description="Net increase or decrease in cash during the period"
    )
    beginning_cash: float = Field(
        ...,
        description="Cash and cash equivalents at the beginning of the period"
    )
    ending_cash: float = Field(
        ...,
        description="Cash and cash equivalents at the end of the period"
    )

class CashFlowStatments(DataListBase[CashFlowStatement]):
    data: list[CashFlowStatement] = Field(default_factory=list)
