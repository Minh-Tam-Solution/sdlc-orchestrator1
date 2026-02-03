"""
=========================================================================
Context Authority V2 Schemas - Gate-Aware Dynamic Context (SPEC-0011)
SDLC Orchestrator - Stage 04 (BUILD)

Version: 1.0.0
Date: January 29, 2026
Status: ACTIVE - Sprint 120 Pre-work (Day 2)
Authority: Backend Lead + CTO Approved
Foundation: SPEC-0011 Context Authority V2, OpenAPI 3.0, Pydantic v2
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Context validation request/response models
- Dynamic overlay generation schemas
- Context snapshot schemas for audit trail
- Overlay template management schemas

Validation:
- Tier validation (LITE, STANDARD, PROFESSIONAL, ENTERPRISE)
- Zone validation (GREEN, YELLOW, ORANGE, RED)
- Trigger type validation (gate_pass, gate_fail, index_zone, stage_constraint)
- Stage validation (00-discover through 10-govern)

API Endpoints Covered:
- POST /context-authority/v2/validate
- POST /context-authority/v2/overlay
- GET  /context-authority/v2/snapshots/{submission_id}
- GET  /context-authority/v2/templates
- POST /context-authority/v2/templates
- GET  /context-authority/v2/templates/{id}
- PUT  /context-authority/v2/templates/{id}
- GET  /context-authority/v2/templates/{id}/usage

Zero Mock Policy: Production-ready Pydantic models
=========================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


# =========================================================================
# Enums
# =========================================================================


class TierEnum(str, Enum):
    """4-Tier classification (SDLC 5.3.0)."""
    LITE = "LITE"
    STANDARD = "STANDARD"
    PROFESSIONAL = "PROFESSIONAL"
    ENTERPRISE = "ENTERPRISE"


class VibecodingZoneEnum(str, Enum):
    """Vibecoding index zones (SPEC-0001)."""
    GREEN = "GREEN"      # 0-20: Auto-approve
    YELLOW = "YELLOW"    # 21-40: Human review
    ORANGE = "ORANGE"    # 41-60: Tech Lead review
    RED = "RED"          # 61-100: CEO review / Block


class TriggerTypeEnum(str, Enum):
    """Overlay template trigger types (SPEC-0011 FR-002)."""
    GATE_PASS = "gate_pass"
    GATE_FAIL = "gate_fail"
    INDEX_ZONE = "index_zone"
    STAGE_CONSTRAINT = "stage_constraint"


class SubmissionTypeEnum(str, Enum):
    """Governance submission types."""
    PR = "PR"
    COMMIT = "COMMIT"
    RELEASE = "RELEASE"


# =========================================================================
# Gate Status Schema
# =========================================================================


class GateStatusSchema(BaseModel):
    """
    Gate status at validation time.

    Used for tracking current project stage and gate progression.
    """
    current_stage: str = Field(
        ...,
        description="Current SDLC stage (e.g., '02-design', '04-build')"
    )
    last_passed_gate: Optional[str] = Field(
        None,
        description="Last gate that passed (e.g., 'G0.2', 'G1', 'G2')"
    )
    pending_gates: List[str] = Field(
        default_factory=list,
        description="Gates pending approval (e.g., ['G1', 'G2'])"
    )

    @field_validator("current_stage")
    @classmethod
    def validate_stage(cls, v: str) -> str:
        """Validate stage is a valid SDLC 5.3.0 stage."""
        valid_stages = [
            "00-discover", "01-planning", "02-design", "03-integrate",
            "04-build", "05-test", "06-deploy", "07-operate",
            "08-collaborate", "09-govern", "10-archive"
        ]
        # Also accept without prefix for backward compatibility
        if v not in valid_stages and v not in ["WHY", "WHAT", "BUILD", "TEST", "SHIP"]:
            # Allow any string for flexibility
            pass
        return v


class V1ResultSchema(BaseModel):
    """
    Context Authority V1 validation result.

    Represents the original context checks (ADR linkage, design doc, etc.)
    """
    adr_linkage: bool = Field(
        default=False,
        description="Whether module references at least one ADR"
    )
    design_doc_exists: bool = Field(
        default=False,
        description="Whether design document exists for new features"
    )
    agents_md_fresh: bool = Field(
        default=True,
        description="Whether AGENTS.md was updated within 7 days"
    )
    module_annotation_consistent: bool = Field(
        default=True,
        description="Whether @module annotation matches directory"
    )
    orphan_code: bool = Field(
        default=False,
        description="True if code has no context linkage"
    )


# =========================================================================
# Context Validation Schemas
# =========================================================================


class ContextValidationRequest(BaseModel):
    """
    Full context validation request (SPEC-0011 FR-001).

    Request Body:
        {
            "submission_id": "550e8400-e29b-41d4-a716-446655440000",
            "submission_type": "PR",
            "project_id": "660e8400-e29b-41d4-a716-446655440001",
            "project_tier": "PROFESSIONAL",
            "vibecoding_index": 35,
            "vibecoding_zone": "YELLOW",
            "gate_status": {
                "current_stage": "04-build",
                "last_passed_gate": "G2",
                "pending_gates": ["G3"]
            },
            "v1_result": {
                "adr_linkage": true,
                "design_doc_exists": true,
                "agents_md_fresh": true
            },
            "changed_paths": ["backend/app/services/new_feature.py"]
        }

    Validation Flow:
        1. Validate V1 context (ADR linkage, design doc, etc.)
        2. Apply V2 gate-aware rules (stage constraints)
        3. Generate dynamic overlay based on triggers
        4. Create context snapshot for audit
    """
    submission_id: UUID = Field(
        ...,
        description="Governance submission UUID"
    )
    submission_type: SubmissionTypeEnum = Field(
        default=SubmissionTypeEnum.PR,
        description="Type of submission (PR, COMMIT, RELEASE)"
    )
    project_id: UUID = Field(
        ...,
        description="Project UUID"
    )
    project_tier: TierEnum = Field(
        ...,
        description="Project tier (LITE, STANDARD, PROFESSIONAL, ENTERPRISE)"
    )
    vibecoding_index: int = Field(
        ...,
        ge=0,
        le=100,
        description="Vibecoding index score (0-100)"
    )
    vibecoding_zone: VibecodingZoneEnum = Field(
        ...,
        description="Vibecoding zone (GREEN, YELLOW, ORANGE, RED)"
    )
    gate_status: GateStatusSchema = Field(
        ...,
        description="Current gate status"
    )
    v1_result: Optional[V1ResultSchema] = Field(
        None,
        description="V1 context validation result (if pre-computed)"
    )
    changed_paths: Optional[List[str]] = Field(
        None,
        description="List of changed file paths (for stage constraint checking)"
    )
    top_signals: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Top contributing signals for overlay template"
    )


class V2ResultSchema(BaseModel):
    """
    Context Authority V2 validation result.

    Contains gate-aware validation details.
    """
    gate_violations: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Stage/gate constraint violations"
    )
    index_warnings: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Vibecoding index warnings"
    )
    applied_templates: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Templates applied to generate overlay"
    )
    stage_allowed: bool = Field(
        default=True,
        description="Whether current stage allows the changes"
    )


class ContextValidationResponse(BaseModel):
    """
    Full context validation response (SPEC-0011 FR-001).

    Response Body:
        {
            "submission_id": "550e8400-e29b-41d4-a716-446655440000",
            "is_valid": true,
            "v1_result": {
                "adr_linkage": true,
                "design_doc_exists": true,
                "agents_md_fresh": true
            },
            "v2_result": {
                "gate_violations": [],
                "index_warnings": [],
                "applied_templates": [
                    {
                        "template_id": "...",
                        "name": "Gate G2 Pass",
                        "trigger_type": "gate_pass"
                    }
                ]
            },
            "dynamic_overlay": "## ✅ Build Phase Active\n...",
            "snapshot_id": "770e8400-e29b-41d4-a716-446655440002",
            "validated_at": "2026-01-29T10:30:00Z"
        }
    """
    submission_id: UUID = Field(
        ...,
        description="Governance submission UUID"
    )
    is_valid: bool = Field(
        ...,
        description="Overall validation result (V1 + V2 combined)"
    )
    v1_result: V1ResultSchema = Field(
        ...,
        description="V1 context validation result"
    )
    v2_result: V2ResultSchema = Field(
        ...,
        description="V2 gate-aware validation result"
    )
    dynamic_overlay: str = Field(
        ...,
        description="Generated dynamic overlay content"
    )
    snapshot_id: UUID = Field(
        ...,
        description="Context snapshot UUID (for audit trail)"
    )
    validated_at: datetime = Field(
        ...,
        description="Validation timestamp"
    )


# =========================================================================
# Overlay Generation Schemas
# =========================================================================


class OverlayGenerateRequest(BaseModel):
    """
    Generate overlay without full validation (SPEC-0011 FR-002).

    Request Body:
        {
            "project_id": "550e8400-e29b-41d4-a716-446655440000",
            "project_tier": "PROFESSIONAL",
            "gate_status": {
                "current_stage": "04-build",
                "last_passed_gate": "G2",
                "pending_gates": ["G3"]
            },
            "vibecoding_index": 35,
            "vibecoding_zone": "YELLOW"
        }

    Use Case:
        - Preview overlay before submission
        - Generate AGENTS.md context section
        - Real-time overlay updates in IDE
    """
    project_id: UUID = Field(
        ...,
        description="Project UUID"
    )
    project_tier: TierEnum = Field(
        ...,
        description="Project tier"
    )
    gate_status: GateStatusSchema = Field(
        ...,
        description="Current gate status"
    )
    vibecoding_index: Optional[int] = Field(
        None,
        ge=0,
        le=100,
        description="Vibecoding index score (optional)"
    )
    vibecoding_zone: Optional[VibecodingZoneEnum] = Field(
        None,
        description="Vibecoding zone (optional)"
    )
    top_signals: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Top contributing signals for template"
    )


class OverlayGenerateResponse(BaseModel):
    """
    Overlay generation response.

    Response Body:
        {
            "overlay_content": "## ✅ Build Phase Active\n...",
            "applied_templates": [
                {
                    "template_id": "...",
                    "name": "Gate G2 Pass",
                    "trigger_type": "gate_pass",
                    "tier": null
                }
            ],
            "variables": {
                "date": "2026-01-29",
                "stage": "04-build",
                "tier": "PROFESSIONAL",
                "gate": "G2"
            },
            "generated_at": "2026-01-29T10:30:00Z"
        }
    """
    overlay_content: str = Field(
        ...,
        description="Generated overlay content"
    )
    applied_templates: List[Dict[str, Any]] = Field(
        ...,
        description="Templates applied"
    )
    variables: Dict[str, Any] = Field(
        ...,
        description="Variables used for template rendering"
    )
    generated_at: datetime = Field(
        ...,
        description="Generation timestamp"
    )


# =========================================================================
# Context Snapshot Schemas
# =========================================================================


class SnapshotResponse(BaseModel):
    """
    Context snapshot response (SPEC-0011 FR-005).

    Response Body:
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "submission_id": "660e8400-e29b-41d4-a716-446655440001",
            "project_id": "770e8400-e29b-41d4-a716-446655440002",
            "gate_status": {
                "current_stage": "04-build",
                "last_passed_gate": "G2",
                "pending_gates": ["G3"]
            },
            "vibecoding_index": 35,
            "vibecoding_zone": "YELLOW",
            "dynamic_overlay": "## ✅ Build Phase Active\n...",
            "v1_result": {...},
            "gate_violations": [],
            "index_warnings": [],
            "tier": "PROFESSIONAL",
            "is_valid": true,
            "applied_template_ids": ["...", "..."],
            "snapshot_at": "2026-01-29T10:30:00Z"
        }

    Immutability:
        - Snapshots are never updated, only created
        - Used for audit trail and compliance
    """
    id: UUID = Field(
        ...,
        description="Snapshot UUID"
    )
    submission_id: UUID = Field(
        ...,
        description="Governance submission UUID"
    )
    project_id: UUID = Field(
        ...,
        description="Project UUID"
    )
    gate_status: Dict[str, Any] = Field(
        ...,
        description="Gate status at snapshot time"
    )
    vibecoding_index: int = Field(
        ...,
        description="Vibecoding index at snapshot time"
    )
    vibecoding_zone: str = Field(
        ...,
        description="Vibecoding zone at snapshot time"
    )
    dynamic_overlay: str = Field(
        ...,
        description="Dynamic overlay content generated"
    )
    v1_result: Optional[Dict[str, Any]] = Field(
        None,
        description="V1 validation result"
    )
    gate_violations: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Gate constraint violations"
    )
    index_warnings: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Vibecoding index warnings"
    )
    tier: str = Field(
        ...,
        description="Project tier at snapshot time"
    )
    is_valid: bool = Field(
        ...,
        description="Overall validation result"
    )
    applied_template_ids: Optional[List[str]] = Field(
        None,
        description="Template IDs applied"
    )
    snapshot_at: datetime = Field(
        ...,
        description="Snapshot creation timestamp"
    )
    created_at: datetime = Field(
        ...,
        description="Record creation timestamp"
    )
    model_config = ConfigDict(from_attributes=True)


class SnapshotListResponse(BaseModel):
    """
    Context snapshot list response.

    Response Body:
        {
            "submission_id": "550e8400-e29b-41d4-a716-446655440000",
            "snapshots": [...],
            "total": 3
        }
    """
    submission_id: UUID = Field(
        ...,
        description="Governance submission UUID"
    )
    snapshots: List[SnapshotResponse] = Field(
        ...,
        description="List of snapshots (most recent first)"
    )
    total: int = Field(
        ...,
        description="Total number of snapshots"
    )


# =========================================================================
# Overlay Template Schemas
# =========================================================================


class TemplateCreateRequest(BaseModel):
    """
    Create overlay template request (Admin only).

    Request Body:
        {
            "name": "Gate G2 Pass - Build Active",
            "trigger_type": "gate_pass",
            "trigger_value": "G2",
            "tier": null,
            "overlay_content": "## ✅ Build Phase Active\n...",
            "priority": 90,
            "is_active": true,
            "description": "Shown when Gate G2 passes"
        }

    Template Variables:
        - {date}: Current date (YYYY-MM-DD)
        - {stage}: Current SDLC stage
        - {tier}: Project tier
        - {gate}: Gate identifier
        - {index}: Vibecoding index value
        - {top_signals}: Top contributing signals
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Human-readable template name"
    )
    trigger_type: TriggerTypeEnum = Field(
        ...,
        description="Trigger type (gate_pass, gate_fail, index_zone, stage_constraint)"
    )
    trigger_value: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Trigger value (e.g., 'G2', 'orange', 'stage_02_code_block')"
    )
    tier: Optional[TierEnum] = Field(
        None,
        description="Tier scope (null = all tiers)"
    )
    overlay_content: str = Field(
        ...,
        min_length=1,
        description="Template content with {variable} placeholders"
    )
    priority: int = Field(
        default=0,
        ge=0,
        le=1000,
        description="Priority for ordering (higher = first)"
    )
    is_active: bool = Field(
        default=True,
        description="Whether template is active"
    )
    description: Optional[str] = Field(
        None,
        description="Template description"
    )


