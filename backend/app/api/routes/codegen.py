"""
Codegen API Routes.

Sprint 45: Multi-Provider Codegen Architecture (EP-06)
ADR-022: Provider-Agnostic Codegen Architecture

This module provides REST API endpoints for code generation service.
Supports multi-provider architecture with Ollama as primary provider.

Endpoints:
- GET  /codegen/providers - List available providers
- POST /codegen/generate - Generate code from IR specification
- POST /codegen/validate - Validate generated code
- POST /codegen/estimate - Estimate generation cost
- GET  /codegen/health - Provider health check

Author: Backend Lead
Date: December 23, 2025
Status: ACTIVE
"""

import logging
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.services.codegen.codegen_service import (
    CodegenService,
    NoProviderAvailableError,
    GenerationError,
    get_codegen_service
)
from app.services.codegen.base_provider import CodegenSpec

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/codegen", tags=["Codegen"])


# ============================================================================
# Request/Response Models
# ============================================================================


class GenerateRequest(BaseModel):
    """
    Request model for code generation.

    Attributes:
        app_blueprint: IR specification defining the app to generate
        target_module: Optional specific module to generate
        language: Target programming language (default: python)
        framework: Target framework (default: fastapi)
        preferred_provider: Optional preferred provider name
    """
    app_blueprint: Dict[str, Any] = Field(
        ...,
        description="App blueprint (IR specification)"
    )
    target_module: Optional[str] = Field(
        None,
        description="Specific module to generate (None = all)"
    )
    language: str = Field(
        "python",
        description="Target programming language"
    )
    framework: str = Field(
        "fastapi",
        description="Target framework"
    )
    preferred_provider: Optional[str] = Field(
        None,
        description="Preferred provider (ollama, claude, etc.)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "app_blueprint": {
                    "name": "TaskManager",
                    "description": "Hệ thống quản lý công việc cho SME",
                    "modules": [
                        {
                            "name": "tasks",
                            "entities": [
                                {
                                    "name": "Task",
                                    "fields": [
                                        {"name": "id", "type": "uuid", "primary": True},
                                        {"name": "title", "type": "string", "max_length": 200},
                                        {"name": "description", "type": "text"},
                                        {"name": "status", "type": "enum", "values": ["todo", "in_progress", "done"]},
                                        {"name": "due_date", "type": "datetime", "nullable": True}
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "language": "python",
                "framework": "fastapi"
            }
        }


class ValidateRequest(BaseModel):
    """
    Request model for code validation.

    Attributes:
        code: Code to validate
        context: Additional context for validation
        provider: Optional specific provider to use
    """
    code: str = Field(
        ...,
        description="Code to validate",
        min_length=1,
        max_length=100000
    )
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context (language, framework, etc.)"
    )
    provider: Optional[str] = Field(
        None,
        description="Specific provider to use"
    )


class ProviderInfo(BaseModel):
    """Provider information response model."""
    name: str
    available: bool
    fallback_position: int
    primary: bool


class ProvidersResponse(BaseModel):
    """Response model for list providers endpoint."""
    providers: List[ProviderInfo]
    fallback_chain: List[str]


class GenerateResponse(BaseModel):
    """Response model for generate endpoint."""
    success: bool
    provider: str
    files: Dict[str, str]
    tokens_used: int
    generation_time_ms: int
    metadata: Dict[str, Any]


class ValidateResponse(BaseModel):
    """Response model for validate endpoint."""
    valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]


class CostEstimateItem(BaseModel):
    """Cost estimate for a single provider."""
    estimated_tokens: int
    estimated_cost_usd: float
    confidence: float


class EstimateResponse(BaseModel):
    """Response model for estimate endpoint."""
    estimates: Dict[str, CostEstimateItem]
    recommended_provider: Optional[str]


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    healthy: bool
    providers: Dict[str, bool]
    available_count: int
    total_count: int
    fallback_chain: List[str]


# ============================================================================
# Dependency
# ============================================================================


def get_service() -> CodegenService:
    """Get the global CodegenService instance."""
    return get_codegen_service()


# ============================================================================
# Endpoints
# ============================================================================


@router.get("/providers", response_model=ProvidersResponse)
async def list_providers(
    current_user: User = Depends(get_current_active_user),
    service: CodegenService = Depends(get_service)
) -> ProvidersResponse:
    """
    List available codegen providers.

    Returns all registered providers with their availability status
    and position in the fallback chain.

    Returns:
        ProvidersResponse with provider list and fallback chain
    """
    providers = service.list_providers()
    health = service.health_check()

    return ProvidersResponse(
        providers=[ProviderInfo(**p) for p in providers],
        fallback_chain=health["fallback_chain"]
    )


@router.post("/generate", response_model=GenerateResponse)
async def generate_code(
    request: GenerateRequest,
    current_user: User = Depends(get_current_active_user),
    service: CodegenService = Depends(get_service)
) -> GenerateResponse:
    """
    Generate code from IR specification.

    Takes an app blueprint (IR) and generates production-ready code
    using the available AI provider (Ollama by default).

    Args:
        request: GenerateRequest with app_blueprint and options

    Returns:
        GenerateResponse with generated files and metadata

    Raises:
        503: No providers available
        500: Generation failed
    """
    logger.info(
        f"Code generation requested by user {current_user.id}: "
        f"language={request.language}, framework={request.framework}"
    )

    try:
        spec = CodegenSpec(
            app_blueprint=request.app_blueprint,
            target_module=request.target_module,
            language=request.language,
            framework=request.framework
        )

        result = await service.generate(
            spec,
            preferred_provider=request.preferred_provider
        )

        logger.info(
            f"Generation complete for user {current_user.id}: "
            f"{len(result.files)} files, {result.tokens_used} tokens"
        )

        return GenerateResponse(
            success=True,
            provider=result.provider,
            files=result.files,
            tokens_used=result.tokens_used,
            generation_time_ms=result.generation_time_ms,
            metadata=result.metadata
        )

    except NoProviderAvailableError as e:
        logger.error(f"No providers available: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

    except GenerationError as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code generation failed: {e}"
        )

    except Exception as e:
        logger.exception(f"Unexpected error during generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {e}"
        )


@router.post("/validate", response_model=ValidateResponse)
async def validate_code(
    request: ValidateRequest,
    current_user: User = Depends(get_current_active_user),
    service: CodegenService = Depends(get_service)
) -> ValidateResponse:
    """
    Validate generated code.

    Performs AI-powered validation on code to check for errors,
    potential issues, and improvement suggestions.

    Args:
        request: ValidateRequest with code and context

    Returns:
        ValidateResponse with validation results

    Raises:
        503: No providers available
        500: Validation failed
    """
    logger.info(
        f"Code validation requested by user {current_user.id}: "
        f"{len(request.code)} chars"
    )

    try:
        result = await service.validate(
            request.code,
            request.context,
            provider_name=request.provider
        )

        return ValidateResponse(
            valid=result.valid,
            errors=result.errors,
            warnings=result.warnings,
            suggestions=result.suggestions
        )

    except NoProviderAvailableError as e:
        logger.error(f"No providers available for validation: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

    except Exception as e:
        logger.exception(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation failed: {e}"
        )


@router.post("/estimate", response_model=EstimateResponse)
async def estimate_cost(
    request: GenerateRequest,
    current_user: User = Depends(get_current_active_user),
    service: CodegenService = Depends(get_service)
) -> EstimateResponse:
    """
    Estimate generation cost across providers.

    Returns cost estimates for all available providers to help
    with budget management and provider selection.

    Args:
        request: GenerateRequest with app_blueprint

    Returns:
        EstimateResponse with per-provider cost estimates
    """
    spec = CodegenSpec(
        app_blueprint=request.app_blueprint,
        target_module=request.target_module,
        language=request.language,
        framework=request.framework
    )

    estimates = service.estimate_cost(spec)

    # Convert to response format
    estimate_items = {
        name: CostEstimateItem(
            estimated_tokens=est.estimated_tokens,
            estimated_cost_usd=est.estimated_cost_usd,
            confidence=est.confidence
        )
        for name, est in estimates.items()
    }

    # Find cheapest available provider
    cheapest = service.get_cheapest_provider(spec)
    recommended = cheapest[0] if cheapest else None

    return EstimateResponse(
        estimates=estimate_items,
        recommended_provider=recommended
    )


# ============================================================================
# IR-Based Generation Endpoints (Sprint 46)
# ============================================================================


class IRGenerateRequest(BaseModel):
    """
    Request model for IR-based deterministic code generation.

    This uses Jinja2 templates (no AI) for predictable, fast generation.
    """
    blueprint: Dict[str, Any] = Field(
        ...,
        description="AppBlueprint specification"
    )
    preview: bool = Field(
        False,
        description="If true, return file list without content"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "blueprint": {
                    "name": "Restaurant Management",
                    "version": "1.0.0",
                    "modules": [{
                        "name": "products",
                        "entities": [{
                            "name": "Product",
                            "fields": [
                                {"name": "name", "type": "string", "required": True},
                                {"name": "price", "type": "float", "required": True}
                            ]
                        }]
                    }]
                },
                "preview": False
            }
        }


class IRGeneratedFile(BaseModel):
    """Single generated file."""
    path: str
    content: Optional[str] = None
    language: Optional[str] = None
    lines: int


class IRGenerateResponse(BaseModel):
    """Response model for IR-based generation."""
    success: bool
    app_name: str
    version: Optional[str] = None
    file_count: int
    total_lines: int
    files: List[IRGeneratedFile]
    errors: List[str] = []
    metadata: Dict[str, Any] = {}


class IRValidateResponse(BaseModel):
    """Response model for IR blueprint validation."""
    valid: bool
    issues: List[Dict[str, str]] = []
    normalized_blueprint: Optional[Dict[str, Any]] = None
    summary: Dict[str, Any] = {}


@router.post("/ir/generate", response_model=IRGenerateResponse)
async def ir_generate(
    request: IRGenerateRequest,
    current_user: User = Depends(get_current_active_user),
) -> IRGenerateResponse:
    """
    Generate backend scaffold from AppBlueprint using IR Processor.

    This endpoint uses deterministic Jinja2 templates (no AI) for fast,
    predictable code generation. Suitable for standard CRUD applications.

    Sprint 46: EP-06 IR-Based Backend Scaffold Generation
    ADR-023: IR-Based Deterministic Code Generation

    Args:
        request: IRGenerateRequest with blueprint specification

    Returns:
        IRGenerateResponse with generated files

    Raises:
        400: Invalid blueprint
        500: Generation failed
    """
    from pathlib import Path
    from app.services.codegen.ir import BundleBuilder, IRValidator

    logger.info(f"IR generation requested by user {current_user.id}")

    try:
        # Validate blueprint
        validator = IRValidator()
        validation = validator.validate_app_blueprint(request.blueprint)

        if not validation.valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Invalid blueprint",
                    "issues": [
                        {"path": i.path, "message": i.message, "severity": i.severity}
                        for i in validation.issues
                    ]
                }
            )

        # Get template directory
        template_dir = Path(__file__).parent.parent.parent / "services" / "codegen" / "templates"

        # Build bundle
        builder = BundleBuilder(template_dir=template_dir)

        if request.preview:
            preview = builder.build_preview(validation.normalized_ir)
            return IRGenerateResponse(
                success=preview["success"],
                app_name=preview.get("app_name", "Unknown"),
                file_count=preview["file_count"],
                total_lines=0,
                files=[
                    IRGeneratedFile(
                        path=f["path"],
                        language=f.get("language"),
                        lines=f.get("lines", 0)
                    )
                    for f in preview.get("files", [])
                ],
                errors=preview.get("errors", [])
            )

        bundle = builder.build(validation.normalized_ir)

        if not bundle.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Generation failed", "errors": bundle.errors}
            )

        logger.info(
            f"IR generation complete for user {current_user.id}: "
            f"{bundle.file_count} files, {bundle.total_lines} lines"
        )

        return IRGenerateResponse(
            success=True,
            app_name=bundle.app_name,
            version=bundle.version,
            file_count=bundle.file_count,
            total_lines=bundle.total_lines,
            files=[
                IRGeneratedFile(
                    path=f.path,
                    content=f.content,
                    language=f.language,
                    lines=len(f.content.split("\n")) if f.content else 0
                )
                for f in bundle.files
            ],
            metadata=bundle.to_dict_for_api().get("metadata", {})
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"IR generation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Generation failed: {str(e)}"
        )


