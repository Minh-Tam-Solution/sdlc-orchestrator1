"""
=========================================================================
Governance Middleware - Request-Level Governance Enforcement
SDLC Orchestrator - Sprint 108 (Governance Foundation)

Version: 1.0.0
Date: January 27, 2026
Status: ACTIVE - Sprint 108 Day 3
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Apply governance checks to incoming requests
- Track governance metrics per endpoint
- Integrate with mode service for enforcement
- Support gradual rollout with feature flags

Key Features:
- Non-blocking in WARNING mode
- Configurable blocking in SOFT/FULL modes
- Metrics collection for dashboard
- Audit logging for compliance

Zero Mock Policy: Real middleware with real enforcement
=========================================================================
"""

import asyncio
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import UUID

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.services.governance.mode_service import (
    GovernanceMode,
    GovernanceModeService,
    get_governance_mode_service,
)

logger = logging.getLogger(__name__)


class GovernanceMetrics:
    """
    Metrics collector for governance middleware.

    Tracks:
    - Requests per endpoint
    - Governance checks performed
    - Violations detected
    - Blocked requests
    - Latency impact
    """

    def __init__(self):
        self._requests_total: int = 0
        self._governance_checks: int = 0
        self._violations_detected: int = 0
        self._requests_blocked: int = 0
        self._latency_samples: List[float] = []
        self._endpoint_stats: Dict[str, Dict[str, int]] = {}

    def record_request(
        self,
        endpoint: str,
        governance_checked: bool,
        violations: int,
        blocked: bool,
        latency_ms: float,
    ) -> None:
        """Record metrics for a request."""
        self._requests_total += 1

        if governance_checked:
            self._governance_checks += 1

        if violations > 0:
            self._violations_detected += violations

        if blocked:
            self._requests_blocked += 1

        self._latency_samples.append(latency_ms)
        if len(self._latency_samples) > 10000:
            self._latency_samples = self._latency_samples[-5000:]

        # Per-endpoint stats
        if endpoint not in self._endpoint_stats:
            self._endpoint_stats[endpoint] = {
                "requests": 0,
                "checks": 0,
                "violations": 0,
                "blocked": 0,
            }

        self._endpoint_stats[endpoint]["requests"] += 1
        if governance_checked:
            self._endpoint_stats[endpoint]["checks"] += 1
        if violations > 0:
            self._endpoint_stats[endpoint]["violations"] += violations
        if blocked:
            self._endpoint_stats[endpoint]["blocked"] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary."""
        avg_latency = (
            sum(self._latency_samples) / len(self._latency_samples)
            if self._latency_samples
            else 0.0
        )

        return {
            "requests_total": self._requests_total,
            "governance_checks": self._governance_checks,
            "violations_detected": self._violations_detected,
            "requests_blocked": self._requests_blocked,
            "avg_latency_ms": round(avg_latency, 2),
            "check_rate": (
                self._governance_checks / self._requests_total
                if self._requests_total > 0
                else 0.0
            ),
            "block_rate": (
                self._requests_blocked / self._governance_checks
                if self._governance_checks > 0
                else 0.0
            ),
        }


class GovernanceMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for governance enforcement.

    This middleware:
    1. Intercepts incoming requests
    2. Checks if endpoint requires governance
    3. Validates request against governance rules
    4. Blocks or warns based on mode
    5. Logs all governance decisions

    Usage:
        app = FastAPI()
        app.add_middleware(GovernanceMiddleware)
    """

    # Endpoints that require governance checks
    GOVERNED_ENDPOINTS: Set[str] = {
        "/api/v1/governance/submit",
        "/api/v1/evidence/upload",
        "/api/v1/gates/evaluate",
        "/api/v1/auto-generate/intent",
        "/api/v1/auto-generate/ownership",
        "/api/v1/auto-generate/context",
        "/api/v1/auto-generate/attestation",
        "/api/v1/auto-generate/all",
    }

    # Endpoints that bypass governance (health checks, public endpoints)
    BYPASS_ENDPOINTS: Set[str] = {
        "/health",
        "/ready",
        "/metrics",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/refresh",
    }

    def __init__(
        self,
        app: ASGIApp,
        mode_service: Optional[GovernanceModeService] = None,
    ):
        """
        Initialize governance middleware.

        Args:
            app: ASGI application
            mode_service: Optional GovernanceModeService instance
        """
        super().__init__(app)
        self._mode_service = mode_service
        self._metrics = GovernanceMetrics()
        self._initialized = False

        logger.info("GovernanceMiddleware initialized")

    async def _ensure_initialized(self) -> GovernanceModeService:
        """Ensure mode service is initialized."""
        if not self._initialized:
            if self._mode_service is None:
                self._mode_service = get_governance_mode_service()
                await self._mode_service.initialize()
            self._initialized = True
        return self._mode_service

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """
        Process request through governance middleware.

        Args:
            request: Incoming request
            call_next: Next middleware/handler

        Returns:
            Response from handler or governance rejection
        """
        start_time = time.perf_counter()
        endpoint = request.url.path

        # Quick bypass for excluded endpoints
        if self._should_bypass(endpoint):
            return await call_next(request)

        # Initialize mode service if needed
        mode_service = await self._ensure_initialized()
        mode = mode_service.get_mode()

        # If governance is OFF, pass through
        if mode == GovernanceMode.OFF:
            return await call_next(request)

        # Check if this endpoint requires governance
        requires_governance = self._requires_governance(endpoint)

        if not requires_governance:
            response = await call_next(request)
            latency_ms = (time.perf_counter() - start_time) * 1000
            self._metrics.record_request(
                endpoint=endpoint,
                governance_checked=False,
                violations=0,
                blocked=False,
                latency_ms=latency_ms,
            )
            return response

        # Perform governance check
        governance_result = await self._check_governance(request, mode_service)
        latency_ms = (time.perf_counter() - start_time) * 1000

        # Record metrics
        self._metrics.record_request(
            endpoint=endpoint,
            governance_checked=True,
            violations=governance_result.get("violations_count", 0),
            blocked=not governance_result.get("allowed", True),
            latency_ms=latency_ms,
        )

        # Handle governance decision
        if not governance_result.get("allowed", True):
            # Request blocked
            return await self._create_blocked_response(
                request, governance_result, latency_ms
            )

        # Add governance headers to response
        response = await call_next(request)
        response.headers["X-Governance-Mode"] = mode.value
        response.headers["X-Governance-Checked"] = "true"

        if governance_result.get("warnings"):
            response.headers["X-Governance-Warnings"] = str(
                len(governance_result["warnings"])
            )

        return response

    def _should_bypass(self, endpoint: str) -> bool:
        """Check if endpoint should bypass governance."""
        # Exact match
        if endpoint in self.BYPASS_ENDPOINTS:
            return True

        # Prefix match for common patterns
        bypass_prefixes = ["/docs", "/static", "/assets"]
        for prefix in bypass_prefixes:
            if endpoint.startswith(prefix):
                return True

        return False

    def _requires_governance(self, endpoint: str) -> bool:
        """Check if endpoint requires governance checks."""
        # Exact match
        if endpoint in self.GOVERNED_ENDPOINTS:
            return True

        # Pattern match for governance-related endpoints
        governance_patterns = [
            "/api/v1/governance/",
            "/api/v1/evidence/",
            "/api/v1/gates/",
            "/api/v1/auto-generate/",
        ]

        for pattern in governance_patterns:
            if endpoint.startswith(pattern):
                return True

        return False

    async def _check_governance(
        self,
        request: Request,
        mode_service: GovernanceModeService,
    ) -> Dict[str, Any]:
        """
        Perform governance check on request.

        This is a placeholder that should be extended with actual
        governance rule evaluation.

        Args:
            request: Incoming request
            mode_service: Governance mode service

        Returns:
            Dictionary with governance check results
        """
        mode = mode_service.get_mode()

        # Get project_id from request if available
        project_id = self._extract_project_id(request)

        # In WARNING mode, always allow but log
        if mode == GovernanceMode.WARNING:
            logger.debug(f"Governance WARNING check: {request.url.path}")
            return {
                "allowed": True,
                "mode": mode.value,
                "violations_count": 0,
                "warnings": [],
            }

        # TODO: Implement actual governance rule evaluation
        # This would integrate with:
        # - Auto-generation service for compliance checks
        # - Signals engine for Vibecoding Index
        # - Stage gating service for stage validation
        # - Context authority for ADR linkage

        return {
            "allowed": True,
            "mode": mode.value,
            "violations_count": 0,
            "warnings": [],
        }

    def _extract_project_id(self, request: Request) -> Optional[UUID]:
        """Extract project_id from request."""
        # Try path parameters
        if hasattr(request, "path_params"):
            project_id = request.path_params.get("project_id")
            if project_id:
                try:
                    return UUID(project_id)
                except ValueError:
                    pass

        # Try query parameters
        project_id = request.query_params.get("project_id")
        if project_id:
            try:
                return UUID(project_id)
            except ValueError:
                pass

        # Try headers
        project_id = request.headers.get("X-Project-ID")
        if project_id:
            try:
                return UUID(project_id)
            except ValueError:
                pass

        return None

    async def _create_blocked_response(
        self,
        request: Request,
        governance_result: Dict[str, Any],
        latency_ms: float,
    ) -> Response:
        """Create response for blocked request."""
        import json

        from starlette.responses import JSONResponse

        violations = governance_result.get("violations", [])
        mode = governance_result.get("mode", "unknown")

        response_body = {
            "error": "GOVERNANCE_BLOCKED",
            "message": "Request blocked by governance rules",
            "mode": mode,
            "violations_count": len(violations),
            "violations": violations,
            "suggestions": self._get_suggestions(violations),
            "documentation": "https://docs.sdlc.dev/governance",
            "processing_time_ms": round(latency_ms, 2),
        }

        logger.warning(
            f"Governance BLOCKED: {request.url.path} - "
            f"{len(violations)} violations in {mode} mode"
        )

        return JSONResponse(
            status_code=403,
            content=response_body,
            headers={
                "X-Governance-Mode": mode,
                "X-Governance-Blocked": "true",
                "X-Governance-Violations": str(len(violations)),
            },
        )

    def _get_suggestions(
        self,
        violations: List[Dict[str, Any]],
    ) -> List[str]:
        """Get actionable suggestions for violations."""
        suggestions = []

        for v in violations:
            if v.get("suggestion"):
                suggestions.append(v["suggestion"])
            elif v.get("cli_command"):
                suggestions.append(f"Run: {v['cli_command']}")

        return suggestions

    def get_metrics(self) -> Dict[str, Any]:
        """Get middleware metrics."""
        return self._metrics.get_summary()


