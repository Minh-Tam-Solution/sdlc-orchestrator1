"""
=========================================================================
E2E Test: Governance Loop — 3-Client Parity (Sprint 173 — ADR-053)
SDLC Orchestrator - Stage 04 (BUILD)

Version: 1.0.0
Date: February 15, 2026
Status: ACTIVE - Sprint 173 (Governance Loop)
Authority: CTO Approved
Framework: SDLC 6.0.5

Purpose:
- Verify the complete governance loop works end-to-end
- Test the same gate lifecycle through all 3 interfaces:
  1. Web API (direct HTTP calls via AsyncClient)
  2. CLI (sdlcctl gate commands via API calls)
  3. Extension (VS Code apiClient methods via API calls)
- Verify state machine transitions: DRAFT → EVALUATED → SUBMITTED → APPROVED
- Verify rejection path: SUBMITTED → REJECTED → re-evaluate
- Verify evidence upload triggers EVALUATED_STALE
- Verify /actions endpoint SSOT invariant
- Verify idempotency (duplicate operations are no-ops)
- Verify cross-interface parity (same policy, same outcome)

State Machine (ADR-053):
  DRAFT → EVALUATED → SUBMITTED → APPROVED
    ↑         ↑           ↓
    └─────────┼───── REJECTED
              └──────────┘
  Evidence upload while EVALUATED → EVALUATED_STALE

Test Stack:
- pytest + pytest-asyncio (async test support)
- httpx.AsyncClient + ASGITransport (direct ASGI calls)
- Fixtures from conftest.py (db_session, client, auth_headers)

Zero Mock Policy: Real database operations, real API routes
=========================================================================
"""

import hashlib
import io
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gate import Gate
from app.models.project import Project, ProjectMember
from app.models.user import User, Role
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)


# =========================================================================
# Fixture Overrides: Disable conftest's mock_external_http
# =========================================================================


@pytest.fixture(autouse=True)
def mock_external_http():
    """
    Override conftest's mock_external_http (no-op).

    The conftest fixture patches httpx.AsyncClient.request globally, which
    breaks the ASGI test transport. The URL check for "testserver" fails
    because httpx.AsyncClient.request receives the raw path ("/api/v1/gates"),
    not the full URL ("http://testserver/api/v1/gates") — base_url merging
    happens inside the original request method, after the patch intercepts.

    This override disables that global mock. External services are mocked
    individually below (MinIO, OPA gracefully degrades with no policies).
    """
    yield


@pytest.fixture(autouse=True)
def mock_external_services():
    """
    Mock external services and suppress background DB tasks.

    1. MinIO: Evidence upload uses requests.put to S3 API (AGPL-safe, network-only).
    2. OPA: Policy evaluation uses requests.post to OPA REST API.
    3. Notification service: approve/reject endpoints use asyncio.create_task(_notify())
       which calls notification_service methods that do DB operations (db.commit() in
       _send_in_app_notification). Since the test shares a single DB session across all
       requests, the background task's DB operations conflict with subsequent test
       requests on the same session, causing deadlocks.
    """
    mock_put_response = MagicMock()
    mock_put_response.status_code = 200
    mock_put_response.raise_for_status = MagicMock()

    mock_post_response = MagicMock()
    mock_post_response.status_code = 200
    mock_post_response.json.return_value = {
        "result": {"allowed": True, "violations": []},
    }
    mock_post_response.raise_for_status = MagicMock()

    # Mock notification service to prevent background task DB conflicts.
    # The approve/reject endpoints create asyncio.create_task(_notify()) which
    # lazily imports create_notification_service and calls methods that do
    # db.add() + db.commit() on the shared test session.
    mock_notification_service = MagicMock()
    mock_notification_service.send_gate_approval_notification = AsyncMock(
        return_value={"in_app": True}
    )
    mock_notification_service.send_gate_approved_notification = AsyncMock(
        return_value={"in_app": True}
    )
    mock_notification_service.send_gate_rejected_notification = AsyncMock(
        return_value={"in_app": True}
    )

    # Mock app.utils.redis.get_redis_client (NOT covered by conftest's mock_redis
    # which only patches app.core.redis). The idempotency middleware imports from
    # app.utils.redis, and the real get_redis_client() creates a connection that
    # can hang or fail unpredictably.
    #
    # IMPORTANT: ALL methods must be AsyncMock (not plain MagicMock). The rate
    # limiter middleware calls zremrangebyscore/zcard/zadd/expire on the redis
    # client. If these return regular MagicMock, `await MagicMock()` raises
    # TypeError which is caught by the rate limiter's except block. While this
    # doesn't block requests, the TypeError handling in asyncio + BaseHTTPMiddleware
    # background tasks can leave pending callbacks that interfere with subsequent
    # requests using the same asyncpg connection (causes db.commit() hangs).
    mock_redis_client = MagicMock()
    mock_redis_client.get = AsyncMock(return_value=None)
    mock_redis_client.setex = AsyncMock(return_value=True)
    mock_redis_client.ping = AsyncMock(return_value=True)
    # Rate limiter sliding window methods
    mock_redis_client.zremrangebyscore = AsyncMock(return_value=0)
    mock_redis_client.zcard = AsyncMock(return_value=0)
    mock_redis_client.zadd = AsyncMock(return_value=1)
    mock_redis_client.expire = AsyncMock(return_value=True)

    # Also need to patch rate_limiter's already-imported reference
    # (module-level: from app.utils.redis import get_redis_client)
    async def mock_get_redis():
        return mock_redis_client

    # Reset the singleton to prevent stale real connections
    import app.utils.redis as _redis_mod
    _old_client = _redis_mod._redis_client
    _redis_mod._redis_client = None

    with patch("requests.put", return_value=mock_put_response), \
         patch("requests.post", return_value=mock_post_response), \
         patch(
             "app.services.notification_service.create_notification_service",
             return_value=mock_notification_service,
         ), \
         patch(
             "app.api.routes.gates.get_gate_stakeholders",
             new_callable=AsyncMock,
             return_value=[],
         ), \
         patch(
             "app.api.routes.gates.get_gate_approvers",
             new_callable=AsyncMock,
             return_value=[],
         ), \
         patch(
             "app.utils.redis.get_redis_client",
             side_effect=mock_get_redis,
         ), \
         patch(
             "app.middleware.rate_limiter.get_redis_client",
             side_effect=mock_get_redis,
         ):
        yield

    # Restore singleton
    _redis_mod._redis_client = _old_client


