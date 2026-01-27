"""
Sprint 111: MinIO AI-Platform Integration Tests

Tests SDLC Orchestrator's integration with AI-Platform's shared MinIO service.

Architecture:
    SDLC Orchestrator → ai-net → AI-Platform MinIO (ai-platform-minio:9000)

Test Categories:
    1. Connection & Health - Verify MinIO is reachable via ai-net
    2. Evidence Vault - Upload/download evidence files
    3. SHA256 Integrity - Verify file integrity after upload/download
    4. Bucket Operations - Create, list, delete buckets
    5. Presigned URLs - Generate URLs for browser upload/download

Environment:
    - MINIO_ENDPOINT: ai-platform-minio:9000 (via docker-compose)
    - MINIO_ACCESS_KEY: minioadmin
    - MINIO_SECRET_KEY: minioadmin_secure_2026

Author: SDLC Orchestrator Team
Sprint: 111 - AI-Platform Integration Testing
Date: January 2026
"""

import hashlib
import io
import os
import pytest
import tempfile
from datetime import datetime
from typing import Generator
from unittest.mock import patch
from uuid import uuid4

# Skip if MinIO not available (CI environment)
pytestmark = pytest.mark.integration


class TestMinIOConnectionHealth:
    """Test MinIO connection and health via AI-Platform."""

    def test_minio_service_initialization(self):
        """Test: MinIOService initializes with AI-Platform endpoint."""
        from app.services.minio_service import MinIOService

        service = MinIOService()

        assert service.endpoint_url is not None
        assert service.bucket_name is not None
        assert service.access_key is not None
        assert service.client is not None

    def test_minio_bucket_exists_or_create(self):
        """Test: Evidence vault bucket exists or can be created."""
        from app.services.minio_service import MinIOService

        service = MinIOService()

        # Should not raise - creates bucket if not exists
        service.ensure_bucket_exists()

        # Verify bucket exists
        response = service.client.head_bucket(Bucket=service.bucket_name)
        assert response is not None

    def test_minio_health_check(self):
        """Test: MinIO health endpoint responds."""
        import httpx

        # Direct health check to MinIO
        endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9020")
        url = f"http://{endpoint}/minio/health/live"

        try:
            response = httpx.get(url, timeout=5.0)
            assert response.status_code == 200
        except httpx.ConnectError:
            pytest.skip("MinIO not available - skipping health check")


class TestEvidenceVaultOperations:
    """Test Evidence Vault upload/download operations."""

    @pytest.fixture
    def minio_service(self):
        """Fixture: MinIOService instance."""
        from app.services.minio_service import MinIOService
        return MinIOService()

    @pytest.fixture
    def sample_evidence_file(self) -> Generator[tuple, None, None]:
        """Fixture: Create sample evidence file."""
        content = b"Sample evidence content for gate G1 approval.\n" * 100
        sha256 = hashlib.sha256(content).hexdigest()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
            f.write(content)
            f.flush()
            yield f.name, content, sha256

        # Cleanup
        os.unlink(f.name)

    def test_upload_evidence_file(self, minio_service, sample_evidence_file):
        """Test: Upload evidence file to MinIO."""
        file_path, content, expected_sha256 = sample_evidence_file
        object_name = f"test/evidence/{uuid4()}/gate-g1-evidence.txt"

        with open(file_path, "rb") as f:
            bucket, key, sha256 = minio_service.upload_file(
                file_obj=f,
                object_name=object_name,
                content_type="text/plain",
                metadata={"gate_id": "g1", "project_id": "test-project"}
            )

        assert bucket == minio_service.bucket_name
        assert key == object_name
        assert sha256 == expected_sha256

        # Cleanup
        minio_service.delete_file(object_name)

    def test_download_evidence_file(self, minio_service, sample_evidence_file):
        """Test: Download evidence file from MinIO."""
        file_path, original_content, expected_sha256 = sample_evidence_file
        object_name = f"test/evidence/{uuid4()}/gate-g1-evidence.txt"

        # Upload first
        with open(file_path, "rb") as f:
            minio_service.upload_file(f, object_name)

        # Download and verify
        downloaded_content = minio_service.download_file(object_name)

        assert downloaded_content == original_content
        assert hashlib.sha256(downloaded_content).hexdigest() == expected_sha256

        # Cleanup
        minio_service.delete_file(object_name)

    def test_upload_download_roundtrip(self, minio_service, sample_evidence_file):
        """Test: Full upload → download → verify roundtrip."""
        file_path, original_content, expected_sha256 = sample_evidence_file
        object_name = f"test/evidence/{uuid4()}/roundtrip-test.txt"

        # Upload
        with open(file_path, "rb") as f:
            bucket, key, upload_sha256 = minio_service.upload_file(f, object_name)

        # Download
        downloaded_content = minio_service.download_file(object_name)

        # Verify integrity
        download_sha256 = hashlib.sha256(downloaded_content).hexdigest()

        assert upload_sha256 == download_sha256
        assert download_sha256 == expected_sha256
        assert downloaded_content == original_content

        # Cleanup
        minio_service.delete_file(object_name)

    def test_upload_large_file_multipart(self, minio_service):
        """Test: Upload large file using multipart (>5MB)."""
        # Create 10MB file
        content = b"x" * (10 * 1024 * 1024)
        expected_sha256 = hashlib.sha256(content).hexdigest()
        object_name = f"test/large/{uuid4()}/large-evidence.bin"

        file_obj = io.BytesIO(content)

        bucket, key, sha256 = minio_service.upload_multipart(
            file_obj=file_obj,
            object_name=object_name,
            content_type="application/octet-stream",
            part_size=5 * 1024 * 1024  # 5MB parts
        )

        assert bucket == minio_service.bucket_name
        assert key == object_name
        assert sha256 == expected_sha256

        # Verify download
        downloaded = minio_service.download_file(object_name)
        assert len(downloaded) == 10 * 1024 * 1024
        assert hashlib.sha256(downloaded).hexdigest() == expected_sha256

        # Cleanup
        minio_service.delete_file(object_name)


