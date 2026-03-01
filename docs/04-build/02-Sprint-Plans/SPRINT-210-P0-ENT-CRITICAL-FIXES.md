# Sprint 210 — P0 ENT Critical Fixes (v2 — CTO+PM Reviewed)

**Sprint Duration**: 3 working days
**Sprint Goal**: Fix 6 P0 blockers from CTO-RPT-209-001 + PM/CTO review — cookie-blind middleware, ConversationFirstGuard, gate creation (3 interfaces), FR traceability, sprint close parity
**Status**: PLANNED → **CTO APPROVED (v2, all corrections applied)**
**Priority**: P0 (ENT launch blockers) + selected P1 (ADR-068, sprint close)
**Framework**: SDLC 6.1.1
**Previous Sprint**: [Sprint 209 — OTT Identity + Team Collaboration](SPRINT-209-OTT-IDENTITY-TEAM-COLLAB.md)
**CTO Report**: [CTO-RPT-209-001](../../09-govern/01-CTO-Reports/CTO-REPORT-Sprint209-ENT-Compliance-Audit.md)
**PM Review**: APPROVED WITH 3 CORRECTIONS (applied)
**CTO Review**: NO-GO v1 → 5 corrections applied → resubmitted v2
**ENT Compliance Target**: 58% → 68%

---

## Scope Classification (CTO Correction 1)

This sprint addresses **4 P0 items + 2 selected P1 items**:

| Priority | ID | Item |
|----------|-----|------|
| **P0** | A0 | Cookie-blind middleware (TierGate + UsageLimits + ConversationFirstGuard) |
| **P0** | A | ConversationFirstGuard blocks non-admin governance via Web App |
| **P0** | B | Gate creation exposed in 0/4 interfaces |
| **P0** | C | FR numbering collisions (FR-045, FR-046) |
| **P1** | D | ADR-068 status DRAFT → submit for CTO approval |
| **P1** | E | Sprint close — only 1/4 interfaces |

---

## Track A0 — P0: Cookie-Blind Middleware Fix (Day 1, PREREQUISITE)

**Problem**: TierGateMiddleware, UsageLimitsMiddleware, and ConversationFirstGuard only read `Authorization: Bearer` headers — never parse `sdlc_access_token` httpOnly cookies. ALL cookie-authenticated web dashboard users are misresolved:
- TierGate: resolves as LITE → silently blocks ENTERPRISE routes with HTTP 402
- UsageLimits: resolves as LITE → wrong quota enforcement
- ConversationFirstGuard: user_id=None → fail-open (guard is no-op for web users)

**Impact**: CTO's platform admin account cannot access `/admin/ai-providers` via web — bug reported this sprint.

**Status**: Cookie parsing already coded for `tier_gate.py` + `usage_limits.py` (local changes, not committed). `conversation_first_guard.py` needs the same fix.

| ID | Item | LOC | Status |
|----|------|-----|--------|
| A0a | `tier_gate.py:384-420` — cookie JWT parsing in `_extract_user_id()` (already coded) | ~20 | ✅ DONE |
| A0b | `usage_limits.py:285-335` — cookie JWT parsing (already coded) | ~20 | ✅ DONE |
| A0c | `conversation_first_guard.py:208+` — add cookie JWT parsing to `_extract_user_id()` (same pattern) | ~20 | |
| A0d | Tests: cookie-based tier resolution returns correct tier (3 tests) | ~30 | |

**Verification** (CTO Correction 5):
```
Test A0d-1: TierGate cookie → ENTERPRISE user sees tier=ENTERPRISE (not LITE)
Test A0d-2: UsageLimits cookie → correct quota for STANDARD user
Test A0d-3: ConversationFirstGuard cookie → correctly identifies non-admin member
Expected: 3/3 passing, HTTP 200 on /admin/ai-providers for superuser via cookie
```

**MUST SHIP BEFORE**: Track A (ConversationFirstGuard role-aware), Track B3 (Web gate creation)

---

## Track A — P0: ConversationFirstGuard Scope-Based Bypass

**Problem**: `ADMIN_WRITE_PATHS` blocks POST to `/api/v1/gates`, `/api/v1/evidence`, `/api/v1/projects` for ALL non-admin users.

**Root Cause**: Sprint 192 added gates/evidence/projects to `ADMIN_WRITE_PATHS` without considering team members need write access.

