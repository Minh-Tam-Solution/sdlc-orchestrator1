# Service Boundary Audit Report - Sprint 148

**Sprint**: S148 - Service Consolidation
**Date**: February 11, 2026
**Analyst**: Claude AI (Opus 4.5)
**Status**: ✅ COMPLETE

---

## Executive Summary

**Objective**: Analyze 170 service files to identify merge candidates, dead code, and consolidation opportunities.

**Key Findings**:

| Metric | Value |
|--------|-------|
| **Total Service Files** | 170 |
| **Total Lines of Code** | ~51,000 LOC |
| **Average Service Size** | 300 LOC |
| **Merge Candidates** | 8 services → 4 services (-4) |
| **Dead Code Candidates** | 2 files |
| **Low-Usage Services** | 32 (1 reference only) |

**Revised Target**: 170 → 164 services (-6 services, -3.5% reduction)

> **Note**: Original sprint plan assumed 164 services. Actual count is 170. Adjusted target from 140 to 164.

---

## Service Distribution by Domain

### 1. CODEGEN SUBSYSTEM (62 files, ~6,000 LOC)
**Status**: ✅ Well-structured, no merge candidates

```
codegen/
├── codegen_service.py (orchestrator)
├── provider_registry.py (multi-provider gateway)
├── quality_pipeline.py (4-gate validation)
├── session_manager.py (lifecycle)
├── codegen_cache.py (performance)
├── providers/ (4 LLM providers)
│   ├── ollama_provider.py
│   ├── claude_provider.py
│   ├── deepcode_provider.py
│   └── app_builder_provider.py
├── ir/ (7 IR processors)
├── templates/ (8 framework templates)
├── domains/ (4 Vietnamese domain configs)
└── onboarding/ (vendor flows)
```

### 2. GOVERNANCE SUBSYSTEM (14 files, ~14,000 LOC)
**Status**: ⚠️ Some consolidation opportunities

| Service | LOC | Status |
|---------|-----|--------|
| `gates_engine.py` | 1,073 | Core - KEEP |
| `context_authority_v2.py` | 956 | V2 (preferred) |
| `context_authority.py` | 876 | V1 (deprecation planned) |
| `signals_engine.py` | 1,160 | Vibecoding signals |
| `ceo_dashboard.py` | 1,143 | Dashboard |
| `grafana_dashboards.py` | 1,515 | Monitoring |
| `soft_mode_enforcer.py` | 853 | Advisory mode |
| `full_mode_enforcer.py` | 766 | Strict enforcement |
| `mode_service.py` | 878 | Mode orchestration |

### 3. VALIDATION SUBSYSTEM (11 files)
**Status**: ✅ Excellent plugin architecture - KEEP AS-IS

```
validation/
├── validation_pipeline.py (orchestrator)
├── checkers/ (10 modular checks)
│   ├── documentation_checker.py
│   ├── code_naming_checker.py
│   ├── sase_checker.py
│   └── ... (7 more)
└── validators/ (6 quality validators)
    ├── codegen_quality_validator.py
    ├── coverage_validator.py
    ├── lint_validator.py
    └── ... (3 more)
```

### 4. AI DETECTION SUBSYSTEM (6 files)
**Status**: ✅ Complete, no merge candidates

### 5. POLICY MANAGEMENT (5 services)
**Status**: ✅ Good layering - KEEP SEPARATED

```
policy_service.py (CRUD + evaluation)
├── policy_pack_service.py (Pack management)
├── policy_enforcement_service.py (Per-PR enforcement)
└── opa_policy_service.py (Async OPA caching)
     └── opa_service.py (Sync OPA REST adapter)
```

### 6. GITHUB INTEGRATION (5 services)
**Status**: 🔴 MERGE CANDIDATES

| Service | LOC | Version | Status |
|---------|-----|---------|--------|
| `github_service.py` | 804 | - | Core - KEEP |
| `github_app_service.py` | 1,130 | - | GitHub App - KEEP |
| `github_webhook_service.py` | 840 | - | Webhooks - KEEP |
| `github_checks_service.py` | 706 | V1 (Sprint 79) | **MERGE INTO V2** |
| `github_check_run_service.py` | 889 | V2 (Sprint 82) | Preferred |

### 7. AGENTS.md MANAGEMENT (2 services)
**Status**: 🔴 MERGE CANDIDATES

| Service | LOC | Responsibility |
|---------|-----|----------------|
| `agents_md_service.py` | 545 | Generation |
| `agents_md_validator.py` | 484 | Validation |

**Recommendation**: Merge into single `agents_md_manager.py`

### 8. GATE MANAGEMENT (3 services)
**Status**: 🟡 POTENTIAL MERGE (Medium complexity)

| Service | LOC | Responsibility |
|---------|-----|----------------|
| `gate_service.py` | 473 | Generic CRUD |
| `gate_auto_creation_service.py` | 465 | Auto-creation |
| `sprint_gate_service.py` | 600+ | Sprint-specific |

**Recommendation**: Keep separated but document relationships clearly

### 9. TEMPLATE BASE CLASSES (2 files)
**Status**: 🟡 NAMING CONFUSION

| File | Purpose |
|------|---------|
| `base_template.py` | Abstract class (newer, 2026) |
| `base_templates.py` | Prompt base classes (older) |

**Recommendation**: Rename for clarity or consolidate

---

## Merge Candidates (Priority Order)

### HIGH PRIORITY - Clear Duplicates

