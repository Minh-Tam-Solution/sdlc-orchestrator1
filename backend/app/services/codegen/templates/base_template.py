"""
Base Template - Abstract base class for deterministic app scaffolding

SDLC Framework Compliance:
- Framework: SDLC 5.2.0 (7-Pillar + AI Governance Principles)
- Pillar 3: Build Phase - Template-Based Code Generation
- AI Governance Principle 4: Deterministic Intermediate Representations
- Methodology: Template Method pattern for consistent scaffolding

Purpose:
Abstract base class for all app builder templates (Next.js, FastAPI, React Native, etc.)
Provides common scaffolding workflow:
1. Validate blueprint → 2. Generate file structure → 3. Populate files → 4. Return artifacts

Ensures consistency across templates while allowing framework-specific customization.

Related ADRs:
- ADR-022: IR-Based Codegen with 4-Gate Quality Pipeline
- ADR-040: App Builder Integration - Competitive Necessity

Sprint: 106 - App Builder Integration (MVP)
Date: January 28, 2026
Owner: Backend Team
Status: ACTIVE
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from pathlib import Path
import logging

from app.schemas.codegen.template_blueprint import (
    TemplateBlueprint,
    TemplateType,
    ProjectTier,
    Entity,
    APIRoute,
    Page
)
from app.schemas.codegen.codegen_result import GeneratedFile

logger = logging.getLogger(__name__)


class BaseTemplate(ABC):
    """
    Abstract base class for app scaffolding templates.

    Template Method Pattern:
    1. validate_blueprint() → Check blueprint completeness
    2. get_file_structure() → Define directory structure
    3. generate_base_files() → Create common files (README, .gitignore, etc.)
    4. generate_framework_files() → Create framework-specific files
    5. generate_entity_files() → Create entity/model files
    6. generate_route_files() → Create API route files
    7. generate_page_files() → Create frontend page files

    Subclasses implement framework-specific logic while base class orchestrates.
    """

    # Template metadata
    template_type: TemplateType
    template_name: str
    template_version: str = "1.0.0"

    # Tech stack defaults
    default_tech_stack: List[str] = []
    required_env_vars: List[str] = []

    def __init__(self):
        """Initialize template with default configuration"""
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    def get_file_structure(self, blueprint: TemplateBlueprint) -> Dict[str, str]:
        """
        Define directory structure for this template.

        Args:
            blueprint: Template blueprint with project specification

        Returns:
            Dict mapping directory paths to descriptions
            Example: {"src/": "Source code", "src/components/": "React components"}
        """
        pass

    @abstractmethod
    def generate_config_files(self, blueprint: TemplateBlueprint) -> List[GeneratedFile]:
        """
        Generate framework configuration files.

        Examples:
        - Next.js: package.json, next.config.js, tsconfig.json
        - FastAPI: pyproject.toml, setup.py, requirements.txt
        - React Native: package.json, app.json, metro.config.js

        Args:
            blueprint: Template blueprint

        Returns:
            List of configuration files
        """
        pass

    @abstractmethod
    def generate_entry_point(self, blueprint: TemplateBlueprint) -> List[GeneratedFile]:
        """
        Generate application entry point files.

        Examples:
        - Next.js: pages/_app.tsx, pages/index.tsx
        - FastAPI: main.py
        - React Native: App.tsx

        Args:
            blueprint: Template blueprint

        Returns:
            List of entry point files
        """
        pass

    def scaffold(self, blueprint: TemplateBlueprint) -> List[GeneratedFile]:
        """
        Main scaffolding workflow (Template Method).

        Orchestrates the complete scaffolding process:
        1. Validate blueprint
        2. Generate SDLC 6.0 specification file (OpenSpec integration)
        3. Generate base files (README, .gitignore, LICENSE)
        4. Generate framework config files
        5. Generate entry point
        6. Generate entities/models (if applicable)
        7. Generate API routes (if applicable)
        8. Generate pages (if applicable)

        SDLC Framework 6.0 Compliance:
        - Generates SPEC-{id}-{name}.md with YAML frontmatter
        - BDD requirements format (GIVEN-WHEN-THEN)
        - Tier-specific quality requirements

        Args:
            blueprint: Validated and finalized template blueprint

        Returns:
            List of all generated files

        Raises:
            ValueError: If blueprint validation fails
        """
        self.logger.info(f"Starting scaffold for {blueprint.project_name} with {self.template_name}")

        # Step 1: Validate blueprint
        self.validate_blueprint(blueprint)

        # Step 2: Collect all files
        files: List[GeneratedFile] = []

        # Step 3: Generate SDLC 6.0 Specification file (OpenSpec integration)
        # This creates the specification document BEFORE code generation
        # ensuring full SDLC compliance from the start
        spec_file = self.generate_spec_file(blueprint)
        files.append(spec_file)
        self.logger.info(f"Generated SDLC 6.0 spec: {spec_file.path}")

        # Base files (common to all templates)
        files.extend(self.generate_base_files(blueprint))

        # Framework-specific files
        files.extend(self.generate_config_files(blueprint))
        files.extend(self.generate_entry_point(blueprint))

        # Entity/Model files (if entities defined)
        if blueprint.entities:
            files.extend(self.generate_entity_files(blueprint))

        # API route files (always call - templates may have default routes)
        # e.g., SaaS template has Stripe routes regardless of user-specified routes
        route_files = self.generate_route_files(blueprint)
        if route_files:
            files.extend(route_files)

        # Frontend page files (always call - templates may have default pages)
        page_files = self.generate_page_files(blueprint)
        if page_files:
            files.extend(page_files)

        self.logger.info(f"Scaffold complete: {len(files)} files generated (including SDLC 6.0 spec)")

        return files

    def validate_blueprint(self, blueprint: TemplateBlueprint) -> None:
        """
        Validate blueprint completeness for this template.

        Args:
            blueprint: Template blueprint to validate

        Raises:
            ValueError: If blueprint is invalid for this template
        """
        # Check template type matches
        if blueprint.template_type != self.template_type:
            raise ValueError(
                f"Blueprint template type {blueprint.template_type} "
                f"does not match {self.template_type}"
            )

        # Check required tech stack
        if self.default_tech_stack:
            missing = [
                tech for tech in self.default_tech_stack
                if tech not in blueprint.tech_stack
            ]
            if missing:
                self.logger.warning(
                    f"Missing recommended tech stack: {', '.join(missing)}"
                )

        # Verify integrity hash
        if not blueprint.verify_integrity():
            raise ValueError(
                f"Blueprint integrity check failed for {blueprint.blueprint_id}"
            )

        self.logger.debug(f"Blueprint validation passed for {blueprint.project_name}")

    def generate_base_files(self, blueprint: TemplateBlueprint) -> List[GeneratedFile]:
        """
        Generate base files common to all templates.

        Files:
        - README.md: Project documentation
        - .gitignore: Git ignore patterns
        - .env.example: Environment variable template
        - LICENSE: MIT License (default)

        Args:
            blueprint: Template blueprint

        Returns:
            List of base files
        """
        files = []

        # README.md
        files.append(GeneratedFile(
            path="README.md",
            content=self._generate_readme(blueprint),
            language="markdown"
        ))

        # .gitignore
        files.append(GeneratedFile(
            path=".gitignore",
            content=self._generate_gitignore(blueprint),
            language="text"
        ))

        # .env.example
        if blueprint.env_vars:
            files.append(GeneratedFile(
                path=".env.example",
                content=self._generate_env_example(blueprint),
                language="dotenv"
            ))

        return files

    def generate_entity_files(self, blueprint: TemplateBlueprint) -> List[GeneratedFile]:
        """
        Generate entity/model files.

        Default implementation returns empty list.
        Override in subclass for backend frameworks (FastAPI, Express).

        Args:
            blueprint: Template blueprint

        Returns:
            List of entity files
        """
        return []

    def generate_route_files(self, blueprint: TemplateBlueprint) -> List[GeneratedFile]:
        """
        Generate API route files.

        Default implementation returns empty list.
        Override in subclass for API frameworks (Next.js, FastAPI, Express).

        Args:
            blueprint: Template blueprint

        Returns:
            List of route files
        """
        return []

    def generate_page_files(self, blueprint: TemplateBlueprint) -> List[GeneratedFile]:
        """
        Generate frontend page files.

        Default implementation returns empty list.
        Override in subclass for frontend frameworks (Next.js, React Native, Nuxt).

        Args:
            blueprint: Template blueprint

        Returns:
            List of page files
        """
        return []

    # Helper methods for base file generation

    def _generate_readme(self, blueprint: TemplateBlueprint) -> str:
        """Generate README.md content"""
        tech_stack_list = "\n".join([f"- {tech}" for tech in blueprint.tech_stack])
        features_list = "\n".join([f"- {feat}" for feat in blueprint.features]) if blueprint.features else "- Basic scaffolding"

        return f"""# {blueprint.project_name}

