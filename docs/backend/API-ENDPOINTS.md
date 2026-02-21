# API Endpoints Testing Report

**Generated**: 2026-02-21 13:33:04
**Base URL**: http://localhost:8300
**Total Endpoints Tested**: 636

---

## 📊 Test Statistics

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total Tested** | 636 | 100% |
| ✅ Success (2xx) | 52 | 8.2% |
| 🔒 Auth Required (401) | 488 | 76.7% |
| ❌ Not Found (404) | 8 | 1.3% |
| ⚠️ Client Error (4xx) | 69 | 10.8% |
| 🔥 Server Error (5xx) | 8 | 1.3% |

---

## 📋 Detailed Test Results

| # | Service | Method | Endpoint | Status | Root Cause |
|---|---------|--------|----------|--------|------------|
| 1 | unknown | GET | `/` | SUCCESS | ✅ Success - 200 |
| 2 | admin | GET | `/api/v1/admin/ai-providers/config` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 3 | admin | POST | `/api/v1/admin/ai-providers/ollama/refresh-models` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 4 | admin | PATCH | `/api/v1/admin/ai-providers/{provider}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 5 | admin | GET | `/api/v1/admin/ai-providers/{provider}/models` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 6 | admin | POST | `/api/v1/admin/ai-providers/{provider}/test` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 7 | admin | GET | `/api/v1/admin/audit-logs` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 8 | admin | POST | `/api/v1/admin/evidence/retention-archive` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 9 | admin | POST | `/api/v1/admin/evidence/retention-purge` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 10 | admin | GET | `/api/v1/admin/evidence/retention-stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 11 | admin | GET | `/api/v1/admin/override-queue` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 12 | admin | GET | `/api/v1/admin/override-stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 13 | admin | GET | `/api/v1/admin/settings` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 14 | admin | GET | `/api/v1/admin/settings/{key}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 15 | admin | PATCH | `/api/v1/admin/settings/{key}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 16 | admin | POST | `/api/v1/admin/settings/{key}/rollback` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 17 | admin | GET | `/api/v1/admin/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 18 | admin | GET | `/api/v1/admin/system/health` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 19 | admin | GET | `/api/v1/admin/users` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 20 | admin | POST | `/api/v1/admin/users` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 21 | admin | DELETE | `/api/v1/admin/users/bulk` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 22 | admin | POST | `/api/v1/admin/users/bulk` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 23 | admin | DELETE | `/api/v1/admin/users/{user_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 24 | admin | GET | `/api/v1/admin/users/{user_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 25 | admin | PATCH | `/api/v1/admin/users/{user_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 26 | admin | POST | `/api/v1/admin/users/{user_id}/mfa-exempt` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 27 | admin | GET | `/api/v1/admin/users/{user_id}/mfa-status` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 28 | admin | DELETE | `/api/v1/admin/users/{user_id}/permanent` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 29 | admin | POST | `/api/v1/admin/users/{user_id}/restore` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 30 | admin | POST | `/api/v1/admin/users/{user_id}/unlock` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 31 | agent-team | GET | `/api/v1/agent-team/conversations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 32 | agent-team | POST | `/api/v1/agent-team/conversations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 33 | agent-team | GET | `/api/v1/agent-team/conversations/{conversation_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 34 | agent-team | POST | `/api/v1/agent-team/conversations/{conversation_id}/interrupt` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 35 | agent-team | GET | `/api/v1/agent-team/conversations/{conversation_id}/messages` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 36 | agent-team | POST | `/api/v1/agent-team/conversations/{conversation_id}/messages` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 37 | agent-team | GET | `/api/v1/agent-team/definitions` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 38 | agent-team | POST | `/api/v1/agent-team/definitions` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 39 | agent-team | GET | `/api/v1/agent-team/definitions/{definition_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 40 | agent-team | PUT | `/api/v1/agent-team/definitions/{definition_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 41 | agents-md | GET | `/api/v1/agents-md/context/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 42 | agents-md | GET | `/api/v1/agents-md/context/{project_id}/history` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 43 | agents-md | POST | `/api/v1/agents-md/generate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 44 | agents-md | POST | `/api/v1/agents-md/lint` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 45 | agents-md | GET | `/api/v1/agents-md/repos` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 46 | agents-md | POST | `/api/v1/agents-md/validate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 47 | agents-md | GET | `/api/v1/agents-md/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 48 | agents-md | GET | `/api/v1/agents-md/{project_id}/history` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 49 | ai-detection | POST | `/api/v1/ai-detection/analyze` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'pr_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'title'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 50 | ai-detection | GET | `/api/v1/ai-detection/circuit-breakers` | SUCCESS | ✅ Success - 200 |
| 51 | ai-detection | POST | `/api/v1/ai-detection/circuit-breakers/{breaker_name}/reset` | NOT_FOUND | ❌ Endpoint not found - /api/v1/ai-detection/circuit-breakers/{breaker_name}/reset may not be implemented |
| 52 | ai-detection | GET | `/api/v1/ai-detection/shadow-mode` | SUCCESS | ✅ Success - 200 |
| 53 | ai-detection | GET | `/api/v1/ai-detection/status` | SUCCESS | ✅ Success - 200 |
| 54 | ai-detection | GET | `/api/v1/ai-detection/tools` | SUCCESS | ✅ Success - 200 |
| 55 | analytics | GET | `/api/v1/analytics/circuit-breaker/status` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 56 | analytics | GET | `/api/v1/analytics/engagement` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 57 | analytics | POST | `/api/v1/analytics/events` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 58 | analytics | POST | `/api/v1/analytics/events/feature` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 59 | analytics | POST | `/api/v1/analytics/events/page-view` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 60 | analytics | GET | `/api/v1/analytics/features` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 61 | analytics | GET | `/api/v1/analytics/my-activity` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 62 | analytics | GET | `/api/v1/analytics/pilot-metrics` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 63 | analytics | POST | `/api/v1/analytics/pilot-metrics/calculate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 64 | analytics | POST | `/api/v1/analytics/retention/cleanup` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 65 | analytics | GET | `/api/v1/analytics/retention/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 66 | analytics | GET | `/api/v1/analytics/sessions/active` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 67 | analytics | POST | `/api/v1/analytics/sessions/start` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 68 | analytics | POST | `/api/v1/analytics/sessions/{session_id}/end` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 69 | analytics | GET | `/api/v1/analytics/summary` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 70 | analytics | POST | `/api/v1/analytics/v2/events` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 71 | analytics | POST | `/api/v1/analytics/v2/events/batch` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 72 | analytics | GET | `/api/v1/analytics/v2/metrics/ai-safety` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 73 | analytics | GET | `/api/v1/analytics/v2/metrics/dau` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 74 | api-keys | GET | `/api/v1/api-keys` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 75 | api-keys | POST | `/api/v1/api-keys` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 76 | api-keys | DELETE | `/api/v1/api-keys/{key_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 77 | api | GET | `/api/v1/api/v1/github/installations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 78 | api | GET | `/api/v1/api/v1/github/installations/{installation_id}/repositories` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 79 | api | POST | `/api/v1/api/v1/github/projects/{project_id}/clone` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 80 | api | POST | `/api/v1/api/v1/github/projects/{project_id}/link` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 81 | api | GET | `/api/v1/api/v1/github/projects/{project_id}/repository` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 82 | api | GET | `/api/v1/api/v1/github/projects/{project_id}/scan` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 83 | api | DELETE | `/api/v1/api/v1/github/projects/{project_id}/unlink` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 84 | api | POST | `/api/v1/api/v1/github/webhooks` | SERVER_ERROR | 🔥 Server error - 500: {'error': 'webhook_not_configured', 'message': 'GITHUB_APP_WEBHOOK_SECRET not set'} |
| 85 | api | GET | `/api/v1/api/v1/github/webhooks/dlq` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 86 | api | POST | `/api/v1/api/v1/github/webhooks/dlq/{job_id}/retry` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 87 | api | GET | `/api/v1/api/v1/github/webhooks/jobs/{job_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 88 | api | POST | `/api/v1/api/v1/github/webhooks/process` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 89 | api | GET | `/api/v1/api/v1/github/webhooks/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 90 | api | DELETE | `/api/v1/api/v1/org-invitations/{invitation_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 91 | api | POST | `/api/v1/api/v1/org-invitations/{invitation_id}/resend` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 92 | api | GET | `/api/v1/api/v1/org-invitations/{token}` | SERVER_ERROR | 🔥 Server error - 500:  |
| 93 | api | POST | `/api/v1/api/v1/org-invitations/{token}/accept` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 94 | api | POST | `/api/v1/api/v1/org-invitations/{token}/decline` | SERVER_ERROR | 🔥 Server error - 500:  |
| 95 | api | GET | `/api/v1/api/v1/organizations/{organization_id}/invitations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 96 | api | POST | `/api/v1/api/v1/organizations/{organization_id}/invitations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 97 | auth | POST | `/api/v1/auth/forgot-password` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'email'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 98 | auth | POST | `/api/v1/auth/github/device` | SUCCESS | ✅ Success - 200 |
| 99 | auth | POST | `/api/v1/auth/github/token` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'device_code'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 100 | auth | GET | `/api/v1/auth/health` | SUCCESS | ✅ Success - 200 |
| 101 | auth | POST | `/api/v1/auth/login` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'email'], 'msg': 'Field required', 'input': {'username': 'test', 'password': 'test'}}] |
| 102 | auth | POST | `/api/v1/auth/logout` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 103 | auth | GET | `/api/v1/auth/me` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 104 | auth | GET | `/api/v1/auth/oauth/{provider}/authorize` | CLIENT_ERROR | ⚠️ Bad request - Invalid OAuth provider. Valid options: github, google |
| 105 | auth | POST | `/api/v1/auth/oauth/{provider}/callback` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'code'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'state'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 106 | auth | POST | `/api/v1/auth/refresh` | AUTH_REQUIRED | 🔒 Authentication required - endpoint needs valid JWT token |
| 107 | auth | POST | `/api/v1/auth/register` | TIMEOUT | Request timeout after 10s |
| 108 | auth | POST | `/api/v1/auth/reset-password` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'token'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'new_password'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 109 | auth | GET | `/api/v1/auth/verify-reset-token` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['query', 'token'], 'msg': 'Field required', 'input': None}] |
| 110 | auto-generate | POST | `/api/v1/auto-generate/all` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 111 | auto-generate | POST | `/api/v1/auto-generate/attestation` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 112 | auto-generate | POST | `/api/v1/auto-generate/context` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 113 | auto-generate | GET | `/api/v1/auto-generate/health` | SUCCESS | ✅ Success - 200 |
| 114 | auto-generate | POST | `/api/v1/auto-generate/intent` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 115 | auto-generate | POST | `/api/v1/auto-generate/ownership` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 116 | ceo-dashboard | POST | `/api/v1/ceo-dashboard/decisions/{submission_id}/override` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'override_type'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'pr_number'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'pr_title'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_name'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecoding_index'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'original_routing'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 117 | ceo-dashboard | POST | `/api/v1/ceo-dashboard/decisions/{submission_id}/resolve` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'decision'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 118 | ceo-dashboard | GET | `/api/v1/ceo-dashboard/health` | SUCCESS | ✅ Success - 200 |
| 119 | ceo-dashboard | GET | `/api/v1/ceo-dashboard/overrides` | ERROR | Exception: 'list' object has no attribute 'get' |
| 120 | ceo-dashboard | GET | `/api/v1/ceo-dashboard/pending-decisions` | ERROR | Exception: 'list' object has no attribute 'get' |
| 121 | ceo-dashboard | GET | `/api/v1/ceo-dashboard/routing-breakdown` | SUCCESS | ✅ Success - 200 |
| 122 | ceo-dashboard | POST | `/api/v1/ceo-dashboard/submissions` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'submission_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecoding_index'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'routing'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'status'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 123 | ceo-dashboard | GET | `/api/v1/ceo-dashboard/summary` | SUCCESS | ✅ Success - 200 |
| 124 | ceo-dashboard | GET | `/api/v1/ceo-dashboard/system-health` | SUCCESS | ✅ Success - 200 |
| 125 | ceo-dashboard | GET | `/api/v1/ceo-dashboard/time-saved` | SUCCESS | ✅ Success - 200 |
| 126 | ceo-dashboard | GET | `/api/v1/ceo-dashboard/top-rejections` | ERROR | Exception: 'list' object has no attribute 'get' |
| 127 | ceo-dashboard | GET | `/api/v1/ceo-dashboard/trends/time-saved` | ERROR | Exception: 'list' object has no attribute 'get' |
| 128 | ceo-dashboard | GET | `/api/v1/ceo-dashboard/trends/vibecoding-index` | ERROR | Exception: 'list' object has no attribute 'get' |
| 129 | ceo-dashboard | GET | `/api/v1/ceo-dashboard/weekly-summary` | SUCCESS | ✅ Success - 200 |
| 130 | check-runs | GET | `/api/v1/check-runs` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 131 | check-runs | GET | `/api/v1/check-runs/health/status` | SUCCESS | ✅ Success - 200 |
| 132 | check-runs | GET | `/api/v1/check-runs/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 133 | check-runs | GET | `/api/v1/check-runs/{check_run_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 134 | check-runs | POST | `/api/v1/check-runs/{check_run_id}/rerun` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 135 | codegen | POST | `/api/v1/codegen/estimate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 136 | codegen | POST | `/api/v1/codegen/generate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 137 | codegen | POST | `/api/v1/codegen/generate/full` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 138 | codegen | POST | `/api/v1/codegen/generate/resume/{session_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 139 | codegen | POST | `/api/v1/codegen/generate/stream` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 140 | codegen | POST | `/api/v1/codegen/generate/zip` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 141 | codegen | GET | `/api/v1/codegen/health` | SUCCESS | ✅ Success - 200 |
| 142 | codegen | POST | `/api/v1/codegen/ir/generate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 143 | codegen | POST | `/api/v1/codegen/ir/validate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 144 | codegen | GET | `/api/v1/codegen/onboarding/options/domains` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 145 | codegen | GET | `/api/v1/codegen/onboarding/options/features/{domain}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 146 | codegen | GET | `/api/v1/codegen/onboarding/options/scales` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 147 | codegen | POST | `/api/v1/codegen/onboarding/start` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 148 | codegen | GET | `/api/v1/codegen/onboarding/{session_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 149 | codegen | POST | `/api/v1/codegen/onboarding/{session_id}/app_name` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 150 | codegen | POST | `/api/v1/codegen/onboarding/{session_id}/domain` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 151 | codegen | POST | `/api/v1/codegen/onboarding/{session_id}/features` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 152 | codegen | POST | `/api/v1/codegen/onboarding/{session_id}/generate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 153 | codegen | POST | `/api/v1/codegen/onboarding/{session_id}/scale` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 154 | codegen | DELETE | `/api/v1/codegen/preview/{token}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 155 | codegen | GET | `/api/v1/codegen/preview/{token}` | NOT_FOUND | ❌ Endpoint not found - /api/v1/codegen/preview/{token} may not be implemented |
| 156 | codegen | GET | `/api/v1/codegen/providers` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 157 | codegen | GET | `/api/v1/codegen/sessions` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 158 | codegen | GET | `/api/v1/codegen/sessions/active` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 159 | codegen | GET | `/api/v1/codegen/sessions/{session_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 160 | codegen | POST | `/api/v1/codegen/sessions/{session_id}/preview` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 161 | codegen | GET | `/api/v1/codegen/sessions/{session_id}/quality/stream` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 162 | codegen | GET | `/api/v1/codegen/templates` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 163 | codegen | GET | `/api/v1/codegen/usage/monthly` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 164 | codegen | GET | `/api/v1/codegen/usage/provider-health/{provider}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 165 | codegen | GET | `/api/v1/codegen/usage/report` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 166 | codegen | POST | `/api/v1/codegen/validate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 167 | compliance | GET | `/api/v1/compliance/ai/budget` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 168 | compliance | GET | `/api/v1/compliance/ai/models` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 169 | compliance | GET | `/api/v1/compliance/ai/providers` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 170 | compliance | POST | `/api/v1/compliance/ai/recommendations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 171 | compliance | GET | `/api/v1/compliance/jobs/{job_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 172 | compliance | GET | `/api/v1/compliance/queue/status` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 173 | compliance | POST | `/api/v1/compliance/scans/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 174 | compliance | GET | `/api/v1/compliance/scans/{project_id}/history` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 175 | compliance | GET | `/api/v1/compliance/scans/{project_id}/latest` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 176 | compliance | POST | `/api/v1/compliance/scans/{project_id}/schedule` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 177 | compliance | GET | `/api/v1/compliance/violations/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 178 | compliance | POST | `/api/v1/compliance/violations/{violation_id}/ai-recommendation` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 179 | compliance | PUT | `/api/v1/compliance/violations/{violation_id}/resolve` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 180 | consultations | GET | `/api/v1/consultations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 181 | consultations | POST | `/api/v1/consultations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 182 | consultations | POST | `/api/v1/consultations/auto-generate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 183 | consultations | GET | `/api/v1/consultations/my-reviews` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 184 | consultations | GET | `/api/v1/consultations/{consultation_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 185 | consultations | POST | `/api/v1/consultations/{consultation_id}/assign` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 186 | consultations | POST | `/api/v1/consultations/{consultation_id}/comments` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 187 | consultations | POST | `/api/v1/consultations/{consultation_id}/resolve` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 188 | context-authority | GET | `/api/v1/context-authority/adrs` | SUCCESS | ✅ Success - 200 |
| 189 | context-authority | GET | `/api/v1/context-authority/adrs/{adr_id}` | NOT_FOUND | ❌ Endpoint not found - /api/v1/context-authority/adrs/{adr_id} may not be implemented |
| 190 | context-authority | GET | `/api/v1/context-authority/agents-md` | SUCCESS | ✅ Success - 200 |
| 191 | context-authority | POST | `/api/v1/context-authority/check-adr-linkage` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'modules'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 192 | context-authority | POST | `/api/v1/context-authority/check-spec` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'task_id'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 193 | context-authority | GET | `/api/v1/context-authority/health` | SUCCESS | ✅ Success - 200 |
| 194 | context-authority | GET | `/api/v1/context-authority/v2/health` | SUCCESS | ✅ Success - 200 |
| 195 | context-authority | POST | `/api/v1/context-authority/v2/overlay` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_tier'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'gate_status'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 196 | context-authority | GET | `/api/v1/context-authority/v2/snapshot/{submission_id}` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'submission_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `s` at 2', 'input': '{submission_id}', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `s` at 2'}}] |
| 197 | context-authority | GET | `/api/v1/context-authority/v2/snapshots/{project_id}` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'project_id'], 'msg': 'Input should be a valid UUID, invalid length: expected length 32 for simple format, found 1', 'input': '1', 'ctx': {'error': 'invalid length: expected length 32 for simple format, found 1'}}] |
| 198 | context-authority | GET | `/api/v1/context-authority/v2/stats` | SERVER_ERROR | 🔥 Server error - 500: Failed to get statistics: [Errno -2] Name or service not known |
| 199 | context-authority | GET | `/api/v1/context-authority/v2/templates` | SERVER_ERROR | 🔥 Server error - 500: Failed to list templates: [Errno -2] Name or service not known |
| 200 | context-authority | POST | `/api/v1/context-authority/v2/templates` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'name'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'trigger_type'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'trigger_value'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'overlay_content'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 201 | context-authority | GET | `/api/v1/context-authority/v2/templates/{template_id}` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'template_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2', 'input': '{template_id}', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2'}}] |
| 202 | context-authority | PUT | `/api/v1/context-authority/v2/templates/{template_id}` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'template_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2', 'input': '{template_id}', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2'}}] |
| 203 | context-authority | GET | `/api/v1/context-authority/v2/templates/{template_id}/usage` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'template_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2', 'input': '{template_id}', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2'}}] |
| 204 | context-authority | POST | `/api/v1/context-authority/v2/validate` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'submission_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_tier'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecoding_index'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecoding_zone'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'gate_status'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 205 | context-authority | POST | `/api/v1/context-authority/validate` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'submission_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'changed_files'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 206 | context-validation | GET | `/api/v1/context-validation/health` | SUCCESS | ✅ Success - 200 |
| 207 | context-validation | GET | `/api/v1/context-validation/limits` | SERVER_ERROR | 🔥 Server error - 500:  |
| 208 | context-validation | POST | `/api/v1/context-validation/validate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 209 | context-validation | POST | `/api/v1/context-validation/validate-github` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 210 | council | POST | `/api/v1/council/decide` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 211 | council | POST | `/api/v1/council/deliberate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 212 | council | GET | `/api/v1/council/history/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 213 | council | GET | `/api/v1/council/stats/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 214 | council | GET | `/api/v1/council/status/{request_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 215 | cross-reference | GET | `/api/v1/cross-reference/coverage/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 216 | cross-reference | GET | `/api/v1/cross-reference/missing-tests/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 217 | cross-reference | GET | `/api/v1/cross-reference/ssot-check/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 218 | cross-reference | POST | `/api/v1/cross-reference/validate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 219 | dashboard | GET | `/api/v1/dashboard/recent-gates` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 220 | dashboard | GET | `/api/v1/dashboard/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 221 | deprecation | GET | `/api/v1/deprecation/dashboard` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 222 | deprecation | GET | `/api/v1/deprecation/endpoints` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 223 | deprecation | GET | `/api/v1/deprecation/summary` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 224 | deprecation | GET | `/api/v1/deprecation/timeline` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 225 | doc-cross-reference | GET | `/api/v1/doc-cross-reference/links` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['query', 'project_id'], 'msg': 'Field required', 'input': None}, {'type': 'missing', 'loc': ['query', 'document_path'], 'msg': 'Field required', 'input': None}] |
| 226 | doc-cross-reference | GET | `/api/v1/doc-cross-reference/orphaned` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['query', 'project_id'], 'msg': 'Field required', 'input': None}] |
| 227 | doc-cross-reference | POST | `/api/v1/doc-cross-reference/validate` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'document_path'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 228 | doc-cross-reference | POST | `/api/v1/doc-cross-reference/validate-project` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_path'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 229 | docs | GET | `/api/v1/docs/user-support` | ERROR | Exception: 'list' object has no attribute 'get' |
| 230 | docs | GET | `/api/v1/docs/user-support/{filename}` | NOT_FOUND | ❌ Endpoint not found - /api/v1/docs/user-support/{filename} may not be implemented |
| 231 | dogfooding | GET | `/api/v1/dogfooding/ceo-time/entries` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 232 | dogfooding | POST | `/api/v1/dogfooding/ceo-time/record` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 233 | dogfooding | GET | `/api/v1/dogfooding/ceo-time/summary` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 234 | dogfooding | GET | `/api/v1/dogfooding/daily-checks` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 235 | dogfooding | GET | `/api/v1/dogfooding/daily-checks/history` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 236 | dogfooding | POST | `/api/v1/dogfooding/enforce/soft` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'pr_number'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecoding_index'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'zone'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 237 | dogfooding | GET | `/api/v1/dogfooding/enforce/soft/log` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 238 | dogfooding | POST | `/api/v1/dogfooding/enforce/soft/override` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 239 | dogfooding | GET | `/api/v1/dogfooding/enforce/soft/status` | SUCCESS | ✅ Success - 200 |
| 240 | dogfooding | GET | `/api/v1/dogfooding/export/json` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 241 | dogfooding | GET | `/api/v1/dogfooding/export/prometheus` | ERROR | Exception: 'str' object has no attribute 'get' |
| 242 | dogfooding | POST | `/api/v1/dogfooding/feedback` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 243 | dogfooding | GET | `/api/v1/dogfooding/feedback/list` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 244 | dogfooding | GET | `/api/v1/dogfooding/feedback/summary` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 245 | dogfooding | GET | `/api/v1/dogfooding/go-no-go` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 246 | dogfooding | GET | `/api/v1/dogfooding/metrics` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 247 | dogfooding | GET | `/api/v1/dogfooding/prs` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 248 | dogfooding | POST | `/api/v1/dogfooding/prs/record` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'pr_number'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'title'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'author'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecode_index'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'zone'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'friction_minutes'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 249 | dogfooding | POST | `/api/v1/dogfooding/report-false-positive` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 250 | dogfooding | GET | `/api/v1/dogfooding/status` | SUCCESS | ✅ Success - 200 |
| 251 | e2e | POST | `/api/v1/e2e/cancel/{execution_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 252 | e2e | POST | `/api/v1/e2e/execute` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 253 | e2e | GET | `/api/v1/e2e/history` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 254 | e2e | GET | `/api/v1/e2e/results/{execution_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 255 | e2e | GET | `/api/v1/e2e/status/{execution_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 256 | evidence-manifests | GET | `/api/v1/evidence-manifests` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 257 | evidence-manifests | POST | `/api/v1/evidence-manifests` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 258 | evidence-manifests | GET | `/api/v1/evidence-manifests/latest` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 259 | evidence-manifests | GET | `/api/v1/evidence-manifests/status` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 260 | evidence-manifests | GET | `/api/v1/evidence-manifests/verifications` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 261 | evidence-manifests | POST | `/api/v1/evidence-manifests/verify` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 262 | evidence-manifests | GET | `/api/v1/evidence-manifests/{manifest_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 263 | feedback | GET | `/api/v1/feedback` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 264 | feedback | POST | `/api/v1/feedback` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 265 | feedback | GET | `/api/v1/feedback/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 266 | feedback | GET | `/api/v1/feedback/{feedback_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 267 | feedback | PATCH | `/api/v1/feedback/{feedback_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 268 | feedback | GET | `/api/v1/feedback/{feedback_id}/comments` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 269 | feedback | POST | `/api/v1/feedback/{feedback_id}/comments` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 270 | framework-version | GET | `/api/v1/framework-version/health` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 271 | framework-version | GET | `/api/v1/framework-version/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 272 | framework-version | POST | `/api/v1/framework-version/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 273 | framework-version | GET | `/api/v1/framework-version/{project_id}/compliance` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 274 | framework-version | GET | `/api/v1/framework-version/{project_id}/drift` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 275 | framework-version | GET | `/api/v1/framework-version/{project_id}/history` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 276 | gates | GET | `/api/v1/gates` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 277 | gates | POST | `/api/v1/gates` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 278 | gates-engine | POST | `/api/v1/gates-engine/bulk-evaluate` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_type', 'loc': ['body', 'project_id'], 'msg': 'UUID input should be a string, bytes or UUID object', 'input': 1}] |
| 279 | gates-engine | POST | `/api/v1/gates-engine/evaluate-by-code` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_type', 'loc': ['body', 'project_id'], 'msg': 'UUID input should be a string, bytes or UUID object', 'input': 1}, {'type': 'missing', 'loc': ['body', 'gate_code'], 'msg': 'Field required', 'input': {'project_id': 1, 'gate_type': 'G1_CONSULTATION', 'name': 'Test Gate', 'description': 'Test gate for API testing'}}] |
| 280 | gates-engine | POST | `/api/v1/gates-engine/evaluate/{gate_id}` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'gate_id'], 'msg': 'Input should be a valid UUID, invalid length: expected length 32 for simple format, found 1', 'input': '1', 'ctx': {'error': 'invalid length: expected length 32 for simple format, found 1'}}] |
| 281 | gates-engine | GET | `/api/v1/gates-engine/health` | SUCCESS | ✅ Success - 200 |
| 282 | gates-engine | GET | `/api/v1/gates-engine/policies/{gate_code}` | CLIENT_ERROR | ⚠️ Bad request - Invalid gate code: {gate_code}. Valid codes: G0.1, G0.2, G1, G2, G3, G4, G5, G6, G7, G8, G9 |
| 283 | gates-engine | GET | `/api/v1/gates-engine/prerequisites/{gate_code}` | CLIENT_ERROR | ⚠️ Bad request - Invalid gate code: {gate_code}. Valid codes: G0.1, G0.2, G1, G2, G3, G4, G5, G6, G7, G8, G9 |
| 284 | gates-engine | GET | `/api/v1/gates-engine/readiness/{project_id}` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'project_id'], 'msg': 'Input should be a valid UUID, invalid length: expected length 32 for simple format, found 1', 'input': '1', 'ctx': {'error': 'invalid length: expected length 32 for simple format, found 1'}}] |
| 285 | gates-engine | GET | `/api/v1/gates-engine/stages` | SUCCESS | ✅ Success - 200 |
| 286 | gates | DELETE | `/api/v1/gates/{gate_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 287 | gates | GET | `/api/v1/gates/{gate_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 288 | gates | PUT | `/api/v1/gates/{gate_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 289 | gates | GET | `/api/v1/gates/{gate_id}/actions` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 290 | gates | GET | `/api/v1/gates/{gate_id}/approvals` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 291 | gates | POST | `/api/v1/gates/{gate_id}/approve` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 292 | gates | POST | `/api/v1/gates/{gate_id}/evaluate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 293 | gates | POST | `/api/v1/gates/{gate_id}/evidence` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 294 | gates | POST | `/api/v1/gates/{gate_id}/reject` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 295 | gates | POST | `/api/v1/gates/{gate_id}/submit` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 296 | governance-metrics | GET | `/api/v1/governance-metrics` | SUCCESS | ✅ Success - 200 |
| 297 | governance-metrics | GET | `/api/v1/governance-metrics/definitions` | SUCCESS | ✅ Success - 200 |
| 298 | governance-metrics | GET | `/api/v1/governance-metrics/health` | SUCCESS | ✅ Success - 200 |
| 299 | governance-metrics | GET | `/api/v1/governance-metrics/json` | SUCCESS | ✅ Success - 200 |
| 300 | governance-metrics | POST | `/api/v1/governance-metrics/record-break-glass` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'severity'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 301 | governance-metrics | POST | `/api/v1/governance-metrics/record-bypass` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'bypass_type'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 302 | governance-metrics | POST | `/api/v1/governance-metrics/record-ceo-override` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'override_type'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 303 | governance-metrics | POST | `/api/v1/governance-metrics/record-developer-friction` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'friction_minutes'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 304 | governance-metrics | POST | `/api/v1/governance-metrics/record-evidence` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'evidence_type'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'size_bytes'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 305 | governance-metrics | POST | `/api/v1/governance-metrics/record-llm` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'provider'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'model'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'duration_seconds'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'success'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 306 | governance-metrics | POST | `/api/v1/governance-metrics/record-submission` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'status'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecoding_index'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'routing'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'duration_seconds'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 307 | governance-metrics | POST | `/api/v1/governance-metrics/set-kill-switch` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'status'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 308 | governance-metrics | POST | `/api/v1/governance-metrics/update-ceo-metrics` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'week'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'time_saved_hours'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'pr_review_reduction_percent'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'governance_without_ceo_percent'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'false_positive_rate'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 309 | governance-metrics | POST | `/api/v1/governance-metrics/update-system-health` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'cpu_percent'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'memory_percent'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 310 | governance | GET | `/api/v1/governance/dogfooding/status` | SUCCESS | ✅ Success - 200 |
| 311 | governance | POST | `/api/v1/governance/false-positive` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 312 | governance | GET | `/api/v1/governance/health` | SUCCESS | ✅ Success - 200 |
| 313 | governance | POST | `/api/v1/governance/kill-switch` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 314 | governance | GET | `/api/v1/governance/metrics` | SUCCESS | ✅ Success - 200 |
| 315 | governance | GET | `/api/v1/governance/mode` | SUCCESS | ✅ Success - 200 |
| 316 | governance | PUT | `/api/v1/governance/mode` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 317 | governance | GET | `/api/v1/governance/mode/state` | SUCCESS | ✅ Success - 200 |
| 318 | governance | GET | `/api/v1/governance/specs/health` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 319 | governance | POST | `/api/v1/governance/specs/validate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 320 | governance | GET | `/api/v1/governance/specs/{spec_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 321 | governance | GET | `/api/v1/governance/specs/{spec_id}/acceptance-criteria` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 322 | governance | GET | `/api/v1/governance/specs/{spec_id}/requirements` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 323 | governance | GET | `/api/v1/governance/tiers/` | SERVER_ERROR | 🔥 Server error - 500:  |
| 324 | governance | GET | `/api/v1/governance/tiers/health` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 325 | governance | GET | `/api/v1/governance/tiers/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 326 | governance | POST | `/api/v1/governance/tiers/{project_id}/upgrade` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 327 | governance | GET | `/api/v1/governance/tiers/{tier}/requirements` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 328 | governance | POST | `/api/v1/governance/vibecoding/calculate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 329 | governance | GET | `/api/v1/governance/vibecoding/health` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 330 | governance | POST | `/api/v1/governance/vibecoding/kill-switch/check` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 331 | governance | POST | `/api/v1/governance/vibecoding/route` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 332 | governance | GET | `/api/v1/governance/vibecoding/signals/{submission_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 333 | governance | GET | `/api/v1/governance/vibecoding/stats/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 334 | governance | GET | `/api/v1/governance/vibecoding/{submission_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 335 | grafana-dashboards | GET | `/api/v1/grafana-dashboards` | SUCCESS | ✅ Success - 200 |
| 336 | grafana-dashboards | GET | `/api/v1/grafana-dashboards/datasource/template` | SUCCESS | ✅ Success - 200 |
| 337 | grafana-dashboards | GET | `/api/v1/grafana-dashboards/export/all` | ERROR | Exception: 'list' object has no attribute 'get' |
| 338 | grafana-dashboards | POST | `/api/v1/grafana-dashboards/provision` | SUCCESS | ✅ Success - 200 |
| 339 | grafana-dashboards | GET | `/api/v1/grafana-dashboards/{dashboard_type}` | CLIENT_ERROR | ⚠️ Bad request - Invalid dashboard type: {dashboard_type}. Valid types: ceo, tech, ops |
| 340 | grafana-dashboards | GET | `/api/v1/grafana-dashboards/{dashboard_type}/json` | CLIENT_ERROR | ⚠️ Bad request - Invalid dashboard type: {dashboard_type}. Valid types: ceo, tech, ops |
| 341 | grafana-dashboards | GET | `/api/v1/grafana-dashboards/{dashboard_type}/panels` | CLIENT_ERROR | ⚠️ Bad request - Invalid dashboard type: {dashboard_type}. Valid types: ceo, tech, ops |
| 342 | learnings | GET | `/api/v1/learnings/projects/{project_id}/aggregations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 343 | learnings | POST | `/api/v1/learnings/projects/{project_id}/aggregations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 344 | learnings | GET | `/api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 345 | learnings | POST | `/api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}/apply` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 346 | learnings | POST | `/api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}/reject` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 347 | learnings | POST | `/api/v1/learnings/projects/{project_id}/generate-hints` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 348 | learnings | GET | `/api/v1/learnings/projects/{project_id}/hints` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 349 | learnings | POST | `/api/v1/learnings/projects/{project_id}/hints` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 350 | learnings | GET | `/api/v1/learnings/projects/{project_id}/hints/active` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 351 | learnings | GET | `/api/v1/learnings/projects/{project_id}/hints/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 352 | learnings | POST | `/api/v1/learnings/projects/{project_id}/hints/usage` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 353 | learnings | POST | `/api/v1/learnings/projects/{project_id}/hints/usage/{usage_id}/feedback` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 354 | learnings | GET | `/api/v1/learnings/projects/{project_id}/hints/{hint_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 355 | learnings | PATCH | `/api/v1/learnings/projects/{project_id}/hints/{hint_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 356 | learnings | POST | `/api/v1/learnings/projects/{project_id}/hints/{hint_id}/verify` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 357 | learnings | GET | `/api/v1/learnings/projects/{project_id}/learnings` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 358 | learnings | POST | `/api/v1/learnings/projects/{project_id}/learnings` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 359 | learnings | POST | `/api/v1/learnings/projects/{project_id}/learnings/bulk-status` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 360 | learnings | POST | `/api/v1/learnings/projects/{project_id}/learnings/extract` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 361 | learnings | GET | `/api/v1/learnings/projects/{project_id}/learnings/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 362 | learnings | GET | `/api/v1/learnings/projects/{project_id}/learnings/{learning_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 363 | learnings | PATCH | `/api/v1/learnings/projects/{project_id}/learnings/{learning_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 364 | maturity | GET | `/api/v1/maturity/health` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 365 | maturity | GET | `/api/v1/maturity/levels` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 366 | maturity | GET | `/api/v1/maturity/org/{org_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 367 | maturity | GET | `/api/v1/maturity/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 368 | maturity | POST | `/api/v1/maturity/{project_id}/assess` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 369 | maturity | GET | `/api/v1/maturity/{project_id}/history` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 370 | mcp | GET | `/api/v1/mcp/context` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 371 | mcp | GET | `/api/v1/mcp/cost` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 372 | mcp | GET | `/api/v1/mcp/dashboard` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 373 | mcp | GET | `/api/v1/mcp/health` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 374 | mcp | GET | `/api/v1/mcp/latency` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 375 | mrp | GET | `/api/v1/mrp/health` | SUCCESS | ✅ Success - 200 |
| 376 | mrp | POST | `/api/v1/mrp/policies/compare` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 377 | mrp | GET | `/api/v1/mrp/policies/compliance/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 378 | mrp | POST | `/api/v1/mrp/policies/enforce` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 379 | mrp | GET | `/api/v1/mrp/policies/tiers` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 380 | mrp | POST | `/api/v1/mrp/validate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 381 | mrp | GET | `/api/v1/mrp/validate/{project_id}/{pr_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 382 | mrp | GET | `/api/v1/mrp/vcr/{project_id}/history` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 383 | mrp | GET | `/api/v1/mrp/vcr/{project_id}/{pr_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 384 | notifications | GET | `/api/v1/notifications` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 385 | notifications | PUT | `/api/v1/notifications/read-all` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 386 | notifications | GET | `/api/v1/notifications/settings/preferences` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 387 | notifications | PUT | `/api/v1/notifications/settings/preferences` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 388 | notifications | GET | `/api/v1/notifications/stats/summary` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 389 | notifications | DELETE | `/api/v1/notifications/{notification_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 390 | notifications | GET | `/api/v1/notifications/{notification_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 391 | notifications | PUT | `/api/v1/notifications/{notification_id}/read` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 392 | onboarding | POST | `/api/v1/onboarding/{session_id}/force-unlock` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 393 | onboarding | POST | `/api/v1/onboarding/{session_id}/lock` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 394 | onboarding | GET | `/api/v1/onboarding/{session_id}/lock-audit` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 395 | onboarding | GET | `/api/v1/onboarding/{session_id}/lock-status` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 396 | onboarding | GET | `/api/v1/onboarding/{session_id}/status` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 397 | onboarding | POST | `/api/v1/onboarding/{session_id}/unlock` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 398 | onboarding | POST | `/api/v1/onboarding/{session_id}/verify-hash` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 399 | organizations | GET | `/api/v1/organizations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 400 | organizations | POST | `/api/v1/organizations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 401 | organizations | GET | `/api/v1/organizations/{org_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 402 | organizations | PATCH | `/api/v1/organizations/{org_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 403 | organizations | POST | `/api/v1/organizations/{org_id}/members` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 404 | organizations | GET | `/api/v1/organizations/{org_id}/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 405 | overrides | GET | `/api/v1/overrides/event/{event_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 406 | overrides | POST | `/api/v1/overrides/request` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 407 | overrides | GET | `/api/v1/overrides/{override_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 408 | overrides | POST | `/api/v1/overrides/{override_id}/approve` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 409 | overrides | POST | `/api/v1/overrides/{override_id}/cancel` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 410 | overrides | POST | `/api/v1/overrides/{override_id}/reject` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 411 | payments | GET | `/api/v1/payments/subscriptions/me` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 412 | payments | POST | `/api/v1/payments/vnpay/create` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 413 | payments | POST | `/api/v1/payments/vnpay/ipn` | SUCCESS | ✅ Success - 200 |
| 414 | payments | GET | `/api/v1/payments/vnpay/return` | SUCCESS | ✅ Success - 200 |
| 415 | payments | GET | `/api/v1/payments/{vnp_txn_ref}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 416 | pilot | POST | `/api/v1/pilot/feedback` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 417 | pilot | POST | `/api/v1/pilot/metrics/aggregate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 418 | pilot | GET | `/api/v1/pilot/metrics/summary` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 419 | pilot | GET | `/api/v1/pilot/metrics/targets` | SUCCESS | ✅ Success - 200 |
| 420 | pilot | GET | `/api/v1/pilot/participants` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 421 | pilot | POST | `/api/v1/pilot/participants` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 422 | pilot | GET | `/api/v1/pilot/participants/me` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 423 | pilot | GET | `/api/v1/pilot/participants/{participant_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 424 | pilot | GET | `/api/v1/pilot/sessions` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 425 | pilot | POST | `/api/v1/pilot/sessions` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 426 | pilot | GET | `/api/v1/pilot/sessions/{session_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 427 | pilot | POST | `/api/v1/pilot/sessions/{session_id}/generation` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 428 | pilot | PATCH | `/api/v1/pilot/sessions/{session_id}/stage` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 429 | planning | POST | `/api/v1/planning/action-items/bulk/status` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 430 | planning | DELETE | `/api/v1/planning/action-items/{item_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 431 | planning | GET | `/api/v1/planning/action-items/{item_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 432 | planning | PUT | `/api/v1/planning/action-items/{item_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 433 | planning | POST | `/api/v1/planning/allocations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 434 | planning | POST | `/api/v1/planning/allocations/check-conflicts` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 435 | planning | DELETE | `/api/v1/planning/allocations/{allocation_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 436 | planning | GET | `/api/v1/planning/allocations/{allocation_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 437 | planning | PUT | `/api/v1/planning/allocations/{allocation_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 438 | planning | GET | `/api/v1/planning/backlog` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 439 | planning | POST | `/api/v1/planning/backlog` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 440 | planning | GET | `/api/v1/planning/backlog/assignees/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 441 | planning | POST | `/api/v1/planning/backlog/bulk/move-to-sprint` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 442 | planning | POST | `/api/v1/planning/backlog/bulk/update-priority` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 443 | planning | DELETE | `/api/v1/planning/backlog/{item_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 444 | planning | GET | `/api/v1/planning/backlog/{item_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 445 | planning | PUT | `/api/v1/planning/backlog/{item_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 446 | planning | GET | `/api/v1/planning/dashboard/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 447 | planning | POST | `/api/v1/planning/dependencies` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 448 | planning | POST | `/api/v1/planning/dependencies/bulk/resolve` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 449 | planning | GET | `/api/v1/planning/dependencies/check-circular` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 450 | planning | DELETE | `/api/v1/planning/dependencies/{dependency_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 451 | planning | GET | `/api/v1/planning/dependencies/{dependency_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 452 | planning | PUT | `/api/v1/planning/dependencies/{dependency_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 453 | planning | POST | `/api/v1/planning/dependencies/{dependency_id}/resolve` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 454 | planning | GET | `/api/v1/planning/phases` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 455 | planning | POST | `/api/v1/planning/phases` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 456 | planning | DELETE | `/api/v1/planning/phases/{phase_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 457 | planning | GET | `/api/v1/planning/phases/{phase_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 458 | planning | PUT | `/api/v1/planning/phases/{phase_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 459 | planning | GET | `/api/v1/planning/projects/{project_id}/dependency-analysis` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 460 | planning | GET | `/api/v1/planning/projects/{project_id}/dependency-graph` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 461 | planning | GET | `/api/v1/planning/projects/{project_id}/resource-heatmap` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 462 | planning | GET | `/api/v1/planning/projects/{project_id}/retrospective-comparison` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 463 | planning | GET | `/api/v1/planning/projects/{project_id}/template-suggestions` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 464 | planning | GET | `/api/v1/planning/projects/{project_id}/velocity` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 465 | planning | GET | `/api/v1/planning/roadmaps` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 466 | planning | POST | `/api/v1/planning/roadmaps` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 467 | planning | DELETE | `/api/v1/planning/roadmaps/{roadmap_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 468 | planning | GET | `/api/v1/planning/roadmaps/{roadmap_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 469 | planning | PUT | `/api/v1/planning/roadmaps/{roadmap_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 470 | planning | GET | `/api/v1/planning/sprints` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 471 | planning | POST | `/api/v1/planning/sprints` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 472 | planning | DELETE | `/api/v1/planning/sprints/{sprint_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 473 | planning | GET | `/api/v1/planning/sprints/{sprint_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 474 | planning | PUT | `/api/v1/planning/sprints/{sprint_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 475 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/action-items` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 476 | planning | POST | `/api/v1/planning/sprints/{sprint_id}/action-items` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 477 | planning | POST | `/api/v1/planning/sprints/{sprint_id}/action-items/bulk` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 478 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/action-items/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 479 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/allocations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 480 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/analytics` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 481 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/burndown` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 482 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/capacity` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 483 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/dependencies` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 484 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/forecast` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 485 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/gates` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 486 | planning | POST | `/api/v1/planning/sprints/{sprint_id}/gates` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 487 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/gates/{gate_type}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 488 | planning | PUT | `/api/v1/planning/sprints/{sprint_id}/gates/{gate_type}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 489 | planning | POST | `/api/v1/planning/sprints/{sprint_id}/gates/{gate_type}/submit` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 490 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/health` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 491 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/retrospective` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 492 | planning | GET | `/api/v1/planning/sprints/{sprint_id}/suggestions` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 493 | planning | POST | `/api/v1/planning/subagent/conformance` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 494 | planning | GET | `/api/v1/planning/subagent/health` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 495 | planning | POST | `/api/v1/planning/subagent/plan` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 496 | planning | POST | `/api/v1/planning/subagent/plan/with-risk` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 497 | planning | GET | `/api/v1/planning/subagent/sessions` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 498 | planning | POST | `/api/v1/planning/subagent/should-plan` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 499 | planning | GET | `/api/v1/planning/subagent/{planning_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 500 | planning | POST | `/api/v1/planning/subagent/{planning_id}/approve` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 501 | planning | GET | `/api/v1/planning/teams/{team_id}/capacity` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 502 | planning | GET | `/api/v1/planning/templates` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 503 | planning | POST | `/api/v1/planning/templates` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 504 | planning | POST | `/api/v1/planning/templates/bulk/delete` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 505 | planning | GET | `/api/v1/planning/templates/default` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 506 | planning | DELETE | `/api/v1/planning/templates/{template_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 507 | planning | GET | `/api/v1/planning/templates/{template_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 508 | planning | PUT | `/api/v1/planning/templates/{template_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 509 | planning | POST | `/api/v1/planning/templates/{template_id}/apply` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 510 | planning | GET | `/api/v1/planning/users/{user_id}/allocations` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 511 | planning | GET | `/api/v1/planning/users/{user_id}/capacity` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 512 | policies | GET | `/api/v1/policies` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 513 | policies | POST | `/api/v1/policies/evaluate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 514 | policies | GET | `/api/v1/policies/evaluations/{gate_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 515 | policies | GET | `/api/v1/policies/{policy_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 516 | policies | PUT | `/api/v1/policies/{policy_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 517 | projects | GET | `/api/v1/projects` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 518 | projects | POST | `/api/v1/projects` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 519 | projects | POST | `/api/v1/projects/init` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 520 | projects | DELETE | `/api/v1/projects/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 521 | projects | GET | `/api/v1/projects/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 522 | projects | PUT | `/api/v1/projects/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 523 | projects | GET | `/api/v1/projects/{project_id}/compliance-summary` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 524 | projects | GET | `/api/v1/projects/{project_id}/compliance/history` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 525 | projects | GET | `/api/v1/projects/{project_id}/compliance/last-check` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 526 | projects | GET | `/api/v1/projects/{project_id}/compliance/score` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 527 | projects | GET | `/api/v1/projects/{project_id}/context` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 528 | projects | PUT | `/api/v1/projects/{project_id}/context` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 529 | projects | GET | `/api/v1/projects/{project_id}/evidence/gaps` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 530 | projects | GET | `/api/v1/projects/{project_id}/evidence/status` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 531 | projects | POST | `/api/v1/projects/{project_id}/evidence/validate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 532 | projects | POST | `/api/v1/projects/{project_id}/migrate-stages` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 533 | projects | GET | `/api/v1/projects/{project_id}/overrides` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 534 | projects | DELETE | `/api/v1/projects/{project_id}/policy-pack` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 535 | projects | GET | `/api/v1/projects/{project_id}/policy-pack` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 536 | projects | POST | `/api/v1/projects/{project_id}/policy-pack` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 537 | projects | POST | `/api/v1/projects/{project_id}/policy-pack/evaluate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 538 | projects | POST | `/api/v1/projects/{project_id}/policy-pack/init` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 539 | projects | POST | `/api/v1/projects/{project_id}/policy-pack/rules` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 540 | projects | DELETE | `/api/v1/projects/{project_id}/policy-pack/rules/{policy_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 541 | projects | PUT | `/api/v1/projects/{project_id}/policy-pack/rules/{policy_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 542 | projects | POST | `/api/v1/projects/{project_id}/sync` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 543 | projects | GET | `/api/v1/projects/{project_id}/timeline` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 544 | projects | GET | `/api/v1/projects/{project_id}/timeline/export` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 545 | projects | GET | `/api/v1/projects/{project_id}/timeline/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 546 | projects | GET | `/api/v1/projects/{project_id}/timeline/{event_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 547 | projects | POST | `/api/v1/projects/{project_id}/validate-structure` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 548 | projects | POST | `/api/v1/projects/{project_id}/validate/compliance` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 549 | projects | POST | `/api/v1/projects/{project_id}/validate/duplicates` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 550 | projects | GET | `/api/v1/projects/{project_id}/validation-history` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 551 | push | GET | `/api/v1/push/status` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 552 | push | POST | `/api/v1/push/subscribe` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 553 | push | GET | `/api/v1/push/subscriptions` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 554 | push | POST | `/api/v1/push/unsubscribe` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 555 | push | GET | `/api/v1/push/vapid-key` | SUCCESS | ✅ Success - 200 |
| 556 | risk | POST | `/api/v1/risk/analyze` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 557 | risk | GET | `/api/v1/risk/factors` | ERROR | Exception: 'list' object has no attribute 'get' |
| 558 | risk | GET | `/api/v1/risk/levels` | SUCCESS | ✅ Success - 200 |
| 559 | risk | GET | `/api/v1/risk/should-plan` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 560 | sast | GET | `/api/v1/sast/health` | SUCCESS | ✅ Success - 200 |
| 561 | sast | GET | `/api/v1/sast/projects/{project_id}/analytics` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 562 | sast | POST | `/api/v1/sast/projects/{project_id}/scan` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 563 | sast | GET | `/api/v1/sast/projects/{project_id}/scans` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 564 | sast | GET | `/api/v1/sast/projects/{project_id}/scans/{scan_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 565 | sast | GET | `/api/v1/sast/projects/{project_id}/trend` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 566 | sast | POST | `/api/v1/sast/scan-snippet` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'code'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'language'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 567 | sop | POST | `/api/v1/sop/generate` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'sop_type'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'workflow_description'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 568 | sop | GET | `/api/v1/sop/health` | SUCCESS | ✅ Success - 200 |
| 569 | sop | GET | `/api/v1/sop/list` | SUCCESS | ✅ Success - 200 |
| 570 | sop | GET | `/api/v1/sop/types` | ERROR | Exception: 'list' object has no attribute 'get' |
| 571 | sop | GET | `/api/v1/sop/{sop_id}` | NOT_FOUND | ❌ Endpoint not found - /api/v1/sop/{sop_id} may not be implemented |
| 572 | sop | GET | `/api/v1/sop/{sop_id}/mrp` | NOT_FOUND | ❌ Endpoint not found - /api/v1/sop/{sop_id}/mrp may not be implemented |
| 573 | sop | GET | `/api/v1/sop/{sop_id}/vcr` | NOT_FOUND | ❌ Endpoint not found - /api/v1/sop/{sop_id}/vcr may not be implemented |
| 574 | sop | POST | `/api/v1/sop/{sop_id}/vcr` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'decision'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'reviewer'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 575 | spec-converter | POST | `/api/v1/spec-converter/convert` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'content'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'source_format'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'target_format'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 576 | spec-converter | POST | `/api/v1/spec-converter/detect` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'content'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 577 | spec-converter | POST | `/api/v1/spec-converter/import/jira` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'issue_key'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 578 | spec-converter | POST | `/api/v1/spec-converter/import/linear` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'issue_id'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 579 | spec-converter | POST | `/api/v1/spec-converter/import/text` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'content'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 580 | spec-converter | POST | `/api/v1/spec-converter/parse` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'content'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'source_format'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 581 | spec-converter | POST | `/api/v1/spec-converter/render` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'ir'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'target_format'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 582 | stage-gating | POST | `/api/v1/stage-gating/advance` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'advanced_by'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 583 | stage-gating | POST | `/api/v1/stage-gating/complete` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'stage'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'completed_by'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 584 | stage-gating | GET | `/api/v1/stage-gating/health` | SUCCESS | ✅ Success - 200 |
| 585 | stage-gating | GET | `/api/v1/stage-gating/progress/{project_id}` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'project_id'], 'msg': 'Input should be a valid UUID, invalid length: expected length 32 for simple format, found 1', 'input': '1', 'ctx': {'error': 'invalid length: expected length 32 for simple format, found 1'}}] |
| 586 | stage-gating | GET | `/api/v1/stage-gating/rules` | SUCCESS | ✅ Success - 200 |
| 587 | stage-gating | GET | `/api/v1/stage-gating/rules/{stage}` | NOT_FOUND | ❌ Endpoint not found - /api/v1/stage-gating/rules/{stage} may not be implemented |
| 588 | stage-gating | POST | `/api/v1/stage-gating/validate` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'request'], 'msg': 'Field required', 'input': None}, {'type': 'missing', 'loc': ['body', 'project_context'], 'msg': 'Field required', 'input': None}] |
| 589 | teams | GET | `/api/v1/teams` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 590 | teams | POST | `/api/v1/teams` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 591 | teams | DELETE | `/api/v1/teams/{team_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 592 | teams | GET | `/api/v1/teams/{team_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 593 | teams | PATCH | `/api/v1/teams/{team_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 594 | teams | GET | `/api/v1/teams/{team_id}/members` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 595 | teams | POST | `/api/v1/teams/{team_id}/members` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 596 | teams | DELETE | `/api/v1/teams/{team_id}/members/{user_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 597 | teams | PATCH | `/api/v1/teams/{team_id}/members/{user_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 598 | teams | GET | `/api/v1/teams/{team_id}/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 599 | telemetry | GET | `/api/v1/telemetry/dashboard` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 600 | telemetry | POST | `/api/v1/telemetry/events` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 601 | telemetry | POST | `/api/v1/telemetry/events/batch` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 602 | telemetry | GET | `/api/v1/telemetry/funnels/{funnel_name}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 603 | telemetry | GET | `/api/v1/telemetry/health` | SUCCESS | ✅ Success - 200 |
| 604 | telemetry | GET | `/api/v1/telemetry/interfaces` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 605 | timeline | POST | `/api/v1/timeline/{event_id}/override/approve` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 606 | timeline | POST | `/api/v1/timeline/{event_id}/override/reject` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 607 | timeline | POST | `/api/v1/timeline/{event_id}/override/request` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 608 | triage | POST | `/api/v1/triage/analyze` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 609 | triage | GET | `/api/v1/triage/sla-breaches` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 610 | triage | GET | `/api/v1/triage/stats` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 611 | triage | POST | `/api/v1/triage/{feedback_id}/apply` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 612 | triage | POST | `/api/v1/triage/{feedback_id}/auto-triage` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 613 | triage | GET | `/api/v1/triage/{feedback_id}/sla` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 614 | vcr | GET | `/api/v1/vcr` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 615 | vcr | POST | `/api/v1/vcr` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 616 | vcr | POST | `/api/v1/vcr/auto-generate` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 617 | vcr | GET | `/api/v1/vcr/stats/{project_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 618 | vcr | DELETE | `/api/v1/vcr/{vcr_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 619 | vcr | GET | `/api/v1/vcr/{vcr_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 620 | vcr | PUT | `/api/v1/vcr/{vcr_id}` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 621 | vcr | POST | `/api/v1/vcr/{vcr_id}/approve` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 622 | vcr | POST | `/api/v1/vcr/{vcr_id}/reject` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 623 | vcr | POST | `/api/v1/vcr/{vcr_id}/reopen` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 624 | vcr | POST | `/api/v1/vcr/{vcr_id}/submit` | AUTH_REQUIRED | 🔒 Invalid or missing authentication token (JWT required) |
| 625 | vibecoding | POST | `/api/v1/vibecoding/batch` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'submissions'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 626 | vibecoding | POST | `/api/v1/vibecoding/calculate` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'submission_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'changed_files'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 627 | vibecoding | POST | `/api/v1/vibecoding/calibrate` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'submission_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'calculated_score'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'ceo_agrees'], 'msg': 'Field required', 'input': {'test': 'data'}}] |
| 628 | vibecoding | GET | `/api/v1/vibecoding/health` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'submission_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `h` at 1', 'input': 'health', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `h` at 1'}}] |
| 629 | vibecoding | GET | `/api/v1/vibecoding/stats` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'submission_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `s` at 1', 'input': 'stats', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `s` at 1'}}] |
| 630 | vibecoding | GET | `/api/v1/vibecoding/thresholds` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'submission_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 1', 'input': 'thresholds', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 1'}}] |
| 631 | vibecoding | GET | `/api/v1/vibecoding/{submission_id}` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'submission_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `s` at 2', 'input': '{submission_id}', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `s` at 2'}}] |
| 632 | unknown | GET | `/health` | SUCCESS | ✅ Success - 200 |
| 633 | unknown | GET | `/health/ready` | SERVER_ERROR | 🔥 Server error - 503:  |
| 634 | unknown | GET | `/metrics` | SUCCESS | ✅ Success - 200 |
| 635 | project | POST | `/ws/broadcast/project/{project_id}` | CLIENT_ERROR | ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'project_id'], 'msg': 'Input should be a valid UUID, invalid length: expected length 32 for simple format, found 1', 'input': '1', 'ctx': {'error': 'invalid length: expected length 32 for simple format, found 1'}}, {'type': 'missing', 'loc': ['query', 'event_type'], 'msg': 'Field required', 'input': None}] |
| 636 | unknown | GET | `/ws/stats` | SUCCESS | ✅ Success - 200 |

---

## 🔍 Full Request/Response Details

### SUCCESS (52 endpoints)

#### GET /

**Summary**: Root

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 6ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "service": "SDLC Orchestrator API",
  "version": "1.2.0",
  "docs": "/api/docs",
  "health": "/health",
  "metrics": "/metrics"
}
```

---

#### GET /api/v1/ai-detection/circuit-breakers

**Summary**: Get Circuit Breakers

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 15ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/ai-detection/circuit-breakers",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "circuit_breakers": {
    "github_api": {
      "name": "github_api",
      "config": {
        "failure_threshold": 5,
        "recovery_timeout": 30.0,
        "success_threshold": 3,
        "enabled": true
      },
      "stats": {
        "state": "closed",
        "failure_count": 0,
        "success_count": 0,
        "last_failure_time": null,
        "last_state_change": 1771650013.3285801,
        "total_requests": 0,
        "total_failures": 0,
        "total_successes": 0,
        "total_rejections": 0,
        "uptime_seconds": 5514.606889009476
      }
    },
    "external_ai": {
      "name": "external_ai",
      "config": {
        "failure_threshold": 5,
        "recovery_timeout": 30.0,
        "success_threshold": 3,
        "enabled": true
      },
      "stats": {
        "state": "closed",
        "failure_count": 0,
        "success_count": 0,
        "last_failure_time": null,
        "last_state_change": 1771650013.3285892,
        "total_requests": 0,
   
... (truncated)
```

---

#### GET /api/v1/ai-detection/shadow-mode

**Summary**: Get Shadow Mode

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/ai-detection/shadow-mode",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "enabled",
  "config": {
    "enabled": true,
    "sample_rate": 1.0,
    "log_level": "INFO",
    "collect_metrics": true
  },
  "description": "Shadow mode logs detection results for production validation without blocking or modifying PRs."
}
```

---

#### GET /api/v1/ai-detection/status

**Summary**: Get Detection Status

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/ai-detection/status",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "service": "GitHubAIDetectionService",
  "version": "1.0.0",
  "detection_threshold": 0.5,
  "strategies": [
    "metadata",
    "commit",
    "pattern"
  ],
  "weights": {
    "metadata": 0.4,
    "commit": 0.4,
    "pattern": 0.2
  },
  "shadow_mode": {
    "enabled": true,
    "sample_rate": 1.0,
    "log_level": "INFO",
    "collect_metrics": true
  }
}
```

---

#### GET /api/v1/ai-detection/tools

**Summary**: Get Supported Tools

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 4ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/ai-detection/tools",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "tools": [
    {
      "id": "cursor",
      "name": "Cursor"
    },
    {
      "id": "copilot",
      "name": "Copilot"
    },
    {
      "id": "claude_code",
      "name": "Claude Code"
    },
    {
      "id": "chatgpt",
      "name": "Chatgpt"
    },
    {
      "id": "windsurf",
      "name": "Windsurf"
    },
    {
      "id": "cody",
      "name": "Cody"
    },
    {
      "id": "tabnine",
      "name": "Tabnine"
    },
    {
      "id": "other",
      "name": "Other"
    },
    {
      "id": "manual_tag",
      "name": "Manual Tag"
    }
  ],
  "count": 9
}
```

---

#### POST /api/v1/auth/github/device

**Summary**: Github Device Flow Init

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 634ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/auth/github/device",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "device_code": "3dde2377ba69ef92225c202c4ec39ef1ef4895dd",
  "user_code": "4C95-98BA",
  "verification_uri": "https://github.com/login/device",
  "expires_in": 899,
  "interval": 5
}
```

---

#### GET /api/v1/auth/health

**Summary**: Auth Health Check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 7ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/auth/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "healthy",
  "service": "authentication",
  "version": "1.0.0"
}
```

---

#### GET /api/v1/auto-generate/health

**Summary**: Auto-Generation Health Check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 20ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/auto-generate/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "service": "AutoGenerationService",
  "healthy": true,
  "ollama_available": false,
  "ollama_models": [],
  "generators": {
    "intent": "enabled",
    "ownership": "enabled",
    "context": "enabled",
    "attestation": "enabled"
  },
  "fail_safe_enabled": true,
  "target_latency": "<5s per generator"
}
```

---

#### GET /api/v1/ceo-dashboard/health

**Summary**: CEO Dashboard health check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 12ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/ceo-dashboard/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "healthy",
  "service": "ceo_dashboard",
  "timestamp": "2026-02-21T06:32:23.107666",
  "metrics": {
    "submissions_tracked": 0,
    "overrides_tracked": 0,
    "pending_queue_size": 0
  }
}
```

---

#### GET /api/v1/ceo-dashboard/routing-breakdown

**Summary**: Get PR routing breakdown

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/ceo-dashboard/routing-breakdown",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "total_prs": 0,
  "auto_approved": 0,
  "tech_lead_review": 0,
  "ceo_should_review": 0,
  "ceo_must_review": 0,
  "auto_approval_rate": 0.0,
  "trend": "stable",
  "last_updated": "2026-02-21T06:32:23.317350"
}
```

---

#### GET /api/v1/ceo-dashboard/summary

**Summary**: Get complete CEO dashboard summary

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/ceo-dashboard/summary",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "executive_summary": {
    "time_saved": {
      "baseline_hours": 40.0,
      "actual_review_hours": 0.0,
      "time_saved_hours": 40.0,
      "time_saved_percent": 100.0,
      "trend": "stable",
      "status": "excellent",
      "target_week": 7,
      "target_hours": 10.0,
      "on_track": true,
      "last_updated": "2026-02-21T06:32:23.448170"
    },
    "routing_breakdown": {
      "total_prs": 0,
      "auto_approved": 0,
      "tech_lead_review": 0,
      "ceo_should_review": 0,
      "ceo_must_review": 0,
      "auto_approval_rate": 0.0,
      "trend": "stable",
      "last_updated": "2026-02-21T06:32:23.448177"
    },
    "pending_decisions_count": 0
  },
  "weekly_summary": {
    "week_number": 8,
    "week_start": "2026-02-16T00:00:00",
    "week_end": "2026-02-23T00:00:00",
    "compliance_pass_rate": 0,
    "vibecoding_index_avg": 0,
    "false_positive_rate": 0,
    "developer_satisfaction_nps": null,
    "time_saved_hours": 40.0,
    "total_submissions": 0,
    
... (truncated)
```

---

#### GET /api/v1/ceo-dashboard/system-health

**Summary**: Get system health snapshot

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 9ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/ceo-dashboard/system-health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "uptime_percent": 99.9,
  "api_latency_p95_ms": 85.0,
  "kill_switch_status": "WARNING",
  "overall_status": "excellent",
  "alerts_active": 0,
  "last_incident": null
}
```

---

#### GET /api/v1/ceo-dashboard/time-saved

**Summary**: Get CEO time saved metrics

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/ceo-dashboard/time-saved",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "baseline_hours": 40.0,
  "actual_review_hours": 0.0,
  "time_saved_hours": 40.0,
  "time_saved_percent": 100.0,
  "trend": "stable",
  "status": "excellent",
  "target_week": 7,
  "target_hours": 10.0,
  "on_track": true,
  "last_updated": "2026-02-21T06:32:23.577477"
}
```

---

#### GET /api/v1/ceo-dashboard/weekly-summary

**Summary**: Get weekly governance summary

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 19ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/ceo-dashboard/weekly-summary",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "week_number": 8,
  "week_start": "2026-02-16T00:00:00",
  "week_end": "2026-02-23T00:00:00",
  "compliance_pass_rate": 0.0,
  "vibecoding_index_avg": 0.0,
  "false_positive_rate": 0.0,
  "developer_satisfaction_nps": null,
  "time_saved_hours": 40.0,
  "total_submissions": 0,
  "total_rejections": 0,
  "ceo_overrides": 0,
  "status": "warning"
}
```

---

#### GET /api/v1/check-runs/health/status

**Summary**: Health Check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/check-runs/health/status",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "healthy",
  "service": "check-runs-api",
  "version": "1.0.0",
  "feature_status": "in_development",
  "message": "Check runs endpoints available but database table not yet created"
}
```

---

#### GET /api/v1/codegen/health

**Summary**: Health Check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 136ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/codegen/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "healthy": true,
  "providers": {
    "app-builder": true,
    "ollama": false,
    "claude": false,
    "deepcode": false
  },
  "available_count": 1,
  "total_count": 4,
  "fallback_chain": [
    "ollama",
    "claude",
    "deepcode"
  ]
}
```

---

#### GET /api/v1/context-authority/adrs

**Summary**: [DEPRECATED] List all ADRs

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 26ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-authority/adrs",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "total": 0,
  "adrs": [],
  "statuses": {}
}
```

---

#### GET /api/v1/context-authority/agents-md

**Summary**: [DEPRECATED] Get AGENTS.md status

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 13ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-authority/agents-md",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "exists": false,
  "file_path": "/app/AGENTS.md",
  "last_modified": null,
  "age_days": 0,
  "is_stale": true,
  "staleness_threshold_days": 7,
  "line_count": 0,
  "message": "AGENTS.md not found"
}
```

---

#### GET /api/v1/context-authority/health

**Summary**: [DEPRECATED] Context authority health check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 13ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-authority/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "healthy",
  "service": "context_authority_v1",
  "deprecated": true,
  "deprecation_notice": "This V1 endpoint will be removed on 2026-03-06. Use /context-authority/v2/health",
  "adr_count": 0,
  "adr_path": "docs/02-design/03-ADRs",
  "spec_path": "docs/02-design/specs",
  "agents_md_path": "AGENTS.md",
  "staleness_threshold_days": 7,
  "timestamp": "2026-02-21T06:32:28.208173"
}
```

---

#### GET /api/v1/context-authority/v2/health

**Summary**: Health check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 40ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-authority/v2/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "unhealthy",
  "version": "2.0.0",
  "template_count": 0,
  "snapshot_count_24h": 0,
  "avg_validation_ms": 0.0,
  "avg_overlay_ms": 0.0,
  "last_check": "2026-02-21T06:32:28.297513"
}
```

---

#### GET /api/v1/context-validation/health

**Summary**: Health check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-validation/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "healthy",
  "service": "context-validation",
  "version": "1.0.0",
  "max_lines_per_file": 60
}
```

---

#### GET /api/v1/dogfooding/enforce/soft/status

**Summary**: Get Soft Mode Status

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 9ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/dogfooding/enforce/soft/status",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "mode": "soft",
  "active": false,
  "sprint": "115",
  "configuration": {
    "signal_weights": {
      "architectural_smell": 0.25,
      "abstraction_complexity": 0.15,
      "ai_dependency_ratio": 0.2,
      "change_surface_area": 0.25,
      "drift_velocity": 0.15
    },
    "zone_thresholds": {
      "green": [
        0,
        30
      ],
      "yellow": [
        31,
        60
      ],
      "orange": [
        61,
        80
      ],
      "red": [
        81,
        100
      ]
    },
    "exemptions_enabled": [
      "dependency_update_exemption",
      "documentation_safe_pattern",
      "test_only_pattern"
    ],
    "block_rules": [
      "red_zone_blocking",
      "missing_ownership",
      "missing_intent",
      "security_scan_critical"
    ]
  },
  "metrics": {
    "total_enforcements": 0,
    "blocked": 0,
    "warned": 0,
    "passed": 0,
    "block_rate": 0,
    "exemption_usage": {}
  }
}
```

---

#### GET /api/v1/dogfooding/status

**Summary**: Get Dogfooding Status

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/dogfooding/status",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "sprint": "114",
  "mode": "WARNING",
  "start_date": "2026-02-03",
  "end_date": "2026-02-07",
  "days_elapsed": 5,
  "prs_evaluated": 0,
  "prs_target": 15,
  "status": "active"
}
```

---

#### GET /api/v1/gates-engine/health

**Summary**: Gates engine health check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 29ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/gates-engine/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "healthy",
  "service": "gates_engine",
  "opa_available": true,
  "valid_gate_codes": [
    "G0.1",
    "G0.2",
    "G1",
    "G2",
    "G3",
    "G4",
    "G5",
    "G6",
    "G7",
    "G8",
    "G9"
  ],
  "timestamp": "2026-02-21T06:32:34.083963"
}
```

---

#### GET /api/v1/gates-engine/stages

**Summary**: Get gate-to-stage mapping

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/gates-engine/stages",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "G0.1": "WHY",
  "G0.2": "WHY",
  "G1": "WHAT",
  "G2": "HOW",
  "G3": "BUILD",
  "G4": "TEST",
  "G5": "DEPLOY",
  "G6": "OPERATE",
  "G7": "INTEGRATE",
  "G8": "COLLABORATE",
  "G9": "GOVERN"
}
```

---

#### GET /api/v1/governance-metrics

**Summary**: Get Prometheus metrics

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 13ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/governance-metrics",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
# HELP governance_submissions_total Total number of governance submissions
# TYPE governance_submissions_total counter

# HELP governance_submissions_duration_seconds Time from submission to validation complete
# TYPE governance_submissions_duration_seconds histogram

# HELP governance_rejections_total Total number of rejections by reason
# TYPE governance_rejections_total counter

# HELP governance_vibecoding_index Vibecoding Index distribution
# TYPE governance_vibecoding_index histogram

# HE
```

---

#### GET /api/v1/governance-metrics/definitions

**Summary**: Get metric definitions

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/governance-metrics/definitions",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "total": 47,
  "categories": {
    "governance_system": 15,
    "performance": 10,
    "business_ceo_dashboard": 8,
    "developer_experience": 7,
    "system_health": 5
  },
  "definitions": [
    {
      "name": "governance_submissions_total",
      "type": "counter",
      "description": "Total number of governance submissions",
      "labels": [
        "project_id",
        "status"
      ],
      "buckets": null
    },
    {
      "name": "governance_submissions_duration_seconds",
      "type": "histogram",
      "description": "Time from submission to validation complete",
      "labels": [
        "project_id"
      ],
      "buckets": [
        0.1,
        0.5,
        1.0,
        2.0,
        5.0,
        10.0
      ]
    },
    {
      "name": "governance_rejections_total",
      "type": "counter",
      "description": "Total number of rejections by reason",
      "labels": [
        "project_id",
        "rejection_reason"
      ],
      "buckets": null
    },
    {
 
... (truncated)
```

---

#### GET /api/v1/governance-metrics/health

**Summary**: Metrics service health check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 7ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/governance-metrics/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "healthy",
  "service": "prometheus_metrics_collector",
  "timestamp": "2026-02-21T06:32:35.160174",
  "metrics_count": 47,
  "counters_active": 0,
  "gauges_active": 0,
  "histograms_active": 0
}
```

---

#### GET /api/v1/governance-metrics/json

**Summary**: Get metrics in JSON format

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 12ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/governance-metrics/json",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "counters": {},
  "gauges": {},
  "histograms": {},
  "timestamp": "2026-02-21T06:32:35.226254",
  "total_metrics": 47
}
```

---

#### GET /api/v1/governance/dogfooding/status

**Summary**: Get dogfooding status

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 15ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/governance/dogfooding/status",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "phase": "week_1_preparation",
  "mode": "warning",
  "start_date": "2026-02-21T06:32:35.942881",
  "current_week": 1,
  "metrics": {
    "total_evaluations": 0,
    "rejection_rate": "0.0%",
    "false_positive_rate": "0.0%",
    "first_pass_rate": "N/A"
  },
  "success_criteria_status": {
    "first_submission_pass_rate": true,
    "developer_friction_low": true,
    "auto_generation_usage_high": true
  },
  "failure_criteria_triggered": [],
  "recommendation": "Ready to advance to SOFT enforcement"
}
```

---

#### GET /api/v1/governance/health

**Summary**: Governance service health check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/governance/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "healthy",
  "mode": "warning",
  "auto_rollback_enabled": true,
  "total_evaluations": 0,
  "latency_p95_ms": 0.0,
  "timestamp": "2026-02-21T06:32:36.072965"
}
```

---

#### GET /api/v1/governance/metrics

**Summary**: Get governance metrics

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/governance/metrics",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "mode": "warning",
  "total_evaluations": 0,
  "total_blocked": 0,
  "total_warned": 0,
  "total_passed": 0,
  "rejection_rate": 0.0,
  "false_positive_rate": 0.0,
  "latency_p95_ms": 0.0,
  "ceo_overrides": 0,
  "auto_rollback_enabled": true,
  "uptime_since": "2026-02-21T06:32:35.942881"
}
```

---

#### GET /api/v1/governance/mode

**Summary**: Get current governance mode

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 12ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/governance/mode",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "mode": "warning",
  "previous_mode": null,
  "changed_at": "2026-02-21T06:32:35.942881",
  "changed_by": "system",
  "reason": "Initial startup",
  "is_rollback": false,
  "auto_rollback_enabled": true
}
```

---

#### GET /api/v1/governance/mode/state

**Summary**: Get full governance mode state

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/governance/mode/state",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "mode": "warning",
  "previous_mode": null,
  "changed_at": "2026-02-21T06:32:35.942881",
  "changed_by": "system",
  "reason": "Initial startup",
  "is_rollback": false,
  "auto_rollback_enabled": true,
  "total_evaluations": 0,
  "total_blocked": 0,
  "total_warned": 0,
  "total_passed": 0,
  "rejection_rate": 0.0,
  "false_positive_rate": 0.0,
  "ceo_overrides": 0
}
```

---

#### GET /api/v1/grafana-dashboards

**Summary**: List all Grafana dashboards

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/grafana-dashboards",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "dashboards": [
    {
      "uid": "ceo-dashboard",
      "title": "CEO Dashboard - Governance Intelligence",
      "description": "Executive governance intelligence dashboard for CEO, CTO, CPO. Real-time visibility into governance effectiveness and team productivity.",
      "type": "ceo",
      "tags": [
        "governance",
        "ceo",
        "executive",
        "vibecoding"
      ],
      "panel_count": 15,
      "refresh": "5s",
      "time_from": "now-7d",
      "time_to": "now"
    },
    {
      "uid": "tech-dashboard",
      "title": "Tech Dashboard - Developer Experience & Performance",
      "description": "Technical dashboard for Tech Lead, Backend Lead, DevOps. Developer experience metrics, system performance, and LLM health.",
      "type": "tech",
      "tags": [
        "governance",
        "tech",
        "performance",
        "developer-experience"
      ],
      "panel_count": 12,
      "refresh": "5m",
      "time_from": "now-24h",
      "time_to": "now"
... (truncated)
```

---

#### GET /api/v1/grafana-dashboards/datasource/template

**Summary**: Get Prometheus datasource template

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/grafana-dashboards/datasource/template",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "name": "Prometheus-SDLC",
  "type": "prometheus",
  "access": "proxy",
  "url": "http://prometheus:9090",
  "isDefault": true,
  "editable": true,
  "jsonData": {
    "httpMethod": "POST",
    "timeInterval": "5s",
    "queryTimeout": "30s"
  },
  "secureJsonData": {},
  "uid": "prometheus-sdlc"
}
```

---

#### POST /api/v1/grafana-dashboards/provision

**Summary**: Provision dashboards to Grafana

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 22ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/grafana-dashboards/provision",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "success": false,
  "provisioned": [],
  "failed": [
    {
      "uid": "ceo-dashboard",
      "error": "All connection attempts failed"
    },
    {
      "uid": "tech-dashboard",
      "error": "All connection attempts failed"
    },
    {
      "uid": "ops-dashboard",
      "error": "All connection attempts failed"
    }
  ],
  "message": "Provisioned 0 dashboards, 3 failed"
}
```

---

#### GET /api/v1/mrp/health

**Summary**: Health check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/mrp/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "healthy",
  "service": "mrp-validation",
  "version": "1.0.0",
  "features": [
    "5-point-mrp-validation",
    "vcr-generation",
    "4-tier-policy-enforcement"
  ]
}
```

---

#### POST /api/v1/payments/vnpay/ipn

**Summary**: Vnpay Ipn Handler

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 10ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/payments/vnpay/ipn",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "RspCode": "97",
  "Message": "Invalid signature"
}
```

---

#### GET /api/v1/payments/vnpay/return

**Summary**: Vnpay Return Handler

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 9ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/payments/vnpay/return",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "success": false,
  "message": "Missing transaction reference",
  "redirect": "/checkout/failed"
}
```

---

#### GET /api/v1/pilot/metrics/targets

**Summary**: Get Sprint 49 targets

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/pilot/metrics/targets",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "participants": {
    "target": 10,
    "description": "Vietnamese SME founders to recruit"
  },
  "ttfv": {
    "target_seconds": 1800,
    "target_minutes": 30,
    "description": "Time from idea to working app"
  },
  "satisfaction": {
    "target": 8,
    "max": 10,
    "description": "Average satisfaction score"
  },
  "quality_gate": {
    "target_percent": 95.0,
    "description": "Quality gate pass rate"
  },
  "sprint": "Sprint 49",
  "ceo_approved": "December 23, 2025"
}
```

---

#### GET /api/v1/push/vapid-key

**Summary**: Get Vapid Public Key

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/push/vapid-key",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "public_key": "BNbxGGkqLJiJqhspMQU0JCzKHJtKqkq0TdVbJGiWFhB1GGJhkPGiWFhB1GGJhkPGiWFhB1GGJhkPGiWFhB1GGJhkPGiWFhB1GGJhkP"
}
```

---

#### GET /api/v1/risk/levels

**Summary**: Get risk level thresholds

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/risk/levels",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "levels": [
    {
      "level": "minimal",
      "score_range": "0-20",
      "planning_required": false,
      "description": "No significant risk factors. Planning optional."
    },
    {
      "level": "low",
      "score_range": "21-40",
      "planning_required": false,
      "description": "Minor risk factors. Planning recommended."
    },
    {
      "level": "medium",
      "score_range": "41-60",
      "planning_required": true,
      "description": "Moderate risk factors. Planning strongly recommended."
    },
    {
      "level": "high",
      "score_range": "61-80",
      "planning_required": true,
      "description": "High risk factors. Planning required."
    },
    {
      "level": "critical",
      "score_range": "81-100",
      "planning_required": true,
      "description": "Critical risk factors. Planning + CRP required."
    }
  ],
  "thresholds": {
    "planning_recommended": 20,
    "planning_required": 50,
    "crp_required": 70
  },
  "loc_thresholds": {
 
... (truncated)
```

---

#### GET /api/v1/sast/health

**Summary**: SAST health check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 1828ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/sast/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "degraded",
  "semgrep_available": false,
  "custom_rules": {
    "ai_security": false,
    "owasp_python": false
  },
  "timestamp": "2026-02-21T06:32:53.800633"
}
```

---

#### GET /api/v1/sop/health

**Summary**: SOP Generator health check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 20ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/sop/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "healthy",
  "service": "sop_generator",
  "version": "1.0.0",
  "ollama": {
    "status": "error: HTTPConnectionPool(host='ollama', port=11434): Max retries exceeded with url: /api/tags (Caused by NameResolutionError(\"HTTPConnection(host='ollama', port=11434): Failed to resolve 'ollama' ([Errno -2] Name or service not known)\"))",
    "url": "http://ollama:11434",
    "model": "qwen3:14b",
    "available_models": []
  },
  "sase_level": "Level 1 (BRS + MRP + VCR)",
  "brs_reference": "BRS-PILOT-001"
}
```

---

#### GET /api/v1/sop/list

**Summary**: List generated SOPs

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/sop/list",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "page_size": 20
}
```

---

#### GET /api/v1/stage-gating/health

**Summary**: Stage gating health check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/stage-gating/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "healthy",
  "service": "stage_gating",
  "stages_configured": 11,
  "timestamp": "2026-02-21T06:32:55.344963"
}
```

---

#### GET /api/v1/stage-gating/rules

**Summary**: Get all stage rules

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/stage-gating/rules",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "stages": {
    "stage_00_foundation": {
      "stage": "stage_00_foundation",
      "allows": [
        "docs/00-foundation/**",
        "docs/00-discover/**",
        "README.md",
        ".gitignore",
        "LICENSE",
        "CLAUDE.md",
        "AGENTS.md",
        ".github/**"
      ],
      "blocks": [
        "src/**",
        "backend/**",
        "frontend/**",
        "app/**"
      ],
      "requires_complete": [],
      "requires_for_pr": [],
      "blocks_new_features": false,
      "message": "Foundation stage not complete. Cannot write code yet. Complete: docs/00-foundation/03-Problem-Statement.md"
    },
    "stage_01_planning": {
      "stage": "stage_01_planning",
      "allows": [
        "docs/01-planning/**",
        "docs/00-foundation/**",
        "docs/00-discover/**",
        "README.md",
        ".github/**"
      ],
      "blocks": [
        "src/**",
        "backend/app/**",
        "frontend/src/**"
      ],
      "requires_complete": [
        "sta
... (truncated)
```

---

#### GET /api/v1/telemetry/health

**Summary**: Telemetry Health

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 15ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/telemetry/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "unhealthy",
  "service": "telemetry",
  "error": "[Errno -2] Name or service not known"
}
```

---

#### GET /health

**Summary**: Health Check

**Status**: SUCCESS

**Root Cause**: ✅ Success - 200

**Latency**: 7ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "healthy",
  "version": "1.2.0",
  "service": "sdlc-orchestrator-backend"
}
```

---

*... and 2 more endpoints with SUCCESS status*

### AUTH_REQUIRED (488 endpoints)

#### GET /api/v1/admin/ai-providers/config

**Summary**: Get AI provider configuration

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 14ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/ai-providers/config",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/admin/ai-providers/ollama/refresh-models

**Summary**: Refresh Ollama models

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 7ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/admin/ai-providers/ollama/refresh-models",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### PATCH /api/v1/admin/ai-providers/{provider}

**Summary**: Update provider settings

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 10ms

**Request**:
```json
{
  "method": "PATCH",
  "url": "http://localhost:8300/api/v1/admin/ai-providers/ollama",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/admin/ai-providers/{provider}/models

**Summary**: Get available models for provider

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 7ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/ai-providers/ollama/models",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/admin/ai-providers/{provider}/test

**Summary**: Test provider connection

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 12ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/admin/ai-providers/ollama/test",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/admin/audit-logs

**Summary**: List audit logs (paginated)

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 15ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/audit-logs",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/admin/evidence/retention-archive

**Summary**: Trigger evidence archival (ADR-027)

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 9ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/admin/evidence/retention-archive",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "gate_id": 1,
    "type": "TEST_RESULTS",
    "description": "Test evidence"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/admin/evidence/retention-purge

**Summary**: Trigger evidence purge (ADR-027)

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 9ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/admin/evidence/retention-purge",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "gate_id": 1,
    "type": "TEST_RESULTS",
    "description": "Test evidence"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/admin/evidence/retention-stats

**Summary**: Get evidence retention statistics (ADR-027)

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/evidence/retention-stats",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/admin/override-queue

**Summary**: Get override approval queue

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 12ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/override-queue",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/admin/override-stats

**Summary**: Get override statistics

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/override-stats",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/admin/settings

**Summary**: Get all system settings

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/settings",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/admin/settings/{key}

**Summary**: Get setting by key

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 9ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/settings/test_key",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### PATCH /api/v1/admin/settings/{key}

**Summary**: Update setting

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 10ms

**Request**:
```json
{
  "method": "PATCH",
  "url": "http://localhost:8300/api/v1/admin/settings/test_key",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/admin/settings/{key}/rollback

**Summary**: Rollback setting

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 11ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/admin/settings/test_key/rollback",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/admin/stats

**Summary**: Get admin dashboard statistics

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 12ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/stats",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/admin/system/health

**Summary**: Get system health

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 12ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/system/health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/admin/users

**Summary**: List all users (paginated)

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/users",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/admin/users

**Summary**: Create new user

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 12ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/admin/users",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### DELETE /api/v1/admin/users/bulk

**Summary**: Bulk delete users (soft delete)

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 10ms

**Request**:
```json
{
  "method": "DELETE",
  "url": "http://localhost:8300/api/v1/admin/users/bulk",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/admin/users/bulk

**Summary**: Bulk user action

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 11ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/admin/users/bulk",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### DELETE /api/v1/admin/users/{user_id}

**Summary**: Delete user (soft delete)

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 9ms

**Request**:
```json
{
  "method": "DELETE",
  "url": "http://localhost:8300/api/v1/admin/users/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/admin/users/{user_id}

**Summary**: Get user details

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/users/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### PATCH /api/v1/admin/users/{user_id}

**Summary**: Update user

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 9ms

**Request**:
```json
{
  "method": "PATCH",
  "url": "http://localhost:8300/api/v1/admin/users/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/admin/users/{user_id}/mfa-exempt

**Summary**: Set MFA exemption (ADR-027)

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 10ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/admin/users/1/mfa-exempt",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/admin/users/{user_id}/mfa-status

**Summary**: Get user MFA status (ADR-027)

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 13ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/admin/users/1/mfa-status",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### DELETE /api/v1/admin/users/{user_id}/permanent

**Summary**: Permanently delete user (Sprint 105)

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 9ms

**Request**:
```json
{
  "method": "DELETE",
  "url": "http://localhost:8300/api/v1/admin/users/1/permanent",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/admin/users/{user_id}/restore

**Summary**: Restore deleted user (Sprint 105)

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 10ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/admin/users/1/restore",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/admin/users/{user_id}/unlock

**Summary**: Unlock user account (ADR-027)

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 9ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/admin/users/1/unlock",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/agent-team/conversations

**Summary**: List conversations

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 13ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/agent-team/conversations",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/agent-team/conversations

**Summary**: Start conversation

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 12ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/agent-team/conversations",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "agent_id": 1,
    "project_id": 1,
    "initial_message": "Test message"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/agent-team/conversations/{conversation_id}

**Summary**: Get conversation

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/agent-team/conversations/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/agent-team/conversations/{conversation_id}/interrupt

**Summary**: Interrupt conversation

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 12ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/agent-team/conversations/1/interrupt",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "agent_id": 1,
    "project_id": 1,
    "initial_message": "Test message"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/agent-team/conversations/{conversation_id}/messages

**Summary**: Get messages

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/agent-team/conversations/1/messages",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/agent-team/conversations/{conversation_id}/messages

**Summary**: Send message

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 10ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/agent-team/conversations/1/messages",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "agent_id": 1,
    "project_id": 1,
    "initial_message": "Test message"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/agent-team/definitions

**Summary**: List agent definitions

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 13ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/agent-team/definitions",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/agent-team/definitions

**Summary**: Create agent definition

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 12ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/agent-team/definitions",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "name": "Test Agent",
    "role": "DEVELOPER",
    "system_prompt": "Test agent",
    "provider": "ollama"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/agent-team/definitions/{definition_id}

**Summary**: Get agent definition

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 9ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/agent-team/definitions/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### PUT /api/v1/agent-team/definitions/{definition_id}

**Summary**: Update agent definition

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 7ms

**Request**:
```json
{
  "method": "PUT",
  "url": "http://localhost:8300/api/v1/agent-team/definitions/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "name": "Test Agent",
    "role": "DEVELOPER",
    "system_prompt": "Test agent",
    "provider": "ollama"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/agents-md/context/{project_id}

**Summary**: Get context overlay

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 14ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/agents-md/context/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/agents-md/context/{project_id}/history

**Summary**: Get context overlay history

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 6ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/agents-md/context/1/history",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/agents-md/generate

**Summary**: Generate AGENTS.md

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 6ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/agents-md/generate",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/agents-md/lint

**Summary**: Lint AGENTS.md

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 6ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/agents-md/lint",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/agents-md/repos

**Summary**: List all repositories with AGENTS.md status

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 6ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/agents-md/repos",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/agents-md/validate

**Summary**: Validate AGENTS.md

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 8ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/agents-md/validate",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/agents-md/{project_id}

**Summary**: Get latest AGENTS.md

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 12ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/agents-md/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/agents-md/{project_id}/history

**Summary**: Get AGENTS.md history

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 7ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/agents-md/1/history",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/analytics/circuit-breaker/status

**Summary**: Get Circuit Breaker Status

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/analytics/circuit-breaker/status",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### GET /api/v1/analytics/engagement

**Summary**: Get Engagement Summary

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/analytics/engagement",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### POST /api/v1/analytics/events

**Summary**: Track Event

**Status**: AUTH_REQUIRED

**Root Cause**: 🔒 Invalid or missing authentication token (JWT required)

**Latency**: 10ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/analytics/events",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

*... and 438 more endpoints with AUTH_REQUIRED status*

### NOT_FOUND (8 endpoints)

#### POST /api/v1/ai-detection/circuit-breakers/{breaker_name}/reset

**Summary**: Reset Circuit Breaker

**Status**: NOT_FOUND

**Root Cause**: ❌ Endpoint not found - /api/v1/ai-detection/circuit-breakers/{breaker_name}/reset may not be implemented

**Latency**: 12ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/ai-detection/circuit-breakers/test/reset",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": "Circuit breaker 'test' not found. Available: ['github_api', 'external_ai']"
}
```

---

#### GET /api/v1/codegen/preview/{token}

**Summary**: Get Preview

**Status**: NOT_FOUND

**Root Cause**: ❌ Endpoint not found - /api/v1/codegen/preview/{token} may not be implemented

**Latency**: 12ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/codegen/preview/{token}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Preview not found or expired"
}
```

---

#### GET /api/v1/context-authority/adrs/{adr_id}

**Summary**: [DEPRECATED] Get specific ADR

**Status**: NOT_FOUND

**Root Cause**: ❌ Endpoint not found - /api/v1/context-authority/adrs/{adr_id} may not be implemented

**Latency**: 16ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-authority/adrs/{adr_id}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "ADR not found: {adr_id}"
}
```

---

#### GET /api/v1/docs/user-support/{filename}

**Summary**: Get User Support Doc

**Status**: NOT_FOUND

**Root Cause**: ❌ Endpoint not found - /api/v1/docs/user-support/{filename} may not be implemented

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/docs/user-support/{filename}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Documentation file '{filename}' not found"
}
```

---

#### GET /api/v1/sop/{sop_id}

**Summary**: Get SOP details

**Status**: NOT_FOUND

**Root Cause**: ❌ Endpoint not found - /api/v1/sop/{sop_id} may not be implemented

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/sop/{sop_id}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "SOP not found: {sop_id}"
}
```

---

#### GET /api/v1/sop/{sop_id}/mrp

**Summary**: Get MRP evidence for SOP

**Status**: NOT_FOUND

**Root Cause**: ❌ Endpoint not found - /api/v1/sop/{sop_id}/mrp may not be implemented

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/sop/{sop_id}/mrp",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "SOP not found: {sop_id}"
}
```

---

#### GET /api/v1/sop/{sop_id}/vcr

**Summary**: Get VCR decision for SOP

**Status**: NOT_FOUND

**Root Cause**: ❌ Endpoint not found - /api/v1/sop/{sop_id}/vcr may not be implemented

**Latency**: 4ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/sop/{sop_id}/vcr",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "SOP not found: {sop_id}"
}
```

---

#### GET /api/v1/stage-gating/rules/{stage}

**Summary**: Get rules for specific stage

**Status**: NOT_FOUND

**Root Cause**: ❌ Endpoint not found - /api/v1/stage-gating/rules/{stage} may not be implemented

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/stage-gating/rules/{stage}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Stage not found: {stage}"
}
```

---

### CLIENT_ERROR (69 endpoints)

#### POST /api/v1/ai-detection/analyze

**Summary**: Analyze Pr

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'pr_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'title'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 13ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/ai-detection/analyze",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "pr_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "title"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/auth/forgot-password

**Summary**: Forgot Password

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'email'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 17ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/auth/forgot-password",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "email"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/auth/github/token

**Summary**: Github Device Flow Poll

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'device_code'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 13ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/auth/github/token",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "device_code"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/auth/login

**Summary**: Login

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'email'], 'msg': 'Field required', 'input': {'username': 'test', 'password': 'test'}}]

**Latency**: 9ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/auth/login",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "username": "test",
    "password": "test"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "email"
      ],
      "msg": "Field required",
      "input": {
        "username": "test",
        "password": "test"
      }
    }
  ],
  "body": "{'username': 'test', 'password': 'test'}"
}
```

---

#### GET /api/v1/auth/oauth/{provider}/authorize

**Summary**: Oauth Authorize

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Bad request - Invalid OAuth provider. Valid options: github, google

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/auth/oauth/ollama/authorize",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Invalid OAuth provider. Valid options: github, google"
}
```

---

#### POST /api/v1/auth/oauth/{provider}/callback

**Summary**: Oauth Callback

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'code'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'state'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 18ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/auth/oauth/ollama/callback",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "code"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "state"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/auth/reset-password

**Summary**: Reset Password

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'token'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'new_password'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 14ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/auth/reset-password",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "token"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "new_password"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### GET /api/v1/auth/verify-reset-token

**Summary**: Verify Reset Token

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['query', 'token'], 'msg': 'Field required', 'input': None}]

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/auth/verify-reset-token",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "token"
      ],
      "msg": "Field required",
      "input": null
    }
  ],
  "body": null
}
```

---

#### POST /api/v1/ceo-dashboard/decisions/{submission_id}/override

**Summary**: Record CEO override for calibration

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'override_type'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'pr_number'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'pr_title'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_name'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecoding_index'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'original_routing'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 51ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/ceo-dashboard/decisions/{submission_id}/override",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "override_type"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "pr_number"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "pr_title"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "project_name"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "vibecoding_index"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "original_routin
... (truncated)
```

---

#### POST /api/v1/ceo-dashboard/decisions/{submission_id}/resolve

**Summary**: Resolve pending CEO decision

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'decision'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 13ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/ceo-dashboard/decisions/{submission_id}/resolve",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "decision"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/ceo-dashboard/submissions

**Summary**: Record governance submission

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'submission_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecoding_index'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'routing'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'status'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 9ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/ceo-dashboard/submissions",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "submission_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "project_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "vibecoding_index"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "routing"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "status"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/context-authority/check-adr-linkage

**Summary**: [DEPRECATED] Check ADR linkage for modules

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'modules'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 13ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/context-authority/check-adr-linkage",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "modules"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/context-authority/check-spec

**Summary**: [DEPRECATED] Check design spec existence

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'task_id'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 14ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/context-authority/check-spec",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "task_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/context-authority/v2/overlay

**Summary**: Generate dynamic overlay

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_tier'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'gate_status'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 7ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/context-authority/v2/overlay",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "project_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "project_tier"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "gate_status"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### GET /api/v1/context-authority/v2/snapshot/{submission_id}

**Summary**: Get context snapshot

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'submission_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `s` at 2', 'input': '{submission_id}', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `s` at 2'}}]

**Latency**: 9ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-authority/v2/snapshot/{submission_id}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "uuid_parsing",
      "loc": [
        "path",
        "submission_id"
      ],
      "msg": "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `s` at 2",
      "input": "{submission_id}",
      "ctx": {
        "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `s` at 2"
      }
    }
  ],
  "body": null
}
```

---

#### GET /api/v1/context-authority/v2/snapshots/{project_id}

**Summary**: List project snapshots

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'project_id'], 'msg': 'Input should be a valid UUID, invalid length: expected length 32 for simple format, found 1', 'input': '1', 'ctx': {'error': 'invalid length: expected length 32 for simple format, found 1'}}]

**Latency**: 9ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-authority/v2/snapshots/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "uuid_parsing",
      "loc": [
        "path",
        "project_id"
      ],
      "msg": "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 1",
      "input": "1",
      "ctx": {
        "error": "invalid length: expected length 32 for simple format, found 1"
      }
    }
  ],
  "body": null
}
```

