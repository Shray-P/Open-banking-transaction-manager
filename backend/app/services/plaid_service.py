import time

import plaid
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser


from app.config import get_settings


def get_plaid_client() -> plaid_api.PlaidApi:
    settings = get_settings()

    if settings.plaid_env != "sandbox":
        raise RuntimeError(
            f"Current Plaid environment: {settings.plaid_env} is not implemented"
        )

    configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox,
        api_key={
            "clientId": settings.plaid_client_id,
            "secret": settings.plaid_secret,
        },
    )

    api_client = plaid.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)

    return client


def create_link_token(client: plaid_api.PlaidApi):
    request = plaid_api.LinkTokenCreateRequest(
        products=[Products("transactions")],
        client_name="Plaid Web App",
        country_codes=[CountryCode("GB")],
        language="en",
        user=LinkTokenCreateRequestUser(client_user_id=str(time.time())),
    )
    response = client.link_token_create(request)

    return response
