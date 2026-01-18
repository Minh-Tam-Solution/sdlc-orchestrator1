"""
=========================================================================
Forecast Service - Sprint Completion Prediction
SDLC Orchestrator - Sprint 77 Day 3

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 77 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)
Reference: Sprint 77 Technical Design - Sprint Forecasting

Purpose:
- Predict sprint completion probability
- Calculate burn rates (current vs required)
- Identify risk factors (blocked items, incomplete P0s)
- Generate recommendations for on-time delivery

Performance Budget:
- Query time: <50ms
- Calculation time: <30ms
- Total response: <100ms p95

Zero Mock Policy: Production-ready implementation with real DB queries
=========================================================================
"""

from datetime import date as date_type, datetime, timedelta
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.backlog_item import BacklogItem
from app.models.sprint import Sprint


# =========================================================================
# Schemas
# =========================================================================


class ForecastRisk(BaseModel):
    """Identified risk factor."""

    risk_type: str = Field(
        ...,
        description="Risk type: blocked_items, low_completion, p0_incomplete, behind_schedule",
    )
    severity: str = Field(
        ...,
        description="Severity: low, medium, high, critical",
    )
    message: str = Field(..., description="Human-readable risk description")
    recommendation: str = Field(..., description="Suggested action to mitigate risk")

    model_config = ConfigDict(from_attributes=True)


class SprintForecast(BaseModel):
    """Sprint completion forecast."""

    sprint_id: UUID = Field(..., description="Sprint UUID")
    sprint_number: int = Field(..., description="Sprint number")
    sprint_name: str = Field(..., description="Sprint name")
    probability: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Completion probability (0-100%)",
    )
    predicted_end_date: Optional[date_type] = Field(
        None,
        description="Predicted completion date based on current burn rate",
    )
    on_track: bool = Field(
        ...,
        description="Whether sprint is on track to complete on time",
    )
    remaining_points: int = Field(..., description="Story points remaining")
    total_points: int = Field(..., description="Total committed story points")
    completed_points: int = Field(..., description="Completed story points")
    current_burn_rate: float = Field(
        ...,
        description="Current points per day burn rate",
    )
    required_burn_rate: float = Field(
        ...,
        description="Required points per day to complete on time",
    )
    days_elapsed: int = Field(..., description="Days since sprint start")
    days_remaining: int = Field(..., description="Days until sprint end")
    risks: List[ForecastRisk] = Field(
        default_factory=list,
        description="Identified risk factors",
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="AI-generated recommendations",
    )

    model_config = ConfigDict(from_attributes=True)


# =========================================================================
# Service
# =========================================================================