---

#### POST /api/v1/context-authority/v2/templates

**Summary**: Create overlay template

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'name'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'trigger_type'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'trigger_value'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'overlay_content'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 10ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/context-authority/v2/templates",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "name"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "trigger_type"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "trigger_value"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "overlay_content"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### GET /api/v1/context-authority/v2/templates/{template_id}

**Summary**: Get template by ID

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'template_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2', 'input': '{template_id}', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2'}}]

**Latency**: 13ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-authority/v2/templates/{template_id}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "uuid_parsing",
      "loc": [
        "path",
        "template_id"
      ],
      "msg": "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2",
      "input": "{template_id}",
      "ctx": {
        "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2"
      }
    }
  ],
  "body": null
}
```

---

#### PUT /api/v1/context-authority/v2/templates/{template_id}

**Summary**: Update template

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'template_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2', 'input': '{template_id}', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2'}}]

**Latency**: 22ms

**Request**:
```json
{
  "method": "PUT",
  "url": "http://localhost:8300/api/v1/context-authority/v2/templates/{template_id}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "uuid_parsing",
      "loc": [
        "path",
        "template_id"
      ],
      "msg": "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2",
      "input": "{template_id}",
      "ctx": {
        "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### GET /api/v1/context-authority/v2/templates/{template_id}/usage

**Summary**: Get template usage statistics

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'template_id'], 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2', 'input': '{template_id}', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2'}}]

