"""
=========================================================================
Evidence Manifest Model - Tamper-Evident Hash Chain
SDLC Orchestrator - Sprint 82 (Pre-Launch Hardening)

Version: 1.0.0
Date: January 19, 2026
Status: ACTIVE - P0 Launch Blocker
Authority: CTO Approved (Pre-Launch Hardening Plan)
Framework: SDLC 5.1.3 P7 (Documentation Permanence)

Purpose:
- Tamper-evident manifest with hash chain linking
- HMAC-SHA256 signed manifests for audit
- Evidence integrity verification
- Compliance with 7-year retention policy

Security Standards:
- SHA256 hash chain (each manifest links to previous)
- HMAC-SHA256 signatures with server secret
- Append-only design (manifests never deleted)
- Go/No-Go criteria: Tamper-evident test pass

Zero Mock Policy: Real SQLAlchemy model with full implementation
=========================================================================
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, String, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class EvidenceManifest(Base):
    """
    Tamper-evident manifest for Evidence Vault.

    Design (Sprint 82 P0 Blocker):
    1. Each artifact gets SHA256 hash stored in manifest entry
    2. Manifest includes previous_manifest_hash (chain)
    3. Manifest is signed with server key (HMAC-SHA256)
    4. Append-only table (manifests never modified/deleted)

    Chain Verification:
    - manifest_n.previous_hash == hash(manifest_n-1)
    - Any tampering breaks the chain
    - Verification runs from oldest to newest

    Hash Computation:
    - content = JSON(manifest_id, project_id, previous_hash, artifacts)
    - manifest_hash = SHA256(content)
    - signature = HMAC-SHA256(manifest_hash, server_secret)

    Fields:
        - id: UUID primary key
        - project_id: Foreign key to Project
        - sequence_number: Auto-increment within project (for ordering)
        - manifest_hash: SHA256 of manifest content (64 chars)
        - previous_manifest_hash: Links to previous manifest (NULL for first)
        - artifacts: JSONB array of artifact entries
        - signature: HMAC-SHA256 signature (64 chars)
        - is_genesis: True if first manifest in chain
        - created_at: Manifest creation timestamp
        - created_by: User who triggered manifest creation

    Artifacts JSONB Schema:
        [
            {
                "artifact_id": "uuid",
                "sha256": "64-char hash",
                "path": "evidence/project-123/file.pdf",
                "size": 1234567,
                "file_name": "original-name.pdf",
                "evidence_type": "DESIGN_DOCUMENT",
                "uploaded_at": "2026-01-19T12:00:00Z"
            },
            ...
        ]

    Usage Example:
        manifest = EvidenceManifest(
            project_id=project.id,
            sequence_number=1,
            manifest_hash="abc123...",
            previous_manifest_hash=None,  # Genesis
            artifacts=[{...}],
            signature="def456...",
            is_genesis=True,
            created_by=user.id
        )

    Verification Example:
        # Verify chain integrity
        for i, manifest in enumerate(manifests_ordered_by_seq):
            if i > 0:
                expected_prev = manifests[i-1].manifest_hash
                assert manifest.previous_manifest_hash == expected_prev
            # Verify signature
            expected_sig = hmac_sha256(manifest.manifest_hash, secret)
            assert manifest.signature == expected_sig
    """

    __tablename__ = "evidence_manifests"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Project Relationship (evidence belongs to project)
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Sequence number within project (for ordering without timestamps)
    sequence_number = Column(
        BigInteger,
        nullable=False,
    )

    # Hash Chain
    manifest_hash = Column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
        comment="SHA256 of manifest content",
    )
    previous_manifest_hash = Column(
        String(64),
        nullable=True,
        index=True,
        comment="Hash of previous manifest (NULL for genesis)",
    )

    # Artifacts included in this manifest
    artifacts = Column(
        JSONB,
        nullable=False,
        default=list,
        comment="Array of artifact entries with hashes",
    )

    # Signature for tamper detection
    signature = Column(
        String(64),
        nullable=False,
        comment="HMAC-SHA256 signature",
    )

    # Genesis flag (first manifest in chain)
    is_genesis = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="True if first manifest in project chain",
    )

    # Audit timestamps
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        comment="Manifest creation timestamp (immutable)",
    )

    # Created by (user who triggered manifest creation)
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Relationships
    project = relationship("Project", back_populates="evidence_manifests")
    creator = relationship("User", foreign_keys=[created_by])

    # Table constraints
    __table_args__ = (
        # Unique sequence per project
        Index(
            "uq_evidence_manifests_project_sequence",
            "project_id",
            "sequence_number",
            unique=True,
        ),
        # Fast lookup by previous hash (for chain verification)
        Index(
            "idx_evidence_manifests_chain",
            "project_id",
            "previous_manifest_hash",
        ),
        # Genesis manifests must have NULL previous_hash
        # (enforced in application layer)
    )

    def __repr__(self) -> str:
        return (
            f"<EvidenceManifest(id={self.id}, project_id={self.project_id}, "
            f"seq={self.sequence_number}, is_genesis={self.is_genesis})>"
        )

    @property
    def artifact_count(self) -> int:
        """Get number of artifacts in this manifest."""
        return len(self.artifacts) if self.artifacts else 0

    @property
    def total_size_bytes(self) -> int:
        """Get total size of all artifacts in bytes."""
        if not self.artifacts:
            return 0
        return sum(a.get("size", 0) for a in self.artifacts)

    @property
    def total_size_mb(self) -> float:
        """Get total size in megabytes."""
        return self.total_size_bytes / (1024 * 1024)


class EvidenceManifestVerification(Base):
    """
    Evidence Manifest Verification Log.

    Records each verification run of the hash chain.
    Used for audit and compliance reporting.

    Fields:
        - id: UUID primary key
        - project_id: Project being verified
        - verified_at: Verification timestamp
        - manifests_checked: Number of manifests verified
        - chain_valid: Overall result (True = all valid)
        - first_broken_at: UUID of first broken manifest (if any)
        - error_message: Error details (if invalid)
        - verified_by: System or user who ran verification

    Usage:
        - Scheduled daily verification cron
        - On-demand verification via API
        - Compliance audit reports
    """

    __tablename__ = "evidence_manifest_verifications"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Project being verified
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Verification results
    verified_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )
    manifests_checked = Column(
        BigInteger,
        nullable=False,
        default=0,
    )
    chain_valid = Column(
        Boolean,
        nullable=False,
        index=True,
    )

    # Error details (if invalid)
    first_broken_at = Column(
        UUID(as_uuid=True),
        ForeignKey("evidence_manifests.id", ondelete="SET NULL"),
        nullable=True,
    )
    error_message = Column(
        Text,
        nullable=True,
    )

    # Verification metadata
    verified_by = Column(
        String(100),
        nullable=False,
        comment="'system-cron', 'api-request', 'user-{id}'",
    )

    # Relationships
    project = relationship("Project")
    broken_manifest = relationship("EvidenceManifest", foreign_keys=[first_broken_at])

    def __repr__(self) -> str:
        status = "VALID" if self.chain_valid else "INVALID"
        return (
            f"<EvidenceManifestVerification(project_id={self.project_id}, "
            f"status={status}, checked={self.manifests_checked})>"
        )


