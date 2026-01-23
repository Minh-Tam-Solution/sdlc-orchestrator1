"""
=========================================================================
Framework Version Model - Version History Tracking
SDLC Orchestrator - Sprint 103 (Framework Version Tracking)

Version: 1.0.0
Date: January 23, 2026
Status: ACTIVE - Sprint 103 Implementation
Authority: Backend Lead + CTO Approved
Reference: docs/04-build/02-Sprint-Plans/SPRINT-103-DESIGN.md
Reference: SDLC Framework 5.2.0, Section 09-GOVERN

Purpose:
- Track Framework version history per project
- Enable compliance audits with version proof
- Detect version drift from latest Framework
- Support Framework migration tracking

Why track version history?
- Compliance audits require version proof at specific points in time
- Framework updates need migration tracking
- Policy changes need retroactive application records
- Training materials reference specific versions

Zero Mock Policy: Real SQLAlchemy model with all fields
=========================================================================
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class FrameworkVersion(Base):
    """
    Framework Version model for tracking SDLC Framework versions per project.

    Purpose:
        - Record Framework version when project created/updated
        - Enable compliance audits with version history
        - Detect version drift from latest Framework

    Fields:
        - id: UUID primary key
        - project_id: Foreign key to Project
        - version: Semantic version string (e.g., "5.2.0")
        - major: Major version number (breaking changes)
        - minor: Minor version number (features)
        - patch: Patch version number (fixes)
        - release_notes: Optional notes about this version
        - applied_at: When this version was applied
        - applied_by: User who applied the version

    Relationships:
        - project: Many-to-One with Project model
        - applied_by_user: Many-to-One with User model

    Indexes:
        - project_id (B-tree) - Fast project version lookup
        - applied_at (B-tree) - Chronological ordering

    Usage Example:
        fv = FrameworkVersion(
            project_id=project.id,
            version="5.2.0",
            major=5,
            minor=2,
            patch=0,
            applied_by=user.id
        )
        session.add(fv)
        session.commit()
    """

    __tablename__ = "framework_versions"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Project Relationship
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Version Information
    version = Column(
        String(20),
        nullable=False,
        comment="Semantic version string (e.g., 5.2.0)"
    )
    major = Column(
        Integer,
        nullable=False,
        comment="Major version number"
    )
    minor = Column(
        Integer,
        nullable=False,
        comment="Minor version number"
    )
    patch = Column(
        Integer,
        nullable=False,
        comment="Patch version number"
    )

    # Optional Metadata
    release_notes = Column(
        Text,
        nullable=True,
        comment="Notes about this version application"
    )

    # Audit Information
    applied_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
        comment="When this version was applied to the project"
    )
    applied_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="User who applied this version"
    )

    # Relationships
    project = relationship("Project", back_populates="framework_versions")
    applied_by_user = relationship("User", foreign_keys=[applied_by])

    def __repr__(self) -> str:
        return f"<FrameworkVersion(project_id={self.project_id}, version={self.version}, applied_at={self.applied_at})>"

    @property
    def version_tuple(self) -> tuple[int, int, int]:
        """Get version as tuple for comparison."""
        return (self.major, self.minor, self.patch)

    def is_older_than(self, other_version: str) -> bool:
        """
        Check if this version is older than another version.

        Args:
            other_version: Version string to compare (e.g., "5.2.0")

        Returns:
            True if this version is older
        """
        parts = other_version.split('.')
        if len(parts) != 3:
            return False
        other_tuple = (int(parts[0]), int(parts[1]), int(parts[2]))
        return self.version_tuple < other_tuple

    def is_newer_than(self, other_version: str) -> bool:
        """
        Check if this version is newer than another version.

        Args:
            other_version: Version string to compare (e.g., "5.2.0")

        Returns:
            True if this version is newer
        """
        parts = other_version.split('.')
        if len(parts) != 3:
            return False
        other_tuple = (int(parts[0]), int(parts[1]), int(parts[2]))
        return self.version_tuple > other_tuple
