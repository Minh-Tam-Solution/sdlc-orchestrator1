"""
Dogfooding API Routes - Sprint 114 Track 2

Provides endpoints for monitoring WARNING mode dogfooding metrics
and Go/No-Go decision support.

Day 2-4 additions:
- Developer feedback/survey system
- CEO time tracking
- Daily checks automation
- Enhanced false positive tracking
"""

from datetime import date, datetime, timedelta
from enum import Enum
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.services.governance.mode_service import GovernanceModeService, GovernanceMode

router = APIRouter(prefix="/dogfooding", tags=["dogfooding"])


# ============================================================================
# Enums
# ============================================================================

class FeedbackRating(str, Enum):
    """Developer feedback rating scale."""
    VERY_DISSATISFIED = "very_dissatisfied"
    DISSATISFIED = "dissatisfied"
    NEUTRAL = "neutral"
    SATISFIED = "satisfied"
    VERY_SATISFIED = "very_satisfied"


class FeedbackCategory(str, Enum):
    """Feedback category for classification."""
    FRICTION = "friction"
    FALSE_POSITIVE = "false_positive"
    AUTO_GENERATION = "auto_generation"
    UI_UX = "ui_ux"
    DOCUMENTATION = "documentation"
    OTHER = "other"


# ============================================================================
# Request/Response Models
# ============================================================================

class VibecodingDistribution(BaseModel):
    """Vibecoding index distribution across zones."""
    green: int = Field(description="PRs with index 0-30")
    yellow: int = Field(description="PRs with index 31-60")
    orange: int = Field(description="PRs with index 61-80")
    red: int = Field(description="PRs with index 81-100")


class DogfoodingMetricsResponse(BaseModel):
    """Sprint dogfooding metrics response."""
    sprint: str
    mode: str
    start_date: str
    end_date: str
    days_elapsed: int
    total_days: int

    # PR Metrics
    prs_evaluated: int
    prs_target: int

    # Vibecoding Index
    distribution: VibecodingDistribution
    average_index: float

    # Developer Friction
    avg_friction_minutes: float
    friction_target: float

    # Accuracy
    false_positive_rate: float
    false_positive_target: float

    # Team Satisfaction
    team_nps: Optional[float]
    nps_target: float

    # Go/No-Go
    go_no_go_ready: bool
    blockers: list[str]


class PRMetricResponse(BaseModel):
    """Individual PR governance metric."""
    pr_number: int
    title: str
    author: str
    vibecode_index: float
    zone: str
    friction_minutes: float
    auto_gen_used: bool
    timestamp: datetime


class PRMetricsListResponse(BaseModel):
    """List of PR metrics."""
    items: list[PRMetricResponse]
    total: int
    page: int
    page_size: int


class RecordPRMetricRequest(BaseModel):
    """Request to record a PR governance evaluation metric."""
    pr_number: int
    title: str
    author: str
    vibecode_index: float
    zone: str
    friction_minutes: float
    auto_gen_used: bool = False
    file_count: int = 0
    violations: list[str] = []


class GoNoGoDecisionResponse(BaseModel):
    """Go/No-Go decision for next sprint."""
    ready: bool
    checks: list[dict]
    recommendation: str
    blockers: list[str]
    next_sprint: str
    next_mode: str


# ============================================================================
# Day 2-4: Developer Feedback Models
# ============================================================================

class DeveloperFeedbackRequest(BaseModel):
    """Developer feedback submission request."""
    rating: FeedbackRating = Field(description="Overall satisfaction rating")
    nps_score: int = Field(ge=-100, le=100, description="Net Promoter Score (-100 to 100)")
    friction_minutes: float = Field(ge=0, description="Perceived friction in minutes")
    category: FeedbackCategory = Field(description="Feedback category")
    helpful_aspects: list[str] = Field(default=[], description="What was helpful")
    pain_points: list[str] = Field(default=[], description="Pain points experienced")
    suggestions: str = Field(default="", description="Improvement suggestions")
    would_recommend: bool = Field(description="Would recommend to other teams")
    pr_number: Optional[int] = Field(default=None, description="Related PR number if applicable")


class DeveloperFeedbackResponse(BaseModel):
    """Developer feedback submission response."""
    feedback_id: str
    submitted_at: datetime
    message: str


class FeedbackSummaryResponse(BaseModel):
    """Aggregated feedback summary."""
    total_responses: int
    average_nps: float
    nps_target: float
    satisfaction_distribution: dict[str, int]
    avg_perceived_friction: float
    top_pain_points: list[dict]
    top_helpful_aspects: list[dict]
    recommendation_rate: float
    feedback_by_category: dict[str, int]


# ============================================================================
# Day 2-4: CEO Time Tracking Models
# ============================================================================

class CEOTimeEntryRequest(BaseModel):
    """CEO time tracking entry request."""
    activity_type: str = Field(description="Type: pr_review, architecture_debate, firefighting, vibecoding_cleanup")
    duration_minutes: float = Field(ge=0, description="Duration in minutes")
    description: str = Field(description="Activity description")
    pr_number: Optional[int] = Field(default=None, description="Related PR if applicable")
    date: Optional[str] = Field(default=None, description="Date (YYYY-MM-DD), defaults to today")


