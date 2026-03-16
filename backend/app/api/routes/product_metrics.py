"""
Product Metrics API — Sprint 226, ADR-071 D-071-05.

Admin-only endpoints for Option 5 pilot validation metrics:
  - GET /product-metrics/baseline — time-to-gate baseline (collect BEFORE pilot)
  - GET /product-metrics/current — live metrics (completion, override, retention)

Kill signal: completion <50% OR retention <2/3 after Week 2 → stop.
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.services.product_metrics_service import ProductMetricsService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/product-metrics",
    tags=["Product Metrics"],
)


@router.get("/baseline")
async def get_baseline(
    project_id: Optional[UUID] = Query(None, description="Filter by project (default: all)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Collect time-to-gate baseline metrics.

    Must be run BEFORE pilot begins to establish comparison baseline.
    Returns average/min/max seconds from gate evaluated_at → approved_at per gate type.
    """
    svc = ProductMetricsService(db)
    return await svc.time_to_gate_baseline(project_id)


@router.get("/current")
async def get_current_metrics(
    date_from: Optional[date] = Query(None, description="Start date (default: all time)"),
    date_to: Optional[date] = Query(None, description="End date (default: now)"),
    tier: Optional[str] = Query(None, description="Filter override rate by tier (e.g. STANDARD)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get current product metrics for pilot validation.

    Returns all 4 metrics from ADR-071 D-071-05:
    - conversation_completion_rate (target ≥70%, kill <50%)
    - human_override_rate (target ≤30% at STANDARD)
    - time_to_gate (current vs baseline)
    - pilot_retention (target 3/3, kill <2/3)
    """
    svc = ProductMetricsService(db)

    dt_from = datetime.combine(date_from, datetime.min.time()).replace(tzinfo=timezone.utc) if date_from else None
    dt_to = datetime.combine(date_to, datetime.max.time()).replace(tzinfo=timezone.utc) if date_to else None

    completion = await svc.conversation_completion_rate(dt_from, dt_to)
    override = await svc.human_override_rate(tier, dt_from, dt_to)
    retention = await svc.pilot_retention(dt_from)
    baseline = await svc.time_to_gate_baseline()

    # Aggregate kill signal check
    any_kill = completion.get("kill_signal", False) or retention.get("kill_signal", False)

    return {
        "period": {"from": str(date_from), "to": str(date_to)},
        "conversation_completion": completion,
        "human_override": override,
        "pilot_retention": retention,
        "time_to_gate_baseline": baseline,
        "kill_signal": any_kill,
        "kill_reason": (
            "completion_rate < 50%" if completion.get("kill_signal") else
            "retention < 2/3" if retention.get("kill_signal") else
            None
        ),
    }
