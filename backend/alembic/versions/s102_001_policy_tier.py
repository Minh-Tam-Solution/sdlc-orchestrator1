"""Sprint 102: Add policy_pack_tier to projects (4-Tier Enforcement)

Revision ID: s102_001_policy_tier
Revises: s101_002_crp_tables
Create Date: 2026-01-23 16:00:00.000000

Implements SDLC 5.2.0 4-Tier Policy Enforcement:
- Add policy_pack_tier column to projects table
- Determines which policy tier applies to the project
- Controls enforcement strictness and required checks

4-Tier Classification:
  - LITE: Advisory only, never blocks (startups, prototypes)
  - STANDARD: Soft enforcement, warnings only (small teams)
  - PROFESSIONAL: Hard enforcement, block merge (most teams)
  - ENTERPRISE: Zero tolerance, strictest (regulated industries)

Reference: docs/04-build/02-Sprint-Plans/SPRINT-102-DESIGN.md
Reference: SDLC Framework 5.2.0, 4-Tier Classification
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 's102_001_policy_tier'
down_revision = 's101_002_crp_tables'
branch_labels = None
depends_on = None


def upgrade():
    # =========================================================================
    # Add policy_pack_tier column to projects table
    # Default: PROFESSIONAL (most common tier for established teams)
    # Existing projects get backfilled with PROFESSIONAL
    #
    # Why track policy tier?
    #   - Graduated governance (startups vs enterprises have different needs)
    #   - MRP 5-point validation required checks differ by tier
    #   - Enforcement mode controls merge blocking behavior
    #   - Compliance reporting needs tier context
    # =========================================================================
    op.add_column(
        'projects',
        sa.Column(
            'policy_pack_tier',
            sa.String(20),
            nullable=False,
            server_default='PROFESSIONAL',
            comment='Policy tier: LITE, STANDARD, PROFESSIONAL, ENTERPRISE',
        ),
    )

    # Create index for policy tier filtering
    op.create_index(
        'idx_projects_policy_tier',
        'projects',
        ['policy_pack_tier'],
    )

    # Add check constraint for valid tier values
    op.create_check_constraint(
        'projects_policy_tier_check',
        'projects',
        "policy_pack_tier IN ('LITE', 'STANDARD', 'PROFESSIONAL', 'ENTERPRISE')",
    )

    # Add column comment
    op.execute("""
        COMMENT ON COLUMN projects.policy_pack_tier IS
        '4-Tier Policy Classification: LITE (advisory), STANDARD (soft), PROFESSIONAL (hard), ENTERPRISE (strictest). Controls MRP enforcement mode and required checks.';
    """)


def downgrade():
    op.drop_constraint('projects_policy_tier_check', 'projects', type_='check')
    op.drop_index('idx_projects_policy_tier', table_name='projects')
    op.drop_column('projects', 'policy_pack_tier')