**Latency**: 20ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-authority/v2/templates/{template_id}/usage",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "uuid_parsing",
      "loc": [
        "path",
        "template_id"
      ],
      "msg": "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2",
      "input": "{template_id}",
      "ctx": {
        "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `t` at 2"
      }
    }
  ],
  "body": null
}
```

---

#### POST /api/v1/context-authority/v2/validate

**Summary**: Gate-aware context validation

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'submission_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_tier'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecoding_index'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecoding_zone'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'gate_status'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 12ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/context-authority/v2/validate",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "submission_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "project_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "project_tier"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "vibecoding_index"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "vibecoding_zone"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "gate_st
... (truncated)
```

---

#### POST /api/v1/context-authority/validate

**Summary**: [DEPRECATED] Validate code context linkage

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'submission_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'changed_files'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 13ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/context-authority/validate",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "submission_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "project_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "changed_files"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### GET /api/v1/doc-cross-reference/links

**Summary**: Get document links

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['query', 'project_id'], 'msg': 'Field required', 'input': None}, {'type': 'missing', 'loc': ['query', 'document_path'], 'msg': 'Field required', 'input': None}]

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/doc-cross-reference/links",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "project_id"
      ],
      "msg": "Field required",
      "input": null
    },
    {
      "type": "missing",
      "loc": [
        "query",
        "document_path"
      ],
      "msg": "Field required",
      "input": null
    }
  ],
  "body": null
}
```

---

#### GET /api/v1/doc-cross-reference/orphaned

**Summary**: Get orphaned documents

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['query', 'project_id'], 'msg': 'Field required', 'input': None}]

**Latency**: 9ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/doc-cross-reference/orphaned",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "project_id"
      ],
      "msg": "Field required",
      "input": null
    }
  ],
  "body": null
}
```