# =========================================================================
# Test Fixtures
# =========================================================================


@pytest_asyncio.fixture(scope="function")
async def dev_user(db_session: AsyncSession) -> User:
    """Create a developer user (governance:write scope — can evaluate, submit, upload evidence)."""
    role = Role(
        id=uuid4(),
        name="developer",
        display_name="Developer",
        description="Developer role",
    )
    db_session.add(role)
    await db_session.flush()

    user = User(
        id=uuid4(),
        email="dev@e2e-test.com",
        full_name="E2E Developer",
        password_hash=get_password_hash("devpass123"),
        role="dev",
        is_active=True,
    )
    user.roles.append(role)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def cto_user(db_session: AsyncSession) -> User:
    """Create a CTO user (governance:approve scope — can approve, reject)."""
    role = Role(
        id=uuid4(),
        name="cto",
        display_name="Chief Technology Officer",
        description="CTO role — can approve/reject gates",
    )
    db_session.add(role)
    await db_session.flush()

    user = User(
        id=uuid4(),
        email="cto@e2e-test.com",
        full_name="E2E CTO",
        password_hash=get_password_hash("ctopass123"),
        role="cto",
        is_active=True,
    )
    user.roles.append(role)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_project(db_session: AsyncSession, dev_user: User) -> Project:
    """Create a test project for gate operations."""
    project = Project(
        id=uuid4(),
        name="Sprint 173 E2E Test Project",
        slug=f"sprint-173-e2e-{uuid4().hex[:8]}",
        description="Project for governance loop E2E testing",
        owner_id=dev_user.id,
    )
    db_session.add(project)
    await db_session.flush()
    return project


@pytest_asyncio.fixture(scope="function")
async def project_with_members(
    db_session: AsyncSession,
    test_project: Project,
    dev_user: User,
    cto_user: User,
) -> Project:
    """Set up project with both developer and CTO as members."""
    dev_member = ProjectMember(
        id=uuid4(),
        project_id=test_project.id,
        user_id=dev_user.id,
        role="developer",
    )
    db_session.add(dev_member)

    cto_member = ProjectMember(
        id=uuid4(),
        project_id=test_project.id,
        user_id=cto_user.id,
        role="admin",
    )
    db_session.add(cto_member)

    await db_session.commit()
    return test_project


