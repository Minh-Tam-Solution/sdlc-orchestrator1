# Backend 99-Legacy

**Purpose**: Store deprecated backend code scheduled for deletion.

**Policy**:
- Code moved here is **NOT** imported by active code
- Will be **DELETED** after 2 sprints
- Kept for reference only

---

## Contents

### Sprint 148 (Feb 11, 2026)

| File | Reason | Status |
|------|--------|--------|
| ~~`services/github_checks_service.py`~~ | Superseded by `github_check_run_service.py` (V2) | ✅ DELETED (Sprint 149) |

### Sprint 149 (Feb 18, 2026)

*Pending deletion candidates after audit:*
- Context Authority V1 (under evaluation)

---

## Migration Guide

If you need functionality from legacy code:
1. Check if V2/replacement exists
2. If not, create new implementation following current patterns
3. Do NOT copy-paste from legacy (may have outdated patterns)

---

**Created**: Sprint 148 (Feb 11, 2026)
**Owner**: Backend Lead
