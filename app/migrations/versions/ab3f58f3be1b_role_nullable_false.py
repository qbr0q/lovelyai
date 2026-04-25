"""role nullable false

Revision ID: ab3f58f3be1b
Revises: 44ec4e208d44
Create Date: 2026-04-25 16:57:00.408213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = 'ab3f58f3be1b'
down_revision: Union[str, Sequence[str], None] = '44ec4e208d44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('user_profile', 'role',
               existing_type=sa.VARCHAR(),
               nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('user_profile', 'role',
               existing_type=sa.VARCHAR(),
               nullable=True)
