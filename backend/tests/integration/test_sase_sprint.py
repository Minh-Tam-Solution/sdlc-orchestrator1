"""
=========================================================================
Integration Tests for SASE Sprint Context (GAP 3)
SDLC Orchestrator - Sprint 76 Day 2

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 76 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P5 (SASE Integration)
Reference: SPRINT-76-SASE-WORKFLOW-INTEGRATION.md

Purpose:
- Test SprintContextProvider functionality
- Verify GAP 3 resolution (SASE sprint team context)
- Test deployment authorization with gate checks

Test Coverage (10 tests):
1. test_get_sprint_context_success - Get context with all relations
2. test_get_sprint_context_not_found - Return None for missing sprint
3. test_is_requester_in_team_member - Team member recognized
4. test_is_requester_in_team_non_member - Non-member not recognized
5. test_deploy_staging_g_sprint_passed - Can deploy with passed gate
6. test_deploy_staging_g_sprint_pending - Cannot deploy with pending gate
7. test_deploy_staging_non_member - Non-member cannot deploy
8. test_deploy_production_requires_both_gates - Production needs both gates
9. test_can_approve_gate_coach - SE4H Coach can approve
10. test_can_approve_gate_non_coach - Non-coach cannot approve

Zero Mock Policy: Real database fixtures, no mocks
=========================================================================
"""

import pytest
from datetime import date, datetime
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.roadmap import Roadmap
from app.models.phase import Phase
from app.models.sprint import Sprint
from app.models.team import Team
from app.models.team_member import TeamMember
from app.models.user import User
from app.services.sase_sprint_integration import SprintContextProvider


# ==================== Fixtures ====================

