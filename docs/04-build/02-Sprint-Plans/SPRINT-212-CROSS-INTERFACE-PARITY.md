# Sprint 212 — Cross-Interface Parity + Frontend Testing Foundation

**Sprint Duration**: 5 working days
**Sprint Goal**: Achieve 80%+ action×interface coverage, establish frontend testing baseline, fill remaining ENT compliance gaps (SSO UI, usage dashboard, team management parity)
**Status**: PLANNED
**Priority**: P1/P2 (ENT compliance + quality)
**Framework**: SDLC 6.1.1
**Previous Sprint**: [Sprint 211 — ENT Feature Parity](SPRINT-211-ENT-FEATURE-PARITY.md)
**CTO Report**: [CTO-RPT-209-001](../../09-govern/01-CTO-Reports/CTO-REPORT-Sprint209-ENT-Compliance-Audit.md)
**ENT Compliance Target**: 78% → 85%

---

## Sprint 212 Goal

Sprint 210 fixed P0 blockers (58→68%). Sprint 211 closed P1 feature gaps (68→78%). Sprint 212 focuses on cross-interface parity and testing foundation:

1. **P0-3** (partial): Frontend test foundation — critical path tests (Vitest + Playwright already configured)
2. **P2-7**: Invite team member parity (CLI + Extension)
3. **P2-8**: Export audit parity (Web App button)
4. **P2-9**: CLI auth login command
5. **P2-4**: SSO configuration UI (SAML 2.0 admin page)
6. **P2-6**: Usage limits visibility dashboard
7. **Cross-interface**: Raise coverage matrix from ~70% → 85%

---

## Track A — P0-3: Frontend Testing Foundation

**Problem**: Frontend test coverage ~0%. ENT tier requires >90%. This sprint writes critical path tests (target: 30%+ critical paths).

> **PM Correction 1 (MAJOR)**: Vitest + Playwright are already configured. `frontend/vitest.config.ts` (jsdom, globals, v8 coverage), `frontend/src/__tests__/setup.ts` (1.1KB), `frontend/playwright.config.ts` all exist. Libraries installed: `vitest@^4.0.18`, `@testing-library/react@^16.3.2`, `@playwright/test@^1.57.0`. A1 (setup) and A3a (Playwright config) removed. Focus on writing tests only.

### ~~A1 — Vitest Setup + CI Integration~~ (ALREADY DONE — removed)

### A2 — Critical Path Unit Tests

| ID | Item | LOC | Status |
|----|------|-----|--------|
| A2a | Auth flow: login form validation, token storage, redirect logic | ~60 | |
| A2b | Gates page: gate list rendering, status badges, create gate dialog | ~50 | |
| A2c | Evidence page: file upload, type selector, integrity display | ~50 | |
| A2d | Sidebar: feature flag filtering, role-based visibility | ~40 | |
| A2e | ConversationFirstFallback: channel rendering, multi-channel display | ~20 | |

### A3 — Playwright E2E Tests (config already exists)

| ID | Item | LOC | Status |
|----|------|-----|--------|
| ~~A3a~~ | ~~Playwright config~~ — already exists (`playwright.config.ts`) | 0 | DONE |
| A3b | E2E: Login → Dashboard → View Gates → View Evidence (happy path) | ~50 | |
| A3c | E2E: Login → Create Gate → Submit Evidence → Evaluate (governance flow) | ~60 | |

**Estimated LOC**: ~330 (tests only, reduced from ~430 after removing setup items)

---

## Track B — P2-9: CLI Auth Login Command

**Problem**: `sdlcctl` has no `login` subcommand. Users must manually configure API tokens.

**Modified file**: `backend/sdlcctl/sdlcctl/commands/auth.py` (new sub-app)

| ID | Item | LOC | Status |
|----|------|-----|--------|
| B1 | `sdlcctl auth login` — interactive email+password prompt → JWT token → save to `~/.sdlcctl/config.json` | ~50 | |
| B2 | `sdlcctl auth login --api-key <key>` — API key mode for CI/CD | ~15 | |
| B3 | `sdlcctl auth status` — show current auth state (logged in user, token expiry) | ~20 | |
| B4 | `sdlcctl auth logout` — clear stored credentials | ~10 | |
| B5 | Register `auth` sub-app in `cli.py` | ~3 | |
| B6 | Token refresh: auto-refresh if within 5 min of expiry | ~20 | |

**Estimated LOC**: ~118

---

## Track C — P2-7: Invite Team Member Parity

**Problem**: Team invitation only works in Web App (admin panel) and OTT. CLI and Extension have no team management.

### C1 — CLI: `sdlcctl team invite`

**Modified file**: `backend/sdlcctl/sdlcctl/commands/team.py` (new or extend existing)

