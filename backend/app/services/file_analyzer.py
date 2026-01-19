"""
=========================================================================
File Analyzer Service - Project Structure Analysis
SDLC Orchestrator - Sprint 80 (AGENTS.md Integration)

Version: 1.0.0
Date: January 19, 2026
Status: ACTIVE - Sprint 80 Implementation
Authority: Backend Lead + CTO Approved
Reference: ADR-029-AGENTS-MD-Integration-Strategy
Reference: TDS-080-001 AGENTS.md Technical Design

Purpose:
- Analyze project file structure for AGENTS.md generation
- Detect frameworks, languages, and configurations
- Extract setup commands from docker-compose, package.json, etc.
- Identify security-related configurations (AGPL deps, etc.)

Security:
- Read-only file access
- No execution of discovered scripts
- Safe path traversal prevention

Zero Mock Policy: Production-ready file analysis implementation
=========================================================================
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any
from uuid import UUID

import yaml

logger = logging.getLogger(__name__)


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class ProjectAnalysis:
    """
    Result of project structure analysis.

    Contains detected configurations, frameworks, and tools
    that inform AGENTS.md generation.
    """

    # Project basics
    project_id: UUID
    project_path: str
    analyzed_at: str

    # Docker
    has_docker_compose: bool = False
    docker_services: List[str] = field(default_factory=list)

    # Backend
    backend_type: Optional[str] = None  # python, node, go, java, etc.
    backend_path: str = "backend"
    has_requirements: bool = False
    has_poetry: bool = False
    has_pipfile: bool = False
    has_pyproject: bool = False

    # Frontend
    frontend_type: Optional[str] = None  # react, vue, angular, svelte, etc.
    frontend_path: Optional[str] = None
    has_package_json: bool = False

    # Database
    has_database: bool = False
    database_type: Optional[str] = None  # postgresql, mysql, mongodb, etc.

    # Configuration files
    has_tsconfig: bool = False
    has_ruff: bool = False
    has_flake8: bool = False
    has_eslint: bool = False
    has_prettier: bool = False
    has_editorconfig: bool = False

    # CI/CD
    has_github_actions: bool = False
    has_gitlab_ci: bool = False
    has_dockerfile: bool = False

    # AGPL dependencies (important for SDLC Orchestrator)
    has_minio: bool = False
    has_grafana: bool = False
    has_agpl_deps: bool = False

    # Documentation
    has_docs_folder: bool = False
    has_readme: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "project_id": str(self.project_id),
            "project_path": self.project_path,
            "analyzed_at": self.analyzed_at,
            "has_docker_compose": self.has_docker_compose,
            "docker_services": self.docker_services,
            "backend_type": self.backend_type,
            "backend_path": self.backend_path,
            "has_requirements": self.has_requirements,
            "has_poetry": self.has_poetry,
            "frontend_type": self.frontend_type,
            "frontend_path": self.frontend_path,
            "has_database": self.has_database,
            "database_type": self.database_type,
            "has_tsconfig": self.has_tsconfig,
            "has_ruff": self.has_ruff,
            "has_eslint": self.has_eslint,
            "has_minio": self.has_minio,
            "has_grafana": self.has_grafana,
            "has_agpl_deps": self.has_agpl_deps,
            "has_github_actions": self.has_github_actions,
        }


# ============================================================================
# FileAnalyzer Service
# ============================================================================


class FileAnalyzer:
    """
    Analyze project file structure for AGENTS.md generation.

    Scans project directories to detect:
    - Languages and frameworks (Python, TypeScript, React, etc.)
    - Build tools (Docker, npm, poetry, etc.)
    - Configuration files (ruff, eslint, tsconfig, etc.)
    - Database types (PostgreSQL, MySQL, MongoDB, etc.)
    - AGPL dependencies (MinIO, Grafana) for compliance

    Usage:
        analyzer = FileAnalyzer()
        analysis = await analyzer.analyze_project(project_id, "/path/to/project")
    """

    # Common paths to check
    BACKEND_PATHS = ["backend", "api", "server", "src", "app"]
    FRONTEND_PATHS = ["frontend", "web", "client", "ui", "frontend/web"]

    # Framework detection patterns
    PYTHON_INDICATORS = [
        "requirements.txt",
        "pyproject.toml",
        "Pipfile",
        "setup.py",
        "poetry.lock",
    ]

    NODE_INDICATORS = [
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
    ]

    REACT_INDICATORS = [
        "src/App.tsx",
        "src/App.jsx",
        "src/index.tsx",
        "src/index.jsx",
    ]

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize FileAnalyzer.

        Args:
            base_path: Optional base path for all project lookups
        """
        self.base_path = Path(base_path) if base_path else None

    async def analyze_project(
        self,
        project_id: UUID,
        project_path: Optional[str] = None,
    ) -> ProjectAnalysis:
        """
        Analyze project structure.

        Args:
            project_id: Project UUID
            project_path: Path to project root

        Returns:
            ProjectAnalysis with detected configurations
        """
        from datetime import datetime

        path = Path(project_path) if project_path else self.base_path
        if not path:
            raise ValueError("No project path provided")

        analysis = ProjectAnalysis(
            project_id=project_id,
            project_path=str(path),
            analyzed_at=datetime.utcnow().isoformat(),
        )

        # Check Docker
        await self._analyze_docker(path, analysis)

        # Check backend
        await self._analyze_backend(path, analysis)

        # Check frontend
        await self._analyze_frontend(path, analysis)

        # Check config files
        await self._analyze_configs(path, analysis)

        # Check CI/CD
        await self._analyze_cicd(path, analysis)

        # Check documentation
        await self._analyze_docs(path, analysis)

        # Determine AGPL status
        analysis.has_agpl_deps = analysis.has_minio or analysis.has_grafana

        return analysis

    async def _analyze_docker(self, path: Path, analysis: ProjectAnalysis) -> None:
        """Analyze Docker configuration."""
        docker_compose = path / "docker-compose.yml"
        docker_compose_alt = path / "docker-compose.yaml"

        compose_file = None
        if docker_compose.exists():
            compose_file = docker_compose
        elif docker_compose_alt.exists():
            compose_file = docker_compose_alt

        if compose_file:
            analysis.has_docker_compose = True

            try:
                with open(compose_file, 'r') as f:
                    compose_content = yaml.safe_load(f)

                if compose_content and 'services' in compose_content:
                    services = compose_content['services']
                    analysis.docker_services = list(services.keys())

                    # Check for specific services
                    for service_name, service_config in services.items():
                        service_str = str(service_config).lower()
                        name_lower = service_name.lower()

                        # Database detection
                        if any(db in name_lower or db in service_str
                               for db in ['postgres', 'postgresql']):
                            analysis.has_database = True
                            analysis.database_type = "postgresql"
                        elif any(db in name_lower or db in service_str
                                 for db in ['mysql', 'mariadb']):
                            analysis.has_database = True
                            analysis.database_type = "mysql"
                        elif 'mongo' in name_lower or 'mongo' in service_str:
                            analysis.has_database = True
                            analysis.database_type = "mongodb"

                        # AGPL detection
                        if 'minio' in name_lower or 'minio' in service_str:
                            analysis.has_minio = True
                        if 'grafana' in name_lower or 'grafana' in service_str:
                            analysis.has_grafana = True

            except Exception as e:
                logger.warning(f"Failed to parse docker-compose: {e}")

        # Check for Dockerfile
        if (path / "Dockerfile").exists():
            analysis.has_dockerfile = True

    async def _analyze_backend(self, path: Path, analysis: ProjectAnalysis) -> None:
        """Analyze backend configuration."""
        # Find backend path
        backend_path = None
        for bp in self.BACKEND_PATHS:
            if (path / bp).is_dir():
                backend_path = path / bp
                analysis.backend_path = bp
                break

        if not backend_path:
            backend_path = path  # Use root if no backend folder

        # Check for Python
        for indicator in self.PYTHON_INDICATORS:
            check_paths = [backend_path / indicator, path / indicator]
            for check_path in check_paths:
                if check_path.exists():
                    analysis.backend_type = "python"

                    if "requirements" in indicator:
                        analysis.has_requirements = True
                    elif "pyproject" in indicator:
                        analysis.has_pyproject = True
                    elif "poetry" in indicator:
                        analysis.has_poetry = True
                    elif "Pipfile" in indicator:
                        analysis.has_pipfile = True
                    break

        # Check for Node.js backend
        if not analysis.backend_type:
            for indicator in self.NODE_INDICATORS:
                if (backend_path / indicator).exists():
                    analysis.backend_type = "node"
                    break

    async def _analyze_frontend(self, path: Path, analysis: ProjectAnalysis) -> None:
        """Analyze frontend configuration."""
        # Find frontend path
        frontend_path = None
        for fp in self.FRONTEND_PATHS:
            check_path = path / fp
            if check_path.is_dir():
                # Check if it has package.json (actual frontend)
                if (check_path / "package.json").exists():
                    frontend_path = check_path
                    analysis.frontend_path = fp
                    analysis.has_package_json = True
                    break

        if not frontend_path:
            # Check root for package.json
            if (path / "package.json").exists():
                frontend_path = path
                analysis.frontend_path = "."
                analysis.has_package_json = True

        if frontend_path:
            # Detect framework
            package_json = frontend_path / "package.json"
            if package_json.exists():
                try:
                    import json
                    with open(package_json, 'r') as f:
                        pkg = json.load(f)

                    deps = {
                        **pkg.get('dependencies', {}),
                        **pkg.get('devDependencies', {}),
                    }

                    if 'react' in deps or 'react-dom' in deps:
                        analysis.frontend_type = "react"
                    elif 'vue' in deps:
                        analysis.frontend_type = "vue"
                    elif '@angular/core' in deps:
                        analysis.frontend_type = "angular"
                    elif 'svelte' in deps:
                        analysis.frontend_type = "svelte"
                    elif 'next' in deps:
                        analysis.frontend_type = "nextjs"
                    else:
                        analysis.frontend_type = "javascript"

                except Exception as e:
                    logger.warning(f"Failed to parse package.json: {e}")

    async def _analyze_configs(self, path: Path, analysis: ProjectAnalysis) -> None:
        """Analyze configuration files."""
        # TypeScript
        analysis.has_tsconfig = (
            (path / "tsconfig.json").exists() or
            (path / "frontend" / "tsconfig.json").exists() or
            (path / "frontend" / "web" / "tsconfig.json").exists()
        )

        # Python linting
        analysis.has_ruff = (
            (path / "ruff.toml").exists() or
            (path / "pyproject.toml").exists() and
            self._pyproject_has_ruff(path / "pyproject.toml")
        )

        analysis.has_flake8 = (
            (path / ".flake8").exists() or
            (path / "setup.cfg").exists()
        )

        # JavaScript linting
        analysis.has_eslint = (
            (path / ".eslintrc").exists() or
            (path / ".eslintrc.js").exists() or
            (path / ".eslintrc.json").exists() or
            (path / "eslint.config.js").exists()
        )

        analysis.has_prettier = (
            (path / ".prettierrc").exists() or
            (path / ".prettierrc.json").exists() or
            (path / "prettier.config.js").exists()
        )

        # Editor config
        analysis.has_editorconfig = (path / ".editorconfig").exists()

    def _pyproject_has_ruff(self, pyproject_path: Path) -> bool:
        """Check if pyproject.toml has ruff configuration."""
        try:
            import tomllib
            with open(pyproject_path, 'rb') as f:
                data = tomllib.load(f)
            return 'tool' in data and 'ruff' in data['tool']
        except Exception:
            return False

    async def _analyze_cicd(self, path: Path, analysis: ProjectAnalysis) -> None:
        """Analyze CI/CD configuration."""
        # GitHub Actions
        github_workflows = path / ".github" / "workflows"
        analysis.has_github_actions = (
            github_workflows.is_dir() and
            any(github_workflows.glob("*.yml")) or
            any(github_workflows.glob("*.yaml"))
        ) if github_workflows.exists() else False

        # GitLab CI
        analysis.has_gitlab_ci = (path / ".gitlab-ci.yml").exists()

    async def _analyze_docs(self, path: Path, analysis: ProjectAnalysis) -> None:
        """Analyze documentation."""
        # Docs folder
        analysis.has_docs_folder = (path / "docs").is_dir()

        # README
        analysis.has_readme = (
            (path / "README.md").exists() or
            (path / "README.rst").exists() or
            (path / "README.txt").exists()
        )

    async def exists(self, project_id: UUID, relative_path: str) -> bool:
        """
        Check if a file exists in the project.

        Args:
            project_id: Project UUID (used for multi-project setups)
            relative_path: Path relative to project root

        Returns:
            True if file exists
        """
        if not self.base_path:
            return False

        full_path = self.base_path / relative_path
        return full_path.exists()

    async def read(self, project_id: UUID, relative_path: str) -> str:
        """
        Read file content from project.

        Args:
            project_id: Project UUID
            relative_path: Path relative to project root

        Returns:
            File content as string
        """
        if not self.base_path:
            raise ValueError("No base path configured")

        full_path = self.base_path / relative_path
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")

        # Security: prevent path traversal
        try:
            full_path.resolve().relative_to(self.base_path.resolve())
        except ValueError:
            raise ValueError("Path traversal not allowed")

        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
