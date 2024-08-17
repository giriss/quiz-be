"""create posts table

Revision ID: 69b154cc9625
Revises: 08047e9333eb
Create Date: 2024-08-17 15:47:28.193835

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa

from app.models.utils import get_utc_time


# revision identifiers, used by Alembic.
revision: str = '69b154cc9625'
down_revision: Union[str, None] = '08047e9333eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column('id', sa.Uuid, primary_key=True, default=uuid.uuid4),
        sa.Column('caption', sa.String(200), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=get_utc_time, server_default=sa.func.now()),
        sa.Column("account_id", sa.Uuid, sa.ForeignKey("accounts.id"), nullable=False),
    )
    op.create_foreign_key(None, "posts", "accounts", ["account_id"], ["id"])


def downgrade() -> None:
    op.drop_table("posts")
