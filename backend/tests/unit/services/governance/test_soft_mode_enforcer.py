"""
=========================================================================
SOFT Mode Enforcer Tests - Sprint 115 Track 2
SDLC Orchestrator - Anti-Vibecoding System

Version: 1.0.0
Date: January 28, 2026
Status: Ready for Sprint 115 Deployment

Tests:
1. Exemption rules (dependency, documentation, test-only)
2. Block rules (red zone, missing ownership, security)
3. Warn rules (orange zone, missing ADR, low coverage)
4. Action determination (blocked, warned, approved, auto-approved)
5. Weight adjustments (drift_velocity tuning)

Target: 95%+ coverage for soft_mode_enforcer.py
=========================================================================
"""

from datetime import datetime
from uuid import uuid4

import pytest

from app.services.governance.signals_engine import (
    CodeSubmission,
    IndexCategory,
    RoutingDecision,
    SignalScore,
    SignalType,
    VibecodingIndex,
)
from app.services.governance.soft_mode_enforcer import (
    EnforcementAction,
    ExemptionType,
    SoftModeEnforcer,
    create_soft_mode_enforcer,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def enforcer():
    """Create a SoftModeEnforcer with default config."""
    return create_soft_mode_enforcer()


@pytest.fixture
def green_index():
    """Create a green zone Vibecoding Index (score=25)."""
    return VibecodingIndex(
        score=25.0,
        category=IndexCategory.GREEN,
        routing=RoutingDecision.AUTO_APPROVE,
        signals={
            SignalType.ARCHITECTURAL_SMELL: SignalScore(
                signal_type=SignalType.ARCHITECTURAL_SMELL,
                score=20.0,
                weight=0.25,
                weighted_score=5.0,
            ),
            SignalType.ABSTRACTION_COMPLEXITY: SignalScore(
                signal_type=SignalType.ABSTRACTION_COMPLEXITY,
                score=15.0,
                weight=0.15,
                weighted_score=2.25,
            ),
            SignalType.AI_DEPENDENCY_RATIO: SignalScore(
                signal_type=SignalType.AI_DEPENDENCY_RATIO,
                score=30.0,
                weight=0.20,
                weighted_score=6.0,
            ),
            SignalType.CHANGE_SURFACE_AREA: SignalScore(
                signal_type=SignalType.CHANGE_SURFACE_AREA,
                score=20.0,
                weight=0.25,
                weighted_score=5.0,
            ),
            SignalType.DRIFT_VELOCITY: SignalScore(
                signal_type=SignalType.DRIFT_VELOCITY,
                score=45.0,
                weight=0.15,
                weighted_score=6.75,
            ),
        },
    )


@pytest.fixture
def yellow_index():
    """Create a yellow zone Vibecoding Index (score=45)."""
    return VibecodingIndex(
        score=45.0,
        category=IndexCategory.YELLOW,
        routing=RoutingDecision.TECH_LEAD_REVIEW,
        signals={
            SignalType.ARCHITECTURAL_SMELL: SignalScore(
                signal_type=SignalType.ARCHITECTURAL_SMELL,
                score=40.0,
                weight=0.25,
                weighted_score=10.0,
            ),
            SignalType.ABSTRACTION_COMPLEXITY: SignalScore(
                signal_type=SignalType.ABSTRACTION_COMPLEXITY,
                score=30.0,
                weight=0.15,
                weighted_score=4.5,
            ),
            SignalType.AI_DEPENDENCY_RATIO: SignalScore(
                signal_type=SignalType.AI_DEPENDENCY_RATIO,
                score=50.0,
                weight=0.20,
                weighted_score=10.0,
            ),
            SignalType.CHANGE_SURFACE_AREA: SignalScore(
                signal_type=SignalType.CHANGE_SURFACE_AREA,
                score=35.0,
                weight=0.25,
                weighted_score=8.75,
            ),
            SignalType.DRIFT_VELOCITY: SignalScore(
                signal_type=SignalType.DRIFT_VELOCITY,
                score=78.0,
                weight=0.15,
                weighted_score=11.75,
            ),
        },
    )


@pytest.fixture
def orange_index():
    """Create an orange zone Vibecoding Index (score=72)."""
    return VibecodingIndex(
        score=72.0,
        category=IndexCategory.ORANGE,
        routing=RoutingDecision.CEO_SHOULD_REVIEW,
        signals={
            SignalType.ARCHITECTURAL_SMELL: SignalScore(
                signal_type=SignalType.ARCHITECTURAL_SMELL,
                score=65.0,
                weight=0.25,
                weighted_score=16.25,
            ),
            SignalType.ABSTRACTION_COMPLEXITY: SignalScore(
                signal_type=SignalType.ABSTRACTION_COMPLEXITY,
                score=55.0,
                weight=0.15,
                weighted_score=8.25,
            ),
            SignalType.AI_DEPENDENCY_RATIO: SignalScore(
                signal_type=SignalType.AI_DEPENDENCY_RATIO,
                score=80.0,
                weight=0.20,
                weighted_score=16.0,
            ),
            SignalType.CHANGE_SURFACE_AREA: SignalScore(
                signal_type=SignalType.CHANGE_SURFACE_AREA,
                score=70.0,
                weight=0.25,
                weighted_score=17.5,
            ),
            SignalType.DRIFT_VELOCITY: SignalScore(
                signal_type=SignalType.DRIFT_VELOCITY,
                score=93.0,
                weight=0.15,
                weighted_score=14.0,
            ),
        },
    )


@pytest.fixture
def red_index():
    """Create a red zone Vibecoding Index (score=88)."""
    return VibecodingIndex(
        score=88.0,
        category=IndexCategory.RED,
        routing=RoutingDecision.CEO_MUST_REVIEW,
        signals={
            SignalType.ARCHITECTURAL_SMELL: SignalScore(
                signal_type=SignalType.ARCHITECTURAL_SMELL,
                score=85.0,
                weight=0.25,
                weighted_score=21.25,
            ),
            SignalType.ABSTRACTION_COMPLEXITY: SignalScore(
                signal_type=SignalType.ABSTRACTION_COMPLEXITY,
                score=70.0,
                weight=0.15,
                weighted_score=10.5,
            ),
            SignalType.AI_DEPENDENCY_RATIO: SignalScore(
                signal_type=SignalType.AI_DEPENDENCY_RATIO,
                score=95.0,
                weight=0.20,
                weighted_score=19.0,
            ),
            SignalType.CHANGE_SURFACE_AREA: SignalScore(
                signal_type=SignalType.CHANGE_SURFACE_AREA,
                score=90.0,
                weight=0.25,
                weighted_score=22.5,
            ),
            SignalType.DRIFT_VELOCITY: SignalScore(
                signal_type=SignalType.DRIFT_VELOCITY,
                score=98.0,
                weight=0.15,
                weighted_score=14.75,
            ),
        },
    )


@pytest.fixture
def regular_submission():
    """Create a regular code submission."""
    return CodeSubmission(
        submission_id=uuid4(),
        project_id=uuid4(),
        changed_files=[
            "backend/app/services/auth_service.py",
            "backend/tests/test_auth_service.py",
        ],
        added_lines=150,
        removed_lines=30,
        ai_generated_lines=50,
        total_lines=180,
        commit_messages=["feat(auth): Add MFA support"],
        is_new_feature=True,
        affected_modules=["auth", "security"],
    )


@pytest.fixture
def dependency_submission():
    """Create a dependency update submission."""
    return CodeSubmission(
        submission_id=uuid4(),
        project_id=uuid4(),
        changed_files=["package.json", "package-lock.json"],
        added_lines=25,
        removed_lines=20,
        ai_generated_lines=0,
        total_lines=45,
        commit_messages=["chore: Update dependencies"],
        is_new_feature=False,
        affected_modules=[],
    )


@pytest.fixture
def documentation_submission():
    """Create a documentation-only submission."""
    return CodeSubmission(
        submission_id=uuid4(),
        project_id=uuid4(),
        changed_files=["docs/api-reference.md", "README.md"],
        added_lines=80,
        removed_lines=10,
        ai_generated_lines=20,
        total_lines=90,
        commit_messages=["docs: Update API documentation"],
        is_new_feature=False,
        affected_modules=[],
    )


@pytest.fixture
def test_only_submission():
    """Create a test-only submission."""
    return CodeSubmission(
        submission_id=uuid4(),
        project_id=uuid4(),
        changed_files=[
            "tests/unit/test_auth.py",
            "tests/integration/test_api.py",
        ],
        added_lines=300,
        removed_lines=50,
        ai_generated_lines=100,
        total_lines=350,
        commit_messages=["test: Add comprehensive auth tests"],
        is_new_feature=False,
        affected_modules=["tests"],
    )


# ============================================================================
# Exemption Tests
# ============================================================================


class TestDependencyExemption:
    """Tests for dependency_update_exemption rule."""

    def test_dependency_exemption_applies(self, enforcer, dependency_submission):
        """Dependency exemption should apply for package file changes."""
        exemptions = enforcer.evaluate_exemptions(dependency_submission)
        dep_exemption = next(
            (e for e in exemptions if e.exemption_type == ExemptionType.DEPENDENCY_UPDATE),
            None,
        )

        assert dep_exemption is not None
        assert dep_exemption.applied is True
        assert "drift_velocity_multiplier" in dep_exemption.adjustments
        assert dep_exemption.adjustments["drift_velocity_multiplier"] == 0.5
        assert dep_exemption.adjustments["max_index_cap"] == 40

    def test_dependency_exemption_not_applies_for_code(
        self, enforcer, regular_submission
    ):
        """Dependency exemption should not apply for regular code changes."""
        exemptions = enforcer.evaluate_exemptions(regular_submission)
        dep_exemption = next(
            (e for e in exemptions if e.exemption_type == ExemptionType.DEPENDENCY_UPDATE),
            None,
        )

        assert dep_exemption is None or dep_exemption.applied is False


class TestDocumentationExemption:
    """Tests for documentation_safe_pattern rule."""

    def test_documentation_exemption_applies(
        self, enforcer, documentation_submission
    ):
        """Documentation exemption should apply for docs-only changes."""
        exemptions = enforcer.evaluate_exemptions(documentation_submission)
        doc_exemption = next(
            (e for e in exemptions if e.exemption_type == ExemptionType.DOCUMENTATION_SAFE),
            None,
        )

        assert doc_exemption is not None
        assert doc_exemption.applied is True
        assert doc_exemption.adjustments.get("auto_approve") is True

    def test_documentation_exemption_not_applies_for_code(
        self, enforcer, regular_submission
    ):
        """Documentation exemption should not apply for code changes."""
        exemptions = enforcer.evaluate_exemptions(regular_submission)
        doc_exemption = next(
            (e for e in exemptions if e.exemption_type == ExemptionType.DOCUMENTATION_SAFE),
            None,
        )

        assert doc_exemption is None or doc_exemption.applied is False


class TestTestOnlyExemption:
    """Tests for test_only_pattern rule."""

    def test_test_only_exemption_applies(self, enforcer, test_only_submission):
        """Test-only exemption should apply for test file changes."""
        exemptions = enforcer.evaluate_exemptions(test_only_submission)
        test_exemption = next(
            (e for e in exemptions if e.exemption_type == ExemptionType.TEST_ONLY),
            None,
        )

        assert test_exemption is not None
        assert test_exemption.applied is True
        assert "abstraction_complexity_multiplier" in test_exemption.adjustments

    def test_test_only_exemption_not_applies_for_code(
        self, enforcer, regular_submission
    ):
        """Test-only exemption should not apply for regular code changes."""
        exemptions = enforcer.evaluate_exemptions(regular_submission)
        test_exemption = next(
            (e for e in exemptions if e.exemption_type == ExemptionType.TEST_ONLY),
            None,
        )

        assert test_exemption is None or test_exemption.applied is False


# ============================================================================
# Block Rule Tests
# ============================================================================


class TestBlockRules:
    """Tests for block rules in SOFT mode."""

    def test_red_zone_blocked(self, enforcer, red_index, regular_submission):
        """Red zone PRs should be blocked."""
        result = enforcer.enforce(red_index, regular_submission)

        assert result.action == EnforcementAction.BLOCKED
        assert result.can_merge is False
        assert result.requires_override is True
        assert "CTO" in result.override_authority

    def test_missing_ownership_blocked(self, enforcer, green_index, regular_submission):
        """PRs without ownership should be blocked (no override)."""
        result = enforcer.enforce(
            green_index, regular_submission, has_ownership=False
        )

        assert result.action == EnforcementAction.BLOCKED
        assert result.can_merge is False
        assert result.requires_override is False  # No override allowed

    def test_missing_intent_blocked(self, enforcer, green_index, regular_submission):
        """PRs without intent should be blocked (no override)."""
        result = enforcer.enforce(
            green_index, regular_submission, has_intent=False
        )

        assert result.action == EnforcementAction.BLOCKED
        assert result.can_merge is False

    def test_security_critical_blocked(self, enforcer, green_index, regular_submission):
        """PRs with critical security issues should be blocked."""
        result = enforcer.enforce(
            green_index, regular_submission, security_scan_critical=3
        )

        assert result.action == EnforcementAction.BLOCKED
        assert result.can_merge is False
        assert result.requires_override is True
        assert "CTO" in result.override_authority
        assert "Security Lead" in result.override_authority


# ============================================================================
# Warn Rule Tests
# ============================================================================


class TestWarnRules:
    """Tests for warn rules in SOFT mode."""

    def test_orange_zone_warned(self, enforcer, orange_index, regular_submission):
        """Orange zone PRs should be warned but can merge."""
        result = enforcer.enforce(orange_index, regular_submission)

        assert result.action == EnforcementAction.WARNED
        assert result.can_merge is True
        assert "orange zone" in result.message.lower()

    def test_missing_adr_warned_for_new_feature(
        self, enforcer, green_index, regular_submission
    ):
        """New features without ADR linkage should be warned."""
        result = enforcer.enforce(
            green_index, regular_submission, has_adr_linkage=False
        )

        # Should be warned (new feature without ADR)
        warned_rules = [w for w in result.warn_rules_triggered if w.triggered]
        adr_warning = next(
            (w for w in warned_rules if w.rule_name == "missing_adr_linkage"), None
        )
        assert adr_warning is not None

    def test_low_coverage_warned(self, enforcer, green_index, regular_submission):
        """PRs with low test coverage should be warned."""
        result = enforcer.enforce(
            green_index, regular_submission, test_coverage=65.0
        )

        warned_rules = [w for w in result.warn_rules_triggered if w.triggered]
        coverage_warning = next(
            (w for w in warned_rules if w.rule_name == "low_test_coverage"), None
        )
        assert coverage_warning is not None
        assert "65" in coverage_warning.message


# ============================================================================
# Action Determination Tests
# ============================================================================


class TestActionDetermination:
    """Tests for enforcement action determination."""

    def test_green_zone_auto_approved(self, enforcer, green_index, regular_submission):
        """Green zone PRs should be auto-approved."""
        result = enforcer.enforce(green_index, regular_submission)

        assert result.action == EnforcementAction.AUTO_APPROVED
        assert result.can_merge is True

    def test_yellow_zone_approved(self, enforcer, yellow_index, regular_submission):
        """Yellow zone PRs should be approved with Tech Lead suggestion."""
        result = enforcer.enforce(yellow_index, regular_submission)

        assert result.action == EnforcementAction.APPROVED
        assert result.can_merge is True
        assert "yellow zone" in result.message.lower()

    def test_documentation_auto_approved(
        self, enforcer, green_index, documentation_submission
    ):
        """Documentation-only PRs with low index should be auto-approved."""
        result = enforcer.enforce(green_index, documentation_submission)

        assert result.action == EnforcementAction.AUTO_APPROVED
        assert result.can_merge is True


# ============================================================================
# Weight Adjustment Tests
# ============================================================================


class TestWeightAdjustments:
    """Tests for signal weight adjustments (Sprint 114 Day 3 tuning)."""

    def test_adjusted_weights_returned(self, enforcer):
        """Get adjusted weights should return tuned values."""
        weights = enforcer.get_adjusted_weights()

        # Sprint 114 tuning: drift_velocity reduced from 0.20 to 0.15
        assert weights[SignalType.DRIFT_VELOCITY] == 0.15

        # change_surface_area increased from 0.20 to 0.25
        assert weights[SignalType.CHANGE_SURFACE_AREA] == 0.25

        # Others unchanged
        assert weights[SignalType.ARCHITECTURAL_SMELL] == 0.25
        assert weights[SignalType.ABSTRACTION_COMPLEXITY] == 0.15
        assert weights[SignalType.AI_DEPENDENCY_RATIO] == 0.20

    def test_weights_sum_to_one(self, enforcer):
        """All weights should sum to 1.0."""
        weights = enforcer.get_adjusted_weights()
        total = sum(weights.values())
        assert abs(total - 1.0) < 0.001


# ============================================================================
# Integration Tests
# ============================================================================


class TestEnforcementIntegration:
    """Integration tests for complete enforcement flow."""

    def test_dependency_update_exemption_caps_index(
        self, enforcer, dependency_submission
    ):
        """Dependency update exemption should cap index at 40."""
        # Create a high index that would normally be yellow/orange
        high_index = VibecodingIndex(
            score=55.0,
            category=IndexCategory.YELLOW,
            routing=RoutingDecision.TECH_LEAD_REVIEW,
            signals={},
        )

        result = enforcer.enforce(high_index, dependency_submission)

        # Index should be capped at 40 (dependency exemption)
        assert result.vibecoding_index.score <= 40
        assert result.can_merge is True

    def test_enforcement_result_to_dict(self, enforcer, green_index, regular_submission):
        """EnforcementResult should serialize to dict correctly."""
        result = enforcer.enforce(green_index, regular_submission)
        result_dict = result.to_dict()

        assert "enforcement" in result_dict
        assert "vibecoding_index" in result_dict
        assert "exemptions" in result_dict
        assert "block_rules" in result_dict
        assert "warnings" in result_dict
        assert result_dict["enforcement"]["can_merge"] is True

    def test_multiple_exemptions_can_apply(
        self, enforcer
    ):
        """Multiple exemptions can apply to the same submission."""
        # Create a submission with both test and doc files
        mixed_submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["tests/test_readme.py"],  # Matches test pattern
            added_lines=50,
            removed_lines=10,
            is_new_feature=False,
        )

        exemptions = enforcer.evaluate_exemptions(mixed_submission)
        applied = [e for e in exemptions if e.applied]

        # Test-only pattern should apply
        test_applied = any(
            e.exemption_type == ExemptionType.TEST_ONLY for e in applied
        )
        assert test_applied is True


# ============================================================================
# Factory Tests
# ============================================================================


class TestFactory:
    """Tests for factory function."""

    def test_create_soft_mode_enforcer_default(self):
        """Factory should create enforcer with default config."""
        enforcer = create_soft_mode_enforcer()
        assert enforcer is not None
        assert isinstance(enforcer, SoftModeEnforcer)

    def test_create_soft_mode_enforcer_custom_path(self, tmp_path):
        """Factory should accept custom config path."""
        # Create a minimal config file
        config_file = tmp_path / "custom_config.yaml"
        config_file.write_text(
            """
governance:
  mode: soft
signal_weights:
  architectural_smell: 0.30
  abstraction_complexity: 0.10
  ai_dependency_ratio: 0.20
  change_surface_area: 0.25
  drift_velocity: 0.15
exemptions:
  dependency_update_exemption:
    enabled: true
    trigger_files:
      - package.json
"""
        )

        enforcer = create_soft_mode_enforcer(str(config_file))
        weights = enforcer.get_adjusted_weights()

        # Custom weights should be loaded
        assert weights[SignalType.ARCHITECTURAL_SMELL] == 0.30
        assert weights[SignalType.ABSTRACTION_COMPLEXITY] == 0.10
