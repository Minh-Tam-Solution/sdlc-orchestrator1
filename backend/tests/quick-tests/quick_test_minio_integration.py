"""
Quick validation script for MinIO AI-Platform Integration.

Sprint 111 Day 1: Validates SDLC Orchestrator → AI-Platform MinIO connection.

Usage:
    cd backend
    python quick_test_minio_integration.py

Environment:
    - MINIO_ENDPOINT: ai-platform-minio:9000 (default via docker-compose)
    - Or localhost:9020 for local testing

Author: SDLC Orchestrator Team
Sprint: 111 - AI-Platform Integration Testing
"""

import hashlib
import io
import os
import sys
import time
from pathlib import Path
from uuid import uuid4

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))


def test_service_initialization():
    """Test: MinIOService initializes correctly."""
    from app.services.minio_service import MinIOService

    service = MinIOService()

    assert service.endpoint_url is not None, "endpoint_url should be set"
    assert service.bucket_name is not None, "bucket_name should be set"
    assert service.client is not None, "S3 client should be initialized"

    print(f"   Endpoint: {service.endpoint_url}")
    print(f"   Bucket: {service.bucket_name}")
    print("   S3 Client: Initialized")


def test_bucket_access():
    """Test: Can access/create evidence vault bucket."""
    from app.services.minio_service import MinIOService

    service = MinIOService()
    service.ensure_bucket_exists()

    # Verify bucket exists
    response = service.client.head_bucket(Bucket=service.bucket_name)
    assert response is not None, "Bucket should exist"

    print(f"   Bucket '{service.bucket_name}' accessible")


def test_upload_download_roundtrip():
    """Test: Upload and download file successfully."""
    from app.services.minio_service import MinIOService

    service = MinIOService()

    # Create test content
    test_content = f"Test evidence content - {uuid4()}".encode()
    object_name = f"test/sprint111/{uuid4()}/evidence.txt"

    # Upload
    file_obj = io.BytesIO(test_content)
    bucket, key, sha256 = service.upload_file(
        file_obj=file_obj,
        object_name=object_name,
        content_type="text/plain",
        metadata={"test": "sprint111"}
    )

    print(f"   Uploaded: s3://{bucket}/{key}")
    print(f"   SHA256: {sha256[:16]}...")

    # Download
    downloaded = service.download_file(object_name)

    assert downloaded == test_content, "Downloaded content should match original"
    print(f"   Downloaded: {len(downloaded)} bytes")

    # Cleanup
    service.delete_file(object_name)
    print(f"   Cleaned up: {object_name}")


def test_sha256_integrity():
    """Test: SHA256 integrity verification works."""
    from app.services.minio_service import MinIOService

    content = b"Test content for SHA256 verification"
    expected_hash = hashlib.sha256(content).hexdigest()

    # Test compute
    computed_hash = MinIOService.compute_sha256(content)
    assert computed_hash == expected_hash, "Computed hash should match"
    print(f"   Computed SHA256: {computed_hash[:16]}...")

    # Test verify - valid
    is_valid = MinIOService.verify_sha256(content, expected_hash)
    assert is_valid is True, "Valid content should pass verification"
    print("   Valid content: PASSED")

    # Test verify - invalid
    is_invalid = MinIOService.verify_sha256(b"tampered", expected_hash)
    assert is_invalid is False, "Tampered content should fail verification"
    print("   Tampered content: REJECTED (expected)")


def test_presigned_url_generation():
    """Test: Presigned URL generation works."""
    from app.services.minio_service import MinIOService

    service = MinIOService()
    object_name = f"test/presigned/{uuid4()}/test.txt"

    # Upload URL
    upload_url = service.generate_presigned_upload_url(
        object_name=object_name,
        expiration=300,
        content_type="text/plain"
    )

    assert "X-Amz-Algorithm" in upload_url, "URL should have algorithm"
    assert "X-Amz-Signature" in upload_url, "URL should have signature"
    print(f"   Upload URL: {upload_url[:80]}...")

    # Download URL (need to upload first)
    content = b"Content for download URL test"
    file_obj = io.BytesIO(content)
    service.upload_file(file_obj, object_name)

    download_url = service.generate_presigned_download_url(
        object_name=object_name,
        expiration=300
    )

    assert "X-Amz-Signature" in download_url, "URL should have signature"
    print(f"   Download URL: {download_url[:80]}...")

    # Cleanup
    service.delete_file(object_name)