class TestSHA256IntegrityVerification:
    """Test SHA256 integrity verification."""

    @pytest.fixture
    def minio_service(self):
        """Fixture: MinIOService instance."""
        from app.services.minio_service import MinIOService
        return MinIOService()

    def test_compute_sha256_deterministic(self, minio_service):
        """Test: SHA256 computation is deterministic."""
        content = b"Test content for SHA256 verification"

        hash1 = minio_service.compute_sha256(content)
        hash2 = minio_service.compute_sha256(content)

        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 hex length

    def test_verify_sha256_valid(self, minio_service):
        """Test: SHA256 verification passes for valid content."""
        content = b"Test content for verification"
        expected_hash = hashlib.sha256(content).hexdigest()

        is_valid = minio_service.verify_sha256(content, expected_hash)

        assert is_valid is True

    def test_verify_sha256_invalid(self, minio_service):
        """Test: SHA256 verification fails for tampered content."""
        original_content = b"Original content"
        tampered_content = b"Tampered content"

        original_hash = hashlib.sha256(original_content).hexdigest()

        is_valid = minio_service.verify_sha256(tampered_content, original_hash)

        assert is_valid is False

    def test_uploaded_file_has_sha256_metadata(self, minio_service):
        """Test: Uploaded file has SHA256 in metadata."""
        content = b"Content with SHA256 metadata"
        expected_sha256 = hashlib.sha256(content).hexdigest()
        object_name = f"test/metadata/{uuid4()}/file-with-hash.txt"

        file_obj = io.BytesIO(content)
        minio_service.upload_file(file_obj, object_name)

        # Get metadata
        metadata = minio_service.get_file_metadata(object_name)

        assert "sha256" in metadata
        assert metadata["sha256"] == expected_sha256

        # Cleanup
        minio_service.delete_file(object_name)


