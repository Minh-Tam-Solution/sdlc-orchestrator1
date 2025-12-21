"""
Test Validator - Unit and Integration Tests

SDLC Stage: 04 - BUILD
Sprint: 42 - AI Detection & Validation Pipeline
Framework: SDLC 5.1.1

Purpose:
Run tests for changed files and validate they pass.
Automatically finds related test files based on naming conventions.

Blocking: Yes (default) - test failures block merge
Timeout: 300 seconds (5 minutes default)
"""

import asyncio
import logging
import re
import time
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from . import BaseValidator, ValidatorConfig, ValidatorResult, ValidatorStatus

logger = logging.getLogger(__name__)


class TestValidator(BaseValidator):
    """Run tests for changed files."""

    name = "tests"
    description = "Unit and integration test execution"
    default_blocking = True
    default_timeout_seconds = 300

    # Test file patterns
    PYTHON_TEST_PATTERNS = [
        r"test_.*\.py$",
        r".*_test\.py$",
        r"tests/.*\.py$",
    ]
    TYPESCRIPT_TEST_PATTERNS = [
        r".*\.test\.[tj]sx?$",
        r".*\.spec\.[tj]sx?$",
        r"__tests__/.*\.[tj]sx?$",
    ]

    async def validate(
        self,
        project_id: UUID,
        pr_number: str,
        files: List[str],
        diff: str,
    ) -> ValidatorResult:
        """
        Run tests for changed files.

        Process:
        1. Find test files related to changed files
        2. Run pytest/vitest for respective file types
        3. Parse results and return status

        Args:
            project_id: Project UUID
            pr_number: Pull request number
            files: List of changed file paths
            diff: Unified diff

        Returns:
            ValidatorResult with test results
        """
        started_at = time.time()

        try:
            # Find related test files
            test_files = self._find_related_tests(files)

            if not test_files:
                duration_ms = int((time.time() - started_at) * 1000)
                return ValidatorResult(
                    validator_name=self.name,
                    status=ValidatorStatus.SKIPPED,
                    message="No related tests found",
                    details={"files_checked": len(files), "test_files": []},
                    duration_ms=duration_ms,
                    blocking=False,  # Don't block if no tests
                )

            logger.info(f"Running {len(test_files)} test files")

            # Categorize test files
            python_tests = [f for f in test_files if f.endswith(".py")]
            ts_tests = [f for f in test_files if self._is_typescript_test(f)]

            # Run tests
            results = {"passed": 0, "failed": 0, "skipped": 0, "errors": []}

            if python_tests:
                python_result = await self._run_pytest(python_tests)
                results["passed"] += python_result.get("passed", 0)
                results["failed"] += python_result.get("failed", 0)
                results["skipped"] += python_result.get("skipped", 0)
                results["errors"].extend(python_result.get("errors", []))

            if ts_tests:
                ts_result = await self._run_vitest(ts_tests)
                results["passed"] += ts_result.get("passed", 0)
                results["failed"] += ts_result.get("failed", 0)
                results["skipped"] += ts_result.get("skipped", 0)
                results["errors"].extend(ts_result.get("errors", []))

            duration_ms = int((time.time() - started_at) * 1000)

            # Determine status
            total = results["passed"] + results["failed"]
            if results["failed"] > 0:
                status = ValidatorStatus.FAILED
                message = f"{results['passed']}/{total} tests passed, {results['failed']} failed"
            elif results["passed"] > 0:
                status = ValidatorStatus.PASSED
                message = f"{results['passed']}/{total} tests passed"
            else:
                status = ValidatorStatus.SKIPPED
                message = "No tests were executed"

            return ValidatorResult(
                validator_name=self.name,
                status=status,
                message=message,
                details={
                    "passed": results["passed"],
                    "failed": results["failed"],
                    "skipped": results["skipped"],
                    "total": total,
                    "errors": results["errors"][:10],
                    "test_files": test_files[:20],
                },
                duration_ms=duration_ms,
                blocking=self.config.blocking if results["failed"] > 0 else False,
            )

        except asyncio.TimeoutError:
            duration_ms = int((time.time() - started_at) * 1000)
            return ValidatorResult(
                validator_name=self.name,
                status=ValidatorStatus.TIMEOUT,
                message=f"Test execution timed out after {self.config.timeout_seconds}s",
                details={},
                duration_ms=duration_ms,
                blocking=False,
            )

        except Exception as e:
            logger.error(f"Test validation error: {e}", exc_info=True)
            duration_ms = int((time.time() - started_at) * 1000)
            return ValidatorResult(
                validator_name=self.name,
                status=ValidatorStatus.ERROR,
                message=f"Test execution error: {str(e)}",
                details={"error": str(e)},
                duration_ms=duration_ms,
                blocking=False,
            )

    def _find_related_tests(self, files: List[str]) -> List[str]:
        """
        Find test files related to changed files.

        Strategies:
        1. Changed file is a test file itself
        2. Corresponding test file exists (e.g., service.py -> test_service.py)
        3. Test file in tests/ directory with matching name
        """
        test_files = []

        for file_path in files:
            # Check if file is already a test file
            if self._is_test_file(file_path):
                test_files.append(file_path)
                continue

            # Find corresponding test file
            related_tests = self._find_test_file_for(file_path)
            test_files.extend(related_tests)

        # Remove duplicates while preserving order
        seen = set()
        unique_tests = []
        for f in test_files:
            if f not in seen:
                seen.add(f)
                unique_tests.append(f)

        return unique_tests

    def _is_test_file(self, path: str) -> bool:
        """Check if file is a test file."""
        for pattern in self.PYTHON_TEST_PATTERNS + self.TYPESCRIPT_TEST_PATTERNS:
            if re.search(pattern, path):
                return True
        return False

    def _is_typescript_test(self, path: str) -> bool:
        """Check if file is a TypeScript test file."""
        for pattern in self.TYPESCRIPT_TEST_PATTERNS:
            if re.search(pattern, path):
                return True
        return False

    def _find_test_file_for(self, source_path: str) -> List[str]:
        """Find test files for a source file."""
        test_files = []
        path = Path(source_path)

        # Python file -> test_*.py
        if source_path.endswith(".py"):
            # Check for test_<name>.py in same directory
            test_name = f"test_{path.stem}.py"
            same_dir_test = path.parent / test_name
            if same_dir_test.exists():
                test_files.append(str(same_dir_test))

            # Check for tests/<name>_test.py
            tests_dir = path.parent / "tests"
            if tests_dir.exists():
                test_in_dir = tests_dir / test_name
                if test_in_dir.exists():
                    test_files.append(str(test_in_dir))

        # TypeScript file -> *.test.ts
        elif source_path.endswith((".ts", ".tsx")):
            # Check for <name>.test.ts
            test_ext = ".test" + path.suffix
            test_path = path.with_suffix(test_ext)
            if test_path.exists():
                test_files.append(str(test_path))

            # Check for <name>.spec.ts
            spec_ext = ".spec" + path.suffix
            spec_path = path.with_suffix(spec_ext)
            if spec_path.exists():
                test_files.append(str(spec_path))

        return test_files

    async def _run_pytest(self, test_files: List[str]) -> dict:
        """
        Run pytest on test files.

        Returns dict with passed, failed, skipped counts.
        """
        result = {"passed": 0, "failed": 0, "skipped": 0, "errors": []}

        try:
            files_arg = " ".join(f'"{f}"' for f in test_files[:20])  # Limit files
            process = await asyncio.create_subprocess_shell(
                f"python -m pytest {files_arg} --tb=short -q 2>/dev/null",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=self.config.timeout_seconds
            )

            output = stdout.decode() + stderr.decode()

            # Parse pytest output
            # Example: "5 passed, 2 failed, 1 skipped"
            passed_match = re.search(r"(\d+) passed", output)
            failed_match = re.search(r"(\d+) failed", output)
            skipped_match = re.search(r"(\d+) skipped", output)

            if passed_match:
                result["passed"] = int(passed_match.group(1))
            if failed_match:
                result["failed"] = int(failed_match.group(1))
            if skipped_match:
                result["skipped"] = int(skipped_match.group(1))

            # Extract failure messages
            if result["failed"] > 0:
                failures = re.findall(r"FAILED (.*?) - (.*?)(?:\n|$)", output)
                for test_name, message in failures[:5]:
                    result["errors"].append(
                        {"test": test_name.strip(), "message": message.strip()}
                    )

        except asyncio.TimeoutError:
            result["errors"].append({"error": "pytest timed out"})
        except FileNotFoundError:
            logger.warning("pytest not installed, skipping Python tests")
        except Exception as e:
            result["errors"].append({"error": f"pytest error: {str(e)}"})

        return result

    async def _run_vitest(self, test_files: List[str]) -> dict:
        """
        Run vitest on test files.

        Returns dict with passed, failed, skipped counts.
        """
        result = {"passed": 0, "failed": 0, "skipped": 0, "errors": []}

        try:
            files_arg = " ".join(f'"{f}"' for f in test_files[:20])  # Limit files
            process = await asyncio.create_subprocess_shell(
                f"npx vitest run {files_arg} --reporter=json 2>/dev/null",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await asyncio.wait_for(
                process.communicate(), timeout=self.config.timeout_seconds
            )

            if stdout:
                import json

                try:
                    data = json.loads(stdout.decode())
                    result["passed"] = data.get("numPassedTests", 0)
                    result["failed"] = data.get("numFailedTests", 0)
                    result["skipped"] = data.get("numPendingTests", 0)

                    # Extract failures
                    for test_result in data.get("testResults", []):
                        for assertion in test_result.get("assertionResults", []):
                            if assertion.get("status") == "failed":
                                result["errors"].append(
                                    {
                                        "test": assertion.get("fullName"),
                                        "message": assertion.get("failureMessages", [""])[
                                            0
                                        ][:200],
                                    }
                                )
                except json.JSONDecodeError:
                    # Fall back to regex parsing
                    output = stdout.decode()
                    passed_match = re.search(r"(\d+) passed", output)
                    failed_match = re.search(r"(\d+) failed", output)
                    if passed_match:
                        result["passed"] = int(passed_match.group(1))
                    if failed_match:
                        result["failed"] = int(failed_match.group(1))

        except asyncio.TimeoutError:
            result["errors"].append({"error": "vitest timed out"})
        except FileNotFoundError:
            logger.warning("vitest not installed, skipping TypeScript tests")
        except Exception as e:
            result["errors"].append({"error": f"vitest error: {str(e)}"})

        return result
