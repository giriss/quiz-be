"""create accounts table

Revision ID: febce9d1be64
Revises: 
Create Date: 2024-06-20 15:21:47.695454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'febce9d1be64'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'accounts',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('email', sa.String(200), nullable=False, unique=True),
        sa.Column('email_verified', sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column('password_hash', sa.String(60)),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table('accounts')
