import uuid
import pytest

from sqlmodel import Session, SQLModel, create_engine, delete

from app.config import get_settings
from app.database.database import (
    add_account,
    add_item,
    add_user,
    delete_item,
    get_account,
    get_accounts_from_item,
    get_item,
    get_user,
)
from app.database.models import Item as ItemDB

from app.models.users import User
from app.models.accounts import Account
from app.models.item import Item


@pytest.fixture(scope="session")
def engine():
    database_url = get_settings().test_database_url
    assert database_url

    engine = create_engine(database_url, echo=True)
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture()
def session(engine):
    with Session(engine) as session:
        session.exec(delete(ItemDB))
        session.commit()
        yield session


def test_insert_item(session):
    add_item(
        session,
        Item(id="1", institution_name="institution",
             access_token="access_token"),
    )

    item = get_item(session, "1")

    assert item is not None
    assert item.id
    assert item.access_token


def test_insert_item_duplicate_id_fail(session):
    add_item(
        session,
        Item(id="1", institution_name="institution",
             access_token="access_token1"),
    )

    with pytest.raises(Exception):
        add_item(
            session,
            Item(
                id="1",
                institution_name="institution",
                access_token="access_token2",
            ),
        )

    session.rollback()


def test_delete_item(session):
    add_item(
        session,
        Item(id="1", institution_name="institution",
             access_token="access_token"),
    )

    item = get_item(session, "1")
    assert item is not None

    delete_item(session, "1")

    item = get_item(session, "1")
    assert item is None


def test_insert_account(session):
    item = Item(id="1", access_token="access_token",
                institution_name="institution")

    add_item(session, item)

    add_account(session, Account(id="1", name="Account 1"), item)

    account = get_account(session, "1")

    assert account
    assert account.id
    assert account.name


def test_get_accounts_from_item(session):
    item = Item(id="1", access_token="access_token",
                institution_name="institution")

    add_item(session, item)

    add_account(session, Account(id="1", name="Account 1"), item)
    add_account(session, Account(id="2", name="Account 2"), item)

    accounts = get_accounts_from_item(session, item)

    assert accounts
    assert len(accounts) == 2

    for account in accounts:
        assert account


def test_insert_user(session):
    id = uuid.uuid4()

    add_user(session, User(id=id, name="1"))

    user = get_user(session, id)

    assert user
    assert user.id
    assert user.name
