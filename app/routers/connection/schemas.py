from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from ..account.schemas import AccountSearchItem
from ...models.connection.model import Status


class ConnectionCreate(BaseModel):
    responder_id: UUID


class ConnectionResponse(BaseModel):
    status: Status
    created_at: datetime
    requester: AccountSearchItem
    responder: AccountSearchItem
