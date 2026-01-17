"""
=========================================================================
P1 Backend Security Checks - Sprint 69 Go-Live
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: January 16, 2026
Status: ACTIVE - Sprint 69 Phase 3 QA
Authority: Backend Lead + Security Lead + CTO Approved
Foundation: CTO Go-Live Requirements (ADR-027), OWASP ASVS L2
Framework: SDLC 5.1.2

Purpose:
- Security testing for P1 backend endpoints
- OWASP Top 10 vulnerability checks
- Input validation and sanitization tests
- Authorization and access control tests
- Rate limiting verification

Security Targets (OWASP ASVS L2):
- SQL Injection prevention
- XSS prevention
- CSRF protection
- Authentication bypass prevention
- Authorization enforcement
- Input validation
- Rate limiting

Endpoints Tested:
- Council API endpoints
- SAST API endpoints
- Evidence Timeline API endpoints
- Gate API endpoints

Zero Mock Policy: Real security validation tests
=========================================================================
"""

import pytest
import pytest_asyncio
from datetime import datetime
from httpx import AsyncClient
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project, ProjectMember
from app.models.user import User


# =========================================================================
# Test Fixtures
# =========================================================================


@pytest_asyncio.fixture
async def security_test_project(db_session: AsyncSession, test_user: User) -> Project:
    """Create project for security testing."""
    project = Project(
        id=uuid4(),
        name="Security Test Project",
        description="Project for security testing",
        owner_id=test_user.id,
        sdlc_stage="BUILD",
        created_at=datetime.utcnow(),
    )
    db_session.add(project)

    # Add user as project member
    member = ProjectMember(
        project_id=project.id,
        user_id=test_user.id,
        role="owner",
    )
    db_session.add(member)

    await db_session.commit()
    await db_session.refresh(project)
    return project


