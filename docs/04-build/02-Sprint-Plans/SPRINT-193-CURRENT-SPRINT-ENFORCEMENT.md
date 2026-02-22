---
sdlc_version: "6.1.1"
document_type: "Sprint Plan"
status: "COMPLETE"
sprint: "193"
spec_id: "SPRINT-193"
tier: "ALL"
stage: "04 - Build"
cto_review: "9.1/10 APPROVED"
reviewer_audit: "Implementation Plan Review (2026-02-22)"
---

# Sprint 193 — CURRENT-SPRINT.md Platform Enforcement

**Status**: COMPLETE (implementation done, sprint plan backfilled)
**Duration**: 1 working day (February 22, 2026)
**Goal**: Enforce CURRENT-SPRINT.md maintenance on all governed projects as a platform feature — automated generation from DB, GitHub push, auto-verification in G-Sprint-Close gates
**Epic**: EP-08 Chat-First Governance Loop (Sprint Governance Automation)
**CEO Directive**: "Platform must enforce CURRENT-SPRINT.md on ALL governed customer projects, not just Orchestrator's own repo"
**ADR**: N/A — extends existing DynamicContextService + G-Sprint gate patterns
**Preceded by**: Sprint 192 (Enterprise Hardening, CTO 9.0/10)
**Budget**: ~$640 (8 hrs @ $80/hr)
**Reference**: TinySDLC v1.2.0 context maintenance plan (~170 LOC, 7 files)

---

## Context

SDLC 6.1.1 mandates that all project members (AI and Human) maintain `CURRENT-SPRINT.md` as the single source of sprint truth. Before this sprint, the Orchestrator:

- Stored sprint data ONLY in the database (`Sprint` model, 33 tables)
- Had `G-Sprint-Close` checklist with `current_sprint_updated` item — but it was a **manual checkbox** with no automated verification
- Had **no mechanism** to read/write `CURRENT-SPRINT.md` in customer project repos
- `DynamicContextService` generated `AGENTS.md` overlays from DB data but referenced `github_service.update_file()` and `create_update_pr()` — methods that **did not exist** (dead code since inception)
- Team Orchestrator built agent context WITHOUT sprint awareness

### Pre-Existing Bugs Discovered During Review

1. **`github_service.py` missing 3 methods** — `update_file()`, `get_file_content()`, `create_update_pr()` were called by `DynamicContextService` (lines 775, 784) but never implemented. AGENTS.md push to GitHub was dead code.
2. **`checked` vs `passed` field mismatch** — Checklist templates use `"passed": None` but the serializer in `planning.py` read `item.get("checked", False)`, making gate completion percentage always 0%.

### Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Sprint context source | DB-first (Option C) | Sprint DB is truth; `CURRENT-SPRINT.md` is a generated artifact, same as `AGENTS.md` |
| File update mechanism | GitHub API commit (Option A) | Mirrors existing `AGENTS.md` push pattern in `DynamicContextService`; `Project` model already has `github_repo_full_name` |
| G-Sprint-Close verification | GitHub API check + auto_verify flag | Automated file freshness check via GitHub API; replaces manual checkbox |
| GitHub repo field | Property delegation pattern | `project.github_repo` delegates to `GitHubRepository` relationship with fallback to `github_repo_full_name` column |

---

## Deliverables

| # | Deliverable | Description | LOC | Phase | Priority |
|---|-------------|-------------|-----|-------|----------|
| 0a | Project model properties | `github_repo` + `default_branch` delegation properties | ~20 | 0 | P0 |
| 0b | GitHub Service — 3 missing methods | `get_file_content()`, `update_file()`, `create_update_pr()` using `_make_request()` | ~220 | 0 | P0 |
| 0c | Serializer field fix | `planning.py` — change `item.get("checked")` → `item.get("passed")` | ~10 | 0 | P0 |
| 1 | SprintFileService | Template generation from Sprint DB + GitHub push + freshness check | ~474 | 1 | P1 |
| 2 | DynamicContextService sprint push | Push `CURRENT-SPRINT.md` alongside `AGENTS.md` on sprint events | ~40 | 2 | P1 |
| 3 | Sprint context injection | Inject sprint name/goal/days/gate status into agent system prompts | ~85 | 3 | P2 |
| 4 | SprintVerificationService | Auto-verify `G-Sprint-Close` checklist items via GitHub API | ~228 | 4 | P1 |
| 5 | G-Sprint gate enhancement | Add `auto_verify: True` flags to 3 checklist items | ~15 | 5 | P1 |
| T | Tests (3 files) | Phase 0 tests (16) + file service tests (19) + verification tests (10) | ~1,168 | All | P0 |

