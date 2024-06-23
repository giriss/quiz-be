from uuid import uuid4
from hashlib import sha256
from base64 import b64encode
from sqlalchemy.orm import Session
from bcrypt import hashpw, gensalt, checkpw
from .model import Account


class AccountCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, name: str, email: str, password: str = None) -> Account:
        password_hash = None if password is None else hashpw(prehash_pw(password), gensalt()).decode()
        account = Account(id=uuid4(), name=name, email=email, password_hash=password_hash)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        self.db.reset()
        return account

    def find(self, uuid: str) -> Account:
        result = self.db.query(Account).filter_by(id=uuid).one()
        self.db.reset()
        return result

    def authenticate(self, email: str, password: str) -> Account:
        user = self.db.query(Account).filter_by(email=email).one()
        if checkpw(prehash_pw(password), user.password_hash.encode()):
            return user
        raise InvalidPassword()

    def verify_account(self, email: str) -> Account:
        user = self.db.query(Account).filter_by(email=email).one()
        user.email_verified = True
        self.db.commit()
        self.db.refresh(user)
        self.db.reset()
        return user


class InvalidPassword(Exception):
    pass


def prehash_pw(password: str) -> bytes:
    return b64encode(sha256(password.encode()).digest())
