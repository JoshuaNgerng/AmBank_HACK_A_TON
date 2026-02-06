from datetime import datetime, date as Date
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.schemas.naming_utlis import to_camel

# ---------- Core Entities ----------

class CompanyInfo(BaseModel):
    id: int = Field(..., description="Internal numeric identifier for the company")
    name: str | None = Field(default=None, description="Registered legal name of the company")
    industry: str | None = Field(default=None, description="Primary industry or sector the company operates in")
    company_id: str | None = Field(default=None, description="Official company registration or incorporation number")

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

class Citation(BaseModel):
    id: str = Field(..., description="Unique citation identifier")
    title: str = Field(..., description="Title of the cited document or source")
    source: str = Field(..., description="Publishing entity or data provider")
    date: Date = Field(..., description="Publication or release date of the source")
    url: str = Field(..., description="Public URL where the source can be accessed")


# ---------- Executive Summary ----------

class ExecutiveSummary(BaseModel):
    overview: str = Field(..., description="High-level narrative summary of company performance and outlook")
    keyPositives: List[str] = Field(..., description="List of major strengths or favorable observations")
    keyConcerns: List[str] = Field(..., description="List of key risks or areas of concern")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score associated with the summary assessment")
    riskLevel: Literal["low", "moderate", "high"] = Field(..., description="Overall qualitative risk level (e.g. low, moderate, high)")


# ---------- Methodology ----------

class Methodology(BaseModel):
    signalSelection: str = Field(..., description="Method used to select relevant signals or evidence")
    ordering: str = Field(..., description="Ordering logic applied to signals or insights")
    lookbackYears: int = Field(..., description="Number of historical years considered in the analysis")


# ---------- Business Strategy ----------

class StrategySignal(BaseModel):
    year: int = Field(default=int(datetime.now().year) - 1, description="Calendar year the signal pertains to")
    summary: str = Field(..., description="Concise description of the strategic signal")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score for the signal interpretation")
    citations: List[str] = Field(default_factory=list, description="List of citation IDs supporting this signal")

    @field_validator('summary', mode='before')
    def check_null(v): return '' if v is None else v

    @field_validator('year', mode='before')
    def check_null_yr(v): return int(datetime.now().year) - 1 if v is None else v

class BusinessStrategyTheme(BaseModel):
    theme: str = Field(..., description="Strategic theme or focus area")
    consistencyScore: float = Field(..., ge=0, le=1, description="Score indicating consistency of the strategy over time")
    trend: str = Field(..., description="Observed trend direction (e.g. up, down, stable)")

class BusinessStrategy(BusinessStrategyTheme):
    signals: List[StrategySignal] = Field(..., description="Supporting signals for the strategic theme")


# ---------- Growth Potential ----------

class GrowthPotential(BaseModel):
    growth_level: str = Field(..., description="Qualitative growth classification")
    growth_score: float = Field(..., ge=0, le=1, description="Quantitative score representing growth potential")
    confidence: float = Field(..., ge=0, le=1, description="Confidence level in the growth assessment")
    growth_drivers: List[str] = Field(..., description="Primary factors driving growth")
    constraints: List[str] = Field(..., description="Key constraints or limiting factors")
    summary: str = Field(..., description="Narrative explanation of growth outlook")
    citations: List[str] = Field(default_factory=list, description="Citation IDs supporting the growth assessment")

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    @field_validator('summary', mode='before')
    def check_null(v): return '' if v is None else v

# ---------- Sentiment Analysis ----------

class SentimentAnalysis(BaseModel):
    topic: str = Field(..., description="Topic or dimension being evaluated")
    sentiment_label: str = Field(..., description="Overall sentiment classification")
    sentiment_score: float = Field(..., ge=-1, le=1, description="Numerical sentiment score")
    confidence_level: str = Field(..., description="Confidence level of the sentiment assessment")
    rationale: str = Field(..., description="Explanation supporting the sentiment evaluation")
    supporting_signals: List[str] = Field(..., description="Signal identifiers used to derive sentiment")
    citations: List[str] = Field(default_factory=list, description="Citation IDs supporting the sentiment analysis")

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

# ---------- Risk Assessment ----------

class RiskFactor(BaseModel):
    name: str = Field(..., description="Name of the risk factor", alias='topic')
    score: int = Field(..., description="Risk score for this factor", alias='risk_score')
    # trend: str = Field(..., description="Observed risk trend direction")
    severity: float = Field(..., ge=0, le=1, description="Severity level of the risk", alias='tone')
    management_tone: str | None = Field(default=None, description="Observed management response posture", alias="managementTone")
    key_signals: List[str] = Field(..., description="Signals indicating the presence of this risk")
    summary: str = Field(..., description="Brief explanation of the risk factor")
    citations: List[str] = Field(default_factory=list, description="Citation IDs supporting the risk assessment")

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    @field_validator('summary', mode='before')
    def check_null(v): return '' if v is None else v

class RiskAssessmentBase(BaseModel):
    overallScore: int = Field(..., description="Aggregate risk score for the company")
    posture: str = Field(..., description="Overall qualitative risk posture")
    summary: str = Field(..., description="Narrative summary of the company’s risk profile")

    @field_validator('summary', mode='before')
    def check_null(v): return '' if v is None else v

class RiskAssessment(RiskAssessmentBase):
    factors: List[RiskFactor] = Field(..., description="Individual contributing risk factors")


# ---------- Details ----------

class Details(BaseModel):
    methodology: Methodology = Field(..., description="Methodological assumptions and configuration")
    businessStrategy: List[BusinessStrategy] = Field(..., description="Analysis of business strategy themes")
    growthPotential: List[GrowthPotential] = Field(..., description="Growth potential assessments")
    sentimentAnalysis: List[SentimentAnalysis] = Field(..., description="Sentiment analysis across key topics")
    riskAssessment: RiskAssessment = Field(..., description="Comprehensive risk assessment")


# ---------- Root Model ----------

class CompanyAnalysis(BaseModel):
    company: CompanyInfo = Field(..., description="Company metadata")
    asOf: datetime = Field(..., description="Timestamp indicating when the analysis is valid as of")
    lookbackYears: int = Field(..., description="Primary historical lookback period for the analysis")
    executiveSummary: ExecutiveSummary = Field(..., description="High-level executive summary of findings")
    details: Details = Field(..., description="Detailed analytical sections")
    citations: List[Citation] = Field(..., description="Reference materials used throughout the analysis")

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

class CompanyAnalysisResult(BaseModel):
    success: bool = Field(default=True)
    data: CompanyAnalysis = Field(...)
    error: str | None = Field(default=None)

class CompanyListing(BaseModel):
    success: bool = Field(default=True)
    data: list[CompanyInfo] = Field(default_factory=list)
    error: str | None = Field(default=None)

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)