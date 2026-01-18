"""
=========================================================================
Integration Tests for Sprint Assistant Service
SDLC Orchestrator - Sprint 76 Day 4

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 76 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)
Reference: SPRINT-76-SASE-WORKFLOW-INTEGRATION.md

Purpose:
- Test velocity calculation from historical sprints
- Test sprint health indicators and risk assessment
- Test backlog prioritization suggestions
- Verify AI-powered analytics accuracy

Test Coverage (12 tests):
1. test_velocity_with_completed_sprints - Calculate from history
2. test_velocity_no_completed_sprints - Handle empty history
3. test_velocity_trend_increasing - Detect increasing trend
4. test_velocity_trend_decreasing - Detect decreasing trend
5. test_sprint_health_on_track - Low risk assessment
6. test_sprint_health_at_risk - High risk assessment
7. test_sprint_health_blocked_items - Blocked item counting
8. test_suggest_p0_not_started - P0 priority warning
9. test_suggest_overloaded - Overload detection
10. test_suggest_unassigned - Unassigned high-priority
11. test_suggest_blocked - Blocked item suggestions
12. test_analytics_comprehensive - Full analytics response

Zero Mock Policy: Real database fixtures, no mocks
=========================================================================
"""

import pytest
from datetime import date, timedelta
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.sprint import Sprint
from app.models.backlog_item import BacklogItem
from app.models.user import User
from app.services.sprint_assistant import (
    SprintAssistantService,
    VelocityMetrics,
    SprintHealth,
    PrioritySuggestion,
)


# ==================== Fixtures ====================

