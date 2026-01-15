# ADR-027 Phase 2 - Handover Document

**Date**: January 15, 2026
**Status**: IN PROGRESS
**Author**: Claude Opus 4.5 (AI Assistant)
**Reviewer**: Backend Lead, CTO

---

## Executive Summary

Phase 2 implements **3 resource limit settings** from ADR-027:

| Setting | Purpose | Status |
|---------|---------|--------|
| `max_projects_per_user` | Limit project ownership per user | ✅ Implemented |
| `max_file_size_mb` | Evidence upload size limit | ✅ Implemented |
| `ai_council_enabled` | Feature flag for AI Council | ✅ Implemented |

---

## Implementation Details

### 1. max_projects_per_user

**Files Modified**:
- `backend/app/api/routes/projects.py` - Added limit check in `create_project` and `init_project`

**Logic**:
```python
# Count user's owned projects (excluding deleted)
owned_count = count(Project.id).where(
    Project.owner_id == current_user.id,
    Project.deleted_at.is_(None),
)

if owned_count >= max_projects:
    raise HTTPException(400, "Project limit reached...")
```

**Behavior**:
- Default limit: 50 projects per user
- Deleted projects don't count toward limit
- Admin can adjust via Admin Panel → System Settings

**Error Response**:
```json
{
  "detail": "Project limit reached. You own 50 projects (max: 50). Delete existing projects or contact admin to increase limit."
}
```

---

### 2. max_file_size_mb

**Files Modified**:
- `backend/app/api/routes/evidence.py` - Dynamic file size validation

**Logic**:
```python
# Get limit from database (cached)
max_file_size_mb = await settings_service.get_max_file_size_mb()
max_size_bytes = max_file_size_mb * 1024 * 1024

if file_size > max_size_bytes:
    raise HTTPException(413, "File size exceeds maximum...")
```

**Behavior**:
- Default limit: 100 MB
- Returns HTTP 413 (Request Entity Too Large) on violation
- Shows file size and limit in error message

**Error Response**:
```json
{
  "detail": "File size 150.00MB exceeds maximum 100MB. Contact admin to adjust file size limit."
}
```

---

### 3. ai_council_enabled

**Files Modified**:
- `backend/app/api/routes/council.py` - Feature flag check before deliberation

**Logic**:
```python
if not await settings_service.is_ai_council_enabled():
    raise HTTPException(503, "AI Council is currently disabled...")
```

**Behavior**:
- Default: True (enabled)
- When disabled: All council endpoints return 503 Service Unavailable
- Toggle takes effect immediately (after cache refresh)

**Error Response**:
```json
{
  "detail": "AI Council is currently disabled. Contact admin to enable this feature."
}
```

---

## SettingsService Accessors

The `SettingsService` class already had these accessors prepared in Phase 1:

```python
# backend/app/services/settings_service.py

async def get_max_projects_per_user(self) -> int:
    """Returns max projects limit (default: 50)"""

async def get_max_file_size_mb(self) -> int:
    """Returns max file size in MB (default: 100)"""

async def is_ai_council_enabled(self) -> bool:
    """Returns True if AI Council is enabled"""
```

All accessors:
- Cache values in Redis (5-min TTL)
- Return type-safe defaults on error
- Log warnings for invalid values

---

## Test Coverage

### Unit Tests

| File | Tests | Status |
|------|-------|--------|
| `test_max_projects_per_user.py` | 12 | ✅ Created |
| `test_max_file_size.py` | 18 | ✅ Created |
| `test_ai_council_enabled.py` | 17 | ✅ Created |

**Total**: 47 unit tests

### Integration Tests

| File | Tests | Status |
|------|-------|--------|
| `test_adr027_phase2_integration.py` | 18 | ✅ Created |

---

## Files Changed

### Modified
1. `backend/app/api/routes/projects.py`
   - Added `SettingsService` import
   - Added limit check in `create_project` (line 135-153)
   - Added limit check in `init_project` (line 641-658)

2. `backend/app/api/routes/evidence.py`
   - Added `SettingsService` import
   - Dynamic file size check (line 143-153)

3. `backend/app/api/routes/council.py`
   - Added `SettingsService` import
   - Feature flag check (line 282-288)

### Created
1. `backend/tests/unit/test_max_projects_per_user.py`
2. `backend/tests/unit/test_max_file_size.py`
3. `backend/tests/unit/test_ai_council_enabled.py`
4. `backend/tests/integration/test_adr027_phase2_integration.py`
5. `docs/04-build/07-Handover/ADR-027-PHASE-2-HANDOVER.md` (this file)

---

## Acceptance Criteria

| Criteria | Status |
|----------|--------|
| ✅ User at project limit gets 400 error with clear message | ✅ |
| ✅ File exceeding limit gets 413 error | ✅ |
| ✅ AI Council disabled returns 503 | ✅ |
| ✅ Settings read from database (not hardcoded) | ✅ |
| ✅ Settings cached in Redis | ✅ |
| ✅ Admin can change settings via Admin Panel | ✅ (existing UI) |

---

## Deployment Notes

### No Database Migration Required
- All 3 settings already exist in `system_settings` table
- `SettingsService` handles missing settings with defaults

### Cache Considerations
- Settings cached for 5 minutes
- Cache auto-invalidates on Admin Panel update
- Manual invalidation: `POST /api/v1/admin/settings/invalidate-cache`

### Rollback
- To disable enforcement: Set settings to permissive values
  - `max_projects_per_user`: 10000
  - `max_file_size_mb`: 10000
  - `ai_council_enabled`: true

---

## Next Steps

### Phase 3: Lifecycle & Advanced (Week 5-6)
- `evidence_retention_days` - Background job for evidence archival

---

## Sign-off

| Role | Name | Approval |
|------|------|----------|
| AI Assistant | Claude Opus 4.5 | ✅ Implemented |
| Backend Lead | | ☐ Pending |
| CTO | | ☐ Pending |

---

**Phase 2 Status**: Ready for Code Review