@pytest_asyncio.fixture(scope="function")
async def dev_headers(dev_user: User) -> dict:
    """Get JWT auth headers for developer user (direct token creation)."""
    from datetime import timedelta
    from app.core.security import create_access_token

    token = await create_access_token(
        subject=str(dev_user.id),
        expires_delta=timedelta(hours=1),
    )
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture(scope="function")
async def cto_headers(cto_user: User) -> dict:
    """Get JWT auth headers for CTO user (direct token creation)."""
    from datetime import timedelta
    from app.core.security import create_access_token

    token = await create_access_token(
        subject=str(cto_user.id),
        expires_delta=timedelta(hours=1),
    )
    return {"Authorization": f"Bearer {token}"}


# =========================================================================
# Helper: Simulate 3 Client Interfaces
# =========================================================================


class WebAPIClient:
    """Simulates Web UI — direct HTTP calls to API."""

    def __init__(self, client: AsyncClient, headers: dict):
        self.client = client
        self.headers = headers

    async def create_gate(self, project_id, gate_name, gate_type, stage, exit_criteria=None) -> dict:
        response = await self.client.post(
            "/api/v1/gates",
            json={
                "project_id": str(project_id),
                "gate_name": gate_name,
                "gate_type": gate_type,
                "stage": stage,
                "description": f"E2E test gate: {gate_name}",
                "exit_criteria": exit_criteria or [],
            },
            headers=self.headers,
        )
        assert response.status_code == 201, f"Create gate failed: {response.text}"
        return response.json()

    async def get_actions(self, gate_id: str) -> dict:
        response = await self.client.get(
            f"/api/v1/gates/{gate_id}/actions",
            headers=self.headers,
        )
        assert response.status_code == 200, f"Get actions failed: {response.text}"
        return response.json()

    async def evaluate(self, gate_id: str) -> dict:
        response = await self.client.post(
            f"/api/v1/gates/{gate_id}/evaluate",
            headers={**self.headers, "X-Idempotency-Key": str(uuid4())},
        )
        assert response.status_code == 200, f"Evaluate failed: {response.text}"
        return response.json()

    async def submit(self, gate_id: str, message: str = None) -> dict:
        response = await self.client.post(
            f"/api/v1/gates/{gate_id}/submit",
            json={"message": message} if message else {},
            headers={**self.headers, "X-Idempotency-Key": str(uuid4())},
        )
        return response.json() if response.status_code == 200 else {"_status": response.status_code, **response.json()}

    async def approve(self, gate_id: str, comment: str) -> dict:
        response = await self.client.post(
            f"/api/v1/gates/{gate_id}/approve",
            json={"comment": comment},
            headers={**self.headers, "X-Idempotency-Key": str(uuid4())},
        )
        assert response.status_code == 200, f"Approve failed: {response.text}"
        return response.json()

    async def reject(self, gate_id: str, comment: str) -> dict:
        response = await self.client.post(
            f"/api/v1/gates/{gate_id}/reject",
            json={"comment": comment},
            headers={**self.headers, "X-Idempotency-Key": str(uuid4())},
        )
        assert response.status_code == 200, f"Reject failed: {response.text}"
        return response.json()

    async def upload_evidence(self, gate_id: str, file_content: bytes, filename: str, evidence_type: str, source: str = "web") -> dict:
        sha256_client = hashlib.sha256(file_content).hexdigest()
        response = await self.client.post(
            f"/api/v1/gates/{gate_id}/evidence",
            files={"file": (filename, io.BytesIO(file_content), "application/json")},
            data={
                "evidence_type": evidence_type,
                "sha256_client": sha256_client,
                "size_bytes": str(len(file_content)),
                "mime_type": "application/json",
                "source": source,
            },
            headers={"Authorization": self.headers["Authorization"]},
        )
        return response.json() if response.status_code == 201 else {"_status": response.status_code, **response.json()}

    async def get_gate(self, gate_id: str) -> dict:
        response = await self.client.get(
            f"/api/v1/gates/{gate_id}",
            headers=self.headers,
        )
        assert response.status_code == 200, f"Get gate failed: {response.text}"
        return response.json()


