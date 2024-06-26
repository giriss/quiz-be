import uuid
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from ..utils import get_utc_time
from ...db import Base

cols = [
    sa.Column('id', sa.Uuid, primary_key=True, default=uuid.uuid4),
    sa.Column('name', sa.String(200), nullable=False),
    sa.Column('password_hash', sa.String(60)),
    sa.Column('created_at', sa.DateTime, nullable=False, default=get_utc_time, server_default=sa.func.now())
]


class Account(Base):
    __tablename__ = "accounts"

    id = cols[0]
    name = cols[1]
    password_hash = cols[2]
    created_at = cols[3]

    emails = relationship("Email", back_populates="account")
