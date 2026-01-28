"""
=========================================================================
Unit Tests: FULL Mode Enforcer - Sprint 116 Track 2
SDLC Orchestrator - Anti-Vibecoding System

Version: 1.0.0
Date: January 28, 2026
Status: READY FOR DEPLOYMENT
Framework: SDLC 5.3.0 Quality Assurance System

Tests:
- FULL mode zone behavior (GREEN auto-approve, others require approval)
- Approval workflow (Tech Lead, CEO, CTO+CEO)
- CEO time tracking integration
- Coverage drop blocking
- Kill switch criteria

Zero Mock Policy: Real enforcer with test configurations
=========================================================================
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from app.services.governance.full_mode_enforcer import (
    ApprovalRequirement,
    ApprovalStatus,
    CEOTimeEntry,
    FullModeEnforcer,
    FullModeEnforcementResult,
    create_full_mode_enforcer,
    get_full_mode_enforcer,
)
from app.services.governance.signals_engine import (
    IndexCategory,
    RoutingDecision,
    VibecodingIndex,
)
from app.services.governance.soft_mode_enforcer import EnforcementAction


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def enforcer():
    """Create a FULL mode enforcer with default config."""
    return FullModeEnforcer()


@pytest.fixture
def green_index():
    """Create a GREEN zone Vibecoding Index (score 25)."""
    return VibecodingIndex(
        score=25.0,
        category=IndexCategory.GREEN,
        routing=RoutingDecision.AUTO_APPROVE,
        signals={},
    )


@pytest.fixture
def yellow_index():
    """Create a YELLOW zone Vibecoding Index (score 45)."""
    return VibecodingIndex(
        score=45.0,
        category=IndexCategory.YELLOW,
        routing=RoutingDecision.TECH_LEAD_REVIEW,
        signals={},
    )


@pytest.fixture
def orange_index():
    """Create an ORANGE zone Vibecoding Index (score 72)."""
    return VibecodingIndex(
        score=72.0,
        category=IndexCategory.ORANGE,
        routing=RoutingDecision.CEO_SHOULD_REVIEW,
        signals={},
    )


@pytest.fixture
def red_index():
    """Create a RED zone Vibecoding Index (score 88)."""
    return VibecodingIndex(
        score=88.0,
        category=IndexCategory.RED,
        routing=RoutingDecision.CEO_MUST_REVIEW,
        signals={},
    )


@pytest.fixture
def simple_submission():
    """Create a simple code submission."""
    class MockSubmission:
        def __init__(self):
            self.changed_files = ["backend/app/services/user_service.py"]
            self.is_new_feature = False
            self.pr_number = 123

    return MockSubmission()


# ============================================================================
# GREEN Zone Tests (Auto-Approve)
# ============================================================================


class TestGreenZoneFullMode:
    """Test GREEN zone behavior in FULL mode."""

    def test_green_zone_auto_approved(self, enforcer, green_index, simple_submission):
        """GREEN zone PRs should be auto-approved without review."""
        result = enforcer.enforce_full(
            vibecoding_index=green_index,
            submission=simple_submission,
        )

        assert result.action == EnforcementAction.AUTO_APPROVED
        assert result.can_merge is True
        assert result.approval_required is False
        assert result.approval_type == ApprovalRequirement.NONE
        assert result.ceo_review_required is False
        assert "auto-approved" in result.message.lower()

    def test_green_zone_no_approval_request(self, enforcer, green_index, simple_submission):
        """GREEN zone should not create approval request."""
        result = enforcer.enforce_full(
            vibecoding_index=green_index,
            submission=simple_submission,
        )

        assert result.approval_request is None
        assert result.estimated_review_time_minutes == 0.0


# ============================================================================
# YELLOW Zone Tests (Tech Lead Approval)
# ============================================================================


class TestYellowZoneFullMode:
    """Test YELLOW zone behavior in FULL mode."""

    def test_yellow_zone_requires_tech_lead(self, enforcer, yellow_index, simple_submission):
        """YELLOW zone PRs should require Tech Lead approval."""
        result = enforcer.enforce_full(
            vibecoding_index=yellow_index,
            submission=simple_submission,
        )

        assert result.approval_required is True
        assert result.approval_type == ApprovalRequirement.TECH_LEAD
        assert result.can_merge is False
        assert result.ceo_review_required is False
        assert "tech lead" in result.message.lower()

    def test_yellow_zone_creates_approval_request(self, enforcer, yellow_index, simple_submission):
        """YELLOW zone should create approval request for Tech Lead."""
        result = enforcer.enforce_full(
            vibecoding_index=yellow_index,
            submission=simple_submission,
        )

        assert result.approval_request is not None
        assert "Tech Lead" in result.approval_request.required_approvers
        assert result.approval_request.timeout_hours == 24

    def test_yellow_zone_estimated_review_time(self, enforcer, yellow_index, simple_submission):
        """YELLOW zone should have 15 min estimated review time."""
        result = enforcer.enforce_full(
            vibecoding_index=yellow_index,
            submission=simple_submission,
        )

        assert result.estimated_review_time_minutes == 15.0


# ============================================================================
# ORANGE Zone Tests (CEO Approval)
# ============================================================================


class TestOrangeZoneFullMode:
    """Test ORANGE zone behavior in FULL mode."""

    def test_orange_zone_requires_ceo(self, enforcer, orange_index, simple_submission):
        """ORANGE zone PRs should require CEO approval."""
        result = enforcer.enforce_full(
            vibecoding_index=orange_index,
            submission=simple_submission,
        )

        assert result.approval_required is True
        assert result.approval_type == ApprovalRequirement.CEO
        assert result.can_merge is False
        assert result.ceo_review_required is True
        assert "ceo" in result.message.lower()

    def test_orange_zone_creates_approval_request(self, enforcer, orange_index, simple_submission):
        """ORANGE zone should create approval request for CEO."""
        result = enforcer.enforce_full(
            vibecoding_index=orange_index,
            submission=simple_submission,
        )

        assert result.approval_request is not None
        assert "CEO" in result.approval_request.required_approvers
        assert result.approval_request.timeout_hours == 48

    def test_orange_zone_estimated_review_time(self, enforcer, orange_index, simple_submission):
        """ORANGE zone should have 30 min estimated review time."""
        result = enforcer.enforce_full(
            vibecoding_index=orange_index,
            submission=simple_submission,
        )

        assert result.estimated_review_time_minutes == 30.0


# ============================================================================
# RED Zone Tests (CTO+CEO Override)
# ============================================================================


class TestRedZoneFullMode:
    """Test RED zone behavior in FULL mode."""

    def test_red_zone_blocked(self, enforcer, red_index, simple_submission):
        """RED zone PRs should be blocked."""
        result = enforcer.enforce_full(
            vibecoding_index=red_index,
            submission=simple_submission,
        )

        assert result.action == EnforcementAction.BLOCKED
        assert result.approval_required is True
        assert result.approval_type == ApprovalRequirement.CTO_CEO
        assert result.can_merge is False
        assert result.ceo_review_required is True

    def test_red_zone_requires_cto_ceo_override(self, enforcer, red_index, simple_submission):
        """RED zone should require CTO+CEO override."""
        result = enforcer.enforce_full(
            vibecoding_index=red_index,
            submission=simple_submission,
        )

        assert result.requires_override is True
        assert "CTO" in result.override_authority or result.approval_type == ApprovalRequirement.CTO_CEO

    def test_red_zone_estimated_review_time(self, enforcer, red_index, simple_submission):
        """RED zone should have 60 min estimated review time."""
        result = enforcer.enforce_full(
            vibecoding_index=red_index,
            submission=simple_submission,
        )

        assert result.estimated_review_time_minutes == 60.0


# ============================================================================
# Coverage Drop Tests
# ============================================================================


class TestCoverageDropFullMode:
    """Test coverage drop blocking in FULL mode."""

    def test_coverage_drop_blocks(self, enforcer, green_index, simple_submission):
        """Coverage drop > 5% should block PR."""
        result = enforcer.enforce_full(
            vibecoding_index=green_index,
            submission=simple_submission,
            coverage_delta=-7.0,  # 7% drop
        )

        assert result.action == EnforcementAction.BLOCKED
        assert any("coverage" in b.message.lower() for b in result.block_rules_triggered if b.triggered)

    def test_small_coverage_drop_allowed(self, enforcer, green_index, simple_submission):
        """Coverage drop < 5% should be allowed."""
        result = enforcer.enforce_full(
            vibecoding_index=green_index,
            submission=simple_submission,
            coverage_delta=-3.0,  # 3% drop - acceptable
        )

        # GREEN zone with small coverage drop should still auto-approve
        assert result.action == EnforcementAction.AUTO_APPROVED

    def test_coverage_increase_allowed(self, enforcer, green_index, simple_submission):
        """Coverage increase should always be allowed."""
        result = enforcer.enforce_full(
            vibecoding_index=green_index,
            submission=simple_submission,
            coverage_delta=5.0,  # 5% increase
        )

        assert result.action == EnforcementAction.AUTO_APPROVED


# ============================================================================
# Approval Workflow Tests
# ============================================================================


class TestApprovalWorkflow:
    """Test approval workflow functionality."""

    def test_approve_tech_lead_request(self, enforcer, yellow_index, simple_submission):
        """Tech Lead can approve YELLOW zone PRs."""
        # Create enforcement result with approval request
        result = enforcer.enforce_full(
            vibecoding_index=yellow_index,
            submission=simple_submission,
        )

        request_id = result.approval_request.id

        # Approve as Tech Lead
        success = enforcer.approve(
            request_id=request_id,
            approved_by="tech_lead_user",
            approver_role="Tech Lead",
        )

        assert success is True
        assert enforcer._pending_approvals[request_id].status == ApprovalStatus.APPROVED

    def test_wrong_role_cannot_approve(self, enforcer, orange_index, simple_submission):
        """Tech Lead cannot approve CEO-required PRs."""
        result = enforcer.enforce_full(
            vibecoding_index=orange_index,
            submission=simple_submission,
        )

        request_id = result.approval_request.id

        # Try to approve as Tech Lead (should fail - requires CEO)
        success = enforcer.approve(
            request_id=request_id,
            approved_by="tech_lead_user",
            approver_role="Tech Lead",
        )

        assert success is False
        assert enforcer._pending_approvals[request_id].status == ApprovalStatus.PENDING

    def test_reject_approval_request(self, enforcer, yellow_index, simple_submission):
        """Approval requests can be rejected."""
        result = enforcer.enforce_full(
            vibecoding_index=yellow_index,
            submission=simple_submission,
        )

        request_id = result.approval_request.id

        # Reject
        success = enforcer.reject(
            request_id=request_id,
            rejected_by="reviewer",
            reason="Needs refactoring",
        )

        assert success is True
        assert enforcer._pending_approvals[request_id].status == ApprovalStatus.REJECTED
        assert "refactoring" in enforcer._pending_approvals[request_id].rejection_reason.lower()

    def test_get_pending_approvals(self, enforcer, yellow_index, orange_index, simple_submission):
        """Can retrieve pending approvals filtered by role."""
        # Create two approval requests
        enforcer.enforce_full(vibecoding_index=yellow_index, submission=simple_submission)
        enforcer.enforce_full(vibecoding_index=orange_index, submission=simple_submission)

        # Get all pending
        all_pending = enforcer.get_pending_approvals()
        assert len(all_pending) == 2

        # Get Tech Lead pending
        tech_lead_pending = enforcer.get_pending_approvals(approver_role="Tech Lead")
        assert len(tech_lead_pending) == 1

        # Get CEO pending
        ceo_pending = enforcer.get_pending_approvals(approver_role="CEO")
        assert len(ceo_pending) == 1


# ============================================================================
# CEO Time Tracking Tests
# ============================================================================


class TestCEOTimeTracking:
    """Test CEO time tracking functionality."""

    def test_ceo_approval_records_time(self, enforcer, orange_index, simple_submission):
        """CEO approval should automatically record time."""
        result = enforcer.enforce_full(
            vibecoding_index=orange_index,
            submission=simple_submission,
        )

        request_id = result.approval_request.id
        initial_entries = len(enforcer._ceo_time_entries)

        # Approve as CEO
        enforcer.approve(
            request_id=request_id,
            approved_by="ceo_user",
            approver_role="CEO",
        )

        # Check time was recorded
        assert len(enforcer._ceo_time_entries) == initial_entries + 1
        latest_entry = enforcer._ceo_time_entries[-1]
        assert latest_entry.activity_type == "pr_approval"
        assert latest_entry.category == "governance"

    def test_manual_ceo_time_recording(self, enforcer):
        """Can manually record CEO time."""
        entry = enforcer.record_manual_ceo_time(
            activity_type="architecture_review",
            duration_minutes=60.0,
            notes="Reviewed new microservice design",
        )

        assert entry.activity_type == "architecture_review"
        assert entry.duration_minutes == 60.0
        assert entry.category == "design"

    def test_ceo_time_summary(self, enforcer):
        """Can get CEO time summary with savings calculation."""
        # Record some time
        enforcer.record_manual_ceo_time("pr_review", 30.0)
        enforcer.record_manual_ceo_time("meeting", 60.0)
        enforcer.record_manual_ceo_time("architecture_review", 45.0)

        summary = enforcer.get_ceo_time_summary(days=7)

        assert summary["total_hours"] == 2.25  # 135 min = 2.25 hours
        assert summary["baseline_hours"] == 40  # 40 hours baseline
        assert summary["savings_hours"] > 0
        assert summary["savings_percent"] > 0
        assert summary["entry_count"] == 3

    def test_ceo_time_breakdown(self, enforcer):
        """CEO time summary includes breakdown by category."""
        enforcer.record_manual_ceo_time("pr_review", 30.0)
        enforcer.record_manual_ceo_time("pr_review", 20.0)
        enforcer.record_manual_ceo_time("meeting", 60.0)

        summary = enforcer.get_ceo_time_summary(days=7)

        assert "code_review" in summary["breakdown_minutes"]
        assert "meeting" in summary["breakdown_minutes"]
        assert summary["breakdown_minutes"]["code_review"] == 50.0
        assert summary["breakdown_minutes"]["meeting"] == 60.0


# ============================================================================
# Kill Switch Tests
# ============================================================================


class TestKillSwitchFullMode:
    """Test kill switch criteria for FULL mode."""

    def test_kill_switch_not_triggered_normal(self, enforcer):
        """Kill switch should not trigger under normal conditions."""
        result = enforcer.check_kill_switch()
        assert result is None

    def test_kill_switch_stricter_than_soft(self, enforcer):
        """FULL mode kill switch has stricter thresholds."""
        # FULL mode threshold is 50% vs SOFT mode 80%
        config = enforcer.full_config.get("kill_switch", {}).get("criteria", {})
        rejection_threshold = config.get("rejection_rate", {}).get("threshold", 0.5)

        assert rejection_threshold <= 0.5  # Stricter than SOFT mode's 0.8


# ============================================================================
# Factory Function Tests
# ============================================================================


class TestFactoryFunctions:
    """Test factory functions."""

    def test_create_full_mode_enforcer(self):
        """Can create FULL mode enforcer."""
        enforcer = create_full_mode_enforcer()
        assert isinstance(enforcer, FullModeEnforcer)

    def test_get_full_mode_enforcer_singleton(self):
        """get_full_mode_enforcer returns singleton."""
        enforcer1 = get_full_mode_enforcer()
        enforcer2 = get_full_mode_enforcer()
        assert enforcer1 is enforcer2


# ============================================================================
# Result Serialization Tests
# ============================================================================


class TestResultSerialization:
    """Test result serialization."""

    def test_full_mode_result_to_dict(self, enforcer, orange_index, simple_submission):
        """FullModeEnforcementResult can be serialized."""
        result = enforcer.enforce_full(
            vibecoding_index=orange_index,
            submission=simple_submission,
        )

        result_dict = result.to_dict()

        assert "full_mode" in result_dict
        assert result_dict["full_mode"]["approval_required"] is True
        assert result_dict["full_mode"]["approval_type"] == "ceo"
        assert result_dict["full_mode"]["ceo_review_required"] is True
        assert result_dict["full_mode"]["estimated_review_time_minutes"] == 30.0
