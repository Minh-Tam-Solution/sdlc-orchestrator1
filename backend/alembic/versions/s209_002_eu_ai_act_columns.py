"""s209_002_eu_ai_act_columns — Add EU AI Act risk classification columns to projects

Sprint 209 (post-migration fix): Add missing eu_ai_act_* columns that exist
in the Project model but were never added via migration.

Revision ID: s209_002
Revises: s209_001
Create Date: 2026-02-27
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "s209_002"
down_revision = "s209_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add eu_ai_act_risk_level
    op.add_column(
        "projects",
        sa.Column(
            "eu_ai_act_risk_level",
            sa.String(20),
            nullable=True,
            comment="EU AI Act risk classification: prohibited, high_risk, limited_risk, minimal_risk",
        ),
    )
    op.create_index("ix_projects_eu_ai_act_risk_level", "projects", ["eu_ai_act_risk_level"])

    # Add eu_ai_act_classified_at
    op.add_column(
        "projects",
        sa.Column(
            "eu_ai_act_classified_at",
            sa.DateTime(timezone=True),
            nullable=True,
            comment="Timestamp of EU AI Act classification",
        ),
    )

    # Add eu_ai_act_classified_by
    op.add_column(
        "projects",
        sa.Column(
            "eu_ai_act_classified_by",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
            comment="User who performed EU AI Act classification",
        ),
    )


def downgrade() -> None:
    op.drop_column("projects", "eu_ai_act_classified_by")
    op.drop_column("projects", "eu_ai_act_classified_at")
    op.drop_index("ix_projects_eu_ai_act_risk_level", table_name="projects")
    op.drop_column("projects", "eu_ai_act_risk_level")