@pytest.fixture
async def test_user(db: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        id=uuid4(),
        email="test-sase@example.com",
        full_name="Test SASE User",
        password_hash="$2b$12$test_hash",
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def non_member_user(db: AsyncSession) -> User:
    """Create a user who is not a team member."""
    user = User(
        id=uuid4(),
        email="non-member@example.com",
        full_name="Non Member User",
        password_hash="$2b$12$test_hash",
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def owner_user(db: AsyncSession) -> User:
    """Create an owner user (SE4H Coach)."""
    user = User(
        id=uuid4(),
        email="owner@example.com",
        full_name="Owner User",
        password_hash="$2b$12$test_hash",
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def ai_agent_user(db: AsyncSession) -> User:
    """Create an AI agent user."""
    user = User(
        id=uuid4(),
        email="ai-agent@example.com",
        full_name="AI Agent",
        password_hash="$2b$12$test_hash",
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def test_team(db: AsyncSession) -> Team:
    """Create a test team."""
    team = Team(
        id=uuid4(),
        name="SASE Test Team",
        description="Team for SASE integration testing",
    )
    db.add(team)
    await db.commit()
    await db.refresh(team)
    return team


@pytest.fixture
async def team_member(db: AsyncSession, test_team: Team, test_user: User) -> TeamMember:
    """Add test_user as a team member."""
    member = TeamMember(
        id=uuid4(),
        team_id=test_team.id,
        user_id=test_user.id,
        role="member",
        member_type="human",
    )
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member


@pytest.fixture
async def owner_member(db: AsyncSession, test_team: Team, owner_user: User) -> TeamMember:
    """Add owner_user as team owner (SE4H Coach)."""
    member = TeamMember(
        id=uuid4(),
        team_id=test_team.id,
        user_id=owner_user.id,
        role="owner",
        member_type="human",
    )
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member


@pytest.fixture
async def ai_member(db: AsyncSession, test_team: Team, ai_agent_user: User) -> TeamMember:
    """Add AI agent as team member."""
    member = TeamMember(
        id=uuid4(),
        team_id=test_team.id,
        user_id=ai_agent_user.id,
        role="member",
        member_type="ai_agent",
    )
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member


@pytest.fixture
async def test_project(db: AsyncSession, test_user: User, test_team: Team) -> Project:
    """Create a test project with team."""
    project = Project(
        id=uuid4(),
        name="SASE Test Project",
        description="Project for SASE integration testing",
        owner_id=test_user.id,
        team_id=test_team.id,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@pytest.fixture
async def legacy_project(db: AsyncSession, test_user: User) -> Project:
    """Create a legacy project without team."""
    project = Project(
        id=uuid4(),
        name="Legacy Project",
        description="Project without team assignment",
        owner_id=test_user.id,
        team_id=None,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@pytest.fixture
async def test_roadmap(db: AsyncSession, test_project: Project) -> Roadmap:
    """Create a test roadmap."""
    roadmap = Roadmap(
        id=uuid4(),
        project_id=test_project.id,
        name="2026 Roadmap",
        vision="Build the SDLC Orchestrator platform",
    )
    db.add(roadmap)
    await db.commit()
    await db.refresh(roadmap)
    return roadmap


@pytest.fixture
async def test_phase(db: AsyncSession, test_roadmap: Roadmap) -> Phase:
    """Create a test phase."""
    phase = Phase(
        id=uuid4(),
        roadmap_id=test_roadmap.id,
        number=1,
        name="Phase 1: Foundation",
        theme="Q1 Foundation",
        objective="Establish core platform infrastructure",
        status="active",
    )
    db.add(phase)
    await db.commit()
    await db.refresh(phase)
    return phase


@pytest.fixture
async def pending_sprint(
    db: AsyncSession,
    test_project: Project,
    test_phase: Phase,
    test_user: User,
    team_member: TeamMember,  # Ensure team member is created
    owner_member: TeamMember,  # Ensure owner is created
) -> Sprint:
    """Create a sprint with pending G-Sprint gate."""
    sprint = Sprint(
        id=uuid4(),
        project_id=test_project.id,
        phase_id=test_phase.id,
        number=76,
        name="Sprint 76: SASE Integration",
        goal="Complete Team-Sprint Integration for SASE Workflows",
        status="planning",
        start_date=date(2026, 1, 27),
        end_date=date(2026, 1, 31),
        g_sprint_status="pending",
        g_sprint_close_status="pending",
        created_by=test_user.id,
    )
    db.add(sprint)
    await db.commit()
    await db.refresh(sprint)
    return sprint


@pytest.fixture
async def approved_sprint(
    db: AsyncSession,
    test_project: Project,
    test_phase: Phase,
    test_user: User,
    owner_user: User,
    team_member: TeamMember,
    owner_member: TeamMember,
) -> Sprint:
    """Create a sprint with passed G-Sprint gate."""
    sprint = Sprint(
        id=uuid4(),
        project_id=test_project.id,
        phase_id=test_phase.id,
        number=75,
        name="Sprint 75: Planning API",
        goal="Complete Planning API endpoints",
        status="active",
        start_date=date(2026, 1, 20),
        end_date=date(2026, 1, 24),
        g_sprint_status="passed",
        g_sprint_approved_by=owner_user.id,
        g_sprint_approved_at=datetime.utcnow(),
        g_sprint_close_status="pending",
        created_by=test_user.id,
    )
    db.add(sprint)
    await db.commit()
    await db.refresh(sprint)
    return sprint


@pytest.fixture
async def completed_sprint(
    db: AsyncSession,
    test_project: Project,
    test_phase: Phase,
    test_user: User,
    owner_user: User,
    team_member: TeamMember,
    owner_member: TeamMember,
) -> Sprint:
    """Create a sprint with both gates passed."""
    sprint = Sprint(
        id=uuid4(),
        project_id=test_project.id,
        phase_id=test_phase.id,
        number=74,
        name="Sprint 74: Planning Hierarchy",
        goal="Implement complete Planning Hierarchy",
        status="completed",
        start_date=date(2026, 1, 13),
        end_date=date(2026, 1, 17),
        g_sprint_status="passed",
        g_sprint_approved_by=owner_user.id,
        g_sprint_approved_at=datetime(2026, 1, 13, 9, 0),
        g_sprint_close_status="passed",
        g_sprint_close_approved_by=owner_user.id,
        g_sprint_close_approved_at=datetime(2026, 1, 17, 17, 0),
        created_by=test_user.id,
    )
    db.add(sprint)
    await db.commit()
    await db.refresh(sprint)
    return sprint


@pytest.fixture
async def legacy_sprint(
    db: AsyncSession,
    legacy_project: Project,
    test_user: User,
) -> Sprint:
    """Create a sprint for legacy project (no team)."""
    sprint = Sprint(
        id=uuid4(),
        project_id=legacy_project.id,
        phase_id=None,
        number=1,
        name="Legacy Sprint 1",
        goal="Legacy work",
        status="planning",
        g_sprint_status="pending",
        g_sprint_close_status="pending",
        created_by=test_user.id,
    )
    db.add(sprint)
    await db.commit()
    await db.refresh(sprint)
    return sprint


@pytest.fixture
def sprint_context_provider(db: AsyncSession) -> SprintContextProvider:
    """Create SprintContextProvider instance."""
    return SprintContextProvider(db)


# ==================== Test Cases ====================

@pytest.mark.asyncio
class TestSprintContextProvider:
    """Test SprintContextProvider functionality."""

    async def test_get_sprint_context_success(
        self,
        sprint_context_provider: SprintContextProvider,
        pending_sprint: Sprint,
        test_project: Project,
        test_phase: Phase,
    ):
        """
        Test 1: Get sprint context with all relations loaded.

        GAP 3 Resolution: Verify SprintContext includes all required fields
        for SASE policy evaluation.
        """
        context = await sprint_context_provider.get_sprint_context(pending_sprint.id)

        assert context is not None
        assert context.sprint_id == pending_sprint.id
        assert context.sprint_number == 76
        assert context.sprint_name == "Sprint 76: SASE Integration"
        assert context.project_id == test_project.id
        assert context.project_name == test_project.name
        assert context.team_id is not None
        assert len(context.team_members) >= 2  # member + owner
        assert context.phase is not None
        assert context.phase.id == test_phase.id
        assert context.phase.name == "Phase 1: Foundation"
        assert context.gates.g_sprint == "pending"
        assert context.gates.g_sprint_close == "pending"
        assert context.status == "planning"

    async def test_get_sprint_context_not_found(
        self,
        sprint_context_provider: SprintContextProvider,
    ):
        """
        Test 2: Return None for non-existent sprint.
        """
        context = await sprint_context_provider.get_sprint_context(uuid4())
        assert context is None

    async def test_is_requester_in_team_member(
        self,
        sprint_context_provider: SprintContextProvider,
        pending_sprint: Sprint,
        test_user: User,
    ):
        """
        Test 3: Team member is recognized as sprint team member.

        GAP 3 Resolution: Verify team membership check works correctly.
        """
        is_member = await sprint_context_provider.is_requester_in_sprint_team(
            pending_sprint.id, test_user.id
        )
        assert is_member is True

    async def test_is_requester_in_team_non_member(
        self,
        sprint_context_provider: SprintContextProvider,
        pending_sprint: Sprint,
        non_member_user: User,
    ):
        """
        Test 4: Non-member is not recognized as sprint team member.
        """
        is_member = await sprint_context_provider.is_requester_in_sprint_team(
            pending_sprint.id, non_member_user.id
        )
        assert is_member is False

    async def test_deploy_staging_g_sprint_passed(
        self,
        sprint_context_provider: SprintContextProvider,
        approved_sprint: Sprint,
        test_user: User,
    ):
        """
        Test 5: Can deploy to staging if G-Sprint gate is passed.

        SDLC 5.1.3 Rule #3: Sprint must be approved before execution.
        """
        result = await sprint_context_provider.can_requester_deploy(
            approved_sprint.id, test_user.id, "staging"
        )

        assert result["allowed"] is True
        assert "staging" in result["reason"].lower()
        assert "g_sprint" in result["passed_gates"]
        assert len(result["missing_gates"]) == 0

    async def test_deploy_staging_g_sprint_pending(
        self,
        sprint_context_provider: SprintContextProvider,
        pending_sprint: Sprint,
        test_user: User,
    ):
        """
        Test 6: Cannot deploy to staging if G-Sprint gate is pending.
        """
        result = await sprint_context_provider.can_requester_deploy(
            pending_sprint.id, test_user.id, "staging"
        )

        assert result["allowed"] is False
        assert "g_sprint" in result["reason"].lower()
        assert "g_sprint" in result["missing_gates"]

    async def test_deploy_staging_non_member(
        self,
        sprint_context_provider: SprintContextProvider,
        approved_sprint: Sprint,
        non_member_user: User,
    ):
        """
        Test 7: Non-member cannot deploy even if gate is passed.

        GAP 3 Resolution: SASE requires team membership for deployment.
        """
        result = await sprint_context_provider.can_requester_deploy(
            approved_sprint.id, non_member_user.id, "staging"
        )

        assert result["allowed"] is False
        assert "not a member" in result["reason"].lower()

    async def test_deploy_production_requires_both_gates(
        self,
        sprint_context_provider: SprintContextProvider,
        approved_sprint: Sprint,
        test_user: User,
    ):
        """
        Test 8: Production deployment requires both G-Sprint and G-Sprint-Close.

        SDLC 5.1.3 Rule #2: Post-Sprint Documentation required for production.
        """
        result = await sprint_context_provider.can_requester_deploy(
            approved_sprint.id, test_user.id, "production"
        )

        assert result["allowed"] is False
        assert "g_sprint_close" in result["missing_gates"]
        assert "g_sprint" in result["passed_gates"]
        assert "g_sprint" in result["required_gates"]
        assert "g_sprint_close" in result["required_gates"]

    async def test_deploy_production_both_gates_passed(
        self,
        sprint_context_provider: SprintContextProvider,
        completed_sprint: Sprint,
        test_user: User,
    ):
        """
        Test 8b: Production deployment allowed when both gates passed.
        """
        result = await sprint_context_provider.can_requester_deploy(
            completed_sprint.id, test_user.id, "production"
        )

        assert result["allowed"] is True
        assert "g_sprint" in result["passed_gates"]
        assert "g_sprint_close" in result["passed_gates"]
        assert len(result["missing_gates"]) == 0

    async def test_can_approve_gate_coach(
        self,
        sprint_context_provider: SprintContextProvider,
        pending_sprint: Sprint,
        owner_user: User,
    ):
        """
        Test 9: SE4H Coach (owner) can approve sprint gates.

        SDLC 5.1.3: Only human owners/admins can approve governance gates.
        """
        result = await sprint_context_provider.can_requester_approve_gate(
            pending_sprint.id, owner_user.id
        )

        assert result["allowed"] is True
        assert "SE4H Coach" in result["reason"]
        assert result["role"] == "owner"

    async def test_can_approve_gate_non_coach(
        self,
        sprint_context_provider: SprintContextProvider,
        pending_sprint: Sprint,
        test_user: User,
    ):
        """
        Test 10: Regular member cannot approve sprint gates.
        """
        result = await sprint_context_provider.can_requester_approve_gate(
            pending_sprint.id, test_user.id
        )

        assert result["allowed"] is False
        assert "cannot approve" in result["reason"].lower()
        assert "SE4H Coach" in result["reason"]


@pytest.mark.asyncio
class TestSprintContextProviderEdgeCases:
    """Test edge cases and special scenarios."""

    async def test_legacy_project_allows_any_requester(
        self,
        sprint_context_provider: SprintContextProvider,
        legacy_sprint: Sprint,
        non_member_user: User,
    ):
        """
        Test: Legacy project without team allows any requester.

        Backward compatibility for projects not yet migrated to team model.
        """
        is_member = await sprint_context_provider.is_requester_in_sprint_team(
            legacy_sprint.id, non_member_user.id
        )
        assert is_member is True  # Legacy behavior

    async def test_ai_agent_in_team_cannot_approve_gates(
        self,
        sprint_context_provider: SprintContextProvider,
        pending_sprint: Sprint,
        ai_agent_user: User,
        ai_member: TeamMember,
    ):
        """
        Test: AI agent team member cannot approve gates (SE4A rule).

        SDLC 5.1.3: AI agents can be assigned tasks but cannot approve gates.
        """
        result = await sprint_context_provider.can_requester_approve_gate(
            pending_sprint.id, ai_agent_user.id
        )

        assert result["allowed"] is False
        assert "cannot approve" in result["reason"].lower()

    async def test_get_coaches_for_sprint(
        self,
        sprint_context_provider: SprintContextProvider,
        pending_sprint: Sprint,
        owner_member: TeamMember,
    ):
        """
        Test: Get all SE4H Coaches for a sprint.
        """
        coaches = await sprint_context_provider.get_coaches_for_sprint(pending_sprint.id)

        assert len(coaches) >= 1
        assert all(c.can_approve_gates for c in coaches)
        assert any(c.role == "owner" for c in coaches)

    async def test_get_team_members_for_sprint(
        self,
        sprint_context_provider: SprintContextProvider,
        pending_sprint: Sprint,
    ):
        """
        Test: Get all team members for a sprint.
        """
        members = await sprint_context_provider.get_team_members_for_sprint(pending_sprint.id)

        assert len(members) >= 2  # member + owner
        assert all(hasattr(m, "user_id") for m in members)
        assert all(hasattr(m, "role") for m in members)

    async def test_get_requester_role(
        self,
        sprint_context_provider: SprintContextProvider,
        pending_sprint: Sprint,
        owner_user: User,
        test_user: User,
        non_member_user: User,
    ):
        """
        Test: Get requester's role in sprint team.
        """
        owner_role = await sprint_context_provider.get_requester_role(
            pending_sprint.id, owner_user.id
        )
        assert owner_role == "owner"

        member_role = await sprint_context_provider.get_requester_role(
            pending_sprint.id, test_user.id
        )
        assert member_role == "member"

        non_member_role = await sprint_context_provider.get_requester_role(
            pending_sprint.id, non_member_user.id
        )
        assert non_member_role is None

    async def test_sprint_context_includes_all_required_fields(
        self,
        sprint_context_provider: SprintContextProvider,
        completed_sprint: Sprint,
    ):
        """
        Test: SprintContext includes all fields required by SASE policies.

        Comprehensive check that all GAP 3 requirements are met.
        """
        context = await sprint_context_provider.get_sprint_context(completed_sprint.id)

        # Required fields for SASE policy evaluation
        assert context.sprint_id is not None
        assert context.sprint_number is not None
        assert context.sprint_name is not None
        assert context.project_id is not None
        assert context.project_name is not None
        assert context.status is not None
        assert context.gates is not None
        assert context.gates.g_sprint is not None
        assert context.gates.g_sprint_close is not None

        # Team context (when team exists)
        assert context.team_id is not None
        assert context.team_members is not None
        assert len(context.team_members) > 0

        # Each team member has required fields
        for member in context.team_members:
            assert member.user_id is not None
            assert member.role is not None
            assert member.can_approve_gates is not None
            assert member.can_manage_backlog is not None
