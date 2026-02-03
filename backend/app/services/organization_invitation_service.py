"""
Organization Invitation Service

Business logic for secure organization invitation system with hash-based tokens.

Security Features:
- Cryptographically secure token generation (secrets.token_urlsafe)
- SHA256 token hashing (no raw tokens stored)
- Constant-time comparison (hmac.compare_digest)
- One-time use enforcement (status change)
- Rate limiting (Redis-based, 50/hour per org)
- Audit trail (IP, user agent, timestamps)
- Role constraint (admin/member only, no owner)

Reference: ADR-047-Organization-Invitation-System.md
Sprint: 146
"""
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.organization_invitation import OrganizationInvitation, OrgInvitationStatus
from app.models.organization import Organization, UserOrganization
from app.models.user import User
from app.schemas.organization_invitation import (
    OrgInvitationCreate,
    OrgInvitationResponse,
    OrgInvitationDetails,
    OrgInvitationAccepted,
    OrgInvitationDeclined,
    OrgInvitationResent,
)
from app.services.email_service import send_invitation_email
from app.core.redis import redis_client


# ============================================================================
# Token Security Functions (Reused from Team Invitation Service)
# ============================================================================

def generate_invitation_token() -> str:
    """
    Generate cryptographically secure invitation token.

    Returns:
        43-character base64url string (256-bit entropy)
    """
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """
    Hash invitation token with SHA256.

    Args:
        token: Raw invitation token

    Returns:
        64-character hexadecimal hash
    """
    return hashlib.sha256(token.encode()).hexdigest()


def verify_token(provided_token: str, stored_hash: str) -> bool:
    """
    Verify invitation token with constant-time comparison.

    Args:
        provided_token: Token from user request
        stored_hash: SHA256 hash from database

    Returns:
        True if token matches hash, False otherwise
    """
    provided_hash = hash_token(provided_token)
    return hmac.compare_digest(provided_hash, stored_hash)


# ============================================================================
# Rate Limiting Functions
# ============================================================================

def check_org_rate_limit(organization_id: UUID) -> None:
    """
    Check if organization has exceeded invitation rate limit.

    Limit: 50 invitations per hour per organization (sliding window)

    Args:
        organization_id: Organization UUID

    Raises:
        HTTPException(429): If rate limit exceeded
    """
    if not redis_client:
        return  # Skip rate limit check if Redis not available

    key = f"org_invitation_rate:{organization_id}:{datetime.now(timezone.utc).strftime('%Y%m%d%H')}"
    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, 3600)  # 1 hour TTL

    max_per_hour = getattr(settings, 'MAX_ORG_INVITATIONS_PER_HOUR', 50)
    if count > max_per_hour:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "rate_limit_exceeded",
                "message": f"Maximum {max_per_hour} invitations per hour per organization",
                "retry_after": 3600
            }
        )


def check_email_rate_limit(email: str) -> None:
    """
    Check if email has received too many invitations recently.

    Limit: 10 invitations per day across all organizations

    Args:
        email: Email address

    Raises:
        HTTPException(429): If rate limit exceeded
    """
    if not redis_client:
        return  # Skip rate limit check if Redis not available

    key = f"org_invitation_email:{email}:{datetime.now(timezone.utc).strftime('%Y%m%d')}"
    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, 86400)  # 24 hours TTL

    max_per_day = getattr(settings, 'MAX_ORG_INVITATIONS_PER_EMAIL_PER_DAY', 10)
    if count > max_per_day:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "rate_limit_exceeded",
                "message": f"Maximum {max_per_day} organization invitations per day per email",
                "retry_after": 86400
            }
        )


# ============================================================================
# Permission Check Functions
# ============================================================================

def check_invitation_permission(
    organization_id: UUID,
    user_id: UUID,
    requested_role: str,
    db: Session
) -> UserOrganization:
    """
    Check if user has permission to send invitations.

    RBAC Rules:
    - Owner: Can invite admin/member
    - Admin: Can invite member only
    - Member: Cannot invite

    Args:
        organization_id: Organization UUID
        user_id: User sending invitation
        requested_role: Role being invited (admin/member)
        db: Database session

    Returns:
        UserOrganization membership record

    Raises:
        HTTPException(403): If not authorized
    """
    # Get user's membership in org
    membership = db.query(UserOrganization).filter(
        UserOrganization.organization_id == organization_id,
        UserOrganization.user_id == user_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "not_member",
                "message": "You are not a member of this organization"
            }
        )

    # Check role permissions
    if membership.role not in ['owner', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "insufficient_permission",
                "message": "Only organization owners and admins can send invitations"
            }
        )

    # Only owner can invite admin
    if requested_role == 'admin' and membership.role != 'owner':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "insufficient_permission",
                "message": "Only organization owners can invite admins"
            }
        )

    # Cannot invite as owner (there can only be one owner per org)
    if requested_role == 'owner':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_role",
                "message": "Cannot invite users as owner. Use 'admin' or 'member'."
            }
        )

    return membership


