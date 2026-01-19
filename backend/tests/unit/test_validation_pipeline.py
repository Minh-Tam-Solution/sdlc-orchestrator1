"""
Unit Tests - Validation Pipeline

SDLC Stage: 04 - BUILD
Sprint: 42 - AI Detection & Validation Pipeline
Framework: SDLC 5.1.3

Purpose:
Unit tests for ValidationPipeline covering:
1. Pipeline execution with multiple validators
2. Parallel validator execution
3. Blocking/non-blocking failure handling
4. Result aggregation
5. Error handling and timeouts

Coverage Target: 95%+
"""

import asyncio
from datetime import datetime
from uuid import uuid4

import pytest

from app.services.validators import (
    BaseValidator,
    PipelineResult,
    ValidationStatus,
    ValidatorConfig,
    ValidatorResult,
    ValidatorStatus,
)
from app.services.validation_pipeline import ValidationPipeline


# ============================================================================
# Mock Validators for Testing
# ============================================================================


class MockPassingValidator(BaseValidator):
    """Mock validator that always passes."""

    name = "mock_pass"
    description = "Always passes"
    default_blocking = True

    async def validate(self, project_id, pr_number, files, diff):
        return ValidatorResult(
            validator_name=self.name,
            status=ValidatorStatus.PASSED,
            message="Mock passed",
            details={"mock": True},
            duration_ms=10,
            blocking=self.config.blocking,
        )


class MockFailingValidator(BaseValidator):
    """Mock validator that always fails."""

    name = "mock_fail"
    description = "Always fails"
    default_blocking = True

    async def validate(self, project_id, pr_number, files, diff):
        return ValidatorResult(
            validator_name=self.name,
            status=ValidatorStatus.FAILED,
            message="Mock failed",
            details={"mock": True},
            duration_ms=10,
            blocking=self.config.blocking,
        )


class MockNonBlockingFailValidator(BaseValidator):
    """Mock validator that fails but doesn't block."""

    name = "mock_nonblocking"
    description = "Fails without blocking"
    default_blocking = False

    async def validate(self, project_id, pr_number, files, diff):
        return ValidatorResult(
            validator_name=self.name,
            status=ValidatorStatus.FAILED,
            message="Non-blocking failure",
            details={},
            duration_ms=10,
            blocking=False,
        )


class MockSlowValidator(BaseValidator):
    """Mock validator that takes time."""

    name = "mock_slow"
    description = "Slow validator"
    default_blocking = True
    default_timeout_seconds = 1

    def __init__(self, delay: float = 0.5):
        super().__init__()
        self.delay = delay

    async def validate(self, project_id, pr_number, files, diff):
        await asyncio.sleep(self.delay)
        return ValidatorResult(
            validator_name=self.name,
            status=ValidatorStatus.PASSED,
            message="Slow passed",
            details={},
            duration_ms=int(self.delay * 1000),
            blocking=self.config.blocking,
        )


class MockTimeoutValidator(BaseValidator):
    """Mock validator that times out."""

    name = "mock_timeout"
    description = "Always times out"
    default_blocking = True
    default_timeout_seconds = 1

    async def validate(self, project_id, pr_number, files, diff):
        await asyncio.sleep(10)  # Will timeout
        return ValidatorResult(
            validator_name=self.name,
            status=ValidatorStatus.PASSED,
            message="Should not reach",
            details={},
            duration_ms=0,
            blocking=True,
        )


class MockErrorValidator(BaseValidator):
    """Mock validator that raises an error."""

    name = "mock_error"
    description = "Always errors"

    async def validate(self, project_id, pr_number, files, diff):
        raise ValueError("Mock error")


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def project_id():
    return uuid4()


@pytest.fixture
def event_id():
    return uuid4()


# ============================================================================
# Test Pipeline Execution
# ============================================================================


@pytest.mark.asyncio
async def test_pipeline_all_pass(project_id, event_id):
    """Test pipeline with all passing validators."""
    pipeline = ValidationPipeline(
        validators=[MockPassingValidator(), MockPassingValidator()]
    )

    result = await pipeline.run(event_id, project_id, "123", ["file.py"], "diff")

    assert result.status == ValidationStatus.PASSED
    assert result.validators_run == 2
    assert result.validators_passed == 2
    assert result.validators_failed == 0
    assert len(result.blocking_failures) == 0


@pytest.mark.asyncio
async def test_pipeline_blocking_failure(project_id, event_id):
    """Test pipeline with blocking failure."""
    pipeline = ValidationPipeline(
        validators=[MockPassingValidator(), MockFailingValidator()]
    )

    result = await pipeline.run(event_id, project_id, "123", ["file.py"], "diff")

    assert result.status == ValidationStatus.FAILED
    assert result.validators_passed == 1
    assert result.validators_failed == 1
    assert len(result.blocking_failures) == 1
    assert result.blocking_failures[0].validator_name == "mock_fail"


@pytest.mark.asyncio
async def test_pipeline_nonblocking_failure(project_id, event_id):
    """Test pipeline with non-blocking failure."""
    pipeline = ValidationPipeline(
        validators=[MockPassingValidator(), MockNonBlockingFailValidator()]
    )

    result = await pipeline.run(event_id, project_id, "123", ["file.py"], "diff")

    assert result.status == ValidationStatus.PASSED  # Non-blocking
    assert result.validators_passed == 1
    assert result.validators_failed == 1
    assert len(result.blocking_failures) == 0  # Failure was not blocking


# ============================================================================
# Test Parallel Execution
# ============================================================================


