# Sprint 213 — Frontend Test Coverage Push + Extension Gate Create

**Sprint Duration**: 5 working days
**Sprint Goal**: Push frontend test coverage from 30% → 70% critical paths, add Extension gate create for cross-interface parity
**Status**: IN PROGRESS
**Priority**: P1 (ENT compliance + quality)
**Framework**: SDLC 6.1.1
**Previous Sprint**: [Sprint 212 — Cross-Interface Parity](SPRINT-212-CROSS-INTERFACE-PARITY.md)
**CTO Report**: [CTO-RPT-209-001](../../09-govern/01-CTO-Reports/CTO-REPORT-Sprint209-ENT-Compliance-Audit.md)
**ENT Compliance Target**: 85% → 88%

---

## Sprint 213 Goal

Sprint 212 established frontend testing baseline (12 tests across 4 suites) and closed cross-interface gaps (CLI auth, team invite, SSO UI, usage dashboard). Sprint 213 focuses on:

1. **Frontend test coverage push** (30% → 70% critical paths): Hook tests + component tests
2. **Extension gate create** — last major cross-interface gap for gate operations

---

## Track A — Hook Unit Tests

**Problem**: 0 out of 44 hooks have tests. Hooks contain all data-fetching and business logic for the frontend.

**Strategy**: Test the 8 most critical hooks that are used across multiple pages.

| ID | Item | LOC | Status |
|----|------|-----|--------|
| A1 | `useAuth` — login, logout, token management, user state | ~80 | |
| A2 | `useProjects` — project listing, CRUD, query caching | ~70 | |
| A3 | `useGates` — gate CRUD, status management | ~70 | |
| A4 | `useEvidence` — evidence list, upload, integrity | ~60 | |
| A5 | `useTeams` — team listing, member management | ~50 | |
| A6 | `useUserTier` — tier detection, feature gating | ~40 | |
| A7 | `useCodegen` — code generation, streaming | ~50 | |
| A8 | `useKillSwitch` — governance mode, kill switch state | ~40 | |

**Estimated LOC**: ~460 (tests only)

---

## Track B — Component Unit Tests

**Problem**: Only 2 out of 87 components have tests (GitHubConnectButton, InviteMemberModal). Critical dashboard and governance components untested.

| ID | Item | LOC | Status |
|----|------|-----|--------|
| B1 | `UsageWidget` — progress bars, color coding, upgrade CTA | ~50 | |
| B2 | `ExportAuditButton` — dropdown, CSV/PDF export, loading state | ~50 | |
| B3 | `Header` — user info, navigation, logout | ~40 | |
| B4 | `AuthGuard` — redirect unauthenticated, loading state | ~40 | |
| B5 | `TierBadge` — tier display, color mapping | ~30 | |
| B6 | `NotificationCenter` — notification list, mark read, empty state | ~50 | |

**Estimated LOC**: ~260 (tests only)

---

## Track C — Extension Gate Create Command

**Problem**: Gate creation available in Web App, CLI, and OTT but NOT in VS Code Extension. Cross-interface matrix shows 3/4 for Create Gate.

### C1 — API Client Method

**Modified file**: `vscode-extension/src/services/apiClient.ts`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| C1a | `createGate()` method — POST /api/v1/gates | ~15 | |

### C2 — Command Implementation

**New file**: `vscode-extension/src/commands/createGateCommand.ts`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| C2a | Gate type quick pick (G0.1, G0.2, G1, G2, G3, G4) with GATE_PRESETS | ~40 | |
| C2b | Multi-step input: project → type → name → description → exit criteria | ~80 | |
| C2c | Server-driven: call createGate → show result → refresh gate view | ~30 | |

### C3 — Registration

**Modified file**: `vscode-extension/src/extension.ts`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| C3a | Import + register `sdlc.createGate` command | ~3 | |

**Estimated LOC**: ~168

---

## Track D — Tests + Regression Guard

| ID | Item | LOC | Status |
|----|------|-----|--------|
| D1 | `test_sprint213_ext_gate.py` — backend tests for extension gate create parity | ~80 | |
| D2 | Sprint 209-213 combined regression (109+ baseline) — 0 regressions | | |
| D3 | Full regression guard (3569+ baseline) | | |

**Test breakdown**:
- T1-T2: Extension createGateCommand file exists + sdlc.createGate content
- T3-T4: apiClient.ts has createGate method + POST /api/v1/gates
- T5-T8: Frontend test file existence checks (8 hook + 6 component test files)

---

## Summary

| Track | Focus | LOC (code) | LOC (tests) | Day |
|-------|-------|-----------|-------------|-----|
| A | Hook unit tests (8 hooks) | 0 | ~460 | 1-3 |
| B | Component unit tests (6 components) | 0 | ~260 | 2-4 |
| C | Extension gate create | ~168 | ~20 | 3-4 |
| D | Backend tests + regression | 0 | ~80 | 5 |
| **Total** | | **~168 LOC** | **~820 LOC** | **5 days** |

---

## Cross-Interface Coverage After Sprint 213

| Action | Web App | CLI | Extension | OTT | Coverage |
|--------|---------|-----|-----------|-----|----------|
| Create Project | YES | YES | NO | YES | 3/4 |
| **Create Gate** | YES | YES | **YES (S213)** | YES | **4/4** |
| Submit Evidence | YES | YES | YES | YES | 4/4 |
| Evaluate Gate | YES | YES | read-only | YES | 3/4 |
| Approve Gate | YES | YES | YES | YES | 4/4 |
| Invite Member | YES | YES | YES | YES | 4/4 |
| Export Audit | YES | YES | NO | NO | 2/4 |
| Auth Login | YES | YES | YES | YES | 4/4 |

**Coverage after Sprint 213**: ~58/72 = **81%** (was 78%)

---

## Definition of Done — Sprint 213

- [ ] 8 hook test suites passing (useAuth, useProjects, useGates, useEvidence, useTeams, useUserTier, useCodegen, useKillSwitch)
- [ ] 6 component test suites passing (UsageWidget, ExportAuditButton, Header, AuthGuard, TierBadge, NotificationCenter)
- [ ] Extension: `sdlc.createGate` command registered and functional
- [ ] apiClient.createGate() method added
- [ ] Backend Sprint 213 tests passing
- [ ] Sprint 209-213 combined tests passing
- [ ] 3569+ regression guards passing | 0 regressions
- [ ] Frontend test coverage: >50% critical paths
- [ ] CURRENT-SPRINT.md updated

---

*Sprint 213 — Frontend test coverage push + Extension gate create*
*CTO-RPT-209-001 P1 remediation sprint*
