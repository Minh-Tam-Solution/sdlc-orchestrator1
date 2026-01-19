"""
=========================================================================
AGENTS.md Service - Static File Generator
SDLC Orchestrator - Sprint 80 (AGENTS.md Integration)

Version: 1.0.0
Date: January 19, 2026
Status: ACTIVE - Sprint 80 Implementation
Authority: Backend Lead + CTO Approved
Reference: ADR-029-AGENTS-MD-Integration-Strategy
Reference: TDS-080-001 AGENTS.md Technical Design

Purpose:
- Generate AGENTS.md from project configuration analysis
- Store generation history for audit trail
- Enforce ≤150 line limit for optimal AI context
- Validate content before generation

Layer A (Static):
- Generated content is committed to repo root
- Read by AI coding tools (Cursor, Copilot, Claude Code)
- Rarely changes (architecture, conventions only)

Zero Mock Policy: Production-ready service implementation
=========================================================================
"""

import hashlib
import logging
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.agents_md import AgentsMdFile
from app.models.project import Project
from app.services.file_analyzer import FileAnalyzer, ProjectAnalysis
from app.services.agents_md_validator import AgentsMdValidator, ValidationResult

logger = logging.getLogger(__name__)


# ============================================================================
# Data Models
# ============================================================================


class AgentsMdConfig(BaseModel):
    """Configuration for AGENTS.md generation."""

    include_quick_start: bool = True
    include_architecture: bool = True
    include_current_stage: bool = True
    include_conventions: bool = True
    include_security: bool = True
    include_git_workflow: bool = True
    include_do_not: bool = True
    max_lines: int = Field(default=150, ge=50, le=200)

    # Custom content
    custom_quick_start: Optional[str] = None
    custom_architecture: Optional[str] = None
    custom_conventions: Optional[str] = None
    custom_do_not: Optional[List[str]] = None


class AgentsMdResult(BaseModel):
    """Result of AGENTS.md generation."""

    id: Optional[UUID] = None
    content: str
    content_hash: str
    line_count: int
    sections: List[str]
    generated_at: datetime
    generator_version: str = "1.0.0"
    validation_status: str = "pending"
    validation_errors: List[dict] = []
    validation_warnings: List[dict] = []
    source_analysis: Optional[dict] = None

    class Config:
        from_attributes = True


# ============================================================================
# AgentsMdService
# ============================================================================


