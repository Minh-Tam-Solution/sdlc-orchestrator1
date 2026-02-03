# Sprint 148: Service Consolidation
## Merge Service Boundaries + Dead Code Removal

**Sprint ID**: S148  
**Phase**: Phase 1 - Consolidation  
**Dates**: February 11-15, 2026 (5 days)  
**Status**: 📋 PLANNED  
**Priority**: P0 - Tech Debt Reduction  
**Budget**: $6,000  
**Team**: 2 FTE (Backend + DevOps)

---

## Executive Summary

**Objective**: Reduce service count from 164 → 140 by merging duplicate boundaries and removing dead code.

**Success Criteria**:
- [ ] Service count: 164 → 140 (-24 services, -15% reduction)
- [ ] Test coverage maintained at ≥95%
- [ ] Zero P0 regressions
- [ ] All service imports updated
- [ ] Documentation updated

**Business Impact**:
- **Maintainability**: -24 services = -15% maintenance overhead
- **Onboarding**: Clearer service boundaries for new developers
- **Performance**: Reduced import graph complexity
- **Testing**: Faster test suite execution

---

## Day-by-Day Plan

### Day 1: Service Boundary Audit + Merge Plan

**Objectives**:
- Analyze 164 service files for duplication
- Identify merge candidates
- Create merge plan with risk assessment

**Tasks**:

#### Analysis (4 hours)
- [ ] Run static analysis on `backend/app/services/` (164 files)
- [ ] Identify duplicate service boundaries:
  - Auth services (3 files) → 1 consolidated
  - Gate services (5 files) → 2 consolidated
  - Evidence services (4 files) → 2 consolidated
  - Context services (6 files) → 3 consolidated
- [ ] Calculate coupling metrics (import graph analysis)
- [ ] Identify dead code (unused functions, unreferenced classes)

#### Planning (4 hours)
- [ ] Create merge plan with 4 phases:
  1. Phase A: Auth services (3 → 1)
  2. Phase B: Gate services (5 → 2)
  3. Phase C: Evidence services (4 → 2)
  4. Phase D: Context services (6 → 3)
- [ ] Document breaking changes
- [ ] Create rollback plan
- [ ] Risk assessment (High/Medium/Low for each merge)

**Deliverables**:
- `docs/04-build/04-Analysis/service-boundary-audit-s148.md` (audit report)
- `docs/04-build/02-Sprint-Plans/service-merge-plan-s148.md` (merge plan)
- Risk matrix spreadsheet

**Exit Criteria**:
- [ ] All 24 merge candidates identified
- [ ] Merge plan approved by CTO
- [ ] Risk assessment complete

### Day 2: Phase A + B - Auth & Gate Service Merges

**Objectives**:
- Merge auth services (3 → 1)
- Merge gate services (5 → 2)
- Total: 8 → 3 services

**Tasks**:

#### Phase A: Auth Services (3 hours)
- [ ] Merge `auth_service.py`, `auth_helper.py`, `auth_validator.py` → `auth_service.py`
- [ ] Consolidate duplicate functions:
  - `validate_token()` (2 implementations) → 1 canonical
  - `hash_password()` (2 implementations) → 1 with bcrypt
  - `verify_mfa()` (3 implementations) → 1 with TOTP
- [ ] Update imports in 25 dependent files
- [ ] Run auth test suite (45 tests)

#### Phase B: Gate Services (4 hours)
- [ ] Merge `gate_service.py`, `gate_executor.py`, `gate_validator.py`, `gate_helper.py`, `gate_cache.py` → `gate_service.py` (core), `gate_executor.py` (execution)
- [ ] Move gate execution logic to `gate_executor.py`
- [ ] Move validation to `gate_service.py`
- [ ] Consolidate caching logic
- [ ] Update imports in 40 dependent files
- [ ] Run gate test suite (68 tests)

#### Verification (1 hour)
- [ ] Run full backend test suite
- [ ] Check import errors
- [ ] Verify API endpoints still functional

**Deliverables**:
- `backend/app/services/auth_service.py` (consolidated, ~600 LOC)
- `backend/app/services/gate_service.py` (core, ~800 LOC)
- `backend/app/services/gate_executor.py` (execution, ~400 LOC)
- Updated import statements in 65 files

**Exit Criteria**:
- [ ] 8 → 3 services (5 files removed)
- [ ] All tests passing (113/113)
- [ ] Zero import errors

### Day 3: Phase C + D - Evidence & Context Service Merges

**Objectives**:
- Merge evidence services (4 → 2)
- Merge context services (6 → 3)
- Total: 10 → 5 services

**Tasks**:

