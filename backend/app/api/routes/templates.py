"""
=========================================================================
SDLC 5.0.0 Templates Router
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: December 7, 2025
Status: ACTIVE - Sprint 32 (Onboarding Alignment)
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.0.0 Complete Lifecycle

Purpose:
- Provide SDLC 5.0.0 folder structure templates by tier
- Support VS Code Extension /init command
- Support offline-first project initialization

Endpoints:
- GET /templates/sdlc-structure - Get SDLC structure template by tier

Security:
- Public endpoint (no authentication required for templates)
- Rate limiting: 100 requests/minute per IP

Zero Mock Policy: Production-ready SDLC 5.0.0 templates
=========================================================================
"""

import logging
from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/templates", tags=["Templates"])


# =========================================================================
# SDLC 5.0.0 Constants
# =========================================================================

# SDLC 5.0.0 Stage Definitions (Contract-First Order)
# Stage 03 is INTEGRATE (moved from old Stage 07)
# Folder names use SHORT format: XX-name (e.g., 00-foundation, not 00-Project-Foundation)
SDLC_STAGES = {
    "00": {
        "id": "00",
        "name": "foundation",
        "full_name": "Foundation (WHY)",
        "description": "Problem Definition & Design Thinking",
        "folder_name": "00-foundation",
    },
    "01": {
        "id": "01",
        "name": "planning",
        "full_name": "Planning (WHAT)",
        "description": "Requirements Analysis & User Stories",
        "folder_name": "01-planning",
    },
    "02": {
        "id": "02",
        "name": "design",
        "full_name": "Design (HOW)",
        "description": "System Architecture & ADRs",
        "folder_name": "02-design",
    },
    "03": {
        "id": "03",
        "name": "integration",
        "full_name": "Integration",
        "description": "API Design & System Integration (Contract-First)",
        "folder_name": "03-integration",
    },
    "04": {
        "id": "04",
        "name": "build",
        "full_name": "Build",
        "description": "Development & Implementation",
        "folder_name": "04-build",
    },
    "05": {
        "id": "05",
        "name": "test",
        "full_name": "Test",
        "description": "Quality Assurance & Testing",
        "folder_name": "05-test",
    },
    "06": {
        "id": "06",
        "name": "deploy",
        "full_name": "Deploy",
        "description": "Release & Deployment",
        "folder_name": "06-deploy",
    },
    "07": {
        "id": "07",
        "name": "operate",
        "full_name": "Operate",
        "description": "Production Operations & SRE",
        "folder_name": "07-operate",
    },
    "08": {
        "id": "08",
        "name": "collaborate",
        "full_name": "Collaborate",
        "description": "Team & Stakeholder Collaboration",
        "folder_name": "08-collaborate",
    },
    "09": {
        "id": "09",
        "name": "govern",
        "full_name": "Govern",
        "description": "Compliance & Governance",
        "folder_name": "09-govern",
    },
}

# 4-Tier Classification
TIER_REQUIREMENTS = {
    "LITE": {
        "team_size_range": "1-2",
        "required_stages": ["00", "01", "04", "05", "06"],
        "optional_stages": ["02", "03", "07", "08", "09"],
        "description": "Minimal documentation for small projects",
    },
    "STANDARD": {
        "team_size_range": "3-10",
        "required_stages": ["00", "01", "02", "03", "04", "05", "06", "07"],
        "optional_stages": ["08", "09"],
        "description": "Standard documentation for most projects",
    },
    "PROFESSIONAL": {
        "team_size_range": "10-50",
        "required_stages": ["00", "01", "02", "03", "04", "05", "06", "07", "08"],
        "optional_stages": ["09"],
        "description": "Professional documentation for larger teams",
    },
    "ENTERPRISE": {
        "team_size_range": "50+",
        "required_stages": ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"],
        "optional_stages": [],
        "description": "Full enterprise documentation with governance",
    },
}


# =========================================================================
# Pydantic Schemas
# =========================================================================


class SDLCTier(str, Enum):
    """SDLC tier enumeration."""

    LITE = "LITE"
    STANDARD = "STANDARD"
    PROFESSIONAL = "PROFESSIONAL"
    ENTERPRISE = "ENTERPRISE"


class TemplateFile(BaseModel):
    """A template file with path and content."""

    path: str = Field(description="Relative path from project root")
    content: str = Field(description="File content (markdown or yaml)")


class SDLCStructureResponse(BaseModel):
    """Response containing SDLC folder structure template."""

    version: str = Field(default="5.0.0", description="SDLC framework version")
    tier: str = Field(description="Selected tier")
    tier_description: str = Field(description="Tier description")
    team_size_range: str = Field(description="Recommended team size")
    folders: List[str] = Field(description="List of folders to create")
    files: List[TemplateFile] = Field(description="Template files with content")
    required_stages: List[str] = Field(description="Required stage IDs for this tier")
    optional_stages: List[str] = Field(description="Optional stage IDs for this tier")


