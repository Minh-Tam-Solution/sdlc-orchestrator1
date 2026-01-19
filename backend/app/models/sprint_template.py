"""
=========================================================================
Sprint Template Model
SDLC Orchestrator - Sprint 78 Day 4

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 78 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)

Purpose:
- Reusable sprint configuration templates
- Standard sprint types (2-week, feature, bugfix, release)
- Default backlog structure for quick setup

Design Reference:
docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
=========================================================================
"""

from __future__ import annotations

import uuid as uuid_module
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List, Any

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    Boolean,
    Integer,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.team import Team
    from app.models.user import User


# Valid template types
TEMPLATE_TYPES = ["standard", "feature", "bugfix", "release", "custom"]


class SprintTemplate(Base):
    """
    Reusable sprint configuration template.

    Use cases:
    - 2-week standard sprint template
    - Feature sprint template (focused on new features)
    - Bug-fix sprint template (focused on bug resolution)
    - Release sprint template (focused on deployment prep)

    Backlog Structure JSON format:
    [
        {
            "title": "Sprint Planning",
            "type": "task",
            "priority": "P0",
            "story_points": 1,
            "description": "Sprint planning meeting"
        },
        ...
    ]
    """

    __tablename__ = "sprint_templates"

    # Primary key
    id: Mapped[uuid_module.UUID] = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid_module.uuid4,
    )

    # Template identification
    name: Mapped[str] = Column(
        String(100),
        nullable=False,
        comment="Template name (e.g., '2-Week Sprint')",
    )

    description: Mapped[Optional[str]] = Column(
        Text,
        nullable=True,
        comment="Template description",
    )

    template_type: Mapped[str] = Column(
        String(20),
        nullable=False,
        default="standard",
        comment="Type: standard, feature, bugfix, release, custom",
    )

    # Sprint configuration
    duration_days: Mapped[int] = Column(
        Integer,
        nullable=False,
        default=10,
        comment="Default sprint duration in days",
    )

    default_capacity_points: Mapped[int] = Column(
        Integer,
        nullable=False,
        default=40,
        comment="Default story points capacity",
    )

    # Default backlog structure
    backlog_structure: Mapped[Optional[List[Any]]] = Column(
        JSON,
        nullable=True,
        comment="List of default backlog items",
    )

    # Gate configuration
    gates_enabled: Mapped[bool] = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Enable G-Sprint/G-Sprint-Close gates",
    )

    # Default sprint goal template
    goal_template: Mapped[Optional[str]] = Column(
        Text,
        nullable=True,
        comment="Template for sprint goal (supports placeholders)",
    )

    # Ownership
    team_id: Mapped[Optional[uuid_module.UUID]] = Column(
        UUID(as_uuid=True),
        ForeignKey("teams.id", ondelete="SET NULL"),
        nullable=True,
        comment="Team-specific template (null = org-wide)",
    )

    is_public: Mapped[bool] = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Available to all teams",
    )

    is_default: Mapped[bool] = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Default template for new sprints",
    )

    # Usage tracking
    usage_count: Mapped[int] = Column(
        Integer,
        default=0,
        nullable=False,
        comment="Number of sprints created from this template",
    )

    # Audit fields
    created_by_id: Mapped[Optional[uuid_module.UUID]] = Column(
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
    team: Mapped[Optional["Team"]] = relationship(
        "Team",
        foreign_keys=[team_id],
    )

    created_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    # Indexes
    __table_args__ = (
        Index("idx_sprint_template_team", "team_id"),
        Index("idx_sprint_template_type", "template_type"),
        Index("idx_sprint_template_public", "is_public"),
        Index("idx_sprint_template_default", "is_default"),
    )

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def backlog_item_count(self) -> int:
        """Count of items in backlog structure."""
        if self.backlog_structure:
            return len(self.backlog_structure)
        return 0

    @property
    def total_story_points(self) -> int:
        """Total story points in backlog structure."""
        if not self.backlog_structure:
            return 0
        return sum(
            item.get("story_points", 0)
            for item in self.backlog_structure
        )

    # =========================================================================
    # Methods
    # =========================================================================

    def increment_usage(self) -> None:
        """Increment usage count when template is applied."""
        self.usage_count = (self.usage_count or 0) + 1

    def add_backlog_item(
        self,
        title: str,
        item_type: str,
        priority: str = "P2",
        story_points: int = 0,
        description: Optional[str] = None,
    ) -> None:
        """Add item to backlog structure."""
        if not self.backlog_structure:
            self.backlog_structure = []

        self.backlog_structure.append({
            "title": title,
            "type": item_type,
            "priority": priority,
            "story_points": story_points,
            "description": description,
        })

    # =========================================================================
    # Representation
    # =========================================================================

    def __repr__(self) -> str:
        return (
            f"<SprintTemplate("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"type={self.template_type}, "
            f"duration={self.duration_days}d"
            f")>"
        )
