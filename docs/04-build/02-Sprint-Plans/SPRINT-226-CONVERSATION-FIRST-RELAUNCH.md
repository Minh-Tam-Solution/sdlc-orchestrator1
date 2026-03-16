---
sdlc_version: "6.1.2"
document_type: "Sprint Plan"
status: "DRAFT — Pending CTO Approval"
sprint: "226"
tier: "ALL"
stage: "04 - Build"
---

# Sprint 226 — Conversation-First Relaunch (Week 1-2: Foundation)

| Field            | Value |
|------------------|-------|
| Sprint Duration  | March 2026 (Week 1-2 of 10-week plan) |
| Sprint Goal      | Implement 5 CTO-approved changes: reframe thesis, 4 autonomy presets, telemetry labels, Telegram-only flag, product metrics baseline |
| Status           | DRAFT — Pending CTO Approval |
| Priority         | P0 — Strategic pivot foundation (Option 5 APPROVED) |
| Framework        | SDLC 6.1.2 |
| Previous Sprint  | Sprint 225 — SOUL Template Integration |
| Dependency       | Option 5 Strategic Decision (APPROVED 2026-03-16) |
| Raised by        | CEO + CTO + CPO + PM + Architect |
| ADR              | ADR-071 — Option 5 Conversation-First Relaunch |

---

## Context

Option 5 (Conversation-First Relaunch) approved by CEO+CTO+CPO on March 16, 2026. CTO review identified 5 required changes before execution can begin. This sprint implements all 5 foundational changes (~9 working days).

Sprint 226 is Week 1-2 of the 10-week execution plan. No new features — only foundation work to enable Weeks 3-10.

---

## Deliverables

### S226-01: Thesis Reframe — Documentation Updates (1 day)

**MODIFY**: `CLAUDE.md`, ADR-064

Update all positioning references from "OTT primary" to "Conversation for action, web for visualization/admin."

| File | Change |
|------|--------|
| `CLAUDE.md` header | ✅ DONE — Interface Strategy line updated |
| `CLAUDE.md` changelog | ✅ DONE — v3.11.0 entry added |
| ADR-064 Section 2.3 | Add note: "Thesis reframed by ADR-071 D-071-01" |

### S226-02: 4 Fixed Autonomy Presets (2 days)

**CREATE**: Alembic migration `s226_001_add_autonomy_level.py`
**MODIFY**: `backend/app/models/agent_definition.py`, `backend/app/services/agent_team/agent_registry.py`, `backend/app/services/gate_service.py`

Add `autonomy_level` column to `agent_definitions`:

```python
# In model
autonomy_level = Column(
    String(30),
    nullable=False,
    default="assist_only",
    server_default="assist_only",
    comment="Tier-mapped preset: assist_only|contribute_only|member_guardrails|autonomous_gated"
)
```

Tier enforcement in `agent_registry.py`:

```python
TIER_AUTONOMY_MAP = {
    "LITE": "assist_only",
    "FOUNDER": "assist_only",
    "STARTER": "contribute_only",
    "STANDARD": "contribute_only",
    "PROFESSIONAL": "member_guardrails",
    "ENTERPRISE": "autonomous_gated",
}
```

Gate integration in `gate_service.py` → `compute_gate_actions()`:
- `assist_only`: agent CANNOT approve any gate (always require human)
- `contribute_only`: agent can evaluate G1/G2, human approves all
- `member_guardrails`: agent auto-approves G1/G2, human approves G3/G4
- `autonomous_gated`: agent auto-approves G1/G2/G3, human approves G4 only via Magic Link

**Validation**: Reject custom autonomy values at API level. Only 4 presets accepted.

### S226-03: Surface Reduction Telemetry (3 days)

**CREATE**: `backend/app/middleware/route_telemetry.py` (~100 LOC)
**MODIFY**: `backend/app/main.py` (add middleware)

Lightweight pure ASGI middleware:

```python
async def __call__(self, scope, receive, send):
    if scope["type"] == "http":
        path = scope["path"]
        date = datetime.utcnow().strftime("%Y-%m-%d")
        await redis.incr(f"route_hits:{path}:{date}")
    await self.app(scope, receive, send)
```

**CREATE**: `backend/app/api/routes/telemetry.py` (~50 LOC)

Admin-only endpoint to query hit rates:

```
GET /api/v1/admin/telemetry/route-hits?date=2026-03-20
→ { "/api/v1/gates": 142, "/api/v1/evidence": 89, "/api/v1/planning/sprints": 3 }
```

**Label assignment**: Add route-level labels in `main.py` router registration comments:

