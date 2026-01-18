"""
=========================================================================
Burndown Service - Sprint Burndown Chart Data Generation
SDLC Orchestrator - Sprint 77 Day 2

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 77 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)
Reference: Sprint 77 Technical Design - Burndown Charts

Purpose:
- Generate burndown chart data for sprint visualization
- Calculate ideal burndown line (linear from total to 0)
- Calculate actual burndown from completion history
- Support sprint progress tracking and forecasting

Performance Budget:
- Query time: <50ms
- Calculation time: <20ms
- Total response: <100ms p95

Zero Mock Policy: Production-ready implementation with real DB queries
=========================================================================
"""

from datetime import date as date_type, datetime, timedelta
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.backlog_item import BacklogItem
from app.models.sprint import Sprint


# =========================================================================
# Schemas
# =========================================================================


class BurndownPoint(BaseModel):
    """Single point on burndown chart."""

    date: date_type = Field(..., description="Date for this data point")
    points: float = Field(..., description="Story points remaining")
    type: str = Field(..., description="Point type: 'ideal' or 'actual'")

    model_config = ConfigDict(from_attributes=True)


class BurndownChart(BaseModel):
    """Complete burndown chart data."""

    sprint_id: UUID = Field(..., description="Sprint UUID")
    sprint_number: int = Field(..., description="Sprint number")
    sprint_name: str = Field(..., description="Sprint name")
    total_points: int = Field(..., description="Total committed story points")
    start_date: date_type = Field(..., description="Sprint start date")
    end_date: date_type = Field(..., description="Sprint end date")
    ideal: List[BurndownPoint] = Field(
        default_factory=list, description="Ideal burndown line (linear)"
    )
    actual: List[BurndownPoint] = Field(
        default_factory=list, description="Actual burndown line"
    )
    remaining_points: int = Field(
        default=0, description="Current remaining story points"
    )
    completion_rate: float = Field(
        default=0.0, description="Completion rate (0-100)"
    )
    days_elapsed: int = Field(default=0, description="Days since sprint start")
    days_remaining: int = Field(default=0, description="Days until sprint end")
    on_track: bool = Field(
        default=True,
        description="Whether sprint is on track (actual <= ideal)",
    )

    model_config = ConfigDict(from_attributes=True)


# =========================================================================
# Service
# =========================================================================


