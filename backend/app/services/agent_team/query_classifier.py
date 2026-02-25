"""
=========================================================================
Query Classifier — ADR-058 Pattern E (ZeroClaw)
SDLC Orchestrator - Sprint 179 (ZeroClaw Security Hardening)
                  + Sprint 204 (Confidence-Based Routing)

Version: 2.0.0
Date: February 2026
Status: ACTIVE - Sprint 204
Authority: CTO Approved (ADR-058 Decision 3)
Reference: ADR-058-ZeroClaw-Best-Practice-Adoption.md
           SPRINT-204-CONFIDENCE-ROUTING.md (Locked AD-1, AD-2)

Purpose:
- Classify incoming messages to route to the right model tier.
- Pure function: classify(rules, message) → ClassificationResult
- Sprint 179: first matching rule (by priority) wins.
- Sprint 204: ALL rules evaluated; confidence computed from match count,
  hint deduplication, and priority gaps. `ClassificationResult` replaces
  `str | None`.

ClassificationResult.confidence bands:
  >= 0.9   → high confidence (single code/pattern match)
  0.75-0.9 → medium confidence (single keyword/length match)
  < 0.6    → low confidence → LLM fallback in TeamOrchestrator
  0.3      → no match → LLM fallback always triggered

Classification Rules:
  code      (priority=10): coding tasks → qwen3-coder:30b (256K context)
  governance(priority=8):  gate/evidence/sprint actions → command_router
  reasoning (priority=5):  analysis/explain → deepseek-r1:32b
  fast      (priority=1):  short confirmations → qwen3:8b

Rule conditions (AND logic — all conditions must match):
  - keywords: case-insensitive substring match against full message text
  - patterns: case-sensitive substring match (code snippets, markers)
  - min_length: message length (chars) must be >= min_length
  - max_length: message length must be <= max_length

If no rule matches, returns ClassificationResult(hint=None, confidence=0.3).
Backward compatibility: ClassificationResult.__bool__() returns True iff
hint is not None, preserving `if classify(...):` call patterns.

References:
  - ADR-058 Decision 3 (LOCKED)
  - ZeroClaw src/agent/classifier.rs (pure function, single pass)
  - config.py: DEFAULT_CLASSIFICATION_RULES + MODEL_ROUTE_HINTS
=========================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ClassificationRule:
    """
    A single query classification rule.

    All non-empty conditions are ANDed: the rule fires only if ALL
    specified conditions match the message.

    Attributes:
        hint:        Model routing hint returned when this rule matches.
        priority:    Higher number = checked first (sorted descending).
        keywords:    Case-insensitive substrings that must ALL appear.
        patterns:    Case-sensitive substrings that must ALL appear.
        min_length:  Minimum message length in chars (0 = no minimum).
        max_length:  Maximum message length in chars (0 = no maximum).
    """

    hint: str
    priority: int = 5
    keywords: tuple[str, ...] = field(default_factory=tuple)
    patterns: tuple[str, ...] = field(default_factory=tuple)
    min_length: int = 0
    max_length: int = 0


@dataclass(frozen=True)
class ClassificationResult:
    """
    Result of classifying a message against a rule set.

    Sprint 204 (AD-1): Replaces bare ``str | None`` return type.

    Attributes:
        hint:       Model routing hint (e.g., "code", "reasoning",
                    "fast", "governance") or None if no rule matched.
        confidence: Float 0.0–1.0 indicating match certainty.
                    Bands: >=0.9 high, 0.75-0.9 medium, <0.6 triggers
                    LLM fallback in TeamOrchestrator.
        method:     How the classification was produced.
                    "substring"       — pure rule match (this module)
                    "llm"             — qwen3:8b LLM fallback
                    "llm_failed"      — LLM returned invalid JSON
                    "timeout_fallback" — LLM timed out (>1s)
                    "none"            — no rule matched, no LLM called
        matches:    Number of rules that fired (0 = no match, 1 = clear,
                    2+ = ambiguous). Used for confidence computation.

    Backward compatibility:
        ``bool(result)`` returns True iff ``hint is not None``, preserving
        existing ``if classify(...):`` checks without code changes.
    """

    hint: str | None
    confidence: float
    method: str = "substring"
    matches: int = 0

    def __bool__(self) -> bool:
        """True iff a hint was assigned (hint is not None)."""
        return self.hint is not None


def _compute_confidence(matching_rules: list[ClassificationRule]) -> float:
    """
    Compute a confidence score from the list of rules that matched.

    Sprint 204 (AD-1, AD-2): Confidence reflects how unambiguous the
    classification was.

    Args:
        matching_rules: Rules that matched, sorted descending by priority.

    Returns:
        Float 0.0–1.0.

    Rules:
        - No matches      → 0.3   (no-match sentinel, triggers LLM fallback)
        - 1 match p>=10   → 0.95  (pattern match, e.g. "```" for code)
        - 1 match p>=8    → 0.90  (governance keyword)
        - 1 match p>=5    → 0.85  (reasoning keyword)
        - 1 match p<5     → 0.75  (fast length heuristic)
        - Same-hint multi  → treat as single match (unambiguous)
        - Diff-hint multi  → min(0.9, 0.6 + gap * 0.1) where gap = best_p - second_p
                             Larger priority gap = more confident winner.
    """
    if not matching_rules:
        return 0.3

    # Deduplicate by hint: if all matching rules share the same hint,
    # the classification is unambiguous — use single-match scoring
    # based on the highest priority rule. This handles cases like
    # "approve gate G2" matching both "approve" and "gate" governance
    # rules (both p=8, same hint="governance").
    unique_hints = {r.hint for r in matching_rules}
    if len(unique_hints) == 1:
        best = max(matching_rules, key=lambda r: r.priority)
        if best.priority >= 10:
            return 0.95  # Pattern match (e.g., code fence)
        elif best.priority >= 8:
            return 0.90  # Governance keyword
        elif best.priority >= 5:
            return 0.85  # Reasoning keyword
        else:
            return 0.75  # Length heuristic (fast)

    # Multiple DIFFERENT hints matched — compute confidence from
    # priority gap between the best and runner-up hints.
    # A large gap means the winner is clearly dominant; small gap = ambiguous.
    # Group by hint, take max priority per hint, then compare top two.
    hint_priorities: dict[str, int] = {}
    for r in matching_rules:
        if r.hint not in hint_priorities or r.priority > hint_priorities[r.hint]:
            hint_priorities[r.hint] = r.priority
    ranked = sorted(hint_priorities.values(), reverse=True)
    gap = ranked[0] - ranked[1]
    return min(0.9, 0.6 + (gap * 0.1))


def classify(
    rules: list[ClassificationRule],
    message: str,
) -> ClassificationResult:
    """
    Classify a message and return a ``ClassificationResult``.

    Sprint 204: Updated from returning ``str | None`` to returning
    ``ClassificationResult`` with confidence scoring. Backward compat:
    ``if classify(rules, msg):`` still works because
    ``ClassificationResult.__bool__()`` is True iff hint is not None.

    Pure function — no side effects, no I/O.

    All rules are evaluated (not early-exit). The best match (highest
    priority) is selected as the winner. Confidence is computed from
    the number and relative priorities of all matching rules.

    Conditions checked (AND logic):
    - keywords: every keyword must appear in lower(message)
    - patterns: every pattern must appear in message (case-sensitive)
    - min_length: len(message) >= rule.min_length (if non-zero)
    - max_length: len(message) <= rule.max_length (if non-zero)

    Args:
        rules: List of ClassificationRule to evaluate.
        message: The incoming message text to classify.

    Returns:
        ClassificationResult with hint, confidence, method, and match count.
        hint is None and confidence=0.3 when no rule matches.
    """
    if not message:
        return ClassificationResult(
            hint=None,
            confidence=0.3,
            method="none",
            matches=0,
        )

    msg_lower = message.lower()
    msg_len = len(message)

    # Sort by priority descending; stable sort preserves insertion order
    # for equal-priority rules.
    sorted_rules = sorted(rules, key=lambda r: r.priority, reverse=True)

    # Collect ALL matching rules (not just first — Sprint 204 change).
    matching_rules: list[ClassificationRule] = []
    for rule in sorted_rules:
        # Keyword check (case-insensitive, ALL must match)
        if rule.keywords and not all(kw in msg_lower for kw in rule.keywords):
            continue

        # Pattern check (case-sensitive, ALL must match)
        if rule.patterns and not all(pat in message for pat in rule.patterns):
            continue

        # Length checks
        if rule.min_length and msg_len < rule.min_length:
            continue
        if rule.max_length and msg_len > rule.max_length:
            continue

        matching_rules.append(rule)

    if not matching_rules:
        return ClassificationResult(
            hint=None,
            confidence=0.3,
            method="none",
            matches=0,
        )

    # Best match = highest priority (first in sorted list).
    best_rule = matching_rules[0]
    confidence = _compute_confidence(matching_rules)

    return ClassificationResult(
        hint=best_rule.hint,
        confidence=confidence,
        method="substring",
        matches=len(matching_rules),
    )
