---
sdlc_version: "6.1.1"
document_type: "Sprint Plan"
status: "APPROVED"
sprint: "194"
spec_id: "SPRINT-194"
tier: "ALL"
stage: "04 - Build"
cto_review: "Pending"
reviewer_audit: "Sprint 193 CTO Review (9.1/10) + Sprint 192 Carried Findings"
---

# Sprint 194 — Security Hardening + Agent Enrichment

**Status**: APPROVED — Ready for @dev team execution
**Duration**: 8 working days (February 24 – March 5, 2026)
**Goal**: Resolve Sprint 192 carried findings, close Sprint 193 CTO carry-forwards, add seed agent definitions + team presets, and register `update_sprint` chat command
**Epic**: EP-08 Chat-First Governance Loop (P2 — Hardening + Agent Enrichment)
**Preceded by**: Sprint 193 (CURRENT-SPRINT.md Platform Enforcement, CTO 9.1/10)
**Budget**: ~$5,120 (64 hrs @ $80/hr)

---

## Context

- Sprint 193 was re-scoped to CURRENT-SPRINT.md Platform Enforcement (CEO directive). Original backlog deferred.
- Sprint 193 CTO review (9.1/10) identified 3 carry-forwards: F401 cleanup, inline imports, integration test.
- Sprint 192 carried 5 findings (F-192-03 through F-192-07). **Investigation found 2 already resolved**:
  - F-192-03 (deferred import in `_verify_zalo_signature`): **NO ACTION** — intentional lazy-load pattern, best practice.
  - F-192-04 (PA-69 empty-timestamp test): **NO ACTION** — test already exists at `test_zalo_normalizer.py:141-154`, comprehensive (2 assertions).
- Feature parity gaps GAP-01 and GAP-02 from MTS-OpenClaw comparison remain open.
- `ROLE_MODEL_DEFAULTS` in `agent_team/config.py:38-54` provides 12 role defaults ready for seeding.
- Command registry has 5/10 slots used — room for `update_sprint` (slot 6).

### Three Tracks

| Track | Priority | Scope | Days |
|-------|----------|-------|------|
| **A: Quick Fixes** | P0-P1 | F-192-05 settings singleton, CF-193-01 F401 cleanup, CF-193-02 inline imports, F-192-06 CI cache | Day 1 |
| **B: Infrastructure** | P1-P2 | F-192-07 Semgrep removal from runtime, F-PARITY-01/02/03 docs, CLAUDE.md update | Days 2-3 |
| **C: Agent Enrichment** | P2 | GAP-01 seed agents, GAP-02 team presets, ENR-01 update_sprint command, ENR-02 activity log, CF-193-03 integration test | Days 4-7 |

---

## Deliverables

| # | Deliverable | Description | LOC Delta | Day | Priority |
|---|-------------|-------------|-----------|-----|----------|
| 1 | Settings singleton fix | Replace `Settings()` → `settings` in `gates.py` L1690-1691 | ~-2 | 1 | P0 |
| 2 | F401 unused imports cleanup | Remove 5 unused imports from `planning.py` L57-77 | ~-5 | 1 | P1 |
| 3 | Inline imports refactor | Move Sprint 193 imports from try block to module level in `planning.py` L1317-1318 | ~+3/-2 | 1 | P1 |
| 4 | CI cache path fix | Update `test.yml` L70 + L167 cache-dependency-path to `backend/requirements/core.txt` | ~2 | 1 | P1 |
| 5 | Semgrep runtime removal | Remove Semgrep from Dockerfile builder stage (line 32); keep in CI job only | ~-2 | 2 | P1 |
| 6 | Docker image size verification | Build + measure image; target ≤600 MB after Semgrep removal | ~0 | 2 | P2 |
| 7 | Feature parity doc updates | Update F-PARITY-01 (Zalo HMAC done), F-PARITY-03 (validation count) | ~10 | 2 | P2 |
| 8 | CLAUDE.md Module 7 update | Add `magic_link_service.py` to Module 7 key files list | ~3 | 2 | P2 |
| 9 | Seed agent definitions migration | Alembic migration inserting 12 default `agent_definition` records from `ROLE_MODEL_DEFAULTS` | ~120 | 4 | P2 |
| 10 | `sdlcctl agents seed` CLI command | CLI command to re-seed agent definitions (idempotent, upsert by role) | ~80 | 4-5 | P2 |
| 11 | Team presets service | `team_presets.py` — 5 JSON presets (solo-dev, startup-2, enterprise-3, review-pair, full-sprint) | ~200 | 5-6 | P2 |
| 12 | `update_sprint` chat command | Register in command registry (slot 6/10), handler calls `SprintFileService.push_to_github()` | ~100 | 6 | P2 |
| 13 | Activity log append | Extend `team_orchestrator.py` — append conversation summary to sprint context | ~60 | 7 | P3 |
| 14 | Integration test (CF-193-03) | E2E test: `submit_gate_evaluation` → `auto_evaluate_checklist_item` → verify `auto_verified=True` | ~80 | 7 | P1 |
| 15 | Acceptance tests + sprint close | 10 acceptance tests + SPRINT-194-CLOSE.md | ~150 | 8 | P0 |