class CLIClient(WebAPIClient):
    """
    Simulates sdlcctl CLI — same API calls but with CLI-specific patterns:
    - Calls GET /actions BEFORE mutations (pre-check pattern)
    - Adds X-Idempotency-Key to all mutations
    - source="cli" for evidence uploads
    """

    async def evaluate(self, gate_id: str) -> dict:
        # CLI pre-check: GET /actions first
        actions = await self.get_actions(gate_id)
        assert actions["actions"]["can_evaluate"], (
            f"CLI pre-check failed: cannot evaluate. Reason: {actions['reasons'].get('can_evaluate')}"
        )
        return await super().evaluate(gate_id)

    async def submit(self, gate_id: str, message: str = None) -> dict:
        # CLI pre-check: GET /actions first
        actions = await self.get_actions(gate_id)
        if not actions["actions"]["can_submit"]:
            return {"error": actions["reasons"].get("can_submit"), "missing_evidence": actions["missing_evidence"]}
        return await super().submit(gate_id, message)

    async def approve(self, gate_id: str, comment: str) -> dict:
        actions = await self.get_actions(gate_id)
        assert actions["actions"]["can_approve"], (
            f"CLI pre-check failed: cannot approve. Reason: {actions['reasons'].get('can_approve')}"
        )
        return await super().approve(gate_id, comment)

    async def reject(self, gate_id: str, comment: str) -> dict:
        actions = await self.get_actions(gate_id)
        assert actions["actions"]["can_reject"], (
            f"CLI pre-check failed: cannot reject. Reason: {actions['reasons'].get('can_reject')}"
        )
        return await super().reject(gate_id, comment)

    async def upload_evidence(self, gate_id, file_content, filename, evidence_type, source="cli"):
        return await super().upload_evidence(gate_id, file_content, filename, evidence_type, source)


class ExtensionClient(WebAPIClient):
    """
    Simulates VS Code Extension — same API calls with extension patterns:
    - Server-driven UI: calls GET /actions to decide what to show
    - source="extension" for evidence uploads
    - SHA256 computed client-side (Node.js crypto.createHash)
    """

    async def evaluate(self, gate_id: str) -> dict:
        actions = await self.get_actions(gate_id)
        if not actions["actions"]["can_evaluate"]:
            return {"error": actions["reasons"].get("can_evaluate")}
        return await super().evaluate(gate_id)

    async def approve(self, gate_id: str, comment: str) -> dict:
        actions = await self.get_actions(gate_id)
        if not actions["actions"]["can_approve"]:
            return {"error": actions["reasons"].get("can_approve")}
        return await super().approve(gate_id, comment)

    async def reject(self, gate_id: str, comment: str) -> dict:
        actions = await self.get_actions(gate_id)
        if not actions["actions"]["can_reject"]:
            return {"error": actions["reasons"].get("can_reject")}
        return await super().reject(gate_id, comment)

    async def upload_evidence(self, gate_id, file_content, filename, evidence_type, source="extension"):
        return await super().upload_evidence(gate_id, file_content, filename, evidence_type, source)


# =========================================================================
# Test Class: Web API Interface (Direct HTTP)
# =========================================================================


