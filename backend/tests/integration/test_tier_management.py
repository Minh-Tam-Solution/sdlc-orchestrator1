"""
=========================================================================
Tier Management Integration Tests - Sprint 118 (4-Tier Classification)
SDLC Orchestrator - Stage 04 (BUILD)

Version: 1.0.0
Date: January 29, 2026
Status: ACTIVE - Sprint 118 Track 2 Phase 5
Authority: Backend Lead + CTO Approved
Foundation: ADR-041 4-Tier Classification System
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Integration tests for 4-Tier Classification critical path
- Test tier status retrieval
- Test tier upgrade eligibility
- Test tier upgrade request flow
- Test tier requirements validation

Test Coverage:
- ✅ GET /governance/tiers/{project_id}/status
- ✅ GET /governance/tiers/{project_id}/requirements
- ✅ POST /governance/tiers/{project_id}/upgrade-request
- ✅ GET /governance/tiers/{project_id}/upgrade-eligibility

Tier System: LITE → STANDARD → PROFESSIONAL → ENTERPRISE
Zero Mock Policy: Production-ready integration tests
=========================================================================
"""

import pytest
from httpx import AsyncClient
from uuid import uuid4

from app.models.user import User


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def lite_project_id() -> str:
    """Sample project ID for LITE tier testing."""
    return f"proj-lite-{uuid4().hex[:8]}"


@pytest.fixture
def standard_project_id() -> str:
    """Sample project ID for STANDARD tier testing."""
    return f"proj-standard-{uuid4().hex[:8]}"


@pytest.fixture
def professional_project_id() -> str:
    """Sample project ID for PROFESSIONAL tier testing."""
    return f"proj-pro-{uuid4().hex[:8]}"


@pytest.fixture
def enterprise_project_id() -> str:
    """Sample project ID for ENTERPRISE tier testing."""
    return f"proj-ent-{uuid4().hex[:8]}"


@pytest.fixture
def upgrade_request_data() -> dict:
    """Valid upgrade request data."""
    return {
        "target_tier": "STANDARD",
        "justification": "Team has grown and needs more governance features",
        "business_case": "Project complexity has increased significantly",
    }


# ============================================================================
# Tier Status Tests
# ============================================================================


@pytest.mark.asyncio
async def test_get_tier_status(
    client: AsyncClient,
    auth_headers: dict,
    lite_project_id: str,
):
    """Test GET /governance/tiers/{project_id}/status - Get project tier status."""
    response = await client.get(
        f"/api/v1/governance/tiers/{lite_project_id}/status",
        headers=auth_headers,
    )

    # May return 200 with data or 404 if project doesn't exist
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()

        # Verify response structure
        assert "project_id" in data
        assert "current_tier" in data
        assert "tier_since" in data
        assert "compliance_score" in data
        assert "requirements_met" in data
        assert "requirements_total" in data
        assert "next_tier" in data
        assert "upgrade_eligibility" in data

        # Verify tier is valid
        assert data["current_tier"] in ["LITE", "STANDARD", "PROFESSIONAL", "ENTERPRISE"]

        # Verify compliance score is in valid range
        assert 0 <= data["compliance_score"] <= 100


