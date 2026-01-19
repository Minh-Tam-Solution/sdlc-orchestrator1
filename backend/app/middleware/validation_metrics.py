"""
Validation Pipeline Metrics - Prometheus Monitoring

SDLC Stage: 04 - BUILD
Sprint: 42 - AI Detection & Validation Pipeline
Framework: SDLC 5.1.3

Purpose:
Prometheus metrics for validation pipeline monitoring.
Provides visibility into pipeline latency, validator performance, and blocking rates.

Metrics Categories:
1. Pipeline Duration (Histogram) - Total pipeline execution time
2. Pipeline Results (Counter) - Pass/fail/error counts
3. Validator Duration (Histogram) - Per-validator execution time
4. Validator Results (Counter) - Per-validator pass/fail/error counts
5. Blocking Failures (Counter) - Merge-blocking failure counts

Performance Target:
- Metric recording: <1ms overhead
- No blocking on validation path
"""

from prometheus_client import Counter, Gauge, Histogram

# ============================================================================
# Pipeline Duration Metrics
# ============================================================================

validation_pipeline_duration_seconds = Histogram(
    "validation_pipeline_duration_seconds",
    "Duration of validation pipeline execution in seconds",
    buckets=[1, 5, 10, 30, 60, 120, 180, 300, 360],
)

# ============================================================================
# Pipeline Results Metrics
# ============================================================================

validation_pipeline_results_total = Counter(
    "validation_pipeline_results_total",
    "Total number of validation pipeline results",
    labelnames=["status"],  # passed, failed, error
)

validation_pipeline_requests_total = Counter(
    "validation_pipeline_requests_total",
    "Total number of validation pipeline requests",
)

# ============================================================================
# Validator Duration Metrics
# ============================================================================

validation_validator_duration_seconds = Histogram(
    "validation_validator_duration_seconds",
    "Duration of individual validator execution in seconds",
    labelnames=["validator"],
    buckets=[0.5, 1, 5, 10, 30, 60, 120, 180],
)

# ============================================================================
# Validator Results Metrics
# ============================================================================

validation_validator_results_total = Counter(
    "validation_validator_results_total",
    "Total number of validator results",
    labelnames=["validator", "status"],  # passed, failed, error, timeout, skipped
)

# ============================================================================
# Blocking Failures Metrics
# ============================================================================

validation_blocking_failures_total = Counter(
    "validation_blocking_failures_total",
    "Total number of merge-blocking validation failures",
    labelnames=["validator"],
)

validation_blocking_rate = Gauge(
    "validation_blocking_rate",
    "Rate of merge-blocking failures (rolling window)",
)

# ============================================================================
# Queue Metrics
# ============================================================================

validation_queue_size = Gauge(
    "validation_queue_size",
    "Current size of validation queue",
)

validation_queue_wait_seconds = Histogram(
    "validation_queue_wait_seconds",
    "Time spent waiting in validation queue",
    buckets=[1, 5, 10, 30, 60, 120, 300, 600],
)

# ============================================================================
# Helper Functions
# ============================================================================


def record_pipeline_result(
    status: str,
    duration_seconds: float,
    validators_run: int,
    blocking_failures: int,
):
    """
    Record a validation pipeline result.

    Args:
        status: Pipeline status (passed, failed, error)
        duration_seconds: Total pipeline duration in seconds
        validators_run: Number of validators executed
        blocking_failures: Number of blocking failures
    """
    validation_pipeline_requests_total.inc()
    validation_pipeline_results_total.labels(status=status).inc()
    validation_pipeline_duration_seconds.observe(duration_seconds)

    # Update blocking rate (simplified - in production use rolling window)
    if blocking_failures > 0:
        validation_blocking_rate.set(blocking_failures / validators_run)


def record_validator_result(
    validator_name: str,
    status: str,
    duration_seconds: float,
    blocking: bool = False,
):
    """
    Record an individual validator result.

    Args:
        validator_name: Name of the validator
        status: Validator status (passed, failed, error, timeout, skipped)
        duration_seconds: Validator execution duration
        blocking: Whether this was a blocking failure
    """
    validation_validator_results_total.labels(
        validator=validator_name, status=status
    ).inc()
    validation_validator_duration_seconds.labels(validator=validator_name).observe(
        duration_seconds
    )

    if blocking and status in ("failed", "error"):
        validation_blocking_failures_total.labels(validator=validator_name).inc()


def record_queue_size(size: int):
    """Record current validation queue size."""
    validation_queue_size.set(size)


def record_queue_wait(wait_seconds: float):
    """Record time spent waiting in validation queue."""
    validation_queue_wait_seconds.observe(wait_seconds)
