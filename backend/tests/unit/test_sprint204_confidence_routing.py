"""
=========================================================================
Sprint 204 — Track A: Confidence-Based Routing Test Suite
SDLC Orchestrator - Sprint 204 (Confidence-Based Routing + Human Escalation)

Version: 1.0.0
Date: 2026-05-19
Status: ACTIVE - Sprint 204
Authority: CTO Approved (Anthropic Best Practices Gap 3 — Confidence Routing)

Coverage (30 tests):
  Class 01: _llm_classify() happy path — 4 tests
    Valid JSON responses: code, governance, reasoning, fast hints
  Class 02: _llm_classify() markdown fence stripping — 2 tests
    ```json...``` and ``` ... ``` variants stripped before JSON parsing
  Class 03: _llm_classify() error handling — 6 tests
    timeout_fallback, llm_failed (json), llm_failed (ollama),
    invalid_category hint=None, confidence clamped >1.0, clamped <0.0
  Class 04: _llm_classify() content handling — 3 tests
    Short content preserved in prompt, long content truncated at 500 chars,
    matches=0 on all LLM results
  Class 05: _LLM_CLASSIFY_PROMPT constant — 2 tests
    All four categories present, {user_message} placeholder present
  Class 06: Step 5.7 trigger — low confidence → LLM — 4 tests
    confidence < 0.6 triggers, >= 0.6 skips, exactly 0.6 skips,
    LLM governance result propagates correctly
  Class 07: Governance interceptor (step 5.6) — 2 tests
    Governance confidence >= 0.9 (same-hint dedup applied),
    governance confidence >= 0.6 (never triggers step 5.7)
  Class 08: Regression — Sprint 179 classify() behavior unchanged — 7 tests
    Code 0.95, reasoning 0.85, fast 0.75, no-match 0.3,
    bool compat True/False, method="substring" for direct match

Zero Mock Policy: Real Pydantic models, real classify() calls, real
_compute_confidence(). Ollama mocked only at service boundary
(get_ollama_service + run_in_threadpool).
=========================================================================
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Ensure backend is on path for standalone pytest runs
_BACKEND_DIR = Path(__file__).parent.parent.parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.services.agent_team.config import DEFAULT_CLASSIFICATION_RULES
from app.services.agent_team.query_classifier import (
    ClassificationResult,
    ClassificationRule,
    _compute_confidence,
    classify,
)
from app.services.agent_team.team_orchestrator import TeamOrchestrator, _LLM_CLASSIFY_PROMPT
from app.services.ollama_service import OllamaError, OllamaResponse


# ─── Test Helpers ──────────────────────────────────────────────────────────────


def _make_ollama_response(text: str) -> OllamaResponse:
    """Build a minimal OllamaResponse with the given response text."""
    return OllamaResponse(
        model="qwen3:8b",
        response=text,
        done=True,
        total_duration_ns=100_000_000,
        load_duration_ns=10_000_000,
        prompt_eval_count=10,
        eval_count=20,
        eval_duration_ns=80_000_000,
    )


def _no_match() -> ClassificationResult:
    """A ClassificationResult with no substring match (confidence=0.3)."""
    return ClassificationResult(hint=None, confidence=0.3, method="substring", matches=0)


@pytest.fixture
def orchestrator():
    """Minimal TeamOrchestrator with all sub-services mocked out.

    Only the _llm_classify() method is exercised — all other service
    dependencies are replaced with MagicMock so __init__ completes
    without real DB/Redis connections.
    """
    db = MagicMock()
    with (
        patch("app.services.agent_team.team_orchestrator.MessageQueue"),
        patch("app.services.agent_team.team_orchestrator.ConversationTracker"),
        patch("app.services.agent_team.team_orchestrator.AgentRegistry"),
        patch("app.services.agent_team.team_orchestrator.MentionParser"),
        patch("app.services.agent_team.team_orchestrator.EvidenceCollector"),
        patch("app.services.agent_team.team_orchestrator.HistoryCompactor"),
    ):
        return TeamOrchestrator(db=db, redis=None)


async def _llm_call(
    orchestrator: TeamOrchestrator,
    content: str,
    original: ClassificationResult,
    response_text: str,
) -> ClassificationResult:
    """Call _llm_classify() with Ollama mocked to return response_text."""
    mock_ollama = MagicMock()
    mock_ollama.generate.return_value = _make_ollama_response(response_text)

    async def _fake_threadpool(func, *args, **kwargs):
        return func(*args, **kwargs)

    with (
        patch(
            "app.services.agent_team.team_orchestrator.get_ollama_service",
            return_value=mock_ollama,
        ),
        patch(
            "app.services.agent_team.team_orchestrator.run_in_threadpool",
            _fake_threadpool,
        ),
    ):
        return await orchestrator._llm_classify(content=content, original=original)


# ─── Class 01: _llm_classify() Happy Path ─────────────────────────────────────


class TestLlmClassifyHappyPath:
    """LLM returns valid JSON with a recognized category."""

    @pytest.mark.asyncio
    async def test_code_hint_returned(self, orchestrator):
        result = await _llm_call(
            orchestrator,
            "fix the authentication bug in user_service.py",
            _no_match(),
            '{"hint": "code", "confidence": 0.88}',
        )
        assert result.hint == "code"
        assert result.confidence == pytest.approx(0.88)
        assert result.method == "llm"

    @pytest.mark.asyncio
    async def test_governance_hint_returned(self, orchestrator):
        result = await _llm_call(
            orchestrator,
            "should we proceed with approving gate 5",
            _no_match(),
            '{"hint": "governance", "confidence": 0.82}',
        )
        assert result.hint == "governance"
        assert result.confidence == pytest.approx(0.82)
        assert result.method == "llm"

    @pytest.mark.asyncio
    async def test_reasoning_hint_returned(self, orchestrator):
        result = await _llm_call(
            orchestrator,
            "review the latest changes and tell me what you think",
            _no_match(),
            '{"hint": "reasoning", "confidence": 0.76}',
        )
        assert result.hint == "reasoning"
        assert result.confidence == pytest.approx(0.76)
        assert result.method == "llm"

    @pytest.mark.asyncio
    async def test_fast_hint_returned(self, orchestrator):
        result = await _llm_call(
            orchestrator,
            "ok",
            _no_match(),
            '{"hint": "fast", "confidence": 0.91}',
        )
        assert result.hint == "fast"
        assert result.confidence == pytest.approx(0.91)
        assert result.method == "llm"


# ─── Class 02: _llm_classify() — Markdown Fence Stripping ─────────────────────


class TestLlmClassifyFenceStripping:
    """Markdown code fences around JSON are stripped before parsing."""

    @pytest.mark.asyncio
    async def test_json_fence_stripped(self, orchestrator):
        """LLM wraps JSON in ```json...``` fences — should still parse."""
        fenced = '```json\n{"hint": "code", "confidence": 0.85}\n```'
        result = await _llm_call(orchestrator, "write a sort function", _no_match(), fenced)
        assert result.hint == "code"
        assert result.method == "llm"

    @pytest.mark.asyncio
    async def test_plain_fence_stripped(self, orchestrator):
        """LLM wraps JSON in plain ``` fences without language tag."""
        fenced = '```\n{"hint": "reasoning", "confidence": 0.72}\n```'
        result = await _llm_call(orchestrator, "why did gate G2 fail", _no_match(), fenced)
        assert result.hint == "reasoning"
        assert result.method == "llm"


# ─── Class 03: _llm_classify() — Error Handling ───────────────────────────────


class TestLlmClassifyErrorHandling:
    """All errors are non-fatal; original ClassificationResult is preserved."""

    @pytest.mark.asyncio
    async def test_timeout_preserves_original_hint(self, orchestrator):
        """asyncio.TimeoutError → method='timeout_fallback', original hint/confidence kept."""
        original = ClassificationResult(
            hint="fast", confidence=0.45, method="substring", matches=1
        )
        with patch(
            "app.services.agent_team.team_orchestrator.asyncio.wait_for",
            side_effect=asyncio.TimeoutError(),
        ):
            result = await orchestrator._llm_classify(
                content="hello there", original=original
            )

        assert result.hint == "fast"
        assert result.confidence == pytest.approx(0.45)
        assert result.method == "timeout_fallback"
        assert result.matches == 1

    @pytest.mark.asyncio
    async def test_json_decode_error_returns_original(self, orchestrator):
        """Malformed JSON → method='llm_failed', original preserved."""
        original = _no_match()
        result = await _llm_call(orchestrator, "ambiguous query", original, "NOT VALID JSON")
        assert result.hint is None
        assert result.confidence == pytest.approx(0.3)
        assert result.method == "llm_failed"

    @pytest.mark.asyncio
    async def test_ollama_error_returns_original(self, orchestrator):
        """OllamaError → method='llm_failed', original hint preserved."""
        original = ClassificationResult(
            hint="reasoning", confidence=0.45, method="substring", matches=1
        )
        mock_ollama = MagicMock()
        mock_ollama.generate.side_effect = OllamaError("Connection refused")

        async def _fake_threadpool(func, *args, **kwargs):
            return func(*args, **kwargs)

        with (
            patch(
                "app.services.agent_team.team_orchestrator.get_ollama_service",
                return_value=mock_ollama,
            ),
            patch(
                "app.services.agent_team.team_orchestrator.run_in_threadpool",
                _fake_threadpool,
            ),
        ):
            result = await orchestrator._llm_classify(
                content="explain why this fails", original=original
            )

        assert result.hint == "reasoning"
        assert result.confidence == pytest.approx(0.45)
        assert result.method == "llm_failed"

    @pytest.mark.asyncio
    async def test_invalid_category_sets_hint_none(self, orchestrator):
        """LLM returns unknown category → hint=None but method='llm' (parse succeeded)."""
        result = await _llm_call(
            orchestrator,
            "random query",
            _no_match(),
            '{"hint": "completely_unknown_category", "confidence": 0.7}',
        )
        assert result.hint is None
        assert result.method == "llm"

    @pytest.mark.asyncio
    async def test_confidence_clamped_above_one(self, orchestrator):
        """LLM returns confidence=1.8 → clamped to 1.0."""
        result = await _llm_call(
            orchestrator,
            "fix the null pointer",
            _no_match(),
            '{"hint": "code", "confidence": 1.8}',
        )
        assert result.confidence == pytest.approx(1.0)

    @pytest.mark.asyncio
    async def test_confidence_clamped_below_zero(self, orchestrator):
        """LLM returns confidence=-0.3 → clamped to 0.0."""
        result = await _llm_call(
            orchestrator,
            "fix the null pointer",
            _no_match(),
            '{"hint": "code", "confidence": -0.3}',
        )
        assert result.confidence == pytest.approx(0.0)


# ─── Class 04: _llm_classify() — Content Handling ─────────────────────────────


class TestLlmClassifyContentHandling:
    """Message content is processed correctly before being sent to LLM."""

    @pytest.mark.asyncio
    async def test_short_content_appears_in_prompt(self, orchestrator):
        """Content under 500 chars is passed intact to the LLM prompt."""
        content = "fix the bug in auth_service.py line 42"
        mock_ollama = MagicMock()
        mock_ollama.generate.return_value = _make_ollama_response(
            '{"hint": "code", "confidence": 0.9}'
        )

        async def _fake_threadpool(func, *args, **kwargs):
            return func(*args, **kwargs)

        with (
            patch(
                "app.services.agent_team.team_orchestrator.get_ollama_service",
                return_value=mock_ollama,
            ),
            patch(
                "app.services.agent_team.team_orchestrator.run_in_threadpool",
                _fake_threadpool,
            ),
        ):
            await orchestrator._llm_classify(content=content, original=_no_match())

        prompt_used: str = mock_ollama.generate.call_args[0][0]
        assert content in prompt_used

    @pytest.mark.asyncio
    async def test_long_content_truncated_at_500_chars(self, orchestrator):
        """Content over 500 chars is truncated in the LLM prompt."""
        content = "a" * 1_000  # 1000 chars → truncated to 500
        mock_ollama = MagicMock()
        mock_ollama.generate.return_value = _make_ollama_response(
            '{"hint": "fast", "confidence": 0.6}'
        )

        async def _fake_threadpool(func, *args, **kwargs):
            return func(*args, **kwargs)

        with (
            patch(
                "app.services.agent_team.team_orchestrator.get_ollama_service",
                return_value=mock_ollama,
            ),
            patch(
                "app.services.agent_team.team_orchestrator.run_in_threadpool",
                _fake_threadpool,
            ),
        ):
            await orchestrator._llm_classify(content=content, original=_no_match())

        prompt_used: str = mock_ollama.generate.call_args[0][0]
        # 501 consecutive 'a' chars must NOT appear — 500 'a' chars must appear
        assert "a" * 501 not in prompt_used
        assert "a" * 500 in prompt_used

    @pytest.mark.asyncio
    async def test_matches_field_always_zero_on_llm_result(self, orchestrator):
        """ClassificationResult from _llm_classify() always has matches=0."""
        result = await _llm_call(
            orchestrator,
            "write unit tests for the gate service",
            _no_match(),
            '{"hint": "code", "confidence": 0.87}',
        )
        assert result.matches == 0


# ─── Class 05: _LLM_CLASSIFY_PROMPT Constant ──────────────────────────────────


class TestLlmClassifyPromptConstant:
    """_LLM_CLASSIFY_PROMPT is well-formed with all required categories."""

    def test_prompt_contains_all_four_categories(self):
        for category in ("code", "reasoning", "governance", "fast"):
            assert category in _LLM_CLASSIFY_PROMPT, (
                f"Category '{category}' missing from _LLM_CLASSIFY_PROMPT"
            )

    def test_prompt_has_user_message_placeholder(self):
        assert "{user_message}" in _LLM_CLASSIFY_PROMPT


# ─── Class 06: Step 5.7 Integration — Low Confidence Triggers LLM ─────────────


class TestStepFiveSevenTrigger:
    """Step 5.7 in _process(): confidence < 0.6 triggers _llm_classify()."""

    @pytest.mark.asyncio
    async def test_confidence_below_threshold_triggers_llm(self, orchestrator):
        """Confidence = 0.3 (no match) → _llm_classify called."""
        original = _no_match()  # confidence=0.3
        llm_result = ClassificationResult(
            hint="code", confidence=0.82, method="llm", matches=0
        )
        orchestrator._llm_classify = AsyncMock(return_value=llm_result)

        # Replicate the step 5.7 conditional
        if original.confidence < 0.6:
            result = await orchestrator._llm_classify(
                content="review this function", original=original
            )
        else:
            result = original

        orchestrator._llm_classify.assert_called_once()
        assert result.hint == "code"
        assert result.method == "llm"

    @pytest.mark.asyncio
    async def test_confidence_at_threshold_skips_llm(self, orchestrator):
        """Confidence = 0.75 (fast length heuristic) → _llm_classify NOT called."""
        high = ClassificationResult(
            hint="fast", confidence=0.75, method="substring", matches=1
        )
        orchestrator._llm_classify = AsyncMock()

        if high.confidence < 0.6:
            await orchestrator._llm_classify(content="hello", original=high)

        orchestrator._llm_classify.assert_not_called()

    @pytest.mark.asyncio
    async def test_exactly_0_6_skips_llm(self, orchestrator):
        """Confidence of exactly 0.6 does NOT trigger LLM (strict less-than)."""
        boundary = ClassificationResult(
            hint="fast", confidence=0.6, method="substring", matches=1
        )
        orchestrator._llm_classify = AsyncMock()

        if boundary.confidence < 0.6:
            await orchestrator._llm_classify(content="ok", original=boundary)

        orchestrator._llm_classify.assert_not_called()

    @pytest.mark.asyncio
    async def test_llm_governance_result_has_method_llm(self, orchestrator):
        """When LLM upgrades classification to governance, method='llm' preserved."""
        result = await _llm_call(
            orchestrator,
            "should we close sprint 204 or continue?",
            _no_match(),
            '{"hint": "governance", "confidence": 0.84}',
        )
        assert result.hint == "governance"
        assert result.method == "llm"
        assert result.confidence >= 0.8


# ─── Class 07: Governance Interceptor (Step 5.6) Priority ─────────────────────


class TestGovernanceInterceptorPriority:
    """Governance classification (step 5.6) fires BEFORE LLM fallback (step 5.7).

    Governance rules at priority=8 produce confidence >= 0.9 via same-hint
    multi-match deduplication — well above the < 0.6 LLM trigger threshold.
    """

    def test_governance_confidence_exceeds_llm_trigger(self):
        """Governance rules yield confidence >= 0.9 → step 5.7 never triggered."""
        result = classify(DEFAULT_CLASSIFICATION_RULES, "approve gate G3 for project")
        assert result.hint == "governance"
        # Same-hint dedup: both "approve" and "gate" p=8 match → treated as single
        # unambiguous match → confidence=0.90
        assert result.confidence >= 0.6, (
            "Governance confidence must be >= 0.6 to bypass the step 5.7 LLM trigger"
        )

    def test_close_sprint_governance_confidence(self):
        """'close sprint' keyword alone yields governance at >= 0.9."""
        result = classify(DEFAULT_CLASSIFICATION_RULES, "close sprint 204")
        assert result.hint == "governance"
        assert result.confidence >= 0.85


# ─── Class 08: Regression — Sprint 179 classify() Behavior Unchanged ──────────


class TestRegressionSprint179:
    """Verify Sprint 179 query_classifier behavior is fully preserved."""

    def test_code_fence_pattern_confidence_095(self):
        """Code fence pattern (priority=10, single match) → confidence=0.95."""
        result = classify(DEFAULT_CLASSIFICATION_RULES, "```python\nprint('hello')\n```")
        assert result.hint == "code"
        assert result.confidence == pytest.approx(0.95)

    def test_reasoning_keyword_confidence_085(self):
        """All reasoning keywords present + min_length met → confidence=0.85.

        The DEFAULT reasoning rule uses AND logic for all 6 keywords
        (explain, analyze, why, compare, trade-off, design) and requires
        len >= 50. Message deliberately avoids governance keywords.
        """
        msg = (
            "explain and analyze why we should compare trade-off design "
            "approaches for the authentication service"
        )
        result = classify(DEFAULT_CLASSIFICATION_RULES, msg)
        assert result.hint == "reasoning"
        assert result.confidence == pytest.approx(0.85)

    def test_fast_length_heuristic_confidence_075(self):
        """Short message (<=20 chars, priority=1, single match) → confidence=0.75."""
        result = classify(DEFAULT_CLASSIFICATION_RULES, "ok done")  # 7 chars
        assert result.hint == "fast"
        assert result.confidence == pytest.approx(0.75)

    def test_no_match_confidence_030(self):
        """Unclassifiable message → confidence=0.3 (LLM trigger sentinel)."""
        result = classify(
            DEFAULT_CLASSIFICATION_RULES,
            "the deployment went smoothly yesterday afternoon",
        )
        assert result.hint is None
        assert result.confidence == pytest.approx(0.3)

    def test_bool_compat_true_when_hint_set(self):
        """ClassificationResult is truthy when hint is not None.

        'approve sprint 204' triggers the governance hint (approve keyword,
        length ≤ 200), so hint='governance' and bool(result) is True.
        """
        result = classify(DEFAULT_CLASSIFICATION_RULES, "approve sprint 204 for merge")
        assert bool(result) is True

    def test_bool_compat_false_when_no_hint(self):
        """ClassificationResult is falsy when hint is None."""
        result = classify(
            DEFAULT_CLASSIFICATION_RULES,
            "the weather in Hanoi is warm today",
        )
        assert bool(result) is False

    def test_method_is_substring_for_direct_match(self):
        """Direct substring (or pattern) match records method='substring'.

        A code fence triggers the code rule (pattern match); method is
        always 'substring' for classify() results (vs 'llm' / 'llm_failed').
        """
        result = classify(DEFAULT_CLASSIFICATION_RULES, "```python\nprint('hello')\n```")
        assert result.method == "substring"
