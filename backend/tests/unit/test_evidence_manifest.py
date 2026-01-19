"""
=========================================================================
Sprint 82 - Unit Tests: Evidence Manifest Service
SDLC Orchestrator - Stage 04 (BUILD)

Version: 1.0.0
Date: January 19, 2026
Status: ACTIVE - Sprint 82 (Pre-Launch Hardening)
Authority: CTO + Security Lead Approved
Ticket: Sprint 82 P0 - Evidence Hash Chain

Test Coverage:
- UT-82.1: create_manifest creates manifest with hash
- UT-82.2: create_manifest links to previous manifest (chain)
- UT-82.3: verify_manifest validates hash integrity
- UT-82.4: verify_manifest detects tampering
- UT-82.5: verify_chain validates entire chain
- UT-82.6: verify_chain detects broken chain
- UT-82.7: genesis manifest has no previous_hash
- UT-82.8: sequence numbers are monotonically increasing
- UT-82.9: anonymize_manifest removes PII
- UT-82.10: Ed25519 signing and verification

Go/No-Go Criteria (Feb 28, 2026):
- Evidence hash chain: Tamper-evident test pass ✅

Zero Mock Policy: Real cryptography, mocked database
=========================================================================
"""

import pytest
from datetime import datetime, timezone
from uuid import uuid4

from app.services.evidence_manifest_service import (
    EvidenceManifestService,
    EvidenceManifest,
    ArtifactEntry,
    ManifestVerificationResult,
    KeyStorageService,
    HashChainBrokenError,
    ManifestVerificationError,
)


# =========================================================================
# Fixtures
# =========================================================================


@pytest.fixture
def key_storage():
    """Create key storage with test keys."""
    storage = KeyStorageService()
    # Generate test keys
    private_bytes, public_bytes, key_id = storage.generate_key_pair()
    storage._private_key = private_bytes
    storage._public_key = public_bytes
    storage._key_id = key_id
    return storage


@pytest.fixture
def manifest_service(key_storage):
    """Create manifest service with test keys."""
    return EvidenceManifestService(key_storage=key_storage)


@pytest.fixture
def sample_artifact():
    """Create sample artifact entry."""
    return ArtifactEntry(
        artifact_id=uuid4(),
        file_path="evidence/project-123/design.pdf",
        sha256_hash="a" * 64,
        size_bytes=1024,
        content_type="application/pdf",
        uploaded_at=datetime.now(timezone.utc),
        uploaded_by=uuid4(),
        metadata={"type": "design_document"},
    )


@pytest.fixture
def sample_artifacts(sample_artifact):
    """Create list of sample artifacts."""
    return [
        sample_artifact,
        ArtifactEntry(
            artifact_id=uuid4(),
            file_path="evidence/project-123/test-results.json",
            sha256_hash="b" * 64,
            size_bytes=2048,
            content_type="application/json",
            uploaded_at=datetime.now(timezone.utc),
            uploaded_by=uuid4(),
            metadata={"type": "test_results"},
        ),
    ]


# =========================================================================
# Hash/Signature Tests
# =========================================================================


class TestManifestCreation:
    """Tests for manifest creation."""

    def test_create_manifest_has_hash(self, manifest_service, sample_artifacts):
        """UT-82.1: create_manifest creates manifest with hash."""
        # Arrange
        project_id = uuid4()

        # Act
        manifest = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts,
            sequence_number=1,
        )

        # Assert
        assert manifest.manifest_hash is not None
        assert len(manifest.manifest_hash) == 64  # SHA256 hex
        assert manifest.manifest_id is not None

    def test_create_manifest_chain_linking(self, manifest_service, sample_artifacts):
        """UT-82.2: create_manifest links to previous manifest."""
        # Arrange
        project_id = uuid4()

        # Create first manifest (genesis)
        manifest1 = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts[:1],
            sequence_number=1,
        )

        # Act - Create second manifest linked to first
        manifest2 = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts[1:],
            sequence_number=2,
            previous_manifest=manifest1,
        )

        # Assert
        assert manifest2.previous_manifest_hash == manifest1.manifest_hash
        assert manifest2.sequence_number == 2

    def test_genesis_manifest_no_previous(self, manifest_service, sample_artifacts):
        """UT-82.7: Genesis manifest has no previous_hash."""
        # Arrange
        project_id = uuid4()

        # Act
        manifest = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts,
            sequence_number=1,
            previous_manifest=None,
        )

        # Assert
        assert manifest.previous_manifest_hash is None


