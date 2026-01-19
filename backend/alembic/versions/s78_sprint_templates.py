"""Sprint 78: Sprint Templates Table

Revision ID: s78_sprint_templates
Revises: s78_resource_allocations
Create Date: 2026-01-18 23:00:00.000000

Implements Sprint 78 Day 4 - Sprint Template Library:
- sprint_templates: Reusable sprint configurations
- Default backlog structure support
- Team-specific and public templates
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON


# revision identifiers, used by Alembic.
revision = 's78_sprint_templates'
down_revision = 's78_resource_allocations'
branch_labels = None
depends_on = None


def upgrade():
    """Create sprint_templates table for Sprint 78 Day 4."""
    op.create_table(
        'sprint_templates',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column(
            'template_type',
            sa.String(20),
            server_default='standard',
            nullable=False,
            comment='Type: standard, feature, bugfix, release, custom'
        ),
        sa.Column('duration_days', sa.Integer, server_default='10', nullable=False),
        sa.Column('default_capacity_points', sa.Integer, server_default='40', nullable=False),
        sa.Column('backlog_structure', JSON, nullable=True),
        sa.Column('gates_enabled', sa.Boolean, server_default='true', nullable=False),
        sa.Column('goal_template', sa.Text, nullable=True),
        sa.Column('team_id', UUID(as_uuid=True), sa.ForeignKey('teams.id', ondelete='SET NULL'), nullable=True),
        sa.Column('is_public', sa.Boolean, server_default='false', nullable=False),
        sa.Column('is_default', sa.Boolean, server_default='false', nullable=False),
        sa.Column('usage_count', sa.Integer, server_default='0', nullable=False),
        sa.Column('created_by_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('NOW()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean, server_default='false', nullable=False),
    )

    # Create indexes for common queries
    op.create_index('idx_sprint_template_team', 'sprint_templates', ['team_id'])
    op.create_index('idx_sprint_template_type', 'sprint_templates', ['template_type'])
    op.create_index('idx_sprint_template_public', 'sprint_templates', ['is_public'])
    op.create_index('idx_sprint_template_default', 'sprint_templates', ['is_default'])

    # Insert default templates
    op.execute("""
        INSERT INTO sprint_templates (id, name, description, template_type, duration_days, default_capacity_points, gates_enabled, is_public, backlog_structure, goal_template)
        VALUES
        (
            gen_random_uuid(),
            '2-Week Standard Sprint',
            'Standard 2-week sprint template with basic structure. Suitable for most teams and projects.',
            'standard',
            10,
            40,
            true,
            true,
            '[
                {"title": "Sprint Planning", "type": "task", "priority": "P0", "story_points": 1, "description": "Sprint planning meeting and backlog grooming"},
                {"title": "Daily Standup Setup", "type": "task", "priority": "P0", "story_points": 0, "description": "Configure daily standup schedule"},
                {"title": "Sprint Review", "type": "task", "priority": "P0", "story_points": 1, "description": "Demo and review completed work"},
                {"title": "Retrospective", "type": "task", "priority": "P0", "story_points": 1, "description": "Sprint retrospective and action items"}
            ]'::jsonb,
            'Complete [GOAL] by delivering [DELIVERABLES] with quality standards met'
        ),
        (
            gen_random_uuid(),
            'Feature Sprint',
            'Sprint focused on delivering a major feature. Includes design, implementation, and testing phases.',
            'feature',
            14,
            50,
            true,
            true,
            '[
                {"title": "Feature Design Review", "type": "spike", "priority": "P0", "story_points": 3, "description": "Review and finalize feature design"},
                {"title": "Implementation Tasks", "type": "story", "priority": "P0", "story_points": 13, "description": "Core feature implementation"},
                {"title": "Unit Tests", "type": "task", "priority": "P0", "story_points": 5, "description": "Write comprehensive unit tests"},
                {"title": "Integration Tests", "type": "task", "priority": "P1", "story_points": 3, "description": "Integration testing with existing features"},
                {"title": "Documentation", "type": "task", "priority": "P1", "story_points": 2, "description": "Update documentation and guides"}
            ]'::jsonb,
            'Deliver [FEATURE_NAME] feature with full test coverage and documentation'
        ),
        (
            gen_random_uuid(),
            'Bug Fix Sprint',
            'Sprint dedicated to fixing critical bugs and technical debt. Short duration for quick turnaround.',
            'bugfix',
            5,
            25,
            true,
            true,
            '[
                {"title": "Bug Triage", "type": "task", "priority": "P0", "story_points": 2, "description": "Prioritize and assign bugs"},
                {"title": "Critical Bug Fixes", "type": "bug", "priority": "P0", "story_points": 8, "description": "Fix P0/P1 bugs"},
                {"title": "Regression Testing", "type": "task", "priority": "P0", "story_points": 3, "description": "Verify fixes and check for regressions"},
                {"title": "Hotfix Deployment", "type": "task", "priority": "P0", "story_points": 2, "description": "Deploy fixes to production"}
            ]'::jsonb,
            'Resolve [COUNT] critical bugs and reduce bug backlog by [PERCENTAGE]%'
        ),
        (
            gen_random_uuid(),
            'Release Sprint',
            'Sprint focused on preparing and executing a release. Includes final testing, documentation, and deployment.',
            'release',
            7,
            30,
            true,
            true,
            '[
                {"title": "Release Candidate Build", "type": "task", "priority": "P0", "story_points": 2, "description": "Create and verify release candidate"},
                {"title": "QA Sign-off", "type": "task", "priority": "P0", "story_points": 5, "description": "Final QA testing and sign-off"},
                {"title": "Release Notes", "type": "task", "priority": "P0", "story_points": 2, "description": "Prepare release notes and changelog"},
                {"title": "Deployment Plan", "type": "task", "priority": "P0", "story_points": 3, "description": "Create and review deployment plan"},
                {"title": "Production Deployment", "type": "task", "priority": "P0", "story_points": 3, "description": "Execute production deployment"},
                {"title": "Post-Release Monitoring", "type": "task", "priority": "P0", "story_points": 2, "description": "Monitor production after release"}
            ]'::jsonb,
            'Release v[VERSION] with zero critical bugs and <1h downtime'
        );
    """)


def downgrade():
    """Drop sprint_templates table."""
    op.drop_index('idx_sprint_template_default', 'sprint_templates')
    op.drop_index('idx_sprint_template_public', 'sprint_templates')
    op.drop_index('idx_sprint_template_type', 'sprint_templates')
    op.drop_index('idx_sprint_template_team', 'sprint_templates')
    op.drop_table('sprint_templates')