@router.post("/ir/validate", response_model=IRValidateResponse)
async def ir_validate(
    request: IRGenerateRequest,
    current_user: User = Depends(get_current_active_user),
) -> IRValidateResponse:
    """
    Validate AppBlueprint without generating code.

    Returns validation results and normalized blueprint if valid.

    Args:
        request: IRGenerateRequest with blueprint to validate

    Returns:
        IRValidateResponse with validation results
    """
    from app.services.codegen.ir import IRValidator

    logger.info(f"IR validation requested by user {current_user.id}")

    validator = IRValidator()
    result = validator.validate_app_blueprint(request.blueprint)

    # Build summary
    summary = {}
    if result.valid and result.normalized_ir:
        ir = result.normalized_ir
        modules = ir.get("modules", [])
        summary = {
            "name": ir.get("name"),
            "version": ir.get("version"),
            "business_domain": ir.get("business_domain"),
            "module_count": len(modules),
            "entity_count": sum(len(m.get("entities", [])) for m in modules),
            "total_fields": sum(
                len(e.get("fields", []))
                for m in modules
                for e in m.get("entities", [])
            )
        }

    return IRValidateResponse(
        valid=result.valid,
        issues=[
            {"path": i.path, "message": i.message, "severity": i.severity}
            for i in result.issues
        ],
        normalized_blueprint=result.normalized_ir if result.valid else None,
        summary=summary
    )


