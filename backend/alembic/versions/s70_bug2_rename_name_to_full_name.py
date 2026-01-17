"""S70-BUG2: Rename users.name to users.full_name

Revision ID: s70_bug2_name_fix
Revises: s70_teams_foundation
Create Date: 2026-01-20 10:00:00.000000

Sprint: 70 - Teams Foundation
Story: BUG #2 - User name Field Fix
Reference: E2E Test Report - BUG #2

Issue:
Design Doc specifies `full_name` but database has `name`

Solution:
Rename column from `name` to `full_name` for consistency with design docs

SDLC 5.1.2 Compliance:
- Zero Breaking Changes: Migration preserves all existing data
- API Compatibility: Both fields supported during transition
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 's70_bug2_name_fix'
down_revision = 's70_teams_foundation'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Rename users.name to users.full_name.

    Steps:
    1. Rename column from name to full_name
    2. No data migration needed (column rename preserves data)
    """
    # Rename column
    op.alter_column(
        'users',
        'name',
        new_column_name='full_name',
        existing_type=sa.String(255),
        existing_nullable=True
    )


def downgrade() -> None:
    """
    Rollback: Rename users.full_name back to users.name.
    """
    # Rename column back
    op.alter_column(
        'users',
        'full_name',
        new_column_name='name',
        existing_type=sa.String(255),
        existing_nullable=True
    )
