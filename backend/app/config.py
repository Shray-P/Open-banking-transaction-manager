from typing import Optional, Literal
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    plaid_client_id: Optional[str] = None
    plaid_secret: Optional[str] = None
    plaid_env: Optional[Literal["sandbox", "development", "production"]] = None
    dev_database_url: Optional[str] = None
    test_database_url: Optional[str] = None
    secret_key: Optional[str] = None
    signing_algorithm: Optional[str] = None
    google_auth_client_id: Optional[str] = None
    google_auth_client_secret: Optional[str] = None
    microsoft_auth_client_id: Optional[str] = None
    microsoft_auth_client_secret: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
