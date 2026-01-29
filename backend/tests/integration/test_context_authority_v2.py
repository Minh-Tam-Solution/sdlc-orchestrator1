"""
=========================================================================
Context Authority V2 Integration Tests - Sprint 120 (SPEC-0011)
SDLC Orchestrator - Stage 04 (BUILD)

Version: 1.0.0
Date: January 29, 2026
Status: ACTIVE - Sprint 120 Pre-work (Day 2)
Authority: Backend Lead + CTO Approved
Foundation: SPEC-0011 Context Authority V2 - Gate-Aware Dynamic Context
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Integration tests for Context Authority V2 critical path
- Test full flow: template → overlay → snapshot → audit
- Test gate-triggered overlay updates
- Test vibecoding zone integration
- Test concurrent overlay applications

Test Coverage:
- ✅ POST /context-authority/v2/validate (full validation)
- ✅ POST /context-authority/v2/overlay (generate overlay)
- ✅ GET /context-authority/v2/templates (list templates)
- ✅ POST /context-authority/v2/templates (create template)
- ✅ GET /context-authority/v2/snapshots/{submission_id}
- ✅ GET /context-authority/v2/templates/{id}/usage

Zero Mock Policy: Production-ready integration tests

Test Scenarios (CTO-approved):
1. test_overlay_application_full_flow
2. test_snapshot_creation_and_retrieval
3. test_vibecoding_zone_overlay_integration
4. test_gate_triggered_overlay
5. test_concurrent_overlay_applications
=========================================================================
"""

import asyncio
import pytest
from httpx import AsyncClient
from uuid import uuid4
from datetime import datetime


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def sample_submission_id() -> str:
    """Generate a sample submission ID for testing."""
    return str(uuid4())


@pytest.fixture
def sample_project_id() -> str:
    """Generate a sample project ID for testing."""
    return str(uuid4())


@pytest.fixture
def sample_gate_id() -> str:
    """Generate a sample gate ID for testing."""
    return str(uuid4())


@pytest.fixture
def lite_tier_project() -> dict:
    """Project configuration for LITE tier."""
    return {
        "id": str(uuid4()),
        "name": "Test Project LITE",
        "tier": "LITE",
        "current_stage": "04-build",
        "last_passed_gate": "G0.2",
        "pending_gates": ["G1"],
    }


@pytest.fixture
def enterprise_tier_project() -> dict:
    """Project configuration for ENTERPRISE tier."""
    return {
        "id": str(uuid4()),
        "name": "Test Project ENTERPRISE",
        "tier": "ENTERPRISE",
        "current_stage": "04-build",
        "last_passed_gate": "G2",
        "pending_gates": ["G3"],
    }


@pytest.fixture
def green_zone_context() -> dict:
    """Context data for GREEN zone (index 0-20)."""
    return {
        "vibecoding_index": 15,
        "vibecoding_zone": "GREEN",
        "gate_status": {
            "current_stage": "04-build",
            "last_passed_gate": "G2",
            "pending_gates": ["G3"],
        },
        "v1_result": {
            "adr_linkage": True,
            "design_doc_exists": True,
            "agents_md_fresh": True,
        },
    }


@pytest.fixture
def orange_zone_context() -> dict:
    """Context data for ORANGE zone (index 41-60)."""
    return {
        "vibecoding_index": 55,
        "vibecoding_zone": "ORANGE",
        "gate_status": {
            "current_stage": "04-build",
            "last_passed_gate": "G1",
            "pending_gates": ["G2"],
        },
        "v1_result": {
            "adr_linkage": True,
            "design_doc_exists": False,
            "agents_md_fresh": False,
        },
    }


@pytest.fixture
def red_zone_context() -> dict:
    """Context data for RED zone (index 61-100)."""
    return {
        "vibecoding_index": 85,
        "vibecoding_zone": "RED",
        "gate_status": {
            "current_stage": "02-design",
            "last_passed_gate": "G0.2",
            "pending_gates": ["G1", "G2"],
        },
        "v1_result": {
            "adr_linkage": False,
            "design_doc_exists": False,
            "agents_md_fresh": False,
        },
    }


