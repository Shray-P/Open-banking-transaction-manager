from typing import Annotated
import uuid
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database.database import add_user, create_tables, get_session, get_user
from app.models.tokens import AccessToken
from app.models.users import (
    UserCreateRequest,
    UserCreateResponse,
    User,
    UserLoginRequest,
    UserLoginResponse,
)
from app.models.item import ItemCreateRequest, ItemCreateResponse
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_password_hash,
    get_user_by_access_token,
)
from app.services.plaid_service import (
    create_plaid_link_token,
    get_plaid_client,
    get_plaid_item,
)

create_tables()

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@app.get("", response_model=str)
def root():
    return "Bank transaction tracker!!"


@app.post("/token", tags=["Token"])
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session=Depends(get_session),
) -> AccessToken | None:

    user = authenticate_user(session, form_data.username, form_data.password)

    if user is None:
        return None

    access_token = create_access_token(user)

    return access_token


@app.get("/user/me", response_model=User, tags=["User"])
def get_me(token: Annotated[str, Depends(oauth2_scheme)], session=Depends(get_session)):
    return get_user_by_access_token(session, token)


@app.post("/user/create", response_model=UserCreateResponse, tags=["User"])
def create_user(request: UserCreateRequest, session=Depends(get_session)):
    user = User(id=uuid.uuid4(), name=request.name)

    add_user(session, user, create_password_hash(request.password))

    return UserCreateResponse(user=user)


@app.post("/user/login", response_model=UserLoginResponse, tags=["User"])
def login_user(user_login: UserLoginRequest, session=Depends(get_session)):
    user = authenticate_user(session, user_login.name, user_login.password)

    if user is None:
        return None

    access_token = create_access_token(user)

    return UserLoginResponse(user=user, access_token=access_token)


@app.get("/link/request-token", tags=["Link"])
def request_link_token(client=Depends(get_plaid_client)):
    token = create_plaid_link_token(client)
    return token


@app.post("/items/create", response_model=ItemCreateResponse, tags=["Items"])
def create_item(request: ItemCreateRequest, client=Depends(get_plaid_client)):
    item = get_plaid_item(client, request.public_token)
    return ItemCreateResponse(id=item.id, institution_name=item.institution_name)
