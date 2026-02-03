"""
=========================================================================
Organizations API Routes - Organization Management Endpoints
SDLC Orchestrator - Sprint 71 (Teams Backend API)

Version: 1.0.0
Date: January 27, 2026
Status: ACTIVE - Sprint 71 Implementation
Authority: Backend Lead + CTO Approved
Reference: ADR-028-Teams-Feature-Architecture
Reference: Teams-API-Specification.md

API Endpoints (4 total):
- POST   /organizations              - Create organization
- GET    /organizations              - List organizations
- GET    /organizations/{org_id}     - Get organization details
- PATCH  /organizations/{org_id}     - Update organization
- GET    /organizations/{org_id}/stats - Organization statistics

Multi-Tenancy:
- Organizations are the root entity for multi-tenancy
- Users belong to one organization
- Teams belong to organizations

Zero Mock Policy: Production-ready API routes
=========================================================================
"""

import logging
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.organization import Organization, UserOrganization
from app.schemas.team import (
    OrganizationCreate,
    OrganizationListResponse,
    OrganizationResponse,
    OrganizationUpdate,
)
from app.schemas.organization_invitation import (
    AddMemberRequest,
    MemberAddedResponse,
)
from app.services.organizations_service import (
    OrganizationNotFoundError,
    OrganizationSlugExistsError,
    OrganizationsService,
    UserNotInOrganizationError,
)

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/organizations", tags=["organizations"])


# =========================================================================
# Helper Functions
# =========================================================================

def org_to_response(
    org,
    teams_count: int | None = None,
    users_count: int | None = None
) -> OrganizationResponse:
    """
    Convert Organization model to OrganizationResponse schema.

    Args:
        org: Organization model instance
        teams_count: Explicit teams count. If None, tries to get from loaded relationship.
        users_count: Explicit users count. If None, tries to get from loaded relationship.

    Note:
        When relationships are eager-loaded via selectinload, we can safely access them.
        Only pass explicit counts when relationships are NOT loaded (e.g., after create).
    """
    # Use explicit counts if provided, otherwise try to get from loaded relationships
    # For newly created orgs, relationships may not be loaded yet - default to 0
    actual_teams_count = teams_count if teams_count is not None else (
        len(org.teams) if hasattr(org, 'teams') and org.teams is not None else 0
    )
    actual_users_count = users_count if users_count is not None else (
        len(org.users) if hasattr(org, 'users') and org.users is not None else 0
    )

    return OrganizationResponse(
        id=org.id,
        name=org.name,
        slug=org.slug,
        plan=org.plan,
        settings=org.settings or {},
        teams_count=actual_teams_count,
        users_count=actual_users_count,
        created_at=org.created_at,
        updated_at=org.updated_at
    )


# =========================================================================
# Organization CRUD Endpoints (S71-T26 to T29)
# =========================================================================

@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Organization",
    description="Create a new organization. The creator is automatically assigned to it."
)
async def create_organization(
    data: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new organization.

    - **name**: Organization display name (2-255 chars)
    - **slug**: URL-safe identifier (globally unique)
    - **plan**: Subscription plan (free, starter, pro, enterprise)
    - **settings**: Organization settings including SASE config

    The authenticated user is automatically assigned to the new organization.
    """
    service = OrganizationsService(db)
    
    try:
        org = await service.create_organization(data, current_user.id)
        return org_to_response(org)
    except OrganizationSlugExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Organization with slug '{e.slug}' already exists"
        )


@router.get(
    "",
    response_model=OrganizationListResponse,
    summary="List Organizations",
    description="List organizations. Regular users see only their own organization."
)
async def list_organizations(
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(20, ge=1, le=100, description="Max results"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List organizations.

    For regular users: Returns only the organization they belong to.
    For superusers: Returns all organizations (for admin purposes).

    - **skip**: Pagination offset (default 0)
    - **limit**: Max results per page (1-100, default 20)
    """
    service = OrganizationsService(db)

    # Sprint 88: Platform admins CANNOT access customer data
    # Only regular admins (non-platform admins) can see all organizations
    user_filter = None if (current_user.is_superuser and not current_user.is_platform_admin) else current_user.id
    
    orgs = await service.list_organizations(
        user_id=user_filter,
        skip=skip,
        limit=limit
    )
    
    return OrganizationListResponse(
        items=[org_to_response(o) for o in orgs],
        total=len(orgs),
        page=skip // limit + 1 if limit > 0 else 1,
        page_size=limit,
        has_next=len(orgs) == limit
    )


@router.get(
    "/{org_id}",
    response_model=OrganizationResponse,
    summary="Get Organization",
    description="Get organization details by ID."
)
async def get_organization(
    org_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed information about a specific organization.

    Returns organization details including:
    - Basic info (name, slug, plan)
    - Settings (MFA requirement, allowed domains, SASE config)
    - Team count
    - User count
    """
    service = OrganizationsService(db)
    
    org = await service.get_organization(org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization {org_id} not found"
        )

    # Sprint 88: Platform admins CANNOT access customer data
    # Check access: user must belong to org or be regular admin (not platform admin)
    is_regular_admin = current_user.is_superuser and not current_user.is_platform_admin

    # Multi-org support: Check if user is a member of this organization
    is_member_result = await db.execute(
        select(UserOrganization).where(
            UserOrganization.user_id == current_user.id,
            UserOrganization.organization_id == org_id
        )
    )
    is_member = is_member_result.scalar_one_or_none() is not None

    # Allow access if: regular admin OR primary org matches OR is a member
    if not is_regular_admin and current_user.organization_id != org_id and not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this organization"
        )

    return org_to_response(org)


@router.patch(
    "/{org_id}",
    response_model=OrganizationResponse,
    summary="Update Organization",
    description="Update organization details. User must be a member."
)
async def update_organization(
    org_id: UUID,
    data: OrganizationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update organization details.

    User must be a member of the organization.

    Updatable fields:
    - **name**: Organization display name
    - **slug**: URL-safe identifier (must be globally unique)
    - **plan**: Subscription plan
    - **settings**: Organization settings
    """
    service = OrganizationsService(db)
    
    try:
        org = await service.update_organization(org_id, data, current_user.id)
        return org_to_response(org)
    except OrganizationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization {org_id} not found"
        )
    except UserNotInOrganizationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization"
        )
    except OrganizationSlugExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Organization with slug '{e.slug}' already exists"
        )


