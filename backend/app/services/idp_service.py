from abc import ABC
from authlib.integrations.starlette_client import OAuth
from fastapi import Request
from jwt import PyJWKClient
import jwt
from pydantic import BaseModel
from app.config import get_settings

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


oauth.register(
    name="microsoft",
    client_id=get_settings().microsoft_auth_client_id,
    client_secret=get_settings().microsoft_auth_client_secret,
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration",
)


class IDPUserInfo(BaseModel):
    provider: str
    provider_id: str
    name: str
    email: str


class IdentityProvider(ABC):
    def __init__(self, name: str, client):
        self.name = name
        self.client = client

    async def redirect(self, request: Request, redirect_uri):
        return await self.client.authorize_redirect(
            request,
            redirect_uri=redirect_uri,
            prompt="select_account",
        )

    async def authenticate(self, request: Request) -> IDPUserInfo:
        token = await self.client.authorize_access_token(request)
        assert token
        user_info = token["userinfo"]
        assert user_info

        return self._user_info_from_dict(user_info)

    def _user_info_from_dict(self, user_info: dict[str, str]):
        return IDPUserInfo(
            provider=self.name,
            provider_id=user_info["sub"],
            name=user_info["name"],
            email=user_info["email"],
        )


class GoogleIDP(IdentityProvider):
    def __init__(self):
        super().__init__("google", oauth.google)


class MicrosoftIDP(IdentityProvider):
    def __init__(self):
        super().__init__("microsoft", oauth.microsoft)

    async def authenticate(self, request: Request) -> IDPUserInfo:
        code = request.query_params["code"]

        token_info = await self.client.fetch_access_token(
            code=code,
            redirect_uri=str(request.url_for(
                "auth_idp_callback", provider=self.name)),
        )

        id_token = token_info["id_token"]

        jwks_url = "https://login.microsoftonline.com/common/discovery/v2.0/keys"

        jwks_client = PyJWKClient(jwks_url)

        signing_key = jwks_client.get_signing_key_from_jwt(
            id_token,
        )

        claims = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=get_settings().microsoft_auth_client_id,
            options={"require": ["exp", "aud"]},
        )

        assert (
            claims["iss"] == f"https://login.microsoftonline.com/{claims['tid']}/v2.0"
        )

        return self._user_info_from_dict(claims)


IDENTITY_PROVIDERS = {"google": GoogleIDP(), "microsoft": MicrosoftIDP()}
