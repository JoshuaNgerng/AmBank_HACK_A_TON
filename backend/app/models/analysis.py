from datetime import date
from enum import Enum as ENUM
from decimal import Decimal
from typing import Any, TYPE_CHECKING
from sqlalchemy import Integer, Float, Date, Numeric, JSON, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.source import FinancialElementBase 

class SentimentTopic(ENUM):
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

class SentimentLabel(ENUM):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

class DegreeLevelEnum(ENUM):
    VERY_LOW = "Very Low"
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    VERY_HIGH = "Very High"


class RiskTopics(str, ENUM):
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    LIQUIDITY = "liquidity"
    CREDIT = "credit"
    MARKET = "market"
    REGULATORY = "regulatory"
    LEGAL = "legal"
    COMPLIANCE = "compliance"
    CYBERSECURITY = "cybersecurity"
    TECHNOLOGY = "technology"
    DATA_PRIVACY = "data_privacy"
    REPUTATIONAL = "reputational"
    ESG = "esg"
    ENVIRONMENTAL = "environmental"
    SOCIAL = "social"
    GOVERNANCE = "governance"
    SUPPLY_CHAIN = "supply_chain"
    GEOPOLITICAL = "geopolitical"
    MACROECONOMIC = "macroeconomic"
    HUMAN_CAPITAL = "human_capital"
    HEALTH_AND_SAFETY = "health_and_safety"
    FRAUD = "fraud"
    BUSINESS_CONTINUITY = "business_continuity"

class RiskTone(ENUM):
    proactive = "proactive"
    defensive = "defensive"
    vague = "vague"
    transparent = "transparent"
    mixed = "mixed"

class BusinessStrategy(FinancialElementBase):
    __tablename__ = "business_strategy"

    primary_theme: Mapped[str] = mapped_column(
        String, index=True
    )

    strategic_direction: Mapped[str | None] = mapped_column(String)
    summary: Mapped[str | None] = mapped_column(String)

    core_focus: Mapped[list[str]] = mapped_column(JSON, default=[])
    competitive_advantages: Mapped[list[str]] = mapped_column(JSON, default=[])

    execution_risk: Mapped[str] = mapped_column(
        String, default="Unknown"
    )

class RiskAnalysis(FinancialElementBase):
    __tablename__ = "risk_analysis"

    topic: Mapped[RiskTopics] = mapped_column(
        Enum(
            RiskTopics,
            name="risk_topics_enum",
            native_enum=True,     # use PostgreSQL ENUM
            create_constraint=True,
        ),
        nullable=False
    )
    # Enum-like fields stored as strings
    risk_posture: Mapped[DegreeLevelEnum] = mapped_column(
        Enum(
            DegreeLevelEnum,
            name="degree_level_enum",
            native_enum=True,     # use PostgreSQL ENUM
            create_constraint=True
        ),
        nullable=False
    )
    risk_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0.0)
    tone: Mapped[RiskTone] = mapped_column(
        Enum(
            RiskTone,
            name="risk_tone_enum",
            native_enum=True,     # use PostgreSQL ENUM
            create_constraint=True
        ),
        nullable=False
    )

    # Array of strings stored as JSON
    key_risks: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])

    # Optional string
    risk_management_approach: Mapped[str | None] = mapped_column(String, nullable=True)


class QualitativePerformance(FinancialElementBase):
    __tablename__ = "qualitative_performance"

    # Enum-like fields stored as strings
    topic: Mapped[SentimentTopic] = mapped_column(
        Enum(
            SentimentTopic,
            name="sentiment_topic_enum",
            native_enum=True,     # use PostgreSQL ENUM
            create_constraint=True
        ),
        nullable=False
    )
    sentiment_label: Mapped[SentimentLabel] = mapped_column(
        Enum(
            SentimentLabel,
            name="sentiment_degree_enum",
            native_enum=True,     # use PostgreSQL ENUM
            create_constraint=True
        ),
        nullable=False
    )

    sentiment_score: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
    )
    confidence_level: Mapped[DegreeLevelEnum] = mapped_column(
        Enum(DegreeLevelEnum, name="degree_level_enum"),
        nullable=False
    )
    rationale: Mapped[str | None] = mapped_column(String, nullable=True)

    # Array of strings stored as JSON
    supporting_signals: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])


class GrowthPotential(FinancialElementBase):
    __tablename__ = "growth_potential"

    growth_level: Mapped[DegreeLevelEnum] = mapped_column(
        Enum(DegreeLevelEnum, name="degree_level_enum"),
        nullable=False
    )
    growth_score: Mapped[Decimal] = mapped_column(
        Numeric(4, 2), default=0.0
    )

    growth_drivers: Mapped[list[str]] = mapped_column(JSON, default=[])
    constraints: Mapped[list[str]] = mapped_column(JSON, default=[])

    summary: Mapped[str | None] = mapped_column(String)


