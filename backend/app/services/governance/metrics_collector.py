"""
=========================================================================
Prometheus Metrics Collector - Governance System Observability
SDLC Orchestrator - Sprint 110 (CEO Dashboard & Observability)

Version: 1.0.0
Date: January 27, 2026
Status: ACTIVE - Sprint 110 Day 3
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Collect and export 45 Prometheus metrics
- Support CEO/Tech/Ops dashboards in Grafana
- Enable kill switch auto-trigger monitoring
- Track SLO compliance (>99% uptime, <100ms p95)

Metric Categories (per MONITORING-PLAN.md):
1. Governance System Metrics (15 metrics)
2. Performance Metrics (10 metrics)
3. Business Metrics - CEO Dashboard (8 metrics)
4. Developer Experience Metrics (7 metrics)
5. System Health Metrics (5 metrics)

Zero Mock Policy: Real Prometheus metrics collection
=========================================================================
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

logger = logging.getLogger(__name__)


# ============================================================================
# Prometheus Metric Definitions
# ============================================================================


class MetricType(str, Enum):
    """Prometheus metric types."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class MetricDefinition:
    """
    Definition of a Prometheus metric.
    """

    name: str
    type: MetricType
    description: str
    labels: List[str] = field(default_factory=list)
    buckets: Optional[List[float]] = None  # For histograms


# ============================================================================
# Governance System Metrics (15 metrics)
# ============================================================================

GOVERNANCE_METRICS = [
    # Submission Lifecycle
    MetricDefinition(
        name="governance_submissions_total",
        type=MetricType.COUNTER,
        description="Total number of governance submissions",
        labels=["project_id", "status"],
    ),
    MetricDefinition(
        name="governance_submissions_duration_seconds",
        type=MetricType.HISTOGRAM,
        description="Time from submission to validation complete",
        labels=["project_id"],
        buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
    ),
    MetricDefinition(
        name="governance_rejections_total",
        type=MetricType.COUNTER,
        description="Total number of rejections by reason",
        labels=["project_id", "rejection_reason"],
    ),
    # Vibecoding Index
    MetricDefinition(
        name="governance_vibecoding_index",
        type=MetricType.HISTOGRAM,
        description="Vibecoding Index distribution",
        labels=["project_id", "routing"],
        buckets=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    ),
    MetricDefinition(
        name="governance_vibecoding_index_avg",
        type=MetricType.GAUGE,
        description="Average Vibecoding Index (7-day rolling)",
        labels=["project_id"],
    ),
    # Routing Decisions
    MetricDefinition(
        name="governance_routing_total",
        type=MetricType.COUNTER,
        description="Routing decisions by category",
        labels=["project_id", "routing"],
    ),
    # Signal Breakdown (5 signals)
    MetricDefinition(
        name="governance_signals_architectural_smell",
        type=MetricType.HISTOGRAM,
        description="Architectural smell signal (0-100)",
        labels=["project_id"],
        buckets=[0, 20, 40, 60, 80, 100],
    ),
    MetricDefinition(
        name="governance_signals_abstraction_complexity",
        type=MetricType.HISTOGRAM,
        description="Abstraction complexity signal (0-100)",
        labels=["project_id"],
        buckets=[0, 20, 40, 60, 80, 100],
    ),
    MetricDefinition(
        name="governance_signals_ai_dependency_ratio",
        type=MetricType.HISTOGRAM,
        description="AI dependency ratio signal (0-100)",
        labels=["project_id"],
        buckets=[0, 20, 40, 60, 80, 100],
    ),
    MetricDefinition(
        name="governance_signals_change_surface_area",
        type=MetricType.HISTOGRAM,
        description="Change surface area signal (0-100)",
        labels=["project_id"],
        buckets=[0, 20, 40, 60, 80, 100],
    ),
    MetricDefinition(
        name="governance_signals_drift_velocity",
        type=MetricType.HISTOGRAM,
        description="Drift velocity signal (0-100)",
        labels=["project_id"],
        buckets=[0, 20, 40, 60, 80, 100],
    ),
    # Critical Path Override
    MetricDefinition(
        name="governance_critical_override_total",
        type=MetricType.COUNTER,
        description="MAX CRITICALITY OVERRIDE activations",
        labels=["project_id", "critical_category"],
    ),
    # Evidence Vault
    MetricDefinition(
        name="evidence_vault_uploads_total",
        type=MetricType.COUNTER,
        description="Total evidence uploads",
        labels=["project_id", "evidence_type"],
    ),
    MetricDefinition(
        name="evidence_vault_size_bytes",
        type=MetricType.GAUGE,
        description="Total evidence storage size",
        labels=["project_id"],
    ),
    # Escalations & CEO Overrides
    MetricDefinition(
        name="governance_escalations_total",
        type=MetricType.COUNTER,
        description="Total escalations to CEO/CTO",
        labels=["project_id", "escalated_to"],
    ),
    MetricDefinition(
        name="governance_ceo_overrides_total",
        type=MetricType.COUNTER,
        description="CEO overrides (agrees vs disagrees with index)",
        labels=["project_id", "override_type"],
    ),
]

