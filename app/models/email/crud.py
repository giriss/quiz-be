from .model import Email
from ..crud_base import CRUDBase


class EmailCRUD(CRUDBase):
    def create(self, address: str, verified=False, primary=False):
        email = Email(address=address, verified=verified, primary=primary, account_id=self.user.id)
        self.db.add(email)
        return email

    def delete(self, address: str):
        self.db.query(Email).filter_by(address=address, account_id=str(self.user.id)).delete()

    def make_primary(self, address: str):
        email_query = self.db.query(Email).filter_by(account_id=str(self.user.id))
        email_query.update({"primary": False})
        email = email_query.filter_by(address=address).one()
        email.primary = True
        return email

    def verify(self, email: str) -> None:
        email = self.db.query(Email).filter_by(address=email).one()
        email.verified = True
