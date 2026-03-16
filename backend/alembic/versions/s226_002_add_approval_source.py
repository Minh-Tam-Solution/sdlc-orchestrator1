"""Add source column to gate_approvals (ADR-071 D-071-05)

Revision ID: s226_002
Revises: s226_001
Create Date: 2026-03-16

Sprint 226 — Tracks which interface initiated gate approval:
  web, chat, magic_link, cli, api, agent.
Required for human_override_rate() product metric.
"""
from alembic import op
import sqlalchemy as sa

revision = "s226_002"
down_revision = "s226_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "gate_approvals",
        sa.Column(
            "source",
            sa.String(length=20),
            nullable=True,
            comment="Source interface: web, chat, magic_link, cli, api, agent (ADR-071)",
        ),
    )


def downgrade() -> None:
    raise NotImplementedError(
        "Downgrade not supported — source column is required for product metrics."
    )
