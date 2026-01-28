"""
=========================================================================
GovernanceModeService Unit Tests - Sprint 108 (Governance Foundation)
SDLC Orchestrator - Stage 04 (BUILD)

Version: 1.0.0
Date: January 28, 2026
Status: ACTIVE - Sprint 108 Tests
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
Unit tests for GovernanceModeService - governance enforcement level management
with kill switch capability and auto-rollback.

Test Coverage:
- Mode management (get_mode, set_mode, project overrides)
- Rollback functionality (rollback_to_warning, kill switch)
- Enforcement logic (enforce, _should_block for each mode)
- Metrics tracking (rejection rate, latency p95)
- Auto-rollback triggers (threshold breaches)
- Mode change listeners (sync and async)

Test Categories:
- UT-MODE-001 to UT-MODE-010: Mode Management Tests
- UT-ENFORCE-001 to UT-ENFORCE-015: Enforcement Tests
- UT-ROLLBACK-001 to UT-ROLLBACK-005: Rollback Tests
- UT-METRICS-001 to UT-METRICS-005: Metrics Tests
- UT-LISTENER-001 to UT-LISTENER-003: Listener Tests

Zero Mock Policy: Real enforcement logic, in-memory state only
=========================================================================
"""

import asyncio
import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from unittest.mock import AsyncMock, Mock, patch

from app.services.governance.mode_service import (
    GovernanceMode,
    GovernanceModeService,
    GovernanceModeState,
    GovernanceViolation,
    ViolationSeverity,
    EnforcementResult,
    RollbackCriteria,
)


# =========================================================================
# Fixtures
# =========================================================================


@pytest.fixture
def mode_service() -> GovernanceModeService:
    """Create GovernanceModeService instance for testing."""
    return GovernanceModeService(default_mode=GovernanceMode.WARNING)


@pytest.fixture
def mode_service_off() -> GovernanceModeService:
    """Create GovernanceModeService in OFF mode."""
    return GovernanceModeService(default_mode=GovernanceMode.OFF)


@pytest.fixture
def mode_service_full() -> GovernanceModeService:
    """Create GovernanceModeService in FULL mode."""
    service = GovernanceModeService(default_mode=GovernanceMode.FULL)
    return service


@pytest.fixture
def sample_violation_critical() -> GovernanceViolation:
    """Create a CRITICAL severity violation."""
    return GovernanceViolation(
        id="v-001",
        rule_id="SEC-001",
        severity=ViolationSeverity.CRITICAL,
        message="Security vulnerability detected",
        file_path="backend/app/auth.py",
        line_number=42,
        suggestion="Add input validation",
        cli_command="sdlcctl fix --rule SEC-001",
    )


@pytest.fixture
def sample_violation_error() -> GovernanceViolation:
    """Create an ERROR severity violation."""
    return GovernanceViolation(
        id="v-002",
        rule_id="OWN-001",
        severity=ViolationSeverity.ERROR,
        message="Missing ownership annotation",
        file_path="backend/app/services/user_service.py",
        suggestion="Add @owner header",
    )


@pytest.fixture
def sample_violation_warning() -> GovernanceViolation:
    """Create a WARNING severity violation."""
    return GovernanceViolation(
        id="v-003",
        rule_id="STYLE-001",
        severity=ViolationSeverity.WARNING,
        message="Variable naming inconsistency",
        file_path="backend/app/utils.py",
    )


@pytest.fixture
def sample_violation_info() -> GovernanceViolation:
    """Create an INFO severity violation."""
    return GovernanceViolation(
        id="v-004",
        rule_id="DOC-001",
        severity=ViolationSeverity.INFO,
        message="Consider adding docstring",
        file_path="backend/app/helpers.py",
    )


# =========================================================================
# Mode Management Tests (UT-MODE-001 to UT-MODE-010)
# =========================================================================