#### Phase C: Evidence Services (3 hours)
- [ ] Merge `evidence_service.py`, `evidence_validator.py`, `evidence_storage.py`, `evidence_helper.py` → `evidence_service.py` (core), `evidence_storage.py` (storage)
- [ ] Move MinIO logic to `evidence_storage.py`
- [ ] Move validation to `evidence_service.py`
- [ ] Update imports in 30 dependent files
- [ ] Run evidence test suite (52 tests)

#### Phase D: Context Services (4 hours)
- [ ] Merge `context_service.py`, `context_authority.py`, `context_cache.py`, `context_validator.py`, `context_helper.py`, `context_snapshot.py` → `context_service.py` (core), `context_authority.py` (authority), `context_snapshot.py` (snapshot)
- [ ] Consolidate authority logic
- [ ] Move snapshot logic to separate service
- [ ] Update imports in 45 dependent files
- [ ] Run context test suite (38 tests)

#### Verification (1 hour)
- [ ] Run full backend test suite
- [ ] Integration test: E2E evidence workflow
- [ ] Integration test: E2E context authority workflow

**Deliverables**:
- `backend/app/services/evidence_service.py` (core, ~700 LOC)
- `backend/app/services/evidence_storage.py` (storage, ~300 LOC)
- `backend/app/services/context_service.py` (core, ~800 LOC)
- `backend/app/services/context_authority.py` (authority, ~500 LOC)
- `backend/app/services/context_snapshot.py` (snapshot, ~400 LOC)
- Updated import statements in 75 files

**Exit Criteria**:
- [ ] 10 → 5 services (5 files removed)
- [ ] All tests passing (90/90)
- [ ] Zero regressions

### Day 4: Dead Code Removal + Import Cleanup

**Objectives**:
- Remove dead code from remaining services
- Clean up unused imports
- Optimize import graph

**Tasks**:

#### Dead Code Removal (4 hours)
- [ ] Run Vulture for dead code detection
- [ ] Remove unused functions (target: 50+ functions)
- [ ] Remove unused classes (target: 10+ classes)
- [ ] Remove commented-out code
- [ ] Services to review:
  - `project_service.py` (8 unused functions)
  - `user_service.py` (5 unused functions)
  - `organization_service.py` (6 unused functions)
  - `sprint_service.py` (4 unused functions)
  - 20+ other services

#### Import Cleanup (3 hours)
- [ ] Run `autoflake` to remove unused imports
- [ ] Run `isort` to organize imports
- [ ] Verify no circular imports (using `pytest --import-mode=importlib`)
- [ ] Update all `__init__.py` files

#### Verification (1 hour)
- [ ] Run `mypy` for type checking
- [ ] Run `pylint` for code quality
- [ ] Run full test suite

**Deliverables**:
- ~500 lines of dead code removed
- All imports organized (isort)
- Zero circular import warnings
- Vulture report: 0 dead code warnings

**Exit Criteria**:
- [ ] Dead code removed from 30+ services
- [ ] Import graph optimized
- [ ] All linters passing

### Day 5: Documentation + Verification + Tag Release

**Objectives**:
- Complete documentation
- Final verification
- Tag release

**Tasks**:

#### Documentation (3 hours)
- [ ] Update `docs/02-design/SERVICE-ARCHITECTURE.md`
  - New service boundaries diagram
  - Import graph visualization
  - Service responsibility matrix
- [ ] Update API documentation (Swagger/OpenAPI)
- [ ] Create migration guide: `docs/04-build/03-Migration-Guides/service-consolidation-guide.md`
- [ ] Update `AGENTS.md` with new service structure
- [ ] Update `CHANGELOG.md`

#### Verification (3 hours)
- [ ] Run full test suite (target: ≥95% coverage)
- [ ] Performance test: Service import time (<100ms)
- [ ] Load test: API endpoints still <500ms p95
- [ ] Integration test: E2E workflows (auth, gates, evidence, context)
- [ ] Check for regressions (compare with Sprint 147 baseline)

#### Release (2 hours)
- [ ] Code review by CTO
- [ ] Fix any critical issues
- [ ] Merge to main branch
- [ ] Tag release: `sprint-148-v1.0.0`
- [ ] Deploy to staging environment
- [ ] Smoke test staging

**Deliverables**:
- Updated service architecture documentation
- Migration guide
- Sprint 148 completion report
- Git tag: `sprint-148-v1.0.0`

**Exit Criteria**:
- [ ] All documentation complete
- [ ] All tests passing (≥95% coverage)
- [ ] Release tagged
- [ ] Staging deployment successful

---

## Key Performance Indicators (KPIs)

