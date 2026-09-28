"""add triage metadata

Revision ID: d4f8a6b1c203
Revises: c2ad1b7a8b81
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "d4f8a6b1c203"
down_revision: str | Sequence[str] | None = "c2ad1b7a8b81"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "complaints",
        sa.Column("priority", sa.String(length=10), nullable=False, server_default="normal"),
    )
    op.add_column(
        "complaints",
        sa.Column("ai_summary", sa.String(length=140), nullable=False, server_default=""),
    )
    op.add_column(
        "complaints",
        sa.Column("triaged_by", sa.String(length=50), nullable=False, server_default="rules"),
    )
    op.add_column(
        "complaints",
        sa.Column("triage_latency_ms", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "complaints",
        sa.Column("triage_confidence", sa.Float(), nullable=False, server_default="0"),
    )

    for column in (
        "priority",
        "ai_summary",
        "triaged_by",
        "triage_latency_ms",
        "triage_confidence",
    ):
        op.alter_column("complaints", column, server_default=None)


def downgrade() -> None:
    op.drop_column("complaints", "triage_confidence")
    op.drop_column("complaints", "triage_latency_ms")
    op.drop_column("complaints", "triaged_by")
    op.drop_column("complaints", "ai_summary")
    op.drop_column("complaints", "priority")
