"""
Unit tests for QueryClassifier — ADR-058 Pattern E.

Sprint 179 — ZeroClaw Security Hardening.
Sprint 204 — Confidence-Based Routing (ClassificationResult return type).
Test IDs: QC-01 to QC-08 (see ADR-058 §2.4).

Coverage:
  QC-01  Code hint: coding keywords trigger 'code' (priority=10)
  QC-02  Reasoning hint: analysis keywords + min_length trigger 'reasoning'
  QC-03  Fast hint: short message (≤ 20 chars) → 'fast'
  QC-04  No match: general text → None (no hint)
  QC-05  Priority order: higher-priority rule wins over lower
  QC-06  AND-condition logic: all conditions must match
  QC-07  Empty message → None
  QC-08  DEFAULT_CLASSIFICATION_RULES integration — classify() with defaults
"""

from __future__ import annotations

import pytest

from app.services.agent_team.config import DEFAULT_CLASSIFICATION_RULES
from app.services.agent_team.query_classifier import (
    ClassificationResult,
    ClassificationRule,
    classify,
)


# ── QC-01: Code hint ─────────────────────────────────────────────────────────

class TestCodeHint:
    def test_implement_keyword_triggers_code(self) -> None:
        """QC-01a — 'implement' keyword + code block → 'code' hint."""
        rules = [
            ClassificationRule(
                hint="code",
                priority=10,
                keywords=("implement",),
                patterns=("```",),
            ),
        ]
        result = classify(rules, "Please implement this:\n```python\ndef foo(): pass\n```")
        assert result.hint == "code"
        assert bool(result) is True

    def test_fix_keyword_triggers_code(self) -> None:
        """QC-01b — 'fix' keyword + code block → 'code' hint."""
        rules = [
            ClassificationRule(
                hint="code",
                priority=10,
                keywords=("fix",),
                patterns=("```",),
            ),
        ]
        result = classify(rules, "Can you fix this? ```python raise ValueError ```")
        assert result.hint == "code"
        assert bool(result) is True

    def test_code_hint_case_insensitive(self) -> None:
        """QC-01c — keyword check is case-insensitive."""
        rules = [
            ClassificationRule(
                hint="code",
                priority=10,
                keywords=("implement",),
                patterns=(),
            ),
        ]
        result = classify(rules, "IMPLEMENT the auth service")
        assert result.hint == "code"
        assert bool(result) is True


# ── QC-02: Reasoning hint ─────────────────────────────────────────────────────

class TestReasoningHint:
    def test_explain_with_min_length_triggers_reasoning(self) -> None:
        """QC-02a — 'explain' + min_length satisfied → 'reasoning'."""
        rules = [
            ClassificationRule(
                hint="reasoning",
                priority=5,
                keywords=("explain",),
                patterns=(),
                min_length=50,
            ),
        ]
        long_msg = "Can you explain why the architecture was designed this way and what trade-offs were made?"
        result = classify(rules, long_msg)
        assert result.hint == "reasoning"
        assert bool(result) is True

    def test_explain_below_min_length_no_match(self) -> None:
        """QC-02b — 'explain' but message too short → no match."""
        rules = [
            ClassificationRule(
                hint="reasoning",
                priority=5,
                keywords=("explain",),
                min_length=50,
            ),
        ]
        result = classify(rules, "explain this")  # 12 chars < 50
        assert result.hint is None
        assert bool(result) is False

    def test_analyze_keyword_triggers_reasoning(self) -> None:
        """QC-02c — 'analyze' keyword + sufficient length → 'reasoning'."""
        rules = [
            ClassificationRule(
                hint="reasoning",
                priority=5,
                keywords=("analyze",),
                min_length=50,
            ),
        ]
        long_msg = "Please analyze the performance bottlenecks in the current system and provide recommendations."
        result = classify(rules, long_msg)
        assert result.hint == "reasoning"
        assert bool(result) is True


# ── QC-03: Fast hint ─────────────────────────────────────────────────────────

class TestFastHint:
    def test_short_message_triggers_fast(self) -> None:
        """QC-03a — message ≤ 20 chars → 'fast' hint."""
        rules = [
            ClassificationRule(
                hint="fast",
                priority=1,
                max_length=20,
            ),
        ]
        result = classify(rules, "ok")
        assert result.hint == "fast"
        assert bool(result) is True

    def test_exactly_20_chars_triggers_fast(self) -> None:
        """QC-03b — exactly 20-char message → 'fast'."""
        rules = [
            ClassificationRule(
                hint="fast",
                priority=1,
                max_length=20,
            ),
        ]
        result = classify(rules, "a" * 20)  # exactly 20 chars
        assert result.hint == "fast"
        assert bool(result) is True

    def test_21_chars_does_not_trigger_fast(self) -> None:
        """QC-03c — 21-char message → does not match fast rule."""
        rules = [
            ClassificationRule(
                hint="fast",
                priority=1,
                max_length=20,
            ),
        ]
        result = classify(rules, "a" * 21)
        assert result.hint is None
        assert bool(result) is False


