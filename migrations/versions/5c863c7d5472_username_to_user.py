"""username to user

Revision ID: 5c863c7d5472
Revises: 569c36572c5d
Create Date: 2026-04-03 22:58:42.995549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = '5c863c7d5472'
down_revision: Union[str, Sequence[str], None] = '569c36572c5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user_profile', sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user_profile', 'username')
