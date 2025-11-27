# E2E Test Scenarios - SDLC Orchestrator

**Version**: 1.0.0
**Date**: November 27, 2025
**Status**: ACTIVE - STAGE 03 (BUILD)
**Authority**: QA Lead + CTO Approved
**Framework**: SDLC 4.9 Complete Lifecycle

---

## 1. Overview

This document defines comprehensive End-to-End (E2E) test scenarios for SDLC Orchestrator, covering all 5 Functional Requirements (FR1-FR5) and critical user journeys.

### Test Environment

| Component | URL | Credentials |
|-----------|-----|-------------|
| Frontend | http://localhost:3000 | - |
| Backend API | http://localhost:8000 | - |
| API Docs | http://localhost:8000/api/docs | - |
| MinIO Console | http://localhost:9001 | minioadmin / minioadmin |
| OPA | http://localhost:8181 | - |

### Test Accounts

| Role | Email | Password | Permissions |
|------|-------|----------|-------------|
| Platform Admin | admin@sdlc-orchestrator.io | Admin@123 | Full access, superuser |
| CTO | cto@bflow.vn | password123 | Approve G2, G3 gates |
| PM | pm@bflow.vn | password123 | Create projects, manage gates |
| Developer | dev@bflow.vn | password123 | Submit evidence, view dashboards |
| QA Lead | qa@bflow.vn | password123 | Review evidence, test policies |

---

## 2. User Journey Test Scenarios

### 2.1 Authentication Flow (FR: Security)

#### TC-AUTH-001: Email/Password Login
```
GIVEN: User is on login page (http://localhost:3000/login)
WHEN: User enters valid email and password
  - Email: admin@sdlc-orchestrator.io
  - Password: Admin@123
AND: User clicks "Sign In" button
THEN: User is redirected to Dashboard (/)
AND: User sees welcome message with their name
AND: JWT access_token is stored in localStorage
```

#### TC-AUTH-002: Invalid Credentials
```
GIVEN: User is on login page
WHEN: User enters invalid credentials
  - Email: admin@sdlc-orchestrator.io
  - Password: wrongpassword
AND: User clicks "Sign In" button
THEN: Error message "Invalid email or password" is displayed
AND: User remains on login page
```

#### TC-AUTH-003: Session Expiry & Refresh
```
GIVEN: User is logged in with valid session
WHEN: Access token expires (after 1 hour)
AND: User performs any authenticated action
THEN: System automatically refreshes token using refresh_token
AND: User action completes successfully without re-login
```

#### TC-AUTH-004: Logout
```
GIVEN: User is logged in
WHEN: User clicks "Sign Out" in header
THEN: User is redirected to login page
AND: JWT tokens are cleared from storage
AND: Refresh token is revoked on server
```

#### TC-AUTH-005: Protected Route Access
```
GIVEN: User is NOT logged in
WHEN: User tries to access /projects directly
THEN: User is redirected to /login
AND: After login, user is redirected back to /projects
```

---

### 2.2 Dashboard Overview (FR4: Real-Time Dashboard)

#### TC-DASH-001: View Dashboard Statistics
```
GIVEN: User is logged in as admin@sdlc-orchestrator.io
WHEN: User navigates to Dashboard (/)
THEN: User sees 4 stat cards:
  - Total Projects: 3
  - Active Gates: 3
  - Pending Approvals: 3
  - Pass Rate: 100%
```

#### TC-DASH-002: Recent Gate Activity
```
GIVEN: User is on Dashboard
THEN: User sees "Recent Gate Activity" section
AND: Shows up to 5 most recent gates:
  | Gate Name | Project Name | Status |
  |-----------|--------------|--------|
  | G1 | MTC Internal Tool - SDLC Automation | pending |
  | G1 | MTC Internal Tool - SDLC Automation | pending |
  | G1 | BFlow Workflow Automation - v3.0 | pending |
  | G0.2 | BFlow Workflow Automation - v3.0 | passed |
  | G1 | NQH E-commerce Platform - Phase 2 | pending |
```