**Net LOC delta**: ~+800 (additions) — primarily agent enrichment features

---

## Resolved Findings (NO ACTION NEEDED)

These items from the original Sprint 193 backlog were investigated and found to be already resolved:

| ID | Finding | Status | Evidence |
|----|---------|--------|----------|
| F-192-03 | Deferred import in `_verify_zalo_signature()` | **RESOLVED** | Intentional lazy-load pattern, best practice per CLAUDE.md Section 5 |
| F-192-04 | Missing PA-69 empty-timestamp test | **RESOLVED** | Test exists at `test_zalo_normalizer.py:141-154`, covers valid + invalid empty timestamp |

---

## Daily Schedule

### Day 1: Quick Fixes (Track A — All P0-P1 Cleanup)

**Goal**: Close all code-level findings from Sprint 192 + Sprint 193 CTO carry-forwards.

#### P0 Fix: Settings singleton (5 min)

| File | Change |
|------|--------|
| `backend/app/api/routes/gates.py` L1690-1691 | Replace `from app.core.config import Settings` + `settings = Settings()` → `from app.core.config import settings` |

**Why P0**: Per-request `Settings()` instantiation re-parses env vars + regenerates secrets. Performance + correctness issue.

**Verification**: `grep -n "Settings()" backend/app/api/routes/gates.py` → 0 matches

#### P1 Fix: F401 unused imports (5 min)

| File | Change |
|------|--------|
| `backend/app/api/routes/planning.py` L57 | Remove `G_SPRINT_CHECKLIST_TEMPLATE` import |
| `backend/app/api/routes/planning.py` L58 | Remove `G_SPRINT_CLOSE_CHECKLIST_TEMPLATE` import |
| `backend/app/api/routes/planning.py` L69 | Remove `SprintAssistantService` import |
| `backend/app/api/routes/planning.py` L73 | Remove `BurndownService` import |
| `backend/app/api/routes/planning.py` L77 | Remove `ForecastService` import |

**Verification**: `ruff check backend/app/api/routes/planning.py` → 0 F401 errors

#### P1 Fix: Inline imports refactor (10 min)

| File | Change |
|------|--------|
| `backend/app/api/routes/planning.py` top-level imports | Add `from app.services.github_service import github_service` and `from app.services.sprint_verification_service import SprintVerificationService` |
| `backend/app/api/routes/planning.py` L1317-1318 | Remove the two inline imports from inside the try block |

**Note**: The try/except block around auto-verification (L1310-1334) must remain — only the imports move. The service instantiation and call stay inside the try block.

#### P1 Fix: CI cache path (5 min)

| File | Change |
|------|--------|
| `.github/workflows/test.yml` L70 | `cache-dependency-path: 'backend/requirements.txt'` → `cache-dependency-path: 'backend/requirements/core.txt'` |
| `.github/workflows/test.yml` L167 | Same change |

**Verification**: `grep "requirements.txt" .github/workflows/test.yml` → 0 matches (only `requirements/core.txt`)

**Day 1 Verification**:
- `ruff check backend/app/api/routes/gates.py backend/app/api/routes/planning.py` → 0 errors
- `grep -n "Settings()" backend/app/api/routes/gates.py` → 0 matches
- `grep "requirements.txt" .github/workflows/test.yml | grep -v "core.txt"` → 0 matches
- All existing tests still pass

---

### Day 2-3: Infrastructure (Track B — Docker + Documentation)

**Goal**: Remove Semgrep from runtime image, verify image size, update feature parity docs.

