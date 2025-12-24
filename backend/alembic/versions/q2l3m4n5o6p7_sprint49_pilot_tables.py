"""sprint49_pilot_tables

Revision ID: q2l3m4n5o6p7
Revises: p1k2l3m4n5o6
Create Date: 2025-12-24 07:30:00.000000

SDLC Stage: 04 - BUILD
Sprint: 49 - EP-06 Pilot Execution + Metrics Hardening
Epic: EP-06 IR-Based Codegen Engine
Framework: SDLC 5.1.1

Purpose:
Create pilot tracking tables for Vietnamese SME pilot program.
Track TTFV (Time To First Value) and satisfaction metrics.

Tables:
1. pilot_participants - Pilot program participants
2. pilot_sessions - Individual sessions with TTFV tracking
3. pilot_satisfaction_surveys - Post-generation satisfaction surveys
4. pilot_daily_metrics - Aggregated daily metrics for CEO dashboard

Success Metrics (CEO Approved):
- 10 Vietnamese SME founders
- TTFV < 30 minutes
- Satisfaction score 8/10
- Quality gate pass rate 95%+

Retention:
- All pilot tables: 2 years (pilot program analysis)
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "q2l3m4n5o6p7"
down_revision: Union[str, None] = "p1k2l3m4n5o6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create pilot_participants table
    op.create_table(
        "pilot_participants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        # Participant info
        sa.Column("status", sa.String(20), nullable=False, default="invited"),
        sa.Column("domain", sa.String(20), nullable=True),
        sa.Column("company_name", sa.String(255), nullable=True),
        sa.Column("company_size", sa.String(20), nullable=True),
        # Recruitment tracking
        sa.Column("invited_at", sa.DateTime, nullable=True),
        sa.Column("registered_at", sa.DateTime, nullable=True),
        sa.Column("first_login_at", sa.DateTime, nullable=True),
        sa.Column("activated_at", sa.DateTime, nullable=True),
        # Pilot metrics
        sa.Column("total_sessions", sa.Integer, default=0),
        sa.Column("total_generations", sa.Integer, default=0),
        sa.Column("successful_generations", sa.Integer, default=0),
        sa.Column("quality_gate_passes", sa.Integer, default=0),
        sa.Column("quality_gate_failures", sa.Integer, default=0),
        # TTFV metrics
        sa.Column("best_ttfv_seconds", sa.Integer, nullable=True),
        sa.Column("avg_ttfv_seconds", sa.Integer, nullable=True),
        # Satisfaction
        sa.Column("latest_satisfaction_score", sa.Integer, nullable=True),
        sa.Column("would_recommend", sa.Boolean, nullable=True),
        # Metadata
        sa.Column("referral_source", sa.String(100), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    # Indexes for pilot_participants
    op.create_index("ix_pilot_participants_id", "pilot_participants", ["id"])
    op.create_index("ix_pilot_participants_user_id", "pilot_participants", ["user_id"])
    op.create_index("ix_pilot_participants_status", "pilot_participants", ["status"])
    op.create_index("ix_pilot_participants_domain", "pilot_participants", ["domain"])
    op.create_index(
        "ix_pilot_participant_status_domain",
        "pilot_participants",
        ["status", "domain"],
    )

    # 2. Create pilot_sessions table
    op.create_table(
        "pilot_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "participant_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("pilot_participants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("onboarding_session_id", sa.String(36), nullable=True),
        # Session lifecycle
        sa.Column("started_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime, nullable=True),
        sa.Column("abandoned_at", sa.DateTime, nullable=True),
        # Stage tracking
        sa.Column("current_stage", sa.String(30), nullable=False, default="started"),
        sa.Column("stage_history", postgresql.JSONB, nullable=True),
        # Stage timestamps
        sa.Column("domain_selected_at", sa.DateTime, nullable=True),
        sa.Column("app_named_at", sa.DateTime, nullable=True),
        sa.Column("features_selected_at", sa.DateTime, nullable=True),
        sa.Column("scale_selected_at", sa.DateTime, nullable=True),
        sa.Column("blueprint_generated_at", sa.DateTime, nullable=True),
        sa.Column("code_generation_started_at", sa.DateTime, nullable=True),
        sa.Column("code_generation_completed_at", sa.DateTime, nullable=True),
        sa.Column("quality_gate_passed_at", sa.DateTime, nullable=True),
        sa.Column("deployed_at", sa.DateTime, nullable=True),
        # TTFV calculation
        sa.Column("ttfv_seconds", sa.Integer, nullable=True),
        sa.Column("ttfv_target_met", sa.Boolean, nullable=True),
        # Generation details
        sa.Column("domain", sa.String(20), nullable=True),
        sa.Column("app_name", sa.String(100), nullable=True),
        sa.Column("selected_features", postgresql.JSONB, nullable=True),
        sa.Column("scale", sa.String(20), nullable=True),
        # Code generation metrics
        sa.Column("generation_provider", sa.String(20), nullable=True),
        sa.Column("generation_time_ms", sa.Integer, nullable=True),
        sa.Column("tokens_used", sa.Integer, nullable=True),
        sa.Column("files_generated", sa.Integer, nullable=True),
        sa.Column("lines_of_code", sa.Integer, nullable=True),
        # Quality gate results
        sa.Column("quality_gate_passed", sa.Boolean, nullable=True),
        sa.Column("quality_gate_score", sa.Float, nullable=True),
        sa.Column("quality_gate_details", postgresql.JSONB, nullable=True),
        # Error tracking
        sa.Column("errors", postgresql.JSONB, nullable=True),
        sa.Column("error_count", sa.Integer, default=0),
        # User context
        sa.Column("user_agent", sa.String(512), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        # Metadata
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    # Indexes for pilot_sessions
    op.create_index("ix_pilot_sessions_id", "pilot_sessions", ["id"])
    op.create_index("ix_pilot_sessions_participant_id", "pilot_sessions", ["participant_id"])
    op.create_index("ix_pilot_sessions_onboarding_session_id", "pilot_sessions", ["onboarding_session_id"])
    op.create_index("ix_pilot_sessions_started_at", "pilot_sessions", ["started_at"])
    op.create_index(
        "ix_pilot_session_participant_started",
        "pilot_sessions",
        ["participant_id", "started_at"],
    )
    op.create_index(
        "ix_pilot_session_ttfv",
        "pilot_sessions",
        ["ttfv_seconds", "ttfv_target_met"],
    )

    # 3. Create pilot_satisfaction_surveys table
    op.create_table(
        "pilot_satisfaction_surveys",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "participant_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("pilot_participants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "session_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("pilot_sessions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        # Core satisfaction metrics
        sa.Column("overall_score", sa.Integer, nullable=False),
        sa.Column("would_recommend", sa.Boolean, nullable=True),
        sa.Column("ease_of_use_score", sa.Integer, nullable=True),
        sa.Column("code_quality_score", sa.Integer, nullable=True),
        sa.Column("speed_score", sa.Integer, nullable=True),
        # Qualitative feedback
        sa.Column("what_went_well", sa.Text, nullable=True),
        sa.Column("what_needs_improvement", sa.Text, nullable=True),
        sa.Column("feature_requests", sa.Text, nullable=True),
        sa.Column("bugs_reported", sa.Text, nullable=True),
        # Structured feedback
        sa.Column("pain_points", postgresql.JSONB, nullable=True),
        sa.Column("favorite_features", postgresql.JSONB, nullable=True),
        sa.Column("missing_features", postgresql.JSONB, nullable=True),
        # Context
        sa.Column("feedback_context", sa.String(50), nullable=True),
        sa.Column("submitted_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        # Metadata
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    # Indexes for pilot_satisfaction_surveys
    op.create_index("ix_pilot_satisfaction_surveys_id", "pilot_satisfaction_surveys", ["id"])
    op.create_index("ix_pilot_satisfaction_surveys_participant_id", "pilot_satisfaction_surveys", ["participant_id"])
    op.create_index("ix_pilot_satisfaction_surveys_session_id", "pilot_satisfaction_surveys", ["session_id"])
    op.create_index("ix_pilot_satisfaction_surveys_submitted_at", "pilot_satisfaction_surveys", ["submitted_at"])
    op.create_index(
        "ix_pilot_satisfaction_participant_submitted",
        "pilot_satisfaction_surveys",
        ["participant_id", "submitted_at"],
    )

    # 4. Create pilot_daily_metrics table
    op.create_table(
        "pilot_daily_metrics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("date", sa.Date, nullable=False, unique=True),
        # Participant metrics
        sa.Column("total_participants", sa.Integer, default=0),
        sa.Column("active_participants", sa.Integer, default=0),
        sa.Column("new_participants", sa.Integer, default=0),
        sa.Column("churned_participants", sa.Integer, default=0),
        # Session metrics
        sa.Column("total_sessions", sa.Integer, default=0),
        sa.Column("completed_sessions", sa.Integer, default=0),
        sa.Column("abandoned_sessions", sa.Integer, default=0),
        # TTFV metrics
        sa.Column("avg_ttfv_seconds", sa.Integer, nullable=True),
        sa.Column("min_ttfv_seconds", sa.Integer, nullable=True),
        sa.Column("max_ttfv_seconds", sa.Integer, nullable=True),
        sa.Column("ttfv_target_met_count", sa.Integer, default=0),
        sa.Column("ttfv_target_missed_count", sa.Integer, default=0),
        # Quality gate metrics
        sa.Column("quality_gate_passes", sa.Integer, default=0),
        sa.Column("quality_gate_failures", sa.Integer, default=0),
        sa.Column("quality_gate_pass_rate", sa.Float, nullable=True),
        # Satisfaction metrics
        sa.Column("surveys_submitted", sa.Integer, default=0),
        sa.Column("avg_satisfaction_score", sa.Float, nullable=True),
        sa.Column("nps_promoters", sa.Integer, default=0),
        sa.Column("nps_passives", sa.Integer, default=0),
        sa.Column("nps_detractors", sa.Integer, default=0),
        # Generation metrics
        sa.Column("total_generations", sa.Integer, default=0),
        sa.Column("successful_generations", sa.Integer, default=0),
        sa.Column("failed_generations", sa.Integer, default=0),
        sa.Column("avg_generation_time_ms", sa.Integer, nullable=True),
        sa.Column("total_tokens_used", sa.Integer, default=0),
        # Domain breakdown
        sa.Column("domain_breakdown", postgresql.JSONB, nullable=True),
        # Metadata
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    # Indexes for pilot_daily_metrics
    op.create_index("ix_pilot_daily_metrics_id", "pilot_daily_metrics", ["id"])
    op.create_index("ix_pilot_daily_metrics_date", "pilot_daily_metrics", ["date"])


def downgrade() -> None:
    # Drop tables in reverse order (due to foreign key constraints)
    op.drop_table("pilot_daily_metrics")
    op.drop_table("pilot_satisfaction_surveys")
    op.drop_table("pilot_sessions")
    op.drop_table("pilot_participants")