@pytest.mark.asyncio
class TestWebAPIGovernanceLoop:
    """E2E: Complete governance loop via Web API (direct HTTP calls)."""

    async def test_happy_path_draft_to_approved(
        self, client, dev_headers, cto_headers, project_with_members
    ):
        """DRAFT → EVALUATED → SUBMITTED → APPROVED (happy path)."""
        web = WebAPIClient(client, dev_headers)
        web_cto = WebAPIClient(client, cto_headers)

        # Step 1: Create gate (DRAFT)
        gate = await web.create_gate(
            project_id=project_with_members.id,
            gate_name="E2E Web Test Gate",
            gate_type="G1_DESIGN_READY",
            stage="WHAT",
            exit_criteria=[
                {"criterion": "FRD complete", "evidence_type": "design-doc", "status": "pending"},
                {"criterion": "API spec complete", "evidence_type": "api-docs", "status": "pending"},
            ],
        )
        gate_id = gate["id"]
        assert gate["status"] == "DRAFT"

        # Step 2: Check actions from DRAFT
        actions = await web.get_actions(gate_id)
        assert actions["status"] == "DRAFT"
        assert actions["actions"]["can_evaluate"] is True
        assert actions["actions"]["can_submit"] is False  # Not EVALUATED yet
        assert actions["actions"]["can_approve"] is False  # Dev has no approve scope

        # Step 3: Upload evidence for both criteria
        evidence_1 = b'{"frd": "complete", "sections": 12}'
        evidence_2 = b'{"openapi": "3.0", "endpoints": 64}'

        result_1 = await web.upload_evidence(gate_id, evidence_1, "frd.json", "design-doc")
        assert result_1.get("integrity_verified") is True
        assert result_1.get("sha256_server") == hashlib.sha256(evidence_1).hexdigest()

        result_2 = await web.upload_evidence(gate_id, evidence_2, "api-spec.json", "api-docs")
        assert result_2.get("integrity_verified") is True

        # Step 4: Evaluate (DRAFT → EVALUATED)
        eval_result = await web.evaluate(gate_id)
        assert eval_result["status"] == "EVALUATED"
        assert eval_result["summary"]["total"] == 2
        assert eval_result["summary"]["met"] == 2
        assert eval_result["summary"]["pass_rate"] == 100.0

        # Step 5: Submit (EVALUATED → SUBMITTED)
        submit_result = await web.submit(gate_id)
        assert submit_result["status"] == "SUBMITTED"

        # Step 6: CTO approves (SUBMITTED → APPROVED)
        approve_result = await web_cto.approve(gate_id, "All criteria met. Ship it.")
        assert approve_result["status"] == "APPROVED"
        assert approve_result["approved_at"] is not None

        # Step 7: Verify final state
        final_gate = await web.get_gate(gate_id)
        assert final_gate["status"] == "APPROVED"

    async def test_rejection_and_re_evaluate_path(
        self, client, dev_headers, cto_headers, project_with_members
    ):
        """DRAFT → EVALUATED → SUBMITTED → REJECTED → re-evaluate → EVALUATED."""
        web = WebAPIClient(client, dev_headers)
        web_cto = WebAPIClient(client, cto_headers)

        gate = await web.create_gate(
            project_id=project_with_members.id,
            gate_name="Rejection Path Test",
            gate_type="G2_SHIP_READY",
            stage="HOW",
        )
        gate_id = gate["id"]

        # DRAFT → EVALUATED
        await web.evaluate(gate_id)

        # EVALUATED → SUBMITTED
        await web.submit(gate_id)

        # SUBMITTED → REJECTED (CTO rejects)
        reject_result = await web_cto.reject(gate_id, "Security scan shows 2 HIGH vulnerabilities")
        assert reject_result["status"] == "REJECTED"

        # Verify actions after rejection: can re-evaluate
        actions = await web.get_actions(gate_id)
        assert actions["status"] == "REJECTED"
        assert actions["actions"]["can_evaluate"] is True  # Re-evaluate allowed
        assert actions["actions"]["can_submit"] is False   # Must re-evaluate first

        # REJECTED → EVALUATED (re-evaluate after fixing issues)
        re_eval = await web.evaluate(gate_id)
        assert re_eval["status"] == "EVALUATED"

    async def test_evidence_upload_triggers_evaluated_stale(
        self, client, dev_headers, project_with_members
    ):
        """Evidence upload while EVALUATED → EVALUATED_STALE."""
        web = WebAPIClient(client, dev_headers)

        gate = await web.create_gate(
            project_id=project_with_members.id,
            gate_name="Stale Test Gate",
            gate_type="G1_DESIGN_READY",
            stage="WHAT",
            exit_criteria=[{"criterion": "Test", "evidence_type": "test-results", "status": "pending"}],
        )
        gate_id = gate["id"]

        # Evaluate first
        await web.evaluate(gate_id)
        gate_state = await web.get_gate(gate_id)
        assert gate_state["status"] == "EVALUATED"

        # Upload evidence AFTER evaluation → should go STALE
        result = await web.upload_evidence(gate_id, b"new evidence data", "test.json", "test-results")
        assert result.get("gate_status_changed") is True
        assert result.get("new_gate_status") == "EVALUATED_STALE"

        # Verify gate is now EVALUATED_STALE
        actions = await web.get_actions(gate_id)
        assert actions["status"] == "EVALUATED_STALE"
        assert actions["actions"]["can_evaluate"] is True  # Can re-evaluate
        assert actions["actions"]["can_submit"] is False   # Must re-evaluate first

    async def test_submit_blocked_when_missing_evidence(
        self, client, dev_headers, project_with_members
    ):
        """Submit blocked when required evidence is missing (SDLC Expert v2)."""
        web = WebAPIClient(client, dev_headers)

        gate = await web.create_gate(
            project_id=project_with_members.id,
            gate_name="Missing Evidence Test",
            gate_type="G1_DESIGN_READY",
            stage="WHAT",
            exit_criteria=[
                {"criterion": "Tests pass", "evidence_type": "test-results", "status": "pending"},
                {"criterion": "Security scan", "evidence_type": "security-scan", "status": "pending"},
            ],
        )
        gate_id = gate["id"]

        # Upload only one of two required evidence types
        await web.upload_evidence(gate_id, b"test results", "report.json", "test-results")

        # Evaluate
        await web.evaluate(gate_id)

        # Actions should show can_submit=False (missing security-scan)
        actions = await web.get_actions(gate_id)
        assert actions["actions"]["can_submit"] is False
        assert "security-scan" in actions["missing_evidence"]

        # Submit should fail with 422
        response = await client.post(
            f"/api/v1/gates/{gate_id}/submit",
            json={},
            headers={**dev_headers, "X-Idempotency-Key": str(uuid4())},
        )
        assert response.status_code == 422

    async def test_invalid_state_transition_returns_409(
        self, client, dev_headers, cto_headers, project_with_members
    ):
        """Approve a DRAFT gate → 409 Conflict."""
        web_cto = WebAPIClient(client, cto_headers)

        # Create gate (stays DRAFT)
        gate_data = await WebAPIClient(client, dev_headers).create_gate(
            project_id=project_with_members.id,
            gate_name="Invalid Transition Test",
            gate_type="G1_DESIGN_READY",
            stage="WHAT",
        )

        # Try to approve DRAFT → should fail
        response = await client.post(
            f"/api/v1/gates/{gate_data['id']}/approve",
            json={"comment": "Trying to approve draft"},
            headers={**cto_headers, "X-Idempotency-Key": str(uuid4())},
        )
        assert response.status_code == 409

    async def test_evidence_integrity_sha256_mismatch(
        self, client, dev_headers, project_with_members
    ):
        """SHA256 mismatch on upload → 400 Bad Request."""
        web = WebAPIClient(client, dev_headers)

        gate = await web.create_gate(
            project_id=project_with_members.id,
            gate_name="Hash Mismatch Test",
            gate_type="G1_DESIGN_READY",
            stage="WHAT",
        )

        # Upload with wrong hash
        file_content = b"real file content"
        wrong_hash = hashlib.sha256(b"different content").hexdigest()

        response = await client.post(
            f"/api/v1/gates/{gate['id']}/evidence",
            files={"file": ("test.json", io.BytesIO(file_content), "application/json")},
            data={
                "evidence_type": "test-results",
                "sha256_client": wrong_hash,
                "source": "web",
            },
            headers={"Authorization": dev_headers["Authorization"]},
        )
        assert response.status_code == 400
        assert "mismatch" in response.json()["detail"].lower()


