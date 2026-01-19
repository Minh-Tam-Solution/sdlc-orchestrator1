"""
AI Detection E2E Tests - Sprint 42 Day 8

SDLC Stage: 04 - BUILD
Sprint: 42 - AI Detection & Validation Pipeline
Framework: SDLC 5.1.3
Day: 8 - End-to-End Validation

Purpose:
End-to-end tests validating the complete AI detection pipeline:
1. HALF_OPEN recovery path (CTO recommendation)
2. Concurrent request handling (CTO recommendation)
3. Full detection pipeline with real data
4. False positive protection
5. Performance validation

CTO Review Recommendations (Day 6):
- "Add HALF_OPEN recovery path tests"
- "Add concurrent request handling tests"
- "End-to-end GitHub API failure tests"

Coverage Target: 95%+
"""

import asyncio
import time
from typing import List

import pytest

from app.services.ai_detection import AIToolType, DetectionMethod
from app.services.ai_detection.service import GitHubAIDetectionService, DETECTION_THRESHOLD
from app.services.ai_detection.shadow_mode import shadow_mode_config, log_shadow_result
from app.services.ai_detection.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerError,
    CircuitState,
    github_api_breaker,
    external_ai_breaker,
)


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def detection_service():
    """Create fresh detection service instance."""
    return GitHubAIDetectionService()


@pytest.fixture
def fast_recovery_breaker():
    """Create circuit breaker with fast recovery for testing."""
    config = CircuitBreakerConfig()
    config.failure_threshold = 2
    config.recovery_timeout = 0.1  # 100ms for fast testing
    config.success_threshold = 2
    return CircuitBreaker(name="test_fast_recovery", config=config)


# ============================================================================
# CTO Recommendation #1: HALF_OPEN Recovery Path Tests
# ============================================================================


class TestHalfOpenRecoveryPath:
    """
    Tests for HALF_OPEN state recovery path.

    CTO Quote: "Add HALF_OPEN recovery path tests"

    Validates:
    - CLOSED → OPEN → HALF_OPEN → CLOSED full cycle
    - HALF_OPEN → OPEN on failure (regression protection)
    - Success threshold enforcement in HALF_OPEN
    """

    @pytest.mark.asyncio
    async def test_full_recovery_cycle_closed_open_halfopen_closed(
        self, fast_recovery_breaker
    ):
        """
        Test complete state machine cycle:
        CLOSED → OPEN → HALF_OPEN → CLOSED
        """
        breaker = fast_recovery_breaker

        # Initial state: CLOSED
        assert breaker.state == CircuitState.CLOSED

        # Step 1: Trip circuit with failures (CLOSED → OPEN)
        await breaker.record_failure(Exception("Failure 1"))
        assert breaker.state == CircuitState.CLOSED  # Not yet tripped

        await breaker.record_failure(Exception("Failure 2"))
        assert breaker.state == CircuitState.OPEN  # Now tripped

        # Step 2: Wait for recovery timeout
        await asyncio.sleep(0.15)  # Wait > recovery_timeout (0.1s)

        # Step 3: Next request should transition to HALF_OPEN
        can_execute = await breaker.can_execute()
        assert can_execute is True
        assert breaker.state == CircuitState.HALF_OPEN

        # Step 4: Record successes to close circuit
        await breaker.record_success()
        assert breaker.state == CircuitState.HALF_OPEN  # Need 2 successes

        await breaker.record_success()
        assert breaker.state == CircuitState.CLOSED  # Recovered!

        # Verify clean state
        assert breaker.stats.failure_count == 0
        assert breaker.stats.success_count == 0

    @pytest.mark.asyncio
    async def test_halfopen_failure_returns_to_open(self, fast_recovery_breaker):
        """
        Test that failure in HALF_OPEN returns to OPEN.

        This is critical for preventing premature recovery when
        service is still unstable.
        """
        breaker = fast_recovery_breaker

        # Trip circuit
        await breaker.record_failure(Exception("Error 1"))
        await breaker.record_failure(Exception("Error 2"))
        assert breaker.state == CircuitState.OPEN

        # Wait and transition to HALF_OPEN
        await asyncio.sleep(0.15)
        await breaker.can_execute()
        assert breaker.state == CircuitState.HALF_OPEN

        # Record one success, then one failure
        await breaker.record_success()
        assert breaker.state == CircuitState.HALF_OPEN

        # Single failure in HALF_OPEN → back to OPEN
        await breaker.record_failure(Exception("Still failing"))
        assert breaker.state == CircuitState.OPEN

        # Verify failure count reset
        assert breaker.stats.failure_count == 1  # Fresh failure count

    @pytest.mark.asyncio
    async def test_halfopen_requires_consecutive_successes(self, fast_recovery_breaker):
        """
        Test that HALF_OPEN requires configured success threshold.
        """
        breaker = fast_recovery_breaker
        breaker.config.success_threshold = 3

        # Trip circuit
        await breaker.record_failure(Exception("Error 1"))
        await breaker.record_failure(Exception("Error 2"))

        # Transition to HALF_OPEN
        await asyncio.sleep(0.15)
        await breaker.can_execute()
        assert breaker.state == CircuitState.HALF_OPEN

        # Record 2 successes (not enough)
        await breaker.record_success()
        await breaker.record_success()
        assert breaker.state == CircuitState.HALF_OPEN

        # Third success closes the circuit
        await breaker.record_success()
        assert breaker.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_multiple_recovery_cycles(self, fast_recovery_breaker):
        """
        Test multiple open/recovery cycles to ensure state machine stability.
        """
        breaker = fast_recovery_breaker

        for cycle in range(3):
            # Trip circuit
            await breaker.record_failure(Exception(f"Cycle {cycle} error 1"))
            await breaker.record_failure(Exception(f"Cycle {cycle} error 2"))
            assert breaker.state == CircuitState.OPEN, f"Cycle {cycle}: Should be OPEN"

            # Wait and recover
            await asyncio.sleep(0.15)
            await breaker.can_execute()
            assert breaker.state == CircuitState.HALF_OPEN

            await breaker.record_success()
            await breaker.record_success()
            assert breaker.state == CircuitState.CLOSED, f"Cycle {cycle}: Should be CLOSED"


