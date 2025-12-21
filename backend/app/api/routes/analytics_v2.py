"""
Analytics API Routes - Sprint 41 (Mixpanel + PostgreSQL Dual Approach)

SDLC Stage: 04 - BUILD
Sprint: 41 - AI Safety Foundation
Epic: EP-01/EP-02
Status: IMPLEMENTED
Framework: SDLC 5.1.1

Purpose:
Product analytics endpoints for event tracking and metrics reporting.
Implements dual approach per ADR-021 (PostgreSQL + Mixpanel).

Endpoints:
1. POST /analytics/v2/events - Track single event
2. POST /analytics/v2/events/batch - Track batch events
3. GET /analytics/v2/metrics/dau - Daily Active Users
4. GET /analytics/v2/metrics/ai-safety - AI Safety Layer metrics

CTO Approval: ✅ ADR-021 approved December 21, 2025
"""

from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.analytics import (
    EventCreate,
    EventResponse,
    BatchEventCreate,
    BatchEventResponse,
    DAUMetrics,
    AISafetyMetrics,
)
from app.services.analytics_service import analytics_service


router = APIRouter(prefix="/analytics/v2", tags=["Analytics v2"])


# ============================================================================
# Event Tracking Endpoints
# ============================================================================


@router.post("/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def track_event(
    event: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EventResponse:
    """
    Track a single analytics event.

    Stores event in both PostgreSQL (audit trail) and Mixpanel (analytics UX).

    Request Body:
        {
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "event_name": "gate_passed",
            "properties": {
                "gate_id": "G2",
                "project_id": "proj_123",
                "duration_ms": 1250
            }
        }

    Response:
        {
            "success": true,
            "event_id": "660e8400-e29b-41d4-a716-446655440000",
            "message": null
        }

    Security:
        - User ID is hashed with salt before sending to Mixpanel (GDPR)
        - Original user_id stored in PostgreSQL for audit trail
        - No PII in event properties

    Performance:
        - Async event tracking (non-blocking)
        - Circuit breaker prevents cascading failures
        - Fallback to PostgreSQL-only if Mixpanel is down
    """
    success = await analytics_service.track_event(
        user_id=event.user_id,
        event_name=event.event_name,
        properties=event.properties,
        db=db
    )

    if not success:
        return EventResponse(
            success=False,
            event_id=None,
            message="Event tracking failed (circuit breaker may be open)"
        )

    return EventResponse(
        success=True,
        event_id=None,  # Event ID available from DB query if needed
        message=None
    )


@router.post("/events/batch", response_model=BatchEventResponse, status_code=status.HTTP_201_CREATED)
async def track_batch_events(
    batch: BatchEventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BatchEventResponse:
    """
    Track multiple analytics events in batch.

    Supports up to 100 events per batch for performance optimization.

    Request Body:
        {
            "events": [
                {
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "event_name": "gate_passed",
                    "properties": {"gate_id": "G2"}
                },
                {
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "event_name": "evidence_uploaded",
                    "properties": {"file_size_kb": 1024}
                }
            ]
        }

    Response:
        {
            "success_count": 98,
            "total_count": 100,
            "failed_events": [12, 45]
        }

    Performance:
        - Batch processing (100 events in ~200ms vs 10s sequential)
        - Automatic retry on batch failure
        - Partial success supported (some events may fail)
    """
    success_count = await analytics_service.track_batch_events(
        events=batch.events,
        db=db
    )

    failed_count = len(batch.events) - success_count
    failed_indexes = list(range(success_count, len(batch.events))) if failed_count > 0 else []

    return BatchEventResponse(
        success_count=success_count,
        total_count=len(batch.events),
        failed_events=failed_indexes
    )


# ============================================================================
# Metrics Endpoints
# ============================================================================


@router.get("/metrics/dau", response_model=DAUMetrics)
async def get_daily_active_users(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DAUMetrics:
    """
    Get Daily Active Users (DAU) metrics for the last N days.

    Query Parameters:
        days: Number of days to query (default: 30)

    Response:
        {
            "start_date": "2026-01-01",
            "end_date": "2026-01-30",
            "daily_counts": {
                "2026-01-06": 45,
                "2026-01-07": 52,
                "2026-01-08": 48
            },
            "total_unique_users": 127,
            "avg_dau": 48.3
        }

    Notes:
        - DAU is calculated from user_login events
        - Unique users are counted per day
        - Average DAU is calculated across the period
    """
    if days < 1 or days > 365:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Days must be between 1 and 365"
        )

    daily_counts = await analytics_service.get_daily_active_users(db, days)

    # Calculate metrics
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    total_unique = len(set(daily_counts.values()))
    avg_dau = sum(daily_counts.values()) / len(daily_counts) if daily_counts else 0

    return DAUMetrics(
        start_date=start_date.date().isoformat(),
        end_date=end_date.date().isoformat(),
        daily_counts=daily_counts,
        total_unique_users=total_unique,
        avg_dau=round(avg_dau, 1)
    )


@router.get("/metrics/ai-safety", response_model=AISafetyMetrics)
async def get_ai_safety_metrics(
    days: int = 7,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AISafetyMetrics:
    """
    Get AI Safety Layer aggregate metrics for the last N days.

    Query Parameters:
        days: Number of days to query (default: 7)

    Response:
        {
            "period_days": 7,
            "total_validations": 1234,
            "pass_rate": 0.87,
            "avg_duration_ms": 945.2,
            "top_tools": {
                "claude-code": 450,
                "cursor": 380,
                "copilot": 250,
                "windsurf": 100,
                "continue": 54
            },
            "violations_by_type": {
                "naming_convention": 12,
                "folder_structure": 8,
                "missing_evidence": 5
            }
        }

    Metrics Explained:
        - total_validations: Number of PRs validated by AI Safety Layer
        - pass_rate: Percentage of validations that passed (0.0-1.0)
        - avg_duration_ms: Average validation duration in milliseconds
        - top_tools: AI tools usage count (top 5)
        - violations_by_type: Violation counts by category

    Use Cases:
        - Design Partner feedback (EP-03)
        - AI Safety Layer effectiveness (EP-02)
        - Tool adoption metrics
    """
    if days < 1 or days > 90:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Days must be between 1 and 90"
        )

    metrics = await analytics_service.get_ai_safety_metrics(db, days)

    return AISafetyMetrics(
        period_days=days,
        total_validations=metrics["total_validations"],
        pass_rate=round(metrics["pass_rate"], 2),
        avg_duration_ms=round(metrics["avg_duration_ms"], 1),
        top_tools=metrics["top_tools"],
        violations_by_type=metrics.get("violations_by_type", {})
    )
