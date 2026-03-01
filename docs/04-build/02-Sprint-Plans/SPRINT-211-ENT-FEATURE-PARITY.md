# Sprint 211 — ENT Feature Parity (MFA + Granular Feature Flags + DORA)

**Sprint Duration**: 5 working days
**Sprint Goal**: Close 8 P1 gaps from CTO-RPT-209-001 — MFA enrollment, granular feature flags, DORA metrics dashboard, audit export, multi-channel fallback
**Status**: PLANNED
**Priority**: P1 (ENT compliance gaps)
**Framework**: SDLC 6.1.1
**Previous Sprint**: [Sprint 210 — P0 ENT Critical Fixes](SPRINT-210-P0-ENT-CRITICAL-FIXES.md)
**CTO Report**: [CTO-RPT-209-001](../../09-govern/01-CTO-Reports/CTO-REPORT-Sprint209-ENT-Compliance-Audit.md)
**ENT Compliance Target**: 68% → 78%

---

## Sprint 211 Goal

Sprint 210 fixed the 5 P0 blockers. Sprint 211 addresses 8 P1 gaps to bring ENT compliance from 68% to 78%:

1. **P0-4**: Replace binary feature flag with granular per-module flags (Sidebar)
2. **P1-2**: MFA TOTP enrollment API + frontend UI
3. **P1-6**: DORA Metrics dashboard (Recharts)
4. **P1-7**: PDF/CSV audit export for evidence + compliance
5. **P1-8**: ConversationFirstFallback multi-channel support
6. **P1-5** (cont.): Gate approval parity — add to CLI and Extension actions
7. **P1-4**: STM-056 status upgrade (PROPOSED → APPROVED)
8. **P1-1** (partial): FR gap audit (FR-010 to FR-035 mapping)

---

## Track A — P0-4: Granular Feature Flags (Replace Binary Toggle)

**Problem**: Single `NEXT_PUBLIC_FEATURE_FLAG_LEGACY_DASHBOARD` hides ~14 non-core pages (Context Authority, VCR, CRP, MRP, SASE Templates, AGENTS.md, CLI Tokens, Check Runs, Hash Chain, App Builder, CEO Dashboard, MCP Analytics, Planning, Plan Review). ENT customers need compliance, planning, CEO dashboard visible.

> **PM Correction 1**: Page count is ~14 (not 22). 9 core admin pages are always visible.

**Solution**: Replace binary flag with per-module env vars. ENT tier enables all by default.

**Modified file**: `frontend/src/components/dashboard/Sidebar.tsx`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| A1 | Define 6 granular feature flags (env vars) | ~15 | |
| A2 | Tag each sidebar item with its flag group | ~20 | |
| A3 | Filter logic: check per-module flag instead of single binary | ~15 | |
| A4 | `.env.example` update with all flags documented | ~10 | |

**Feature flag mapping**:
```typescript
// 6 granular flags (replace single LEGACY_DASHBOARD)
NEXT_PUBLIC_FF_COMPLIANCE     // NIST, Compliance pages
NEXT_PUBLIC_FF_PLANNING       // Planning, Roadmaps, Phases, Sprints, Backlog
NEXT_PUBLIC_FF_CEO_DASHBOARD  // CEO Dashboard, MCP Analytics
NEXT_PUBLIC_FF_SASE           // VCR, CRP, MRP, SASE Templates, AGENTS.md
NEXT_PUBLIC_FF_GOVERNANCE     // Governance Mode, Context Authority, Stage Gating
NEXT_PUBLIC_FF_DEVTOOLS       // CLI Tokens, Check Runs, Hash Chain, Plan Review
```

**ENT tier**: All flags = `true` by default. LITE/STANDARD: subset enabled.

**Estimated LOC**: ~60

---

## Track B — P1-2: MFA TOTP Enrollment

**Existing state**: `mfa_middleware.py` exists (Sprint 195, 980+ LOC, production-ready), User model has `mfa_enabled`, `mfa_secret`, `backup_codes`, `mfa_setup_deadline` fields. MFA middleware already lists `/api/v1/auth/mfa/setup` and `/api/v1/auth/mfa/verify` as exempt paths. Some MFA-related code exists in `admin.py` and `organizations.py`. **Missing**: dedicated enrollment endpoints + frontend UI.

> **PM Correction 3**: MFA routes partially exist. Verify whether to extend `admin.py`/`organizations.py` or create dedicated `mfa.py`. MFA middleware (BaseHTTPMiddleware subclass) should be considered for pure ASGI conversion to avoid FastAPI 0.100+ hang bug.

### B1 — Backend: TOTP Enrollment API

**New file**: `backend/app/api/routes/mfa.py` (or extend existing routes if sufficient)

