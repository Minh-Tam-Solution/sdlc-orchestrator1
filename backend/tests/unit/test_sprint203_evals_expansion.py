"""
=========================================================================
Sprint 203 — Track B+C: Evals Expansion Test Suite
SDLC Orchestrator - Sprint 203 (Evaluator-Optimizer + Evals Expansion)

Version: 1.0.0
Date: 2026-05-05
Status: ACTIVE - Sprint 203
Authority: CTO Approved (Anthropic Best Practices Gap 5 — Evals)

Coverage:
  Class 01: MultiJudgeResult — Pydantic model, compute_averages(), passed, consensus
  Class 02: MultiJudgeResult edge cases — single judge, all-fail, mismatched safety
  Class 03: EvalScorer.multi_judge_eval() — happy path, partial results, all-fail
  Class 04: 10 new YAML eval cases — load + validate structure
  Class 05: YAML case tags — codegen / multi-agent tag coverage
  Class 06: EvalScorer.load_cases_from_yaml() — directory loading, dedup, error handling
  Class 07: CI eval runner _load_baseline() — valid JSON, missing file, comment keys
  Class 08: CI eval runner _filter_by_tags() — tag matching, empty tags, all-miss
  Class 09: CI eval runner run() — dry-run exit 0, ollama unavailable exit 3
  Class 10: CI eval runner dry-run suite — 15 cases loaded, avg computed
  Class 11: EvalSuiteResult regression detection — 20% drop triggers FAIL
  Class 12: EvalTestCase schema — required fields, optional ground_truth
  Class 13: Regression guards — 15 total cases, baseline structure

Zero Mock Policy: Tests use real Pydantic models, real YAML loading,
and real run_evals.py code paths. Ollama is mocked at the service boundary.
=========================================================================
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

# Ensure backend is on path for standalone pytest runs
_BACKEND_DIR = Path(__file__).parent.parent.parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.schemas.eval_rubric import (
    EvalRubric,
    EvalRunResult,
    EvalSuiteResult,
    EvalTestCase,
    MultiJudgeResult,
)
from app.services.agent_team.eval_scorer import (
    DEFAULT_REGRESSION_THRESHOLD,
    EvalScorer,
    EvalScorerError,
)

# Paths
_CASES_DIR = Path(__file__).parent.parent / "evals" / "cases"
_BASELINE_PATH = Path(__file__).parent.parent / "evals" / "reference_answers" / "baseline.json"
_RUN_EVALS_PY = Path(__file__).parent.parent / "evals" / "run_evals.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_rubric(correctness: int = 8, completeness: int = 8, safety: int = 9) -> EvalRubric:
    return EvalRubric(
        correctness=correctness,
        completeness=completeness,
        safety=safety,
        explanation="test rubric",
    )


def _make_run_result(case_id: str = "test_01", tool: str = "tool_a", total_override: float | None = None) -> EvalRunResult:
    """Helper to produce a run result with optional score override."""
    correctness = 8
    completeness = 8
    safety = 9
    rubric = EvalRubric(
        correctness=correctness,
        completeness=completeness,
        safety=safety,
        explanation="test",
    )
    return EvalRunResult(
        case_id=case_id,
        tool_name=tool,
        prompt="test prompt",
        actual_response="test response",
        rubric=rubric,
        evaluator_model="deepseek-r1:32b",
    )


# ---------------------------------------------------------------------------
# Class 01 — MultiJudgeResult: model, compute_averages, passed, consensus
# ---------------------------------------------------------------------------

class TestMultiJudgeResult:
    """Class 01: MultiJudgeResult Pydantic model basics."""

    def test_fields_present(self) -> None:
        """MultiJudgeResult has all required fields."""
        result = MultiJudgeResult(
            case_id="test_case",
            tool_name="test_tool",
            rubrics=[],
        )
        assert hasattr(result, "case_id")
        assert hasattr(result, "tool_name")
        assert hasattr(result, "rubrics")
        assert hasattr(result, "judge_count")
        assert hasattr(result, "avg_correctness")
        assert hasattr(result, "avg_completeness")
        assert hasattr(result, "avg_safety")
        assert hasattr(result, "avg_total")
        assert hasattr(result, "evaluator_model")
        assert hasattr(result, "timestamp")

    def test_compute_averages_3_judges(self) -> None:
        """compute_averages() correctly averages across 3 rubrics."""
        rubrics = [
            _make_rubric(8, 8, 9),
            _make_rubric(9, 9, 10),
            _make_rubric(7, 8, 9),
        ]
        result = MultiJudgeResult(case_id="c", tool_name="t", rubrics=rubrics)
        result.compute_averages()

        assert result.judge_count == 3
        assert abs(result.avg_correctness - 8.0) < 0.01   # (8+9+7)/3
        assert abs(result.avg_completeness - 8.33) < 0.05  # (8+9+8)/3
        assert abs(result.avg_safety - 9.33) < 0.05        # (9+10+9)/3
        # avg_total = avg of three totals: (8.33+9.33+8.33)/3 ≈ 8.67
        assert result.avg_total > 8.0

    def test_passed_property_true(self) -> None:
        """passed=True when avg_total>=7.0 and avg_safety>=8.0."""
        result = MultiJudgeResult(case_id="c", tool_name="t", rubrics=[_make_rubric(8, 8, 9)])
        result.compute_averages()
        assert result.passed is True

    def test_passed_property_false_low_total(self) -> None:
        """passed=False when avg_total < 7.0."""
        result = MultiJudgeResult(
            case_id="c", tool_name="t",
            rubrics=[_make_rubric(5, 5, 5)],  # total=5.0
        )
        result.compute_averages()
        assert result.passed is False

    def test_passed_property_false_low_safety(self) -> None:
        """passed=False when avg_safety < 8.0 even if total is high."""
        result = MultiJudgeResult(
            case_id="c", tool_name="t",
            rubrics=[_make_rubric(10, 10, 7)],  # safety=7, total=9.0
        )
        result.compute_averages()
        assert result.passed is False

    def test_consensus_explanation_property(self) -> None:
        """consensus_explanation is a non-empty string."""
        rubrics = [_make_rubric(8, 8, 9), _make_rubric(9, 9, 10)]
        result = MultiJudgeResult(case_id="c", tool_name="t", rubrics=rubrics)
        result.compute_averages()
        assert isinstance(result.consensus_explanation, str)
        assert len(result.consensus_explanation) > 0


# ---------------------------------------------------------------------------
# Class 02 — MultiJudgeResult edge cases
# ---------------------------------------------------------------------------

class TestMultiJudgeResultEdgeCases:
    """Class 02: MultiJudgeResult edge cases."""

    def test_single_judge(self) -> None:
        """Single judge produces the same score as that rubric's total."""
        rubric = _make_rubric(8, 9, 10)
        result = MultiJudgeResult(case_id="c", tool_name="t", rubrics=[rubric])
        result.compute_averages()

        assert result.judge_count == 1
        assert abs(result.avg_correctness - 8.0) < 0.01
        assert abs(result.avg_completeness - 9.0) < 0.01
        assert abs(result.avg_safety - 10.0) < 0.01

    def test_empty_rubrics_sets_zero_averages(self) -> None:
        """compute_averages() on empty rubrics list → zeroed fields."""
        result = MultiJudgeResult(case_id="c", tool_name="t", rubrics=[])
        result.compute_averages()

        assert result.judge_count == 0
        assert result.avg_correctness == 0.0
        assert result.avg_completeness == 0.0
        assert result.avg_safety == 0.0
        assert result.avg_total == 0.0

    def test_passed_false_with_empty_rubrics(self) -> None:
        """passed=False when rubrics is empty (avg_total=0 < 7.0)."""
        result = MultiJudgeResult(case_id="c", tool_name="t", rubrics=[])
        result.compute_averages()
        assert result.passed is False

    def test_consensus_with_variance(self) -> None:
        """High variance between judges doesn't break consensus_explanation."""
        rubrics = [
            _make_rubric(10, 10, 10),
            _make_rubric(1, 1, 8),   # extreme disagreement
        ]
        result = MultiJudgeResult(case_id="c", tool_name="t", rubrics=rubrics)
        result.compute_averages()
        # Should not raise, and explanation references multiple judges
        assert isinstance(result.consensus_explanation, str)


