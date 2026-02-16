from pydantic import BaseModel, EmailStr, Field


class RequestContact(BaseModel):
    name: str = Field(min_length=6)
    email: EmailStr
    message: str = Field(min_length=10)