# =========================================================================
# Organization Statistics Endpoint
# =========================================================================

@router.get(
    "/{org_id}/stats",
    summary="Get Organization Statistics",
    description="Get organization metrics and statistics."
)
async def get_organization_statistics(
    org_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed statistics for an organization.

    Returns:
    - **plan**: Subscription plan
    - **teams_count**: Total teams
    - **users_count**: Total users
    - **agentic_maturity**: SASE maturity level
    - **require_mfa**: MFA requirement status
    - **allowed_domains**: Email domain restrictions
    """
    service = OrganizationsService(db)

    # Sprint 88: Platform admins CANNOT access customer data
    # Check access: user must belong to org or be regular admin (not platform admin)
    is_regular_admin = current_user.is_superuser and not current_user.is_platform_admin

    # Multi-org support: Check if user is a member of this organization
    is_member_result = await db.execute(
        select(UserOrganization).where(
            UserOrganization.user_id == current_user.id,
            UserOrganization.organization_id == org_id
        )
    )
    is_member = is_member_result.scalar_one_or_none() is not None

    # Allow access if: regular admin OR primary org matches OR is a member
    if not is_regular_admin and current_user.organization_id != org_id and not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this organization"
        )

    try:
        return await service.get_organization_statistics(org_id)
    except OrganizationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization {org_id} not found"
        )


# =========================================================================
# Direct Member Addition Endpoint (Sprint 146 - ADR-047 Phase 2)
# =========================================================================

@router.post(
    "/{org_id}/members",
    response_model=MemberAddedResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Member Directly",
    description="Add existing user to organization directly (bypass invitation flow)."
)
async def add_member_directly(
    org_id: UUID,
    data: AddMemberRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MemberAddedResponse:
    """
    Add existing user to organization directly (no invitation email).

    **Use Cases**:
    - Enterprise bulk onboarding (HR has employee list)
    - SSO/LDAP integration (auto-provision from directory)
    - Internal teams (faster than invitation flow)

    **Permissions**:
    - Owner: Can add with any role (admin, member)
    - Admin: Can add members only

    **Errors**:
    - 404: User or organization not found
    - 403: Insufficient permissions
    - 409: User already member

    **ADR-047**: Direct member addition endpoint for enterprise use cases.
    """
    # 1. Get organization
    org_result = await db.execute(
        select(Organization).where(Organization.id == org_id)
    )
    org = org_result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization {org_id} not found"
        )

    # 2. Check current user's permission (must be owner or admin in this org)
    membership_result = await db.execute(
        select(UserOrganization).where(
            UserOrganization.organization_id == org_id,
            UserOrganization.user_id == current_user.id,
            UserOrganization.role.in_(["owner", "admin"])
        )
    )
    membership = membership_result.scalar_one_or_none()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organization owners and admins can add members"
        )

    # 3. Role restriction: only owner can add admin
    if data.role == "admin" and membership.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organization owner can add admins"
        )

    # 4. Find user by email
    user_result = await db.execute(
        select(User).where(User.email == data.user_email.lower())
    )
    user_to_add = user_result.scalar_one_or_none()

    if not user_to_add:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {data.user_email} not found. User must be registered first."
        )

    # 5. Check if user is already a member
    existing_result = await db.execute(
        select(UserOrganization).where(
            UserOrganization.user_id == user_to_add.id,
            UserOrganization.organization_id == org_id
        )
    )
    existing = existing_result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {data.user_email} is already a member of this organization"
        )

    # 6. Create membership
    now = datetime.now(timezone.utc)
    new_membership = UserOrganization(
        user_id=user_to_add.id,
        organization_id=org_id,
        role=data.role,
        joined_at=now
    )
    db.add(new_membership)

    # 7. Audit log (optional - log to structured logger)
    logger.info(
        "Member added directly to organization",
        extra={
            "action": "member_added_directly",
            "user_id": str(current_user.id),
            "target_user_id": str(user_to_add.id),
            "organization_id": str(org_id),
            "role": data.role,
            "method": "direct_add"
        }
    )

    await db.commit()

    # 8. TODO: Send notification email (not invitation)
    # This would be implemented via email service
    # send_notification_email(
    #     to_email=user_to_add.email,
    #     subject=f"Added to {org.name}",
    #     template="member_added",
    #     data={"organization_name": org.name, "role": data.role, "added_by": current_user.display_name}
    # )

    return MemberAddedResponse(
        user_id=user_to_add.id,
        organization_id=org_id,
        organization_name=org.name,
        role=data.role,
        joined_at=now,
        added_by={
            "user_id": str(current_user.id),
            "display_name": current_user.display_name or current_user.email
        },
        message=f"Successfully added {data.user_email} to {org.name} as {data.role}"
    )
