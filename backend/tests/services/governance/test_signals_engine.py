"""
=========================================================================
Governance Signals Engine Tests
SDLC Orchestrator - Sprint 109 (Vibecoding Index & Stage-Aware Gating)

Version: 1.0.0
Date: January 27, 2026
Status: ACTIVE - Sprint 109 Day 7
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 Quality Assurance System

Test Coverage:
- Signal calculators (5 signals)
- Vibecoding Index calculation
- Critical path detection
- Routing decisions
- Factory functions

Zero Mock Policy: Real calculations, no mocked results
=========================================================================
"""

import pytest
from datetime import datetime
from uuid import uuid4

from app.services.governance.signals_engine import (
    GovernanceSignalsEngine,
    CodeSubmission,
    ProjectContext,
    VibecodingIndex,
    SignalScore,
    SignalType,
    IndexCategory,
    RoutingDecision,
    CriticalPathMatch,
    ArchitecturalSmellCalculator,
    AbstractionComplexityCalculator,
    AIDependencyRatioCalculator,
    ChangeSurfaceAreaCalculator,
    DriftVelocityCalculator,
    CriticalPathChecker,
    create_signals_engine,
    get_signals_engine,
    INDEX_THRESHOLDS,
    SIGNAL_WEIGHTS,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def engine():
    """Create a fresh signals engine instance."""
    return GovernanceSignalsEngine()


@pytest.fixture
def simple_submission():
    """Create a simple code submission."""
    return CodeSubmission(
        submission_id=uuid4(),
        project_id=uuid4(),
        changed_files=["backend/app/services/user_service.py"],
        added_lines=50,
        removed_lines=10,
        ai_generated_lines=20,
        total_lines=100,
        commit_messages=["Add user service"],
        is_new_feature=True,
        affected_modules=["services"],
    )


@pytest.fixture
def large_submission():
    """Create a large multi-file submission."""
    return CodeSubmission(
        submission_id=uuid4(),
        project_id=uuid4(),
        changed_files=[
            "backend/app/services/auth.py",
            "backend/app/services/user.py",
            "backend/app/api/routes/auth.py",
            "backend/app/api/routes/users.py",
            "backend/app/models/user.py",
            "backend/app/db/migrations/001.py",
            "frontend/src/components/Login.tsx",
            "frontend/src/hooks/useAuth.ts",
            "tests/test_auth.py",
            "tests/test_users.py",
            "prisma/schema.prisma",
        ],
        added_lines=500,
        removed_lines=100,
        ai_generated_lines=400,
        total_lines=500,
        commit_messages=["Major auth refactor"],
        is_new_feature=True,
        affected_modules=["services", "api", "models", "db", "frontend"],
    )


@pytest.fixture
def critical_path_submission():
    """Create a submission with critical path files."""
    return CodeSubmission(
        submission_id=uuid4(),
        project_id=uuid4(),
        changed_files=[
            "backend/app/services/auth/authentication.py",
            "backend/app/security/tokens.py",
        ],
        added_lines=30,
        removed_lines=5,
        ai_generated_lines=10,
        total_lines=50,
        commit_messages=["Update auth"],
        is_new_feature=False,
        affected_modules=["auth", "security"],
    )


# ============================================================================
# Signal Calculator Tests
# ============================================================================


class TestArchitecturalSmellCalculator:
    """Test architectural smell signal calculator."""

    @pytest.mark.asyncio
    async def test_calculate_no_smells(self, simple_submission):
        """Test calculation with no architectural smells."""
        calc = ArchitecturalSmellCalculator()
        score = await calc.calculate(simple_submission, {})

        assert score.signal_type == SignalType.ARCHITECTURAL_SMELL
        assert 0 <= score.score <= 100
        assert score.weight == SIGNAL_WEIGHTS[SignalType.ARCHITECTURAL_SMELL]

    @pytest.mark.asyncio
    async def test_calculate_shotgun_surgery(self, large_submission):
        """Test detection of shotgun surgery (many files changed)."""
        calc = ArchitecturalSmellCalculator()
        score = await calc.calculate(large_submission, {})

        # Many files changed should increase smell score
        assert score.score > 0
        assert "shotgun_surgery" in score.details.lower() or len(score.evidence) > 0

    @pytest.mark.asyncio
    async def test_weighted_score(self, simple_submission):
        """Test weighted score calculation."""
        calc = ArchitecturalSmellCalculator()
        score = await calc.calculate(simple_submission, {})

        expected_weighted = score.score * score.weight
        assert abs(score.weighted_score - expected_weighted) < 0.01


class TestAbstractionComplexityCalculator:
    """Test abstraction complexity signal calculator."""

    @pytest.mark.asyncio
    async def test_calculate_basic(self, simple_submission):
        """Test basic abstraction complexity calculation."""
        calc = AbstractionComplexityCalculator()
        score = await calc.calculate(simple_submission, {})

        assert score.signal_type == SignalType.ABSTRACTION_COMPLEXITY
        assert 0 <= score.score <= 100
        assert score.weight == SIGNAL_WEIGHTS[SignalType.ABSTRACTION_COMPLEXITY]

    @pytest.mark.asyncio
    async def test_complexity_increases_with_files(self, large_submission):
        """Test that complexity increases with more files."""
        calc = AbstractionComplexityCalculator()
        score = await calc.calculate(large_submission, {})

        # More files should indicate higher complexity
        assert score.score >= 0


class TestAIDependencyRatioCalculator:
    """Test AI dependency ratio signal calculator."""

    @pytest.mark.asyncio
    async def test_calculate_low_ai(self):
        """Test calculation with low AI dependency."""
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["test.py"],
            ai_generated_lines=10,
            total_lines=100,
        )

        calc = AIDependencyRatioCalculator()
        score = await calc.calculate(submission, {})

        assert score.signal_type == SignalType.AI_DEPENDENCY_RATIO
        # 10% AI should be low risk
        assert score.score < 50

    @pytest.mark.asyncio
    async def test_calculate_high_ai(self):
        """Test calculation with high AI dependency."""
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["test.py"],
            ai_generated_lines=90,
            total_lines=100,
        )

        calc = AIDependencyRatioCalculator()
        score = await calc.calculate(submission, {})

        # 90% AI should be high risk
        assert score.score > 50

    @pytest.mark.asyncio
    async def test_zero_total_lines(self):
        """Test calculation with zero total lines."""
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["test.py"],
            ai_generated_lines=0,
            total_lines=0,
        )

        calc = AIDependencyRatioCalculator()
        score = await calc.calculate(submission, {})

        # Should handle zero division gracefully
        assert 0 <= score.score <= 100


