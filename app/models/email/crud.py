from sqlalchemy.orm import Session
from uuid import UUID
from .model import Email
from ..crud_base import CRUDBase


class EmailCRUD(CRUDBase):
    def create(self, address: str, account_id: UUID, verified: bool = False, primary: bool = False):
        email = Email(address=address, verified=verified, primary=primary, account_id=account_id)
        self.db.add(email)
        return email

    def make_primary(self, email: Email):
        self.db.query(Email).filter_by(
            address=email.address, account_id=email.account_id
        ).update({"primary": False})
        email.primary = True
        return email

    def verify_account(self, email: str) -> None:
        email = self.db.query(Email).filter_by(address=email).one()
        email.verified = True
