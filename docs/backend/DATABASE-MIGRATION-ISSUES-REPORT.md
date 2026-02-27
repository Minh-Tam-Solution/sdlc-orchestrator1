# 🔴 Database Migration Issues Report

**Date**: 2026-02-21
**Status**: ❌ **CRITICAL** - Backend cannot authenticate
**Root Cause**: Database tables do not exist

---

## 📊 Issue Summary (TOON Format)

```
Services Status:      6/6 running
Backend Health:       ✅ Healthy
PostgreSQL Status:    ✅ Running
Database Connection:  ✅ Connected
Database Tables:      ❌ MISSING
Login Endpoint:       ❌ TIMEOUT (table 'users' not found)
Alembic Migrations:   ❌ BROKEN (KeyError: 's160_001')
```

---

## 🐛 Problem Discovered

### Issue #1: Missing PostgreSQL Container
```
Root Cause: Backend configured to use external postgres-central
Status: ✅ FIXED
Solution: Created postgres-central container
Command: docker run -d --name postgres-central --network ai-net \
          -e POSTGRES_USER=sdlc_user \
          -e POSTGRES_PASSWORD=changeme_secure_password \
          -e POSTGRES_DB=sdlc_orchestrator \
          -p 15432:5432 postgres:15.5-alpine
```

### Issue #2: Database Tables Missing
```
Error: relation "users" does not exist
Root Cause: Alembic migrations not run
Impact: Login endpoint returns 500 error and timeouts
Backend Log:
  (sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError)
  <class 'asyncpg.exceptions.UndefinedTableError'>:
  relation "users" does not exist
```

### Issue #3: Alembic Migration Chain Broken
```
Error: KeyError: 's160_001'
Root Cause: Missing migration file or broken revision chain
Command: docker exec sdlc-backend alembic upgrade head
Result: FAILED
```

---

## 🔍 Root Cause Analysis

### Why Login Fails

**Flow**:
1. User sends POST /api/v1/auth/login
2. Backend queries: `SELECT * FROM users WHERE email = 'admin@sop-generator.vn'`
3. PostgreSQL returns: ERROR - relation "users" does not exist
4. Backend waits for database response (hangs)
5. Request times out after 120 seconds
6. User sees: ReadTimeoutError

### Why Migrations Fail

**Alembic Issue**:
```python
# Migration chain expects:
base → s160_001 → s160_002 → ... → head

# But s160_001 file is missing or incorrectly referenced
# Location: backend/alembic/versions/s160_001_*.py
```

---

## ✅ Solutions

### 🟢 Solution 1: Quick Fix - Manual Schema Creation (5 minutes)

**Step 1: Find latest working migration**
```bash
# List migration files
docker exec sdlc-backend ls -la /app/alembic/versions/ | grep "\.py$"

# Find most recent migration
docker exec sdlc-backend ls -t /app/alembic/versions/*.py | head -1
```

**Step 2: Apply schema directly from models**
```python
# Run inside backend container
docker exec -it sdlc-backend python3 << 'EOF'
from app.database import engine, Base
from app.models import *  # Import all models
import asyncio

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created successfully")

asyncio.run(create_tables())
EOF
```

**Step 3: Create admin user**
```python
docker exec -it sdlc-backend python3 << 'EOF'
from app.database import get_db
from app.models.user import User
from app.core.security import get_password_hash
import asyncio
from sqlalchemy import select

async def create_admin():
    async for db in get_db():
        # Check if user exists
        result = await db.execute(
            select(User).where(User.email == "admin@sop-generator.vn")
        )
        existing = result.scalar_one_or_none()

        if existing:
            print("❌ User already exists")
            return

        # Create admin user
        user = User(
            email="admin@sop-generator.vn",
            password_hash=get_password_hash("AdminPass@2025"),
            full_name="Admin User",
            role="ADMIN",
            is_active=True,
            is_superuser=True
        )
        db.add(user)
        await db.commit()
        print("✅ Admin user created")

asyncio.run(create_admin())
EOF
```

### 🟡 Solution 2: Fix Migration Chain (15 minutes)

**Step 1: Check migration files**
```bash
# Find missing s160_001
docker exec sdlc-backend find /app/alembic/versions -name "*s160*"

# If missing, check git history
git log --all --full-history --oneline -- "backend/alembic/versions/s160*"
```

**Step 2: Restore missing migration**
```bash
# Checkout from previous commit if deleted
git checkout <commit-hash> -- backend/alembic/versions/s160_001_*.py
```

**Step 3: Re-run migrations**
```bash
docker exec sdlc-backend alembic upgrade head
```

### 🔴 Solution 3: Nuclear Option - Fresh Database (30 minutes)

**Step 1: Backup current state**
```bash
docker exec postgres-central pg_dump -U sdlc_user sdlc_orchestrator > backup.sql
```

