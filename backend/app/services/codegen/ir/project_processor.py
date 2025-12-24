"""
Project Processor - Generates project scaffold.

Sprint 46: EP-06 IR-Based Backend Scaffold Generation
ADR-023: IR-Based Deterministic Code Generation

Generates the foundational project structure including:
- app/main.py: FastAPI application entry point
- app/core/config.py: Settings configuration
- app/core/database.py: Database connection setup
- requirements.txt: Python dependencies
- Docker files: Dockerfile and docker-compose.yml
- Configuration: .env.example, .gitignore

Design Reference:
    docs/02-design/14-Technical-Specs/IR-Processor-Specification.md

Author: Backend Lead
Date: December 23, 2025
Version: 1.0.0
Status: ACTIVE - Sprint 46 Implementation
"""

from typing import Dict, Any, List
from pathlib import Path
import logging

from .processor_base import IRProcessor, ProcessorResult, GeneratedFile

logger = logging.getLogger(__name__)


class ProjectProcessor(IRProcessor):
    """
    Generates project scaffold files.

    This processor creates:
    - app/main.py: FastAPI application entry point
    - app/core/config.py: Settings configuration
    - app/core/database.py: Database connection setup
    - requirements.txt: Python dependencies
    - Dockerfile: Container build file
    - docker-compose.yml: Local development stack
    - .env.example: Environment template
    - .gitignore: Git ignore patterns

    Example:
        processor = ProjectProcessor(template_dir=Path("templates"))
        result = processor.process(normalized_ir)
        for f in result.files:
            print(f"{f.path}: {len(f.content)} chars")
    """

    @property
    def name(self) -> str:
        return "project"

    def process(self, ir: Dict[str, Any]) -> ProcessorResult:
        """
        Generate project scaffold files.

        Args:
            ir: Normalized IR (AppBlueprint)

        Returns:
            ProcessorResult with scaffold files
        """
        files: List[GeneratedFile] = []
        errors: List[str] = []

        try:
            app_name = self._get_app_name(ir)
            database = self._get_database_config(ir)
            modules = self._get_all_modules(ir)
            version = ir.get("version", "1.0.0")

            # Generate main.py
            files.append(GeneratedFile(
                path="app/main.py",
                content=self.render_template("main.py.j2", {
                    "app_name": app_name,
                    "version": version,
                    "modules": modules,
                })
            ))

            # Generate config.py
            files.append(GeneratedFile(
                path="app/core/config.py",
                content=self.render_template("config.py.j2", {
                    "app_name": app_name,
                    "database": database,
                })
            ))

            # Generate database.py
            files.append(GeneratedFile(
                path="app/core/database.py",
                content=self.render_template("database.py.j2", {
                    "database": database,
                })
            ))

            # Generate app/core/__init__.py
            files.append(GeneratedFile(
                path="app/core/__init__.py",
                content='"""Core application components."""\n'
                        'from .config import settings\n'
                        'from .database import get_db, Base, init_db\n\n'
                        '__all__ = ["settings", "get_db", "Base", "init_db"]\n'
            ))

            # Generate app/__init__.py
            files.append(GeneratedFile(
                path="app/__init__.py",
                content=f'"""{app_name} application package."""\n'
            ))

            # Generate requirements.txt
            files.append(GeneratedFile(
                path="requirements.txt",
                content=self._generate_requirements(),
                language="text"
            ))

            # Generate Docker files
            app_slug = self._to_snake_case(app_name)
            files.append(GeneratedFile(
                path="Dockerfile",
                content=self._generate_dockerfile(),
                language="dockerfile"
            ))

            files.append(GeneratedFile(
                path="docker-compose.yml",
                content=self._generate_docker_compose(app_slug, database),
                language="yaml"
            ))

            # Generate .env.example
            files.append(GeneratedFile(
                path=".env.example",
                content=self._generate_env_example(database),
                language="text"
            ))

            # Generate .gitignore
            files.append(GeneratedFile(
                path=".gitignore",
                content=self._generate_gitignore(),
                language="text"
            ))

            # Generate empty __init__.py files for packages
            for subdir in ["models", "schemas", "services", "api", "api/routes"]:
                files.append(GeneratedFile(
                    path=f"app/{subdir}/__init__.py",
                    content=f'"""{subdir.replace("/", " ").title()} package."""\n'
                ))

            logger.info(f"ProjectProcessor generated {len(files)} files")
            return ProcessorResult(success=True, files=files)

        except Exception as e:
            logger.exception(f"ProjectProcessor error: {e}")
            errors.append(f"ProjectProcessor failed: {str(e)}")
            return ProcessorResult(success=False, files=files, errors=errors)

    def _generate_requirements(self) -> str:
        """Generate requirements.txt content."""
        return """# Generated by SDLC Orchestrator EP-06 IR Processor
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.2
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.13.0
psycopg2-binary==2.9.9

# Utilities
python-dotenv==1.0.0
httpx==0.25.2
tenacity==8.2.3

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.12.0
ruff==0.1.7
mypy==1.7.1
"""

    def _generate_env_example(self, database: Dict[str, Any]) -> str:
        """Generate .env.example content."""
        db_name = database.get("name", "app")
        return f"""# Generated by SDLC Orchestrator EP-06 IR Processor
# Copy this file to .env and fill in the values

# Database
DATABASE_URL=postgresql+asyncpg://{db_name}:password@localhost:5432/{db_name}
DATABASE_ECHO=false

# Security
SECRET_KEY=change-me-in-production-use-openssl-rand-hex-32

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
"""

    def _generate_gitignore(self) -> str:
        """Generate .gitignore content."""
        return """# Generated by SDLC Orchestrator EP-06 IR Processor

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Environment
.env
.env.local
.env.*.local

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/
coverage.xml
*.cover
*.py,cover

# Mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Ruff
.ruff_cache/

# Docker
*.log

# Alembic
alembic/versions/*.pyc

# OS
.DS_Store
Thumbs.db
"""

    def _generate_dockerfile(self) -> str:
        """Generate Dockerfile content."""
        return """# Generated by SDLC Orchestrator EP-06 IR Processor
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    def _generate_docker_compose(self, app_name: str, database: Dict[str, Any]) -> str:
        """Generate docker-compose.yml content."""
        db_name = database.get("name", "app")
        return f"""# Generated by SDLC Orchestrator EP-06 IR Processor
version: '3.8'

services:
  app:
    build: .
    container_name: {app_name}_app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://{db_name}:password@db:5432/{db_name}
    depends_on:
      db:
        condition: service_healthy
    networks:
      - {app_name}_network

  db:
    image: postgres:15-alpine
    container_name: {app_name}_db
    environment:
      - POSTGRES_USER={db_name}
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB={db_name}
    volumes:
      - {app_name}_postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U {db_name}"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - {app_name}_network

networks:
  {app_name}_network:
    driver: bridge

volumes:
  {app_name}_postgres_data:
"""