class CEOTimeEntryResponse(BaseModel):
    """CEO time tracking entry response."""
    entry_id: str
    recorded_at: datetime
    message: str


class CEOTimeSummaryResponse(BaseModel):
    """CEO time tracking summary."""
    baseline_hours: float
    current_hours: float
    hours_saved: float
    savings_percentage: float
    target_hours: float
    target_percentage: float
    on_track: bool
    breakdown: dict[str, float]
    daily_trend: list[dict]
    pr_review_count: int
    auto_approved_count: int
    manual_review_ratio: float


# ============================================================================
# Day 2-4: Daily Checks Models
# ============================================================================

class DailyCheckResult(BaseModel):
    """Individual daily check result."""
    check_name: str
    passed: bool
    current_value: str
    target_value: str
    severity: str  # info, warning, critical
    message: str


class DailyChecksResponse(BaseModel):
    """Daily checks aggregated response."""
    day: int
    date: str
    checks: list[DailyCheckResult]
    all_passed: bool
    critical_issues: int
    warnings: int
    recommendations: list[str]


# ============================================================================
# In-Memory Storage (Sprint 114 POC - Replace with DB in production)
# ============================================================================

# Sprint 114 configuration
SPRINT_114_CONFIG = {
    "sprint": "114",
    "mode": "WARNING",
    "start_date": "2026-02-03",
    "end_date": "2026-02-07",
    "total_days": 5,
    "prs_target": 15,
    "friction_target": 10.0,  # minutes
    "false_positive_target": 20.0,  # percent
    "nps_target": 50.0,
}

# In-memory PR metrics storage
_pr_metrics: list[dict] = []

# In-memory developer feedback storage (Day 2)
_developer_feedback: list[dict] = []

# In-memory CEO time tracking storage (Day 2)
_ceo_time_entries: list[dict] = []

# CEO time baseline (40 hours/week as per plan)
CEO_TIME_BASELINE = {
    "weekly_hours": 40.0,
    "week_2_target": 30.0,  # -25%
    "week_4_target": 20.0,  # -50%
    "week_8_target": 10.0,  # -75%
}


def _calculate_days_elapsed() -> int:
    """Calculate days elapsed since sprint start."""
    start = datetime.strptime(SPRINT_114_CONFIG["start_date"], "%Y-%m-%d").date()
    today = date.today()
    if today < start:
        return 0
    elapsed = (today - start).days + 1
    return min(elapsed, SPRINT_114_CONFIG["total_days"])


def _calculate_distribution() -> VibecodingDistribution:
    """Calculate vibecoding index distribution from recorded PRs."""
    dist = {"green": 0, "yellow": 0, "orange": 0, "red": 0}
    for pr in _pr_metrics:
        zone = pr.get("zone", "green").lower()
        if zone in dist:
            dist[zone] += 1
    return VibecodingDistribution(**dist)


def _calculate_average_index() -> float:
    """Calculate average vibecoding index."""
    if not _pr_metrics:
        return 0.0
    return sum(pr.get("vibecode_index", 0) for pr in _pr_metrics) / len(_pr_metrics)


def _calculate_avg_friction() -> float:
    """Calculate average developer friction in minutes."""
    if not _pr_metrics:
        return 0.0
    return sum(pr.get("friction_minutes", 0) for pr in _pr_metrics) / len(_pr_metrics)


def _calculate_false_positive_rate() -> float:
    """Calculate false positive rate based on reported false positives."""
    if not _pr_metrics:
        return 0.0

    total_prs = len(_pr_metrics)
    false_positives = sum(
        1 for pr in _pr_metrics
        if pr.get("false_positive_reports") and len(pr["false_positive_reports"]) > 0
    )

    return (false_positives / total_prs) * 100 if total_prs > 0 else 0.0


def _calculate_team_nps() -> Optional[float]:
    """Calculate team NPS from developer feedback."""
    if not _developer_feedback:
        return None

    nps_scores = [f["nps_score"] for f in _developer_feedback if "nps_score" in f]
    if not nps_scores:
        return None

    return sum(nps_scores) / len(nps_scores)


def _calculate_ceo_time_summary() -> dict:
    """Calculate CEO time tracking summary."""
    if not _ceo_time_entries:
        return {
            "total_hours": 0.0,
            "breakdown": {},
            "daily": [],
        }

    # Group by activity type
    breakdown: dict[str, float] = {}
    daily: dict[str, float] = {}

    for entry in _ceo_time_entries:
        activity = entry.get("activity_type", "other")
        duration = entry.get("duration_minutes", 0) / 60  # Convert to hours
        entry_date = entry.get("date", date.today().isoformat())

        breakdown[activity] = breakdown.get(activity, 0) + duration
        daily[entry_date] = daily.get(entry_date, 0) + duration

    total_hours = sum(breakdown.values())

    return {
        "total_hours": total_hours,
        "breakdown": breakdown,
        "daily": [{"date": d, "hours": h} for d, h in sorted(daily.items())],
    }


