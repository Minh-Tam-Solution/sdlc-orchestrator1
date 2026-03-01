# Project Context — SDLC Orchestrator

*-CyEyes-* — Phase -1 Analysis Record

**Analyzed**: 2026-02-21
**By**: @tester (e2e-api-testing skill v2.0.0, SDLC 6.1.1)

---

## Backend Service

| Property | Value |
|----------|-------|
| **Framework** | FastAPI (Uvicorn) |
| **Location** | `backend/app/` |
| **Port** | 8300 |
| **Base URL** | `http://localhost:8300` |
| **Container** | `sdlc-staging-backend` |
| **Version** | 1.2.0 |
| **Health** | `/health` → `{"status":"healthy","version":"1.2.0"}` |

## Supporting Services

| Service | Container | Port | Status |
|---------|-----------|------|--------|
| PostgreSQL | `sdlc-staging-postgres` | 5450 | ✅ |
| Redis | `sdlc-staging-redis` | 6395 | ✅ |
| MinIO | `sdlc-staging-minio` | 9010 | ✅ |
| OPA | `sdlc-staging-opa` | 8185 | ✅ |
| Frontend | `sdlc-staging-frontend` | 8310 | ✅ |

## Test Credentials

| Role | Email | Password | Notes |
|------|-------|----------|-------|
| **Admin (superuser)** | `taidt@mtsolution.com.vn` | `Admin@123456` | Active — login confirmed 2026-02-21 |
| Source | `backend/create_admin.py` | | Account unlocked, original password works |

> NOTE: Account was previously locked (2026-02-20). As of 2026-02-21, `Admin@123456` works. Login via `POST /api/v1/auth/login`.

## API Entry Points

| Endpoint | URL |
|----------|-----|
| Health | `http://localhost:8300/health` |
| Ready | `http://localhost:8300/health/ready` |
| Swagger UI | `http://localhost:8300/api/docs` |
| OpenAPI JSON | `http://localhost:8300/api/openapi.json` |
| Metrics | `http://localhost:8300/metrics` |

## OpenAPI Spec

- **SSOT Location**: `docs/03-integrate/02-API-Specifications/openapi.json`
- **Live endpoint**: `http://localhost:8300/api/openapi.json`
- **Total Paths**: 617
- **Total Operations**: 704 (GET: 375, POST: 266, PUT: 27, DELETE: 26, PATCH: 10)

## Latest E2E Test Results (2026-02-28)

- **Report**: [E2E-API-REPORT-2026-02-28.md](reports/E2E-API-REPORT-2026-02-28.md)
- **Tested**: 579/585 operations (6 skipped)
- **API Health Score**: 94.5% (non-5xx responses)
- **Direct Pass Rate**: 24.9% (auto-generated bodies — manual tests confirm endpoints work)
- **Server Errors**: 31 endpoints (5.4%) — categorized in report
- **p95 Latency**: 11.4ms (well under 100ms budget)
- **Sprint 214 Manual Pass Rate**: 14/15 (93.3%)
- **SHA256**: `7158fbaca16a8d65d2987f284e3a4d6d759e87cba7ffb1fe033941a87c609496`

### Previous Results (2026-02-21)

- **Report**: [E2E-API-REPORT-2026-02-21.md](reports/E2E-API-REPORT-2026-02-21.md)
- **Tested**: 698/704 operations
- **API Health Score**: 94.7%

## Key Finding — GDPR DSAR List 500

`GET /api/v1/gdpr/dsar` returns 500 Internal Server Error. The POST endpoint (create DSAR) works with `requester_email` field. This is **P0 for Sprint 215**.

## Staging Build Status

As of 2026-02-28, staging is running latest build with Sprint 209-214 code deployed:
- Sprint 209-213: All routes deployed and tested
- Sprint 214: GDPR, Data Residency, Compliance dashboard — deployed
- 31 endpoints return 5xx (GitHub webhooks, MCP, Invitations — config/infra issues)
