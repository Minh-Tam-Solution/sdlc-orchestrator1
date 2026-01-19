"""
Pilot Tracking API Routes - Sprint 49.

Endpoints for pilot program management, TTFV tracking, and satisfaction surveys.

SDLC Stage: 04 - BUILD
Sprint: 49 - EP-06 Pilot Execution + Metrics Hardening
Framework: SDLC 5.1.3

Endpoints:
- POST /pilot/participants - Register participant
- GET /pilot/participants - List participants
- GET /pilot/participants/{id} - Get participant details
- POST /pilot/sessions - Start session (TTFV timer)
- PATCH /pilot/sessions/{id}/stage - Update session stage
- POST /pilot/sessions/{id}/generation - Record generation result
- POST /pilot/feedback - Submit satisfaction survey
- GET /pilot/metrics/summary - Get pilot summary (CEO dashboard)
- GET /pilot/metrics/daily - Get daily metrics
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.pilot_tracking import (
    PilotStatus,
    PilotDomain,
    OnboardingStage,
)
from app.services.pilot_tracking_service import (
    PilotTrackingService,
    get_pilot_tracking_service,
    TTFV_TARGET_SECONDS,
    SATISFACTION_TARGET,
    QUALITY_GATE_PASS_TARGET,
    PILOT_TARGET_COUNT,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/pilot", tags=["pilot"])


# =============================================================================
# Schemas
# =============================================================================


class ParticipantCreate(BaseModel):
    """Schema for registering a pilot participant."""

    domain: Optional[str] = Field(None, description="Business domain: fnb, hospitality, retail")
    company_name: Optional[str] = Field(None, max_length=255)
    company_size: Optional[str] = Field(None, description="micro, small, medium")
    referral_source: Optional[str] = Field(None, max_length=100)


class ParticipantResponse(BaseModel):
    """Schema for participant response."""

    id: UUID
    user_id: UUID
    status: str
    domain: Optional[str]
    company_name: Optional[str]
    company_size: Optional[str]
    registered_at: Optional[datetime]
    activated_at: Optional[datetime]
    total_sessions: int
    total_generations: int
    successful_generations: int
    best_ttfv_seconds: Optional[int]
    avg_ttfv_seconds: Optional[int]
    latest_satisfaction_score: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class SessionStart(BaseModel):
    """Schema for starting a pilot session."""

    onboarding_session_id: Optional[str] = Field(None, description="Links to OnboardingSession")


class SessionResponse(BaseModel):
    """Schema for session response."""

    id: UUID
    participant_id: UUID
    onboarding_session_id: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]
    current_stage: str
    ttfv_seconds: Optional[int]
    ttfv_target_met: Optional[bool]
    domain: Optional[str]
    app_name: Optional[str]
    generation_provider: Optional[str]
    generation_time_ms: Optional[int]
    quality_gate_passed: Optional[bool]
    quality_gate_score: Optional[float]
    error_count: int

    class Config:
        from_attributes = True


class StageUpdate(BaseModel):
    """Schema for updating session stage."""

    stage: str = Field(..., description="New stage name")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Stage-specific data")
    domain: Optional[str] = Field(None, description="Selected domain")
    app_name: Optional[str] = Field(None, description="App name")
    selected_features: Optional[List[str]] = Field(None, description="Selected features")
    scale: Optional[str] = Field(None, description="Business scale")


class GenerationResult(BaseModel):
    """Schema for recording generation results."""

    provider: str = Field(..., description="AI provider used")
    generation_time_ms: int = Field(..., ge=0)
    tokens_used: int = Field(..., ge=0)
    files_generated: int = Field(..., ge=0)
    lines_of_code: int = Field(..., ge=0)
    quality_gate_passed: bool
    quality_gate_score: Optional[float] = Field(None, ge=0, le=100)
    quality_gate_details: Optional[Dict[str, Any]] = None


class SatisfactionSurvey(BaseModel):
    """Schema for satisfaction survey submission."""

    session_id: Optional[UUID] = None
    overall_score: int = Field(..., ge=1, le=10, description="Overall satisfaction 1-10")
    would_recommend: Optional[bool] = None
    ease_of_use_score: Optional[int] = Field(None, ge=1, le=10)
    code_quality_score: Optional[int] = Field(None, ge=1, le=10)
    speed_score: Optional[int] = Field(None, ge=1, le=10)
    what_went_well: Optional[str] = Field(None, max_length=2000)
    what_needs_improvement: Optional[str] = Field(None, max_length=2000)
    feature_requests: Optional[str] = Field(None, max_length=2000)
    bugs_reported: Optional[str] = Field(None, max_length=2000)


class SurveyResponse(BaseModel):
    """Schema for survey response."""

    id: UUID
    participant_id: UUID
    session_id: Optional[UUID]
    overall_score: int
    would_recommend: Optional[bool]
    submitted_at: datetime

    class Config:
        from_attributes = True


class PilotMetricsSummary(BaseModel):
    """Schema for pilot metrics summary."""

    summary: Dict[str, Any]
    ttfv: Dict[str, Any]
    quality: Dict[str, Any]
    satisfaction: Dict[str, Any]
    domains: Dict[str, int]
    overall_status: str
    generated_at: str


# =============================================================================
# Participant Endpoints
# =============================================================================


@router.post(
    "/participants",
    response_model=ParticipantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register as pilot participant",
)
async def register_participant(
    data: ParticipantCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ParticipantResponse:
    """
    Register current user as a pilot participant.

    Validates domain if provided and creates participant record.
    """
    service = get_pilot_tracking_service(db)

    # Validate domain
    if data.domain and data.domain not in [d.value for d in PilotDomain]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid domain. Must be one of: {[d.value for d in PilotDomain]}",
        )

    participant = await service.register_participant(
        user_id=current_user.id,
        domain=data.domain,
        company_name=data.company_name,
        company_size=data.company_size,
        referral_source=data.referral_source,
    )

    logger.info(f"User {current_user.id} registered as pilot participant {participant.id}")
    return participant


@router.get(
    "/participants",
    response_model=List[ParticipantResponse],
    summary="List pilot participants",
)
async def list_participants(
    status_filter: Optional[str] = Query(None, alias="status"),
    domain: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ParticipantResponse]:
    """
    List pilot participants.

    Requires admin role for full access.
    """
    service = get_pilot_tracking_service(db)

    status_enum = None
    domain_enum = None

    if status_filter:
        try:
            status_enum = PilotStatus(status_filter)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {[s.value for s in PilotStatus]}",
            )

    if domain:
        try:
            domain_enum = PilotDomain(domain)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid domain. Must be one of: {[d.value for d in PilotDomain]}",
            )

    participants = await service.list_participants(
        status=status_enum,
        domain=domain_enum,
        limit=limit,
    )

    return participants


@router.get(
    "/participants/me",
    response_model=ParticipantResponse,
    summary="Get current user's participant profile",
)
async def get_my_participant_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ParticipantResponse:
    """Get pilot participant profile for current user."""
    service = get_pilot_tracking_service(db)

    participant = await service.get_participant(current_user.id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not registered as pilot participant",
        )

    return participant


@router.get(
    "/participants/{participant_id}",
    response_model=ParticipantResponse,
    summary="Get participant by ID",
)
async def get_participant(
    participant_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ParticipantResponse:
    """Get pilot participant details by ID."""
    service = get_pilot_tracking_service(db)

    participant = await service.get_participant_by_id(participant_id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found",
        )

    return participant


# =============================================================================
# Session Endpoints (TTFV Tracking)
# =============================================================================


@router.post(
    "/sessions",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start pilot session (TTFV timer begins)",
)
async def start_session(
    data: SessionStart,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SessionResponse:
    """
    Start a new pilot session.

    This marks the beginning of the TTFV timer.
    """
    service = get_pilot_tracking_service(db)

    # Get participant
    participant = await service.get_participant(current_user.id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not registered as pilot participant. Register first.",
        )

    session = await service.start_session(
        participant_id=participant.id,
        onboarding_session_id=data.onboarding_session_id,
    )

    logger.info(f"Started pilot session {session.id} for participant {participant.id}")
    return session


@router.patch(
    "/sessions/{session_id}/stage",
    response_model=SessionResponse,
    summary="Update session stage",
)
async def update_session_stage(
    session_id: UUID,
    data: StageUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SessionResponse:
    """
    Update session to a new stage.

    Valid stages: started, domain_selected, app_named, features_selected,
    scale_selected, blueprint_generated, code_generating, code_generated,
    quality_gate_passed, deployed, completed
    """
    service = get_pilot_tracking_service(db)

    # Validate stage
    try:
        stage = OnboardingStage(data.stage)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stage. Must be one of: {[s.value for s in OnboardingStage]}",
        )

    session = await service.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    # Update stage
    updated = await service.update_session_stage(
        session_id=session_id,
        stage=stage,
        metadata=data.metadata,
        domain=data.domain,
        app_name=data.app_name,
        selected_features=data.selected_features,
        scale=data.scale,
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    return updated


@router.post(
    "/sessions/{session_id}/generation",
    response_model=SessionResponse,
    summary="Record generation results",
)
async def record_generation(
    session_id: UUID,
    data: GenerationResult,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SessionResponse:
    """
    Record code generation results for a session.

    If quality_gate_passed is True, TTFV will be calculated.
    """
    service = get_pilot_tracking_service(db)

    session = await service.record_generation_result(
        session_id=session_id,
        provider=data.provider,
        generation_time_ms=data.generation_time_ms,
        tokens_used=data.tokens_used,
        files_generated=data.files_generated,
        lines_of_code=data.lines_of_code,
        quality_gate_passed=data.quality_gate_passed,
        quality_gate_score=data.quality_gate_score,
        quality_gate_details=data.quality_gate_details,
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    return session


@router.get(
    "/sessions/{session_id}",
    response_model=SessionResponse,
    summary="Get session details",
)
async def get_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SessionResponse:
    """Get pilot session details."""
    service = get_pilot_tracking_service(db)

    session = await service.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    return session


@router.get(
    "/sessions",
    response_model=List[SessionResponse],
    summary="Get my sessions",
)
async def get_my_sessions(
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[SessionResponse]:
    """Get pilot sessions for current user."""
    service = get_pilot_tracking_service(db)

    participant = await service.get_participant(current_user.id)
    if not participant:
        return []

    sessions = await service.get_participant_sessions(participant.id, limit=limit)
    return sessions


# =============================================================================
# Feedback Endpoints
# =============================================================================


@router.post(
    "/feedback",
    response_model=SurveyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit satisfaction survey",
)
async def submit_feedback(
    data: SatisfactionSurvey,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SurveyResponse:
    """
    Submit satisfaction survey.

    Score is 1-10, with 8+ being the target.
    """
    service = get_pilot_tracking_service(db)

    participant = await service.get_participant(current_user.id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not registered as pilot participant",
        )

    survey = await service.submit_satisfaction_survey(
        participant_id=participant.id,
        session_id=data.session_id,
        overall_score=data.overall_score,
        would_recommend=data.would_recommend,
        ease_of_use_score=data.ease_of_use_score,
        code_quality_score=data.code_quality_score,
        speed_score=data.speed_score,
        what_went_well=data.what_went_well,
        what_needs_improvement=data.what_needs_improvement,
        feature_requests=data.feature_requests,
        bugs_reported=data.bugs_reported,
    )

    logger.info(f"Satisfaction survey submitted: {survey.id}, score: {data.overall_score}")
    return survey


# =============================================================================
# Metrics Endpoints (CEO Dashboard)
# =============================================================================


@router.get(
    "/metrics/summary",
    response_model=PilotMetricsSummary,
    summary="Get pilot program summary",
)
async def get_metrics_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PilotMetricsSummary:
    """
    Get overall pilot program metrics for CEO dashboard.

    Includes:
    - Participant progress (target: 10)
    - TTFV metrics (target: <30 min)
    - Quality gate pass rate (target: 95%+)
    - Satisfaction scores (target: 8/10)
    """
    service = get_pilot_tracking_service(db)
    summary = await service.get_pilot_summary()
    return summary


@router.get(
    "/metrics/targets",
    summary="Get Sprint 49 targets",
)
async def get_targets() -> Dict[str, Any]:
    """Get Sprint 49 pilot targets for reference."""
    return {
        "participants": {
            "target": PILOT_TARGET_COUNT,
            "description": "Vietnamese SME founders to recruit",
        },
        "ttfv": {
            "target_seconds": TTFV_TARGET_SECONDS,
            "target_minutes": TTFV_TARGET_SECONDS // 60,
            "description": "Time from idea to working app",
        },
        "satisfaction": {
            "target": SATISFACTION_TARGET,
            "max": 10,
            "description": "Average satisfaction score",
        },
        "quality_gate": {
            "target_percent": QUALITY_GATE_PASS_TARGET * 100,
            "description": "Quality gate pass rate",
        },
        "sprint": "Sprint 49",
        "ceo_approved": "December 23, 2025",
    }


@router.post(
    "/metrics/aggregate",
    summary="Trigger daily metrics aggregation",
)
async def aggregate_metrics(
    date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Trigger daily metrics aggregation.

    Defaults to today if no date provided. Admin only.
    """
    service = get_pilot_tracking_service(db)

    target_date = date or datetime.now(timezone.utc)
    metrics = await service.aggregate_daily_metrics(target_date)

    return {
        "success": True,
        "date": metrics.date.isoformat(),
        "total_sessions": metrics.total_sessions,
        "ttfv_avg_seconds": metrics.ttfv_avg_seconds,
        "quality_gate_pass_rate": metrics.quality_gate_pass_rate,
        "avg_satisfaction_score": metrics.avg_satisfaction_score,
    }
