from datetime import datetime, date
import time

import plaid
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser


from app.config import get_settings
from app.models.transactions import Transaction


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


def create_sandbox_public_token(
    client: plaid_api.PlaidApi,
) -> str:

    # Get first institution from plaid
    inst_request = plaid_api.InstitutionsGetRequest(
        country_codes=[CountryCode("GB")], count=1, offset=0
    )

    inst_response = client.institutions_get(inst_request)

    request = plaid_api.SandboxPublicTokenCreateRequest(
        institution_id=inst_response.institutions[0].institution_id,
        initial_products=[Products("transactions")],
    )

    response = client.sandbox_public_token_create(request)

    return response.public_token


def exchange_public_for_access_token(
    client: plaid_api.PlaidApi, public_token: str
) -> str:
    request = plaid_api.ItemPublicTokenExchangeRequest(
        public_token=public_token)

    exchange_response = client.item_public_token_exchange(request)

    return exchange_response.access_token


def get_transactions(
    client: plaid_api.PlaidApi, access_token: str
) -> list[Transaction]:
    cursor = ""

    added = []
    modified = []
    removed = []
    has_more = True

    while has_more:
        request = plaid_api.TransactionsSyncRequest(
            access_token=access_token,
            cursor=cursor,
        )
        response = client.transactions_sync(request)
        cursor = response.next_cursor

        if cursor == "":
            time.sleep(2)
            continue

        added.extend(response.added)
        modified.extend(response.modified)
        removed.extend(response.removed)
        has_more = response.has_more

    transactions = [Transaction.from_plaid(
        transaction) for transaction in added]

    return transactions
