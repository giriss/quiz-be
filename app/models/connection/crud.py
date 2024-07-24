from typing import List
from uuid import UUID
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
from ..crud_base import CRUDBase
from .model import Connection, Status


class ConnectionCRUD(CRUDBase):
    def create(self, responder_id: str | UUID) -> Connection:
        try:
            connection = self.db.query(Connection).filter_by(requester_id=self.user.id, responder_id=responder_id).one()
            connection.status = Status.pending
            return connection
        except NoResultFound:
            connection = Connection(requester_id=self.user.id, responder_id=responder_id)
            self.db.add(connection)
            return connection
        
    def list_all(self) -> List[Connection]:
        return self.db.query(Connection).filter(
            or_(Connection.requester_id == self.user.id, Connection.responder_id == self.user.id)
        ).all()