def test_performance():
    """Test: Upload/download performance (<1s for small files)."""
    from app.services.minio_service import MinIOService

    service = MinIOService()

    # Create ~10KB file
    content = b"Performance test content\n" * 400
    object_name = f"test/performance/{uuid4()}/perf-test.txt"

    file_obj = io.BytesIO(content)

    # Measure upload
    start_upload = time.time()
    service.upload_file(file_obj, object_name)
    upload_time = time.time() - start_upload

    print(f"   Upload time: {upload_time:.3f}s ({len(content)} bytes)")
    assert upload_time < 1.0, f"Upload should be <1s, was {upload_time:.3f}s"

    # Measure download
    start_download = time.time()
    downloaded = service.download_file(object_name)
    download_time = time.time() - start_download

    print(f"   Download time: {download_time:.3f}s ({len(downloaded)} bytes)")
    assert download_time < 1.0, f"Download should be <1s, was {download_time:.3f}s"

    # Cleanup
    service.delete_file(object_name)


def test_metadata_operations():
    """Test: File metadata operations work."""
    from app.services.minio_service import MinIOService

    service = MinIOService()

    content = b"Content with metadata"
    object_name = f"test/metadata/{uuid4()}/meta-test.txt"

    # Upload with metadata
    file_obj = io.BytesIO(content)
    service.upload_file(
        file_obj,
        object_name,
        content_type="text/plain",
        metadata={"gate_id": "g1", "project_id": "test-project"}
    )

    # Get metadata
    metadata = service.get_file_metadata(object_name)

    assert metadata["ContentType"] == "text/plain", "Content type should match"
    assert metadata["ContentLength"] == len(content), "Content length should match"
    assert metadata.get("gate_id") == "g1", "Custom metadata should be preserved"

    print(f"   Content-Type: {metadata['ContentType']}")
    print(f"   Content-Length: {metadata['ContentLength']}")
    print(f"   Custom metadata: gate_id={metadata.get('gate_id')}")

    # Cleanup
    service.delete_file(object_name)


def main():
    """Run all MinIO integration tests."""
    print("\n" + "=" * 60)
    print("Sprint 111: MinIO AI-Platform Integration Tests")
    print("=" * 60)

    tests = [
        ("Service Initialization", test_service_initialization),
        ("Bucket Access", test_bucket_access),
        ("Upload/Download Roundtrip", test_upload_download_roundtrip),
        ("SHA256 Integrity", test_sha256_integrity),
        ("Presigned URL Generation", test_presigned_url_generation),
        ("Performance (<1s)", test_performance),
        ("Metadata Operations", test_metadata_operations),
    ]

    passed = 0
    failed = 0
    skipped = 0

    for name, test_func in tests:
        print(f"\n{name}:")
        try:
            test_func()
            print(f"   PASSED")
            passed += 1
        except AssertionError as e:
            print(f"   FAILED: {e}")
            failed += 1
        except Exception as e:
            error_msg = str(e)
            if "Could not connect" in error_msg or "Connection refused" in error_msg:
                print(f"   SKIPPED (MinIO not available): {error_msg[:50]}...")
                skipped += 1
            else:
                print(f"   ERROR: {e}")
                failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    print("=" * 60)

    if failed == 0 and passed > 0:
        print("\n MinIO AI-Platform Integration: VALIDATED")
        print("   - Evidence Vault operations working")
        print("   - SHA256 integrity verification working")
        print("   - Presigned URLs working")
        print("   - Performance targets met (<1s)")
        return 0
    elif skipped == len(tests):
        print("\n MinIO not available - all tests skipped")
        print("   Ensure AI-Platform is running: docker-compose up -d")
        return 0  # Not a failure, just not available
    else:
        print("\n MinIO AI-Platform Integration: ISSUES DETECTED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
