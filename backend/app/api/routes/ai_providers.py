"""
=========================================================================
AI Provider Configuration Routes - Admin Panel
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: January 16, 2026
Status: ACTIVE - Sprint 70 AI Provider Admin UI
Authority: CTO Approved
Foundation: ADR-007 Multi-Provider AI Integration, ADR-027 Database Settings
Framework: SDLC 5.1.1 Complete Lifecycle

Endpoints:
- GET  /api/v1/admin/ai-providers/config      - Get full AI config
- GET  /api/v1/admin/ai-providers/{provider}/models - Get available models
- PATCH /api/v1/admin/ai-providers/{provider} - Update provider settings
- POST /api/v1/admin/ai-providers/{provider}/test - Test provider connection
- POST /api/v1/admin/ai-providers/ollama/refresh-models - Refresh Ollama models

Security:
- All endpoints require is_superuser=true
- API keys are masked in responses
- Audit logging for all changes

Zero Mock Policy: Real provider connections and validation
=========================================================================
"""

import logging
import time
from datetime import datetime
from typing import Any, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, require_superuser
from app.models import User
from app.services.audit_service import get_audit_service
from app.services.settings_service import SettingsService, get_settings_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/ai-providers", tags=["AI Providers"])


# =========================================================================
# Schemas
# =========================================================================


class ProviderStatus(BaseModel):
    """Status of an AI provider."""
    available: bool = Field(..., description="Whether provider is configured and available")
    configured: bool = Field(..., description="Whether credentials are set")
    url: Optional[str] = Field(None, description="Provider URL (Ollama only)")
    model: Optional[str] = Field(None, description="Default model")
    timeout: Optional[int] = Field(None, description="Request timeout in seconds")


class CodegenConfig(BaseModel):
    """Code generation configuration."""
    url: str = Field(..., description="Ollama URL for codegen")
    model_primary: str = Field(..., description="Primary codegen model")
    model_fast: str = Field(..., description="Fast codegen model")
    timeout: int = Field(..., description="Codegen timeout in seconds")


class AIProviderConfigResponse(BaseModel):
    """Full AI provider configuration response."""
    ollama: ProviderStatus
    claude: ProviderStatus
    openai: ProviderStatus
    codegen: CodegenConfig
    ai_council_enabled: bool
    default_provider: str
    fallback_enabled: bool
    fallback_chain: list[str]
    available_models: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Available models per provider"
    )


class ProviderUpdateRequest(BaseModel):
    """Request to update provider settings."""
    url: Optional[str] = Field(None, description="Provider URL (Ollama)")
    model: Optional[str] = Field(None, description="Default model")
    api_key: Optional[str] = Field(None, description="API key (Claude/OpenAI)")
    timeout: Optional[int] = Field(None, ge=5, le=300, description="Timeout in seconds")


class FallbackUpdateRequest(BaseModel):
    """Request to update fallback configuration."""
    default_provider: Optional[str] = Field(None, description="Default provider")
    fallback_enabled: Optional[bool] = Field(None, description="Enable fallback")
    fallback_chain: Optional[list[str]] = Field(None, description="Fallback order")


class TestResult(BaseModel):
    """Result of provider connection test."""
    success: bool
    latency_ms: int
    error: Optional[str] = None
    provider: str
    model: Optional[str] = None
    tested_at: str


class AvailableModelsResponse(BaseModel):
    """Available models for a provider."""
    models: list[str]


# =========================================================================
# Predefined Models (for Claude/OpenAI which don't have dynamic lists)
# =========================================================================

CLAUDE_MODELS = [
    "claude-sonnet-4-5-20250929",
    "claude-opus-4-5-20251101",
    "claude-3-5-sonnet-20241022",
    "claude-3-haiku-20240307",
]

OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-4",
    "gpt-3.5-turbo",
]


# =========================================================================
# Helper Functions
# =========================================================================


async def get_ollama_models(url: str, timeout: float = 3.0) -> list[str]:
    """
    Fetch available models from Ollama server.

    Args:
        url: Ollama server URL
        timeout: Request timeout in seconds (default 3s for fast fail)

    Returns:
        List of model names

    Note:
        Returns empty list if Ollama is unavailable.
        Uses short timeout to avoid blocking page load.
    """
    if not url:
        return []

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(f"{url.rstrip('/')}/api/tags")
            if response.status_code == 200:
                data = response.json()
                models = [m["name"] for m in data.get("models", [])]
                return sorted(models)
    except Exception as e:
        logger.warning(f"Failed to fetch Ollama models: {e}")

    return []


