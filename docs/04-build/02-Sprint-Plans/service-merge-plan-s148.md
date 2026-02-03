# Service Merge Plan - Sprint 148

**Sprint**: S148 - Service Consolidation
**Date**: February 11, 2026
**Status**: 📋 APPROVED
**Author**: Claude AI (Opus 4.5)

---

## Overview

Based on the [Service Boundary Audit Report](../04-Analysis/service-boundary-audit-s148.md), this document details the merge execution plan.

**Scope Adjustment**: Original plan targeted 164→140 services. Actual: 170→166 services (-4).

---

## Merge Schedule

| Day | Task | Services | Impact | Status |
|-----|------|----------|--------|--------|
| Day 1 | Audit | N/A | Report generated | ✅ DONE |
| Day 2 | GitHub Checks Merge | 2 → 1 | LOW (2 test files) | ⏳ |
| Day 3 | AGENTS.md Merge | 2 → 1 | LOW (1 route file) | ⏳ |
| Day 4 | Dead Code + Cleanup | -2 files | LOW | ⏳ |
| Day 5 | Documentation + Release | N/A | N/A | ⏳ |

---

## Day 2: GitHub Checks Merge

### Target
```
github_checks_service.py (706 LOC) [V1 - Sprint 79]
    ↓ MERGE INTO
github_check_run_service.py (889 LOC) [V2 - Sprint 82]
```

### Files Affected
| File | Action |
|------|--------|
| `backend/app/services/github_checks_service.py` | DELETE after merge |
| `backend/app/services/github_check_run_service.py` | UPDATE - add V1 functions |
| `backend/tests/unit/test_github_check_run_service.py` | UPDATE - add V1 tests |
| `backend/tests/unit/test_check_run_blocking.py` | KEEP (already uses V2) |

