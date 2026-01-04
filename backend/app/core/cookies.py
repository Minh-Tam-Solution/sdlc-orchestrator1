"""
=========================================================================
Cookie Authentication Helper Functions
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: January 03, 2026
Status: ACTIVE - Sprint 63 (httpOnly Cookie Auth)
Authority: Backend Lead + CTO Approved
Foundation: OWASP ASVS Level 2, ADR-026 Cookie Authentication
Framework: SDLC 5.1.2 Universal Framework

Purpose:
- Set httpOnly cookies for access and refresh tokens
- Clear cookies on logout
- Cookie security configuration (XSS protection)

Security Features:
- httpOnly: Prevents JavaScript access (XSS protection)
- Secure: HTTPS only (prevents MITM attacks)
- SameSite=Lax: CSRF protection while allowing OAuth redirects
- Short-lived access token (15 minutes)
- Long-lived refresh token (7 days)

Zero Mock Policy: Production-ready cookie implementation
=========================================================================
"""

from typing import Optional

from fastapi import Response

from app.core.config import settings


# Cookie name constants (CTO Approved - Sprint 63)
ACCESS_TOKEN_COOKIE_NAME = "sdlc_access_token"
REFRESH_TOKEN_COOKIE_NAME = "sdlc_refresh_token"


def get_cookie_settings() -> dict:
    """
    Get cookie security settings from configuration.

    Returns settings aligned with Sprint 63 DoD:
    - httponly: True (XSS protection)
    - secure: From settings (HTTPS only in production)
    - samesite: From settings (default: "lax")
    - path: "/" (available for all paths)

    Returns:
        dict: Cookie settings dictionary
    """
    return {
        "httponly": True,                   # XSS protection - JS cannot read
        "secure": settings.COOKIE_SECURE,   # HTTPS only (configurable for dev)
        "samesite": settings.COOKIE_SAMESITE,  # CSRF protection
        "path": "/",                        # Cookie available for all paths
    }


def get_cookie_domain() -> Optional[str]:
    """
    Get cookie domain from configuration.

    In development (COOKIE_DOMAIN not set), returns None to allow localhost.
    In production, returns the configured domain (e.g., "sdlc.nhatquangholding.com").

    Returns:
        Optional[str]: Cookie domain for production, None for development
    """
    return settings.COOKIE_DOMAIN


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
) -> None:
    """
    Set httpOnly authentication cookies on the response.

    Sets two cookies:
    - sdlc_access_token: Short-lived (15 min) for API access
    - sdlc_refresh_token: Long-lived (7 days) for token refresh

    Args:
        response: FastAPI Response object to set cookies on
        access_token: JWT access token string
        refresh_token: JWT refresh token string

    Example:
        @router.post("/login")
        async def login(response: Response, ...):
            # ... validate credentials ...
            access_token = create_access_token(user_id)
            refresh_token = create_refresh_token(user_id)
            set_auth_cookies(response, access_token, refresh_token)
            return {"message": "Login successful"}
    """
    cookie_domain = get_cookie_domain()
    cookie_settings = get_cookie_settings()

    # Set access token cookie (15 minutes from settings)
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        max_age=settings.COOKIE_ACCESS_TOKEN_MAX_AGE,
        domain=cookie_domain,
        **cookie_settings
    )

    # Set refresh token cookie (7 days from settings)
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        max_age=settings.COOKIE_REFRESH_TOKEN_MAX_AGE,
        domain=cookie_domain,
        **cookie_settings
    )


def clear_auth_cookies(response: Response) -> None:
    """
    Clear authentication cookies on logout.

    Removes both access and refresh token cookies by setting
    their max_age to 0.

    Args:
        response: FastAPI Response object to clear cookies from

    Example:
        @router.post("/logout")
        async def logout(response: Response, ...):
            clear_auth_cookies(response)
            return Response(status_code=204)
    """
    cookie_domain = get_cookie_domain()

    # Clear access token cookie
    response.delete_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        path="/",
        domain=cookie_domain,
    )

    # Clear refresh token cookie
    response.delete_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        path="/",
        domain=cookie_domain,
    )


def set_access_token_cookie(
    response: Response,
    access_token: str,
) -> None:
    """
    Set only the access token cookie (for token refresh).

    Used by the /auth/refresh endpoint to update only the
    access token while keeping the refresh token unchanged.

    Args:
        response: FastAPI Response object to set cookie on
        access_token: New JWT access token string
    """
    cookie_domain = get_cookie_domain()
    cookie_settings = get_cookie_settings()

    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        max_age=settings.COOKIE_ACCESS_TOKEN_MAX_AGE,
        domain=cookie_domain,
        **cookie_settings
    )
