# ADR-027 Phase 1 - Code Review Checklist

**Sprint**: Sprint N+1 (Jan 27 - Feb 7, 2026)
**Purpose**: Ensure code quality and security for Phase 1 implementation
**Reviewers**: Tech Lead + BE Lead + Security Lead
**Approval Required**: 2+ reviewers

---

## 🎯 Review Objectives

**Quality Standards**:
- ✅ Zero Mock Policy compliance (no placeholders)
- ✅ Production-ready code (error handling, logging, security)
- ✅ Test coverage ≥95% (unit + integration)
- ✅ Performance meets budget (<5ms cache, <100ms p95 API)
- ✅ Security baseline maintained (OWASP ASVS L2)
- ✅ Backward compatible (env var fallback)

---

## 📋 General Code Review Checklist

### Code Quality

- [ ] **No TODO comments** or placeholders
  ```python
  # ❌ BAD
  def validate_password():
      # TODO: Implement validation
      pass

  # ✅ GOOD
  def validate_password(password: str, min_length: int) -> bool:
      if len(password) < min_length:
          raise ValueError(f"Password must be at least {min_length} characters")
      return True
  ```

- [ ] **Type hints 100%** (Python) or **TypeScript strict mode** (Frontend)
  ```python
  # ✅ GOOD
  def get_setting(key: str, default: Any = None) -> Any:
      ...

  # ❌ BAD (no type hints)
  def get_setting(key, default=None):
      ...
  ```

- [ ] **Docstrings present** (Google style for Python)
  ```python
  # ✅ GOOD
  def get_session_timeout_minutes(self) -> int:
      """
      Get session timeout in minutes from database.

      Returns:
          Session timeout value (default: 30 minutes)

      Note:
          This setting controls how long a user session remains valid.
      """
      ...
  ```

- [ ] **Error handling comprehensive**
  ```python
  # ✅ GOOD
  try:
      setting = await self.get("session_timeout_minutes")
  except DatabaseError as e:
      logger.error(f"Failed to read setting: {e}")
      return 30  # Fallback to default
  ```

- [ ] **Logging appropriate** (structured logging with context)
  ```python
  # ✅ GOOD
  logger.info(
      f"Setting changed: {key}={new_value} (old={old_value})",
      extra={"user_id": user_id, "setting_key": key}
  )
  ```

---

## 🔧 SettingsService Review (SDLC-ADR027-000)

### File: `backend/app/services/settings_service.py`

#### Functional Requirements

- [ ] **Reads from system_settings table** (not hardcoded)
- [ ] **Redis caching implemented** (5-min TTL)
- [ ] **Cache invalidation works** (on setting update)
- [ ] **Fallback to defaults** if setting missing
- [ ] **Type accessors for all 4 settings**:
  - `get_session_timeout_minutes() -> int`
  - `get_max_login_attempts() -> int`
  - `is_mfa_required() -> bool`
  - `get_password_min_length() -> int`

#### Implementation Review

- [ ] **Async/await used correctly** (no blocking calls)
  ```python
  # ✅ GOOD
  async def get(self, key: str) -> Any:
      result = await self.db.execute(select(...))
      return result.scalar_one_or_none()

  # ❌ BAD (blocking call in async function)
  async def get(self, key: str) -> Any:
      return requests.get(...)  # Blocks event loop!
  ```

- [ ] **Database queries optimized** (no N+1 queries)
- [ ] **Redis connection handling** (lazy init, error handling)
- [ ] **Value parsing correct** (JSONB → Python types)

#### Security Review

- [ ] **No SQL injection** (uses SQLAlchemy ORM, not raw SQL)
- [ ] **No secrets in logs** (API keys, passwords never logged)
- [ ] **Cache keys namespaced** (`system_settings:{key}`)

#### Testing Review

- [ ] **Unit tests cover all methods** (100% coverage)
- [ ] **Test cache hit/miss behavior**
- [ ] **Test fallback to defaults**
- [ ] **Test cache invalidation**

---

## 🕐 session_timeout_minutes Review (SDLC-ADR027-101)

### Files Modified

- `backend/app/core/security.py`
- `backend/app/api/routes/auth.py`
- `backend/app/api/routes/github.py`

#### Functional Requirements

- [ ] **create_access_token() uses SettingsService**
- [ ] **Token expiry set to DB value** (not env var)
- [ ] **Fallback to 30 min** if setting missing
- [ ] **All callers updated** (auth.py, github.py)

#### Implementation Review