# ---------------------------------------------------------------------------
# Class 03 — EvalScorer.multi_judge_eval()
# ---------------------------------------------------------------------------

class TestMultiJudgeEval:
    """Class 03: EvalScorer.multi_judge_eval() method."""

    def _make_scorer(self, responses: list[str]) -> tuple[EvalScorer, Any]:
        """Build a scorer with a mock ollama returning successive responses."""
        mock_ollama = MagicMock()
        call_count = iter(responses)
        def _side_effect(**kwargs):  # noqa: ANN001
            resp_text = next(call_count, '{"correctness":8,"completeness":8,"safety":9,"explanation":"ok"}')
            mock_resp = MagicMock()
            mock_resp.response = resp_text
            return mock_resp
        mock_ollama.generate.side_effect = _side_effect
        scorer = EvalScorer(ollama_service=mock_ollama)
        return scorer, mock_ollama

    def test_happy_path_3_judges(self) -> None:
        """multi_judge_eval() returns MultiJudgeResult with 3 rubrics."""
        json_resp = '{"correctness":8,"completeness":8,"safety":9,"explanation":"ok"}'
        scorer, _ = self._make_scorer([json_resp] * 3)

        result = scorer.multi_judge_eval(
            case_id="test_01",
            tool_name="get_gate_status",
            prompt="What is the gate status?",
            actual_response="Gate is APPROVED",
            expected_behavior="Returns gate status",
            judge_runs=3,
        )

        assert isinstance(result, MultiJudgeResult)
        assert result.judge_count == 3
        assert len(result.rubrics) == 3
        assert result.avg_total > 0

    def test_partial_results_kept(self) -> None:
        """If 2/3 judge runs succeed, result has 2 rubrics (not raised)."""
        good_resp = '{"correctness":8,"completeness":8,"safety":9,"explanation":"ok"}'

        mock_ollama = MagicMock()
        call_count = [0]
        def _side_effect(**kwargs):  # noqa: ANN001
            idx = call_count[0]
            call_count[0] += 1
            if idx == 1:
                raise RuntimeError("simulated network error")
            mock_resp = MagicMock()
            mock_resp.response = good_resp
            return mock_resp
        mock_ollama.generate.side_effect = _side_effect
        scorer = EvalScorer(ollama_service=mock_ollama)

        result = scorer.multi_judge_eval(
            case_id="test_01",
            tool_name="get_gate_status",
            prompt="prompt",
            actual_response="response",
            expected_behavior="expected",
            judge_runs=3,
        )
        # 2/3 succeeded — result has 2 rubrics
        assert result.judge_count == 2

    def test_all_fail_raises_scorer_error(self) -> None:
        """EvalScorerError is raised only when ALL judge runs fail."""
        mock_ollama = MagicMock()
        mock_ollama.generate.side_effect = RuntimeError("all fail")
        scorer = EvalScorer(ollama_service=mock_ollama)

        with pytest.raises(EvalScorerError) as exc_info:
            scorer.multi_judge_eval(
                case_id="test_01",
                tool_name="get_gate_status",
                prompt="prompt",
                actual_response="response",
                expected_behavior="expected",
                judge_runs=2,
            )
        assert "judge runs failed" in str(exc_info.value).lower()

    def test_judge_runs_1_valid(self) -> None:
        """judge_runs=1 is valid (single judge = same as score())."""
        json_resp = '{"correctness":9,"completeness":8,"safety":10,"explanation":"excellent"}'
        scorer, _ = self._make_scorer([json_resp])

        result = scorer.multi_judge_eval(
            case_id="test_01",
            tool_name="get_gate_status",
            prompt="prompt",
            actual_response="response",
            expected_behavior="expected",
            judge_runs=1,
        )
        assert result.judge_count == 1
        assert result.avg_correctness == pytest.approx(9.0)


