"""
=========================================================================
Usage Analytics API Routes V1 - DEPRECATED
SDLC Orchestrator - Sprint 24 Day 4 + Sprint 41 Enhancement

Version: 1.0.0 (DEPRECATED)
Sunset Date: March 6, 2026
Successor: /api/v1/telemetry
Migration Guide: /docs/migration/analytics-v2.md
Sprint: 147 - Spring Cleaning (Deprecation)

⚠️ DEPRECATION NOTICE:
This API is deprecated and will be removed on March 6, 2026.
Please migrate to the new Telemetry API (/api/v1/telemetry).

Endpoints for tracking and reporting user activity:
- Session management (Sprint 24) - Use /telemetry/events
- Event tracking (Sprint 24) - Use /telemetry/events
- Usage analytics (Sprint 24) - Use /telemetry/dashboard
- Pilot metrics (Sprint 24) - Use /telemetry/funnels
- Retention management (Sprint 41)
- Circuit breaker status (Sprint 41)

New Telemetry API Features:
- Activation funnels (Time-to-First-Project, Evidence, Gate)
- Interface breakdown (web, cli, extension, api)
- Measured metrics to replace "82-85% realization" narrative
=========================================================================
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.models.usage_tracking import EventType
from app.services.usage_tracking_service import UsageTrackingService
from app.services.analytics_service import analytics_service  # Sprint 41
from app.tasks.analytics_retention import AnalyticsRetentionTask  # Sprint 41
from app.utils.deprecation import add_deprecation_headers

# ============================================================================
# Deprecation Constants - Sprint 147
# ============================================================================

V1_SUNSET = "2026-03-06"  # 30 days for internal API
V1_SUCCESSOR = "/api/v1/telemetry"
V1_MIGRATION_GUIDE = "/docs/migration/analytics-v2.md"


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics V1 (DEPRECATED)"],
    deprecated=True,
)


# ============================================================================
# Request/Response Models
# ============================================================================


class StartSessionRequest(BaseModel):
    """Request to start a new session."""

    pass  # User agent and IP from request headers


class SessionResponse(BaseModel):
    """Session information response."""

    id: str
    session_token: str
    started_at: datetime
    ended_at: Optional[datetime]
    is_active: bool
    duration_seconds: Optional[int]
    device_type: Optional[str]
    browser: Optional[str]
    os: Optional[str]
    page_views_count: int
    events_count: int


class TrackEventRequest(BaseModel):
    """Request to track an event."""

    event_type: str
    event_name: str
    session_token: Optional[str] = None
    page_url: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    metadata: Optional[dict] = None
    duration_ms: Optional[int] = None


class TrackPageViewRequest(BaseModel):
    """Request to track a page view."""

    page_url: str
    session_token: Optional[str] = None
    referrer_url: Optional[str] = None


class TrackFeatureRequest(BaseModel):
    """Request to track feature usage."""

    feature_name: str
    session_token: Optional[str] = None
    success: bool = True
    duration_ms: Optional[int] = None
    metadata: Optional[dict] = None


class EventResponse(BaseModel):
    """Event tracking response."""

    id: str
    event_type: str
    event_name: str
    timestamp: datetime


class EngagementSummary(BaseModel):
    """Engagement summary response."""

    today_active_users: int
    week_active_users: int
    today_sessions: int
    avg_session_duration_seconds: int
    top_features: list[dict]


class PilotMetricsResponse(BaseModel):
    """Pilot metrics response."""

    date: datetime
    total_users: int
    active_users: int
    total_sessions: int
    avg_session_duration: int
    total_page_views: int
    users_using_gates: int
    users_using_evidence: int
    users_using_compliance: int
    gates_evaluated: int
    evidence_uploaded: int
    compliance_scans: int
    feedback_submitted: int
    bugs_reported: int
    features_requested: int


class UserActivityResponse(BaseModel):
    """User activity response."""

    events: list[dict]
    total_count: int


# ============================================================================
# Session Endpoints
# ============================================================================


@router.post("/sessions/start", response_model=SessionResponse, deprecated=True)
async def start_session(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SessionResponse:
    """
    Start a new user session.

    ⚠️ DEPRECATED: Use POST /telemetry/events with event_name="session_started" instead.
    Sunset: March 6, 2026

    Automatically captures user agent and IP address from request.
    Returns session token for subsequent event tracking.
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/events",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Use Telemetry API for session tracking",
    )

    service = UsageTrackingService(db)

    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None

    session = await service.start_session(
        user_id=current_user.id,
        user_agent=user_agent,
        ip_address=ip_address,
    )

    return SessionResponse(
        id=str(session.id),
        session_token=session.session_token,
        started_at=session.started_at,
        ended_at=session.ended_at,
        is_active=session.is_active,
        duration_seconds=session.duration_seconds,
        device_type=session.device_type,
        browser=session.browser,
        os=session.os,
        page_views_count=session.page_views_count or 0,
        events_count=session.events_count or 0,
    )


