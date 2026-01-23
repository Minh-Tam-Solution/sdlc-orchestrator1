"""
=========================================================================
Consultation Request Protocol (CRP) Schemas
SDLC Orchestrator - Sprint 101 (Risk-Based Planning Trigger)

Version: 1.0.0
Date: January 23, 2026
Status: ACTIVE - Sprint 101 Implementation
Authority: Backend Lead + CTO Approved
Reference: docs/04-build/02-Sprint-Plans/SPRINT-101-DESIGN.md
Reference: SDLC 5.2.0 AI Governance - Consultation Request Protocol

Purpose:
- Define schemas for CRP (Consultation Request Protocol)
- Enable human oversight for high-risk AI-proposed changes
- Track consultation history and resolution

CRP Workflow:
1. AI proposes high-risk change (risk_score > 70)
2. CRP created automatically
3. Reviewer assigned (based on risk factor expertise)
4. Human reviews, comments, approves/rejects
5. Resolution tracked in Evidence Vault

Zero Mock Policy: Production-ready Pydantic v2 models
=========================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.risk_analysis import RiskAnalysis


# =========================================================================
# Enums
# =========================================================================


class ConsultationStatus(str, Enum):
    """Status of consultation request."""

    PENDING = "pending"  # Awaiting reviewer assignment or action
    IN_REVIEW = "in_review"  # Reviewer assigned and reviewing
    APPROVED = "approved"  # Human approved the change
    REJECTED = "rejected"  # Human rejected the change
    CANCELLED = "cancelled"  # Request cancelled (e.g., PR closed)
    EXPIRED = "expired"  # Request expired without resolution


class ConsultationPriority(str, Enum):
    """Priority of consultation request."""

    LOW = "low"  # Can wait
    MEDIUM = "medium"  # Normal turnaround
    HIGH = "high"  # Needs quick attention
    URGENT = "urgent"  # Blocking work, immediate attention


class ReviewerExpertise(str, Enum):
    """Expertise required for review."""

    SECURITY = "security"  # Security expertise
    DATABASE = "database"  # Database/schema expertise
    API = "api"  # API design expertise
    ARCHITECTURE = "architecture"  # System architecture expertise
    CONCURRENCY = "concurrency"  # Concurrency/async expertise
    GENERAL = "general"  # General code review


# =========================================================================
# Request Schemas
# =========================================================================


class CreateConsultationRequest(BaseModel):
    """Request to create a new consultation."""

    model_config = ConfigDict(str_strip_whitespace=True)

    project_id: UUID = Field(..., description="Project ID")
    pr_id: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Pull request ID or reference",
    )
    risk_analysis_id: UUID = Field(
        ...,
        description="ID of the risk analysis that triggered CRP",
    )
    title: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Consultation title",
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Detailed description of the change requiring consultation",
    )
    priority: ConsultationPriority = Field(
        default=ConsultationPriority.MEDIUM,
        description="Priority of the consultation",
    )
    required_expertise: list[ReviewerExpertise] = Field(
        default_factory=lambda: [ReviewerExpertise.GENERAL],
        description="Expertise required for review",
    )
    diff_url: Optional[str] = Field(
        default=None,
        max_length=500,
        description="URL to view the diff (GitHub PR URL)",
    )


class AssignReviewerRequest(BaseModel):
    """Request to assign a reviewer to a consultation."""

    reviewer_id: UUID = Field(..., description="User ID of the reviewer")
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Notes about the assignment",
    )


class ResolveConsultationRequest(BaseModel):
    """Request to resolve a consultation."""

    status: ConsultationStatus = Field(
        ...,
        description="Resolution status (approved/rejected/cancelled)",
    )
    resolution_notes: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Notes explaining the resolution",
    )
    conditions: Optional[list[str]] = Field(
        default=None,
        description="Conditions for approval (if approved with conditions)",
    )


class AddCommentRequest(BaseModel):
    """Request to add a comment to a consultation."""

    comment: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Comment text (markdown supported)",
    )
    is_resolution_note: bool = Field(
        default=False,
        description="Whether this is a resolution note (vs. discussion comment)",
    )


# =========================================================================
# Response Schemas
# =========================================================================


class ConsultationCommentResponse(BaseModel):
    """Response for a single comment."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Comment ID")
    consultation_id: UUID = Field(..., description="Parent consultation ID")
    user_id: UUID = Field(..., description="Author user ID")
    user_name: Optional[str] = Field(
        default=None,
        description="Author name (populated from join)",
    )
    comment: str = Field(..., description="Comment text")
    is_resolution_note: bool = Field(
        default=False,
        description="Whether this is a resolution note",
    )
    created_at: datetime = Field(..., description="When comment was created")


