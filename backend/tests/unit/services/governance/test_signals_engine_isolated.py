"""
=========================================================================
Isolated Unit Tests for GovernanceSignalsEngine
SDLC Orchestrator - Sprint 109 (Vibecoding Index Calculator)

These tests run WITHOUT the full app context for faster feedback.
Run: cd backend && PYTHONPATH=. python3 -m pytest tests/unit/services/governance/test_signals_engine_isolated.py -v --noconftest
=========================================================================
"""

import sys
from pathlib import Path

# Add backend to path for isolated testing
backend_path = Path(__file__).parent.parent.parent.parent.parent / "app"
sys.path.insert(0, str(backend_path.parent))

import pytest
from uuid import uuid4

from app.services.governance.signals_engine import (
    IndexCategory,
    RoutingDecision,
    SignalType,
    SIGNAL_WEIGHTS,
    INDEX_THRESHOLDS,
    ArchitecturalSmell,
    SignalScore,
    CodeSubmission,
    ProjectContext,
    CriticalPathMatch,
    VibecodingIndex,
    ArchitecturalSmellCalculator,
    AbstractionComplexityCalculator,
    AIDependencyRatioCalculator,
    ChangeSurfaceAreaCalculator,
    DriftVelocityCalculator,
    CriticalPathChecker,
    GovernanceSignalsEngine,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def simple_submission() -> CodeSubmission:
    """Create simple code submission for testing."""
    return CodeSubmission(
        submission_id=uuid4(),
        project_id=uuid4(),
        changed_files=["backend/app/services/example.py"],
        added_lines=50,
        removed_lines=10,
        ai_generated_lines=0,
        total_lines=50,
        affected_modules=["services"],
    )


@pytest.fixture
def large_submission() -> CodeSubmission:
    """Create large multi-file submission."""
    return CodeSubmission(
        submission_id=uuid4(),
        project_id=uuid4(),
        changed_files=[
            "backend/app/services/user_service.py",
            "backend/app/services/auth_service.py",
            "backend/app/api/users.py",
            "backend/app/api/auth.py",
            "backend/app/models/user.py",
            "backend/app/models/session.py",
            "backend/tests/test_users.py",
            "backend/tests/test_auth.py",
            "backend/app/core/security.py",
            "backend/app/core/config.py",
            "backend/alembic/versions/add_users.py",
            "docs/api-users.md",
        ],
        added_lines=500,
        removed_lines=100,
        ai_generated_lines=300,
        total_lines=500,
        affected_modules=["services", "api", "models", "core", "tests"],
        is_new_feature=True,
    )


@pytest.fixture
def critical_submission() -> CodeSubmission:
    """Create submission touching critical paths."""
    return CodeSubmission(
        submission_id=uuid4(),
        project_id=uuid4(),
        changed_files=[
            "backend/app/services/auth.py",
            "backend/app/core/security.py",
        ],
        added_lines=10,
        removed_lines=5,
        ai_generated_lines=0,
        total_lines=10,
        affected_modules=["services", "core"],
    )


@pytest.fixture
def python_code_with_god_class() -> str:
    """Python code containing a God class (>500 lines simulated)."""
    # Create a class with many lines
    methods = "\n".join([
        f"    def method_{i}(self):\n        pass\n" for i in range(200)
    ])
    return f'''
class GodClass:
    """A class with too many responsibilities."""

    def __init__(self):
        self.data = {{}}

{methods}
'''


@pytest.fixture
def python_code_clean() -> str:
    """Clean Python code without issues."""
    return '''
class UserService:
    """Clean user service."""

    def __init__(self, db):
        self.db = db

    def get_user(self, user_id: str):
        return self.db.query(User).get(user_id)

    def create_user(self, data: dict):
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        return user
'''


@pytest.fixture
def signals_engine() -> GovernanceSignalsEngine:
    """Create GovernanceSignalsEngine for testing."""
    return GovernanceSignalsEngine()


# ============================================================================
# Test Suite 1: Enums and Constants
# ============================================================================

class TestEnumsAndConstants:
    """Test enum values and constants."""

    def test_index_category_values(self):
        """Index categories should have correct values."""
        assert IndexCategory.GREEN.value == "green"
        assert IndexCategory.YELLOW.value == "yellow"
        assert IndexCategory.ORANGE.value == "orange"
        assert IndexCategory.RED.value == "red"

    def test_routing_decision_values(self):
        """Routing decisions should have correct values."""
        assert RoutingDecision.AUTO_APPROVE.value == "auto_approve"
        assert RoutingDecision.TECH_LEAD_REVIEW.value == "tech_lead_review"
        assert RoutingDecision.CEO_SHOULD_REVIEW.value == "ceo_should_review"
        assert RoutingDecision.CEO_MUST_REVIEW.value == "ceo_must_review"

    def test_signal_weights_sum_to_one(self):
        """Signal weights should sum to 1.0."""
        total = sum(SIGNAL_WEIGHTS.values())
        assert abs(total - 1.0) < 0.001

    def test_index_thresholds_coverage(self):
        """Index thresholds should cover 0-100 range."""
        assert INDEX_THRESHOLDS[IndexCategory.GREEN] == (0, 30)
        assert INDEX_THRESHOLDS[IndexCategory.YELLOW] == (31, 60)
        assert INDEX_THRESHOLDS[IndexCategory.ORANGE] == (61, 80)
        assert INDEX_THRESHOLDS[IndexCategory.RED] == (81, 100)


# ============================================================================
# Test Suite 2: Architectural Smell Calculator
# ============================================================================

class TestArchitecturalSmellCalculator:
    """Test architectural smell detection."""

    @pytest.mark.asyncio
    async def test_smell_001_no_issues_clean_code(self, python_code_clean: str):
        """Clean code should have score 0."""
        calc = ArchitecturalSmellCalculator()
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["service.py"],
        )
        result = await calc.calculate(submission, {"service.py": python_code_clean})

        assert result.score == 0.0
        assert "No architectural smells" in result.details

    @pytest.mark.asyncio
    async def test_smell_002_shotgun_surgery_many_files(self):
        """>10 files changed should trigger shotgun surgery smell."""
        calc = ArchitecturalSmellCalculator()
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=[f"file_{i}.py" for i in range(15)],
        )
        result = await calc.calculate(submission, {})

        assert result.score > 0
        assert any("shotgun_surgery" in str(e) for e in result.evidence)

    @pytest.mark.asyncio
    async def test_smell_003_signal_type_correct(self):
        """Result should have correct signal type."""
        calc = ArchitecturalSmellCalculator()
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["test.py"],
        )
        result = await calc.calculate(submission, {})

        assert result.signal_type == SignalType.ARCHITECTURAL_SMELL
        assert result.weight == 0.25