---

#### POST /api/v1/doc-cross-reference/validate

**Summary**: Validate single document

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'document_path'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 11ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/doc-cross-reference/validate",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "project_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "document_path"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/doc-cross-reference/validate-project

**Summary**: Validate entire project

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'project_path'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 9ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/doc-cross-reference/validate-project",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "project_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "project_path"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/dogfooding/enforce/soft

**Summary**: Enforce Soft Mode

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'pr_number'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecoding_index'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'zone'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 23ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/dogfooding/enforce/soft",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "pr_number"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "vibecoding_index"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "zone"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/dogfooding/prs/record

**Summary**: Record Pr Metric

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'pr_number'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'title'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'author'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecode_index'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'zone'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'friction_minutes'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 13ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/dogfooding/prs/record",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "pr_number"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "title"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "author"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "vibecode_index"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "zone"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "friction_minutes"
      ],
      "m
... (truncated)
```

---

#### POST /api/v1/gates-engine/bulk-evaluate

**Summary**: Evaluate multiple gates

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'uuid_type', 'loc': ['body', 'project_id'], 'msg': 'UUID input should be a string, bytes or UUID object', 'input': 1}]

**Latency**: 18ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/gates-engine/bulk-evaluate",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "project_id": 1,
    "gate_type": "G1_CONSULTATION",
    "name": "Test Gate",
    "description": "Test gate for API testing"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "uuid_type",
      "loc": [
        "body",
        "project_id"
      ],
      "msg": "UUID input should be a string, bytes or UUID object",
      "input": 1
    }
  ],
  "body": "{'project_id': 1, 'gate_type': 'G1_CONSULTATION', 'name': 'Test Gate', 'description': 'Test gate for API testing'}"
}
```