class AgentsMdService:
    """
    Generate and manage AGENTS.md files.

    Implements ADR-029 Static AGENTS.md layer:
    - Generates from project configuration analysis
    - Enforces ≤150 line limit (configurable)
    - Validates forbidden content (secrets, credentials)
    - Stores generation history for audit

    Usage:
        service = AgentsMdService(db, file_analyzer, validator)
        result = await service.generate(project_id, config)
        # Write result.content to AGENTS.md in repo root
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        db: AsyncSession,
        file_analyzer: Optional[FileAnalyzer] = None,
        validator: Optional[AgentsMdValidator] = None,
    ):
        """
        Initialize AgentsMdService.

        Args:
            db: Database session for storing generation records
            file_analyzer: File analyzer for project structure (optional)
            validator: Content validator (optional, created if not provided)
        """
        self.db = db
        self.file_analyzer = file_analyzer or FileAnalyzer()
        self.validator = validator or AgentsMdValidator()

    async def generate(
        self,
        project_id: UUID,
        config: Optional[AgentsMdConfig] = None,
        user_id: Optional[UUID] = None,
        project_path: Optional[str] = None,
    ) -> AgentsMdResult:
        """
        Generate AGENTS.md from project configuration.

        Args:
            project_id: Project UUID
            config: Generation configuration (optional)
            user_id: User triggering generation (for audit)
            project_path: Path to project for analysis (optional)

        Returns:
            AgentsMdResult with content and metadata

        Raises:
            ValueError: If project not found
        """
        config = config or AgentsMdConfig()

        # Get project
        project = await self._get_project(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")

        # Analyze project structure
        analysis = None
        if project_path:
            try:
                self.file_analyzer.base_path = project_path
                analysis = await self.file_analyzer.analyze_project(
                    project_id,
                    project_path,
                )
            except Exception as e:
                logger.warning(f"Project analysis failed: {e}")

        # Generate content
        content, section_names = await self._generate_content(
            project,
            config,
            analysis,
        )

        # Enforce line limit
        line_count = content.count('\n') + 1
        if line_count > config.max_lines:
            content = self._truncate_to_limit(content, config.max_lines)
            line_count = config.max_lines

        # Calculate hash
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        # Validate
        validation = self.validator.validate(content)

        # Create result
        result = AgentsMdResult(
            content=content,
            content_hash=content_hash,
            line_count=line_count,
            sections=section_names,
            generated_at=datetime.utcnow(),
            generator_version=self.VERSION,
            validation_status="valid" if validation.valid else "invalid",
            validation_errors=[e.dict() for e in validation.errors],
            validation_warnings=[w.dict() for w in validation.warnings],
            source_analysis=analysis.to_dict() if analysis else None,
        )

        # Save to database
        saved = await self._save_generation(
            project_id=project_id,
            result=result,
            user_id=user_id,
        )
        result.id = saved.id

        return result

    async def _generate_content(
        self,
        project: Project,
        config: AgentsMdConfig,
        analysis: Optional[ProjectAnalysis],
    ) -> tuple[str, List[str]]:
        """Generate AGENTS.md content."""
        sections = []
        section_names = []

        # Header
        header = f"# AGENTS.md - {project.name}\n\n"
        sections.append(header)

        # Quick Start
        if config.include_quick_start:
            qs = await self._generate_quick_start(config, analysis)
            if qs:
                sections.append(qs)
                section_names.append("Quick Start")

        # Architecture
        if config.include_architecture:
            arch = await self._generate_architecture(config, analysis)
            if arch:
                sections.append(arch)
                section_names.append("Architecture")

        # Current Stage
        if config.include_current_stage:
            stage = self._generate_current_stage()
            sections.append(stage)
            section_names.append("Current Stage")

        # Conventions
        if config.include_conventions:
            conv = await self._generate_conventions(config, analysis)
            if conv:
                sections.append(conv)
                section_names.append("Conventions")

        # Security
        if config.include_security:
            sec = await self._generate_security(config, analysis)
            if sec:
                sections.append(sec)
                section_names.append("Security")

        # Git Workflow
        if config.include_git_workflow:
            git = self._generate_git_workflow()
            sections.append(git)
            section_names.append("Git Workflow")

        # DO NOT
        if config.include_do_not:
            dont = await self._generate_do_not(config, analysis)
            if dont:
                sections.append(dont)
                section_names.append("DO NOT")

        content = "".join(sections)
        return content, section_names

    async def _generate_quick_start(
        self,
        config: AgentsMdConfig,
        analysis: Optional[ProjectAnalysis],
    ) -> str:
        """Generate Quick Start section."""
        if config.custom_quick_start:
            return f"## Quick Start\n{config.custom_quick_start}\n\n"

        commands = []

        if analysis:
            # Docker Compose
            if analysis.has_docker_compose:
                commands.append("- Full stack: `docker compose up -d`")

            # Backend
            if analysis.backend_type == "python":
                if analysis.has_poetry:
                    commands.append("- Backend only: `cd backend && poetry run pytest`")
                elif analysis.has_requirements:
                    commands.append("- Backend only: `cd backend && pip install -r requirements.txt && pytest`")
                else:
                    commands.append("- Backend only: `cd backend && pytest`")
            elif analysis.backend_type == "node":
                commands.append("- Backend only: `cd backend && npm install && npm test`")

            # Frontend
            if analysis.frontend_type and analysis.frontend_path:
                frontend_cmd = f"cd {analysis.frontend_path}"
                if analysis.frontend_type in ["react", "vue", "angular", "nextjs"]:
                    commands.append(f"- Frontend only: `{frontend_cmd} && npm install && npm run dev`")
        else:
            # Default commands when no analysis
            commands = [
                "- Full stack: `docker compose up -d`",
                "- Backend only: `cd backend && pytest`",
                "- Frontend only: `cd frontend && npm run dev`",
            ]

        if not commands:
            return ""

        return f"""## Quick Start
{chr(10).join(commands)}

"""

    async def _generate_architecture(
        self,
        config: AgentsMdConfig,
        analysis: Optional[ProjectAnalysis],
    ) -> str:
        """Generate Architecture section."""
        if config.custom_architecture:
            return f"## Architecture\n{config.custom_architecture}\n\n"

        layers = []

        if analysis:
            if analysis.has_docker_compose:
                layers.append(f"- Infrastructure: Docker Compose ({len(analysis.docker_services)} services)")
            if analysis.backend_type:
                layers.append(f"- Backend: {analysis.backend_type.title()}")
            if analysis.frontend_type:
                layers.append(f"- Frontend: {analysis.frontend_type.title()}")
            if analysis.has_database:
                layers.append(f"- Database: {analysis.database_type or 'PostgreSQL'}")

        if not layers:
            layers = ["See `/docs/02-design/` for detailed architecture documentation."]

        return f"""## Architecture
{chr(10).join(layers)}

"""

    def _generate_current_stage(self) -> str:
        """Generate Current Stage section (static note)."""
        return """## Current Stage
Check project dashboard for current SDLC stage and gate status.
Dynamic context is delivered via PR comments (not in this file).

