import uuid
from app.database.database import add_user
from app.models.users import User
from app.services.auth_service import (
    create_access_token,
    create_password_hash,
    decode_access_token,
    get_user_by_access_token,
)
from .test_database import session, engine


def test_access_token(session):
    id = uuid.uuid4()
    original_user = User(id=id, name="1")

    password = "1"
    password_hash = create_password_hash(password)

    add_user(session, original_user, password_hash)

    token = create_access_token(original_user)

    retreived_user = get_user_by_access_token(session, token.access_token)

    assert retreived_user
    assert original_user.id == retreived_user.id
    assert original_user.name == retreived_user.name
