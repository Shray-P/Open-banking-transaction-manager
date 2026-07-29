from pydantic import BaseModel
import uuid
from datetime import datetime

from app.models.tokens import AccessToken


class LoginCode(BaseModel):
    code: str
    user_id: uuid.UUID
    expire: datetime


class LoginCodeRequest(BaseModel):
    code: str


class LoginCodeResponse(BaseModel):
    token: AccessToken
