from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class RefreshTokenResponse(BaseModel):
    access_token: AccessToken
