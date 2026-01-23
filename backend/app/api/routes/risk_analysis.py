"""
=========================================================================
Risk Analysis API Routes - Risk-Based Planning Trigger
SDLC Orchestrator - Sprint 101 (Risk-Based Planning Trigger)

Version: 1.0.0
Date: January 23, 2026
Status: ACTIVE - Sprint 101 Implementation
Authority: Backend Lead + CTO Approved
Reference: docs/04-build/02-Sprint-Plans/SPRINT-101-DESIGN.md
Reference: SDLC 5.2.0 Planning Mode Principle (7 Mandatory Risk Factors)

Endpoints:
- POST /risk/analyze: Full risk analysis of a diff
- GET /risk/should-plan: Quick check if planning is needed
- GET /risk/factors: List 7 mandatory risk factors

Key Features:
- 7 mandatory risk factor detection (SDLC 5.2.0)
- Risk score calculation (0-100)
- Planning trigger decision (not_required/recommended/required/requires_crp)
- LOC analysis with multiplier

Performance Targets:
- /analyze: <2s (p95)
- /should-plan: <1s (p95)

Zero Mock Policy: Production-ready FastAPI routes
=========================================================================
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.api.dependencies import get_current_user
from app.schemas.risk_analysis import (
    PlanningDecision,
    RiskAnalysis,
    RiskAnalysisRequest,
    RiskFactor,
    RiskLevel,
    ShouldPlanResponse,
)
from app.services.risk_factor_detector_service import RiskFactorDetectorService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/risk", tags=["Risk Analysis"])


# =============================================================================
# Dependency Injection
# =============================================================================


def get_risk_detector() -> RiskFactorDetectorService:
    """Get risk factor detector service instance."""
    return RiskFactorDetectorService()


# =============================================================================
# Request/Response Models
# =============================================================================


class AnalyzeRequestBody(BaseModel):
    """Request body for risk analysis."""

    diff: str = Field(
        ...,
        min_length=1,
        max_length=500000,  # 500KB max
        description="Git diff or PR diff content to analyze",
    )
    context: Optional[dict] = Field(
        default=None,
        description="Additional context (project_id, file_types, etc.)",
    )
    project_id: Optional[UUID] = Field(
        default=None,
        description="Project ID for project-specific thresholds",
    )


class RiskFactorInfo(BaseModel):
    """Information about a single risk factor."""

    factor: RiskFactor
    name: str
    description: str
    examples: list[str]
    severity: str


# =============================================================================
# Endpoints
# =============================================================================


@router.post(
    "/analyze",
    response_model=RiskAnalysis,
    status_code=status.HTTP_200_OK,
    summary="Analyze diff for risk factors",
    description="Perform full risk analysis on a git diff. Detects 7 mandatory risk factors and calculates risk score.",
)
async def analyze_diff(
    body: AnalyzeRequestBody,
    detector: RiskFactorDetectorService = Depends(get_risk_detector),
    current_user=Depends(get_current_user),
) -> RiskAnalysis:
    """
    Analyze a diff for 7 mandatory risk factors.

    Returns full RiskAnalysis with:
    - Detected risk factors with evidence
    - Risk score (0-100)
    - LOC analysis
    - Planning decision recommendation
    - Actionable recommendations
    """
    logger.info(f"Risk analysis requested by user {current_user.id}")

    request = RiskAnalysisRequest(
        diff=body.diff,
        context=body.context,
        project_id=body.project_id,
    )

    analysis = await detector.analyze_diff(request)

    logger.info(
        f"Risk analysis complete: score={analysis.risk_score}, "
        f"factors={analysis.risk_factor_count}, "
        f"decision={analysis.planning_decision.value}"
    )

    return analysis


@router.get(
    "/should-plan",
    response_model=ShouldPlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Quick check if planning is needed",
    description="Lightweight check for planning trigger. Use for CI/CD integration.",
)
async def should_plan(
    diff: str = Query(
        ...,
        min_length=1,
        max_length=500000,
        description="Git diff content",
    ),
    project_id: Optional[UUID] = Query(
        default=None,
        description="Project ID for project-specific thresholds",
    ),
    detector: RiskFactorDetectorService = Depends(get_risk_detector),
    current_user=Depends(get_current_user),
) -> ShouldPlanResponse:
    """
    Quick check if planning mode should be triggered.

    Returns:
    - should_plan: Boolean decision
    - reason: Human-readable explanation
    - risk_score: Quick risk assessment
    - planning_decision: Specific recommendation
    """
    response = await detector.should_plan(diff=diff)
    return response


@router.get(
    "/factors",
    response_model=list[RiskFactorInfo],
    status_code=status.HTTP_200_OK,
    summary="List 7 mandatory risk factors",
    description="Get information about the 7 mandatory risk factors from SDLC 5.2.0.",
)
async def list_risk_factors() -> list[RiskFactorInfo]:
    """
    List the 7 mandatory risk factors.

    These factors are defined in SDLC Framework 5.2.0:
    1. Data schema changes
    2. API contract changes
    3. Authentication/Authorization
    4. Cross-service boundaries
    5. Concurrency/race conditions
    6. Security-sensitive code
    7. Public API interfaces
    """
    return [
        RiskFactorInfo(
            factor=RiskFactor.DATA_SCHEMA,
            name="Data Schema Changes",
            description="Migrations, model changes, database schema modifications",
            examples=[
                "Alembic migration files",
                "SQLAlchemy model changes",
                "CREATE TABLE / ALTER TABLE statements",
            ],
            severity="high",
        ),
        RiskFactorInfo(
            factor=RiskFactor.API_CONTRACT,
            name="API Contract Changes",
            description="API route changes, breaking changes, endpoint modifications",
            examples=[
                "FastAPI route decorators",
                "Request/Response schema changes",
                "OpenAPI specification updates",
            ],
            severity="high",
        ),
        RiskFactorInfo(
            factor=RiskFactor.AUTH,
            name="Authentication / Authorization",
            description="Auth flow changes, RBAC, permissions, tokens",
            examples=[
                "JWT token handling",
                "OAuth2 configuration",
                "Password hashing changes",
                "Role/permission checks",
            ],
            severity="critical",
        ),
        RiskFactorInfo(
            factor=RiskFactor.CROSS_SERVICE,
            name="Cross-Service Boundaries",
            description="Inter-service communication, messaging, external API calls",
            examples=[
                "HTTP client calls to other services",
                "Message queue integration",
                "gRPC/Protobuf changes",
            ],
            severity="high",
        ),
        RiskFactorInfo(
            factor=RiskFactor.CONCURRENCY,
            name="Concurrency / Race Conditions",
            description="Async patterns, threading, locks, parallel processing",
            examples=[
                "asyncio.gather usage",
                "Threading/multiprocessing",
                "Database locking (SELECT FOR UPDATE)",
            ],
            severity="high",
        ),
        RiskFactorInfo(
            factor=RiskFactor.SECURITY,
            name="Security-Sensitive Code",
            description="Payment, PII, encryption, secrets handling",
            examples=[
                "Payment processing (Stripe, PayPal)",
                "Personal data handling (GDPR)",
                "Encryption/decryption",
                "Secret management",
            ],
            severity="critical",
        ),
        RiskFactorInfo(
            factor=RiskFactor.PUBLIC_API,
            name="Public API Interfaces",
            description="External-facing APIs, SDKs, webhooks",
            examples=[
                "Public endpoint additions",
                "SDK interface changes",
                "Webhook payload modifications",
                "API versioning changes",
            ],
            severity="high",
        ),
    ]


@router.get(
    "/levels",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get risk level thresholds",
    description="Get risk score thresholds for each risk level.",
)
async def get_risk_levels() -> dict:
    """
    Get risk level thresholds and their meanings.

    Used by UI to display risk level indicators.
    """
    return {
        "levels": [
            {
                "level": RiskLevel.MINIMAL.value,
                "score_range": "0-20",
                "planning_required": False,
                "description": "No significant risk factors. Planning optional.",
            },
            {
                "level": RiskLevel.LOW.value,
                "score_range": "21-40",
                "planning_required": False,
                "description": "Minor risk factors. Planning recommended.",
            },
            {
                "level": RiskLevel.MEDIUM.value,
                "score_range": "41-60",
                "planning_required": True,
                "description": "Moderate risk factors. Planning strongly recommended.",
            },
            {
                "level": RiskLevel.HIGH.value,
                "score_range": "61-80",
                "planning_required": True,
                "description": "High risk factors. Planning required.",
            },
            {
                "level": RiskLevel.CRITICAL.value,
                "score_range": "81-100",
                "planning_required": True,
                "description": "Critical risk factors. Planning + CRP required.",
            },
        ],
        "thresholds": {
            "planning_recommended": 20,
            "planning_required": 50,
            "crp_required": 70,
        },
        "loc_thresholds": {
            "optimal": 60,
            "large": 150,
            "very_large": 300,
        },
    }
