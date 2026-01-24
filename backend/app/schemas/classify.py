from enum import StrEnum, auto
from pydantic import BaseModel, Field

class PossibleSignal(StrEnum):
    business_strategy = auto()
    growth_potential  = auto()
    risk_analysis = auto()
    qualitative_performance = auto()

class SentimentSignal(BaseModel):
    signals : list[PossibleSignal] = Field(...)