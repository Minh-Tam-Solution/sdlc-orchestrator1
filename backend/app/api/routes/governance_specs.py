"""
=========================================================================
Governance Specifications API Routes
SDLC Orchestrator - Sprint 118 (Track 2 Implementation)

Version: 1.0.0
Date: January 29, 2026
Status: ACTIVE - Sprint 118 Phase 3
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 + SPEC-0002 Specification Standard

Endpoints (4):
- POST /governance/specs/validate - Validate YAML frontmatter
- GET /governance/specs/{spec_id} - Retrieve spec metadata
- GET /governance/specs/{spec_id}/requirements - List functional requirements
- GET /governance/specs/{spec_id}/acceptance-criteria - List acceptance criteria

Zero Mock Policy: Real database queries with SQLAlchemy 2.0
=========================================================================
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.services.specification_service import SpecificationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/governance/specs")


# ============================================================================
# Request/Response Models
# ============================================================================


class FrontmatterValidationRequest(BaseModel):
    """Request model for validating YAML frontmatter."""

    content: str = Field(..., description="Full markdown content with YAML frontmatter")
    spec_id: Optional[str] = Field(None, description="Spec ID to validate against (e.g., SPEC-0001)")


class FrontmatterField(BaseModel):
    """Frontmatter field with validation status."""

    name: str
    value: Any
    is_valid: bool
    error: Optional[str] = None


class FrontmatterValidationResponse(BaseModel):
    """Response model for frontmatter validation."""

    is_valid: bool
    spec_version: Optional[str] = None
    status: Optional[str] = None
    tier: Optional[str] = None
    stage: Optional[str] = None
    owner: Optional[str] = None
    fields: List[FrontmatterField]
    errors: List[str]
    warnings: List[str]
    validation_time_ms: float


class SpecVersionResponse(BaseModel):
    """Response model for spec version."""

    id: UUID
    version: str
    content_hash: str
    change_summary: Optional[str]
    created_by: Optional[str]
    created_at: datetime


class SpecMetadataResponse(BaseModel):
    """Response model for specification metadata."""

    id: UUID
    project_id: UUID
    spec_number: str
    title: str
    status: str
    tier: str
    stage: str
    owner: Optional[str]
    current_version: str
    created_at: datetime
    updated_at: datetime
    versions: List[SpecVersionResponse]
    frontmatter: Optional[Dict[str, Any]]


class FunctionalRequirementResponse(BaseModel):
    """Response model for functional requirement."""

    id: UUID
    requirement_id: str
    title: str
    description: str
    priority: str
    tier_applicability: List[str]
    bdd_given: Optional[str]
    bdd_when: Optional[str]
    bdd_then: Optional[str]
    created_at: datetime


class AcceptanceCriterionResponse(BaseModel):
    """Response model for acceptance criterion."""

    id: UUID
    criterion_id: str
    description: str
    verification_method: str
    tier_applicability: List[str]
    is_automated: bool
    automation_tool: Optional[str]
    created_at: datetime


class RequirementsListResponse(BaseModel):
    """Response model for list of requirements."""

    spec_id: UUID
    spec_number: str
    total_count: int
    requirements: List[FunctionalRequirementResponse]


class AcceptanceCriteriaListResponse(BaseModel):
    """Response model for list of acceptance criteria."""

    spec_id: UUID
    spec_number: str
    total_count: int
    criteria: List[AcceptanceCriterionResponse]


# ============================================================================
# Endpoints
# ============================================================================


@router.post(
    "/validate",
    response_model=FrontmatterValidationResponse,
    summary="Validate YAML Frontmatter",
    description="""
    Validate YAML frontmatter against SPEC-0002 Specification Standard.

    **Mandatory Fields:**
    - authors (list of strings)

    **Recommended Fields:**
    - spec_version, status, tier, stage, owner
    - reviewers, stakeholders
    - created, last_updated
    - related_adrs

    **Validation Rules:**
    - YAML must be valid and parseable
    - Required fields must be present
    - Tier must be one of: LITE, STANDARD, PROFESSIONAL, ENTERPRISE
    - Stage must be valid SDLC stage (00-10)
    - Status must be one of: draft, review, approved, deprecated
    """,
)
async def validate_frontmatter(
    request: FrontmatterValidationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FrontmatterValidationResponse:
    """Validate YAML frontmatter for SPEC-0002 compliance."""
    import time

    start_time = time.perf_counter()

    service = SpecificationService(db)

    try:
        result = await service.validate_frontmatter(request.content)
    except Exception as e:
        logger.error(f"Frontmatter validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Frontmatter validation failed: {str(e)}",
        )

    processing_time = (time.perf_counter() - start_time) * 1000

    # Build field responses
    fields = []
    if result.get("parsed_frontmatter"):
        fm = result["parsed_frontmatter"]
        for key, value in fm.items():
            is_valid = key not in [e.split(":")[0] for e in result.get("errors", [])]
            fields.append(FrontmatterField(
                name=key,
                value=value,
                is_valid=is_valid,
                error=None,
            ))

    return FrontmatterValidationResponse(
        is_valid=result["is_valid"],
        spec_version=result.get("parsed_frontmatter", {}).get("spec_version"),
        status=result.get("parsed_frontmatter", {}).get("status"),
        tier=result.get("parsed_frontmatter", {}).get("tier"),
        stage=result.get("parsed_frontmatter", {}).get("stage"),
        owner=result.get("parsed_frontmatter", {}).get("owner"),
        fields=fields,
        errors=result.get("errors", []),
        warnings=result.get("warnings", []),
        validation_time_ms=round(processing_time, 2),
    )


@router.get(
    "/{spec_id}",
    response_model=SpecMetadataResponse,
    summary="Get Specification Metadata",
    description="""
    Retrieve specification metadata by ID.

    Returns:
    - Spec metadata (number, title, status, tier, stage)
    - Version history
    - Frontmatter metadata
    """,
)
async def get_specification(
    spec_id: UUID,
    include_versions: bool = Query(True, description="Include version history"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SpecMetadataResponse:
    """Get specification metadata by ID."""
    service = SpecificationService(db)

    try:
        spec = await service.get_specification(spec_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    # Build version responses
    versions = []
    if include_versions and spec.versions:
        for v in spec.versions:
            versions.append(SpecVersionResponse(
                id=v.id,
                version=v.version,
                content_hash=v.content_hash,
                change_summary=v.change_summary,
                created_by=v.created_by,
                created_at=v.created_at,
            ))

    # Get frontmatter if available
    frontmatter = None
    if spec.frontmatter_metadata:
        fm = spec.frontmatter_metadata
        frontmatter = {
            "spec_version": fm.spec_version,
            "authors": fm.authors,
            "reviewers": fm.reviewers,
            "stakeholders": fm.stakeholders,
            "created": fm.created.isoformat() if fm.created else None,
            "last_updated": fm.last_updated.isoformat() if fm.last_updated else None,
            "related_adrs": fm.related_adrs,
        }

    return SpecMetadataResponse(
        id=spec.id,
        project_id=spec.project_id,
        spec_number=spec.spec_number,
        title=spec.title,
        status=spec.status,
        tier=spec.tier,
        stage=spec.stage,
        owner=spec.owner,
        current_version=spec.current_version,
        created_at=spec.created_at,
        updated_at=spec.updated_at,
        versions=versions,
        frontmatter=frontmatter,
    )


@router.get(
    "/{spec_id}/requirements",
    response_model=RequirementsListResponse,
    summary="List Functional Requirements",
    description="""
    List all functional requirements for a specification.

    Requirements include:
    - Requirement ID (e.g., FR-001)
    - Title and description
    - Priority (MUST, SHOULD, MAY, COULD)
    - Tier applicability
    - BDD format (GIVEN-WHEN-THEN)
    """,
)
async def list_requirements(
    spec_id: UUID,
    tier: Optional[str] = Query(None, description="Filter by tier"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> RequirementsListResponse:
    """List functional requirements for a specification."""
    service = SpecificationService(db)

    # Verify spec exists
    try:
        spec = await service.get_specification(spec_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    # Get requirements
    requirements = await service.get_functional_requirements(
        spec_id=spec_id,
        tier=tier,
        priority=priority,
    )

    return RequirementsListResponse(
        spec_id=spec_id,
        spec_number=spec.spec_number,
        total_count=len(requirements),
        requirements=[
            FunctionalRequirementResponse(
                id=req.id,
                requirement_id=req.requirement_id,
                title=req.title,
                description=req.description,
                priority=req.priority,
                tier_applicability=req.tier_applicability or [],
                bdd_given=req.bdd_given,
                bdd_when=req.bdd_when,
                bdd_then=req.bdd_then,
                created_at=req.created_at,
            )
            for req in requirements
        ],
    )


@router.get(
    "/{spec_id}/acceptance-criteria",
    response_model=AcceptanceCriteriaListResponse,
    summary="List Acceptance Criteria",
    description="""
    List all acceptance criteria for a specification.

    Criteria include:
    - Criterion ID (e.g., AC-001)
    - Description
    - Verification method (automated, manual, hybrid)
    - Tier applicability
    - Automation status and tool
    """,
)
async def list_acceptance_criteria(
    spec_id: UUID,
    tier: Optional[str] = Query(None, description="Filter by tier"),
    automated_only: bool = Query(False, description="Only show automated criteria"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AcceptanceCriteriaListResponse:
    """List acceptance criteria for a specification."""
    service = SpecificationService(db)

    # Verify spec exists
    try:
        spec = await service.get_specification(spec_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    # Get acceptance criteria
    criteria = await service.get_acceptance_criteria(
        spec_id=spec_id,
        tier=tier,
        automated_only=automated_only,
    )

    return AcceptanceCriteriaListResponse(
        spec_id=spec_id,
        spec_number=spec.spec_number,
        total_count=len(criteria),
        criteria=[
            AcceptanceCriterionResponse(
                id=ac.id,
                criterion_id=ac.criterion_id,
                description=ac.description,
                verification_method=ac.verification_method,
                tier_applicability=ac.tier_applicability or [],
                is_automated=ac.is_automated,
                automation_tool=ac.automation_tool,
                created_at=ac.created_at,
            )
            for ac in criteria
        ],
    )


@router.get(
    "/health",
    summary="Specification service health check",
    description="Check health of the specification service.",
)
async def specs_health() -> Dict[str, Any]:
    """Health check for specification service."""
    return {
        "status": "healthy",
        "service": "governance_specs",
        "spec_standard": "SPEC-0002",
        "timestamp": datetime.utcnow().isoformat(),
    }