class TestModeManagement:
    """Tests for governance mode management functionality."""

    @pytest.mark.asyncio
    async def test_mode_001_default_mode_is_warning(self, mode_service: GovernanceModeService):
        """UT-MODE-001: Service initializes with WARNING mode by default."""
        assert mode_service.get_mode() == GovernanceMode.WARNING

    @pytest.mark.asyncio
    async def test_mode_002_get_state_returns_full_state(self, mode_service: GovernanceModeService):
        """UT-MODE-002: get_state returns complete GovernanceModeState."""
        state = mode_service.get_state()

        assert isinstance(state, GovernanceModeState)
        assert state.current_mode == GovernanceMode.WARNING
        assert state.changed_by == "system"
        assert state.reason == "Initial startup"
        assert isinstance(state.changed_at, datetime)

    @pytest.mark.asyncio
    async def test_mode_003_set_mode_changes_global_mode(self, mode_service: GovernanceModeService):
        """UT-MODE-003: set_mode changes global governance mode."""
        await mode_service.set_mode(
            mode=GovernanceMode.SOFT,
            changed_by="cto@company.com",
            reason="Enable soft enforcement for pilot",
        )

        assert mode_service.get_mode() == GovernanceMode.SOFT
        state = mode_service.get_state()
        assert state.previous_mode == GovernanceMode.WARNING
        assert state.changed_by == "cto@company.com"
        assert "pilot" in state.reason

    @pytest.mark.asyncio
    async def test_mode_004_set_mode_progression(self, mode_service: GovernanceModeService):
        """UT-MODE-004: Mode can progress through all levels."""
        # OFF → WARNING → SOFT → FULL
        await mode_service.set_mode(GovernanceMode.OFF, "test", "testing off")
        assert mode_service.get_mode() == GovernanceMode.OFF

        await mode_service.set_mode(GovernanceMode.WARNING, "test", "testing warning")
        assert mode_service.get_mode() == GovernanceMode.WARNING

        await mode_service.set_mode(GovernanceMode.SOFT, "test", "testing soft")
        assert mode_service.get_mode() == GovernanceMode.SOFT

        await mode_service.set_mode(GovernanceMode.FULL, "test", "testing full")
        assert mode_service.get_mode() == GovernanceMode.FULL

    @pytest.mark.asyncio
    async def test_mode_005_project_override(self, mode_service: GovernanceModeService):
        """UT-MODE-005: Project-level mode override works."""
        project_id = uuid4()

        # Global mode is WARNING
        assert mode_service.get_mode() == GovernanceMode.WARNING

        # Set project override to FULL
        await mode_service.set_mode(
            mode=GovernanceMode.FULL,
            changed_by="pm@company.com",
            reason="High-risk project needs full enforcement",
            project_id=project_id,
        )

        # Project gets FULL, others get WARNING
        assert mode_service.get_mode(project_id) == GovernanceMode.FULL
        assert mode_service.get_mode() == GovernanceMode.WARNING
        assert mode_service.get_mode(uuid4()) == GovernanceMode.WARNING

    @pytest.mark.asyncio
    async def test_mode_006_multiple_project_overrides(self, mode_service: GovernanceModeService):
        """UT-MODE-006: Multiple projects can have different overrides."""
        project_a = uuid4()
        project_b = uuid4()
        project_c = uuid4()

        await mode_service.set_mode(GovernanceMode.FULL, "admin", "high-risk", project_id=project_a)
        await mode_service.set_mode(GovernanceMode.SOFT, "admin", "medium-risk", project_id=project_b)
        # project_c has no override

        assert mode_service.get_mode(project_a) == GovernanceMode.FULL
        assert mode_service.get_mode(project_b) == GovernanceMode.SOFT
        assert mode_service.get_mode(project_c) == GovernanceMode.WARNING  # global default

    @pytest.mark.asyncio
    async def test_mode_007_mode_change_timestamp_updates(self, mode_service: GovernanceModeService):
        """UT-MODE-007: Mode change updates timestamp."""
        initial_time = mode_service.get_state().changed_at

        await asyncio.sleep(0.01)  # Small delay

        await mode_service.set_mode(GovernanceMode.SOFT, "test", "testing")

        new_time = mode_service.get_state().changed_at
        assert new_time > initial_time

    @pytest.mark.asyncio
    async def test_mode_008_initialization_with_off_mode(self, mode_service_off: GovernanceModeService):
        """UT-MODE-008: Service can be initialized with OFF mode."""
        assert mode_service_off.get_mode() == GovernanceMode.OFF

    @pytest.mark.asyncio
    async def test_mode_009_initialization_with_full_mode(self, mode_service_full: GovernanceModeService):
        """UT-MODE-009: Service can be initialized with FULL mode."""
        assert mode_service_full.get_mode() == GovernanceMode.FULL

    @pytest.mark.asyncio
    async def test_mode_010_state_to_dict_serialization(self, mode_service: GovernanceModeService):
        """UT-MODE-010: State can be serialized to dictionary."""
        state = mode_service.get_state()
        state_dict = state.to_dict()

        assert "current_mode" in state_dict
        assert "changed_at" in state_dict
        assert "changed_by" in state_dict
        assert "auto_rollback_enabled" in state_dict
        assert state_dict["current_mode"] == "warning"


