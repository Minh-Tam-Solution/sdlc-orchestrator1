"""
ProjectService - Project Lifecycle Management

SDLC 5.2.0 Compliance - Test-Driven Development
Framework: Test Strategy 2026

Purpose:
    Manage project CRUD operations, GitHub sync, team member management,
    and tier support (LITE/PRO/ENTERPRISE).

Principles:
    1. Zero Mock Policy (real database operations)
    2. TDD Iron Law (this implements GREEN phase)
    3. Soft delete pattern (deleted_at timestamp)
    4. GitHub sync integration
    5. Tier-based feature access

Usage:
    service = ProjectService()
    project = service.create_project(db, project_data)
    service.sync_with_github(db, project_id, repo_url)

Reference:
    - Test Strategy: docs/05-test/00-TEST-STRATEGY-2026.md
    - Test Stubs: backend/tests/services/test_project_service.py
    - Factory: backend/tests/factories/project_factory.py
"""

import re
from datetime import datetime, UTC
from typing import Optional, List, Dict, Any
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.models.project import Project, ProjectMember

# Custom Exceptions


class ProjectNotFoundError(Exception):
    """Raised when project does not exist or is soft-deleted."""
    pass


class ProjectValidationError(Exception):
    """Raised when project data fails validation."""
    pass


class InvalidProjectTierError(Exception):
    """Raised when project tier is invalid."""
    pass


class GitHubSyncError(Exception):
    """Raised when GitHub sync fails."""
    pass


