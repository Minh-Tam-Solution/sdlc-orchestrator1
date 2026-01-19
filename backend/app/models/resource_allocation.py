"""
=========================================================================
Resource Allocation Model
SDLC Orchestrator - Sprint 78 Day 3

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 78 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)

Purpose:
- Track team member allocation across sprints
- Support capacity planning and conflict detection
- Enable resource utilization optimization

Design Reference:
docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
=========================================================================
"""

from __future__ import annotations

import uuid as uuid_module
from datetime import datetime, date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Column,
    DateTime,
    Date,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.sprint import Sprint
    from app.models.user import User


# Valid roles for allocation
ALLOCATION_ROLES = [
    "developer",
    "qa",
    "designer",
    "pm",
    "tech_lead",
    "devops",
    "analyst",
    "other",
]


class ResourceAllocation(Base):
    """
    Resource allocation model for sprint capacity planning.

    Tracks team member allocation to sprints with:
    - Allocation percentage (0-100%)
    - Role-based assignments
    - Date range for partial allocations
    - Conflict detection support

    Usage:
        - Full allocation: user allocated 100% to one sprint
        - Split allocation: user allocated 50% to two sprints
        - Partial period: user allocated 100% for first week only
    """

    __tablename__ = "resource_allocations"

    # Primary key
    id: Mapped[uuid_module.UUID] = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid_module.uuid4,
    )

    # Foreign keys
    sprint_id: Mapped[uuid_module.UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey("sprints.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[uuid_module.UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Allocation details
    allocation_percentage: Mapped[int] = Column(
        Integer,
        nullable=False,
        default=100,
        comment="Allocation percentage (0-100)",
    )

    role: Mapped[str] = Column(
        String(50),
        nullable=False,
        default="developer",
        comment="Role: developer, qa, designer, pm, tech_lead, devops, analyst, other",
    )

    # Date range (defaults to sprint dates if not specified)
    start_date: Mapped[date] = Column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date] = Column(
        Date,
        nullable=False,
    )

    # Notes
    notes: Mapped[Optional[str]] = Column(
        Text,
        nullable=True,
    )

    # Audit
    created_by_id: Mapped[Optional[uuid_module.UUID]] = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[datetime] = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Soft delete
    is_deleted: Mapped[bool] = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Relationships
    sprint: Mapped["Sprint"] = relationship(
        "Sprint",
        backref="resource_allocations",
    )

    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
        backref="sprint_allocations",
    )

    created_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    # Indexes
    __table_args__ = (
        Index("idx_resource_alloc_sprint", "sprint_id"),
        Index("idx_resource_alloc_user", "user_id"),
        Index("idx_resource_alloc_dates", "start_date", "end_date"),
        Index("idx_resource_alloc_role", "role"),
        # Unique constraint: one allocation per user-sprint pair
        Index("idx_resource_alloc_user_sprint", "user_id", "sprint_id", unique=True),
    )

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def duration_days(self) -> int:
        """Calculate allocation duration in days."""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0

    @property
    def allocated_days(self) -> float:
        """Calculate effective allocated days (considering percentage)."""
        return self.duration_days * (self.allocation_percentage / 100)

    @property
    def is_full_allocation(self) -> bool:
        """Check if this is a full (100%) allocation."""
        return self.allocation_percentage == 100

    @property
    def is_over_allocated(self) -> bool:
        """Check if allocation exceeds 100% (should not happen with validation)."""
        return self.allocation_percentage > 100

    # =========================================================================
    # Date Range Methods
    # =========================================================================

    def overlaps_with(self, other_start: date, other_end: date) -> bool:
        """Check if this allocation overlaps with a date range."""
        return self.start_date <= other_end and self.end_date >= other_start

    def get_overlap_days(self, other_start: date, other_end: date) -> int:
        """Calculate number of overlapping days with a date range."""
        if not self.overlaps_with(other_start, other_end):
            return 0

        overlap_start = max(self.start_date, other_start)
        overlap_end = min(self.end_date, other_end)
        return (overlap_end - overlap_start).days + 1

    # =========================================================================
    # Representation
    # =========================================================================

    def __repr__(self) -> str:
        return (
            f"<ResourceAllocation("
            f"id={self.id}, "
            f"user={self.user_id}, "
            f"sprint={self.sprint_id}, "
            f"allocation={self.allocation_percentage}%, "
            f"role={self.role}"
            f")>"
        )
