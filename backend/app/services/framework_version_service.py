"""
=========================================================================
Framework Version Service - SDLC Framework Version Tracking
SDLC Orchestrator - Sprint 103 (Framework Version Tracking)

Version: 1.0.0
Date: January 23, 2026
Status: ACTIVE - Sprint 103 Implementation
Authority: Backend Lead + CTO Approved
Reference: docs/04-build/02-Sprint-Plans/SPRINT-103-DESIGN.md
Reference: SDLC Framework 5.2.0, Section 09-GOVERN

Purpose:
- Record Framework version for projects
- Track version history for audits
- Detect version drift from latest Framework
- Support Framework migration tracking

SDLC 5.2.0 Compliance:
> "All projects MUST track which Framework version they were built against
> for audit and compliance."
> — SDLC Framework 5.2.0, Section 09-GOVERN

Zero Mock Policy: Production-ready implementation
=========================================================================
"""

import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.framework_version import FrameworkVersion

logger = logging.getLogger(__name__)

# Current Framework version (should be updated when Framework is upgraded)
CURRENT_FRAMEWORK_VERSION = "5.2.0"


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class VersionDrift:
    """Version drift analysis result."""
    current: Optional[str]
    latest: str
    drift: bool
    major_drift: bool
    minor_drift: bool
    patch_drift: bool

    @property
    def severity(self) -> str:
        """Get drift severity level."""
        if not self.drift:
            return "none"
        if self.major_drift:
            return "critical"
        if self.minor_drift:
            return "warning"
        return "info"

    @property
    def message(self) -> str:
        """Get human-readable drift message."""
        if not self.drift:
            return f"✅ Up to date with Framework {self.latest}"
        if self.major_drift:
            return f"❌ CRITICAL: Major version drift ({self.current} → {self.latest})"
        if self.minor_drift:
            return f"⚠️ WARNING: Minor version drift ({self.current} → {self.latest})"
        return f"ℹ️ INFO: Patch version drift ({self.current} → {self.latest})"


# ============================================================================
# Framework Version Service
# ============================================================================


