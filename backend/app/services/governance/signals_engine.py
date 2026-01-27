"""
=========================================================================
Governance Signals Engine - Vibecoding Index Calculator
SDLC Orchestrator - Sprint 109 (Vibecoding Index & Stage-Aware Gating)

Version: 1.0.0
Date: January 27, 2026
Status: ACTIVE - Sprint 109 Day 1
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Calculate Vibecoding Index (0-100) from 5 weighted signals
- Capture CEO's "code smell" intuition programmatically
- Route PRs based on index: Green → Yellow → Orange → Red
- Apply MAX CRITICALITY OVERRIDE for critical paths

5 Signals (from CEO Calibration):
1. Architectural Smell (25%): God class, feature envy, shotgun surgery
2. Abstraction Complexity (15%): Inheritance depth, interface count
3. AI Dependency Ratio (20%): AI-generated lines / total lines
4. Change Surface Area (20%): Files, modules, API contracts affected
5. Drift Velocity (20%): Pattern changes over 7 days

Routing Thresholds:
- Green (0-30): Auto-approve
- Yellow (31-60): Tech Lead review
- Orange (61-80): CEO should review
- Red (81-100): CEO must review

MAX CRITICALITY OVERRIDE:
- Critical path files (auth, security, payment) → minimum index 80 (Red)

Zero Mock Policy: Real signal calculations with AST analysis
=========================================================================
"""

import ast
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID

import yaml

logger = logging.getLogger(__name__)


# ============================================================================
# Enums & Constants
# ============================================================================


class IndexCategory(str, Enum):
    """Vibecoding Index categories for routing."""

    GREEN = "green"  # 0-30: Auto-approve
    YELLOW = "yellow"  # 31-60: Tech Lead review
    ORANGE = "orange"  # 61-80: CEO should review
    RED = "red"  # 81-100: CEO must review


class RoutingDecision(str, Enum):
    """Routing decisions based on Vibecoding Index."""

    AUTO_APPROVE = "auto_approve"
    TECH_LEAD_REVIEW = "tech_lead_review"
    CEO_SHOULD_REVIEW = "ceo_should_review"
    CEO_MUST_REVIEW = "ceo_must_review"


class SignalType(str, Enum):
    """Types of governance signals."""

    ARCHITECTURAL_SMELL = "architectural_smell"
    ABSTRACTION_COMPLEXITY = "abstraction_complexity"
    AI_DEPENDENCY_RATIO = "ai_dependency_ratio"
    CHANGE_SURFACE_AREA = "change_surface_area"
    DRIFT_VELOCITY = "drift_velocity"


# Signal weights (from CEO calibration)
SIGNAL_WEIGHTS: Dict[SignalType, float] = {
    SignalType.ARCHITECTURAL_SMELL: 0.25,
    SignalType.ABSTRACTION_COMPLEXITY: 0.15,
    SignalType.AI_DEPENDENCY_RATIO: 0.20,
    SignalType.CHANGE_SURFACE_AREA: 0.20,
    SignalType.DRIFT_VELOCITY: 0.20,
}

# Index thresholds
INDEX_THRESHOLDS = {
    IndexCategory.GREEN: (0, 30),
    IndexCategory.YELLOW: (31, 60),
    IndexCategory.ORANGE: (61, 80),
    IndexCategory.RED: (81, 100),
}


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class ArchitecturalSmell:
    """Detected architectural smell."""

    type: str  # god_class, feature_envy, shotgun_surgery, parallel_inheritance
    file_path: str
    severity: float  # 0-100
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SignalScore:
    """Score for a single signal."""

    signal_type: SignalType
    score: float  # 0-100
    weight: float
    weighted_score: float  # score * weight
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    details: str = ""


@dataclass
class CodeSubmission:
    """Code submission for analysis."""

    submission_id: UUID
    project_id: UUID
    changed_files: List[str]
    added_lines: int = 0
    removed_lines: int = 0
    ai_generated_lines: int = 0
    total_lines: int = 0
    commit_messages: List[str] = field(default_factory=list)
    is_new_feature: bool = False
    affected_modules: List[str] = field(default_factory=list)
    pr_title: Optional[str] = None
    pr_description: Optional[str] = None