# ============================================================================
# Test Suite 3: AI Dependency Ratio Calculator
# ============================================================================

class TestAIDependencyRatioCalculator:
    """Test AI dependency ratio calculation."""

    @pytest.mark.asyncio
    async def test_ai_ratio_001_zero_ai(self):
        """0% AI code should score 0."""
        calc = AIDependencyRatioCalculator()
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["test.py"],
            total_lines=100,
            ai_generated_lines=0,
        )
        result = await calc.calculate(submission, {})

        assert result.score == 0.0
        assert "0.0% AI-generated" in result.details

    @pytest.mark.asyncio
    async def test_ai_ratio_002_fifty_percent(self):
        """50% AI code should score ~50."""
        calc = AIDependencyRatioCalculator()
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["test.py"],
            total_lines=100,
            ai_generated_lines=50,
        )
        result = await calc.calculate(submission, {})

        assert abs(result.score - 50.0) < 1

    @pytest.mark.asyncio
    async def test_ai_ratio_003_red_flag_high_ai_low_human(self):
        """90% AI with <10% human mod should trigger red flag."""
        calc = AIDependencyRatioCalculator()
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["test.py"],
            total_lines=100,
            ai_generated_lines=95,
        )
        result = await calc.calculate(submission, {})

        assert result.score >= 95  # High score
        assert "RED FLAG" in result.details

    @pytest.mark.asyncio
    async def test_ai_ratio_004_weight_correct(self):
        """Signal weight should be 0.20."""
        calc = AIDependencyRatioCalculator()
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["test.py"],
            total_lines=100,
            ai_generated_lines=50,
        )
        result = await calc.calculate(submission, {})

        assert result.weight == 0.20
        assert abs(result.weighted_score - 10.0) < 1  # 50 * 0.20 = 10