class TestManifestVerification:
    """Tests for manifest verification."""

    def test_verify_manifest_valid(self, manifest_service, sample_artifacts):
        """UT-82.3: verify_manifest validates hash integrity."""
        # Arrange
        project_id = uuid4()
        manifest = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts,
            sequence_number=1,
        )

        # Act
        result = manifest_service.verify_manifest(manifest)

        # Assert
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_verify_manifest_detects_tampering(self, manifest_service, sample_artifacts):
        """UT-82.4: verify_manifest detects hash tampering."""
        # Arrange
        project_id = uuid4()
        manifest = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts,
            sequence_number=1,
        )

        # Tamper with manifest hash
        manifest.manifest_hash = "x" * 64

        # Act
        result = manifest_service.verify_manifest(manifest)

        # Assert
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert "Hash mismatch" in result.errors[0]


class TestChainVerification:
    """Tests for hash chain verification."""

    def test_verify_chain_valid(self, manifest_service, sample_artifacts):
        """UT-82.5: verify_chain validates entire chain."""
        # Arrange
        project_id = uuid4()

        # Create chain of 3 manifests
        m1 = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts[:1],
            sequence_number=1,
        )
        m2 = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts[1:],
            sequence_number=2,
            previous_manifest=m1,
        )
        m3 = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts,
            sequence_number=3,
            previous_manifest=m2,
        )

        # Act
        result = manifest_service.verify_chain([m1, m2, m3])

        # Assert
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_verify_chain_detects_broken_chain(self, manifest_service, sample_artifacts):
        """UT-82.6: verify_chain detects broken hash chain."""
        # Arrange
        project_id = uuid4()

        # Create chain
        m1 = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts[:1],
            sequence_number=1,
        )
        m2 = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts[1:],
            sequence_number=2,
            previous_manifest=m1,
        )

        # Break the chain by modifying m2's previous_manifest_hash
        m2.previous_manifest_hash = "broken" + "0" * 58

        # Act
        result = manifest_service.verify_chain([m1, m2])

        # Assert
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert "chain broken" in result.errors[0].lower()

    def test_verify_chain_detects_sequence_gap(self, manifest_service, sample_artifacts):
        """UT-82.8: verify_chain detects sequence gaps."""
        # Arrange
        project_id = uuid4()

        # Create manifests with sequence gap
        m1 = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts[:1],
            sequence_number=1,
        )
        m3 = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts[1:],
            sequence_number=3,  # Gap - missing sequence 2
            previous_manifest=m1,
        )

        # Act
        result = manifest_service.verify_chain([m1, m3])

        # Assert
        assert result.is_valid is False
        assert any("gap" in e.lower() for e in result.errors)

    def test_verify_empty_chain(self, manifest_service):
        """verify_chain handles empty chain gracefully."""
        # Act
        result = manifest_service.verify_chain([])

        # Assert
        assert result.is_valid is True
        assert len(result.warnings) > 0
        assert "empty" in result.warnings[0].lower()


class TestAnonymization:
    """Tests for GDPR anonymization."""

    def test_anonymize_manifest_removes_pii(self, manifest_service, sample_artifacts):
        """UT-82.9: anonymize_manifest removes user PII."""
        # Arrange
        user_id = uuid4()
        sample_artifacts[0].uploaded_by = user_id
        sample_artifacts[0].metadata = {
            "user_email": "test@example.com",
            "user_name": "John Doe",
            "ip_address": "192.168.1.1",
            "safe_data": "keep_this",
        }

        project_id = uuid4()
        manifest = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts,
            sequence_number=1,
        )

        # Act
        anonymized = manifest_service.anonymize_manifest(
            manifest,
            user_id_mapping={user_id: uuid4()},
        )

        # Assert
        assert anonymized.manifest_hash == manifest.manifest_hash  # Hash preserved
        assert anonymized.signature == manifest.signature  # Signature preserved
        # PII should be removed from metadata
        anon_artifact = anonymized.artifacts[0]
        assert "user_email" not in anon_artifact.metadata
        assert "user_name" not in anon_artifact.metadata
        assert "ip_address" not in anon_artifact.metadata
        assert anon_artifact.metadata.get("safe_data") == "keep_this"