class FrameworkVersionService:
    """
    Service for tracking SDLC Framework versions per project.

    This service:
    1. Records Framework version when projects are created/updated
    2. Maintains version history for compliance audits
    3. Detects version drift from latest Framework
    4. Supports Framework migration tracking

    Usage:
        service = FrameworkVersionService(db)

        # Record version on project creation
        fv = await service.record_framework_version(project_id, "5.2.0", user_id)

        # Check version drift
        drift = await service.detect_version_drift(project_id, "5.2.0")
        if drift.drift:
            print(f"Project is behind: {drift.message}")
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize FrameworkVersionService.

        Args:
            db: Database session for queries
        """
        self.db = db

    # =========================================================================
    # Version Recording
    # =========================================================================

    async def record_framework_version(
        self,
        project_id: UUID,
        version: str,
        applied_by: Optional[UUID] = None,
        release_notes: Optional[str] = None,
    ) -> FrameworkVersion:
        """
        Record Framework version for project.

        Used when:
            - Project created
            - Framework manually updated
            - Migration applied

        Args:
            project_id: Project UUID
            version: Semantic version string (e.g., "5.2.0")
            applied_by: User who applied the version
            release_notes: Optional notes about this version

        Returns:
            FrameworkVersion record

        Raises:
            ValueError: If version string is invalid
        """
        # Validate and parse version
        major, minor, patch = self._parse_version(version)

        fv = FrameworkVersion(
            id=uuid4(),
            project_id=project_id,
            version=version,
            major=major,
            minor=minor,
            patch=patch,
            release_notes=release_notes,
            applied_at=datetime.utcnow(),
            applied_by=applied_by,
        )

        self.db.add(fv)
        await self.db.commit()
        await self.db.refresh(fv)

        logger.info(
            f"Recorded Framework version {version} for project {project_id} "
            f"(applied_by={applied_by})"
        )

        return fv

    async def ensure_initial_version(
        self,
        project_id: UUID,
        version: str = CURRENT_FRAMEWORK_VERSION,
        applied_by: Optional[UUID] = None,
    ) -> FrameworkVersion:
        """
        Ensure project has at least one Framework version record.

        If no version exists, creates one with the specified version.
        If version exists, returns the current version.

        Args:
            project_id: Project UUID
            version: Default version to use if none exists
            applied_by: User who created the project

        Returns:
            Current or newly created FrameworkVersion
        """
        current = await self.get_current_framework_version(project_id)
        if current:
            return current

        return await self.record_framework_version(
            project_id=project_id,
            version=version,
            applied_by=applied_by,
            release_notes="Initial Framework version on project creation",
        )

    # =========================================================================
    # Version Queries
    # =========================================================================

    async def get_current_framework_version(
        self,
        project_id: UUID,
    ) -> Optional[FrameworkVersion]:
        """
        Get latest Framework version for project.

        Args:
            project_id: Project UUID

        Returns:
            Latest FrameworkVersion or None
        """
        result = await self.db.execute(
            select(FrameworkVersion)
            .where(FrameworkVersion.project_id == project_id)
            .order_by(desc(FrameworkVersion.applied_at))
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_version_history(
        self,
        project_id: UUID,
        limit: int = 50,
    ) -> list[FrameworkVersion]:
        """
        Get full version history for project.

        Args:
            project_id: Project UUID
            limit: Max records to return

        Returns:
            List of FrameworkVersion records (newest first)
        """
        result = await self.db.execute(
            select(FrameworkVersion)
            .where(FrameworkVersion.project_id == project_id)
            .order_by(desc(FrameworkVersion.applied_at))
            .limit(limit)
        )
        return list(result.scalars().all())

    # =========================================================================
    # Version Drift Detection
    # =========================================================================

    async def detect_version_drift(
        self,
        project_id: UUID,
        latest_framework_version: str = CURRENT_FRAMEWORK_VERSION,
    ) -> VersionDrift:
        """
        Detect if project is behind latest Framework version.

        Args:
            project_id: Project UUID
            latest_framework_version: Latest available Framework version

        Returns:
            VersionDrift with drift analysis
        """
        current = await self.get_current_framework_version(project_id)

        if not current:
            return VersionDrift(
                current=None,
                latest=latest_framework_version,
                drift=True,
                major_drift=True,
                minor_drift=False,
                patch_drift=False,
            )

        # Parse versions
        current_tuple = (current.major, current.minor, current.patch)
        latest_major, latest_minor, latest_patch = self._parse_version(latest_framework_version)
        latest_tuple = (latest_major, latest_minor, latest_patch)

        drift = current_tuple < latest_tuple
        major_drift = current.major < latest_major
        minor_drift = not major_drift and current.minor < latest_minor
        patch_drift = not major_drift and not minor_drift and current.patch < latest_patch

        return VersionDrift(
            current=current.version,
            latest=latest_framework_version,
            drift=drift,
            major_drift=major_drift,
            minor_drift=minor_drift,
            patch_drift=patch_drift,
        )

    async def get_projects_with_drift(
        self,
        latest_framework_version: str = CURRENT_FRAMEWORK_VERSION,
    ) -> list[tuple[UUID, str, VersionDrift]]:
        """
        Get all projects with version drift.

        Args:
            latest_framework_version: Latest available Framework version

        Returns:
            List of (project_id, current_version, drift) tuples
        """
        # Get latest version for each project (using distinct on)
        # This is a simplified implementation - for production, use a subquery
        result = await self.db.execute(
            select(FrameworkVersion.project_id, FrameworkVersion.version)
            .distinct(FrameworkVersion.project_id)
            .order_by(FrameworkVersion.project_id, desc(FrameworkVersion.applied_at))
        )

        projects_with_drift = []
        for project_id, version in result:
            drift = await self.detect_version_drift(project_id, latest_framework_version)
            if drift.drift:
                projects_with_drift.append((project_id, version, drift))

        return projects_with_drift

    # =========================================================================
    # Compliance Reporting
    # =========================================================================

    async def get_compliance_summary(
        self,
        project_id: UUID,
    ) -> dict:
        """
        Get Framework compliance summary for project.

        Args:
            project_id: Project UUID

        Returns:
            Dict with compliance information
        """
        current = await self.get_current_framework_version(project_id)
        history = await self.get_version_history(project_id, limit=10)
        drift = await self.detect_version_drift(project_id)

        return {
            "project_id": str(project_id),
            "current_version": current.version if current else None,
            "current_applied_at": current.applied_at.isoformat() if current else None,
            "latest_framework_version": CURRENT_FRAMEWORK_VERSION,
            "drift": {
                "has_drift": drift.drift,
                "severity": drift.severity,
                "message": drift.message,
                "major_drift": drift.major_drift,
                "minor_drift": drift.minor_drift,
                "patch_drift": drift.patch_drift,
            },
            "version_count": len(history),
            "versions": [
                {
                    "version": v.version,
                    "applied_at": v.applied_at.isoformat(),
                    "release_notes": v.release_notes,
                }
                for v in history[:5]  # Last 5 versions
            ],
        }

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _parse_version(self, version: str) -> tuple[int, int, int]:
        """
        Parse semantic version string.

        Args:
            version: Version string (e.g., "5.2.0")

        Returns:
            Tuple of (major, minor, patch)

        Raises:
            ValueError: If version string is invalid
        """
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version)
        if not match:
            raise ValueError(
                f"Invalid version string: {version}. "
                f"Expected semantic version format (e.g., 5.2.0)"
            )

        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


# ============================================================================
# Factory Function
# ============================================================================


def create_framework_version_service(
    db: AsyncSession,
) -> FrameworkVersionService:
    """
    Factory function to create FrameworkVersionService.

    Args:
        db: Database session

    Returns:
        Configured FrameworkVersionService
    """
    return FrameworkVersionService(db=db)
