"""Add conversation_id to documents table

Revision ID: i4j5k6l7m8n9
Revises: h3i4j5k6l7m8
Create Date: 2026-06-02
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "i4j5k6l7m8n9"
down_revision: Union[str, Sequence[str], None] = "h3i4j5k6l7m8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "documents",
        sa.Column("conversation_id", sa.String(128), nullable=True),
    )
    op.create_index(
        "ix_documents_conversation_id",
        "documents",
        ["conversation_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_documents_conversation_id", table_name="documents")
    op.drop_column("documents", "conversation_id")
