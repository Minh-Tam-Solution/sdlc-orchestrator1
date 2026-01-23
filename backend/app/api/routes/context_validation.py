"""
=========================================================================
Context Validation API Routes - SDLC Orchestrator
Sprint 103: Context <60 Lines + Framework Version Tracking

Version: 1.0.0
Date: January 23, 2026
Status: ACTIVE - Sprint 103 Implementation
Authority: Backend Lead + CTO Approved
Reference: docs/04-build/02-Sprint-Plans/SPRINT-103-DESIGN.md

Endpoints:
- POST /context-validation/validate: Validate AGENTS.md context limits
- POST /context-validation/validate-github: Validate AGENTS.md from GitHub repo
- GET /context-validation/limits: Get current context limits configuration

SDLC 5.2.0 Compliance:
- Per-file context limit: 60 lines max
- Enforces concise, focused file contexts in AGENTS.md
- GitHub Check Run integration for CI/CD gates

Zero Mock Policy: Production-ready FastAPI routes
=========================================================================
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.dependencies import get_current_user
from app.services.context_validation_service import (
    ContextValidationService,
    create_context_validation_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/context-validation", tags=["Context Validation"])


# =============================================================================
# Request/Response Models
# =============================================================================


class ValidateContentRequest(BaseModel):
    """Request to validate AGENTS.md content."""
    content: str = Field(
        ...,
        description="Raw AGENTS.md content to validate",
        min_length=1,
    )
    max_lines: Optional[int] = Field(
        default=None,
        description="Override default max lines per file (default: 60)",
        ge=10,
        le=200,
    )


class ValidateGitHubRequest(BaseModel):
    """Request to validate AGENTS.md from GitHub repo."""
    repo_full_name: str = Field(
        ...,
        description="GitHub repository (owner/repo format)",
        pattern=r'^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$',
    )
    branch: str = Field(
        default="main",
        description="Branch to fetch AGENTS.md from",
    )
    path: str = Field(
        default="AGENTS.md",
        description="Path to AGENTS.md file in repository",
    )


class FileContextResponse(BaseModel):
    """Response for a single file context."""
    file_path: str
    line_count: int
    start_line: int
    end_line: int
    exceeds_limit: bool
    severity: str = Field(..., description="none | warning | error")


class ContextValidationResponse(BaseModel):
    """Response for context validation."""
    valid: bool
    total_files: int
    files_exceeding_limit: int
    max_lines_allowed: int
    violations: list[FileContextResponse]
    summary: str
    github_check_output: Optional[dict] = None


class ContextLimitsResponse(BaseModel):
    """Response for context limits configuration."""
    max_lines_per_file: int
    warning_threshold: int
    description: str
    reference: str


# =============================================================================
# Endpoints
# =============================================================================


@router.post(
    "/validate",
    response_model=ContextValidationResponse,
    summary="Validate AGENTS.md context limits",
    description="Validate that all file contexts in AGENTS.md are within the 60-line limit.",
)
async def validate_content(
    body: ValidateContentRequest,
    current_user: dict = Depends(get_current_user),
) -> ContextValidationResponse:
    """
    Validate AGENTS.md content for per-file context limits.

    Parses the AGENTS.md content to extract file-specific code blocks,
    then validates each file's context against the 60-line limit.

    Args:
        body: Request with AGENTS.md content
        current_user: Authenticated user

    Returns:
        Validation result with list of violations
    """
    service = create_context_validation_service(max_lines=body.max_lines)
    result = service.validate_content(body.content)

    violations = [
        FileContextResponse(
            file_path=ctx.file_path,
            line_count=ctx.line_count,
            start_line=ctx.start_line,
            end_line=ctx.end_line,
            exceeds_limit=ctx.line_count > service.max_context_lines,
            severity="error" if ctx.line_count > service.max_context_lines else "none",
        )
        for ctx in result.violations
    ]

    return ContextValidationResponse(
        valid=result.valid,
        total_files=result.total_files,
        files_exceeding_limit=result.files_exceeding_limit,
        max_lines_allowed=service.max_context_lines,
        violations=violations,
        summary=f"{'PASS' if result.valid else 'FAIL'}: {result.files_exceeding_limit}/{result.total_files} files exceed {service.max_context_lines}-line limit",
        github_check_output=service.format_github_check_output(result) if not result.valid else None,
    )


@router.post(
    "/validate-github",
    response_model=ContextValidationResponse,
    summary="Validate AGENTS.md from GitHub repository",
    description="Fetch and validate AGENTS.md from a GitHub repository.",
)
async def validate_github(
    body: ValidateGitHubRequest,
    current_user: dict = Depends(get_current_user),
) -> ContextValidationResponse:
    """
    Validate AGENTS.md from a GitHub repository.

    Fetches the AGENTS.md file from the specified repository and branch,
    then validates its content against the 60-line limit.

    Args:
        body: Request with GitHub repo details
        current_user: Authenticated user

    Returns:
        Validation result with list of violations
    """
    service = create_context_validation_service()

    try:
        result = await service.validate_remote_agents_md(
            repo_full_name=body.repo_full_name,
            branch=body.branch,
            file_path=body.path,
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AGENTS.md not found at {body.path} in {body.repo_full_name}@{body.branch}",
        )
    except Exception as e:
        logger.error(f"Error fetching AGENTS.md from GitHub: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to fetch AGENTS.md from GitHub: {str(e)}",
        )

    violations = [
        FileContextResponse(
            file_path=ctx.file_path,
            line_count=ctx.line_count,
            start_line=ctx.start_line,
            end_line=ctx.end_line,
            exceeds_limit=ctx.line_count > service.max_context_lines,
            severity="error" if ctx.line_count > service.max_context_lines else "none",
        )
        for ctx in result.violations
    ]

    return ContextValidationResponse(
        valid=result.valid,
        total_files=result.total_files,
        files_exceeding_limit=result.files_exceeding_limit,
        max_lines_allowed=service.max_context_lines,
        violations=violations,
        summary=f"{'PASS' if result.valid else 'FAIL'}: {result.files_exceeding_limit}/{result.total_files} files exceed {service.max_context_lines}-line limit",
        github_check_output=service.format_github_check_output(result) if not result.valid else None,
    )


@router.get(
    "/limits",
    response_model=ContextLimitsResponse,
    summary="Get context limits configuration",
    description="Get the current context limits configuration for AGENTS.md validation.",
)
async def get_limits() -> ContextLimitsResponse:
    """
    Get current context limits configuration.

    Returns the configured limits for AGENTS.md validation,
    including the max lines per file and warning threshold.

    Returns:
        Context limits configuration
    """
    service = create_context_validation_service()

    return ContextLimitsResponse(
        max_lines_per_file=service.max_context_lines,
        warning_threshold=int(service.max_context_lines * 0.8),  # 80% threshold
        description="Per-file context limit in AGENTS.md. Each file's code block must not exceed this limit.",
        reference="SDLC Framework 5.2.0 - Context <60 Lines per file for focused, maintainable AGENTS.md files",
    )


# =============================================================================
# Health Check
# =============================================================================


@router.get(
    "/health",
    summary="Health check",
    description="Check context validation service health.",
)
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "context-validation",
        "version": "1.0.0",
        "max_lines_per_file": 60,
    }
