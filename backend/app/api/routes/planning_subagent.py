"""
=========================================================================
Planning Sub-agent API Routes - SDLC Orchestrator
Sprint 99: Planning Sub-agent Implementation Part 2

Version: 1.0.0
Date: January 23, 2026
Status: ACTIVE - Sprint 99 Implementation
Authority: Backend Lead + CTO Approved
Reference: ADR-034-Planning-Subagent-Orchestration
Design: Conformance-Check-Service-Design.md

Endpoints:
- POST /plan: Start planning session with sub-agent orchestration
- GET /{id}: Get planning result
- POST /{id}/approve: Approve or reject plan
- POST /conformance: Check PR conformance (for GitHub CI)
- GET /sessions: List active planning sessions

Key Features:
- Agentic grep pattern extraction (>RAG)
- Conformance scoring (0-100)
- Human approval gate
- GitHub Check integration ready

SDLC 5.2.0 Compliance:
- Planning Mode mandatory for >15 LOC changes
- Prevents architectural drift
- Evidence Vault integration ready

Zero Mock Policy: Production-ready FastAPI routes
=========================================================================
"""

import logging
from pathlib import Path
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from pydantic import BaseModel, Field

from app.api.dependencies import get_current_user
from app.schemas.planning_subagent import (
    ConformanceResult,
    PlanningRequest,
    PlanningResult,
    PlanningStatus,
)
from app.services.planning_orchestrator_service import (
    PlanningOrchestratorService,
    create_planning_orchestrator_service,
)
from app.services.conformance_check_service import (
    ConformanceCheckService,
    create_conformance_check_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/planning/subagent", tags=["Planning Sub-agent"])


# =============================================================================
# Dependency Injection
# =============================================================================


def get_planning_orchestrator() -> PlanningOrchestratorService:
    """Get planning orchestrator service instance."""
    return create_planning_orchestrator_service()


def get_conformance_service() -> ConformanceCheckService:
    """Get conformance check service instance."""
    return create_conformance_check_service()


# =============================================================================
# Request/Response Models
# =============================================================================


class PlanRequestBody(BaseModel):
    """Request body for creating a planning session."""

    task: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Task description for planning",
        examples=["Add OAuth2 authentication with Google provider"],
    )
    project_path: str = Field(
        default=".",
        description="Project root path",
    )
    depth: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Search depth for pattern extraction (1=quick, 5=thorough)",
    )
    include_tests: bool = Field(
        default=True,
        description="Include test pattern analysis",
    )
    include_adrs: bool = Field(
        default=True,
        description="Include ADR analysis",
    )
    auto_approve: bool = Field(
        default=False,
        description="Auto-approve plan without human review",
    )


class PlanApprovalRequest(BaseModel):
    """Request body for approving/rejecting a plan."""

    approved: bool = Field(
        ...,
        description="True to approve, False to reject",
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional notes (required for rejection)",
    )


class ConformanceCheckRequest(BaseModel):
    """Request body for checking PR conformance."""

    diff_content: str = Field(
        ...,
        min_length=1,
        description="Unified diff content from PR",
    )
    project_path: str = Field(
        default=".",
        description="Project root path for pattern extraction",
    )


class PlanningSessionSummary(BaseModel):
    """Summary of a planning session for listing."""

    id: UUID
    task: str
    status: PlanningStatus
    conformance_score: int
    created_at: str
    requires_approval: bool


class PlanningSessionListResponse(BaseModel):
    """Response for listing planning sessions."""

    sessions: list[PlanningSessionSummary]
    total: int


# =============================================================================
# API Endpoints
# =============================================================================