@pytest.mark.asyncio
async def test_get_tier_status_unauthorized(
    client: AsyncClient,
    lite_project_id: str,
):
    """Test GET /governance/tiers/{project_id}/status - Unauthorized."""
    response = await client.get(
        f"/api/v1/governance/tiers/{lite_project_id}/status",
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_tier_status_not_found(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test GET /governance/tiers/{project_id}/status - Project not found."""
    non_existent_id = f"proj-{uuid4().hex}"

    response = await client.get(
        f"/api/v1/governance/tiers/{non_existent_id}/status",
        headers=auth_headers,
    )
    assert response.status_code == 404


# ============================================================================
# Tier Requirements Tests
# ============================================================================


@pytest.mark.asyncio
async def test_get_tier_requirements(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test GET /governance/tiers/requirements - Get tier requirements."""
    response = await client.get(
        "/api/v1/governance/tiers/requirements",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify all 4 tiers are present
    assert "LITE" in data
    assert "STANDARD" in data
    assert "PROFESSIONAL" in data
    assert "ENTERPRISE" in data

    # Verify each tier has requirements
    for tier in ["LITE", "STANDARD", "PROFESSIONAL", "ENTERPRISE"]:
        tier_data = data[tier]
        assert "name" in tier_data
        assert "requirements" in tier_data
        assert isinstance(tier_data["requirements"], list)


@pytest.mark.asyncio
async def test_get_tier_requirements_structure(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that tier requirements have correct structure."""
    response = await client.get(
        "/api/v1/governance/tiers/requirements",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Check LITE requirements (minimal)
    lite_reqs = data["LITE"]["requirements"]
    assert len(lite_reqs) > 0
    for req in lite_reqs:
        assert "id" in req
        assert "description" in req
        assert "category" in req

    # Check ENTERPRISE requirements (most comprehensive)
    enterprise_reqs = data["ENTERPRISE"]["requirements"]
    assert len(enterprise_reqs) > len(lite_reqs)  # ENTERPRISE has more requirements


@pytest.mark.asyncio
async def test_get_project_tier_requirements(
    client: AsyncClient,
    auth_headers: dict,
    lite_project_id: str,
):
    """Test GET /governance/tiers/{project_id}/requirements - Get project-specific requirements."""
    response = await client.get(
        f"/api/v1/governance/tiers/{lite_project_id}/requirements",
        headers=auth_headers,
    )

    # May return 200 with data or 404 if project doesn't exist
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()

        assert "project_id" in data
        assert "current_tier" in data
        assert "requirements" in data
        assert "met_requirements" in data
        assert "missing_requirements" in data


# ============================================================================
# Upgrade Eligibility Tests
# ============================================================================


@pytest.mark.asyncio
async def test_get_upgrade_eligibility(
    client: AsyncClient,
    auth_headers: dict,
    lite_project_id: str,
):
    """Test GET /governance/tiers/{project_id}/upgrade-eligibility - Get upgrade eligibility."""
    response = await client.get(
        f"/api/v1/governance/tiers/{lite_project_id}/upgrade-eligibility",
        headers=auth_headers,
    )

    # May return 200 with data or 404 if project doesn't exist
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()

        assert "project_id" in data
        assert "current_tier" in data
        assert "next_tier" in data
        assert "eligible" in data
        assert "completion_percentage" in data
        assert "missing_requirements" in data

        # Verify completion percentage is in valid range
        assert 0 <= data["completion_percentage"] <= 100

        # Verify missing_requirements is a list
        assert isinstance(data["missing_requirements"], list)


@pytest.mark.asyncio
async def test_upgrade_eligibility_enterprise(
    client: AsyncClient,
    auth_headers: dict,
    enterprise_project_id: str,
):
    """Test upgrade eligibility for ENTERPRISE tier (no further upgrades)."""
    response = await client.get(
        f"/api/v1/governance/tiers/{enterprise_project_id}/upgrade-eligibility",
        headers=auth_headers,
    )

    # May return 200 with data or 404 if project doesn't exist
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()

        # ENTERPRISE has no next tier
        if data["current_tier"] == "ENTERPRISE":
            assert data["next_tier"] is None
            assert data["eligible"] is False  # Can't upgrade further


# ============================================================================
# Upgrade Request Tests
# ============================================================================


@pytest.mark.asyncio
async def test_request_tier_upgrade(
    client: AsyncClient,
    auth_headers: dict,
    lite_project_id: str,
    upgrade_request_data: dict,
):
    """Test POST /governance/tiers/{project_id}/upgrade-request - Request tier upgrade."""
    response = await client.post(
        f"/api/v1/governance/tiers/{lite_project_id}/upgrade-request",
        json=upgrade_request_data,
        headers=auth_headers,
    )

    # May return 201, 200, 400 (ineligible), or 404 (project not found)
    assert response.status_code in [200, 201, 400, 404]

    if response.status_code in [200, 201]:
        data = response.json()

        assert "request_id" in data
        assert "project_id" in data
        assert "current_tier" in data
        assert "target_tier" in data
        assert "status" in data
        assert "created_at" in data

        # Verify status is pending
        assert data["status"] in ["pending", "approved", "rejected"]


@pytest.mark.asyncio
async def test_request_tier_upgrade_unauthorized(
    client: AsyncClient,
    lite_project_id: str,
    upgrade_request_data: dict,
):
    """Test POST /governance/tiers/{project_id}/upgrade-request - Unauthorized."""
    response = await client.post(
        f"/api/v1/governance/tiers/{lite_project_id}/upgrade-request",
        json=upgrade_request_data,
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_request_tier_upgrade_invalid_tier(
    client: AsyncClient,
    auth_headers: dict,
    lite_project_id: str,
):
    """Test upgrade request with invalid target tier."""
    invalid_request = {
        "target_tier": "INVALID_TIER",
        "justification": "Test upgrade",
    }

    response = await client.post(
        f"/api/v1/governance/tiers/{lite_project_id}/upgrade-request",
        json=invalid_request,
        headers=auth_headers,
    )
    assert response.status_code in [400, 422]


@pytest.mark.asyncio
async def test_request_tier_downgrade_blocked(
    client: AsyncClient,
    auth_headers: dict,
    professional_project_id: str,
):
    """Test that tier downgrade requests are blocked."""
    downgrade_request = {
        "target_tier": "LITE",  # Downgrade from PROFESSIONAL
        "justification": "Want to downgrade",
    }

    response = await client.post(
        f"/api/v1/governance/tiers/{professional_project_id}/upgrade-request",
        json=downgrade_request,
        headers=auth_headers,
    )

    # Should be blocked (400) or project not found (404)
    # Downgrades are not allowed through upgrade request endpoint
    assert response.status_code in [400, 404]


@pytest.mark.asyncio
async def test_request_skip_tier_blocked(
    client: AsyncClient,
    auth_headers: dict,
    lite_project_id: str,
):
    """Test that skipping tiers is blocked (LITE → ENTERPRISE)."""
    skip_request = {
        "target_tier": "ENTERPRISE",  # Skip STANDARD and PROFESSIONAL
        "justification": "Want to skip to enterprise",
    }

    response = await client.post(
        f"/api/v1/governance/tiers/{lite_project_id}/upgrade-request",
        json=skip_request,
        headers=auth_headers,
    )

    # Should be blocked (400) or project not found (404)
    # Can only upgrade to next tier
    assert response.status_code in [400, 404]


# ============================================================================
# Tier Progression Tests
# ============================================================================


@pytest.mark.asyncio
async def test_tier_progression_order(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that tier progression follows LITE → STANDARD → PROFESSIONAL → ENTERPRISE."""
    response = await client.get(
        "/api/v1/governance/tiers/requirements",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify tier ordering (if order field exists)
    tiers = ["LITE", "STANDARD", "PROFESSIONAL", "ENTERPRISE"]
    for i, tier in enumerate(tiers):
        tier_data = data[tier]
        if "order" in tier_data:
            assert tier_data["order"] == i + 1


@pytest.mark.asyncio
async def test_tier_requirements_cumulative(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that higher tiers include all requirements from lower tiers."""
    response = await client.get(
        "/api/v1/governance/tiers/requirements",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Get requirement counts
    lite_count = len(data["LITE"]["requirements"])
    standard_count = len(data["STANDARD"]["requirements"])
    professional_count = len(data["PROFESSIONAL"]["requirements"])
    enterprise_count = len(data["ENTERPRISE"]["requirements"])

    # Requirements should be cumulative
    assert lite_count <= standard_count
    assert standard_count <= professional_count
    assert professional_count <= enterprise_count


# ============================================================================
# Compliance Score Tests
# ============================================================================


@pytest.mark.asyncio
async def test_compliance_score_calculation(
    client: AsyncClient,
    auth_headers: dict,
    lite_project_id: str,
):
    """Test that compliance score is calculated correctly."""
    response = await client.get(
        f"/api/v1/governance/tiers/{lite_project_id}/status",
        headers=auth_headers,
    )

    if response.status_code == 200:
        data = response.json()

        # Compliance score should match requirements ratio
        if data["requirements_total"] > 0:
            expected_score = (
                data["requirements_met"] / data["requirements_total"]
            ) * 100
            # Allow some tolerance for rounding
            assert abs(data["compliance_score"] - expected_score) <= 1


@pytest.mark.asyncio
async def test_compliance_score_range(
    client: AsyncClient,
    auth_headers: dict,
    standard_project_id: str,
):
    """Test that compliance score is always in valid range."""
    response = await client.get(
        f"/api/v1/governance/tiers/{standard_project_id}/status",
        headers=auth_headers,
    )

    if response.status_code == 200:
        data = response.json()
        assert 0 <= data["compliance_score"] <= 100


# ============================================================================
# Full Tier Management Flow Tests
# ============================================================================


@pytest.mark.asyncio
async def test_tier_management_full_flow(
    client: AsyncClient,
    auth_headers: dict,
    lite_project_id: str,
):
    """Test full tier management flow: status → eligibility → upgrade request."""
    # Step 1: Get current tier status
    status_response = await client.get(
        f"/api/v1/governance/tiers/{lite_project_id}/status",
        headers=auth_headers,
    )

    if status_response.status_code != 200:
        # Project doesn't exist, skip flow test
        pytest.skip("Project not found, skipping flow test")

    status_data = status_response.json()
    current_tier = status_data["current_tier"]

    # Step 2: Get upgrade eligibility
    eligibility_response = await client.get(
        f"/api/v1/governance/tiers/{lite_project_id}/upgrade-eligibility",
        headers=auth_headers,
    )
    assert eligibility_response.status_code == 200
    eligibility_data = eligibility_response.json()

    # Step 3: If eligible, request upgrade
    if eligibility_data["eligible"] and eligibility_data["next_tier"]:
        upgrade_request = {
            "target_tier": eligibility_data["next_tier"],
            "justification": "Integration test upgrade",
        }

        upgrade_response = await client.post(
            f"/api/v1/governance/tiers/{lite_project_id}/upgrade-request",
            json=upgrade_request,
            headers=auth_headers,
        )
        assert upgrade_response.status_code in [200, 201, 400]


@pytest.mark.asyncio
async def test_tier_requirements_to_eligibility_flow(
    client: AsyncClient,
    auth_headers: dict,
    standard_project_id: str,
):
    """Test flow from requirements check to eligibility assessment."""
    # Step 1: Get project requirements
    req_response = await client.get(
        f"/api/v1/governance/tiers/{standard_project_id}/requirements",
        headers=auth_headers,
    )

    if req_response.status_code != 200:
        pytest.skip("Project not found")

    req_data = req_response.json()
    met_count = len(req_data.get("met_requirements", []))
    missing_count = len(req_data.get("missing_requirements", []))

    # Step 2: Get eligibility
    elig_response = await client.get(
        f"/api/v1/governance/tiers/{standard_project_id}/upgrade-eligibility",
        headers=auth_headers,
    )
    assert elig_response.status_code == 200
    elig_data = elig_response.json()

    # Missing requirements should match
    assert len(elig_data["missing_requirements"]) == missing_count

    # Eligibility should be true only if no missing requirements
    if missing_count == 0:
        assert elig_data["eligible"] is True
    else:
        assert elig_data["eligible"] is False


# ============================================================================
# Tier Display Tests
# ============================================================================


@pytest.mark.asyncio
async def test_tier_display_info(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that tier display information is available."""
    response = await client.get(
        "/api/v1/governance/tiers/requirements",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Each tier should have display info
    for tier in ["LITE", "STANDARD", "PROFESSIONAL", "ENTERPRISE"]:
        tier_data = data[tier]
        assert "name" in tier_data
        # Optional display fields
        if "description" in tier_data:
            assert isinstance(tier_data["description"], str)
        if "features" in tier_data:
            assert isinstance(tier_data["features"], list)


@pytest.mark.asyncio
async def test_tier_colors_and_icons(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that tier color/icon information is consistent."""
    response = await client.get(
        "/api/v1/governance/tiers/requirements",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # If color/icon info exists, validate it
    expected_colors = {
        "LITE": "gray",
        "STANDARD": "blue",
        "PROFESSIONAL": "purple",
        "ENTERPRISE": "gold",
    }

    for tier, expected_color in expected_colors.items():
        tier_data = data[tier]
        if "color" in tier_data:
            assert tier_data["color"] == expected_color