async def test_ollama_connection(url: str, model: str) -> TestResult:
    """
    Test Ollama connection with a simple generation request.

    Args:
        url: Ollama server URL
        model: Model to test

    Returns:
        TestResult with success status and latency
    """
    if not url:
        return TestResult(
            success=False,
            latency_ms=0,
            error="Ollama URL not configured",
            provider="ollama",
            tested_at=datetime.utcnow().isoformat(),
        )

    try:
        start = time.time()
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Try to generate a simple response
            response = await client.post(
                f"{url.rstrip('/')}/api/generate",
                json={
                    "model": model,
                    "prompt": "Say 'OK' if you are working.",
                    "stream": False,
                    "options": {"num_predict": 10},
                },
            )
            latency = int((time.time() - start) * 1000)

            if response.status_code == 200:
                return TestResult(
                    success=True,
                    latency_ms=latency,
                    provider="ollama",
                    model=model,
                    tested_at=datetime.utcnow().isoformat(),
                )
            else:
                return TestResult(
                    success=False,
                    latency_ms=latency,
                    error=f"HTTP {response.status_code}: {response.text[:200]}",
                    provider="ollama",
                    model=model,
                    tested_at=datetime.utcnow().isoformat(),
                )
    except httpx.TimeoutException:
        return TestResult(
            success=False,
            latency_ms=30000,
            error="Connection timeout (30s)",
            provider="ollama",
            model=model,
            tested_at=datetime.utcnow().isoformat(),
        )
    except Exception as e:
        return TestResult(
            success=False,
            latency_ms=0,
            error=str(e),
            provider="ollama",
            model=model,
            tested_at=datetime.utcnow().isoformat(),
        )


async def test_claude_connection(api_key: str, model: str) -> TestResult:
    """
    Test Claude API connection.

    Args:
        api_key: Anthropic API key
        model: Model to test

    Returns:
        TestResult with success status and latency
    """
    if not api_key:
        return TestResult(
            success=False,
            latency_ms=0,
            error="Anthropic API key not configured",
            provider="claude",
            tested_at=datetime.utcnow().isoformat(),
        )

    try:
        start = time.time()
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": model,
                    "max_tokens": 10,
                    "messages": [{"role": "user", "content": "Say OK"}],
                },
            )
            latency = int((time.time() - start) * 1000)

            if response.status_code == 200:
                return TestResult(
                    success=True,
                    latency_ms=latency,
                    provider="claude",
                    model=model,
                    tested_at=datetime.utcnow().isoformat(),
                )
            else:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get("error", {}).get("message", response.text[:200])
                return TestResult(
                    success=False,
                    latency_ms=latency,
                    error=f"HTTP {response.status_code}: {error_msg}",
                    provider="claude",
                    model=model,
                    tested_at=datetime.utcnow().isoformat(),
                )
    except Exception as e:
        return TestResult(
            success=False,
            latency_ms=0,
            error=str(e),
            provider="claude",
            model=model,
            tested_at=datetime.utcnow().isoformat(),
        )


async def test_openai_connection(api_key: str, model: str) -> TestResult:
    """
    Test OpenAI API connection.

    Args:
        api_key: OpenAI API key
        model: Model to test

    Returns:
        TestResult with success status and latency
    """
    if not api_key:
        return TestResult(
            success=False,
            latency_ms=0,
            error="OpenAI API key not configured",
            provider="openai",
            tested_at=datetime.utcnow().isoformat(),
        )

    try:
        start = time.time()
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "max_tokens": 10,
                    "messages": [{"role": "user", "content": "Say OK"}],
                },
            )
            latency = int((time.time() - start) * 1000)

            if response.status_code == 200:
                return TestResult(
                    success=True,
                    latency_ms=latency,
                    provider="openai",
                    model=model,
                    tested_at=datetime.utcnow().isoformat(),
                )
            else:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get("error", {}).get("message", response.text[:200])
                return TestResult(
                    success=False,
                    latency_ms=latency,
                    error=f"HTTP {response.status_code}: {error_msg}",
                    provider="openai",
                    model=model,
                    tested_at=datetime.utcnow().isoformat(),
                )
    except Exception as e:
        return TestResult(
            success=False,
            latency_ms=0,
            error=str(e),
            provider="openai",
            model=model,
            tested_at=datetime.utcnow().isoformat(),
        )


# =========================================================================
# Routes
# =========================================================================