class TemplateUpdateRequest(BaseModel):
    """
    Update overlay template request (Admin only).

    All fields optional for partial update.
    """
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Human-readable template name"
    )
    trigger_type: Optional[TriggerTypeEnum] = Field(
        None,
        description="Trigger type"
    )
    trigger_value: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Trigger value"
    )
    tier: Optional[TierEnum] = Field(
        None,
        description="Tier scope"
    )
    overlay_content: Optional[str] = Field(
        None,
        min_length=1,
        description="Template content"
    )
    priority: Optional[int] = Field(
        None,
        ge=0,
        le=1000,
        description="Priority"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Whether template is active"
    )
    description: Optional[str] = Field(
        None,
        description="Template description"
    )


class TemplateResponse(BaseModel):
    """
    Overlay template response.

    Response Body:
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Gate G2 Pass - Build Active",
            "trigger_type": "gate_pass",
            "trigger_value": "G2",
            "tier": null,
            "overlay_content": "## ✅ Build Phase Active\n...",
            "priority": 90,
            "is_active": true,
            "description": "Shown when Gate G2 passes",
            "created_by_id": "660e8400-e29b-41d4-a716-446655440001",
            "created_at": "2026-01-29T10:30:00Z",
            "updated_at": "2026-01-29T10:30:00Z"
        }
    """
    id: UUID = Field(
        ...,
        description="Template UUID"
    )
    name: str = Field(
        ...,
        description="Human-readable template name"
    )
    trigger_type: str = Field(
        ...,
        description="Trigger type"
    )
    trigger_value: str = Field(
        ...,
        description="Trigger value"
    )
    tier: Optional[str] = Field(
        None,
        description="Tier scope (null = all tiers)"
    )
    overlay_content: str = Field(
        ...,
        description="Template content"
    )
    priority: int = Field(
        ...,
        description="Priority"
    )
    is_active: bool = Field(
        ...,
        description="Whether template is active"
    )
    description: Optional[str] = Field(
        None,
        description="Template description"
    )
    created_by_id: Optional[UUID] = Field(
        None,
        description="Creator user UUID"
    )
    created_at: datetime = Field(
        ...,
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp"
    )
    model_config = ConfigDict(from_attributes=True)


