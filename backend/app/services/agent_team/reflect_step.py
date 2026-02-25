"""
=========================================================================
Reflect-after-tools — Evaluator-Optimizer loop (Sprint 203 upgrade)
SDLC Orchestrator - Sprint 203 (Evaluator-Optimizer + Evals Expansion)

Version: 2.0.0
Date: 2026-05-05
Status: ACTIVE - Sprint 203
Authority: CTO Approved (Anthropic Best Practices — Evaluator-Optimizer)
Reference: Anthropic "Building Effective AI Agents" Ch 11

Sprint History:
  Sprint 177 Day 6: Initial implementation (frequency-based reflection injection)
  Sprint 203:       Upgraded to Evaluator-Optimizer — scored iterations + early stop

Purpose:
- Score agent responses via LLM-as-Judge (deepseek-r1:32b, temperature=0)
- Inject reflection prompt only when quality score < EARLY_STOP_THRESHOLD (8.0)
- Early stop when avg score >= 8.0 (prevents unnecessary round-trips)
- max_reflect_iterations bounds loop to 1-3 iterations (CHECK constraint DB)
- Default max_iterations=1 preserves exact Sprint 202 behavior

Evaluator-Optimizer Pattern (Anthropic):
  Generator (agent) produces assistant message after tool batch
  → Evaluator scores: correctness + completeness + safety (0-10 each)
  → avg >= 8.0: early stop (no reflection injected, continue to next batch)
  → avg < 8.0:  inject scored feedback prompt → agent retries (next iteration)
  → After max_iterations: always proceed regardless of score

Zero Mock Policy: Production-ready with real Ollama evaluator calls.
=========================================================================
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any, Optional

from app.schemas.eval_rubric import EvalRubric

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

REFLECT_PROMPT = (
    "Review the tool results above. Were there any errors or unexpected outcomes? "
    "If so, explain what went wrong and suggest a corrected approach. "
    "If everything looks correct, confirm and proceed."
)

REFLECT_EVALUATOR_SYSTEM = """\
You are a code quality evaluator for an AI coding agent's tool usage session.
Score the agent's most recent response on three dimensions (0-10 each):
- correctness: Did the agent use the right tools with valid parameters?
- completeness: Were all necessary tools called and steps completed?
- safety: Were all permission checks followed, no credentials exposed?

Use your reasoning to be strict but fair. Be especially strict on safety.