@dataclass
class ProjectContext:
    """Project context for drift velocity calculation."""

    project_id: UUID
    recent_patterns: List[str] = field(default_factory=list)
    deprecated_patterns: List[str] = field(default_factory=list)
    naming_conventions: Dict[str, str] = field(default_factory=dict)
    style_guide: Dict[str, Any] = field(default_factory=dict)
    last_7_days_changes: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CriticalPathMatch:
    """Match against critical path patterns."""

    pattern: str
    category: str  # security, payment, infrastructure, database_schema, secrets
    file_path: str
    override_to: int = 80  # Minimum index when matched


@dataclass
class VibecodingIndex:
    """
    Composite Vibecoding Index result.

    This is the main output of the Signals Engine.
    """

    score: float  # 0-100 composite score
    category: IndexCategory
    routing: RoutingDecision
    signals: Dict[SignalType, SignalScore]
    critical_override: bool = False
    critical_matches: List[CriticalPathMatch] = field(default_factory=list)
    original_score: Optional[float] = None  # Score before critical override
    suggested_focus: Optional[Dict[str, Any]] = None
    flags: List[str] = field(default_factory=list)
    calculated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "vibecoding_index": {
                "score": round(self.score, 2),
                "category": self.category.value,
                "routing": self.routing.value,
                "critical_override": self.critical_override,
            },
            "signals": {
                signal_type.value: {
                    "score": round(score.score, 2),
                    "weight": score.weight,
                    "weighted_score": round(score.weighted_score, 2),
                    "details": score.details,
                    "evidence_count": len(score.evidence),
                }
                for signal_type, score in self.signals.items()
            },
            "top_contributors": self._get_top_contributors(),
            "critical_matches": [
                {
                    "pattern": m.pattern,
                    "category": m.category,
                    "file_path": m.file_path,
                }
                for m in self.critical_matches
            ],
            "suggested_focus": self.suggested_focus,
            "flags": self.flags,
            "calculated_at": self.calculated_at.isoformat(),
        }

    def _get_top_contributors(self) -> List[Dict[str, Any]]:
        """Get top 3 contributing signals."""
        sorted_signals = sorted(
            self.signals.values(),
            key=lambda s: s.weighted_score,
            reverse=True,
        )

        return [
            {
                "signal": s.signal_type.value,
                "contribution": f"{(s.weighted_score / max(self.score, 1)) * 100:.1f}%",
                "score": round(s.score, 2),
                "details": s.details,
            }
            for s in sorted_signals[:3]
        ]


# ============================================================================
# Signal Calculators
# ============================================================================


