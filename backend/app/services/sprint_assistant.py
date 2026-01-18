"""
=========================================================================
Sprint Assistant Service - AI-Powered Sprint Recommendations & Analytics
SDLC Orchestrator - Sprint 76 Day 4

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 76 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)
Reference: SPRINT-76-SASE-WORKFLOW-INTEGRATION.md

Purpose:
- Calculate velocity metrics from historical sprint data
- Provide sprint health indicators (completion rate, risk level)
- Generate AI-powered backlog prioritization suggestions
- Support data-driven sprint planning decisions

Features:
- Velocity calculation from last N completed sprints
- Sprint health with risk level assessment
- P0/P1/P2 prioritization suggestions
- Overload detection based on historical velocity
- Blocked item warnings
- Unassigned high-priority item alerts

Performance Targets:
- calculate_velocity: <100ms (5 sprints)
- get_sprint_health: <50ms
- suggest_priorities: <100ms

Zero Mock Policy: Production-ready service with real database queries
=========================================================================
"""

from datetime import datetime, date
from typing import List, Optional
from uuid import UUID
import logging

from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.sprint import Sprint
from app.models.backlog_item import BacklogItem
from app.models.project import Project


logger = logging.getLogger(__name__)


# ==================== Response Models ====================

class VelocityMetrics(BaseModel):
    """
    Velocity metrics calculated from historical sprint data.

    Attributes:
        average: Average story points completed per sprint
        trend: Velocity trend (increasing, decreasing, stable, unknown)
        confidence: Confidence score based on data availability (0-1)
        history: List of velocity values from recent sprints
        sprint_count: Number of sprints used in calculation
    """
    average: float = Field(default=0.0, description="Average velocity in story points")
    trend: str = Field(default="unknown", description="Trend: increasing, decreasing, stable, unknown")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score")
    history: List[int] = Field(default_factory=list, description="Velocity history")
    sprint_count: int = Field(default=0, description="Number of sprints analyzed")


class SprintHealth(BaseModel):
    """
    Sprint health indicators.

    Attributes:
        completion_rate: Percentage of story points completed (0-100)
        completed_points: Story points completed
        total_points: Total story points in sprint
        blocked_count: Number of blocked items
        risk_level: Risk assessment (low, medium, high)
        days_remaining: Days until sprint end
        days_elapsed: Days since sprint start
        expected_completion: Expected completion rate based on time elapsed
    """
    completion_rate: float = Field(default=0.0, ge=0.0, le=100.0)
    completed_points: int = Field(default=0)
    total_points: int = Field(default=0)
    blocked_count: int = Field(default=0)
    risk_level: str = Field(default="low", description="Risk level: low, medium, high")
    days_remaining: int = Field(default=0)
    days_elapsed: int = Field(default=0)
    expected_completion: float = Field(default=0.0, ge=0.0, le=100.0)


class PrioritySuggestion(BaseModel):
    """
    AI-powered prioritization suggestion.

    Attributes:
        type: Suggestion type (start_p0, unassigned_p0, overloaded, blocked, etc.)
        message: Human-readable suggestion message
        severity: Severity level (info, warning, error)
        items: List of backlog item IDs related to suggestion
        action: Recommended action
    """
    type: str = Field(description="Suggestion type identifier")
    message: str = Field(description="Human-readable message")
    severity: str = Field(default="info", description="Severity: info, warning, error")
    items: List[UUID] = Field(default_factory=list, description="Related backlog item IDs")
    action: Optional[str] = Field(default=None, description="Recommended action")


class SprintAnalytics(BaseModel):
    """
    Comprehensive sprint analytics.

    Combines velocity, health, and suggestions for a complete picture.
    """
    sprint_id: UUID
    sprint_number: int
    sprint_name: str
    health: SprintHealth
    velocity: VelocityMetrics
    suggestions: List[PrioritySuggestion]
    summary: str = Field(description="AI-generated summary of sprint status")


# ==================== Service Implementation ====================