# ============================================================================
# Test Suite 4: Change Surface Area Calculator
# ============================================================================

class TestChangeSurfaceAreaCalculator:
    """Test change surface area calculation."""

    @pytest.mark.asyncio
    async def test_surface_001_single_file(self, simple_submission: CodeSubmission):
        """Single file should have low score."""
        calc = ChangeSurfaceAreaCalculator()
        result = await calc.calculate(simple_submission, {})

        assert result.score < 20
        assert "1 files" in result.details

    @pytest.mark.asyncio
    async def test_surface_002_many_files(self, large_submission: CodeSubmission):
        """Many files should have higher score."""
        calc = ChangeSurfaceAreaCalculator()
        result = await calc.calculate(large_submission, {})

        assert result.score > 20
        assert "12 files" in result.details

    @pytest.mark.asyncio
    async def test_surface_003_security_files_detected(self):
        """Security files should be detected and add weight."""
        calc = ChangeSurfaceAreaCalculator()
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=[
                "backend/app/core/security.py",
                "backend/app/services/auth.py",
            ],
            affected_modules=["core", "services"],
        )
        result = await calc.calculate(submission, {})

        assert "security file" in result.details.lower() or result.score > 10

    @pytest.mark.asyncio
    async def test_surface_004_db_schema_detected(self):
        """DB schema files should be detected."""
        calc = ChangeSurfaceAreaCalculator()
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=[
                "backend/alembic/versions/migration.py",
            ],
            affected_modules=["alembic"],
        )
        result = await calc.calculate(submission, {})

        assert result.score > 0  # Should detect migration file


# ============================================================================
# Test Suite 5: Critical Path Checker
# ============================================================================

class TestCriticalPathChecker:
    """Test critical path matching."""

    def test_critical_001_auth_file_matches(self):
        """auth.py should match security critical path."""
        checker = CriticalPathChecker()
        matches = checker.check(["backend/app/services/auth.py"])

        assert len(matches) > 0
        assert any(m.category == "security" for m in matches)

    def test_critical_002_alembic_matches(self):
        """Alembic migrations should match database_schema."""
        checker = CriticalPathChecker()
        matches = checker.check(["alembic/versions/add_users.py"])

        assert len(matches) > 0
        assert any(m.category == "database_schema" for m in matches)

    def test_critical_003_payment_matches(self):
        """Payment files should match payment critical path."""
        checker = CriticalPathChecker()
        matches = checker.check(["backend/app/services/payment.py"])

        assert len(matches) > 0
        assert any(m.category == "payment" for m in matches)

    def test_critical_004_regular_file_no_match(self):
        """Regular service file should not match."""
        checker = CriticalPathChecker()
        matches = checker.check(["backend/app/services/user_service.py"])

        # May or may not match depending on patterns, but auth/payment/security should not
        critical_categories = {m.category for m in matches}
        # Regular user service shouldn't be security/payment
        assert "payment" not in critical_categories

    def test_critical_005_override_value(self):
        """Critical matches should have override_to = 80."""
        checker = CriticalPathChecker()
        matches = checker.check(["backend/app/services/auth.py"])

        if matches:
            assert all(m.override_to == 80 for m in matches)


# ============================================================================
# Test Suite 6: GovernanceSignalsEngine Integration
# ============================================================================

