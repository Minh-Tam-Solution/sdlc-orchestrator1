"""
=========================================================================
Governance Vibecoding API Routes (Database-Backed)
SDLC Orchestrator - Sprint 118 (Track 2 Implementation)

Version: 1.0.0
Date: January 29, 2026
Status: ACTIVE - Sprint 118 Phase 3
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 + SPEC-0001 Anti-Vibecoding System

Endpoints (5):
- POST /governance/vibecoding/calculate - Calculate Vibecoding Index (DB-backed)
- GET /governance/vibecoding/{submission_id} - Get index history
- POST /governance/vibecoding/route - Progressive routing decision
- GET /governance/vibecoding/signals/{submission_id} - Get 5 signal breakdown
- POST /governance/vibecoding/kill-switch/check - Check kill switch triggers

Zero Mock Policy: Real database queries with SQLAlchemy 2.0
5-Signal Formula: Intent (30%) + Ownership (25%) + Context (20%) + AI Attestation (15%) + Rejection (10%)
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
from app.services.vibecoding_service import VibecodingService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/governance/vibecoding")


# ============================================================================
# Request/Response Models
# ============================================================================


class CalculateIndexRequest(BaseModel):
    """Request model for calculating Vibecoding Index (database-backed)."""

    project_id: UUID = Field(..., description="Project ID")
    submission_id: str = Field(..., description="Submission/PR identifier")
    intent_clarity: int = Field(..., ge=0, le=100, description="Intent clarity score (0-100)")
    code_ownership: int = Field(..., ge=0, le=100, description="Code ownership score (0-100)")
    context_completeness: int = Field(..., ge=0, le=100, description="Context completeness score (0-100)")
    ai_attestation: bool = Field(..., description="Whether AI attestation is present")
    rejection_rate: float = Field(..., ge=0, le=1, description="Historical rejection rate (0-1)")
    evidence: Optional[Dict[str, Any]] = Field(None, description="Supporting evidence")


class SignalBreakdownResponse(BaseModel):
    """Response model for signal breakdown."""

    signal_type: str
    signal_value: int
    signal_weight: float
    weighted_score: float
    description: str


class VibecodingIndexResult(BaseModel):
    """Response model for Vibecoding Index calculation."""

    submission_id: str
    index_score: int = Field(..., ge=0, le=100)
    zone: str = Field(..., description="GREEN, YELLOW, ORANGE, or RED")
    routing_action: str
    requires_human_review: bool
    signals: List[SignalBreakdownResponse]
    evidence: Optional[Dict[str, Any]]
    calculated_at: datetime


class IndexHistoryResponse(BaseModel):
    """Response model for index history."""

    submission_id: str
    history: List[VibecodingIndexResult]
    total_count: int


class RouteRequest(BaseModel):
    """Request model for progressive routing decision."""

    project_id: UUID = Field(..., description="Project ID")
    submission_id: str = Field(..., description="Submission/PR identifier")
    index_score: int = Field(..., ge=0, le=100, description="Pre-calculated index score")


class RouteResponse(BaseModel):
    """Response model for routing decision."""

    submission_id: str
    index_score: int
    zone: str
    routing_action: str
    requires_human_review: bool
    approver_role: Optional[str] = None
    sla_hours: Optional[int] = None
    escalation_path: Optional[List[str]] = None


class SignalsRequest(BaseModel):
    """Request model for getting signal breakdown."""

    project_id: UUID = Field(..., description="Project ID")
    submission_id: str = Field(..., description="Submission/PR identifier")


class SignalsResponse(BaseModel):
    """Response model for signal breakdown."""

    submission_id: str
    signals: List[SignalBreakdownResponse]
    total_weighted_score: float
    index_score: int
    zone: str


class KillSwitchCheckRequest(BaseModel):
    """Request model for kill switch check."""

    project_id: UUID = Field(..., description="Project ID")


class KillSwitchTriggerStatus(BaseModel):
    """Status of a kill switch trigger."""

    trigger_name: str
    threshold: str
    current_value: str
    is_triggered: bool
    severity: str


class KillSwitchCheckResponse(BaseModel):
    """Response model for kill switch check."""

    project_id: UUID
    is_triggered: bool
    active_triggers: List[KillSwitchTriggerStatus]
    recommended_action: str
    checked_at: datetime


class ZoneStatisticsResponse(BaseModel):
    """Response model for zone statistics."""

    project_id: UUID
    period_days: int
    total_submissions: int
    zone_distribution: Dict[str, int]
    zone_percentages: Dict[str, float]
    average_index_score: float
    trend: str  # improving, stable, degrading


# ============================================================================
# Endpoints
# ============================================================================


@router.post(
    "/calculate",
    response_model=VibecodingIndexResult,
    summary="Calculate Vibecoding Index (Database-Backed)",
    description="""
    Calculate and store Vibecoding Index for a code submission.

    **5-Signal Formula (SPEC-0001):**
    - **Intent Clarity** (30%): How well documented is the "why"?
    - **Code Ownership** (25%): Is ownership clearly declared?
    - **Context Completeness** (20%): Are ADRs and context linked?
    - **AI Attestation** (15%): Is AI usage attested?
    - **Historical Rejection Rate** (10%): Past rejection history

    **Index Calculation:**
    index = 100 - (intent*0.30 + ownership*0.25 + context*0.20 + ai*0.15 + rejection*0.10)

    **Zone Routing (Progressive):**
    - GREEN (0-20): AUTO_MERGE
    - YELLOW (20-40): HUMAN_REVIEW
    - ORANGE (40-60): SENIOR_REVIEW
    - RED (60-100): BLOCK

    Results are stored in database for historical analysis.
    """,
)
async def calculate_index(
    request: CalculateIndexRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VibecodingIndexResult:
    """Calculate and store Vibecoding Index."""
    service = VibecodingService(db)

    try:
        result = await service.calculate_index(
            project_id=request.project_id,
            submission_id=request.submission_id,
            intent_clarity=request.intent_clarity,
            code_ownership=request.code_ownership,
            context_completeness=request.context_completeness,
            ai_attestation=request.ai_attestation,
            rejection_rate=request.rejection_rate,
            evidence=request.evidence,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Failed to calculate Vibecoding Index: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Index calculation failed: {str(e)}",
        )

    return VibecodingIndexResult(
        submission_id=request.submission_id,
        index_score=result["index_score"],
        zone=result["zone"],
        routing_action=result["routing_action"],
        requires_human_review=result["requires_human_review"],
        signals=[
            SignalBreakdownResponse(
                signal_type=s["signal_type"],
                signal_value=s["signal_value"],
                signal_weight=s["signal_weight"],
                weighted_score=s["weighted_score"],
                description=s.get("description", ""),
            )
            for s in result["signals"]
        ],
        evidence=result.get("evidence"),
        calculated_at=result["calculated_at"],
    )


@router.get(
    "/{submission_id}",
    response_model=IndexHistoryResponse,
    summary="Get Index History",
    description="""
    Get historical Vibecoding Index calculations for a submission.

    Returns all index calculations with signals breakdown,
    sorted by calculation time (most recent first).
    """,
)
async def get_index_history(
    submission_id: str,
    project_id: UUID = Query(..., description="Project ID"),
    limit: int = Query(10, ge=1, le=100, description="Max results"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> IndexHistoryResponse:
    """Get index calculation history for a submission."""
    service = VibecodingService(db)

    try:
        history = await service.get_index_history(
            project_id=project_id,
            submission_id=submission_id,
            limit=limit,
        )
    except Exception as e:
        logger.error(f"Failed to get index history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get history: {str(e)}",
        )

    return IndexHistoryResponse(
        submission_id=submission_id,
        history=[
            VibecodingIndexResult(
                submission_id=h["submission_id"],
                index_score=h["index_score"],
                zone=h["zone"],
                routing_action=h["routing_action"],
                requires_human_review=h["requires_human_review"],
                signals=h.get("signals", []),
                evidence=h.get("evidence"),
                calculated_at=h["calculated_at"],
            )
            for h in history
        ],
        total_count=len(history),
    )


@router.post(
    "/route",
    response_model=RouteResponse,
    summary="Progressive Routing Decision",
    description="""
    Get routing decision for a given index score.

    **Routing Rules:**
    - GREEN (0-20): AUTO_MERGE - No human review needed
    - YELLOW (20-40): HUMAN_REVIEW - Team lead review
    - ORANGE (40-60): SENIOR_REVIEW - Senior engineer review
    - RED (60-100): BLOCK - Requires remediation

    Returns routing action with SLA and escalation path.
    """,
)
async def get_routing_decision(
    request: RouteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> RouteResponse:
    """Get progressive routing decision."""
    service = VibecodingService(db)

    try:
        result = await service.get_routing_decision(
            project_id=request.project_id,
            submission_id=request.submission_id,
            index_score=request.index_score,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return RouteResponse(
        submission_id=request.submission_id,
        index_score=request.index_score,
        zone=result["zone"],
        routing_action=result["routing_action"],
        requires_human_review=result["requires_human_review"],
        approver_role=result.get("approver_role"),
        sla_hours=result.get("sla_hours"),
        escalation_path=result.get("escalation_path"),
    )


@router.get(
    "/signals/{submission_id}",
    response_model=SignalsResponse,
    summary="Get Signal Breakdown",
    description="""
    Get detailed breakdown of 5 signals for a submission.

    Returns each signal with:
    - Signal type and value
    - Weight in formula
    - Weighted contribution to final score
    """,
)
async def get_signal_breakdown(
    submission_id: str,
    project_id: UUID = Query(..., description="Project ID"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SignalsResponse:
    """Get signal breakdown for a submission."""
    service = VibecodingService(db)

    try:
        result = await service.get_signal_breakdown(
            project_id=project_id,
            submission_id=submission_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return SignalsResponse(
        submission_id=submission_id,
        signals=[
            SignalBreakdownResponse(
                signal_type=s["signal_type"],
                signal_value=s["signal_value"],
                signal_weight=s["signal_weight"],
                weighted_score=s["weighted_score"],
                description=s.get("description", ""),
            )
            for s in result["signals"]
        ],
        total_weighted_score=result["total_weighted_score"],
        index_score=result["index_score"],
        zone=result["zone"],
    )


@router.post(
    "/kill-switch/check",
    response_model=KillSwitchCheckResponse,
    summary="Check Kill Switch Triggers",
    description="""
    Check if any kill switch triggers are active for a project.

    **Kill Switch Triggers (SPEC-0001):**
    1. **Rejection Rate >80%** (30min window) - Governance too strict
    2. **API Latency >500ms** (15min window) - Performance degradation
    3. **Critical CVEs >=5** (immediate) - Security emergency

    If triggered, returns recommended action (WARNING or FULL rollback).
    """,
)
async def check_kill_switch(
    request: KillSwitchCheckRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> KillSwitchCheckResponse:
    """Check kill switch triggers for a project."""
    service = VibecodingService(db)

    try:
        result = await service.check_kill_switch_status(
            project_id=request.project_id,
        )
    except Exception as e:
        logger.error(f"Failed to check kill switch: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Kill switch check failed: {str(e)}",
        )

    return KillSwitchCheckResponse(
        project_id=request.project_id,
        is_triggered=result["is_triggered"],
        active_triggers=[
            KillSwitchTriggerStatus(
                trigger_name=t["trigger_name"],
                threshold=t["threshold"],
                current_value=t["current_value"],
                is_triggered=t["is_triggered"],
                severity=t["severity"],
            )
            for t in result["triggers"]
        ],
        recommended_action=result["recommended_action"],
        checked_at=result["checked_at"],
    )


@router.get(
    "/stats/{project_id}",
    response_model=ZoneStatisticsResponse,
    summary="Get Zone Statistics",
    description="""
    Get aggregate zone statistics for a project.

    Returns:
    - Zone distribution (count per zone)
    - Zone percentages
    - Average index score
    - Trend analysis (improving/stable/degrading)
    """,
)
async def get_zone_statistics(
    project_id: UUID,
    days: int = Query(7, ge=1, le=90, description="Period in days"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ZoneStatisticsResponse:
    """Get zone statistics for a project."""
    service = VibecodingService(db)

    try:
        result = await service.get_zone_statistics(
            project_id=project_id,
            days=days,
        )
    except Exception as e:
        logger.error(f"Failed to get zone statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Statistics query failed: {str(e)}",
        )

    return ZoneStatisticsResponse(
        project_id=project_id,
        period_days=days,
        total_submissions=result["total_submissions"],
        zone_distribution=result["zone_distribution"],
        zone_percentages=result["zone_percentages"],
        average_index_score=result["average_index_score"],
        trend=result["trend"],
    )


@router.get(
    "/health",
    summary="Vibecoding service health check",
    description="Check health of the vibecoding governance service.",
)
async def vibecoding_health() -> Dict[str, Any]:
    """Health check for vibecoding service."""
    return {
        "status": "healthy",
        "service": "governance_vibecoding",
        "spec": "SPEC-0001",
        "signals": 5,
        "zones": ["GREEN", "YELLOW", "ORANGE", "RED"],
        "timestamp": datetime.utcnow().isoformat(),
    }
