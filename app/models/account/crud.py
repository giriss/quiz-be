from typing import List
from uuid import UUID
from hashlib import sha256
from uuid import uuid4
from base64 import b64encode
from bcrypt import hashpw, gensalt, checkpw
from cloudinary.uploader import destroy as cloudinary_destroy
from sqlalchemy import or_
from .model import Account
from ..email import Email
from ..email import EmailCRUD
from ..crud_base import CRUDBase


class AccountCRUD(CRUDBase):
    def create(self, name: str, username: str, email: str, password: str = None) -> Account:
        password_hash = None if password is None else hashpw(prehash_pw(password), gensalt()).decode()
        account = Account(id=uuid4(), username=username, name=name, password_hash=password_hash)
        self.db.add(account)
        EmailCRUD(self.db, account).create(address=email, primary=True)
        return account

    def search(self, query: str) -> List[Account]:
        q = f"%{query}%"
        return self.db.query(Account).filter(
            or_(Account.name.ilike(q), Account.username.ilike(q))
        ).limit(10).all()

    def is_username_available(self, username: str):
        return self.db.query(Account).filter_by(username=username).count() == 0

    def find(self, uuid_or_username: str | UUID) -> Account:
        try:
            uuid = UUID(hex=uuid_or_username) if isinstance(uuid_or_username, str) else uuid_or_username
            return self.db.query(Account).filter_by(id=str(uuid)).one()
        except ValueError:
            return self.db.query(Account).filter_by(username=uuid_or_username).one()

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