class SprintAssistantService:
    """
    AI-powered sprint recommendations and analytics.

    Provides data-driven insights for sprint planning and execution:
    - Velocity calculation from historical data
    - Sprint health indicators with risk assessment
    - Backlog prioritization suggestions
    - Overload and blocked item detection

    SDLC 5.1.3 Alignment:
    - Rule #7: Sprint Goal Must Align with Roadmap Phase
    - Rule #8: Strategic Priorities Explicit (P0/P1/P2)
    - Data-driven sprint capacity planning

    Usage:
        assistant = SprintAssistantService(db)
        velocity = await assistant.calculate_velocity(project_id)
        health = await assistant.get_sprint_health(sprint_id)
        suggestions = await assistant.suggest_priorities(sprint_id)
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize SprintAssistantService.

        Args:
            db: SQLAlchemy async session for database operations
        """
        self.db = db

    # ==================== Velocity Calculation ====================

    async def calculate_velocity(
        self,
        project_id: UUID,
        sprint_count: int = 5,
    ) -> VelocityMetrics:
        """
        Calculate average velocity from last N completed sprints.

        Velocity is measured as story points completed per sprint.
        Uses only completed sprints with at least one done item.

        Args:
            project_id: Project UUID
            sprint_count: Number of completed sprints to analyze (default: 5)

        Returns:
            VelocityMetrics with average, trend, confidence, and history

        Performance:
            - Target: <100ms for 5 sprints
            - Uses eager loading for backlog items
        """
        # Query completed sprints with backlog items
        result = await self.db.execute(
            select(Sprint)
            .options(selectinload(Sprint.backlog_items))
            .where(
                Sprint.project_id == project_id,
                Sprint.status.in_(["completed", "closed"]),
            )
            .order_by(Sprint.end_date.desc())
            .limit(sprint_count)
        )
        completed_sprints = result.scalars().all()

        if not completed_sprints:
            logger.debug(f"No completed sprints found for project {project_id}")
            return VelocityMetrics(
                average=0.0,
                trend="unknown",
                confidence=0.0,
                history=[],
                sprint_count=0,
            )

        # Calculate velocity for each sprint (completed story points)
        velocities = []
        for sprint in completed_sprints:
            sprint_velocity = sum(
                item.story_points or 0
                for item in sprint.backlog_items
                if item.status == "done"
            )
            velocities.append(sprint_velocity)

        # Reverse to chronological order for trend calculation
        velocities = velocities[::-1]

        # Calculate metrics
        average = sum(velocities) / len(velocities) if velocities else 0.0
        trend = self._calculate_trend(velocities)
        confidence = min(len(velocities) / sprint_count, 1.0)

        logger.debug(
            f"Velocity for project {project_id}: "
            f"avg={average:.1f}, trend={trend}, confidence={confidence:.2f}"
        )

        return VelocityMetrics(
            average=round(average, 1),
            trend=trend,
            confidence=round(confidence, 2),
            history=velocities,
            sprint_count=len(velocities),
        )

    def _calculate_trend(self, velocities: List[int]) -> str:
        """
        Calculate velocity trend from history.

        Uses simple linear comparison of first half vs second half.

        Args:
            velocities: List of velocity values (chronological order)

        Returns:
            Trend string: "increasing", "decreasing", "stable", or "unknown"
        """
        if len(velocities) < 2:
            return "unknown"

        if len(velocities) == 2:
            if velocities[1] > velocities[0] * 1.1:
                return "increasing"
            elif velocities[1] < velocities[0] * 0.9:
                return "decreasing"
            return "stable"

        # Compare first half average to second half average
        mid = len(velocities) // 2
        first_half = sum(velocities[:mid]) / mid if mid > 0 else 0
        second_half = sum(velocities[mid:]) / (len(velocities) - mid) if len(velocities) > mid else 0

        if second_half > first_half * 1.1:
            return "increasing"
        elif second_half < first_half * 0.9:
            return "decreasing"
        return "stable"

    # ==================== Sprint Health ====================

    async def get_sprint_health(
        self,
        sprint_id: UUID,
    ) -> SprintHealth:
        """
        Calculate sprint health indicators.

        Analyzes completion rate, blocked items, and time progress
        to determine risk level.

        Risk Level Calculation:
        - High: Completion rate 20%+ behind expected
        - Medium: Completion rate 10-20% behind expected
        - Low: On track or ahead

        Args:
            sprint_id: Sprint UUID

        Returns:
            SprintHealth with completion metrics and risk assessment

        Raises:
            ValueError: If sprint not found
        """
        # Query sprint with backlog items
        result = await self.db.execute(
            select(Sprint)
            .options(selectinload(Sprint.backlog_items))
            .where(Sprint.id == sprint_id)
        )
        sprint = result.scalar_one_or_none()

        if not sprint:
            raise ValueError(f"Sprint {sprint_id} not found")

        # Calculate story points
        total_points = sum(
            item.story_points or 0 for item in sprint.backlog_items
        )
        completed_points = sum(
            item.story_points or 0
            for item in sprint.backlog_items
            if item.status == "done"
        )
        blocked_count = sum(
            1 for item in sprint.backlog_items
            if item.status == "blocked"
        )

        # Calculate completion rate (as percentage)
        completion_rate = (completed_points / total_points * 100) if total_points > 0 else 0.0

        # Calculate time progress
        today = date.today()
        days_elapsed = 0
        days_remaining = 0
        expected_completion = 0.0

        if sprint.start_date and sprint.end_date:
            if today >= sprint.start_date:
                days_elapsed = (today - sprint.start_date).days
            if today <= sprint.end_date:
                days_remaining = (sprint.end_date - today).days
            else:
                days_remaining = 0

            days_total = (sprint.end_date - sprint.start_date).days
            if days_total > 0:
                expected_completion = min(100.0, (days_elapsed / days_total) * 100)

        # Determine risk level
        risk_level = "low"
        if total_points > 0 and sprint.start_date and sprint.end_date:
            completion_gap = expected_completion - completion_rate
            if completion_gap > 20:
                risk_level = "high"
            elif completion_gap > 10:
                risk_level = "medium"
            elif blocked_count >= 3:
                risk_level = "medium"

        logger.debug(
            f"Sprint health for {sprint_id}: "
            f"completion={completion_rate:.1f}%, risk={risk_level}, blocked={blocked_count}"
        )

        return SprintHealth(
            completion_rate=round(completion_rate, 1),
            completed_points=completed_points,
            total_points=total_points,
            blocked_count=blocked_count,
            risk_level=risk_level,
            days_remaining=max(0, days_remaining),
            days_elapsed=max(0, days_elapsed),
            expected_completion=round(expected_completion, 1),
        )

    # ==================== Prioritization Suggestions ====================

    async def suggest_priorities(
        self,
        sprint_id: UUID,
    ) -> List[PrioritySuggestion]:
        """
        Generate AI-powered backlog prioritization suggestions.

        Analyzes backlog items and generates suggestions based on:
        - P0 items not yet started
        - Unassigned high-priority items
        - Sprint overload based on velocity
        - Blocked items requiring attention
        - Low-priority items at risk

        Args:
            sprint_id: Sprint UUID

        Returns:
            List of PrioritySuggestion with recommended actions
        """
        # Query sprint with backlog items and project
        result = await self.db.execute(
            select(Sprint)
            .options(
                selectinload(Sprint.backlog_items),
                selectinload(Sprint.project),
            )
            .where(Sprint.id == sprint_id)
        )
        sprint = result.scalar_one_or_none()

        if not sprint:
            raise ValueError(f"Sprint {sprint_id} not found")

        suggestions = []

        # Get velocity for overload check
        velocity = await self.calculate_velocity(sprint.project_id)

        # 1. P0 items not started (CRITICAL)
        p0_not_started = [
            item for item in sprint.backlog_items
            if item.priority == "P0" and item.status == "todo"
        ]
        if p0_not_started:
            suggestions.append(PrioritySuggestion(
                type="start_p0",
                message=f"{len(p0_not_started)} P0 (critical) item(s) not yet started",
                severity="error",
                items=[item.id for item in p0_not_started],
                action="Start P0 items immediately - they are sprint-critical",
            ))

        # 2. Unassigned P0/P1 items
        unassigned_high_priority = [
            item for item in sprint.backlog_items
            if item.priority in ("P0", "P1") and item.assignee_id is None
        ]
        if unassigned_high_priority:
            suggestions.append(PrioritySuggestion(
                type="unassigned_priority",
                message=f"{len(unassigned_high_priority)} high-priority item(s) unassigned",
                severity="warning",
                items=[item.id for item in unassigned_high_priority],
                action="Assign P0/P1 items to team members",
            ))

        # 3. Sprint overload check
        total_points = sum(item.story_points or 0 for item in sprint.backlog_items)
        if velocity.average > 0 and total_points > velocity.average * 1.2:
            suggestions.append(PrioritySuggestion(
                type="overloaded",
                message=f"Sprint has {total_points} SP but velocity is {velocity.average:.0f} SP",
                severity="warning",
                items=[],
                action=f"Consider moving {total_points - int(velocity.average)} SP to next sprint",
            ))

        # 4. Blocked items
        blocked_items = [
            item for item in sprint.backlog_items
            if item.status == "blocked"
        ]
        if blocked_items:
            suggestions.append(PrioritySuggestion(
                type="blocked",
                message=f"{len(blocked_items)} item(s) are blocked",
                severity="warning" if len(blocked_items) < 3 else "error",
                items=[item.id for item in blocked_items],
                action="Resolve blockers to unblock progress",
            ))

        # 5. P2 items at risk (if sprint is >50% complete and P0/P1 not done)
        health = await self.get_sprint_health(sprint_id)
        if health.expected_completion > 50:
            p0_p1_incomplete = [
                item for item in sprint.backlog_items
                if item.priority in ("P0", "P1") and item.status != "done"
            ]
            p2_items = [
                item for item in sprint.backlog_items
                if item.priority == "P2" and item.status != "done"
            ]
            if p0_p1_incomplete and p2_items:
                suggestions.append(PrioritySuggestion(
                    type="p2_at_risk",
                    message=f"{len(p2_items)} P2 item(s) may not complete due to P0/P1 backlog",
                    severity="info",
                    items=[item.id for item in p2_items],
                    action="Consider moving P2 items to next sprint if P0/P1 delayed",
                ))

        # 6. Underloaded sprint (opportunity)
        if velocity.average > 0 and total_points < velocity.average * 0.8:
            suggestions.append(PrioritySuggestion(
                type="underloaded",
                message=f"Sprint has only {total_points} SP, team velocity is {velocity.average:.0f} SP",
                severity="info",
                items=[],
                action="Consider pulling items from backlog to maximize sprint value",
            ))

        logger.debug(f"Generated {len(suggestions)} suggestions for sprint {sprint_id}")

        return suggestions

    # ==================== Comprehensive Analytics ====================

    async def get_sprint_analytics(
        self,
        sprint_id: UUID,
    ) -> SprintAnalytics:
        """
        Get comprehensive sprint analytics.

        Combines velocity, health, and suggestions into a single response.

        Args:
            sprint_id: Sprint UUID

        Returns:
            SprintAnalytics with all metrics and AI summary
        """
        # Query sprint
        result = await self.db.execute(
            select(Sprint)
            .options(selectinload(Sprint.project))
            .where(Sprint.id == sprint_id)
        )
        sprint = result.scalar_one_or_none()

        if not sprint:
            raise ValueError(f"Sprint {sprint_id} not found")

        # Get all metrics
        health = await self.get_sprint_health(sprint_id)
        velocity = await self.calculate_velocity(sprint.project_id)
        suggestions = await self.suggest_priorities(sprint_id)

        # Generate summary
        summary = self._generate_summary(sprint, health, velocity, suggestions)

        return SprintAnalytics(
            sprint_id=sprint.id,
            sprint_number=sprint.number,
            sprint_name=sprint.name,
            health=health,
            velocity=velocity,
            suggestions=suggestions,
            summary=summary,
        )

    def _generate_summary(
        self,
        sprint: Sprint,
        health: SprintHealth,
        velocity: VelocityMetrics,
        suggestions: List[PrioritySuggestion],
    ) -> str:
        """
        Generate AI summary of sprint status.

        Args:
            sprint: Sprint model
            health: Sprint health metrics
            velocity: Velocity metrics
            suggestions: List of suggestions

        Returns:
            Human-readable summary string
        """
        parts = []

        # Health status
        if health.risk_level == "high":
            parts.append(f"Sprint {sprint.number} is at HIGH RISK with {health.completion_rate:.0f}% completion.")
        elif health.risk_level == "medium":
            parts.append(f"Sprint {sprint.number} needs attention with {health.completion_rate:.0f}% completion.")
        else:
            parts.append(f"Sprint {sprint.number} is on track with {health.completion_rate:.0f}% completion.")

        # Points progress
        parts.append(f"{health.completed_points}/{health.total_points} story points done.")

        # Time remaining
        if health.days_remaining > 0:
            parts.append(f"{health.days_remaining} day(s) remaining.")
        elif health.days_remaining == 0:
            parts.append("Sprint ends today.")
        else:
            parts.append("Sprint has ended.")

        # Critical issues
        error_suggestions = [s for s in suggestions if s.severity == "error"]
        if error_suggestions:
            parts.append(f"CRITICAL: {len(error_suggestions)} issue(s) require immediate attention.")

        return " ".join(parts)


# ==================== Factory Function ====================

def get_sprint_assistant_service(db: AsyncSession) -> SprintAssistantService:
    """
    Factory function for dependency injection.

    Args:
        db: AsyncSession from dependency injection

    Returns:
        SprintAssistantService instance
    """
    return SprintAssistantService(db)