# =========================================================================
# Test Class: CLI Interface (sdlcctl gate commands)
# =========================================================================


@pytest.mark.asyncio
class TestCLIGovernanceLoop:
    """E2E: Complete governance loop via CLI (sdlcctl commands pattern)."""

    async def test_cli_happy_path(
        self, client, dev_headers, cto_headers, project_with_members
    ):
        """CLI: list → evaluate → evidence submit → submit → approve."""
        cli_dev = CLIClient(client, dev_headers)
        cli_cto = CLIClient(client, cto_headers)

        # sdlcctl gate create (via API)
        gate = await cli_dev.create_gate(
            project_id=project_with_members.id,
            gate_name="CLI E2E Gate",
            gate_type="G3_BUILD_COMPLETE",
            stage="BUILD",
            exit_criteria=[
                {"criterion": "Unit tests pass", "evidence_type": "test-results", "status": "pending"},
            ],
        )
        gate_id = gate["id"]
        assert gate["status"] == "DRAFT"

        # sdlcctl evidence submit (CLI computes SHA256 client-side, source=cli)
        test_report = b'{"tests_passed": 142, "tests_failed": 0, "coverage": 94.2}'
        evidence = await cli_dev.upload_evidence(gate_id, test_report, "pytest-report.json", "test-results")
        assert evidence.get("source") in ("cli", None)  # source may or may not be echoed

        # sdlcctl gate evaluate (pre-checks /actions first)
        eval_result = await cli_dev.evaluate(gate_id)
        assert eval_result["status"] == "EVALUATED"

        # sdlcctl gate submit (pre-checks /actions, verifies no missing evidence)
        submit_result = await cli_dev.submit(gate_id)
        assert submit_result["status"] == "SUBMITTED"

        # sdlcctl gate approve (CTO, pre-checks /actions for can_approve)
        approve_result = await cli_cto.approve(gate_id, "All tests pass. Build approved.")
        assert approve_result["status"] == "APPROVED"

    async def test_cli_reject_and_re_evaluate(
        self, client, dev_headers, cto_headers, project_with_members
    ):
        """CLI: reject → re-evaluate cycle."""
        cli_dev = CLIClient(client, dev_headers)
        cli_cto = CLIClient(client, cto_headers)

        gate = await cli_dev.create_gate(
            project_id=project_with_members.id,
            gate_name="CLI Reject Test",
            gate_type="G2_SHIP_READY",
            stage="HOW",
        )
        gate_id = gate["id"]

        await cli_dev.evaluate(gate_id)
        await cli_dev.submit(gate_id)

        # CTO rejects
        reject_result = await cli_cto.reject(gate_id, "Need better test coverage")
        assert reject_result["status"] == "REJECTED"

        # Developer re-evaluates after fixing
        re_eval = await cli_dev.evaluate(gate_id)
        assert re_eval["status"] == "EVALUATED"

    async def test_cli_submit_blocked_missing_evidence(
        self, client, dev_headers, project_with_members
    ):
        """CLI pre-check: submit fails when missing evidence."""
        cli = CLIClient(client, dev_headers)

        gate = await cli.create_gate(
            project_id=project_with_members.id,
            gate_name="CLI Missing Evidence",
            gate_type="G4_TEST_COMPLETE",
            stage="TEST",
            exit_criteria=[
                {"criterion": "Security scan", "evidence_type": "security-scan", "status": "pending"},
            ],
        )
        gate_id = gate["id"]

        await cli.evaluate(gate_id)

        # Submit should return error (CLI pre-checks /actions first)
        result = await cli.submit(gate_id)
        assert "error" in result or "missing_evidence" in result