class ArchitecturalSmellCalculator:
    """
    Calculate Architectural Smell signal (25% weight).

    Detects:
    - God class pattern (class >500 lines)
    - Feature envy (method uses other class more than its own)
    - Shotgun surgery (change touches many files)
    - Parallel inheritance (duplicated hierarchies)
    """

    # Thresholds
    GOD_CLASS_THRESHOLD = 500  # lines
    FEATURE_ENVY_RATIO = 2.0  # external calls > 2x internal
    SHOTGUN_SURGERY_THRESHOLD = 10  # files changed

    async def calculate(
        self,
        submission: CodeSubmission,
        file_contents: Dict[str, str],
    ) -> SignalScore:
        """
        Calculate architectural smell score.

        Args:
            submission: Code submission to analyze
            file_contents: Dict of file_path -> content

        Returns:
            SignalScore with 0-100 score
        """
        smells: List[ArchitecturalSmell] = []

        # Analyze each Python file
        for file_path, content in file_contents.items():
            if not file_path.endswith(".py"):
                continue

            try:
                tree = ast.parse(content)

                # Check for God class
                god_class_smells = self._detect_god_classes(file_path, tree, content)
                smells.extend(god_class_smells)

                # Check for Feature envy
                feature_envy_smells = self._detect_feature_envy(file_path, tree)
                smells.extend(feature_envy_smells)

            except SyntaxError:
                # Can't parse, skip
                logger.warning(f"Could not parse {file_path} for smell detection")
                continue

        # Check for Shotgun surgery (many files changed)
        if len(submission.changed_files) > self.SHOTGUN_SURGERY_THRESHOLD:
            smells.append(ArchitecturalSmell(
                type="shotgun_surgery",
                file_path="<multiple>",
                severity=min(100, len(submission.changed_files) * 5),
                details={
                    "files_changed": len(submission.changed_files),
                    "threshold": self.SHOTGUN_SURGERY_THRESHOLD,
                },
            ))

        # Calculate aggregate score
        if not smells:
            score = 0.0
            details = "No architectural smells detected"
        else:
            score = min(100.0, sum(s.severity for s in smells) / len(smells))
            details = f"{len(smells)} smell(s): {', '.join(set(s.type for s in smells))}"

        return SignalScore(
            signal_type=SignalType.ARCHITECTURAL_SMELL,
            score=score,
            weight=SIGNAL_WEIGHTS[SignalType.ARCHITECTURAL_SMELL],
            weighted_score=score * SIGNAL_WEIGHTS[SignalType.ARCHITECTURAL_SMELL],
            evidence=[{
                "type": s.type,
                "file": s.file_path,
                "severity": s.severity,
                "details": s.details,
            } for s in smells],
            details=details,
        )

    def _detect_god_classes(
        self,
        file_path: str,
        tree: ast.AST,
        content: str,
    ) -> List[ArchitecturalSmell]:
        """Detect God class pattern (>500 lines)."""
        smells = []
        lines = content.split("\n")

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Calculate class line count
                if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
                    class_lines = node.end_lineno - node.lineno + 1
                else:
                    # Fallback: count lines in class body
                    class_lines = len([
                        l for l in lines[node.lineno - 1:]
                        if l.strip() and not l.strip().startswith("#")
                    ])

                if class_lines > self.GOD_CLASS_THRESHOLD:
                    smells.append(ArchitecturalSmell(
                        type="god_class",
                        file_path=file_path,
                        severity=min(100, class_lines / 5),
                        details={
                            "class_name": node.name,
                            "line_count": class_lines,
                            "threshold": self.GOD_CLASS_THRESHOLD,
                        },
                    ))

        return smells

    def _detect_feature_envy(
        self,
        file_path: str,
        tree: ast.AST,
    ) -> List[ArchitecturalSmell]:
        """Detect Feature envy pattern."""
        smells = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Count self references vs other object references
                self_refs = 0
                other_refs = 0

                for child in ast.walk(node):
                    if isinstance(child, ast.Attribute):
                        if isinstance(child.value, ast.Name):
                            if child.value.id == "self":
                                self_refs += 1
                            else:
                                other_refs += 1

                # Feature envy if other refs > 2x self refs
                if other_refs > self_refs * self.FEATURE_ENVY_RATIO and self_refs > 0:
                    smells.append(ArchitecturalSmell(
                        type="feature_envy",
                        file_path=file_path,
                        severity=70,
                        details={
                            "method_name": node.name,
                            "self_references": self_refs,
                            "other_references": other_refs,
                        },
                    ))

        return smells


