"""
Integration Tests for Compliance API

File: tests/integration/test_compliance_integration.py
Version: 1.0.0
Date: December 2, 2025
Status: ACTIVE - Sprint 21 Day 5
Authority: Backend Lead + QA Lead
Framework: SDLC 4.9.1 Complete Lifecycle

Test Coverage:
- POST /api/v1/compliance/scans/{project_id} - Trigger compliance scan
- GET /api/v1/compliance/scans/{project_id}/latest - Get latest scan result
- GET /api/v1/compliance/scans/{project_id}/history - Get scan history
- GET /api/v1/compliance/violations/{project_id} - Get project violations
- PUT /api/v1/compliance/violations/{violation_id}/resolve - Resolve violation
- POST /api/v1/compliance/scans/{project_id}/schedule - Schedule scan
- GET /api/v1/compliance/jobs/{job_id} - Get job status
- GET /api/v1/compliance/queue/status - Get queue status
- POST /api/v1/compliance/ai/recommendations - Generate AI recommendation
- POST /api/v1/compliance/violations/{id}/ai-recommendation - Update violation with AI
- GET /api/v1/compliance/ai/budget - Get AI budget status
- GET /api/v1/compliance/ai/providers - Get AI providers status

Total Endpoints: 12
Total Tests: 25+
Target Coverage: 90%+
"""

import pytest
import pytest_asyncio
from datetime import datetime
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from app.models.user import User
from app.models.project import Project
from app.models.compliance_scan import (
    ComplianceScan,
    ComplianceViolation,
    TriggerType,
    ViolationSeverity,
    ViolationType,
)