#### Day 2: Semgrep + Docker (2 hrs)

| File | Change |
|------|--------|
| `backend/Dockerfile` L31-32 | Remove `RUN pip install --no-cache-dir --prefix=/install semgrep` from builder stage |
| `backend/Dockerfile` | Verify `COPY --from=builder /install /usr/local` (L46) no longer copies Semgrep |

**Why**: Semgrep is only needed for CI SAST jobs, not for FastAPI runtime. Removing it:
- Reduces image size by ~200-300 MB (target ≤600 MB total)
- Removes unnecessary tooling from production attack surface
- Semgrep CI step (Sprint 192, `test.yml`) already runs SAST independently

**Verification**:
```bash
docker build -t sdlc-backend:test -f backend/Dockerfile backend/
docker images sdlc-backend:test --format "{{.Size}}"  # Target ≤600 MB
docker run --rm sdlc-backend:test semgrep --version  # Should fail (not installed)
```

**Rollback**: If any service actually needs Semgrep at runtime (unlikely), keep `Dockerfile.full` as fallback.

#### Day 3: Documentation Updates (1 hr)

| File | Change |
|------|--------|
| Feature parity comparison doc | F-PARITY-01: Update Zalo HMAC status → "Implemented Sprint 192 ✅" |
| Feature parity comparison doc | F-PARITY-03: Clarify "14 validation files" → "8 root `.py` + 2 subdirs (`consistency/` + `validators/`)" |
| `CLAUDE.md` Module 7 key files | F-PARITY-02: Add `magic_link_service.py` (~11 KB) entry under Multi-Agent Team Engine |

**Day 2-3 Verification**:
- Docker image ≤600 MB
- `semgrep --version` fails in runtime container
- Feature parity doc has no "pending" references to Sprint 192
- `grep "magic_link_service" CLAUDE.md` → 1+ match

---

### Days 4-5: Agent Seed Definitions + CLI (Track C, Part 1)

**Goal**: Seed 12 default agent definitions from `ROLE_MODEL_DEFAULTS` and create CLI seed command.

#### Day 4: Alembic Seed Migration (3 hrs)

New file: `backend/alembic/versions/s194_001_seed_agent_defs.py`

**Approach**: Insert 12 records using values from `config.py:ROLE_MODEL_DEFAULTS`:

| Role | Provider | Model | SE4H? |
|------|----------|-------|-------|
| researcher | ollama | qwen3:32b | No |
| pm | ollama | qwen3:32b | No |
| pjm | ollama | qwen3:14b | No |
| architect | ollama | deepseek-r1:32b | No |
| coder | ollama | qwen3-coder:30b | No |
| reviewer | ollama | deepseek-r1:32b | No |
| tester | ollama | qwen3-coder:30b | No |
| devops | ollama | qwen3:14b | No |
| ceo | anthropic | claude-opus-4-6 | **Yes** |
| cpo | anthropic | claude-sonnet-4-5 | **Yes** |
| cto | anthropic | claude-opus-4-6 | **Yes** |
| assistant | ollama | qwen3:14b | No |

**Key columns per record**: `agent_name`, `sdlc_role`, `provider`, `model`, `queue_mode="queue"`, `session_scope="per-sender"`, `max_delegation_depth=1`, `allowed_tools=["*"]`, `temperature=0.7`, `max_tokens=4096`, `is_active=true`.

SE4H roles (ceo/cpo/cto) get `allowed_tools=[]` and `max_delegation_depth=0` per ADR-056 non-negotiable #3.

**Migration must be idempotent**: Use `INSERT ... ON CONFLICT (agent_name) DO NOTHING` or check existence before insert.

#### Day 5: `sdlcctl agents seed` CLI Command (2 hrs)

| File | Change |
|------|--------|
| `backend/sdlcctl/` (CLI module) | Add `agents seed` subcommand |
| Implementation | Read `ROLE_MODEL_DEFAULTS` from config, upsert into `agent_definitions` table |

**Idempotent**: Running `sdlcctl agents seed` twice produces same result (upsert by `sdlc_role`).

**Days 4-5 Verification**:
```bash
# Run migration
alembic upgrade head

# Verify 12 records
psql -c "SELECT agent_name, sdlc_role, provider, model FROM agent_definitions ORDER BY sdlc_role;"
# Expected: 12 rows

# Run CLI seed (idempotent)
sdlcctl agents seed
# Expected: "12 agent definitions seeded (0 new, 12 existing)"
```

