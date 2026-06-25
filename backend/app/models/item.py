from pydantic import BaseModel


class Item(BaseModel):
    id: str
    access_token: str
    institution_name: str