# ============================================================================
# Performance Metrics (10 metrics)
# ============================================================================

PERFORMANCE_METRICS = [
    # API Latency
    MetricDefinition(
        name="api_request_duration_seconds",
        type=MetricType.HISTOGRAM,
        description="API request duration",
        labels=["method", "endpoint", "status"],
        buckets=[0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0],
    ),
    # Database Query Performance
    MetricDefinition(
        name="db_query_duration_seconds",
        type=MetricType.HISTOGRAM,
        description="Database query duration",
        labels=["query_name", "table"],
        buckets=[0.001, 0.01, 0.05, 0.1, 0.5, 1.0],
    ),
    # OPA Policy Evaluation
    MetricDefinition(
        name="opa_evaluation_duration_seconds",
        type=MetricType.HISTOGRAM,
        description="OPA policy evaluation duration",
        labels=["policy_name"],
        buckets=[0.01, 0.05, 0.1, 0.2, 0.5],
    ),
    # MinIO Evidence Upload
    MetricDefinition(
        name="minio_upload_duration_seconds",
        type=MetricType.HISTOGRAM,
        description="MinIO evidence upload duration",
        labels=["bucket"],
        buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
    ),
    # LLM Generation
    MetricDefinition(
        name="llm_generation_duration_seconds",
        type=MetricType.HISTOGRAM,
        description="LLM generation duration",
        labels=["provider", "model"],
        buckets=[1.0, 3.0, 5.0, 10.0, 15.0, 30.0],
    ),
    MetricDefinition(
        name="llm_generation_success_rate",
        type=MetricType.GAUGE,
        description="LLM generation success rate (0-1)",
        labels=["provider", "model"],
    ),
    MetricDefinition(
        name="llm_fallback_triggered_total",
        type=MetricType.COUNTER,
        description="LLM fallback activations",
        labels=["provider", "fallback_type"],
    ),
    # Auto-Generation Performance
    MetricDefinition(
        name="auto_generation_duration_seconds",
        type=MetricType.HISTOGRAM,
        description="Auto-generation component duration",
        labels=["component"],
        buckets=[1.0, 3.0, 5.0, 10.0, 15.0, 30.0],
    ),
    # Cache Performance
    MetricDefinition(
        name="cache_hit_rate",
        type=MetricType.GAUGE,
        description="Redis cache hit rate (0-1)",
        labels=["cache_name"],
    ),
    # Worker Queue
    MetricDefinition(
        name="worker_queue_length",
        type=MetricType.GAUGE,
        description="Celery worker queue length",
        labels=["queue_name"],
    ),
]

# ============================================================================
# Business Metrics - CEO Dashboard (8 metrics)
# ============================================================================

BUSINESS_METRICS = [
    # CEO Time Saved
    MetricDefinition(
        name="ceo_time_saved_hours",
        type=MetricType.GAUGE,
        description="CEO time saved this week (hours)",
        labels=["week"],
    ),
    MetricDefinition(
        name="ceo_pr_review_reduction_percent",
        type=MetricType.GAUGE,
        description="Percentage of PRs NOT requiring CEO review",
        labels=["week"],
    ),
    # Governance Autonomy
    MetricDefinition(
        name="governance_without_ceo_percent",
        type=MetricType.GAUGE,
        description="Decisions made without CEO involvement",
        labels=["week"],
    ),
    # Code Quality Improvement
    MetricDefinition(
        name="code_quality_test_coverage_percent",
        type=MetricType.GAUGE,
        description="Test coverage percentage",
        labels=["project_id"],
    ),
    MetricDefinition(
        name="code_quality_production_bugs_total",
        type=MetricType.COUNTER,
        description="Production bugs (P0/P1/P2)",
        labels=["severity"],
    ),
    # Compliance
    MetricDefinition(
        name="compliance_pass_rate_percent",
        type=MetricType.GAUGE,
        description="First submission pass rate",
        labels=["project_id"],
    ),
    # Bypass Incidents
    MetricDefinition(
        name="governance_bypass_incidents_total",
        type=MetricType.COUNTER,
        description="Bypass incidents",
        labels=["bypass_type"],
    ),
    # False Positive Rate
    MetricDefinition(
        name="governance_false_positive_rate",
        type=MetricType.GAUGE,
        description="CEO disagrees with Red/Orange routing",
        labels=["week"],
    ),
]