#### TC-DASH-003: Quick Actions
```
GIVEN: User is on Dashboard
THEN: User sees Quick Actions section with:
  - "Create New Project" link → /projects/new
  - "Upload Evidence" link → /evidence
  - "Manage Policies" link → /policies
```

---

### 2.3 Project Management (FR1: Quality Gate Management)

#### TC-PROJ-001: View Projects List
```
GIVEN: User is logged in
WHEN: User navigates to Projects (/projects)
THEN: User sees list of 3 projects:
  | Project Name | Current Stage | Status | Progress |
  |--------------|---------------|--------|----------|
  | BFlow Workflow Automation - v3.0 | WHY | pending | 20% |
  | NQH E-commerce Platform - Phase 2 | WHY | pending | 20% |
  | MTC Internal Tool - SDLC Automation | WHY | pending | 30% |
```

#### TC-PROJ-002: View Project Detail
```
GIVEN: User is on Projects page
WHEN: User clicks on "BFlow Workflow Automation - v3.0"
THEN: User sees project detail page with:
  - Project name and description
  - Current stage: WHY
  - List of gates with their status
  - Gate timeline visualization
```

#### TC-PROJ-003: Create New Project
```
GIVEN: User is on Projects page
WHEN: User clicks "New Project" button
THEN: Project creation form appears with fields:
  - Name (required)
  - Slug (auto-generated from name)
  - Description (optional)
AND: User fills form:
  - Name: "Demo Project - Test Scenarios"
  - Description: "Project for E2E testing"
AND: User clicks "Create Project"
THEN: New project is created
AND: User is redirected to project detail page
AND: Project appears in projects list
```

---

### 2.4 Gate Evaluation (FR1: Quality Gate Management)

#### TC-GATE-001: View Gate Status
```
GIVEN: User is on project detail page
THEN: User sees gate cards showing:
  | Gate | Stage | Type | Status |
  |------|-------|------|--------|
  | G0.1 | WHY | Problem Definition | APPROVED |
  | G0.2 | WHY | Solution Diversity | APPROVED |
  | G1 | WHAT | Planning Complete | PENDING_APPROVAL |
```

#### TC-GATE-002: Create New Gate
```
GIVEN: User is on project detail page
WHEN: User clicks "Add Gate" button
THEN: Gate creation form appears
AND: User fills:
  - Gate Name: G2
  - Gate Type: DESIGN
  - Stage: 02 (HOW)
  - Description: "Architecture design complete"
AND: User clicks "Create Gate"
THEN: Gate is created with status PENDING
AND: Gate appears in project gates list
```

#### TC-GATE-003: Submit Gate for Evaluation
```
GIVEN: User has a gate in PENDING status
AND: User has uploaded required evidence
WHEN: User clicks "Submit for Evaluation"
THEN: Gate status changes to PENDING_APPROVAL
AND: OPA policy evaluation is triggered
AND: Evaluation result is displayed
```

#### TC-GATE-004: Approve Gate (CTO)
```
GIVEN: User is logged in as cto@bflow.vn
AND: Gate G1 is in PENDING_APPROVAL status
WHEN: User navigates to gate detail
AND: User reviews evidence
AND: User clicks "Approve Gate"
AND: User enters approval comment
THEN: Gate status changes to APPROVED
AND: Gate approval is recorded in audit log
AND: Project progress is updated
```

#### TC-GATE-005: Reject Gate with Feedback
```
GIVEN: User is logged in as cto@bflow.vn
AND: Gate G2 is in PENDING_APPROVAL status
WHEN: User clicks "Reject Gate"
AND: User enters rejection reason: "Missing security review document"
THEN: Gate status changes to REJECTED
AND: Rejection reason is recorded
AND: Notification sent to project owner
```

---

### 2.5 Evidence Vault (FR2: Evidence Vault)

#### TC-EVID-001: View Evidence List
```
GIVEN: User is logged in
WHEN: User navigates to Evidence Vault (/evidence)
THEN: User sees evidence list (currently empty state)
AND: "Upload Evidence" button is visible
```

