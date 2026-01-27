"""
Infrastructure Services Layer - Sprint 111

AGPL-Safe Network-Only Access Pattern:
- MinIO: S3 API via HTTP/S (no minio SDK)
- OPA: REST API via HTTP/S (no opa SDK)
- Redis: redis-py (BSD license, safe)
- GitHub: REST API via HTTP/S
- Notifications: Slack webhook, SMTP

All AGPL components (MinIO, Grafana) accessed via network only.
"""

from .minio_service import (
    MinioService,
    MinioError,
    BucketNotFoundError,
    ObjectNotFoundError,
    UploadError,
    DownloadError,
)

__all__ = [
    # MinIO Service
    "MinioService",
    "MinioError",
    "BucketNotFoundError",
    "ObjectNotFoundError",
    "UploadError",
    "DownloadError",
]