| ID | Item | LOC | Status |
|----|------|-----|--------|
| C1a | `sdlcctl team invite <email> --role member --project-id <uuid>` | ~30 | |
| C1b | `sdlcctl team list --project-id <uuid>` — show team members | ~20 | |
| C1c | `sdlcctl team remove <user-id> --project-id <uuid>` — admin only | ~15 | |

### C2 — Extension: Team Quick Invite

**Modified file**: `vscode-extension/src/commands/teamCommand.ts` (new)

| ID | Item | LOC | Status |
|----|------|-----|--------|
| C2a | `sdlc.inviteTeamMember` command — input box for email, dropdown for role | ~40 | |
| C2b | API call to `POST /api/v1/teams/{id}/members` | ~15 | |
| C2c | Register command in `extension.ts` | ~5 | |

**Estimated LOC**: ~125

---

## Track D — P2-8: Export Audit Parity (Web App UI Only)

**Problem**: Backend audit export API already exists at `POST /enterprise/audit/export` (Sprint 185, SOC2 Type II, `audit_trail.py` ~525 LOC with CSV + JSON export). **No Web App UI button** exists to trigger the export.

> **PM Correction 2 (MAJOR)**: Backend `audit_trail.py` already has full export capability. Remove D1/D3 backend items.
> **PM Correction 4**: Corrected claim — the issue is "No Web App UI button for the existing backend export API", not "Export audit only in CLI."

**Existing backend**: `backend/app/api/routes/audit_trail.py` — `POST /enterprise/audit/export`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| ~~D1~~ | ~~Backend audit export~~ — already exists in `audit_trail.py` | 0 | DONE |
| D2 | Web App: "Export Audit Trail" button on project detail page (calls existing API) | ~25 | |
| ~~D3~~ | ~~Include fields~~ — already implemented in existing endpoint | 0 | DONE |

**Estimated LOC**: ~25 (frontend button only)

---

## Track E — P2-4: SSO Configuration UI (Frontend Only)

**Problem**: Backend has complete SAML 2.0 + Azure AD SSO implementation, but no admin UI for configuration.

> **PM Correction 3 (MAJOR)**: SSO backend is fully complete in `enterprise_sso.py` (Sprint 183, ADR-061) with 6 endpoints:
> - `POST /enterprise/sso/configure`
> - `GET /enterprise/sso/saml/metadata`
> - `POST /enterprise/sso/saml/login`
> - `POST /enterprise/sso/saml/callback`
> - `GET /enterprise/sso/azure-ad/login`
> - `GET /enterprise/sso/azure-ad/callback`
>
> Remove E1 backend items entirely. Track E is frontend UI only.

### ~~E1 — Backend: SSO Config CRUD~~ (ALREADY COMPLETE — `enterprise_sso.py`, Sprint 183)

**Existing backend**: `backend/app/api/routes/enterprise_sso.py` — 6 SAML + Azure AD endpoints

**Note**: Verify whether `GET /enterprise/sso/config` (read config) and `POST /enterprise/sso/test` (test connection) exist in current routes or need adding as thin wrappers.

### E2 — Frontend: SSO Admin Page

**New file**: `frontend/src/app/admin/sso/page.tsx`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| E2a | SAML configuration form: IdP metadata URL, Entity ID, Certificate (textarea) | ~60 | |
| E2b | Test connection button with status indicator | ~20 | |
| E2c | SSO status badge (Enabled/Disabled/Error) | ~10 | |
| E2d | Help text: setup instructions for common IdPs (Okta, Azure AD, Google Workspace) | ~15 | |

**Estimated LOC**: ~105 (frontend only, reduced from ~183)

---

## Track F — P2-6: Usage Limits Dashboard

**Problem**: `UsageLimitsMiddleware` enforces limits but users can't see their current usage vs quota.

### F1 — Backend: Usage Stats Endpoint

**New file**: `backend/app/api/routes/usage.py`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| F1a | `GET /api/v1/usage/stats` — current usage vs tier limits (projects, storage, gates/month, members) | ~40 | |
| F1b | Register route, tier LITE=1 (all tiers can see their own usage) | ~3 | |

### F2 — Frontend: Usage Dashboard Widget

**New file**: `frontend/src/components/dashboard/UsageWidget.tsx`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| F2a | 4 progress bars: projects, storage, gates/month, team members | ~40 | |
| F2b | Color coding: green (<60%), yellow (60-80%), red (>80%) | ~10 | |
| F2c | "Upgrade" CTA when approaching limit | ~10 | |
| F2d | Add widget to main dashboard page | ~5 | |

**Estimated LOC**: ~108

---

## Track G — Tests + Regression Guard

