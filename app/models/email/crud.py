from sqlalchemy.orm import Session
from uuid import UUID
from .model import Email
from ..crud_base import CRUDBase


class EmailCRUD(CRUDBase):
    def create(self, address: str, account_id: UUID, verified=False, primary=False):
        email = Email(address=address, verified=verified, primary=primary, account_id=account_id)
        self.db.add(email)
        return email

    def make_primary(self, uuid: str, account_id: UUID | str):
        email_query = self.db.query(Email).filter_by(account_id=str(account_id))
        email_query.update({"primary": False})
        email = email_query.filter_by(id=uuid).one()
        email.primary = True
        return email

    def verify(self, email: str) -> None:
        email = self.db.query(Email).filter_by(address=email).one()
        email.verified = True
