from pydantic import BaseModel


class Arena(BaseModel):
    id: int
    name: str
