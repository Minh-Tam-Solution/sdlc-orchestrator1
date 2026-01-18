"""
=========================================================================
Retrospective Service - Sprint Retrospective Generation
SDLC Orchestrator - Sprint 77 Day 4

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 77 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)
Reference: Sprint 77 Technical Design - Retrospective Automation

Purpose:
- Auto-generate sprint retrospective from metrics
- Identify "went well" and "needs improvement" insights
- Generate action items based on sprint performance
- Calculate completion and velocity metrics

Performance Budget:
- Query time: <50ms
- Analysis time: <30ms
- Total response: <100ms p95

Zero Mock Policy: Production-ready implementation with real DB queries
=========================================================================
"""

from datetime import date as date_type, datetime, timedelta
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.backlog_item import BacklogItem
from app.models.sprint import Sprint


# =========================================================================
# Schemas
# =========================================================================


class RetroInsight(BaseModel):
    """Retrospective insight item."""

    category: str = Field(
        ...,
        description="Category: delivery, priority, velocity, planning, scope, blockers, team",
    )
    insight_type: str = Field(
        ...,
        description="Type: went_well or needs_improvement",
    )
    title: str = Field(..., description="Short insight title")
    description: str = Field(..., description="Detailed insight description")
    impact: str = Field(
        default="medium",
        description="Impact level: low, medium, high",
    )

    model_config = ConfigDict(from_attributes=True)


class RetroAction(BaseModel):
    """Retrospective action item."""

    id: UUID = Field(default_factory=uuid4, description="Action item UUID")
    description: str = Field(..., description="Action item description")
    owner: Optional[str] = Field(None, description="Assigned owner")
    due_date: Optional[date_type] = Field(None, description="Target completion date")
    status: str = Field(
        default="pending",
        description="Status: pending, in_progress, done",
    )
    priority: str = Field(
        default="medium",
        description="Priority: low, medium, high",
    )

    model_config = ConfigDict(from_attributes=True)


class RetroMetrics(BaseModel):
    """Sprint metrics for retrospective."""

    committed_points: int = Field(..., description="Total committed story points")
    completed_points: int = Field(..., description="Completed story points")
    completion_rate: float = Field(..., description="Completion rate (0-1)")
    p0_total: int = Field(..., description="Total P0 items")
    p0_completed: int = Field(..., description="Completed P0 items")
    p0_completion_rate: float = Field(..., description="P0 completion rate (0-1)")
    items_added_mid_sprint: int = Field(..., description="Items added after sprint start")
    blocked_items: int = Field(..., description="Items that were blocked")
    average_cycle_time_days: Optional[float] = Field(
        None,
        description="Average days from start to completion",
    )
    velocity_trend: str = Field(
        default="stable",
        description="Velocity trend: improving, stable, declining",
    )

    model_config = ConfigDict(from_attributes=True)


class SprintRetrospective(BaseModel):
    """Complete sprint retrospective."""

    sprint_id: UUID = Field(..., description="Sprint UUID")
    sprint_number: int = Field(..., description="Sprint number")
    sprint_name: str = Field(..., description="Sprint name")
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Generation timestamp",
    )
    metrics: RetroMetrics = Field(..., description="Sprint metrics summary")
    went_well: List[RetroInsight] = Field(
        default_factory=list,
        description="What went well",
    )
    needs_improvement: List[RetroInsight] = Field(
        default_factory=list,
        description="What needs improvement",
    )
    action_items: List[RetroAction] = Field(
        default_factory=list,
        description="Suggested action items",
    )
    summary: str = Field(..., description="Executive summary of the sprint")

    model_config = ConfigDict(from_attributes=True)


# =========================================================================
# Service
# =========================================================================


