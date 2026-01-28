"""
=========================================================================
FULL Mode Enforcer - Sprint 116 Track 2 Production Governance
SDLC Orchestrator - Anti-Vibecoding System

Version: 1.0.0
Date: January 28, 2026 (Prepared ahead of Feb 17 kickoff)
Status: READY FOR DEPLOYMENT
Authority: CTO Approved (Sprint 115 GO Decision Pending)
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Implement FULL enforcement mode (strict blocking)
- Only GREEN zone auto-approves
- YELLOW requires Tech Lead approval
- ORANGE requires CEO approval
- RED blocked with CTO+CEO override
- Track CEO time savings (target: -75%)

FULL Mode Rules:
- GREEN (0-30): AUTO-APPROVED (no review)
- YELLOW (31-60): REQUIRES Tech Lead approval
- ORANGE (61-80): REQUIRES CEO approval
- RED (81-100): BLOCKED (CTO+CEO override required)

Zero Mock Policy: Real enforcement with configurable rules
=========================================================================
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID

import yaml

from app.services.governance.signals_engine import (
    CodeSubmission,
    IndexCategory,
    RoutingDecision,
    VibecodingIndex,
)
from app.services.governance.soft_mode_enforcer import (
    BlockRuleResult,
    EnforcementAction,
    EnforcementResult,
    ExemptionResult,
    ExemptionType,
    SoftModeEnforcer,
    WarnRuleResult,
)

logger = logging.getLogger(__name__)


# ============================================================================
# FULL Mode Specific Enums
# ============================================================================


class ApprovalRequirement(str, Enum):
    """Approval requirements for FULL mode."""

    NONE = "none"
    TECH_LEAD = "tech_lead"
    CEO = "ceo"
    CTO_CEO = "cto_ceo"


class ApprovalStatus(str, Enum):
    """Status of approval request."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    ESCALATED = "escalated"


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class ApprovalRequest:
    """Request for approval in FULL mode."""

    id: str
    pr_number: int
    zone: IndexCategory
    vibecoding_index: float
    required_approvers: List[str]
    requested_at: datetime
    timeout_hours: int
    status: ApprovalStatus = ApprovalStatus.PENDING
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None


@dataclass
class CEOTimeEntry:
    """Track CEO time spent on governance activities."""

    id: str
    activity_type: str
    pr_number: Optional[int]
    duration_minutes: float
    category: str
    recorded_at: datetime
    notes: Optional[str] = None


@dataclass
class FullModeEnforcementResult(EnforcementResult):
    """Extended enforcement result for FULL mode."""

    approval_required: bool = False
    approval_type: ApprovalRequirement = ApprovalRequirement.NONE
    approval_request: Optional[ApprovalRequest] = None
    ceo_review_required: bool = False
    estimated_review_time_minutes: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        base_dict = super().to_dict()
        base_dict.update({
            "full_mode": {
                "approval_required": self.approval_required,
                "approval_type": self.approval_type.value,
                "ceo_review_required": self.ceo_review_required,
                "estimated_review_time_minutes": self.estimated_review_time_minutes,
            }
        })
        return base_dict


# ============================================================================
# FULL Mode Enforcer Service
# ============================================================================


