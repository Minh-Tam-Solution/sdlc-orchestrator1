"""
=========================================================================
Compliance Scan Model - SDLC 4.9.1 Violation Detection
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: December 2, 2025
Status: ACTIVE - Sprint 21 Day 1 (Compliance Scanner)
Authority: Backend Lead + CTO Approved
Foundation: Sprint 21 Plan (1,168 lines), ADR-007 Approved
Framework: SDLC 4.9.1 Complete Lifecycle

Purpose:
- Store compliance scan results and violations
- Track scan history per project
- Support AI recommendations for violations
- Enable scheduled and on-demand scans

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
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class TriggerType(str, Enum):
    """Compliance scan trigger types."""
    SCHEDULED = "scheduled"
    MANUAL = "manual"
    WEBHOOK = "webhook"
    CI_CD = "ci_cd"


class ViolationSeverity(str, Enum):
    """Violation severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ViolationType(str, Enum):
    """Types of SDLC 4.9.1 compliance violations."""
    MISSING_DOCUMENTATION = "missing_documentation"
    SKIPPED_STAGE = "skipped_stage"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    POLICY_VIOLATION = "policy_violation"
    DOC_CODE_DRIFT = "doc_code_drift"
    API_NOT_DOCUMENTED = "api_not_documented"
    DB_SCHEMA_DRIFT = "db_schema_drift"
    SECURITY_RULE_MISSING = "security_rule_missing"
    TEST_COVERAGE_LOW = "test_coverage_low"
    GATE_SKIPPED = "gate_skipped"


class ComplianceScan(Base):
    """
    Compliance Scan model for SDLC 4.9.1 violation tracking.

    Purpose:
        - Store compliance scan results per project
        - Track violations and warnings
        - Calculate compliance score
        - Support scan history and trends

    Fields:
        - id: UUID primary key
        - project_id: Foreign key to Project
        - triggered_by: Foreign key to User (who triggered the scan)
        - trigger_type: How the scan was triggered (scheduled, manual, webhook, ci_cd)
        - compliance_score: Score from 0-100
        - violations_count: Number of violations detected
        - warnings_count: Number of warnings detected
        - violations: JSONB array of violation details
        - warnings: JSONB array of warning details
        - scanned_at: Timestamp when scan completed
        - duration_ms: Scan duration in milliseconds
        - scan_metadata: Additional scan metadata (JSONB)
        - created_at: Record creation timestamp

    Relationships:
        - project: Many-to-One with Project model
        - triggered_by_user: Many-to-One with User model

    Indexes:
        - project_id (B-tree) - Fast project lookup
        - scanned_at DESC - Fast recent scans lookup
        - compliance_score - Score-based filtering

    Usage Example:
        scan = ComplianceScan(
            project_id=project.id,
            triggered_by=user.id,
            trigger_type=TriggerType.MANUAL,
            compliance_score=85,
            violations_count=3,
            violations=[
                {
                    "type": "MISSING_DOCUMENTATION",
                    "severity": "HIGH",
                    "location": "docs/00-Project-Foundation",
                    "description": "Missing required stage folder",
                    "recommendation": "Create docs/00-Project-Foundation folder"
                }
            ]
        )
        session.add(scan)
        session.commit()
    """

    __tablename__ = "compliance_scans"

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
    trigger_type = Column(
        String(50),
        nullable=False,
        default=TriggerType.MANUAL.value,
    )

    # Compliance Score (0-100)
    compliance_score = Column(
        Integer,
        nullable=False,
        default=0,
        index=True,
    )

    # Violation/Warning Counts
    violations_count = Column(Integer, nullable=False, default=0)
    warnings_count = Column(Integer, nullable=False, default=0)

    # Detailed Results (JSONB)
    violations = Column(
        JSONB,
        nullable=False,
        default=list,
        comment="Array of violation objects with type, severity, location, description",
    )
    warnings = Column(
        JSONB,
        nullable=False,
        default=list,
        comment="Array of warning objects with type, severity, location, description",
    )

    # Scan Metadata
    scan_metadata = Column(
        JSONB,
        nullable=True,
        default=dict,
        comment="Additional metadata: git_commit, branch, files_scanned, etc.",
    )

    # Timing
    scanned_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )
    duration_ms = Column(
        Integer,
        nullable=True,
        comment="Scan duration in milliseconds",
    )

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    project = relationship("Project", backref="compliance_scans")
    triggered_by_user = relationship("User", backref="triggered_scans")

    def __repr__(self) -> str:
        return (
            f"<ComplianceScan(id={self.id}, project_id={self.project_id}, "
            f"score={self.compliance_score}, violations={self.violations_count})>"
        )

    @property
    def is_compliant(self) -> bool:
        """Check if scan passed (no critical/high violations)."""
        if not self.violations:
            return True
        critical_high = [
            v for v in self.violations
            if v.get("severity") in ("critical", "high")
        ]
        return len(critical_high) == 0

    @property
    def critical_violations(self) -> list:
        """Get critical severity violations only."""
        if not self.violations:
            return []
        return [v for v in self.violations if v.get("severity") == "critical"]

    @property
    def high_violations(self) -> list:
        """Get high severity violations only."""
        if not self.violations:
            return []
        return [v for v in self.violations if v.get("severity") == "high"]