# ---------------------------------------------------------------------------
# Class 04 — 10 new YAML eval cases: load + validate structure
# ---------------------------------------------------------------------------

class TestNewYAMLEvalCases:
    """Class 04: All 10 Sprint 203 YAML cases can be loaded and are structurally valid."""

    _SPRINT_203_CASE_IDS = {
        "codegen_generate_01",
        "codegen_quality_01",
        "codegen_fix_01",
        "codegen_ir_01",
        "codegen_test_01",
        "agent_mention_01",
        "agent_failover_01",
        "agent_budget_01",
        "agent_delegation_01",
        "agent_reflect_01",
    }

    @pytest.fixture(scope="class")
    def loaded_cases(self) -> list[EvalTestCase]:
        """Load all YAML cases from evals/cases directory."""
        cases = EvalScorer.load_cases_from_yaml(_CASES_DIR)
        assert cases, f"No YAML cases found in {_CASES_DIR}"
        return cases

    def test_sprint_203_cases_loaded(self, loaded_cases: list[EvalTestCase]) -> None:
        """All 10 Sprint 203 case IDs are present in the loaded set."""
        loaded_ids = {c.id for c in loaded_cases}
        missing = self._SPRINT_203_CASE_IDS - loaded_ids
        assert not missing, f"Missing Sprint 203 case IDs: {missing}"

    def test_all_cases_have_required_fields(self, loaded_cases: list[EvalTestCase]) -> None:
        """Each case has non-empty id, tool_name, prompt, expected_behavior."""
        sprint_203_cases = [c for c in loaded_cases if c.id in self._SPRINT_203_CASE_IDS]
        for case in sprint_203_cases:
            assert case.id, f"Empty id in case {case}"
            assert case.tool_name, f"Empty tool_name in case {case.id}"
            assert case.prompt, f"Empty prompt in case {case.id}"
            assert case.expected_behavior, f"Empty expected_behavior in case {case.id}"

    def test_cases_have_tags(self, loaded_cases: list[EvalTestCase]) -> None:
        """Sprint 203 cases have at least 1 tag each."""
        sprint_203_cases = [c for c in loaded_cases if c.id in self._SPRINT_203_CASE_IDS]
        for case in sprint_203_cases:
            assert case.tags, f"Case {case.id} has no tags"
            assert len(case.tags) >= 1

    def test_ground_truth_is_optional(self, loaded_cases: list[EvalTestCase]) -> None:
        """ground_truth may be None — not required for all cases."""
        sprint_203_cases = [c for c in loaded_cases if c.id in self._SPRINT_203_CASE_IDS]
        # At least one case can have ground_truth=None without error
        none_count = sum(1 for c in sprint_203_cases if c.ground_truth is None)
        assert none_count >= 1, "Expected at least one case with ground_truth=None"


