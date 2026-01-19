"""
Codegen Cost Tracking Service - Sprint 48.

Tracks and reports AI code generation costs for budget management.
Target: <$50/month infrastructure cost per project (Founder Plan).

SDLC Stage: 04 - BUILD
Sprint: 48 - Quality Gates + Ollama Optimization + MVP Hardening
Framework: SDLC 5.1.3
Epic: EP-06 IR-Based Vietnamese SME Codegen

Features:
- Log individual generation requests with token usage
- Aggregate daily/monthly cost summaries
- Budget alerts and tracking
- Provider health monitoring
- Cost estimation before generation

Author: Backend Lead
Date: December 23, 2025
Status: ACTIVE
"""

import hashlib
import logging
import uuid
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session

from app.models.codegen_usage import (
    CodegenUsageLog,
    CodegenDailySummary,
    CodegenMonthlyCost,
    CodegenProviderHealth,
    GenerationStatus,
    QualityGateStatus,
)
from .base_provider import CodegenSpec, CodegenResult, CostEstimate

logger = logging.getLogger(__name__)


# Provider cost rates (USD per 1K tokens)
PROVIDER_COSTS = {
    "ollama": {
        "input": Decimal("0.0001"),   # ~$0.0001 per 1K input tokens (electricity only)
        "output": Decimal("0.0002"),  # ~$0.0002 per 1K output tokens
    },
    "claude": {
        "input": Decimal("0.003"),    # Claude 3.5 Sonnet pricing
        "output": Decimal("0.015"),
    },
    "deepcode": {
        "input": Decimal("0.005"),    # Estimated
        "output": Decimal("0.020"),
    },
}

# Default budget per project (Founder Plan)
DEFAULT_MONTHLY_BUDGET_USD = Decimal("50.00")