# =========================================================================
# Template Generation Functions
# =========================================================================


def generate_readme_content(stage_id: str, project_name: str = "My Project") -> str:
    """Generate README.md content for a stage."""
    stage = SDLC_STAGES.get(stage_id, {})
    stage_name = stage.get("full_name", f"Stage {stage_id}")
    description = stage.get("description", "")

    return f"""# {stage_name}

{description}

## Overview

This folder contains documentation for the **{stage_name}** stage of the {project_name} project.

## Contents

<!-- Add your content here -->

## SDLC 5.0.0 Compliance

This documentation follows SDLC 5.0.0 Complete Lifecycle methodology.

- **Stage ID**: {stage_id}
- **Stage Name**: {stage.get('name', 'unknown')}
- **Purpose**: {description}

## References

- [SDLC 5.0.0 Framework](https://github.com/nqh-team/sdlc-enterprise-framework)
- [Project Documentation Standards](../00-foundation/README.md)
"""


def generate_sdlc_config(
    project_name: str,
    tier: str,
    project_id: Optional[str] = None,
) -> str:
    """Generate .sdlc-config.json content."""
    tier_info = TIER_REQUIREMENTS.get(tier, TIER_REQUIREMENTS["STANDARD"])
    required_stages = tier_info["required_stages"]

    # Build stage mapping
    stage_mapping = {}
    for stage_id in required_stages:
        stage = SDLC_STAGES.get(stage_id, {})
        folder_name = stage.get("folder_name", f"docs/{stage_id}-Unknown")
        if stage_id == "04":
            stage_mapping[f"{stage_id}-{stage.get('name', 'build')}"] = "src"
        elif stage_id == "05":
            stage_mapping[f"{stage_id}-{stage.get('name', 'test')}"] = "tests"
        elif stage_id == "06":
            stage_mapping[f"{stage_id}-{stage.get('name', 'deploy')}"] = "infrastructure"
        else:
            stage_mapping[f"{stage_id}-{stage.get('name', 'unknown')}"] = f"docs/{folder_name}"

    import json

    config = {
        "$schema": "https://sdlc-orchestrator.io/schemas/config-v1.json",
        "version": "1.0.0",
        "project": {
            "id": project_id or "local-" + project_name.lower().replace(" ", "-"),
            "name": project_name,
            "slug": project_name.lower().replace(" ", "-"),
        },
        "sdlc": {
            "frameworkVersion": "5.0.0",
            "tier": tier,
            "stages": stage_mapping,
        },
        "server": {
            "url": "https://sdlc.mtsolution.com.vn",
            "connected": project_id is not None,
        },
        "gates": {
            "current": "G0.1",
            "passed": [],
        },
    }

    return json.dumps(config, indent=2)


def generate_problem_statement(project_name: str = "My Project") -> str:
    """Generate problem statement template."""
    return f"""# Problem Statement - {project_name}

## Document Information

| Attribute | Value |
|-----------|-------|
| Version | 1.0.0 |
| Status | DRAFT |
| Author | [Your Name] |
| Created | [Date] |
| Last Updated | [Date] |

## Executive Summary

<!-- 2-3 sentence summary of the problem -->

## Problem Definition

### Current State

<!-- Describe the current situation and pain points -->

### Root Cause Analysis

<!-- Analyze the underlying causes of the problem -->

### Impact Assessment

| Impact Area | Description | Severity (1-5) |
|-------------|-------------|----------------|
| Business | | |
| Users | | |
| Technical | | |
| Financial | | |

## Target State

<!-- Describe the desired future state -->

## Success Metrics

| Metric | Current Value | Target Value | Measurement Method |
|--------|---------------|--------------|-------------------|
| | | | |

## Constraints & Assumptions

### Constraints

-

### Assumptions

-

## Stakeholders

| Role | Name | Interest | Influence |
|------|------|----------|-----------|
| | | | |

## SDLC 5.0.0 Gate Reference

This document is required for **Gate G0.1 - Problem Definition**.

- [ ] Problem clearly defined
- [ ] Root cause analyzed
- [ ] Success metrics established
- [ ] Stakeholders identified
"""


def generate_folders_for_tier(tier: str) -> List[str]:
    """Generate list of folders for a tier."""
    tier_info = TIER_REQUIREMENTS.get(tier, TIER_REQUIREMENTS["STANDARD"])
    required_stages = tier_info["required_stages"]

    folders = ["docs"]

    for stage_id in required_stages:
        stage = SDLC_STAGES.get(stage_id, {})
        folder_name = stage.get("folder_name", f"{stage_id}-Unknown")
        folders.append(f"docs/{folder_name}")

    # Add common non-docs folders
    if "04" in required_stages:  # build stage
        folders.append("src")
    if "05" in required_stages:  # test stage
        folders.append("tests")
    if "06" in required_stages:  # deploy stage
        folders.append("infrastructure")

    return sorted(folders)