| Metric | Baseline (S147) | Target (S148) | Success Criteria |
|--------|-----------------|---------------|------------------|
| **Service Count** | 164 | 140 | -24 services (-15%) |
| **Lines of Code** | ~45,000 | ~43,500 | -1,500 LOC (-3.3%) |
| **Dead Code (Vulture)** | ~500 warnings | 0 warnings | 100% cleanup |
| **Circular Imports** | 0 | 0 | Maintained |
| **Test Coverage** | 95% | ≥95% | Maintained |
| **Test Suite Duration** | ~120s | ~110s | -10s faster |
| **Service Import Time** | ~150ms | <100ms | -50ms |

---

## Service Consolidation Matrix

### Before (164 services)

| Category | Count | Examples |
|----------|-------|----------|
| Auth | 3 | `auth_service`, `auth_helper`, `auth_validator` |
| Gate | 5 | `gate_service`, `gate_executor`, `gate_validator`, `gate_helper`, `gate_cache` |
| Evidence | 4 | `evidence_service`, `evidence_validator`, `evidence_storage`, `evidence_helper` |
| Context | 6 | `context_service`, `context_authority`, `context_cache`, `context_validator`, `context_helper`, `context_snapshot` |
| Other | 146 | Project, User, Organization, Sprint, etc. |

### After (140 services)

| Category | Count | Examples |
|----------|-------|----------|
| Auth | 1 | `auth_service` (consolidated) |
| Gate | 2 | `gate_service` (core), `gate_executor` (execution) |
| Evidence | 2 | `evidence_service` (core), `evidence_storage` (storage) |
| Context | 3 | `context_service` (core), `context_authority` (authority), `context_snapshot` (snapshot) |
| Other | 132 | Project, User, Organization, Sprint, etc. (14 dead files removed) |

**Total Reduction**: -24 services (-15%)

---

## Risk Management

| Risk | Impact | Probability | Mitigation | Status |
|------|--------|-------------|------------|--------|
| **Breaking changes in API** | High | Low | Comprehensive tests + rollback plan | ⏳ |
| **Import errors after merge** | High | Medium | Automated import updates + verification | ⏳ |
| **Test failures** | Medium | Medium | Run tests after each merge phase | ⏳ |
| **Performance regression** | Medium | Low | Performance benchmarks before/after | ⏳ |
| **Dead code removal breaks prod** | High | Low | Vulture analysis + manual review | ⏳ |

---

## Dependencies

### Upstream (Blockers)
- ✅ Sprint 147 complete (V1/V2 consolidation, telemetry baseline)
- ✅ All Sprint 147 tests passing

### Downstream (Depends on Sprint 148)
- Sprint 149: Vibecoding V1/V2 consolidation requires clean service boundaries
- Sprint 150: Phase 1 verification requires service count baseline

---

## Technical Decisions

### TDD-001: Service Consolidation Principles

**Decision**: Consolidate services by domain responsibility, not by file size

**Principles**:
1. **Single Responsibility**: Each service should have ONE clear domain responsibility
2. **Bounded Context**: Service boundaries align with DDD bounded contexts
3. **Minimal Dependencies**: Reduce coupling between services
4. **Testability**: Each service should be independently testable

**Anti-patterns to avoid**:
- God services (>1000 LOC)
- Anemic services (just pass-through)
- Circular dependencies

### TDD-002: Dead Code Removal Strategy

**Decision**: Use Vulture + manual review, remove only 100% unused code

**Strategy**:
1. Run Vulture to identify unused code
2. Manual review each warning (false positives common)
3. Remove only code with 0 references
4. Keep code if:
   - Used in tests
   - Part of public API (even if unused internally)
   - Documented as future feature

---

## Success Metrics Summary

### Primary Metrics
- ✅ Service count: 164 → 140 (-15%)
- ✅ Dead code removed: ~500 LOC
- ✅ Test coverage maintained: ≥95%

### Secondary Metrics
- ✅ Import graph optimized
- ✅ Test suite faster: ~110s (was ~120s)
- ✅ Documentation complete

### Business Metrics
- **Developer Productivity**: Faster onboarding (fewer services to learn)
- **Maintainability**: -15% maintenance overhead
- **Code Quality**: Zero dead code warnings

---

## Retrospective Template (Post-Sprint)

*To be filled after Sprint 148 completion (Feb 15, 2026)*

### What Went Well
- TBD

### What Could Be Improved
- TBD

### Action Items for Sprint 149
- TBD

### Key Learnings
- TBD

---

## References

- [ROADMAP-147-170.md](ROADMAP-147-170.md) - Overall roadmap
- [V1-V2-CONSOLIDATION-PLAN.md](V1-V2-CONSOLIDATION-PLAN.md) - API migration strategy
- [SERVICE-ARCHITECTURE.md](../../02-design/SERVICE-ARCHITECTURE.md) - Service architecture
- Vulture documentation: https://github.com/jendrikseipp/vulture

---

**Sprint Owner**: CTO  
**Created**: February 3, 2026  
**Next Sprint Planning**: February 15, 2026 (Sprint 149)
