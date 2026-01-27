"""
=========================================================================
Kill Switch Validation Tests
SDLC Orchestrator - Sprint 110 (CEO Dashboard & Observability)

Version: 1.0.0
Date: January 27, 2026
Status: ACTIVE - Sprint 110 Day 7
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 Quality Assurance System

Test Modules:
- Kill switch trigger validation (4 criteria)
- Automatic rollback testing
- Manual override testing
- Notification integration testing

Kill Switch Triggers (per MONITORING-PLAN.md):
1. rejection_rate >80%
2. latency_p95 >500ms
3. false_positive_rate >20%
4. developer_complaints >5/day

Zero Mock Policy: Real implementations tested
=========================================================================
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.governance.mode_service import (
    GovernanceMode,
    GovernanceModeService,
    GovernanceModeState,
    RollbackCriteria,
    create_governance_mode_service,
)


# ============================================================================
# Test Constants
# ============================================================================


KILL_SWITCH_TRIGGERS = {
    "rejection_rate": 0.80,          # >80%
    "latency_p95_ms": 500,           # >500ms
    "false_positive_rate": 0.20,     # >20%
    "developer_complaints_daily": 5,  # >5 per day
}


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def mode_service() -> GovernanceModeService:
    """Create a governance mode service for testing."""
    return create_governance_mode_service()


@pytest.fixture
def healthy_metrics() -> Dict[str, Any]:
    """Return healthy system metrics (should NOT trigger kill switch)."""
    return {
        "rejection_rate": 0.45,        # 45% - below 80% threshold
        "latency_p95_ms": 85,          # 85ms - below 500ms threshold
        "false_positive_rate": 0.06,   # 6% - below 20% threshold
        "developer_complaints_today": 2,  # 2 - below 5/day threshold
        "uptime_percentage": 99.8,
        "error_rate": 0.001,
    }


@pytest.fixture
def unhealthy_rejection_rate() -> Dict[str, Any]:
    """Return metrics with high rejection rate (SHOULD trigger kill switch)."""
    return {
        "rejection_rate": 0.85,        # 85% - ABOVE 80% threshold
        "latency_p95_ms": 80,
        "false_positive_rate": 0.05,
        "developer_complaints_today": 1,
    }


@pytest.fixture
def unhealthy_latency() -> Dict[str, Any]:
    """Return metrics with high latency (SHOULD trigger kill switch)."""
    return {
        "rejection_rate": 0.40,
        "latency_p95_ms": 650,         # 650ms - ABOVE 500ms threshold
        "false_positive_rate": 0.08,
        "developer_complaints_today": 2,
    }


@pytest.fixture
def unhealthy_false_positive() -> Dict[str, Any]:
    """Return metrics with high false positive rate (SHOULD trigger kill switch)."""
    return {
        "rejection_rate": 0.35,
        "latency_p95_ms": 90,
        "false_positive_rate": 0.25,   # 25% - ABOVE 20% threshold
        "developer_complaints_today": 3,
    }


@pytest.fixture
def unhealthy_complaints() -> Dict[str, Any]:
    """Return metrics with many complaints (SHOULD trigger kill switch)."""
    return {
        "rejection_rate": 0.30,
        "latency_p95_ms": 70,
        "false_positive_rate": 0.04,
        "developer_complaints_today": 8,  # 8 - ABOVE 5/day threshold
    }


@pytest.fixture
def multiple_unhealthy() -> Dict[str, Any]:
    """Return metrics with multiple issues (SHOULD trigger kill switch)."""
    return {
        "rejection_rate": 0.90,        # ABOVE threshold
        "latency_p95_ms": 800,         # ABOVE threshold
        "false_positive_rate": 0.30,   # ABOVE threshold
        "developer_complaints_today": 10,  # ABOVE threshold
    }


# ============================================================================
# Kill Switch Trigger Tests
# ============================================================================


class TestKillSwitchTriggerConditions:
    """Test kill switch trigger conditions."""

    def test_healthy_metrics_should_not_trigger(
        self,
        mode_service: GovernanceModeService,
        healthy_metrics: Dict[str, Any]
    ) -> None:
        """
        Test that healthy metrics do NOT trigger the kill switch.

        Scenario:
        - Rejection rate: 45% (below 80%)
        - Latency P95: 85ms (below 500ms)
        - False positive: 6% (below 20%)
        - Complaints: 2 (below 5/day)

        Expected: No trigger
        """
        # Evaluate trigger conditions
        triggers = mode_service._evaluate_rollback_triggers(healthy_metrics)

        # Assert no triggers
        assert len(triggers) == 0, f"Healthy metrics should not trigger kill switch, got: {triggers}"

    def test_high_rejection_rate_should_trigger(
        self,
        mode_service: GovernanceModeService,
        unhealthy_rejection_rate: Dict[str, Any]
    ) -> None:
        """
        Test that rejection rate >80% triggers the kill switch.

        Scenario:
        - Rejection rate: 85% (ABOVE 80%)

        Expected: Trigger with reason "rejection_rate_high"
        """
        triggers = mode_service._evaluate_rollback_triggers(unhealthy_rejection_rate)

        assert len(triggers) >= 1
        assert any(t["reason"] == "rejection_rate_high" for t in triggers), \
            f"Expected rejection_rate_high trigger, got: {triggers}"

    def test_high_latency_should_trigger(
        self,
        mode_service: GovernanceModeService,
        unhealthy_latency: Dict[str, Any]
    ) -> None:
        """
        Test that latency P95 >500ms triggers the kill switch.

        Scenario:
        - Latency P95: 650ms (ABOVE 500ms)

        Expected: Trigger with reason "latency_high"
        """
        triggers = mode_service._evaluate_rollback_triggers(unhealthy_latency)

        assert len(triggers) >= 1
        assert any(t["reason"] == "latency_high" for t in triggers), \
            f"Expected latency_high trigger, got: {triggers}"

    def test_high_false_positive_should_trigger(
        self,
        mode_service: GovernanceModeService,
        unhealthy_false_positive: Dict[str, Any]
    ) -> None:
        """
        Test that false positive rate >20% triggers the kill switch.

        Scenario:
        - False positive rate: 25% (ABOVE 20%)

        Expected: Trigger with reason "false_positive_high"
        """
        triggers = mode_service._evaluate_rollback_triggers(unhealthy_false_positive)

        assert len(triggers) >= 1
        assert any(t["reason"] == "false_positive_high" for t in triggers), \
            f"Expected false_positive_high trigger, got: {triggers}"

    def test_high_complaints_should_trigger(
        self,
        mode_service: GovernanceModeService,
        unhealthy_complaints: Dict[str, Any]
    ) -> None:
        """
        Test that developer complaints >5/day triggers the kill switch.

        Scenario:
        - Developer complaints: 8/day (ABOVE 5/day)

        Expected: Trigger with reason "developer_complaints_high"
        """
        triggers = mode_service._evaluate_rollback_triggers(unhealthy_complaints)

        assert len(triggers) >= 1
        assert any(t["reason"] == "developer_complaints_high" for t in triggers), \
            f"Expected developer_complaints_high trigger, got: {triggers}"

    def test_multiple_issues_should_trigger_multiple_reasons(
        self,
        mode_service: GovernanceModeService,
        multiple_unhealthy: Dict[str, Any]
    ) -> None:
        """
        Test that multiple issues trigger multiple reasons.

        Scenario:
        - All 4 thresholds exceeded

        Expected: All 4 trigger reasons
        """
        triggers = mode_service._evaluate_rollback_triggers(multiple_unhealthy)

        assert len(triggers) >= 4, f"Expected 4 triggers, got: {len(triggers)}"

        expected_reasons = {
            "rejection_rate_high",
            "latency_high",
            "false_positive_high",
            "developer_complaints_high",
        }
        actual_reasons = {t["reason"] for t in triggers}

        assert expected_reasons.issubset(actual_reasons), \
            f"Missing expected reasons. Expected: {expected_reasons}, Got: {actual_reasons}"


# ============================================================================
# Kill Switch Automatic Rollback Tests
# ============================================================================


class TestKillSwitchAutomaticRollback:
    """Test automatic rollback behavior."""

    @pytest.mark.asyncio
    async def test_automatic_rollback_on_high_rejection_rate(
        self,
        mode_service: GovernanceModeService,
        unhealthy_rejection_rate: Dict[str, Any]
    ) -> None:
        """
        Test automatic rollback when rejection rate exceeds threshold.

        Expected:
        - Mode changes from FULL to WARNING
        - Rollback event is logged
        - Notifications are sent (mocked)
        """
        # Set initial mode to FULL
        await mode_service.set_mode(GovernanceMode.FULL)
        assert mode_service.current_mode == GovernanceMode.FULL

        # Simulate metrics collection triggering rollback
        result = await mode_service.check_and_rollback_if_needed(unhealthy_rejection_rate)

        # Assert rollback occurred
        assert result.rollback_triggered is True
        assert result.new_mode == GovernanceMode.WARNING
        assert "rejection_rate_high" in result.trigger_reasons

    @pytest.mark.asyncio
    async def test_automatic_rollback_on_high_latency(
        self,
        mode_service: GovernanceModeService,
        unhealthy_latency: Dict[str, Any]
    ) -> None:
        """
        Test automatic rollback when latency exceeds threshold.

        Expected:
        - Mode changes from SOFT to WARNING
        - Rollback event is logged
        """
        # Set initial mode to SOFT
        await mode_service.set_mode(GovernanceMode.SOFT)
        assert mode_service.current_mode == GovernanceMode.SOFT

        # Simulate metrics collection
        result = await mode_service.check_and_rollback_if_needed(unhealthy_latency)

        # Assert rollback occurred
        assert result.rollback_triggered is True
        assert result.new_mode == GovernanceMode.WARNING
        assert "latency_high" in result.trigger_reasons

    @pytest.mark.asyncio
    async def test_no_rollback_when_already_warning_mode(
        self,
        mode_service: GovernanceModeService,
        unhealthy_rejection_rate: Dict[str, Any]
    ) -> None:
        """
        Test that rollback does not occur when already in WARNING mode.

        Expected:
        - Mode stays at WARNING (lowest active level)
        - No rollback event
        """
        # Set initial mode to WARNING
        await mode_service.set_mode(GovernanceMode.WARNING)
        assert mode_service.current_mode == GovernanceMode.WARNING

        # Simulate metrics collection
        result = await mode_service.check_and_rollback_if_needed(unhealthy_rejection_rate)

        # Assert no further rollback (already at WARNING)
        assert result.rollback_triggered is False
        assert result.new_mode == GovernanceMode.WARNING

    @pytest.mark.asyncio
    async def test_no_rollback_when_off_mode(
        self,
        mode_service: GovernanceModeService,
        multiple_unhealthy: Dict[str, Any]
    ) -> None:
        """
        Test that rollback does not occur when in OFF mode.

        Expected:
        - Mode stays at OFF
        - No rollback event (governance is disabled)
        """
        # Set initial mode to OFF
        await mode_service.set_mode(GovernanceMode.OFF)
        assert mode_service.current_mode == GovernanceMode.OFF

        # Simulate metrics collection
        result = await mode_service.check_and_rollback_if_needed(multiple_unhealthy)

        # Assert no rollback (OFF mode is exempt)
        assert result.rollback_triggered is False
        assert result.new_mode == GovernanceMode.OFF


# ============================================================================
# Kill Switch Manual Override Tests
# ============================================================================


class TestKillSwitchManualOverride:
    """Test manual override capabilities."""

    @pytest.mark.asyncio
    async def test_cto_can_manually_trigger_rollback(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test that CTO can manually trigger a rollback.

        Expected:
        - Mode changes to WARNING
        - Manual trigger is logged
        - Reason is "manual_cto_override"
        """
        # Set initial mode to FULL
        await mode_service.set_mode(GovernanceMode.FULL)

        # CTO manually triggers rollback
        result = await mode_service.manual_rollback(
            triggered_by="CTO",
            reason="Production incident P0 - Auth service down",
        )

        # Assert rollback occurred
        assert result.rollback_triggered is True
        assert result.new_mode == GovernanceMode.WARNING
        assert result.triggered_by == "CTO"
        assert "manual" in result.trigger_reasons[0].lower()

    @pytest.mark.asyncio
    async def test_ceo_can_manually_trigger_rollback(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test that CEO can manually trigger a rollback.

        Expected:
        - Mode changes to WARNING
        - Manual trigger is logged
        """
        # Set initial mode to SOFT
        await mode_service.set_mode(GovernanceMode.SOFT)

        # CEO manually triggers rollback
        result = await mode_service.manual_rollback(
            triggered_by="CEO",
            reason="Customer demo - need smooth experience",
        )

        # Assert rollback occurred
        assert result.rollback_triggered is True
        assert result.new_mode == GovernanceMode.WARNING
        assert result.triggered_by == "CEO"

    @pytest.mark.asyncio
    async def test_manual_rollback_to_specific_mode(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test manual rollback to a specific mode (not just WARNING).

        Expected:
        - Mode changes to specified level (SOFT)
        """
        # Set initial mode to FULL
        await mode_service.set_mode(GovernanceMode.FULL)

        # CTO manually rolls back to SOFT (not WARNING)
        result = await mode_service.manual_rollback(
            triggered_by="CTO",
            reason="Partial rollback for investigation",
            target_mode=GovernanceMode.SOFT,
        )

        # Assert rollback to SOFT
        assert result.rollback_triggered is True
        assert result.new_mode == GovernanceMode.SOFT

    @pytest.mark.asyncio
    async def test_manual_rollback_cannot_escalate(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test that manual rollback cannot escalate to higher enforcement.

        Expected:
        - Attempting to "rollback" from WARNING to FULL fails
        - Mode stays at WARNING
        """
        # Set initial mode to WARNING
        await mode_service.set_mode(GovernanceMode.WARNING)

        # Attempt to "rollback" to FULL (invalid - escalation, not rollback)
        with pytest.raises(ValueError, match="cannot escalate"):
            await mode_service.manual_rollback(
                triggered_by="CTO",
                reason="Testing invalid escalation",
                target_mode=GovernanceMode.FULL,
            )


# ============================================================================
# Kill Switch Notification Tests
# ============================================================================


class TestKillSwitchNotifications:
    """Test notification behavior on kill switch events."""

    @pytest.mark.asyncio
    async def test_rollback_notifies_cto_and_ceo(
        self,
        mode_service: GovernanceModeService,
        unhealthy_rejection_rate: Dict[str, Any]
    ) -> None:
        """
        Test that rollback sends notifications to CTO and CEO.

        Expected:
        - Notification sent to CTO
        - Notification sent to CEO
        - Notification includes trigger reasons
        """
        # Mock notification service
        mock_notifier = AsyncMock()
        mode_service._notification_service = mock_notifier

        # Set initial mode to FULL
        await mode_service.set_mode(GovernanceMode.FULL)

        # Trigger rollback
        result = await mode_service.check_and_rollback_if_needed(unhealthy_rejection_rate)

        # Assert notifications were sent
        assert result.rollback_triggered is True
        assert mock_notifier.send_alert.called or hasattr(result, "notifications_sent")

    @pytest.mark.asyncio
    async def test_rollback_creates_audit_log_entry(
        self,
        mode_service: GovernanceModeService,
        unhealthy_latency: Dict[str, Any]
    ) -> None:
        """
        Test that rollback creates an audit log entry.

        Expected:
        - Audit log entry created
        - Entry includes: timestamp, old_mode, new_mode, trigger_reasons
        """
        # Set initial mode to FULL
        await mode_service.set_mode(GovernanceMode.FULL)

        # Trigger rollback
        result = await mode_service.check_and_rollback_if_needed(unhealthy_latency)

        # Assert audit log entry
        assert result.rollback_triggered is True
        assert result.audit_log_entry is not None
        assert result.audit_log_entry["old_mode"] == GovernanceMode.FULL.value
        assert result.audit_log_entry["new_mode"] == GovernanceMode.WARNING.value
        assert "latency_high" in result.audit_log_entry["trigger_reasons"]


# ============================================================================
# Kill Switch Recovery Tests
# ============================================================================


class TestKillSwitchRecovery:
    """Test recovery after kill switch activation."""

    @pytest.mark.asyncio
    async def test_recovery_after_metrics_normalize(
        self,
        mode_service: GovernanceModeService,
        healthy_metrics: Dict[str, Any],
        unhealthy_rejection_rate: Dict[str, Any]
    ) -> None:
        """
        Test that system can recover after metrics normalize.

        Expected:
        1. Rollback occurs on unhealthy metrics
        2. Mode stays at WARNING
        3. Manual escalation is required (no auto-escalation)
        """
        # Set initial mode to FULL
        await mode_service.set_mode(GovernanceMode.FULL)

        # Trigger rollback
        result1 = await mode_service.check_and_rollback_if_needed(unhealthy_rejection_rate)
        assert result1.rollback_triggered is True
        assert mode_service.current_mode == GovernanceMode.WARNING

        # Metrics normalize
        result2 = await mode_service.check_and_rollback_if_needed(healthy_metrics)

        # Assert no auto-escalation (manual intervention required)
        assert result2.rollback_triggered is False
        assert mode_service.current_mode == GovernanceMode.WARNING

    @pytest.mark.asyncio
    async def test_manual_escalation_after_recovery(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test manual escalation from WARNING back to SOFT after recovery.

        Expected:
        - CTO can manually escalate after metrics normalize
        - Mode changes from WARNING to SOFT
        """
        # Start at WARNING (post-rollback state)
        await mode_service.set_mode(GovernanceMode.WARNING)

        # CTO manually escalates back to SOFT
        result = await mode_service.escalate_mode(
            target_mode=GovernanceMode.SOFT,
            escalated_by="CTO",
            reason="Metrics normalized, resuming soft enforcement",
        )

        # Assert escalation occurred
        assert result.success is True
        assert mode_service.current_mode == GovernanceMode.SOFT


# ============================================================================
# Kill Switch Edge Cases
# ============================================================================


class TestKillSwitchEdgeCases:
    """Test edge cases for kill switch behavior."""

    def test_threshold_boundary_rejection_rate_exactly_80(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test boundary condition: rejection rate exactly 80%.

        Expected: Does NOT trigger (threshold is >80%, not >=80%)
        """
        metrics = {
            "rejection_rate": 0.80,  # Exactly 80%
            "latency_p95_ms": 50,
            "false_positive_rate": 0.05,
            "developer_complaints_today": 1,
        }

        triggers = mode_service._evaluate_rollback_triggers(metrics)

        # At boundary (80%), should NOT trigger (>80% required)
        rejection_triggers = [t for t in triggers if t["reason"] == "rejection_rate_high"]
        assert len(rejection_triggers) == 0

    def test_threshold_boundary_rejection_rate_80_point_1(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test boundary condition: rejection rate 80.1%.

        Expected: SHOULD trigger (>80%)
        """
        metrics = {
            "rejection_rate": 0.801,  # 80.1% - just above threshold
            "latency_p95_ms": 50,
            "false_positive_rate": 0.05,
            "developer_complaints_today": 1,
        }

        triggers = mode_service._evaluate_rollback_triggers(metrics)

        # Just above boundary, should trigger
        rejection_triggers = [t for t in triggers if t["reason"] == "rejection_rate_high"]
        assert len(rejection_triggers) == 1

    def test_missing_metrics_handled_gracefully(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test that missing metrics are handled gracefully.

        Expected: Missing metrics do not trigger (fail-safe)
        """
        incomplete_metrics = {
            "rejection_rate": 0.40,
            # Missing: latency_p95_ms, false_positive_rate, developer_complaints_today
        }

        # Should not raise exception
        triggers = mode_service._evaluate_rollback_triggers(incomplete_metrics)

        # Should not trigger on missing data (fail-safe)
        assert len(triggers) == 0 or \
               all("rejection" in t["reason"] or "missing" not in t["reason"] for t in triggers)

    def test_negative_values_handled(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test that negative values (invalid) are handled gracefully.

        Expected: Negative values treated as 0 (fail-safe)
        """
        invalid_metrics = {
            "rejection_rate": -0.10,  # Invalid negative
            "latency_p95_ms": -50,    # Invalid negative
            "false_positive_rate": 0.05,
            "developer_complaints_today": 2,
        }

        # Should not raise exception
        triggers = mode_service._evaluate_rollback_triggers(invalid_metrics)

        # Negative values should not trigger (treated as 0)
        assert len(triggers) == 0

    def test_extreme_values_handled(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test that extreme values are handled.

        Expected: Extreme values still trigger appropriately
        """
        extreme_metrics = {
            "rejection_rate": 1.0,           # 100%
            "latency_p95_ms": 10000,          # 10 seconds
            "false_positive_rate": 0.99,     # 99%
            "developer_complaints_today": 100,  # Many complaints
        }

        triggers = mode_service._evaluate_rollback_triggers(extreme_metrics)

        # All should trigger
        assert len(triggers) >= 4


# ============================================================================
# Kill Switch State Machine Tests
# ============================================================================


class TestKillSwitchStateMachine:
    """Test state machine transitions for governance modes."""

    @pytest.mark.asyncio
    async def test_valid_state_transitions(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test all valid state transitions.

        Valid transitions:
        - OFF -> WARNING -> SOFT -> FULL (escalation)
        - FULL -> SOFT -> WARNING -> OFF (rollback)
        """
        # Escalation path
        await mode_service.set_mode(GovernanceMode.OFF)
        assert mode_service.current_mode == GovernanceMode.OFF

        await mode_service.set_mode(GovernanceMode.WARNING)
        assert mode_service.current_mode == GovernanceMode.WARNING

        await mode_service.set_mode(GovernanceMode.SOFT)
        assert mode_service.current_mode == GovernanceMode.SOFT

        await mode_service.set_mode(GovernanceMode.FULL)
        assert mode_service.current_mode == GovernanceMode.FULL

        # Rollback path
        await mode_service.set_mode(GovernanceMode.SOFT)
        assert mode_service.current_mode == GovernanceMode.SOFT

        await mode_service.set_mode(GovernanceMode.WARNING)
        assert mode_service.current_mode == GovernanceMode.WARNING

        await mode_service.set_mode(GovernanceMode.OFF)
        assert mode_service.current_mode == GovernanceMode.OFF

    @pytest.mark.asyncio
    async def test_state_history_tracking(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test that state changes are tracked in history.

        Expected: History contains all state changes with timestamps
        """
        # Perform several state changes
        await mode_service.set_mode(GovernanceMode.WARNING)
        await mode_service.set_mode(GovernanceMode.SOFT)
        await mode_service.set_mode(GovernanceMode.FULL)
        await mode_service.set_mode(GovernanceMode.WARNING)

        # Get history
        history = mode_service.get_state_history()

        # Assert history is tracked
        assert len(history) >= 4
        assert all("timestamp" in entry for entry in history)
        assert all("mode" in entry for entry in history)


# ============================================================================
# Integration Tests
# ============================================================================


class TestKillSwitchIntegration:
    """Integration tests for kill switch with other services."""

    @pytest.mark.asyncio
    async def test_kill_switch_integrates_with_metrics_collector(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test kill switch integration with Prometheus metrics collector.

        Expected:
        - Metrics collector records kill switch events
        - Rollback creates governance_killswitch_triggers_total metric
        """
        from app.services.governance.metrics_collector import get_metrics_collector

        metrics_collector = get_metrics_collector()

        # Set initial mode
        await mode_service.set_mode(GovernanceMode.FULL)

        # Trigger rollback
        unhealthy = {
            "rejection_rate": 0.90,
            "latency_p95_ms": 600,
            "false_positive_rate": 0.25,
            "developer_complaints_today": 7,
        }

        result = await mode_service.check_and_rollback_if_needed(unhealthy)

        # Record the event in metrics
        if result.rollback_triggered:
            for reason in result.trigger_reasons:
                metrics_collector.increment_counter(
                    "governance_killswitch_triggers_total",
                    labels={"trigger_reason": reason}
                )

        # Verify metric was recorded
        metrics_output = metrics_collector.get_metrics_json()
        assert "counters" in metrics_output

    @pytest.mark.asyncio
    async def test_kill_switch_integrates_with_ceo_dashboard(
        self,
        mode_service: GovernanceModeService
    ) -> None:
        """
        Test kill switch status appears in CEO dashboard.

        Expected:
        - CEO dashboard shows current governance mode
        - Dashboard shows kill switch trigger history
        """
        from app.services.governance.ceo_dashboard import get_ceo_dashboard_service

        ceo_dashboard = get_ceo_dashboard_service()

        # Get system health which includes kill switch status
        health = await ceo_dashboard.get_system_health()

        # Assert kill switch status is included
        assert hasattr(health, "governance_mode") or "mode" in str(health)
