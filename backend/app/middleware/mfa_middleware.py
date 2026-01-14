"""
=========================================================================
MFA Enforcement Middleware - ADR-027 Phase 1
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: 2026-01-14
Status: ACTIVE - Sprint N+1 (ADR-027 Phase 1)
Authority: Backend Lead + CTO Approved
Foundation: FastAPI Middleware, SettingsService
Framework: SDLC 5.1.2 Universal Framework

Purpose:
Enforce MFA requirement for all users when mfa_required setting is enabled.

Features:
- 7-day grace period for new users to complete MFA setup
- Grace period countdown header (X-MFA-Setup-Required)
- Admin exemption support (is_mfa_exempt flag)
- Auto-set deadline on first login after flag enabled
- Block access after deadline expires (403 Forbidden)

ADR-027 Phase 1: mfa_required implementation
Zero Mock Policy: Real MFA enforcement with database-backed deadline tracking
=========================================================================
"""

from datetime import datetime, timedelta
from typing import Callable, Optional

from fastapi import HTTPException, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.services.settings_service import SettingsService
from app.models.user import User


class MFAEnforcementMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce MFA requirement when mfa_required setting is enabled.

    Flow:
    1. Check if mfa_required setting is enabled in database
    2. Skip enforcement if user already has MFA enabled or is exempt
    3. Set 7-day deadline if first time seeing flag (auto-onboarding)
    4. Check if deadline has passed
       - If passed: Block access with 403 error
       - If not passed: Add warning header (X-MFA-Setup-Required)

    Exemption:
    - Admins can exempt users via is_mfa_exempt flag
    - Useful for service accounts, external integrations

    Grace Period:
    - 7 days from first login after flag enabled
    - Countdown shown in response header
    - User can still access system during grace period

    Example Response Headers:
        X-MFA-Setup-Required: 5 days remaining
        X-MFA-Setup-Deadline: 2026-01-21T12:34:56Z
    """

    # Endpoints that bypass MFA enforcement
    EXEMPT_PATHS = [
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/refresh",
        "/api/v1/auth/mfa/setup",
        "/api/v1/auth/mfa/verify",
        "/api/v1/auth/mfa/backup",
        "/api/v1/health",
        "/api/v1/docs",
        "/api/v1/openapi.json",
    ]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and enforce MFA requirement if enabled.

        Args:
            request: FastAPI request object
            call_next: Next middleware/route handler

        Returns:
            Response with MFA enforcement applied

        Raises:
            HTTPException(403): If MFA setup deadline has passed
        """
        # Skip MFA enforcement for exempt endpoints
        if self._is_exempt_path(request.url.path):
            return await call_next(request)

        # Skip if user not authenticated (auth middleware will handle)
        try:
            user = await self._get_user_from_request(request)
            if not user:
                return await call_next(request)
        except Exception:
            # If we can't get user, let auth middleware handle it
            return await call_next(request)

        # Check if MFA is required (read from database setting)
        db: AsyncSession = request.state.db
        settings_service = SettingsService(db)

        is_required = await settings_service.is_mfa_required()

        if not is_required:
            # MFA not required - proceed normally
            return await call_next(request)

        # MFA is required - check user status

        # Skip if user already has MFA enabled
        if user.mfa_enabled:
            return await call_next(request)

        # Skip if user is exempt (admin override)
        if user.is_mfa_exempt:
            return await call_next(request)

        # User needs to set up MFA

        # First time seeing this flag - set deadline (7 days grace period)
        if not user.mfa_setup_deadline:
            user.mfa_setup_deadline = datetime.utcnow() + timedelta(days=7)
            await db.commit()
            await db.refresh(user)

        # Check if deadline has passed
        now = datetime.utcnow()

        if now > user.mfa_setup_deadline:
            # Deadline passed - block access
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"MFA setup is required. Your 7-day grace period expired on "
                    f"{user.mfa_setup_deadline.strftime('%Y-%m-%d %H:%M:%S UTC')}. "
                    f"Please contact an administrator for assistance."
                ),
            )

        # Still in grace period - allow access with warning
        days_left = (user.mfa_setup_deadline - now).days
        hours_left = int((user.mfa_setup_deadline - now).total_seconds() / 3600)

        response = await call_next(request)

        # Add warning headers
        if days_left > 0:
            response.headers["X-MFA-Setup-Required"] = f"{days_left} days remaining"
        elif hours_left > 0:
            response.headers["X-MFA-Setup-Required"] = f"{hours_left} hours remaining"
        else:
            response.headers["X-MFA-Setup-Required"] = "Less than 1 hour remaining"

        response.headers["X-MFA-Setup-Deadline"] = user.mfa_setup_deadline.isoformat()

        return response

    def _is_exempt_path(self, path: str) -> bool:
        """
        Check if path is exempt from MFA enforcement.

        Args:
            path: Request URL path

        Returns:
            True if path is exempt, False otherwise
        """
        return any(path.startswith(exempt) for exempt in self.EXEMPT_PATHS)

    async def _get_user_from_request(self, request: Request) -> Optional[User]:
        """
        Extract user from request state.

        Args:
            request: FastAPI request object

        Returns:
            User object if authenticated, None otherwise
        """
        # User should be set by auth middleware
        return getattr(request.state, "user", None)