**Total**: ~2,260 LOC (source + tests) | **Tests**: 45/45 passing | **ruff**: clean

---

## Phase Breakdown

### Phase 0: Pre-Existing Bug Fixes (P0 — Blockers)

**Phase 0a: Project Model Properties** — `project.py`

Added `github_repo` and `default_branch` properties to the `Project` model, delegating to `GitHubRepository` (Sprint 129, ADR-044) relationship with fallback to legacy `github_repo_full_name` column.

| File | Change |
|------|--------|
| `backend/app/models/project.py` (L287-304) | `@property github_repo` → delegates to `GitHubRepository.full_name`, fallback to `github_repo_full_name` |
| `backend/app/models/project.py` (L299-304) | `@property default_branch` → delegates to `GitHubRepository.default_branch`, fallback to `"main"` |

**Phase 0b: GitHub Service Extension** — `github_service.py`

Added 3 methods that `DynamicContextService` referenced but were never implemented:

| Method | Lines | API | Pattern |
|--------|-------|-----|---------|
| `get_file_content()` | 595-649 | `GET /repos/{owner}/{repo}/contents/{path}` | `_make_request()`, returns decoded content dict, handles 404 |
| `update_file()` | 651-716 | `PUT /repos/{owner}/{repo}/contents/{path}` | `_make_request()`, base64 encodes content, supports `sha` for optimistic locking |
| `create_update_pr()` | 718-811 | 4-step: get base ref → create branch → commit → create PR | `_make_request()` × 3 + `update_file()` |

**Phase 0c: Serializer Field Fix** — `planning.py`

| File | Change |
|------|--------|
| `backend/app/api/routes/planning.py` (L1368) | `item.get("checked", False)` → `item.get("passed") is True` |

**Why P0**: Both bugs blocked the entire sprint's deliverables — GitHub Service methods are prerequisite for all phases, serializer fix is prerequisite for `auto_verify` to work.

---

### Phase 1: Sprint File Service (P1 — Core Feature)

New file: `backend/app/services/sprint_file_service.py` (474 LOC)

| Method | Purpose |
|--------|---------|
| `generate_current_sprint_md(sprint, project, previous_sprint)` | Generates markdown from Sprint DB record — 7 sections: header, goal, backlog table, success criteria, gate status, previous sprint summary, footer with Rule 9 timestamp |
| `push_to_github(project, content, path)` | Commits `CURRENT-SPRINT.md` to project's GitHub repo via `github_service.update_file()`. Guards for missing `github_repo`. Uses GitHub App installation token. |
| `verify_freshness(project, sprint, path)` | Checks if `CURRENT-SPRINT.md` in repo references the correct sprint number. Returns `{fresh, reason, sprint_match, file_exists, sha}` |
| `get_active_sprint(project_id)` | Query active sprint with backlog relationships |

**Error handling**: Returns `None` for projects without GitHub repos (guard at L120-125). Catches `GitHubAPIError` and logs without crashing (L153-159).

---

### Phase 2: DynamicContextService Sprint Push (P1)

Modified: `backend/app/services/dynamic_context_service.py`

Extended `_on_sprint_change()` to also push `CURRENT-SPRINT.md` when sprint state changes. Reuses existing `_push_to_github()` infrastructure — added `_push_current_sprint_md()` method that calls `SprintFileService.push_to_github()`.