# ============================================================================
# Invitation Service Functions
# ============================================================================

def send_org_invitation(
    organization_id: UUID,
    data: OrgInvitationCreate,
    invited_by_user_id: UUID,
    db: Session,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> tuple[OrgInvitationResponse, str]:
    """
    Send organization invitation with secure token.

    Security features:
    - Rate limiting (org + email)
    - Permission check (RBAC)
    - Duplicate detection (pending invitation check)
    - Token hashing (SHA256)
    - Audit trail (IP, user agent)

    Args:
        organization_id: Organization UUID
        data: Invitation creation data
        invited_by_user_id: User who is sending invitation
        db: Database session
        ip_address: IP address of inviter (optional)
        user_agent: User agent of inviter (optional)

    Returns:
        Tuple of (OrgInvitationResponse, raw_token)
        raw_token is used for email link (only returned once)

    Raises:
        HTTPException(403): If user not authorized
        HTTPException(404): If organization not found
        HTTPException(409): If pending invitation already exists
        HTTPException(429): If rate limit exceeded
    """
    # 1. Permission check (RBAC)
    check_invitation_permission(organization_id, invited_by_user_id, data.role, db)

    # 2. Rate limiting
    check_org_rate_limit(organization_id)
    check_email_rate_limit(data.email)

    # 3. Verify organization exists
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    # 4. Check if pending invitation already exists
    existing = db.query(OrganizationInvitation).filter(
        and_(
            OrganizationInvitation.organization_id == organization_id,
            OrganizationInvitation.invited_email == data.email,
            OrganizationInvitation.status == OrgInvitationStatus.PENDING
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "invitation_exists",
                "message": "Pending invitation already sent to this email",
                "invitation_id": str(existing.id)
            }
        )

    # 5. Check if user is already a member
    email_user = db.query(User).filter(User.email == data.email).first()
    if email_user:
        existing_member = db.query(UserOrganization).filter(
            UserOrganization.organization_id == organization_id,
            UserOrganization.user_id == email_user.id
        ).first()

        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "already_member",
                    "message": "User with this email is already a member of this organization",
                    "role": existing_member.role
                }
            )

    # 6. Generate secure token
    raw_token = generate_invitation_token()
    token_hash = hash_token(raw_token)

    # 7. Create invitation record
    expiry_days = getattr(settings, 'INVITATION_EXPIRY_DAYS', 7)
    invitation = OrganizationInvitation(
        organization_id=organization_id,
        invited_email=data.email,
        invitation_token_hash=token_hash,
        role=data.role,
        status=OrgInvitationStatus.PENDING,
        invited_by=invited_by_user_id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=expiry_days),
        ip_address=ip_address,
        user_agent=user_agent
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    # 8. Prepare response
    inviter = db.query(User).filter(User.id == invited_by_user_id).first()

    response = OrgInvitationResponse(
        invitation_id=invitation.id,
        organization_id=invitation.organization_id,
        organization_name=org.name,
        invited_email=invitation.invited_email,
        role=invitation.role,
        status=invitation.status,
        expires_at=invitation.expires_at,
        invited_by={
            "user_id": inviter.id,
            "display_name": inviter.display_name or inviter.username
        },
        created_at=invitation.created_at,
        message=data.message
    )

    return response, raw_token


def get_org_invitation_by_token(token: str, db: Session) -> OrgInvitationDetails:
    """
    Get organization invitation details by token (public endpoint, no auth).

    Args:
        token: Raw invitation token from URL
        db: Database session

    Returns:
        OrgInvitationDetails

    Raises:
        HTTPException(404): If invitation not found or expired
        HTTPException(410): If invitation already used
    """
    # Hash token for lookup
    token_hash = hash_token(token)

    # Find invitation by hash
    invitation = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.invitation_token_hash == token_hash
    ).first()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "invitation_not_found",
                "message": "Invitation not found or has expired"
            }
        )

    # Check if already used
    if invitation.status != OrgInvitationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={
                "error": "invitation_already_used",
                "message": f"This invitation has already been {invitation.status}"
            }
        )

    # Check if expired
    if invitation.is_expired:
        invitation.mark_expired()
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "invitation_expired",
                "message": "This invitation has expired"
            }
        )

    # Build response
    org = db.query(Organization).filter(Organization.id == invitation.organization_id).first()
    inviter = db.query(User).filter(User.id == invitation.invited_by).first()

    return OrgInvitationDetails(
        organization={
            "organization_id": org.id,
            "organization_name": org.name,
            "organization_slug": org.slug,
            "plan": org.plan
        },
        invited_email=invitation.invited_email,
        role=invitation.role,
        status=invitation.status,
        expires_at=invitation.expires_at,
        invited_by={
            "user_id": inviter.id,
            "display_name": inviter.display_name or inviter.username
        },
        created_at=invitation.created_at
    )