**Solution**: Split into `ADMIN_ONLY_PATHS` (admin/owner) + `TEAM_WRITE_PATHS` (any project member with active membership).

**Modified file**: `backend/app/middleware/conversation_first_guard.py`

**Dependency**: Track A0 MUST be merged first (cookie parsing needed for web user identification).

| ID | Item | LOC | Status |
|----|------|-----|--------|
| A1 | Split `ADMIN_WRITE_PATHS` into `ADMIN_ONLY_PATHS` + `TEAM_WRITE_PATHS` | ~15 | |
| A2 | Add `_resolve_is_project_member()` — check `ProjectMember` table for user_id (reuses existing `check_project_membership` pattern from `gates.py:454`) | ~25 | |
| A3 | Update `__call__()` — if path in `TEAM_WRITE_PATHS` and user is project member → pass | ~10 | |
| A4 | Tests: 4 cases (see verification matrix) | ~40 | |

**Verification** (CTO Correction 5):
```
Test A4-1: Member POST /api/v1/gates → 200 (pass through to route handler)
Test A4-2: Non-member POST /api/v1/gates → 403 (conversation_first_guard)
Test A4-3: Admin POST /api/v1/admin → 200 (admin path, admin user)
Test A4-4: GET /api/v1/gates (any user) → 200 (read-only always passes)
Expected: 4/4 passing
```

**Estimated LOC**: ~50 (middleware) + ~40 (tests) = **~90 LOC**

---

## Track B — P0: Gate Creation Across 3 Interfaces

**Problem**: `POST /api/v1/gates` exists in backend (gates.py:400) but no interface exposes it.

### API Contract (CTO Correction 2)

The `GateCreateRequest` schema (gate.py:79-110) requires:

```python
class GateCreateRequest(BaseModel):
    project_id: UUID          # REQUIRED — project UUID
    gate_name: str            # REQUIRED — e.g. "G1", "G2", "G0.1"
    gate_type: str            # REQUIRED — e.g. "CONSULTATION", "SHIP_READY"
    stage: str                # REQUIRED — e.g. "WHAT", "BUILD", "SHIP"
    description: Optional[str]
    exit_criteria: List[Dict] # defaults to []
```

**Gate name → (gate_type, stage) mapping table** (used by OTT and CLI to auto-fill):

| User Input | gate_name | gate_type | stage | description |
|-----------|-----------|-----------|-------|-------------|
| `G0.1` | G0.1 | FOUNDATION_READY | WHY | Problem Definition |
| `G0.2` | G0.2 | SOLUTION_DIVERSITY | WHY | Solution Diversity |
| `G1` | G1 | CONSULTATION | WHAT | Planning Review |
| `G2` | G2 | DESIGN_READY | HOW | Design Review |
| `G3` | G3 | SHIP_READY | BUILD | Ship Ready |
| `G4` | G4 | LAUNCH_READY | DEPLOY | Launch Ready |

This mapping is defined ONCE in a shared constant (`GATE_PRESETS` dict) reused by OTT handler and CLI.

### B1 — OTT: Route via Intent (No Registry Slot Needed — CTO Correction 3)

**Problem**: `MAX_COMMANDS=10` already full (all 10 `ToolName` slots used). Adding a new command would violate the cap.

**Solution**: Route `/gate create` via **slash command intercept** in `ai_response_handler.py` (same pattern as `/workspace set` which also bypasses the LLM command registry). No new `ToolName` slot needed.

**Modified file**: `backend/app/services/agent_bridge/ai_response_handler.py`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| B1a | Add `/gate_create` to slash-to-governance bypass (same as `/workspace_set` pattern, line ~480) | ~5 | |
| B1b | Parse `/gate create G1` → extract gate preset name | ~10 | |

**Modified file**: `backend/app/services/agent_bridge/governance_action_handler.py`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| B1c | Add `GATE_PRESETS` dict — 6 entries mapping gate_name → (gate_type, stage, description) | ~20 | |
| B1d | Add `execute_create_gate(db, project_id, gate_preset, user_id)` — build `GateCreateRequest` payload from preset, call `create_gate()` service, format reply | ~45 | |
| B1e | Error handling: invalid preset name → list available presets; missing workspace → prompt `/workspace set` | ~15 | |

