"""
=========================================================================
Stage-Aware PR Gating Service
SDLC Orchestrator - Sprint 109 (Vibecoding Index & Stage-Aware Gating)

Version: 1.0.0
Date: January 27, 2026
Status: ACTIVE - Sprint 109 Day 2
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Validate PRs against current project stage
- Prevent working ahead of design (Stage 00 → 03 progression)
- Map stage rules to daily work (PR/Task)
- Generate actionable fix suggestions

Principle:
  "Working ahead of design = rework. Stage gates prevent this."

Stage Rules:
- Stage 00 (Foundation): Only docs/00-foundation/** allowed
- Stage 01 (Planning): Docs allowed, no src/backend/frontend yet
- Stage 02 (Design): Schema design allowed, no implementation
- Stage 03 (Integration): API contracts and specs allowed
- Stage 04 (Build): All code allowed with compliance requirements
- Stage 05 (Test): Bug fixes and tests only
- Stage 06 (Deploy): Only deployment configs, code freeze

Zero Mock Policy: Real stage validation with file pattern matching
=========================================================================
"""

import fnmatch
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID

import yaml

logger = logging.getLogger(__name__)


# ============================================================================
# Enums & Constants
# ============================================================================


class SDLCStage(str, Enum):
    """SDLC stages (0-10)."""

    STAGE_00_FOUNDATION = "stage_00_foundation"
    STAGE_01_PLANNING = "stage_01_planning"
    STAGE_02_DESIGN = "stage_02_design"
    STAGE_03_INTEGRATION = "stage_03_integration"
    STAGE_04_BUILD = "stage_04_build"
    STAGE_05_TEST = "stage_05_test"
    STAGE_06_DEPLOY = "stage_06_deploy"
    STAGE_07_OPERATE = "stage_07_operate"
    STAGE_08_MONITOR = "stage_08_monitor"
    STAGE_09_GOVERN = "stage_09_govern"
    STAGE_10_EVOLVE = "stage_10_evolve"


class ViolationType(str, Enum):
    """Types of stage gating violations."""

    FILE_BLOCKED = "file_blocked"
    PREREQUISITE_INCOMPLETE = "prerequisite_incomplete"
    PR_REQUIREMENT_MISSING = "pr_requirement_missing"
    STAGE_TRANSITION_INVALID = "stage_transition_invalid"


class PRRequirement(str, Enum):
    """PR requirements for certain stages."""

    LINKED_TASK = "linked_task"
    OWNERSHIP_HEADER = "ownership_header"
    INTENT_STATEMENT = "intent_statement"
    TEST_COVERAGE_80 = "test_coverage_80"
    ADR_REFERENCE = "adr_reference"
    DESIGN_DOC = "design_doc"
    SECURITY_SCAN_PASS = "security_scan_pass"


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class StageViolation:
    """A violation of stage gating rules."""

    type: ViolationType
    severity: str  # error, warning
    message: str
    file_path: Optional[str] = None
    current_stage: Optional[str] = None
    required_stage: Optional[str] = None
    missing_stage: Optional[str] = None
    requirement: Optional[str] = None
    suggestion: Optional[str] = None
    cli_command: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "type": self.type.value,
            "severity": self.severity,
            "message": self.message,
            "file_path": self.file_path,
            "current_stage": self.current_stage,
            "required_stage": self.required_stage,
            "missing_stage": self.missing_stage,
            "requirement": self.requirement,
            "suggestion": self.suggestion,
            "cli_command": self.cli_command,
        }


@dataclass
class StageRules:
    """Rules for a specific stage."""

    stage: SDLCStage
    allows: List[str]  # Allowed file patterns
    blocks: List[str]  # Blocked file patterns
    requires_complete: List[str]  # Prerequisite stages
    requires_for_pr: List[PRRequirement]  # PR requirements
    message: str
    blocks_new_features: bool = False


@dataclass
class StageGatingResult:
    """Result of stage gating validation."""

    allowed: bool
    current_stage: SDLCStage
    violations: List[StageViolation]
    warnings: List[StageViolation]
    pr_requirements_met: Dict[str, bool]
    suggestion: Optional[str] = None
    stage_progress: Dict[str, bool] = field(default_factory=dict)
    validated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "allowed": self.allowed,
            "current_stage": self.current_stage.value,
            "violations_count": len(self.violations),
            "warnings_count": len(self.warnings),
            "violations": [v.to_dict() for v in self.violations],
            "warnings": [v.to_dict() for v in self.warnings],
            "pr_requirements_met": self.pr_requirements_met,
            "suggestion": self.suggestion,
            "stage_progress": self.stage_progress,
            "validated_at": self.validated_at.isoformat(),
        }


