"""
Gate Model - Quality Gate Management (FR1)
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: November 28, 2025
Status: ACTIVE - Week 3 Architecture Design
Authority: Backend Lead + CTO Approved
Foundation: Data Model v0.1 (9.8/10 quality), FR1 (Quality Gate Management)

Zero Mock Policy: Real SQLAlchemy model with all fields
Performance: Indexed for <200ms query response (p95)
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Gate(Base):
    """
    Gate model for SDLC quality gates (G0, G1, G2...G9).

    Purpose (FR1):
        - Quality gate creation and lifecycle management
        - Multi-approver workflow (CTO, CPO, CEO)
        - Stage progression tracking (WHY → WHAT → BUILD...)
        - Policy evaluation results storage

    SDLC 4.9 Gates:
        - G0.1: Foundation Ready (WHY stage)
        - G0.2: Solution Diversity (WHY stage)
        - G1: Design Ready (WHAT stage)
        - G2: Ship Ready (HOW stage)
        - G3: Build Complete (BUILD stage)
        - G4: Test Complete (TEST stage)
        - G5: Deploy Ready (DEPLOY stage)
        - G6: Operate Ready (OPERATE stage)
        - G7: Integration Complete (INTEGRATE stage)
        - G8: Collaboration Ready (COLLABORATE stage)
        - G9: Governance Complete (GOVERN stage)

    Fields:
        - id: UUID primary key
        - gate_name: Human-readable name (e.g., "Q4 2025 E-commerce Platform - G1")
        - gate_type: SDLC 4.9 gate type (e.g., 'G1_DESIGN_READY')
        - stage: Current SDLC stage ('WHY', 'WHAT', 'BUILD', etc.)
        - project_id: Foreign key to Project
        - created_by: Foreign key to User (gate creator)
        - status: Gate status ('DRAFT', 'PENDING_APPROVAL', 'APPROVED', 'REJECTED', 'ARCHIVED')
        - exit_criteria: JSONB array of exit criteria
        - description: Gate description
        - approved_at: Approval timestamp
        - rejected_at: Rejection timestamp
        - archived_at: Archive timestamp
        - created_at: Gate creation timestamp
        - updated_at: Last update timestamp
        - deleted_at: Soft delete timestamp

    Relationships:
        - project: Many-to-One with Project model
        - creator: Many-to-One with User model
        - approvals: One-to-Many with GateApproval model
        - evidence: One-to-Many with GateEvidence model
        - policy_evaluations: One-to-Many with PolicyEvaluation model
        - stage_transitions: One-to-Many with StageTransition model

    Indexes:
        - project_id (B-tree) - Fast project gate lookup
        - created_by (B-tree) - Fast creator lookup
        - status (B-tree) - Active gate filtering
        - gate_type (B-tree) - Gate type filtering
        - created_at (B-tree) - Recent gates queries

    Usage Example:
        gate = Gate(
            gate_name="E-commerce Platform v2.0 - G1 Design Ready",
            gate_type="G1_DESIGN_READY",
            stage="WHAT",
            project_id=project.id,
            created_by=user.id,
            status="DRAFT",
            exit_criteria=[
                {"id": "FRD_COMPLETE", "description": "Functional Requirements Document complete"},
                {"id": "DATA_MODEL", "description": "Data Model v0.1 designed"}
            ]
        )
    """

    __tablename__ = "gates"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Gate Identity
    gate_name = Column(String(255), nullable=False)
    gate_type = Column(
        String(50), nullable=False, index=True
    )  # 'G1_DESIGN_READY', 'G2_SHIP_READY', etc.
    stage = Column(
        String(20), nullable=False, index=True
    )  # 'WHY', 'WHAT', 'BUILD', 'TEST', etc.

    # Project Relationship
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Creator
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Gate Status
    status = Column(
        String(20),
        nullable=False,
        default="DRAFT",
        index=True,
    )  # 'DRAFT', 'PENDING_APPROVAL', 'APPROVED', 'REJECTED', 'ARCHIVED'

    # Exit Criteria (JSONB)
    exit_criteria = Column(
        JSONB, nullable=False, default=list
    )  # [{"id": "...", "description": "...", "met": false}]

    # Description
    description = Column(Text, nullable=True)

    # Status Timestamps
    approved_at = Column(DateTime, nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    archived_at = Column(DateTime, nullable=True)

    # Audit Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="gates")
    creator = relationship("User", back_populates="created_gates")
    approvals = relationship(
        "GateApproval", back_populates="gate", cascade="all, delete-orphan"
    )
    evidence = relationship(
        "GateEvidence", back_populates="gate", cascade="all, delete-orphan"
    )
    policy_evaluations = relationship(
        "PolicyEvaluation", back_populates="gate", cascade="all, delete-orphan"
    )
    stage_transitions = relationship(
        "StageTransition", back_populates="gate", cascade="all, delete-orphan"
    )
    ai_requests = relationship("AIRequest", back_populates="gate")
    ai_evidence_drafts = relationship(
        "AIEvidenceDraft", back_populates="gate", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Gate(id={self.id}, gate_name={self.gate_name}, status={self.status})>"

    @property
    def is_approved(self) -> bool:
        """Check if gate is approved"""
        return self.status == "APPROVED"

    @property
    def is_pending(self) -> bool:
        """Check if gate is pending approval"""
        return self.status == "PENDING_APPROVAL"

    @property
    def is_draft(self) -> bool:
        """Check if gate is still in draft"""
        return self.status == "DRAFT"

    @property
    def all_criteria_met(self) -> bool:
        """Check if all exit criteria are met"""
        if not self.exit_criteria:
            return False
        return all(criterion.get("met", False) for criterion in self.exit_criteria)

    @property
    def criteria_met_count(self) -> int:
        """Count how many criteria are met"""
        if not self.exit_criteria:
            return 0
        return sum(1 for criterion in self.exit_criteria if criterion.get("met", False))

    @property
    def criteria_total_count(self) -> int:
        """Total number of exit criteria"""
        return len(self.exit_criteria) if self.exit_criteria else 0
