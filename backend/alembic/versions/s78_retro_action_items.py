"""Sprint 78: Retrospective Action Items Table

Revision ID: s78_retro_action_items
Revises: s74_planning_hierarchy
Create Date: 2026-01-18 18:00:00.000000

Implements Sprint 78 Day 1 - Retrospective Enhancement:
- retro_action_items: Action items from sprint retrospectives
- Supports assignment, status tracking, and cross-sprint due dates
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 's78_retro_action_items'
down_revision = 's74_planning_hierarchy'
branch_labels = None
depends_on = None


def upgrade():
    """Create retro_action_items table for Sprint 78 Day 1."""
    op.create_table(
        'retro_action_items',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('sprint_id', UUID(as_uuid=True), sa.ForeignKey('sprints.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column(
            'category',
            sa.String(50),
            server_default='general',
            nullable=False,
            comment='Category: delivery, priority, velocity, planning, scope, blockers, team, general'
        ),
        sa.Column(
            'priority',
            sa.String(20),
            server_default='medium',
            nullable=False,
            comment='Priority: low, medium, high'
        ),
        sa.Column(
            'status',
            sa.String(20),
            server_default='open',
            nullable=False,
            comment='Status: open, in_progress, completed, cancelled'
        ),
        sa.Column('assignee_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column(
            'due_sprint_id',
            UUID(as_uuid=True),
            sa.ForeignKey('sprints.id', ondelete='SET NULL'),
            nullable=True,
            comment='Target sprint for completion'
        ),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()'), nullable=False),
        sa.Column('completed_at', sa.DateTime, nullable=True),
        sa.Column('is_deleted', sa.Boolean, server_default='false', nullable=False),
    )

    # Create indexes for common queries
    op.create_index('idx_retro_action_items_sprint', 'retro_action_items', ['sprint_id'])
    op.create_index('idx_retro_action_items_status', 'retro_action_items', ['status'])
    op.create_index('idx_retro_action_items_assignee', 'retro_action_items', ['assignee_id'])
    op.create_index('idx_retro_action_items_due_sprint', 'retro_action_items', ['due_sprint_id'])
    op.create_index('idx_retro_action_items_category', 'retro_action_items', ['category'])


def downgrade():
    """Drop retro_action_items table."""
    op.drop_index('idx_retro_action_items_category', 'retro_action_items')
    op.drop_index('idx_retro_action_items_due_sprint', 'retro_action_items')
    op.drop_index('idx_retro_action_items_assignee', 'retro_action_items')
    op.drop_index('idx_retro_action_items_status', 'retro_action_items')
    op.drop_index('idx_retro_action_items_sprint', 'retro_action_items')
    op.drop_table('retro_action_items')