class CostTrackingService:
    """
    Service for tracking and reporting codegen costs.

    Provides:
    - Request logging with token usage
    - Cost calculation per provider
    - Daily/monthly aggregation
    - Budget monitoring
    - Cost reports
    """

    def __init__(self, db: Session):
        """
        Initialize cost tracking service.

        Args:
            db: Database session
        """
        self.db = db

    def log_generation_request(
        self,
        request_id: str,
        spec: CodegenSpec,
        user_id: Optional[uuid.UUID] = None,
        project_id: Optional[uuid.UUID] = None,
    ) -> CodegenUsageLog:
        """
        Log a new generation request (before generation starts).

        Args:
            request_id: Unique request ID
            spec: CodegenSpec for the request
            user_id: Optional user ID
            project_id: Optional project ID

        Returns:
            Created CodegenUsageLog record
        """
        # Calculate blueprint hash for deduplication
        blueprint_json = str(spec.app_blueprint)
        blueprint_hash = hashlib.sha256(blueprint_json.encode()).hexdigest()[:16]

        log = CodegenUsageLog(
            request_id=request_id,
            user_id=user_id,
            project_id=project_id,
            provider="pending",  # Will be updated when generation starts
            status=GenerationStatus.PENDING.value,
            language=spec.language,
            framework=spec.framework,
            target_module=spec.target_module,
            blueprint_name=spec.app_blueprint.get("name"),
            blueprint_hash=blueprint_hash,
            blueprint_size_bytes=len(blueprint_json),
        )

        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        logger.info(f"Logged generation request: {request_id}")
        return log

    def update_generation_start(
        self,
        request_id: str,
        provider: str,
        model: Optional[str] = None,
        estimated_cost: Optional[CostEstimate] = None,
    ) -> Optional[CodegenUsageLog]:
        """
        Update log when generation starts.

        Args:
            request_id: Request ID
            provider: Provider being used
            model: Model name (if known)
            estimated_cost: Pre-generation cost estimate

        Returns:
            Updated log or None if not found
        """
        log = self.db.query(CodegenUsageLog).filter(
            CodegenUsageLog.request_id == request_id
        ).first()

        if not log:
            logger.warning(f"Log not found for request: {request_id}")
            return None

        log.provider = provider
        log.model = model
        log.status = GenerationStatus.IN_PROGRESS.value

        if estimated_cost:
            log.estimated_cost_usd = Decimal(str(estimated_cost.estimated_cost_usd))

        self.db.commit()
        self.db.refresh(log)

        return log

    def update_generation_complete(
        self,
        request_id: str,
        result: CodegenResult,
        quality_passed: bool = True,
        quality_errors: int = 0,
        quality_warnings: int = 0,
        quality_blocked: bool = False,
    ) -> Optional[CodegenUsageLog]:
        """
        Update log when generation completes.

        Args:
            request_id: Request ID
            result: CodegenResult from provider
            quality_passed: Whether quality gates passed
            quality_errors: Number of quality errors
            quality_warnings: Number of quality warnings
            quality_blocked: Whether blocked by quality gates

        Returns:
            Updated log or None if not found
        """
        log = self.db.query(CodegenUsageLog).filter(
            CodegenUsageLog.request_id == request_id
        ).first()

        if not log:
            logger.warning(f"Log not found for request: {request_id}")
            return None

        # Update token usage
        metadata = result.metadata or {}
        log.prompt_tokens = metadata.get("prompt_tokens", 0)
        log.completion_tokens = metadata.get("completion_tokens", 0)
        log.total_tokens = result.tokens_used

        # Calculate actual cost
        actual_cost = self._calculate_cost(
            provider=result.provider,
            prompt_tokens=log.prompt_tokens,
            completion_tokens=log.completion_tokens,
        )
        log.actual_cost_usd = actual_cost

        # Update performance metrics
        log.generation_time_ms = result.generation_time_ms
        log.model = metadata.get("model", log.model)

        # Update output metrics
        log.files_generated = len(result.files)
        log.total_lines_generated = sum(
            content.count("\n") + 1 for content in result.files.values()
        )
        log.output_size_bytes = sum(
            len(content.encode("utf-8")) for content in result.files.values()
        )

        # Update quality gate results
        if quality_blocked:
            log.status = GenerationStatus.BLOCKED.value
        else:
            log.status = GenerationStatus.COMPLETED.value

        log.quality_gate_status = (
            QualityGateStatus.PASSED.value if quality_passed
            else QualityGateStatus.FAILED.value
        )
        log.quality_errors = quality_errors
        log.quality_warnings = quality_warnings
        log.quality_blocked = quality_blocked

        log.completed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(log)

        logger.info(
            f"Generation complete: {request_id} "
            f"tokens={log.total_tokens} cost=${log.actual_cost_usd:.6f}"
        )

        return log

    def update_generation_failed(
        self,
        request_id: str,
        error_message: str,
        error_type: Optional[str] = None,
    ) -> Optional[CodegenUsageLog]:
        """
        Update log when generation fails.

        Args:
            request_id: Request ID
            error_message: Error message
            error_type: Error type/category

        Returns:
            Updated log or None if not found
        """
        log = self.db.query(CodegenUsageLog).filter(
            CodegenUsageLog.request_id == request_id
        ).first()

        if not log:
            return None

        log.status = GenerationStatus.FAILED.value
        log.error_message = error_message
        log.error_type = error_type
        log.completed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(log)

        logger.warning(f"Generation failed: {request_id} - {error_message}")
        return log

    def _calculate_cost(
        self,
        provider: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> Decimal:
        """Calculate cost for token usage."""
        rates = PROVIDER_COSTS.get(provider, PROVIDER_COSTS["ollama"])

        input_cost = (Decimal(prompt_tokens) / 1000) * rates["input"]
        output_cost = (Decimal(completion_tokens) / 1000) * rates["output"]

        return input_cost + output_cost

    def get_daily_summary(
        self,
        target_date: date,
        user_id: Optional[uuid.UUID] = None,
        project_id: Optional[uuid.UUID] = None,
    ) -> Dict[str, Any]:
        """
        Get daily usage summary.

        Args:
            target_date: Date to get summary for
            user_id: Optional filter by user
            project_id: Optional filter by project

        Returns:
            Daily summary dict
        """
        start_dt = datetime.combine(target_date, datetime.min.time())
        end_dt = datetime.combine(target_date + timedelta(days=1), datetime.min.time())

        # Build query filters
        filters = [
            CodegenUsageLog.created_at >= start_dt,
            CodegenUsageLog.created_at < end_dt,
        ]
        if user_id:
            filters.append(CodegenUsageLog.user_id == user_id)
        if project_id:
            filters.append(CodegenUsageLog.project_id == project_id)

        # Query aggregations
        result = self.db.query(
            func.count(CodegenUsageLog.id).label("total_requests"),
            func.sum(CodegenUsageLog.total_tokens).label("total_tokens"),
            func.sum(CodegenUsageLog.actual_cost_usd).label("total_cost"),
            func.avg(CodegenUsageLog.generation_time_ms).label("avg_time_ms"),
            func.sum(CodegenUsageLog.files_generated).label("total_files"),
        ).filter(and_(*filters)).first()

        # Query by status
        status_counts = self.db.query(
            CodegenUsageLog.status,
            func.count(CodegenUsageLog.id),
        ).filter(and_(*filters)).group_by(CodegenUsageLog.status).all()

        # Query by provider
        provider_costs = self.db.query(
            CodegenUsageLog.provider,
            func.sum(CodegenUsageLog.actual_cost_usd),
            func.count(CodegenUsageLog.id),
        ).filter(and_(*filters)).group_by(CodegenUsageLog.provider).all()

        return {
            "date": target_date.isoformat(),
            "total_requests": result.total_requests or 0,
            "total_tokens": result.total_tokens or 0,
            "total_cost_usd": float(result.total_cost or 0),
            "avg_generation_time_ms": int(result.avg_time_ms or 0),
            "total_files_generated": result.total_files or 0,
            "by_status": {s: c for s, c in status_counts},
            "by_provider": {
                p: {"cost_usd": float(c or 0), "requests": r}
                for p, c, r in provider_costs
            },
        }

    def get_monthly_cost(
        self,
        year: int,
        month: int,
        project_id: Optional[uuid.UUID] = None,
    ) -> Dict[str, Any]:
        """
        Get monthly cost summary.

        Args:
            year: Year
            month: Month (1-12)
            project_id: Optional filter by project

        Returns:
            Monthly cost summary dict
        """
        start_dt = datetime(year, month, 1)
        if month == 12:
            end_dt = datetime(year + 1, 1, 1)
        else:
            end_dt = datetime(year, month + 1, 1)

        # Build query filters
        filters = [
            CodegenUsageLog.created_at >= start_dt,
            CodegenUsageLog.created_at < end_dt,
        ]
        if project_id:
            filters.append(CodegenUsageLog.project_id == project_id)

        # Query total
        result = self.db.query(
            func.count(CodegenUsageLog.id).label("total_requests"),
            func.sum(CodegenUsageLog.total_tokens).label("total_tokens"),
            func.sum(CodegenUsageLog.actual_cost_usd).label("total_cost"),
        ).filter(and_(*filters)).first()

        # Query by provider
        provider_costs = self.db.query(
            CodegenUsageLog.provider,
            func.sum(CodegenUsageLog.actual_cost_usd).label("cost"),
        ).filter(and_(*filters)).group_by(CodegenUsageLog.provider).all()

        total_cost = float(result.total_cost or 0)
        budget = float(DEFAULT_MONTHLY_BUDGET_USD)
        budget_used_percent = (total_cost / budget * 100) if budget > 0 else 0

        return {
            "year": year,
            "month": month,
            "total_requests": result.total_requests or 0,
            "total_tokens": result.total_tokens or 0,
            "total_cost_usd": total_cost,
            "budget_limit_usd": budget,
            "budget_used_percent": round(budget_used_percent, 2),
            "budget_exceeded": budget_used_percent > 100,
            "cost_by_provider": {
                p: float(c or 0) for p, c in provider_costs
            },
        }

    def get_cost_report(
        self,
        user_id: Optional[uuid.UUID] = None,
        project_id: Optional[uuid.UUID] = None,
        days: int = 30,
    ) -> Dict[str, Any]:
        """
        Generate comprehensive cost report.

        Args:
            user_id: Optional filter by user
            project_id: Optional filter by project
            days: Number of days to include

        Returns:
            Cost report dict
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        # Build query filters
        filters = [
            CodegenUsageLog.created_at >= datetime.combine(start_date, datetime.min.time()),
        ]
        if user_id:
            filters.append(CodegenUsageLog.user_id == user_id)
        if project_id:
            filters.append(CodegenUsageLog.project_id == project_id)

        # Total metrics
        totals = self.db.query(
            func.count(CodegenUsageLog.id).label("total_requests"),
            func.sum(CodegenUsageLog.total_tokens).label("total_tokens"),
            func.sum(CodegenUsageLog.actual_cost_usd).label("total_cost"),
            func.avg(CodegenUsageLog.generation_time_ms).label("avg_time_ms"),
            func.sum(CodegenUsageLog.files_generated).label("total_files"),
            func.sum(CodegenUsageLog.total_lines_generated).label("total_lines"),
        ).filter(and_(*filters)).first()

        # Daily breakdown
        daily_costs = self.db.query(
            func.date_trunc("day", CodegenUsageLog.created_at).label("date"),
            func.sum(CodegenUsageLog.actual_cost_usd).label("cost"),
            func.count(CodegenUsageLog.id).label("requests"),
        ).filter(and_(*filters)).group_by(
            func.date_trunc("day", CodegenUsageLog.created_at)
        ).order_by("date").all()

        # Quality metrics
        from sqlalchemy import case
        quality_stats = self.db.query(
            func.count(CodegenUsageLog.id).label("total"),
            func.sum(
                case(
                    (CodegenUsageLog.quality_gate_status == QualityGateStatus.PASSED.value, 1),
                    else_=0
                )
            ).label("passed"),
            func.sum(CodegenUsageLog.quality_errors).label("errors"),
            func.sum(CodegenUsageLog.quality_warnings).label("warnings"),
        ).filter(and_(*filters)).first()

        quality_pass_rate = (
            (quality_stats.passed / quality_stats.total * 100)
            if quality_stats.total > 0 else 0
        )

        return {
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": days,
            },
            "totals": {
                "requests": totals.total_requests or 0,
                "tokens": totals.total_tokens or 0,
                "cost_usd": float(totals.total_cost or 0),
                "avg_generation_time_ms": int(totals.avg_time_ms or 0),
                "files_generated": totals.total_files or 0,
                "lines_generated": totals.total_lines or 0,
            },
            "daily_costs": [
                {
                    "date": d.strftime("%Y-%m-%d") if d else None,
                    "cost_usd": float(c or 0),
                    "requests": r,
                }
                for d, c, r in daily_costs
            ],
            "quality": {
                "pass_rate_percent": round(quality_pass_rate, 2),
                "total_errors": quality_stats.errors or 0,
                "total_warnings": quality_stats.warnings or 0,
            },
            "projections": {
                "monthly_estimate_usd": float(totals.total_cost or 0) / days * 30,
                "budget_limit_usd": float(DEFAULT_MONTHLY_BUDGET_USD),
            },
        }

    def log_provider_health(
        self,
        provider: str,
        is_available: bool,
        response_time_ms: Optional[int] = None,
        model: Optional[str] = None,
        model_available: bool = True,
        error_message: Optional[str] = None,
    ) -> CodegenProviderHealth:
        """
        Log provider health check result.

        Args:
            provider: Provider name
            is_available: Whether provider is available
            response_time_ms: Health check response time
            model: Model name checked
            model_available: Whether model is available
            error_message: Error message if unavailable

        Returns:
            Created health record
        """
        health = CodegenProviderHealth(
            provider=provider,
            is_available=is_available,
            response_time_ms=response_time_ms,
            model=model,
            model_available=model_available,
            error_message=error_message,
        )

        self.db.add(health)
        self.db.commit()
        self.db.refresh(health)

        return health

    def get_provider_health_history(
        self,
        provider: str,
        hours: int = 24,
    ) -> List[Dict[str, Any]]:
        """
        Get provider health history.

        Args:
            provider: Provider name
            hours: Hours of history to fetch

        Returns:
            List of health check results
        """
        since = datetime.utcnow() - timedelta(hours=hours)

        records = self.db.query(CodegenProviderHealth).filter(
            CodegenProviderHealth.provider == provider,
            CodegenProviderHealth.checked_at >= since,
        ).order_by(CodegenProviderHealth.checked_at.desc()).limit(100).all()

        return [
            {
                "checked_at": r.checked_at.isoformat(),
                "is_available": r.is_available,
                "response_time_ms": r.response_time_ms,
                "model": r.model,
                "model_available": r.model_available,
                "error_message": r.error_message,
            }
            for r in records
        ]


def get_cost_tracking_service(db: Session) -> CostTrackingService:
    """
    Factory function to create CostTrackingService.

    Args:
        db: Database session

    Returns:
        CostTrackingService instance
    """
    return CostTrackingService(db)
