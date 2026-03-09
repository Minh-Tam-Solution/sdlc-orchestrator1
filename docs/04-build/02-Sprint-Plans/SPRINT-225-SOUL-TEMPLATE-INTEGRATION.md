---
sdlc_version: "6.1.2"
document_type: "Sprint Plan"
status: "APPROVED — CTO Conditionally Approved (B1-B3 addressed)"
sprint: "225"
tier: "PROFESSIONAL"
stage: "04 - Build"
---

# Sprint 225 — SOUL Template Integration

| Field            | Value |
|------------------|-------|
| Sprint Duration  | March 2026 |
| Sprint Goal      | Load rich SOUL templates into agent system prompts, enforce tier-based role filtering, add 5 missing roles, wire ContextInjector into TeamOrchestrator |
| Status           | APPROVED — CTO Conditionally Approved (B1-B3 addressed) |
| Priority         | P1 — Agent Quality (SOUL templates differentiate SDLC Orchestrator agents from generic LLM calls) |
| Framework        | SDLC 6.1.2 |
| Previous Sprint  | Sprint 224 — Auto-Generation Quality Gates |
| Dependency       | SDLC-Enterprise-Framework submodule at 6.1.2 (17 SOULs + 10 TEAMs committed) |
| Raised by        | PM + Architect gap audit (2026-03-09) |
| CTO Review       | CONDITIONALLY APPROVED — 3 blocking items addressed below |

---

## Context

Framework 6.1.2 added 17 SOUL role templates (2.7-13.5KB each) and 10 TEAM charters to Ring 2 (`04-SASE-Artifacts/souls/` and `teams/`). These define rich role personas with Identity, Capabilities, Constraints, Communication Patterns, and Gate Responsibilities.

However, the Orchestrator's Multi-Agent Team Engine (EP-07) seeds agents with **basic 1-sentence system prompts** (24-160 chars) in `agent_seed_service.py`. Gap audit identified 5 critical issues — this sprint closes the top 4.

---

## Root Cause

`AgentSeedService` uses hardcoded `_ROLE_PROMPTS` dict with minimal descriptions like "You are a developer assistant..." while Framework SOUL templates contain 2.7-13.5KB of behavioral rules (Design-First Gate, Zero Mock Policy, TDD Workflow, tier-aware coverage targets).

The `ContextInjector` (built Sprints 216-221, 7 dynamic sections) exists but is **not wired** into `team_orchestrator._build_llm_context()`. Additionally, only 12 of 17 Framework roles are seeded (missing fullstack + 4 optional), and no tier-based filtering prevents LITE projects from spawning all 13 roles.

---

## CTO Review — Blocking Items (All Addressed)

### B1: Token budget underestimate — ADDRESSED

**Problem**: Plan claimed "extracted SOUL content ~800-2000 tokens" but SOUL-tester is 13.5KB (~3,375 tokens raw).

**Resolution**: `get_system_prompt()` has explicit `max_chars=6000` parameter (~1,500 tokens). Extracts sections in priority order until budget exhausted. Logs `WARNING` when SOUL content exceeds threshold.

**Revised token budget**:
| Component | Tokens |
|-----------|--------|
| Extracted SOUL content (capped) | ~1,500 |
| SYSTEM_PROMPT_TEMPLATE wrapper | ~100 |
| Sprint context + agent notes | ~500 |
| ContextInjector (7 sections) | ~5,000-6,000 |
| **Total** | **~7,100-8,100** |

### B2: Missing Alembic migration — NOT NEEDED

**Verification**: `sdlc_role` column is `String(20)` (free VARCHAR), NOT a PostgreSQL enum type. No migration required. All new role names fit within 20 chars: "fullstack"(9), "writer"(6), "sales"(5), "cs"(2), "itadmin"(7).

### B3: SE4A auto-expansion security — ADDRESSED

**Problem**: Adding 5 roles to `SDLCRole` enum auto-expands `SE4A_ROLES` via `set(SDLCRole) - SE4H_ROLES - ROUTER_ROLES`. Support roles (writer, sales, cs, itadmin) would inherit `allowed_tools=["*"]` and `can_spawn_subagent=True`.

**Resolution**: Define `SUPPORT_ROLES` frozenset in `agent_team.py`. Update `SE4A_ROLES` computation to exclude support roles. Support roles get restricted permissions (similar to SE4H but with `max_delegation_depth=1`):
```python
SUPPORT_ROLES = frozenset({SDLCRole.WRITER, SDLCRole.SALES, SDLCRole.CS, SDLCRole.ITADMIN})
SE4A_ROLES = frozenset(set(SDLCRole) - SE4H_ROLES - ROUTER_ROLES - SUPPORT_ROLES)
```