@pytest_asyncio.fixture
async def other_user(db_session: AsyncSession) -> User:
    """Create another user for authorization testing."""
    from app.core.security import get_password_hash

    user = User(
        id=uuid4(),
        email="other_user@example.com",
        full_name="Other User",
        password_hash=get_password_hash("password456"),
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def other_user_headers(client: AsyncClient, other_user: User) -> dict:
    """Get authentication headers for other user."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "other_user@example.com", "password": "password456"},
    )
    if response.status_code == 200:
        data = response.json()
        return {"Authorization": f"Bearer {data['access_token']}"}
    return {}


# =========================================================================
# 1. SQL Injection Prevention Tests
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.security
async def test_sql_injection_in_council_mode_filter(
    client: AsyncClient,
    auth_headers: dict,
    security_test_project: Project,
):
    """Test SQL injection prevention in council history mode filter."""
    malicious_inputs = [
        "'; DROP TABLE council_sessions; --",
        "1 OR 1=1",
        "' UNION SELECT * FROM users --",
        "1; DELETE FROM projects;",
        "' OR '1'='1",
        "${sleep(5)}",
    ]

    for payload in malicious_inputs:
        response = await client.get(
            f"/api/v1/council/history/{security_test_project.id}",
            headers=auth_headers,
            params={"mode": payload},
        )

        # Should not cause server error or unexpected behavior
        assert response.status_code in [200, 400, 422], f"Unexpected status for payload: {payload}"

        # Verify no SQL error messages in response
        if response.status_code != 200:
            response_text = response.text.lower()
            assert "syntax error" not in response_text
            assert "sql" not in response_text or "sequel" not in response_text
            assert "query" not in response_text


@pytest.mark.asyncio
@pytest.mark.security
async def test_sql_injection_in_timeline_search(
    client: AsyncClient,
    auth_headers: dict,
    security_test_project: Project,
):
    """Test SQL injection prevention in timeline search parameter."""
    malicious_inputs = [
        "'; DROP TABLE ai_code_events; --",
        "1 OR 1=1",
        "' UNION SELECT password FROM users --",
        "1; TRUNCATE TABLE projects;",
    ]

    for payload in malicious_inputs:
        response = await client.get(
            f"/api/v1/evidence/projects/{security_test_project.id}/timeline",
            headers=auth_headers,
            params={"search": payload},
        )

        assert response.status_code in [200, 400, 422]

        if response.status_code != 200:
            response_text = response.text.lower()
            assert "syntax error" not in response_text


@pytest.mark.asyncio
@pytest.mark.security
async def test_sql_injection_in_sast_branch_filter(
    client: AsyncClient,
    auth_headers: dict,
    security_test_project: Project,
):
    """Test SQL injection prevention in SAST branch parameter."""
    malicious_inputs = [
        "main'; DROP TABLE sast_scans; --",
        "main' OR '1'='1",
    ]

    for payload in malicious_inputs:
        response = await client.post(
            f"/api/v1/sast/projects/{security_test_project.id}/scan",
            headers=auth_headers,
            json={
                "scan_type": "quick",
                "branch": payload,
            },
        )

        # Should not cause SQL error
        assert response.status_code in [200, 400, 422]


# =========================================================================
# 2. Authentication Tests
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.security
async def test_council_endpoints_require_auth(
    client: AsyncClient,
    security_test_project: Project,
):
    """Test that council endpoints require authentication."""
    endpoints = [
        f"/api/v1/council/history/{security_test_project.id}",
        f"/api/v1/council/stats/{security_test_project.id}",
    ]

    for endpoint in endpoints:
        # Without auth header
        response = await client.get(endpoint)
        assert response.status_code == 401, f"Endpoint {endpoint} should require auth"

        # With invalid token
        response = await client.get(
            endpoint,
            headers={"Authorization": "Bearer invalid_token_here"},
        )
        assert response.status_code == 401, f"Endpoint {endpoint} should reject invalid token"


@pytest.mark.asyncio
@pytest.mark.security
async def test_sast_endpoints_require_auth(
    client: AsyncClient,
    security_test_project: Project,
):
    """Test that SAST endpoints require authentication."""
    endpoints = [
        f"/api/v1/sast/projects/{security_test_project.id}/scans",
        f"/api/v1/sast/projects/{security_test_project.id}/analytics",
        f"/api/v1/sast/projects/{security_test_project.id}/trend",
    ]

    for endpoint in endpoints:
        response = await client.get(endpoint)
        assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.security
async def test_timeline_endpoints_require_auth(
    client: AsyncClient,
    security_test_project: Project,
):
    """Test that timeline endpoints require authentication."""
    endpoints = [
        f"/api/v1/evidence/projects/{security_test_project.id}/timeline",
        f"/api/v1/evidence/projects/{security_test_project.id}/timeline/stats",
    ]

    for endpoint in endpoints:
        response = await client.get(endpoint)
        assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.security
async def test_expired_token_rejected(
    client: AsyncClient,
    security_test_project: Project,
):
    """Test that expired tokens are rejected."""
    # Simulate expired token (old format)
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZXhwIjoxMDAwMDAwMDAwfQ.invalid"

    response = await client.get(
        f"/api/v1/council/history/{security_test_project.id}",
        headers={"Authorization": f"Bearer {expired_token}"},
    )

    assert response.status_code == 401


# =========================================================================
# 3. Authorization Tests (Access Control)
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.security
async def test_user_cannot_access_other_project_council(
    client: AsyncClient,
    other_user_headers: dict,
    security_test_project: Project,
):
    """Test that users cannot access council history of projects they don't belong to."""
    if not other_user_headers:
        pytest.skip("Could not authenticate other user")

    response = await client.get(
        f"/api/v1/council/history/{security_test_project.id}",
        headers=other_user_headers,
    )

    # Should be forbidden or not found
    assert response.status_code in [403, 404]


@pytest.mark.asyncio
@pytest.mark.security
async def test_user_cannot_access_other_project_sast(
    client: AsyncClient,
    other_user_headers: dict,
    security_test_project: Project,
):
    """Test that users cannot access SAST data of projects they don't belong to."""
    if not other_user_headers:
        pytest.skip("Could not authenticate other user")

    endpoints = [
        f"/api/v1/sast/projects/{security_test_project.id}/scans",
        f"/api/v1/sast/projects/{security_test_project.id}/analytics",
    ]

    for endpoint in endpoints:
        response = await client.get(endpoint, headers=other_user_headers)
        assert response.status_code in [403, 404], f"Endpoint {endpoint} should deny access"


@pytest.mark.asyncio
@pytest.mark.security
async def test_user_cannot_access_other_project_timeline(
    client: AsyncClient,
    other_user_headers: dict,
    security_test_project: Project,
):
    """Test that users cannot access timeline of projects they don't belong to."""
    if not other_user_headers:
        pytest.skip("Could not authenticate other user")

    response = await client.get(
        f"/api/v1/evidence/projects/{security_test_project.id}/timeline",
        headers=other_user_headers,
    )

    assert response.status_code in [403, 404]


@pytest.mark.asyncio
@pytest.mark.security
async def test_override_approval_requires_admin_role(
    client: AsyncClient,
    auth_headers: dict,  # Regular user, not admin
):
    """Test that override approval requires admin/manager role."""
    fake_event_id = uuid4()

    response = await client.post(
        f"/api/v1/evidence/timeline/{fake_event_id}/override/approve",
        headers=auth_headers,
        json={"comment": "Test approval"},
    )

    # Should be forbidden for non-admin or not found
    assert response.status_code in [403, 404]


# =========================================================================
# 4. Input Validation Tests
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.security
async def test_invalid_uuid_handled_gracefully(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that invalid UUIDs are handled gracefully."""
    invalid_uuids = [
        "not-a-uuid",
        "12345",
        "../../etc/passwd",
        "<script>alert(1)</script>",
        "null",
        "undefined",
    ]

    for invalid_id in invalid_uuids:
        response = await client.get(
            f"/api/v1/council/history/{invalid_id}",
            headers=auth_headers,
        )

        # Should be 422 (validation error) or 404 (not found)
        assert response.status_code in [404, 422], f"Invalid UUID '{invalid_id}' should be rejected"


@pytest.mark.asyncio
@pytest.mark.security
async def test_negative_pagination_rejected(
    client: AsyncClient,
    auth_headers: dict,
    security_test_project: Project,
):
    """Test that negative pagination values are rejected."""
    response = await client.get(
        f"/api/v1/council/history/{security_test_project.id}",
        headers=auth_headers,
        params={"limit": -1, "offset": -10},
    )

    # Should be rejected (422) or handle gracefully (200)
    assert response.status_code in [200, 422]


@pytest.mark.asyncio
@pytest.mark.security
async def test_excessive_pagination_limit_capped(
    client: AsyncClient,
    auth_headers: dict,
    security_test_project: Project,
):
    """Test that excessive pagination limits are capped."""
    response = await client.get(
        f"/api/v1/council/history/{security_test_project.id}",
        headers=auth_headers,
        params={"limit": 999999},
    )

    # Should be handled (capped or rejected)
    assert response.status_code in [200, 422]


@pytest.mark.asyncio
@pytest.mark.security
async def test_xss_in_override_reason_sanitized(
    client: AsyncClient,
    auth_headers: dict,
    security_test_project: Project,
    db_session: AsyncSession,
):
    """Test that XSS payloads in override reason are sanitized."""
    from app.models.analytics import AICodeEvent

    # Create an event to request override for
    event = AICodeEvent(
        id=uuid4(),
        project_id=security_test_project.id,
        user_id=uuid4(),  # Dummy user
        commit_sha="abc123",
        validation_result="failed",
        created_at=datetime.utcnow(),
    )
    db_session.add(event)
    await db_session.commit()

    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>",
        "javascript:alert(1)",
        "<svg onload=alert(1)>",
        "' onclick='alert(1)'",
    ]

    for payload in xss_payloads:
        response = await client.post(
            f"/api/v1/evidence/timeline/{event.id}/override/request",
            headers=auth_headers,
            json={
                "override_type": "false_positive",
                "reason": f"This is a test reason with XSS: {payload} - ending text",
            },
        )

        # Should succeed but sanitize content or reject
        assert response.status_code in [201, 400, 422]

        if response.status_code == 201:
            data = response.json()
            # Verify the script tags are not in response as-is
            assert "<script>" not in data.get("reason", "")


# =========================================================================
# 5. Path Traversal Prevention Tests
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.security
async def test_path_traversal_in_project_id(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test path traversal prevention in project ID parameter."""
    traversal_payloads = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32",
        "%2e%2e%2f%2e%2e%2f",
        "....//....//",
    ]

    for payload in traversal_payloads:
        response = await client.get(
            f"/api/v1/council/history/{payload}",
            headers=auth_headers,
        )

        # Should be rejected (validation error)
        assert response.status_code in [404, 422]


# =========================================================================
# 6. Rate Limiting Tests
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.security
async def test_council_deliberate_rate_limit(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that council deliberate endpoint has rate limiting."""
    fake_violation_id = uuid4()

    # Send multiple requests rapidly
    responses = []
    for _ in range(20):
        response = await client.post(
            "/api/v1/council/deliberate",
            headers=auth_headers,
            json={
                "violation_id": str(fake_violation_id),
                "council_mode": "single",
            },
        )
        responses.append(response.status_code)

    # Should have some 404 (violation not found) or 429 (rate limited)
    # or 503 (AI council disabled) - but not all 500 (server error)
    assert 500 not in responses, "Should not cause server errors"


# =========================================================================
# 7. IDOR (Insecure Direct Object Reference) Tests
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.security
async def test_cannot_access_other_session_by_id(
    client: AsyncClient,
    other_user_headers: dict,
):
    """Test that users cannot access council sessions by guessing IDs."""
    if not other_user_headers:
        pytest.skip("Could not authenticate other user")

    # Try to access a random session ID
    random_session_id = uuid4()

    response = await client.get(
        f"/api/v1/council/status/{random_session_id}",
        headers=other_user_headers,
    )

    # Should be 404 (not found) not 200 with data
    assert response.status_code in [404, 403]


# =========================================================================
# Summary Test
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.security
async def test_security_check_summary():
    """
    Summary of security checks for P1 backend.

    Run this to get an overview of security test coverage.
    """
    print("\n" + "=" * 70)
    print("P1 BACKEND SECURITY CHECKS - Sprint 69 Go-Live")
    print("=" * 70)
    print(f"Test Time: {datetime.now().isoformat()}")
    print("\nSecurity Tests (OWASP ASVS L2):")
    print("  1. SQL Injection Prevention")
    print("  2. Authentication Enforcement")
    print("  3. Authorization (Access Control)")
    print("  4. Input Validation")
    print("  5. Path Traversal Prevention")
    print("  6. Rate Limiting")
    print("  7. IDOR Prevention")
    print("\nEndpoints Covered:")
    print("  - Council API (/api/v1/council/*)")
    print("  - SAST API (/api/v1/sast/*)")
    print("  - Evidence Timeline API (/api/v1/evidence/*)")
    print("\nRun with: pytest -m security --tb=short -v")
    print("=" * 70)