# ============================================================================
# Vietnamese Onboarding Endpoints (Sprint 47)
# ============================================================================


class OnboardingStartRequest(BaseModel):
    """Request to start onboarding session."""
    locale: str = Field("vi", description="Locale (vi or en)")


class OnboardingSessionResponse(BaseModel):
    """Onboarding session info."""
    session_id: str
    current_step: str
    completed_steps: List[str]
    domain: Optional[str] = None
    app_name: Optional[str] = None
    app_name_display: Optional[str] = None
    features: List[str] = []
    scale: Optional[str] = None
    has_blueprint: bool = False
    locale: str = "vi"


class DomainOptionResponse(BaseModel):
    """Domain option for UI."""
    key: str
    name: str
    name_en: str
    description: str
    icon: str
    example_apps: List[str]


class FeatureOptionResponse(BaseModel):
    """Feature option for UI."""
    key: str
    name: str
    description: str


class ScaleOptionResponse(BaseModel):
    """Scale option for UI."""
    key: str
    label: str
    employee_min: int
    employee_max: int
    cgf_tier: str


class SetDomainRequest(BaseModel):
    """Request to set domain."""
    domain: str = Field(..., description="Domain key (restaurant, hotel, retail)")


class SetAppNameRequest(BaseModel):
    """Request to set app name."""
    app_name: str = Field(..., description="App name (Vietnamese OK)")