```python
# ACTIVE_PRIMARY — conversation workflows
app.include_router(gates.router, ...)
app.include_router(evidence.router, ...)
app.include_router(agent_team.router, ...)

# ACTIVE_ADMIN — admin dashboard
app.include_router(admin.router, ...)
app.include_router(auth.router, ...)

# LEGACY_SUPPORTED — monitor usage
app.include_router(planning.router, ...)
app.include_router(analytics_v2.router, ...)
```

### S226-04: Telegram-Only Feature Flag (1 day)

**MODIFY**: `backend/app/core/config.py`, `backend/app/api/routes/ott_gateway.py`

```python
# In config.py Settings
FEATURE_FLAG_ZALO_OTT: bool = False
FEATURE_FLAG_TEAMS_OTT: bool = False
FEATURE_FLAG_SLACK_OTT: bool = False
```

In `ott_gateway.py` webhook handler:
```python
if channel == "zalo" and not settings.FEATURE_FLAG_ZALO_OTT:
    return JSONResponse({"error": "Zalo channel disabled in v1"}, status_code=503)
```

### S226-05: Product Metrics Baseline (2 days)

**CREATE**: `backend/app/services/product_metrics_service.py` (~150 LOC)

Collect baseline metrics from existing data:

```python
class ProductMetricsService:
    async def time_to_gate_baseline(self, project_id: UUID) -> dict:
        """Average time from gate evaluated_at → approved_at/rejected_at"""
        ...

    async def conversation_completion_rate(self, date_range: tuple) -> float:
        """% of conversations started via chat that completed without web fallback"""
        ...

    async def human_override_rate(self, tier: str, date_range: tuple) -> float:
        """% of agent actions overridden by human at given tier"""
        ...
```

**CREATE**: `backend/app/api/routes/product_metrics.py` (~40 LOC)

```
GET /api/v1/admin/product-metrics/baseline
GET /api/v1/admin/product-metrics/current?date_from=&date_to=
```

---

## Key Files

| File | Action |
|------|--------|
| `CLAUDE.md` | ✅ DONE (v3.11.0) |
| `docs/02-design/01-ADRs/ADR-071-*.md` | ✅ DONE |
| `docs/09-govern/07-Strategic-Decisions/Option5-*.md` | ✅ DONE |
| `backend/app/models/agent_definition.py` | MODIFY (autonomy_level) |
| `backend/alembic/versions/s226_001_*.py` | CREATE (migration) |
| `backend/app/services/agent_team/agent_registry.py` | MODIFY (tier enforcement) |
| `backend/app/services/gate_service.py` | MODIFY (autonomy in compute_gate_actions) |
| `backend/app/middleware/route_telemetry.py` | CREATE (hit counter) |
| `backend/app/api/routes/telemetry.py` | CREATE (admin query) |
| `backend/app/main.py` | MODIFY (middleware + labels) |
| `backend/app/core/config.py` | MODIFY (feature flags) |
| `backend/app/api/routes/ott_gateway.py` | MODIFY (channel guards) |
| `backend/app/services/product_metrics_service.py` | CREATE |
| `backend/app/api/routes/product_metrics.py` | CREATE |

---

## Implementation Sequence

```
S226-01 (Docs)              ← ✅ DONE
S226-04 (Feature flags)     ← No deps, start immediately (1 day)
S226-02 (Autonomy presets)  ← No deps, parallel (2 days)
S226-03 (Telemetry)         ← No deps, parallel (3 days)
S226-05 (Metrics baseline)  ← Depends on S226-02 (needs autonomy for override calc)
```

Parallelizable: S226-01, S226-02, S226-03, S226-04 can run simultaneously.

---

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Alembic migration chain break | High | Verify s202001 → s226001. Test on staging first |
| Redis INCR overhead on latency | Low | O(1) operation, ~0.1ms. Fire-and-forget (no await) |
| 3 test files check command count | Medium | Not modifying command count this sprint — safe |
| gate_service autonomy logic complex | Medium | Start with assist_only only. Add other presets incrementally |

---

## Estimates

| Metric | Value |
|--------|-------|
| Production LOC | ~340 (new) + ~200 (modified) |
| Test LOC | ~200 |
| Total LOC | ~740 |
| Timeline | 9 working days |

---

## Verification

1. **Migration**: `alembic upgrade head` — no errors, `autonomy_level` column exists with default 'assist_only'
2. **Autonomy enforcement**: Create LITE project agent → verify autonomy_level='assist_only'. Attempt custom value → 400 error
3. **Telemetry**: Hit `/api/v1/gates` 5 times → `GET /admin/telemetry/route-hits` shows count=5
4. **Feature flags**: POST Zalo webhook → 503 "Zalo channel disabled in v1"
5. **Baseline metrics**: `GET /admin/product-metrics/baseline` returns time-to-gate averages
6. **Regression**: `python -m pytest backend/tests/ -x --timeout=60` — all green
