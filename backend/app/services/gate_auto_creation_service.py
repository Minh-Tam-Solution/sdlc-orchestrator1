"""
=========================================================================
Gate Auto-Creation Service - BUG #7 Fix
SDLC Orchestrator - Sprint 73 Day 1

Version: 1.0.0
Date: 2026-02-10
Status: ACTIVE - Sprint 73 (Teams Integration)
Authority: Backend Lead + CTO Approved
Foundation: SDLC 5.1.2 Complete Lifecycle, Zero Mock Policy

Purpose:
- Auto-create default gates when new project is created
- Align gates with SDLC 10-stage lifecycle
- Support customizable gate templates per team
- Provide option to skip auto-creation

Bug Reference: E2E Test Report - BUG #7
Issue: Design states gates should be auto-created when project created
Actual: New projects have 0 gates, must create manually
Impact: User must manually create gates for each project

Sprint 73 Task: S73-T11A~T11G (3 SP)
- S73-T11A: Define default gate templates per project type
- S73-T11B: Create auto_create_gates() function
- S73-T11C: Hook auto_create_gates to project creation
- S73-T11D: Create default gates config in Team.settings
- S73-T11E: Add "Skip auto-creation" option
- S73-T11F: Backfill existing projects with default gates
- S73-T11G: Test auto-creation for new projects

Design References:
- Gate Model: backend/app/models/gate.py
- Project Model: backend/app/models/project.py
- Team Model: backend/app/models/team.py
- FR1: Quality Gate Management

SDLC 5.1.2 Default Gates:
Stage 01 (PLAN):   Planning Review
Stage 02 (DESIGN): Design Review
Stage 03 (BUILD):  Code Review
Stage 05 (TEST):   Test Review
Stage 06 (DEPLOY): Deploy Approval

Changelog:
- v1.0.0 (2026-02-10): Initial implementation (Sprint 73 - BUG #7 fix)
=========================================================================
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.gate import Gate
from app.models.project import Project
from app.models.team import Team
from app.models.user import User


# Default gate templates aligned with SDLC 5.1.2 10-stage lifecycle
DEFAULT_GATE_TEMPLATES = [
    {
        "name": "Planning Review",
        "gate_type": "G1_PLANNING_REVIEW",
        "stage": "01-PLAN",
        "description": "Review and approve project planning artifacts (BRD, PRD, requirements)",
        "required": True,
        "exit_criteria": [
            {
                "id": "BRD_COMPLETE",
                "description": "Business Requirements Document (BRD) complete and reviewed",
                "met": False,
            },
            {
                "id": "PRD_COMPLETE",
                "description": "Product Requirements Document (PRD) complete and reviewed",
                "met": False,
            },
            {
                "id": "STAKEHOLDER_SIGNOFF",
                "description": "Key stakeholders have signed off on requirements",
                "met": False,
            },
        ],
    },
    {
        "name": "Design Review",
        "gate_type": "G2_DESIGN_REVIEW",
        "stage": "02-DESIGN",
        "description": "Review and approve system design, architecture, and technical specifications",
        "required": True,
        "exit_criteria": [
            {
                "id": "ARCHITECTURE_APPROVED",
                "description": "System architecture document approved by CTO/Tech Lead",
                "met": False,
            },
            {
                "id": "DATA_MODEL_COMPLETE",
                "description": "Data model designed and validated",
                "met": False,
            },
            {
                "id": "API_SPEC_COMPLETE",
                "description": "API specification (OpenAPI 3.0) complete",
                "met": False,
            },
        ],
    },
    {
        "name": "Code Review",
        "gate_type": "G3_CODE_REVIEW",
        "stage": "03-BUILD",
        "description": "Review code quality, security, and adherence to standards",
        "required": True,
        "exit_criteria": [
            {
                "id": "CODE_REVIEW_PASSED",
                "description": "All pull requests reviewed and approved",
                "met": False,
            },
            {
                "id": "LINT_PASSED",
                "description": "Linting passed (ruff, ESLint)",
                "met": False,
            },
            {
                "id": "SECURITY_SCAN_PASSED",
                "description": "Security scan passed (Semgrep SAST)",
                "met": False,
            },
            {
                "id": "TEST_COVERAGE_MET",
                "description": "Test coverage meets threshold (90%+)",
                "met": False,
            },
        ],
    },
    {
        "name": "Test Review",
        "gate_type": "G5_TEST_REVIEW",
        "stage": "05-TEST",
        "description": "Review test coverage, results, and quality assurance",
        "required": True,
        "exit_criteria": [
            {
                "id": "UNIT_TESTS_PASSED",
                "description": "All unit tests passed (95%+ coverage)",
                "met": False,
            },
            {
                "id": "INTEGRATION_TESTS_PASSED",
                "description": "Integration tests passed (90%+ coverage)",
                "met": False,
            },
            {
                "id": "E2E_TESTS_PASSED",
                "description": "End-to-end tests passed (critical user journeys)",
                "met": False,
            },
            {
                "id": "LOAD_TESTS_PASSED",
                "description": "Load tests passed (100K concurrent users target)",
                "met": False,
            },
        ],
    },
    {
        "name": "Deploy Approval",
        "gate_type": "G6_DEPLOY_APPROVAL",
        "stage": "06-DEPLOY",
        "description": "Approve deployment to production environment",
        "required": True,
        "exit_criteria": [
            {
                "id": "STAGING_VALIDATED",
                "description": "Staging environment validated and smoke tests passed",
                "met": False,
            },
            {
                "id": "SECURITY_AUDIT_PASSED",
                "description": "Security audit passed (OWASP ASVS Level 2)",
                "met": False,
            },
            {
                "id": "ROLLBACK_PLAN_READY",
                "description": "Rollback plan documented and tested",
                "met": False,
            },
            {
                "id": "CTO_APPROVAL",
                "description": "CTO approval for production deployment",
                "met": False,
            },
        ],
    },
]


class GateAutoCreationService:
    """
    Service for auto-creating default gates when projects are created.

    This service implements BUG #7 fix to automatically create SDLC gates
    when a new project is created, eliminating manual gate creation burden.

    Features:
    - Auto-create 5 default gates aligned with SDLC 5.1.2
    - Support team-specific gate templates (via Team.settings)
    - Option to skip auto-creation per project
    - Backfill existing projects with gates

    Usage:
        service = GateAutoCreationService(db)
        await service.auto_create_gates(project_id, created_by, skip_auto_creation=False)
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize gate auto-creation service.

        Args:
            db: AsyncSession for database operations
        """
        self.db = db

    async def auto_create_gates(
        self,
        project_id: UUID,
        created_by: UUID,
        skip_auto_creation: bool = False,
        team_id: Optional[UUID] = None,
    ) -> List[Gate]:
        """
        Auto-create default gates for a new project.

        Creates 5 default gates aligned with SDLC 5.1.2 lifecycle:
        1. Planning Review (Stage 01-PLAN)
        2. Design Review (Stage 02-DESIGN)
        3. Code Review (Stage 03-BUILD)
        4. Test Review (Stage 05-TEST)
        5. Deploy Approval (Stage 06-DEPLOY)

        Args:
            project_id: UUID of project to create gates for
            created_by: UUID of user creating the project
            skip_auto_creation: If True, skip auto-creation (default: False)
            team_id: Optional team ID to load custom gate templates

        Returns:
            List of created Gate objects

        Raises:
            ValueError: If project not found

        Example:
            gates = await service.auto_create_gates(
                project_id=project.id,
                created_by=current_user.id,
                team_id=project.team_id,
            )
            # Returns 5 gates in DRAFT status
        """
        # Skip if requested
        if skip_auto_creation:
            return []

        # Verify project exists
        project_result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = project_result.scalar_one_or_none()
        if not project:
            raise ValueError(f"Project {project_id} not found")

        # Load gate templates (team-specific or default)
        gate_templates = await self._get_gate_templates(team_id)

        # Create gates from templates
        created_gates = []
        for template in gate_templates:
            gate = Gate(
                gate_name=f"{project.name} - {template['name']}",
                gate_type=template["gate_type"],
                stage=template["stage"],
                project_id=project_id,
                created_by=created_by,
                status="DRAFT",  # All gates start in DRAFT
                description=template["description"],
                exit_criteria=template["exit_criteria"],
            )
            self.db.add(gate)
            created_gates.append(gate)

        # Commit all gates
        await self.db.commit()

        # Refresh to get IDs and timestamps
        for gate in created_gates:
            await self.db.refresh(gate)

        return created_gates

    async def _get_gate_templates(
        self, team_id: Optional[UUID] = None
    ) -> List[Dict[str, Any]]:
        """
        Get gate templates for project creation.

        Priority:
        1. Team-specific templates (if team_id provided and team has custom templates)
        2. Default SDLC 5.1.2 templates

        Args:
            team_id: Optional team ID to load custom templates

        Returns:
            List of gate template dictionaries
        """
        # Try to load team-specific templates
        if team_id:
            team_result = await self.db.execute(
                select(Team).where(Team.id == team_id)
            )
            team = team_result.scalar_one_or_none()

            if team and team.settings:
                # Check if team has custom gate templates
                custom_templates = team.settings.get("default_gates")
                if custom_templates and isinstance(custom_templates, list):
                    return custom_templates

        # Fall back to default templates
        return DEFAULT_GATE_TEMPLATES

    async def backfill_existing_projects(
        self, user_id: UUID, dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        Backfill existing projects with default gates.

        This function is used for S73-T11F to add gates to projects
        that were created before auto-creation was implemented.

        Args:
            user_id: UUID of user performing backfill (for created_by)
            dry_run: If True, simulate backfill without creating gates (default: True)

        Returns:
            Dictionary with backfill statistics:
            {
                "total_projects": 10,
                "projects_without_gates": 5,
                "gates_created": 25,  # 5 projects * 5 gates
                "dry_run": True,
                "projects_backfilled": [
                    {"id": "uuid", "name": "Project 1", "gates_created": 5},
                    ...
                ]
            }

        Example:
            # Dry run first to see what would be created
            stats = await service.backfill_existing_projects(user_id, dry_run=True)
            print(f"Would create {stats['gates_created']} gates for {stats['projects_without_gates']} projects")

            # Actual backfill
            stats = await service.backfill_existing_projects(user_id, dry_run=False)
        """
        # Find all projects without gates
        projects_result = await self.db.execute(
            select(Project)
            .outerjoin(Gate, Project.id == Gate.project_id)
            .where(
                Project.deleted_at.is_(None),
                Gate.id.is_(None),  # No gates exist
            )
            .distinct()
        )
        projects_without_gates = projects_result.scalars().all()

        # Get total projects count
        total_projects_result = await self.db.execute(
            select(Project).where(Project.deleted_at.is_(None))
        )
        total_projects = len(total_projects_result.scalars().all())

        # Prepare statistics
        stats = {
            "total_projects": total_projects,
            "projects_without_gates": len(projects_without_gates),
            "gates_created": 0,
            "dry_run": dry_run,
            "projects_backfilled": [],
        }

        # Backfill each project
        for project in projects_without_gates:
            if not dry_run:
                # Actually create gates
                gates = await self.auto_create_gates(
                    project_id=project.id,
                    created_by=user_id,
                    skip_auto_creation=False,
                    team_id=project.team_id,
                )
                gates_created = len(gates)
            else:
                # Dry run: just count how many would be created
                templates = await self._get_gate_templates(project.team_id)
                gates_created = len(templates)

            stats["gates_created"] += gates_created
            stats["projects_backfilled"].append({
                "id": str(project.id),
                "name": project.name,
                "team_id": str(project.team_id) if project.team_id else None,
                "gates_created": gates_created,
            })

        return stats


# Convenience functions for common operations

async def create_default_gates(
    db: AsyncSession,
    project_id: UUID,
    created_by: UUID,
    skip_auto_creation: bool = False,
    team_id: Optional[UUID] = None,
) -> List[Gate]:
    """
    Convenience function to create default gates for a project.

    This is the main entry point used by the project creation API.

    Args:
        db: AsyncSession for database operations
        project_id: UUID of project to create gates for
        created_by: UUID of user creating the project
        skip_auto_creation: If True, skip auto-creation
        team_id: Optional team ID for custom templates

    Returns:
        List of created Gate objects

    Example:
        gates = await create_default_gates(
            db=db,
            project_id=project.id,
            created_by=current_user.id,
            team_id=project.team_id,
        )
    """
    service = GateAutoCreationService(db)
    return await service.auto_create_gates(
        project_id=project_id,
        created_by=created_by,
        skip_auto_creation=skip_auto_creation,
        team_id=team_id,
    )
