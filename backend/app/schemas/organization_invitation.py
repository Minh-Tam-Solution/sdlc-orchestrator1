"""
Organization Invitation Schemas

Pydantic schemas for organization invitation API request/response validation.

Reference: ADR-047-Organization-Invitation-System.md
Sprint: 146
"""
from datetime import datetime
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# ============================================================================
# Request Schemas
# ============================================================================

class OrgInvitationCreate(BaseModel):
    """Request schema for sending organization invitation"""

    email: EmailStr = Field(
        ...,
        description="Email address of invitee",
        example="user@example.com"
    )
    role: str = Field(
        default="member",
        description="Organization role (admin, member). Cannot invite as owner.",
        example="member"
    )
    message: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional custom message",
        example="Join our organization!"
    )

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """
        Validate role is one of allowed values.

        CTO Constraint: Cannot invite as owner.
        """
        allowed_roles = {"admin", "member"}
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of: {allowed_roles}. Cannot invite as 'owner'.")
        return v


class OrgInvitationDecline(BaseModel):
    """Request schema for declining organization invitation"""

    reason: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional reason for declining",
        example="Not interested"
    )


# ============================================================================
# Response Schemas
# ============================================================================

class InviterInfo(BaseModel):
    """Nested schema for inviter information"""
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    display_name: str


class OrganizationInfo(BaseModel):
    """Nested schema for organization information"""
    model_config = ConfigDict(from_attributes=True)

    organization_id: UUID
    organization_name: str
    organization_slug: str
    plan: str


class OrgInvitationResponse(BaseModel):
    """Response schema for organization invitation (list/detail)"""
    model_config = ConfigDict(from_attributes=True)

    invitation_id: UUID = Field(..., description="Unique invitation ID")
    organization_id: UUID = Field(..., description="Organization ID")
    organization_name: str = Field(..., description="Organization display name")
    invited_email: EmailStr = Field(..., description="Email address invited")
    role: str = Field(..., description="Role being invited (admin/member)")
    status: str = Field(..., description="Invitation status (pending/accepted/declined/expired/cancelled)")
    expires_at: datetime = Field(..., description="Expiry timestamp")
    invited_by: dict[str, Any] = Field(..., description="Inviter info (user_id, display_name)")
    created_at: datetime = Field(..., description="Creation timestamp")
    message: Optional[str] = Field(None, description="Optional custom message")


class OrgInvitationDetails(BaseModel):
    """Detailed invitation info for public token lookup"""
    model_config = ConfigDict(from_attributes=True)

    organization: dict[str, Any] = Field(..., description="Organization info")
    invited_email: EmailStr = Field(..., description="Email address invited")
    role: str = Field(..., description="Role being invited")
    status: str = Field(..., description="Invitation status")
    expires_at: datetime = Field(..., description="Expiry timestamp")
    invited_by: dict[str, Any] = Field(..., description="Inviter info")
    created_at: datetime = Field(..., description="Creation timestamp")


class OrgInvitationAccepted(BaseModel):
    """Response schema for successful acceptance"""
    model_config = ConfigDict(from_attributes=True)

    status: str = Field("accepted", description="Status: accepted")
    organization_id: UUID = Field(..., description="Organization ID joined")
    organization_name: str = Field(..., description="Organization name")
    organization_slug: str = Field(..., description="Organization slug")
    role: str = Field(..., description="Role assigned")
    accepted_at: datetime = Field(..., description="Acceptance timestamp")
    redirect_url: str = Field(..., description="URL to redirect user after acceptance")


class OrgInvitationDeclined(BaseModel):
    """Response schema for declined invitation"""
    model_config = ConfigDict(from_attributes=True)

    status: str = Field("declined", description="Status: declined")
    declined_at: datetime = Field(..., description="Decline timestamp")
    message: str = Field(..., description="Confirmation message")


class OrgInvitationResent(BaseModel):
    """Response schema for resent invitation"""
    model_config = ConfigDict(from_attributes=True)

    invitation_id: UUID = Field(..., description="Invitation ID")
    status: str = Field(..., description="Invitation status")
    resend_count: int = Field(..., description="Total resend count")
    last_resent_at: datetime = Field(..., description="Last resend timestamp")
    expires_at: datetime = Field(..., description="New expiry timestamp")
    message: str = Field(..., description="Confirmation message")


# ============================================================================
# List Response Schema
# ============================================================================

class OrgInvitationListResponse(BaseModel):
    """Paginated list of organization invitations"""
    model_config = ConfigDict(from_attributes=True)

    invitations: list[OrgInvitationResponse] = Field(..., description="List of invitations")
    total: int = Field(..., description="Total count of invitations")
    limit: int = Field(..., description="Page size")
    offset: int = Field(..., description="Offset")


# ============================================================================
# Direct Member Addition Schemas (Phase 2 - ADR-047)
# ============================================================================

class AddMemberRequest(BaseModel):
    """
    Request schema for adding member directly (bypass invitation).

    Use Cases:
    - Enterprise bulk onboarding (HR has employee list)
    - SSO/LDAP integration (auto-provision from directory)
    - Internal teams (faster than invitation flow)
    """

    user_email: EmailStr = Field(
        ...,
        description="Email of existing user to add",
        example="existing.user@company.com"
    )
    role: str = Field(
        default="member",
        description="Role: admin or member (cannot set owner)",
        example="member"
    )

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is admin or member (not owner)."""
        if v not in {"admin", "member"}:
            raise ValueError("Role must be 'admin' or 'member' (cannot set 'owner')")
        return v


class MemberAddedResponse(BaseModel):
    """Response schema for successfully added member"""
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID = Field(..., description="Added user's ID")
    organization_id: UUID = Field(..., description="Organization ID")
    organization_name: str = Field(..., description="Organization name")
    role: str = Field(..., description="Assigned role")
    joined_at: datetime = Field(..., description="When user was added")
    added_by: dict[str, Any] = Field(..., description="Admin who added the user")
    message: str = Field(..., description="Confirmation message")
