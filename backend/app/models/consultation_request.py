"""
=========================================================================
Consultation Request Model - CRP Database Tables
SDLC Orchestrator - Sprint 101 (Risk-Based Planning Trigger)

Version: 1.0.0
Date: January 23, 2026
Status: ACTIVE - Sprint 101 Implementation
Authority: Backend Lead + CTO Approved
Reference: docs/04-build/02-Sprint-Plans/SPRINT-101-DESIGN.md
Reference: SDLC 5.2.0 AI Governance - Consultation Request Protocol

Purpose:
- Store consultation requests for high-risk changes
- Track human review workflow (assign, review, resolve)
- Maintain audit trail for compliance

Tables:
- consultation_requests: Main CRP records
- consultation_comments: Discussion thread for each consultation

Security Standards:
- Row-Level Security (RLS) for multi-tenancy
- Audit trail with timestamps
- Immutable resolution records

Zero Mock Policy: Real SQLAlchemy model with all fields
=========================================================================
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ConsultationRequest(Base):
    """
    Consultation Request model for CRP (Consultation Request Protocol).

    Purpose:
        - Enable human oversight for high-risk AI-proposed changes
        - Track consultation workflow from creation to resolution
        - Link to risk analysis that triggered the consultation

    Fields:
        - id: UUID primary key
        - project_id: Foreign key to Project
        - pr_id: Pull request reference (optional)
        - risk_analysis_id: ID of triggering risk analysis
        - risk_analysis: JSONB storing the full RiskAnalysis object
        - title: Consultation title
        - description: Detailed description
        - priority: low/medium/high/urgent
        - required_expertise: List of expertise areas needed
        - status: pending/in_review/approved/rejected/cancelled/expired
        - requester_id: User who created the request
        - assigned_reviewer_id: Assigned reviewer
        - resolution_notes: Notes explaining resolution
        - conditions: Conditions for approval
        - resolved_at: Resolution timestamp
        - resolved_by_id: User who resolved

    Relationships:
        - project: Many-to-One with Project model
        - requester: Many-to-One with User model
        - reviewer: Many-to-One with User model
        - resolver: Many-to-One with User model
        - comments: One-to-Many with ConsultationComment

    Usage Example:
        consultation = ConsultationRequest(
            project_id=project.id,
            risk_analysis_id=analysis.id,
            risk_analysis=analysis.model_dump(),
            title="High-risk auth changes",
            description="Changes to authentication flow...",
            priority="high",
            requester_id=user.id
        )
        session.add(consultation)
        session.commit()
    """

    __tablename__ = "consultation_requests"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Project Association
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # External References
    pr_id = Column(
        String(100),
        nullable=True,
        index=True,
        comment="Pull request ID or reference",
    )

    # Risk Analysis Link
    risk_analysis_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="ID of the risk analysis that triggered CRP",
    )
    risk_analysis = Column(
        JSONB,
        nullable=False,
        comment="Full RiskAnalysis object as JSON",
    )

    # Consultation Details
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(
        String(20),
        nullable=False,
        default="medium",
        index=True,
        comment="Priority: low, medium, high, urgent",
    )
    required_expertise = Column(
        ARRAY(String),
        nullable=False,
        default=["general"],
        comment="Required reviewer expertise areas",
    )
    diff_url = Column(
        String(500),
        nullable=True,
        comment="URL to view the diff (GitHub PR URL)",
    )

    # Status
    status = Column(
        String(20),
        nullable=False,
        default="pending",
        index=True,
        comment="Status: pending, in_review, approved, rejected, cancelled, expired",
    )

    # Participants
    requester_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="User who created the request",
    )
    assigned_reviewer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Assigned reviewer",
    )
    assigned_at = Column(
        DateTime,
        nullable=True,
        comment="When reviewer was assigned",
    )

    # Resolution
    resolution_notes = Column(
        Text,
        nullable=True,
        comment="Notes explaining the resolution",
    )
    conditions = Column(
        ARRAY(String),
        nullable=True,
        comment="Conditions for approval",
    )
    resolved_at = Column(
        DateTime,
        nullable=True,
        index=True,
        comment="When consultation was resolved",
    )
    resolved_by_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="User who resolved the consultation",
    )

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    project = relationship("Project", backref="consultation_requests")
    requester = relationship("User", foreign_keys=[requester_id], backref="requested_consultations")
    reviewer = relationship("User", foreign_keys=[assigned_reviewer_id], backref="assigned_consultations")
    resolver = relationship("User", foreign_keys=[resolved_by_id], backref="resolved_consultations")
    comments = relationship(
        "ConsultationComment",
        back_populates="consultation",
        cascade="all, delete-orphan",
        order_by="ConsultationComment.created_at",
    )

    def __repr__(self) -> str:
        return f"<ConsultationRequest(id={self.id}, title={self.title[:30]}, status={self.status})>"

    @property
    def is_pending(self) -> bool:
        """Check if consultation is awaiting action."""
        return self.status in ("pending", "in_review")

    @property
    def is_resolved(self) -> bool:
        """Check if consultation has been resolved."""
        return self.status in ("approved", "rejected", "cancelled", "expired")

    @property
    def comment_count(self) -> int:
        """Count comments on this consultation."""
        return len(self.comments) if self.comments else 0


class ConsultationComment(Base):
    """
    Consultation Comment model for discussion threads.

    Purpose:
        - Enable discussion on consultation requests
        - Track reviewer feedback and questions
        - Support resolution notes

    Fields:
        - id: UUID primary key
        - consultation_id: Foreign key to ConsultationRequest
        - user_id: Comment author
        - comment: Comment text (markdown)
        - is_resolution_note: Whether this is a resolution note
        - created_at: When comment was created

    Usage Example:
        comment = ConsultationComment(
            consultation_id=consultation.id,
            user_id=reviewer.id,
            comment="Please clarify the auth token handling.",
        )
        session.add(comment)
        session.commit()
    """

    __tablename__ = "consultation_comments"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Consultation Association
    consultation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("consultation_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Author
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Comment Content
    comment = Column(Text, nullable=False)
    is_resolution_note = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether this is a resolution note (vs. discussion comment)",
    )

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    consultation = relationship("ConsultationRequest", back_populates="comments")
    user = relationship("User", backref="consultation_comments")

    def __repr__(self) -> str:
        return f"<ConsultationComment(id={self.id}, user_id={self.user_id})>"