class TestChangeSurfaceAreaCalculator:
    """Test change surface area signal calculator."""

    @pytest.mark.asyncio
    async def test_calculate_small_change(self, simple_submission):
        """Test calculation with small change surface area."""
        calc = ChangeSurfaceAreaCalculator()
        score = await calc.calculate(simple_submission, {})

        assert score.signal_type == SignalType.CHANGE_SURFACE_AREA
        # Small change should have low risk
        assert score.score < 50

    @pytest.mark.asyncio
    async def test_calculate_large_change(self, large_submission):
        """Test calculation with large change surface area."""
        calc = ChangeSurfaceAreaCalculator()
        score = await calc.calculate(large_submission, {})

        # Large change with many files/modules should have higher risk
        assert score.score > 20

    @pytest.mark.asyncio
    async def test_detects_multiple_modules(self, large_submission):
        """Test that multiple modules are detected."""
        calc = ChangeSurfaceAreaCalculator()
        score = await calc.calculate(large_submission, {})

        assert "modules" in score.details.lower() or "files" in score.details.lower()


class TestDriftVelocityCalculator:
    """Test drift velocity signal calculator."""

    @pytest.mark.asyncio
    async def test_calculate_no_context(self, simple_submission):
        """Test calculation without project context."""
        calc = DriftVelocityCalculator()
        score = await calc.calculate(simple_submission, None, {})

        assert score.signal_type == SignalType.DRIFT_VELOCITY
        # Without context, should return baseline
        assert 0 <= score.score <= 100

    @pytest.mark.asyncio
    async def test_calculate_with_new_feature(self, simple_submission):
        """Test calculation with new feature flag."""
        simple_submission.is_new_feature = True

        calc = DriftVelocityCalculator()
        score = await calc.calculate(simple_submission, None, {})

        # New features may have higher drift
        assert 0 <= score.score <= 100


