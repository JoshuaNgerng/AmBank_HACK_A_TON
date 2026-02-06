from pydantic import BaseModel, Field

class Context(BaseModel):
    company_id: int = Field(..., alias='selectedCompany')

class UserQuestion(BaseModel):
    message: str
    chat_history: list[str] = Field(..., alias='conversationHistory')
    context: Context | None = Field(default=None)

class ChatResponse(BaseModel):
    success: bool
    message: str
    error: str | None = None    
    context: Context | None = Field(default=None)