#### 1. GitHub Check Services (V1 + V2)
```
github_checks_service.py (706 LOC) [V1, Sprint 79]
    ↓ MERGE INTO
github_check_run_service.py (889 LOC) [V2, Sprint 82]
```

**Reason**: V2 has enforcement modes (ADVISORY/BLOCKING/STRICT), supersedes V1
**Impact**: HIGH - Affects GitHub PR integration
**Complexity**: MEDIUM
**Files to Update**: ~15 imports

#### 2. AGENTS.md Services
```
agents_md_service.py (545 LOC) [Generation]
agents_md_validator.py (484 LOC) [Validation]
    ↓ MERGE INTO
agents_md_manager.py (new, ~900 LOC)
```

**Reason**: Generation and validation are tightly coupled
**Impact**: MEDIUM
**Complexity**: LOW
**Files to Update**: ~8 imports

### MEDIUM PRIORITY - Scheduled Deprecation

#### 3. Context Authority (V1 → V2)
```
context_authority.py (876 LOC) [V1]
    ↓ DEPRECATE (Sprint 149)
context_authority_v2.py (956 LOC) [V2, preferred]
```

**Status**: V2 imports V1, intentional co-existence
**Plan**: V1 deprecation scheduled for Sprint 149
**Impact**: HIGH
**Complexity**: HIGH (requires migration)

### LOW PRIORITY - Naming Only

#### 4. Template Base Classes
```
base_template.py → template_base.py
base_templates.py → prompt_templates_base.py
```

**Reason**: Naming confusion, not functional duplication
**Impact**: LOW
**Complexity**: LOW

---

## Dead Code Candidates

| Service | LOC | References | Recommendation |
|---------|-----|------------|----------------|
| `infrastructure/__init__.py` | 31 | 0 | **REMOVE** (empty module) |
| `conformance_check_service.py` | N/A | 1 | Verify if superseded by validators/ |

---

## Low-Usage Services (1 reference only)

32 services have only 1 reference. Risk of unused code:

| Service | LOC | Usage | Recommendation |
|---------|-----|-------|----------------|
| `cache_service.py` | 300 | 2 refs | Audit |
| `framework_version_service.py` | 424 | 1 ref | KEEP (version mgmt) |
| `vnpay_service.py` | 308 | 1 ref | KEEP (Vietnam SME) |
| `triage_service.py` | 432 | 1 ref | KEEP (issue triage) |
| `agentic_maturity_service.py` | N/A | 1 ref | Verify active |
| `e2e_execution_store.py` | 468 | 1 ref | KEEP (E2E testing) |
| `adr_scanner_service.py` | 536 | 1 ref | KEEP (ADR linkage) |

---

## Coupling Metrics

### High Coupling (>10 dependents)
- `codegen_service.py` - 29 references
- `gates_engine.py` - 17 references
- `settings_service.py` - 5 references
- `audit_service.py` - 5 references

### Low Coupling (<3 dependents)
- 32 services with 1 reference
- 18 services with 2 references

---

## Risk Assessment

| Merge | Impact | Probability | Risk Level | Mitigation |
|-------|--------|-------------|------------|------------|
| GitHub Checks V1→V2 | HIGH | MEDIUM | **YELLOW** | Run full PR test suite |
| AGENTS.md Merge | MEDIUM | LOW | **GREEN** | Unit tests sufficient |
| Context Auth V1 Deprecation | HIGH | HIGH | **RED** | 2-sprint migration plan |
| Template Rename | LOW | LOW | **GREEN** | IDE refactor tools |
| Remove infrastructure/ | LOW | LOW | **GREEN** | Verify no imports |

---

## Revised Sprint 148 Plan

### Original Plan (from sprint doc)
- Target: 164 → 140 services (-24 services, -15%)
- Auth services: 3 → 1
- Gate services: 5 → 2
- Evidence services: 4 → 2
- Context services: 6 → 3

### Actual Plan (based on audit)
- Target: 170 → 164 services (-6 services, -3.5%)
- GitHub checks: 2 → 1 (-1)
- AGENTS.md: 2 → 1 (-1)
- Context Authority: Keep V1+V2 (deprecation Sprint 149)
- Dead code removal: 2 files (-2)
- Template rename: 2 files (no count change)

### Execution Order
1. **Day 1** (Today): ✅ Audit complete
2. **Day 2**: Merge GitHub checks services
3. **Day 3**: Merge AGENTS.md services
4. **Day 4**: Dead code removal + template rename
5. **Day 5**: Documentation + verification + release

---

## Recommendations

### Immediate Actions (Sprint 148)
1. ✅ Complete audit report
2. Merge `github_checks_service.py` → `github_check_run_service.py`
3. Merge `agents_md_service.py` + `agents_md_validator.py` → `agents_md_manager.py`
4. Remove `infrastructure/__init__.py`
5. Rename template files for clarity

### Future Sprints
- **Sprint 149**: Context Authority V1 deprecation
- **Sprint 150**: Audit low-usage services (32 with 1 ref)
- **Sprint 151**: Gate services consolidation (if needed)

---

## Appendix: Service Count Summary

| Category | Before | After | Change |
|----------|--------|-------|--------|
| GitHub Integration | 5 | 4 | -1 |
| AGENTS.md | 2 | 1 | -1 |
| Infrastructure | 1 | 0 | -1 |
| Dead Code | 1 | 0 | -1 |
| **Total** | **170** | **166** | **-4** |

> Note: Conservative target. Actual reduction may be higher after detailed dead code analysis.

---

**Report Complete**: ✅
**Next Step**: Create merge plan for Day 2-4
**CTO Approval Required**: Yes (before execution)
