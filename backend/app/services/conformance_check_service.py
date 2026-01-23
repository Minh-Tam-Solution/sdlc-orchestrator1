"""
=========================================================================
Conformance Check Service - Pattern Conformance Validation
SDLC Orchestrator - Sprint 99 (Planning Sub-agent Implementation Part 2)

Version: 1.0.0
Date: January 23, 2026
Status: ACTIVE - Sprint 99 Implementation
Authority: Backend Lead + CTO Approved
Reference: ADR-034-Planning-Subagent-Orchestration
Design: Conformance-Check-Service-Design.md

Purpose:
- Compare proposed changes (PR diff) against established patterns
- Prevent architectural drift by validating conformance before merge
- Calculate deviation scores (0-100) for quality gates
- Generate actionable recommendations for deviations

Scoring Criteria (100 points total):
- Pattern coverage: 40 points
- ADR alignment: 20 points
- Convention following: 20 points
- Risk assessment: 20 points

Performance Targets:
- PR diff check (p95): <30s
- Plan conformance check (p95): <10s
- Score calculation: <1s

Zero Mock Policy: 100% real implementation
=========================================================================
"""

import logging
import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional
from uuid import UUID, uuid4

from app.schemas.planning_subagent import (
    ConformanceDeviation,
    ConformanceLevel,
    ConformanceResult,
    ExtractedPattern,
    ImplementationPlan,
    PatternCategory,
    PatternSummary,
)
from app.services.pattern_extraction_service import PatternExtractionService

logger = logging.getLogger(__name__)


class DeviationSeverity(str, Enum):
    """Severity levels for conformance deviations."""

    CRITICAL = "critical"  # -20 points, blocks merge
    HIGH = "high"  # -15 points
    MEDIUM = "medium"  # -10 points
    LOW = "low"  # -5 points
    INFO = "info"  # -0 points, advisory only


@dataclass
class DeviationRule:
    """Rule for detecting pattern deviations."""

    id: str
    name: str
    category: PatternCategory
    pattern: str  # Regex pattern to detect violation
    severity: DeviationSeverity
    description: str
    suggestion: str


