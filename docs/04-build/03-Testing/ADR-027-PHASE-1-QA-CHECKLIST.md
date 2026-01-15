# ADR-027 Phase 1 - QA Testing Checklist

**Sprint**: Sprint N+1 (Jan 27 - Feb 7, 2026)
**Owner**: QA Team
**Purpose**: Comprehensive testing checklist for 4 security settings
**Status**: Ready for Sprint N+1

---

## 🎯 Testing Objectives

**Goal**: Verify all 4 security settings work correctly and meet acceptance criteria

**Coverage Targets**:
- Unit tests: 100% for SettingsService
- Integration tests: 95%+ for all settings
- E2E tests: All critical user journeys
- Performance: <5ms cache hit, <50ms cache miss

---

## 📋 Pre-Testing Setup

### Environment Preparation
- [ ] Staging environment ready (PostgreSQL, Redis, Backend, Frontend)
- [ ] Test database seeded with default settings
- [ ] Test users created (regular user, admin, superuser)
- [ ] Redis cache accessible
- [ ] Monitoring tools ready (Grafana, logs)

### Test Data
- [ ] Create 3 test users:
  - `test-user@example.com` (regular user)
  - `test-admin@example.com` (admin)
  - `test-superuser@example.com` (superuser)
- [ ] Seed default settings in database
- [ ] Prepare test passwords (various lengths)

---

## 🧪 Unit Testing Checklist

### SDLC-ADR027-000: SettingsService

**File**: `backend/tests/services/test_settings_service.py`

- [ ] **Test 1**: get() with existing setting → returns DB value
  ```python
  setting = await settings_service.get("session_timeout_minutes")
  assert setting == 30
  ```

- [ ] **Test 2**: get() with missing setting → returns default
  ```python
  setting = await settings_service.get("nonexistent_key", default=99)
  assert setting == 99
  ```

- [ ] **Test 3**: Cache hit → no DB query (verify with mock)
  ```python
  # First call → DB query
  # Second call → cache hit (no DB query)
  ```

- [ ] **Test 4**: Cache miss → DB query + cache store
  ```python
  # Clear cache
  # Call get() → verify DB query happened
  # Call get() again → verify cache hit
  ```

- [ ] **Test 5**: invalidate_cache() → cache cleared
  ```python
  await settings_service.invalidate_cache("session_timeout_minutes")
  # Next get() should query DB
  ```

**Coverage Target**: 100%

---

## 🔐 1. session_timeout_minutes Testing

### Unit Tests (SDLC-ADR027-102)

**File**: `backend/tests/core/test_security.py`

- [ ] **UT-1.1**: Token expiry calculation with timeout=15
  ```python
  token = create_access_token("user-123", timeout_minutes=15)
  decoded = decode_token(token)
  assert expires_in_minutes(decoded["exp"]) == 15
  ```

- [ ] **UT-1.2**: Token expiry calculation with timeout=60
- [ ] **UT-1.3**: Token expiry with missing setting → fallback to 30
- [ ] **UT-1.4**: Multiple tokens with different timeouts (verify independence)

### Integration Tests

**File**: `backend/tests/integration/test_session_timeout.py`

- [ ] **IT-1.1**: Login → Change timeout to 15 → Login again → Verify token expires at 15min
  ```
  1. Login as user → get token with 30min expiry (default)
  2. Admin changes timeout to 15
  3. Wait 5 min (cache expiry)
  4. Login again → verify new token expires at 15min
  ```

- [ ] **IT-1.2**: Change timeout to 10 → Existing tokens still valid until original expiry
- [ ] **IT-1.3**: Change timeout to 60 → New tokens last 60 minutes

### Manual E2E Tests

- [ ] **E2E-1.1**: Admin changes session_timeout via UI
  1. Login as admin
  2. Navigate to Settings → Security
  3. Change `session_timeout_minutes` from 30 to 45
  4. Click Save
  5. Verify success message
  6. Wait 5 minutes (cache expiry)
  7. Login as regular user
  8. Inspect JWT token → verify expiry is 45 minutes from now

