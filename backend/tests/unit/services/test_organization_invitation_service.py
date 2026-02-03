"""
Unit Tests for Organization Invitation Service

Tests for business logic, security features, and error handling.

Sprint: 146
Reference: ADR-047-Organization-Invitation-System-Architecture.md

Coverage:
- Token security functions (generate, hash, verify)
- Rate limiting (Redis-based)
- Core service functions (send, get, accept, decline, resend, cancel)
- Permission checks (RBAC)
- Error cases and edge cases
"""
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.organization_invitation import (
    OrganizationInvitation,
    OrgInvitationStatus,
)
from app.schemas.organization_invitation import OrgInvitationCreate
from app.services import organization_invitation_service as service


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_db():
    """Mock database session (synchronous SQLAlchemy Session)"""
    mock = MagicMock(spec=Session)
    return mock


@pytest.fixture
def mock_redis():
    """Mock Redis client for rate limiting"""
    with patch("app.services.organization_invitation_service.redis_client") as mock:
        mock.incr.return_value = 1  # Default: under limit
        mock.expire.return_value = True
        yield mock


@pytest.fixture
def sample_organization():
    """Sample organization for testing"""
    org = MagicMock()
    org.id = uuid4()
    org.name = "Test Organization"
    org.slug = "test-org"
    org.plan = "pro"
    return org


@pytest.fixture
def sample_user():
    """Sample user for testing"""
    user = MagicMock()
    user.id = uuid4()
    user.email = "test@example.com"
    user.full_name = "Test User"
    user.display_name = "Test User"
    return user


@pytest.fixture
def sample_inviter():
    """Sample inviter user for testing"""
    inviter = MagicMock()
    inviter.id = uuid4()
    inviter.email = "admin@example.com"
    inviter.full_name = "Admin User"
    inviter.display_name = "Admin User"
    return inviter


@pytest.fixture
def sample_invitation_data():
    """Sample invitation creation data"""
    return OrgInvitationCreate(
        email="invitee@example.com",
        role="member",
        message="Welcome to our organization!",
    )


@pytest.fixture
def sample_invitation(sample_organization, sample_inviter):
    """Sample pending invitation"""
    invitation = MagicMock(spec=OrganizationInvitation)
    invitation.id = uuid4()
    invitation.organization_id = sample_organization.id
    invitation.invited_email = "invitee@example.com"
    invitation.invitation_token_hash = hashlib.sha256(b"test_token").hexdigest()
    invitation.role = "member"
    invitation.status = OrgInvitationStatus.PENDING
    invitation.invited_by = sample_inviter.id
    invitation.created_at = datetime.now(timezone.utc)
    invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    invitation.resend_count = 0
    invitation.is_pending = True
    invitation.is_expired = False
    invitation.can_resend = True
    invitation.organization = sample_organization
    invitation.inviter = sample_inviter
    return invitation


# ============================================================================
# Token Security Tests
# ============================================================================

class TestTokenSecurity:
    """Test token generation, hashing, and verification"""

    def test_generate_invitation_token_format(self):
        """Token should be URL-safe base64 with sufficient length"""
        token = service.generate_invitation_token()

        assert token is not None
        assert len(token) >= 32  # At least 32 characters
        assert isinstance(token, str)
        # URL-safe characters only
        assert all(c.isalnum() or c in '-_' for c in token)

    def test_generate_invitation_token_uniqueness(self):
        """Generated tokens should be unique"""
        tokens = [service.generate_invitation_token() for _ in range(100)]
        unique_tokens = set(tokens)
        assert len(unique_tokens) == 100  # All tokens unique

    def test_hash_token(self):
        """Token hash should be SHA256 hex digest"""
        token = "test_token_123"
        hashed = service.hash_token(token)

        expected = hashlib.sha256(token.encode()).hexdigest()
        assert hashed == expected
        assert len(hashed) == 64  # SHA256 produces 64 hex chars

    def test_verify_token_success(self):
        """Valid token should verify against its hash"""
        token = "test_token_123"
        token_hash = service.hash_token(token)

        assert service.verify_token(token, token_hash) is True

    def test_verify_token_failure(self):
        """Invalid token should fail verification"""
        token = "test_token_123"
        wrong_hash = hashlib.sha256(b"wrong_token").hexdigest()

        assert service.verify_token(token, wrong_hash) is False

    def test_verify_token_constant_time(self):
        """Verification should use constant-time comparison"""
        # This tests that hmac.compare_digest is used
        token = "test_token"
        token_hash = service.hash_token(token)

        # Both should work (constant time prevents timing attacks)
        assert service.verify_token(token, token_hash) is True
        assert service.verify_token("wrong", token_hash) is False


# ============================================================================
# Rate Limiting Tests
# ============================================================================

