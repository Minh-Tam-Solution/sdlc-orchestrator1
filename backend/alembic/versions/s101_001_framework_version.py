"""Sprint 101: Add framework_version to projects (SDLC 5.2.0 Compliance)

Revision ID: s101_001_framework_version
Revises: s100_001_decomposition_hints
Create Date: 2026-01-23 14:00:00.000000

Implements SDLC 5.2.0 Compliance - Framework Version Tracking:
- Add framework_version column to projects table
- Enables compliance audits with version proof
- Tracks which Framework version projects were built against
- Supports framework migration tracking

Reference: docs/04-build/02-Sprint-Plans/SPRINT-101-DESIGN.md
Reference: SDLC Framework 5.2.0, Section 09-GOVERN
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 's101_001_framework_version'
down_revision = 's100_001_decomposition_hints'
branch_labels = None
depends_on = None


def upgrade():
    # =========================================================================
    # Add framework_version column to projects table
    # Default: 5.2.0 (current Framework version)
    # Existing projects get backfilled with 5.2.0
    #
    # Why track framework version?
    #   - Compliance audits require version proof
    #   - Framework updates need migration tracking
    #   - Policy changes need retroactive application
    #   - Training materials reference specific versions
    # =========================================================================
    op.add_column(
        'projects',
        sa.Column(
            'framework_version',
            sa.String(20),
            nullable=False,
            server_default='5.2.0',
            comment='SDLC Framework version (e.g., 5.2.0) for compliance audits',
        ),
    )

    # Create index for framework version queries
    op.create_index(
        'idx_projects_framework_version',
        'projects',
        ['framework_version'],
    )

    # Add column comment
    op.execute("""
        COMMENT ON COLUMN projects.framework_version IS
        'SDLC Framework version this project was created/updated against. Used for compliance audits and migration tracking.';
    """)


def downgrade():
    op.drop_index('idx_projects_framework_version', table_name='projects')
    op.drop_column('projects', 'framework_version')
