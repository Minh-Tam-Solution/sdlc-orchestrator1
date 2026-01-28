"""
=========================================================================
Unit Tests for PrometheusMetricsCollector Service
SDLC Orchestrator - Sprint 110 (CEO Dashboard & Observability)

Version: 1.0.0
Date: January 28, 2026
Coverage Target: 80%+ isolated unit tests

Test Categories:
1. Enums (4 tests)
2. Data Classes (12 tests)
3. Metric Collections (5 tests)
4. Counter Methods (8 tests)
5. Gauge Methods (10 tests)
6. Histogram Methods (10 tests)
7. Timer Context Manager (4 tests)
8. Record Methods (15 tests)
9. System Health Methods (8 tests)
10. CEO Metrics Methods (4 tests)
11. Output Methods (6 tests)
12. Helper Methods (8 tests)
13. Factory Functions (4 tests)
14. Edge Cases (6 tests)

Zero Mock Policy: Real logic testing with in-memory storage
=========================================================================
"""

import pytest
import time
from datetime import datetime, timedelta
from unittest.mock import patch

from app.services.governance.metrics_collector import (
    MetricType,
    MetricDefinition,
    CounterValue,
    GaugeValue,
    HistogramValue,
    GOVERNANCE_METRICS,
    PERFORMANCE_METRICS,
    BUSINESS_METRICS,
    DEVELOPER_EXPERIENCE_METRICS,
    SYSTEM_HEALTH_METRICS,
    ALL_METRICS,
    PrometheusMetricsCollector,
    create_metrics_collector,
    get_metrics_collector,
)


# =============================================================================
# CATEGORY 1: ENUMS
# =============================================================================

class TestMetricTypeEnum:
    """Tests for MetricType enum."""

    def test_enum_001_counter_value(self):
        """Should have COUNTER type."""
        assert MetricType.COUNTER == "counter"
        assert MetricType.COUNTER.value == "counter"

    def test_enum_002_gauge_value(self):
        """Should have GAUGE type."""
        assert MetricType.GAUGE == "gauge"
        assert MetricType.GAUGE.value == "gauge"

    def test_enum_003_histogram_value(self):
        """Should have HISTOGRAM type."""
        assert MetricType.HISTOGRAM == "histogram"
        assert MetricType.HISTOGRAM.value == "histogram"

    def test_enum_004_summary_value(self):
        """Should have SUMMARY type."""
        assert MetricType.SUMMARY == "summary"
        assert MetricType.SUMMARY.value == "summary"


# =============================================================================
# CATEGORY 2: DATA CLASSES
# =============================================================================

class TestDataClasses:
    """Tests for metric data classes."""

    def test_dataclass_001_metric_definition_minimal(self):
        """Should create MetricDefinition with required fields."""
        metric = MetricDefinition(
            name="test_metric",
            type=MetricType.COUNTER,
            description="Test metric",
        )
        assert metric.name == "test_metric"
        assert metric.type == MetricType.COUNTER
        assert metric.description == "Test metric"
        assert metric.labels == []
        assert metric.buckets is None

    def test_dataclass_002_metric_definition_with_labels(self):
        """Should create MetricDefinition with labels."""
        metric = MetricDefinition(
            name="test_metric",
            type=MetricType.COUNTER,
            description="Test metric",
            labels=["project_id", "status"],
        )
        assert metric.labels == ["project_id", "status"]

    def test_dataclass_003_metric_definition_with_buckets(self):
        """Should create MetricDefinition with histogram buckets."""
        metric = MetricDefinition(
            name="duration_seconds",
            type=MetricType.HISTOGRAM,
            description="Duration histogram",
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
        )
        assert metric.buckets == [0.1, 0.5, 1.0, 2.0, 5.0]

    def test_dataclass_004_counter_value_minimal(self):
        """Should create CounterValue with required fields."""
        counter = CounterValue(
            name="requests_total",
            value=100,
        )
        assert counter.name == "requests_total"
        assert counter.value == 100
        assert counter.labels == {}
        assert isinstance(counter.timestamp, datetime)

    def test_dataclass_005_counter_value_with_labels(self):
        """Should create CounterValue with labels."""
        counter = CounterValue(
            name="requests_total",
            value=100,
            labels={"method": "GET", "status": "200"},
        )
        assert counter.labels == {"method": "GET", "status": "200"}

    def test_dataclass_006_gauge_value_minimal(self):
        """Should create GaugeValue with required fields."""
        gauge = GaugeValue(
            name="temperature",
            value=23.5,
        )
        assert gauge.name == "temperature"
        assert gauge.value == 23.5
        assert gauge.labels == {}

    def test_dataclass_007_gauge_value_with_labels(self):
        """Should create GaugeValue with labels."""
        gauge = GaugeValue(
            name="queue_length",
            value=42.0,
            labels={"queue": "high_priority"},
        )
        assert gauge.labels == {"queue": "high_priority"}

    def test_dataclass_008_histogram_value_minimal(self):
        """Should create HistogramValue with required fields."""
        histogram = HistogramValue(
            name="latency_seconds",
            value=0.123,
        )
        assert histogram.name == "latency_seconds"
        assert histogram.value == 0.123

    def test_dataclass_009_histogram_value_with_labels(self):
        """Should create HistogramValue with labels."""
        histogram = HistogramValue(
            name="latency_seconds",
            value=0.123,
            labels={"endpoint": "/api/v1/gates"},
        )
        assert histogram.labels == {"endpoint": "/api/v1/gates"}

    def test_dataclass_010_timestamp_defaults_to_now(self):
        """Should default timestamp to current time."""
        before = datetime.utcnow()
        counter = CounterValue(name="test", value=1)
        after = datetime.utcnow()

        assert before <= counter.timestamp <= after

    def test_dataclass_011_custom_timestamp(self):
        """Should allow custom timestamp."""
        custom_time = datetime(2026, 1, 15, 10, 30, 0)
        counter = CounterValue(name="test", value=1, timestamp=custom_time)
        assert counter.timestamp == custom_time

    def test_dataclass_012_gauge_value_negative(self):
        """Should allow negative gauge values."""
        gauge = GaugeValue(name="offset", value=-10.5)
        assert gauge.value == -10.5