@router.get(
    "/config",
    response_model=AIProviderConfigResponse,
    summary="Get AI provider configuration",
    description="Get full AI provider configuration including status and available models",
)
async def get_ai_provider_config(
    admin: User = Depends(require_superuser),
    settings: SettingsService = Depends(get_settings_service),
) -> AIProviderConfigResponse:
    """
    Get full AI provider configuration.

    Returns:
        AIProviderConfigResponse with all provider statuses and settings

    Security:
        - Requires is_superuser=true
        - API keys are NOT returned (only configured status)
    """
    # Get all settings
    ollama_url = await settings.get_ai_ollama_url()
    ollama_model = await settings.get_ai_ollama_model()
    ollama_timeout = await settings.get_ai_ollama_timeout()

    anthropic_key = await settings.get_ai_anthropic_api_key()
    anthropic_model = await settings.get_ai_anthropic_model()

    openai_key = await settings.get_ai_openai_api_key()
    openai_model = await settings.get_ai_openai_model()

    codegen_url = await settings.get_codegen_ollama_url()
    codegen_primary = await settings.get_codegen_model_primary()
    codegen_fast = await settings.get_codegen_model_fast()
    codegen_timeout = await settings.get_codegen_timeout()

    default_provider = await settings.get_ai_default_provider()
    fallback_enabled = await settings.is_ai_fallback_enabled()
    fallback_chain = await settings.get_ai_fallback_chain()
    ai_council = await settings.is_ai_council_enabled()

    # Note: Ollama models are fetched async via /ollama/models endpoint
    # to avoid blocking page load when Ollama is slow/unavailable

    return AIProviderConfigResponse(
        ollama=ProviderStatus(
            available=bool(ollama_url),
            configured=bool(ollama_url),
            url=ollama_url,
            model=ollama_model,
            timeout=ollama_timeout,
        ),
        claude=ProviderStatus(
            available=bool(anthropic_key),
            configured=bool(anthropic_key),
            model=anthropic_model,
        ),
        openai=ProviderStatus(
            available=bool(openai_key),
            configured=bool(openai_key),
            model=openai_model,
        ),
        codegen=CodegenConfig(
            url=codegen_url or ollama_url or "",
            model_primary=codegen_primary,
            model_fast=codegen_fast,
            timeout=codegen_timeout,
        ),
        ai_council_enabled=ai_council,
        default_provider=default_provider,
        fallback_enabled=fallback_enabled,
        fallback_chain=fallback_chain,
        available_models={
            "ollama": [],  # Fetched async via /ollama/models
            "claude": CLAUDE_MODELS,
            "openai": OPENAI_MODELS,
        },
    )


@router.get(
    "/{provider}/models",
    response_model=AvailableModelsResponse,
    summary="Get available models for provider",
    description="Get list of available models for a specific provider",
)
async def get_provider_models(
    provider: str,
    admin: User = Depends(require_superuser),
    settings: SettingsService = Depends(get_settings_service),
) -> AvailableModelsResponse:
    """
    Get available models for a provider.

    For Ollama: Fetches from server API
    For Claude/OpenAI: Returns predefined list

    Args:
        provider: Provider name (ollama, claude, openai)

    Returns:
        AvailableModelsResponse with model list
    """
    if provider == "ollama":
        url = await settings.get_ai_ollama_url()
        models = await get_ollama_models(url)
        return AvailableModelsResponse(models=models)
    elif provider == "claude":
        return AvailableModelsResponse(models=CLAUDE_MODELS)
    elif provider == "openai":
        return AvailableModelsResponse(models=OPENAI_MODELS)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown provider: {provider}",
        )


