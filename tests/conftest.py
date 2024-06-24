from uuid import uuid4
from pytest import fixture
from sqlalchemy.orm import Session
from app.db import engine, session_maker, Base
from app.models import Account


@fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@fixture(scope='session')
def db_session():
    yield session_maker()


@fixture
def created_user(db_session: Session):
    account = Account(
        id=uuid4(),
        name="Girish Gopaul",
        email="girish@gopaul.me",
        email_verified=True,
        # password="JustAPass01!"
        password_hash=b"$2b$12$U0NJfwAp/aBMx7EPktNAR.7chKu24k4NsSyLppN/lzjrzSNWYjy56"
    )
    db_session.add(account)
    db_session.commit()
    db_session.refresh(account)
    yield account