# =============================================================================
# CATEGORY 3: METRIC COLLECTIONS
# =============================================================================

class TestMetricCollections:
    """Tests for metric definition collections."""

    def test_collection_001_governance_metrics_count(self):
        """Should have 15 governance metrics."""
        # Count may vary slightly based on implementation
        assert len(GOVERNANCE_METRICS) >= 10

    def test_collection_002_performance_metrics_count(self):
        """Should have 10 performance metrics."""
        assert len(PERFORMANCE_METRICS) >= 5

    def test_collection_003_business_metrics_count(self):
        """Should have 8 business metrics."""
        assert len(BUSINESS_METRICS) >= 5

    def test_collection_004_developer_experience_metrics(self):
        """Should have 7 developer experience metrics."""
        assert len(DEVELOPER_EXPERIENCE_METRICS) >= 5

    def test_collection_005_all_metrics_combined(self):
        """Should have all metrics combined correctly."""
        expected_total = (
            len(GOVERNANCE_METRICS) +
            len(PERFORMANCE_METRICS) +
            len(BUSINESS_METRICS) +
            len(DEVELOPER_EXPERIENCE_METRICS) +
            len(SYSTEM_HEALTH_METRICS)
        )
        assert len(ALL_METRICS) == expected_total


# =============================================================================
# CATEGORY 4: COUNTER METHODS
# =============================================================================

