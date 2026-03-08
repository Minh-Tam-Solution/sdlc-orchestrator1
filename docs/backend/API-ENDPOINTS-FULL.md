<!-- *-CyEyes-* -->
# *-CyEyes-* API Endpoints — Full Coverage Report (Sessions 3+4+5)

> **Generated**: 2026-03-08 12:09:09  
> **Server**: https://sdlc.nhatquangholding.com  
> **Auth**: `taidt@mtsolution.com.vn` (CTO/superuser)  
> **Sessions**: 3 + 4 + 5a + 5b (cumulative)  

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total unique endpoints tested | **572** |
| HTTP 200 ✅ | **190** (33%) |
| HTTP 2xx ⚠️ | **197** (34%) |
| HTTP 404 🔴 (not deployed) | **223** (38%) |
| HTTP 5xx 💥 (server errors) | **66** (11%) |
| OpenAPI spec paths | **517** |
| Coverage | **110%** |

## Status Code Breakdown

| Code | Count | Meaning |
|------|-------|---------|
| 0 | 1 | Network/connection error |
| 200 | 190 | OK — working correctly |
| 201 | 5 | Created — resource created |
| 204 | 2 | No Content — success, no body |
| 400 | 11 | Bad Request — wrong params/body |
| 404 | 223 | Not Found — route not deployed or wrong path |
| 405 | 14 | Method Not Allowed — wrong HTTP method |
| 409 | 1 | Conflict — resource already exists |
| 422 | 59 | Unprocessable — missing required param |
| 500 | 65 | Internal Server Error — DB migration missing or service error |
| 503 | 1 | Service Unavailable |

## Known HTTP 500 Root Causes

| Module | Endpoint | Root Cause |
|--------|----------|------------|
| Agent Team | — | Missing DB migration: `agent_definitions`, `agent_conversations`, `agent_messages` (Sprint 176 — s176_001_agent_team_tables.py not applied to production) |
| Agents Md Repos | — | GitHub repos fetch fails — GitHub App not configured |
| Codegen Usage | — | Codegen usage tables not populated / DB error |
| Consultations | — | DB error — `crp_submissions` table missing or schema mismatch (s101_002_crp_tables.py) |
| Context Authority | — | Missing DB migration: `ca_snapshots`, `ca_templates` (s120_001_context_authority_v2.py not applied) |
| Deprecation | — | DB error — deprecated tables query fails after Sprint 190 cleanup |
| Github | — | GitHub App not configured in production environment (missing GITHUB_APP_ID, GITHUB_PRIVATE_KEY) |
| Governance Tiers | — | DB error — `governance_tiers` table missing |
| Jira | — | Jira connection not configured in production |
| Maturity | — | Missing DB migration: `maturity_assessments` table (s104_001_maturity_assessments.py not applied) |
| Mcp | — | MCP service startup error — dependency not initialized |
| Ott Channels | — | OTT gateway not configured (missing TELEGRAM_BOT_TOKEN) |
| Sast | — | Missing DB migration: `sast_scans`, `sast_findings` (s209_004_add_sast_tables.py not applied) |
| Telemetry | — | DB error — telemetry events table not populated / query error |
| Vcr | — | Missing DB migration: `vcr_submissions`, `vcr_approvals` (s151_001_vcr.py not applied to production) |
| Workflows | — | Workflow conversation_id not found — needs valid agent conversation UUID |

## Working Endpoints (HTTP 200) ✅

**190 endpoints confirmed working**

