from pydantic import BaseModel, EmailStr

class UserQuestion(BaseModel):
    chat_history: list[str]
    