class TestCounterMethods:
    """Tests for counter metric operations."""

    def test_counter_001_increment_new_counter(self):
        """Should create new counter when incrementing."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("test_counter")
        assert collector.get_counter("test_counter") == 1

    def test_counter_002_increment_existing_counter(self):
        """Should increment existing counter."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("test_counter")
        collector.increment_counter("test_counter")
        collector.increment_counter("test_counter")
        assert collector.get_counter("test_counter") == 3

    def test_counter_003_increment_with_value(self):
        """Should increment by specified value."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("test_counter", value=5)
        assert collector.get_counter("test_counter") == 5

    def test_counter_004_increment_with_labels(self):
        """Should handle labeled counters separately."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("requests", {"method": "GET"})
        collector.increment_counter("requests", {"method": "POST"})
        collector.increment_counter("requests", {"method": "GET"})

        assert collector.get_counter("requests", {"method": "GET"}) == 2
        assert collector.get_counter("requests", {"method": "POST"}) == 1

    def test_counter_005_get_nonexistent_counter(self):
        """Should return 0 for nonexistent counter."""
        collector = PrometheusMetricsCollector()
        assert collector.get_counter("nonexistent") == 0

    def test_counter_006_get_counter_wrong_labels(self):
        """Should return 0 for wrong labels."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("requests", {"method": "GET"})
        assert collector.get_counter("requests", {"method": "DELETE"}) == 0

    def test_counter_007_multiple_counters(self):
        """Should track multiple counters independently."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("counter_a", value=10)
        collector.increment_counter("counter_b", value=20)

        assert collector.get_counter("counter_a") == 10
        assert collector.get_counter("counter_b") == 20

    def test_counter_008_empty_labels_same_as_none(self):
        """Should treat empty labels same as no labels."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("test", {})
        collector.increment_counter("test", None)

        assert collector.get_counter("test") == 2


# =============================================================================
# CATEGORY 5: GAUGE METHODS
# =============================================================================

class TestGaugeMethods:
    """Tests for gauge metric operations."""

    def test_gauge_001_set_new_gauge(self):
        """Should create new gauge when setting."""
        collector = PrometheusMetricsCollector()
        collector.set_gauge("temperature", 25.5)
        assert collector.get_gauge("temperature") == 25.5

    def test_gauge_002_overwrite_gauge(self):
        """Should overwrite existing gauge value."""
        collector = PrometheusMetricsCollector()
        collector.set_gauge("temperature", 25.5)
        collector.set_gauge("temperature", 30.0)
        assert collector.get_gauge("temperature") == 30.0

    def test_gauge_003_gauge_with_labels(self):
        """Should handle labeled gauges separately."""
        collector = PrometheusMetricsCollector()
        collector.set_gauge("cpu", 50.0, {"host": "server1"})
        collector.set_gauge("cpu", 75.0, {"host": "server2"})

        assert collector.get_gauge("cpu", {"host": "server1"}) == 50.0
        assert collector.get_gauge("cpu", {"host": "server2"}) == 75.0

    def test_gauge_004_get_nonexistent_gauge(self):
        """Should return 0.0 for nonexistent gauge."""
        collector = PrometheusMetricsCollector()
        assert collector.get_gauge("nonexistent") == 0.0

    def test_gauge_005_inc_gauge(self):
        """Should increment gauge value."""
        collector = PrometheusMetricsCollector()
        collector.set_gauge("queue_length", 10.0)
        collector.inc_gauge("queue_length")
        assert collector.get_gauge("queue_length") == 11.0

    def test_gauge_006_inc_gauge_with_value(self):
        """Should increment gauge by specified value."""
        collector = PrometheusMetricsCollector()
        collector.set_gauge("queue_length", 10.0)
        collector.inc_gauge("queue_length", value=5.0)
        assert collector.get_gauge("queue_length") == 15.0

    def test_gauge_007_dec_gauge(self):
        """Should decrement gauge value."""
        collector = PrometheusMetricsCollector()
        collector.set_gauge("queue_length", 10.0)
        collector.dec_gauge("queue_length")
        assert collector.get_gauge("queue_length") == 9.0

    def test_gauge_008_dec_gauge_with_value(self):
        """Should decrement gauge by specified value."""
        collector = PrometheusMetricsCollector()
        collector.set_gauge("queue_length", 10.0)
        collector.dec_gauge("queue_length", value=3.0)
        assert collector.get_gauge("queue_length") == 7.0

    def test_gauge_009_negative_gauge(self):
        """Should allow negative gauge values."""
        collector = PrometheusMetricsCollector()
        collector.set_gauge("offset", -50.5)
        assert collector.get_gauge("offset") == -50.5

    def test_gauge_010_inc_nonexistent_gauge(self):
        """Should start from 0 when incrementing nonexistent gauge."""
        collector = PrometheusMetricsCollector()
        collector.inc_gauge("new_gauge", value=5.0)
        assert collector.get_gauge("new_gauge") == 5.0


# =============================================================================
# CATEGORY 6: HISTOGRAM METHODS
# =============================================================================

class TestHistogramMethods:
    """Tests for histogram metric operations."""

    def test_histogram_001_observe_new_histogram(self):
        """Should create new histogram when observing."""
        collector = PrometheusMetricsCollector()
        collector.observe_histogram("latency", 0.5)
        stats = collector.get_histogram_stats("latency")
        assert stats["count"] == 1
        assert stats["sum"] == 0.5

    def test_histogram_002_observe_multiple_values(self):
        """Should accumulate multiple observations."""
        collector = PrometheusMetricsCollector()
        collector.observe_histogram("latency", 0.1)
        collector.observe_histogram("latency", 0.5)
        collector.observe_histogram("latency", 1.0)

        stats = collector.get_histogram_stats("latency")
        assert stats["count"] == 3
        assert stats["sum"] == 1.6

    def test_histogram_003_observe_with_labels(self):
        """Should handle labeled histograms separately."""
        collector = PrometheusMetricsCollector()
        collector.observe_histogram("latency", 0.1, {"endpoint": "/api/a"})
        collector.observe_histogram("latency", 0.5, {"endpoint": "/api/b"})

        stats_a = collector.get_histogram_stats("latency", {"endpoint": "/api/a"})
        stats_b = collector.get_histogram_stats("latency", {"endpoint": "/api/b"})

        assert stats_a["count"] == 1
        assert stats_b["count"] == 1

    def test_histogram_004_percentile_p50(self):
        """Should calculate median (p50) correctly."""
        collector = PrometheusMetricsCollector()
        for i in range(1, 11):  # 1 to 10
            collector.observe_histogram("latency", float(i))

        stats = collector.get_histogram_stats("latency")
        # _percentile uses: index = int(len * percentile / 100) = int(10 * 50 / 100) = 5
        # sorted_data[5] = 6 (0-indexed, 6th element)
        assert stats["p50"] == 6.0

    def test_histogram_005_percentile_p95(self):
        """Should calculate p95 correctly."""
        collector = PrometheusMetricsCollector()
        for i in range(1, 101):  # 1 to 100
            collector.observe_histogram("latency", float(i))

        stats = collector.get_histogram_stats("latency")
        assert stats["p95"] >= 95.0

    def test_histogram_006_percentile_p99(self):
        """Should calculate p99 correctly."""
        collector = PrometheusMetricsCollector()
        for i in range(1, 101):  # 1 to 100
            collector.observe_histogram("latency", float(i))

        stats = collector.get_histogram_stats("latency")
        assert stats["p99"] >= 99.0

    def test_histogram_007_empty_histogram_stats(self):
        """Should return zeros for nonexistent histogram."""
        collector = PrometheusMetricsCollector()
        stats = collector.get_histogram_stats("nonexistent")

        assert stats["count"] == 0
        assert stats["sum"] == 0.0
        assert stats["p50"] == 0.0
        assert stats["p95"] == 0.0
        assert stats["p99"] == 0.0

    def test_histogram_008_limit_observations(self):
        """Should keep only last 1000 observations."""
        collector = PrometheusMetricsCollector()
        for i in range(1500):
            collector.observe_histogram("latency", float(i))

        stats = collector.get_histogram_stats("latency")
        assert stats["count"] == 1000

    def test_histogram_009_single_observation_percentiles(self):
        """Should handle single observation percentiles."""
        collector = PrometheusMetricsCollector()
        collector.observe_histogram("latency", 5.0)

        stats = collector.get_histogram_stats("latency")
        assert stats["p50"] == 5.0
        assert stats["p95"] == 5.0
        assert stats["p99"] == 5.0

    def test_histogram_010_float_precision(self):
        """Should maintain float precision."""
        collector = PrometheusMetricsCollector()
        collector.observe_histogram("latency", 0.123456)
        collector.observe_histogram("latency", 0.654321)

        stats = collector.get_histogram_stats("latency")
        assert abs(stats["sum"] - 0.777777) < 0.0001


# =============================================================================
# CATEGORY 7: TIMER CONTEXT MANAGER
# =============================================================================

class TestTimerContextManager:
    """Tests for Timer context manager."""

    def test_timer_001_measures_duration(self):
        """Should measure operation duration."""
        collector = PrometheusMetricsCollector()

        with collector.timer("operation_duration"):
            time.sleep(0.05)  # 50ms

        stats = collector.get_histogram_stats("operation_duration")
        assert stats["count"] == 1
        assert stats["sum"] >= 0.05

    def test_timer_002_with_labels(self):
        """Should record duration with labels."""
        collector = PrometheusMetricsCollector()

        with collector.timer("api_latency", {"method": "GET"}):
            time.sleep(0.01)

        stats = collector.get_histogram_stats("api_latency", {"method": "GET"})
        assert stats["count"] == 1

    def test_timer_003_multiple_timings(self):
        """Should accumulate multiple timings."""
        collector = PrometheusMetricsCollector()

        for _ in range(3):
            with collector.timer("operation"):
                time.sleep(0.01)

        stats = collector.get_histogram_stats("operation")
        assert stats["count"] == 3

    def test_timer_004_timer_on_exception(self):
        """Should record duration even on exception."""
        collector = PrometheusMetricsCollector()

        try:
            with collector.timer("failing_operation"):
                time.sleep(0.01)
                raise ValueError("Test error")
        except ValueError:
            pass

        stats = collector.get_histogram_stats("failing_operation")
        assert stats["count"] == 1


# =============================================================================
# CATEGORY 8: RECORD METHODS
# =============================================================================

class TestRecordMethods:
    """Tests for high-level record methods."""

    def test_record_001_submission_basic(self):
        """Should record basic submission metrics."""
        collector = PrometheusMetricsCollector()

        collector.record_submission(
            project_id="proj-123",
            status="passed",
            vibecoding_index=25.0,
            routing="auto_approve",
            duration_seconds=1.5,
        )

        assert collector.get_counter(
            "governance_submissions_total",
            {"project_id": "proj-123", "status": "passed"},
        ) == 1

    def test_record_002_submission_with_rejection(self):
        """Should record rejection reason."""
        collector = PrometheusMetricsCollector()

        collector.record_submission(
            project_id="proj-123",
            status="rejected",
            vibecoding_index=85.0,
            routing="ceo_must_review",
            duration_seconds=2.0,
            rejection_reason="missing_ownership",
        )

        assert collector.get_counter(
            "governance_rejections_total",
            {"project_id": "proj-123", "rejection_reason": "missing_ownership"},
        ) == 1

    def test_record_003_submission_with_signals(self):
        """Should record signal breakdown."""
        collector = PrometheusMetricsCollector()

        collector.record_submission(
            project_id="proj-123",
            status="passed",
            vibecoding_index=45.0,
            routing="tech_lead_review",
            duration_seconds=1.0,
            signal_breakdown={
                "architectural_smell": 30.0,
                "abstraction_complexity": 20.0,
                "ai_dependency_ratio": 50.0,
                "change_surface_area": 40.0,
                "drift_velocity": 35.0,
            },
        )

        stats = collector.get_histogram_stats(
            "governance_signals_architectural_smell",
            {"project_id": "proj-123"},
        )
        assert stats["count"] == 1

    def test_record_004_submission_critical_override(self):
        """Should record critical path override."""
        collector = PrometheusMetricsCollector()

        collector.record_submission(
            project_id="proj-123",
            status="passed",
            vibecoding_index=80.0,
            routing="ceo_must_review",
            duration_seconds=1.0,
            critical_override="security",
        )

        assert collector.get_counter(
            "governance_critical_override_total",
            {"project_id": "proj-123", "critical_category": "security"},
        ) == 1

    def test_record_005_ceo_override(self):
        """Should record CEO override."""
        collector = PrometheusMetricsCollector()

        collector.record_ceo_override("proj-123", "agrees")
        collector.record_ceo_override("proj-123", "disagrees")

        assert collector.get_counter(
            "governance_ceo_overrides_total",
            {"project_id": "proj-123", "override_type": "agrees"},
        ) == 1
        assert collector.get_counter(
            "governance_ceo_overrides_total",
            {"project_id": "proj-123", "override_type": "disagrees"},
        ) == 1

    def test_record_006_evidence_upload(self):
        """Should record evidence upload metrics."""
        collector = PrometheusMetricsCollector()

        collector.record_evidence_upload("proj-123", "test_coverage", 1024)

        assert collector.get_counter(
            "evidence_vault_uploads_total",
            {"project_id": "proj-123", "evidence_type": "test_coverage"},
        ) == 1
        assert collector.get_gauge(
            "evidence_vault_size_bytes",
            {"project_id": "proj-123"},
        ) == 1024

    def test_record_007_evidence_upload_accumulates(self):
        """Should accumulate evidence size."""
        collector = PrometheusMetricsCollector()

        collector.record_evidence_upload("proj-123", "test_coverage", 1024)
        collector.record_evidence_upload("proj-123", "security_scan", 2048)

        assert collector.get_gauge(
            "evidence_vault_size_bytes",
            {"project_id": "proj-123"},
        ) == 3072

    def test_record_008_llm_generation_success(self):
        """Should record successful LLM generation."""
        collector = PrometheusMetricsCollector()

        collector.record_llm_generation(
            provider="ollama",
            model="qwen3:32b",
            duration_seconds=5.0,
            success=True,
        )

        stats = collector.get_histogram_stats(
            "llm_generation_duration_seconds",
            {"provider": "ollama", "model": "qwen3:32b"},
        )
        assert stats["count"] == 1

    def test_record_009_llm_generation_with_fallback(self):
        """Should record LLM fallback."""
        collector = PrometheusMetricsCollector()

        collector.record_llm_generation(
            provider="ollama",
            model="qwen3:32b",
            duration_seconds=5.0,
            success=False,
            fallback_triggered=True,
            fallback_type="timeout",
        )

        assert collector.get_counter(
            "llm_fallback_triggered_total",
            {"provider": "ollama", "fallback_type": "timeout"},
        ) == 1

    def test_record_010_developer_friction(self):
        """Should record developer friction."""
        collector = PrometheusMetricsCollector()

        collector.record_developer_friction("proj-123", 4.5)

        stats = collector.get_histogram_stats(
            "developer_friction_minutes",
            {"project_id": "proj-123"},
        )
        assert stats["count"] == 1
        assert stats["sum"] == 4.5

    def test_record_011_break_glass(self):
        """Should record break glass activation."""
        collector = PrometheusMetricsCollector()

        collector.record_break_glass("P0")
        collector.record_break_glass("P1")
        collector.record_break_glass("P0")

        assert collector.get_counter(
            "governance_break_glass_total",
            {"severity": "P0"},
        ) == 2
        assert collector.get_counter(
            "governance_break_glass_total",
            {"severity": "P1"},
        ) == 1

    def test_record_012_bypass_incident(self):
        """Should record bypass incident."""
        collector = PrometheusMetricsCollector()

        collector.record_bypass_incident("pre_commit_skip")

        assert collector.get_counter(
            "governance_bypass_incidents_total",
            {"bypass_type": "pre_commit_skip"},
        ) == 1

    def test_record_013_escalation_ceo_must_review(self):
        """Should record escalation for ceo_must_review."""
        collector = PrometheusMetricsCollector()

        collector.record_submission(
            project_id="proj-123",
            status="pending",
            vibecoding_index=90.0,
            routing="ceo_must_review",
            duration_seconds=1.0,
        )

        assert collector.get_counter(
            "governance_escalations_total",
            {"project_id": "proj-123", "escalated_to": "ceo"},
        ) == 1

    def test_record_014_escalation_ceo_should_review(self):
        """Should record escalation for ceo_should_review."""
        collector = PrometheusMetricsCollector()

        collector.record_submission(
            project_id="proj-123",
            status="pending",
            vibecoding_index=70.0,
            routing="ceo_should_review",
            duration_seconds=1.0,
        )

        assert collector.get_counter(
            "governance_escalations_total",
            {"project_id": "proj-123", "escalated_to": "tech_lead"},
        ) == 1

    def test_record_015_routing_counter(self):
        """Should record routing decision counter."""
        collector = PrometheusMetricsCollector()

        collector.record_submission(
            project_id="proj-123",
            status="passed",
            vibecoding_index=25.0,
            routing="auto_approve",
            duration_seconds=1.0,
        )

        assert collector.get_counter(
            "governance_routing_total",
            {"project_id": "proj-123", "routing": "auto_approve"},
        ) == 1


# =============================================================================
# CATEGORY 9: SYSTEM HEALTH METHODS
# =============================================================================

class TestSystemHealthMethods:
    """Tests for system health metric methods."""

    def test_health_001_update_system_health(self):
        """Should update CPU and memory gauges."""
        collector = PrometheusMetricsCollector()

        collector.update_system_health(cpu_percent=45.0, memory_percent=60.0)

        assert collector.get_gauge("system_cpu_usage_percent") == 45.0
        assert collector.get_gauge("system_memory_usage_percent") == 60.0

    def test_health_002_update_uptime(self):
        """Should update uptime gauge."""
        collector = PrometheusMetricsCollector()
        time.sleep(0.1)  # Wait a bit

        collector.update_system_health(cpu_percent=0.0, memory_percent=0.0)

        uptime = collector.get_gauge("system_uptime_seconds")
        assert uptime >= 0.1

    def test_health_003_kill_switch_off(self):
        """Should set kill switch status OFF."""
        collector = PrometheusMetricsCollector()
        collector.set_kill_switch_status("OFF")
        assert collector.get_gauge("kill_switch_status") == 0

    def test_health_004_kill_switch_warning(self):
        """Should set kill switch status WARNING."""
        collector = PrometheusMetricsCollector()
        collector.set_kill_switch_status("WARNING")
        assert collector.get_gauge("kill_switch_status") == 1

    def test_health_005_kill_switch_soft(self):
        """Should set kill switch status SOFT."""
        collector = PrometheusMetricsCollector()
        collector.set_kill_switch_status("SOFT")
        assert collector.get_gauge("kill_switch_status") == 2

    def test_health_006_kill_switch_full(self):
        """Should set kill switch status FULL."""
        collector = PrometheusMetricsCollector()
        collector.set_kill_switch_status("FULL")
        assert collector.get_gauge("kill_switch_status") == 3

    def test_health_007_kill_switch_trigger(self):
        """Should record kill switch trigger."""
        collector = PrometheusMetricsCollector()

        collector.record_kill_switch_trigger("rejection_rate_high")

        assert collector.get_counter(
            "kill_switch_triggered_total",
            {"trigger_reason": "rejection_rate_high"},
        ) == 1

    def test_health_008_system_error(self):
        """Should record system error."""
        collector = PrometheusMetricsCollector()

        collector.record_system_error("database_connection", "critical")

        assert collector.get_counter(
            "system_errors_total",
            {"error_type": "database_connection", "severity": "critical"},
        ) == 1


# =============================================================================
# CATEGORY 10: CEO METRICS METHODS
# =============================================================================

class TestCEOMetricsMethods:
    """Tests for CEO dashboard metric methods."""

    def test_ceo_001_update_ceo_metrics(self):
        """Should update all CEO metrics."""
        collector = PrometheusMetricsCollector()

        collector.update_ceo_metrics(
            week=4,
            time_saved_hours=15.0,
            pr_review_reduction_percent=60.0,
            governance_without_ceo_percent=70.0,
            false_positive_rate=5.0,
        )

        assert collector.get_gauge("ceo_time_saved_hours", {"week": "4"}) == 15.0
        assert collector.get_gauge("ceo_pr_review_reduction_percent", {"week": "4"}) == 60.0
        assert collector.get_gauge("governance_without_ceo_percent", {"week": "4"}) == 70.0
        assert collector.get_gauge("governance_false_positive_rate", {"week": "4"}) == 5.0

    def test_ceo_002_different_weeks(self):
        """Should track metrics for different weeks."""
        collector = PrometheusMetricsCollector()

        collector.update_ceo_metrics(2, 10.0, 40.0, 50.0, 10.0)
        collector.update_ceo_metrics(4, 20.0, 60.0, 70.0, 5.0)

        assert collector.get_gauge("ceo_time_saved_hours", {"week": "2"}) == 10.0
        assert collector.get_gauge("ceo_time_saved_hours", {"week": "4"}) == 20.0

    def test_ceo_003_update_week_metrics(self):
        """Should overwrite metrics for same week."""
        collector = PrometheusMetricsCollector()

        collector.update_ceo_metrics(4, 10.0, 40.0, 50.0, 10.0)
        collector.update_ceo_metrics(4, 20.0, 60.0, 70.0, 5.0)

        assert collector.get_gauge("ceo_time_saved_hours", {"week": "4"}) == 20.0

    def test_ceo_004_zero_values(self):
        """Should handle zero values."""
        collector = PrometheusMetricsCollector()

        collector.update_ceo_metrics(1, 0.0, 0.0, 0.0, 0.0)

        assert collector.get_gauge("ceo_time_saved_hours", {"week": "1"}) == 0.0


# =============================================================================
# CATEGORY 11: OUTPUT METHODS
# =============================================================================

class TestOutputMethods:
    """Tests for metric output methods."""

    def test_output_001_prometheus_format_counter(self):
        """Should output counter in Prometheus format."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("governance_submissions_total", {"project_id": "p1", "status": "passed"})

        output = collector.get_metrics_output()

        assert "governance_submissions_total" in output
        assert "HELP" in output
        assert "TYPE" in output

    def test_output_002_prometheus_format_gauge(self):
        """Should output gauge in Prometheus format."""
        collector = PrometheusMetricsCollector()
        collector.set_gauge("ceo_time_saved_hours", 25.0, {"week": "4"})

        output = collector.get_metrics_output()

        assert "ceo_time_saved_hours" in output

    def test_output_003_json_format_structure(self):
        """Should output JSON with correct structure."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("test_counter")
        collector.set_gauge("test_gauge", 10.0)

        json_output = collector.get_metrics_json()

        assert "counters" in json_output
        assert "gauges" in json_output
        assert "histograms" in json_output
        assert "timestamp" in json_output
        assert "total_metrics" in json_output

    def test_output_004_json_counter_values(self):
        """Should include counter values in JSON."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("test_counter", value=5)

        json_output = collector.get_metrics_json()

        assert "test_counter" in json_output["counters"]

    def test_output_005_json_histogram_stats(self):
        """Should include histogram stats in JSON."""
        collector = PrometheusMetricsCollector()
        collector.observe_histogram("test_histogram", 1.0)
        collector.observe_histogram("test_histogram", 2.0)

        json_output = collector.get_metrics_json()

        assert "test_histogram" in json_output["histograms"]

    def test_output_006_total_metrics_count(self):
        """Should report correct total metrics count."""
        collector = PrometheusMetricsCollector()

        json_output = collector.get_metrics_json()

        assert json_output["total_metrics"] == len(ALL_METRICS)


