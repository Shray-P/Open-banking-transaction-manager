from typing import Optional, Literal
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    plaid_client_id: Optional[str] = None
    plaid_secret: Optional[str] = None
    plaid_env: Optional[Literal["sandbox", "development", "production"]] = None

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
