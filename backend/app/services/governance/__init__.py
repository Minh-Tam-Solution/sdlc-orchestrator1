"""
=========================================================================
Governance Services - Auto-Generation Layer, Mode Management & Signals
SDLC Orchestrator - Sprint 108 (Governance Foundation)

Version: 1.1.0
Date: January 27, 2026
Status: ACTIVE - Sprint 108 Day 3
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 Quality Assurance System

Services:
- AutoGenerationService: 4 generators for compliance artifacts
- GovernanceModeService: Enforcement mode management (OFF/WARNING/SOFT/FULL)
- SignalsEngine: Vibecoding Index calculation (planned)
- FeedbackService: Actionable error messages (planned)

Zero Mock Policy: Real implementations only
=========================================================================
"""

from app.services.governance.auto_generator import (
    AutoGenerationService,
    IntentGenerator,
    OwnershipGenerator,
    ContextAttachmentGenerator,
    AttestationGenerator,
    GenerationResult,
    FallbackLevel,
    create_auto_generation_service,
    get_auto_generation_service,
)

from app.services.governance.mode_service import (
    GovernanceMode,
    GovernanceModeService,
    GovernanceModeState,
    GovernanceViolation,
    ViolationSeverity,
    EnforcementResult,
    RollbackCriteria,
    create_governance_mode_service,
    get_governance_mode_service,
    initialize_governance_mode_service,
)

__all__ = [
    # Auto-Generation Service
    "AutoGenerationService",
    # Individual Generators
    "IntentGenerator",
    "OwnershipGenerator",
    "ContextAttachmentGenerator",
    "AttestationGenerator",
    # Auto-Generation Data Classes
    "GenerationResult",
    "FallbackLevel",
    # Auto-Generation Factory Functions
    "create_auto_generation_service",
    "get_auto_generation_service",
    # Mode Service
    "GovernanceMode",
    "GovernanceModeService",
    "GovernanceModeState",
    "GovernanceViolation",
    "ViolationSeverity",
    "EnforcementResult",
    "RollbackCriteria",
    # Mode Service Factory Functions
    "create_governance_mode_service",
    "get_governance_mode_service",
    "initialize_governance_mode_service",
]