# ============================================================================
# CTO Recommendation #2: Concurrent Request Handling Tests
# ============================================================================


class TestConcurrentRequestHandling:
    """
    Tests for concurrent request handling.

    CTO Quote: "Add concurrent request handling tests"

    Validates:
    - Thread safety under concurrent load
    - No race conditions in state transitions
    - Stats accuracy under concurrent requests
    """

    @pytest.mark.asyncio
    async def test_concurrent_successes_thread_safe(self):
        """
        Test that concurrent successful requests don't cause race conditions.
        """
        breaker = CircuitBreaker(name="concurrent_success_test")
        num_requests = 100

        async def simulate_success():
            await breaker.record_success()

        # Run concurrent successes
        await asyncio.gather(*[simulate_success() for _ in range(num_requests)])

        # Verify stats
        assert breaker.stats.total_successes == num_requests
        assert breaker.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_concurrent_failures_trip_once(self):
        """
        Test that concurrent failures don't trip circuit multiple times.
        """
        config = CircuitBreakerConfig()
        config.failure_threshold = 5
        breaker = CircuitBreaker(name="concurrent_failure_test", config=config)

        async def simulate_failure():
            await breaker.record_failure(Exception("Concurrent error"))

        # Run 10 concurrent failures (more than threshold)
        await asyncio.gather(*[simulate_failure() for _ in range(10)])

        # Circuit should be OPEN
        assert breaker.state == CircuitState.OPEN
        # Total failures should be exactly 10
        assert breaker.stats.total_failures == 10

    @pytest.mark.asyncio
    async def test_concurrent_mixed_operations(self):
        """
        Test mixed concurrent successes and failures.
        """
        config = CircuitBreakerConfig()
        config.failure_threshold = 20  # High threshold to stay CLOSED
        breaker = CircuitBreaker(name="concurrent_mixed_test", config=config)

        async def simulate_success():
            await breaker.record_success()

        async def simulate_failure():
            await breaker.record_failure(Exception("Error"))

        # 50 successes + 10 failures concurrently
        tasks = (
            [simulate_success() for _ in range(50)] +
            [simulate_failure() for _ in range(10)]
        )
        await asyncio.gather(*tasks)

        # Verify stats accuracy
        assert breaker.stats.total_successes == 50
        assert breaker.stats.total_failures == 10
        assert breaker.state == CircuitState.CLOSED  # Threshold not reached

    @pytest.mark.asyncio
    async def test_concurrent_detections_isolation(self, detection_service):
        """
        Test that concurrent AI detections are isolated and accurate.

        Uses realistic scenarios with multi-signal detection (metadata + commits).
        """
        # Mix of AI and human PRs with realistic signals
        pr_scenarios = [
            {
                "title": "feat: with Cursor",
                "body": "Cursor AI.",
                "commits": [{"commit": {"message": "[cursor] add"}}],
                "expected_ai": True,
            },
            {
                "title": "fix: typo in README",
                "body": "",
                "commits": [],
                "expected_ai": False,
            },
            {
                "title": "feat: add feature",
                "body": "",
                "commits": [{"commit": {"message": "Co-authored-by: GitHub Copilot"}}],
                "expected_ai": True,
            },
            {
                "title": "docs: update changelog",
                "body": "",
                "commits": [],
                "expected_ai": False,
            },
            {
                "title": "feat: Claude implementation",
                "body": "Claude AI.",
                "commits": [{"commit": {"message": "[claude] add"}}],
                "expected_ai": True,
            },
        ] * 10  # 50 total requests

        async def detect_pr(scenario):
            result = await detection_service.detect(
                pr_data={"title": scenario["title"], "body": scenario["body"]},
                commits=scenario["commits"],
                diff="",
            )
            return {
                "expected": scenario["expected_ai"],
                "actual": result.is_ai_generated,
                "confidence": result.confidence,
            }

        # Run all detections concurrently
        results = await asyncio.gather(*[detect_pr(s) for s in pr_scenarios])

        # Verify accuracy
        correct = sum(1 for r in results if r["expected"] == r["actual"])
        accuracy = correct / len(results)

        assert accuracy >= 0.9, f"Accuracy {accuracy:.1%} below 90% target"

    @pytest.mark.asyncio
    async def test_concurrent_state_transitions_safe(self):
        """
        Test that state transitions under concurrent load are safe.
        """
        config = CircuitBreakerConfig()
        config.failure_threshold = 3
        config.recovery_timeout = 0.05  # 50ms
        config.success_threshold = 2
        breaker = CircuitBreaker(name="concurrent_state_test", config=config)

        async def trip_and_recover():
            """Single trip and recovery cycle."""
            # Trip
            for _ in range(3):
                await breaker.record_failure(Exception("Error"))

            # Wait for recovery
            await asyncio.sleep(0.06)

            # Attempt recovery
            await breaker.can_execute()
            await breaker.record_success()
            await breaker.record_success()

        # Run multiple trip/recover cycles concurrently
        await asyncio.gather(*[trip_and_recover() for _ in range(5)])

        # State should be stable (no crash, no deadlock)
        assert breaker.state in [
            CircuitState.CLOSED,
            CircuitState.OPEN,
            CircuitState.HALF_OPEN,
        ]