def generate_files_for_tier(
    tier: str,
    project_name: str = "My Project",
    project_id: Optional[str] = None,
) -> List[TemplateFile]:
    """Generate template files for a tier."""
    tier_info = TIER_REQUIREMENTS.get(tier, TIER_REQUIREMENTS["STANDARD"])
    required_stages = tier_info["required_stages"]

    files = []

    # .sdlc-config.json
    files.append(
        TemplateFile(
            path=".sdlc-config.json",
            content=generate_sdlc_config(project_name, tier, project_id),
        )
    )

    # README for each required stage
    for stage_id in required_stages:
        stage = SDLC_STAGES.get(stage_id, {})
        folder_name = stage.get("folder_name", f"{stage_id}-Unknown")
        files.append(
            TemplateFile(
                path=f"docs/{folder_name}/README.md",
                content=generate_readme_content(stage_id, project_name),
            )
        )

    # Problem Statement (Stage 00)
    if "00" in required_stages:
        files.append(
            TemplateFile(
                path="docs/00-foundation/problem-statement.md",
                content=generate_problem_statement(project_name),
            )
        )

    # .gitkeep files for code folders
    if "04" in required_stages:
        files.append(TemplateFile(path="src/.gitkeep", content=""))
    if "05" in required_stages:
        files.append(TemplateFile(path="tests/.gitkeep", content=""))
    if "06" in required_stages:
        files.append(TemplateFile(path="infrastructure/.gitkeep", content=""))

    return files


# =========================================================================
# Endpoints
# =========================================================================


@router.get(
    "/sdlc-structure",
    response_model=SDLCStructureResponse,
    summary="Get SDLC structure template",
    description=(
        "Returns SDLC 5.0.0 folder structure template for the specified tier. "
        "Used by VS Code Extension /init command."
    ),
)
async def get_sdlc_structure(
    tier: SDLCTier = Query(
        default=SDLCTier.STANDARD,
        description="SDLC tier: LITE, STANDARD, PROFESSIONAL, ENTERPRISE",
    ),
    version: str = Query(
        default="5.0.0",
        description="SDLC framework version",
    ),
    project_name: str = Query(
        default="My Project",
        description="Project name for template personalization",
    ),
    project_id: Optional[str] = Query(
        default=None,
        description="Project ID if connected to server",
    ),
) -> SDLCStructureResponse:
    """
    Get SDLC 5.0.0 folder structure template.

    This endpoint provides:
    1. List of folders to create based on tier
    2. Template files with initial content
    3. Stage requirements for the tier

    Used by:
    - VS Code Extension /init command
    - Web Dashboard project creation
    - CLI sdlcctl init command

    Args:
        tier: SDLC tier (LITE, STANDARD, PROFESSIONAL, ENTERPRISE)
        version: Framework version (default 5.0.0)
        project_name: Project name for personalization
        project_id: Optional server project ID

    Returns:
        SDLCStructureResponse with folders and template files
    """
    logger.info(f"Getting SDLC structure template for tier={tier.value}, version={version}")

    tier_info = TIER_REQUIREMENTS.get(tier.value, TIER_REQUIREMENTS["STANDARD"])

    folders = generate_folders_for_tier(tier.value)
    files = generate_files_for_tier(tier.value, project_name, project_id)

    return SDLCStructureResponse(
        version=version,
        tier=tier.value,
        tier_description=tier_info["description"],
        team_size_range=tier_info["team_size_range"],
        folders=folders,
        files=files,
        required_stages=tier_info["required_stages"],
        optional_stages=tier_info["optional_stages"],
    )


@router.get(
    "/tiers",
    summary="Get available SDLC tiers",
    description="Returns all available SDLC tiers with their requirements.",
)
async def get_tiers() -> dict:
    """
    Get all available SDLC tiers.

    Returns tier definitions with:
    - Team size recommendations
    - Required stages
    - Optional stages
    - Description
    """
    return {
        "version": "5.0.0",
        "tiers": TIER_REQUIREMENTS,
    }


@router.get(
    "/stages",
    summary="Get SDLC 5.0.0 stages",
    description="Returns all SDLC 5.0.0 stages with their definitions.",
)
async def get_stages() -> dict:
    """
    Get all SDLC 5.0.0 stages.

    Returns stage definitions with:
    - Stage ID (00-09)
    - Stage name
    - Description
    - Folder name convention
    """
    return {
        "version": "5.0.0",
        "stages": SDLC_STAGES,
    }