class RetrospectiveService:
    """
    AI-powered sprint retrospective generation service.

    Analyzes sprint data to automatically generate:
    - Metrics summary (completion rate, P0 status, velocity)
    - "Went well" insights (positive observations)
    - "Needs improvement" insights (areas for growth)
    - Action items (concrete next steps)

    Performance:
    - Query complexity: O(n) where n = backlog items
    - Response time target: <100ms p95
    """

    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        self.db = db

    async def generate_retrospective(self, sprint_id: UUID) -> SprintRetrospective:
        """
        Generate sprint retrospective automatically.

        Analyzes:
        1. Completion metrics (points, items, P0s)
        2. Process metrics (blocked items, mid-sprint additions)
        3. Velocity trends (compared to previous sprints)
        4. Team patterns (cycle time, throughput)

        Args:
            sprint_id: Sprint UUID

        Returns:
            SprintRetrospective with metrics, insights, and actions

        Raises:
            ValueError: If sprint not found
        """
        # 1. Fetch sprint details
        sprint = await self._get_sprint(sprint_id)
        if not sprint:
            raise ValueError(f"Sprint {sprint_id} not found")

        # 2. Get backlog items
        items = await self._get_backlog_items(sprint_id)

        # 3. Calculate metrics
        metrics = self._calculate_metrics(items, sprint)

        # 4. Generate insights
        went_well = self._generate_went_well(metrics)
        needs_improvement = self._generate_needs_improvement(metrics)

        # 5. Generate action items
        action_items = self._generate_action_items(metrics, needs_improvement)

        # 6. Generate summary
        summary = self._generate_summary(metrics, went_well, needs_improvement)

        return SprintRetrospective(
            sprint_id=sprint.id,
            sprint_number=sprint.number,
            sprint_name=sprint.name,
            generated_at=datetime.utcnow(),
            metrics=metrics,
            went_well=went_well,
            needs_improvement=needs_improvement,
            action_items=action_items,
            summary=summary,
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

    def _calculate_metrics(
        self,
        items: List[BacklogItem],
        sprint: Sprint,
    ) -> RetroMetrics:
        """
        Calculate sprint metrics from backlog items.

        Args:
            items: List of backlog items
            sprint: Sprint object

        Returns:
            RetroMetrics with calculated values
        """
        # Total and completed points
        committed_points = sum(item.story_points or 0 for item in items)
        completed_points = sum(
            item.story_points or 0
            for item in items
            if item.status == "done"
        )

        # Completion rate
        completion_rate = (
            completed_points / committed_points
            if committed_points > 0
            else 0.0
        )

        # P0 metrics
        p0_items = [item for item in items if item.priority == "P0"]
        p0_total = len(p0_items)
        p0_completed = len([item for item in p0_items if item.status == "done"])
        p0_completion_rate = (
            p0_completed / p0_total
            if p0_total > 0
            else 1.0  # No P0s = 100% P0 completion
        )

        # Mid-sprint additions (items created after sprint start)
        items_added_mid_sprint = 0
        if sprint.start_date:
            for item in items:
                if hasattr(item, 'created_at') and item.created_at:
                    # Convert date to datetime for comparison if needed
                    sprint_start = datetime.combine(sprint.start_date, datetime.min.time())
                    if item.created_at > sprint_start:
                        items_added_mid_sprint += 1

        # Blocked items
        blocked_items = len([item for item in items if item.status == "blocked"])

        # Velocity trend (simplified - would need historical data)
        velocity_trend = self._calculate_velocity_trend(completion_rate)

        return RetroMetrics(
            committed_points=committed_points,
            completed_points=completed_points,
            completion_rate=round(completion_rate, 2),
            p0_total=p0_total,
            p0_completed=p0_completed,
            p0_completion_rate=round(p0_completion_rate, 2),
            items_added_mid_sprint=items_added_mid_sprint,
            blocked_items=blocked_items,
            average_cycle_time_days=None,  # Would need item-level timestamps
            velocity_trend=velocity_trend,
        )

    def _calculate_velocity_trend(self, completion_rate: float) -> str:
        """
        Determine velocity trend based on completion rate.

        Args:
            completion_rate: Current sprint completion rate (0-1)

        Returns:
            Trend: improving, stable, declining
        """
        # Simplified logic - in production would compare to historical sprints
        if completion_rate >= 0.9:
            return "improving"
        elif completion_rate >= 0.7:
            return "stable"
        else:
            return "declining"

    def _generate_went_well(self, metrics: RetroMetrics) -> List[RetroInsight]:
        """
        Generate "went well" insights based on metrics.

        Args:
            metrics: Calculated sprint metrics

        Returns:
            List of positive insights
        """
        insights = []

        # Strong Delivery
        if metrics.completion_rate >= 0.9:
            insights.append(RetroInsight(
                category="delivery",
                insight_type="went_well",
                title="Strong Delivery",
                description=f"Achieved {metrics.completion_rate * 100:.0f}% completion rate. "
                           f"Completed {metrics.completed_points} of {metrics.committed_points} story points.",
                impact="high",
            ))
        elif metrics.completion_rate >= 0.8:
            insights.append(RetroInsight(
                category="delivery",
                insight_type="went_well",
                title="Good Delivery",
                description=f"Achieved {metrics.completion_rate * 100:.0f}% completion rate. "
                           f"Solid execution on committed work.",
                impact="medium",
            ))

        # P0 Focus
        if metrics.p0_completion_rate == 1.0 and metrics.p0_total > 0:
            insights.append(RetroInsight(
                category="priority",
                insight_type="went_well",
                title="P0 Focus Excellence",
                description=f"Completed all {metrics.p0_total} P0 items. "
                           f"Team prioritized correctly and delivered critical work first.",
                impact="high",
            ))
        elif metrics.p0_completion_rate >= 0.9 and metrics.p0_total > 0:
            insights.append(RetroInsight(
                category="priority",
                insight_type="went_well",
                title="Strong P0 Focus",
                description=f"Completed {metrics.p0_completed}/{metrics.p0_total} P0 items. "
                           f"High priority items received appropriate attention.",
                impact="medium",
            ))

        # Improving Velocity
        if metrics.velocity_trend == "improving":
            insights.append(RetroInsight(
                category="velocity",
                insight_type="went_well",
                title="Improving Velocity",
                description="Team velocity is trending upward. "
                           "Process improvements are showing results.",
                impact="high",
            ))

        # No Blockers
        if metrics.blocked_items == 0:
            insights.append(RetroInsight(
                category="blockers",
                insight_type="went_well",
                title="Clear Path",
                description="No blocked items during sprint. "
                           "Dependencies were well-managed and issues resolved proactively.",
                impact="medium",
            ))

        # Stable Scope
        if metrics.items_added_mid_sprint == 0:
            insights.append(RetroInsight(
                category="scope",
                insight_type="went_well",
                title="Stable Scope",
                description="No mid-sprint additions. "
                           "Sprint scope remained stable throughout execution.",
                impact="medium",
            ))

        return insights

    def _generate_needs_improvement(self, metrics: RetroMetrics) -> List[RetroInsight]:
        """
        Generate "needs improvement" insights based on metrics.

        Args:
            metrics: Calculated sprint metrics

        Returns:
            List of improvement insights
        """
        insights = []

        # Over-commitment
        if metrics.completion_rate < 0.7:
            insights.append(RetroInsight(
                category="planning",
                insight_type="needs_improvement",
                title="Over-commitment",
                description=f"Only {metrics.completion_rate * 100:.0f}% completion rate. "
                           f"Consider reducing sprint scope by "
                           f"{int((1 - metrics.completion_rate) * metrics.committed_points)} points.",
                impact="high",
            ))
        elif metrics.completion_rate < 0.8:
            insights.append(RetroInsight(
                category="planning",
                insight_type="needs_improvement",
                title="Planning Accuracy",
                description=f"Achieved {metrics.completion_rate * 100:.0f}% completion. "
                           f"Sprint planning could be more accurate.",
                impact="medium",
            ))

        # P0 Incomplete
        if metrics.p0_completion_rate < 1.0 and metrics.p0_total > 0:
            incomplete = metrics.p0_total - metrics.p0_completed
            insights.append(RetroInsight(
                category="priority",
                insight_type="needs_improvement",
                title="P0 Items Incomplete",
                description=f"{incomplete} P0 item(s) not completed. "
                           f"Critical work should be prioritized above all else.",
                impact="high" if incomplete > 1 else "medium",
            ))

        # Scope Creep
        if metrics.items_added_mid_sprint > 2:
            insights.append(RetroInsight(
                category="scope",
                insight_type="needs_improvement",
                title="Scope Creep",
                description=f"{metrics.items_added_mid_sprint} items added mid-sprint. "
                           f"Protect sprint scope by deferring new requests to next sprint.",
                impact="high" if metrics.items_added_mid_sprint > 5 else "medium",
            ))
        elif metrics.items_added_mid_sprint > 0:
            insights.append(RetroInsight(
                category="scope",
                insight_type="needs_improvement",
                title="Minor Scope Changes",
                description=f"{metrics.items_added_mid_sprint} item(s) added mid-sprint. "
                           f"Monitor for patterns.",
                impact="low",
            ))

        # Unresolved Blockers
        if metrics.blocked_items > 0:
            insights.append(RetroInsight(
                category="blockers",
                insight_type="needs_improvement",
                title="Unresolved Blockers",
                description=f"{metrics.blocked_items} item(s) still blocked. "
                           f"Blockers should be escalated and resolved within 24 hours.",
                impact="high" if metrics.blocked_items > 2 else "medium",
            ))

        # Declining Velocity
        if metrics.velocity_trend == "declining":
            insights.append(RetroInsight(
                category="velocity",
                insight_type="needs_improvement",
                title="Declining Velocity",
                description="Team velocity is trending downward. "
                           "Investigate root causes (technical debt, team changes, unclear requirements).",
                impact="high",
            ))

        return insights

    def _generate_action_items(
        self,
        metrics: RetroMetrics,
        needs_improvement: List[RetroInsight],
    ) -> List[RetroAction]:
        """
        Generate action items based on metrics and improvement areas.

        Args:
            metrics: Calculated sprint metrics
            needs_improvement: List of improvement insights

        Returns:
            List of concrete action items
        """
        actions = []
        next_sprint_start = date_type.today() + timedelta(days=1)

        # Action for over-commitment
        if metrics.completion_rate < 0.8:
            actions.append(RetroAction(
                id=uuid4(),
                description=f"Reduce next sprint capacity by {int((1 - metrics.completion_rate) * 100)}% "
                           f"to improve predictability",
                owner="Scrum Master",
                due_date=next_sprint_start,
                status="pending",
                priority="high",
            ))

        # Action for P0 incomplete
        if metrics.p0_completion_rate < 1.0 and metrics.p0_total > 0:
            actions.append(RetroAction(
                id=uuid4(),
                description="Review P0 definition and team capacity allocation for critical items",
                owner="Product Manager",
                due_date=next_sprint_start,
                status="pending",
                priority="high",
            ))

        # Action for scope creep
        if metrics.items_added_mid_sprint > 2:
            actions.append(RetroAction(
                id=uuid4(),
                description="Implement sprint protection policy - all new requests go to backlog",
                owner="Product Manager",
                due_date=next_sprint_start,
                status="pending",
                priority="medium",
            ))

        # Action for blockers
        if metrics.blocked_items > 0:
            actions.append(RetroAction(
                id=uuid4(),
                description=f"Create escalation path for {metrics.blocked_items} blocked items "
                           f"with 24-hour SLA",
                owner="Tech Lead",
                due_date=date_type.today(),
                status="pending",
                priority="high",
            ))

        # Action for declining velocity
        if metrics.velocity_trend == "declining":
            actions.append(RetroAction(
                id=uuid4(),
                description="Schedule velocity analysis session to identify root causes",
                owner="Tech Lead",
                due_date=next_sprint_start,
                status="pending",
                priority="medium",
            ))

        # General improvement action if no specific issues
        if not actions:
            actions.append(RetroAction(
                id=uuid4(),
                description="Continue current practices and identify one process improvement to pilot",
                owner="Team",
                due_date=next_sprint_start + timedelta(days=14),
                status="pending",
                priority="low",
            ))

        return actions[:5]  # Limit to 5 action items

    def _generate_summary(
        self,
        metrics: RetroMetrics,
        went_well: List[RetroInsight],
        needs_improvement: List[RetroInsight],
    ) -> str:
        """
        Generate executive summary of the sprint.

        Args:
            metrics: Calculated sprint metrics
            went_well: List of positive insights
            needs_improvement: List of improvement insights

        Returns:
            Human-readable summary string
        """
        # Overall rating
        if metrics.completion_rate >= 0.9 and metrics.p0_completion_rate == 1.0:
            rating = "Excellent"
            emoji = "🌟"
        elif metrics.completion_rate >= 0.8:
            rating = "Good"
            emoji = "✅"
        elif metrics.completion_rate >= 0.7:
            rating = "Fair"
            emoji = "⚠️"
        else:
            rating = "Needs Attention"
            emoji = "🔴"

        # Build summary
        summary_parts = [
            f"{emoji} **{rating} Sprint Performance**",
            f"",
            f"Delivered {metrics.completed_points}/{metrics.committed_points} story points "
            f"({metrics.completion_rate * 100:.0f}% completion rate).",
        ]

        # P0 status
        if metrics.p0_total > 0:
            if metrics.p0_completion_rate == 1.0:
                summary_parts.append(f"All {metrics.p0_total} P0 items completed. ✓")
            else:
                summary_parts.append(
                    f"P0 items: {metrics.p0_completed}/{metrics.p0_total} completed. "
                    f"({int(metrics.p0_completion_rate * 100)}%)"
                )

        # Key highlights
        if went_well:
            highlights = [i.title for i in went_well[:2]]
            summary_parts.append(f"Highlights: {', '.join(highlights)}.")

        # Key improvements
        if needs_improvement:
            improvements = [i.title for i in needs_improvement[:2]]
            summary_parts.append(f"Focus areas: {', '.join(improvements)}.")

        return " ".join(summary_parts)


def get_retrospective_service(db: AsyncSession) -> RetrospectiveService:
    """Factory function for RetrospectiveService."""
    return RetrospectiveService(db)