@router.post("/sessions/{session_id}/end", response_model=SessionResponse, deprecated=True)
async def end_session(
    session_id: UUID,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SessionResponse:
    """
    End a user session.

    ⚠️ DEPRECATED: Use POST /telemetry/events with event_name="session_ended" instead.
    Sunset: March 6, 2026

    Calculates total session duration and marks session as inactive.
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/events",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Use Telemetry API for session tracking",
    )

    service = UsageTrackingService(db)

    session = await service.end_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found",
        )

    return SessionResponse(
        id=str(session.id),
        session_token=session.session_token,
        started_at=session.started_at,
        ended_at=session.ended_at,
        is_active=session.is_active,
        duration_seconds=session.duration_seconds,
        device_type=session.device_type,
        browser=session.browser,
        os=session.os,
        page_views_count=session.page_views_count or 0,
        events_count=session.events_count or 0,
    )


@router.get("/sessions/active", response_model=Optional[SessionResponse], deprecated=True)
async def get_active_session(
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Optional[SessionResponse]:
    """
    Get the current active session for the authenticated user.

    ⚠️ DEPRECATED: Session management via Telemetry API.
    Sunset: March 6, 2026
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=V1_SUCCESSOR,
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Use Telemetry API for session tracking",
    )

    service = UsageTrackingService(db)

    session = await service.get_active_session(current_user.id)

    if not session:
        return None

    return SessionResponse(
        id=str(session.id),
        session_token=session.session_token,
        started_at=session.started_at,
        ended_at=session.ended_at,
        is_active=session.is_active,
        duration_seconds=session.duration_seconds,
        device_type=session.device_type,
        browser=session.browser,
        os=session.os,
        page_views_count=session.page_views_count or 0,
        events_count=session.events_count or 0,
    )


# ============================================================================
# Event Tracking Endpoints
# ============================================================================


@router.post("/events", response_model=EventResponse, deprecated=True)
async def track_event(
    request: TrackEventRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EventResponse:
    """
    Track a usage event.

    ⚠️ DEPRECATED: Use POST /telemetry/events instead.
    Sunset: March 6, 2026

    Generic event tracking for any type of user activity.
    For specific events, use dedicated endpoints (page views, features).
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/events",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Use Telemetry API with standardized event taxonomy",
    )

    service = UsageTrackingService(db)

    # Get session ID from token if provided
    session_id = None
    if request.session_token:
        session = await service.get_active_session(current_user.id)
        if session and session.session_token == request.session_token:
            session_id = session.id

    resource_id = UUID(request.resource_id) if request.resource_id else None

    event = await service.track_event(
        user_id=current_user.id,
        session_id=session_id,
        event_type=request.event_type,
        event_name=request.event_name,
        page_url=request.page_url,
        resource_type=request.resource_type,
        resource_id=resource_id,
        metadata=request.metadata,
        duration_ms=request.duration_ms,
    )

    return EventResponse(
        id=str(event.id),
        event_type=event.event_type,
        event_name=event.event_name,
        timestamp=event.timestamp,
    )


@router.post("/events/page-view", response_model=EventResponse, deprecated=True)
async def track_page_view(
    request: TrackPageViewRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EventResponse:
    """
    Track a page view event.

    ⚠️ DEPRECATED: Use POST /telemetry/events with event_name="dashboard_page_viewed".
    Sunset: March 6, 2026
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/events",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Use Telemetry API for page view tracking",
    )

    service = UsageTrackingService(db)

    # Get session ID from token if provided
    session_id = None
    if request.session_token:
        session = await service.get_active_session(current_user.id)
        if session and session.session_token == request.session_token:
            session_id = session.id

    event = await service.track_page_view(
        user_id=current_user.id,
        session_id=session_id,
        page_url=request.page_url,
        referrer_url=request.referrer_url,
    )

    return EventResponse(
        id=str(event.id),
        event_type=event.event_type,
        event_name=event.event_name,
        timestamp=event.timestamp,
    )


