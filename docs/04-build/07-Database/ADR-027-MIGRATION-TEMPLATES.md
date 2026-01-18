# ADR-027 Phase 1 - Database Migration Templates

**Sprint**: Sprint N+1 (Jan 27 - Feb 7, 2026)
**Purpose**: Ready-to-use Alembic migration templates for Phase 1
**Owner**: BE Lead
**Status**: Ready for implementation

---

## 🎯 Overview

Phase 1 requires **2 database migrations**:

1. **Login Lockout Fields** (SDLC-ADR027-201)
   - Add `failed_login_count` column to users table
   - Add `locked_until` column to users table
   - Create index on `locked_until` for performance

2. **MFA Enforcement Fields** (SDLC-ADR027-401)
   - Add `mfa_setup_deadline` column to users table
   - Add `is_mfa_exempt` column to users table

---

## 📋 Migration Naming Convention

**Format**: `{revision}_{description}.py`

**Examples**:
- `abc123def456_add_login_lockout_fields.py`
- `def456ghi789_add_mfa_enforcement_fields.py`

**Commands**:
```bash
# Generate migration (auto-detect changes)
cd backend
alembic revision --autogenerate -m "add login lockout fields"

# Generate empty migration (manual SQL)
alembic revision -m "add login lockout fields"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

---

## 🔒 Migration 1: Login Lockout Fields

### File Location
```
backend/alembic/versions/
└── XXXXXX_add_login_lockout_fields.py
```

### Migration Template

```python
"""Add login lockout fields to users table

Revision ID: XXXXXX
Revises: YYYYYY
Create Date: 2026-01-27 10:00:00.000000

Purpose:
    Support for ADR-027 Phase 1 - max_login_attempts setting
    Tracks failed login attempts and account lockout status

Changes:
    - Add failed_login_count column (tracks consecutive failures)
    - Add locked_until column (lockout expiry timestamp)
    - Create index on locked_until (performance optimization)

Ticket: SDLC-ADR027-201
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'XXXXXX'
down_revision: Union[str, None] = 'YYYYYY'  # Previous migration
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Apply migration: Add login lockout fields to users table.

    This migration is backward compatible:
    - Default values provided (failed_login_count=0, locked_until=NULL)
    - Existing users unaffected (not locked by default)
    - Can be rolled back safely
    """

    # Add failed_login_count column
    # Default: 0 (no failed attempts)
    # Not nullable (always has a value)
    op.add_column(
        'users',
        sa.Column(
            'failed_login_count',
            sa.Integer(),
            nullable=False,
            server_default='0',
            comment='Number of consecutive failed login attempts'
        )
    )

    # Add locked_until column
    # Default: NULL (not locked)
    # Nullable (NULL = unlocked, timestamp = locked until that time)
    op.add_column(
        'users',
        sa.Column(
            'locked_until',
            sa.DateTime(timezone=True),
            nullable=True,
            comment='Account locked until this timestamp (NULL = not locked)'
        )
    )

    # Create index on locked_until for performance
    # Queries frequently check: WHERE locked_until > NOW()
    op.create_index(
        'idx_users_locked_until',
        'users',
        ['locked_until'],
        unique=False
    )

    print("✅ Added login lockout fields to users table")
    print("   - failed_login_count: INTEGER DEFAULT 0")
    print("   - locked_until: TIMESTAMP NULL")
    print("   - Index: idx_users_locked_until")


def downgrade() -> None:
    """
    Rollback migration: Remove login lockout fields.

    WARNING: This will delete all lockout data!
    - Failed login counts lost
    - Locked accounts will be unlocked
    - Use with caution in production
    """

    # Drop index first (dependencies)
    op.drop_index('idx_users_locked_until', table_name='users')

    # Drop columns
    op.drop_column('users', 'locked_until')
    op.drop_column('users', 'failed_login_count')

    print("⚠️  Rolled back login lockout fields")
    print("   - All lockout data deleted")
    print("   - All accounts unlocked")
```

### Testing the Migration

```bash
# 1. Apply migration (upgrade)
cd backend
alembic upgrade head

# Verify columns exist
psql -U sdlc_user -d sdlc_orchestrator -c "
  SELECT column_name, data_type, is_nullable, column_default
  FROM information_schema.columns
  WHERE table_name = 'users'
    AND column_name IN ('failed_login_count', 'locked_until')
  ORDER BY column_name;