Support role constraints in seed service:
```python
SUPPORT_CONSTRAINTS = {
    "allowed_tools": ["read_file", "search", "analyze", "write_file"],
    "denied_tools": ["execute_command", "spawn_agent", "approve_gate"],
    "can_spawn_subagent": False,
    "max_delegation_depth": 1,
}
```

---

## CTO Recommendations — All Addressed

### R1: OPTIONAL_ROLES location → `agent_team.py` schemas (alongside SE4H_ROLES, ROUTER_ROLES)

### R2: Section extraction flexibility → Priority-based extraction with `max_chars` budget

`get_system_prompt()` extracts all `## ` sections in order, accumulates until `max_chars` exhausted. Role-specific sections (Design-First Gate, Zero Mock Policy) are included naturally by position. No hardcoded 4-section filter.

### R3: TEAM charter vs presets → Charters supplement presets, don't replace

TeamCharterLoader provides metadata (mission, leader_role, member_roles) that enriches existing team presets. Presets remain the operational mechanism; charters add context for display and documentation.

### R4: Backward compat for default seeding → `tier=None` defaults to all 12 core roles

`seed_project_agents(project_id, tier=None)` seeds all 12 core roles (existing behavior). Tier filtering only applies when `tier` is explicitly passed. Existing tests and callers unaffected.

---

## Design Decision: Option C — SOUL as base + ContextInjector on top

**Decision**: SOUL template content becomes `definition.system_prompt` stored in DB on seed. ContextInjector appends 7 dynamic sections on every LLM call.

**Rationale**:
- Static persona (SOUL) vs dynamic runtime context (ContextInjector) — clean separation
- SOUL content extracted with `max_chars=6000` budget (~1,500 tokens)
- Total estimated: ~7,100-8,100 tokens — well within 128K+ context windows
- Fallback: if SOUL file missing, use existing basic `_ROLE_PROMPTS`

**System prompt assembly order**:
```
1. SYSTEM_PROMPT_TEMPLATE (agent name, role, session scope)
2. definition.system_prompt (SOUL content — from DB)
3. Compaction summary (if conversation compressed)
4. Sprint context (current sprint plan)
5. Agent notes (cross-session memory)
6. <system_context> (7 ContextInjector sections)
```

---

## Deliverables

### S225-01: SOULLoaderService (~200 LOC)

**CREATE**: `backend/app/services/agent_team/soul_loader.py`

Reads SOUL markdown files from Framework submodule, parses YAML frontmatter + markdown body, extracts sections with token budget control, caches in memory.

**Key classes/functions**:
- `SOULTemplate` dataclass: role, category, version, sdlc_stages, sdlc_gates, sections (dict of heading → content), raw_content
- `SOULLoaderService`:
  - `__init__(base_path: Path | None = None)` — defaults to `settings.FRAMEWORK_SUBMODULE_PATH / "05-Templates-Tools/04-SASE-Artifacts/souls"`
  - `load_all() -> dict[str, SOULTemplate]` — scans `SOUL-*.md`, parses each
  - `get_system_prompt(role: str, max_chars: int = 6000) -> str | None` — extracts sections in order until budget exhausted. Returns `None` if file missing (caller falls back to basic prompt)
  - `get_tier_roles(tier: str) -> frozenset[str]` — returns roles available at given tier
- Parse YAML frontmatter via `yaml.safe_load()` between `---` markers
- Parse markdown sections via `## ` heading split — preserves all sections including role-specific ones (Design-First Gate, Zero Mock Policy, etc.)
- Module-level `_soul_cache: dict[str, SOULTemplate] = {}` populated on first access
- Add `FRAMEWORK_SUBMODULE_PATH: str = "SDLC-Enterprise-Framework"` to `backend/app/core/config.py`

**CTO B1 compliance**: `max_chars=6000` parameter + `WARNING` log when truncated.

### S225-02: TeamCharterLoader (~80 LOC)

**CREATE**: `backend/app/services/agent_team/team_charter_loader.py`

