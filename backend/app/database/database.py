import uuid
from datetime import datetime, timezone, timedelta
from sqlmodel import Session, SQLModel, create_engine, delete, select

from app.config import get_settings

from app.database.models import (
    Account as AccountDB,
    Item as ItemDB,
    User as UserDB,
    LoginCode as LoginCodeDB,
)

from app.models.item import Item
from app.models.accounts import Account
from app.models.users import User
from app.models.login_code import LoginCode

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
    session.commit()


def get_account(session: Session, id: str) -> Account | None:
    account = session.get(AccountDB, id)
    if account is None:
        return None

    return Account(id=account.id, name=account.name)


def get_accounts_from_item(session: Session, item: Item) -> list[Account]:
    accounts = session.exec(
        select(AccountDB).where(AccountDB.item_id == item.id))

    return [Account(id=account.id, name=account.name) for account in accounts]


def add_user(
    session: Session,
    user: User,
    password_hash: str | None = None,
    google_id: str | None = None,
):
    session.add(
        UserDB(
            id=user.id, name=user.name, password_hash=password_hash, google_id=google_id
        )
    )
    session.commit()


def get_user(session: Session, id: uuid.UUID) -> User | None:
    user = session.get(UserDB, id)

    if user is None:
        return None

    return User(id=user.id, name=user.name)


def get_user_by_name(session: Session, name: str):
    user = session.exec(select(UserDB).where(UserDB.name == name)).one()
    if user is None:
        return None

    return User(id=user.id, name=user.name)


def get_user_password_hash(session: Session, id: uuid.UUID) -> str | None:
    user = session.get(UserDB, id)

    if user is None:
        return None

    return user.password_hash


def get_user_by_google_id(session: Session, id: str):
    user = session.exec(select(UserDB).where(UserDB.google_id == id)).first()
    if user is None:
        return None

    return User(id=user.id, name=user.name)


def add_login_code(session: Session, code: str, user: User, expire_minuets: float):
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minuets)

    session.add(LoginCodeDB(code=code, user_id=user.id, expire=expire))
    session.commit()


def get_login_code(session: Session, code: str):
    login_code = session.get(LoginCodeDB, code)

    if login_code is None:
        return None

    return LoginCode(
        code=login_code.code, user_id=login_code.user_id, expire=login_code.expire
    )


def delete_login_code(session: Session, code: str):
    login_code = session.get(LoginCodeDB, code)
    if login_code is None:
        return None

    session.delete(login_code)
    session.commit()
