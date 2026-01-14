"""add_login_lockout_fields

Revision ID: sb5212d71967
Revises: s69_policy_packs
Create Date: 2026-01-14 (ADR-027 Phase 1)

Description:
Add login lockout tracking fields to users table for max_login_attempts setting.

Fields Added:
- failed_login_count: Counter for consecutive failed login attempts
- locked_until: Timestamp when account lockout expires (30 min after reaching max attempts)

ADR-027 Phase 1: max_login_attempts implementation
Zero Mock Policy: Real account lockout based on database setting
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'sb5212d71967'
down_revision = 's69_policy_packs'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add login lockout fields to users table."""
    # Add failed_login_count column (tracks consecutive failures)
    op.add_column(
        'users',
        sa.Column(
            'failed_login_count',
            sa.Integer(),
            nullable=False,
            server_default='0',
            comment='Number of consecutive failed login attempts'
        )
    )

    # Add locked_until column (timestamp when lockout expires)
    op.add_column(
        'users',
        sa.Column(
            'locked_until',
            sa.DateTime(timezone=True),
            nullable=True,
            comment='Account locked until this timestamp (NULL = not locked)'
        )
    )

    # Create index on locked_until for efficient lockout checks
    op.create_index(
        'idx_users_locked_until',
        'users',
        ['locked_until'],
        postgresql_where=sa.text('locked_until IS NOT NULL')
    )


def downgrade() -> None:
    """Remove login lockout fields from users table."""
    # Drop index
    op.drop_index('idx_users_locked_until', table_name='users')

    # Drop columns
    op.drop_column('users', 'locked_until')
    op.drop_column('users', 'failed_login_count')