class TestEd25519Signing:
    """Tests for Ed25519 cryptographic signing."""

    def test_manifest_is_signed(self, manifest_service, sample_artifacts):
        """UT-82.10a: create_manifest signs with Ed25519."""
        # Arrange
        project_id = uuid4()

        # Act
        manifest = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts,
            sequence_number=1,
        )

        # Assert
        assert manifest.signature is not None
        assert len(manifest.signature) > 0  # Base64 encoded signature
        assert manifest.signer_key_id is not None

    def test_signature_verification_succeeds(self, manifest_service, sample_artifacts):
        """UT-82.10b: Valid signature passes verification."""
        # Arrange
        project_id = uuid4()
        manifest = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts,
            sequence_number=1,
        )

        # Act
        result = manifest_service.verify_manifest(manifest)

        # Assert
        assert result.is_valid is True
        assert not any("signature" in e.lower() for e in result.errors)

    def test_invalid_signature_detected(self, manifest_service, sample_artifacts):
        """UT-82.10c: Invalid signature is detected."""
        # Arrange
        project_id = uuid4()
        manifest = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts,
            sequence_number=1,
        )

        # Tamper with signature
        manifest.signature = "invalidbase64signature" + "A" * 40

        # Act
        result = manifest_service.verify_manifest(manifest)

        # Assert
        assert result.is_valid is False
        assert any("signature" in e.lower() for e in result.errors)


class TestManifestComputation:
    """Tests for hash computation."""

    def test_hash_is_deterministic(self, manifest_service, sample_artifacts):
        """Hash computation is deterministic."""
        # Arrange
        project_id = uuid4()
        manifest = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts,
            sequence_number=1,
        )

        # Act
        hash1 = manifest.compute_hash()
        hash2 = manifest.compute_hash()

        # Assert
        assert hash1 == hash2

    def test_different_artifacts_different_hash(self, manifest_service):
        """Different artifacts produce different hashes."""
        # Arrange
        project_id = uuid4()

        artifact1 = ArtifactEntry(
            artifact_id=uuid4(),
            file_path="file1.txt",
            sha256_hash="a" * 64,
            size_bytes=100,
            content_type="text/plain",
            uploaded_at=datetime.now(timezone.utc),
            uploaded_by=uuid4(),
        )

        artifact2 = ArtifactEntry(
            artifact_id=uuid4(),
            file_path="file2.txt",
            sha256_hash="b" * 64,
            size_bytes=200,
            content_type="text/plain",
            uploaded_at=datetime.now(timezone.utc),
            uploaded_by=uuid4(),
        )

        # Act
        m1 = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=[artifact1],
            sequence_number=1,
        )
        m2 = manifest_service.create_manifest(
            project_id=project_id,
            artifacts=[artifact2],
            sequence_number=2,
            previous_manifest=m1,
        )

        # Assert
        assert m1.manifest_hash != m2.manifest_hash


class TestKeyStorage:
    """Tests for key storage."""

    def test_generate_key_pair(self):
        """Key storage generates valid key pairs."""
        # Arrange
        storage = KeyStorageService()

        # Act
        private_bytes, public_bytes, key_id = storage.generate_key_pair()

        # Assert
        assert private_bytes is not None
        assert public_bytes is not None
        assert len(private_bytes) == 32  # Ed25519 private key
        assert len(public_bytes) == 32  # Ed25519 public key
        assert key_id.startswith("key-")

    def test_unsigned_manifest_warning(self, sample_artifacts):
        """Unsigned manifests produce warning (not error)."""
        # Arrange - Create service without keys
        storage = KeyStorageService()
        storage._private_key = None
        service = EvidenceManifestService(key_storage=storage)

        project_id = uuid4()
        manifest = service.create_manifest(
            project_id=project_id,
            artifacts=sample_artifacts,
            sequence_number=1,
        )

        # Act
        result = service.verify_manifest(manifest)

        # Assert
        assert result.is_valid is True  # Unsigned is valid (legacy support)
        assert any("unsigned" in w.lower() for w in result.warnings)
