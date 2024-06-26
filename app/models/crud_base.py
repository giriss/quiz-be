from sqlalchemy.orm import Session
from ..db import Base


class CRUDBase:
    def __init__(self, db: Session) -> None:
        self.db = db

    def commit(self, *refresh_models: Base):
        self.db.commit()
        for model in refresh_models:
            self.db.refresh(model)
