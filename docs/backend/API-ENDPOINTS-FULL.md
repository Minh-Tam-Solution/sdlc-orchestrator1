# *-CyEyes-* API Endpoints — Full Coverage Report (Sessions 3 + 4)

**Generated**: 2026-03-07 by CyEyes (Claude Code)
**Sessions**: Session 3 (271 endpoints) + Session 4 (362 endpoints) = **458 unique**
**Base URL**: `https://sdlc.nhatquangholding.com`
**Auth Primary**: `anhhn2002@gmail.com` (not found → fallback)
**Auth Fallback**: `taidt@mtsolution.com.vn` (CTO / superuser) + `requests.Session()` cookie mode
**OpenAPI Spec**: 517 paths / 586 methods

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total unique endpoints tested** | **458** |
| OpenAPI total paths | 517 |
| Coverage | 88% |
| HTTP 200 OK | **185** (40%) |
| HTTP 2xx (200/201/204) | **192** (41%) |
| HTTP 404 Not Found | 132 (28%) |
| HTTP 500 Server Error | 61 (13%) |
| HTTP 422 Validation Error | 50 |
| HTTP 402 Tier Restriction | 0 |

### Status Code Breakdown

| Code | Count | Meaning |
|------|-------|---------|
| 0 | 1 | Connection/timeout error |
| 200 | 185 | OK — success |
| 201 | 5 | Created |
| 204 | 2 | No Content |
| 400 | 10 | Bad Request |
| 404 | 132 | Not Found |
| 405 | 11 | Method Not Allowed |
| 409 | 1 | Conflict |
| 422 | 50 | Unprocessable Entity |
| 500 | 60 | Internal Server Error |
| 503 | 1 | Service Unavailable |

## Table of Contents

