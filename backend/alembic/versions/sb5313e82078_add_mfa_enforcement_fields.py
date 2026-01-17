"""add_mfa_enforcement_fields

Revision ID: sb5313e82078
Revises: sb5212d71967
Create Date: 2026-01-14 (ADR-027 Phase 1)

Description:
Add MFA enforcement tracking fields to users table for mfa_required setting.

Fields Added:
- mfa_setup_deadline: Timestamp when user must complete MFA setup (7-day grace period)
- is_mfa_exempt: Flag to exempt specific users from MFA requirement (admin override)

ADR-027 Phase 1: mfa_required implementation
Zero Mock Policy: Real MFA enforcement with grace period and admin exemptions
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'sb5313e82078'
down_revision = 'sb5212d71967'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add MFA enforcement fields to users table."""
    # Add mfa_setup_deadline column (7-day grace period deadline)
    op.add_column(
        'users',
        sa.Column(
            'mfa_setup_deadline',
            sa.DateTime(timezone=True),
            nullable=True,
            comment='Deadline for completing MFA setup when mfa_required is enabled (7-day grace period)'
        )
    )

    # Add is_mfa_exempt column (admin can exempt users)
    op.add_column(
        'users',
        sa.Column(
            'is_mfa_exempt',
            sa.Boolean(),
            nullable=False,
            server_default='false',
            comment='User is exempt from MFA requirement (admin override)'
        )
    )

    # Create index on mfa_setup_deadline for efficient grace period checks
    op.create_index(
        'idx_users_mfa_setup_deadline',
        'users',
        ['mfa_setup_deadline'],
        postgresql_where=sa.text('mfa_setup_deadline IS NOT NULL')
    )


def downgrade() -> None:
    """Remove MFA enforcement fields from users table."""
    # Drop index
    op.drop_index('idx_users_mfa_setup_deadline', table_name='users')

    # Drop columns
    op.drop_column('users', 'is_mfa_exempt')
    op.drop_column('users', 'mfa_setup_deadline')