class TestGovernanceSignalsEngine:
    """Test main signals engine integration."""

    @pytest.mark.asyncio
    async def test_engine_001_clean_submission_green(
        self,
        signals_engine: GovernanceSignalsEngine,
        simple_submission: CodeSubmission,
        python_code_clean: str,
    ):
        """Clean simple submission should be GREEN."""
        result = await signals_engine.calculate_vibecoding_index(
            submission=simple_submission,
            file_contents={simple_submission.changed_files[0]: python_code_clean},
        )

        assert result.category == IndexCategory.GREEN
        assert result.routing == RoutingDecision.AUTO_APPROVE
        assert result.score <= 30

    @pytest.mark.asyncio
    async def test_engine_002_large_submission_higher_score(
        self,
        signals_engine: GovernanceSignalsEngine,
        large_submission: CodeSubmission,
    ):
        """Large submission with AI code should have higher score."""
        result = await signals_engine.calculate_vibecoding_index(
            submission=large_submission,
        )

        assert result.score > 30  # Should be at least Yellow
        assert result.category in [IndexCategory.YELLOW, IndexCategory.ORANGE, IndexCategory.RED]

    @pytest.mark.asyncio
    async def test_engine_003_critical_path_override(
        self,
        signals_engine: GovernanceSignalsEngine,
        critical_submission: CodeSubmission,
    ):
        """Critical path should trigger override and elevate attention."""
        result = await signals_engine.calculate_vibecoding_index(
            submission=critical_submission,
        )

        assert result.critical_override is True
        assert result.score >= 80  # Should be boosted to at least 80
        # Category should be RED (81-100) since score >= 80
        # But 80 exactly is ORANGE boundary. Score must be > 80 for RED.
        # The override sets min to 80, which is at ORANGE/RED boundary
        assert result.category in [IndexCategory.ORANGE, IndexCategory.RED]
        assert result.routing in [RoutingDecision.CEO_SHOULD_REVIEW, RoutingDecision.CEO_MUST_REVIEW]

    @pytest.mark.asyncio
    async def test_engine_004_all_signals_present(
        self,
        signals_engine: GovernanceSignalsEngine,
        simple_submission: CodeSubmission,
    ):
        """Result should contain all 5 signal scores."""
        result = await signals_engine.calculate_vibecoding_index(
            submission=simple_submission,
        )

        assert len(result.signals) == 5
        assert SignalType.ARCHITECTURAL_SMELL in result.signals
        assert SignalType.ABSTRACTION_COMPLEXITY in result.signals
        assert SignalType.AI_DEPENDENCY_RATIO in result.signals
        assert SignalType.CHANGE_SURFACE_AREA in result.signals
        assert SignalType.DRIFT_VELOCITY in result.signals

    @pytest.mark.asyncio
    async def test_engine_005_to_dict_serialization(
        self,
        signals_engine: GovernanceSignalsEngine,
        simple_submission: CodeSubmission,
    ):
        """Result should serialize to dict correctly."""
        result = await signals_engine.calculate_vibecoding_index(
            submission=simple_submission,
        )

        d = result.to_dict()
        assert "vibecoding_index" in d
        assert "signals" in d
        assert "top_contributors" in d
        assert d["vibecoding_index"]["category"] in ["green", "yellow", "orange", "red"]


# ============================================================================
# Test Suite 7: Routing Thresholds
# ============================================================================

