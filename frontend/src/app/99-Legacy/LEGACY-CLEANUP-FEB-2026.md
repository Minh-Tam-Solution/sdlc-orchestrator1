# Frontend Legacy Cleanup — February 2026

**Audit Date**: February 17, 2026  
**Sprint Context**: Sprint 173 Deferred Items (Phase 2.3)  
**Total LOC Removed**: 2,032 LOC

---

## Orphaned Pages Moved to 99-Legacy

### 1. Dogfooding System (1,615 LOC)
**Origin**: Sprint 114 Track 2  
**Reason**: Deferred in Sprint 173, not in sidebar navigation  
**Status**: Orphaned - no production usage

**Files Moved**:
- `dogfooding/page.tsx` (1,088 LOC) - Main dogfooding dashboard
- `dogfooding/feedback/page.tsx` (527 LOC) - Feedback submission page

**Backend APIs**: 21 endpoints (POST /api/dogfooding/feedback, etc.)  
**Deferred Item Match**: "Dogfooding pages deletion (~1,600 LOC)"

---

### 2. Duplicate Code Generation Page (417 LOC)
**Origin**: Early codegen implementation  
**Reason**: Duplicate of `/app/codegen/` page  
**Status**: Orphaned - replaced by newer implementation

**Files Moved**:
- `code-generation/page.tsx` (417 LOC) - Duplicate codegen page
- `code-generation/loading.tsx` (2,652 bytes) - Loading state

**Backend APIs**: SSE streaming codegen endpoint  
**Deferred Item Match**: "Phase 2.3: Codegen template consolidation"

**Reference Fixed**:
- `app/app-builder/page.tsx` line 131: Changed route from `/app/code-generation` → `/app/codegen`

---

## Frontend Audit Context

**Total Pages Analyzed**: 85 page.tsx files  
**Backend Endpoints**: 651 endpoints verified  
**Hidden Pages Found**: 12 pages not in sidebar

**Production Pages (Kept)**:
- `/app/sase-templates/` (841 LOC) - SASE template system
- `/app/mcp-analytics/` (557 LOC) - Sprint 150 MCP analytics
- `/app/learnings/` (627 LOC) - EP-11 learnings capture (18 endpoints)
- `/app/plan-review/` (1,167 LOC) - ADR-034 plan review system
- `/app/ceo-dashboard/` (763 LOC) - CEO insights dashboard (13 endpoints)
- `/app/planning/` (553 LOC) - Planning interface (94 endpoints)

These pages have real backend APIs and are production features — intentionally kept.

---

## Impact

- **LOC Reduced**: -2,032 LOC from active codebase
- **Directories Cleaned**: 3 orphaned routes removed
- **Routes Fixed**: 1 reference updated to correct route
- **Technical Debt**: Sprint 173 deferred items partially resolved

---

## Restoration Notes

If these pages need to be restored:
1. Move files from `99-Legacy/` back to `app/`
2. Restore route reference in `app-builder/page.tsx`
3. Verify backend endpoints still exist
4. Add to sidebar navigation

**Backend Preservation**: All backend endpoints remain active for potential future use.

---

**Audit Report**: Frontend Audit Results (Feb 17, 2026)  
**Cleanup Executed**: CTO Review Session  
**Framework**: SDLC 6.0.6
