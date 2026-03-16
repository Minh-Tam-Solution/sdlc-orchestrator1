---
sdlc_version: "6.1.2"
document_type: "Architecture Decision Record"
status: "APPROVED"
sprint: "226"
spec_id: "ADR-071"
tier: "ALL"
stage: "02 - Design"
owner: "CTO"
approved_by: "CEO + CTO + CPO"
approved_date: "2026-03-16"
supersedes: "Refines ADR-064 (Chat-First Facade)"
---

# ADR-071 — Option 5: Conversation-First Relaunch

**Status**: APPROVED (CEO + CTO + CPO, Mar 16, 2026)
**Sprint**: 226+
**Deciders**: CEO, CTO, CPO, PM, Architect
**Category**: Strategic Architecture + Interface Pivot + Collaboration Model
**Refines**: ADR-064 (Chat-First Facade — thesis reframed)
**Related**: ADR-056 (Multi-Agent), ADR-059 (Enterprise-First), ADR-064 (Chat-First), ADR-065 (Unified Tier)
**Triggers**: Option 5 strategic decision, 225+ sprint audit, PM/Architect/CPO review

---

## 1. Context

### 1.1 Triggering Event

After 225+ sprints (230K LOC, 579 endpoints, 102 models), SDLC Orchestrator has mature codebase (8.2/10 health score) but zero commercial customers. Four options were evaluated and rejected:

| Option | Why Rejected |
|--------|-------------|
| 1. Continue as-is | Go-to-market failure, not engineering failure |
| 2. New Product (rewrite) | 10-14 weeks minimum, repeats estimate optimism |
| 3. Sunset | Write-off $564K + 90K LOC unique IP |
| 4. Radical Scope Cut | Dependency audit: 10/19 target files are hard deps. Risk too high |

### 1.2 CEO Clarification

> "SDLC Orchestrator = hiện thực hoá SDLC Framework, giúp phát triển ứng dụng liền mạch, phối hợp giữa team members và agents."

Planning, Gates, Evidence, Agents, Team Coordination = ALL CORE. Not commodity. Problem is interface strategy + lack of customer validation, not scope.

### 1.3 ADR-064 Thesis Reframe

ADR-064 (Sprint 189) said "OTT+CLI primary, Web App admin-only." CTO review identified this as oversimplified:

| Before (ADR-064) | After (ADR-071) |
|-------------------|-----------------|
| "OTT is primary interface" | **"Conversation for action, web for visualization/admin"** |

Chat excels at: triggers, approvals, status checks, @mentions.
Chat fails at: backlog visualization, dependency management, audit browsing, dense comparative views.

---

## 2. Decision

### 2.1 Locked Decisions (5)

| # | Decision | Rationale |
|---|----------|-----------|
| D-071-01 | **Conversation for action, web for visualization** | Chat = triggers/approvals/status. Web = dashboards/audit/planning views. Neither is "primary" — each serves its strength. |
| D-071-02 | **4 fixed autonomy presets, tier-mapped 1:1** | LITE→assist_only, STANDARD→contribute_only, PRO→member_guardrails, ENTERPRISE→autonomous_gated. No custom matrix v1. |
| D-071-03 | **Telemetry-first deprecation** | Label all endpoints Day 1 (ACTIVE_PRIMARY/ACTIVE_ADMIN/LEGACY_SUPPORTED/LEGACY_UNUSED). Data-driven deletion after 4-6 weeks pilot. |
| D-071-04 | **Telegram-only v1** | Zalo deferred unless Week 1 survey >60% blocker. Slack/Teams deferred. |
| D-071-05 | **Product metrics over delivery metrics** | Measure completion rate, override rate, time-to-gate, retention. Kill signal defined. |

### 2.2 Hybrid Collaboration Matrix

```
┌──────────┬──────────────────┬──────────────────────────────────────┐
│ Tier     │ Autonomy Preset  │ Governance Rule                      │
├──────────┼──────────────────┼──────────────────────────────────────┤
│ LITE     │ assist_only      │ Agents suggest, humans execute ALL   │
│ STANDARD │ contribute_only  │ Agents execute code, humans approve  │
│ PRO      │ member_guardrails│ Agents auto G1/G2, humans G3/G4     │
│ ENTERPRISE│ autonomous_gated│ Full autonomy, humans override only  │
└──────────┴──────────────────┴──────────────────────────────────────┘
```