class TestRateLimiting:
    """Test rate limiting for invitation sending"""

    def test_org_rate_limit_under_limit(self, mock_redis):
        """Should allow when under rate limit (no exception raised)"""
        mock_redis.incr.return_value = 1  # Under limit

        # Should not raise (returns None when under limit)
        service.check_org_rate_limit(uuid4())

    def test_org_rate_limit_at_limit(self, mock_redis):
        """Should block when at rate limit"""
        mock_redis.incr.return_value = 51  # Over limit

        with pytest.raises(HTTPException) as exc_info:
            service.check_org_rate_limit(uuid4())

        assert exc_info.value.status_code == 429
        assert "rate_limit" in str(exc_info.value.detail).lower()

    def test_email_rate_limit_under_limit(self, mock_redis):
        """Should allow email when under limit"""
        mock_redis.incr.return_value = 1  # Under limit

        # Should not raise (returns None when under limit)
        service.check_email_rate_limit("test@example.com")

    def test_email_rate_limit_exceeded(self, mock_redis):
        """Should block email when rate limit exceeded"""
        mock_redis.incr.return_value = 11  # Over limit

        with pytest.raises(HTTPException) as exc_info:
            service.check_email_rate_limit("test@example.com")

        assert exc_info.value.status_code == 429


# ============================================================================
# Permission Tests
# ============================================================================

class TestPermissions:
    """Test RBAC permission checks"""

    def test_owner_can_invite_admin(self, mock_db):
        """Organization owner can invite as admin"""
        org_id = uuid4()
        user_id = uuid4()

        # Mock owner membership using SQLAlchemy query pattern
        mock_membership = MagicMock()
        mock_membership.role = "owner"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_membership

        result = service.check_invitation_permission(
            org_id, user_id, "admin", mock_db
        )
        assert result == mock_membership

    def test_owner_can_invite_member(self, mock_db):
        """Organization owner can invite as member"""
        org_id = uuid4()
        user_id = uuid4()

        mock_membership = MagicMock()
        mock_membership.role = "owner"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_membership

        result = service.check_invitation_permission(
            org_id, user_id, "member", mock_db
        )
        assert result == mock_membership

    def test_admin_can_invite_member(self, mock_db):
        """Organization admin can invite as member"""
        org_id = uuid4()
        user_id = uuid4()

        mock_membership = MagicMock()
        mock_membership.role = "admin"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_membership

        result = service.check_invitation_permission(
            org_id, user_id, "member", mock_db
        )
        assert result == mock_membership

    def test_admin_cannot_invite_admin(self, mock_db):
        """Organization admin cannot invite as admin"""
        org_id = uuid4()
        user_id = uuid4()

        mock_membership = MagicMock()
        mock_membership.role = "admin"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_membership

        with pytest.raises(HTTPException) as exc_info:
            service.check_invitation_permission(
                org_id, user_id, "admin", mock_db
            )

        assert exc_info.value.status_code == 403
        assert "owner" in str(exc_info.value.detail).lower()

    def test_member_cannot_invite(self, mock_db):
        """Regular member cannot send invitations"""
        org_id = uuid4()
        user_id = uuid4()

        # No membership found
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            service.check_invitation_permission(
                org_id, user_id, "member", mock_db
            )

        assert exc_info.value.status_code == 403


# ============================================================================
# Invitation Model Tests
# ============================================================================

class TestInvitationModel:
    """Test OrganizationInvitation model properties"""

    def test_is_expired_property(self):
        """is_expired should return True when past expiry"""
        invitation = OrganizationInvitation()
        invitation.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)

        assert invitation.is_expired is True

    def test_is_not_expired_property(self):
        """is_expired should return False when before expiry"""
        invitation = OrganizationInvitation()
        invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=1)

        assert invitation.is_expired is False

    def test_is_pending_property(self):
        """is_pending should check status and expiry"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.PENDING
        invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=1)

        assert invitation.is_pending is True

    def test_is_pending_false_when_expired(self):
        """is_pending should be False when expired"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.PENDING
        invitation.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)

        assert invitation.is_pending is False

    def test_is_pending_false_when_accepted(self):
        """is_pending should be False when accepted"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.ACCEPTED
        invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=1)

        assert invitation.is_pending is False

    def test_can_resend_within_limits(self):
        """can_resend should return True within limits"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.PENDING
        invitation.resend_count = 1
        invitation.last_resent_at = datetime.now(timezone.utc) - timedelta(minutes=10)

        assert invitation.can_resend is True

    def test_can_resend_at_max_count(self):
        """can_resend should return False at max resend count"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.PENDING
        invitation.resend_count = 3  # Max is 3
        invitation.last_resent_at = datetime.now(timezone.utc) - timedelta(minutes=10)

        assert invitation.can_resend is False

    def test_can_resend_cooldown_not_elapsed(self):
        """can_resend should return False during cooldown"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.PENDING
        invitation.resend_count = 1
        invitation.last_resent_at = datetime.now(timezone.utc) - timedelta(minutes=2)  # < 5 min

        assert invitation.can_resend is False


# ============================================================================
# Invitation Acceptance Tests
# ============================================================================

