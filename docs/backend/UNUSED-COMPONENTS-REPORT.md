# Unused Components Report — SDLC Orchestrator Backend

**Generated**: 2026-02-26
**Scope**: `/backend/app/`
**Framework**: SDLC 6.1.1 (Sprint 190 post-cleanup analysis)

---

## TL;DR (TOON Format)

```
TOTAL ENDPOINTS : 590 (77 route modules)
TOTAL SERVICES  : 219
UNUSED SERVICES : 48 (22% — mostly codegen sub-modules, indirectly used)
UNUSED MODELS   : 6 (orphaned from Sprint 190 deleted routes)
ROUTE FILES     : All 77 registered ✅
DEPRECATED ROUTES (Sprint 190): 9 removed from main.py, files deleted
```

---

## 1. Orphaned Model Files (Safe to Archive)

These model files correspond to routes/features deleted in **Sprint 190 Conversation-First Cleanup**. Routes are gone, tables deprecated (COMMENT ON TABLE via Alembic s190_001).

| Model File | Linked Feature | Status |
|------------|----------------|--------|
| `council_session.py` | AI Council (council.router deleted S190) | ORPHANED — archive |
| `learning_aggregation.py` | Learning Service (learnings.router deleted S190) | ORPHANED — archive |
| `nist_manage.py` | NIST Manage (nist routes deleted S190) | ORPHANED — archive |
| `nist_map_measure.py` | NIST Map/Measure (nist routes deleted S190) | ORPHANED — archive |
| `pilot_tracking.py` | Pilot Tracking (pilot.router deleted S190) | ORPHANED — archive |
| `pr_learning.py` | PR Learnings (feedback.router deleted S190) | ORPHANED — archive |

**Action**: Move to `backend/99-Legacy/models/` or `backend/app/models/archive/`

---

## 2. Potentially Unused Service Files

> ⚠️ NOTE: Many of these are **indirectly used** (called from other services, not directly imported by routes). Manual review required before deletion.

### 2a. Likely Truly Unused (Safe to Review)

| Service | Reason |
|---------|--------|
| `compliance_service.py` | Superceded by `compliance_scanner.py` + route-level logic |
| `github_check_run_service.py` | Check runs handled via `github_check_run_service` import in routes |
| `mcp_client_service.py` | MCP analytics uses direct API calls |
| `policy_service.py` | Route uses `opa_policy_service.py` directly |
| `project_service.py` | Route uses `project_metadata_service.py` + `project_sync_service.py` |
| `sase_sprint_integration.py` | Sprint integration deferred to Sprint 191+ |
| `tier_approval_service.py` | Tier changes handled by `tier_management` route directly |
| `governance.error_templates` | Templates embedded in enforcement services |

### 2b. Indirectly Used (Do NOT Delete)

| Service | Used By |
|---------|---------|
| `codegen.claude_provider` | `codegen_service.py` via provider registry |
| `codegen.ollama_provider` | `codegen_service.py` via provider registry |
| `codegen.deepcode_provider` | `codegen_service.py` via provider registry |
| `codegen.domains.*` | Domain-specific generators called by `codegen_service` |
| `codegen.ir.*` | IR processing pipeline called by `codegen_service` |
| `codegen.templates.*` | Template system for code generation |
| `codegen.onboarding.*` | Onboarding flow (6 codegen onboarding endpoints) |
| `agent_team.eval_scorer` | Called by `conversation_tracker.py` |
| `agent_team.langchain_tool_registry` | LangGraph integration (Sprint 208) |
| `semgrep_service.py` | Called by `sast_route.py` via `semgrep_service` |
| `user_service.py` | Called by `admin.py` and `auth.py` |
| `usage_alert_service.py` | Called by `usage_service.py` |
| `usage_tracking_service.py` | Called by `usage_service.py` |
| `validators.sast_validator` | Called by `codegen quality_pipeline` |
| `validators.policy_guard_validator` | Called by `policy_pack_service` |

---

## 3. Routes Removed in Sprint 190 (Files Deleted)

These routes were removed per CEO directive (Conversation-First Cleanup):

| Route Module | Deleted Sprint | Replacement |
|--------------|---------------|-------------|
| `feedback.py` | Sprint 190 | `analytics_v2` |
| `analytics.py` (v1) | Sprint 190 | `analytics_v2` |
| `council.py` | Sprint 190 | None (removed) |
| `sop.py` | Sprint 190 | None (removed) |
| `pilot.py` | Sprint 190 | None (removed) |
| `learnings.py` | Sprint 190 | None (removed) |
| `context_authority.py` (v1) | Sprint 190 | `context_authority_v2` |
| `dogfooding.py` | Sprint 190 | None (removed) |
| `spec_converter.py` | Sprint 190 | None (removed) |
| `nist_govern.py` | Sprint 190 | None (removed) |
| `nist_manage.py` | Sprint 190 | None (removed) |
| `nist_map.py` | Sprint 190 | None (removed) |
| `nist_measure.py` | Sprint 190 | None (removed) |

> ✅ Route files confirmed deleted from disk. No stale route files remain.
> ⚠️ No HTTP 410 stub (deprecated_routes.py) currently exists — consider adding for migration period.

---

## 4. Route Files Not Registered in main.py

**Status: NONE** — All 77 route files are properly registered in `main.py`. ✅

---

## 5. Middleware Stack (Active)

All middleware is active and serving purposes:

| Middleware | Purpose | Sprint |
|-----------|---------|--------|
| `CORSMiddleware` | Cross-origin requests | Core |
| `GZipMiddleware` | Response compression | Core |
| `PrometheusMetricsMiddleware` | Metrics collection | Sprint 21 |
| `RateLimiterMiddleware` | Rate limiting (100 req/min) | Core |
| `SecurityHeadersMiddleware` | OWASP headers | Core |
| `CacheHeadersMiddleware` | Cache control | Core |
| `TierGateMiddleware` | 4-tier enforcement | Sprint 184 |
| `UsageLimitsMiddleware` | Per-resource limits | Sprint 188 |
| `ConversationFirstGuard` | Admin-only write paths | Sprint 190 |

---

## 6. Background Jobs

| Job | Schedule | Module |
|-----|----------|--------|
| Daily compliance scan | 2:00 AM | `jobs/compliance_scan.py` |
| Scan queue processor | Every 5 min | `jobs/compliance_scan.py` |
| WorkflowResumer | On startup (if LANGGRAPH_ENABLED) | `agent_team/workflow_resumer.py` |

---

## 7. Recommendations

### Immediate (P0)
1. **Archive orphaned models** — Move 6 models to `99-Legacy/` (council, learning, nist, pilot, pr_learning)
2. **Add HTTP 410 stubs** — Create `deprecated_routes.py` with 410 Gone for deleted Sprint 190 routes

### Short-term (P1)
3. **Verify unused services** — Run dependency analysis on `compliance_service.py`, `policy_service.py`, `project_service.py`
4. **Codegen sub-module audit** — Many `codegen/domains/*` templates may be redundant; consolidate
5. **MCP client service** — Verify `mcp_client_service.py` is actually unused before removal

### Long-term (P2)
6. **Sprint 191+ blockers** — `sase_generation_service.py`, `analytics_service.py` v1, `context_authority.py` v1 deferred
7. **Agent bridge cleanup** — `agent_bridge/` services (OTT handlers) may need consolidation after Sprint 198

---

*Report generated by static code analysis. Verify before deletion.*