def accept_org_invitation(
    token: str,
    user_id: UUID,
    user_email: str,
    db: Session
) -> OrgInvitationAccepted:
    """
    Accept organization invitation and create membership.

    Security checks:
    - Token verification (constant-time)
    - Email matching (user email must match invited email)
    - Status check (must be pending)
    - Expiry check
    - One-time use (status change)

    Args:
        token: Raw invitation token
        user_id: Authenticated user ID
        user_email: Authenticated user email
        db: Database session

    Returns:
        OrgInvitationAccepted

    Raises:
        HTTPException(400): If cannot accept
        HTTPException(403): If email mismatch
        HTTPException(404): If invitation not found
        HTTPException(409): If already member
    """
    # Hash token for lookup
    token_hash = hash_token(token)

    # Find invitation
    invitation = db.query(OrganizationInvitation).filter(
        and_(
            OrganizationInvitation.invitation_token_hash == token_hash,
            OrganizationInvitation.status == OrgInvitationStatus.PENDING
        )
    ).first()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found or already used"
        )

    # Check expiry
    if invitation.is_expired:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invitation_expired",
                "message": "This invitation has expired",
                "expires_at": invitation.expires_at.isoformat()
            }
        )

    # Verify email match
    if user_email.lower() != invitation.invited_email.lower():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "email_mismatch",
                "message": "This invitation was sent to a different email address"
            }
        )

    # Check if already a member
    existing_member = db.query(UserOrganization).filter(
        UserOrganization.organization_id == invitation.organization_id,
        UserOrganization.user_id == user_id
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "already_member",
                "message": "You are already a member of this organization",
                "organization_id": str(invitation.organization_id),
                "role": existing_member.role
            }
        )

    # Accept invitation (one-time use)
    invitation.accept(user_id)

    # Get org info
    org = db.query(Organization).filter(Organization.id == invitation.organization_id).first()

    # Create organization membership
    user_org = UserOrganization(
        user_id=user_id,
        organization_id=invitation.organization_id,
        role=invitation.role,
        joined_at=datetime.now(timezone.utc)
    )
    db.add(user_org)
    db.commit()

    return OrgInvitationAccepted(
        status="accepted",
        organization_id=invitation.organization_id,
        organization_name=org.name,
        organization_slug=org.slug,
        role=invitation.role,
        accepted_at=invitation.accepted_at,
        redirect_url=f"/org/{org.slug}/dashboard"
    )


def decline_org_invitation(token: str, db: Session) -> OrgInvitationDeclined:
    """
    Decline organization invitation (polite rejection).

    Args:
        token: Raw invitation token
        db: Database session

    Returns:
        OrgInvitationDeclined

    Raises:
        HTTPException(400): If cannot decline
        HTTPException(404): If invitation not found
    """
    # Hash token for lookup
    token_hash = hash_token(token)

    # Find invitation
    invitation = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.invitation_token_hash == token_hash
    ).first()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found"
        )

    # Check if can decline
    if invitation.status == OrgInvitationStatus.ACCEPTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "cannot_decline_invitation",
                "message": "Invitation has already been accepted"
            }
        )

    # Decline invitation
    invitation.decline()
    db.commit()

    return OrgInvitationDeclined(
        status="declined",
        declined_at=invitation.declined_at,
        message="Invitation declined successfully"
    )


