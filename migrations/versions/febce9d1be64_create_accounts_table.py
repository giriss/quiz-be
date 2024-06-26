"""create accounts table

Revision ID: febce9d1be64
Revises: 
Create Date: 2024-06-20 15:21:47.695454

"""
from typing import Sequence, Union
from alembic import op
from app.models.account.model import cols


# revision identifiers, used by Alembic.
revision: str = 'febce9d1be64'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'accounts',
        *cols
    )


def downgrade() -> None:
    op.drop_table('accounts')
