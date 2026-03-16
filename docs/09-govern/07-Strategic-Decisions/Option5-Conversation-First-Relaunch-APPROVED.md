# Strategic Decision: Option 5 — Conversation-First Relaunch

**Document Status:** ✅ APPROVED (CEO + CTO + CPO)
**Date:** March 16, 2026
**Authors:** PM + Architect + CPO
**Reviewers:** CTO (5 required changes), CEO (final approval)
**Framework:** SDLC 6.1.2 — Pillar 7 (Govern)
**Sprint:** 226+ (execution begins)
**Supersedes:** Option 1-4 analysis (same date)

---

## Executive Summary

### Decision

**SDLC Orchestrator pivots to Conversation-First Relaunch (Option 5).** Giữ full codebase (230K LOC, 579 endpoints), chuyển interface chính sang OTT+CLI cho actions, web app cho visualization/admin. Hybrid collaboration model: agents hỗ trợ (LITE) → agents tự chủ (ENTERPRISE).

### Context

Sau 225+ sprints, SDLC Orchestrator có codebase mature (8.2/10 health score) nhưng chưa có commercial customer. 4 options được phân tích:

| Option | Description | Verdict |
|--------|-------------|---------|
| 1. Continue as-is | Tiếp tục 579 endpoints full platform | ❌ Go-to-market failure, không phải engineering failure |
| 2. New Product | Port unique IP sang Go/TypeScript | ❌ 10-14 weeks rewrite, lặp lại lỗi estimate lạc quan |
| 3. Sunset | Archive, focus Bflow/MTClaw | ❌ Write-off $564K investment + 90K LOC unique IP |
| 4. Radical Scope Cut | Xóa 70% commodity code | ❌ Dependency audit: 10/19 target files là hard deps. Risk cao |
| **5. Conversation-First** | **Giữ code, chuyển interface** | **✅ APPROVED** |

### Why Option 5

CEO clarified: SDLC Orchestrator = **hiện thực hoá SDLC Framework**, giúp phát triển ứng dụng liền mạch, phối hợp giữa team members và agents. Planning, Gates, Evidence, Agents, Team Coordination đều là CORE — không phải commodity.

Vấn đề không phải scope quá rộng. Vấn đề là **chưa có customer validation** và **interface strategy chưa đúng cho audience**.

---

## Part 1: 5 CTO Required Changes — APPROVED

### Change 1: Reframe Thesis

| Before | After |
|--------|-------|
| "OTT is primary interface" | **"Conversation-first for action, web for visualization/admin"** |

**Rationale:** Chat excels at triggers, approvals, status, @mentions. Chat fails at backlog visualization, dependency management, audit browsing, dense comparative views. Reframed thesis is more honest and sustainable.

**Week 1 validation must answer:**
1. What tasks do users want via chat? (gate approval, code gen trigger, status check)
2. What tasks do users NOT want via chat? (backlog planning, evidence browsing, audit)
3. At what complexity threshold do they switch to visual interface?

**Files to update:** `CLAUDE.md`, `AGENTS.md`, ADR-064 positioning sections.

---

### Change 2: 4 Fixed Autonomy Presets (Not 16 Combinations)

```yaml
LITE       → assist_only       # Agent suggests, human executes everything
STANDARD   → contribute_only   # Agent executes code, human approves gates
PRO        → member_guardrails # Agent autonomous except G3/G4 gates
ENTERPRISE → autonomous_gated  # Full autonomy, human approves G3/G4 only
```

**v1 rule: Tier maps 1:1 to preset. No custom autonomy matrix per org.**

**Rationale:** Original plan had 4 tiers × 4 autonomy levels = 16 combinations. CPO audit found actual policy space is 6 tiers × 5 presets × 14+ fields = exponentially larger. Fixed presets eliminate policy bug minefield.

**Implementation:**
- Add `autonomy_level` column to `agent_definitions` (DEFAULT `'assist'`)
- `compute_gate_actions()` respects autonomy preset
- Validation: reject custom autonomy rules at API level in v1

**Alembic:** `s226_001_add_autonomy_level.py` — `ALTER TABLE ADD COLUMN ... DEFAULT 'assist'` (zero-downtime safe)

---

### Change 3: Surface Reduction Program (Telemetry, Not Deletion)

Option 5 means "don't delete yet" but NOT "maintain equally."

**Day 1 endpoint labels:**

| Label | Description | Action |
|-------|-------------|--------|
| `ACTIVE_PRIMARY` | Conversation workflows, core gates, evidence | Active investment |
| `ACTIVE_ADMIN` | Admin dashboard, user mgmt, RBAC | Keep stable |
| `LEGACY_SUPPORTED` | Existing API consumers still hitting it | Monitor |
| `LEGACY_UNUSED` | Zero hits after 4 weeks | Candidate for deprecation |

**Implementation:**
- Lightweight middleware counter per route group
- `Redis INCR` on `route_hits:{path}:{date}`
- Weekly report
- After 4-6 weeks pilot → data-driven deprecation decisions