"

# Expected output:
#     column_name      | data_type | is_nullable | column_default
# ---------------------+-----------+-------------+----------------
#  failed_login_count  | integer   | NO          | 0
#  locked_until        | timestamp | YES         | NULL

# Verify index exists
psql -U sdlc_user -d sdlc_orchestrator -c "
  SELECT indexname, indexdef
  FROM pg_indexes
  WHERE tablename = 'users'
    AND indexname = 'idx_users_locked_until';
"

# 2. Test rollback (downgrade)
alembic downgrade -1

# Verify columns removed
psql -U sdlc_user -d sdlc_orchestrator -c "
  SELECT column_name
  FROM information_schema.columns
  WHERE table_name = 'users'
    AND column_name IN ('failed_login_count', 'locked_until');
"

# Expected: No rows (columns removed)

# 3. Re-apply migration
alembic upgrade head
```

### Data Verification Queries

```sql
-- Check default values for existing users
SELECT
  id,
  email,
  failed_login_count,
  locked_until,
  is_active
FROM users
LIMIT 5;

-- Expected:
-- - failed_login_count = 0 for all users
-- - locked_until = NULL for all users

-- Simulate lockout (manual test)
UPDATE users
SET
  failed_login_count = 5,
  locked_until = NOW() + INTERVAL '30 minutes'
WHERE email = 'test@example.com';

-- Verify lockout
SELECT
  email,
  failed_login_count,
  locked_until,
  locked_until > NOW() AS is_locked
FROM users
WHERE email = 'test@example.com';

-- Cleanup test data
UPDATE users
SET
  failed_login_count = 0,
  locked_until = NULL
WHERE email = 'test@example.com';
```

---

## 🛡️ Migration 2: MFA Enforcement Fields

### File Location
```
backend/alembic/versions/
└── YYYYYY_add_mfa_enforcement_fields.py
```

### Migration Template

```python
"""Add MFA enforcement fields to users table

Revision ID: YYYYYY
Revises: XXXXXX
Create Date: 2026-01-29 10:00:00.000000

Purpose:
    Support for ADR-027 Phase 1 - mfa_required setting
    Tracks MFA setup deadline and exemption status

Changes:
    - Add mfa_setup_deadline column (grace period expiry)
    - Add is_mfa_exempt column (admin exemption flag)

Ticket: SDLC-ADR027-401
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'YYYYYY'
down_revision: Union[str, None] = 'XXXXXX'  # Previous migration (lockout fields)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Apply migration: Add MFA enforcement fields to users table.

    This migration is backward compatible:
    - Default values provided (mfa_setup_deadline=NULL, is_mfa_exempt=FALSE)
    - Existing users unaffected (no deadline set yet)
    - Superusers will be automatically exempt via application logic
    - Can be rolled back safely
    """

    # Add mfa_setup_deadline column
    # Default: NULL (no deadline yet)
    # Set to NOW() + 7 days when mfa_required is first enabled
    op.add_column(
        'users',
        sa.Column(
            'mfa_setup_deadline',
            sa.DateTime(timezone=True),
            nullable=True,
            comment='User must set up MFA before this deadline (NULL = no requirement)'
        )
    )

    # Add is_mfa_exempt column
    # Default: FALSE (not exempt)
    # Admin can set to TRUE to exempt specific users from MFA requirement
    op.add_column(
        'users',
        sa.Column(
            'is_mfa_exempt',
            sa.Boolean(),
            nullable=False,
            server_default='false',
            comment='User is exempt from MFA requirement (admin override)'
        )
    )

    # Optional: Create index on mfa_setup_deadline (if queries are slow)
    # op.create_index(
    #     'idx_users_mfa_setup_deadline',
    #     'users',
    #     ['mfa_setup_deadline'],
    #     unique=False
    # )

    print("✅ Added MFA enforcement fields to users table")
    print("   - mfa_setup_deadline: TIMESTAMP NULL")
    print("   - is_mfa_exempt: BOOLEAN DEFAULT FALSE")


