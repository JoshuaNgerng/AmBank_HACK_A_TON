from pydantic import BaseModel, Field
from typing import Literal
from app.schemas.shared_identifier import IdentifierBase, DataListBase

class BusinessStrategy(IdentifierBase):
    summary: str | None = Field(
        None,
        description="A high-level narrative summary of the company's financial health and performance."
    )
    core_focus: list[str] = Field(
        ...,
        description="List of the company's primary business focuses or revenue-generating areas."
    )
    competitive_advantages: list[str] = Field(
        ...,
        description="List of factors that provide the company with an edge over its competitors, e.g., brand strength, technology, cost advantages."
    )
    strategic_direction: str | None = Field(
        None,
        description="Narrative of the company's planned strategic initiatives or future direction."
    )

class BusinessStrategyData(DataListBase[BusinessStrategy]):
    data: list[BusinessStrategy] = Field(default_factory=list)

class RiskAnalysis(IdentifierBase):
    risk_posture: Literal["Low", "Moderate", "High", "Unknown"] = Field(
        ...,
        description="Overall assessment of the company's risk exposure or vulnerability."
    )
    key_risks: list[str] = Field(
        ...,
        description="List of the most significant risks facing the company, e.g., operational, financial, regulatory."
    )
    risk_management_approach: str | None = Field(
        None,
        description="Narrative description of how the company manages or mitigates its key risks."
    )
    tone: Literal["Proactive", "Defensive", "Vague", "Transparent", "Mixed", "Unknown"] = Field(
        ...,
        description="The qualitative tone of the company's risk communication or strategy."
    )

class RiskAnalysisData(DataListBase[RiskAnalysis]):
    data: list[RiskAnalysis] = Field(default_factory=list)

class QualitativePerformance(IdentifierBase):
    sentiment: Literal["Positive", "Neutral", "Negative", "Mixed", "Unknown"] = Field(
        ...,
        description="Overall qualitative sentiment regarding the company's performance."
    )
    confidence_level: Literal["High", "Medium", "Low", "Unknown"] = Field(
        ...,
        description="Degree of confidence in the qualitative assessment based on available information."
    )
    supporting_signals: list[str] = Field(
        ...,
        description="Observable signals or qualitative indicators supporting the sentiment, such as management commentary, market reactions, or analyst opinions."
    )    

class QualitativePerformanceData(DataListBase[QualitativePerformance]):
    data: list[QualitativePerformance] = Field(default_factory=list)

class GrowthPotential(IdentifierBase):
    level: Literal["High", "Medium", "Low", "Unknown"] = Field(
        ...,
        description="Overall assessment of the company's growth potential based on market conditions, strategy, and performance."
    )
    growth_drivers: list[str] = Field(
        ...,
        description="Key factors expected to drive future growth, such as market expansion, product innovation, or pricing power."
    )
    constraints: list[str] = Field(
        ...,
        description="Primary limitations or challenges that may restrict growth, such as competition, regulatory issues, or capital constraints."
    )
    summary: str | None = Field(
        None,
        description="Optional narrative summary synthesizing the growth outlook, drivers, and constraints."
    )

class GrowthPotentialData(DataListBase[GrowthPotential]):
    data: list[GrowthPotential] = Field(default_factory=list)