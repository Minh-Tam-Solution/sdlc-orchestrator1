"""
=========================================================================
Rate Limiting Middleware - Redis-Based (Pure ASGI)
SDLC Orchestrator - Week 5 Day 1 (P1 Features)

Purpose:
- Per-user rate limiting: 100 requests/minute
- Per-IP rate limiting: 1000 requests/hour
- Redis-backed sliding window algorithm
- OWASP ASVS Level 2 compliance (V11: Business Logic)

Requirements:
- 100 req/min per authenticated user
- 1000 req/hour per IP address
- Graceful degradation (fail-open if Redis unavailable)

Architecture:
- Pure ASGI (NOT BaseHTTPMiddleware) — avoids FastAPI 0.100+ hang bug
  (Starlette BaseHTTPMiddleware event loop conflict on unhandled exceptions;
  see CLAUDE.md Module 1 Debugging section)
- Sprint 213: Converted from BaseHTTPMiddleware to pure ASGI to prevent
  indefinite request hangs when downstream route handlers raise exceptions
=========================================================================
"""

import json
import logging
import time
from typing import Optional
from uuid import UUID

from jose import JWTError
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.security import decode_token
from app.utils.redis import get_redis_client

logger = logging.getLogger(__name__)

# Rate limit configuration
USER_RATE_LIMIT = 100  # requests per minute per user
IP_RATE_LIMIT = 1000  # requests per hour per IP
USER_WINDOW = 60  # seconds
IP_WINDOW = 3600  # seconds (1 hour)