class SetFeaturesRequest(BaseModel):
    """Request to set features."""
    features: List[str] = Field(..., description="Feature keys")


class SetScaleRequest(BaseModel):
    """Request to set scale."""
    scale: str = Field(..., description="Scale key (micro, small, medium, large)")


class OnboardingStepResponse(BaseModel):
    """Response for onboarding step."""
    success: bool
    error: Optional[str] = None
    next_step: Optional[str] = None
    data: Dict[str, Any] = {}


class OnboardingBlueprintResponse(BaseModel):
    """Response for blueprint generation."""
    success: bool
    errors: List[str] = []
    blueprint: Optional[Dict[str, Any]] = None
    stats: Dict[str, Any] = {}


@router.post("/onboarding/start", response_model=OnboardingSessionResponse)
async def start_onboarding(
    request: OnboardingStartRequest,
    current_user: User = Depends(get_current_active_user),
) -> OnboardingSessionResponse:
    """
    Start new onboarding session for Vietnamese SME founder.

    Sprint 47: Vietnamese Domain Templates + Onboarding IR (EP-06)

    Returns session ID and initial state for guided wizard.
    """
    from app.services.codegen.onboarding import OnboardingService

    service = OnboardingService(locale=request.locale)
    session = service.create_session()

    logger.info(f"Onboarding started by user {current_user.id}: {session.session_id}")

    data = session.to_dict()
    return OnboardingSessionResponse(**data)


