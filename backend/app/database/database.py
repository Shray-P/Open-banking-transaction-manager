from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings

from app.database.models import Item as ItemDB

from app.models.item import Item


database_url = get_settings().dev_database_url

assert database_url

engine = create_engine(database_url, echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def add_item(session: Session, item: Item):
    session.add(
        ItemDB(
            id=item.id,
            institution_name=item.institution_name,
            access_token=item.access_token,
        )
    )
    session.commit()


def get_item(session: Session, id: str):
    item_db = session.get(Item, id)

    if item_db is None:
        return None

    return Item(
        id=item_db.id,
        access_token=item_db.access_token,
        institution_name=item_db.institution_name,
    )


def delete_item(session: Session, id: str):
    item = session.get(Item, id)
    if item is None:
        return

    session.delete(item)
    session.commit()