---

### Days 5-6: Team Presets (Track C, Part 2)

**Goal**: Create 5 named team presets for common SDLC team configurations.

New file: `backend/app/services/agent_team/team_presets.py` (~200 LOC)

**5 Presets**:

| Preset Name | Roles | Use Case |
|-------------|-------|----------|
| `solo-dev` | coder | Single developer working alone |
| `startup-2` | coder, reviewer | Small team with code review |
| `enterprise-3` | architect, coder, reviewer | Standard enterprise dev team |
| `review-pair` | reviewer, tester | Quality-focused review pair |
| `full-sprint` | pm, architect, coder, reviewer, tester, devops | Full SDLC sprint team |

**Implementation**:

```python
TEAM_PRESETS: dict[str, TeamPresetConfig] = {
    "solo-dev": TeamPresetConfig(
        name="solo-dev",
        description="Single developer working alone",
        roles=["coder"],
        delegation_chain=[],
    ),
    # ...
}
```

Each preset includes:
- `name`: Preset identifier
- `description`: Human-readable description (English + Vietnamese)
- `roles`: List of `sdlc_role` values to include
- `delegation_chain`: Who delegates to whom (e.g., `[("pm", "coder"), ("coder", "reviewer")]`)
- `default_queue_mode`: `"queue"` (default) or `"steer"`

**API Endpoint**: `GET /api/v1/agent-team/presets` — list available presets (no CRUD needed, presets are code-defined constants).

**Days 5-6 Verification**:
```bash
# Unit test
python -m pytest backend/tests/unit/ -k "team_preset" -v

# API endpoint
curl -s localhost:8000/api/v1/agent-team/presets | jq '.[] | .name'
# Expected: ["solo-dev", "startup-2", "enterprise-3", "review-pair", "full-sprint"]
```

---

### Day 6: `update_sprint` Chat Command (Track C, Part 3)

**Goal**: Register `update_sprint` as command slot 6/10 in the governance command registry.

#### Command Registration

| File | Change |
|------|--------|
| `backend/app/services/agent_team/command_registry.py` L35-72 | Add `UpdateSprintParams` Pydantic model |
| `backend/app/services/agent_team/command_registry.py` L79-86 | Add `UPDATE_SPRINT` to `ToolName` enum |
| `backend/app/services/agent_team/command_registry.py` L133-204 | Add 6th `CommandDef` to `GOVERNANCE_COMMANDS` |

**UpdateSprintParams**:
```python
class UpdateSprintParams(BaseModel):
    status_note: Optional[str] = Field(None, max_length=500, description="Optional status update note")
```

**CommandDef**:
```python
CommandDef(
    name="update_sprint",
    description="Update CURRENT-SPRINT.md with latest sprint status",
    params=UpdateSprintParams,
    permission="planning:write",
    handler="sprint_file_service.push_to_github",
    cli_name="update-sprint",
    ott_description="Update CURRENT-SPRINT.md file. Use when user says 'cập nhật sprint', 'update sprint file', etc.",
    ott_aliases=("cập nhật sprint", "update sprint", "update sprint file"),
    required_params=(),
)
```

#### Command Handler

New file: `backend/app/services/agent_team/sprint_command_handler.py` (~100 LOC)

**Flow**:
1. Get active sprint for current project from DB
2. Generate CURRENT-SPRINT.md via `SprintFileService.generate_current_sprint_md()`
3. Push to GitHub via `SprintFileService.push_to_github()`
4. Return confirmation with commit SHA and diff summary

**Day 6 Verification**:
```bash
# Slot count
python -c "from app.services.agent_team.command_registry import GOVERNANCE_COMMANDS; print(len(GOVERNANCE_COMMANDS))"
# Expected: 6

# Command exists
python -c "from app.services.agent_team.command_registry import get_command; print(get_command('update_sprint').cli_name)"
# Expected: update-sprint
```

---

### Day 7: Activity Log + Integration Test (Track C, Part 4)

**Goal**: Add activity log append pattern and close CF-193-03 integration test gap.

#### Activity Log Append (ENR-02, ~60 LOC)

| File | Change |
|------|--------|
| `backend/app/services/agent_team/team_orchestrator.py` | Add `_log_sprint_activity()` private method |