@router.patch(
    "/{provider}",
    summary="Update provider settings",
    description="Update settings for a specific AI provider",
)
async def update_provider_settings(
    provider: str,
    request: Request,
    update: ProviderUpdateRequest,
    admin: User = Depends(require_superuser),
    settings: SettingsService = Depends(get_settings_service),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Update provider settings.

    Args:
        provider: Provider name (ollama, claude, openai)
        update: Settings to update

    Security:
        - Requires is_superuser=true
        - Changes are audit logged
    """
    from app.models import SystemSetting
    from sqlalchemy import select

    updates_made = []

    if provider == "ollama":
        if update.url is not None:
            # Validate URL format
            if update.url and not update.url.startswith(("http://", "https://")):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="URL must start with http:// or https://",
                )
            await _update_setting(db, "ai_ollama_url", update.url, admin.id)
            updates_made.append("url")

        if update.model is not None:
            await _update_setting(db, "ai_ollama_model", update.model, admin.id)
            updates_made.append("model")

        if update.timeout is not None:
            await _update_setting(db, "ai_ollama_timeout", update.timeout, admin.id)
            updates_made.append("timeout")

    elif provider == "claude":
        if update.api_key is not None:
            # Validate API key format
            if update.api_key and not update.api_key.startswith("sk-"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid Anthropic API key format (should start with sk-)",
                )
            await _update_setting(db, "ai_anthropic_api_key", update.api_key, admin.id)
            updates_made.append("api_key")

        if update.model is not None:
            if update.model not in CLAUDE_MODELS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid Claude model. Available: {CLAUDE_MODELS}",
                )
            await _update_setting(db, "ai_anthropic_model", update.model, admin.id)
            updates_made.append("model")

    elif provider == "openai":
        if update.api_key is not None:
            # Validate API key format
            if update.api_key and not update.api_key.startswith("sk-"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid OpenAI API key format (should start with sk-)",
                )
            await _update_setting(db, "ai_openai_api_key", update.api_key, admin.id)
            updates_made.append("api_key")

        if update.model is not None:
            if update.model not in OPENAI_MODELS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid OpenAI model. Available: {OPENAI_MODELS}",
                )
            await _update_setting(db, "ai_openai_model", update.model, admin.id)
            updates_made.append("model")

    elif provider == "fallback":
        # Handle fallback configuration update
        body = await request.json()
        if "default_provider" in body:
            await _update_setting(db, "ai_default_provider", body["default_provider"], admin.id)
            updates_made.append("default_provider")
        if "fallback_enabled" in body:
            await _update_setting(db, "ai_fallback_enabled", body["fallback_enabled"], admin.id)
            updates_made.append("fallback_enabled")
        if "fallback_chain" in body:
            await _update_setting(db, "ai_fallback_chain", body["fallback_chain"], admin.id)
            updates_made.append("fallback_chain")

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown provider: {provider}",
        )

    await db.commit()

    # Invalidate settings cache
    await settings.invalidate_cache()

    # Audit log
    audit_service = get_audit_service(db)
    await audit_service.log(
        action="AI_PROVIDER_UPDATED",
        user_id=admin.id,
        resource_type="ai_provider",
        resource_id=provider,
        details={
            "provider": provider,
            "updates": updates_made,
            "updated_by": admin.email,
        },
        request=request,
    )

    return {
        "status": "success",
        "provider": provider,
        "updates": updates_made,
    }


@router.post(
    "/{provider}/test",
    response_model=TestResult,
    summary="Test provider connection",
    description="Test connection to an AI provider",
)
async def test_provider_connection(
    provider: str,
    admin: User = Depends(require_superuser),
    settings: SettingsService = Depends(get_settings_service),
) -> TestResult:
    """
    Test AI provider connection.

    Args:
        provider: Provider name (ollama, claude, openai)

    Returns:
        TestResult with success status and latency
    """
    if provider == "ollama":
        url = await settings.get_ai_ollama_url()
        model = await settings.get_ai_ollama_model()
        return await test_ollama_connection(url, model)

    elif provider == "claude":
        api_key = await settings.get_ai_anthropic_api_key()
        model = await settings.get_ai_anthropic_model()
        return await test_claude_connection(api_key, model)

    elif provider == "openai":
        api_key = await settings.get_ai_openai_api_key()
        model = await settings.get_ai_openai_model()
        return await test_openai_connection(api_key, model)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown provider: {provider}",
        )


@router.post(
    "/ollama/refresh-models",
    response_model=AvailableModelsResponse,
    summary="Refresh Ollama models",
    description="Fetch fresh list of available models from Ollama server",
)
async def refresh_ollama_models(
    admin: User = Depends(require_superuser),
    settings: SettingsService = Depends(get_settings_service),
) -> AvailableModelsResponse:
    """
    Refresh available Ollama models from server.

    Returns:
        AvailableModelsResponse with fresh model list
    """
    url = await settings.get_ai_ollama_url()
    if not url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ollama URL not configured",
        )

    models = await get_ollama_models(url)
    return AvailableModelsResponse(models=models)


# =========================================================================
# Helper Functions
# =========================================================================


async def _update_setting(
    db: AsyncSession,
    key: str,
    value: Any,
    updated_by,
) -> None:
    """Update a single setting in database."""
    from datetime import datetime
    from sqlalchemy import select, update
    from app.models import SystemSetting

    # Get current setting
    result = await db.execute(
        select(SystemSetting).where(SystemSetting.key == key)
    )
    setting = result.scalar_one_or_none()

    if setting:
        # Store previous value
        setting.previous_value = setting.value
        setting.value = value
        setting.version += 1
        setting.updated_at = datetime.utcnow()
        setting.updated_by = updated_by
    else:
        logger.warning(f"Setting '{key}' not found in database")