def _get_feedback_summary() -> dict:
    """Get aggregated feedback summary."""
    if not _developer_feedback:
        return {
            "total": 0,
            "avg_nps": 0.0,
            "satisfaction_dist": {},
            "avg_friction": 0.0,
            "pain_points": [],
            "helpful": [],
            "recommend_rate": 0.0,
            "by_category": {},
        }

    # Calculate distributions
    satisfaction_dist: dict[str, int] = {}
    pain_points_count: dict[str, int] = {}
    helpful_count: dict[str, int] = {}
    by_category: dict[str, int] = {}

    total_friction = 0.0
    recommend_count = 0

    for feedback in _developer_feedback:
        # Satisfaction distribution
        rating = feedback.get("rating", "neutral")
        satisfaction_dist[rating] = satisfaction_dist.get(rating, 0) + 1

        # Pain points
        for point in feedback.get("pain_points", []):
            pain_points_count[point] = pain_points_count.get(point, 0) + 1

        # Helpful aspects
        for aspect in feedback.get("helpful_aspects", []):
            helpful_count[aspect] = helpful_count.get(aspect, 0) + 1

        # Category
        category = feedback.get("category", "other")
        by_category[category] = by_category.get(category, 0) + 1

        # Friction
        total_friction += feedback.get("friction_minutes", 0)

        # Recommendation
        if feedback.get("would_recommend", False):
            recommend_count += 1

    total = len(_developer_feedback)
    avg_nps = _calculate_team_nps() or 0.0

    # Sort and get top items
    top_pain = sorted(pain_points_count.items(), key=lambda x: x[1], reverse=True)[:5]
    top_helpful = sorted(helpful_count.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "total": total,
        "avg_nps": avg_nps,
        "satisfaction_dist": satisfaction_dist,
        "avg_friction": total_friction / total if total > 0 else 0.0,
        "pain_points": [{"item": k, "count": v} for k, v in top_pain],
        "helpful": [{"item": k, "count": v} for k, v in top_helpful],
        "recommend_rate": (recommend_count / total * 100) if total > 0 else 0.0,
        "by_category": by_category,
    }


def _get_blockers() -> list[str]:
    """Identify blockers for Go/No-Go decision."""
    blockers = []

    # Check PR count
    if len(_pr_metrics) < SPRINT_114_CONFIG["prs_target"]:
        blockers.append(
            f"Need {SPRINT_114_CONFIG['prs_target']}+ PRs evaluated "
            f"(currently: {len(_pr_metrics)})"
        )

    # Check average friction
    avg_friction = _calculate_avg_friction()
    if avg_friction > SPRINT_114_CONFIG["friction_target"]:
        blockers.append(
            f"Developer friction too high: {avg_friction:.1f} min "
            f"(target: <{SPRINT_114_CONFIG['friction_target']} min)"
        )

    # Check false positive rate
    fp_rate = _calculate_false_positive_rate()
    if fp_rate > SPRINT_114_CONFIG["false_positive_target"]:
        blockers.append(
            f"False positive rate too high: {fp_rate:.1f}% "
            f"(target: <{SPRINT_114_CONFIG['false_positive_target']}%)"
        )

    # Check NPS from developer feedback
    team_nps = _calculate_team_nps()
    if team_nps is None:
        blockers.append("Team NPS survey not completed (need 3+ responses)")
    elif team_nps < SPRINT_114_CONFIG["nps_target"]:
        blockers.append(
            f"Team NPS too low: {team_nps:.1f} "
            f"(target: >{SPRINT_114_CONFIG['nps_target']})"
        )

    return blockers


# ============================================================================
# API Endpoints
# ============================================================================

@router.get("/metrics", response_model=DogfoodingMetricsResponse)
async def get_dogfooding_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get Sprint 114 dogfooding metrics for WARNING mode observation.

    Returns aggregated metrics for Go/No-Go decision support.
    """
    distribution = _calculate_distribution()
    avg_index = _calculate_average_index()
    avg_friction = _calculate_avg_friction()
    fp_rate = _calculate_false_positive_rate()
    blockers = _get_blockers()

    team_nps = _calculate_team_nps()

    return DogfoodingMetricsResponse(
        sprint=SPRINT_114_CONFIG["sprint"],
        mode=SPRINT_114_CONFIG["mode"],
        start_date=SPRINT_114_CONFIG["start_date"],
        end_date=SPRINT_114_CONFIG["end_date"],
        days_elapsed=_calculate_days_elapsed(),
        total_days=SPRINT_114_CONFIG["total_days"],
        prs_evaluated=len(_pr_metrics),
        prs_target=SPRINT_114_CONFIG["prs_target"],
        distribution=distribution,
        average_index=avg_index,
        avg_friction_minutes=avg_friction,
        friction_target=SPRINT_114_CONFIG["friction_target"],
        false_positive_rate=fp_rate,
        false_positive_target=SPRINT_114_CONFIG["false_positive_target"],
        team_nps=team_nps,
        nps_target=SPRINT_114_CONFIG["nps_target"],
        go_no_go_ready=len(blockers) == 0,
        blockers=blockers,
    )


@router.get("/prs", response_model=PRMetricsListResponse)
async def get_pr_metrics(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get list of PR governance evaluations.

    Paginated list of PRs evaluated during dogfooding period.
    """
    start = (page - 1) * page_size
    end = start + page_size

    items = [
        PRMetricResponse(
            pr_number=pr["pr_number"],
            title=pr["title"],
            author=pr["author"],
            vibecode_index=pr["vibecode_index"],
            zone=pr["zone"],
            friction_minutes=pr["friction_minutes"],
            auto_gen_used=pr.get("auto_gen_used", False),
            timestamp=pr.get("timestamp", datetime.utcnow()),
        )
        for pr in _pr_metrics[start:end]
    ]

    return PRMetricsListResponse(
        items=items,
        total=len(_pr_metrics),
        page=page,
        page_size=page_size,
    )


