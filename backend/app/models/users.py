import uuid
from pydantic import BaseModel


class User(BaseModel):
    id: uuid.UUID
    name: str


class UserCreateRequest(BaseModel):
    name: str


class UserCreateResponse(BaseModel):
    user: User