class ProjectService:
    """
    Service for managing project lifecycle operations.

    Implements all CRUD operations, GitHub sync, team management,
    and tier-based feature access control.
    """

    VALID_TIERS = ["LITE", "STANDARD", "PROFESSIONAL", "ENTERPRISE"]

    TIER_LIMITS = {
        "LITE": {
            "max_team_members": 3,
            "max_projects": 5,
            "github_sync": False,
            "ai_features": False,
        },
        "STANDARD": {
            "max_team_members": 10,
            "max_projects": 20,
            "github_sync": True,
            "ai_features": False,
        },
        "PROFESSIONAL": {
            "max_team_members": 50,
            "max_projects": 100,
            "github_sync": True,
            "ai_features": True,
        },
        "ENTERPRISE": {
            "max_team_members": None,  # Unlimited
            "max_projects": None,  # Unlimited
            "github_sync": True,
            "ai_features": True,
        },
    }

    def create_project(
        self,
        db: Session,
        project_data: Dict[str, Any]
    ) -> Any:  # Returns Project model instance
        """
        Create a new project with validation.

        Args:
            db: Database session
            project_data: Project data dict
                Required: project_name, organization_id, tier
                Optional: description, github_repo_url, created_by

        Returns:
            Project model instance

        Raises:
            ProjectValidationError: If validation fails
            InvalidProjectTierError: If tier is invalid

        Example:
            >>> project = service.create_project(db, {
            ...     "project_name": "SDLC Orchestrator",
            ...     "organization_id": "org-123",
            ...     "tier": "PROFESSIONAL",
            ...     "created_by": "user-456"
            ... })
        """
        # Validation
        if not project_data.get("project_name"):
            raise ProjectValidationError("project_name is required")

        if not project_data.get("organization_id"):
            raise ProjectValidationError("organization_id is required")

        tier = project_data.get("tier", "STANDARD")
        if tier not in self.VALID_TIERS:
            raise InvalidProjectTierError(
                f"Invalid tier: {tier}. Must be one of {self.VALID_TIERS}"
            )

        # Generate URL-friendly slug from project name
        raw_slug = project_data["project_name"].lower().strip()
        raw_slug = re.sub(r"[^\w\s-]", "", raw_slug)
        raw_slug = re.sub(r"[\s_]+", "-", raw_slug)
        raw_slug = re.sub(r"-+", "-", raw_slug).strip("-")

        # Ensure slug uniqueness by appending short UUID suffix if collision exists
        slug = raw_slug
        existing = db.query(Project).filter(Project.slug == slug).first()
        if existing:
            slug = f"{raw_slug}-{uuid4().hex[:8]}"

        # Build real Project model instance
        project = Project(
            name=project_data["project_name"],
            slug=slug,
            description=project_data.get("description", ""),
            owner_id=project_data.get("created_by"),
            policy_pack_tier=tier,
            is_active=True,
        )

        # Persist to database
        db.add(project)
        db.commit()
        db.refresh(project)

        return project

    def get_project_by_id(
        self,
        db: Session,
        project_id: str
    ) -> Optional[Any]:
        """
        Retrieve project by ID (excluding soft-deleted).

        Args:
            db: Database session
            project_id: Project UUID

        Returns:
            Project model instance or None if not found

        Raises:
            ProjectNotFoundError: If project does not exist or is deleted

        Example:
            >>> project = service.get_project_by_id(db, "project-123")
            >>> if project is None:
            ...     raise ProjectNotFoundError("Project not found")
        """
        project = db.query(Project).filter(
            and_(
                Project.id == project_id,
                Project.deleted_at.is_(None)
            )
        ).first()
        return project

    def list_projects_by_organization(
        self,
        db: Session,
        organization_id: str,
        include_deleted: bool = False
    ) -> List[Any]:
        """
        List all projects for an organization.

        Args:
            db: Database session
            organization_id: Organization UUID
            include_deleted: Include soft-deleted projects

        Returns:
            List of Project model instances

        Example:
            >>> projects = service.list_projects_by_organization(
            ...     db, "org-123", include_deleted=False
            ... )
            >>> len(projects)
            5
        """
        query = db.query(Project).filter(Project.owner_id == organization_id)
        if not include_deleted:
            query = query.filter(Project.deleted_at.is_(None))
        return query.order_by(Project.created_at.desc()).all()

    def update_project(
        self,
        db: Session,
        project_id: str,
        update_data: Dict[str, Any]
    ) -> Any:
        """
        Update project fields.

        Args:
            db: Database session
            project_id: Project UUID
            update_data: Fields to update (project_name, description, tier, etc.)

        Returns:
            Updated Project model instance

        Raises:
            ProjectNotFoundError: If project does not exist
            InvalidProjectTierError: If new tier is invalid

        Example:
            >>> project = service.update_project(db, "project-123", {
            ...     "project_name": "New Name",
            ...     "tier": "ENTERPRISE"
            ... })
        """
        project = self.get_project_by_id(db, project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        # Validate tier if provided
        if "tier" in update_data:
            if update_data["tier"] not in self.VALID_TIERS:
                raise InvalidProjectTierError(
                    f"Invalid tier: {update_data['tier']}"
                )

        # Map service-level field names to model column names
        field_mapping = {
            "project_name": "name",
            "tier": "policy_pack_tier",
        }
        for field, value in update_data.items():
            model_field = field_mapping.get(field, field)
            setattr(project, model_field, value)

        project.updated_at = datetime.now(UTC)
        db.commit()
        db.refresh(project)

        return project

    def delete_project(
        self,
        db: Session,
        project_id: str,
        hard_delete: bool = False
    ) -> bool:
        """
        Delete project (soft or hard).

        Args:
            db: Database session
            project_id: Project UUID
            hard_delete: If True, permanently delete. If False, soft delete.

        Returns:
            True if deleted successfully

        Raises:
            ProjectNotFoundError: If project does not exist

        Example:
            >>> service.delete_project(db, "project-123", hard_delete=False)
            True
        """
        project = self.get_project_by_id(db, project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        if hard_delete:
            db.delete(project)
        else:
            project.deleted_at = datetime.now(UTC)
            project.is_active = False

        db.commit()
        return True

    def sync_with_github(
        self,
        db: Session,
        project_id: str,
        repo_url: str
    ) -> Dict[str, Any]:
        """
        Sync project with GitHub repository.

        Args:
            db: Database session
            project_id: Project UUID
            repo_url: GitHub repository URL

        Returns:
            Sync result dict with status and metadata

        Raises:
            ProjectNotFoundError: If project does not exist
            GitHubSyncError: If GitHub sync fails
            ProjectValidationError: If tier doesn't support GitHub sync

        Example:
            >>> result = service.sync_with_github(
            ...     db, "project-123", "https://github.com/owner/repo"
            ... )
            >>> result["status"]
            "success"
        """
        project = self.get_project_by_id(db, project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        # Check tier limits
        tier_config = self.TIER_LIMITS.get(project.policy_pack_tier, {})
        if not tier_config.get("github_sync", False):
            raise ProjectValidationError(
                f"GitHub sync not available for tier {project.policy_pack_tier}"
            )

        # Validate GitHub URL
        if not repo_url or not repo_url.startswith("https://github.com/"):
            raise GitHubSyncError(f"Invalid GitHub URL: {repo_url}")

        # Update project with GitHub sync metadata
        project.github_repo_full_name = repo_url.replace("https://github.com/", "")
        project.github_sync_status = "synced"
        project.github_synced_at = datetime.now(UTC)
        db.commit()
        db.refresh(project)

        sync_result = {
            "status": "success",
            "repo_url": repo_url,
            "synced_at": project.github_synced_at.isoformat(),
            "commits_synced": 0,
            "issues_synced": 0,
            "prs_synced": 0,
        }

        return sync_result

    def add_team_member(
        self,
        db: Session,
        project_id: str,
        user_id: str,
        role: str = "developer"
    ) -> bool:
        """
        Add team member to project.

        Args:
            db: Database session
            project_id: Project UUID
            user_id: User UUID
            role: Member role (owner, admin, developer, viewer)

        Returns:
            True if added successfully

        Raises:
            ProjectNotFoundError: If project does not exist
            ProjectValidationError: If team limit reached

        Example:
            >>> service.add_team_member(db, "project-123", "user-456", "developer")
            True
        """
        project = self.get_project_by_id(db, project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        # Check tier limits
        tier_config = self.TIER_LIMITS.get(project.policy_pack_tier, {})
        max_members = tier_config.get("max_team_members")

        if max_members is not None:
            current_count = db.query(func.count(ProjectMember.id)).filter(
                ProjectMember.project_id == project_id
            ).scalar() or 0

            if current_count >= max_members:
                raise ProjectValidationError(
                    f"Team member limit ({max_members}) reached for tier {project.policy_pack_tier}"
                )

        # Check for duplicate membership
        existing_member = db.query(ProjectMember).filter(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id
            )
        ).first()
        if existing_member:
            raise ProjectValidationError(
                f"User {user_id} is already a member of project {project_id}"
            )

        # Create and persist the new team member
        member = ProjectMember(
            project_id=project_id,
            user_id=user_id,
            role=role,
            invited_at=datetime.now(UTC),
        )
        db.add(member)
        db.commit()

        return True

    def remove_team_member(
        self,
        db: Session,
        project_id: str,
        user_id: str
    ) -> bool:
        """
        Remove team member from project.

        Args:
            db: Database session
            project_id: Project UUID
            user_id: User UUID

        Returns:
            True if removed successfully

        Raises:
            ProjectNotFoundError: If project or member does not exist

        Example:
            >>> service.remove_team_member(db, "project-123", "user-456")
            True
        """
        project = self.get_project_by_id(db, project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        member = db.query(ProjectMember).filter(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id
            )
        ).first()
        if member is None:
            raise ProjectNotFoundError(
                f"Team member (user {user_id}) not found in project {project_id}"
            )
        db.delete(member)
        db.commit()

        return True

    def list_team_members(
        self,
        db: Session,
        project_id: str
    ) -> List[Dict[str, Any]]:
        """
        List all team members for a project.

        Args:
            db: Database session
            project_id: Project UUID

        Returns:
            List of team member dicts (user_id, role, created_at)

        Raises:
            ProjectNotFoundError: If project does not exist

        Example:
            >>> members = service.list_team_members(db, "project-123")
            >>> len(members)
            5
        """
        project = self.get_project_by_id(db, project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        members = db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id
        ).all()
        return members

    def check_feature_access(
        self,
        db: Session,
        project_id: str,
        feature: str
    ) -> bool:
        """
        Check if project tier allows feature access.

        Args:
            db: Database session
            project_id: Project UUID
            feature: Feature name (github_sync, ai_features, etc.)

        Returns:
            True if feature is accessible, False otherwise

        Raises:
            ProjectNotFoundError: If project does not exist

        Example:
            >>> can_use_ai = service.check_feature_access(
            ...     db, "project-123", "ai_features"
            ... )
            >>> can_use_ai
            True
        """
        project = self.get_project_by_id(db, project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        tier_config = self.TIER_LIMITS.get(project.policy_pack_tier, {})
        return tier_config.get(feature, False)

    def archive_project(
        self,
        db: Session,
        project_id: str
    ) -> bool:
        """
        Archive project (different from delete - still visible but read-only).

        Args:
            db: Database session
            project_id: Project UUID

        Returns:
            True if archived successfully

        Raises:
            ProjectNotFoundError: If project does not exist

        Example:
            >>> service.archive_project(db, "project-123")
            True
        """
        project = self.get_project_by_id(db, project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        project.is_active = False
        project.updated_at = datetime.now(UTC)
        db.commit()

        return True

    def restore_project(
        self,
        db: Session,
        project_id: str
    ) -> bool:
        """
        Restore archived or soft-deleted project.

        Args:
            db: Database session
            project_id: Project UUID

        Returns:
            True if restored successfully

        Raises:
            ProjectNotFoundError: If project does not exist

        Example:
            >>> service.restore_project(db, "project-123")
            True
        """
        # Query including soft-deleted and archived projects
        project = db.query(Project).filter(Project.id == project_id).first()

        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        project.is_active = True
        project.deleted_at = None
        project.updated_at = datetime.now(UTC)
        db.commit()

        return True

    def get_project_stats(
        self,
        db: Session,
        project_id: str
    ) -> Dict[str, Any]:
        """
        Get project statistics (gates, evidence, team size, etc.).

        Args:
            db: Database session
            project_id: Project UUID

        Returns:
            Dict with project statistics

        Raises:
            ProjectNotFoundError: If project does not exist

        Example:
            >>> stats = service.get_project_stats(db, "project-123")
            >>> stats["total_gates"]
            12
            >>> stats["team_size"]
            5
        """
        project = self.get_project_by_id(db, project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        # Compute gate stats via the relationship (avoids separate Gate import)
        active_gates = [g for g in project.gates if g.deleted_at is None]
        total_gates = len(active_gates)
        gates_approved = sum(
            1 for g in active_gates if getattr(g, "status", None) == "APPROVED"
        )
        gates_pending = sum(
            1 for g in active_gates
            if getattr(g, "status", None) in ("DRAFT", "EVALUATED", "SUBMITTED")
        )

        team_size = db.query(func.count(ProjectMember.id)).filter(
            ProjectMember.project_id == project_id
        ).scalar() or 0

        stats = {
            "project_id": project_id,
            "total_gates": total_gates,
            "gates_approved": gates_approved,
            "gates_pending": gates_pending,
            "total_evidence": 0,  # Evidence count via separate Evidence service
            "team_size": team_size,
            "github_synced": project.github_sync_status == "synced",
            "tier": project.policy_pack_tier,
            "created_at": project.created_at.isoformat() if project.created_at else None,
        }

        return stats
