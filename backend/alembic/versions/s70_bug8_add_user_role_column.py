"""S70-BUG8: Add role column to users table

Revision ID: s70_bug8_user_role
Revises: s70_bug2_name_fix
Create Date: 2026-01-20 11:00:00.000000

Sprint: 70 - Teams Foundation
Story: BUG #8 - User Role Field Missing
Reference: E2E Test Report - BUG #8

Issue:
Design Doc specifies user `role` enum (ceo, cto, pm, dev, qa, devops, designer)
but database has no role column.

Solution:
Add `role` column with enum constraint for RBAC

SDLC 5.1.2 Compliance:
- Default role: 'dev' for existing users
- Constraint ensures only valid roles
- Backfill migration for existing data
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 's70_bug8_user_role'
down_revision = 's70_bug2_name_fix'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add role column to users table.

    Steps:
    1. Add role column (nullable initially for migration)
    2. Backfill existing users with default role 'dev'
    3. Make column NOT NULL
    4. Add CHECK constraint for valid roles
    """
    # Step 1: Add role column (nullable)
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.String(50),
            nullable=True,
            comment='User role: ceo, cto, cpo, pm, dev, qa, devops, designer, ba'
        )
    )

    # Step 2: Backfill existing users with default role 'dev'
    op.execute("""
        UPDATE users
        SET role = 'dev'
        WHERE role IS NULL
    """)

    # Step 3: Make column NOT NULL
    op.alter_column(
        'users',
        'role',
        existing_type=sa.String(50),
        nullable=False,
        server_default='dev'
    )

    # Step 4: Add CHECK constraint
    op.create_check_constraint(
        'users_role_check',
        'users',
        "role IN ('ceo', 'cto', 'cpo', 'cio', 'cfo', 'em', 'tl', 'pm', 'dev', 'qa', 'devops', 'security', 'ba', 'designer')"
    )

    # Step 5: Add index for role-based queries
    op.create_index('idx_users_role', 'users', ['role'])


def downgrade() -> None:
    """
    Rollback: Remove role column from users table.
    """
    # Remove index
    op.drop_index('idx_users_role', table_name='users')

    # Remove CHECK constraint
    op.drop_constraint('users_role_check', 'users', type_='check')

    # Remove column
    op.drop_column('users', 'role')
