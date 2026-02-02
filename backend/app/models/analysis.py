from datetime import date
from decimal import Decimal
from typing import Any, TYPE_CHECKING
from sqlalchemy import Integer, Float, Date, Numeric, JSON, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.source import FinicialElementBase 

class BusinessStrategy(FinicialElementBase):
    __tablename__ = "business_strategy"

    # Basic fields
    summary: Mapped[str | None] = mapped_column(String, nullable=True)
    strategic_direction: Mapped[str | None] = mapped_column(String, nullable=True)

    # JSON fields for arrays of strings
    core_focus: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])
    competitive_advantages: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])

class RiskAnalysis(FinicialElementBase):
    __tablename__ = "risk_analysis"

    # Enum-like fields stored as strings
    risk_posture: Mapped[str] = mapped_column(String, nullable=False, default="Unknown")
    tone: Mapped[str] = mapped_column(String, nullable=False, default="Unknown")

    # Array of strings stored as JSON
    key_risks: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])

    # Optional string
    risk_management_approach: Mapped[str | None] = mapped_column(String, nullable=True)


class QualitativePerformance(FinicialElementBase):
    __tablename__ = "qualitative_performance"

    # Enum-like fields stored as strings
    sentiment: Mapped[str] = mapped_column(String, nullable=False, default="Unknown")
    confidence_level: Mapped[str] = mapped_column(String, nullable=False, default="Unknown")

    # Array of strings stored as JSON
    supporting_signals: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])


class GrowthPotential(FinicialElementBase):
    __tablename__ = "growth_potential"

    # Enum-like field stored as string
    level: Mapped[str] = mapped_column(String, nullable=False, default="Unknown")

    # Arrays of strings stored as JSON
    growth_drivers: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])
    constraints: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])

    # Optional string
    summary: Mapped[str | None] = mapped_column(String, nullable=True)

