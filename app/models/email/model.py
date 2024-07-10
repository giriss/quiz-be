from sqlalchemy import Column, Uuid, String, Boolean, DateTime, ForeignKey, false, func
from sqlalchemy.orm import relationship
from ..utils import get_utc_time
from ...db import Base

cols = [
    Column("address", String(200), primary_key=True),
    Column("verified", Boolean, nullable=False, default=False, server_default=false()),
    Column("primary", Boolean, nullable=False, default=False, server_default=false()),
    Column("created_at", DateTime, nullable=False, default=get_utc_time, server_default=func.now()),
    Column("account_id", Uuid, ForeignKey("accounts.id"), nullable=False)
]


class Email(Base):
    __tablename__ = "emails"

    address = cols[0]
    verified = cols[1]
    primary = cols[2]
    created_at = cols[3]
    account_id = cols[4]

    account = relationship("Account", back_populates="emails")
