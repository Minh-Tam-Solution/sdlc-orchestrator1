"""Sprint 203: Add max_reflect_iterations to agent_definitions

Revision ID: s203001
Revises: s202001
Create Date: 2026-05-05 00:00:00.000000

CONTEXT:
- Sprint 203 "Evaluator-Optimizer + Evals Expansion"
- Anthropic Best Practices: Evaluator-Optimizer pattern
- max_reflect_iterations bounds the reflect-and-score loop (1-3 iterations)
- Default=1 preserves exact Sprint 202 behavior (no extra round-trips)
- CHECK constraint enforces valid range: 1-3

ROLLBACK:
- safe: drops column and check constraint
- All existing agents default to 1 (server_default="1")
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "s203001"
down_revision = "s202001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add max_reflect_iterations column with CHECK constraint."""
    op.add_column(
        "agent_definitions",
        sa.Column(
            "max_reflect_iterations",
            sa.Integer(),
            nullable=False,
            server_default="1",
            comment="Max Evaluator-Optimizer iterations per tool batch (1-3). Sprint 203.",
        ),
    )
    op.create_check_constraint(
        "ck_agent_definitions_max_reflect_1_to_3",
        "agent_definitions",
        "max_reflect_iterations BETWEEN 1 AND 3",
    )


def downgrade() -> None:
    """Remove max_reflect_iterations column and check constraint."""
    op.drop_constraint(
        "ck_agent_definitions_max_reflect_1_to_3",
        "agent_definitions",
        type_="check",
    )
    op.drop_column("agent_definitions", "max_reflect_iterations")
