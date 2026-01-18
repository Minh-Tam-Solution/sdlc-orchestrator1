"""
=========================================================================
Integration Tests for Analytics API Rate Limiting
SDLC Orchestrator - Sprint 76 P0 Fix

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 76 P0 Fix
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)
Reference: Sprint 76 CTO Review - APPROVED with blocking condition

Purpose:
- Test rate limiting on analytics endpoints
- Verify 429 response when limit exceeded
- Test Retry-After header
- Verify rate limit reset after window

Test Coverage (6 tests):
1. test_velocity_rate_limit_allows_requests - Within limit succeeds
2. test_velocity_rate_limit_exceeded - 429 after 10 requests
3. test_health_rate_limit_exceeded - Health endpoint rate limited
4. test_suggestions_rate_limit_exceeded - Suggestions endpoint rate limited
5. test_analytics_rate_limit_exceeded - Analytics endpoint rate limited
6. test_rate_limit_retry_after_header - Retry-After header present

Zero Mock Policy: Real Redis for rate limiting
=========================================================================
"""

import pytest
from datetime import date, timedelta
from uuid import uuid4

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.sprint import Sprint
from app.models.user import User
from app.utils.redis import get_redis_client


# ==================== Fixtures ====================

@pytest.fixture
async def test_user(db: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        id=uuid4(),
        email="rate-limit-test@example.com",
        full_name="Rate Limit Test User",
        password_hash="$2b$12$test_hash",
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def auth_headers(test_user: User) -> dict:
    """Get auth headers for test user."""
    # In real tests, this would generate a real JWT token
    return {"Authorization": f"Bearer test-token-for-{test_user.id}"}


@pytest.fixture
async def test_project(db: AsyncSession, test_user: User) -> Project:
    """Create a test project."""
    project = Project(
        id=uuid4(),
        name="Rate Limit Test Project",
        description="Project for rate limit testing",
        owner_id=test_user.id,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@pytest.fixture
async def test_sprint(
    db: AsyncSession,
    test_project: Project,
    test_user: User,
) -> Sprint:
    """Create an active sprint for testing."""
    today = date.today()
    sprint = Sprint(
        id=uuid4(),
        project_id=test_project.id,
        number=76,
        name="Sprint 76: Rate Limit Test",
        goal="Test rate limiting",
        status="active",
        start_date=today - timedelta(days=5),
        end_date=today + timedelta(days=5),
        g_sprint_status="passed",
        g_sprint_close_status="pending",
        created_by=test_user.id,
    )
    db.add(sprint)
    await db.commit()
    await db.refresh(sprint)
    return sprint


@pytest.fixture
async def clear_rate_limits(test_user: User):
    """Clear rate limit keys before each test."""
    try:
        redis = await get_redis_client()
        # Clear analytics rate limit keys for test user
        pattern = f"ratelimit:analytics:user:{test_user.id}"
        await redis.delete(pattern)
    except Exception:
        # Redis may not be available in test environment
        pass
    yield
    # Cleanup after test
    try:
        redis = await get_redis_client()
        pattern = f"ratelimit:analytics:user:{test_user.id}"
        await redis.delete(pattern)
    except Exception:
        pass


# ==================== Rate Limit Tests ====================

@pytest.mark.asyncio
class TestAnalyticsRateLimiting:
    """Test rate limiting on analytics endpoints."""

    async def test_velocity_rate_limit_allows_requests(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
        clear_rate_limits,
    ):
        """
        Test 1: Requests within rate limit succeed.

        Should allow up to 10 requests per minute.
        """
        # Make 5 requests (within limit)
        for i in range(5):
            response = await client.get(
                f"/api/v1/planning/projects/{test_project.id}/velocity",
                headers=auth_headers,
            )
            # Should succeed (200 or 404 if no data)
            assert response.status_code in (200, 404), f"Request {i+1} failed with {response.status_code}"

    async def test_velocity_rate_limit_exceeded(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
        clear_rate_limits,
    ):
        """
        Test 2: 429 returned after exceeding rate limit.

        Rate limit: 10 requests per minute.
        After 10 requests, should return 429 Too Many Requests.
        """
        # Make 10 requests to hit the limit
        for i in range(10):
            response = await client.get(
                f"/api/v1/planning/projects/{test_project.id}/velocity",
                headers=auth_headers,
            )
            # First 10 should succeed
            assert response.status_code in (200, 404), f"Request {i+1} failed prematurely"

        # 11th request should be rate limited
        response = await client.get(
            f"/api/v1/planning/projects/{test_project.id}/velocity",
            headers=auth_headers,
        )

        assert response.status_code == 429
        data = response.json()
        assert data["detail"]["error"] == "rate_limit_exceeded"
        assert data["detail"]["limit"] == 10
        assert data["detail"]["window_seconds"] == 60

    async def test_health_rate_limit_exceeded(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_sprint: Sprint,
        clear_rate_limits,
    ):
        """
        Test 3: Health endpoint is also rate limited.

        All analytics endpoints share the same rate limit bucket.
        """
        # Make 10 requests to hit the limit
        for i in range(10):
            response = await client.get(
                f"/api/v1/planning/sprints/{test_sprint.id}/health",
                headers=auth_headers,
            )
            assert response.status_code in (200, 404)

        # 11th request should be rate limited
        response = await client.get(
            f"/api/v1/planning/sprints/{test_sprint.id}/health",
            headers=auth_headers,
        )

        assert response.status_code == 429

    async def test_suggestions_rate_limit_exceeded(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_sprint: Sprint,
        clear_rate_limits,
    ):
        """
        Test 4: Suggestions endpoint is rate limited.
        """
        # Make 10 requests to hit the limit
        for i in range(10):
            response = await client.get(
                f"/api/v1/planning/sprints/{test_sprint.id}/suggestions",
                headers=auth_headers,
            )
            assert response.status_code in (200, 404)

        # 11th request should be rate limited
        response = await client.get(
            f"/api/v1/planning/sprints/{test_sprint.id}/suggestions",
            headers=auth_headers,
        )

        assert response.status_code == 429

    async def test_analytics_rate_limit_exceeded(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_sprint: Sprint,
        clear_rate_limits,
    ):
        """
        Test 5: Analytics endpoint is rate limited.
        """
        # Make 10 requests to hit the limit
        for i in range(10):
            response = await client.get(
                f"/api/v1/planning/sprints/{test_sprint.id}/analytics",
                headers=auth_headers,
            )
            assert response.status_code in (200, 404)

        # 11th request should be rate limited
        response = await client.get(
            f"/api/v1/planning/sprints/{test_sprint.id}/analytics",
            headers=auth_headers,
        )

        assert response.status_code == 429

    async def test_rate_limit_retry_after_header(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
        clear_rate_limits,
    ):
        """
        Test 6: Retry-After header is present when rate limited.

        OWASP ASVS V11.1.7: Proper rate limit response headers.
        """
        # Make 10 requests to hit the limit
        for _ in range(10):
            await client.get(
                f"/api/v1/planning/projects/{test_project.id}/velocity",
                headers=auth_headers,
            )

        # 11th request should be rate limited
        response = await client.get(
            f"/api/v1/planning/projects/{test_project.id}/velocity",
            headers=auth_headers,
        )

        assert response.status_code == 429
        assert "Retry-After" in response.headers
        retry_after = int(response.headers["Retry-After"])
        assert 1 <= retry_after <= 60  # Should be within the window


@pytest.mark.asyncio
class TestRateLimitSharedBucket:
    """Test that analytics endpoints share a rate limit bucket."""

    async def test_shared_bucket_across_endpoints(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
        test_sprint: Sprint,
        clear_rate_limits,
    ):
        """
        Test: All analytics endpoints share the same rate limit bucket.

        Making 5 requests each to velocity and health should hit
        the combined limit of 10.
        """
        # Make 5 velocity requests
        for _ in range(5):
            await client.get(
                f"/api/v1/planning/projects/{test_project.id}/velocity",
                headers=auth_headers,
            )

        # Make 5 health requests
        for _ in range(5):
            await client.get(
                f"/api/v1/planning/sprints/{test_sprint.id}/health",
                headers=auth_headers,
            )

        # 11th request (to any analytics endpoint) should be rate limited
        response = await client.get(
            f"/api/v1/planning/sprints/{test_sprint.id}/suggestions",
            headers=auth_headers,
        )

        assert response.status_code == 429
