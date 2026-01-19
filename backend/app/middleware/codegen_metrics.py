"""
=========================================================================
EP-06 Codegen Metrics - Prometheus Monitoring for Code Generation
SDLC Orchestrator - Sprint 50 (EP-06 Productization)

Purpose:
- Track code generation latency by provider and domain
- Monitor quality gate pass rates
- Measure TTFV (Time To First Value) for pilot tracking
- Track provider health and fallback events

Metrics Exposed:
- codegen_generation_duration_seconds (histogram) - Generation latency
- codegen_generation_total (counter) - Total generations
- codegen_quality_gate_duration_seconds (histogram) - Gate latency
- codegen_quality_gate_pass_rate (gauge) - Gate pass rate
- codegen_ttfv_seconds (histogram) - Time to first value
- codegen_provider_health (gauge) - Provider health status
- codegen_provider_fallback_total (counter) - Fallback events

Performance Targets (Sprint 49):
- TTFV: <30 minutes (1800 seconds)
- Quality Gate Pass Rate: >95%
- Generation Latency (p95): <15s (Ollama), <25s (Claude)
- Satisfaction: 8/10

Framework: SDLC 5.1.3 + SASE Level 2
=========================================================================
"""

from prometheus_client import Counter, Gauge, Histogram

# ============================================================================
# GENERATION METRICS
# ============================================================================

# Histogram: Code generation latency
codegen_generation_duration_seconds = Histogram(
    "codegen_generation_duration_seconds",
    "Code generation latency in seconds",
    ["provider", "domain", "scale"],
    buckets=(5, 10, 15, 20, 25, 30, 45, 60, 90, 120, 180),
)

# Counter: Total generations
codegen_generation_total = Counter(
    "codegen_generation_total",
    "Total code generation requests",
    ["provider", "domain", "status"],  # status: success, error, timeout
)

# Counter: Generation errors by type
codegen_generation_errors_total = Counter(
    "codegen_generation_errors_total",
    "Total code generation errors",
    ["provider", "error_type"],  # error_type: timeout, model_error, validation_failed
)

# Counter: Tokens used
codegen_tokens_total = Counter(
    "codegen_tokens_total",
    "Total tokens used for generation",
    ["provider", "domain"],
)

# ============================================================================
# QUALITY GATE METRICS
# ============================================================================

# Histogram: Quality gate duration
codegen_quality_gate_duration_seconds = Histogram(
    "codegen_quality_gate_duration_seconds",
    "Quality gate execution time in seconds",
    ["gate"],  # gate: syntax, security, context, tests
    buckets=(1, 2, 5, 10, 15, 30, 60),
)

# Gauge: Quality gate pass rate (rolling window)
codegen_quality_gate_pass_rate = Gauge(
    "codegen_quality_gate_pass_rate",
    "Quality gate pass rate (0.0 to 1.0)",
    ["gate"],
)

# Counter: Quality gate results
codegen_quality_gate_total = Counter(
    "codegen_quality_gate_total",
    "Total quality gate executions",
    ["gate", "result"],  # result: pass, fail, skip, error
)

# Counter: Quality gate failures by reason
codegen_quality_gate_failures_total = Counter(
    "codegen_quality_gate_failures_total",
    "Quality gate failures by reason",
    ["gate", "reason"],
)

# ============================================================================
# TTFV (TIME TO FIRST VALUE) METRICS
# ============================================================================

# Histogram: TTFV distribution
codegen_ttfv_seconds = Histogram(
    "codegen_ttfv_seconds",
    "Time to first value in seconds (session start to quality gate pass)",
    ["domain", "scale"],
    buckets=(300, 600, 900, 1200, 1500, 1800, 2400, 3600, 5400, 7200),  # 5m to 2h
)

# Counter: TTFV target met
codegen_ttfv_target_met_total = Counter(
    "codegen_ttfv_target_met_total",
    "Sessions that met TTFV target (<30 min)",
    ["domain"],
)

# Counter: TTFV target missed
codegen_ttfv_target_missed_total = Counter(
    "codegen_ttfv_target_missed_total",
    "Sessions that missed TTFV target (>=30 min)",
    ["domain"],
)

# ============================================================================
# PROVIDER HEALTH METRICS
# ============================================================================

# Gauge: Provider health (1=healthy, 0=unhealthy)
codegen_provider_health = Gauge(
    "codegen_provider_health",
    "Provider health status (1=healthy, 0=unhealthy)",
    ["provider"],
)

# Counter: Provider fallback events
codegen_provider_fallback_total = Counter(
    "codegen_provider_fallback_total",
    "Provider fallback events",
    ["from_provider", "to_provider", "reason"],
)

# Gauge: Provider response time (last request)
codegen_provider_latency_seconds = Gauge(
    "codegen_provider_latency_seconds",
    "Provider response time for last request",
    ["provider"],
)

# ============================================================================
# PILOT PROGRAM METRICS
# ============================================================================

