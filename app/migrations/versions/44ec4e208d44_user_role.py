"""user role

Revision ID: 44ec4e208d44
Revises: dc96e44151ee
Create Date: 2026-04-25 16:54:07.585834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = '44ec4e208d44'
down_revision: Union[str, Sequence[str], None] = 'dc96e44151ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user_profile', sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user_profile', 'role')
