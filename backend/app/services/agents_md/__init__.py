"""
=========================================================================
AGENTS.md Manager - Unified Service Module (Sprint 148)
SDLC Orchestrator - Stage 04 (BUILD)

Version: 1.0.0
Date: February 11, 2026
Status: ACTIVE - Sprint 148 (Service Consolidation)
Authority: Backend Lead + CTO Approved

Purpose:
This module provides a unified import point for AGENTS.md functionality.
Instead of importing from multiple files, use:

    from app.services.agents_md import (
        AgentsMdService,
        AgentsMdValidator,
        AgentsMdConfig,
        AgentsMdResult,
        ValidationResult,
        ValidationError,
    )

Architecture:
- AgentsMdService: Generation (Layer A - Static file)
- AgentsMdValidator: Validation (security, line limits, structure)

Reference: ADR-029-AGENTS-MD-Integration-Strategy
=========================================================================
"""

# Re-export from individual modules for unified access
from app.services.agents_md_service import (
    AgentsMdService,
    AgentsMdConfig,
    AgentsMdResult,
)

from app.services.agents_md_validator import (
    AgentsMdValidator,
    ValidationResult,
    ValidationError,
)

__all__ = [
    # Service
    "AgentsMdService",
    "AgentsMdConfig",
    "AgentsMdResult",
    # Validator
    "AgentsMdValidator",
    "ValidationResult",
    "ValidationError",
]

# Convenience aliases
Manager = AgentsMdService
Validator = AgentsMdValidator