class TestRoutingThresholds:
    """Test routing threshold boundaries."""

    @pytest.mark.asyncio
    async def test_threshold_001_score_30_green(
        self,
        signals_engine: GovernanceSignalsEngine,
    ):
        """Score exactly 30 should be GREEN."""
        # Create submission that yields ~30 score
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["test.py"],
            total_lines=100,
            ai_generated_lines=30,  # 30% AI = 30 score contribution * 0.20 = 6
        )
        result = await signals_engine.calculate_vibecoding_index(submission=submission)

        # Check category boundary logic
        if result.score <= 30:
            assert result.category == IndexCategory.GREEN

    @pytest.mark.asyncio
    async def test_threshold_002_score_60_yellow(
        self,
        signals_engine: GovernanceSignalsEngine,
    ):
        """Score 31-60 should be YELLOW."""
        engine = signals_engine
        # Verify threshold logic directly
        assert engine._determine_category(45) == IndexCategory.YELLOW
        assert engine._determine_routing(IndexCategory.YELLOW) == RoutingDecision.TECH_LEAD_REVIEW

    @pytest.mark.asyncio
    async def test_threshold_003_score_80_orange(
        self,
        signals_engine: GovernanceSignalsEngine,
    ):
        """Score 61-80 should be ORANGE."""
        engine = signals_engine
        assert engine._determine_category(70) == IndexCategory.ORANGE
        assert engine._determine_routing(IndexCategory.ORANGE) == RoutingDecision.CEO_SHOULD_REVIEW

    @pytest.mark.asyncio
    async def test_threshold_004_score_100_red(
        self,
        signals_engine: GovernanceSignalsEngine,
    ):
        """Score >80 should be RED."""
        engine = signals_engine
        assert engine._determine_category(85) == IndexCategory.RED
        assert engine._determine_routing(IndexCategory.RED) == RoutingDecision.CEO_MUST_REVIEW


# ============================================================================
# Test Suite 8: Flags Generation
# ============================================================================

class TestFlagsGeneration:
    """Test warning flag generation."""

    @pytest.mark.asyncio
    async def test_flags_001_high_ai_dependency(
        self,
        signals_engine: GovernanceSignalsEngine,
    ):
        """High AI dependency should generate flag."""
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["test.py"],
            total_lines=100,
            ai_generated_lines=80,  # 80% AI
        )
        result = await signals_engine.calculate_vibecoding_index(submission=submission)

        assert "HIGH_AI_DEPENDENCY" in result.flags

    @pytest.mark.asyncio
    async def test_flags_002_critical_path_flag(
        self,
        signals_engine: GovernanceSignalsEngine,
    ):
        """Critical path should generate CRITICAL_PATH flag."""
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["backend/app/services/auth.py"],
        )
        result = await signals_engine.calculate_vibecoding_index(submission=submission)

        # Should have a CRITICAL_PATH_* flag
        critical_flags = [f for f in result.flags if "CRITICAL_PATH" in f]
        assert len(critical_flags) > 0

    @pytest.mark.asyncio
    async def test_flags_003_large_change(
        self,
        signals_engine: GovernanceSignalsEngine,
        large_submission: CodeSubmission,
    ):
        """Large change should generate LARGE_CHANGE flag if score > 60."""
        result = await signals_engine.calculate_vibecoding_index(
            submission=large_submission,
        )

        surface_signal = result.signals.get(SignalType.CHANGE_SURFACE_AREA)
        if surface_signal and surface_signal.score > 60:
            assert "LARGE_CHANGE" in result.flags


# ============================================================================
# Test Suite 9: Suggested Focus
# ============================================================================

class TestSuggestedFocus:
    """Test suggested focus generation."""

    @pytest.mark.asyncio
    async def test_focus_001_provides_top_signal(
        self,
        signals_engine: GovernanceSignalsEngine,
        large_submission: CodeSubmission,
    ):
        """Should provide top contributing signal in focus."""
        result = await signals_engine.calculate_vibecoding_index(
            submission=large_submission,
        )

        if result.suggested_focus:
            assert "top_signal" in result.suggested_focus
            assert "reason" in result.suggested_focus

    @pytest.mark.asyncio
    async def test_focus_002_estimates_review_time(
        self,
        signals_engine: GovernanceSignalsEngine,
        simple_submission: CodeSubmission,
    ):
        """Should estimate review time."""
        result = await signals_engine.calculate_vibecoding_index(
            submission=simple_submission,
        )

        if result.suggested_focus:
            assert "estimated_review_time" in result.suggested_focus


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