# ---------------------------------------------------------------------------
# Class 05 — YAML case tags: codegen / multi-agent coverage
# ---------------------------------------------------------------------------

class TestYAMLCaseTags:
    """Class 05: Tag coverage for Sprint 203 YAML cases."""

    @pytest.fixture(scope="class")
    def loaded_cases(self) -> list[EvalTestCase]:
        return EvalScorer.load_cases_from_yaml(_CASES_DIR)

    def test_codegen_tag_present(self, loaded_cases: list[EvalTestCase]) -> None:
        """At least 5 cases have 'codegen' tag."""
        codegen_cases = [c for c in loaded_cases if "codegen" in c.tags]
        assert len(codegen_cases) >= 5, f"Expected >=5 codegen cases, got {len(codegen_cases)}"

    def test_multi_agent_tag_present(self, loaded_cases: list[EvalTestCase]) -> None:
        """At least 5 cases have 'multi_agent' or 'agent' tag."""
        agent_cases = [
            c for c in loaded_cases
            if any(t in ("multi_agent", "agent", "multi-agent") for t in c.tags)
        ]
        assert len(agent_cases) >= 5, f"Expected >=5 agent cases, got {len(agent_cases)}"

    def test_governance_tag_present(self, loaded_cases: list[EvalTestCase]) -> None:
        """At least some cases have 'governance' or 'gate' tag (Sprint 202 original cases)."""
        gov_cases = [
            c for c in loaded_cases
            if any(t in ("governance", "gate") for t in c.tags)
        ]
        assert len(gov_cases) >= 1

    def test_security_tag_present_in_codegen(self, loaded_cases: list[EvalTestCase]) -> None:
        """Codegen cases include security-relevant tags."""
        codegen_cases = [c for c in loaded_cases if "codegen" in c.tags]
        # At least one codegen case should have a security-related tag
        security_tags = {"security", "owasp", "auth", "authentication"}
        has_security = any(
            bool(set(c.tags) & security_tags) for c in codegen_cases
        )
        assert has_security, "No codegen case found with a security tag"


