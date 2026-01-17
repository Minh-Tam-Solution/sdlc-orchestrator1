"""
=========================================================================
SAST Scan Model - Static Application Security Testing Results
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: January 16, 2026
Status: ACTIVE - Sprint 69 CTO Go-Live
Authority: Backend Lead + CTO Approved
Foundation: Sprint 43 (SAST Integration), ADR-027 Phase 1
Framework: SDLC 5.1.2 Universal Framework

Purpose:
- Store SAST scan results and security findings
- Track scan history per project
- Support vulnerability trend analysis
- Enable scan-based gate blocking

Security Standards:
- Row-Level Security (RLS) for multi-tenancy
- Soft delete pattern (deleted_at timestamp)
- Immutable audit trail

Zero Mock Policy: Real SQLAlchemy model with all fields
=========================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class SASTScanStatus(str, Enum):
    """SAST scan status types."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SASTScanType(str, Enum):
    """SAST scan types."""
    FULL = "full"
    QUICK = "quick"
    PR = "pr"
    INCREMENTAL = "incremental"


class SASTSeverity(str, Enum):
    """SAST finding severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class SASTScan(Base):
    """
    SAST Scan model for security vulnerability tracking.

    Purpose:
        - Store SAST scan results per project
        - Track security findings and severity counts
        - Support scan history and trend analysis
        - Enable merge blocking for critical/high findings

    Fields:
        - id: UUID primary key (scan_id)
        - project_id: Foreign key to Project
        - triggered_by: Foreign key to User (who triggered the scan)
        - scan_type: Type of scan (full, quick, pr_check, scheduled)
        - status: Scan status (pending, running, completed, failed)
        - branch: Git branch scanned
        - commit_sha: Git commit SHA scanned
        - total_findings: Total number of findings
        - critical_count: Number of critical findings
        - high_count: Number of high findings
        - medium_count: Number of medium findings
        - low_count: Number of low findings
        - info_count: Number of info findings
        - files_scanned: Number of files scanned
        - rules_run: Number of rules executed
        - scan_duration_ms: Scan duration in milliseconds
        - blocks_merge: Whether scan blocks PR merge
        - findings: JSONB array of finding details
        - by_category: JSONB breakdown by category
        - top_affected_files: JSONB top files with findings
        - error_message: Error message if scan failed
        - started_at: Timestamp when scan started
        - completed_at: Timestamp when scan completed
        - created_at: Record creation timestamp

    Relationships:
        - project: Many-to-One with Project model
        - triggered_by_user: Many-to-One with User model

    Indexes:
        - project_id (B-tree) - Fast project lookup
        - completed_at DESC - Fast recent scans lookup
        - status - Status-based filtering

    Usage Example:
        scan = SASTScan(
            project_id=project.id,
            triggered_by=user.id,
            scan_type=SASTScanType.FULL,
            status=SASTScanStatus.COMPLETED,
            total_findings=15,
            critical_count=2,
            high_count=5,
            blocks_merge=True,
            findings=[
                {
                    "rule_id": "python.lang.security.audit.dangerous-exec",
                    "severity": "critical",
                    "file_path": "app/utils.py",
                    "start_line": 42,
                    "message": "Dangerous exec() usage detected"
                }
            ]
        )
        session.add(scan)
        session.commit()
    """

    __tablename__ = "sast_scans"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Project Reference
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Trigger Information
    triggered_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Scan Configuration
    scan_type = Column(
        SQLEnum(SASTScanType),
        nullable=False,
        default=SASTScanType.FULL,
    )
    status = Column(
        SQLEnum(SASTScanStatus),
        nullable=False,
        default=SASTScanStatus.PENDING,
        index=True,
    )

    # Git Information
    branch = Column(String(255), nullable=True)
    commit_sha = Column(String(64), nullable=True)

    # Findings Summary
    total_findings = Column(Integer, nullable=False, default=0)
    critical_count = Column(Integer, nullable=False, default=0)
    high_count = Column(Integer, nullable=False, default=0)
    medium_count = Column(Integer, nullable=False, default=0)
    low_count = Column(Integer, nullable=False, default=0)
    info_count = Column(Integer, nullable=False, default=0)

    # Scan Metrics
    files_scanned = Column(Integer, nullable=False, default=0)
    rules_run = Column(Integer, nullable=False, default=0)
    scan_duration_ms = Column(Integer, nullable=True)

    # Blocking Status
    blocks_merge = Column(Boolean, nullable=False, default=False)

    # Detailed Data (JSONB)
    findings = Column(JSONB, nullable=True, default=list)
    by_category = Column(JSONB, nullable=True, default=dict)
    top_affected_files = Column(JSONB, nullable=True, default=list)

    # Error Handling
    error_message = Column(Text, nullable=True)

    # Timestamps
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="sast_scans")
    triggered_by_user = relationship("User", foreign_keys=[triggered_by])

    def __repr__(self) -> str:
        return (
            f"<SASTScan(id={self.id}, project_id={self.project_id}, "
            f"status={self.status}, findings={self.total_findings})>"
        )

    @property
    def has_blocking_findings(self) -> bool:
        """Check if scan has findings that should block merge."""
        return self.critical_count > 0 or self.high_count > 0

    @property
    def scan_duration_seconds(self) -> Optional[float]:
        """Get scan duration in seconds."""
        if self.scan_duration_ms:
            return self.scan_duration_ms / 1000.0
        return None


class SASTFinding(Base):
    """
    Individual SAST finding model for detailed vulnerability tracking.

    Purpose:
        - Store individual security findings
        - Track finding status (open, fixed, false_positive)
        - Support finding-level comments and remediation

    Fields:
        - id: UUID primary key
        - scan_id: Foreign key to SASTScan
        - project_id: Foreign key to Project (for direct queries)
        - rule_id: Semgrep rule ID
        - rule_name: Human-readable rule name
        - severity: Finding severity (critical, high, medium, low, info)
        - category: OWASP category
        - file_path: Path to affected file
        - start_line: Start line number
        - end_line: End line number
        - message: Finding description
        - snippet: Code snippet
        - fix_suggestion: Suggested fix
        - cwe: CWE identifier(s)
        - owasp: OWASP category
        - status: Finding status (open, fixed, false_positive, ignored)
        - fixed_at: Timestamp when fixed
        - fixed_by: User who fixed the finding
    """

    __tablename__ = "sast_findings"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # References
    scan_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sast_scans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Rule Information
    rule_id = Column(String(255), nullable=False, index=True)
    rule_name = Column(String(500), nullable=True)
    severity = Column(
        SQLEnum(SASTSeverity),
        nullable=False,
        default=SASTSeverity.MEDIUM,
        index=True,
    )
    category = Column(String(100), nullable=True, index=True)

    # Location
    file_path = Column(String(1000), nullable=False, index=True)
    start_line = Column(Integer, nullable=False)
    end_line = Column(Integer, nullable=True)
    start_col = Column(Integer, nullable=True)
    end_col = Column(Integer, nullable=True)

    # Finding Details
    message = Column(Text, nullable=False)
    snippet = Column(Text, nullable=True)
    fix_suggestion = Column(Text, nullable=True)

    # Security Classification
    cwe = Column(JSONB, nullable=True)  # List of CWE IDs
    owasp = Column(JSONB, nullable=True)  # List of OWASP categories
    references = Column(JSONB, nullable=True)  # List of reference URLs
    confidence = Column(String(50), nullable=True)

    # Status Tracking
    status = Column(String(50), nullable=False, default="open", index=True)
    fixed_at = Column(DateTime, nullable=True)
    fixed_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    scan = relationship("SASTScan", backref="finding_details")
    project = relationship("Project")
    fixed_by_user = relationship("User", foreign_keys=[fixed_by])

    def __repr__(self) -> str:
        return (
            f"<SASTFinding(id={self.id}, rule_id={self.rule_id}, "
            f"severity={self.severity}, file={self.file_path}:{self.start_line})>"
        )