@dataclass
class PullRequest:
    """Pull request data for gating."""

    pr_id: int
    project_id: UUID
    changed_files: List[str]
    title: Optional[str] = None
    description: Optional[str] = None
    linked_task_id: Optional[str] = None
    author: Optional[str] = None
    has_intent_statement: bool = False
    has_ownership_headers: bool = False
    test_coverage: Optional[float] = None
    adr_references: List[str] = field(default_factory=list)
    design_doc_path: Optional[str] = None
    security_scan_passed: bool = False


@dataclass
class Project:
    """Project with stage information."""

    project_id: UUID
    name: str
    current_stage: SDLCStage
    completed_stages: List[SDLCStage] = field(default_factory=list)
    stage_started_at: Optional[datetime] = None


# ============================================================================
# Stage Rules Configuration
# ============================================================================


DEFAULT_STAGE_RULES: Dict[SDLCStage, StageRules] = {
    SDLCStage.STAGE_00_FOUNDATION: StageRules(
        stage=SDLCStage.STAGE_00_FOUNDATION,
        allows=[
            "docs/00-foundation/**",
            "docs/00-discover/**",
            "README.md",
            ".gitignore",
            "LICENSE",
            "CLAUDE.md",
            "AGENTS.md",
            ".github/**",
        ],
        blocks=[
            "src/**",
            "backend/**",
            "frontend/**",
            "app/**",
        ],
        requires_complete=[],
        requires_for_pr=[],
        message="Foundation stage not complete. Cannot write code yet. "
                "Complete: docs/00-foundation/03-Problem-Statement.md",
    ),

    SDLCStage.STAGE_01_PLANNING: StageRules(
        stage=SDLCStage.STAGE_01_PLANNING,
        allows=[
            "docs/01-planning/**",
            "docs/00-foundation/**",
            "docs/00-discover/**",
            "README.md",
            ".github/**",
        ],
        blocks=[
            "src/**",
            "backend/app/**",
            "frontend/src/**",
        ],
        requires_complete=["stage_00_foundation"],
        requires_for_pr=[],
        message="Planning stage not complete. Finish requirements first. "
                "Complete: docs/01-planning/05-API-Design/API-Specification.md",
    ),

    SDLCStage.STAGE_02_DESIGN: StageRules(
        stage=SDLCStage.STAGE_02_DESIGN,
        allows=[
            "docs/02-design/**",
            "docs/01-planning/**",
            "docs/00-foundation/**",
            "prisma/schema.prisma",
            "openapi/**",
            "*.graphql",
        ],
        blocks=[
            "backend/app/services/**",
            "backend/app/api/**",
            "frontend/src/components/**",
            "frontend/src/pages/**",
        ],
        requires_complete=["stage_00_foundation", "stage_01_planning"],
        requires_for_pr=[
            PRRequirement.ADR_REFERENCE,
        ],
        message="Design stage not complete. Approve architecture before coding. "
                "Complete: docs/02-design/03-ADRs/ADR-*.md (minimum 3 ADRs)",
    ),

    SDLCStage.STAGE_03_INTEGRATION: StageRules(
        stage=SDLCStage.STAGE_03_INTEGRATION,
        allows=[
            "docs/03-integrate/**",
            "docs/02-design/**",
            "openapi/**",
            "*.graphql",
            "backend/app/api/contracts/**",
        ],
        blocks=[
            "backend/app/services/business/**",
            "frontend/src/features/**",
        ],
        requires_complete=["stage_00_foundation", "stage_01_planning", "stage_02_design"],
        requires_for_pr=[
            PRRequirement.ADR_REFERENCE,
            PRRequirement.DESIGN_DOC,
        ],
        message="Integration stage. Define API contracts before implementation.",
    ),

    SDLCStage.STAGE_04_BUILD: StageRules(
        stage=SDLCStage.STAGE_04_BUILD,
        allows=["**"],  # All code allowed
        blocks=[],
        requires_complete=[
            "stage_00_foundation",
            "stage_01_planning",
            "stage_02_design",
        ],
        requires_for_pr=[
            PRRequirement.LINKED_TASK,
            PRRequirement.OWNERSHIP_HEADER,
            PRRequirement.INTENT_STATEMENT,
            PRRequirement.TEST_COVERAGE_80,
        ],
        message="BUILD stage active. All code changes allowed with compliance.",
    ),

    SDLCStage.STAGE_05_TEST: StageRules(
        stage=SDLCStage.STAGE_05_TEST,
        allows=[
            "tests/**",
            "e2e/**",
            "docs/05-test/**",
            "backend/tests/**",
            "frontend/tests/**",
            "backend/**/*.py",  # Bug fixes only
            "frontend/**/*.ts",
            "frontend/**/*.tsx",
        ],
        blocks=[],
        requires_complete=[
            "stage_00_foundation",
            "stage_01_planning",
            "stage_02_design",
            "stage_04_build",
        ],
        requires_for_pr=[
            PRRequirement.LINKED_TASK,
            PRRequirement.TEST_COVERAGE_80,
        ],
        blocks_new_features=True,
        message="TEST stage active. Only bug fixes and tests allowed. "
                "No new features until testing complete.",
    ),

    SDLCStage.STAGE_06_DEPLOY: StageRules(
        stage=SDLCStage.STAGE_06_DEPLOY,
        allows=[
            "docker/**",
            "k8s/**",
            "terraform/**",
            ".github/workflows/**",
            "docs/06-deploy/**",
            "scripts/deploy/**",
        ],
        blocks=[
            "backend/app/services/**",
            "frontend/src/**",
        ],
        requires_complete=[
            "stage_00_foundation",
            "stage_01_planning",
            "stage_02_design",
            "stage_04_build",
            "stage_05_test",
        ],
        requires_for_pr=[
            PRRequirement.SECURITY_SCAN_PASS,
        ],
        message="DEPLOY stage active. Only deployment configs allowed. "
                "Code freeze in effect.",
    ),

    # Additional stages with minimal rules
    SDLCStage.STAGE_07_OPERATE: StageRules(
        stage=SDLCStage.STAGE_07_OPERATE,
        allows=["**"],
        blocks=[],
        requires_complete=[],
        requires_for_pr=[],
        message="OPERATE stage. Production operations.",
    ),

    SDLCStage.STAGE_08_MONITOR: StageRules(
        stage=SDLCStage.STAGE_08_MONITOR,
        allows=["**"],
        blocks=[],
        requires_complete=[],
        requires_for_pr=[],
        message="MONITOR stage. Performance monitoring.",
    ),

    SDLCStage.STAGE_09_GOVERN: StageRules(
        stage=SDLCStage.STAGE_09_GOVERN,
        allows=["**"],
        blocks=[],
        requires_complete=[],
        requires_for_pr=[],
        message="GOVERN stage. Compliance and governance.",
    ),

    SDLCStage.STAGE_10_EVOLVE: StageRules(
        stage=SDLCStage.STAGE_10_EVOLVE,
        allows=["**"],
        blocks=[],
        requires_complete=[],
        requires_for_pr=[],
        message="EVOLVE stage. Product evolution.",
    ),
}