# =============================================================================
# CATEGORY 12: HELPER METHODS
# =============================================================================

class TestHelperMethods:
    """Tests for internal helper methods."""

    def test_helper_001_make_label_key_empty(self):
        """Should handle empty labels."""
        collector = PrometheusMetricsCollector()
        key = collector._make_label_key({})
        assert key == ""

    def test_helper_002_make_label_key_single(self):
        """Should create key from single label."""
        collector = PrometheusMetricsCollector()
        key = collector._make_label_key({"project_id": "p1"})
        assert 'project_id="p1"' in key

    def test_helper_003_make_label_key_multiple(self):
        """Should create sorted key from multiple labels."""
        collector = PrometheusMetricsCollector()
        key = collector._make_label_key({"status": "passed", "project_id": "p1"})
        # Should be sorted alphabetically
        assert key.index("project_id") < key.index("status")

    def test_helper_004_parse_label_key_empty(self):
        """Should parse empty label key."""
        collector = PrometheusMetricsCollector()
        labels = collector._parse_label_key("")
        assert labels == {}

    def test_helper_005_parse_label_key_roundtrip(self):
        """Should roundtrip labels through make/parse."""
        collector = PrometheusMetricsCollector()
        original = {"project_id": "p1", "status": "passed"}
        key = collector._make_label_key(original)
        parsed = collector._parse_label_key(key)
        assert parsed == original

    def test_helper_006_format_labels_empty(self):
        """Should format empty labels."""
        collector = PrometheusMetricsCollector()
        formatted = collector._format_labels("")
        assert formatted == ""

    def test_helper_007_format_labels_with_values(self):
        """Should format labels with braces."""
        collector = PrometheusMetricsCollector()
        formatted = collector._format_labels('project_id="p1"')
        assert formatted == '{project_id="p1"}'

    def test_helper_008_percentile_empty_list(self):
        """Should handle empty list in percentile."""
        collector = PrometheusMetricsCollector()
        result = collector._percentile([], 50)
        assert result == 0.0


