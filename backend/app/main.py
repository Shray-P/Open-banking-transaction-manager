from datetime import timedelta
from typing import Annotated
import uuid
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authlib.integrations.starlette_client import OAuth
from app.config import Settings, get_settings
from app.database.database import (
    add_login_code,
    add_user,
    create_tables,
    get_login_code,
    get_session,
    get_user,
    get_user_by_google_id,
)
from app.models.login_code import LoginCodeRequest, LoginCodeResponse
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
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    create_password_hash,
    get_user_by_access_token,
    is_login_code_valid,
)
from app.services.plaid_service import (
    create_plaid_link_token,
    get_plaid_client,
    get_plaid_item,
)
import secrets

create_tables()

app = FastAPI(root_path="/api")

assert SECRET_KEY

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
)

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

oauth = OAuth()
oauth.register(
    name="google",
    client_id=get_settings().google_auth_client_id,
    client_secret=get_settings().google_auth_client_secret,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)


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


@app.get("/auth/google")
async def auth_google(request: Request):
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri="http://localhost:8000/api/auth/google/callback",
        prompt="select_account",
    )


@app.get("/auth/google/callback", tags=["Auth"])
async def google_callback(request: Request, session=Depends(get_session)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"] or {}

    user = get_user_by_google_id(session, user_info["sub"])

    if user is None:
        user = User(id=uuid.uuid4(), name=user_info["email"])
        add_user(session, user, google_id=user_info["sub"])

    token = create_access_token(user)

    code = secrets.token_urlsafe()

    add_login_code(session, code, user, 1)

    return RedirectResponse(url=f"http://localhost:3000/auth/callback?code={code}")


@app.post("/auth/exchange-login-code", tags=["Auth"])
def exchange_login_code_for_token(
    request: LoginCodeRequest, session=Depends(get_session)
):
    login_code = get_login_code(session, request.code)
    if login_code is None:
        return None

    if is_login_code_valid(login_code):
        return None

    user = get_user(session, login_code.user_id)
    if user is None:
        return None

    token = create_access_token(user)

    return LoginCodeResponse(token=token)


@app.get("/user/me", response_model=User, tags=["User"])
def get_me(token: Annotated[str, Depends(oauth2_scheme)], session=Depends(get_session)):
    return get_user_by_access_token(session, token)


@app.post("/user/create", response_model=UserCreateResponse, tags=["User"])
def create_user(request: UserCreateRequest, session=Depends(get_session)):
    user = User(id=uuid.uuid4(), name=request.name)

    add_user(session, user, password_hash=create_password_hash(request.password))

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