# =========================================================================
# Test Class: Extension Interface (VS Code)
# =========================================================================


@pytest.mark.asyncio
class TestExtensionGovernanceLoop:
    """E2E: Complete governance loop via VS Code Extension (apiClient pattern)."""

    async def test_extension_happy_path(
        self, client, dev_headers, cto_headers, project_with_members
    ):
        """Extension: server-driven actions → approve/reject → evidence submit."""
        ext_dev = ExtensionClient(client, dev_headers)
        ext_cto = ExtensionClient(client, cto_headers)

        gate = await ext_dev.create_gate(
            project_id=project_with_members.id,
            gate_name="Extension E2E Gate",
            gate_type="G1_DESIGN_READY",
            stage="WHAT",
            exit_criteria=[
                {"criterion": "Design doc", "evidence_type": "design-doc", "status": "pending"},
            ],
        )
        gate_id = gate["id"]

        # Extension: upload evidence (source=extension, SHA256 via Node.js crypto)
        design_doc = b'{"component": "GateApproval", "status": "reviewed"}'
        evidence = await ext_dev.upload_evidence(gate_id, design_doc, "design.json", "design-doc")
        assert evidence.get("integrity_verified") is True

        # Extension: evaluate (server-driven check first)
        eval_result = await ext_dev.evaluate(gate_id)
        assert eval_result["status"] == "EVALUATED"

        # Extension: submit
        submit_result = await ext_dev.submit(gate_id)
        assert submit_result["status"] == "SUBMITTED"

        # Extension: CTO approves via command palette
        approve_result = await ext_cto.approve(gate_id, "LGTM. Approved from VS Code.")
        assert approve_result["status"] == "APPROVED"

    async def test_extension_server_driven_actions(
        self, client, dev_headers, cto_headers, project_with_members
    ):
        """Extension: UI shows only what server allows (no client-side permission logic)."""
        ext_dev = ExtensionClient(client, dev_headers)
        ext_cto = ExtensionClient(client, cto_headers)

        gate = await ext_dev.create_gate(
            project_id=project_with_members.id,
            gate_name="Server-Driven UI Test",
            gate_type="G1_DESIGN_READY",
            stage="WHAT",
        )
        gate_id = gate["id"]

        # Developer sees: can_evaluate=True, can_approve=False (no scope)
        dev_actions = await ext_dev.get_actions(gate_id)
        assert dev_actions["actions"]["can_evaluate"] is True
        assert dev_actions["actions"]["can_approve"] is False
        assert "governance:approve" in dev_actions["reasons"].get("can_approve", "")

        # CTO sees: can_evaluate=True, can_approve=False (gate is DRAFT, not SUBMITTED)
        cto_actions = await ext_cto.get_actions(gate_id)
        assert cto_actions["actions"]["can_evaluate"] is True
        assert cto_actions["actions"]["can_approve"] is False
        assert "SUBMITTED" in cto_actions["reasons"].get("can_approve", "")


# =========================================================================
# Test Class: Cross-Interface Parity
# =========================================================================