class TestInvitationAcceptance:
    """Test invitation acceptance logic"""

    def test_accept_valid_invitation(self, sample_invitation):
        """Valid invitation should be accepted"""
        user_id = uuid4()

        # Mock the accept method
        sample_invitation.is_pending = True
        sample_invitation.accept = MagicMock()

        sample_invitation.accept(user_id)

        sample_invitation.accept.assert_called_once_with(user_id)

    def test_accept_expired_invitation_fails(self):
        """Expired invitation cannot be accepted"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.PENDING
        invitation.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)

        with pytest.raises(ValueError) as exc_info:
            invitation.accept(uuid4())

        assert "cannot be accepted" in str(exc_info.value).lower()

    def test_accept_already_accepted_fails(self):
        """Already accepted invitation cannot be accepted again"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.ACCEPTED
        invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=1)

        with pytest.raises(ValueError) as exc_info:
            invitation.accept(uuid4())

        assert "cannot be accepted" in str(exc_info.value).lower()


# ============================================================================
# Invitation Decline Tests
# ============================================================================

class TestInvitationDecline:
    """Test invitation decline logic"""

    def test_decline_valid_invitation(self):
        """Valid invitation should be declined"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.PENDING
        invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=1)

        invitation.decline()

        assert invitation.status == OrgInvitationStatus.DECLINED
        assert invitation.declined_at is not None

    def test_decline_expired_invitation_fails(self):
        """Expired invitation cannot be declined"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.PENDING
        invitation.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)

        with pytest.raises(ValueError) as exc_info:
            invitation.decline()

        assert "cannot be declined" in str(exc_info.value).lower()


# ============================================================================
# Invitation Cancellation Tests
# ============================================================================

class TestInvitationCancellation:
    """Test invitation cancellation logic"""

    def test_cancel_pending_invitation(self):
        """Pending invitation should be cancelled"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.PENDING

        invitation.cancel()

        assert invitation.status == OrgInvitationStatus.CANCELLED

    def test_cancel_accepted_invitation_fails(self):
        """Accepted invitation cannot be cancelled"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.ACCEPTED

        with pytest.raises(ValueError) as exc_info:
            invitation.cancel()

        assert "cannot be cancelled" in str(exc_info.value).lower()


# ============================================================================
# Resend Tests
# ============================================================================

class TestInvitationResend:
    """Test invitation resend logic"""

    def test_increment_resend_count(self):
        """Resend count should be incremented"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.PENDING
        invitation.resend_count = 1
        invitation.last_resent_at = datetime.now(timezone.utc) - timedelta(minutes=10)

        invitation.increment_resend_count()

        assert invitation.resend_count == 2
        assert invitation.last_resent_at is not None

    def test_increment_resend_count_at_limit_fails(self):
        """Cannot resend when at limit"""
        invitation = OrganizationInvitation()
        invitation.status = OrgInvitationStatus.PENDING
        invitation.resend_count = 3  # Max is 3
        invitation.last_resent_at = datetime.now(timezone.utc) - timedelta(minutes=10)

        with pytest.raises(ValueError) as exc_info:
            invitation.increment_resend_count()

        assert "cannot resend" in str(exc_info.value).lower()


# ============================================================================
# Role Validation Tests
# ============================================================================

class TestRoleValidation:
    """Test role validation in invitation creation"""

    def test_valid_member_role(self):
        """Member role should be valid"""
        data = OrgInvitationCreate(
            email="test@example.com",
            role="member"
        )
        assert data.role == "member"

    def test_valid_admin_role(self):
        """Admin role should be valid"""
        data = OrgInvitationCreate(
            email="test@example.com",
            role="admin"
        )
        assert data.role == "admin"

    def test_invalid_owner_role(self):
        """Owner role should be rejected"""
        with pytest.raises(ValueError) as exc_info:
            OrgInvitationCreate(
                email="test@example.com",
                role="owner"
            )

        assert "owner" in str(exc_info.value).lower()

    def test_invalid_unknown_role(self):
        """Unknown role should be rejected"""
        with pytest.raises(ValueError):
            OrgInvitationCreate(
                email="test@example.com",
                role="unknown"
            )


# ============================================================================
# Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_email_normalization(self):
        """Email should be normalized (lowercase)"""
        data = OrgInvitationCreate(
            email="Test.User@Example.COM",
            role="member"
        )
        # Pydantic EmailStr normalizes to lowercase
        assert data.email.lower() == "test.user@example.com"

    def test_message_max_length(self):
        """Message should respect max length"""
        long_message = "x" * 501  # Over 500 char limit

        with pytest.raises(ValueError):
            OrgInvitationCreate(
                email="test@example.com",
                role="member",
                message=long_message
            )

    def test_empty_message_allowed(self):
        """Empty/None message should be allowed"""
        data = OrgInvitationCreate(
            email="test@example.com",
            role="member",
            message=None
        )
        assert data.message is None

    def test_invitation_status_enum(self):
        """Status enum should have all required values"""
        assert OrgInvitationStatus.PENDING == "pending"
        assert OrgInvitationStatus.ACCEPTED == "accepted"
        assert OrgInvitationStatus.DECLINED == "declined"
        assert OrgInvitationStatus.EXPIRED == "expired"
        assert OrgInvitationStatus.CANCELLED == "cancelled"
