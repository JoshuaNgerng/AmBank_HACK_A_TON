from decimal import Decimal
from enum import Enum
from sqlalchemy import String, Integer, Numeric, Float, Enum as ENUM, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import TableBase
from app.models.report import Company

class SentimentTopic(Enum):
    FINANCIAL_PERFORMANCE = "FINANCIAL_PERFORMANCE"
    REVENUE_GROWTH = "REVENUE_GROWTH"
    PROFITABILITY_MARGINS = "PROFITABILITY_MARGINS"
    BALANCE_SHEET_LIQUIDITY = "BALANCE_SHEET_LIQUIDITY"
    CASH_FLOW = "CASH_FLOW"
    CAPITAL_ALLOCATION = "CAPITAL_ALLOCATION"

    STRATEGY_EXECUTION = "STRATEGY_EXECUTION"
    GROWTH_EXPANSION = "GROWTH_EXPANSION"
    DIGITAL_TRANSFORMATION = "DIGITAL_TRANSFORMATION"
    COST_OPTIMIZATION = "COST_OPTIMIZATION"

    MARKET_POSITION = "MARKET_POSITION"
    COMPETITION = "COMPETITION"
    CUSTOMER_DEMAND = "CUSTOMER_DEMAND"
    PRICING_POWER = "PRICING_POWER"

    MANAGEMENT_GOVERNANCE = "MANAGEMENT_GOVERNANCE"
    LEADERSHIP_CHANGES = "LEADERSHIP_CHANGES"
    ESG_SUSTAINABILITY = "ESG_SUSTAINABILITY"

    REGULATORY_LEGAL = "REGULATORY_LEGAL"
    MACROECONOMIC = "MACROECONOMIC"

    RISK_OUTLOOK = "RISK_OUTLOOK"

class SentimentLabel(Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

class SentimentAnalysis(TableBase):
    sentiment_topic: Mapped[SentimentTopic] = mapped_column(
        ENUM(
            SentimentTopic,
            name="sentiment_topic_enum",
            native_enum=True,     # use PostgreSQL ENUM
            create_constraint=True
        ),
        nullable=False
    )
    sentiment: Mapped[SentimentLabel] = mapped_column(
        ENUM(
            SentimentLabel,
            name="sentiment_degree_enum",
            native_enum=True,     # use PostgreSQL ENUM
            create_constraint=True
        ),
        nullable=False
    )
    score: Mapped[float] = mapped_column(Float, default=0.0)
    rationale: Mapped[str] = mapped_column()
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company: Mapped['Company'] = relationship()
    # citations: []