Lighter loader for TEAM charters. Extracts metadata for team preset enrichment (R3: supplements, doesn't replace presets).

- `TeamCharter` dataclass: team, archetype, version, mission, leader_role, member_roles
- `TeamCharterLoader` with `load_all()` and `load_team(name: str)`
- Same cache pattern as soul_loader

### S225-03: Extend SDLCRole + ROLE_MODEL_DEFAULTS (+5 roles, ~60 LOC)

**MODIFY**: 3 files

**`backend/app/schemas/agent_team.py`** — Add 5 enum values + SUPPORT_ROLES:
```python
# SE4A — autonomous AI agents
FULLSTACK = "fullstack"       # Full-stack developer (SE4A)
# Support — restricted permissions (non-SDLC, OPTIONAL tier)
WRITER = "writer"
SALES = "sales"
CS = "cs"
ITADMIN = "itadmin"

SUPPORT_ROLES = frozenset({SDLCRole.WRITER, SDLCRole.SALES, SDLCRole.CS, SDLCRole.ITADMIN})
SE4A_ROLES = frozenset(set(SDLCRole) - SE4H_ROLES - ROUTER_ROLES - SUPPORT_ROLES)
```

**`backend/app/services/agent_team/config.py`** — Add 5 entries to `ROLE_MODEL_DEFAULTS`:
```python
"fullstack": {"provider": "ollama", "model": "qwen3-coder:30b"},
"writer": {"provider": "ollama", "model": "qwen3:32b"},
"sales": {"provider": "ollama", "model": "qwen3:14b"},
"cs": {"provider": "ollama", "model": "qwen3:14b"},
"itadmin": {"provider": "ollama", "model": "qwen3:14b"},
```

**`backend/app/services/agent_team/agent_seed_service.py`** — Add 5 entries to `_ROLE_PROMPTS` and `_ROLE_MAX_TOKENS` (basic fallbacks):
```python
"fullstack": "You are an SDLC Full-Stack Developer agent...",
"writer": "You are an SDLC Documentation Writer agent...",
"sales": "You are an SDLC Sales Engineer agent...",
"cs": "You are an SDLC Customer Service agent...",
"itadmin": "You are an SDLC IT Administrator agent...",
```

**CTO B3 compliance**: `SUPPORT_ROLES` excluded from `SE4A_ROLES`. Support constraints applied in seed service.

### S225-04: Tier-Aware Agent Seeding (~100 LOC)

**MODIFY**: `backend/app/services/agent_team/agent_seed_service.py`

Replace basic `_ROLE_PROMPTS` with SOUL template content and add tier-based filtering.

- Add `tier: str | None = None` parameter to `seed_project_agents()`
- `tier=None` seeds all 12 core roles (backward compat — R4)
- Tier-to-roles mapping:
  ```
  LITE:         assistant, coder, tester (3)
  STANDARD:     + pm, architect, reviewer (6)
  PROFESSIONAL: + devops, fullstack, pjm, researcher (10)
  ENTERPRISE:   + ceo, cpo, cto (13)
  ```
  OPTIONAL roles (writer, sales, cs, itadmin) never auto-seeded.
- Call `soul_loader.get_system_prompt(role, max_chars=6000)` — use SOUL content if available, fall back to `_ROLE_PROMPTS[role]` if not
- Store `{"soul_version": "1.0.0", "soul_source": "framework"}` in `config` JSONB field
- Apply `SUPPORT_CONSTRAINTS` for support roles (B3 compliance)

### S225-05: Wire ContextInjector into TeamOrchestrator (~30 LOC)

**MODIFY**: `backend/app/services/agent_team/team_orchestrator.py`

Connect existing `ContextInjector.inject_context()` to `_build_llm_context()` (line 609).

- Import `ContextInjector` at module top
- Instantiate `self._context_injector = ContextInjector(db)` in `__init__`
- Call after sprint context + agent notes (after line 660):
  ```python
  system_prompt = await self._context_injector.inject_context(
      agent_id=definition.id,
      team_id=definition.team_id,
      system_prompt=system_prompt,
      project_id=conversation.project_id,
      conversation_id=conversation.id,
  )
  ```

### S225-06: Seed Caller Integration (~40 LOC)

**MODIFY**: `backend/app/api/routes/agent_team.py`

- Add optional `tier: str | None = Query(None)` param to seed endpoint
- Pass to `svc.seed_project_agents(project_id, team_id=team_id, tier=tier)`
- Add `POST /api/v1/agent-team/definitions/reseed` endpoint:
  - Accepts `project_id` and `tier`
  - Calls `seed_project_agents(project_id, tier=tier, skip_existing=True)`
  - Returns count of newly seeded agents

### S225-07: Unit Tests (~250 LOC)

| Test File | Action | Tests | LOC |
|-----------|--------|-------|-----|
| `backend/tests/unit/test_soul_loader.py` | CREATE | load_all (17), parse frontmatter, extract sections, get_system_prompt with max_chars, truncation warning, fallback for missing, get_tier_roles, cache | ~120 |
| `backend/tests/unit/test_team_charter_loader.py` | CREATE | load_all (10), parse leader/members | ~40 |
| `backend/tests/unit/test_agent_seed_service.py` | MODIFY | tier=None seeds 12, LITE seeds 3, STANDARD 6, PRO 10, ENTERPRISE 13, SOUL prompt used, fallback works, support role constraints, optional not seeded | ~60 |
| `backend/tests/unit/test_agent_team_config.py` | MODIFY | 17 SDLCRole values, SUPPORT_ROLES defined, SE4A_ROLES excludes support | ~20 |
| `backend/tests/unit/test_team_orchestrator.py` | MODIFY | _build_llm_context calls inject_context | ~10 |

---

## Key Files

| File | Action | Deliverable |
|------|--------|-------------|
| `backend/app/services/agent_team/soul_loader.py` | CREATE | S225-01 |
| `backend/app/services/agent_team/team_charter_loader.py` | CREATE | S225-02 |
| `backend/app/schemas/agent_team.py` | MODIFY | S225-03 |
| `backend/app/services/agent_team/config.py` | MODIFY | S225-03 |
| `backend/app/services/agent_team/agent_seed_service.py` | MODIFY | S225-03, S225-04 |
| `backend/app/services/agent_team/team_orchestrator.py` | MODIFY | S225-05 |
| `backend/app/api/routes/agent_team.py` | MODIFY | S225-06 |
| `backend/app/core/config.py` | MODIFY | S225-01 |
| `backend/app/services/agent_team/context_injector.py` | READ ONLY | S225-05 |
| `SDLC-Enterprise-Framework/05-Templates-Tools/04-SASE-Artifacts/souls/` | READ ONLY | S225-01 |
| `SDLC-Enterprise-Framework/05-Templates-Tools/04-SASE-Artifacts/teams/` | READ ONLY | S225-02 |

---

## Implementation Sequence

```
S225-01 (SOULLoader)          ← No deps, start immediately
S225-02 (TeamCharterLoader)   ← No deps, parallel with S225-01
S225-03 (SDLCRole +5)         ← No deps, parallel with S225-01/02
S225-05 (ContextInjector Wire) ← No deps, parallel
                ↓
S225-04 (Tier-Aware Seeding)  ← Depends on S225-01 + S225-03
                ↓
S225-06 (Seed Caller)         ← Depends on S225-04
S225-07 (Tests)               ← Written alongside each deliverable
```

---

## Dependencies & Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Framework submodule not initialized | Medium | `soul_loader` checks path existence, logs warning, falls back to basic prompts |
| Existing tests assert `len(created) == 12` | High | `tier=None` default preserves 12-role behavior (R4) |
| Token budget overflow | Medium | `max_chars=6000` cap + WARNING log (B1) |
| Support roles inherit SE4A permissions | Blocked→Fixed | `SUPPORT_ROLES` frozenset + restricted constraints (B3) |
| `sdlc_role` VARCHAR(20) size | None | All new names fit: max "fullstack"=9 chars |

---

## Estimates

| Metric | Value |
|--------|-------|
| Production LOC | ~510 (280 new + 230 modified) |
| Test LOC | ~250 |
| Total LOC | ~760 |
| Test target | 95%+ coverage on new code |

---

## Verification

1. **Unit tests**: `python -m pytest backend/tests/unit/test_soul_loader.py backend/tests/unit/test_team_charter_loader.py backend/tests/unit/test_agent_seed_service.py -v` — all green
2. **Backward compat**: `seed_project_agents(project_id)` (no tier) → 12 agents created
3. **Tier filtering**: Seed LITE → 3 agents. Seed ENTERPRISE → 13 agents
4. **SOUL content**: `system_prompt` contains SOUL Identity+Constraints (not 1-sentence)
5. **Token budget**: No role exceeds 6,000 chars in extracted SOUL content
6. **Support role security**: writer/sales/cs/itadmin get restricted `allowed_tools` (B3)
7. **ContextInjector wired**: `_build_llm_context()` output includes `<system_context>` block
8. **Fallback**: Rename SOUL file → agent gets basic prompt
9. **Regression**: `python -m pytest backend/tests/unit/ -k "agent_seed or agent_team" -v` — all pass
