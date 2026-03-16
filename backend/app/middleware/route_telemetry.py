"""
Route Telemetry Middleware — Sprint 226, ADR-071 D-071-03.

Surface Reduction Program: Count hits per endpoint per day via Redis INCR.
Labels: ACTIVE_PRIMARY / ACTIVE_ADMIN / LEGACY_SUPPORTED / LEGACY_UNUSED.

Pure ASGI middleware (Sprint 213 mandate: NEVER use BaseHTTPMiddleware).
Fire-and-forget Redis INCR — no await, no latency impact on request path.

Usage data drives data-driven deprecation decisions after 4-6 weeks pilot.
"""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Callable

import re

from starlette.types import ASGIApp, Receive, Scope, Send

logger = logging.getLogger(__name__)

# Pre-compiled regexes for path normalization (P2-1: moved from hot path)
_UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
_NUMERIC_ID_RE = re.compile(r"/\d+(?=/|$)")


class RouteTelemetryMiddleware:
    """
    Pure ASGI middleware that increments a Redis counter per route per day.

    Key format: ``{prefix}:{path}:{YYYY-MM-DD}``
    Example:    ``route_hits:/api/v1/gates:2026-03-16``

    Redis INCR is O(1) and fire-and-forget (~0.1ms, no request blocking).
    Counter keys auto-expire after 90 days to prevent unbounded growth.
    """

    KEY_TTL_SECONDS: int = 90 * 86400  # 90 days

    def __init__(
        self,
        app: ASGIApp,
        *,
        redis_client: Any = None,
        prefix: str = "route_hits",
        enabled: bool = True,
    ) -> None:
        self.app = app
        self._redis = redis_client
        self._prefix = prefix
        self._enabled = enabled

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and self._enabled and self._redis is not None:
            path = scope.get("path", "")
            if path.startswith("/api/"):
                # Normalize: strip trailing slash, collapse path params to {id}
                normalized = self._normalize_path(path)
                date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                key = f"{self._prefix}:{normalized}:{date_str}"

                # Fire-and-forget: don't block request pipeline
                asyncio.create_task(self._increment(key))

        await self.app(scope, receive, send)

    async def _increment(self, key: str) -> None:
        """Increment counter with TTL. Swallow errors — telemetry must never crash requests."""
        try:
            pipe = self._redis.pipeline()
            pipe.incr(key)
            pipe.expire(key, self.KEY_TTL_SECONDS)
            await pipe.execute()
        except Exception:
            # Telemetry failure is never a request failure
            logger.debug("Route telemetry INCR failed for key=%s", key, exc_info=True)

    @staticmethod
    def _normalize_path(path: str) -> str:
        """
        Normalize path for aggregation: collapse UUIDs and numeric IDs to {id}.

        /api/v1/gates/550e8400-e29b-41d4-a716-446655440000/approve → /api/v1/gates/{id}/approve
        /api/v1/projects/123/members → /api/v1/projects/{id}/members
        """
        path = _UUID_RE.sub("{id}", path)
        path = _NUMERIC_ID_RE.sub("/{id}", path)
        return path.rstrip("/")