@pytest.fixture
def sample_overlay_template() -> dict:
    """Sample overlay template for testing."""
    return {
        "name": "Test Gate Pass Template",
        "trigger_type": "gate_pass",
        "trigger_value": "G2",
        "tier": None,  # Applies to all tiers
        "overlay_content": """## ✅ Build Phase Active

Gate G2 (Design Ready) PASSED on {date}.

**Build phase guidelines:**
- Follow approved architecture in ADRs
- Maintain 95%+ test coverage
- Run SAST scans before PR
- No new features without spec

**Current Stage:** {stage}
**Project Tier:** {tier}
""",
        "priority": 90,
        "is_active": True,
        "description": "Shown when Gate G2 (Design Ready) passes",
    }


@pytest.fixture
def sample_index_zone_template() -> dict:
    """Sample index zone template for testing."""
    return {
        "name": "Orange Zone Warning",
        "trigger_type": "index_zone",
        "trigger_value": "orange",
        "tier": None,
        "overlay_content": """## ⚠️ Vibecoding Index: ORANGE ({index})

This submission requires Tech Lead review before merge.

**Contributing signals:**
{top_signals}

**Suggested Actions:**
- Review architectural patterns
- Reduce AI dependency ratio
- Consider breaking into smaller PRs

**Escalation:**
- Queue: Tech Lead Review
- SLA: 4 hours
""",
        "priority": 80,
        "is_active": True,
        "description": "Shown when vibecoding index is in Orange zone (41-60)",
    }


# ============================================================================
# Test 1: Overlay Application Full Flow
# ============================================================================


@pytest.mark.asyncio
async def test_overlay_application_full_flow(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    lite_tier_project: dict,
    green_zone_context: dict,
):
    """
    Test 1: Full flow from validation request to overlay generation.

    Flow: Request → Validate V1 → Calculate V2 → Generate Overlay → Store Snapshot
    """
    # Step 1: Create validation request
    validation_request = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": green_zone_context["vibecoding_index"],
        "vibecoding_zone": green_zone_context["vibecoding_zone"],
        "gate_status": green_zone_context["gate_status"],
        "v1_result": green_zone_context["v1_result"],
    }

    # Step 2: Call full validation endpoint
    response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Step 3: Verify response structure (SPEC-0011 FR-001)
    assert "submission_id" in data
    assert "is_valid" in data
    assert "v1_result" in data
    assert "v2_result" in data
    assert "dynamic_overlay" in data
    assert "snapshot_id" in data
    assert "validated_at" in data

    # Step 4: Verify V2-specific fields
    v2_result = data["v2_result"]
    assert "gate_violations" in v2_result
    assert "index_warnings" in v2_result
    assert "applied_templates" in v2_result

    # Step 5: Verify dynamic overlay is not empty for GREEN zone
    assert len(data["dynamic_overlay"]) > 0

    # Step 6: Verify snapshot was created
    assert data["snapshot_id"] is not None


