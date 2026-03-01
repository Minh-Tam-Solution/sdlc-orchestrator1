"""
=========================================================================
Security Headers Middleware - OWASP ASVS Level 2 Compliance (Pure ASGI)
SDLC Orchestrator - Week 5 Day 1 (P1 Features)

Purpose:
- Add security headers to all HTTP responses
- HSTS (HTTP Strict Transport Security)
- CSP (Content Security Policy)
- X-Frame-Options, X-Content-Type-Options, etc.
- OWASP ASVS Level 2 compliance (V9: Communication Security)

Architecture:
- Pure ASGI (NOT BaseHTTPMiddleware) — avoids FastAPI 0.100+ hang bug
  (Starlette BaseHTTPMiddleware event loop conflict on unhandled exceptions;
  see CLAUDE.md Module 1 Debugging section)
- Sprint 213: Converted from BaseHTTPMiddleware to pure ASGI to prevent
  indefinite request hangs when downstream route handlers raise exceptions

Headers Added:
- Strict-Transport-Security (HSTS): max-age=31536000; includeSubDomains
- Content-Security-Policy (CSP): default-src 'self'
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin
- Permissions-Policy: restrict browser features
=========================================================================
"""

from starlette.types import ASGIApp, Message, Receive, Scope, Send

# Pre-encoded security headers (computed once at module load)
_SECURITY_HEADERS: list[tuple[bytes, bytes]] = [
    # HSTS (HTTP Strict Transport Security)
    # max-age=31536000 = 1 year, includeSubDomains
    (b"strict-transport-security", b"max-age=31536000; includeSubDomains; preload"),
    # Content Security Policy (CSP)
    (
        b"content-security-policy",
        b"default-src 'self'; "
        b"script-src 'self'; "
        b"style-src 'self'; "
        b"img-src 'self' data: https:; "
        b"font-src 'self' data:; "
        b"connect-src 'self' https:; "
        b"frame-ancestors 'none';",
    ),
    # X-Frame-Options: Prevent clickjacking
    (b"x-frame-options", b"DENY"),
    # X-Content-Type-Options: Prevent MIME sniffing
    (b"x-content-type-options", b"nosniff"),
    # X-XSS-Protection: Enable XSS filter (legacy browsers)
    (b"x-xss-protection", b"1; mode=block"),
    # Referrer-Policy: Control referrer information
    (b"referrer-policy", b"strict-origin-when-cross-origin"),
    # Permissions-Policy (Feature Policy): Restrict browser features
    (b"permissions-policy", b"geolocation=(), microphone=(), camera=(), payment=(), usb=()"),
]


class SecurityHeadersMiddleware:
    """
    Pure ASGI middleware that adds security headers to all HTTP responses.

    Usage:
        app.add_middleware(SecurityHeadersMiddleware)

    OWASP ASVS Mapping:
    - V9.1.1: TLS only (HSTS)
    - V9.1.2: HSTS header with max-age
    - V9.1.3: HSTS includeSubDomains
    - V9.1.4: Content Security Policy
    - V9.2.1: X-Frame-Options header
    - V9.2.2: X-Content-Type-Options header
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_security_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.extend(_SECURITY_HEADERS)
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_with_security_headers)