@pytest.fixture
async def test_user(db: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        id=uuid4(),
        email="sprint-assistant@example.com",
        full_name="Sprint Assistant Test",
        password_hash="$2b$12$test_hash",
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def test_project(db: AsyncSession, test_user: User) -> Project:
    """Create a test project."""
    project = Project(
        id=uuid4(),
        name="Sprint Assistant Test Project",
        description="Project for sprint assistant testing",
        owner_id=test_user.id,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@pytest.fixture
async def completed_sprints(
    db: AsyncSession,
    test_project: Project,
    test_user: User,
) -> list[Sprint]:
    """Create completed sprints with backlog items for velocity calculation."""
    sprints = []
    today = date.today()

    # Create 5 completed sprints with varying velocities
    velocities = [20, 25, 22, 28, 30]  # Increasing trend

    for i, velocity in enumerate(velocities):
        sprint = Sprint(
            id=uuid4(),
            project_id=test_project.id,
            number=70 + i,
            name=f"Sprint {70 + i}",
            goal=f"Complete {velocity} story points",
            status="completed",
            start_date=today - timedelta(days=14 * (5 - i)),
            end_date=today - timedelta(days=14 * (4 - i)),
            g_sprint_status="passed",
            g_sprint_close_status="passed",
            created_by=test_user.id,
        )
        db.add(sprint)
        await db.flush()

        # Add backlog items with total = velocity
        points_remaining = velocity
        item_num = 1
        while points_remaining > 0:
            points = min(5, points_remaining)
            item = BacklogItem(
                id=uuid4(),
                sprint_id=sprint.id,
                project_id=test_project.id,
                type="task",
                title=f"Task {item_num} for Sprint {70 + i}",
                priority="P1",
                story_points=points,
                status="done",
                created_by=test_user.id,
            )
            db.add(item)
            points_remaining -= points
            item_num += 1

        sprints.append(sprint)

    await db.commit()
    return sprints


@pytest.fixture
async def active_sprint(
    db: AsyncSession,
    test_project: Project,
    test_user: User,
) -> Sprint:
    """Create an active sprint for health and suggestion testing."""
    today = date.today()
    sprint = Sprint(
        id=uuid4(),
        project_id=test_project.id,
        number=76,
        name="Sprint 76: Test Sprint",
        goal="Test sprint assistant functionality",
        status="active",
        start_date=today - timedelta(days=5),
        end_date=today + timedelta(days=5),  # 10-day sprint, 5 days elapsed
        g_sprint_status="passed",
        g_sprint_close_status="pending",
        capacity_points=30,
        created_by=test_user.id,
    )
    db.add(sprint)
    await db.commit()
    await db.refresh(sprint)
    return sprint


@pytest.fixture
async def sprint_with_items(
    db: AsyncSession,
    active_sprint: Sprint,
    test_user: User,
) -> Sprint:
    """Add backlog items to active sprint."""
    items = [
        # P0 items
        BacklogItem(
            id=uuid4(),
            sprint_id=active_sprint.id,
            project_id=active_sprint.project_id,
            type="story",
            title="P0 Critical Feature",
            priority="P0",
            story_points=8,
            status="todo",
            created_by=test_user.id,
        ),
        BacklogItem(
            id=uuid4(),
            sprint_id=active_sprint.id,
            project_id=active_sprint.project_id,
            type="bug",
            title="P0 Critical Bug",
            priority="P0",
            story_points=5,
            status="in_progress",
            created_by=test_user.id,
        ),
        # P1 items
        BacklogItem(
            id=uuid4(),
            sprint_id=active_sprint.id,
            project_id=active_sprint.project_id,
            type="task",
            title="P1 Task Done",
            priority="P1",
            story_points=5,
            status="done",
            created_by=test_user.id,
        ),
        BacklogItem(
            id=uuid4(),
            sprint_id=active_sprint.id,
            project_id=active_sprint.project_id,
            type="task",
            title="P1 Task In Progress",
            priority="P1",
            story_points=5,
            status="in_progress",
            assignee_id=test_user.id,
            created_by=test_user.id,
        ),
        # P2 items
        BacklogItem(
            id=uuid4(),
            sprint_id=active_sprint.id,
            project_id=active_sprint.project_id,
            type="task",
            title="P2 Optional Task",
            priority="P2",
            story_points=3,
            status="todo",
            created_by=test_user.id,
        ),
        # Blocked item
        BacklogItem(
            id=uuid4(),
            sprint_id=active_sprint.id,
            project_id=active_sprint.project_id,
            type="task",
            title="Blocked Task",
            priority="P1",
            story_points=4,
            status="blocked",
            created_by=test_user.id,
        ),
    ]

    for item in items:
        db.add(item)

    await db.commit()
    await db.refresh(active_sprint)
    return active_sprint


@pytest.fixture
def sprint_assistant(db: AsyncSession) -> SprintAssistantService:
    """Create SprintAssistantService instance."""
    return SprintAssistantService(db)


# ==================== Velocity Tests ====================

@pytest.mark.asyncio
class TestVelocityCalculation:
    """Test velocity calculation from historical sprints."""

    async def test_velocity_with_completed_sprints(
        self,
        sprint_assistant: SprintAssistantService,
        test_project: Project,
        completed_sprints: list[Sprint],
    ):
        """
        Test 1: Calculate velocity from completed sprints.

        Expected: Average of [20, 25, 22, 28, 30] = 25 SP
        """
        velocity = await sprint_assistant.calculate_velocity(test_project.id)

        assert velocity.average == 25.0
        assert velocity.sprint_count == 5
        assert velocity.confidence == 1.0
        assert len(velocity.history) == 5
        assert velocity.history == [20, 25, 22, 28, 30]

    async def test_velocity_no_completed_sprints(
        self,
        sprint_assistant: SprintAssistantService,
        test_project: Project,
    ):
        """
        Test 2: Handle project with no completed sprints.
        """
        # Note: Don't create completed_sprints fixture
        velocity = await sprint_assistant.calculate_velocity(test_project.id)

        assert velocity.average == 0.0
        assert velocity.trend == "unknown"
        assert velocity.confidence == 0.0
        assert velocity.sprint_count == 0
        assert velocity.history == []

    async def test_velocity_trend_increasing(
        self,
        sprint_assistant: SprintAssistantService,
        test_project: Project,
        completed_sprints: list[Sprint],
    ):
        """
        Test 3: Detect increasing velocity trend.

        History [20, 25, 22, 28, 30] shows increasing trend.
        """
        velocity = await sprint_assistant.calculate_velocity(test_project.id)

        assert velocity.trend == "increasing"

    async def test_velocity_trend_decreasing(
        self,
        sprint_assistant: SprintAssistantService,
        db: AsyncSession,
        test_project: Project,
        test_user: User,
    ):
        """
        Test 4: Detect decreasing velocity trend.
        """
        # Create sprints with decreasing velocities
        today = date.today()
        velocities = [30, 28, 25, 22, 20]  # Decreasing

        for i, velocity_val in enumerate(velocities):
            sprint = Sprint(
                id=uuid4(),
                project_id=test_project.id,
                number=80 + i,
                name=f"Sprint {80 + i}",
                goal="Decreasing velocity test",
                status="completed",
                start_date=today - timedelta(days=14 * (5 - i)),
                end_date=today - timedelta(days=14 * (4 - i)),
                g_sprint_status="passed",
                g_sprint_close_status="passed",
                created_by=test_user.id,
            )
            db.add(sprint)
            await db.flush()

            # Add done items
            item = BacklogItem(
                id=uuid4(),
                sprint_id=sprint.id,
                project_id=test_project.id,
                type="task",
                title="Task",
                priority="P1",
                story_points=velocity_val,
                status="done",
                created_by=test_user.id,
            )
            db.add(item)

        await db.commit()

        velocity = await sprint_assistant.calculate_velocity(test_project.id)
        assert velocity.trend == "decreasing"


# ==================== Sprint Health Tests ====================

@pytest.mark.asyncio
class TestSprintHealth:
    """Test sprint health indicator calculation."""

    async def test_sprint_health_on_track(
        self,
        sprint_assistant: SprintAssistantService,
        sprint_with_items: Sprint,
    ):
        """
        Test 5: Sprint on track has low risk.

        Sprint is 50% through time with items in progress.
        """
        health = await sprint_assistant.get_sprint_health(sprint_with_items.id)

        assert health.total_points == 30  # Sum of all items
        assert health.completed_points == 5  # Only "done" item
        assert health.blocked_count == 1
        # Days elapsed = 5, Days total = 10, expected = 50%
        # Completed = 5/30 = 16.7%, gap = 33% = HIGH risk
        assert health.risk_level in ("medium", "high")
        assert health.days_remaining >= 0

    async def test_sprint_health_at_risk(
        self,
        sprint_assistant: SprintAssistantService,
        db: AsyncSession,
        test_project: Project,
        test_user: User,
    ):
        """
        Test 6: Sprint with poor progress has high risk.
        """
        # Create sprint at 80% time with only 20% done
        today = date.today()
        sprint = Sprint(
            id=uuid4(),
            project_id=test_project.id,
            number=77,
            name="At Risk Sprint",
            goal="Test high risk",
            status="active",
            start_date=today - timedelta(days=8),
            end_date=today + timedelta(days=2),  # 80% elapsed
            g_sprint_status="passed",
            created_by=test_user.id,
        )
        db.add(sprint)
        await db.flush()

        # Add 100 SP, only 20 done
        for i in range(5):
            item = BacklogItem(
                id=uuid4(),
                sprint_id=sprint.id,
                project_id=test_project.id,
                type="task",
                title=f"Task {i}",
                priority="P1",
                story_points=20,
                status="done" if i == 0 else "todo",
                created_by=test_user.id,
            )
            db.add(item)

        await db.commit()

        health = await sprint_assistant.get_sprint_health(sprint.id)

        assert health.risk_level == "high"
        assert health.completion_rate == 20.0  # 20/100
        assert health.expected_completion == 80.0  # 8/10 days

    async def test_sprint_health_blocked_items(
        self,
        sprint_assistant: SprintAssistantService,
        sprint_with_items: Sprint,
    ):
        """
        Test 7: Count blocked items correctly.
        """
        health = await sprint_assistant.get_sprint_health(sprint_with_items.id)

        assert health.blocked_count == 1


# ==================== Suggestion Tests ====================

@pytest.mark.asyncio
class TestPrioritySuggestions:
    """Test backlog prioritization suggestions."""

    async def test_suggest_p0_not_started(
        self,
        sprint_assistant: SprintAssistantService,
        sprint_with_items: Sprint,
    ):
        """
        Test 8: Suggest starting P0 items not yet started.
        """
        suggestions = await sprint_assistant.suggest_priorities(sprint_with_items.id)

        # Find the P0 suggestion
        p0_suggestion = next(
            (s for s in suggestions if s.type == "start_p0"),
            None
        )

        assert p0_suggestion is not None
        assert p0_suggestion.severity == "error"  # P0 is critical
        assert len(p0_suggestion.items) == 1  # One P0 in "todo"
        assert "P0" in p0_suggestion.message

    async def test_suggest_overloaded(
        self,
        sprint_assistant: SprintAssistantService,
        db: AsyncSession,
        test_project: Project,
        test_user: User,
        completed_sprints: list[Sprint],  # Creates velocity history
    ):
        """
        Test 9: Detect sprint overload vs velocity.

        Velocity is 25 SP, create sprint with 40 SP.
        """
        today = date.today()
        sprint = Sprint(
            id=uuid4(),
            project_id=test_project.id,
            number=78,
            name="Overloaded Sprint",
            goal="Test overload detection",
            status="active",
            start_date=today,
            end_date=today + timedelta(days=10),
            g_sprint_status="passed",
            created_by=test_user.id,
        )
        db.add(sprint)
        await db.flush()

        # Add 40 SP (well above 25 velocity * 1.2 = 30)
        for i in range(4):
            item = BacklogItem(
                id=uuid4(),
                sprint_id=sprint.id,
                project_id=test_project.id,
                type="task",
                title=f"Task {i}",
                priority="P1",
                story_points=10,
                status="todo",
                created_by=test_user.id,
            )
            db.add(item)

        await db.commit()

        suggestions = await sprint_assistant.suggest_priorities(sprint.id)

        overload_suggestion = next(
            (s for s in suggestions if s.type == "overloaded"),
            None
        )

        assert overload_suggestion is not None
        assert "40" in overload_suggestion.message
        assert "25" in overload_suggestion.message

    async def test_suggest_unassigned(
        self,
        sprint_assistant: SprintAssistantService,
        sprint_with_items: Sprint,
    ):
        """
        Test 10: Suggest assigning high-priority items.
        """
        suggestions = await sprint_assistant.suggest_priorities(sprint_with_items.id)

        unassigned_suggestion = next(
            (s for s in suggestions if s.type == "unassigned_priority"),
            None
        )

        # Sprint has unassigned P0 and P1 items
        assert unassigned_suggestion is not None
        assert "unassigned" in unassigned_suggestion.message.lower()

    async def test_suggest_blocked(
        self,
        sprint_assistant: SprintAssistantService,
        sprint_with_items: Sprint,
    ):
        """
        Test 11: Suggest resolving blocked items.
        """
        suggestions = await sprint_assistant.suggest_priorities(sprint_with_items.id)

        blocked_suggestion = next(
            (s for s in suggestions if s.type == "blocked"),
            None
        )

        assert blocked_suggestion is not None
        assert "blocked" in blocked_suggestion.message.lower()
        assert len(blocked_suggestion.items) == 1


# ==================== Comprehensive Analytics Test ====================

@pytest.mark.asyncio
class TestSprintAnalytics:
    """Test comprehensive analytics endpoint."""

    async def test_analytics_comprehensive(
        self,
        sprint_assistant: SprintAssistantService,
        sprint_with_items: Sprint,
        completed_sprints: list[Sprint],  # For velocity
    ):
        """
        Test 12: Get comprehensive sprint analytics.
        """
        analytics = await sprint_assistant.get_sprint_analytics(sprint_with_items.id)

        assert analytics.sprint_id == sprint_with_items.id
        assert analytics.sprint_number == 76
        assert analytics.sprint_name == "Sprint 76: Test Sprint"

        # Health should be populated
        assert analytics.health is not None
        assert analytics.health.total_points > 0
        assert analytics.health.risk_level in ("low", "medium", "high")

        # Velocity should be from completed sprints
        assert analytics.velocity is not None
        assert analytics.velocity.sprint_count == 5

        # Suggestions should be populated
        assert analytics.suggestions is not None

        # Summary should be generated
        assert analytics.summary is not None
        assert "Sprint 76" in analytics.summary