# =========================================================================
# Enforcement Tests (UT-ENFORCE-001 to UT-ENFORCE-015)
# =========================================================================


class TestEnforcement:
    """Tests for governance enforcement logic."""

    @pytest.mark.asyncio
    async def test_enforce_001_off_mode_allows_all(
        self,
        mode_service_off: GovernanceModeService,
        sample_violation_critical: GovernanceViolation,
    ):
        """UT-ENFORCE-001: OFF mode allows all violations."""
        result = await mode_service_off.enforce(
            violations=[sample_violation_critical],
        )

        assert result.allowed is True
        assert result.mode == GovernanceMode.OFF
        assert len(result.blocked_violations) == 0
        assert len(result.warned_violations) == 0

    @pytest.mark.asyncio
    async def test_enforce_002_warning_mode_warns_all(
        self,
        mode_service: GovernanceModeService,
        sample_violation_critical: GovernanceViolation,
        sample_violation_error: GovernanceViolation,
    ):
        """UT-ENFORCE-002: WARNING mode warns but doesn't block."""
        result = await mode_service.enforce(
            violations=[sample_violation_critical, sample_violation_error],
        )

        assert result.allowed is True
        assert result.mode == GovernanceMode.WARNING
        assert len(result.blocked_violations) == 0
        assert len(result.warned_violations) == 2

    @pytest.mark.asyncio
    async def test_enforce_003_soft_mode_blocks_critical(
        self,
        mode_service: GovernanceModeService,
        sample_violation_critical: GovernanceViolation,
        sample_violation_warning: GovernanceViolation,
    ):
        """UT-ENFORCE-003: SOFT mode blocks CRITICAL violations."""
        await mode_service.set_mode(GovernanceMode.SOFT, "test", "testing soft")

        result = await mode_service.enforce(
            violations=[sample_violation_critical, sample_violation_warning],
        )

        assert result.allowed is False
        assert len(result.blocked_violations) == 1
        assert result.blocked_violations[0].severity == ViolationSeverity.CRITICAL
        assert len(result.warned_violations) == 1

    @pytest.mark.asyncio
    async def test_enforce_004_soft_mode_blocks_error(
        self,
        mode_service: GovernanceModeService,
        sample_violation_error: GovernanceViolation,
    ):
        """UT-ENFORCE-004: SOFT mode blocks ERROR violations."""
        await mode_service.set_mode(GovernanceMode.SOFT, "test", "testing soft")

        result = await mode_service.enforce(violations=[sample_violation_error])

        assert result.allowed is False
        assert len(result.blocked_violations) == 1
        assert result.blocked_violations[0].severity == ViolationSeverity.ERROR

    @pytest.mark.asyncio
    async def test_enforce_005_soft_mode_warns_warning(
        self,
        mode_service: GovernanceModeService,
        sample_violation_warning: GovernanceViolation,
    ):
        """UT-ENFORCE-005: SOFT mode only warns on WARNING severity."""
        await mode_service.set_mode(GovernanceMode.SOFT, "test", "testing soft")

        result = await mode_service.enforce(violations=[sample_violation_warning])

        assert result.allowed is True
        assert len(result.blocked_violations) == 0
        assert len(result.warned_violations) == 1

    @pytest.mark.asyncio
    async def test_enforce_006_full_mode_blocks_warning(
        self,
        mode_service: GovernanceModeService,
        sample_violation_warning: GovernanceViolation,
    ):
        """UT-ENFORCE-006: FULL mode blocks WARNING violations."""
        await mode_service.set_mode(GovernanceMode.FULL, "test", "testing full")

        result = await mode_service.enforce(violations=[sample_violation_warning])

        assert result.allowed is False
        assert len(result.blocked_violations) == 1

    @pytest.mark.asyncio
    async def test_enforce_007_full_mode_allows_info_only(
        self,
        mode_service: GovernanceModeService,
        sample_violation_info: GovernanceViolation,
    ):
        """UT-ENFORCE-007: FULL mode allows INFO (does not block)."""
        await mode_service.set_mode(GovernanceMode.FULL, "test", "testing full")

        result = await mode_service.enforce(violations=[sample_violation_info])

        assert result.allowed is True
        assert len(result.blocked_violations) == 0

    @pytest.mark.asyncio
    async def test_enforce_008_empty_violations_allowed(self, mode_service: GovernanceModeService):
        """UT-ENFORCE-008: No violations means allowed."""
        await mode_service.set_mode(GovernanceMode.FULL, "test", "testing full")

        result = await mode_service.enforce(violations=[])

        assert result.allowed is True
        assert len(result.violations) == 0

    @pytest.mark.asyncio
    async def test_enforce_009_vibecoding_index_routing_green(
        self, mode_service: GovernanceModeService
    ):
        """UT-ENFORCE-009: Vibecoding Index < 30 routes to auto_approve."""
        result = await mode_service.enforce(violations=[], vibecoding_index=25.0)

        assert result.vibecoding_index == 25.0
        assert result.routing == "auto_approve"

    @pytest.mark.asyncio
    async def test_enforce_010_vibecoding_index_routing_yellow(
        self, mode_service: GovernanceModeService
    ):
        """UT-ENFORCE-010: Vibecoding Index 31-60 routes to tech_lead_review."""
        result = await mode_service.enforce(violations=[], vibecoding_index=45.0)

        assert result.routing == "tech_lead_review"

    @pytest.mark.asyncio
    async def test_enforce_011_vibecoding_index_routing_orange(
        self, mode_service: GovernanceModeService
    ):
        """UT-ENFORCE-011: Vibecoding Index 61-80 routes to ceo_should_review."""
        result = await mode_service.enforce(violations=[], vibecoding_index=72.0)

        assert result.routing == "ceo_should_review"

    @pytest.mark.asyncio
    async def test_enforce_012_vibecoding_index_routing_red(
        self, mode_service: GovernanceModeService
    ):
        """UT-ENFORCE-012: Vibecoding Index > 80 routes to ceo_must_review."""
        result = await mode_service.enforce(violations=[], vibecoding_index=85.0)

        assert result.routing == "ceo_must_review"

    @pytest.mark.asyncio
    async def test_enforce_013_processing_time_tracked(self, mode_service: GovernanceModeService):
        """UT-ENFORCE-013: Processing time is tracked in result."""
        result = await mode_service.enforce(violations=[])

        assert result.processing_time_ms >= 0
        assert result.processing_time_ms < 100  # Should be fast

    @pytest.mark.asyncio
    async def test_enforce_014_result_to_dict(
        self,
        mode_service: GovernanceModeService,
        sample_violation_warning: GovernanceViolation,
    ):
        """UT-ENFORCE-014: EnforcementResult can be serialized to dict."""
        result = await mode_service.enforce(
            violations=[sample_violation_warning],
            vibecoding_index=50.0,
        )

        result_dict = result.to_dict()

        assert "allowed" in result_dict
        assert "mode" in result_dict
        assert "violations_count" in result_dict
        assert "blocked_count" in result_dict
        assert "warned_count" in result_dict
        assert "processing_time_ms" in result_dict

    @pytest.mark.asyncio
    async def test_enforce_015_project_override_enforcement(
        self,
        mode_service: GovernanceModeService,
        sample_violation_warning: GovernanceViolation,
    ):
        """UT-ENFORCE-015: Project override affects enforcement."""
        project_id = uuid4()

        # Global is WARNING, project is FULL
        await mode_service.set_mode(GovernanceMode.FULL, "admin", "project needs full", project_id=project_id)

        # Global enforcement (WARNING) - allows warning violations
        global_result = await mode_service.enforce(
            violations=[sample_violation_warning],
        )
        assert global_result.allowed is True

        # Project enforcement (FULL) - blocks warning violations
        project_result = await mode_service.enforce(
            violations=[sample_violation_warning],
            project_id=project_id,
        )
        assert project_result.allowed is False


