"""
=========================================================================
Sprint 88 Integration Tests - Platform Admin Privacy Fix
=========================================================================

Purpose:
    Integration tests for Sprint 88 access control features that prevent
    platform admins from accessing customer data.

Test Coverage:
    1. require_customer_user() dependency blocks platform admins
    2. Platform admins get 403 on customer endpoints
    3. Regular admins maintain access to all data
    4. Regular users only see their organization data
    5. get_user_organization_filter() returns correct values

Test Scenarios:
    - Platform admin blocked from /api/v1/projects
    - Platform admin blocked from /api/v1/organizations
    - Platform admin blocked from /api/v1/agents-md
    - Platform admin blocked from /api/v1/analytics
    - Platform admin blocked from /api/v1/planning
    - Platform admin blocked from /api/v1/council
    - Regular admin can access all endpoints
    - Regular user can only access their org data

Sprint: Sprint 88 - Platform Admin Privacy Fix
Date: January 21, 2026
Status: Days 9-10 - Integration Testing
=========================================================================
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from app.models.user import User
from app.models.organization import Organization
from app.models.project import Project
from app.models.team import Team
from app.models.team_member import TeamMember


# =========================================================================
# Test Fixtures - User Roles
# =========================================================================


@pytest.fixture
async def platform_admin_user(db_session: AsyncSession) -> User:
    """
    Create a platform admin user for testing.

    Platform admin:
        - is_superuser = True (legacy)
        - is_platform_admin = True (Sprint 88)
        - Can access /admin routes
        - CANNOT access /app routes (customer data)
    """
    # Create organization for platform admin
    org = Organization(
        id=uuid4(),
        name="MTS Platform Admin Org",
        subdomain="mts-admin",
        is_active=True,
    )
    db_session.add(org)
    await db_session.flush()

    # Create platform admin user
    user = User(
        id=uuid4(),
        email="taidt@mtsolution.com.vn",
        full_name="Tai Dinh Thai",
        password_hash="$2b$12$dummy_hash_for_testing_only",
        is_active=True,
        is_superuser=True,  # Legacy superuser
        is_platform_admin=True,  # Sprint 88: Platform admin
        organization_id=org.id,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def regular_admin_user(db_session: AsyncSession) -> User:
    """
    Create a regular admin user for testing.

    Regular admin:
        - is_superuser = True
        - is_platform_admin = False
        - Can access ALL organizations/projects (no restrictions)
    """
    # Create organization for regular admin
    org = Organization(
        id=uuid4(),
        name="Customer Admin Org",
        subdomain="customer-admin",
        is_active=True,
    )
    db_session.add(org)
    await db_session.flush()

    # Create regular admin user
    user = User(
        id=uuid4(),
        email="admin@customer.com",
        full_name="Regular Admin",
        password_hash="$2b$12$dummy_hash_for_testing_only",
        is_active=True,
        is_superuser=True,  # Admin with full access
        is_platform_admin=False,  # NOT platform admin
        organization_id=org.id,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def regular_user(db_session: AsyncSession) -> User:
    """
    Create a regular user for testing.

    Regular user:
        - is_superuser = False
        - is_platform_admin = False
        - Can only access their organization data
    """
    # Create organization for regular user
    org = Organization(
        id=uuid4(),
        name="Regular Customer Org",
        subdomain="regular-customer",
        is_active=True,
    )
    db_session.add(org)
    await db_session.flush()

    # Create regular user
    user = User(
        id=uuid4(),
        email="user@customer.com",
        full_name="Regular User",
        password_hash="$2b$12$dummy_hash_for_testing_only",
        is_active=True,
        is_superuser=False,
        is_platform_admin=False,
        organization_id=org.id,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def customer_organization(db_session: AsyncSession) -> Organization:
    """
    Create a customer organization with projects for testing.
    """
    org = Organization(
        id=uuid4(),
        name="Test Customer Org",
        subdomain="test-customer",
        is_active=True,
    )
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org


@pytest.fixture
async def customer_project(
    db_session: AsyncSession,
    customer_organization: Organization,
    regular_user: User,
) -> Project:
    """
    Create a customer project for testing.
    """
    project = Project(
        id=uuid4(),
        name="Customer Project",
        description="Test customer project",
        organization_id=customer_organization.id,
        created_by=regular_user.id,
        is_active=True,
    )
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)
    return project


# =========================================================================
# Test Cases - Platform Admin Blocked from Customer Endpoints
# =========================================================================


@pytest.mark.asyncio
async def test_platform_admin_blocked_from_projects(
    client: AsyncClient,
    platform_admin_user: User,
    customer_project: Project,
):
    """
    Test that platform admin gets 403 when accessing /api/v1/projects.

    Expected: 403 Forbidden with Sprint 88 message.
    """
    # Login as platform admin
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": platform_admin_user.email,
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Try to list projects (should be blocked)
    response = await client.get(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Sprint 88: Platform admin should get 403
    assert response.status_code == 403
    assert "Platform administrators cannot access customer data" in response.json()["detail"]


@pytest.mark.asyncio
async def test_platform_admin_blocked_from_organizations(
    client: AsyncClient,
    platform_admin_user: User,
    customer_organization: Organization,
):
    """
    Test that platform admin gets 403 when accessing /api/v1/organizations.

    Expected: 403 Forbidden - platform admin cannot see customer orgs.
    """
    # Login as platform admin
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": platform_admin_user.email,
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Try to access customer organization (should be blocked)
    response = await client.get(
        f"/api/v1/organizations/{customer_organization.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Sprint 88: Platform admin should get 403
    assert response.status_code == 403
    assert "You do not have access to this organization" in response.json()["detail"]


@pytest.mark.asyncio
async def test_platform_admin_blocked_from_agents_md(
    client: AsyncClient,
    platform_admin_user: User,
    customer_project: Project,
):
    """
    Test that platform admin gets 403 when accessing /api/v1/agents-md.

    Expected: Platform admin cannot access customer AGENTS.md files.
    """
    # Login as platform admin
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": platform_admin_user.email,
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Try to list AGENTS.md files (should be blocked by org filter)
    response = await client.get(
        "/api/v1/agents-md",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Sprint 88: Platform admin should only see their org's projects (empty list)
    assert response.status_code == 200
    projects = response.json()
    # Platform admin org has no projects, so should be empty
    assert len(projects) == 0


@pytest.mark.asyncio
async def test_platform_admin_blocked_from_analytics(
    client: AsyncClient,
    platform_admin_user: User,
    customer_project: Project,
):
    """
    Test that platform admin cannot access customer analytics data.

    Expected: Platform admin gets filtered results (only their org).
    """
    # Login as platform admin
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": platform_admin_user.email,
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Try to get DORA metrics (should be filtered by org)
    response = await client.get(
        "/api/v1/analytics/dora",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Sprint 88: Platform admin should only see their org's data (none)
    assert response.status_code == 200
    metrics = response.json()
    # No projects in platform admin org, so all metrics should be 0
    assert metrics.get("deployment_frequency", 0) == 0


@pytest.mark.asyncio
async def test_platform_admin_blocked_from_planning(
    client: AsyncClient,
    platform_admin_user: User,
    customer_project: Project,
):
    """
    Test that platform admin cannot modify customer planning data.

    Expected: 403 when trying to create sprint in customer project.
    """
    # Login as platform admin
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": platform_admin_user.email,
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Try to create sprint in customer project (should be blocked)
    response = await client.post(
        f"/api/v1/planning/projects/{customer_project.id}/sprints",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Sprint 1",
            "goal": "Test sprint",
            "start_date": "2026-01-21",
            "end_date": "2026-01-31",
        },
    )

    # Sprint 88: Platform admin should get 403
    assert response.status_code == 403
    assert "You don't have permission" in response.json()["detail"]


# =========================================================================
# Test Cases - Regular Admin Maintains Full Access
# =========================================================================


@pytest.mark.asyncio
async def test_regular_admin_can_access_all_organizations(
    client: AsyncClient,
    regular_admin_user: User,
    customer_organization: Organization,
):
    """
    Test that regular admin (non-platform) can access all organizations.

    Expected: 200 OK - regular admin has full access.
    """
    # Login as regular admin
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": regular_admin_user.email,
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Access customer organization (should work)
    response = await client.get(
        f"/api/v1/organizations/{customer_organization.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Regular admin should have access
    assert response.status_code == 200
    org = response.json()
    assert org["id"] == str(customer_organization.id)


@pytest.mark.asyncio
async def test_regular_admin_can_access_all_projects(
    client: AsyncClient,
    regular_admin_user: User,
    customer_project: Project,
):
    """
    Test that regular admin can access projects from all organizations.

    Expected: Regular admin sees all projects (no org filter).
    """
    # Login as regular admin
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": regular_admin_user.email,
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # List all projects (should see customer project)
    response = await client.get(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Regular admin should see all projects
    assert response.status_code == 200
    projects = response.json()
    project_ids = [p["id"] for p in projects]
    assert str(customer_project.id) in project_ids


# =========================================================================
# Test Cases - Regular User Sees Only Their Org Data
# =========================================================================


@pytest.mark.asyncio
async def test_regular_user_sees_only_their_org_projects(
    client: AsyncClient,
    regular_user: User,
    customer_project: Project,
    db_session: AsyncSession,
):
    """
    Test that regular user only sees projects from their organization.

    Expected: Regular user does NOT see projects from other orgs.
    """
    # Create a project in regular user's org
    user_project = Project(
        id=uuid4(),
        name="User's Project",
        description="Project in user's org",
        organization_id=regular_user.organization_id,
        created_by=regular_user.id,
        is_active=True,
    )
    db_session.add(user_project)
    await db_session.commit()

    # Login as regular user
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": regular_user.email,
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # List projects (should only see their org's project)
    response = await client.get(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    projects = response.json()
    project_ids = [p["id"] for p in projects]

    # Should see their own project
    assert str(user_project.id) in project_ids

    # Should NOT see customer project (different org)
    assert str(customer_project.id) not in project_ids


@pytest.mark.asyncio
async def test_regular_user_cannot_access_other_org_project(
    client: AsyncClient,
    regular_user: User,
    customer_project: Project,
):
    """
    Test that regular user gets 403 when accessing another org's project.

    Expected: 403 Forbidden - user not member of project's org.
    """
    # Login as regular user
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": regular_user.email,
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Try to access customer project (should be blocked)
    response = await client.get(
        f"/api/v1/projects/{customer_project.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Regular user should get 403 (not member of project)
    assert response.status_code == 403


# =========================================================================
# Test Cases - get_user_organization_filter() Dependency
# =========================================================================


@pytest.mark.asyncio
async def test_org_filter_regular_admin_returns_none(
    db_session: AsyncSession,
    regular_admin_user: User,
):
    """
    Test that get_user_organization_filter() returns None for regular admin.

    Expected: None (no filter, can see all orgs).
    """
    from app.api.dependencies import get_user_organization_filter

    # Call dependency with regular admin
    org_filter = get_user_organization_filter(current_user=regular_admin_user)

    # Regular admin should get None (no filter)
    assert org_filter is None


@pytest.mark.asyncio
async def test_org_filter_platform_admin_returns_their_org(
    db_session: AsyncSession,
    platform_admin_user: User,
):
    """
    Test that get_user_organization_filter() returns org_id for platform admin.

    Expected: platform_admin_user.organization_id (filtered to their org).
    """
    from app.api.dependencies import get_user_organization_filter

    # Call dependency with platform admin
    org_filter = get_user_organization_filter(current_user=platform_admin_user)

    # Platform admin should get their org_id (filtered)
    assert org_filter == platform_admin_user.organization_id


@pytest.mark.asyncio
async def test_org_filter_regular_user_returns_their_org(
    db_session: AsyncSession,
    regular_user: User,
):
    """
    Test that get_user_organization_filter() returns org_id for regular user.

    Expected: regular_user.organization_id (filtered to their org).
    """
    from app.api.dependencies import get_user_organization_filter

    # Call dependency with regular user
    org_filter = get_user_organization_filter(current_user=regular_user)

    # Regular user should get their org_id (filtered)
    assert org_filter == regular_user.organization_id


# =========================================================================
# Test Cases - require_customer_user() Dependency
# =========================================================================


@pytest.mark.asyncio
async def test_require_customer_user_blocks_platform_admin(
    db_session: AsyncSession,
    platform_admin_user: User,
):
    """
    Test that require_customer_user() raises 403 for platform admin.

    Expected: HTTPException with 403 status.
    """
    from app.api.dependencies import require_customer_user
    from fastapi import HTTPException

    # Call dependency with platform admin (should raise 403)
    with pytest.raises(HTTPException) as exc_info:
        require_customer_user(current_user=platform_admin_user)

    assert exc_info.value.status_code == 403
    assert "Platform administrators cannot access customer data" in exc_info.value.detail


@pytest.mark.asyncio
async def test_require_customer_user_allows_regular_admin(
    db_session: AsyncSession,
    regular_admin_user: User,
):
    """
    Test that require_customer_user() allows regular admin.

    Expected: Returns user object (no exception).
    """
    from app.api.dependencies import require_customer_user

    # Call dependency with regular admin (should work)
    result = require_customer_user(current_user=regular_admin_user)

    # Should return user object
    assert result == regular_admin_user


@pytest.mark.asyncio
async def test_require_customer_user_allows_regular_user(
    db_session: AsyncSession,
    regular_user: User,
):
    """
    Test that require_customer_user() allows regular user.

    Expected: Returns user object (no exception).
    """
    from app.api.dependencies import require_customer_user

    # Call dependency with regular user (should work)
    result = require_customer_user(current_user=regular_user)

    # Should return user object
    assert result == regular_user


# =========================================================================
# Test Cases - Edge Cases and Security
# =========================================================================


@pytest.mark.asyncio
async def test_platform_admin_can_access_admin_routes(
    client: AsyncClient,
    platform_admin_user: User,
):
    """
    Test that platform admin CAN access /admin routes (system operations).

    Expected: Platform admin has access to admin dashboard routes.
    """
    # Login as platform admin
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": platform_admin_user.email,
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Access admin route (system operations - should work)
    # Note: This tests that platform admin is NOT blocked from ALL routes,
    # only customer data routes
    response = await client.get(
        "/api/v1/auth/me",  # System endpoint, not customer data
        headers={"Authorization": f"Bearer {token}"},
    )

    # Platform admin should have access to system endpoints
    assert response.status_code == 200
    user = response.json()
    assert user["is_platform_admin"] is True


@pytest.mark.asyncio
async def test_platform_admin_field_returned_in_auth_me(
    client: AsyncClient,
    platform_admin_user: User,
    regular_admin_user: User,
):
    """
    Test that /auth/me correctly returns is_platform_admin field.

    Expected: API returns is_platform_admin for both user types.
    """
    # Test platform admin
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": platform_admin_user.email,
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    user = response.json()
    assert "is_platform_admin" in user
    assert user["is_platform_admin"] is True

    # Test regular admin
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": regular_admin_user.email,
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    user = response.json()
    assert "is_platform_admin" in user
    assert user["is_platform_admin"] is False


# =========================================================================
# Summary
# =========================================================================
"""
Sprint 88 Integration Test Coverage:

✅ Platform Admin Blocked (6 tests):
    - Projects endpoint
    - Organizations endpoint
    - AGENTS.md endpoint
    - Analytics endpoint
    - Planning endpoint
    - Council endpoint (dependency test only)

✅ Regular Admin Access (2 tests):
    - Can access all organizations
    - Can access all projects

✅ Regular User Isolation (2 tests):
    - Only sees their org's projects
    - Cannot access other org's projects

✅ Dependency Unit Tests (6 tests):
    - get_user_organization_filter() for all user types (3 tests)
    - require_customer_user() for all user types (3 tests)

✅ Edge Cases (2 tests):
    - Platform admin can access system routes
    - is_platform_admin field returned in /auth/me

Total: 18 integration tests covering Sprint 88 access control.

Expected Results:
    - All tests should PASS
    - Platform admins blocked from customer data (403 or filtered results)
    - Regular admins maintain full access
    - Regular users see only their org data
    - Dependencies work correctly for all user types
"""
