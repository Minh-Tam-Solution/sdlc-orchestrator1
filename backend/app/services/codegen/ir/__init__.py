"""
IR (Intermediate Representation) Processor Package.

Sprint 46: EP-06 IR-Based Backend Scaffold Generation
ADR-023: IR-Based Deterministic Code Generation

This package transforms validated IR schemas into deterministic backend code
scaffolds using Jinja2 templates (no AI required for generation).

Components:
- IRValidator: JSON Schema validation for AppBlueprint
- IRProcessor: Abstract base for code processors
- ProjectProcessor: Scaffold generation (main.py, config, requirements)
- ModelProcessor: SQLAlchemy model + Pydantic schema generation
- EndpointProcessor: CRUD endpoint generation
- MigrationProcessor: Alembic migration generation
- BundleBuilder: Orchestrator that combines all processors

Design Reference:
    docs/02-design/14-Technical-Specs/IR-Processor-Specification.md

Usage:
    from app.services.codegen.ir import BundleBuilder

    builder = BundleBuilder(schema_dir, template_dir)
    bundle = builder.build(app_blueprint_dict)

    if bundle.success:
        for file in bundle.files:
            print(f"{file.path}: {len(file.content)} bytes")

Author: Backend Lead
Date: December 23, 2025
Version: 1.0.0
Status: ACTIVE - Sprint 46 Implementation
"""

from .validator import (
    IRValidator,
    IRValidationResult,
    ValidationIssue,
)
from .processor_base import (
    IRProcessor,
    ProcessorResult,
    GeneratedFile,
    CompositeProcessor,
)
from .project_processor import ProjectProcessor
from .model_processor import ModelProcessor
from .endpoint_processor import EndpointProcessor
from .bundle_builder import BundleBuilder, GeneratedBundle

__all__ = [
    # Validator
    "IRValidator",
    "IRValidationResult",
    "ValidationIssue",
    # Base classes
    "IRProcessor",
    "ProcessorResult",
    "GeneratedFile",
    "CompositeProcessor",
    # Processors
    "ProjectProcessor",
    "ModelProcessor",
    "EndpointProcessor",
    # Bundle Builder
    "BundleBuilder",
    "GeneratedBundle",
]