class BurndownService:
    """
    Sprint burndown chart data service.

    Generates burndown chart data for sprint visualization:
    - Ideal line: Linear progression from total points to 0
    - Actual line: Based on completed items with timestamps

    Performance:
    - Query complexity: O(n) where n = backlog items
    - Response time target: <100ms p95
    """

    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        self.db = db

    async def get_burndown_data(self, sprint_id: UUID) -> BurndownChart:
        """
        Generate burndown chart data for a sprint.

        Algorithm:
        1. Fetch sprint details (start_date, end_date)
        2. Calculate total committed story points
        3. Generate ideal burndown line (linear from total to 0)
        4. Calculate actual burndown from completion history
        5. Return both lines for chart rendering

        Args:
            sprint_id: Sprint UUID

        Returns:
            BurndownChart with ideal and actual burndown lines

        Raises:
            ValueError: If sprint not found or has no dates
        """
        # 1. Fetch sprint details
        sprint = await self._get_sprint(sprint_id)
        if not sprint:
            raise ValueError(f"Sprint {sprint_id} not found")

        if not sprint.start_date or not sprint.end_date:
            raise ValueError(f"Sprint {sprint_id} has no start/end dates")

        # 2. Get backlog items with completion data
        items = await self._get_backlog_items(sprint_id)

        # Calculate totals
        total_points = sum(item.story_points or 0 for item in items)
        completed_points = sum(
            item.story_points or 0
            for item in items
            if item.status == "done"
        )
        remaining_points = total_points - completed_points

        # 3. Generate ideal burndown line
        ideal_line = self._calculate_ideal_burndown(
            total_points=total_points,
            start_date=sprint.start_date,
            end_date=sprint.end_date,
        )

        # 4. Calculate actual burndown
        actual_line = self._calculate_actual_burndown(
            items=items,
            total_points=total_points,
            start_date=sprint.start_date,
            end_date=sprint.end_date,
        )

        # 5. Calculate progress metrics
        today = date_type.today()
        days_elapsed = max(0, (today - sprint.start_date).days) if today >= sprint.start_date else 0
        days_remaining = max(0, (sprint.end_date - today).days) if today <= sprint.end_date else 0

        # Determine if on track (actual <= ideal at current date)
        on_track = self._check_on_track(
            actual_line=actual_line,
            ideal_line=ideal_line,
            current_date=min(today, sprint.end_date),
        )

        # Calculate completion rate
        completion_rate = (completed_points / total_points * 100) if total_points > 0 else 0.0

        return BurndownChart(
            sprint_id=sprint.id,
            sprint_number=sprint.number,
            sprint_name=sprint.name,
            total_points=total_points,
            start_date=sprint.start_date,
            end_date=sprint.end_date,
            ideal=ideal_line,
            actual=actual_line,
            remaining_points=remaining_points,
            completion_rate=round(completion_rate, 1),
            days_elapsed=days_elapsed,
            days_remaining=days_remaining,
            on_track=on_track,
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
            .order_by(BacklogItem.updated_at)
        )
        return list(result.scalars().all())

    def _calculate_ideal_burndown(
        self,
        total_points: int,
        start_date: date_type,
        end_date: date_type,
    ) -> List[BurndownPoint]:
        """
        Calculate ideal burndown line (linear from total to 0).

        Creates a linear progression from total_points at start_date
        to 0 at end_date.

        Args:
            total_points: Total committed story points
            start_date: Sprint start date
            end_date: Sprint end date

        Returns:
            List of BurndownPoint for ideal line
        """
        if total_points == 0:
            return []

        ideal_points: List[BurndownPoint] = []
        duration_days = (end_date - start_date).days
        if duration_days <= 0:
            return [
                BurndownPoint(date=start_date, points=float(total_points), type="ideal"),
                BurndownPoint(date=end_date, points=0.0, type="ideal"),
            ]

        points_per_day = total_points / duration_days

        current_date = start_date
        remaining = float(total_points)

        while current_date <= end_date:
            ideal_points.append(
                BurndownPoint(
                    date=current_date,
                    points=round(remaining, 1),
                    type="ideal",
                )
            )
            current_date += timedelta(days=1)
            remaining = max(0, remaining - points_per_day)

        return ideal_points

    def _calculate_actual_burndown(
        self,
        items: List[BacklogItem],
        total_points: int,
        start_date: date_type,
        end_date: date_type,
    ) -> List[BurndownPoint]:
        """
        Calculate actual burndown from completion history.

        Tracks completed items by date based on their updated_at timestamp
        when status became 'done'.

        Args:
            items: List of backlog items
            total_points: Total committed story points
            start_date: Sprint start date
            end_date: Sprint end date

        Returns:
            List of BurndownPoint for actual line
        """
        if total_points == 0:
            return []

        # Build completion map: date -> points completed that day
        completion_map: dict[date_type, int] = {}
        for item in items:
            if item.status == "done" and item.updated_at:
                # Use the date portion of updated_at as completion date
                completed_date = item.updated_at.date()
                # Clamp to sprint date range
                if completed_date < start_date:
                    completed_date = start_date
                elif completed_date > end_date:
                    completed_date = end_date

                points = item.story_points or 0
                completion_map[completed_date] = completion_map.get(completed_date, 0) + points

        # Build actual burndown line
        actual_points: List[BurndownPoint] = []
        today = date_type.today()
        end_tracking_date = min(today, end_date)

        current_date = start_date
        remaining = float(total_points)

        while current_date <= end_tracking_date:
            # Subtract points completed on this date
            if current_date in completion_map:
                remaining = max(0, remaining - completion_map[current_date])

            actual_points.append(
                BurndownPoint(
                    date=current_date,
                    points=round(remaining, 1),
                    type="actual",
                )
            )
            current_date += timedelta(days=1)

        return actual_points

    def _check_on_track(
        self,
        actual_line: List[BurndownPoint],
        ideal_line: List[BurndownPoint],
        current_date: date_type,
    ) -> bool:
        """
        Check if sprint is on track.

        Sprint is on track if actual remaining points <= ideal remaining
        points at the current date.

        Args:
            actual_line: Actual burndown points
            ideal_line: Ideal burndown points
            current_date: Date to check

        Returns:
            True if on track, False otherwise
        """
        if not actual_line or not ideal_line:
            return True

        # Find points at current date for both lines
        actual_at_date = None
        ideal_at_date = None

        for point in actual_line:
            if point.date == current_date:
                actual_at_date = point.points
                break
            if point.date < current_date:
                actual_at_date = point.points

        for point in ideal_line:
            if point.date == current_date:
                ideal_at_date = point.points
                break
            if point.date < current_date:
                ideal_at_date = point.points

        if actual_at_date is None or ideal_at_date is None:
            return True

        # On track if actual <= ideal (fewer remaining points is better)
        return actual_at_date <= ideal_at_date


def get_burndown_service(db: AsyncSession) -> BurndownService:
    """Factory function for BurndownService."""
    return BurndownService(db)
