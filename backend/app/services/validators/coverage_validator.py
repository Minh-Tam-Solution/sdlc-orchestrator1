"""
Coverage Validator - Test Coverage Analysis

SDLC Stage: 04 - BUILD
Sprint: 42 - AI Detection & Validation Pipeline
Framework: SDLC 5.1.1

Purpose:
Validate test coverage meets configured thresholds.
Supports Python (pytest-cov) and TypeScript (vitest coverage).

Blocking: No (default) - coverage is advisory by default
Timeout: 300 seconds (5 minutes default)
"""

import asyncio
import json
import logging
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID

from . import BaseValidator, ValidatorConfig, ValidatorResult, ValidatorStatus

logger = logging.getLogger(__name__)


class CoverageValidator(BaseValidator):
    """Validate test coverage thresholds."""

    name = "coverage"
    description = "Test coverage validation"
    default_blocking = False  # Coverage is advisory by default
    default_timeout_seconds = 300

    # Default thresholds
    DEFAULT_COVERAGE_THRESHOLD = 80  # 80%

    async def validate(
        self,
        project_id: UUID,
        pr_number: str,
        files: List[str],
        diff: str,
    ) -> ValidatorResult:
        """
        Run coverage analysis on changed files.

        Process:
        1. Run tests with coverage enabled
        2. Parse coverage report
        3. Check against threshold
        4. Report per-file coverage for changed files

        Args:
            project_id: Project UUID
            pr_number: Pull request number
            files: List of changed file paths
            diff: Unified diff

        Returns:
            ValidatorResult with coverage metrics
        """
        started_at = time.time()

        try:
            # Get threshold from config or use default
            threshold = self.config.settings.get(
                "threshold", self.DEFAULT_COVERAGE_THRESHOLD
            )

            # Determine language from files
            python_files = [f for f in files if f.endswith(".py")]
            ts_files = [f for f in files if f.endswith((".ts", ".tsx"))]

            coverage_results = {
                "total_coverage": 0.0,
                "file_coverage": [],
                "threshold": threshold,
            }

            if python_files:
                python_coverage = await self._run_python_coverage()
                if python_coverage:
                    coverage_results["total_coverage"] = python_coverage.get(
                        "total", 0.0
                    )
                    # Filter to changed files
                    for file_cov in python_coverage.get("files", []):
                        if file_cov["file"] in python_files:
                            coverage_results["file_coverage"].append(file_cov)

            if ts_files:
                ts_coverage = await self._run_typescript_coverage()
                if ts_coverage:
                    # Combine with Python coverage
                    if coverage_results["total_coverage"] == 0:
                        coverage_results["total_coverage"] = ts_coverage.get(
                            "total", 0.0
                        )
                    # Filter to changed files
                    for file_cov in ts_coverage.get("files", []):
                        if file_cov["file"] in ts_files:
                            coverage_results["file_coverage"].append(file_cov)

            duration_ms = int((time.time() - started_at) * 1000)

            total_coverage = coverage_results["total_coverage"]

            # Determine status
            if total_coverage >= threshold:
                status = ValidatorStatus.PASSED
                message = f"Coverage: {total_coverage:.1f}% (threshold: {threshold}%)"
            elif total_coverage == 0:
                status = ValidatorStatus.SKIPPED
                message = "No coverage data available"
            else:
                status = ValidatorStatus.FAILED
                message = f"Coverage: {total_coverage:.1f}% below threshold {threshold}%"

            # Calculate changed files coverage
            changed_coverage = []
            for file_cov in coverage_results["file_coverage"]:
                changed_coverage.append(
                    {
                        "file": file_cov["file"],
                        "coverage": file_cov["coverage"],
                        "covered_lines": file_cov.get("covered_lines", 0),
                        "total_lines": file_cov.get("total_lines", 0),
                    }
                )

            return ValidatorResult(
                validator_name=self.name,
                status=status,
                message=message,
                details={
                    "total_coverage": round(total_coverage, 2),
                    "threshold": threshold,
                    "changed_files_coverage": changed_coverage,
                    "files_analyzed": len(files),
                    "below_threshold": total_coverage < threshold,
                },
                duration_ms=duration_ms,
                blocking=self.config.blocking if total_coverage < threshold else False,
            )

        except asyncio.TimeoutError:
            duration_ms = int((time.time() - started_at) * 1000)
            return ValidatorResult(
                validator_name=self.name,
                status=ValidatorStatus.TIMEOUT,
                message=f"Coverage analysis timed out after {self.config.timeout_seconds}s",
                details={},
                duration_ms=duration_ms,
                blocking=False,
            )

        except Exception as e:
            logger.error(f"Coverage validation error: {e}", exc_info=True)
            duration_ms = int((time.time() - started_at) * 1000)
            return ValidatorResult(
                validator_name=self.name,
                status=ValidatorStatus.ERROR,
                message=f"Coverage analysis error: {str(e)}",
                details={"error": str(e)},
                duration_ms=duration_ms,
                blocking=False,
            )

    async def _run_python_coverage(self) -> Optional[Dict[str, Any]]:
        """
        Run pytest with coverage.

        Returns dict with total coverage and per-file coverage.
        """
        try:
            process = await asyncio.create_subprocess_shell(
                "python -m pytest --cov=. --cov-report=json -q 2>/dev/null",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await asyncio.wait_for(
                process.communicate(), timeout=self.config.timeout_seconds
            )

            # Read coverage.json
            coverage_file = Path("coverage.json")
            if coverage_file.exists():
                data = json.loads(coverage_file.read_text())

                total = data.get("totals", {}).get("percent_covered", 0.0)
                files = []

                for file_path, file_data in data.get("files", {}).items():
                    summary = file_data.get("summary", {})
                    files.append(
                        {
                            "file": file_path,
                            "coverage": summary.get("percent_covered", 0.0),
                            "covered_lines": summary.get("covered_lines", 0),
                            "total_lines": summary.get("num_statements", 0),
                        }
                    )

                return {"total": total, "files": files}

        except asyncio.TimeoutError:
            logger.warning("Python coverage timed out")
        except FileNotFoundError:
            logger.warning("pytest-cov not installed, skipping Python coverage")
        except Exception as e:
            logger.error(f"Python coverage error: {e}")

        return None

    async def _run_typescript_coverage(self) -> Optional[Dict[str, Any]]:
        """
        Run vitest with coverage.

        Returns dict with total coverage and per-file coverage.
        """
        try:
            process = await asyncio.create_subprocess_shell(
                "npx vitest run --coverage --reporter=json 2>/dev/null",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await asyncio.wait_for(
                process.communicate(), timeout=self.config.timeout_seconds
            )

            # Parse vitest JSON output
            if stdout:
                try:
                    data = json.loads(stdout.decode())
                    coverage_summary = data.get("coverageMap", {})

                    total_lines = 0
                    covered_lines = 0
                    files = []

                    for file_path, file_data in coverage_summary.items():
                        line_map = file_data.get("lineMap", {})
                        file_total = len(line_map)
                        file_covered = sum(1 for v in line_map.values() if v > 0)

                        total_lines += file_total
                        covered_lines += file_covered

                        file_percent = (
                            (file_covered / file_total * 100) if file_total > 0 else 0
                        )
                        files.append(
                            {
                                "file": file_path,
                                "coverage": round(file_percent, 2),
                                "covered_lines": file_covered,
                                "total_lines": file_total,
                            }
                        )

                    total = (covered_lines / total_lines * 100) if total_lines > 0 else 0
                    return {"total": round(total, 2), "files": files}

                except json.JSONDecodeError:
                    pass

        except asyncio.TimeoutError:
            logger.warning("TypeScript coverage timed out")
        except FileNotFoundError:
            logger.warning("vitest not installed, skipping TypeScript coverage")
        except Exception as e:
            logger.error(f"TypeScript coverage error: {e}")

        return None
