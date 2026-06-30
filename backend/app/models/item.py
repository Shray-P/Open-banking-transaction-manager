from pydantic import BaseModel


class Item(BaseModel):
    id: str
    access_token: str
    institution_name: str


class ItemCreateRequest(BaseModel):
    public_token: str


class ItemCreateResponse(BaseModel):
    id: str
    institution_name: str
