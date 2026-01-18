# ADR-027 Phase 3 Handover - Evidence Retention

## Overview

**Status**: ✅ COMPLETE
**Date**: 2026-01-15
**Ticket**: SDLC-ADR027-601
**Setting**: `evidence_retention_days`
**Category**: Lifecycle
**Complexity**: HIGH

## Implementation Summary

Phase 3 implements automated evidence retention management based on the `evidence_retention_days` system setting. Evidence older than the configured retention period is automatically archived (soft-deleted), and archived evidence beyond the grace period is permanently purged.

### Evidence Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Evidence Retention Lifecycle                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ACTIVE                    ARCHIVED                    PURGED          │
│   ┌─────────┐              ┌─────────┐              ┌─────────┐        │
│   │ Evidence│  Retention   │ Evidence│  Grace      │ Evidence│        │
│   │ uploaded│────expires──▶│ soft    │───period───▶│ hard    │        │
│   │ <365d   │              │ deleted │  expires    │ deleted │        │
│   └─────────┘              └─────────┘              └─────────┘        │
│                                                                         │
│   - Files in MinIO         - deleted_at set        - DB record gone    │
│   - DB record active       - Files retained        - MinIO file gone   │
│   - Fully accessible       - Recoverable           - Irreversible      │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│   Default Values:                                                       │
│   - evidence_retention_days: 365 days                                   │
│   - grace_period_days: 30 days                                          │
│   - batch_size: 100 records per transaction                             │
└─────────────────────────────────────────────────────────────────────────┘
```

## Files Created/Modified

### New Files

| File | Purpose |
|------|---------|
| `backend/app/tasks/evidence_retention.py` | EvidenceRetentionTask service with archive/purge logic |
| `backend/tests/unit/test_evidence_retention.py` | 25 unit tests for retention logic |
| `backend/tests/integration/test_adr027_phase3_integration.py` | 18 integration tests |
| `docs/04-build/07-Handover/ADR-027-PHASE-3-HANDOVER.md` | This handover document |

### Modified Files

| File | Changes |
|------|---------|
| `backend/app/api/routes/admin.py` | Added 3 new admin endpoints for retention management |

## API Endpoints Added

### GET /api/v1/admin/evidence/retention-stats
Get current evidence retention statistics.

**Response:**
```json
{
    "total_evidence": 5000,
    "active_evidence": 4800,
    "archived_evidence": 180,
    "evidence_due_for_archive": 20,
    "evidence_due_for_purge": 10,
    "oldest_evidence_date": "2024-01-15T10:30:00",
    "newest_evidence_date": "2026-01-15T08:15:00",
    "retention_days": 365,
    "grace_period_days": 30,
    "archive_cutoff_date": "2025-01-15T00:00:00",
    "purge_cutoff_date": "2025-12-16T00:00:00"
}
```

### POST /api/v1/admin/evidence/retention-archive
Manually trigger evidence archival.

**Response:**
```json
{
    "message": "Evidence archival completed",
    "archived_count": 125,
    "cutoff_date": "2025-01-15T00:00:00",
    "retention_days": 365,
    "duration_seconds": 2.5,
    "status": "success",
    "triggered_by": "admin@example.com"
}
```

### POST /api/v1/admin/evidence/retention-purge
Manually trigger evidence purge (⚠️ IRREVERSIBLE).

**Response:**
```json
{
    "message": "Evidence purge completed",
    "purged_count": 50,
    "files_deleted": 48,
    "files_failed": 2,
    "cutoff_date": "2024-12-15T00:00:00",
    "grace_period_days": 30,
    "duration_seconds": 5.2,
    "status": "success",
    "triggered_by": "admin@example.com"
}
```

## SettingsService Method

The `get_evidence_retention_days()` method was already implemented in Phase 1:

```python
async def get_evidence_retention_days(self) -> int:
    """
    Get evidence retention period in days.
    Returns: Retention period in days (default: 365)
    """
    value = await self.get("evidence_retention_days", default=365)
    try:
        return int(value)
    except (ValueError, TypeError):
        return 365
