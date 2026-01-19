"""
=========================================================================
Evidence Manifest API Router - Tamper-Evident Hash Chain (Sprint 82)
SDLC Orchestrator - Stage 04 (BUILD)

Version: 1.0.0
Date: January 19, 2026
Status: ACTIVE - Sprint 82 (Pre-Launch Hardening)
Authority: CTO + Security Lead Approved
Foundation: SPRINT-82-HARDENING-EVIDENCE.md, Pre-Launch Hardening Plan
Framework: SDLC 5.1.3 (7-Pillar Architecture)

Purpose:
- Tamper-evident manifest management for Evidence Vault
- Hash chain verification API
- Verification history and chain status
- GDPR-compliant anonymization (future)

API Endpoints (7):
1. POST /evidence-manifests - Create new manifest (with hash chain linking)
2. GET /evidence-manifests - List manifests for project
3. GET /evidence-manifests/{id} - Get manifest by ID
4. GET /evidence-manifests/latest - Get latest manifest for project
5. POST /evidence-manifests/verify - Verify hash chain integrity
6. GET /evidence-manifests/status - Get chain status summary
7. GET /evidence-manifests/verifications - Get verification history

Go/No-Go Criteria (Feb 28, 2026):
- Evidence hash chain: Tamper-evident test pass ✅

Zero Mock Policy: 100% COMPLIANCE (real Ed25519 + database)
=========================================================================
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.services.evidence_manifest_service import (
    evidence_manifest_db_service,
    ManifestVerificationResult,
)

router = APIRouter()


# ============================================================================
# Request/Response Schemas
# ============================================================================


class ArtifactInput(BaseModel):
    """Input schema for artifact entry."""
    artifact_id: Optional[UUID] = None
    file_path: str
    sha256_hash: str
    size_bytes: int = 0
    content_type: str = "application/octet-stream"
    uploaded_at: Optional[datetime] = None
    uploaded_by: Optional[UUID] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class CreateManifestRequest(BaseModel):
    """Request to create a new evidence manifest."""
    project_id: UUID
    artifacts: list[ArtifactInput] = Field(default_factory=list)


class ManifestResponse(BaseModel):
    """Response schema for evidence manifest."""
    id: UUID
    project_id: UUID
    sequence_number: int
    manifest_hash: str
    previous_manifest_hash: Optional[str] = None
    artifacts: list[dict[str, Any]]
    signature: str
    is_genesis: bool
    created_at: datetime
    created_by: Optional[UUID] = None
    artifact_count: int
    total_size_bytes: int

    class Config:
        from_attributes = True


class ManifestListResponse(BaseModel):
    """Response for manifest list."""
    total: int
    manifests: list[ManifestResponse]


class VerifyChainRequest(BaseModel):
    """Request to verify hash chain."""
    project_id: UUID
    verified_by: str = "api-request"


class VerifyChainResponse(BaseModel):
    """Response for chain verification."""
    is_valid: bool
    manifest_id: UUID
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    verified_at: datetime
    manifests_checked: int = 0


class ChainStatusResponse(BaseModel):
    """Response for chain status summary."""
    project_id: str
    total_manifests: int
    latest_sequence: int
    latest_manifest_hash: Optional[str] = None
    latest_manifest_at: Optional[str] = None
    last_verification_valid: Optional[bool] = None
    last_verified_at: Optional[str] = None
    last_verified_by: Optional[str] = None


class VerificationHistoryItem(BaseModel):
    """Single verification history item."""
    id: UUID
    project_id: UUID
    verified_at: datetime
    manifests_checked: int
    chain_valid: bool
    first_broken_at: Optional[UUID] = None
    error_message: Optional[str] = None
    verified_by: str

    class Config:
        from_attributes = True


class VerificationHistoryResponse(BaseModel):
    """Response for verification history."""
    total: int
    verifications: list[VerificationHistoryItem]


# ============================================================================
# Helper Functions
# ============================================================================


def manifest_to_response(manifest) -> ManifestResponse:
    """Convert SQLAlchemy manifest to response schema."""
    return ManifestResponse(
        id=manifest.id,
        project_id=manifest.project_id,
        sequence_number=manifest.sequence_number,
        manifest_hash=manifest.manifest_hash,
        previous_manifest_hash=manifest.previous_manifest_hash,
        artifacts=manifest.artifacts or [],
        signature=manifest.signature,
        is_genesis=manifest.is_genesis,
        created_at=manifest.created_at,
        created_by=manifest.created_by,
        artifact_count=manifest.artifact_count,
        total_size_bytes=manifest.total_size_bytes,
    )


# ============================================================================
# Manifest Endpoints
# ============================================================================


@router.post(
    "/evidence-manifests",
    response_model=ManifestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create evidence manifest",
    description="""
    Create a new evidence manifest with hash chain linking (Sprint 82 P0).

    **Hash Chain Design**:
    - Each manifest's `manifest_hash` = SHA256(content)
    - Each manifest's `previous_manifest_hash` = previous manifest's hash
    - Genesis manifests have `previous_manifest_hash = null`
    - Chain forms linked list: M1 → M2 → M3 → ...

    **Ed25519 Signing**:
    - Manifests are signed with Ed25519 private key
    - Non-repudiation: Only server can sign, anyone can verify
    - Signature stored in `signature` field

    **Request**:
    - `project_id`: Project UUID
    - `artifacts`: List of artifact entries to include

    **Response** (201 Created):
    - Complete manifest with hash, signature, sequence number
    - `is_genesis = true` if first manifest for project
    """,
)
async def create_manifest(
    request: CreateManifestRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ManifestResponse:
    """Create new evidence manifest with hash chain linking."""
    # Convert artifacts to dict format
    artifacts = [
        {
            "artifact_id": str(a.artifact_id) if a.artifact_id else None,
            "file_path": a.file_path,
            "sha256_hash": a.sha256_hash,
            "size_bytes": a.size_bytes,
            "content_type": a.content_type,
            "uploaded_at": a.uploaded_at,
            "uploaded_by": str(a.uploaded_by) if a.uploaded_by else None,
            "metadata": a.metadata,
        }
        for a in request.artifacts
    ]

    manifest = await evidence_manifest_db_service.create_manifest(
        db=db,
        project_id=request.project_id,
        artifacts=artifacts,
        created_by=current_user.id,
    )

    return manifest_to_response(manifest)


@router.get(
    "/evidence-manifests",
    response_model=ManifestListResponse,
    summary="List evidence manifests",
    description="""
    List all evidence manifests for a project, ordered by sequence number.

    **Pagination**:
    - `limit`: Max results (default 100, max 1000)
    - `offset`: Offset for pagination

    **Response**:
    - `total`: Total manifests for project
    - `manifests`: List of manifest objects
    """,
)
async def list_manifests(
    project_id: UUID = Query(..., description="Project UUID to list manifests for"),
    limit: int = Query(100, ge=1, le=1000, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ManifestListResponse:
    """List all evidence manifests for a project."""
    manifests = await evidence_manifest_db_service.get_project_manifests(
        db=db,
        project_id=project_id,
        limit=limit,
        offset=offset,
    )

    # Get total count
    from sqlalchemy import select, func
    from app.models.evidence_manifest import EvidenceManifest as DBManifest

    count_query = select(func.count(DBManifest.id)).where(
        DBManifest.project_id == project_id
    )
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    return ManifestListResponse(
        total=total,
        manifests=[manifest_to_response(m) for m in manifests],
    )


@router.get(
    "/evidence-manifests/latest",
    response_model=Optional[ManifestResponse],
    summary="Get latest manifest",
    description="""
    Get the latest (highest sequence number) manifest for a project.

    Returns null if no manifests exist for the project.
    """,
)
async def get_latest_manifest(
    project_id: UUID = Query(..., description="Project UUID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Optional[ManifestResponse]:
    """Get the latest manifest for a project."""
    manifest = await evidence_manifest_db_service.get_latest_manifest(
        db=db,
        project_id=project_id,
    )

    if not manifest:
        return None

    return manifest_to_response(manifest)


@router.get(
    "/evidence-manifests/status",
    response_model=ChainStatusResponse,
    summary="Get chain status",
    description="""
    Get chain status summary for a project.

    **Response includes**:
    - Total manifest count
    - Latest sequence number
    - Latest manifest hash
    - Last verification result (if any)
    """,
)
async def get_chain_status(
    project_id: UUID = Query(..., description="Project UUID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ChainStatusResponse:
    """Get chain status summary."""
    status = await evidence_manifest_db_service.get_chain_status(
        db=db,
        project_id=project_id,
    )

    return ChainStatusResponse(**status)


@router.get(
    "/evidence-manifests/{manifest_id}",
    response_model=ManifestResponse,
    summary="Get manifest by ID",
    description="Get a specific evidence manifest by its UUID.",
)
async def get_manifest(
    manifest_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ManifestResponse:
    """Get manifest by ID."""
    manifest = await evidence_manifest_db_service.get_manifest(
        db=db,
        manifest_id=manifest_id,
    )

    if not manifest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manifest {manifest_id} not found",
        )

    return manifest_to_response(manifest)


@router.post(
    "/evidence-manifests/verify",
    response_model=VerifyChainResponse,
    summary="Verify hash chain",
    description="""
    Verify the integrity of the entire hash chain for a project (Sprint 82 P0).

    **Verification Steps**:
    1. Load all manifests ordered by sequence
    2. Verify each manifest's hash matches content
    3. Verify each manifest's `previous_manifest_hash` matches prior manifest
    4. Verify Ed25519 signatures (if keys available)
    5. Check for sequence gaps

    **Result**:
    - `is_valid = true`: All checks passed
    - `is_valid = false`: Chain integrity broken (tampering detected)

    **Audit**:
    - Each verification is logged to `evidence_manifest_verifications`
    - Results available via GET /evidence-manifests/verifications
    """,
)
async def verify_chain(
    request: VerifyChainRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> VerifyChainResponse:
    """Verify hash chain integrity for a project."""
    # Use user ID as verified_by if not specified
    verified_by = request.verified_by
    if verified_by == "api-request":
        verified_by = f"user-{current_user.id}"

    result = await evidence_manifest_db_service.verify_project_chain(
        db=db,
        project_id=request.project_id,
        verified_by=verified_by,
    )

    # Get manifest count for response
    from sqlalchemy import select, func
    from app.models.evidence_manifest import EvidenceManifest as DBManifest

    count_query = select(func.count(DBManifest.id)).where(
        DBManifest.project_id == request.project_id
    )
    count_result = await db.execute(count_query)
    manifests_checked = count_result.scalar() or 0

    return VerifyChainResponse(
        is_valid=result.is_valid,
        manifest_id=result.manifest_id,
        errors=result.errors,
        warnings=result.warnings,
        verified_at=result.verified_at,
        manifests_checked=manifests_checked,
    )


@router.get(
    "/evidence-manifests/verifications",
    response_model=VerificationHistoryResponse,
    summary="Get verification history",
    description="""
    Get verification history for a project.

    Shows all past chain verification runs, including:
    - Verification timestamp
    - Result (valid/invalid)
    - Error details (if invalid)
    - Who/what triggered verification
    """,
)
async def get_verification_history(
    project_id: UUID = Query(..., description="Project UUID"),
    limit: int = Query(10, ge=1, le=100, description="Max results"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> VerificationHistoryResponse:
    """Get verification history for a project."""
    verifications = await evidence_manifest_db_service.get_verification_history(
        db=db,
        project_id=project_id,
        limit=limit,
    )

    return VerificationHistoryResponse(
        total=len(verifications),
        verifications=[
            VerificationHistoryItem(
                id=v.id,
                project_id=v.project_id,
                verified_at=v.verified_at,
                manifests_checked=v.manifests_checked,
                chain_valid=v.chain_valid,
                first_broken_at=v.first_broken_at,
                error_message=v.error_message,
                verified_by=v.verified_by,
            )
            for v in verifications
        ],
    )
