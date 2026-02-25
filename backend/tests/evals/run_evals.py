#!/usr/bin/env python3
"""
=========================================================================
CI Eval Runner — Sprint 204 (Confidence-Based Routing + Evals Expansion)
SDLC Orchestrator - Sprint 204

Version: 2.0.0
Date: 2026-05-19
Status: ACTIVE - Sprint 204
Authority: CTO Approved (Anthropic Best Practices Gap 5 — Evals)

Purpose:
- Load all 20 YAML eval cases from tests/evals/cases/
  - 15 behavioral cases (Sprint 203): LLM-as-judge scoring via deepseek-r1:32b
  - 5 routing cases (Sprint 204): deterministic classify() scoring (no LLM)
- Run full EvalScorer.run_suite() for behavioral cases against a live Ollama evaluator
- Score routing cases via classify(DEFAULT_CLASSIFICATION_RULES, prompt) directly
- Compare results to reference_answers/baseline.json for regression detection
- Exit non-zero on regression (for CI gates)

Routing Eval Cases (Sprint 204 — Blocker 4):
  Cases with expected_hint set are routing eval cases — scored deterministically
  by calling query_classifier.classify() and checking hint/confidence assertions.
  No Ollama required for routing cases (deterministic pure function).

Usage:
  # Run all cases against live Ollama (routing cases are always deterministic)
  python tests/evals/run_evals.py

  # Dry run (no live Ollama calls — behavioral cases use expected_behavior as mock)
  python tests/evals/run_evals.py --dry-run

  # Run only specific tags
  python tests/evals/run_evals.py --tags governance,gate
  python tests/evals/run_evals.py --tags routing,sprint204

  # Print detailed scores
  python tests/evals/run_evals.py --verbose

Exit codes:
  0 — all cases passed, no regression
  1 — regression detected (avg score drop > 20% from baseline)
  2 — eval suite failed (< 50% cases scored)
  3 — configuration error (Ollama not available)
=========================================================================
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Ensure project root is in sys.path when running as standalone script
_BACKEND_DIR = Path(__file__).parent.parent.parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.schemas.eval_rubric import EvalRubric, EvalRunResult, EvalSuiteResult, EvalTestCase
from app.services.agent_team.config import DEFAULT_CLASSIFICATION_RULES
from app.services.agent_team.eval_scorer import (
    DEFAULT_REGRESSION_THRESHOLD,
    EvalScorer,
    EvalScorerError,
)
from app.services.agent_team.query_classifier import classify
from app.services.ollama_service import OllamaService

logger = logging.getLogger("eval_runner")

_CASES_DIR = Path(__file__).parent / "cases"
_BASELINE_PATH = Path(__file__).parent / "reference_answers" / "baseline.json"

# Minimum fraction of cases that must be scored for a valid suite run
_MIN_SCORED_FRACTION = 0.50


def _load_baseline() -> EvalSuiteResult | None:
    """Load baseline EvalSuiteResult from reference_answers/baseline.json.

    Returns None if the baseline file is missing (first run).
    """
    if not _BASELINE_PATH.exists():
        logger.warning("No baseline found at %s — skipping regression check.", _BASELINE_PATH)
        return None

    with open(_BASELINE_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # Build a lightweight EvalSuiteResult from the JSON averages
    from app.schemas.eval_rubric import EvalRubric, EvalRunResult

    results = []
    for case_id, scores in raw.items():
        if case_id.startswith("_"):
            continue  # skip comment keys
        rubric = EvalRubric(
            correctness=scores["correctness"],
            completeness=scores["completeness"],
            safety=scores["safety"],
            explanation="baseline",
        )
        results.append(EvalRunResult(
            case_id=case_id,
            tool_name="baseline",
            prompt="",
            actual_response="",
            rubric=rubric,
            evaluator_model="baseline",
        ))

    suite = EvalSuiteResult(results=results)
    suite.compute_summary()
    return suite


def _filter_by_tags(
    cases: list,
    tags: list[str],
) -> list:
    """Filter eval cases to only those matching any of the given tags."""
    if not tags:
        return cases
    return [c for c in cases if any(t in c.tags for t in tags)]


def _score_routing_case(case: EvalTestCase) -> EvalRunResult:
    """Score a routing eval case deterministically via classify().

    Sprint 204 (Track C — Blocker 4 resolution):
    Routing cases have expected_hint and/or expected_min_confidence set.
    They are scored by calling classify(DEFAULT_CLASSIFICATION_RULES, prompt)
    directly — no LLM calls required. Classification is a pure function.

    Scoring:
    - hint correct AND confidence >= floor  → correctness=10, completeness=10, safety=10
    - hint wrong                            → correctness=0,  completeness=7,  safety=10
    - hint correct but confidence too low   → correctness=7,  completeness=7,  safety=10

    Safety is always 10 for routing cases — classification routing does not
    touch sensitive data or credential handling.

    Args:
        case: EvalTestCase with expected_hint and/or expected_min_confidence set.

    Returns:
        EvalRunResult with deterministic rubric score.
    """
    result = classify(DEFAULT_CLASSIFICATION_RULES, case.prompt)

    actual_response = (
        f"hint={result.hint!r}, confidence={result.confidence:.2f}, "
        f"method={result.method!r}, matches={result.matches}"
    )

    hint_ok = (case.expected_hint is None) or (result.hint == case.expected_hint)
    confidence_ok = (
        case.expected_min_confidence is None
        or result.confidence >= case.expected_min_confidence
    )

    if hint_ok and confidence_ok:
        rubric = EvalRubric(
            correctness=10,
            completeness=10,
            safety=10,
            explanation=(
                f"Routing correct: hint={result.hint!r} == expected={case.expected_hint!r}, "
                f"confidence={result.confidence:.2f} >= {case.expected_min_confidence}"
            ),
        )
    elif not hint_ok:
        rubric = EvalRubric(
            correctness=0,
            completeness=7,
            safety=10,
            explanation=(
                f"Routing FAIL (wrong hint): expected={case.expected_hint!r}, "
                f"got={result.hint!r} (confidence={result.confidence:.2f})"
            ),
        )
    else:
        # hint correct but confidence below floor
        rubric = EvalRubric(
            correctness=7,
            completeness=7,
            safety=10,
            explanation=(
                f"Routing FAIL (low confidence): hint={result.hint!r} correct, "
                f"but {result.confidence:.2f} < required {case.expected_min_confidence}"
            ),
        )

    logger.info(
        "TRACE_ROUTING: case=%s, hint=%r (expected=%r), "
        "confidence=%.2f (min=%s), passed=%s",
        case.id,
        result.hint,
        case.expected_hint,
        result.confidence,
        case.expected_min_confidence,
        rubric.passed,
    )

    return EvalRunResult(
        case_id=case.id,
        tool_name=case.tool_name,
        prompt=case.prompt,
        actual_response=actual_response,
        rubric=rubric,
        evaluator_model="deterministic/classify",
    )


def run(dry_run: bool = False, tags: list[str] | None = None, verbose: bool = False) -> int:
    """Run the eval suite and return exit code.

    Args:
        dry_run: If True, use the baseline expected_behavior as mock responses
                 (no live Ollama calls).
        tags:    Optional list of tags to filter cases. None = all cases.
        verbose: Print detailed per-case scores.

    Returns:
        Exit code: 0=pass, 1=regression, 2=suite_failed, 3=config_error.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # ── Load YAML cases ──────────────────────────────────────────────────────
    all_cases = EvalScorer.load_cases_from_yaml(_CASES_DIR)

    if not all_cases:
        logger.error("No YAML eval cases found in %s", _CASES_DIR)
        return 2

    filtered_cases = _filter_by_tags(all_cases, tags or [])
    if not filtered_cases:
        logger.warning("No cases matched tags: %s", tags)
        return 2

    # ── Split: routing (deterministic) vs behavioral (LLM-as-judge) ──────────
    # Sprint 204 (Track C): Cases with expected_hint are routing eval cases —
    # scored via classify() without Ollama. Behavioral cases use LLM-as-judge.
    routing_cases = [
        c for c in filtered_cases
        if c.expected_hint is not None or c.expected_min_confidence is not None
    ]
    behavioral_cases = [c for c in filtered_cases if c not in routing_cases]

    logger.info(
        "Eval suite: %d total (%d routing + %d behavioral) of %d loaded",
        len(filtered_cases),
        len(routing_cases),
        len(behavioral_cases),
        len(all_cases),
    )

    # ── Check Ollama only if behavioral cases exist ───────────────────────────
    ollama = OllamaService()
    if behavioral_cases and not dry_run and not ollama.is_available:
        logger.error(
            "Ollama is not available at %s. "
            "Run with --dry-run or start Ollama first. "
            "(%d routing-only cases can still run without Ollama.)",
            ollama.base_url if hasattr(ollama, "base_url") else "(unknown URL)",
            len(routing_cases),
        )
        return 3

    # ── Load baseline ────────────────────────────────────────────────────────
    baseline = _load_baseline()

    # ── Score routing cases (deterministic — no Ollama needed) ───────────────
    routing_results: list[EvalRunResult] = []
    for case in routing_cases:
        result = _score_routing_case(case)
        routing_results.append(result)

    # ── Score behavioral cases (LLM-as-judge via EvalScorer) ─────────────────
    behavioral_suite = EvalSuiteResult(evaluator_model="")
    if behavioral_cases:
        scorer = EvalScorer(ollama_service=ollama)

        response_generator = None
        if dry_run:
            # Use expected_behavior as a mock agent response (no real LLM calls)
            response_generator = lambda prompt: (
                next(
                    (c.expected_behavior for c in behavioral_cases if c.prompt == prompt),
                    prompt,
                )
            )
            logger.info("DRY RUN: using expected_behavior as mock agent responses")

        behavioral_suite = scorer.run_suite(
            cases=behavioral_cases,
            response_generator=response_generator,
            baseline=baseline,
        )

    # ── Merge routing + behavioral into a single suite result ─────────────────
    suite = EvalSuiteResult(
        results=routing_results + behavioral_suite.results,
        evaluator_model=behavioral_suite.evaluator_model or "deterministic/classify",
    )
    suite.compute_summary()
    if baseline is not None:
        suite.check_regression(baseline, DEFAULT_REGRESSION_THRESHOLD)

    # ── Print results ────────────────────────────────────────────────────────
    routing_passed = sum(1 for r in routing_results if r.passed)
    behavioral_passed = behavioral_suite.passed_cases

    print(f"\n{'='*60}")
    print(f"EVAL SUITE RESULTS — Sprint 204")
    print(f"{'='*60}")
    print(
        f"Cases:      {suite.passed_cases}/{suite.total_cases} passed "
        f"(routing: {routing_passed}/{len(routing_results)}, "
        f"behavioral: {behavioral_passed}/{len(behavioral_suite.results)})"
    )
    print(f"Avg scores: correctness={suite.avg_correctness:.1f}, "
          f"completeness={suite.avg_completeness:.1f}, "
          f"safety={suite.avg_safety:.1f}")
    print(f"Avg total:  {suite.avg_total:.1f}/10")
    print(f"Regression: {'DETECTED' if suite.regression_detected else 'none'}")

    if suite.regression_detected:
        print(f"\n⚠️  REGRESSION: {suite.regression_details}")

    if verbose:
        print(f"\n{'─'*60}")
        print("Per-case scores:")
        for r in suite.results:
            status = "PASS" if r.passed else "FAIL"
            model_tag = "[routing]" if r.evaluator_model == "deterministic/classify" else "[llm]"
            print(
                f"  [{status}] {model_tag} {r.case_id:<30} "
                f"C={r.rubric.correctness} P={r.rubric.completeness} "
                f"S={r.rubric.safety} avg={r.rubric.total_score:.1f}"
            )
    print(f"{'='*60}\n")

    # ── Exit code logic ───────────────────────────────────────────────────────
    # Check minimum scored fraction
    if suite.total_cases > 0 and (suite.total_cases / len(filtered_cases)) < _MIN_SCORED_FRACTION:
        logger.error(
            "Only %d/%d cases scored (< %.0f%% minimum).",
            suite.total_cases,
            len(filtered_cases),
            _MIN_SCORED_FRACTION * 100,
        )
        return 2

    if suite.regression_detected:
        return 1

    return 0


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SDLC Orchestrator CI Eval Runner — Sprint 203",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Use expected_behavior as mock responses (no live Ollama calls)",
    )
    parser.add_argument(
        "--tags",
        type=str,
        default="",
        help="Comma-separated list of tags to filter cases (e.g. governance,gate)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed per-case scores",
    )
    args = parser.parse_args()

    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
    exit_code = run(dry_run=args.dry_run, tags=tags, verbose=args.verbose)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
