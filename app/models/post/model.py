import uuid
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from ..utils import get_utc_time
from ...db import Base


class Post(Base):
    __tablename__ = "posts"

    id = sa.Column('id', sa.Uuid, primary_key=True, default=uuid.uuid4)
    caption = sa.Column('caption', sa.String(200), nullable=True)
    created_at = sa.Column('created_at', sa.DateTime, nullable=False, default=get_utc_time, server_default=sa.func.now())
    account_id = sa.Column("account_id", sa.Uuid, sa.ForeignKey("accounts.id"), nullable=False)

    account = relationship("Account", back_populates="posts")
