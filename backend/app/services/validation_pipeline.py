"""
Validation Pipeline - Orchestrator for AI-Generated Code Validation

SDLC Stage: 04 - BUILD
Sprint: 42 - AI Detection & Validation Pipeline
Framework: SDLC 5.1.3
Epic: EP-02 AI Safety Layer v1

Purpose:
Orchestrate validation of AI-generated Pull Requests.
Runs multiple validators in parallel and aggregates results.

Architecture:
- Parallel validator execution (asyncio.gather)
- Configurable validator chain (Lint, Tests, Coverage, etc.)
- Policy-based blocking/non-blocking modes
- Redis queue integration for async processing
- Prometheus metrics for observability

Pipeline Flow:
1. AI PR Detected → ValidationPipeline.queue()
2. Background Worker → ValidationPipeline.run()
3. Validators execute in parallel
4. Results aggregated → PR comment posted
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.services.validators import (
    BaseValidator,
    PipelineResult,
    ValidationStatus,
    ValidatorConfig,
    ValidatorResult,
    ValidatorStatus,
)
from app.services.validators.coverage_validator import CoverageValidator
from app.services.validators.lint_validator import LintValidator
from app.services.validators.test_validator import TestValidator

logger = logging.getLogger(__name__)

# Import metrics (may fail in test environment)
try:
    from app.middleware.validation_metrics import (
        record_pipeline_result,
        record_validator_result,
    )

    METRICS_ENABLED = True
except ImportError:
    METRICS_ENABLED = False
    logger.warning("Validation metrics not available")


class ValidationPipeline:
    """
    Orchestrate validation of AI-generated Pull Requests.

    Runs multiple validators in parallel and aggregates results
    to determine if the PR can be merged.

    Validators:
    - LintValidator: Code style compliance (blocking)
    - TestValidator: Test execution (blocking)
    - CoverageValidator: Coverage thresholds (non-blocking by default)

    Usage:
        pipeline = ValidationPipeline()
        result = await pipeline.run(event_id, project_id, pr_number, files, diff)
    """

    def __init__(self, validators: Optional[List[BaseValidator]] = None):
        """
        Initialize pipeline with validators.

        Args:
            validators: List of validators to run. Uses defaults if None.
        """
        if validators is None:
            # Default validators
            self.validators = [
                LintValidator(),
                TestValidator(),
                CoverageValidator(),
            ]
        else:
            self.validators = validators

    async def run(
        self,
        event_id: UUID,
        project_id: UUID,
        pr_number: str,
        files: List[str],
        diff: str,
    ) -> PipelineResult:
        """
        Run all validators on PR files.

        Process:
        1. Record start time
        2. Run all validators in parallel
        3. Handle exceptions from individual validators
        4. Aggregate results
        5. Determine overall status (PASSED if no blocking failures)
        6. Record metrics

        Args:
            event_id: AI code event UUID
            project_id: Project UUID
            pr_number: Pull request number
            files: List of changed file paths
            diff: Unified diff of all changes

        Returns:
            PipelineResult with all validator results

        Performance:
        - Target: <6 minutes p95 (all validators combined)
        - Parallel execution minimizes total time
        """
        started_at = datetime.utcnow()
        start_time = time.time()

        logger.info(
            f"Starting validation pipeline for event {event_id}",
            extra={
                "event_id": str(event_id),
                "project_id": str(project_id),
                "pr_number": pr_number,
                "file_count": len(files),
            },
        )

        try:
            # Run all validators in parallel
            tasks = [
                self._run_validator_safe(v, project_id, pr_number, files, diff)
                for v in self.validators
            ]
            results = await asyncio.gather(*tasks)

            # Aggregate results
            processed_results = []
            blocking_failures = []
            validators_passed = 0
            validators_failed = 0

            for result in results:
                processed_results.append(result)

                # Record per-validator metrics
                if METRICS_ENABLED:
                    record_validator_result(
                        validator_name=result.validator_name,
                        status=result.status.value,
                        duration_seconds=result.duration_ms / 1000,
                    )

                # Count results
                if result.status == ValidatorStatus.PASSED:
                    validators_passed += 1
                elif result.status in (ValidatorStatus.FAILED, ValidatorStatus.ERROR):
                    validators_failed += 1
                    if result.blocking:
                        blocking_failures.append(result)

            # Determine overall status
            if blocking_failures:
                overall_status = ValidationStatus.FAILED
            elif validators_failed > 0:
                overall_status = ValidationStatus.PASSED  # Non-blocking failures
            else:
                overall_status = ValidationStatus.PASSED

            duration_ms = int((time.time() - start_time) * 1000)
            completed_at = datetime.utcnow()

            pipeline_result = PipelineResult(
                event_id=event_id,
                status=overall_status,
                results=processed_results,
                blocking_failures=blocking_failures,
                duration_ms=duration_ms,
                started_at=started_at,
                completed_at=completed_at,
                validators_run=len(self.validators),
                validators_passed=validators_passed,
                validators_failed=validators_failed,
            )

            # Record pipeline metrics
            if METRICS_ENABLED:
                record_pipeline_result(
                    status=overall_status.value,
                    duration_seconds=duration_ms / 1000,
                    validators_run=len(self.validators),
                    blocking_failures=len(blocking_failures),
                )

            logger.info(
                f"Validation pipeline completed: {overall_status.value}",
                extra={
                    "event_id": str(event_id),
                    "status": overall_status.value,
                    "duration_ms": duration_ms,
                    "validators_passed": validators_passed,
                    "validators_failed": validators_failed,
                    "blocking_failures": len(blocking_failures),
                },
            )

            return pipeline_result

        except Exception as e:
            logger.error(f"Validation pipeline error: {e}", exc_info=True)

            duration_ms = int((time.time() - start_time) * 1000)

            return PipelineResult(
                event_id=event_id,
                status=ValidationStatus.ERROR,
                results=[],
                blocking_failures=[],
                duration_ms=duration_ms,
                started_at=started_at,
                completed_at=datetime.utcnow(),
            )

    async def _run_validator_safe(
        self,
        validator: BaseValidator,
        project_id: UUID,
        pr_number: str,
        files: List[str],
        diff: str,
    ) -> ValidatorResult:
        """
        Run a single validator with error handling and timeout.

        Args:
            validator: Validator to run
            project_id: Project UUID
            pr_number: Pull request number
            files: Changed files
            diff: Unified diff

        Returns:
            ValidatorResult (or error result if exception)
        """
        start_time = time.time()

        try:
            # Apply timeout
            result = await asyncio.wait_for(
                validator.validate(project_id, pr_number, files, diff),
                timeout=validator.get_timeout(),
            )

            # Ensure timestamps are set
            if result.started_at is None:
                result.started_at = datetime.utcnow()
            if result.completed_at is None:
                result.completed_at = datetime.utcnow()

            return result

        except asyncio.TimeoutError:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.warning(
                f"Validator {validator.get_name()} timed out after {validator.get_timeout()}s"
            )
            return ValidatorResult(
                validator_name=validator.get_name(),
                status=ValidatorStatus.TIMEOUT,
                message=f"Timed out after {validator.get_timeout()}s",
                details={},
                duration_ms=duration_ms,
                blocking=False,  # Don't block on timeout
                started_at=datetime.utcnow(),
                completed_at=datetime.utcnow(),
            )

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error(
                f"Validator {validator.get_name()} error: {e}",
                exc_info=True,
            )
            return ValidatorResult(
                validator_name=validator.get_name(),
                status=ValidatorStatus.ERROR,
                message=f"Error: {str(e)}",
                details={"error": str(e), "error_type": type(e).__name__},
                duration_ms=duration_ms,
                blocking=False,  # Don't block on error
                started_at=datetime.utcnow(),
                completed_at=datetime.utcnow(),
            )

    def add_validator(self, validator: BaseValidator) -> None:
        """Add a validator to the pipeline."""
        self.validators.append(validator)

    def remove_validator(self, name: str) -> bool:
        """Remove a validator by name."""
        for i, v in enumerate(self.validators):
            if v.get_name() == name:
                self.validators.pop(i)
                return True
        return False

    def get_validators(self) -> List[str]:
        """Get list of validator names."""
        return [v.get_name() for v in self.validators]


# Singleton instance
validation_pipeline = ValidationPipeline()