- [ ] **E2E-1.2**: Token expires at correct time
  1. Set timeout to 5 minutes
  2. Login as user
  3. Wait 5 minutes
  4. Try to access protected endpoint → 401 Unauthorized

- [ ] **E2E-1.3**: Refresh token still works after access token expires

**Pass Criteria**: ✅ All tests green

---

## 🔒 2. max_login_attempts Testing

### Unit Tests (SDLC-ADR027-202)

**File**: `backend/tests/api/test_auth.py`

- [ ] **UT-2.1**: Fail login N times → account locked
  ```python
  for i in range(5):
      response = await client.post("/api/v1/auth/login", ...)
      assert response.status_code == 401
  # 6th attempt
  response = await client.post("/api/v1/auth/login", ...)
  assert response.status_code == 403  # Account locked
  ```

- [ ] **UT-2.2**: Fail N-1 times → still can login with correct password
- [ ] **UT-2.3**: Locked account → 403 with locked_until in response
- [ ] **UT-2.4**: Auto-unlock after 30 minutes
- [ ] **UT-2.5**: Admin unlocks account → user can login
- [ ] **UT-2.6**: Successful login → reset failed_login_count to 0
- [ ] **UT-2.7**: Superuser exempt from lockout
- [ ] **UT-2.8**: Concurrent failed logins → counter increments correctly (race condition test)

### Integration Tests

**File**: `backend/tests/integration/test_account_lockout.py`

- [ ] **IT-2.1**: Full lockout flow
  1. User fails login 5 times
  2. Verify account locked (403)
  3. Wait 30 minutes
  4. Verify auto-unlocked (can login)

- [ ] **IT-2.2**: Admin unlock flow
  1. User fails login 5 times (locked)
  2. Admin calls unlock endpoint
  3. Verify user can login immediately

- [ ] **IT-2.3**: Change max_attempts setting
  1. Set max_attempts=3
  2. User fails 3 times → locked
  3. Admin unlocks
  4. Set max_attempts=5
  5. User fails 5 times → locked

### Load Tests

**File**: `backend/tests/load/test_lockout_load.py`

- [ ] **Load-2.1**: 100 concurrent failed logins
  ```python
  # Verify failed_login_count = 100 (no race conditions)
  # Verify account locked
  ```

- [ ] **Load-2.2**: 1000 req/s sustained for 10s
  - Verify lockout logic still works
  - Verify p95 latency <100ms

### Manual E2E Tests

- [ ] **E2E-2.1**: Fail login multiple times via UI
  1. Navigate to login page
  2. Enter wrong password 5 times
  3. Verify "Account locked" error message
  4. Verify locked_until time displayed
  5. Screenshot error message

- [ ] **E2E-2.2**: Admin unlocks account
  1. Login as admin
  2. Navigate to Users page
  3. Find locked user (locked icon shown)
  4. Click "Unlock Account" button
  5. Verify success message
  6. User can login immediately

- [ ] **E2E-2.3**: Auto-unlock after 30 minutes
  1. Lock account (fail 5 times)
  2. Wait 30 minutes (or adjust system time)
  3. Verify user can login

**Pass Criteria**: ✅ All tests green + Load test passes

---

## 🔑 3. password_min_length Testing

### Unit Tests (SDLC-ADR027-302)

**File**: `backend/tests/schemas/test_user_schemas.py`

- [ ] **UT-3.1**: Password length validation with min=12
  ```python
  # Valid password (12 chars)
  user = UserCreate(email="...", password="StrongPass12")
  assert user.password == "StrongPass12"

  # Invalid password (11 chars)
  with pytest.raises(ValidationError):
      user = UserCreate(email="...", password="ShortPass1")
  ```

- [ ] **UT-3.2**: Change min_length to 16 → 15 chars rejected
- [ ] **UT-3.3**: Change min_length to 8 → 8 chars accepted
- [ ] **UT-3.4**: Error message includes min length
  ```python
  with pytest.raises(ValidationError) as exc:
      user = UserCreate(email="...", password="short")
  assert "at least 12 characters" in str(exc.value)
  ```