class ConformanceCheckService:
    """
    Compares proposed changes against established patterns.

    This service is the core of architectural drift prevention:
    1. Analyzes PR diffs for pattern violations
    2. Validates implementation plans before approval
    3. Calculates conformance scores (0-100)
    4. Generates actionable recommendations

    Scoring Algorithm:
        Base Score: 100
        Deductions:
        - Critical violation: -20 points
        - High violation: -15 points
        - Medium violation: -10 points
        - Low violation: -5 points

        Final Score = max(0, Base Score - Total Deductions)

    Conformance Levels:
        - EXCELLENT: >= 90 (green, auto-approve eligible)
        - GOOD: >= 70 (yellow, review recommended)
        - FAIR: >= 50 (orange, review required)
        - POOR: < 50 (red, changes required)

    Usage:
        service = ConformanceCheckService()
        result = await service.check_pr_diff(
            pr_diff_url="https://github.com/.../pull/123.diff",
            project_path=Path("/path/to/project")
        )

        if result.level == ConformanceLevel.POOR:
            for dev in result.deviations:
                print(f"Fix: {dev.suggestion}")

    SDLC 5.2.0 Compliance:
        - Integrated with Planning Mode workflow
        - Supports GitHub Check integration
        - Evidence Vault compatible
    """

    # Default deviation rules
    DEFAULT_RULES: list[DeviationRule] = [
        # Architecture violations
        DeviationRule(
            id="ARCH-001",
            name="Service Layer Bypass",
            category=PatternCategory.ARCHITECTURE,
            pattern=r"(router|controller).*\.(query|execute|insert|update|delete)",
            severity=DeviationSeverity.HIGH,
            description="Direct database access in controller/router bypasses service layer",
            suggestion="Move database operations to service layer",
        ),
        DeviationRule(
            id="ARCH-002",
            name="Circular Import Risk",
            category=PatternCategory.ARCHITECTURE,
            pattern=r"from\s+app\.services\.\w+\s+import.*from\s+app\.services\.\w+",
            severity=DeviationSeverity.MEDIUM,
            description="Multiple service imports may indicate circular dependency risk",
            suggestion="Consider using dependency injection or interfaces",
        ),
        # Code style violations
        DeviationRule(
            id="STYLE-001",
            name="Missing Type Hints",
            category=PatternCategory.CODE_STYLE,
            pattern=r"def\s+\w+\([^)]*\)(?!\s*->)",
            severity=DeviationSeverity.LOW,
            description="Function missing return type hint",
            suggestion="Add return type annotation (e.g., -> None, -> str)",
        ),
        DeviationRule(
            id="STYLE-002",
            name="God Function",
            category=PatternCategory.CODE_STYLE,
            pattern=r"def\s+\w+\([^)]*\):(?:.*\n){50,}",
            severity=DeviationSeverity.MEDIUM,
            description="Function exceeds 50 lines - may be too complex",
            suggestion="Consider breaking into smaller functions",
        ),
        # Error handling violations
        DeviationRule(
            id="ERR-001",
            name="Bare Except Clause",
            category=PatternCategory.ERROR_HANDLING,
            pattern=r"except\s*:",
            severity=DeviationSeverity.HIGH,
            description="Bare except clause catches all exceptions including system exits",
            suggestion="Use specific exception types (e.g., except ValueError:)",
        ),
        DeviationRule(
            id="ERR-002",
            name="Silent Exception",
            category=PatternCategory.ERROR_HANDLING,
            pattern=r"except\s+\w+.*:\s*\n\s*pass",
            severity=DeviationSeverity.MEDIUM,
            description="Exception silently ignored without logging",
            suggestion="Add logging or re-raise with context",
        ),
        # Security violations
        DeviationRule(
            id="SEC-001",
            name="Hardcoded Secret",
            category=PatternCategory.SECURITY,
            pattern=r'(password|secret|api_key|token)\s*=\s*["\'][^"\']{8,}["\']',
            severity=DeviationSeverity.CRITICAL,
            description="Potential hardcoded secret in code",
            suggestion="Use environment variables or secrets manager",
        ),
        DeviationRule(
            id="SEC-002",
            name="SQL Injection Risk",
            category=PatternCategory.SECURITY,
            pattern=r'(execute|raw)\s*\([^)]*["\'].*\%|\.format\(',
            severity=DeviationSeverity.CRITICAL,
            description="Potential SQL injection vulnerability",
            suggestion="Use parameterized queries or ORM methods",
        ),
        # Testing violations
        DeviationRule(
            id="TEST-001",
            name="Missing Test Assertion",
            category=PatternCategory.TESTING,
            pattern=r"def\s+test_\w+\([^)]*\):(?:(?!assert).)*$",
            severity=DeviationSeverity.MEDIUM,
            description="Test function without assertions",
            suggestion="Add assert statements to verify behavior",
        ),
        # API Design violations
        DeviationRule(
            id="API-001",
            name="Missing Response Model",
            category=PatternCategory.API_DESIGN,
            pattern=r"@(router|app)\.(get|post|put|delete)\s*\([^)]*\)(?!.*response_model)",
            severity=DeviationSeverity.LOW,
            description="API endpoint without response_model",
            suggestion="Add response_model for API documentation",
        ),
        # Database violations
        DeviationRule(
            id="DB-001",
            name="N+1 Query Risk",
            category=PatternCategory.DATABASE,
            pattern=r"for\s+\w+\s+in\s+\w+:.*\n.*\.(query|get|filter)",
            severity=DeviationSeverity.MEDIUM,
            description="Potential N+1 query pattern detected",
            suggestion="Use eager loading or batch queries",
        ),
    ]

    def __init__(
        self,
        pattern_service: Optional[PatternExtractionService] = None,
        custom_rules: Optional[list[DeviationRule]] = None,
    ):
        """
        Initialize ConformanceCheckService.

        Args:
            pattern_service: Pattern extraction service (optional)
            custom_rules: Additional custom deviation rules (optional)
        """
        self.pattern_service = pattern_service or PatternExtractionService()
        self.rules = self.DEFAULT_RULES.copy()
        if custom_rules:
            self.rules.extend(custom_rules)

        # Compile regex patterns for efficiency
        self._compiled_rules: dict[str, re.Pattern] = {}
        for rule in self.rules:
            try:
                self._compiled_rules[rule.id] = re.compile(
                    rule.pattern, re.MULTILINE | re.IGNORECASE
                )
            except re.error as e:
                logger.warning(f"Invalid regex in rule {rule.id}: {e}")

    async def check_pr_diff(
        self,
        diff_content: str,
        project_path: Path,
        patterns: Optional[PatternSummary] = None,
    ) -> ConformanceResult:
        """
        Check PR diff content against established patterns.

        This is the main entry point for CI/CD integration (GitHub Checks).

        Args:
            diff_content: Unified diff content from PR
            project_path: Path to project for pattern extraction
            patterns: Pre-extracted patterns (optional, will extract if not provided)

        Returns:
            ConformanceResult with score, level, and deviations

        Example:
            diff = await fetch_pr_diff("https://github.com/.../pull/123.diff")
            result = await service.check_pr_diff(
                diff_content=diff,
                project_path=Path("/repo")
            )
            if result.score >= 70:
                approve_check()
        """
        logger.info(f"Checking PR diff conformance for project: {project_path}")

        # Extract patterns if not provided
        if patterns is None:
            explore_result = await self.pattern_service.search_similar_implementations(
                task="General codebase patterns",
                project_path=project_path,
                depth=3,
            )
            patterns = PatternSummary(
                patterns=explore_result.patterns,
                total_files_scanned=explore_result.files_searched,
                total_patterns_found=len(explore_result.patterns),
                categories={},
                top_patterns=[],
                conventions_detected={},
            )

        # Parse diff to extract added/modified lines
        added_lines = self._parse_diff_additions(diff_content)

        # Analyze for deviations
        deviations = self._analyze_diff_patterns(added_lines, patterns)

        # Calculate score
        score = self._calculate_score(deviations, patterns)

        # Determine level
        level = self._score_to_level(score)

        # Generate recommendations
        recommendations = self._generate_recommendations(deviations, patterns)

        # Check if new patterns need ADR
        requires_adr = any(
            d.severity in [DeviationSeverity.CRITICAL, DeviationSeverity.HIGH]
            and "new pattern" in d.description.lower()
            for d in deviations
        )

        return ConformanceResult(
            score=score,
            level=level,
            deviations=deviations,
            recommendations=recommendations,
            requires_adr=requires_adr,
            new_patterns_detected=[],
        )

    async def check_plan_conformance(
        self,
        plan: ImplementationPlan,
        patterns: PatternSummary,
    ) -> ConformanceResult:
        """
        Check implementation plan conformance before approval.

        This validates that the proposed plan aligns with existing patterns.

        Args:
            plan: Implementation plan to validate
            patterns: Extracted patterns from codebase

        Returns:
            ConformanceResult with score and recommendations

        Example:
            plan = orchestrator.plan(request)
            result = await conformance.check_plan_conformance(
                plan=plan.plan,
                patterns=plan.patterns
            )
            if result.level == ConformanceLevel.POOR:
                request_changes(result.recommendations)
        """
        logger.info(f"Checking plan conformance for task: {plan.task[:50]}...")

        deviations: list[ConformanceDeviation] = []

        # Check 1: Pattern coverage
        pattern_coverage = len(plan.patterns_applied) / max(
            len(patterns.patterns), 1
        )
        if pattern_coverage < 0.2:
            deviations.append(
                ConformanceDeviation(
                    pattern_id="PLAN-001",
                    pattern_name="Low Pattern Coverage",
                    description=f"Plan applies only {pattern_coverage:.0%} of established patterns",
                    severity="high",
                    suggestion="Review existing patterns and incorporate more into the plan",
                )
            )

        # Check 2: ADR alignment
        if not plan.adrs_referenced and patterns.total_patterns_found > 5:
            deviations.append(
                ConformanceDeviation(
                    pattern_id="PLAN-002",
                    pattern_name="Missing ADR References",
                    description="Plan doesn't reference any ADRs despite established patterns",
                    severity="medium",
                    suggestion="Review and reference relevant ADRs in the plan",
                )
            )

        # Check 3: New patterns without documentation
        if plan.new_patterns_introduced:
            for new_pattern in plan.new_patterns_introduced:
                deviations.append(
                    ConformanceDeviation(
                        pattern_id="PLAN-003",
                        pattern_name="New Pattern Introduction",
                        description=f"Plan introduces new pattern: {new_pattern}",
                        severity="low",
                        suggestion="Consider creating ADR for new pattern if widely applicable",
                    )
                )

        # Check 4: Risk assessment
        high_risk_count = sum(
            1 for risk in plan.risks
            if any(word in risk.lower() for word in ["security", "database", "auth"])
        )
        if high_risk_count > 0:
            deviations.append(
                ConformanceDeviation(
                    pattern_id="PLAN-004",
                    pattern_name="High-Risk Changes",
                    description=f"Plan contains {high_risk_count} high-risk changes",
                    severity="medium",
                    suggestion="Ensure thorough review and testing for high-risk changes",
                )
            )

        # Check 5: Estimated LOC vs complexity
        if plan.total_estimated_loc > 500:
            deviations.append(
                ConformanceDeviation(
                    pattern_id="PLAN-005",
                    pattern_name="Large Implementation",
                    description=f"Plan estimates {plan.total_estimated_loc} LOC - consider breaking into smaller tasks",
                    severity="low",
                    suggestion="Consider breaking into multiple smaller, incremental PRs",
                )
            )

        # Calculate score
        score = self._calculate_score(deviations, patterns)
        level = self._score_to_level(score)
        recommendations = self._generate_recommendations(deviations, patterns)

        requires_adr = len(plan.new_patterns_introduced) > 0

        return ConformanceResult(
            score=score,
            level=level,
            deviations=deviations,
            recommendations=recommendations,
            requires_adr=requires_adr,
            new_patterns_detected=plan.new_patterns_introduced,
        )

    def _parse_diff_additions(self, diff_content: str) -> str:
        """
        Parse unified diff to extract added/modified lines.

        Args:
            diff_content: Unified diff format content

        Returns:
            String containing only added lines (without + prefix)
        """
        added_lines: list[str] = []

        for line in diff_content.split("\n"):
            # Lines starting with + (but not +++) are additions
            if line.startswith("+") and not line.startswith("+++"):
                added_lines.append(line[1:])  # Remove + prefix

        return "\n".join(added_lines)

    def _analyze_diff_patterns(
        self,
        diff_additions: str,
        patterns: PatternSummary,
    ) -> list[ConformanceDeviation]:
        """
        Analyze diff additions for pattern violations.

        Args:
            diff_additions: Added lines from diff
            patterns: Established patterns to check against

        Returns:
            List of detected deviations
        """
        deviations: list[ConformanceDeviation] = []
        seen_violations: set[str] = set()  # Avoid duplicate detections

        for rule in self.rules:
            compiled = self._compiled_rules.get(rule.id)
            if not compiled:
                continue

            matches = compiled.findall(diff_additions)
            if matches and rule.id not in seen_violations:
                seen_violations.add(rule.id)
                deviations.append(
                    ConformanceDeviation(
                        pattern_id=rule.id,
                        pattern_name=rule.name,
                        description=rule.description,
                        severity=rule.severity.value,
                        suggestion=rule.suggestion,
                    )
                )

        # Check for patterns that SHOULD be present but aren't
        # (e.g., if codebase uses async everywhere, new code should too)
        deviations.extend(
            self._check_missing_patterns(diff_additions, patterns)
        )

        return deviations

    def _check_missing_patterns(
        self,
        diff_additions: str,
        patterns: PatternSummary,
    ) -> list[ConformanceDeviation]:
        """
        Check for expected patterns that are missing from the diff.

        Args:
            diff_additions: Added lines from diff
            patterns: Established patterns

        Returns:
            List of deviations for missing patterns
        """
        deviations: list[ConformanceDeviation] = []

        # Check if codebase uses async but new code doesn't
        async_patterns = [
            p for p in patterns.patterns
            if "async" in p.name.lower() or "async" in p.code_snippet.lower()
        ]

        has_functions = bool(re.search(r"def\s+\w+\(", diff_additions))
        has_async = bool(re.search(r"async\s+def", diff_additions))

        if len(async_patterns) > 3 and has_functions and not has_async:
            deviations.append(
                ConformanceDeviation(
                    pattern_id="MISS-001",
                    pattern_name="Missing Async Pattern",
                    description="Codebase predominantly uses async, but new functions are synchronous",
                    severity="low",
                    suggestion="Consider using async def for consistency with existing patterns",
                )
            )

        # Check if codebase uses type hints but new code doesn't
        typed_patterns = [
            p for p in patterns.patterns
            if "->" in p.code_snippet or ": " in p.code_snippet
        ]

        has_type_hints = bool(re.search(r"def\s+\w+\([^)]*:\s*\w+", diff_additions))

        if len(typed_patterns) > 5 and has_functions and not has_type_hints:
            deviations.append(
                ConformanceDeviation(
                    pattern_id="MISS-002",
                    pattern_name="Missing Type Hints",
                    description="Codebase uses type hints, but new code lacks type annotations",
                    severity="low",
                    suggestion="Add type hints for consistency (e.g., def func(x: int) -> str)",
                )
            )

        return deviations

    def _calculate_score(
        self,
        deviations: list[ConformanceDeviation],
        patterns: PatternSummary,
    ) -> int:
        """
        Calculate conformance score (0-100).

        Args:
            deviations: List of detected deviations
            patterns: Established patterns

        Returns:
            Integer score from 0 to 100
        """
        score = 100

        # Deduct points based on severity
        severity_points = {
            "critical": 20,
            "high": 15,
            "medium": 10,
            "low": 5,
            "info": 0,
        }

        for deviation in deviations:
            deduction = severity_points.get(deviation.severity, 5)
            score -= deduction

        # Bonus points for good pattern coverage (up to +10)
        if patterns.total_patterns_found > 0:
            coverage_bonus = min(10, patterns.total_patterns_found // 2)
            score += coverage_bonus

        # Ensure score is within bounds
        return max(0, min(100, score))

    def _score_to_level(self, score: int) -> ConformanceLevel:
        """
        Convert numeric score to conformance level.

        Args:
            score: Numeric score (0-100)

        Returns:
            ConformanceLevel enum value
        """
        if score >= 90:
            return ConformanceLevel.EXCELLENT
        elif score >= 70:
            return ConformanceLevel.GOOD
        elif score >= 50:
            return ConformanceLevel.FAIR
        else:
            return ConformanceLevel.POOR

    def _generate_recommendations(
        self,
        deviations: list[ConformanceDeviation],
        patterns: PatternSummary,
    ) -> list[str]:
        """
        Generate actionable recommendations based on deviations.

        Args:
            deviations: List of detected deviations
            patterns: Established patterns

        Returns:
            List of recommendation strings
        """
        recommendations: list[str] = []

        # Group deviations by category
        category_counts: dict[str, int] = {}
        for dev in deviations:
            # Extract category from pattern_id prefix
            category = dev.pattern_id.split("-")[0]
            category_counts[category] = category_counts.get(category, 0) + 1

        # Generate category-specific recommendations
        if category_counts.get("SEC", 0) > 0:
            recommendations.append(
                "⚠️ SECURITY: Address security findings before merging"
            )

        if category_counts.get("ARCH", 0) > 0:
            recommendations.append(
                "📐 ARCHITECTURE: Review architectural alignment with existing patterns"
            )

        if category_counts.get("ERR", 0) > 0:
            recommendations.append(
                "🔧 ERROR HANDLING: Improve exception handling per codebase standards"
            )

        if category_counts.get("TEST", 0) > 0:
            recommendations.append(
                "🧪 TESTING: Add or improve test coverage"
            )

        # Add specific suggestions from deviations
        critical_suggestions = [
            d.suggestion for d in deviations
            if d.severity == "critical"
        ]
        for suggestion in critical_suggestions[:3]:  # Top 3 critical
            recommendations.append(f"🚨 {suggestion}")

        # Add pattern-based recommendations
        if patterns.conventions_detected:
            if "naming" in patterns.conventions_detected:
                recommendations.append(
                    f"📝 Follow naming convention: {patterns.conventions_detected['naming'][:100]}..."
                )

        return recommendations


# Factory function
def create_conformance_check_service(
    pattern_service: Optional[PatternExtractionService] = None,
) -> ConformanceCheckService:
    """
    Factory function to create ConformanceCheckService.

    Args:
        pattern_service: Optional pattern extraction service

    Returns:
        Configured ConformanceCheckService
    """
    return ConformanceCheckService(pattern_service=pattern_service)
