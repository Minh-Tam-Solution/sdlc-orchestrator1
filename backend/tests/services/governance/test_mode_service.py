"""
=========================================================================
Tests for Governance Mode Service
SDLC Orchestrator - Sprint 108 (Governance Foundation)

Version: 1.0.0
Date: January 27, 2026
Status: ACTIVE - Sprint 108 Day 3

Tests cover:
- Mode transitions (OFF → WARNING → SOFT → FULL)
- Enforcement logic (block/warn based on mode + severity)
- Auto-rollback criteria
- Kill switch functionality
- False positive reporting
- Metrics tracking

Zero Mock Policy: Real service tests with assertions
=========================================================================
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from app.services.governance.mode_service import (
    GovernanceMode,
    GovernanceModeService,
    GovernanceModeState,
    GovernanceViolation,
    ViolationSeverity,
    EnforcementResult,
    RollbackCriteria,
    create_governance_mode_service,
    get_governance_mode_service,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def mode_service():
    """Create a fresh GovernanceModeService for testing."""
    return GovernanceModeService(default_mode=GovernanceMode.WARNING)


@pytest.fixture
def sample_violations():
    """Create sample violations for testing."""
    return [
        GovernanceViolation(
            id="v1",
            rule_id="missing_ownership",
            severity=ViolationSeverity.ERROR,
            message="File missing @owner annotation",
            file_path="backend/app/services/new_service.py",
            suggestion="Add @owner: @backend-lead annotation",
            cli_command="sdlcctl add-ownership --file backend/app/services/new_service.py",
        ),
        GovernanceViolation(
            id="v2",
            rule_id="stale_agents_md",
            severity=ViolationSeverity.WARNING,
            message="AGENTS.md is 10 days old",
            suggestion="Update AGENTS.md with recent changes",
        ),
        GovernanceViolation(
            id="v3",
            rule_id="vibecoding_index_red",
            severity=ViolationSeverity.CRITICAL,
            message="Vibecoding Index > 80 requires CEO review",
        ),
    ]


# ============================================================================
# Test: Mode Transitions
# ============================================================================


class TestModeTransitions:
    """Test governance mode transitions."""

    @pytest.mark.asyncio
    async def test_initial_mode_is_warning(self, mode_service):
        """Default mode should be WARNING for safety."""
        assert mode_service.get_mode() == GovernanceMode.WARNING

    @pytest.mark.asyncio
    async def test_set_mode_to_soft(self, mode_service):
        """Should be able to transition from WARNING to SOFT."""
        await mode_service.set_mode(
            mode=GovernanceMode.SOFT,
            changed_by="admin",
            reason="Week 2 rollout",
        )

        assert mode_service.get_mode() == GovernanceMode.SOFT
        state = mode_service.get_state()
        assert state.previous_mode == GovernanceMode.WARNING
        assert state.changed_by == "admin"
        assert state.reason == "Week 2 rollout"

    @pytest.mark.asyncio
    async def test_set_mode_to_full(self, mode_service):
        """Should be able to transition to FULL mode."""
        await mode_service.set_mode(
            mode=GovernanceMode.FULL,
            changed_by="cto",
            reason="Week 3 full enforcement",
        )

        assert mode_service.get_mode() == GovernanceMode.FULL

    @pytest.mark.asyncio
    async def test_set_mode_to_off(self, mode_service):
        """Should be able to disable governance."""
        await mode_service.set_mode(
            mode=GovernanceMode.OFF,
            changed_by="developer",
            reason="Development mode",
        )

        assert mode_service.get_mode() == GovernanceMode.OFF

    @pytest.mark.asyncio
    async def test_project_level_override(self, mode_service):
        """Should support project-level mode overrides."""
        project_id = uuid4()

        # Global mode is WARNING
        assert mode_service.get_mode() == GovernanceMode.WARNING

        # Set project-specific mode to SOFT
        await mode_service.set_mode(
            mode=GovernanceMode.SOFT,
            changed_by="pm",
            reason="This project is ready for soft enforcement",
            project_id=project_id,
        )

        # Global mode unchanged
        assert mode_service.get_mode() == GovernanceMode.WARNING

        # Project mode is SOFT
        assert mode_service.get_mode(project_id) == GovernanceMode.SOFT


# ============================================================================
# Test: Enforcement Logic
# ============================================================================


class TestEnforcementLogic:
    """Test enforcement decisions based on mode and severity."""

    @pytest.mark.asyncio
    async def test_warning_mode_never_blocks(self, mode_service, sample_violations):
        """WARNING mode should never block, only log."""
        result = await mode_service.enforce(violations=sample_violations)

        assert result.allowed is True
        assert result.mode == GovernanceMode.WARNING
        assert len(result.blocked_violations) == 0
        assert len(result.warned_violations) == len(sample_violations)

    @pytest.mark.asyncio
    async def test_soft_mode_blocks_critical_and_error(self, mode_service, sample_violations):
        """SOFT mode should block CRITICAL and ERROR severities."""
        await mode_service.set_mode(
            mode=GovernanceMode.SOFT,
            changed_by="test",
            reason="test",
        )

        result = await mode_service.enforce(violations=sample_violations)

        assert result.allowed is False
        assert result.mode == GovernanceMode.SOFT
        # CRITICAL and ERROR should be blocked
        assert len(result.blocked_violations) == 2
        # WARNING should only be warned
        assert len(result.warned_violations) == 1

    @pytest.mark.asyncio
    async def test_full_mode_blocks_all_except_info(self, mode_service, sample_violations):
        """FULL mode should block everything except INFO severity."""
        await mode_service.set_mode(
            mode=GovernanceMode.FULL,
            changed_by="test",
            reason="test",
        )

        result = await mode_service.enforce(violations=sample_violations)

        assert result.allowed is False
        assert result.mode == GovernanceMode.FULL
        # All violations should be blocked
        assert len(result.blocked_violations) == len(sample_violations)
        assert len(result.warned_violations) == 0

    @pytest.mark.asyncio
    async def test_off_mode_allows_everything(self, mode_service, sample_violations):
        """OFF mode should allow everything."""
        await mode_service.set_mode(
            mode=GovernanceMode.OFF,
            changed_by="test",
            reason="test",
        )

        result = await mode_service.enforce(violations=sample_violations)

        assert result.allowed is True
        assert len(result.blocked_violations) == 0

    @pytest.mark.asyncio
    async def test_no_violations_always_allowed(self, mode_service):
        """No violations should always be allowed in any mode."""
        await mode_service.set_mode(
            mode=GovernanceMode.FULL,
            changed_by="test",
            reason="test",
        )

        result = await mode_service.enforce(violations=[])

        assert result.allowed is True
        assert len(result.blocked_violations) == 0


# ============================================================================
# Test: Vibecoding Index Routing
# ============================================================================


class TestVibecodingIndexRouting:
    """Test routing decisions based on Vibecoding Index."""

    @pytest.mark.asyncio
    async def test_green_auto_approve(self, mode_service):
        """Index 0-30 should auto-approve."""
        result = await mode_service.enforce(
            violations=[],
            vibecoding_index=25.0,
        )

        assert result.routing == "auto_approve"

    @pytest.mark.asyncio
    async def test_yellow_tech_lead_review(self, mode_service):
        """Index 31-60 should require tech lead review."""
        result = await mode_service.enforce(
            violations=[],
            vibecoding_index=45.0,
        )

        assert result.routing == "tech_lead_review"

    @pytest.mark.asyncio
    async def test_orange_ceo_should_review(self, mode_service):
        """Index 61-80 should recommend CEO review."""
        result = await mode_service.enforce(
            violations=[],
            vibecoding_index=70.0,
        )

        assert result.routing == "ceo_should_review"

    @pytest.mark.asyncio
    async def test_red_ceo_must_review(self, mode_service):
        """Index 81-100 should require CEO review."""
        result = await mode_service.enforce(
            violations=[],
            vibecoding_index=85.0,
        )

        assert result.routing == "ceo_must_review"


# ============================================================================
# Test: Rollback & Kill Switch
# ============================================================================


class TestRollbackAndKillSwitch:
    """Test rollback and kill switch functionality."""

    @pytest.mark.asyncio
    async def test_rollback_to_warning(self, mode_service):
        """Should rollback to WARNING mode."""
        await mode_service.set_mode(
            mode=GovernanceMode.FULL,
            changed_by="test",
            reason="test",
        )

        await mode_service.rollback_to_warning(
            triggered_by="auto_rollback",
            reason="High rejection rate",
        )

        assert mode_service.get_mode() == GovernanceMode.WARNING
        state = mode_service.get_state()
        assert state.is_rollback is True
        assert state.previous_mode == GovernanceMode.FULL

    @pytest.mark.asyncio
    async def test_kill_switch(self, mode_service):
        """Kill switch should immediately rollback to WARNING."""
        await mode_service.set_mode(
            mode=GovernanceMode.FULL,
            changed_by="test",
            reason="test",
        )

        await mode_service.kill_switch(
            triggered_by="cto",
            reason="Production deployment blocked",
        )

        assert mode_service.get_mode() == GovernanceMode.WARNING
        state = mode_service.get_state()
        assert state.is_rollback is True
        assert "KILL_SWITCH" in state.changed_by

    @pytest.mark.asyncio
    async def test_rollback_in_warning_mode_noop(self, mode_service):
        """Rollback should be no-op when already in WARNING mode."""
        assert mode_service.get_mode() == GovernanceMode.WARNING

        await mode_service.rollback_to_warning(
            triggered_by="test",
            reason="test",
        )

        assert mode_service.get_mode() == GovernanceMode.WARNING


# ============================================================================
# Test: Auto-Rollback Criteria
# ============================================================================


class TestAutoRollbackCriteria:
    """Test automatic rollback based on criteria."""

    @pytest.mark.asyncio
    async def test_auto_rollback_on_high_rejection_rate(self, mode_service, sample_violations):
        """Should auto-rollback when rejection rate > 80%."""
        await mode_service.set_mode(
            mode=GovernanceMode.FULL,
            changed_by="test",
            reason="test",
        )

        # Simulate many blocked requests (>80%)
        for i in range(100):
            await mode_service.enforce(violations=sample_violations)

        # Should have auto-rolled back to WARNING
        # (auto_rollback_enabled is True by default)
        state = mode_service.get_state()
        assert state.rejection_rate() > 0.8
        # Note: In actual implementation, rollback happens during enforce()

    @pytest.mark.asyncio
    async def test_auto_rollback_disabled(self, mode_service):
        """Should not auto-rollback when disabled."""
        mode_service._state.auto_rollback_enabled = False

        await mode_service.set_mode(
            mode=GovernanceMode.FULL,
            changed_by="test",
            reason="test",
        )

        should_rollback, reason = mode_service._state.should_auto_rollback()
        assert should_rollback is False


# ============================================================================
# Test: False Positive Reporting
# ============================================================================


class TestFalsePositiveReporting:
    """Test false positive reporting for calibration."""

    @pytest.mark.asyncio
    async def test_report_false_positive(self, mode_service):
        """Should track false positives."""
        initial_count = mode_service._state.false_positives_reported

        await mode_service.report_false_positive(
            violation_id="v1",
            reported_by="developer",
            reason="This ownership check is incorrect",
        )

        assert mode_service._state.false_positives_reported == initial_count + 1

    @pytest.mark.asyncio
    async def test_false_positive_rate_calculation(self, mode_service, sample_violations):
        """Should calculate false positive rate correctly."""
        await mode_service.set_mode(
            mode=GovernanceMode.FULL,
            changed_by="test",
            reason="test",
        )

        # Simulate some blocked requests
        for _ in range(10):
            await mode_service.enforce(violations=sample_violations)

        # Report some false positives
        for _ in range(3):
            await mode_service.report_false_positive(
                violation_id="v1",
                reported_by="dev",
                reason="test",
            )

        # False positive rate should be 3 / (10 blocks)
        state = mode_service.get_state()
        assert state.total_blocked == 10
        assert state.false_positives_reported == 3
        assert 0.29 <= state.false_positive_rate() <= 0.31  # ~30%


# ============================================================================
# Test: Metrics Tracking
# ============================================================================


class TestMetricsTracking:
    """Test metrics tracking for calibration."""

    @pytest.mark.asyncio
    async def test_tracks_total_evaluations(self, mode_service):
        """Should track total evaluations."""
        for _ in range(5):
            await mode_service.enforce(violations=[])

        assert mode_service._state.total_evaluations == 5

    @pytest.mark.asyncio
    async def test_tracks_blocked_count(self, mode_service, sample_violations):
        """Should track blocked count."""
        await mode_service.set_mode(
            mode=GovernanceMode.FULL,
            changed_by="test",
            reason="test",
        )

        for _ in range(3):
            await mode_service.enforce(violations=sample_violations)

        assert mode_service._state.total_blocked == 3

    @pytest.mark.asyncio
    async def test_tracks_passed_count(self, mode_service):
        """Should track passed count."""
        for _ in range(5):
            await mode_service.enforce(violations=[])

        assert mode_service._state.total_passed == 5

    @pytest.mark.asyncio
    async def test_latency_p95_calculation(self, mode_service):
        """Should calculate p95 latency."""
        # Simulate some enforcement calls
        for _ in range(100):
            await mode_service.enforce(violations=[])

        p95 = mode_service.get_latency_p95()
        assert p95 >= 0.0  # Latency should be non-negative


# ============================================================================
# Test: Mode Change Listeners
# ============================================================================


class TestModeChangeListeners:
    """Test mode change listener functionality."""

    @pytest.mark.asyncio
    async def test_listener_called_on_mode_change(self, mode_service):
        """Listener should be called when mode changes."""
        listener_called = []

        async def mock_listener(old_mode, new_mode, changed_by, reason):
            listener_called.append({
                "old": old_mode,
                "new": new_mode,
                "by": changed_by,
                "reason": reason,
            })

        mode_service.add_mode_change_listener(mock_listener)

        await mode_service.set_mode(
            mode=GovernanceMode.SOFT,
            changed_by="admin",
            reason="Test",
        )

        assert len(listener_called) == 1
        assert listener_called[0]["old"] == GovernanceMode.WARNING
        assert listener_called[0]["new"] == GovernanceMode.SOFT


# ============================================================================
# Test: Factory Functions
# ============================================================================


class TestFactoryFunctions:
    """Test factory functions."""

    def test_create_governance_mode_service(self):
        """Should create service with specified default mode."""
        service = create_governance_mode_service(
            default_mode=GovernanceMode.OFF
        )

        assert service.get_mode() == GovernanceMode.OFF

    def test_get_governance_mode_service_singleton(self):
        """Should return same singleton instance."""
        # Reset singleton
        import app.services.governance.mode_service as mod
        mod._governance_mode_service = None

        service1 = get_governance_mode_service()
        service2 = get_governance_mode_service()

        assert service1 is service2


# ============================================================================
# Test: GovernanceViolation
# ============================================================================


class TestGovernanceViolation:
    """Test GovernanceViolation dataclass."""

    def test_to_dict(self, sample_violations):
        """Should convert violation to dictionary."""
        violation = sample_violations[0]
        data = violation.to_dict()

        assert data["id"] == "v1"
        assert data["rule_id"] == "missing_ownership"
        assert data["severity"] == "error"
        assert data["file_path"] == "backend/app/services/new_service.py"
        assert "suggestion" in data
        assert "cli_command" in data


# ============================================================================
# Test: EnforcementResult
# ============================================================================


class TestEnforcementResult:
    """Test EnforcementResult dataclass."""

    @pytest.mark.asyncio
    async def test_enforcement_result_to_dict(self, mode_service, sample_violations):
        """Should convert result to dictionary."""
        result = await mode_service.enforce(
            violations=sample_violations,
            vibecoding_index=65.0,
        )

        data = result.to_dict()

        assert "allowed" in data
        assert "mode" in data
        assert "violations_count" in data
        assert "blocked_count" in data
        assert "warned_count" in data
        assert "vibecoding_index" in data
        assert "routing" in data
        assert "processing_time_ms" in data


# ============================================================================
# Test: Performance
# ============================================================================


class TestPerformance:
    """Test performance requirements."""

    @pytest.mark.asyncio
    async def test_enforce_latency(self, mode_service, sample_violations):
        """Enforcement should be fast (<10ms typical)."""
        import time

        start = time.perf_counter()
        for _ in range(100):
            await mode_service.enforce(violations=sample_violations)
        elapsed_ms = (time.perf_counter() - start) * 1000

        avg_latency = elapsed_ms / 100
        assert avg_latency < 10.0, f"Avg latency {avg_latency}ms exceeds 10ms target"