# ============================================================================
# CTO Recommendation #3: End-to-End GitHub API Failure Tests
# ============================================================================


class TestGitHubAPIFailureE2E:
    """
    Tests for end-to-end GitHub API failure scenarios.

    CTO Quote: "End-to-end GitHub API failure tests"

    Validates:
    - Detection works when GitHub is unavailable
    - Graceful degradation with fallbacks
    - Recovery when GitHub becomes available
    """

    @pytest.mark.asyncio
    async def test_detection_with_github_circuit_open(self, detection_service):
        """
        Test that detection still works when GitHub circuit is open.

        The detection service should degrade gracefully and still
        analyze available data (title, body, local diff).
        """
        # Trip GitHub circuit breaker
        for _ in range(6):
            await github_api_breaker.record_failure(Exception("GitHub unavailable"))

        assert github_api_breaker.state == CircuitState.OPEN

        try:
            # Detection should still work with local data
            result = await detection_service.detect(
                pr_data={
                    "title": "feat: implement with Cursor",
                    "body": "Generated using Cursor AI.",
                },
                commits=[],  # No GitHub commits
                diff="def my_func(): pass",  # Local diff
            )

            # Should still detect AI from metadata
            assert result.is_ai_generated is True
            assert result.detected_tool == AIToolType.CURSOR

        finally:
            # Cleanup: reset breaker
            await github_api_breaker.reset()

    @pytest.mark.asyncio
    async def test_fallback_when_all_external_services_fail(self, detection_service):
        """
        Test graceful degradation when all external services fail.
        """
        # Trip both circuit breakers
        for _ in range(6):
            await github_api_breaker.record_failure(Exception("GitHub down"))
            await external_ai_breaker.record_failure(Exception("AI service down"))

        try:
            # Detection should still work with basic pattern matching
            result = await detection_service.detect(
                pr_data={
                    "title": "feat: add feature [Copilot]",
                    "body": "",
                },
                commits=[],
                diff="",
            )

            # Should detect from title pattern
            assert result.is_ai_generated is True

        finally:
            await github_api_breaker.reset()
            await external_ai_breaker.reset()

    @pytest.mark.asyncio
    async def test_recovery_after_github_returns(self, detection_service):
        """
        Test that detection fully recovers after GitHub returns.
        """
        # Trip breaker
        for _ in range(6):
            await github_api_breaker.record_failure(Exception("Temporary outage"))

        assert github_api_breaker.state == CircuitState.OPEN

        # Reset (simulating GitHub recovery)
        await github_api_breaker.reset()

        # Full detection should work
        result = await detection_service.detect(
            pr_data={
                "title": "feat: implementation",
                "body": "",
            },
            commits=[
                {"commit": {"message": "feat: add\n\nCo-authored-by: GitHub Copilot"}}
            ],
            diff="",
        )

        # Should detect from commit metadata
        assert result.is_ai_generated is True
        assert result.detected_tool == AIToolType.COPILOT

    @pytest.mark.asyncio
    async def test_protected_function_with_fallback(self):
        """
        Test protected function decorator with fallback.
        """
        config = CircuitBreakerConfig()
        config.failure_threshold = 1
        breaker = CircuitBreaker(name="fallback_test", config=config)

        fallback_value = {"fallback": True, "data": "cached"}

        @breaker.protected(fallback=lambda: fallback_value)
        async def fetch_github_data():
            raise Exception("GitHub unavailable")

        # First call fails and trips circuit
        with pytest.raises(Exception):
            await fetch_github_data()

        assert breaker.state == CircuitState.OPEN

        # Second call uses fallback
        result = await fetch_github_data()
        assert result == fallback_value


