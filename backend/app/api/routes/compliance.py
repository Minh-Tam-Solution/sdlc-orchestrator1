"""
=========================================================================
Compliance Router - SDLC 4.9.1 Compliance Scanning
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: December 2, 2025
Status: ACTIVE - Sprint 21 Day 1 (Compliance Scanner)
Authority: Backend Lead + CTO Approved
Foundation: Sprint 21 Plan (1,168 lines), ADR-007 Approved
Framework: SDLC 4.9.1 Complete Lifecycle

Purpose:
- Trigger compliance scans (manual or on-demand)
- Get scan results and history
- View violations and warnings
- Track violation resolution

Endpoints:
- POST /compliance/scans - Trigger compliance scan
- GET /compliance/scans/{project_id}/latest - Get latest scan result
- GET /compliance/scans/{project_id}/history - Get scan history
- GET /compliance/violations/{project_id} - Get project violations
- PUT /compliance/violations/{violation_id}/resolve - Resolve violation

Security:
- Authentication required (JWT)
- Project membership required for scan access
- Admin/Owner only for triggering scans

Zero Mock Policy: Production-ready compliance scanning
=========================================================================
"""

import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.compliance_scan import (
    ComplianceScan,
    ComplianceViolation,
    TriggerType,
)
from app.models.project import Project, ProjectMember
from app.models.user import User
from app.services.compliance_scanner import ComplianceScanner
from app.services.ai_recommendation_service import (
    AIRecommendationService,
    create_ai_recommendation_service,
    AIProviderType,
)
from app.services.ollama_service import get_ollama_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/compliance", tags=["Compliance"])


# =========================================================================
# Pydantic Schemas
# =========================================================================


class ViolationSchema(BaseModel):
    """Violation response schema."""

    type: str
    severity: str
    location: Optional[str] = None
    description: str
    recommendation: Optional[str] = None
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True


class ScanResultSchema(BaseModel):
    """Compliance scan result response."""

    id: UUID
    project_id: UUID
    triggered_by: Optional[UUID] = None
    trigger_type: str
    compliance_score: int = Field(ge=0, le=100)
    violations_count: int
    warnings_count: int
    violations: List[ViolationSchema]
    warnings: List[ViolationSchema]
    scanned_at: datetime
    duration_ms: Optional[int] = None
    is_compliant: bool

    class Config:
        from_attributes = True


class ScanHistoryItemSchema(BaseModel):
    """Scan history item (summary)."""

    id: UUID
    compliance_score: int
    violations_count: int
    warnings_count: int
    trigger_type: str
    scanned_at: datetime

    class Config:
        from_attributes = True


class TriggerScanRequest(BaseModel):
    """Request to trigger a compliance scan."""

    include_doc_code_sync: bool = Field(
        default=True,
        description="Include doc-code drift detection (slower but more thorough)",
    )


class TriggerScanResponse(BaseModel):
    """Response after triggering a scan."""

    scan_id: UUID
    message: str
    compliance_score: int
    violations_count: int
    warnings_count: int
    is_compliant: bool
    scanned_at: datetime


class ViolationDetailSchema(BaseModel):
    """Detailed violation for individual tracking."""

    id: UUID
    scan_id: UUID
    project_id: UUID
    violation_type: str
    severity: str
    location: Optional[str] = None
    description: str
    recommendation: Optional[str] = None
    ai_recommendation: Optional[str] = None
    ai_provider: Optional[str] = None
    ai_confidence: Optional[int] = None
    is_resolved: bool
    resolved_by: Optional[UUID] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ResolveViolationRequest(BaseModel):
    """Request to mark a violation as resolved."""

    resolution_notes: Optional[str] = Field(
        None, max_length=2000, description="Notes about how the violation was resolved"
    )


class ResolveViolationResponse(BaseModel):
    """Response after resolving a violation."""

    id: UUID
    is_resolved: bool
    resolved_by: UUID
    resolved_at: datetime
    resolution_notes: Optional[str] = None
    message: str


# =========================================================================
# Helper Functions
# =========================================================================