| # | Method | Endpoint | Status | ms | Response |
|---|--------|----------|--------|-----|----------|
| 1 | `GET` | `/` | ✅ 200 | 15ms | "<!DOCTYPE html><html lang=\"vi\"><head><meta charSet=\"utf-8\"/><meta name=\"viewport\" content=\"w |
| 2 | `GET` | `/api/v1/admin/ai-providers/config` | ✅ 200 | 22ms | {"ollama": {"available": true, "configured": true, "url": "http://ollama:11434", "model": "qwen3:14b |
| 3 | `GET` | `/api/v1/admin/ai-providers/ollama/models` | ✅ 200 | 36ms | {"models": ["bge-m3:latest", "deepseek-ocr:3b", "gemma3:12b", "ministral-3:8b-instruct-2512-q4_K_M", |
| 4 | `POST` | `/api/v1/admin/ai-providers/ollama/refresh-models` | ✅ 200 | 29ms | {"models": ["bge-m3:latest", "deepseek-ocr:3b", "gemma3:12b", "ministral-3:8b-instruct-2512-q4_K_M", |
| 5 | `GET` | `/api/v1/admin/audit-logs` | ✅ 200 | 36ms | {"items": [{"id": "0e55df7e-a247-4dfa-9a3e-9023cdf0ac7a", "timestamp": "2026-03-08T11:56:44.275771", |
| 6 | `GET` | `/api/v1/admin/evidence/retention-stats` | ✅ 200 | 18ms | {"total_evidence": 2, "active_evidence": 2, "archived_evidence": 0, "evidence_due_for_archive": 0, " |
| 7 | `GET` | `/api/v1/admin/ott-channels/config` | ✅ 200 | 14ms | {"channels": [{"channel": "slack", "status": "offline", "tier": "PROFESSIONAL", "webhook_url": "http |
| 8 | `GET` | `/api/v1/admin/override-queue` | ✅ 200 | 22ms | {"pending": [], "recent_decisions": [], "total_pending": 0} |
| 9 | `GET` | `/api/v1/admin/override-stats` | ✅ 200 | 17ms | {"total": 0, "by_status": {}, "by_type": {}, "approval_rate": 0.0, "pending": 0, "days": 30} |
| 10 | `GET` | `/api/v1/admin/settings` | ✅ 200 | 13ms | {"security": [{"key": "max_login_attempts", "value": 5, "version": 2, "category": "security", "descr |
| 11 | `GET` | `/api/v1/admin/settings/max_login_attempts` | ✅ 200 | 14ms | {"key": "max_login_attempts", "value": 5, "version": 1, "category": "security", "description": "Maxi |
| 12 | `PATCH` | `/api/v1/admin/settings/max_login_attempts` | ✅ 200 | 23ms | {"key": "max_login_attempts", "value": 5, "version": 2, "category": "security", "description": "Maxi |
| 13 | `GET` | `/api/v1/admin/stats` | ✅ 200 | 14ms | {"total_users": 13, "active_users": 13, "inactive_users": 0, "superusers": 2, "total_projects": 7, " |
| 14 | `GET` | `/api/v1/admin/system/health` | ✅ 200 | 16ms | {"overall_status": "healthy", "services": [{"name": "PostgreSQL", "status": "healthy", "response_tim |
| 15 | `GET` | `/api/v1/admin/users` | ✅ 200 | 24ms | {"items": [{"id": "818d8908-481d-471b-8688-9a1b96878c4b", "email": "cyeyes-s4-1772877264@test.com",  |
| 16 | `GET` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d` | ✅ 200 | 17ms | {"id": "2e542eba-b1b5-4f91-ab82-b853a6887b8d", "email": "cyeyes-reg3@test.com", "full_name": null, " |
| 17 | `PATCH` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d` | ✅ 200 | 41ms | {"id": "2e542eba-b1b5-4f91-ab82-b853a6887b8d", "email": "cyeyes-reg3@test.com", "full_name": null, " |
| 18 | `GET` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/mfa-status` | ✅ 200 | 17ms | {"user_id": "2e542eba-b1b5-4f91-ab82-b853a6887b8d", "email": "cyeyes-reg3@test.com", "mfa_enabled":  |
| 19 | `GET` | `/api/v1/admin/users/a0000000-0000-0000-0000-000000000001` | ✅ 200 | 21ms | {"id": "a0000000-0000-0000-0000-000000000001", "email": "taidt@mtsolution.com.vn", "full_name": null |
| 20 | `GET` | `/api/v1/agent-team/presets` | ✅ 200 | 22ms | [{"name": "solo-dev", "description": "Single developer working alone", "roles": ["coder"], "delegati |
| 21 | `GET` | `/api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 35ms | {"id": "492cddc7-d13c-46f0-b9b0-b9bf15c3e951", "content": "# AGENTS.md - CyEyes-S4\n\n## Quick Start |
| 22 | `GET` | `/api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | ✅ 200 | 20ms | [{"id": "492cddc7-d13c-46f0-b9b0-b9bf15c3e951", "generated_at": "2026-03-07T09:54:40.834579+00:00",  |
| 23 | `GET` | `/api/v1/agents-md/context/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 35ms | {"id": "ab0a7a88-f96c-4a1a-aa41-3c48f18ea19b", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |
| 24 | `GET` | `/api/v1/agents-md/context/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | ✅ 200 | 22ms | [{"id": "ab0a7a88-f96c-4a1a-aa41-3c48f18ea19b", "generated_at": "2026-03-08T05:05:21.586040+00:00",  |
| 25 | `POST` | `/api/v1/agents-md/lint` | ✅ 200 | 14ms | {"original_content": "# Test", "fixed_content": "# Test\n", "changes": ["Added newline at end of fil |
| 26 | `POST` | `/api/v1/agents-md/validate` | ✅ 200 | 27ms | {"valid": true, "errors": [], "warnings": [{"severity": "warning", "message": "Missing recommended s |
| 27 | `GET` | `/api/v1/ai-detection/circuit-breakers` | ✅ 200 | 12ms | {"circuit_breakers": {"github_api": {"name": "github_api", "config": {"failure_threshold": 5, "recov |
| 28 | `GET` | `/api/v1/ai-detection/shadow-mode` | ✅ 200 | 12ms | {"status": "enabled", "config": {"enabled": true, "sample_rate": 1.0, "log_level": "INFO", "collect_ |
| 29 | `GET` | `/api/v1/ai-detection/status` | ✅ 200 | 17ms | {"service": "GitHubAIDetectionService", "version": "1.0.0", "detection_threshold": 0.5, "strategies" |
| 30 | `GET` | `/api/v1/ai-detection/tools` | ✅ 200 | 17ms | {"tools": [{"id": "cursor", "name": "Cursor"}, {"id": "copilot", "name": "Copilot"}, {"id": "claude_ |
| 31 | `GET` | `/api/v1/analytics/v2/metrics/ai-safety` | ✅ 200 | 14ms | {"period_days": 7, "total_validations": 0, "pass_rate": 0.0, "avg_duration_ms": 0.0, "top_tools": {} |
| 32 | `GET` | `/api/v1/analytics/v2/metrics/dau` | ✅ 200 | 18ms | {"start_date": "2026-02-06", "end_date": "2026-03-08", "daily_counts": {}, "total_unique_users": 0,  |
| 33 | `GET` | `/api/v1/api-keys` | ✅ 200 | 13ms | [{"id": "ce5a6ad5-adcb-4b95-bcf5-1a419a3835b4", "name": "*-CyEyes-* Key 1772860135", "prefix": "sdlc |
| 34 | `POST` | `/api/v1/auth/forgot-password` | ✅ 200 | 37ms | {"message": "If an account with this email exists, you will receive a password reset link.", "email" |
| 35 | `POST` | `/api/v1/auth/github/device` | ✅ 200 | 509ms | {"device_code": "5b46c60aa896d89ebf2bcea293cb2e1b6ec684b1", "user_code": "AF38-1A6F", "verification_ |
| 36 | `GET` | `/api/v1/auth/health` | ✅ 200 | 14ms | {"status": "healthy", "service": "authentication", "version": "1.0.0"} |
| 37 | `GET` | `/api/v1/auth/me` | ✅ 200 | 15ms | {"id": "a0000000-0000-0000-0000-000000000001", "email": "taidt@mtsolution.com.vn", "name": "Platform |
| 38 | `GET` | `/api/v1/auth/oauth/github/authorize` | ✅ 200 | 10ms | {"authorization_url": "https://github.com/login/oauth/authorize?client_id=Ov23li0mfFERLtQgdEeI&redir |
| 39 | `GET` | `/api/v1/auth/oauth/google/authorize` | ✅ 200 | 10ms | {"authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=315273414049-e9q0o0nb0 |
| 40 | `GET` | `/api/v1/auth/verify-reset-token` | ✅ 200 | 16ms | {"valid": false, "email": null, "expires_at": null, "error": "Invalid or expired token"} |
| 41 | `GET` | `/api/v1/auto-generate/health` | ✅ 200 | 15ms | {"service": "AutoGenerationService", "healthy": true, "ollama_available": false, "ollama_models": [] |
| 42 | `GET` | `/api/v1/ceo-dashboard/health` | ✅ 200 | 11ms | {"status": "healthy", "service": "ceo_dashboard", "timestamp": "2026-03-08T05:05:20.741105", "metric |
| 43 | `GET` | `/api/v1/ceo-dashboard/overrides` | ✅ 200 | 10ms | [] |
| 44 | `GET` | `/api/v1/ceo-dashboard/pending-decisions` | ✅ 200 | 17ms | [] |
| 45 | `GET` | `/api/v1/ceo-dashboard/routing-breakdown` | ✅ 200 | 11ms | {"total_prs": 0, "auto_approved": 0, "tech_lead_review": 0, "ceo_should_review": 0, "ceo_must_review |
| 46 | `GET` | `/api/v1/ceo-dashboard/summary` | ✅ 200 | 15ms | {"executive_summary": {"time_saved": {"baseline_hours": 40.0, "actual_review_hours": 0.0, "time_save |
| 47 | `GET` | `/api/v1/ceo-dashboard/system-health` | ✅ 200 | 12ms | {"uptime_percent": 99.9, "api_latency_p95_ms": 85.0, "kill_switch_status": "WARNING", "overall_statu |
| 48 | `GET` | `/api/v1/ceo-dashboard/time-saved` | ✅ 200 | 13ms | {"baseline_hours": 40.0, "actual_review_hours": 0.0, "time_saved_hours": 40.0, "time_saved_percent": |
| 49 | `GET` | `/api/v1/ceo-dashboard/top-rejections` | ✅ 200 | 13ms | [] |
| 50 | `GET` | `/api/v1/ceo-dashboard/trends/time-saved` | ✅ 200 | 10ms | [{"week": 3, "week_start": "2026-01-17", "time_saved_hours": 0, "baseline_hours": 40.0, "target_hour |
| 51 | `GET` | `/api/v1/ceo-dashboard/trends/vibecoding-index` | ✅ 200 | 10ms | [{"date": "2026-03-02", "day_name": "Monday", "average_index": 0, "count": 0, "distribution": {"0-10 |
| 52 | `GET` | `/api/v1/ceo-dashboard/weekly-summary` | ✅ 200 | 12ms | {"week_number": 10, "week_start": "2026-03-02T00:00:00", "week_end": "2026-03-09T00:00:00", "complia |
| 53 | `GET` | `/api/v1/check-runs` | ✅ 200 | 16ms | {"items": [], "total": 0, "page": 1, "page_size": 20, "has_more": false} |
| 54 | `GET` | `/api/v1/check-runs/health/status` | ✅ 200 | 16ms | {"status": "healthy", "service": "check-runs-api", "version": "1.0.0", "feature_status": "in_develop |
| 55 | `GET` | `/api/v1/check-runs/stats` | ✅ 200 | 24ms | {"total_runs": 0, "passed_runs": 0, "failed_runs": 0, "bypassed_runs": 0, "advisory_runs": 0, "block |
| 56 | `GET` | `/api/v1/codegen/health` | ✅ 200 | 24ms | {"healthy": true, "providers": {"app-builder": true, "ollama": true, "claude": false, "deepcode": fa |
| 57 | `GET` | `/api/v1/codegen/onboarding/options/domains` | ✅ 200 | 18ms | [{"key": "restaurant", "name": "Nha hang / Quan an", "name_en": "Restaurant / F&B", "description": " |
| 58 | `GET` | `/api/v1/codegen/onboarding/options/features/ecommerce` | ✅ 200 | 15ms | [{"key": "products", "name": "Quan ly san pham", "description": "Danh muc, gia ban, hinh anh"}, {"ke |
| 59 | `GET` | `/api/v1/codegen/onboarding/options/scales` | ✅ 200 | 16ms | [{"key": "micro", "label": "Ca nhan / 1-5 nhan vien", "employee_min": 1, "employee_max": 5, "cgf_tie |
| 60 | `POST` | `/api/v1/codegen/onboarding/start` | ✅ 200 | 15ms | {"session_id": "d1555ffe-99ab-452f-84bd-f9d5ad954b81", "current_step": "welcome", "completed_steps": |
| 61 | `GET` | `/api/v1/codegen/providers` | ✅ 200 | 18ms | {"providers": [{"name": "ollama", "available": true, "fallback_position": 0, "primary": true}, {"nam |
| 62 | `GET` | `/api/v1/codegen/sessions` | ✅ 200 | 15ms | {"sessions": [], "total": 0, "page": 1, "page_size": 20} |
| 63 | `GET` | `/api/v1/codegen/sessions/09e33f72-f57e-45db-8bd2-d9791098444d/quality/stream` | ✅ 200 | 14ms | "data: {\"type\": \"error\", \"session_id\": \"09e33f72-f57e-45db-8bd2-d9791098444d\", \"message\":  |
| 64 | `GET` | `/api/v1/codegen/templates` | ✅ 200 | 21ms | [{"id": "fastapi", "name": "FastAPI Service", "description": "Full CRUD service with authentication" |
| 65 | `GET` | `/api/v1/compliance/ai/budget` | ✅ 200 | 21ms | {"month": "2026-03", "total_spent": 0.0, "budget": 500.0, "remaining": 500.0, "percentage_used": 0.0 |
| 66 | `GET` | `/api/v1/compliance/ai/models` | ✅ 200 | 13ms | {"models": [], "default_model": "qwen3:32b", "ollama_url": "http://localhost:11434"} |
| 67 | `GET` | `/api/v1/compliance/ai/providers` | ✅ 200 | 17ms | {"ollama": {"healthy": false, "models": [], "version": "unknown", "error": "Connection refused - Oll |
| 68 | `GET` | `/api/v1/compliance/queue/status` | ✅ 200 | 19ms | {"pending": 0, "running": 0, "completed": 0, "failed": 0, "total_jobs": 0} |
| 69 | `GET` | `/api/v1/compliance/scans/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | ✅ 200 | 16ms | [{"id": "fda86bce-a730-42ad-a713-ba3ffd718cb6", "compliance_score": 100, "violations_count": 0, "war |
| 70 | `GET` | `/api/v1/compliance/scans/3ec1d475-c294-40e9-806f-0691dffa3fa8/latest` | ✅ 200 | 17ms | {"id": "fda86bce-a730-42ad-a713-ba3ffd718cb6", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |
| 71 | `GET` | `/api/v1/compliance/violations/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 15ms | [] |
| 72 | `GET` | `/api/v1/context-authority/v2/health` | ✅ 200 | 20ms | {"status": "unhealthy", "version": "2.0.0", "template_count": 0, "snapshot_count_24h": 0, "avg_valid |
| 73 | `GET` | `/api/v1/context-validation/health` | ✅ 200 | 9ms | {"status": "healthy", "service": "context-validation", "version": "1.0.0", "max_lines_per_file": 60} |
| 74 | `GET` | `/api/v1/cross-reference/coverage/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 21ms | {"total": 0, "covered": 0, "uncovered": 0, "percentage": 0.0} |
| 75 | `GET` | `/api/v1/cross-reference/missing-tests/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 25ms | [] |
| 76 | `GET` | `/api/v1/cross-reference/ssot-check/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 19ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "ssot_compliant": true, "violations": [], "me |
| 77 | `GET` | `/api/v1/dashboard/recent-gates` | ✅ 200 | 13ms | [{"id": "b1913ff7-15cb-4ad3-9846-4200ce4f70af", "gate_name": "Final Retest - Planning Review", "proj |
| 78 | `GET` | `/api/v1/dashboard/stats` | ✅ 200 | 17ms | {"total_projects": 7, "active_gates": 2, "pending_approvals": 2, "pass_rate": 0} |
| 79 | `GET` | `/api/v1/data-residency/regions` | ✅ 200 | 18ms | {"regions": [{"region": "VN", "display_name": "Vietnam / Singapore (Asia Pacific)", "endpoint_url":  |
| 80 | `GET` | `/api/v1/docs/user-support` | ✅ 200 | 9ms | ["01-Getting-Started.md", "02-SDLC-Framework-Overview.md", "03-Platform-Features.md", "04-User-Roles |
| 81 | `GET` | `/api/v1/enterprise/audit` | ✅ 200 | 18ms | {"events": [], "total": 0, "page": 1, "page_size": 50, "has_more": false} |
| 82 | `GET` | `/api/v1/evidence` | ✅ 200 | 20ms | {"items": [{"id": "036b2a6d-5959-4327-a77c-54ca4407847e", "gate_id": "1074f1fa-8f9e-4504-8656-0367b0 |
| 83 | `GET` | `/api/v1/evidence-manifests` | ✅ 200 | 17ms | {"total": 1, "manifests": [{"id": "b807b471-b8b5-430c-b240-7a1fdeeff3cf", "project_id": "3ec1d475-c2 |
| 84 | `GET` | `/api/v1/evidence-manifests/b807b471-b8b5-430c-b240-7a1fdeeff3cf` | ✅ 200 | 22ms | {"id": "b807b471-b8b5-430c-b240-7a1fdeeff3cf", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |
| 85 | `GET` | `/api/v1/evidence/` | ✅ 200 | 61ms | {"items": [{"id": "036b2a6d-5959-4327-a77c-54ca4407847e", "gate_id": "1074f1fa-8f9e-4504-8656-0367b0 |
| 86 | `POST` | `/api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e/validate-content` | ✅ 200 | 43ms | {"score": 1.0, "passed": true, "document_type": "DOCUMENTATION", "missing_sections": [], "found_sect |
| 87 | `GET` | `/api/v1/gates` | ✅ 200 | 15ms | {"items": [{"id": "b186b6cb-0320-4077-80e2-775c59f79bd8", "project_id": "3ec1d475-c294-40e9-806f-069 |
| 88 | `GET` | `/api/v1/gates-engine/health` | ✅ 200 | 20ms | {"status": "healthy", "service": "gates_engine", "opa_available": true, "valid_gate_codes": ["G0.1", |
| 89 | `GET` | `/api/v1/gates-engine/readiness/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 31ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "total_gates": 5, "approved_count": 0, "curre |
| 90 | `GET` | `/api/v1/gates-engine/stages` | ✅ 200 | 16ms | {"G0.1": "WHY", "G0.2": "WHY", "G1": "WHAT", "G2": "HOW", "G3": "BUILD", "G4": "TEST", "G5": "DEPLOY |
| 91 | `GET` | `/api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8` | ✅ 200 | 15ms | {"id": "b186b6cb-0320-4077-80e2-775c59f79bd8", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |
| 92 | `GET` | `/api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/approvals` | ✅ 200 | 16ms | [] |
| 93 | `POST` | `/api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/evaluate` | ✅ 200 | 40ms | {"gate_id": "b186b6cb-0320-4077-80e2-775c59f79bd8", "status": "EVALUATED", "evaluated_at": "2026-03- |
| 94 | `GET` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af` | ✅ 200 | 33ms | {"id": "b1913ff7-15cb-4ad3-9846-4200ce4f70af", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |
| 95 | `GET` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/actions` | ✅ 200 | 24ms | {"gate_id": "b1913ff7-15cb-4ad3-9846-4200ce4f70af", "status": "EVALUATED", "actions": {"can_evaluate |
| 96 | `GET` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/approvals` | ✅ 200 | 19ms | [] |
| 97 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/evaluate` | ✅ 200 | 33ms | {"gate_id": "b1913ff7-15cb-4ad3-9846-4200ce4f70af", "status": "EVALUATED", "evaluated_at": "2026-03- |
| 98 | `GET` | `/api/v1/gdpr/dsar` | ✅ 200 | 17ms | {"items": [{"id": "fd92da75-1708-4faf-9004-343af644fbb5", "request_type": "access", "status": "pendi |
| 99 | `GET` | `/api/v1/gdpr/me/consents` | ✅ 200 | 14ms | {"consents": [{"id": "feb3d147-61a2-4607-8f75-b03d62986ef0", "purpose": "essential", "granted": true |
| 100 | `GET` | `/api/v1/gdpr/me/data-export` | ✅ 200 | 13ms | {"user_id": "a0000000-0000-0000-0000-000000000001", "generated_at": "2026-03-08T05:05:22.304787+00:0 |
| 101 | `GET` | `/api/v1/governance-metrics` | ✅ 200 | 10ms | # HELP governance_submissions_total Total number of governance submissions # TYPE governance_submiss |
| 102 | `GET` | `/api/v1/governance-metrics/definitions` | ✅ 200 | 12ms | {"total": 47, "categories": {"governance_system": 15, "performance": 10, "business_ceo_dashboard": 8 |
| 103 | `GET` | `/api/v1/governance-metrics/health` | ✅ 200 | 10ms | {"status": "healthy", "service": "prometheus_metrics_collector", "timestamp": "2026-03-08T05:05:20.8 |
| 104 | `GET` | `/api/v1/governance-metrics/json` | ✅ 200 | 10ms | {"counters": {}, "gauges": {}, "histograms": {}, "timestamp": "2026-03-08T05:05:20.898895", "total_m |
| 105 | `GET` | `/api/v1/governance/dogfooding/status` | ✅ 200 | 11ms | {"phase": "week_1_preparation", "mode": "warning", "start_date": "2026-03-07T04:33:00.508460", "curr |
| 106 | `GET` | `/api/v1/governance/health` | ✅ 200 | 14ms | {"status": "healthy", "mode": "warning", "auto_rollback_enabled": true, "total_evaluations": 0, "lat |
| 107 | `GET` | `/api/v1/governance/metrics` | ✅ 200 | 13ms | {"mode": "warning", "total_evaluations": 0, "total_blocked": 0, "total_warned": 0, "total_passed": 0 |
| 108 | `GET` | `/api/v1/governance/mode` | ✅ 200 | 13ms | {"mode": "warning", "previous_mode": null, "changed_at": "2026-03-07T04:33:00.508460", "changed_by": |
| 109 | `GET` | `/api/v1/governance/mode/state` | ✅ 200 | 13ms | {"mode": "warning", "previous_mode": null, "changed_at": "2026-03-07T04:33:00.508460", "changed_by": |
| 110 | `GET` | `/api/v1/grafana-dashboards` | ✅ 200 | 19ms | {"dashboards": [{"uid": "ceo-dashboard", "title": "CEO Dashboard - Governance Intelligence", "descri |
| 111 | `GET` | `/api/v1/grafana-dashboards/datasource/template` | ✅ 200 | 13ms | {"name": "Prometheus-SDLC", "type": "prometheus", "access": "proxy", "url": "http://prometheus:9090" |
| 112 | `GET` | `/api/v1/grafana-dashboards/export/all` | ✅ 200 | 14ms | [{"uid": "ceo-dashboard", "title": "CEO Dashboard - Governance Intelligence", "description": "Execut |
| 113 | `GET` | `/api/v1/maturity/health` | ✅ 200 | 13ms | {"status": "healthy", "service": "agentic-maturity", "version": "1.0.0", "levels": ["L0", "L1", "L2" |
| 114 | `GET` | `/api/v1/maturity/levels` | ✅ 200 | 12ms | [{"level": "L0", "name": "Manual", "description": "Human writes all code, manual testing and reviews |
| 115 | `GET` | `/api/v1/mrp/health` | ✅ 200 | 13ms | {"status": "healthy", "service": "mrp-validation", "version": "1.0.0", "features": ["5-point-mrp-val |
| 116 | `GET` | `/api/v1/mrp/policies/compliance/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 19ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "current_tier": "PROFESSIONAL", "is_compliant |
| 117 | `GET` | `/api/v1/mrp/policies/tiers` | ✅ 200 | 19ms | {"tiers": [{"tier": "LITE", "display_name": "Lite", "description": "Advisory mode for individuals an |
| 118 | `GET` | `/api/v1/mrp/vcr/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | ✅ 200 | 24ms | {"id": "1eeb9e41-da40-4b28-9313-bbac7449bad8", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |
| 119 | `GET` | `/api/v1/notifications` | ✅ 200 | 23ms | {"notifications": [], "total": 0, "unread_count": 0, "page": 1, "page_size": 20} |
| 120 | `GET` | `/api/v1/notifications/settings/preferences` | ✅ 200 | 16ms | {"email_enabled": true, "slack_enabled": false, "slack_webhook_url": null, "teams_enabled": false, " |
| 121 | `GET` | `/api/v1/notifications/stats/summary` | ✅ 200 | 17ms | {"total": 0, "unread": 0, "read": 0, "by_type": {}, "unread_by_priority": {}} |
| 122 | `GET` | `/api/v1/planning/backlog` | ✅ 200 | 17ms | {"items": [{"id": "135b6b04-5530-45d0-a3b2-a9fe5bc138f5", "project_id": "3ec1d475-c294-40e9-806f-069 |
| 123 | `GET` | `/api/v1/planning/backlog/135b6b04-5530-45d0-a3b2-a9fe5bc138f5` | ✅ 200 | 16ms | {"id": "135b6b04-5530-45d0-a3b2-a9fe5bc138f5", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |
| 124 | `PUT` | `/api/v1/planning/backlog/135b6b04-5530-45d0-a3b2-a9fe5bc138f5` | ✅ 200 | 18ms | {"id": "135b6b04-5530-45d0-a3b2-a9fe5bc138f5", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |
| 125 | `GET` | `/api/v1/planning/backlog/assignees/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 15ms | [] |
| 126 | `GET` | `/api/v1/planning/dashboard/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 23ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "roadmaps": [{"id": "624cc6c6-115f-4609-8b1d- |
| 127 | `GET` | `/api/v1/planning/phases/55bec71c-8228-4b39-8a78-a34de8b3dc8d` | ✅ 200 | 16ms | {"id": "55bec71c-8228-4b39-8a78-a34de8b3dc8d", "roadmap_id": "624cc6c6-115f-4609-8b1d-dd1912fd527b", |
| 128 | `PUT` | `/api/v1/planning/phases/55bec71c-8228-4b39-8a78-a34de8b3dc8d` | ✅ 200 | 21ms | {"id": "55bec71c-8228-4b39-8a78-a34de8b3dc8d", "roadmap_id": "624cc6c6-115f-4609-8b1d-dd1912fd527b", |
| 129 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/dependency-analysis` | ✅ 200 | 18ms | {"total_dependencies": 0, "blocking_dependencies": 0, "cross_project_dependencies": 0, "pending_depe |
| 130 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/dependency-graph` | ✅ 200 | 19ms | {"nodes": [], "edges": [], "total_sprints": 0, "total_dependencies": 0, "blocking_dependencies": 0,  |
| 131 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/resource-heatmap` | ✅ 200 | 23ms | {"users": [{"id": "2e542eba-b1b5-4f91-ab82-b853a6887b8d", "name": "*-CyEyes-* S4 Admin", "email": "c |
| 132 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/template-suggestions` | ✅ 200 | 21ms | {"suggestions": [{"template_id": "df4beaf4-54e8-48fd-98d0-98c03daae6e4", "template_name": "Feature S |
| 133 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/velocity` | ✅ 200 | 18ms | {"average": 0.0, "trend": "unknown", "confidence": 0.0, "history": [], "sprint_count": 0, "project_i |
| 134 | `GET` | `/api/v1/planning/roadmaps` | ✅ 200 | 14ms | {"items": [{"id": "624cc6c6-115f-4609-8b1d-dd1912fd527b", "project_id": "3ec1d475-c294-40e9-806f-069 |
| 135 | `GET` | `/api/v1/planning/roadmaps/624cc6c6-115f-4609-8b1d-dd1912fd527b` | ✅ 200 | 18ms | {"id": "624cc6c6-115f-4609-8b1d-dd1912fd527b", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |
| 136 | `PUT` | `/api/v1/planning/roadmaps/624cc6c6-115f-4609-8b1d-dd1912fd527b` | ✅ 200 | 20ms | {"id": "624cc6c6-115f-4609-8b1d-dd1912fd527b", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |
| 137 | `GET` | `/api/v1/planning/sprints` | ✅ 200 | 16ms | {"items": [{"id": "901b185c-a99d-44f9-af4a-91ac8891e449", "project_id": "3ec1d475-c294-40e9-806f-069 |
| 138 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449` | ✅ 200 | 16ms | {"id": "901b185c-a99d-44f9-af4a-91ac8891e449", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |
| 139 | `PUT` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449` | ✅ 200 | 22ms | {"id": "901b185c-a99d-44f9-af4a-91ac8891e449", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |
| 140 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/action-items` | ✅ 200 | 15ms | {"items": [], "total": 0, "page": 1, "page_size": 20} |
| 141 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/action-items/stats` | ✅ 200 | 13ms | {"total_items": 0, "open_items": 0, "in_progress_items": 0, "completed_items": 0, "cancelled_items": |
| 142 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/allocations` | ✅ 200 | 14ms | {"items": [{"allocation_percentage": 100, "role": "developer", "notes": null, "id": "0cb006df-d414-4 |
| 143 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/analytics` | ✅ 200 | 29ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "sprint_number": 1, "sprint_name": "*-CyEyes-* |
| 144 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/burndown` | ✅ 200 | 27ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "sprint_number": 1, "sprint_name": "*-CyEyes-* |
| 145 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/capacity` | ✅ 200 | 25ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "sprint_number": 1, "sprint_name": "*-CyEyes-* |
| 146 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/dependencies` | ✅ 200 | 17ms | {"items": [], "total": 0, "page": 1, "page_size": 20} |
| 147 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/forecast` | ✅ 200 | 16ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "sprint_number": 1, "sprint_name": "*-CyEyes-* |
| 148 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/gates` | ✅ 200 | 14ms | [] |
| 149 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/health` | ✅ 200 | 21ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "completion_rate": 0.0, "completed_points": 0, |
| 150 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/retrospective` | ✅ 200 | 22ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "sprint_number": 1, "sprint_name": "*-CyEyes-* |
| 151 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/suggestions` | ✅ 200 | 18ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "suggestions": [{"type": "unassigned_priority" |
| 152 | `GET` | `/api/v1/planning/subagent/health` | ✅ 200 | 17ms | {"status": "healthy", "service": "planning-subagent", "version": "2.0.0", "features": ["risk-based-p |
| 153 | `GET` | `/api/v1/planning/templates` | ✅ 200 | 28ms | {"items": [{"name": "Release Sprint", "description": "Sprint focused on preparing and executing a re |
| 154 | `GET` | `/api/v1/policies` | ✅ 200 | 16ms | {"items": [], "total": 0, "page": 1, "page_size": 20, "pages": 0} |
| 155 | `GET` | `/api/v1/policies/evaluations/b1913ff7-15cb-4ad3-9846-4200ce4f70af` | ✅ 200 | 22ms | {"items": [], "total": 0, "passed": 0, "failed": 0, "pass_rate": 0.0} |
| 156 | `GET` | `/api/v1/projects` | ✅ 200 | 17ms | [{"id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "name": "CyEyes-S4", "description": "*-CyEyes-* sess |
| 157 | `GET` | `/api/v1/projects/` | ✅ 200 | 50ms | [{"id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "name": "CyEyes-Updated", "description": "*-CyEyes-* |
| 158 | `POST` | `/api/v1/projects/` | ✅ 200 | 53ms | [{"id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "name": "CyEyes-S4", "description": "*-CyEyes-* sess |
| 159 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 27ms | {"id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "name": "CyEyes-S4", "description": "*-CyEyes-* sessi |
| 160 | `PUT` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 50ms | {"id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "name": "CyEyes-S4", "slug": "final-retest", "descrip |
| 161 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance-summary` | ✅ 200 | 23ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "project_name": "CyEyes-S4", "tier": "profess |
| 162 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/context` | ✅ 200 | 26ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "stage": "06-DEPLOY", "gate": "Final Retest - |
| 163 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence/gaps` | ✅ 200 | 16ms | {"gaps": {"missing_evidence": [], "backend_gaps": [], "frontend_gaps": [], "extension_gaps": [], "cl |
| 164 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence/status` | ✅ 200 | 29ms | {"status": "complete", "gaps": {"backend": [], "frontend": [], "extension": [], "cli": []}, "total_g |
| 165 | `POST` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence/validate` | ✅ 200 | 15ms | {"validation_id": "val-1772877275.6906", "status": "complete", "violations": [], "summary": {"errors |
| 166 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/overrides` | ✅ 200 | 17ms | [] |
| 167 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/policy-pack` | ✅ 200 | 22ms | {"name": "Standard Policy Pack", "description": "Auto-configured Standard tier policy pack for Final |
| 168 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/timeline` | ✅ 200 | 39ms | {"events": [], "stats": {"total_events": 0, "ai_detected": 0, "pass_rate": 0.0, "override_rate": 0.0 |
| 169 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/timeline/stats` | ✅ 200 | 21ms | {"total_events": 0, "ai_detected": 0, "pass_rate": 0.0, "override_rate": 0.0, "by_tool": {}, "by_sta |
| 170 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/validation-history` | ✅ 200 | 26ms | [] |
| 171 | `GET` | `/api/v1/push/status` | ✅ 200 | 16ms | {"is_subscribed": false, "subscriptions_count": 0} |
| 172 | `GET` | `/api/v1/push/subscriptions` | ✅ 200 | 14ms | {"subscriptions": [], "total": 0} |
| 173 | `GET` | `/api/v1/push/vapid-key` | ✅ 200 | 13ms | {"public_key": "BNbxGGkqLJiJqhspMQU0JCzKHJtKqkq0TdVbJGiWFhB1GGJhkPGiWFhB1GGJhkPGiWFhB1GGJhkPGiWFhB1G |
| 174 | `GET` | `/api/v1/risk/factors` | ✅ 200 | 16ms | [{"factor": "data_schema", "name": "Data Schema Changes", "description": "Migrations, model changes, |
| 175 | `GET` | `/api/v1/risk/levels` | ✅ 200 | 13ms | {"levels": [{"level": "minimal", "score_range": "0-20", "planning_required": false, "description": " |
| 176 | `GET` | `/api/v1/sast/health` | ✅ 200 | 12ms | {"status": "degraded", "semgrep_available": false, "custom_rules": {"ai_security": false, "owasp_pyt |
| 177 | `POST` | `/api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/scan` | ✅ 200 | 19ms | {"scan_id": "9762c907-074e-4523-9945-eef1fadad2eb", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3 |
| 178 | `POST` | `/api/v1/sast/scan-snippet` | ✅ 200 | 13ms | {"scan_id": "2f72718b-6866-4a28-b58d-90845bef4b73", "project_id": "66dddcdf-2209-4c3e-8a70-4d666207b |
| 179 | `GET` | `/api/v1/stage-gating/health` | ✅ 200 | 18ms | {"status": "healthy", "service": "stage_gating", "stages_configured": 11, "timestamp": "2026-03-08T0 |
| 180 | `GET` | `/api/v1/stage-gating/progress/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 23ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "current_stage": "stage_04_build", "completed |
| 181 | `GET` | `/api/v1/stage-gating/rules` | ✅ 200 | 20ms | {"stages": {"stage_00_foundation": {"stage": "stage_00_foundation", "allows": ["docs/00-foundation/* |
| 182 | `GET` | `/api/v1/telemetry/health` | ✅ 200 | 13ms | {"status": "healthy", "service": "telemetry", "version": "1.0.0", "funnels_available": ["time_to_fir |
| 183 | `GET` | `/api/v1/templates/sdlc-structure` | ✅ 200 | 10ms | {"version": "5.0.0", "tier": "STANDARD", "tier_description": "Standard documentation for most projec |
| 184 | `GET` | `/api/v1/templates/stages` | ✅ 200 | 10ms | {"version": "5.0.0", "stages": {"00": {"id": "00", "name": "foundation", "full_name": "Foundation (W |
| 185 | `GET` | `/api/v1/templates/tiers` | ✅ 200 | 16ms | {"version": "5.0.0", "tiers": {"LITE": {"team_size_range": "1-2", "required_stages": ["00", "01", "0 |
| 186 | `GET` | `/api/v1/triage/stats` | ✅ 200 | 26ms | {"by_status": {}, "by_priority": {}, "untriaged_count": 0, "total": 0, "triage_rate": 0.0} |
| 187 | `GET` | `/api/v1/vibecoding/health` | ✅ 200 | 18ms | {"status": "healthy", "service": "vibecoding_index_engine", "signals_configured": 5, "critical_path_ |
| 188 | `GET` | `/api/v1/vibecoding/stats` | ✅ 200 | 11ms | {"total_calculations": 0, "average_score": 0.0, "category_distribution": {"green": 0, "yellow": 0, " |
| 189 | `GET` | `/api/v1/vibecoding/thresholds` | ✅ 200 | 12ms | {"thresholds": {"green": {"min": 0, "max": 30}, "yellow": {"min": 31, "max": 60}, "orange": {"min":  |
| 190 | `GET` | `/health` | ✅ 200 | 15ms | {"status": "healthy", "version": "1.2.0", "service": "sdlc-orchestrator-backend"} |

## Per-Module Endpoint Tables

### Admin

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/admin/ai-providers` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/admin/ai-providers/config` | ✅ 200 | 22ms | {"ollama": {"available": true, "configured": true, "url": "http://ollama:11434", "model": "qwen3:14b |  |
| 3 | `GET` | `/api/v1/admin/ai-providers/ollama/models` | ✅ 200 | 36ms | {"models": ["bge-m3:latest", "deepseek-ocr:3b", "gemma3:12b", "ministral-3:8b-instruct-2512-q4_K_M", |  |
| 4 | `POST` | `/api/v1/admin/ai-providers/ollama/refresh-models` | ✅ 200 | 29ms | {"models": ["bge-m3:latest", "deepseek-ocr:3b", "gemma3:12b", "ministral-3:8b-instruct-2512-q4_K_M", |  |
| 5 | `GET` | `/api/v1/admin/ai-providers/ollama/refresh-models` | ❌ 405 | 17ms | {"detail": "Method Not Allowed"} |  |
| 6 | `GET` | `/api/v1/admin/audit-logs` | ✅ 200 | 36ms | {"items": [{"id": "0e55df7e-a247-4dfa-9a3e-9023cdf0ac7a", "timestamp": "2026-03-08T11:56:44.275771", |  |
| 7 | `POST` | `/api/v1/admin/broadcast` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 8 | `POST` | `/api/v1/admin/cache/clear` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 9 | `GET` | `/api/v1/admin/evidence/retention-stats` | ✅ 200 | 18ms | {"total_evidence": 2, "active_evidence": 2, "archived_evidence": 0, "evidence_due_for_archive": 0, " |  |
| 10 | `GET` | `/api/v1/admin/metrics` | 🔴 404 | 19ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 11 | `GET` | `/api/v1/admin/ott-channels` | 🔴 404 | 9ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 12 | `GET` | `/api/v1/admin/ott-channels/config` | ✅ 200 | 14ms | {"channels": [{"channel": "slack", "status": "offline", "tier": "PROFESSIONAL", "webhook_url": "http |  |
| 13 | `GET` | `/api/v1/admin/ott-channels/health` | 🔴 404 | 38ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 14 | `GET` | `/api/v1/admin/ott-channels/stats` | 💥 500 | 13ms | Internal Server Error | DB migration missing / Service error |
| 15 | `GET` | `/api/v1/admin/ott-channels/telegram/conversations` | 💥 500 | 19ms | "Internal Server Error" | DB migration missing / Service error |
| 16 | `GET` | `/api/v1/admin/ott-channels/telegram/health` | 💥 500 | 16ms | Internal Server Error | DB migration missing / Service error |
| 17 | `POST` | `/api/v1/admin/ott-channels/telegram/send` | 🔴 404 | 16ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 18 | `GET` | `/api/v1/admin/override-queue` | ✅ 200 | 22ms | {"pending": [], "recent_decisions": [], "total_pending": 0} |  |
| 19 | `GET` | `/api/v1/admin/override-stats` | ✅ 200 | 17ms | {"total": 0, "by_status": {}, "by_type": {}, "approval_rate": 0.0, "pending": 0, "days": 30} |  |
| 20 | `GET` | `/api/v1/admin/settings` | ✅ 200 | 13ms | {"security": [{"key": "max_login_attempts", "value": 5, "version": 2, "category": "security", "descr |  |
| 21 | `POST` | `/api/v1/admin/settings` | ❌ 405 | 11ms | {"detail": "Method Not Allowed"} |  |
| 22 | `GET` | `/api/v1/admin/settings/maintenance_mode` | 🔴 404 | 21ms | {"detail": "Setting 'maintenance_mode' not found"} | Route not registered / path incorrect |
| 23 | `GET` | `/api/v1/admin/settings/max_login_attempts` | ✅ 200 | 14ms | {"key": "max_login_attempts", "value": 5, "version": 1, "category": "security", "description": "Maxi |  |
| 24 | `PATCH` | `/api/v1/admin/settings/max_login_attempts` | ✅ 200 | 23ms | {"key": "max_login_attempts", "value": 5, "version": 2, "category": "security", "description": "Maxi |  |
| 25 | `GET` | `/api/v1/admin/stats` | ✅ 200 | 14ms | {"total_users": 13, "active_users": 13, "inactive_users": 0, "superusers": 2, "total_projects": 7, " |  |
| 26 | `GET` | `/api/v1/admin/system/health` | ✅ 200 | 16ms | {"overall_status": "healthy", "services": [{"name": "PostgreSQL", "status": "healthy", "response_tim |  |
| 27 | `GET` | `/api/v1/admin/usage` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 28 | `GET` | `/api/v1/admin/users` | ✅ 200 | 24ms | {"items": [{"id": "818d8908-481d-471b-8688-9a1b96878c4b", "email": "cyeyes-s4-1772877264@test.com",  |  |
| 29 | `GET` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d` | ✅ 200 | 17ms | {"id": "2e542eba-b1b5-4f91-ab82-b853a6887b8d", "email": "cyeyes-reg3@test.com", "full_name": null, " |  |
| 30 | `PATCH` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d` | ✅ 200 | 41ms | {"id": "2e542eba-b1b5-4f91-ab82-b853a6887b8d", "email": "cyeyes-reg3@test.com", "full_name": null, " |  |
| 31 | `POST` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/activate` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 32 | `GET` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/mfa-status` | ✅ 200 | 17ms | {"user_id": "2e542eba-b1b5-4f91-ab82-b853a6887b8d", "email": "cyeyes-reg3@test.com", "mfa_enabled":  |  |
| 33 | `PUT` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/role` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 34 | `POST` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/suspend` | 🔴 404 | 27ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 35 | `POST` | `/api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/unlock` | ❌ 400 | 15ms | {"detail": "User account is not locked. Email: cyeyes-reg3@test.com"} |  |
| 36 | `GET` | `/api/v1/admin/users/a0000000-0000-0000-0000-000000000001` | ✅ 200 | 21ms | {"id": "a0000000-0000-0000-0000-000000000001", "email": "taidt@mtsolution.com.vn", "full_name": null |  |
| 37 | `DELETE` | `/api/v1/admin/users/cyeyes-reg3@test.com` | ❌ 422 | 15ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "user_id"], "msg": "Input should be a valid UUI | Missing required parameter |

### Agent Team

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/agent-team/conversations` | 💥 500 | 18ms | Internal Server Error | DB migration missing / Service error |
| 2 | `POST` | `/api/v1/agent-team/conversations` | ❌ 422 | 0ms | {"detail": [{"type": "missing", "loc": ["body", "agent_definition_id"], "msg": "Field required", "in | Missing required parameter |
| 3 | `GET` | `/api/v1/agent-team/definitions` | 💥 500 | 16ms | Internal Server Error | DB migration missing / Service error |
| 4 | `POST` | `/api/v1/agent-team/definitions/seed` | ❌ 422 | 16ms | {"detail": [{"type": "missing", "loc": ["query", "project_id"], "msg": "Field required", "input": nu | Missing required parameter |
| 5 | `GET` | `/api/v1/agent-team/presets` | ✅ 200 | 22ms | [{"name": "solo-dev", "description": "Single developer working alone", "roles": ["coder"], "delegati |  |
| 6 | `POST` | `/api/v1/agent-team/presets/solo-dev/apply` | ❌ 422 | 17ms | {"detail": [{"type": "missing", "loc": ["query", "project_id"], "msg": "Field required", "input": nu | Missing required parameter |

### Agentic Maturity

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/agentic-maturity` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/agentic-maturity/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Agents

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/agents/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 21ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/agents/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | 🔴 404 | 18ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Agents Md

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/agents-md` | 🔴 404 | 19ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 35ms | {"id": "492cddc7-d13c-46f0-b9b0-b9bf15c3e951", "content": "# AGENTS.md - CyEyes-S4\n\n## Quick Start |  |
| 3 | `PUT` | `/api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ❌ 405 | 25ms | {"detail": "Method Not Allowed"} |  |
| 4 | `POST` | `/api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8/generate` | 🔴 404 | 27ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | ✅ 200 | 20ms | [{"id": "492cddc7-d13c-46f0-b9b0-b9bf15c3e951", "generated_at": "2026-03-07T09:54:40.834579+00:00",  |  |
| 6 | `GET` | `/api/v1/agents-md/context/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 35ms | {"id": "ab0a7a88-f96c-4a1a-aa41-3c48f18ea19b", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |
| 7 | `GET` | `/api/v1/agents-md/context/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | ✅ 200 | 22ms | [{"id": "ab0a7a88-f96c-4a1a-aa41-3c48f18ea19b", "generated_at": "2026-03-08T05:05:21.586040+00:00",  |  |
| 8 | `POST` | `/api/v1/agents-md/generate` | ⚠️ 201 | 26ms | {"id": "492cddc7-d13c-46f0-b9b0-b9bf15c3e951", "content": "# AGENTS.md - CyEyes-S4\n\n## Quick Start |  |
| 9 | `POST` | `/api/v1/agents-md/lint` | ✅ 200 | 14ms | {"original_content": "# Test", "fixed_content": "# Test\n", "changes": ["Added newline at end of fil |  |
| 10 | `GET` | `/api/v1/agents-md/repos` | 💥 500 | 18ms | Internal Server Error | DB migration missing / Service error |
| 11 | `POST` | `/api/v1/agents-md/validate` | ✅ 200 | 27ms | {"valid": true, "errors": [], "warnings": [{"severity": "warning", "message": "Missing recommended s |  |

### Ai Detection

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/ai-detection` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `POST` | `/api/v1/ai-detection/analyze` | ❌ 422 | 13ms | {"detail": [{"type": "missing", "loc": ["body", "pr_id"], "msg": "Field required", "input": {"conten | Missing required parameter |
| 3 | `GET` | `/api/v1/ai-detection/circuit-breakers` | ✅ 200 | 12ms | {"circuit_breakers": {"github_api": {"name": "github_api", "config": {"failure_threshold": 5, "recov |  |
| 4 | `POST` | `/api/v1/ai-detection/detect` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/ai-detection/shadow-mode` | ✅ 200 | 12ms | {"status": "enabled", "config": {"enabled": true, "sample_rate": 1.0, "log_level": "INFO", "collect_ |  |
| 6 | `GET` | `/api/v1/ai-detection/status` | ✅ 200 | 17ms | {"service": "GitHubAIDetectionService", "version": "1.0.0", "detection_threshold": 0.5, "strategies" |  |
| 7 | `GET` | `/api/v1/ai-detection/tools` | ✅ 200 | 17ms | {"tools": [{"id": "cursor", "name": "Cursor"}, {"id": "copilot", "name": "Copilot"}, {"id": "claude_ |  |

### Ai Providers

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/ai-providers` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/ai-providers/health` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Analytics

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `POST` | `/api/v1/analytics/v2/events` | ❌ 422 | 16ms | {"detail": [{"type": "missing", "loc": ["body", "user_id"], "msg": "Field required", "input": {"even | Missing required parameter |
| 2 | `POST` | `/api/v1/analytics/v2/events/batch` | ❌ 422 | 17ms | {"detail": [{"type": "missing", "loc": ["body", "events", 0, "user_id"], "msg": "Field required", "i | Missing required parameter |
| 3 | `GET` | `/api/v1/analytics/v2/metrics/ai-safety` | ✅ 200 | 14ms | {"period_days": 7, "total_validations": 0, "pass_rate": 0.0, "avg_duration_ms": 0.0, "top_tools": {} |  |
| 4 | `GET` | `/api/v1/analytics/v2/metrics/dau` | ✅ 200 | 18ms | {"start_date": "2026-02-06", "end_date": "2026-03-08", "daily_counts": {}, "total_unique_users": 0,  |  |
| 5 | `GET` | `/api/v1/analytics/v2/trends` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 6 | `GET` | `/api/v1/analytics/v2/usage` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Analytics V2

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/analytics-v2/dora` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/analytics-v2/evidence` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/analytics-v2/gates` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/analytics-v2/overview` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Api Keys

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/api-keys` | ✅ 200 | 13ms | [{"id": "ce5a6ad5-adcb-4b95-bcf5-1a419a3835b4", "name": "*-CyEyes-* Key 1772860135", "prefix": "sdlc |  |
| 2 | `POST` | `/api/v1/api-keys` | ⚠️ 201 | 17ms | {"id": "ce5a6ad5-adcb-4b95-bcf5-1a419a3835b4", "name": "*-CyEyes-* Key 1772860135", "api_key": "sdlc |  |
| 3 | `GET` | `/api/v1/api-keys/bab4226d-b556-43e0-b535-271b18fd4908` | ❌ 405 | 12ms | {"detail": "Method Not Allowed"} |  |
| 4 | `DELETE` | `/api/v1/api-keys/bab4226d-b556-43e0-b535-271b18fd4908` | ⚠️ 204 | 15ms | "" |  |
| 5 | `GET` | `/api/v1/api-keys/ce5a6ad5-adcb-4b95-bcf5-1a419a3835b4` | ❌ 405 | 13ms | {"detail": "Method Not Allowed"} |  |
| 6 | `GET` | `/api/v1/api-keys/scopes` | ❌ 405 | 11ms | {"detail": "Method Not Allowed"} |  |

### Audit Trail

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/audit-trail` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/audit-trail/logs` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/audit-trail/resource/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Auth

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `POST` | `/api/v1/auth/forgot-password` | ✅ 200 | 37ms | {"message": "If an account with this email exists, you will receive a password reset link.", "email" |  |
| 2 | `POST` | `/api/v1/auth/github/device` | ✅ 200 | 509ms | {"device_code": "5b46c60aa896d89ebf2bcea293cb2e1b6ec684b1", "user_code": "AF38-1A6F", "verification_ |  |
| 3 | `POST` | `/api/v1/auth/github/token` | ❌ 400 | 715ms | {"detail": "GitHub device token error: The device_code provided is not valid."} |  |
| 4 | `GET` | `/api/v1/auth/health` | ✅ 200 | 14ms | {"status": "healthy", "service": "authentication", "version": "1.0.0"} |  |
| 5 | `POST` | `/api/v1/auth/login` | 💥 500 | 167ms | "Internal Server Error" | DB migration missing / Service error |
| 6 | `POST` | `/api/v1/auth/logout` | ⚠️ 204 | 20ms | "" |  |
| 7 | `GET` | `/api/v1/auth/me` | ✅ 200 | 15ms | {"id": "a0000000-0000-0000-0000-000000000001", "email": "taidt@mtsolution.com.vn", "name": "Platform |  |
| 8 | `GET` | `/api/v1/auth/mfa/qr-code` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 9 | `POST` | `/api/v1/auth/mfa/setup` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 10 | `GET` | `/api/v1/auth/mfa/status` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 11 | `GET` | `/api/v1/auth/oauth/github/authorize` | ✅ 200 | 10ms | {"authorization_url": "https://github.com/login/oauth/authorize?client_id=Ov23li0mfFERLtQgdEeI&redir |  |
| 12 | `GET` | `/api/v1/auth/oauth/github/callback` | ❌ 405 | 13ms | {"detail": "Method Not Allowed"} |  |
| 13 | `GET` | `/api/v1/auth/oauth/google/authorize` | ✅ 200 | 10ms | {"authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=315273414049-e9q0o0nb0 |  |
| 14 | `GET` | `/api/v1/auth/oauth/google/callback` | ❌ 405 | 16ms | {"detail": "Method Not Allowed"} |  |
| 15 | `POST` | `/api/v1/auth/refresh` | ❌ 422 | 11ms | {"detail": [{"type": "missing", "loc": ["body", "refresh_token"], "msg": "Field required", "input":  | Missing required parameter |
| 16 | `POST` | `/api/v1/auth/register` | ⚠️ 201 | 0ms | {"id": "818d8908-481d-471b-8688-9a1b96878c4b", "email": "cyeyes-s4-1772877264@test.com", "full_name" |  |
| 17 | `POST` | `/api/v1/auth/reset-password` | ❌ 422 | 15ms | {"detail": [{"type": "string_too_short", "loc": ["body", "token"], "msg": "String should have at lea | Missing required parameter |
| 18 | `GET` | `/api/v1/auth/sessions` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 19 | `GET` | `/api/v1/auth/users` | 🔴 404 | 9ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 20 | `GET` | `/api/v1/auth/users/a0000000-0000-0000-0000-000000000001` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 21 | `GET` | `/api/v1/auth/verify-reset-token` | ✅ 200 | 16ms | {"valid": false, "email": null, "expires_at": null, "error": "Invalid or expired token"} |  |

### Auto Generate

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `POST` | `/api/v1/auto-generate/attestation` | ❌ 422 | 18ms | {"detail": [{"type": "missing", "loc": ["body", "pr_number"], "msg": "Field required", "input": {"pr | Missing required parameter |
| 2 | `POST` | `/api/v1/auto-generate/context` | ❌ 422 | 17ms | {"detail": [{"type": "missing", "loc": ["body", "pr_number"], "msg": "Field required", "input": {"pr | Missing required parameter |
| 3 | `GET` | `/api/v1/auto-generate/health` | ✅ 200 | 15ms | {"service": "AutoGenerationService", "healthy": true, "ollama_available": false, "ollama_models": [] |  |
| 4 | `POST` | `/api/v1/auto-generate/intent` | ❌ 422 | 18ms | {"detail": [{"type": "missing", "loc": ["body", "task_id"], "msg": "Field required", "input": {"proj | Missing required parameter |
| 5 | `POST` | `/api/v1/auto-generate/ownership` | ❌ 422 | 17ms | {"detail": [{"type": "missing", "loc": ["body", "file_path"], "msg": "Field required", "input": {"pr | Missing required parameter |

### Auto Generation

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/auto-generation` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `POST` | `/api/v1/auto-generation/generate` | 🔴 404 | 8ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/auto-generation/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/auto-generation/status` | 🔴 404 | 15ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/auto-generation/templates` | 🔴 404 | 21ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Ceo Dashboard

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/ceo-dashboard` | 🔴 404 | 21ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/ceo-dashboard/health` | ✅ 200 | 11ms | {"status": "healthy", "service": "ceo_dashboard", "timestamp": "2026-03-08T05:05:20.741105", "metric |  |
| 3 | `GET` | `/api/v1/ceo-dashboard/overrides` | ✅ 200 | 10ms | [] |  |
| 4 | `GET` | `/api/v1/ceo-dashboard/pending-decisions` | ✅ 200 | 17ms | [] |  |
| 5 | `GET` | `/api/v1/ceo-dashboard/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 6 | `GET` | `/api/v1/ceo-dashboard/routing-breakdown` | ✅ 200 | 11ms | {"total_prs": 0, "auto_approved": 0, "tech_lead_review": 0, "ceo_should_review": 0, "ceo_must_review |  |
| 7 | `GET` | `/api/v1/ceo-dashboard/summary` | ✅ 200 | 15ms | {"executive_summary": {"time_saved": {"baseline_hours": 40.0, "actual_review_hours": 0.0, "time_save |  |
| 8 | `GET` | `/api/v1/ceo-dashboard/system-health` | ✅ 200 | 12ms | {"uptime_percent": 99.9, "api_latency_p95_ms": 85.0, "kill_switch_status": "WARNING", "overall_statu |  |
| 9 | `GET` | `/api/v1/ceo-dashboard/time-saved` | ✅ 200 | 13ms | {"baseline_hours": 40.0, "actual_review_hours": 0.0, "time_saved_hours": 40.0, "time_saved_percent": |  |
| 10 | `GET` | `/api/v1/ceo-dashboard/top-rejections` | ✅ 200 | 13ms | [] |  |
| 11 | `GET` | `/api/v1/ceo-dashboard/trends/time-saved` | ✅ 200 | 10ms | [{"week": 3, "week_start": "2026-01-17", "time_saved_hours": 0, "baseline_hours": 40.0, "target_hour |  |
| 12 | `GET` | `/api/v1/ceo-dashboard/trends/vibecoding-index` | ✅ 200 | 10ms | [{"date": "2026-03-02", "day_name": "Monday", "average_index": 0, "count": 0, "distribution": {"0-10 |  |
| 13 | `GET` | `/api/v1/ceo-dashboard/weekly-summary` | ✅ 200 | 12ms | {"week_number": 10, "week_start": "2026-03-02T00:00:00", "week_end": "2026-03-09T00:00:00", "complia |  |

### Channels

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/channels` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Check Runs

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/check-runs` | ✅ 200 | 16ms | {"items": [], "total": 0, "page": 1, "page_size": 20, "has_more": false} |  |
| 2 | `GET` | `/api/v1/check-runs/health/status` | ✅ 200 | 16ms | {"status": "healthy", "service": "check-runs-api", "version": "1.0.0", "feature_status": "in_develop |  |
| 3 | `GET` | `/api/v1/check-runs/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/check-runs/stats` | ✅ 200 | 24ms | {"total_runs": 0, "passed_runs": 0, "failed_runs": 0, "bypassed_runs": 0, "advisory_runs": 0, "block |  |

### Codegen

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `POST` | `/api/v1/codegen/estimate` | 💥 500 | 61ms | "Internal Server Error" | DB migration missing / Service error |
| 2 | `POST` | `/api/v1/codegen/generate` | ❌ 0 | 20005ms | "HTTPSConnectionPool(host='sdlc.nhatquangholding.com', port=443): Read timed out. (read timeout=20)" |  |
| 3 | `GET` | `/api/v1/codegen/health` | ✅ 200 | 24ms | {"healthy": true, "providers": {"app-builder": true, "ollama": true, "claude": false, "deepcode": fa |  |
| 4 | `POST` | `/api/v1/codegen/ir/validate` | ❌ 422 | 15ms | {"detail": [{"type": "missing", "loc": ["body", "blueprint"], "msg": "Field required", "input": {"sp | Missing required parameter |
| 5 | `GET` | `/api/v1/codegen/onboarding/options` | 🔴 404 | 19ms | {"detail": "Session not found"} | Route not registered / path incorrect |
| 6 | `GET` | `/api/v1/codegen/onboarding/options/domains` | ✅ 200 | 18ms | [{"key": "restaurant", "name": "Nha hang / Quan an", "name_en": "Restaurant / F&B", "description": " |  |
| 7 | `GET` | `/api/v1/codegen/onboarding/options/features/ecommerce` | ✅ 200 | 15ms | [{"key": "products", "name": "Quan ly san pham", "description": "Danh muc, gia ban, hinh anh"}, {"ke |  |
| 8 | `GET` | `/api/v1/codegen/onboarding/options/scales` | ✅ 200 | 16ms | [{"key": "micro", "label": "Ca nhan / 1-5 nhan vien", "employee_min": 1, "employee_max": 5, "cgf_tie |  |
| 9 | `POST` | `/api/v1/codegen/onboarding/start` | ✅ 200 | 15ms | {"session_id": "d1555ffe-99ab-452f-84bd-f9d5ad954b81", "current_step": "welcome", "completed_steps": |  |
| 10 | `GET` | `/api/v1/codegen/providers` | ✅ 200 | 18ms | {"providers": [{"name": "ollama", "available": true, "fallback_position": 0, "primary": true}, {"nam |  |
| 11 | `GET` | `/api/v1/codegen/providers/health` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 12 | `GET` | `/api/v1/codegen/providers/stats` | 🔴 404 | 16ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 13 | `GET` | `/api/v1/codegen/sessions` | ✅ 200 | 15ms | {"sessions": [], "total": 0, "page": 1, "page_size": 20} |  |
| 14 | `GET` | `/api/v1/codegen/sessions/09e33f72-f57e-45db-8bd2-d9791098444d` | 🔴 404 | 22ms | {"detail": "Session 09e33f72-f57e-45db-8bd2-d9791098444d not found or expired"} | Route not registered / path incorrect |
| 15 | `GET` | `/api/v1/codegen/sessions/09e33f72-f57e-45db-8bd2-d9791098444d/quality/stream` | ✅ 200 | 14ms | "data: {\"type\": \"error\", \"session_id\": \"09e33f72-f57e-45db-8bd2-d9791098444d\", \"message\":  |  |
| 16 | `GET` | `/api/v1/codegen/sessions/active` | ❌ 400 | 15ms | {"detail": "Invalid session ID format: active"} |  |
| 17 | `GET` | `/api/v1/codegen/templates` | ✅ 200 | 21ms | [{"id": "fastapi", "name": "FastAPI Service", "description": "Full CRUD service with authentication" |  |
| 18 | `GET` | `/api/v1/codegen/usage` | 🔴 404 | 24ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 19 | `GET` | `/api/v1/codegen/usage/monthly` | ❌ 422 | 15ms | {"detail": [{"type": "missing", "loc": ["query", "year"], "msg": "Field required", "input": null}, { | Missing required parameter |
| 20 | `GET` | `/api/v1/codegen/usage/provider-health/ollama` | 💥 500 | 21ms | Internal Server Error | DB migration missing / Service error |
| 21 | `GET` | `/api/v1/codegen/usage/report` | 💥 500 | 47ms | Internal Server Error | DB migration missing / Service error |

### Compliance

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/compliance/ai/budget` | ✅ 200 | 21ms | {"month": "2026-03", "total_spent": 0.0, "budget": 500.0, "remaining": 500.0, "percentage_used": 0.0 |  |
| 2 | `GET` | `/api/v1/compliance/ai/models` | ✅ 200 | 13ms | {"models": [], "default_model": "qwen3:32b", "ollama_url": "http://localhost:11434"} |  |
| 3 | `GET` | `/api/v1/compliance/ai/providers` | ✅ 200 | 17ms | {"ollama": {"healthy": false, "models": [], "version": "unknown", "error": "Connection refused - Oll |  |
| 4 | `GET` | `/api/v1/compliance/assessments` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/compliance/controls` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 6 | `GET` | `/api/v1/compliance/export` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 7 | `GET` | `/api/v1/compliance/frameworks` | 💥 500 | 31ms | Internal Server Error | DB migration missing / Service error |
| 8 | `GET` | `/api/v1/compliance/frameworks/OWASP` | 💥 500 | 18ms | "Internal Server Error" | DB migration missing / Service error |
| 9 | `GET` | `/api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/assessments` | 💥 500 | 17ms | "Internal Server Error" | DB migration missing / Service error |
| 10 | `POST` | `/api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence-mapping` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 11 | `GET` | `/api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/gap-analysis` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 12 | `GET` | `/api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/recommendations` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 13 | `GET` | `/api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/status` | 🔴 404 | 15ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 14 | `GET` | `/api/v1/compliance/queue/status` | ✅ 200 | 19ms | {"pending": 0, "running": 0, "completed": 0, "failed": 0, "total_jobs": 0} |  |
| 15 | `GET` | `/api/v1/compliance/scans/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | ✅ 200 | 16ms | [{"id": "fda86bce-a730-42ad-a713-ba3ffd718cb6", "compliance_score": 100, "violations_count": 0, "war |  |
| 16 | `GET` | `/api/v1/compliance/scans/3ec1d475-c294-40e9-806f-0691dffa3fa8/latest` | ✅ 200 | 17ms | {"id": "fda86bce-a730-42ad-a713-ba3ffd718cb6", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |
| 17 | `GET` | `/api/v1/compliance/status` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 18 | `GET` | `/api/v1/compliance/validation/rules` | 🔴 404 | 25ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 19 | `POST` | `/api/v1/compliance/validation/validate` | 🔴 404 | 16ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 20 | `GET` | `/api/v1/compliance/violations/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 15ms | [] |  |

### Compliance Validation

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/compliance-validation/checks` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/compliance-validation/status` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Consultations

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/consultations` | 💥 500 | 18ms | Internal Server Error | DB migration missing / Service error |
| 2 | `GET` | `/api/v1/consultations/my-reviews` | 💥 500 | 19ms | "Internal Server Error" | DB migration missing / Service error |

### Context Authority

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/context-authority/v2/contexts` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `POST` | `/api/v1/context-authority/v2/evaluate` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/context-authority/v2/health` | ✅ 200 | 20ms | {"status": "unhealthy", "version": "2.0.0", "template_count": 0, "snapshot_count_24h": 0, "avg_valid |  |
| 4 | `GET` | `/api/v1/context-authority/v2/project-profile` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/context-authority/v2/requirements` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 6 | `GET` | `/api/v1/context-authority/v2/snapshots/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 💥 500 | 17ms | {"detail": "Failed to list snapshots: (sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError) <cla | DB migration missing / Service error |
| 7 | `GET` | `/api/v1/context-authority/v2/stats` | 💥 500 | 19ms | {"detail": "Failed to get statistics: (sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError) <cla | DB migration missing / Service error |
| 8 | `GET` | `/api/v1/context-authority/v2/templates` | 💥 500 | 19ms | {"detail": "Failed to list templates: (sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError) <cla | DB migration missing / Service error |

### Context Authority V2

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/context-authority-v2/profile` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/context-authority-v2/requirements` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Context Validation

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/context-validation` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/context-validation/health` | ✅ 200 | 9ms | {"status": "healthy", "service": "context-validation", "version": "1.0.0", "max_lines_per_file": 60} |  |
| 3 | `GET` | `/api/v1/context-validation/limits` | 💥 500 | 11ms | "Internal Server Error" | DB migration missing / Service error |
| 4 | `GET` | `/api/v1/context-validation/status` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `POST` | `/api/v1/context-validation/validate` | ❌ 422 | 12ms | {"detail": [{"type": "missing", "loc": ["body", "content"], "msg": "Field required", "input": {"proj | Missing required parameter |

### Contract Lock

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/contract-lock` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/contract-lock/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/contract-lock/status` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Cross Reference

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/cross-reference` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/cross-reference/coverage/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 21ms | {"total": 0, "covered": 0, "uncovered": 0, "percentage": 0.0} |  |
| 3 | `GET` | `/api/v1/cross-reference/missing-tests/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 25ms | [] |  |
| 4 | `GET` | `/api/v1/cross-reference/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/cross-reference/ssot-check/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 19ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "ssot_compliant": true, "violations": [], "me |  |

### Cross Reference Validation

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/cross-reference-validation/status` | 🔴 404 | 15ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Dashboard

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/dashboard` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/dashboard/recent-gates` | ✅ 200 | 13ms | [{"id": "b1913ff7-15cb-4ad3-9846-4200ce4f70af", "gate_name": "Final Retest - Planning Review", "proj |  |
| 3 | `GET` | `/api/v1/dashboard/stats` | ✅ 200 | 17ms | {"total_projects": 7, "active_gates": 2, "pending_approvals": 2, "pass_rate": 0} |  |
| 4 | `GET` | `/api/v1/dashboard/summary` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Data Residency

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/data-residency` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/data-residency/config` | 🔴 404 | 17ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/data-residency/regions` | ✅ 200 | 18ms | {"regions": [{"region": "VN", "display_name": "Vietnam / Singapore (Asia Pacific)", "endpoint_url":  |  |

### Deprecation

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/deprecation/dashboard` | 💥 500 | 18ms | Internal Server Error | DB migration missing / Service error |
| 2 | `GET` | `/api/v1/deprecation/endpoints` | 💥 500 | 16ms | Internal Server Error | DB migration missing / Service error |
| 3 | `GET` | `/api/v1/deprecation/summary` | 💥 500 | 22ms | Internal Server Error | DB migration missing / Service error |
| 4 | `GET` | `/api/v1/deprecation/timeline` | 💥 500 | 26ms | Internal Server Error | DB migration missing / Service error |

### Deprecation Monitoring

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/deprecation-monitoring` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/deprecation-monitoring/endpoints` | 🔴 404 | 24ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/deprecation-monitoring/report` | 🔴 404 | 9ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/deprecation-monitoring/status` | 🔴 404 | 28ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Doc Cross Reference

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/doc-cross-reference/links` | ❌ 422 | 10ms | {"detail": [{"type": "missing", "loc": ["query", "project_id"], "msg": "Field required", "input": nu | Missing required parameter |
| 2 | `GET` | `/api/v1/doc-cross-reference/orphaned` | ❌ 422 | 10ms | {"detail": [{"type": "missing", "loc": ["query", "project_id"], "msg": "Field required", "input": nu | Missing required parameter |

### Docs

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/docs/list` | 🔴 404 | 9ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/docs/user-support` | ✅ 200 | 9ms | ["01-Getting-Started.md", "02-SDLC-Framework-Overview.md", "03-Platform-Features.md", "04-User-Roles |  |
| 3 | `GET` | `/api/v1/docs/user-support/01-Getting-Started.md` | 🔴 404 | 13ms | {"detail": "Documentation file '01-Getting-Started.md' not found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/docs/user-support/readme.md` | 🔴 404 | 10ms | {"detail": "Documentation file 'readme.md' not found"} | Route not registered / path incorrect |

### Dora

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/dora/metrics` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/dora/metrics/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### E2E

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/e2e/results` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `POST` | `/api/v1/e2e/run` | 🔴 404 | 26ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Enterprise

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/enterprise/audit` | ✅ 200 | 18ms | {"events": [], "total": 0, "page": 1, "page_size": 50, "has_more": false} |  |
| 2 | `GET` | `/api/v1/enterprise/sso/azure-ad/login` | ❌ 422 | 12ms | {"detail": [{"type": "missing", "loc": ["query", "organization_id"], "msg": "Field required", "input | Missing required parameter |
| 3 | `GET` | `/api/v1/enterprise/sso/saml/metadata` | ❌ 422 | 10ms | {"detail": [{"type": "missing", "loc": ["query", "organization_id"], "msg": "Field required", "input | Missing required parameter |

### Enterprise Sso

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/enterprise-sso` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/enterprise-sso/metadata` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/enterprise-sso/providers` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/enterprise-sso/status` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Evidence

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/evidence` | ✅ 200 | 20ms | {"items": [{"id": "036b2a6d-5959-4327-a77c-54ca4407847e", "gate_id": "1074f1fa-8f9e-4504-8656-0367b0 |  |
| 2 | `GET` | `/api/v1/evidence/` | ✅ 200 | 61ms | {"items": [{"id": "036b2a6d-5959-4327-a77c-54ca4407847e", "gate_id": "1074f1fa-8f9e-4504-8656-0367b0 |  |
| 3 | `GET` | `/api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e/download` | 🔴 404 | 15ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e/metadata` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 6 | `POST` | `/api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e/validate-content` | ✅ 200 | 43ms | {"score": 1.0, "passed": true, "document_type": "DOCUMENTATION", "missing_sections": [], "found_sect |  |
| 7 | `GET` | `/api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e/verify` | 🔴 404 | 17ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 8 | `GET` | `/api/v1/evidence/search` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 9 | `GET` | `/api/v1/evidence/statistics` | 🔴 404 | 9ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 10 | `POST` | `/api/v1/evidence/upload` | 🔴 404 | 0ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Evidence Manifest

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/evidence-manifest/` | 🔴 404 | 8ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `POST` | `/api/v1/evidence-manifest/` | 🔴 404 | 0ms | "{\"detail\":\"Not Found\"}" | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/evidence-manifest/dummy` | 🔴 404 | 19ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Evidence Manifests

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/evidence-manifests` | ✅ 200 | 17ms | {"total": 1, "manifests": [{"id": "b807b471-b8b5-430c-b240-7a1fdeeff3cf", "project_id": "3ec1d475-c2 |  |
| 2 | `POST` | `/api/v1/evidence-manifests` | ⚠️ 201 | 0ms | {"id": "b807b471-b8b5-430c-b240-7a1fdeeff3cf", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |
| 3 | `GET` | `/api/v1/evidence-manifests/b807b471-b8b5-430c-b240-7a1fdeeff3cf` | ✅ 200 | 22ms | {"id": "b807b471-b8b5-430c-b240-7a1fdeeff3cf", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |
| 4 | `GET` | `/api/v1/evidence-manifests/latest` | ❌ 422 | 17ms | {"detail": [{"type": "missing", "loc": ["query", "project_id"], "msg": "Field required", "input": nu | Missing required parameter |
| 5 | `GET` | `/api/v1/evidence-manifests/status` | ❌ 422 | 16ms | {"detail": [{"type": "missing", "loc": ["query", "project_id"], "msg": "Field required", "input": nu | Missing required parameter |
| 6 | `GET` | `/api/v1/evidence-manifests/verifications` | ❌ 422 | 17ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "manifest_id"], "msg": "Input should be a valid | Missing required parameter |
| 7 | `POST` | `/api/v1/evidence-manifests/verify` | ❌ 422 | 14ms | {"detail": [{"type": "missing", "loc": ["body", "project_id"], "msg": "Field required", "input": {"m | Missing required parameter |

### Evidence Timeline

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/evidence-timeline` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/evidence-timeline/` | 🔴 404 | 16ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/evidence-timeline/gates` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/evidence-timeline/summary` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Framework Version

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/framework-version` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/framework-version/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance` | 💥 500 | 20ms | "Internal Server Error" | DB migration missing / Service error |
| 3 | `GET` | `/api/v1/framework-version/3ec1d475-c294-40e9-806f-0691dffa3fa8/drift` | 💥 500 | 20ms | "Internal Server Error" | DB migration missing / Service error |
| 4 | `GET` | `/api/v1/framework-version/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | 💥 500 | 19ms | "Internal Server Error" | DB migration missing / Service error |
| 5 | `GET` | `/api/v1/framework-version/current` | ❌ 422 | 17ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "project_id"], "msg": "Input should be a valid  | Missing required parameter |
| 6 | `GET` | `/api/v1/framework-version/health` | ❌ 422 | 15ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "project_id"], "msg": "Input should be a valid  | Missing required parameter |
| 7 | `GET` | `/api/v1/framework-version/history` | ❌ 422 | 12ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "project_id"], "msg": "Input should be a valid  | Missing required parameter |
| 8 | `GET` | `/api/v1/framework-version/latest` | ❌ 422 | 15ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "project_id"], "msg": "Input should be a valid  | Missing required parameter |

### Gates

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/gates` | ✅ 200 | 15ms | {"items": [{"id": "b186b6cb-0320-4077-80e2-775c59f79bd8", "project_id": "3ec1d475-c294-40e9-806f-069 |  |
| 2 | `GET` | `/api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8` | ✅ 200 | 15ms | {"id": "b186b6cb-0320-4077-80e2-775c59f79bd8", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |
| 3 | `GET` | `/api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/ai-recommendations` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/approvals` | ✅ 200 | 16ms | [] |  |
| 5 | `GET` | `/api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/comments` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 6 | `POST` | `/api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/evaluate` | ✅ 200 | 40ms | {"gate_id": "b186b6cb-0320-4077-80e2-775c59f79bd8", "status": "EVALUATED", "evaluated_at": "2026-03- |  |
| 7 | `GET` | `/api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/evidence-summary` | 🔴 404 | 15ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 8 | `GET` | `/api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/exit-criteria` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 9 | `GET` | `/api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/history` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 10 | `GET` | `/api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/policy-result` | 🔴 404 | 25ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 11 | `GET` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af` | ✅ 200 | 33ms | {"id": "b1913ff7-15cb-4ad3-9846-4200ce4f70af", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |
| 12 | `GET` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/actions` | ✅ 200 | 24ms | {"gate_id": "b1913ff7-15cb-4ad3-9846-4200ce4f70af", "status": "EVALUATED", "actions": {"can_evaluate |  |
| 13 | `GET` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/approvals` | ✅ 200 | 19ms | [] |  |
| 14 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/approve` | ❌ 409 | 21ms | {"detail": "Cannot approve gate from status: EVALUATED. Allowed from: SUBMITTED"} |  |
| 15 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/break-glass-approve` | ❌ 422 | 20ms | {"detail": [{"type": "missing", "loc": ["body", "incident_ticket"], "msg": "Field required", "input" | Missing required parameter |
| 16 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/evaluate` | ✅ 200 | 33ms | {"gate_id": "b1913ff7-15cb-4ad3-9846-4200ce4f70af", "status": "EVALUATED", "evaluated_at": "2026-03- |  |
| 17 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/evidence` | 💥 500 | 0ms | {"detail": "Evidence storage failed: HTTPConnectionPool(host='minio', port=9000): Max retries exceed | DB migration missing / Service error |
| 18 | `GET` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/policy-result` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 19 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/reject` | ❌ 422 | 22ms | {"detail": [{"type": "missing", "loc": ["body", "comment"], "msg": "Field required", "input": {"reas | Missing required parameter |
| 20 | `POST` | `/api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/submit` | ❌ 422 | 19ms | {"detail": "Cannot submit: missing required evidence: BRD_COMPLETE, PRD_COMPLETE, STAKEHOLDER_SIGNOF | Missing required parameter |
| 21 | `GET` | `/api/v1/gates/export` | ❌ 422 | 14ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "gate_id"], "msg": "Input should be a valid UUI | Missing required parameter |
| 22 | `GET` | `/api/v1/gates/statistics` | ❌ 422 | 15ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "gate_id"], "msg": "Input should be a valid UUI | Missing required parameter |
| 23 | `GET` | `/api/v1/gates/types` | ❌ 422 | 14ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "gate_id"], "msg": "Input should be a valid UUI | Missing required parameter |

### Gates Engine

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/gates-engine/health` | ✅ 200 | 20ms | {"status": "healthy", "service": "gates_engine", "opa_available": true, "valid_gate_codes": ["G0.1", |  |
| 2 | `GET` | `/api/v1/gates-engine/policies` | 🔴 404 | 18ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/gates-engine/policies/G1_CONSULTATION` | ❌ 400 | 13ms | {"detail": "Invalid gate code: G1_CONSULTATION. Valid codes: G0.1, G0.2, G1, G2, G3, G4, G5, G6, G7, |  |
| 4 | `GET` | `/api/v1/gates-engine/prerequisites/G1_CONSULTATION` | ❌ 400 | 11ms | {"detail": "Invalid gate code: G1_CONSULTATION. Valid codes: G0.1, G0.2, G1, G2, G3, G4, G5, G6, G7, |  |
| 5 | `GET` | `/api/v1/gates-engine/readiness/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 31ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "total_gates": 5, "approved_count": 0, "curre |  |
| 6 | `GET` | `/api/v1/gates-engine/stages` | ✅ 200 | 16ms | {"G0.1": "WHY", "G0.2": "WHY", "G1": "WHAT", "G2": "HOW", "G3": "BUILD", "G4": "TEST", "G5": "DEPLOY |  |
| 7 | `GET` | `/api/v1/gates-engine/status` | 🔴 404 | 16ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Gdpr

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/gdpr/consents` | 🔴 404 | 17ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/gdpr/data-requests` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/gdpr/dsar` | ✅ 200 | 17ms | {"items": [{"id": "fd92da75-1708-4faf-9004-343af644fbb5", "request_type": "access", "status": "pendi |  |
| 4 | `POST` | `/api/v1/gdpr/export-request` | 🔴 404 | 9ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/gdpr/me/consents` | ✅ 200 | 14ms | {"consents": [{"id": "feb3d147-61a2-4607-8f75-b03d62986ef0", "purpose": "essential", "granted": true |  |
| 6 | `GET` | `/api/v1/gdpr/me/data-export` | ✅ 200 | 13ms | {"user_id": "a0000000-0000-0000-0000-000000000001", "generated_at": "2026-03-08T05:05:22.304787+00:0 |  |

### Github

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/github/app/status` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/github/installations` | 💥 500 | 23ms | Internal Server Error | DB migration missing / Service error |
| 3 | `GET` | `/api/v1/github/installations/3ec1d475-c294-40e9-806f-0691dffa3fa8/repositories` | 💥 500 | 13ms | Internal Server Error | DB migration missing / Service error |
| 4 | `GET` | `/api/v1/github/installations/3ec1d475-c294-40e9-806f-0691dffa3fa8/status` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/github/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/repository` | 💥 500 | 24ms | "Internal Server Error" | DB migration missing / Service error |
| 6 | `GET` | `/api/v1/github/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/scan` | 💥 500 | 19ms | "Internal Server Error" | DB migration missing / Service error |
| 7 | `GET` | `/api/v1/github/repos` | 🔴 404 | 17ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 8 | `POST` | `/api/v1/github/webhook` | 🔴 404 | 20ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 9 | `GET` | `/api/v1/github/webhooks` | ❌ 405 | 12ms | {"detail": "Method Not Allowed"} |  |
| 10 | `GET` | `/api/v1/github/webhooks/dlq` | 💥 500 | 14ms | "Internal Server Error" | DB migration missing / Service error |
| 11 | `GET` | `/api/v1/github/webhooks/jobs` | 🔴 404 | 23ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 12 | `GET` | `/api/v1/github/webhooks/jobs/dummy` | 🔴 404 | 22ms | {"detail": {"error": "job_not_found", "message": "Job dummy not found"}} | Route not registered / path incorrect |
| 13 | `GET` | `/api/v1/github/webhooks/stats` | 💥 500 | 16ms | "Internal Server Error" | DB migration missing / Service error |

### Governance

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/governance/dogfooding/status` | ✅ 200 | 11ms | {"phase": "week_1_preparation", "mode": "warning", "start_date": "2026-03-07T04:33:00.508460", "curr |  |
| 2 | `GET` | `/api/v1/governance/health` | ✅ 200 | 14ms | {"status": "healthy", "mode": "warning", "auto_rollback_enabled": true, "total_evaluations": 0, "lat |  |
| 3 | `GET` | `/api/v1/governance/metrics` | ✅ 200 | 13ms | {"mode": "warning", "total_evaluations": 0, "total_blocked": 0, "total_warned": 0, "total_passed": 0 |  |
| 4 | `GET` | `/api/v1/governance/metrics/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 19ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/governance/mode` | ✅ 200 | 13ms | {"mode": "warning", "previous_mode": null, "changed_at": "2026-03-07T04:33:00.508460", "changed_by": |  |
| 6 | `GET` | `/api/v1/governance/mode/state` | ✅ 200 | 13ms | {"mode": "warning", "previous_mode": null, "changed_at": "2026-03-07T04:33:00.508460", "changed_by": |  |
| 7 | `GET` | `/api/v1/governance/specs/health` | ❌ 422 | 11ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "spec_id"], "msg": "Input should be a valid UUI | Missing required parameter |
| 8 | `GET` | `/api/v1/governance/tiers/` | 💥 500 | 13ms | Internal Server Error | DB migration missing / Service error |
| 9 | `GET` | `/api/v1/governance/tiers/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 💥 500 | 23ms | Internal Server Error | DB migration missing / Service error |
| 10 | `GET` | `/api/v1/governance/tiers/LITE/requirements` | 💥 500 | 18ms | Internal Server Error | DB migration missing / Service error |
| 11 | `GET` | `/api/v1/governance/tiers/STANDARD/requirements` | 💥 500 | 14ms | "Internal Server Error" | DB migration missing / Service error |
| 12 | `GET` | `/api/v1/governance/tiers/health` | ❌ 422 | 13ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "project_id"], "msg": "Input should be a valid  | Missing required parameter |
| 13 | `GET` | `/api/v1/governance/vibecoding/health` | ❌ 422 | 15ms | {"detail": [{"type": "missing", "loc": ["query", "project_id"], "msg": "Field required", "input": nu | Missing required parameter |
| 14 | `GET` | `/api/v1/governance/vibecoding/stats/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 💥 500 | 17ms | {"detail": "Statistics query failed: (sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError) <clas | DB migration missing / Service error |

### Governance Metrics

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/governance-metrics` | ✅ 200 | 10ms | # HELP governance_submissions_total Total number of governance submissions # TYPE governance_submiss |  |
| 2 | `GET` | `/api/v1/governance-metrics/definitions` | ✅ 200 | 12ms | {"total": 47, "categories": {"governance_system": 15, "performance": 10, "business_ceo_dashboard": 8 |  |
| 3 | `GET` | `/api/v1/governance-metrics/health` | ✅ 200 | 10ms | {"status": "healthy", "service": "prometheus_metrics_collector", "timestamp": "2026-03-08T05:05:20.8 |  |
| 4 | `GET` | `/api/v1/governance-metrics/json` | ✅ 200 | 10ms | {"counters": {}, "gauges": {}, "histograms": {}, "timestamp": "2026-03-08T05:05:20.898895", "total_m |  |

### Governance Mode

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/governance-mode` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/governance-mode/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 23ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Governance Specs

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/governance-specs` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/governance-specs/list` | 🔴 404 | 25ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Governance Vibecoding

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/governance-vibecoding` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/governance-vibecoding/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/governance-vibecoding/score` | 🔴 404 | 24ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Grafana

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/grafana/dashboards` | 🔴 404 | 15ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/grafana/panels` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Grafana Dashboards

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/grafana-dashboards` | ✅ 200 | 19ms | {"dashboards": [{"uid": "ceo-dashboard", "title": "CEO Dashboard - Governance Intelligence", "descri |  |
| 2 | `GET` | `/api/v1/grafana-dashboards/datasource/template` | ✅ 200 | 13ms | {"name": "Prometheus-SDLC", "type": "prometheus", "access": "proxy", "url": "http://prometheus:9090" |  |
| 3 | `GET` | `/api/v1/grafana-dashboards/export/all` | ✅ 200 | 14ms | [{"uid": "ceo-dashboard", "title": "CEO Dashboard - Governance Intelligence", "description": "Execut |  |
| 4 | `GET` | `/api/v1/grafana-dashboards/gates` | ❌ 400 | 14ms | {"detail": "Invalid dashboard type: gates. Valid types: ceo, tech, ops"} |  |
| 5 | `GET` | `/api/v1/grafana-dashboards/overview` | ❌ 400 | 13ms | {"detail": "Invalid dashboard type: overview. Valid types: ceo, tech, ops"} |  |
| 6 | `GET` | `/api/v1/grafana-dashboards/overview/json` | ❌ 400 | 24ms | {"detail": "Invalid dashboard type: overview. Valid types: ceo, tech, ops"} |  |
| 7 | `GET` | `/api/v1/grafana-dashboards/overview/panels` | ❌ 400 | 13ms | {"detail": "Invalid dashboard type: overview. Valid types: ceo, tech, ops"} |  |

### Invitations

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/invitations` | 🔴 404 | 9ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `POST` | `/api/v1/invitations` | 🔴 404 | 0ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/invitations/dummy` | 💥 500 | 21ms | "Internal Server Error" | DB migration missing / Service error |

### Jira

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/jira` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/jira/connections` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/jira/projects` | 💥 500 | 17ms | Internal Server Error | DB migration missing / Service error |
| 4 | `POST` | `/api/v1/jira/sync` | ❌ 422 | 22ms | {"detail": [{"type": "missing", "loc": ["body", "gate_id"], "msg": "Field required", "input": {"proj | Missing required parameter |
| 5 | `GET` | `/api/v1/jira/sync-status` | 🔴 404 | 16ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Magic Link

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `POST` | `/api/v1/magic-link/verify` | ❌ 405 | 10ms | {"detail": "Method Not Allowed"} |  |

### Maturity

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/maturity/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 💥 500 | 22ms | Internal Server Error | DB migration missing / Service error |
| 2 | `GET` | `/api/v1/maturity/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | 💥 500 | 20ms | Internal Server Error | DB migration missing / Service error |
| 3 | `GET` | `/api/v1/maturity/assessment` | ❌ 422 | 20ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "project_id"], "msg": "Input should be a valid  | Missing required parameter |
| 4 | `GET` | `/api/v1/maturity/health` | ✅ 200 | 13ms | {"status": "healthy", "service": "agentic-maturity", "version": "1.0.0", "levels": ["L0", "L1", "L2" |  |
| 5 | `GET` | `/api/v1/maturity/levels` | ✅ 200 | 12ms | [{"level": "L0", "name": "Manual", "description": "Human writes all code, manual testing and reviews |  |

### Mcp

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/mcp/context` | 💥 500 | 22ms | Internal Server Error | DB migration missing / Service error |
| 2 | `GET` | `/api/v1/mcp/cost` | 💥 500 | 16ms | Internal Server Error | DB migration missing / Service error |
| 3 | `GET` | `/api/v1/mcp/dashboard` | 💥 500 | 16ms | Internal Server Error | DB migration missing / Service error |
| 4 | `GET` | `/api/v1/mcp/health` | 💥 500 | 18ms | Internal Server Error | DB migration missing / Service error |
| 5 | `GET` | `/api/v1/mcp/latency` | 💥 500 | 28ms | Internal Server Error | DB migration missing / Service error |

### Mcp Analytics

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/mcp-analytics` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/mcp-analytics/sessions` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/mcp-analytics/tools` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Mfa

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `POST` | `/api/v1/mfa/setup` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/mfa/status` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Mrp

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/mrp` | 🔴 404 | 30ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `POST` | `/api/v1/mrp` | 🔴 404 | 0ms | "{\"detail\":\"Not Found\"}" | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/mrp/dummy` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/mrp/health` | ✅ 200 | 13ms | {"status": "healthy", "service": "mrp-validation", "version": "1.0.0", "features": ["5-point-mrp-val |  |
| 5 | `GET` | `/api/v1/mrp/policies/compliance/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 19ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "current_tier": "PROFESSIONAL", "is_compliant |  |
| 6 | `GET` | `/api/v1/mrp/policies/tiers` | ✅ 200 | 19ms | {"tiers": [{"tier": "LITE", "display_name": "Lite", "description": "Advisory mode for individuals an |  |
| 7 | `GET` | `/api/v1/mrp/vcr/3ec1d475-c294-40e9-806f-0691dffa3fa8/history` | ✅ 200 | 24ms | {"id": "1eeb9e41-da40-4b28-9313-bbac7449bad8", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |

### Notifications

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/notifications` | ✅ 200 | 23ms | {"notifications": [], "total": 0, "unread_count": 0, "page": 1, "page_size": 20} |  |
| 2 | `GET` | `/api/v1/notifications/count` | ❌ 422 | 16ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "notification_id"], "msg": "Input should be a v | Missing required parameter |
| 3 | `GET` | `/api/v1/notifications/preferences` | ❌ 422 | 14ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "notification_id"], "msg": "Input should be a v | Missing required parameter |
| 4 | `POST` | `/api/v1/notifications/read-all` | ❌ 405 | 13ms | {"detail": "Method Not Allowed"} |  |
| 5 | `GET` | `/api/v1/notifications/settings/preferences` | ✅ 200 | 16ms | {"email_enabled": true, "slack_enabled": false, "slack_webhook_url": null, "teams_enabled": false, " |  |
| 6 | `GET` | `/api/v1/notifications/stats/summary` | ✅ 200 | 17ms | {"total": 0, "unread": 0, "read": 0, "by_type": {}, "unread_by_priority": {}} |  |
| 7 | `GET` | `/api/v1/notifications/unread-count` | ❌ 422 | 14ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "notification_id"], "msg": "Input should be a v | Missing required parameter |

### Organization Invitations

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/organization-invitations` | 🔴 404 | 9ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Organizations

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/organizations` | 💥 500 | 19ms | Internal Server Error | DB migration missing / Service error |

### Ott Gateway

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/ott-gateway` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/ott-gateway/channels` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `POST` | `/api/v1/ott-gateway/send` | 🔴 404 | 9ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/ott-gateway/status` | 🔴 404 | 31ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Override

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/override/dummy` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `POST` | `/api/v1/override/dummy/approve` | 🔴 404 | 22ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/override/history` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/override/queue` | 🔴 404 | 20ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `POST` | `/api/v1/override/request` | 🔴 404 | 0ms | "{\"detail\":\"Not Found\"}" | Route not registered / path incorrect |

### Payments

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/payments/me` | 🔴 404 | 15ms | {"detail": "Payment not found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/payments/plans` | 🔴 404 | 39ms | {"detail": "Payment not found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/payments/subscription` | 🔴 404 | 33ms | {"detail": "Payment not found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/payments/subscriptions/me` | 🔴 404 | 16ms | {"detail": "No subscription found"} | Route not registered / path incorrect |

### Planning

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/planning/action-items/dummy` | ❌ 422 | 12ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "item_id"], "msg": "Input should be a valid UUI | Missing required parameter |
| 2 | `POST` | `/api/v1/planning/allocations` | ❌ 400 | 0ms | {"detail": "User already allocated to this sprint"} |  |
| 3 | `GET` | `/api/v1/planning/allocations/dummy` | ❌ 422 | 12ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "allocation_id"], "msg": "Input should be a val | Missing required parameter |
| 4 | `GET` | `/api/v1/planning/backlog` | ✅ 200 | 17ms | {"items": [{"id": "135b6b04-5530-45d0-a3b2-a9fe5bc138f5", "project_id": "3ec1d475-c294-40e9-806f-069 |  |
| 5 | `GET` | `/api/v1/planning/backlog/135b6b04-5530-45d0-a3b2-a9fe5bc138f5` | ✅ 200 | 16ms | {"id": "135b6b04-5530-45d0-a3b2-a9fe5bc138f5", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |
| 6 | `PUT` | `/api/v1/planning/backlog/135b6b04-5530-45d0-a3b2-a9fe5bc138f5` | ✅ 200 | 18ms | {"id": "135b6b04-5530-45d0-a3b2-a9fe5bc138f5", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |
| 7 | `GET` | `/api/v1/planning/backlog/assignees/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 15ms | [] |  |
| 8 | `GET` | `/api/v1/planning/dashboard/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 23ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "roadmaps": [{"id": "624cc6c6-115f-4609-8b1d- |  |
| 9 | `GET` | `/api/v1/planning/dependencies` | ❌ 405 | 12ms | {"detail": "Method Not Allowed"} |  |
| 10 | `GET` | `/api/v1/planning/dependencies/check-circular` | ❌ 422 | 13ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "dependency_id"], "msg": "Input should be a val | Missing required parameter |
| 11 | `GET` | `/api/v1/planning/phases` | ❌ 422 | 13ms | {"detail": [{"type": "missing", "loc": ["query", "roadmap_id"], "msg": "Field required", "input": nu | Missing required parameter |
| 12 | `GET` | `/api/v1/planning/phases/55bec71c-8228-4b39-8a78-a34de8b3dc8d` | ✅ 200 | 16ms | {"id": "55bec71c-8228-4b39-8a78-a34de8b3dc8d", "roadmap_id": "624cc6c6-115f-4609-8b1d-dd1912fd527b", |  |
| 13 | `PUT` | `/api/v1/planning/phases/55bec71c-8228-4b39-8a78-a34de8b3dc8d` | ✅ 200 | 21ms | {"id": "55bec71c-8228-4b39-8a78-a34de8b3dc8d", "roadmap_id": "624cc6c6-115f-4609-8b1d-dd1912fd527b", |  |
| 14 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/dependency-analysis` | ✅ 200 | 18ms | {"total_dependencies": 0, "blocking_dependencies": 0, "cross_project_dependencies": 0, "pending_depe |  |
| 15 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/dependency-graph` | ✅ 200 | 19ms | {"nodes": [], "edges": [], "total_sprints": 0, "total_dependencies": 0, "blocking_dependencies": 0,  |  |
| 16 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/resource-heatmap` | ✅ 200 | 23ms | {"users": [{"id": "2e542eba-b1b5-4f91-ab82-b853a6887b8d", "name": "*-CyEyes-* S4 Admin", "email": "c |  |
| 17 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/retrospective-comparison` | ❌ 422 | 14ms | {"detail": [{"type": "missing", "loc": ["query", "sprint_ids"], "msg": "Field required", "input": nu | Missing required parameter |
| 18 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/template-suggestions` | ✅ 200 | 21ms | {"suggestions": [{"template_id": "df4beaf4-54e8-48fd-98d0-98c03daae6e4", "template_name": "Feature S |  |
| 19 | `GET` | `/api/v1/planning/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/velocity` | ✅ 200 | 18ms | {"average": 0.0, "trend": "unknown", "confidence": 0.0, "history": [], "sprint_count": 0, "project_i |  |
| 20 | `GET` | `/api/v1/planning/roadmaps` | ✅ 200 | 14ms | {"items": [{"id": "624cc6c6-115f-4609-8b1d-dd1912fd527b", "project_id": "3ec1d475-c294-40e9-806f-069 |  |
| 21 | `GET` | `/api/v1/planning/roadmaps/624cc6c6-115f-4609-8b1d-dd1912fd527b` | ✅ 200 | 18ms | {"id": "624cc6c6-115f-4609-8b1d-dd1912fd527b", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |
| 22 | `PUT` | `/api/v1/planning/roadmaps/624cc6c6-115f-4609-8b1d-dd1912fd527b` | ✅ 200 | 20ms | {"id": "624cc6c6-115f-4609-8b1d-dd1912fd527b", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |
| 23 | `GET` | `/api/v1/planning/sprints` | ✅ 200 | 16ms | {"items": [{"id": "901b185c-a99d-44f9-af4a-91ac8891e449", "project_id": "3ec1d475-c294-40e9-806f-069 |  |
| 24 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449` | ✅ 200 | 16ms | {"id": "901b185c-a99d-44f9-af4a-91ac8891e449", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |
| 25 | `PUT` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449` | ✅ 200 | 22ms | {"id": "901b185c-a99d-44f9-af4a-91ac8891e449", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", |  |
| 26 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/action-items` | ✅ 200 | 15ms | {"items": [], "total": 0, "page": 1, "page_size": 20} |  |
| 27 | `POST` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/action-items` | ❌ 422 | 0ms | {"detail": [{"type": "value_error", "loc": ["body", "priority"], "msg": "Value error, priority must  | Missing required parameter |
| 28 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/action-items/stats` | ✅ 200 | 13ms | {"total_items": 0, "open_items": 0, "in_progress_items": 0, "completed_items": 0, "cancelled_items": |  |
| 29 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/allocations` | ✅ 200 | 14ms | {"items": [{"allocation_percentage": 100, "role": "developer", "notes": null, "id": "0cb006df-d414-4 |  |
| 30 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/analytics` | ✅ 200 | 29ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "sprint_number": 1, "sprint_name": "*-CyEyes-* |  |
| 31 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/burndown` | ✅ 200 | 27ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "sprint_number": 1, "sprint_name": "*-CyEyes-* |  |
| 32 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/capacity` | ✅ 200 | 25ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "sprint_number": 1, "sprint_name": "*-CyEyes-* |  |
| 33 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/dependencies` | ✅ 200 | 17ms | {"items": [], "total": 0, "page": 1, "page_size": 20} |  |
| 34 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/forecast` | ✅ 200 | 16ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "sprint_number": 1, "sprint_name": "*-CyEyes-* |  |
| 35 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/gates` | ✅ 200 | 14ms | [] |  |
| 36 | `POST` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/gates` | ❌ 422 | 27ms | {"detail": [{"type": "enum", "loc": ["body", "gate_type"], "msg": "Input should be 'g_sprint' or 'g_ | Missing required parameter |
| 37 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/gates/G_SPRINT` | ❌ 422 | 20ms | {"detail": [{"type": "enum", "loc": ["path", "gate_type"], "msg": "Input should be 'g_sprint' or 'g_ | Missing required parameter |
| 38 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/health` | ✅ 200 | 21ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "completion_rate": 0.0, "completed_points": 0, |  |
| 39 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/retrospective` | ✅ 200 | 22ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "sprint_number": 1, "sprint_name": "*-CyEyes-* |  |
| 40 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/suggestions` | ✅ 200 | 18ms | {"sprint_id": "901b185c-a99d-44f9-af4a-91ac8891e449", "suggestions": [{"type": "unassigned_priority" |  |
| 41 | `GET` | `/api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/velocity` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 42 | `POST` | `/api/v1/planning/subagent/conformance` | ❌ 422 | 17ms | {"detail": [{"type": "missing", "loc": ["body", "diff_content"], "msg": "Field required", "input": { | Missing required parameter |
| 43 | `GET` | `/api/v1/planning/subagent/health` | ✅ 200 | 17ms | {"status": "healthy", "service": "planning-subagent", "version": "2.0.0", "features": ["risk-based-p |  |
| 44 | `POST` | `/api/v1/planning/subagent/plan` | ❌ 422 | 17ms | {"detail": [{"type": "missing", "loc": ["body", "task"], "msg": "Field required", "input": {"project | Missing required parameter |
| 45 | `GET` | `/api/v1/planning/subagent/sessions` | ❌ 422 | 19ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "planning_id"], "msg": "Input should be a valid | Missing required parameter |
| 46 | `POST` | `/api/v1/planning/subagent/should-plan` | ❌ 422 | 14ms | {"detail": [{"type": "missing", "loc": ["body", "diff"], "msg": "Field required", "input": {"project | Missing required parameter |
| 47 | `GET` | `/api/v1/planning/summary` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 48 | `GET` | `/api/v1/planning/templates` | ✅ 200 | 28ms | {"items": [{"name": "Release Sprint", "description": "Sprint focused on preparing and executing a re |  |
| 49 | `POST` | `/api/v1/planning/templates` | ⚠️ 201 | 30ms | {"name": "*-CyEyes-* Template", "description": null, "template_type": "standard", "duration_days": 1 |  |
| 50 | `GET` | `/api/v1/planning/templates/default` | ❌ 422 | 14ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "template_id"], "msg": "Input should be a valid | Missing required parameter |
| 51 | `GET` | `/api/v1/planning/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/allocations` | 💥 500 | 20ms | "Internal Server Error" | DB migration missing / Service error |
| 52 | `GET` | `/api/v1/planning/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/capacity` | ❌ 422 | 14ms | {"detail": [{"type": "missing", "loc": ["query", "start_date"], "msg": "Field required", "input": nu | Missing required parameter |

### Planning Subagent

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/planning-subagent/sessions` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/planning-subagent/status` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Policies

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/policies` | ✅ 200 | 16ms | {"items": [], "total": 0, "page": 1, "page_size": 20, "pages": 0} |  |
| 2 | `POST` | `/api/v1/policies` | ❌ 405 | 0ms | "{\"detail\":\"Method Not Allowed\"}" |  |
| 3 | `POST` | `/api/v1/policies/evaluate` | ❌ 422 | 14ms | {"detail": [{"type": "uuid_parsing", "loc": ["body", "policy_id"], "msg": "Input should be a valid U | Missing required parameter |
| 4 | `GET` | `/api/v1/policies/evaluations/b1913ff7-15cb-4ad3-9846-4200ce4f70af` | ✅ 200 | 22ms | {"items": [], "total": 0, "passed": 0, "failed": 0, "pass_rate": 0.0} |  |

### Policy Packs

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/policy-packs` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/policy-packs/categories` | 🔴 404 | 9ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Preview

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/preview` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/preview/dummy` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/preview/gates` | 🔴 404 | 21ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Projects

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/projects` | ✅ 200 | 17ms | [{"id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "name": "CyEyes-S4", "description": "*-CyEyes-* sess |  |
| 2 | `GET` | `/api/v1/projects/` | ✅ 200 | 50ms | [{"id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "name": "CyEyes-Updated", "description": "*-CyEyes-* |  |
| 3 | `POST` | `/api/v1/projects/` | ✅ 200 | 53ms | [{"id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "name": "CyEyes-S4", "description": "*-CyEyes-* sess |  |
| 4 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 27ms | {"id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "name": "CyEyes-S4", "description": "*-CyEyes-* sessi |  |
| 5 | `PUT` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 50ms | {"id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "name": "CyEyes-S4", "slug": "final-retest", "descrip |  |
| 6 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/activity` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 7 | `POST` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/archive` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 8 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance-summary` | ✅ 200 | 23ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "project_name": "CyEyes-S4", "tier": "profess |  |
| 9 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance/history` | 💥 500 | 19ms | "Internal Server Error" | DB migration missing / Service error |
| 10 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance/last-check` | 💥 500 | 21ms | "Internal Server Error" | DB migration missing / Service error |
| 11 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/compliance/score` | 💥 500 | 28ms | "Internal Server Error" | DB migration missing / Service error |
| 12 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/context` | ✅ 200 | 26ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "stage": "06-DEPLOY", "gate": "Final Retest - |  |
| 13 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/dashboard` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 14 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence/gaps` | ✅ 200 | 16ms | {"gaps": {"missing_evidence": [], "backend_gaps": [], "frontend_gaps": [], "extension_gaps": [], "cl |  |
| 15 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence/status` | ✅ 200 | 29ms | {"status": "complete", "gaps": {"backend": [], "frontend": [], "extension": [], "cli": []}, "total_g |  |
| 16 | `POST` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence/validate` | ✅ 200 | 15ms | {"validation_id": "val-1772877275.6906", "status": "complete", "violations": [], "summary": {"errors |  |
| 17 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/github-status` | 🔴 404 | 15ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 18 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/members` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 19 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/overrides` | ✅ 200 | 17ms | [] |  |
| 20 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/policy-pack` | ✅ 200 | 22ms | {"name": "Standard Policy Pack", "description": "Auto-configured Standard tier policy pack for Final |  |
| 21 | `POST` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/restore` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 22 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/sdlc-info` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 23 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/stats` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 24 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/tier-info` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 25 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/timeline` | ✅ 200 | 39ms | {"events": [], "stats": {"total_events": 0, "ai_detected": 0, "pass_rate": 0.0, "override_rate": 0.0 |  |
| 26 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/timeline/stats` | ✅ 200 | 21ms | {"total_events": 0, "ai_detected": 0, "pass_rate": 0.0, "override_rate": 0.0, "by_tool": {}, "by_sta |  |
| 27 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/usage` | 🔴 404 | 19ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 28 | `GET` | `/api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/validation-history` | ✅ 200 | 26ms | [] |  |

### Push

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/push/status` | ✅ 200 | 16ms | {"is_subscribed": false, "subscriptions_count": 0} |  |
| 2 | `GET` | `/api/v1/push/subscriptions` | ✅ 200 | 14ms | {"subscriptions": [], "total": 0} |  |
| 3 | `GET` | `/api/v1/push/vapid-key` | ✅ 200 | 13ms | {"public_key": "BNbxGGkqLJiJqhspMQU0JCzKHJtKqkq0TdVbJGiWFhB1GGJhkPGiWFhB1GGJhkPGiWFhB1GGJhkPGiWFhB1G |  |

### Push Notifications

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/push-notifications` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `POST` | `/api/v1/push-notifications/subscribe` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Risk

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/risk/factors` | ✅ 200 | 16ms | [{"factor": "data_schema", "name": "Data Schema Changes", "description": "Migrations, model changes, |  |
| 2 | `GET` | `/api/v1/risk/levels` | ✅ 200 | 13ms | {"levels": [{"level": "minimal", "score_range": "0-20", "planning_required": false, "description": " |  |
| 3 | `GET` | `/api/v1/risk/should-plan` | ❌ 422 | 20ms | {"detail": [{"type": "missing", "loc": ["query", "diff"], "msg": "Field required", "input": null}],  | Missing required parameter |

### Risk Analysis

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/risk-analysis` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `POST` | `/api/v1/risk-analysis/analyze` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/risk-analysis/items` | 🔴 404 | 16ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/risk-analysis/overview` | 🔴 404 | 17ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/risk-analysis/project/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Root

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/` | ✅ 200 | 15ms | "<!DOCTYPE html><html lang=\"vi\"><head><meta charSet=\"utf-8\"/><meta name=\"viewport\" content=\"w |  |
| 2 | `GET` | `/health` | ✅ 200 | 15ms | {"status": "healthy", "version": "1.2.0", "service": "sdlc-orchestrator-backend"} |  |
| 3 | `GET` | `/health/ready` | 💥 503 | 9204ms | {"status": "not_ready", "dependencies": {"postgres": {"status": "connected", "healthy": true}, "redi | DB migration missing / Service error |
| 4 | `GET` | `/metrics` | 🔴 404 | 49ms | "<!DOCTYPE html><html lang=\"vi\"><head><meta charSet=\"utf-8\"/><meta name=\"viewport\" content=\"w | Route not registered / path incorrect |
| 5 | `GET` | `/ws/stats` | 🔴 404 | 20ms | "<!DOCTYPE html><html lang=\"vi\"><head><meta charSet=\"utf-8\"/><meta name=\"viewport\" content=\"w | Route not registered / path incorrect |

### Sast

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/sast/health` | ✅ 200 | 12ms | {"status": "degraded", "semgrep_available": false, "custom_rules": {"ai_security": false, "owasp_pyt |  |
| 2 | `GET` | `/api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/analytics` | 💥 500 | 17ms | Internal Server Error | DB migration missing / Service error |
| 3 | `POST` | `/api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/scan` | ✅ 200 | 19ms | {"scan_id": "9762c907-074e-4523-9945-eef1fadad2eb", "project_id": "3ec1d475-c294-40e9-806f-0691dffa3 |  |
| 4 | `GET` | `/api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/scans` | 💥 500 | 14ms | Internal Server Error | DB migration missing / Service error |
| 5 | `GET` | `/api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/scans/09e33f72-f57e-45db-8bd2-d9791098444d` | 💥 500 | 15ms | "Internal Server Error" | DB migration missing / Service error |
| 6 | `GET` | `/api/v1/sast/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/trend` | 💥 500 | 16ms | Internal Server Error | DB migration missing / Service error |
| 7 | `POST` | `/api/v1/sast/scan-snippet` | ✅ 200 | 13ms | {"scan_id": "2f72718b-6866-4a28-b58d-90845bef4b73", "project_id": "66dddcdf-2209-4c3e-8a70-4d666207b |  |

### Sdlc Structure

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/sdlc-structure` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/sdlc-structure/report` | 🔴 404 | 9ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/sdlc-structure/status` | 🔴 404 | 8ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `POST` | `/api/v1/sdlc-structure/validate` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/sdlc-structure/validate` | 🔴 404 | 9ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Skill Grants?Project Id=3Ec1D475 C294 40E9 806F 0691Dffa3Fa8

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/skill-grants?project_id=3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Skills

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/skills` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/skills/grants?project_id=3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Stage Gating

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/stage-gating` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/stage-gating/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/stage-gating/health` | ✅ 200 | 18ms | {"status": "healthy", "service": "stage_gating", "stages_configured": 11, "timestamp": "2026-03-08T0 |  |
| 4 | `GET` | `/api/v1/stage-gating/progress/3ec1d475-c294-40e9-806f-0691dffa3fa8` | ✅ 200 | 23ms | {"project_id": "3ec1d475-c294-40e9-806f-0691dffa3fa8", "current_stage": "stage_04_build", "completed |  |
| 5 | `GET` | `/api/v1/stage-gating/rules` | ✅ 200 | 20ms | {"stages": {"stage_00_foundation": {"stage": "stage_00_foundation", "allows": ["docs/00-foundation/* |  |
| 6 | `GET` | `/api/v1/stage-gating/rules/STAGE_00` | 🔴 404 | 11ms | {"detail": "Stage not found: STAGE_00"} | Route not registered / path incorrect |

### Teams

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/teams` | 💥 500 | 16ms | Internal Server Error | DB migration missing / Service error |

### Teams?Project Id=3Ec1D475 C294 40E9 806F 0691Dffa3Fa8

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/teams?project_id=3ec1d475-c294-40e9-806f-0691dffa3fa8` | 💥 500 | 14ms | Internal Server Error | DB migration missing / Service error |

### Telemetry

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/telemetry` | 🔴 404 | 12ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/telemetry/dashboard` | 💥 500 | 19ms | Internal Server Error | DB migration missing / Service error |
| 3 | `POST` | `/api/v1/telemetry/event` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/telemetry/events` | ❌ 405 | 12ms | {"detail": "Method Not Allowed"} |  |
| 5 | `GET` | `/api/v1/telemetry/funnels/onboarding` | ❌ 400 | 14ms | {"detail": "Unknown funnel: onboarding"} |  |
| 6 | `GET` | `/api/v1/telemetry/health` | ✅ 200 | 13ms | {"status": "healthy", "service": "telemetry", "version": "1.0.0", "funnels_available": ["time_to_fir |  |
| 7 | `GET` | `/api/v1/telemetry/interfaces` | 💥 500 | 16ms | Internal Server Error | DB migration missing / Service error |

### Templates

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/templates` | 🔴 404 | 16ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/templates/categories` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/templates/sdlc-structure` | ✅ 200 | 10ms | {"version": "5.0.0", "tier": "STANDARD", "tier_description": "Standard documentation for most projec |  |
| 4 | `GET` | `/api/v1/templates/stages` | ✅ 200 | 10ms | {"version": "5.0.0", "stages": {"00": {"id": "00", "name": "foundation", "full_name": "Foundation (W |  |
| 5 | `GET` | `/api/v1/templates/tiers` | ✅ 200 | 16ms | {"version": "5.0.0", "tiers": {"LITE": {"team_size_range": "1-2", "required_stages": ["00", "01", "0 |  |

### Tier Management

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/tier-management` | 🔴 404 | 13ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/tier-management/current` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `GET` | `/api/v1/tier-management/limits` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 4 | `GET` | `/api/v1/tier-management/plans` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 5 | `GET` | `/api/v1/tier-management/usage` | 🔴 404 | 19ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Triage

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/triage/issues` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/triage/sla-breaches` | 💥 500 | 23ms | Internal Server Error | DB migration missing / Service error |
| 3 | `GET` | `/api/v1/triage/stats` | ✅ 200 | 26ms | {"by_status": {}, "by_priority": {}, "untriaged_count": 0, "total": 0, "triage_rate": 0.0} |  |
| 4 | `GET` | `/api/v1/triage/summary` | 🔴 404 | 10ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Usage

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/usage/current` | 🔴 404 | 24ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/usage/history` | 🔴 404 | 49ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Vcr

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/vcr` | 💥 500 | 17ms | Internal Server Error | DB migration missing / Service error |
| 2 | `POST` | `/api/v1/vcr` | 💥 500 | 0ms | "{\"detail\":\"(sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError) <class 'asyncpg.exceptions. | DB migration missing / Service error |
| 3 | `GET` | `/api/v1/vcr/dummy` | ❌ 422 | 16ms | {"detail": [{"type": "uuid_parsing", "loc": ["path", "vcr_id"], "msg": "Input should be a valid UUID | Missing required parameter |
| 4 | `GET` | `/api/v1/vcr/stats/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 💥 500 | 17ms | "Internal Server Error" | DB migration missing / Service error |

### Vibecoding

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/vibecoding/health` | ✅ 200 | 18ms | {"status": "healthy", "service": "vibecoding_index_engine", "signals_configured": 5, "critical_path_ |  |
| 2 | `GET` | `/api/v1/vibecoding/stats` | ✅ 200 | 11ms | {"total_calculations": 0, "average_score": 0.0, "category_distribution": {"green": 0, "yellow": 0, " |  |
| 3 | `GET` | `/api/v1/vibecoding/thresholds` | ✅ 200 | 12ms | {"thresholds": {"green": {"min": 0, "max": 30}, "yellow": {"min": 31, "max": 60}, "orange": {"min":  |  |

### Vibecoding Index

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/vibecoding-index` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/vibecoding-index/3ec1d475-c294-40e9-806f-0691dffa3fa8` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 3 | `POST` | `/api/v1/vibecoding-index/3ec1d475-c294-40e9-806f-0691dffa3fa8/calculate` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Websocket

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/websocket/status` | 🔴 404 | 14ms | {"detail": "Not Found"} | Route not registered / path incorrect |

### Workflows

| # | Method | Endpoint | Status | ms | Response | Root Cause |
|---|--------|----------|--------|-----|----------|------------|
| 1 | `GET` | `/api/v1/workflows` | 🔴 404 | 11ms | {"detail": "Not Found"} | Route not registered / path incorrect |
| 2 | `GET` | `/api/v1/workflows/b186b6cb-0320-4077-80e2-775c59f79bd8/status` | 💥 500 | 89ms | Internal Server Error | DB migration missing / Service error |

## Required Actions (Next Sprint)

### P0 — DB Migrations (affects ~65 endpoints)

Run the following Alembic migrations in production:
```bash
# SSH into production server, then:
cd /app && alembic upgrade head

# Or run specific migrations:
alembic upgrade s176_001  # Agent Team tables (EP-07)
alembic upgrade s209_004  # SAST tables
alembic upgrade s151_001  # VCR tables
alembic upgrade s120_001  # Context Authority V2 tables
alembic upgrade s104_001  # Maturity Assessment tables
alembic upgrade s101_002  # CRP tables
```

### P1 — External Service Configuration

| Service | Env Var | Impact |
|---------|---------|--------|
| GitHub App | `GITHUB_APP_ID`, `GITHUB_PRIVATE_KEY` | 8 github/* endpoints |
| Telegram Bot | `TELEGRAM_BOT_TOKEN` | OTT gateway endpoints |
| Jira | `JIRA_URL`, `JIRA_TOKEN` | jira/* endpoints |

### P2 — 404 Paths (confirm correct routes)

**223 endpoints** returned 404 — may be spec paths not yet deployed:

```
GET    /api/v1/admin/ai-providers
POST   /api/v1/admin/broadcast
POST   /api/v1/admin/cache/clear
GET    /api/v1/admin/metrics
GET    /api/v1/admin/ott-channels
GET    /api/v1/admin/ott-channels/health
POST   /api/v1/admin/ott-channels/telegram/send
GET    /api/v1/admin/settings/maintenance_mode
GET    /api/v1/admin/usage
POST   /api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/activate
PUT    /api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/role
POST   /api/v1/admin/users/2e542eba-b1b5-4f91-ab82-b853a6887b8d/suspend
GET    /api/v1/agentic-maturity
GET    /api/v1/agentic-maturity/project/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/agents-md
POST   /api/v1/agents-md/3ec1d475-c294-40e9-806f-0691dffa3fa8/generate
GET    /api/v1/agents/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/agents/3ec1d475-c294-40e9-806f-0691dffa3fa8/history
GET    /api/v1/ai-detection
POST   /api/v1/ai-detection/detect
GET    /api/v1/ai-providers
GET    /api/v1/ai-providers/health
GET    /api/v1/analytics-v2/dora
GET    /api/v1/analytics-v2/evidence
GET    /api/v1/analytics-v2/gates
GET    /api/v1/analytics-v2/overview
GET    /api/v1/analytics/v2/trends
GET    /api/v1/analytics/v2/usage
GET    /api/v1/audit-trail
GET    /api/v1/audit-trail/logs
GET    /api/v1/audit-trail/resource/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/auth/mfa/qr-code
POST   /api/v1/auth/mfa/setup
GET    /api/v1/auth/mfa/status
GET    /api/v1/auth/sessions
GET    /api/v1/auth/users
GET    /api/v1/auth/users/a0000000-0000-0000-0000-000000000001
GET    /api/v1/auto-generation
POST   /api/v1/auto-generation/generate
GET    /api/v1/auto-generation/project/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/auto-generation/status
GET    /api/v1/auto-generation/templates
GET    /api/v1/ceo-dashboard
GET    /api/v1/ceo-dashboard/project/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/channels
GET    /api/v1/check-runs/project/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/codegen/onboarding/options
GET    /api/v1/codegen/providers/health
GET    /api/v1/codegen/providers/stats
GET    /api/v1/codegen/sessions/09e33f72-f57e-45db-8bd2-d9791098444d
GET    /api/v1/codegen/usage
GET    /api/v1/compliance-validation/checks
GET    /api/v1/compliance-validation/status
GET    /api/v1/compliance/assessments
GET    /api/v1/compliance/controls
GET    /api/v1/compliance/export
POST   /api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/evidence-mapping
GET    /api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/gap-analysis
GET    /api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/recommendations
GET    /api/v1/compliance/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/status
GET    /api/v1/compliance/status
GET    /api/v1/compliance/validation/rules
POST   /api/v1/compliance/validation/validate
GET    /api/v1/context-authority-v2/profile
GET    /api/v1/context-authority-v2/requirements
GET    /api/v1/context-authority/v2/contexts
POST   /api/v1/context-authority/v2/evaluate
GET    /api/v1/context-authority/v2/project-profile
GET    /api/v1/context-authority/v2/requirements
GET    /api/v1/context-validation
GET    /api/v1/context-validation/status
GET    /api/v1/contract-lock
GET    /api/v1/contract-lock/project/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/contract-lock/status
GET    /api/v1/cross-reference
GET    /api/v1/cross-reference-validation/status
GET    /api/v1/cross-reference/project/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/dashboard
GET    /api/v1/dashboard/summary
GET    /api/v1/data-residency
GET    /api/v1/data-residency/config
GET    /api/v1/deprecation-monitoring
GET    /api/v1/deprecation-monitoring/endpoints
GET    /api/v1/deprecation-monitoring/report
GET    /api/v1/deprecation-monitoring/status
GET    /api/v1/docs/list
GET    /api/v1/docs/user-support/01-Getting-Started.md
GET    /api/v1/docs/user-support/readme.md
GET    /api/v1/dora/metrics
GET    /api/v1/dora/metrics/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/e2e/results
POST   /api/v1/e2e/run
GET    /api/v1/enterprise-sso
GET    /api/v1/enterprise-sso/metadata
GET    /api/v1/enterprise-sso/providers
GET    /api/v1/enterprise-sso/status
GET    /api/v1/evidence-manifest/
POST   /api/v1/evidence-manifest/
GET    /api/v1/evidence-manifest/dummy
GET    /api/v1/evidence-timeline
GET    /api/v1/evidence-timeline/
GET    /api/v1/evidence-timeline/gates
GET    /api/v1/evidence-timeline/summary
GET    /api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e
GET    /api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e/download
GET    /api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e/metadata
GET    /api/v1/evidence/036b2a6d-5959-4327-a77c-54ca4407847e/verify
GET    /api/v1/evidence/search
GET    /api/v1/evidence/statistics
POST   /api/v1/evidence/upload
GET    /api/v1/framework-version
GET    /api/v1/gates-engine/policies
GET    /api/v1/gates-engine/status
GET    /api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/ai-recommendations
GET    /api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/comments
GET    /api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/evidence-summary
GET    /api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/exit-criteria
GET    /api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/history
GET    /api/v1/gates/b186b6cb-0320-4077-80e2-775c59f79bd8/policy-result
GET    /api/v1/gates/b1913ff7-15cb-4ad3-9846-4200ce4f70af/policy-result
GET    /api/v1/gdpr/consents
GET    /api/v1/gdpr/data-requests
POST   /api/v1/gdpr/export-request
GET    /api/v1/github/app/status
GET    /api/v1/github/installations/3ec1d475-c294-40e9-806f-0691dffa3fa8/status
GET    /api/v1/github/repos
POST   /api/v1/github/webhook
GET    /api/v1/github/webhooks/jobs
GET    /api/v1/github/webhooks/jobs/dummy
GET    /api/v1/governance-mode
GET    /api/v1/governance-mode/project/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/governance-specs
GET    /api/v1/governance-specs/list
GET    /api/v1/governance-vibecoding
GET    /api/v1/governance-vibecoding/project/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/governance-vibecoding/score
GET    /api/v1/governance/metrics/project/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/grafana/dashboards
GET    /api/v1/grafana/panels
GET    /api/v1/invitations
POST   /api/v1/invitations
GET    /api/v1/jira
GET    /api/v1/jira/connections
GET    /api/v1/jira/sync-status
GET    /api/v1/mcp-analytics
GET    /api/v1/mcp-analytics/sessions
GET    /api/v1/mcp-analytics/tools
POST   /api/v1/mfa/setup
GET    /api/v1/mfa/status
GET    /api/v1/mrp
POST   /api/v1/mrp
GET    /api/v1/mrp/dummy
GET    /api/v1/organization-invitations
GET    /api/v1/ott-gateway
GET    /api/v1/ott-gateway/channels
POST   /api/v1/ott-gateway/send
GET    /api/v1/ott-gateway/status
GET    /api/v1/override/dummy
POST   /api/v1/override/dummy/approve
GET    /api/v1/override/history
GET    /api/v1/override/queue
POST   /api/v1/override/request
GET    /api/v1/payments/me
GET    /api/v1/payments/plans
GET    /api/v1/payments/subscription
GET    /api/v1/payments/subscriptions/me
GET    /api/v1/planning-subagent/sessions
GET    /api/v1/planning-subagent/status
GET    /api/v1/planning/sprints/901b185c-a99d-44f9-af4a-91ac8891e449/velocity
GET    /api/v1/planning/summary
GET    /api/v1/policy-packs
GET    /api/v1/policy-packs/categories
GET    /api/v1/preview
GET    /api/v1/preview/dummy
GET    /api/v1/preview/gates
GET    /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/activity
POST   /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/archive
GET    /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/dashboard
GET    /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/github-status
GET    /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/members
POST   /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/restore
GET    /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/sdlc-info
GET    /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/stats
GET    /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/tier-info
GET    /api/v1/projects/3ec1d475-c294-40e9-806f-0691dffa3fa8/usage
GET    /api/v1/push-notifications
POST   /api/v1/push-notifications/subscribe
GET    /api/v1/risk-analysis
POST   /api/v1/risk-analysis/analyze
GET    /api/v1/risk-analysis/items
GET    /api/v1/risk-analysis/overview
GET    /api/v1/risk-analysis/project/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/sdlc-structure
GET    /api/v1/sdlc-structure/report
GET    /api/v1/sdlc-structure/status
POST   /api/v1/sdlc-structure/validate
GET    /api/v1/sdlc-structure/validate
GET    /api/v1/skill-grants?project_id=3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/skills
GET    /api/v1/skills/grants?project_id=3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/stage-gating
GET    /api/v1/stage-gating/3ec1d475-c294-40e9-806f-0691dffa3fa8
GET    /api/v1/stage-gating/rules/STAGE_00
GET    /api/v1/telemetry
POST   /api/v1/telemetry/event
GET    /api/v1/templates
GET    /api/v1/templates/categories
GET    /api/v1/tier-management
GET    /api/v1/tier-management/current
GET    /api/v1/tier-management/limits
GET    /api/v1/tier-management/plans
GET    /api/v1/tier-management/usage
GET    /api/v1/triage/issues
GET    /api/v1/triage/summary
GET    /api/v1/usage/current
GET    /api/v1/usage/history
GET    /api/v1/vibecoding-index
GET    /api/v1/vibecoding-index/3ec1d475-c294-40e9-806f-0691dffa3fa8
POST   /api/v1/vibecoding-index/3ec1d475-c294-40e9-806f-0691dffa3fa8/calculate
GET    /api/v1/websocket/status
GET    /api/v1/workflows
GET    /metrics
GET    /ws/stats
```