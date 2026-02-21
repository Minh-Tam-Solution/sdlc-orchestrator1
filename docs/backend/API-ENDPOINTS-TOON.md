# API Endpoints Summary - TOON Format

**Total**: 636 endpoints
**Version**: 1.2.0

## By Method

- GET: 341
- POST: 240
- PUT: 22
- PATCH: 10
- DELETE: 23

## By Service/Tag

- **AGENTS.md**: 16 endpoints
- **AI**: 2 endpoints
- **AI Council**: 10 endpoints
- **AI Detection**: 12 endpoints
- **AI Providers**: 10 endpoints
- **API Keys**: 6 endpoints
- **Admin Panel**: 22 endpoints
- **Agentic Maturity**: 12 endpoints
- **Analytics**: 22 endpoints
- **Analytics V1 (DEPRECATED)**: 15 endpoints
- **Analytics v2**: 8 endpoints
- **Authentication**: 26 endpoints
- **Auto-Generation**: 12 endpoints
- **CEO Dashboard**: 14 endpoints
- **CRP - Consultations**: 16 endpoints
- **Check Runs**: 5 endpoints
- **Codegen**: 58 endpoints
- **Compliance**: 26 endpoints
- **Compliance Validation**: 10 endpoints
- **Context Authority**: 7 endpoints
- **Context Authority V1 (DEPRECATED)**: 7 endpoints
- **Context Authority V2**: 22 endpoints
- **Context Overlay**: 2 endpoints
- **Context Validation**: 8 endpoints
- **Contract Lock**: 14 endpoints
- **Cross-Reference**: 8 endpoints
- **Cross-Reference Validation**: 4 endpoints
- **Dashboard**: 2 endpoints
- **Dependencies**: 10 endpoints
- **Deprecation Monitoring**: 8 endpoints
- **Documentation**: 4 endpoints
- **Dogfooding**: 20 endpoints
- **E2E Testing**: 10 endpoints
- **Evidence**: 3 endpoints
- **Evidence Manifest**: 7 endpoints
- **Evidence Timeline**: 7 endpoints
- **Feedback**: 14 endpoints
- **Feedback Learning**: 22 endpoints
- **Feedback Learning (EP-11)**: 22 endpoints
- **Framework Version**: 12 endpoints
- **Gates**: 24 endpoints
- **Gates Engine**: 16 endpoints
- **GitHub**: 13 endpoints
- **Governance Metrics**: 14 endpoints
- **Governance Mode**: 8 endpoints
- **Governance Specs**: 5 endpoints
- **Governance Vibecoding**: 7 endpoints
- **Grafana Dashboards**: 7 endpoints
- **MCP Analytics**: 10 endpoints
- **MRP - Merge Readiness Protocol**: 18 endpoints
- **MRP - Policy Enforcement**: 4 endpoints
- **Multi-Agent Team Engine**: 20 endpoints
- **Notifications**: 8 endpoints
- **Organization Invitations**: 7 endpoints
- **Organizations**: 6 endpoints
- **Override / VCR**: 9 endpoints
- **Payments**: 5 endpoints
- **Pilot**: 13 endpoints
- **Planning**: 46 endpoints
- **Planning Hierarchy**: 150 endpoints
- **Planning Sub-agent**: 16 endpoints
- **Policies**: 5 endpoints
- **Policy Packs**: 8 endpoints
- **Preview**: 6 endpoints
- **Projects**: 10 endpoints
- **Push Notifications**: 10 endpoints
- **Resource Allocation**: 11 endpoints
- **Retrospective**: 9 endpoints
- **Risk Analysis**: 8 endpoints
- **SAST**: 14 endpoints
- **SDLC Structure**: 6 endpoints
- **SOP Generator**: 16 endpoints
- **Spec Converter**: 7 endpoints
- **Sprint 77**: 3 endpoints
- **Sprint 78**: 39 endpoints
- **Stage Gating**: 7 endpoints
- **Teams**: 10 endpoints
- **Telemetry**: 12 endpoints
- **Templates**: 9 endpoints
- **Tier Management**: 5 endpoints
- **Triage**: 12 endpoints
- **Uncategorized**: 4 endpoints
- **VCR (Version Controlled Resolution)**: 22 endpoints
- **Vibecoding Index**: 7 endpoints
- **WebSocket**: 2 endpoints
- **dashboard**: 2 endpoints
- **doc-cross-reference**: 4 endpoints
- **dogfooding**: 20 endpoints
- **github**: 13 endpoints
- **organization-invitations**: 7 endpoints
- **organizations**: 6 endpoints
- **payments**: 5 endpoints
- **pilot**: 13 endpoints
- **projects**: 10 endpoints
- **spec-converter**: 7 endpoints
- **teams**: 10 endpoints

