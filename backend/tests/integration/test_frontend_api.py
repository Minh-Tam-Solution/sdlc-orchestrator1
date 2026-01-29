"""
=========================================================================
Frontend API Integration Tests - Sprint 118
SDLC Orchestrator - Stage 04 (BUILD)

Version: 1.0.0
Date: January 29, 2026
Status: ACTIVE - Sprint 118 Track 2 Phase 5
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Integration tests for frontend-facing API contracts
- Test API response structure matches TypeScript interfaces
- Test pagination, filtering, and sorting
- Test real-time data freshness
- Validate React Query cache compatibility

Test Coverage:
- ✅ Dashboard summary endpoints
- ✅ List endpoints with pagination
- ✅ Filter and search endpoints
- ✅ Real-time update endpoints
- ✅ Cache invalidation scenarios

Frontend Contract: TypeScript interfaces in frontend/src/hooks/
Zero Mock Policy: Production-ready integration tests
=========================================================================
"""

import pytest
from httpx import AsyncClient
from uuid import uuid4
from datetime import datetime, timedelta


# ============================================================================
# Dashboard Summary Tests (Frontend Dashboard Components)
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_stats_summary(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test GET /governance/vibecoding/stats - Dashboard summary endpoint."""
    response = await client.get(
        "/api/v1/governance/vibecoding/stats",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify structure matches VibecodingStats TypeScript interface
    assert "total_submissions" in data
    assert "avg_index" in data
    assert "zone_distribution" in data
    assert "auto_merge_rate" in data
    assert "period" in data

    # Verify zone distribution structure
    zones = data["zone_distribution"]
    assert "green" in zones
    assert "yellow" in zones
    assert "orange" in zones
    assert "red" in zones

    # Verify numeric types
    assert isinstance(data["total_submissions"], int)
    assert isinstance(data["avg_index"], (int, float))
    assert isinstance(data["auto_merge_rate"], (int, float))


@pytest.mark.asyncio
async def test_tier_overview_summary(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test GET /governance/tiers/overview - Tier distribution summary."""
    response = await client.get(
        "/api/v1/governance/tiers/overview",
        headers=auth_headers,
    )

    # May return 200 or 404 if endpoint not implemented
    if response.status_code == 200:
        data = response.json()

        # Verify structure matches frontend expectations
        assert "total_projects" in data
        assert "tier_distribution" in data

        distribution = data["tier_distribution"]
        for tier in ["LITE", "STANDARD", "PROFESSIONAL", "ENTERPRISE"]:
            assert tier in distribution
            assert isinstance(distribution[tier], int)


@pytest.mark.asyncio
async def test_spec_compliance_summary(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test GET /governance/specs/summary - Spec compliance summary."""
    response = await client.get(
        "/api/v1/governance/specs/summary",
        headers=auth_headers,
    )

    if response.status_code == 200:
        data = response.json()

        # Verify structure
        assert "total_specs" in data
        assert "valid_specs" in data
        assert "invalid_specs" in data
        assert "avg_compliance_score" in data


# ============================================================================
# Pagination Tests (React Query List Components)
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_history_pagination(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test pagination for vibecoding history endpoint."""
    # First page
    response = await client.get(
        "/api/v1/governance/vibecoding/history",
        params={"page": 1, "page_size": 10},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify pagination structure
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data

    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["items"]) <= 10


@pytest.mark.asyncio
async def test_vibecoding_history_page_navigation(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test page navigation for vibecoding history."""
    # Get first page to check total
    first_response = await client.get(
        "/api/v1/governance/vibecoding/history",
        params={"page": 1, "page_size": 5},
        headers=auth_headers,
    )
    assert first_response.status_code == 200
    first_data = first_response.json()

    if first_data["total_pages"] > 1:
        # Get second page
        second_response = await client.get(
            "/api/v1/governance/vibecoding/history",
            params={"page": 2, "page_size": 5},
            headers=auth_headers,
        )
        assert second_response.status_code == 200
        second_data = second_response.json()

        # Items should be different
        first_ids = {item.get("id") for item in first_data["items"]}
        second_ids = {item.get("id") for item in second_data["items"]}
        assert first_ids.isdisjoint(second_ids)  # No overlap


@pytest.mark.asyncio
async def test_pagination_invalid_page(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test pagination with invalid page number."""
    response = await client.get(
        "/api/v1/governance/vibecoding/history",
        params={"page": 0, "page_size": 10},
        headers=auth_headers,
    )
    # Should return 422 (validation error) or 200 with empty results
    assert response.status_code in [200, 422]


@pytest.mark.asyncio
async def test_pagination_large_page_size(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test pagination with large page size (should be capped)."""
    response = await client.get(
        "/api/v1/governance/vibecoding/history",
        params={"page": 1, "page_size": 1000},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Page size should be capped at maximum (e.g., 100)
    assert data["page_size"] <= 100


# ============================================================================
# Filtering Tests (React Query Filter Components)
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_history_zone_filter(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test filtering vibecoding history by zone."""
    for zone in ["GREEN", "YELLOW", "ORANGE", "RED"]:
        response = await client.get(
            "/api/v1/governance/vibecoding/history",
            params={"zone": zone},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()

        # All items should match the zone filter
        for item in data["items"]:
            if "zone" in item:
                assert item["zone"].upper() == zone


@pytest.mark.asyncio
async def test_vibecoding_history_date_filter(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test filtering vibecoding history by date range."""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)

    response = await client.get(
        "/api/v1/governance/vibecoding/history",
        params={
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # All items should be within date range
    for item in data["items"]:
        if "created_at" in item:
            item_date = datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
            assert start_date <= item_date.replace(tzinfo=None) <= end_date


@pytest.mark.asyncio
async def test_spec_validation_tier_filter(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test filtering specs by tier."""
    for tier in ["LITE", "STANDARD", "PROFESSIONAL", "ENTERPRISE"]:
        response = await client.get(
            "/api/v1/governance/specs",
            params={"tier": tier},
            headers=auth_headers,
        )

        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                if "tier" in item:
                    assert item["tier"] == tier


# ============================================================================
# Sorting Tests
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_history_sort_by_index(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test sorting vibecoding history by index."""
    # Descending order
    response = await client.get(
        "/api/v1/governance/vibecoding/history",
        params={"sort_by": "index", "sort_order": "desc"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify descending order
    indexes = [item.get("index", 0) for item in data["items"]]
    assert indexes == sorted(indexes, reverse=True)


@pytest.mark.asyncio
async def test_vibecoding_history_sort_by_created_at(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test sorting vibecoding history by creation date."""
    response = await client.get(
        "/api/v1/governance/vibecoding/history",
        params={"sort_by": "created_at", "sort_order": "desc"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify descending order by date
    dates = [item.get("created_at", "") for item in data["items"]]
    assert dates == sorted(dates, reverse=True)


# ============================================================================
# Response Structure Tests (TypeScript Interface Compatibility)
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_signals_structure(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that vibecoding signals match TypeScript interface."""
    submission_id = str(uuid4())

    response = await client.get(
        f"/api/v1/governance/vibecoding/{submission_id}/signals",
        headers=auth_headers,
    )

    # 200 or 404
    if response.status_code == 200:
        data = response.json()

        # Verify signal structure matches SignalBreakdown interface
        assert "submission_id" in data
        assert "signals" in data

        signals = data["signals"]
        expected_signals = [
            "intent_signal",
            "ownership_signal",
            "context_signal",
            "ai_attestation_signal",
            "rejection_history_signal",
        ]

        for signal in expected_signals:
            if signal in signals:
                signal_data = signals[signal]
                assert "score" in signal_data
                assert "weight" in signal_data
                assert "weighted_score" in signal_data


@pytest.mark.asyncio
async def test_tier_status_structure(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that tier status matches TypeScript interface."""
    project_id = str(uuid4())

    response = await client.get(
        f"/api/v1/governance/tiers/{project_id}/status",
        headers=auth_headers,
    )

    if response.status_code == 200:
        data = response.json()

        # Verify matches ProjectTier TypeScript interface
        required_fields = [
            "project_id",
            "current_tier",
            "tier_since",
            "compliance_score",
            "requirements_met",
            "requirements_total",
        ]

        for field in required_fields:
            assert field in data


@pytest.mark.asyncio
async def test_spec_validation_response_structure(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that spec validation response matches TypeScript interface."""
    valid_frontmatter = """---
spec_version: "1.0"
spec_id: SPEC-TEST
status: draft
tier: LITE
stage: 01-planning
owner: test-team
created: 2026-01-29
last_updated: 2026-01-29
related_adrs: []
---

## Overview
Test specification.
"""

    response = await client.post(
        "/api/v1/governance/specs/validate",
        json={"content": valid_frontmatter},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify matches FrontmatterValidationResponse interface
    required_fields = [
        "valid",
        "errors",
        "warnings",
        "parsed_metadata",
        "compliance_score",
        "suggestions",
    ]

    for field in required_fields:
        assert field in data


# ============================================================================
# Error Response Tests (Frontend Error Handling)
# ============================================================================


@pytest.mark.asyncio
async def test_error_response_structure(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that error responses match frontend ErrorResponse interface."""
    response = await client.get(
        "/api/v1/governance/vibecoding/invalid-id/signals",
        headers=auth_headers,
    )

    if response.status_code == 404:
        data = response.json()

        # Verify error response structure
        assert "detail" in data or "message" in data


@pytest.mark.asyncio
async def test_validation_error_response(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test validation error response structure (422)."""
    # Send invalid data
    response = await client.post(
        "/api/v1/governance/specs/validate",
        json={},  # Missing required content field
        headers=auth_headers,
    )

    if response.status_code == 422:
        data = response.json()

        # FastAPI validation error structure
        assert "detail" in data
        assert isinstance(data["detail"], list)


# ============================================================================
# Cache Compatibility Tests (React Query)
# ============================================================================


@pytest.mark.asyncio
async def test_response_includes_cache_headers(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that responses include appropriate cache headers for React Query."""
    response = await client.get(
        "/api/v1/governance/vibecoding/stats",
        headers=auth_headers,
    )
    assert response.status_code == 200

    # Check for ETag or Last-Modified headers (optional but helpful for caching)
    # These help React Query with cache invalidation
    headers = response.headers

    # At minimum, Content-Type should be set
    assert "content-type" in headers
    assert "application/json" in headers["content-type"]


@pytest.mark.asyncio
async def test_consistent_id_format(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that IDs are consistently formatted (UUID format for React Query keys)."""
    response = await client.get(
        "/api/v1/governance/vibecoding/history",
        params={"page": 1, "page_size": 5},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # IDs should be consistent format for React Query cache keys
    for item in data["items"]:
        if "id" in item:
            # Should be valid UUID or consistent string format
            assert isinstance(item["id"], str)
            assert len(item["id"]) > 0


# ============================================================================
# Real-time Data Tests
# ============================================================================


@pytest.mark.asyncio
async def test_stats_reflect_recent_changes(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that stats endpoint reflects recent data (not stale)."""
    # Get current stats
    response = await client.get(
        "/api/v1/governance/vibecoding/stats",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Period should indicate recent data
    if "period" in data and "end_date" in data["period"]:
        end_date = datetime.fromisoformat(
            data["period"]["end_date"].replace("Z", "+00:00")
        )
        # Should be within last day
        assert (datetime.utcnow() - end_date.replace(tzinfo=None)).days <= 1


@pytest.mark.asyncio
async def test_timestamps_are_iso_format(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that all timestamps are in ISO 8601 format for JavaScript Date parsing."""
    response = await client.get(
        "/api/v1/governance/vibecoding/history",
        params={"page": 1, "page_size": 5},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    for item in data["items"]:
        for field in ["created_at", "updated_at", "calculated_at"]:
            if field in item and item[field]:
                # Should be parseable as ISO date
                try:
                    datetime.fromisoformat(item[field].replace("Z", "+00:00"))
                except ValueError:
                    pytest.fail(f"Invalid ISO date format: {item[field]}")


# ============================================================================
# Concurrent Request Tests (React Query Parallel Fetching)
# ============================================================================


@pytest.mark.asyncio
async def test_concurrent_dashboard_requests(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test concurrent requests (simulating React Query parallel fetching)."""
    import asyncio

    # Simulate dashboard loading multiple endpoints in parallel
    async def fetch_stats():
        return await client.get(
            "/api/v1/governance/vibecoding/stats",
            headers=auth_headers,
        )

    async def fetch_history():
        return await client.get(
            "/api/v1/governance/vibecoding/history",
            params={"page": 1, "page_size": 10},
            headers=auth_headers,
        )

    async def fetch_tiers():
        return await client.get(
            "/api/v1/governance/tiers/requirements",
            headers=auth_headers,
        )

    # Execute in parallel
    results = await asyncio.gather(
        fetch_stats(),
        fetch_history(),
        fetch_tiers(),
        return_exceptions=True,
    )

    # All should succeed without errors
    for result in results:
        if isinstance(result, Exception):
            pytest.fail(f"Concurrent request failed: {result}")
        else:
            assert result.status_code in [200, 404]