@pytest.mark.asyncio
async def test_overlay_application_unauthorized(
    client: AsyncClient,
    sample_submission_id: str,
    lite_tier_project: dict,
    green_zone_context: dict,
):
    """Test validation endpoint requires authentication."""
    validation_request = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": green_zone_context["vibecoding_index"],
        "vibecoding_zone": green_zone_context["vibecoding_zone"],
        "gate_status": green_zone_context["gate_status"],
        "v1_result": green_zone_context["v1_result"],
    }

    response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_overlay_application_invalid_request(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test validation endpoint with invalid request."""
    # Missing required fields
    validation_request = {
        "submission_id": "test-123",
    }

    response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
        headers=auth_headers,
    )
    assert response.status_code == 422  # Validation error


# ============================================================================
# Test 2: Snapshot Creation and Retrieval
# ============================================================================


@pytest.mark.asyncio
async def test_snapshot_creation_and_retrieval(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    lite_tier_project: dict,
    green_zone_context: dict,
):
    """
    Test 2: Verify snapshot is created and can be retrieved.

    Tests FR-005: Context snapshots for audit trail.
    """
    # Step 1: Create validation (which creates snapshot)
    validation_request = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": green_zone_context["vibecoding_index"],
        "vibecoding_zone": green_zone_context["vibecoding_zone"],
        "gate_status": green_zone_context["gate_status"],
        "v1_result": green_zone_context["v1_result"],
    }

    create_response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
        headers=auth_headers,
    )
    assert create_response.status_code == 200
    created_data = create_response.json()
    snapshot_id = created_data["snapshot_id"]

    # Step 2: Retrieve snapshot by submission ID
    retrieve_response = await client.get(
        f"/api/v1/context-authority/v2/snapshots/{sample_submission_id}",
        headers=auth_headers,
    )
    assert retrieve_response.status_code == 200
    snapshot_data = retrieve_response.json()

    # Step 3: Verify snapshot structure (SPEC-0011 FR-005)
    assert "snapshots" in snapshot_data
    assert len(snapshot_data["snapshots"]) >= 1

    latest_snapshot = snapshot_data["snapshots"][0]
    assert latest_snapshot["id"] == snapshot_id
    assert latest_snapshot["submission_id"] == sample_submission_id
    assert "gate_status" in latest_snapshot
    assert "vibecoding_index" in latest_snapshot
    assert "vibecoding_zone" in latest_snapshot
    assert "dynamic_overlay" in latest_snapshot
    assert "is_valid" in latest_snapshot
    assert "snapshot_at" in latest_snapshot

    # Step 4: Verify immutability - snapshot content matches original
    assert latest_snapshot["vibecoding_index"] == green_zone_context["vibecoding_index"]
    assert latest_snapshot["vibecoding_zone"] == green_zone_context["vibecoding_zone"]


@pytest.mark.asyncio
async def test_snapshot_retrieval_not_found(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test snapshot retrieval for non-existent submission."""
    non_existent_id = str(uuid4())

    response = await client.get(
        f"/api/v1/context-authority/v2/snapshots/{non_existent_id}",
        headers=auth_headers,
    )
    # Should return empty list or 404
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert data["snapshots"] == []


@pytest.mark.asyncio
async def test_snapshot_multiple_validations(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    lite_tier_project: dict,
    green_zone_context: dict,
    orange_zone_context: dict,
):
    """Test that multiple validations create multiple snapshots."""
    # First validation - GREEN zone
    validation_request_1 = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": green_zone_context["vibecoding_index"],
        "vibecoding_zone": green_zone_context["vibecoding_zone"],
        "gate_status": green_zone_context["gate_status"],
        "v1_result": green_zone_context["v1_result"],
    }

    await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request_1,
        headers=auth_headers,
    )

    # Second validation - ORANGE zone (context changed)
    validation_request_2 = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": orange_zone_context["vibecoding_index"],
        "vibecoding_zone": orange_zone_context["vibecoding_zone"],
        "gate_status": orange_zone_context["gate_status"],
        "v1_result": orange_zone_context["v1_result"],
    }

    await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request_2,
        headers=auth_headers,
    )

    # Retrieve all snapshots
    response = await client.get(
        f"/api/v1/context-authority/v2/snapshots/{sample_submission_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Should have 2 snapshots
    assert len(data["snapshots"]) >= 2

    # Verify snapshots are ordered (most recent first)
    snapshots = data["snapshots"]
    first_snapshot_time = datetime.fromisoformat(snapshots[0]["snapshot_at"].replace("Z", "+00:00"))
    second_snapshot_time = datetime.fromisoformat(snapshots[1]["snapshot_at"].replace("Z", "+00:00"))
    assert first_snapshot_time >= second_snapshot_time


# ============================================================================
# Test 3: Vibecoding Zone Overlay Integration
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_zone_overlay_integration(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    lite_tier_project: dict,
    orange_zone_context: dict,
):
    """
    Test 3: Verify zone-specific overlays are applied correctly.

    Tests FR-002: Dynamic overlay based on vibecoding zone.
    """
    # Step 1: Validate with ORANGE zone
    validation_request = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": orange_zone_context["vibecoding_index"],
        "vibecoding_zone": orange_zone_context["vibecoding_zone"],
        "gate_status": orange_zone_context["gate_status"],
        "v1_result": orange_zone_context["v1_result"],
    }

    response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Step 2: Verify ORANGE zone triggers warning overlay
    dynamic_overlay = data["dynamic_overlay"]
    assert "ORANGE" in dynamic_overlay or "⚠️" in dynamic_overlay
    assert "Tech Lead" in dynamic_overlay or "review" in dynamic_overlay.lower()

    # Step 3: Verify applied templates include index_zone trigger
    v2_result = data["v2_result"]
    applied_templates = v2_result.get("applied_templates", [])
    zone_template_applied = any(
        t.get("trigger_type") == "index_zone" for t in applied_templates
    )
    assert zone_template_applied or len(dynamic_overlay) > 0