**Existing infrastructure to extend:**
- `backend/app/utils/deprecation.py` — RFC 8594 headers + async telemetry queue (already exists)
- `backend/app/utils/deprecation_monitoring.py` — tracking API (already exists)
- **Gap:** endpoint hit rate tracking, label system

---

### Change 4: Telegram-Only for v1

**Rule:** Zalo only if Week 1 survey shows >60% of target users say Telegram is a hard blocker. Otherwise, Telegram-only through pilot.

**Rationale:**
- `telegram_normalizer.py` + `telegram_responder.py` — production-ready (Sprint 178)
- `zalo_normalizer.py` — exists but untested in production
- Opening Zalo kills timeline (2+ weeks hardening)

**Implementation:** Add `FEATURE_FLAG_ZALO_OTT=false` in config. Zalo normalizer guarded by flag.

---

### Change 5: Product Metrics Replace Delivery Metrics

| Metric | Minimum Threshold | Measurement |
|--------|-------------------|-------------|
| Conversation completion rate | ≥ 70% | Workflow started via chat AND completed without unplanned web fallback |
| Human override rate | ≤ 30% at STANDARD tier | % of agent actions overridden by human |
| Time-to-gate improvement | ≥ 40% faster | Time from "evaluate gate" to approved/rejected vs baseline |
| Pilot retention | 3/3 active end of Week 2 | User returns to conversation workflow after first week |

**Kill signal:** If completion rate <50% OR retention <2/3 after Week 2 → stop and reassess thesis.

**Baseline required:** Collect time-to-gate metrics from existing `gates` table (`evaluated_at` → `approved_at`) BEFORE pilot begins.

---

## Part 2: Hybrid Collaboration Model — APPROVED

```
┌──────────┬──────────────┬────────────────────┬──────────────────────┐
│ Tier     │ Team Setup   │ Agent Role         │ Governance           │
├──────────┼──────────────┼────────────────────┼──────────────────────┤
│ LITE     │ 1-2 humans   │ assist_only        │ Agents suggest,      │
│          │ 3 agents     │ @coder helps       │ humans decide ALL    │
├──────────┼──────────────┼────────────────────┼──────────────────────┤
│ STANDARD │ 3-5 humans   │ contribute_only    │ Agents execute code, │
│          │ 6 agents     │ @coder PRs         │ humans approve gates │
├──────────┼──────────────┼────────────────────┼──────────────────────┤
│ PRO      │ 5-15 humans  │ member_guardrails  │ Agents auto G1/G2,  │
│          │ 10 agents    │ @pm plans          │ humans approve G3/G4 │
├──────────┼──────────────┼────────────────────┼──────────────────────┤
│ ENTERPRISE│ 15+ humans  │ autonomous_gated   │ Full autonomy,       │
│          │ 13 agents    │ Full SDLC lifecycle│ humans override only │
└──────────┴──────────────┴────────────────────┴──────────────────────┘
```

**Non-negotiable:** Magic Link required for G3/G4 gate approval regardless of tier (security).

---

## Part 3: 5 Core Conversation Workflows — APPROVED

| # | Workflow | Chat Trigger | Agents | Human Touchpoint |
|---|---------|-------------|--------|------------------|
| 1 | Project Init | "@assistant tạo project HRM" | @assistant → @pm → @architect | PM approve scope |
| 2 | Sprint Planning | "@pm plan sprint 3" | @pm decompose → @coder estimate | PM approve backlog |
| 3 | Code Generation | "@coder implement user auth" | @coder → @reviewer (reflection) → @tester | Dev review + merge |
| 4 | Gate Evaluation | "@assistant evaluate gate G2" | @assistant collect → evaluate → submit | CTO/CPO Magic Link |
| 5 | Bug Fix | "@coder fix JWT expiry bug" | @coder → @reviewer → @tester | Dev merge |

**Reflection loop (LangGraph):** Only for Workflow 3 (Code Generation) and complex Workflow 5 (Bug Fix). NOT for status checks or gate triggers.

---

## Part 4: Execution Timeline — APPROVED

```
Week 1:    Customer interviews (10 SME users, PM leads)
           + Design 5 conversation workflows (sequence diagrams)
           + Collect time-to-gate baseline metrics
Week 2:    Finalize workflow design + autonomy matrix
           + Implement telemetry labels (Surface Reduction Day 1)
Week 3-4:  Backend: command_registry expansion (MAX_COMMANDS=20),
           autonomy_level migration, gate integration, X-Source middleware
Week 5-6:  OTT enrichment (planning+evidence+gate commands via Telegram)
           + ConversationFirstGuard update (source-aware routing)
           ── HARD FREEZE (no new features after Week 6) ──
Week 7-8:  Frontend admin-only transformation
           + Conversation analytics dashboard
           + Bug fixes only
Week 9:    Internal pilot (MTClaw team uses Orch for own development)
Week 10:   External pilot (3 Vietnamese SME partners)
```

**Team:** 4 FTE (2 backend, 1 frontend, 1 PM doing customer development full-time)

