"""
=========================================================================
Governance Metrics API Routes - Prometheus Metrics Exposition
SDLC Orchestrator - Sprint 110 (CEO Dashboard & Observability)

Version: 1.0.0
Date: January 27, 2026
Status: ACTIVE - Sprint 110 Day 3
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 Quality Assurance System

Endpoints:
- GET /governance-metrics - Prometheus text format
- GET /governance-metrics/json - JSON format
- GET /governance-metrics/health - Metrics service health
- POST /governance-metrics/record-submission - Record submission
- POST /governance-metrics/record-ceo-override - Record override
- POST /governance-metrics/record-evidence - Record evidence upload
- POST /governance-metrics/record-llm - Record LLM generation
- POST /governance-metrics/update-system-health - Update health gauges
- POST /governance-metrics/update-ceo-metrics - Update CEO metrics

Zero Mock Policy: Real Prometheus metrics
=========================================================================
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, Field

from app.services.governance.metrics_collector import (
    PrometheusMetricsCollector,
    get_metrics_collector,
    ALL_METRICS,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/governance-metrics")


# ============================================================================
# Request Models
# ============================================================================


class RecordSubmissionRequest(BaseModel):
    """Request model for recording a submission."""

    project_id: str
    status: str = Field(..., description="passed, rejected, or pending")
    vibecoding_index: float = Field(..., ge=0, le=100)
    routing: str = Field(..., description="auto_approve, tech_lead_review, ceo_should_review, ceo_must_review")
    duration_seconds: float = Field(..., ge=0)
    signal_breakdown: Optional[Dict[str, float]] = None
    rejection_reason: Optional[str] = None
    critical_override: Optional[str] = None


class RecordCEOOverrideRequest(BaseModel):
    """Request model for recording a CEO override."""

    project_id: str
    override_type: str = Field(..., description="agrees or disagrees")


class RecordEvidenceRequest(BaseModel):
    """Request model for recording evidence upload."""

    project_id: str
    evidence_type: str
    size_bytes: int = Field(..., ge=0)


class RecordLLMRequest(BaseModel):
    """Request model for recording LLM generation."""

    provider: str
    model: str
    duration_seconds: float = Field(..., ge=0)
    success: bool
    fallback_triggered: bool = False
    fallback_type: Optional[str] = None


class UpdateSystemHealthRequest(BaseModel):
    """Request model for updating system health."""

    cpu_percent: float = Field(..., ge=0, le=100)
    memory_percent: float = Field(..., ge=0, le=100)


class UpdateCEOMetricsRequest(BaseModel):
    """Request model for updating CEO metrics."""

    week: int = Field(..., ge=1, le=52)
    time_saved_hours: float = Field(..., ge=0)
    pr_review_reduction_percent: float = Field(..., ge=0, le=100)
    governance_without_ceo_percent: float = Field(..., ge=0, le=100)
    false_positive_rate: float = Field(..., ge=0, le=100)


class SetKillSwitchRequest(BaseModel):
    """Request model for setting kill switch status."""

    status: str = Field(..., description="OFF, WARNING, SOFT, or FULL")


class RecordDeveloperFrictionRequest(BaseModel):
    """Request model for recording developer friction."""

    project_id: str
    friction_minutes: float = Field(..., ge=0)


class RecordBreakGlassRequest(BaseModel):
    """Request model for recording break glass activation."""

    severity: str = Field(..., description="P0, P1, or abuse")


class RecordBypassRequest(BaseModel):
    """Request model for recording bypass incident."""

    bypass_type: str = Field(..., description="pre_commit_skip, direct_push, or break_glass_abuse")


# ============================================================================
# Endpoints
# ============================================================================


@router.get(
    "",
    summary="Get Prometheus metrics",
    description="""
    Get all governance metrics in Prometheus text exposition format.

    **Metric Categories (45 total):**
    1. Governance System (15 metrics)
    2. Performance (10 metrics)
    3. Business / CEO Dashboard (8 metrics)
    4. Developer Experience (7 metrics)
    5. System Health (5 metrics)

    **Response Format:**
    ```
    # HELP governance_submissions_total Total number of governance submissions
    # TYPE governance_submissions_total counter
    governance_submissions_total{project_id="proj-123",status="passed"} 150
    ```

    Use with Prometheus scrape config:
    ```yaml
    scrape_configs:
      - job_name: 'sdlc-orchestrator'
        static_configs:
          - targets: ['localhost:8000']
        metrics_path: '/api/v1/governance-metrics'
    ```
    """,
    response_class=Response,
)
async def get_metrics(
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Response:
    """Get metrics in Prometheus text format."""
    try:
        metrics_output = collector.get_metrics_output()

        return Response(
            content=metrics_output,
            media_type="text/plain; version=0.0.4; charset=utf-8",
        )

    except Exception as e:
        logger.error(f"Failed to get metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get metrics: {str(e)}",
        )


@router.get(
    "/json",
    summary="Get metrics in JSON format",
    description="""
    Get all governance metrics in JSON format.

    **Structure:**
    ```json
    {
      "counters": {"metric_name": {"labels": value}},
      "gauges": {"metric_name": {"labels": value}},
      "histograms": {"metric_name": {"labels": {stats}}},
      "timestamp": "2026-01-27T...",
      "total_metrics": 45
    }
    ```

    Useful for:
    - Custom dashboards
    - API integrations
    - Debugging
    """,
)
async def get_metrics_json(
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Dict[str, Any]:
    """Get metrics in JSON format."""
    try:
        return collector.get_metrics_json()

    except Exception as e:
        logger.error(f"Failed to get metrics JSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get metrics JSON: {str(e)}",
        )


@router.get(
    "/definitions",
    summary="Get metric definitions",
    description="""
    Get all metric definitions with descriptions and types.

    Useful for documentation and understanding available metrics.
    """,
)
async def get_metric_definitions() -> Dict[str, Any]:
    """Get metric definitions."""
    definitions = []

    for metric in ALL_METRICS:
        definitions.append({
            "name": metric.name,
            "type": metric.type.value,
            "description": metric.description,
            "labels": metric.labels,
            "buckets": metric.buckets,
        })

    return {
        "total": len(definitions),
        "categories": {
            "governance_system": 15,
            "performance": 10,
            "business_ceo_dashboard": 8,
            "developer_experience": 7,
            "system_health": 5,
        },
        "definitions": definitions,
    }


@router.get(
    "/health",
    summary="Metrics service health check",
    description="Check health of the metrics collector service.",
)
async def metrics_health(
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Dict[str, Any]:
    """Health check for metrics service."""
    return {
        "status": "healthy",
        "service": "prometheus_metrics_collector",
        "timestamp": datetime.utcnow().isoformat(),
        "metrics_count": len(ALL_METRICS),
        "counters_active": len(collector._counters),
        "gauges_active": len(collector._gauges),
        "histograms_active": len(collector._histograms),
    }


@router.post(
    "/record-submission",
    summary="Record governance submission metrics",
    description="""
    Record a governance submission with all related metrics.

    **Metrics Updated:**
    - governance_submissions_total
    - governance_submissions_duration_seconds
    - governance_vibecoding_index
    - governance_routing_total
    - governance_rejections_total (if rejected)
    - governance_signals_* (if signal_breakdown provided)
    - governance_critical_override_total (if critical override)
    - governance_escalations_total (if Orange/Red)
    """,
)
async def record_submission(
    request: RecordSubmissionRequest,
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Dict[str, Any]:
    """Record a governance submission."""
    try:
        collector.record_submission(
            project_id=request.project_id,
            status=request.status,
            vibecoding_index=request.vibecoding_index,
            routing=request.routing,
            duration_seconds=request.duration_seconds,
            signal_breakdown=request.signal_breakdown,
            rejection_reason=request.rejection_reason,
            critical_override=request.critical_override,
        )

        return {
            "status": "recorded",
            "project_id": request.project_id,
            "routing": request.routing,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to record submission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record submission: {str(e)}",
        )


@router.post(
    "/record-ceo-override",
    summary="Record CEO override",
    description="""
    Record a CEO override for calibration tracking.

    **Override Types:**
    - agrees: CEO confirms the routing was correct
    - disagrees: CEO disagrees (false positive/negative)

    **Metrics Updated:**
    - governance_ceo_overrides_total
    """,
)
async def record_ceo_override(
    request: RecordCEOOverrideRequest,
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Dict[str, Any]:
    """Record a CEO override."""
    try:
        if request.override_type not in ("agrees", "disagrees"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="override_type must be 'agrees' or 'disagrees'",
            )

        collector.record_ceo_override(
            project_id=request.project_id,
            override_type=request.override_type,
        )

        return {
            "status": "recorded",
            "override_type": request.override_type,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to record CEO override: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record CEO override: {str(e)}",
        )


@router.post(
    "/record-evidence",
    summary="Record evidence upload",
    description="""
    Record an evidence upload.

    **Metrics Updated:**
    - evidence_vault_uploads_total
    - evidence_vault_size_bytes
    """,
)
async def record_evidence(
    request: RecordEvidenceRequest,
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Dict[str, Any]:
    """Record an evidence upload."""
    try:
        collector.record_evidence_upload(
            project_id=request.project_id,
            evidence_type=request.evidence_type,
            size_bytes=request.size_bytes,
        )

        return {
            "status": "recorded",
            "evidence_type": request.evidence_type,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to record evidence: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record evidence: {str(e)}",
        )


@router.post(
    "/record-llm",
    summary="Record LLM generation metrics",
    description="""
    Record LLM generation metrics.

    **Metrics Updated:**
    - llm_generation_duration_seconds
    - llm_generation_success_rate
    - llm_fallback_triggered_total (if fallback)
    """,
)
async def record_llm(
    request: RecordLLMRequest,
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Dict[str, Any]:
    """Record LLM generation metrics."""
    try:
        collector.record_llm_generation(
            provider=request.provider,
            model=request.model,
            duration_seconds=request.duration_seconds,
            success=request.success,
            fallback_triggered=request.fallback_triggered,
            fallback_type=request.fallback_type,
        )

        return {
            "status": "recorded",
            "provider": request.provider,
            "model": request.model,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to record LLM metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record LLM metrics: {str(e)}",
        )


@router.post(
    "/update-system-health",
    summary="Update system health metrics",
    description="""
    Update system health gauges.

    **Metrics Updated:**
    - system_uptime_seconds
    - system_cpu_usage_percent
    - system_memory_usage_percent
    """,
)
async def update_system_health(
    request: UpdateSystemHealthRequest,
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Dict[str, Any]:
    """Update system health metrics."""
    try:
        collector.update_system_health(
            cpu_percent=request.cpu_percent,
            memory_percent=request.memory_percent,
        )

        return {
            "status": "updated",
            "cpu_percent": request.cpu_percent,
            "memory_percent": request.memory_percent,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to update system health: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update system health: {str(e)}",
        )


@router.post(
    "/update-ceo-metrics",
    summary="Update CEO dashboard metrics",
    description="""
    Update CEO dashboard metrics.

    **Metrics Updated:**
    - ceo_time_saved_hours
    - ceo_pr_review_reduction_percent
    - governance_without_ceo_percent
    - governance_false_positive_rate
    """,
)
async def update_ceo_metrics(
    request: UpdateCEOMetricsRequest,
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Dict[str, Any]:
    """Update CEO dashboard metrics."""
    try:
        collector.update_ceo_metrics(
            week=request.week,
            time_saved_hours=request.time_saved_hours,
            pr_review_reduction_percent=request.pr_review_reduction_percent,
            governance_without_ceo_percent=request.governance_without_ceo_percent,
            false_positive_rate=request.false_positive_rate,
        )

        return {
            "status": "updated",
            "week": request.week,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to update CEO metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update CEO metrics: {str(e)}",
        )


@router.post(
    "/set-kill-switch",
    summary="Set kill switch status",
    description="""
    Set kill switch status gauge.

    **Statuses:**
    - OFF: No enforcement (0)
    - WARNING: Log only (1)
    - SOFT: Block critical (2)
    - FULL: Block all (3)

    **Metrics Updated:**
    - kill_switch_status
    """,
)
async def set_kill_switch(
    request: SetKillSwitchRequest,
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Dict[str, Any]:
    """Set kill switch status."""
    try:
        valid_statuses = ["OFF", "WARNING", "SOFT", "FULL"]
        if request.status.upper() not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"status must be one of: {valid_statuses}",
            )

        collector.set_kill_switch_status(request.status)

        return {
            "status": "set",
            "kill_switch_status": request.status.upper(),
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to set kill switch: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set kill switch: {str(e)}",
        )


@router.post(
    "/record-developer-friction",
    summary="Record developer friction",
    description="""
    Record developer friction (time to pass governance).

    **Target:** <5 minutes (P95)

    **Metrics Updated:**
    - developer_friction_minutes
    """,
)
async def record_developer_friction(
    request: RecordDeveloperFrictionRequest,
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Dict[str, Any]:
    """Record developer friction."""
    try:
        collector.record_developer_friction(
            project_id=request.project_id,
            friction_minutes=request.friction_minutes,
        )

        return {
            "status": "recorded",
            "friction_minutes": request.friction_minutes,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to record developer friction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record developer friction: {str(e)}",
        )


@router.post(
    "/record-break-glass",
    summary="Record break glass activation",
    description="""
    Record break glass activation.

    **Severities:**
    - P0: Production critical (justified)
    - P1: High priority (justified)
    - abuse: Unjustified use

    **Metrics Updated:**
    - governance_break_glass_total
    """,
)
async def record_break_glass(
    request: RecordBreakGlassRequest,
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Dict[str, Any]:
    """Record break glass activation."""
    try:
        valid_severities = ["P0", "P1", "abuse"]
        if request.severity not in valid_severities:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"severity must be one of: {valid_severities}",
            )

        collector.record_break_glass(severity=request.severity)

        return {
            "status": "recorded",
            "severity": request.severity,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to record break glass: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record break glass: {str(e)}",
        )


@router.post(
    "/record-bypass",
    summary="Record governance bypass incident",
    description="""
    Record governance bypass incident.

    **Bypass Types:**
    - pre_commit_skip: Skipped pre-commit hook
    - direct_push: Direct push to protected branch
    - break_glass_abuse: Abuse of break glass

    **Target:** 0 incidents

    **Metrics Updated:**
    - governance_bypass_incidents_total
    """,
)
async def record_bypass(
    request: RecordBypassRequest,
    collector: PrometheusMetricsCollector = Depends(get_metrics_collector),
) -> Dict[str, Any]:
    """Record governance bypass incident."""
    try:
        valid_types = ["pre_commit_skip", "direct_push", "break_glass_abuse"]
        if request.bypass_type not in valid_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"bypass_type must be one of: {valid_types}",
            )

        collector.record_bypass_incident(bypass_type=request.bypass_type)

        return {
            "status": "recorded",
            "bypass_type": request.bypass_type,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to record bypass: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record bypass: {str(e)}",
        )
