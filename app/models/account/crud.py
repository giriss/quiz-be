from hashlib import sha256
from uuid import uuid4
from base64 import b64encode
from bcrypt import hashpw, gensalt, checkpw
from .model import Account
from ..email import Email
from ..email import EmailCRUD
from ..crud_base import CRUDBase


class AccountCRUD(CRUDBase):
    def create(self, name: str, email: str, password: str = None) -> Account:
        password_hash = None if password is None else hashpw(prehash_pw(password), gensalt()).decode()
        account = Account(id=uuid4(), name=name, password_hash=password_hash)
        self.db.add(account)
        EmailCRUD(self.db).create(address=email, primary=True, account_id=account.id)
        return account

    def find(self, uuid: str) -> Account:
        return self.db.query(Account).filter_by(id=uuid).one()

    def authenticate(self, email: str, password: str) -> Account:
        user = self.db.query(Account).join(Email).filter_by(address=email).one()
        if checkpw(prehash_pw(password), user.password_hash.encode()):
            return user
        raise InvalidPassword()


class InvalidPassword(Exception):
    pass


def prehash_pw(password: str) -> bytes:
    return b64encode(sha256(password.encode()).digest())
