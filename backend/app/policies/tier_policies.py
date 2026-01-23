"""
=========================================================================
4-Tier Policy Definitions - SDLC Orchestrator
Sprint 102: 4-Tier Policy Enforcement

Version: 1.0.0
Date: January 23, 2026
Status: ACTIVE - Sprint 102 Implementation
Authority: Backend Lead + CTO Approved
Reference: docs/04-build/02-Sprint-Plans/SPRINT-102-DESIGN.md
Reference: SDLC 5.2.0 Framework - 4-Tier Classification

Purpose:
- Define policy tiers (LITE, STANDARD, PROFESSIONAL, ENTERPRISE)
- Specify requirements per tier
- Enable graduated governance

4-Tier Overview:
- LITE: Individuals, prototypes (advisory only)
- STANDARD: Small teams 2-5 (soft enforcement)
- PROFESSIONAL: Medium teams 5-15 (hard enforcement)
- ENTERPRISE: Large orgs 15+ (strictest)

Zero Mock Policy: Production-ready policy definitions
=========================================================================
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class PolicyTier(str, Enum):
    """
    Policy tier levels for graduated governance.

    SDLC 5.2.0 Classification:
    - LITE: Minimal requirements, advisory mode
    - STANDARD: Basic requirements, soft enforcement
    - PROFESSIONAL: Full requirements, hard enforcement
    - ENTERPRISE: Strictest requirements, zero tolerance
    """
    LITE = "LITE"
    STANDARD = "STANDARD"
    PROFESSIONAL = "PROFESSIONAL"
    ENTERPRISE = "ENTERPRISE"


@dataclass
class TierPolicy:
    """
    Policy configuration for a specific tier.

    Defines what checks are required and thresholds for each tier.

    Attributes:
        tier: The policy tier level
        display_name: Human-readable tier name
        description: Tier description for UI
        target_audience: Who should use this tier

        # Evidence Requirements (MRP 5-Point)
        test_required: Whether test evidence is required
        test_coverage_required: Minimum test coverage percentage (0-100)
        lint_required: Whether lint evidence is required
        security_scan_required: Whether security scan is required
        build_verification_required: Whether build verification is required
        conformance_check_required: Whether conformance check is required

        # Additional Checks
        risk_analysis_required: Whether risk analysis (Sprint 101) is required
        crp_required_for_high_risk: Whether CRP is required for high-risk changes
        adr_alignment_required: Whether ADR alignment check is required

        # Vulnerability Thresholds
        max_critical_vulnerabilities: Max allowed critical vulns (0 = none allowed)
        max_high_vulnerabilities: Max allowed high vulns
        max_medium_vulnerabilities: Max allowed medium vulns

        # Conformance Thresholds
        min_conformance_score: Minimum conformance score (0-100)

        # Enforcement Mode
        enforcement_mode: "advisory" | "soft" | "hard"
    """
    tier: PolicyTier
    display_name: str
    description: str
    target_audience: str

    # Evidence Requirements (MRP 5-Point Structure)
    test_required: bool = False
    test_coverage_required: int = 0  # 0-100%
    lint_required: bool = False
    security_scan_required: bool = False
    build_verification_required: bool = False
    conformance_check_required: bool = False

    # Additional Checks
    risk_analysis_required: bool = False
    crp_required_for_high_risk: bool = False
    adr_alignment_required: bool = False

    # Vulnerability Thresholds
    max_critical_vulnerabilities: int = 999  # 999 = unlimited
    max_high_vulnerabilities: int = 999
    max_medium_vulnerabilities: int = 999

    # Conformance Thresholds
    min_conformance_score: int = 0  # 0-100

    # Enforcement Mode
    enforcement_mode: str = "advisory"

    # Optional Overrides
    custom_rules: dict = field(default_factory=dict)

    def is_test_required(self) -> bool:
        """Check if test evidence is required for this tier."""
        return self.test_required

    def is_security_required(self) -> bool:
        """Check if security scan is required for this tier."""
        return self.security_scan_required

    def get_required_checks(self) -> list[str]:
        """Get list of required checks for this tier."""
        checks = []
        if self.test_required:
            checks.append("test")
        if self.lint_required:
            checks.append("lint")
        if self.security_scan_required:
            checks.append("security")
        if self.build_verification_required:
            checks.append("build")
        if self.conformance_check_required:
            checks.append("conformance")
        if self.risk_analysis_required:
            checks.append("risk_analysis")
        if self.adr_alignment_required:
            checks.append("adr_alignment")
        return checks

    def get_mrp_points_required(self) -> int:
        """Get number of MRP points required for this tier (0-5)."""
        count = 0
        if self.test_required:
            count += 1
        if self.lint_required:
            count += 1
        if self.security_scan_required:
            count += 1
        if self.build_verification_required:
            count += 1
        if self.conformance_check_required:
            count += 1
        return count


# =========================================================================
# Tier Policy Definitions (SDLC 5.2.0)
# =========================================================================

TIER_POLICIES: dict[PolicyTier, TierPolicy] = {
    PolicyTier.LITE: TierPolicy(
        tier=PolicyTier.LITE,
        display_name="Lite",
        description="Advisory mode for individuals and prototypes. "
                    "All checks are recommendations only.",
        target_audience="Individuals, side projects, prototypes, learning",

        # Evidence Requirements (all optional)
        test_required=False,
        test_coverage_required=0,
        lint_required=False,
        security_scan_required=False,
        build_verification_required=False,
        conformance_check_required=False,

        # Additional Checks
        risk_analysis_required=False,
        crp_required_for_high_risk=False,
        adr_alignment_required=False,

        # Vulnerability Thresholds (unlimited)
        max_critical_vulnerabilities=999,
        max_high_vulnerabilities=999,
        max_medium_vulnerabilities=999,

        # Conformance Thresholds
        min_conformance_score=0,

        # Enforcement Mode
        enforcement_mode="advisory",
    ),

    PolicyTier.STANDARD: TierPolicy(
        tier=PolicyTier.STANDARD,
        display_name="Standard",
        description="Soft enforcement for small teams. "
                    "Core checks required with reasonable thresholds.",
        target_audience="Small teams (2-5 developers), early-stage startups",

        # Evidence Requirements
        test_required=True,
        test_coverage_required=80,  # 80% coverage
        lint_required=True,
        security_scan_required=True,
        build_verification_required=False,  # Not required for Standard
        conformance_check_required=False,   # Not required for Standard

        # Additional Checks
        risk_analysis_required=True,   # Risk analysis from Sprint 101
        crp_required_for_high_risk=False,  # No CRP for Standard
        adr_alignment_required=False,

        # Vulnerability Thresholds
        max_critical_vulnerabilities=0,  # No critical allowed
        max_high_vulnerabilities=5,      # Up to 5 high allowed
        max_medium_vulnerabilities=20,   # Up to 20 medium allowed

        # Conformance Thresholds
        min_conformance_score=50,  # 50% minimum

        # Enforcement Mode
        enforcement_mode="soft",
    ),

    PolicyTier.PROFESSIONAL: TierPolicy(
        tier=PolicyTier.PROFESSIONAL,
        display_name="Professional",
        description="Hard enforcement for medium teams. "
                    "All MRP points required with strict thresholds.",
        target_audience="Medium teams (5-15 developers), growth-stage companies",

        # Evidence Requirements (all required)
        test_required=True,
        test_coverage_required=90,  # 90% coverage
        lint_required=True,
        security_scan_required=True,
        build_verification_required=True,
        conformance_check_required=True,

        # Additional Checks
        risk_analysis_required=True,
        crp_required_for_high_risk=True,  # CRP for high-risk changes
        adr_alignment_required=True,

        # Vulnerability Thresholds
        max_critical_vulnerabilities=0,  # No critical allowed
        max_high_vulnerabilities=2,      # Up to 2 high allowed
        max_medium_vulnerabilities=10,   # Up to 10 medium allowed

        # Conformance Thresholds
        min_conformance_score=70,  # 70% minimum

        # Enforcement Mode
        enforcement_mode="hard",
    ),

    PolicyTier.ENTERPRISE: TierPolicy(
        tier=PolicyTier.ENTERPRISE,
        display_name="Enterprise",
        description="Strictest enforcement for large organizations. "
                    "Zero tolerance for violations, full audit trail.",
        target_audience="Large organizations (15+ developers), enterprise, regulated industries",

        # Evidence Requirements (all required)
        test_required=True,
        test_coverage_required=95,  # 95% coverage
        lint_required=True,
        security_scan_required=True,
        build_verification_required=True,
        conformance_check_required=True,

        # Additional Checks
        risk_analysis_required=True,
        crp_required_for_high_risk=True,  # CRP for high-risk changes
        adr_alignment_required=True,

        # Vulnerability Thresholds (zero tolerance for high/critical)
        max_critical_vulnerabilities=0,  # No critical allowed
        max_high_vulnerabilities=0,      # No high allowed
        max_medium_vulnerabilities=5,    # Up to 5 medium allowed

        # Conformance Thresholds
        min_conformance_score=85,  # 85% minimum

        # Enforcement Mode
        enforcement_mode="hard",
    ),
}


# =========================================================================
# Utility Functions
# =========================================================================

def get_tier_policy(tier: PolicyTier | str) -> TierPolicy:
    """
    Get policy configuration for a specific tier.

    Args:
        tier: PolicyTier enum or tier name string

    Returns:
        TierPolicy for the specified tier

    Raises:
        ValueError: If tier is not valid

    Example:
        policy = get_tier_policy(PolicyTier.PROFESSIONAL)
        policy = get_tier_policy("PROFESSIONAL")
    """
    if isinstance(tier, str):
        try:
            tier = PolicyTier(tier.upper())
        except ValueError:
            raise ValueError(
                f"Invalid tier: {tier}. Valid tiers: {[t.value for t in PolicyTier]}"
            )

    if tier not in TIER_POLICIES:
        raise ValueError(f"No policy defined for tier: {tier}")

    return TIER_POLICIES[tier]


def get_all_tiers() -> list[TierPolicy]:
    """
    Get all tier policies in order from least to most strict.

    Returns:
        List of TierPolicy objects ordered by strictness

    Example:
        tiers = get_all_tiers()
        for tier in tiers:
            print(f"{tier.display_name}: {tier.enforcement_mode}")
    """
    return [
        TIER_POLICIES[PolicyTier.LITE],
        TIER_POLICIES[PolicyTier.STANDARD],
        TIER_POLICIES[PolicyTier.PROFESSIONAL],
        TIER_POLICIES[PolicyTier.ENTERPRISE],
    ]


def compare_tiers(
    current_tier: PolicyTier | str,
    target_tier: PolicyTier | str,
) -> dict:
    """
    Compare two tiers and return differences.

    Useful for tier upgrade/downgrade flows.

    Args:
        current_tier: Current tier
        target_tier: Target tier

    Returns:
        Dict with comparison details:
        - direction: "upgrade" | "downgrade" | "same"
        - new_requirements: List of new requirements
        - removed_requirements: List of removed requirements
        - stricter_thresholds: Dict of stricter thresholds
        - relaxed_thresholds: Dict of relaxed thresholds

    Example:
        diff = compare_tiers("STANDARD", "PROFESSIONAL")
        if diff["direction"] == "upgrade":
            print("New requirements:", diff["new_requirements"])
    """
    current_policy = get_tier_policy(current_tier)
    target_policy = get_tier_policy(target_tier)

    # Determine direction
    tier_order = [PolicyTier.LITE, PolicyTier.STANDARD,
                  PolicyTier.PROFESSIONAL, PolicyTier.ENTERPRISE]
    current_idx = tier_order.index(current_policy.tier)
    target_idx = tier_order.index(target_policy.tier)

    if target_idx > current_idx:
        direction = "upgrade"
    elif target_idx < current_idx:
        direction = "downgrade"
    else:
        direction = "same"

    # Compare requirements
    current_checks = set(current_policy.get_required_checks())
    target_checks = set(target_policy.get_required_checks())

    new_requirements = list(target_checks - current_checks)
    removed_requirements = list(current_checks - target_checks)

    # Compare thresholds
    stricter_thresholds = {}
    relaxed_thresholds = {}

    # Test coverage
    if target_policy.test_coverage_required > current_policy.test_coverage_required:
        stricter_thresholds["test_coverage"] = {
            "current": current_policy.test_coverage_required,
            "target": target_policy.test_coverage_required,
        }
    elif target_policy.test_coverage_required < current_policy.test_coverage_required:
        relaxed_thresholds["test_coverage"] = {
            "current": current_policy.test_coverage_required,
            "target": target_policy.test_coverage_required,
        }

    # Conformance score
    if target_policy.min_conformance_score > current_policy.min_conformance_score:
        stricter_thresholds["conformance_score"] = {
            "current": current_policy.min_conformance_score,
            "target": target_policy.min_conformance_score,
        }
    elif target_policy.min_conformance_score < current_policy.min_conformance_score:
        relaxed_thresholds["conformance_score"] = {
            "current": current_policy.min_conformance_score,
            "target": target_policy.min_conformance_score,
        }

    # Vulnerability thresholds (lower = stricter)
    if target_policy.max_high_vulnerabilities < current_policy.max_high_vulnerabilities:
        stricter_thresholds["max_high_vulnerabilities"] = {
            "current": current_policy.max_high_vulnerabilities,
            "target": target_policy.max_high_vulnerabilities,
        }
    elif target_policy.max_high_vulnerabilities > current_policy.max_high_vulnerabilities:
        relaxed_thresholds["max_high_vulnerabilities"] = {
            "current": current_policy.max_high_vulnerabilities,
            "target": target_policy.max_high_vulnerabilities,
        }

    return {
        "current_tier": current_policy.tier.value,
        "target_tier": target_policy.tier.value,
        "direction": direction,
        "new_requirements": new_requirements,
        "removed_requirements": removed_requirements,
        "stricter_thresholds": stricter_thresholds,
        "relaxed_thresholds": relaxed_thresholds,
        "current_mrp_points": current_policy.get_mrp_points_required(),
        "target_mrp_points": target_policy.get_mrp_points_required(),
    }


def get_default_tier() -> PolicyTier:
    """
    Get the default policy tier for new projects.

    Returns:
        PolicyTier.PROFESSIONAL (default for SDLC Orchestrator)
    """
    return PolicyTier.PROFESSIONAL


def is_stricter_tier(tier_a: PolicyTier, tier_b: PolicyTier) -> bool:
    """
    Check if tier_a is stricter than tier_b.

    Args:
        tier_a: First tier
        tier_b: Second tier

    Returns:
        True if tier_a is stricter than tier_b

    Example:
        is_stricter_tier(PolicyTier.ENTERPRISE, PolicyTier.STANDARD)  # True
        is_stricter_tier(PolicyTier.LITE, PolicyTier.PROFESSIONAL)  # False
    """
    tier_order = [PolicyTier.LITE, PolicyTier.STANDARD,
                  PolicyTier.PROFESSIONAL, PolicyTier.ENTERPRISE]
    return tier_order.index(tier_a) > tier_order.index(tier_b)
