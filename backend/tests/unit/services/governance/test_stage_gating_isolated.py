"""
=========================================================================
Unit Tests for StageGatingService
SDLC Orchestrator - Sprint 109 (Vibecoding Index & Stage-Aware Gating)

Version: 1.0.0
Date: January 28, 2026
Status: ACTIVE - Unit Test Coverage
Authority: CTO Directive (P2-P3 Priority)
Framework: SDLC 5.3.0 Quality Assurance System

Coverage Target: 95%+ for stage_gating.py

Test Categories:
1. Enums & Constants (10 tests)
2. Data Classes (10 tests)
3. File Pattern Matching (10 tests)
4. Prerequisite Checking (8 tests)
5. PR Requirements (10 tests)
6. Stage Validation (12 tests)
7. Stage Management (8 tests)
8. Edge Cases (6 tests)

Total: 74 tests

Zero Mock Policy: Real pattern matching, real validation logic
=========================================================================
"""

import pytest
from dataclasses import asdict
from datetime import datetime
from typing import List
from uuid import uuid4

# Import directly from the module to test
import sys
sys.path.insert(0, "/home/nqh/shared/SDLC-Orchestrator/backend")

from app.services.governance.stage_gating import (
    SDLCStage,
    ViolationType,
    PRRequirement,
    StageViolation,
    StageRules,
    StageGatingResult,
    PullRequest,
    Project,
    StageGatingService,
    DEFAULT_STAGE_RULES,
    create_stage_gating_service,
    get_stage_gating_service,
)


# ============================================================================
# CATEGORY 1: Enums & Constants
# ============================================================================


