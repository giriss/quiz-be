from uuid import uuid4
from pytest import fixture
from sqlalchemy.orm import Session
from app.db import Base
from app.models import Account, Email
from app.utils import encode_auth_token
from .db import engine, session_maker


@fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@fixture(scope='session')
def db_session():
    session = session_maker()
    yield session
    session.close()


@fixture
def verified_user(db_session: Session):
    account = Account(
        id=uuid4(),
        name="Girish Gopaul",
        username="gir.ish",
        # password="JustAPass01!"
        password_hash="$2b$12$U0NJfwAp/aBMx7EPktNAR.7chKu24k4NsSyLppN/lzjrzSNWYjy56"
    )
    db_session.add(account)
    db_session.add(Email(
        address="girish@gopaul.me",
        verified=True,
        primary=True,
        account_id=account.id
    ))
    db_session.commit()
    db_session.refresh(account)
    return account


@fixture
def unverified_user(db_session: Session):
    account = Account(
        id=uuid4(),
        name="Girish Gopaul",
        username="gir.ish",
        # password="JustAPass01!"
        password_hash="$2b$12$U0NJfwAp/aBMx7EPktNAR.7chKu24k4NsSyLppN/lzjrzSNWYjy56"
    )
    db_session.add(account)
    db_session.add(Email(
        address="girish@gopaul.me",
        verified=False,
        primary=True,
        account_id=account.id
    ))
    db_session.commit()
    db_session.refresh(account)
    return account


@fixture
def verified_user_with_token(verified_user: Account):
    return verified_user, encode_auth_token(verified_user.id)
