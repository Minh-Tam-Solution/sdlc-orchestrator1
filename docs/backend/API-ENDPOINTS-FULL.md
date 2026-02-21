# API Endpoints Documentation - SDLC Orchestrator API

**Version**: 1.2.0
**Total Endpoints**: 636
**Generated**: Auto-generated from OpenAPI spec

---

## 📋 Table of Contents

1. [AGENTS.md](#agents.md) (16 endpoints)
2. [AI](#ai) (2 endpoints)
3. [AI Council](#ai-council) (10 endpoints)
4. [AI Detection](#ai-detection) (12 endpoints)
5. [AI Providers](#ai-providers) (10 endpoints)
6. [API Keys](#api-keys) (6 endpoints)
7. [Admin Panel](#admin-panel) (22 endpoints)
8. [Agentic Maturity](#agentic-maturity) (12 endpoints)
9. [Analytics](#analytics) (22 endpoints)
10. [Analytics V1 (DEPRECATED)](#analytics-v1-(deprecated)) (15 endpoints)
11. [Analytics v2](#analytics-v2) (8 endpoints)
12. [Authentication](#authentication) (26 endpoints)
13. [Auto-Generation](#auto-generation) (12 endpoints)
14. [CEO Dashboard](#ceo-dashboard) (14 endpoints)
15. [CRP - Consultations](#crp---consultations) (16 endpoints)
16. [Check Runs](#check-runs) (5 endpoints)
17. [Codegen](#codegen) (58 endpoints)
18. [Compliance](#compliance) (26 endpoints)
19. [Compliance Validation](#compliance-validation) (10 endpoints)
20. [Context Authority](#context-authority) (7 endpoints)
21. [Context Authority V1 (DEPRECATED)](#context-authority-v1-(deprecated)) (7 endpoints)
22. [Context Authority V2](#context-authority-v2) (22 endpoints)
23. [Context Overlay](#context-overlay) (2 endpoints)
24. [Context Validation](#context-validation) (8 endpoints)
25. [Contract Lock](#contract-lock) (14 endpoints)
26. [Cross-Reference](#cross-reference) (8 endpoints)
27. [Cross-Reference Validation](#cross-reference-validation) (4 endpoints)
28. [Dashboard](#dashboard) (2 endpoints)
29. [Dependencies](#dependencies) (10 endpoints)
30. [Deprecation Monitoring](#deprecation-monitoring) (8 endpoints)
31. [Documentation](#documentation) (4 endpoints)
32. [Dogfooding](#dogfooding) (20 endpoints)
33. [E2E Testing](#e2e-testing) (10 endpoints)
34. [Evidence](#evidence) (3 endpoints)
35. [Evidence Manifest](#evidence-manifest) (7 endpoints)
36. [Evidence Timeline](#evidence-timeline) (7 endpoints)
37. [Feedback](#feedback) (14 endpoints)
38. [Feedback Learning](#feedback-learning) (22 endpoints)
39. [Feedback Learning (EP-11)](#feedback-learning-(ep-11)) (22 endpoints)
40. [Framework Version](#framework-version) (12 endpoints)
41. [Gates](#gates) (24 endpoints)
42. [Gates Engine](#gates-engine) (16 endpoints)
43. [GitHub](#github) (13 endpoints)
44. [Governance Metrics](#governance-metrics) (14 endpoints)
45. [Governance Mode](#governance-mode) (8 endpoints)
46. [Governance Specs](#governance-specs) (5 endpoints)
47. [Governance Vibecoding](#governance-vibecoding) (7 endpoints)
48. [Grafana Dashboards](#grafana-dashboards) (7 endpoints)
49. [MCP Analytics](#mcp-analytics) (10 endpoints)
50. [MRP - Merge Readiness Protocol](#mrp---merge-readiness-protocol) (18 endpoints)
51. [MRP - Policy Enforcement](#mrp---policy-enforcement) (4 endpoints)
52. [Multi-Agent Team Engine](#multi-agent-team-engine) (20 endpoints)
53. [Notifications](#notifications) (8 endpoints)
54. [Organization Invitations](#organization-invitations) (7 endpoints)
55. [Organizations](#organizations) (6 endpoints)
56. [Override / VCR](#override-/-vcr) (9 endpoints)
57. [Payments](#payments) (5 endpoints)
58. [Pilot](#pilot) (13 endpoints)
59. [Planning](#planning) (46 endpoints)
60. [Planning Hierarchy](#planning-hierarchy) (150 endpoints)
61. [Planning Sub-agent](#planning-sub-agent) (16 endpoints)
62. [Policies](#policies) (5 endpoints)
63. [Policy Packs](#policy-packs) (8 endpoints)
64. [Preview](#preview) (6 endpoints)
65. [Projects](#projects) (10 endpoints)
66. [Push Notifications](#push-notifications) (10 endpoints)
67. [Resource Allocation](#resource-allocation) (11 endpoints)
68. [Retrospective](#retrospective) (9 endpoints)
69. [Risk Analysis](#risk-analysis) (8 endpoints)
70. [SAST](#sast) (14 endpoints)
71. [SDLC Structure](#sdlc-structure) (6 endpoints)
72. [SOP Generator](#sop-generator) (16 endpoints)
73. [Spec Converter](#spec-converter) (7 endpoints)
74. [Sprint 77](#sprint-77) (3 endpoints)
75. [Sprint 78](#sprint-78) (39 endpoints)
76. [Stage Gating](#stage-gating) (7 endpoints)
77. [Teams](#teams) (10 endpoints)
78. [Telemetry](#telemetry) (12 endpoints)
79. [Templates](#templates) (9 endpoints)
80. [Tier Management](#tier-management) (5 endpoints)
81. [Triage](#triage) (12 endpoints)
82. [Uncategorized](#uncategorized) (4 endpoints)
83. [VCR (Version Controlled Resolution)](#vcr-(version-controlled-resolution)) (22 endpoints)
84. [Vibecoding Index](#vibecoding-index) (7 endpoints)
85. [WebSocket](#websocket) (2 endpoints)
86. [dashboard](#dashboard) (2 endpoints)
87. [doc-cross-reference](#doc-cross-reference) (4 endpoints)
88. [dogfooding](#dogfooding) (20 endpoints)
89. [github](#github) (13 endpoints)
90. [organization-invitations](#organization-invitations) (7 endpoints)
91. [organizations](#organizations) (6 endpoints)
92. [payments](#payments) (5 endpoints)
93. [pilot](#pilot) (13 endpoints)
94. [projects](#projects) (10 endpoints)
95. [spec-converter](#spec-converter) (7 endpoints)
96. [teams](#teams) (10 endpoints)

---

## AGENTS.md (16 endpoints)

### 🔵 `GET /api/v1/agents-md/context/{project_id}`

**Summary**: Get context overlay

**Operation ID**: `get_context_overlay_api_v1_agents_md_context__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `format` | query | string | ❌ |
| `trigger_type` | query | string | ❌ |
| `trigger_ref` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agents-md/context/{project_id}`

**Summary**: Get context overlay

**Operation ID**: `get_context_overlay_api_v1_agents_md_context__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `format` | query | string | ❌ |
| `trigger_type` | query | string | ❌ |
| `trigger_ref` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agents-md/context/{project_id}/history`

**Summary**: Get context overlay history

**Operation ID**: `get_context_history_api_v1_agents_md_context__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Context History Api V1 Agents Md Context  Project Id  History Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agents-md/context/{project_id}/history`

**Summary**: Get context overlay history

**Operation ID**: `get_context_history_api_v1_agents_md_context__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Context History Api V1 Agents Md Context  Project Id  History Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agents-md/generate`

**Summary**: Generate AGENTS.md

**Operation ID**: `generate_agents_md_api_v1_agents_md_generate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agents-md/generate`

**Summary**: Generate AGENTS.md

**Operation ID**: `generate_agents_md_api_v1_agents_md_generate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agents-md/lint`

**Summary**: Lint AGENTS.md

**Operation ID**: `lint_agents_md_api_v1_agents_md_lint_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agents-md/lint`

**Summary**: Lint AGENTS.md

**Operation ID**: `lint_agents_md_api_v1_agents_md_lint_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agents-md/repos`

**Summary**: List all repositories with AGENTS.md status

**Operation ID**: `list_agents_md_repos_api_v1_agents_md_repos_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `status` | query | string | ❌ |
| `project_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agents-md/repos`

**Summary**: List all repositories with AGENTS.md status

**Operation ID**: `list_agents_md_repos_api_v1_agents_md_repos_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `status` | query | string | ❌ |
| `project_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agents-md/validate`

**Summary**: Validate AGENTS.md

**Operation ID**: `validate_agents_md_api_v1_agents_md_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agents-md/validate`

**Summary**: Validate AGENTS.md

**Operation ID**: `validate_agents_md_api_v1_agents_md_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agents-md/{project_id}`

**Summary**: Get latest AGENTS.md

**Operation ID**: `get_latest_agents_md_api_v1_agents_md__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agents-md/{project_id}`

**Summary**: Get latest AGENTS.md

**Operation ID**: `get_latest_agents_md_api_v1_agents_md__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agents-md/{project_id}/history`

**Summary**: Get AGENTS.md history

**Operation ID**: `get_agents_md_history_api_v1_agents_md__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Agents Md History Api V1 Agents Md  Project Id  History Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agents-md/{project_id}/history`

**Summary**: Get AGENTS.md history

**Operation ID**: `get_agents_md_history_api_v1_agents_md__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Agents Md History Api V1 Agents Md  Project Id  History Get`
- **422**: Validation Error
  - Schema: `object`

---

## AI (2 endpoints)

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/analytics`

**Summary**: Get comprehensive sprint analytics

**Operation ID**: `get_sprint_analytics_api_v1_planning_sprints__sprint_id__analytics_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/suggestions`

**Summary**: Get AI prioritization suggestions

**Operation ID**: `get_sprint_suggestions_api_v1_planning_sprints__sprint_id__suggestions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## AI Council (10 endpoints)

### 🟢 `POST /api/v1/council/decide`

**Summary**: Request council decision with sprint context

**Operation ID**: `request_council_decision_api_v1_council_decide_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/council/decide`

**Summary**: Request council decision with sprint context

**Operation ID**: `request_council_decision_api_v1_council_decide_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/council/deliberate`

**Summary**: Trigger AI Council deliberation

**Operation ID**: `trigger_deliberation_api_v1_council_deliberate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/council/deliberate`

**Summary**: Trigger AI Council deliberation

**Operation ID**: `trigger_deliberation_api_v1_council_deliberate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/council/history/{project_id}`

**Summary**: Get project council history

**Operation ID**: `get_project_council_history_api_v1_council_history__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `mode` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Project Council History Api V1 Council History  Project Id  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/council/history/{project_id}`

**Summary**: Get project council history

**Operation ID**: `get_project_council_history_api_v1_council_history__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `mode` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Project Council History Api V1 Council History  Project Id  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/council/stats/{project_id}`

**Summary**: Get project council statistics

**Operation ID**: `get_project_council_stats_api_v1_council_stats__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/council/stats/{project_id}`

**Summary**: Get project council statistics

**Operation ID**: `get_project_council_stats_api_v1_council_stats__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/council/status/{request_id}`

**Summary**: Get deliberation status

**Operation ID**: `get_deliberation_status_api_v1_council_status__request_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `request_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/council/status/{request_id}`

**Summary**: Get deliberation status

**Operation ID**: `get_deliberation_status_api_v1_council_status__request_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `request_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## AI Detection (12 endpoints)

### 🟢 `POST /api/v1/ai-detection/analyze`

**Summary**: Analyze Pr

**Operation ID**: `analyze_pr_api_v1_ai_detection_analyze_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/ai-detection/analyze`

**Summary**: Analyze Pr

**Operation ID**: `analyze_pr_api_v1_ai_detection_analyze_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/ai-detection/circuit-breakers`

**Summary**: Get Circuit Breakers

**Operation ID**: `get_circuit_breakers_api_v1_ai_detection_circuit_breakers_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Circuit Breakers Api V1 Ai Detection Circuit Breakers Get`

---

### 🔵 `GET /api/v1/ai-detection/circuit-breakers`

**Summary**: Get Circuit Breakers

**Operation ID**: `get_circuit_breakers_api_v1_ai_detection_circuit_breakers_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Circuit Breakers Api V1 Ai Detection Circuit Breakers Get`

---

### 🟢 `POST /api/v1/ai-detection/circuit-breakers/{breaker_name}/reset`

**Summary**: Reset Circuit Breaker

**Operation ID**: `reset_circuit_breaker_api_v1_ai_detection_circuit_breakers__breaker_name__reset_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `breaker_name` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Reset Circuit Breaker Api V1 Ai Detection Circuit Breakers  Breaker Name  Reset Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/ai-detection/circuit-breakers/{breaker_name}/reset`

**Summary**: Reset Circuit Breaker

**Operation ID**: `reset_circuit_breaker_api_v1_ai_detection_circuit_breakers__breaker_name__reset_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `breaker_name` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Reset Circuit Breaker Api V1 Ai Detection Circuit Breakers  Breaker Name  Reset Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/ai-detection/shadow-mode`

**Summary**: Get Shadow Mode

**Operation ID**: `get_shadow_mode_api_v1_ai_detection_shadow_mode_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Shadow Mode Api V1 Ai Detection Shadow Mode Get`

---

### 🔵 `GET /api/v1/ai-detection/shadow-mode`

**Summary**: Get Shadow Mode

**Operation ID**: `get_shadow_mode_api_v1_ai_detection_shadow_mode_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Shadow Mode Api V1 Ai Detection Shadow Mode Get`

---

### 🔵 `GET /api/v1/ai-detection/status`

**Summary**: Get Detection Status

**Operation ID**: `get_detection_status_api_v1_ai_detection_status_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/ai-detection/status`

**Summary**: Get Detection Status

**Operation ID**: `get_detection_status_api_v1_ai_detection_status_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/ai-detection/tools`

**Summary**: Get Supported Tools

**Operation ID**: `get_supported_tools_api_v1_ai_detection_tools_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Supported Tools Api V1 Ai Detection Tools Get`

---

### 🔵 `GET /api/v1/ai-detection/tools`

**Summary**: Get Supported Tools

**Operation ID**: `get_supported_tools_api_v1_ai_detection_tools_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Supported Tools Api V1 Ai Detection Tools Get`

---

## AI Providers (10 endpoints)

### 🔵 `GET /api/v1/admin/ai-providers/config`

**Summary**: Get AI provider configuration

**Operation ID**: `get_ai_provider_config_api_v1_admin_ai_providers_config_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/admin/ai-providers/config`

**Summary**: Get AI provider configuration

**Operation ID**: `get_ai_provider_config_api_v1_admin_ai_providers_config_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/admin/ai-providers/ollama/refresh-models`

**Summary**: Refresh Ollama models

**Operation ID**: `refresh_ollama_models_api_v1_admin_ai_providers_ollama_refresh_models_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/admin/ai-providers/ollama/refresh-models`

**Summary**: Refresh Ollama models

**Operation ID**: `refresh_ollama_models_api_v1_admin_ai_providers_ollama_refresh_models_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/admin/ai-providers/{provider}`

**Summary**: Update provider settings

**Operation ID**: `update_provider_settings_api_v1_admin_ai_providers__provider__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `provider` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Update Provider Settings Api V1 Admin Ai Providers  Provider  Patch`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/admin/ai-providers/{provider}`

**Summary**: Update provider settings

**Operation ID**: `update_provider_settings_api_v1_admin_ai_providers__provider__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `provider` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Update Provider Settings Api V1 Admin Ai Providers  Provider  Patch`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/admin/ai-providers/{provider}/models`

**Summary**: Get available models for provider

**Operation ID**: `get_provider_models_api_v1_admin_ai_providers__provider__models_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `provider` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/admin/ai-providers/{provider}/models`

**Summary**: Get available models for provider

**Operation ID**: `get_provider_models_api_v1_admin_ai_providers__provider__models_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `provider` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/admin/ai-providers/{provider}/test`

**Summary**: Test provider connection

**Operation ID**: `test_provider_connection_api_v1_admin_ai_providers__provider__test_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `provider` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/admin/ai-providers/{provider}/test`

**Summary**: Test provider connection

**Operation ID**: `test_provider_connection_api_v1_admin_ai_providers__provider__test_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `provider` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## API Keys (6 endpoints)

### 🔵 `GET /api/v1/api-keys`

**Summary**: List Api Keys

**Operation ID**: `list_api_keys_api_v1_api_keys_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Api Keys Api V1 Api Keys Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api-keys`

**Summary**: List Api Keys

**Operation ID**: `list_api_keys_api_v1_api_keys_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Api Keys Api V1 Api Keys Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api-keys`

**Summary**: Create Api Key

**Operation ID**: `create_api_key_api_v1_api_keys_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api-keys`

**Summary**: Create Api Key

**Operation ID**: `create_api_key_api_v1_api_keys_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/api-keys/{key_id}`

**Summary**: Revoke Api Key

**Operation ID**: `revoke_api_key_api_v1_api_keys__key_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `key_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/api-keys/{key_id}`

**Summary**: Revoke Api Key

**Operation ID**: `revoke_api_key_api_v1_api_keys__key_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `key_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

## Admin Panel (22 endpoints)

### 🔵 `GET /api/v1/admin/audit-logs`

**Summary**: List audit logs (paginated)

**Operation ID**: `list_audit_logs_api_v1_admin_audit_logs_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `action` | query | string | ❌ |
| `actor_id` | query | string | ❌ |
| `target_type` | query | string | ❌ |
| `date_from` | query | string | ❌ |
| `date_to` | query | string | ❌ |
| `search` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/admin/evidence/retention-archive`

**Summary**: Trigger evidence archival (ADR-027)

**Operation ID**: `trigger_evidence_archival_api_v1_admin_evidence_retention_archive_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Trigger Evidence Archival Api V1 Admin Evidence Retention Archive Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/admin/evidence/retention-purge`

**Summary**: Trigger evidence purge (ADR-027)

**Operation ID**: `trigger_evidence_purge_api_v1_admin_evidence_retention_purge_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Trigger Evidence Purge Api V1 Admin Evidence Retention Purge Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/admin/evidence/retention-stats`

**Summary**: Get evidence retention statistics (ADR-027)

**Operation ID**: `get_evidence_retention_stats_api_v1_admin_evidence_retention_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Evidence Retention Stats Api V1 Admin Evidence Retention Stats Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/admin/settings`

**Summary**: Get all system settings

**Operation ID**: `get_all_settings_api_v1_admin_settings_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/admin/settings/{key}`

**Summary**: Get setting by key

**Operation ID**: `get_setting_api_v1_admin_settings__key__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `key` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/admin/settings/{key}`

**Summary**: Update setting

**Operation ID**: `update_setting_api_v1_admin_settings__key__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `key` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/admin/settings/{key}/rollback`

**Summary**: Rollback setting

**Operation ID**: `rollback_setting_api_v1_admin_settings__key__rollback_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `key` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/admin/stats`

**Summary**: Get admin dashboard statistics

**Operation ID**: `get_admin_stats_api_v1_admin_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/admin/system/health`

**Summary**: Get system health

**Operation ID**: `get_system_health_api_v1_admin_system_health_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/admin/users`

**Summary**: List all users (paginated)

**Operation ID**: `list_users_api_v1_admin_users_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `search` | query | string | ❌ |
| `is_active` | query | string | ❌ |
| `is_superuser` | query | string | ❌ |
| `include_deleted` | query | boolean | ❌ |
| `sort_by` | query | string | ❌ |
| `sort_order` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/admin/users`

**Summary**: Create new user

**Operation ID**: `create_user_api_v1_admin_users_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/admin/users/bulk`

**Summary**: Bulk delete users (soft delete)

**Operation ID**: `bulk_delete_users_api_v1_admin_users_bulk_delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/admin/users/bulk`

**Summary**: Bulk user action

**Operation ID**: `bulk_user_action_api_v1_admin_users_bulk_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/admin/users/{user_id}`

**Summary**: Delete user (soft delete)

**Operation ID**: `delete_user_api_v1_admin_users__user_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/admin/users/{user_id}`

**Summary**: Get user details

**Operation ID**: `get_user_detail_api_v1_admin_users__user_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/admin/users/{user_id}`

**Summary**: Update user

**Operation ID**: `update_user_api_v1_admin_users__user_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/admin/users/{user_id}/mfa-exempt`

**Summary**: Set MFA exemption (ADR-027)

**Operation ID**: `set_mfa_exemption_api_v1_admin_users__user_id__mfa_exempt_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `Exempt`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Set Mfa Exemption Api V1 Admin Users  User Id  Mfa Exempt Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/admin/users/{user_id}/mfa-status`

**Summary**: Get user MFA status (ADR-027)

**Operation ID**: `get_user_mfa_status_api_v1_admin_users__user_id__mfa_status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get User Mfa Status Api V1 Admin Users  User Id  Mfa Status Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/admin/users/{user_id}/permanent`

**Summary**: Permanently delete user (Sprint 105)

**Operation ID**: `permanent_delete_user_api_v1_admin_users__user_id__permanent_delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/admin/users/{user_id}/restore`

**Summary**: Restore deleted user (Sprint 105)

**Operation ID**: `restore_user_api_v1_admin_users__user_id__restore_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/admin/users/{user_id}/unlock`

**Summary**: Unlock user account (ADR-027)

**Operation ID**: `unlock_user_account_api_v1_admin_users__user_id__unlock_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Unlock User Account Api V1 Admin Users  User Id  Unlock Post`
- **422**: Validation Error
  - Schema: `object`

---

## Agentic Maturity (12 endpoints)

### 🔵 `GET /api/v1/maturity/health`

**Summary**: Health check

**Operation ID**: `health_check_api_v1_maturity_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Maturity Health Get`

---

### 🔵 `GET /api/v1/maturity/health`

**Summary**: Health check

**Operation ID**: `health_check_api_v1_maturity_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Maturity Health Get`

---

### 🔵 `GET /api/v1/maturity/levels`

**Summary**: Get maturity level definitions

**Operation ID**: `get_maturity_levels_api_v1_maturity_levels_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Maturity Levels Api V1 Maturity Levels Get`

---

### 🔵 `GET /api/v1/maturity/levels`

**Summary**: Get maturity level definitions

**Operation ID**: `get_maturity_levels_api_v1_maturity_levels_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Maturity Levels Api V1 Maturity Levels Get`

---

### 🔵 `GET /api/v1/maturity/org/{org_id}`

**Summary**: Get org-wide maturity report

**Operation ID**: `get_org_maturity_report_api_v1_maturity_org__org_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `org_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/maturity/org/{org_id}`

**Summary**: Get org-wide maturity report

**Operation ID**: `get_org_maturity_report_api_v1_maturity_org__org_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `org_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/maturity/{project_id}`

**Summary**: Get latest maturity assessment

**Operation ID**: `get_latest_assessment_api_v1_maturity__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/maturity/{project_id}`

**Summary**: Get latest maturity assessment

**Operation ID**: `get_latest_assessment_api_v1_maturity__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/maturity/{project_id}/assess`

**Summary**: Perform fresh maturity assessment

**Operation ID**: `assess_project_maturity_api_v1_maturity__project_id__assess_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/maturity/{project_id}/assess`

**Summary**: Perform fresh maturity assessment

**Operation ID**: `assess_project_maturity_api_v1_maturity__project_id__assess_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/maturity/{project_id}/history`

**Summary**: Get assessment history

**Operation ID**: `get_assessment_history_api_v1_maturity__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/maturity/{project_id}/history`

**Summary**: Get assessment history

**Operation ID**: `get_assessment_history_api_v1_maturity__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Analytics (22 endpoints)

### 🔵 `GET /api/v1/analytics/circuit-breaker/status`

**Summary**: Get Circuit Breaker Status

**Operation ID**: `get_circuit_breaker_status_api_v1_analytics_circuit_breaker_status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Circuit Breaker Status Api V1 Analytics Circuit Breaker Status Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/engagement`

**Summary**: Get Engagement Summary

**Operation ID**: `get_engagement_summary_api_v1_analytics_engagement_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/events`

**Summary**: Track Event

**Operation ID**: `track_event_api_v1_analytics_events_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/events/feature`

**Summary**: Track Feature Use

**Operation ID**: `track_feature_use_api_v1_analytics_events_feature_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/events/page-view`

**Summary**: Track Page View

**Operation ID**: `track_page_view_api_v1_analytics_events_page_view_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/features`

**Summary**: Get Feature Usage

**Operation ID**: `get_feature_usage_api_v1_analytics_features_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Feature Usage Api V1 Analytics Features Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/my-activity`

**Summary**: Get My Activity

**Operation ID**: `get_my_activity_api_v1_analytics_my_activity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/pilot-metrics`

**Summary**: Get Pilot Metrics

**Operation ID**: `get_pilot_metrics_api_v1_analytics_pilot_metrics_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Pilot Metrics Api V1 Analytics Pilot Metrics Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/pilot-metrics/calculate`

**Summary**: Calculate Today Metrics

**Operation ID**: `calculate_today_metrics_api_v1_analytics_pilot_metrics_calculate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Calculate Today Metrics Api V1 Analytics Pilot Metrics Calculate Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/retention/cleanup`

**Summary**: Run Retention Cleanup

**Operation ID**: `run_retention_cleanup_api_v1_analytics_retention_cleanup_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Run Retention Cleanup Api V1 Analytics Retention Cleanup Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/retention/stats`

**Summary**: Get Retention Stats

**Operation ID**: `get_retention_stats_api_v1_analytics_retention_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Retention Stats Api V1 Analytics Retention Stats Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/sessions/active`

**Summary**: Get Active Session

**Operation ID**: `get_active_session_api_v1_analytics_sessions_active_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Active Session Api V1 Analytics Sessions Active Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/sessions/start`

**Summary**: Start Session

**Operation ID**: `start_session_api_v1_analytics_sessions_start_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/sessions/{session_id}/end`

**Summary**: End Session

**Operation ID**: `end_session_api_v1_analytics_sessions__session_id__end_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/summary`

**Summary**: Get Analytics Summary

**Operation ID**: `get_analytics_summary_api_v1_analytics_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `period_start` | query | string | ❌ |
| `period_end` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Analytics Summary Api V1 Analytics Summary Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/velocity`

**Summary**: Get project velocity metrics

**Operation ID**: `get_project_velocity_api_v1_planning_projects__project_id__velocity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_count` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/analytics`

**Summary**: Get comprehensive sprint analytics

**Operation ID**: `get_sprint_analytics_api_v1_planning_sprints__sprint_id__analytics_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/burndown`

**Summary**: Get sprint burndown chart data

**Operation ID**: `get_sprint_burndown_api_v1_planning_sprints__sprint_id__burndown_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/forecast`

**Summary**: Get sprint completion forecast

**Operation ID**: `get_sprint_forecast_api_v1_planning_sprints__sprint_id__forecast_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/health`

**Summary**: Get sprint health indicators

**Operation ID**: `get_sprint_health_api_v1_planning_sprints__sprint_id__health_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/retrospective`

**Summary**: Get auto-generated sprint retrospective

**Operation ID**: `get_sprint_retrospective_api_v1_planning_sprints__sprint_id__retrospective_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/suggestions`

**Summary**: Get AI prioritization suggestions

**Operation ID**: `get_sprint_suggestions_api_v1_planning_sprints__sprint_id__suggestions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Analytics V1 (DEPRECATED) (15 endpoints)

### 🔵 `GET /api/v1/analytics/circuit-breaker/status`

**Summary**: Get Circuit Breaker Status

**Operation ID**: `get_circuit_breaker_status_api_v1_analytics_circuit_breaker_status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Circuit Breaker Status Api V1 Analytics Circuit Breaker Status Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/engagement`

**Summary**: Get Engagement Summary

**Operation ID**: `get_engagement_summary_api_v1_analytics_engagement_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/events`

**Summary**: Track Event

**Operation ID**: `track_event_api_v1_analytics_events_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/events/feature`

**Summary**: Track Feature Use

**Operation ID**: `track_feature_use_api_v1_analytics_events_feature_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/events/page-view`

**Summary**: Track Page View

**Operation ID**: `track_page_view_api_v1_analytics_events_page_view_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/features`

**Summary**: Get Feature Usage

**Operation ID**: `get_feature_usage_api_v1_analytics_features_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Feature Usage Api V1 Analytics Features Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/my-activity`

**Summary**: Get My Activity

**Operation ID**: `get_my_activity_api_v1_analytics_my_activity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/pilot-metrics`

**Summary**: Get Pilot Metrics

**Operation ID**: `get_pilot_metrics_api_v1_analytics_pilot_metrics_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Pilot Metrics Api V1 Analytics Pilot Metrics Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/pilot-metrics/calculate`

**Summary**: Calculate Today Metrics

**Operation ID**: `calculate_today_metrics_api_v1_analytics_pilot_metrics_calculate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Calculate Today Metrics Api V1 Analytics Pilot Metrics Calculate Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/retention/cleanup`

**Summary**: Run Retention Cleanup

**Operation ID**: `run_retention_cleanup_api_v1_analytics_retention_cleanup_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Run Retention Cleanup Api V1 Analytics Retention Cleanup Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/retention/stats`

**Summary**: Get Retention Stats

**Operation ID**: `get_retention_stats_api_v1_analytics_retention_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Retention Stats Api V1 Analytics Retention Stats Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/sessions/active`

**Summary**: Get Active Session

**Operation ID**: `get_active_session_api_v1_analytics_sessions_active_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Active Session Api V1 Analytics Sessions Active Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/sessions/start`

**Summary**: Start Session

**Operation ID**: `start_session_api_v1_analytics_sessions_start_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/sessions/{session_id}/end`

**Summary**: End Session

**Operation ID**: `end_session_api_v1_analytics_sessions__session_id__end_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/summary`

**Summary**: Get Analytics Summary

**Operation ID**: `get_analytics_summary_api_v1_analytics_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `period_start` | query | string | ❌ |
| `period_end` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Analytics Summary Api V1 Analytics Summary Get`
- **422**: Validation Error
  - Schema: `object`

---

## Analytics v2 (8 endpoints)

### 🟢 `POST /api/v1/analytics/v2/events`

**Summary**: Track Event

**Operation ID**: `track_event_api_v1_analytics_v2_events_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/v2/events`

**Summary**: Track Event

**Operation ID**: `track_event_api_v1_analytics_v2_events_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/v2/events/batch`

**Summary**: Track Batch Events

**Operation ID**: `track_batch_events_api_v1_analytics_v2_events_batch_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/analytics/v2/events/batch`

**Summary**: Track Batch Events

**Operation ID**: `track_batch_events_api_v1_analytics_v2_events_batch_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/v2/metrics/ai-safety`

**Summary**: Get Ai Safety Metrics

**Operation ID**: `get_ai_safety_metrics_api_v1_analytics_v2_metrics_ai_safety_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/v2/metrics/ai-safety`

**Summary**: Get Ai Safety Metrics

**Operation ID**: `get_ai_safety_metrics_api_v1_analytics_v2_metrics_ai_safety_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/v2/metrics/dau`

**Summary**: Get Daily Active Users

**Operation ID**: `get_daily_active_users_api_v1_analytics_v2_metrics_dau_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/analytics/v2/metrics/dau`

**Summary**: Get Daily Active Users

**Operation ID**: `get_daily_active_users_api_v1_analytics_v2_metrics_dau_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Authentication (26 endpoints)

### 🟢 `POST /api/v1/auth/forgot-password`

**Summary**: Forgot Password

**Operation ID**: `forgot_password_api_v1_auth_forgot_password_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/forgot-password`

**Summary**: Forgot Password

**Operation ID**: `forgot_password_api_v1_auth_forgot_password_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/github/device`

**Summary**: Github Device Flow Init

**Operation ID**: `github_device_flow_init_api_v1_auth_github_device_post`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Github Device Flow Init Api V1 Auth Github Device Post`

---

### 🟢 `POST /api/v1/auth/github/device`

**Summary**: Github Device Flow Init

**Operation ID**: `github_device_flow_init_api_v1_auth_github_device_post`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Github Device Flow Init Api V1 Auth Github Device Post`

---

### 🟢 `POST /api/v1/auth/github/token`

**Summary**: Github Device Flow Poll

**Operation ID**: `github_device_flow_poll_api_v1_auth_github_token_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/github/token`

**Summary**: Github Device Flow Poll

**Operation ID**: `github_device_flow_poll_api_v1_auth_github_token_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/auth/health`

**Summary**: Auth Health Check

**Operation ID**: `auth_health_check_api_v1_auth_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Auth Health Check Api V1 Auth Health Get`

---

### 🔵 `GET /api/v1/auth/health`

**Summary**: Auth Health Check

**Operation ID**: `auth_health_check_api_v1_auth_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Auth Health Check Api V1 Auth Health Get`

---

### 🟢 `POST /api/v1/auth/login`

**Summary**: Login

**Operation ID**: `login_api_v1_auth_login_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/login`

**Summary**: Login

**Operation ID**: `login_api_v1_auth_login_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/logout`

**Summary**: Logout

**Operation ID**: `logout_api_v1_auth_logout_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_refresh_token` | cookie | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `Logout Data`

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/logout`

**Summary**: Logout

**Operation ID**: `logout_api_v1_auth_logout_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_refresh_token` | cookie | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `Logout Data`

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/auth/me`

**Summary**: Get Current User Profile

**Operation ID**: `get_current_user_profile_api_v1_auth_me_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/auth/me`

**Summary**: Get Current User Profile

**Operation ID**: `get_current_user_profile_api_v1_auth_me_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/auth/oauth/{provider}/authorize`

**Summary**: Oauth Authorize

**Operation ID**: `oauth_authorize_api_v1_auth_oauth__provider__authorize_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `provider` | path | string | ✅ |
| `redirect_uri` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/auth/oauth/{provider}/authorize`

**Summary**: Oauth Authorize

**Operation ID**: `oauth_authorize_api_v1_auth_oauth__provider__authorize_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `provider` | path | string | ✅ |
| `redirect_uri` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/oauth/{provider}/callback`

**Summary**: Oauth Callback

**Operation ID**: `oauth_callback_api_v1_auth_oauth__provider__callback_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `provider` | path | string | ✅ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/oauth/{provider}/callback`

**Summary**: Oauth Callback

**Operation ID**: `oauth_callback_api_v1_auth_oauth__provider__callback_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `provider` | path | string | ✅ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/refresh`

**Summary**: Refresh Access Token

**Operation ID**: `refresh_access_token_api_v1_auth_refresh_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_refresh_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `Refresh Data`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/refresh`

**Summary**: Refresh Access Token

**Operation ID**: `refresh_access_token_api_v1_auth_refresh_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_refresh_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `Refresh Data`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/register`

**Summary**: Register

**Operation ID**: `register_api_v1_auth_register_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/register`

**Summary**: Register

**Operation ID**: `register_api_v1_auth_register_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/reset-password`

**Summary**: Reset Password

**Operation ID**: `reset_password_api_v1_auth_reset_password_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auth/reset-password`

**Summary**: Reset Password

**Operation ID**: `reset_password_api_v1_auth_reset_password_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/auth/verify-reset-token`

**Summary**: Verify Reset Token

**Operation ID**: `verify_reset_token_api_v1_auth_verify_reset_token_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `token` | query | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/auth/verify-reset-token`

**Summary**: Verify Reset Token

**Operation ID**: `verify_reset_token_api_v1_auth_verify_reset_token_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `token` | query | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Auto-Generation (12 endpoints)

### 🟢 `POST /api/v1/auto-generate/all`

**Summary**: Generate All Compliance Artifacts

**Operation ID**: `generate_all_api_v1_auto_generate_all_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auto-generate/all`

**Summary**: Generate All Compliance Artifacts

**Operation ID**: `generate_all_api_v1_auto_generate_all_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auto-generate/attestation`

**Summary**: Generate AI Attestation

**Operation ID**: `generate_attestation_api_v1_auto_generate_attestation_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auto-generate/attestation`

**Summary**: Generate AI Attestation

**Operation ID**: `generate_attestation_api_v1_auto_generate_attestation_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auto-generate/context`

**Summary**: Attach Context to PR

**Operation ID**: `attach_context_api_v1_auto_generate_context_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auto-generate/context`

**Summary**: Attach Context to PR

**Operation ID**: `attach_context_api_v1_auto_generate_context_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/auto-generate/health`

**Summary**: Auto-Generation Health Check

**Operation ID**: `health_check_api_v1_auto_generate_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/auto-generate/health`

**Summary**: Auto-Generation Health Check

**Operation ID**: `health_check_api_v1_auto_generate_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🟢 `POST /api/v1/auto-generate/intent`

**Summary**: Generate Intent Document

**Operation ID**: `generate_intent_api_v1_auto_generate_intent_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auto-generate/intent`

**Summary**: Generate Intent Document

**Operation ID**: `generate_intent_api_v1_auto_generate_intent_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auto-generate/ownership`

**Summary**: Suggest File Ownership

**Operation ID**: `suggest_ownership_api_v1_auto_generate_ownership_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/auto-generate/ownership`

**Summary**: Suggest File Ownership

**Operation ID**: `suggest_ownership_api_v1_auto_generate_ownership_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## CEO Dashboard (14 endpoints)

### 🟢 `POST /api/v1/ceo-dashboard/decisions/{submission_id}/override`

**Summary**: Record CEO override for calibration

**Operation ID**: `record_override_api_v1_ceo_dashboard_decisions__submission_id__override_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `submission_id` | path | string | ✅ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Record Override Api V1 Ceo Dashboard Decisions  Submission Id  Override Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/ceo-dashboard/decisions/{submission_id}/resolve`

**Summary**: Resolve pending CEO decision

**Operation ID**: `resolve_decision_api_v1_ceo_dashboard_decisions__submission_id__resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `submission_id` | path | string | ✅ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Resolve Decision Api V1 Ceo Dashboard Decisions  Submission Id  Resolve Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/ceo-dashboard/health`

**Summary**: CEO Dashboard health check

**Operation ID**: `ceo_dashboard_health_api_v1_ceo_dashboard_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Ceo Dashboard Health Api V1 Ceo Dashboard Health Get`

---

### 🔵 `GET /api/v1/ceo-dashboard/overrides`

**Summary**: Get CEO overrides this week

**Operation ID**: `get_ceo_overrides_api_v1_ceo_dashboard_overrides_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Ceo Overrides Api V1 Ceo Dashboard Overrides Get`

---

### 🔵 `GET /api/v1/ceo-dashboard/pending-decisions`

**Summary**: Get pending CEO decisions queue

**Operation ID**: `get_pending_decisions_api_v1_ceo_dashboard_pending_decisions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `limit` | query | integer | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Pending Decisions Api V1 Ceo Dashboard Pending Decisions Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/ceo-dashboard/routing-breakdown`

**Summary**: Get PR routing breakdown

**Operation ID**: `get_routing_breakdown_api_v1_ceo_dashboard_routing_breakdown_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `time_range` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/ceo-dashboard/submissions`

**Summary**: Record governance submission

**Operation ID**: `record_submission_api_v1_ceo_dashboard_submissions_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Record Submission Api V1 Ceo Dashboard Submissions Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/ceo-dashboard/summary`

**Summary**: Get complete CEO dashboard summary

**Operation ID**: `get_dashboard_summary_api_v1_ceo_dashboard_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `time_range` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/ceo-dashboard/system-health`

**Summary**: Get system health snapshot

**Operation ID**: `get_system_health_api_v1_ceo_dashboard_system_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/ceo-dashboard/time-saved`

**Summary**: Get CEO time saved metrics

**Operation ID**: `get_time_saved_api_v1_ceo_dashboard_time_saved_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `time_range` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/ceo-dashboard/top-rejections`

**Summary**: Get top rejection reasons

**Operation ID**: `get_top_rejections_api_v1_ceo_dashboard_top_rejections_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `time_range` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Top Rejections Api V1 Ceo Dashboard Top Rejections Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/ceo-dashboard/trends/time-saved`

**Summary**: Get time saved trend (8 weeks)

**Operation ID**: `get_time_saved_trend_api_v1_ceo_dashboard_trends_time_saved_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Time Saved Trend Api V1 Ceo Dashboard Trends Time Saved Get`

---

### 🔵 `GET /api/v1/ceo-dashboard/trends/vibecoding-index`

**Summary**: Get vibecoding index trend (7 days)

**Operation ID**: `get_vibecoding_index_trend_api_v1_ceo_dashboard_trends_vibecoding_index_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Vibecoding Index Trend Api V1 Ceo Dashboard Trends Vibecoding Index Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/ceo-dashboard/weekly-summary`

**Summary**: Get weekly governance summary

**Operation ID**: `get_weekly_summary_api_v1_ceo_dashboard_weekly_summary_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

## CRP - Consultations (16 endpoints)

### 🔵 `GET /api/v1/consultations`

**Summary**: List consultations

**Operation ID**: `list_consultations_api_v1_consultations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `status` | query | string | ❌ |
| `priority` | query | string | ❌ |
| `reviewer_id` | query | string | ❌ |
| `expertise` | query | string | ❌ |
| `search` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/consultations`

**Summary**: List consultations

**Operation ID**: `list_consultations_api_v1_consultations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `status` | query | string | ❌ |
| `priority` | query | string | ❌ |
| `reviewer_id` | query | string | ❌ |
| `expertise` | query | string | ❌ |
| `search` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/consultations`

**Summary**: Create consultation request

**Operation ID**: `create_consultation_api_v1_consultations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/consultations`

**Summary**: Create consultation request

**Operation ID**: `create_consultation_api_v1_consultations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/consultations/auto-generate`

**Summary**: AI-assisted CRP generation

**Operation ID**: `auto_generate_crp_api_v1_consultations_auto_generate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/consultations/auto-generate`

**Summary**: AI-assisted CRP generation

**Operation ID**: `auto_generate_crp_api_v1_consultations_auto_generate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/consultations/my-reviews`

**Summary**: Get my pending reviews

**Operation ID**: `get_my_pending_reviews_api_v1_consultations_my_reviews_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get My Pending Reviews Api V1 Consultations My Reviews Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/consultations/my-reviews`

**Summary**: Get my pending reviews

**Operation ID**: `get_my_pending_reviews_api_v1_consultations_my_reviews_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get My Pending Reviews Api V1 Consultations My Reviews Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/consultations/{consultation_id}`

**Summary**: Get consultation

**Operation ID**: `get_consultation_api_v1_consultations__consultation_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `consultation_id` | path | string | ✅ |
| `include_comments` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/consultations/{consultation_id}`

**Summary**: Get consultation

**Operation ID**: `get_consultation_api_v1_consultations__consultation_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `consultation_id` | path | string | ✅ |
| `include_comments` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/consultations/{consultation_id}/assign`

**Summary**: Assign reviewer

**Operation ID**: `assign_reviewer_api_v1_consultations__consultation_id__assign_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `consultation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/consultations/{consultation_id}/assign`

**Summary**: Assign reviewer

**Operation ID**: `assign_reviewer_api_v1_consultations__consultation_id__assign_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `consultation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/consultations/{consultation_id}/comments`

**Summary**: Add comment

**Operation ID**: `add_comment_api_v1_consultations__consultation_id__comments_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `consultation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/consultations/{consultation_id}/comments`

**Summary**: Add comment

**Operation ID**: `add_comment_api_v1_consultations__consultation_id__comments_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `consultation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/consultations/{consultation_id}/resolve`

**Summary**: Resolve consultation

**Operation ID**: `resolve_consultation_api_v1_consultations__consultation_id__resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `consultation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/consultations/{consultation_id}/resolve`

**Summary**: Resolve consultation

**Operation ID**: `resolve_consultation_api_v1_consultations__consultation_id__resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `consultation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Check Runs (5 endpoints)

### 🔵 `GET /api/v1/check-runs`

**Summary**: List Check Runs

**Operation ID**: `list_check_runs_api_v1_check_runs_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `project_id` | query | string | ❌ |
| `repository` | query | string | ❌ |
| `status` | query | string | ❌ |
| `conclusion` | query | string | ❌ |
| `mode` | query | string | ❌ |
| `from_date` | query | string | ❌ |
| `to_date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/check-runs/health/status`

**Summary**: Health Check

**Operation ID**: `health_check_api_v1_check_runs_health_status_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Check Runs Health Status Get`

---

### 🔵 `GET /api/v1/check-runs/stats`

**Summary**: Get Check Run Stats

**Operation ID**: `get_check_run_stats_api_v1_check_runs_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `period_days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/check-runs/{check_run_id}`

**Summary**: Get Check Run

**Operation ID**: `get_check_run_api_v1_check_runs__check_run_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `check_run_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Check Run Api V1 Check Runs  Check Run Id  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/check-runs/{check_run_id}/rerun`

**Summary**: Rerun Check Run

**Operation ID**: `rerun_check_run_api_v1_check_runs__check_run_id__rerun_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `check_run_id` | path | string | ✅ |
| `force` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Rerun Check Run Api V1 Check Runs  Check Run Id  Rerun Post`
- **422**: Validation Error
  - Schema: `object`

---

## Codegen (58 endpoints)

### 🟢 `POST /api/v1/codegen/estimate`

**Summary**: Estimate Cost

**Operation ID**: `estimate_cost_api_v1_codegen_estimate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/estimate`

**Summary**: Estimate Cost

**Operation ID**: `estimate_cost_api_v1_codegen_estimate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/generate`

**Summary**: Generate Code

**Operation ID**: `generate_code_api_v1_codegen_generate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/generate`

**Summary**: Generate Code

**Operation ID**: `generate_code_api_v1_codegen_generate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/generate/full`

**Summary**: Generate With Quality

**Operation ID**: `generate_with_quality_api_v1_codegen_generate_full_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/generate/full`

**Summary**: Generate With Quality

**Operation ID**: `generate_with_quality_api_v1_codegen_generate_full_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/generate/resume/{session_id}`

**Summary**: Resume Generation

**Operation ID**: `resume_generation_api_v1_codegen_generate_resume__session_id__post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/generate/resume/{session_id}`

**Summary**: Resume Generation

**Operation ID**: `resume_generation_api_v1_codegen_generate_resume__session_id__post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/generate/stream`

**Summary**: Generate Stream

**Operation ID**: `generate_stream_api_v1_codegen_generate_stream_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/generate/stream`

**Summary**: Generate Stream

**Operation ID**: `generate_stream_api_v1_codegen_generate_stream_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/generate/zip`

**Summary**: Generate Zip

**Operation ID**: `generate_zip_api_v1_codegen_generate_zip_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/generate/zip`

**Summary**: Generate Zip

**Operation ID**: `generate_zip_api_v1_codegen_generate_zip_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/health`

**Summary**: Health Check

**Operation ID**: `health_check_api_v1_codegen_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/health`

**Summary**: Health Check

**Operation ID**: `health_check_api_v1_codegen_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/ir/generate`

**Summary**: Ir Generate

**Operation ID**: `ir_generate_api_v1_codegen_ir_generate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/ir/generate`

**Summary**: Ir Generate

**Operation ID**: `ir_generate_api_v1_codegen_ir_generate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/ir/validate`

**Summary**: Ir Validate

**Operation ID**: `ir_validate_api_v1_codegen_ir_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/ir/validate`

**Summary**: Ir Validate

**Operation ID**: `ir_validate_api_v1_codegen_ir_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/onboarding/options/domains`

**Summary**: Get Domain Options

**Operation ID**: `get_domain_options_api_v1_codegen_onboarding_options_domains_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Domain Options Api V1 Codegen Onboarding Options Domains Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/onboarding/options/domains`

**Summary**: Get Domain Options

**Operation ID**: `get_domain_options_api_v1_codegen_onboarding_options_domains_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Domain Options Api V1 Codegen Onboarding Options Domains Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/onboarding/options/features/{domain}`

**Summary**: Get Feature Options

**Operation ID**: `get_feature_options_api_v1_codegen_onboarding_options_features__domain__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `domain` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Feature Options Api V1 Codegen Onboarding Options Features  Domain  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/onboarding/options/features/{domain}`

**Summary**: Get Feature Options

**Operation ID**: `get_feature_options_api_v1_codegen_onboarding_options_features__domain__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `domain` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Feature Options Api V1 Codegen Onboarding Options Features  Domain  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/onboarding/options/scales`

**Summary**: Get Scale Options

**Operation ID**: `get_scale_options_api_v1_codegen_onboarding_options_scales_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Scale Options Api V1 Codegen Onboarding Options Scales Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/onboarding/options/scales`

**Summary**: Get Scale Options

**Operation ID**: `get_scale_options_api_v1_codegen_onboarding_options_scales_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Scale Options Api V1 Codegen Onboarding Options Scales Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/onboarding/start`

**Summary**: Start Onboarding

**Operation ID**: `start_onboarding_api_v1_codegen_onboarding_start_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/onboarding/start`

**Summary**: Start Onboarding

**Operation ID**: `start_onboarding_api_v1_codegen_onboarding_start_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/onboarding/{session_id}`

**Summary**: Get Onboarding Session

**Operation ID**: `get_onboarding_session_api_v1_codegen_onboarding__session_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/onboarding/{session_id}`

**Summary**: Get Onboarding Session

**Operation ID**: `get_onboarding_session_api_v1_codegen_onboarding__session_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/onboarding/{session_id}/app_name`

**Summary**: Set Onboarding App Name

**Operation ID**: `set_onboarding_app_name_api_v1_codegen_onboarding__session_id__app_name_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/onboarding/{session_id}/app_name`

**Summary**: Set Onboarding App Name

**Operation ID**: `set_onboarding_app_name_api_v1_codegen_onboarding__session_id__app_name_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/onboarding/{session_id}/domain`

**Summary**: Set Onboarding Domain

**Operation ID**: `set_onboarding_domain_api_v1_codegen_onboarding__session_id__domain_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/onboarding/{session_id}/domain`

**Summary**: Set Onboarding Domain

**Operation ID**: `set_onboarding_domain_api_v1_codegen_onboarding__session_id__domain_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/onboarding/{session_id}/features`

**Summary**: Set Onboarding Features

**Operation ID**: `set_onboarding_features_api_v1_codegen_onboarding__session_id__features_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/onboarding/{session_id}/features`

**Summary**: Set Onboarding Features

**Operation ID**: `set_onboarding_features_api_v1_codegen_onboarding__session_id__features_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/onboarding/{session_id}/generate`

**Summary**: Generate Onboarding Blueprint

**Operation ID**: `generate_onboarding_blueprint_api_v1_codegen_onboarding__session_id__generate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/onboarding/{session_id}/generate`

**Summary**: Generate Onboarding Blueprint

**Operation ID**: `generate_onboarding_blueprint_api_v1_codegen_onboarding__session_id__generate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/onboarding/{session_id}/scale`

**Summary**: Set Onboarding Scale

**Operation ID**: `set_onboarding_scale_api_v1_codegen_onboarding__session_id__scale_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/onboarding/{session_id}/scale`

**Summary**: Set Onboarding Scale

**Operation ID**: `set_onboarding_scale_api_v1_codegen_onboarding__session_id__scale_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/providers`

**Summary**: List Providers

**Operation ID**: `list_providers_api_v1_codegen_providers_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/providers`

**Summary**: List Providers

**Operation ID**: `list_providers_api_v1_codegen_providers_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/sessions`

**Summary**: List Sessions

**Operation ID**: `list_sessions_api_v1_codegen_sessions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `status_filter` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/sessions`

**Summary**: List Sessions

**Operation ID**: `list_sessions_api_v1_codegen_sessions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `status_filter` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/sessions/active`

**Summary**: List Active Sessions

**Operation ID**: `list_active_sessions_api_v1_codegen_sessions_active_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/sessions/active`

**Summary**: List Active Sessions

**Operation ID**: `list_active_sessions_api_v1_codegen_sessions_active_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/sessions/{session_id}`

**Summary**: Get Session Status

**Operation ID**: `get_session_status_api_v1_codegen_sessions__session_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/sessions/{session_id}`

**Summary**: Get Session Status

**Operation ID**: `get_session_status_api_v1_codegen_sessions__session_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/sessions/{session_id}/quality/stream`

**Summary**: Stream Quality Pipeline

**Operation ID**: `stream_quality_pipeline_api_v1_codegen_sessions__session_id__quality_stream_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/sessions/{session_id}/quality/stream`

**Summary**: Stream Quality Pipeline

**Operation ID**: `stream_quality_pipeline_api_v1_codegen_sessions__session_id__quality_stream_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/templates`

**Summary**: List Templates

**Operation ID**: `list_templates_api_v1_codegen_templates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Templates Api V1 Codegen Templates Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/templates`

**Summary**: List Templates

**Operation ID**: `list_templates_api_v1_codegen_templates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Templates Api V1 Codegen Templates Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/usage/monthly`

**Summary**: Get Monthly Cost

**Operation ID**: `get_monthly_cost_api_v1_codegen_usage_monthly_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `year` | query | integer | ✅ |
| `month` | query | integer | ✅ |
| `project_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/usage/monthly`

**Summary**: Get Monthly Cost

**Operation ID**: `get_monthly_cost_api_v1_codegen_usage_monthly_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `year` | query | integer | ✅ |
| `month` | query | integer | ✅ |
| `project_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/usage/provider-health/{provider}`

**Summary**: Get Provider Health History

**Operation ID**: `get_provider_health_history_api_v1_codegen_usage_provider_health__provider__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `provider` | path | string | ✅ |
| `hours` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/usage/provider-health/{provider}`

**Summary**: Get Provider Health History

**Operation ID**: `get_provider_health_history_api_v1_codegen_usage_provider_health__provider__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `provider` | path | string | ✅ |
| `hours` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/usage/report`

**Summary**: Get Cost Report

**Operation ID**: `get_cost_report_api_v1_codegen_usage_report_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `project_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/usage/report`

**Summary**: Get Cost Report

**Operation ID**: `get_cost_report_api_v1_codegen_usage_report_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `project_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/validate`

**Summary**: Validate Code

**Operation ID**: `validate_code_api_v1_codegen_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/validate`

**Summary**: Validate Code

**Operation ID**: `validate_code_api_v1_codegen_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Compliance (26 endpoints)

### 🔵 `GET /api/v1/compliance/ai/budget`

**Summary**: Get AI budget status

**Operation ID**: `get_ai_budget_status_api_v1_compliance_ai_budget_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/ai/budget`

**Summary**: Get AI budget status

**Operation ID**: `get_ai_budget_status_api_v1_compliance_ai_budget_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/ai/models`

**Summary**: List available Ollama models

**Operation ID**: `list_ollama_models_api_v1_compliance_ai_models_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Ollama Models Api V1 Compliance Ai Models Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/ai/models`

**Summary**: List available Ollama models

**Operation ID**: `list_ollama_models_api_v1_compliance_ai_models_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Ollama Models Api V1 Compliance Ai Models Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/ai/providers`

**Summary**: Get AI providers status

**Operation ID**: `get_ai_providers_status_api_v1_compliance_ai_providers_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/ai/providers`

**Summary**: Get AI providers status

**Operation ID**: `get_ai_providers_status_api_v1_compliance_ai_providers_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/compliance/ai/recommendations`

**Summary**: Generate AI recommendation

**Operation ID**: `generate_ai_recommendation_api_v1_compliance_ai_recommendations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/compliance/ai/recommendations`

**Summary**: Generate AI recommendation

**Operation ID**: `generate_ai_recommendation_api_v1_compliance_ai_recommendations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/jobs/{job_id}`

**Summary**: Get scan job status

**Operation ID**: `get_job_status_api_v1_compliance_jobs__job_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `job_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/jobs/{job_id}`

**Summary**: Get scan job status

**Operation ID**: `get_job_status_api_v1_compliance_jobs__job_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `job_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/queue/status`

**Summary**: Get scan queue status

**Operation ID**: `get_queue_status_endpoint_api_v1_compliance_queue_status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/queue/status`

**Summary**: Get scan queue status

**Operation ID**: `get_queue_status_endpoint_api_v1_compliance_queue_status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/compliance/scans/{project_id}`

**Summary**: Trigger compliance scan

**Operation ID**: `trigger_scan_api_v1_compliance_scans__project_id__post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/compliance/scans/{project_id}`

**Summary**: Trigger compliance scan

**Operation ID**: `trigger_scan_api_v1_compliance_scans__project_id__post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/scans/{project_id}/history`

**Summary**: Get scan history

**Operation ID**: `get_scan_history_api_v1_compliance_scans__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Scan History Api V1 Compliance Scans  Project Id  History Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/scans/{project_id}/history`

**Summary**: Get scan history

**Operation ID**: `get_scan_history_api_v1_compliance_scans__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Scan History Api V1 Compliance Scans  Project Id  History Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/scans/{project_id}/latest`

**Summary**: Get latest scan result

**Operation ID**: `get_latest_scan_api_v1_compliance_scans__project_id__latest_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/scans/{project_id}/latest`

**Summary**: Get latest scan result

**Operation ID**: `get_latest_scan_api_v1_compliance_scans__project_id__latest_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/compliance/scans/{project_id}/schedule`

**Summary**: Schedule compliance scan

**Operation ID**: `schedule_scan_api_v1_compliance_scans__project_id__schedule_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **202**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/compliance/scans/{project_id}/schedule`

**Summary**: Schedule compliance scan

**Operation ID**: `schedule_scan_api_v1_compliance_scans__project_id__schedule_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **202**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/violations/{project_id}`

**Summary**: Get project violations

**Operation ID**: `get_project_violations_api_v1_compliance_violations__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `resolved` | query | string | ❌ |
| `severity` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Project Violations Api V1 Compliance Violations  Project Id  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/compliance/violations/{project_id}`

**Summary**: Get project violations

**Operation ID**: `get_project_violations_api_v1_compliance_violations__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `resolved` | query | string | ❌ |
| `severity` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Project Violations Api V1 Compliance Violations  Project Id  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/compliance/violations/{violation_id}/ai-recommendation`

**Summary**: Generate recommendation for violation

**Operation ID**: `generate_violation_recommendation_api_v1_compliance_violations__violation_id__ai_recommendation_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `violation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/compliance/violations/{violation_id}/ai-recommendation`

**Summary**: Generate recommendation for violation

**Operation ID**: `generate_violation_recommendation_api_v1_compliance_violations__violation_id__ai_recommendation_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `violation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/compliance/violations/{violation_id}/resolve`

**Summary**: Resolve violation

**Operation ID**: `resolve_violation_api_v1_compliance_violations__violation_id__resolve_put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `violation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/compliance/violations/{violation_id}/resolve`

**Summary**: Resolve violation

**Operation ID**: `resolve_violation_api_v1_compliance_violations__violation_id__resolve_put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `violation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Compliance Validation (10 endpoints)

### 🔵 `GET /api/v1/projects/{project_id}/compliance/history`

**Summary**: Get compliance score history

**Operation ID**: `get_compliance_history_api_v1_projects__project_id__compliance_history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/compliance/history`

**Summary**: Get compliance score history

**Operation ID**: `get_compliance_history_api_v1_projects__project_id__compliance_history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/compliance/last-check`

**Summary**: Get last folder collision check

**Operation ID**: `get_last_collision_check_api_v1_projects__project_id__compliance_last_check_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Last Collision Check Api V1 Projects  Project Id  Compliance Last Check Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/compliance/last-check`

**Summary**: Get last folder collision check

**Operation ID**: `get_last_collision_check_api_v1_projects__project_id__compliance_last_check_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Last Collision Check Api V1 Projects  Project Id  Compliance Last Check Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/compliance/score`

**Summary**: Get quick compliance score

**Operation ID**: `get_quick_score_api_v1_projects__project_id__compliance_score_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/compliance/score`

**Summary**: Get quick compliance score

**Operation ID**: `get_quick_score_api_v1_projects__project_id__compliance_score_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/validate/compliance`

**Summary**: Calculate compliance score

**Operation ID**: `validate_compliance_api_v1_projects__project_id__validate_compliance_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/validate/compliance`

**Summary**: Calculate compliance score

**Operation ID**: `validate_compliance_api_v1_projects__project_id__validate_compliance_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/validate/duplicates`

**Summary**: Detect duplicate stage folders

**Operation ID**: `validate_duplicates_api_v1_projects__project_id__validate_duplicates_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/validate/duplicates`

**Summary**: Detect duplicate stage folders

**Operation ID**: `validate_duplicates_api_v1_projects__project_id__validate_duplicates_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Context Authority (7 endpoints)

### 🔵 `GET /api/v1/context-authority/adrs`

**Summary**: [DEPRECATED] List all ADRs

**Operation ID**: `list_adrs_api_v1_context_authority_adrs_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `status_filter` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/adrs/{adr_id}`

**Summary**: [DEPRECATED] Get specific ADR

**Operation ID**: `get_adr_api_v1_context_authority_adrs__adr_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `adr_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/agents-md`

**Summary**: [DEPRECATED] Get AGENTS.md status

**Operation ID**: `get_agents_md_status_api_v1_context_authority_agents_md_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `repo_path` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-authority/check-adr-linkage`

**Summary**: [DEPRECATED] Check ADR linkage for modules

**Operation ID**: `check_adr_linkage_api_v1_context_authority_check_adr_linkage_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-authority/check-spec`

**Summary**: [DEPRECATED] Check design spec existence

**Operation ID**: `check_spec_api_v1_context_authority_check_spec_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/health`

**Summary**: [DEPRECATED] Context authority health check

**Operation ID**: `context_authority_health_api_v1_context_authority_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Context Authority Health Api V1 Context Authority Health Get`

---

### 🟢 `POST /api/v1/context-authority/validate`

**Summary**: [DEPRECATED] Validate code context linkage

**Operation ID**: `validate_context_api_v1_context_authority_validate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Context Authority V1 (DEPRECATED) (7 endpoints)

### 🔵 `GET /api/v1/context-authority/adrs`

**Summary**: [DEPRECATED] List all ADRs

**Operation ID**: `list_adrs_api_v1_context_authority_adrs_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `status_filter` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/adrs/{adr_id}`

**Summary**: [DEPRECATED] Get specific ADR

**Operation ID**: `get_adr_api_v1_context_authority_adrs__adr_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `adr_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/agents-md`

**Summary**: [DEPRECATED] Get AGENTS.md status

**Operation ID**: `get_agents_md_status_api_v1_context_authority_agents_md_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `repo_path` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-authority/check-adr-linkage`

**Summary**: [DEPRECATED] Check ADR linkage for modules

**Operation ID**: `check_adr_linkage_api_v1_context_authority_check_adr_linkage_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-authority/check-spec`

**Summary**: [DEPRECATED] Check design spec existence

**Operation ID**: `check_spec_api_v1_context_authority_check_spec_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/health`

**Summary**: [DEPRECATED] Context authority health check

**Operation ID**: `context_authority_health_api_v1_context_authority_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Context Authority Health Api V1 Context Authority Health Get`

---

### 🟢 `POST /api/v1/context-authority/validate`

**Summary**: [DEPRECATED] Validate code context linkage

**Operation ID**: `validate_context_api_v1_context_authority_validate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Context Authority V2 (22 endpoints)

### 🔵 `GET /api/v1/context-authority/v2/health`

**Summary**: Health check

**Operation ID**: `health_check_api_v1_context_authority_v2_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/health`

**Summary**: Health check

**Operation ID**: `health_check_api_v1_context_authority_v2_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-authority/v2/overlay`

**Summary**: Generate dynamic overlay

**Operation ID**: `generate_overlay_api_v1_context_authority_v2_overlay_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-authority/v2/overlay`

**Summary**: Generate dynamic overlay

**Operation ID**: `generate_overlay_api_v1_context_authority_v2_overlay_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/snapshot/{submission_id}`

**Summary**: Get context snapshot

**Operation ID**: `get_snapshot_api_v1_context_authority_v2_snapshot__submission_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `submission_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/snapshot/{submission_id}`

**Summary**: Get context snapshot

**Operation ID**: `get_snapshot_api_v1_context_authority_v2_snapshot__submission_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `submission_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/snapshots/{project_id}`

**Summary**: List project snapshots

**Operation ID**: `list_project_snapshots_api_v1_context_authority_v2_snapshots__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `valid_only` | query | boolean | ❌ |
| `zone` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/snapshots/{project_id}`

**Summary**: List project snapshots

**Operation ID**: `list_project_snapshots_api_v1_context_authority_v2_snapshots__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `valid_only` | query | boolean | ❌ |
| `zone` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/stats`

**Summary**: Get statistics

**Operation ID**: `get_stats_api_v1_context_authority_v2_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/stats`

**Summary**: Get statistics

**Operation ID**: `get_stats_api_v1_context_authority_v2_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/templates`

**Summary**: List overlay templates

**Operation ID**: `list_templates_api_v1_context_authority_v2_templates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `trigger_type` | query | string | ❌ |
| `tier` | query | string | ❌ |
| `active_only` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/templates`

**Summary**: List overlay templates

**Operation ID**: `list_templates_api_v1_context_authority_v2_templates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `trigger_type` | query | string | ❌ |
| `tier` | query | string | ❌ |
| `active_only` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-authority/v2/templates`

**Summary**: Create overlay template

**Operation ID**: `create_template_api_v1_context_authority_v2_templates_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-authority/v2/templates`

**Summary**: Create overlay template

**Operation ID**: `create_template_api_v1_context_authority_v2_templates_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/templates/{template_id}`

**Summary**: Get template by ID

**Operation ID**: `get_template_api_v1_context_authority_v2_templates__template_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/templates/{template_id}`

**Summary**: Get template by ID

**Operation ID**: `get_template_api_v1_context_authority_v2_templates__template_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/context-authority/v2/templates/{template_id}`

**Summary**: Update template

**Operation ID**: `update_template_api_v1_context_authority_v2_templates__template_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/context-authority/v2/templates/{template_id}`

**Summary**: Update template

**Operation ID**: `update_template_api_v1_context_authority_v2_templates__template_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/templates/{template_id}/usage`

**Summary**: Get template usage statistics

**Operation ID**: `get_template_usage_api_v1_context_authority_v2_templates__template_id__usage_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `days` | query | integer | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-authority/v2/templates/{template_id}/usage`

**Summary**: Get template usage statistics

**Operation ID**: `get_template_usage_api_v1_context_authority_v2_templates__template_id__usage_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `days` | query | integer | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-authority/v2/validate`

**Summary**: Gate-aware context validation

**Operation ID**: `validate_context_api_v1_context_authority_v2_validate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-authority/v2/validate`

**Summary**: Gate-aware context validation

**Operation ID**: `validate_context_api_v1_context_authority_v2_validate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Context Overlay (2 endpoints)

### 🔵 `GET /api/v1/agents-md/context/{project_id}`

**Summary**: Get context overlay

**Operation ID**: `get_context_overlay_api_v1_agents_md_context__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `format` | query | string | ❌ |
| `trigger_type` | query | string | ❌ |
| `trigger_ref` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agents-md/context/{project_id}/history`

**Summary**: Get context overlay history

**Operation ID**: `get_context_history_api_v1_agents_md_context__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Context History Api V1 Agents Md Context  Project Id  History Get`
- **422**: Validation Error
  - Schema: `object`

---

## Context Validation (8 endpoints)

### 🔵 `GET /api/v1/context-validation/health`

**Summary**: Health check

**Operation ID**: `health_check_api_v1_context_validation_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Context Validation Health Get`

---

### 🔵 `GET /api/v1/context-validation/health`

**Summary**: Health check

**Operation ID**: `health_check_api_v1_context_validation_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Context Validation Health Get`

---

### 🔵 `GET /api/v1/context-validation/limits`

**Summary**: Get context limits configuration

**Operation ID**: `get_limits_api_v1_context_validation_limits_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/context-validation/limits`

**Summary**: Get context limits configuration

**Operation ID**: `get_limits_api_v1_context_validation_limits_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-validation/validate`

**Summary**: Validate AGENTS.md context limits

**Operation ID**: `validate_content_api_v1_context_validation_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-validation/validate`

**Summary**: Validate AGENTS.md context limits

**Operation ID**: `validate_content_api_v1_context_validation_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-validation/validate-github`

**Summary**: Validate AGENTS.md from GitHub repository

**Operation ID**: `validate_github_api_v1_context_validation_validate_github_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/context-validation/validate-github`

**Summary**: Validate AGENTS.md from GitHub repository

**Operation ID**: `validate_github_api_v1_context_validation_validate_github_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Contract Lock (14 endpoints)

### 🟢 `POST /api/v1/onboarding/{session_id}/force-unlock`

**Summary**: Force unlock (admin)

**Operation ID**: `force_unlock_api_v1_onboarding__session_id__force_unlock_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `reason` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/onboarding/{session_id}/force-unlock`

**Summary**: Force unlock (admin)

**Operation ID**: `force_unlock_api_v1_onboarding__session_id__force_unlock_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `reason` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/onboarding/{session_id}/lock`

**Summary**: Lock specification

**Operation ID**: `lock_specification_api_v1_onboarding__session_id__lock_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/onboarding/{session_id}/lock`

**Summary**: Lock specification

**Operation ID**: `lock_specification_api_v1_onboarding__session_id__lock_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/onboarding/{session_id}/lock-audit`

**Summary**: Get lock audit log

**Operation ID**: `get_lock_audit_api_v1_onboarding__session_id__lock_audit_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/onboarding/{session_id}/lock-audit`

**Summary**: Get lock audit log

**Operation ID**: `get_lock_audit_api_v1_onboarding__session_id__lock_audit_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/onboarding/{session_id}/lock-status`

**Summary**: Get lock status

**Operation ID**: `get_lock_status_api_v1_onboarding__session_id__lock_status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/onboarding/{session_id}/lock-status`

**Summary**: Get lock status

**Operation ID**: `get_lock_status_api_v1_onboarding__session_id__lock_status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/onboarding/{session_id}/status`

**Summary**: Get full session status

**Operation ID**: `get_session_status_api_v1_onboarding__session_id__status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/onboarding/{session_id}/status`

**Summary**: Get full session status

**Operation ID**: `get_session_status_api_v1_onboarding__session_id__status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/onboarding/{session_id}/unlock`

**Summary**: Unlock specification

**Operation ID**: `unlock_specification_api_v1_onboarding__session_id__unlock_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/onboarding/{session_id}/unlock`

**Summary**: Unlock specification

**Operation ID**: `unlock_specification_api_v1_onboarding__session_id__unlock_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/onboarding/{session_id}/verify-hash`

**Summary**: Verify spec hash

**Operation ID**: `verify_hash_api_v1_onboarding__session_id__verify_hash_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/onboarding/{session_id}/verify-hash`

**Summary**: Verify spec hash

**Operation ID**: `verify_hash_api_v1_onboarding__session_id__verify_hash_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Cross-Reference (8 endpoints)

### 🔵 `GET /api/v1/cross-reference/coverage/{project_id}`

**Summary**: Get Coverage

**Operation ID**: `get_coverage_api_v1_cross_reference_coverage__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `stage_03_path` | query | string | ❌ |
| `stage_05_path` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/cross-reference/coverage/{project_id}`

**Summary**: Get Coverage

**Operation ID**: `get_coverage_api_v1_cross_reference_coverage__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `stage_03_path` | query | string | ❌ |
| `stage_05_path` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/cross-reference/missing-tests/{project_id}`

**Summary**: Get Missing Tests

**Operation ID**: `get_missing_tests_api_v1_cross_reference_missing_tests__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `stage_03_path` | query | string | ❌ |
| `stage_05_path` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Missing Tests Api V1 Cross Reference Missing Tests  Project Id  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/cross-reference/missing-tests/{project_id}`

**Summary**: Get Missing Tests

**Operation ID**: `get_missing_tests_api_v1_cross_reference_missing_tests__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `stage_03_path` | query | string | ❌ |
| `stage_05_path` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Missing Tests Api V1 Cross Reference Missing Tests  Project Id  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/cross-reference/ssot-check/{project_id}`

**Summary**: Check Ssot Compliance

**Operation ID**: `check_ssot_compliance_api_v1_cross_reference_ssot_check__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Check Ssot Compliance Api V1 Cross Reference Ssot Check  Project Id  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/cross-reference/ssot-check/{project_id}`

**Summary**: Check Ssot Compliance

**Operation ID**: `check_ssot_compliance_api_v1_cross_reference_ssot_check__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Check Ssot Compliance Api V1 Cross Reference Ssot Check  Project Id  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/cross-reference/validate`

**Summary**: Validate Cross Reference

**Operation ID**: `validate_cross_reference_api_v1_cross_reference_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/cross-reference/validate`

**Summary**: Validate Cross Reference

**Operation ID**: `validate_cross_reference_api_v1_cross_reference_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Cross-Reference Validation (4 endpoints)

### 🔵 `GET /api/v1/doc-cross-reference/links`

**Summary**: Get document links

**Operation ID**: `get_document_links_api_v1_doc_cross_reference_links_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `document_path` | query | string | ✅ |
| `project_path` | query | string | ❌ |
| `direction` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/doc-cross-reference/orphaned`

**Summary**: Get orphaned documents

**Operation ID**: `get_orphaned_documents_api_v1_doc_cross_reference_orphaned_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `project_path` | query | string | ❌ |
| `document_type` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/doc-cross-reference/validate`

**Summary**: Validate single document

**Operation ID**: `validate_document_api_v1_doc_cross_reference_validate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/doc-cross-reference/validate-project`

**Summary**: Validate entire project

**Operation ID**: `validate_project_api_v1_doc_cross_reference_validate_project_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Dashboard (2 endpoints)

### 🔵 `GET /api/v1/dashboard/recent-gates`

**Summary**: Get Recent Gates

**Operation ID**: `get_recent_gates_api_v1_dashboard_recent_gates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dashboard/stats`

**Summary**: Get Dashboard Stats

**Operation ID**: `get_dashboard_stats_api_v1_dashboard_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Dependencies (10 endpoints)

### 🟢 `POST /api/v1/planning/dependencies`

**Summary**: Create sprint dependency

**Operation ID**: `create_sprint_dependency_api_v1_planning_dependencies_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies/bulk/resolve`

**Summary**: Bulk resolve dependencies

**Operation ID**: `bulk_resolve_dependencies_api_v1_planning_dependencies_bulk_resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/dependencies/check-circular`

**Summary**: Check for circular dependency

**Operation ID**: `check_circular_dependency_api_v1_planning_dependencies_check_circular_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `source_sprint_id` | query | string | ✅ |
| `target_sprint_id` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Check Circular Dependency Api V1 Planning Dependencies Check Circular Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Delete a sprint dependency

**Operation ID**: `delete_sprint_dependency_api_v1_planning_dependencies__dependency_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Get a sprint dependency

**Operation ID**: `get_sprint_dependency_api_v1_planning_dependencies__dependency_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Update a sprint dependency

**Operation ID**: `update_sprint_dependency_api_v1_planning_dependencies__dependency_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies/{dependency_id}/resolve`

**Summary**: Resolve a sprint dependency

**Operation ID**: `resolve_sprint_dependency_api_v1_planning_dependencies__dependency_id__resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/dependency-analysis`

**Summary**: Analyze project dependencies

**Operation ID**: `analyze_project_dependencies_api_v1_planning_projects__project_id__dependency_analysis_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/dependency-graph`

**Summary**: Get dependency graph for a project

**Operation ID**: `get_project_dependency_graph_api_v1_planning_projects__project_id__dependency_graph_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `include_cross_project` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/dependencies`

**Summary**: List dependencies for a sprint

**Operation ID**: `list_sprint_dependencies_api_v1_planning_sprints__sprint_id__dependencies_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `direction` | query | string | ❌ |
| `include_resolved` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Deprecation Monitoring (8 endpoints)

### 🔵 `GET /api/v1/deprecation/dashboard`

**Summary**: Get Deprecation Dashboard

**Operation ID**: `get_deprecation_dashboard_api_v1_deprecation_dashboard_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/deprecation/dashboard`

**Summary**: Get Deprecation Dashboard

**Operation ID**: `get_deprecation_dashboard_api_v1_deprecation_dashboard_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/deprecation/endpoints`

**Summary**: Get Deprecated Endpoints

**Operation ID**: `get_deprecated_endpoints_api_v1_deprecation_endpoints_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `category` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Deprecated Endpoints Api V1 Deprecation Endpoints Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/deprecation/endpoints`

**Summary**: Get Deprecated Endpoints

**Operation ID**: `get_deprecated_endpoints_api_v1_deprecation_endpoints_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `category` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Deprecated Endpoints Api V1 Deprecation Endpoints Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/deprecation/summary`

**Summary**: Get Deprecation Summary

**Operation ID**: `get_deprecation_summary_api_v1_deprecation_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/deprecation/summary`

**Summary**: Get Deprecation Summary

**Operation ID**: `get_deprecation_summary_api_v1_deprecation_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/deprecation/timeline`

**Summary**: Get Deprecation Timeline

**Operation ID**: `get_deprecation_timeline_api_v1_deprecation_timeline_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Deprecation Timeline Api V1 Deprecation Timeline Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/deprecation/timeline`

**Summary**: Get Deprecation Timeline

**Operation ID**: `get_deprecation_timeline_api_v1_deprecation_timeline_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Deprecation Timeline Api V1 Deprecation Timeline Get`
- **422**: Validation Error
  - Schema: `object`

---

## Documentation (4 endpoints)

### 🔵 `GET /api/v1/docs/user-support`

**Summary**: List User Support Docs

**Operation ID**: `list_user_support_docs_api_v1_docs_user_support_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response List User Support Docs Api V1 Docs User Support Get`

---

### 🔵 `GET /api/v1/docs/user-support`

**Summary**: List User Support Docs

**Operation ID**: `list_user_support_docs_api_v1_docs_user_support_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response List User Support Docs Api V1 Docs User Support Get`

---

### 🔵 `GET /api/v1/docs/user-support/{filename}`

**Summary**: Get User Support Doc

**Operation ID**: `get_user_support_doc_api_v1_docs_user_support__filename__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `filename` | path | string | ✅ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/docs/user-support/{filename}`

**Summary**: Get User Support Doc

**Operation ID**: `get_user_support_doc_api_v1_docs_user_support__filename__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `filename` | path | string | ✅ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

## Dogfooding (20 endpoints)

### 🔵 `GET /api/v1/dogfooding/ceo-time/entries`

**Summary**: List Ceo Time Entries

**Operation ID**: `list_ceo_time_entries_api_v1_dogfooding_ceo_time_entries_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `activity_type` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/dogfooding/ceo-time/record`

**Summary**: Record Ceo Time

**Operation ID**: `record_ceo_time_api_v1_dogfooding_ceo_time_record_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/ceo-time/summary`

**Summary**: Get Ceo Time Summary

**Operation ID**: `get_ceo_time_summary_api_v1_dogfooding_ceo_time_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/daily-checks`

**Summary**: Run Daily Checks

**Operation ID**: `run_daily_checks_api_v1_dogfooding_daily_checks_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/daily-checks/history`

**Summary**: Get Daily Checks History

**Operation ID**: `get_daily_checks_history_api_v1_dogfooding_daily_checks_history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/dogfooding/enforce/soft`

**Summary**: Enforce Soft Mode

**Operation ID**: `enforce_soft_mode_api_v1_dogfooding_enforce_soft_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/enforce/soft/log`

**Summary**: Get Soft Enforcement Log

**Operation ID**: `get_soft_enforcement_log_api_v1_dogfooding_enforce_soft_log_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `action_filter` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/dogfooding/enforce/soft/override`

**Summary**: Request Cto Override

**Operation ID**: `request_cto_override_api_v1_dogfooding_enforce_soft_override_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `pr_number` | query | integer | ✅ |
| `reason` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/enforce/soft/status`

**Summary**: Get Soft Mode Status

**Operation ID**: `get_soft_mode_status_api_v1_dogfooding_enforce_soft_status_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/export/json`

**Summary**: Export Json Metrics

**Operation ID**: `export_json_metrics_api_v1_dogfooding_export_json_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/export/prometheus`

**Summary**: Export Prometheus Metrics

**Operation ID**: `export_prometheus_metrics_api_v1_dogfooding_export_prometheus_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🟢 `POST /api/v1/dogfooding/feedback`

**Summary**: Submit Developer Feedback

**Operation ID**: `submit_developer_feedback_api_v1_dogfooding_feedback_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/feedback/list`

**Summary**: List Developer Feedback

**Operation ID**: `list_developer_feedback_api_v1_dogfooding_feedback_list_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/feedback/summary`

**Summary**: Get Feedback Summary

**Operation ID**: `get_feedback_summary_api_v1_dogfooding_feedback_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/go-no-go`

**Summary**: Get Go No Go Decision

**Operation ID**: `get_go_no_go_decision_api_v1_dogfooding_go_no_go_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/metrics`

**Summary**: Get Dogfooding Metrics

**Operation ID**: `get_dogfooding_metrics_api_v1_dogfooding_metrics_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/prs`

**Summary**: Get Pr Metrics

**Operation ID**: `get_pr_metrics_api_v1_dogfooding_prs_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/dogfooding/prs/record`

**Summary**: Record Pr Metric

**Operation ID**: `record_pr_metric_api_v1_dogfooding_prs_record_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/dogfooding/report-false-positive`

**Summary**: Report False Positive

**Operation ID**: `report_false_positive_api_v1_dogfooding_report_false_positive_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `pr_number` | query | integer | ✅ |
| `reason` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/status`

**Summary**: Get Dogfooding Status

**Operation ID**: `get_dogfooding_status_api_v1_dogfooding_status_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

## E2E Testing (10 endpoints)

### 🟢 `POST /api/v1/e2e/cancel/{execution_id}`

**Summary**: Cancel Execution

**Operation ID**: `cancel_execution_api_v1_e2e_cancel__execution_id__post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `execution_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Cancel Execution Api V1 E2E Cancel  Execution Id  Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/e2e/cancel/{execution_id}`

**Summary**: Cancel Execution

**Operation ID**: `cancel_execution_api_v1_e2e_cancel__execution_id__post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `execution_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Cancel Execution Api V1 E2E Cancel  Execution Id  Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/e2e/execute`

**Summary**: Execute E2E Tests

**Operation ID**: `execute_e2e_tests_api_v1_e2e_execute_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/e2e/execute`

**Summary**: Execute E2E Tests

**Operation ID**: `execute_e2e_tests_api_v1_e2e_execute_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/e2e/history`

**Summary**: Get Execution History

**Operation ID**: `get_execution_history_api_v1_e2e_history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Execution History Api V1 E2E History Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/e2e/history`

**Summary**: Get Execution History

**Operation ID**: `get_execution_history_api_v1_e2e_history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Execution History Api V1 E2E History Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/e2e/results/{execution_id}`

**Summary**: Get Test Results

**Operation ID**: `get_test_results_api_v1_e2e_results__execution_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `execution_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/e2e/results/{execution_id}`

**Summary**: Get Test Results

**Operation ID**: `get_test_results_api_v1_e2e_results__execution_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `execution_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/e2e/status/{execution_id}`

**Summary**: Get Execution Status

**Operation ID**: `get_execution_status_api_v1_e2e_status__execution_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `execution_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/e2e/status/{execution_id}`

**Summary**: Get Execution Status

**Operation ID**: `get_execution_status_api_v1_e2e_status__execution_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `execution_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Evidence (3 endpoints)

### 🔵 `GET /api/v1/projects/{project_id}/evidence/gaps`

**Summary**: Get Evidence Gaps

**Operation ID**: `get_evidence_gaps_api_v1_projects__project_id__evidence_gaps_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | integer | ✅ |
| `interface` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Evidence Gaps Api V1 Projects  Project Id  Evidence Gaps Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/evidence/status`

**Summary**: Get Evidence Status

**Operation ID**: `get_evidence_status_api_v1_projects__project_id__evidence_status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | integer | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Evidence Status Api V1 Projects  Project Id  Evidence Status Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/evidence/validate`

**Summary**: Trigger Evidence Validation

**Operation ID**: `trigger_evidence_validation_api_v1_projects__project_id__evidence_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | integer | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Trigger Evidence Validation Api V1 Projects  Project Id  Evidence Validate Post`
- **422**: Validation Error
  - Schema: `object`

---

## Evidence Manifest (7 endpoints)

### 🔵 `GET /api/v1/evidence-manifests`

**Summary**: List evidence manifests

**Operation ID**: `list_manifests_api_v1_evidence_manifests_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/evidence-manifests`

**Summary**: Create evidence manifest

**Operation ID**: `create_manifest_api_v1_evidence_manifests_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/evidence-manifests/latest`

**Summary**: Get latest manifest

**Operation ID**: `get_latest_manifest_api_v1_evidence_manifests_latest_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Latest Manifest Api V1 Evidence Manifests Latest Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/evidence-manifests/status`

**Summary**: Get chain status

**Operation ID**: `get_chain_status_api_v1_evidence_manifests_status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/evidence-manifests/verifications`

**Summary**: Get verification history

**Operation ID**: `get_verification_history_api_v1_evidence_manifests_verifications_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/evidence-manifests/verify`

**Summary**: Verify hash chain

**Operation ID**: `verify_chain_api_v1_evidence_manifests_verify_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/evidence-manifests/{manifest_id}`

**Summary**: Get manifest by ID

**Operation ID**: `get_manifest_api_v1_evidence_manifests__manifest_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `manifest_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Evidence Timeline (7 endpoints)

### 🔵 `GET /api/v1/projects/{project_id}/timeline`

**Summary**: List evidence timeline events

**Operation ID**: `list_timeline_events_api_v1_projects__project_id__timeline_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `limit` | query | integer | ❌ |
| `date_start` | query | string | ❌ |
| `date_end` | query | string | ❌ |
| `ai_tool` | query | string | ❌ |
| `validation_status` | query | string | ❌ |
| `search` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/timeline/export`

**Summary**: Export evidence data

**Operation ID**: `export_timeline_api_v1_projects__project_id__timeline_export_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `format` | query | string | ❌ |
| `date_start` | query | string | ❌ |
| `date_end` | query | string | ❌ |
| `include_details` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/timeline/stats`

**Summary**: Get timeline statistics

**Operation ID**: `get_timeline_stats_api_v1_projects__project_id__timeline_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/timeline/{event_id}`

**Summary**: Get event detail

**Operation ID**: `get_event_detail_api_v1_projects__project_id__timeline__event_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `event_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/timeline/{event_id}/override/approve`

**Summary**: Approve override

**Operation ID**: `approve_override_api_v1_timeline__event_id__override_approve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `event_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/timeline/{event_id}/override/reject`

**Summary**: Reject override

**Operation ID**: `reject_override_api_v1_timeline__event_id__override_reject_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `event_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/timeline/{event_id}/override/request`

**Summary**: Request override

**Operation ID**: `request_override_api_v1_timeline__event_id__override_request_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `event_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Feedback (14 endpoints)

### 🔵 `GET /api/v1/feedback`

**Summary**: List Feedback

**Operation ID**: `list_feedback_api_v1_feedback_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `type` | query | string | ❌ |
| `status` | query | string | ❌ |
| `priority` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/feedback`

**Summary**: List Feedback

**Operation ID**: `list_feedback_api_v1_feedback_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `type` | query | string | ❌ |
| `status` | query | string | ❌ |
| `priority` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/feedback`

**Summary**: Create Feedback

**Operation ID**: `create_feedback_api_v1_feedback_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/feedback`

**Summary**: Create Feedback

**Operation ID**: `create_feedback_api_v1_feedback_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/feedback/stats`

**Summary**: Get Feedback Stats

**Operation ID**: `get_feedback_stats_api_v1_feedback_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/feedback/stats`

**Summary**: Get Feedback Stats

**Operation ID**: `get_feedback_stats_api_v1_feedback_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/feedback/{feedback_id}`

**Summary**: Get Feedback

**Operation ID**: `get_feedback_api_v1_feedback__feedback_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/feedback/{feedback_id}`

**Summary**: Get Feedback

**Operation ID**: `get_feedback_api_v1_feedback__feedback_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/feedback/{feedback_id}`

**Summary**: Update Feedback

**Operation ID**: `update_feedback_api_v1_feedback__feedback_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/feedback/{feedback_id}`

**Summary**: Update Feedback

**Operation ID**: `update_feedback_api_v1_feedback__feedback_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/feedback/{feedback_id}/comments`

**Summary**: List Comments

**Operation ID**: `list_comments_api_v1_feedback__feedback_id__comments_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Comments Api V1 Feedback  Feedback Id  Comments Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/feedback/{feedback_id}/comments`

**Summary**: List Comments

**Operation ID**: `list_comments_api_v1_feedback__feedback_id__comments_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Comments Api V1 Feedback  Feedback Id  Comments Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/feedback/{feedback_id}/comments`

**Summary**: Add Comment

**Operation ID**: `add_comment_api_v1_feedback__feedback_id__comments_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/feedback/{feedback_id}/comments`

**Summary**: Add Comment

**Operation ID**: `add_comment_api_v1_feedback__feedback_id__comments_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Feedback Learning (22 endpoints)

### 🔵 `GET /api/v1/learnings/projects/{project_id}/aggregations`

**Summary**: List aggregations

**Operation ID**: `list_aggregations_api_v1_learnings_projects__project_id__aggregations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/aggregations`

**Summary**: Create aggregation

**Operation ID**: `create_aggregation_api_v1_learnings_projects__project_id__aggregations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}`

**Summary**: Get aggregation

**Operation ID**: `get_aggregation_api_v1_learnings_projects__project_id__aggregations__aggregation_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `aggregation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}/apply`

**Summary**: Apply aggregation suggestions

**Operation ID**: `apply_aggregation_api_v1_learnings_projects__project_id__aggregations__aggregation_id__apply_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `aggregation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}/reject`

**Summary**: Reject aggregation suggestions

**Operation ID**: `reject_aggregation_api_v1_learnings_projects__project_id__aggregations__aggregation_id__reject_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `aggregation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/generate-hints`

**Summary**: Generate hints from learnings

**Operation ID**: `generate_hints_from_learnings_api_v1_learnings_projects__project_id__generate_hints_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `since` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Generate Hints From Learnings Api V1 Learnings Projects  Project Id  Generate Hints Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/hints`

**Summary**: List hints

**Operation ID**: `list_hints_api_v1_learnings_projects__project_id__hints_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `hint_type` | query | string | ❌ |
| `category` | query | string | ❌ |
| `status` | query | string | ❌ |
| `ai_generated` | query | string | ❌ |
| `human_verified` | query | string | ❌ |
| `min_confidence` | query | string | ❌ |
| `min_effectiveness` | query | string | ❌ |
| `applies_to` | query | string | ❌ |
| `language` | query | string | ❌ |
| `framework` | query | string | ❌ |
| `search` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/hints`

**Summary**: Create a hint

**Operation ID**: `create_hint_api_v1_learnings_projects__project_id__hints_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/hints/active`

**Summary**: Get active hints for decomposition

**Operation ID**: `get_active_hints_api_v1_learnings_projects__project_id__hints_active_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `applies_to` | query | string | ❌ |
| `language` | query | string | ❌ |
| `framework` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Active Hints Api V1 Learnings Projects  Project Id  Hints Active Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/hints/stats`

**Summary**: Get hint statistics

**Operation ID**: `get_hint_stats_api_v1_learnings_projects__project_id__hints_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/hints/usage`

**Summary**: Record hint usage

**Operation ID**: `record_hint_usage_api_v1_learnings_projects__project_id__hints_usage_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/hints/usage/{usage_id}/feedback`

**Summary**: Provide hint usage feedback

**Operation ID**: `provide_hint_feedback_api_v1_learnings_projects__project_id__hints_usage__usage_id__feedback_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `usage_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/hints/{hint_id}`

**Summary**: Get a hint

**Operation ID**: `get_hint_api_v1_learnings_projects__project_id__hints__hint_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `hint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/learnings/projects/{project_id}/hints/{hint_id}`

**Summary**: Update a hint

**Operation ID**: `update_hint_api_v1_learnings_projects__project_id__hints__hint_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `hint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/hints/{hint_id}/verify`

**Summary**: Verify a hint

**Operation ID**: `verify_hint_api_v1_learnings_projects__project_id__hints__hint_id__verify_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `hint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/learnings`

**Summary**: List learnings

**Operation ID**: `list_learnings_api_v1_learnings_projects__project_id__learnings_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `feedback_type` | query | string | ❌ |
| `severity` | query | string | ❌ |
| `status` | query | string | ❌ |
| `ai_extracted` | query | string | ❌ |
| `applied_to_claude_md` | query | string | ❌ |
| `applied_to_decomposition` | query | string | ❌ |
| `pr_number` | query | string | ❌ |
| `from_date` | query | string | ❌ |
| `to_date` | query | string | ❌ |
| `search` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/learnings`

**Summary**: Create a learning manually

**Operation ID**: `create_learning_api_v1_learnings_projects__project_id__learnings_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/learnings/bulk-status`

**Summary**: Bulk update learning status

**Operation ID**: `bulk_update_learning_status_api_v1_learnings_projects__project_id__learnings_bulk_status_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Bulk Update Learning Status Api V1 Learnings Projects  Project Id  Learnings Bulk Status Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/learnings/extract`

**Summary**: Extract learning from PR comment

**Operation ID**: `extract_learning_api_v1_learnings_projects__project_id__learnings_extract_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `use_ai` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/learnings/stats`

**Summary**: Get learning statistics

**Operation ID**: `get_learning_stats_api_v1_learnings_projects__project_id__learnings_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `from_date` | query | string | ❌ |
| `to_date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/learnings/{learning_id}`

**Summary**: Get a learning

**Operation ID**: `get_learning_api_v1_learnings_projects__project_id__learnings__learning_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `learning_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/learnings/projects/{project_id}/learnings/{learning_id}`

**Summary**: Update a learning

**Operation ID**: `update_learning_api_v1_learnings_projects__project_id__learnings__learning_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `learning_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Feedback Learning (EP-11) (22 endpoints)

### 🔵 `GET /api/v1/learnings/projects/{project_id}/aggregations`

**Summary**: List aggregations

**Operation ID**: `list_aggregations_api_v1_learnings_projects__project_id__aggregations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/aggregations`

**Summary**: Create aggregation

**Operation ID**: `create_aggregation_api_v1_learnings_projects__project_id__aggregations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}`

**Summary**: Get aggregation

**Operation ID**: `get_aggregation_api_v1_learnings_projects__project_id__aggregations__aggregation_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `aggregation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}/apply`

**Summary**: Apply aggregation suggestions

**Operation ID**: `apply_aggregation_api_v1_learnings_projects__project_id__aggregations__aggregation_id__apply_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `aggregation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}/reject`

**Summary**: Reject aggregation suggestions

**Operation ID**: `reject_aggregation_api_v1_learnings_projects__project_id__aggregations__aggregation_id__reject_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `aggregation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/generate-hints`

**Summary**: Generate hints from learnings

**Operation ID**: `generate_hints_from_learnings_api_v1_learnings_projects__project_id__generate_hints_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `since` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Generate Hints From Learnings Api V1 Learnings Projects  Project Id  Generate Hints Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/hints`

**Summary**: List hints

**Operation ID**: `list_hints_api_v1_learnings_projects__project_id__hints_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `hint_type` | query | string | ❌ |
| `category` | query | string | ❌ |
| `status` | query | string | ❌ |
| `ai_generated` | query | string | ❌ |
| `human_verified` | query | string | ❌ |
| `min_confidence` | query | string | ❌ |
| `min_effectiveness` | query | string | ❌ |
| `applies_to` | query | string | ❌ |
| `language` | query | string | ❌ |
| `framework` | query | string | ❌ |
| `search` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/hints`

**Summary**: Create a hint

**Operation ID**: `create_hint_api_v1_learnings_projects__project_id__hints_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/hints/active`

**Summary**: Get active hints for decomposition

**Operation ID**: `get_active_hints_api_v1_learnings_projects__project_id__hints_active_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `applies_to` | query | string | ❌ |
| `language` | query | string | ❌ |
| `framework` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Active Hints Api V1 Learnings Projects  Project Id  Hints Active Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/hints/stats`

**Summary**: Get hint statistics

**Operation ID**: `get_hint_stats_api_v1_learnings_projects__project_id__hints_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/hints/usage`

**Summary**: Record hint usage

**Operation ID**: `record_hint_usage_api_v1_learnings_projects__project_id__hints_usage_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/hints/usage/{usage_id}/feedback`

**Summary**: Provide hint usage feedback

**Operation ID**: `provide_hint_feedback_api_v1_learnings_projects__project_id__hints_usage__usage_id__feedback_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `usage_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/hints/{hint_id}`

**Summary**: Get a hint

**Operation ID**: `get_hint_api_v1_learnings_projects__project_id__hints__hint_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `hint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/learnings/projects/{project_id}/hints/{hint_id}`

**Summary**: Update a hint

**Operation ID**: `update_hint_api_v1_learnings_projects__project_id__hints__hint_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `hint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/hints/{hint_id}/verify`

**Summary**: Verify a hint

**Operation ID**: `verify_hint_api_v1_learnings_projects__project_id__hints__hint_id__verify_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `hint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/learnings`

**Summary**: List learnings

**Operation ID**: `list_learnings_api_v1_learnings_projects__project_id__learnings_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `feedback_type` | query | string | ❌ |
| `severity` | query | string | ❌ |
| `status` | query | string | ❌ |
| `ai_extracted` | query | string | ❌ |
| `applied_to_claude_md` | query | string | ❌ |
| `applied_to_decomposition` | query | string | ❌ |
| `pr_number` | query | string | ❌ |
| `from_date` | query | string | ❌ |
| `to_date` | query | string | ❌ |
| `search` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/learnings`

**Summary**: Create a learning manually

**Operation ID**: `create_learning_api_v1_learnings_projects__project_id__learnings_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/learnings/bulk-status`

**Summary**: Bulk update learning status

**Operation ID**: `bulk_update_learning_status_api_v1_learnings_projects__project_id__learnings_bulk_status_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Bulk Update Learning Status Api V1 Learnings Projects  Project Id  Learnings Bulk Status Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/learnings/projects/{project_id}/learnings/extract`

**Summary**: Extract learning from PR comment

**Operation ID**: `extract_learning_api_v1_learnings_projects__project_id__learnings_extract_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `use_ai` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/learnings/stats`

**Summary**: Get learning statistics

**Operation ID**: `get_learning_stats_api_v1_learnings_projects__project_id__learnings_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `from_date` | query | string | ❌ |
| `to_date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/learnings/projects/{project_id}/learnings/{learning_id}`

**Summary**: Get a learning

**Operation ID**: `get_learning_api_v1_learnings_projects__project_id__learnings__learning_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `learning_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/learnings/projects/{project_id}/learnings/{learning_id}`

**Summary**: Update a learning

**Operation ID**: `update_learning_api_v1_learnings_projects__project_id__learnings__learning_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `learning_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Framework Version (12 endpoints)

### 🔵 `GET /api/v1/framework-version/health`

**Summary**: Health check

**Operation ID**: `health_check_api_v1_framework_version_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Framework Version Health Get`

---

### 🔵 `GET /api/v1/framework-version/health`

**Summary**: Health check

**Operation ID**: `health_check_api_v1_framework_version_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Framework Version Health Get`

---

### 🔵 `GET /api/v1/framework-version/{project_id}`

**Summary**: Get current Framework version

**Operation ID**: `get_current_version_api_v1_framework_version__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/framework-version/{project_id}`

**Summary**: Get current Framework version

**Operation ID**: `get_current_version_api_v1_framework_version__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/framework-version/{project_id}`

**Summary**: Record new Framework version

**Operation ID**: `record_version_api_v1_framework_version__project_id__post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/framework-version/{project_id}`

**Summary**: Record new Framework version

**Operation ID**: `record_version_api_v1_framework_version__project_id__post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/framework-version/{project_id}/compliance`

**Summary**: Get compliance summary

**Operation ID**: `get_compliance_summary_api_v1_framework_version__project_id__compliance_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/framework-version/{project_id}/compliance`

**Summary**: Get compliance summary

**Operation ID**: `get_compliance_summary_api_v1_framework_version__project_id__compliance_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/framework-version/{project_id}/drift`

**Summary**: Check version drift

**Operation ID**: `check_version_drift_api_v1_framework_version__project_id__drift_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `latest_version` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/framework-version/{project_id}/drift`

**Summary**: Check version drift

**Operation ID**: `check_version_drift_api_v1_framework_version__project_id__drift_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `latest_version` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/framework-version/{project_id}/history`

**Summary**: Get version history

**Operation ID**: `get_version_history_api_v1_framework_version__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/framework-version/{project_id}/history`

**Summary**: Get version history

**Operation ID**: `get_version_history_api_v1_framework_version__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Gates (24 endpoints)

### 🔵 `GET /api/v1/gates`

**Summary**: List Gates

**Operation ID**: `list_gates_api_v1_gates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `stage` | query | string | ❌ |
| `status` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates`

**Summary**: List Gates

**Operation ID**: `list_gates_api_v1_gates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `stage` | query | string | ❌ |
| `status` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates`

**Summary**: Create Gate

**Operation ID**: `create_gate_api_v1_gates_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates`

**Summary**: Create Gate

**Operation ID**: `create_gate_api_v1_gates_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/gates/{gate_id}`

**Summary**: Delete Gate

**Operation ID**: `delete_gate_api_v1_gates__gate_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/gates/{gate_id}`

**Summary**: Delete Gate

**Operation ID**: `delete_gate_api_v1_gates__gate_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates/{gate_id}`

**Summary**: Get Gate

**Operation ID**: `get_gate_api_v1_gates__gate_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates/{gate_id}`

**Summary**: Get Gate

**Operation ID**: `get_gate_api_v1_gates__gate_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/gates/{gate_id}`

**Summary**: Update Gate

**Operation ID**: `update_gate_api_v1_gates__gate_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/gates/{gate_id}`

**Summary**: Update Gate

**Operation ID**: `update_gate_api_v1_gates__gate_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates/{gate_id}/actions`

**Summary**: Get Gate Actions

**Operation ID**: `get_gate_actions_api_v1_gates__gate_id__actions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates/{gate_id}/actions`

**Summary**: Get Gate Actions

**Operation ID**: `get_gate_actions_api_v1_gates__gate_id__actions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates/{gate_id}/approvals`

**Summary**: Get Gate Approvals

**Operation ID**: `get_gate_approvals_api_v1_gates__gate_id__approvals_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Gate Approvals Api V1 Gates  Gate Id  Approvals Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates/{gate_id}/approvals`

**Summary**: Get Gate Approvals

**Operation ID**: `get_gate_approvals_api_v1_gates__gate_id__approvals_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Gate Approvals Api V1 Gates  Gate Id  Approvals Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates/{gate_id}/approve`

**Summary**: Approve Gate

**Operation ID**: `approve_gate_api_v1_gates__gate_id__approve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates/{gate_id}/approve`

**Summary**: Approve Gate

**Operation ID**: `approve_gate_api_v1_gates__gate_id__approve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates/{gate_id}/evaluate`

**Summary**: Evaluate Gate

**Operation ID**: `evaluate_gate_api_v1_gates__gate_id__evaluate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates/{gate_id}/evaluate`

**Summary**: Evaluate Gate

**Operation ID**: `evaluate_gate_api_v1_gates__gate_id__evaluate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates/{gate_id}/evidence`

**Summary**: Upload Evidence

**Operation ID**: `upload_evidence_api_v1_gates__gate_id__evidence_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates/{gate_id}/evidence`

**Summary**: Upload Evidence

**Operation ID**: `upload_evidence_api_v1_gates__gate_id__evidence_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates/{gate_id}/reject`

**Summary**: Reject Gate

**Operation ID**: `reject_gate_api_v1_gates__gate_id__reject_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates/{gate_id}/reject`

**Summary**: Reject Gate

**Operation ID**: `reject_gate_api_v1_gates__gate_id__reject_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates/{gate_id}/submit`

**Summary**: Submit Gate

**Operation ID**: `submit_gate_api_v1_gates__gate_id__submit_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates/{gate_id}/submit`

**Summary**: Submit Gate

**Operation ID**: `submit_gate_api_v1_gates__gate_id__submit_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Gates Engine (16 endpoints)

### 🟢 `POST /api/v1/gates-engine/bulk-evaluate`

**Summary**: Evaluate multiple gates

**Operation ID**: `bulk_evaluate_api_v1_gates_engine_bulk_evaluate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates-engine/bulk-evaluate`

**Summary**: Evaluate multiple gates

**Operation ID**: `bulk_evaluate_api_v1_gates_engine_bulk_evaluate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates-engine/evaluate-by-code`

**Summary**: Evaluate gate by project and code

**Operation ID**: `evaluate_by_code_api_v1_gates_engine_evaluate_by_code_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates-engine/evaluate-by-code`

**Summary**: Evaluate gate by project and code

**Operation ID**: `evaluate_by_code_api_v1_gates_engine_evaluate_by_code_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates-engine/evaluate/{gate_id}`

**Summary**: Evaluate single gate

**Operation ID**: `evaluate_gate_api_v1_gates_engine_evaluate__gate_id__post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/gates-engine/evaluate/{gate_id}`

**Summary**: Evaluate single gate

**Operation ID**: `evaluate_gate_api_v1_gates_engine_evaluate__gate_id__post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates-engine/health`

**Summary**: Gates engine health check

**Operation ID**: `health_check_api_v1_gates_engine_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates-engine/health`

**Summary**: Gates engine health check

**Operation ID**: `health_check_api_v1_gates_engine_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates-engine/policies/{gate_code}`

**Summary**: Get policies for gate

**Operation ID**: `get_policies_api_v1_gates_engine_policies__gate_code__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_code` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates-engine/policies/{gate_code}`

**Summary**: Get policies for gate

**Operation ID**: `get_policies_api_v1_gates_engine_policies__gate_code__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_code` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates-engine/prerequisites/{gate_code}`

**Summary**: Check gate prerequisites

**Operation ID**: `check_prerequisites_api_v1_gates_engine_prerequisites__gate_code__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_code` | path | string | ✅ |
| `project_id` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates-engine/prerequisites/{gate_code}`

**Summary**: Check gate prerequisites

**Operation ID**: `check_prerequisites_api_v1_gates_engine_prerequisites__gate_code__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_code` | path | string | ✅ |
| `project_id` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates-engine/readiness/{project_id}`

**Summary**: Get project gate readiness

**Operation ID**: `get_readiness_api_v1_gates_engine_readiness__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates-engine/readiness/{project_id}`

**Summary**: Get project gate readiness

**Operation ID**: `get_readiness_api_v1_gates_engine_readiness__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/gates-engine/stages`

**Summary**: Get gate-to-stage mapping

**Operation ID**: `get_stages_api_v1_gates_engine_stages_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Stages Api V1 Gates Engine Stages Get`

---

### 🔵 `GET /api/v1/gates-engine/stages`

**Summary**: Get gate-to-stage mapping

**Operation ID**: `get_stages_api_v1_gates_engine_stages_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Stages Api V1 Gates Engine Stages Get`

---

## GitHub (13 endpoints)

### 🔵 `GET /api/v1/api/v1/github/installations`

**Summary**: List user's GitHub installations

**Operation ID**: `list_installations_api_v1_api_v1_github_installations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/github/installations/{installation_id}/repositories`

**Summary**: List repositories for installation

**Operation ID**: `list_installation_repositories_api_v1_api_v1_github_installations__installation_id__repositories_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `installation_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `per_page` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/github/projects/{project_id}/clone`

**Summary**: Clone linked repository

**Operation ID**: `clone_repository_api_v1_api_v1_github_projects__project_id__clone_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/github/projects/{project_id}/link`

**Summary**: Link GitHub repository to project

**Operation ID**: `link_repository_api_v1_api_v1_github_projects__project_id__link_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/github/projects/{project_id}/repository`

**Summary**: Get linked repository for project

**Operation ID**: `get_project_repository_api_v1_api_v1_github_projects__project_id__repository_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/github/projects/{project_id}/scan`

**Summary**: Scan cloned repository

**Operation ID**: `scan_repository_api_v1_api_v1_github_projects__project_id__scan_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/api/v1/github/projects/{project_id}/unlink`

**Summary**: Unlink GitHub repository from project

**Operation ID**: `unlink_repository_api_v1_api_v1_github_projects__project_id__unlink_delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/github/webhooks`

**Summary**: GitHub webhook handler

**Operation ID**: `handle_webhook_api_v1_api_v1_github_webhooks_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `X-GitHub-Event` | header | string | ❌ |
| `X-Hub-Signature-256` | header | string | ❌ |
| `X-GitHub-Delivery` | header | string | ❌ |

**Responses**:

- **202**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/github/webhooks/dlq`

**Summary**: Get dead letter queue jobs

**Operation ID**: `get_dlq_jobs_api_v1_api_v1_github_webhooks_dlq_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/github/webhooks/dlq/{job_id}/retry`

**Summary**: Retry a dead letter queue job

**Operation ID**: `retry_dlq_job_api_v1_api_v1_github_webhooks_dlq__job_id__retry_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `job_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/github/webhooks/jobs/{job_id}`

**Summary**: Get webhook job status

**Operation ID**: `get_webhook_job_status_api_v1_api_v1_github_webhooks_jobs__job_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `job_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/github/webhooks/process`

**Summary**: Trigger webhook job processing

**Operation ID**: `trigger_webhook_processing_api_v1_api_v1_github_webhooks_process_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `max_jobs` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/github/webhooks/stats`

**Summary**: Get webhook job queue statistics

**Operation ID**: `get_webhook_stats_api_v1_api_v1_github_webhooks_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Governance Metrics (14 endpoints)

### 🔵 `GET /api/v1/governance-metrics`

**Summary**: Get Prometheus metrics

**Operation ID**: `get_metrics_api_v1_governance_metrics_get`

---

### 🔵 `GET /api/v1/governance-metrics/definitions`

**Summary**: Get metric definitions

**Operation ID**: `get_metric_definitions_api_v1_governance_metrics_definitions_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Metric Definitions Api V1 Governance Metrics Definitions Get`

---

### 🔵 `GET /api/v1/governance-metrics/health`

**Summary**: Metrics service health check

**Operation ID**: `metrics_health_api_v1_governance_metrics_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Metrics Health Api V1 Governance Metrics Health Get`

---

### 🔵 `GET /api/v1/governance-metrics/json`

**Summary**: Get metrics in JSON format

**Operation ID**: `get_metrics_json_api_v1_governance_metrics_json_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Metrics Json Api V1 Governance Metrics Json Get`

---

### 🟢 `POST /api/v1/governance-metrics/record-break-glass`

**Summary**: Record break glass activation

**Operation ID**: `record_break_glass_api_v1_governance_metrics_record_break_glass_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Record Break Glass Api V1 Governance Metrics Record Break Glass Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/governance-metrics/record-bypass`

**Summary**: Record governance bypass incident

**Operation ID**: `record_bypass_api_v1_governance_metrics_record_bypass_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Record Bypass Api V1 Governance Metrics Record Bypass Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/governance-metrics/record-ceo-override`

**Summary**: Record CEO override

**Operation ID**: `record_ceo_override_api_v1_governance_metrics_record_ceo_override_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Record Ceo Override Api V1 Governance Metrics Record Ceo Override Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/governance-metrics/record-developer-friction`

**Summary**: Record developer friction

**Operation ID**: `record_developer_friction_api_v1_governance_metrics_record_developer_friction_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Record Developer Friction Api V1 Governance Metrics Record Developer Friction Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/governance-metrics/record-evidence`

**Summary**: Record evidence upload

**Operation ID**: `record_evidence_api_v1_governance_metrics_record_evidence_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Record Evidence Api V1 Governance Metrics Record Evidence Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/governance-metrics/record-llm`

**Summary**: Record LLM generation metrics

**Operation ID**: `record_llm_api_v1_governance_metrics_record_llm_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Record Llm Api V1 Governance Metrics Record Llm Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/governance-metrics/record-submission`

**Summary**: Record governance submission metrics

**Operation ID**: `record_submission_api_v1_governance_metrics_record_submission_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Record Submission Api V1 Governance Metrics Record Submission Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/governance-metrics/set-kill-switch`

**Summary**: Set kill switch status

**Operation ID**: `set_kill_switch_api_v1_governance_metrics_set_kill_switch_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Set Kill Switch Api V1 Governance Metrics Set Kill Switch Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/governance-metrics/update-ceo-metrics`

**Summary**: Update CEO dashboard metrics

**Operation ID**: `update_ceo_metrics_api_v1_governance_metrics_update_ceo_metrics_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Update Ceo Metrics Api V1 Governance Metrics Update Ceo Metrics Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/governance-metrics/update-system-health`

**Summary**: Update system health metrics

**Operation ID**: `update_system_health_api_v1_governance_metrics_update_system_health_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Update System Health Api V1 Governance Metrics Update System Health Post`
- **422**: Validation Error
  - Schema: `object`

---

## Governance Mode (8 endpoints)

### 🔵 `GET /api/v1/governance/dogfooding/status`

**Summary**: Get dogfooding status

**Operation ID**: `get_dogfooding_status_api_v1_governance_dogfooding_status_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🟢 `POST /api/v1/governance/false-positive`

**Summary**: Report false positive

**Operation ID**: `report_false_positive_api_v1_governance_false_positive_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/governance/health`

**Summary**: Governance service health check

**Operation ID**: `governance_health_api_v1_governance_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Governance Health Api V1 Governance Health Get`

---

### 🟢 `POST /api/v1/governance/kill-switch`

**Summary**: Emergency kill switch

**Operation ID**: `trigger_kill_switch_api_v1_governance_kill_switch_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/governance/metrics`

**Summary**: Get governance metrics

**Operation ID**: `get_governance_metrics_api_v1_governance_metrics_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/governance/mode`

**Summary**: Get current governance mode

**Operation ID**: `get_governance_mode_api_v1_governance_mode_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/governance/mode`

**Summary**: Set governance mode

**Operation ID**: `set_governance_mode_api_v1_governance_mode_put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/governance/mode/state`

**Summary**: Get full governance mode state

**Operation ID**: `get_governance_mode_state_api_v1_governance_mode_state_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

## Governance Specs (5 endpoints)

### 🔵 `GET /api/v1/governance/specs/health`

**Summary**: Specification service health check

**Operation ID**: `specs_health_api_v1_governance_specs_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Specs Health Api V1 Governance Specs Health Get`

---

### 🟢 `POST /api/v1/governance/specs/validate`

**Summary**: Validate YAML Frontmatter

**Operation ID**: `validate_frontmatter_api_v1_governance_specs_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/governance/specs/{spec_id}`

**Summary**: Get Specification Metadata

**Operation ID**: `get_specification_api_v1_governance_specs__spec_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `spec_id` | path | string | ✅ |
| `include_versions` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/governance/specs/{spec_id}/acceptance-criteria`

**Summary**: List Acceptance Criteria

**Operation ID**: `list_acceptance_criteria_api_v1_governance_specs__spec_id__acceptance_criteria_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `spec_id` | path | string | ✅ |
| `tier` | query | string | ❌ |
| `automated_only` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/governance/specs/{spec_id}/requirements`

**Summary**: List Functional Requirements

**Operation ID**: `list_requirements_api_v1_governance_specs__spec_id__requirements_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `spec_id` | path | string | ✅ |
| `tier` | query | string | ❌ |
| `priority` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Governance Vibecoding (7 endpoints)

### 🟢 `POST /api/v1/governance/vibecoding/calculate`

**Summary**: Calculate Vibecoding Index (Database-Backed)

**Operation ID**: `calculate_index_api_v1_governance_vibecoding_calculate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/governance/vibecoding/health`

**Summary**: Vibecoding service health check

**Operation ID**: `vibecoding_health_api_v1_governance_vibecoding_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Vibecoding Health Api V1 Governance Vibecoding Health Get`

---

### 🟢 `POST /api/v1/governance/vibecoding/kill-switch/check`

**Summary**: Check Kill Switch Triggers

**Operation ID**: `check_kill_switch_api_v1_governance_vibecoding_kill_switch_check_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/governance/vibecoding/route`

**Summary**: Progressive Routing Decision

**Operation ID**: `get_routing_decision_api_v1_governance_vibecoding_route_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/governance/vibecoding/signals/{submission_id}`

**Summary**: Get Signal Breakdown

**Operation ID**: `get_signal_breakdown_api_v1_governance_vibecoding_signals__submission_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `submission_id` | path | string | ✅ |
| `project_id` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/governance/vibecoding/stats/{project_id}`

**Summary**: Get Zone Statistics

**Operation ID**: `get_zone_statistics_api_v1_governance_vibecoding_stats__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/governance/vibecoding/{submission_id}`

**Summary**: Get Index History

**Operation ID**: `get_index_history_api_v1_governance_vibecoding__submission_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `submission_id` | path | string | ✅ |
| `project_id` | query | string | ✅ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Grafana Dashboards (7 endpoints)

### 🔵 `GET /api/v1/grafana-dashboards`

**Summary**: List all Grafana dashboards

**Operation ID**: `list_dashboards_api_v1_grafana_dashboards_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/grafana-dashboards/datasource/template`

**Summary**: Get Prometheus datasource template

**Operation ID**: `get_datasource_template_api_v1_grafana_dashboards_datasource_template_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Datasource Template Api V1 Grafana Dashboards Datasource Template Get`

---

### 🔵 `GET /api/v1/grafana-dashboards/export/all`

**Summary**: Export all dashboards

**Operation ID**: `export_all_dashboards_api_v1_grafana_dashboards_export_all_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Export All Dashboards Api V1 Grafana Dashboards Export All Get`

---

### 🟢 `POST /api/v1/grafana-dashboards/provision`

**Summary**: Provision dashboards to Grafana

**Operation ID**: `provision_dashboards_api_v1_grafana_dashboards_provision_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/grafana-dashboards/{dashboard_type}`

**Summary**: Get dashboard configuration

**Operation ID**: `get_dashboard_api_v1_grafana_dashboards__dashboard_type__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dashboard_type` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Dashboard Api V1 Grafana Dashboards  Dashboard Type  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/grafana-dashboards/{dashboard_type}/json`

**Summary**: Download dashboard JSON

**Operation ID**: `download_dashboard_json_api_v1_grafana_dashboards__dashboard_type__json_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dashboard_type` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/grafana-dashboards/{dashboard_type}/panels`

**Summary**: List dashboard panels

**Operation ID**: `list_dashboard_panels_api_v1_grafana_dashboards__dashboard_type__panels_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dashboard_type` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## MCP Analytics (10 endpoints)

### 🔵 `GET /api/v1/mcp/context`

**Summary**: Get context provider usage

**Operation ID**: `get_context_usage_api_v1_mcp_context_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mcp/context`

**Summary**: Get context provider usage

**Operation ID**: `get_context_usage_api_v1_mcp_context_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mcp/cost`

**Summary**: Get cost tracking metrics

**Operation ID**: `get_cost_tracking_api_v1_mcp_cost_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mcp/cost`

**Summary**: Get cost tracking metrics

**Operation ID**: `get_cost_tracking_api_v1_mcp_cost_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mcp/dashboard`

**Summary**: Get complete dashboard summary

**Operation ID**: `get_dashboard_summary_api_v1_mcp_dashboard_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mcp/dashboard`

**Summary**: Get complete dashboard summary

**Operation ID**: `get_dashboard_summary_api_v1_mcp_dashboard_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mcp/health`

**Summary**: Get provider health metrics

**Operation ID**: `get_provider_health_api_v1_mcp_health_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mcp/health`

**Summary**: Get provider health metrics

**Operation ID**: `get_provider_health_api_v1_mcp_health_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mcp/latency`

**Summary**: Get latency metrics

**Operation ID**: `get_latency_metrics_api_v1_mcp_latency_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `granularity` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mcp/latency`

**Summary**: Get latency metrics

**Operation ID**: `get_latency_metrics_api_v1_mcp_latency_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `granularity` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## MRP - Merge Readiness Protocol (18 endpoints)

### 🔵 `GET /api/v1/mrp/health`

**Summary**: Health check

**Operation ID**: `health_check_api_v1_mrp_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Mrp Health Get`

---

### 🔵 `GET /api/v1/mrp/health`

**Summary**: Health check

**Operation ID**: `health_check_api_v1_mrp_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Mrp Health Get`

---

### 🟢 `POST /api/v1/mrp/policies/compare`

**Summary**: Compare two tiers

**Operation ID**: `compare_policy_tiers_api_v1_mrp_policies_compare_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/mrp/policies/compare`

**Summary**: Compare two tiers

**Operation ID**: `compare_policy_tiers_api_v1_mrp_policies_compare_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mrp/policies/compliance/{project_id}`

**Summary**: Get tier compliance report

**Operation ID**: `get_compliance_report_api_v1_mrp_policies_compliance__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mrp/policies/compliance/{project_id}`

**Summary**: Get tier compliance report

**Operation ID**: `get_compliance_report_api_v1_mrp_policies_compliance__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/mrp/policies/enforce`

**Summary**: Enforce policies for PR

**Operation ID**: `enforce_policies_api_v1_mrp_policies_enforce_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/mrp/policies/enforce`

**Summary**: Enforce policies for PR

**Operation ID**: `enforce_policies_api_v1_mrp_policies_enforce_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mrp/policies/tiers`

**Summary**: Get all policy tiers

**Operation ID**: `get_policy_tiers_api_v1_mrp_policies_tiers_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mrp/policies/tiers`

**Summary**: Get all policy tiers

**Operation ID**: `get_policy_tiers_api_v1_mrp_policies_tiers_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/mrp/validate`

**Summary**: Validate MRP 5-point structure

**Operation ID**: `validate_mrp_api_v1_mrp_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/mrp/validate`

**Summary**: Validate MRP 5-point structure

**Operation ID**: `validate_mrp_api_v1_mrp_validate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mrp/validate/{project_id}/{pr_id}`

**Summary**: Get latest MRP validation

**Operation ID**: `get_mrp_validation_api_v1_mrp_validate__project_id___pr_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `pr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mrp/validate/{project_id}/{pr_id}`

**Summary**: Get latest MRP validation

**Operation ID**: `get_mrp_validation_api_v1_mrp_validate__project_id___pr_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `pr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mrp/vcr/{project_id}/history`

**Summary**: Get VCR history

**Operation ID**: `get_vcr_history_api_v1_mrp_vcr__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `pr_id` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mrp/vcr/{project_id}/history`

**Summary**: Get VCR history

**Operation ID**: `get_vcr_history_api_v1_mrp_vcr__project_id__history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `pr_id` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mrp/vcr/{project_id}/{pr_id}`

**Summary**: Get latest VCR

**Operation ID**: `get_vcr_api_v1_mrp_vcr__project_id___pr_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `pr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mrp/vcr/{project_id}/{pr_id}`

**Summary**: Get latest VCR

**Operation ID**: `get_vcr_api_v1_mrp_vcr__project_id___pr_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `pr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## MRP - Policy Enforcement (4 endpoints)

### 🟢 `POST /api/v1/mrp/policies/compare`

**Summary**: Compare two tiers

**Operation ID**: `compare_policy_tiers_api_v1_mrp_policies_compare_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mrp/policies/compliance/{project_id}`

**Summary**: Get tier compliance report

**Operation ID**: `get_compliance_report_api_v1_mrp_policies_compliance__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/mrp/policies/enforce`

**Summary**: Enforce policies for PR

**Operation ID**: `enforce_policies_api_v1_mrp_policies_enforce_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/mrp/policies/tiers`

**Summary**: Get all policy tiers

**Operation ID**: `get_policy_tiers_api_v1_mrp_policies_tiers_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Multi-Agent Team Engine (20 endpoints)

### 🔵 `GET /api/v1/agent-team/conversations`

**Summary**: List conversations

**Operation ID**: `list_conversations_api_v1_agent_team_conversations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `status` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agent-team/conversations`

**Summary**: List conversations

**Operation ID**: `list_conversations_api_v1_agent_team_conversations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `status` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agent-team/conversations`

**Summary**: Start conversation

**Operation ID**: `start_conversation_api_v1_agent_team_conversations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agent-team/conversations`

**Summary**: Start conversation

**Operation ID**: `start_conversation_api_v1_agent_team_conversations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agent-team/conversations/{conversation_id}`

**Summary**: Get conversation

**Operation ID**: `get_conversation_api_v1_agent_team_conversations__conversation_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `conversation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agent-team/conversations/{conversation_id}`

**Summary**: Get conversation

**Operation ID**: `get_conversation_api_v1_agent_team_conversations__conversation_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `conversation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agent-team/conversations/{conversation_id}/interrupt`

**Summary**: Interrupt conversation

**Operation ID**: `interrupt_conversation_api_v1_agent_team_conversations__conversation_id__interrupt_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `conversation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agent-team/conversations/{conversation_id}/interrupt`

**Summary**: Interrupt conversation

**Operation ID**: `interrupt_conversation_api_v1_agent_team_conversations__conversation_id__interrupt_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `conversation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agent-team/conversations/{conversation_id}/messages`

**Summary**: Get messages

**Operation ID**: `get_messages_api_v1_agent_team_conversations__conversation_id__messages_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `conversation_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agent-team/conversations/{conversation_id}/messages`

**Summary**: Get messages

**Operation ID**: `get_messages_api_v1_agent_team_conversations__conversation_id__messages_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `conversation_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agent-team/conversations/{conversation_id}/messages`

**Summary**: Send message

**Operation ID**: `send_message_api_v1_agent_team_conversations__conversation_id__messages_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `conversation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agent-team/conversations/{conversation_id}/messages`

**Summary**: Send message

**Operation ID**: `send_message_api_v1_agent_team_conversations__conversation_id__messages_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `conversation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agent-team/definitions`

**Summary**: List agent definitions

**Operation ID**: `list_agent_definitions_api_v1_agent_team_definitions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `sdlc_role` | query | string | ❌ |
| `is_active` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agent-team/definitions`

**Summary**: List agent definitions

**Operation ID**: `list_agent_definitions_api_v1_agent_team_definitions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `sdlc_role` | query | string | ❌ |
| `is_active` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agent-team/definitions`

**Summary**: Create agent definition

**Operation ID**: `create_agent_definition_api_v1_agent_team_definitions_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/agent-team/definitions`

**Summary**: Create agent definition

**Operation ID**: `create_agent_definition_api_v1_agent_team_definitions_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agent-team/definitions/{definition_id}`

**Summary**: Get agent definition

**Operation ID**: `get_agent_definition_api_v1_agent_team_definitions__definition_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `definition_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/agent-team/definitions/{definition_id}`

**Summary**: Get agent definition

**Operation ID**: `get_agent_definition_api_v1_agent_team_definitions__definition_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `definition_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/agent-team/definitions/{definition_id}`

**Summary**: Update agent definition

**Operation ID**: `update_agent_definition_api_v1_agent_team_definitions__definition_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `definition_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/agent-team/definitions/{definition_id}`

**Summary**: Update agent definition

**Operation ID**: `update_agent_definition_api_v1_agent_team_definitions__definition_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `definition_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Notifications (8 endpoints)

### 🔵 `GET /api/v1/notifications`

**Summary**: List Notifications

**Operation ID**: `list_notifications_api_v1_notifications_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `unread_only` | query | boolean | ❌ |
| `notification_type` | query | string | ❌ |
| `project_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/notifications/read-all`

**Summary**: Mark All Notifications Read

**Operation ID**: `mark_all_notifications_read_api_v1_notifications_read_all_put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/notifications/settings/preferences`

**Summary**: Get Notification Settings

**Operation ID**: `get_notification_settings_api_v1_notifications_settings_preferences_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/notifications/settings/preferences`

**Summary**: Update Notification Settings

**Operation ID**: `update_notification_settings_api_v1_notifications_settings_preferences_put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/notifications/stats/summary`

**Summary**: Get Notification Stats

**Operation ID**: `get_notification_stats_api_v1_notifications_stats_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Notification Stats Api V1 Notifications Stats Summary Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/notifications/{notification_id}`

**Summary**: Delete Notification

**Operation ID**: `delete_notification_api_v1_notifications__notification_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `notification_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/notifications/{notification_id}`

**Summary**: Get Notification

**Operation ID**: `get_notification_api_v1_notifications__notification_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `notification_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/notifications/{notification_id}/read`

**Summary**: Mark Notification Read

**Operation ID**: `mark_notification_read_api_v1_notifications__notification_id__read_put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `notification_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Organization Invitations (7 endpoints)

### 🔴 `DELETE /api/v1/api/v1/org-invitations/{invitation_id}`

**Summary**: Cancel organization invitation

**Operation ID**: `cancel_invitation_api_v1_api_v1_org_invitations__invitation_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `invitation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/org-invitations/{invitation_id}/resend`

**Summary**: Resend organization invitation email

**Operation ID**: `resend_invitation_api_v1_api_v1_org_invitations__invitation_id__resend_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `invitation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/org-invitations/{token}`

**Summary**: Get organization invitation details by token

**Operation ID**: `get_invitation_by_token_api_v1_api_v1_org_invitations__token__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `token` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/org-invitations/{token}/accept`

**Summary**: Accept organization invitation

**Operation ID**: `accept_invitation_api_v1_api_v1_org_invitations__token__accept_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `token` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/org-invitations/{token}/decline`

**Summary**: Decline organization invitation

**Operation ID**: `decline_invitation_api_v1_api_v1_org_invitations__token__decline_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `token` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/organizations/{organization_id}/invitations`

**Summary**: List organization invitations

**Operation ID**: `list_org_invitations_api_v1_api_v1_organizations__organization_id__invitations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `organization_id` | path | string | ✅ |
| `status` | query | string | ❌ |
| `email` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Org Invitations Api V1 Api V1 Organizations  Organization Id  Invitations Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/organizations/{organization_id}/invitations`

**Summary**: Send organization invitation

**Operation ID**: `send_invitation_api_v1_api_v1_organizations__organization_id__invitations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `organization_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Organizations (6 endpoints)

### 🔵 `GET /api/v1/organizations`

**Summary**: List Organizations

**Operation ID**: `list_organizations_api_v1_organizations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `skip` | query | integer | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/organizations`

**Summary**: Create Organization

**Operation ID**: `create_organization_api_v1_organizations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/organizations/{org_id}`

**Summary**: Get Organization

**Operation ID**: `get_organization_api_v1_organizations__org_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `org_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/organizations/{org_id}`

**Summary**: Update Organization

**Operation ID**: `update_organization_api_v1_organizations__org_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `org_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/organizations/{org_id}/members`

**Summary**: Add Member Directly

**Operation ID**: `add_member_directly_api_v1_organizations__org_id__members_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `org_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/organizations/{org_id}/stats`

**Summary**: Get Organization Statistics

**Operation ID**: `get_organization_statistics_api_v1_organizations__org_id__stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `org_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Override / VCR (9 endpoints)

### 🔵 `GET /api/v1/admin/override-queue`

**Summary**: Get override approval queue

**Operation ID**: `get_override_queue_api_v1_admin_override_queue_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/admin/override-stats`

**Summary**: Get override statistics

**Operation ID**: `get_override_stats_api_v1_admin_override_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/overrides/event/{event_id}`

**Summary**: Get overrides for event

**Operation ID**: `get_overrides_for_event_api_v1_overrides_event__event_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `event_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Overrides For Event Api V1 Overrides Event  Event Id  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/overrides/request`

**Summary**: Create override request

**Operation ID**: `create_override_request_api_v1_overrides_request_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/overrides/{override_id}`

**Summary**: Get override details

**Operation ID**: `get_override_api_v1_overrides__override_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `override_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/overrides/{override_id}/approve`

**Summary**: Approve override

**Operation ID**: `approve_override_api_v1_overrides__override_id__approve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `override_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/overrides/{override_id}/cancel`

**Summary**: Cancel override

**Operation ID**: `cancel_override_api_v1_overrides__override_id__cancel_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `override_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/overrides/{override_id}/reject`

**Summary**: Reject override

**Operation ID**: `reject_override_api_v1_overrides__override_id__reject_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `override_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/overrides`

**Summary**: Get project overrides

**Operation ID**: `get_project_overrides_api_v1_projects__project_id__overrides_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `status` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Project Overrides Api V1 Projects  Project Id  Overrides Get`
- **422**: Validation Error
  - Schema: `object`

---

## Payments (5 endpoints)

### 🔵 `GET /api/v1/payments/subscriptions/me`

**Summary**: Get My Subscription

**Operation ID**: `get_my_subscription_api_v1_payments_subscriptions_me_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/payments/vnpay/create`

**Summary**: Create Vnpay Payment

**Operation ID**: `create_vnpay_payment_api_v1_payments_vnpay_create_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/payments/vnpay/ipn`

**Summary**: Vnpay Ipn Handler

**Operation ID**: `vnpay_ipn_handler_api_v1_payments_vnpay_ipn_post`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Vnpay Ipn Handler Api V1 Payments Vnpay Ipn Post`

---

### 🔵 `GET /api/v1/payments/vnpay/return`

**Summary**: Vnpay Return Handler

**Operation ID**: `vnpay_return_handler_api_v1_payments_vnpay_return_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Vnpay Return Handler Api V1 Payments Vnpay Return Get`

---

### 🔵 `GET /api/v1/payments/{vnp_txn_ref}`

**Summary**: Get Payment Status

**Operation ID**: `get_payment_status_api_v1_payments__vnp_txn_ref__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vnp_txn_ref` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Pilot (13 endpoints)

### 🟢 `POST /api/v1/pilot/feedback`

**Summary**: Submit satisfaction survey

**Operation ID**: `submit_feedback_api_v1_pilot_feedback_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/pilot/metrics/aggregate`

**Summary**: Trigger daily metrics aggregation

**Operation ID**: `aggregate_metrics_api_v1_pilot_metrics_aggregate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Aggregate Metrics Api V1 Pilot Metrics Aggregate Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/pilot/metrics/summary`

**Summary**: Get pilot program summary

**Operation ID**: `get_metrics_summary_api_v1_pilot_metrics_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/pilot/metrics/targets`

**Summary**: Get Sprint 49 targets

**Operation ID**: `get_targets_api_v1_pilot_metrics_targets_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Targets Api V1 Pilot Metrics Targets Get`

---

### 🔵 `GET /api/v1/pilot/participants`

**Summary**: List pilot participants

**Operation ID**: `list_participants_api_v1_pilot_participants_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `status` | query | string | ❌ |
| `domain` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Participants Api V1 Pilot Participants Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/pilot/participants`

**Summary**: Register as pilot participant

**Operation ID**: `register_participant_api_v1_pilot_participants_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/pilot/participants/me`

**Summary**: Get current user's participant profile

**Operation ID**: `get_my_participant_profile_api_v1_pilot_participants_me_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/pilot/participants/{participant_id}`

**Summary**: Get participant by ID

**Operation ID**: `get_participant_api_v1_pilot_participants__participant_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `participant_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/pilot/sessions`

**Summary**: Get my sessions

**Operation ID**: `get_my_sessions_api_v1_pilot_sessions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get My Sessions Api V1 Pilot Sessions Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/pilot/sessions`

**Summary**: Start pilot session (TTFV timer begins)

**Operation ID**: `start_session_api_v1_pilot_sessions_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/pilot/sessions/{session_id}`

**Summary**: Get session details

**Operation ID**: `get_session_api_v1_pilot_sessions__session_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/pilot/sessions/{session_id}/generation`

**Summary**: Record generation results

**Operation ID**: `record_generation_api_v1_pilot_sessions__session_id__generation_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/pilot/sessions/{session_id}/stage`

**Summary**: Update session stage

**Operation ID**: `update_session_stage_api_v1_pilot_sessions__session_id__stage_patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Planning (46 endpoints)

### 🟢 `POST /api/v1/planning/action-items/bulk/status`

**Summary**: Bulk update action item status

**Operation ID**: `bulk_update_retro_action_item_status_api_v1_planning_action_items_bulk_status_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Bulk Update Retro Action Item Status Api V1 Planning Action Items Bulk Status Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/action-items/{item_id}`

**Summary**: Delete an action item

**Operation ID**: `delete_retro_action_item_api_v1_planning_action_items__item_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/action-items/{item_id}`

**Summary**: Get a single action item

**Operation ID**: `get_retro_action_item_api_v1_planning_action_items__item_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/action-items/{item_id}`

**Summary**: Update an action item

**Operation ID**: `update_retro_action_item_api_v1_planning_action_items__item_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/allocations`

**Summary**: Create resource allocation

**Operation ID**: `create_resource_allocation_api_v1_planning_allocations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/allocations/check-conflicts`

**Summary**: Check allocation conflicts

**Operation ID**: `check_allocation_conflicts_api_v1_planning_allocations_check_conflicts_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | query | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `allocation_percentage` | query | integer | ✅ |
| `exclude_sprint_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/allocations/{allocation_id}`

**Summary**: Delete a resource allocation

**Operation ID**: `delete_resource_allocation_api_v1_planning_allocations__allocation_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/allocations/{allocation_id}`

**Summary**: Get a resource allocation

**Operation ID**: `get_resource_allocation_api_v1_planning_allocations__allocation_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/allocations/{allocation_id}`

**Summary**: Update a resource allocation

**Operation ID**: `update_resource_allocation_api_v1_planning_allocations__allocation_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies`

**Summary**: Create sprint dependency

**Operation ID**: `create_sprint_dependency_api_v1_planning_dependencies_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies/bulk/resolve`

**Summary**: Bulk resolve dependencies

**Operation ID**: `bulk_resolve_dependencies_api_v1_planning_dependencies_bulk_resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/dependencies/check-circular`

**Summary**: Check for circular dependency

**Operation ID**: `check_circular_dependency_api_v1_planning_dependencies_check_circular_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `source_sprint_id` | query | string | ✅ |
| `target_sprint_id` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Check Circular Dependency Api V1 Planning Dependencies Check Circular Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Delete a sprint dependency

**Operation ID**: `delete_sprint_dependency_api_v1_planning_dependencies__dependency_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Get a sprint dependency

**Operation ID**: `get_sprint_dependency_api_v1_planning_dependencies__dependency_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Update a sprint dependency

**Operation ID**: `update_sprint_dependency_api_v1_planning_dependencies__dependency_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies/{dependency_id}/resolve`

**Summary**: Resolve a sprint dependency

**Operation ID**: `resolve_sprint_dependency_api_v1_planning_dependencies__dependency_id__resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/dependency-analysis`

**Summary**: Analyze project dependencies

**Operation ID**: `analyze_project_dependencies_api_v1_planning_projects__project_id__dependency_analysis_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/dependency-graph`

**Summary**: Get dependency graph for a project

**Operation ID**: `get_project_dependency_graph_api_v1_planning_projects__project_id__dependency_graph_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `include_cross_project` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/resource-heatmap`

**Summary**: Get resource allocation heatmap

**Operation ID**: `get_project_resource_heatmap_api_v1_planning_projects__project_id__resource_heatmap_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_ids` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/retrospective-comparison`

**Summary**: Compare retrospectives across sprints

**Operation ID**: `compare_sprint_retrospectives_api_v1_planning_projects__project_id__retrospective_comparison_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_ids` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Compare Sprint Retrospectives Api V1 Planning Projects  Project Id  Retrospective Comparison Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/template-suggestions`

**Summary**: Get template suggestions for project

**Operation ID**: `get_template_suggestions_api_v1_planning_projects__project_id__template_suggestions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `team_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/velocity`

**Summary**: Get project velocity metrics

**Operation ID**: `get_project_velocity_api_v1_planning_projects__project_id__velocity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_count` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/action-items`

**Summary**: List action items for a sprint

**Operation ID**: `list_retro_action_items_api_v1_planning_sprints__sprint_id__action_items_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `status` | query | string | ❌ |
| `category` | query | string | ❌ |
| `priority` | query | string | ❌ |
| `assignee_id` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/action-items`

**Summary**: Create action item from retrospective

**Operation ID**: `create_retro_action_item_api_v1_planning_sprints__sprint_id__action_items_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/action-items/bulk`

**Summary**: Bulk create action items

**Operation ID**: `bulk_create_retro_action_items_api_v1_planning_sprints__sprint_id__action_items_bulk_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `Response Bulk Create Retro Action Items Api V1 Planning Sprints  Sprint Id  Action Items Bulk Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/action-items/stats`

**Summary**: Get action items statistics

**Operation ID**: `get_retro_action_item_stats_api_v1_planning_sprints__sprint_id__action_items_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/allocations`

**Summary**: List allocations for a sprint

**Operation ID**: `list_sprint_allocations_api_v1_planning_sprints__sprint_id__allocations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/analytics`

**Summary**: Get comprehensive sprint analytics

**Operation ID**: `get_sprint_analytics_api_v1_planning_sprints__sprint_id__analytics_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/burndown`

**Summary**: Get sprint burndown chart data

**Operation ID**: `get_sprint_burndown_api_v1_planning_sprints__sprint_id__burndown_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/capacity`

**Summary**: Get sprint capacity

**Operation ID**: `get_sprint_capacity_api_v1_planning_sprints__sprint_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/dependencies`

**Summary**: List dependencies for a sprint

**Operation ID**: `list_sprint_dependencies_api_v1_planning_sprints__sprint_id__dependencies_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `direction` | query | string | ❌ |
| `include_resolved` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/forecast`

**Summary**: Get sprint completion forecast

**Operation ID**: `get_sprint_forecast_api_v1_planning_sprints__sprint_id__forecast_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/health`

**Summary**: Get sprint health indicators

**Operation ID**: `get_sprint_health_api_v1_planning_sprints__sprint_id__health_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/retrospective`

**Summary**: Get auto-generated sprint retrospective

**Operation ID**: `get_sprint_retrospective_api_v1_planning_sprints__sprint_id__retrospective_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/suggestions`

**Summary**: Get AI prioritization suggestions

**Operation ID**: `get_sprint_suggestions_api_v1_planning_sprints__sprint_id__suggestions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/teams/{team_id}/capacity`

**Summary**: Get team capacity

**Operation ID**: `get_team_capacity_api_v1_planning_teams__team_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates`

**Summary**: List sprint templates

**Operation ID**: `list_sprint_templates_api_v1_planning_templates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | query | string | ❌ |
| `template_type` | query | string | ❌ |
| `include_public` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates`

**Summary**: Create sprint template

**Operation ID**: `create_sprint_template_api_v1_planning_templates_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates/bulk/delete`

**Summary**: Bulk delete templates

**Operation ID**: `bulk_delete_templates_api_v1_planning_templates_bulk_delete_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates/default`

**Summary**: Get default template

**Operation ID**: `get_default_template_api_v1_planning_templates_default_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/templates/{template_id}`

**Summary**: Delete a sprint template

**Operation ID**: `delete_sprint_template_api_v1_planning_templates__template_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates/{template_id}`

**Summary**: Get a sprint template

**Operation ID**: `get_sprint_template_api_v1_planning_templates__template_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/templates/{template_id}`

**Summary**: Update a sprint template

**Operation ID**: `update_sprint_template_api_v1_planning_templates__template_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates/{template_id}/apply`

**Summary**: Apply template to create sprint

**Operation ID**: `apply_sprint_template_api_v1_planning_templates__template_id__apply_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/users/{user_id}/allocations`

**Summary**: List allocations for a user

**Operation ID**: `list_user_allocations_api_v1_planning_users__user_id__allocations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/users/{user_id}/capacity`

**Summary**: Get user capacity

**Operation ID**: `get_user_capacity_api_v1_planning_users__user_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Planning Hierarchy (150 endpoints)

### 🟢 `POST /api/v1/planning/action-items/bulk/status`

**Summary**: Bulk update action item status

**Operation ID**: `bulk_update_retro_action_item_status_api_v1_planning_action_items_bulk_status_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Bulk Update Retro Action Item Status Api V1 Planning Action Items Bulk Status Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/action-items/bulk/status`

**Summary**: Bulk update action item status

**Operation ID**: `bulk_update_retro_action_item_status_api_v1_planning_action_items_bulk_status_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Bulk Update Retro Action Item Status Api V1 Planning Action Items Bulk Status Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/action-items/{item_id}`

**Summary**: Delete an action item

**Operation ID**: `delete_retro_action_item_api_v1_planning_action_items__item_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/action-items/{item_id}`

**Summary**: Delete an action item

**Operation ID**: `delete_retro_action_item_api_v1_planning_action_items__item_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/action-items/{item_id}`

**Summary**: Get a single action item

**Operation ID**: `get_retro_action_item_api_v1_planning_action_items__item_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/action-items/{item_id}`

**Summary**: Get a single action item

**Operation ID**: `get_retro_action_item_api_v1_planning_action_items__item_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/action-items/{item_id}`

**Summary**: Update an action item

**Operation ID**: `update_retro_action_item_api_v1_planning_action_items__item_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/action-items/{item_id}`

**Summary**: Update an action item

**Operation ID**: `update_retro_action_item_api_v1_planning_action_items__item_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/allocations`

**Summary**: Create resource allocation

**Operation ID**: `create_resource_allocation_api_v1_planning_allocations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/allocations`

**Summary**: Create resource allocation

**Operation ID**: `create_resource_allocation_api_v1_planning_allocations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/allocations/check-conflicts`

**Summary**: Check allocation conflicts

**Operation ID**: `check_allocation_conflicts_api_v1_planning_allocations_check_conflicts_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | query | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `allocation_percentage` | query | integer | ✅ |
| `exclude_sprint_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/allocations/check-conflicts`

**Summary**: Check allocation conflicts

**Operation ID**: `check_allocation_conflicts_api_v1_planning_allocations_check_conflicts_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | query | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `allocation_percentage` | query | integer | ✅ |
| `exclude_sprint_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/allocations/{allocation_id}`

**Summary**: Delete a resource allocation

**Operation ID**: `delete_resource_allocation_api_v1_planning_allocations__allocation_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/allocations/{allocation_id}`

**Summary**: Delete a resource allocation

**Operation ID**: `delete_resource_allocation_api_v1_planning_allocations__allocation_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/allocations/{allocation_id}`

**Summary**: Get a resource allocation

**Operation ID**: `get_resource_allocation_api_v1_planning_allocations__allocation_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/allocations/{allocation_id}`

**Summary**: Get a resource allocation

**Operation ID**: `get_resource_allocation_api_v1_planning_allocations__allocation_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/allocations/{allocation_id}`

**Summary**: Update a resource allocation

**Operation ID**: `update_resource_allocation_api_v1_planning_allocations__allocation_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/allocations/{allocation_id}`

**Summary**: Update a resource allocation

**Operation ID**: `update_resource_allocation_api_v1_planning_allocations__allocation_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/backlog`

**Summary**: List Backlog Items

**Operation ID**: `list_backlog_items_api_v1_planning_backlog_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `sprint_id` | query | string | ❌ |
| `type` | query | string | ❌ |
| `status` | query | string | ❌ |
| `priority` | query | string | ❌ |
| `assignee_id` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/backlog`

**Summary**: List Backlog Items

**Operation ID**: `list_backlog_items_api_v1_planning_backlog_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `sprint_id` | query | string | ❌ |
| `type` | query | string | ❌ |
| `status` | query | string | ❌ |
| `priority` | query | string | ❌ |
| `assignee_id` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/backlog`

**Summary**: Create Backlog Item

**Operation ID**: `create_backlog_item_api_v1_planning_backlog_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/backlog`

**Summary**: Create Backlog Item

**Operation ID**: `create_backlog_item_api_v1_planning_backlog_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/backlog/assignees/{project_id}`

**Summary**: Get Valid Assignees

**Operation ID**: `get_valid_assignees_api_v1_planning_backlog_assignees__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Valid Assignees Api V1 Planning Backlog Assignees  Project Id  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/backlog/assignees/{project_id}`

**Summary**: Get Valid Assignees

**Operation ID**: `get_valid_assignees_api_v1_planning_backlog_assignees__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Valid Assignees Api V1 Planning Backlog Assignees  Project Id  Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/backlog/bulk/move-to-sprint`

**Summary**: Bulk Move To Sprint

**Operation ID**: `bulk_move_to_sprint_api_v1_planning_backlog_bulk_move_to_sprint_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/backlog/bulk/move-to-sprint`

**Summary**: Bulk Move To Sprint

**Operation ID**: `bulk_move_to_sprint_api_v1_planning_backlog_bulk_move_to_sprint_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/backlog/bulk/update-priority`

**Summary**: Bulk Update Priority

**Operation ID**: `bulk_update_priority_api_v1_planning_backlog_bulk_update_priority_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/backlog/bulk/update-priority`

**Summary**: Bulk Update Priority

**Operation ID**: `bulk_update_priority_api_v1_planning_backlog_bulk_update_priority_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/backlog/{item_id}`

**Summary**: Delete Backlog Item

**Operation ID**: `delete_backlog_item_api_v1_planning_backlog__item_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/backlog/{item_id}`

**Summary**: Delete Backlog Item

**Operation ID**: `delete_backlog_item_api_v1_planning_backlog__item_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/backlog/{item_id}`

**Summary**: Get Backlog Item

**Operation ID**: `get_backlog_item_api_v1_planning_backlog__item_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/backlog/{item_id}`

**Summary**: Get Backlog Item

**Operation ID**: `get_backlog_item_api_v1_planning_backlog__item_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/backlog/{item_id}`

**Summary**: Update Backlog Item

**Operation ID**: `update_backlog_item_api_v1_planning_backlog__item_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/backlog/{item_id}`

**Summary**: Update Backlog Item

**Operation ID**: `update_backlog_item_api_v1_planning_backlog__item_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/dashboard/{project_id}`

**Summary**: Get Planning Dashboard

**Operation ID**: `get_planning_dashboard_api_v1_planning_dashboard__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/dashboard/{project_id}`

**Summary**: Get Planning Dashboard

**Operation ID**: `get_planning_dashboard_api_v1_planning_dashboard__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies`

**Summary**: Create sprint dependency

**Operation ID**: `create_sprint_dependency_api_v1_planning_dependencies_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies`

**Summary**: Create sprint dependency

**Operation ID**: `create_sprint_dependency_api_v1_planning_dependencies_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies/bulk/resolve`

**Summary**: Bulk resolve dependencies

**Operation ID**: `bulk_resolve_dependencies_api_v1_planning_dependencies_bulk_resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies/bulk/resolve`

**Summary**: Bulk resolve dependencies

**Operation ID**: `bulk_resolve_dependencies_api_v1_planning_dependencies_bulk_resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/dependencies/check-circular`

**Summary**: Check for circular dependency

**Operation ID**: `check_circular_dependency_api_v1_planning_dependencies_check_circular_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `source_sprint_id` | query | string | ✅ |
| `target_sprint_id` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Check Circular Dependency Api V1 Planning Dependencies Check Circular Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/dependencies/check-circular`

**Summary**: Check for circular dependency

**Operation ID**: `check_circular_dependency_api_v1_planning_dependencies_check_circular_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `source_sprint_id` | query | string | ✅ |
| `target_sprint_id` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Check Circular Dependency Api V1 Planning Dependencies Check Circular Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Delete a sprint dependency

**Operation ID**: `delete_sprint_dependency_api_v1_planning_dependencies__dependency_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Delete a sprint dependency

**Operation ID**: `delete_sprint_dependency_api_v1_planning_dependencies__dependency_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Get a sprint dependency

**Operation ID**: `get_sprint_dependency_api_v1_planning_dependencies__dependency_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Get a sprint dependency

**Operation ID**: `get_sprint_dependency_api_v1_planning_dependencies__dependency_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Update a sprint dependency

**Operation ID**: `update_sprint_dependency_api_v1_planning_dependencies__dependency_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Update a sprint dependency

**Operation ID**: `update_sprint_dependency_api_v1_planning_dependencies__dependency_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies/{dependency_id}/resolve`

**Summary**: Resolve a sprint dependency

**Operation ID**: `resolve_sprint_dependency_api_v1_planning_dependencies__dependency_id__resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies/{dependency_id}/resolve`

**Summary**: Resolve a sprint dependency

**Operation ID**: `resolve_sprint_dependency_api_v1_planning_dependencies__dependency_id__resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/phases`

**Summary**: List Phases

**Operation ID**: `list_phases_api_v1_planning_phases_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `roadmap_id` | query | string | ✅ |
| `status` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/phases`

**Summary**: List Phases

**Operation ID**: `list_phases_api_v1_planning_phases_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `roadmap_id` | query | string | ✅ |
| `status` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/phases`

**Summary**: Create Phase

**Operation ID**: `create_phase_api_v1_planning_phases_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/phases`

**Summary**: Create Phase

**Operation ID**: `create_phase_api_v1_planning_phases_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/phases/{phase_id}`

**Summary**: Delete Phase

**Operation ID**: `delete_phase_api_v1_planning_phases__phase_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `phase_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/phases/{phase_id}`

**Summary**: Delete Phase

**Operation ID**: `delete_phase_api_v1_planning_phases__phase_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `phase_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/phases/{phase_id}`

**Summary**: Get Phase

**Operation ID**: `get_phase_api_v1_planning_phases__phase_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `phase_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/phases/{phase_id}`

**Summary**: Get Phase

**Operation ID**: `get_phase_api_v1_planning_phases__phase_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `phase_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/phases/{phase_id}`

**Summary**: Update Phase

**Operation ID**: `update_phase_api_v1_planning_phases__phase_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `phase_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/phases/{phase_id}`

**Summary**: Update Phase

**Operation ID**: `update_phase_api_v1_planning_phases__phase_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `phase_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/dependency-analysis`

**Summary**: Analyze project dependencies

**Operation ID**: `analyze_project_dependencies_api_v1_planning_projects__project_id__dependency_analysis_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/dependency-analysis`

**Summary**: Analyze project dependencies

**Operation ID**: `analyze_project_dependencies_api_v1_planning_projects__project_id__dependency_analysis_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/dependency-graph`

**Summary**: Get dependency graph for a project

**Operation ID**: `get_project_dependency_graph_api_v1_planning_projects__project_id__dependency_graph_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `include_cross_project` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/dependency-graph`

**Summary**: Get dependency graph for a project

**Operation ID**: `get_project_dependency_graph_api_v1_planning_projects__project_id__dependency_graph_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `include_cross_project` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/resource-heatmap`

**Summary**: Get resource allocation heatmap

**Operation ID**: `get_project_resource_heatmap_api_v1_planning_projects__project_id__resource_heatmap_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_ids` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/resource-heatmap`

**Summary**: Get resource allocation heatmap

**Operation ID**: `get_project_resource_heatmap_api_v1_planning_projects__project_id__resource_heatmap_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_ids` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/retrospective-comparison`

**Summary**: Compare retrospectives across sprints

**Operation ID**: `compare_sprint_retrospectives_api_v1_planning_projects__project_id__retrospective_comparison_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_ids` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Compare Sprint Retrospectives Api V1 Planning Projects  Project Id  Retrospective Comparison Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/retrospective-comparison`

**Summary**: Compare retrospectives across sprints

**Operation ID**: `compare_sprint_retrospectives_api_v1_planning_projects__project_id__retrospective_comparison_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_ids` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Compare Sprint Retrospectives Api V1 Planning Projects  Project Id  Retrospective Comparison Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/template-suggestions`

**Summary**: Get template suggestions for project

**Operation ID**: `get_template_suggestions_api_v1_planning_projects__project_id__template_suggestions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `team_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/template-suggestions`

**Summary**: Get template suggestions for project

**Operation ID**: `get_template_suggestions_api_v1_planning_projects__project_id__template_suggestions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `team_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/velocity`

**Summary**: Get project velocity metrics

**Operation ID**: `get_project_velocity_api_v1_planning_projects__project_id__velocity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_count` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/velocity`

**Summary**: Get project velocity metrics

**Operation ID**: `get_project_velocity_api_v1_planning_projects__project_id__velocity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_count` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/roadmaps`

**Summary**: List Roadmaps

**Operation ID**: `list_roadmaps_api_v1_planning_roadmaps_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `status` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/roadmaps`

**Summary**: List Roadmaps

**Operation ID**: `list_roadmaps_api_v1_planning_roadmaps_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `status` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/roadmaps`

**Summary**: Create Roadmap

**Operation ID**: `create_roadmap_api_v1_planning_roadmaps_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/roadmaps`

**Summary**: Create Roadmap

**Operation ID**: `create_roadmap_api_v1_planning_roadmaps_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/roadmaps/{roadmap_id}`

**Summary**: Delete Roadmap

**Operation ID**: `delete_roadmap_api_v1_planning_roadmaps__roadmap_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `roadmap_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/roadmaps/{roadmap_id}`

**Summary**: Delete Roadmap

**Operation ID**: `delete_roadmap_api_v1_planning_roadmaps__roadmap_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `roadmap_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/roadmaps/{roadmap_id}`

**Summary**: Get Roadmap

**Operation ID**: `get_roadmap_api_v1_planning_roadmaps__roadmap_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `roadmap_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/roadmaps/{roadmap_id}`

**Summary**: Get Roadmap

**Operation ID**: `get_roadmap_api_v1_planning_roadmaps__roadmap_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `roadmap_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/roadmaps/{roadmap_id}`

**Summary**: Update Roadmap

**Operation ID**: `update_roadmap_api_v1_planning_roadmaps__roadmap_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `roadmap_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/roadmaps/{roadmap_id}`

**Summary**: Update Roadmap

**Operation ID**: `update_roadmap_api_v1_planning_roadmaps__roadmap_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `roadmap_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints`

**Summary**: List Sprints

**Operation ID**: `list_sprints_api_v1_planning_sprints_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `phase_id` | query | string | ❌ |
| `status` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints`

**Summary**: List Sprints

**Operation ID**: `list_sprints_api_v1_planning_sprints_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `phase_id` | query | string | ❌ |
| `status` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints`

**Summary**: Create Sprint

**Operation ID**: `create_sprint_api_v1_planning_sprints_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints`

**Summary**: Create Sprint

**Operation ID**: `create_sprint_api_v1_planning_sprints_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/sprints/{sprint_id}`

**Summary**: Delete Sprint

**Operation ID**: `delete_sprint_api_v1_planning_sprints__sprint_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/sprints/{sprint_id}`

**Summary**: Delete Sprint

**Operation ID**: `delete_sprint_api_v1_planning_sprints__sprint_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}`

**Summary**: Get Sprint

**Operation ID**: `get_sprint_api_v1_planning_sprints__sprint_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}`

**Summary**: Get Sprint

**Operation ID**: `get_sprint_api_v1_planning_sprints__sprint_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/sprints/{sprint_id}`

**Summary**: Update Sprint

**Operation ID**: `update_sprint_api_v1_planning_sprints__sprint_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/sprints/{sprint_id}`

**Summary**: Update Sprint

**Operation ID**: `update_sprint_api_v1_planning_sprints__sprint_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/action-items`

**Summary**: List action items for a sprint

**Operation ID**: `list_retro_action_items_api_v1_planning_sprints__sprint_id__action_items_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `status` | query | string | ❌ |
| `category` | query | string | ❌ |
| `priority` | query | string | ❌ |
| `assignee_id` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/action-items`

**Summary**: List action items for a sprint

**Operation ID**: `list_retro_action_items_api_v1_planning_sprints__sprint_id__action_items_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `status` | query | string | ❌ |
| `category` | query | string | ❌ |
| `priority` | query | string | ❌ |
| `assignee_id` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/action-items`

**Summary**: Create action item from retrospective

**Operation ID**: `create_retro_action_item_api_v1_planning_sprints__sprint_id__action_items_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/action-items`

**Summary**: Create action item from retrospective

**Operation ID**: `create_retro_action_item_api_v1_planning_sprints__sprint_id__action_items_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/action-items/bulk`

**Summary**: Bulk create action items

**Operation ID**: `bulk_create_retro_action_items_api_v1_planning_sprints__sprint_id__action_items_bulk_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `Response Bulk Create Retro Action Items Api V1 Planning Sprints  Sprint Id  Action Items Bulk Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/action-items/bulk`

**Summary**: Bulk create action items

**Operation ID**: `bulk_create_retro_action_items_api_v1_planning_sprints__sprint_id__action_items_bulk_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `Response Bulk Create Retro Action Items Api V1 Planning Sprints  Sprint Id  Action Items Bulk Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/action-items/stats`

**Summary**: Get action items statistics

**Operation ID**: `get_retro_action_item_stats_api_v1_planning_sprints__sprint_id__action_items_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/action-items/stats`

**Summary**: Get action items statistics

**Operation ID**: `get_retro_action_item_stats_api_v1_planning_sprints__sprint_id__action_items_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/allocations`

**Summary**: List allocations for a sprint

**Operation ID**: `list_sprint_allocations_api_v1_planning_sprints__sprint_id__allocations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/allocations`

**Summary**: List allocations for a sprint

**Operation ID**: `list_sprint_allocations_api_v1_planning_sprints__sprint_id__allocations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/analytics`

**Summary**: Get comprehensive sprint analytics

**Operation ID**: `get_sprint_analytics_api_v1_planning_sprints__sprint_id__analytics_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/analytics`

**Summary**: Get comprehensive sprint analytics

**Operation ID**: `get_sprint_analytics_api_v1_planning_sprints__sprint_id__analytics_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/burndown`

**Summary**: Get sprint burndown chart data

**Operation ID**: `get_sprint_burndown_api_v1_planning_sprints__sprint_id__burndown_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/burndown`

**Summary**: Get sprint burndown chart data

**Operation ID**: `get_sprint_burndown_api_v1_planning_sprints__sprint_id__burndown_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/capacity`

**Summary**: Get sprint capacity

**Operation ID**: `get_sprint_capacity_api_v1_planning_sprints__sprint_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/capacity`

**Summary**: Get sprint capacity

**Operation ID**: `get_sprint_capacity_api_v1_planning_sprints__sprint_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/dependencies`

**Summary**: List dependencies for a sprint

**Operation ID**: `list_sprint_dependencies_api_v1_planning_sprints__sprint_id__dependencies_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `direction` | query | string | ❌ |
| `include_resolved` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/dependencies`

**Summary**: List dependencies for a sprint

**Operation ID**: `list_sprint_dependencies_api_v1_planning_sprints__sprint_id__dependencies_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `direction` | query | string | ❌ |
| `include_resolved` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/forecast`

**Summary**: Get sprint completion forecast

**Operation ID**: `get_sprint_forecast_api_v1_planning_sprints__sprint_id__forecast_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/forecast`

**Summary**: Get sprint completion forecast

**Operation ID**: `get_sprint_forecast_api_v1_planning_sprints__sprint_id__forecast_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/gates`

**Summary**: List Gate Evaluations

**Operation ID**: `list_gate_evaluations_api_v1_planning_sprints__sprint_id__gates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Gate Evaluations Api V1 Planning Sprints  Sprint Id  Gates Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/gates`

**Summary**: List Gate Evaluations

**Operation ID**: `list_gate_evaluations_api_v1_planning_sprints__sprint_id__gates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Gate Evaluations Api V1 Planning Sprints  Sprint Id  Gates Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/gates`

**Summary**: Create Gate Evaluation

**Operation ID**: `create_gate_evaluation_api_v1_planning_sprints__sprint_id__gates_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/gates`

**Summary**: Create Gate Evaluation

**Operation ID**: `create_gate_evaluation_api_v1_planning_sprints__sprint_id__gates_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/gates/{gate_type}`

**Summary**: Get Gate Evaluation

**Operation ID**: `get_gate_evaluation_api_v1_planning_sprints__sprint_id__gates__gate_type__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `gate_type` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/gates/{gate_type}`

**Summary**: Get Gate Evaluation

**Operation ID**: `get_gate_evaluation_api_v1_planning_sprints__sprint_id__gates__gate_type__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `gate_type` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/sprints/{sprint_id}/gates/{gate_type}`

**Summary**: Update Gate Evaluation

**Operation ID**: `update_gate_evaluation_api_v1_planning_sprints__sprint_id__gates__gate_type__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `gate_type` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/sprints/{sprint_id}/gates/{gate_type}`

**Summary**: Update Gate Evaluation

**Operation ID**: `update_gate_evaluation_api_v1_planning_sprints__sprint_id__gates__gate_type__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `gate_type` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/gates/{gate_type}/submit`

**Summary**: Submit Gate Evaluation

**Operation ID**: `submit_gate_evaluation_api_v1_planning_sprints__sprint_id__gates__gate_type__submit_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `gate_type` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/gates/{gate_type}/submit`

**Summary**: Submit Gate Evaluation

**Operation ID**: `submit_gate_evaluation_api_v1_planning_sprints__sprint_id__gates__gate_type__submit_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `gate_type` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/health`

**Summary**: Get sprint health indicators

**Operation ID**: `get_sprint_health_api_v1_planning_sprints__sprint_id__health_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/health`

**Summary**: Get sprint health indicators

**Operation ID**: `get_sprint_health_api_v1_planning_sprints__sprint_id__health_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/retrospective`

**Summary**: Get auto-generated sprint retrospective

**Operation ID**: `get_sprint_retrospective_api_v1_planning_sprints__sprint_id__retrospective_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/retrospective`

**Summary**: Get auto-generated sprint retrospective

**Operation ID**: `get_sprint_retrospective_api_v1_planning_sprints__sprint_id__retrospective_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/suggestions`

**Summary**: Get AI prioritization suggestions

**Operation ID**: `get_sprint_suggestions_api_v1_planning_sprints__sprint_id__suggestions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/suggestions`

**Summary**: Get AI prioritization suggestions

**Operation ID**: `get_sprint_suggestions_api_v1_planning_sprints__sprint_id__suggestions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/teams/{team_id}/capacity`

**Summary**: Get team capacity

**Operation ID**: `get_team_capacity_api_v1_planning_teams__team_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/teams/{team_id}/capacity`

**Summary**: Get team capacity

**Operation ID**: `get_team_capacity_api_v1_planning_teams__team_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates`

**Summary**: List sprint templates

**Operation ID**: `list_sprint_templates_api_v1_planning_templates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | query | string | ❌ |
| `template_type` | query | string | ❌ |
| `include_public` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates`

**Summary**: List sprint templates

**Operation ID**: `list_sprint_templates_api_v1_planning_templates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | query | string | ❌ |
| `template_type` | query | string | ❌ |
| `include_public` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates`

**Summary**: Create sprint template

**Operation ID**: `create_sprint_template_api_v1_planning_templates_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates`

**Summary**: Create sprint template

**Operation ID**: `create_sprint_template_api_v1_planning_templates_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates/bulk/delete`

**Summary**: Bulk delete templates

**Operation ID**: `bulk_delete_templates_api_v1_planning_templates_bulk_delete_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates/bulk/delete`

**Summary**: Bulk delete templates

**Operation ID**: `bulk_delete_templates_api_v1_planning_templates_bulk_delete_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates/default`

**Summary**: Get default template

**Operation ID**: `get_default_template_api_v1_planning_templates_default_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates/default`

**Summary**: Get default template

**Operation ID**: `get_default_template_api_v1_planning_templates_default_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/templates/{template_id}`

**Summary**: Delete a sprint template

**Operation ID**: `delete_sprint_template_api_v1_planning_templates__template_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/templates/{template_id}`

**Summary**: Delete a sprint template

**Operation ID**: `delete_sprint_template_api_v1_planning_templates__template_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates/{template_id}`

**Summary**: Get a sprint template

**Operation ID**: `get_sprint_template_api_v1_planning_templates__template_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates/{template_id}`

**Summary**: Get a sprint template

**Operation ID**: `get_sprint_template_api_v1_planning_templates__template_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/templates/{template_id}`

**Summary**: Update a sprint template

**Operation ID**: `update_sprint_template_api_v1_planning_templates__template_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/templates/{template_id}`

**Summary**: Update a sprint template

**Operation ID**: `update_sprint_template_api_v1_planning_templates__template_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates/{template_id}/apply`

**Summary**: Apply template to create sprint

**Operation ID**: `apply_sprint_template_api_v1_planning_templates__template_id__apply_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates/{template_id}/apply`

**Summary**: Apply template to create sprint

**Operation ID**: `apply_sprint_template_api_v1_planning_templates__template_id__apply_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/users/{user_id}/allocations`

**Summary**: List allocations for a user

**Operation ID**: `list_user_allocations_api_v1_planning_users__user_id__allocations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/users/{user_id}/allocations`

**Summary**: List allocations for a user

**Operation ID**: `list_user_allocations_api_v1_planning_users__user_id__allocations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/users/{user_id}/capacity`

**Summary**: Get user capacity

**Operation ID**: `get_user_capacity_api_v1_planning_users__user_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/users/{user_id}/capacity`

**Summary**: Get user capacity

**Operation ID**: `get_user_capacity_api_v1_planning_users__user_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Planning Sub-agent (16 endpoints)

### 🟢 `POST /api/v1/planning/subagent/conformance`

**Summary**: Check PR conformance

**Operation ID**: `check_conformance_api_v1_planning_subagent_conformance_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/subagent/conformance`

**Summary**: Check PR conformance

**Operation ID**: `check_conformance_api_v1_planning_subagent_conformance_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/subagent/health`

**Summary**: Health check

**Operation ID**: `health_check_api_v1_planning_subagent_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Planning Subagent Health Get`

---

### 🔵 `GET /api/v1/planning/subagent/health`

**Summary**: Health check

**Operation ID**: `health_check_api_v1_planning_subagent_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Planning Subagent Health Get`

---

### 🟢 `POST /api/v1/planning/subagent/plan`

**Summary**: Start planning session

**Operation ID**: `create_planning_session_api_v1_planning_subagent_plan_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/subagent/plan`

**Summary**: Start planning session

**Operation ID**: `create_planning_session_api_v1_planning_subagent_plan_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/subagent/plan/with-risk`

**Summary**: Start risk-based planning session (Sprint 101)

**Operation ID**: `create_risk_based_planning_session_api_v1_planning_subagent_plan_with_risk_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/subagent/plan/with-risk`

**Summary**: Start risk-based planning session (Sprint 101)

**Operation ID**: `create_risk_based_planning_session_api_v1_planning_subagent_plan_with_risk_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/subagent/sessions`

**Summary**: List planning sessions

**Operation ID**: `list_planning_sessions_api_v1_planning_subagent_sessions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `status_filter` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/subagent/sessions`

**Summary**: List planning sessions

**Operation ID**: `list_planning_sessions_api_v1_planning_subagent_sessions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `status_filter` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/subagent/should-plan`

**Summary**: Check if planning is required

**Operation ID**: `check_should_plan_api_v1_planning_subagent_should_plan_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/subagent/should-plan`

**Summary**: Check if planning is required

**Operation ID**: `check_should_plan_api_v1_planning_subagent_should_plan_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/subagent/{planning_id}`

**Summary**: Get planning result

**Operation ID**: `get_planning_session_api_v1_planning_subagent__planning_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `planning_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/subagent/{planning_id}`

**Summary**: Get planning result

**Operation ID**: `get_planning_session_api_v1_planning_subagent__planning_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `planning_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/subagent/{planning_id}/approve`

**Summary**: Approve or reject plan

**Operation ID**: `approve_planning_session_api_v1_planning_subagent__planning_id__approve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `planning_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/subagent/{planning_id}/approve`

**Summary**: Approve or reject plan

**Operation ID**: `approve_planning_session_api_v1_planning_subagent__planning_id__approve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `planning_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Policies (5 endpoints)

### 🔵 `GET /api/v1/policies`

**Summary**: List policies

**Operation ID**: `list_policies_api_v1_policies_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `stage` | query | string | ❌ |
| `is_active` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/policies/evaluate`

**Summary**: Evaluate policy

**Operation ID**: `evaluate_policy_api_v1_policies_evaluate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/policies/evaluations/{gate_id}`

**Summary**: Get policy evaluations for gate

**Operation ID**: `get_gate_evaluations_api_v1_policies_evaluations__gate_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `gate_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/policies/{policy_id}`

**Summary**: Get policy details

**Operation ID**: `get_policy_api_v1_policies__policy_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `policy_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/policies/{policy_id}`

**Summary**: Update policy

**Operation ID**: `update_policy_api_v1_policies__policy_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `policy_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Policy Packs (8 endpoints)

### 🔴 `DELETE /api/v1/projects/{project_id}/policy-pack`

**Summary**: Delete policy pack

**Operation ID**: `delete_policy_pack_api_v1_projects__project_id__policy_pack_delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/policy-pack`

**Summary**: Get project's policy pack

**Operation ID**: `get_policy_pack_api_v1_projects__project_id__policy_pack_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/policy-pack`

**Summary**: Create or update policy pack

**Operation ID**: `create_policy_pack_api_v1_projects__project_id__policy_pack_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/policy-pack/evaluate`

**Summary**: Evaluate policies

**Operation ID**: `evaluate_policies_api_v1_projects__project_id__policy_pack_evaluate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Evaluate Policies Api V1 Projects  Project Id  Policy Pack Evaluate Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/policy-pack/init`

**Summary**: Initialize default policy pack

**Operation ID**: `init_default_pack_api_v1_projects__project_id__policy_pack_init_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `tier` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/policy-pack/rules`

**Summary**: Add policy rule

**Operation ID**: `add_policy_rule_api_v1_projects__project_id__policy_pack_rules_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/projects/{project_id}/policy-pack/rules/{policy_id}`

**Summary**: Delete policy rule

**Operation ID**: `delete_policy_rule_api_v1_projects__project_id__policy_pack_rules__policy_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `policy_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/projects/{project_id}/policy-pack/rules/{policy_id}`

**Summary**: Update policy rule

**Operation ID**: `update_policy_rule_api_v1_projects__project_id__policy_pack_rules__policy_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `policy_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Preview (6 endpoints)

### 🔴 `DELETE /api/v1/codegen/preview/{token}`

**Summary**: Delete Preview

**Operation ID**: `delete_preview_api_v1_codegen_preview__token__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `token` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/codegen/preview/{token}`

**Summary**: Delete Preview

**Operation ID**: `delete_preview_api_v1_codegen_preview__token__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `token` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/preview/{token}`

**Summary**: Get Preview

**Operation ID**: `get_preview_api_v1_codegen_preview__token__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `token` | path | string | ✅ |
| `password` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/codegen/preview/{token}`

**Summary**: Get Preview

**Operation ID**: `get_preview_api_v1_codegen_preview__token__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `token` | path | string | ✅ |
| `password` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/sessions/{session_id}/preview`

**Summary**: Create Preview

**Operation ID**: `create_preview_api_v1_codegen_sessions__session_id__preview_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/codegen/sessions/{session_id}/preview`

**Summary**: Create Preview

**Operation ID**: `create_preview_api_v1_codegen_sessions__session_id__preview_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Projects (10 endpoints)

### 🔵 `GET /api/v1/projects`

**Summary**: List Projects

**Operation ID**: `list_projects_api_v1_projects_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `skip` | query | integer | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects`

**Summary**: Create Project

**Operation ID**: `create_project_api_v1_projects_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/init`

**Summary**: Initialize SDLC project

**Operation ID**: `init_project_api_v1_projects_init_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/projects/{project_id}`

**Summary**: Delete Project

**Operation ID**: `delete_project_api_v1_projects__project_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}`

**Summary**: Get Project

**Operation ID**: `get_project_api_v1_projects__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/projects/{project_id}`

**Summary**: Update Project

**Operation ID**: `update_project_api_v1_projects__project_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/context`

**Summary**: Get project context (stage, gate, sprint)

**Operation ID**: `get_project_context_api_v1_projects__project_id__context_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/projects/{project_id}/context`

**Summary**: Update project context (stage, gate, sprint)

**Operation ID**: `update_project_context_api_v1_projects__project_id__context_put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/migrate-stages`

**Summary**: Migrate project stages to SDLC 5.0.0

**Operation ID**: `migrate_stages_api_v1_projects__project_id__migrate_stages_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/sync`

**Summary**: Sync project metadata from repository files

**Operation ID**: `sync_project_metadata_api_v1_projects__project_id__sync_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Push Notifications (10 endpoints)

### 🔵 `GET /api/v1/push/status`

**Summary**: Get Push Status

**Operation ID**: `get_push_status_api_v1_push_status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/push/status`

**Summary**: Get Push Status

**Operation ID**: `get_push_status_api_v1_push_status_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/push/subscribe`

**Summary**: Subscribe To Push

**Operation ID**: `subscribe_to_push_api_v1_push_subscribe_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/push/subscribe`

**Summary**: Subscribe To Push

**Operation ID**: `subscribe_to_push_api_v1_push_subscribe_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/push/subscriptions`

**Summary**: List User Subscriptions

**Operation ID**: `list_user_subscriptions_api_v1_push_subscriptions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List User Subscriptions Api V1 Push Subscriptions Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/push/subscriptions`

**Summary**: List User Subscriptions

**Operation ID**: `list_user_subscriptions_api_v1_push_subscriptions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List User Subscriptions Api V1 Push Subscriptions Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/push/unsubscribe`

**Summary**: Unsubscribe From Push

**Operation ID**: `unsubscribe_from_push_api_v1_push_unsubscribe_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/push/unsubscribe`

**Summary**: Unsubscribe From Push

**Operation ID**: `unsubscribe_from_push_api_v1_push_unsubscribe_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/push/vapid-key`

**Summary**: Get Vapid Public Key

**Operation ID**: `get_vapid_public_key_api_v1_push_vapid_key_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/push/vapid-key`

**Summary**: Get Vapid Public Key

**Operation ID**: `get_vapid_public_key_api_v1_push_vapid_key_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

## Resource Allocation (11 endpoints)

### 🟢 `POST /api/v1/planning/allocations`

**Summary**: Create resource allocation

**Operation ID**: `create_resource_allocation_api_v1_planning_allocations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/allocations/check-conflicts`

**Summary**: Check allocation conflicts

**Operation ID**: `check_allocation_conflicts_api_v1_planning_allocations_check_conflicts_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | query | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `allocation_percentage` | query | integer | ✅ |
| `exclude_sprint_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/allocations/{allocation_id}`

**Summary**: Delete a resource allocation

**Operation ID**: `delete_resource_allocation_api_v1_planning_allocations__allocation_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/allocations/{allocation_id}`

**Summary**: Get a resource allocation

**Operation ID**: `get_resource_allocation_api_v1_planning_allocations__allocation_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/allocations/{allocation_id}`

**Summary**: Update a resource allocation

**Operation ID**: `update_resource_allocation_api_v1_planning_allocations__allocation_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/resource-heatmap`

**Summary**: Get resource allocation heatmap

**Operation ID**: `get_project_resource_heatmap_api_v1_planning_projects__project_id__resource_heatmap_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_ids` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/allocations`

**Summary**: List allocations for a sprint

**Operation ID**: `list_sprint_allocations_api_v1_planning_sprints__sprint_id__allocations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/capacity`

**Summary**: Get sprint capacity

**Operation ID**: `get_sprint_capacity_api_v1_planning_sprints__sprint_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/teams/{team_id}/capacity`

**Summary**: Get team capacity

**Operation ID**: `get_team_capacity_api_v1_planning_teams__team_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/users/{user_id}/allocations`

**Summary**: List allocations for a user

**Operation ID**: `list_user_allocations_api_v1_planning_users__user_id__allocations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/users/{user_id}/capacity`

**Summary**: Get user capacity

**Operation ID**: `get_user_capacity_api_v1_planning_users__user_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Retrospective (9 endpoints)

### 🟢 `POST /api/v1/planning/action-items/bulk/status`

**Summary**: Bulk update action item status

**Operation ID**: `bulk_update_retro_action_item_status_api_v1_planning_action_items_bulk_status_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Bulk Update Retro Action Item Status Api V1 Planning Action Items Bulk Status Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/action-items/{item_id}`

**Summary**: Delete an action item

**Operation ID**: `delete_retro_action_item_api_v1_planning_action_items__item_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/action-items/{item_id}`

**Summary**: Get a single action item

**Operation ID**: `get_retro_action_item_api_v1_planning_action_items__item_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/action-items/{item_id}`

**Summary**: Update an action item

**Operation ID**: `update_retro_action_item_api_v1_planning_action_items__item_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/retrospective-comparison`

**Summary**: Compare retrospectives across sprints

**Operation ID**: `compare_sprint_retrospectives_api_v1_planning_projects__project_id__retrospective_comparison_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_ids` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Compare Sprint Retrospectives Api V1 Planning Projects  Project Id  Retrospective Comparison Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/action-items`

**Summary**: List action items for a sprint

**Operation ID**: `list_retro_action_items_api_v1_planning_sprints__sprint_id__action_items_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `status` | query | string | ❌ |
| `category` | query | string | ❌ |
| `priority` | query | string | ❌ |
| `assignee_id` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/action-items`

**Summary**: Create action item from retrospective

**Operation ID**: `create_retro_action_item_api_v1_planning_sprints__sprint_id__action_items_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/action-items/bulk`

**Summary**: Bulk create action items

**Operation ID**: `bulk_create_retro_action_items_api_v1_planning_sprints__sprint_id__action_items_bulk_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `Response Bulk Create Retro Action Items Api V1 Planning Sprints  Sprint Id  Action Items Bulk Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/action-items/stats`

**Summary**: Get action items statistics

**Operation ID**: `get_retro_action_item_stats_api_v1_planning_sprints__sprint_id__action_items_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Risk Analysis (8 endpoints)

### 🟢 `POST /api/v1/risk/analyze`

**Summary**: Analyze diff for risk factors

**Operation ID**: `analyze_diff_api_v1_risk_analyze_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/risk/analyze`

**Summary**: Analyze diff for risk factors

**Operation ID**: `analyze_diff_api_v1_risk_analyze_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/risk/factors`

**Summary**: List 7 mandatory risk factors

**Operation ID**: `list_risk_factors_api_v1_risk_factors_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Risk Factors Api V1 Risk Factors Get`

---

### 🔵 `GET /api/v1/risk/factors`

**Summary**: List 7 mandatory risk factors

**Operation ID**: `list_risk_factors_api_v1_risk_factors_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Risk Factors Api V1 Risk Factors Get`

---

### 🔵 `GET /api/v1/risk/levels`

**Summary**: Get risk level thresholds

**Operation ID**: `get_risk_levels_api_v1_risk_levels_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Risk Levels Api V1 Risk Levels Get`

---

### 🔵 `GET /api/v1/risk/levels`

**Summary**: Get risk level thresholds

**Operation ID**: `get_risk_levels_api_v1_risk_levels_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Risk Levels Api V1 Risk Levels Get`

---

### 🔵 `GET /api/v1/risk/should-plan`

**Summary**: Quick check if planning is needed

**Operation ID**: `should_plan_api_v1_risk_should_plan_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `diff` | query | string | ✅ |
| `project_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/risk/should-plan`

**Summary**: Quick check if planning is needed

**Operation ID**: `should_plan_api_v1_risk_should_plan_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `diff` | query | string | ✅ |
| `project_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## SAST (14 endpoints)

### 🔵 `GET /api/v1/sast/health`

**Summary**: SAST health check

**Operation ID**: `sast_health_check_api_v1_sast_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Sast Health Check Api V1 Sast Health Get`

---

### 🔵 `GET /api/v1/sast/health`

**Summary**: SAST health check

**Operation ID**: `sast_health_check_api_v1_sast_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Sast Health Check Api V1 Sast Health Get`

---

### 🔵 `GET /api/v1/sast/projects/{project_id}/analytics`

**Summary**: Get SAST analytics

**Operation ID**: `get_sast_analytics_api_v1_sast_projects__project_id__analytics_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sast/projects/{project_id}/analytics`

**Summary**: Get SAST analytics

**Operation ID**: `get_sast_analytics_api_v1_sast_projects__project_id__analytics_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/sast/projects/{project_id}/scan`

**Summary**: Initiate SAST scan

**Operation ID**: `initiate_sast_scan_api_v1_sast_projects__project_id__scan_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/sast/projects/{project_id}/scan`

**Summary**: Initiate SAST scan

**Operation ID**: `initiate_sast_scan_api_v1_sast_projects__project_id__scan_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sast/projects/{project_id}/scans`

**Summary**: Get scan history

**Operation ID**: `get_scan_history_api_v1_sast_projects__project_id__scans_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sast/projects/{project_id}/scans`

**Summary**: Get scan history

**Operation ID**: `get_scan_history_api_v1_sast_projects__project_id__scans_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sast/projects/{project_id}/scans/{scan_id}`

**Summary**: Get scan details

**Operation ID**: `get_scan_details_api_v1_sast_projects__project_id__scans__scan_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `scan_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sast/projects/{project_id}/scans/{scan_id}`

**Summary**: Get scan details

**Operation ID**: `get_scan_details_api_v1_sast_projects__project_id__scans__scan_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `scan_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sast/projects/{project_id}/trend`

**Summary**: Get findings trend

**Operation ID**: `get_findings_trend_api_v1_sast_projects__project_id__trend_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sast/projects/{project_id}/trend`

**Summary**: Get findings trend

**Operation ID**: `get_findings_trend_api_v1_sast_projects__project_id__trend_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `days` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/sast/scan-snippet`

**Summary**: Scan code snippet

**Operation ID**: `scan_code_snippet_api_v1_sast_scan_snippet_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/sast/scan-snippet`

**Summary**: Scan code snippet

**Operation ID**: `scan_code_snippet_api_v1_sast_scan_snippet_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## SDLC Structure (6 endpoints)

### 🔵 `GET /api/v1/projects/{project_id}/compliance-summary`

**Summary**: Get compliance summary

**Operation ID**: `get_compliance_summary_api_v1_projects__project_id__compliance_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/compliance-summary`

**Summary**: Get compliance summary

**Operation ID**: `get_compliance_summary_api_v1_projects__project_id__compliance_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/validate-structure`

**Summary**: Validate SDLC 5.0.0 structure

**Operation ID**: `validate_structure_api_v1_projects__project_id__validate_structure_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **200**: Validation completed
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/validate-structure`

**Summary**: Validate SDLC 5.0.0 structure

**Operation ID**: `validate_structure_api_v1_projects__project_id__validate_structure_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **200**: Validation completed
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/validation-history`

**Summary**: Get validation history

**Operation ID**: `get_validation_history_api_v1_projects__project_id__validation_history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Validation History Api V1 Projects  Project Id  Validation History Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/validation-history`

**Summary**: Get validation history

**Operation ID**: `get_validation_history_api_v1_projects__project_id__validation_history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Validation History Api V1 Projects  Project Id  Validation History Get`
- **422**: Validation Error
  - Schema: `object`

---

## SOP Generator (16 endpoints)

### 🟢 `POST /api/v1/sop/generate`

**Summary**: Generate SOP from workflow description

**Operation ID**: `generate_sop_api_v1_sop_generate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/sop/generate`

**Summary**: Generate SOP from workflow description

**Operation ID**: `generate_sop_api_v1_sop_generate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sop/health`

**Summary**: SOP Generator health check

**Operation ID**: `health_check_api_v1_sop_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Sop Health Get`

---

### 🔵 `GET /api/v1/sop/health`

**Summary**: SOP Generator health check

**Operation ID**: `health_check_api_v1_sop_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Health Check Api V1 Sop Health Get`

---

### 🔵 `GET /api/v1/sop/list`

**Summary**: List generated SOPs

**Operation ID**: `list_sops_api_v1_sop_list_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sop_type` | query | string | ❌ |
| `status` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sop/list`

**Summary**: List generated SOPs

**Operation ID**: `list_sops_api_v1_sop_list_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sop_type` | query | string | ❌ |
| `status` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sop/types`

**Summary**: List supported SOP types

**Operation ID**: `get_sop_types_api_v1_sop_types_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Sop Types Api V1 Sop Types Get`

---

### 🔵 `GET /api/v1/sop/types`

**Summary**: List supported SOP types

**Operation ID**: `get_sop_types_api_v1_sop_types_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Sop Types Api V1 Sop Types Get`

---

### 🔵 `GET /api/v1/sop/{sop_id}`

**Summary**: Get SOP details

**Operation ID**: `get_sop_api_v1_sop__sop_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sop_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sop/{sop_id}`

**Summary**: Get SOP details

**Operation ID**: `get_sop_api_v1_sop__sop_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sop_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sop/{sop_id}/mrp`

**Summary**: Get MRP evidence for SOP

**Operation ID**: `get_sop_mrp_api_v1_sop__sop_id__mrp_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sop_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sop/{sop_id}/mrp`

**Summary**: Get MRP evidence for SOP

**Operation ID**: `get_sop_mrp_api_v1_sop__sop_id__mrp_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sop_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sop/{sop_id}/vcr`

**Summary**: Get VCR decision for SOP

**Operation ID**: `get_sop_vcr_api_v1_sop__sop_id__vcr_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sop_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/sop/{sop_id}/vcr`

**Summary**: Get VCR decision for SOP

**Operation ID**: `get_sop_vcr_api_v1_sop__sop_id__vcr_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sop_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/sop/{sop_id}/vcr`

**Summary**: Submit VCR decision for SOP

**Operation ID**: `submit_vcr_api_v1_sop__sop_id__vcr_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sop_id` | path | string | ✅ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/sop/{sop_id}/vcr`

**Summary**: Submit VCR decision for SOP

**Operation ID**: `submit_vcr_api_v1_sop__sop_id__vcr_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sop_id` | path | string | ✅ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Spec Converter (7 endpoints)

### 🟢 `POST /api/v1/spec-converter/convert`

**Summary**: Convert Specification

**Operation ID**: `convert_specification_api_v1_spec_converter_convert_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/spec-converter/detect`

**Summary**: Detect Format

**Operation ID**: `detect_format_api_v1_spec_converter_detect_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/spec-converter/import/jira`

**Summary**: Import From Jira

**Operation ID**: `import_from_jira_api_v1_spec_converter_import_jira_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/spec-converter/import/linear`

**Summary**: Import From Linear

**Operation ID**: `import_from_linear_api_v1_spec_converter_import_linear_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/spec-converter/import/text`

**Summary**: Import From Text

**Operation ID**: `import_from_text_api_v1_spec_converter_import_text_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/spec-converter/parse`

**Summary**: Parse Specification

**Operation ID**: `parse_specification_api_v1_spec_converter_parse_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/spec-converter/render`

**Summary**: Render Specification

**Operation ID**: `render_specification_api_v1_spec_converter_render_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Sprint 77 (3 endpoints)

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/burndown`

**Summary**: Get sprint burndown chart data

**Operation ID**: `get_sprint_burndown_api_v1_planning_sprints__sprint_id__burndown_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/forecast`

**Summary**: Get sprint completion forecast

**Operation ID**: `get_sprint_forecast_api_v1_planning_sprints__sprint_id__forecast_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/retrospective`

**Summary**: Get auto-generated sprint retrospective

**Operation ID**: `get_sprint_retrospective_api_v1_planning_sprints__sprint_id__retrospective_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Sprint 78 (39 endpoints)

### 🟢 `POST /api/v1/planning/action-items/bulk/status`

**Summary**: Bulk update action item status

**Operation ID**: `bulk_update_retro_action_item_status_api_v1_planning_action_items_bulk_status_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Bulk Update Retro Action Item Status Api V1 Planning Action Items Bulk Status Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/action-items/{item_id}`

**Summary**: Delete an action item

**Operation ID**: `delete_retro_action_item_api_v1_planning_action_items__item_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/action-items/{item_id}`

**Summary**: Get a single action item

**Operation ID**: `get_retro_action_item_api_v1_planning_action_items__item_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/action-items/{item_id}`

**Summary**: Update an action item

**Operation ID**: `update_retro_action_item_api_v1_planning_action_items__item_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `item_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/allocations`

**Summary**: Create resource allocation

**Operation ID**: `create_resource_allocation_api_v1_planning_allocations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/allocations/check-conflicts`

**Summary**: Check allocation conflicts

**Operation ID**: `check_allocation_conflicts_api_v1_planning_allocations_check_conflicts_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | query | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `allocation_percentage` | query | integer | ✅ |
| `exclude_sprint_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/allocations/{allocation_id}`

**Summary**: Delete a resource allocation

**Operation ID**: `delete_resource_allocation_api_v1_planning_allocations__allocation_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/allocations/{allocation_id}`

**Summary**: Get a resource allocation

**Operation ID**: `get_resource_allocation_api_v1_planning_allocations__allocation_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/allocations/{allocation_id}`

**Summary**: Update a resource allocation

**Operation ID**: `update_resource_allocation_api_v1_planning_allocations__allocation_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `allocation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies`

**Summary**: Create sprint dependency

**Operation ID**: `create_sprint_dependency_api_v1_planning_dependencies_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies/bulk/resolve`

**Summary**: Bulk resolve dependencies

**Operation ID**: `bulk_resolve_dependencies_api_v1_planning_dependencies_bulk_resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/dependencies/check-circular`

**Summary**: Check for circular dependency

**Operation ID**: `check_circular_dependency_api_v1_planning_dependencies_check_circular_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `source_sprint_id` | query | string | ✅ |
| `target_sprint_id` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Check Circular Dependency Api V1 Planning Dependencies Check Circular Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Delete a sprint dependency

**Operation ID**: `delete_sprint_dependency_api_v1_planning_dependencies__dependency_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Get a sprint dependency

**Operation ID**: `get_sprint_dependency_api_v1_planning_dependencies__dependency_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/dependencies/{dependency_id}`

**Summary**: Update a sprint dependency

**Operation ID**: `update_sprint_dependency_api_v1_planning_dependencies__dependency_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/dependencies/{dependency_id}/resolve`

**Summary**: Resolve a sprint dependency

**Operation ID**: `resolve_sprint_dependency_api_v1_planning_dependencies__dependency_id__resolve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `dependency_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/dependency-analysis`

**Summary**: Analyze project dependencies

**Operation ID**: `analyze_project_dependencies_api_v1_planning_projects__project_id__dependency_analysis_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/dependency-graph`

**Summary**: Get dependency graph for a project

**Operation ID**: `get_project_dependency_graph_api_v1_planning_projects__project_id__dependency_graph_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `include_cross_project` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/resource-heatmap`

**Summary**: Get resource allocation heatmap

**Operation ID**: `get_project_resource_heatmap_api_v1_planning_projects__project_id__resource_heatmap_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_ids` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/retrospective-comparison`

**Summary**: Compare retrospectives across sprints

**Operation ID**: `compare_sprint_retrospectives_api_v1_planning_projects__project_id__retrospective_comparison_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sprint_ids` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Compare Sprint Retrospectives Api V1 Planning Projects  Project Id  Retrospective Comparison Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/projects/{project_id}/template-suggestions`

**Summary**: Get template suggestions for project

**Operation ID**: `get_template_suggestions_api_v1_planning_projects__project_id__template_suggestions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `team_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/action-items`

**Summary**: List action items for a sprint

**Operation ID**: `list_retro_action_items_api_v1_planning_sprints__sprint_id__action_items_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `status` | query | string | ❌ |
| `category` | query | string | ❌ |
| `priority` | query | string | ❌ |
| `assignee_id` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/action-items`

**Summary**: Create action item from retrospective

**Operation ID**: `create_retro_action_item_api_v1_planning_sprints__sprint_id__action_items_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/sprints/{sprint_id}/action-items/bulk`

**Summary**: Bulk create action items

**Operation ID**: `bulk_create_retro_action_items_api_v1_planning_sprints__sprint_id__action_items_bulk_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `Response Bulk Create Retro Action Items Api V1 Planning Sprints  Sprint Id  Action Items Bulk Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/action-items/stats`

**Summary**: Get action items statistics

**Operation ID**: `get_retro_action_item_stats_api_v1_planning_sprints__sprint_id__action_items_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/allocations`

**Summary**: List allocations for a sprint

**Operation ID**: `list_sprint_allocations_api_v1_planning_sprints__sprint_id__allocations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/capacity`

**Summary**: Get sprint capacity

**Operation ID**: `get_sprint_capacity_api_v1_planning_sprints__sprint_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/sprints/{sprint_id}/dependencies`

**Summary**: List dependencies for a sprint

**Operation ID**: `list_sprint_dependencies_api_v1_planning_sprints__sprint_id__dependencies_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sprint_id` | path | string | ✅ |
| `direction` | query | string | ❌ |
| `include_resolved` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/teams/{team_id}/capacity`

**Summary**: Get team capacity

**Operation ID**: `get_team_capacity_api_v1_planning_teams__team_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates`

**Summary**: List sprint templates

**Operation ID**: `list_sprint_templates_api_v1_planning_templates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | query | string | ❌ |
| `template_type` | query | string | ❌ |
| `include_public` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates`

**Summary**: Create sprint template

**Operation ID**: `create_sprint_template_api_v1_planning_templates_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates/bulk/delete`

**Summary**: Bulk delete templates

**Operation ID**: `bulk_delete_templates_api_v1_planning_templates_bulk_delete_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates/default`

**Summary**: Get default template

**Operation ID**: `get_default_template_api_v1_planning_templates_default_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/templates/{template_id}`

**Summary**: Delete a sprint template

**Operation ID**: `delete_sprint_template_api_v1_planning_templates__template_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates/{template_id}`

**Summary**: Get a sprint template

**Operation ID**: `get_sprint_template_api_v1_planning_templates__template_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/templates/{template_id}`

**Summary**: Update a sprint template

**Operation ID**: `update_sprint_template_api_v1_planning_templates__template_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates/{template_id}/apply`

**Summary**: Apply template to create sprint

**Operation ID**: `apply_sprint_template_api_v1_planning_templates__template_id__apply_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/users/{user_id}/allocations`

**Summary**: List allocations for a user

**Operation ID**: `list_user_allocations_api_v1_planning_users__user_id__allocations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/users/{user_id}/capacity`

**Summary**: Get user capacity

**Operation ID**: `get_user_capacity_api_v1_planning_users__user_id__capacity_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `user_id` | path | string | ✅ |
| `start_date` | query | string | ✅ |
| `end_date` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Stage Gating (7 endpoints)

### 🟢 `POST /api/v1/stage-gating/advance`

**Summary**: Advance to next stage

**Operation ID**: `advance_stage_api_v1_stage_gating_advance_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/stage-gating/complete`

**Summary**: Mark stage as complete

**Operation ID**: `complete_stage_api_v1_stage_gating_complete_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/stage-gating/health`

**Summary**: Stage gating health check

**Operation ID**: `stage_gating_health_api_v1_stage_gating_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Stage Gating Health Api V1 Stage Gating Health Get`

---

### 🔵 `GET /api/v1/stage-gating/progress/{project_id}`

**Summary**: Get stage progress

**Operation ID**: `get_stage_progress_api_v1_stage_gating_progress__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/stage-gating/rules`

**Summary**: Get all stage rules

**Operation ID**: `get_all_rules_api_v1_stage_gating_rules_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/stage-gating/rules/{stage}`

**Summary**: Get rules for specific stage

**Operation ID**: `get_stage_rules_api_v1_stage_gating_rules__stage__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `stage` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/stage-gating/validate`

**Summary**: Validate PR against stage rules

**Operation ID**: `validate_pr_against_stage_api_v1_stage_gating_validate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Teams (10 endpoints)

### 🔵 `GET /api/v1/teams`

**Summary**: List Teams

**Operation ID**: `list_teams_api_v1_teams_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `organization_id` | query | string | ❌ |
| `skip` | query | integer | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/teams`

**Summary**: Create Team

**Operation ID**: `create_team_api_v1_teams_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/teams/{team_id}`

**Summary**: Delete Team

**Operation ID**: `delete_team_api_v1_teams__team_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/teams/{team_id}`

**Summary**: Get Team

**Operation ID**: `get_team_api_v1_teams__team_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/teams/{team_id}`

**Summary**: Update Team

**Operation ID**: `update_team_api_v1_teams__team_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/teams/{team_id}/members`

**Summary**: List Team Members

**Operation ID**: `list_team_members_api_v1_teams__team_id__members_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `skip` | query | integer | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/teams/{team_id}/members`

**Summary**: Add Team Member

**Operation ID**: `add_team_member_api_v1_teams__team_id__members_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/teams/{team_id}/members/{user_id}`

**Summary**: Remove Team Member

**Operation ID**: `remove_team_member_api_v1_teams__team_id__members__user_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `user_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/teams/{team_id}/members/{user_id}`

**Summary**: Update Member Role

**Operation ID**: `update_member_role_api_v1_teams__team_id__members__user_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `user_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/teams/{team_id}/stats`

**Summary**: Get Team Statistics

**Operation ID**: `get_team_statistics_api_v1_teams__team_id__stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Telemetry (12 endpoints)

### 🔵 `GET /api/v1/telemetry/dashboard`

**Summary**: Get Dashboard Metrics

**Operation ID**: `get_dashboard_metrics_api_v1_telemetry_dashboard_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/telemetry/dashboard`

**Summary**: Get Dashboard Metrics

**Operation ID**: `get_dashboard_metrics_api_v1_telemetry_dashboard_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/telemetry/events`

**Summary**: Track Event

**Operation ID**: `track_event_api_v1_telemetry_events_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/telemetry/events`

**Summary**: Track Event

**Operation ID**: `track_event_api_v1_telemetry_events_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/telemetry/events/batch`

**Summary**: Track Events Batch

**Operation ID**: `track_events_batch_api_v1_telemetry_events_batch_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/telemetry/events/batch`

**Summary**: Track Events Batch

**Operation ID**: `track_events_batch_api_v1_telemetry_events_batch_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/telemetry/funnels/{funnel_name}`

**Summary**: Get Funnel Metrics

**Operation ID**: `get_funnel_metrics_api_v1_telemetry_funnels__funnel_name__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `funnel_name` | path | string | ✅ |
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/telemetry/funnels/{funnel_name}`

**Summary**: Get Funnel Metrics

**Operation ID**: `get_funnel_metrics_api_v1_telemetry_funnels__funnel_name__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `funnel_name` | path | string | ✅ |
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/telemetry/health`

**Summary**: Telemetry Health

**Operation ID**: `telemetry_health_api_v1_telemetry_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Telemetry Health Api V1 Telemetry Health Get`

---

### 🔵 `GET /api/v1/telemetry/health`

**Summary**: Telemetry Health

**Operation ID**: `telemetry_health_api_v1_telemetry_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Telemetry Health Api V1 Telemetry Health Get`

---

### 🔵 `GET /api/v1/telemetry/interfaces`

**Summary**: Get Interface Breakdown

**Operation ID**: `get_interface_breakdown_api_v1_telemetry_interfaces_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/telemetry/interfaces`

**Summary**: Get Interface Breakdown

**Operation ID**: `get_interface_breakdown_api_v1_telemetry_interfaces_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `start_date` | query | string | ❌ |
| `end_date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Templates (9 endpoints)

### 🔵 `GET /api/v1/planning/projects/{project_id}/template-suggestions`

**Summary**: Get template suggestions for project

**Operation ID**: `get_template_suggestions_api_v1_planning_projects__project_id__template_suggestions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `team_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates`

**Summary**: List sprint templates

**Operation ID**: `list_sprint_templates_api_v1_planning_templates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | query | string | ❌ |
| `template_type` | query | string | ❌ |
| `include_public` | query | boolean | ❌ |
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates`

**Summary**: Create sprint template

**Operation ID**: `create_sprint_template_api_v1_planning_templates_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates/bulk/delete`

**Summary**: Bulk delete templates

**Operation ID**: `bulk_delete_templates_api_v1_planning_templates_bulk_delete_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates/default`

**Summary**: Get default template

**Operation ID**: `get_default_template_api_v1_planning_templates_default_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/planning/templates/{template_id}`

**Summary**: Delete a sprint template

**Operation ID**: `delete_sprint_template_api_v1_planning_templates__template_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/planning/templates/{template_id}`

**Summary**: Get a sprint template

**Operation ID**: `get_sprint_template_api_v1_planning_templates__template_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/planning/templates/{template_id}`

**Summary**: Update a sprint template

**Operation ID**: `update_sprint_template_api_v1_planning_templates__template_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/planning/templates/{template_id}/apply`

**Summary**: Apply template to create sprint

**Operation ID**: `apply_sprint_template_api_v1_planning_templates__template_id__apply_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `template_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Tier Management (5 endpoints)

### 🔵 `GET /api/v1/governance/tiers/`

**Summary**: List All Tiers

**Operation ID**: `list_tiers_api_v1_governance_tiers__get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Tiers Api V1 Governance Tiers  Get`

---

### 🔵 `GET /api/v1/governance/tiers/health`

**Summary**: Tier management health check

**Operation ID**: `tiers_health_api_v1_governance_tiers_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Tiers Health Api V1 Governance Tiers Health Get`

---

### 🔵 `GET /api/v1/governance/tiers/{project_id}`

**Summary**: Get Project Tier

**Operation ID**: `get_project_tier_api_v1_governance_tiers__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/governance/tiers/{project_id}/upgrade`

**Summary**: Request Tier Upgrade

**Operation ID**: `request_tier_upgrade_api_v1_governance_tiers__project_id__upgrade_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/governance/tiers/{tier}/requirements`

**Summary**: Get Tier Requirements

**Operation ID**: `get_tier_requirements_api_v1_governance_tiers__tier__requirements_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `tier` | path | string | ✅ |
| `category` | query | string | ❌ |
| `mandatory_only` | query | boolean | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Triage (12 endpoints)

### 🟢 `POST /api/v1/triage/analyze`

**Summary**: Analyze For Triage

**Operation ID**: `analyze_for_triage_api_v1_triage_analyze_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/triage/analyze`

**Summary**: Analyze For Triage

**Operation ID**: `analyze_for_triage_api_v1_triage_analyze_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/triage/sla-breaches`

**Summary**: Get Sla Breaches

**Operation ID**: `get_sla_breaches_api_v1_triage_sla_breaches_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Sla Breaches Api V1 Triage Sla Breaches Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/triage/sla-breaches`

**Summary**: Get Sla Breaches

**Operation ID**: `get_sla_breaches_api_v1_triage_sla_breaches_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Sla Breaches Api V1 Triage Sla Breaches Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/triage/stats`

**Summary**: Get Triage Statistics

**Operation ID**: `get_triage_statistics_api_v1_triage_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/triage/stats`

**Summary**: Get Triage Statistics

**Operation ID**: `get_triage_statistics_api_v1_triage_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/triage/{feedback_id}/apply`

**Summary**: Apply Triage Decision

**Operation ID**: `apply_triage_decision_api_v1_triage__feedback_id__apply_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Apply Triage Decision Api V1 Triage  Feedback Id  Apply Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/triage/{feedback_id}/apply`

**Summary**: Apply Triage Decision

**Operation ID**: `apply_triage_decision_api_v1_triage__feedback_id__apply_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Apply Triage Decision Api V1 Triage  Feedback Id  Apply Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/triage/{feedback_id}/auto-triage`

**Summary**: Auto Triage Feedback

**Operation ID**: `auto_triage_feedback_api_v1_triage__feedback_id__auto_triage_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/triage/{feedback_id}/auto-triage`

**Summary**: Auto Triage Feedback

**Operation ID**: `auto_triage_feedback_api_v1_triage__feedback_id__auto_triage_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/triage/{feedback_id}/sla`

**Summary**: Get Sla Status

**Operation ID**: `get_sla_status_api_v1_triage__feedback_id__sla_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/triage/{feedback_id}/sla`

**Summary**: Get Sla Status

**Operation ID**: `get_sla_status_api_v1_triage__feedback_id__sla_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `feedback_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Uncategorized (4 endpoints)

### 🔵 `GET /`

**Summary**: Root

**Operation ID**: `root__get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /health`

**Summary**: Health Check

**Operation ID**: `health_check_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /health/ready`

**Summary**: Readiness Check

**Operation ID**: `readiness_check_health_ready_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /metrics`

**Summary**: Metrics

**Operation ID**: `metrics_metrics_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

## VCR (Version Controlled Resolution) (22 endpoints)

### 🔵 `GET /api/v1/vcr`

**Summary**: List VCRs

**Operation ID**: `list_vcrs_api_v1_vcr_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `status` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/vcr`

**Summary**: List VCRs

**Operation ID**: `list_vcrs_api_v1_vcr_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ❌ |
| `status` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vcr`

**Summary**: Create VCR

**Operation ID**: `create_vcr_api_v1_vcr_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vcr`

**Summary**: Create VCR

**Operation ID**: `create_vcr_api_v1_vcr_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vcr/auto-generate`

**Summary**: AI-assisted VCR generation

**Operation ID**: `auto_generate_vcr_api_v1_vcr_auto_generate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vcr/auto-generate`

**Summary**: AI-assisted VCR generation

**Operation ID**: `auto_generate_vcr_api_v1_vcr_auto_generate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/vcr/stats/{project_id}`

**Summary**: Get VCR statistics

**Operation ID**: `get_vcr_stats_api_v1_vcr_stats__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/vcr/stats/{project_id}`

**Summary**: Get VCR statistics

**Operation ID**: `get_vcr_stats_api_v1_vcr_stats__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/vcr/{vcr_id}`

**Summary**: Delete VCR

**Operation ID**: `delete_vcr_api_v1_vcr__vcr_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/vcr/{vcr_id}`

**Summary**: Delete VCR

**Operation ID**: `delete_vcr_api_v1_vcr__vcr_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/vcr/{vcr_id}`

**Summary**: Get VCR

**Operation ID**: `get_vcr_api_v1_vcr__vcr_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/vcr/{vcr_id}`

**Summary**: Get VCR

**Operation ID**: `get_vcr_api_v1_vcr__vcr_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/vcr/{vcr_id}`

**Summary**: Update VCR

**Operation ID**: `update_vcr_api_v1_vcr__vcr_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/vcr/{vcr_id}`

**Summary**: Update VCR

**Operation ID**: `update_vcr_api_v1_vcr__vcr_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vcr/{vcr_id}/approve`

**Summary**: Approve VCR

**Operation ID**: `approve_vcr_api_v1_vcr__vcr_id__approve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vcr/{vcr_id}/approve`

**Summary**: Approve VCR

**Operation ID**: `approve_vcr_api_v1_vcr__vcr_id__approve_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vcr/{vcr_id}/reject`

**Summary**: Reject VCR

**Operation ID**: `reject_vcr_api_v1_vcr__vcr_id__reject_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vcr/{vcr_id}/reject`

**Summary**: Reject VCR

**Operation ID**: `reject_vcr_api_v1_vcr__vcr_id__reject_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vcr/{vcr_id}/reopen`

**Summary**: Reopen rejected VCR

**Operation ID**: `reopen_vcr_api_v1_vcr__vcr_id__reopen_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vcr/{vcr_id}/reopen`

**Summary**: Reopen rejected VCR

**Operation ID**: `reopen_vcr_api_v1_vcr__vcr_id__reopen_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vcr/{vcr_id}/submit`

**Summary**: Submit VCR for approval

**Operation ID**: `submit_vcr_api_v1_vcr__vcr_id__submit_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vcr/{vcr_id}/submit`

**Summary**: Submit VCR for approval

**Operation ID**: `submit_vcr_api_v1_vcr__vcr_id__submit_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vcr_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## Vibecoding Index (7 endpoints)

### 🟢 `POST /api/v1/vibecoding/batch`

**Summary**: Batch calculate Vibecoding Index

**Operation ID**: `batch_calculate_index_api_v1_vibecoding_batch_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vibecoding/calculate`

**Summary**: Calculate Vibecoding Index

**Operation ID**: `calculate_vibecoding_index_api_v1_vibecoding_calculate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/vibecoding/calibrate`

**Summary**: Submit calibration feedback

**Operation ID**: `submit_calibration_api_v1_vibecoding_calibrate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/vibecoding/health`

**Summary**: Signals engine health check

**Operation ID**: `signals_health_api_v1_vibecoding_health_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Signals Health Api V1 Vibecoding Health Get`

---

### 🔵 `GET /api/v1/vibecoding/stats`

**Summary**: Get index statistics

**Operation ID**: `get_stats_api_v1_vibecoding_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `days` | query | integer | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/vibecoding/thresholds`

**Summary**: Get index thresholds

**Operation ID**: `get_thresholds_api_v1_vibecoding_thresholds_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/vibecoding/{submission_id}`

**Summary**: Get cached Vibecoding Index

**Operation ID**: `get_vibecoding_index_api_v1_vibecoding__submission_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `submission_id` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## WebSocket (2 endpoints)

### 🟢 `POST /ws/broadcast/project/{project_id}`

**Summary**: Broadcast To Project

**Operation ID**: `broadcast_to_project_ws_broadcast_project__project_id__post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `event_type` | query | string | ✅ |

**Request Body** (Required: ❌):
- Schema: `Payload`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /ws/stats`

**Summary**: Get Websocket Stats

**Operation ID**: `get_websocket_stats_ws_stats_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

## dashboard (2 endpoints)

### 🔵 `GET /api/v1/dashboard/recent-gates`

**Summary**: Get Recent Gates

**Operation ID**: `get_recent_gates_api_v1_dashboard_recent_gates_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dashboard/stats`

**Summary**: Get Dashboard Stats

**Operation ID**: `get_dashboard_stats_api_v1_dashboard_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## doc-cross-reference (4 endpoints)

### 🔵 `GET /api/v1/doc-cross-reference/links`

**Summary**: Get document links

**Operation ID**: `get_document_links_api_v1_doc_cross_reference_links_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `document_path` | query | string | ✅ |
| `project_path` | query | string | ❌ |
| `direction` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/doc-cross-reference/orphaned`

**Summary**: Get orphaned documents

**Operation ID**: `get_orphaned_documents_api_v1_doc_cross_reference_orphaned_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | query | string | ✅ |
| `project_path` | query | string | ❌ |
| `document_type` | query | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/doc-cross-reference/validate`

**Summary**: Validate single document

**Operation ID**: `validate_document_api_v1_doc_cross_reference_validate_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/doc-cross-reference/validate-project`

**Summary**: Validate entire project

**Operation ID**: `validate_project_api_v1_doc_cross_reference_validate_project_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## dogfooding (20 endpoints)

### 🔵 `GET /api/v1/dogfooding/ceo-time/entries`

**Summary**: List Ceo Time Entries

**Operation ID**: `list_ceo_time_entries_api_v1_dogfooding_ceo_time_entries_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `activity_type` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/dogfooding/ceo-time/record`

**Summary**: Record Ceo Time

**Operation ID**: `record_ceo_time_api_v1_dogfooding_ceo_time_record_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/ceo-time/summary`

**Summary**: Get Ceo Time Summary

**Operation ID**: `get_ceo_time_summary_api_v1_dogfooding_ceo_time_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/daily-checks`

**Summary**: Run Daily Checks

**Operation ID**: `run_daily_checks_api_v1_dogfooding_daily_checks_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/daily-checks/history`

**Summary**: Get Daily Checks History

**Operation ID**: `get_daily_checks_history_api_v1_dogfooding_daily_checks_history_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/dogfooding/enforce/soft`

**Summary**: Enforce Soft Mode

**Operation ID**: `enforce_soft_mode_api_v1_dogfooding_enforce_soft_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/enforce/soft/log`

**Summary**: Get Soft Enforcement Log

**Operation ID**: `get_soft_enforcement_log_api_v1_dogfooding_enforce_soft_log_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `action_filter` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/dogfooding/enforce/soft/override`

**Summary**: Request Cto Override

**Operation ID**: `request_cto_override_api_v1_dogfooding_enforce_soft_override_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `pr_number` | query | integer | ✅ |
| `reason` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/enforce/soft/status`

**Summary**: Get Soft Mode Status

**Operation ID**: `get_soft_mode_status_api_v1_dogfooding_enforce_soft_status_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/export/json`

**Summary**: Export Json Metrics

**Operation ID**: `export_json_metrics_api_v1_dogfooding_export_json_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/export/prometheus`

**Summary**: Export Prometheus Metrics

**Operation ID**: `export_prometheus_metrics_api_v1_dogfooding_export_prometheus_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

### 🟢 `POST /api/v1/dogfooding/feedback`

**Summary**: Submit Developer Feedback

**Operation ID**: `submit_developer_feedback_api_v1_dogfooding_feedback_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/feedback/list`

**Summary**: List Developer Feedback

**Operation ID**: `list_developer_feedback_api_v1_dogfooding_feedback_list_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/feedback/summary`

**Summary**: Get Feedback Summary

**Operation ID**: `get_feedback_summary_api_v1_dogfooding_feedback_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/go-no-go`

**Summary**: Get Go No Go Decision

**Operation ID**: `get_go_no_go_decision_api_v1_dogfooding_go_no_go_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/metrics`

**Summary**: Get Dogfooding Metrics

**Operation ID**: `get_dogfooding_metrics_api_v1_dogfooding_metrics_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/prs`

**Summary**: Get Pr Metrics

**Operation ID**: `get_pr_metrics_api_v1_dogfooding_prs_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `page` | query | integer | ❌ |
| `page_size` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/dogfooding/prs/record`

**Summary**: Record Pr Metric

**Operation ID**: `record_pr_metric_api_v1_dogfooding_prs_record_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/dogfooding/report-false-positive`

**Summary**: Report False Positive

**Operation ID**: `report_false_positive_api_v1_dogfooding_report_false_positive_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `pr_number` | query | integer | ✅ |
| `reason` | query | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/dogfooding/status`

**Summary**: Get Dogfooding Status

**Operation ID**: `get_dogfooding_status_api_v1_dogfooding_status_get`

**Responses**:

- **200**: Successful Response
  - Schema: `object`

---

## github (13 endpoints)

### 🔵 `GET /api/v1/api/v1/github/installations`

**Summary**: List user's GitHub installations

**Operation ID**: `list_installations_api_v1_api_v1_github_installations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/github/installations/{installation_id}/repositories`

**Summary**: List repositories for installation

**Operation ID**: `list_installation_repositories_api_v1_api_v1_github_installations__installation_id__repositories_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `installation_id` | path | string | ✅ |
| `page` | query | integer | ❌ |
| `per_page` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/github/projects/{project_id}/clone`

**Summary**: Clone linked repository

**Operation ID**: `clone_repository_api_v1_api_v1_github_projects__project_id__clone_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ❌):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/github/projects/{project_id}/link`

**Summary**: Link GitHub repository to project

**Operation ID**: `link_repository_api_v1_api_v1_github_projects__project_id__link_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/github/projects/{project_id}/repository`

**Summary**: Get linked repository for project

**Operation ID**: `get_project_repository_api_v1_api_v1_github_projects__project_id__repository_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/github/projects/{project_id}/scan`

**Summary**: Scan cloned repository

**Operation ID**: `scan_repository_api_v1_api_v1_github_projects__project_id__scan_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/api/v1/github/projects/{project_id}/unlink`

**Summary**: Unlink GitHub repository from project

**Operation ID**: `unlink_repository_api_v1_api_v1_github_projects__project_id__unlink_delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/github/webhooks`

**Summary**: GitHub webhook handler

**Operation ID**: `handle_webhook_api_v1_api_v1_github_webhooks_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `X-GitHub-Event` | header | string | ❌ |
| `X-Hub-Signature-256` | header | string | ❌ |
| `X-GitHub-Delivery` | header | string | ❌ |

**Responses**:

- **202**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/github/webhooks/dlq`

**Summary**: Get dead letter queue jobs

**Operation ID**: `get_dlq_jobs_api_v1_api_v1_github_webhooks_dlq_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/github/webhooks/dlq/{job_id}/retry`

**Summary**: Retry a dead letter queue job

**Operation ID**: `retry_dlq_job_api_v1_api_v1_github_webhooks_dlq__job_id__retry_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `job_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/github/webhooks/jobs/{job_id}`

**Summary**: Get webhook job status

**Operation ID**: `get_webhook_job_status_api_v1_api_v1_github_webhooks_jobs__job_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `job_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/github/webhooks/process`

**Summary**: Trigger webhook job processing

**Operation ID**: `trigger_webhook_processing_api_v1_api_v1_github_webhooks_process_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `max_jobs` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/github/webhooks/stats`

**Summary**: Get webhook job queue statistics

**Operation ID**: `get_webhook_stats_api_v1_api_v1_github_webhooks_stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## organization-invitations (7 endpoints)

### 🔴 `DELETE /api/v1/api/v1/org-invitations/{invitation_id}`

**Summary**: Cancel organization invitation

**Operation ID**: `cancel_invitation_api_v1_api_v1_org_invitations__invitation_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `invitation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/org-invitations/{invitation_id}/resend`

**Summary**: Resend organization invitation email

**Operation ID**: `resend_invitation_api_v1_api_v1_org_invitations__invitation_id__resend_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `invitation_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/org-invitations/{token}`

**Summary**: Get organization invitation details by token

**Operation ID**: `get_invitation_by_token_api_v1_api_v1_org_invitations__token__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `token` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/org-invitations/{token}/accept`

**Summary**: Accept organization invitation

**Operation ID**: `accept_invitation_api_v1_api_v1_org_invitations__token__accept_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `token` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/org-invitations/{token}/decline`

**Summary**: Decline organization invitation

**Operation ID**: `decline_invitation_api_v1_api_v1_org_invitations__token__decline_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `token` | path | string | ✅ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/api/v1/organizations/{organization_id}/invitations`

**Summary**: List organization invitations

**Operation ID**: `list_org_invitations_api_v1_api_v1_organizations__organization_id__invitations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `organization_id` | path | string | ✅ |
| `status` | query | string | ❌ |
| `email` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `offset` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Org Invitations Api V1 Api V1 Organizations  Organization Id  Invitations Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/api/v1/organizations/{organization_id}/invitations`

**Summary**: Send organization invitation

**Operation ID**: `send_invitation_api_v1_api_v1_organizations__organization_id__invitations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `organization_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## organizations (6 endpoints)

### 🔵 `GET /api/v1/organizations`

**Summary**: List Organizations

**Operation ID**: `list_organizations_api_v1_organizations_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `skip` | query | integer | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/organizations`

**Summary**: Create Organization

**Operation ID**: `create_organization_api_v1_organizations_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/organizations/{org_id}`

**Summary**: Get Organization

**Operation ID**: `get_organization_api_v1_organizations__org_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `org_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/organizations/{org_id}`

**Summary**: Update Organization

**Operation ID**: `update_organization_api_v1_organizations__org_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `org_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/organizations/{org_id}/members`

**Summary**: Add Member Directly

**Operation ID**: `add_member_directly_api_v1_organizations__org_id__members_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `org_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/organizations/{org_id}/stats`

**Summary**: Get Organization Statistics

**Operation ID**: `get_organization_statistics_api_v1_organizations__org_id__stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `org_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## payments (5 endpoints)

### 🔵 `GET /api/v1/payments/subscriptions/me`

**Summary**: Get My Subscription

**Operation ID**: `get_my_subscription_api_v1_payments_subscriptions_me_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/payments/vnpay/create`

**Summary**: Create Vnpay Payment

**Operation ID**: `create_vnpay_payment_api_v1_payments_vnpay_create_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/payments/vnpay/ipn`

**Summary**: Vnpay Ipn Handler

**Operation ID**: `vnpay_ipn_handler_api_v1_payments_vnpay_ipn_post`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Vnpay Ipn Handler Api V1 Payments Vnpay Ipn Post`

---

### 🔵 `GET /api/v1/payments/vnpay/return`

**Summary**: Vnpay Return Handler

**Operation ID**: `vnpay_return_handler_api_v1_payments_vnpay_return_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Vnpay Return Handler Api V1 Payments Vnpay Return Get`

---

### 🔵 `GET /api/v1/payments/{vnp_txn_ref}`

**Summary**: Get Payment Status

**Operation ID**: `get_payment_status_api_v1_payments__vnp_txn_ref__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `vnp_txn_ref` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## pilot (13 endpoints)

### 🟢 `POST /api/v1/pilot/feedback`

**Summary**: Submit satisfaction survey

**Operation ID**: `submit_feedback_api_v1_pilot_feedback_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/pilot/metrics/aggregate`

**Summary**: Trigger daily metrics aggregation

**Operation ID**: `aggregate_metrics_api_v1_pilot_metrics_aggregate_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `date` | query | string | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Aggregate Metrics Api V1 Pilot Metrics Aggregate Post`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/pilot/metrics/summary`

**Summary**: Get pilot program summary

**Operation ID**: `get_metrics_summary_api_v1_pilot_metrics_summary_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/pilot/metrics/targets`

**Summary**: Get Sprint 49 targets

**Operation ID**: `get_targets_api_v1_pilot_metrics_targets_get`

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get Targets Api V1 Pilot Metrics Targets Get`

---

### 🔵 `GET /api/v1/pilot/participants`

**Summary**: List pilot participants

**Operation ID**: `list_participants_api_v1_pilot_participants_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `status` | query | string | ❌ |
| `domain` | query | string | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response List Participants Api V1 Pilot Participants Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/pilot/participants`

**Summary**: Register as pilot participant

**Operation ID**: `register_participant_api_v1_pilot_participants_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/pilot/participants/me`

**Summary**: Get current user's participant profile

**Operation ID**: `get_my_participant_profile_api_v1_pilot_participants_me_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/pilot/participants/{participant_id}`

**Summary**: Get participant by ID

**Operation ID**: `get_participant_api_v1_pilot_participants__participant_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `participant_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/pilot/sessions`

**Summary**: Get my sessions

**Operation ID**: `get_my_sessions_api_v1_pilot_sessions_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `Response Get My Sessions Api V1 Pilot Sessions Get`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/pilot/sessions`

**Summary**: Start pilot session (TTFV timer begins)

**Operation ID**: `start_session_api_v1_pilot_sessions_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/pilot/sessions/{session_id}`

**Summary**: Get session details

**Operation ID**: `get_session_api_v1_pilot_sessions__session_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/pilot/sessions/{session_id}/generation`

**Summary**: Record generation results

**Operation ID**: `record_generation_api_v1_pilot_sessions__session_id__generation_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/pilot/sessions/{session_id}/stage`

**Summary**: Update session stage

**Operation ID**: `update_session_stage_api_v1_pilot_sessions__session_id__stage_patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `session_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## projects (10 endpoints)

### 🔵 `GET /api/v1/projects`

**Summary**: List Projects

**Operation ID**: `list_projects_api_v1_projects_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `skip` | query | integer | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects`

**Summary**: Create Project

**Operation ID**: `create_project_api_v1_projects_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/init`

**Summary**: Initialize SDLC project

**Operation ID**: `init_project_api_v1_projects_init_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/projects/{project_id}`

**Summary**: Delete Project

**Operation ID**: `delete_project_api_v1_projects__project_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}`

**Summary**: Get Project

**Operation ID**: `get_project_api_v1_projects__project_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/projects/{project_id}`

**Summary**: Update Project

**Operation ID**: `update_project_api_v1_projects__project_id__put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/projects/{project_id}/context`

**Summary**: Get project context (stage, gate, sprint)

**Operation ID**: `get_project_context_api_v1_projects__project_id__context_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟡 `PUT /api/v1/projects/{project_id}/context`

**Summary**: Update project context (stage, gate, sprint)

**Operation ID**: `update_project_context_api_v1_projects__project_id__context_put`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/migrate-stages`

**Summary**: Migrate project stages to SDLC 5.0.0

**Operation ID**: `migrate_stages_api_v1_projects__project_id__migrate_stages_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/projects/{project_id}/sync`

**Summary**: Sync project metadata from repository files

**Operation ID**: `sync_project_metadata_api_v1_projects__project_id__sync_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `project_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## spec-converter (7 endpoints)

### 🟢 `POST /api/v1/spec-converter/convert`

**Summary**: Convert Specification

**Operation ID**: `convert_specification_api_v1_spec_converter_convert_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/spec-converter/detect`

**Summary**: Detect Format

**Operation ID**: `detect_format_api_v1_spec_converter_detect_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/spec-converter/import/jira`

**Summary**: Import From Jira

**Operation ID**: `import_from_jira_api_v1_spec_converter_import_jira_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/spec-converter/import/linear`

**Summary**: Import From Linear

**Operation ID**: `import_from_linear_api_v1_spec_converter_import_linear_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/spec-converter/import/text`

**Summary**: Import From Text

**Operation ID**: `import_from_text_api_v1_spec_converter_import_text_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/spec-converter/parse`

**Summary**: Parse Specification

**Operation ID**: `parse_specification_api_v1_spec_converter_parse_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/spec-converter/render`

**Summary**: Render Specification

**Operation ID**: `render_specification_api_v1_spec_converter_render_post`

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

## teams (10 endpoints)

### 🔵 `GET /api/v1/teams`

**Summary**: List Teams

**Operation ID**: `list_teams_api_v1_teams_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `organization_id` | query | string | ❌ |
| `skip` | query | integer | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/teams`

**Summary**: Create Team

**Operation ID**: `create_team_api_v1_teams_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/teams/{team_id}`

**Summary**: Delete Team

**Operation ID**: `delete_team_api_v1_teams__team_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/teams/{team_id}`

**Summary**: Get Team

**Operation ID**: `get_team_api_v1_teams__team_id__get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/teams/{team_id}`

**Summary**: Update Team

**Operation ID**: `update_team_api_v1_teams__team_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/teams/{team_id}/members`

**Summary**: List Team Members

**Operation ID**: `list_team_members_api_v1_teams__team_id__members_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `skip` | query | integer | ❌ |
| `limit` | query | integer | ❌ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🟢 `POST /api/v1/teams/{team_id}/members`

**Summary**: Add Team Member

**Operation ID**: `add_team_member_api_v1_teams__team_id__members_post`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **201**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔴 `DELETE /api/v1/teams/{team_id}/members/{user_id}`

**Summary**: Remove Team Member

**Operation ID**: `remove_team_member_api_v1_teams__team_id__members__user_id__delete`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `user_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **422**: Validation Error
  - Schema: `object`

---

### 🟠 `PATCH /api/v1/teams/{team_id}/members/{user_id}`

**Summary**: Update Member Role

**Operation ID**: `update_member_role_api_v1_teams__team_id__members__user_id__patch`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `user_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Request Body** (Required: ✅):
- Schema: `object`

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

### 🔵 `GET /api/v1/teams/{team_id}/stats`

**Summary**: Get Team Statistics

**Operation ID**: `get_team_statistics_api_v1_teams__team_id__stats_get`

**Parameters**:

| Name | In | Type | Required |
|------|-------|------|----------|
| `team_id` | path | string | ✅ |
| `sdlc_access_token` | cookie | string | ❌ |

**Responses**:

- **200**: Successful Response
  - Schema: `object`
- **422**: Validation Error
  - Schema: `object`

---