# =========================================================================
# Rollback Tests (UT-ROLLBACK-001 to UT-ROLLBACK-005)
# =========================================================================


class TestRollback:
    """Tests for rollback functionality and kill switch."""

    @pytest.mark.asyncio
    async def test_rollback_001_rollback_from_full_to_warning(
        self, mode_service: GovernanceModeService
    ):
        """UT-ROLLBACK-001: Can rollback from FULL to WARNING."""
        await mode_service.set_mode(GovernanceMode.FULL, "admin", "enable full")
        assert mode_service.get_mode() == GovernanceMode.FULL

        await mode_service.rollback_to_warning("kill_switch", "Rejection rate exceeded 80%")

        state = mode_service.get_state()
        assert state.current_mode == GovernanceMode.WARNING
        assert state.previous_mode == GovernanceMode.FULL
        assert state.is_rollback is True
        assert "ROLLBACK" in state.reason

    @pytest.mark.asyncio
    async def test_rollback_002_rollback_from_soft_to_warning(
        self, mode_service: GovernanceModeService
    ):
        """UT-ROLLBACK-002: Can rollback from SOFT to WARNING."""
        await mode_service.set_mode(GovernanceMode.SOFT, "admin", "enable soft")

        await mode_service.rollback_to_warning("auto_rollback", "P95 latency exceeded 500ms")

        assert mode_service.get_mode() == GovernanceMode.WARNING
        state = mode_service.get_state()
        assert state.previous_mode == GovernanceMode.SOFT

    @pytest.mark.asyncio
    async def test_rollback_003_rollback_when_already_warning(
        self, mode_service: GovernanceModeService
    ):
        """UT-ROLLBACK-003: Rollback when already WARNING does nothing."""
        assert mode_service.get_mode() == GovernanceMode.WARNING
        initial_state = mode_service.get_state()

        await mode_service.rollback_to_warning("test", "Testing rollback")

        # Should still be WARNING, state unchanged
        assert mode_service.get_mode() == GovernanceMode.WARNING
        assert mode_service.get_state().previous_mode == initial_state.previous_mode

    @pytest.mark.asyncio
    async def test_rollback_004_rollback_from_off_to_warning(
        self, mode_service_off: GovernanceModeService
    ):
        """UT-ROLLBACK-004: Can rollback from OFF to WARNING."""
        assert mode_service_off.get_mode() == GovernanceMode.OFF

        await mode_service_off.rollback_to_warning("admin", "Enable monitoring")

        assert mode_service_off.get_mode() == GovernanceMode.WARNING

    @pytest.mark.asyncio
    async def test_rollback_005_rollback_preserves_triggered_by(
        self, mode_service: GovernanceModeService
    ):
        """UT-ROLLBACK-005: Rollback preserves who triggered it."""
        await mode_service.set_mode(GovernanceMode.FULL, "admin", "enable full")

        await mode_service.rollback_to_warning("cto@company.com", "Manual kill switch")

        state = mode_service.get_state()
        assert state.changed_by == "cto@company.com"


