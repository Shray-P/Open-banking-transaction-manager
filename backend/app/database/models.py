from sqlmodel import Field, SQLModel, table

import uuid
from datetime import datetime


class Item(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    institution_name: str
    access_token: str


class Account(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str
    item_id: str = Field(default=None, foreign_key="item.id")


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    password_hash: str | None
    google_id: str | None


class LoginCode(SQLModel, table=True):
    code: str = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(default=None)
    expire: datetime