### Integration Tests

**File**: `backend/tests/integration/test_password_validation.py`

- [ ] **IT-3.1**: Create user with weak password → 422
  ```
  POST /api/v1/users
  {
    "email": "test@example.com",
    "password": "short"
  }

  Expected: 422 Unprocessable Entity
  ```

- [ ] **IT-3.2**: Change password with weak password → 422
- [ ] **IT-3.3**: Admin changes min_length → next user creation validates correctly

### Manual E2E Tests

- [ ] **E2E-3.1**: Signup with weak password
  1. Navigate to signup page
  2. Enter email and short password (11 chars)
  3. Click "Sign Up"
  4. Verify error: "Password must be at least 12 characters"
  5. Screenshot error

- [ ] **E2E-3.2**: Admin changes password_min_length
  1. Login as admin
  2. Navigate to Settings → Security
  3. Change `password_min_length` from 12 to 16
  4. Click Save
  5. Logout
  6. Try signup with 15-char password → rejected
  7. Try signup with 16-char password → accepted

**Pass Criteria**: ✅ All tests green

---

## 🛡️ 4. mfa_required Testing

### Unit Tests (SDLC-ADR027-402)

**File**: `backend/tests/middleware/test_mfa_middleware.py`

- [ ] **UT-4.1**: mfa_required=false → MFA optional
  ```python
  # User without MFA can login
  ```

- [ ] **UT-4.2**: mfa_required=true + user has MFA → normal 2FA flow
- [ ] **UT-4.3**: mfa_required=true + no MFA + within grace → warning
- [ ] **UT-4.4**: mfa_required=true + no MFA + past grace → 403 blocked
- [ ] **UT-4.5**: Exempted user (is_mfa_exempt=true) → never required
- [ ] **UT-4.6**: Superuser → automatically exempt
- [ ] **UT-4.7**: Grace period calculation (7 days)

### Integration Tests

**File**: `backend/tests/integration/test_mfa_enforcement.py`

- [ ] **IT-4.1**: Enable MFA requirement → users prompted
  1. Admin enables mfa_required
  2. User without MFA logs in
  3. Verify warning banner shown
  4. Verify mfa_setup_deadline set (7 days from now)

- [ ] **IT-4.2**: Grace period expires → hard block
  1. User has mfa_setup_deadline in past
  2. User tries to login
  3. Verify 403 with "MFA required" message

- [ ] **IT-4.3**: Admin exempts user
  1. Admin calls exempt endpoint
  2. User.is_mfa_exempt = true
  3. User can login without MFA (even if required)

### Manual E2E Tests

- [ ] **E2E-4.1**: Enable MFA requirement as admin
  1. Login as admin
  2. Navigate to Settings → Security
  3. Toggle "Require MFA for all users" ON
  4. Click Save
  5. Logout
  6. Login as regular user (no MFA)
  7. Verify warning banner: "MFA will be required in 7 days"
  8. Screenshot warning

- [ ] **E2E-4.2**: User sets up MFA during grace period
  1. User sees warning banner
  2. Click "Set up MFA" link
  3. Follow MFA setup flow (scan QR code)
  4. Verify MFA enabled
  5. Login again → 2FA flow works

- [ ] **E2E-4.3**: Grace period expires → hard block
  1. Simulate 8 days passing (adjust mfa_setup_deadline)
  2. User tries to login
  3. Verify 403 error: "MFA is required"
  4. Verify redirect to MFA setup page
  5. Screenshot error

- [ ] **E2E-4.4**: Admin exempts user
  1. Login as admin
  2. Navigate to Users page
  3. Find user without MFA
  4. Check "Exempt from MFA" checkbox
  5. Save
  6. User can login without MFA

**Pass Criteria**: ✅ All tests green

---

## 🔄 Integration Testing (All 4 Settings Together)