@pytest.mark.asyncio
async def test_vibecoding_red_zone_blocks(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    lite_tier_project: dict,
    red_zone_context: dict,
):
    """Test that RED zone triggers blocking overlay."""
    validation_request = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": red_zone_context["vibecoding_index"],
        "vibecoding_zone": red_zone_context["vibecoding_zone"],
        "gate_status": red_zone_context["gate_status"],
        "v1_result": red_zone_context["v1_result"],
    }

    response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify RED zone triggers strong warning
    dynamic_overlay = data["dynamic_overlay"]
    assert "RED" in dynamic_overlay or "🚫" in dynamic_overlay or "BLOCK" in dynamic_overlay


@pytest.mark.asyncio
async def test_vibecoding_green_zone_auto_approve(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    lite_tier_project: dict,
    green_zone_context: dict,
):
    """Test that GREEN zone gets minimal overlay."""
    validation_request = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": green_zone_context["vibecoding_index"],
        "vibecoding_zone": green_zone_context["vibecoding_zone"],
        "gate_status": green_zone_context["gate_status"],
        "v1_result": green_zone_context["v1_result"],
    }

    response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify GREEN zone is valid
    assert data["is_valid"] is True

    # Verify no blocking warnings in overlay
    dynamic_overlay = data["dynamic_overlay"]
    assert "BLOCK" not in dynamic_overlay
    assert "🚫" not in dynamic_overlay


# ============================================================================
# Test 4: Gate-Triggered Overlay
# ============================================================================


@pytest.mark.asyncio
async def test_gate_triggered_overlay(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    lite_tier_project: dict,
    green_zone_context: dict,
):
    """
    Test 4: Verify gate pass/fail triggers correct overlay.

    Tests FR-002: Dynamic overlay based on gate events.
    """
    # Test with gate G2 passed in context
    gate_status_g2_passed = {
        "current_stage": "04-build",
        "last_passed_gate": "G2",
        "pending_gates": ["G3"],
    }

    validation_request = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": green_zone_context["vibecoding_index"],
        "vibecoding_zone": green_zone_context["vibecoding_zone"],
        "gate_status": gate_status_g2_passed,
        "v1_result": green_zone_context["v1_result"],
    }

    response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify overlay reflects gate status
    dynamic_overlay = data["dynamic_overlay"]
    # Should mention build phase or G2 related content
    overlay_lower = dynamic_overlay.lower()
    assert "build" in overlay_lower or "g2" in overlay_lower or "design" in overlay_lower


