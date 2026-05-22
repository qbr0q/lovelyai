"""update_at to match_action

Revision ID: dc96e44151ee
Revises: 2579ae7c81a7
Create Date: 2026-04-21 23:21:53.753387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = 'dc96e44151ee'
down_revision: Union[str, Sequence[str], None] = '2579ae7c81a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'match_action',
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('match_action', 'updated_at')
