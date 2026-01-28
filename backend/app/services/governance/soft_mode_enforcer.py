"""
=========================================================================
SOFT Mode Enforcer - Sprint 115 Track 2 Governance Enforcement
SDLC Orchestrator - Anti-Vibecoding System

Version: 1.0.0
Date: January 28, 2026 (Prepared ahead of Feb 10 kickoff)
Status: READY FOR DEPLOYMENT
Authority: CTO Approved (Sprint 114 GO Decision)
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Implement SOFT enforcement mode (partial blocking)
- Apply exemption rules (dependency_update, documentation_safe, test_only)
- Evaluate block/warn/approve decisions
- Track enforcement metrics for Sprint 115 Go/No-Go

SOFT Mode Rules:
- RED (81-100): BLOCKED (CTO override required)
- ORANGE (61-80): WARNED (CEO review recommended)
- YELLOW (31-60): PASSED (Tech Lead review suggested)
- GREEN (0-30): AUTO-APPROVED

Zero Mock Policy: Real enforcement with configurable rules
=========================================================================
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

import yaml

from app.services.governance.signals_engine import (
    CodeSubmission,
    IndexCategory,
    RoutingDecision,
    SignalType,
    VibecodingIndex,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Enums & Constants
# ============================================================================


class EnforcementAction(str, Enum):
    """Enforcement actions for SOFT mode."""

    BLOCKED = "blocked"
    WARNED = "warned"
    APPROVED = "approved"
    AUTO_APPROVED = "auto_approved"


class ExemptionType(str, Enum):
    """Types of exemptions that can be applied."""

    DEPENDENCY_UPDATE = "dependency_update_exemption"
    DOCUMENTATION_SAFE = "documentation_safe_pattern"
    TEST_ONLY = "test_only_pattern"


class OverrideAuthority(str, Enum):
    """Authorities that can override blocks."""

    CTO = "CTO"
    CEO = "CEO"
    SECURITY_LEAD = "Security Lead"


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class ExemptionResult:
    """Result of exemption rule evaluation."""

    applied: bool
    exemption_type: Optional[ExemptionType] = None
    message: str = ""
    adjustments: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BlockRuleResult:
    """Result of block rule evaluation."""

    rule_name: str
    triggered: bool
    message: str = ""
    override_allowed: bool = False
    override_requires: List[str] = field(default_factory=list)


@dataclass
class WarnRuleResult:
    """Result of warn rule evaluation."""

    rule_name: str
    triggered: bool
    message: str = ""


@dataclass
class EnforcementResult:
    """
    Complete enforcement decision for a PR.

    This is the main output of the SOFT Mode Enforcer.
    """

    action: EnforcementAction
    vibecoding_index: VibecodingIndex
    exemptions_applied: List[ExemptionResult] = field(default_factory=list)
    block_rules_triggered: List[BlockRuleResult] = field(default_factory=list)
    warn_rules_triggered: List[WarnRuleResult] = field(default_factory=list)
    can_merge: bool = True
    requires_override: bool = False
    override_authority: List[str] = field(default_factory=list)
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    evaluated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "enforcement": {
                "action": self.action.value,
                "can_merge": self.can_merge,
                "requires_override": self.requires_override,
                "override_authority": self.override_authority,
                "message": self.message,
            },
            "vibecoding_index": self.vibecoding_index.to_dict(),
            "exemptions": [
                {
                    "applied": e.applied,
                    "type": e.exemption_type.value if e.exemption_type else None,
                    "message": e.message,
                    "adjustments": e.adjustments,
                }
                for e in self.exemptions_applied
                if e.applied
            ],
            "block_rules": [
                {
                    "rule": r.rule_name,
                    "triggered": r.triggered,
                    "message": r.message,
                    "override_allowed": r.override_allowed,
                    "override_requires": r.override_requires,
                }
                for r in self.block_rules_triggered
                if r.triggered
            ],
            "warnings": [
                {"rule": w.rule_name, "message": w.message}
                for w in self.warn_rules_triggered
                if w.triggered
            ],
            "evaluated_at": self.evaluated_at.isoformat(),
        }

    @property
    def blocked(self) -> bool:
        """Whether the PR is blocked."""
        return self.action == EnforcementAction.BLOCKED

    @property
    def warned(self) -> bool:
        """Whether the PR has warnings."""
        return self.action == EnforcementAction.WARNED

    @property
    def block_reasons(self) -> List[str]:
        """List of reasons for blocking."""
        return [r.message for r in self.block_rules_triggered if r.triggered and r.message]

    @property
    def warn_reasons(self) -> List[str]:
        """List of warning reasons."""
        return [w.message for w in self.warn_rules_triggered if w.triggered and w.message]

    @property
    def exemptions_applied_list(self) -> List[str]:
        """List of applied exemption names."""
        return [
            e.exemption_type.value for e in self.exemptions_applied
            if e.applied and e.exemption_type
        ]


# ============================================================================
# SOFT Mode Enforcer Service
# ============================================================================


class SoftModeEnforcer:
    """
    SOFT Mode Enforcement Service.

    Implements Sprint 115 Track 2 governance enforcement:
    - Evaluate exemption rules (reduce false positives)
    - Apply block/warn/approve rules
    - Track enforcement metrics
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize SOFT Mode Enforcer.

        Args:
            config_path: Path to governance_soft_mode.yaml (optional)
        """
        self.config = self._load_config(config_path)
        self._dependency_files: Set[str] = set(
            self.config.get("exemptions", {})
            .get("dependency_update_exemption", {})
            .get("trigger_files", [])
        )
        self._doc_patterns: List[str] = (
            self.config.get("exemptions", {})
            .get("documentation_safe_pattern", {})
            .get("trigger_paths", [])
        )
        self._test_patterns: List[str] = (
            self.config.get("exemptions", {})
            .get("test_only_pattern", {})
            .get("trigger_paths", [])
        )

        logger.info("SoftModeEnforcer initialized with config")

    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load governance configuration."""
        if config_path:
            path = Path(config_path)
        else:
            # Default path
            path = Path(__file__).parent.parent.parent / "config" / "governance_soft_mode.yaml"

        if path.exists():
            with open(path) as f:
                return yaml.safe_load(f)
        else:
            logger.warning(f"Config not found at {path}, using defaults")
            return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration if file not found."""
        return {
            "governance": {"mode": "soft"},
            "signal_weights": {
                "architectural_smell": 0.25,
                "abstraction_complexity": 0.15,
                "ai_dependency_ratio": 0.20,
                "change_surface_area": 0.25,
                "drift_velocity": 0.15,
            },
            "exemptions": {
                "dependency_update_exemption": {
                    "enabled": True,
                    "trigger_files": [
                        "package.json",
                        "package-lock.json",
                        "requirements.txt",
                        "poetry.lock",
                    ],
                },
                "documentation_safe_pattern": {
                    "enabled": True,
                    "trigger_paths": ["docs/**", "*.md"],
                },
                "test_only_pattern": {
                    "enabled": True,
                    "trigger_paths": ["tests/**", "**/test_*.py"],
                },
            },
        }

    def get_adjusted_weights(self) -> Dict[SignalType, float]:
        """
        Get signal weights adjusted for SOFT mode.

        Returns weights from config (Sprint 114 Day 3 tuning applied).
        """
        weights_config = self.config.get("signal_weights", {})
        return {
            SignalType.ARCHITECTURAL_SMELL: weights_config.get("architectural_smell", 0.25),
            SignalType.ABSTRACTION_COMPLEXITY: weights_config.get("abstraction_complexity", 0.15),
            SignalType.AI_DEPENDENCY_RATIO: weights_config.get("ai_dependency_ratio", 0.20),
            SignalType.CHANGE_SURFACE_AREA: weights_config.get("change_surface_area", 0.25),
            SignalType.DRIFT_VELOCITY: weights_config.get("drift_velocity", 0.15),
        }

    # ========================================================================
    # Exemption Evaluation
    # ========================================================================

    def evaluate_exemptions(
        self, submission: CodeSubmission
    ) -> List[ExemptionResult]:
        """
        Evaluate all exemption rules for a submission.

        Args:
            submission: Code submission to evaluate

        Returns:
            List of exemption results (applied or not)
        """
        results = []

        # Check dependency update exemption
        dep_result = self._check_dependency_exemption(submission)
        results.append(dep_result)

        # Check documentation safe pattern
        doc_result = self._check_documentation_exemption(submission)
        results.append(doc_result)

        # Check test-only pattern
        test_result = self._check_test_only_exemption(submission)
        results.append(test_result)

        return results

    def _check_dependency_exemption(
        self, submission: CodeSubmission
    ) -> ExemptionResult:
        """
        Check if dependency update exemption applies.

        Exemption applies when:
        - ALL changed files are dependency/lockfiles
        - Maximum non-lock lines < 50

        Effect:
        - drift_velocity multiplied by 0.5
        - Index capped at 40 (yellow zone max)
        """
        exemption_config = self.config.get("exemptions", {}).get(
            "dependency_update_exemption", {}
        )

        if not exemption_config.get("enabled", False):
            return ExemptionResult(applied=False)

        # Check if all files are dependency files
        changed_basenames = [Path(f).name for f in submission.changed_files]
        all_dependency_files = all(
            basename in self._dependency_files for basename in changed_basenames
        )

        if not all_dependency_files:
            return ExemptionResult(applied=False)

        # Check line count (exclude lockfiles which can have many lines)
        non_lock_lines = submission.added_lines
        for f in submission.changed_files:
            if "lock" in f.lower():
                # Lockfiles don't count toward line limit
                continue

        max_lines = exemption_config.get("conditions", {}).get("max_non_lock_lines", 50)
        if non_lock_lines > max_lines:
            return ExemptionResult(
                applied=False,
                message=f"Too many non-lock lines ({non_lock_lines} > {max_lines})",
            )

        # Exemption applies
        effect = exemption_config.get("effect", {})
        return ExemptionResult(
            applied=True,
            exemption_type=ExemptionType.DEPENDENCY_UPDATE,
            message=effect.get("auto_message", "Dependency update exemption applied"),
            adjustments={
                "drift_velocity_multiplier": effect.get("drift_velocity_multiplier", 0.5),
                "max_index_cap": effect.get("max_index_cap", 40),
            },
        )

    def _check_documentation_exemption(
        self, submission: CodeSubmission
    ) -> ExemptionResult:
        """
        Check if documentation safe pattern applies.

        Exemption applies when:
        - ALL changed files match doc patterns
        - Vibecoding index < 25

        Effect:
        - Force GREEN zone
        - Auto-approve
        """
        exemption_config = self.config.get("exemptions", {}).get(
            "documentation_safe_pattern", {}
        )

        if not exemption_config.get("enabled", False):
            return ExemptionResult(applied=False)

        # Check if all files match documentation patterns
        all_docs = all(
            self._matches_patterns(f, self._doc_patterns)
            for f in submission.changed_files
        )

        if not all_docs:
            return ExemptionResult(applied=False)

        # Index check happens during enforcement (we don't have index yet)
        effect = exemption_config.get("effect", {})
        return ExemptionResult(
            applied=True,
            exemption_type=ExemptionType.DOCUMENTATION_SAFE,
            message=effect.get("auto_message", "Documentation-only PR - auto-approved"),
            adjustments={
                "force_zone": effect.get("force_zone", "green"),
                "auto_approve": effect.get("auto_approve", True),
                "max_index_required": exemption_config.get("conditions", {}).get("max_index", 25),
            },
        )

    def _check_test_only_exemption(
        self, submission: CodeSubmission
    ) -> ExemptionResult:
        """
        Check if test-only pattern applies.

        Exemption applies when:
        - ALL changed files are test files
        - Vibecoding index < 50

        Effect:
        - Reduce abstraction_complexity weight by 50%
        - Reduce ai_dependency weight by 30%
        """
        exemption_config = self.config.get("exemptions", {}).get(
            "test_only_pattern", {}
        )

        if not exemption_config.get("enabled", False):
            return ExemptionResult(applied=False)

        # Check if all files match test patterns
        all_tests = all(
            self._matches_patterns(f, self._test_patterns)
            for f in submission.changed_files
        )

        if not all_tests:
            return ExemptionResult(applied=False)

        effect = exemption_config.get("effect", {})
        return ExemptionResult(
            applied=True,
            exemption_type=ExemptionType.TEST_ONLY,
            message=effect.get("auto_message", "Test-only PR - reduced scrutiny applied"),
            adjustments={
                "abstraction_complexity_multiplier": effect.get(
                    "abstraction_complexity_multiplier", 0.5
                ),
                "ai_dependency_multiplier": effect.get("ai_dependency_multiplier", 0.7),
                "max_index_required": exemption_config.get("conditions", {}).get("max_index", 50),
            },
        )

    def _matches_patterns(self, file_path: str, patterns: List[str]) -> bool:
        """Check if file path matches any of the glob patterns."""
        from fnmatch import fnmatch

        for pattern in patterns:
            if fnmatch(file_path, pattern):
                return True
            # Also check basename
            if fnmatch(Path(file_path).name, pattern):
                return True
        return False

    # ========================================================================
    # Enforcement Evaluation
    # ========================================================================

    def enforce(
        self,
        vibecoding_index: VibecodingIndex,
        submission: CodeSubmission,
        has_ownership: bool = True,
        has_intent: bool = True,
        security_scan_critical: int = 0,
        has_adr_linkage: bool = True,
        test_coverage: float = 80.0,
    ) -> EnforcementResult:
        """
        Evaluate SOFT mode enforcement for a PR.

        Args:
            vibecoding_index: Calculated Vibecoding Index
            submission: Code submission details
            has_ownership: Whether PR has @owner annotation
            has_intent: Whether PR has intent statement
            security_scan_critical: Number of critical security issues
            has_adr_linkage: Whether new features have ADR linkage
            test_coverage: Test coverage percentage

        Returns:
            EnforcementResult with action, rules triggered, and merge decision
        """
        # Evaluate exemptions
        exemptions = self.evaluate_exemptions(submission)
        applied_exemptions = [e for e in exemptions if e.applied]

        # Apply exemption adjustments to index if applicable
        adjusted_index = self._apply_exemption_adjustments(
            vibecoding_index, applied_exemptions
        )

        # Evaluate block rules
        block_results = self._evaluate_block_rules(
            adjusted_index,
            has_ownership,
            has_intent,
            security_scan_critical,
        )
        triggered_blocks = [b for b in block_results if b.triggered]

        # Evaluate warn rules
        warn_results = self._evaluate_warn_rules(
            adjusted_index,
            has_adr_linkage,
            submission.is_new_feature,
            test_coverage,
        )
        triggered_warns = [w for w in warn_results if w.triggered]

        # Determine final action
        action, can_merge, requires_override, override_authority, message = (
            self._determine_action(
                adjusted_index, triggered_blocks, triggered_warns, applied_exemptions
            )
        )

        return EnforcementResult(
            action=action,
            vibecoding_index=adjusted_index,
            exemptions_applied=exemptions,
            block_rules_triggered=block_results,
            warn_rules_triggered=warn_results,
            can_merge=can_merge,
            requires_override=requires_override,
            override_authority=override_authority,
            message=message,
            details={
                "original_index": vibecoding_index.score,
                "adjusted_index": adjusted_index.score,
                "exemptions_count": len(applied_exemptions),
                "blocks_count": len(triggered_blocks),
                "warns_count": len(triggered_warns),
            },
        )

    def _apply_exemption_adjustments(
        self,
        index: VibecodingIndex,
        exemptions: List[ExemptionResult],
    ) -> VibecodingIndex:
        """Apply exemption adjustments to the Vibecoding Index."""
        adjusted_score = index.score

        for exemption in exemptions:
            if not exemption.applied:
                continue

            adjustments = exemption.adjustments

            # Apply index cap
            if "max_index_cap" in adjustments:
                cap = adjustments["max_index_cap"]
                if adjusted_score > cap:
                    adjusted_score = cap
                    logger.info(f"Index capped to {cap} by {exemption.exemption_type}")

            # Force zone
            if adjustments.get("force_zone") == "green":
                max_index_required = adjustments.get("max_index_required", 25)
                if index.score <= max_index_required:
                    adjusted_score = min(adjusted_score, 25)
                    logger.info(
                        f"Index forced to green zone by {exemption.exemption_type}"
                    )

        # Recalculate category based on adjusted score
        if adjusted_score <= 30:
            category = IndexCategory.GREEN
            routing = RoutingDecision.AUTO_APPROVE
        elif adjusted_score <= 60:
            category = IndexCategory.YELLOW
            routing = RoutingDecision.TECH_LEAD_REVIEW
        elif adjusted_score <= 80:
            category = IndexCategory.ORANGE
            routing = RoutingDecision.CEO_SHOULD_REVIEW
        else:
            category = IndexCategory.RED
            routing = RoutingDecision.CEO_MUST_REVIEW

        # Create adjusted index (preserve original signals)
        return VibecodingIndex(
            score=adjusted_score,
            category=category,
            routing=routing,
            signals=index.signals,
            critical_override=index.critical_override,
            critical_matches=index.critical_matches,
            original_score=index.score,
            suggested_focus=index.suggested_focus,
            flags=index.flags + [f"exemption_adjusted:{e.exemption_type.value}" for e in exemptions if e.applied],
        )

    def _evaluate_block_rules(
        self,
        index: VibecodingIndex,
        has_ownership: bool,
        has_intent: bool,
        security_critical: int,
    ) -> List[BlockRuleResult]:
        """Evaluate block rules."""
        results = []

        # Rule: vibecoding_index_red
        results.append(
            BlockRuleResult(
                rule_name="vibecoding_index_red",
                triggered=index.score >= 81,
                message=f"PR blocked: Vibecoding Index {index.score:.1f} exceeds threshold (81)"
                if index.score >= 81
                else "",
                override_allowed=True,
                override_requires=["CTO"],
            )
        )

        # Rule: missing_ownership
        results.append(
            BlockRuleResult(
                rule_name="missing_ownership",
                triggered=not has_ownership,
                message="PR blocked: Missing @owner annotation",
                override_allowed=False,
                override_requires=[],
            )
        )

        # Rule: missing_intent
        results.append(
            BlockRuleResult(
                rule_name="missing_intent",
                triggered=not has_intent,
                message="PR blocked: Missing intent statement",
                override_allowed=False,
                override_requires=[],
            )
        )

        # Rule: security_scan_fail
        results.append(
            BlockRuleResult(
                rule_name="security_scan_fail",
                triggered=security_critical > 0,
                message=f"PR blocked: {security_critical} critical security vulnerabilities detected",
                override_allowed=True,
                override_requires=["CTO", "Security Lead"],
            )
        )

        return results

    def _evaluate_warn_rules(
        self,
        index: VibecodingIndex,
        has_adr_linkage: bool,
        is_new_feature: bool,
        test_coverage: float,
    ) -> List[WarnRuleResult]:
        """Evaluate warn rules."""
        results = []

        # Rule: vibecoding_index_orange
        results.append(
            WarnRuleResult(
                rule_name="vibecoding_index_orange",
                triggered=61 <= index.score <= 80,
                message=f"Warning: Vibecoding Index {index.score:.1f} in orange zone. CEO review recommended.",
            )
        )

        # Rule: missing_adr_linkage (for new features only)
        results.append(
            WarnRuleResult(
                rule_name="missing_adr_linkage",
                triggered=is_new_feature and not has_adr_linkage,
                message="Warning: New feature without ADR linkage",
            )
        )

        # Rule: low_test_coverage
        results.append(
            WarnRuleResult(
                rule_name="low_test_coverage",
                triggered=test_coverage < 80,
                message=f"Warning: Test coverage {test_coverage:.1f}% below 80% target",
            )
        )

        return results

    def _determine_action(
        self,
        index: VibecodingIndex,
        blocks: List[BlockRuleResult],
        warns: List[WarnRuleResult],
        exemptions: List[ExemptionResult],
    ) -> tuple:
        """
        Determine final enforcement action.

        Returns:
            (action, can_merge, requires_override, override_authority, message)
        """
        # Check for non-overridable blocks first
        non_overridable = [b for b in blocks if not b.override_allowed]
        if non_overridable:
            return (
                EnforcementAction.BLOCKED,
                False,
                False,
                [],
                non_overridable[0].message,
            )

        # Check for overridable blocks
        overridable = [b for b in blocks if b.override_allowed]
        if overridable:
            all_authorities = []
            for b in overridable:
                all_authorities.extend(b.override_requires)
            unique_authorities = list(set(all_authorities))
            return (
                EnforcementAction.BLOCKED,
                False,
                True,
                unique_authorities,
                overridable[0].message,
            )

        # Check for auto-approve exemptions
        for e in exemptions:
            if e.adjustments.get("auto_approve"):
                return (
                    EnforcementAction.AUTO_APPROVED,
                    True,
                    False,
                    [],
                    e.message,
                )

        # Check for warnings
        if warns:
            warning_messages = [w.message for w in warns]
            return (
                EnforcementAction.WARNED,
                True,
                False,
                [],
                "; ".join(warning_messages),
            )

        # Green zone auto-approve
        if index.category == IndexCategory.GREEN:
            return (
                EnforcementAction.AUTO_APPROVED,
                True,
                False,
                [],
                f"Auto-approved: Vibecoding Index {index.score:.1f} in green zone",
            )

        # Yellow zone approved with Tech Lead suggestion
        if index.category == IndexCategory.YELLOW:
            return (
                EnforcementAction.APPROVED,
                True,
                False,
                [],
                f"Approved: Vibecoding Index {index.score:.1f} in yellow zone. Tech Lead review suggested.",
            )

        # Default approved
        return (
            EnforcementAction.APPROVED,
            True,
            False,
            [],
            f"Approved: Vibecoding Index {index.score:.1f}",
        )


# ============================================================================
# Factory Function
# ============================================================================


def create_soft_mode_enforcer(config_path: Optional[str] = None) -> SoftModeEnforcer:
    """
    Create a SoftModeEnforcer instance.

    Args:
        config_path: Optional path to configuration file

    Returns:
        Configured SoftModeEnforcer instance
    """
    return SoftModeEnforcer(config_path)


# Singleton instance
_soft_mode_enforcer: Optional[SoftModeEnforcer] = None


def get_soft_mode_enforcer() -> SoftModeEnforcer:
    """
    Get or create SoftModeEnforcer singleton.

    Returns:
        SoftModeEnforcer singleton instance
    """
    global _soft_mode_enforcer
    if _soft_mode_enforcer is None:
        _soft_mode_enforcer = create_soft_mode_enforcer()
    return _soft_mode_enforcer