**Hard freeze rules (after Week 6):**
- Bug fix only. No "minor enhancements."
- No new team presets
- No new autonomy fields on agent_definition
- No new watched endpoints in UsageLimitsMiddleware
- PM enforces.

---

## Part 5: Exit Criteria — APPROVED

### Success Criteria (Week 10)

- [ ] ≥3 external pilot users actively using @mention workflows
- [ ] All 255 existing test files pass
- [ ] 5 conversation workflows working end-to-end
- [ ] Hybrid collaboration matrix enforced per tier (4 presets)
- [ ] Magic Link gate approval working via Telegram
- [ ] Admin-only web dashboard live
- [ ] Conversation completion rate ≥ 70%
- [ ] Human override rate ≤ 30% at STANDARD tier
- [ ] Time-to-gate improvement ≥ 40% vs baseline

### Kill Criteria (Week 2 of pilot)

- [ ] Conversation completion rate < 50% → STOP, reassess thesis
- [ ] Pilot retention < 2/3 after first week → STOP, reassess thesis

---

## Part 6: Codebase Audit Summary

### What We Have (verified by code audit March 16, 2026)

| Metric | Value |
|--------|-------|
| Backend LOC | 230,066 |
| API endpoints | 579 |
| Service files | 252 |
| SQLAlchemy models | 102 |
| Alembic migrations | 101 |
| Test files | 255 (133K LOC) |
| Test-to-code ratio | 58% |
| Health score | 8.2/10 |
| Zero Mock compliance | 93% |
| AGPL containment | ✅ Verified (boto3, not minio SDK) |

### Multi-Agent Engine (EP-07) — Unique IP

| Component | LOC | Status |
|-----------|-----|--------|
| Core engine (12 files) | 5,157 | ✅ Production-ready |
| Valuable features (14 files) | 5,567 | ✅ Competitive moat |
| Convenience (19 files) | 5,040 | ⚠️ Keep, low priority |
| **Total** | **15,764** | 44 files, 3 DB tables |

### Competitive Differentiation

| Feature | SDLC Orch | LangChain | CrewAI | AutoGen |
|---------|-----------|-----------|--------|---------|
| SDLC-stage-aware context | ✅ | ❌ | ❌ | ❌ |
| Gate approval via chat | ✅ | ❌ | ❌ | ❌ |
| Per-conversation budget | ✅ | ❌ | ❌ | ❌ |
| Durable workflow checkpoint | ✅ | ⚠️ | ❌ | ❌ |
| Provider failover (6 reasons) | ✅ | ⚠️ | ⚠️ | ❌ |
| Evidence capture (SHA256) | ✅ | ❌ | ❌ | ❌ |
| Input sanitization (12 patterns) | ✅ | ❌ | ❌ | ❌ |

---

## Part 7: Open CEO Decisions

| # | Decision | PM Recommendation |
|---|----------|-------------------|
| 1 | Product name | Giữ "SDLC Orchestrator" (brand equity từ 225 sprints) |
| 2 | Primary OTT channel | Telegram v1 (Zalo only if survey >60% blocker) |
| 3 | Team allocation | 4 FTE from current 8.5 — remaining to Bflow/MTClaw |
| 4 | Pricing | Pilot free → paid after 3 months validation |

---

## Approval Record

| Role | Name | Date | Decision |
|------|------|------|----------|
| PM | — | 2026-03-16 | ✅ APPROVED with 4 conditions (interviews, freeze, retention, team) |
| Architect | — | 2026-03-16 | ✅ APPROVED with 4 technical notes (MAX_COMMANDS, migration, Telegram-only, middleware) |
| CTO | — | 2026-03-16 | ✅ APPROVED with 5 required changes (thesis, presets, telemetry, channel, metrics) |
| CPO | — | 2026-03-16 | ✅ APPROVED — "verdict đúng, thực thi được, nên GO" |
| CEO | — | 2026-03-16 | ✅ APPROVED — Option 5 selected, hybrid collaboration model confirmed |

---

## References

- [ADR-064: Chat-First Facade Option D+](../../02-design/01-ADRs/ADR-064-Chat-First-Facade-Option-D-Plus.md)
- [ADR-056: Multi-Agent Team Engine](../../02-design/01-ADRs/ADR-056-Multi-Agent-Team-Engine.md)
- [ADR-059: Enterprise-First Refocus](../../02-design/01-ADRs/ADR-059-Enterprise-First-Refocus.md)
- [ADR-065: Unified Tier Resolution](../../02-design/01-ADRs/ADR-065-Unified-Tier-Resolution.md)
- [Sprint 190: Aggressive Cleanup](../../04-build/02-Sprint-Plans/SPRINT-190-AGGRESSIVE-CLEANUP.md)
- [Pre-Launch Strategic Response Jan 2026](PRE-LAUNCH-STRATEGIC-RESPONSE-JAN-2026.md)

---

**Document Version:** 1.0.0
**Last Updated:** March 16, 2026
**Next Review:** Week 2 of pilot (kill criteria check)