**Implementation**: After each agent conversation completion, append a summary line to the sprint's JSONB metadata field (or a dedicated `sprint_activities` key in the Sprint model's `metadata` column). Used by `SprintFileService` when generating CURRENT-SPRINT.md.

```python
async def _log_sprint_activity(self, conversation_id: UUID, project_id: UUID, summary: str):
    """Append conversation summary to sprint activity log (TinySDLC pattern)."""
    sprint = await self._get_active_sprint(project_id)
    if not sprint:
        return
    activities = sprint.metadata_.get("activities", []) if sprint.metadata_ else []
    activities.append({
        "conversation_id": str(conversation_id),
        "summary": summary,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    # Keep last 50 activities to prevent unbounded growth
    sprint.metadata_ = {**(sprint.metadata_ or {}), "activities": activities[-50:]}
    await self.db.flush()
```

#### Integration Test for CF-193-03 (~80 LOC)

New file: `backend/tests/integration/test_sprint_auto_verify.py`

**Test**: `test_submit_g_sprint_close_gate_with_auto_verify()`

1. Create Sprint + Project + SprintGateEvaluation with real `G_SPRINT_CLOSE_CHECKLIST_TEMPLATE`
2. Mock `github_service.get_file_content()` to return file with correct sprint reference
3. Call `POST /api/v1/planning/sprints/{id}/gates/g_sprint_close/submit`
4. Assert: `current_sprint_updated` item has `passed=True`, `auto_verified=True`, `verification_reason="current"`
5. Assert: `current_sprint_fresh` item has `passed=True`, `auto_verified=True`

**Day 7 Verification**:
```bash
# Integration test
python -m pytest backend/tests/integration/test_sprint_auto_verify.py -v
# Expected: 1/1 passed

# Activity log
python -m pytest backend/tests/unit/ -k "sprint_activity" -v
```

---

### Day 8: Acceptance Tests + Sprint Close

**Goal**: Run full acceptance suite, write SPRINT-194-CLOSE.md.

**10 Acceptance Tests**:

| # | Test | Criterion |
|---|------|-----------|
| 1 | `grep "Settings()" backend/app/api/routes/gates.py` → 0 | Settings singleton enforced |
| 2 | `ruff check backend/app/api/routes/planning.py` → 0 F401 | Unused imports cleaned |
| 3 | `grep "requirements.txt" .github/workflows/test.yml \| grep -v core` → 0 | CI cache paths correct |
| 4 | Docker image ≤600 MB | Semgrep removed from runtime |
| 5 | `SELECT count(*) FROM agent_definitions` → 12 | Seed agents populated |
| 6 | `sdlcctl agents seed` returns success (idempotent) | CLI seed works |
| 7 | `GET /api/v1/agent-team/presets` returns 5 presets | Team presets available |
| 8 | Command registry has 6/10 slots used | `update_sprint` registered |
| 9 | Integration test `test_sprint_auto_verify.py` passes | CF-193-03 closed |
| 10 | `grep "magic_link_service" CLAUDE.md` → 1+ match | F-PARITY-02 closed |

---

## New Files

| File | LOC | Purpose | Day |
|------|-----|---------|-----|
| `backend/alembic/versions/s194_001_seed_agent_defs.py` | ~120 | Seed 12 default agent definitions | 4 |
| `backend/app/services/agent_team/team_presets.py` | ~200 | 5 named team preset configurations | 5-6 |
| `backend/app/services/agent_team/sprint_command_handler.py` | ~100 | `update_sprint` command handler | 6 |
| `backend/tests/integration/test_sprint_auto_verify.py` | ~80 | CF-193-03: submit + auto-verify integration test | 7 |
| `backend/tests/unit/test_sprint194_acceptance.py` | ~150 | 10 acceptance tests | 8 |

## Modified Files