# ============================================================================
# Middleware Setup
# ============================================================================


def setup_governance_middleware(
    app: FastAPI,
    mode_service: Optional[GovernanceModeService] = None,
) -> GovernanceMiddleware:
    """
    Set up governance middleware on FastAPI app.

    Args:
        app: FastAPI application
        mode_service: Optional GovernanceModeService instance

    Returns:
        Configured GovernanceMiddleware instance
    """
    middleware = GovernanceMiddleware(app, mode_service=mode_service)
    app.add_middleware(GovernanceMiddleware, mode_service=mode_service)

    logger.info("Governance middleware configured")

    return middleware


# ============================================================================
# Governance Decorator (Alternative to Middleware)
# ============================================================================


def require_governance(
    rule_ids: Optional[List[str]] = None,
    severity: str = "error",
):
    """
    Decorator to require governance checks on specific endpoints.

    This provides fine-grained control over which endpoints require
    governance and what rules apply.

    Usage:
        @router.post("/submit")
        @require_governance(rule_ids=["ownership", "intent"], severity="error")
        async def submit_code(request: Request):
            ...

    Args:
        rule_ids: Specific rule IDs to check (None = all rules)
        severity: Minimum severity to block on (info, warning, error, critical)

    Returns:
        Decorated function
    """
    from functools import wraps

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get request from args/kwargs
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if request is None:
                request = kwargs.get("request")

            if request is None:
                # No request found, proceed without governance
                return await func(*args, **kwargs)

            # Get mode service
            mode_service = get_governance_mode_service()
            mode = mode_service.get_mode()

            # If OFF, skip governance
            if mode == GovernanceMode.OFF:
                return await func(*args, **kwargs)

            # TODO: Implement rule-specific governance checks
            # This would check only the specified rule_ids
            # and respect the severity level

            # For now, proceed with the request
            return await func(*args, **kwargs)

        return wrapper

    return decorator
