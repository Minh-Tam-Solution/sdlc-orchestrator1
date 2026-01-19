"""Sprint 78: Resource Allocations Table

Revision ID: s78_resource_allocations
Revises: s78_sprint_dependencies
Create Date: 2026-01-18 20:00:00.000000

Implements Sprint 78 Day 3 - Resource Allocation Optimization:
- resource_allocations: Track team member allocation to sprints
- Supports capacity planning and conflict detection
- Enables resource utilization visualization
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 's78_resource_allocations'
down_revision = 's78_sprint_dependencies'
branch_labels = None
depends_on = None


def upgrade():
    """Create resource_allocations table for Sprint 78 Day 3."""
    op.create_table(
        'resource_allocations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('sprint_id', UUID(as_uuid=True), sa.ForeignKey('sprints.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column(
            'allocation_percentage',
            sa.Integer,
            server_default='100',
            nullable=False,
            comment='Allocation percentage (0-100)'
        ),
        sa.Column(
            'role',
            sa.String(50),
            server_default='developer',
            nullable=False,
            comment='Role: developer, qa, designer, pm, tech_lead, devops, analyst, other'
        ),
        sa.Column('start_date', sa.Date, nullable=False),
        sa.Column('end_date', sa.Date, nullable=False),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('created_by_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean, server_default='false', nullable=False),
    )

    # Create indexes for common queries
    op.create_index('idx_resource_alloc_sprint', 'resource_allocations', ['sprint_id'])
    op.create_index('idx_resource_alloc_user', 'resource_allocations', ['user_id'])
    op.create_index('idx_resource_alloc_dates', 'resource_allocations', ['start_date', 'end_date'])
    op.create_index('idx_resource_alloc_role', 'resource_allocations', ['role'])

    # Unique constraint: one allocation per user-sprint pair
    op.create_index(
        'idx_resource_alloc_user_sprint',
        'resource_allocations',
        ['user_id', 'sprint_id'],
        unique=True
    )


def downgrade():
    """Drop resource_allocations table."""
    op.drop_index('idx_resource_alloc_user_sprint', 'resource_allocations')
    op.drop_index('idx_resource_alloc_role', 'resource_allocations')
    op.drop_index('idx_resource_alloc_dates', 'resource_allocations')
    op.drop_index('idx_resource_alloc_user', 'resource_allocations')
    op.drop_index('idx_resource_alloc_sprint', 'resource_allocations')
    op.drop_table('resource_allocations')