| File | Change | LOC Delta | Day |
|------|--------|-----------|-----|
| `backend/app/api/routes/gates.py` L1690-1691 | Settings singleton fix | -2 | 1 |
| `backend/app/api/routes/planning.py` L57-77, L1317-1318 | Remove 5 F401 imports + refactor inline imports | -5/+3 | 1 |
| `.github/workflows/test.yml` L70, L167 | CI cache path fix | ~2 | 1 |
| `backend/Dockerfile` L31-32 | Remove Semgrep from builder | -2 | 2 |
| `CLAUDE.md` Module 7 | Add `magic_link_service.py` | +3 | 2 |
| Feature parity comparison doc | F-PARITY-01, F-PARITY-03 updates | ~10 | 3 |
| `backend/app/services/agent_team/command_registry.py` | Add `update_sprint` command (slot 6/10) | ~30 | 6 |
| `backend/app/services/agent_team/chat_command_router.py` | Wire `update_sprint` tool | ~15 | 6 |
| `backend/app/services/agent_team/team_orchestrator.py` | Activity log append | ~60 | 7 |

---

## Risk Register

| Risk | Prob | Impact | Mitigation | Day |
|------|------|--------|------------|-----|
| Semgrep removal breaks runtime SAST scan feature | LOW | HIGH | Verify no route calls Semgrep at runtime (CI-only since Sprint 192) | 2 |
| Seed migration conflicts with existing agent_definitions | LOW | MEDIUM | Use `ON CONFLICT DO NOTHING`; idempotent | 4 |
| team_presets.py requires DB table changes | LOW | LOW | Code-only presets (JSON constants, no new table) | 5 |
| `update_sprint` command conflicts with planning.py endpoint | LOW | LOW | Chat command calls SprintFileService, not the REST endpoint | 6 |

---

## Definition of Done

- [ ] `Settings()` per-request eliminated in `gates.py` (F-192-05)
- [ ] 5 F401 unused imports removed from `planning.py` (CF-193-01)
- [ ] Inline imports moved to module level in `planning.py` (CF-193-02)
- [ ] CI cache paths use `backend/requirements/core.txt` (F-192-06)
- [ ] Docker image ≤600 MB, no Semgrep in runtime (F-192-07)
- [ ] CLAUDE.md Module 7 lists `magic_link_service.py` (F-PARITY-02)
- [ ] Feature parity doc updated (F-PARITY-01, F-PARITY-03)
- [ ] 12 seed agent definitions in DB (GAP-01)
- [ ] `sdlcctl agents seed` CLI command works (GAP-01)
- [ ] 5 team presets available via API (GAP-02)
- [ ] `update_sprint` chat command registered, slot 6/10 (ENR-01)
- [ ] Activity log append per agent conversation (ENR-02)
- [ ] Integration test for submit + auto-verify passes (CF-193-03)
- [ ] 10 acceptance tests pass
- [ ] `ruff check` clean on all modified files
- [ ] G-Sprint-Close within 24h of sprint end
- [ ] CURRENT-SPRINT.md updated to COMPLETED on close

---

## Scope

### In-Scope

**Track A** (Day 1 — Quick Fixes):
- F-192-05: Settings singleton
- CF-193-01: F401 cleanup
- CF-193-02: Inline imports refactor
- F-192-06: CI cache path

**Track B** (Days 2-3 — Infrastructure):
- F-192-07: Semgrep removal from runtime Docker
- F-PARITY-01/02/03: Documentation updates
- CLAUDE.md Module 7 update

**Track C** (Days 4-7 — Agent Enrichment):
- GAP-01: Seed agent definitions + CLI
- GAP-02: Team presets service
- ENR-01: `update_sprint` chat command
- ENR-02: Activity log append
- CF-193-03: Integration test

### Out-of-Scope (Resolved — No Action)

- F-192-03: Deferred import in `_verify_zalo_signature()` — intentional pattern, no fix needed
- F-192-04: PA-69 empty-timestamp test — already exists and passes

### Deferred to Sprint 195+

- EP-06 Codegen Quality Gates hardening
- Vietnamese SME Pilot Prep (3 founding customers)
- Ollama `qwen3-coder:30b` integration testing

---

## Handoff to @dev Team

**Execution order**: Day 1 (Track A) → Days 2-3 (Track B) → Days 4-7 (Track C) → Day 8 (close)

**Day 1 can be parallelized**:
- Developer A: `gates.py` Settings fix + `planning.py` cleanup
- Developer B: `test.yml` CI cache fix

**Critical path**: Day 4 (seed migration) → Day 5 (CLI + presets) → Day 6 (update_sprint command uses seed agents)

**Track B and C are independent** — Documentation updates (Track B) can proceed in parallel with Agent Enrichment (Track C).

---

**Sprint 194 Status**: APPROVED — Ready for @dev team execution
**GO/NO-GO**: GO