# =========================================================================
# Metrics Tests (UT-METRICS-001 to UT-METRICS-005)
# =========================================================================


class TestMetrics:
    """Tests for metrics tracking functionality."""

    @pytest.mark.asyncio
    async def test_metrics_001_initial_metrics_zero(self, mode_service: GovernanceModeService):
        """UT-METRICS-001: Initial metrics are zero."""
        state = mode_service.get_state()

        assert state.total_evaluations == 0
        assert state.total_rejections == 0
        assert state.rejection_rate() == 0.0

    @pytest.mark.asyncio
    async def test_metrics_002_rejection_count_increases(
        self,
        mode_service: GovernanceModeService,
        sample_violation_critical: GovernanceViolation,
    ):
        """UT-METRICS-002: Rejection count increases after blocked enforcement."""
        await mode_service.set_mode(GovernanceMode.SOFT, "test", "testing")

        # First enforcement - blocked
        await mode_service.enforce(violations=[sample_violation_critical])

        state = mode_service.get_state()
        assert state.total_evaluations == 1
        assert state.total_rejections == 1

    @pytest.mark.asyncio
    async def test_metrics_003_allowed_doesnt_increase_rejection(
        self, mode_service: GovernanceModeService
    ):
        """UT-METRICS-003: Allowed enforcement doesn't increase rejection count."""
        await mode_service.set_mode(GovernanceMode.SOFT, "test", "testing")

        # Enforcement with no violations
        await mode_service.enforce(violations=[])

        state = mode_service.get_state()
        assert state.total_evaluations == 1
        assert state.total_rejections == 0

    @pytest.mark.asyncio
    async def test_metrics_004_rejection_rate_calculation(
        self,
        mode_service: GovernanceModeService,
        sample_violation_critical: GovernanceViolation,
    ):
        """UT-METRICS-004: Rejection rate is calculated correctly."""
        await mode_service.set_mode(GovernanceMode.SOFT, "test", "testing")

        # 2 rejections, 2 approvals
        await mode_service.enforce(violations=[sample_violation_critical])
        await mode_service.enforce(violations=[])
        await mode_service.enforce(violations=[sample_violation_critical])
        await mode_service.enforce(violations=[])

        state = mode_service.get_state()
        assert state.total_evaluations == 4
        assert state.total_rejections == 2
        assert state.rejection_rate() == 0.5  # 50%

    @pytest.mark.asyncio
    async def test_metrics_005_latency_p95_calculation(
        self, mode_service: GovernanceModeService
    ):
        """UT-METRICS-005: Latency P95 is calculated from measurements."""
        # Run multiple enforcements
        for _ in range(10):
            await mode_service.enforce(violations=[])

        state = mode_service.get_state()
        # Should have some latency measurements
        assert state.latency_p95_ms >= 0