**File**: `backend/tests/integration/test_phase1_integration.py`

### Cross-Setting Tests

- [ ] **INT-1**: All 4 settings work simultaneously
  1. Set session_timeout=20
  2. Set max_login_attempts=3
  3. Set password_min_length=14
  4. Enable mfa_required
  5. Create new user with 14-char password → success
  6. User fails login 3 times → locked
  7. Admin unlocks user
  8. User logs in → token expires at 20 min
  9. User without MFA → warned about MFA requirement

- [ ] **INT-2**: Admin changes all settings → all take effect
- [ ] **INT-3**: Cache invalidation works for all settings
- [ ] **INT-4**: Settings persist after backend restart
- [ ] **INT-5**: Rollback setting change works (use previous_value)

### Performance Tests

- [ ] **PERF-1**: Settings cache hit <5ms (100 requests)
  ```python
  for i in range(100):
      start = time.time()
      await settings_service.get("session_timeout_minutes")
      duration = time.time() - start
      assert duration < 0.005  # 5ms
  ```

- [ ] **PERF-2**: Settings cache miss <50ms
- [ ] **PERF-3**: No API latency regression (p95 still <100ms)

---

## 📱 End-to-End Testing (User Journeys)

### Journey 1: New User Signup (All Settings Active)

**Prerequisites**: All 4 settings configured
- session_timeout = 30
- max_login_attempts = 5
- password_min_length = 12
- mfa_required = true (7-day grace)

**Steps**:
1. [ ] Navigate to signup page
2. [ ] Enter email: `newuser@example.com`
3. [ ] Enter weak password (10 chars) → Error: "Password must be at least 12 characters"
4. [ ] Enter strong password (12+ chars) → Success
5. [ ] Verify account created
6. [ ] Login with correct credentials → Success
7. [ ] Verify warning banner: "MFA required in 7 days"
8. [ ] Wait 30 minutes (or change token)
9. [ ] Verify session expired (401 on protected endpoint)

**Expected**: All validations work, user can complete signup and login

---

### Journey 2: Account Lockout & Admin Unlock

**Steps**:
1. [ ] User fails login 5 times (wrong password)
2. [ ] Verify account locked (403)
3. [ ] Verify error message shows unlock time
4. [ ] Admin logs in
5. [ ] Admin navigates to Users page
6. [ ] Admin finds locked user (icon shown)
7. [ ] Admin clicks "Unlock Account"
8. [ ] Verify success message
9. [ ] User logs in immediately → Success

**Expected**: Lockout works, admin can unlock, user can login

---

### Journey 3: MFA Enforcement (Grace Period → Hard Block)

**Steps**:
1. [ ] Admin enables mfa_required
2. [ ] User without MFA logs in
3. [ ] Verify warning banner (7 days)
4. [ ] User ignores warning (continues using app)
5. [ ] Simulate 8 days passing
6. [ ] User tries to login → 403 Blocked
7. [ ] Verify redirect to MFA setup page
8. [ ] User sets up MFA (scan QR, enter code)
9. [ ] User logs in with MFA → Success

**Expected**: Grace period works, hard block enforced, MFA setup works

---

## 🎯 Acceptance Criteria Verification

### Functional Requirements

- [ ] **FR-1**: Admin changes session_timeout → new tokens use new duration (verified in staging)
- [ ] **FR-2**: Admin sets max_login_attempts → accounts lock after N failures (tested manually)
- [ ] **FR-3**: Admin enables mfa_required → users prompted to set up MFA (E2E test passes)
- [ ] **FR-4**: Admin sets password_min_length → weak passwords rejected (unit tests 100%)

### Non-Functional Requirements

- [ ] **NFR-1**: Settings cached in Redis (verified with monitoring)
- [ ] **NFR-2**: Cache hit <5ms (performance test passes)
- [ ] **NFR-3**: Cache miss <50ms (performance test passes)
- [ ] **NFR-4**: No API latency regression (p95 <100ms maintained)
- [ ] **NFR-5**: Zero production incidents (1 week monitoring)