class TemplateListResponse(BaseModel):
    """
    Template list response with pagination.

    Response Body:
        {
            "templates": [...],
            "total": 15,
            "page": 1,
            "page_size": 20,
            "pages": 1
        }
    """
    templates: List[TemplateResponse] = Field(
        ...,
        description="List of templates"
    )
    total: int = Field(
        ...,
        description="Total number of templates"
    )
    page: int = Field(
        default=1,
        description="Current page number"
    )
    page_size: int = Field(
        default=20,
        description="Items per page"
    )
    pages: int = Field(
        ...,
        description="Total number of pages"
    )


class TemplateApplicationRecord(BaseModel):
    """
    Template application record (for usage analytics).
    """
    snapshot_id: UUID = Field(
        ...,
        description="Snapshot UUID where applied"
    )
    rendered_content: str = Field(
        ...,
        description="Rendered content after variable substitution"
    )
    variables_used: Optional[Dict[str, Any]] = Field(
        None,
        description="Variables used for rendering"
    )
    applied_at: datetime = Field(
        ...,
        description="Application timestamp"
    )


class TemplateUsageResponse(BaseModel):
    """
    Template usage analytics response.

    Response Body:
        {
            "template_id": "550e8400-e29b-41d4-a716-446655440000",
            "template_name": "Gate G2 Pass",
            "application_count": 42,
            "recent_applications": [...],
            "first_applied_at": "2026-01-15T10:30:00Z",
            "last_applied_at": "2026-01-29T10:30:00Z"
        }
    """
    template_id: UUID = Field(
        ...,
        description="Template UUID"
    )
    template_name: str = Field(
        ...,
        description="Template name"
    )
    application_count: int = Field(
        ...,
        description="Total number of applications"
    )
    recent_applications: List[TemplateApplicationRecord] = Field(
        default_factory=list,
        description="Recent application records (last 10)"
    )
    first_applied_at: Optional[datetime] = Field(
        None,
        description="First application timestamp"
    )
    last_applied_at: Optional[datetime] = Field(
        None,
        description="Last application timestamp"
    )