**Step 2: Drop and recreate database**
```bash
docker exec -it postgres-central psql -U sdlc_user << 'EOF'
DROP DATABASE IF EXISTS sdlc_orchestrator;
CREATE DATABASE sdlc_orchestrator;
\q
EOF
```

**Step 3: Re-run all migrations**
```bash
# Start from base
docker exec sdlc-backend alembic downgrade base
docker exec sdlc-backend alembic upgrade head
```

**Step 4: Seed initial data**
```bash
docker exec sdlc-backend python3 scripts/seed_initial_data.py
```

---

## 🎯 Recommended Approach

**Priority**: Use Solution 1 (Quick Fix)

**Rationale**:
- ✅ Fastest (5 minutes)
- ✅ Works immediately
- ✅ Unblocks API testing
- ⚠️ Bypasses migration system (temporary)

**After Quick Fix**:
1. Test login works
2. Complete API testing with valid credentials
3. Fix migration chain in parallel (Solution 2)
4. Migrate to proper schema (Solution 3) for production

---

## 📝 Step-by-Step Quick Fix

### Part A: Create Database Schema

```bash
# 1. Create all tables from models
docker exec sdlc-backend python3 -c "
from app.database import engine, Base
from app import models
import asyncio

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('✅ All tables created')

asyncio.run(create_all())
"
```

### Part B: Create Admin User

```bash
# 2. Create admin@sop-generator.vn user
docker exec sdlc-backend python3 -c "
from app.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()
try:
    user = User(
        email='admin@sop-generator.vn',
        password_hash=get_password_hash('AdminPass@2025'),
        full_name='Admin User',
        role='ADMIN',
        is_active=True,
        is_superuser=True
    )
    db.add(user)
    db.commit()
    print('✅ Admin user created')
except Exception as e:
    print(f'❌ Error: {e}')
finally:
    db.close()
"
```

### Part C: Test Login

```bash
# 3. Test login
curl -X POST http://localhost:8300/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@sop-generator.vn","password":"AdminPass@2025"}' \
  | python3 -m json.tool
```

**Expected Result**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 900
}
```

---

## 🔧 Alternative: Use Existing Script

If backend has seed script:

```bash
# Check for existing seed scripts
docker exec sdlc-backend ls -la /app/scripts/ | grep seed

# Run seed script
docker exec sdlc-backend python3 /app/scripts/seed_data.py
```

---

## 📊 Expected Outcomes

### After Quick Fix:

| Metric | Before | After |
|--------|--------|-------|
| Login Status | ❌ Timeout | ✅ Success |
| JWT Token | ❌ N/A | ✅ Valid |
| Protected Endpoints | ❌ 401 | ✅ Accessible |
| API Success Rate | 8.2% | 80%+ |

### After Complete Fix:

| Metric | Status |
|--------|--------|
| Migration Chain | ✅ Fixed |
| Database Schema | ✅ Versioned |
| Rollback Support | ✅ Available |
| Production Ready | ✅ Yes |

---

## ⚠️ Known Limitations (Quick Fix)

1. **No Migration History**
   - Tables created directly from models
   - Alembic version table empty
   - Cannot track schema changes

2. **Future Migrations May Fail**
   - Migration chain assumes base state
   - May need to manually stamp revision

3. **Not Production Grade**
   - OK for development/testing
   - MUST fix migration chain before production

---

## 🚀 Next Steps After Fix

1. **Verify Login Works**
   ```bash
   # Test credentials
   python3 scripts/test-all-api-endpoints.py
   ```

2. **Seed Test Data**
   ```bash
   # Create projects, gates, evidence
   docker exec sdlc-backend python3 scripts/seed_test_data.py
   ```

3. **Re-run API Tests**
   ```bash
   # Expected: 80%+ success rate
   python3 scripts/test-all-api-endpoints.py
   ```

4. **Fix Migration Chain** (Parallel task)
   - Identify missing/broken migrations
   - Restore from git history
   - Test full migration path

---

## 📞 If Quick Fix Fails

### Diagnostic Commands:

```bash
# Check database connection
docker exec sdlc-backend python3 -c "
from app.database import engine
import asyncio

async def test():
    async with engine.connect() as conn:
        result = await conn.execute('SELECT 1')
        print('✅ Database connected')

asyncio.run(test())
"

# List tables
docker exec postgres-central psql -U sdlc_user -d sdlc_orchestrator -c "\dt"

# Check user table structure
docker exec postgres-central psql -U sdlc_user -d sdlc_orchestrator -c "\d users"
```

---

**Status**: ⏳ Awaiting Quick Fix Execution
**Priority**: 🔴 P0 - Critical
**Impact**: Blocks all API testing
**ETA**: 5 minutes with Quick Fix

---

**Generated**: 2026-02-21
**Issue**: Database migration failures
**Recommendation**: Execute Quick Fix (Solution 1) immediately
