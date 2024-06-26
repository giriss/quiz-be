from sqlalchemy import Column, Uuid, String, Boolean, DateTime, ForeignKey, false, func
from sqlalchemy.orm import relationship
from uuid import uuid4
from ..utils import get_utc_time
from ...db import Base

cols = [
    Column("id", Uuid, primary_key=True, default=uuid4),
    Column("address", String(200), nullable=False, unique=True),
    Column("verified", Boolean, nullable=False, default=False, server_default=false()),
    Column("primary", Boolean, nullable=False, default=False, server_default=false()),
    Column("created_at", DateTime, nullable=False, default=get_utc_time, server_default=func.now()),
    Column("account_id", Uuid, ForeignKey("accounts.id"), nullable=False)
]


class Email(Base):
    __tablename__ = "emails"

    id = cols[0]
    address = cols[1]
    verified = cols[2] 
    primary = cols[3] 
    created_at = cols[4]
    account_id = cols[5]

    account = relationship("Account", back_populates="emails")
