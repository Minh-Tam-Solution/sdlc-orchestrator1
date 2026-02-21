# API Endpoints - Compact Table

**Total Endpoints**: 1260
**Format**: Compact table for quick reference

---

## 📋 Quick Index

- [AGENTS.md](#agents.md) (1260)

---

## AGENTS.md

| Method | Endpoint | Summary |
|--------|----------|----------|
| 🔵 GET | `/` | Root |
| 🔵 GET | `/api/v1/admin/ai-providers/config` | Get AI provider configuration |
| 🔵 GET | `/api/v1/admin/ai-providers/config` | Get AI provider configuration |
| 🟢 POST | `/api/v1/admin/ai-providers/ollama/refresh-models` | Refresh Ollama models |
| 🟢 POST | `/api/v1/admin/ai-providers/ollama/refresh-models` | Refresh Ollama models |
| 🟠 PATCH | `/api/v1/admin/ai-providers/{provider}` | Update provider settings |
| 🟠 PATCH | `/api/v1/admin/ai-providers/{provider}` | Update provider settings |
| 🔵 GET | `/api/v1/admin/ai-providers/{provider}/models` | Get available models for provider |
| 🔵 GET | `/api/v1/admin/ai-providers/{provider}/models` | Get available models for provider |
| 🟢 POST | `/api/v1/admin/ai-providers/{provider}/test` | Test provider connection |
| 🟢 POST | `/api/v1/admin/ai-providers/{provider}/test` | Test provider connection |
| 🔵 GET | `/api/v1/admin/audit-logs` | List audit logs (paginated) |
| 🟢 POST | `/api/v1/admin/evidence/retention-archive` | Trigger evidence archival (ADR-027) |
| 🟢 POST | `/api/v1/admin/evidence/retention-purge` | Trigger evidence purge (ADR-027) |
| 🔵 GET | `/api/v1/admin/evidence/retention-stats` | Get evidence retention statistics (ADR-027) |
| 🔵 GET | `/api/v1/admin/override-queue` | Get override approval queue |
| 🔵 GET | `/api/v1/admin/override-stats` | Get override statistics |
| 🔵 GET | `/api/v1/admin/settings` | Get all system settings |
| 🔵 GET | `/api/v1/admin/settings/{key}` | Get setting by key |
| 🟠 PATCH | `/api/v1/admin/settings/{key}` | Update setting |
| 🟢 POST | `/api/v1/admin/settings/{key}/rollback` | Rollback setting |
| 🔵 GET | `/api/v1/admin/stats` | Get admin dashboard statistics |
| 🔵 GET | `/api/v1/admin/system/health` | Get system health |
| 🔵 GET | `/api/v1/admin/users` | List all users (paginated) |
| 🟢 POST | `/api/v1/admin/users` | Create new user |
| 🔴 DELETE | `/api/v1/admin/users/bulk` | Bulk delete users (soft delete) |
| 🟢 POST | `/api/v1/admin/users/bulk` | Bulk user action |
| 🔴 DELETE | `/api/v1/admin/users/{user_id}` | Delete user (soft delete) |
| 🔵 GET | `/api/v1/admin/users/{user_id}` | Get user details |
| 🟠 PATCH | `/api/v1/admin/users/{user_id}` | Update user |
| 🟢 POST | `/api/v1/admin/users/{user_id}/mfa-exempt` | Set MFA exemption (ADR-027) |
| 🔵 GET | `/api/v1/admin/users/{user_id}/mfa-status` | Get user MFA status (ADR-027) |
| 🔴 DELETE | `/api/v1/admin/users/{user_id}/permanent` | Permanently delete user (Sprint 105) |
| 🟢 POST | `/api/v1/admin/users/{user_id}/restore` | Restore deleted user (Sprint 105) |
| 🟢 POST | `/api/v1/admin/users/{user_id}/unlock` | Unlock user account (ADR-027) |
| 🔵 GET | `/api/v1/agent-team/conversations` | List conversations |
| 🔵 GET | `/api/v1/agent-team/conversations` | List conversations |
| 🟢 POST | `/api/v1/agent-team/conversations` | Start conversation |
| 🟢 POST | `/api/v1/agent-team/conversations` | Start conversation |
| 🔵 GET | `/api/v1/agent-team/conversations/{conversation_id}` | Get conversation |
| 🔵 GET | `/api/v1/agent-team/conversations/{conversation_id}` | Get conversation |
| 🟢 POST | `/api/v1/agent-team/conversations/{conversation_id}/interrupt` | Interrupt conversation |
| 🟢 POST | `/api/v1/agent-team/conversations/{conversation_id}/interrupt` | Interrupt conversation |
| 🔵 GET | `/api/v1/agent-team/conversations/{conversation_id}/messages` | Get messages |
| 🔵 GET | `/api/v1/agent-team/conversations/{conversation_id}/messages` | Get messages |
| 🟢 POST | `/api/v1/agent-team/conversations/{conversation_id}/messages` | Send message |
| 🟢 POST | `/api/v1/agent-team/conversations/{conversation_id}/messages` | Send message |
| 🔵 GET | `/api/v1/agent-team/definitions` | List agent definitions |
| 🔵 GET | `/api/v1/agent-team/definitions` | List agent definitions |
| 🟢 POST | `/api/v1/agent-team/definitions` | Create agent definition |
| 🟢 POST | `/api/v1/agent-team/definitions` | Create agent definition |
| 🔵 GET | `/api/v1/agent-team/definitions/{definition_id}` | Get agent definition |
| 🔵 GET | `/api/v1/agent-team/definitions/{definition_id}` | Get agent definition |
| 🟡 PUT | `/api/v1/agent-team/definitions/{definition_id}` | Update agent definition |
| 🟡 PUT | `/api/v1/agent-team/definitions/{definition_id}` | Update agent definition |
| 🔵 GET | `/api/v1/agents-md/context/{project_id}` | Get context overlay |
| 🔵 GET | `/api/v1/agents-md/context/{project_id}` | Get context overlay |
| 🔵 GET | `/api/v1/agents-md/context/{project_id}` | Get context overlay |
| 🔵 GET | `/api/v1/agents-md/context/{project_id}/history` | Get context overlay history |
| 🔵 GET | `/api/v1/agents-md/context/{project_id}/history` | Get context overlay history |
| 🔵 GET | `/api/v1/agents-md/context/{project_id}/history` | Get context overlay history |
| 🟢 POST | `/api/v1/agents-md/generate` | Generate AGENTS.md |
| 🟢 POST | `/api/v1/agents-md/generate` | Generate AGENTS.md |
| 🟢 POST | `/api/v1/agents-md/lint` | Lint AGENTS.md |
| 🟢 POST | `/api/v1/agents-md/lint` | Lint AGENTS.md |
| 🔵 GET | `/api/v1/agents-md/repos` | List all repositories with AGENTS.md status |
| 🔵 GET | `/api/v1/agents-md/repos` | List all repositories with AGENTS.md status |
| 🟢 POST | `/api/v1/agents-md/validate` | Validate AGENTS.md |
| 🟢 POST | `/api/v1/agents-md/validate` | Validate AGENTS.md |
| 🔵 GET | `/api/v1/agents-md/{project_id}` | Get latest AGENTS.md |
| 🔵 GET | `/api/v1/agents-md/{project_id}` | Get latest AGENTS.md |
| 🔵 GET | `/api/v1/agents-md/{project_id}/history` | Get AGENTS.md history |
| 🔵 GET | `/api/v1/agents-md/{project_id}/history` | Get AGENTS.md history |
| 🟢 POST | `/api/v1/ai-detection/analyze` | Analyze Pr |
| 🟢 POST | `/api/v1/ai-detection/analyze` | Analyze Pr |
| 🔵 GET | `/api/v1/ai-detection/circuit-breakers` | Get Circuit Breakers |
| 🔵 GET | `/api/v1/ai-detection/circuit-breakers` | Get Circuit Breakers |
| 🟢 POST | `/api/v1/ai-detection/circuit-breakers/{breaker_name}/reset` | Reset Circuit Breaker |
| 🟢 POST | `/api/v1/ai-detection/circuit-breakers/{breaker_name}/reset` | Reset Circuit Breaker |
| 🔵 GET | `/api/v1/ai-detection/shadow-mode` | Get Shadow Mode |
| 🔵 GET | `/api/v1/ai-detection/shadow-mode` | Get Shadow Mode |
| 🔵 GET | `/api/v1/ai-detection/status` | Get Detection Status |
| 🔵 GET | `/api/v1/ai-detection/status` | Get Detection Status |
| 🔵 GET | `/api/v1/ai-detection/tools` | Get Supported Tools |
| 🔵 GET | `/api/v1/ai-detection/tools` | Get Supported Tools |
| 🔵 GET | `/api/v1/analytics/circuit-breaker/status` | Get Circuit Breaker Status |
| 🔵 GET | `/api/v1/analytics/circuit-breaker/status` | Get Circuit Breaker Status |
| 🔵 GET | `/api/v1/analytics/engagement` | Get Engagement Summary |
| 🔵 GET | `/api/v1/analytics/engagement` | Get Engagement Summary |
| 🟢 POST | `/api/v1/analytics/events` | Track Event |
| 🟢 POST | `/api/v1/analytics/events` | Track Event |
| 🟢 POST | `/api/v1/analytics/events/feature` | Track Feature Use |
| 🟢 POST | `/api/v1/analytics/events/feature` | Track Feature Use |
| 🟢 POST | `/api/v1/analytics/events/page-view` | Track Page View |
| 🟢 POST | `/api/v1/analytics/events/page-view` | Track Page View |
| 🔵 GET | `/api/v1/analytics/features` | Get Feature Usage |
| 🔵 GET | `/api/v1/analytics/features` | Get Feature Usage |
| 🔵 GET | `/api/v1/analytics/my-activity` | Get My Activity |
| 🔵 GET | `/api/v1/analytics/my-activity` | Get My Activity |
| 🔵 GET | `/api/v1/analytics/pilot-metrics` | Get Pilot Metrics |
| 🔵 GET | `/api/v1/analytics/pilot-metrics` | Get Pilot Metrics |
| 🟢 POST | `/api/v1/analytics/pilot-metrics/calculate` | Calculate Today Metrics |
| 🟢 POST | `/api/v1/analytics/pilot-metrics/calculate` | Calculate Today Metrics |
| 🟢 POST | `/api/v1/analytics/retention/cleanup` | Run Retention Cleanup |
| 🟢 POST | `/api/v1/analytics/retention/cleanup` | Run Retention Cleanup |
| 🔵 GET | `/api/v1/analytics/retention/stats` | Get Retention Stats |
| 🔵 GET | `/api/v1/analytics/retention/stats` | Get Retention Stats |
| 🔵 GET | `/api/v1/analytics/sessions/active` | Get Active Session |
| 🔵 GET | `/api/v1/analytics/sessions/active` | Get Active Session |
| 🟢 POST | `/api/v1/analytics/sessions/start` | Start Session |
| 🟢 POST | `/api/v1/analytics/sessions/start` | Start Session |
| 🟢 POST | `/api/v1/analytics/sessions/{session_id}/end` | End Session |
| 🟢 POST | `/api/v1/analytics/sessions/{session_id}/end` | End Session |
| 🔵 GET | `/api/v1/analytics/summary` | Get Analytics Summary |
| 🔵 GET | `/api/v1/analytics/summary` | Get Analytics Summary |
| 🟢 POST | `/api/v1/analytics/v2/events` | Track Event |
| 🟢 POST | `/api/v1/analytics/v2/events` | Track Event |
| 🟢 POST | `/api/v1/analytics/v2/events/batch` | Track Batch Events |
| 🟢 POST | `/api/v1/analytics/v2/events/batch` | Track Batch Events |
| 🔵 GET | `/api/v1/analytics/v2/metrics/ai-safety` | Get Ai Safety Metrics |
| 🔵 GET | `/api/v1/analytics/v2/metrics/ai-safety` | Get Ai Safety Metrics |
| 🔵 GET | `/api/v1/analytics/v2/metrics/dau` | Get Daily Active Users |
| 🔵 GET | `/api/v1/analytics/v2/metrics/dau` | Get Daily Active Users |
| 🔵 GET | `/api/v1/api-keys` | List Api Keys |
| 🔵 GET | `/api/v1/api-keys` | List Api Keys |
| 🟢 POST | `/api/v1/api-keys` | Create Api Key |
| 🟢 POST | `/api/v1/api-keys` | Create Api Key |
| 🔴 DELETE | `/api/v1/api-keys/{key_id}` | Revoke Api Key |
| 🔴 DELETE | `/api/v1/api-keys/{key_id}` | Revoke Api Key |
| 🔵 GET | `/api/v1/api/v1/github/installations` | List user's GitHub installations |
| 🔵 GET | `/api/v1/api/v1/github/installations` | List user's GitHub installations |
| 🔵 GET | `/api/v1/api/v1/github/installations/{installation_id}/repositories` | List repositories for installation |
| 🔵 GET | `/api/v1/api/v1/github/installations/{installation_id}/repositories` | List repositories for installation |
| 🟢 POST | `/api/v1/api/v1/github/projects/{project_id}/clone` | Clone linked repository |
| 🟢 POST | `/api/v1/api/v1/github/projects/{project_id}/clone` | Clone linked repository |
| 🟢 POST | `/api/v1/api/v1/github/projects/{project_id}/link` | Link GitHub repository to project |
| 🟢 POST | `/api/v1/api/v1/github/projects/{project_id}/link` | Link GitHub repository to project |
| 🔵 GET | `/api/v1/api/v1/github/projects/{project_id}/repository` | Get linked repository for project |
| 🔵 GET | `/api/v1/api/v1/github/projects/{project_id}/repository` | Get linked repository for project |
| 🔵 GET | `/api/v1/api/v1/github/projects/{project_id}/scan` | Scan cloned repository |
| 🔵 GET | `/api/v1/api/v1/github/projects/{project_id}/scan` | Scan cloned repository |
| 🔴 DELETE | `/api/v1/api/v1/github/projects/{project_id}/unlink` | Unlink GitHub repository from project |
| 🔴 DELETE | `/api/v1/api/v1/github/projects/{project_id}/unlink` | Unlink GitHub repository from project |
| 🟢 POST | `/api/v1/api/v1/github/webhooks` | GitHub webhook handler |
| 🟢 POST | `/api/v1/api/v1/github/webhooks` | GitHub webhook handler |
| 🔵 GET | `/api/v1/api/v1/github/webhooks/dlq` | Get dead letter queue jobs |
| 🔵 GET | `/api/v1/api/v1/github/webhooks/dlq` | Get dead letter queue jobs |
| 🟢 POST | `/api/v1/api/v1/github/webhooks/dlq/{job_id}/retry` | Retry a dead letter queue job |
| 🟢 POST | `/api/v1/api/v1/github/webhooks/dlq/{job_id}/retry` | Retry a dead letter queue job |
| 🔵 GET | `/api/v1/api/v1/github/webhooks/jobs/{job_id}` | Get webhook job status |
| 🔵 GET | `/api/v1/api/v1/github/webhooks/jobs/{job_id}` | Get webhook job status |
| 🟢 POST | `/api/v1/api/v1/github/webhooks/process` | Trigger webhook job processing |
| 🟢 POST | `/api/v1/api/v1/github/webhooks/process` | Trigger webhook job processing |
| 🔵 GET | `/api/v1/api/v1/github/webhooks/stats` | Get webhook job queue statistics |
| 🔵 GET | `/api/v1/api/v1/github/webhooks/stats` | Get webhook job queue statistics |
| 🔴 DELETE | `/api/v1/api/v1/org-invitations/{invitation_id}` | Cancel organization invitation |
| 🔴 DELETE | `/api/v1/api/v1/org-invitations/{invitation_id}` | Cancel organization invitation |
| 🟢 POST | `/api/v1/api/v1/org-invitations/{invitation_id}/resend` | Resend organization invitation email |
| 🟢 POST | `/api/v1/api/v1/org-invitations/{invitation_id}/resend` | Resend organization invitation email |
| 🔵 GET | `/api/v1/api/v1/org-invitations/{token}` | Get organization invitation details by token |
| 🔵 GET | `/api/v1/api/v1/org-invitations/{token}` | Get organization invitation details by token |
| 🟢 POST | `/api/v1/api/v1/org-invitations/{token}/accept` | Accept organization invitation |
| 🟢 POST | `/api/v1/api/v1/org-invitations/{token}/accept` | Accept organization invitation |
| 🟢 POST | `/api/v1/api/v1/org-invitations/{token}/decline` | Decline organization invitation |
| 🟢 POST | `/api/v1/api/v1/org-invitations/{token}/decline` | Decline organization invitation |
| 🔵 GET | `/api/v1/api/v1/organizations/{organization_id}/invitations` | List organization invitations |
| 🔵 GET | `/api/v1/api/v1/organizations/{organization_id}/invitations` | List organization invitations |
| 🟢 POST | `/api/v1/api/v1/organizations/{organization_id}/invitations` | Send organization invitation |
| 🟢 POST | `/api/v1/api/v1/organizations/{organization_id}/invitations` | Send organization invitation |
| 🟢 POST | `/api/v1/auth/forgot-password` | Forgot Password |
| 🟢 POST | `/api/v1/auth/forgot-password` | Forgot Password |
| 🟢 POST | `/api/v1/auth/github/device` | Github Device Flow Init |
| 🟢 POST | `/api/v1/auth/github/device` | Github Device Flow Init |
| 🟢 POST | `/api/v1/auth/github/token` | Github Device Flow Poll |
| 🟢 POST | `/api/v1/auth/github/token` | Github Device Flow Poll |
| 🔵 GET | `/api/v1/auth/health` | Auth Health Check |
| 🔵 GET | `/api/v1/auth/health` | Auth Health Check |
| 🟢 POST | `/api/v1/auth/login` | Login |
| 🟢 POST | `/api/v1/auth/login` | Login |
| 🟢 POST | `/api/v1/auth/logout` | Logout |
| 🟢 POST | `/api/v1/auth/logout` | Logout |
| 🔵 GET | `/api/v1/auth/me` | Get Current User Profile |
| 🔵 GET | `/api/v1/auth/me` | Get Current User Profile |
| 🔵 GET | `/api/v1/auth/oauth/{provider}/authorize` | Oauth Authorize |
| 🔵 GET | `/api/v1/auth/oauth/{provider}/authorize` | Oauth Authorize |
| 🟢 POST | `/api/v1/auth/oauth/{provider}/callback` | Oauth Callback |
| 🟢 POST | `/api/v1/auth/oauth/{provider}/callback` | Oauth Callback |
| 🟢 POST | `/api/v1/auth/refresh` | Refresh Access Token |
| 🟢 POST | `/api/v1/auth/refresh` | Refresh Access Token |
| 🟢 POST | `/api/v1/auth/register` | Register |
| 🟢 POST | `/api/v1/auth/register` | Register |
| 🟢 POST | `/api/v1/auth/reset-password` | Reset Password |
| 🟢 POST | `/api/v1/auth/reset-password` | Reset Password |
| 🔵 GET | `/api/v1/auth/verify-reset-token` | Verify Reset Token |
| 🔵 GET | `/api/v1/auth/verify-reset-token` | Verify Reset Token |
| 🟢 POST | `/api/v1/auto-generate/all` | Generate All Compliance Artifacts |
| 🟢 POST | `/api/v1/auto-generate/all` | Generate All Compliance Artifacts |
| 🟢 POST | `/api/v1/auto-generate/attestation` | Generate AI Attestation |
| 🟢 POST | `/api/v1/auto-generate/attestation` | Generate AI Attestation |
| 🟢 POST | `/api/v1/auto-generate/context` | Attach Context to PR |
| 🟢 POST | `/api/v1/auto-generate/context` | Attach Context to PR |
| 🔵 GET | `/api/v1/auto-generate/health` | Auto-Generation Health Check |
| 🔵 GET | `/api/v1/auto-generate/health` | Auto-Generation Health Check |
| 🟢 POST | `/api/v1/auto-generate/intent` | Generate Intent Document |
| 🟢 POST | `/api/v1/auto-generate/intent` | Generate Intent Document |
| 🟢 POST | `/api/v1/auto-generate/ownership` | Suggest File Ownership |
| 🟢 POST | `/api/v1/auto-generate/ownership` | Suggest File Ownership |
| 🟢 POST | `/api/v1/ceo-dashboard/decisions/{submission_id}/override` | Record CEO override for calibration |
| 🟢 POST | `/api/v1/ceo-dashboard/decisions/{submission_id}/resolve` | Resolve pending CEO decision |
| 🔵 GET | `/api/v1/ceo-dashboard/health` | CEO Dashboard health check |
| 🔵 GET | `/api/v1/ceo-dashboard/overrides` | Get CEO overrides this week |
| 🔵 GET | `/api/v1/ceo-dashboard/pending-decisions` | Get pending CEO decisions queue |
| 🔵 GET | `/api/v1/ceo-dashboard/routing-breakdown` | Get PR routing breakdown |
| 🟢 POST | `/api/v1/ceo-dashboard/submissions` | Record governance submission |
| 🔵 GET | `/api/v1/ceo-dashboard/summary` | Get complete CEO dashboard summary |
| 🔵 GET | `/api/v1/ceo-dashboard/system-health` | Get system health snapshot |
| 🔵 GET | `/api/v1/ceo-dashboard/time-saved` | Get CEO time saved metrics |
| 🔵 GET | `/api/v1/ceo-dashboard/top-rejections` | Get top rejection reasons |
| 🔵 GET | `/api/v1/ceo-dashboard/trends/time-saved` | Get time saved trend (8 weeks) |
| 🔵 GET | `/api/v1/ceo-dashboard/trends/vibecoding-index` | Get vibecoding index trend (7 days) |
| 🔵 GET | `/api/v1/ceo-dashboard/weekly-summary` | Get weekly governance summary |
| 🔵 GET | `/api/v1/check-runs` | List Check Runs |
| 🔵 GET | `/api/v1/check-runs/health/status` | Health Check |
| 🔵 GET | `/api/v1/check-runs/stats` | Get Check Run Stats |
| 🔵 GET | `/api/v1/check-runs/{check_run_id}` | Get Check Run |
| 🟢 POST | `/api/v1/check-runs/{check_run_id}/rerun` | Rerun Check Run |
| 🟢 POST | `/api/v1/codegen/estimate` | Estimate Cost |
| 🟢 POST | `/api/v1/codegen/estimate` | Estimate Cost |
| 🟢 POST | `/api/v1/codegen/generate` | Generate Code |
| 🟢 POST | `/api/v1/codegen/generate` | Generate Code |
| 🟢 POST | `/api/v1/codegen/generate/full` | Generate With Quality |
| 🟢 POST | `/api/v1/codegen/generate/full` | Generate With Quality |
| 🟢 POST | `/api/v1/codegen/generate/resume/{session_id}` | Resume Generation |
| 🟢 POST | `/api/v1/codegen/generate/resume/{session_id}` | Resume Generation |
| 🟢 POST | `/api/v1/codegen/generate/stream` | Generate Stream |
| 🟢 POST | `/api/v1/codegen/generate/stream` | Generate Stream |
| 🟢 POST | `/api/v1/codegen/generate/zip` | Generate Zip |
| 🟢 POST | `/api/v1/codegen/generate/zip` | Generate Zip |
| 🔵 GET | `/api/v1/codegen/health` | Health Check |
| 🔵 GET | `/api/v1/codegen/health` | Health Check |
| 🟢 POST | `/api/v1/codegen/ir/generate` | Ir Generate |
| 🟢 POST | `/api/v1/codegen/ir/generate` | Ir Generate |
| 🟢 POST | `/api/v1/codegen/ir/validate` | Ir Validate |
| 🟢 POST | `/api/v1/codegen/ir/validate` | Ir Validate |
| 🔵 GET | `/api/v1/codegen/onboarding/options/domains` | Get Domain Options |
| 🔵 GET | `/api/v1/codegen/onboarding/options/domains` | Get Domain Options |
| 🔵 GET | `/api/v1/codegen/onboarding/options/features/{domain}` | Get Feature Options |
| 🔵 GET | `/api/v1/codegen/onboarding/options/features/{domain}` | Get Feature Options |
| 🔵 GET | `/api/v1/codegen/onboarding/options/scales` | Get Scale Options |
| 🔵 GET | `/api/v1/codegen/onboarding/options/scales` | Get Scale Options |
| 🟢 POST | `/api/v1/codegen/onboarding/start` | Start Onboarding |
| 🟢 POST | `/api/v1/codegen/onboarding/start` | Start Onboarding |
| 🔵 GET | `/api/v1/codegen/onboarding/{session_id}` | Get Onboarding Session |
| 🔵 GET | `/api/v1/codegen/onboarding/{session_id}` | Get Onboarding Session |
| 🟢 POST | `/api/v1/codegen/onboarding/{session_id}/app_name` | Set Onboarding App Name |
| 🟢 POST | `/api/v1/codegen/onboarding/{session_id}/app_name` | Set Onboarding App Name |
| 🟢 POST | `/api/v1/codegen/onboarding/{session_id}/domain` | Set Onboarding Domain |
| 🟢 POST | `/api/v1/codegen/onboarding/{session_id}/domain` | Set Onboarding Domain |
| 🟢 POST | `/api/v1/codegen/onboarding/{session_id}/features` | Set Onboarding Features |
| 🟢 POST | `/api/v1/codegen/onboarding/{session_id}/features` | Set Onboarding Features |
| 🟢 POST | `/api/v1/codegen/onboarding/{session_id}/generate` | Generate Onboarding Blueprint |
| 🟢 POST | `/api/v1/codegen/onboarding/{session_id}/generate` | Generate Onboarding Blueprint |
| 🟢 POST | `/api/v1/codegen/onboarding/{session_id}/scale` | Set Onboarding Scale |
| 🟢 POST | `/api/v1/codegen/onboarding/{session_id}/scale` | Set Onboarding Scale |
| 🔴 DELETE | `/api/v1/codegen/preview/{token}` | Delete Preview |
| 🔴 DELETE | `/api/v1/codegen/preview/{token}` | Delete Preview |
| 🔵 GET | `/api/v1/codegen/preview/{token}` | Get Preview |
| 🔵 GET | `/api/v1/codegen/preview/{token}` | Get Preview |
| 🔵 GET | `/api/v1/codegen/providers` | List Providers |
| 🔵 GET | `/api/v1/codegen/providers` | List Providers |
| 🔵 GET | `/api/v1/codegen/sessions` | List Sessions |
| 🔵 GET | `/api/v1/codegen/sessions` | List Sessions |
| 🔵 GET | `/api/v1/codegen/sessions/active` | List Active Sessions |
| 🔵 GET | `/api/v1/codegen/sessions/active` | List Active Sessions |
| 🔵 GET | `/api/v1/codegen/sessions/{session_id}` | Get Session Status |
| 🔵 GET | `/api/v1/codegen/sessions/{session_id}` | Get Session Status |
| 🟢 POST | `/api/v1/codegen/sessions/{session_id}/preview` | Create Preview |
| 🟢 POST | `/api/v1/codegen/sessions/{session_id}/preview` | Create Preview |
| 🔵 GET | `/api/v1/codegen/sessions/{session_id}/quality/stream` | Stream Quality Pipeline |
| 🔵 GET | `/api/v1/codegen/sessions/{session_id}/quality/stream` | Stream Quality Pipeline |
| 🔵 GET | `/api/v1/codegen/templates` | List Templates |
| 🔵 GET | `/api/v1/codegen/templates` | List Templates |
| 🔵 GET | `/api/v1/codegen/usage/monthly` | Get Monthly Cost |
| 🔵 GET | `/api/v1/codegen/usage/monthly` | Get Monthly Cost |
| 🔵 GET | `/api/v1/codegen/usage/provider-health/{provider}` | Get Provider Health History |
| 🔵 GET | `/api/v1/codegen/usage/provider-health/{provider}` | Get Provider Health History |
| 🔵 GET | `/api/v1/codegen/usage/report` | Get Cost Report |
| 🔵 GET | `/api/v1/codegen/usage/report` | Get Cost Report |
| 🟢 POST | `/api/v1/codegen/validate` | Validate Code |
| 🟢 POST | `/api/v1/codegen/validate` | Validate Code |
| 🔵 GET | `/api/v1/compliance/ai/budget` | Get AI budget status |
| 🔵 GET | `/api/v1/compliance/ai/budget` | Get AI budget status |
| 🔵 GET | `/api/v1/compliance/ai/models` | List available Ollama models |
| 🔵 GET | `/api/v1/compliance/ai/models` | List available Ollama models |
| 🔵 GET | `/api/v1/compliance/ai/providers` | Get AI providers status |
| 🔵 GET | `/api/v1/compliance/ai/providers` | Get AI providers status |
| 🟢 POST | `/api/v1/compliance/ai/recommendations` | Generate AI recommendation |
| 🟢 POST | `/api/v1/compliance/ai/recommendations` | Generate AI recommendation |
| 🔵 GET | `/api/v1/compliance/jobs/{job_id}` | Get scan job status |
| 🔵 GET | `/api/v1/compliance/jobs/{job_id}` | Get scan job status |
| 🔵 GET | `/api/v1/compliance/queue/status` | Get scan queue status |
| 🔵 GET | `/api/v1/compliance/queue/status` | Get scan queue status |
| 🟢 POST | `/api/v1/compliance/scans/{project_id}` | Trigger compliance scan |
| 🟢 POST | `/api/v1/compliance/scans/{project_id}` | Trigger compliance scan |
| 🔵 GET | `/api/v1/compliance/scans/{project_id}/history` | Get scan history |
| 🔵 GET | `/api/v1/compliance/scans/{project_id}/history` | Get scan history |
| 🔵 GET | `/api/v1/compliance/scans/{project_id}/latest` | Get latest scan result |
| 🔵 GET | `/api/v1/compliance/scans/{project_id}/latest` | Get latest scan result |
| 🟢 POST | `/api/v1/compliance/scans/{project_id}/schedule` | Schedule compliance scan |
| 🟢 POST | `/api/v1/compliance/scans/{project_id}/schedule` | Schedule compliance scan |
| 🔵 GET | `/api/v1/compliance/violations/{project_id}` | Get project violations |
| 🔵 GET | `/api/v1/compliance/violations/{project_id}` | Get project violations |
| 🟢 POST | `/api/v1/compliance/violations/{violation_id}/ai-recommendation` | Generate recommendation for violation |
| 🟢 POST | `/api/v1/compliance/violations/{violation_id}/ai-recommendation` | Generate recommendation for violation |
| 🟡 PUT | `/api/v1/compliance/violations/{violation_id}/resolve` | Resolve violation |
| 🟡 PUT | `/api/v1/compliance/violations/{violation_id}/resolve` | Resolve violation |
| 🔵 GET | `/api/v1/consultations` | List consultations |
| 🔵 GET | `/api/v1/consultations` | List consultations |
| 🟢 POST | `/api/v1/consultations` | Create consultation request |
| 🟢 POST | `/api/v1/consultations` | Create consultation request |
| 🟢 POST | `/api/v1/consultations/auto-generate` | AI-assisted CRP generation |
| 🟢 POST | `/api/v1/consultations/auto-generate` | AI-assisted CRP generation |
| 🔵 GET | `/api/v1/consultations/my-reviews` | Get my pending reviews |
| 🔵 GET | `/api/v1/consultations/my-reviews` | Get my pending reviews |
| 🔵 GET | `/api/v1/consultations/{consultation_id}` | Get consultation |
| 🔵 GET | `/api/v1/consultations/{consultation_id}` | Get consultation |
| 🟢 POST | `/api/v1/consultations/{consultation_id}/assign` | Assign reviewer |
| 🟢 POST | `/api/v1/consultations/{consultation_id}/assign` | Assign reviewer |
| 🟢 POST | `/api/v1/consultations/{consultation_id}/comments` | Add comment |
| 🟢 POST | `/api/v1/consultations/{consultation_id}/comments` | Add comment |
| 🟢 POST | `/api/v1/consultations/{consultation_id}/resolve` | Resolve consultation |
| 🟢 POST | `/api/v1/consultations/{consultation_id}/resolve` | Resolve consultation |
| 🔵 GET | `/api/v1/context-authority/adrs` | [DEPRECATED] List all ADRs |
| 🔵 GET | `/api/v1/context-authority/adrs` | [DEPRECATED] List all ADRs |
| 🔵 GET | `/api/v1/context-authority/adrs/{adr_id}` | [DEPRECATED] Get specific ADR |
| 🔵 GET | `/api/v1/context-authority/adrs/{adr_id}` | [DEPRECATED] Get specific ADR |
| 🔵 GET | `/api/v1/context-authority/agents-md` | [DEPRECATED] Get AGENTS.md status |
| 🔵 GET | `/api/v1/context-authority/agents-md` | [DEPRECATED] Get AGENTS.md status |
| 🟢 POST | `/api/v1/context-authority/check-adr-linkage` | [DEPRECATED] Check ADR linkage for modules |
| 🟢 POST | `/api/v1/context-authority/check-adr-linkage` | [DEPRECATED] Check ADR linkage for modules |
| 🟢 POST | `/api/v1/context-authority/check-spec` | [DEPRECATED] Check design spec existence |
| 🟢 POST | `/api/v1/context-authority/check-spec` | [DEPRECATED] Check design spec existence |
| 🔵 GET | `/api/v1/context-authority/health` | [DEPRECATED] Context authority health check |
| 🔵 GET | `/api/v1/context-authority/health` | [DEPRECATED] Context authority health check |
| 🔵 GET | `/api/v1/context-authority/v2/health` | Health check |
| 🔵 GET | `/api/v1/context-authority/v2/health` | Health check |
| 🟢 POST | `/api/v1/context-authority/v2/overlay` | Generate dynamic overlay |
| 🟢 POST | `/api/v1/context-authority/v2/overlay` | Generate dynamic overlay |
| 🔵 GET | `/api/v1/context-authority/v2/snapshot/{submission_id}` | Get context snapshot |
| 🔵 GET | `/api/v1/context-authority/v2/snapshot/{submission_id}` | Get context snapshot |
| 🔵 GET | `/api/v1/context-authority/v2/snapshots/{project_id}` | List project snapshots |
| 🔵 GET | `/api/v1/context-authority/v2/snapshots/{project_id}` | List project snapshots |
| 🔵 GET | `/api/v1/context-authority/v2/stats` | Get statistics |
| 🔵 GET | `/api/v1/context-authority/v2/stats` | Get statistics |
| 🔵 GET | `/api/v1/context-authority/v2/templates` | List overlay templates |
| 🔵 GET | `/api/v1/context-authority/v2/templates` | List overlay templates |
| 🟢 POST | `/api/v1/context-authority/v2/templates` | Create overlay template |
| 🟢 POST | `/api/v1/context-authority/v2/templates` | Create overlay template |
| 🔵 GET | `/api/v1/context-authority/v2/templates/{template_id}` | Get template by ID |
| 🔵 GET | `/api/v1/context-authority/v2/templates/{template_id}` | Get template by ID |
| 🟡 PUT | `/api/v1/context-authority/v2/templates/{template_id}` | Update template |
| 🟡 PUT | `/api/v1/context-authority/v2/templates/{template_id}` | Update template |
| 🔵 GET | `/api/v1/context-authority/v2/templates/{template_id}/usage` | Get template usage statistics |
| 🔵 GET | `/api/v1/context-authority/v2/templates/{template_id}/usage` | Get template usage statistics |
| 🟢 POST | `/api/v1/context-authority/v2/validate` | Gate-aware context validation |
| 🟢 POST | `/api/v1/context-authority/v2/validate` | Gate-aware context validation |
| 🟢 POST | `/api/v1/context-authority/validate` | [DEPRECATED] Validate code context linkage |
| 🟢 POST | `/api/v1/context-authority/validate` | [DEPRECATED] Validate code context linkage |
| 🔵 GET | `/api/v1/context-validation/health` | Health check |
| 🔵 GET | `/api/v1/context-validation/health` | Health check |
| 🔵 GET | `/api/v1/context-validation/limits` | Get context limits configuration |
| 🔵 GET | `/api/v1/context-validation/limits` | Get context limits configuration |
| 🟢 POST | `/api/v1/context-validation/validate` | Validate AGENTS.md context limits |
| 🟢 POST | `/api/v1/context-validation/validate` | Validate AGENTS.md context limits |
| 🟢 POST | `/api/v1/context-validation/validate-github` | Validate AGENTS.md from GitHub repository |
| 🟢 POST | `/api/v1/context-validation/validate-github` | Validate AGENTS.md from GitHub repository |
| 🟢 POST | `/api/v1/council/decide` | Request council decision with sprint context |
| 🟢 POST | `/api/v1/council/decide` | Request council decision with sprint context |
| 🟢 POST | `/api/v1/council/deliberate` | Trigger AI Council deliberation |
| 🟢 POST | `/api/v1/council/deliberate` | Trigger AI Council deliberation |
| 🔵 GET | `/api/v1/council/history/{project_id}` | Get project council history |
| 🔵 GET | `/api/v1/council/history/{project_id}` | Get project council history |
| 🔵 GET | `/api/v1/council/stats/{project_id}` | Get project council statistics |
| 🔵 GET | `/api/v1/council/stats/{project_id}` | Get project council statistics |
| 🔵 GET | `/api/v1/council/status/{request_id}` | Get deliberation status |
| 🔵 GET | `/api/v1/council/status/{request_id}` | Get deliberation status |
| 🔵 GET | `/api/v1/cross-reference/coverage/{project_id}` | Get Coverage |
| 🔵 GET | `/api/v1/cross-reference/coverage/{project_id}` | Get Coverage |
| 🔵 GET | `/api/v1/cross-reference/missing-tests/{project_id}` | Get Missing Tests |
| 🔵 GET | `/api/v1/cross-reference/missing-tests/{project_id}` | Get Missing Tests |
| 🔵 GET | `/api/v1/cross-reference/ssot-check/{project_id}` | Check Ssot Compliance |
| 🔵 GET | `/api/v1/cross-reference/ssot-check/{project_id}` | Check Ssot Compliance |
| 🟢 POST | `/api/v1/cross-reference/validate` | Validate Cross Reference |
| 🟢 POST | `/api/v1/cross-reference/validate` | Validate Cross Reference |
| 🔵 GET | `/api/v1/dashboard/recent-gates` | Get Recent Gates |
| 🔵 GET | `/api/v1/dashboard/recent-gates` | Get Recent Gates |
| 🔵 GET | `/api/v1/dashboard/stats` | Get Dashboard Stats |
| 🔵 GET | `/api/v1/dashboard/stats` | Get Dashboard Stats |
| 🔵 GET | `/api/v1/deprecation/dashboard` | Get Deprecation Dashboard |
| 🔵 GET | `/api/v1/deprecation/dashboard` | Get Deprecation Dashboard |
| 🔵 GET | `/api/v1/deprecation/endpoints` | Get Deprecated Endpoints |
| 🔵 GET | `/api/v1/deprecation/endpoints` | Get Deprecated Endpoints |
| 🔵 GET | `/api/v1/deprecation/summary` | Get Deprecation Summary |
| 🔵 GET | `/api/v1/deprecation/summary` | Get Deprecation Summary |
| 🔵 GET | `/api/v1/deprecation/timeline` | Get Deprecation Timeline |
| 🔵 GET | `/api/v1/deprecation/timeline` | Get Deprecation Timeline |
| 🔵 GET | `/api/v1/doc-cross-reference/links` | Get document links |
| 🔵 GET | `/api/v1/doc-cross-reference/links` | Get document links |
| 🔵 GET | `/api/v1/doc-cross-reference/orphaned` | Get orphaned documents |
| 🔵 GET | `/api/v1/doc-cross-reference/orphaned` | Get orphaned documents |
| 🟢 POST | `/api/v1/doc-cross-reference/validate` | Validate single document |
| 🟢 POST | `/api/v1/doc-cross-reference/validate` | Validate single document |
| 🟢 POST | `/api/v1/doc-cross-reference/validate-project` | Validate entire project |
| 🟢 POST | `/api/v1/doc-cross-reference/validate-project` | Validate entire project |
| 🔵 GET | `/api/v1/docs/user-support` | List User Support Docs |
| 🔵 GET | `/api/v1/docs/user-support` | List User Support Docs |
| 🔵 GET | `/api/v1/docs/user-support/{filename}` | Get User Support Doc |
| 🔵 GET | `/api/v1/docs/user-support/{filename}` | Get User Support Doc |
| 🔵 GET | `/api/v1/dogfooding/ceo-time/entries` | List Ceo Time Entries |
| 🔵 GET | `/api/v1/dogfooding/ceo-time/entries` | List Ceo Time Entries |
| 🟢 POST | `/api/v1/dogfooding/ceo-time/record` | Record Ceo Time |
| 🟢 POST | `/api/v1/dogfooding/ceo-time/record` | Record Ceo Time |
| 🔵 GET | `/api/v1/dogfooding/ceo-time/summary` | Get Ceo Time Summary |
| 🔵 GET | `/api/v1/dogfooding/ceo-time/summary` | Get Ceo Time Summary |
| 🔵 GET | `/api/v1/dogfooding/daily-checks` | Run Daily Checks |
| 🔵 GET | `/api/v1/dogfooding/daily-checks` | Run Daily Checks |
| 🔵 GET | `/api/v1/dogfooding/daily-checks/history` | Get Daily Checks History |
| 🔵 GET | `/api/v1/dogfooding/daily-checks/history` | Get Daily Checks History |
| 🟢 POST | `/api/v1/dogfooding/enforce/soft` | Enforce Soft Mode |
| 🟢 POST | `/api/v1/dogfooding/enforce/soft` | Enforce Soft Mode |
| 🔵 GET | `/api/v1/dogfooding/enforce/soft/log` | Get Soft Enforcement Log |
| 🔵 GET | `/api/v1/dogfooding/enforce/soft/log` | Get Soft Enforcement Log |
| 🟢 POST | `/api/v1/dogfooding/enforce/soft/override` | Request Cto Override |
| 🟢 POST | `/api/v1/dogfooding/enforce/soft/override` | Request Cto Override |
| 🔵 GET | `/api/v1/dogfooding/enforce/soft/status` | Get Soft Mode Status |
| 🔵 GET | `/api/v1/dogfooding/enforce/soft/status` | Get Soft Mode Status |
| 🔵 GET | `/api/v1/dogfooding/export/json` | Export Json Metrics |
| 🔵 GET | `/api/v1/dogfooding/export/json` | Export Json Metrics |
| 🔵 GET | `/api/v1/dogfooding/export/prometheus` | Export Prometheus Metrics |
| 🔵 GET | `/api/v1/dogfooding/export/prometheus` | Export Prometheus Metrics |
| 🟢 POST | `/api/v1/dogfooding/feedback` | Submit Developer Feedback |
| 🟢 POST | `/api/v1/dogfooding/feedback` | Submit Developer Feedback |
| 🔵 GET | `/api/v1/dogfooding/feedback/list` | List Developer Feedback |
| 🔵 GET | `/api/v1/dogfooding/feedback/list` | List Developer Feedback |
| 🔵 GET | `/api/v1/dogfooding/feedback/summary` | Get Feedback Summary |
| 🔵 GET | `/api/v1/dogfooding/feedback/summary` | Get Feedback Summary |
| 🔵 GET | `/api/v1/dogfooding/go-no-go` | Get Go No Go Decision |
| 🔵 GET | `/api/v1/dogfooding/go-no-go` | Get Go No Go Decision |
| 🔵 GET | `/api/v1/dogfooding/metrics` | Get Dogfooding Metrics |
| 🔵 GET | `/api/v1/dogfooding/metrics` | Get Dogfooding Metrics |
| 🔵 GET | `/api/v1/dogfooding/prs` | Get Pr Metrics |
| 🔵 GET | `/api/v1/dogfooding/prs` | Get Pr Metrics |
| 🟢 POST | `/api/v1/dogfooding/prs/record` | Record Pr Metric |
| 🟢 POST | `/api/v1/dogfooding/prs/record` | Record Pr Metric |
| 🟢 POST | `/api/v1/dogfooding/report-false-positive` | Report False Positive |
| 🟢 POST | `/api/v1/dogfooding/report-false-positive` | Report False Positive |
| 🔵 GET | `/api/v1/dogfooding/status` | Get Dogfooding Status |
| 🔵 GET | `/api/v1/dogfooding/status` | Get Dogfooding Status |
| 🟢 POST | `/api/v1/e2e/cancel/{execution_id}` | Cancel Execution |
| 🟢 POST | `/api/v1/e2e/cancel/{execution_id}` | Cancel Execution |
| 🟢 POST | `/api/v1/e2e/execute` | Execute E2E Tests |
| 🟢 POST | `/api/v1/e2e/execute` | Execute E2E Tests |
| 🔵 GET | `/api/v1/e2e/history` | Get Execution History |
| 🔵 GET | `/api/v1/e2e/history` | Get Execution History |
| 🔵 GET | `/api/v1/e2e/results/{execution_id}` | Get Test Results |
| 🔵 GET | `/api/v1/e2e/results/{execution_id}` | Get Test Results |
| 🔵 GET | `/api/v1/e2e/status/{execution_id}` | Get Execution Status |
| 🔵 GET | `/api/v1/e2e/status/{execution_id}` | Get Execution Status |
| 🔵 GET | `/api/v1/evidence-manifests` | List evidence manifests |
| 🟢 POST | `/api/v1/evidence-manifests` | Create evidence manifest |
| 🔵 GET | `/api/v1/evidence-manifests/latest` | Get latest manifest |
| 🔵 GET | `/api/v1/evidence-manifests/status` | Get chain status |
| 🔵 GET | `/api/v1/evidence-manifests/verifications` | Get verification history |
| 🟢 POST | `/api/v1/evidence-manifests/verify` | Verify hash chain |
| 🔵 GET | `/api/v1/evidence-manifests/{manifest_id}` | Get manifest by ID |
| 🔵 GET | `/api/v1/feedback` | List Feedback |
| 🔵 GET | `/api/v1/feedback` | List Feedback |
| 🟢 POST | `/api/v1/feedback` | Create Feedback |
| 🟢 POST | `/api/v1/feedback` | Create Feedback |
| 🔵 GET | `/api/v1/feedback/stats` | Get Feedback Stats |
| 🔵 GET | `/api/v1/feedback/stats` | Get Feedback Stats |
| 🔵 GET | `/api/v1/feedback/{feedback_id}` | Get Feedback |
| 🔵 GET | `/api/v1/feedback/{feedback_id}` | Get Feedback |
| 🟠 PATCH | `/api/v1/feedback/{feedback_id}` | Update Feedback |
| 🟠 PATCH | `/api/v1/feedback/{feedback_id}` | Update Feedback |
| 🔵 GET | `/api/v1/feedback/{feedback_id}/comments` | List Comments |
| 🔵 GET | `/api/v1/feedback/{feedback_id}/comments` | List Comments |
| 🟢 POST | `/api/v1/feedback/{feedback_id}/comments` | Add Comment |
| 🟢 POST | `/api/v1/feedback/{feedback_id}/comments` | Add Comment |
| 🔵 GET | `/api/v1/framework-version/health` | Health check |
| 🔵 GET | `/api/v1/framework-version/health` | Health check |
| 🔵 GET | `/api/v1/framework-version/{project_id}` | Get current Framework version |
| 🔵 GET | `/api/v1/framework-version/{project_id}` | Get current Framework version |
| 🟢 POST | `/api/v1/framework-version/{project_id}` | Record new Framework version |
| 🟢 POST | `/api/v1/framework-version/{project_id}` | Record new Framework version |
| 🔵 GET | `/api/v1/framework-version/{project_id}/compliance` | Get compliance summary |
| 🔵 GET | `/api/v1/framework-version/{project_id}/compliance` | Get compliance summary |
| 🔵 GET | `/api/v1/framework-version/{project_id}/drift` | Check version drift |
| 🔵 GET | `/api/v1/framework-version/{project_id}/drift` | Check version drift |
| 🔵 GET | `/api/v1/framework-version/{project_id}/history` | Get version history |
| 🔵 GET | `/api/v1/framework-version/{project_id}/history` | Get version history |
| 🔵 GET | `/api/v1/gates` | List Gates |
| 🔵 GET | `/api/v1/gates` | List Gates |
| 🟢 POST | `/api/v1/gates` | Create Gate |
| 🟢 POST | `/api/v1/gates` | Create Gate |
| 🟢 POST | `/api/v1/gates-engine/bulk-evaluate` | Evaluate multiple gates |
| 🟢 POST | `/api/v1/gates-engine/bulk-evaluate` | Evaluate multiple gates |
| 🟢 POST | `/api/v1/gates-engine/evaluate-by-code` | Evaluate gate by project and code |
| 🟢 POST | `/api/v1/gates-engine/evaluate-by-code` | Evaluate gate by project and code |
| 🟢 POST | `/api/v1/gates-engine/evaluate/{gate_id}` | Evaluate single gate |
| 🟢 POST | `/api/v1/gates-engine/evaluate/{gate_id}` | Evaluate single gate |
| 🔵 GET | `/api/v1/gates-engine/health` | Gates engine health check |
| 🔵 GET | `/api/v1/gates-engine/health` | Gates engine health check |
| 🔵 GET | `/api/v1/gates-engine/policies/{gate_code}` | Get policies for gate |
| 🔵 GET | `/api/v1/gates-engine/policies/{gate_code}` | Get policies for gate |
| 🔵 GET | `/api/v1/gates-engine/prerequisites/{gate_code}` | Check gate prerequisites |
| 🔵 GET | `/api/v1/gates-engine/prerequisites/{gate_code}` | Check gate prerequisites |
| 🔵 GET | `/api/v1/gates-engine/readiness/{project_id}` | Get project gate readiness |
| 🔵 GET | `/api/v1/gates-engine/readiness/{project_id}` | Get project gate readiness |
| 🔵 GET | `/api/v1/gates-engine/stages` | Get gate-to-stage mapping |
| 🔵 GET | `/api/v1/gates-engine/stages` | Get gate-to-stage mapping |
| 🔴 DELETE | `/api/v1/gates/{gate_id}` | Delete Gate |
| 🔴 DELETE | `/api/v1/gates/{gate_id}` | Delete Gate |
| 🔵 GET | `/api/v1/gates/{gate_id}` | Get Gate |
| 🔵 GET | `/api/v1/gates/{gate_id}` | Get Gate |
| 🟡 PUT | `/api/v1/gates/{gate_id}` | Update Gate |
| 🟡 PUT | `/api/v1/gates/{gate_id}` | Update Gate |
| 🔵 GET | `/api/v1/gates/{gate_id}/actions` | Get Gate Actions |
| 🔵 GET | `/api/v1/gates/{gate_id}/actions` | Get Gate Actions |
| 🔵 GET | `/api/v1/gates/{gate_id}/approvals` | Get Gate Approvals |
| 🔵 GET | `/api/v1/gates/{gate_id}/approvals` | Get Gate Approvals |
| 🟢 POST | `/api/v1/gates/{gate_id}/approve` | Approve Gate |
| 🟢 POST | `/api/v1/gates/{gate_id}/approve` | Approve Gate |
| 🟢 POST | `/api/v1/gates/{gate_id}/evaluate` | Evaluate Gate |
| 🟢 POST | `/api/v1/gates/{gate_id}/evaluate` | Evaluate Gate |
| 🟢 POST | `/api/v1/gates/{gate_id}/evidence` | Upload Evidence |
| 🟢 POST | `/api/v1/gates/{gate_id}/evidence` | Upload Evidence |
| 🟢 POST | `/api/v1/gates/{gate_id}/reject` | Reject Gate |
| 🟢 POST | `/api/v1/gates/{gate_id}/reject` | Reject Gate |
| 🟢 POST | `/api/v1/gates/{gate_id}/submit` | Submit Gate |
| 🟢 POST | `/api/v1/gates/{gate_id}/submit` | Submit Gate |
| 🔵 GET | `/api/v1/governance-metrics` | Get Prometheus metrics |
| 🔵 GET | `/api/v1/governance-metrics/definitions` | Get metric definitions |
| 🔵 GET | `/api/v1/governance-metrics/health` | Metrics service health check |
| 🔵 GET | `/api/v1/governance-metrics/json` | Get metrics in JSON format |
| 🟢 POST | `/api/v1/governance-metrics/record-break-glass` | Record break glass activation |
| 🟢 POST | `/api/v1/governance-metrics/record-bypass` | Record governance bypass incident |
| 🟢 POST | `/api/v1/governance-metrics/record-ceo-override` | Record CEO override |
| 🟢 POST | `/api/v1/governance-metrics/record-developer-friction` | Record developer friction |
| 🟢 POST | `/api/v1/governance-metrics/record-evidence` | Record evidence upload |
| 🟢 POST | `/api/v1/governance-metrics/record-llm` | Record LLM generation metrics |
| 🟢 POST | `/api/v1/governance-metrics/record-submission` | Record governance submission metrics |
| 🟢 POST | `/api/v1/governance-metrics/set-kill-switch` | Set kill switch status |
| 🟢 POST | `/api/v1/governance-metrics/update-ceo-metrics` | Update CEO dashboard metrics |
| 🟢 POST | `/api/v1/governance-metrics/update-system-health` | Update system health metrics |
| 🔵 GET | `/api/v1/governance/dogfooding/status` | Get dogfooding status |
| 🟢 POST | `/api/v1/governance/false-positive` | Report false positive |
| 🔵 GET | `/api/v1/governance/health` | Governance service health check |
| 🟢 POST | `/api/v1/governance/kill-switch` | Emergency kill switch |
| 🔵 GET | `/api/v1/governance/metrics` | Get governance metrics |
| 🔵 GET | `/api/v1/governance/mode` | Get current governance mode |
| 🟡 PUT | `/api/v1/governance/mode` | Set governance mode |
| 🔵 GET | `/api/v1/governance/mode/state` | Get full governance mode state |
| 🔵 GET | `/api/v1/governance/specs/health` | Specification service health check |
| 🟢 POST | `/api/v1/governance/specs/validate` | Validate YAML Frontmatter |
| 🔵 GET | `/api/v1/governance/specs/{spec_id}` | Get Specification Metadata |
| 🔵 GET | `/api/v1/governance/specs/{spec_id}/acceptance-criteria` | List Acceptance Criteria |
| 🔵 GET | `/api/v1/governance/specs/{spec_id}/requirements` | List Functional Requirements |
| 🔵 GET | `/api/v1/governance/tiers/` | List All Tiers |
| 🔵 GET | `/api/v1/governance/tiers/health` | Tier management health check |
| 🔵 GET | `/api/v1/governance/tiers/{project_id}` | Get Project Tier |
| 🟢 POST | `/api/v1/governance/tiers/{project_id}/upgrade` | Request Tier Upgrade |
| 🔵 GET | `/api/v1/governance/tiers/{tier}/requirements` | Get Tier Requirements |
| 🟢 POST | `/api/v1/governance/vibecoding/calculate` | Calculate Vibecoding Index (Database-Backed) |
| 🔵 GET | `/api/v1/governance/vibecoding/health` | Vibecoding service health check |
| 🟢 POST | `/api/v1/governance/vibecoding/kill-switch/check` | Check Kill Switch Triggers |
| 🟢 POST | `/api/v1/governance/vibecoding/route` | Progressive Routing Decision |
| 🔵 GET | `/api/v1/governance/vibecoding/signals/{submission_id}` | Get Signal Breakdown |
| 🔵 GET | `/api/v1/governance/vibecoding/stats/{project_id}` | Get Zone Statistics |
| 🔵 GET | `/api/v1/governance/vibecoding/{submission_id}` | Get Index History |
| 🔵 GET | `/api/v1/grafana-dashboards` | List all Grafana dashboards |
| 🔵 GET | `/api/v1/grafana-dashboards/datasource/template` | Get Prometheus datasource template |
| 🔵 GET | `/api/v1/grafana-dashboards/export/all` | Export all dashboards |
| 🟢 POST | `/api/v1/grafana-dashboards/provision` | Provision dashboards to Grafana |
| 🔵 GET | `/api/v1/grafana-dashboards/{dashboard_type}` | Get dashboard configuration |
| 🔵 GET | `/api/v1/grafana-dashboards/{dashboard_type}/json` | Download dashboard JSON |
| 🔵 GET | `/api/v1/grafana-dashboards/{dashboard_type}/panels` | List dashboard panels |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/aggregations` | List aggregations |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/aggregations` | List aggregations |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/aggregations` | Create aggregation |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/aggregations` | Create aggregation |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}` | Get aggregation |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}` | Get aggregation |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}/apply` | Apply aggregation suggestions |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}/apply` | Apply aggregation suggestions |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}/reject` | Reject aggregation suggestions |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/aggregations/{aggregation_id}/reject` | Reject aggregation suggestions |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/generate-hints` | Generate hints from learnings |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/generate-hints` | Generate hints from learnings |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/hints` | List hints |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/hints` | List hints |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/hints` | Create a hint |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/hints` | Create a hint |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/hints/active` | Get active hints for decomposition |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/hints/active` | Get active hints for decomposition |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/hints/stats` | Get hint statistics |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/hints/stats` | Get hint statistics |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/hints/usage` | Record hint usage |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/hints/usage` | Record hint usage |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/hints/usage/{usage_id}/feedback` | Provide hint usage feedback |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/hints/usage/{usage_id}/feedback` | Provide hint usage feedback |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/hints/{hint_id}` | Get a hint |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/hints/{hint_id}` | Get a hint |
| 🟠 PATCH | `/api/v1/learnings/projects/{project_id}/hints/{hint_id}` | Update a hint |
| 🟠 PATCH | `/api/v1/learnings/projects/{project_id}/hints/{hint_id}` | Update a hint |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/hints/{hint_id}/verify` | Verify a hint |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/hints/{hint_id}/verify` | Verify a hint |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/learnings` | List learnings |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/learnings` | List learnings |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/learnings` | Create a learning manually |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/learnings` | Create a learning manually |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/learnings/bulk-status` | Bulk update learning status |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/learnings/bulk-status` | Bulk update learning status |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/learnings/extract` | Extract learning from PR comment |
| 🟢 POST | `/api/v1/learnings/projects/{project_id}/learnings/extract` | Extract learning from PR comment |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/learnings/stats` | Get learning statistics |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/learnings/stats` | Get learning statistics |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/learnings/{learning_id}` | Get a learning |
| 🔵 GET | `/api/v1/learnings/projects/{project_id}/learnings/{learning_id}` | Get a learning |
| 🟠 PATCH | `/api/v1/learnings/projects/{project_id}/learnings/{learning_id}` | Update a learning |
| 🟠 PATCH | `/api/v1/learnings/projects/{project_id}/learnings/{learning_id}` | Update a learning |
| 🔵 GET | `/api/v1/maturity/health` | Health check |
| 🔵 GET | `/api/v1/maturity/health` | Health check |
| 🔵 GET | `/api/v1/maturity/levels` | Get maturity level definitions |
| 🔵 GET | `/api/v1/maturity/levels` | Get maturity level definitions |
| 🔵 GET | `/api/v1/maturity/org/{org_id}` | Get org-wide maturity report |
| 🔵 GET | `/api/v1/maturity/org/{org_id}` | Get org-wide maturity report |
| 🔵 GET | `/api/v1/maturity/{project_id}` | Get latest maturity assessment |
| 🔵 GET | `/api/v1/maturity/{project_id}` | Get latest maturity assessment |
| 🟢 POST | `/api/v1/maturity/{project_id}/assess` | Perform fresh maturity assessment |
| 🟢 POST | `/api/v1/maturity/{project_id}/assess` | Perform fresh maturity assessment |
| 🔵 GET | `/api/v1/maturity/{project_id}/history` | Get assessment history |
| 🔵 GET | `/api/v1/maturity/{project_id}/history` | Get assessment history |
| 🔵 GET | `/api/v1/mcp/context` | Get context provider usage |
| 🔵 GET | `/api/v1/mcp/context` | Get context provider usage |
| 🔵 GET | `/api/v1/mcp/cost` | Get cost tracking metrics |
| 🔵 GET | `/api/v1/mcp/cost` | Get cost tracking metrics |
| 🔵 GET | `/api/v1/mcp/dashboard` | Get complete dashboard summary |
| 🔵 GET | `/api/v1/mcp/dashboard` | Get complete dashboard summary |
| 🔵 GET | `/api/v1/mcp/health` | Get provider health metrics |
| 🔵 GET | `/api/v1/mcp/health` | Get provider health metrics |
| 🔵 GET | `/api/v1/mcp/latency` | Get latency metrics |
| 🔵 GET | `/api/v1/mcp/latency` | Get latency metrics |
| 🔵 GET | `/api/v1/mrp/health` | Health check |
| 🔵 GET | `/api/v1/mrp/health` | Health check |
| 🟢 POST | `/api/v1/mrp/policies/compare` | Compare two tiers |
| 🟢 POST | `/api/v1/mrp/policies/compare` | Compare two tiers |
| 🟢 POST | `/api/v1/mrp/policies/compare` | Compare two tiers |
| 🔵 GET | `/api/v1/mrp/policies/compliance/{project_id}` | Get tier compliance report |
| 🔵 GET | `/api/v1/mrp/policies/compliance/{project_id}` | Get tier compliance report |
| 🔵 GET | `/api/v1/mrp/policies/compliance/{project_id}` | Get tier compliance report |
| 🟢 POST | `/api/v1/mrp/policies/enforce` | Enforce policies for PR |
| 🟢 POST | `/api/v1/mrp/policies/enforce` | Enforce policies for PR |
| 🟢 POST | `/api/v1/mrp/policies/enforce` | Enforce policies for PR |
| 🔵 GET | `/api/v1/mrp/policies/tiers` | Get all policy tiers |
| 🔵 GET | `/api/v1/mrp/policies/tiers` | Get all policy tiers |
| 🔵 GET | `/api/v1/mrp/policies/tiers` | Get all policy tiers |
| 🟢 POST | `/api/v1/mrp/validate` | Validate MRP 5-point structure |
| 🟢 POST | `/api/v1/mrp/validate` | Validate MRP 5-point structure |
| 🔵 GET | `/api/v1/mrp/validate/{project_id}/{pr_id}` | Get latest MRP validation |
| 🔵 GET | `/api/v1/mrp/validate/{project_id}/{pr_id}` | Get latest MRP validation |
| 🔵 GET | `/api/v1/mrp/vcr/{project_id}/history` | Get VCR history |
| 🔵 GET | `/api/v1/mrp/vcr/{project_id}/history` | Get VCR history |
| 🔵 GET | `/api/v1/mrp/vcr/{project_id}/{pr_id}` | Get latest VCR |
| 🔵 GET | `/api/v1/mrp/vcr/{project_id}/{pr_id}` | Get latest VCR |
| 🔵 GET | `/api/v1/notifications` | List Notifications |
| 🟡 PUT | `/api/v1/notifications/read-all` | Mark All Notifications Read |
| 🔵 GET | `/api/v1/notifications/settings/preferences` | Get Notification Settings |
| 🟡 PUT | `/api/v1/notifications/settings/preferences` | Update Notification Settings |
| 🔵 GET | `/api/v1/notifications/stats/summary` | Get Notification Stats |
| 🔴 DELETE | `/api/v1/notifications/{notification_id}` | Delete Notification |
| 🔵 GET | `/api/v1/notifications/{notification_id}` | Get Notification |
| 🟡 PUT | `/api/v1/notifications/{notification_id}/read` | Mark Notification Read |
| 🟢 POST | `/api/v1/onboarding/{session_id}/force-unlock` | Force unlock (admin) |
| 🟢 POST | `/api/v1/onboarding/{session_id}/force-unlock` | Force unlock (admin) |
| 🟢 POST | `/api/v1/onboarding/{session_id}/lock` | Lock specification |
| 🟢 POST | `/api/v1/onboarding/{session_id}/lock` | Lock specification |
| 🔵 GET | `/api/v1/onboarding/{session_id}/lock-audit` | Get lock audit log |
| 🔵 GET | `/api/v1/onboarding/{session_id}/lock-audit` | Get lock audit log |
| 🔵 GET | `/api/v1/onboarding/{session_id}/lock-status` | Get lock status |
| 🔵 GET | `/api/v1/onboarding/{session_id}/lock-status` | Get lock status |
| 🔵 GET | `/api/v1/onboarding/{session_id}/status` | Get full session status |
| 🔵 GET | `/api/v1/onboarding/{session_id}/status` | Get full session status |
| 🟢 POST | `/api/v1/onboarding/{session_id}/unlock` | Unlock specification |
| 🟢 POST | `/api/v1/onboarding/{session_id}/unlock` | Unlock specification |
| 🟢 POST | `/api/v1/onboarding/{session_id}/verify-hash` | Verify spec hash |
| 🟢 POST | `/api/v1/onboarding/{session_id}/verify-hash` | Verify spec hash |
| 🔵 GET | `/api/v1/organizations` | List Organizations |
| 🔵 GET | `/api/v1/organizations` | List Organizations |
| 🟢 POST | `/api/v1/organizations` | Create Organization |
| 🟢 POST | `/api/v1/organizations` | Create Organization |
| 🔵 GET | `/api/v1/organizations/{org_id}` | Get Organization |
| 🔵 GET | `/api/v1/organizations/{org_id}` | Get Organization |
| 🟠 PATCH | `/api/v1/organizations/{org_id}` | Update Organization |
| 🟠 PATCH | `/api/v1/organizations/{org_id}` | Update Organization |
| 🟢 POST | `/api/v1/organizations/{org_id}/members` | Add Member Directly |
| 🟢 POST | `/api/v1/organizations/{org_id}/members` | Add Member Directly |
| 🔵 GET | `/api/v1/organizations/{org_id}/stats` | Get Organization Statistics |
| 🔵 GET | `/api/v1/organizations/{org_id}/stats` | Get Organization Statistics |
| 🔵 GET | `/api/v1/overrides/event/{event_id}` | Get overrides for event |
| 🟢 POST | `/api/v1/overrides/request` | Create override request |
| 🔵 GET | `/api/v1/overrides/{override_id}` | Get override details |
| 🟢 POST | `/api/v1/overrides/{override_id}/approve` | Approve override |
| 🟢 POST | `/api/v1/overrides/{override_id}/cancel` | Cancel override |
| 🟢 POST | `/api/v1/overrides/{override_id}/reject` | Reject override |
| 🔵 GET | `/api/v1/payments/subscriptions/me` | Get My Subscription |
| 🔵 GET | `/api/v1/payments/subscriptions/me` | Get My Subscription |
| 🟢 POST | `/api/v1/payments/vnpay/create` | Create Vnpay Payment |
| 🟢 POST | `/api/v1/payments/vnpay/create` | Create Vnpay Payment |
| 🟢 POST | `/api/v1/payments/vnpay/ipn` | Vnpay Ipn Handler |
| 🟢 POST | `/api/v1/payments/vnpay/ipn` | Vnpay Ipn Handler |
| 🔵 GET | `/api/v1/payments/vnpay/return` | Vnpay Return Handler |
| 🔵 GET | `/api/v1/payments/vnpay/return` | Vnpay Return Handler |
| 🔵 GET | `/api/v1/payments/{vnp_txn_ref}` | Get Payment Status |
| 🔵 GET | `/api/v1/payments/{vnp_txn_ref}` | Get Payment Status |
| 🟢 POST | `/api/v1/pilot/feedback` | Submit satisfaction survey |
| 🟢 POST | `/api/v1/pilot/feedback` | Submit satisfaction survey |
| 🟢 POST | `/api/v1/pilot/metrics/aggregate` | Trigger daily metrics aggregation |
| 🟢 POST | `/api/v1/pilot/metrics/aggregate` | Trigger daily metrics aggregation |
| 🔵 GET | `/api/v1/pilot/metrics/summary` | Get pilot program summary |
| 🔵 GET | `/api/v1/pilot/metrics/summary` | Get pilot program summary |
| 🔵 GET | `/api/v1/pilot/metrics/targets` | Get Sprint 49 targets |
| 🔵 GET | `/api/v1/pilot/metrics/targets` | Get Sprint 49 targets |
| 🔵 GET | `/api/v1/pilot/participants` | List pilot participants |
| 🔵 GET | `/api/v1/pilot/participants` | List pilot participants |
| 🟢 POST | `/api/v1/pilot/participants` | Register as pilot participant |
| 🟢 POST | `/api/v1/pilot/participants` | Register as pilot participant |
| 🔵 GET | `/api/v1/pilot/participants/me` | Get current user's participant profile |
| 🔵 GET | `/api/v1/pilot/participants/me` | Get current user's participant profile |
| 🔵 GET | `/api/v1/pilot/participants/{participant_id}` | Get participant by ID |
| 🔵 GET | `/api/v1/pilot/participants/{participant_id}` | Get participant by ID |
| 🔵 GET | `/api/v1/pilot/sessions` | Get my sessions |
| 🔵 GET | `/api/v1/pilot/sessions` | Get my sessions |
| 🟢 POST | `/api/v1/pilot/sessions` | Start pilot session (TTFV timer begins) |
| 🟢 POST | `/api/v1/pilot/sessions` | Start pilot session (TTFV timer begins) |
| 🔵 GET | `/api/v1/pilot/sessions/{session_id}` | Get session details |
| 🔵 GET | `/api/v1/pilot/sessions/{session_id}` | Get session details |
| 🟢 POST | `/api/v1/pilot/sessions/{session_id}/generation` | Record generation results |
| 🟢 POST | `/api/v1/pilot/sessions/{session_id}/generation` | Record generation results |
| 🟠 PATCH | `/api/v1/pilot/sessions/{session_id}/stage` | Update session stage |
| 🟠 PATCH | `/api/v1/pilot/sessions/{session_id}/stage` | Update session stage |
| 🟢 POST | `/api/v1/planning/action-items/bulk/status` | Bulk update action item status |
| 🟢 POST | `/api/v1/planning/action-items/bulk/status` | Bulk update action item status |
| 🟢 POST | `/api/v1/planning/action-items/bulk/status` | Bulk update action item status |
| 🟢 POST | `/api/v1/planning/action-items/bulk/status` | Bulk update action item status |
| 🟢 POST | `/api/v1/planning/action-items/bulk/status` | Bulk update action item status |
| 🔴 DELETE | `/api/v1/planning/action-items/{item_id}` | Delete an action item |
| 🔴 DELETE | `/api/v1/planning/action-items/{item_id}` | Delete an action item |
| 🔴 DELETE | `/api/v1/planning/action-items/{item_id}` | Delete an action item |
| 🔴 DELETE | `/api/v1/planning/action-items/{item_id}` | Delete an action item |
| 🔴 DELETE | `/api/v1/planning/action-items/{item_id}` | Delete an action item |
| 🔵 GET | `/api/v1/planning/action-items/{item_id}` | Get a single action item |
| 🔵 GET | `/api/v1/planning/action-items/{item_id}` | Get a single action item |
| 🔵 GET | `/api/v1/planning/action-items/{item_id}` | Get a single action item |
| 🔵 GET | `/api/v1/planning/action-items/{item_id}` | Get a single action item |
| 🔵 GET | `/api/v1/planning/action-items/{item_id}` | Get a single action item |
| 🟡 PUT | `/api/v1/planning/action-items/{item_id}` | Update an action item |
| 🟡 PUT | `/api/v1/planning/action-items/{item_id}` | Update an action item |
| 🟡 PUT | `/api/v1/planning/action-items/{item_id}` | Update an action item |
| 🟡 PUT | `/api/v1/planning/action-items/{item_id}` | Update an action item |
| 🟡 PUT | `/api/v1/planning/action-items/{item_id}` | Update an action item |
| 🟢 POST | `/api/v1/planning/allocations` | Create resource allocation |
| 🟢 POST | `/api/v1/planning/allocations` | Create resource allocation |
| 🟢 POST | `/api/v1/planning/allocations` | Create resource allocation |
| 🟢 POST | `/api/v1/planning/allocations` | Create resource allocation |
| 🟢 POST | `/api/v1/planning/allocations` | Create resource allocation |
| 🟢 POST | `/api/v1/planning/allocations/check-conflicts` | Check allocation conflicts |
| 🟢 POST | `/api/v1/planning/allocations/check-conflicts` | Check allocation conflicts |
| 🟢 POST | `/api/v1/planning/allocations/check-conflicts` | Check allocation conflicts |
| 🟢 POST | `/api/v1/planning/allocations/check-conflicts` | Check allocation conflicts |
| 🟢 POST | `/api/v1/planning/allocations/check-conflicts` | Check allocation conflicts |
| 🔴 DELETE | `/api/v1/planning/allocations/{allocation_id}` | Delete a resource allocation |
| 🔴 DELETE | `/api/v1/planning/allocations/{allocation_id}` | Delete a resource allocation |
| 🔴 DELETE | `/api/v1/planning/allocations/{allocation_id}` | Delete a resource allocation |
| 🔴 DELETE | `/api/v1/planning/allocations/{allocation_id}` | Delete a resource allocation |
| 🔴 DELETE | `/api/v1/planning/allocations/{allocation_id}` | Delete a resource allocation |
| 🔵 GET | `/api/v1/planning/allocations/{allocation_id}` | Get a resource allocation |
| 🔵 GET | `/api/v1/planning/allocations/{allocation_id}` | Get a resource allocation |
| 🔵 GET | `/api/v1/planning/allocations/{allocation_id}` | Get a resource allocation |
| 🔵 GET | `/api/v1/planning/allocations/{allocation_id}` | Get a resource allocation |
| 🔵 GET | `/api/v1/planning/allocations/{allocation_id}` | Get a resource allocation |
| 🟡 PUT | `/api/v1/planning/allocations/{allocation_id}` | Update a resource allocation |
| 🟡 PUT | `/api/v1/planning/allocations/{allocation_id}` | Update a resource allocation |
| 🟡 PUT | `/api/v1/planning/allocations/{allocation_id}` | Update a resource allocation |
| 🟡 PUT | `/api/v1/planning/allocations/{allocation_id}` | Update a resource allocation |
| 🟡 PUT | `/api/v1/planning/allocations/{allocation_id}` | Update a resource allocation |
| 🔵 GET | `/api/v1/planning/backlog` | List Backlog Items |
| 🔵 GET | `/api/v1/planning/backlog` | List Backlog Items |
| 🟢 POST | `/api/v1/planning/backlog` | Create Backlog Item |
| 🟢 POST | `/api/v1/planning/backlog` | Create Backlog Item |
| 🔵 GET | `/api/v1/planning/backlog/assignees/{project_id}` | Get Valid Assignees |
| 🔵 GET | `/api/v1/planning/backlog/assignees/{project_id}` | Get Valid Assignees |
| 🟢 POST | `/api/v1/planning/backlog/bulk/move-to-sprint` | Bulk Move To Sprint |
| 🟢 POST | `/api/v1/planning/backlog/bulk/move-to-sprint` | Bulk Move To Sprint |
| 🟢 POST | `/api/v1/planning/backlog/bulk/update-priority` | Bulk Update Priority |
| 🟢 POST | `/api/v1/planning/backlog/bulk/update-priority` | Bulk Update Priority |
| 🔴 DELETE | `/api/v1/planning/backlog/{item_id}` | Delete Backlog Item |
| 🔴 DELETE | `/api/v1/planning/backlog/{item_id}` | Delete Backlog Item |
| 🔵 GET | `/api/v1/planning/backlog/{item_id}` | Get Backlog Item |
| 🔵 GET | `/api/v1/planning/backlog/{item_id}` | Get Backlog Item |
| 🟡 PUT | `/api/v1/planning/backlog/{item_id}` | Update Backlog Item |
| 🟡 PUT | `/api/v1/planning/backlog/{item_id}` | Update Backlog Item |
| 🔵 GET | `/api/v1/planning/dashboard/{project_id}` | Get Planning Dashboard |
| 🔵 GET | `/api/v1/planning/dashboard/{project_id}` | Get Planning Dashboard |
| 🟢 POST | `/api/v1/planning/dependencies` | Create sprint dependency |
| 🟢 POST | `/api/v1/planning/dependencies` | Create sprint dependency |
| 🟢 POST | `/api/v1/planning/dependencies` | Create sprint dependency |
| 🟢 POST | `/api/v1/planning/dependencies` | Create sprint dependency |
| 🟢 POST | `/api/v1/planning/dependencies` | Create sprint dependency |
| 🟢 POST | `/api/v1/planning/dependencies/bulk/resolve` | Bulk resolve dependencies |
| 🟢 POST | `/api/v1/planning/dependencies/bulk/resolve` | Bulk resolve dependencies |
| 🟢 POST | `/api/v1/planning/dependencies/bulk/resolve` | Bulk resolve dependencies |
| 🟢 POST | `/api/v1/planning/dependencies/bulk/resolve` | Bulk resolve dependencies |
| 🟢 POST | `/api/v1/planning/dependencies/bulk/resolve` | Bulk resolve dependencies |
| 🔵 GET | `/api/v1/planning/dependencies/check-circular` | Check for circular dependency |
| 🔵 GET | `/api/v1/planning/dependencies/check-circular` | Check for circular dependency |
| 🔵 GET | `/api/v1/planning/dependencies/check-circular` | Check for circular dependency |
| 🔵 GET | `/api/v1/planning/dependencies/check-circular` | Check for circular dependency |
| 🔵 GET | `/api/v1/planning/dependencies/check-circular` | Check for circular dependency |
| 🔴 DELETE | `/api/v1/planning/dependencies/{dependency_id}` | Delete a sprint dependency |
| 🔴 DELETE | `/api/v1/planning/dependencies/{dependency_id}` | Delete a sprint dependency |
| 🔴 DELETE | `/api/v1/planning/dependencies/{dependency_id}` | Delete a sprint dependency |
| 🔴 DELETE | `/api/v1/planning/dependencies/{dependency_id}` | Delete a sprint dependency |
| 🔴 DELETE | `/api/v1/planning/dependencies/{dependency_id}` | Delete a sprint dependency |
| 🔵 GET | `/api/v1/planning/dependencies/{dependency_id}` | Get a sprint dependency |
| 🔵 GET | `/api/v1/planning/dependencies/{dependency_id}` | Get a sprint dependency |
| 🔵 GET | `/api/v1/planning/dependencies/{dependency_id}` | Get a sprint dependency |
| 🔵 GET | `/api/v1/planning/dependencies/{dependency_id}` | Get a sprint dependency |
| 🔵 GET | `/api/v1/planning/dependencies/{dependency_id}` | Get a sprint dependency |
| 🟡 PUT | `/api/v1/planning/dependencies/{dependency_id}` | Update a sprint dependency |
| 🟡 PUT | `/api/v1/planning/dependencies/{dependency_id}` | Update a sprint dependency |
| 🟡 PUT | `/api/v1/planning/dependencies/{dependency_id}` | Update a sprint dependency |
| 🟡 PUT | `/api/v1/planning/dependencies/{dependency_id}` | Update a sprint dependency |
| 🟡 PUT | `/api/v1/planning/dependencies/{dependency_id}` | Update a sprint dependency |
| 🟢 POST | `/api/v1/planning/dependencies/{dependency_id}/resolve` | Resolve a sprint dependency |
| 🟢 POST | `/api/v1/planning/dependencies/{dependency_id}/resolve` | Resolve a sprint dependency |
| 🟢 POST | `/api/v1/planning/dependencies/{dependency_id}/resolve` | Resolve a sprint dependency |
| 🟢 POST | `/api/v1/planning/dependencies/{dependency_id}/resolve` | Resolve a sprint dependency |
| 🟢 POST | `/api/v1/planning/dependencies/{dependency_id}/resolve` | Resolve a sprint dependency |
| 🔵 GET | `/api/v1/planning/phases` | List Phases |
| 🔵 GET | `/api/v1/planning/phases` | List Phases |
| 🟢 POST | `/api/v1/planning/phases` | Create Phase |
| 🟢 POST | `/api/v1/planning/phases` | Create Phase |
| 🔴 DELETE | `/api/v1/planning/phases/{phase_id}` | Delete Phase |
| 🔴 DELETE | `/api/v1/planning/phases/{phase_id}` | Delete Phase |
| 🔵 GET | `/api/v1/planning/phases/{phase_id}` | Get Phase |
| 🔵 GET | `/api/v1/planning/phases/{phase_id}` | Get Phase |
| 🟡 PUT | `/api/v1/planning/phases/{phase_id}` | Update Phase |
| 🟡 PUT | `/api/v1/planning/phases/{phase_id}` | Update Phase |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/dependency-analysis` | Analyze project dependencies |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/dependency-analysis` | Analyze project dependencies |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/dependency-analysis` | Analyze project dependencies |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/dependency-analysis` | Analyze project dependencies |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/dependency-analysis` | Analyze project dependencies |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/dependency-graph` | Get dependency graph for a project |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/dependency-graph` | Get dependency graph for a project |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/dependency-graph` | Get dependency graph for a project |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/dependency-graph` | Get dependency graph for a project |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/dependency-graph` | Get dependency graph for a project |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/resource-heatmap` | Get resource allocation heatmap |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/resource-heatmap` | Get resource allocation heatmap |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/resource-heatmap` | Get resource allocation heatmap |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/resource-heatmap` | Get resource allocation heatmap |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/resource-heatmap` | Get resource allocation heatmap |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/retrospective-comparison` | Compare retrospectives across sprints |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/retrospective-comparison` | Compare retrospectives across sprints |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/retrospective-comparison` | Compare retrospectives across sprints |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/retrospective-comparison` | Compare retrospectives across sprints |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/retrospective-comparison` | Compare retrospectives across sprints |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/template-suggestions` | Get template suggestions for project |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/template-suggestions` | Get template suggestions for project |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/template-suggestions` | Get template suggestions for project |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/template-suggestions` | Get template suggestions for project |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/template-suggestions` | Get template suggestions for project |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/velocity` | Get project velocity metrics |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/velocity` | Get project velocity metrics |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/velocity` | Get project velocity metrics |
| 🔵 GET | `/api/v1/planning/projects/{project_id}/velocity` | Get project velocity metrics |
| 🔵 GET | `/api/v1/planning/roadmaps` | List Roadmaps |
| 🔵 GET | `/api/v1/planning/roadmaps` | List Roadmaps |
| 🟢 POST | `/api/v1/planning/roadmaps` | Create Roadmap |
| 🟢 POST | `/api/v1/planning/roadmaps` | Create Roadmap |
| 🔴 DELETE | `/api/v1/planning/roadmaps/{roadmap_id}` | Delete Roadmap |
| 🔴 DELETE | `/api/v1/planning/roadmaps/{roadmap_id}` | Delete Roadmap |
| 🔵 GET | `/api/v1/planning/roadmaps/{roadmap_id}` | Get Roadmap |
| 🔵 GET | `/api/v1/planning/roadmaps/{roadmap_id}` | Get Roadmap |
| 🟡 PUT | `/api/v1/planning/roadmaps/{roadmap_id}` | Update Roadmap |
| 🟡 PUT | `/api/v1/planning/roadmaps/{roadmap_id}` | Update Roadmap |
| 🔵 GET | `/api/v1/planning/sprints` | List Sprints |
| 🔵 GET | `/api/v1/planning/sprints` | List Sprints |
| 🟢 POST | `/api/v1/planning/sprints` | Create Sprint |
| 🟢 POST | `/api/v1/planning/sprints` | Create Sprint |
| 🔴 DELETE | `/api/v1/planning/sprints/{sprint_id}` | Delete Sprint |
| 🔴 DELETE | `/api/v1/planning/sprints/{sprint_id}` | Delete Sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}` | Get Sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}` | Get Sprint |
| 🟡 PUT | `/api/v1/planning/sprints/{sprint_id}` | Update Sprint |
| 🟡 PUT | `/api/v1/planning/sprints/{sprint_id}` | Update Sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/action-items` | List action items for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/action-items` | List action items for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/action-items` | List action items for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/action-items` | List action items for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/action-items` | List action items for a sprint |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/action-items` | Create action item from retrospective |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/action-items` | Create action item from retrospective |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/action-items` | Create action item from retrospective |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/action-items` | Create action item from retrospective |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/action-items` | Create action item from retrospective |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/action-items/bulk` | Bulk create action items |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/action-items/bulk` | Bulk create action items |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/action-items/bulk` | Bulk create action items |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/action-items/bulk` | Bulk create action items |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/action-items/bulk` | Bulk create action items |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/action-items/stats` | Get action items statistics |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/action-items/stats` | Get action items statistics |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/action-items/stats` | Get action items statistics |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/action-items/stats` | Get action items statistics |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/action-items/stats` | Get action items statistics |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/allocations` | List allocations for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/allocations` | List allocations for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/allocations` | List allocations for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/allocations` | List allocations for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/allocations` | List allocations for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/analytics` | Get comprehensive sprint analytics |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/analytics` | Get comprehensive sprint analytics |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/analytics` | Get comprehensive sprint analytics |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/analytics` | Get comprehensive sprint analytics |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/analytics` | Get comprehensive sprint analytics |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/burndown` | Get sprint burndown chart data |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/burndown` | Get sprint burndown chart data |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/burndown` | Get sprint burndown chart data |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/burndown` | Get sprint burndown chart data |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/burndown` | Get sprint burndown chart data |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/capacity` | Get sprint capacity |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/capacity` | Get sprint capacity |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/capacity` | Get sprint capacity |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/capacity` | Get sprint capacity |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/capacity` | Get sprint capacity |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/dependencies` | List dependencies for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/dependencies` | List dependencies for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/dependencies` | List dependencies for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/dependencies` | List dependencies for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/dependencies` | List dependencies for a sprint |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/forecast` | Get sprint completion forecast |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/forecast` | Get sprint completion forecast |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/forecast` | Get sprint completion forecast |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/forecast` | Get sprint completion forecast |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/forecast` | Get sprint completion forecast |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/gates` | List Gate Evaluations |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/gates` | List Gate Evaluations |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/gates` | Create Gate Evaluation |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/gates` | Create Gate Evaluation |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/gates/{gate_type}` | Get Gate Evaluation |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/gates/{gate_type}` | Get Gate Evaluation |
| 🟡 PUT | `/api/v1/planning/sprints/{sprint_id}/gates/{gate_type}` | Update Gate Evaluation |
| 🟡 PUT | `/api/v1/planning/sprints/{sprint_id}/gates/{gate_type}` | Update Gate Evaluation |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/gates/{gate_type}/submit` | Submit Gate Evaluation |
| 🟢 POST | `/api/v1/planning/sprints/{sprint_id}/gates/{gate_type}/submit` | Submit Gate Evaluation |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/health` | Get sprint health indicators |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/health` | Get sprint health indicators |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/health` | Get sprint health indicators |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/health` | Get sprint health indicators |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/retrospective` | Get auto-generated sprint retrospective |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/retrospective` | Get auto-generated sprint retrospective |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/retrospective` | Get auto-generated sprint retrospective |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/retrospective` | Get auto-generated sprint retrospective |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/retrospective` | Get auto-generated sprint retrospective |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/suggestions` | Get AI prioritization suggestions |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/suggestions` | Get AI prioritization suggestions |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/suggestions` | Get AI prioritization suggestions |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/suggestions` | Get AI prioritization suggestions |
| 🔵 GET | `/api/v1/planning/sprints/{sprint_id}/suggestions` | Get AI prioritization suggestions |
| 🟢 POST | `/api/v1/planning/subagent/conformance` | Check PR conformance |
| 🟢 POST | `/api/v1/planning/subagent/conformance` | Check PR conformance |
| 🔵 GET | `/api/v1/planning/subagent/health` | Health check |
| 🔵 GET | `/api/v1/planning/subagent/health` | Health check |
| 🟢 POST | `/api/v1/planning/subagent/plan` | Start planning session |
| 🟢 POST | `/api/v1/planning/subagent/plan` | Start planning session |
| 🟢 POST | `/api/v1/planning/subagent/plan/with-risk` | Start risk-based planning session (Sprint 101) |
| 🟢 POST | `/api/v1/planning/subagent/plan/with-risk` | Start risk-based planning session (Sprint 101) |
| 🔵 GET | `/api/v1/planning/subagent/sessions` | List planning sessions |
| 🔵 GET | `/api/v1/planning/subagent/sessions` | List planning sessions |
| 🟢 POST | `/api/v1/planning/subagent/should-plan` | Check if planning is required |
| 🟢 POST | `/api/v1/planning/subagent/should-plan` | Check if planning is required |
| 🔵 GET | `/api/v1/planning/subagent/{planning_id}` | Get planning result |
| 🔵 GET | `/api/v1/planning/subagent/{planning_id}` | Get planning result |
| 🟢 POST | `/api/v1/planning/subagent/{planning_id}/approve` | Approve or reject plan |
| 🟢 POST | `/api/v1/planning/subagent/{planning_id}/approve` | Approve or reject plan |
| 🔵 GET | `/api/v1/planning/teams/{team_id}/capacity` | Get team capacity |
| 🔵 GET | `/api/v1/planning/teams/{team_id}/capacity` | Get team capacity |
| 🔵 GET | `/api/v1/planning/teams/{team_id}/capacity` | Get team capacity |
| 🔵 GET | `/api/v1/planning/teams/{team_id}/capacity` | Get team capacity |
| 🔵 GET | `/api/v1/planning/teams/{team_id}/capacity` | Get team capacity |
| 🔵 GET | `/api/v1/planning/templates` | List sprint templates |
| 🔵 GET | `/api/v1/planning/templates` | List sprint templates |
| 🔵 GET | `/api/v1/planning/templates` | List sprint templates |
| 🔵 GET | `/api/v1/planning/templates` | List sprint templates |
| 🔵 GET | `/api/v1/planning/templates` | List sprint templates |
| 🟢 POST | `/api/v1/planning/templates` | Create sprint template |
| 🟢 POST | `/api/v1/planning/templates` | Create sprint template |
| 🟢 POST | `/api/v1/planning/templates` | Create sprint template |
| 🟢 POST | `/api/v1/planning/templates` | Create sprint template |
| 🟢 POST | `/api/v1/planning/templates` | Create sprint template |
| 🟢 POST | `/api/v1/planning/templates/bulk/delete` | Bulk delete templates |
| 🟢 POST | `/api/v1/planning/templates/bulk/delete` | Bulk delete templates |
| 🟢 POST | `/api/v1/planning/templates/bulk/delete` | Bulk delete templates |
| 🟢 POST | `/api/v1/planning/templates/bulk/delete` | Bulk delete templates |
| 🟢 POST | `/api/v1/planning/templates/bulk/delete` | Bulk delete templates |
| 🔵 GET | `/api/v1/planning/templates/default` | Get default template |
| 🔵 GET | `/api/v1/planning/templates/default` | Get default template |
| 🔵 GET | `/api/v1/planning/templates/default` | Get default template |
| 🔵 GET | `/api/v1/planning/templates/default` | Get default template |
| 🔵 GET | `/api/v1/planning/templates/default` | Get default template |
| 🔴 DELETE | `/api/v1/planning/templates/{template_id}` | Delete a sprint template |
| 🔴 DELETE | `/api/v1/planning/templates/{template_id}` | Delete a sprint template |
| 🔴 DELETE | `/api/v1/planning/templates/{template_id}` | Delete a sprint template |
| 🔴 DELETE | `/api/v1/planning/templates/{template_id}` | Delete a sprint template |
| 🔴 DELETE | `/api/v1/planning/templates/{template_id}` | Delete a sprint template |
| 🔵 GET | `/api/v1/planning/templates/{template_id}` | Get a sprint template |
| 🔵 GET | `/api/v1/planning/templates/{template_id}` | Get a sprint template |
| 🔵 GET | `/api/v1/planning/templates/{template_id}` | Get a sprint template |
| 🔵 GET | `/api/v1/planning/templates/{template_id}` | Get a sprint template |
| 🔵 GET | `/api/v1/planning/templates/{template_id}` | Get a sprint template |
| 🟡 PUT | `/api/v1/planning/templates/{template_id}` | Update a sprint template |
| 🟡 PUT | `/api/v1/planning/templates/{template_id}` | Update a sprint template |
| 🟡 PUT | `/api/v1/planning/templates/{template_id}` | Update a sprint template |
| 🟡 PUT | `/api/v1/planning/templates/{template_id}` | Update a sprint template |
| 🟡 PUT | `/api/v1/planning/templates/{template_id}` | Update a sprint template |
| 🟢 POST | `/api/v1/planning/templates/{template_id}/apply` | Apply template to create sprint |
| 🟢 POST | `/api/v1/planning/templates/{template_id}/apply` | Apply template to create sprint |
| 🟢 POST | `/api/v1/planning/templates/{template_id}/apply` | Apply template to create sprint |
| 🟢 POST | `/api/v1/planning/templates/{template_id}/apply` | Apply template to create sprint |
| 🟢 POST | `/api/v1/planning/templates/{template_id}/apply` | Apply template to create sprint |
| 🔵 GET | `/api/v1/planning/users/{user_id}/allocations` | List allocations for a user |
| 🔵 GET | `/api/v1/planning/users/{user_id}/allocations` | List allocations for a user |
| 🔵 GET | `/api/v1/planning/users/{user_id}/allocations` | List allocations for a user |
| 🔵 GET | `/api/v1/planning/users/{user_id}/allocations` | List allocations for a user |
| 🔵 GET | `/api/v1/planning/users/{user_id}/allocations` | List allocations for a user |
| 🔵 GET | `/api/v1/planning/users/{user_id}/capacity` | Get user capacity |
| 🔵 GET | `/api/v1/planning/users/{user_id}/capacity` | Get user capacity |
| 🔵 GET | `/api/v1/planning/users/{user_id}/capacity` | Get user capacity |
| 🔵 GET | `/api/v1/planning/users/{user_id}/capacity` | Get user capacity |
| 🔵 GET | `/api/v1/planning/users/{user_id}/capacity` | Get user capacity |
| 🔵 GET | `/api/v1/policies` | List policies |
| 🟢 POST | `/api/v1/policies/evaluate` | Evaluate policy |
| 🔵 GET | `/api/v1/policies/evaluations/{gate_id}` | Get policy evaluations for gate |
| 🔵 GET | `/api/v1/policies/{policy_id}` | Get policy details |
| 🟡 PUT | `/api/v1/policies/{policy_id}` | Update policy |
| 🔵 GET | `/api/v1/projects` | List Projects |
| 🔵 GET | `/api/v1/projects` | List Projects |
| 🟢 POST | `/api/v1/projects` | Create Project |
| 🟢 POST | `/api/v1/projects` | Create Project |
| 🟢 POST | `/api/v1/projects/init` | Initialize SDLC project |
| 🟢 POST | `/api/v1/projects/init` | Initialize SDLC project |
| 🔴 DELETE | `/api/v1/projects/{project_id}` | Delete Project |
| 🔴 DELETE | `/api/v1/projects/{project_id}` | Delete Project |
| 🔵 GET | `/api/v1/projects/{project_id}` | Get Project |
| 🔵 GET | `/api/v1/projects/{project_id}` | Get Project |
| 🟡 PUT | `/api/v1/projects/{project_id}` | Update Project |
| 🟡 PUT | `/api/v1/projects/{project_id}` | Update Project |
| 🔵 GET | `/api/v1/projects/{project_id}/compliance-summary` | Get compliance summary |
| 🔵 GET | `/api/v1/projects/{project_id}/compliance-summary` | Get compliance summary |
| 🔵 GET | `/api/v1/projects/{project_id}/compliance/history` | Get compliance score history |
| 🔵 GET | `/api/v1/projects/{project_id}/compliance/history` | Get compliance score history |
| 🔵 GET | `/api/v1/projects/{project_id}/compliance/last-check` | Get last folder collision check |
| 🔵 GET | `/api/v1/projects/{project_id}/compliance/last-check` | Get last folder collision check |
| 🔵 GET | `/api/v1/projects/{project_id}/compliance/score` | Get quick compliance score |
| 🔵 GET | `/api/v1/projects/{project_id}/compliance/score` | Get quick compliance score |
| 🔵 GET | `/api/v1/projects/{project_id}/context` | Get project context (stage, gate, sprint) |
| 🔵 GET | `/api/v1/projects/{project_id}/context` | Get project context (stage, gate, sprint) |
| 🟡 PUT | `/api/v1/projects/{project_id}/context` | Update project context (stage, gate, sprint) |
| 🟡 PUT | `/api/v1/projects/{project_id}/context` | Update project context (stage, gate, sprint) |
| 🔵 GET | `/api/v1/projects/{project_id}/evidence/gaps` | Get Evidence Gaps |
| 🔵 GET | `/api/v1/projects/{project_id}/evidence/status` | Get Evidence Status |
| 🟢 POST | `/api/v1/projects/{project_id}/evidence/validate` | Trigger Evidence Validation |
| 🟢 POST | `/api/v1/projects/{project_id}/migrate-stages` | Migrate project stages to SDLC 5.0.0 |
| 🟢 POST | `/api/v1/projects/{project_id}/migrate-stages` | Migrate project stages to SDLC 5.0.0 |
| 🔵 GET | `/api/v1/projects/{project_id}/overrides` | Get project overrides |
| 🔴 DELETE | `/api/v1/projects/{project_id}/policy-pack` | Delete policy pack |
| 🔵 GET | `/api/v1/projects/{project_id}/policy-pack` | Get project's policy pack |
| 🟢 POST | `/api/v1/projects/{project_id}/policy-pack` | Create or update policy pack |
| 🟢 POST | `/api/v1/projects/{project_id}/policy-pack/evaluate` | Evaluate policies |
| 🟢 POST | `/api/v1/projects/{project_id}/policy-pack/init` | Initialize default policy pack |
| 🟢 POST | `/api/v1/projects/{project_id}/policy-pack/rules` | Add policy rule |
| 🔴 DELETE | `/api/v1/projects/{project_id}/policy-pack/rules/{policy_id}` | Delete policy rule |
| 🟡 PUT | `/api/v1/projects/{project_id}/policy-pack/rules/{policy_id}` | Update policy rule |
| 🟢 POST | `/api/v1/projects/{project_id}/sync` | Sync project metadata from repository files |
| 🟢 POST | `/api/v1/projects/{project_id}/sync` | Sync project metadata from repository files |
| 🔵 GET | `/api/v1/projects/{project_id}/timeline` | List evidence timeline events |
| 🔵 GET | `/api/v1/projects/{project_id}/timeline/export` | Export evidence data |
| 🔵 GET | `/api/v1/projects/{project_id}/timeline/stats` | Get timeline statistics |
| 🔵 GET | `/api/v1/projects/{project_id}/timeline/{event_id}` | Get event detail |
| 🟢 POST | `/api/v1/projects/{project_id}/validate-structure` | Validate SDLC 5.0.0 structure |
| 🟢 POST | `/api/v1/projects/{project_id}/validate-structure` | Validate SDLC 5.0.0 structure |
| 🟢 POST | `/api/v1/projects/{project_id}/validate/compliance` | Calculate compliance score |
| 🟢 POST | `/api/v1/projects/{project_id}/validate/compliance` | Calculate compliance score |
| 🟢 POST | `/api/v1/projects/{project_id}/validate/duplicates` | Detect duplicate stage folders |
| 🟢 POST | `/api/v1/projects/{project_id}/validate/duplicates` | Detect duplicate stage folders |
| 🔵 GET | `/api/v1/projects/{project_id}/validation-history` | Get validation history |
| 🔵 GET | `/api/v1/projects/{project_id}/validation-history` | Get validation history |
| 🔵 GET | `/api/v1/push/status` | Get Push Status |
| 🔵 GET | `/api/v1/push/status` | Get Push Status |
| 🟢 POST | `/api/v1/push/subscribe` | Subscribe To Push |
| 🟢 POST | `/api/v1/push/subscribe` | Subscribe To Push |
| 🔵 GET | `/api/v1/push/subscriptions` | List User Subscriptions |
| 🔵 GET | `/api/v1/push/subscriptions` | List User Subscriptions |
| 🟢 POST | `/api/v1/push/unsubscribe` | Unsubscribe From Push |
| 🟢 POST | `/api/v1/push/unsubscribe` | Unsubscribe From Push |
| 🔵 GET | `/api/v1/push/vapid-key` | Get Vapid Public Key |
| 🔵 GET | `/api/v1/push/vapid-key` | Get Vapid Public Key |
| 🟢 POST | `/api/v1/risk/analyze` | Analyze diff for risk factors |
| 🟢 POST | `/api/v1/risk/analyze` | Analyze diff for risk factors |
| 🔵 GET | `/api/v1/risk/factors` | List 7 mandatory risk factors |
| 🔵 GET | `/api/v1/risk/factors` | List 7 mandatory risk factors |
| 🔵 GET | `/api/v1/risk/levels` | Get risk level thresholds |
| 🔵 GET | `/api/v1/risk/levels` | Get risk level thresholds |
| 🔵 GET | `/api/v1/risk/should-plan` | Quick check if planning is needed |
| 🔵 GET | `/api/v1/risk/should-plan` | Quick check if planning is needed |
| 🔵 GET | `/api/v1/sast/health` | SAST health check |
| 🔵 GET | `/api/v1/sast/health` | SAST health check |
| 🔵 GET | `/api/v1/sast/projects/{project_id}/analytics` | Get SAST analytics |
| 🔵 GET | `/api/v1/sast/projects/{project_id}/analytics` | Get SAST analytics |
| 🟢 POST | `/api/v1/sast/projects/{project_id}/scan` | Initiate SAST scan |
| 🟢 POST | `/api/v1/sast/projects/{project_id}/scan` | Initiate SAST scan |
| 🔵 GET | `/api/v1/sast/projects/{project_id}/scans` | Get scan history |
| 🔵 GET | `/api/v1/sast/projects/{project_id}/scans` | Get scan history |
| 🔵 GET | `/api/v1/sast/projects/{project_id}/scans/{scan_id}` | Get scan details |
| 🔵 GET | `/api/v1/sast/projects/{project_id}/scans/{scan_id}` | Get scan details |
| 🔵 GET | `/api/v1/sast/projects/{project_id}/trend` | Get findings trend |
| 🔵 GET | `/api/v1/sast/projects/{project_id}/trend` | Get findings trend |
| 🟢 POST | `/api/v1/sast/scan-snippet` | Scan code snippet |
| 🟢 POST | `/api/v1/sast/scan-snippet` | Scan code snippet |
| 🟢 POST | `/api/v1/sop/generate` | Generate SOP from workflow description |
| 🟢 POST | `/api/v1/sop/generate` | Generate SOP from workflow description |
| 🔵 GET | `/api/v1/sop/health` | SOP Generator health check |
| 🔵 GET | `/api/v1/sop/health` | SOP Generator health check |
| 🔵 GET | `/api/v1/sop/list` | List generated SOPs |
| 🔵 GET | `/api/v1/sop/list` | List generated SOPs |
| 🔵 GET | `/api/v1/sop/types` | List supported SOP types |
| 🔵 GET | `/api/v1/sop/types` | List supported SOP types |
| 🔵 GET | `/api/v1/sop/{sop_id}` | Get SOP details |
| 🔵 GET | `/api/v1/sop/{sop_id}` | Get SOP details |
| 🔵 GET | `/api/v1/sop/{sop_id}/mrp` | Get MRP evidence for SOP |
| 🔵 GET | `/api/v1/sop/{sop_id}/mrp` | Get MRP evidence for SOP |
| 🔵 GET | `/api/v1/sop/{sop_id}/vcr` | Get VCR decision for SOP |
| 🔵 GET | `/api/v1/sop/{sop_id}/vcr` | Get VCR decision for SOP |
| 🟢 POST | `/api/v1/sop/{sop_id}/vcr` | Submit VCR decision for SOP |
| 🟢 POST | `/api/v1/sop/{sop_id}/vcr` | Submit VCR decision for SOP |
| 🟢 POST | `/api/v1/spec-converter/convert` | Convert Specification |
| 🟢 POST | `/api/v1/spec-converter/convert` | Convert Specification |
| 🟢 POST | `/api/v1/spec-converter/detect` | Detect Format |
| 🟢 POST | `/api/v1/spec-converter/detect` | Detect Format |
| 🟢 POST | `/api/v1/spec-converter/import/jira` | Import From Jira |
| 🟢 POST | `/api/v1/spec-converter/import/jira` | Import From Jira |
| 🟢 POST | `/api/v1/spec-converter/import/linear` | Import From Linear |
| 🟢 POST | `/api/v1/spec-converter/import/linear` | Import From Linear |
| 🟢 POST | `/api/v1/spec-converter/import/text` | Import From Text |
| 🟢 POST | `/api/v1/spec-converter/import/text` | Import From Text |
| 🟢 POST | `/api/v1/spec-converter/parse` | Parse Specification |
| 🟢 POST | `/api/v1/spec-converter/parse` | Parse Specification |
| 🟢 POST | `/api/v1/spec-converter/render` | Render Specification |
| 🟢 POST | `/api/v1/spec-converter/render` | Render Specification |
| 🟢 POST | `/api/v1/stage-gating/advance` | Advance to next stage |
| 🟢 POST | `/api/v1/stage-gating/complete` | Mark stage as complete |
| 🔵 GET | `/api/v1/stage-gating/health` | Stage gating health check |
| 🔵 GET | `/api/v1/stage-gating/progress/{project_id}` | Get stage progress |
| 🔵 GET | `/api/v1/stage-gating/rules` | Get all stage rules |
| 🔵 GET | `/api/v1/stage-gating/rules/{stage}` | Get rules for specific stage |
| 🟢 POST | `/api/v1/stage-gating/validate` | Validate PR against stage rules |
| 🔵 GET | `/api/v1/teams` | List Teams |
| 🔵 GET | `/api/v1/teams` | List Teams |
| 🟢 POST | `/api/v1/teams` | Create Team |
| 🟢 POST | `/api/v1/teams` | Create Team |
| 🔴 DELETE | `/api/v1/teams/{team_id}` | Delete Team |
| 🔴 DELETE | `/api/v1/teams/{team_id}` | Delete Team |
| 🔵 GET | `/api/v1/teams/{team_id}` | Get Team |
| 🔵 GET | `/api/v1/teams/{team_id}` | Get Team |
| 🟠 PATCH | `/api/v1/teams/{team_id}` | Update Team |
| 🟠 PATCH | `/api/v1/teams/{team_id}` | Update Team |
| 🔵 GET | `/api/v1/teams/{team_id}/members` | List Team Members |
| 🔵 GET | `/api/v1/teams/{team_id}/members` | List Team Members |
| 🟢 POST | `/api/v1/teams/{team_id}/members` | Add Team Member |
| 🟢 POST | `/api/v1/teams/{team_id}/members` | Add Team Member |
| 🔴 DELETE | `/api/v1/teams/{team_id}/members/{user_id}` | Remove Team Member |
| 🔴 DELETE | `/api/v1/teams/{team_id}/members/{user_id}` | Remove Team Member |
| 🟠 PATCH | `/api/v1/teams/{team_id}/members/{user_id}` | Update Member Role |
| 🟠 PATCH | `/api/v1/teams/{team_id}/members/{user_id}` | Update Member Role |
| 🔵 GET | `/api/v1/teams/{team_id}/stats` | Get Team Statistics |
| 🔵 GET | `/api/v1/teams/{team_id}/stats` | Get Team Statistics |
| 🔵 GET | `/api/v1/telemetry/dashboard` | Get Dashboard Metrics |
| 🔵 GET | `/api/v1/telemetry/dashboard` | Get Dashboard Metrics |
| 🟢 POST | `/api/v1/telemetry/events` | Track Event |
| 🟢 POST | `/api/v1/telemetry/events` | Track Event |
| 🟢 POST | `/api/v1/telemetry/events/batch` | Track Events Batch |
| 🟢 POST | `/api/v1/telemetry/events/batch` | Track Events Batch |
| 🔵 GET | `/api/v1/telemetry/funnels/{funnel_name}` | Get Funnel Metrics |
| 🔵 GET | `/api/v1/telemetry/funnels/{funnel_name}` | Get Funnel Metrics |
| 🔵 GET | `/api/v1/telemetry/health` | Telemetry Health |
| 🔵 GET | `/api/v1/telemetry/health` | Telemetry Health |
| 🔵 GET | `/api/v1/telemetry/interfaces` | Get Interface Breakdown |
| 🔵 GET | `/api/v1/telemetry/interfaces` | Get Interface Breakdown |
| 🟢 POST | `/api/v1/timeline/{event_id}/override/approve` | Approve override |
| 🟢 POST | `/api/v1/timeline/{event_id}/override/reject` | Reject override |
| 🟢 POST | `/api/v1/timeline/{event_id}/override/request` | Request override |
| 🟢 POST | `/api/v1/triage/analyze` | Analyze For Triage |
| 🟢 POST | `/api/v1/triage/analyze` | Analyze For Triage |
| 🔵 GET | `/api/v1/triage/sla-breaches` | Get Sla Breaches |
| 🔵 GET | `/api/v1/triage/sla-breaches` | Get Sla Breaches |
| 🔵 GET | `/api/v1/triage/stats` | Get Triage Statistics |
| 🔵 GET | `/api/v1/triage/stats` | Get Triage Statistics |
| 🟢 POST | `/api/v1/triage/{feedback_id}/apply` | Apply Triage Decision |
| 🟢 POST | `/api/v1/triage/{feedback_id}/apply` | Apply Triage Decision |
| 🟢 POST | `/api/v1/triage/{feedback_id}/auto-triage` | Auto Triage Feedback |
| 🟢 POST | `/api/v1/triage/{feedback_id}/auto-triage` | Auto Triage Feedback |
| 🔵 GET | `/api/v1/triage/{feedback_id}/sla` | Get Sla Status |
| 🔵 GET | `/api/v1/triage/{feedback_id}/sla` | Get Sla Status |
| 🔵 GET | `/api/v1/vcr` | List VCRs |
| 🔵 GET | `/api/v1/vcr` | List VCRs |
| 🟢 POST | `/api/v1/vcr` | Create VCR |
| 🟢 POST | `/api/v1/vcr` | Create VCR |
| 🟢 POST | `/api/v1/vcr/auto-generate` | AI-assisted VCR generation |
| 🟢 POST | `/api/v1/vcr/auto-generate` | AI-assisted VCR generation |
| 🔵 GET | `/api/v1/vcr/stats/{project_id}` | Get VCR statistics |
| 🔵 GET | `/api/v1/vcr/stats/{project_id}` | Get VCR statistics |
| 🔴 DELETE | `/api/v1/vcr/{vcr_id}` | Delete VCR |
| 🔴 DELETE | `/api/v1/vcr/{vcr_id}` | Delete VCR |
| 🔵 GET | `/api/v1/vcr/{vcr_id}` | Get VCR |
| 🔵 GET | `/api/v1/vcr/{vcr_id}` | Get VCR |
| 🟡 PUT | `/api/v1/vcr/{vcr_id}` | Update VCR |
| 🟡 PUT | `/api/v1/vcr/{vcr_id}` | Update VCR |
| 🟢 POST | `/api/v1/vcr/{vcr_id}/approve` | Approve VCR |
| 🟢 POST | `/api/v1/vcr/{vcr_id}/approve` | Approve VCR |
| 🟢 POST | `/api/v1/vcr/{vcr_id}/reject` | Reject VCR |
| 🟢 POST | `/api/v1/vcr/{vcr_id}/reject` | Reject VCR |
| 🟢 POST | `/api/v1/vcr/{vcr_id}/reopen` | Reopen rejected VCR |
| 🟢 POST | `/api/v1/vcr/{vcr_id}/reopen` | Reopen rejected VCR |
| 🟢 POST | `/api/v1/vcr/{vcr_id}/submit` | Submit VCR for approval |
| 🟢 POST | `/api/v1/vcr/{vcr_id}/submit` | Submit VCR for approval |
| 🟢 POST | `/api/v1/vibecoding/batch` | Batch calculate Vibecoding Index |
| 🟢 POST | `/api/v1/vibecoding/calculate` | Calculate Vibecoding Index |
| 🟢 POST | `/api/v1/vibecoding/calibrate` | Submit calibration feedback |
| 🔵 GET | `/api/v1/vibecoding/health` | Signals engine health check |
| 🔵 GET | `/api/v1/vibecoding/stats` | Get index statistics |
| 🔵 GET | `/api/v1/vibecoding/thresholds` | Get index thresholds |
| 🔵 GET | `/api/v1/vibecoding/{submission_id}` | Get cached Vibecoding Index |
| 🔵 GET | `/health` | Health Check |
| 🔵 GET | `/health/ready` | Readiness Check |
| 🔵 GET | `/metrics` | Metrics |
| 🟢 POST | `/ws/broadcast/project/{project_id}` | Broadcast To Project |
| 🔵 GET | `/ws/stats` | Get Websocket Stats |