class TestEnums:
    """Test enum definitions and constants."""

    def test_enum_001_sdlc_stage_all_values(self):
        """SDLCStage has all 11 stages (00-10)."""
        assert len(SDLCStage) == 11
        assert SDLCStage.STAGE_00_FOUNDATION.value == "stage_00_foundation"
        assert SDLCStage.STAGE_10_EVOLVE.value == "stage_10_evolve"

    def test_enum_002_sdlc_stage_ordering(self):
        """SDLCStage values follow logical progression."""
        stages = list(SDLCStage)
        assert stages[0] == SDLCStage.STAGE_00_FOUNDATION
        assert stages[4] == SDLCStage.STAGE_04_BUILD
        assert stages[10] == SDLCStage.STAGE_10_EVOLVE

    def test_enum_003_violation_types_complete(self):
        """ViolationType has all expected values."""
        assert ViolationType.FILE_BLOCKED.value == "file_blocked"
        assert ViolationType.PREREQUISITE_INCOMPLETE.value == "prerequisite_incomplete"
        assert ViolationType.PR_REQUIREMENT_MISSING.value == "pr_requirement_missing"
        assert ViolationType.STAGE_TRANSITION_INVALID.value == "stage_transition_invalid"

    def test_enum_004_pr_requirements_complete(self):
        """PRRequirement has all 7 requirements."""
        assert len(PRRequirement) == 7
        assert PRRequirement.LINKED_TASK.value == "linked_task"
        assert PRRequirement.TEST_COVERAGE_80.value == "test_coverage_80"
        assert PRRequirement.SECURITY_SCAN_PASS.value == "security_scan_pass"

    def test_enum_005_default_rules_all_stages(self):
        """DEFAULT_STAGE_RULES covers all stages."""
        for stage in SDLCStage:
            assert stage in DEFAULT_STAGE_RULES

    def test_enum_006_stage_00_blocks_code(self):
        """Stage 00 blocks src/backend/frontend code."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_00_FOUNDATION]
        assert "src/**" in rules.blocks
        assert "backend/**" in rules.blocks
        assert "frontend/**" in rules.blocks

    def test_enum_007_stage_04_allows_all(self):
        """Stage 04 (BUILD) allows all code."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_04_BUILD]
        assert "**" in rules.allows
        assert len(rules.blocks) == 0

    def test_enum_008_stage_04_requires_pr_items(self):
        """Stage 04 requires PR compliance items."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_04_BUILD]
        assert PRRequirement.LINKED_TASK in rules.requires_for_pr
        assert PRRequirement.OWNERSHIP_HEADER in rules.requires_for_pr
        assert PRRequirement.INTENT_STATEMENT in rules.requires_for_pr
        assert PRRequirement.TEST_COVERAGE_80 in rules.requires_for_pr

    def test_enum_009_stage_05_blocks_new_features(self):
        """Stage 05 (TEST) blocks new features."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_05_TEST]
        assert rules.blocks_new_features is True

    def test_enum_010_stage_06_requires_security_scan(self):
        """Stage 06 (DEPLOY) requires security scan pass."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_06_DEPLOY]
        assert PRRequirement.SECURITY_SCAN_PASS in rules.requires_for_pr


# ============================================================================
# CATEGORY 2: Data Classes
# ============================================================================


class TestDataClasses:
    """Test data class structures and conversions."""

    def test_data_001_stage_violation_to_dict(self):
        """StageViolation converts to dictionary correctly."""
        violation = StageViolation(
            type=ViolationType.FILE_BLOCKED,
            severity="error",
            message="Test violation",
            file_path="backend/app/test.py",
            current_stage="stage_00_foundation",
            required_stage="stage_04_build",
        )
        d = violation.to_dict()
        assert d["type"] == "file_blocked"
        assert d["severity"] == "error"
        assert d["file_path"] == "backend/app/test.py"

    def test_data_002_stage_rules_fields(self):
        """StageRules has all required fields."""
        rules = StageRules(
            stage=SDLCStage.STAGE_04_BUILD,
            allows=["**"],
            blocks=[],
            requires_complete=["stage_02_design"],
            requires_for_pr=[PRRequirement.LINKED_TASK],
            message="Build stage",
        )
        assert rules.stage == SDLCStage.STAGE_04_BUILD
        assert rules.blocks_new_features is False

    def test_data_003_stage_gating_result_to_dict(self):
        """StageGatingResult converts to dictionary correctly."""
        result = StageGatingResult(
            allowed=True,
            current_stage=SDLCStage.STAGE_04_BUILD,
            violations=[],
            warnings=[],
            pr_requirements_met={"linked_task": True},
        )
        d = result.to_dict()
        assert d["allowed"] is True
        assert d["current_stage"] == "stage_04_build"
        assert d["violations_count"] == 0

    def test_data_004_pull_request_defaults(self):
        """PullRequest has correct defaults."""
        pr = PullRequest(
            pr_id=123,
            project_id=uuid4(),
            changed_files=["file1.py", "file2.py"],
        )
        assert pr.pr_id == 123
        assert pr.linked_task_id is None
        assert pr.has_intent_statement is False
        assert pr.adr_references == []

    def test_data_005_project_defaults(self):
        """Project has correct defaults."""
        project = Project(
            project_id=uuid4(),
            name="Test Project",
            current_stage=SDLCStage.STAGE_04_BUILD,
        )
        assert project.completed_stages == []
        assert project.stage_started_at is None

    def test_data_006_violation_with_cli_command(self):
        """StageViolation includes CLI command suggestion."""
        violation = StageViolation(
            type=ViolationType.PR_REQUIREMENT_MISSING,
            severity="error",
            message="Missing linked task",
            requirement="linked_task",
            cli_command="sdlcctl pr link-task --pr 123",
        )
        d = violation.to_dict()
        assert d["cli_command"] == "sdlcctl pr link-task --pr 123"

    def test_data_007_result_with_stage_progress(self):
        """StageGatingResult includes stage progress."""
        result = StageGatingResult(
            allowed=True,
            current_stage=SDLCStage.STAGE_04_BUILD,
            violations=[],
            warnings=[],
            pr_requirements_met={},
            stage_progress={
                "stage_00_foundation": True,
                "stage_01_planning": True,
                "stage_02_design": True,
                "stage_04_build": False,
            },
        )
        d = result.to_dict()
        assert d["stage_progress"]["stage_00_foundation"] is True
        assert d["stage_progress"]["stage_04_build"] is False

    def test_data_008_result_includes_timestamp(self):
        """StageGatingResult includes validation timestamp."""
        result = StageGatingResult(
            allowed=True,
            current_stage=SDLCStage.STAGE_04_BUILD,
            violations=[],
            warnings=[],
            pr_requirements_met={},
        )
        d = result.to_dict()
        assert "validated_at" in d
        assert isinstance(d["validated_at"], str)

    def test_data_009_pr_with_full_compliance(self):
        """PullRequest with full compliance data."""
        pr = PullRequest(
            pr_id=456,
            project_id=uuid4(),
            changed_files=["backend/app/service.py"],
            linked_task_id="TASK-123",
            has_intent_statement=True,
            has_ownership_headers=True,
            test_coverage=85.0,
            adr_references=["ADR-001"],
            design_doc_path="docs/design.md",
            security_scan_passed=True,
        )
        assert pr.linked_task_id == "TASK-123"
        assert pr.test_coverage == 85.0

    def test_data_010_project_with_completed_stages(self):
        """Project with multiple completed stages."""
        project = Project(
            project_id=uuid4(),
            name="Mature Project",
            current_stage=SDLCStage.STAGE_05_TEST,
            completed_stages=[
                SDLCStage.STAGE_00_FOUNDATION,
                SDLCStage.STAGE_01_PLANNING,
                SDLCStage.STAGE_02_DESIGN,
                SDLCStage.STAGE_04_BUILD,
            ],
            stage_started_at=datetime.utcnow(),
        )
        assert len(project.completed_stages) == 4
        assert SDLCStage.STAGE_04_BUILD in project.completed_stages


# ============================================================================
# CATEGORY 3: File Pattern Matching
# ============================================================================


class TestFilePatternMatching:
    """Test file pattern matching logic."""

    @pytest.fixture
    def service(self) -> StageGatingService:
        """Create a StageGatingService instance."""
        return StageGatingService()

    def test_pattern_001_exact_match(self, service):
        """Exact file pattern matches."""
        assert service._matches_pattern("README.md", "README.md") is True
        assert service._matches_pattern("LICENSE", "LICENSE") is True

    def test_pattern_002_wildcard_single(self, service):
        """Single wildcard (*) matches file names."""
        assert service._matches_pattern("file.py", "*.py") is True
        assert service._matches_pattern("test.ts", "*.ts") is True
        assert service._matches_pattern("file.py", "*.ts") is False

    def test_pattern_003_double_wildcard_directory(self, service):
        """Double wildcard (**) matches any directory depth."""
        assert service._matches_pattern("docs/00-foundation/readme.md", "docs/**") is True
        assert service._matches_pattern("docs/deep/nested/file.md", "docs/**") is True

    def test_pattern_004_directory_specific(self, service):
        """Directory-specific patterns."""
        assert service._matches_pattern("backend/app/service.py", "backend/**") is True
        assert service._matches_pattern("frontend/src/App.tsx", "frontend/**") is True
        assert service._matches_pattern("backend/test.py", "frontend/**") is False

    def test_pattern_005_nested_pattern(self, service):
        """Nested directory patterns match correctly."""
        pattern = "docs/00-foundation/**"
        assert service._matches_pattern("docs/00-foundation/problem.md", pattern) is True
        assert service._matches_pattern("docs/01-planning/spec.md", pattern) is False

    def test_pattern_006_case_insensitive(self, service):
        """Pattern matching is case insensitive."""
        assert service._matches_pattern("README.MD", "readme.md") is True
        assert service._matches_pattern("Backend/App/Test.py", "backend/**") is True

    def test_pattern_007_path_normalization(self, service):
        """Windows paths are normalized in _check_file_patterns."""
        # Note: Path normalization happens in _check_file_patterns, not _matches_pattern
        # The _matches_pattern method works with already-normalized paths
        # Test that forward slashes work correctly
        assert service._matches_pattern("backend/app/test.py", "backend/**") is True
        assert service._matches_pattern("backend/app/deep/nested/file.py", "backend/**") is True

    def test_pattern_008_file_extension_pattern(self, service):
        """File extension patterns work."""
        assert service._matches_pattern("schema.prisma", "*.prisma") is True
        assert service._matches_pattern("schema.graphql", "*.graphql") is True

    def test_pattern_009_github_patterns(self, service):
        """GitHub workflow patterns match."""
        pattern = ".github/workflows/**"
        assert service._matches_pattern(".github/workflows/ci.yml", pattern) is True
        assert service._matches_pattern(".github/CODEOWNERS", pattern) is False

    def test_pattern_010_multi_level_pattern(self, service):
        """Multi-level specific patterns."""
        pattern = "backend/app/services/**"
        assert service._matches_pattern("backend/app/services/auth.py", pattern) is True
        assert service._matches_pattern("backend/app/api/routes.py", pattern) is False


# ============================================================================
# CATEGORY 4: Prerequisite Checking
# ============================================================================


class TestPrerequisiteChecking:
    """Test prerequisite stage checking."""

    @pytest.fixture
    def service(self) -> StageGatingService:
        """Create service instance."""
        return StageGatingService()

    @pytest.fixture
    def project_no_prereqs(self) -> Project:
        """Project with no completed stages."""
        return Project(
            project_id=uuid4(),
            name="New Project",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[],
        )

    @pytest.fixture
    def project_with_prereqs(self) -> Project:
        """Project with completed prerequisites."""
        return Project(
            project_id=uuid4(),
            name="Prepared Project",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[
                SDLCStage.STAGE_00_FOUNDATION,
                SDLCStage.STAGE_01_PLANNING,
                SDLCStage.STAGE_02_DESIGN,
            ],
        )

    def test_prereq_001_missing_all_prereqs(self, service, project_no_prereqs):
        """Detect missing prerequisites for BUILD stage."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_04_BUILD]
        violations = service._check_prerequisites(project_no_prereqs, rules)

        # BUILD requires foundation, planning, design
        assert len(violations) == 3
        missing = [v.missing_stage for v in violations]
        assert "stage_00_foundation" in missing
        assert "stage_01_planning" in missing
        assert "stage_02_design" in missing

    def test_prereq_002_all_prereqs_met(self, service, project_with_prereqs):
        """No violations when all prerequisites met."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_04_BUILD]
        violations = service._check_prerequisites(project_with_prereqs, rules)
        assert len(violations) == 0

    def test_prereq_003_partial_prereqs(self, service):
        """Detect partially completed prerequisites."""
        project = Project(
            project_id=uuid4(),
            name="Partial Project",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[SDLCStage.STAGE_00_FOUNDATION],
        )
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_04_BUILD]
        violations = service._check_prerequisites(project, rules)

        assert len(violations) == 2
        missing = [v.missing_stage for v in violations]
        assert "stage_01_planning" in missing
        assert "stage_02_design" in missing

    def test_prereq_004_violation_includes_cli(self, service, project_no_prereqs):
        """Prerequisite violations include CLI commands."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_04_BUILD]
        violations = service._check_prerequisites(project_no_prereqs, rules)

        for v in violations:
            assert v.cli_command is not None
            assert "sdlcctl stage complete" in v.cli_command

    def test_prereq_005_stage_00_no_prereqs(self, service):
        """Stage 00 has no prerequisites."""
        project = Project(
            project_id=uuid4(),
            name="Fresh Project",
            current_stage=SDLCStage.STAGE_00_FOUNDATION,
            completed_stages=[],
        )
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_00_FOUNDATION]
        violations = service._check_prerequisites(project, rules)
        assert len(violations) == 0

    def test_prereq_006_stage_06_requires_test(self, service):
        """Stage 06 requires stage 05 (TEST) complete."""
        project = Project(
            project_id=uuid4(),
            name="Deploy Project",
            current_stage=SDLCStage.STAGE_06_DEPLOY,
            completed_stages=[
                SDLCStage.STAGE_00_FOUNDATION,
                SDLCStage.STAGE_01_PLANNING,
                SDLCStage.STAGE_02_DESIGN,
                SDLCStage.STAGE_04_BUILD,
                # Missing STAGE_05_TEST
            ],
        )
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_06_DEPLOY]
        violations = service._check_prerequisites(project, rules)

        missing = [v.missing_stage for v in violations]
        assert "stage_05_test" in missing

    def test_prereq_007_violation_type_correct(self, service, project_no_prereqs):
        """Violation type is PREREQUISITE_INCOMPLETE."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_04_BUILD]
        violations = service._check_prerequisites(project_no_prereqs, rules)

        for v in violations:
            assert v.type == ViolationType.PREREQUISITE_INCOMPLETE
            assert v.severity == "error"

    def test_prereq_008_later_stages_minimal_prereqs(self, service):
        """Later stages (07-10) have minimal prerequisites."""
        project = Project(
            project_id=uuid4(),
            name="Operate Project",
            current_stage=SDLCStage.STAGE_07_OPERATE,
            completed_stages=[],
        )
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_07_OPERATE]
        violations = service._check_prerequisites(project, rules)
        # Stages 07-10 have no prerequisites
        assert len(violations) == 0


# ============================================================================
# CATEGORY 5: PR Requirements
# ============================================================================


class TestPRRequirements:
    """Test PR requirement checking."""

    @pytest.fixture
    def service(self) -> StageGatingService:
        """Create service instance."""
        return StageGatingService()

    @pytest.fixture
    def compliant_pr(self) -> PullRequest:
        """PR with all requirements met."""
        return PullRequest(
            pr_id=100,
            project_id=uuid4(),
            changed_files=["backend/app/service.py"],
            linked_task_id="TASK-100",
            has_intent_statement=True,
            has_ownership_headers=True,
            test_coverage=90.0,
            adr_references=["ADR-001", "ADR-002"],
            design_doc_path="docs/design/feature.md",
            security_scan_passed=True,
        )

    @pytest.fixture
    def non_compliant_pr(self) -> PullRequest:
        """PR with no requirements met."""
        return PullRequest(
            pr_id=101,
            project_id=uuid4(),
            changed_files=["backend/app/service.py"],
        )

    def test_pr_req_001_linked_task_check(self, service, compliant_pr, non_compliant_pr):
        """LINKED_TASK requirement check."""
        assert service._check_single_requirement(compliant_pr, PRRequirement.LINKED_TASK) is True
        assert service._check_single_requirement(non_compliant_pr, PRRequirement.LINKED_TASK) is False

    def test_pr_req_002_ownership_header_check(self, service, compliant_pr, non_compliant_pr):
        """OWNERSHIP_HEADER requirement check."""
        assert service._check_single_requirement(compliant_pr, PRRequirement.OWNERSHIP_HEADER) is True
        assert service._check_single_requirement(non_compliant_pr, PRRequirement.OWNERSHIP_HEADER) is False

    def test_pr_req_003_intent_statement_check(self, service, compliant_pr, non_compliant_pr):
        """INTENT_STATEMENT requirement check."""
        assert service._check_single_requirement(compliant_pr, PRRequirement.INTENT_STATEMENT) is True
        assert service._check_single_requirement(non_compliant_pr, PRRequirement.INTENT_STATEMENT) is False

    def test_pr_req_004_test_coverage_check(self, service, compliant_pr, non_compliant_pr):
        """TEST_COVERAGE_80 requirement check."""
        assert service._check_single_requirement(compliant_pr, PRRequirement.TEST_COVERAGE_80) is True
        assert service._check_single_requirement(non_compliant_pr, PRRequirement.TEST_COVERAGE_80) is False

        # Edge case: exactly 80%
        pr_exact = PullRequest(
            pr_id=102,
            project_id=uuid4(),
            changed_files=[],
            test_coverage=80.0,
        )
        assert service._check_single_requirement(pr_exact, PRRequirement.TEST_COVERAGE_80) is True

        # Edge case: just below 80%
        pr_below = PullRequest(
            pr_id=103,
            project_id=uuid4(),
            changed_files=[],
            test_coverage=79.9,
        )
        assert service._check_single_requirement(pr_below, PRRequirement.TEST_COVERAGE_80) is False

    def test_pr_req_005_adr_reference_check(self, service, compliant_pr, non_compliant_pr):
        """ADR_REFERENCE requirement check."""
        assert service._check_single_requirement(compliant_pr, PRRequirement.ADR_REFERENCE) is True
        assert service._check_single_requirement(non_compliant_pr, PRRequirement.ADR_REFERENCE) is False

    def test_pr_req_006_design_doc_check(self, service, compliant_pr, non_compliant_pr):
        """DESIGN_DOC requirement check."""
        assert service._check_single_requirement(compliant_pr, PRRequirement.DESIGN_DOC) is True
        assert service._check_single_requirement(non_compliant_pr, PRRequirement.DESIGN_DOC) is False

    def test_pr_req_007_security_scan_check(self, service, compliant_pr, non_compliant_pr):
        """SECURITY_SCAN_PASS requirement check."""
        assert service._check_single_requirement(compliant_pr, PRRequirement.SECURITY_SCAN_PASS) is True
        assert service._check_single_requirement(non_compliant_pr, PRRequirement.SECURITY_SCAN_PASS) is False

    def test_pr_req_008_build_stage_requirements(self, service, non_compliant_pr):
        """BUILD stage requires 4 PR items."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_04_BUILD]
        requirements_met, violations = service._check_pr_requirements(non_compliant_pr, rules)

        # Should fail all 4 requirements
        assert len(violations) == 4
        assert requirements_met.get("linked_task") is False
        assert requirements_met.get("ownership_header") is False

    def test_pr_req_009_violation_includes_suggestion(self, service, non_compliant_pr):
        """Requirement violations include suggestions."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_04_BUILD]
        _, violations = service._check_pr_requirements(non_compliant_pr, rules)

        for v in violations:
            assert v.suggestion is not None
            assert len(v.suggestion) > 0

    def test_pr_req_010_violation_includes_cli_command(self, service, non_compliant_pr):
        """Requirement violations include CLI commands."""
        rules = DEFAULT_STAGE_RULES[SDLCStage.STAGE_04_BUILD]
        _, violations = service._check_pr_requirements(non_compliant_pr, rules)

        for v in violations:
            assert v.cli_command is not None
            # CLI commands can be sdlcctl or pytest (for coverage)
            assert len(v.cli_command) > 0


# ============================================================================
# CATEGORY 6: Stage Validation (Full Flow)
# ============================================================================


class TestStageValidation:
    """Test full stage validation flow."""

    @pytest.fixture
    def service(self) -> StageGatingService:
        """Create service instance."""
        return StageGatingService()

    @pytest.fixture
    def build_stage_project(self) -> Project:
        """Project in BUILD stage with prerequisites."""
        return Project(
            project_id=uuid4(),
            name="Build Project",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[
                SDLCStage.STAGE_00_FOUNDATION,
                SDLCStage.STAGE_01_PLANNING,
                SDLCStage.STAGE_02_DESIGN,
            ],
        )

    @pytest.fixture
    def foundation_project(self) -> Project:
        """Project in FOUNDATION stage."""
        return Project(
            project_id=uuid4(),
            name="New Project",
            current_stage=SDLCStage.STAGE_00_FOUNDATION,
            completed_stages=[],
        )

    @pytest.mark.asyncio
    async def test_validate_001_allowed_pr(self, service, build_stage_project):
        """Compliant PR passes validation."""
        pr = PullRequest(
            pr_id=200,
            project_id=build_stage_project.project_id,
            changed_files=["backend/app/service.py"],
            linked_task_id="TASK-200",
            has_intent_statement=True,
            has_ownership_headers=True,
            test_coverage=85.0,
        )

        result = await service.validate_pr_against_stage(pr, build_stage_project)

        assert result.allowed is True
        assert len(result.violations) == 0

    @pytest.mark.asyncio
    async def test_validate_002_blocked_file_in_foundation(self, service, foundation_project):
        """Code files blocked in FOUNDATION stage."""
        pr = PullRequest(
            pr_id=201,
            project_id=foundation_project.project_id,
            changed_files=["backend/app/service.py"],
        )

        result = await service.validate_pr_against_stage(pr, foundation_project)

        assert result.allowed is False
        assert len(result.violations) > 0
        assert any(v.type == ViolationType.FILE_BLOCKED for v in result.violations)

    @pytest.mark.asyncio
    async def test_validate_003_docs_allowed_in_foundation(self, service, foundation_project):
        """Doc files allowed in FOUNDATION stage."""
        pr = PullRequest(
            pr_id=202,
            project_id=foundation_project.project_id,
            changed_files=["docs/00-foundation/problem.md", "README.md"],
        )

        result = await service.validate_pr_against_stage(pr, foundation_project)

        assert result.allowed is True
        assert len(result.violations) == 0

    @pytest.mark.asyncio
    async def test_validate_004_missing_prerequisites(self, service):
        """Detect missing prerequisites."""
        project = Project(
            project_id=uuid4(),
            name="Skip Project",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[],  # No prerequisites
        )
        pr = PullRequest(
            pr_id=203,
            project_id=project.project_id,
            changed_files=["backend/app/test.py"],
            linked_task_id="TASK-203",
            has_intent_statement=True,
            has_ownership_headers=True,
            test_coverage=90.0,
        )

        result = await service.validate_pr_against_stage(pr, project)

        assert result.allowed is False
        prereq_violations = [v for v in result.violations
                           if v.type == ViolationType.PREREQUISITE_INCOMPLETE]
        assert len(prereq_violations) == 3

    @pytest.mark.asyncio
    async def test_validate_005_missing_pr_requirements(self, service, build_stage_project):
        """Detect missing PR requirements."""
        pr = PullRequest(
            pr_id=204,
            project_id=build_stage_project.project_id,
            changed_files=["backend/app/test.py"],
            # Missing: linked_task, intent, ownership, coverage
        )

        result = await service.validate_pr_against_stage(pr, build_stage_project)

        assert result.allowed is False
        req_violations = [v for v in result.violations
                         if v.type == ViolationType.PR_REQUIREMENT_MISSING]
        assert len(req_violations) == 4

    @pytest.mark.asyncio
    async def test_validate_006_new_feature_warning_in_test_stage(self, service):
        """New feature in TEST stage generates warning."""
        project = Project(
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
        pr = PullRequest(
            pr_id=205,
            project_id=project.project_id,
            changed_files=["backend/tests/test_feature.py"],
            title="feat: Add new login feature",
            linked_task_id="TASK-205",
            test_coverage=90.0,
        )

        result = await service.validate_pr_against_stage(pr, project)

        assert len(result.warnings) > 0
        feature_warnings = [w for w in result.warnings
                          if w.type == ViolationType.STAGE_TRANSITION_INVALID]
        assert len(feature_warnings) >= 1

    @pytest.mark.asyncio
    async def test_validate_007_stage_progress_calculated(self, service, build_stage_project):
        """Stage progress is calculated."""
        pr = PullRequest(
            pr_id=206,
            project_id=build_stage_project.project_id,
            changed_files=["README.md"],
            linked_task_id="TASK-206",
            has_intent_statement=True,
            has_ownership_headers=True,
            test_coverage=80.0,
        )

        result = await service.validate_pr_against_stage(pr, build_stage_project)

        assert "stage_00_foundation" in result.stage_progress
        assert result.stage_progress["stage_00_foundation"] is True
        assert result.stage_progress["stage_04_build"] is False

    @pytest.mark.asyncio
    async def test_validate_008_suggestion_generated(self, service):
        """Suggestion generated for violations."""
        project = Project(
            project_id=uuid4(),
            name="Bad Project",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[],
        )
        pr = PullRequest(
            pr_id=207,
            project_id=project.project_id,
            changed_files=["backend/app/test.py"],
        )

        result = await service.validate_pr_against_stage(pr, project)

        assert result.suggestion is not None
        assert len(result.suggestion) > 0

    @pytest.mark.asyncio
    async def test_validate_009_deploy_stage_code_freeze(self, service):
        """DEPLOY stage blocks service code."""
        project = Project(
            project_id=uuid4(),
            name="Deploy Project",
            current_stage=SDLCStage.STAGE_06_DEPLOY,
            completed_stages=[
                SDLCStage.STAGE_00_FOUNDATION,
                SDLCStage.STAGE_01_PLANNING,
                SDLCStage.STAGE_02_DESIGN,
                SDLCStage.STAGE_04_BUILD,
                SDLCStage.STAGE_05_TEST,
            ],
        )
        pr = PullRequest(
            pr_id=208,
            project_id=project.project_id,
            changed_files=["backend/app/services/auth.py"],
            security_scan_passed=True,
        )

        result = await service.validate_pr_against_stage(pr, project)

        assert result.allowed is False
        file_blocked = [v for v in result.violations
                       if v.type == ViolationType.FILE_BLOCKED]
        assert len(file_blocked) > 0

    @pytest.mark.asyncio
    async def test_validate_010_deploy_stage_allows_k8s(self, service):
        """DEPLOY stage allows deployment configs."""
        project = Project(
            project_id=uuid4(),
            name="Deploy Project",
            current_stage=SDLCStage.STAGE_06_DEPLOY,
            completed_stages=[
                SDLCStage.STAGE_00_FOUNDATION,
                SDLCStage.STAGE_01_PLANNING,
                SDLCStage.STAGE_02_DESIGN,
                SDLCStage.STAGE_04_BUILD,
                SDLCStage.STAGE_05_TEST,
            ],
        )
        pr = PullRequest(
            pr_id=209,
            project_id=project.project_id,
            changed_files=["k8s/deployment.yaml", "docker/Dockerfile"],
            security_scan_passed=True,
        )

        result = await service.validate_pr_against_stage(pr, project)

        assert result.allowed is True

    @pytest.mark.asyncio
    async def test_validate_011_requirements_met_dict(self, service, build_stage_project):
        """PR requirements met dictionary populated."""
        pr = PullRequest(
            pr_id=210,
            project_id=build_stage_project.project_id,
            changed_files=["backend/app/test.py"],
            linked_task_id="TASK-210",
            has_ownership_headers=True,
            # Missing: intent, coverage
        )

        result = await service.validate_pr_against_stage(pr, build_stage_project)

        assert result.pr_requirements_met["linked_task"] is True
        assert result.pr_requirements_met["ownership_header"] is True
        assert result.pr_requirements_met["intent_statement"] is False
        assert result.pr_requirements_met["test_coverage_80"] is False

    @pytest.mark.asyncio
    async def test_validate_012_to_dict_conversion(self, service, build_stage_project):
        """Result converts to dictionary for API."""
        pr = PullRequest(
            pr_id=211,
            project_id=build_stage_project.project_id,
            changed_files=["README.md"],
            linked_task_id="TASK-211",
            has_intent_statement=True,
            has_ownership_headers=True,
            test_coverage=95.0,
        )

        result = await service.validate_pr_against_stage(pr, build_stage_project)
        d = result.to_dict()

        assert isinstance(d, dict)
        assert "allowed" in d
        assert "current_stage" in d
        assert "violations" in d
        assert "pr_requirements_met" in d


# ============================================================================
# CATEGORY 7: Stage Management
# ============================================================================


class TestStageManagement:
    """Test stage completion and advancement."""

    @pytest.fixture
    def service(self) -> StageGatingService:
        """Create service instance."""
        return StageGatingService()

    @pytest.fixture
    def project(self) -> Project:
        """Create test project."""
        return Project(
            project_id=uuid4(),
            name="Test Project",
            current_stage=SDLCStage.STAGE_00_FOUNDATION,
            completed_stages=[],
        )

    @pytest.mark.asyncio
    async def test_mgmt_001_complete_stage(self, service, project):
        """Complete a stage successfully."""
        success = await service.complete_stage(
            project,
            SDLCStage.STAGE_00_FOUNDATION,
            "test_user"
        )

        assert success is True
        assert SDLCStage.STAGE_00_FOUNDATION in project.completed_stages

    @pytest.mark.asyncio
    async def test_mgmt_002_complete_stage_idempotent(self, service, project):
        """Completing same stage twice is idempotent."""
        await service.complete_stage(project, SDLCStage.STAGE_00_FOUNDATION, "user1")
        await service.complete_stage(project, SDLCStage.STAGE_00_FOUNDATION, "user2")

        # Should only appear once
        count = project.completed_stages.count(SDLCStage.STAGE_00_FOUNDATION)
        assert count == 1

    @pytest.mark.asyncio
    async def test_mgmt_003_complete_requires_prereqs(self, service):
        """Cannot complete stage without prerequisites."""
        project = Project(
            project_id=uuid4(),
            name="Test",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[],  # Missing 00, 01, 02
        )

        # Try to complete BUILD without prereqs
        success = await service.complete_stage(
            project,
            SDLCStage.STAGE_04_BUILD,
            "user"
        )

        assert success is False
        assert SDLCStage.STAGE_04_BUILD not in project.completed_stages

    @pytest.mark.asyncio
    async def test_mgmt_004_advance_stage(self, service, project):
        """Advance to next stage."""
        new_stage = await service.advance_stage(project, "test_user")

        assert new_stage == SDLCStage.STAGE_01_PLANNING
        assert project.current_stage == SDLCStage.STAGE_01_PLANNING
        assert SDLCStage.STAGE_00_FOUNDATION in project.completed_stages

    @pytest.mark.asyncio
    async def test_mgmt_005_advance_updates_timestamp(self, service, project):
        """Advancing stage updates started_at timestamp."""
        original_time = project.stage_started_at
        await service.advance_stage(project, "user")

        assert project.stage_started_at is not None
        if original_time:
            assert project.stage_started_at >= original_time

    @pytest.mark.asyncio
    async def test_mgmt_006_cannot_advance_past_final(self, service):
        """Cannot advance past final stage."""
        project = Project(
            project_id=uuid4(),
            name="Final",
            current_stage=SDLCStage.STAGE_10_EVOLVE,
            completed_stages=list(SDLCStage)[:-1],
        )

        new_stage = await service.advance_stage(project, "user")

        assert new_stage is None
        assert project.current_stage == SDLCStage.STAGE_10_EVOLVE

    @pytest.mark.asyncio
    async def test_mgmt_007_advance_multiple_stages(self, service, project):
        """Advance through multiple stages."""
        # Advance from 00 to 01
        await service.advance_stage(project, "user")
        assert project.current_stage == SDLCStage.STAGE_01_PLANNING

        # Advance from 01 to 02
        await service.advance_stage(project, "user")
        assert project.current_stage == SDLCStage.STAGE_02_DESIGN

        # Check completed stages
        assert SDLCStage.STAGE_00_FOUNDATION in project.completed_stages
        assert SDLCStage.STAGE_01_PLANNING in project.completed_stages

    @pytest.mark.asyncio
    async def test_mgmt_008_later_stages_no_prereq_check(self, service):
        """Later stages (07-10) have no prerequisite enforcement."""
        project = Project(
            project_id=uuid4(),
            name="Ops",
            current_stage=SDLCStage.STAGE_07_OPERATE,
            completed_stages=[],
        )

        # Should succeed even without prerequisites
        success = await service.complete_stage(
            project,
            SDLCStage.STAGE_07_OPERATE,
            "user"
        )

        assert success is True


# ============================================================================
# CATEGORY 8: Edge Cases
# ============================================================================


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.fixture
    def service(self) -> StageGatingService:
        """Create service instance."""
        return StageGatingService()

    @pytest.mark.asyncio
    async def test_edge_001_empty_changed_files(self, service):
        """Handle PR with no changed files."""
        project = Project(
            project_id=uuid4(),
            name="Test",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[
                SDLCStage.STAGE_00_FOUNDATION,
                SDLCStage.STAGE_01_PLANNING,
                SDLCStage.STAGE_02_DESIGN,
            ],
        )
        pr = PullRequest(
            pr_id=300,
            project_id=project.project_id,
            changed_files=[],
            linked_task_id="TASK-300",
            has_intent_statement=True,
            has_ownership_headers=True,
            test_coverage=90.0,
        )

        result = await service.validate_pr_against_stage(pr, project)

        # Should pass with no file violations
        assert len([v for v in result.violations
                   if v.type == ViolationType.FILE_BLOCKED]) == 0

    @pytest.mark.asyncio
    async def test_edge_002_mixed_allowed_blocked_files(self, service):
        """Handle PR with mix of allowed and blocked files."""
        project = Project(
            project_id=uuid4(),
            name="Mixed",
            current_stage=SDLCStage.STAGE_00_FOUNDATION,
            completed_stages=[],
        )
        pr = PullRequest(
            pr_id=301,
            project_id=project.project_id,
            changed_files=[
                "README.md",  # Allowed
                "docs/00-foundation/problem.md",  # Allowed
                "backend/app/service.py",  # Blocked
            ],
        )

        result = await service.validate_pr_against_stage(pr, project)

        assert result.allowed is False
        blocked = [v for v in result.violations
                  if v.type == ViolationType.FILE_BLOCKED]
        assert len(blocked) == 1
        assert blocked[0].file_path == "backend/app/service.py"

    def test_edge_003_infer_stage_from_path(self, service):
        """Infer required stage from file path."""
        assert "foundation" in service._infer_required_stage("docs/00-foundation/x.md")
        assert "planning" in service._infer_required_stage("docs/01-planning/x.md")
        assert "design" in service._infer_required_stage("docs/02-design/adr.md")
        assert "build" in service._infer_required_stage("backend/app/service.py")
        assert "deploy" in service._infer_required_stage("docker/Dockerfile")

    def test_edge_004_factory_functions(self):
        """Test factory functions."""
        service1 = create_stage_gating_service()
        service2 = get_stage_gating_service()

        assert service1 is not None
        assert service2 is not None
        # Singleton behavior
        assert service1 is service2

    @pytest.mark.asyncio
    async def test_edge_005_special_characters_in_path(self, service):
        """Handle special characters in file paths."""
        project = Project(
            project_id=uuid4(),
            name="Special",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[
                SDLCStage.STAGE_00_FOUNDATION,
                SDLCStage.STAGE_01_PLANNING,
                SDLCStage.STAGE_02_DESIGN,
            ],
        )
        pr = PullRequest(
            pr_id=302,
            project_id=project.project_id,
            changed_files=[
                "backend/app/service-v2.py",
                "docs/feature_spec.md",
            ],
            linked_task_id="TASK-302",
            has_intent_statement=True,
            has_ownership_headers=True,
            test_coverage=80.0,
        )

        result = await service.validate_pr_against_stage(pr, project)

        # Should handle without errors
        assert isinstance(result, StageGatingResult)

    @pytest.mark.asyncio
    async def test_edge_006_coverage_exactly_threshold(self, service):
        """Test coverage at exact 80% threshold."""
        project = Project(
            project_id=uuid4(),
            name="Threshold",
            current_stage=SDLCStage.STAGE_04_BUILD,
            completed_stages=[
                SDLCStage.STAGE_00_FOUNDATION,
                SDLCStage.STAGE_01_PLANNING,
                SDLCStage.STAGE_02_DESIGN,
            ],
        )

        # Exactly 80%
        pr_80 = PullRequest(
            pr_id=303,
            project_id=project.project_id,
            changed_files=["backend/app/test.py"],
            linked_task_id="TASK-303",
            has_intent_statement=True,
            has_ownership_headers=True,
            test_coverage=80.0,
        )
        result_80 = await service.validate_pr_against_stage(pr_80, project)
        assert result_80.pr_requirements_met.get("test_coverage_80") is True

        # Just below 80%
        pr_79 = PullRequest(
            pr_id=304,
            project_id=project.project_id,
            changed_files=["backend/app/test.py"],
            linked_task_id="TASK-304",
            has_intent_statement=True,
            has_ownership_headers=True,
            test_coverage=79.99,
        )
        result_79 = await service.validate_pr_against_stage(pr_79, project)
        assert result_79.pr_requirements_met.get("test_coverage_80") is False


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