def resend_org_invitation(
    invitation_id: UUID,
    db: Session
) -> tuple[OrgInvitationResent, str]:
    """
    Resend organization invitation email.

    Rate limiting:
    - Max 3 resends per invitation
    - 5 minute cooldown between resends

    Args:
        invitation_id: Invitation UUID
        db: Database session

    Returns:
        Tuple of (OrgInvitationResent, raw_token)

    Raises:
        HTTPException(400): If cannot resend
        HTTPException(404): If invitation not found
        HTTPException(429): If resend limit exceeded
    """
    # Find invitation
    invitation = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.id == invitation_id
    ).first()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found"
        )

    # Check if can resend
    if invitation.status == OrgInvitationStatus.ACCEPTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "cannot_resend_invitation",
                "message": "Invitation has already been accepted",
                "status": invitation.status
            }
        )

    # Check resend limit
    max_resends = getattr(settings, 'MAX_INVITATION_RESENDS', 3)
    if invitation.resend_count >= max_resends:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "resend_limit_exceeded",
                "message": f"Maximum {max_resends} resends per invitation",
                "resend_count": invitation.resend_count
            }
        )

    # Check cooldown
    cooldown_minutes = getattr(settings, 'INVITATION_RESEND_COOLDOWN_MINUTES', 5)
    if invitation.last_resent_at:
        cooldown = timedelta(minutes=cooldown_minutes)
        elapsed = datetime.now(timezone.utc) - invitation.last_resent_at

        if elapsed < cooldown:
            retry_after = int((cooldown - elapsed).total_seconds())
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "resend_cooldown_active",
                    "message": f"Please wait {cooldown_minutes} minutes before resending",
                    "retry_after": retry_after
                }
            )

    # Generate new token (security: regenerate token on resend)
    raw_token = generate_invitation_token()
    token_hash = hash_token(raw_token)

    # Update invitation
    invitation.invitation_token_hash = token_hash
    invitation.increment_resend_count()
    db.commit()
    db.refresh(invitation)

    return OrgInvitationResent(
        invitation_id=invitation.id,
        status=invitation.status,
        resend_count=invitation.resend_count,
        last_resent_at=invitation.last_resent_at,
        expires_at=invitation.expires_at,
        message="Invitation email resent successfully"
    ), raw_token


def list_org_invitations(
    organization_id: UUID,
    db: Session,
    status_filter: Optional[str] = None,
    email_filter: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> list[OrgInvitationResponse]:
    """
    List organization invitations with optional filters.

    Args:
        organization_id: Organization UUID
        db: Database session
        status_filter: Filter by invitation status (optional)
        email_filter: Filter by invited email (optional)
        limit: Max results per page (default: 50)
        offset: Skip N results (default: 0)

    Returns:
        List of OrgInvitationResponse

    Raises:
        HTTPException(404): If organization not found
    """
    # Verify organization exists
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    # Build query
    query = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.organization_id == organization_id
    )

    # Apply status filter
    if status_filter:
        valid_statuses = ['pending', 'accepted', 'declined', 'expired', 'cancelled']
        if status_filter not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status_filter}. Must be one of: {', '.join(valid_statuses)}"
            )
        query = query.filter(OrganizationInvitation.status == status_filter)

    # Apply email filter
    if email_filter:
        query = query.filter(
            OrganizationInvitation.invited_email.ilike(f"%{email_filter}%")
        )

    # Order by created_at descending (newest first)
    query = query.order_by(OrganizationInvitation.created_at.desc())

    # Apply pagination
    query = query.offset(offset).limit(limit)

    # Execute query
    invitations = query.all()

    # Build response list
    responses = []
    for invitation in invitations:
        inviter = db.query(User).filter(User.id == invitation.invited_by).first()

        responses.append(OrgInvitationResponse(
            invitation_id=invitation.id,
            organization_id=invitation.organization_id,
            organization_name=org.name,
            invited_email=invitation.invited_email,
            role=invitation.role,
            status=invitation.status,
            expires_at=invitation.expires_at,
            invited_by={
                "user_id": inviter.id if inviter else None,
                "display_name": (inviter.display_name or inviter.username) if inviter else "Unknown"
            },
            created_at=invitation.created_at,
            message=None
        ))

    return responses


def cancel_org_invitation(
    invitation_id: UUID,
    cancelled_by_user_id: UUID,
    db: Session
) -> None:
    """
    Cancel a pending organization invitation (admin action).

    Args:
        invitation_id: Invitation UUID
        cancelled_by_user_id: User performing the cancellation
        db: Database session

    Raises:
        HTTPException(400): If invitation cannot be cancelled
        HTTPException(403): If user not authorized
        HTTPException(404): If invitation not found
    """
    # Find invitation
    invitation = db.query(OrganizationInvitation).filter(
        OrganizationInvitation.id == invitation_id
    ).first()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found"
        )

    # Check permission (owner/admin can cancel)
    membership = db.query(UserOrganization).filter(
        UserOrganization.organization_id == invitation.organization_id,
        UserOrganization.user_id == cancelled_by_user_id,
        UserOrganization.role.in_(['owner', 'admin'])
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "insufficient_permission",
                "message": "Only organization owners and admins can cancel invitations"
            }
        )

    # Check if can cancel
    if invitation.status == OrgInvitationStatus.ACCEPTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "cannot_cancel_invitation",
                "message": "Cannot cancel an already accepted invitation"
            }
        )

    if invitation.status == OrgInvitationStatus.DECLINED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "cannot_cancel_invitation",
                "message": "Cannot cancel an already declined invitation"
            }
        )

    if invitation.status == OrgInvitationStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "already_cancelled",
                "message": "Invitation is already cancelled"
            }
        )

    # Cancel the invitation
    invitation.status = OrgInvitationStatus.CANCELLED
    db.commit()
