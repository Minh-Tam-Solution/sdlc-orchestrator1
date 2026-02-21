# API Endpoints - Summary Table (TOON Format)

**Date**: 2026-02-21
**Total**: 636 endpoints
**Format**: Optimized for quick reference

---

## 📊 Statistics

| Metric | Count | % |
|--------|-------|---|
| **Total Endpoints** | 636 | 100% |
| GET | 341 | 53.6% |
| POST | 240 | 37.7% |
| DELETE | 23 | 3.6% |
| PUT | 22 | 3.5% |
| PATCH | 10 | 1.6% |
| **Services** | 96 | - |

---

## 🔝 Top 20 Services by Endpoint Count

| # | Service | Endpoints | Key Focus |
|---|---------|-----------|-----------|
| 1 | Planning Hierarchy | 150 | Roadmap, Phase, Sprint, Backlog |
| 2 | Codegen (EP-06) | 58 | IR-based code generation |
| 3 | Planning | 46 | General planning ops |
| 4 | Sprint 78 | 39 | Sprint operations |
| 5 | Authentication | 26 | Login, OAuth, JWT, MFA |
| 6 | Compliance | 26 | NIST, OWASP validation |
| 7 | Gates | 24 | Quality gate lifecycle |
| 8 | Admin Panel | 22 | System administration |
| 9 | Analytics | 22 | DORA metrics |
| 10 | Context Authority V2 | 22 | Requirement classification |
| 11 | Feedback Learning (EP-11) | 22 | AI feedback loop |
| 12 | VCR | 22 | Version Control Resolution |
| 13 | Multi-Agent Team (EP-07) | 20 | Agent orchestration |
| 14 | Dogfooding | 20 | Self-use tracking |
| 15 | MRP | 18 | Merge Readiness Protocol |
| 16 | AGENTS.md | 16 | Agent config management |
| 17 | Agentic Maturity | 16 | Maturity assessment |
| 18 | CRP - Consultations | 16 | Consultation requests |
| 19 | Planning Sub-agent | 16 | Planning automation |
| 20 | SOP Generator | 16 | SOP creation |

---

## 🎯 Core API Endpoints (Most Used)

### Authentication (26 endpoints)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/auth/register` | User registration |
| POST | `/api/v1/auth/login` | Login (email/password) |
| POST | `/api/v1/auth/refresh` | Refresh JWT token |
| POST | `/api/v1/auth/logout` | Logout |
| GET | `/api/v1/auth/me` | Get current user |
| POST | `/api/v1/auth/github/callback` | GitHub OAuth |
| POST | `/api/v1/auth/google/callback` | Google OAuth |
| POST | `/api/v1/auth/microsoft/callback` | Microsoft OAuth |
| POST | `/api/v1/auth/mfa/enable` | Enable MFA |
| POST | `/api/v1/auth/mfa/verify` | Verify MFA code |

### Gates (24 endpoints)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/gates` | List all gates |
| POST | `/api/v1/gates` | Create gate |
| GET | `/api/v1/gates/{id}` | Get gate details |
| PUT | `/api/v1/gates/{id}` | Update gate |
| DELETE | `/api/v1/gates/{id}` | Delete gate |
| POST | `/api/v1/gates/{id}/evaluate` | Evaluate gate (OPA) |
| POST | `/api/v1/gates/{id}/submit` | Submit for approval |
| POST | `/api/v1/gates/{id}/approve` | Approve gate |
| POST | `/api/v1/gates/{id}/reject` | Reject gate |
| GET | `/api/v1/gates/{id}/policy-result` | Get OPA result |
| POST | `/api/v1/gates/{id}/override` | Override gate |
| GET | `/api/v1/gates/{id}/evidence` | List evidence |

### Evidence (10 endpoints total: 3 + 7 manifest)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/evidence` | List evidence |
| POST | `/api/v1/evidence/upload` | Upload evidence |
| GET | `/api/v1/evidence/{id}` | Get evidence |
| DELETE | `/api/v1/evidence/{id}` | Delete evidence |
| GET | `/api/v1/evidence/{id}/download` | Download file |
| GET | `/api/v1/evidence/{id}/verify` | Verify SHA256 |
| POST | `/api/v1/evidence/{id}/lock` | Lock (immutable) |
| GET | `/api/v1/evidence/manifest` | Get manifest |
| POST | `/api/v1/evidence/manifest` | Create manifest |
| GET | `/api/v1/evidence/manifest/{id}` | Get manifest by ID |

