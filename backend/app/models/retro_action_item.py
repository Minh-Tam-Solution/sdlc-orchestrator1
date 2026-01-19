"""
=========================================================================
Retrospective Action Item Model
SDLC Orchestrator - Sprint 78 Day 1

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 78 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)
Reference: Sprint 78 Technical Design - Retrospective Enhancement

Purpose:
- Track action items generated from sprint retrospectives
- Enable assignment and completion tracking
- Support retrospective comparison across sprints

Design Reference:
docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
=========================================================================
"""

import uuid as uuid_module
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class RetroActionItem(Base):
    """
    Retrospective action item model.

    Tracks action items from sprint retrospectives with:
    - Assignee tracking
    - Status tracking (open, in_progress, completed, cancelled)
    - Priority levels (low, medium, high)
    - Cross-sprint tracking (due_sprint_id)

    Relationships:
    - Sprint (source sprint where item was created)
    - User (assignee)
    - Due Sprint (target sprint for completion)
    """

    __tablename__ = "retro_action_items"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid_module.uuid4,
        index=True,
    )

    # Source sprint (where action was identified)
    sprint_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sprints.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Action item content
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Category from retrospective insight
    category = Column(
        String(50),
        nullable=False,
        default="general",
        comment="Category: delivery, priority, velocity, planning, scope, blockers, team",
    )

    # Priority and status
    priority = Column(
        String(20),
        nullable=False,
        default="medium",
        comment="Priority: low, medium, high",
    )
    status = Column(
        String(20),
        nullable=False,
        default="open",
        index=True,
        comment="Status: open, in_progress, completed, cancelled",
    )

    # Assignment
    assignee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Target sprint for completion (cross-sprint tracking)
    due_sprint_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sprints.id", ondelete="SET NULL"),
        nullable=True,
        comment="Target sprint for completion",
    )

    # Timestamps
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    completed_at = Column(
        DateTime,
        nullable=True,
    )

    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)

    # Relationships
    sprint = relationship(
        "Sprint",
        foreign_keys=[sprint_id],
        back_populates="retro_action_items",
    )
    assignee = relationship(
        "User",
        foreign_keys=[assignee_id],
    )
    due_sprint = relationship(
        "Sprint",
        foreign_keys=[due_sprint_id],
    )

    def __repr__(self) -> str:
        return f"<RetroActionItem(id={self.id}, title='{self.title[:30]}...', status={self.status})>"

    def mark_completed(self) -> None:
        """Mark action item as completed."""
        self.status = "completed"
        self.completed_at = datetime.utcnow()

    def mark_cancelled(self) -> None:
        """Mark action item as cancelled."""
        self.status = "cancelled"

    def assign_to(self, user_id: uuid_module.UUID) -> None:
        """Assign action item to a user."""
        self.assignee_id = user_id
        if self.status == "open":
            self.status = "in_progress"