class RateLimiterMiddleware:
    """
    Pure ASGI rate limiting middleware using Redis sliding window.

    Algorithm:
    1. Check user rate limit (if authenticated): 100 req/min
    2. Check IP rate limit: 1000 req/hour
    3. If limit exceeded, return 429 Too Many Requests
    4. Fail-open if Redis unavailable (log warning, allow request)

    Usage:
        app.add_middleware(RateLimiterMiddleware)
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path: str = scope.get("path", "")

        # Skip rate limiting for health checks
        if path in ("/health", "/health/ready", "/"):
            await self.app(scope, receive, send)
            return

        # Rate limit check (fail-open: any exception → allow request)
        # IMPORTANT: Do NOT wrap self.app() in this try/except — if the downstream
        # app raises an exception, it must propagate cleanly. Catching it and
        # re-calling self.app() corrupts ASGI state (response already started).
        rate_limited = False
        limit_type = ""
        try:
            user_id = self._get_user_id(scope)
            ip_address = self._get_ip_address(scope)

            if user_id:
                if await self._check_rate_limit(
                    identifier=f"user:{user_id}",
                    limit=USER_RATE_LIMIT,
                    window=USER_WINDOW,
                ):
                    rate_limited = True
                    limit_type = "user"

            if not rate_limited:
                if await self._check_rate_limit(
                    identifier=f"ip:{ip_address}",
                    limit=IP_RATE_LIMIT,
                    window=IP_WINDOW,
                ):
                    rate_limited = True
                    limit_type = "ip"
        except Exception as e:
            # Fail-open: if Redis unavailable, allow request (log warning)
            logger.warning(f"Rate limit check failed (allowing request): {e}")

        if rate_limited:
            await self._send_rate_limit_response(scope, receive, send, limit_type)
            return

        # Rate limit passed — forward to downstream app
        # Exceptions from downstream MUST propagate (not caught here)
        await self.app(scope, receive, send)

    def _get_user_id(self, scope: Scope) -> Optional[str]:
        """
        Extract user ID from JWT token in Authorization header or cookie.

        Sprint 105: Support both Authorization header and httpOnly cookies.

        Args:
            scope: ASGI connection scope

        Returns:
            User ID string or None if not authenticated
        """
        headers: dict[bytes, bytes] = dict(scope.get("headers", []))
        token = None

        # Priority 1: Check httpOnly cookie
        try:
            from app.core.cookies import ACCESS_TOKEN_COOKIE_NAME
            raw_cookie: bytes = headers.get(b"cookie", b"")
            cookie_str = raw_cookie.decode("utf-8", errors="replace")
            if cookie_str:
                for part in cookie_str.split(";"):
                    part = part.strip()
                    if part.startswith(f"{ACCESS_TOKEN_COOKIE_NAME}="):
                        token = part[len(ACCESS_TOKEN_COOKIE_NAME) + 1:]
                        break
        except Exception:
            pass

        # Priority 2: Check Authorization header for JWT token
        if not token:
            raw_auth: bytes = headers.get(b"authorization", b"")
            auth_str: str = raw_auth.decode("utf-8", errors="replace").strip()
            if auth_str.lower().startswith("bearer "):
                token = auth_str[7:].strip()

        if token:
            try:
                # Decode JWT token to extract user_id
                payload = decode_token(token)

                # Extract user ID from token (sub claim)
                user_id = payload.get("sub")
                token_type = payload.get("type")

                # Only use access tokens for rate limiting
                if user_id and token_type == "access":
                    return str(user_id)

            except JWTError:
                # Invalid or expired token - treat as unauthenticated
                logger.debug("Invalid JWT token in rate limiter (treating as unauthenticated)")
                return None
            except Exception as e:
                # Other errors - log and treat as unauthenticated
                logger.debug(f"Failed to extract user_id from token: {e}")
                return None

        return None

    def _get_ip_address(self, scope: Scope) -> str:
        """
        Extract client IP address from ASGI scope.

        Handles proxies/load balancers (X-Forwarded-For header).

        Args:
            scope: ASGI connection scope

        Returns:
            IP address string
        """
        headers: dict[bytes, bytes] = dict(scope.get("headers", []))

        # Check X-Forwarded-For header (from proxies/load balancers)
        forwarded_for = headers.get(b"x-forwarded-for", b"").decode("utf-8", errors="replace")
        if forwarded_for:
            # Take first IP (original client)
            return forwarded_for.split(",")[0].strip()

        # Check X-Real-IP header (from nginx)
        real_ip = headers.get(b"x-real-ip", b"").decode("utf-8", errors="replace")
        if real_ip:
            return real_ip.strip()

        # Fallback to direct client IP from ASGI scope
        client = scope.get("client")
        if client:
            return client[0]  # (host, port) tuple
        return "unknown"

    async def _check_rate_limit(
        self, identifier: str, limit: int, window: int
    ) -> bool:
        """
        Check if rate limit exceeded using Redis sliding window.

        Algorithm:
        1. Get current request count from Redis (key: identifier, sorted set)
        2. Remove old entries (outside window)
        3. Count remaining entries
        4. If count >= limit, return True (rate limit exceeded)
        5. Add current timestamp to sorted set
        6. Set TTL on key (window + 1 second)

        Args:
            identifier: Rate limit identifier (e.g., "user:123" or "ip:1.2.3.4")
            limit: Maximum requests allowed
            window: Time window in seconds

        Returns:
            True if rate limit exceeded, False otherwise
        """
        try:
            redis = await get_redis_client()

            # Get current timestamp
            now = int(time.time())

            # Redis key for this identifier
            key = f"ratelimit:{identifier}"

            # Remove entries outside time window (older than now - window)
            cutoff = now - window
            await redis.zremrangebyscore(key, 0, cutoff)

            # Count current requests in window
            count = await redis.zcard(key)

            # Check if limit exceeded
            if count >= limit:
                logger.warning(
                    f"Rate limit exceeded: {identifier} ({count}/{limit} requests)"
                )
                return True

            # Add current request timestamp
            await redis.zadd(key, {str(now): now})

            # Set TTL on key (window + 1 second for safety)
            await redis.expire(key, window + 1)

            return False

        except Exception as e:
            # Fail-open: if Redis unavailable, log warning and allow request
            logger.warning(f"Rate limit check failed (Redis error): {e}")
            return False

    async def _send_rate_limit_response(
        self, scope: Scope, receive: Receive, send: Send, limit_type: str
    ) -> None:
        """
        Send 429 Too Many Requests response via raw ASGI protocol.

        Args:
            scope: ASGI scope
            receive: ASGI receive callable
            send: ASGI send callable
            limit_type: Type of rate limit ("user" or "ip")
        """
        retry_after = USER_WINDOW if limit_type == "user" else IP_WINDOW
        body = json.dumps({
            "error": "rate_limit_exceeded",
            "message": f"{limit_type.title()} rate limit exceeded",
            "retry_after": retry_after,
        }).encode("utf-8")

        await send({
            "type": "http.response.start",
            "status": 429,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode()),
                (b"retry-after", str(retry_after).encode()),
            ],
        })
        await send({
            "type": "http.response.body",
            "body": body,
        })
