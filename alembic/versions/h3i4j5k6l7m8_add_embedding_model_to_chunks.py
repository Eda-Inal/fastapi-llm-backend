"""Add embedding_model_name to document_chunks

Revision ID: h3i4j5k6l7m8
Revises: g2h3i4j5k6l7
Create Date: 2026-06-01
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "h3i4j5k6l7m8"
down_revision: Union[str, Sequence[str], None] = "g2h3i4j5k6l7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "document_chunks",
        sa.Column("embedding_model_name", sa.String(256), nullable=True),
    )
    # Backfill existing chunks from their parent document's embedding_model_name.
    # All chunks in one ingestion batch share the same model, so this is accurate.
    op.execute("""
        UPDATE document_chunks dc
        SET embedding_model_name = d.embedding_model_name
        FROM documents d
        WHERE dc.document_id = d.id
          AND d.embedding_model_name IS NOT NULL
    """)


def downgrade() -> None:
    op.drop_column("document_chunks", "embedding_model_name")
