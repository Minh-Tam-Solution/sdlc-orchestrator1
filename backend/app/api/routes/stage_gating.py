"""
=========================================================================
Stage Gating API Routes - PR Stage Validation
SDLC Orchestrator - Sprint 109 (Vibecoding Index & Stage-Aware Gating)

Version: 1.0.0
Date: January 27, 2026
Status: ACTIVE - Sprint 109 Day 2
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 Quality Assurance System

Endpoints:
- POST /stage-gating/validate - Validate PR against stage rules
- GET /stage-gating/rules - Get stage rules
- GET /stage-gating/rules/{stage} - Get rules for specific stage
- POST /stage-gating/complete - Mark stage as complete
- POST /stage-gating/advance - Advance project to next stage
- GET /stage-gating/progress/{project_id} - Get stage progress

Zero Mock Policy: Real stage validation
=========================================================================
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.services.governance.stage_gating import (
    PRRequirement,
    Project,
    PullRequest,
    SDLCStage,
    StageGatingResult,
    StageGatingService,
    StageViolation,
    get_stage_gating_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stage-gating")


# ============================================================================
# Request/Response Models
# ============================================================================


class PRValidationRequest(BaseModel):
    """Request model for PR validation."""

    pr_id: int = Field(..., ge=1, description="Pull request ID")
    project_id: UUID = Field(..., description="Project ID")
    changed_files: List[str] = Field(..., min_length=1, description="List of changed file paths")
    title: Optional[str] = Field(None, max_length=255, description="PR title")
    description: Optional[str] = Field(None, max_length=10000, description="PR description")
    linked_task_id: Optional[str] = Field(None, description="Linked task ID")
    author: Optional[str] = Field(None, description="PR author")
    has_intent_statement: bool = Field(False, description="Whether PR has intent statement")
    has_ownership_headers: bool = Field(False, description="Whether files have @owner headers")
    test_coverage: Optional[float] = Field(None, ge=0, le=100, description="Test coverage percentage")
    adr_references: List[str] = Field(default_factory=list, description="Referenced ADRs")
    design_doc_path: Optional[str] = Field(None, description="Path to design document")
    security_scan_passed: bool = Field(False, description="Whether security scan passed")


class ProjectContextRequest(BaseModel):
    """Request model for project context."""

    project_id: UUID = Field(..., description="Project ID")
    name: str = Field(..., description="Project name")
    current_stage: str = Field(..., description="Current SDLC stage")
    completed_stages: List[str] = Field(default_factory=list, description="Completed stages")


class ViolationResponse(BaseModel):
    """Response model for a violation."""

    type: str
    severity: str
    message: str
    file_path: Optional[str]
    current_stage: Optional[str]
    required_stage: Optional[str]
    missing_stage: Optional[str]
    requirement: Optional[str]
    suggestion: Optional[str]
    cli_command: Optional[str]


class ValidationResponse(BaseModel):
    """Response model for PR validation."""

    allowed: bool = Field(..., description="Whether PR is allowed")
    current_stage: str = Field(..., description="Current project stage")
    violations_count: int = Field(..., description="Number of violations")
    warnings_count: int = Field(..., description="Number of warnings")
    violations: List[ViolationResponse]
    warnings: List[ViolationResponse]
    pr_requirements_met: Dict[str, bool]
    suggestion: Optional[str]
    stage_progress: Dict[str, bool]
    validated_at: datetime


class StageRulesResponse(BaseModel):
    """Response model for stage rules."""

    stage: str
    allows: List[str]
    blocks: List[str]
    requires_complete: List[str]
    requires_for_pr: List[str]
    blocks_new_features: bool
    message: str


class AllRulesResponse(BaseModel):
    """Response model for all stage rules."""

    stages: Dict[str, StageRulesResponse]
    stage_order: List[str]


class CompleteStageRequest(BaseModel):
    """Request model for completing a stage."""

    project_id: UUID = Field(..., description="Project ID")
    stage: str = Field(..., description="Stage to mark complete")
    completed_by: str = Field(..., description="User completing the stage")


class CompleteStageResponse(BaseModel):
    """Response model for stage completion."""

    success: bool
    project_id: UUID
    stage: str
    completed_by: str
    completed_at: datetime
    message: str


class AdvanceStageRequest(BaseModel):
    """Request model for advancing stage."""

    project_id: UUID = Field(..., description="Project ID")
    advanced_by: str = Field(..., description="User advancing the stage")


class AdvanceStageResponse(BaseModel):
    """Response model for stage advancement."""

    success: bool
    project_id: UUID
    previous_stage: str
    new_stage: Optional[str]
    advanced_by: str
    advanced_at: datetime
    message: str


class StageProgressResponse(BaseModel):
    """Response model for stage progress."""

    project_id: UUID
    current_stage: str
    completed_stages: List[str]
    stage_progress: Dict[str, bool]
    next_stage: Optional[str]
    completion_percentage: float


# ============================================================================
# Endpoints
# ============================================================================


@router.post(
    "/validate",
    response_model=ValidationResponse,
    summary="Validate PR against stage rules",
    description="""
    Validate a pull request against the current project stage rules.

    This endpoint checks:
    - **File patterns**: Are changed files allowed in current stage?
    - **Prerequisites**: Are all prerequisite stages complete?
    - **PR requirements**: Does PR meet stage requirements (task link, tests, etc)?

    **Stage Progression**:
    - Stage 00 (Foundation): Only docs/00-foundation/** allowed
    - Stage 01 (Planning): Docs allowed, no src/backend/frontend
    - Stage 02 (Design): Schema/specs allowed, no implementation
    - Stage 04 (Build): All code allowed with compliance
    - Stage 05 (Test): Bug fixes and tests only
    - Stage 06 (Deploy): Only deployment configs, code freeze
    """,
)
async def validate_pr_against_stage(
    request: PRValidationRequest,
    project_context: ProjectContextRequest,
    service: StageGatingService = Depends(get_stage_gating_service),
) -> ValidationResponse:
    """Validate PR against stage rules."""
    # Convert request to domain objects
    pr = PullRequest(
        pr_id=request.pr_id,
        project_id=request.project_id,
        changed_files=request.changed_files,
        title=request.title,
        description=request.description,
        linked_task_id=request.linked_task_id,
        author=request.author,
        has_intent_statement=request.has_intent_statement,
        has_ownership_headers=request.has_ownership_headers,
        test_coverage=request.test_coverage,
        adr_references=request.adr_references,
        design_doc_path=request.design_doc_path,
        security_scan_passed=request.security_scan_passed,
    )

    try:
        current_stage = SDLCStage(project_context.current_stage)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stage: {project_context.current_stage}",
        )

    completed_stages = []
    for stage_name in project_context.completed_stages:
        try:
            completed_stages.append(SDLCStage(stage_name))
        except ValueError:
            pass

    project = Project(
        project_id=project_context.project_id,
        name=project_context.name,
        current_stage=current_stage,
        completed_stages=completed_stages,
    )

    # Validate
    result = await service.validate_pr_against_stage(pr, project)

    logger.info(
        f"Stage gating validation: PR #{request.pr_id} in {current_stage.value} - "
        f"{'ALLOWED' if result.allowed else 'BLOCKED'} "
        f"({len(result.violations)} violations, {len(result.warnings)} warnings)"
    )

    return ValidationResponse(
        allowed=result.allowed,
        current_stage=result.current_stage.value,
        violations_count=len(result.violations),
        warnings_count=len(result.warnings),
        violations=[
            ViolationResponse(
                type=v.type.value,
                severity=v.severity,
                message=v.message,
                file_path=v.file_path,
                current_stage=v.current_stage,
                required_stage=v.required_stage,
                missing_stage=v.missing_stage,
                requirement=v.requirement,
                suggestion=v.suggestion,
                cli_command=v.cli_command,
            )
            for v in result.violations
        ],
        warnings=[
            ViolationResponse(
                type=v.type.value,
                severity=v.severity,
                message=v.message,
                file_path=v.file_path,
                current_stage=v.current_stage,
                required_stage=v.required_stage,
                missing_stage=v.missing_stage,
                requirement=v.requirement,
                suggestion=v.suggestion,
                cli_command=v.cli_command,
            )
            for v in result.warnings
        ],
        pr_requirements_met=result.pr_requirements_met,
        suggestion=result.suggestion,
        stage_progress=result.stage_progress,
        validated_at=result.validated_at,
    )


@router.get(
    "/rules",
    response_model=AllRulesResponse,
    summary="Get all stage rules",
    description="Get rules for all SDLC stages.",
)
async def get_all_rules(
    service: StageGatingService = Depends(get_stage_gating_service),
) -> AllRulesResponse:
    """Get all stage rules."""
    from app.services.governance.stage_gating import DEFAULT_STAGE_RULES

    stages = {}
    for stage, rules in DEFAULT_STAGE_RULES.items():
        stages[stage.value] = StageRulesResponse(
            stage=rules.stage.value,
            allows=rules.allows,
            blocks=rules.blocks,
            requires_complete=rules.requires_complete,
            requires_for_pr=[r.value for r in rules.requires_for_pr],
            blocks_new_features=rules.blocks_new_features,
            message=rules.message,
        )

    stage_order = [s.value for s in SDLCStage]

    return AllRulesResponse(
        stages=stages,
        stage_order=stage_order,
    )


@router.get(
    "/rules/{stage}",
    response_model=StageRulesResponse,
    summary="Get rules for specific stage",
    description="Get rules for a specific SDLC stage.",
)
async def get_stage_rules(
    stage: str,
    service: StageGatingService = Depends(get_stage_gating_service),
) -> StageRulesResponse:
    """Get rules for a specific stage."""
    from app.services.governance.stage_gating import DEFAULT_STAGE_RULES

    try:
        sdlc_stage = SDLCStage(stage)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stage not found: {stage}",
        )

    rules = DEFAULT_STAGE_RULES.get(sdlc_stage)
    if not rules:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No rules defined for stage: {stage}",
        )

    return StageRulesResponse(
        stage=rules.stage.value,
        allows=rules.allows,
        blocks=rules.blocks,
        requires_complete=rules.requires_complete,
        requires_for_pr=[r.value for r in rules.requires_for_pr],
        blocks_new_features=rules.blocks_new_features,
        message=rules.message,
    )


@router.post(
    "/complete",
    response_model=CompleteStageResponse,
    summary="Mark stage as complete",
    description="Mark a stage as complete for a project.",
)
async def complete_stage(
    request: CompleteStageRequest,
    service: StageGatingService = Depends(get_stage_gating_service),
) -> CompleteStageResponse:
    """Mark stage as complete."""
    try:
        stage = SDLCStage(request.stage)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stage: {request.stage}",
        )

    # TODO: Load project from database
    # For now, create a minimal project object
    project = Project(
        project_id=request.project_id,
        name="",
        current_stage=stage,
        completed_stages=[],
    )

    success = await service.complete_stage(
        project=project,
        stage=stage,
        completed_by=request.completed_by,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot complete stage {request.stage}: prerequisites not met",
        )

    logger.info(
        f"Stage {request.stage} completed for project {request.project_id} "
        f"by {request.completed_by}"
    )

    return CompleteStageResponse(
        success=True,
        project_id=request.project_id,
        stage=request.stage,
        completed_by=request.completed_by,
        completed_at=datetime.utcnow(),
        message=f"Stage {request.stage} marked as complete",
    )


@router.post(
    "/advance",
    response_model=AdvanceStageResponse,
    summary="Advance to next stage",
    description="Advance project to the next SDLC stage.",
)
async def advance_stage(
    request: AdvanceStageRequest,
    service: StageGatingService = Depends(get_stage_gating_service),
) -> AdvanceStageResponse:
    """Advance to next stage."""
    # TODO: Load project from database
    # For now, return a placeholder response
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Stage advancement requires database integration. Use /complete endpoint for now.",
    )


@router.get(
    "/progress/{project_id}",
    response_model=StageProgressResponse,
    summary="Get stage progress",
    description="Get stage progress for a project.",
)
async def get_stage_progress(
    project_id: UUID,
    service: StageGatingService = Depends(get_stage_gating_service),
) -> StageProgressResponse:
    """Get stage progress."""
    # TODO: Load project from database
    # For now, return a placeholder

    # Return a default progress (would be loaded from DB in real implementation)
    all_stages = list(SDLCStage)
    stage_progress = {s.value: False for s in all_stages}

    return StageProgressResponse(
        project_id=project_id,
        current_stage=SDLCStage.STAGE_04_BUILD.value,
        completed_stages=[],
        stage_progress=stage_progress,
        next_stage=SDLCStage.STAGE_05_TEST.value,
        completion_percentage=0.0,
    )


@router.get(
    "/health",
    summary="Stage gating health check",
    description="Check health of stage gating service.",
)
async def stage_gating_health(
    service: StageGatingService = Depends(get_stage_gating_service),
) -> Dict[str, Any]:
    """Health check for stage gating."""
    return {
        "status": "healthy",
        "service": "stage_gating",
        "stages_configured": len(SDLCStage),
        "timestamp": datetime.utcnow().isoformat(),
    }
