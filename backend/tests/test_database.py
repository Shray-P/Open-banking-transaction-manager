import pytest

from sqlmodel import Session, SQLModel, create_engine, delete

from app.config import get_settings
from app.database.database import add_item, delete_item, get_item
from app.database.models import Item


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
        session.exec(delete(Item))
        session.commit()
        yield session


def test_insert_item(session):
    add_item(session, "1", "access_token")

    item = get_item(session, "1")

    assert item is not None
    assert item.id
    assert item.access_token


def test_insert_item_duplicate_id_fail(session):
    add_item(session, "1", "access_token1")

    with pytest.raises(Exception):
        add_item(session, "1", "access_token2")

    session.rollback()


def test_delete_item(session):
    add_item(session, "1", "access_token")

    item = get_item(session, "1")
    assert item is not None

    delete_item(session, "1")

    item = get_item(session, "1")
    assert item is None