#### TC-EVID-002: Upload Evidence File
```
GIVEN: User is on Evidence Vault page
WHEN: User clicks "Upload Evidence"
THEN: Upload dialog appears
AND: User selects file: "architecture-diagram.pdf" (5MB)
AND: User fills metadata:
  - Title: "System Architecture Document"
  - Gate: G2 - Design Ready
  - Project: BFlow Workflow Automation
  - Description: "4-layer architecture diagram"
AND: User clicks "Upload"
THEN: File is uploaded to MinIO
AND: SHA256 hash is calculated and stored
AND: Evidence appears in list with metadata
```

#### TC-EVID-003: Verify Evidence Integrity
```
GIVEN: Evidence "architecture-diagram.pdf" exists in vault
WHEN: User clicks "Verify Integrity"
THEN: System recalculates SHA256 hash
AND: Compares with stored hash
AND: Shows "Integrity Verified" status
```

#### TC-EVID-004: Download Evidence
```
GIVEN: Evidence exists in vault
WHEN: User clicks "Download"
THEN: File downloads successfully
AND: Download is recorded in audit log
```

#### TC-EVID-005: Search Evidence
```
GIVEN: Multiple evidence files exist
WHEN: User enters search query: "architecture"
THEN: Results show matching evidence
AND: Results include evidence from "architecture-diagram.pdf"
```

---

### 2.6 Policy Management (FR5: Policy Pack Library)

#### TC-POL-001: View Policy Packs
```
GIVEN: User is on Policies page (/policies)
THEN: User sees policy packs list:
  | Pack Name | Description | Policies | Status |
  |-----------|-------------|----------|--------|
  | SDLC 4.9 Standard | Default policy pack | 110 | Active |
  | Security Baseline | OWASP ASVS Level 2 | 45 | Inactive |
  | Compliance (SOC 2) | SOC 2 Type II | 32 | Inactive |
```

#### TC-POL-002: View Policy Pack Detail
```
GIVEN: User is on Policies page
WHEN: User clicks "View" on "SDLC 4.9 Standard"
THEN: User sees list of 110 policies organized by stage:
  - Stage 00 (WHY): 8 policies
  - Stage 01 (WHAT): 12 policies
  - Stage 02 (HOW): 15 policies
  - ... (etc)
```

#### TC-POL-003: Activate Policy Pack
```
GIVEN: "Security Baseline" pack is inactive
WHEN: User clicks "Activate"
THEN: Pack status changes to "Active"
AND: Policies are applied to future gate evaluations
```

#### TC-POL-004: Create Custom Policy
```
GIVEN: User is on Policies page
WHEN: User clicks "Create Policy"
THEN: Policy editor appears
AND: User enters:
  - Name: "Code Coverage Threshold"
  - Description: "Require 95% code coverage"
  - Stage: 04 (VERIFY)
  - Rego code:
    ```rego
    package sdlc.verify.coverage

    default allow = false

    allow {
      input.coverage >= 95
    }
    ```
AND: User clicks "Save"
THEN: Custom policy is created
AND: Policy appears in custom policies list
```

---

### 2.7 AI Context Engine (FR3: AI Context Engine)

#### TC-AI-001: Generate Gate Checklist
```
GIVEN: User is on gate G1 detail page
WHEN: User clicks "Generate Checklist with AI"
THEN: AI generates stage-specific checklist:
  - [ ] Problem statement documented
  - [ ] User personas defined
  - [ ] Market research completed
  - [ ] Competitive analysis done
  - [ ] Success metrics defined
```

#### TC-AI-002: AI Evidence Review Suggestion
```
GIVEN: User is uploading evidence for G2 gate
WHEN: AI analyzes uploaded document
THEN: AI provides suggestions:
  - "Document covers architecture design"
  - "Missing: Performance requirements section"
  - "Recommendation: Add scalability considerations"
```

#### TC-AI-003: AI Policy Recommendation
```
GIVEN: User is creating new project
WHEN: User enters project description
THEN: AI recommends relevant policy packs:
  - "Based on your project type, we recommend:"
  - "SDLC 4.9 Standard" (matched: 95%)
  - "Security Baseline" (matched: 78%)
```

---

## 3. API Test Scenarios

### 3.1 Authentication API

