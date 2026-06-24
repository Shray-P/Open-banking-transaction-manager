from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings

from app.database.models import Item

database_url = get_settings().dev_database_url

assert database_url

engine = create_engine(database_url, echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def add_item(session: Session, id: str, access_token: str):
    session.add(Item(id=id, access_token=access_token))
    session.commit()


def get_item(session: Session, id: str):
    return session.get(Item, id)


def delete_item(session: Session, id: str):
    item = session.get(Item, id)
    session.delete(item)
    session.commit()
