"""Sprint 78: Sprint Dependencies Table

Revision ID: s78_sprint_dependencies
Revises: s78_retro_action_items
Create Date: 2026-01-18 19:00:00.000000

Implements Sprint 78 Day 2 - Cross-Project Sprint Dependencies:
- sprint_dependencies: Track dependencies between sprints
- Supports circular dependency detection
- Enables dependency graph visualization
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 's78_sprint_dependencies'
down_revision = 's78_retro_action_items'
branch_labels = None
depends_on = None


def upgrade():
    """Create sprint_dependencies table for Sprint 78 Day 2."""
    op.create_table(
        'sprint_dependencies',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('source_sprint_id', UUID(as_uuid=True), sa.ForeignKey('sprints.id', ondelete='CASCADE'), nullable=False),
        sa.Column('target_sprint_id', UUID(as_uuid=True), sa.ForeignKey('sprints.id', ondelete='CASCADE'), nullable=False),
        sa.Column(
            'dependency_type',
            sa.String(20),
            server_default='related',
            nullable=False,
            comment='Type: blocks, requires, related'
        ),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column(
            'status',
            sa.String(20),
            server_default='pending',
            nullable=False,
            comment='Status: pending, active, resolved, cancelled'
        ),
        sa.Column('created_by_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('resolved_by_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()'), nullable=False),
        sa.Column('resolved_at', sa.DateTime, nullable=True),
        sa.Column('is_deleted', sa.Boolean, server_default='false', nullable=False),
    )

    # Create indexes for common queries
    op.create_index('idx_sprint_dep_source', 'sprint_dependencies', ['source_sprint_id'])
    op.create_index('idx_sprint_dep_target', 'sprint_dependencies', ['target_sprint_id'])
    op.create_index('idx_sprint_dep_status', 'sprint_dependencies', ['status'])
    op.create_index('idx_sprint_dep_type', 'sprint_dependencies', ['dependency_type'])

    # Unique constraint to prevent duplicate dependencies
    op.create_index(
        'idx_sprint_dep_source_target',
        'sprint_dependencies',
        ['source_sprint_id', 'target_sprint_id'],
        unique=True
    )


def downgrade():
    """Drop sprint_dependencies table."""
    op.drop_index('idx_sprint_dep_source_target', 'sprint_dependencies')
    op.drop_index('idx_sprint_dep_type', 'sprint_dependencies')
    op.drop_index('idx_sprint_dep_status', 'sprint_dependencies')
    op.drop_index('idx_sprint_dep_target', 'sprint_dependencies')
    op.drop_index('idx_sprint_dep_source', 'sprint_dependencies')
    op.drop_table('sprint_dependencies')