### Security Requirements

- [ ] **SEC-1**: Superusers exempt from account lockout
- [ ] **SEC-2**: MFA enforcement cannot be bypassed
- [ ] **SEC-3**: Password validation cannot be bypassed
- [ ] **SEC-4**: All setting changes logged in audit log

---

## 🐛 Bug Tracking Template

### Bug Report Format

```markdown
**Bug ID**: ADR027-BUG-XXX
**Setting**: [session_timeout | max_login_attempts | password_min_length | mfa_required]
**Severity**: [P0 - Critical | P1 - High | P2 - Medium | P3 - Low]
**Status**: [New | In Progress | Fixed | Verified]

**Description**:
[Describe the bug]

**Steps to Reproduce**:
1.
2.
3.

**Expected Behavior**:
[What should happen]

**Actual Behavior**:
[What actually happens]

**Environment**:
- Branch: feature/adr-027-phase1
- Commit: abc123
- Database: PostgreSQL 15.5
- Redis: 7.2

**Screenshots/Logs**:
[Attach screenshots or log excerpts]

**Assignee**: [BE Lead | BE Dev #2 | QA]
**Discovered By**: [QA Name]
**Discovered On**: [Date]
```

---

## ✅ Sign-Off Checklist

### Before Merging to Main

- [ ] All unit tests pass (100% coverage for SettingsService)
- [ ] All integration tests pass (95%+ coverage)
- [ ] All E2E tests pass (3 user journeys completed)
- [ ] Performance tests pass (cache <5ms, no regression)
- [ ] Load tests pass (1000 req/s sustained)
- [ ] Security audit complete (no bypasses found)
- [ ] Code review approved (2+ reviewers)
- [ ] Documentation updated (API docs, admin guide)
- [ ] Zero P0/P1 bugs remaining
- [ ] QA sign-off obtained
- [ ] Security Lead sign-off obtained

### Before Deploying to Production

- [ ] Staging tests all green (1 week stable)
- [ ] Rollback plan tested
- [ ] Monitoring dashboards ready (Grafana)
- [ ] Alert rules configured (Prometheus)
- [ ] On-call team briefed
- [ ] Deployment checklist reviewed
- [ ] CTO approval obtained

---

## 📊 Test Results Summary Template

```markdown
# ADR-027 Phase 1 - Test Results Summary

**Date**: [Date]
**Tester**: [QA Name]
**Sprint**: Sprint N+1
**Status**: [In Progress | Complete]

## Test Coverage

| Category | Tests Run | Tests Passed | Coverage | Status |
|----------|-----------|--------------|----------|--------|
| Unit Tests | 25 | 25 | 100% | ✅ PASS |
| Integration Tests | 15 | 14 | 93% | 🟡 1 FAIL |
| E2E Tests | 10 | 10 | 100% | ✅ PASS |
| Performance Tests | 5 | 5 | 100% | ✅ PASS |
| Load Tests | 2 | 2 | 100% | ✅ PASS |
| **TOTAL** | **57** | **56** | **98%** | 🟡 |

## Failed Tests

1. **IT-2.2**: Admin unlock flow
   - **Issue**: Unlock endpoint returns 500 when user not found
   - **Severity**: P2 - Medium
   - **Assigned**: BE Lead
   - **ETA**: Jan 30

## Performance Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Cache hit latency | <5ms | 3.2ms | ✅ |
| Cache miss latency | <50ms | 42ms | ✅ |
| API p95 latency | <100ms | 87ms | ✅ |
| Load test (1000 req/s) | PASS | PASS | ✅ |

## Bugs Found

- ADR027-BUG-001: [Description]
- ADR027-BUG-002: [Description]

## Sign-Off

- [ ] QA Lead: _______________
- [ ] Security Lead: _______________
- [ ] BE Lead: _______________
```

---

**QA Checklist Ready for Sprint N+1** ✅

**Next**: BE team implements → QA tests → Iterate until all green 🚀