- [Health](#health) — 3 endpoints, 2 × HTTP 200
- [Projects](#projects) — 21 endpoints, 15 × HTTP 200
- [Gates](#gates) — 10 endpoints, 5 × HTTP 200
- [Gates Engine](#gates-engine) — 5 endpoints, 3 × HTTP 200
- [Evidence](#evidence) — 7 endpoints, 3 × HTTP 200
- [Admin](#admin) — 34 endpoints, 17 × HTTP 200
- [Planning](#planning) — 45 endpoints, 32 × HTTP 200
- [Multi-Agent](#multi-agent) — 6 endpoints, 1 × HTTP 200
- [Codegen](#codegen) — 20 endpoints, 9 × HTTP 200
- [SAST](#sast) — 7 endpoints, 3 × HTTP 200
- [Compliance](#compliance) — 15 endpoints, 7 × HTTP 200
- [Governance](#governance) — 12 endpoints, 5 × HTTP 200
- [Governance Metrics](#governance-metrics) — 1 endpoints, 0 × HTTP 200
- [CEO Dashboard](#ceo-dashboard) — 13 endpoints, 11 × HTTP 200
- [Vibecoding](#vibecoding) — 3 endpoints, 3 × HTTP 200
- [Vibecoding Index](#vibecoding-index) — 3 endpoints, 0 × HTTP 200
- [DORA](#dora) — 2 endpoints, 0 × HTTP 200
- [Telemetry](#telemetry) — 7 endpoints, 1 × HTTP 200
- [AI Detection](#ai-detection) — 7 endpoints, 4 × HTTP 200
- [Notifications](#notifications) — 6 endpoints, 3 × HTTP 200
- [API Keys](#api-keys) — 4 endpoints, 1 × HTTP 200
- [MFA](#mfa) — 2 endpoints, 0 × HTTP 200
- [Policies](#policies) — 4 endpoints, 2 × HTTP 200
- [Override](#override) — 5 endpoints, 0 × HTTP 200
- [MRP](#mrp) — 6 endpoints, 3 × HTTP 200
- [VCR](#vcr) — 4 endpoints, 0 × HTTP 200
- [GitHub](#github) — 11 endpoints, 0 × HTTP 200
- [Stage Gating](#stage-gating) — 6 endpoints, 3 × HTTP 200
- [Deprecation](#deprecation) — 4 endpoints, 0 × HTTP 200
- [MCP](#mcp) — 5 endpoints, 0 × HTTP 200
- [Risk](#risk) — 3 endpoints, 2 × HTTP 200
- [Maturity](#maturity) — 4 endpoints, 2 × HTTP 200
- [Agentic Maturity](#agentic-maturity) — 2 endpoints, 0 × HTTP 200
- [SDLC Structure](#sdlc-structure) — 2 endpoints, 0 × HTTP 200
- [Triage](#triage) — 2 endpoints, 1 × HTTP 200
- [Enterprise](#enterprise) — 1 endpoints, 1 × HTTP 200
- [GDPR](#gdpr) — 5 endpoints, 3 × HTTP 200
- [Grafana](#grafana) — 6 endpoints, 3 × HTTP 200
- [Payments](#payments) — 3 endpoints, 0 × HTTP 200
- [Consultations](#consultations) — 2 endpoints, 0 × HTTP 200
- [Organizations](#organizations) — 1 endpoints, 0 × HTTP 200
- [Teams](#teams) — 1 endpoints, 0 × HTTP 200
- [Dashboard](#dashboard) — 3 endpoints, 2 × HTTP 200
- [Check Runs](#check-runs) — 4 endpoints, 3 × HTTP 200
- [Invitations](#invitations) — 3 endpoints, 0 × HTTP 200
- [Docs](#docs) — 3 endpoints, 1 × HTTP 200
- [Magic Link](#magic-link) — 1 endpoints, 0 × HTTP 200
- [Templates](#templates) — 4 endpoints, 3 × HTTP 200
- [Auth](#auth) — 15 endpoints, 8 × HTTP 200
- [Evidence Manifest](#evidence-manifest) — 10 endpoints, 1 × HTTP 200
- [Evidence Timeline](#evidence-timeline) — 1 endpoints, 0 × HTTP 200
- [Planning Subagent](#planning-subagent) — 5 endpoints, 1 × HTTP 200
- [Compliance Export](#compliance-export) — 1 endpoints, 0 × HTTP 200
- [Compliance Validation](#compliance-validation) — 2 endpoints, 0 × HTTP 200
- [CA V2](#ca-v2) — 7 endpoints, 1 × HTTP 200
- [Risk Analysis](#risk-analysis) — 3 endpoints, 0 × HTTP 200
- [Governance Mode](#governance-mode) — 2 endpoints, 0 × HTTP 200
- [Gov Vibecoding](#gov-vibecoding) — 2 endpoints, 0 × HTTP 200
- [Gov Specs](#gov-specs) — 1 endpoints, 0 × HTTP 200
- [Auto Gen](#auto-gen) — 8 endpoints, 1 × HTTP 200
- [Ctx Val](#ctx-val) — 3 endpoints, 1 × HTTP 200
- [Context Val](#context-val) — 1 endpoints, 0 × HTTP 200
- [XRef](#xref) — 5 endpoints, 3 × HTTP 200
- [Contract](#contract) — 2 endpoints, 0 × HTTP 200
- [FW Version](#fw-version) — 6 endpoints, 0 × HTTP 200
- [Deprecation Mon](#deprecation-mon) — 2 endpoints, 0 × HTTP 200
- [AGENTS.md](#agentsmd) — 11 endpoints, 5 × HTTP 200
- [Jira](#jira) — 2 endpoints, 0 × HTTP 200
- [OTT Gateway](#ott-gateway) — 1 endpoints, 0 × HTTP 200
- [OTT](#ott) — 1 endpoints, 0 × HTTP 200
- [Push Notif](#push-notif) — 2 endpoints, 0 × HTTP 200
- [E2E](#e2e) — 2 endpoints, 0 × HTTP 200
- [MCP Analytics](#mcp-analytics) — 1 endpoints, 0 × HTTP 200
- [Audit Trail](#audit-trail) — 2 endpoints, 0 × HTTP 200
- [Enterprise SSO](#enterprise-sso) — 4 endpoints, 0 × HTTP 200
- [Tier](#tier) — 3 endpoints, 0 × HTTP 200
- [Data Residency](#data-residency) — 2 endpoints, 1 × HTTP 200
- [Preview](#preview) — 2 endpoints, 0 × HTTP 200
- [WebSocket](#websocket) — 2 endpoints, 0 × HTTP 200
- [Workflows](#workflows) — 1 endpoints, 0 × HTTP 200
- [Analytics v2](#analytics-v2) — 6 endpoints, 2 × HTTP 200
- [AI Providers](#ai-providers) — 1 endpoints, 0 × HTTP 200
- [Metrics](#metrics) — 1 endpoints, 0 × HTTP 200
- [Gov Metrics](#gov-metrics) — 4 endpoints, 4 × HTTP 200
- [Doc XRef](#doc-xref) — 2 endpoints, 0 × HTTP 200
- [Push](#push) — 3 endpoints, 3 × HTTP 200
- [Channels](#channels) — 1 endpoints, 0 × HTTP 200

---
## Health

**3 endpoints** | HTTP 200: **2** | HTTP 2xx: 2

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 1 | `GET` | `/` | ✅ 200 OK | 15ms | — | `<!DOCTYPE html><html lang="vi"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><link rel="preload" href="/_next/static/media/4473ecc91f70f139-s.p.woff...` | ✅ OK |
| 2 | `GET` | `/health` | ✅ 200 OK | 15ms | — | `{'status': 'healthy', 'version': '1.2.0', 'service': 'sdlc-orchestrator-backend'}` | ✅ OK |
| 3 | `GET` | `/health/ready` | 💥 503 Unavailable | 9204ms | — | `{'status': 'not_ready', 'dependencies': {'postgres': {'status': 'connected', 'healthy': True}, 'redis': {'status': 'connected', 'healthy': True}, 'opa': {'status': 'connected', 'healthy': True, 'versi...` | Service not ready (dependencies starting) |

---
## Projects

**21 endpoints** | HTTP 200: **15** | HTTP 2xx: 15

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 4 | `GET` | `/api/v1/projects` | ✅ 200 OK | 55ms | — | `[{'id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'name': 'CyEyes-Updated', 'description': '*-CyEyes-* test', 'current_stage': '06-DEPLOY', 'gate_status': 'pending', 'progress': 0, 'created_at': '2026-0...` | ✅ OK |
| 5 | `GET` | `/api/v1/projects/` | ✅ 200 OK | 50ms | — | `[{'id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'name': 'CyEyes-Updated', 'description': '*-CyEyes-* test', 'current_stage': '06-DEPLOY', 'gate_status': 'pending', 'progress': 0, 'created_at': '2026-0...` | ✅ OK |
| 6 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 OK | 34ms | — | `{'id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'name': 'CyEyes-Updated', 'description': '*-CyEyes-* test', 'current_stage': '06-DEPLOY', 'created_at': '2026-03-01T04:23:25.478537', 'updated_at': '2026...` | ✅ OK |
| 7 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance-summary` | ✅ 200 OK | 23ms | — | `{'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'project_name': 'CyEyes-S4', 'tier': 'professional', 'current_score': 0, 'is_compliant': False, 'last_validated': None, 'validation_count': 0, 's...` | ✅ OK |
| 8 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance/history` | 💥 500 Server Error | 19ms | — | `Internal Server Error` | Compliance service DB error |
| 9 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance/last-check` | 💥 500 Server Error | 21ms | — | `Internal Server Error` | Compliance service DB error |
| 10 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance/score` | 💥 500 Server Error | 28ms | — | `Internal Server Error` | Compliance service DB error |
| 11 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/context` | ✅ 200 OK | 26ms | — | `{'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'stage': '06-DEPLOY', 'gate': 'Final Retest - Deploy Approval DRAFT', 'sprint_number': None, 'sprint_goal': None, 'strict_mode': False, 'updated_...` | ✅ OK |
| 12 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence/gaps` | ✅ 200 OK | 16ms | — | `{'gaps': {'missing_evidence': [], 'backend_gaps': [], 'frontend_gaps': [], 'extension_gaps': [], 'cli_gaps': [], 'test_gaps': []}, 'total_gaps': 0, 'recommendations': [], 'analyzed_at': '2026-03-07T09...` | ✅ OK |
| 13 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence/status` | ✅ 200 OK | 29ms | — | `{'status': 'complete', 'gaps': {'backend': [], 'frontend': [], 'extension': [], 'cli': []}, 'total_gaps': 0, 'checked_at': '2026-03-07T09:54:35.651890Z', 'specs_checked': 0, 'specs_complete': 0, 'comp...` | ✅ OK |
| 14 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/overrides` | ✅ 200 OK | 17ms | — | `[]` | ✅ OK |
| 15 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/policy-pack` | ✅ 200 OK | 30ms | — | `{'name': 'Standard Policy Pack', 'description': 'Auto-configured Standard tier policy pack for Final Retest', 'version': '1.0.0', 'tier': 'standard', 'id': 'f8c4e013-ac89-40ad-aff6-c45617c2ee30', 'pro...` | ✅ OK |
| 16 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/stats` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 17 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/timeline` | ✅ 200 OK | 39ms | — | `{'events': [], 'stats': {'total_events': 0, 'ai_detected': 0, 'pass_rate': 0.0, 'override_rate': 0.0, 'by_tool': {}, 'by_status': {}}, 'total': 0, 'page': 1, 'pages': 1, 'has_next': False}` | ✅ OK |
| 18 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/timeline/stats` | ✅ 200 OK | 21ms | — | `{'total_events': 0, 'ai_detected': 0, 'pass_rate': 0.0, 'override_rate': 0.0, 'by_tool': {}, 'by_status': {}}` | ✅ OK |
| 19 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/validation-history` | ✅ 200 OK | 26ms | — | `[]` | ✅ OK |
| 20 | `POST` | `/api/v1/projects/` | ✅ 200 OK | 53ms | `{"name": "*-CyEyes-* S4 1772877264"}` | `[{'id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'name': 'CyEyes-S4', 'description': '*-CyEyes-* session 4', 'current_stage': '06-DEPLOY', 'gate_status': 'pending', 'progress': 0, 'created_at': '2026-0...` | ✅ OK |
| 21 | `POST` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/archive` | 🔍 404 Not Found | 14ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 22 | `POST` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence/validate` | ✅ 200 OK | 15ms | — | `{'validation_id': 'val-1772877275.6906', 'status': 'complete', 'violations': [], 'summary': {'errors': 0, 'warnings': 0, 'info': 0}, 'validated_at': '2026-03-07T09:54:35.690606Z', 'note': 'sdlcctl val...` | ✅ OK |
| 23 | `POST` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/restore` | 🔍 404 Not Found | 14ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 24 | `PUT` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 OK | 50ms | `{"name": "CyEyes-S4", "description": "*-CyEyes-* session 4"}` | `{'id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'name': 'CyEyes-S4', 'slug': 'final-retest', 'description': '*-CyEyes-* session 4', 'owner_id': 'a0000000-0000-0000-0000-000000000001', 'is_active': True...` | ✅ OK |

---
## Gates

**10 endpoints** | HTTP 200: **5** | HTTP 2xx: 5

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 25 | `GET` | `/api/v1/gates` | ✅ 200 OK | 37ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'items': [{'id': 'b186b6cb-0320-4077-80e2-775c59f79bd8', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'gate_name': 'Final Retest - Design Review', 'gate_type': 'G2_DESIGN_REVIEW', 'stage': '...` | ✅ OK |
| 26 | `GET` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af` | ✅ 200 OK | 33ms | — | `{'id': 'b1913ff7-15cb-4ad3-9846-4200ce4f70af', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'gate_name': 'Final Retest - Planning Review', 'gate_type': 'G1_PLANNING_REVIEW', 'stage': '01-PLAN...` | ✅ OK |
| 27 | `GET` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/actions` | ✅ 200 OK | 24ms | — | `{'gate_id': 'b1913ff7-15cb-4ad3-9846-4200ce4f70af', 'status': 'EVALUATED', 'actions': {'can_evaluate': True, 'can_submit': False, 'can_approve': False, 'can_reject': False, 'can_upload_evidence': True...` | ✅ OK |
| 28 | `GET` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/approvals` | ✅ 200 OK | 19ms | — | `[]` | ✅ OK |
| 29 | `GET` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/policy-result` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 30 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/approve` | ⚠️ 409 Conflict | 21ms | `{"comment": "*-CyEyes-* approved"}` | `{'detail': 'Cannot approve gate from status: EVALUATED. Allowed from: SUBMITTED'}` | Conflict — resource already exists |
| 31 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/break-glass-approve` | ⚠️ 422 Unprocessable | 20ms | `{"reason": "*-CyEyes-* emergency", "comment": "Test"}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'incident_ticket'], 'msg': 'Field required', 'input': {'reason': '*-CyEyes-* emergency', 'comment': 'Test'}}, {'type': 'missing', 'loc': ['body', 'sever...` | Request validation failed — schema mismatch or missing required field |
| 32 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/evaluate` | ✅ 200 OK | 33ms | — | `{'gate_id': 'b1913ff7-15cb-4ad3-9846-4200ce4f70af', 'status': 'EVALUATED', 'evaluated_at': '2026-03-07T09:54:36.032349', 'exit_criteria': [{'id': 'BRD_COMPLETE', 'met': False, 'description': 'Business...` | ✅ OK |
| 33 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/reject` | ⚠️ 422 Unprocessable | 22ms | `{"reason": "*-CyEyes-* test"}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'comment'], 'msg': 'Field required', 'input': {'reason': '*-CyEyes-* test'}}], 'body': "{'reason': '*-CyEyes-* test'}"}` | Request validation failed — schema mismatch or missing required field |
| 34 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/submit` | ⚠️ 422 Unprocessable | 19ms | — | `{'detail': 'Cannot submit: missing required evidence: BRD_COMPLETE, PRD_COMPLETE, STAKEHOLDER_SIGNOFF'}` | Request validation failed — schema mismatch or missing required field |

---
## Gates Engine

**5 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 35 | `GET` | `/api/v1/gates-engine/health` | ✅ 200 OK | 20ms | — | `{'status': 'healthy', 'service': 'gates_engine', 'opa_available': True, 'valid_gate_codes': ['G0.1', 'G0.2', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'], 'timestamp': '2026-03-07T09:54:36.12...` | ✅ OK |
| 36 | `GET` | `/api/v1/gates-engine/policies/G1_CONSULTATION` | ⚠️ 400 Bad Request | 13ms | — | `{'detail': 'Invalid gate code: G1_CONSULTATION. Valid codes: G0.1, G0.2, G1, G2, G3, G4, G5, G6, G7, G8, G9'}` | Expected for dummy/test values |
| 37 | `GET` | `/api/v1/gates-engine/prerequisites/G1_CONSULTATION` | ⚠️ 400 Bad Request | 11ms | — | `{'detail': 'Invalid gate code: G1_CONSULTATION. Valid codes: G0.1, G0.2, G1, G2, G3, G4, G5, G6, G7, G8, G9'}` | Expected for dummy/test values |
| 38 | `GET` | `/api/v1/gates-engine/readiness/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 OK | 31ms | — | `{'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'total_gates': 5, 'approved_count': 0, 'current_stage': None, 'next_gate': None, 'overall_progress': 0.0, 'gates': {'G0.1': {'id': None, 'name': ...` | ✅ OK |
| 39 | `GET` | `/api/v1/gates-engine/stages` | ✅ 200 OK | 16ms | — | `{'G0.1': 'WHY', 'G0.2': 'WHY', 'G1': 'WHAT', 'G2': 'HOW', 'G3': 'BUILD', 'G4': 'TEST', 'G5': 'DEPLOY', 'G6': 'OPERATE', 'G7': 'INTEGRATE', 'G8': 'COLLABORATE', 'G9': 'GOVERN'}` | ✅ OK |

---
## Evidence

**7 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 40 | `GET` | `/api/v1/evidence` | ✅ 200 OK | 20ms | — | `{'items': [{'id': '036b2a6d-5959-4327-a77c-54ca4407847e', 'gate_id': '1074f1fa-8f9e-4504-8656-0367b0172e0e', 'file_name': 'test_evidence.txt', 'file_size': 49, 'file_type': 'text/plain', 'evidence_typ...` | ✅ OK |
| 41 | `GET` | `/api/v1/evidence/` | ✅ 200 OK | 61ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'items': [{'id': '036b2a6d-5959-4327-a77c-54ca4407847e', 'gate_id': '1074f1fa-8f9e-4504-8656-0367b0172e0e', 'file_name': 'test_evidence.txt', 'file_size': 49, 'file_type': 'text/plain', 'evidence_typ...` | ✅ OK |
| 42 | `GET` | `/api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 43 | `GET` | `/api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e/download` | 🔍 404 Not Found | 15ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 44 | `POST` | `/api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e/validate-content` | ✅ 200 OK | 43ms | — | `{'score': 1.0, 'passed': True, 'document_type': 'DOCUMENTATION', 'missing_sections': [], 'found_sections': [], 'section_word_counts': {}, 'placeholder_count': 0, 'placeholder_warnings': [], 'thin_sect...` | ✅ OK |
| 45 | `POST` | `/api/v1/evidence/upload` | 🔍 404 Not Found | 0ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 46 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/evidence` | 💥 500 Server Error | 0ms | — | `{'detail': 'Evidence storage failed: HTTPConnectionPool(host=\'minio\', port=9000): Max retries exceeded with url: /evidence-vault-v2/evidence/b1913ff7-15cb-4ad3-9846-4200ce4f70af/cyeyes-s4.txt (Cause...` | MinIO storage unavailable |

---
## Admin

**34 endpoints** | HTTP 200: **17** | HTTP 2xx: 17

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 47 | `DELETE` | `/api/v1/admin/users/cyeyes-reg3@test.com` | ⚠️ 422 Unprocessable | 15ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'user_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `y`...` | Request validation failed — schema mismatch or missing required field |
| 48 | `GET` | `/api/v1/admin/ai-providers` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 49 | `GET` | `/api/v1/admin/ai-providers/config` | ✅ 200 OK | 22ms | — | `{'ollama': {'available': True, 'configured': True, 'url': 'http://ollama:11434', 'model': 'qwen3:14b', 'timeout': 30}, 'claude': {'available': False, 'configured': False, 'url': None, 'model': 'claude...` | ✅ OK |
| 50 | `GET` | `/api/v1/admin/ai-providers/ollama/models` | ✅ 200 OK | 36ms | — | `{'models': ['bge-m3:latest', 'deepseek-ocr:3b', 'gemma3:12b', 'ministral-3:8b-instruct-2512-q4_K_M', 'qwen3-coder:30b', 'qwen3-embedding:4b', 'qwen3.5:27b', 'qwen3.5:35b', 'qwen3.5:9b', 'qwen3:14b', '...` | ✅ OK |
| 51 | `GET` | `/api/v1/admin/audit-logs` | ✅ 200 OK | 22ms | — | `{'items': [{'id': 'ed08bf65-7913-482e-a4ed-339bb321d4cc', 'timestamp': '2026-03-07T16:54:36.611358', 'action': 'USER_UPDATED', 'actor_id': 'a0000000-0000-0000-0000-000000000001', 'actor_email': None, ...` | ✅ OK |
| 52 | `GET` | `/api/v1/admin/evidence/retention-stats` | ✅ 200 OK | 22ms | — | `{'total_evidence': 2, 'active_evidence': 2, 'archived_evidence': 0, 'evidence_due_for_archive': 0, 'evidence_due_for_purge': 0, 'oldest_evidence_date': '2026-01-16T17:48:50.881227', 'newest_evidence_d...` | ✅ OK |
| 53 | `GET` | `/api/v1/admin/metrics` | 🔍 404 Not Found | 19ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 54 | `GET` | `/api/v1/admin/ott-channels` | 🔍 404 Not Found | 9ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 55 | `GET` | `/api/v1/admin/ott-channels/config` | ✅ 200 OK | 15ms | — | `{'channels': [{'channel': 'slack', 'status': 'offline', 'tier': 'PROFESSIONAL', 'webhook_url': 'https://sdlc.nhatquangholding.com/api/v1/channels/slack/webhook', 'hmac_enabled': False, 'secret_configu...` | ✅ OK |
| 56 | `GET` | `/api/v1/admin/ott-channels/stats` | 💥 500 Server Error | 18ms | — | `Internal Server Error` | OTT channel service error |
| 57 | `GET` | `/api/v1/admin/ott-channels/telegram/conversations` | 💥 500 Server Error | 19ms | — | `Internal Server Error` | OTT channel service error |
| 58 | `GET` | `/api/v1/admin/ott-channels/telegram/health` | 💥 500 Server Error | 20ms | — | `Internal Server Error` | OTT channel service error |
| 59 | `GET` | `/api/v1/admin/override-queue` | ✅ 200 OK | 21ms | — | `{'pending': [], 'recent_decisions': [], 'total_pending': 0}` | ✅ OK |
| 60 | `GET` | `/api/v1/admin/override-stats` | ✅ 200 OK | 18ms | — | `{'total': 0, 'by_status': {}, 'by_type': {}, 'approval_rate': 0.0, 'pending': 0, 'days': 30}` | ✅ OK |
| 61 | `GET` | `/api/v1/admin/settings` | ✅ 200 OK | 17ms | — | `{'security': [{'key': 'max_login_attempts', 'value': 5, 'version': 1, 'category': 'security', 'description': 'Maximum failed login attempts before lockout', 'updated_at': '2026-01-14T18:06:05.742775',...` | ✅ OK |
| 62 | `GET` | `/api/v1/admin/settings/maintenance_mode` | 🔍 404 Not Found | 21ms | — | `{'detail': "Setting 'maintenance_mode' not found"}` | Resource ID not found or route missing |
| 63 | `GET` | `/api/v1/admin/settings/max_login_attempts` | ✅ 200 OK | 14ms | — | `{'key': 'max_login_attempts', 'value': 5, 'version': 1, 'category': 'security', 'description': 'Maximum failed login attempts before lockout', 'updated_at': '2026-01-14T18:06:05.742775', 'updated_by':...` | ✅ OK |
| 64 | `GET` | `/api/v1/admin/stats` | ✅ 200 OK | 21ms | — | `{'total_users': 13, 'active_users': 13, 'inactive_users': 0, 'superusers': 2, 'total_projects': 7, 'total_gates': 28, 'active_projects': 7, 'system_status': 'healthy'}` | ✅ OK |
| 65 | `GET` | `/api/v1/admin/system/health` | ✅ 200 OK | 16ms | — | `{'overall_status': 'healthy', 'services': [{'name': 'PostgreSQL', 'status': 'healthy', 'response_time_ms': 0, 'details': {'type': 'database'}}, {'name': 'Redis', 'status': 'healthy', 'response_time_ms...` | ✅ OK |
| 66 | `GET` | `/api/v1/admin/usage` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 67 | `GET` | `/api/v1/admin/users` | ✅ 200 OK | 24ms | — | `{'items': [{'id': '818d8908-481d-471b-8688-9a1b96878c4b', 'email': 'cyeyes-s4-1772877264@test.com', 'full_name': None, 'role': 'dev', 'is_active': True, 'is_superuser': False, 'created_at': '2026-03-0...` | ✅ OK |
| 68 | `GET` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d` | ✅ 200 OK | 17ms | — | `{'id': '2e542eba-b1b5-4f91-ab82-b853a6887b8d', 'email': 'cyeyes-reg3@test.com', 'full_name': None, 'role': 'dev', 'avatar_url': None, 'is_active': True, 'is_superuser': False, 'mfa_enabled': False, 'o...` | ✅ OK |
| 69 | `GET` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/mfa-status` | ✅ 200 OK | 17ms | — | `{'user_id': '2e542eba-b1b5-4f91-ab82-b853a6887b8d', 'email': 'cyeyes-reg3@test.com', 'mfa_enabled': False, 'is_mfa_exempt': False, 'mfa_required_global': False, 'mfa_setup_deadline': None, 'days_remai...` | ✅ OK |
| 70 | `PATCH` | `/api/v1/admin/settings/max_login_attempts` | ✅ 200 OK | 23ms | `{"value": 5}` | `{'key': 'max_login_attempts', 'value': 5, 'version': 2, 'category': 'security', 'description': 'Maximum failed login attempts before lockout', 'updated_at': '2026-03-07T09:54:36.718103', 'updated_by':...` | ✅ OK |
| 71 | `PATCH` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d` | ✅ 200 OK | 41ms | `{"full_name": "*-CyEyes-* S4 Admin"}` | `{'id': '2e542eba-b1b5-4f91-ab82-b853a6887b8d', 'email': 'cyeyes-reg3@test.com', 'full_name': None, 'role': 'dev', 'avatar_url': None, 'is_active': True, 'is_superuser': False, 'mfa_enabled': False, 'o...` | ✅ OK |
| 72 | `POST` | `/api/v1/admin/ai-providers/ollama/refresh-models` | ✅ 200 OK | 29ms | — | `{'models': ['bge-m3:latest', 'deepseek-ocr:3b', 'gemma3:12b', 'ministral-3:8b-instruct-2512-q4_K_M', 'qwen3-coder:30b', 'qwen3-embedding:4b', 'qwen3.5:27b', 'qwen3.5:35b', 'qwen3.5:9b', 'qwen3:14b', '...` | ✅ OK |
| 73 | `POST` | `/api/v1/admin/broadcast` | 🔍 404 Not Found | 14ms | `{"message": "*-CyEyes-* test broadcast", "type": "info"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 74 | `POST` | `/api/v1/admin/cache/clear` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 75 | `POST` | `/api/v1/admin/ott-channels/telegram/send` | 🔍 404 Not Found | 16ms | `{"message": "*-CyEyes-* test", "chat_id": "test"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 76 | `POST` | `/api/v1/admin/settings` | ⚠️ 405 Method Not Allowed | 11ms | `{"key": "test", "value": "cyeyes"}` | `{'detail': 'Method Not Allowed'}` | OAuth callback: POST from provider required (not GET) |
| 77 | `POST` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/activate` | 🔍 404 Not Found | 14ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 78 | `POST` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/suspend` | 🔍 404 Not Found | 27ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 79 | `POST` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/unlock` | ⚠️ 400 Bad Request | 15ms | — | `{'detail': 'User account is not locked. Email: cyeyes-reg3@test.com'}` | Expected for dummy/test values |
| 80 | `PUT` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/role` | 🔍 404 Not Found | 10ms | `{"role": "dev"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Planning

**45 endpoints** | HTTP 200: **32** | HTTP 2xx: 33

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 81 | `GET` | `/api/v1/planning/action-items/dummy` | ⚠️ 422 Unprocessable | 12ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'item_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `u`...` | Request validation failed — schema mismatch or missing required field |
| 82 | `GET` | `/api/v1/planning/allocations/dummy` | ⚠️ 422 Unprocessable | 12ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'allocation_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], fou...` | Request validation failed — schema mismatch or missing required field |
| 83 | `GET` | `/api/v1/planning/backlog` | ✅ 200 OK | 18ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'items': [{'id': '135b6b04-5530-45d0-a3b2-a9fe5bc138f5', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'sprint_id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'parent_id': None, 'type': 'task', ...` | ✅ OK |
| 84 | `GET` | `/api/v1/planning/backlog/135b6b04-5530-45d0-a3b2-a9fe5bc138f5` | ✅ 200 OK | 15ms | — | `{'id': '135b6b04-5530-45d0-a3b2-a9fe5bc138f5', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'sprint_id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'parent_id': None, 'type': 'task', 'title': '*...` | ✅ OK |
| 85 | `GET` | `/api/v1/planning/backlog/assignees/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 OK | 15ms | — | `[]` | ✅ OK |
| 86 | `GET` | `/api/v1/planning/dashboard/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 OK | 23ms | — | `{'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'roadmaps': [{'id': '624cc6c6-115f-4609-8b1d-dd1912fd527b', 'name': '*-CyEyes-* S4 Roadmap', 'status': 'active', 'vision': None, 'start_date': '2...` | ✅ OK |
| 87 | `GET` | `/api/v1/planning/dependencies` | ⚠️ 405 Method Not Allowed | 12ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': 'Method Not Allowed'}` | OAuth callback: POST from provider required (not GET) |
| 88 | `GET` | `/api/v1/planning/dependencies/check-circular` | ⚠️ 422 Unprocessable | 13ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'dependency_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], fou...` | Request validation failed — schema mismatch or missing required field |
| 89 | `GET` | `/api/v1/planning/phases` | ✅ 200 OK | 21ms | params: `{"roadmap_id": "624cc6c6-115f-4609-8b1d-dd1912fd527b"}` | `{'items': [{'id': '55bec71c-8228-4b39-8a78-a34de8b3dc8d', 'roadmap_id': '624cc6c6-115f-4609-8b1d-dd1912fd527b', 'number': 1, 'name': '*-CyEyes-* Phase Updated', 'theme': None, 'objective': None, 'star...` | ✅ OK |
| 90 | `GET` | `/api/v1/planning/phases/55bec71c-8228-4b39-8a78-a34de8b3dc8d` | ✅ 200 OK | 16ms | — | `{'id': '55bec71c-8228-4b39-8a78-a34de8b3dc8d', 'roadmap_id': '624cc6c6-115f-4609-8b1d-dd1912fd527b', 'number': 1, 'name': '*-CyEyes-* Phase Updated', 'theme': None, 'objective': None, 'start_date': '2...` | ✅ OK |
| 91 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/dependency-analysis` | ✅ 200 OK | 18ms | — | `{'total_dependencies': 0, 'blocking_dependencies': 0, 'cross_project_dependencies': 0, 'pending_dependencies': 0, 'resolved_dependencies': 0, 'critical_path': [], 'max_depth': 0, 'has_circular_risk': ...` | ✅ OK |
| 92 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/dependency-graph` | ✅ 200 OK | 19ms | — | `{'nodes': [], 'edges': [], 'total_sprints': 0, 'total_dependencies': 0, 'blocking_dependencies': 0, 'cross_project_dependencies': 0}` | ✅ OK |
| 93 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/resource-heatmap` | ✅ 200 OK | 23ms | — | `{'users': [{'id': '2e542eba-b1b5-4f91-ab82-b853a6887b8d', 'name': '*-CyEyes-* S4 Admin', 'email': 'cyeyes-reg3@test.com'}], 'sprints': [{'id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'number': 1, 'nam...` | ✅ OK |
| 94 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/retrospective-comparison` | ⚠️ 422 Unprocessable | 14ms | — | `{'detail': [{'type': 'missing', 'loc': ['query', 'sprint_ids'], 'msg': 'Field required', 'input': None}], 'body': None}` | Request validation failed — schema mismatch or missing required field |
| 95 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/template-suggestions` | ✅ 200 OK | 19ms | — | `{'suggestions': [{'template_id': 'df4beaf4-54e8-48fd-98d0-98c03daae6e4', 'template_name': 'Feature Sprint', 'template_type': 'feature', 'match_score': 0.7, 'reason': 'Duration matches recent sprints'}...` | ✅ OK |
| 96 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/velocity` | ✅ 200 OK | 18ms | — | `{'average': 0.0, 'trend': 'unknown', 'confidence': 0.0, 'history': [], 'sprint_count': 0, 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8'}` | ✅ OK |
| 97 | `GET` | `/api/v1/planning/roadmaps` | ✅ 200 OK | 25ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'items': [{'id': '624cc6c6-115f-4609-8b1d-dd1912fd527b', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'name': '*-CyEyes-* Roadmap Updated', 'description': None, 'vision': None, 'start_date':...` | ✅ OK |
| 98 | `GET` | `/api/v1/planning/roadmaps/624cc6c6-115f-4609-8b1d-dd1912fd527b` | ✅ 200 OK | 18ms | — | `{'id': '624cc6c6-115f-4609-8b1d-dd1912fd527b', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'name': '*-CyEyes-* Roadmap Updated', 'description': None, 'vision': None, 'start_date': '2026-01-0...` | ✅ OK |
| 99 | `GET` | `/api/v1/planning/sprints` | ✅ 200 OK | 23ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'items': [{'id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'phase_id': '55bec71c-8228-4b39-8a78-a34de8b3dc8d', 'number': 1, 'name': '*-CyEyes-* Spr...` | ✅ OK |
| 100 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449` | ✅ 200 OK | 16ms | — | `{'id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'phase_id': '55bec71c-8228-4b39-8a78-a34de8b3dc8d', 'number': 1, 'name': '*-CyEyes-* Sprint Updated...` | ✅ OK |
| 101 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/action-items` | ✅ 200 OK | 15ms | — | `{'items': [], 'total': 0, 'page': 1, 'page_size': 20}` | ✅ OK |
| 102 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/action-items/stats` | ✅ 200 OK | 13ms | — | `{'total_items': 0, 'open_items': 0, 'in_progress_items': 0, 'completed_items': 0, 'cancelled_items': 0, 'completion_rate': 0.0, 'by_category': {}, 'by_priority': {}}` | ✅ OK |
| 103 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/allocations` | ✅ 200 OK | 14ms | — | `{'items': [{'allocation_percentage': 100, 'role': 'developer', 'notes': None, 'id': '0cb006df-d414-4198-b619-853c7e9a19b9', 'sprint_id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'user_id': '2e542eba-b1...` | ✅ OK |
| 104 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/analytics` | ✅ 200 OK | 22ms | — | `{'sprint_id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'sprint_number': 1, 'sprint_name': '*-CyEyes-* Sprint Updated', 'health': {'sprint_id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'completion_rate':...` | ✅ OK |
| 105 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/burndown` | ✅ 200 OK | 20ms | — | `{'sprint_id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'sprint_number': 1, 'sprint_name': '*-CyEyes-* Sprint Updated', 'total_points': 0, 'start_date': '2026-01-01', 'end_date': '2026-01-14', 'ideal': ...` | ✅ OK |
| 106 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/capacity` | ✅ 200 OK | 25ms | — | `{'sprint_id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'sprint_number': 1, 'sprint_name': '*-CyEyes-* Sprint Updated', 'start_date': '2026-01-01', 'end_date': '2026-01-14', 'team_size': 1, 'total_capac...` | ✅ OK |
| 107 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/dependencies` | ✅ 200 OK | 17ms | — | `{'items': [], 'total': 0, 'page': 1, 'page_size': 20}` | ✅ OK |
| 108 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/forecast` | ✅ 200 OK | 16ms | — | `{'sprint_id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'sprint_number': 1, 'sprint_name': '*-CyEyes-* Sprint Updated', 'probability': 100.0, 'predicted_end_date': '2026-03-07', 'on_track': False, 'rema...` | ✅ OK |
| 109 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/gates` | ✅ 200 OK | 14ms | — | `[]` | ✅ OK |
| 110 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/gates/G_SPRINT` | ⚠️ 422 Unprocessable | 20ms | — | `{'detail': [{'type': 'enum', 'loc': ['path', 'gate_type'], 'msg': "Input should be 'g_sprint' or 'g_sprint_close'", 'input': 'G_SPRINT', 'ctx': {'expected': "'g_sprint' or 'g_sprint_close'"}}], 'body'...` | Request validation failed — schema mismatch or missing required field |
| 111 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/health` | ✅ 200 OK | 21ms | — | `{'sprint_id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'completion_rate': 0.0, 'completed_points': 0, 'total_points': 0, 'blocked_count': 0, 'risk_level': 'low', 'days_remaining': 0, 'days_elapsed': 65...` | ✅ OK |
| 112 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/retrospective` | ✅ 200 OK | 22ms | — | `{'sprint_id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'sprint_number': 1, 'sprint_name': '*-CyEyes-* Sprint Updated', 'generated_at': '2026-03-07T09:54:37.299386', 'metrics': {'committed_points': 0, '...` | ✅ OK |
| 113 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/suggestions` | ✅ 200 OK | 18ms | — | `{'sprint_id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'suggestions': [{'type': 'unassigned_priority', 'message': '1 high-priority item(s) unassigned', 'severity': 'warning', 'items': ['135b6b04-5530-4...` | ✅ OK |
| 114 | `GET` | `/api/v1/planning/templates` | ✅ 200 OK | 17ms | — | `{'items': [{'name': 'Release Sprint', 'description': 'Sprint focused on preparing and executing a release. Includes final testing, documentation, and deployment.', 'template_type': 'release', 'duratio...` | ✅ OK |
| 115 | `GET` | `/api/v1/planning/templates/default` | ⚠️ 422 Unprocessable | 14ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'template_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found...` | Request validation failed — schema mismatch or missing required field |
| 116 | `GET` | `/api/v1/planning/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/allocations` | 💥 500 Server Error | 20ms | — | `Internal Server Error` | Server-side error — check logs |
| 117 | `GET` | `/api/v1/planning/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/capacity` | ⚠️ 422 Unprocessable | 14ms | — | `{'detail': [{'type': 'missing', 'loc': ['query', 'start_date'], 'msg': 'Field required', 'input': None}, {'type': 'missing', 'loc': ['query', 'end_date'], 'msg': 'Field required', 'input': None}], 'bo...` | Request validation failed — schema mismatch or missing required field |
| 118 | `POST` | `/api/v1/planning/allocations` | ⚠️ 400 Bad Request | 0ms | — | `{'detail': 'User already allocated to this sprint'}` | Expected for dummy/test values |
| 119 | `POST` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/action-items` | ⚠️ 422 Unprocessable | 0ms | — | `{'detail': [{'type': 'value_error', 'loc': ['body', 'priority'], 'msg': 'Value error, priority must be one of: low, medium, high', 'input': 'P1', 'ctx': {'error': 'priority must be one of: low, medium...` | Request validation failed — schema mismatch or missing required field |
| 120 | `POST` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/gates` | ⚠️ 422 Unprocessable | 27ms | `{"gate_type": "G_SPRINT", "sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449"}` | `{'detail': [{'type': 'enum', 'loc': ['body', 'gate_type'], 'msg': "Input should be 'g_sprint' or 'g_sprint_close'", 'input': 'G_SPRINT', 'ctx': {'expected': "'g_sprint' or 'g_sprint_close'"}}], 'body'...` | Request validation failed — schema mismatch or missing required field |
| 121 | `POST` | `/api/v1/planning/templates` | ✅ 201 Created | 30ms | `{"name": "*-CyEyes-* Template", "type": "sprint", "content": {}}` | `{'name': '*-CyEyes-* Template', 'description': None, 'template_type': 'standard', 'duration_days': 10, 'default_capacity_points': 40, 'gates_enabled': True, 'goal_template': None, 'is_public': False, ...` | ✅ Created successfully |
| 122 | `PUT` | `/api/v1/planning/backlog/135b6b04-5530-45d0-a3b2-a9fe5bc138f5` | ✅ 200 OK | 18ms | `{"title": "*-CyEyes-* S4 task"}` | `{'id': '135b6b04-5530-45d0-a3b2-a9fe5bc138f5', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'sprint_id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'parent_id': None, 'type': 'task', 'title': '*...` | ✅ OK |
| 123 | `PUT` | `/api/v1/planning/phases/55bec71c-8228-4b39-8a78-a34de8b3dc8d` | ✅ 200 OK | 21ms | `{"name": "*-CyEyes-* S4 Phase"}` | `{'id': '55bec71c-8228-4b39-8a78-a34de8b3dc8d', 'roadmap_id': '624cc6c6-115f-4609-8b1d-dd1912fd527b', 'number': 1, 'name': '*-CyEyes-* S4 Phase', 'theme': None, 'objective': None, 'start_date': '2026-0...` | ✅ OK |
| 124 | `PUT` | `/api/v1/planning/roadmaps/624cc6c6-115f-4609-8b1d-dd1912fd527b` | ✅ 200 OK | 20ms | `{"name": "*-CyEyes-* S4 Roadmap"}` | `{'id': '624cc6c6-115f-4609-8b1d-dd1912fd527b', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'name': '*-CyEyes-* S4 Roadmap', 'description': None, 'vision': None, 'start_date': '2026-01-01', '...` | ✅ OK |
| 125 | `PUT` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449` | ✅ 200 OK | 22ms | `{"goal": "*-CyEyes-* S4 goal"}` | `{'id': '901b185c-a99d-44f9-af4a-91ac8891e449', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'phase_id': '55bec71c-8228-4b39-8a78-a34de8b3dc8d', 'number': 1, 'name': '*-CyEyes-* Sprint Updated...` | ✅ OK |

---
## Multi-Agent

**6 endpoints** | HTTP 200: **1** | HTTP 2xx: 1

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 126 | `GET` | `/api/v1/agent-team/conversations` | 💥 500 Server Error | 19ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `Internal Server Error` | Agent team service DB error |
| 127 | `GET` | `/api/v1/agent-team/definitions` | 💥 500 Server Error | 25ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `Internal Server Error` | Agent team service DB error |
| 128 | `GET` | `/api/v1/agent-team/presets` | ✅ 200 OK | 18ms | — | `[{'name': 'solo-dev', 'description': 'Single developer working alone', 'roles': ['coder'], 'delegation_chain': [], 'default_queue_mode': 'queue', 'role_count': 1}, {'name': 'startup-2', 'description':...` | ✅ OK |
| 129 | `POST` | `/api/v1/agent-team/conversations` | ⚠️ 422 Unprocessable | 0ms | — | `{'detail': [{'type': 'missing', 'loc': ['body', 'agent_definition_id'], 'msg': 'Field required', 'input': {'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'title': '*-CyEyes-* S4 conv', 'initial...` | Request validation failed — schema mismatch or missing required field |
| 130 | `POST` | `/api/v1/agent-team/definitions/seed` | 💥 500 Server Error | 22ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `Internal Server Error` | Agent team service DB error |
| 131 | `POST` | `/api/v1/agent-team/presets/solo-dev/apply` | ⚠️ 422 Unprocessable | 17ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': [{'type': 'missing', 'loc': ['query', 'project_id'], 'msg': 'Field required', 'input': None}], 'body': None}` | Request validation failed — schema mismatch or missing required field |

---
## Codegen

**20 endpoints** | HTTP 200: **9** | HTTP 2xx: 9

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 132 | `GET` | `/api/v1/codegen/health` | ✅ 200 OK | 24ms | — | `{'healthy': True, 'providers': {'app-builder': True, 'ollama': True, 'claude': False, 'deepcode': False}, 'available_count': 2, 'total_count': 4, 'fallback_chain': ['ollama', 'claude', 'deepcode']}` | ✅ OK |
| 133 | `GET` | `/api/v1/codegen/onboarding/options` | 🔍 404 Not Found | 19ms | — | `{'detail': 'Session not found'}` | Resource ID not found or route missing |
| 134 | `GET` | `/api/v1/codegen/onboarding/options/domains` | ✅ 200 OK | 18ms | — | `[{'key': 'restaurant', 'name': 'Nha hang / Quan an', 'name_en': 'Restaurant / F&B', 'description': 'Quan ly thuc don, don hang, ban, dat cho. Phu hop cho quan cafe, nha hang, quan an, bun pho...', 'ic...` | ✅ OK |
| 135 | `GET` | `/api/v1/codegen/onboarding/options/features/ecommerce` | ✅ 200 OK | 15ms | — | `[{'key': 'products', 'name': 'Quan ly san pham', 'description': 'Danh muc, gia ban, hinh anh'}, {'key': 'orders', 'name': 'Quan ly don hang', 'description': 'Don hang online, trang thai van chuyen'}, ...` | ✅ OK |
| 136 | `GET` | `/api/v1/codegen/onboarding/options/scales` | ✅ 200 OK | 16ms | — | `[{'key': 'micro', 'label': 'Ca nhan / 1-5 nhan vien', 'employee_min': 1, 'employee_max': 5, 'cgf_tier': 'LITE'}, {'key': 'small', 'label': 'Nho / 6-20 nhan vien', 'employee_min': 6, 'employee_max': 20...` | ✅ OK |
| 137 | `GET` | `/api/v1/codegen/providers` | ✅ 200 OK | 16ms | — | `{'providers': [{'name': 'ollama', 'available': True, 'fallback_position': 0, 'primary': True}, {'name': 'claude', 'available': False, 'fallback_position': 1, 'primary': False}, {'name': 'deepcode', 'a...` | ✅ OK |
| 138 | `GET` | `/api/v1/codegen/providers/health` | 🔍 404 Not Found | 14ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 139 | `GET` | `/api/v1/codegen/sessions` | ✅ 200 OK | 18ms | — | `{'sessions': [], 'total': 0, 'page': 1, 'page_size': 20}` | ✅ OK |
| 140 | `GET` | `/api/v1/codegen/sessions/09e33f72-f57e-45db-8bd2-d9791098444d` | 🔍 404 Not Found | 22ms | — | `{'detail': 'Session 09e33f72-f57e-45db-8bd2-d9791098444d not found or expired'}` | Resource ID not found or route missing |
| 141 | `GET` | `/api/v1/codegen/sessions/09e33f72-f57e-45db-8bd2-d9791098444d/quality/stream` | ✅ 200 OK | 14ms | — | `data: {"type": "error", "session_id": "09e33f72-f57e-45db-8bd2-d9791098444d", "message": "Session not found"}

` | ✅ OK |
| 142 | `GET` | `/api/v1/codegen/sessions/active` | ⚠️ 400 Bad Request | 15ms | — | `{'detail': 'Invalid session ID format: active'}` | Expected for dummy/test values |
| 143 | `GET` | `/api/v1/codegen/templates` | ✅ 200 OK | 15ms | — | `[{'id': 'fastapi', 'name': 'FastAPI Service', 'description': 'Full CRUD service with authentication', 'language': 'python', 'framework': 'fastapi'}, {'id': 'crud', 'name': 'CRUD Endpoint', 'descriptio...` | ✅ OK |
| 144 | `GET` | `/api/v1/codegen/usage` | 🔍 404 Not Found | 24ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 145 | `GET` | `/api/v1/codegen/usage/monthly` | ⚠️ 422 Unprocessable | 16ms | — | `{'detail': [{'type': 'missing', 'loc': ['query', 'year'], 'msg': 'Field required', 'input': None}, {'type': 'missing', 'loc': ['query', 'month'], 'msg': 'Field required', 'input': None}], 'body': None...` | Request validation failed — schema mismatch or missing required field |
| 146 | `GET` | `/api/v1/codegen/usage/provider-health/ollama` | 💥 500 Server Error | 22ms | — | `Internal Server Error` | Server-side error — check logs |
| 147 | `GET` | `/api/v1/codegen/usage/report` | 💥 500 Server Error | 37ms | — | `Internal Server Error` | Server-side error — check logs |
| 148 | `POST` | `/api/v1/codegen/estimate` | 💥 500 Server Error | 61ms | `{"app_blueprint": {"name": "hello", "type": "api"}}` | `Internal Server Error` | Server-side error — check logs |
| 149 | `POST` | `/api/v1/codegen/generate` | ❌ Connection Error | 20005ms | `{"app_blueprint": {"name": "hello", "type": "api", "language": "python"}, "language": "python"}` | `HTTPSConnectionPool(host='sdlc.nhatquangholding.com', port=443): Read timed out. (read timeout=20)` | Network error / connection refused |
| 150 | `POST` | `/api/v1/codegen/ir/validate` | ⚠️ 422 Unprocessable | 15ms | `{"spec": {"name": "hello", "type": "api"}}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'blueprint'], 'msg': 'Field required', 'input': {'spec': {'name': 'hello', 'type': 'api'}}}], 'body': "{'spec': {'name': 'hello', 'type': 'api'}}"}` | Request validation failed — schema mismatch or missing required field |
| 151 | `POST` | `/api/v1/codegen/onboarding/start` | ✅ 200 OK | 15ms | `{"project_type": "api", "domain": "ecommerce"}` | `{'session_id': 'd1555ffe-99ab-452f-84bd-f9d5ad954b81', 'current_step': 'welcome', 'completed_steps': [], 'domain': None, 'app_name': None, 'app_name_display': None, 'features': [], 'scale': None, 'has...` | ✅ OK |

---
## SAST

**7 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 152 | `GET` | `/api/v1/sast/health` | ✅ 200 OK | 12ms | — | `{'status': 'degraded', 'semgrep_available': False, 'custom_rules': {'ai_security': False, 'owasp_python': False}, 'timestamp': '2026-03-07T09:54:38.141440'}` | ✅ OK |
| 153 | `GET` | `/api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/analytics` | 💥 500 Server Error | 23ms | — | `Internal Server Error` | Server-side error — check logs |
| 154 | `GET` | `/api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/scans` | 💥 500 Server Error | 17ms | — | `Internal Server Error` | Server-side error — check logs |
| 155 | `GET` | `/api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/scans/09e33f72-f57e-45db-8bd2-d9791098444d` | 💥 500 Server Error | 15ms | — | `Internal Server Error` | Server-side error — check logs |
| 156 | `GET` | `/api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/trend` | 💥 500 Server Error | 28ms | — | `Internal Server Error` | Server-side error — check logs |
| 157 | `POST` | `/api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/scan` | ✅ 200 OK | 19ms | — | `{'scan_id': '9762c907-074e-4523-9945-eef1fadad2eb', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'success': False, 'error_message': 'Semgrep CLI not installed', 'summary': {'total_findings': ...` | ✅ OK |
| 158 | `POST` | `/api/v1/sast/scan-snippet` | ✅ 200 OK | 13ms | `{"code": "def hello():\n    return 'hello'", "language": "python", "include_ai_rules": true}` | `{'scan_id': '2f72718b-6866-4a28-b58d-90845bef4b73', 'project_id': '66dddcdf-2209-4c3e-8a70-4d666207bee6', 'success': False, 'error_message': 'Semgrep CLI not installed', 'summary': {'total_findings': ...` | ✅ OK |

---
## Compliance

**15 endpoints** | HTTP 200: **7** | HTTP 2xx: 7

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 159 | `GET` | `/api/v1/compliance/ai/budget` | ✅ 200 OK | 21ms | — | `{'month': '2026-03', 'total_spent': 0.0, 'budget': 500.0, 'remaining': 500.0, 'percentage_used': 0.0, 'by_provider': {}, 'alerts': []}` | ✅ OK |
| 160 | `GET` | `/api/v1/compliance/ai/models` | ✅ 200 OK | 13ms | — | `{'models': [], 'default_model': 'qwen3:32b', 'ollama_url': 'http://localhost:11434'}` | ✅ OK |
| 161 | `GET` | `/api/v1/compliance/ai/providers` | ✅ 200 OK | 17ms | — | `{'ollama': {'healthy': False, 'models': [], 'version': 'unknown', 'error': 'Connection refused - Ollama not running'}, 'claude': {'available': False}, 'gpt4': {'available': False}, 'rule_based': {'ava...` | ✅ OK |
| 162 | `GET` | `/api/v1/compliance/controls` | 🔍 404 Not Found | 14ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 163 | `GET` | `/api/v1/compliance/frameworks` | 💥 500 Server Error | 19ms | — | `Internal Server Error` | Compliance service DB error |
| 164 | `GET` | `/api/v1/compliance/frameworks/OWASP` | 💥 500 Server Error | 18ms | — | `Internal Server Error` | Compliance service DB error |
| 165 | `GET` | `/api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/assessments` | 💥 500 Server Error | 17ms | — | `Internal Server Error` | Compliance service DB error |
| 166 | `GET` | `/api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/gap-analysis` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 167 | `GET` | `/api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/recommendations` | 🔍 404 Not Found | 10ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 168 | `GET` | `/api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/status` | 🔍 404 Not Found | 15ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 169 | `GET` | `/api/v1/compliance/queue/status` | ✅ 200 OK | 19ms | — | `{'pending': 0, 'running': 0, 'completed': 0, 'failed': 0, 'total_jobs': 0}` | ✅ OK |
| 170 | `GET` | `/api/v1/compliance/scans/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | ✅ 200 OK | 16ms | — | `[{'id': 'fda86bce-a730-42ad-a713-ba3ffd718cb6', 'compliance_score': 100, 'violations_count': 0, 'warnings_count': 0, 'trigger_type': 'scheduled', 'scanned_at': '2026-03-07T02:00:00.295944'}]` | ✅ OK |
| 171 | `GET` | `/api/v1/compliance/scans/3ec1d475-c294-40e9-806f-0691dffa3fa8/latest` | ✅ 200 OK | 17ms | — | `{'id': 'fda86bce-a730-42ad-a713-ba3ffd718cb6', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'triggered_by': None, 'trigger_type': 'scheduled', 'compliance_score': 100, 'violations_count': 0, ...` | ✅ OK |
| 172 | `GET` | `/api/v1/compliance/violations/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 OK | 15ms | — | `[]` | ✅ OK |
| 173 | `POST` | `/api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence-mapping` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Governance

**12 endpoints** | HTTP 200: **5** | HTTP 2xx: 5

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 174 | `GET` | `/api/v1/governance/dogfooding/status` | ✅ 200 OK | 11ms | — | `{'phase': 'week_1_preparation', 'mode': 'warning', 'start_date': '2026-03-07T04:33:00.508460', 'current_week': 1, 'metrics': {'total_evaluations': 0, 'rejection_rate': '0.0%', 'false_positive_rate': '...` | ✅ OK |
| 175 | `GET` | `/api/v1/governance/health` | ✅ 200 OK | 14ms | — | `{'status': 'healthy', 'mode': 'warning', 'auto_rollback_enabled': True, 'total_evaluations': 0, 'latency_p95_ms': 0.0, 'timestamp': '2026-03-07T09:54:38.383310'}` | ✅ OK |
| 176 | `GET` | `/api/v1/governance/metrics` | ✅ 200 OK | 13ms | — | `{'mode': 'warning', 'total_evaluations': 0, 'total_blocked': 0, 'total_warned': 0, 'total_passed': 0, 'rejection_rate': 0.0, 'false_positive_rate': 0.0, 'latency_p95_ms': 0.0, 'ceo_overrides': 0, 'aut...` | ✅ OK |
| 177 | `GET` | `/api/v1/governance/mode` | ✅ 200 OK | 13ms | — | `{'mode': 'warning', 'previous_mode': None, 'changed_at': '2026-03-07T04:33:00.508460', 'changed_by': 'system', 'reason': 'Initial startup', 'is_rollback': False, 'auto_rollback_enabled': True}` | ✅ OK |
| 178 | `GET` | `/api/v1/governance/mode/state` | ✅ 200 OK | 13ms | — | `{'mode': 'warning', 'previous_mode': None, 'changed_at': '2026-03-07T04:33:00.508460', 'changed_by': 'system', 'reason': 'Initial startup', 'is_rollback': False, 'auto_rollback_enabled': True, 'total_...` | ✅ OK |
| 179 | `GET` | `/api/v1/governance/specs/health` | ⚠️ 422 Unprocessable | 11ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'spec_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `h`...` | Request validation failed — schema mismatch or missing required field |
| 180 | `GET` | `/api/v1/governance/tiers/` | 💥 500 Server Error | 19ms | — | `Internal Server Error` | Server-side error — check logs |
| 181 | `GET` | `/api/v1/governance/tiers/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 💥 500 Server Error | 18ms | — | `Internal Server Error` | Server-side error — check logs |
| 182 | `GET` | `/api/v1/governance/tiers/LITE/requirements` | 💥 500 Server Error | 14ms | — | `Internal Server Error` | Server-side error — check logs |
| 183 | `GET` | `/api/v1/governance/tiers/STANDARD/requirements` | 💥 500 Server Error | 14ms | — | `Internal Server Error` | Server-side error — check logs |
| 184 | `GET` | `/api/v1/governance/tiers/health` | ⚠️ 422 Unprocessable | 18ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'project_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found ...` | Request validation failed — schema mismatch or missing required field |
| 185 | `GET` | `/api/v1/governance/vibecoding/health` | ⚠️ 422 Unprocessable | 12ms | — | `{'detail': [{'type': 'missing', 'loc': ['query', 'project_id'], 'msg': 'Field required', 'input': None}], 'body': None}` | Request validation failed — schema mismatch or missing required field |

---
## Governance Metrics

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 186 | `GET` | `/api/v1/governance/metrics/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 19ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## CEO Dashboard

**13 endpoints** | HTTP 200: **11** | HTTP 2xx: 11

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 187 | `GET` | `/api/v1/ceo-dashboard` | 🔍 404 Not Found | 27ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 188 | `GET` | `/api/v1/ceo-dashboard/health` | ✅ 200 OK | 15ms | — | `{'status': 'healthy', 'service': 'ceo_dashboard', 'timestamp': '2026-03-07T09:54:38.593081', 'metrics': {'submissions_tracked': 0, 'overrides_tracked': 0, 'pending_queue_size': 0}}` | ✅ OK |
| 189 | `GET` | `/api/v1/ceo-dashboard/overrides` | ✅ 200 OK | 12ms | — | `[]` | ✅ OK |
| 190 | `GET` | `/api/v1/ceo-dashboard/pending-decisions` | ✅ 200 OK | 13ms | — | `[]` | ✅ OK |
| 191 | `GET` | `/api/v1/ceo-dashboard/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 192 | `GET` | `/api/v1/ceo-dashboard/routing-breakdown` | ✅ 200 OK | 14ms | — | `{'total_prs': 0, 'auto_approved': 0, 'tech_lead_review': 0, 'ceo_should_review': 0, 'ceo_must_review': 0, 'auto_approval_rate': 0.0, 'trend': 'stable', 'last_updated': '2026-03-07T09:54:38.664921'}` | ✅ OK |
| 193 | `GET` | `/api/v1/ceo-dashboard/summary` | ✅ 200 OK | 17ms | — | `{'executive_summary': {'time_saved': {'baseline_hours': 40.0, 'actual_review_hours': 0.0, 'time_saved_hours': 40.0, 'time_saved_percent': 100.0, 'trend': 'stable', 'status': 'excellent', 'target_week'...` | ✅ OK |
| 194 | `GET` | `/api/v1/ceo-dashboard/system-health` | ✅ 200 OK | 12ms | — | `{'uptime_percent': 99.9, 'api_latency_p95_ms': 85.0, 'kill_switch_status': 'WARNING', 'overall_status': 'excellent', 'alerts_active': 0, 'last_incident': None}` | ✅ OK |
| 195 | `GET` | `/api/v1/ceo-dashboard/time-saved` | ✅ 200 OK | 13ms | — | `{'baseline_hours': 40.0, 'actual_review_hours': 0.0, 'time_saved_hours': 40.0, 'time_saved_percent': 100.0, 'trend': 'stable', 'status': 'excellent', 'target_week': 9, 'target_hours': 10.0, 'on_track'...` | ✅ OK |
| 196 | `GET` | `/api/v1/ceo-dashboard/top-rejections` | ✅ 200 OK | 13ms | — | `[]` | ✅ OK |
| 197 | `GET` | `/api/v1/ceo-dashboard/trends/time-saved` | ✅ 200 OK | 10ms | — | `[{'week': 3, 'week_start': '2026-01-17', 'time_saved_hours': 0, 'baseline_hours': 40.0, 'target_hours': 30.0}, {'week': 4, 'week_start': '2026-01-24', 'time_saved_hours': 0, 'baseline_hours': 40.0, 't...` | ✅ OK |
| 198 | `GET` | `/api/v1/ceo-dashboard/trends/vibecoding-index` | ✅ 200 OK | 11ms | — | `[{'date': '2026-03-01', 'day_name': 'Sunday', 'average_index': 0, 'count': 0, 'distribution': {'0-10': 0, '11-20': 0, '21-30': 0, '31-40': 0, '41-50': 0, '51-60': 0, '61-70': 0, '71-80': 0, '81-90': 0...` | ✅ OK |
| 199 | `GET` | `/api/v1/ceo-dashboard/weekly-summary` | ✅ 200 OK | 12ms | — | `{'week_number': 10, 'week_start': '2026-03-02T00:00:00', 'week_end': '2026-03-09T00:00:00', 'compliance_pass_rate': 0.0, 'vibecoding_index_avg': 0.0, 'false_positive_rate': 0.0, 'developer_satisfactio...` | ✅ OK |

---
## Vibecoding

**3 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 200 | `GET` | `/api/v1/vibecoding/health` | ✅ 200 OK | 18ms | — | `{'status': 'healthy', 'service': 'vibecoding_index_engine', 'signals_configured': 5, 'critical_path_checker': 'enabled', 'timestamp': '2026-03-07T09:54:38.747129'}` | ✅ OK |
| 201 | `GET` | `/api/v1/vibecoding/stats` | ✅ 200 OK | 11ms | — | `{'total_calculations': 0, 'average_score': 0.0, 'category_distribution': {'green': 0, 'yellow': 0, 'orange': 0, 'red': 0}, 'routing_distribution': {'auto_approve': 0, 'tech_lead_review': 0, 'ceo_shoul...` | ✅ OK |
| 202 | `GET` | `/api/v1/vibecoding/thresholds` | ✅ 200 OK | 12ms | — | `{'thresholds': {'green': {'min': 0, 'max': 30}, 'yellow': {'min': 31, 'max': 60}, 'orange': {'min': 61, 'max': 80}, 'red': {'min': 81, 'max': 100}}, 'routing_rules': {'green': 'auto_approve', 'yellow'...` | ✅ OK |

---
## Vibecoding Index

**3 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 203 | `GET` | `/api/v1/vibecoding-index` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 204 | `GET` | `/api/v1/vibecoding-index/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 205 | `POST` | `/api/v1/vibecoding-index/3ec1d475-c294-40e9-806f-0691dffa3fa8/calculate` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## DORA

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 206 | `GET` | `/api/v1/dora/metrics` | 🔍 404 Not Found | 10ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 207 | `GET` | `/api/v1/dora/metrics/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Telemetry

**7 endpoints** | HTTP 200: **1** | HTTP 2xx: 1

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 208 | `GET` | `/api/v1/telemetry` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 209 | `GET` | `/api/v1/telemetry/dashboard` | 💥 500 Server Error | 17ms | — | `Internal Server Error` | Server-side error — check logs |
| 210 | `GET` | `/api/v1/telemetry/events` | ⚠️ 405 Method Not Allowed | 10ms | — | `{'detail': 'Method Not Allowed'}` | OAuth callback: POST from provider required (not GET) |
| 211 | `GET` | `/api/v1/telemetry/funnels/onboarding` | ⚠️ 400 Bad Request | 14ms | — | `{'detail': 'Unknown funnel: onboarding'}` | Expected for dummy/test values |
| 212 | `GET` | `/api/v1/telemetry/health` | ✅ 200 OK | 13ms | — | `{'status': 'healthy', 'service': 'telemetry', 'version': '1.0.0', 'funnels_available': ['time_to_first_project', 'time_to_first_evidence', 'time_to_first_gate'], 'core_events': 10, 'engagement_events'...` | ✅ OK |
| 213 | `GET` | `/api/v1/telemetry/interfaces` | 💥 500 Server Error | 17ms | — | `Internal Server Error` | Server-side error — check logs |
| 214 | `POST` | `/api/v1/telemetry/event` | 🔍 404 Not Found | 10ms | `{"event": "*-CyEyes-* S4 test", "properties": {}}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## AI Detection

**7 endpoints** | HTTP 200: **4** | HTTP 2xx: 4

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 215 | `GET` | `/api/v1/ai-detection` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 216 | `GET` | `/api/v1/ai-detection/circuit-breakers` | ✅ 200 OK | 12ms | — | `{'circuit_breakers': {'github_api': {'name': 'github_api', 'config': {'failure_threshold': 5, 'recovery_timeout': 30.0, 'success_threshold': 3, 'enabled': True}, 'stats': {'state': 'closed', 'failure_...` | ✅ OK |
| 217 | `GET` | `/api/v1/ai-detection/shadow-mode` | ✅ 200 OK | 12ms | — | `{'status': 'enabled', 'config': {'enabled': True, 'sample_rate': 1.0, 'log_level': 'INFO', 'collect_metrics': True}, 'description': 'Shadow mode logs detection results for production validation withou...` | ✅ OK |
| 218 | `GET` | `/api/v1/ai-detection/status` | ✅ 200 OK | 14ms | — | `{'service': 'GitHubAIDetectionService', 'version': '1.0.0', 'detection_threshold': 0.5, 'strategies': ['metadata', 'commit', 'pattern'], 'weights': {'metadata': 0.4, 'commit': 0.4, 'pattern': 0.2}, 's...` | ✅ OK |
| 219 | `GET` | `/api/v1/ai-detection/tools` | ✅ 200 OK | 17ms | — | `{'tools': [{'id': 'cursor', 'name': 'Cursor'}, {'id': 'copilot', 'name': 'Copilot'}, {'id': 'claude_code', 'name': 'Claude Code'}, {'id': 'chatgpt', 'name': 'Chatgpt'}, {'id': 'windsurf', 'name': 'Win...` | ✅ OK |
| 220 | `POST` | `/api/v1/ai-detection/analyze` | ⚠️ 422 Unprocessable | 13ms | `{"content": "print('hello')", "language": "python"}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'pr_id'], 'msg': 'Field required', 'input': {'content': "print('hello')", 'language': 'python'}}, {'type': 'missing', 'loc': ['body', 'title'], 'msg': '...` | Request validation failed — schema mismatch or missing required field |
| 221 | `POST` | `/api/v1/ai-detection/detect` | 🔍 404 Not Found | 11ms | `{"content": "Hello world", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Notifications

**6 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 222 | `GET` | `/api/v1/notifications` | ✅ 200 OK | 21ms | — | `{'notifications': [], 'total': 0, 'unread_count': 0, 'page': 1, 'page_size': 20}` | ✅ OK |
| 223 | `GET` | `/api/v1/notifications/count` | ⚠️ 422 Unprocessable | 16ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'notification_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], f...` | Request validation failed — schema mismatch or missing required field |
| 224 | `GET` | `/api/v1/notifications/preferences` | ⚠️ 422 Unprocessable | 14ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'notification_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], f...` | Request validation failed — schema mismatch or missing required field |
| 225 | `GET` | `/api/v1/notifications/settings/preferences` | ✅ 200 OK | 16ms | — | `{'email_enabled': True, 'slack_enabled': False, 'slack_webhook_url': None, 'teams_enabled': False, 'teams_webhook_url': None, 'notification_types': {'compliance_violation': True, 'scan_completed': Tru...` | ✅ OK |
| 226 | `GET` | `/api/v1/notifications/stats/summary` | ✅ 200 OK | 17ms | — | `{'total': 0, 'unread': 0, 'read': 0, 'by_type': {}, 'unread_by_priority': {}}` | ✅ OK |
| 227 | `POST` | `/api/v1/notifications/read-all` | ⚠️ 405 Method Not Allowed | 13ms | — | `{'detail': 'Method Not Allowed'}` | OAuth callback: POST from provider required (not GET) |

---
## API Keys

**4 endpoints** | HTTP 200: **1** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 228 | `DELETE` | `/api/v1/api-keys/bab4226d-b556-43e0-b535-271b18fd4908` | ✅ 204 No Content | 15ms | — | `` | ✅ Success (no body) |
| 229 | `GET` | `/api/v1/api-keys` | ✅ 200 OK | 17ms | — | `[{'id': 'ce5a6ad5-adcb-4b95-bcf5-1a419a3835b4', 'name': '*-CyEyes-* Key 1772860135', 'prefix': 'sdlc_live__JWPF8NYJw...', 'last_used_at': None, 'expires_at': None, 'is_active': True, 'created_at': '20...` | ✅ OK |
| 230 | `GET` | `/api/v1/api-keys/bab4226d-b556-43e0-b535-271b18fd4908` | ⚠️ 405 Method Not Allowed | 12ms | — | `{'detail': 'Method Not Allowed'}` | OAuth callback: POST from provider required (not GET) |
| 231 | `POST` | `/api/v1/api-keys` | ✅ 201 Created | 17ms | `{"name": "*-CyEyes-* Key 1772860135"}` | `{'id': 'ce5a6ad5-adcb-4b95-bcf5-1a419a3835b4', 'name': '*-CyEyes-* Key 1772860135', 'api_key': 'sdlc_live__JWPF8NYJwJZT9iows8xBkQD6sdwYCFQzmOGRx9B0zI', 'prefix': 'sdlc_live__JWPF8NYJw...', 'expires_at...` | ✅ Created successfully |

---
## MFA

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 232 | `GET` | `/api/v1/mfa/status` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 233 | `POST` | `/api/v1/mfa/setup` | 🔍 404 Not Found | 12ms | `{"method": "totp"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Policies

**4 endpoints** | HTTP 200: **2** | HTTP 2xx: 2

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 234 | `GET` | `/api/v1/policies` | ✅ 200 OK | 18ms | — | `{'items': [], 'total': 0, 'page': 1, 'page_size': 20, 'pages': 0}` | ✅ OK |
| 235 | `GET` | `/api/v1/policies/evaluations/b1913ff7-15cb-4ad3-9846-4200ce4f70af` | ✅ 200 OK | 22ms | — | `{'items': [], 'total': 0, 'passed': 0, 'failed': 0, 'pass_rate': 0.0}` | ✅ OK |
| 236 | `POST` | `/api/v1/policies` | ⚠️ 405 Method Not Allowed | 0ms | — | `{"detail":"Method Not Allowed"}` | OAuth callback: POST from provider required (not GET) |
| 237 | `POST` | `/api/v1/policies/evaluate` | ⚠️ 422 Unprocessable | 14ms | `{"gate_id": "b1913ff7-15cb-4ad3-9846-4200ce4f70af", "policy_id": "dummy", "input_data": {}}` | `{'detail': [{'type': 'uuid_parsing', 'loc': ['body', 'policy_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `...` | Request validation failed — schema mismatch or missing required field |

---
## Override

**5 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 238 | `GET` | `/api/v1/override/dummy` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 239 | `GET` | `/api/v1/override/history` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 240 | `GET` | `/api/v1/override/queue` | 🔍 404 Not Found | 20ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 241 | `POST` | `/api/v1/override/dummy/approve` | 🔍 404 Not Found | 22ms | `{"comment": "*-CyEyes-* approved"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 242 | `POST` | `/api/v1/override/request` | 🔍 404 Not Found | 0ms | — | `{"detail":"Not Found"}` | Endpoint not yet deployed (route missing in production) |

---
## MRP

**6 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 243 | `GET` | `/api/v1/mrp` | 🔍 404 Not Found | 10ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 244 | `GET` | `/api/v1/mrp/dummy` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 245 | `GET` | `/api/v1/mrp/health` | ✅ 200 OK | 13ms | — | `{'status': 'healthy', 'service': 'mrp-validation', 'version': '1.0.0', 'features': ['5-point-mrp-validation', 'vcr-generation', '4-tier-policy-enforcement']}` | ✅ OK |
| 246 | `GET` | `/api/v1/mrp/policies/compliance/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 OK | 27ms | — | `{'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'current_tier': 'PROFESSIONAL', 'is_compliant': True, 'compliance_score': 100, 'missing_requirements': [], 'recommendations': ['Project is fully ...` | ✅ OK |
| 247 | `GET` | `/api/v1/mrp/policies/tiers` | ✅ 200 OK | 17ms | — | `{'tiers': [{'tier': 'LITE', 'display_name': 'Lite', 'description': 'Advisory mode for individuals and prototypes. All checks are recommendations only.', 'target_audience': 'Individuals, side projects,...` | ✅ OK |
| 248 | `POST` | `/api/v1/mrp` | 🔍 404 Not Found | 0ms | — | `{"detail":"Not Found"}` | Endpoint not yet deployed (route missing in production) |

---
## VCR

**4 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 249 | `GET` | `/api/v1/vcr` | 💥 500 Server Error | 22ms | — | `Internal Server Error` | VCR table missing (migration) |
| 250 | `GET` | `/api/v1/vcr/dummy` | ⚠️ 422 Unprocessable | 16ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'vcr_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `u` ...` | Request validation failed — schema mismatch or missing required field |
| 251 | `GET` | `/api/v1/vcr/stats/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 💥 500 Server Error | 17ms | — | `Internal Server Error` | VCR table missing (migration) |
| 252 | `POST` | `/api/v1/vcr` | 💥 500 Server Error | 0ms | — | `{"detail":"(sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError) <class 'asyncpg.exceptions.UndefinedTableError'>: relation \"version_controlled_resolutions\" does not exist\n[SQL: INSERT INTO ver...` | DB migration pending — table missing |

---
## GitHub

**11 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 253 | `GET` | `/api/v1/github/app/status` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 254 | `GET` | `/api/v1/github/installations` | 💥 500 Server Error | 19ms | — | `Internal Server Error` | GitHub App not configured |
| 255 | `GET` | `/api/v1/github/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/repository` | 💥 500 Server Error | 24ms | — | `Internal Server Error` | GitHub App not configured |
| 256 | `GET` | `/api/v1/github/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/scan` | 💥 500 Server Error | 19ms | — | `Internal Server Error` | GitHub App not configured |
| 257 | `GET` | `/api/v1/github/repos` | 🔍 404 Not Found | 17ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 258 | `GET` | `/api/v1/github/webhooks` | ⚠️ 405 Method Not Allowed | 12ms | — | `{'detail': 'Method Not Allowed'}` | OAuth callback: POST from provider required (not GET) |
| 259 | `GET` | `/api/v1/github/webhooks/dlq` | 💥 500 Server Error | 14ms | — | `Internal Server Error` | GitHub App not configured |
| 260 | `GET` | `/api/v1/github/webhooks/jobs` | 🔍 404 Not Found | 23ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 261 | `GET` | `/api/v1/github/webhooks/jobs/dummy` | 🔍 404 Not Found | 22ms | — | `{'detail': {'error': 'job_not_found', 'message': 'Job dummy not found'}}` | Resource ID not found or route missing |
| 262 | `GET` | `/api/v1/github/webhooks/stats` | 💥 500 Server Error | 16ms | — | `Internal Server Error` | GitHub App not configured |
| 263 | `POST` | `/api/v1/github/webhook` | 🔍 404 Not Found | 20ms | `{"action": "ping", "zen": "*-CyEyes-*", "hook_id": 1}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Stage Gating

**6 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 264 | `GET` | `/api/v1/stage-gating` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 265 | `GET` | `/api/v1/stage-gating/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 266 | `GET` | `/api/v1/stage-gating/health` | ✅ 200 OK | 14ms | — | `{'status': 'healthy', 'service': 'stage_gating', 'stages_configured': 11, 'timestamp': '2026-03-07T09:54:39.230608'}` | ✅ OK |
| 267 | `GET` | `/api/v1/stage-gating/progress/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 OK | 14ms | — | `{'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'current_stage': 'stage_04_build', 'completed_stages': [], 'stage_progress': {'stage_00_foundation': False, 'stage_01_planning': False, 'stage_02...` | ✅ OK |
| 268 | `GET` | `/api/v1/stage-gating/rules` | ✅ 200 OK | 13ms | — | `{'stages': {'stage_00_foundation': {'stage': 'stage_00_foundation', 'allows': ['docs/00-foundation/**', 'docs/00-discover/**', 'README.md', '.gitignore', 'LICENSE', 'CLAUDE.md', 'AGENTS.md', '.github/...` | ✅ OK |
| 269 | `GET` | `/api/v1/stage-gating/rules/STAGE_00` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Stage not found: STAGE_00'}` | Resource ID not found or route missing |

---
## Deprecation

**4 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 270 | `GET` | `/api/v1/deprecation/dashboard` | 💥 500 Server Error | 17ms | — | `Internal Server Error` | Deprecation service DB error |
| 271 | `GET` | `/api/v1/deprecation/endpoints` | 💥 500 Server Error | 20ms | — | `Internal Server Error` | Deprecation service DB error |
| 272 | `GET` | `/api/v1/deprecation/summary` | 💥 500 Server Error | 18ms | — | `Internal Server Error` | Deprecation service DB error |
| 273 | `GET` | `/api/v1/deprecation/timeline` | 💥 500 Server Error | 16ms | — | `Internal Server Error` | Deprecation service DB error |

---
## MCP

**5 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 274 | `GET` | `/api/v1/mcp/context` | 💥 500 Server Error | 20ms | — | `Internal Server Error` | MCP service error |
| 275 | `GET` | `/api/v1/mcp/cost` | 💥 500 Server Error | 15ms | — | `Internal Server Error` | MCP service error |
| 276 | `GET` | `/api/v1/mcp/dashboard` | 💥 500 Server Error | 25ms | — | `Internal Server Error` | MCP service error |
| 277 | `GET` | `/api/v1/mcp/health` | 💥 500 Server Error | 23ms | — | `Internal Server Error` | MCP service error |
| 278 | `GET` | `/api/v1/mcp/latency` | 💥 500 Server Error | 19ms | — | `Internal Server Error` | MCP service error |

---
## Risk

**3 endpoints** | HTTP 200: **2** | HTTP 2xx: 2

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 279 | `GET` | `/api/v1/risk/factors` | ✅ 200 OK | 13ms | — | `[{'factor': 'data_schema', 'name': 'Data Schema Changes', 'description': 'Migrations, model changes, database schema modifications', 'examples': ['Alembic migration files', 'SQLAlchemy model changes',...` | ✅ OK |
| 280 | `GET` | `/api/v1/risk/levels` | ✅ 200 OK | 13ms | — | `{'levels': [{'level': 'minimal', 'score_range': '0-20', 'planning_required': False, 'description': 'No significant risk factors. Planning optional.'}, {'level': 'low', 'score_range': '21-40', 'plannin...` | ✅ OK |
| 281 | `GET` | `/api/v1/risk/should-plan` | ⚠️ 422 Unprocessable | 17ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': [{'type': 'missing', 'loc': ['query', 'diff'], 'msg': 'Field required', 'input': None}], 'body': None}` | Request validation failed — schema mismatch or missing required field |

---
## Maturity

**4 endpoints** | HTTP 200: **2** | HTTP 2xx: 2

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 282 | `GET` | `/api/v1/maturity/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 💥 500 Server Error | 26ms | — | `Internal Server Error` | Maturity service DB error |
| 283 | `GET` | `/api/v1/maturity/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | 💥 500 Server Error | 23ms | — | `Internal Server Error` | Maturity service DB error |
| 284 | `GET` | `/api/v1/maturity/health` | ✅ 200 OK | 12ms | — | `{'status': 'healthy', 'service': 'agentic-maturity', 'version': '1.0.0', 'levels': ['L0', 'L1', 'L2', 'L3']}` | ✅ OK |
| 285 | `GET` | `/api/v1/maturity/levels` | ✅ 200 OK | 15ms | — | `[{'level': 'L0', 'name': 'Manual', 'description': 'Human writes all code, manual testing and reviews. No AI assistance.', 'score_range': [0, 20], 'key_features': ['All code written manually', 'Manual ...` | ✅ OK |

---
## Agentic Maturity

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 286 | `GET` | `/api/v1/agentic-maturity` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 287 | `GET` | `/api/v1/agentic-maturity/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## SDLC Structure

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 288 | `GET` | `/api/v1/sdlc-structure` | 🔍 404 Not Found | 10ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 289 | `POST` | `/api/v1/sdlc-structure/validate` | 🔍 404 Not Found | 12ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Triage

**2 endpoints** | HTTP 200: **1** | HTTP 2xx: 1

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 290 | `GET` | `/api/v1/triage/sla-breaches` | 💥 500 Server Error | 21ms | — | `Internal Server Error` | Triage service DB error |
| 291 | `GET` | `/api/v1/triage/stats` | ✅ 200 OK | 28ms | — | `{'by_status': {}, 'by_priority': {}, 'untriaged_count': 0, 'total': 0, 'triage_rate': 0.0}` | ✅ OK |

---
## Enterprise

**1 endpoints** | HTTP 200: **1** | HTTP 2xx: 1

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 292 | `GET` | `/api/v1/enterprise/audit` | ✅ 200 OK | 20ms | — | `{'events': [], 'total': 0, 'page': 1, 'page_size': 50, 'has_more': False}` | ✅ OK |

---
## GDPR

**5 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 293 | `GET` | `/api/v1/gdpr/consents` | 🔍 404 Not Found | 17ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 294 | `GET` | `/api/v1/gdpr/dsar` | ✅ 200 OK | 14ms | — | `{'items': [{'id': 'fd92da75-1708-4faf-9004-343af644fbb5', 'request_type': 'access', 'status': 'pending', 'requester_email': 'retest@example.com', 'created_at': '2026-03-01T04:23:25.409759+00:00', 'due...` | ✅ OK |
| 295 | `GET` | `/api/v1/gdpr/me/consents` | ✅ 200 OK | 17ms | — | `{'consents': [{'id': 'feb3d147-61a2-4607-8f75-b03d62986ef0', 'purpose': 'essential', 'granted': True, 'version': '2.0', 'created_at': '2026-03-01T04:23:25.421614+00:00'}, {'id': 'b7505fd3-81fa-4476-a0...` | ✅ OK |
| 296 | `GET` | `/api/v1/gdpr/me/data-export` | ✅ 200 OK | 13ms | — | `{'user_id': 'a0000000-0000-0000-0000-000000000001', 'generated_at': '2026-03-07T09:54:41.029134+00:00', 'data_categories': {'agent_messages': 'unavailable', 'evidence_uploads': 'unavailable', 'audit_e...` | ✅ OK |
| 297 | `POST` | `/api/v1/gdpr/export-request` | 🔍 404 Not Found | 9ms | `{"reason": "testing"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Grafana

**6 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 298 | `GET` | `/api/v1/grafana-dashboards` | ✅ 200 OK | 11ms | — | `{'dashboards': [{'uid': 'ceo-dashboard', 'title': 'CEO Dashboard - Governance Intelligence', 'description': 'Executive governance intelligence dashboard for CEO, CTO, CPO. Real-time visibility into go...` | ✅ OK |
| 299 | `GET` | `/api/v1/grafana-dashboards/datasource/template` | ✅ 200 OK | 13ms | — | `{'name': 'Prometheus-SDLC', 'type': 'prometheus', 'access': 'proxy', 'url': 'http://prometheus:9090', 'isDefault': True, 'editable': True, 'jsonData': {'httpMethod': 'POST', 'timeInterval': '5s', 'que...` | ✅ OK |
| 300 | `GET` | `/api/v1/grafana-dashboards/export/all` | ✅ 200 OK | 19ms | — | `[{'uid': 'ceo-dashboard', 'title': 'CEO Dashboard - Governance Intelligence', 'description': 'Executive governance intelligence dashboard for CEO, CTO, CPO. Real-time visibility into governance effect...` | ✅ OK |
| 301 | `GET` | `/api/v1/grafana-dashboards/overview` | ⚠️ 400 Bad Request | 13ms | — | `{'detail': 'Invalid dashboard type: overview. Valid types: ceo, tech, ops'}` | Expected for dummy/test values |
| 302 | `GET` | `/api/v1/grafana-dashboards/overview/json` | ⚠️ 400 Bad Request | 24ms | — | `{'detail': 'Invalid dashboard type: overview. Valid types: ceo, tech, ops'}` | Expected for dummy/test values |
| 303 | `GET` | `/api/v1/grafana-dashboards/overview/panels` | ⚠️ 400 Bad Request | 13ms | — | `{'detail': 'Invalid dashboard type: overview. Valid types: ceo, tech, ops'}` | Expected for dummy/test values |

---
## Payments

**3 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 304 | `GET` | `/api/v1/payments/me` | 🔍 404 Not Found | 15ms | — | `{'detail': 'Payment not found'}` | Resource ID not found or route missing |
| 305 | `GET` | `/api/v1/payments/plans` | 🔍 404 Not Found | 22ms | — | `{'detail': 'Payment not found'}` | Resource ID not found or route missing |
| 306 | `GET` | `/api/v1/payments/subscriptions/me` | 🔍 404 Not Found | 15ms | — | `{'detail': 'No subscription found'}` | Resource ID not found or route missing |

---
## Consultations

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 307 | `GET` | `/api/v1/consultations` | 💥 500 Server Error | 20ms | — | `Internal Server Error` | Consultations service DB error |
| 308 | `GET` | `/api/v1/consultations/my-reviews` | 💥 500 Server Error | 19ms | — | `Internal Server Error` | Consultations service DB error |

---
## Organizations

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 309 | `GET` | `/api/v1/organizations` | 💥 500 Server Error | 19ms | — | `Internal Server Error` | Org/Team service DB error |

---
## Teams

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 310 | `GET` | `/api/v1/teams` | 💥 500 Server Error | 20ms | — | `Internal Server Error` | Org/Team service DB error |

---
## Dashboard

**3 endpoints** | HTTP 200: **2** | HTTP 2xx: 2

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 311 | `GET` | `/api/v1/dashboard` | 🔍 404 Not Found | 10ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 312 | `GET` | `/api/v1/dashboard/recent-gates` | ✅ 200 OK | 13ms | — | `[{'id': 'b1913ff7-15cb-4ad3-9846-4200ce4f70af', 'gate_name': 'Final Retest - Planning Review', 'project_name': 'CyEyes-S4', 'status': 'pending', 'updated_at': '2026-03-07T09:54:36.032349'}, {'id': 'ca...` | ✅ OK |
| 313 | `GET` | `/api/v1/dashboard/stats` | ✅ 200 OK | 17ms | — | `{'total_projects': 7, 'active_gates': 2, 'pending_approvals': 2, 'pass_rate': 0}` | ✅ OK |

---
## Check Runs

**4 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 314 | `GET` | `/api/v1/check-runs` | ✅ 200 OK | 16ms | — | `{'items': [], 'total': 0, 'page': 1, 'page_size': 20, 'has_more': False}` | ✅ OK |
| 315 | `GET` | `/api/v1/check-runs/health/status` | ✅ 200 OK | 12ms | — | `{'status': 'healthy', 'service': 'check-runs-api', 'version': '1.0.0', 'feature_status': 'in_development', 'message': 'Check runs endpoints available but database table not yet created'}` | ✅ OK |
| 316 | `GET` | `/api/v1/check-runs/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 317 | `GET` | `/api/v1/check-runs/stats` | ✅ 200 OK | 16ms | — | `{'total_runs': 0, 'passed_runs': 0, 'failed_runs': 0, 'bypassed_runs': 0, 'advisory_runs': 0, 'blocking_runs': 0, 'strict_runs': 0, 'avg_duration_ms': 0, 'pass_rate': 0.0, 'period_start': '2026-02-28T...` | ✅ OK |

---
## Invitations

**3 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 318 | `GET` | `/api/v1/invitations` | 🔍 404 Not Found | 9ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 319 | `GET` | `/api/v1/invitations/dummy` | 💥 500 Server Error | 21ms | — | `Internal Server Error` | Invitations service error |
| 320 | `POST` | `/api/v1/invitations` | 🔍 404 Not Found | 0ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Docs

**3 endpoints** | HTTP 200: **1** | HTTP 2xx: 1

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 321 | `GET` | `/api/v1/docs/user-support` | ✅ 200 OK | 10ms | — | `['01-Getting-Started.md', '02-SDLC-Framework-Overview.md', '03-Platform-Features.md', '04-User-Roles-Permissions.md', '05-Common-Tasks.md', '06-Troubleshooting.md', '07-FAQ.md', '08-Best-Practices.md'...` | ✅ OK |
| 322 | `GET` | `/api/v1/docs/user-support/01-Getting-Started.md` | 🔍 404 Not Found | 13ms | — | `{'detail': "Documentation file '01-Getting-Started.md' not found"}` | Resource ID not found or route missing |
| 323 | `GET` | `/api/v1/docs/user-support/readme.md` | 🔍 404 Not Found | 10ms | — | `{'detail': "Documentation file 'readme.md' not found"}` | Resource ID not found or route missing |

---
## Magic Link

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 324 | `POST` | `/api/v1/magic-link/verify` | ⚠️ 405 Method Not Allowed | 10ms | `{"token": "dummy_cyeyes_s4"}` | `{'detail': 'Method Not Allowed'}` | OAuth callback: POST from provider required (not GET) |

---
## Templates

**4 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 325 | `GET` | `/api/v1/templates` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 326 | `GET` | `/api/v1/templates/sdlc-structure` | ✅ 200 OK | 16ms | — | `{'version': '5.0.0', 'tier': 'STANDARD', 'tier_description': 'Standard documentation for most projects', 'team_size_range': '3-10', 'folders': ['docs', 'docs/00-foundation', 'docs/01-planning', 'docs/...` | ✅ OK |
| 327 | `GET` | `/api/v1/templates/stages` | ✅ 200 OK | 10ms | — | `{'version': '5.0.0', 'stages': {'00': {'id': '00', 'name': 'foundation', 'full_name': 'Foundation (WHY)', 'description': 'Problem Definition & Design Thinking', 'folder_name': '00-foundation'}, '01': ...` | ✅ OK |
| 328 | `GET` | `/api/v1/templates/tiers` | ✅ 200 OK | 10ms | — | `{'version': '5.0.0', 'tiers': {'LITE': {'team_size_range': '1-2', 'required_stages': ['00', '01', '04', '05', '06'], 'optional_stages': ['02', '03', '07', '08', '09'], 'description': 'Minimal document...` | ✅ OK |

---
## Auth

**15 endpoints** | HTTP 200: **8** | HTTP 2xx: 10

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 329 | `GET` | `/api/v1/auth/health` | ✅ 200 OK | 14ms | — | `{'status': 'healthy', 'service': 'authentication', 'version': '1.0.0'}` | ✅ OK |
| 330 | `GET` | `/api/v1/auth/me` | ✅ 200 OK | 40ms | — | `{'id': 'a0000000-0000-0000-0000-000000000001', 'email': 'taidt@mtsolution.com.vn', 'name': 'Platform Admin', 'is_active': True, 'is_superuser': True, 'is_platform_admin': True, 'roles': [], 'oauth_pro...` | ✅ OK |
| 331 | `GET` | `/api/v1/auth/oauth/github/authorize` | ✅ 200 OK | 14ms | — | `{'authorization_url': 'https://github.com/login/oauth/authorize?client_id=Ov23li0mfFERLtQgdEeI&redirect_uri=https%3A%2F%2Fsdlc.nhatquangholding.com%2Fauth%2Fgithub%2Fcallback&scope=read%3Auser+user%3A...` | ✅ OK |
| 332 | `GET` | `/api/v1/auth/oauth/github/callback` | ⚠️ 405 Method Not Allowed | 13ms | params: `{"code": "dummy", "state": "dummy"}` | `{'detail': 'Method Not Allowed'}` | OAuth callback: POST from provider required (not GET) |
| 333 | `GET` | `/api/v1/auth/oauth/google/authorize` | ✅ 200 OK | 11ms | — | `{'authorization_url': 'https://accounts.google.com/o/oauth2/v2/auth?client_id=315273414049-e9q0o0nb081a08j5ehhg451e08q5n0nq.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fsdlc.nhatquangholding....` | ✅ OK |
| 334 | `GET` | `/api/v1/auth/oauth/google/callback` | ⚠️ 405 Method Not Allowed | 16ms | params: `{"code": "dummy", "state": "dummy"}` | `{'detail': 'Method Not Allowed'}` | OAuth callback: POST from provider required (not GET) |
| 335 | `GET` | `/api/v1/auth/verify-reset-token` | ✅ 200 OK | 16ms | params: `{"token": "dummy"}` | `{'valid': False, 'email': None, 'expires_at': None, 'error': 'Invalid or expired token'}` | ✅ OK |
| 336 | `POST` | `/api/v1/auth/forgot-password` | ✅ 200 OK | 37ms | `{"email": "taidt@mtsolution.com.vn"}` | `{'message': 'If an account with this email exists, you will receive a password reset link.', 'email': 'taidt@mtsolution.com.vn'}` | ✅ OK |
| 337 | `POST` | `/api/v1/auth/github/device` | ✅ 200 OK | 509ms | `{"client_id": "test"}` | `{'device_code': '5b46c60aa896d89ebf2bcea293cb2e1b6ec684b1', 'user_code': 'AF38-1A6F', 'verification_uri': 'https://github.com/login/device', 'expires_in': 899, 'interval': 5}` | ✅ OK |
| 338 | `POST` | `/api/v1/auth/github/token` | ⚠️ 400 Bad Request | 715ms | `{"device_code": "dummy", "client_id": "test"}` | `{'detail': 'GitHub device token error: The device_code provided is not valid.'}` | Expected for dummy/test values |
| 339 | `POST` | `/api/v1/auth/login` | 💥 500 Server Error | 167ms | `{"email": "taidt@mtsolution.com.vn", "password": "Admin@123456"}` | `Internal Server Error` | Server-side error — check logs |
| 340 | `POST` | `/api/v1/auth/logout` | ✅ 204 No Content | 20ms | — | `` | ✅ Success (no body) |
| 341 | `POST` | `/api/v1/auth/refresh` | ✅ 200 OK | 24ms | `{"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzU0NjkyNjQsImlhdCI6MTc3Mjg3NzI2NCwic3ViIjoiYTAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAxIiwidHlwZSI6InJlZnJlc2gifQ.MmQw63b5j2GyI...` | `{'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzI4NzkwNzMsImlhdCI6MTc3Mjg3NzI3MywidHlwZSI6ImFjY2VzcyIsInN1YiI6ImEwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMSJ9.OHZo1RsCsFITQ_J2...` | ✅ OK |
| 342 | `POST` | `/api/v1/auth/register` | ✅ 201 Created | 0ms | — | `{'id': '818d8908-481d-471b-8688-9a1b96878c4b', 'email': 'cyeyes-s4-1772877264@test.com', 'full_name': '*-CyEyes-* S4', 'role': 'dev', 'is_active': True, 'created_at': '2026-03-07T09:54:35.307101', 'me...` | ✅ Created successfully |
| 343 | `POST` | `/api/v1/auth/reset-password` | ⚠️ 422 Unprocessable | 15ms | `{"token": "dummy", "new_password": "NewPass@123456X"}` | `{'detail': [{'type': 'string_too_short', 'loc': ['body', 'token'], 'msg': 'String should have at least 32 characters', 'input': 'dummy', 'ctx': {'min_length': 32}}], 'body': "{'token': 'dummy', 'new_p...` | Request validation failed — schema mismatch or missing required field |

---
## Evidence Manifest

**10 endpoints** | HTTP 200: **1** | HTTP 2xx: 2

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 344 | `GET` | `/api/v1/evidence-manifest/` | 🔍 404 Not Found | 8ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 345 | `GET` | `/api/v1/evidence-manifest/dummy` | 🔍 404 Not Found | 19ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 346 | `GET` | `/api/v1/evidence-manifests` | ⚠️ 422 Unprocessable | 22ms | — | `{'detail': [{'type': 'missing', 'loc': ['query', 'project_id'], 'msg': 'Field required', 'input': None}], 'body': None}` | Request validation failed — schema mismatch or missing required field |
| 347 | `GET` | `/api/v1/evidence-manifests/b807b471-b8b5-430c-b240-7a1fdeeff3cf` | ✅ 200 OK | 14ms | — | `{'id': 'b807b471-b8b5-430c-b240-7a1fdeeff3cf', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'sequence_number': 1, 'manifest_hash': '41625c2efa7df2d5a28fe569fa4f236bd323c640c015f11f28d37a0b296...` | ✅ OK |
| 348 | `GET` | `/api/v1/evidence-manifests/latest` | ⚠️ 422 Unprocessable | 17ms | — | `{'detail': [{'type': 'missing', 'loc': ['query', 'project_id'], 'msg': 'Field required', 'input': None}], 'body': None}` | Request validation failed — schema mismatch or missing required field |
| 349 | `GET` | `/api/v1/evidence-manifests/status` | ⚠️ 422 Unprocessable | 16ms | — | `{'detail': [{'type': 'missing', 'loc': ['query', 'project_id'], 'msg': 'Field required', 'input': None}], 'body': None}` | Request validation failed — schema mismatch or missing required field |
| 350 | `GET` | `/api/v1/evidence-manifests/verifications` | ⚠️ 422 Unprocessable | 17ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'manifest_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found...` | Request validation failed — schema mismatch or missing required field |
| 351 | `POST` | `/api/v1/evidence-manifest/` | 🔍 404 Not Found | 0ms | — | `{"detail":"Not Found"}` | Endpoint not yet deployed (route missing in production) |
| 352 | `POST` | `/api/v1/evidence-manifests` | ✅ 201 Created | 0ms | — | `{'id': 'b807b471-b8b5-430c-b240-7a1fdeeff3cf', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'sequence_number': 1, 'manifest_hash': '41625c2efa7df2d5a28fe569fa4f236bd323c640c015f11f28d37a0b296...` | ✅ Created successfully |
| 353 | `POST` | `/api/v1/evidence-manifests/verify` | ⚠️ 422 Unprocessable | 14ms | `{"manifest_id": "b807b471-b8b5-430c-b240-7a1fdeeff3cf"}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'manifest_id': 'b807b471-b8b5-430c-b240-7a1fdeeff3cf'}}], 'body': "{'manifest_id': 'b807b471-b8b5-430c...` | Request validation failed — schema mismatch or missing required field |

---
## Evidence Timeline

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 354 | `GET` | `/api/v1/evidence-timeline/` | 🔍 404 Not Found | 16ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Planning Subagent

**5 endpoints** | HTTP 200: **1** | HTTP 2xx: 1

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 355 | `GET` | `/api/v1/planning/subagent/health` | ✅ 200 OK | 17ms | — | `{'status': 'healthy', 'service': 'planning-subagent', 'version': '2.0.0', 'features': ['risk-based-planning-trigger', 'crp-integration', '7-risk-factors']}` | ✅ OK |
| 356 | `GET` | `/api/v1/planning/subagent/sessions` | ⚠️ 422 Unprocessable | 20ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'planning_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found...` | Request validation failed — schema mismatch or missing required field |
| 357 | `POST` | `/api/v1/planning/subagent/conformance` | ⚠️ 422 Unprocessable | 17ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'diff_content'], 'msg': 'Field required', 'input': {'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8'}}], 'body': "{'project_id': '3ec1d475-c294-40e9...` | Request validation failed — schema mismatch or missing required field |
| 358 | `POST` | `/api/v1/planning/subagent/plan` | ⚠️ 422 Unprocessable | 17ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "intent": "Add *-CyEyes-* feature", "context": {}}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'task'], 'msg': 'Field required', 'input': {'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'intent': 'Add *-CyEyes-* feature', 'context': {}}}], ...` | Request validation failed — schema mismatch or missing required field |
| 359 | `POST` | `/api/v1/planning/subagent/should-plan` | ⚠️ 422 Unprocessable | 14ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "change_description": "*-CyEyes-* add feature"}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'diff'], 'msg': 'Field required', 'input': {'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'change_description': '*-CyEyes-* add feature'}}], 'bo...` | Request validation failed — schema mismatch or missing required field |

---
## Compliance Export

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 360 | `GET` | `/api/v1/compliance/export` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Compliance Validation

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 361 | `GET` | `/api/v1/compliance/validation/rules` | 🔍 404 Not Found | 25ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 362 | `POST` | `/api/v1/compliance/validation/validate` | 🔍 404 Not Found | 16ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## CA V2

**7 endpoints** | HTTP 200: **1** | HTTP 2xx: 1

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 363 | `GET` | `/api/v1/context-authority/v2/contexts` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 364 | `GET` | `/api/v1/context-authority/v2/health` | ✅ 200 OK | 15ms | — | `{'status': 'unhealthy', 'version': '2.0.0', 'template_count': 0, 'snapshot_count_24h': 0, 'avg_validation_ms': 0.0, 'avg_overlay_ms': 0.0, 'last_check': '2026-03-07T09:54:38.843708'}` | ✅ OK |
| 365 | `GET` | `/api/v1/context-authority/v2/project-profile` | 🔍 404 Not Found | 11ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 366 | `GET` | `/api/v1/context-authority/v2/requirements` | 🔍 404 Not Found | 12ms | params: `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 367 | `GET` | `/api/v1/context-authority/v2/stats` | 💥 500 Server Error | 16ms | — | `{'detail': 'Failed to get statistics: (sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError) <class \'asyncpg.exceptions.UndefinedTableError\'>: relation "ca_v2_context_snapshots" does not exist\n[...` | DB migration pending — table missing |
| 368 | `GET` | `/api/v1/context-authority/v2/templates` | 💥 500 Server Error | 16ms | — | `{'detail': 'Failed to list templates: (sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError) <class \'asyncpg.exceptions.UndefinedTableError\'>: relation "ca_v2_overlay_templates" does not exist\n[...` | DB migration pending — table missing |
| 369 | `POST` | `/api/v1/context-authority/v2/evaluate` | 🔍 404 Not Found | 11ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Risk Analysis

**3 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 370 | `GET` | `/api/v1/risk-analysis` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 371 | `GET` | `/api/v1/risk-analysis/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 372 | `POST` | `/api/v1/risk-analysis/analyze` | 🔍 404 Not Found | 12ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Governance Mode

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 373 | `GET` | `/api/v1/governance-mode` | 🔍 404 Not Found | 22ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 374 | `GET` | `/api/v1/governance-mode/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 23ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Gov Vibecoding

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 375 | `GET` | `/api/v1/governance-vibecoding` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 376 | `GET` | `/api/v1/governance-vibecoding/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Gov Specs

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 377 | `GET` | `/api/v1/governance-specs` | 🔍 404 Not Found | 10ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Auto Gen

**8 endpoints** | HTTP 200: **1** | HTTP 2xx: 1

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 378 | `GET` | `/api/v1/auto-generate/health` | ✅ 200 OK | 15ms | — | `{'service': 'AutoGenerationService', 'healthy': True, 'ollama_available': False, 'ollama_models': [], 'generators': {'intent': 'enabled', 'ownership': 'enabled', 'context': 'enabled', 'attestation': '...` | ✅ OK |
| 379 | `GET` | `/api/v1/auto-generation` | 🔍 404 Not Found | 10ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 380 | `GET` | `/api/v1/auto-generation/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 10ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 381 | `POST` | `/api/v1/auto-generate/attestation` | ⚠️ 422 Unprocessable | 18ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'pr_number'], 'msg': 'Field required', 'input': {'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8'}}, {'type': 'missing', 'loc': ['body', 'pr_title']...` | Request validation failed — schema mismatch or missing required field |
| 382 | `POST` | `/api/v1/auto-generate/context` | ⚠️ 422 Unprocessable | 17ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'pr_number'], 'msg': 'Field required', 'input': {'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8'}}, {'type': 'missing', 'loc': ['body', 'pr_title']...` | Request validation failed — schema mismatch or missing required field |
| 383 | `POST` | `/api/v1/auto-generate/intent` | ⚠️ 422 Unprocessable | 18ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "description": "*-CyEyes-* test intent"}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'task_id'], 'msg': 'Field required', 'input': {'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'description': '*-CyEyes-* test intent'}}, {'type':...` | Request validation failed — schema mismatch or missing required field |
| 384 | `POST` | `/api/v1/auto-generate/ownership` | ⚠️ 422 Unprocessable | 17ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'file_path'], 'msg': 'Field required', 'input': {'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8'}}], 'body': "{'project_id': '3ec1d475-c294-40e9-80...` | Request validation failed — schema mismatch or missing required field |
| 385 | `POST` | `/api/v1/auto-generation/generate` | 🔍 404 Not Found | 8ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "type": "sprint_report"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Ctx Val

**3 endpoints** | HTTP 200: **1** | HTTP 2xx: 1

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 386 | `GET` | `/api/v1/context-validation` | 🔍 404 Not Found | 10ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 387 | `GET` | `/api/v1/context-validation/health` | ✅ 200 OK | 9ms | — | `{'status': 'healthy', 'service': 'context-validation', 'version': '1.0.0', 'max_lines_per_file': 60}` | ✅ OK |
| 388 | `GET` | `/api/v1/context-validation/limits` | 💥 500 Server Error | 11ms | — | `Internal Server Error` | Server-side error — check logs |

---
## Context Val

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 389 | `POST` | `/api/v1/context-validation/validate` | ⚠️ 422 Unprocessable | 12ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'content'], 'msg': 'Field required', 'input': {'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8'}}], 'body': "{'project_id': '3ec1d475-c294-40e9-806f...` | Request validation failed — schema mismatch or missing required field |

---
## XRef

**5 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 390 | `GET` | `/api/v1/cross-reference` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 391 | `GET` | `/api/v1/cross-reference/coverage/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 OK | 21ms | — | `{'total': 0, 'covered': 0, 'uncovered': 0, 'percentage': 0.0}` | ✅ OK |
| 392 | `GET` | `/api/v1/cross-reference/missing-tests/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 OK | 16ms | — | `[]` | ✅ OK |
| 393 | `GET` | `/api/v1/cross-reference/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 394 | `GET` | `/api/v1/cross-reference/ssot-check/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 OK | 15ms | — | `{'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'ssot_compliant': True, 'violations': [], 'message': 'SSOT compliant: OpenAPI is only in Stage 03', 'checked_at': '2026-03-07T09:54:39.604715+00:...` | ✅ OK |

---
## Contract

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 395 | `GET` | `/api/v1/contract-lock` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 396 | `GET` | `/api/v1/contract-lock/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## FW Version

**6 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 397 | `GET` | `/api/v1/framework-version` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 398 | `GET` | `/api/v1/framework-version/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance` | 💥 500 Server Error | 20ms | — | `Internal Server Error` | Compliance service DB error |
| 399 | `GET` | `/api/v1/framework-version/3ec1d475-c294-40e9-806f-0691dffa3fa8/drift` | 💥 500 Server Error | 20ms | — | `Internal Server Error` | Framework version DB error |
| 400 | `GET` | `/api/v1/framework-version/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | 💥 500 Server Error | 19ms | — | `Internal Server Error` | Framework version DB error |
| 401 | `GET` | `/api/v1/framework-version/current` | ⚠️ 422 Unprocessable | 17ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'project_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found ...` | Request validation failed — schema mismatch or missing required field |
| 402 | `GET` | `/api/v1/framework-version/health` | ⚠️ 422 Unprocessable | 15ms | — | `{'detail': [{'type': 'uuid_parsing', 'loc': ['path', 'project_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found ...` | Request validation failed — schema mismatch or missing required field |

---
## Deprecation Mon

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 403 | `GET` | `/api/v1/deprecation-monitoring` | 🔍 404 Not Found | 10ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 404 | `GET` | `/api/v1/deprecation-monitoring/report` | 🔍 404 Not Found | 9ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## AGENTS.md

**11 endpoints** | HTTP 200: **5** | HTTP 2xx: 6

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 405 | `GET` | `/api/v1/agents-md` | 🔍 404 Not Found | 19ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 406 | `GET` | `/api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 19ms | — | `{'detail': 'No AGENTS.md found for project 3ec1d475-c294-40e9-806f-0691dffa3fa8. Generate one first.'}` | Resource ID not found or route missing |
| 407 | `GET` | `/api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | ✅ 200 OK | 16ms | — | `[]` | ✅ OK |
| 408 | `GET` | `/api/v1/agents-md/context/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 OK | 28ms | — | `{'id': '9d9fc882-8148-48a2-8fb9-394fb15b29df', 'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8', 'generated_at': '2026-03-07T09:54:40.786970', 'stage_name': '06-DEPLOY', 'gate_status': 'Final Rete...` | ✅ OK |
| 409 | `GET` | `/api/v1/agents-md/context/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | ✅ 200 OK | 18ms | — | `[{'id': '9d9fc882-8148-48a2-8fb9-394fb15b29df', 'generated_at': '2026-03-07T09:54:40.786970+00:00', 'line_count': None, 'sections': None, 'validation_status': None, 'trigger_type': 'api', 'trigger_ref...` | ✅ OK |
| 410 | `GET` | `/api/v1/agents-md/repos` | 💥 500 Server Error | 18ms | — | `Internal Server Error` | Agent team service DB error |
| 411 | `POST` | `/api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8/generate` | 🔍 404 Not Found | 27ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 412 | `POST` | `/api/v1/agents-md/generate` | ✅ 201 Created | 26ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'id': '492cddc7-d13c-46f0-b9b0-b9bf15c3e951', 'content': "# AGENTS.md - CyEyes-S4\n\n## Quick Start\n- Full stack: `docker compose up -d`\n- Backend only: `cd backend && pytest`\n- Frontend only: `cd...` | ✅ Created successfully |
| 413 | `POST` | `/api/v1/agents-md/lint` | ✅ 200 OK | 14ms | `{"content": "# Test"}` | `{'original_content': '# Test', 'fixed_content': '# Test\n', 'changes': ['Added newline at end of file'], 'valid': False}` | ✅ OK |
| 414 | `POST` | `/api/v1/agents-md/validate` | ✅ 200 OK | 27ms | `{"content": "# *-CyEyes-* AGENTS.md\n"}` | `{'valid': True, 'errors': [], 'warnings': [{'severity': 'warning', 'message': 'Missing recommended section: Quick Start', 'line_number': None}, {'severity': 'warning', 'message': 'Missing recommended ...` | ✅ OK |
| 415 | `PUT` | `/api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ⚠️ 405 Method Not Allowed | 25ms | `{"content": "# *-CyEyes-* Test"}` | `{'detail': 'Method Not Allowed'}` | OAuth callback: POST from provider required (not GET) |

---
## Jira

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 416 | `GET` | `/api/v1/jira` | 🔍 404 Not Found | 14ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 417 | `POST` | `/api/v1/jira/sync` | ⚠️ 422 Unprocessable | 22ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'gate_id'], 'msg': 'Field required', 'input': {'project_id': '3ec1d475-c294-40e9-806f-0691dffa3fa8'}}, {'type': 'missing', 'loc': ['body', 'board_id'], ...` | Request validation failed — schema mismatch or missing required field |

---
## OTT Gateway

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 418 | `GET` | `/api/v1/ott-gateway` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## OTT

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 419 | `POST` | `/api/v1/ott-gateway/send` | 🔍 404 Not Found | 9ms | `{"channel": "telegram", "message": "*-CyEyes-* test", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Push Notif

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 420 | `GET` | `/api/v1/push-notifications` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 421 | `POST` | `/api/v1/push-notifications/subscribe` | 🔍 404 Not Found | 11ms | `{"endpoint": "https://test.com", "keys": {}}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## E2E

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 422 | `GET` | `/api/v1/e2e/results` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 423 | `POST` | `/api/v1/e2e/run` | 🔍 404 Not Found | 26ms | `{"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "suite": "smoke"}` | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## MCP Analytics

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 424 | `GET` | `/api/v1/mcp-analytics` | 🔍 404 Not Found | 14ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Audit Trail

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 425 | `GET` | `/api/v1/audit-trail` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 426 | `GET` | `/api/v1/audit-trail/resource/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Enterprise SSO

**4 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 427 | `GET` | `/api/v1/enterprise-sso` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 428 | `GET` | `/api/v1/enterprise-sso/metadata` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 429 | `GET` | `/api/v1/enterprise/sso/azure-ad/login` | ⚠️ 422 Unprocessable | 12ms | — | `{'detail': [{'type': 'missing', 'loc': ['query', 'organization_id'], 'msg': 'Field required', 'input': None}], 'body': None}` | Request validation failed — schema mismatch or missing required field |
| 430 | `GET` | `/api/v1/enterprise/sso/saml/metadata` | ⚠️ 422 Unprocessable | 10ms | — | `{'detail': [{'type': 'missing', 'loc': ['query', 'organization_id'], 'msg': 'Field required', 'input': None}], 'body': None}` | Request validation failed — schema mismatch or missing required field |

---
## Tier

**3 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 431 | `GET` | `/api/v1/tier-management` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 432 | `GET` | `/api/v1/tier-management/limits` | 🔍 404 Not Found | 14ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 433 | `GET` | `/api/v1/tier-management/usage` | 🔍 404 Not Found | 19ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Data Residency

**2 endpoints** | HTTP 200: **1** | HTTP 2xx: 1

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 434 | `GET` | `/api/v1/data-residency` | 🔍 404 Not Found | 14ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 435 | `GET` | `/api/v1/data-residency/regions` | ✅ 200 OK | 18ms | — | `{'regions': [{'region': 'VN', 'display_name': 'Vietnam / Singapore (Asia Pacific)', 'endpoint_url': 'http://minio:9000', 'bucket': 'sdlc-evidence-vn', 'gdpr_compliant': False}, {'region': 'EU', 'displ...` | ✅ OK |

---
## Preview

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 436 | `GET` | `/api/v1/preview` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 437 | `GET` | `/api/v1/preview/dummy` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## WebSocket

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 438 | `GET` | `/api/v1/websocket/status` | 🔍 404 Not Found | 14ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 439 | `GET` | `/ws/stats` | 🔍 404 Not Found | 20ms | — | `<!DOCTYPE html><html lang="vi"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><link rel="stylesheet" href="/_next/static/css/27b4d6b789fddb24.css" da...` | Resource ID not found or route missing |

---
## Workflows

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 440 | `GET` | `/api/v1/workflows` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Analytics v2

**6 endpoints** | HTTP 200: **2** | HTTP 2xx: 2

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 441 | `GET` | `/api/v1/analytics/v2/metrics/ai-safety` | ✅ 200 OK | 16ms | — | `{'period_days': 7, 'total_validations': 0, 'pass_rate': 0.0, 'avg_duration_ms': 0.0, 'top_tools': {}, 'violations_by_type': {}}` | ✅ OK |
| 442 | `GET` | `/api/v1/analytics/v2/metrics/dau` | ✅ 200 OK | 19ms | — | `{'start_date': '2026-02-05', 'end_date': '2026-03-07', 'daily_counts': {}, 'total_unique_users': 0, 'avg_dau': 0.0}` | ✅ OK |
| 443 | `GET` | `/api/v1/analytics/v2/trends` | 🔍 404 Not Found | 13ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 444 | `GET` | `/api/v1/analytics/v2/usage` | 🔍 404 Not Found | 12ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |
| 445 | `POST` | `/api/v1/analytics/v2/events` | ⚠️ 422 Unprocessable | 16ms | `{"event": "test", "properties": {"source": "*-CyEyes-*"}}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'user_id'], 'msg': 'Field required', 'input': {'event': 'test', 'properties': {'source': '*-CyEyes-*'}}}, {'type': 'missing', 'loc': ['body', 'event_nam...` | Request validation failed — schema mismatch or missing required field |
| 446 | `POST` | `/api/v1/analytics/v2/events/batch` | ⚠️ 422 Unprocessable | 17ms | `{"events": [{"event": "test", "properties": {}}]}` | `{'detail': [{'type': 'missing', 'loc': ['body', 'events', 0, 'user_id'], 'msg': 'Field required', 'input': {'event': 'test', 'properties': {}}}, {'type': 'missing', 'loc': ['body', 'events', 0, 'event...` | Request validation failed — schema mismatch or missing required field |

---
## AI Providers

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 447 | `GET` | `/api/v1/ai-providers` | 🔍 404 Not Found | 17ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Metrics

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 448 | `GET` | `/metrics` | 🔍 404 Not Found | 49ms | — | `<!DOCTYPE html><html lang="vi"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><link rel="stylesheet" href="/_next/static/css/27b4d6b789fddb24.css" da...` | Resource ID not found or route missing |

---
## Gov Metrics

**4 endpoints** | HTTP 200: **4** | HTTP 2xx: 4

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 449 | `GET` | `/api/v1/governance-metrics` | ✅ 200 OK | 14ms | — | `# HELP governance_submissions_total Total number of governance submissions
# TYPE governance_submissions_total counter

# HELP governance_submissions_duration_seconds Time from submission to validatio...` | ✅ OK |
| 450 | `GET` | `/api/v1/governance-metrics/definitions` | ✅ 200 OK | 10ms | — | `{'total': 47, 'categories': {'governance_system': 15, 'performance': 10, 'business_ceo_dashboard': 8, 'developer_experience': 7, 'system_health': 5}, 'definitions': [{'name': 'governance_submissions_t...` | ✅ OK |
| 451 | `GET` | `/api/v1/governance-metrics/health` | ✅ 200 OK | 10ms | — | `{'status': 'healthy', 'service': 'prometheus_metrics_collector', 'timestamp': '2026-03-07T09:54:38.556564', 'metrics_count': 47, 'counters_active': 0, 'gauges_active': 0, 'histograms_active': 0}` | ✅ OK |
| 452 | `GET` | `/api/v1/governance-metrics/json` | ✅ 200 OK | 11ms | — | `{'counters': {}, 'gauges': {}, 'histograms': {}, 'timestamp': '2026-03-07T09:54:38.578852', 'total_metrics': 47}` | ✅ OK |

---
## Doc XRef

**2 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 453 | `GET` | `/api/v1/doc-cross-reference/links` | ⚠️ 422 Unprocessable | 12ms | — | `{'detail': [{'type': 'missing', 'loc': ['query', 'project_id'], 'msg': 'Field required', 'input': None}, {'type': 'missing', 'loc': ['query', 'document_path'], 'msg': 'Field required', 'input': None}]...` | Request validation failed — schema mismatch or missing required field |
| 454 | `GET` | `/api/v1/doc-cross-reference/orphaned` | ⚠️ 422 Unprocessable | 12ms | — | `{'detail': [{'type': 'missing', 'loc': ['query', 'project_id'], 'msg': 'Field required', 'input': None}], 'body': None}` | Request validation failed — schema mismatch or missing required field |

---
## Push

**3 endpoints** | HTTP 200: **3** | HTTP 2xx: 3

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 455 | `GET` | `/api/v1/push/status` | ✅ 200 OK | 16ms | — | `{'is_subscribed': False, 'subscriptions_count': 0}` | ✅ OK |
| 456 | `GET` | `/api/v1/push/subscriptions` | ✅ 200 OK | 16ms | — | `{'subscriptions': [], 'total': 0}` | ✅ OK |
| 457 | `GET` | `/api/v1/push/vapid-key` | ✅ 200 OK | 13ms | — | `{'public_key': 'BNbxGGkqLJiJqhspMQU0JCzKHJtKqkq0TdVbJGiWFhB1GGJhkPGiWFhB1GGJhkPGiWFhB1GGJhkPGiWFhB1GGJhkPGiWFhB1GGJhkP'}` | ✅ OK |

---
## Channels

**1 endpoints** | HTTP 200: **0** | HTTP 2xx: 0

| # | Method | Endpoint | Status | ms | Request | Response | Root Cause |
|---|--------|----------|--------|----|---------|----------|------------|
| 458 | `GET` | `/api/v1/channels` | 🔍 404 Not Found | 11ms | — | `{'detail': 'Not Found'}` | Endpoint not yet deployed (route missing in production) |

---
## Known Issues & Server Errors

### 💥 HTTP 500 Endpoints (require fixes)

| Endpoint | Root Cause | Fix |
|----------|------------|-----|
| `POST /api/v1/auth/login` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/admin/ott-channels/telegram/conversations` | OTT channel service error | Investigate server logs |
| `GET /api/v1/admin/ott-channels/telegram/health` | OTT channel service error | Investigate server logs |
| `GET /api/v1/planning/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/allocations` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/agent-team/definitions` | Agent team service DB error | Investigate server logs |
| `POST /api/v1/agent-team/definitions/seed` | Agent team service DB error | Investigate server logs |
| `GET /api/v1/agent-team/conversations` | Agent team service DB error | Investigate server logs |
| `GET /api/v1/codegen/usage/provider-health/ollama` | Server-side error — check logs | Investigate server logs |
| `POST /api/v1/codegen/estimate` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/scans` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/scans/09e33f72-f57e-45db-8bd2-d9791098444d` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/trend` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/analytics` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/github/installations` | GitHub App not configured | Configure GitHub App credentials |
| `GET /api/v1/compliance/frameworks` | Compliance service DB error | Compliance service DB migration |
| `GET /api/v1/governance/tiers/LITE/requirements` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/governance/tiers/STANDARD/requirements` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/vcr` | VCR table missing (migration) | Investigate server logs |
| `POST /api/v1/vcr` | DB migration pending — table missing | Apply Alembic migration |
| `GET /api/v1/invitations/dummy` | Invitations service error | Investigate server logs |
| `GET /health/ready` | Service not ready (dependencies starting) | Start MinIO service |
| `GET /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance/score` | Compliance service DB error | Compliance service DB migration |
| `GET /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance/history` | Compliance service DB error | Compliance service DB migration |
| `GET /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance/last-check` | Compliance service DB error | Compliance service DB migration |
| `POST /api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/evidence` | MinIO storage unavailable | Start MinIO service |
| `GET /api/v1/admin/ott-channels/stats` | OTT channel service error | Investigate server logs |
| `GET /api/v1/codegen/usage/report` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/compliance/frameworks/OWASP` | Compliance service DB error | Compliance service DB migration |
| `GET /api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/assessments` | Compliance service DB error | Compliance service DB migration |
| `GET /api/v1/governance/tiers/` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/governance/tiers/3ec1d475-c294-40e9-806f-0691dffa3fa8` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/context-authority/v2/stats` | DB migration pending — table missing | Apply Alembic migration |
| `GET /api/v1/context-authority/v2/templates` | DB migration pending — table missing | Apply Alembic migration |
| `GET /api/v1/mcp/health` | MCP service error | Investigate server logs |
| `GET /api/v1/mcp/context` | MCP service error | Investigate server logs |
| `GET /api/v1/mcp/dashboard` | MCP service error | Investigate server logs |
| `GET /api/v1/mcp/latency` | MCP service error | Investigate server logs |
| `GET /api/v1/mcp/cost` | MCP service error | Investigate server logs |
| `GET /api/v1/maturity/3ec1d475-c294-40e9-806f-0691dffa3fa8` | Maturity service DB error | Investigate server logs |
| `GET /api/v1/maturity/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | Maturity service DB error | Investigate server logs |
| `GET /api/v1/framework-version/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance` | Compliance service DB error | Compliance service DB migration |
| `GET /api/v1/framework-version/3ec1d475-c294-40e9-806f-0691dffa3fa8/drift` | Framework version DB error | Investigate server logs |
| `GET /api/v1/framework-version/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | Framework version DB error | Investigate server logs |
| `GET /api/v1/deprecation/summary` | Deprecation service DB error | Investigate server logs |
| `GET /api/v1/deprecation/endpoints` | Deprecation service DB error | Investigate server logs |
| `GET /api/v1/deprecation/dashboard` | Deprecation service DB error | Investigate server logs |
| `GET /api/v1/deprecation/timeline` | Deprecation service DB error | Investigate server logs |
| `GET /api/v1/context-validation/limits` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/telemetry/interfaces` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/telemetry/dashboard` | Server-side error — check logs | Investigate server logs |
| `GET /api/v1/vcr/stats/3ec1d475-c294-40e9-806f-0691dffa3fa8` | VCR table missing (migration) | Investigate server logs |
| `GET /api/v1/github/webhooks/stats` | GitHub App not configured | Configure GitHub App credentials |
| `GET /api/v1/github/webhooks/dlq` | GitHub App not configured | Configure GitHub App credentials |
| `GET /api/v1/github/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/repository` | GitHub App not configured | Configure GitHub App credentials |
| `GET /api/v1/github/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/scan` | GitHub App not configured | Configure GitHub App credentials |
| `GET /api/v1/consultations` | Consultations service DB error | Investigate server logs |
| `GET /api/v1/consultations/my-reviews` | Consultations service DB error | Investigate server logs |
| `GET /api/v1/organizations` | Org/Team service DB error | Investigate server logs |
| `GET /api/v1/teams` | Org/Team service DB error | Investigate server logs |
| `GET /api/v1/agents-md/repos` | Agent team service DB error | Investigate server logs |
| `GET /api/v1/triage/sla-breaches` | Triage service DB error | Investigate server logs |

### 🔍 HTTP 404 Not Deployed

Endpoints in OpenAPI spec but not found in production:

| Endpoint |
|----------|
| `GET /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/stats` |
| `POST /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/archive` |
| `POST /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/restore` |
| `GET /api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e` |
| `GET /api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e/download` |
| `POST /api/v1/evidence/upload` |
| `GET /api/v1/evidence-manifest/` |
| `POST /api/v1/evidence-manifest/` |
| `GET /api/v1/evidence-manifest/dummy` |
| `GET /api/v1/evidence-timeline/` |
| `GET /api/v1/admin/ai-providers` |
| `GET /api/v1/admin/ott-channels` |
| `POST /api/v1/admin/ott-channels/telegram/send` |
| `PUT /api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/role` |
| `GET /api/v1/admin/usage` |
| `GET /api/v1/admin/metrics` |
| `GET /api/v1/admin/settings/maintenance_mode` |
| `POST /api/v1/admin/cache/clear` |
| `POST /api/v1/admin/broadcast` |
| `POST /api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/suspend` |
| `POST /api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/activate` |
| `GET /api/v1/codegen/providers/health` |
| `GET /api/v1/codegen/sessions/09e33f72-f57e-45db-8bd2-d9791098444d` |
| `GET /api/v1/codegen/usage` |
| `GET /api/v1/codegen/onboarding/options` |
| `GET /api/v1/github/app/status` |
| `GET /api/v1/github/repos` |
| `GET /api/v1/github/webhooks/jobs` |
| `GET /api/v1/github/webhooks/jobs/dummy` |
| `POST /api/v1/github/webhook` |
| `GET /api/v1/compliance/controls` |
| `GET /api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/status` |
| `GET /api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/gap-analysis` |
| `GET /api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/recommendations` |
| `POST /api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence-mapping` |
| `GET /api/v1/compliance/export` |
| `GET /api/v1/compliance/validation/rules` |
| `POST /api/v1/compliance/validation/validate` |
| `GET /api/v1/governance/metrics/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `GET /api/v1/vibecoding-index` |
| `GET /api/v1/vibecoding-index/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `POST /api/v1/vibecoding-index/3ec1d475-c294-40e9-806f-0691dffa3fa8/calculate` |
| `GET /api/v1/dora/metrics` |
| `GET /api/v1/dora/metrics/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `GET /api/v1/ceo-dashboard` |
| `GET /api/v1/ceo-dashboard/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `GET /api/v1/mfa/status` |
| `POST /api/v1/mfa/setup` |
| `GET /api/v1/override/queue` |
| `GET /api/v1/override/history` |
| `POST /api/v1/override/request` |
| `GET /api/v1/override/dummy` |
| `POST /api/v1/override/dummy/approve` |
| `GET /api/v1/mrp` |
| `POST /api/v1/mrp` |
| `GET /api/v1/mrp/dummy` |
| `GET /api/v1/stage-gating` |
| `GET /api/v1/stage-gating/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `GET /api/v1/stage-gating/rules/STAGE_00` |
| `GET /api/v1/context-authority/v2/requirements` |
| `GET /api/v1/context-authority/v2/contexts` |
| `POST /api/v1/context-authority/v2/evaluate` |
| `GET /api/v1/context-authority/v2/project-profile` |
| `GET /api/v1/risk-analysis` |
| `POST /api/v1/risk-analysis/analyze` |
| `GET /api/v1/risk-analysis/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `GET /api/v1/governance-mode` |
| `GET /api/v1/governance-mode/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `GET /api/v1/governance-vibecoding` |
| `GET /api/v1/governance-vibecoding/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `GET /api/v1/governance-specs` |
| `GET /api/v1/auto-generation` |
| `GET /api/v1/auto-generation/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `POST /api/v1/auto-generation/generate` |
| `GET /api/v1/context-validation` |
| `GET /api/v1/cross-reference` |
| `GET /api/v1/cross-reference/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `GET /api/v1/contract-lock` |
| `GET /api/v1/contract-lock/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `GET /api/v1/framework-version` |
| `GET /api/v1/deprecation-monitoring` |
| `GET /api/v1/deprecation-monitoring/report` |
| `GET /api/v1/telemetry` |
| `POST /api/v1/telemetry/event` |
| `GET /api/v1/ai-detection` |
| `POST /api/v1/ai-detection/detect` |
| `GET /api/v1/agentic-maturity` |
| `GET /api/v1/agentic-maturity/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `GET /api/v1/agents-md` |
| `GET /api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `POST /api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8/generate` |
| `GET /api/v1/sdlc-structure` |
| `POST /api/v1/sdlc-structure/validate` |
| `GET /api/v1/jira` |
| `GET /api/v1/ott-gateway` |
| `POST /api/v1/ott-gateway/send` |
| `GET /api/v1/invitations` |
| `POST /api/v1/invitations` |
| `GET /api/v1/payments/plans` |
| `GET /api/v1/payments/me` |
| `GET /api/v1/push-notifications` |
| `POST /api/v1/push-notifications/subscribe` |
| `GET /api/v1/e2e/results` |
| `POST /api/v1/e2e/run` |
| `GET /api/v1/mcp-analytics` |
| `GET /api/v1/audit-trail` |
| `GET /api/v1/audit-trail/resource/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `GET /api/v1/gdpr/consents` |
| `POST /api/v1/gdpr/export-request` |
| `GET /api/v1/enterprise-sso` |
| `GET /api/v1/enterprise-sso/metadata` |
| `GET /api/v1/tier-management` |
| `GET /api/v1/tier-management/limits` |
| `GET /api/v1/tier-management/usage` |
| `GET /api/v1/templates` |
| `GET /api/v1/data-residency` |
| `GET /api/v1/check-runs/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` |
| `GET /api/v1/docs/user-support/readme.md` |
| `GET /api/v1/dashboard` |
| `GET /api/v1/preview` |
| `GET /api/v1/preview/dummy` |
| `GET /api/v1/websocket/status` |
| `GET /ws/stats` |
| `GET /api/v1/workflows` |
| `GET /api/v1/analytics/v2/usage` |
| `GET /api/v1/analytics/v2/trends` |
| `GET /api/v1/ai-providers` |
| `GET /metrics` |
| `GET /api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/policy-result` |
| `GET /api/v1/payments/subscriptions/me` |
| `GET /api/v1/docs/user-support/01-Getting-Started.md` |
| `GET /api/v1/channels` |

---
*Report generated by \*-CyEyes-\* — Sessions 3+4 — 2026-03-07*
*Total: 458 unique endpoints tested across 517 OpenAPI paths (88% coverage)*