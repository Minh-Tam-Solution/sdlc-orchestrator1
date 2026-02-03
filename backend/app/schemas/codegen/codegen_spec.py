"""
Codegen Spec Schema - Request specification for code generation

SDLC Framework Compliance:
- Framework: SDLC 5.3.0 (8-Pillar Architecture)
- Pillar 3: Build Phase - Code Generation Specifications
- AI Governance Principle 4: Deterministic Intermediate Representations
- Methodology: Contract-first design for AI-assisted codegen

Purpose:
Input specification for code generation requests. Used by:
- CodegenService to route requests
- Intent Router to detect user intent
- App Builder Provider for scaffolding
- Ollama/Claude providers for LLM generation

Sprint: 106 - App Builder Integration (MVP)
Date: January 28, 2026
Owner: Backend Team
Status: ACTIVE
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid


class CodegenSpec(BaseModel):
    """
    Code generation request specification.

    This is the primary input for all codegen workflows:
    - App scaffolding (deterministic templates)
    - LLM-based code generation
    - Feature additions
    - Bug fixes

    Example:
        spec = CodegenSpec(
            description="Create Instagram clone with Next.js",
            project_name="instapic",
            language="typescript",
            framework="nextjs",
            tech_stack=["prisma", "tailwind", "nextauth"],
            entities=[
                {"name": "Post", "fields": [
                    {"name": "image_url", "type": "string"},
                    {"name": "caption", "type": "string"},
                ]}
            ]
        )
    """

    # Required fields
    description: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Description of what to generate (e.g., 'Create Instagram clone')"
    )
    project_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Project name (lowercase, hyphen-separated: 'my-app')"
    )

    # Language and framework
    language: str = Field(
        default="typescript",
        description="Primary programming language: typescript, python, etc."
    )
    framework: Optional[str] = Field(
        default=None,
        description="Web framework: nextjs, fastapi, react-native, express"
    )

    # Tech stack
    tech_stack: List[str] = Field(
        default_factory=list,
        description="Additional technologies: ['prisma', 'tailwind', 'stripe']"
    )

    # Structure (optional, for scaffolding)
    entities: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Database entities/models to generate"
    )
    api_routes: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="API routes to generate"
    )
    pages: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Frontend pages to generate"
    )

    # Context
    context: Optional[str] = Field(
        default=None,
        description="Additional context (existing code snippets, requirements, etc.)"
    )
    constraints: Optional[List[str]] = Field(
        default=None,
        description="Constraints to follow (e.g., 'No external APIs', 'Must use shadcn')"
    )

    # Provider hints
    preferred_provider: Optional[str] = Field(
        default=None,
        description="Preferred provider: app-builder, ollama, claude (overrides auto-routing)"
    )
    quality_mode: str = Field(
        default="scaffold",
        description="Quality mode: 'scaffold' (lenient) or 'production' (strict)"
    )

    # Metadata
    spec_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique spec identifier"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Spec creation timestamp"
    )
    user_id: Optional[str] = Field(
        default=None,
        description="User who created the spec"
    )
    project_id: Optional[str] = Field(
        default=None,
        description="Associated project ID"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "Create Instagram clone with Next.js and Prisma",
                "project_name": "instapic",
                "language": "typescript",
                "framework": "nextjs",
                "tech_stack": ["prisma", "tailwind", "nextauth", "cloudinary"],
                "entities": [
                    {
                        "name": "Post",
                        "fields": [
                            {"name": "image_url", "type": "string", "required": True},
                            {"name": "caption", "type": "string", "required": False},
                            {"name": "created_at", "type": "datetime", "required": True},
                        ],
                        "auth_required": True
                    },
                    {
                        "name": "Comment",
                        "fields": [
                            {"name": "content", "type": "string", "required": True},
                            {"name": "post_id", "type": "relation", "relation_to": "Post"},
                        ],
                        "auth_required": True
                    }
                ],
                "pages": [
                    {"path": "/feed", "name": "Feed", "auth_required": True},
                    {"path": "/profile", "name": "Profile", "auth_required": True},
                ],
                "quality_mode": "scaffold"
            }
        }
    )