## Quick Reference

| Method | Path | Summary |
|--------|------|----------|
| POST | `/api/v1/auth/register` | Register |
| POST | `/api/v1/auth/login` | Login |
| POST | `/api/v1/auth/refresh` | Refresh Access Token |
| POST | `/api/v1/auth/logout` | Logout |
| GET | `/api/v1/auth/me` | Get Current User Profile |
| GET | `/api/v1/auth/oauth/{provider}/authorize` | Oauth Authorize |
| POST | `/api/v1/auth/oauth/{provider}/callback` | Oauth Callback |
| POST | `/api/v1/auth/github/device` | Github Device Flow Init |
| POST | `/api/v1/auth/github/token` | Github Device Flow Poll |
| GET | `/api/v1/auth/health` | Auth Health Check |
| POST | `/api/v1/auth/forgot-password` | Forgot Password |
| GET | `/api/v1/auth/verify-reset-token` | Verify Reset Token |
| POST | `/api/v1/auth/reset-password` | Reset Password |
| GET | `/api/v1/gates/{gate_id}` | Get Gate |
| PUT | `/api/v1/gates/{gate_id}` | Update Gate |
| DELETE | `/api/v1/gates/{gate_id}` | Delete Gate |
| GET | `/api/v1/gates/{gate_id}/actions` | Get Gate Actions |
| POST | `/api/v1/gates/{gate_id}/evaluate` | Evaluate Gate |
| POST | `/api/v1/gates/{gate_id}/submit` | Submit Gate |
| POST | `/api/v1/gates/{gate_id}/approve` | Approve Gate |
| POST | `/api/v1/gates/{gate_id}/reject` | Reject Gate |
| POST | `/api/v1/gates/{gate_id}/evidence` | Upload Evidence |
| GET | `/api/v1/gates/{gate_id}/approvals` | Get Gate Approvals |
| GET | `/api/v1/projects/{project_id}/evidence/status` | Get Evidence Status |
| POST | `/api/v1/projects/{project_id}/evidence/validate` | Trigger Evidence Validation |
| GET | `/api/v1/projects/{project_id}/evidence/gaps` | Get Evidence Gaps |
| GET | `/api/v1/projects/{project_id}` | Get Project |
| PUT | `/api/v1/projects/{project_id}` | Update Project |
| DELETE | `/api/v1/projects/{project_id}` | Delete Project |
| PUT | `/api/v1/projects/{project_id}/context` | Update project context (stage, gate, sprint) |
| GET | `/api/v1/projects/{project_id}/context` | Get project context (stage, gate, sprint) |
| POST | `/api/v1/projects/{project_id}/sync` | Sync project metadata from repository files |
| POST | `/api/v1/projects/init` | Initialize SDLC project |
| POST | `/api/v1/projects/{project_id}/migrate-stages` | Migrate project stages to SDLC 5.0.0 |
| POST | `/api/v1/api/v1/github/projects/{project_id}/link` | Link GitHub repository to project |
| DELETE | `/api/v1/api/v1/github/projects/{project_id}/unlink` | Unlink GitHub repository from project |
| GET | `/api/v1/api/v1/github/projects/{project_id}/repository` | Get linked repository for project |
| POST | `/api/v1/api/v1/github/projects/{project_id}/clone` | Clone linked repository |
| GET | `/api/v1/api/v1/github/projects/{project_id}/scan` | Scan cloned repository |
| POST | `/api/v1/projects/{project_id}/validate-structure` | Validate SDLC 5.0.0 structure |
| GET | `/api/v1/projects/{project_id}/validation-history` | Get validation history |
| GET | `/api/v1/projects/{project_id}/compliance-summary` | Get compliance summary |
| GET | `/api/v1/admin/evidence/retention-stats` | Get evidence retention statistics (ADR-027) |
| POST | `/api/v1/admin/evidence/retention-archive` | Trigger evidence archival (ADR-027) |
| POST | `/api/v1/admin/evidence/retention-purge` | Trigger evidence purge (ADR-027) |
| GET | `/api/v1/projects/{project_id}/policy-pack` | Get project's policy pack |
| POST | `/api/v1/projects/{project_id}/policy-pack` | Create or update policy pack |
| DELETE | `/api/v1/projects/{project_id}/policy-pack` | Delete policy pack |
| POST | `/api/v1/projects/{project_id}/policy-pack/rules` | Add policy rule |
| PUT | `/api/v1/projects/{project_id}/policy-pack/rules/{policy_id}` | Update policy rule |
