import enum
from sqlalchemy import Column, Uuid, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..utils import get_utc_time
from ...db import Base


class Status(enum.Enum):
    pending = 0
    rejected = -1
    accepted = 1


cols = [
    Column("requester_id", Uuid, ForeignKey("accounts.id"), primary_key=True, nullable=False),
    Column("responder_id", Uuid, ForeignKey("accounts.id"), primary_key=True, nullable=False),
    Column("status", Enum(Status), default=Status.pending),
    Column("created_at", DateTime, nullable=False, default=get_utc_time, server_default=func.now()),
]


class Connection(Base):
    __tablename__ = "connections"

    requester_id = cols[0]
    responder_id = cols[1]
    status = cols[2]
    created_at = cols[3]

    requester = relationship("Account", back_populates="sent_requests", foreign_keys=requester_id)
    responder = relationship("Account", back_populates="received_requests", foreign_keys=responder_id)