def downgrade() -> None:
    """
    Rollback migration: Remove MFA enforcement fields.

    WARNING: This will delete all MFA enforcement data!
    - MFA setup deadlines lost
    - Exemption flags lost
    - Use with caution in production
    """

    # Drop columns
    op.drop_column('users', 'is_mfa_exempt')
    op.drop_column('users', 'mfa_setup_deadline')

    print("⚠️  Rolled back MFA enforcement fields")
    print("   - All MFA enforcement data deleted")
```

### Testing the Migration

```bash
# 1. Apply migration (upgrade)
alembic upgrade head

# Verify columns exist
psql -U sdlc_user -d sdlc_orchestrator -c "
  SELECT column_name, data_type, is_nullable, column_default
  FROM information_schema.columns
  WHERE table_name = 'users'
    AND column_name IN ('mfa_setup_deadline', 'is_mfa_exempt')
  ORDER BY column_name;
"

# Expected output:
#     column_name      | data_type | is_nullable | column_default
# --------------------+-----------+-------------+----------------
#  is_mfa_exempt      | boolean   | NO          | false
#  mfa_setup_deadline | timestamp | YES         | NULL

# 2. Test rollback
alembic downgrade -1

# 3. Re-apply
alembic upgrade head
```

### Data Verification Queries

```sql
-- Check default values for existing users
SELECT
  id,
  email,
  mfa_enabled,
  mfa_setup_deadline,
  is_mfa_exempt,
  is_superuser
FROM users
LIMIT 5;

-- Expected:
-- - mfa_setup_deadline = NULL for all users (no deadline yet)
-- - is_mfa_exempt = FALSE for all users (not exempt)

-- Simulate MFA requirement enabled (set deadline for users without MFA)
UPDATE users
SET mfa_setup_deadline = NOW() + INTERVAL '7 days'
WHERE mfa_enabled = FALSE
  AND is_superuser = FALSE
  AND is_mfa_exempt = FALSE;

-- Verify deadlines set
SELECT
  email,
  mfa_enabled,
  mfa_setup_deadline,
  mfa_setup_deadline > NOW() AS within_grace_period,
  is_mfa_exempt
FROM users
WHERE mfa_enabled = FALSE
LIMIT 5;

-- Simulate admin exempting a user
UPDATE users
SET is_mfa_exempt = TRUE
WHERE email = 'test@example.com';

-- Verify exemption
SELECT
  email,
  is_mfa_exempt,
  mfa_setup_deadline
FROM users
WHERE email = 'test@example.com';

-- Cleanup test data
UPDATE users
SET
  mfa_setup_deadline = NULL,
  is_mfa_exempt = FALSE