class ComplianceViolation(Base):
    """
    Individual Compliance Violation model for detailed tracking.

    Purpose:
        - Store individual violation details
        - Track AI recommendations for each violation
        - Support violation resolution workflow
        - Enable violation trend analysis

    Fields:
        - id: UUID primary key
        - scan_id: Foreign key to ComplianceScan
        - project_id: Foreign key to Project (denormalized for performance)
        - violation_type: Type of violation (enum)
        - severity: Severity level (critical, high, medium, low, info)
        - location: File/folder path or code location
        - description: Human-readable description
        - recommendation: Suggested fix
        - ai_recommendation: AI-generated recommendation (nullable)
        - ai_provider: Which AI provider generated recommendation
        - is_resolved: Whether violation has been fixed
        - resolved_by: User who resolved the violation
        - resolved_at: Resolution timestamp
        - created_at: Record creation timestamp

    Relationships:
        - scan: Many-to-One with ComplianceScan model
        - project: Many-to-One with Project model
        - resolver: Many-to-One with User model

    Usage Example:
        violation = ComplianceViolation(
            scan_id=scan.id,
            project_id=project.id,
            violation_type=ViolationType.MISSING_DOCUMENTATION,
            severity=ViolationSeverity.HIGH,
            location="docs/00-Project-Foundation",
            description="Missing required SDLC 4.9.1 stage folder",
            recommendation="Create docs/00-Project-Foundation folder with required files"
        )
        session.add(violation)
        session.commit()
    """

    __tablename__ = "compliance_violations"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Scan Reference
    scan_id = Column(
        UUID(as_uuid=True),
        ForeignKey("compliance_scans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Project Reference (denormalized for query performance)
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Violation Details
    violation_type = Column(
        String(100),
        nullable=False,
        index=True,
    )
    severity = Column(
        String(20),
        nullable=False,
        default=ViolationSeverity.MEDIUM.value,
        index=True,
    )
    location = Column(
        String(1000),
        nullable=True,
        comment="File path, folder path, or code location",
    )
    description = Column(
        Text,
        nullable=False,
    )
    recommendation = Column(
        Text,
        nullable=True,
        comment="Human-generated recommendation",
    )

    # AI Recommendation
    ai_recommendation = Column(
        Text,
        nullable=True,
        comment="AI-generated recommendation (Ollama/Claude/GPT-4o)",
    )
    ai_provider = Column(
        String(50),
        nullable=True,
        comment="AI provider used: ollama, claude, gpt4o",
    )
    ai_confidence = Column(
        Integer,
        nullable=True,
        comment="AI confidence score (0-100)",
    )

    # Resolution Status
    is_resolved = Column(Boolean, default=False, nullable=False, index=True)
    resolved_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    scan = relationship("ComplianceScan", backref="violation_records")
    project = relationship("Project", backref="violations")
    resolver = relationship("User", backref="resolved_violations")

    def __repr__(self) -> str:
        return (
            f"<ComplianceViolation(id={self.id}, type={self.violation_type}, "
            f"severity={self.severity}, resolved={self.is_resolved})>"
        )

    @property
    def is_blocking(self) -> bool:
        """Check if violation should block gate progression."""
        return self.severity in (
            ViolationSeverity.CRITICAL.value,
            ViolationSeverity.HIGH.value,
        )

    @property
    def has_ai_recommendation(self) -> bool:
        """Check if AI recommendation is available."""
        return self.ai_recommendation is not None and len(self.ai_recommendation) > 0


class ScanJobStatus(str, Enum):
    """Scan job status values."""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ScanJob(Base):
    """
    Scan Job model for persistent background job tracking.

    Purpose:
        - Persist scan job queue to database (survives restarts)
        - Track job status and progress
        - Store job results and errors
        - Enable job retry on failure

    Fields:
        - id: UUID primary key (also serves as job_id)
        - project_id: Project to scan
        - triggered_by: User who triggered the job
        - trigger_type: How job was triggered
        - status: Job status (queued, running, completed, failed)
        - priority: Job priority (high, normal, low)
        - include_doc_code_sync: Whether to check doc-code drift
        - queued_at: When job was queued
        - started_at: When job started processing
        - completed_at: When job finished
        - result: Job result data (JSONB)
        - error: Error message if failed
        - retry_count: Number of retry attempts
        - created_at: Record creation timestamp

    Relationships:
        - project: Many-to-One with Project model
        - triggered_by_user: Many-to-One with User model

    Usage Example:
        job = ScanJob(
            project_id=project.id,
            triggered_by=user.id,
            trigger_type=TriggerType.MANUAL,
            priority="high",
        )
        session.add(job)
        session.commit()
    """

    __tablename__ = "scan_jobs"

    # Primary Key (also used as job_id)
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
    trigger_type = Column(
        String(50),
        nullable=False,
        default=TriggerType.MANUAL.value,
    )

    # Job Configuration
    priority = Column(
        String(20),
        nullable=False,
        default="normal",
        index=True,
    )
    include_doc_code_sync = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    # Job Status
    status = Column(
        String(20),
        nullable=False,
        default=ScanJobStatus.QUEUED.value,
        index=True,
    )

    # Timing
    queued_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Result/Error
    result = Column(
        JSONB,
        nullable=True,
        comment="Job result with compliance_score, violations_count, etc.",
    )
    error = Column(Text, nullable=True)

    # Retry Configuration
    retry_count = Column(Integer, nullable=False, default=0)
    max_retries = Column(Integer, nullable=False, default=3)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    project = relationship("Project", backref="scan_jobs")
    triggered_by_user = relationship("User", backref="triggered_scan_jobs")

    def __repr__(self) -> str:
        return (
            f"<ScanJob(id={self.id}, project_id={self.project_id}, "
            f"status={self.status}, priority={self.priority})>"
        )

    @property
    def is_finished(self) -> bool:
        """Check if job is in terminal state."""
        return self.status in (
            ScanJobStatus.COMPLETED.value,
            ScanJobStatus.FAILED.value,
            ScanJobStatus.CANCELLED.value,
        )

    @property
    def can_retry(self) -> bool:
        """Check if job can be retried."""
        return (
            self.status == ScanJobStatus.FAILED.value
            and self.retry_count < self.max_retries
        )