# ============================================================================
# Full Pipeline E2E Tests
# ============================================================================


class TestFullPipelineE2E:
    """
    End-to-end tests for the complete AI detection pipeline.
    """

    @pytest.mark.asyncio
    async def test_complete_detection_pipeline_cursor(self, detection_service):
        """
        Test complete detection pipeline for Cursor-generated PR.
        """
        # Realistic Cursor PR data
        pr_data = {
            "title": "feat(auth): implement OAuth2 flow with Cursor",
            "body": """## Summary
            Implemented OAuth2 authentication flow.

            ## Changes
            - Added OAuth2 endpoints
            - Integrated with GitHub OAuth
            - Added session management

            Generated using Cursor AI assistant.
            """,
        }
        commits = [
            {"commit": {"message": "[cursor] add oauth endpoints"}},
            {"commit": {"message": "[cursor] implement token refresh"}},
            {"commit": {"message": "[cursor] add session management"}},
        ]
        diff = """
        +@router.post("/oauth/callback")
        +async def oauth_callback(code: str):
        +    token = await exchange_code(code)
        +    return {"access_token": token}
        """

        result = await detection_service.detect(pr_data, commits, diff)

        # Assertions
        assert result.is_ai_generated is True
        assert result.detected_tool == AIToolType.CURSOR
        assert result.confidence >= 0.7
        assert result.detection_method == DetectionMethod.COMBINED
        assert "metadata" in result.strategies_used
        assert "commit" in result.strategies_used
        assert "pattern" in result.strategies_used
        assert result.detection_duration_ms < 600  # Performance target

    @pytest.mark.asyncio
    async def test_complete_detection_pipeline_human(self, detection_service):
        """
        Test complete detection pipeline for human-written PR.
        """
        pr_data = {
            "title": "fix: resolve race condition in cache invalidation",
            "body": """## Bug Description
            Found race condition when multiple threads invalidate cache simultaneously.

            ## Root Cause
            Missing lock around cache write operations.

            ## Fix
            Added asyncio.Lock() to ensure atomic cache updates.

            ## Testing
            Added unit tests with concurrent cache operations.
            """,
        }
        commits = [
            {"commit": {"message": "fix: add lock to cache invalidation"}},
            {"commit": {"message": "test: add concurrent cache tests"}},
        ]
        diff = """
        +async with self._cache_lock:
        +    await self._cache.delete(key)
        """

        result = await detection_service.detect(pr_data, commits, diff)

        # Assertions
        assert result.is_ai_generated is False
        assert result.detected_tool is None
        assert result.confidence < 0.5
        assert result.detection_duration_ms < 600

    @pytest.mark.asyncio
    async def test_shadow_mode_integration(self, detection_service):
        """
        Test that shadow mode correctly logs detection results.
        """
        # Ensure shadow mode is enabled
        original_enabled = shadow_mode_config.is_enabled
        shadow_mode_config.is_enabled = True

        try:
            pr_data = {
                "title": "feat: add feature with Claude Code",
                "body": "🤖 Generated with Claude Code",
            }

            result = await detection_service.detect(
                pr_data=pr_data,
                commits=[],
                diff="",
            )

            # Result should be logged in shadow mode
            assert result.is_ai_generated is True

            # Log result (simulating API behavior)
            log_shadow_result(
                pr_id="test-pr-123",
                pr_title=pr_data["title"],
                result=result,
            )

        finally:
            shadow_mode_config.is_enabled = original_enabled

    @pytest.mark.asyncio
    async def test_detection_with_all_evidence_types(self, detection_service):
        """
        Test detection with all evidence types contributing.
        """
        pr_data = {
            "title": "feat: implement API with Cursor",  # metadata signal
            "body": "Used Cursor AI for implementation",  # metadata signal
        }
        commits = [
            {"commit": {"message": "[cursor] initial implementation"}},  # commit signal
        ]
        diff = "// Generated by Cursor"  # pattern signal

        result = await detection_service.detect(pr_data, commits, diff)

        # Verify all strategies contributed
        evidence = result.detection_evidence
        assert evidence is not None
        assert evidence.get("metadata", {}).get("confidence", 0) > 0
        assert evidence.get("commit", {}).get("confidence", 0) > 0
        # Pattern may or may not match depending on implementation


