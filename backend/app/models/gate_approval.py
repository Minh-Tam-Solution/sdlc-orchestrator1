"""
=========================================================================
Gate Approval Model - Multi-Approver Workflow (FR1)
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: November 28, 2025
Status: ACTIVE - Week 3 Architecture Design
Authority: Backend Lead + CTO Approved
Foundation: Data Model v0.1 (9.8/10 quality), FR1 (Quality Gate Management)
Framework: SDLC 4.9 Complete Lifecycle

Purpose:
- Multi-approver workflow (CTO, CPO, CEO approval required)
- Gate approval tracking (PENDING → APPROVED/REJECTED)
- Approval comments and rationale
- Rejection handling with feedback

Business Logic:
- All approvers must approve for gate to pass
- Rejection blocks gate progression
- Approval timestamps for audit trail

Zero Mock Policy: Real SQLAlchemy model with all fields
=========================================================================
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GateApproval(Base):
    """
    Gate Approval model for multi-approver workflow.

    Purpose (FR1):
        - Multi-level approval (CTO, CPO, CEO for critical gates)
        - Approval/rejection tracking with comments
        - Audit trail for compliance (who approved when)

    Approval Flow:
        1. Gate submitted (status = PENDING_APPROVAL)
        2. Approvers assigned (CTO, CPO, CEO roles)
        3. Each approver reviews and approves/rejects
        4. All approvals required → Gate status = APPROVED
        5. Any rejection → Gate status = REJECTED

    Fields:
        - id: UUID primary key
        - gate_id: Foreign key to Gate
        - approver_id: Foreign key to User (approver)
        - status: Approval status ('PENDING', 'APPROVED', 'REJECTED')
        - comments: Approval/rejection comments
        - approved_at: Approval timestamp
        - rejected_at: Rejection timestamp
        - created_at: Record creation timestamp
        - updated_at: Last update timestamp

    Relationships:
        - gate: Many-to-One with Gate model
        - approver: Many-to-One with User model

    Indexes:
        - gate_id (B-tree) - Fast gate approval lookup
        - approver_id (B-tree) - Fast approver lookup
        - status (B-tree) - Pending approval filtering

    Usage Example:
        approval = GateApproval(
            gate_id=gate.id,
            approver_id=cto_user.id,
            status='PENDING'
        )
        session.add(approval)
        session.commit()

        # CTO approves
        approval.status = 'APPROVED'
        approval.comments = 'Data Model quality 9.8/10. Unconditional approval.'
        approval.approved_at = datetime.utcnow()
        session.commit()
    """

    __tablename__ = "gate_approvals"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Gate Relationship
    gate_id = Column(
        UUID(as_uuid=True),
        ForeignKey("gates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Approver
    approver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Approval Status
    status = Column(
        String(20), nullable=False, default="PENDING", index=True
    )  # 'PENDING', 'APPROVED', 'REJECTED'

    # Comments
    comments = Column(Text, nullable=True)

    # Status Timestamps
    approved_at = Column(DateTime, nullable=True)
    rejected_at = Column(DateTime, nullable=True)

    # Audit Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    gate = relationship("Gate", back_populates="approvals")
    approver = relationship("User", back_populates="gate_approvals")

    def __repr__(self) -> str:
        return f"<GateApproval(gate_id={self.gate_id}, approver_id={self.approver_id}, status={self.status})>"

    @property
    def is_approved(self) -> bool:
        """Check if approval is approved"""
        return self.status == "APPROVED"

    @property
    def is_rejected(self) -> bool:
        """Check if approval is rejected"""
        return self.status == "REJECTED"

    @property
    def is_pending(self) -> bool:
        """Check if approval is pending"""
        return self.status == "PENDING"

    def approve(self, comments: Optional[str] = None) -> None:
        """Approve the gate with optional comments"""
        self.status = "APPROVED"
        self.comments = comments
        self.approved_at = datetime.utcnow()

    def reject(self, comments: str) -> None:
        """Reject the gate with required comments"""
        self.status = "REJECTED"
        self.comments = comments
        self.rejected_at = datetime.utcnow()