| ID | Item | LOC | Status |
|----|------|-----|--------|
| G1 | `test_sprint212_parity.py` — 12 backend tests covering Tracks B-F | ~120 | |
| G2 | Sprint 200-212 regression guard (310+ baseline) — 0 regressions | | |

**Test breakdown**:
- T1-T3: CLI auth (login with password, login with API key, status)
- T4-T5: CLI team invite (valid invite, admin-only remove)
- T6-T7: Audit export (full trail CSV, project not found)
- T8-T9: SSO config (get, update with valid metadata)
- T10-T11: Usage stats (returns correct limits per tier, storage calculation)
- T12: Extension team invite command registered

---

## Summary

| Track | Focus | LOC (code) | LOC (tests) | Day | PM Notes |
|-------|-------|-----------|-------------|-----|----------|
| A | Frontend testing (tests only) | 0 | ~330 | 1-3 | Setup already done (-100) |
| B | CLI auth login | ~118 | ~30 | 1-2 | |
| C | Team invite parity (CLI+Extension) | ~125 | ~20 | 2-3 | |
| D | Export audit (Web App button only) | ~25 | ~15 | 3 | Backend exists (-65) |
| E | SSO config UI (frontend only) | ~105 | ~20 | 3-4 | Backend exists (-78) |
| F | Usage limits dashboard | ~108 | ~15 | 4 | |
| G | Backend tests + regression | 0 | ~120 | 5 | |
| **Total** | | **~481 LOC** | **~550 LOC** | **5 days** | PM -343 LOC from original |

> **PM Assessment**: Sprint is ~27% smaller than originally estimated. Recommend pulling Sprint 213 "Extension gate create" into Sprint 212 to maximize output.

---

## Definition of Done — Sprint 212

- [ ] ~~Vitest configured~~ (already done) — 5 test suites for critical paths (auth, gates, evidence, sidebar, fallback)
- [ ] ~~Playwright configured~~ (already done) — 2 E2E scenarios (happy path + governance flow)
- [ ] `sdlcctl auth login` / `status` / `logout` working
- [ ] `sdlcctl team invite` / `list` / `remove` working
- [ ] Extension: `sdlc.inviteTeamMember` command registered
- [ ] Audit trail export: Web App button, CSV/PDF formats
- [ ] SSO admin page: frontend UI for existing SAML backend (`enterprise_sso.py`)
- [ ] Usage widget: 4 progress bars on dashboard
- [ ] 12/12 Sprint 212 backend tests passing
- [ ] Frontend test coverage: >30% critical paths
- [ ] 310+ regression guards passing | 0 regressions
- [ ] CURRENT-SPRINT.md updated

---

## Cross-Interface Coverage After Sprint 212

> **PM Correction 5**: Matrix should be verified against current interface capabilities before Sprint 212 starts, to avoid double-counting existing work. Some actions (e.g., Create Project in Web App) may already work from MVP era.

| Action | Web App | CLI | Extension | OTT | Coverage |
|--------|---------|-----|-----------|-----|----------|
| Create Project | YES (S210) | YES | NO | YES | 3/4 |
| **Create Gate** | **YES (S210)** | **YES (S210)** | NO | **YES (S210)** | **3/4** |
| Submit Evidence | YES (S210) | YES | YES | YES | 4/4 |
| Evaluate Gate | YES (S210) | YES | read-only | YES | 3/4 |
| Approve Gate | YES (S210) | YES | YES | YES | 4/4 |
| Set Workspace | N/A | N/A | N/A | YES | 1/1 |
| Link Identity | N/A | N/A | N/A | YES | 1/1 |
| View Status | YES | YES | YES | YES | 4/4 |
| Close Sprint | YES (S210) | YES (S210) | NO | YES | 3/4 |
| **Invite Member** | YES | **YES (S212)** | **YES (S212)** | YES | **4/4** |
| **Export Audit** | **YES (S212)** | YES | NO | NO | **2/4** |
| **Auth Login** | YES | **YES (S212)** | YES | YES | **4/4** |

**Coverage after Sprint 212**: ~56/72 = **78%** (was 61%)

---

## Sprint 213-216 Preview (Remaining to 90%+)

| Sprint | Focus | Target |
|--------|-------|--------|
| 213 | Frontend test coverage push (30→70%) + Extension gate create | 82% |
| 214 | GDPR/Data Residency UI + Compliance dashboard unhide | 85% |
| 215 | Full P2 close: dual doc cleanup, ERD header update, ADR gaps | 88% |
| 216 | Performance audit + Load testing + ENT certification prep | 90%+ |

---

*Sprint 212 — Cross-interface parity + frontend testing foundation*
*CTO-RPT-209-001 P1/P2 remediation sprint*
