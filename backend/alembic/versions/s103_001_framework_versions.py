"""Sprint 103: Framework Version History Table

Revision ID: s103_001_framework_versions
Revises: s102_001_policy_tier
Create Date: 2026-01-23 17:00:00.000000

Implements SDLC 5.2.0 Framework Version Tracking:
- Track Framework version history per project
- Enable compliance audits with version proof
- Detect version drift from latest Framework
- Support Framework migration tracking

Why track version history?
- Compliance audits require version proof at specific points in time
- Framework updates need migration tracking
- Policy changes need retroactive application records
- Training materials reference specific versions

Reference: docs/04-build/02-Sprint-Plans/SPRINT-103-DESIGN.md
Reference: SDLC Framework 5.2.0, Section 09-GOVERN
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 's103_001_framework_versions'
down_revision = 's102_001_policy_tier'
branch_labels = None
depends_on = None


def upgrade():
    # =========================================================================
    # Table: framework_versions
    # Track SDLC Framework version history per project.
    #
    # Purpose:
    #   - Record Framework version on project creation/update
    #   - Maintain audit trail for compliance
    #   - Enable version drift detection
    #   - Support Framework migration tracking
    # =========================================================================
    op.create_table(
        'framework_versions',
        sa.Column(
            'id',
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text('gen_random_uuid()'),
        ),
        sa.Column(
            'project_id',
            UUID(as_uuid=True),
            sa.ForeignKey('projects.id', ondelete='CASCADE'),
            nullable=False,
            index=True,
        ),

        # Version Information
        sa.Column(
            'version',
            sa.String(20),
            nullable=False,
            comment='Semantic version string (e.g., 5.2.0)',
        ),
        sa.Column(
            'major',
            sa.Integer(),
            nullable=False,
            comment='Major version number',
        ),
        sa.Column(
            'minor',
            sa.Integer(),
            nullable=False,
            comment='Minor version number',
        ),
        sa.Column(
            'patch',
            sa.Integer(),
            nullable=False,
            comment='Patch version number',
        ),

        # Optional Metadata
        sa.Column(
            'release_notes',
            sa.Text(),
            nullable=True,
            comment='Notes about this version application',
        ),

        # Audit Information
        sa.Column(
            'applied_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('NOW()'),
            nullable=False,
            index=True,
            comment='When this version was applied',
        ),
        sa.Column(
            'applied_by',
            UUID(as_uuid=True),
            sa.ForeignKey('users.id', ondelete='SET NULL'),
            nullable=True,
            comment='User who applied this version',
        ),
    )

    # Composite index for common queries
    op.create_index(
        'idx_framework_versions_project_applied',
        'framework_versions',
        ['project_id', 'applied_at'],
    )

    # Add table comments
    op.execute("""
        COMMENT ON TABLE framework_versions IS
        'SDLC Framework version history per project for compliance audits';

        COMMENT ON COLUMN framework_versions.version IS
        'Semantic version string matching SDLC Framework releases';

        COMMENT ON COLUMN framework_versions.applied_at IS
        'Timestamp when this Framework version was applied to the project';
    """)

    # =========================================================================
    # Backfill: Create initial version records for existing projects
    # Uses the framework_version column added in Sprint 101
    # =========================================================================
    op.execute("""
        INSERT INTO framework_versions (id, project_id, version, major, minor, patch, applied_at, release_notes)
        SELECT
            gen_random_uuid(),
            id,
            COALESCE(framework_version, '5.2.0'),
            SPLIT_PART(COALESCE(framework_version, '5.2.0'), '.', 1)::INTEGER,
            SPLIT_PART(COALESCE(framework_version, '5.2.0'), '.', 2)::INTEGER,
            SPLIT_PART(COALESCE(framework_version, '5.2.0'), '.', 3)::INTEGER,
            created_at,
            'Backfilled from Sprint 103 migration'
        FROM projects
        WHERE deleted_at IS NULL
    """)


def downgrade():
    op.drop_index('idx_framework_versions_project_applied', table_name='framework_versions')
    op.drop_table('framework_versions')
