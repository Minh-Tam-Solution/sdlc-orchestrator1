"""
=========================================================================
Sprint 203 — Evaluator-Optimizer Test Suite (Track D)
SDLC Orchestrator - Sprint 203 (Evaluator-Optimizer + Evals Expansion)

Version: 1.0.0
Date: 2026-05-05
Status: ACTIVE - Sprint 203
Authority: CTO Approved (Anthropic Best Practices — Evaluator-Optimizer)

Test Coverage:
  Class 01: ReflectResult dataclass (4 tests)
  Class 02: ReflectStep.__init__ — extended params (4 tests)
  Class 03: ReflectStep.should_reflect — unchanged behavior (4 tests)
  Class 04: ReflectStep.inject_reflection — backward compat (3 tests)
  Class 05: ReflectStep.reflect_and_score — early stop path (5 tests)
  Class 06: ReflectStep.reflect_and_score — inject path (4 tests)
  Class 07: ReflectStep.reflect_and_score — fallback paths (4 tests)
  Class 08: ReflectStep._extract_last_assistant (4 tests)
  Class 09: reflect_step._parse_rubric (4 tests)
  Class 10: ConversationTracker.record_reflect_iteration (5 tests)
  Class 11: AgentInvoker.run_reflect_loop (5 tests)
  Class 12: AgentDefinition.max_reflect_iterations field (4 tests)
  Class 13: Regression guards (6 tests)

Total: 56 tests
=========================================================================
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Optional
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
import pytest_asyncio

from app.schemas.eval_rubric import EvalRubric
from app.services.agent_team.reflect_step import (
    EARLY_STOP_THRESHOLD,
    REFLECT_EVALUATOR_MODEL,
    ReflectResult,
    ReflectStep,
    _extract_score,
    _parse_rubric,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_ollama_response(correctness: int = 8, completeness: int = 8, safety: int = 9) -> MagicMock:
    """Build a mock OllamaResponse for the evaluator path."""
    obj = MagicMock()
    obj.response = json.dumps({
        "correctness": correctness,
        "completeness": completeness,
        "safety": safety,
        "explanation": f"Scores: C={correctness} P={completeness} S={safety}",
    })
    return obj


def _messages_with_assistant(content: str = "I completed the task.") -> list[dict]:
    return [
        {"role": "user", "content": "Do the task"},
        {"role": "assistant", "content": content},
    ]


def _tool_results(with_error: bool = False) -> list[dict]:
    if with_error:
        return [{"tool": "read_file", "error": "FileNotFoundError"}]
    return [{"tool": "read_file"}, {"tool": "write_file"}]


# ============================================================================
# Class 01: ReflectResult dataclass
# ============================================================================

class TestReflectResultDataclass:
    """ReflectResult dataclass — Sprint 203 A-03"""

    def test_fields_present(self) -> None:
        fields = list(ReflectResult.__dataclass_fields__.keys())
        assert "rubric" in fields
        assert "iteration" in fields
        assert "early_stopped" in fields
        assert "feedback" in fields

    def test_create_with_rubric(self) -> None:
        rubric = EvalRubric(correctness=9, completeness=8, safety=9, explanation="Good")
        r = ReflectResult(rubric=rubric, iteration=1, early_stopped=True, feedback="Excellent")
        assert r.early_stopped is True
        assert r.rubric is not None
        assert r.rubric.total_score == pytest.approx(8.67, abs=0.01)

    def test_create_without_rubric(self) -> None:
        """rubric=None is valid (evaluator failure fallback path)."""
        r = ReflectResult(rubric=None, iteration=2, early_stopped=False, feedback="fallback")
        assert r.rubric is None
        assert r.iteration == 2

    def test_early_stopped_false_by_default(self) -> None:
        r = ReflectResult(rubric=None, iteration=1, early_stopped=False, feedback="")
        assert r.early_stopped is False


# ============================================================================
# Class 02: ReflectStep.__init__ — extended params
# ============================================================================

class TestReflectStepInit:
    """ReflectStep constructor extended for Sprint 203"""

    def test_defaults(self) -> None:
        step = ReflectStep()
        assert step.frequency == 1
        assert step.max_iterations == 1
        assert step.evaluator_model == REFLECT_EVALUATOR_MODEL

    def test_custom_frequency(self) -> None:
        step = ReflectStep(frequency=3)
        assert step.frequency == 3

    def test_custom_max_iterations(self) -> None:
        step = ReflectStep(max_iterations=3)
        assert step.max_iterations == 3

    def test_custom_evaluator_model(self) -> None:
        step = ReflectStep(evaluator_model="qwen3:32b")
        assert step.evaluator_model == "qwen3:32b"


# ============================================================================
# Class 03: ReflectStep.should_reflect — unchanged behavior (Sprint 177)
# ============================================================================

class TestShouldReflect:
    """should_reflect() — Sprint 177 behavior must be preserved"""

    def test_frequency_zero_always_false(self) -> None:
        step = ReflectStep(frequency=0)
        assert step.should_reflect(_tool_results(), batch_index=0) is False
        assert step.should_reflect(_tool_results(with_error=True), batch_index=0) is False

    def test_error_always_reflects(self) -> None:
        step = ReflectStep(frequency=5)
        assert step.should_reflect(_tool_results(with_error=True), batch_index=4) is True

    def test_frequency_schedule(self) -> None:
        step = ReflectStep(frequency=2)
        assert step.should_reflect(_tool_results(), batch_index=0) is True
        assert step.should_reflect(_tool_results(), batch_index=1) is False
        assert step.should_reflect(_tool_results(), batch_index=2) is True

    def test_frequency_one_always_reflects(self) -> None:
        step = ReflectStep(frequency=1)
        for i in range(5):
            assert step.should_reflect(_tool_results(), batch_index=i) is True


# ============================================================================
# Class 04: inject_reflection — backward compatibility
# ============================================================================

class TestInjectReflection:
    """inject_reflection() — Sprint 177 callers still work"""

    def test_appends_user_message(self) -> None:
        step = ReflectStep()
        messages = _messages_with_assistant()
        original_len = len(messages)
        step.inject_reflection(messages, _tool_results())
        assert len(messages) == original_len + 1
        assert messages[-1]["role"] == "user"

    def test_contains_tool_summary(self) -> None:
        step = ReflectStep()
        messages = _messages_with_assistant()
        step.inject_reflection(messages, _tool_results())
        content = messages[-1]["content"]
        assert "read_file" in content
        assert "write_file" in content

    def test_returns_same_list(self) -> None:
        step = ReflectStep()
        messages = _messages_with_assistant()
        result = step.inject_reflection(messages, _tool_results())
        assert result is messages


# ============================================================================
# Class 05: reflect_and_score — early stop path
# ============================================================================

class TestReflectAndScoreEarlyStop:
    """reflect_and_score() → early stop when score >= 8.0"""

    @pytest.mark.asyncio
    async def test_early_stop_high_score(self) -> None:
        step = ReflectStep(max_iterations=3)
        ollama = MagicMock()
        ollama.generate.return_value = _make_ollama_response(9, 9, 9)
        messages = _messages_with_assistant()
        original_len = len(messages)

        result = await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=0,
            ollama_client=ollama,
            iteration=1,
        )

        assert result.early_stopped is True
        assert result.rubric is not None
        assert result.rubric.total_score >= EARLY_STOP_THRESHOLD
        # No reflection injected on early stop
        assert len(messages) == original_len

    @pytest.mark.asyncio
    async def test_early_stop_boundary(self) -> None:
        """Exactly 8.0 average should trigger early stop."""
        step = ReflectStep(max_iterations=2)
        ollama = MagicMock()
        # (8+8+8)/3 = 8.0 — exactly at threshold
        ollama.generate.return_value = _make_ollama_response(8, 8, 8)
        messages = _messages_with_assistant()

        result = await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=0,
            ollama_client=ollama,
            iteration=1,
        )

        assert result.early_stopped is True

    @pytest.mark.asyncio
    async def test_early_stop_returns_rubric(self) -> None:
        step = ReflectStep()
        ollama = MagicMock()
        ollama.generate.return_value = _make_ollama_response(9, 8, 9)
        messages = _messages_with_assistant()

        result = await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=1,
            ollama_client=ollama,
            iteration=1,
        )

        assert result.rubric.correctness == 9
        assert result.rubric.safety == 9
        assert result.iteration == 1

    @pytest.mark.asyncio
    async def test_early_stop_feedback_is_explanation(self) -> None:
        step = ReflectStep()
        ollama = MagicMock()
        ollama.generate.return_value = _make_ollama_response(9, 9, 9)
        messages = _messages_with_assistant()

        result = await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=0,
            ollama_client=ollama,
            iteration=1,
        )

        assert result.feedback == result.rubric.explanation

    @pytest.mark.asyncio
    async def test_early_stop_different_iterations(self) -> None:
        step = ReflectStep()
        ollama = MagicMock()
        ollama.generate.return_value = _make_ollama_response(9, 9, 10)
        messages = _messages_with_assistant()

        result = await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=2,
            ollama_client=ollama,
            iteration=3,
        )

        assert result.iteration == 3
        assert result.early_stopped is True


# ============================================================================
# Class 06: reflect_and_score — inject reflection path (score < 8.0)
# ============================================================================

class TestReflectAndScoreInjectPath:
    """reflect_and_score() → inject reflection when score < 8.0"""

    @pytest.mark.asyncio
    async def test_below_threshold_injects_reflection(self) -> None:
        step = ReflectStep()
        ollama = MagicMock()
        # (6+6+8)/3 = 6.67 — below 8.0 threshold
        ollama.generate.return_value = _make_ollama_response(6, 6, 8)
        messages = _messages_with_assistant()
        original_len = len(messages)

        result = await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=0,
            ollama_client=ollama,
            iteration=1,
        )

        assert result.early_stopped is False
        assert len(messages) == original_len + 1
        assert messages[-1]["role"] == "user"

    @pytest.mark.asyncio
    async def test_injected_message_contains_score(self) -> None:
        step = ReflectStep()
        ollama = MagicMock()
        ollama.generate.return_value = _make_ollama_response(6, 7, 8)
        messages = _messages_with_assistant()

        await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=0,
            ollama_client=ollama,
            iteration=1,
        )

        content = messages[-1]["content"]
        assert "7.0" in content or "score" in content.lower()

    @pytest.mark.asyncio
    async def test_just_below_threshold(self) -> None:
        """7.99 average should NOT trigger early stop."""
        step = ReflectStep()
        ollama = MagicMock()
        # (8+8+8)/3 - delta (use 7,8,9 = 8.0 exactly — should early stop)
        # Use 7,7,9 = 7.67 — below threshold
        ollama.generate.return_value = _make_ollama_response(7, 7, 9)
        messages = _messages_with_assistant()
        original_len = len(messages)

        result = await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=0,
            ollama_client=ollama,
            iteration=1,
        )

        assert result.early_stopped is False
        assert len(messages) == original_len + 1

    @pytest.mark.asyncio
    async def test_feedback_contains_threshold_info(self) -> None:
        step = ReflectStep()
        ollama = MagicMock()
        ollama.generate.return_value = _make_ollama_response(6, 7, 8)
        messages = _messages_with_assistant()

        result = await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=0,
            ollama_client=ollama,
            iteration=1,
        )

        assert str(EARLY_STOP_THRESHOLD) in result.feedback


# ============================================================================
# Class 07: reflect_and_score — fallback paths
# ============================================================================

class TestReflectAndScoreFallback:
    """reflect_and_score() fallback paths — evaluator failure + no assistant msg"""

    @pytest.mark.asyncio
    async def test_no_assistant_message_falls_back(self) -> None:
        step = ReflectStep()
        ollama = MagicMock()
        # No assistant message in list
        messages = [{"role": "user", "content": "Do the task"}]
        original_len = len(messages)

        result = await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=0,
            ollama_client=ollama,
            iteration=1,
        )

        assert result.rubric is None
        assert result.early_stopped is False
        assert len(messages) == original_len + 1
        # ollama should NOT have been called
        ollama.generate.assert_not_called()

    @pytest.mark.asyncio
    async def test_evaluator_exception_falls_back(self) -> None:
        step = ReflectStep()
        ollama = MagicMock()
        ollama.generate.side_effect = ConnectionError("Ollama not available")
        messages = _messages_with_assistant()
        original_len = len(messages)

        result = await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=0,
            ollama_client=ollama,
            iteration=1,
        )

        assert result.rubric is None
        assert result.early_stopped is False
        assert len(messages) == original_len + 1

    @pytest.mark.asyncio
    async def test_evaluator_parse_failure_falls_back(self) -> None:
        step = ReflectStep()
        ollama = MagicMock()
        bad_resp = MagicMock()
        bad_resp.response = "I cannot score this response."
        ollama.generate.return_value = bad_resp
        messages = _messages_with_assistant()

        result = await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=0,
            ollama_client=ollama,
            iteration=1,
        )

        assert result.rubric is None
        assert result.early_stopped is False

    @pytest.mark.asyncio
    async def test_is_gate_action_param_accepted(self) -> None:
        """is_gate_action=True should not break anything (reserved param)."""
        step = ReflectStep()
        ollama = MagicMock()
        ollama.generate.return_value = _make_ollama_response(9, 9, 9)
        messages = _messages_with_assistant()

        result = await step.reflect_and_score(
            messages=messages,
            tool_results=_tool_results(),
            batch_index=0,
            ollama_client=ollama,
            iteration=1,
            is_gate_action=True,
        )

        assert result is not None


# ============================================================================
# Class 08: _extract_last_assistant
# ============================================================================

class TestExtractLastAssistant:
    """ReflectStep._extract_last_assistant — string and structured content"""

    def test_string_content(self) -> None:
        messages = _messages_with_assistant("I did the task.")
        result = ReflectStep._extract_last_assistant(messages)
        assert result == "I did the task."

    def test_structured_content_blocks(self) -> None:
        messages = [
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "Part 1."},
                    {"type": "text", "text": "Part 2."},
                ],
            }
        ]
        result = ReflectStep._extract_last_assistant(messages)
        assert result == "Part 1. Part 2."

    def test_no_assistant_returns_none(self) -> None:
        messages = [{"role": "user", "content": "hello"}]
        result = ReflectStep._extract_last_assistant(messages)
        assert result is None

    def test_returns_last_assistant(self) -> None:
        messages = [
            {"role": "assistant", "content": "First response."},
            {"role": "user", "content": "Another user message."},
            {"role": "assistant", "content": "Second response."},
        ]
        result = ReflectStep._extract_last_assistant(messages)
        assert result == "Second response."


# ============================================================================
# Class 09: _parse_rubric module-level function
# ============================================================================

class TestParseRubric:
    """_parse_rubric — 3-stage parsing: JSON / regex-in-think / regex fallback"""

    def test_clean_json(self) -> None:
        raw = '{"correctness": 8, "completeness": 9, "safety": 10, "explanation": "Good"}'
        rubric = _parse_rubric(raw)
        assert rubric.correctness == 8
        assert rubric.completeness == 9
        assert rubric.safety == 10

    def test_markdown_wrapped_json(self) -> None:
        raw = '```json\n{"correctness": 7, "completeness": 8, "safety": 9, "explanation": "ok"}\n```'
        rubric = _parse_rubric(raw)
        assert rubric.correctness == 7

    def test_think_wrapped_json(self) -> None:
        raw = '<think>I need to evaluate...</think>{"correctness": 8, "completeness": 8, "safety": 9, "explanation": "passed"}'
        rubric = _parse_rubric(raw)
        assert rubric.correctness == 8

    def test_invalid_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Failed to parse"):
            _parse_rubric("This has no scores at all, nothing parseable here.")


# ============================================================================
# Class 10: ConversationTracker.record_reflect_iteration
# ============================================================================

class TestRecordReflectIteration:
    """ConversationTracker.record_reflect_iteration — Sprint 203 A-04"""

    @pytest.mark.asyncio
    async def test_adds_entry_to_metadata(self) -> None:
        from app.services.agent_team.conversation_tracker import ConversationTracker

        db = AsyncMock()
        tracker = ConversationTracker(db)
        conv_id = uuid4()

        mock_conv = MagicMock()
        mock_conv.metadata_ = {}
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_conv
        db.execute = AsyncMock(return_value=mock_result)

        await tracker.record_reflect_iteration(
            conversation_id=conv_id,
            batch_index=0,
            iteration=1,
            rubric_score=7.5,
            early_stopped=False,
            feedback="Score below threshold.",
        )

        entries = mock_conv.metadata_["reflect_iterations"]
        assert len(entries) == 1
        assert entries[0]["batch"] == 0
        assert entries[0]["iter"] == 1
        assert entries[0]["score"] == 7.5
        assert entries[0]["early_stopped"] is False

    @pytest.mark.asyncio
    async def test_circular_buffer_max_20(self) -> None:
        from app.services.agent_team.conversation_tracker import ConversationTracker

        db = AsyncMock()
        tracker = ConversationTracker(db)
        conv_id = uuid4()

        mock_conv = MagicMock()
        # Pre-populate with 20 entries
        mock_conv.metadata_ = {
            "reflect_iterations": [{"batch": i, "iter": 1, "score": 7.0,
                                    "early_stopped": False, "feedback": "", "ts": ""}
                                   for i in range(20)]
        }
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_conv
        db.execute = AsyncMock(return_value=mock_result)

        await tracker.record_reflect_iteration(
            conversation_id=conv_id,
            batch_index=99,
            iteration=1,
            rubric_score=9.0,
            early_stopped=True,
            feedback="Excellent.",
        )

        entries = mock_conv.metadata_["reflect_iterations"]
        # Still max 20 entries
        assert len(entries) == 20
        # Last entry is the new one
        assert entries[-1]["batch"] == 99

    @pytest.mark.asyncio
    async def test_none_rubric_score_stored(self) -> None:
        from app.services.agent_team.conversation_tracker import ConversationTracker

        db = AsyncMock()
        tracker = ConversationTracker(db)
        conv_id = uuid4()

        mock_conv = MagicMock()
        mock_conv.metadata_ = {}
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_conv
        db.execute = AsyncMock(return_value=mock_result)

        await tracker.record_reflect_iteration(
            conversation_id=conv_id,
            batch_index=0,
            iteration=1,
            rubric_score=None,  # evaluator failure
            early_stopped=False,
            feedback="Fallback reflection.",
        )

        entries = mock_conv.metadata_["reflect_iterations"]
        assert entries[0]["score"] is None

    @pytest.mark.asyncio
    async def test_db_failure_is_non_fatal(self) -> None:
        from app.services.agent_team.conversation_tracker import ConversationTracker

        db = AsyncMock()
        db.execute = AsyncMock(side_effect=Exception("DB connection lost"))
        tracker = ConversationTracker(db)

        # Should NOT raise — non-fatal by design
        await tracker.record_reflect_iteration(
            conversation_id=uuid4(),
            batch_index=0,
            iteration=1,
            rubric_score=7.5,
            early_stopped=False,
            feedback="test",
        )

    @pytest.mark.asyncio
    async def test_feedback_truncated_at_200_chars(self) -> None:
        from app.services.agent_team.conversation_tracker import ConversationTracker

        db = AsyncMock()
        tracker = ConversationTracker(db)
        conv_id = uuid4()

        mock_conv = MagicMock()
        mock_conv.metadata_ = {}
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_conv
        db.execute = AsyncMock(return_value=mock_result)

        long_feedback = "x" * 500

        await tracker.record_reflect_iteration(
            conversation_id=conv_id,
            batch_index=0,
            iteration=1,
            rubric_score=7.0,
            early_stopped=False,
            feedback=long_feedback,
        )

        entries = mock_conv.metadata_["reflect_iterations"]
        assert len(entries[0]["feedback"]) <= 200


# ============================================================================
# Class 11: AgentInvoker.run_reflect_loop
# ============================================================================

class TestRunReflectLoop:
    """AgentInvoker.run_reflect_loop — Sprint 203 A-05"""

    @pytest.mark.asyncio
    async def test_max_iterations_1_uses_inject_reflection(self) -> None:
        """Default max_iterations=1 calls inject_reflection() directly (Sprint 202 compat)."""
        from app.services.agent_team.agent_invoker import AgentInvoker, ProviderConfig

        invoker = AgentInvoker(provider_chain=[])
        step = ReflectStep(frequency=1, max_iterations=1)
        messages = _messages_with_assistant()
        original_len = len(messages)
        ollama = MagicMock()

        results = await invoker.run_reflect_loop(
            messages=messages,
            tool_results=_tool_results(),
            reflect_step=step,
            ollama_client=ollama,
            batch_index=0,
        )

        # inject_reflection appends a message; reflect_and_score is NOT called
        assert len(messages) == original_len + 1
        assert results == []  # No ReflectResult for simple injection
        ollama.generate.assert_not_called()

    @pytest.mark.asyncio
    async def test_frequency_zero_skips_all(self) -> None:
        from app.services.agent_team.agent_invoker import AgentInvoker

        invoker = AgentInvoker(provider_chain=[])
        step = ReflectStep(frequency=0, max_iterations=3)
        messages = _messages_with_assistant()
        ollama = MagicMock()

        results = await invoker.run_reflect_loop(
            messages=messages,
            tool_results=_tool_results(),
            reflect_step=step,
            ollama_client=ollama,
            batch_index=0,
        )

        assert results == []
        assert len(messages) == 2  # unchanged

    @pytest.mark.asyncio
    async def test_max_iterations_2_early_stop(self) -> None:
        """With max_iterations=2, early stop at iteration 1 stops the loop."""
        from app.services.agent_team.agent_invoker import AgentInvoker

        invoker = AgentInvoker(provider_chain=[])
        step = ReflectStep(frequency=1, max_iterations=2)
        messages = _messages_with_assistant()
        ollama = MagicMock()
        ollama.generate.return_value = _make_ollama_response(9, 9, 9)  # high score

        results = await invoker.run_reflect_loop(
            messages=messages,
            tool_results=_tool_results(),
            reflect_step=step,
            ollama_client=ollama,
            batch_index=0,
        )

        assert len(results) == 1
        assert results[0].early_stopped is True
        ollama.generate.assert_called_once()  # Only 1 evaluator call

    @pytest.mark.asyncio
    async def test_max_iterations_2_no_early_stop(self) -> None:
        """With max_iterations=2, both iterations run if score < 8.0."""
        from app.services.agent_team.agent_invoker import AgentInvoker

        invoker = AgentInvoker(provider_chain=[])
        step = ReflectStep(frequency=1, max_iterations=2)
        messages = _messages_with_assistant()
        ollama = MagicMock()
        ollama.generate.return_value = _make_ollama_response(6, 7, 8)  # score=7.0 < 8.0

        results = await invoker.run_reflect_loop(
            messages=messages,
            tool_results=_tool_results(),
            reflect_step=step,
            ollama_client=ollama,
            batch_index=0,
        )

        assert len(results) == 2
        assert not any(r.early_stopped for r in results)
        assert ollama.generate.call_count == 2

    @pytest.mark.asyncio
    async def test_telemetry_recorded_per_iteration(self) -> None:
        """record_reflect_iteration is called for each completed iteration."""
        from app.services.agent_team.agent_invoker import AgentInvoker

        invoker = AgentInvoker(provider_chain=[])
        step = ReflectStep(frequency=1, max_iterations=3)
        messages = _messages_with_assistant()
        ollama = MagicMock()
        ollama.generate.return_value = _make_ollama_response(6, 7, 8)  # score < 8.0

        tracker = AsyncMock()

        await invoker.run_reflect_loop(
            messages=messages,
            tool_results=_tool_results(),
            reflect_step=step,
            ollama_client=ollama,
            batch_index=1,
            conversation_tracker=tracker,
            conversation_id=uuid4(),
        )

        assert tracker.record_reflect_iteration.await_count == 3


# ============================================================================
# Class 12: AgentDefinition.max_reflect_iterations field
# ============================================================================

class TestAgentDefinitionMaxReflectIterations:
    """AgentDefinition.max_reflect_iterations — Sprint 203 A-01"""

    def test_field_exists_on_model(self) -> None:
        from app.models.agent_definition import AgentDefinition
        assert hasattr(AgentDefinition, "max_reflect_iterations")

    def test_default_is_1(self) -> None:
        from app.models.agent_definition import AgentDefinition
        col = AgentDefinition.__table__.c["max_reflect_iterations"]
        # server_default should be "1"
        assert col.server_default is not None

    def test_server_default_value(self) -> None:
        from app.models.agent_definition import AgentDefinition
        col = AgentDefinition.__table__.c["max_reflect_iterations"]
        assert "1" in str(col.server_default.arg)

    def test_column_is_not_nullable(self) -> None:
        from app.models.agent_definition import AgentDefinition
        col = AgentDefinition.__table__.c["max_reflect_iterations"]
        assert not col.nullable


# ============================================================================
# Class 13: Regression guards
# ============================================================================

class TestRegressionGuards:
    """Sprint 203 regression guard tests — verify Sprint 202 behavior unchanged"""

    def test_reflect_step_frequency_zero_still_works(self) -> None:
        """Sprint 177 frequency=0 disabling still works after Sprint 203 upgrade."""
        step = ReflectStep(frequency=0, max_iterations=3)
        assert step.should_reflect(_tool_results(with_error=True), batch_index=0) is False

    def test_inject_reflection_still_returns_modified_list(self) -> None:
        """Sprint 177 inject_reflection still returns the messages list."""
        step = ReflectStep()
        messages: list[dict] = [{"role": "user", "content": "test"}]
        result = step.inject_reflection(messages, _tool_results())
        assert result is messages
        assert len(result) == 2

    def test_early_stop_threshold_is_8(self) -> None:
        """EARLY_STOP_THRESHOLD must be 8.0 (not 7.0 pass threshold)."""
        assert EARLY_STOP_THRESHOLD == 8.0

    def test_default_evaluator_model_is_deepseek(self) -> None:
        """Default evaluator model must be deepseek-r1:32b."""
        assert "deepseek-r1" in REFLECT_EVALUATOR_MODEL

    def test_max_iterations_default_preserves_sprint202(self) -> None:
        """Default max_iterations=1 must preserve Sprint 202 single-inject behavior."""
        step = ReflectStep()
        assert step.max_iterations == 1

    def test_reflect_result_rubric_can_be_none(self) -> None:
        """rubric=None is valid for fallback path — not a typing error."""
        r = ReflectResult(rubric=None, iteration=1, early_stopped=False, feedback="fallback")
        assert r.rubric is None
        assert isinstance(r, ReflectResult)
