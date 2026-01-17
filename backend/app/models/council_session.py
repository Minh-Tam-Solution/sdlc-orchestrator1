"""
=========================================================================
Council Session Model - AI Council Deliberation History
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: January 16, 2026
Status: ACTIVE - Sprint 69 CTO Go-Live
Authority: Backend Lead + CTO Approved
Foundation: Sprint 26 (AI Council), ADR-011 (AI Governance Layer)
Framework: SDLC 5.1.2 Universal Framework

Purpose:
- Persist AI council deliberation sessions
- Track council history per project
- Store provider responses and costs
- Support analytics and audit trail

Security Standards:
- Row-Level Security (RLS) for multi-tenancy
- Immutable audit trail (sessions are read-only after creation)

Zero Mock Policy: Real SQLAlchemy model with all fields
=========================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CouncilModeType(str, Enum):
    """Council deliberation mode types."""
    SINGLE = "single"
    COUNCIL = "council"
    AUTO = "auto"


class CouncilSessionStatus(str, Enum):
    """Council session status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class CouncilSession(Base):
    """
    Council Session model for AI deliberation history tracking.

    Purpose:
        - Store AI council deliberation results
        - Track provider responses and costs
        - Support council history queries
        - Enable analytics on council usage

    Fields:
        - id: UUID primary key (request_id)
        - project_id: Foreign key to Project
        - violation_id: Foreign key to ComplianceViolation
        - triggered_by: Foreign key to User (who triggered, null for auto)
        - mode_requested: Council mode requested (single, council, auto)
        - mode_used: Council mode actually used
        - status: Session status
        - providers_used: List of provider names used
        - recommendation: Final AI recommendation text
        - confidence_score: Confidence score (0-100)
        - provider_responses: JSONB with individual provider responses
        - total_duration_ms: Total deliberation duration in milliseconds
        - total_cost_usd: Total cost in USD
        - error_message: Error message if failed
        - created_at: Record creation timestamp
        - completed_at: Deliberation completion timestamp

    Relationships:
        - project: Many-to-One with Project model
        - violation: Many-to-One with ComplianceViolation model
        - triggered_by_user: Many-to-One with User model

    Indexes:
        - project_id (B-tree) - Fast project history lookup
        - violation_id (B-tree) - Fast violation lookup
        - created_at DESC - Fast recent sessions lookup
        - mode_used - Mode-based filtering

    Usage Example:
        session = CouncilSession(
            project_id=project.id,
            violation_id=violation.id,
            triggered_by=user.id,
            mode_requested=CouncilModeType.AUTO,
            mode_used=CouncilModeType.COUNCIL,
            status=CouncilSessionStatus.COMPLETED,
            providers_used=["ollama", "claude", "gpt4o"],
            recommendation="Apply input validation...",
            confidence_score=85,
            total_duration_ms=4523.5,
            total_cost_usd=0.0234,
        )
        session.add(session)
        session.commit()
    """

    __tablename__ = "council_sessions"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Project Reference
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Violation Reference
    violation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("compliance_violations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Trigger Information
    triggered_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,  # Null for auto-triggered
        index=True,
    )

    # Council Mode
    mode_requested = Column(
        SQLEnum(CouncilModeType),
        nullable=False,
        default=CouncilModeType.AUTO,
    )
    mode_used = Column(
        SQLEnum(CouncilModeType),
        nullable=True,  # Set after deliberation completes
        index=True,
    )

    # Session Status
    status = Column(
        SQLEnum(CouncilSessionStatus),
        nullable=False,
        default=CouncilSessionStatus.PENDING,
        index=True,
    )

    # Providers
    providers_used = Column(JSONB, nullable=True, default=list)  # List of provider names

    # Results
    recommendation = Column(Text, nullable=True)
    confidence_score = Column(Integer, nullable=True)  # 0-100

    # Provider Responses (detailed)
    provider_responses = Column(JSONB, nullable=True, default=list)
    # Format: [
    #     {
    #         "provider": "ollama",
    #         "model": "qwen3:32b",
    #         "response": "...",
    #         "latency_ms": 1234.5,
    #         "cost_usd": 0.0,
    #         "tokens_used": 500,
    #         "peer_rank": 1
    #     },
    #     ...
    # ]

    # Metrics
    total_duration_ms = Column(Float, nullable=True)
    total_cost_usd = Column(Float, nullable=True, default=0.0)

    # Error Handling
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    project = relationship("Project", backref="council_sessions")
    violation = relationship("ComplianceViolation", backref="council_sessions")
    triggered_by_user = relationship("User", foreign_keys=[triggered_by])

    def __repr__(self) -> str:
        return (
            f"<CouncilSession(id={self.id}, project_id={self.project_id}, "
            f"mode={self.mode_used}, status={self.status}, confidence={self.confidence_score})>"
        )

    @property
    def is_completed(self) -> bool:
        """Check if session is completed."""
        return self.status == CouncilSessionStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        """Check if session failed."""
        return self.status == CouncilSessionStatus.FAILED

    @property
    def duration_seconds(self) -> Optional[float]:
        """Get session duration in seconds."""
        if self.total_duration_ms:
            return self.total_duration_ms / 1000.0
        return None

    @property
    def providers_count(self) -> int:
        """Get number of providers used."""
        if self.providers_used:
            return len(self.providers_used)
        return 0
