from typing import Any
from pydantic import BaseModel, Field

class ResponseSchema(BaseModel):
    status: str = Field(...)
    status_code: int = Field(...)
    message: str = Field(...)
    payload: Any

class UserInfo(BaseModel):
    name: str
    email: str
    password: str

class Question(BaseModel):
    question: str