from uuid import uuid4
from pytest import fixture
from sqlalchemy.orm import Session
from app.db import Base
from app.models import Account
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
def created_user(db_session: Session):
    account = Account(
        id=uuid4(),
        name="Girish Gopaul",
        email="girish@gopaul.me",
        email_verified=True,
        # password="JustAPass01!"
        password_hash="$2b$12$U0NJfwAp/aBMx7EPktNAR.7chKu24k4NsSyLppN/lzjrzSNWYjy56"
    )
    db_session.add(account)
    db_session.commit()
    db_session.refresh(account)
    return account