async def check_project_access(
    project_id: UUID, user: User, db: AsyncSession
) -> Project:
    """
    Check if user has access to the project.

    Args:
        project_id: UUID of the project
        user: Current user
        db: Database session

    Returns:
        Project if access granted

    Raises:
        HTTPException: If project not found or access denied
    """
    # Get project
    result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.deleted_at.is_(None),
        )
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project not found: {project_id}",
        )

    # Check if user is owner
    if project.owner_id == user.id:
        return project

    # Check if user is member
    membership_result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user.id,
        )
    )
    membership = membership_result.scalar_one_or_none()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You are not a member of this project.",
        )

    return project


async def check_admin_access(
    project_id: UUID, user: User, db: AsyncSession
) -> Project:
    """
    Check if user has admin access to the project.

    Args:
        project_id: UUID of the project
        user: Current user
        db: Database session

    Returns:
        Project if admin access granted

    Raises:
        HTTPException: If not admin/owner
    """
    project = await check_project_access(project_id, user, db)

    # Owner always has admin access
    if project.owner_id == user.id:
        return project

    # Check member role
    membership_result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user.id,
        )
    )
    membership = membership_result.scalar_one_or_none()

    if not membership or membership.role not in ("owner", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required to trigger compliance scans.",
        )

    return project


# =========================================================================
# Endpoints
# =========================================================================