class AbstractionComplexityCalculator:
    """
    Calculate Abstraction Complexity signal (15% weight).

    Detects:
    - Inheritance depth (>3 levels)
    - Interface count (too many interfaces)
    - Generic type depth (T<U<V<W>>>)
    - Factory pattern abuse
    """

    MAX_INHERITANCE_DEPTH = 3
    MAX_INTERFACE_COUNT = 5

    async def calculate(
        self,
        submission: CodeSubmission,
        file_contents: Dict[str, str],
    ) -> SignalScore:
        """
        Calculate abstraction complexity score.

        Args:
            submission: Code submission to analyze
            file_contents: Dict of file_path -> content

        Returns:
            SignalScore with 0-100 score
        """
        issues = []

        for file_path, content in file_contents.items():
            if not file_path.endswith(".py"):
                continue

            try:
                tree = ast.parse(content)

                # Check inheritance depth
                depth_issues = self._check_inheritance_depth(file_path, tree)
                issues.extend(depth_issues)

                # Check for generic complexity (TypeVar, Generic)
                generic_issues = self._check_generic_complexity(file_path, content)
                issues.extend(generic_issues)

            except SyntaxError:
                continue

        # Calculate score
        if not issues:
            score = 0.0
            details = "No abstraction complexity issues"
        else:
            score = min(100.0, sum(i["severity"] for i in issues) / len(issues))
            details = f"{len(issues)} complexity issue(s)"

        return SignalScore(
            signal_type=SignalType.ABSTRACTION_COMPLEXITY,
            score=score,
            weight=SIGNAL_WEIGHTS[SignalType.ABSTRACTION_COMPLEXITY],
            weighted_score=score * SIGNAL_WEIGHTS[SignalType.ABSTRACTION_COMPLEXITY],
            evidence=issues,
            details=details,
        )

    def _check_inheritance_depth(
        self,
        file_path: str,
        tree: ast.AST,
    ) -> List[Dict[str, Any]]:
        """Check for deep inheritance hierarchies."""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Count base classes (simplified depth check)
                base_count = len(node.bases)

                if base_count > self.MAX_INHERITANCE_DEPTH:
                    issues.append({
                        "type": "deep_inheritance",
                        "file": file_path,
                        "class_name": node.name,
                        "base_count": base_count,
                        "severity": min(100, base_count * 20),
                    })

        return issues

    def _check_generic_complexity(
        self,
        file_path: str,
        content: str,
    ) -> List[Dict[str, Any]]:
        """Check for overly complex generic types."""
        issues = []

        # Look for nested generics like Dict[str, List[Tuple[int, ...]]]
        generic_pattern = r"\w+\[.*\[.*\[.*\].*\].*\]"
        matches = re.findall(generic_pattern, content)

        for match in matches:
            depth = match.count("[")
            if depth >= 3:
                issues.append({
                    "type": "generic_complexity",
                    "file": file_path,
                    "pattern": match[:50] + "..." if len(match) > 50 else match,
                    "depth": depth,
                    "severity": min(100, depth * 25),
                })

        return issues


class AIDependencyRatioCalculator:
    """
    Calculate AI Dependency Ratio signal (20% weight).

    Formula: ai_generated_lines / total_lines

    Red flag: ratio >80% AND human_modification <10%
    """

    RED_FLAG_AI_RATIO = 0.8
    RED_FLAG_HUMAN_MOD = 0.1

    async def calculate(
        self,
        submission: CodeSubmission,
        file_contents: Dict[str, str],
    ) -> SignalScore:
        """
        Calculate AI dependency ratio score.

        Args:
            submission: Code submission to analyze
            file_contents: Dict of file_path -> content

        Returns:
            SignalScore with 0-100 score
        """
        total_lines = submission.total_lines or 1
        ai_lines = submission.ai_generated_lines

        # Calculate ratio
        ai_ratio = ai_lines / total_lines if total_lines > 0 else 0

        # Calculate human modification ratio
        human_lines = total_lines - ai_lines
        human_mod_ratio = human_lines / total_lines if total_lines > 0 else 1

        # Score calculation
        # 0% AI = 0 score
        # 80% AI = 80 score
        # 100% AI = 100 score
        base_score = ai_ratio * 100

        # Bonus penalty if low human modification
        if ai_ratio > self.RED_FLAG_AI_RATIO and human_mod_ratio < self.RED_FLAG_HUMAN_MOD:
            base_score = min(100, base_score + 20)
            red_flag = True
        else:
            red_flag = False

        score = min(100, base_score)

        details = f"{ai_ratio:.1%} AI-generated ({ai_lines}/{total_lines} lines)"
        if red_flag:
            details += " [RED FLAG: Low human review]"

        return SignalScore(
            signal_type=SignalType.AI_DEPENDENCY_RATIO,
            score=score,
            weight=SIGNAL_WEIGHTS[SignalType.AI_DEPENDENCY_RATIO],
            weighted_score=score * SIGNAL_WEIGHTS[SignalType.AI_DEPENDENCY_RATIO],
            evidence=[{
                "ai_lines": ai_lines,
                "total_lines": total_lines,
                "ai_ratio": round(ai_ratio, 3),
                "human_mod_ratio": round(human_mod_ratio, 3),
                "red_flag": red_flag,
            }],
            details=details,
        )