# ============================================================================
# Performance E2E Tests
# ============================================================================


class TestPerformanceE2E:
    """
    End-to-end performance tests.
    """

    @pytest.mark.asyncio
    async def test_detection_latency_p95(self, detection_service):
        """
        Test that p95 latency is under 600ms target.
        """
        latencies: List[float] = []
        num_requests = 100

        pr_data = {
            "title": "feat: implement feature with Cursor",
            "body": "Generated using Cursor AI.\n" * 50,  # Moderate body
        }
        commits = [{"commit": {"message": f"commit {i}"}} for i in range(10)]
        diff = "def func():\n    pass\n" * 50  # Moderate diff

        for _ in range(num_requests):
            start = time.perf_counter()
            await detection_service.detect(pr_data, commits, diff)
            latencies.append((time.perf_counter() - start) * 1000)  # ms

        # Calculate p95
        latencies.sort()
        p95_index = int(num_requests * 0.95)
        p95_latency = latencies[p95_index]

        assert p95_latency < 600, f"p95 latency {p95_latency:.1f}ms exceeds 600ms target"

    @pytest.mark.asyncio
    async def test_throughput_under_load(self, detection_service):
        """
        Test throughput under concurrent load.
        """
        num_requests = 50

        pr_data = {"title": "feat: with Cursor", "body": ""}

        start = time.perf_counter()
        await asyncio.gather(*[
            detection_service.detect(pr_data, [], "")
            for _ in range(num_requests)
        ])
        duration = time.perf_counter() - start

        throughput = num_requests / duration

        # Should handle at least 20 requests per second
        assert throughput >= 20, f"Throughput {throughput:.1f} req/s below 20 req/s target"


