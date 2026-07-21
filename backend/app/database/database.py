from os import name
from sqlmodel import Session, SQLModel, create_engine, select

from app.config import get_settings

from app.database.models import Account as AccountDB, Item as ItemDB

from app.models.item import Item
from app.models.accounts import Account

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
    item_db = session.get(ItemDB, id)

    if item_db is None:
        return None

    return Item(
        id=item_db.id,
        access_token=item_db.access_token,
        institution_name=item_db.institution_name,
    )


def delete_item(session: Session, id: str):
    item = session.get(ItemDB, id)
    if item is None:
        return

    session.delete(item)
    session.commit()


def add_account(session: Session, account: Account, item: Item):
    session.add(AccountDB(id=account.id, name=account.name, item_id=item.id))


def get_account(session: Session, id: str) -> Account | None:
    account = session.get(AccountDB, id)
    if account is None:
        return None

    return Account(id=account.id, name=account.name)


def get_accounts_from_item(session: Session, item: Item) -> list[Account]:
    accounts = session.exec(
        select(AccountDB).where(AccountDB.item_id == item.id))

    return [Account(id=account.id, name=account.name) for account in accounts]
