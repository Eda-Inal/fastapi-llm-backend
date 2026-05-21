"""add user_id to chat_logs

Revision ID: 52f4ef9962b6
Revises: a1b2c3d4e5f6
Create Date: 2026-05-21 09:56:18.771672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '52f4ef9962b6'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index(op.f('ix_chat_pairwise_evaluations_chat_log_id'), table_name='chat_pairwise_evaluations')
    op.drop_table('chat_pairwise_evaluations')
    op.add_column('chat_logs', sa.Column('user_id', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_chat_logs_user_id'), 'chat_logs', ['user_id'], unique=False)
    # NOTE: document_chunks.text_search (tsvector) and its indexes are intentionally
    # kept — they are not in the ORM model but are used by hybrid search via raw SQL.


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_chat_logs_user_id'), table_name='chat_logs')
    op.drop_column('chat_logs', 'user_id')
    op.create_table('chat_pairwise_evaluations',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('chat_log_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rubric_version', sa.VARCHAR(length=50), server_default=sa.text("'v1'::character varying"), autoincrement=False, nullable=False),
    sa.Column('candidate_model_a', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('candidate_model_b', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('answer_a', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('answer_b', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('judge_model_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('winner', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('notes', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('score_a', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('score_b', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['chat_log_id'], ['chat_logs.id'], name=op.f('chat_pairwise_evaluations_chat_log_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('chat_pairwise_evaluations_pkey')),
    sa.UniqueConstraint('chat_log_id', 'rubric_version', 'candidate_model_a', 'candidate_model_b', name=op.f('uq_chat_pairwise_log_rubric_pair'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    op.create_index(op.f('ix_chat_pairwise_evaluations_chat_log_id'), 'chat_pairwise_evaluations', ['chat_log_id'], unique=False)
    # ### end Alembic commands ###
