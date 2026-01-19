"""
=========================================================================
Resource Allocation Service
SDLC Orchestrator - Sprint 78 Day 3

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 78 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)

Purpose:
- Manage team member allocation to sprints
- Calculate team and user capacity
- Detect allocation conflicts
- Generate resource heatmaps

Design Reference:
docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
=========================================================================
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import List, Optional, Dict, Set
from uuid import UUID

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.resource_allocation import ResourceAllocation
from app.models.sprint import Sprint
from app.models.user import User
from app.models.team import Team
from app.models.team_member import TeamMember
from app.schemas.resource_allocation import (
    UserCapacity,
    TeamCapacity,
    SprintCapacity,
    AllocationConflict,
    ConflictCheckResult,
    ResourceHeatmapCell,
    ResourceHeatmap,
)


# Constants
HOURS_PER_DAY = 8
WORKING_DAYS_PER_WEEK = 5


class ResourceAllocationService:
    """
    Service for managing resource allocations.

    Features:
    - CRUD operations for allocations
    - Capacity calculation (user, team, sprint)
    - Conflict detection
    - Resource heatmap generation
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    # =========================================================================
    # Allocation CRUD
    # =========================================================================

    async def create_allocation(
        self,
        sprint_id: UUID,
        user_id: UUID,
        allocation_percentage: int,
        role: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        notes: Optional[str] = None,
        created_by_id: Optional[UUID] = None,
    ) -> ResourceAllocation:
        """
        Create a new resource allocation.

        Args:
            sprint_id: Sprint to allocate to
            user_id: User being allocated
            allocation_percentage: Percentage (1-100)
            role: Role for this allocation
            start_date: Optional start (defaults to sprint start)
            end_date: Optional end (defaults to sprint end)
            notes: Optional notes
            created_by_id: User creating the allocation

        Returns:
            Created ResourceAllocation

        Raises:
            ValueError: If validation fails or conflict detected
        """
        # Get sprint
        sprint = await self._get_sprint(sprint_id)
        if not sprint:
            raise ValueError(f"Sprint {sprint_id} not found")

        # Verify user exists
        user = await self._get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Set dates to sprint dates if not provided
        if not start_date:
            start_date = sprint.start_date
        if not end_date:
            end_date = sprint.end_date

        # Validate date range
        if start_date > end_date:
            raise ValueError("Start date must be before end date")

        if start_date < sprint.start_date or end_date > sprint.end_date:
            raise ValueError("Allocation dates must be within sprint dates")

        # Check for existing allocation
        existing = await self._get_existing_allocation(sprint_id, user_id)
        if existing:
            raise ValueError("User already allocated to this sprint")

        # Check for conflicts (over-allocation)
        conflicts = await self.detect_conflicts(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            new_percentage=allocation_percentage,
            exclude_sprint_id=None,
        )

        if conflicts.has_conflicts:
            conflict_msg = "; ".join([c.message for c in conflicts.conflicts])
            raise ValueError(f"Allocation conflict: {conflict_msg}")

        # Create allocation
        allocation = ResourceAllocation(
            sprint_id=sprint_id,
            user_id=user_id,
            allocation_percentage=allocation_percentage,
            role=role,
            start_date=start_date,
            end_date=end_date,
            notes=notes,
            created_by_id=created_by_id,
        )

        self.db.add(allocation)
        await self.db.commit()
        await self.db.refresh(allocation)

        return allocation

    async def get_allocation(self, allocation_id: UUID) -> Optional[ResourceAllocation]:
        """Get allocation by ID."""
        result = await self.db.execute(
            select(ResourceAllocation)
            .options(
                selectinload(ResourceAllocation.sprint),
                selectinload(ResourceAllocation.user),
            )
            .where(
                ResourceAllocation.id == allocation_id,
                ResourceAllocation.is_deleted == False,
            )
        )
        return result.scalar_one_or_none()

    async def update_allocation(
        self,
        allocation_id: UUID,
        allocation_percentage: Optional[int] = None,
        role: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        notes: Optional[str] = None,
    ) -> Optional[ResourceAllocation]:
        """Update an allocation."""
        allocation = await self.get_allocation(allocation_id)
        if not allocation:
            return None

        # Prepare new values
        new_percentage = allocation_percentage if allocation_percentage is not None else allocation.allocation_percentage
        new_start = start_date if start_date is not None else allocation.start_date
        new_end = end_date if end_date is not None else allocation.end_date

        # Validate dates
        if new_start > new_end:
            raise ValueError("Start date must be before end date")

        # Check for conflicts with new values
        conflicts = await self.detect_conflicts(
            user_id=allocation.user_id,
            start_date=new_start,
            end_date=new_end,
            new_percentage=new_percentage,
            exclude_sprint_id=allocation.sprint_id,
        )

        if conflicts.has_conflicts:
            conflict_msg = "; ".join([c.message for c in conflicts.conflicts])
            raise ValueError(f"Allocation conflict: {conflict_msg}")

        # Update fields
        if allocation_percentage is not None:
            allocation.allocation_percentage = allocation_percentage
        if role is not None:
            allocation.role = role
        if start_date is not None:
            allocation.start_date = start_date
        if end_date is not None:
            allocation.end_date = end_date
        if notes is not None:
            allocation.notes = notes

        await self.db.commit()
        await self.db.refresh(allocation)

        return allocation

    async def delete_allocation(self, allocation_id: UUID) -> bool:
        """Soft delete an allocation."""
        allocation = await self.get_allocation(allocation_id)
        if not allocation:
            return False

        allocation.is_deleted = True
        await self.db.commit()
        return True

    # =========================================================================
    # Query Methods
    # =========================================================================

    async def get_sprint_allocations(
        self,
        sprint_id: UUID,
    ) -> List[ResourceAllocation]:
        """Get all allocations for a sprint."""
        result = await self.db.execute(
            select(ResourceAllocation)
            .options(
                selectinload(ResourceAllocation.user),
            )
            .where(
                ResourceAllocation.sprint_id == sprint_id,
                ResourceAllocation.is_deleted == False,
            )
            .order_by(ResourceAllocation.role)
        )
        return list(result.scalars().all())

    async def get_user_allocations(
        self,
        user_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[ResourceAllocation]:
        """Get allocations for a user, optionally filtered by date range."""
        conditions = [
            ResourceAllocation.user_id == user_id,
            ResourceAllocation.is_deleted == False,
        ]

        if start_date:
            conditions.append(ResourceAllocation.end_date >= start_date)
        if end_date:
            conditions.append(ResourceAllocation.start_date <= end_date)

        result = await self.db.execute(
            select(ResourceAllocation)
            .options(
                selectinload(ResourceAllocation.sprint),
            )
            .where(*conditions)
            .order_by(ResourceAllocation.start_date)
        )
        return list(result.scalars().all())

    # =========================================================================
    # Capacity Calculation
    # =========================================================================

    async def calculate_user_capacity(
        self,
        user_id: UUID,
        start_date: date,
        end_date: date,
    ) -> UserCapacity:
        """
        Calculate capacity for a user in a date range.

        Args:
            user_id: User UUID
            start_date: Start of period
            end_date: End of period

        Returns:
            UserCapacity with utilization details
        """
        user = await self._get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Calculate working days
        working_days = self._count_working_days(start_date, end_date)

        # Get allocations in period
        allocations = await self.get_user_allocations(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        # Calculate allocated days
        allocated_days = 0.0
        for alloc in allocations:
            # Calculate overlap with period
            overlap_start = max(alloc.start_date, start_date)
            overlap_end = min(alloc.end_date, end_date)
            overlap_days = self._count_working_days(overlap_start, overlap_end)
            allocated_days += overlap_days * (alloc.allocation_percentage / 100)

        available_days = max(0, working_days - allocated_days)
        utilization = (allocated_days / working_days * 100) if working_days > 0 else 0

        return UserCapacity(
            user_id=user_id,
            user_name=user.full_name or user.username,
            user_email=user.email,
            total_days=working_days,
            allocated_days=round(allocated_days, 1),
            available_days=round(available_days, 1),
            utilization_rate=round(utilization, 1),
            allocations=[self._serialize_allocation(a) for a in allocations],
        )

    async def calculate_team_capacity(
        self,
        team_id: UUID,
        start_date: date,
        end_date: date,
    ) -> TeamCapacity:
        """
        Calculate capacity for a team in a date range.

        Args:
            team_id: Team UUID
            start_date: Start of period
            end_date: End of period

        Returns:
            TeamCapacity with member breakdown
        """
        # Get team
        team_result = await self.db.execute(
            select(Team).where(Team.id == team_id)
        )
        team = team_result.scalar_one_or_none()
        if not team:
            raise ValueError(f"Team {team_id} not found")

        # Get team members
        members_result = await self.db.execute(
            select(TeamMember)
            .options(selectinload(TeamMember.user))
            .where(
                TeamMember.team_id == team_id,
                TeamMember.is_active == True,
            )
        )
        team_members = members_result.scalars().all()

        # Calculate capacity for each member
        working_days = self._count_working_days(start_date, end_date)
        total_hours = 0.0
        allocated_hours = 0.0
        members = []
        by_role: Dict[str, Dict] = {}

        for tm in team_members:
            member_capacity = await self.calculate_user_capacity(
                user_id=tm.user_id,
                start_date=start_date,
                end_date=end_date,
            )
            members.append(member_capacity)

            member_hours = working_days * HOURS_PER_DAY
            total_hours += member_hours
            allocated_hours += member_capacity.allocated_days * HOURS_PER_DAY

            # Aggregate by role
            role = tm.role or "member"
            if role not in by_role:
                by_role[role] = {"total_hours": 0, "allocated_hours": 0, "count": 0}
            by_role[role]["total_hours"] += member_hours
            by_role[role]["allocated_hours"] += member_capacity.allocated_days * HOURS_PER_DAY
            by_role[role]["count"] += 1

        available_hours = max(0, total_hours - allocated_hours)
        utilization = (allocated_hours / total_hours * 100) if total_hours > 0 else 0

        return TeamCapacity(
            team_id=team_id,
            team_name=team.name,
            start_date=start_date,
            end_date=end_date,
            total_members=len(team_members),
            total_capacity_hours=round(total_hours, 1),
            allocated_hours=round(allocated_hours, 1),
            available_hours=round(available_hours, 1),
            utilization_rate=round(utilization, 1),
            members=members,
            by_role=by_role,
        )

    async def calculate_sprint_capacity(
        self,
        sprint_id: UUID,
    ) -> SprintCapacity:
        """
        Calculate capacity for a sprint.

        Args:
            sprint_id: Sprint UUID

        Returns:
            SprintCapacity with allocation breakdown
        """
        sprint = await self._get_sprint(sprint_id)
        if not sprint:
            raise ValueError(f"Sprint {sprint_id} not found")

        allocations = await self.get_sprint_allocations(sprint_id)

        working_days = self._count_working_days(sprint.start_date, sprint.end_date)
        total_hours = 0.0
        allocated_hours = 0.0
        by_role: Dict[str, Dict] = {}
        alloc_details = []

        for alloc in allocations:
            alloc_days = self._count_working_days(alloc.start_date, alloc.end_date)
            alloc_hours = alloc_days * HOURS_PER_DAY * (alloc.allocation_percentage / 100)

            total_hours += working_days * HOURS_PER_DAY
            allocated_hours += alloc_hours

            # By role
            role = alloc.role
            if role not in by_role:
                by_role[role] = {"hours": 0, "count": 0}
            by_role[role]["hours"] += alloc_hours
            by_role[role]["count"] += 1

            # Details
            alloc_details.append({
                **self._serialize_allocation(alloc),
                "user_name": alloc.user.full_name or alloc.user.username if alloc.user else None,
                "user_email": alloc.user.email if alloc.user else None,
                "sprint_number": sprint.number,
                "sprint_name": sprint.name,
                "project_id": sprint.project_id,
                "project_name": None,
            })

        available = max(0, total_hours - allocated_hours)
        utilization = (allocated_hours / total_hours * 100) if total_hours > 0 else 0

        return SprintCapacity(
            sprint_id=sprint_id,
            sprint_number=sprint.number,
            sprint_name=sprint.name or f"Sprint {sprint.number}",
            start_date=sprint.start_date,
            end_date=sprint.end_date,
            team_size=len(allocations),
            total_capacity_hours=round(total_hours, 1),
            allocated_hours=round(allocated_hours, 1),
            available_hours=round(available, 1),
            utilization_rate=round(utilization, 1),
            by_role=by_role,
            allocations=alloc_details,
        )

    # =========================================================================
    # Conflict Detection
    # =========================================================================

    async def detect_conflicts(
        self,
        user_id: UUID,
        start_date: date,
        end_date: date,
        new_percentage: int,
        exclude_sprint_id: Optional[UUID] = None,
    ) -> ConflictCheckResult:
        """
        Detect allocation conflicts for a user.

        Args:
            user_id: User to check
            start_date: Start of new allocation
            end_date: End of new allocation
            new_percentage: Percentage of new allocation
            exclude_sprint_id: Sprint to exclude (for updates)

        Returns:
            ConflictCheckResult with detected conflicts
        """
        # Get overlapping allocations
        conditions = [
            ResourceAllocation.user_id == user_id,
            ResourceAllocation.is_deleted == False,
            ResourceAllocation.end_date >= start_date,
            ResourceAllocation.start_date <= end_date,
        ]

        if exclude_sprint_id:
            conditions.append(ResourceAllocation.sprint_id != exclude_sprint_id)

        result = await self.db.execute(
            select(ResourceAllocation)
            .options(selectinload(ResourceAllocation.sprint))
            .where(*conditions)
        )
        overlapping = list(result.scalars().all())

        conflicts = []
        warnings = []

        if overlapping:
            # Calculate total allocation for each day
            current_date = start_date
            while current_date <= end_date:
                day_total = new_percentage

                for alloc in overlapping:
                    if alloc.start_date <= current_date <= alloc.end_date:
                        day_total += alloc.allocation_percentage

                if day_total > 100:
                    # Build conflict info
                    sprint_names = [
                        alloc.sprint.name or f"Sprint {alloc.sprint.number}"
                        for alloc in overlapping
                        if alloc.start_date <= current_date <= alloc.end_date
                    ]

                    user = await self._get_user(user_id)
                    conflicts.append(
                        AllocationConflict(
                            user_id=user_id,
                            user_name=user.full_name or user.username if user else "Unknown",
                            conflict_type="over_allocation",
                            total_allocation=day_total,
                            conflicting_sprints=sprint_names,
                            conflicting_dates=str(current_date),
                            message=f"Over-allocated on {current_date}: {day_total}% (max 100%)",
                        )
                    )
                    break  # One conflict is enough

                current_date += timedelta(days=1)

        # Add warnings for high utilization
        if not conflicts:
            total_with_new = sum(a.allocation_percentage for a in overlapping) + new_percentage
            if total_with_new > 80:
                warnings.append(
                    f"User will be at {total_with_new}% utilization during overlapping period"
                )

        return ConflictCheckResult(
            has_conflicts=len(conflicts) > 0,
            conflicts=conflicts,
            warnings=warnings,
        )

    # =========================================================================
    # Resource Heatmap
    # =========================================================================

    async def generate_heatmap(
        self,
        project_id: UUID,
        sprint_ids: Optional[List[UUID]] = None,
    ) -> ResourceHeatmap:
        """
        Generate resource allocation heatmap for visualization.

        Args:
            project_id: Project UUID
            sprint_ids: Optional list of specific sprints

        Returns:
            ResourceHeatmap with cells for each user-sprint combination
        """
        # Get sprints
        sprint_conditions = [Sprint.project_id == project_id]
        if sprint_ids:
            sprint_conditions.append(Sprint.id.in_(sprint_ids))

        sprints_result = await self.db.execute(
            select(Sprint)
            .where(*sprint_conditions)
            .order_by(Sprint.number)
        )
        sprints = list(sprints_result.scalars().all())

        if not sprints:
            return ResourceHeatmap(users=[], sprints=[], cells=[], total_conflicts=0)

        # Get all users with allocations to these sprints
        alloc_result = await self.db.execute(
            select(ResourceAllocation)
            .options(
                selectinload(ResourceAllocation.user),
                selectinload(ResourceAllocation.sprint),
            )
            .where(
                ResourceAllocation.sprint_id.in_([s.id for s in sprints]),
                ResourceAllocation.is_deleted == False,
            )
        )
        allocations = list(alloc_result.scalars().all())

        # Build user list
        users_dict: Dict[UUID, dict] = {}
        for alloc in allocations:
            if alloc.user_id not in users_dict and alloc.user:
                users_dict[alloc.user_id] = {
                    "id": str(alloc.user_id),
                    "name": alloc.user.full_name or alloc.user.username,
                    "email": alloc.user.email,
                }

        # Build sprint list
        sprints_list = [
            {
                "id": str(s.id),
                "number": s.number,
                "name": s.name or f"Sprint {s.number}",
                "start_date": str(s.start_date),
                "end_date": str(s.end_date),
            }
            for s in sprints
        ]

        # Build cells
        cells = []
        conflict_count = 0
        alloc_map: Dict[tuple, ResourceAllocation] = {
            (a.user_id, a.sprint_id): a for a in allocations
        }

        for user_id, user_info in users_dict.items():
            for sprint in sprints:
                alloc = alloc_map.get((user_id, sprint.id))

                if alloc:
                    percentage = alloc.allocation_percentage
                    role = alloc.role

                    if percentage > 100:
                        cell_status = "over_allocated"
                        conflict_count += 1
                    elif percentage == 100:
                        cell_status = "full"
                    elif percentage > 0:
                        cell_status = "partial"
                    else:
                        cell_status = "available"
                else:
                    percentage = 0
                    role = ""
                    cell_status = "available"

                cells.append(
                    ResourceHeatmapCell(
                        user_id=user_id,
                        user_name=user_info["name"],
                        sprint_id=sprint.id,
                        sprint_number=sprint.number,
                        allocation_percentage=percentage,
                        role=role,
                        status=cell_status,
                    )
                )

        return ResourceHeatmap(
            users=list(users_dict.values()),
            sprints=sprints_list,
            cells=cells,
            total_conflicts=conflict_count,
        )

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _count_working_days(self, start: date, end: date) -> int:
        """Count working days (Mon-Fri) between dates."""
        if start > end:
            return 0

        count = 0
        current = start
        while current <= end:
            if current.weekday() < 5:  # Monday = 0, Friday = 4
                count += 1
            current += timedelta(days=1)
        return count

    async def _get_sprint(self, sprint_id: UUID) -> Optional[Sprint]:
        """Get sprint by ID."""
        result = await self.db.execute(
            select(Sprint).where(Sprint.id == sprint_id)
        )
        return result.scalar_one_or_none()

    async def _get_user(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def _get_existing_allocation(
        self,
        sprint_id: UUID,
        user_id: UUID,
    ) -> Optional[ResourceAllocation]:
        """Check if allocation already exists."""
        result = await self.db.execute(
            select(ResourceAllocation).where(
                ResourceAllocation.sprint_id == sprint_id,
                ResourceAllocation.user_id == user_id,
                ResourceAllocation.is_deleted == False,
            )
        )
        return result.scalar_one_or_none()

    def _serialize_allocation(self, alloc: ResourceAllocation) -> dict:
        """Serialize allocation to dict."""
        return {
            "id": alloc.id,
            "sprint_id": alloc.sprint_id,
            "user_id": alloc.user_id,
            "allocation_percentage": alloc.allocation_percentage,
            "role": alloc.role,
            "start_date": alloc.start_date,
            "end_date": alloc.end_date,
            "notes": alloc.notes,
            "created_by_id": alloc.created_by_id,
            "created_at": alloc.created_at,
            "updated_at": alloc.updated_at,
        }


def get_resource_allocation_service(db: AsyncSession) -> ResourceAllocationService:
    """Factory function to create ResourceAllocationService."""
    return ResourceAllocationService(db)