class ConsultationResponse(BaseModel):
    """Response for a consultation request."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Consultation ID")
    project_id: UUID = Field(..., description="Project ID")
    pr_id: Optional[str] = Field(default=None, description="Pull request ID")

    # Risk Analysis
    risk_analysis_id: UUID = Field(
        ...,
        description="ID of the triggering risk analysis",
    )
    risk_analysis: Optional[RiskAnalysis] = Field(
        default=None,
        description="Full risk analysis (if populated)",
    )

    # Consultation Details
    title: str = Field(..., description="Consultation title")
    description: str = Field(..., description="Detailed description")
    priority: ConsultationPriority = Field(..., description="Priority level")
    required_expertise: list[ReviewerExpertise] = Field(
        ...,
        description="Required reviewer expertise",
    )
    diff_url: Optional[str] = Field(default=None, description="URL to view diff")

    # Status
    status: ConsultationStatus = Field(..., description="Current status")

    # Participants
    requester_id: UUID = Field(..., description="User who created the request")
    requester_name: Optional[str] = Field(
        default=None,
        description="Requester name (populated from join)",
    )
    assigned_reviewer_id: Optional[UUID] = Field(
        default=None,
        description="Assigned reviewer ID",
    )
    reviewer_name: Optional[str] = Field(
        default=None,
        description="Reviewer name (populated from join)",
    )

    # Resolution
    resolution_notes: Optional[str] = Field(
        default=None,
        description="Notes explaining the resolution",
    )
    conditions: Optional[list[str]] = Field(
        default=None,
        description="Conditions for approval",
    )
    resolved_at: Optional[datetime] = Field(
        default=None,
        description="When consultation was resolved",
    )
    resolved_by_id: Optional[UUID] = Field(
        default=None,
        description="User who resolved the consultation",
    )

    # Timestamps
    created_at: datetime = Field(..., description="When consultation was created")
    updated_at: datetime = Field(..., description="When consultation was last updated")

    # Comments (optional, based on include)
    comments: Optional[list[ConsultationCommentResponse]] = Field(
        default=None,
        description="Comments on this consultation",
    )
    comment_count: int = Field(
        default=0,
        description="Total number of comments",
    )


class ConsultationListResponse(BaseModel):
    """Response for listing consultations."""

    consultations: list[ConsultationResponse] = Field(
        ...,
        description="List of consultations",
    )
    total: int = Field(..., description="Total count (for pagination)")
    page: int = Field(default=1, description="Current page")
    page_size: int = Field(default=20, description="Page size")
    has_more: bool = Field(default=False, description="Whether there are more pages")


# =========================================================================
# Query Schemas
# =========================================================================


class ConsultationFilters(BaseModel):
    """Filters for querying consultations."""

    project_id: Optional[UUID] = Field(
        default=None,
        description="Filter by project",
    )
    status: Optional[ConsultationStatus] = Field(
        default=None,
        description="Filter by status",
    )
    priority: Optional[ConsultationPriority] = Field(
        default=None,
        description="Filter by priority",
    )
    requester_id: Optional[UUID] = Field(
        default=None,
        description="Filter by requester",
    )
    reviewer_id: Optional[UUID] = Field(
        default=None,
        description="Filter by assigned reviewer",
    )
    expertise: Optional[ReviewerExpertise] = Field(
        default=None,
        description="Filter by required expertise",
    )
    search: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Search in title and description",
    )
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Page size")
