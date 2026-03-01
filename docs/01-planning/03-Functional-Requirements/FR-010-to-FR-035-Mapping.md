---
sdlc_version: "6.1.1"
document_type: "FR Gap Mapping"
status: "APPROVED"
sprint: "211"
tier: "STANDARD"
stage: "01 - Planning"
---

# FR-010 to FR-035 — Feature Mapping Document

**Sprint**: 211 (Track F — P1-1 ENT compliance gap audit)
**Date**: February 2026
**Author**: CTO Nguyen Quoc Huy
**Purpose**: Map FR-010 to FR-035 numbers to existing implemented features
**CTO Report**: CTO-RPT-209-001

---

## Context

FRs FR-001 to FR-009 were defined pre-MVP as core capability requirements (authentication, gate engine, evidence vault, etc.) and implemented across Sprints 1-45. FR-010 to FR-035 cover features delivered in Sprints 45-175 but were not retroactively documented as individual FR specs. FR-036+ follow the SDLC 6.1.1 BDD specification format.

This mapping document closes the gap by identifying which features cover FR-010 to FR-035.

---

## Mapping Table

| FR # | Feature | Implemented Sprint | Key Files | Status |
|------|---------|-------------------|-----------|--------|
| FR-010 | OPA Policy Engine Integration | Sprint 43 | `policy_packs/rego/`, `gates_engine.py` | COMPLETE |
| FR-011 | Semgrep SAST Integration | Sprint 43 | `semgrep_service.py`, `sast.py` | COMPLETE |
| FR-012 | Cross-Reference Validation | Sprint 44 | `cross_reference_validation.py` | COMPLETE |
| FR-013 | Auto-Fix Engine (LLM-based) | Sprint 45 | `codegen/error_classifier.py` | COMPLETE |
| FR-014 | IR Processor Service | Sprint 46 | `codegen/codegen_service.py` | COMPLETE |
| FR-015 | Vietnamese Domain Templates | Sprint 47 | `codegen/` templates | COMPLETE |
| FR-016 | 4-Gate Quality Pipeline | Sprint 48 | `codegen/quality_pipeline.py` | COMPLETE |
| FR-017 | Multi-Provider Codegen Gateway | Sprint 45 | `codegen/provider_registry.py` | COMPLETE |
| FR-018 | AI Task Decomposition (ADR-011) | Sprint 26 | `ai_recommendation_service.py` | COMPLETE |
| FR-019 | Context-Aware Requirements (ADR-012) | Sprint 28 | `context_authority_v2.py` | COMPLETE |
| FR-020 | 4-Level Planning Hierarchy (ADR-013) | Sprint 74 | `planning.py` routes | COMPLETE |
| FR-021 | SDLC Structure Validator (ADR-014) | Sprint 30 | `sdlc_structure.py` | COMPLETE |
| FR-022 | VS Code Extension MVP | Sprint 27 | `vscode-extension/` | COMPLETE |
| FR-023 | Evidence Manifest & Hash Chain | Sprint 87 | `evidence_manifest.py` | COMPLETE |
| FR-024 | GitHub Check Runs Integration | Sprint 86 | `check_runs.py` | COMPLETE |
| FR-025 | CLI Token Management | Sprint 85 | `api_keys.py`, `cli-tokens/` | COMPLETE |
| FR-026 | AGENTS.md Dynamic Context | Sprint 85 | `agents.py` routes | COMPLETE |
| FR-027 | MFA Enforcement (ADR-027) | Sprint N+1 | `mfa_middleware.py` | COMPLETE |
| FR-028 | Teams & Organizations RBAC | Sprint 84 | `admin.py`, `organizations.py` | COMPLETE |
| FR-029 | Notifications System | Sprint 153 | `notifications.py` | COMPLETE |
| FR-030 | SASE Artifacts (VCR/CRP/MRP) | Sprint 151-152 | `override.py`, `mrp.py`, `consultations.py` | COMPLETE |
| FR-031 | CEO Dashboard & Analytics | Sprint 175 | `ceo_dashboard.py`, `analytics_v2.py` | COMPLETE |
| FR-032 | Compliance Framework (NIST) | Sprint 156 | `compliance_framework.py` | COMPLETE |
| FR-033 | Governance Mode & Vibecoding | Sprint 160+ | `governance_mode.py`, `governance_vibecoding.py` | COMPLETE |
| FR-034 | Contract Lock (Spec Immutability) | Sprint 53 | `contract_lock.py` | COMPLETE |
| FR-035 | Override / VCR Flow | Sprint 43 | `override.py` | COMPLETE |

---

## Notes

1. **All 26 features (FR-010 to FR-035) are implemented** — no gaps in functional coverage
2. **BDD specs not retroactively created** — features pre-date SDLC 6.1.1 BDD format (FR-036+)
3. **Traceability**: Each feature maps to its sprint plan in `docs/04-build/02-Sprint-Plans/`
4. **Future work**: Consider creating formal BDD specs for high-risk FRs (FR-027 MFA, FR-010 OPA)

---

*Sprint 211 — Track F: FR Gap Mapping (P1-1 ENT compliance)*
