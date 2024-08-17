import uuid
import re
import sqlalchemy as sa
from sqlalchemy.orm import relationship, validates
from ..utils import get_utc_time
from ...db import Base

cols = [
    sa.Column('id', sa.Uuid, primary_key=True, default=uuid.uuid4),
    sa.Column('username', sa.String(25), unique=True, nullable=False),
    sa.Column('name', sa.String(200), nullable=False),
    sa.Column('password_hash', sa.String(60)),
    sa.Column('picture_id', sa.Uuid, unique=True),
    sa.Column('created_at', sa.DateTime, nullable=False, default=get_utc_time, server_default=sa.func.now())
]


class Account(Base):
    __tablename__ = "accounts"

    id = cols[0]
    username = cols[1]
    name = cols[2]
    password_hash = cols[3]
    picture_id = cols[4]
    created_at = cols[5]

    emails = relationship("Email", back_populates="account")
    posts = relationship("Post", back_populates="account")
    sent_requests = relationship("Connection", back_populates="requester", foreign_keys="Connection.requester_id")
    received_requests = relationship("Connection", back_populates="responder", foreign_keys="Connection.responder_id")

    @validates('username')
    def validate_username(self, _key: str, username: str):
        if not re.match(r'^(?=.*[a-z])[a-z0-9_.-]{3,25}$', username, re.IGNORECASE):
            raise ValueError("Username must be 3-25 characters and contain at least one letter.")

        return username.lower()