### B2 — CLI: `sdlcctl gate create`

**Modified file**: `backend/sdlcctl/sdlcctl/commands/gate.py`

| ID | Item | LOC | Status |
|----|------|-----|--------|
| B2a | Add `create` subcommand with `--gate-name` (e.g. `G1`), `--project-id` (UUID) options | ~25 | |
| B2b | Import `GATE_PRESETS` → auto-fill `gate_type` + `stage` from `--gate-name` | ~10 | |
| B2c | API call: `POST /api/v1/gates` with full payload `{project_id, gate_name, gate_type, stage, description}` | ~15 | |
| B2d | Validation: `--gate-name` must be in GATE_PRESETS keys, else show available options | ~10 | |

### B3 — Web App: "Create Gate" Button

**Modified file**: `frontend/src/app/app/gates/page.tsx`

**Dependency**: **BLOCKED-BY Track A3** (PM Correction 2). ConversationFirstGuard must allow member POST to /gates before this UI works.

| ID | Item | LOC | Status |
|----|------|-----|--------|
| B3a | "Create Gate" button next to page title (Dialog trigger) | ~15 | |
| B3b | `CreateGateDialog` — project selector (from user's projects) + gate type dropdown (6 presets) + auto-filled type/stage/description | ~60 | |
| B3c | `useCreateGate` mutation hook (`POST /api/v1/gates`, invalidate gates query) | ~20 | |

### B4 — Tests + Verification

| ID | Item | LOC | Status |
|----|------|-----|--------|
| B4a | OTT: `/gate create G1` with workspace → 201 Created, response has gate_type=CONSULTATION, stage=WHAT | ~25 | |
| B4b | OTT: `/gate create` without workspace → "Set workspace first" prompt | ~15 | |
| B4c | OTT: `/gate create INVALID` → list of valid gate names | ~15 | |
| B4d | CLI: `sdlcctl gate create --gate-name G1 --project-id <uuid>` → 201 | ~20 | |

**Verification** (CTO Correction 5):
```
Test B4a: POST /api/v1/gates with {project_id, gate_name:"G1", gate_type:"CONSULTATION", stage:"WHAT"} → 201
Test B4b: Missing workspace → 400-level guidance message
Test B4c: Invalid gate name → 422 with available options
Test B4d: CLI output: "✅ Gate G1 (Planning Review) created for project X"
Expected: 4/4 passing
```

**Estimated LOC**: ~95 (OTT) + ~60 (CLI) + ~95 (Web) = **~250 LOC** + ~75 (tests)

---

## Track C — P0: FR Numbering Collision Fix

**Problem**: FR-045 = GDPR AND LangChain. FR-046 = Chat Router AND LangGraph.

**Solution**: Renumber Sprint 205-206 FRs to FR-051 and FR-052.

| ID | Item | Status |
|----|------|--------|
| C1 | `git mv` FR-045-LangChain-Provider-Plugin.md → FR-051-LangChain-Provider-Plugin.md | |
| C2 | `git mv` FR-046-LangGraph-Workflow-Engine.md → FR-052-LangGraph-Workflow-Engine.md | |
| C3 | Update YAML frontmatter `fr_id` field in both files | |
| C4 | Update reference in `SPRINT-205-LANGCHAIN-PROVIDER.md` (confirmed: 1 match) | |
| C5 | Update reference in `SPRINT-206-LANGGRAPH-WORKFLOWS.md` (confirmed: 1 match) | |
| C6 | ~~Update ADR-065/ADR-066~~ → **NO CHANGE NEEDED** (CTO Correction 5: grep confirmed 0 matches in ADR files) | |
| C7 | Grep full codebase for remaining `FR-045` and `FR-046` references in code comments | |

**Estimated effort**: ~1 hour documentation work, 0 code changes

---

## Track D — P1: ADR-068 Status Promotion (CTO Correction 4)

**Problem**: ADR-068-OTT-Identity-Linking.md exists but status is **DRAFT** (line 4).

**Corrected approach** (was: "verify APPROVED"; now: "submit for approval"):

| ID | Item | Owner | Due |
|----|------|-------|-----|
| D1 | Verify ADR-068 has: Context, Decision, Consequences, Alternatives Considered | Dev | Day 1 |
| D2 | Verify ADR-068 documents: email verification, rate limiting (5/15min), GETDEL atomicity, 60-min cache TTL | Dev | Day 1 |
| D3 | **Promote ADR-068 status from DRAFT → SUBMITTED** (add `submitted_by: PM`, `submitted_date`) | PM | Day 2 |
| D4 | **CTO approval target: Sprint 210 review** (CTO signs off → status becomes APPROVED) | CTO | Sprint close |
| D5 | Update ADR index / SPRINT-INDEX.md if applicable | Dev | Day 3 |

**Key change from v1**: Status target is **SUBMITTED** (not APPROVED) during sprint execution. CTO promotes to APPROVED during sprint review.

---

## Track E — P1: Sprint Close Parity (CLI + Web)

**Problem**: `/close sprint` only works via OTT (1/4 interfaces).

### E1 — CLI: `sdlcctl governance close-sprint`

**Modified file**: `backend/sdlcctl/sdlcctl/commands/governance.py`

Note: `governance.py` already has the governance sub-app structure with existing commands.

| ID | Item | LOC | Status |
|----|------|-----|--------|
| E1a | Add `close-sprint` subcommand — `--project-id` (UUID) required | ~25 | |
| E1b | Confirmation prompt: "Close sprint for project {name}? [y/N]" | ~5 | |
| E1c | API call: delegates to `sprint_governance_handler.handle_close_sprint()` logic via HTTP | ~15 | |

### E2 — Web App: Sprint Close Button

**Modified file**: `frontend/src/app/app/gates/page.tsx` (or sprint governance section if it exists)

| ID | Item | LOC | Status |
|----|------|-----|--------|
| E2a | "Close Sprint" action button with confirmation AlertDialog | ~30 | |
| E2b | `useCloseSprint` mutation hook | ~15 | |

**Verification** (CTO Correction 5):
```
Test E-1: CLI: `sdlcctl governance close-sprint --project-id <uuid>` → confirmation + success
Test E-2: Web: Click "Close Sprint" → confirmation dialog → POST /close → success toast
Expected: 2/2 passing
```

**Estimated LOC**: ~45 (CLI) + ~45 (Web) = **~90 LOC**

---

## Track F — Tests + Regression Guard

| ID | Item | LOC | Status |
|----|------|-----|--------|
| F1 | `test_sprint210_p0_fixes.py` — 15 tests covering all tracks | ~150 | |
| F2 | Sprint 200-210 regression guard (310+ baseline) — 0 regressions | | |

**Test matrix** (CTO Correction 5):

| Test | Track | Input | Expected Output |
|------|-------|-------|----------------|
| T1 | A0 | Cookie JWT → TierGate | Correct tier (ENTERPRISE) |
| T2 | A0 | Cookie JWT → UsageLimits | Correct quota |
| T3 | A0 | Cookie JWT → ConvFirstGuard | Identifies user correctly |
| T4 | A | Member POST /gates | 200 (pass through) |
| T5 | A | Non-member POST /gates | 403 (blocked) |
| T6 | A | Admin POST /admin | 200 (admin path) |
| T7 | A | GET /gates (any) | 200 (read-only) |
| T8 | B | OTT `/gate create G1` + workspace | 201, gate_type=CONSULTATION |
| T9 | B | OTT `/gate create` no workspace | Guidance message |
| T10 | B | OTT `/gate create INVALID` | Available presets list |
| T11 | B | CLI `gate create --gate-name G1` | 201 Created |
| T12 | C | FR-051 file exists | True |
| T13 | C | FR-052 file exists | True |
| T14 | E | CLI `governance close-sprint` | Success + confirmation |
| T15 | E | Web sprint close mutation | POST succeeds |

---

## Day Schedule (with Dependencies — PM Correction 2)

| Day | Track | Items | Dependency |
|-----|-------|-------|------------|
| **Day 1 AM** | A0 | Cookie parsing for conversation_first_guard.py + commit tier_gate/usage_limits fixes | None (prerequisite) |
| **Day 1 PM** | A | ConversationFirstGuard split ADMIN_ONLY/TEAM_WRITE + member check | A0 merged |
| **Day 1 PM** | C | FR renumbering (git mv + frontmatter + sprint plan refs) | None |
| **Day 1 PM** | D | ADR-068 completeness check + promote to SUBMITTED | None |
| **Day 2 AM** | B1+B2 | Gate creation OTT (slash bypass + GATE_PRESETS) + CLI | A merged (for OTT testing) |
| **Day 2 PM** | **B3** | **Web "Create Gate" button** | **A3 merged + verified** (PM Correction 2) |
| **Day 2 PM** | E | Sprint close CLI + Web | None |
| **Day 3** | F | All 15 tests + regression guard | All tracks merged |

---

## Summary

| Track | Focus | LOC (code) | LOC (tests) | Day |
|-------|-------|-----------|-------------|-----|
| A0 | Cookie-blind middleware fix | ~40 | ~30 | 1 AM |
| A | ConversationFirstGuard bypass | ~50 | ~40 | 1 PM |
| B | Gate creation (OTT+CLI+Web) | ~250 | ~75 | 2 |
| C | FR numbering fix | 0 (docs) | 0 | 1 |
| D | ADR-068 → SUBMITTED | 0 (docs) | 0 | 1 |
| E | Sprint close parity | ~90 | ~20 | 2 |
| F | Tests + regression | 0 | ~150 | 3 |
| **Total** | | **~430 LOC** | **~315 LOC** | **3 days** |

---

## Definition of Done — Sprint 210

- [ ] Cookie JWT parsing: all 3 middleware resolve web dashboard users correctly
- [ ] ConversationFirstGuard: team members can POST to /gates, /evidence, /projects; non-members blocked
- [ ] Gate creation: works in OTT (`/gate create G1`), CLI (`sdlcctl gate create --gate-name G1`), Web App (dialog)
- [ ] `GATE_PRESETS` shared constant: 6 gate types with auto-filled gate_type+stage+description
- [ ] FR-045/FR-046 collision resolved (renamed to FR-051/FR-052)
- [ ] ADR-068 status: SUBMITTED (CTO signs APPROVED at sprint review)
- [ ] Sprint close: works in CLI (`sdlcctl governance close-sprint`) and Web App
- [ ] 15/15 Sprint 210 tests passing (verification matrix above)
- [ ] 310+ regression guards passing | 0 regressions
- [ ] CURRENT-SPRINT.md updated

---

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| ConversationFirstGuard opens security hole | `_resolve_is_project_member()` validates ProjectMember table. Non-members blocked at middleware |
| **B3 blocked by A** (PM Correction 2) | Day schedule enforces: A merged Day 1 → B3 starts Day 2 PM |
| Gate creation 422 from mismatched payload (CTO Correction 2) | `GATE_PRESETS` auto-fills gate_type+stage. Manual override available for custom gates |
| OTT command cap exceeded (CTO Correction 3) | Slash bypass pattern (no ToolName slot). Same pattern as `/workspace set` |
| ADR-068 not approved within sprint (CTO Correction 4) | Target is SUBMITTED (achievable). CTO approval at sprint review (realistic) |
| FR rename breaks cross-references (CTO Correction 5) | C6 confirmed: ADR-065/066 have 0 FR-045/046 refs. Only sprint plans need update |

---

## Review Corrections Applied

| # | Source | Original | Corrected |
|---|--------|----------|-----------|
| PM-1 | PM Review | "Verify ADR-068 APPROVED" | "Promote DRAFT → SUBMITTED, CTO approves at review" |
| PM-2 | PM Review | B3 not explicitly blocked by A | "B3 BLOCKED-BY A3" in day schedule + risk table |
| PM-3 | PM Review | Missing cookie-blind fix | Track A0 added as Day 1 prerequisite |
| CTO-1 | CTO Review | Scope mixed P0+P1 without labels | Scope table with explicit P0/P1 classification |
| CTO-2 | CTO Review | Gate input `G1` mismatches API contract | `GATE_PRESETS` mapping table + `GateCreateRequest` fields documented |
| CTO-3 | CTO Review | New OTT command hits MAX_COMMANDS=10 | Slash bypass pattern (no registry slot needed) |
| CTO-4 | CTO Review | ADR APPROVED unrealistic in execution | Target is SUBMITTED; CTO signs at sprint review |
| CTO-5 | CTO Review | Missing verification matrix | Per-track test→expected output tables added |

---

*Sprint 210 v2 — All 8 review corrections applied*
*CTO-RPT-209-001 P0 remediation sprint*
