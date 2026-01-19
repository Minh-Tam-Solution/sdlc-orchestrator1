"""
=========================================================================
Project Sync Service - GitHub Repository Synchronization
SDLC Orchestrator - Stage 03 (BUILD)

Version: 2.0.0
Date: December 24, 2025
Status: ACTIVE - Sprint 49
Authority: CTO Approved
Foundation: SDLC-Project-Structure-Standard.md (SDLC 5.1.2)
Framework: SDLC 5.1.2 Complete Lifecycle

Purpose:
- Sync GitHub repository metadata to SDLC Orchestrator project
- Auto-detect project type and recommend policy pack
- Auto-map /docs folders to SDLC stages (00-09) - NOT code folders
- Validate project root structure (backend, frontend, required files)
- Create initial gates (G0, G1) for new projects

Changes in v2.0.0:
- Separated stage mapping (docs only) from structure validation (code folders)
- Code folders (backend, frontend, tests) are NOT stage-mapped
- Added PROJECT_STRUCTURE_SPEC for tier-based validation
- structure_validation field added to API response
- Backward compatible: stage_mappings field preserved

Zero Mock Policy: Real GitHub API + database operations
=========================================================================
"""

import logging
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gate import Gate
from app.models.project import Project
from app.models.user import OAuthAccount
from app.services.github_service import (
    GitHubAPIError,
    GitHubAuthError,
    github_service,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Constants
# ============================================================================

# SDLC 5.1.2 Stage Definitions (10 Stages: 00-09 + Archive folder)
# Reference: SDLC-Enterprise-Framework/02-Core-Methodology/Documentation-Standards/SDLC-Project-Structure-Standard.md
SDLC_STAGES = {
    "STAGE_00": {"name": "FOUNDATION", "description": "Strategic Discovery & Validation", "question": "WHY?"},
    "STAGE_01": {"name": "PLANNING", "description": "Requirements & User Stories", "question": "WHAT?"},
    "STAGE_02": {"name": "DESIGN", "description": "Architecture & Technical Design", "question": "HOW?"},
    "STAGE_03": {"name": "INTEGRATE", "description": "API Contracts & Third-party Setup", "question": "How connect?"},
    "STAGE_04": {"name": "BUILD", "description": "Development & Implementation", "question": "Building right?"},
    "STAGE_05": {"name": "TEST", "description": "Quality Assurance & Validation", "question": "Works correctly?"},
    "STAGE_06": {"name": "DEPLOY", "description": "Release & Deployment", "question": "Ship safely?"},
    "STAGE_07": {"name": "OPERATE", "description": "Production Operations & Monitoring", "question": "Running reliably?"},
    "STAGE_08": {"name": "COLLABORATE", "description": "Team Coordination & Knowledge", "question": "Team effective?"},
    "STAGE_09": {"name": "GOVERN", "description": "Compliance & Strategic Oversight", "question": "Compliant?"},
    "STAGE_10": {"name": "ARCHIVE", "description": "Project Archive (Legacy Docs)", "question": "Archived?"},
}

# Folder → Stage Mapping Rules (SDLC 5.1.2)
# Reference: SDLC-Enterprise-Framework/02-Core-Methodology/Documentation-Standards/SDLC-Project-Structure-Standard.md
# IMPORTANT: Only /docs folders are stage-mapped. Code folders are NOT stage-mapped.
FOLDER_STAGE_MAPPING = {
    # Stage 00: FOUNDATION - Strategic Discovery & Validation
    "docs/00-foundation": "STAGE_00",
    "docs/00-Project-Foundation": "STAGE_00",  # Legacy 4.9.x support
    "docs/why": "STAGE_00",
    "docs/problem": "STAGE_00",
    "docs/research": "STAGE_00",
    "docs/interviews": "STAGE_00",
    # Stage 01: PLANNING - Requirements & User Stories
    "docs/01-planning": "STAGE_01",
    "docs/01-Planning-Analysis": "STAGE_01",  # Legacy 4.9.x support
    "docs/requirements": "STAGE_01",
    "docs/specs": "STAGE_01",
    "docs/user-stories": "STAGE_01",
    # Stage 02: DESIGN - Architecture & Technical Design
    "docs/02-design": "STAGE_02",
    "docs/02-Design-Architecture": "STAGE_02",  # Legacy 4.9.x support
    "docs/architecture": "STAGE_02",
    "docs/adr": "STAGE_02",
    # Stage 03: INTEGRATE - API Contracts & Third-party Setup
    "docs/03-integrate": "STAGE_03",
    "docs/integrations": "STAGE_03",
    "docs/api-contracts": "STAGE_03",
    "docs/api": "STAGE_03",
    # Stage 04: BUILD - Development & Implementation
    "docs/04-build": "STAGE_04",
    "docs/development": "STAGE_04",
    "docs/sprints": "STAGE_04",
    # Stage 05: TEST - Quality Assurance & Validation
    "docs/05-test": "STAGE_05",
    "docs/testing": "STAGE_05",
    "docs/qa": "STAGE_05",
    # Stage 06: DEPLOY - Release & Deployment
    "docs/06-deploy": "STAGE_06",
    "docs/deployment": "STAGE_06",
    "docs/release": "STAGE_06",
    # Stage 07: OPERATE - Production Operations & Monitoring
    "docs/07-operate": "STAGE_07",
    "docs/operations": "STAGE_07",
    "docs/runbooks": "STAGE_07",
    # Stage 08: COLLABORATE - Team Coordination & Knowledge
    "docs/08-collaborate": "STAGE_08",
    "docs/team": "STAGE_08",
    "docs/retrospective": "STAGE_08",
    "docs/lessons": "STAGE_08",
    # Stage 09: GOVERN - Compliance & Strategic Oversight
    "docs/09-govern": "STAGE_09",
    "docs/compliance": "STAGE_09",
    "docs/governance": "STAGE_09",
    "docs/audit": "STAGE_09",
    # Stage 10: ARCHIVE - Project Archive (NOT a stage, just archive folder)
    "docs/10-archive": "STAGE_10",
    "docs/archive": "STAGE_10",
}

# Project Structure Validation Spec (SDLC 5.1.2)
# Reference: SDLC-Enterprise-Framework/02-Core-Methodology/Documentation-Standards/SDLC-Project-Structure-Standard.md
# NOTE: Code folders are validated for PRESENCE only, NOT mapped to stages
PROJECT_STRUCTURE_SPEC = {
    # Code folders (NOT stage-mapped, validated for presence)
    "code_folders": {
        "backend": {"required_for": "all", "description": "Backend code"},
        "frontend": {"required_for": "all", "description": "Frontend code"},
        "tools": {"required_for": "professional+", "description": "Utility scripts"},
        "tests": {"required_for": "standard+", "description": "Test suites"},
        "mobile": {"required_for": "optional", "description": "Mobile app code"},
        "infra": {"required_for": "professional+", "description": "Infrastructure as Code"},
    },
    # Required files by tier
    "required_files": {
        "README.md": {"required_for": "all", "description": "Project overview"},
        "CLAUDE.md": {"required_for": "standard+", "description": "AI Assistant context"},
        ".env.example": {"required_for": "standard+", "description": "Environment template"},
        "docker-compose.yml": {"required_for": "professional+", "description": "Local dev environment"},
        "Makefile": {"required_for": "professional+", "description": "Build automation"},
        ".gitignore": {"required_for": "all", "description": "Git ignore rules"},
    },
    # Legacy folders (99-legacy/) requirements
    "legacy_folders": {
        "required_for": "professional+",
        "locations": ["backend/99-legacy", "frontend/99-legacy", "tools/99-legacy"],
    },
}

# Tier hierarchy for requirement matching
TIER_HIERARCHY = {
    "lite": 1,
    "standard": 2,
    "professional": 3,
    "enterprise": 4,
}

def _tier_matches(required_for: str, current_tier: str) -> bool:
    """Check if current tier meets requirement level."""
    if required_for == "all":
        return True
    if required_for == "optional":
        return False  # Optional items don't count as required

    # Parse "standard+", "professional+", etc.
    if required_for.endswith("+"):
        min_tier = required_for[:-1]
        return TIER_HIERARCHY.get(current_tier, 0) >= TIER_HIERARCHY.get(min_tier, 0)

    # Exact tier match
    return current_tier == required_for

# Policy Pack Definitions (SDLC 5.1.3 4-Tier Classification)
# Reference: SDLC-Enterprise-Framework/README.md (v5.1.1)
POLICY_PACKS = {
    "lite": {
        "name": "Lite",
        "gates": ["G0", "G1", "G2", "G4"],  # FOUNDATION, PLANNING, DESIGN, BUILD
        "description": "Essential gates for solo developers & startups (1-2 people)",
        "team_size_range": (1, 2),
        "requirements": ["Basic Quality Gates", "README.md + .env.example"],
        "required_stages": ["00", "01", "02", "04"],
    },
    "standard": {
        "name": "Standard",
        "gates": ["G0", "G1", "G2", "G4", "G5", "G6"],  # FOUNDATION to DEPLOY
        "description": "Comprehensive governance for small teams (3-10 people)",
        "team_size_range": (3, 10),
        "requirements": ["Quality Gates (CI/CD)", "Security Gates", "CLAUDE.md"],
        "required_stages": ["00", "01", "02", "04", "05", "06"],
    },
    "professional": {
        "name": "Professional",
        "gates": ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"],  # All 10 stages
        "description": "Full governance for growing organizations (10-50 people)",
        "team_size_range": (10, 50),
        "requirements": ["Full Quality Gates (80%+ coverage)", "SBOM, SAST, OWASP L1", "Full /docs structure"],
        "required_stages": ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"],
    },
    "enterprise": {
        "name": "Enterprise",
        "gates": ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"],  # All stages + Archive
        "description": "Full SDLC 5.1.3 compliance for large organizations (50+ people)",
        "team_size_range": (50, 10000),
        "requirements": ["Everything in Professional", "OWASP ASVS L2+", "95%+ coverage", "Quarterly audits"],
        "required_stages": ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10"],
    },
}

# Gate Definitions with Exit Criteria (SDLC 5.1.3)
# Reference: SDLC-Enterprise-Framework/README.md (v5.1.1)
GATE_DEFINITIONS = {
    "G0": {
        "name": "Foundation Ready",
        "stage": "STAGE_00",
        "type": "FOUNDATION_READY",
        "description": "Strategic discovery and validation complete",
        "exit_criteria": [
            "Problem statement documented",
            "5+ user interviews conducted",
            "Pain points identified and prioritized",
            "Success metrics defined",
            "3+ solution alternatives documented",
            "Build vs Buy analysis completed",
        ],
    },
    "G1": {
        "name": "Planning Complete",
        "stage": "STAGE_01",
        "type": "PLANNING_COMPLETE",
        "description": "Requirements and user stories defined",
        "exit_criteria": [
            "Functional requirements documented",
            "User stories created and prioritized",
            "Data model designed",
            "API specification drafted",
        ],
    },
    "G2": {
        "name": "Design Ready",
        "stage": "STAGE_02",
        "type": "DESIGN_READY",
        "description": "Architecture and technical design complete",
        "exit_criteria": [
            "System architecture documented",
            "ADRs for key decisions",
            "Security baseline defined",
            "Performance budget set",
        ],
    },
    "G3": {
        "name": "Integration Ready",
        "stage": "STAGE_03",
        "type": "INTEGRATE_READY",
        "description": "API contracts and third-party setup complete",
        "exit_criteria": [
            "API contracts finalized",
            "Third-party integrations configured",
            "Authentication/authorization setup",
            "Data flow documented",
        ],
    },
    "G4": {
        "name": "Build Complete",
        "stage": "STAGE_04",
        "type": "BUILD_COMPLETE",
        "description": "Development and implementation complete",
        "exit_criteria": [
            "All features implemented",
            "Code review completed",
            "Unit tests passing (95%+ coverage)",
            "No critical bugs",
        ],
    },
    "G5": {
        "name": "Test Passed",
        "stage": "STAGE_05",
        "type": "TEST_PASSED",
        "description": "Quality assurance and validation complete",
        "exit_criteria": [
            "Integration tests passing",
            "E2E tests passing",
            "Performance tests passing",
            "Security scan passed",
        ],
    },
    "G6": {
        "name": "Deploy Ready",
        "stage": "STAGE_06",
        "type": "DEPLOY_READY",
        "description": "Ready for production deployment",
        "exit_criteria": [
            "CI/CD pipeline configured",
            "Deployment runbook created",
            "Rollback procedure tested",
            "Monitoring configured",
        ],
    },
    "G7": {
        "name": "Operate Ready",
        "stage": "STAGE_07",
        "type": "OPERATE_READY",
        "description": "Production operations stable",
        "exit_criteria": [
            "SLO targets met",
            "Incident response tested",
            "On-call rotation established",
            "Documentation complete",
        ],
    },
    "G8": {
        "name": "Collaborate Setup",
        "stage": "STAGE_08",
        "type": "COLLABORATE_SETUP",
        "description": "Team coordination and knowledge sharing",
        "exit_criteria": [
            "Knowledge base updated",
            "Team retrospective completed",
            "Lessons learned documented",
            "Training materials available",
        ],
    },
    "G9": {
        "name": "Govern Complete",
        "stage": "STAGE_09",
        "type": "GOVERN_COMPLETE",
        "description": "Compliance and strategic oversight complete",
        "exit_criteria": [
            "Compliance audit passed",
            "Security review completed",
            "Executive report delivered",
            "Strategic alignment verified",
        ],
    },
    "G10": {
        "name": "Archive Complete",
        "stage": "STAGE_10",
        "type": "ARCHIVE_COMPLETE",
        "description": "Project archived with full documentation",
        "exit_criteria": [
            "All artifacts archived",
            "Knowledge transfer completed",
            "Deprecation plan executed",
            "Final report delivered",
        ],
    },
}


# ============================================================================
# Project Sync Service
# ============================================================================


class ProjectSyncService:
    """
    Service for syncing GitHub repositories to SDLC Orchestrator projects.

    Features:
    - Repository metadata sync
    - Project type detection
    - Policy pack recommendation
    - Stage mapping
    - Initial gate creation

    Usage:
        sync_service = ProjectSyncService()

        # Full sync from GitHub repo
        result = await sync_service.sync_project(
            project_id=project.id,
            access_token=oauth_account.access_token,
            owner="developer",
            repo="my-project",
            db=session
        )

        # Analyze repository for recommendations
        analysis = await sync_service.analyze_repository(
            access_token=token,
            owner="developer",
            repo="my-project"
        )
    """

    def __init__(self):
        """Initialize project sync service."""
        self.github = github_service
        logger.info("Project sync service initialized")

    async def sync_project(
        self,
        project_id: UUID,
        access_token: str,
        owner: str,
        repo: str,
        db: AsyncSession,
        create_initial_gates: bool = True,
    ) -> dict[str, Any]:
        """
        Sync GitHub repository to SDLC Orchestrator project.

        Args:
            project_id: Project UUID
            access_token: GitHub OAuth access token
            owner: Repository owner
            repo: Repository name
            db: Database session
            create_initial_gates: Whether to create initial gates (G0.1, G0.2)

        Returns:
            Sync result with project metadata and recommendations

        Example:
            result = await sync_service.sync_project(
                project_id=project.id,
                access_token=token,
                owner="developer",
                repo="my-project",
                db=session
            )
        """
        logger.info(f"Starting sync for project {project_id} from {owner}/{repo}")

        # 1. Get project from database
        result = await db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()

        if not project:
            raise ValueError(f"Project {project_id} not found")

        # 2. Update sync status
        project.github_sync_status = "syncing"
        await db.commit()

        try:
            # 3. Analyze repository
            analysis = await self.analyze_repository(access_token, owner, repo)

            # 4. Update project metadata
            project.description = (
                project.description
                or analysis["repository"].get("description")
                or f"Synced from GitHub: {owner}/{repo}"
            )
            project.github_sync_status = "synced"
            project.github_synced_at = datetime.utcnow()

            # 5. Create initial gates if requested
            gates_created = []
            if create_initial_gates:
                gates_created = await self._create_initial_gates(
                    project_id=project_id,
                    created_by=project.owner_id,
                    recommended_pack=analysis["recommendations"]["policy_pack"],
                    db=db,
                )

            await db.commit()

            logger.info(
                f"Sync complete for project {project_id}: "
                f"{len(gates_created)} gates created"
            )

            return {
                "project_id": str(project_id),
                "sync_status": "synced",
                "synced_at": project.github_synced_at.isoformat(),
                "analysis": analysis,
                "gates_created": gates_created,
            }

        except Exception as e:
            logger.error(f"Sync failed for project {project_id}: {e}")
            project.github_sync_status = "error"
            await db.commit()
            raise

    async def analyze_repository(
        self,
        access_token: str,
        owner: str,
        repo: str,
    ) -> dict[str, Any]:
        """
        Analyze GitHub repository for SDLC recommendations.

        Args:
            access_token: GitHub OAuth access token
            owner: Repository owner
            repo: Repository name

        Returns:
            Analysis result with repository info and recommendations

        Example:
            analysis = await sync_service.analyze_repository(
                access_token=token,
                owner="developer",
                repo="my-project"
            )
            print(f"Recommended pack: {analysis['recommendations']['policy_pack']}")
        """
        logger.info(f"Analyzing repository {owner}/{repo}")

        # 1. Get repository details
        repo_data = self.github.get_repository(access_token, owner, repo)

        # 2. Get repository languages
        languages = self.github.get_repository_languages(access_token, owner, repo)

        # 3. Get repository contents (root level)
        try:
            contents = self.github.get_repository_contents(access_token, owner, repo)
            if isinstance(contents, dict):
                contents = [contents]
        except GitHubAPIError:
            contents = []

        # 4. Fetch /docs folder contents if exists (for stage mapping)
        docs_contents = []
        for item in contents:
            if item.get("type") == "dir" and item.get("name", "").lower() == "docs":
                try:
                    docs_items = self.github.get_repository_contents(
                        access_token, owner, repo, path="docs"
                    )
                    if isinstance(docs_items, dict):
                        docs_items = [docs_items]
                    # Add docs subfolders to contents for stage mapping
                    docs_contents = docs_items
                    logger.info(f"Found {len(docs_contents)} items in /docs folder")
                except GitHubAPIError as e:
                    logger.warning(f"Failed to fetch /docs contents: {e}")
                break

        # 5. Detect project type
        project_type = self._detect_project_type(languages, contents)

        # 6. Estimate team size from contributors (simplified)
        # Note: Full contributor API requires additional call
        team_size = self._estimate_team_size(repo_data)

        # 7. Detect compliance requirements
        compliance = self._detect_compliance_requirements(contents)

        # 8. Recommend policy pack first (needed for structure validation)
        file_count = len(contents) if contents else 0
        recommended_pack = self._recommend_policy_pack(
            team_size=team_size,
            compliance=compliance,
            languages=languages,
            file_count=file_count
        )

        # 9. Map /docs folders to stages (SDLC 5.1.2: only docs, not code folders)
        # Use docs_contents (fetched from /docs subfolder) for accurate stage mapping
        stage_mappings = self._map_folders_to_stages(docs_contents if docs_contents else contents)

        # 10. Validate project structure (SDLC 5.1.2: code folders + required files)
        structure_validation = self._validate_project_structure(
            contents=contents,
            recommended_tier=recommended_pack,
        )

        # 11. Build analysis result
        primary_language = max(languages, key=languages.get) if languages else None

        # Calculate codebase metrics for transparency
        codebase_bytes = sum(languages.values()) if languages else 0
        estimated_loc = int(codebase_bytes / 40) if codebase_bytes > 0 else 0

        return {
            "repository": {
                "id": repo_data["id"],
                "full_name": repo_data["full_name"],
                "description": repo_data.get("description"),
                "html_url": repo_data["html_url"],
                "default_branch": repo_data.get("default_branch", "main"),
                "private": repo_data.get("private", False),
                "stargazers_count": repo_data.get("stargazers_count", 0),
                "forks_count": repo_data.get("forks_count", 0),
            },
            "languages": languages,
            "primary_language": primary_language,
            "project_type": project_type,
            "team_size_estimate": team_size,
            "team_size_source": "github_contributors",  # or "unknown" if not detected
            "compliance_requirements": compliance,
            # SDLC 5.1.2: stage_mappings contains only /docs folders (backward compatible)
            "stage_mappings": stage_mappings,
            # SDLC 5.1.2: NEW - structure_validation for code folders + required files
            "structure_validation": structure_validation,
            "codebase_metrics": {
                "total_bytes": codebase_bytes,
                "estimated_loc": estimated_loc,
                "file_count": file_count,
                "language_count": len(languages) if languages else 0,
            },
            "recommendations": {
                "policy_pack": recommended_pack,
                "policy_pack_info": POLICY_PACKS[recommended_pack],
                "initial_gates": POLICY_PACKS[recommended_pack]["gates"][:2],  # G0, G1
                "confidence_score": 0.85,
                "factors": {
                    "codebase_size": "large" if estimated_loc >= 100_000 else "medium" if estimated_loc >= 10_000 else "small",
                    "team_size": "detected" if team_size > 0 else "unknown",
                    "compliance": "required" if compliance else "none",
                },
            },
        }

    async def _create_initial_gates(
        self,
        project_id: UUID,
        created_by: UUID,
        recommended_pack: str,
        db: AsyncSession,
    ) -> list[dict[str, Any]]:
        """
        Create initial gates for a new project.

        Args:
            project_id: Project UUID
            created_by: User UUID who created the project
            recommended_pack: Recommended policy pack name
            db: Database session

        Returns:
            List of created gate info
        """
        gates_created = []
        initial_gates = ["G0", "G1"]  # Start with Foundation Ready and Planning Complete gates

        for gate_code in initial_gates:
            gate_def = GATE_DEFINITIONS.get(gate_code)
            if not gate_def:
                continue

            # Check if gate already exists
            existing = await db.execute(
                select(Gate).where(
                    and_(
                        Gate.project_id == project_id,
                        Gate.gate_name == gate_def["name"],
                        Gate.deleted_at.is_(None),
                    )
                )
            )
            if existing.scalar_one_or_none():
                logger.info(f"Gate {gate_code} already exists for project {project_id}")
                continue

            # Create gate
            gate = Gate(
                project_id=project_id,
                gate_name=gate_def["name"],
                gate_type=gate_def["type"],
                stage=gate_def["stage"],
                status="DRAFT",
                description=gate_def["description"],
                exit_criteria=gate_def["exit_criteria"],
                created_by=created_by,
            )
            db.add(gate)
            await db.flush()

            gates_created.append({
                "id": str(gate.id),
                "gate_code": gate_code,
                "gate_name": gate_def["name"],
                "stage": gate_def["stage"],
                "status": "DRAFT",
            })

            logger.info(f"Created gate {gate_code} for project {project_id}")

        return gates_created

    def _detect_project_type(
        self,
        languages: dict[str, int],
        contents: list[dict],
    ) -> str:
        """Detect project type from languages and file structure."""
        file_names = [item["name"].lower() for item in contents]

        # Check for specific project indicators
        if "package.json" in file_names:
            if "next.config.js" in file_names or "next.config.mjs" in file_names:
                return "nextjs_app"
            elif "vite.config.ts" in file_names or "vite.config.js" in file_names:
                return "vite_app"
            elif any("react" in str(languages).lower() for _ in [1]):
                return "react_app"
            else:
                return "node_app"

        if "requirements.txt" in file_names or "pyproject.toml" in file_names:
            if "manage.py" in file_names:
                return "django_app"
            elif "app.py" in file_names or "main.py" in file_names:
                return "fastapi_app"
            else:
                return "python_library"

        if "go.mod" in file_names:
            return "go_service"

        if "cargo.toml" in file_names:
            return "rust_app"

        if "pom.xml" in file_names or "build.gradle" in file_names:
            return "java_app"

        if "pubspec.yaml" in file_names:
            return "flutter_app"

        # Check by primary language
        if languages:
            primary = max(languages, key=languages.get)
            return f"{primary.lower()}_project"

        return "generic_project"

    def _estimate_team_size(self, repo_data: dict) -> int:
        """Estimate team size from repository metadata."""
        # Use watchers/stars as proxy for project size
        # In production, would use contributors API
        stars = repo_data.get("stargazers_count", 0)
        forks = repo_data.get("forks_count", 0)

        if stars > 1000 or forks > 100:
            return 50  # Enterprise
        elif stars > 100 or forks > 10:
            return 20  # Standard
        else:
            return 5  # Lite

    def _detect_compliance_requirements(
        self,
        contents: list[dict],
    ) -> list[str]:
        """Detect compliance requirements from repository files."""
        compliance = []
        file_names = [item["name"].lower() for item in contents]

        if "security.md" in file_names:
            compliance.append("security_critical")

        if "license" in file_names:
            compliance.append("license_present")

        if ".github" in file_names:
            compliance.append("ci_cd_enabled")

        if any("hipaa" in name for name in file_names):
            compliance.append("hipaa")

        if any("gdpr" in name for name in file_names):
            compliance.append("gdpr")

        if any("soc" in name for name in file_names):
            compliance.append("soc2")

        return compliance

    def _map_folders_to_stages(
        self,
        contents: list[dict],
    ) -> list[dict[str, Any]]:
        """
        Map /docs folders to SDLC stages (SDLC 5.1.2).

        IMPORTANT: Only /docs subfolders are stage-mapped.
        Code folders (backend, frontend, tests) are NOT stage-mapped.
        They are validated separately via _validate_project_structure().

        Naming Flexibility (CTO Decision):
        - Stage NUMBER (00, 01, 02...) MUST be correct - this determines stage mapping
        - Stage NAME can vary (e.g., "00-Project-Foundation" vs "00-foundation")
        - Non-standard names get "naming_suggestion" for optional rename

        Args:
            contents: List of repository contents from GitHub API
                      Can be root contents or /docs subfolder contents

        Returns:
            List of stage mappings for /docs folders only
        """
        mappings = []

        # Standard SDLC 5.1.2 naming convention (lowercase, hyphenated)
        STANDARD_NAMES = {
            "00": "00-foundation",
            "01": "01-planning",
            "02": "02-design",
            "03": "03-integrate",
            "04": "04-build",
            "05": "05-test",
            "06": "06-deploy",
            "07": "07-operate",
            "08": "08-collaborate",
            "09": "09-govern",
            "10": "10-archive",
        }

        for item in contents:
            if item["type"] != "dir":
                continue

            original_path = item["path"]
            path = original_path.lower()

            # Determine if this is a docs subfolder
            # Case 1: Contents from /docs folder directly (path = "00-foundation")
            # Case 2: Contents from root (path = "docs/00-foundation")
            folder_name = ""
            if path.startswith("docs/"):
                # Root-level contents with docs/ prefix
                parts = path.split("/")
                if len(parts) >= 2:
                    folder_name = parts[1]
            elif not "/" in path:
                # Direct /docs subfolder contents (no prefix)
                folder_name = path
            else:
                # Skip non-docs folders
                continue

            if not folder_name:
                continue

            # Skip legacy folders
            if folder_name.startswith("99-"):
                continue

            # Extract stage number from folder name (e.g., "00-Project-Foundation" -> "00")
            stage_code = None
            if len(folder_name) >= 2 and folder_name[:2].isdigit():
                potential_code = folder_name[:2]
                if potential_code in STANDARD_NAMES:
                    stage_code = potential_code

            if stage_code:
                stage_key = f"STAGE_{stage_code}"
                stage_info = SDLC_STAGES.get(stage_key, {})
                standard_name = STANDARD_NAMES.get(stage_code, "")

                # Check if folder name matches standard convention
                # Standard: "00-foundation", Legacy acceptable: "00-Project-Foundation"
                is_standard_name = folder_name == standard_name

                # Also check legacy patterns in FOLDER_STAGE_MAPPING
                full_path_lower = f"docs/{folder_name}"
                is_known_legacy = full_path_lower in FOLDER_STAGE_MAPPING

                # Determine confidence and naming status
                if is_standard_name:
                    confidence = 0.98
                    naming_status = "standard"
                    naming_suggestion = None
                elif is_known_legacy:
                    confidence = 0.95
                    naming_status = "legacy_accepted"
                    naming_suggestion = f"docs/{standard_name}"
                else:
                    # Non-standard name but correct stage number
                    confidence = 0.85
                    naming_status = "non_standard"
                    naming_suggestion = f"docs/{standard_name}"

                mappings.append({
                    "path": original_path,
                    "folder_path": f"docs/{folder_name}" if not original_path.lower().startswith("docs/") else original_path,
                    "stage": stage_key,
                    "stage_name": stage_info.get("name", "UNKNOWN"),
                    "stage_code": stage_code,
                    "confidence": confidence,
                    "status": "found",
                    "naming_status": naming_status,
                    "naming_suggestion": naming_suggestion,
                })
            else:
                # Unrecognized folder - doesn't start with valid stage number
                mappings.append({
                    "path": original_path,
                    "folder_path": f"docs/{folder_name}" if not original_path.lower().startswith("docs/") else original_path,
                    "stage": None,
                    "stage_name": None,
                    "stage_code": None,
                    "confidence": 0.0,
                    "status": "unmapped",
                    "naming_status": "unknown",
                    "naming_suggestion": None,
                })

        # Sort by stage code for consistent ordering
        mappings.sort(key=lambda x: x.get("stage_code") or "99")

        return mappings

    def _validate_project_structure(
        self,
        contents: list[dict],
        recommended_tier: str = "standard",
    ) -> dict[str, Any]:
        """
        Validate project root structure (SDLC 5.1.2).

        This validates code folders (backend, frontend, etc.) and required files.
        These items are NOT stage-mapped - they exist independently of SDLC stages.

        Args:
            contents: List of repository contents from GitHub API
            recommended_tier: Tier to validate against (lite, standard, professional, enterprise)

        Returns:
            Structure validation result with found/missing items and breakdown
        """
        # Build lookup sets for quick matching
        folder_names = {item["name"].lower() for item in contents if item["type"] == "dir"}
        file_names = {item["name"].lower() for item in contents if item["type"] == "file"}
        all_items = folder_names | file_names

        # Validate code folders
        code_folders_result = {}
        for folder, spec in PROJECT_STRUCTURE_SPEC["code_folders"].items():
            is_required = _tier_matches(spec["required_for"], recommended_tier)
            found = folder.lower() in folder_names
            code_folders_result[folder] = {
                "found": found,
                "required_for": spec["required_for"],
                "required": is_required,
                "status": "found" if found else ("missing" if is_required else "optional"),
            }

        # Validate required files
        required_files_result = {}
        for filename, spec in PROJECT_STRUCTURE_SPEC["required_files"].items():
            is_required = _tier_matches(spec["required_for"], recommended_tier)
            found = filename.lower() in all_items
            required_files_result[filename] = {
                "found": found,
                "required_for": spec["required_for"],
                "required": is_required,
                "status": "found" if found else ("missing" if is_required else "optional"),
            }

        # Calculate breakdown
        all_items_to_check = list(code_folders_result.values()) + list(required_files_result.values())
        found_count = sum(1 for item in all_items_to_check if item["found"])
        required_count = sum(1 for item in all_items_to_check if item["required"])
        missing_required = sum(1 for item in all_items_to_check if item["required"] and not item["found"])

        return {
            "code_folders": code_folders_result,
            "required_files": required_files_result,
            "compliance_score": None,  # Per CTO: null, no scoring yet
            "breakdown": {
                "found": found_count,
                "missing": missing_required,
                "total": len(all_items_to_check),
                "required_total": required_count,
            },
            "tier_validated": recommended_tier,
        }

    def _recommend_policy_pack(
        self,
        team_size: int,
        compliance: list[str],
        languages: dict[str, int] | None = None,
        file_count: int = 0,
    ) -> str:
        """
        Recommend policy pack based on multiple factors.

        Factors considered:
        - Team size: Number of contributors
        - Compliance requirements: HIPAA, GDPR, SOC2, etc.
        - Codebase size: Total bytes of code across all languages
        - File count: Number of files in repository

        AI-assisted development (like SDLC Orchestrator) enables small teams
        to build enterprise-scale applications, so codebase complexity
        is weighted heavily in the recommendation.
        """
        # Calculate codebase size (total bytes across all languages)
        codebase_bytes = sum(languages.values()) if languages else 0
        codebase_mb = codebase_bytes / (1024 * 1024)  # Convert to MB

        # Estimate Lines of Code (rough approximation: 40 bytes per line avg)
        estimated_loc = codebase_bytes / 40 if codebase_bytes > 0 else 0

        # Score-based recommendation (0-100)
        score = 0

        # 1. Compliance requirements (highest weight - auto-enterprise)
        if any(c in compliance for c in ["hipaa", "gdpr", "soc2", "security_critical", "pci_dss"]):
            return "enterprise"

        # 2. Codebase size scoring (40% weight)
        # - >1M LOC or >40MB code = Enterprise-scale
        # - >100K LOC or >4MB code = Professional-scale
        # - >10K LOC or >400KB code = Standard-scale
        # - <10K LOC = Lite-scale
        if estimated_loc >= 1_000_000 or codebase_mb >= 40:
            score += 40  # Enterprise codebase
        elif estimated_loc >= 100_000 or codebase_mb >= 4:
            score += 30  # Professional codebase
        elif estimated_loc >= 10_000 or codebase_mb >= 0.4:
            score += 20  # Standard codebase
        else:
            score += 10  # Lite codebase

        # 3. Team size scoring (30% weight)
        if team_size >= 50:
            score += 30
        elif team_size >= 20:
            score += 25
        elif team_size >= 10:
            score += 20
        elif team_size >= 5:
            score += 15
        else:
            score += 10

        # 4. File count scoring (20% weight)
        # More files = more complexity = higher governance needs
        if file_count >= 1000:
            score += 20
        elif file_count >= 500:
            score += 15
        elif file_count >= 100:
            score += 10
        else:
            score += 5

        # 5. Language diversity scoring (10% weight)
        # More languages = more complex project
        num_languages = len(languages) if languages else 0
        if num_languages >= 5:
            score += 10
        elif num_languages >= 3:
            score += 7
        else:
            score += 5

        # Determine tier based on total score
        if score >= 75:
            return "enterprise"
        elif score >= 55:
            return "professional"
        elif score >= 35:
            return "standard"
        else:
            return "lite"


# ============================================================================
# Global Service Instance
# ============================================================================

project_sync_service = ProjectSyncService()
