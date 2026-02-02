from typing import Generic, TypeVar
from pydantic import BaseModel, Field

class IdentifierBase(BaseModel): 
    period_label: str = Field(
        ...,
        description="Human-readable label for the reporting period, e.g. 'Q1 2024', 'FY 2023'"
    )
    year: int | None = Field(
        default=None,
        description="Calendar or fiscal year the statement or text refers to"
    )
    period_type: str = Field(
        ...,
        description="Type of period, e.g. 'quarterly', 'annual', 'trailing twelve months'"
    )
    confidence: float = Field(
        default=0.0,
        description="Model confidence score between 0 and 1 for the accuracy of this statement"
    )
    remarks: str = Field(
        ...,
        description="Any notes, assumptions, or clarifications about this statement"
    )

TStatement = TypeVar("TStatement", bound=IdentifierBase)

class DataListBase(BaseModel, Generic[TStatement]):
    data: list[TStatement] = Field(default_factory=list)