---

#### POST /api/v1/gates-engine/evaluate-by-code

**Summary**: Evaluate gate by project and code

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'uuid_type', 'loc': ['body', 'project_id'], 'msg': 'UUID input should be a string, bytes or UUID object', 'input': 1}, {'type': 'missing', 'loc': ['body', 'gate_code'], 'msg': 'Field required', 'input': {'project_id': 1, 'gate_type': 'G1_CONSULTATION', 'name': 'Test Gate', 'description': 'Test gate for API testing'}}]

**Latency**: 21ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/gates-engine/evaluate-by-code",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "project_id": 1,
    "gate_type": "G1_CONSULTATION",
    "name": "Test Gate",
    "description": "Test gate for API testing"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "uuid_type",
      "loc": [
        "body",
        "project_id"
      ],
      "msg": "UUID input should be a string, bytes or UUID object",
      "input": 1
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "gate_code"
      ],
      "msg": "Field required",
      "input": {
        "project_id": 1,
        "gate_type": "G1_CONSULTATION",
        "name": "Test Gate",
        "description": "Test gate for API testing"
      }
    }
  ],
  "body": "{'project_id': 1, 'gate_type': 'G1_CONSULTATION', 'name': 'Test Gate', 'description': 'Test gate for API testing'}"
}
```

---

#### POST /api/v1/gates-engine/evaluate/{gate_id}

**Summary**: Evaluate single gate

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'gate_id'], 'msg': 'Input should be a valid UUID, invalid length: expected length 32 for simple format, found 1', 'input': '1', 'ctx': {'error': 'invalid length: expected length 32 for simple format, found 1'}}]

**Latency**: 13ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/gates-engine/evaluate/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "project_id": 1,
    "gate_type": "G1_CONSULTATION",
    "name": "Test Gate",
    "description": "Test gate for API testing"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "uuid_parsing",
      "loc": [
        "path",
        "gate_id"
      ],
      "msg": "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 1",
      "input": "1",
      "ctx": {
        "error": "invalid length: expected length 32 for simple format, found 1"
      }
    }
  ],
  "body": "{'project_id': 1, 'gate_type': 'G1_CONSULTATION', 'name': 'Test Gate', 'description': 'Test gate for API testing'}"
}
```