| ID | Item | LOC | Status |
|----|------|-----|--------|
| B1a | `POST /api/v1/auth/mfa/setup` — generate TOTP secret, return QR code URI + backup codes | ~40 | |
| B1b | `POST /api/v1/auth/mfa/verify` — verify TOTP code, enable MFA, store hashed secret | ~35 | |
| B1c | `POST /api/v1/auth/mfa/disable` — admin-only, disable MFA for user | ~20 | |
| B1d | `GET /api/v1/auth/mfa/status` — return MFA enabled, setup deadline, grace period remaining | ~15 | |
| B1e | Register routes in `main.py` | ~3 | |

**Dependencies**: `pyotp` (MIT, already in `requirements/core.txt` as `pyotp==2.9.0`) and `qrcode` (MIT, already in `requirements/core.txt` as `qrcode==8.2`). No new packages needed.

> **PM Correction 2**: Both pyotp and qrcode already installed — no requirements.txt changes needed.

### B2 — Frontend: MFA Setup Page

**New file**: `frontend/src/app/auth/mfa/page.tsx`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| B2a | MFA setup wizard: QR code display + 6-digit code input | ~80 | |
| B2b | Backup codes display (one-time view, print/download option) | ~30 | |
| B2c | MFA status indicator in user profile/settings | ~20 | |
| B2d | Grace period banner ("MFA required by {deadline}") | ~15 | |

### B3 — Tests

| ID | Item | LOC | Status |
|----|------|-----|--------|
| B3a | Setup: generates valid TOTP secret + QR URI | ~20 | |
| B3b | Verify: correct code enables MFA | ~20 | |
| B3c | Verify: wrong code returns 400 | ~10 | |
| B3d | Disable: admin can disable, non-admin cannot | ~15 | |
| B3e | Status: returns correct grace period | ~10 | |

**Estimated LOC**: ~113 (backend) + ~145 (frontend) + ~75 (tests) = **~333 LOC**

---

## Track C — P1-6: DORA Metrics Dashboard

**Problem**: ENT tier expects DORA metrics (Deployment Frequency, Lead Time, MTTR, Change Failure Rate). No visualization exists.

**Existing baseline**: A test fixture references `/api/v1/analytics/dora` with `deployment_frequency` field, indicating minimal DORA infrastructure may exist. Track C builds on top of any existing baseline.

> **PM Correction 4**: Existing DORA baseline should be audited before implementation. Track C extends or replaces as needed.

**Solution**: New dashboard page with Recharts (already in deps) pulling from existing data.

### C1 — Backend: DORA Aggregation Endpoint

**New file**: `backend/app/api/routes/dora.py`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| C1a | `GET /api/v1/dora/metrics?project_id=X&period=30d` — aggregate from gates, evidence, deployments | ~60 | |
| C1b | Metrics: deployment_frequency, lead_time_hours, mttr_hours, change_failure_rate | ~30 | |
| C1c | Register route in `main.py`, add to `tier_gate.py` ROUTE_TIER_TABLE (tier STANDARD=2) | ~5 | |

### C2 — Frontend: DORA Dashboard Page

**New file**: `frontend/src/app/app/dora/page.tsx`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| C2a | 4 metric cards (DF, LT, MTTR, CFR) with trend indicators | ~60 | |
| C2b | Recharts line chart: 30-day trend for each metric | ~50 | |
| C2c | Period selector (7d, 30d, 90d) | ~15 | |
| C2d | DORA rating badges (Elite, High, Medium, Low) per metric | ~20 | |
| C2e | Add to sidebar under `NEXT_PUBLIC_FF_CEO_DASHBOARD` flag group | ~3 | |

### C3 — Tests

| ID | Item | LOC | Status |
|----|------|-----|--------|
| C3a | DORA endpoint returns 4 metrics for project with gate history | ~25 | |
| C3b | Empty project returns zero metrics (no errors) | ~10 | |

**Estimated LOC**: ~95 (backend) + ~148 (frontend) + ~35 (tests) = **~278 LOC**

---

## Track D — P1-7: Audit Export (PDF/CSV)

**Problem**: ENT customers need downloadable audit reports for SOC 2 / ISO 27001 compliance audits.

### D1 — Backend: Export Endpoint

**New file**: `backend/app/api/routes/audit_export.py`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| D1a | `GET /api/v1/evidence/export?format=csv&project_id=X` — CSV export of evidence records | ~40 | |
| D1b | `GET /api/v1/evidence/export?format=pdf&project_id=X` — PDF export (reportlab, optional dep guard) | ~50 | |
| D1c | Include: evidence type, upload date, submitter, SHA256 hash, gate binding, integrity status | ~10 | |
| D1d | Register route in `main.py`, tier STANDARD=2 | ~3 | |

### D2 — Frontend: Export Button

**Modified file**: `frontend/src/app/app/evidence/page.tsx`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| D2a | "Export" dropdown button (CSV / PDF options) | ~25 | |
| D2b | Download trigger with loading state | ~15 | |