# ============================================================================
# Stage Gating Service
# ============================================================================


class StageGatingService:
    """
    Validate PRs against current project stage.

    Prevents:
    - Working ahead of design
    - Skipping stages
    - Missing PR requirements for stage

    Usage:
        service = StageGatingService()
        result = await service.validate_pr_against_stage(pr, project)
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize stage gating service.

        Args:
            config_path: Optional path to stage_pr_gating.yaml
        """
        self._config_path = config_path or "backend/app/config/stage_pr_gating.yaml"
        self._rules = self._load_rules()

        logger.info("StageGatingService initialized")

    def _load_rules(self) -> Dict[SDLCStage, StageRules]:
        """Load stage rules from config or use defaults."""
        try:
            with open(self._config_path, "r") as f:
                config = yaml.safe_load(f)
                # Parse custom rules from YAML
                # For now, use defaults
                return DEFAULT_STAGE_RULES
        except FileNotFoundError:
            logger.info("Using default stage rules")
            return DEFAULT_STAGE_RULES

    async def validate_pr_against_stage(
        self,
        pr: PullRequest,
        project: Project,
    ) -> StageGatingResult:
        """
        Check if PR is allowed in current project stage.

        Args:
            pr: Pull request to validate
            project: Project with stage information

        Returns:
            StageGatingResult with pass/fail and violations
        """
        current_stage = project.current_stage
        rules = self._rules.get(current_stage)

        if not rules:
            # No rules for this stage, allow
            return StageGatingResult(
                allowed=True,
                current_stage=current_stage,
                violations=[],
                warnings=[],
                pr_requirements_met={},
            )

        violations: List[StageViolation] = []
        warnings: List[StageViolation] = []

        # Check file patterns
        file_violations = self._check_file_patterns(
            pr.changed_files,
            rules,
            current_stage,
        )
        for v in file_violations:
            if v.severity == "error":
                violations.append(v)
            else:
                warnings.append(v)

        # Check prerequisites
        prereq_violations = self._check_prerequisites(
            project,
            rules,
        )
        violations.extend(prereq_violations)

        # Check PR requirements
        pr_requirements_met, requirement_violations = self._check_pr_requirements(
            pr,
            rules,
        )
        violations.extend(requirement_violations)

        # Check for new features in test/deploy stages
        if rules.blocks_new_features:
            feature_warnings = self._check_new_features(pr, current_stage)
            warnings.extend(feature_warnings)

        # Generate suggestion
        suggestion = self._generate_suggestion(violations) if violations else None

        # Calculate stage progress
        stage_progress = self._calculate_stage_progress(project)

        return StageGatingResult(
            allowed=len(violations) == 0,
            current_stage=current_stage,
            violations=violations,
            warnings=warnings,
            pr_requirements_met=pr_requirements_met,
            suggestion=suggestion,
            stage_progress=stage_progress,
        )

    def _check_file_patterns(
        self,
        changed_files: List[str],
        rules: StageRules,
        current_stage: SDLCStage,
    ) -> List[StageViolation]:
        """Check files against allowed/blocked patterns."""
        violations = []

        for file_path in changed_files:
            # Normalize path
            file_path = file_path.replace("\\", "/")

            # Check if file matches any blocked pattern
            is_blocked = False
            matched_block_pattern = None

            for pattern in rules.blocks:
                if self._matches_pattern(file_path, pattern):
                    is_blocked = True
                    matched_block_pattern = pattern
                    break

            # Check if file matches any allowed pattern
            is_allowed = False
            if rules.allows:
                for pattern in rules.allows:
                    if self._matches_pattern(file_path, pattern):
                        is_allowed = True
                        break
            else:
                # No allows means all files are allowed (except blocked)
                is_allowed = True

            # If blocked and not explicitly allowed
            if is_blocked and not is_allowed:
                required_stage = self._infer_required_stage(file_path)
                violations.append(StageViolation(
                    type=ViolationType.FILE_BLOCKED,
                    severity="error",
                    message=f"File '{file_path}' not allowed in {current_stage.value}",
                    file_path=file_path,
                    current_stage=current_stage.value,
                    required_stage=required_stage,
                    suggestion=f"Complete {required_stage} before modifying this file",
                    cli_command=f"sdlcctl stage complete {required_stage.replace('stage_', '').replace('_', '-')}",
                ))

        return violations

    def _matches_pattern(self, file_path: str, pattern: str) -> bool:
        """Check if file matches glob pattern."""
        # Normalize
        file_path = file_path.lower()
        pattern = pattern.lower()

        return fnmatch.fnmatch(file_path, pattern)

    def _infer_required_stage(self, file_path: str) -> str:
        """Infer which stage is required for a file path."""
        file_lower = file_path.lower()

        if "docs/00" in file_lower or "foundation" in file_lower:
            return "stage_00_foundation"
        elif "docs/01" in file_lower or "planning" in file_lower:
            return "stage_01_planning"
        elif "docs/02" in file_lower or "design" in file_lower or "adr" in file_lower:
            return "stage_02_design"
        elif "docs/03" in file_lower or "integrate" in file_lower:
            return "stage_03_integration"
        elif any(x in file_lower for x in ["backend/app", "frontend/src", "src/"]):
            return "stage_04_build"
        elif "test" in file_lower or "e2e" in file_lower:
            return "stage_05_test"
        elif any(x in file_lower for x in ["docker", "k8s", "terraform", "deploy"]):
            return "stage_06_deploy"
        else:
            return "stage_04_build"

    def _check_prerequisites(
        self,
        project: Project,
        rules: StageRules,
    ) -> List[StageViolation]:
        """Check if prerequisite stages are complete."""
        violations = []

        for prereq_stage_name in rules.requires_complete:
            try:
                prereq_stage = SDLCStage(prereq_stage_name)
            except ValueError:
                continue

            if prereq_stage not in project.completed_stages:
                violations.append(StageViolation(
                    type=ViolationType.PREREQUISITE_INCOMPLETE,
                    severity="error",
                    message=f"Prerequisite stage '{prereq_stage.value}' not complete",
                    missing_stage=prereq_stage.value,
                    suggestion=f"Complete {prereq_stage.value} before proceeding",
                    cli_command=f"sdlcctl stage complete {prereq_stage.value.replace('stage_', '').replace('_', '-')}",
                ))

        return violations

    def _check_pr_requirements(
        self,
        pr: PullRequest,
        rules: StageRules,
    ) -> Tuple[Dict[str, bool], List[StageViolation]]:
        """Check PR requirements for the stage."""
        requirements_met: Dict[str, bool] = {}
        violations: List[StageViolation] = []

        for requirement in rules.requires_for_pr:
            met = self._check_single_requirement(pr, requirement)
            requirements_met[requirement.value] = met

            if not met:
                violations.append(StageViolation(
                    type=ViolationType.PR_REQUIREMENT_MISSING,
                    severity="error",
                    message=f"PR missing required: {requirement.value}",
                    requirement=requirement.value,
                    suggestion=self._get_requirement_suggestion(requirement),
                    cli_command=self._get_requirement_cli(requirement, pr),
                ))

        return requirements_met, violations

    def _check_single_requirement(
        self,
        pr: PullRequest,
        requirement: PRRequirement,
    ) -> bool:
        """Check if a single PR requirement is met."""
        if requirement == PRRequirement.LINKED_TASK:
            return pr.linked_task_id is not None

        elif requirement == PRRequirement.OWNERSHIP_HEADER:
            return pr.has_ownership_headers

        elif requirement == PRRequirement.INTENT_STATEMENT:
            return pr.has_intent_statement

        elif requirement == PRRequirement.TEST_COVERAGE_80:
            return pr.test_coverage is not None and pr.test_coverage >= 80.0

        elif requirement == PRRequirement.ADR_REFERENCE:
            return len(pr.adr_references) > 0

        elif requirement == PRRequirement.DESIGN_DOC:
            return pr.design_doc_path is not None

        elif requirement == PRRequirement.SECURITY_SCAN_PASS:
            return pr.security_scan_passed

        return False

    def _get_requirement_suggestion(self, requirement: PRRequirement) -> str:
        """Get suggestion text for a requirement."""
        suggestions = {
            PRRequirement.LINKED_TASK: "Link this PR to a task in your project management tool",
            PRRequirement.OWNERSHIP_HEADER: "Add @owner annotations to changed files",
            PRRequirement.INTENT_STATEMENT: "Add intent statement explaining WHY this change",
            PRRequirement.TEST_COVERAGE_80: "Add tests to reach 80% coverage",
            PRRequirement.ADR_REFERENCE: "Reference at least one ADR that this change relates to",
            PRRequirement.DESIGN_DOC: "Create design document for this feature",
            PRRequirement.SECURITY_SCAN_PASS: "Fix security scan issues before merging",
        }
        return suggestions.get(requirement, "Meet the requirement")

    def _get_requirement_cli(
        self,
        requirement: PRRequirement,
        pr: PullRequest,
    ) -> str:
        """Get CLI command for meeting a requirement."""
        commands = {
            PRRequirement.LINKED_TASK: f"sdlcctl pr link-task --pr {pr.pr_id}",
            PRRequirement.OWNERSHIP_HEADER: f"sdlcctl add-ownership --pr {pr.pr_id}",
            PRRequirement.INTENT_STATEMENT: f"sdlcctl add-intent --pr {pr.pr_id}",
            PRRequirement.TEST_COVERAGE_80: "pytest --cov --cov-report=term-missing",
            PRRequirement.ADR_REFERENCE: f"sdlcctl add-adr-ref --pr {pr.pr_id}",
            PRRequirement.DESIGN_DOC: f"sdlcctl create-design-doc --pr {pr.pr_id}",
            PRRequirement.SECURITY_SCAN_PASS: "sdlcctl security-scan --fix",
        }
        return commands.get(requirement, "sdlcctl help")

    def _check_new_features(
        self,
        pr: PullRequest,
        current_stage: SDLCStage,
    ) -> List[StageViolation]:
        """Check for new feature indicators in test/deploy stages."""
        warnings = []

        # Keywords indicating new feature
        feature_keywords = ["feat:", "feature:", "add:", "new:", "implement:"]

        title_lower = (pr.title or "").lower()
        if any(kw in title_lower for kw in feature_keywords):
            warnings.append(StageViolation(
                type=ViolationType.STAGE_TRANSITION_INVALID,
                severity="warning",
                message=f"New feature detected in {current_stage.value}. Only bug fixes allowed.",
                suggestion="Consider waiting for next development cycle for new features",
            ))

        return warnings

    def _generate_suggestion(self, violations: List[StageViolation]) -> str:
        """Generate comprehensive fix suggestion from violations."""
        fixes = []

        for v in violations:
            if v.type == ViolationType.PREREQUISITE_INCOMPLETE:
                fixes.append(
                    f"1. Complete {v.missing_stage}:\n"
                    f"   $ {v.cli_command}"
                )
            elif v.type == ViolationType.FILE_BLOCKED:
                fixes.append(
                    f"2. File {v.file_path} requires {v.required_stage}:\n"
                    f"   Complete the prerequisite stage first"
                )
            elif v.type == ViolationType.PR_REQUIREMENT_MISSING:
                fixes.append(
                    f"3. Add {v.requirement}:\n"
                    f"   $ {v.cli_command}"
                )

        return "\n\n".join(fixes) if fixes else None

    def _calculate_stage_progress(self, project: Project) -> Dict[str, bool]:
        """Calculate progress through stages."""
        progress = {}

        for stage in SDLCStage:
            progress[stage.value] = stage in project.completed_stages

        return progress

    # ========================================================================
    # Stage Management
    # ========================================================================

    async def complete_stage(
        self,
        project: Project,
        stage: SDLCStage,
        completed_by: str,
    ) -> bool:
        """
        Mark a stage as complete.

        Args:
            project: Project to update
            stage: Stage to mark complete
            completed_by: User completing the stage

        Returns:
            True if successful
        """
        rules = self._rules.get(stage)

        if rules:
            # Check prerequisites
            for prereq_name in rules.requires_complete:
                try:
                    prereq = SDLCStage(prereq_name)
                    if prereq not in project.completed_stages:
                        logger.warning(
                            f"Cannot complete {stage.value}: "
                            f"prerequisite {prereq.value} not complete"
                        )
                        return False
                except ValueError:
                    continue

        # Add to completed stages
        if stage not in project.completed_stages:
            project.completed_stages.append(stage)

        logger.info(
            f"Stage {stage.value} completed for project {project.project_id} "
            f"by {completed_by}"
        )

        return True

    async def advance_stage(
        self,
        project: Project,
        advanced_by: str,
    ) -> Optional[SDLCStage]:
        """
        Advance project to next stage.

        Args:
            project: Project to advance
            advanced_by: User advancing the stage

        Returns:
            New stage if successful, None otherwise
        """
        stages = list(SDLCStage)
        current_index = stages.index(project.current_stage)

        if current_index >= len(stages) - 1:
            logger.info(f"Project {project.project_id} already at final stage")
            return None

        # Complete current stage
        await self.complete_stage(project, project.current_stage, advanced_by)

        # Advance to next
        next_stage = stages[current_index + 1]
        project.current_stage = next_stage
        project.stage_started_at = datetime.utcnow()

        logger.info(
            f"Project {project.project_id} advanced to {next_stage.value} "
            f"by {advanced_by}"
        )

        return next_stage


# ============================================================================
# Factory Functions
# ============================================================================

_stage_gating_service: Optional[StageGatingService] = None


def create_stage_gating_service(
    config_path: Optional[str] = None,
) -> StageGatingService:
    """Create a new StageGatingService instance."""
    global _stage_gating_service
    _stage_gating_service = StageGatingService(config_path=config_path)
    return _stage_gating_service


def get_stage_gating_service() -> StageGatingService:
    """Get or create StageGatingService singleton."""
    global _stage_gating_service
    if _stage_gating_service is None:
        _stage_gating_service = create_stage_gating_service()
    return _stage_gating_service