---

#### GET /api/v1/gates-engine/policies/{gate_code}

**Summary**: Get policies for gate

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Bad request - Invalid gate code: {gate_code}. Valid codes: G0.1, G0.2, G1, G2, G3, G4, G5, G6, G7, G8, G9

**Latency**: 8ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/gates-engine/policies/{gate_code}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Invalid gate code: {gate_code}. Valid codes: G0.1, G0.2, G1, G2, G3, G4, G5, G6, G7, G8, G9"
}
```

---

#### GET /api/v1/gates-engine/prerequisites/{gate_code}

**Summary**: Check gate prerequisites

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Bad request - Invalid gate code: {gate_code}. Valid codes: G0.1, G0.2, G1, G2, G3, G4, G5, G6, G7, G8, G9

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/gates-engine/prerequisites/{gate_code}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Invalid gate code: {gate_code}. Valid codes: G0.1, G0.2, G1, G2, G3, G4, G5, G6, G7, G8, G9"
}
```

---

#### GET /api/v1/gates-engine/readiness/{project_id}

**Summary**: Get project gate readiness

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'uuid_parsing', 'loc': ['path', 'project_id'], 'msg': 'Input should be a valid UUID, invalid length: expected length 32 for simple format, found 1', 'input': '1', 'ctx': {'error': 'invalid length: expected length 32 for simple format, found 1'}}]

