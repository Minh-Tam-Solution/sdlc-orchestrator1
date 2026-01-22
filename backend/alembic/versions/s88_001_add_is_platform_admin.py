"""Add is_platform_admin field to User model

Revision ID: s88_001_add_is_platform_admin
Revises: s82_001_evidence_manifests
Create Date: 2026-01-21 23:00:00.000000

Sprint 88 Day 4-5: Platform Admin Privacy Fix - Backend Migration

Purpose:
    Add is_platform_admin field to separate platform administrators from customer users.
    Platform admins manage system operations but CANNOT access customer data.

Changes:
    1. Add is_platform_admin boolean column to users table
    2. Set default value to False
    3. Add index for fast filtering
    4. Migrate existing is_superuser=True users to is_platform_admin=True

Security Impact:
    - Platform admins (taidt@mtsolution.com.vn) get is_platform_admin=True
    - Regular admins keep is_superuser=True for backward compatibility
    - Frontend/backend will check is_platform_admin for privacy enforcement

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 's88_001_add_is_platform_admin'
down_revision: Union[str, None] = 's82_001_evidence_manifests'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Add is_platform_admin field to users table.

    Steps:
        1. Add is_platform_admin column (default False)
        2. Create index on is_platform_admin
        3. Migrate existing is_superuser=True users to is_platform_admin=True
    """
    # Step 1: Add is_platform_admin column
    op.add_column(
        'users',
        sa.Column(
            'is_platform_admin',
            sa.Boolean(),
            nullable=False,
            server_default='false',
            comment='Platform admin - manages system operations, CANNOT access customer data (Sprint 88)'
        )
    )

    # Step 2: Create index for fast filtering
    op.create_index(
        'ix_users_is_platform_admin',
        'users',
        ['is_platform_admin'],
        unique=False
    )

    # Step 3: Migrate existing is_superuser=True users to is_platform_admin=True
    # This ensures existing platform admins (like taidt@mtsolution.com.vn) get the new flag
    op.execute("""
        UPDATE users
        SET is_platform_admin = true
        WHERE is_superuser = true
    """)


def downgrade() -> None:
    """
    Remove is_platform_admin field from users table.

    Steps:
        1. Drop index
        2. Drop column
    """
    # Step 1: Drop index
    op.drop_index('ix_users_is_platform_admin', table_name='users')

    # Step 2: Drop column
    op.drop_column('users', 'is_platform_admin')