@router.post(
    "/scans/{project_id}",
    response_model=TriggerScanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Trigger compliance scan",
    description="Trigger a compliance scan for a project. Only project owners and admins can trigger scans.",
)
async def trigger_scan(
    project_id: UUID,
    request: TriggerScanRequest = TriggerScanRequest(),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> TriggerScanResponse:
    """
    Trigger immediate compliance scan for a project.

    This endpoint:
    1. Validates project access (admin/owner only)
    2. Runs compliance scanner
    3. Stores results in database
    4. Returns scan summary

    Args:
        project_id: UUID of project to scan
        request: Scan configuration options
        current_user: Authenticated user
        db: Database session

    Returns:
        TriggerScanResponse with scan summary
    """
    # Check admin access
    project = await check_admin_access(project_id, current_user, db)

    logger.info(
        f"Triggering compliance scan for project {project_id} by user {current_user.id}"
    )

    # Create scanner and run scan
    scanner = ComplianceScanner(db)

    try:
        result = await scanner.scan_project(
            project_id=project_id,
            triggered_by=current_user.id,
            trigger_type=TriggerType.MANUAL,
            include_doc_code_sync=request.include_doc_code_sync,
        )

        logger.info(
            f"Compliance scan completed for project {project_id}: "
            f"score={result.compliance_score}, violations={result.violations_count}"
        )

        # Send notifications for violations (Sprint 22)
        if result.violations_count > 0:
            try:
                from app.services.notification_service import NotificationService

                notification_service = NotificationService(db)
                await notification_service.send_violation_alert(
                    project=project,
                    violations=result.violations,
                    compliance_score=result.compliance_score,
                    recipients=[current_user],  # Notify the triggering user
                )
                logger.info(f"Violation alert sent for project {project_id}")
            except Exception as notif_error:
                # Don't fail scan due to notification error
                logger.error(f"Failed to send violation notification: {notif_error}")

        # Get the stored scan ID
        latest_scan_result = await db.execute(
            select(ComplianceScan)
            .where(ComplianceScan.project_id == project_id)
            .order_by(desc(ComplianceScan.scanned_at))
            .limit(1)
        )
        latest_scan = latest_scan_result.scalar_one()

        return TriggerScanResponse(
            scan_id=latest_scan.id,
            message="Compliance scan completed successfully",
            compliance_score=result.compliance_score,
            violations_count=result.violations_count,
            warnings_count=result.warnings_count,
            is_compliant=result.is_compliant,
            scanned_at=result.scanned_at,
        )

    except Exception as e:
        logger.error(f"Compliance scan failed for project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Compliance scan failed: {str(e)}",
        )


@router.get(
    "/scans/{project_id}/latest",
    response_model=ScanResultSchema,
    summary="Get latest scan result",
    description="Get the most recent compliance scan result for a project.",
)
async def get_latest_scan(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ScanResultSchema:
    """
    Get the latest compliance scan result for a project.

    Args:
        project_id: UUID of the project
        current_user: Authenticated user
        db: Database session

    Returns:
        Most recent scan result
    """
    # Check project access
    await check_project_access(project_id, current_user, db)

    # Get latest scan
    result = await db.execute(
        select(ComplianceScan)
        .where(ComplianceScan.project_id == project_id)
        .order_by(desc(ComplianceScan.scanned_at))
        .limit(1)
    )
    scan = result.scalar_one_or_none()

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No compliance scans found for this project. Trigger a scan first.",
        )

    # Convert violations/warnings to schema format
    violations = [ViolationSchema(**v) for v in (scan.violations or [])]
    warnings = [ViolationSchema(**w) for w in (scan.warnings or [])]

    return ScanResultSchema(
        id=scan.id,
        project_id=scan.project_id,
        triggered_by=scan.triggered_by,
        trigger_type=scan.trigger_type,
        compliance_score=scan.compliance_score,
        violations_count=scan.violations_count,
        warnings_count=scan.warnings_count,
        violations=violations,
        warnings=warnings,
        scanned_at=scan.scanned_at,
        duration_ms=scan.duration_ms,
        is_compliant=scan.is_compliant,
    )


@router.get(
    "/scans/{project_id}/history",
    response_model=List[ScanHistoryItemSchema],
    summary="Get scan history",
    description="Get compliance scan history for a project.",
)
async def get_scan_history(
    project_id: UUID,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List[ScanHistoryItemSchema]:
    """
    Get historical compliance scan results for a project.

    Args:
        project_id: UUID of the project
        limit: Maximum number of results
        offset: Number of results to skip
        current_user: Authenticated user
        db: Database session

    Returns:
        List of scan history items
    """
    # Check project access
    await check_project_access(project_id, current_user, db)

    # Get scan history
    result = await db.execute(
        select(ComplianceScan)
        .where(ComplianceScan.project_id == project_id)
        .order_by(desc(ComplianceScan.scanned_at))
        .offset(offset)
        .limit(limit)
    )
    scans = result.scalars().all()

    return [
        ScanHistoryItemSchema(
            id=scan.id,
            compliance_score=scan.compliance_score,
            violations_count=scan.violations_count,
            warnings_count=scan.warnings_count,
            trigger_type=scan.trigger_type,
            scanned_at=scan.scanned_at,
        )
        for scan in scans
    ]


@router.get(
    "/violations/{project_id}",
    response_model=List[ViolationDetailSchema],
    summary="Get project violations",
    description="Get all violations for a project, optionally filtered by resolution status.",
)
async def get_project_violations(
    project_id: UUID,
    resolved: Optional[bool] = Query(default=None, description="Filter by resolved status"),
    severity: Optional[str] = Query(default=None, description="Filter by severity"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List[ViolationDetailSchema]:
    """
    Get violations for a project with optional filters.

    Args:
        project_id: UUID of the project
        resolved: Filter by resolution status
        severity: Filter by severity level
        limit: Maximum number of results
        offset: Number of results to skip
        current_user: Authenticated user
        db: Database session

    Returns:
        List of violation details
    """
    # Check project access
    await check_project_access(project_id, current_user, db)

    # Build query
    query = select(ComplianceViolation).where(
        ComplianceViolation.project_id == project_id
    )

    if resolved is not None:
        query = query.where(ComplianceViolation.is_resolved == resolved)

    if severity:
        query = query.where(ComplianceViolation.severity == severity)

    query = query.order_by(desc(ComplianceViolation.created_at)).offset(offset).limit(limit)

    result = await db.execute(query)
    violations = result.scalars().all()

    return [ViolationDetailSchema.model_validate(v) for v in violations]


@router.put(
    "/violations/{violation_id}/resolve",
    response_model=ResolveViolationResponse,
    summary="Resolve violation",
    description="Mark a violation as resolved with optional notes.",
)
async def resolve_violation(
    violation_id: UUID,
    request: ResolveViolationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ResolveViolationResponse:
    """
    Mark a compliance violation as resolved.

    Args:
        violation_id: UUID of the violation
        request: Resolution details
        current_user: Authenticated user
        db: Database session

    Returns:
        Updated violation status
    """
    # Get violation
    result = await db.execute(
        select(ComplianceViolation).where(ComplianceViolation.id == violation_id)
    )
    violation = result.scalar_one_or_none()

    if not violation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Violation not found: {violation_id}",
        )

    # Check project access
    await check_project_access(violation.project_id, current_user, db)

    # Check if already resolved
    if violation.is_resolved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Violation is already resolved.",
        )

    # Mark as resolved
    violation.is_resolved = True
    violation.resolved_by = current_user.id
    violation.resolved_at = datetime.utcnow()
    violation.resolution_notes = request.resolution_notes

    await db.commit()
    await db.refresh(violation)

    logger.info(
        f"Violation {violation_id} resolved by user {current_user.id}"
    )

    return ResolveViolationResponse(
        id=violation.id,
        is_resolved=violation.is_resolved,
        resolved_by=violation.resolved_by,
        resolved_at=violation.resolved_at,
        resolution_notes=violation.resolution_notes,
        message="Violation marked as resolved successfully",
    )


# =========================================================================
# Scan Scheduling Endpoints (Day 2)
# =========================================================================


class ScheduleScanRequest(BaseModel):
    """Request to schedule a background compliance scan."""

    priority: str = Field(
        default="normal",
        description="Job priority: high, normal, low",
    )
    include_doc_code_sync: bool = Field(
        default=True,
        description="Include doc-code drift detection",
    )


class ScheduleScanResponse(BaseModel):
    """Response after scheduling a scan."""

    job_id: str
    status: str
    message: str
    queued_at: str


class ScanJobStatusResponse(BaseModel):
    """Response for scan job status."""

    job_id: str
    project_id: str
    status: str
    queued_at: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[dict] = None
    error: Optional[str] = None


class QueueStatusResponse(BaseModel):
    """Response for queue status."""

    pending: int
    running: int
    completed: int
    failed: int
    total_jobs: int


@router.post(
    "/scans/{project_id}/schedule",
    response_model=ScheduleScanResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Schedule compliance scan",
    description="Schedule a compliance scan to run in background. Returns immediately with job ID.",
)
async def schedule_scan(
    project_id: UUID,
    request: ScheduleScanRequest = ScheduleScanRequest(),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ScheduleScanResponse:
    """
    Schedule a compliance scan for background execution.

    This endpoint returns immediately with a job ID that can be used
    to check the scan status later.

    Args:
        project_id: UUID of project to scan
        request: Scan configuration options
        current_user: Authenticated user
        db: Database session

    Returns:
        ScheduleScanResponse with job ID
    """
    from app.jobs.compliance_scan import schedule_compliance_scan

    # Check admin access
    await check_admin_access(project_id, current_user, db)

    logger.info(
        f"Scheduling compliance scan for project {project_id} by user {current_user.id}"
    )

    # Schedule the scan
    job = await schedule_compliance_scan(
        project_id=project_id,
        triggered_by=current_user.id,
        trigger_type=TriggerType.MANUAL,
        priority=request.priority,
        include_doc_code_sync=request.include_doc_code_sync,
    )

    return ScheduleScanResponse(
        job_id=job["job_id"],
        status=job["status"],
        message=job["message"],
        queued_at=job["queued_at"],
    )


@router.get(
    "/jobs/{job_id}",
    response_model=ScanJobStatusResponse,
    summary="Get scan job status",
    description="Get the status of a scheduled compliance scan job.",
)
async def get_job_status(
    job_id: str,
    current_user: User = Depends(get_current_active_user),
) -> ScanJobStatusResponse:
    """
    Get the status of a compliance scan job.

    Args:
        job_id: UUID of the job
        current_user: Authenticated user

    Returns:
        Job status details
    """
    from app.jobs.compliance_scan import get_scan_job_status

    job = await get_scan_job_status(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan job not found: {job_id}",
        )

    return ScanJobStatusResponse(
        job_id=job["job_id"],
        project_id=job["project_id"],
        status=job["status"],
        queued_at=job.get("queued_at"),
        started_at=job.get("started_at"),
        completed_at=job.get("completed_at"),
        result=job.get("result"),
        error=job.get("error"),
    )


@router.get(
    "/queue/status",
    response_model=QueueStatusResponse,
    summary="Get scan queue status",
    description="Get the current status of the compliance scan queue.",
)
async def get_queue_status_endpoint(
    current_user: User = Depends(get_current_active_user),
) -> QueueStatusResponse:
    """
    Get the current status of the compliance scan queue.

    Args:
        current_user: Authenticated user

    Returns:
        Queue status with pending/running/completed counts
    """
    from app.jobs.compliance_scan import get_queue_status

    status_data = await get_queue_status()

    return QueueStatusResponse(
        pending=status_data["pending"],
        running=status_data["running"],
        completed=status_data["completed"],
        failed=status_data["failed"],
        total_jobs=status_data["total_jobs"],
    )


# =========================================================================
# AI Recommendation Endpoints (Day 3)
# =========================================================================


class AIRecommendationRequest(BaseModel):
    """Request for AI-generated recommendation."""

    violation_type: str = Field(description="Type of violation")
    severity: str = Field(description="Severity level (critical, high, medium, low, info)")
    location: Optional[str] = Field(None, description="File/folder path")
    description: str = Field(description="Violation description")
    context: Optional[dict] = Field(None, description="Additional context")
    force_provider: Optional[str] = Field(
        None, description="Force specific provider: ollama, claude, gpt4, rule_based"
    )


class AIRecommendationResponse(BaseModel):
    """Response with AI-generated recommendation."""

    recommendation: str
    provider: str
    model: str
    confidence: int = Field(ge=0, le=100)
    duration_ms: float
    tokens_used: int
    cost_usd: float
    fallback_used: bool
    fallback_reason: Optional[str] = None


class AIBudgetStatusResponse(BaseModel):
    """Response with AI budget status."""

    month: str
    total_spent: float
    budget: float
    remaining: float
    percentage_used: float
    by_provider: dict
    alerts: List[str]


class AIProvidersStatusResponse(BaseModel):
    """Response with AI providers status."""

    ollama: dict
    claude: dict
    gpt4: dict
    rule_based: dict


class GenerateViolationRecommendationResponse(BaseModel):
    """Response after generating recommendation for a violation."""

    violation_id: UUID
    ai_recommendation: str
    ai_provider: str
    ai_confidence: int
    message: str


@router.post(
    "/ai/recommendations",
    response_model=AIRecommendationResponse,
    summary="Generate AI recommendation",
    description="Generate an AI recommendation for a compliance violation using the fallback chain.",
)
async def generate_ai_recommendation(
    request: AIRecommendationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> AIRecommendationResponse:
    """
    Generate AI recommendation for a compliance violation.

    Uses fallback chain: Ollama → Claude → GPT-4 → Rule-based

    Args:
        request: Recommendation request details
        current_user: Authenticated user
        db: Database session

    Returns:
        AI-generated recommendation with metadata
    """
    logger.info(
        f"Generating AI recommendation for {request.violation_type} by user {current_user.id}"
    )

    # Parse force_provider if provided
    force_provider = None
    if request.force_provider:
        try:
            force_provider = AIProviderType(request.force_provider)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid provider: {request.force_provider}. "
                f"Valid options: ollama, claude, gpt4, rule_based",
            )

    # Create service and generate recommendation
    service = create_ai_recommendation_service(db)

    try:
        result = await service.generate_recommendation(
            violation_type=request.violation_type,
            severity=request.severity,
            location=request.location or "unknown",
            description=request.description,
            context=request.context,
            user_id=current_user.id,
            force_provider=force_provider,
        )

        return AIRecommendationResponse(
            recommendation=result.recommendation,
            provider=result.provider,
            model=result.model,
            confidence=result.confidence,
            duration_ms=result.duration_ms,
            tokens_used=result.tokens_used,
            cost_usd=result.cost_usd,
            fallback_used=result.fallback_used,
            fallback_reason=result.fallback_reason,
        )

    except Exception as e:
        logger.error(f"AI recommendation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate AI recommendation: {str(e)}",
        )


@router.post(
    "/violations/{violation_id}/ai-recommendation",
    response_model=GenerateViolationRecommendationResponse,
    summary="Generate recommendation for violation",
    description="Generate and store AI recommendation for a specific violation.",
)
async def generate_violation_recommendation(
    violation_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> GenerateViolationRecommendationResponse:
    """
    Generate AI recommendation and update a specific violation.

    Args:
        violation_id: UUID of the violation
        current_user: Authenticated user
        db: Database session

    Returns:
        Updated violation with AI recommendation
    """
    # Get violation
    result = await db.execute(
        select(ComplianceViolation).where(ComplianceViolation.id == violation_id)
    )
    violation = result.scalar_one_or_none()

    if not violation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Violation not found: {violation_id}",
        )

    # Check project access
    await check_project_access(violation.project_id, current_user, db)

    logger.info(
        f"Generating AI recommendation for violation {violation_id} by user {current_user.id}"
    )

    # Create service and generate recommendation
    service = create_ai_recommendation_service(db)

    try:
        updated_violation = await service.update_violation_with_recommendation(
            violation_id=violation_id,
            user_id=current_user.id,
        )

        return GenerateViolationRecommendationResponse(
            violation_id=updated_violation.id,
            ai_recommendation=updated_violation.ai_recommendation or "",
            ai_provider=updated_violation.ai_provider or "",
            ai_confidence=updated_violation.ai_confidence or 0,
            message="AI recommendation generated and stored successfully",
        )

    except Exception as e:
        logger.error(f"Failed to generate recommendation for violation {violation_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate AI recommendation: {str(e)}",
        )


@router.get(
    "/ai/budget",
    response_model=AIBudgetStatusResponse,
    summary="Get AI budget status",
    description="Get current month's AI usage and budget status.",
)
async def get_ai_budget_status(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> AIBudgetStatusResponse:
    """
    Get current month's AI budget status.

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        Budget status with spend breakdown
    """
    service = create_ai_recommendation_service(db)
    budget_status = await service.get_monthly_budget_status()

    return AIBudgetStatusResponse(
        month=budget_status["month"],
        total_spent=budget_status["total_spent"],
        budget=budget_status["budget"],
        remaining=budget_status["remaining"],
        percentage_used=budget_status["percentage_used"],
        by_provider=budget_status["by_provider"],
        alerts=budget_status["alerts"],
    )


@router.get(
    "/ai/providers",
    response_model=AIProvidersStatusResponse,
    summary="Get AI providers status",
    description="Get health status of all AI providers.",
)
async def get_ai_providers_status(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> AIProvidersStatusResponse:
    """
    Get status of all AI providers in the fallback chain.

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        Provider status for ollama, claude, gpt4, rule_based
    """
    service = create_ai_recommendation_service(db)
    providers_status = await service.get_providers_status()

    return AIProvidersStatusResponse(
        ollama=providers_status["ollama"],
        claude=providers_status["claude"],
        gpt4=providers_status["gpt4"],
        rule_based=providers_status["rule_based"],
    )


@router.get(
    "/ai/models",
    summary="List available Ollama models",
    description="Get list of available models in local Ollama instance.",
)
async def list_ollama_models(
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    List available Ollama models.

    Args:
        current_user: Authenticated user

    Returns:
        List of available models
    """
    ollama = get_ollama_service()
    models = ollama.list_models()

    return {
        "models": models,
        "default_model": ollama.model,
        "ollama_url": ollama.base_url,
    }