"""

    async def _generate_conventions(
        self,
        config: AgentsMdConfig,
        analysis: Optional[ProjectAnalysis],
    ) -> str:
        """Generate Conventions section."""
        if config.custom_conventions:
            return f"## Conventions\n{config.custom_conventions}\n\n"

        conventions = []

        if analysis:
            # Python
            if analysis.backend_type == "python":
                if analysis.has_ruff:
                    conventions.append("- Python: ruff + mypy strict mode")
                elif analysis.has_flake8:
                    conventions.append("- Python: flake8 + mypy")
                else:
                    conventions.append("- Python: Follow PEP 8, type hints required")

            # TypeScript
            if analysis.has_tsconfig:
                conventions.append("- TypeScript: strict mode enabled")

            # Linting
            if analysis.has_eslint:
                conventions.append("- JavaScript/TypeScript: ESLint enforced")
            if analysis.has_prettier:
                conventions.append("- Formatting: Prettier")
        else:
            conventions = [
                "- Python: ruff + mypy strict mode",
                "- TypeScript: strict mode enabled",
            ]

        # Standard conventions (always include)
        conventions.extend([
            "- Files: snake_case (Python ≤50 chars), camelCase/PascalCase (TypeScript)",
            "- Tests: 95%+ coverage required",
        ])

        return f"""## Conventions
{chr(10).join(conventions)}

"""

    async def _generate_security(
        self,
        config: AgentsMdConfig,
        analysis: Optional[ProjectAnalysis],
    ) -> str:
        """Generate Security section."""
        rules = [
            "- OWASP ASVS L2 compliance required",
            "- No hardcoded secrets (use environment variables)",
            "- Input validation on all API endpoints",
            "- SQL injection prevention via ORM",
        ]

        # AGPL containment
        if analysis and (analysis.has_minio or analysis.has_grafana):
            rules.append("- AGPL: MinIO/Grafana network-only (NO SDK imports)")

        return f"""## Security
{chr(10).join(rules)}

"""

    def _generate_git_workflow(self) -> str:
        """Generate Git Workflow section."""
        return """## Git Workflow
- Branch: `feature/{ticket}-{description}`
- Commit: `feat|fix|chore(scope): message`
- PR: Must pass quality gates before merge

"""

    async def _generate_do_not(
        self,
        config: AgentsMdConfig,
        analysis: Optional[ProjectAnalysis],
    ) -> str:
        """Generate DO NOT section."""
        rules = config.custom_do_not or [
            "Add mocks or placeholders (Zero Mock Policy)",
            "Skip tests for 'quick fixes'",
            "Hardcode secrets or credentials",
            "Use `// TODO` without ticket reference",
        ]

        # AGPL containment
        if analysis and (analysis.has_minio or analysis.has_grafana):
            rules.append("Import AGPL libraries (MinIO SDK, Grafana SDK)")

        formatted = [f"- {r}" for r in rules]

        return f"""## DO NOT
{chr(10).join(formatted)}
"""

    def _truncate_to_limit(self, content: str, max_lines: int) -> str:
        """Truncate content to max lines while preserving structure."""
        lines = content.split('\n')
        if len(lines) <= max_lines:
            return content

        # Keep content and add truncation notice
        truncated = lines[:max_lines - 2]
        truncated.append("")
        truncated.append("<!-- Truncated to fit AI context window. See docs for full details. -->")
        return '\n'.join(truncated)

    async def _get_project(self, project_id: UUID) -> Optional[Project]:
        """Get project by ID."""
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def _save_generation(
        self,
        project_id: UUID,
        result: AgentsMdResult,
        user_id: Optional[UUID],
    ) -> AgentsMdFile:
        """Save generation record to database."""
        record = AgentsMdFile(
            project_id=project_id,
            content=result.content,
            content_hash=result.content_hash,
            line_count=result.line_count,
            sections=result.sections,
            generated_at=result.generated_at,
            generated_by=user_id,
            generator_version=result.generator_version,
            source_analysis=result.source_analysis,
            validation_status=result.validation_status,
            validation_errors=result.validation_errors,
            validation_warnings=result.validation_warnings,
        )

        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)

        return record

    async def get_latest(self, project_id: UUID) -> Optional[AgentsMdFile]:
        """Get latest AGENTS.md generation for project."""
        result = await self.db.execute(
            select(AgentsMdFile)
            .where(AgentsMdFile.project_id == project_id)
            .order_by(AgentsMdFile.generated_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_history(
        self,
        project_id: UUID,
        limit: int = 10,
    ) -> List[AgentsMdFile]:
        """Get generation history for project."""
        result = await self.db.execute(
            select(AgentsMdFile)
            .where(AgentsMdFile.project_id == project_id)
            .order_by(AgentsMdFile.generated_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    def validate_content(self, content: str) -> ValidationResult:
        """
        Validate AGENTS.md content.

        Args:
            content: Content to validate

        Returns:
            ValidationResult with errors and warnings
        """
        return self.validator.validate(content)