### Merge Strategy
1. Review V1 functions not present in V2
2. Copy unique functions to V2 with `# Legacy (Sprint 79)` comments
3. Add deprecation notice to V1 (don't delete immediately)
4. Update any imports in other files
5. Run tests

### V1 Functions to Migrate
- `create_check_run()` - Similar in V2
- `update_check_run()` - Similar in V2
- `list_check_runs()` - May not exist in V2
- Exception classes: `GitHubChecksError`, etc.

### Exit Criteria
- [ ] All V1 functions available in V2
- [ ] All V1 tests pass using V2
- [ ] github_checks_service.py marked deprecated
- [ ] No production regressions

---

## Day 3: AGENTS.md Merge

### Target
```
agents_md_service.py (545 LOC) [Generation]
agents_md_validator.py (484 LOC) [Validation]
    ↓ MERGE INTO
agents_md_manager.py (~900 LOC) [Unified]
```

### Files Affected
| File | Action |
|------|--------|
| `backend/app/services/agents_md_service.py` | MERGE → agents_md_manager.py |
| `backend/app/services/agents_md_validator.py` | DELETE after merge |
| `backend/app/api/routes/agents.py` | UPDATE imports |
| `backend/tests/unit/services/test_agents_md_validator.py` | MERGE into test_agents_md_manager.py |
| `backend/tests/e2e/test_agents_md_e2e.py` | UPDATE imports |

### Merge Strategy
1. Create new `agents_md_manager.py`
2. Move AgentsMdService class as-is
3. Move AgentsMdValidator class as-is
4. Add unified interface: `AgentsMdManager` combining both
5. Update imports in routes
6. Run tests

### New File Structure
```python
# agents_md_manager.py

class AgentsMdValidator:
    """Validation logic from agents_md_validator.py"""
    ...

class AgentsMdGenerator:
    """Generation logic from agents_md_service.py"""
    ...

class AgentsMdManager:
    """Unified manager combining generation + validation"""
    def __init__(self):
        self.validator = AgentsMdValidator()
        self.generator = AgentsMdGenerator()

    def generate_and_validate(self, ...): ...
    def validate(self, ...): ...
    def generate(self, ...): ...
```

### Exit Criteria
- [ ] All generation functions work
- [ ] All validation functions work
- [ ] API routes use new manager
- [ ] All tests pass
- [ ] Old files deleted

---

## Day 4: Dead Code + Cleanup

### Dead Code Removal
| File | Reason | Action |
|------|--------|--------|
| `backend/app/services/infrastructure/__init__.py` | Empty module (31 LOC) | DELETE |
| `backend/app/services/conformance_check_service.py` | Superseded by validators/ | VERIFY & DELETE if unused |

### Template Rename (for clarity)
| Old Name | New Name | Reason |
|----------|----------|--------|
| `base_template.py` | Keep | Clear (2026 version) |
| `base_templates.py` | `prompt_base_templates.py` | Disambiguate from base_template.py |

### Import Cleanup
```bash
# Run autoflake to remove unused imports
autoflake --in-place --remove-all-unused-imports --recursive backend/app/

# Run isort to organize imports
isort backend/app/

# Verify no circular imports
python -c "from app.services import *"
```

### Exit Criteria
- [ ] Dead code files removed
- [ ] Template files renamed
- [ ] All imports clean (autoflake)
- [ ] No circular imports
- [ ] All tests pass

---

## Day 5: Documentation + Release

### Documentation Updates
1. Update `AGENTS.md` with new service structure
2. Update `docs/02-design/SERVICE-ARCHITECTURE.md` (create if not exists)
3. Create `docs/04-build/03-Migration-Guides/service-consolidation-guide.md`
4. Update `CHANGELOG.md`

### Verification
```bash
# Full test suite
pytest backend/tests/ -v

# Coverage check (target: ≥95%)
pytest backend/tests/ --cov=backend/app --cov-report=term-missing

# Lint check
ruff check backend/app/
mypy backend/app/

# Import time (target: <100ms)
time python -c "from app.services import *"
```

### Release
```bash
# Commit all changes
git add .
git commit -m "feat(Sprint 148): Service Consolidation - 170→166 services

- Merge github_checks_service.py into github_check_run_service.py
- Merge agents_md_service.py + agents_md_validator.py into agents_md_manager.py
- Remove dead code: infrastructure/__init__.py
- Clean up unused imports

Sprint 148: -4 services (-2.4% reduction)
All tests passing, 95%+ coverage maintained

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# Tag release
git tag -a sprint-148-v1.0.0 -m "Sprint 148: Service Consolidation"

# Push
git push origin main --tags
```

### Exit Criteria
- [ ] All documentation complete
- [ ] All tests passing (≥95% coverage)
- [ ] Release tagged
- [ ] Staging deployment successful

---

## Risk Mitigation

### Rollback Plan
If any merge causes production issues:

```bash
# Revert to pre-merge state
git revert HEAD~N  # Where N is number of merge commits

# Or restore specific files
git checkout HEAD~1 -- backend/app/services/github_checks_service.py
git checkout HEAD~1 -- backend/app/services/agents_md_validator.py
```

### Testing Strategy
- Run tests after EACH merge (not batched)
- If any test fails, stop and investigate
- Keep old files with deprecation notice until next sprint

---

## Metrics Tracking

| Metric | Before | Target | Actual |
|--------|--------|--------|--------|
| Service Count | 170 | 166 | - |
| Test Coverage | 95% | ≥95% | - |
| Test Duration | ~120s | ~115s | - |
| Import Time | ~150ms | <100ms | - |
| Dead Code (Vulture) | ~50 warnings | 0 | - |

---

## Approval

**CTO Approval**: Required before execution

- [ ] Audit report reviewed
- [ ] Merge plan approved
- [ ] Risk assessment accepted
- [ ] Timeline approved

---

**Created**: February 11, 2026
**Next Review**: February 12, 2026 (Day 2 kickoff)
