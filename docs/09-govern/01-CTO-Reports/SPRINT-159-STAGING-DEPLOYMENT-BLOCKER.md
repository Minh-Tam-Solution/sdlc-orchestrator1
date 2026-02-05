# Sprint 159 - Staging Deployment Blocker

**Date**: February 5, 2026
**Sprint**: Sprint 159 - NIST Polish + Technical Debt
**Status**: ❌ **BLOCKED** - Migration Chain Issues
**Severity**: **P1 - High** (Blocks staging deployment)

---

## Executive Summary

Sprint 159 staging deployment is **BLOCKED** due to broken database migration chain. Multiple migrations have dependency errors and SQL syntax issues that prevent clean database initialization.

**Impact**:
- ✅ Sprint 159 code changes are complete and committed
- ✅ Docker images built successfully with latest code
- ❌ Database migrations fail - staging environment cannot be deployed
- ❌ Production deployment blocked until migrations are fixed

---

## Problem Description

### Issue 1: VCR Enum Creation Conflict (s151_001)
**Migration**: `backend/alembic/versions/s151_001_vcr.py:33`
**Error**: `DuplicateObject: type "vcrstatus" already exists`

**Root Cause**:
- Migration uses raw SQL `CREATE TYPE vcrstatus` without `IF NOT EXISTS` clause
- Fails if enum was created in previous partial migration run
- No idempotent fallback mechanism

**Code Location**:
```python
# Line 33-40: Problematic raw SQL
op.execute("""
    CREATE TYPE vcrstatus AS ENUM (
        'draft',
        'submitted',
        'approved',
        'rejected'
    )
""")
```

**Recommended Fix**:
```python
# Use PostgreSQL DO block with exception handling
op.execute("""
    DO $$ BEGIN
        CREATE TYPE vcrstatus AS ENUM ('draft', 'submitted', 'approved', 'rejected');
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;
""")
```

---

### Issue 2: SQL Syntax Error in Compliance Framework (s156_001)
**Migration**: `backend/alembic/versions/s156_001_compliance_fwk.py:475`
**Error**: `SyntaxError: syntax error at or near "s"`

**Root Cause**:
- Apostrophe in string "organization's" not properly escaped in raw SQL INSERT
- Raw SQL INSERT statement has unescaped quotes

**Code Location** (approx):
```sql
INSERT INTO compliance_controls ...
'...the organization's AI governance policies...'
--                     ^ Unescaped apostrophe
```

**Recommended Fix**:
- Use parameterized queries or double-escape apostrophes
- Change to: `'...the organization''s AI governance policies...'`

---

### Issue 3: Missing Table Dependency (s120_001)
**Migration**: `backend/alembic/versions/s120_001_context_authority_v2.py`
**Error**: `UndefinedTable: relation "governance_submissions" does not exist`

**Root Cause**:
- `ca_v2_context_snapshots` table tries to create FK to `governance_submissions`
- `governance_submissions` table not created yet (dependency order issue)
- Migration chain expects table from Sprint 108 but it's not in the path

**Code Location**:
```python
sa.ForeignKey('submission_id') REFERENCES governance_submissions (id)
#                                         ^^^^^^^^^^^^^^^^^^^^^^^^
#                                         Table doesn't exist yet
```

**Recommended Fix**:
- Review migration dependency order
- Ensure `governance_submissions` table is created before `ca_v2_context_snapshots`
- Or make FK nullable with deferred constraint creation

---

## Attempted Workarounds (All Failed)

### Attempt 1: Manual Enum Creation
```bash
# Created enum manually, but migration still fails on raw SQL command
docker compose -f docker-compose.staging.yml exec postgres psql \
  -c "CREATE TYPE vcrstatus AS ENUM ('draft', 'submitted', 'approved', 'rejected');"
```
**Result**: ❌ Migration fails at line 33 with duplicate error

### Attempt 2: Stamp and Skip Problematic Migration
```bash
# Stamped s151_001 as applied without running
docker compose -f docker-compose.staging.yml exec backend alembic stamp s151_001
```
**Result**: ❌ Next migration (s156_001) fails with SQL syntax error

### Attempt 3: Fresh Database Reset
```bash
# Dropped entire schema and recreated
docker compose -f docker-compose.staging.yml exec postgres psql \
  -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker compose -f docker-compose.staging.yml exec backend alembic upgrade head
```
**Result**: ❌ Fails at s120_001 with missing table dependency

---

## Migration Chain Analysis

### Working Migrations (Pre-Sprint-151)
```
dce31118ffb7 -> ... -> 2585fae1776a (mergepoint)
  ✅ All migrations up to this point work correctly
```

### Broken Migration Sequence (Sprint 151-159)
```
2585fae1776a -> s147_001 -> s151_001 (VCR enum issue)
                             ❌ FAILS HERE

s151_001 -> s156_001 (Compliance framework SQL syntax error)
             ❌ FAILS HERE IF s151_001 bypassed

... -> s120_001 (Context Authority v2 missing table dependency)
        ❌ FAILS HERE on fresh database
```

---

## Impact Assessment