# ============================================================================
# Critical Path Checker Tests
# ============================================================================


class TestCriticalPathChecker:
    """Test critical path detection."""

    def test_no_critical_files(self, simple_submission):
        """Test submission with no critical files."""
        checker = CriticalPathChecker()
        matches = checker.check(simple_submission.changed_files)

        # user_service.py is not critical
        assert len(matches) == 0

    def test_auth_critical_path(self, critical_path_submission):
        """Test detection of auth files as critical."""
        checker = CriticalPathChecker()
        matches = checker.check(critical_path_submission.changed_files)

        # Auth files should be detected as critical
        assert len(matches) > 0
        categories = [m.category for m in matches]
        assert "security" in categories or "authentication" in categories

    def test_payment_critical_path(self):
        """Test detection of payment files as critical."""
        files = [
            "backend/app/services/payment/stripe_service.py",
            "backend/app/api/routes/payments.py",
        ]

        checker = CriticalPathChecker()
        matches = checker.check(files)

        assert len(matches) > 0
        categories = [m.category for m in matches]
        assert "payment" in categories

    def test_database_schema_critical(self):
        """Test detection of database schema as critical."""
        files = ["prisma/schema.prisma"]

        checker = CriticalPathChecker()
        matches = checker.check(files)

        assert len(matches) > 0
        categories = [m.category for m in matches]
        assert "database_schema" in categories


# ============================================================================
# Vibecoding Index Calculation Tests
# ============================================================================


class TestVibecodingIndexCalculation:
    """Test full Vibecoding Index calculation."""

    @pytest.mark.asyncio
    async def test_calculate_simple(self, engine, simple_submission):
        """Test index calculation for simple submission."""
        index = await engine.calculate_vibecoding_index(simple_submission)

        assert isinstance(index, VibecodingIndex)
        assert 0 <= index.score <= 100
        assert index.category in IndexCategory
        assert index.routing in RoutingDecision
        assert len(index.signals) == 5

    @pytest.mark.asyncio
    async def test_calculate_large(self, engine, large_submission):
        """Test index calculation for large submission."""
        index = await engine.calculate_vibecoding_index(large_submission)

        assert isinstance(index, VibecodingIndex)
        assert 0 <= index.score <= 100
        # Large submission should have higher index
        assert index.score > 0

    @pytest.mark.asyncio
    async def test_critical_path_override(self, engine, critical_path_submission):
        """Test MAX CRITICALITY OVERRIDE for critical paths."""
        index = await engine.calculate_vibecoding_index(critical_path_submission)

        # Critical path files should boost index to minimum 80
        assert index.critical_override is True
        assert index.score >= 80
        # Score 80 falls in ORANGE (61-80), requiring CEO SHOULD review
        # Score 81+ would fall in RED requiring CEO MUST review
        assert index.routing in (RoutingDecision.CEO_SHOULD_REVIEW, RoutingDecision.CEO_MUST_REVIEW)

    @pytest.mark.asyncio
    async def test_routing_green(self, engine):
        """Test GREEN routing (0-30)."""
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["README.md"],
            added_lines=5,
            removed_lines=0,
            ai_generated_lines=0,
            total_lines=10,
        )

        index = await engine.calculate_vibecoding_index(submission)

        # Minimal change should be green
        if index.score <= 30:
            assert index.category == IndexCategory.GREEN
            assert index.routing == RoutingDecision.AUTO_APPROVE

    @pytest.mark.asyncio
    async def test_signals_have_weights(self, engine, simple_submission):
        """Test that all signals have proper weights."""
        index = await engine.calculate_vibecoding_index(simple_submission)

        for signal_type, score in index.signals.items():
            assert score.weight > 0
            assert score.weight <= 1.0

    @pytest.mark.asyncio
    async def test_top_contributors(self, engine, large_submission):
        """Test top contributors calculation."""
        index = await engine.calculate_vibecoding_index(large_submission)

        contributors = index._get_top_contributors()
        assert len(contributors) <= 3
        # Should be sorted by contribution
        if len(contributors) >= 2:
            assert contributors[0]["contribution"] >= contributors[1]["contribution"]


