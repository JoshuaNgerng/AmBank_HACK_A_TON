from enum import Enum 
from pydantic import BaseModel, Field
from app.models.source import PossibleSignal, PossibleStatement

class ClassifyBase(BaseModel):
    confidence: float = Field(
        default=0.0,
        description="Confidence score between 0 and 1 for the accuracy of this classification"
    )
    remarks: str | None = Field(default=None, description="Reasoning for the classification")

class SentimentSignal(ClassifyBase):
    signals : list[PossibleSignal] = Field(
        default=[], description="all possible signal that appear in the text"
    )

class Statement(ClassifyBase):
    type: PossibleStatement = Field(..., description="Possible Statement")

class SectionTypes(Enum):
    text = "text"
    doc_title = "doc_title"
    paragraph_title = "paragraph_title"
    table = "table"

class TextSection(BaseModel):
    type: SectionTypes = SectionTypes.text
    confidence: float = 0.0
    content: str = ''

