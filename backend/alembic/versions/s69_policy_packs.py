"""Sprint 69 - Policy Packs Tables

Revision ID: s69_policy_packs
Revises: s60_pwd_reset
Create Date: 2026-01-07

Sprint 69: Policy Packs Feature
- policy_packs: Project-level policy configuration
- policy_rules: Individual OPA policies
- policy_evaluation_history: Audit trail for evaluations
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 's69_policy_packs'
down_revision = 's60_pwd_reset'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create policy_packs table
    op.create_table(
        'policy_packs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('version', sa.String(20), nullable=False, server_default='1.0.0'),
        sa.Column('tier', sa.String(20), nullable=False, server_default='standard', comment='lite, standard, professional, enterprise'),
        sa.Column('validators', postgresql.JSONB, nullable=False, server_default='[]', comment='[{"name": "lint", "enabled": true, "blocking": true, "config": {}}]'),
        sa.Column('coverage_threshold', sa.Integer, nullable=False, server_default='80', comment='Minimum test coverage percentage (0-100)'),
        sa.Column('coverage_blocking', sa.Boolean, nullable=False, server_default='false', comment='If true, coverage below threshold blocks merge'),
        sa.Column('forbidden_imports', postgresql.JSONB, nullable=False, server_default='[]', comment='["minio", "grafana_sdk"] - AGPL imports to block'),
        sa.Column('required_patterns', postgresql.JSONB, nullable=False, server_default='[]', comment='["from app.core.logging import"] - Required patterns'),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        comment='Policy Pack - Project-level policy configuration (Sprint 69)'
    )

    # Create indexes for policy_packs
    op.create_index('ix_policy_packs_id', 'policy_packs', ['id'])
    op.create_index('ix_policy_packs_project_id', 'policy_packs', ['project_id'], unique=True)
    op.create_index('ix_policy_packs_tier', 'policy_packs', ['tier'])

    # Create policy_rules table
    op.create_table(
        'policy_rules',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('policy_pack_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('policy_packs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('policy_id', sa.String(100), nullable=False, comment='Unique policy identifier (kebab-case)'),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('rego_policy', sa.Text, nullable=False, comment='OPA Rego policy source code'),
        sa.Column('severity', sa.String(20), nullable=False, server_default='medium', comment='critical, high, medium, low, info'),
        sa.Column('blocking', sa.Boolean, nullable=False, server_default='true', comment='If true, violation blocks merge'),
        sa.Column('enabled', sa.Boolean, nullable=False, server_default='true', comment='If false, policy is skipped'),
        sa.Column('message_template', sa.Text, nullable=False, comment='Message shown on failure'),
        sa.Column('tags', postgresql.JSONB, nullable=False, server_default='[]', comment='["security", "architecture"]'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        comment='Policy Rule - Individual OPA policy (Sprint 69)'
    )

    # Create indexes for policy_rules
    op.create_index('ix_policy_rules_id', 'policy_rules', ['id'])
    op.create_index('ix_policy_rules_policy_pack_id', 'policy_rules', ['policy_pack_id'])
    op.create_index('ix_policy_rules_policy_id', 'policy_rules', ['policy_id'])
    op.create_index('ix_policy_rules_severity', 'policy_rules', ['severity'])

    # Create policy_evaluation_history table
    op.create_table(
        'policy_evaluation_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('pr_number', sa.Integer, nullable=False),
        sa.Column('policy_pack_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('policy_packs.id', ondelete='SET NULL'), nullable=True),
        sa.Column('total_policies', sa.Integer, nullable=False),
        sa.Column('passed_count', sa.Integer, nullable=False),
        sa.Column('failed_count', sa.Integer, nullable=False),
        sa.Column('blocked', sa.Boolean, nullable=False, comment='True if any blocking policy failed'),
        sa.Column('results', postgresql.JSONB, nullable=False, comment='Full evaluation results'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('duration_ms', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        comment='Policy Evaluation History - Audit trail (Sprint 69)'
    )

    # Create indexes for policy_evaluation_history
    op.create_index('ix_policy_evaluation_history_id', 'policy_evaluation_history', ['id'])
    op.create_index('ix_policy_evaluation_history_project_id', 'policy_evaluation_history', ['project_id'])
    op.create_index('ix_policy_evaluation_history_pr', 'policy_evaluation_history', ['project_id', 'pr_number'])
    op.create_index('ix_policy_evaluation_history_created', 'policy_evaluation_history', ['created_at'])


def downgrade() -> None:
    # Drop policy_evaluation_history
    op.drop_index('ix_policy_evaluation_history_created', table_name='policy_evaluation_history')
    op.drop_index('ix_policy_evaluation_history_pr', table_name='policy_evaluation_history')
    op.drop_index('ix_policy_evaluation_history_project_id', table_name='policy_evaluation_history')
    op.drop_index('ix_policy_evaluation_history_id', table_name='policy_evaluation_history')
    op.drop_table('policy_evaluation_history')

    # Drop policy_rules
    op.drop_index('ix_policy_rules_severity', table_name='policy_rules')
    op.drop_index('ix_policy_rules_policy_id', table_name='policy_rules')
    op.drop_index('ix_policy_rules_policy_pack_id', table_name='policy_rules')
    op.drop_index('ix_policy_rules_id', table_name='policy_rules')
    op.drop_table('policy_rules')

    # Drop policy_packs
    op.drop_index('ix_policy_packs_tier', table_name='policy_packs')
    op.drop_index('ix_policy_packs_project_id', table_name='policy_packs')
    op.drop_index('ix_policy_packs_id', table_name='policy_packs')
    op.drop_table('policy_packs')