# Gauge: Active pilot participants
codegen_pilot_participants_total = Gauge(
    "codegen_pilot_participants_total",
    "Total pilot program participants",
    ["status"],  # status: invited, registered, active, churned, completed
)

# Gauge: Pilot satisfaction score (average)
codegen_pilot_satisfaction_score = Gauge(
    "codegen_pilot_satisfaction_score",
    "Average pilot satisfaction score (1-10)",
    ["domain"],
)

# Counter: Pilot sessions
codegen_pilot_sessions_total = Counter(
    "codegen_pilot_sessions_total",
    "Total pilot sessions",
    ["domain", "result"],  # result: completed, abandoned
)

# ============================================================================
# COST METRICS
# ============================================================================

# Counter: Estimated cost (USD)
codegen_cost_usd_total = Counter(
    "codegen_cost_usd_total",
    "Estimated generation cost in USD",
    ["provider"],
)

# Gauge: Cost per generation (moving average)
codegen_cost_per_generation_usd = Gauge(
    "codegen_cost_per_generation_usd",
    "Average cost per generation in USD",
    ["provider"],
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def record_generation(
    provider: str,
    domain: str,
    scale: str,
    duration_seconds: float,
    status: str,
    tokens_used: int = 0,
    error_type: str = None,
) -> None:
    """
    Record a code generation event.

    Args:
        provider: Provider name (ollama, claude, deepcode)
        domain: Business domain (fnb, hospitality, retail)
        scale: Business scale (micro, small, medium)
        duration_seconds: Generation duration
        status: Result status (success, error, timeout)
        tokens_used: Number of tokens used
        error_type: Error type if status != success
    """
    # Record duration
    codegen_generation_duration_seconds.labels(
        provider=provider,
        domain=domain,
        scale=scale,
    ).observe(duration_seconds)

    # Increment counter
    codegen_generation_total.labels(
        provider=provider,
        domain=domain,
        status=status,
    ).inc()

    # Record tokens
    if tokens_used > 0:
        codegen_tokens_total.labels(
            provider=provider,
            domain=domain,
        ).inc(tokens_used)

    # Record error
    if error_type:
        codegen_generation_errors_total.labels(
            provider=provider,
            error_type=error_type,
        ).inc()

    # Update provider latency
    codegen_provider_latency_seconds.labels(provider=provider).set(duration_seconds)


def record_quality_gate(
    gate: str,
    duration_seconds: float,
    result: str,
    failure_reason: str = None,
) -> None:
    """
    Record a quality gate execution.

    Args:
        gate: Gate name (syntax, security, context, tests)
        duration_seconds: Gate execution time
        result: Result (pass, fail, skip, error)
        failure_reason: Reason for failure if result != pass
    """
    # Record duration
    codegen_quality_gate_duration_seconds.labels(gate=gate).observe(duration_seconds)

    # Increment counter
    codegen_quality_gate_total.labels(gate=gate, result=result).inc()

    # Record failure reason
    if failure_reason:
        codegen_quality_gate_failures_total.labels(
            gate=gate,
            reason=failure_reason,
        ).inc()


def record_ttfv(
    domain: str,
    scale: str,
    ttfv_seconds: int,
    target_met: bool,
) -> None:
    """
    Record TTFV measurement.

    Args:
        domain: Business domain
        scale: Business scale
        ttfv_seconds: Time to first value in seconds
        target_met: Whether TTFV target (<30 min) was met
    """
    # Record histogram
    codegen_ttfv_seconds.labels(domain=domain, scale=scale).observe(ttfv_seconds)

    # Increment appropriate counter
    if target_met:
        codegen_ttfv_target_met_total.labels(domain=domain).inc()
    else:
        codegen_ttfv_target_missed_total.labels(domain=domain).inc()


def record_provider_fallback(
    from_provider: str,
    to_provider: str,
    reason: str,
) -> None:
    """
    Record a provider fallback event.

    Args:
        from_provider: Provider that failed
        to_provider: Provider that was used instead
        reason: Reason for fallback (timeout, error, rate_limit)
    """
    codegen_provider_fallback_total.labels(
        from_provider=from_provider,
        to_provider=to_provider,
        reason=reason,
    ).inc()


def update_provider_health(provider: str, healthy: bool) -> None:
    """
    Update provider health status.

    Args:
        provider: Provider name
        healthy: Whether provider is healthy
    """
    codegen_provider_health.labels(provider=provider).set(1 if healthy else 0)


def update_pilot_metrics(
    participants_by_status: dict,
    satisfaction_by_domain: dict,
) -> None:
    """
    Update pilot program metrics.

    Args:
        participants_by_status: Dict of status -> count
        satisfaction_by_domain: Dict of domain -> average score
    """
    for status, count in participants_by_status.items():
        codegen_pilot_participants_total.labels(status=status).set(count)

    for domain, score in satisfaction_by_domain.items():
        codegen_pilot_satisfaction_score.labels(domain=domain).set(score)
