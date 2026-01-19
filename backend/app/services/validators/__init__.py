"""
Validators - Base Interfaces and Types

SDLC Stage: 04 - BUILD
Sprint: 42 - AI Detection & Validation Pipeline
Framework: SDLC 5.1.3
Epic: EP-02 AI Safety Layer v1

Purpose:
Base classes and enums for the Validation Pipeline.
Provides unified interface for all validators (Lint, Tests, Coverage, etc.).

Architecture:
- Strategy pattern for extensible validators
- Async execution for parallel processing
- Blocking/non-blocking modes for policy control
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID


class ValidatorStatus(str, Enum):
    """Validator execution status."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    TIMEOUT = "timeout"


class ValidationStatus(str, Enum):
    """Overall validation pipeline status."""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"


@dataclass
class ValidatorResult:
    """Result from a single validator execution."""

    # Identification
    validator_name: str

    # Outcome
    status: ValidatorStatus
    message: str
    details: Dict[str, Any]

    # Performance
    duration_ms: int

    # Policy control
    blocking: bool  # If true, failure blocks merge

    # Timestamps
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert to dict for JSON serialization."""
        return {
            "validator_name": self.validator_name,
            "status": self.status.value,
            "message": self.message,
            "details": self.details,
            "duration_ms": self.duration_ms,
            "blocking": self.blocking,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass
class PipelineResult:
    """Result from the validation pipeline."""

    # Identification
    event_id: UUID

    # Outcome
    status: ValidationStatus
    results: List[ValidatorResult]
    blocking_failures: List[ValidatorResult]

    # Performance
    duration_ms: int

    # Timestamps
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Summary
    validators_run: int = 0
    validators_passed: int = 0
    validators_failed: int = 0

    def to_dict(self) -> dict:
        """Convert to dict for JSON serialization."""
        return {
            "event_id": str(self.event_id),
            "status": self.status.value,
            "results": [r.to_dict() for r in self.results],
            "blocking_failures": [f.to_dict() for f in self.blocking_failures],
            "duration_ms": self.duration_ms,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "validators_run": self.validators_run,
            "validators_passed": self.validators_passed,
            "validators_failed": self.validators_failed,
        }


@dataclass
class ValidatorConfig:
    """Configuration for a validator."""

    # Enable/disable
    enabled: bool = True

    # Policy control
    blocking: bool = True  # If true, failure blocks merge

    # Timeouts
    timeout_seconds: int = 300  # 5 minutes default

    # Custom settings
    settings: Dict[str, Any] = field(default_factory=dict)


class BaseValidator(ABC):
    """
    Base class for all validators.

    Validators are responsible for checking specific aspects of code quality:
    - Lint/Format: Code style compliance
    - Tests: Unit/integration test execution
    - Coverage: Test coverage thresholds
    - Security: SAST/vulnerability scanning
    - Custom: Project-specific validations

    Each validator:
    - Receives PR files and diff
    - Runs validation logic
    - Returns ValidatorResult
    - Can be blocking (merge-blocking) or non-blocking (advisory)
    """

    # Validator identification
    name: str = "base"
    description: str = "Base validator"

    # Default configuration
    default_blocking: bool = True
    default_timeout_seconds: int = 300

    def __init__(self, config: Optional[ValidatorConfig] = None):
        """
        Initialize validator with optional configuration.

        Args:
            config: Validator configuration (uses defaults if None)
        """
        self.config = config or ValidatorConfig(
            blocking=self.default_blocking,
            timeout_seconds=self.default_timeout_seconds,
        )

    @abstractmethod
    async def validate(
        self,
        project_id: UUID,
        pr_number: str,
        files: List[str],
        diff: str,
    ) -> ValidatorResult:
        """
        Run validation on PR files.

        Args:
            project_id: Project UUID for context
            pr_number: Pull request number
            files: List of changed file paths
            diff: Unified diff of all changes

        Returns:
            ValidatorResult with status, message, and details
        """
        pass

    def get_name(self) -> str:
        """Return validator name."""
        return self.name

    def is_blocking(self) -> bool:
        """Return whether validator is merge-blocking."""
        return self.config.blocking

    def get_timeout(self) -> int:
        """Return timeout in seconds."""
        return self.config.timeout_seconds