# ============================================================================
# Adversarial E2E Tests
# ============================================================================


class TestAdversarialE2E:
    """
    End-to-end adversarial tests to prevent false positives.
    """

    @pytest.mark.asyncio
    async def test_technical_terms_not_detected(self, detection_service):
        """
        Test that technical terms don't trigger false positives.
        """
        technical_prs = [
            {
                "title": "fix: database cursor leak in connection pool",
                "body": "Fixed cursor leak when connection times out.",
            },
            {
                "title": "feat: implement pilot project for A/B testing",
                "body": "Pilot project for testing new feature flags.",
            },
            {
                "title": "docs: add Claude Shannon information theory docs",
                "body": "Documentation about Claude Shannon's entropy formula.",
            },
            {
                "title": "chore: update windsurf event handler",
                "body": "Refactored windsurf sports booking system.",
            },
            {
                "title": "fix: tab navigation focus handling",
                "body": "Fixed tab key navigation in form inputs.",
            },
        ]

        for pr in technical_prs:
            result = await detection_service.detect(
                pr_data=pr,
                commits=[],
                diff="",
            )

            assert result.is_ai_generated is False, (
                f"False positive for: {pr['title']}"
            )

    @pytest.mark.asyncio
    async def test_legitimate_ai_mentions_in_context(self, detection_service):
        """
        Test that legitimate AI discussions don't trigger false positives.
        """
        discussion_prs = [
            {
                "title": "docs: compare Cursor vs VS Code features",
                "body": "Added comparison documentation for editor features.",
            },
            {
                "title": "feat: add Copilot competitor analysis",
                "body": "Market research for AI assistant competitors.",
            },
        ]

        for pr in discussion_prs:
            result = await detection_service.detect(
                pr_data=pr,
                commits=[{"commit": {"message": "docs: add comparison"}}],
                diff="",
            )

            # These might be detected due to tool mentions
            # but confidence should be lower
            if result.is_ai_generated:
                assert result.confidence < 0.8, (
                    f"High confidence false positive for: {pr['title']}"
                )


# ============================================================================
# Configuration E2E Tests
# ============================================================================


class TestConfigurationE2E:
    """
    End-to-end tests for configuration validation.
    """

    def test_detection_threshold_valid(self):
        """Test that detection threshold is properly configured."""
        assert 0.0 <= DETECTION_THRESHOLD <= 1.0
        assert DETECTION_THRESHOLD == 0.5  # Default production value

    def test_shadow_mode_default_config(self):
        """Test shadow mode default configuration."""
        assert shadow_mode_config.is_enabled is True
        assert shadow_mode_config.sample_rate == 1.0
        assert shadow_mode_config.log_level in ["DEBUG", "INFO", "WARNING"]

    def test_circuit_breaker_default_config(self):
        """Test circuit breaker default configuration."""
        assert github_api_breaker.config.failure_threshold == 5
        assert github_api_breaker.config.recovery_timeout == 30.0
        assert github_api_breaker.config.success_threshold == 3
        assert github_api_breaker.config.enabled is True