@router.get("/onboarding/{session_id}", response_model=OnboardingSessionResponse)
async def get_onboarding_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
) -> OnboardingSessionResponse:
    """Get onboarding session status."""
    from app.services.codegen.onboarding import OnboardingService

    service = OnboardingService()
    session = service.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    data = session.to_dict()
    return OnboardingSessionResponse(**data)


@router.get("/onboarding/options/domains", response_model=List[DomainOptionResponse])
async def get_domain_options(
    current_user: User = Depends(get_current_active_user),
) -> List[DomainOptionResponse]:
    """Get available domain options (restaurant, hotel, retail)."""
    from app.services.codegen.onboarding import OnboardingService

    service = OnboardingService()
    options = service.get_domain_options()

    return [DomainOptionResponse(**opt) for opt in options]


@router.get(
    "/onboarding/options/features/{domain}",
    response_model=List[FeatureOptionResponse]
)
async def get_feature_options(
    domain: str,
    current_user: User = Depends(get_current_active_user),
) -> List[FeatureOptionResponse]:
    """Get available features for a domain."""
    from app.services.codegen.onboarding import OnboardingService

    service = OnboardingService()
    options = service.get_feature_options(domain)

    if not options:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown domain: {domain}"
        )

    return [FeatureOptionResponse(**opt) for opt in options]


@router.get("/onboarding/options/scales", response_model=List[ScaleOptionResponse])
async def get_scale_options(
    current_user: User = Depends(get_current_active_user),
) -> List[ScaleOptionResponse]:
    """Get available scale options."""
    from app.services.codegen.onboarding import OnboardingService

    service = OnboardingService()
    options = service.get_scale_options()

    return [ScaleOptionResponse(**opt) for opt in options]


@router.post(
    "/onboarding/{session_id}/domain",
    response_model=OnboardingStepResponse
)
async def set_onboarding_domain(
    session_id: str,
    request: SetDomainRequest,
    current_user: User = Depends(get_current_active_user),
) -> OnboardingStepResponse:
    """Set domain selection for onboarding session."""
    from app.services.codegen.onboarding import OnboardingService

    service = OnboardingService()
    session = service.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    result = service.set_domain(session, request.domain)

    return OnboardingStepResponse(
        success=result.get("success", False),
        error=result.get("error"),
        next_step=result.get("next_step"),
        data={k: v for k, v in result.items() if k not in ["success", "error", "next_step"]}
    )


@router.post(
    "/onboarding/{session_id}/app_name",
    response_model=OnboardingStepResponse
)
async def set_onboarding_app_name(
    session_id: str,
    request: SetAppNameRequest,
    current_user: User = Depends(get_current_active_user),
) -> OnboardingStepResponse:
    """Set app name for onboarding session."""
    from app.services.codegen.onboarding import OnboardingService

    service = OnboardingService()
    session = service.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    result = service.set_app_name(session, request.app_name)

    return OnboardingStepResponse(
        success=result.get("success", False),
        error=result.get("error"),
        next_step=result.get("next_step"),
        data={k: v for k, v in result.items() if k not in ["success", "error", "next_step"]}
    )


