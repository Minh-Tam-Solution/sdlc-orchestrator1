"""
=========================================================================
Sprint Template Service
SDLC Orchestrator - Sprint 78 Day 4

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 78 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)

Purpose:
- CRUD operations for sprint templates
- Apply template to create new sprints
- Template suggestions based on project context

Design Reference:
docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
=========================================================================
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.sprint_template import SprintTemplate
from app.models.sprint import Sprint
from app.models.backlog_item import BacklogItem
from app.models.team import Team
from app.models.project import Project
from app.schemas.sprint_template import (
    ApplyTemplateResponse,
    TemplateSuggestion,
)


class SprintTemplateService:
    """
    Service for managing sprint templates.

    Features:
    - CRUD operations for templates
    - Apply template to create new sprints
    - Template suggestions based on context
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    # =========================================================================
    # Template CRUD
    # =========================================================================

    async def create_template(
        self,
        name: str,
        description: Optional[str] = None,
        template_type: str = "standard",
        duration_days: int = 10,
        default_capacity_points: int = 40,
        gates_enabled: bool = True,
        goal_template: Optional[str] = None,
        team_id: Optional[UUID] = None,
        is_public: bool = False,
        is_default: bool = False,
        backlog_structure: Optional[List[dict]] = None,
        created_by_id: Optional[UUID] = None,
    ) -> SprintTemplate:
        """
        Create a new sprint template.

        Args:
            name: Template name
            description: Template description
            template_type: Type (standard, feature, bugfix, release, custom)
            duration_days: Default sprint duration
            default_capacity_points: Default story points
            gates_enabled: Enable sprint gates
            goal_template: Template for sprint goal
            team_id: Team-specific (null for org-wide)
            is_public: Available to all teams
            is_default: Default template for new sprints
            backlog_structure: Default backlog items
            created_by_id: User creating the template

        Returns:
            Created SprintTemplate
        """
        # If setting as default, unset other defaults for the team
        if is_default:
            await self._unset_default_templates(team_id)

        template = SprintTemplate(
            name=name,
            description=description,
            template_type=template_type,
            duration_days=duration_days,
            default_capacity_points=default_capacity_points,
            gates_enabled=gates_enabled,
            goal_template=goal_template,
            team_id=team_id,
            is_public=is_public,
            is_default=is_default,
            backlog_structure=backlog_structure,
            created_by_id=created_by_id,
        )

        self.db.add(template)
        await self.db.commit()
        await self.db.refresh(template)

        return template

    async def get_template(self, template_id: UUID) -> Optional[SprintTemplate]:
        """Get template by ID."""
        result = await self.db.execute(
            select(SprintTemplate)
            .options(
                selectinload(SprintTemplate.team),
                selectinload(SprintTemplate.created_by),
            )
            .where(
                SprintTemplate.id == template_id,
                SprintTemplate.is_deleted == False,
            )
        )
        return result.scalar_one_or_none()

    async def update_template(
        self,
        template_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        template_type: Optional[str] = None,
        duration_days: Optional[int] = None,
        default_capacity_points: Optional[int] = None,
        gates_enabled: Optional[bool] = None,
        goal_template: Optional[str] = None,
        is_public: Optional[bool] = None,
        is_default: Optional[bool] = None,
        backlog_structure: Optional[List[dict]] = None,
    ) -> Optional[SprintTemplate]:
        """Update a template."""
        template = await self.get_template(template_id)
        if not template:
            return None

        # If setting as default, unset other defaults
        if is_default is True:
            await self._unset_default_templates(template.team_id)

        # Update fields
        if name is not None:
            template.name = name
        if description is not None:
            template.description = description
        if template_type is not None:
            template.template_type = template_type
        if duration_days is not None:
            template.duration_days = duration_days
        if default_capacity_points is not None:
            template.default_capacity_points = default_capacity_points
        if gates_enabled is not None:
            template.gates_enabled = gates_enabled
        if goal_template is not None:
            template.goal_template = goal_template
        if is_public is not None:
            template.is_public = is_public
        if is_default is not None:
            template.is_default = is_default
        if backlog_structure is not None:
            template.backlog_structure = backlog_structure

        await self.db.commit()
        await self.db.refresh(template)

        return template

    async def delete_template(self, template_id: UUID) -> bool:
        """Soft delete a template."""
        template = await self.get_template(template_id)
        if not template:
            return False

        template.is_deleted = True
        await self.db.commit()
        return True

    # =========================================================================
    # Query Methods
    # =========================================================================

    async def list_templates(
        self,
        team_id: Optional[UUID] = None,
        template_type: Optional[str] = None,
        include_public: bool = True,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[List[SprintTemplate], int]:
        """
        List templates with filtering.

        Args:
            team_id: Filter by team (also includes public templates)
            template_type: Filter by type
            include_public: Include public templates
            page: Page number
            page_size: Items per page

        Returns:
            Tuple of (templates, total_count)
        """
        conditions = [SprintTemplate.is_deleted == False]

        # Build team filter
        if team_id:
            if include_public:
                conditions.append(
                    or_(
                        SprintTemplate.team_id == team_id,
                        SprintTemplate.is_public == True,
                    )
                )
            else:
                conditions.append(SprintTemplate.team_id == team_id)
        else:
            if include_public:
                conditions.append(SprintTemplate.is_public == True)

        if template_type:
            conditions.append(SprintTemplate.template_type == template_type)

        # Get total count
        count_result = await self.db.execute(
            select(SprintTemplate).where(*conditions)
        )
        total = len(count_result.scalars().all())

        # Get paginated results
        offset = (page - 1) * page_size
        result = await self.db.execute(
            select(SprintTemplate)
            .options(
                selectinload(SprintTemplate.team),
            )
            .where(*conditions)
            .order_by(SprintTemplate.is_default.desc(), SprintTemplate.usage_count.desc())
            .offset(offset)
            .limit(page_size)
        )

        return list(result.scalars().all()), total

    async def get_default_template(
        self,
        team_id: Optional[UUID] = None,
    ) -> Optional[SprintTemplate]:
        """Get default template for a team or public default."""
        conditions = [
            SprintTemplate.is_deleted == False,
            SprintTemplate.is_default == True,
        ]

        if team_id:
            conditions.append(
                or_(
                    SprintTemplate.team_id == team_id,
                    and_(
                        SprintTemplate.team_id.is_(None),
                        SprintTemplate.is_public == True,
                    )
                )
            )
        else:
            conditions.append(SprintTemplate.is_public == True)

        result = await self.db.execute(
            select(SprintTemplate)
            .where(*conditions)
            .order_by(
                SprintTemplate.team_id.isnot(None).desc(),  # Prefer team-specific
                SprintTemplate.is_default.desc(),
            )
            .limit(1)
        )
        return result.scalar_one_or_none()

    # =========================================================================
    # Apply Template
    # =========================================================================

    async def apply_template(
        self,
        template_id: UUID,
        project_id: UUID,
        start_date: date,
        phase_id: Optional[UUID] = None,
        sprint_name: Optional[str] = None,
        goal: Optional[str] = None,
        team_size: Optional[int] = None,
        include_backlog: bool = True,
        created_by_id: Optional[UUID] = None,
    ) -> ApplyTemplateResponse:
        """
        Create a new sprint from a template.

        Args:
            template_id: Template to apply
            project_id: Project to create sprint in
            start_date: Sprint start date
            phase_id: Phase to assign sprint to
            sprint_name: Override sprint name
            goal: Override sprint goal
            team_size: Override team size
            include_backlog: Create backlog items from template
            created_by_id: User creating the sprint

        Returns:
            ApplyTemplateResponse with created sprint details

        Raises:
            ValueError: If template or project not found
        """
        # Get template
        template = await self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")

        # Get project to determine next sprint number
        project_result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = project_result.scalar_one_or_none()
        if not project:
            raise ValueError(f"Project {project_id} not found")

        # Get next sprint number
        sprint_number = await self._get_next_sprint_number(project_id)

        # Calculate end date
        end_date = start_date + timedelta(days=template.duration_days)

        # Prepare sprint name and goal
        final_name = sprint_name or f"Sprint {sprint_number}"
        final_goal = goal or template.goal_template or f"Sprint {sprint_number} goals"

        # Create sprint
        sprint = Sprint(
            project_id=project_id,
            phase_id=phase_id,
            number=sprint_number,
            name=final_name,
            goal=final_goal,
            start_date=start_date,
            end_date=end_date,
            capacity_points=template.default_capacity_points,
            team_size=team_size,
            status="planning",
            created_by_id=created_by_id,
        )

        self.db.add(sprint)
        await self.db.flush()  # Get sprint ID

        # Create backlog items from template
        backlog_items_created = 0
        if include_backlog and template.backlog_structure:
            for item_template in template.backlog_structure:
                backlog_item = BacklogItem(
                    sprint_id=sprint.id,
                    project_id=project_id,
                    title=item_template.get("title", "Untitled"),
                    description=item_template.get("description"),
                    type=item_template.get("type", "task"),
                    priority=item_template.get("priority", "P2"),
                    story_points=item_template.get("story_points", 0),
                    status="todo",
                    created_by_id=created_by_id,
                )
                self.db.add(backlog_item)
                backlog_items_created += 1

        # Increment template usage count
        template.increment_usage()

        await self.db.commit()
        await self.db.refresh(sprint)

        return ApplyTemplateResponse(
            sprint_id=sprint.id,
            sprint_number=sprint.number,
            sprint_name=sprint.name,
            start_date=sprint.start_date,
            end_date=sprint.end_date,
            backlog_items_created=backlog_items_created,
            template_id=template.id,
            template_name=template.name,
        )

    # =========================================================================
    # Template Suggestions
    # =========================================================================

    async def suggest_templates(
        self,
        project_id: UUID,
        team_id: Optional[UUID] = None,
    ) -> List[TemplateSuggestion]:
        """
        Suggest templates based on project context.

        Args:
            project_id: Project to suggest templates for
            team_id: Team ID for filtering

        Returns:
            List of suggested templates with scores
        """
        # Get project info
        project_result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = project_result.scalar_one_or_none()
        if not project:
            return []

        # Get recent sprints to analyze patterns
        recent_sprints = await self.db.execute(
            select(Sprint)
            .where(Sprint.project_id == project_id)
            .order_by(Sprint.number.desc())
            .limit(5)
        )
        sprints = list(recent_sprints.scalars().all())

        # Get available templates
        templates, _ = await self.list_templates(
            team_id=team_id,
            include_public=True,
            page_size=100,
        )

        suggestions = []
        for template in templates:
            score, reason = self._calculate_template_score(template, sprints, project)

            suggestions.append(TemplateSuggestion(
                template_id=template.id,
                template_name=template.name,
                template_type=template.template_type,
                match_score=score,
                reason=reason,
            ))

        # Sort by score
        suggestions.sort(key=lambda s: s.match_score, reverse=True)

        return suggestions[:5]  # Return top 5

    # =========================================================================
    # Helper Methods
    # =========================================================================

    async def _get_next_sprint_number(self, project_id: UUID) -> int:
        """Get next sprint number for a project."""
        result = await self.db.execute(
            select(Sprint.number)
            .where(Sprint.project_id == project_id)
            .order_by(Sprint.number.desc())
            .limit(1)
        )
        last_number = result.scalar_one_or_none()
        return (last_number or 0) + 1

    async def _unset_default_templates(self, team_id: Optional[UUID]) -> None:
        """Unset default flag for all templates in team/org."""
        conditions = [
            SprintTemplate.is_deleted == False,
            SprintTemplate.is_default == True,
        ]

        if team_id:
            conditions.append(SprintTemplate.team_id == team_id)
        else:
            conditions.append(SprintTemplate.team_id.is_(None))

        result = await self.db.execute(
            select(SprintTemplate).where(*conditions)
        )
        for template in result.scalars().all():
            template.is_default = False

    def _calculate_template_score(
        self,
        template: SprintTemplate,
        recent_sprints: List[Sprint],
        project: Project,
    ) -> tuple[float, str]:
        """Calculate match score for a template."""
        score = 0.5  # Base score
        reasons = []

        # Factor 1: Template type matches recent patterns
        if recent_sprints:
            # Analyze recent sprints for patterns
            avg_duration = sum(
                (s.end_date - s.start_date).days for s in recent_sprints
            ) / len(recent_sprints)

            if abs(template.duration_days - avg_duration) <= 2:
                score += 0.2
                reasons.append("Duration matches recent sprints")

        # Factor 2: Default template bonus
        if template.is_default:
            score += 0.15
            reasons.append("Default template")

        # Factor 3: Usage popularity
        if template.usage_count > 10:
            score += 0.1
            reasons.append("Popular template")

        # Factor 4: Template type suggestions
        if template.template_type == "standard":
            score += 0.05
            reasons.append("Standard sprint type")

        # Cap at 1.0
        score = min(score, 1.0)

        reason = "; ".join(reasons) if reasons else "General purpose template"
        return score, reason


def get_sprint_template_service(db: AsyncSession) -> SprintTemplateService:
    """Factory function to create SprintTemplateService."""
    return SprintTemplateService(db)
