"""Sprint 94: PR Learnings Table (EP-11 Feedback Loop)

Revision ID: s94_001_pr_learnings
Revises: s89_001_rls_policies
Create Date: 2026-01-22 21:00:00.000000

Implements EP-11 Feedback Loop Closure:
- pr_learnings: Store learnings extracted from PR review comments
- Enable continuous improvement of AI code generation

Reference: ADR-034-Planning-Subagent-Orchestration (Section 7)
Expert Workflow Analysis: "Learning from Code Reviews"
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers, used by Alembic.
revision = 's94_001_pr_learnings'
down_revision = 's89_001_rls_policies'
branch_labels = None
depends_on = None


def upgrade():
    # =========================================================================
    # Table: pr_learnings
    # Stores learnings extracted from PR review comments for continuous
    # improvement of AI code generation.
    #
    # Workflow:
    #   1. PR merged with review comments
    #   2. System extracts learnings automatically
    #   3. Monthly: Aggregate learnings → Update decomposition hints
    #   4. Quarterly: Update CLAUDE.md with new patterns
    # =========================================================================
    op.create_table(
        'pr_learnings',
        sa.Column(
            'id',
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text('gen_random_uuid()'),
        ),
        sa.Column(
            'project_id',
            UUID(as_uuid=True),
            sa.ForeignKey('projects.id', ondelete='CASCADE'),
            nullable=False,
            index=True,
        ),

        # PR Reference
        sa.Column('pr_number', sa.Integer, nullable=False),
        sa.Column('pr_title', sa.String(255), nullable=True),
        sa.Column('pr_url', sa.String(500), nullable=True),
        sa.Column('pr_merged_at', sa.DateTime(timezone=True), nullable=True),

        # Learning Classification
        # Categories: pattern_violation, missing_requirement, edge_case, performance,
        #             security_issue, test_coverage, documentation, refactoring
        sa.Column(
            'feedback_type',
            sa.String(50),
            nullable=False,
            index=True,
        ),
        sa.Column(
            'severity',
            sa.String(20),
            nullable=False,
            server_default='medium',
        ),  # low, medium, high, critical

        # Learning Content
        sa.Column('original_code', sa.Text, nullable=True),
        sa.Column('original_spec_section', sa.Text, nullable=True),
        sa.Column('review_comment', sa.Text, nullable=False),
        sa.Column('corrected_approach', sa.Text, nullable=True),
        sa.Column('pattern_extracted', sa.Text, nullable=True),

        # Context
        sa.Column('file_path', sa.String(500), nullable=True),
        sa.Column('line_start', sa.Integer, nullable=True),
        sa.Column('line_end', sa.Integer, nullable=True),
        sa.Column('related_adr', sa.String(100), nullable=True),  # e.g., "ADR-002"

        # Reviewer Information
        sa.Column(
            'reviewer_id',
            UUID(as_uuid=True),
            sa.ForeignKey('users.id', ondelete='SET NULL'),
            nullable=True,
        ),
        sa.Column('reviewer_github_login', sa.String(100), nullable=True),

        # Processing Status
        # Status: extracted, reviewed, applied, archived
        sa.Column(
            'status',
            sa.String(20),
            nullable=False,
            server_default='extracted',
            index=True,
        ),
        sa.Column('applied_to_claude_md', sa.Boolean, server_default='false'),
        sa.Column('applied_to_decomposition', sa.Boolean, server_default='false'),
        sa.Column('applied_at', sa.DateTime(timezone=True), nullable=True),

        # AI Processing
        sa.Column('ai_extracted', sa.Boolean, server_default='true'),  # vs manual
        sa.Column('ai_confidence', sa.Float, nullable=True),  # 0.0 - 1.0
        sa.Column('ai_model', sa.String(50), nullable=True),  # e.g., "qwen3:32b"
        sa.Column('extraction_metadata', JSONB, nullable=True),

        # Aggregation Helper
        sa.Column('tags', JSONB, nullable=True, server_default='[]'),
        sa.Column('related_learnings', JSONB, nullable=True, server_default='[]'),

        # Audit
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('NOW()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('NOW()'),
            nullable=False,
        ),

        # Check constraints
        sa.CheckConstraint(
            "feedback_type IN ('pattern_violation', 'missing_requirement', "
            "'edge_case', 'performance', 'security_issue', 'test_coverage', "
            "'documentation', 'refactoring', 'other')",
            name='pr_learnings_feedback_type_check',
        ),
        sa.CheckConstraint(
            "severity IN ('low', 'medium', 'high', 'critical')",
            name='pr_learnings_severity_check',
        ),
        sa.CheckConstraint(
            "status IN ('extracted', 'reviewed', 'applied', 'archived')",
            name='pr_learnings_status_check',
        ),
    )

    # Indexes for common queries
    op.create_index(
        'idx_pr_learnings_project_feedback',
        'pr_learnings',
        ['project_id', 'feedback_type'],
    )
    op.create_index(
        'idx_pr_learnings_project_created',
        'pr_learnings',
        ['project_id', 'created_at'],
    )
    op.create_index(
        'idx_pr_learnings_status_applied',
        'pr_learnings',
        ['status', 'applied_to_claude_md', 'applied_to_decomposition'],
    )
    op.create_index(
        'idx_pr_learnings_pr_number',
        'pr_learnings',
        ['project_id', 'pr_number'],
    )

    # =========================================================================
    # Table: learning_aggregations
    # Stores monthly/quarterly aggregations of learnings for pattern updates
    # =========================================================================
    op.create_table(
        'learning_aggregations',
        sa.Column(
            'id',
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text('gen_random_uuid()'),
        ),
        sa.Column(
            'project_id',
            UUID(as_uuid=True),
            sa.ForeignKey('projects.id', ondelete='CASCADE'),
            nullable=False,
            index=True,
        ),

        # Aggregation Period
        sa.Column(
            'period_type',
            sa.String(20),
            nullable=False,
        ),  # monthly, quarterly
        sa.Column('period_start', sa.Date, nullable=False),
        sa.Column('period_end', sa.Date, nullable=False),

        # Statistics
        sa.Column('total_learnings', sa.Integer, nullable=False, server_default='0'),
        sa.Column('by_feedback_type', JSONB, nullable=False, server_default='{}'),
        sa.Column('by_severity', JSONB, nullable=False, server_default='{}'),
        sa.Column('top_patterns', JSONB, nullable=False, server_default='[]'),
        sa.Column('top_files', JSONB, nullable=False, server_default='[]'),

        # Generated Updates
        sa.Column('claude_md_suggestions', JSONB, nullable=True),
        sa.Column('decomposition_hints', JSONB, nullable=True),
        sa.Column('adr_recommendations', JSONB, nullable=True),

        # Processing
        sa.Column(
            'status',
            sa.String(20),
            nullable=False,
            server_default='pending',
        ),  # pending, processed, applied
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            'processed_by',
            UUID(as_uuid=True),
            sa.ForeignKey('users.id', ondelete='SET NULL'),
            nullable=True,
        ),

        # Audit
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('NOW()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('NOW()'),
            nullable=False,
        ),

        # Constraints
        sa.CheckConstraint(
            "period_type IN ('monthly', 'quarterly')",
            name='learning_aggregations_period_type_check',
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'processed', 'applied')",
            name='learning_aggregations_status_check',
        ),
        sa.UniqueConstraint(
            'project_id', 'period_type', 'period_start',
            name='learning_aggregations_unique_period',
        ),
    )

    # Index for finding aggregations
    op.create_index(
        'idx_learning_aggregations_project_period',
        'learning_aggregations',
        ['project_id', 'period_type', 'period_start'],
    )

    # Add table comments
    op.execute("""
        COMMENT ON TABLE pr_learnings IS 'PR review learnings for AI improvement (EP-11)';
        COMMENT ON COLUMN pr_learnings.feedback_type IS 'Category: pattern_violation, missing_requirement, edge_case, performance, security_issue, test_coverage, documentation, refactoring';
        COMMENT ON COLUMN pr_learnings.pattern_extracted IS 'Reusable pattern extracted from this learning for future generations';
    """)

    op.execute("""
        COMMENT ON TABLE learning_aggregations IS 'Monthly/quarterly aggregations of PR learnings';
        COMMENT ON COLUMN learning_aggregations.claude_md_suggestions IS 'Suggested additions to CLAUDE.md based on aggregated learnings';
        COMMENT ON COLUMN learning_aggregations.decomposition_hints IS 'Hints for AI task decomposition based on common issues';
    """)


def downgrade():
    # Drop indexes first
    op.drop_index('idx_learning_aggregations_project_period', table_name='learning_aggregations')
    op.drop_index('idx_pr_learnings_pr_number', table_name='pr_learnings')
    op.drop_index('idx_pr_learnings_status_applied', table_name='pr_learnings')
    op.drop_index('idx_pr_learnings_project_created', table_name='pr_learnings')
    op.drop_index('idx_pr_learnings_project_feedback', table_name='pr_learnings')

    # Drop tables
    op.drop_table('learning_aggregations')
    op.drop_table('pr_learnings')
