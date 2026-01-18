"""
=========================================================================
SASE Sprint Integration - Sprint Context for SASE Workflows
SDLC Orchestrator - Sprint 76 (GAP 3 Resolution)

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 76 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P5 (SASE Integration)
Reference: SPRINT-76-SASE-WORKFLOW-INTEGRATION.md

Purpose:
- Provide sprint context to SASE approval workflows
- Enable team membership verification for SASE policies
- Support sprint-aware deployment authorization

GAP 3 Resolution:
- SASE policies can now access sprint team members and roles
- Sprint phase and roadmap context available for traceability
- Sprint gate status (G-Sprint, G-Sprint-Close) for deployment decisions

Security Standards:
- Row-Level Security compliance (project-scoped access)
- Audit trail for all authorization decisions
- SE4H Coach validation for gate approvals

Performance Targets:
- get_sprint_context: <50ms (with eager loading)
- is_requester_in_sprint_team: <30ms
- can_requester_deploy: <50ms

Zero Mock Policy: Production-ready service with real database queries
=========================================================================
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.phase import Phase
from app.models.project import Project
from app.models.roadmap import Roadmap
from app.models.sprint import Sprint
from app.models.team import Team
from app.models.team_member import TeamMember
from app.schemas.sase import (
    SprintContext,
    TeamMemberContext,
    PhaseContext,
    GateStatusContext,
    DeploymentCheckRequest,
    DeploymentCheckResponse,
)


logger = logging.getLogger(__name__)


class SprintContextProviderError(Exception):
    """Base exception for SprintContextProvider."""
    pass


class SprintNotFoundError(SprintContextProviderError):
    """Sprint not found."""
    def __init__(self, sprint_id: UUID):
        self.sprint_id = sprint_id
        super().__init__(f"Sprint {sprint_id} not found")


class SprintContextProvider:
    """
    Provides sprint context to SASE approval workflows.

    GAP 3 Resolution: SASE policies can now access:
    - Sprint team members and roles
    - Sprint phase and roadmap context
    - Sprint gate status (G-Sprint, G-Sprint-Close)
    - Project information

    This service is the bridge between sprint planning and SASE policy
    evaluation, enabling sprint-aware authorization decisions.

    Usage:
        provider = SprintContextProvider(db)
        context = await provider.get_sprint_context(sprint_id)

        # Use in SASE policy evaluation
        opa_input = {
            "sprint_context": context.model_dump(),
            "requester_id": str(requester_id),
            "action": "deploy_staging",
        }
        result = await opa_service.evaluate(opa_input)

    SDLC 5.1.3 Compliance:
        - Rule #3: Sprint Planning Requires Approval (G-Sprint gate check)
        - Rule #2: Post-Sprint Documentation (G-Sprint-Close gate check)
        - SE4H Coach: Only human owners/admins can approve gates

    Attributes:
        db: AsyncSession for database operations
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize SprintContextProvider.

        Args:
            db: SQLAlchemy async session for database operations
        """
        self.db = db

    async def get_sprint_context(
        self,
        sprint_id: UUID,
    ) -> Optional[SprintContext]:
        """
        Get comprehensive sprint context for SASE policy evaluation.

        Loads sprint with all required relations using eager loading
        for optimal performance (single query with JOINs).

        Relations loaded:
        - Sprint → Phase → Roadmap
        - Sprint → Project → Team → Members → User

        Args:
            sprint_id: Sprint UUID

        Returns:
            SprintContext or None if sprint not found

        Performance:
            - Target: <50ms with eager loading
            - Uses selectinload for efficient relation loading
        """
        result = await self.db.execute(
            select(Sprint)
            .options(
                selectinload(Sprint.phase).selectinload(Phase.roadmap),
                selectinload(Sprint.project)
                .selectinload(Project.team)
                .selectinload(Team.members)
                .selectinload(TeamMember.user),
            )
            .where(Sprint.id == sprint_id)
        )
        sprint = result.scalar_one_or_none()

        if not sprint:
            logger.debug(f"Sprint {sprint_id} not found")
            return None

        # Build team member context
        team_members = []
        if sprint.project.team:
            for member in sprint.project.team.members:
                if member.deleted_at is None:
                    team_members.append(
                        TeamMemberContext(
                            user_id=member.user_id,
                            role=member.role,
                            can_approve_gates=member.can_approve_sprint_gate,
                            can_manage_backlog=member.can_manage_backlog,
                        )
                    )

        # Build phase context
        phase_context = None
        if sprint.phase:
            phase_context = PhaseContext(
                id=sprint.phase.id,
                name=sprint.phase.name,
                number=sprint.phase.number,
                roadmap_id=sprint.phase.roadmap_id,
            )

        # Build gate status context
        gates = GateStatusContext(
            g_sprint=sprint.g_sprint_status or "pending",
            g_sprint_close=sprint.g_sprint_close_status or "pending",
        )

        # Build sprint context
        context = SprintContext(
            sprint_id=sprint.id,
            sprint_number=sprint.number,
            sprint_name=sprint.name,
            project_id=sprint.project_id,
            project_name=sprint.project.name,
            team_id=sprint.project.team.id if sprint.project.team else None,
            team_name=sprint.project.team.name if sprint.project.team else None,
            team_members=team_members,
            phase=phase_context,
            gates=gates,
            status=sprint.status,
            start_date=datetime.combine(sprint.start_date, datetime.min.time()) if sprint.start_date else None,
            end_date=datetime.combine(sprint.end_date, datetime.min.time()) if sprint.end_date else None,
        )

        logger.debug(
            f"Built sprint context for sprint {sprint_id}: "
            f"team_members={len(team_members)}, gates={gates.g_sprint}/{gates.g_sprint_close}"
        )

        return context

    async def is_requester_in_sprint_team(
        self,
        sprint_id: UUID,
        requester_id: UUID,
    ) -> bool:
        """
        Check if requester is a member of the sprint's project team.

        This is the primary authorization check for SASE policies that
        require team membership.

        Args:
            sprint_id: Sprint UUID
            requester_id: User UUID making the request

        Returns:
            True if:
            - Requester is an active team member, OR
            - Project has no team (legacy behavior)
            False if:
            - Sprint not found, OR
            - Requester is not a team member

        Performance:
            - Target: <30ms
            - Reuses get_sprint_context for consistency
        """
        context = await self.get_sprint_context(sprint_id)

        if not context:
            logger.warning(f"Sprint {sprint_id} not found for team membership check")
            return False

        # No team = allow (legacy behavior for projects without teams)
        if not context.team_id:
            logger.debug(f"Sprint {sprint_id} has no team, allowing requester {requester_id}")
            return True

        is_member = any(
            member.user_id == requester_id
            for member in context.team_members
        )

        logger.debug(
            f"Team membership check: sprint={sprint_id}, requester={requester_id}, "
            f"is_member={is_member}"
        )

        return is_member

    async def get_requester_role(
        self,
        sprint_id: UUID,
        requester_id: UUID,
    ) -> Optional[str]:
        """
        Get the role of a requester in the sprint's project team.

        Args:
            sprint_id: Sprint UUID
            requester_id: User UUID

        Returns:
            Role string (owner, admin, member, ai_agent) or None if not a member
        """
        context = await self.get_sprint_context(sprint_id)

        if not context:
            return None

        for member in context.team_members:
            if member.user_id == requester_id:
                return member.role

        return None

    async def can_requester_approve_gate(
        self,
        sprint_id: UUID,
        requester_id: UUID,
    ) -> dict:
        """
        Check if requester can approve Sprint Gates (G-Sprint/G-Sprint-Close).

        SDLC 5.1.3 Sprint Planning Governance:
        - Only SE4H Coach (human owner/admin) can approve sprint gates
        - AI agents cannot approve governance gates

        Args:
            sprint_id: Sprint UUID
            requester_id: User UUID

        Returns:
            dict with:
            - allowed: bool
            - reason: str
            - role: str (if allowed)
        """
        context = await self.get_sprint_context(sprint_id)

        if not context:
            return {
                "allowed": False,
                "reason": "Sprint not found",
            }

        # Find requester in team
        for member in context.team_members:
            if member.user_id == requester_id:
                if member.can_approve_gates:
                    return {
                        "allowed": True,
                        "reason": f"User is SE4H Coach with role '{member.role}'",
                        "role": member.role,
                    }
                else:
                    return {
                        "allowed": False,
                        "reason": f"User with role '{member.role}' cannot approve sprint gates. "
                                  f"Only SE4H Coach (human owner/admin) can approve gates.",
                        "role": member.role,
                    }

        return {
            "allowed": False,
            "reason": "Requester is not a member of the sprint team",
        }

    async def can_requester_deploy(
        self,
        sprint_id: UUID,
        requester_id: UUID,
        environment: str = "staging",
    ) -> dict:
        """
        Check if requester can deploy from this sprint.

        Deployment authorization rules:
        - staging: G-Sprint must be passed, requester must be team member
        - production: G-Sprint AND G-Sprint-Close must be passed

        Args:
            sprint_id: Sprint UUID
            requester_id: User UUID
            environment: Target environment (staging, production)

        Returns:
            dict with:
            - allowed: bool
            - reason: str
            - context: SprintContext (if allowed, for audit)
            - required_gates: list of required gates
            - passed_gates: list of passed gates
            - missing_gates: list of missing gates
        """
        context = await self.get_sprint_context(sprint_id)

        if not context:
            return {
                "allowed": False,
                "reason": "Sprint not found",
                "required_gates": [],
                "passed_gates": [],
                "missing_gates": [],
            }

        # Check team membership
        is_member = await self.is_requester_in_sprint_team(sprint_id, requester_id)
        if not is_member:
            return {
                "allowed": False,
                "reason": "Requester is not a member of the sprint team",
                "required_gates": [],
                "passed_gates": [],
                "missing_gates": [],
            }

        # Define required gates by environment
        if environment == "staging":
            required_gates = ["g_sprint"]
        elif environment == "production":
            required_gates = ["g_sprint", "g_sprint_close"]
        else:
            return {
                "allowed": False,
                "reason": f"Unknown environment: {environment}. Valid options: staging, production",
                "required_gates": [],
                "passed_gates": [],
                "missing_gates": [],
            }

        # Check gate status
        passed_gates = []
        missing_gates = []

        if "g_sprint" in required_gates:
            if context.gates.g_sprint == "passed":
                passed_gates.append("g_sprint")
            else:
                missing_gates.append("g_sprint")

        if "g_sprint_close" in required_gates:
            if context.gates.g_sprint_close == "passed":
                passed_gates.append("g_sprint_close")
            else:
                missing_gates.append("g_sprint_close")

        if missing_gates:
            gate_names = ", ".join(f"'{g}'" for g in missing_gates)
            return {
                "allowed": False,
                "reason": f"Required gate(s) not passed: {gate_names}. "
                          f"Cannot deploy to {environment} until these gates are approved.",
                "required_gates": required_gates,
                "passed_gates": passed_gates,
                "missing_gates": missing_gates,
            }

        return {
            "allowed": True,
            "reason": f"Deployment to {environment} allowed. "
                      f"All required gates passed: {', '.join(passed_gates)}",
            "context": context.model_dump(),
            "required_gates": required_gates,
            "passed_gates": passed_gates,
            "missing_gates": [],
        }

    async def check_deployment(
        self,
        request: DeploymentCheckRequest,
    ) -> DeploymentCheckResponse:
        """
        Check deployment authorization (convenience method).

        Wrapper around can_requester_deploy that uses request/response models.

        Args:
            request: DeploymentCheckRequest with sprint_id, requester_id, environment

        Returns:
            DeploymentCheckResponse with full authorization details
        """
        result = await self.can_requester_deploy(
            sprint_id=request.sprint_id,
            requester_id=request.requester_id,
            environment=request.environment,
        )

        context = None
        if result.get("context"):
            context = SprintContext(**result["context"])

        return DeploymentCheckResponse(
            allowed=result["allowed"],
            reason=result["reason"],
            sprint_context=context,
            required_gates=result.get("required_gates", []),
            passed_gates=result.get("passed_gates", []),
            missing_gates=result.get("missing_gates", []),
        )

    async def get_team_members_for_sprint(
        self,
        sprint_id: UUID,
    ) -> list[TeamMemberContext]:
        """
        Get all team members for a sprint.

        Convenience method for getting just the team members without
        full sprint context.

        Args:
            sprint_id: Sprint UUID

        Returns:
            List of TeamMemberContext, empty if sprint not found or has no team
        """
        context = await self.get_sprint_context(sprint_id)
        if not context:
            return []
        return context.team_members

    async def get_coaches_for_sprint(
        self,
        sprint_id: UUID,
    ) -> list[TeamMemberContext]:
        """
        Get SE4H Coaches (users who can approve gates) for a sprint.

        Returns only team members who can approve sprint gates.

        Args:
            sprint_id: Sprint UUID

        Returns:
            List of TeamMemberContext for coaches, empty if none found
        """
        team_members = await self.get_team_members_for_sprint(sprint_id)
        return [m for m in team_members if m.can_approve_gates]


# ==================== Factory Function ====================

def get_sprint_context_provider(db: AsyncSession) -> SprintContextProvider:
    """
    Factory function for dependency injection.

    Usage in FastAPI routes:
        @router.get("/check-deploy")
        async def check_deploy(
            sprint_id: UUID,
            db: AsyncSession = Depends(get_db),
        ):
            provider = get_sprint_context_provider(db)
            context = await provider.get_sprint_context(sprint_id)
            ...

    Args:
        db: AsyncSession from dependency injection

    Returns:
        SprintContextProvider instance
    """
    return SprintContextProvider(db)