@pytest.mark.asyncio
async def test_pipeline_parallel_execution(project_id, event_id):
    """Test that validators run in parallel."""
    # 3 validators each taking 100ms
    pipeline = ValidationPipeline(
        validators=[
            MockSlowValidator(delay=0.1),
            MockSlowValidator(delay=0.1),
            MockSlowValidator(delay=0.1),
        ]
    )

    result = await pipeline.run(event_id, project_id, "123", ["file.py"], "diff")

    # If parallel, should complete in ~100ms, not 300ms
    assert result.duration_ms < 200  # Allow some overhead


# ============================================================================
# Test Timeout Handling
# ============================================================================


@pytest.mark.asyncio
async def test_pipeline_validator_timeout(project_id, event_id):
    """Test timeout handling for slow validators."""
    pipeline = ValidationPipeline(validators=[MockTimeoutValidator()])

    result = await pipeline.run(event_id, project_id, "123", ["file.py"], "diff")

    assert len(result.results) == 1
    assert result.results[0].status == ValidatorStatus.TIMEOUT
    assert result.results[0].blocking is False  # Timeout doesn't block


# ============================================================================
# Test Error Handling
# ============================================================================


@pytest.mark.asyncio
async def test_pipeline_validator_error(project_id, event_id):
    """Test error handling for failing validators."""
    pipeline = ValidationPipeline(validators=[MockErrorValidator()])

    result = await pipeline.run(event_id, project_id, "123", ["file.py"], "diff")

    assert len(result.results) == 1
    assert result.results[0].status == ValidatorStatus.ERROR
    assert "Mock error" in result.results[0].message
    assert result.results[0].blocking is False  # Error doesn't block


@pytest.mark.asyncio
async def test_pipeline_mixed_results(project_id, event_id):
    """Test pipeline with mixed results."""
    pipeline = ValidationPipeline(
        validators=[
            MockPassingValidator(),
            MockFailingValidator(),
            MockNonBlockingFailValidator(),
            MockErrorValidator(),
        ]
    )

    result = await pipeline.run(event_id, project_id, "123", ["file.py"], "diff")

    assert result.status == ValidationStatus.FAILED  # Has blocking failure
    assert result.validators_run == 4
    assert result.validators_passed == 1
    assert result.validators_failed == 3  # fail + nonblocking + error


# ============================================================================
# Test Result Structure
# ============================================================================


@pytest.mark.asyncio
async def test_pipeline_result_structure(project_id, event_id):
    """Test that result has correct structure."""
    pipeline = ValidationPipeline(validators=[MockPassingValidator()])

    result = await pipeline.run(event_id, project_id, "123", ["file.py"], "diff")

    assert isinstance(result, PipelineResult)
    assert result.event_id == event_id
    assert result.started_at is not None
    assert result.completed_at is not None
    assert result.duration_ms > 0


@pytest.mark.asyncio
async def test_pipeline_result_serialization(project_id, event_id):
    """Test that result can be serialized to dict."""
    pipeline = ValidationPipeline(validators=[MockPassingValidator()])

    result = await pipeline.run(event_id, project_id, "123", ["file.py"], "diff")
    result_dict = result.to_dict()

    assert "event_id" in result_dict
    assert "status" in result_dict
    assert "results" in result_dict
    assert "duration_ms" in result_dict
    assert result_dict["status"] == "passed"


# ============================================================================
# Test Validator Management
# ============================================================================


def test_add_validator():
    """Test adding validators to pipeline."""
    pipeline = ValidationPipeline(validators=[])

    pipeline.add_validator(MockPassingValidator())

    assert len(pipeline.validators) == 1
    assert "mock_pass" in pipeline.get_validators()


def test_remove_validator():
    """Test removing validators from pipeline."""
    pipeline = ValidationPipeline(
        validators=[MockPassingValidator(), MockFailingValidator()]
    )

    result = pipeline.remove_validator("mock_pass")

    assert result is True
    assert len(pipeline.validators) == 1
    assert "mock_pass" not in pipeline.get_validators()


def test_remove_nonexistent_validator():
    """Test removing non-existent validator."""
    pipeline = ValidationPipeline(validators=[MockPassingValidator()])

    result = pipeline.remove_validator("nonexistent")

    assert result is False
    assert len(pipeline.validators) == 1


def test_get_validators():
    """Test getting validator names."""
    pipeline = ValidationPipeline(
        validators=[MockPassingValidator(), MockFailingValidator()]
    )

    names = pipeline.get_validators()

    assert names == ["mock_pass", "mock_fail"]


# ============================================================================
# Test Default Validators
# ============================================================================


def test_default_validators():
    """Test that default validators are created."""
    pipeline = ValidationPipeline()

    names = pipeline.get_validators()

    assert "lint" in names
    assert "tests" in names
    assert "coverage" in names


# ============================================================================
# Test Edge Cases
# ============================================================================


@pytest.mark.asyncio
async def test_pipeline_empty_validators(project_id, event_id):
    """Test pipeline with no validators."""
    pipeline = ValidationPipeline(validators=[])

    result = await pipeline.run(event_id, project_id, "123", [], "")

    assert result.status == ValidationStatus.PASSED
    assert result.validators_run == 0


@pytest.mark.asyncio
async def test_pipeline_empty_files(project_id, event_id):
    """Test pipeline with empty file list."""
    pipeline = ValidationPipeline(validators=[MockPassingValidator()])

    result = await pipeline.run(event_id, project_id, "123", [], "")

    assert result.status == ValidationStatus.PASSED