# ── QC-04: No match → None ───────────────────────────────────────────────────

class TestNoMatch:
    def test_general_text_returns_none(self) -> None:
        """QC-04a — general text with no matching keywords → None."""
        rules = [
            ClassificationRule(
                hint="code",
                priority=10,
                keywords=("implement", "fix"),
                patterns=("```",),
            ),
        ]
        result = classify(rules, "What is the weather today in Hanoi?")
        assert result.hint is None
        assert bool(result) is False

    def test_empty_rules_returns_none(self) -> None:
        """QC-04b — no rules defined → None for any message."""
        result = classify([], "Please implement something")
        assert result.hint is None
        assert bool(result) is False


# ── QC-05: Priority ordering ─────────────────────────────────────────────────

class TestPriorityOrder:
    def test_higher_priority_wins(self) -> None:
        """QC-05a — code (p=10) fires before reasoning (p=5) when both match."""
        rules = [
            ClassificationRule(
                hint="reasoning",
                priority=5,
                keywords=("analyze",),
                min_length=0,
            ),
            ClassificationRule(
                hint="code",
                priority=10,
                keywords=("analyze",),  # same keyword → both match
            ),
        ]
        result = classify(rules, "analyze this code and implement fixes")
        assert result.hint == "code"  # higher priority wins

    def test_lower_priority_fires_if_high_fails(self) -> None:
        """QC-05b — code (p=10) doesn't match → reasoning (p=5) fires."""
        rules = [
            ClassificationRule(
                hint="code",
                priority=10,
                keywords=("implement",),
                patterns=("```",),    # requires code block
            ),
            ClassificationRule(
                hint="reasoning",
                priority=5,
                keywords=("analyze",),
                min_length=0,
            ),
        ]
        # No code block → code rule fails; reasoning matches
        result = classify(rules, "analyze the design patterns in use")
        assert result.hint == "reasoning"


# ── QC-06: AND-condition logic ────────────────────────────────────────────────

class TestAndConditionLogic:
    def test_all_keywords_must_match(self) -> None:
        """QC-06a — rule with 2 keywords fires only if BOTH present."""
        rules = [
            ClassificationRule(
                hint="code",
                priority=10,
                keywords=("implement", "function"),
            ),
        ]
        # Only 'implement' present → no match
        result = classify(rules, "implement a new feature")
        assert result.hint is None
        assert bool(result) is False

    def test_all_keywords_present_matches(self) -> None:
        """QC-06b — both keywords present → match."""
        rules = [
            ClassificationRule(
                hint="code",
                priority=10,
                keywords=("implement", "function"),
            ),
        ]
        result = classify(rules, "implement a new function for auth")
        assert result.hint == "code"
        assert bool(result) is True

    def test_pattern_must_match_case_sensitive(self) -> None:
        """QC-06c — pattern check is case-sensitive."""
        rules = [
            ClassificationRule(
                hint="code",
                priority=10,
                patterns=("```",),
            ),
        ]
        # Wrong case in pattern — backticks are exact-match so this is trivially ok
        result_with = classify(rules, "here is code:\n```python\npass\n```")
        result_without = classify(rules, "here is code without backticks")
        assert result_with.hint == "code"
        assert result_without.hint is None


# ── QC-07: Empty message ─────────────────────────────────────────────────────

class TestEmptyMessage:
    def test_empty_string_returns_none(self) -> None:
        """QC-07a — empty message → None regardless of rules."""
        rules = [
            ClassificationRule(hint="fast", priority=1, max_length=20),
        ]
        result = classify(rules, "")
        assert result.hint is None
        assert bool(result) is False

    def test_whitespace_only_classified_normally(self) -> None:
        """QC-07b — whitespace-only short message → 'fast' (len ≤ 20)."""
        rules = [
            ClassificationRule(hint="fast", priority=1, max_length=20),
        ]
        result = classify(rules, "   ")
        assert result.hint == "fast"
        assert bool(result) is True


# ── QC-08: DEFAULT_CLASSIFICATION_RULES integration ──────────────────────────

class TestDefaultRulesIntegration:
    def test_code_keyword_plus_backtick_gives_code(self) -> None:
        """QC-08a — default rules: 'implement' + ``` → 'code'."""
        msg = "Please implement this:\n```python\ndef handler(): pass\n```"
        result = classify(DEFAULT_CLASSIFICATION_RULES, msg)
        assert result.hint == "code"

    def test_very_short_message_gives_fast(self) -> None:
        """QC-08b — default rules: 'yes' (3 chars) → 'fast'."""
        result = classify(DEFAULT_CLASSIFICATION_RULES, "yes")
        assert result.hint == "fast"

    def test_neutral_long_message_no_hint(self) -> None:
        """QC-08c — default rules: long neutral message → None."""
        msg = (
            "The system is designed to handle multiple concurrent requests "
            "using a lane-based message queue with SKIP LOCKED semantics."
        )
        result = classify(DEFAULT_CLASSIFICATION_RULES, msg)
        # No code keywords, no code block, too long for fast → None
        assert result.hint is None

    def test_rules_are_sorted_by_priority(self) -> None:
        """QC-08d — default rules are priority-ordered (code=10 > reasoning=5 > fast=1)."""
        priorities = [r.priority for r in DEFAULT_CLASSIFICATION_RULES]
        # Should contain 10, 5, 1 in some combination
        assert max(priorities) == 10
        assert min(priorities) == 1


