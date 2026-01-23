"""Sprint 101: CRP (Consultation Request Protocol) Tables

Revision ID: s101_002_crp_tables
Revises: s101_001_framework_version
Create Date: 2026-01-23 15:00:00.000000

Implements SDLC 5.2.0 Consultation Request Protocol:
- consultation_requests: Store CRP records for high-risk changes
- consultation_comments: Discussion thread for each consultation

CRP Workflow:
1. AI detects high-risk change (risk_score > 70)
2. CRP created automatically
3. Reviewer assigned based on expertise
4. Human reviews, comments, approves/rejects
5. Resolution tracked in Evidence Vault

Reference: docs/04-build/02-Sprint-Plans/SPRINT-101-DESIGN.md
Reference: SDLC Framework 5.2.0, AI Governance - CRP
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY


# revision identifiers, used by Alembic.
revision = 's101_002_crp_tables'
down_revision = 's101_001_framework_version'
branch_labels = None
depends_on = None


def upgrade():
    # =========================================================================
    # Table: consultation_requests
    # Main CRP records linking risk analysis to human review workflow.
    #
    # Status Flow:
    #   pending → in_review → approved/rejected
    #   pending → cancelled (if PR closed)
    #   pending → expired (if not resolved in time)
    #
    # Priority Levels:
    #   low: Can wait (SLA: 5 days)
    #   medium: Normal turnaround (SLA: 2 days)
    #   high: Needs quick attention (SLA: 1 day)
    #   urgent: Blocking work (SLA: 4 hours)
    # =========================================================================
    op.create_table(
        'consultation_requests',
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

        # External References
        sa.Column(
            'pr_id',
            sa.String(100),
            nullable=True,
            index=True,
        ),

        # Risk Analysis Link
        sa.Column(
            'risk_analysis_id',
            UUID(as_uuid=True),
            nullable=False,
            index=True,
        ),
        sa.Column('risk_analysis', JSONB, nullable=False),

        # Consultation Details
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column(
            'priority',
            sa.String(20),
            nullable=False,
            server_default='medium',
            index=True,
        ),
        sa.Column(
            'required_expertise',
            ARRAY(sa.String),
            nullable=False,
            server_default='{"general"}',
        ),
        sa.Column('diff_url', sa.String(500), nullable=True),

        # Status
        sa.Column(
            'status',
            sa.String(20),
            nullable=False,
            server_default='pending',
            index=True,
        ),

        # Participants
        sa.Column(
            'requester_id',
            UUID(as_uuid=True),
            sa.ForeignKey('users.id', ondelete='SET NULL'),
            nullable=True,
            index=True,
        ),
        sa.Column(
            'assigned_reviewer_id',
            UUID(as_uuid=True),
            sa.ForeignKey('users.id', ondelete='SET NULL'),
            nullable=True,
            index=True,
        ),
        sa.Column('assigned_at', sa.DateTime(timezone=True), nullable=True),

        # Resolution
        sa.Column('resolution_notes', sa.Text, nullable=True),
        sa.Column('conditions', ARRAY(sa.String), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column(
            'resolved_by_id',
            UUID(as_uuid=True),
            sa.ForeignKey('users.id', ondelete='SET NULL'),
            nullable=True,
        ),

        # Timestamps
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('NOW()'),
            nullable=False,
            index=True,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('NOW()'),
            nullable=False,
        ),

        # Check constraints
        sa.CheckConstraint(
            "status IN ('pending', 'in_review', 'approved', 'rejected', 'cancelled', 'expired')",
            name='consultation_requests_status_check',
        ),
        sa.CheckConstraint(
            "priority IN ('low', 'medium', 'high', 'urgent')",
            name='consultation_requests_priority_check',
        ),
    )

    # Composite indexes for common queries
    op.create_index(
        'idx_consultation_requests_project_status',
        'consultation_requests',
        ['project_id', 'status'],
    )
    op.create_index(
        'idx_consultation_requests_reviewer_status',
        'consultation_requests',
        ['assigned_reviewer_id', 'status'],
    )
    op.create_index(
        'idx_consultation_requests_pending',
        'consultation_requests',
        ['project_id', 'created_at'],
        postgresql_where=sa.text("status = 'pending'"),
    )

    # =========================================================================
    # Table: consultation_comments
    # Discussion thread for each consultation request.
    # =========================================================================
    op.create_table(
        'consultation_comments',
        sa.Column(
            'id',
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text('gen_random_uuid()'),
        ),
        sa.Column(
            'consultation_id',
            UUID(as_uuid=True),
            sa.ForeignKey('consultation_requests.id', ondelete='CASCADE'),
            nullable=False,
            index=True,
        ),
        sa.Column(
            'user_id',
            UUID(as_uuid=True),
            sa.ForeignKey('users.id', ondelete='SET NULL'),
            nullable=True,
            index=True,
        ),

        # Content
        sa.Column('comment', sa.Text, nullable=False),
        sa.Column(
            'is_resolution_note',
            sa.Boolean,
            nullable=False,
            server_default='false',
        ),

        # Timestamps
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('NOW()'),
            nullable=False,
            index=True,
        ),
    )

    # Index for fetching comments in order
    op.create_index(
        'idx_consultation_comments_thread',
        'consultation_comments',
        ['consultation_id', 'created_at'],
    )

    # Add table comments
    op.execute("""
        COMMENT ON TABLE consultation_requests IS 'CRP - Consultation Request Protocol for high-risk AI changes';
        COMMENT ON COLUMN consultation_requests.risk_analysis IS 'Full RiskAnalysis object that triggered this CRP';
        COMMENT ON COLUMN consultation_requests.required_expertise IS 'Expertise areas needed for review (security, database, api, etc.)';
        COMMENT ON COLUMN consultation_requests.status IS 'Workflow status: pending → in_review → approved/rejected';
        COMMENT ON COLUMN consultation_requests.conditions IS 'Conditions attached to approval (if any)';
    """)

    op.execute("""
        COMMENT ON TABLE consultation_comments IS 'Discussion thread for CRP consultations';
        COMMENT ON COLUMN consultation_comments.is_resolution_note IS 'True if this is a resolution note (vs. discussion)';
    """)


def downgrade():
    # Drop indexes first
    op.drop_index('idx_consultation_comments_thread', table_name='consultation_comments')
    op.drop_index('idx_consultation_requests_pending', table_name='consultation_requests')
    op.drop_index('idx_consultation_requests_reviewer_status', table_name='consultation_requests')
    op.drop_index('idx_consultation_requests_project_status', table_name='consultation_requests')

    # Drop tables
    op.drop_table('consultation_comments')
    op.drop_table('consultation_requests')