### D3 — Tests

| ID | Item | LOC | Status |
|----|------|-----|--------|
| D3a | CSV export: correct columns, valid CSV format | ~20 | |
| D3b | PDF export: returns application/pdf content-type (requires reportlab) | ~15 | |

**Estimated LOC**: ~103 (backend) + ~40 (frontend) + ~35 (tests) = **~178 LOC**

---

## Track E — P1-8: ConversationFirstFallback Multi-Channel

**Problem**: `ConversationFirstFallback.tsx` hardcodes `https://t.me/sdlc_orchestrator_bot`. ENT customers may use Zalo, Teams, or Slack.

**Modified file**: `frontend/src/components/dashboard/ConversationFirstFallback.tsx`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| E1 | Read OTT channel config from env vars (TELEGRAM_BOT_URL, ZALO_OA_URL, TEAMS_BOT_URL, SLACK_BOT_URL) | ~10 | |
| E2 | Display all configured channels as buttons (not just Telegram) | ~20 | |
| E3 | Fallback: if no channel configured, show generic "Contact admin" message | ~5 | |

**Estimated LOC**: ~35

---

## Track F — P1-4 + P1-1: Documentation Fixes

| ID | Item | Status |
|----|------|--------|
| F1 | STM-056: Update status from PROPOSED → APPROVED (CTO sign-off in sprint review) | |
| F2 | FR-010 to FR-035 gap: Create mapping document showing which existing features cover these numbers | |
| F3 | Update ADR-068 if needed after Sprint 210 gate creation changes | |

**Estimated effort**: ~3 hours documentation work

---

## Track G — Tests + Regression Guard

| ID | Item | LOC | Status |
|----|------|-----|--------|
| G1 | `test_sprint211_ent_features.py` — 15 tests covering Tracks A-E | ~150 | |
| G2 | Sprint 200-211 regression guard (310+ baseline) — 0 regressions | | |

**Test breakdown**:
- T1-T3: Granular feature flags (each flag controls correct pages, all-on for ENT)
- T4-T8: MFA enrollment (setup, verify, wrong code, disable, grace period)
- T9-T10: DORA metrics (with data, empty project)
- T11-T12: Audit export (CSV format, PDF content-type)
- T13: ConversationFirstFallback renders multiple channels
- T14-T15: STM-056 APPROVED, FR mapping exists

---

## Summary

| Track | Focus | LOC (code) | LOC (tests) | Day | PM Notes |
|-------|-------|-----------|-------------|-----|----------|
| A | Granular feature flags | ~50 | ~30 | 1 | ~14 pages, not 22 |
| B | MFA TOTP enrollment | ~205 | ~75 | 1-3 | pyotp/qrcode pre-installed; check existing MFA routes |
| C | DORA metrics dashboard | ~243 | ~35 | 2-4 | Audit existing DORA baseline first |
| D | Audit export (CSV/PDF) | ~143 | ~35 | 3-4 | |
| E | Multi-channel fallback | ~35 | ~10 | 4 | |
| F | Documentation fixes | 0 | 0 | 5 | |
| G | Tests + regression | 0 | ~150 | 5 | |
| **Total** | | **~676 LOC** | **~335 LOC** | **5 days** | PM -63 LOC from original |

---

## Definition of Done — Sprint 211

- [ ] 6 granular feature flags replace binary `LEGACY_DASHBOARD` toggle
- [ ] MFA TOTP: setup (QR code), verify (6-digit), disable (admin), status endpoints working
- [ ] MFA frontend: setup wizard, backup codes, grace period banner
- [ ] DORA dashboard: 4 metrics + 30-day trend chart + period selector
- [ ] Audit export: CSV and PDF for evidence records
- [ ] ConversationFirstFallback: shows all configured OTT channels
- [ ] STM-056 status: APPROVED
- [ ] FR-010 to FR-035 mapping documented
- [ ] 15/15 Sprint 211 tests passing
- [ ] 310+ regression guards passing | 0 regressions
- [ ] CURRENT-SPRINT.md updated

---

## Dependencies

| Dependency | Track | Risk |
|-----------|-------|------|
| Sprint 210 Track A (ConversationFirstGuard fix) | Track B (MFA setup via Web) | Sprint 210 must ship first |
| `pyotp` (MIT) — already in `requirements/core.txt` | Track B | No action needed |
| `qrcode` (MIT) — already in `requirements/core.txt` | Track B | No action needed |
| `reportlab` (BSD) — optional dep guard | Track D | Already has ImportError guard pattern |
| MFA middleware BaseHTTPMiddleware → pure ASGI | Track B | MEDIUM risk — consider conversion |

---

*Sprint 211 — Close ENT feature gaps: MFA, DORA, exports, multi-channel*
*CTO-RPT-209-001 P1 remediation sprint*
