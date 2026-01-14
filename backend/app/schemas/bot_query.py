from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator

class AnalysisType(str, Enum):
    descriptive = "descriptive"
    profitability = "profitability"
    liquidity = "liquidity"
    leverage = "leverage"
    cash_flow_quality = "cash_flow_quality"
    growth = "growth"
    financial_health = "financial_health"
    trend_analysis = "trend_analysis"
    comparison = "comparison"

class TimeMode(str, Enum):
    single_period = "single_period"
    comparison = "comparison"
    trend = "trend"
    unspecified = "unspecified"

class ComparisonTarget(str, Enum):
    prior_period = "prior_period"
    peer = "peer"
    industry = "industry"

class Metric(str, Enum):
    revenue = "revenue"
    gross_profit = "gross_profit"
    operating_income = "operating_income"
    net_income = "net_income"
    operating_cash_flow = "operating_cash_flow"
    free_cash_flow = "free_cash_flow"
    gross_margin = "gross_margin"
    operating_margin = "operating_margin"
    net_margin = "net_margin"
    current_ratio = "current_ratio"
    quick_ratio = "quick_ratio"
    debt_to_equity = "debt_to_equity"
    interest_coverage = "interest_coverage"
    roe = "roe"
    roa = "roa"

class CompanyReference(BaseModel):
    raw_reference: Optional[str] = Field(
        None,
        description="Exactly how the user referred to the company"
    )
    ticker: Optional[str] = Field(
        None,
        description="Always null in Stage 1"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="LLM confidence in company reference extraction"
    )

class AnalysisIntent(BaseModel):
    type: AnalysisType
    subtype: Optional[str] = None

class TimeScope(BaseModel):
    mode: TimeMode
    years: List[Union[int, str]] = Field(
        description="Fiscal years or symbolic values like 'latest', 'previous', 'last_5_years'"
    )

    @field_validator("years")
    @classmethod
    def validate_years(cls, v):
        if not v:
            raise ValueError("years must not be empty")
        return v

class Comparison(BaseModel):
    enabled: bool
    target: Optional[ComparisonTarget] = None

    @field_validator("target")
    @classmethod
    def validate_target(cls, v, info):
        enabled = info.data.get("enabled")
        if enabled and v is None:
            raise ValueError("comparison.target is required when comparison.enabled is true")
        if not enabled and v is not None:
            raise ValueError("comparison.target must be null when comparison.enabled is false")
        return v

class QueryPlan(BaseModel):
    company: CompanyReference
    analysis: AnalysisIntent
    metrics: List[Metric]
    time: TimeScope
    comparison: Comparison
    assumptions: List[str] = Field(default_factory=list)

    @field_validator("metrics")
    @classmethod
    def validate_metrics(cls, v):
        if not v:
            raise ValueError("At least one metric must be selected")
        return v