**Latency**: 12ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/gates-engine/readiness/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "uuid_parsing",
      "loc": [
        "path",
        "project_id"
      ],
      "msg": "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 1",
      "input": "1",
      "ctx": {
        "error": "invalid length: expected length 32 for simple format, found 1"
      }
    }
  ],
  "body": null
}
```

---

#### POST /api/v1/governance-metrics/record-break-glass

**Summary**: Record break glass activation

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'severity'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 12ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/governance-metrics/record-break-glass",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "severity"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/governance-metrics/record-bypass

**Summary**: Record governance bypass incident

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'bypass_type'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 8ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/governance-metrics/record-bypass",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "bypass_type"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/governance-metrics/record-ceo-override

**Summary**: Record CEO override

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'override_type'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 8ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/governance-metrics/record-ceo-override",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "project_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "override_type"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/governance-metrics/record-developer-friction

**Summary**: Record developer friction

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'friction_minutes'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 10ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/governance-metrics/record-developer-friction",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "project_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "friction_minutes"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/governance-metrics/record-evidence

**Summary**: Record evidence upload

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'evidence_type'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'size_bytes'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 10ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/governance-metrics/record-evidence",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "project_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "evidence_type"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "size_bytes"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/governance-metrics/record-llm

**Summary**: Record LLM generation metrics

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'provider'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'model'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'duration_seconds'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'success'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 8ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/governance-metrics/record-llm",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "provider"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "model"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "duration_seconds"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "success"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/governance-metrics/record-submission

**Summary**: Record governance submission metrics

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'project_id'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'status'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'vibecoding_index'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'routing'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'duration_seconds'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 9ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/governance-metrics/record-submission",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "project_id"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "status"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "vibecoding_index"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "routing"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "duration_seconds"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/governance-metrics/set-kill-switch

**Summary**: Set kill switch status

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'status'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 9ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/governance-metrics/set-kill-switch",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "status"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/governance-metrics/update-ceo-metrics

**Summary**: Update CEO dashboard metrics

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'week'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'time_saved_hours'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'pr_review_reduction_percent'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'governance_without_ceo_percent'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'false_positive_rate'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 9ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/governance-metrics/update-ceo-metrics",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "week"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "time_saved_hours"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "pr_review_reduction_percent"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "governance_without_ceo_percent"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "false_positive_rate"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/governance-metrics/update-system-health

**Summary**: Update system health metrics

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'cpu_percent'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'memory_percent'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 10ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/governance-metrics/update-system-health",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "cpu_percent"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "memory_percent"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### GET /api/v1/grafana-dashboards/{dashboard_type}

**Summary**: Get dashboard configuration

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Bad request - Invalid dashboard type: {dashboard_type}. Valid types: ceo, tech, ops

**Latency**: 5ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/grafana-dashboards/{dashboard_type}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Invalid dashboard type: {dashboard_type}. Valid types: ceo, tech, ops"
}
```

