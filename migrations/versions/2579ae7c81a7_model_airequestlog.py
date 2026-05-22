"""model AIRequestLog

Revision ID: 2579ae7c81a7
Revises: 5c863c7d5472
Create Date: 2026-04-16 00:09:34.800082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = '2579ae7c81a7'
down_revision: Union[str, Sequence[str], None] = '5c863c7d5472'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('ai_request_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('action_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('prompt_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('completion_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('tokens_used', sa.Integer(), nullable=False),
        sa.Column('response_time', sa.Integer(), nullable=False),
        sa.Column('model_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user_profile.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_request_log_response_time'), 'ai_request_log', ['response_time'], unique=False)
    op.create_index(op.f('ix_ai_request_log_tokens_used'), 'ai_request_log', ['tokens_used'], unique=False)
    op.create_index(op.f('ix_ai_request_log_user_id'), 'ai_request_log', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_ai_request_log_user_id'), table_name='ai_request_log')
    op.drop_index(op.f('ix_ai_request_log_tokens_used'), table_name='ai_request_log')
    op.drop_index(op.f('ix_ai_request_log_response_time'), table_name='ai_request_log')
    op.drop_table('ai_request_log')