**Non-negotiable**: Magic Link required for G3/G4 regardless of tier.

### 2.3 5 Core Conversation Workflows

| # | Workflow | Trigger | Human Touchpoint |
|---|---------|---------|------------------|
| 1 | Project Init | "@assistant tạo project" | PM approve scope |
| 2 | Sprint Planning | "@pm plan sprint N" | PM approve backlog |
| 3 | Code Generation | "@coder implement X" | Dev review + merge |
| 4 | Gate Evaluation | "@assistant evaluate gate" | CTO/CPO Magic Link (G3/G4) |
| 5 | Bug Fix | "@coder fix bug" | Dev merge |

### 2.4 Surface Reduction Labels

| Label | Description | Action |
|-------|-------------|--------|
| ACTIVE_PRIMARY | Conversation workflows, gates, evidence | Active investment |
| ACTIVE_ADMIN | Admin dashboard, user mgmt, RBAC | Keep stable |
| LEGACY_SUPPORTED | Existing consumers still hitting it | Monitor |
| LEGACY_UNUSED | Zero hits after 4 weeks | Deprecation candidate |

Implementation: `Redis INCR route_hits:{path}:{date}` via lightweight middleware.

### 2.5 Success Metrics

| Metric | Threshold | Kill Signal |
|--------|-----------|-------------|
| Conversation completion rate | ≥ 70% | < 50% → stop |
| Human override rate (STANDARD) | ≤ 30% | — |
| Time-to-gate improvement | ≥ 40% faster | — |
| Pilot retention (Week 2) | 3/3 active | < 2/3 → stop |

---

## 3. Consequences

### 3.1 Positive

- **Zero codebase risk**: No deletion, only addition (~5K LOC) + modification (~5K LOC)
- **Leverages 225 sprints**: Full 230K LOC platform remains available
- **Validates thesis cheaply**: 10-week plan with kill criteria at Week 2
- **Hybrid model scales**: LITE (1-2 people) to ENTERPRISE (15+ people) with same engine
- **Data-driven future cuts**: Telemetry provides evidence for deprecation decisions

### 3.2 Negative

- **579 endpoints remain**: Maintenance burden continues until telemetry data drives cuts
- **Thesis unvalidated**: "Conversation for action" may not resonate with Vietnamese SME
- **Complexity hidden, not removed**: Backend complexity persists behind chat interface

### 3.3 Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| SME users prefer dashboard over chat | MEDIUM | HIGH | Week 1 interviews, kill criteria Week 2 |
| 4 presets too rigid for edge cases | LOW | MEDIUM | Custom matrix deferred to v2 if validated |
| Telemetry overhead on request latency | LOW | LOW | Redis INCR is O(1), ~0.1ms added |

---

## 4. Implementation Roadmap

| Week | Phase | Deliverables |
|------|-------|-------------|
| 1-2 | Design + Validate | Customer interviews, workflow design, baseline metrics, telemetry labels |
| 3-4 | Backend | autonomy_level migration, command expansion, gate integration |
| 5-6 | OTT Enrichment | Planning+evidence+gate commands via Telegram |
| 6 | **HARD FREEZE** | Bug fix only after this point |
| 7-8 | Frontend | Admin-only transformation, conversation analytics |
| 9 | Internal Pilot | MTClaw team uses Orch for own development |
| 10 | External Pilot | 3 Vietnamese SME partners |

---

## 5. References

- [Option 5 Strategic Decision](../../09-govern/07-Strategic-Decisions/Option5-Conversation-First-Relaunch-APPROVED.md)
- [ADR-064: Chat-First Facade](ADR-064-Chat-First-Facade-Option-D-Plus.md) — thesis reframed by D-071-01
- [ADR-056: Multi-Agent Team Engine](ADR-056-Multi-Agent-Team-Engine.md)
- [ADR-059: Enterprise-First Refocus](ADR-059-Enterprise-First-Refocus.md)
- [ADR-065: Unified Tier Resolution](ADR-065-Unified-Tier-Resolution.md)
