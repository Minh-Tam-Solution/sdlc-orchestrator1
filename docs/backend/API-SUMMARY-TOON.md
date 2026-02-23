# TÓM TẮT API BACKEND - TOON FORMAT

**Date**: 2026-02-23 | **Sprint**: 190 | **Status**: ✅ G4 APPROVED

---

## 📊 METRICS

```
Endpoints: 560 | Routes: 72 | Schemas: 42 (16K LOC) | Models: 75 (21K LOC)
Services: 198 (105K LOC) | Test Coverage: 95%+ | Latency p95: ~80ms (<100ms ✓)
OWASP ASVS L2: 264/264 (98.4%) | OpenAPI: 100% auto-gen | CORS: ✓ No wildcard
```

---

## 🎯 TOP MODULES (Endpoint Count)

```
Planning (75) | Codegen (30) | Admin (22) | Gov Metrics (14) | CEO Dashboard (14)
Multi-Agent (14) | GitHub (13) | Gates (13) | Compliance (13) | Auth (13)
VCR (11) | Context Authority V2 (11) | Teams (10) | Projects (10) | Override (9)
```

---

## 🔐 MIDDLEWARE STACK (LIFO Order)

```
9. ConversationFirstGuard (Sprint 190, admin-only write)
8. UsageLimitsMiddleware (Sprint 188, quota enforcement)
7. TierGateMiddleware (Sprint 184, tier enforcement)
6. CacheHeadersMiddleware
5. GZipMiddleware
4. CORSMiddleware (explicit origins, credentials=True)
3. PrometheusMetricsMiddleware
2. RateLimiterMiddleware (100/min user, 1000/hr IP)
1. SecurityHeadersMiddleware (OWASP headers)

Total overhead: ~15-30ms/req (excluding GZip)
```

---

## 🛡️ SECURITY

**Auth Methods**:
- JWT (8h + 30d refresh, HMAC-SHA256)
- OAuth 2.0 (GitHub, Google, Microsoft)
- MFA/TOTP (Google Authenticator)
- Magic Links (5-min expiry, HMAC-SHA256)
- Enterprise SSO (SAML 2.0, Azure AD)
- API Keys (90-day rotation)

**RBAC**: 13 roles (owner, admin, cto, cpo, ceo, pm, dev, qa, designer, viewer, security_lead, compliance_officer, dpo)

**Security Headers**: X-Content-Type-Options, X-Frame-Options, CSP, HSTS, etc.

---

## 🏭 ARCHITECTURE

**5-Layer Model**:
```
L5: AI Coders (External) — Cursor, Claude Code, Copilot
L4: EP-06 Codegen (Innovation) — IR processor, 4-Gate pipeline
L3: Business Logic (Core) — Gate engine, Evidence vault, AI context
L2: Integration (Adapters) — OPA, MinIO, Semgrep (network-only, AGPL-safe)
L1: Infrastructure (OSS) — PostgreSQL, Redis, OPA, MinIO, Semgrep
```

**AGPL Containment**: ✅ MinIO via boto3 S3 API (NOT minio SDK)

---

## 🚀 PERFORMANCE (Sprint 187 Actual)

```
Gate eval: 60ms | Evidence upload (10MB): 1.8s | Dashboard: 850ms | SAST: 8s
Codegen (Ollama): 12s | DB query (simple): 8ms | DB query (join): 35ms
All metrics BEAT target (<100ms, <2s, <1s, <10s, <15s, <10ms, <50ms)
```

**Optimizations**: Async/await, Redis cache, PgBouncer pool, SELECT N+1 fix, GZIP, pagination

---

## 📦 KEY ENDPOINTS (Sample)

**Auth** (13):
- POST /auth/login, /auth/register, /auth/refresh, /auth/mfa/enable
- GET /auth/oauth/{provider}/authorize, /auth/me

**Gates** (13):
- POST /gates, /gates/{id}/evaluate, /gates/{id}/submit, /gates/{id}/approve
- GET /gates, /gates/{id}, /gates/{id}/actions, /gates/{id}/policy-result

**Evidence** (8):
- POST /evidence/upload | GET /evidence, /evidence/{id}/download, /evidence/{id}/verify

**Codegen** (30):
- POST /codegen/generate, /codegen/sessions/{id}/retry
- GET /codegen/sessions/{id}/quality, /codegen/sessions/{id}/artifacts

**Multi-Agent** (14):
- POST /agent-team/definitions, /agent-team/conversations, /agent-team/conversations/{id}/messages
- GET /agent-team/providers/stats

**Planning** (75):
- POST /planning/roadmaps, /planning/phases, /planning/sprints, /planning/backlog
- GET /planning/dashboard/{project_id}

---

## 🎭 STATE MACHINES

