from pydantic import BaseModel

from app.schemas.arena import Arena
from app.schemas.court import Court
from app.schemas.user import User


class OwnerPromotionRequest(BaseModel):
    user: User
    arena: Arena


class NewCourtRequest(BaseModel):
    user: User
    arena: Arena
    court: Court
