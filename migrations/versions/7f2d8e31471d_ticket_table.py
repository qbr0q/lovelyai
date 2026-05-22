"""ticket table

Revision ID: 7f2d8e31471d
Revises: ab3f58f3be1b
Create Date: 2026-05-05 21:28:17.984646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = '7f2d8e31471d'
down_revision: Union[str, Sequence[str], None] = 'ab3f58f3be1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('ticket',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user_profile.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ticket_status'), 'ticket', ['status'], unique=False)
    op.create_index(op.f('ix_ticket_user_id'), 'ticket', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_ticket_user_id'), table_name='ticket')
    op.drop_index(op.f('ix_ticket_status'), table_name='ticket')
    op.drop_table('ticket')