@router.post("/events/feature", response_model=EventResponse, deprecated=True)
async def track_feature_use(
    request: TrackFeatureRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EventResponse:
    """
    Track feature usage event.

    ⚠️ DEPRECATED: Use POST /telemetry/events with appropriate event_name.
    Sunset: March 6, 2026
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/events",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Use Telemetry API for feature tracking",
    )

    service = UsageTrackingService(db)

    # Get session ID from token if provided
    session_id = None
    if request.session_token:
        session = await service.get_active_session(current_user.id)
        if session and session.session_token == request.session_token:
            session_id = session.id

    event = await service.track_feature_use(
        user_id=current_user.id,
        session_id=session_id,
        feature_name=request.feature_name,
        success=request.success,
        duration_ms=request.duration_ms,
        metadata=request.metadata,
    )

    return EventResponse(
        id=str(event.id),
        event_type=event.event_type,
        event_name=event.event_name,
        timestamp=event.timestamp,
    )


# ============================================================================
# Analytics Endpoints
# ============================================================================


@router.get("/my-activity", response_model=UserActivityResponse, deprecated=True)
async def get_my_activity(
    response: Response,
    days: int = 7,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserActivityResponse:
    """
    Get the current user's recent activity.

    ⚠️ DEPRECATED: Use GET /telemetry/dashboard instead.
    Sunset: March 6, 2026

    Returns events from the last N days (default 7).
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/dashboard",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Use Telemetry dashboard for activity metrics",
    )

    service = UsageTrackingService(db)

    start_date = datetime.utcnow() - timedelta(days=days)

    events = await service.get_user_activity(
        user_id=current_user.id,
        start_date=start_date,
        limit=limit,
    )

    return UserActivityResponse(
        events=[
            {
                "id": str(e.id),
                "event_type": e.event_type,
                "event_name": e.event_name,
                "timestamp": e.timestamp.isoformat(),
                "page_url": e.page_url,
                "resource_type": e.resource_type,
                "resource_id": str(e.resource_id) if e.resource_id else None,
            }
            for e in events
        ],
        total_count=len(events),
    )