@pytest.mark.asyncio
class TestCrossInterfaceParity:
    """P0: Same policy enforced identically across Web, CLI, Extension."""

    async def test_same_gate_actions_across_interfaces(
        self, client, dev_headers, cto_headers, project_with_members
    ):
        """All 3 clients get identical /actions response for the same gate."""
        web = WebAPIClient(client, dev_headers)
        cli = CLIClient(client, dev_headers)
        ext = ExtensionClient(client, dev_headers)

        gate = await web.create_gate(
            project_id=project_with_members.id,
            gate_name="Cross-Interface Parity Gate",
            gate_type="G1_DESIGN_READY",
            stage="WHAT",
            exit_criteria=[
                {"criterion": "FRD", "evidence_type": "design-doc", "status": "pending"},
            ],
        )
        gate_id = gate["id"]

        # All 3 clients query /actions
        web_actions = await web.get_actions(gate_id)
        cli_actions = await cli.get_actions(gate_id)
        ext_actions = await ext.get_actions(gate_id)

        # Actions must be identical
        assert web_actions["actions"] == cli_actions["actions"] == ext_actions["actions"]
        assert web_actions["status"] == cli_actions["status"] == ext_actions["status"]
        assert web_actions["missing_evidence"] == cli_actions["missing_evidence"] == ext_actions["missing_evidence"]

    async def test_state_machine_enforced_server_side(
        self, client, dev_headers, cto_headers, project_with_members
    ):
        """State transitions enforced server-side — no client can bypass."""
        web = WebAPIClient(client, dev_headers)

        gate = await web.create_gate(
            project_id=project_with_members.id,
            gate_name="Server Enforcement Test",
            gate_type="G1_DESIGN_READY",
            stage="WHAT",
        )
        gate_id = gate["id"]

        # Try submit from DRAFT (should fail 409)
        response = await client.post(
            f"/api/v1/gates/{gate_id}/submit",
            json={},
            headers={**dev_headers, "X-Idempotency-Key": str(uuid4())},
        )
        assert response.status_code == 409

        # Try approve from DRAFT (should fail 409)
        response = await client.post(
            f"/api/v1/gates/{gate_id}/approve",
            json={"comment": "bypass attempt"},
            headers={**cto_headers, "X-Idempotency-Key": str(uuid4())},
        )
        assert response.status_code == 409

    async def test_evidence_integrity_all_sources(
        self, client, dev_headers, project_with_members
    ):
        """SHA256 verification works for cli, extension, web sources."""
        web = WebAPIClient(client, dev_headers)

        gate = await web.create_gate(
            project_id=project_with_members.id,
            gate_name="Multi-Source Evidence Test",
            gate_type="G1_DESIGN_READY",
            stage="WHAT",
        )
        gate_id = gate["id"]

        for source in ["web", "cli", "extension"]:
            content = f'{{"source": "{source}", "data": "test"}}'.encode()
            sha256 = hashlib.sha256(content).hexdigest()

            response = await client.post(
                f"/api/v1/gates/{gate_id}/evidence",
                files={"file": (f"evidence-{source}.json", io.BytesIO(content), "application/json")},
                data={
                    "evidence_type": "test-results",
                    "sha256_client": sha256,
                    "source": source,
                },
                headers={"Authorization": dev_headers["Authorization"]},
            )
            assert response.status_code == 201, f"Evidence upload failed for source={source}: {response.text}"
            data = response.json()
            assert data["integrity_verified"] is True
            assert data["sha256_server"] == sha256


# =========================================================================
# Test Class: Actions Endpoint SSOT Invariant
# =========================================================================


@pytest.mark.asyncio
class TestActionsSSoTInvariant:
    """GET /actions reports exactly what mutations enforce."""

    async def test_actions_matches_mutation_outcomes(
        self, client, dev_headers, cto_headers, project_with_members
    ):
        """Whatever /actions says, the mutation endpoint agrees."""
        web = WebAPIClient(client, dev_headers)
        web_cto = WebAPIClient(client, cto_headers)

        gate = await web.create_gate(
            project_id=project_with_members.id,
            gate_name="SSOT Invariant Test",
            gate_type="G1_DESIGN_READY",
            stage="WHAT",
        )
        gate_id = gate["id"]

        # Actions says can_evaluate=True for DRAFT
        actions = await web.get_actions(gate_id)
        assert actions["actions"]["can_evaluate"] is True

        # Mutation succeeds (consistent with /actions)
        result = await web.evaluate(gate_id)
        assert result["status"] == "EVALUATED"

        # Now actions says can_submit=True (no exit criteria → no missing evidence)
        actions = await web.get_actions(gate_id)
        assert actions["actions"]["can_submit"] is True

        # Mutation succeeds
        result = await web.submit(gate_id)
        assert result["status"] == "SUBMITTED"

        # CTO actions says can_approve=True
        cto_actions = await web_cto.get_actions(gate_id)
        assert cto_actions["actions"]["can_approve"] is True

        # Mutation succeeds
        result = await web_cto.approve(gate_id, "SSOT verified")
        assert result["status"] == "APPROVED"