# ============================================================================
# Developer Experience Metrics (7 metrics)
# ============================================================================

DEVELOPER_EXPERIENCE_METRICS = [
    # Developer Friction
    MetricDefinition(
        name="developer_friction_minutes",
        type=MetricType.HISTOGRAM,
        description="Time from PR ready to governance passed",
        labels=["project_id"],
        buckets=[1, 3, 5, 10, 15, 30],
    ),
    # Auto-Generation Usage
    MetricDefinition(
        name="auto_generation_usage_rate",
        type=MetricType.GAUGE,
        description="Auto-generation usage rate (0-1)",
        labels=["component"],
    ),
    MetricDefinition(
        name="auto_generation_quality_score",
        type=MetricType.HISTOGRAM,
        description="LLM output quality score (0-1)",
        labels=["component"],
        buckets=[0.0, 0.3, 0.5, 0.7, 0.9, 1.0],
    ),
    # Developer Satisfaction
    MetricDefinition(
        name="developer_satisfaction_nps",
        type=MetricType.GAUGE,
        description="Developer NPS score (-100 to 100)",
        labels=["week"],
    ),
    # Feedback Actionability
    MetricDefinition(
        name="feedback_template_usage_total",
        type=MetricType.COUNTER,
        description="Feedback template usage",
        labels=["template_id"],
    ),
    MetricDefinition(
        name="feedback_resolution_time_minutes",
        type=MetricType.HISTOGRAM,
        description="Time to resolve feedback",
        labels=["template_id"],
        buckets=[1, 5, 10, 30, 60],
    ),
    # Break Glass Activations
    MetricDefinition(
        name="governance_break_glass_total",
        type=MetricType.COUNTER,
        description="Break glass activations",
        labels=["severity"],
    ),
]

# ============================================================================
# System Health Metrics (5 metrics)
# ============================================================================

SYSTEM_HEALTH_METRICS = [
    # Uptime
    MetricDefinition(
        name="system_uptime_seconds",
        type=MetricType.GAUGE,
        description="System uptime in seconds",
        labels=[],
    ),
    # Error Rate
    MetricDefinition(
        name="system_errors_total",
        type=MetricType.COUNTER,
        description="System errors",
        labels=["error_type", "severity"],
    ),
    # Kill Switch Status
    MetricDefinition(
        name="kill_switch_status",
        type=MetricType.GAUGE,
        description="Kill switch status (0=OFF, 1=WARNING, 2=SOFT, 3=FULL)",
        labels=[],
    ),
    MetricDefinition(
        name="kill_switch_triggered_total",
        type=MetricType.COUNTER,
        description="Kill switch activations",
        labels=["trigger_reason"],
    ),
    # Resource Usage
    MetricDefinition(
        name="system_cpu_usage_percent",
        type=MetricType.GAUGE,
        description="CPU usage percentage",
        labels=[],
    ),
    MetricDefinition(
        name="system_memory_usage_percent",
        type=MetricType.GAUGE,
        description="Memory usage percentage",
        labels=[],
    ),
]

# Combine all metrics
ALL_METRICS = (
    GOVERNANCE_METRICS +
    PERFORMANCE_METRICS +
    BUSINESS_METRICS +
    DEVELOPER_EXPERIENCE_METRICS +
    SYSTEM_HEALTH_METRICS
)


# ============================================================================
# Metrics Data Classes
# ============================================================================


@dataclass
class CounterValue:
    """Counter metric value."""

    name: str
    value: int
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class GaugeValue:
    """Gauge metric value."""

    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class HistogramValue:
    """Histogram metric value."""

    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# Prometheus Metrics Collector Service
