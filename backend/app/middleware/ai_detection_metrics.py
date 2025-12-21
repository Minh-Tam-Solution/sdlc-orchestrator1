"""
AI Detection Metrics - Prometheus Monitoring

SDLC Stage: 04 - BUILD
Sprint: 42 - AI Detection & Validation Pipeline
Framework: SDLC 5.1.1
CTO Review: P1 Requirement

Purpose:
Prometheus metrics for AI detection service monitoring.
Provides visibility into detection accuracy, latency, and strategy performance.

Metrics Categories:
1. Detection Duration (Histogram) - Per-strategy latency
2. Detection Results (Counter) - Tool detection counts
3. Strategy Confidence (Histogram) - Confidence distribution
4. Circuit Breaker (Gauge) - Detection service health

Performance Target:
- Metric recording: <1ms overhead
- No blocking on detection path
"""

from prometheus_client import Counter, Gauge, Histogram

from app.services.ai_detection import AIToolType, DetectionMethod

# ============================================================================
# Detection Duration Metrics
# ============================================================================

ai_detection_duration_seconds = Histogram(
    "ai_detection_duration_seconds",
    "Duration of AI detection operations in seconds",
    labelnames=["strategy"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

ai_detection_total_duration_seconds = Histogram(
    "ai_detection_total_duration_seconds",
    "Total duration of combined AI detection in seconds",
    buckets=[0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0],
)

# ============================================================================
# Detection Results Metrics
# ============================================================================

ai_detection_results_total = Counter(
    "ai_detection_results_total",
    "Total number of AI detection results",
    labelnames=["tool", "detected", "method"],
)

ai_detection_requests_total = Counter(
    "ai_detection_requests_total",
    "Total number of AI detection requests",
)

ai_detection_errors_total = Counter(
    "ai_detection_errors_total",
    "Total number of AI detection errors",
    labelnames=["strategy", "error_type"],
)

# ============================================================================
# Strategy Confidence Metrics
# ============================================================================

ai_detection_confidence = Histogram(
    "ai_detection_confidence",
    "AI detection confidence score distribution",
    labelnames=["strategy"],
    buckets=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
)

ai_detection_combined_confidence = Histogram(
    "ai_detection_combined_confidence",
    "Combined AI detection confidence score distribution",
    buckets=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
)

# ============================================================================
# Tool Detection Distribution
# ============================================================================

ai_detection_tool_distribution = Counter(
    "ai_detection_tool_distribution_total",
    "Distribution of detected AI tools",
    labelnames=["tool"],
)

# ============================================================================
# Circuit Breaker Metrics (P2 preparation)
# ============================================================================

ai_detection_circuit_state = Gauge(
    "ai_detection_circuit_state",
    "AI detection circuit breaker state (0=closed, 1=open, 2=half_open)",
)

ai_detection_circuit_failures = Counter(
    "ai_detection_circuit_failures_total",
    "Total AI detection circuit breaker failures",
)

# ============================================================================
# Helper Functions
# ============================================================================


def record_detection_request():
    """Record an AI detection request."""
    ai_detection_requests_total.inc()


def record_detection_result(
    detected: bool,
    tool: AIToolType | None,
    method: DetectionMethod,
    confidence: float,
    duration_seconds: float,
):
    """
    Record an AI detection result with all metrics.

    Args:
        detected: Whether AI code was detected
        tool: Detected AI tool (or None)
        method: Detection method used
        confidence: Combined confidence score
        duration_seconds: Total detection duration in seconds
    """
    # Record detection result
    tool_label = tool.value if tool else "none"
    ai_detection_results_total.labels(
        tool=tool_label,
        detected=str(detected).lower(),
        method=method.value,
    ).inc()

    # Record total duration
    ai_detection_total_duration_seconds.observe(duration_seconds)

    # Record combined confidence
    ai_detection_combined_confidence.observe(confidence)

    # Record tool distribution
    if detected and tool:
        ai_detection_tool_distribution.labels(tool=tool_label).inc()


def record_strategy_result(
    strategy: str,
    confidence: float,
    duration_seconds: float,
):
    """
    Record an individual strategy result.

    Args:
        strategy: Strategy name (metadata, commit, pattern)
        confidence: Strategy confidence score
        duration_seconds: Strategy execution duration
    """
    ai_detection_duration_seconds.labels(strategy=strategy).observe(duration_seconds)
    ai_detection_confidence.labels(strategy=strategy).observe(confidence)


def record_detection_error(strategy: str, error_type: str):
    """
    Record a detection error.

    Args:
        strategy: Strategy that errored
        error_type: Type of error (e.g., "timeout", "invalid_input")
    """
    ai_detection_errors_total.labels(strategy=strategy, error_type=error_type).inc()


def set_circuit_state(state: int):
    """
    Set circuit breaker state.

    Args:
        state: 0=closed (healthy), 1=open (failing), 2=half_open (recovering)
    """
    ai_detection_circuit_state.set(state)


def record_circuit_failure():
    """Record a circuit breaker failure."""
    ai_detection_circuit_failures.inc()