class TestPresignedURLs:
    """Test presigned URL generation for browser access."""

    @pytest.fixture
    def minio_service(self):
        """Fixture: MinIOService instance."""
        from app.services.minio_service import MinIOService
        return MinIOService()

    def test_generate_presigned_upload_url(self, minio_service):
        """Test: Generate presigned URL for upload."""
        object_name = f"test/presigned/{uuid4()}/upload-target.txt"

        url = minio_service.generate_presigned_upload_url(
            object_name=object_name,
            expiration=3600,
            content_type="text/plain"
        )

        assert url is not None
        assert "X-Amz-Algorithm" in url
        assert "X-Amz-Signature" in url
        assert object_name in url

    def test_generate_presigned_download_url(self, minio_service):
        """Test: Generate presigned URL for download."""
        content = b"Content for presigned download"
        object_name = f"test/presigned/{uuid4()}/download-source.txt"

        # Upload file first
        file_obj = io.BytesIO(content)
        minio_service.upload_file(file_obj, object_name)

        # Generate presigned URL
        url = minio_service.generate_presigned_download_url(
            object_name=object_name,
            expiration=3600
        )

        assert url is not None
        assert "X-Amz-Algorithm" in url
        assert "X-Amz-Signature" in url

        # Cleanup
        minio_service.delete_file(object_name)

    def test_presigned_url_expiration(self, minio_service):
        """Test: Presigned URL has correct expiration."""
        object_name = f"test/presigned/{uuid4()}/expiration-test.txt"
        expiration_seconds = 300  # 5 minutes

        url = minio_service.generate_presigned_upload_url(
            object_name=object_name,
            expiration=expiration_seconds
        )

        # URL should contain X-Amz-Expires parameter
        assert f"X-Amz-Expires={expiration_seconds}" in url


class TestBucketOperations:
    """Test bucket management operations."""

    @pytest.fixture
    def minio_service(self):
        """Fixture: MinIOService instance."""
        from app.services.minio_service import MinIOService
        return MinIOService()

    def test_ensure_bucket_creates_if_not_exists(self, minio_service):
        """Test: ensure_bucket_exists creates bucket if missing."""
        # This should not raise
        minio_service.ensure_bucket_exists()

        # Verify bucket exists
        try:
            minio_service.client.head_bucket(Bucket=minio_service.bucket_name)
            bucket_exists = True
        except Exception:
            bucket_exists = False

        assert bucket_exists is True


class TestFileMetadata:
    """Test file metadata operations."""

    @pytest.fixture
    def minio_service(self):
        """Fixture: MinIOService instance."""
        from app.services.minio_service import MinIOService
        return MinIOService()

    def test_get_file_metadata(self, minio_service):
        """Test: Get file metadata without downloading content."""
        content = b"Content for metadata test"
        object_name = f"test/metadata/{uuid4()}/metadata-test.txt"

        file_obj = io.BytesIO(content)
        minio_service.upload_file(
            file_obj,
            object_name,
            content_type="text/plain",
            metadata={"gate_id": "g1", "user_id": "test-user"}
        )

        # Get metadata
        metadata = minio_service.get_file_metadata(object_name)

        assert metadata["ContentType"] == "text/plain"
        assert metadata["ContentLength"] == len(content)
        assert "LastModified" in metadata
        assert metadata.get("gate_id") == "g1"
        assert metadata.get("user_id") == "test-user"

        # Cleanup
        minio_service.delete_file(object_name)

    def test_file_not_found_raises_error(self, minio_service):
        """Test: Getting metadata for non-existent file raises error."""
        from botocore.exceptions import ClientError

        object_name = f"test/nonexistent/{uuid4()}/does-not-exist.txt"

        with pytest.raises(ClientError):
            minio_service.get_file_metadata(object_name)


class TestDeleteOperations:
    """Test file deletion operations."""

    @pytest.fixture
    def minio_service(self):
        """Fixture: MinIOService instance."""
        from app.services.minio_service import MinIOService
        return MinIOService()

    def test_delete_file(self, minio_service):
        """Test: Delete file from MinIO."""
        content = b"Content to be deleted"
        object_name = f"test/delete/{uuid4()}/delete-me.txt"

        # Upload
        file_obj = io.BytesIO(content)
        minio_service.upload_file(file_obj, object_name)

        # Verify exists
        metadata = minio_service.get_file_metadata(object_name)
        assert metadata is not None

        # Delete
        minio_service.delete_file(object_name)

        # Verify deleted
        from botocore.exceptions import ClientError
        with pytest.raises(ClientError):
            minio_service.get_file_metadata(object_name)