# =========================================================================
# Listener Tests (UT-LISTENER-001 to UT-LISTENER-003)
# =========================================================================


class TestModeChangeListeners:
    """Tests for mode change listener functionality."""

    @pytest.mark.asyncio
    async def test_listener_001_sync_listener_called(self, mode_service: GovernanceModeService):
        """UT-LISTENER-001: Sync listener is called on mode change."""
        listener_called = []

        def on_mode_change(old_mode, new_mode, changed_by, reason):
            listener_called.append((old_mode, new_mode, changed_by, reason))

        mode_service.add_mode_change_listener(on_mode_change)

        await mode_service.set_mode(GovernanceMode.SOFT, "test", "testing listener")

        assert len(listener_called) == 1
        old, new, by, reason = listener_called[0]
        assert old == GovernanceMode.WARNING
        assert new == GovernanceMode.SOFT
        assert by == "test"

    @pytest.mark.asyncio
    async def test_listener_002_async_listener_called(self, mode_service: GovernanceModeService):
        """UT-LISTENER-002: Async listener is called on mode change."""
        listener_called = []

        async def on_mode_change_async(old_mode, new_mode, changed_by, reason):
            await asyncio.sleep(0.001)  # Simulate async work
            listener_called.append((old_mode, new_mode, changed_by, reason))

        mode_service.add_mode_change_listener(on_mode_change_async)

        await mode_service.set_mode(GovernanceMode.FULL, "test", "testing async")

        assert len(listener_called) == 1

    @pytest.mark.asyncio
    async def test_listener_003_multiple_listeners(self, mode_service: GovernanceModeService):
        """UT-LISTENER-003: Multiple listeners all receive notification."""
        calls_1 = []
        calls_2 = []

        def listener_1(old, new, by, reason):
            calls_1.append(new)

        def listener_2(old, new, by, reason):
            calls_2.append(new)

        mode_service.add_mode_change_listener(listener_1)
        mode_service.add_mode_change_listener(listener_2)

        await mode_service.set_mode(GovernanceMode.SOFT, "test", "testing")

        assert len(calls_1) == 1
        assert len(calls_2) == 1
        assert calls_1[0] == GovernanceMode.SOFT
        assert calls_2[0] == GovernanceMode.SOFT


# =========================================================================
# Violation Tests (Supporting Data Structures)
# =========================================================================


class TestViolationDataStructures:
    """Tests for GovernanceViolation and related data structures."""

    def test_violation_to_dict(self, sample_violation_critical: GovernanceViolation):
        """Violation can be serialized to dictionary."""
        v_dict = sample_violation_critical.to_dict()

        assert v_dict["id"] == "v-001"
        assert v_dict["rule_id"] == "SEC-001"
        assert v_dict["severity"] == "critical"
        assert v_dict["message"] == "Security vulnerability detected"
        assert v_dict["file_path"] == "backend/app/auth.py"
        assert v_dict["line_number"] == 42
        assert v_dict["suggestion"] == "Add input validation"
        assert v_dict["cli_command"] == "sdlcctl fix --rule SEC-001"

    def test_violation_optional_fields(self):
        """Violation works with minimal required fields."""
        v = GovernanceViolation(
            id="v-min",
            rule_id="TEST",
            severity=ViolationSeverity.INFO,
            message="Test message",
        )

        v_dict = v.to_dict()
        assert v_dict["file_path"] is None
        assert v_dict["line_number"] is None
        assert v_dict["auto_fixable"] is False

    def test_rollback_criteria_defaults(self):
        """RollbackCriteria has sensible defaults."""
        criteria = RollbackCriteria()

        assert criteria.max_rejection_rate == 0.8  # 80%
        assert criteria.max_latency_p95_ms == 500.0
        assert criteria.max_false_positive_rate == 0.2  # 20%
        assert criteria.max_developer_complaints_per_day == 5
        assert criteria.evaluation_window_minutes == 60