Return ONLY valid JSON (no markdown fences, no extra text):
{"correctness": N, "completeness": N, "safety": N, "explanation": "..."}
"""

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Default evaluator model — deepseek-r1:32b uses <think> reasoning mode
REFLECT_EVALUATOR_MODEL = "deepseek-r1:32b"

# Early-stop threshold: above this, response quality is good enough to proceed.
# Higher than pass threshold (7.0) — only stop early when genuinely excellent.
EARLY_STOP_THRESHOLD = 8.0


# ---------------------------------------------------------------------------
# ReflectResult dataclass
# ---------------------------------------------------------------------------

@dataclass
class ReflectResult:
    """Result of a single Evaluator-Optimizer iteration.

    Attributes:
        rubric:        Scored EvalRubric from evaluator model.
                       None if evaluator call failed (fallback reflection used).
        iteration:     Which iteration produced this result (1-indexed).
        early_stopped: True if score >= EARLY_STOP_THRESHOLD before max_iterations.
        feedback:      Human-readable feedback injected into messages (or explanation).
    """

    rubric: Optional[EvalRubric]
    iteration: int
    early_stopped: bool
    feedback: str


# ---------------------------------------------------------------------------
# ReflectStep
# ---------------------------------------------------------------------------

class ReflectStep:
    """
    Manages reflect-after-tools injection with Evaluator-Optimizer scoring.

    Sprint 177: Simple reflection injection (frequency-based).
    Sprint 203: Upgraded to Evaluator-Optimizer — scores each iteration and
    stops early when quality threshold (avg >= 8.0) is reached.

    Configuration via agent_definitions:
      reflect_frequency:
        - 0 = disabled (no reflection at all)
        - 1 = reflect after every tool batch (Nanobot default, safest)
        - N = reflect every N-th batch

      max_reflect_iterations (Sprint 203 addition):
        - 1-3 iterations per batch (enforced by DB CHECK constraint)
        - Default=1 preserves exact Sprint 202 behavior (no extra round-trips)
    """

    def __init__(
        self,
        frequency: int = 1,
        max_iterations: int = 1,
        evaluator_model: str = REFLECT_EVALUATOR_MODEL,
    ) -> None:
        self.frequency = frequency
        self.max_iterations = max_iterations
        self.evaluator_model = evaluator_model

    def should_reflect(
        self,
        tool_results: list[dict[str, Any]],
        batch_index: int,
    ) -> bool:
        """
        Determine if reflection step should be injected.

        Always reflects on errors regardless of frequency setting.
        Otherwise follows batch_index % frequency schedule.
        """
        if self.frequency == 0:
            return False

        # Always reflect if any tool returned an error
        if any(r.get("error") for r in tool_results):
            return True

        return (batch_index % self.frequency) == 0

    @staticmethod
    def format_tool_summary(tool_results: list[dict[str, Any]]) -> str:
        """Format tool results into a human-readable summary."""
        lines: list[str] = []
        for result in tool_results:
            tool_name = result.get("tool", "unknown")
            error = result.get("error")
            if error:
                lines.append(f"- {tool_name}: ERROR: {error}")
            else:
                lines.append(f"- {tool_name}: OK")
        return "\n".join(lines)

    def inject_reflection(
        self,
        messages: list[dict[str, Any]],
        tool_results: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Append reflection prompt after tool results.

        Modifies messages in-place and returns the same list.
        Preserved for backward compatibility — Sprint 177 callers still work.
        For Evaluator-Optimizer scoring, use reflect_and_score() instead.
        """
        summary = self.format_tool_summary(tool_results)
        reflection_message = {
            "role": "user",
            "content": f"Tool execution summary:\n{summary}\n\n{REFLECT_PROMPT}",
        }
        messages.append(reflection_message)

        logger.debug(
            "Injected reflection step after %d tool results",
            len(tool_results),
        )
        return messages

    async def reflect_and_score(
        self,
        messages: list[dict[str, Any]],
        tool_results: list[dict[str, Any]],
        batch_index: int,
        ollama_client: Any,
        iteration: int = 1,
        is_gate_action: bool = False,
    ) -> ReflectResult:
        """Evaluate the last agent response and inject reflection if needed.

        Implements the Evaluator-Optimizer pattern (Sprint 203):
          1. Extract last assistant message for evaluation.
          2. Call evaluator model (deepseek-r1:32b, temperature=0) to score it.
          3. If avg >= EARLY_STOP_THRESHOLD (8.0): early stop, no reflection injected.
          4. If avg < 8.0: inject scored reflection prompt for next iteration.
          5. Return ReflectResult with rubric, iteration, early_stopped flag.

        On evaluator failure (network error, parse error): falls back to the
        simple inject_reflection() path and returns rubric=None.

        Args:
            messages:       Current conversation message list (modified in-place
                            when reflection is injected).
            tool_results:   Tool results from the last batch.
            batch_index:    Current batch number (0-indexed, for logging).
            ollama_client:  OllamaService instance for evaluator calls (sync).
            iteration:      Current iteration number (1-indexed).
            is_gate_action: True if this is a governance gate action (reserved
                            for future stricter safety threshold).

        Returns:
            ReflectResult with scored rubric, iteration number, and early_stopped flag.
        """
        # Extract last assistant message for evaluation
        last_assistant = self._extract_last_assistant(messages)

        if not last_assistant:
            # No assistant message to evaluate — fall back to plain reflection
            logger.debug(
                "REFLECT_EVAL: No assistant message at batch=%d iter=%d, "
                "falling back to inject_reflection",
                batch_index,
                iteration,
            )
            feedback = self.format_tool_summary(tool_results)
            self.inject_reflection(messages, tool_results)
            return ReflectResult(
                rubric=None,
                iteration=iteration,
                early_stopped=False,
                feedback=feedback,
            )

        # Build evaluation prompt
        eval_prompt = self._build_reflect_eval_prompt(
            last_assistant=last_assistant,
            tool_results=tool_results,
            batch_index=batch_index,
        )

        # Call evaluator model (sync API, temperature=0 for determinism)
        rubric: Optional[EvalRubric] = None
        try:
            response = ollama_client.generate(
                prompt=eval_prompt,
                model=self.evaluator_model,
                system=REFLECT_EVALUATOR_SYSTEM,
                temperature=0.0,
                max_tokens=512,
            )
            raw_text = response.response.strip()
            rubric = _parse_rubric(raw_text)

            logger.info(
                "REFLECT_EVAL: batch=%d, iter=%d/%d, "
                "scores=(%d,%d,%d), total=%.1f, threshold=%.1f",
                batch_index,
                iteration,
                self.max_iterations,
                rubric.correctness,
                rubric.completeness,
                rubric.safety,
                rubric.total_score,
                EARLY_STOP_THRESHOLD,
            )

        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "REFLECT_EVAL: Evaluator call failed at batch=%d iter=%d: %s. "
                "Falling back to plain reflection.",
                batch_index,
                iteration,
                exc,
            )
            # Evaluator failure is non-fatal — fall back to simple reflection
            feedback = self.format_tool_summary(tool_results)
            self.inject_reflection(messages, tool_results)
            return ReflectResult(
                rubric=None,
                iteration=iteration,
                early_stopped=False,
                feedback=feedback,
            )

        # ── Early stop check ────────────────────────────────────────────────
        if rubric.total_score >= EARLY_STOP_THRESHOLD:
            logger.info(
                "REFLECT_EVAL: Early stop at batch=%d iter=%d — "
                "score %.1f >= threshold %.1f",
                batch_index,
                iteration,
                rubric.total_score,
                EARLY_STOP_THRESHOLD,
            )
            return ReflectResult(
                rubric=rubric,
                iteration=iteration,
                early_stopped=True,
                feedback=rubric.explanation,
            )

        # ── Inject scored reflection (score below threshold) ─────────────────
        summary = self.format_tool_summary(tool_results)
        reflection_content = (
            f"Tool execution summary:\n{summary}\n\n"
            f"Evaluator feedback (score {rubric.total_score:.1f}/10): "
            f"{rubric.explanation}\n\n"
            f"{REFLECT_PROMPT}"
        )
        messages.append({"role": "user", "content": reflection_content})

        feedback = (
            f"Quality score {rubric.total_score:.1f}/10 below threshold "
            f"{EARLY_STOP_THRESHOLD}. {rubric.explanation}"
        )
        logger.debug(
            "REFLECT_EVAL: Injected scored reflection at batch=%d iter=%d",
            batch_index,
            iteration,
        )
        return ReflectResult(
            rubric=rubric,
            iteration=iteration,
            early_stopped=False,
            feedback=feedback,
        )

    @staticmethod
    def _extract_last_assistant(
        messages: list[dict[str, Any]],
    ) -> Optional[str]:
        """Extract the content of the last assistant message.

        Handles both plain string content and structured content blocks
        (list of {type, text} dicts as returned by Anthropic API).

        Returns:
            Content string of the last assistant message, or None if not found.
        """
        for msg in reversed(messages):
            if msg.get("role") == "assistant":
                content = msg.get("content", "")
                if isinstance(content, str):
                    return content or None
                # Structured content blocks (Anthropic API format)
                if isinstance(content, list):
                    text_parts = [
                        block.get("text", "")
                        for block in content
                        if isinstance(block, dict) and block.get("type") == "text"
                    ]
                    joined = " ".join(text_parts).strip()
                    return joined if joined else None
        return None

    @staticmethod
    def _build_reflect_eval_prompt(
        last_assistant: str,
        tool_results: list[dict[str, Any]],
        batch_index: int,
    ) -> str:
        """Build the evaluator prompt for scoring the agent's tool-use response.

        Includes tool execution context (with truncated outputs to avoid token
        overflow) and the agent's latest assistant message.
        """
        tool_lines: list[str] = []
        for r in tool_results:
            tool_name = r.get("tool", "unknown")
            error = r.get("error")
            if error:
                tool_lines.append(f"- {tool_name}: ERROR: {error}")
            else:
                output = str(r.get("output", ""))
                # Truncate long outputs to avoid filling evaluator context
                tool_lines.append(f"- {tool_name}: OK → {output[:200]}")

        tool_summary = "\n".join(tool_lines) if tool_lines else "(no tool results)"

        return "\n".join([
            "## Agent Tool-Use Quality Evaluation",
            "",
            f"### Tool Execution Batch {batch_index}",
            tool_summary,
            "",
            "### Agent Response",
            last_assistant[:2000],  # truncate to avoid token overflow
            "",
            "### Instructions",
            "Score the agent response quality given the tool execution results above.",
            "Return ONLY valid JSON: "
            '{"correctness": N, "completeness": N, "safety": N, "explanation": "..."}',
        ])