**Trigger points** (same as existing AGENTS.md push):
- Sprint created/activated (G-Sprint pass)
- Sprint status changed (PLANNED → ACTIVE → COMPLETED)
- Sprint backlog modified
- G-Sprint-Close submitted

---

### Phase 3: Sprint Context Injection (P2 — Agent Enrichment)

Modified: `backend/app/services/agent_team/team_orchestrator.py` (L493-577)

Added sprint context injection into `_build_llm_context()`:

```python
# L493-496: Injection point (after compaction summary, before history)
sprint_context = await self._get_sprint_context(conversation.project_id)
if sprint_context:
    system_prompt += f"\n\n## Current Sprint Context\n{sprint_context}"
```

New private method `_get_sprint_context(project_id)` (L524-577):
- Queries active `Sprint` for project
- Formats: sprint name, goal, status, days remaining, key backlog items, gate status
- Returns `None` if no active sprint or `project_id` is `None` (NULL guard)
- Exception handler logs warning and returns `None` (graceful fallback)

---

### Phase 4: Sprint Verification Service (P1 — Gate Automation)

New file: `backend/app/services/sprint_verification_service.py` (228 LOC)

| Method | Purpose |
|--------|---------|
| `verify_sprint_close_docs(sprint, project)` | 3-check verification: file exists in repo, references correct sprint number, project has GitHub repo. Returns `VerificationResult` dataclass. |
| `auto_evaluate_checklist_item(evaluation, sprint, project)` | Scans checklist for items with `auto_verify: True`. Auto-evaluates 3 items: `current_sprint_md_exists`, `current_sprint_updated`, `current_sprint_fresh`. Sets `passed`, `auto_verified`, `verification_reason` on each. |