@router.post(
    "/plan",
    response_model=PlanningResult,
    status_code=status.HTTP_201_CREATED,
    summary="Start planning session",
    description="""
    Start a new planning session with sub-agent orchestration.

    This endpoint:
    1. Spawns 3-5 explore sub-agents (parallel)
    2. Extracts patterns from codebase, ADRs, tests
    3. Synthesizes implementation plan
    4. Calculates conformance score (0-100)
    5. Returns plan for human approval

    **Planning Mode is MANDATORY for changes >15 LOC** (SDLC 5.2.0)

    Performance: Typical response in <60s (p95)
    """,
)
async def create_planning_session(
    body: PlanRequestBody,
    background_tasks: BackgroundTasks,
    orchestrator: PlanningOrchestratorService = Depends(get_planning_orchestrator),
    current_user: dict = Depends(get_current_user),
) -> PlanningResult:
    """
    Create a new planning session with sub-agent orchestration.

    Args:
        body: Planning request parameters
        orchestrator: Planning orchestrator service
        current_user: Authenticated user

    Returns:
        PlanningResult with patterns, plan, and conformance score

    Raises:
        HTTPException 400: Invalid request (e.g., task too short)
        HTTPException 404: Project path not found
        HTTPException 500: Planning failed
    """
    logger.info(f"Starting planning session for user {current_user.get('sub')}: {body.task[:50]}...")

    try:
        # Validate project path
        project_path = Path(body.project_path).resolve()
        if not project_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project path not found: {body.project_path}",
            )

        # Create planning request
        request = PlanningRequest(
            task=body.task,
            project_path=str(project_path),
            depth=body.depth,
            include_tests=body.include_tests,
            include_adrs=body.include_adrs,
            auto_approve=body.auto_approve,
        )

        # Execute planning
        result = await orchestrator.plan(request)

        logger.info(
            f"Planning session {result.id} created. "
            f"Patterns: {result.patterns.total_patterns_found}, "
            f"Conformance: {result.conformance.score}%"
        )

        return result

    except ValueError as e:
        logger.warning(f"Invalid planning request: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Planning failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Planning failed: {str(e)}",
        )


@router.get(
    "/{planning_id}",
    response_model=PlanningResult,
    summary="Get planning result",
    description="Retrieve a planning session by ID.",
)
async def get_planning_session(
    planning_id: UUID,
    orchestrator: PlanningOrchestratorService = Depends(get_planning_orchestrator),
    current_user: dict = Depends(get_current_user),
) -> PlanningResult:
    """
    Get a planning session by ID.

    Args:
        planning_id: Planning session UUID
        orchestrator: Planning orchestrator service
        current_user: Authenticated user

    Returns:
        PlanningResult

    Raises:
        HTTPException 404: Planning session not found
    """
    result = orchestrator.get_session(planning_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Planning session not found: {planning_id}",
        )

    return result