# ---------------------------------------------------------------------------
# Module-level rubric parsing helpers
# (mirrors eval_scorer._parse_rubric + _extract_score to avoid import coupling)
# ---------------------------------------------------------------------------

def _parse_rubric(raw_text: str) -> EvalRubric:
    """Parse LLM evaluator output into EvalRubric.

    Handles three formats:
    1. Clean JSON:             {"correctness": 8, ...}
    2. Markdown-wrapped JSON:  ```json {...} ```
    3. Fallback regex:         correctness: 8, completeness: 9, safety: 10

    Raises:
        ValueError: If none of the three parsing strategies succeed.
    """
    cleaned = raw_text.strip()

    # Strip markdown code fences if present
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    # Stage 1: direct JSON parse
    try:
        data = json.loads(cleaned)
        return EvalRubric(
            correctness=int(data.get("correctness", 0)),
            completeness=int(data.get("completeness", 0)),
            safety=int(data.get("safety", 0)),
            explanation=str(data.get("explanation", "")),
        )
    except (json.JSONDecodeError, ValueError, TypeError):
        pass

    # Stage 2: extract JSON object from deepseek-r1 <think>...</think> output
    json_match = re.search(r'\{[^{}]*"correctness"[^{}]*\}', cleaned)
    if json_match:
        try:
            data = json.loads(json_match.group())
            return EvalRubric(
                correctness=int(data.get("correctness", 0)),
                completeness=int(data.get("completeness", 0)),
                safety=int(data.get("safety", 0)),
                explanation=str(data.get("explanation", "")),
            )
        except (json.JSONDecodeError, ValueError, TypeError):
            pass

    # Stage 3: regex extraction of individual scores
    correctness = _extract_score(cleaned, "correctness")
    completeness = _extract_score(cleaned, "completeness")
    safety = _extract_score(cleaned, "safety")

    if correctness is not None and completeness is not None and safety is not None:
        return EvalRubric(
            correctness=correctness,
            completeness=completeness,
            safety=safety,
            explanation=f"Parsed via regex fallback from: {cleaned[:200]}",
        )

    raise ValueError(
        f"Failed to parse rubric scores from evaluator output: {cleaned[:500]}"
    )


def _extract_score(text: str, dimension: str) -> Optional[int]:
    """Extract a single integer score for a named dimension.

    Matches patterns like:
      "correctness": 8
      correctness: 8
      Correctness = 8
    """
    pattern = rf'{dimension}\s*[=:]\s*(\d+)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        val = int(match.group(1))
        return min(max(val, 0), 10)
    return None
