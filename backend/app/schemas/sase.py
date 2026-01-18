"""
=========================================================================
SASE Integration Schemas - Sprint Context for SASE Workflows
SDLC Orchestrator - Sprint 76 (GAP 3 Resolution)

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 76 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P5 (SASE Integration)
Reference: SPRINT-76-SASE-WORKFLOW-INTEGRATION.md

Purpose:
- Define schemas for SASE policy evaluation with sprint context
- Provide team member context for authorization decisions
- Enable sprint-aware SASE approval workflows

GAP 3 Resolution:
- SASE workflows now receive full sprint team context
- Policies can verify requester is sprint team member
- Gate status available for deployment authorization

Security Standards:
- All IDs are UUIDs (not sequential integers)
- Timestamps in UTC
- Role-based authorization context

Zero Mock Policy: Production-ready Pydantic schemas
=========================================================================
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TeamMemberContext(BaseModel):
    """
    Team member context for SASE policies.

    Provides role and permission information for a single team member,
    enabling SASE policies to make authorization decisions.

    Attributes:
        user_id: UUID of the team member
        role: Team role (owner, admin, member, ai_agent)
        can_approve_gates: Whether member can approve Sprint gates (SE4H Coach)
        can_manage_backlog: Whether member can manage backlog items

    SDLC 5.1.3 Alignment:
        - SE4H Coach: Human owner/admin who can approve gates
        - SE4A: AI agent who can be assigned tasks but not approve gates
    """
    user_id: UUID
    role: str = Field(description="Team role: owner, admin, member, ai_agent")
    can_approve_gates: bool = Field(
        default=False,
        description="Whether member can approve Sprint gates (SE4H Coach only)"
    )
    can_manage_backlog: bool = Field(
        default=True,
        description="Whether member can manage backlog items"
    )


class PhaseContext(BaseModel):
    """
    Phase context for sprint.

    Provides phase information for traceability and policy decisions.

    Attributes:
        id: Phase UUID
        name: Phase name (e.g., "Phase 1: Foundation")
        number: Sequential phase number within roadmap
        roadmap_id: Parent roadmap UUID
    """
    id: UUID
    name: str
    number: int
    roadmap_id: UUID


class GateStatusContext(BaseModel):
    """
    Gate status context for sprint.

    Tracks the status of Sprint Governance Gates for SASE policy decisions.

    Attributes:
        g_sprint: G-Sprint gate status (pending, passed, failed)
        g_sprint_close: G-Sprint-Close gate status (pending, passed, failed)

    SDLC 5.1.3 Alignment:
        - G-Sprint: Must pass before sprint can start (Rule #3)
        - G-Sprint-Close: Must pass for proper closure (Rule #2 - 24h docs)
    """
    g_sprint: str = Field(
        default="pending",
        description="G-Sprint gate status: pending, passed, failed"
    )
    g_sprint_close: str = Field(
        default="pending",
        description="G-Sprint-Close gate status: pending, passed, failed"
    )


class SprintContext(BaseModel):
    """
    Comprehensive sprint context for SASE policy evaluation.

    GAP 3 Resolution: Provides complete sprint context including
    team members, gate status, and phase information for SASE policies.

    This context enables SASE policies to:
    - Verify requester is a sprint team member
    - Check gate status before authorizing deployments
    - Access phase/roadmap information for traceability

    Attributes:
        sprint_id: Sprint UUID
        sprint_number: Immutable sprint number (SDLC 5.1.3 Rule #1)
        sprint_name: Sprint name (e.g., "Sprint 76: SASE Integration")
        project_id: Project UUID
        project_name: Project name for display
        team_id: Project team UUID (None for legacy projects)
        team_name: Team name for display
        team_members: List of team member contexts for authorization
        phase: Optional phase context for traceability
        gates: Gate status context for deployment authorization
        status: Sprint status (planning, active, completed, cancelled)
        start_date: Sprint start date
        end_date: Sprint end date

    Usage Example:
        # In SASE policy evaluation
        context = await provider.get_sprint_context(sprint_id)
        opa_input = {
            "sprint_context": context.model_dump(),
            "requester_id": str(requester_id),
            "action": "deploy_staging",
        }
        result = await opa_service.evaluate(opa_input)
    """
    sprint_id: UUID
    sprint_number: int = Field(description="Immutable sprint number (Rule #1)")
    sprint_name: str
    project_id: UUID
    project_name: str
    team_id: Optional[UUID] = Field(
        default=None,
        description="Project team UUID (None for legacy projects without teams)"
    )
    team_name: Optional[str] = None
    team_members: List[TeamMemberContext] = Field(
        default_factory=list,
        description="List of team members for authorization decisions"
    )
    phase: Optional[PhaseContext] = Field(
        default=None,
        description="Parent phase context (None for standalone sprints)"
    )
    gates: GateStatusContext = Field(
        default_factory=GateStatusContext,
        description="Sprint governance gate status"
    )
    status: str = Field(
        description="Sprint status: planning, active, completed, cancelled"
    )
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SASEApprovalRequest(BaseModel):
    """
    SASE approval request with sprint context.

    Updated for Sprint 76 GAP 3:
    - Added sprint_id for sprint-aware policy evaluation
    - sprint_context computed from sprint by SprintContextProvider

    Attributes:
        resource_type: Type of resource (deployment, code_review, release)
        resource_id: UUID of the resource being acted upon
        action: Action being requested (deploy_staging, deploy_prod, approve_pr)
        requester_id: UUID of the user making the request
        sprint_id: Optional sprint UUID for sprint-aware policies
        sprint_context: Computed sprint context (populated by service)

    Usage Example:
        request = SASEApprovalRequest(
            resource_type="deployment",
            resource_id=deployment_id,
            action="deploy_staging",
            requester_id=current_user.id,
            sprint_id=sprint_id,
        )
        # SprintContextProvider populates sprint_context
        result = await sase_service.evaluate(request)
    """
    resource_type: str = Field(
        description="Resource type: deployment, code_review, release, gate_approval"
    )
    resource_id: UUID = Field(description="UUID of the resource")
    action: str = Field(
        description="Action: deploy_staging, deploy_prod, approve_pr, approve_gate"
    )
    requester_id: UUID = Field(description="UUID of the requesting user")
    sprint_id: Optional[UUID] = Field(
        default=None,
        description="Sprint UUID for sprint-aware policy evaluation (GAP 3)"
    )

    # Computed from sprint context (populated by SprintContextProvider)
    sprint_context: Optional[SprintContext] = Field(
        default=None,
        description="Sprint context populated by SprintContextProvider"
    )


class SASEApprovalResponse(BaseModel):
    """
    SASE approval response.

    Attributes:
        allowed: Whether the action is allowed
        reason: Human-readable reason for the decision
        policy_name: Name of the policy that made the decision
        evaluated_at: Timestamp of evaluation (UTC)
        sprint_context_used: Whether sprint context was used in evaluation
        required_gate: Gate that must pass (if action requires gate)
        missing_permissions: List of missing permissions (if denied)
    """
    allowed: bool
    reason: str
    policy_name: str = Field(default="unknown")
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)
    sprint_context_used: bool = Field(
        default=False,
        description="Whether sprint context was used in policy evaluation"
    )
    required_gate: Optional[str] = Field(
        default=None,
        description="Gate required for action (e.g., g_sprint, g_sprint_close)"
    )
    missing_permissions: List[str] = Field(
        default_factory=list,
        description="List of missing permissions if denied"
    )


class DeploymentCheckRequest(BaseModel):
    """
    Request to check if deployment is allowed from a sprint.

    Simplified request for deployment authorization checks.

    Attributes:
        sprint_id: Sprint from which deployment is being made
        requester_id: User requesting deployment
        environment: Target environment (staging, production)
    """
    sprint_id: UUID
    requester_id: UUID
    environment: str = Field(
        default="staging",
        description="Target environment: staging, production"
    )


class DeploymentCheckResponse(BaseModel):
    """
    Response for deployment authorization check.

    Attributes:
        allowed: Whether deployment is allowed
        reason: Human-readable reason
        sprint_context: Sprint context (if allowed, for audit)
        required_gates: List of gates that must pass
        passed_gates: List of gates that have passed
        missing_gates: List of gates that have not passed
    """
    allowed: bool
    reason: str
    sprint_context: Optional[SprintContext] = None
    required_gates: List[str] = Field(default_factory=list)
    passed_gates: List[str] = Field(default_factory=list)
    missing_gates: List[str] = Field(default_factory=list)