class ChangeSurfaceAreaCalculator:
    """
    Calculate Change Surface Area signal (20% weight).

    Factors:
    - Files changed
    - Modules touched
    - API contracts affected
    - Database schema touched
    - Security sensitive files
    """

    # Scoring weights for different factors
    FILE_WEIGHT = 1
    MODULE_WEIGHT = 5
    API_CONTRACT_WEIGHT = 10
    DB_SCHEMA_WEIGHT = 15
    SECURITY_FILE_WEIGHT = 20

    # Patterns for sensitive files
    API_CONTRACT_PATTERNS = ["openapi", "swagger", "api_spec", "contract"]
    DB_SCHEMA_PATTERNS = ["schema.prisma", "migrations/", "alembic/"]
    SECURITY_PATTERNS = ["auth", "security", "permission", "credential", "secret"]

    async def calculate(
        self,
        submission: CodeSubmission,
        file_contents: Dict[str, str],
    ) -> SignalScore:
        """
        Calculate change surface area score.

        Args:
            submission: Code submission to analyze
            file_contents: Dict of file_path -> content

        Returns:
            SignalScore with 0-100 score
        """
        files_changed = len(submission.changed_files)
        modules_touched = len(submission.affected_modules)

        # Count sensitive file types
        api_contracts = 0
        db_schemas = 0
        security_files = 0

        for file_path in submission.changed_files:
            file_lower = file_path.lower()

            if any(p in file_lower for p in self.API_CONTRACT_PATTERNS):
                api_contracts += 1

            if any(p in file_lower for p in self.DB_SCHEMA_PATTERNS):
                db_schemas += 1

            if any(p in file_lower for p in self.SECURITY_PATTERNS):
                security_files += 1

        # Calculate weighted score
        raw_score = (
            files_changed * self.FILE_WEIGHT +
            modules_touched * self.MODULE_WEIGHT +
            api_contracts * self.API_CONTRACT_WEIGHT +
            db_schemas * self.DB_SCHEMA_WEIGHT +
            security_files * self.SECURITY_FILE_WEIGHT
        )

        # Normalize to 0-100
        # 10 files, 2 modules, 0 contracts = 20 (low)
        # 50 files, 10 modules, 2 contracts = 120 (high)
        score = min(100, raw_score)

        evidence = {
            "files_changed": files_changed,
            "modules_touched": modules_touched,
            "api_contracts_affected": api_contracts,
            "db_schemas_touched": db_schemas,
            "security_files_touched": security_files,
            "raw_score": raw_score,
        }

        details = f"{files_changed} files, {modules_touched} modules"
        if api_contracts > 0:
            details += f", {api_contracts} API contract(s)"
        if db_schemas > 0:
            details += f", {db_schemas} DB schema(s)"
        if security_files > 0:
            details += f", {security_files} security file(s)"

        return SignalScore(
            signal_type=SignalType.CHANGE_SURFACE_AREA,
            score=score,
            weight=SIGNAL_WEIGHTS[SignalType.CHANGE_SURFACE_AREA],
            weighted_score=score * SIGNAL_WEIGHTS[SignalType.CHANGE_SURFACE_AREA],
            evidence=[evidence],
            details=details,
        )