class TestAIPlatformIntegration:
    """Test specific AI-Platform integration scenarios."""

    @pytest.fixture
    def minio_service(self):
        """Fixture: MinIOService instance."""
        from app.services.minio_service import MinIOService
        return MinIOService()

    def test_evidence_vault_bucket_access(self, minio_service):
        """Test: SDLC can access evidence-vault bucket on AI-Platform."""
        # Ensure bucket exists
        minio_service.ensure_bucket_exists()

        # Upload test evidence
        content = b"Evidence for gate G1 approval"
        object_name = f"evidence/gate-g1/{uuid4()}/approval-document.txt"

        file_obj = io.BytesIO(content)
        bucket, key, sha256 = minio_service.upload_file(
            file_obj,
            object_name,
            metadata={"gate": "G1", "type": "approval"}
        )

        assert bucket == minio_service.bucket_name

        # Cleanup
        minio_service.delete_file(object_name)

    def test_cross_project_isolation(self, minio_service):
        """Test: SDLC evidence is isolated from AI-Platform documents."""
        # SDLC uses evidence-vault bucket
        # AI-Platform uses documents bucket
        # They should be separate

        sdlc_bucket = minio_service.bucket_name  # evidence-vault

        # Verify SDLC bucket is evidence-focused
        assert "evidence" in sdlc_bucket.lower() or sdlc_bucket == "evidence-vault-v2"

    def test_performance_upload_under_1_second(self, minio_service):
        """Test: Evidence upload completes in <1 second for small files."""
        import time

        content = b"Small evidence file for performance test" * 10  # ~400 bytes
        object_name = f"test/performance/{uuid4()}/small-file.txt"

        file_obj = io.BytesIO(content)

        start_time = time.time()
        minio_service.upload_file(file_obj, object_name)
        upload_time = time.time() - start_time

        assert upload_time < 1.0, f"Upload took {upload_time:.2f}s, expected <1s"

        # Cleanup
        minio_service.delete_file(object_name)

    def test_performance_download_under_1_second(self, minio_service):
        """Test: Evidence download completes in <1 second for small files."""
        import time

        content = b"Small evidence file for download test" * 10
        object_name = f"test/performance/{uuid4()}/download-test.txt"

        file_obj = io.BytesIO(content)
        minio_service.upload_file(file_obj, object_name)

        start_time = time.time()
        downloaded = minio_service.download_file(object_name)
        download_time = time.time() - start_time

        assert download_time < 1.0, f"Download took {download_time:.2f}s, expected <1s"
        assert downloaded == content

        # Cleanup
        minio_service.delete_file(object_name)


def run_quick_validation():
    """Quick validation script for MinIO AI-Platform integration."""
    print("\n" + "=" * 60)
    print("MinIO AI-Platform Integration Validation")
    print("=" * 60 + "\n")

    tests = [
        ("Service Initialization", test_service_init),
        ("Bucket Access", test_bucket_access),
        ("Upload/Download Roundtrip", test_roundtrip),
        ("SHA256 Integrity", test_sha256),
        ("Presigned URL", test_presigned),
        ("Performance (<1s)", test_performance),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            print(f"  {name} PASSED")
            passed += 1
        except Exception as e:
            print(f"  {name} FAILED: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")

    return failed == 0


def test_service_init():
    from app.services.minio_service import MinIOService
    service = MinIOService()
    assert service.client is not None


def test_bucket_access():
    from app.services.minio_service import MinIOService
    service = MinIOService()
    service.ensure_bucket_exists()


def test_roundtrip():
    from app.services.minio_service import MinIOService
    service = MinIOService()

    content = b"Roundtrip test content"
    object_name = f"test/validation/{uuid4()}.txt"

    file_obj = io.BytesIO(content)
    service.upload_file(file_obj, object_name)

    downloaded = service.download_file(object_name)
    assert downloaded == content

    service.delete_file(object_name)


def test_sha256():
    from app.services.minio_service import MinIOService

    content = b"SHA256 test content"
    expected = hashlib.sha256(content).hexdigest()
    actual = MinIOService.compute_sha256(content)

    assert actual == expected


def test_presigned():
    from app.services.minio_service import MinIOService
    service = MinIOService()

    url = service.generate_presigned_upload_url(
        f"test/presigned/{uuid4()}.txt",
        expiration=300
    )
    assert "X-Amz-Signature" in url


def test_performance():
    import time
    from app.services.minio_service import MinIOService
    service = MinIOService()

    content = b"Performance test" * 100
    object_name = f"test/perf/{uuid4()}.txt"

    file_obj = io.BytesIO(content)

    start = time.time()
    service.upload_file(file_obj, object_name)
    service.download_file(object_name)
    elapsed = time.time() - start

    service.delete_file(object_name)

    assert elapsed < 2.0, f"Roundtrip took {elapsed:.2f}s"


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(__file__).replace("/tests/integration/test_minio_ai_platform.py", ""))
    success = run_quick_validation()
    sys.exit(0 if success else 1)