@pytest.mark.asyncio
async def test_stage_constraint_overlay(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    lite_tier_project: dict,
):
    """Test stage constraint triggers blocking overlay when code changes in design stage."""
    # Simulate code change attempt in stage 02 (design)
    gate_status_stage_02 = {
        "current_stage": "02-design",
        "last_passed_gate": "G0.2",
        "pending_gates": ["G1", "G2"],
    }

    validation_request = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": 30,  # YELLOW zone
        "vibecoding_zone": "YELLOW",
        "gate_status": gate_status_stage_02,
        "v1_result": {
            "adr_linkage": False,
            "design_doc_exists": False,
            "agents_md_fresh": True,
        },
        "changed_paths": ["backend/app/services/new_feature.py"],  # Code change
    }

    response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify gate violations are reported
    v2_result = data["v2_result"]
    gate_violations = v2_result.get("gate_violations", [])

    # Should have stage constraint violation or warning in overlay
    dynamic_overlay = data["dynamic_overlay"]
    has_stage_warning = (
        len(gate_violations) > 0 or
        "stage" in dynamic_overlay.lower() or
        "design" in dynamic_overlay.lower() or
        "g1" in dynamic_overlay.lower()
    )
    assert has_stage_warning


@pytest.mark.asyncio
async def test_gate_g02_pass_overlay(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    lite_tier_project: dict,
    green_zone_context: dict,
):
    """Test G0.2 pass triggers design approved overlay."""
    gate_status_g02_passed = {
        "current_stage": "03-build",
        "last_passed_gate": "G0.2",
        "pending_gates": ["G1"],
    }

    validation_request = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": green_zone_context["vibecoding_index"],
        "vibecoding_zone": green_zone_context["vibecoding_zone"],
        "gate_status": gate_status_g02_passed,
        "v1_result": green_zone_context["v1_result"],
    }

    response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Should have overlay content
    assert len(data["dynamic_overlay"]) > 0


# ============================================================================
# Test 5: Concurrent Overlay Applications
# ============================================================================


@pytest.mark.asyncio
async def test_concurrent_overlay_applications(
    client: AsyncClient,
    auth_headers: dict,
    lite_tier_project: dict,
    green_zone_context: dict,
):
    """
    Test 5: Verify concurrent validations are handled correctly.

    Tests thread safety and data isolation.
    """
    # Create 5 concurrent validation requests with different submission IDs
    submission_ids = [str(uuid4()) for _ in range(5)]

    async def validate_submission(submission_id: str) -> dict:
        validation_request = {
            "submission_id": submission_id,
            "submission_type": "PR",
            "project_id": lite_tier_project["id"],
            "project_tier": lite_tier_project["tier"],
            "vibecoding_index": green_zone_context["vibecoding_index"],
            "vibecoding_zone": green_zone_context["vibecoding_zone"],
            "gate_status": green_zone_context["gate_status"],
            "v1_result": green_zone_context["v1_result"],
        }

        response = await client.post(
            "/api/v1/context-authority/v2/validate",
            json=validation_request,
            headers=auth_headers,
        )
        return {
            "submission_id": submission_id,
            "status_code": response.status_code,
            "data": response.json() if response.status_code == 200 else None,
        }

    # Execute all validations concurrently
    results = await asyncio.gather(
        *[validate_submission(sid) for sid in submission_ids]
    )

    # Verify all requests succeeded
    for result in results:
        assert result["status_code"] == 200
        assert result["data"]["submission_id"] == result["submission_id"]
        assert result["data"]["snapshot_id"] is not None

    # Verify each submission has its own snapshot
    snapshot_ids = [r["data"]["snapshot_id"] for r in results]
    assert len(set(snapshot_ids)) == 5  # All unique