```python
# File: backend/app/core/security.py

# ✅ GOOD
async def create_access_token(
    subject: str,
    settings_service: Optional[SettingsService] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    elif settings_service:
        # Read from database setting
        timeout_minutes = await settings_service.get_session_timeout_minutes()
        expire = datetime.utcnow() + timedelta(minutes=timeout_minutes)
    else:
        # Fallback to env var (backward compatible)
        expire = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)

    # ... rest of token creation
```

- [ ] **Backward compatible** (env var fallback works)
- [ ] **No breaking changes** to existing callers
- [ ] **Token expiry calculation correct**

#### Testing Review

- [ ] **Unit tests for token expiry calculation**
- [ ] **Integration test: change setting → verify new tokens**
- [ ] **Test fallback behavior** (settings_service=None)

---

## 🔒 max_login_attempts Review (SDLC-ADR027-201)

### Files Created/Modified

- `alembic/versions/XXXXXX_add_login_lockout_fields.py` (migration)
- `backend/app/models/user.py` (add fields)
- `backend/app/api/routes/auth.py` (lockout logic)
- `backend/app/api/routes/admin.py` (unlock endpoint)

#### Database Migration Review

- [ ] **Migration file follows template** (see ADR-027-MIGRATION-TEMPLATES.md)
- [ ] **Fields added correctly**:
  - `failed_login_count INTEGER DEFAULT 0`
  - `locked_until TIMESTAMP NULL`
- [ ] **Index created** (`idx_users_locked_until`)
- [ ] **Rollback tested** (`alembic downgrade -1` works)

#### Lockout Logic Review

```python
# File: backend/app/api/routes/auth.py

# ✅ GOOD
async def login(credentials: LoginRequest, db: AsyncSession):
    user = await get_user_by_email(db, credentials.email)

    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        unlock_in_minutes = (user.locked_until - datetime.utcnow()).total_seconds() / 60
        raise HTTPException(
            status_code=403,
            detail={
                "message": "Account locked due to too many failed login attempts",
                "locked_until": user.locked_until.isoformat(),
                "unlock_in_minutes": int(unlock_in_minutes)
            }
        )

    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        # Increment failed login count
        user.failed_login_count += 1

        # Check if should lock
        max_attempts = await settings_service.get_max_login_attempts()
        if user.failed_login_count >= max_attempts:
            user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            logger.warning(f"Account locked: {user.email} (attempts: {user.failed_login_count})")

        await db.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Successful login → reset counter
    user.failed_login_count = 0
    user.locked_until = None
    await db.commit()

    # ... generate token
```

- [ ] **Lockout check before password verification** (security)
- [ ] **Increment counter on failed login**
- [ ] **Lock account after N failures**
- [ ] **Reset counter on successful login**
- [ ] **Superusers exempt from lockout**
  ```python
  # ✅ GOOD
  if user.is_superuser:
      # Skip lockout check for superusers
      pass
  ```

#### Unlock Endpoint Review

```python
# File: backend/app/api/routes/admin.py

# ✅ GOOD
@router.post("/users/{user_id}/unlock")
async def unlock_user(
    user_id: UUID,
    admin: User = Depends(require_superuser),  # Only admins
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.failed_login_count = 0
    user.locked_until = None
    await db.commit()

    # Audit log
    await audit_service.log_action(
        action=AuditAction.ACCOUNT_UNLOCKED,
        user_id=admin.id,
        target_user_id=user_id
    )

    return {"message": f"Account unlocked: {user.email}"}
```

- [ ] **Only admins can unlock** (security)
- [ ] **Audit log created** (who unlocked whom)
- [ ] **Handles user not found** (404)

#### Security Review

- [ ] **No race conditions** (database transactions used)
- [ ] **Superusers never locked** (emergency access)
- [ ] **Lockout duration reasonable** (30 min, not configurable in Phase 1)
- [ ] **Failed attempts logged** (audit trail)

#### Testing Review

- [ ] **Unit tests: lockout after N failures**
- [ ] **Unit tests: reset on successful login**
- [ ] **Unit tests: superuser exempt**
- [ ] **Integration test: full lockout → unlock flow**
- [ ] **Load test: 100 concurrent failed logins** (no race conditions)

---

## 🔑 password_min_length Review (SDLC-ADR027-301)

### Files Modified

- `backend/app/main.py` (app startup cache)
- `backend/app/schemas/admin.py` (validators)
- `backend/app/schemas/auth.py` (validators)

#### App-Level Cache Review

