from sqlmodel import Field, SQLModel


class Item(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    access_token: str