@router.post(
    "/{planning_id}/approve",
    response_model=PlanningResult,
    summary="Approve or reject plan",
    description="""
    Approve or reject a planning session.

    **Human oversight is required** for plan approval (SDLC 5.2.0).
    AI agents cannot approve plans - only SE4H (human coach) can.

    On approval:
    - Plan status changes to APPROVED
    - Implementation can proceed

    On rejection:
    - Plan status changes to REJECTED
    - Notes explain required changes
    """,
)
async def approve_planning_session(
    planning_id: UUID,
    body: PlanApprovalRequest,
    orchestrator: PlanningOrchestratorService = Depends(get_planning_orchestrator),
    current_user: dict = Depends(get_current_user),
) -> PlanningResult:
    """
    Approve or reject a planning session.

    Args:
        planning_id: Planning session UUID
        body: Approval request with approved flag and notes
        orchestrator: Planning orchestrator service
        current_user: Authenticated user

    Returns:
        Updated PlanningResult

    Raises:
        HTTPException 400: Rejection requires notes
        HTTPException 404: Planning session not found
    """
    # Validate rejection requires notes
    if not body.approved and not body.notes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rejection requires notes explaining required changes",
        )

    try:
        # Get user ID for audit
        user_id = current_user.get("sub")
        approver_uuid = None
        if user_id:
            try:
                approver_uuid = UUID(user_id)
            except ValueError:
                pass

        result = await orchestrator.approve_plan(
            planning_id=planning_id,
            approved=body.approved,
            notes=body.notes,
            approved_by=approver_uuid,
        )

        action = "approved" if body.approved else "rejected"
        logger.info(f"Planning session {planning_id} {action} by {user_id}")

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/conformance",
    response_model=ConformanceResult,
    summary="Check PR conformance",
    description="""
    Check PR diff conformance against established patterns.

    This endpoint is designed for **GitHub CI integration**:
    1. Receives PR diff content
    2. Extracts patterns from codebase
    3. Analyzes diff for pattern violations
    4. Returns conformance score (0-100)

    **Score Levels**:
    - EXCELLENT (≥90): Auto-approve eligible
    - GOOD (≥70): Review recommended
    - FAIR (≥50): Review required
    - POOR (<50): Changes required

    Use in GitHub Actions:
    ```yaml
    - name: Check Conformance
      run: |
        curl -X POST .../conformance \\
          -d '{"diff_content": "...", "project_path": "."}' \\
          | jq '.score >= 70'
    ```
    """,
)
async def check_conformance(
    body: ConformanceCheckRequest,
    conformance_service: ConformanceCheckService = Depends(get_conformance_service),
    current_user: dict = Depends(get_current_user),
) -> ConformanceResult:
    """
    Check PR diff conformance against established patterns.

    Args:
        body: Conformance check request with diff content
        conformance_service: Conformance check service
        current_user: Authenticated user

    Returns:
        ConformanceResult with score, level, and deviations

    Raises:
        HTTPException 400: Invalid diff content
        HTTPException 404: Project path not found
    """
    logger.info(f"Checking conformance for user {current_user.get('sub')}")

    try:
        project_path = Path(body.project_path).resolve()
        if not project_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project path not found: {body.project_path}",
            )

        result = await conformance_service.check_pr_diff(
            diff_content=body.diff_content,
            project_path=project_path,
        )

        logger.info(
            f"Conformance check complete: score={result.score}, level={result.level.value}"
        )

        return result

    except Exception as e:
        logger.error(f"Conformance check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Conformance check failed: {str(e)}",
        )


@router.get(
    "/sessions",
    response_model=PlanningSessionListResponse,
    summary="List planning sessions",
    description="List all active planning sessions for the current user.",
)
async def list_planning_sessions(
    status_filter: Optional[PlanningStatus] = Query(
        default=None,
        description="Filter by status",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of sessions to return",
    ),
    orchestrator: PlanningOrchestratorService = Depends(get_planning_orchestrator),
    current_user: dict = Depends(get_current_user),
) -> PlanningSessionListResponse:
    """
    List active planning sessions.

    Args:
        status_filter: Optional status filter
        limit: Maximum sessions to return
        orchestrator: Planning orchestrator service
        current_user: Authenticated user

    Returns:
        List of planning session summaries
    """
    sessions = orchestrator.list_sessions()

    # Filter by status if provided
    if status_filter:
        sessions = [s for s in sessions if s.status == status_filter]

    # Apply limit
    sessions = sessions[:limit]

    # Convert to summaries
    summaries = [
        PlanningSessionSummary(
            id=s.id,
            task=s.task[:100] + "..." if len(s.task) > 100 else s.task,
            status=s.status,
            conformance_score=s.conformance.score if s.conformance else 0,
            created_at=s.approved_at.isoformat() if s.approved_at else "",
            requires_approval=s.requires_approval,
        )
        for s in sessions
    ]

    return PlanningSessionListResponse(
        sessions=summaries,
        total=len(summaries),
    )


# =============================================================================
# Health Check
# =============================================================================


@router.get(
    "/health",
    summary="Health check",
    description="Check planning sub-agent service health.",
)
async def health_check() -> dict:
    """
    Health check endpoint for planning sub-agent.

    Returns:
        Health status dict
    """
    return {
        "status": "healthy",
        "service": "planning-subagent",
        "version": "1.0.0",
    }