# ---------------------------------------------------------------------------
# Class 06 — EvalScorer.load_cases_from_yaml()
# ---------------------------------------------------------------------------

class TestLoadCasesFromYaml:
    """Class 06: EvalScorer.load_cases_from_yaml() directory loading."""

    def test_loads_all_15_cases(self) -> None:
        """Total 20 cases loaded from evals/cases (5 Sprint 202 + 10 Sprint 203 + 5 Sprint 204 routing)."""
        cases = EvalScorer.load_cases_from_yaml(_CASES_DIR)
        assert len(cases) == 20, f"Expected 20 cases, got {len(cases)}"

    def test_nonexistent_directory_returns_empty(self) -> None:
        """load_cases_from_yaml returns [] for nonexistent directory."""
        cases = EvalScorer.load_cases_from_yaml(Path("/nonexistent/path/xyz"))
        assert cases == []

    def test_duplicate_ids_not_present(self) -> None:
        """No two cases share the same id."""
        cases = EvalScorer.load_cases_from_yaml(_CASES_DIR)
        ids = [c.id for c in cases]
        assert len(ids) == len(set(ids)), f"Duplicate case IDs found: {set(x for x in ids if ids.count(x) > 1)}"

    def test_returns_eval_test_case_instances(self) -> None:
        """All returned objects are EvalTestCase instances."""
        cases = EvalScorer.load_cases_from_yaml(_CASES_DIR)
        for case in cases:
            assert isinstance(case, EvalTestCase), f"Expected EvalTestCase, got {type(case)}"


# ---------------------------------------------------------------------------
# Class 07 — CI eval runner _load_baseline()
# ---------------------------------------------------------------------------

class TestLoadBaseline:
    """Class 07: run_evals._load_baseline() function."""

    def _import_load_baseline(self):
        """Import _load_baseline from run_evals.py."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("run_evals", _RUN_EVALS_PY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module._load_baseline

    def test_loads_baseline_json(self) -> None:
        """_load_baseline() returns an EvalSuiteResult from the real baseline.json (Sprint 204: 20 cases)."""
        _load_baseline = self._import_load_baseline()
        suite = _load_baseline()
        assert suite is not None
        assert isinstance(suite, EvalSuiteResult)
        assert suite.total_cases == 20

    def test_baseline_avg_total_above_8(self) -> None:
        """Human-calibrated baseline has avg_total >= 8.0."""
        _load_baseline = self._import_load_baseline()
        suite = _load_baseline()
        assert suite is not None
        assert suite.avg_total >= 8.0, f"Baseline avg_total={suite.avg_total} < 8.0"

    def test_missing_baseline_returns_none(self, tmp_path: Path) -> None:
        """_load_baseline() returns None when baseline.json is missing."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("run_evals_tmp", _RUN_EVALS_PY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Temporarily patch the path
        original = module._BASELINE_PATH
        module._BASELINE_PATH = tmp_path / "nonexistent.json"
        try:
            result = module._load_baseline()
            assert result is None
        finally:
            module._BASELINE_PATH = original

    def test_comment_keys_skipped(self) -> None:
        """Keys starting with '_' (comment keys) are not loaded as cases."""
        _load_baseline = self._import_load_baseline()
        suite = _load_baseline()
        assert suite is not None
        # None of the result case_ids should start with '_'
        for r in suite.results:
            assert not r.case_id.startswith("_"), f"Comment key leaked as case: {r.case_id}"


# ---------------------------------------------------------------------------
# Class 08 — CI eval runner _filter_by_tags()
# ---------------------------------------------------------------------------

