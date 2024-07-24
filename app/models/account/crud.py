from typing import List
from uuid import UUID
from hashlib import sha256
from uuid import uuid4
from base64 import b64encode
from bcrypt import hashpw, gensalt, checkpw
from cloudinary.uploader import destroy as cloudinary_destroy
from .model import Account
from ..email import Email
from ..email import EmailCRUD
from ..crud_base import CRUDBase


class AccountCRUD(CRUDBase):
    def create(self, name: str, email: str, password: str = None) -> Account:
        password_hash = None if password is None else hashpw(prehash_pw(password), gensalt()).decode()
        account = Account(id=uuid4(), name=name, password_hash=password_hash)
        self.db.add(account)
        EmailCRUD(self.db, account).create(address=email, primary=True)
        return account

    def search(self, query: str) -> List[Account]:
        return self.db.query(Account).filter(Account.name.ilike(f"%{query}%")).limit(10).all()

    def find(self, uuid: str | UUID) -> Account:
        return self.db.query(Account).filter_by(id=str(uuid)).one()

    def authenticate(self, email: str, password: str) -> Account:
        user = self.db.query(Account).join(Email).filter_by(address=email).one()
        if checkpw(prehash_pw(password), user.password_hash.encode()):
            return user
        raise InvalidPassword()

    def set_picture(self, account_id: str, picture_id: str):
        account = self.find(account_id)
        if account.picture_id is not None:
            cloudinary_destroy(f"{account.id}_{account.picture_id}", resource_type="image")
        account.picture_id = picture_id


class InvalidPassword(Exception):
    pass


def prehash_pw(password: str) -> bytes:
    return b64encode(sha256(password.encode()).digest())