# ============================================================================


class PrometheusMetricsCollector:
    """
    Prometheus Metrics Collector for Governance System.

    Collects and exports 45 metrics across 5 categories:
    1. Governance System (15 metrics)
    2. Performance (10 metrics)
    3. Business / CEO Dashboard (8 metrics)
    4. Developer Experience (7 metrics)
    5. System Health (5 metrics)

    SLO Targets:
    - Uptime: >99%
    - API Latency P95: <100ms
    - False Positive Rate: <10%
    """

    def __init__(self):
        """Initialize the metrics collector."""
        # In-memory metric storage
        self._counters: Dict[str, Dict[str, int]] = {}
        self._gauges: Dict[str, Dict[str, float]] = {}
        self._histograms: Dict[str, Dict[str, List[float]]] = {}

        # Service start time for uptime calculation
        self._start_time = datetime.utcnow()

        # Initialize metric definitions
        self._metric_definitions = {m.name: m for m in ALL_METRICS}

        logger.info(f"PrometheusMetricsCollector initialized with {len(ALL_METRICS)} metrics")

    # =========================================================================
    # Counter Methods
    # =========================================================================

    def increment_counter(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None,
        value: int = 1,
    ) -> None:
        """
        Increment a counter metric.

        Args:
            name: Metric name
            labels: Label key-value pairs
            value: Increment value (default 1)
        """
        labels = labels or {}
        label_key = self._make_label_key(labels)

        if name not in self._counters:
            self._counters[name] = {}

        if label_key not in self._counters[name]:
            self._counters[name][label_key] = 0

        self._counters[name][label_key] += value

    def get_counter(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None,
    ) -> int:
        """Get current counter value."""
        labels = labels or {}
        label_key = self._make_label_key(labels)
        return self._counters.get(name, {}).get(label_key, 0)

    # =========================================================================
    # Gauge Methods
    # =========================================================================

    def set_gauge(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Set a gauge metric value.

        Args:
            name: Metric name
            value: Gauge value
            labels: Label key-value pairs
        """
        labels = labels or {}
        label_key = self._make_label_key(labels)

        if name not in self._gauges:
            self._gauges[name] = {}

        self._gauges[name][label_key] = value

    def get_gauge(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None,
    ) -> float:
        """Get current gauge value."""
        labels = labels or {}
        label_key = self._make_label_key(labels)
        return self._gauges.get(name, {}).get(label_key, 0.0)

    def inc_gauge(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None,
        value: float = 1.0,
    ) -> None:
        """Increment a gauge value."""
        current = self.get_gauge(name, labels)
        self.set_gauge(name, current + value, labels)

    def dec_gauge(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None,
        value: float = 1.0,
    ) -> None:
        """Decrement a gauge value."""
        current = self.get_gauge(name, labels)
        self.set_gauge(name, current - value, labels)

    # =========================================================================
    # Histogram Methods
    # =========================================================================

    def observe_histogram(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Record a histogram observation.

        Args:
            name: Metric name
            value: Observed value
            labels: Label key-value pairs
        """
        labels = labels or {}
        label_key = self._make_label_key(labels)

        if name not in self._histograms:
            self._histograms[name] = {}

        if label_key not in self._histograms[name]:
            self._histograms[name][label_key] = []

        self._histograms[name][label_key].append(value)

        # Keep last 1000 observations for percentile calculations
        if len(self._histograms[name][label_key]) > 1000:
            self._histograms[name][label_key] = self._histograms[name][label_key][-1000:]

    def get_histogram_stats(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None,
    ) -> Dict[str, float]:
        """
        Get histogram statistics (count, sum, percentiles).

        Returns:
            Dictionary with count, sum, p50, p95, p99
        """
        labels = labels or {}
        label_key = self._make_label_key(labels)

        observations = self._histograms.get(name, {}).get(label_key, [])

        if not observations:
            return {"count": 0, "sum": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0}

        sorted_obs = sorted(observations)
        count = len(sorted_obs)

        return {
            "count": count,
            "sum": sum(sorted_obs),
            "p50": self._percentile(sorted_obs, 50),
            "p95": self._percentile(sorted_obs, 95),
            "p99": self._percentile(sorted_obs, 99),
        }

    # =========================================================================
    # Timer Context Manager
    # =========================================================================

    class Timer:
        """Context manager for timing operations."""

        def __init__(
            self,
            collector: "PrometheusMetricsCollector",
            metric_name: str,
            labels: Optional[Dict[str, str]] = None,
        ):
            self.collector = collector
            self.metric_name = metric_name
            self.labels = labels or {}
            self.start_time: Optional[float] = None

        def __enter__(self) -> "PrometheusMetricsCollector.Timer":
            self.start_time = time.time()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            if self.start_time:
                duration = time.time() - self.start_time
                self.collector.observe_histogram(
                    self.metric_name,
                    duration,
                    self.labels,
                )

    def timer(
        self,
        metric_name: str,
        labels: Optional[Dict[str, str]] = None,
    ) -> Timer:
        """
        Create a timer context manager for measuring durations.

        Usage:
            with metrics.timer("api_request_duration_seconds", {"endpoint": "/api/v1/gates"}):
                # ... operation ...
        """
        return self.Timer(self, metric_name, labels)

    # =========================================================================
    # Governance Metrics Recording
    # =========================================================================

    def record_submission(
        self,
        project_id: str,
        status: str,  # "passed", "rejected", "pending"
        vibecoding_index: float,
        routing: str,  # "auto_approve", "tech_lead_review", "ceo_should_review", "ceo_must_review"
        duration_seconds: float,
        signal_breakdown: Optional[Dict[str, float]] = None,
        rejection_reason: Optional[str] = None,
        critical_override: Optional[str] = None,
    ) -> None:
        """
        Record a governance submission with all related metrics.

        This is the main entry point for recording submission metrics.
        """
        # Submission counter
        self.increment_counter(
            "governance_submissions_total",
            {"project_id": project_id, "status": status},
        )

        # Submission duration
        self.observe_histogram(
            "governance_submissions_duration_seconds",
            duration_seconds,
            {"project_id": project_id},
        )

        # Vibecoding Index
        self.observe_histogram(
            "governance_vibecoding_index",
            vibecoding_index,
            {"project_id": project_id, "routing": routing},
        )

        # Routing decision
        self.increment_counter(
            "governance_routing_total",
            {"project_id": project_id, "routing": routing},
        )

        # Rejection reason (if rejected)
        if status == "rejected" and rejection_reason:
            self.increment_counter(
                "governance_rejections_total",
                {"project_id": project_id, "rejection_reason": rejection_reason},
            )

        # Signal breakdown (if provided)
        if signal_breakdown:
            signal_metrics = {
                "architectural_smell": "governance_signals_architectural_smell",
                "abstraction_complexity": "governance_signals_abstraction_complexity",
                "ai_dependency_ratio": "governance_signals_ai_dependency_ratio",
                "change_surface_area": "governance_signals_change_surface_area",
                "drift_velocity": "governance_signals_drift_velocity",
            }

            for signal_name, metric_name in signal_metrics.items():
                if signal_name in signal_breakdown:
                    self.observe_histogram(
                        metric_name,
                        signal_breakdown[signal_name],
                        {"project_id": project_id},
                    )

        # Critical path override
        if critical_override:
            self.increment_counter(
                "governance_critical_override_total",
                {"project_id": project_id, "critical_category": critical_override},
            )

        # Escalation (if Orange or Red)
        if routing in ("ceo_should_review", "ceo_must_review"):
            escalated_to = "ceo" if routing == "ceo_must_review" else "tech_lead"
            self.increment_counter(
                "governance_escalations_total",
                {"project_id": project_id, "escalated_to": escalated_to},
            )

        logger.debug(
            f"Recorded submission metrics: project={project_id}, "
            f"status={status}, index={vibecoding_index:.1f}, routing={routing}"
        )

    def record_ceo_override(
        self,
        project_id: str,
        override_type: str,  # "agrees" or "disagrees"
    ) -> None:
        """Record a CEO override for calibration tracking."""
        self.increment_counter(
            "governance_ceo_overrides_total",
            {"project_id": project_id, "override_type": override_type},
        )

    def record_evidence_upload(
        self,
        project_id: str,
        evidence_type: str,
        size_bytes: int,
    ) -> None:
        """Record an evidence upload."""
        self.increment_counter(
            "evidence_vault_uploads_total",
            {"project_id": project_id, "evidence_type": evidence_type},
        )

        # Update total size gauge
        current_size = self.get_gauge("evidence_vault_size_bytes", {"project_id": project_id})
        self.set_gauge(
            "evidence_vault_size_bytes",
            current_size + size_bytes,
            {"project_id": project_id},
        )

    def record_llm_generation(
        self,
        provider: str,
        model: str,
        duration_seconds: float,
        success: bool,
        fallback_triggered: bool = False,
        fallback_type: Optional[str] = None,
    ) -> None:
        """Record LLM generation metrics."""
        # Duration
        self.observe_histogram(
            "llm_generation_duration_seconds",
            duration_seconds,
            {"provider": provider, "model": model},
        )

        # Update success rate (simplified rolling average)
        current_rate = self.get_gauge("llm_generation_success_rate", {"provider": provider, "model": model})
        new_rate = (current_rate * 0.9) + (1.0 if success else 0.0) * 0.1  # Exponential moving average
        self.set_gauge(
            "llm_generation_success_rate",
            new_rate,
            {"provider": provider, "model": model},
        )

        # Fallback
        if fallback_triggered and fallback_type:
            self.increment_counter(
                "llm_fallback_triggered_total",
                {"provider": provider, "fallback_type": fallback_type},
            )

    def record_developer_friction(
        self,
        project_id: str,
        friction_minutes: float,
    ) -> None:
        """Record developer friction (time to pass governance)."""
        self.observe_histogram(
            "developer_friction_minutes",
            friction_minutes,
            {"project_id": project_id},
        )

    def record_break_glass(
        self,
        severity: str,  # "P0", "P1", "abuse"
    ) -> None:
        """Record break glass activation."""
        self.increment_counter(
            "governance_break_glass_total",
            {"severity": severity},
        )

    def record_bypass_incident(
        self,
        bypass_type: str,  # "pre_commit_skip", "direct_push", "break_glass_abuse"
    ) -> None:
        """Record governance bypass incident."""
        self.increment_counter(
            "governance_bypass_incidents_total",
            {"bypass_type": bypass_type},
        )

    # =========================================================================
    # System Health Metrics
    # =========================================================================

    def update_system_health(
        self,
        cpu_percent: float,
        memory_percent: float,
    ) -> None:
        """Update system health gauges."""
        # Uptime
        uptime_seconds = (datetime.utcnow() - self._start_time).total_seconds()
        self.set_gauge("system_uptime_seconds", uptime_seconds)

        # CPU and memory
        self.set_gauge("system_cpu_usage_percent", cpu_percent)
        self.set_gauge("system_memory_usage_percent", memory_percent)

    def set_kill_switch_status(
        self,
        status: str,  # "OFF", "WARNING", "SOFT", "FULL"
    ) -> None:
        """Set kill switch status gauge."""
        status_values = {"OFF": 0, "WARNING": 1, "SOFT": 2, "FULL": 3}
        self.set_gauge("kill_switch_status", status_values.get(status.upper(), 0))

    def record_kill_switch_trigger(
        self,
        reason: str,  # "rejection_rate_high", "latency_high", "false_positive_high", "developer_complaints"
    ) -> None:
        """Record kill switch trigger."""
        self.increment_counter(
            "kill_switch_triggered_total",
            {"trigger_reason": reason},
        )

    def record_system_error(
        self,
        error_type: str,
        severity: str,
    ) -> None:
        """Record a system error."""
        self.increment_counter(
            "system_errors_total",
            {"error_type": error_type, "severity": severity},
        )

    # =========================================================================
    # CEO Dashboard Metrics
    # =========================================================================

    def update_ceo_metrics(
        self,
        week: int,
        time_saved_hours: float,
        pr_review_reduction_percent: float,
        governance_without_ceo_percent: float,
        false_positive_rate: float,
    ) -> None:
        """Update CEO dashboard metrics."""
        week_str = str(week)

        self.set_gauge("ceo_time_saved_hours", time_saved_hours, {"week": week_str})
        self.set_gauge("ceo_pr_review_reduction_percent", pr_review_reduction_percent, {"week": week_str})
        self.set_gauge("governance_without_ceo_percent", governance_without_ceo_percent, {"week": week_str})
        self.set_gauge("governance_false_positive_rate", false_positive_rate, {"week": week_str})

    # =========================================================================
    # Prometheus Output Format
    # =========================================================================

    def get_metrics_output(self) -> str:
        """
        Get metrics in Prometheus text exposition format.

        Returns:
            String in Prometheus format
        """
        lines = []

        # Add HELP and TYPE for each metric definition
        for metric in ALL_METRICS:
            lines.append(f"# HELP {metric.name} {metric.description}")
            lines.append(f"# TYPE {metric.name} {metric.type.value}")

            # Output metric values
            if metric.type == MetricType.COUNTER:
                for label_key, value in self._counters.get(metric.name, {}).items():
                    labels_str = self._format_labels(label_key)
                    lines.append(f"{metric.name}{labels_str} {value}")

            elif metric.type == MetricType.GAUGE:
                for label_key, value in self._gauges.get(metric.name, {}).items():
                    labels_str = self._format_labels(label_key)
                    lines.append(f"{metric.name}{labels_str} {value}")

            elif metric.type == MetricType.HISTOGRAM:
                for label_key, observations in self._histograms.get(metric.name, {}).items():
                    if not observations:
                        continue

                    labels_str = self._format_labels(label_key)
                    sorted_obs = sorted(observations)

                    # Output bucket counts
                    if metric.buckets:
                        for bucket in metric.buckets:
                            count = sum(1 for v in sorted_obs if v <= bucket)
                            if labels_str:
                                bucket_labels = f'{labels_str[:-1]},le="{bucket}"}}'
                            else:
                                bucket_labels = f'{{le="{bucket}"}}'
                            lines.append(f"{metric.name}_bucket{bucket_labels} {count}")

                        # +Inf bucket
                        if labels_str:
                            inf_labels = f'{labels_str[:-1]},le="+Inf"}}'
                        else:
                            inf_labels = '{le="+Inf"}'
                        lines.append(f"{metric.name}_bucket{inf_labels} {len(sorted_obs)}")

                    # Sum and count
                    lines.append(f"{metric.name}_sum{labels_str} {sum(sorted_obs)}")
                    lines.append(f"{metric.name}_count{labels_str} {len(sorted_obs)}")

            lines.append("")  # Empty line between metrics

        return "\n".join(lines)

    def get_metrics_json(self) -> Dict[str, Any]:
        """
        Get metrics in JSON format for API response.

        Returns:
            Dictionary with all metrics
        """
        result = {
            "counters": {},
            "gauges": {},
            "histograms": {},
            "timestamp": datetime.utcnow().isoformat(),
            "total_metrics": len(ALL_METRICS),
        }

        # Counters
        for name, values in self._counters.items():
            result["counters"][name] = values

        # Gauges
        for name, values in self._gauges.items():
            result["gauges"][name] = values

        # Histograms (with stats)
        for name, values in self._histograms.items():
            result["histograms"][name] = {
                label_key: self.get_histogram_stats(name, self._parse_label_key(label_key))
                for label_key in values.keys()
            }

        return result

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _make_label_key(self, labels: Dict[str, str]) -> str:
        """Create a hashable key from labels."""
        if not labels:
            return ""
        sorted_items = sorted(labels.items())
        return ",".join(f'{k}="{v}"' for k, v in sorted_items)

    def _parse_label_key(self, label_key: str) -> Dict[str, str]:
        """Parse label key back to dictionary."""
        if not label_key:
            return {}

        result = {}
        for part in label_key.split(","):
            if "=" in part:
                key, value = part.split("=", 1)
                result[key] = value.strip('"')
        return result

    def _format_labels(self, label_key: str) -> str:
        """Format label key for Prometheus output."""
        if not label_key:
            return ""
        return "{" + label_key + "}"

    def _percentile(self, sorted_data: List[float], percentile: float) -> float:
        """Calculate percentile from sorted data."""
        if not sorted_data:
            return 0.0
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]


# ============================================================================
# Singleton Pattern
# ============================================================================

_metrics_collector: Optional[PrometheusMetricsCollector] = None


def create_metrics_collector() -> PrometheusMetricsCollector:
    """
    Create new Prometheus Metrics Collector instance.

    Returns:
        PrometheusMetricsCollector instance
    """
    global _metrics_collector
    _metrics_collector = PrometheusMetricsCollector()
    return _metrics_collector


def get_metrics_collector() -> PrometheusMetricsCollector:
    """
    Get Prometheus Metrics Collector singleton.

    Returns:
        PrometheusMetricsCollector instance

    Raises:
        RuntimeError: If collector not initialized
    """
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = PrometheusMetricsCollector()
    return _metrics_collector
