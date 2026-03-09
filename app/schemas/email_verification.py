from pydantic import BaseModel, EmailStr


class RequestEmailVerification(BaseModel):
    email: EmailStr
    token: str
