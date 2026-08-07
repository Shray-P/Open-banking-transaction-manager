import uuid
from pydantic import BaseModel

from app.models.tokens import AccessToken


class User(BaseModel):
    id: uuid.UUID
    name: str


class UserCreateRequest(BaseModel):
    name: str
    password: str


class UserCreateResponse(BaseModel):
    user: User


class UserLoginRequest(BaseModel):
    name: str
    password: str


class UserLoginResponse(BaseModel):
    user: User
    access_token: AccessToken