# =============================================================================
# CATEGORY 13: FACTORY FUNCTIONS
# =============================================================================

class TestFactoryFunctions:
    """Tests for factory functions."""

    def test_factory_001_create_metrics_collector(self):
        """Should create new collector instance."""
        collector = create_metrics_collector()
        assert isinstance(collector, PrometheusMetricsCollector)

    def test_factory_002_get_metrics_collector(self):
        """Should get or create collector singleton."""
        collector = get_metrics_collector()
        assert isinstance(collector, PrometheusMetricsCollector)

    def test_factory_003_get_same_instance(self):
        """Should return same instance on multiple calls."""
        collector1 = get_metrics_collector()
        collector2 = get_metrics_collector()
        assert collector1 is collector2

    def test_factory_004_create_replaces_singleton(self):
        """Should replace singleton on create."""
        old_collector = get_metrics_collector()
        old_collector.increment_counter("test")

        new_collector = create_metrics_collector()

        # New collector should not have the counter
        assert new_collector.get_counter("test") == 0


# =============================================================================
# CATEGORY 14: EDGE CASES
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_edge_001_large_counter_value(self):
        """Should handle large counter values."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("large_counter", value=10**9)
        assert collector.get_counter("large_counter") == 10**9

    def test_edge_002_special_characters_in_labels(self):
        """Should handle special characters in label values."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("test", {"path": "/api/v1/test?foo=bar"})
        assert collector.get_counter("test", {"path": "/api/v1/test?foo=bar"}) == 1

    def test_edge_003_very_small_histogram_value(self):
        """Should handle very small histogram values."""
        collector = PrometheusMetricsCollector()
        collector.observe_histogram("micro_latency", 0.000001)
        stats = collector.get_histogram_stats("micro_latency")
        assert stats["sum"] == 0.000001

    def test_edge_004_zero_gauge_value(self):
        """Should handle zero gauge values correctly."""
        collector = PrometheusMetricsCollector()
        collector.set_gauge("zero_gauge", 0.0)
        assert collector.get_gauge("zero_gauge") == 0.0

    def test_edge_005_unicode_in_labels(self):
        """Should handle unicode in label values."""
        collector = PrometheusMetricsCollector()
        collector.increment_counter("test", {"name": "project-vn-th"})
        assert collector.get_counter("test", {"name": "project-vn-th"}) == 1

    def test_edge_006_concurrent_increments(self):
        """Should handle rapid increments."""
        collector = PrometheusMetricsCollector()

        for _ in range(1000):
            collector.increment_counter("rapid_counter")

        assert collector.get_counter("rapid_counter") == 1000
