# SASE Week 6 - Iteration 1 Sprint Plan (SOP Generator Pilot)

**Date**: Monday, Jan 20, 2026
**Branch**: `feature/sop-generator-pilot`
**Goal**: First SOP generated (Deployment) and reviewed by Friday Jan 24 EOD
**Primary KPI**: Generation time p95 < 30s

## Outcomes (Definition of Done for Week 6)

- TC-001 passes end-to-end (Generate Deployment SOP) from UI and API.
- Generated SOP includes 5/5 mandatory sections (purpose, scope, procedure, roles, quality criteria).
- MRP is generated and retrievable for the SOP.
- VCR can be submitted (at least APPROVED) and status is retrievable.
- Latency measurement exists (logs or response field) and is captured for TC-001.

## Scope (Week 6)

**Must-have**
- Stabilize the existing SOP Generator flow and ensure the happy path works.
- Add missing validation, error handling, and minimal observability (latency + provider/model used).

**Nice-to-have**
- Improve UI polish (loading states, errors, markdown preview formatting).

## Work Breakdown (Suggested)

### Backend - BE #1 (AI Integration)

1) **BE-W6-001: Verify Ollama generation end-to-end**
- Run `POST /api/sop/generate` with deployment input (TC-001).
- Confirm provider/model used, fallback behavior, and generation time.
- **Acceptance**: Returns 201 with non-empty sections and `generation_time_ms` populated.

2) **BE-W6-002: Prompt tuning pass (Deployment SOP)**
- Tune prompt to reliably output all 5 sections and keep it concise.
- **Acceptance**: 3 consecutive runs produce 5/5 sections.

3) **BE-W6-003: Add/verify latency logging**
- Ensure generation latency is logged consistently (include sop_id, provider, model).
- **Acceptance**: Logs include a single structured line per generation.

### Backend - BE #2 (Validation & Quality)

4) **BE-W6-004: Request validation + friendly errors**
- Validate `sop_type` is one of supported; enforce `workflow_description` min length.
- **Acceptance**: Invalid input yields 422/400 with clear message.

5) **BE-W6-005: Smoke tests for core endpoints**
- Cover: types, generate, get sop, get mrp, post vcr, get vcr, list, health.
- **Acceptance**: Manual smoke checklist completed (record outputs + timings).

### Frontend - FE

6) **FE-W6-001: Form validation + user feedback**
- Validate `sop_type` selection and workflow description length.
- **Acceptance**: Prevent submit until valid; show inline error.

7) **FE-W6-002: Loading + error states**
- Disable submit while generating, show progress, display API error.
- **Acceptance**: No double-submits; errors are visible and actionable.

8) **FE-W6-003: SOP preview readability**
- Ensure markdown is readable; basic formatting; optional code block styling.
- **Acceptance**: Preview renders without broken layout.

### Tech Lead

9) **TL-W6-001: PR hygiene + merge discipline**
- Keep PRs small; review within 24h; enforce evidence in PR description.
- **Acceptance**: PR template includes: test run, TC reference, timing.

10) **TL-W6-002: Friday demo package**
- Prepare a 5-minute demo flow: generate SOP -> view MRP -> submit VCR.
- **Acceptance**: Demo script exists and can be executed on demand.

## Day Plan (Recommended)

- **Mon (post-kickoff)**: Everyone boots env; run TC-001 once; confirm blockers.
- **Tue**: Backend stabilizes generation + logs; FE adds validation + loading.
- **Wed**: Smoke all endpoints; tighten prompt; fix edge cases.
- **Thu**: Dry-run demo; capture timing; clean up UX.
- **Fri**: Demo + checkpoint; record p95 timing from 3 runs.

## Risks / Blockers

- Ollama endpoint unreachable or slow: confirm early; use Claude fallback only for unblock.
- Latency >30s: reduce prompt length, lower output verbosity, ensure model selection correct.
- Schema drift between FE and API: validate request/response types during TC-001.

## Links

- Kickoff agenda: [docs/04-build/02-Sprint-Plans/SASE-WEEK-6-KICKOFF-AGENDA-JAN20.md](SASE-WEEK-6-KICKOFF-AGENDA-JAN20.md)
- Technical readiness: [docs/04-build/02-Sprint-Plans/SASE-WEEK-6-TECHNICAL-READINESS.md](SASE-WEEK-6-TECHNICAL-READINESS.md)
- BRS: [docs/04-build/05-SASE-Artifacts/BRS-PILOT-001-NQH-Bot-SOP-Generator.yaml](../05-SASE-Artifacts/BRS-PILOT-001-NQH-Bot-SOP-Generator.yaml)
- LPS: [docs/04-build/05-SASE-Artifacts/LPS-PILOT-001-SOP-Generator.yaml](../05-SASE-Artifacts/LPS-PILOT-001-SOP-Generator.yaml)
