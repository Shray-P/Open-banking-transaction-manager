from app.config import get_settings


def test_env_loaded():
    settings = get_settings()

    assert settings.plaid_client_id is not None
    assert settings.plaid_secret is not None
    assert (
        settings.plaid_env == "sandbox"
        or settings.plaid_env == "development"
        or settings.plaid_env == "production"
    )