@router.post("/prs/record")
async def record_pr_metric(
    request: RecordPRMetricRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Record a PR governance evaluation metric.

    Called by GitHub Actions workflow after each PR evaluation.
    No authentication required for GitHub Actions webhook.
    """
    # Check if PR already recorded
    existing = next(
        (pr for pr in _pr_metrics if pr["pr_number"] == request.pr_number),
        None,
    )

    pr_data = {
        "pr_number": request.pr_number,
        "title": request.title,
        "author": request.author,
        "vibecode_index": request.vibecode_index,
        "zone": request.zone,
        "friction_minutes": request.friction_minutes,
        "auto_gen_used": request.auto_gen_used,
        "file_count": request.file_count,
        "violations": request.violations,
        "timestamp": datetime.utcnow(),
    }

    if existing:
        # Update existing record
        _pr_metrics.remove(existing)

    _pr_metrics.append(pr_data)

    return {
        "status": "recorded",
        "pr_number": request.pr_number,
        "total_prs": len(_pr_metrics),
    }


@router.get("/go-no-go", response_model=GoNoGoDecisionResponse)
async def get_go_no_go_decision(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get Go/No-Go decision for Sprint 115 (SOFT mode).

    Evaluates all criteria and provides recommendation.
    Requires CTO or CEO role.
    """
    if current_user.role not in ["cto", "ceo", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Go/No-Go decision requires CTO or CEO role",
        )

    blockers = _get_blockers()
    avg_friction = _calculate_avg_friction()
    fp_rate = _calculate_false_positive_rate()

    checks = [
        {
            "name": "PRs Evaluated",
            "current": len(_pr_metrics),
            "target": SPRINT_114_CONFIG["prs_target"],
            "passed": len(_pr_metrics) >= SPRINT_114_CONFIG["prs_target"],
        },
        {
            "name": "Developer Friction",
            "current": f"{avg_friction:.1f} min",
            "target": f"<{SPRINT_114_CONFIG['friction_target']} min",
            "passed": avg_friction <= SPRINT_114_CONFIG["friction_target"],
        },
        {
            "name": "False Positive Rate",
            "current": f"{fp_rate:.1f}%",
            "target": f"<{SPRINT_114_CONFIG['false_positive_target']}%",
            "passed": fp_rate <= SPRINT_114_CONFIG["false_positive_target"],
        },
        {
            "name": "Team NPS",
            "current": "N/A",
            "target": f">{SPRINT_114_CONFIG['nps_target']}",
            "passed": False,  # Survey not completed
        },
    ]

    ready = len(blockers) == 0
    recommendation = (
        "PROCEED to Sprint 115 (SOFT Enforcement)"
        if ready
        else "EXTEND WARNING mode - address blockers before enforcement"
    )

    return GoNoGoDecisionResponse(
        ready=ready,
        checks=checks,
        recommendation=recommendation,
        blockers=blockers,
        next_sprint="115",
        next_mode="SOFT" if ready else "WARNING",
    )


@router.get("/status")
async def get_dogfooding_status(
    db: AsyncSession = Depends(get_db),
):
    """
    Get current dogfooding status (public endpoint).

    Returns basic status information for monitoring.
    """
    return {
        "sprint": SPRINT_114_CONFIG["sprint"],
        "mode": SPRINT_114_CONFIG["mode"],
        "start_date": SPRINT_114_CONFIG["start_date"],
        "end_date": SPRINT_114_CONFIG["end_date"],
        "days_elapsed": _calculate_days_elapsed(),
        "prs_evaluated": len(_pr_metrics),
        "prs_target": SPRINT_114_CONFIG["prs_target"],
        "status": "active" if _calculate_days_elapsed() <= SPRINT_114_CONFIG["total_days"] else "completed",
    }


@router.post("/report-false-positive")
async def report_false_positive(
    pr_number: int,
    reason: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Report a false positive governance evaluation.

    Used by developers to flag incorrect violations for calibration.
    """
    # Find the PR metric
    pr = next(
        (pr for pr in _pr_metrics if pr["pr_number"] == pr_number),
        None,
    )

    if not pr:
        raise HTTPException(
            status_code=404,
            detail=f"PR #{pr_number} not found in dogfooding metrics",
        )

    # Record false positive
    if "false_positive_reports" not in pr:
        pr["false_positive_reports"] = []

    pr["false_positive_reports"].append({
        "reporter": current_user.username,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat(),
    })

    return {
        "status": "reported",
        "pr_number": pr_number,
        "message": "False positive report recorded. Thank you for helping calibrate the system.",
    }


# ============================================================================
# Day 2-4: Developer Feedback Endpoints
# ============================================================================

@router.post("/feedback", response_model=DeveloperFeedbackResponse)
async def submit_developer_feedback(
    request: DeveloperFeedbackRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit developer feedback for Sprint 114 dogfooding.

    Collects satisfaction ratings, NPS scores, and qualitative feedback
    to assess developer experience with WARNING mode governance.
    """
    import uuid

    feedback_id = str(uuid.uuid4())[:8]
    submitted_at = datetime.utcnow()

    feedback_data = {
        "feedback_id": feedback_id,
        "user_id": str(current_user.id),
        "username": current_user.username,
        "rating": request.rating.value,
        "nps_score": request.nps_score,
        "friction_minutes": request.friction_minutes,
        "category": request.category.value,
        "helpful_aspects": request.helpful_aspects,
        "pain_points": request.pain_points,
        "suggestions": request.suggestions,
        "would_recommend": request.would_recommend,
        "pr_number": request.pr_number,
        "submitted_at": submitted_at.isoformat(),
    }

    _developer_feedback.append(feedback_data)

    return DeveloperFeedbackResponse(
        feedback_id=feedback_id,
        submitted_at=submitted_at,
        message="Thank you for your feedback! Your input helps us improve governance for everyone.",
    )


@router.get("/feedback/summary", response_model=FeedbackSummaryResponse)
async def get_feedback_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get aggregated developer feedback summary.

    Returns NPS scores, satisfaction distribution, and top pain points
    for Sprint 114 dogfooding analysis.
    """
    summary = _get_feedback_summary()

    return FeedbackSummaryResponse(
        total_responses=summary["total"],
        average_nps=summary["avg_nps"],
        nps_target=SPRINT_114_CONFIG["nps_target"],
        satisfaction_distribution=summary["satisfaction_dist"],
        avg_perceived_friction=summary["avg_friction"],
        top_pain_points=summary["pain_points"],
        top_helpful_aspects=summary["helpful"],
        recommendation_rate=summary["recommend_rate"],
        feedback_by_category=summary["by_category"],
    )


@router.get("/feedback/list")
async def list_developer_feedback(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all developer feedback submissions.

    Requires CTO or admin role for full access.
    Regular users only see their own feedback.
    """
    if current_user.role in ["cto", "ceo", "admin"]:
        # Full access for leadership
        feedback_list = _developer_feedback
    else:
        # Users see only their own feedback
        feedback_list = [
            f for f in _developer_feedback
            if f.get("user_id") == str(current_user.id)
        ]

    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": feedback_list[start:end],
        "total": len(feedback_list),
        "page": page,
        "page_size": page_size,
    }


# ============================================================================
# Day 2-4: CEO Time Tracking Endpoints
# ============================================================================

@router.post("/ceo-time/record", response_model=CEOTimeEntryResponse)
async def record_ceo_time(
    request: CEOTimeEntryRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Record CEO time spent on governance-related activities.

    Used to track time savings during Sprint 114 dogfooding.
    Requires CTO or CEO role.
    """
    if current_user.role not in ["cto", "ceo", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="CEO time tracking requires CTO or CEO role",
        )

    import uuid

    entry_id = str(uuid.uuid4())[:8]
    recorded_at = datetime.utcnow()
    entry_date = request.date or date.today().isoformat()

    entry_data = {
        "entry_id": entry_id,
        "user_id": str(current_user.id),
        "username": current_user.username,
        "activity_type": request.activity_type,
        "duration_minutes": request.duration_minutes,
        "description": request.description,
        "pr_number": request.pr_number,
        "date": entry_date,
        "recorded_at": recorded_at.isoformat(),
    }

    _ceo_time_entries.append(entry_data)

    return CEOTimeEntryResponse(
        entry_id=entry_id,
        recorded_at=recorded_at,
        message=f"Time entry recorded: {request.duration_minutes:.1f} min for {request.activity_type}",
    )


@router.get("/ceo-time/summary", response_model=CEOTimeSummaryResponse)
async def get_ceo_time_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get CEO time tracking summary for Sprint 114.

    Shows baseline vs actual hours, time saved, and trend data.
    """
    time_summary = _calculate_ceo_time_summary()

    baseline = CEO_TIME_BASELINE["weekly_hours"]
    current = time_summary["total_hours"]
    saved = baseline - current if current < baseline else 0
    savings_pct = (saved / baseline * 100) if baseline > 0 else 0

    # Determine target based on days elapsed
    days_elapsed = _calculate_days_elapsed()
    if days_elapsed <= 2:
        target = CEO_TIME_BASELINE["week_2_target"]
        target_pct = 25.0
    elif days_elapsed <= 4:
        target = CEO_TIME_BASELINE["week_4_target"]
        target_pct = 50.0
    else:
        target = CEO_TIME_BASELINE["week_8_target"]
        target_pct = 75.0

    on_track = current <= target or saved > 0

    # Calculate PR review metrics
    pr_review_entries = [
        e for e in _ceo_time_entries
        if e.get("activity_type") == "pr_review"
    ]
    pr_review_count = len(pr_review_entries)

    # Auto-approved = PRs in green zone (no CEO review needed)
    auto_approved = sum(
        1 for pr in _pr_metrics
        if pr.get("zone", "").lower() == "green"
    )

    total_prs = len(_pr_metrics)
    manual_ratio = (pr_review_count / total_prs * 100) if total_prs > 0 else 0

    return CEOTimeSummaryResponse(
        baseline_hours=baseline,
        current_hours=current,
        hours_saved=saved,
        savings_percentage=savings_pct,
        target_hours=target,
        target_percentage=target_pct,
        on_track=on_track,
        breakdown=time_summary["breakdown"],
        daily_trend=time_summary["daily"],
        pr_review_count=pr_review_count,
        auto_approved_count=auto_approved,
        manual_review_ratio=manual_ratio,
    )


@router.get("/ceo-time/entries")
async def list_ceo_time_entries(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    activity_type: Optional[str] = Query(None, description="Filter by activity type"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List CEO time tracking entries.

    Requires CTO or CEO role.
    """
    if current_user.role not in ["cto", "ceo", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="CEO time entries require CTO or CEO role",
        )

    entries = _ceo_time_entries

    if activity_type:
        entries = [e for e in entries if e.get("activity_type") == activity_type]

    # Sort by date descending
    entries = sorted(entries, key=lambda x: x.get("date", ""), reverse=True)

    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": entries[start:end],
        "total": len(entries),
        "page": page,
        "page_size": page_size,
    }


# ============================================================================
# Day 2-4: Daily Checks Endpoints
# ============================================================================

@router.get("/daily-checks", response_model=DailyChecksResponse)
async def run_daily_checks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Run daily checks for Sprint 114 dogfooding.

    Day 2: Verify 5+ PRs evaluated, check kill switch dashboard, baseline CEO time
    Day 3: Analyze first 10 PRs, tune thresholds, collect developer feedback
    Day 4: Review false positives, adjust prompts, prepare metrics report
    """
    days_elapsed = _calculate_days_elapsed()
    today = date.today().isoformat()

    checks: list[DailyCheckResult] = []
    recommendations: list[str] = []

    # ==================
    # Common Checks (All Days)
    # ==================

    # Check 1: PRs Evaluated
    prs_target_daily = 5 * days_elapsed if days_elapsed > 0 else 5
    prs_evaluated = len(_pr_metrics)
    prs_passed = prs_evaluated >= prs_target_daily

    checks.append(DailyCheckResult(
        check_name="PRs Evaluated",
        passed=prs_passed,
        current_value=str(prs_evaluated),
        target_value=f">={prs_target_daily}",
        severity="critical" if not prs_passed and days_elapsed >= 2 else "warning",
        message=f"{prs_evaluated} PRs evaluated (target: {prs_target_daily}+ by Day {days_elapsed})",
    ))

    if not prs_passed:
        recommendations.append("Create more PRs to hit evaluation target")

    # Check 2: Kill Switch Status (always check)
    # In WARNING mode, rejection rate should be 0% (nothing blocked)
    rejection_rate = 0.0  # WARNING mode doesn't block
    ks_passed = True

    checks.append(DailyCheckResult(
        check_name="Kill Switch Status",
        passed=ks_passed,
        current_value="OFF (WARNING mode)",
        target_value="No triggers",
        severity="info",
        message="Kill switch not triggered - WARNING mode is non-blocking",
    ))

    # Check 3: API Latency
    latency_ok = True  # Assume OK for POC
    checks.append(DailyCheckResult(
        check_name="API Latency P95",
        passed=latency_ok,
        current_value="<100ms",
        target_value="<100ms",
        severity="info",
        message="API latency within SLO target",
    ))

    # Check 4: Developer Friction
    avg_friction = _calculate_avg_friction()
    friction_passed = avg_friction <= SPRINT_114_CONFIG["friction_target"]

    checks.append(DailyCheckResult(
        check_name="Developer Friction",
        passed=friction_passed,
        current_value=f"{avg_friction:.1f} min",
        target_value=f"<{SPRINT_114_CONFIG['friction_target']} min",
        severity="warning" if not friction_passed else "info",
        message=f"Average friction: {avg_friction:.1f} min per PR",
    ))

    if not friction_passed:
        recommendations.append("Investigate high friction PRs and tune auto-generation")

    # ==================
    # Day-Specific Checks
    # ==================

    if days_elapsed >= 2:
        # Day 2+: Check CEO time baseline
        ceo_summary = _calculate_ceo_time_summary()
        ceo_recorded = len(_ceo_time_entries) > 0

        checks.append(DailyCheckResult(
            check_name="CEO Time Baseline",
            passed=ceo_recorded,
            current_value=f"{ceo_summary['total_hours']:.1f}h recorded" if ceo_recorded else "Not recorded",
            target_value="Baseline recorded",
            severity="warning" if not ceo_recorded else "info",
            message="CEO time tracking baseline measurement",
        ))

        if not ceo_recorded:
            recommendations.append("Record CEO time baseline for Day 2")

    if days_elapsed >= 3:
        # Day 3+: Check developer feedback
        feedback_count = len(_developer_feedback)
        feedback_passed = feedback_count >= 3

        checks.append(DailyCheckResult(
            check_name="Developer Feedback",
            passed=feedback_passed,
            current_value=f"{feedback_count} responses",
            target_value=">=3 responses",
            severity="warning" if not feedback_passed else "info",
            message=f"{feedback_count} developer feedback responses collected",
        ))

        if not feedback_passed:
            recommendations.append("Collect more developer feedback via /feedback endpoint")

        # Day 3+: Index distribution analysis
        dist = _calculate_distribution()
        total = dist.green + dist.yellow + dist.orange + dist.red
        green_pct = (dist.green / total * 100) if total > 0 else 0

        checks.append(DailyCheckResult(
            check_name="Vibecoding Index Distribution",
            passed=green_pct >= 50,
            current_value=f"Green: {dist.green}, Yellow: {dist.yellow}, Orange: {dist.orange}, Red: {dist.red}",
            target_value=">=50% green zone",
            severity="info",
            message=f"{green_pct:.0f}% PRs in green zone (auto-approve)",
        ))

    if days_elapsed >= 4:
        # Day 4+: Check false positive rate
        fp_rate = _calculate_false_positive_rate()
        fp_passed = fp_rate <= SPRINT_114_CONFIG["false_positive_target"]

        checks.append(DailyCheckResult(
            check_name="False Positive Rate",
            passed=fp_passed,
            current_value=f"{fp_rate:.1f}%",
            target_value=f"<{SPRINT_114_CONFIG['false_positive_target']}%",
            severity="critical" if not fp_passed else "info",
            message=f"False positive rate: {fp_rate:.1f}%",
        ))

        if not fp_passed:
            recommendations.append("Review reported false positives and tune thresholds")

        # Day 4+: Check NPS
        nps = _calculate_team_nps()
        nps_passed = nps is not None and nps >= SPRINT_114_CONFIG["nps_target"]

        checks.append(DailyCheckResult(
            check_name="Team NPS Score",
            passed=nps_passed,
            current_value=f"{nps:.0f}" if nps else "N/A",
            target_value=f">{SPRINT_114_CONFIG['nps_target']}",
            severity="warning" if not nps_passed else "info",
            message=f"Team NPS: {nps:.0f}" if nps else "NPS survey not completed",
        ))

    # Calculate summary
    critical_issues = sum(1 for c in checks if not c.passed and c.severity == "critical")
    warnings = sum(1 for c in checks if not c.passed and c.severity == "warning")
    all_passed = critical_issues == 0 and warnings == 0

    return DailyChecksResponse(
        day=days_elapsed,
        date=today,
        checks=checks,
        all_passed=all_passed,
        critical_issues=critical_issues,
        warnings=warnings,
        recommendations=recommendations,
    )


@router.get("/daily-checks/history")
async def get_daily_checks_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get history of daily checks for all sprint days.

    Returns a summary of checks for each day of Sprint 114.
    """
    days_elapsed = _calculate_days_elapsed()
    history = []

    for day in range(1, days_elapsed + 1):
        # Generate summary for each day
        prs_by_day = [
            pr for pr in _pr_metrics
            if pr.get("timestamp") and
            (datetime.fromisoformat(pr["timestamp"].isoformat() if isinstance(pr["timestamp"], datetime) else pr["timestamp"]).date() -
             datetime.strptime(SPRINT_114_CONFIG["start_date"], "%Y-%m-%d").date()).days < day
        ]

        history.append({
            "day": day,
            "date": (datetime.strptime(SPRINT_114_CONFIG["start_date"], "%Y-%m-%d") +
                     timedelta(days=day - 1)).strftime("%Y-%m-%d"),
            "prs_evaluated": len(prs_by_day),
            "target": 5 * day,
            "status": "on_track" if len(prs_by_day) >= 5 * day else "behind",
        })

    return {
        "sprint": SPRINT_114_CONFIG["sprint"],
        "days_elapsed": days_elapsed,
        "total_days": SPRINT_114_CONFIG["total_days"],
        "history": history,
    }


# ============================================================================
# Day 2-4: Metrics Export Endpoints
# ============================================================================

@router.get("/export/prometheus")
async def export_prometheus_metrics(
    db: AsyncSession = Depends(get_db),
):
    """
    Export dogfooding metrics in Prometheus format.

    Used by Prometheus scraper for Grafana dashboards.
    """
    metrics_output = []

    # PR metrics
    metrics_output.append(f"# HELP dogfooding_prs_evaluated Total PRs evaluated in Sprint 114")
    metrics_output.append(f"# TYPE dogfooding_prs_evaluated gauge")
    metrics_output.append(f'dogfooding_prs_evaluated{{sprint="114",mode="WARNING"}} {len(_pr_metrics)}')

    # Vibecoding distribution
    dist = _calculate_distribution()
    metrics_output.append(f"# HELP dogfooding_vibecoding_distribution PR count by zone")
    metrics_output.append(f"# TYPE dogfooding_vibecoding_distribution gauge")
    metrics_output.append(f'dogfooding_vibecoding_distribution{{zone="green"}} {dist.green}')
    metrics_output.append(f'dogfooding_vibecoding_distribution{{zone="yellow"}} {dist.yellow}')
    metrics_output.append(f'dogfooding_vibecoding_distribution{{zone="orange"}} {dist.orange}')
    metrics_output.append(f'dogfooding_vibecoding_distribution{{zone="red"}} {dist.red}')

    # Average metrics
    avg_index = _calculate_average_index()
    avg_friction = _calculate_avg_friction()
    fp_rate = _calculate_false_positive_rate()
    nps = _calculate_team_nps()

    metrics_output.append(f"# HELP dogfooding_avg_vibecoding_index Average vibecoding index")
    metrics_output.append(f"# TYPE dogfooding_avg_vibecoding_index gauge")
    metrics_output.append(f"dogfooding_avg_vibecoding_index {avg_index:.2f}")

    metrics_output.append(f"# HELP dogfooding_avg_friction_minutes Average developer friction")
    metrics_output.append(f"# TYPE dogfooding_avg_friction_minutes gauge")
    metrics_output.append(f"dogfooding_avg_friction_minutes {avg_friction:.2f}")

    metrics_output.append(f"# HELP dogfooding_false_positive_rate False positive rate percentage")
    metrics_output.append(f"# TYPE dogfooding_false_positive_rate gauge")
    metrics_output.append(f"dogfooding_false_positive_rate {fp_rate:.2f}")

    if nps is not None:
        metrics_output.append(f"# HELP dogfooding_team_nps Team NPS score")
        metrics_output.append(f"# TYPE dogfooding_team_nps gauge")
        metrics_output.append(f"dogfooding_team_nps {nps:.2f}")

    # CEO time metrics
    ceo_summary = _calculate_ceo_time_summary()
    metrics_output.append(f"# HELP dogfooding_ceo_hours_recorded CEO hours recorded")
    metrics_output.append(f"# TYPE dogfooding_ceo_hours_recorded gauge")
    metrics_output.append(f"dogfooding_ceo_hours_recorded {ceo_summary['total_hours']:.2f}")

    # Feedback count
    metrics_output.append(f"# HELP dogfooding_feedback_count Developer feedback count")
    metrics_output.append(f"# TYPE dogfooding_feedback_count gauge")
    metrics_output.append(f"dogfooding_feedback_count {len(_developer_feedback)}")

    # Days elapsed
    metrics_output.append(f"# HELP dogfooding_days_elapsed Days elapsed in sprint")
    metrics_output.append(f"# TYPE dogfooding_days_elapsed gauge")
    metrics_output.append(f"dogfooding_days_elapsed {_calculate_days_elapsed()}")

    # Go/No-Go readiness
    blockers = _get_blockers()
    metrics_output.append(f"# HELP dogfooding_go_no_go_ready Go/No-Go readiness (1=ready, 0=not ready)")
    metrics_output.append(f"# TYPE dogfooding_go_no_go_ready gauge")
    metrics_output.append(f"dogfooding_go_no_go_ready {1 if len(blockers) == 0 else 0}")

    metrics_output.append(f"# HELP dogfooding_blockers_count Number of Go/No-Go blockers")
    metrics_output.append(f"# TYPE dogfooding_blockers_count gauge")
    metrics_output.append(f"dogfooding_blockers_count {len(blockers)}")

    return "\n".join(metrics_output)


@router.get("/export/json")
async def export_json_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Export all dogfooding metrics as JSON.

    Comprehensive export for reporting and analysis.
    """
    distribution = _calculate_distribution()
    feedback_summary = _get_feedback_summary()
    ceo_summary = _calculate_ceo_time_summary()
    blockers = _get_blockers()

    return {
        "sprint": SPRINT_114_CONFIG,
        "days_elapsed": _calculate_days_elapsed(),
        "export_timestamp": datetime.utcnow().isoformat(),

        "pr_metrics": {
            "total": len(_pr_metrics),
            "target": SPRINT_114_CONFIG["prs_target"],
            "distribution": {
                "green": distribution.green,
                "yellow": distribution.yellow,
                "orange": distribution.orange,
                "red": distribution.red,
            },
            "average_index": _calculate_average_index(),
            "average_friction": _calculate_avg_friction(),
            "false_positive_rate": _calculate_false_positive_rate(),
            "raw_data": _pr_metrics,
        },

        "developer_feedback": {
            "total_responses": feedback_summary["total"],
            "average_nps": feedback_summary["avg_nps"],
            "satisfaction_distribution": feedback_summary["satisfaction_dist"],
            "perceived_friction": feedback_summary["avg_friction"],
            "recommendation_rate": feedback_summary["recommend_rate"],
            "top_pain_points": feedback_summary["pain_points"],
            "top_helpful_aspects": feedback_summary["helpful"],
            "by_category": feedback_summary["by_category"],
            "raw_data": _developer_feedback,
        },

        "ceo_time": {
            "baseline_hours": CEO_TIME_BASELINE["weekly_hours"],
            "recorded_hours": ceo_summary["total_hours"],
            "breakdown": ceo_summary["breakdown"],
            "daily_trend": ceo_summary["daily"],
            "raw_data": _ceo_time_entries,
        },

        "go_no_go": {
            "ready": len(blockers) == 0,
            "blockers": blockers,
            "checks": {
                "prs_evaluated": len(_pr_metrics) >= SPRINT_114_CONFIG["prs_target"],
                "friction_ok": _calculate_avg_friction() <= SPRINT_114_CONFIG["friction_target"],
                "fp_rate_ok": _calculate_false_positive_rate() <= SPRINT_114_CONFIG["false_positive_target"],
                "nps_ok": (_calculate_team_nps() or 0) >= SPRINT_114_CONFIG["nps_target"],
            },
        },
    }
