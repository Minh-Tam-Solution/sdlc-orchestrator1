# Current Sprint: Sprint 194 — Security Hardening + Agent Enrichment

**Sprint Duration**: February 24 – March 7, 2026 (10 working days)
**Sprint Goal**: Resolve all carried Sprint 192 findings (F-192-03 through F-192-07), close feature-parity gaps (agent seed definitions, team presets), and complete Sprint 193 deferred items (update_sprint chat command, activity log, planning.py cleanup)
**Status**: PLANNED
**Priority**: P1 (Security + Automation Quality)
**Framework**: SDLC 6.1.1
**CTO Score (Sprint 193)**: 9.1/10 — APPROVED
**Previous Sprint**: [Sprint 193 COMPLETE — CURRENT-SPRINT.md Platform Enforcement](SPRINT-193-CURRENT-SPRINT-ENFORCEMENT.md)
**Detailed Plan**: [SPRINT-194-SECURITY-AGENT-ENRICHMENT.md](SPRINT-194-SECURITY-AGENT-ENRICHMENT.md)

---

## Sprint 194 Goal

Sprint 193 was re-scoped to deliver CURRENT-SPRINT.md Platform Enforcement (CEO directive). The original Sprint 193 backlog (F-192-03 through F-192-07, GAP-01, GAP-02) carries forward, combined with Sprint 193 CTO carry-forwards (3 items) and deferred Phase 6-7 from the enforcement plan.

**Conversation-First** (CEO directive Sprint 190): All sprint governance flows through OTT+CLI. Web App = admin-only.

---

## Sprint 194 Backlog — Ordered by Priority

### P1 — Security (carried from Sprint 193)

| ID | Finding | File | Action |
|----|---------|------|--------|
| F-192-05 | `settings = Settings()` instantiated per-request | `backend/app/api/routes/gates.py` L1691-1692 | Replace with module-level singleton import: `from app.core.config import settings` |

### P1 — Sprint 193 CTO Carry-Forwards

| ID | Finding | File | Action |
|----|---------|------|--------|
| CF-193-01 | 5 pre-existing F401 unused imports in planning.py | `backend/app/api/routes/planning.py` | Remove unused imports (`G_SPRINT_CHECKLIST_TEMPLATE`, `SprintAssistantService`, `BurndownService`, `ForecastService`, `G_SPRINT_CLOSE_CHECKLIST_TEMPLATE`) |
| CF-193-02 | Inline imports inside try block (non-standard) | `backend/app/api/routes/planning.py` L1318 | Move `github_service` and `SprintVerificationService` imports to module level |
| CF-193-03 | Missing integration test for submit + auto-verify path | `backend/tests/integration/` | Add E2E test: `submit_gate_evaluation` → `auto_evaluate_checklist_item` → `finalize_evaluation` |

### P2 — Reliability & Documentation (carried from Sprint 193)

| ID | Finding | File | Action |
|----|---------|------|--------|
| F-192-06 | CI cache-dependency-path stale after requirements split | `.github/workflows/test.yml` L70, L167 | Change `backend/requirements.txt` → `backend/requirements/core.txt` |
| F-PARITY-02 | `magic_link_service.py` missing from CLAUDE.md Module 7 | `CLAUDE.md` Module 7 key files list | Add entry (file is ~11 KB, confirmed present in `agent_team/`) |
| F-PARITY-01 | Parity doc Zalo HMAC status "pending Sprint 192" is stale | Feature parity comparison doc | Update: Zalo SHA256 implemented Sprint 192 |

### P2 — Agent Enrichment (deferred from Sprint 193 Phase 6-7)

| ID | Item | Action |
|----|------|--------|
| ENR-01 | `update_sprint` chat command | New `sprint_command_handler.py` — register in command registry (slot 6/10), wire into `chat_command_router.py` |
| ENR-02 | Activity log append per agent conversation | Extend `team_orchestrator.py` — append conversation summary to sprint activity context |

### P2 — Feature Parity (carried from Sprint 193)

| ID | Gap | Action |
|----|-----|--------|
| GAP-01 | No seed agent definitions for SDLC 6.1.1 roles | Alembic migration seeding 12 `agent_definition` records (Initializer, Coder, Reviewer...) + `sdlcctl agents seed` command |
| GAP-02 | No named team presets | Add `backend/app/services/agent_team/team_presets.py` — 5 JSON presets (solo-dev, startup-2, enterprise-3, review-pair, full-sprint) |

### P3 — Quality & Verification (carried from Sprint 193)

| ID | Finding | File | Action |
|----|---------|------|--------|
| F-192-07 | Semgrep in runtime Docker image — verify <600MB | `backend/Dockerfile` | Build + measure; if >600 MB move Semgrep to CI-only |
| F-192-04 | Missing empty-timestamp edge case test (PA-69) | `backend/tests/unit/test_zalo_normalizer.py` | Add `test_verify_signature_empty_timestamp()` |
| F-192-03 | Deferred import inside `_verify_zalo_signature()` | `backend/app/api/routes/ott_gateway.py` L128 | Move to module-level once circular-import concern confirmed clear |
| F-PARITY-03 | "14 validation files" count unclear in parity doc | Feature parity comparison doc | Clarify: 8 root `.py` + 2 subdirs (`consistency/` + `validators/`) |

