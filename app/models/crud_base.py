from sqlalchemy.orm import Session
from ..db import Base
from .account.model import Account


class CRUDBase:
    def __init__(self, db: Session, user: Account = None) -> None:
        self.db = db
        self.user = user

    def commit(self, *refresh_models: Base):
        self.db.commit()
        for model in refresh_models:
            self.db.refresh(model)
