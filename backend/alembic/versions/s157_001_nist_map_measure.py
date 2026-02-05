"""Sprint 157: NIST AI RMF MAP & MEASURE Tables

Adds 2 new tables for MAP (context & categorization) and MEASURE
(performance metrics & bias detection) functions. Seeds 9 new controls
into existing compliance_controls table and updates NIST framework
total_controls from 5 to 14.

Sprint: 157 - Phase 3 COMPLIANCE (NIST AI RMF MAP & MEASURE)
Priority: P0
Reference: ADR-051

Tables:
- ai_systems: MAP context, categorization, stakeholders, dependencies
- performance_metrics: MEASURE time-series metrics, thresholds, bias tracking

Seeds:
- 5 MAP controls (MAP-1.1 through MAP-3.2)
- 4 MEASURE controls (MEASURE-1.1 through MEASURE-3.1)
- Update NIST_AI_RMF total_controls: 5 → 14

Revision ID: s157_001
Revises: s156_001
Create Date: 2026-04-14
"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "s157_001"
down_revision: Union[str, None] = "s156_001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create 2 tables for MAP & MEASURE, seed 9 controls."""

    # =========================================================================
    # Table 1: ai_systems (MAP context & categorization)
    # =========================================================================

    op.create_table(
        "ai_systems",
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
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column(
            "system_type",
            sa.String(50),
            nullable=False,
            comment="nlp, vision, recommendation, decision, generative",
        ),
        sa.Column(
            "risk_level",
            sa.String(20),
            nullable=False,
            server_default="medium",
            comment="minimal, limited, high, unacceptable",
        ),
        sa.Column("purpose", sa.Text, nullable=True, comment="MAP-1.1: intended purpose"),
        sa.Column("scope", sa.Text, nullable=True, comment="MAP-1.1: deployment scope"),
        sa.Column(
            "stakeholders",
            postgresql.JSONB,
            nullable=False,
            server_default="[]",
            comment="MAP-1.2: [{role, name, impact_type}]",
        ),
        sa.Column(
            "dependencies",
            postgresql.JSONB,
            nullable=False,
            server_default="[]",
            comment="MAP-3.2: [{name, type, version, provider}]",
        ),
        sa.Column(
            "categorization",
            postgresql.JSONB,
            nullable=True,
            comment="MAP-2.1: {risk_tier, data_sensitivity, autonomy_level, reversibility}",
        ),
        sa.Column(
            "owner_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
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
        sa.UniqueConstraint("project_id", "name", name="uq_ai_system_project_name"),
        comment="AI systems for NIST MAP context & categorization",
    )

    op.create_index("ix_ai_systems_project", "ai_systems", ["project_id"])
    op.create_index(
        "ix_ai_systems_project_active",
        "ai_systems",
        ["project_id", "is_active"],
        postgresql_where=sa.text("is_active = true"),
    )

    # =========================================================================
    # Table 2: performance_metrics (MEASURE time-series)
    # =========================================================================

    op.create_table(
        "performance_metrics",
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
            "metric_type",
            sa.String(50),
            nullable=False,
            comment="accuracy, precision, recall, f1_score, latency_p95, bias_score, disparity_index, custom",
        ),
        sa.Column("metric_name", sa.String(200), nullable=False),
        sa.Column("metric_value", sa.Float, nullable=False),
        sa.Column("threshold_min", sa.Float, nullable=True, comment="Acceptable lower bound"),
        sa.Column("threshold_max", sa.Float, nullable=True, comment="Acceptable upper bound"),
        sa.Column(
            "is_within_threshold",
            sa.Boolean,
            nullable=False,
            server_default="true",
            comment="Computed: min<=value<=max",
        ),
        sa.Column("unit", sa.String(50), nullable=True, comment="%, ms, ratio"),
        sa.Column(
            "demographic_group",
            sa.String(100),
            nullable=True,
            comment="MEASURE-2.x: gender:female, age:18-25",
        ),
        sa.Column(
            "tags",
            postgresql.JSONB,
            nullable=False,
            server_default="[]",
            comment='["bias","fairness"], ["performance"]',
        ),
        sa.Column(
            "measured_at",
            sa.DateTime(timezone=True),
            nullable=False,
            comment="When measurement was taken",
        ),
        sa.Column(
            "measured_by_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        comment="Performance metrics for NIST MEASURE function",
    )

    op.create_index("ix_perf_metrics_project", "performance_metrics", ["project_id"])
    op.create_index("ix_perf_metrics_system", "performance_metrics", ["ai_system_id"])
    op.create_index(
        "ix_perf_metrics_trend",
        "performance_metrics",
        ["ai_system_id", "metric_type", "measured_at"],
    )

    # =========================================================================
    # Seed Data: 9 Controls (5 MAP + 4 MEASURE) into compliance_controls
    # =========================================================================

    # Look up the NIST framework ID
    # Use a subquery approach to get the framework ID
    nist_fwk_subquery = (
        "SELECT id FROM compliance_frameworks WHERE code = 'NIST_AI_RMF' LIMIT 1"
    )

    map_controls = [
        {
            "code": "MAP-1.1",
            "category": "MAP",
            "title": "Context Establishment",
            "description": (
                "All AI systems must have documented intended purpose and deployment scope. "
                "Each system must clearly define its context including the problem it solves, "
                "target users, operational environment, and limitations."
            ),
            "severity": "high",
            "gate_mapping": "G1",
            "opa_policy": "compliance.nist.map.context_establishment",
            "sort_order": 6,
            "evidence": (
                '[{"type": "document", "description": "AI system purpose and scope documentation", '
                '"required": true, "accepted_formats": ["pdf", "md"]}, '
                '{"type": "attestation", "description": "Owner sign-off on context accuracy", '
                '"required": true, "accepted_formats": ["pdf", "signed_form"]}]'
            ),
        },
        {
            "code": "MAP-1.2",
            "category": "MAP",
            "title": "Stakeholder Identification",
            "description": (
                "All AI systems must identify affected stakeholders with their roles and impact types. "
                "Stakeholder analysis must include end users, impacted communities, operators, "
                "and oversight bodies with documented impact assessments."
            ),
            "severity": "medium",
            "gate_mapping": "G1",
            "opa_policy": "compliance.nist.map.context_establishment",
            "sort_order": 7,
            "evidence": (
                '[{"type": "document", "description": "Stakeholder analysis with impact assessment", '
                '"required": true, "accepted_formats": ["pdf", "md", "csv"]}, '
                '{"type": "report", "description": "Stakeholder consultation summary", '
                '"required": false, "accepted_formats": ["pdf", "md"]}]'
            ),
        },
        {
            "code": "MAP-2.1",
            "category": "MAP",
            "title": "System Categorization",
            "description": (
                "All AI systems must have valid risk categorization including risk tier, "
                "data sensitivity level, autonomy level, and reversibility assessment. "
                "Categorization follows EU AI Act risk taxonomy: minimal, limited, high, unacceptable."
            ),
            "severity": "critical",
            "gate_mapping": "G1",
            "opa_policy": "compliance.nist.map.system_categorization",
            "sort_order": 8,
            "evidence": (
                '[{"type": "document", "description": "AI system risk categorization assessment", '
                '"required": true, "accepted_formats": ["pdf", "md"]}, '
                '{"type": "attestation", "description": "Risk tier approval by governance board", '
                '"required": true, "accepted_formats": ["pdf", "signed_form"]}]'
            ),
        },
        {
            "code": "MAP-3.1",
            "category": "MAP",
            "title": "Risk and Impact Mapping",
            "description": (
                "All identified AI risks must have documented impact areas and affected stakeholders. "
                "Each risk entry must map to at least one impact area (safety, fairness, privacy, "
                "security) and identify specific affected stakeholder groups."
            ),
            "severity": "high",
            "gate_mapping": "G2",
            "opa_policy": "compliance.nist.map.risk_impact_mapping",
            "sort_order": 9,
            "evidence": (
                '[{"type": "report", "description": "Risk-to-impact mapping analysis", '
                '"required": true, "accepted_formats": ["pdf", "md"]}, '
                '{"type": "document", "description": "Stakeholder impact assessment per risk", '
                '"required": true, "accepted_formats": ["pdf", "csv"]}]'
            ),
        },
        {
            "code": "MAP-3.2",
            "category": "MAP",
            "title": "Dependency Mapping",
            "description": (
                "All AI systems must document their dependencies including third-party models, "
                "data sources, APIs, and infrastructure components with provider details and versions."
            ),
            "severity": "medium",
            "gate_mapping": "G2",
            "opa_policy": "compliance.nist.map.risk_impact_mapping",
            "sort_order": 10,
            "evidence": (
                '[{"type": "document", "description": "System dependency inventory with versions", '
                '"required": true, "accepted_formats": ["pdf", "md", "csv", "json"]}, '
                '{"type": "report", "description": "Dependency risk assessment", '
                '"required": false, "accepted_formats": ["pdf", "md"]}]'
            ),
        },
    ]

    measure_controls = [
        {
            "code": "MEASURE-1.1",
            "category": "MEASURE",
            "title": "Performance Thresholds",
            "description": (
                "All AI system metrics must have defined performance thresholds and current values "
                "within acceptable bounds. Each metric must specify minimum and/or maximum acceptable "
                "values with regular measurement schedules."
            ),
            "severity": "high",
            "gate_mapping": "G2",
            "opa_policy": "compliance.nist.measure.performance_thresholds",
            "sort_order": 11,
            "evidence": (
                '[{"type": "report", "description": "Performance metrics report with threshold analysis", '
                '"required": true, "accepted_formats": ["pdf", "csv", "json"]}, '
                '{"type": "test_result", "description": "Automated performance test results", '
                '"required": true, "accepted_formats": ["json", "csv"]}]'
            ),
        },
        {
            "code": "MEASURE-2.1",
            "category": "MEASURE",
            "title": "Bias Detection",
            "description": (
                "Bias metrics must be measured across at least 2 demographic groups per AI system. "
                "All bias score metrics must be within acceptable thresholds. Systems must demonstrate "
                "equitable performance across protected characteristics."
            ),
            "severity": "critical",
            "gate_mapping": "G2",
            "opa_policy": "compliance.nist.measure.bias_detection",
            "sort_order": 12,
            "evidence": (
                '[{"type": "report", "description": "Bias audit report per demographic group", '
                '"required": true, "accepted_formats": ["pdf", "csv"]}, '
                '{"type": "test_result", "description": "Fairness metric test results", '
                '"required": true, "accepted_formats": ["json", "csv"]}]'
            ),
        },
        {
            "code": "MEASURE-2.2",
            "category": "MEASURE",
            "title": "Disparity Analysis",
            "description": (
                "Disparity ratios between demographic groups must not exceed 1.25 (EEOC 4/5ths rule). "
                "Performance differences across groups must be analyzed and documented with corrective "
                "actions for any disparities exceeding the threshold."
            ),
            "severity": "critical",
            "gate_mapping": "G2",
            "opa_policy": "compliance.nist.measure.disparity_analysis",
            "sort_order": 13,
            "evidence": (
                '[{"type": "report", "description": "Disparity analysis report with 4/5ths rule check", '
                '"required": true, "accepted_formats": ["pdf", "csv"]}, '
                '{"type": "document", "description": "Corrective action plan for disparities", '
                '"required": false, "accepted_formats": ["pdf", "md"]}]'
            ),
        },
        {
            "code": "MEASURE-3.1",
            "category": "MEASURE",
            "title": "Metric Trending",
            "description": (
                "Each key metric must have at least 3 data points over time to establish trends. "
                "Trending analysis enables detection of performance degradation, bias drift, "
                "and proactive intervention before thresholds are breached."
            ),
            "severity": "medium",
            "gate_mapping": "G3",
            "opa_policy": None,
            "sort_order": 14,
            "evidence": (
                '[{"type": "report", "description": "Metric trend analysis with 30-day history", '
                '"required": true, "accepted_formats": ["pdf", "csv", "json"]}, '
                '{"type": "document", "description": "Trend monitoring configuration", '
                '"required": false, "accepted_formats": ["json", "yaml"]}]'
            ),
        },
    ]

    all_controls = map_controls + measure_controls

    for ctrl in all_controls:
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

    # Update total_controls from 5 → 14
    op.execute(
        """
        UPDATE compliance_frameworks
        SET total_controls = 14, updated_at = now()
        WHERE code = 'NIST_AI_RMF'
        """
    )


def downgrade() -> None:
    """Remove MAP/MEASURE tables and controls."""
    # Delete MAP and MEASURE controls
    op.execute(
        """
        DELETE FROM compliance_controls
        WHERE category IN ('MAP', 'MEASURE')
        AND framework_id = (
            SELECT id FROM compliance_frameworks WHERE code = 'NIST_AI_RMF'
        )
        """
    )

    # Revert total_controls from 14 → 5
    op.execute(
        """
        UPDATE compliance_frameworks
        SET total_controls = 5, updated_at = now()
        WHERE code = 'NIST_AI_RMF'
        """
    )

    op.drop_table("performance_metrics")
    op.drop_table("ai_systems")