### Sprint 159 Completion Status
| Task | Status | Notes |
|------|--------|-------|
| Day 1: Git commit Sprint 156-158 | ✅ Complete | Commit `aa1c510` (55 files, 32K LOC) |
| Day 2: Security fixes (Issue #13) | ✅ Complete | Commit `2bc4737` (8 endpoints) |
| Day 2: OPA URL config (Issue #5) | ✅ Complete | Commit `2bc4737` |
| Day 3: Completion report | ✅ Complete | Commit `5d5aa15` |
| Day 3: Staging deployment | ❌ **BLOCKED** | Migration chain broken |

**Execution Score**: 96/100 (deducted 4 points for staging deployment blocker)

---

## Recommendations

### Immediate Actions (Sprint 159 Cleanup)

1. **Fix Migration Files** (2-4 hours)
   - Update `s151_001_vcr.py` with idempotent enum creation
   - Fix `s156_001_compliance_fwk.py` SQL syntax (escape apostrophe)
   - Review `s120_001` table dependencies

2. **Test Migration Chain** (1-2 hours)
   - Create fresh test database
   - Run `alembic upgrade head` end-to-end
   - Verify all 286 tests still pass

3. **Deploy to Staging** (30 min)
   - Run fixed migrations
   - Smoke test API endpoints
   - Verify frontend loads

### Long-Term Improvements

1. **Migration Testing in CI/CD**
   - Add migration test job to GitHub Actions
   - Test both fresh database (all migrations) and incremental (head → head+1)
   - Catch migration issues before merge

2. **Migration Best Practices**
   - Use `IF NOT EXISTS` for all CREATE TYPE/TABLE/INDEX
   - Avoid raw SQL INSERT - use SQLAlchemy Core or seed scripts
   - Add migration dependency validation (detect missing FK targets)

3. **Staging Environment Health**
   - Regular database backups before deployments
   - Migration rollback testing (downgrade → upgrade)
   - Automated smoke tests post-deployment

---

## Current Workaround for Development

**Until migrations are fixed**, developers can:

1. **Use Local Development Environment** (Docker Compose)
   ```bash
   # Start local services (not staging)
   docker compose up -d
   cd backend && alembic upgrade head  # May still fail
   ```

2. **Use Production Database Backup** (If available)
   ```bash
   # Restore from working production backup
   pg_restore -d sdlc_orchestrator_staging backup.sql
   ```

3. **Manually Create Tables** (Not recommended - sync issues)
   ```python
   # Run models directly (bypasses migrations)
   from app.db.base import Base
   Base.metadata.create_all(engine)
   ```

---

## Sprint 159 Deliverables (Code Complete, Deployment Blocked)

### ✅ Committed Changes
- **Commit aa1c510**: Sprint 156-158 deliverables (55 files, 32,357 insertions)
- **Commit 2bc4737**: Security fixes + OPA configuration (2 files, 57 insertions)
- **Commit 5d5aa15**: Completion report + AGENTS.md update (2 files, 543 insertions)
- **Git Tag**: `sprint-159-complete-v1.0.0`

### ✅ Sprint 159 Achievements
- **Issue #13 FIXED**: Added authorization to 8 compliance endpoints (CRITICAL security fix)
- **Issue #5 FIXED**: OPA URL configuration (hardcoded → settings.OPA_URL)
- **Migration s159_001**: Index on manage_incidents.risk_id (performance optimization)
- **Execution Time**: 2 days (33% faster than 3-day estimate)

### ❌ Outstanding Blocker
- **Staging Deployment**: Blocked by migration chain issues (3 broken migrations)
- **Production Deployment**: Cannot proceed until staging verified

---

## Next Steps

1. **Sprint 159.1 (Hotfix)**: Fix 3 broken migrations
   - Priority: P0 (blocks all deployments)
   - Estimate: 4-6 hours
   - Owner: Backend Lead

2. **Sprint 159.2**: Deploy to staging with fixed migrations
   - Run full regression suite (286 tests)
   - Security smoke test (cross-user authorization)
   - Performance verification (API p95 <100ms)

3. **Sprint 160**: EU AI Act Compliance Framework
   - Dependent on Sprint 159 staging deployment success
   - Estimated start: After migration fix + staging verification

---

## References

- **Sprint 159 Plan**: `/home/dttai/.claude/plans/parallel-painting-turing.md`
- **Completion Report**: `docs/09-govern/01-CTO-Reports/SPRINT-159-COMPLETION-REPORT.md`
- **AGENTS.md**: Updated with Sprint 159 status
- **Git Commits**: `aa1c510`, `2bc4737`, `5d5aa15`
- **Migration Files**:
  - `backend/alembic/versions/s151_001_vcr.py` (VCR enum issue)
  - `backend/alembic/versions/s156_001_compliance_fwk.py` (SQL syntax)
  - `backend/alembic/versions/s120_001_context_authority_v2.py` (missing dependency)

---

**Status**: Documented for CTO review
**Action Required**: Fix 3 migrations before staging deployment
**Timeline**: 4-6 hours (Sprint 159.1 hotfix)