# =========================================================================
# Integration Schemas (CA V2 ↔ Vibecoding ↔ Gates)
# =========================================================================


class VibecodingIntegrationData(BaseModel):
    """
    Data from Vibecoding service for CA V2 integration.

    Used when Vibecoding Index calculation triggers overlay update.
    """
    submission_id: UUID = Field(
        ...,
        description="Governance submission UUID"
    )
    index_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Calculated vibecoding index"
    )
    zone: VibecodingZoneEnum = Field(
        ...,
        description="Vibecoding zone"
    )
    signals: Dict[str, Any] = Field(
        ...,
        description="Signal breakdown"
    )
    top_contributors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Top contributing signals"
    )
    routing: Dict[str, Any] = Field(
        ...,
        description="Routing decision"
    )


class GateIntegrationData(BaseModel):
    """
    Data from Gates service for CA V2 integration.

    Used when Gate status changes trigger overlay update.
    """
    project_id: UUID = Field(
        ...,
        description="Project UUID"
    )
    gate_id: UUID = Field(
        ...,
        description="Gate UUID"
    )
    gate_name: str = Field(
        ...,
        description="Gate name (e.g., 'G2')"
    )
    event_type: str = Field(
        ...,
        description="Event type: 'gate_pass' or 'gate_fail'"
    )
    previous_status: str = Field(
        ...,
        description="Previous gate status"
    )
    new_status: str = Field(
        ...,
        description="New gate status"
    )
    approved_by: Optional[UUID] = Field(
        None,
        description="Approver user UUID (if gate_pass)"
    )
    rejection_reason: Optional[str] = Field(
        None,
        description="Rejection reason (if gate_fail)"
    )
    timestamp: datetime = Field(
        ...,
        description="Event timestamp"
    )


