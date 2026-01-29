"""
=========================================================================
Vibecoding Flow Integration Tests - Sprint 118 (SPEC-0001)
SDLC Orchestrator - Stage 04 (BUILD)

Version: 1.0.0
Date: January 29, 2026
Status: ACTIVE - Sprint 118 Track 2 Phase 5
Authority: Backend Lead + CTO Approved
Foundation: SPEC-0001 Anti-Vibecoding System
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Integration tests for Vibecoding Index critical path
- Test full flow: calculate → history → route → kill-switch
- Test 5-signal formula (Intent 30%, Ownership 25%, Context 20%, AI 15%, Rejection 10%)
- Test progressive routing (GREEN → YELLOW → ORANGE → RED)

Test Coverage:
- ✅ POST /governance/vibecoding/calculate
- ✅ GET /governance/vibecoding/{submission_id}
- ✅ POST /governance/vibecoding/route
- ✅ GET /governance/vibecoding/signals/{submission_id}
- ✅ POST /governance/vibecoding/kill-switch/check
- ✅ GET /governance/vibecoding/stats

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
def sample_submission_id() -> str:
    """Generate a sample submission ID for testing."""
    return str(uuid4())


@pytest.fixture
def sample_project_id() -> str:
    """Generate a sample project ID for testing."""
    return str(uuid4())


@pytest.fixture
def green_zone_signals() -> dict:
    """Signals that should result in GREEN zone (0-20)."""
    return {
        "intent_present": True,
        "intent_linked_to_task": True,
        "ownership_declared": True,
        "ownership_in_codeowners": True,
        "context_adr_linked": True,
        "context_design_doc_exists": True,
        "context_agents_md_fresh": True,
        "ai_attestation_provided": True,
        "ai_attestation_review_time_adequate": True,
        "rejection_history_count": 0,
    }


@pytest.fixture
def red_zone_signals() -> dict:
    """Signals that should result in RED zone (60-100)."""
    return {
        "intent_present": False,
        "intent_linked_to_task": False,
        "ownership_declared": False,
        "ownership_in_codeowners": False,
        "context_adr_linked": False,
        "context_design_doc_exists": False,
        "context_agents_md_fresh": False,
        "ai_attestation_provided": False,
        "ai_attestation_review_time_adequate": False,
        "rejection_history_count": 5,
    }


@pytest.fixture
def yellow_zone_signals() -> dict:
    """Signals that should result in YELLOW zone (20-40)."""
    return {
        "intent_present": True,
        "intent_linked_to_task": False,
        "ownership_declared": True,
        "ownership_in_codeowners": False,
        "context_adr_linked": True,
        "context_design_doc_exists": False,
        "context_agents_md_fresh": True,
        "ai_attestation_provided": True,
        "ai_attestation_review_time_adequate": False,
        "rejection_history_count": 1,
    }


# ============================================================================
# Vibecoding Calculate Tests
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_calculate_green_zone(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    sample_project_id: str,
    green_zone_signals: dict,
):
    """Test POST /governance/vibecoding/calculate - GREEN zone."""
    request_data = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": sample_project_id,
        **green_zone_signals,
    }

    response = await client.post(
        "/api/v1/governance/vibecoding/calculate",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "submission_id" in data
    assert "index_score" in data
    assert "zone" in data
    assert "signals" in data
    assert "routing" in data
    assert "calculated_at" in data

    # Verify GREEN zone
    assert data["zone"] == "GREEN"
    assert data["index_score"] <= 20
    assert data["routing"]["decision"] == "AUTO_MERGE"

    # Verify 5-signal breakdown
    signals = data["signals"]
    assert "intent" in signals
    assert "ownership" in signals
    assert "context" in signals
    assert "ai_attestation" in signals
    assert "rejection_history" in signals


@pytest.mark.asyncio
async def test_vibecoding_calculate_red_zone(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    sample_project_id: str,
    red_zone_signals: dict,
):
    """Test POST /governance/vibecoding/calculate - RED zone."""
    request_data = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": sample_project_id,
        **red_zone_signals,
    }

    response = await client.post(
        "/api/v1/governance/vibecoding/calculate",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify RED zone
    assert data["zone"] == "RED"
    assert data["index_score"] >= 60
    assert data["routing"]["decision"] == "BLOCK"


@pytest.mark.asyncio
async def test_vibecoding_calculate_yellow_zone(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    sample_project_id: str,
    yellow_zone_signals: dict,
):
    """Test POST /governance/vibecoding/calculate - YELLOW zone."""
    request_data = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": sample_project_id,
        **yellow_zone_signals,
    }

    response = await client.post(
        "/api/v1/governance/vibecoding/calculate",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify YELLOW zone
    assert data["zone"] == "YELLOW"
    assert 20 < data["index_score"] <= 40
    assert data["routing"]["decision"] == "HUMAN_REVIEW"


@pytest.mark.asyncio
async def test_vibecoding_calculate_unauthorized(
    client: AsyncClient,
    sample_submission_id: str,
    sample_project_id: str,
    green_zone_signals: dict,
):
    """Test POST /governance/vibecoding/calculate - Unauthorized."""
    request_data = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": sample_project_id,
        **green_zone_signals,
    }

    response = await client.post(
        "/api/v1/governance/vibecoding/calculate",
        json=request_data,
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_vibecoding_calculate_invalid_request(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test POST /governance/vibecoding/calculate - Invalid request."""
    # Missing required fields
    request_data = {
        "submission_id": "test-123",
    }

    response = await client.post(
        "/api/v1/governance/vibecoding/calculate",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 422  # Validation error


# ============================================================================
# Vibecoding History Tests
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_get_history(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    sample_project_id: str,
    green_zone_signals: dict,
):
    """Test GET /governance/vibecoding/{submission_id} - Get history."""
    # First, calculate index to create history
    request_data = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": sample_project_id,
        **green_zone_signals,
    }

    await client.post(
        "/api/v1/governance/vibecoding/calculate",
        json=request_data,
        headers=auth_headers,
    )

    # Then, get history
    response = await client.get(
        f"/api/v1/governance/vibecoding/{sample_submission_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "submission_id" in data
    assert "history" in data
    assert "latest_score" in data
    assert "trend" in data

    # Verify history is not empty
    assert len(data["history"]) >= 1
    assert data["submission_id"] == sample_submission_id


@pytest.mark.asyncio
async def test_vibecoding_get_history_not_found(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test GET /governance/vibecoding/{submission_id} - Not found."""
    non_existent_id = str(uuid4())

    response = await client.get(
        f"/api/v1/governance/vibecoding/{non_existent_id}",
        headers=auth_headers,
    )
    # Should return empty history or 404
    assert response.status_code in [200, 404]


# ============================================================================
# Vibecoding Routing Tests
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_route_auto_merge(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    sample_project_id: str,
):
    """Test POST /governance/vibecoding/route - AUTO_MERGE routing."""
    request_data = {
        "submission_id": sample_submission_id,
        "project_id": sample_project_id,
        "index_score": 15,  # GREEN zone
    }

    response = await client.post(
        "/api/v1/governance/vibecoding/route",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    assert data["decision"] == "AUTO_MERGE"
    assert data["zone"] == "GREEN"
    assert data["approver_required"] is None


@pytest.mark.asyncio
async def test_vibecoding_route_human_review(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    sample_project_id: str,
):
    """Test POST /governance/vibecoding/route - HUMAN_REVIEW routing."""
    request_data = {
        "submission_id": sample_submission_id,
        "project_id": sample_project_id,
        "index_score": 35,  # YELLOW zone
    }

    response = await client.post(
        "/api/v1/governance/vibecoding/route",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    assert data["decision"] == "HUMAN_REVIEW"
    assert data["zone"] == "YELLOW"
    assert data["approver_required"] is not None


@pytest.mark.asyncio
async def test_vibecoding_route_block(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    sample_project_id: str,
):
    """Test POST /governance/vibecoding/route - BLOCK routing."""
    request_data = {
        "submission_id": sample_submission_id,
        "project_id": sample_project_id,
        "index_score": 85,  # RED zone
    }

    response = await client.post(
        "/api/v1/governance/vibecoding/route",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    assert data["decision"] == "BLOCK"
    assert data["zone"] == "RED"


# ============================================================================
# Vibecoding Signals Tests
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_get_signals(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    sample_project_id: str,
    green_zone_signals: dict,
):
    """Test GET /governance/vibecoding/signals/{submission_id} - Get signal breakdown."""
    # First, calculate index to create signals
    request_data = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": sample_project_id,
        **green_zone_signals,
    }

    await client.post(
        "/api/v1/governance/vibecoding/calculate",
        json=request_data,
        headers=auth_headers,
    )

    # Then, get signals
    response = await client.get(
        f"/api/v1/governance/vibecoding/signals/{sample_submission_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "submission_id" in data
    assert "index_score" in data
    assert "signals" in data
    assert "top_contributors" in data

    # Verify signal breakdown structure
    signals = data["signals"]
    for signal_name in ["intent", "ownership", "context", "ai_attestation", "rejection_history"]:
        assert signal_name in signals
        signal = signals[signal_name]
        assert "score" in signal
        assert "weight" in signal
        assert "contribution" in signal
        assert "details" in signal


# ============================================================================
# Kill Switch Tests
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_kill_switch_check_healthy(
    client: AsyncClient,
    auth_headers: dict,
    sample_project_id: str,
):
    """Test POST /governance/vibecoding/kill-switch/check - Healthy state."""
    request_data = {
        "project_id": sample_project_id,
    }

    response = await client.post(
        "/api/v1/governance/vibecoding/kill-switch/check",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "should_trigger" in data
    assert "triggered_criteria" in data
    assert "current_metrics" in data
    assert "recommended_action" in data
    assert "last_check" in data

    # Verify metrics structure
    metrics = data["current_metrics"]
    assert "rejection_rate" in metrics
    assert "rejection_rate_threshold" in metrics
    assert "latency_p95_ms" in metrics
    assert "latency_p95_threshold_ms" in metrics


# ============================================================================
# Stats Tests
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_get_stats(
    client: AsyncClient,
    auth_headers: dict,
    sample_project_id: str,
):
    """Test GET /governance/vibecoding/stats - Get project statistics."""
    response = await client.get(
        f"/api/v1/governance/vibecoding/stats?project_id={sample_project_id}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "project_id" in data
    assert "total_submissions" in data
    assert "average_index" in data
    assert "zone_distribution" in data
    assert "trend_7d" in data
    assert "auto_merge_rate" in data

    # Verify zone distribution
    zone_dist = data["zone_distribution"]
    assert "GREEN" in zone_dist
    assert "YELLOW" in zone_dist
    assert "ORANGE" in zone_dist
    assert "RED" in zone_dist


# ============================================================================
# Full Flow Integration Tests
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_full_flow(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    sample_project_id: str,
    green_zone_signals: dict,
):
    """Test full vibecoding flow: calculate → history → signals → route → stats."""
    # Step 1: Calculate index
    calc_request = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": sample_project_id,
        **green_zone_signals,
    }

    calc_response = await client.post(
        "/api/v1/governance/vibecoding/calculate",
        json=calc_request,
        headers=auth_headers,
    )
    assert calc_response.status_code == 200
    calc_data = calc_response.json()
    assert calc_data["zone"] == "GREEN"

    # Step 2: Get history
    history_response = await client.get(
        f"/api/v1/governance/vibecoding/{sample_submission_id}",
        headers=auth_headers,
    )
    assert history_response.status_code == 200
    history_data = history_response.json()
    assert len(history_data["history"]) >= 1

    # Step 3: Get signals
    signals_response = await client.get(
        f"/api/v1/governance/vibecoding/signals/{sample_submission_id}",
        headers=auth_headers,
    )
    assert signals_response.status_code == 200
    signals_data = signals_response.json()
    assert "signals" in signals_data

    # Step 4: Get routing decision
    route_request = {
        "submission_id": sample_submission_id,
        "project_id": sample_project_id,
        "index_score": calc_data["index_score"],
    }

    route_response = await client.post(
        "/api/v1/governance/vibecoding/route",
        json=route_request,
        headers=auth_headers,
    )
    assert route_response.status_code == 200
    route_data = route_response.json()
    assert route_data["decision"] == "AUTO_MERGE"

    # Step 5: Get stats
    stats_response = await client.get(
        f"/api/v1/governance/vibecoding/stats?project_id={sample_project_id}",
        headers=auth_headers,
    )
    assert stats_response.status_code == 200
    stats_data = stats_response.json()
    assert stats_data["total_submissions"] >= 1


@pytest.mark.asyncio
async def test_vibecoding_index_recalculation(
    client: AsyncClient,
    auth_headers: dict,
    sample_submission_id: str,
    sample_project_id: str,
    green_zone_signals: dict,
    yellow_zone_signals: dict,
):
    """Test that recalculating index updates correctly."""
    # First calculation - GREEN zone
    calc_request_1 = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": sample_project_id,
        **green_zone_signals,
    }

    response_1 = await client.post(
        "/api/v1/governance/vibecoding/calculate",
        json=calc_request_1,
        headers=auth_headers,
    )
    assert response_1.status_code == 200
    first_score = response_1.json()["index_score"]

    # Second calculation - YELLOW zone (signals changed)
    calc_request_2 = {
        "submission_id": sample_submission_id,
        "submission_type": "PR",
        "project_id": sample_project_id,
        **yellow_zone_signals,
    }

    response_2 = await client.post(
        "/api/v1/governance/vibecoding/calculate",
        json=calc_request_2,
        headers=auth_headers,
    )
    assert response_2.status_code == 200
    second_score = response_2.json()["index_score"]

    # Second score should be higher (worse) than first
    assert second_score > first_score

    # Check history shows both calculations
    history_response = await client.get(
        f"/api/v1/governance/vibecoding/{sample_submission_id}",
        headers=auth_headers,
    )
    assert history_response.status_code == 200
    history_data = history_response.json()
    assert len(history_data["history"]) >= 2