#### TC-API-AUTH-001: POST /api/v1/auth/login
```bash
# Request
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@sdlc-orchestrator.io","password":"Admin@123"}'

# Expected Response (200 OK)
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### TC-API-AUTH-002: GET /api/v1/auth/me
```bash
# Request
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer ${TOKEN}"

# Expected Response (200 OK)
{
  "id": "a0000000-0000-0000-0000-000000000001",
  "email": "admin@sdlc-orchestrator.io",
  "full_name": "Platform Admin",
  "is_active": true,
  "is_superuser": true
}
```

#### TC-API-AUTH-003: POST /api/v1/auth/refresh
```bash
# Request
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"eyJ..."}'

# Expected Response (200 OK)
{
  "access_token": "eyJ...(new token)",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

### 3.2 Dashboard API

#### TC-API-DASH-001: GET /api/v1/dashboard/stats
```bash
# Request
curl http://localhost:8000/api/v1/dashboard/stats \
  -H "Authorization: Bearer ${TOKEN}"

# Expected Response (200 OK)
{
  "total_projects": 3,
  "active_gates": 3,
  "pending_approvals": 3,
  "pass_rate": 100
}
```

#### TC-API-DASH-002: GET /api/v1/dashboard/recent-gates
```bash
# Request
curl http://localhost:8000/api/v1/dashboard/recent-gates \
  -H "Authorization: Bearer ${TOKEN}"

# Expected Response (200 OK)
[
  {
    "id": "...",
    "gate_name": "G1",
    "project_name": "MTC Internal Tool - SDLC Automation",
    "status": "pending",
    "updated_at": "2025-11-17T14:57:30.638574"
  },
  ...
]
```

---

### 3.3 Projects API

#### TC-API-PROJ-001: GET /api/v1/projects
```bash
# Request
curl http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer ${TOKEN}"

# Expected Response (200 OK)
[
  {
    "id": "...",
    "name": "BFlow Workflow Automation - v3.0",
    "description": "...",
    "current_stage": "WHY",
    "gate_status": "pending",
    "progress": 20,
    "created_at": "2025-10-25T10:23:17.321700",
    "updated_at": "2025-11-14T10:23:17.321703"
  },
  ...
]
```

#### TC-API-PROJ-002: POST /api/v1/projects (Create)
```bash
# Request
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Demo Project - E2E Test",
    "slug": "demo-project-e2e-test",
    "description": "Project for E2E testing scenarios"
  }'

# Expected Response (201 Created)
{
  "id": "...",
  "name": "Demo Project - E2E Test",
  "slug": "demo-project-e2e-test",
  "description": "Project for E2E testing scenarios",
  "owner_id": "...",
  "is_active": true,
  "created_at": "..."
}
```

#### TC-API-PROJ-003: GET /api/v1/projects/{id}
```bash
# Request
curl http://localhost:8000/api/v1/projects/4289d0fc-3c83-4d0e-8f4d-1e3aab7a4dda \
  -H "Authorization: Bearer ${TOKEN}"

# Expected Response (200 OK)
{
  "id": "4289d0fc-3c83-4d0e-8f4d-1e3aab7a4dda",
  "name": "BFlow Workflow Automation - v3.0",
  "description": "...",
  "current_stage": "WHY",
  "gates": [
    {
      "id": "...",
      "gate_name": "G0.1",
      "gate_type": "PROBLEM_DEFINITION",
      "stage": "WHY",
      "status": "APPROVED"
    },
    ...
  ]
}
```

---

### 3.4 Gates API

#### TC-API-GATE-001: GET /api/v1/gates
```bash
# Request
curl http://localhost:8000/api/v1/gates \
  -H "Authorization: Bearer ${TOKEN}"

# Expected Response (200 OK)
[
  {
    "id": "...",
    "gate_name": "G1",
    "project_id": "...",
    "stage": "WHY",
    "status": "PENDING_APPROVAL"
  },
  ...
]
```

#### TC-API-GATE-002: POST /api/v1/gates (Create)
```bash
# Request
curl -X POST http://localhost:8000/api/v1/gates \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "gate_name": "G2",
    "gate_type": "DESIGN",
    "project_id": "4289d0fc-3c83-4d0e-8f4d-1e3aab7a4dda",
    "stage": "02",
    "description": "Architecture design complete"
  }'

# Expected Response (201 Created)
{
  "id": "...",
  "gate_name": "G2",
  "status": "PENDING"
}
```

#### TC-API-GATE-003: POST /api/v1/gates/{id}/evaluate
```bash
# Request
curl -X POST http://localhost:8000/api/v1/gates/{gate_id}/evaluate \
  -H "Authorization: Bearer ${TOKEN}"

# Expected Response (200 OK)
{
  "gate_id": "...",
  "status": "PENDING_APPROVAL",
  "evaluation_result": {
    "passed_policies": 8,
    "failed_policies": 2,
    "warnings": 1,
    "details": [...]
  }
}
```

#### TC-API-GATE-004: POST /api/v1/gates/{id}/approve
```bash
# Request (CTO only)
curl -X POST http://localhost:8000/api/v1/gates/{gate_id}/approve \
  -H "Authorization: Bearer ${CTO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"comment": "All requirements met, approved for next stage"}'

# Expected Response (200 OK)
{
  "gate_id": "...",
  "status": "APPROVED",
  "approved_by": "cto@bflow.vn",
  "approved_at": "2025-11-27T..."
}
```

---

### 3.5 Evidence API

#### TC-API-EVID-001: POST /api/v1/evidence/upload
```bash
# Request
curl -X POST http://localhost:8000/api/v1/evidence/upload \
  -H "Authorization: Bearer ${TOKEN}" \
  -F "file=@architecture-diagram.pdf" \
  -F "gate_id=..." \
  -F "title=System Architecture Document" \
  -F "description=4-layer architecture diagram"

# Expected Response (201 Created)
{
  "id": "...",
  "title": "System Architecture Document",
  "file_name": "architecture-diagram.pdf",
  "file_size": 5242880,
  "mime_type": "application/pdf",
  "sha256_hash": "abc123...",
  "storage_path": "s3://evidence-vault/...",
  "uploaded_at": "..."
}
```

#### TC-API-EVID-002: GET /api/v1/evidence/{id}/verify
```bash
# Request
curl http://localhost:8000/api/v1/evidence/{evidence_id}/verify \
  -H "Authorization: Bearer ${TOKEN}"

# Expected Response (200 OK)
{
  "evidence_id": "...",
  "integrity_status": "VERIFIED",
  "stored_hash": "abc123...",
  "calculated_hash": "abc123...",
  "verified_at": "..."
}
```

---

### 3.6 Policies API

#### TC-API-POL-001: GET /api/v1/policies
```bash
# Request
curl http://localhost:8000/api/v1/policies \
  -H "Authorization: Bearer ${TOKEN}"

# Expected Response (200 OK)
[
  {
    "id": "...",
    "name": "SDLC 4.9 Standard",
    "description": "Default policy pack for SDLC 4.9 methodology",
    "policies_count": 110,
    "is_active": true
  },
  ...
]
```

#### TC-API-POL-002: POST /api/v1/policies/evaluate
```bash
# Request
curl -X POST http://localhost:8000/api/v1/policies/evaluate \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "gate_id": "...",
    "policy_pack_id": "...",
    "input_data": {
      "stage": "WHY",
      "evidence_count": 5,
      "approvers": ["cto@bflow.vn"]
    }
  }'

# Expected Response (200 OK)
{
  "result": "PASS",
  "passed_policies": 8,
  "failed_policies": 0,
  "details": [
    {"policy": "problem_statement_required", "result": "PASS"},
    {"policy": "user_persona_defined", "result": "PASS"},
    ...
  ]
}
```

---

## 4. Performance Test Scenarios

### 4.1 Load Test: Dashboard Stats

#### TC-PERF-001: Dashboard Load Time
```
Target: <1s page load (p95)
Method: 100 concurrent users, 5 minutes duration

Metrics to capture:
- Response time (p50, p95, p99)
- Throughput (requests/second)
- Error rate (%)

Expected:
- p95 response time: <200ms
- Throughput: >500 req/s
- Error rate: <0.1%
```

### 4.2 Load Test: Evidence Upload

#### TC-PERF-002: Concurrent Evidence Upload
```
Target: 50 concurrent uploads (10MB each)
Method: Locust test with 50 users

Expected:
- Upload time (p95): <2s per file
- No upload failures
- MinIO handles concurrent writes
```

### 4.3 Stress Test: Gate Evaluation

#### TC-PERF-003: OPA Policy Evaluation
```
Target: 1000 policy evaluations/second
Method: Evaluate 110 policies per gate

Expected:
- Evaluation time (p95): <100ms
- OPA handles concurrent evaluations
- No policy timeout errors
```

---

## 5. Security Test Scenarios

### 5.1 Authentication Security

#### TC-SEC-001: SQL Injection in Login
```
Input: email = "admin@test.com' OR '1'='1"
Expected: Login fails with "Invalid email" error
Actual: System rejects malformed email
```

#### TC-SEC-002: JWT Token Tampering
```
Action: Modify JWT payload (change user_id)
Expected: 401 Unauthorized response
Actual: Token validation fails
```

#### TC-SEC-003: Rate Limiting
```
Action: Send 100 login requests in 1 second
Expected: Rate limit triggered after 10 requests
Actual: 429 Too Many Requests
```

### 5.2 Authorization Security

#### TC-SEC-004: Cross-Project Access
```
User: dev@bflow.vn (BFlow project member)
Action: Try to access NQH project data
Expected: 403 Forbidden
Actual: Access denied
```

#### TC-SEC-005: Role Escalation
```
User: dev@bflow.vn (Developer role)
Action: Try to approve gate (CTO-only action)
Expected: 403 Forbidden
Actual: Action denied
```

---

## 6. Test Data Requirements

### 6.1 Required Seed Data

See: `DEMO-SEED-DATA.sql` for complete seed data script.

Summary of seed data:
- 5 test users (admin, cto, pm, dev, qa)
- 3 projects (BFlow, NQH, MTC)
- 5 gates across projects
- 10 evidence documents
- 3 policy packs (110+ policies)

### 6.2 Test File Assets

Required test files for evidence upload testing:
- `architecture-diagram.pdf` (5MB)
- `api-specification.yaml` (100KB)
- `test-report.html` (500KB)
- `security-audit.pdf` (2MB)
- `user-guide.docx` (1MB)

---

## 7. Test Execution Checklist

### Pre-Test Setup
- [ ] Docker containers running (all healthy)
- [ ] Seed data loaded
- [ ] Test accounts verified
- [ ] Test files prepared

### Test Execution
- [ ] TC-AUTH-001 through TC-AUTH-005 (Authentication)
- [ ] TC-DASH-001 through TC-DASH-003 (Dashboard)
- [ ] TC-PROJ-001 through TC-PROJ-003 (Projects)
- [ ] TC-GATE-001 through TC-GATE-005 (Gates)
- [ ] TC-EVID-001 through TC-EVID-005 (Evidence)
- [ ] TC-POL-001 through TC-POL-004 (Policies)
- [ ] TC-AI-001 through TC-AI-003 (AI Context)
- [ ] TC-API-* (API Tests)
- [ ] TC-PERF-* (Performance)
- [ ] TC-SEC-* (Security)

### Post-Test
- [ ] Test results documented
- [ ] Bugs logged in issue tracker
- [ ] Test coverage report generated
- [ ] Performance metrics captured

---

## 8. Appendix

### A. Test Environment Setup

```bash
# Start all containers
cd /path/to/SDLC-Orchestrator
docker-compose up -d

# Verify health
docker-compose ps

# Load seed data
psql -h localhost -U sdlc_user -d sdlc_orchestrator -f scripts/seed-demo-data.sql

# Run E2E tests
npm run test:e2e
```

### B. Useful Commands

```bash
# Get fresh JWT token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@sdlc-orchestrator.io","password":"Admin@123"}' \
  | jq -r '.access_token')

# Test dashboard stats
curl -s http://localhost:8000/api/v1/dashboard/stats \
  -H "Authorization: Bearer $TOKEN" | jq

# Test projects list
curl -s http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

**Document Status**: ACTIVE - Ready for QA Testing
**Next Review**: December 1, 2025
**Owner**: QA Lead + CTO
