from pydantic import BaseModel, EmailStr, Field


class RequestEmailVerification(BaseModel):
    email: EmailStr
    token: str