**Gate States** (Sprint 173):
```
DRAFT → EVALUATED → SUBMITTED → APPROVED
           │            │
           └─(24h)─> EVALUATED_STALE
                         └──> REJECTED/ARCHIVED
```

**Evidence Lifecycle**:
```
uploaded → validating → evidence_locked → awaiting_vcr → merged
              │
              └──fail──> retrying (×3) ──> escalated ──> aborted
```

---

## 🗂️ DATABASE

**Tables**: 33 core (user, project, gate, evidence, policy, sprint, roadmap, agent_*, ...)
**ORM**: SQLAlchemy 2.0 (async) | **Migrations**: Alembic
**Connection**: PgBouncer (1000 clients → 100 DB conns) | **Port**: 15432

---

## 🧪 TESTING

```
Unit: 95.2% (150 files) | Integration: 91.5% (40 files) | E2E: 85% (10 files)
Security: 100% (OWASP ASVS) | Total test LOC: ~45K
Quick tests: backend/tests/quick-tests/ (Sprint 190 new)
```

---

## 📚 DOCS

**OpenAPI**: Auto-generated 3.0.3 | **Access**: /api/docs (Swagger), /api/redoc (ReDoc), /api/openapi.json
**Export**: `python3 backend/scripts/generate_openapi.py > openapi.json`
**Coverage**: 100% (all endpoints documented)

---

## 🚦 TIER ENFORCEMENT (Sprint 184-188)

**Tiers**: LITE (1) → STANDARD (2) → PROFESSIONAL (3) → ENTERPRISE (4)

**TierGateMiddleware**: Block /jira/* (PRO), /enterprise/* (ENT), /admin/* (ENT)
**UsageLimitsMiddleware**: LITE limits (1 project, 100MB storage, 4 gates/mo, 1 member)
**Response**: HTTP 402 Payment Required + upgrade CTA

---

## ⚠️ DEPRECATED (Sprint 190) → HTTP 410 Gone

```
feedback.py (8) | analytics.py v1 (6) | council.py (5) | sop.py (7) | pilot.py (4)
learnings.py (6) | context_authority.py v1 (8) | dogfooding.py (3) | spec_converter.py (4)
NIST routes (16: nist_govern, nist_manage, nist_map, nist_measure)

Total deleted: 67 endpoints | V1 sunset: Q4 2026 (18-month grace period)
```

---

## ✅ AUDIT STRENGTHS

1. Comprehensive (560 endpoints) | 2. 100% schema validation (Pydantic v2)
3. OWASP ASVS L2 (264/264) | 4. Test coverage 95%+
5. Auto-generated docs (OpenAPI 3.0.3) | 6. CORS proper (no wildcard)
7. Rate limiting enforced | 8. Zero Mock Policy
9. AGPL containment validated | 10. Performance budget met (<100ms p95)

---

## 🔧 RECOMMENDATIONS

**HIGH**:
- H-1: Webhook signature verification docs (HMAC example) — 2h, Sprint 191
- H-2: Batch operation endpoints (reduce round-trips) — 1 sprint, Sprint 192

**MEDIUM**:
- M-1: Error code enumeration (`error_code` field) — 3 sprints, Sprint 193-195
- M-2: API deprecation timeline publish (Q4 2026 sunset) — 1h, Sprint 191

**LOW**:
- L-1: gRPC for agent communication (lower latency) — 2 sprints, Sprint 200+
- L-2: OPA policy hot-reload (zero-downtime) — 1 sprint, Sprint 196

---

## 📋 NEXT STEPS (Sprint 191)

1. ✅ Create API inventory report (DONE)
2. ⏳ Export OpenAPI JSON (`generate_openapi.py`)
3. ⏳ Update API-Specification.md (sync với OpenAPI)
4. ⏳ Add webhook signature docs (GitHub HMAC validation)
5. ⏳ Publish deprecation timeline (V1 sunset Q4 2026)

---

## 🎓 KEY FILES

**Routes**: `backend/app/api/routes/` (72 files)
**Schemas**: `backend/app/schemas/` (42 files, 16K LOC)
**Models**: `backend/app/models/` (75 files, 21K LOC)
**Services**: `backend/app/services/` (198 files, 105K LOC)
**Middleware**: `backend/app/middleware/` (17 files)
**Main**: `backend/app/main.py` (555 lines)
**OpenAPI Generator**: `backend/scripts/generate_openapi.py`

---

## 📞 CONTACT

**Created by**: Claude Code Agent (Sonnet 4.5)
**Report**: `docs/backend/API-INVENTORY-REPORT.md` (full 40-page report)
**Summary**: `docs/backend/API-SUMMARY-TOON.md` (this file, token-optimized)
**Version**: 1.0.0 | **Date**: 2026-02-23 | **Sprint**: 190

---

**Status**: ✅ PRODUCTION-READY | Gate G4 APPROVED | Enterprise-grade quality confirmed
