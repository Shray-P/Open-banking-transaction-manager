from datetime import datetime
from app.services.plaid_service import create_link_token, get_plaid_client


def test_create_link_token():
    token = create_link_token(get_plaid_client())

    assert token is not None

    assert token.link_token is not None
    assert token.expiration.timestamp() > datetime.now().timestamp()
    assert token.request_id is not None