class ForecastService:
    """
    AI-powered sprint forecasting service.

    Predicts sprint completion probability using:
    - Current burn rate vs required burn rate
    - Historical velocity patterns
    - Blocked items and P0 status
    - Risk factor analysis

    Performance:
    - Query complexity: O(n) where n = backlog items
    - Response time target: <100ms p95
    """

    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        self.db = db

    async def forecast_completion(self, sprint_id: UUID) -> SprintForecast:
        """
        Predict sprint completion probability.

        Factors considered:
        1. Current burn rate (completed / days elapsed)
        2. Required burn rate (remaining / days remaining)
        3. Blocked items count (-5% per blocked item)
        4. P0 completion status (-10% for incomplete P0)
        5. Days remaining (urgency factor)

        Args:
            sprint_id: Sprint UUID

        Returns:
            SprintForecast with probability, risks, and recommendations

        Raises:
            ValueError: If sprint not found or has no dates
        """
        # 1. Fetch sprint details
        sprint = await self._get_sprint(sprint_id)
        if not sprint:
            raise ValueError(f"Sprint {sprint_id} not found")

        if not sprint.start_date or not sprint.end_date:
            raise ValueError(f"Sprint {sprint_id} has no start/end dates")

        # 2. Get backlog items
        items = await self._get_backlog_items(sprint_id)

        # 3. Calculate metrics
        total_points = sum(item.story_points or 0 for item in items)
        completed_points = sum(
            item.story_points or 0
            for item in items
            if item.status == "done"
        )
        remaining_points = total_points - completed_points

        # Count blocked items and incomplete P0s
        blocked_count = len([item for item in items if item.status == "blocked"])
        p0_items = [item for item in items if item.priority == "P0"]
        p0_incomplete = len([item for item in p0_items if item.status != "done"])

        # 4. Calculate time metrics
        today = date_type.today()
        days_elapsed = max(0, (today - sprint.start_date).days) if today >= sprint.start_date else 0
        days_remaining = max(0, (sprint.end_date - today).days + 1) if today <= sprint.end_date else 0

        # 5. Calculate burn rates
        current_burn_rate = completed_points / max(1, days_elapsed) if days_elapsed > 0 else 0.0
        required_burn_rate = remaining_points / max(1, days_remaining) if days_remaining > 0 else float('inf')

        # 6. Calculate probability
        probability = self._calculate_probability(
            remaining_points=remaining_points,
            days_remaining=days_remaining,
            current_burn_rate=current_burn_rate,
            blocked_count=blocked_count,
            p0_incomplete=p0_incomplete,
        )

        # 7. Predict end date based on current burn rate
        predicted_end_date = self._predict_end_date(
            remaining_points=remaining_points,
            current_burn_rate=current_burn_rate,
            start_date=today,
        )

        # 8. Determine if on track
        on_track = probability >= 70 and (
            predicted_end_date is None or predicted_end_date <= sprint.end_date
        )

        # 9. Identify risks
        risks = self._identify_risks(
            blocked_count=blocked_count,
            p0_incomplete=p0_incomplete,
            current_burn_rate=current_burn_rate,
            required_burn_rate=required_burn_rate,
            days_remaining=days_remaining,
            probability=probability,
        )

        # 10. Generate recommendations
        recommendations = self._generate_recommendations(
            risks=risks,
            blocked_count=blocked_count,
            p0_incomplete=p0_incomplete,
            current_burn_rate=current_burn_rate,
            required_burn_rate=required_burn_rate,
            days_remaining=days_remaining,
        )

        return SprintForecast(
            sprint_id=sprint.id,
            sprint_number=sprint.number,
            sprint_name=sprint.name,
            probability=round(probability, 1),
            predicted_end_date=predicted_end_date,
            on_track=on_track,
            remaining_points=remaining_points,
            total_points=total_points,
            completed_points=completed_points,
            current_burn_rate=round(current_burn_rate, 2),
            required_burn_rate=round(required_burn_rate, 2) if required_burn_rate != float('inf') else 0.0,
            days_elapsed=days_elapsed,
            days_remaining=days_remaining,
            risks=risks,
            recommendations=recommendations,
        )

    async def _get_sprint(self, sprint_id: UUID) -> Optional[Sprint]:
        """Fetch sprint by ID."""
        result = await self.db.execute(
            select(Sprint).where(Sprint.id == sprint_id)
        )
        return result.scalar_one_or_none()

    async def _get_backlog_items(self, sprint_id: UUID) -> List[BacklogItem]:
        """Fetch all backlog items for a sprint."""
        result = await self.db.execute(
            select(BacklogItem)
            .where(BacklogItem.sprint_id == sprint_id)
        )
        return list(result.scalars().all())

    def _calculate_probability(
        self,
        remaining_points: int,
        days_remaining: int,
        current_burn_rate: float,
        blocked_count: int,
        p0_incomplete: int,
    ) -> float:
        """
        Calculate completion probability.

        Formula:
        - base_prob = min(100, burn_rate / required_rate * 100)
        - penalties = blocked_count * 5 + p0_incomplete * 10
        - final = max(0, base_prob - penalties)

        Args:
            remaining_points: Story points remaining
            days_remaining: Days until sprint end
            current_burn_rate: Current points per day
            blocked_count: Number of blocked items
            p0_incomplete: Number of incomplete P0 items

        Returns:
            Completion probability (0-100%)
        """
        # Sprint complete
        if remaining_points == 0:
            return 100.0

        # Sprint ended with remaining work
        if days_remaining <= 0:
            return 0.0

        # Calculate required burn rate
        required_rate = remaining_points / days_remaining

        # Edge case: no work required
        if required_rate == 0:
            return 100.0

        # Base probability from burn rate comparison
        if current_burn_rate > 0:
            base_prob = min(100, (current_burn_rate / required_rate) * 100)
        else:
            # No progress yet - estimate based on time remaining
            base_prob = max(0, 100 - (remaining_points * 5))

        # Apply penalties
        penalties = blocked_count * 5 + p0_incomplete * 10

        return max(0, min(100, base_prob - penalties))

    def _predict_end_date(
        self,
        remaining_points: int,
        current_burn_rate: float,
        start_date: date_type,
    ) -> Optional[date_type]:
        """
        Predict sprint completion date based on current burn rate.

        Args:
            remaining_points: Story points remaining
            current_burn_rate: Current points per day
            start_date: Date to start prediction from

        Returns:
            Predicted completion date, or None if burn rate is 0
        """
        if remaining_points == 0:
            return start_date

        if current_burn_rate <= 0:
            return None  # Cannot predict without burn rate

        days_needed = remaining_points / current_burn_rate
        return start_date + timedelta(days=int(days_needed))

    def _identify_risks(
        self,
        blocked_count: int,
        p0_incomplete: int,
        current_burn_rate: float,
        required_burn_rate: float,
        days_remaining: int,
        probability: float,
    ) -> List[ForecastRisk]:
        """
        Identify risk factors affecting sprint completion.

        Args:
            blocked_count: Number of blocked items
            p0_incomplete: Number of incomplete P0 items
            current_burn_rate: Current points per day
            required_burn_rate: Required points per day
            days_remaining: Days until sprint end
            probability: Calculated completion probability

        Returns:
            List of identified risks
        """
        risks = []

        # Risk: Blocked items
        if blocked_count > 0:
            severity = "high" if blocked_count >= 3 else "medium" if blocked_count >= 2 else "low"
            risks.append(ForecastRisk(
                risk_type="blocked_items",
                severity=severity,
                message=f"{blocked_count} item(s) are blocked and cannot progress",
                recommendation="Prioritize unblocking items. Escalate if blocked > 24h.",
            ))

        # Risk: Incomplete P0s
        if p0_incomplete > 0:
            severity = "critical" if p0_incomplete >= 2 else "high"
            risks.append(ForecastRisk(
                risk_type="p0_incomplete",
                severity=severity,
                message=f"{p0_incomplete} P0 item(s) are not yet complete",
                recommendation="Focus team resources on P0 items. Consider scope reduction if needed.",
            ))

        # Risk: Behind schedule
        if required_burn_rate > 0 and current_burn_rate < required_burn_rate * 0.7:
            severity = "critical" if current_burn_rate < required_burn_rate * 0.5 else "high"
            risks.append(ForecastRisk(
                risk_type="behind_schedule",
                severity=severity,
                message=f"Current burn rate ({current_burn_rate:.1f}/day) is below required ({required_burn_rate:.1f}/day)",
                recommendation="Identify and remove blockers. Consider adding resources or reducing scope.",
            ))

        # Risk: Low completion probability
        if probability < 50:
            severity = "critical" if probability < 30 else "high"
            risks.append(ForecastRisk(
                risk_type="low_completion",
                severity=severity,
                message=f"Completion probability is only {probability:.0f}%",
                recommendation="Urgent review needed. Consider de-scoping non-P0 items.",
            ))

        # Risk: Last day crunch
        if days_remaining <= 2 and probability < 80:
            risks.append(ForecastRisk(
                risk_type="time_pressure",
                severity="high",
                message=f"Only {days_remaining} day(s) remaining with {probability:.0f}% probability",
                recommendation="Focus on must-have items only. Move nice-to-haves to backlog.",
            ))

        return risks

    def _generate_recommendations(
        self,
        risks: List[ForecastRisk],
        blocked_count: int,
        p0_incomplete: int,
        current_burn_rate: float,
        required_burn_rate: float,
        days_remaining: int,
    ) -> List[str]:
        """
        Generate actionable recommendations based on sprint state.

        Args:
            risks: Identified risks
            blocked_count: Number of blocked items
            p0_incomplete: Number of incomplete P0 items
            current_burn_rate: Current points per day
            required_burn_rate: Required points per day
            days_remaining: Days until sprint end

        Returns:
            List of recommendations
        """
        recommendations = []

        # Priority-based recommendations
        if p0_incomplete > 0:
            recommendations.append(
                f"🎯 Focus: Complete {p0_incomplete} remaining P0 item(s) before any other work."
            )

        if blocked_count > 0:
            recommendations.append(
                f"🚫 Blockers: Resolve {blocked_count} blocked item(s). Escalate immediately if external."
            )

        # Burn rate recommendations
        if required_burn_rate > 0:
            if current_burn_rate < required_burn_rate * 0.5:
                recommendations.append(
                    "⚡ Velocity: Consider pair programming or swarming on remaining items."
                )
            elif current_burn_rate < required_burn_rate * 0.8:
                recommendations.append(
                    "📈 Velocity: Increase daily focus time. Minimize meetings and context switches."
                )

        # Time-based recommendations
        if days_remaining <= 2:
            recommendations.append(
                "⏰ Time Critical: Only work on sprint-committed items. Defer all other requests."
            )
        elif days_remaining <= 5:
            recommendations.append(
                "📋 Mid-Sprint: Review backlog daily. Move at-risk items to next sprint proactively."
            )

        # Risk-count based
        critical_risks = [r for r in risks if r.severity == "critical"]
        if len(critical_risks) >= 2:
            recommendations.append(
                "🚨 Multiple Critical Risks: Schedule emergency standup to address blockers."
            )

        # Success case
        if not risks and current_burn_rate >= required_burn_rate:
            recommendations.append(
                "✅ On Track: Maintain current pace. Consider helping teammates or preparing for next sprint."
            )

        return recommendations[:5]  # Limit to 5 recommendations


def get_forecast_service(db: AsyncSession) -> ForecastService:
    """Factory function for ForecastService."""
    return ForecastService(db)