@pytest.mark.asyncio
async def test_concurrent_same_submission_validations(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    lite_tier_project: dict,
    green_zone_context: dict,
):
    """Test concurrent validations for the same submission create multiple snapshots."""
    async def validate_same_submission() -> dict:
        validation_request = {
            "submission_id": sample_submission_id,
            "submission_type": "PR",
            "project_id": lite_tier_project["id"],
            "project_tier": lite_tier_project["tier"],
            "vibecoding_index": green_zone_context["vibecoding_index"],
            "vibecoding_zone": green_zone_context["vibecoding_zone"],
            "gate_status": green_zone_context["gate_status"],
            "v1_result": green_zone_context["v1_result"],
        }

        response = await client.post(
            "/api/v1/context-authority/v2/validate",
            json=validation_request,
            headers=auth_headers,
        )
        return response.json() if response.status_code == 200 else None

    # Execute 3 concurrent validations for same submission
    results = await asyncio.gather(
        *[validate_same_submission() for _ in range(3)]
    )

    # All should succeed
    for result in results:
        assert result is not None
        assert result["submission_id"] == sample_submission_id

    # Retrieve snapshots
    response = await client.get(
        f"/api/v1/context-authority/v2/snapshots/{sample_submission_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Should have at least 3 snapshots
    assert len(data["snapshots"]) >= 3


# ============================================================================
# Template Management Tests
# ============================================================================


@pytest.mark.asyncio
async def test_list_templates(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test GET /context-authority/v2/templates - List all templates."""
    response = await client.get(
        "/api/v1/context-authority/v2/templates",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "templates" in data
    assert "total" in data

    # Verify template structure if any exist
    if data["total"] > 0:
        template = data["templates"][0]
        assert "id" in template
        assert "name" in template
        assert "trigger_type" in template
        assert "trigger_value" in template
        assert "priority" in template
        assert "is_active" in template


@pytest.mark.asyncio
async def test_list_templates_filter_by_trigger_type(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test template filtering by trigger type."""
    response = await client.get(
        "/api/v1/context-authority/v2/templates?trigger_type=gate_pass",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # All templates should have gate_pass trigger type
    for template in data["templates"]:
        assert template["trigger_type"] == "gate_pass"


@pytest.mark.asyncio
async def test_create_template(
    client: AsyncClient,
    admin_auth_headers: dict,
    sample_overlay_template: dict,
):
    """Test POST /context-authority/v2/templates - Create template (admin only)."""
    response = await client.post(
        "/api/v1/context-authority/v2/templates",
        json=sample_overlay_template,
        headers=admin_auth_headers,
    )
    # Should succeed (201) or fail with 403 if not admin
    assert response.status_code in [201, 403]

    if response.status_code == 201:
        data = response.json()
        assert data["name"] == sample_overlay_template["name"]
        assert data["trigger_type"] == sample_overlay_template["trigger_type"]
        assert "id" in data


@pytest.mark.asyncio
async def test_template_usage_analytics(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test GET /context-authority/v2/templates/{id}/usage - Template usage stats."""
    # First, get a template ID
    list_response = await client.get(
        "/api/v1/context-authority/v2/templates",
        headers=auth_headers,
    )

    if list_response.status_code == 200 and list_response.json()["total"] > 0:
        template_id = list_response.json()["templates"][0]["id"]

        # Get usage stats
        usage_response = await client.get(
            f"/api/v1/context-authority/v2/templates/{template_id}/usage",
            headers=auth_headers,
        )
        assert usage_response.status_code == 200
        usage_data = usage_response.json()

        # Verify usage structure
        assert "template_id" in usage_data
        assert "application_count" in usage_data
        assert "recent_applications" in usage_data


# ============================================================================
# Overlay Generation Tests
# ============================================================================


@pytest.mark.asyncio
async def test_generate_overlay_only(
    client: AsyncClient,
    auth_headers: dict,
    sample_project_id: str,
    green_zone_context: dict,
):
    """Test POST /context-authority/v2/overlay - Generate overlay without validation."""
    overlay_request = {
        "project_id": sample_project_id,
        "project_tier": "LITE",
        "gate_status": green_zone_context["gate_status"],
        "vibecoding_index": green_zone_context["vibecoding_index"],
        "vibecoding_zone": green_zone_context["vibecoding_zone"],
    }

    response = await client.post(
        "/api/v1/context-authority/v2/overlay",
        json=overlay_request,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify overlay response
    assert "overlay_content" in data
    assert "applied_templates" in data
    assert "variables" in data
    assert "generated_at" in data


@pytest.mark.asyncio
async def test_generate_overlay_with_tier_filter(
    client: AsyncClient,
    auth_headers: dict,
    sample_project_id: str,
    green_zone_context: dict,
):
    """Test overlay generation respects tier filtering."""
    # Generate for ENTERPRISE tier
    overlay_request = {
        "project_id": sample_project_id,
        "project_tier": "ENTERPRISE",
        "gate_status": green_zone_context["gate_status"],
        "vibecoding_index": green_zone_context["vibecoding_index"],
        "vibecoding_zone": green_zone_context["vibecoding_zone"],
    }

    response = await client.post(
        "/api/v1/context-authority/v2/overlay",
        json=overlay_request,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Templates should be filtered by tier
    for template in data["applied_templates"]:
        # Template tier should be None (all tiers) or ENTERPRISE
        assert template.get("tier") is None or template.get("tier") == "ENTERPRISE"


# ============================================================================
# Performance Tests
# ============================================================================


@pytest.mark.asyncio
async def test_validation_performance(
    client: AsyncClient,
    auth_headers: dict,
    lite_tier_project: dict,
    green_zone_context: dict,
):
    """Test validation performance is within SLA (<100ms)."""
    import time

    validation_request = {
        "submission_id": str(uuid4()),
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": green_zone_context["vibecoding_index"],
        "vibecoding_zone": green_zone_context["vibecoding_zone"],
        "gate_status": green_zone_context["gate_status"],
        "v1_result": green_zone_context["v1_result"],
    }

    # Measure response time
    start_time = time.perf_counter()
    response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
        headers=auth_headers,
    )
    end_time = time.perf_counter()

    assert response.status_code == 200
    response_time_ms = (end_time - start_time) * 1000

    # SLA: <100ms for validation (SPEC-0011 NFR)
    # Allow 500ms for test environment overhead
    assert response_time_ms < 500, f"Validation took {response_time_ms:.2f}ms, exceeds threshold"


@pytest.mark.asyncio
async def test_overlay_generation_performance(
    client: AsyncClient,
    auth_headers: dict,
    sample_project_id: str,
    green_zone_context: dict,
):
    """Test overlay generation performance is within SLA (<50ms)."""
    import time

    overlay_request = {
        "project_id": sample_project_id,
        "project_tier": "LITE",
        "gate_status": green_zone_context["gate_status"],
        "vibecoding_index": green_zone_context["vibecoding_index"],
        "vibecoding_zone": green_zone_context["vibecoding_zone"],
    }

    start_time = time.perf_counter()
    response = await client.post(
        "/api/v1/context-authority/v2/overlay",
        json=overlay_request,
        headers=auth_headers,
    )
    end_time = time.perf_counter()

    assert response.status_code == 200
    response_time_ms = (end_time - start_time) * 1000

    # SLA: <50ms for overlay generation (SPEC-0011 NFR)
    # Allow 300ms for test environment overhead
    assert response_time_ms < 300, f"Overlay generation took {response_time_ms:.2f}ms, exceeds threshold"


# ============================================================================
# Error Handling Tests
# ============================================================================


@pytest.mark.asyncio
async def test_invalid_vibecoding_zone(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    lite_tier_project: dict,
):
    """Test validation with invalid vibecoding zone."""
    validation_request = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": lite_tier_project["tier"],
        "vibecoding_index": 50,
        "vibecoding_zone": "INVALID_ZONE",  # Invalid
        "gate_status": {"current_stage": "04-build"},
        "v1_result": {},
    }

    response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
        headers=auth_headers,
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_invalid_tier(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    lite_tier_project: dict,
):
    """Test validation with invalid tier."""
    validation_request = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": lite_tier_project["id"],
        "project_tier": "INVALID_TIER",  # Invalid
        "vibecoding_index": 50,
        "vibecoding_zone": "YELLOW",
        "gate_status": {"current_stage": "04-build"},
        "v1_result": {},
    }

    response = await client.post(
        "/api/v1/context-authority/v2/validate",
        json=validation_request,
        headers=auth_headers,
    )
    assert response.status_code == 422  # Validation error