@router.get("/engagement", response_model=EngagementSummary, deprecated=True)
async def get_engagement_summary(
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EngagementSummary:
    """
    Get engagement summary for dashboard.

    ⚠️ DEPRECATED: Use GET /telemetry/dashboard instead.
    Sunset: March 6, 2026

    Returns today's and this week's metrics.
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/dashboard",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Use Telemetry dashboard for engagement metrics",
    )

    service = UsageTrackingService(db)

    summary = await service.get_engagement_summary()

    return EngagementSummary(**summary)


@router.get("/features", response_model=dict, deprecated=True)
async def get_feature_usage(
    response: Response,
    days: int = 7,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Get feature usage statistics.

    ⚠️ DEPRECATED: Use GET /telemetry/interfaces for interface breakdown.
    Sunset: March 6, 2026

    Returns aggregated feature usage for the last N days.
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/interfaces",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Use Telemetry interfaces endpoint for usage breakdown",
    )

    service = UsageTrackingService(db)

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    stats = await service.get_feature_usage_stats(start_date, end_date)

    return {
        "period_days": days,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "features": stats,
    }


@router.get("/pilot-metrics", response_model=list[PilotMetricsResponse], deprecated=True)
async def get_pilot_metrics(
    response: Response,
    days: int = 7,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PilotMetricsResponse]:
    """
    Get pilot program metrics for dashboard.

    ⚠️ DEPRECATED: Use GET /telemetry/funnels/{funnel_name} instead.
    Sunset: March 6, 2026

    Returns daily metrics for the last N days.
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/funnels/time_to_first_project",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Use Telemetry funnels for activation metrics",
    )

    service = UsageTrackingService(db)

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    metrics = await service.get_pilot_metrics_range(start_date, end_date)

    return [
        PilotMetricsResponse(
            date=m.date,
            total_users=m.total_users,
            active_users=m.active_users,
            total_sessions=m.total_sessions,
            avg_session_duration=m.avg_session_duration,
            total_page_views=m.total_page_views,
            users_using_gates=m.users_using_gates,
            users_using_evidence=m.users_using_evidence,
            users_using_compliance=m.users_using_compliance,
            gates_evaluated=m.gates_evaluated,
            evidence_uploaded=m.evidence_uploaded,
            compliance_scans=m.compliance_scans,
            feedback_submitted=m.feedback_submitted,
            bugs_reported=m.bugs_reported,
            features_requested=m.features_requested,
        )
        for m in metrics
    ]


@router.post("/pilot-metrics/calculate", deprecated=True)
async def calculate_today_metrics(
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Manually trigger pilot metrics calculation for today.

    ⚠️ DEPRECATED: Telemetry API uses real-time event tracking.
    Sunset: March 6, 2026

    This is typically done by a scheduled job, but can be triggered manually.
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/dashboard",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Telemetry API uses real-time event tracking",
    )

    service = UsageTrackingService(db)

    metrics = await service.calculate_pilot_metrics(datetime.utcnow())

    return {
        "success": True,
        "date": metrics.date.isoformat(),
        "active_users": metrics.active_users,
        "total_sessions": metrics.total_sessions,
        "message": "Pilot metrics calculated successfully",
    }


# ============================================================================
# Sprint 41 - Analytics Retention & Circuit Breaker Endpoints
# CTO Approval Conditions #2 and #3
# ============================================================================


@router.get("/retention/stats", deprecated=True)
async def get_retention_stats(
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Get analytics data retention statistics.

    ⚠️ DEPRECATED: Retention stats will be part of admin telemetry dashboard.
    Sunset: March 6, 2026

    Returns current storage metrics and events older than retention period.

    CTO Condition #3: Monitor retention compliance
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/health",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Retention stats available in admin telemetry dashboard",
    )

    task = AnalyticsRetentionTask()
    stats = await task.get_retention_stats(db)

    return {
        "success": True,
        "stats": stats,
        "retention_policy_days": stats["retention_days"],
    }


@router.post("/retention/cleanup", deprecated=True)
async def run_retention_cleanup(
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Manually trigger analytics retention cleanup.

    ⚠️ DEPRECATED: Retention cleanup will be admin-only in telemetry system.
    Sunset: March 6, 2026

    Deletes events older than retention period (default: 90 days).
    This is typically run by cron job daily at 2:00 AM UTC.

    Requires: Admin role (future enhancement)

    CTO Condition #3: Manual cleanup trigger for testing/emergency
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=V1_SUCCESSOR,
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Retention cleanup available via admin endpoints",
    )

    task = AnalyticsRetentionTask()

    # Get stats before cleanup
    stats_before = await task.get_retention_stats(db)

    # Run cleanup
    result = await task.cleanup_old_events(db)

    # Get stats after cleanup
    stats_after = await task.get_retention_stats(db)

    return {
        "success": result["status"] == "success",
        "cleanup_result": result,
        "stats_before": stats_before,
        "stats_after": stats_after,
    }


