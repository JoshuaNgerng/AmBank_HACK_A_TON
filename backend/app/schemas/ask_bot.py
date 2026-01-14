from pydantic import BaseModel, EmailStr

class UserQuestion(BaseModel):
    prompt: str

