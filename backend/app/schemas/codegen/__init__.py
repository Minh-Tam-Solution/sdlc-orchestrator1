"""
Codegen Schemas Package - Schemas for code generation workflows

SDLC Framework Compliance:
- Framework: SDLC 5.3.0 (8-Pillar Architecture)
- Pillar 3: Build Phase - Code Generation
- AI Governance Principle 4: Deterministic Intermediate Representations

Exports:
- CodegenSpec: Input specification for code generation
- CodegenResult: Output from code generation
- GeneratedFile: Single generated file
- CostBreakdown: Cost tracking for planning + execution
- TemplateBlueprint: IR for app scaffolding
- TemplateType: Enum of supported templates
- Entity, EntityField, APIRoute, Page: Blueprint components

Sprint: 106 - App Builder Integration (MVP)
Date: January 28, 2026
"""

# Template Blueprint (IR for app scaffolding)
from app.schemas.codegen.template_blueprint import (
    TemplateBlueprint,
    TemplateType,
    ProjectTier,
    SpecCategory,
    Entity,
    EntityField,
    APIRoute,
    Page,
    AppBuilderBlueprint,  # Alias
)

# Codegen Spec (request input)
from app.schemas.codegen.codegen_spec import CodegenSpec

# Codegen Result (response output)
from app.schemas.codegen.codegen_result import (
    CodegenResult,
    GeneratedFile,
    CostBreakdown,
)

__all__ = [
    # Template Blueprint
    "TemplateBlueprint",
    "TemplateType",
    "Entity",
    "EntityField",
    "APIRoute",
    "Page",
    "AppBuilderBlueprint",
    # Spec
    "CodegenSpec",
    # Result
    "CodegenResult",
    "GeneratedFile",
    "CostBreakdown",
]