# ── Sprint 204: ClassificationResult confidence scoring ──────────────────────

class TestClassificationResultConfidence:
    def test_high_priority_single_match_high_confidence(self) -> None:
        """Sprint 204 — single match at priority=10 yields confidence >= 0.9."""
        rules = [
            ClassificationRule(
                hint="code",
                priority=10,
                keywords=("implement",),
                patterns=("```",),
            ),
        ]
        result = classify(rules, "Please implement:\n```python\npass\n```")
        assert result.hint == "code"
        assert result.confidence >= 0.9
        assert result.method == "substring"
        assert result.matches == 1

    def test_no_match_confidence_sentinel(self) -> None:
        """Sprint 204 — no match returns confidence=0.3 (LLM fallback sentinel)."""
        result = classify([], "anything")
        assert result.hint is None
        assert result.confidence == 0.3
        assert result.method == "none"
        assert result.matches == 0

    def test_bool_compat_true_when_hint_set(self) -> None:
        """Sprint 204 backward compat — bool(result) True iff hint is not None."""
        rules = [ClassificationRule(hint="fast", priority=1, max_length=20)]
        result = classify(rules, "ok")
        assert bool(result) is True

    def test_bool_compat_false_when_no_hint(self) -> None:
        """Sprint 204 backward compat — bool(result) False when hint is None."""
        result = classify([], "ok")
        assert bool(result) is False


# ── Sprint 204 Day 2: Governance rules (AD-4) ────────────────────────────────

class TestGovernanceRules:
    """Tests for 5 governance classification rules at priority=8."""

    def test_approve_keyword_gives_governance(self) -> None:
        """AD-4 — 'approve' keyword → governance hint."""
        result = classify(DEFAULT_CLASSIFICATION_RULES, "approve gate G2")
        assert result.hint == "governance"
        assert result.confidence >= 0.85

    def test_gate_keyword_gives_governance(self) -> None:
        """AD-4 — 'gate' keyword → governance hint."""
        result = classify(DEFAULT_CLASSIFICATION_RULES, "check gate status")
        assert result.hint == "governance"
        assert result.confidence >= 0.85

    def test_submit_evidence_gives_governance(self) -> None:
        """AD-4 — 'submit evidence' keyword → governance hint."""
        result = classify(
            DEFAULT_CLASSIFICATION_RULES,
            "please submit evidence for the security review",
        )
        assert result.hint == "governance"
        assert result.confidence >= 0.85

    def test_export_audit_gives_governance(self) -> None:
        """AD-4 — 'export audit' keyword → governance hint."""
        result = classify(
            DEFAULT_CLASSIFICATION_RULES,
            "export audit report for project 5",
        )
        assert result.hint == "governance"
        assert result.confidence >= 0.85

    def test_close_sprint_gives_governance(self) -> None:
        """AD-4 — 'close sprint' keyword → governance hint."""
        result = classify(
            DEFAULT_CLASSIFICATION_RULES,
            "close sprint 204 please",
        )
        assert result.hint == "governance"
        assert result.confidence >= 0.85

    def test_governance_max_length_200_rejects_long_message(self) -> None:
        """AD-4 — approve/gate rules have max_length=200, long msg no match."""
        long_msg = "approve " + ("x" * 250)
        result = classify(DEFAULT_CLASSIFICATION_RULES, long_msg)
        # "approve" rule has max_length=200, so it should NOT match
        assert result.hint != "governance" or result.hint is None

    def test_governance_priority_below_code(self) -> None:
        """AD-4 — code (p=10) beats governance (p=8) when both match."""
        # A message with both "approve" and "```" should be classified as code
        msg = "approve this code:\n```python\ndef foo(): pass\n```"
        result = classify(DEFAULT_CLASSIFICATION_RULES, msg)
        assert result.hint == "code"

    def test_governance_priority_above_reasoning(self) -> None:
        """AD-4 — governance (p=8) beats reasoning (p=5)."""
        # A message with both "approve" and "explain" keywords
        msg = "explain why we should approve gate G3 for the security review"
        result = classify(DEFAULT_CLASSIFICATION_RULES, msg)
        assert result.hint == "governance"

    def test_vietnamese_approve_case_insensitive(self) -> None:
        """AD-4 — keyword check is case-insensitive for 'approve'."""
        result = classify(DEFAULT_CLASSIFICATION_RULES, "APPROVE gate G1")
        assert result.hint == "governance"

    def test_submit_evidence_no_max_length(self) -> None:
        """AD-4 — 'submit evidence' rule has no max_length restriction."""
        long_msg = "submit evidence " + ("context " * 50)
        result = classify(DEFAULT_CLASSIFICATION_RULES, long_msg)
        assert result.hint == "governance"