@router.get("/circuit-breaker/status", deprecated=True)
async def get_circuit_breaker_status(
    response: Response,
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Get Mixpanel circuit breaker status.

    ⚠️ DEPRECATED: Circuit breaker health available via /telemetry/health.
    Sunset: March 6, 2026

    Returns current circuit state, failure count, and recovery info.

    Circuit States:
    - CLOSED: Normal operation (Mixpanel enabled)
    - OPEN: Too many failures (Mixpanel disabled, PostgreSQL-only)
    - HALF_OPEN: Testing recovery after timeout

    CTO Condition #2: Monitor circuit breaker health
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/health",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Health status available via telemetry health endpoint",
    )

    status = analytics_service.get_circuit_breaker_status()

    return {
        "success": True,
        "circuit_breaker": status,
        "health": "healthy" if status["state"] == "closed" else "degraded",
    }


@router.get("/summary", deprecated=True)
async def get_analytics_summary(
    response: Response,
    period_start: Optional[str] = Query(None, description="Start of period (ISO format)"),
    period_end: Optional[str] = Query(None, description="End of period (ISO format)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Get comprehensive analytics summary for AGENTS.md.

    ⚠️ DEPRECATED: Use GET /telemetry/dashboard for activation metrics.
    Sunset: March 6, 2026

    Sprint 85: Combined metrics endpoint for AGENTS.md analytics dashboard.

    Returns:
        Dictionary with overlay, engagement, gates, security, and agents_md metrics.
    """
    add_deprecation_headers(
        response=response,
        removal_date=V1_SUNSET,
        successor_version=f"{V1_SUCCESSOR}/dashboard",
        migration_guide=V1_MIGRATION_GUIDE,
        reason="Use Telemetry dashboard for comprehensive metrics",
    )

    from sqlalchemy import select, func
    from app.models.project import Project
    from app.models.agents_md import AgentsMdFile

    # Sprint 88: Platform admins CANNOT access customer data
    # Query projects accessible to user
    projects_query = select(Project).where(Project.deleted_at.is_(None))
    is_regular_admin = current_user.is_superuser and not current_user.is_platform_admin
    if not is_regular_admin:
        projects_query = projects_query.where(Project.organization_id == current_user.organization_id)

    projects_result = await db.execute(projects_query)
    all_projects = projects_result.scalars().all()
    total_repos = len(all_projects)

    # Query AGENTS.md files
    agents_md_query = select(AgentsMdFile)
    if not is_regular_admin:
        # Join with projects to filter by organization
        agents_md_query = agents_md_query.join(
            Project, AgentsMdFile.project_id == Project.id
        ).where(Project.organization_id == current_user.organization_id)

    agents_md_result = await db.execute(agents_md_query)
    agents_md_files = agents_md_result.scalars().all()

    # Calculate AGENTS.md metrics
    repos_with_agents_md = len(set(f.project_id for f in agents_md_files))
    valid_files = sum(1 for f in agents_md_files if f.validation_status == "valid")
    invalid_files = sum(1 for f in agents_md_files if f.validation_status == "invalid")
    avg_line_count = (
        sum(f.line_count or 0 for f in agents_md_files) / len(agents_md_files)
        if agents_md_files
        else 0
    )

    return {
        "overlay": {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_hit_rate": 0.0,
            "avg_response_time_ms": 0,
            "p95_response_time_ms": 0,
        },
        "engagement": {
            "total_views": 0,
            "unique_viewers": 0,
            "avg_time_on_page_seconds": 0,
            "regenerations": 0,
            "downloads": 0,
        },
        "gates": {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "pending": 0,
            "pass_rate": 0.0,
            "by_gate_type": {},
        },
        "security": {
            "scans_total": 0,
            "scans_passed": 0,
            "scans_failed": 0,
            "pass_rate": 0.0,
            "vulnerabilities_found": 0,
            "vulnerabilities_by_severity": {},
        },
        "agents_md": {
            "total_repos": total_repos,
            "repos_with_agents_md": repos_with_agents_md,
            "valid_files": valid_files,
            "invalid_files": invalid_files,
            "outdated_files": 0,  # TODO: Implement outdated detection
            "coverage_rate": (repos_with_agents_md / total_repos * 100) if total_repos > 0 else 0.0,
            "avg_line_count": int(avg_line_count),
            "regenerations_this_period": 0,  # TODO: Add period filtering
        },
    }