### Projects (10 endpoints)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/projects` | List projects |
| POST | `/api/v1/projects` | Create project |
| GET | `/api/v1/projects/{id}` | Get project |
| PUT | `/api/v1/projects/{id}` | Update project |
| DELETE | `/api/v1/projects/{id}` | Delete project |
| POST | `/api/v1/projects/{id}/sync` | Sync with GitHub |
| GET | `/api/v1/projects/{id}/gates` | Get project gates |
| GET | `/api/v1/projects/{id}/evidence` | Get project evidence |
| POST | `/api/v1/projects/{id}/decompose` | AI task decomposition |
| GET | `/api/v1/projects/{id}/compliance` | Compliance status |

---

## 🚀 Innovation Features

### EP-06: Codegen (58 endpoints)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/codegen/generate` | Generate code from spec |
| GET | `/api/v1/codegen/sessions` | List sessions |
| GET | `/api/v1/codegen/sessions/{id}` | Get session |
| POST | `/api/v1/codegen/sessions/{id}/retry` | Retry generation |
| POST | `/api/v1/codegen/sessions/{id}/escalate` | Escalate to council |
| GET | `/api/v1/codegen/sessions/{id}/quality` | Quality pipeline result |
| GET | `/api/v1/codegen/providers` | List providers |
| GET | `/api/v1/codegen/providers/{id}/stats` | Provider statistics |
| POST | `/api/v1/codegen/validate` | Validate code |
| DELETE | `/api/v1/codegen/sessions/{id}` | Delete session |

### EP-07: Multi-Agent Team (20 endpoints)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/agent-team/definitions` | Create agent |
| GET | `/api/v1/agent-team/definitions` | List agents |
| GET | `/api/v1/agent-team/definitions/{id}` | Get agent |
| PUT | `/api/v1/agent-team/definitions/{id}` | Update agent |
| DELETE | `/api/v1/agent-team/definitions/{id}` | Delete agent |
| POST | `/api/v1/agent-team/conversations` | Start conversation |
| GET | `/api/v1/agent-team/conversations/{id}` | Get conversation |
| POST | `/api/v1/agent-team/conversations/{id}/messages` | Send message |
| POST | `/api/v1/agent-team/conversations/{id}/interrupt` | Interrupt agent |
| GET | `/api/v1/agent-team/messages/{id}` | Get message |
| POST | `/api/v1/agent-team/messages/{id}/retry` | Retry message |

### EP-11: Feedback Learning (22 endpoints)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/feedback/learnings` | Submit learning |
| GET | `/api/v1/feedback/learnings` | List learnings |
| GET | `/api/v1/feedback/learnings/{id}` | Get learning |
| PUT | `/api/v1/feedback/learnings/{id}` | Update learning |
| DELETE | `/api/v1/feedback/learnings/{id}` | Delete learning |
| POST | `/api/v1/feedback/learnings/{id}/apply` | Apply to project |
| GET | `/api/v1/feedback/patterns` | Extract patterns |
| POST | `/api/v1/feedback/pr-review` | Learn from PR |
| GET | `/api/v1/feedback/recommendations` | Get recommendations |

---

## 📋 Planning Hierarchy (150 endpoints)

### Roadmaps (12 endpoints)
```
GET    /api/v1/planning/roadmaps
POST   /api/v1/planning/roadmaps
GET    /api/v1/planning/roadmaps/{id}
PUT    /api/v1/planning/roadmaps/{id}
DELETE /api/v1/planning/roadmaps/{id}
POST   /api/v1/planning/roadmaps/{id}/sync
GET    /api/v1/planning/roadmaps/{id}/phases
POST   /api/v1/planning/roadmaps/{id}/publish
GET    /api/v1/planning/roadmaps/{id}/metrics
POST   /api/v1/planning/roadmaps/{id}/archive
GET    /api/v1/planning/roadmaps/{id}/timeline
POST   /api/v1/planning/roadmaps/{id}/clone
```

### Phases (38 endpoints)
```
GET    /api/v1/planning/phases
POST   /api/v1/planning/phases
GET    /api/v1/planning/phases/{id}
PUT    /api/v1/planning/phases/{id}
DELETE /api/v1/planning/phases/{id}
... (33 more)
```

