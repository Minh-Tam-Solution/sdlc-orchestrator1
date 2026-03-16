"""Add autonomy_level to agent_definitions (ADR-071 D-071-02)

Revision ID: s226_001
Revises: s221_001
Create Date: 2026-03-16

Sprint 226 — Conversation-First Relaunch
4 fixed autonomy presets mapped 1:1 to tiers:
  LITE → assist_only
  STANDARD → contribute_only
  PRO → member_guardrails
  ENTERPRISE → autonomous_gated
"""
from alembic import op
import sqlalchemy as sa

revision = "s226_001"
down_revision = "s221_001"
branch_labels = None
depends_on = None

VALID_PRESETS = (
    "assist_only",
    "contribute_only",
    "member_guardrails",
    "autonomous_gated",
)


def upgrade() -> None:
    # Add column with server_default so existing rows get 'assist_only'
    op.add_column(
        "agent_definitions",
        sa.Column(
            "autonomy_level",
            sa.String(length=30),
            server_default="assist_only",
            nullable=False,
            comment="Tier-mapped autonomy preset (ADR-071 D-071-02)",
        ),
    )

    # Add CHECK constraint to enforce valid preset values
    op.create_check_constraint(
        "agent_definitions_autonomy_level_check",
        "agent_definitions",
        sa.column("autonomy_level").in_(VALID_PRESETS),
    )


def downgrade() -> None:
    raise NotImplementedError(
        "Downgrade not supported — ADR-071 autonomy_level is a strategic decision. "
        "Removing this column would break tier-based governance enforcement."
    )
