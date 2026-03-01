# Sprint 214 — GDPR/Data Residency UI + Compliance Dashboard + Extension Commands

**Sprint Duration**: Feb 28, 2026
**Sprint Goal**: Complete ENT checklist (12/12), push cross-interface coverage to 86%, enable compliance dashboard
**Status**: PLANNED
**Priority**: P0 (ENT compliance 88% → 91%)
**Framework**: SDLC 6.1.1
**Previous Sprint**: [Sprint 213 — Frontend Test Coverage Push + Extension Gate Create](SPRINT-213-FRONTEND-TEST-PUSH-EXTENSION-GATE.md)

---

## Context

Sprint 213 achieved 88% ENT compliance with 11/12 checklist items done. Two items remain:
- **Item #10**: GDPR/Data Residency UI — backend fully implemented (Sprint 186-187), zero frontend
- **Item #4**: Compliance Dashboard — `FF_COMPLIANCE=false`, dead NIST link in overview page

Cross-interface coverage is at 81%. Extension is missing Export Audit and Close Sprint commands.

---

## Sprint Summary

| Track | Scope | Est. LOC | Impact |
|-------|-------|----------|--------|
| A | GDPR frontend (page + hook) + Data Residency frontend (page + hook) | ~400 | ENT checklist #10 → DONE |
| B | Compliance dashboard enablement: fix dead links, add GDPR/DR, FF_COMPLIANCE=true, Sidebar | ~120 | ENT checklist #4 → DONE |
| C | Extension: exportAuditCommand + closeSprintCommand + 2 apiClient methods | ~250 | Cross-interface 81% → 86% |
| D | Backend + frontend tests | ~200 | Regression safety |
| **Total** | | **~970 LOC** | **88% → 91% ENT** |

---

## Track A — GDPR/Data Residency Frontend

### A1: useGdpr.ts hook
- TanStack Query hooks for 7 GDPR endpoints
- Key factory: `gdprKeys.dsarList()`, `gdprKeys.dataExport()`, `gdprKeys.consents()`
- Mutations: `useCreateDsar()`, `useRecordConsent()`

### A2: GDPR page (app/app/gdpr/page.tsx)
- LockedFeature with `requiredTier="ENTERPRISE"`
- 3 sections: DSAR Requests table, Data Export card, Consent Management
- Submit DSAR form (type selector + email + description)
- Data export summary with "Full Export" button (24h rate limit note)

### A3: useDataResidency.ts hook
- TanStack Query hooks for 4 Data Residency endpoints
- Key factory: `dataResidencyKeys.regions()`, `dataResidencyKeys.projectRegion(id)`
- Mutation: `useUpdateProjectRegion()`

### A4: Data Residency page (app/app/data-residency/page.tsx)
- LockedFeature with `requiredTier="ENTERPRISE"`
- Regions list with GDPR compliance badge
- Per-project region selector with confirmation dialog
- Storage routing info display

---

## Track B — Compliance Dashboard Enablement

### B1: Fix compliance overview page
- Remove dead NIST AI RMF link (backend removed Sprint 190)
- Add GDPR Dashboard card (link to /app/gdpr)
- Add Data Residency card (link to /app/data-residency)
- Keep EU AI Act and ISO 42001 as "coming_soon"

### B2: Sidebar update
- Add GDPR and Data Residency nav items under compliance flagGroup
- Gate both to `FF_COMPLIANCE` flag

### B3: Enable FF_COMPLIANCE
- Set `NEXT_PUBLIC_FF_COMPLIANCE=true` in `.env.example` default

---

## Track C — Extension Cross-Interface Commands

### C1: exportAuditCommand.ts
- Multi-step wizard: project → format (CSV/PDF) → progress → save dialog
- Calls `GET /evidence/export?format=csv|pdf&project_id=UUID`
- Handles binary response (StreamingResponse) → save to file

### C2: closeSprintCommand.ts
- Multi-step wizard: project → sprint select → summary → confirm → close
- Calls sprint close endpoint via apiClient
- Refreshes gate views after close

### C3: apiClient.ts additions
- `exportAuditLog(projectId, format)` — GET with responseType arraybuffer
- `getProjectSprints(projectId)` — GET sprints list
- `closeSprint(projectId, sprintId)` — POST sprint gate close

### C4: extension.ts registration
- Import and register both new commands

---

## Track D — Tests + Regression

### D1: test_sprint214_gdpr_ui.py (backend)
- File existence checks for all new files
- Content validation for key patterns
- Sidebar GDPR/DR entries check
- FF_COMPLIANCE=true in .env.example

### D2: Frontend hook tests (optional — hooks are thin wrappers)
- Validate hooks export correct key factories

### D3: Combined Sprint 209-214 regression
- All sprint tests pass together

---

## Definition of Done

- [ ] GDPR page renders with DSAR table + Data Export + Consent sections
- [ ] Data Residency page renders with region list + project region selector
- [ ] Compliance overview links to GDPR + Data Residency (not dead NIST)
- [ ] FF_COMPLIANCE=true in .env.example
- [ ] Sidebar shows GDPR + Data Residency under compliance flag
- [ ] Extension: sdlc.exportAudit registered and functional
- [ ] Extension: sdlc.closeSprint registered and functional
- [ ] All Sprint 214 tests passing
- [ ] Combined Sprint 209-214 tests passing
- [ ] CURRENT-SPRINT.md updated

---

## ENT Compliance Projection

| Metric | Before (S213) | After (S214) |
|--------|---------------|--------------|
| ENT Checklist | 10/12 (83%) | **12/12 (100%)** |
| Cross-Interface Coverage | 81% | **86%** |
| Frontend Tests | 140/147 | 140+/147 |
| Overall ENT Score | 88% | **91%** |