### Sprints (50 endpoints)
```
GET    /api/v1/planning/sprints
POST   /api/v1/planning/sprints
GET    /api/v1/planning/sprints/{id}
PUT    /api/v1/planning/sprints/{id}
DELETE /api/v1/planning/sprints/{id}
... (45 more)
```

### Backlog (50 endpoints)
```
GET    /api/v1/planning/backlog
POST   /api/v1/planning/backlog
GET    /api/v1/planning/backlog/{id}
PUT    /api/v1/planning/backlog/{id}
DELETE /api/v1/planning/backlog/{id}
... (45 more)
```

---

## 🔍 By HTTP Method

### GET (341 endpoints)
- Resource retrieval
- List operations
- Status checks
- Example: `GET /api/v1/gates`, `GET /api/v1/projects`

### POST (240 endpoints)
- Resource creation
- Action triggers
- Example: `POST /api/v1/auth/login`, `POST /api/v1/gates`

### DELETE (23 endpoints)
- Resource deletion
- Example: `DELETE /api/v1/gates/{id}`

### PUT (22 endpoints)
- Full updates
- Example: `PUT /api/v1/gates/{id}`

### PATCH (10 endpoints)
- Partial updates
- Example: `PATCH /api/v1/projects/{id}`

---

## 🔐 Security Endpoints

### OAuth & Authentication
```
POST   /api/v1/auth/github/callback
POST   /api/v1/auth/google/callback
POST   /api/v1/auth/microsoft/callback
```

### MFA
```
POST   /api/v1/auth/mfa/enable
POST   /api/v1/auth/mfa/verify
POST   /api/v1/auth/mfa/disable
GET    /api/v1/auth/mfa/backup-codes
```

### API Keys
```
GET    /api/v1/api-keys
POST   /api/v1/api-keys
DELETE /api/v1/api-keys/{id}
POST   /api/v1/api-keys/{id}/rotate
GET    /api/v1/api-keys/{id}/usage
```

---

## 📊 Monitoring & Analytics

### Analytics (22 endpoints)
```
GET    /api/v1/analytics/dora
GET    /api/v1/analytics/velocity
GET    /api/v1/analytics/quality
GET    /api/v1/analytics/gates
POST   /api/v1/analytics/custom
```

### Telemetry (12 endpoints)
```
POST   /api/v1/telemetry/events
GET    /api/v1/telemetry/metrics
GET    /api/v1/telemetry/traces
```

### MCP Analytics (10 endpoints)
```
GET    /api/v1/mcp/analytics
POST   /api/v1/mcp/events
GET    /api/v1/mcp/usage
```

---

## 🌐 Integration Endpoints

### GitHub (13 endpoints)
```
POST   /api/v1/github/connect
GET    /api/v1/github/repos
POST   /api/v1/github/webhook
GET    /api/v1/github/issues
POST   /api/v1/github/pr
```

### SAST / Semgrep (14 endpoints)
```
POST   /api/v1/sast/scan
GET    /api/v1/sast/scans
GET    /api/v1/sast/scans/{id}
GET    /api/v1/sast/scans/{id}/findings
```

### AI Providers (10 endpoints)
```
GET    /api/v1/ai-providers
POST   /api/v1/ai-providers/test
GET    /api/v1/ai-providers/{id}/health
GET    /api/v1/ai-providers/{id}/usage
```

---

## 📁 File Locations

### Full Documentation
```
docs/backend/API-ENDPOINTS-FULL.md          # 28,157 lines - Complete details
docs/backend/API-ENDPOINTS-TOON.md          # 166 lines - Quick summary
docs/backend/API-ENDPOINTS-COMPACT.md       # ~1,300 lines - Table format
docs/backend/API-ENDPOINTS-ULTRA-COMPACT.md # ~700 lines - One-line format
docs/backend/API-ENDPOINTS-SUMMARY-TABLE.md # This file - Top endpoints
```

### Live Access
```
Swagger UI:   http://localhost:8300/api/docs
OpenAPI Spec: http://localhost:8300/api/openapi.json
ReDoc:        http://localhost:8300/api/redoc
```

---

## ✅ Usage Examples

### Test Authentication
```bash
# Register
curl -X POST http://localhost:8300/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"Test123456"}'

# Login
curl -X POST http://localhost:8300/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"Test123456"}'

# Use token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8300/api/v1/gates
```

---

**Generated**: 2026-02-21
**Format**: TOON (Token-Optimized)
**Total Endpoints**: 636
**Services**: 96
**Status**: ✅ Production-Ready