```python
# File: backend/app/main.py

# ✅ GOOD
@app.on_event("startup")
async def load_security_settings():
    """Load security settings into app cache on startup."""
    async with get_db_session() as db:
        settings_svc = SettingsService(db)
        app.state.password_min_length = await settings_svc.get_password_min_length()
    logger.info(f"Loaded password_min_length: {app.state.password_min_length}")

@app.on_event("startup")
async def start_settings_refresh_task():
    """Background task to refresh settings every 5 minutes."""
    async def refresh_settings():
        while True:
            try:
                await asyncio.sleep(300)  # 5 minutes
                async with get_db_session() as db:
                    settings_svc = SettingsService(db)
                    new_value = await settings_svc.get_password_min_length()
                    app.state.password_min_length = new_value
                    logger.debug(f"Refreshed password_min_length: {new_value}")
            except Exception as e:
                logger.error(f"Failed to refresh settings: {e}")
    asyncio.create_task(refresh_settings())
```

- [ ] **Settings loaded on startup**
- [ ] **Background task refreshes every 5 min**
- [ ] **Error handling in refresh task** (doesn't crash app)
- [ ] **Logging appropriate**

#### Validator Review

```python
# File: backend/app/schemas/admin.py

# ✅ GOOD
from fastapi import Request

class AdminUserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., description="Password")

    @field_validator('password')
    def validate_password_length(cls, v, info: ValidationInfo):
        # Get min_length from app cache
        request = info.context.get('request') if info.context else None
        if request and hasattr(request.app.state, 'password_min_length'):
            min_length = request.app.state.password_min_length
        else:
            min_length = 12  # Fallback

        if len(v) < min_length:
            raise ValueError(f"Password must be at least {min_length} characters")
        return v
```

- [ ] **Reads from app.state cache** (not DB on every request)
- [ ] **Fallback to 12** if cache unavailable
- [ ] **Error message includes min length**
- [ ] **Validator works in both create and update**

#### Endpoint Integration Review

```python
# File: backend/app/api/routes/admin.py

# ✅ GOOD (passes request to validator)
@router.post("/users")
async def create_user(
    user_data: AdminUserCreate,
    request: Request,  # Add request parameter
    admin: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db)
):
    # Pydantic validator will access request.app.state.password_min_length
    ...
```

- [ ] **Request passed to Pydantic** (for context)
- [ ] **Validation happens before user creation**

#### Testing Review

- [ ] **Unit tests: password validation with various lengths**
- [ ] **Unit tests: error message correct**
- [ ] **Integration test: cache refresh works**
- [ ] **Integration test: admin changes min_length → validated**

---

## 🛡️ mfa_required Review (SDLC-ADR027-401)

### Files Created/Modified

- `alembic/versions/YYYYYY_add_mfa_enforcement_fields.py` (migration)
- `backend/app/models/user.py` (add fields)
- `backend/app/middleware/mfa_middleware.py` (enforcement logic)
- `backend/app/api/routes/auth.py` (integrate middleware)
- `backend/app/api/routes/admin.py` (exempt endpoint)

#### Database Migration Review

- [ ] **Migration file follows template**
- [ ] **Fields added correctly**:
  - `mfa_setup_deadline TIMESTAMP NULL`
  - `is_mfa_exempt BOOLEAN DEFAULT FALSE`
- [ ] **Rollback tested**

#### MFA Enforcement Middleware Review

```python
# File: backend/app/middleware/mfa_middleware.py

# ✅ GOOD
async def mfa_enforcement_middleware(
    user: User,
    settings_service: SettingsService
) -> None:
    """
    Enforce MFA setup requirement.

    Raises:
        HTTPException: 403 if MFA required but not set up (past grace period)
    """
    # Check if MFA is required globally
    mfa_required = await settings_service.is_mfa_required()
    if not mfa_required:
        return  # MFA optional

    # Superusers and exempted users bypass
    if user.is_superuser or user.is_mfa_exempt:
        return

    # User already has MFA → all good
    if user.mfa_enabled:
        return

    # Set deadline if not set yet (first login after requirement enabled)
    if not user.mfa_setup_deadline:
        user.mfa_setup_deadline = datetime.utcnow() + timedelta(days=7)
        await db.commit()
        logger.info(f"Set MFA deadline for {user.email}: {user.mfa_setup_deadline}")

    # Check if past grace period
    if datetime.utcnow() > user.mfa_setup_deadline:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "MFA is required. Please set up MFA to continue.",
                "mfa_setup_url": "/auth/mfa/setup",
                "deadline_passed": user.mfa_setup_deadline.isoformat()
            }
        )

    # Within grace period → show warning
    days_remaining = (user.mfa_setup_deadline - datetime.utcnow()).days
    # Return warning in response headers or body
```

- [ ] **Checks global mfa_required setting**
- [ ] **Superusers and exempt users bypass**
- [ ] **Sets deadline on first login** (7 days grace)
- [ ] **Hard block after grace period**
- [ ] **Warning within grace period**

#### Admin Exempt Endpoint Review

```python
# File: backend/app/api/routes/admin.py

# ✅ GOOD
@router.patch("/users/{user_id}/mfa-exempt")
async def set_mfa_exemption(
    user_id: UUID,
    exempt: bool,
    admin: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_mfa_exempt = exempt
    await db.commit()

    # Audit log
    await audit_service.log_action(
        action=AuditAction.MFA_EXEMPTION_CHANGED,
        user_id=admin.id,
        target_user_id=user_id,
        details={"is_mfa_exempt": exempt}
    )

    return {"message": f"MFA exemption set to {exempt} for {user.email}"}
```

- [ ] **Only admins can exempt** (security)
- [ ] **Audit log created**
- [ ] **Returns clear response**

#### Security Review

- [ ] **No bypasses** (all paths checked)
- [ ] **Superusers auto-exempt** (emergency access)
- [ ] **Grace period enforced** (7 days, not configurable in Phase 1)
- [ ] **Exemption logged** (audit trail)

#### Testing Review

- [ ] **Unit tests: all enforcement scenarios**
- [ ] **Unit tests: grace period calculation**
- [ ] **Integration test: enable MFA requirement → users prompted**
- [ ] **Integration test: grace period → hard block**
- [ ] **Integration test: admin exemption**

---

## 🎯 Cross-Cutting Concerns Review

### Performance

- [ ] **Redis cache hit <5ms** (verified with benchmarks)
- [ ] **Redis cache miss <50ms**
- [ ] **No API latency regression** (p95 <100ms maintained)
- [ ] **Database queries optimized** (no N+1 queries)
- [ ] **Indexes used correctly** (idx_users_locked_until)

### Security

- [ ] **No SQL injection** (ORM used, no raw SQL)
- [ ] **No secrets in logs** (passwords, API keys never logged)
- [ ] **OWASP ASVS L2 maintained** (no new vulnerabilities)
- [ ] **Audit logs complete** (who did what when)
- [ ] **Superuser emergency access** (never locked out)

### Backward Compatibility

- [ ] **Env var fallback works** (backward compatible)
- [ ] **No breaking changes** to existing APIs
- [ ] **Migration is reversible** (rollback tested)
- [ ] **Existing users unaffected** (defaults applied)

### Code Quality

- [ ] **No TODO comments**
- [ ] **Type hints 100%**
- [ ] **Docstrings present**
- [ ] **Error handling comprehensive**
- [ ] **Logging appropriate**
- [ ] **No dead code**

### Testing

- [ ] **Unit tests ≥95% coverage**
- [ ] **Integration tests pass**
- [ ] **E2E tests pass** (3 user journeys)
- [ ] **Load tests pass** (1000 req/s sustained)
- [ ] **Performance tests pass** (cache <5ms)

---

## ✅ Final Approval Checklist

Before merging to main:

- [ ] **Code review approved** (2+ reviewers)
- [ ] **All tests pass** (CI/CD green)
- [ ] **Test coverage ≥95%** (verified)
- [ ] **Performance benchmarks pass** (no regression)
- [ ] **Security scan clean** (Semgrep passes)
- [ ] **Documentation updated** (API docs, admin guide)
- [ ] **Migration tested** (staging + rollback verified)
- [ ] **Acceptance criteria met** (all tickets DONE)
- [ ] **QA sign-off** (E2E tests passed)
- [ ] **Security Lead sign-off** (no vulnerabilities)

---

## 📝 Review Comment Templates

### Request Changes

```markdown
**Issue**: [Description]

**Location**: `file.py:42`

**Problem**:
- [Explain what's wrong]

**Suggested Fix**:
```python
# Your suggested code here
```

**Severity**: [P0 - Blocker | P1 - High | P2 - Medium | P3 - Low]
```

### Approve with Comments

```markdown
**LGTM** (Looks Good To Me) with minor suggestions:

**Nice work**:
- ✅ Error handling comprehensive
- ✅ Tests cover edge cases
- ✅ Performance optimized

**Minor suggestions** (non-blocking):
1. Consider adding docstring example at line 42
2. Typo in comment at line 67: "recieve" → "receive"

**Approved** - Ready to merge after addressing suggestions (optional)
```

---

**Code Review Checklist Ready** ✅

**Next**: Reviewers use this during Sprint N+1 code reviews 🚀
