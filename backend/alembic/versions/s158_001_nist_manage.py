"""Sprint 158: NIST AI RMF MANAGE Tables

Adds 2 new tables for MANAGE (risk response, incident management)
function. Seeds 5 new controls into existing compliance_controls table
and updates NIST framework total_controls from 14 to 19.

Sprint: 158 - Phase 3 COMPLIANCE (NIST AI RMF MANAGE)
Priority: P0
Reference: ADR-051

Tables:
- manage_risk_responses: Risk response plans linked to risk register
- manage_incidents: AI system incidents and post-deployment events

Seeds:
- 5 MANAGE controls (MANAGE-1.1, 2.1, 2.4, 3.1, 4.1)
- Update NIST_AI_RMF total_controls: 14 → 19

Revision ID: s158_001
Revises: s157_001
Create Date: 2026-04-21
"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "s158_001"
down_revision: Union[str, None] = "s157_001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create 2 tables for MANAGE, seed 5 controls."""

    # =========================================================================
    # Table 1: manage_risk_responses (Risk response plans)
    # =========================================================================

    op.create_table(
        "manage_risk_responses",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "project_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "risk_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("compliance_risk_register.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "response_type",
            sa.String(50),
            nullable=False,
            comment="mitigate, accept, transfer, avoid",
        ),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column(
            "assigned_to",
            sa.String(200),
            nullable=True,
            comment="Person/team responsible",
        ),
        sa.Column(
            "priority",
            sa.String(20),
            nullable=False,
            server_default="medium",
            comment="critical, high, medium, low",
        ),
        sa.Column(
            "status",
            sa.String(50),
            nullable=False,
            server_default="planned",
            comment="planned, in_progress, completed, deferred",
        ),
        sa.Column("due_date", sa.Date, nullable=True),
        sa.Column(
            "resources_allocated",
            postgresql.JSONB,
            nullable=False,
            server_default="[]",
            comment="[{type, description, budget}]",
        ),
        sa.Column(
            "deactivation_criteria",
            postgresql.JSONB,
            nullable=True,
            comment="MANAGE-2.4: {conditions: [], threshold, action}",
        ),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        comment="Risk response plans for NIST MANAGE function",
    )

    op.create_index(
        "ix_manage_risk_responses_project",
        "manage_risk_responses",
        ["project_id"],
    )
    op.create_index(
        "ix_manage_risk_responses_risk",
        "manage_risk_responses",
        ["risk_id"],
    )
    op.create_index(
        "ix_manage_risk_responses_status",
        "manage_risk_responses",
        ["project_id", "status"],
    )

    # =========================================================================
    # Table 2: manage_incidents (AI system incidents)
    # =========================================================================

    op.create_table(
        "manage_incidents",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "project_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "ai_system_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("ai_systems.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "risk_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("compliance_risk_register.id", ondelete="SET NULL"),
            nullable=True,
            comment="Optional link to risk that materialized",
        ),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column(
            "severity",
            sa.String(20),
            nullable=False,
            comment="critical, high, medium, low",
        ),
        sa.Column(
            "incident_type",
            sa.String(50),
            nullable=False,
            comment="performance_degradation, bias_detected, security_breach, availability, data_quality, compliance_violation",
        ),
        sa.Column(
            "status",
            sa.String(50),
            nullable=False,
            server_default="open",
            comment="open, investigating, mitigating, resolved, closed",
        ),
        sa.Column("reported_by", sa.String(200), nullable=True),
        sa.Column("assigned_to", sa.String(200), nullable=True),
        sa.Column("resolution", sa.Text, nullable=True),
        sa.Column("root_cause", sa.Text, nullable=True),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            nullable=False,
            comment="When the incident occurred",
        ),
        sa.Column(
            "resolved_at",
            sa.DateTime(timezone=True),
            nullable=True,
            comment="When the incident was resolved",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        comment="AI system incidents for NIST MANAGE function",
    )

    op.create_index(
        "ix_manage_incidents_project",
        "manage_incidents",
        ["project_id"],
    )
    op.create_index(
        "ix_manage_incidents_system",
        "manage_incidents",
        ["ai_system_id"],
    )
    op.create_index(
        "ix_manage_incidents_project_status",
        "manage_incidents",
        ["project_id", "status"],
    )
    op.create_index(
        "ix_manage_incidents_system_time",
        "manage_incidents",
        ["ai_system_id", "occurred_at"],
    )

    # =========================================================================
    # Seed Data: 5 MANAGE Controls into compliance_controls
    # =========================================================================

    nist_fwk_subquery = (
        "SELECT id FROM compliance_frameworks WHERE code = 'NIST_AI_RMF' LIMIT 1"
    )

    manage_controls = [
        {
            "code": "MANAGE-1.1",
            "category": "MANAGE",
            "title": "Risk Response Planning",
            "description": (
                "Every identified AI risk must have at least one documented response plan "
                "with an assigned owner and target completion date. Response types include "
                "mitigate, accept, transfer, or avoid per ISO 31000 risk treatment framework."
            ),
            "severity": "critical",
            "gate_mapping": "G2",
            "opa_policy": "compliance.nist.manage.risk_response_planning",
            "sort_order": 15,
            "evidence": (
                '[{"type": "document", "description": "Risk response plans with assigned owners", '
                '"required": true, "accepted_formats": ["pdf", "md"]}, '
                '{"type": "attestation", "description": "Response plan approval by risk committee", '
                '"required": true, "accepted_formats": ["pdf", "signed_form"]}]'
            ),
        },
        {
            "code": "MANAGE-2.1",
            "category": "MANAGE",
            "title": "Resource Allocation",
            "description": (
                "AI risk management activities must have allocated resources including budget, "
                "personnel, and tools. At least 50%% of non-accept risk responses must have "
                "documented resource allocations with positive budget assignments."
            ),
            "severity": "high",
            "gate_mapping": "G2",
            "opa_policy": "compliance.nist.manage.resource_allocation",
            "sort_order": 16,
            "evidence": (
                '[{"type": "document", "description": "Resource allocation plan with budget breakdown", '
                '"required": true, "accepted_formats": ["pdf", "csv", "xlsx"]}, '
                '{"type": "report", "description": "Resource utilization report", '
                '"required": false, "accepted_formats": ["pdf", "csv"]}]'
            ),
        },
        {
            "code": "MANAGE-2.4",
            "category": "MANAGE",
            "title": "System Deactivation Criteria",
            "description": (
                "At least one AI risk response must define deactivation criteria (kill switch) "
                "specifying conditions under which the AI system should be shut down, the "
                "threshold values that trigger deactivation, and the action to take."
            ),
            "severity": "high",
            "gate_mapping": "G2",
            "opa_policy": None,
            "sort_order": 17,
            "evidence": (
                '[{"type": "document", "description": "Deactivation criteria and kill switch procedures", '
                '"required": true, "accepted_formats": ["pdf", "md"]}, '
                '{"type": "attestation", "description": "Safety review board approval of deactivation plan", '
                '"required": true, "accepted_formats": ["pdf", "signed_form"]}]'
            ),
        },
        {
            "code": "MANAGE-3.1",
            "category": "MANAGE",
            "title": "Third-Party Monitoring",
            "description": (
                "All third-party AI systems (those with external dependencies) must have at "
                "least one incident review or monitoring check documented within the last 90 days. "
                "Third-party systems are identified by having external provider dependencies."
            ),
            "severity": "high",
            "gate_mapping": "G3",
            "opa_policy": "compliance.nist.manage.third_party_monitoring",
            "sort_order": 18,
            "evidence": (
                '[{"type": "report", "description": "Third-party vendor monitoring report (90-day)", '
                '"required": true, "accepted_formats": ["pdf", "csv"]}, '
                '{"type": "document", "description": "Vendor SLA compliance assessment", '
                '"required": false, "accepted_formats": ["pdf", "md"]}]'
            ),
        },
        {
            "code": "MANAGE-4.1",
            "category": "MANAGE",
            "title": "Post-Deployment Monitoring",
            "description": (
                "All active AI systems must have at least one performance metric recorded within "
                "the last 30 days and no unresolved critical incidents. This ensures ongoing "
                "monitoring of deployed systems for safety and performance."
            ),
            "severity": "critical",
            "gate_mapping": "G3",
            "opa_policy": "compliance.nist.manage.post_deployment_monitoring",
            "sort_order": 19,
            "evidence": (
                '[{"type": "report", "description": "Post-deployment monitoring dashboard report", '
                '"required": true, "accepted_formats": ["pdf", "json"]}, '
                '{"type": "test_result", "description": "Automated monitoring check results", '
                '"required": true, "accepted_formats": ["json", "csv"]}]'
            ),
        },
    ]

    for ctrl in manage_controls:
        ctrl_id = str(uuid4())
        opa_value = f"'{ctrl['opa_policy']}'" if ctrl["opa_policy"] else "NULL"
        op.execute(
            f"""
            INSERT INTO compliance_controls
                (id, framework_id, control_code, category, title, description,
                 severity, gate_mapping, evidence_required, opa_policy_code, sort_order)
            VALUES (
                '{ctrl_id}',
                ({nist_fwk_subquery}),
                '{ctrl["code"]}',
                '{ctrl["category"]}',
                '{ctrl["title"]}',
                '{ctrl["description"]}',
                '{ctrl["severity"]}',
                '{ctrl["gate_mapping"]}',
                '{ctrl["evidence"]}'::jsonb,
                {opa_value},
                {ctrl["sort_order"]}
            )
            """
        )

    # Update total_controls from 14 → 19
    op.execute(
        """
        UPDATE compliance_frameworks
        SET total_controls = 19, updated_at = now()
        WHERE code = 'NIST_AI_RMF'
        """
    )


def downgrade() -> None:
    """Remove MANAGE tables and controls."""
    # Delete MANAGE controls
    op.execute(
        """
        DELETE FROM compliance_controls
        WHERE category = 'MANAGE'
        AND framework_id = (
            SELECT id FROM compliance_frameworks WHERE code = 'NIST_AI_RMF'
        )
        """
    )

    # Revert total_controls from 19 → 14
    op.execute(
        """
        UPDATE compliance_frameworks
        SET total_controls = 14, updated_at = now()
        WHERE code = 'NIST_AI_RMF'
        """
    )

    op.drop_table("manage_incidents")
    op.drop_table("manage_risk_responses")