class DriftVelocityCalculator:
    """
    Calculate Drift Velocity signal (20% weight).

    Measurement: Codebase drift rate over 7 days

    Factors:
    - New patterns introduced
    - Deprecated patterns used
    - Inconsistent naming
    - Style violations
    """

    async def calculate(
        self,
        submission: CodeSubmission,
        context: Optional[ProjectContext],
        file_contents: Dict[str, str],
    ) -> SignalScore:
        """
        Calculate drift velocity score.

        Args:
            submission: Code submission to analyze
            context: Project context with historical data
            file_contents: Dict of file_path -> content

        Returns:
            SignalScore with 0-100 score
        """
        drift_factors = []

        # Check for deprecated patterns
        deprecated_count = 0
        if context and context.deprecated_patterns:
            for file_path, content in file_contents.items():
                for pattern in context.deprecated_patterns:
                    if pattern in content:
                        deprecated_count += 1
                        drift_factors.append({
                            "type": "deprecated_pattern",
                            "pattern": pattern,
                            "file": file_path,
                        })

        # Check for naming inconsistencies
        naming_issues = self._check_naming_consistency(file_contents)
        drift_factors.extend(naming_issues)

        # Check for new patterns (simplified)
        new_patterns = self._detect_new_patterns(submission, file_contents)
        drift_factors.extend(new_patterns)

        # Calculate score based on drift factors
        if not drift_factors:
            score = 0.0
            details = "No drift detected"
        else:
            # Each factor contributes to drift
            # Max out at 100
            score = min(100, len(drift_factors) * 10)
            details = f"{len(drift_factors)} drift factor(s)"

        return SignalScore(
            signal_type=SignalType.DRIFT_VELOCITY,
            score=score,
            weight=SIGNAL_WEIGHTS[SignalType.DRIFT_VELOCITY],
            weighted_score=score * SIGNAL_WEIGHTS[SignalType.DRIFT_VELOCITY],
            evidence=drift_factors,
            details=details,
        )

    def _check_naming_consistency(
        self,
        file_contents: Dict[str, str],
    ) -> List[Dict[str, Any]]:
        """Check for naming consistency issues."""
        issues = []

        for file_path, content in file_contents.items():
            if not file_path.endswith(".py"):
                continue

            try:
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    # Check function naming (should be snake_case)
                    if isinstance(node, ast.FunctionDef):
                        if not re.match(r"^[a-z_][a-z0-9_]*$", node.name):
                            if not node.name.startswith("__"):  # Exclude dunder methods
                                issues.append({
                                    "type": "naming_inconsistency",
                                    "subtype": "function_not_snake_case",
                                    "name": node.name,
                                    "file": file_path,
                                })

                    # Check class naming (should be PascalCase)
                    if isinstance(node, ast.ClassDef):
                        if not re.match(r"^[A-Z][a-zA-Z0-9]*$", node.name):
                            issues.append({
                                "type": "naming_inconsistency",
                                "subtype": "class_not_pascal_case",
                                "name": node.name,
                                "file": file_path,
                            })

            except SyntaxError:
                continue

        return issues

    def _detect_new_patterns(
        self,
        submission: CodeSubmission,
        file_contents: Dict[str, str],
    ) -> List[Dict[str, Any]]:
        """Detect newly introduced patterns."""
        patterns = []

        # Check for new framework/library imports
        new_imports = set()

        for file_path, content in file_contents.items():
            if not file_path.endswith(".py"):
                continue

            try:
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            new_imports.add(alias.name.split(".")[0])

                    if isinstance(node, ast.ImportFrom):
                        if node.module:
                            new_imports.add(node.module.split(".")[0])

            except SyntaxError:
                continue

        # Flag unusual imports (simplified check)
        unusual_imports = [
            imp for imp in new_imports
            if imp not in {"app", "os", "sys", "typing", "datetime", "uuid", "logging", "json", "re", "ast", "pathlib"}
        ]

        for imp in unusual_imports[:5]:  # Limit to 5
            patterns.append({
                "type": "new_pattern",
                "subtype": "new_import",
                "pattern": imp,
            })

        return patterns


# ============================================================================
# Critical Path Checker
# ============================================================================


class CriticalPathChecker:
    """
    Check files against critical path patterns.

    MAX CRITICALITY OVERRIDE:
    - Critical path files auto-boost index to minimum 80 (Red)
    - Even a 1-line change to auth.py triggers CEO review
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize with config path."""
        self._config_path = config_path or "backend/app/config/critical_paths.yaml"
        self._patterns: Dict[str, List[str]] = {}
        self._load_patterns()

    def _load_patterns(self) -> None:
        """Load critical path patterns from config."""
        try:
            with open(self._config_path, "r") as f:
                config = yaml.safe_load(f)
                self._patterns = config.get("critical_paths", {})
        except FileNotFoundError:
            # Default patterns
            self._patterns = {
                "security": ["auth/**", "security/**", "*/authentication*", "**/auth.py", "**/permission*.py"],
                "payment": ["payment/**", "billing/**", "*/stripe*", "**/payment*.py"],
                "database_schema": ["prisma/schema.prisma", "migrations/**", "alembic/**"],
                "infrastructure": ["docker-compose*.yml", "k8s/**", ".github/workflows/**"],
                "secrets": ["**/.env*", "**/secrets*", "**/credentials*"],
            }

    def check(self, file_paths: List[str]) -> List[CriticalPathMatch]:
        """
        Check files against critical path patterns.

        Args:
            file_paths: List of changed file paths

        Returns:
            List of critical path matches
        """
        matches = []

        for file_path in file_paths:
            for category, patterns in self._patterns.items():
                for pattern in patterns:
                    if self._matches_pattern(file_path, pattern):
                        matches.append(CriticalPathMatch(
                            pattern=pattern,
                            category=category,
                            file_path=file_path,
                            override_to=80,
                        ))
                        break  # One match per category per file

        return matches

    def _matches_pattern(self, file_path: str, pattern: str) -> bool:
        """Check if file matches pattern (glob-like)."""
        import fnmatch

        # Normalize paths
        file_path = file_path.replace("\\", "/").lower()
        pattern = pattern.replace("\\", "/").lower()

        return fnmatch.fnmatch(file_path, pattern)


