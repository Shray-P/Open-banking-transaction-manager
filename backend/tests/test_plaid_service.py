from datetime import datetime, date

from app.services.plaid_service import (
    create_plaid_link_token,
    create_sandbox_public_token,
    get_plaid_accounts_from_item,
    get_plaid_item,
    get_plaid_client,
    get_plaid_transactions,
)


def test_create_link_token():
    token = create_plaid_link_token(get_plaid_client())

    assert token


def test_get_item():
    client = get_plaid_client()
    pub_token = create_sandbox_public_token(client)

    assert pub_token is not None
    assert isinstance(pub_token, str)
    assert len(pub_token) > 0

    item = get_plaid_item(client, pub_token)

    assert item.id
    assert item.institution_name
    assert item.access_token


def test_get_transactions():
    client = get_plaid_client()
    pub_token = create_sandbox_public_token(client)
    acc_token = get_plaid_item(client, pub_token).access_token

    transactions = get_plaid_transactions(client, acc_token)

    for t in transactions:
        assert t.id
        assert t.account_id
        assert t.name
        assert t.iso_currency_code


def test_get_accounts():
    client = get_plaid_client()
    pub_token = create_sandbox_public_token(client)

    item = get_plaid_item(client, pub_token)

    accounts = get_plaid_accounts_from_item(client, item)

    assert accounts

    for account in accounts:
        assert account.id
        assert account.name
