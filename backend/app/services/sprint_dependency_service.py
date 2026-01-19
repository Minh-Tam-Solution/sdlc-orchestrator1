"""
=========================================================================
Sprint Dependency Service
SDLC Orchestrator - Sprint 78 Day 2

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 78 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)

Purpose:
- Manage sprint-to-sprint dependencies
- Detect circular dependencies (BFS algorithm)
- Generate dependency graph for visualization
- Analyze critical path and risks

Design Reference:
docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
=========================================================================
"""

from __future__ import annotations

from collections import deque
from datetime import datetime
from typing import List, Optional, Set, Tuple
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.sprint import Sprint
from app.models.sprint_dependency import SprintDependency
from app.models.project import Project
from app.schemas.sprint_dependency import (
    DependencyGraph,
    DependencyGraphNode,
    DependencyGraphEdge,
    DependencyAnalysis,
    CriticalPathItem,
)


class SprintDependencyService:
    """
    Service for managing sprint dependencies.

    Features:
    - CRUD operations for dependencies
    - Circular dependency detection (BFS)
    - Dependency graph generation
    - Critical path analysis
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    # =========================================================================
    # Dependency CRUD
    # =========================================================================

    async def create_dependency(
        self,
        source_sprint_id: UUID,
        target_sprint_id: UUID,
        dependency_type: str,
        description: Optional[str],
        user_id: UUID,
    ) -> SprintDependency:
        """
        Create a new dependency between sprints.

        Validates:
        - Both sprints exist
        - No self-reference
        - No circular dependency
        - No duplicate dependency

        Args:
            source_sprint_id: Sprint that depends on another
            target_sprint_id: Sprint being depended on
            dependency_type: blocks, requires, or related
            description: Optional description
            user_id: User creating the dependency

        Returns:
            Created SprintDependency

        Raises:
            ValueError: If validation fails
        """
        # Validate no self-reference
        if source_sprint_id == target_sprint_id:
            raise ValueError("A sprint cannot depend on itself")

        # Verify both sprints exist
        source_sprint = await self._get_sprint(source_sprint_id)
        target_sprint = await self._get_sprint(target_sprint_id)

        if not source_sprint:
            raise ValueError(f"Source sprint {source_sprint_id} not found")
        if not target_sprint:
            raise ValueError(f"Target sprint {target_sprint_id} not found")

        # Check for existing dependency
        existing = await self._get_existing_dependency(source_sprint_id, target_sprint_id)
        if existing:
            raise ValueError("Dependency already exists between these sprints")

        # Check for circular dependency
        if await self.has_circular_dependency(source_sprint_id, target_sprint_id):
            raise ValueError(
                "Creating this dependency would form a circular dependency chain"
            )

        # Determine initial status
        status = "active" if dependency_type == "blocks" else "pending"

        # Create dependency
        dependency = SprintDependency(
            source_sprint_id=source_sprint_id,
            target_sprint_id=target_sprint_id,
            dependency_type=dependency_type,
            description=description,
            status=status,
            created_by_id=user_id,
        )

        self.db.add(dependency)
        await self.db.commit()
        await self.db.refresh(dependency)

        return dependency

    async def get_dependency(self, dependency_id: UUID) -> Optional[SprintDependency]:
        """Get a dependency by ID."""
        result = await self.db.execute(
            select(SprintDependency)
            .options(
                selectinload(SprintDependency.source_sprint),
                selectinload(SprintDependency.target_sprint),
            )
            .where(
                SprintDependency.id == dependency_id,
                SprintDependency.is_deleted == False,
            )
        )
        return result.scalar_one_or_none()

    async def update_dependency(
        self,
        dependency_id: UUID,
        dependency_type: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Optional[SprintDependency]:
        """Update a dependency."""
        dependency = await self.get_dependency(dependency_id)
        if not dependency:
            return None

        if dependency_type is not None:
            dependency.dependency_type = dependency_type
        if description is not None:
            dependency.description = description
        if status is not None:
            dependency.status = status
            if status in ("resolved", "cancelled"):
                dependency.resolved_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(dependency)
        return dependency

    async def resolve_dependency(
        self,
        dependency_id: UUID,
        user_id: UUID,
    ) -> Optional[SprintDependency]:
        """Mark a dependency as resolved."""
        dependency = await self.get_dependency(dependency_id)
        if not dependency:
            return None

        dependency.resolve(user_id)
        await self.db.commit()
        await self.db.refresh(dependency)
        return dependency

    async def delete_dependency(self, dependency_id: UUID) -> bool:
        """Soft delete a dependency."""
        dependency = await self.get_dependency(dependency_id)
        if not dependency:
            return False

        dependency.is_deleted = True
        await self.db.commit()
        return True

    # =========================================================================
    # Query Methods
    # =========================================================================

    async def get_sprint_dependencies(
        self,
        sprint_id: UUID,
        direction: str = "both",
        include_resolved: bool = False,
    ) -> List[SprintDependency]:
        """
        Get dependencies for a sprint.

        Args:
            sprint_id: Sprint UUID
            direction: "incoming", "outgoing", or "both"
            include_resolved: Include resolved/cancelled dependencies

        Returns:
            List of dependencies
        """
        conditions = [SprintDependency.is_deleted == False]

        if not include_resolved:
            conditions.append(SprintDependency.status.in_(["pending", "active"]))

        if direction == "incoming":
            conditions.append(SprintDependency.target_sprint_id == sprint_id)
        elif direction == "outgoing":
            conditions.append(SprintDependency.source_sprint_id == sprint_id)
        else:
            # Both directions
            conditions.append(
                (SprintDependency.source_sprint_id == sprint_id)
                | (SprintDependency.target_sprint_id == sprint_id)
            )

        result = await self.db.execute(
            select(SprintDependency)
            .options(
                selectinload(SprintDependency.source_sprint),
                selectinload(SprintDependency.target_sprint),
            )
            .where(*conditions)
        )
        return list(result.scalars().all())

    async def get_project_dependencies(
        self,
        project_id: UUID,
        include_cross_project: bool = True,
    ) -> List[SprintDependency]:
        """
        Get all dependencies for sprints in a project.

        Args:
            project_id: Project UUID
            include_cross_project: Include dependencies to/from other projects

        Returns:
            List of dependencies
        """
        # Get all sprints in project
        sprints_result = await self.db.execute(
            select(Sprint.id).where(Sprint.project_id == project_id)
        )
        sprint_ids = [row[0] for row in sprints_result.all()]

        if not sprint_ids:
            return []

        query = (
            select(SprintDependency)
            .options(
                selectinload(SprintDependency.source_sprint).selectinload(Sprint.project),
                selectinload(SprintDependency.target_sprint).selectinload(Sprint.project),
            )
            .where(
                SprintDependency.is_deleted == False,
                SprintDependency.status.in_(["pending", "active"]),
            )
        )

        if include_cross_project:
            # Include if either source or target is in project
            query = query.where(
                (SprintDependency.source_sprint_id.in_(sprint_ids))
                | (SprintDependency.target_sprint_id.in_(sprint_ids))
            )
        else:
            # Both must be in project
            query = query.where(
                SprintDependency.source_sprint_id.in_(sprint_ids),
                SprintDependency.target_sprint_id.in_(sprint_ids),
            )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    # =========================================================================
    # Circular Dependency Detection
    # =========================================================================

    async def has_circular_dependency(
        self,
        source_id: UUID,
        target_id: UUID,
    ) -> bool:
        """
        Check if adding a dependency would create a cycle.

        Uses BFS to traverse from target back to source.
        If source is reachable from target, adding source->target creates cycle.

        Args:
            source_id: Source sprint ID
            target_id: Target sprint ID

        Returns:
            True if cycle would be created
        """
        visited: Set[UUID] = set()
        queue: deque[UUID] = deque([target_id])

        while queue:
            current = queue.popleft()

            if current == source_id:
                return True

            if current in visited:
                continue

            visited.add(current)

            # Get outgoing dependencies from current
            deps_result = await self.db.execute(
                select(SprintDependency.target_sprint_id).where(
                    SprintDependency.source_sprint_id == current,
                    SprintDependency.is_deleted == False,
                    SprintDependency.status.in_(["pending", "active"]),
                )
            )
            targets = [row[0] for row in deps_result.all()]
            queue.extend(targets)

        return False

    async def find_cycle_path(
        self,
        source_id: UUID,
        target_id: UUID,
    ) -> Optional[List[UUID]]:
        """
        Find the path that would form a cycle if dependency is added.

        Returns:
            List of sprint IDs in the cycle, or None if no cycle
        """
        # Track paths using BFS with parent tracking
        visited: Set[UUID] = set()
        queue: deque[Tuple[UUID, List[UUID]]] = deque([(target_id, [target_id])])

        while queue:
            current, path = queue.popleft()

            if current == source_id:
                return path + [source_id]

            if current in visited:
                continue

            visited.add(current)

            deps_result = await self.db.execute(
                select(SprintDependency.target_sprint_id).where(
                    SprintDependency.source_sprint_id == current,
                    SprintDependency.is_deleted == False,
                    SprintDependency.status.in_(["pending", "active"]),
                )
            )
            targets = [row[0] for row in deps_result.all()]

            for target in targets:
                queue.append((target, path + [target]))

        return None

    # =========================================================================
    # Dependency Graph
    # =========================================================================

    async def get_dependency_graph(
        self,
        project_id: UUID,
        include_cross_project: bool = True,
    ) -> DependencyGraph:
        """
        Generate dependency graph for visualization.

        Args:
            project_id: Project UUID
            include_cross_project: Include dependencies to/from other projects

        Returns:
            DependencyGraph with nodes (sprints) and edges (dependencies)
        """
        dependencies = await self.get_project_dependencies(
            project_id, include_cross_project
        )

        # Collect unique sprints
        sprint_ids: Set[UUID] = set()
        for dep in dependencies:
            sprint_ids.add(dep.source_sprint_id)
            sprint_ids.add(dep.target_sprint_id)

        # Fetch sprint details
        sprints_result = await self.db.execute(
            select(Sprint)
            .options(selectinload(Sprint.project))
            .where(Sprint.id.in_(sprint_ids))
        )
        sprints = {s.id: s for s in sprints_result.scalars().all()}

        # Identify blocked sprints
        blocked_sprint_ids = {
            dep.source_sprint_id
            for dep in dependencies
            if dep.dependency_type == "blocks" and dep.status == "active"
        }

        blocking_sprint_ids = {
            dep.target_sprint_id
            for dep in dependencies
            if dep.dependency_type == "blocks" and dep.status == "active"
        }

        # Build nodes
        nodes = []
        for sprint_id, sprint in sprints.items():
            nodes.append(
                DependencyGraphNode(
                    id=str(sprint_id),
                    label=f"Sprint {sprint.number}",
                    sprint_number=sprint.number,
                    sprint_name=sprint.name or f"Sprint {sprint.number}",
                    status=sprint.status,
                    project_id=str(sprint.project_id),
                    project_name=sprint.project.name if sprint.project else None,
                    has_blocking_dependency=sprint_id in blocking_sprint_ids,
                    is_blocked=sprint_id in blocked_sprint_ids,
                )
            )

        # Build edges
        edges = []
        blocking_count = 0
        cross_project_count = 0

        for dep in dependencies:
            source = sprints.get(dep.source_sprint_id)
            target = sprints.get(dep.target_sprint_id)
            is_cross = (
                source and target and source.project_id != target.project_id
            )
            is_blocking = dep.dependency_type == "blocks" and dep.status == "active"

            if is_blocking:
                blocking_count += 1
            if is_cross:
                cross_project_count += 1

            edges.append(
                DependencyGraphEdge(
                    id=str(dep.id),
                    source=str(dep.source_sprint_id),
                    target=str(dep.target_sprint_id),
                    dependency_type=dep.dependency_type,
                    status=dep.status,
                    description=dep.description,
                    is_blocking=is_blocking,
                    is_cross_project=is_cross,
                )
            )

        return DependencyGraph(
            nodes=nodes,
            edges=edges,
            total_sprints=len(nodes),
            total_dependencies=len(edges),
            blocking_dependencies=blocking_count,
            cross_project_dependencies=cross_project_count,
        )

    # =========================================================================
    # Dependency Analysis
    # =========================================================================

    async def analyze_dependencies(
        self,
        project_id: UUID,
    ) -> DependencyAnalysis:
        """
        Analyze dependency structure for a project.

        Returns:
            Analysis with stats, critical path, and risk indicators
        """
        dependencies = await self.get_project_dependencies(project_id, True)

        # Count by status and type
        blocking_count = sum(
            1 for d in dependencies if d.dependency_type == "blocks"
        )
        pending_count = sum(1 for d in dependencies if d.status == "pending")
        resolved_count = sum(1 for d in dependencies if d.status == "resolved")

        # Identify cross-project dependencies
        cross_project = []
        for dep in dependencies:
            if dep.source_sprint and dep.target_sprint:
                if dep.source_sprint.project_id != dep.target_sprint.project_id:
                    cross_project.append(dep)

        # Calculate dependency depth and critical path
        critical_path, max_depth = await self._calculate_critical_path(project_id)

        # Identify high-dependency sprints (>3 dependencies)
        sprint_dep_counts: dict[UUID, int] = {}
        for dep in dependencies:
            sprint_dep_counts[dep.source_sprint_id] = (
                sprint_dep_counts.get(dep.source_sprint_id, 0) + 1
            )
            sprint_dep_counts[dep.target_sprint_id] = (
                sprint_dep_counts.get(dep.target_sprint_id, 0) + 1
            )

        high_dep_sprints = [
            str(sid) for sid, count in sprint_dep_counts.items() if count > 3
        ]

        return DependencyAnalysis(
            total_dependencies=len(dependencies),
            blocking_dependencies=blocking_count,
            cross_project_dependencies=len(cross_project),
            pending_dependencies=pending_count,
            resolved_dependencies=resolved_count,
            critical_path=critical_path,
            max_depth=max_depth,
            has_circular_risk=False,  # We prevent circular deps at creation
            high_dependency_sprints=high_dep_sprints,
        )

    async def _calculate_critical_path(
        self,
        project_id: UUID,
    ) -> Tuple[List[CriticalPathItem], int]:
        """Calculate critical path through dependency chain."""
        dependencies = await self.get_project_dependencies(project_id, False)

        if not dependencies:
            return [], 0

        # Build adjacency list
        graph: dict[UUID, List[UUID]] = {}
        for dep in dependencies:
            if dep.source_sprint_id not in graph:
                graph[dep.source_sprint_id] = []
            graph[dep.source_sprint_id].append(dep.target_sprint_id)

        # Find sprints with no incoming deps (entry points)
        all_targets = {dep.target_sprint_id for dep in dependencies}
        all_sources = {dep.source_sprint_id for dep in dependencies}
        entry_points = all_sources - all_targets

        # BFS to find longest path
        max_depth = 0
        deepest_path: List[UUID] = []

        for entry in entry_points:
            queue: deque[Tuple[UUID, int, List[UUID]]] = deque([(entry, 0, [entry])])

            while queue:
                current, depth, path = queue.popleft()

                if depth > max_depth:
                    max_depth = depth
                    deepest_path = path

                for target in graph.get(current, []):
                    queue.append((target, depth + 1, path + [target]))

        # Get sprint details for critical path
        if not deepest_path:
            return [], 0

        sprints_result = await self.db.execute(
            select(Sprint)
            .options(selectinload(Sprint.project))
            .where(Sprint.id.in_(deepest_path))
        )
        sprints = {s.id: s for s in sprints_result.scalars().all()}

        critical_path = []
        for i, sprint_id in enumerate(deepest_path):
            sprint = sprints.get(sprint_id)
            if sprint:
                dep_count = len(graph.get(sprint_id, []))
                blocking = sum(
                    1
                    for d in dependencies
                    if d.source_sprint_id == sprint_id
                    and d.dependency_type == "blocks"
                )
                critical_path.append(
                    CriticalPathItem(
                        sprint_id=sprint_id,
                        sprint_number=sprint.number,
                        sprint_name=sprint.name or f"Sprint {sprint.number}",
                        project_name=sprint.project.name if sprint.project else "",
                        dependencies_count=dep_count,
                        blocking_count=blocking,
                        depth=i,
                    )
                )

        return critical_path, max_depth

    # =========================================================================
    # Helper Methods
    # =========================================================================

    async def _get_sprint(self, sprint_id: UUID) -> Optional[Sprint]:
        """Get sprint by ID."""
        result = await self.db.execute(
            select(Sprint).where(Sprint.id == sprint_id)
        )
        return result.scalar_one_or_none()

    async def _get_existing_dependency(
        self,
        source_id: UUID,
        target_id: UUID,
    ) -> Optional[SprintDependency]:
        """Check if dependency already exists."""
        result = await self.db.execute(
            select(SprintDependency).where(
                SprintDependency.source_sprint_id == source_id,
                SprintDependency.target_sprint_id == target_id,
                SprintDependency.is_deleted == False,
            )
        )
        return result.scalar_one_or_none()


def get_sprint_dependency_service(db: AsyncSession) -> SprintDependencyService:
    """Factory function to create SprintDependencyService."""
    return SprintDependencyService(db)
