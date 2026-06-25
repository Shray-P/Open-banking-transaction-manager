from datetime import datetime, date

from app.services.plaid_service import (
    create_link_token,
    create_sandbox_public_token,
    get_item,
    get_plaid_client,
    get_transactions,
)


def test_create_link_token():
    token = create_link_token(get_plaid_client())

    assert token is not None

    assert token.link_token is not None
    assert token.expiration.timestamp() > datetime.now().timestamp()
    assert token.request_id is not None


def test_get_item():
    client = get_plaid_client()
    pub_token = create_sandbox_public_token(client)

    assert pub_token is not None
    assert isinstance(pub_token, str)
    assert len(pub_token) > 0

    item = get_item(client, pub_token)

    assert item.id
    assert item.institution_name
    assert item.access_token


def test_get_transactions():
    client = get_plaid_client()
    pub_token = create_sandbox_public_token(client)
    acc_token = get_item(client, pub_token).access_token

    transactions = get_transactions(client, acc_token)

    for t in transactions:
        assert t.id
        assert t.account_id
        assert t.name
        assert t.iso_currency_code