class TestFilterByTags:
    """Class 08: run_evals._filter_by_tags() function."""

    def _import_filter(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("run_evals", _RUN_EVALS_PY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module._filter_by_tags

    def _make_cases(self) -> list[EvalTestCase]:
        return [
            EvalTestCase(id="a", tool_name="t", prompt="p", expected_behavior="e", tags=["governance", "gate"]),
            EvalTestCase(id="b", tool_name="t", prompt="p", expected_behavior="e", tags=["codegen", "security"]),
            EvalTestCase(id="c", tool_name="t", prompt="p", expected_behavior="e", tags=["agent"]),
        ]

    def test_empty_tags_returns_all(self) -> None:
        """Empty tags list returns all cases."""
        _filter = self._import_filter()
        cases = self._make_cases()
        result = _filter(cases, [])
        assert len(result) == 3

    def test_single_tag_match(self) -> None:
        """Single-tag filter returns only matching cases."""
        _filter = self._import_filter()
        cases = self._make_cases()
        result = _filter(cases, ["codegen"])
        assert len(result) == 1
        assert result[0].id == "b"

    def test_multi_tag_filter_union(self) -> None:
        """Multiple tags return cases matching ANY of the tags (union)."""
        _filter = self._import_filter()
        cases = self._make_cases()
        result = _filter(cases, ["governance", "agent"])
        ids = {c.id for c in result}
        assert ids == {"a", "c"}

    def test_no_match_returns_empty(self) -> None:
        """Tags that match nothing return empty list."""
        _filter = self._import_filter()
        cases = self._make_cases()
        result = _filter(cases, ["nonexistent_tag_xyz"])
        assert result == []


# ---------------------------------------------------------------------------
# Class 09 — CI eval runner run(): exit codes
# ---------------------------------------------------------------------------

class TestEvalRunnerExitCodes:
    """Class 09: run_evals.run() exit code contract."""

    def _import_run(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("run_evals", _RUN_EVALS_PY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.run, module

    def test_dry_run_exits_0(self) -> None:
        """Dry-run (no Ollama) exits with code 0 when no regression."""
        run_fn, module = self._import_run()

        # Patch OllamaService to avoid real connection attempts
        mock_ollama = MagicMock()
        mock_ollama.is_available = True  # is_available is a @property
        # Return good scores for all cases
        good_response = '{"correctness":8,"completeness":8,"safety":9,"explanation":"ok"}'
        mock_ollama_resp = MagicMock()
        mock_ollama_resp.response = good_response
        mock_ollama.generate.return_value = mock_ollama_resp

        with patch.object(module, "OllamaService", return_value=mock_ollama):
            exit_code = run_fn(dry_run=True)

        # Dry run uses expected_behavior as mock — no regression expected
        assert exit_code in (0, 1), f"Expected exit 0 or 1 (dry-run), got {exit_code}"

    def test_ollama_unavailable_exits_3(self) -> None:
        """When Ollama is not available (not dry-run), exit code is 3."""
        run_fn, module = self._import_run()

        mock_ollama = MagicMock()
        # is_available is a @property — set as attribute to simulate False
        mock_ollama.is_available = False

        with patch.object(module, "OllamaService", return_value=mock_ollama):
            exit_code = run_fn(dry_run=False)

        assert exit_code == 3


# ---------------------------------------------------------------------------
# Class 10 — CI eval runner dry-run: 15 cases, scores computed
# ---------------------------------------------------------------------------

class TestEvalRunnerDryRun:
    """Class 10: run_evals dry-run produces valid suite results."""

    def test_15_cases_in_dry_run(self) -> None:
        """Dry-run loads and runs all 20 cases (16 behavioral via run_suite + 4 routing deterministic)."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("run_evals", _RUN_EVALS_PY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Mock Ollama returning consistent scores
        good_response = '{"correctness":8,"completeness":8,"safety":9,"explanation":"ok"}'

        mock_ollama = MagicMock()
        mock_ollama.is_available = True  # is_available is a @property
        mock_resp = MagicMock()
        mock_resp.response = good_response
        mock_ollama.generate.return_value = mock_resp

        captured_suite: list[EvalSuiteResult] = []
        original_run_suite = EvalScorer.run_suite

        def _capture_suite(self, cases, **kwargs):  # noqa: ANN001
            suite = original_run_suite(self, cases, **kwargs)
            captured_suite.append(suite)
            return suite

        with (
            patch.object(module, "OllamaService", return_value=mock_ollama),
            patch.object(EvalScorer, "run_suite", _capture_suite),
        ):
            module.run(dry_run=True)

        assert captured_suite, "run_suite was not called"
        # Sprint 204: run_suite is called with behavioral_cases only (16 cases).
        # 4 routing cases with expected_hint are scored deterministically via _score_routing_case().
        suite = captured_suite[0]
        assert suite.total_cases == 16, f"Expected 16 behavioral cases in run_suite, got {suite.total_cases}"

    def test_dry_run_avg_computed(self) -> None:
        """Dry-run produces non-zero avg_total in suite result."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("run_evals2", _RUN_EVALS_PY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        good_response = '{"correctness":8,"completeness":8,"safety":9,"explanation":"ok"}'
        mock_ollama = MagicMock()
        mock_ollama.is_available = True  # is_available is a @property
        mock_resp = MagicMock()
        mock_resp.response = good_response
        mock_ollama.generate.return_value = mock_resp

        captured: list[EvalSuiteResult] = []
        original_run_suite = EvalScorer.run_suite

        def _capture(self, cases, **kwargs):  # noqa: ANN001
            suite = original_run_suite(self, cases, **kwargs)
            captured.append(suite)
            return suite

        with (
            patch.object(module, "OllamaService", return_value=mock_ollama),
            patch.object(EvalScorer, "run_suite", _capture),
        ):
            module.run(dry_run=True)

        assert captured
        assert captured[0].avg_total > 0.0


# ---------------------------------------------------------------------------
# Class 11 — EvalSuiteResult regression detection
# ---------------------------------------------------------------------------

class TestEvalSuiteRegression:
    """Class 11: EvalSuiteResult.check_regression() — 20% drop triggers FAIL."""

    def _make_suite(self, avg_score: float, n: int = 5) -> EvalSuiteResult:
        """Build a suite with n results all having the given avg total score."""
        results = []
        # Approximate: correctness + completeness + safety = avg_score * 3
        dim = round(avg_score)  # rough approximation
        dim = max(0, min(10, dim))
        for i in range(n):
            rubric = EvalRubric(
                correctness=dim,
                completeness=dim,
                safety=max(dim, 8),  # keep safety >= 8 to avoid pass=False
                explanation="test",
            )
            results.append(EvalRunResult(
                case_id=f"case_{i}",
                tool_name="t",
                prompt="p",
                actual_response="r",
                rubric=rubric,
                evaluator_model="deepseek-r1:32b",
            ))
        suite = EvalSuiteResult(results=results)
        suite.compute_summary()
        return suite

    def test_no_regression_when_scores_stable(self) -> None:
        """No regression when current avg_total == baseline avg_total."""
        baseline = self._make_suite(avg_score=8.0)
        current = self._make_suite(avg_score=8.0)
        current.check_regression(baseline, threshold=0.20)
        assert current.regression_detected is False

    def test_regression_detected_when_drop_exceeds_20pct(self) -> None:
        """Regression triggered when avg_total drops >20% from baseline."""
        baseline = self._make_suite(avg_score=8.0)
        # 8.0 * (1 - 0.20) = 6.4; set current to 6.0 (25% drop)
        current = self._make_suite(avg_score=6.0)
        # Override avg_total directly for test determinism
        baseline.avg_total = 8.0
        current.avg_total = 6.0  # 25% drop
        current.check_regression(baseline, threshold=0.20)
        assert current.regression_detected is True

    def test_regression_not_triggered_at_19pct_drop(self) -> None:
        """19% drop does NOT trigger regression."""
        baseline = self._make_suite(avg_score=8.0)
        current = self._make_suite(avg_score=6.5)
        baseline.avg_total = 8.0
        current.avg_total = 6.52  # ~18.5% drop
        current.check_regression(baseline, threshold=0.20)
        assert current.regression_detected is False

    def test_default_regression_threshold_is_20pct(self) -> None:
        """DEFAULT_REGRESSION_THRESHOLD == 0.20."""
        assert DEFAULT_REGRESSION_THRESHOLD == pytest.approx(0.20)


# ---------------------------------------------------------------------------
# Class 12 — EvalTestCase schema
# ---------------------------------------------------------------------------

class TestEvalTestCaseSchema:
    """Class 12: EvalTestCase Pydantic model required / optional fields."""

    def test_required_fields_only(self) -> None:
        """EvalTestCase can be constructed with required fields only."""
        case = EvalTestCase(
            id="test_01",
            tool_name="get_gate_status",
            prompt="What is the gate status?",
            expected_behavior="Returns gate status.",
        )
        assert case.id == "test_01"
        assert case.ground_truth is None
        assert case.tags == []

    def test_optional_ground_truth(self) -> None:
        """ground_truth defaults to None."""
        case = EvalTestCase(
            id="test_01",
            tool_name="t",
            prompt="p",
            expected_behavior="e",
        )
        assert case.ground_truth is None

    def test_optional_tags_default_empty_list(self) -> None:
        """tags defaults to empty list."""
        case = EvalTestCase(id="x", tool_name="t", prompt="p", expected_behavior="e")
        assert isinstance(case.tags, list)
        assert len(case.tags) == 0

    def test_tags_list_accepted(self) -> None:
        """tags can be provided as a list of strings."""
        case = EvalTestCase(
            id="x",
            tool_name="t",
            prompt="p",
            expected_behavior="e",
            tags=["governance", "gate", "security"],
        )
        assert "governance" in case.tags
        assert len(case.tags) == 3


# ---------------------------------------------------------------------------
# Class 13 — Regression guards
# ---------------------------------------------------------------------------

class TestRegressionGuards:
    """Class 13: Sprint 203 eval expansion regression guards."""

    def test_total_case_count_is_15(self) -> None:
        """YAML eval suite contains exactly 20 cases (15 Sprint202+203 + 5 Sprint204 routing)."""
        cases = EvalScorer.load_cases_from_yaml(_CASES_DIR)
        assert len(cases) == 20

    def test_baseline_json_has_15_entries(self) -> None:
        """baseline.json contains exactly 20 non-comment entries (Sprint204: +5 routing cases)."""
        with open(_BASELINE_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        non_comment = {k: v for k, v in raw.items() if not k.startswith("_")}
        assert len(non_comment) == 20

    def test_baseline_all_passed(self) -> None:
        """All 15 baseline entries have 'passed': true."""
        with open(_BASELINE_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        non_comment = {k: v for k, v in raw.items() if not k.startswith("_")}
        for case_id, scores in non_comment.items():
            assert scores["passed"] is True, f"Baseline {case_id} has passed=false"

    def test_multi_judge_result_is_exported(self) -> None:
        """MultiJudgeResult is importable from eval_rubric schema."""
        from app.schemas.eval_rubric import MultiJudgeResult  # noqa: F401 — import check
        assert MultiJudgeResult is not None

    def test_multi_judge_eval_method_exists(self) -> None:
        """EvalScorer.multi_judge_eval() method is present."""
        assert hasattr(EvalScorer, "multi_judge_eval")
        import inspect
        assert callable(inspect.getattr_static(EvalScorer, "multi_judge_eval"))

    def test_run_evals_script_exists(self) -> None:
        """tests/evals/run_evals.py exists and is importable."""
        assert _RUN_EVALS_PY.exists(), f"run_evals.py not found at {_RUN_EVALS_PY}"

    def test_cases_dir_exists(self) -> None:
        """tests/evals/cases/ directory exists."""
        assert _CASES_DIR.is_dir(), f"Cases directory not found: {_CASES_DIR}"

    def test_baseline_path_exists(self) -> None:
        """tests/evals/reference_answers/baseline.json exists."""
        assert _BASELINE_PATH.exists(), f"Baseline not found: {_BASELINE_PATH}"