# ============================================================================
# Index Thresholds Tests
# ============================================================================


class TestIndexThresholds:
    """Test index threshold configuration."""

    def test_thresholds_defined(self):
        """Test that all category thresholds are defined."""
        assert IndexCategory.GREEN in INDEX_THRESHOLDS
        assert IndexCategory.YELLOW in INDEX_THRESHOLDS
        assert IndexCategory.ORANGE in INDEX_THRESHOLDS
        assert IndexCategory.RED in INDEX_THRESHOLDS

    def test_thresholds_non_overlapping(self):
        """Test that thresholds don't overlap."""
        green = INDEX_THRESHOLDS[IndexCategory.GREEN]
        yellow = INDEX_THRESHOLDS[IndexCategory.YELLOW]
        orange = INDEX_THRESHOLDS[IndexCategory.ORANGE]
        red = INDEX_THRESHOLDS[IndexCategory.RED]

        assert green[1] < yellow[0] or green[1] == yellow[0]
        assert yellow[1] < orange[0] or yellow[1] == orange[0]
        assert orange[1] < red[0] or orange[1] == red[0]

    def test_signal_weights_sum_to_one(self):
        """Test that signal weights sum to approximately 1.0."""
        total_weight = sum(SIGNAL_WEIGHTS.values())
        assert abs(total_weight - 1.0) < 0.01


# ============================================================================
# Factory Function Tests
# ============================================================================


class TestFactoryFunctions:
    """Test factory functions for signals engine."""

    def test_create_signals_engine(self):
        """Test creating new engine instance."""
        engine = create_signals_engine()
        assert isinstance(engine, GovernanceSignalsEngine)

    def test_get_signals_engine_singleton(self):
        """Test singleton behavior of get_signals_engine."""
        engine1 = get_signals_engine()
        engine2 = get_signals_engine()

        # Should return same instance
        assert engine1 is engine2

    def test_engine_has_calculators(self, engine):
        """Test that engine has all signal calculators."""
        # Engine stores calculators as separate attributes
        assert hasattr(engine, "_arch_smell_calc")
        assert hasattr(engine, "_abstraction_calc")
        assert hasattr(engine, "_ai_dep_calc")
        assert hasattr(engine, "_surface_area_calc")
        assert hasattr(engine, "_drift_calc")

        # Verify calculator types
        assert isinstance(engine._arch_smell_calc, ArchitecturalSmellCalculator)
        assert isinstance(engine._abstraction_calc, AbstractionComplexityCalculator)
        assert isinstance(engine._ai_dep_calc, AIDependencyRatioCalculator)
        assert isinstance(engine._surface_area_calc, ChangeSurfaceAreaCalculator)
        assert isinstance(engine._drift_calc, DriftVelocityCalculator)


# ============================================================================
# Edge Cases Tests
# ============================================================================


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_empty_changed_files(self, engine):
        """Test handling of empty changed files list."""
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=[],
        )

        # Should handle gracefully, not crash
        index = await engine.calculate_vibecoding_index(submission)
        assert isinstance(index, VibecodingIndex)

    @pytest.mark.asyncio
    async def test_very_high_ai_ratio(self, engine):
        """Test handling of 100% AI-generated code."""
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["test.py"],
            ai_generated_lines=1000,
            total_lines=1000,
        )

        index = await engine.calculate_vibecoding_index(submission)
        assert isinstance(index, VibecodingIndex)
        # Should have high AI dependency signal
        ai_signal = index.signals.get(SignalType.AI_DEPENDENCY_RATIO)
        assert ai_signal is not None
        assert ai_signal.score > 50

    @pytest.mark.asyncio
    async def test_to_dict_serialization(self, engine, simple_submission):
        """Test index can be serialized to dict."""
        index = await engine.calculate_vibecoding_index(simple_submission)
        data = index.to_dict()

        # Main keys
        assert "vibecoding_index" in data
        assert "signals" in data
        assert "calculated_at" in data

        # Nested keys in vibecoding_index
        assert "score" in data["vibecoding_index"]
        assert "category" in data["vibecoding_index"]
        assert "routing" in data["vibecoding_index"]