WHERE email = 'test@example.com';
```

---

## 🔄 Combined Migration (Alternative)

If you prefer a single migration for both features:

### File: `ZZZZZZ_add_phase1_user_security_fields.py`

```python
"""Add Phase 1 security fields to users table

Revision ID: ZZZZZZ
Revises: XXXXXX
Create Date: 2026-01-27 10:00:00.000000

Purpose:
    Support for ADR-027 Phase 1 - All 4 security settings
    - max_login_attempts: Login lockout fields
    - mfa_required: MFA enforcement fields

Changes:
    - Add failed_login_count (login lockout)
    - Add locked_until (login lockout)
    - Add mfa_setup_deadline (MFA enforcement)
    - Add is_mfa_exempt (MFA enforcement)
    - Create index on locked_until

Tickets: SDLC-ADR027-201, SDLC-ADR027-401
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'ZZZZZZ'
down_revision: Union[str, None] = 'XXXXXX'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply all Phase 1 security fields."""

    # Login lockout fields
    op.add_column(
        'users',
        sa.Column('failed_login_count', sa.Integer(), nullable=False, server_default='0')
    )
    op.add_column(
        'users',
        sa.Column('locked_until', sa.DateTime(timezone=True), nullable=True)
    )
    op.create_index('idx_users_locked_until', 'users', ['locked_until'], unique=False)

    # MFA enforcement fields
    op.add_column(
        'users',
        sa.Column('mfa_setup_deadline', sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        'users',
        sa.Column('is_mfa_exempt', sa.Boolean(), nullable=False, server_default='false')
    )

    print("✅ Added all Phase 1 security fields")


def downgrade() -> None:
    """Rollback all Phase 1 security fields."""

    # Drop index
    op.drop_index('idx_users_locked_until', table_name='users')

    # Drop all columns
    op.drop_column('users', 'is_mfa_exempt')
    op.drop_column('users', 'mfa_setup_deadline')
    op.drop_column('users', 'locked_until')
    op.drop_column('users', 'failed_login_count')

    print("⚠️  Rolled back all Phase 1 security fields")
```

---

## 🧪 Migration Testing Checklist

### Pre-Migration
- [ ] Backup production database
- [ ] Test migration on staging first
- [ ] Verify alembic current revision
- [ ] Check for pending migrations

### During Migration
- [ ] Run migration on staging: `alembic upgrade head`
- [ ] Verify columns added successfully (SQL queries above)
- [ ] Check default values correct
- [ ] Verify indexes created
- [ ] Test rollback: `alembic downgrade -1`
- [ ] Re-apply: `alembic upgrade head`

### Post-Migration
- [ ] Verify application can read new fields
- [ ] Test new features (lockout, MFA enforcement)
- [ ] Check performance (index usage)
- [ ] Monitor error logs (no migration errors)
- [ ] Update User model in code (if not auto-detected)

---

## 📊 Model Updates Required

After migration, update User model:

### File: `backend/app/models/user.py`

```python
# Add to User class

# Login lockout (ADR-027 Phase 1)
failed_login_count = Column(Integer, default=0, nullable=False)
locked_until = Column(DateTime(timezone=True), nullable=True)

# MFA enforcement (ADR-027 Phase 1)
mfa_setup_deadline = Column(DateTime(timezone=True), nullable=True)
is_mfa_exempt = Column(Boolean, default=False, nullable=False)
```

### Verify Model Matches Database

```python
# backend/tests/test_models.py

def test_user_model_has_phase1_fields():
    """Verify User model has all Phase 1 fields."""
    user = User(
        email="test@example.com",
        password_hash="...",
    )

    # Login lockout fields
    assert hasattr(user, 'failed_login_count')
    assert hasattr(user, 'locked_until')

    # MFA enforcement fields
    assert hasattr(user, 'mfa_setup_deadline')
    assert hasattr(user, 'is_mfa_exempt')

    # Default values
    assert user.failed_login_count == 0
    assert user.locked_until is None
    assert user.mfa_setup_deadline is None
    assert user.is_mfa_exempt is False
```

---

## 🚨 Rollback Plan

### If Migration Fails

**Scenario 1**: Migration fails during `upgrade()`

```bash
# Alembic automatically rolls back on error
# Check error message
alembic current  # Verify still on old revision

# Fix migration code
# Re-run
alembic upgrade head
```

**Scenario 2**: Migration succeeds but app breaks

```bash
# Immediate rollback
alembic downgrade -1

# Verify database state
psql -U sdlc_user -d sdlc_orchestrator -c "
  SELECT column_name FROM information_schema.columns
  WHERE table_name = 'users'
  ORDER BY column_name;
"

# Fix code
# Re-test
# Re-deploy
```

**Scenario 3**: Need to rollback in production

```bash
# 1. Stop application (prevent new writes)
docker stop sdlc-backend

# 2. Backup database
pg_dump -U sdlc_user sdlc_orchestrator > backup_$(date +%Y%m%d_%H%M%S).sql

# 3. Rollback migration
alembic downgrade -1

# 4. Verify rollback success
psql -U sdlc_user -d sdlc_orchestrator -c "SELECT column_name FROM information_schema.columns WHERE table_name = 'users';"

# 5. Restart application (old version)
docker start sdlc-backend

# 6. Verify application works
curl http://localhost:8300/api/v1/health
```

---

## ✅ Migration Checklist

### Before Sprint N+1
- [x] Migration templates prepared
- [ ] BE Lead reviews templates
- [ ] Staging database ready

### During Sprint N+1
- [ ] Create migration files (Week 1 - Tue/Wed)
- [ ] Test migrations on staging
- [ ] Code review migration scripts
- [ ] Update User model
- [ ] Test application with new fields
- [ ] Deploy to staging

### Before Production Deploy
- [ ] Backup production database
- [ ] Test migrations on staging (1 week stable)
- [ ] Rollback plan documented
- [ ] On-call team briefed
- [ ] CTO approval obtained

---

**Migration Templates Ready** ✅

**Next**: BE Lead creates migration files in Sprint N+1 Week 1 🚀
