"""add_project_stage_mappings

Revision ID: r3m4n5o6p7q8
Revises: q2l3m4n5o6p7
Create Date: 2025-12-24 10:00:00.000000

SDLC Stage: 04 - BUILD
Sprint: 49 - Stage Mapping Redesign (SDLC 5.1.2)
Epic: Onboarding Flow Enhancement
Framework: SDLC 5.1.2

Purpose:
Create project_stage_mappings table for persisting folder-to-stage mappings.
Per CTO approval: Only one table, structure validation computed on-read.

Changes in SDLC 5.1.2:
- Only /docs folders are stage-mapped (00-09)
- Code folders (backend, frontend, tests) are NOT stage-mapped
- Structure validation is computed on-read, not persisted

Tables:
1. project_stage_mappings - Folder-to-stage mappings for each project

Reference: SDLC-Project-Structure-Standard.md
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "r3m4n5o6p7q8"
down_revision: Union[str, None] = "q2l3m4n5o6p7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create project_stage_mappings table
    op.create_table(
        "project_stage_mappings",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "project_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "folder_path",
            sa.String(255),
            nullable=False,
            comment="Folder path relative to repo root, e.g., 'docs/00-foundation'",
        ),
        sa.Column(
            "stage_code",
            sa.String(10),
            nullable=False,
            comment="SDLC stage code: '00', '01', ..., '09', '10' (archive)",
        ),
        sa.Column(
            "stage_name",
            sa.String(50),
            nullable=True,
            comment="Human-readable stage name: FOUNDATION, PLANNING, etc.",
        ),
        sa.Column(
            "is_auto_detected",
            sa.Boolean,
            nullable=False,
            server_default=sa.text("true"),
            comment="True if auto-detected by system, False if manually set by user",
        ),
        sa.Column(
            "confidence",
            sa.Float,
            nullable=True,
            comment="Confidence score for auto-detection (0.0-1.0)",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
        # Composite unique constraint: one mapping per folder per project
        sa.UniqueConstraint(
            "project_id", "folder_path", name="uq_project_stage_mapping_folder"
        ),
    )

    # Add index for querying by stage
    op.create_index(
        "ix_project_stage_mappings_stage_code",
        "project_stage_mappings",
        ["stage_code"],
    )

    # Add comment to table
    op.execute(
        """
        COMMENT ON TABLE project_stage_mappings IS
        'SDLC 5.1.2: Maps /docs folders to SDLC stages (00-09). Code folders are NOT stage-mapped.';
        """
    )


def downgrade() -> None:
    op.drop_index("ix_project_stage_mappings_stage_code", table_name="project_stage_mappings")
    op.drop_table("project_stage_mappings")