**Integration**: Wired into `planning.py` `submit_gate_evaluation()` (L1309-1333) — called BEFORE `finalize_evaluation()` so auto-results affect pass/fail. Wrapped in `try/except` for best-effort (doesn't block on failure).

---

### Phase 5: G-Sprint Gate Enhancement (P1)

Modified: `backend/app/models/sprint_gate_evaluation.py`

Added `auto_verify: True` flag to 3 checklist items:

| Template | Item ID | Label | auto_verify |
|----------|---------|-------|-------------|
| G-Sprint | `current_sprint_md_exists` | CURRENT-SPRINT.md exists in repo | `True` (L71) |
| G-Sprint-Close | `current_sprint_updated` | CURRENT-SPRINT.md updated | `True` (L101) |
| G-Sprint-Close | `current_sprint_fresh` | CURRENT-SPRINT.md updated within 24h (Rule 9) | `True` (L102) |

---

## New Files

| File | LOC | Purpose |
|------|-----|---------|
| `backend/app/services/sprint_file_service.py` | 474 | Template generation + GitHub push + freshness check |
| `backend/app/services/sprint_verification_service.py` | 228 | Auto-verify G-Sprint-Close checklist items |
| `backend/tests/unit/test_sprint193_phase0.py` | 361 | Phase 0 bug fix tests (16 tests) |
| `backend/tests/unit/test_sprint_file_service.py` | 418 | Sprint file service tests (19 tests) |
| `backend/tests/unit/test_sprint_verification_service.py` | 389 | Verification service tests (10 tests) |

## Modified Files

| File | Change | LOC Delta |
|------|--------|-----------|
| `backend/app/models/project.py` | `github_repo` + `default_branch` properties | +20 |
| `backend/app/services/github_service.py` | `get_file_content`, `update_file`, `create_update_pr` | +220 |
| `backend/app/api/routes/planning.py` | Serializer fix (`passed` vs `checked`), auto-verification wiring | +30 |
| `backend/app/services/dynamic_context_service.py` | `_push_current_sprint_md()`, fixed `_push_to_github()` | +40 |
| `backend/app/services/agent_team/team_orchestrator.py` | Sprint context injection into agent prompts | +85 |
| `backend/app/models/sprint_gate_evaluation.py` | `auto_verify` flags on 3 checklist items | +15 |

---

## Risk Register

| Risk | Prob | Impact | Mitigation | Status |
|------|------|--------|------------|--------|
| GitHub App token not available for customer repos | MEDIUM | HIGH | Guard returns `None`, sprint file push is best-effort | MITIGATED |
| `auto_verify` fails during G-Sprint-Close | LOW | MEDIUM | Wrapped in `try/except`, manual checklist still works | MITIGATED |
| Sprint context bloats agent system prompt | LOW | LOW | Context is ~10 lines, well under token limits | ACCEPTED |
| `create_update_pr()` branch naming collision | LOW | LOW | Uses timestamp-based branch names | ACCEPTED |

---

## Verification Criteria

| # | Criterion | Target | Result |
|---|-----------|--------|--------|
| 1 | All unit tests pass | 45/45 | PASS |
| 2 | ruff check clean | 0 errors | PASS |
| 3 | `github_service.get_file_content()` uses `_make_request()` | Line 627 | PASS |
| 4 | `github_service.update_file()` uses `_make_request()` | Line 706 | PASS |
| 5 | `github_service.create_update_pr()` uses `_make_request()` | Lines 753, 767, 795 | PASS |
| 6 | Serializer reads `"passed"` not `"checked"` | `planning.py` L1368 | PASS |
| 7 | `SprintFileService.push_to_github()` guards for missing `github_repo` | L120-125 | PASS |
| 8 | `_get_sprint_context()` has NULL guard for `project_id` | L550-551 | PASS |
| 9 | `auto_evaluate_checklist_item()` handles 3 item types | L199, L212, L219 | PASS |
| 10 | `submit_gate_evaluation` calls verification before finalization | L1309-1333 | PASS |

---

## Definition of Done

- [x] `github_service.py` has `get_file_content()`, `update_file()`, `create_update_pr()` (AGENTS.md push no longer dead code)
- [x] `planning.py` serializer reads `passed` field (gate completion % now accurate)
- [x] `SprintFileService` generates markdown from Sprint DB and pushes to GitHub
- [x] `DynamicContextService` pushes `CURRENT-SPRINT.md` on sprint change events
- [x] Team Orchestrator injects sprint context into agent system prompts
- [x] `SprintVerificationService` auto-verifies G-Sprint-Close checklist items
- [x] 3 checklist items have `auto_verify: True` flag
- [x] 45/45 tests passing, ruff clean
- [x] Sprint plan backfilled (this document)
- [x] CURRENT-SPRINT.md updated
- [x] SPRINT-INDEX.md updated

---

## Scope

### In-Scope

- GitHub Service missing methods (pre-existing bug fix)
- Serializer field mismatch (pre-existing bug fix)
- Sprint file generation, push, and verification
- Agent prompt sprint context injection
- G-Sprint gate auto-verification

### Out-of-Scope

- `sprint_command_handler.py` (chat command `update_sprint`) — deferred to Sprint 194
- Activity log append (TinySDLC pattern) — deferred to Sprint 194
- Redis caching for sprint context (not needed at current scale)
- Sprint 193 original backlog (F-192-05 settings singleton, CI cache fix, agent seed definitions) — deferred, to be re-prioritized

### Deferred to Sprint 194+

- Chat command `update_sprint` (Phase 6 from original plan, uses 1 of 5 remaining command registry slots)
- Activity log append per agent conversation (Phase 7 from original plan)
- Original Sprint 193 backlog items (F-192-03 through F-192-07, GAP-01, GAP-02)

---

## Sprint 194 Preview (Tentative)

**Theme**: Original Sprint 193 Backlog + Agent Enrichment
**Scope**: F-192-05 settings singleton, CI cache fix, agent seed definitions, team presets, `update_sprint` chat command, activity log append
**Depends on**: Sprint 193 GitHub Service methods (now available)

---

**Sprint 193 Status**: COMPLETE — Implementation done, sprint plan backfilled
**Tests**: 45/45 passing
**ruff**: Clean
**Ready for CTO Review**: YES
