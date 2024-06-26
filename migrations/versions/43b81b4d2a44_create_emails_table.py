"""create emails table

Revision ID: 43b81b4d2a44
Revises: febce9d1be64
Create Date: 2024-06-25 15:38:33.367514

"""
from typing import Sequence, Union

from alembic import op
from app.models.email.model import cols


# revision identifiers, used by Alembic.
revision: str = '43b81b4d2a44'
down_revision: Union[str, None] = 'febce9d1be64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "emails",
        *cols
    )


def downgrade() -> None:
    op.drop_table("emails")
