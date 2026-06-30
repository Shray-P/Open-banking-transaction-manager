from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.item import ItemCreateRequest, ItemCreateResponse
from app.services.plaid_service import (
    create_plaid_link_token,
    get_plaid_client,
    get_plaid_item,
)

app = FastAPI(root_path="/api")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("", response_model=str)
def root():
    return "Bank transaction tracker!!"


@app.get("/link/request-token")
def request_link_token(client=Depends(get_plaid_client)):
    token = create_plaid_link_token(client)
    return token


@app.post("/items/create", response_model=ItemCreateResponse)
def create_item(request: ItemCreateRequest, client=Depends(get_plaid_client)):
    item = get_plaid_item(client, request.public_token)

    return ItemCreateResponse(id=item.id, institution_name=item.institution_name)