---

#### GET /api/v1/grafana-dashboards/{dashboard_type}/json

**Summary**: Download dashboard JSON

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Bad request - Invalid dashboard type: {dashboard_type}. Valid types: ceo, tech, ops

**Latency**: 11ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/grafana-dashboards/{dashboard_type}/json",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Invalid dashboard type: {dashboard_type}. Valid types: ceo, tech, ops"
}
```

---

#### GET /api/v1/grafana-dashboards/{dashboard_type}/panels

**Summary**: List dashboard panels

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Bad request - Invalid dashboard type: {dashboard_type}. Valid types: ceo, tech, ops

**Latency**: 10ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/grafana-dashboards/{dashboard_type}/panels",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Invalid dashboard type: {dashboard_type}. Valid types: ceo, tech, ops"
}
```

---

#### POST /api/v1/sast/scan-snippet

**Summary**: Scan code snippet

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'code'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'language'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 11ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/sast/scan-snippet",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "code"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "language"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/sop/generate

**Summary**: Generate SOP from workflow description

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'sop_type'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'workflow_description'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 13ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/sop/generate",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "sop_type"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "workflow_description"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

#### POST /api/v1/sop/{sop_id}/vcr

**Summary**: Submit VCR decision for SOP

**Status**: CLIENT_ERROR

**Root Cause**: ⚠️ Validation error - [{'type': 'missing', 'loc': ['body', 'decision'], 'msg': 'Field required', 'input': {'test': 'data'}}, {'type': 'missing', 'loc': ['body', 'reviewer'], 'msg': 'Field required', 'input': {'test': 'data'}}]

**Latency**: 5ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/sop/{sop_id}/vcr",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "decision"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "reviewer"
      ],
      "msg": "Field required",
      "input": {
        "test": "data"
      }
    }
  ],
  "body": "{'test': 'data'}"
}
```

---

*... and 19 more endpoints with CLIENT_ERROR status*

### SERVER_ERROR (8 endpoints)

#### POST /api/v1/api/v1/github/webhooks

**Summary**: GitHub webhook handler

**Status**: SERVER_ERROR

**Root Cause**: 🔥 Server error - 500: {'error': 'webhook_not_configured', 'message': 'GITHUB_APP_WEBHOOK_SECRET not set'}

**Latency**: 59ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/api/v1/github/webhooks",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
{
  "detail": {
    "error": "webhook_not_configured",
    "message": "GITHUB_APP_WEBHOOK_SECRET not set"
  }
}
```

---

#### GET /api/v1/api/v1/org-invitations/{token}

**Summary**: Get organization invitation details by token

**Status**: SERVER_ERROR

**Root Cause**: 🔥 Server error - 500: 

**Latency**: 41ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/api/v1/org-invitations/{token}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
Internal Server Error
```

---

#### POST /api/v1/api/v1/org-invitations/{token}/decline

**Summary**: Decline organization invitation

**Status**: SERVER_ERROR

**Root Cause**: 🔥 Server error - 500: 

**Latency**: 12ms

**Request**:
```json
{
  "method": "POST",
  "url": "http://localhost:8300/api/v1/api/v1/org-invitations/{token}/decline",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "test": "data"
  }
}
```

**Response**:
```json
Internal Server Error
```

---

#### GET /api/v1/context-authority/v2/stats

**Summary**: Get statistics

**Status**: SERVER_ERROR

**Root Cause**: 🔥 Server error - 500: Failed to get statistics: [Errno -2] Name or service not known

**Latency**: 15ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-authority/v2/stats",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Failed to get statistics: [Errno -2] Name or service not known"
}
```

---

#### GET /api/v1/context-authority/v2/templates

**Summary**: List overlay templates

**Status**: SERVER_ERROR

**Root Cause**: 🔥 Server error - 500: Failed to list templates: [Errno -2] Name or service not known

**Latency**: 17ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-authority/v2/templates",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "detail": "Failed to list templates: [Errno -2] Name or service not known"
}
```

---

#### GET /api/v1/context-validation/limits

**Summary**: Get context limits configuration

**Status**: SERVER_ERROR

**Root Cause**: 🔥 Server error - 500: 

**Latency**: 22ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/context-validation/limits",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
Internal Server Error
```

---

#### GET /api/v1/governance/tiers/

**Summary**: List All Tiers

**Status**: SERVER_ERROR

**Root Cause**: 🔥 Server error - 500: 

**Latency**: 17ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/api/v1/governance/tiers/",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
Internal Server Error
```

---

#### GET /health/ready

**Summary**: Readiness Check

**Status**: SERVER_ERROR

**Root Cause**: 🔥 Server error - 503: 

**Latency**: 5940ms

**Request**:
```json
{
  "method": "GET",
  "url": "http://localhost:8300/health/ready",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

**Response**:
```json
{
  "status": "not_ready",
  "dependencies": {
    "postgres": {
      "status": "disconnected",
      "healthy": false,
      "error": "[Errno -2] Name or service not known"
    },
    "redis": {
      "status": "connected",
      "healthy": true
    },
    "opa": {
      "status": "connected",
      "healthy": true,
      "version": "unknown"
    },
    "minio": {
      "status": "disconnected",
      "healthy": false,
      "error": "Could not connect to the endpoint URL: \"http://ai-platform-minio:9000/evidence-vault-v2\""
    },
    "scheduler": {
      "status": "running",
      "healthy": true,
      "jobs_count": 4
    }
  }
}
```

---

### ERROR (10 endpoints)

#### GET /api/v1/ceo-dashboard/overrides

**Summary**: Get CEO overrides this week

**Status**: ERROR

**Root Cause**: Exception: 'list' object has no attribute 'get'

**Latency**: 0ms

---

#### GET /api/v1/ceo-dashboard/pending-decisions

**Summary**: Get pending CEO decisions queue

**Status**: ERROR

**Root Cause**: Exception: 'list' object has no attribute 'get'

**Latency**: 0ms

---

#### GET /api/v1/ceo-dashboard/top-rejections

**Summary**: Get top rejection reasons

**Status**: ERROR

**Root Cause**: Exception: 'list' object has no attribute 'get'

**Latency**: 0ms

---

#### GET /api/v1/ceo-dashboard/trends/time-saved

**Summary**: Get time saved trend (8 weeks)

**Status**: ERROR

**Root Cause**: Exception: 'list' object has no attribute 'get'

**Latency**: 0ms

---

#### GET /api/v1/ceo-dashboard/trends/vibecoding-index

**Summary**: Get vibecoding index trend (7 days)

**Status**: ERROR

**Root Cause**: Exception: 'list' object has no attribute 'get'

**Latency**: 0ms

---

#### GET /api/v1/docs/user-support

**Summary**: List User Support Docs

**Status**: ERROR

**Root Cause**: Exception: 'list' object has no attribute 'get'

**Latency**: 0ms

---

#### GET /api/v1/dogfooding/export/prometheus

**Summary**: Export Prometheus Metrics

**Status**: ERROR

**Root Cause**: Exception: 'str' object has no attribute 'get'

**Latency**: 0ms

---

#### GET /api/v1/grafana-dashboards/export/all

**Summary**: Export all dashboards

**Status**: ERROR

**Root Cause**: Exception: 'list' object has no attribute 'get'

**Latency**: 0ms

---

#### GET /api/v1/risk/factors

**Summary**: List 7 mandatory risk factors

**Status**: ERROR

**Root Cause**: Exception: 'list' object has no attribute 'get'

**Latency**: 0ms

---

#### GET /api/v1/sop/types

**Summary**: List supported SOP types

**Status**: ERROR

**Root Cause**: Exception: 'list' object has no attribute 'get'

**Latency**: 0ms

---

## 💡 Recommendations

1. **Authentication**: 488 endpoints require authentication. Create test users and obtain JWT tokens.
2. **Missing Resources**: 8 endpoints returned 404. Seed test data (projects, gates, evidence) to test fully.
3. **Server Errors**: 8 endpoints have server errors. Check backend logs for details.

---

**Report Generated**: 2026-02-21 13:33:04
**Testing Tool**: SDLC Orchestrator API Tester