Generated with SDLC Orchestrator App Builder

## Tech Stack

{tech_stack_list}

## Features

{features_list}

## Getting Started

1. Install dependencies:
```bash
# See package.json or requirements.txt for dependency installation
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run development server:
```bash
# See package.json scripts for available commands
```

## Project Structure

Generated using template: **{self.template_name}** (v{self.template_version})

## License

MIT License - See LICENSE file for details

---

Built with ❤️ using SDLC Orchestrator
"""

    def _generate_gitignore(self, blueprint: TemplateBlueprint) -> str:
        """Generate .gitignore content"""
        # Common patterns for all templates
        base_patterns = [
            "# Dependencies",
            "node_modules/",
            "__pycache__/",
            "*.pyc",
            ".pytest_cache/",
            "",
            "# Environment variables",
            ".env",
            ".env.local",
            ".env.*.local",
            "",
            "# IDE",
            ".vscode/",
            ".idea/",
            "*.swp",
            "*.swo",
            ".DS_Store",
            "",
            "# Build outputs",
            "dist/",
            "build/",
            ".next/",
            "out/",
            "*.egg-info/",
            "",
            "# Logs",
            "*.log",
            "logs/",
            "",
            "# Testing",
            "coverage/",
            ".coverage",
            "*.cover",
        ]

        return "\n".join(base_patterns)

    def _generate_env_example(self, blueprint: TemplateBlueprint) -> str:
        """Generate .env.example content"""
        lines = ["# Environment Variables\n"]

        for var in blueprint.env_vars:
            lines.append(f"{var}=")

        return "\n".join(lines)

    def get_smoke_test_command(self) -> str:
        """
        Get smoke test command for this template.

        Used by Quality Gate 4 (Smoke Test) to verify scaffolded project.

        Returns:
            Shell command to run smoke test
        """
        return "echo 'No smoke test defined'"

    def generate_spec_file(self, blueprint: TemplateBlueprint) -> GeneratedFile:
        """
        Generate SDLC Specification Standard v6.0 compliant spec file.

        Creates a SPEC-{id}-{project-name}.md file with:
        - YAML frontmatter (spec_id, tier, stage, owner, etc.)
        - Overview section (from blueprint description)
        - Requirements section (BDD format: GIVEN-WHEN-THEN)
        - Technical specifications
        - Entities and API contracts
        - Quality requirements (tier-specific)

        Args:
            blueprint: Template blueprint with project specification

        Returns:
            GeneratedFile containing the SDLC 6.0 spec document
        """
        # Get YAML frontmatter
        frontmatter = blueprint.get_openspec_frontmatter()

        # Build spec content sections
        sections = []

        # Section 1: Overview
        sections.append(self._generate_overview_section(blueprint))

        # Section 2: Requirements (BDD format)
        sections.append(self._generate_requirements_section(blueprint))

        # Section 3: Technical Specifications
        sections.append(self._generate_technical_section(blueprint))

        # Section 4: Data Model (Entities)
        if blueprint.entities:
            sections.append(self._generate_entities_section(blueprint))

        # Section 5: API Contracts
        if blueprint.api_routes:
            sections.append(self._generate_api_section(blueprint))

        # Section 6: Pages/UI Specifications
        if blueprint.pages:
            sections.append(self._generate_pages_section(blueprint))

        # Section 7: Quality Requirements (tier-specific)
        sections.append(self._generate_quality_section(blueprint))

        # Combine all sections
        content = frontmatter + "\n".join(sections)

        # Generate filename: SPEC-{short_id}-{project-name}.md
        spec_filename = f"SPEC-{blueprint.spec_id.split('-')[1]}-{blueprint.project_name}.md"

        return GeneratedFile(
            path=f"docs/{spec_filename}",
            content=content,
            language="markdown"
        )

    def _generate_overview_section(self, blueprint: TemplateBlueprint) -> str:
        """Generate overview section from blueprint."""
        description = blueprint.description or f"A {blueprint.template_type.value} application"
        tech_list = ", ".join(blueprint.tech_stack) if blueprint.tech_stack else "Not specified"
        features_list = ", ".join(blueprint.features) if blueprint.features else "Basic scaffolding"

        return f"""
## 1. Overview

### 1.1 Purpose
{description}

### 1.2 Scope
- **Template Type:** {blueprint.template_type.value}
- **Project Name:** {blueprint.project_name}
- **Tech Stack:** {tech_list}
- **Features:** {features_list}

### 1.3 Stakeholders
- **Owner:** {blueprint.owner}
- **Generated by:** SDLC Orchestrator App Builder
- **Blueprint ID:** {blueprint.blueprint_id}
"""

    def _generate_requirements_section(self, blueprint: TemplateBlueprint) -> str:
        """Generate BDD-format requirements section."""
        requirements = []

        # Core scaffolding requirement
        requirements.append(f"""
**REQ-001: Project Scaffolding**
- **Priority:** P1 (Critical)
- **Status:** Generated

GIVEN a user wants to create a {blueprint.template_type.value} application
WHEN they provide the project specification
THEN the system generates a complete project scaffold
AND all configuration files are properly set up
AND the project follows {blueprint.template_type.value} best practices
""")

        # Auth requirement if applicable
        if "auth" in blueprint.features or any(e.auth_required for e in blueprint.entities):
            requirements.append("""
**REQ-002: Authentication System**
- **Priority:** P1 (Critical)
- **Status:** Generated

GIVEN an unauthenticated user
WHEN they access protected resources
THEN the system redirects to the login page
AND valid credentials grant access to protected areas
AND invalid credentials show appropriate error messages
""")

        # CRUD requirements for entities
        for i, entity in enumerate(blueprint.entities, start=3):
            requirements.append(f"""
**REQ-{i:03d}: {entity.name} Management**
- **Priority:** P2 (High)
- **Status:** Generated

GIVEN an authenticated user with appropriate permissions
WHEN they perform CRUD operations on {entity.name}
THEN the system creates/reads/updates/deletes {entity.name} records
AND data validation is enforced for all fields
AND audit trails are maintained for changes
""")

        return f"""
## 2. Requirements

This section defines functional requirements in BDD (Behavior-Driven Development) format
following SDLC Specification Standard v6.0.

{"".join(requirements)}
"""

    def _generate_technical_section(self, blueprint: TemplateBlueprint) -> str:
        """Generate technical specifications section."""
        tech_details = []
        for tech in blueprint.tech_stack:
            tech_details.append(f"- **{tech}**: Included in project scaffold")

        env_vars = []
        for var in blueprint.env_vars:
            env_vars.append(f"- `{var}`: Required")

        return f"""
## 3. Technical Specifications

### 3.1 Technology Stack

{chr(10).join(tech_details) if tech_details else "- Default stack for template type"}

### 3.2 Environment Variables

{chr(10).join(env_vars) if env_vars else "- See .env.example for required variables"}

### 3.3 Quality Mode

- **Mode:** {blueprint.quality_mode}
- **Description:** {"Lenient validation for rapid prototyping" if blueprint.quality_mode == "scaffold" else "Strict validation for production code"}
"""

    def _generate_entities_section(self, blueprint: TemplateBlueprint) -> str:
        """Generate entities/data model section."""
        entity_docs = []
        for entity in blueprint.entities:
            fields_table = "| Field | Type | Required | Unique | Relation |\n"
            fields_table += "|-------|------|----------|--------|----------|\n"
            for field in entity.fields:
                relation = field.relation_to or "-"
                fields_table += f"| {field.name} | {field.type} | {'Yes' if field.required else 'No'} | {'Yes' if field.unique else 'No'} | {relation} |\n"

            entity_docs.append(f"""
### 4.{blueprint.entities.index(entity) + 1} {entity.name}

- **Auth Required:** {'Yes' if entity.auth_required else 'No'}

{fields_table}
""")

        return f"""
## 4. Data Model

This section defines the database entities and their relationships.

{"".join(entity_docs)}
"""

    def _generate_api_section(self, blueprint: TemplateBlueprint) -> str:
        """Generate API contracts section."""
        api_docs = []
        for i, route in enumerate(blueprint.api_routes, start=1):
            methods_str = ", ".join(route.methods)
            entity_ref = f"Related to: {route.entity}" if route.entity else "Standalone endpoint"

            api_docs.append(f"""
### 5.{i} {route.path}

- **Methods:** {methods_str}
- **Auth Required:** {'Yes' if route.auth_required else 'No'}
- **{entity_ref}**
""")

        return f"""
## 5. API Contracts

This section defines the API endpoints generated by this scaffold.

{"".join(api_docs)}
"""

    def _generate_pages_section(self, blueprint: TemplateBlueprint) -> str:
        """Generate pages/UI specifications section."""
        page_docs = []
        for i, page in enumerate(blueprint.pages, start=1):
            entities_used = ", ".join(page.entities_used) if page.entities_used else "None"

            page_docs.append(f"""
### 6.{i} {page.name}

- **Route:** {page.path}
- **Auth Required:** {'Yes' if page.auth_required else 'No'}
- **Entities Used:** {entities_used}
""")

        return f"""
## 6. User Interface

This section defines the frontend pages generated by this scaffold.

{"".join(page_docs)}
"""

    def _generate_quality_section(self, blueprint: TemplateBlueprint) -> str:
        """Generate tier-specific quality requirements section."""
        tier = blueprint.tier.value

        # Tier-specific requirements based on SDLC Specification Standard v6.0
        tier_requirements = {
            "LITE": """
### Quality Requirements (LITE Tier)

- **Documentation:** README.md with setup instructions
- **Testing:** Basic smoke tests
- **Security:** Input validation on user-facing forms
- **Performance:** Page load < 3s
""",
            "STANDARD": """
### Quality Requirements (STANDARD Tier)

- **Documentation:** README.md + API documentation
- **Testing:** Unit tests (>60% coverage) + Integration tests
- **Security:** OWASP Top 10 basic compliance
- **Performance:** API response < 500ms (p95)
- **Code Quality:** Linting enabled, consistent formatting
""",
            "PROFESSIONAL": """
### Quality Requirements (PROFESSIONAL Tier)

- **Documentation:** Full technical specs + API docs + Architecture diagrams
- **Testing:** Unit (>80%) + Integration + E2E tests
- **Security:** OWASP ASVS Level 1 compliance
- **Performance:** API response < 200ms (p95), page load < 1s
- **Code Quality:** Static analysis, dependency scanning
- **Observability:** Logging + basic metrics
""",
            "ENTERPRISE": """
### Quality Requirements (ENTERPRISE Tier)

- **Documentation:** Complete specification package + ADRs + Runbooks
- **Testing:** Unit (>90%) + Integration + E2E + Load tests
- **Security:** OWASP ASVS Level 2 compliance, penetration testing
- **Performance:** API response < 100ms (p95), 99.9% uptime target
- **Code Quality:** Strict static analysis, SBOM, license scanning
- **Observability:** Full APM, distributed tracing, alerting
- **Compliance:** Audit trails, data retention policies
"""
        }

        return f"""
## 7. Quality Requirements

Project Tier: **{tier}**

{tier_requirements.get(tier, tier_requirements["STANDARD"])}

---

*This specification was auto-generated by SDLC Orchestrator App Builder.*
*Spec ID: {blueprint.spec_id}*
*Generated: {blueprint.created_at.strftime("%Y-%m-%d %H:%M UTC")}*
"""