---

## Sprint 194 Success Criteria

- [ ] `settings = Settings()` per-request eliminated — singleton pattern throughout `gates.py`
- [ ] 5 F401 unused imports removed from `planning.py`
- [ ] Integration test for `submit_gate_evaluation` + `auto_evaluate_checklist_item` path
- [ ] `test.yml` L70 + L167 cache paths updated to `backend/requirements/core.txt`
- [ ] CLAUDE.md Module 7 lists `magic_link_service.py`
- [ ] `update_sprint` chat command registered and functional
- [ ] `sdlcctl agents seed` command operational with 12 agent definitions
- [ ] `team_presets.py` with 5 presets committed
- [ ] Docker image size confirmed ≤600 MB (or Semgrep moved to CI)
- [ ] PA-69 empty-timestamp test added, all Zalo tests pass
- [ ] `ruff check` 0 errors on all modified files
- [ ] G-Sprint-Close within 24h of sprint end

---

## Previous Sprint Summary

### Sprint 193 — CURRENT-SPRINT.md Platform Enforcement (COMPLETE — 9.1/10)

**Duration**: 1 working day (February 22, 2026) · **Tests**: 45/45 passing

Sprint 193 was re-scoped from "Security Hardening & Automation" to "CURRENT-SPRINT.md Platform Enforcement" per CEO directive: *"Platform must enforce CURRENT-SPRINT.md on ALL governed customer projects."*

| # | Deliverable | LOC |
|---|-------------|-----|
| 0a | Project model `github_repo` + `default_branch` properties | ~20 |
| 0b | GitHub Service — 3 missing methods (`get_file_content`, `update_file`, `create_update_pr`) | ~220 |
| 0c | Serializer field fix (`passed` vs `checked` mismatch) | ~10 |
| 1 | SprintFileService — template generation + GitHub push + freshness check | ~474 |
| 2 | DynamicContextService — push CURRENT-SPRINT.md on sprint events | ~40 |
| 3 | Team Orchestrator — sprint context injection into agent prompts | ~85 |
| 4 | SprintVerificationService — auto-verify G-Sprint-Close checklist items | ~228 |
| 5 | G-Sprint gate enhancement — 3 `auto_verify: True` checklist items | ~15 |
| T | Tests (3 files, 45 tests) | ~1,168 |

**Key achievements**:
- Fixed P0 bug: `github_service.py` missing 3 methods — AGENTS.md push was dead code since inception
- Fixed P0 bug: `planning.py` serializer read `checked` instead of `passed` — gate completion % was always 0%
- CURRENT-SPRINT.md now auto-generated from Sprint DB and pushed to customer GitHub repos
- G-Sprint-Close checklist items auto-verified via GitHub API (replaces manual checkbox)

**CTO carry-forwards**: 3 items (F401 cleanup, inline imports, integration test)

**Full report**: [SPRINT-193-CURRENT-SPRINT-ENFORCEMENT.md](SPRINT-193-CURRENT-SPRINT-ENFORCEMENT.md)

---

## Recent Sprint History (Quick Reference)

| Sprint | Theme | Status | CTO Score |
|--------|-------|--------|-----------|
| 193 | CURRENT-SPRINT.md Platform Enforcement | COMPLETE ✅ | 9.1/10 |
| 192 | Enterprise Hardening | COMPLETE ✅ | 9.0/10 |
| 191 | Unified Command Registry | COMPLETE ✅ | 8.9/10 |
| 190 | Conversation-First Cleanup (~47K LOC deleted) | COMPLETE ✅ | 9.1/10 |
| 189 | Chat Governance Loop | COMPLETE ✅ | 9.4/10 |
| 188 | GA Launch | COMPLETE ✅ | Gate G4 APPROVED |

*Full history: [SPRINT-INDEX.md](SPRINT-INDEX.md)*

---

## Sprint 195 Preview (Tentative)

**Theme**: EP-06 Codegen Quality Gates + Vietnamese SME Pilot Prep
**Scope**: 4-Gate Quality Pipeline hardening, Ollama `qwen3-coder:30b` integration testing, 3 founding-customer onboarding flows
**Depends on**: Sprint 194 F-192-05 fix (settings singleton before gate engine changes)

---

## G-Sprint Gate Status

| Gate | Status | Notes |
|------|--------|-------|
| G-Sprint (Sprint 194 start) | ⏳ PENDING | Must be evaluated before Day 1 work begins |
| G-Sprint-Close (Sprint 193) | ✅ PASSED | CTO 9.1/10, 3 carry-forwards logged |

**Rule 9 (Documentation Freeze = Sprint Freeze)**: CURRENT-SPRINT.md updated February 22, 2026.
Next update due: Sprint 194 Day 1 (change Status → ACTIVE) and Sprint 194 close (change Status → COMPLETED).

---

**Last Updated**: February 22, 2026
**Updated By**: PM — Sprint 193 Close + Sprint 194 Planning
**Framework Version**: SDLC 6.1.1
**Previous State**: Sprint 193 PLANNED (original backlog deferred to Sprint 194)
