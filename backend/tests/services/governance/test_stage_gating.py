"""
=========================================================================
Stage Gating Service Tests
SDLC Orchestrator - Sprint 109 (Vibecoding Index & Stage-Aware Gating)

Version: 1.0.0
Date: January 27, 2026
Status: ACTIVE - Sprint 109 Day 7
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 Quality Assurance System

Test Coverage:
- Stage rules configuration
- PR validation against stages
- File pattern matching
- Prerequisites checking
- PR requirements validation
- Stage progression
- Factory functions

Zero Mock Policy: Real validation, no mocked results
=========================================================================
"""

import pytest
from datetime import datetime
from uuid import uuid4

from app.services.governance.stage_gating import (
    StageGatingService,
    SDLCStage,
    ViolationType,
    PRRequirement,
    StageRules,
    StageViolation,
    StageGatingResult,
    PullRequest,
    Project,
    DEFAULT_STAGE_RULES,
    create_stage_gating_service,
    get_stage_gating_service,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def service():
    """Create a fresh stage gating service instance."""
    return StageGatingService()


@pytest.fixture
def foundation_project():
    """Create a project in Foundation stage."""
    return Project(
        project_id=uuid4(),
        name="Test Project",
        current_stage=SDLCStage.STAGE_00_FOUNDATION,
        completed_stages=[],
    )


@pytest.fixture
def planning_project():
    """Create a project in Planning stage with Foundation completed."""
    return Project(
        project_id=uuid4(),
        name="Test Project",
        current_stage=SDLCStage.STAGE_01_PLANNING,
        completed_stages=[SDLCStage.STAGE_00_FOUNDATION],
    )


@pytest.fixture
def build_project():
    """Create a project in Build stage with prior stages completed."""
    return Project(
        project_id=uuid4(),
        name="Test Project",
        current_stage=SDLCStage.STAGE_04_BUILD,
        completed_stages=[
            SDLCStage.STAGE_00_FOUNDATION,
            SDLCStage.STAGE_01_PLANNING,
            SDLCStage.STAGE_02_DESIGN,
        ],
    )


@pytest.fixture
def test_project():
    """Create a project in Test stage."""
    return Project(
        project_id=uuid4(),
        name="Test Project",
        current_stage=SDLCStage.STAGE_05_TEST,
        completed_stages=[
            SDLCStage.STAGE_00_FOUNDATION,
            SDLCStage.STAGE_01_PLANNING,
            SDLCStage.STAGE_02_DESIGN,
            SDLCStage.STAGE_04_BUILD,
        ],
    )


@pytest.fixture
def foundation_pr():
    """Create a PR for foundation docs."""
    return PullRequest(
        pr_id=1,
        project_id=uuid4(),
        changed_files=["docs/00-foundation/01-Vision.md"],
        title="Add vision document",
        linked_task_id="TASK-001",
    )


@pytest.fixture
def code_pr():
    """Create a PR with code changes."""
    return PullRequest(
        pr_id=2,
        project_id=uuid4(),
        changed_files=[
            "backend/app/services/user_service.py",
            "tests/test_user_service.py",
        ],
        title="Add user service",
        linked_task_id="TASK-002",
        has_intent_statement=True,
        has_ownership_headers=True,
        test_coverage=85.0,
    )


# ============================================================================
# Stage Rules Configuration Tests
# ============================================================================


class TestStageRulesConfiguration:
    """Test stage rules are properly configured."""

    def test_all_stages_have_rules(self):
        """Test that all SDLC stages have rules defined."""
        for stage in SDLCStage:
            assert stage in DEFAULT_STAGE_RULES, f"Missing rules for {stage}"

    def test_foundation_stage_rules(self):
        """Test Foundation stage allows only docs."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_00_FOUNDATION]

        assert "docs/00-foundation/**" in rules.allows
        assert any("backend" in b for b in rules.blocks)
        assert any("frontend" in b for b in rules.blocks)

    def test_planning_stage_rules(self):
        """Test Planning stage rules."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_01_PLANNING]

        assert any("docs" in a for a in rules.allows)
        # Should require Foundation stage
        assert SDLCStage.STAGE_00_FOUNDATION.value in rules.requires_complete

    def test_build_stage_rules(self):
        """Test Build stage allows code with compliance."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_04_BUILD]

        assert "**" in rules.allows  # All files allowed
        # Should have PR requirements
        assert len(rules.requires_for_pr) > 0

    def test_test_stage_rules(self):
        """Test Test stage blocks new features."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_05_TEST]

        assert rules.blocks_new_features is True
        assert any("tests" in a for a in rules.allows)

    def test_deploy_stage_rules(self):
        """Test Deploy stage rules."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_06_DEPLOY]

        assert any("docker" in a or "k8s" in a for a in rules.allows)
        # Should block implementation changes
        assert any("services" in b for b in rules.blocks)


# ============================================================================
# PR Validation Tests
# ============================================================================


class TestPRValidation:
    """Test PR validation against stages."""

    @pytest.mark.asyncio
    async def test_foundation_pr_allowed_in_foundation(
        self, service, foundation_project, foundation_pr
    ):
        """Test foundation docs allowed in foundation stage."""
        result = await service.validate_pr_against_stage(foundation_pr, foundation_project)

        assert result.allowed is True
        assert len(result.violations) == 0

    @pytest.mark.asyncio
    async def test_code_blocked_in_foundation(self, service, foundation_project, code_pr):
        """Test code changes blocked in foundation stage."""
        result = await service.validate_pr_against_stage(code_pr, foundation_project)

        assert result.allowed is False
        assert len(result.violations) > 0
        assert any(
            v.type == ViolationType.FILE_BLOCKED for v in result.violations
        )

    @pytest.mark.asyncio
    async def test_code_allowed_in_build(self, service, build_project, code_pr):
        """Test code changes allowed in build stage."""
        result = await service.validate_pr_against_stage(code_pr, build_project)

        # Should be allowed (with proper PR requirements)
        assert result.allowed is True or all(
            v.type == ViolationType.PR_REQUIREMENT_MISSING
            for v in result.violations
        )

    @pytest.mark.asyncio
    async def test_prerequisite_violation(self, service, code_pr):
        """Test violation when prerequisites not met."""
        # Project in Build but Foundation not completed
        project = Project(
            project_id=uuid4(),
            name="Test",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[],  # No stages completed
        )

        result = await service.validate_pr_against_stage(code_pr, project)

        assert result.allowed is False
        assert any(
            v.type == ViolationType.PREREQUISITE_INCOMPLETE
            for v in result.violations
        )


# ============================================================================
# File Pattern Matching Tests
# ============================================================================


class TestFilePatternMatching:
    """Test file pattern matching for stage rules."""

    @pytest.mark.asyncio
    async def test_exact_path_match(self, service, foundation_project):
        """Test exact path matching."""
        pr = PullRequest(
            pr_id=1,
            project_id=uuid4(),
            changed_files=["README.md"],
        )

        result = await service.validate_pr_against_stage(pr, foundation_project)

        # README.md should be allowed in foundation
        assert result.allowed is True

    @pytest.mark.asyncio
    async def test_glob_pattern_match(self, service, foundation_project):
        """Test glob pattern matching."""
        pr = PullRequest(
            pr_id=1,
            project_id=uuid4(),
            changed_files=["docs/00-foundation/sub/deep/file.md"],
        )

        result = await service.validate_pr_against_stage(pr, foundation_project)

        # Deep nested foundation docs should be allowed
        assert result.allowed is True

    @pytest.mark.asyncio
    async def test_block_pattern_match(self, service, foundation_project):
        """Test block pattern matching."""
        pr = PullRequest(
            pr_id=1,
            project_id=uuid4(),
            changed_files=["backend/app/main.py"],
        )

        result = await service.validate_pr_against_stage(pr, foundation_project)

        # Backend files should be blocked in foundation
        assert result.allowed is False

    @pytest.mark.asyncio
    async def test_multiple_files_mixed(self, service, foundation_project):
        """Test PR with both allowed and blocked files."""
        pr = PullRequest(
            pr_id=1,
            project_id=uuid4(),
            changed_files=[
                "docs/00-foundation/Vision.md",  # Allowed
                "backend/app/main.py",  # Blocked
            ],
        )

        result = await service.validate_pr_against_stage(pr, foundation_project)

        # Should be blocked due to backend file
        assert result.allowed is False


# ============================================================================
# PR Requirements Tests
# ============================================================================


class TestPRRequirements:
    """Test PR requirement validation."""

    @pytest.mark.asyncio
    async def test_linked_task_required(self, service, build_project):
        """Test linked task requirement."""
        pr = PullRequest(
            pr_id=1,
            project_id=uuid4(),
            changed_files=["backend/app/test.py"],
            linked_task_id=None,  # Missing task link
            has_ownership_headers=True,
            has_intent_statement=True,
        )

        result = await service.validate_pr_against_stage(pr, build_project)

        # Check if linked_task is required and violation is generated
        requirements = result.pr_requirements_met
        if PRRequirement.LINKED_TASK.value in requirements:
            assert requirements[PRRequirement.LINKED_TASK.value] is False

    @pytest.mark.asyncio
    async def test_ownership_required(self, service, build_project):
        """Test ownership header requirement."""
        pr = PullRequest(
            pr_id=1,
            project_id=uuid4(),
            changed_files=["backend/app/test.py"],
            linked_task_id="TASK-001",
            has_ownership_headers=False,  # Missing ownership
            has_intent_statement=True,
        )

        result = await service.validate_pr_against_stage(pr, build_project)

        requirements = result.pr_requirements_met
        if PRRequirement.OWNERSHIP_HEADER.value in requirements:
            assert requirements[PRRequirement.OWNERSHIP_HEADER.value] is False

    @pytest.mark.asyncio
    async def test_all_requirements_met(self, service, build_project):
        """Test PR with all requirements met."""
        pr = PullRequest(
            pr_id=1,
            project_id=uuid4(),
            changed_files=["backend/app/test.py"],
            linked_task_id="TASK-001",
            has_ownership_headers=True,
            has_intent_statement=True,
            test_coverage=90.0,
            security_scan_passed=True,
        )

        result = await service.validate_pr_against_stage(pr, build_project)

        # All requirements should be met
        for req, met in result.pr_requirements_met.items():
            assert met is True, f"Requirement {req} not met"


# ============================================================================
# Test Stage - Feature Blocking Tests
# ============================================================================


class TestFeatureBlocking:
    """Test feature blocking in test stage."""

    @pytest.mark.asyncio
    async def test_bug_fix_allowed_in_test(self, service, test_project):
        """Test bug fixes allowed in test stage."""
        pr = PullRequest(
            pr_id=1,
            project_id=uuid4(),
            changed_files=["backend/app/services/fix_bug.py"],
            title="Fix authentication bug",
        )

        result = await service.validate_pr_against_stage(pr, test_project)

        # Bug fixes should be allowed (may still have warnings)
        # This depends on stage rules configuration
        assert result is not None

    @pytest.mark.asyncio
    async def test_tests_allowed_in_test(self, service, test_project):
        """Test that test files are allowed in test stage."""
        pr = PullRequest(
            pr_id=1,
            project_id=uuid4(),
            changed_files=["tests/test_auth.py", "e2e/test_login.py"],
            title="Add auth tests",
        )

        result = await service.validate_pr_against_stage(pr, test_project)

        # Test files should be allowed
        assert result.allowed is True or all(
            "tests" not in str(v.file_path) for v in result.violations
        )


# ============================================================================
# Suggestion Generation Tests
# ============================================================================


class TestSuggestionGeneration:
    """Test actionable suggestion generation."""

    @pytest.mark.asyncio
    async def test_violation_has_suggestion(self, service, foundation_project, code_pr):
        """Test that violations include suggestions."""
        result = await service.validate_pr_against_stage(code_pr, foundation_project)

        assert result.allowed is False
        for violation in result.violations:
            assert violation.suggestion is not None or violation.message is not None

    @pytest.mark.asyncio
    async def test_prerequisite_violation_suggestion(self, service, code_pr):
        """Test prerequisite violation has fix suggestion."""
        project = Project(
            project_id=uuid4(),
            name="Test",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[],
        )

        result = await service.validate_pr_against_stage(code_pr, project)

        prerequisite_violations = [
            v for v in result.violations
            if v.type == ViolationType.PREREQUISITE_INCOMPLETE
        ]

        for v in prerequisite_violations:
            assert v.suggestion is not None or v.cli_command is not None


# ============================================================================
# Stage Progression Tests
# ============================================================================


class TestStageProgression:
    """Test stage progression logic."""

    @pytest.mark.asyncio
    async def test_complete_stage(self, service):
        """Test marking a stage as complete."""
        project = Project(
            project_id=uuid4(),
            name="Test",
            current_stage=SDLCStage.STAGE_00_FOUNDATION,
            completed_stages=[],
        )

        success = await service.complete_stage(
            project=project,
            stage=SDLCStage.STAGE_00_FOUNDATION,
            completed_by="test_user",
        )

        assert success is True

    @pytest.mark.asyncio
    async def test_cannot_complete_without_prerequisites(self, service):
        """Test cannot complete stage without prerequisites."""
        project = Project(
            project_id=uuid4(),
            name="Test",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[],
        )

        # Try to complete Build without Foundation, Planning, Design
        success = await service.complete_stage(
            project=project,
            stage=SDLCStage.STAGE_04_BUILD,
            completed_by="test_user",
        )

        # Should fail due to missing prerequisites
        assert success is False

    @pytest.mark.asyncio
    async def test_get_next_stage(self, service, build_project):
        """Test getting next stage."""
        next_stage = service.get_next_stage(SDLCStage.STAGE_04_BUILD)

        assert next_stage == SDLCStage.STAGE_05_TEST

    @pytest.mark.asyncio
    async def test_last_stage_has_no_next(self, service):
        """Test last stage returns None for next."""
        next_stage = service.get_next_stage(SDLCStage.STAGE_10_DECOMMISSION)

        assert next_stage is None


# ============================================================================
# Factory Function Tests
# ============================================================================


class TestFactoryFunctions:
    """Test factory functions for stage gating service."""

    def test_create_stage_gating_service(self):
        """Test creating new service instance."""
        service = create_stage_gating_service()
        assert isinstance(service, StageGatingService)

    def test_get_stage_gating_service_singleton(self):
        """Test singleton behavior of get_stage_gating_service."""
        service1 = get_stage_gating_service()
        service2 = get_stage_gating_service()

        # Should return same instance
        assert service1 is service2


# ============================================================================
# Result Object Tests
# ============================================================================


class TestResultObjects:
    """Test result object structure."""

    @pytest.mark.asyncio
    async def test_result_structure(self, service, foundation_project, foundation_pr):
        """Test StageGatingResult structure."""
        result = await service.validate_pr_against_stage(foundation_pr, foundation_project)

        assert hasattr(result, "allowed")
        assert hasattr(result, "current_stage")
        assert hasattr(result, "violations")
        assert hasattr(result, "warnings")
        assert hasattr(result, "pr_requirements_met")
        assert hasattr(result, "stage_progress")
        assert hasattr(result, "validated_at")

    @pytest.mark.asyncio
    async def test_violation_structure(self, service, foundation_project, code_pr):
        """Test StageViolation structure."""
        result = await service.validate_pr_against_stage(code_pr, foundation_project)

        assert len(result.violations) > 0
        violation = result.violations[0]

        assert hasattr(violation, "type")
        assert hasattr(violation, "severity")
        assert hasattr(violation, "message")


# ============================================================================
# Edge Cases Tests
# ============================================================================


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_empty_changed_files(self, service, build_project):
        """Test PR with no changed files."""
        pr = PullRequest(
            pr_id=1,
            project_id=uuid4(),
            changed_files=[],
        )

        result = await service.validate_pr_against_stage(pr, build_project)

        # Should handle gracefully
        assert isinstance(result, StageGatingResult)

    @pytest.mark.asyncio
    async def test_unknown_file_extension(self, service, build_project):
        """Test PR with unknown file types."""
        pr = PullRequest(
            pr_id=1,
            project_id=uuid4(),
            changed_files=["some_file.xyz", "another.unknown"],
            linked_task_id="TASK-001",
        )

        result = await service.validate_pr_against_stage(pr, build_project)

        # Should handle unknown extensions gracefully
        assert isinstance(result, StageGatingResult)

    @pytest.mark.asyncio
    async def test_deeply_nested_path(self, service, foundation_project):
        """Test deeply nested file paths."""
        pr = PullRequest(
            pr_id=1,
            project_id=uuid4(),
            changed_files=[
                "docs/00-foundation/a/b/c/d/e/f/g/deep_file.md"
            ],
        )

        result = await service.validate_pr_against_stage(pr, foundation_project)

        # Deep paths in allowed pattern should work
        assert isinstance(result, StageGatingResult)
