from pydantic import BaseModel
from tracardi.domain.entity import Entity


class PushOverAuth(BaseModel):
    token: str
    user: str


class PushOverConfiguration(BaseModel):
    source: Entity
    message: str
