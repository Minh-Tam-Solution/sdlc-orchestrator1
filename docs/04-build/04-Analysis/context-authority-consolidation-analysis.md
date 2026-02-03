# Context Authority V1/V2 Consolidation Analysis

**Sprint**: S149 - V2 API Finalization
**Date**: February 18, 2026
**Status**: ✅ AUDIT COMPLETE

---

## Executive Summary

Context Authority has **V1** and **V2** implementations with an inheritance relationship:
- V2 **extends** V1 (not replaces)
- V1 service classes are used by V2
- V1 **routes** are deprecated (sunset: March 6, 2026)

**Recommendation**: Keep V1 service as base class, complete V1 route deprecation.

---

## Architecture Analysis

### V1: `context_authority.py` (876 LOC)
```
Provides:
- ContextAuthorityEngineV1 (base engine)
- ContextValidationResult (result type)
- ContextViolation, ContextViolationType
- ViolationSeverity, CodeSubmission

Used by:
- V2 service (inherits from V1)
- V1 routes (deprecated)
- V2 routes (imports V1 types)
- gates_engine.py (via schema)
- gates_ca_integration.py (via schema)
```

### V2: `context_authority_v2.py` (956 LOC)
```
Provides:
- ContextAuthorityEngineV2 (extends V1)
- Gate-aware validation
- Vibecoding Index awareness
- Dynamic AGENTS.md overlay
- Context snapshots

Imports from V1:
- ContextAuthorityEngineV1
- ContextValidationResult
- ContextViolation
- ContextViolationType
- ViolationSeverity
- CodeSubmission
```

### Relationship Diagram

```
┌─────────────────────────────────────┐
│        context_authority.py         │
│              (V1 Service)           │
├─────────────────────────────────────┤
│ - ContextAuthorityEngineV1          │
│ - ContextValidationResult           │
│ - ContextViolation types            │
│ - Base validation logic             │
└─────────────────┬───────────────────┘
                  │ inherits/extends
                  ▼
┌─────────────────────────────────────┐
│      context_authority_v2.py        │
│              (V2 Service)           │
├─────────────────────────────────────┤
│ - ContextAuthorityEngineV2          │
│ - Gate-aware validation             │
│ - Vibecoding Index routing          │
│ - Dynamic overlays                  │
│ - Audit snapshots                   │
└─────────────────────────────────────┘
```

---

## API Route Analysis

### V1 Routes (`/context-authority/`)
**Status**: ⚠️ DEPRECATED (Sunset: March 6, 2026)

| Endpoint | Status | Migration |
|----------|--------|-----------|
| `POST /validate` | Deprecated | → `/v2/validate` |
| `GET /adrs/{project_id}` | Deprecated | → `/v2/adrs/{project_id}` |
| `GET /modules/{project_id}` | Deprecated | → `/v2/modules/{project_id}` |
| `POST /batch-validate` | Deprecated | → `/v2/batch-validate` |
| `POST /check-freshness` | Deprecated | → `/v2/check-freshness` |
| `GET /stats/{project_id}` | Deprecated | → `/v2/stats/{project_id}` |
| `GET /compliance/{project_id}` | Deprecated | → `/v2/compliance/{project_id}` |

**Total V1 Endpoints**: 7 (all deprecated)

### V2 Routes (`/context-authority/v2/`)
**Status**: ✅ ACTIVE

| Endpoint | Description |
|----------|-------------|
| `POST /validate` | Gate-aware context validation |
| `GET /gates/{project_id}` | Get gate context overlays |
| `POST /overlay/generate` | Generate dynamic AGENTS.md overlay |
| `GET /snapshots/{project_id}` | Get context snapshots |
| `POST /snapshots` | Create context snapshot |
| + V1 equivalents | All V1 endpoints with V2 enhancements |

---

## Consolidation Strategy

### ❌ Cannot Delete V1 Service

V2 depends on V1:
```python
# context_authority_v2.py
from app.services.governance.context_authority import (
    ContextAuthorityEngineV1,
    ContextValidationResult,
    ContextViolation,
    ...
)
```

### ✅ Can Delete V1 Routes (After Sunset)

V1 routes file can be removed after March 6, 2026:
- Current: Both `/context-authority/` and `/context-authority/v2/` active
- After sunset: Only `/context-authority/v2/` remains

### Recommended Actions

1. **Now (Sprint 149)**:
   - ✅ V1 routes already deprecated with headers
   - ✅ Deprecation documented in Sprint 147
   - ⏳ Monitor V1 usage via telemetry

2. **Sprint 153+ (After March 6, 2026)**:
   - Delete V1 route file: `backend/app/api/routes/context_authority.py`
   - Update router registration in `main.py`
   - Update API documentation

3. **Keep Forever**:
   - V1 service (`context_authority.py`) - V2 depends on it
   - Rename to `context_authority_base.py` if desired for clarity

---

## Metrics

| Metric | Value |
|--------|-------|
| V1 Service LOC | 876 |
| V2 Service LOC | 956 |
| V1 Endpoints | 7 (deprecated) |
| V2 Endpoints | 12+ |
| V1 Usage (last 30 days) | TBD (check telemetry) |
| V2 Usage (last 30 days) | TBD (check telemetry) |

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Deleting V1 service breaks V2 | HIGH | N/A | **DO NOT DELETE** - V2 depends on V1 |
| V1 routes used after sunset | LOW | LOW | Telemetry monitoring + docs |
| Clients not migrated | MEDIUM | MEDIUM | Deprecation headers + migration guide |

---

## Conclusion

**V1 Service**: KEEP (V2 dependency)
**V1 Routes**: DELETE after March 6, 2026

**Sprint 149 Actions**:
1. ✅ Audit complete
2. Verify deprecation headers working
3. Monitor V1 usage via telemetry
4. No code changes needed this sprint

**Future Actions** (Sprint 153+):
1. Delete V1 route file
2. Update API documentation
3. Consider renaming V1 service to `context_authority_base.py`

---

**Report Complete**: February 18, 2026
