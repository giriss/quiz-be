"""create connections table

Revision ID: 08047e9333eb
Revises: 43b81b4d2a44
Create Date: 2024-07-23 15:04:11.216235

"""
from typing import Sequence, Union

from alembic import op
from app.models.connection.model import cols


# revision identifiers, used by Alembic.
revision: str = '08047e9333eb'
down_revision: Union[str, None] = '43b81b4d2a44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "connections",
        *cols
    )
    op.create_foreign_key(None, "connections", "accounts", ["requester_id"], ["id"])
    op.create_foreign_key(None, "connections", "accounts", ["responder_id"], ["id"])


def downgrade() -> None:
    op.drop_table("connections")
    