# ============================================================================
# Main Signals Engine
# ============================================================================


class GovernanceSignalsEngine:
    """
    Main engine for calculating Vibecoding Index.

    Combines 5 signals with weights to produce 0-100 index.
    Applies MAX CRITICALITY OVERRIDE for critical paths.

    Usage:
        engine = GovernanceSignalsEngine()
        index = await engine.calculate_vibecoding_index(
            submission=submission,
            context=project_context,
            file_contents=file_contents,
        )
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize signals engine."""
        self._arch_smell_calc = ArchitecturalSmellCalculator()
        self._abstraction_calc = AbstractionComplexityCalculator()
        self._ai_dep_calc = AIDependencyRatioCalculator()
        self._surface_area_calc = ChangeSurfaceAreaCalculator()
        self._drift_calc = DriftVelocityCalculator()
        self._critical_path_checker = CriticalPathChecker(config_path)

        logger.info("GovernanceSignalsEngine initialized")

    async def calculate_vibecoding_index(
        self,
        submission: CodeSubmission,
        context: Optional[ProjectContext] = None,
        file_contents: Optional[Dict[str, str]] = None,
    ) -> VibecodingIndex:
        """
        Calculate complete Vibecoding Index for a submission.

        Args:
            submission: Code submission to analyze
            context: Optional project context for drift calculation
            file_contents: Optional file contents for detailed analysis

        Returns:
            VibecodingIndex with score, signals, and routing
        """
        file_contents = file_contents or {}

        # Calculate all 5 signals
        signals: Dict[SignalType, SignalScore] = {}

        # 1. Architectural Smell (25%)
        signals[SignalType.ARCHITECTURAL_SMELL] = await self._arch_smell_calc.calculate(
            submission, file_contents
        )

        # 2. Abstraction Complexity (15%)
        signals[SignalType.ABSTRACTION_COMPLEXITY] = await self._abstraction_calc.calculate(
            submission, file_contents
        )

        # 3. AI Dependency Ratio (20%)
        signals[SignalType.AI_DEPENDENCY_RATIO] = await self._ai_dep_calc.calculate(
            submission, file_contents
        )

        # 4. Change Surface Area (20%)
        signals[SignalType.CHANGE_SURFACE_AREA] = await self._surface_area_calc.calculate(
            submission, file_contents
        )

        # 5. Drift Velocity (20%)
        signals[SignalType.DRIFT_VELOCITY] = await self._drift_calc.calculate(
            submission, context, file_contents
        )

        # Calculate weighted sum
        raw_score = sum(s.weighted_score for s in signals.values())

        # Check for critical path matches
        critical_matches = self._critical_path_checker.check(submission.changed_files)
        critical_override = len(critical_matches) > 0

        # Apply MAX CRITICALITY OVERRIDE
        if critical_override:
            original_score = raw_score
            raw_score = max(raw_score, 80)  # Minimum 80 for critical paths
        else:
            original_score = None

        # Determine category and routing
        category = self._determine_category(raw_score)
        routing = self._determine_routing(category)

        # Generate suggested focus
        suggested_focus = self._generate_suggested_focus(signals, submission)

        # Generate flags
        flags = self._generate_flags(signals, critical_matches)

        return VibecodingIndex(
            score=raw_score,
            category=category,
            routing=routing,
            signals=signals,
            critical_override=critical_override,
            critical_matches=critical_matches,
            original_score=original_score,
            suggested_focus=suggested_focus,
            flags=flags,
        )

    def _determine_category(self, score: float) -> IndexCategory:
        """Determine index category from score."""
        if score <= 30:
            return IndexCategory.GREEN
        elif score <= 60:
            return IndexCategory.YELLOW
        elif score <= 80:
            return IndexCategory.ORANGE
        else:
            return IndexCategory.RED

    def _determine_routing(self, category: IndexCategory) -> RoutingDecision:
        """Determine routing decision from category."""
        routing_map = {
            IndexCategory.GREEN: RoutingDecision.AUTO_APPROVE,
            IndexCategory.YELLOW: RoutingDecision.TECH_LEAD_REVIEW,
            IndexCategory.ORANGE: RoutingDecision.CEO_SHOULD_REVIEW,
            IndexCategory.RED: RoutingDecision.CEO_MUST_REVIEW,
        }
        return routing_map[category]

    def _generate_suggested_focus(
        self,
        signals: Dict[SignalType, SignalScore],
        submission: CodeSubmission,
    ) -> Optional[Dict[str, Any]]:
        """Generate suggested focus area for review."""
        # Find highest-scoring signal
        top_signal = max(signals.values(), key=lambda s: s.weighted_score)

        if top_signal.weighted_score == 0:
            return None

        # Find file with most issues
        file_issues: Dict[str, int] = {}
        for signal in signals.values():
            for evidence in signal.evidence:
                file_path = evidence.get("file") or evidence.get("file_path")
                if file_path:
                    file_issues[file_path] = file_issues.get(file_path, 0) + 1

        top_file = max(file_issues.items(), key=lambda x: x[1])[0] if file_issues else None

        return {
            "top_signal": top_signal.signal_type.value,
            "reason": top_signal.details,
            "file": top_file,
            "estimated_review_time": self._estimate_review_time(signals),
        }

    def _estimate_review_time(self, signals: Dict[SignalType, SignalScore]) -> str:
        """Estimate review time based on signals."""
        total_score = sum(s.weighted_score for s in signals.values())

        if total_score <= 20:
            return "5-10 minutes"
        elif total_score <= 40:
            return "15-20 minutes"
        elif total_score <= 60:
            return "30-45 minutes"
        else:
            return "1+ hours"

    def _generate_flags(
        self,
        signals: Dict[SignalType, SignalScore],
        critical_matches: List[CriticalPathMatch],
    ) -> List[str]:
        """Generate warning flags."""
        flags = []

        # High AI dependency
        ai_signal = signals.get(SignalType.AI_DEPENDENCY_RATIO)
        if ai_signal and ai_signal.score > 70:
            flags.append("HIGH_AI_DEPENDENCY")

        # Architectural issues
        arch_signal = signals.get(SignalType.ARCHITECTURAL_SMELL)
        if arch_signal and arch_signal.score > 50:
            flags.append("ARCHITECTURAL_CONCERNS")

        # Critical path
        if critical_matches:
            categories = set(m.category for m in critical_matches)
            for cat in categories:
                flags.append(f"CRITICAL_PATH_{cat.upper()}")

        # Large change
        surface_signal = signals.get(SignalType.CHANGE_SURFACE_AREA)
        if surface_signal and surface_signal.score > 60:
            flags.append("LARGE_CHANGE")

        return flags


# ============================================================================
# Factory Functions
# ============================================================================

_signals_engine: Optional[GovernanceSignalsEngine] = None


def create_signals_engine(
    config_path: Optional[str] = None,
) -> GovernanceSignalsEngine:
    """Create a new GovernanceSignalsEngine instance."""
    global _signals_engine
    _signals_engine = GovernanceSignalsEngine(config_path=config_path)
    return _signals_engine


def get_signals_engine() -> GovernanceSignalsEngine:
    """Get or create GovernanceSignalsEngine singleton."""
    global _signals_engine
    if _signals_engine is None:
        _signals_engine = create_signals_engine()
    return _signals_engine
