import sqlalchemy as sa
import datetime as dt
from ...db import Base


class Account(Base):
    __tablename__ = "accounts"

    id = sa.Column(sa.UUID, primary_key=True)
    name = sa.Column('name', sa.String(200), nullable=False)
    email = sa.Column('email', sa.String(200), nullable=False)
    email_verified = sa.Column('email_verified', sa.Boolean, nullable=False, default=False)
    password_hash = sa.Column('password_hash', sa.String(60))
    created_at = sa.Column('created_at', sa.DateTime, nullable=False, default=dt.datetime.now(dt.UTC))