# =========================================================================
# Integration Scenarios
# =========================================================================


class TestIntegrationScenarios:
    """Integration scenarios combining multiple features."""

    @pytest.mark.asyncio
    async def test_scenario_gradual_rollout(self, mode_service: GovernanceModeService):
        """
        Scenario: Gradual rollout from WARNING to FULL.

        Week 1: WARNING (observe violations)
        Week 2: SOFT (block critical only)
        Week 3: FULL (block all)
        """
        # Week 1: WARNING mode
        assert mode_service.get_mode() == GovernanceMode.WARNING

        # Simulate violations in WARNING mode
        v_critical = GovernanceViolation(
            id="v1", rule_id="SEC-001", severity=ViolationSeverity.CRITICAL, message="Security issue"
        )
        result = await mode_service.enforce(violations=[v_critical])
        assert result.allowed is True  # WARNING doesn't block

        # Week 2: Upgrade to SOFT
        await mode_service.set_mode(GovernanceMode.SOFT, "cto", "Week 2 - enable soft enforcement")
        result = await mode_service.enforce(violations=[v_critical])
        assert result.allowed is False  # SOFT blocks critical

        # Week 3: Upgrade to FULL
        await mode_service.set_mode(GovernanceMode.FULL, "cto", "Week 3 - full enforcement")
        v_warning = GovernanceViolation(
            id="v2", rule_id="STYLE-001", severity=ViolationSeverity.WARNING, message="Style issue"
        )
        result = await mode_service.enforce(violations=[v_warning])
        assert result.allowed is False  # FULL blocks warnings too

    @pytest.mark.asyncio
    async def test_scenario_kill_switch_activation(self, mode_service: GovernanceModeService):
        """
        Scenario: Kill switch activates when rejection rate too high.

        1. Enable FULL mode
        2. High rejection rate triggers rollback
        3. System returns to WARNING mode
        """
        await mode_service.set_mode(GovernanceMode.FULL, "cto", "Enable full")

        # Simulate many rejections
        v_warning = GovernanceViolation(
            id="v1", rule_id="STYLE-001", severity=ViolationSeverity.WARNING, message="Style issue"
        )

        # 10 rejections in a row
        for _ in range(10):
            await mode_service.enforce(violations=[v_warning])

        # Manual kill switch trigger
        await mode_service.rollback_to_warning("kill_switch", "High rejection rate")

        assert mode_service.get_mode() == GovernanceMode.WARNING
        assert mode_service.get_state().is_rollback is True

    @pytest.mark.asyncio
    async def test_scenario_project_specific_enforcement(
        self, mode_service: GovernanceModeService
    ):
        """
        Scenario: Different projects have different enforcement levels.

        - Pilot project: FULL enforcement
        - Legacy project: WARNING only
        - New project: SOFT enforcement
        """
        pilot_project = uuid4()
        legacy_project = uuid4()
        new_project = uuid4()

        # Set up project-specific modes
        await mode_service.set_mode(GovernanceMode.FULL, "admin", "Pilot - full", project_id=pilot_project)
        # legacy_project uses global default (WARNING)
        await mode_service.set_mode(GovernanceMode.SOFT, "admin", "New - soft", project_id=new_project)

        v_warning = GovernanceViolation(
            id="v1", rule_id="STYLE-001", severity=ViolationSeverity.WARNING, message="Style issue"
        )

        # Pilot: FULL mode blocks warning
        result = await mode_service.enforce(violations=[v_warning], project_id=pilot_project)
        assert result.allowed is False

        # Legacy: WARNING mode allows all
        result = await mode_service.enforce(violations=[v_warning], project_id=legacy_project)
        assert result.allowed is True

        # New: SOFT mode allows warning
        result = await mode_service.enforce(violations=[v_warning], project_id=new_project)
        assert result.allowed is True
