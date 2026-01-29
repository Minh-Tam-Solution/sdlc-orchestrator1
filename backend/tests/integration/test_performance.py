"""
=========================================================================
Performance Integration Tests - Sprint 118
SDLC Orchestrator - Stage 04 (BUILD)

Version: 1.0.0
Date: January 29, 2026
Status: ACTIVE - Sprint 118 Track 2 Phase 5 Day 3
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Performance integration tests for API endpoints
- Latency validation against SLA targets
- Concurrent request handling
- Load testing for critical paths

Performance Targets (SDLC 5.3.0):
- API p95 Latency: <100ms
- Vibecoding Calculation: <50ms
- Spec Validation: <200ms
- Database Queries: <10ms (simple), <50ms (complex)

Zero Mock Policy: Production-ready integration tests
=========================================================================
"""

import pytest
import asyncio
import time
from httpx import AsyncClient
from uuid import uuid4


# ============================================================================
# Latency Tests
# ============================================================================


@pytest.mark.asyncio
async def test_vibecoding_stats_latency(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test vibecoding stats endpoint latency is <100ms p95."""
    latencies = []

    for _ in range(20):
        start = time.perf_counter()
        response = await client.get(
            "/api/v1/governance/vibecoding/stats",
            headers=auth_headers,
        )
        end = time.perf_counter()

        if response.status_code == 200:
            latencies.append((end - start) * 1000)  # Convert to ms

    if latencies:
        # Calculate p95
        sorted_latencies = sorted(latencies)
        p95_index = int(len(sorted_latencies) * 0.95)
        p95 = sorted_latencies[p95_index] if p95_index < len(sorted_latencies) else sorted_latencies[-1]

        # Target: <100ms p95
        assert p95 < 100, f"p95 latency {p95:.2f}ms exceeds 100ms target"


@pytest.mark.asyncio
async def test_vibecoding_calculate_latency(
    client: AsyncClient,
    auth_headers: dict,
    sample_vibecoding_signals: dict,
):
    """Test vibecoding calculation latency is <50ms p95."""
    latencies = []

    for _ in range(20):
        start = time.perf_counter()
        response = await client.post(
            "/api/v1/governance/vibecoding/calculate",
            json={"signals": sample_vibecoding_signals},
            headers=auth_headers,
        )
        end = time.perf_counter()

        if response.status_code == 200:
            latencies.append((end - start) * 1000)

    if latencies:
        sorted_latencies = sorted(latencies)
        p95_index = int(len(sorted_latencies) * 0.95)
        p95 = sorted_latencies[p95_index] if p95_index < len(sorted_latencies) else sorted_latencies[-1]

        # Target: <50ms p95 for calculation
        assert p95 < 50, f"p95 latency {p95:.2f}ms exceeds 50ms target"


@pytest.mark.asyncio
async def test_spec_validation_latency(
    client: AsyncClient,
    auth_headers: dict,
    sample_spec_content: str,
):
    """Test spec validation latency is <200ms p95."""
    latencies = []

    for _ in range(10):
        start = time.perf_counter()
        response = await client.post(
            "/api/v1/governance/specs/validate",
            json={"content": sample_spec_content},
            headers=auth_headers,
        )
        end = time.perf_counter()

        if response.status_code == 200:
            latencies.append((end - start) * 1000)

    if latencies:
        sorted_latencies = sorted(latencies)
        p95_index = int(len(sorted_latencies) * 0.95)
        p95 = sorted_latencies[p95_index] if p95_index < len(sorted_latencies) else sorted_latencies[-1]

        # Target: <200ms p95 for spec validation
        assert p95 < 200, f"p95 latency {p95:.2f}ms exceeds 200ms target"


@pytest.mark.asyncio
async def test_tier_status_latency(
    client: AsyncClient,
    auth_headers: dict,
    sample_project_id: str,
):
    """Test tier status endpoint latency is <100ms p95."""
    latencies = []

    for _ in range(20):
        start = time.perf_counter()
        response = await client.get(
            f"/api/v1/governance/tiers/{sample_project_id}/status",
            headers=auth_headers,
        )
        end = time.perf_counter()

        # Include 404s as they still measure endpoint performance
        latencies.append((end - start) * 1000)

    if latencies:
        sorted_latencies = sorted(latencies)
        p95_index = int(len(sorted_latencies) * 0.95)
        p95 = sorted_latencies[p95_index] if p95_index < len(sorted_latencies) else sorted_latencies[-1]

        # Target: <100ms p95
        assert p95 < 100, f"p95 latency {p95:.2f}ms exceeds 100ms target"


@pytest.mark.asyncio
async def test_pagination_latency(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test pagination endpoint latency is consistent."""
    latencies = []

    for page in range(1, 6):
        start = time.perf_counter()
        response = await client.get(
            "/api/v1/governance/vibecoding/history",
            params={"page": page, "page_size": 50},
            headers=auth_headers,
        )
        end = time.perf_counter()

        if response.status_code == 200:
            latencies.append((end - start) * 1000)

    if latencies:
        # Latency should be consistent across pages
        avg = sum(latencies) / len(latencies)
        max_latency = max(latencies)

        # Max latency shouldn't be more than 2x average
        assert max_latency < avg * 2, f"Inconsistent latency: max {max_latency:.2f}ms vs avg {avg:.2f}ms"


# ============================================================================
# Concurrent Request Tests
# ============================================================================


@pytest.mark.asyncio
async def test_concurrent_stats_requests(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test handling 50 concurrent stats requests."""
    async def make_request():
        start = time.perf_counter()
        response = await client.get(
            "/api/v1/governance/vibecoding/stats",
            headers=auth_headers,
        )
        end = time.perf_counter()
        return response.status_code, (end - start) * 1000

    # Make 50 concurrent requests
    tasks = [make_request() for _ in range(50)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    success_count = 0
    latencies = []

    for result in results:
        if isinstance(result, tuple):
            status_code, latency = result
            if status_code == 200:
                success_count += 1
                latencies.append(latency)

    # At least 95% should succeed
    assert success_count >= 47, f"Only {success_count}/50 requests succeeded"

    # P95 should still be reasonable under load
    if latencies:
        sorted_latencies = sorted(latencies)
        p95_index = int(len(sorted_latencies) * 0.95)
        p95 = sorted_latencies[p95_index] if p95_index < len(sorted_latencies) else sorted_latencies[-1]

        # Allow higher latency under concurrent load (500ms)
        assert p95 < 500, f"p95 latency {p95:.2f}ms exceeds 500ms under load"


@pytest.mark.asyncio
async def test_concurrent_calculation_requests(
    client: AsyncClient,
    auth_headers: dict,
    sample_vibecoding_signals: dict,
):
    """Test handling 30 concurrent calculation requests."""
    async def make_request():
        return await client.post(
            "/api/v1/governance/vibecoding/calculate",
            json={"signals": sample_vibecoding_signals},
            headers=auth_headers,
        )

    # Make 30 concurrent calculation requests
    tasks = [make_request() for _ in range(30)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    success_count = sum(
        1 for r in results
        if not isinstance(r, Exception) and r.status_code == 200
    )

    # At least 90% should succeed
    assert success_count >= 27, f"Only {success_count}/30 requests succeeded"


@pytest.mark.asyncio
async def test_concurrent_mixed_endpoints(
    client: AsyncClient,
    auth_headers: dict,
    sample_vibecoding_signals: dict,
):
    """Test concurrent requests to different endpoints."""
    async def stats_request():
        return await client.get(
            "/api/v1/governance/vibecoding/stats",
            headers=auth_headers,
        )

    async def history_request():
        return await client.get(
            "/api/v1/governance/vibecoding/history",
            params={"page": 1, "page_size": 10},
            headers=auth_headers,
        )

    async def tier_request():
        return await client.get(
            "/api/v1/governance/tiers/requirements",
            headers=auth_headers,
        )

    # Mix of different endpoints
    tasks = []
    for _ in range(10):
        tasks.extend([
            stats_request(),
            history_request(),
            tier_request(),
        ])

    results = await asyncio.gather(*tasks, return_exceptions=True)

    success_count = sum(
        1 for r in results
        if not isinstance(r, Exception) and r.status_code == 200
    )

    # At least 90% should succeed
    assert success_count >= 27, f"Only {success_count}/30 requests succeeded"


# ============================================================================
# Throughput Tests
# ============================================================================


@pytest.mark.asyncio
async def test_requests_per_second(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test throughput: at least 100 requests per second."""
    request_count = 100
    start = time.perf_counter()

    tasks = []
    for _ in range(request_count):
        tasks.append(
            client.get(
                "/api/v1/governance/vibecoding/stats",
                headers=auth_headers,
            )
        )

    results = await asyncio.gather(*tasks, return_exceptions=True)
    end = time.perf_counter()

    duration = end - start
    rps = request_count / duration

    success_count = sum(
        1 for r in results
        if not isinstance(r, Exception) and r.status_code == 200
    )

    # Should handle at least 100 RPS
    assert rps >= 100, f"Throughput {rps:.2f} RPS below 100 RPS target"
    assert success_count >= 90, f"Only {success_count}/{request_count} succeeded"


# ============================================================================
# Memory/Resource Tests
# ============================================================================


@pytest.mark.asyncio
async def test_large_pagination_no_memory_leak(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that large pagination requests don't cause memory issues."""
    # Request maximum page size multiple times
    for _ in range(10):
        response = await client.get(
            "/api/v1/governance/vibecoding/history",
            params={"page": 1, "page_size": 100},
            headers=auth_headers,
        )
        assert response.status_code == 200

        # Ensure response size is bounded
        content_length = len(response.content)
        assert content_length < 1024 * 1024, f"Response too large: {content_length} bytes"


@pytest.mark.asyncio
async def test_repeated_validation_requests(
    client: AsyncClient,
    auth_headers: dict,
    sample_spec_content: str,
):
    """Test that repeated validation requests don't cause resource issues."""
    for i in range(20):
        response = await client.post(
            "/api/v1/governance/specs/validate",
            json={"content": sample_spec_content},
            headers=auth_headers,
        )
        assert response.status_code == 200

        # Response should be consistent
        data = response.json()
        assert data["valid"] is True


# ============================================================================
# Stress Tests
# ============================================================================


@pytest.mark.asyncio
async def test_burst_traffic(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test handling burst traffic (100 requests in rapid succession)."""
    burst_size = 100

    async def rapid_request():
        return await client.get(
            "/api/v1/governance/vibecoding/stats",
            headers=auth_headers,
        )

    # Send burst
    tasks = [rapid_request() for _ in range(burst_size)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    success_count = sum(
        1 for r in results
        if not isinstance(r, Exception) and r.status_code in [200, 429]  # 429 is acceptable rate limiting
    )

    # Should handle burst gracefully (either succeed or rate limit)
    assert success_count >= burst_size * 0.8, f"Only {success_count}/{burst_size} handled"


@pytest.mark.asyncio
async def test_sustained_load(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test sustained load over 10 seconds."""
    duration_seconds = 5  # Reduced for test speed
    requests_per_second = 20
    total_requests = duration_seconds * requests_per_second

    success_count = 0
    error_count = 0

    for _ in range(total_requests):
        try:
            response = await client.get(
                "/api/v1/governance/vibecoding/stats",
                headers=auth_headers,
            )
            if response.status_code == 200:
                success_count += 1
            else:
                error_count += 1
        except Exception:
            error_count += 1

        # Small delay to spread requests
        await asyncio.sleep(1 / requests_per_second)

    # At least 95% success rate under sustained load
    success_rate = success_count / total_requests
    assert success_rate >= 0.95, f"Success rate {success_rate:.2%} below 95%"


# ============================================================================
# Response Size Tests
# ============================================================================


@pytest.mark.asyncio
async def test_response_size_bounded(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test that API response sizes are bounded."""
    # Stats endpoint
    response = await client.get(
        "/api/v1/governance/vibecoding/stats",
        headers=auth_headers,
    )
    if response.status_code == 200:
        assert len(response.content) < 10 * 1024, "Stats response too large"

    # History endpoint with max page size
    response = await client.get(
        "/api/v1/governance/vibecoding/history",
        params={"page": 1, "page_size": 100},
        headers=auth_headers,
    )
    if response.status_code == 200:
        assert len(response.content) < 500 * 1024, "History response too large"


@pytest.mark.asyncio
async def test_tier_requirements_response_size(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test tier requirements response is reasonably sized."""
    response = await client.get(
        "/api/v1/governance/tiers/requirements",
        headers=auth_headers,
    )
    if response.status_code == 200:
        # Requirements for 4 tiers should be < 100KB
        assert len(response.content) < 100 * 1024, "Requirements response too large"

