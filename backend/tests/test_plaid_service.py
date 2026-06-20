from datetime import datetime, date

from app.services.plaid_service import (
    create_link_token,
    create_sandbox_public_token,
    exchange_public_for_access_token,
    get_plaid_client,
    get_transactions,
)


def test_create_link_token():
    token = create_link_token(get_plaid_client())

    assert token is not None

    assert token.link_token is not None
    assert token.expiration.timestamp() > datetime.now().timestamp()
    assert token.request_id is not None


def test_exchange_public_for_access_token():
    client = get_plaid_client()
    pub_token = create_sandbox_public_token(client)

    assert pub_token is not None
    assert isinstance(pub_token, str)
    assert len(pub_token) > 0

    acc_token = exchange_public_for_access_token(client, pub_token)

    assert acc_token is not None
    assert isinstance(acc_token, str)
    assert len(acc_token) > 0


def test_get_transactions():
    client = get_plaid_client()
    pub_token = create_sandbox_public_token(client)
    acc_token = exchange_public_for_access_token(client, pub_token)

    transactions = get_transactions(client, acc_token)

    for t in transactions:
        assert t.transaction_id
        assert t.account_id
        assert t.name
        assert t.iso_currency_code