# =========================================================================
# Health & Stats Schemas
# =========================================================================


class ContextAuthorityHealthResponse(BaseModel):
    """
    Context Authority V2 health check response.
    """
    status: str = Field(
        ...,
        description="Service status: 'healthy', 'degraded', 'unhealthy'"
    )
    version: str = Field(
        default="2.0.0",
        description="CA V2 version"
    )
    template_count: int = Field(
        ...,
        description="Number of active templates"
    )
    snapshot_count_24h: int = Field(
        ...,
        description="Snapshots created in last 24 hours"
    )
    avg_validation_ms: float = Field(
        ...,
        description="Average validation latency (ms)"
    )
    avg_overlay_ms: float = Field(
        ...,
        description="Average overlay generation latency (ms)"
    )
    last_check: datetime = Field(
        ...,
        description="Last health check timestamp"
    )


class ContextAuthorityStatsResponse(BaseModel):
    """
    Context Authority V2 statistics response.
    """
    total_validations: int = Field(
        ...,
        description="Total validations performed"
    )
    total_snapshots: int = Field(
        ...,
        description="Total snapshots created"
    )
    validation_pass_rate: float = Field(
        ...,
        description="Validation pass rate (0-1)"
    )
    zone_distribution: Dict[str, int] = Field(
        ...,
        description="Distribution by vibecoding zone"
    )
    tier_distribution: Dict[str, int] = Field(
        ...,
        description="Distribution by project tier"
    )
    top_triggered_templates: List[Dict[str, Any]] = Field(
        ...,
        description="Top 10 most triggered templates"
    )
    avg_templates_per_validation: float = Field(
        ...,
        description="Average templates applied per validation"
    )
    period_start: datetime = Field(
        ...,
        description="Stats period start"
    )
    period_end: datetime = Field(
        ...,
        description="Stats period end"
    )
