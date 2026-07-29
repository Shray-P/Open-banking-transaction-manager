from datetime import datetime, timezone, timedelta
from pydantic import BaseModel
import jwt
from sqlmodel import Session
from pwdlib import PasswordHash
import uuid

from app.config import get_settings
from app.models.login_code import LoginCode
from app.models.users import User
from app.database.database import get_user, get_user_by_name, get_user_password_hash
from app.models.tokens import AccessToken


ALGORITHM = get_settings().signing_algorithm
SECRET_KEY = get_settings().secret_key

ACCESS_TOKEN_EXPIRE_MINUTES = 30


password_hash = PasswordHash.recommended()


class AccessTokenData(BaseModel):
    sub: str
    exp: float


class RefreshTokenData(BaseModel):
    sub: str
    exp: float


def create_password_hash(password: str):
    return password_hash.hash(password)


def create_access_token(user: User):
    assert SECRET_KEY
    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    data = {"sub": str(user.id), "exp": expire_time}
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return AccessToken(access_token=encoded_jwt, token_type="bearer")


def decode_access_token(token: str):
    assert ALGORITHM
    assert SECRET_KEY
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    accessTokenData = AccessTokenData(
        sub=payload["sub"], exp=float(payload["exp"]))

    return accessTokenData


def authenticate_user(session: Session, name: str, password: str) -> User | None:
    user = get_user_by_name(session, name)

    if user is None:
        return None

    hashed_password = get_user_password_hash(session, user.id)

    if hashed_password is None:
        return None

    if not password_hash.verify(password, hashed_password):
        return None

    return user


def get_user_by_access_token(session: Session, token: str) -> User | None:
    tok_data = decode_access_token(token)
    user = get_user(session, uuid.UUID(tok_data.sub))
    return user


def is_login_code_valid(login_code: LoginCode):
    return login_code.expire <= datetime.now()
