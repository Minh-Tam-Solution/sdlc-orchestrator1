"""
=========================================================================
Sprint Dependency Model
SDLC Orchestrator - Sprint 78 Day 2

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 78 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)

Purpose:
- Track dependencies between sprints (same or cross-project)
- Support circular dependency detection
- Enable dependency graph visualization

Design Reference:
docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
=========================================================================
"""

from __future__ import annotations

import uuid as uuid_module
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
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


# Valid dependency types
DEPENDENCY_TYPES = ["blocks", "requires", "related"]

# Valid dependency statuses
DEPENDENCY_STATUSES = ["pending", "active", "resolved", "cancelled"]


class SprintDependency(Base):
    """
    Sprint-to-sprint dependency model.

    Tracks dependencies between sprints, supporting:
    - Same project dependencies (sprint ordering)
    - Cross-project dependencies (feature dependencies)
    - Dependency graph visualization

    Dependency Types:
        - blocks: Source sprint blocks target sprint (critical)
        - requires: Source requires deliverable from target
        - related: Sprints are related but not blocking

    Status Flow:
        pending -> active -> resolved/cancelled
    """

    __tablename__ = "sprint_dependencies"

    # Primary key
    id: Mapped[uuid_module.UUID] = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid_module.uuid4,
    )

    # Source sprint (the one that depends on another)
    source_sprint_id: Mapped[uuid_module.UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey("sprints.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Target sprint (the one being depended on)
    target_sprint_id: Mapped[uuid_module.UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey("sprints.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Dependency metadata
    dependency_type: Mapped[str] = Column(
        String(20),
        nullable=False,
        default="related",
        comment="Type: blocks, requires, related",
    )

    description: Mapped[Optional[str]] = Column(
        Text,
        nullable=True,
        comment="Description of the dependency",
    )

    # Status tracking
    status: Mapped[str] = Column(
        String(20),
        nullable=False,
        default="pending",
        comment="Status: pending, active, resolved, cancelled",
    )

    # Audit fields
    created_by_id: Mapped[Optional[uuid_module.UUID]] = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    resolved_by_id: Mapped[Optional[uuid_module.UUID]] = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Timestamps
    created_at: Mapped[datetime] = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    resolved_at: Mapped[Optional[datetime]] = Column(
        DateTime,
        nullable=True,
    )

    # Soft delete
    is_deleted: Mapped[bool] = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Relationships
    source_sprint: Mapped["Sprint"] = relationship(
        "Sprint",
        foreign_keys=[source_sprint_id],
        back_populates="outgoing_dependencies",
    )

    target_sprint: Mapped["Sprint"] = relationship(
        "Sprint",
        foreign_keys=[target_sprint_id],
        back_populates="incoming_dependencies",
    )

    created_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    resolved_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[resolved_by_id],
    )

    # Indexes
    __table_args__ = (
        Index("idx_sprint_dep_source", "source_sprint_id"),
        Index("idx_sprint_dep_target", "target_sprint_id"),
        Index("idx_sprint_dep_status", "status"),
        Index("idx_sprint_dep_type", "dependency_type"),
        Index("idx_sprint_dep_source_target", "source_sprint_id", "target_sprint_id", unique=True),
    )

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def is_blocking(self) -> bool:
        """Check if this is a blocking dependency."""
        return self.dependency_type == "blocks" and self.status == "active"

    @property
    def is_resolved(self) -> bool:
        """Check if dependency is resolved."""
        return self.status in ("resolved", "cancelled")

    @property
    def is_cross_project(self) -> bool:
        """Check if dependency spans projects."""
        if self.source_sprint and self.target_sprint:
            return self.source_sprint.project_id != self.target_sprint.project_id
        return False

    # =========================================================================
    # Status Transitions
    # =========================================================================

    def activate(self) -> None:
        """Activate pending dependency."""
        if self.status == "pending":
            self.status = "active"

    def resolve(self, user_id: Optional[uuid_module.UUID] = None) -> None:
        """Mark dependency as resolved."""
        self.status = "resolved"
        self.resolved_at = datetime.utcnow()
        if user_id:
            self.resolved_by_id = user_id

    def cancel(self, user_id: Optional[uuid_module.UUID] = None) -> None:
        """Cancel dependency."""
        self.status = "cancelled"
        self.resolved_at = datetime.utcnow()
        if user_id:
            self.resolved_by_id = user_id

    # =========================================================================
    # Representation
    # =========================================================================

    def __repr__(self) -> str:
        return (
            f"<SprintDependency("
            f"id={self.id}, "
            f"source={self.source_sprint_id}, "
            f"target={self.target_sprint_id}, "
            f"type={self.dependency_type}, "
            f"status={self.status}"
            f")>"
        )