@pytest.mark.integration
@pytest.mark.compliance
class TestComplianceScanTrigger:
    """Integration tests for triggering compliance scans."""

    async def test_trigger_scan_success(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
    ):
        """Test successful compliance scan trigger."""
        response = await client.post(
            f"/api/v1/compliance/scans/{test_project.id}",
            headers=auth_headers,
            json={"include_doc_code_sync": True},
        )

        assert response.status_code == 201
        data = response.json()

        assert "scan_id" in data
        assert "compliance_score" in data
        assert "violations_count" in data
        assert "warnings_count" in data
        assert data["is_compliant"] in [True, False]
        assert "scanned_at" in data
        assert data["message"] == "Compliance scan completed successfully"

    async def test_trigger_scan_without_doc_code_sync(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
    ):
        """Test compliance scan trigger without doc-code sync."""
        response = await client.post(
            f"/api/v1/compliance/scans/{test_project.id}",
            headers=auth_headers,
            json={"include_doc_code_sync": False},
        )

        assert response.status_code == 201
        data = response.json()

        assert "scan_id" in data
        assert "compliance_score" in data

    async def test_trigger_scan_unauthenticated(
        self, client: AsyncClient, test_project: Project
    ):
        """Test trigger scan without authentication returns 403."""
        response = await client.post(
            f"/api/v1/compliance/scans/{test_project.id}",
            json={"include_doc_code_sync": True},
        )

        assert response.status_code == 403

    async def test_trigger_scan_invalid_project(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test trigger scan with non-existent project returns 404."""
        response = await client.post(
            f"/api/v1/compliance/scans/{uuid4()}",
            headers=auth_headers,
            json={"include_doc_code_sync": True},
        )

        assert response.status_code == 404

    async def test_trigger_scan_non_member(
        self,
        client: AsyncClient,
        db: AsyncSession,
        test_project: Project,
    ):
        """Test trigger scan without project membership returns 403."""
        # Create non-member user
        non_member = User(
            email="nonmember_compliance@example.com",
            name="Non Member",
            password_hash="hashed",
        )
        db.add(non_member)
        await db.commit()
        await db.refresh(non_member)

        # Create token for non-member
        from app.core.security import create_access_token

        token = create_access_token(subject=str(non_member.id))
        non_member_headers = {"Authorization": f"Bearer {token}"}

        # Attempt to trigger scan
        response = await client.post(
            f"/api/v1/compliance/scans/{test_project.id}",
            headers=non_member_headers,
            json={"include_doc_code_sync": True},
        )

        assert response.status_code == 403


@pytest.mark.integration
@pytest.mark.compliance
class TestComplianceScanResults:
    """Integration tests for getting compliance scan results."""

    @pytest_asyncio.fixture
    async def compliance_scan(
        self, db: AsyncSession, test_project: Project, test_user: User
    ) -> ComplianceScan:
        """Create a compliance scan fixture."""
        scan = ComplianceScan(
            id=uuid4(),
            project_id=test_project.id,
            triggered_by=test_user.id,
            trigger_type=TriggerType.MANUAL.value,
            compliance_score=85,
            violations_count=2,
            warnings_count=3,
            violations=[
                {
                    "type": "missing_documentation",
                    "severity": "high",
                    "location": "docs/00-Project-Foundation",
                    "description": "Missing required stage folder",
                    "recommendation": "Create the folder",
                },
                {
                    "type": "insufficient_evidence",
                    "severity": "medium",
                    "location": "gates/G1",
                    "description": "Missing evidence for gate",
                    "recommendation": "Upload evidence",
                },
            ],
            warnings=[
                {
                    "type": "test_coverage_low",
                    "severity": "low",
                    "location": "backend/app",
                    "description": "Test coverage below threshold",
                    "recommendation": "Add more tests",
                },
            ],
            scanned_at=datetime.utcnow(),
            duration_ms=150,
        )
        db.add(scan)
        await db.commit()
        await db.refresh(scan)
        return scan

    async def test_get_latest_scan_success(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
        compliance_scan: ComplianceScan,
    ):
        """Test get latest scan result."""
        response = await client.get(
            f"/api/v1/compliance/scans/{test_project.id}/latest",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == str(compliance_scan.id)
        assert data["project_id"] == str(test_project.id)
        assert data["compliance_score"] == 85
        assert data["violations_count"] == 2
        assert data["warnings_count"] == 3
        assert len(data["violations"]) == 2
        assert data["is_compliant"] is False  # Has high severity violation

    async def test_get_latest_scan_no_scans(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db: AsyncSession,
        test_user: User,
    ):
        """Test get latest scan when no scans exist returns 404."""
        # Create a new project with no scans
        from app.models.project import ProjectMember

        new_project = Project(
            id=uuid4(),
            name="Project Without Scans",
            slug="project-without-scans",
            description="Project for testing no scans",
            owner_id=test_user.id,
        )
        db.add(new_project)
        await db.commit()

        # Add user as member
        member = ProjectMember(
            id=uuid4(),
            project_id=new_project.id,
            user_id=test_user.id,
            role="owner",
            invited_by=test_user.id,
            joined_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
        )
        db.add(member)
        await db.commit()

        response = await client.get(
            f"/api/v1/compliance/scans/{new_project.id}/latest",
            headers=auth_headers,
        )

        assert response.status_code == 404

    async def test_get_scan_history_success(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
        db: AsyncSession,
        test_user: User,
    ):
        """Test get scan history with pagination."""
        # Create multiple scans
        for i in range(5):
            scan = ComplianceScan(
                id=uuid4(),
                project_id=test_project.id,
                triggered_by=test_user.id,
                trigger_type=TriggerType.MANUAL.value,
                compliance_score=80 + i,
                violations_count=i,
                warnings_count=i,
                violations=[],
                warnings=[],
                scanned_at=datetime.utcnow(),
            )
            db.add(scan)
        await db.commit()

        response = await client.get(
            f"/api/v1/compliance/scans/{test_project.id}/history",
            headers=auth_headers,
            params={"limit": 3, "offset": 0},
        )

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) <= 3
        # Verify each item has expected fields
        for item in data:
            assert "id" in item
            assert "compliance_score" in item
            assert "violations_count" in item
            assert "scanned_at" in item

    async def test_get_scan_history_pagination(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
    ):
        """Test scan history pagination with offset."""
        response = await client.get(
            f"/api/v1/compliance/scans/{test_project.id}/history",
            headers=auth_headers,
            params={"limit": 2, "offset": 2},
        )

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)


@pytest.mark.integration
@pytest.mark.compliance
class TestComplianceViolations:
    """Integration tests for violation management."""

    @pytest_asyncio.fixture
    async def compliance_violation(
        self,
        db: AsyncSession,
        test_project: Project,
        test_user: User,
    ) -> ComplianceViolation:
        """Create a compliance violation fixture."""
        # Create scan first
        scan = ComplianceScan(
            id=uuid4(),
            project_id=test_project.id,
            triggered_by=test_user.id,
            trigger_type=TriggerType.MANUAL.value,
            compliance_score=75,
            violations_count=1,
            warnings_count=0,
            violations=[],
            warnings=[],
            scanned_at=datetime.utcnow(),
        )
        db.add(scan)
        await db.commit()

        # Create violation
        violation = ComplianceViolation(
            id=uuid4(),
            scan_id=scan.id,
            project_id=test_project.id,
            violation_type=ViolationType.MISSING_DOCUMENTATION.value,
            severity=ViolationSeverity.HIGH.value,
            location="docs/00-Project-Foundation/README.md",
            description="Missing required README file in Project Foundation stage",
            recommendation="Create README.md with project overview",
            is_resolved=False,
        )
        db.add(violation)
        await db.commit()
        await db.refresh(violation)
        return violation

    async def test_get_project_violations_success(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
        compliance_violation: ComplianceViolation,
    ):
        """Test get project violations."""
        response = await client.get(
            f"/api/v1/compliance/violations/{test_project.id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) >= 1

        # Find our violation
        violation = next(
            (v for v in data if v["id"] == str(compliance_violation.id)), None
        )
        assert violation is not None
        assert violation["violation_type"] == "missing_documentation"
        assert violation["severity"] == "high"
        assert violation["is_resolved"] is False

    async def test_get_violations_filter_by_resolved(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
        compliance_violation: ComplianceViolation,
    ):
        """Test filter violations by resolved status."""
        # Get unresolved only
        response = await client.get(
            f"/api/v1/compliance/violations/{test_project.id}",
            headers=auth_headers,
            params={"resolved": False},
        )

        assert response.status_code == 200
        data = response.json()

        # All returned violations should be unresolved
        for violation in data:
            assert violation["is_resolved"] is False

    async def test_get_violations_filter_by_severity(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
        compliance_violation: ComplianceViolation,
    ):
        """Test filter violations by severity."""
        response = await client.get(
            f"/api/v1/compliance/violations/{test_project.id}",
            headers=auth_headers,
            params={"severity": "high"},
        )

        assert response.status_code == 200
        data = response.json()

        # All returned violations should be high severity
        for violation in data:
            assert violation["severity"] == "high"

    async def test_resolve_violation_success(
        self,
        client: AsyncClient,
        auth_headers: dict,
        compliance_violation: ComplianceViolation,
    ):
        """Test successful violation resolution."""
        response = await client.put(
            f"/api/v1/compliance/violations/{compliance_violation.id}/resolve",
            headers=auth_headers,
            json={"resolution_notes": "Fixed by adding README.md file"},
        )

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == str(compliance_violation.id)
        assert data["is_resolved"] is True
        assert data["resolved_at"] is not None
        assert data["resolved_by"] is not None
        assert data["resolution_notes"] == "Fixed by adding README.md file"
        assert data["message"] == "Violation marked as resolved successfully"

    async def test_resolve_violation_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test resolve non-existent violation returns 404."""
        response = await client.put(
            f"/api/v1/compliance/violations/{uuid4()}/resolve",
            headers=auth_headers,
            json={"resolution_notes": "Test resolution"},
        )

        assert response.status_code == 404

    async def test_resolve_violation_already_resolved(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db: AsyncSession,
        compliance_violation: ComplianceViolation,
        test_user: User,
    ):
        """Test resolve already resolved violation returns 400."""
        # Mark violation as resolved
        compliance_violation.is_resolved = True
        compliance_violation.resolved_by = test_user.id
        compliance_violation.resolved_at = datetime.utcnow()
        await db.commit()

        # Attempt to resolve again
        response = await client.put(
            f"/api/v1/compliance/violations/{compliance_violation.id}/resolve",
            headers=auth_headers,
            json={"resolution_notes": "Second resolution attempt"},
        )

        assert response.status_code == 400
        assert "already resolved" in response.json()["detail"].lower()


@pytest.mark.integration
@pytest.mark.compliance
class TestComplianceScanScheduling:
    """Integration tests for scan scheduling."""

    async def test_schedule_scan_success(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
    ):
        """Test successful scan scheduling."""
        response = await client.post(
            f"/api/v1/compliance/scans/{test_project.id}/schedule",
            headers=auth_headers,
            json={"priority": "high", "include_doc_code_sync": True},
        )

        assert response.status_code == 202
        data = response.json()

        assert "job_id" in data
        assert data["status"] == "queued"
        assert "queued_at" in data
        assert "message" in data

    async def test_schedule_scan_default_priority(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
    ):
        """Test schedule scan with default priority."""
        response = await client.post(
            f"/api/v1/compliance/scans/{test_project.id}/schedule",
            headers=auth_headers,
            json={},
        )

        assert response.status_code == 202
        data = response.json()

        assert "job_id" in data
        assert data["status"] == "queued"

    async def test_get_job_status_success(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
    ):
        """Test get scan job status."""
        # First schedule a scan
        schedule_response = await client.post(
            f"/api/v1/compliance/scans/{test_project.id}/schedule",
            headers=auth_headers,
            json={"priority": "normal"},
        )
        job_id = schedule_response.json()["job_id"]

        # Get job status
        response = await client.get(
            f"/api/v1/compliance/jobs/{job_id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        assert data["job_id"] == job_id
        assert data["project_id"] == str(test_project.id)
        assert data["status"] in ["queued", "running", "completed", "failed"]

    async def test_get_job_status_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test get non-existent job status returns 404."""
        response = await client.get(
            f"/api/v1/compliance/jobs/{uuid4()}",
            headers=auth_headers,
        )

        assert response.status_code == 404

    async def test_get_queue_status_success(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test get queue status."""
        response = await client.get(
            "/api/v1/compliance/queue/status",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        assert "pending" in data
        assert "running" in data
        assert "completed" in data
        assert "failed" in data
        assert "total_jobs" in data
        assert isinstance(data["pending"], int)
        assert isinstance(data["total_jobs"], int)


@pytest.mark.integration
@pytest.mark.compliance
class TestAIRecommendations:
    """Integration tests for AI recommendation endpoints."""

    async def test_generate_ai_recommendation_success(
        self,
        client: AsyncClient,
        auth_headers: dict,
    ):
        """Test generate AI recommendation."""
        response = await client.post(
            "/api/v1/compliance/ai/recommendations",
            headers=auth_headers,
            json={
                "violation_type": "missing_documentation",
                "severity": "high",
                "location": "docs/00-Project-Foundation",
                "description": "Missing required SDLC 4.9.1 stage folder",
                "context": {"project_type": "web_application"},
            },
        )

        assert response.status_code == 200
        data = response.json()

        assert "recommendation" in data
        assert "provider" in data
        assert "model" in data
        assert "confidence" in data
        assert "duration_ms" in data
        assert "tokens_used" in data
        assert "cost_usd" in data
        assert "fallback_used" in data
        # Recommendation should not be empty
        assert len(data["recommendation"]) > 0
        # Confidence should be 0-100
        assert 0 <= data["confidence"] <= 100

    async def test_generate_ai_recommendation_force_provider(
        self,
        client: AsyncClient,
        auth_headers: dict,
    ):
        """Test generate AI recommendation with forced provider."""
        response = await client.post(
            "/api/v1/compliance/ai/recommendations",
            headers=auth_headers,
            json={
                "violation_type": "policy_violation",
                "severity": "critical",
                "location": "backend/app/api",
                "description": "API endpoint missing authentication",
                "force_provider": "rule_based",  # Force rule-based for testing
            },
        )

        assert response.status_code == 200
        data = response.json()

        assert data["provider"] == "rule_based"
        assert len(data["recommendation"]) > 0

    async def test_generate_ai_recommendation_invalid_provider(
        self,
        client: AsyncClient,
        auth_headers: dict,
    ):
        """Test generate AI recommendation with invalid provider returns 400."""
        response = await client.post(
            "/api/v1/compliance/ai/recommendations",
            headers=auth_headers,
            json={
                "violation_type": "test_coverage_low",
                "severity": "medium",
                "location": "backend/tests",
                "description": "Test coverage below threshold",
                "force_provider": "invalid_provider",
            },
        )

        assert response.status_code == 400
        assert "invalid provider" in response.json()["detail"].lower()

    async def test_generate_violation_recommendation_success(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db: AsyncSession,
        test_project: Project,
        test_user: User,
    ):
        """Test generate and store AI recommendation for violation."""
        # Create scan and violation
        scan = ComplianceScan(
            id=uuid4(),
            project_id=test_project.id,
            triggered_by=test_user.id,
            trigger_type=TriggerType.MANUAL.value,
            compliance_score=80,
            violations_count=1,
            warnings_count=0,
            violations=[],
            warnings=[],
            scanned_at=datetime.utcnow(),
        )
        db.add(scan)
        await db.commit()

        violation = ComplianceViolation(
            id=uuid4(),
            scan_id=scan.id,
            project_id=test_project.id,
            violation_type="skipped_stage",
            severity="high",
            location="docs/01-Planning-Analysis",
            description="Stage 01 (WHAT) was skipped without approval",
            recommendation="Complete Stage 01 requirements",
            is_resolved=False,
        )
        db.add(violation)
        await db.commit()
        await db.refresh(violation)

        # Generate AI recommendation
        response = await client.post(
            f"/api/v1/compliance/violations/{violation.id}/ai-recommendation",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        assert data["violation_id"] == str(violation.id)
        assert "ai_recommendation" in data
        assert "ai_provider" in data
        assert "ai_confidence" in data
        assert data["message"] == "AI recommendation generated and stored successfully"

    async def test_generate_violation_recommendation_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test generate recommendation for non-existent violation returns 404."""
        response = await client.post(
            f"/api/v1/compliance/violations/{uuid4()}/ai-recommendation",
            headers=auth_headers,
        )

        assert response.status_code == 404

    async def test_get_ai_budget_status_success(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test get AI budget status."""
        response = await client.get(
            "/api/v1/compliance/ai/budget",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        assert "month" in data
        assert "total_spent" in data
        assert "budget" in data
        assert "remaining" in data
        assert "percentage_used" in data
        assert "by_provider" in data
        assert "alerts" in data
        # Validate types
        assert isinstance(data["total_spent"], (int, float))
        assert isinstance(data["budget"], (int, float))
        assert isinstance(data["percentage_used"], (int, float))
        assert isinstance(data["by_provider"], dict)
        assert isinstance(data["alerts"], list)

    async def test_get_ai_providers_status_success(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test get AI providers status."""
        response = await client.get(
            "/api/v1/compliance/ai/providers",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        # All 4 providers should be present
        assert "ollama" in data
        assert "claude" in data
        assert "gpt4" in data
        assert "rule_based" in data

        # Each provider should have status info
        for provider in ["ollama", "claude", "gpt4", "rule_based"]:
            assert "available" in data[provider]
            assert isinstance(data[provider]["available"], bool)

    async def test_list_ollama_models_success(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test list available Ollama models."""
        response = await client.get(
            "/api/v1/compliance/ai/models",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        assert "models" in data
        assert "default_model" in data
        assert "ollama_url" in data
        assert isinstance(data["models"], list)


@pytest.mark.integration
@pytest.mark.compliance
class TestComplianceAccessControl:
    """Integration tests for compliance API access control."""

    async def test_get_violations_non_member(
        self,
        client: AsyncClient,
        db: AsyncSession,
        test_project: Project,
    ):
        """Test get violations without project membership returns 403."""
        # Create non-member user
        non_member = User(
            email="nonmember_violations@example.com",
            name="Non Member",
            password_hash="hashed",
        )
        db.add(non_member)
        await db.commit()
        await db.refresh(non_member)

        from app.core.security import create_access_token

        token = create_access_token(subject=str(non_member.id))
        non_member_headers = {"Authorization": f"Bearer {token}"}

        response = await client.get(
            f"/api/v1/compliance/violations/{test_project.id}",
            headers=non_member_headers,
        )

        assert response.status_code == 403

    async def test_resolve_violation_non_member(
        self,
        client: AsyncClient,
        db: AsyncSession,
        test_project: Project,
        test_user: User,
    ):
        """Test resolve violation without project membership returns 403."""
        # Create scan and violation
        scan = ComplianceScan(
            id=uuid4(),
            project_id=test_project.id,
            triggered_by=test_user.id,
            trigger_type=TriggerType.MANUAL.value,
            compliance_score=80,
            violations_count=1,
            warnings_count=0,
            violations=[],
            warnings=[],
            scanned_at=datetime.utcnow(),
        )
        db.add(scan)
        await db.commit()

        violation = ComplianceViolation(
            id=uuid4(),
            scan_id=scan.id,
            project_id=test_project.id,
            violation_type="test_coverage_low",
            severity="medium",
            location="backend/tests",
            description="Test coverage below threshold",
            is_resolved=False,
        )
        db.add(violation)
        await db.commit()

        # Create non-member user
        non_member = User(
            email="nonmember_resolve@example.com",
            name="Non Member",
            password_hash="hashed",
        )
        db.add(non_member)
        await db.commit()
        await db.refresh(non_member)

        from app.core.security import create_access_token

        token = create_access_token(subject=str(non_member.id))
        non_member_headers = {"Authorization": f"Bearer {token}"}

        response = await client.put(
            f"/api/v1/compliance/violations/{violation.id}/resolve",
            headers=non_member_headers,
            json={"resolution_notes": "Unauthorized resolution attempt"},
        )

        assert response.status_code == 403

    async def test_get_latest_scan_non_member(
        self,
        client: AsyncClient,
        db: AsyncSession,
        test_project: Project,
    ):
        """Test get latest scan without project membership returns 403."""
        # Create non-member user
        non_member = User(
            email="nonmember_scan@example.com",
            name="Non Member",
            password_hash="hashed",
        )
        db.add(non_member)
        await db.commit()
        await db.refresh(non_member)

        from app.core.security import create_access_token

        token = create_access_token(subject=str(non_member.id))
        non_member_headers = {"Authorization": f"Bearer {token}"}

        response = await client.get(
            f"/api/v1/compliance/scans/{test_project.id}/latest",
            headers=non_member_headers,
        )

        assert response.status_code == 403


@pytest.mark.integration
@pytest.mark.compliance
class TestComplianceEdgeCases:
    """Integration tests for compliance API edge cases."""

    async def test_trigger_scan_empty_project(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db: AsyncSession,
        test_user: User,
    ):
        """Test trigger scan on project with no files (edge case)."""
        from app.models.project import ProjectMember

        # Create empty project
        empty_project = Project(
            id=uuid4(),
            name="Empty Project",
            slug="empty-project",
            description="Project with no files",
            owner_id=test_user.id,
        )
        db.add(empty_project)
        await db.commit()

        # Add user as member
        member = ProjectMember(
            id=uuid4(),
            project_id=empty_project.id,
            user_id=test_user.id,
            role="owner",
            invited_by=test_user.id,
            joined_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
        )
        db.add(member)
        await db.commit()

        # Trigger scan
        response = await client.post(
            f"/api/v1/compliance/scans/{empty_project.id}",
            headers=auth_headers,
            json={"include_doc_code_sync": True},
        )

        # Should succeed even with no files
        assert response.status_code == 201
        data = response.json()

        # May have high violations due to missing structure
        assert "compliance_score" in data
        assert "violations_count" in data

    async def test_get_violations_with_all_filters(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_project: Project,
        db: AsyncSession,
        test_user: User,
    ):
        """Test get violations with all filters applied."""
        # Create scan with multiple violations
        scan = ComplianceScan(
            id=uuid4(),
            project_id=test_project.id,
            triggered_by=test_user.id,
            trigger_type=TriggerType.MANUAL.value,
            compliance_score=70,
            violations_count=3,
            warnings_count=0,
            violations=[],
            warnings=[],
            scanned_at=datetime.utcnow(),
        )
        db.add(scan)
        await db.commit()

        # Create violations with different severities
        for severity in ["critical", "high", "medium"]:
            violation = ComplianceViolation(
                id=uuid4(),
                scan_id=scan.id,
                project_id=test_project.id,
                violation_type="missing_documentation",
                severity=severity,
                location=f"docs/{severity}-level",
                description=f"{severity.upper()} severity violation",
                is_resolved=False,
            )
            db.add(violation)
        await db.commit()

        # Get only unresolved critical violations with limit
        response = await client.get(
            f"/api/v1/compliance/violations/{test_project.id}",
            headers=auth_headers,
            params={"resolved": False, "severity": "critical", "limit": 1},
        )

        assert response.status_code == 200
        data = response.json()

        assert len(data) <= 1
        for violation in data:
            assert violation["severity"] == "critical"
            assert violation["is_resolved"] is False

    async def test_scan_history_empty(
        self,
        client: AsyncClient,
        auth_headers: dict,
        db: AsyncSession,
        test_user: User,
    ):
        """Test scan history returns empty list for project with no scans."""
        from app.models.project import ProjectMember

        # Create project with no scans
        new_project = Project(
            id=uuid4(),
            name="Project No History",
            slug="project-no-history",
            description="Project with no scan history",
            owner_id=test_user.id,
        )
        db.add(new_project)
        await db.commit()

        # Add user as member
        member = ProjectMember(
            id=uuid4(),
            project_id=new_project.id,
            user_id=test_user.id,
            role="owner",
            invited_by=test_user.id,
            joined_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
        )
        db.add(member)
        await db.commit()

        response = await client.get(
            f"/api/v1/compliance/scans/{new_project.id}/history",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 0


# Need to import pytest_asyncio for async fixtures
import pytest_asyncio