class FullModeEnforcer(SoftModeEnforcer):
    """
    FULL Mode Enforcement Service.

    Extends SoftModeEnforcer with stricter rules:
    - Only GREEN auto-approves
    - YELLOW requires Tech Lead approval
    - ORANGE requires CEO approval
    - RED blocked with CTO+CEO override

    Also integrates CEO time tracking for measuring governance impact.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize FULL Mode Enforcer.

        Args:
            config_path: Path to governance_full_mode.yaml (optional)
        """
        # Initialize parent with SOFT mode config
        super().__init__(config_path)

        # Load FULL mode specific config
        self.full_config = self._load_full_config(config_path)

        # Approval tracking
        self._pending_approvals: Dict[str, ApprovalRequest] = {}

        # CEO time tracking
        self._ceo_time_entries: List[CEOTimeEntry] = []
        self._ceo_time_baseline = self.full_config.get(
            "ceo_time_tracking", {}
        ).get("baseline_hours_per_week", 40)
        self._ceo_time_target = self.full_config.get(
            "ceo_time_tracking", {}
        ).get("target_hours_per_week", 10)

        logger.info("FullModeEnforcer initialized")

    def _load_full_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load FULL mode configuration."""
        default_path = Path(__file__).parent.parent.parent / "config" / "governance_full_mode.yaml"
        path = Path(config_path) if config_path else default_path

        try:
            with open(path, "r") as f:
                config = yaml.safe_load(f)
                logger.info(f"Loaded FULL mode config from {path}")
                return config
        except FileNotFoundError:
            logger.warning(f"FULL mode config not found at {path}, using defaults")
            return self._get_default_full_config()

    def _get_default_full_config(self) -> Dict[str, Any]:
        """Get default FULL mode configuration."""
        return {
            "mode": "full",
            "zone_thresholds": {
                "green": {"min": 0, "max": 30, "action": "auto_approve"},
                "yellow": {"min": 31, "max": 60, "action": "require_approval", "review": "tech_lead"},
                "orange": {"min": 61, "max": 80, "action": "require_approval", "review": "ceo"},
                "red": {"min": 81, "max": 100, "action": "blocked", "review": "cto_ceo"},
            },
            "approval_rules": {
                "yellow_zone_tech_lead": {
                    "enabled": True,
                    "zone": "yellow",
                    "requires": ["Tech Lead"],
                    "timeout_hours": 24,
                },
                "orange_zone_ceo": {
                    "enabled": True,
                    "zone": "orange",
                    "requires": ["CEO"],
                    "timeout_hours": 48,
                },
            },
            "ceo_time_tracking": {
                "enabled": True,
                "baseline_hours_per_week": 40,
                "target_hours_per_week": 10,
            },
            "kill_switch": {
                "rejection_rate": {"threshold": 0.5},
                "false_positive_rate": {"threshold": 0.15},
            },
        }

    # ========================================================================
    # FULL Mode Enforcement
    # ========================================================================

    def enforce_full(
        self,
        vibecoding_index: VibecodingIndex,
        submission: CodeSubmission,
        has_ownership: bool = True,
        has_intent: bool = True,
        security_scan_critical: int = 0,
        has_adr_linkage: bool = True,
        test_coverage: float = 80.0,
        coverage_delta: float = 0.0,
    ) -> FullModeEnforcementResult:
        """
        Evaluate FULL mode enforcement for a PR.

        FULL Mode Rules:
        - GREEN (0-30): AUTO-APPROVED
        - YELLOW (31-60): Requires Tech Lead approval
        - ORANGE (61-80): Requires CEO approval
        - RED (81-100): BLOCKED (CTO+CEO override)

        Args:
            vibecoding_index: Calculated Vibecoding Index
            submission: Code submission details
            has_ownership: Whether PR has @owner annotation
            has_intent: Whether PR has intent statement
            security_scan_critical: Number of critical security issues
            has_adr_linkage: Whether new features have ADR linkage
            test_coverage: Test coverage percentage
            coverage_delta: Change in test coverage (negative = drop)

        Returns:
            FullModeEnforcementResult with action, approvals, and CEO time estimate
        """
        # First, run SOFT mode enforcement (handles exemptions and basic rules)
        soft_result = self.enforce(
            vibecoding_index=vibecoding_index,
            submission=submission,
            has_ownership=has_ownership,
            has_intent=has_intent,
            security_scan_critical=security_scan_critical,
            has_adr_linkage=has_adr_linkage,
            test_coverage=test_coverage,
        )

        # Check coverage drop (FULL mode specific)
        coverage_block = self._check_coverage_drop(coverage_delta)
        if coverage_block.triggered:
            soft_result.block_rules_triggered.append(coverage_block)

        # Determine FULL mode specific behavior
        adjusted_index = soft_result.vibecoding_index
        approval_required = False
        approval_type = ApprovalRequirement.NONE
        ceo_review_required = False
        estimated_review_time = 0.0

        # Determine approval requirements based on zone (always compute, even if blocked)
        if adjusted_index.category == IndexCategory.YELLOW:
            approval_required = True
            approval_type = ApprovalRequirement.TECH_LEAD
            estimated_review_time = 15.0  # 15 min Tech Lead review

        elif adjusted_index.category == IndexCategory.ORANGE:
            approval_required = True
            approval_type = ApprovalRequirement.CEO
            ceo_review_required = True
            estimated_review_time = 30.0  # 30 min CEO review

        elif adjusted_index.category == IndexCategory.RED:
            # RED is blocked in FULL mode (requires override)
            approval_required = True
            approval_type = ApprovalRequirement.CTO_CEO
            ceo_review_required = True
            estimated_review_time = 60.0  # 60 min for CTO+CEO review

        # Determine final action
        action, can_merge, message = self._determine_full_mode_action(
            soft_result, approval_required, approval_type, coverage_block
        )

        # Create approval request if needed
        approval_request = None
        if approval_required and action != EnforcementAction.BLOCKED:
            approval_request = self._create_approval_request(
                pr_number=getattr(submission, 'pr_number', 0),
                zone=adjusted_index.category,
                vibecoding_index=adjusted_index.score,
                approval_type=approval_type,
            )

        return FullModeEnforcementResult(
            action=action,
            vibecoding_index=adjusted_index,
            exemptions_applied=soft_result.exemptions_applied,
            block_rules_triggered=soft_result.block_rules_triggered,
            warn_rules_triggered=soft_result.warn_rules_triggered,
            can_merge=can_merge,
            requires_override=soft_result.requires_override,
            override_authority=soft_result.override_authority,
            message=message,
            details=soft_result.details,
            approval_required=approval_required,
            approval_type=approval_type,
            approval_request=approval_request,
            ceo_review_required=ceo_review_required,
            estimated_review_time_minutes=estimated_review_time,
        )

    def _check_coverage_drop(self, coverage_delta: float) -> BlockRuleResult:
        """Check if coverage dropped below threshold."""
        threshold = self.full_config.get("block_rules", {}).get(
            "coverage_drop", {}
        ).get("threshold", -5)

        triggered = coverage_delta < threshold

        return BlockRuleResult(
            rule_name="coverage_drop",
            triggered=triggered,
            message=f"PR blocked: Test coverage dropped by {abs(coverage_delta):.1f}% (threshold: {abs(threshold)}%)"
            if triggered else "",
            override_allowed=True,
            override_requires=["Tech Lead"],
        )

    def _determine_full_mode_action(
        self,
        soft_result: EnforcementResult,
        approval_required: bool,
        approval_type: ApprovalRequirement,
        coverage_block: BlockRuleResult,
    ) -> tuple:
        """
        Determine final action for FULL mode.

        Returns:
            (action, can_merge, message)
        """
        # Check for blocks first
        all_blocks = [
            b for b in soft_result.block_rules_triggered
            if b.triggered
        ]
        if coverage_block.triggered:
            all_blocks.append(coverage_block)

        if all_blocks:
            return (
                EnforcementAction.BLOCKED,
                False,
                all_blocks[0].message,
            )

        # Check for approval requirements
        if approval_required:
            if approval_type == ApprovalRequirement.TECH_LEAD:
                return (
                    EnforcementAction.WARNED,  # Use WARNED to indicate pending
                    False,  # Can't merge until approved
                    f"Requires Tech Lead approval (Vibecoding Index in yellow zone)",
                )
            elif approval_type == ApprovalRequirement.CEO:
                return (
                    EnforcementAction.WARNED,
                    False,
                    f"Requires CEO approval (Vibecoding Index in orange zone)",
                )
            elif approval_type == ApprovalRequirement.CTO_CEO:
                return (
                    EnforcementAction.BLOCKED,
                    False,
                    f"Requires CTO+CEO override (Vibecoding Index in red zone)",
                )

        # GREEN zone - auto-approve
        return (
            EnforcementAction.AUTO_APPROVED,
            True,
            f"Auto-approved: Vibecoding Index {soft_result.vibecoding_index.score:.1f} in green zone",
        )

    def _create_approval_request(
        self,
        pr_number: int,
        zone: IndexCategory,
        vibecoding_index: float,
        approval_type: ApprovalRequirement,
    ) -> ApprovalRequest:
        """Create an approval request for tracking."""
        import uuid

        # Determine timeout based on approval type
        timeout_hours = 24 if approval_type == ApprovalRequirement.TECH_LEAD else 48

        # Determine required approvers
        approvers = {
            ApprovalRequirement.TECH_LEAD: ["Tech Lead"],
            ApprovalRequirement.CEO: ["CEO"],
            ApprovalRequirement.CTO_CEO: ["CTO", "CEO"],
        }.get(approval_type, [])

        request = ApprovalRequest(
            id=str(uuid.uuid4())[:8],
            pr_number=pr_number,
            zone=zone,
            vibecoding_index=vibecoding_index,
            required_approvers=approvers,
            requested_at=datetime.utcnow(),
            timeout_hours=timeout_hours,
        )

        # Store for tracking
        self._pending_approvals[request.id] = request

        logger.info(
            f"Created approval request {request.id} for PR #{pr_number}: "
            f"requires {approvers}"
        )

        return request

    # ========================================================================
    # Approval Management
    # ========================================================================

    def approve(
        self,
        request_id: str,
        approved_by: str,
        approver_role: str,
    ) -> bool:
        """
        Approve a pending request.

        Args:
            request_id: Approval request ID
            approved_by: Username of approver
            approver_role: Role of approver (Tech Lead, CEO, CTO)

        Returns:
            True if approval successful, False otherwise
        """
        request = self._pending_approvals.get(request_id)
        if not request:
            logger.warning(f"Approval request {request_id} not found")
            return False

        if request.status != ApprovalStatus.PENDING:
            logger.warning(f"Approval request {request_id} not pending: {request.status}")
            return False

        # Check if approver has required role
        if approver_role not in request.required_approvers:
            logger.warning(
                f"Approver {approved_by} ({approver_role}) not authorized. "
                f"Required: {request.required_approvers}"
            )
            return False

        # Approve
        request.status = ApprovalStatus.APPROVED
        request.approved_by = approved_by
        request.approved_at = datetime.utcnow()

        logger.info(
            f"Approval request {request_id} approved by {approved_by} ({approver_role})"
        )

        # Track CEO time if CEO approved
        if approver_role == "CEO":
            self._record_ceo_time(
                activity_type="pr_approval",
                pr_number=request.pr_number,
                duration_minutes=30.0,  # Estimated review time
                category="governance",
            )

        return True

    def reject(
        self,
        request_id: str,
        rejected_by: str,
        reason: str,
    ) -> bool:
        """
        Reject a pending request.

        Args:
            request_id: Approval request ID
            rejected_by: Username of rejector
            reason: Rejection reason

        Returns:
            True if rejection successful, False otherwise
        """
        request = self._pending_approvals.get(request_id)
        if not request:
            logger.warning(f"Approval request {request_id} not found")
            return False

        request.status = ApprovalStatus.REJECTED
        request.rejection_reason = reason

        logger.info(
            f"Approval request {request_id} rejected by {rejected_by}: {reason}"
        )

        return True

    def get_pending_approvals(
        self,
        approver_role: Optional[str] = None,
    ) -> List[ApprovalRequest]:
        """
        Get pending approval requests.

        Args:
            approver_role: Filter by approver role (optional)

        Returns:
            List of pending approval requests
        """
        pending = [
            r for r in self._pending_approvals.values()
            if r.status == ApprovalStatus.PENDING
        ]

        if approver_role:
            pending = [
                r for r in pending
                if approver_role in r.required_approvers
            ]

        return pending

    # ========================================================================
    # CEO Time Tracking
    # ========================================================================

    def _record_ceo_time(
        self,
        activity_type: str,
        pr_number: Optional[int],
        duration_minutes: float,
        category: str,
        notes: Optional[str] = None,
    ) -> CEOTimeEntry:
        """Record CEO time entry."""
        import uuid

        entry = CEOTimeEntry(
            id=str(uuid.uuid4())[:8],
            activity_type=activity_type,
            pr_number=pr_number,
            duration_minutes=duration_minutes,
            category=category,
            recorded_at=datetime.utcnow(),
            notes=notes,
        )

        self._ceo_time_entries.append(entry)

        logger.info(
            f"CEO time recorded: {duration_minutes:.1f} min for {activity_type}"
        )

        return entry

    def get_ceo_time_summary(
        self,
        days: int = 7,
    ) -> Dict[str, Any]:
        """
        Get CEO time summary for the last N days.

        Args:
            days: Number of days to include

        Returns:
            Summary dict with total hours, breakdown, and savings
        """
        from datetime import timedelta

        cutoff = datetime.utcnow() - timedelta(days=days)
        recent_entries = [
            e for e in self._ceo_time_entries
            if e.recorded_at >= cutoff
        ]

        total_minutes = sum(e.duration_minutes for e in recent_entries)
        total_hours = total_minutes / 60

        # Calculate breakdown by category
        breakdown = {}
        for entry in recent_entries:
            cat = entry.category
            breakdown[cat] = breakdown.get(cat, 0) + entry.duration_minutes

        # Calculate savings
        baseline_hours = self._ceo_time_baseline * (days / 7)
        savings_hours = baseline_hours - total_hours
        savings_percent = (savings_hours / baseline_hours * 100) if baseline_hours > 0 else 0

        return {
            "period_days": days,
            "total_hours": round(total_hours, 2),
            "baseline_hours": round(baseline_hours, 2),
            "target_hours": round(self._ceo_time_target * (days / 7), 2),
            "savings_hours": round(max(0, savings_hours), 2),
            "savings_percent": round(max(0, savings_percent), 1),
            "on_target": total_hours <= self._ceo_time_target * (days / 7),
            "breakdown_minutes": breakdown,
            "entry_count": len(recent_entries),
        }

    def record_manual_ceo_time(
        self,
        activity_type: str,
        duration_minutes: float,
        pr_number: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> CEOTimeEntry:
        """
        Manually record CEO time (for activities not auto-tracked).

        Args:
            activity_type: Type of activity
            duration_minutes: Time spent in minutes
            pr_number: Associated PR number (optional)
            notes: Additional notes

        Returns:
            Created CEOTimeEntry
        """
        category = self._categorize_activity(activity_type)
        return self._record_ceo_time(
            activity_type=activity_type,
            pr_number=pr_number,
            duration_minutes=duration_minutes,
            category=category,
            notes=notes,
        )

    def _categorize_activity(self, activity_type: str) -> str:
        """Categorize activity type for reporting."""
        categories = {
            "pr_review": "code_review",
            "pr_approval": "governance",
            "override_approval": "governance",
            "architecture_review": "design",
            "security_review": "security",
            "planning": "planning",
            "meeting": "meeting",
        }
        return categories.get(activity_type, "other")

    # ========================================================================
    # Kill Switch Integration
    # ========================================================================

    def check_kill_switch(self) -> Optional[Dict[str, Any]]:
        """
        Check if FULL mode should trigger kill switch.

        FULL mode has stricter thresholds than SOFT mode.

        Returns:
            Dict with trigger reason if triggered, None otherwise
        """
        kill_config = self.full_config.get("kill_switch", {})

        # Calculate current metrics
        total = len(self._pending_approvals) + 1  # Avoid division by zero
        blocked = sum(
            1 for r in self._pending_approvals.values()
            if r.status == ApprovalStatus.REJECTED
        )
        rejection_rate = blocked / total

        # Check rejection rate (stricter: 50% vs 80%)
        threshold = kill_config.get("criteria", {}).get(
            "rejection_rate", {}
        ).get("threshold", 0.5)
        if rejection_rate > threshold:
            return {
                "trigger": "rejection_rate",
                "current": rejection_rate,
                "threshold": threshold,
                "action": "rollback_to_soft",
                "message": f"Rejection rate {rejection_rate:.1%} > {threshold:.1%}",
            }

        return None


# ============================================================================
# Factory Functions
# ============================================================================

_full_mode_enforcer: Optional[FullModeEnforcer] = None


def create_full_mode_enforcer(config_path: Optional[str] = None) -> FullModeEnforcer:
    """
    Create a FullModeEnforcer instance.

    Args:
        config_path: Optional path to configuration file

    Returns:
        Configured FullModeEnforcer instance
    """
    return FullModeEnforcer(config_path)


def get_full_mode_enforcer() -> FullModeEnforcer:
    """
    Get or create FullModeEnforcer singleton.

    Returns:
        FullModeEnforcer singleton instance
    """
    global _full_mode_enforcer
    if _full_mode_enforcer is None:
        _full_mode_enforcer = create_full_mode_enforcer()
    return _full_mode_enforcer
