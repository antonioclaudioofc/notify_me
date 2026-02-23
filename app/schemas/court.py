from pydantic import BaseModel


class Court(BaseModel):
    id: int
    name: str