@router.post(
    "/onboarding/{session_id}/features",
    response_model=OnboardingStepResponse
)
async def set_onboarding_features(
    session_id: str,
    request: SetFeaturesRequest,
    current_user: User = Depends(get_current_active_user),
) -> OnboardingStepResponse:
    """Set features for onboarding session."""
    from app.services.codegen.onboarding import OnboardingService

    service = OnboardingService()
    session = service.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    result = service.set_features(session, request.features)

    return OnboardingStepResponse(
        success=result.get("success", False),
        error=result.get("error"),
        next_step=result.get("next_step"),
        data={k: v for k, v in result.items() if k not in ["success", "error", "next_step"]}
    )


@router.post(
    "/onboarding/{session_id}/scale",
    response_model=OnboardingStepResponse
)
async def set_onboarding_scale(
    session_id: str,
    request: SetScaleRequest,
    current_user: User = Depends(get_current_active_user),
) -> OnboardingStepResponse:
    """Set scale for onboarding session."""
    from app.services.codegen.onboarding import OnboardingService

    service = OnboardingService()
    session = service.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    result = service.set_scale(session, request.scale)

    return OnboardingStepResponse(
        success=result.get("success", False),
        error=result.get("error"),
        next_step=result.get("next_step"),
        data={k: v for k, v in result.items() if k not in ["success", "error", "next_step"]}
    )


@router.post(
    "/onboarding/{session_id}/generate",
    response_model=OnboardingBlueprintResponse
)
async def generate_onboarding_blueprint(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
) -> OnboardingBlueprintResponse:
    """
    Generate AppBlueprint from completed onboarding session.

    Returns valid AppBlueprint IR that can be used with /ir/generate endpoint.
    """
    from app.services.codegen.onboarding import OnboardingService

    service = OnboardingService()
    session = service.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    result = service.generate_blueprint(session)

    logger.info(
        f"Onboarding blueprint generated for user {current_user.id}: "
        f"session={session_id}, success={result.get('success')}"
    )

    return OnboardingBlueprintResponse(
        success=result.get("success", False),
        errors=result.get("errors", []),
        blueprint=result.get("blueprint"),
        stats=result.get("stats", {})
    )


@router.get("/health", response_model=HealthResponse)
async def health_check(
    service: CodegenService = Depends(get_service)
) -> HealthResponse:
    """
    Provider health check.

    Returns health status for all providers without requiring
    authentication (useful for monitoring).

    Returns:
        HealthResponse with provider status
    """
    health = service.health_check()

    return HealthResponse(
        healthy=health["healthy"],
        providers=health["providers"],
        available_count=health["available_count"],
        total_count=health["total_count"],
        fallback_chain=health["fallback_chain"]
    )


# ============================================================================
# Cost Tracking Endpoints (Sprint 48)
# ============================================================================


class CostReportRequest(BaseModel):
    """Request for cost report."""
    days: int = Field(30, ge=1, le=365, description="Number of days to include")
    project_id: Optional[str] = Field(None, description="Filter by project ID")


class DailyCostItem(BaseModel):
    """Daily cost item."""
    date: str
    cost_usd: float
    requests: int


class CostTotals(BaseModel):
    """Cost totals summary."""
    requests: int
    tokens: int
    cost_usd: float
    avg_generation_time_ms: int
    files_generated: int
    lines_generated: int


class QualityMetrics(BaseModel):
    """Quality gate metrics."""
    pass_rate_percent: float
    total_errors: int
    total_warnings: int


class CostProjections(BaseModel):
    """Cost projections."""
    monthly_estimate_usd: float
    budget_limit_usd: float


class CostReportResponse(BaseModel):
    """Response for cost report."""
    period: Dict[str, Any]
    totals: CostTotals
    daily_costs: List[DailyCostItem]
    quality: QualityMetrics
    projections: CostProjections


class MonthlyCostResponse(BaseModel):
    """Response for monthly cost summary."""
    year: int
    month: int
    total_requests: int
    total_tokens: int
    total_cost_usd: float
    budget_limit_usd: float
    budget_used_percent: float
    budget_exceeded: bool
    cost_by_provider: Dict[str, float]


