"""
Organization Invitation Model

Security-focused invitation system with hash-based tokens (ADR-047).

Features:
- SHA256 token hashing (no raw tokens stored)
- One-time use (status change prevents replay)
- 7-day expiry (configurable)
- Rate limiting support (resend_count)
- Full audit trail (who invited whom, when, from where)
- Role constraint (admin/member only, no owner)

Reference: ADR-047-Organization-Invitation-System.md
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    CheckConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID, INET
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class OrgInvitationStatus:
    """Organization invitation status enum"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class OrganizationInvitation(Base):
    """
    Organization invitation with hash-based token security.

    Security features:
    - Token stored as SHA256 hash (invitation_token_hash)
    - One-time use enforcement (status check)
    - Constant-time comparison (hmac.compare_digest)
    - Audit trail (IP, user agent, timestamps)
    - Role constraint (admin/member only, cannot invite as owner)

    Rate limiting:
    - resend_count tracked in DB
    - Limit enforced in application layer (configurable)
    - Default: 50 invitations/hour per organization

    CTO Mandatory Conditions:
    - #1: Role validation constraint (admin/member only)
    - #2: Cleanup index for old invitations (90-day retention)
    - #3: Early exit optimization (User.effective_tier)
    """
    __tablename__ = "organization_invitations"

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    # Invitation details
    organization_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False
    )
    invited_email = Column(String(255), nullable=False, index=True)
    invitation_token_hash = Column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
        comment="SHA256 hash of invitation token (never store raw token)"
    )
    role = Column(String(20), nullable=False, default="member")
    status = Column(String(20), nullable=False, default=OrgInvitationStatus.PENDING, index=True)

    # User relationships
    invited_by = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    accepted_at = Column(DateTime, nullable=True)
    declined_at = Column(DateTime, nullable=True)

    # Rate limiting (enforced in application)
    resend_count = Column(Integer, nullable=False, default=0)
    last_resent_at = Column(DateTime, nullable=True)

    # Audit trail
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="invitations", lazy="joined")
    inviter = relationship("User", foreign_keys=[invited_by], lazy="joined")

    # Constraints
    __table_args__ = (
        CheckConstraint("expires_at > created_at", name="org_invitation_valid_expiry"),
        # CTO MANDATORY CONDITION #1: Role validation constraint
        CheckConstraint("role IN ('admin', 'member')", name="org_invitation_valid_role"),
        # Partial unique index for pending invitations
        Index(
            "idx_org_unique_pending_invitation",
            "organization_id",
            "invited_email",
            unique=True,
            postgresql_where=(status == OrgInvitationStatus.PENDING)
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<OrganizationInvitation(id={self.id}, "
            f"org_id={self.organization_id}, "
            f"email={self.invited_email}, "
            f"status={self.status})>"
        )

    @property
    def is_expired(self) -> bool:
        """Check if invitation has expired"""
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_pending(self) -> bool:
        """Check if invitation is pending"""
        return self.status == OrgInvitationStatus.PENDING and not self.is_expired

    @property
    def is_accepted(self) -> bool:
        """Check if invitation was accepted"""
        return self.status == OrgInvitationStatus.ACCEPTED

    @property
    def is_declined(self) -> bool:
        """Check if invitation was declined"""
        return self.status == OrgInvitationStatus.DECLINED

    @property
    def can_resend(self) -> bool:
        """
        Check if invitation can be resent.

        Rules:
        - Status must be pending or expired
        - Not exceeded max resends limit (default: 3)
        - Cooldown period elapsed (default: 5 minutes)
        """
        max_resends = 3
        cooldown_minutes = 5

        if self.status not in [OrgInvitationStatus.PENDING, OrgInvitationStatus.EXPIRED]:
            return False

        if self.resend_count >= max_resends:
            return False

        if self.last_resent_at:
            cooldown = timedelta(minutes=cooldown_minutes)
            if datetime.now(timezone.utc) - self.last_resent_at < cooldown:
                return False

        return True

    def accept(self, user_id: UUID) -> None:
        """
        Accept invitation (one-time use).

        Args:
            user_id: User who accepted the invitation

        Raises:
            ValueError: If invitation cannot be accepted
        """
        if not self.is_pending:
            raise ValueError(f"Invitation cannot be accepted (status: {self.status})")

        self.status = OrgInvitationStatus.ACCEPTED
        self.accepted_at = datetime.now(timezone.utc)

    def decline(self) -> None:
        """
        Decline invitation.

        Raises:
            ValueError: If invitation cannot be declined
        """
        if not self.is_pending:
            raise ValueError(f"Invitation cannot be declined (status: {self.status})")

        self.status = OrgInvitationStatus.DECLINED
        self.declined_at = datetime.now(timezone.utc)

    def cancel(self) -> None:
        """
        Cancel invitation (admin action).

        Raises:
            ValueError: If invitation cannot be cancelled
        """
        if self.status != OrgInvitationStatus.PENDING:
            raise ValueError(f"Invitation cannot be cancelled (status: {self.status})")

        self.status = OrgInvitationStatus.CANCELLED

    def mark_expired(self) -> None:
        """Mark invitation as expired (background job)"""
        if self.status == OrgInvitationStatus.PENDING and self.is_expired:
            self.status = OrgInvitationStatus.EXPIRED

    def increment_resend_count(self) -> None:
        """
        Increment resend counter (before sending email).

        Raises:
            ValueError: If cannot resend
        """
        if not self.can_resend:
            raise ValueError(
                f"Cannot resend invitation (count: {self.resend_count}, "
                f"status: {self.status})"
            )

        self.resend_count += 1
        self.last_resent_at = datetime.now(timezone.utc)