```

## Background Job Configuration

The `EvidenceRetentionTask` can be run as a scheduled cron job:

```bash
# Daily at 3:00 AM UTC (after analytics cleanup at 2:00 AM)
0 3 * * * cd /app && python -m app.tasks.evidence_retention
```

**Exit Codes:**
- `0`: Success (both archive and purge completed)
- `1`: Partial failure (one phase failed)
- `2`: Complete failure (both phases failed)

## Test Coverage

### Unit Tests (25 tests)
- `test_get_evidence_retention_days_from_database`
- `test_get_evidence_retention_days_default`
- `test_get_evidence_retention_days_invalid_value`
- `test_get_evidence_retention_days_string_parsing`
- `test_archive_old_evidence_success`
- `test_archive_old_evidence_no_records`
- `test_purge_expired_evidence_success`
- `test_purge_expired_evidence_no_records`
- `test_purge_with_file_deletion_failure`
- `test_get_retention_stats`
- `test_retention_days_zero`
- `test_very_large_retention_days`
- `test_archive_with_database_error`
- `test_purge_with_database_error`
- `test_archive_cutoff_date_calculation`
- `test_purge_cutoff_date_calculation`
- `test_run_evidence_retention_success`
- `test_evidence_without_s3_key`
- `test_archive_batching`
- `test_retention_days_cached`
- `test_retention_days_from_cache`
- ... and more

### Integration Tests (18 tests)
- Admin endpoint access control
- Full lifecycle testing
- Cross-phase integration with Phase 1 & 2 settings
- Performance benchmarks
- Audit trail verification

## ADR-027 Complete Status

| Phase | Setting | Status | Tests |
|-------|---------|--------|-------|
| Phase 1 | session_timeout_minutes | ✅ | 14 |
| Phase 1 | max_login_attempts | ✅ | 14 |
| Phase 1 | password_min_length | ✅ | 15 |
| Phase 1 | mfa_required | ✅ | 14 |
| Phase 2 | max_projects_per_user | ✅ | 12 |
| Phase 2 | max_file_size_mb | ✅ | 18 |
| Phase 2 | ai_council_enabled | ✅ | 17 |
| Phase 3 | evidence_retention_days | ✅ | 43 |
| **Total** | **8 settings** | **100%** | **147 tests** |

## Architecture Decisions

### Why Two-Phase Cleanup?

1. **Archive Phase (Soft Delete)**
   - Sets `deleted_at` timestamp
   - Files remain in MinIO
   - Recoverable if needed
   - Grace period allows review

2. **Purge Phase (Hard Delete)**
   - Removes files from MinIO
   - Deletes database records
   - Irreversible action
   - Frees storage space

### Why Batch Processing?

- Prevents long-running transactions
- Reduces memory usage
- Allows progress logging
- Enables graceful shutdown

### Why 30-Day Grace Period?

- Compliance requirements (audit trail)
- Recovery window for accidental archival
- Legal hold compatibility
- Industry standard practice

## Security Considerations

1. **Admin-Only Access**: All retention endpoints require `is_superuser=true`
2. **Audit Logging**: Every archival/purge operation is logged
3. **Irreversibility Warning**: Purge endpoint clearly warns of permanent deletion
4. **Soft Delete First**: Default workflow uses soft delete before hard delete

## Performance Characteristics

| Operation | Target | Notes |
|-----------|--------|-------|
| Stats query | <500ms | Multiple COUNT queries |
| Archive batch | <5s | 100 records per batch |
| Purge batch | <10s | Includes MinIO file deletion |
| Cron job (1M records) | <10min | Batch processing |

## Related Documentation

- [ADR-027 Full Specification](../../02-design/03-ADRs/ADR-027-System-Settings-Real-Implementation.md)
- [Phase 1 Handover](./ADR-027-PHASE-1-HANDOVER.md)
- [Phase 2 Handover](./ADR-027-PHASE-2-HANDOVER.md)
- [SettingsService Implementation](../../../backend/app/services/settings_service.py)

---

**Handover Complete**: ADR-027 Phase 3 is ready for code review and merge.

**Author**: Claude AI
**Date**: 2026-01-15
**Reviewer**: Backend Lead + CTO
