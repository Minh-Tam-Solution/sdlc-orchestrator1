"""
File: backend/app/middleware/cache_headers.py
Version: 2.0.0
Status: ACTIVE - STAGE 03 (BUILD)
Date: 2026-03-01
Authority: Backend Lead + CTO Approved
Foundation: SDLC 6.1.1, Zero Mock Policy

Description:
HTTP Cache Headers Middleware for API responses (Pure ASGI).
Adds Cache-Control and Vary headers to optimize client-side caching.

Sprint 23 Day 4: API Response Optimization
Sprint 213: Converted from BaseHTTPMiddleware to pure ASGI to prevent
  indefinite request hangs when downstream route handlers raise exceptions
  (Starlette BaseHTTPMiddleware event loop conflict on unhandled exceptions)
"""

import logging

from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = logging.getLogger(__name__)

# Cache configuration per endpoint pattern
CACHE_CONFIG = {
    # Static-like endpoints (rarely change)
    "/api/v1/policies": {"max_age": 300, "stale_while_revalidate": 60},
    "/api/docs": {"max_age": 3600, "stale_while_revalidate": 300},
    "/api/openapi.json": {"max_age": 3600, "stale_while_revalidate": 300},
    "/health": {"max_age": 10, "stale_while_revalidate": 5},
    # Dynamic endpoints (short cache)
    "/api/v1/projects": {"max_age": 60, "stale_while_revalidate": 30},
    "/api/v1/gates": {"max_age": 60, "stale_while_revalidate": 30},
    "/api/v1/dashboard": {"max_age": 60, "stale_while_revalidate": 30},
    "/api/v1/compliance": {"max_age": 120, "stale_while_revalidate": 60},
    "/api/v1/evidence": {"max_age": 60, "stale_while_revalidate": 30},
    "/api/v1/sdlc": {"max_age": 120, "stale_while_revalidate": 60},
    "/api/v1/analytics": {"max_age": 300, "stale_while_revalidate": 120},
    # User-specific endpoints (no cache)
    "/api/v1/auth": {"max_age": 0, "private": True},
    "/api/v1/notifications": {"max_age": 0, "private": True},
    "/api/v1/council": {"max_age": 0, "private": True},
}

# Endpoints that should never be cached
NO_CACHE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
NO_CACHE_PATHS = {"/api/v1/auth/login", "/api/v1/auth/logout", "/api/v1/auth/refresh"}


def _get_cache_config(path: str) -> dict | None:
    """Find cache configuration for the given path (exact then prefix match)."""
    if path in CACHE_CONFIG:
        return CACHE_CONFIG[path]
    for config_path, config in CACHE_CONFIG.items():
        if path.startswith(config_path):
            return config
    return None


def _build_cache_control(cache_config: dict) -> bytes:
    """Build Cache-Control header value from config dict."""
    directives = []
    if cache_config.get("private"):
        directives.append("private")
    else:
        directives.append("public")

    max_age = cache_config.get("max_age", 0)
    if max_age > 0:
        directives.append(f"max-age={max_age}")
        swr = cache_config.get("stale_while_revalidate", 0)
        if swr > 0:
            directives.append(f"stale-while-revalidate={swr}")
    else:
        directives.append("no-cache")

    return ", ".join(directives).encode("utf-8")


class CacheHeadersMiddleware:
    """
    Pure ASGI middleware to add HTTP caching headers to API responses.

    Features:
    - Cache-Control header with max-age and stale-while-revalidate
    - Vary header for proper cache key differentiation
    - Private cache for user-specific endpoints
    - No-cache for mutation endpoints (POST, PUT, DELETE)

    Usage:
        app.add_middleware(CacheHeadersMiddleware)
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method: str = scope.get("method", "GET")
        path: str = scope.get("path", "")

        # Determine cache header to add
        if method in NO_CACHE_METHODS or path in NO_CACHE_PATHS:
            cache_header = b"no-store"
            add_vary = False
        else:
            cache_config = _get_cache_config(path)
            if cache_config:
                cache_header = _build_cache_control(cache_config)
                add_vary = True
            else:
                cache_header = None
                add_vary = False

        # Track response status to only cache 200s for dynamic endpoints
        response_status = [0]

        async def send_with_cache(message: Message) -> None:
            if message["type"] == "http.response.start":
                response_status[0] = message.get("status", 0)

                if cache_header is not None:
                    # For non-mutation methods, only cache successful responses
                    if method not in NO_CACHE_METHODS and response_status[0] != 200:
                        await send(message)
                        return

                    headers = list(message.get("headers", []))
                    headers.append((b"cache-control", cache_header))
                    if add_vary:
                        headers.append((b"vary", b"Authorization, Accept-Encoding"))
                    message["headers"] = headers

            await send(message)

        await self.app(scope, receive, send_with_cache)
