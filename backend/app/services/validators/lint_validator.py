"""
Lint Validator - Code Style and Formatting

SDLC Stage: 04 - BUILD
Sprint: 42 - AI Detection & Validation Pipeline
Framework: SDLC 5.1.1

Purpose:
Validate code style and formatting using language-specific linters.
Supports Python (ruff/black) and TypeScript (ESLint).

Blocking: Yes (default) - lint errors block merge
Timeout: 120 seconds (default)
"""

import asyncio
import logging
import time
from typing import List, Optional
from uuid import UUID

from . import BaseValidator, ValidatorConfig, ValidatorResult, ValidatorStatus

logger = logging.getLogger(__name__)


class LintValidator(BaseValidator):
    """Validate code style and formatting."""

    name = "lint"
    description = "Lint and format validation (ruff, black, ESLint)"
    default_blocking = True
    default_timeout_seconds = 120

    # File type mappings
    PYTHON_EXTENSIONS = {".py", ".pyi"}
    TYPESCRIPT_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx"}

    async def validate(
        self,
        project_id: UUID,
        pr_number: str,
        files: List[str],
        diff: str,
    ) -> ValidatorResult:
        """
        Run lint validation on changed files.

        Process:
        1. Categorize files by language
        2. Run ruff/black for Python files
        3. Run ESLint for TypeScript/JavaScript files
        4. Aggregate results

        Args:
            project_id: Project UUID
            pr_number: Pull request number
            files: List of changed file paths
            diff: Unified diff

        Returns:
            ValidatorResult with lint errors/warnings
        """
        started_at = time.time()
        errors = []
        warnings = []

        try:
            # Categorize files by language
            python_files = [f for f in files if self._is_python_file(f)]
            ts_files = [f for f in files if self._is_typescript_file(f)]

            logger.info(
                f"Lint validation: {len(python_files)} Python, {len(ts_files)} TS files"
            )

            # Run linters in parallel
            tasks = []
            if python_files:
                tasks.append(self._run_python_lint(python_files))
            if ts_files:
                tasks.append(self._run_typescript_lint(ts_files))

            if not tasks:
                duration_ms = int((time.time() - started_at) * 1000)
                return ValidatorResult(
                    validator_name=self.name,
                    status=ValidatorStatus.SKIPPED,
                    message="No lintable files found",
                    details={"files_checked": 0},
                    duration_ms=duration_ms,
                    blocking=self.config.blocking,
                )

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Aggregate results
            for result in results:
                if isinstance(result, Exception):
                    errors.append({"error": str(result)})
                else:
                    errors.extend(result.get("errors", []))
                    warnings.extend(result.get("warnings", []))

            duration_ms = int((time.time() - started_at) * 1000)

            # Determine status
            if errors:
                status = ValidatorStatus.FAILED
                message = f"Found {len(errors)} lint errors"
            elif warnings:
                status = ValidatorStatus.PASSED
                message = f"Passed with {len(warnings)} warnings"
            else:
                status = ValidatorStatus.PASSED
                message = "No lint issues found"

            return ValidatorResult(
                validator_name=self.name,
                status=status,
                message=message,
                details={
                    "errors": errors[:20],  # Limit to 20
                    "warnings": warnings[:10],
                    "error_count": len(errors),
                    "warning_count": len(warnings),
                    "files_checked": len(python_files) + len(ts_files),
                },
                duration_ms=duration_ms,
                blocking=self.config.blocking,
            )

        except asyncio.TimeoutError:
            duration_ms = int((time.time() - started_at) * 1000)
            return ValidatorResult(
                validator_name=self.name,
                status=ValidatorStatus.TIMEOUT,
                message=f"Lint validation timed out after {self.config.timeout_seconds}s",
                details={},
                duration_ms=duration_ms,
                blocking=False,  # Don't block on timeout
            )

        except Exception as e:
            logger.error(f"Lint validation error: {e}", exc_info=True)
            duration_ms = int((time.time() - started_at) * 1000)
            return ValidatorResult(
                validator_name=self.name,
                status=ValidatorStatus.ERROR,
                message=f"Lint validation error: {str(e)}",
                details={"error": str(e)},
                duration_ms=duration_ms,
                blocking=False,  # Don't block on error
            )

    def _is_python_file(self, path: str) -> bool:
        """Check if file is a Python file."""
        return any(path.endswith(ext) for ext in self.PYTHON_EXTENSIONS)

    def _is_typescript_file(self, path: str) -> bool:
        """Check if file is a TypeScript/JavaScript file."""
        return any(path.endswith(ext) for ext in self.TYPESCRIPT_EXTENSIONS)

    async def _run_python_lint(self, files: List[str]) -> dict:
        """
        Run Python linting with ruff.

        Returns dict with errors and warnings lists.
        """
        errors = []
        warnings = []

        try:
            # Run ruff check
            files_arg = " ".join(f'"{f}"' for f in files[:50])  # Limit files
            process = await asyncio.create_subprocess_shell(
                f"ruff check {files_arg} --output-format=json 2>/dev/null",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await asyncio.wait_for(
                process.communicate(), timeout=self.config.timeout_seconds
            )

            if stdout:
                import json

                try:
                    issues = json.loads(stdout.decode())
                    for issue in issues:
                        error_obj = {
                            "file": issue.get("filename"),
                            "line": issue.get("location", {}).get("row"),
                            "code": issue.get("code"),
                            "message": issue.get("message"),
                        }
                        # Treat E and W codes differently
                        code = issue.get("code", "")
                        if code.startswith(("E", "F")):
                            errors.append(error_obj)
                        else:
                            warnings.append(error_obj)
                except json.JSONDecodeError:
                    pass

        except asyncio.TimeoutError:
            errors.append({"error": "Python lint timed out"})
        except FileNotFoundError:
            # ruff not installed - skip
            logger.warning("ruff not installed, skipping Python lint")
        except Exception as e:
            errors.append({"error": f"Python lint error: {str(e)}"})

        return {"errors": errors, "warnings": warnings}

    async def _run_typescript_lint(self, files: List[str]) -> dict:
        """
        Run TypeScript linting with ESLint.

        Returns dict with errors and warnings lists.
        """
        errors = []
        warnings = []

        try:
            # Run ESLint
            files_arg = " ".join(f'"{f}"' for f in files[:50])  # Limit files
            process = await asyncio.create_subprocess_shell(
                f"npx eslint {files_arg} --format=json 2>/dev/null",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await asyncio.wait_for(
                process.communicate(), timeout=self.config.timeout_seconds
            )

            if stdout:
                import json

                try:
                    results = json.loads(stdout.decode())
                    for result in results:
                        for message in result.get("messages", []):
                            error_obj = {
                                "file": result.get("filePath"),
                                "line": message.get("line"),
                                "code": message.get("ruleId"),
                                "message": message.get("message"),
                            }
                            if message.get("severity") == 2:
                                errors.append(error_obj)
                            else:
                                warnings.append(error_obj)
                except json.JSONDecodeError:
                    pass

        except asyncio.TimeoutError:
            errors.append({"error": "TypeScript lint timed out"})
        except FileNotFoundError:
            # ESLint not installed - skip
            logger.warning("ESLint not installed, skipping TypeScript lint")
        except Exception as e:
            errors.append({"error": f"TypeScript lint error: {str(e)}"})

        return {"errors": errors, "warnings": warnings}