class ProviderHealthItem(BaseModel):
    """Provider health check item."""
    checked_at: str
    is_available: bool
    response_time_ms: Optional[int]
    model: Optional[str]
    model_available: bool
    error_message: Optional[str]


class ProviderHealthResponse(BaseModel):
    """Response for provider health history."""
    provider: str
    hours: int
    checks: List[ProviderHealthItem]
    availability_percent: float


@router.get("/usage/report", response_model=CostReportResponse)
async def get_cost_report(
    days: int = 30,
    project_id: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
) -> CostReportResponse:
    """
    Get comprehensive cost report for codegen usage.

    Sprint 48: Quality Gates + Ollama Optimization + MVP Hardening

    Target: <$50/month infrastructure cost per project (Founder Plan).

    Args:
        days: Number of days to include (default 30)
        project_id: Optional filter by project

    Returns:
        Cost report with totals, daily breakdown, and projections
    """
    from uuid import UUID
    from app.api.dependencies import get_db
    from app.services.codegen.cost_tracking_service import get_cost_tracking_service

    # Get database session
    db = next(get_db())

    try:
        service = get_cost_tracking_service(db)

        pid = UUID(project_id) if project_id else None

        report = service.get_cost_report(
            user_id=current_user.id,
            project_id=pid,
            days=days,
        )

        return CostReportResponse(
            period=report["period"],
            totals=CostTotals(**report["totals"]),
            daily_costs=[DailyCostItem(**d) for d in report["daily_costs"]],
            quality=QualityMetrics(**report["quality"]),
            projections=CostProjections(**report["projections"]),
        )
    finally:
        db.close()


@router.get("/usage/monthly", response_model=MonthlyCostResponse)
async def get_monthly_cost(
    year: int,
    month: int,
    project_id: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
) -> MonthlyCostResponse:
    """
    Get monthly cost summary.

    Sprint 48: Cost tracking for budget management.

    Args:
        year: Year (e.g., 2025)
        month: Month (1-12)
        project_id: Optional filter by project

    Returns:
        Monthly cost summary with budget status
    """
    from uuid import UUID
    from app.api.dependencies import get_db
    from app.services.codegen.cost_tracking_service import get_cost_tracking_service

    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be between 1 and 12"
        )

    db = next(get_db())

    try:
        service = get_cost_tracking_service(db)

        pid = UUID(project_id) if project_id else None

        summary = service.get_monthly_cost(
            year=year,
            month=month,
            project_id=pid,
        )

        return MonthlyCostResponse(**summary)
    finally:
        db.close()


@router.get("/usage/provider-health/{provider}", response_model=ProviderHealthResponse)
async def get_provider_health_history(
    provider: str,
    hours: int = 24,
    current_user: User = Depends(get_current_active_user),
) -> ProviderHealthResponse:
    """
    Get provider health check history.

    Sprint 48: Monitor provider availability and fallback frequency.

    Args:
        provider: Provider name (ollama, claude, deepcode)
        hours: Hours of history to fetch (default 24)

    Returns:
        Health check history with availability percentage
    """
    from app.api.dependencies import get_db
    from app.services.codegen.cost_tracking_service import get_cost_tracking_service

    if provider not in ["ollama", "claude", "deepcode"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown provider: {provider}"
        )

    db = next(get_db())

    try:
        service = get_cost_tracking_service(db)

        checks = service.get_provider_health_history(
            provider=provider,
            hours=hours,
        )

        # Calculate availability percentage
        if checks:
            available_count = sum(1 for c in checks if c["is_available"])
            availability_percent = (available_count / len(checks)) * 100
        else:
            availability_percent = 0.0

        return ProviderHealthResponse(
            provider=provider,
            hours=hours,
            checks=[ProviderHealthItem(**c) for c in checks],
            availability_percent=round(availability_percent, 2),
        )
    finally:
        db.close()
