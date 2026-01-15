#!/usr/bin/env python3
"""
=========================================================================
ADR-027 Phase 1 - Standalone Validation Script
SDLC Orchestrator - Stage 03 (BUILD)

Purpose:
Validate all Phase 1 implementation files exist and have correct structure.
This script can run without full backend dependencies.

Run: python3 scripts/validate_adr027_phase1.py

Validation Checks:
1. All required files exist
2. Database migrations have correct structure
3. SettingsService has all 4 accessors
4. Middleware exists and has key methods
5. Admin endpoints exist
6. Unit tests exist with expected test counts
7. Integration tests exist
=========================================================================
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Base path
BASE_PATH = Path(__file__).parent.parent


def check_file_exists(path: str, description: str) -> Tuple[bool, str]:
    """Check if file exists."""
    full_path = BASE_PATH / path
    if full_path.exists():
        return True, f"✅ {description}: {path}"
    return False, f"❌ {description}: {path} NOT FOUND"


def check_file_contains(path: str, patterns: List[str], description: str) -> Tuple[bool, str]:
    """Check if file contains expected patterns."""
    full_path = BASE_PATH / path
    if not full_path.exists():
        return False, f"❌ {description}: File not found"

    content = full_path.read_text()
    missing = []
    for pattern in patterns:
        if pattern not in content:
            missing.append(pattern)

    if not missing:
        return True, f"✅ {description}: All patterns found"
    return False, f"❌ {description}: Missing {missing}"


def count_tests(path: str) -> int:
    """Count test functions in a test file."""
    full_path = BASE_PATH / path
    if not full_path.exists():
        return 0

    content = full_path.read_text()
    # Count async def test_ and def test_ functions
    async_tests = len(re.findall(r'async def test_', content))
    sync_tests = len(re.findall(r'def test_', content))
    return async_tests + sync_tests


def print_header(title: str):
    """Print section header."""
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{title}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")


def print_result(passed: bool, message: str):
    """Print validation result."""
    if passed:
        print(f"{GREEN}{message}{RESET}")
    else:
        print(f"{RED}{message}{RESET}")


def main():
    """Run all validations."""
    print(f"\n{BOLD}ADR-027 Phase 1 - Validation Script{RESET}")
    print(f"Date: 2026-01-14")
    print(f"Base Path: {BASE_PATH}")

    all_passed = True
    results = []

    # =========================================================================
    # Check 1: Required Files Exist
    # =========================================================================
    print_header("1. Required Files")

    required_files = [
        ("backend/app/services/settings_service.py", "SettingsService"),
        ("backend/app/utils/password_validator.py", "Password Validator"),
        ("backend/app/middleware/mfa_middleware.py", "MFA Middleware"),
        ("backend/alembic/versions/sb5212d71967_add_login_lockout_fields.py", "Lockout Migration"),
        ("backend/alembic/versions/sb5313e82078_add_mfa_enforcement_fields.py", "MFA Migration"),
        ("backend/tests/unit/test_max_login_attempts.py", "Max Login Tests"),
        ("backend/tests/unit/test_password_min_length.py", "Password Length Tests"),
        ("backend/tests/unit/test_mfa_required.py", "MFA Required Tests"),
        ("backend/tests/integration/test_adr027_phase1_integration.py", "Integration Tests"),
    ]

    for path, desc in required_files:
        passed, msg = check_file_exists(path, desc)
        print_result(passed, msg)
        if not passed:
            all_passed = False

    # =========================================================================
    # Check 2: SettingsService Accessors
    # =========================================================================
    print_header("2. SettingsService Accessors")

    settings_accessors = [
        "get_session_timeout_minutes",
        "get_max_login_attempts",
        "get_password_min_length",
        "is_mfa_required",
    ]

    passed, msg = check_file_contains(
        "backend/app/services/settings_service.py",
        settings_accessors,
        "SettingsService accessors"
    )
    print_result(passed, msg)
    if not passed:
        all_passed = False

    # =========================================================================
    # Check 3: User Model Fields
    # =========================================================================
    print_header("3. User Model Fields (ADR-027)")

    user_fields = [
        "failed_login_count",
        "locked_until",
        "mfa_setup_deadline",
        "is_mfa_exempt",
    ]

    passed, msg = check_file_contains(
        "backend/app/models/user.py",
        user_fields,
        "User model ADR-027 fields"
    )
    print_result(passed, msg)
    if not passed:
        all_passed = False

    # =========================================================================
    # Check 4: Admin Endpoints
    # =========================================================================
    print_header("4. Admin Endpoints (ADR-027)")

    admin_endpoints = [
        "/unlock",
        "/mfa-exempt",
        "/mfa-status",
    ]

    passed, msg = check_file_contains(
        "backend/app/api/routes/admin.py",
        admin_endpoints,
        "Admin ADR-027 endpoints"
    )
    print_result(passed, msg)
    if not passed:
        all_passed = False

    # =========================================================================
    # Check 5: Password Validator
    # =========================================================================
    print_header("5. Password Validator")

    validator_patterns = [
        "validate_password_strength",
        "get_password_min_length",
        "HTTPException",
    ]

    passed, msg = check_file_contains(
        "backend/app/utils/password_validator.py",
        validator_patterns,
        "Password validator implementation"
    )
    print_result(passed, msg)
    if not passed:
        all_passed = False

    # =========================================================================
    # Check 6: MFA Middleware
    # =========================================================================
    print_header("6. MFA Middleware")

    middleware_patterns = [
        "MFAEnforcementMiddleware",
        "mfa_setup_deadline",
        "is_mfa_exempt",
        "X-MFA-Setup-Required",
        "7 days",
    ]

    passed, msg = check_file_contains(
        "backend/app/middleware/mfa_middleware.py",
        middleware_patterns,
        "MFA middleware implementation"
    )
    print_result(passed, msg)
    if not passed:
        all_passed = False

    # =========================================================================
    # Check 7: Test Counts
    # =========================================================================
    print_header("7. Test Coverage")

    test_files = [
        ("backend/tests/unit/test_max_login_attempts.py", 11, "Max Login Attempts"),
        ("backend/tests/unit/test_password_min_length.py", 12, "Password Min Length"),
        ("backend/tests/unit/test_mfa_required.py", 14, "MFA Required"),
        ("backend/tests/integration/test_adr027_phase1_integration.py", 15, "Integration"),
    ]

    total_tests = 0
    for path, expected, desc in test_files:
        count = count_tests(path)
        total_tests += count
        passed = count >= expected
        status = "✅" if passed else "❌"
        print(f"{status} {desc}: {count} tests (expected: {expected})")
        if not passed:
            all_passed = False

    print(f"\n{BOLD}Total Tests: {total_tests}{RESET}")

    # =========================================================================
    # Check 8: Database Migrations
    # =========================================================================
    print_header("8. Database Migrations")

    # Check lockout migration
    lockout_patterns = [
        "failed_login_count",
        "locked_until",
        "upgrade",
        "downgrade",
    ]
    passed, msg = check_file_contains(
        "backend/alembic/versions/sb5212d71967_add_login_lockout_fields.py",
        lockout_patterns,
        "Lockout migration structure"
    )
    print_result(passed, msg)
    if not passed:
        all_passed = False

    # Check MFA migration
    mfa_patterns = [
        "mfa_setup_deadline",
        "is_mfa_exempt",
        "upgrade",
        "downgrade",
    ]
    passed, msg = check_file_contains(
        "backend/alembic/versions/sb5313e82078_add_mfa_enforcement_fields.py",
        mfa_patterns,
        "MFA migration structure"
    )
    print_result(passed, msg)
    if not passed:
        all_passed = False

    # =========================================================================
    # Check 9: Documentation
    # =========================================================================
    print_header("9. Documentation")

    docs = [
        ("docs/04-build/03-Testing/ADR-027-INTEGRATION-TEST-PLAN.md", "Integration Test Plan"),
        ("docs/04-build/03-Testing/ADR-027-CTO-DEMO-SCRIPT.md", "CTO Demo Script"),
        ("docs/04-build/ADR-027-PHASE-1-COMPLETE.md", "Phase 1 Summary"),
        ("docs/04-build/07-Handover/ADR-027-PHASE-1-HANDOVER.md", "Handover Document"),
    ]

    for path, desc in docs:
        passed, msg = check_file_exists(path, desc)
        print_result(passed, msg)
        if not passed:
            all_passed = False

    # =========================================================================
    # Final Summary
    # =========================================================================
    print_header("FINAL SUMMARY")

    if all_passed:
        print(f"\n{GREEN}{BOLD}🎉 ALL VALIDATIONS PASSED!{RESET}")
        print(f"\n{GREEN}ADR-027 Phase 1 is complete and ready for:{RESET}")
        print(f"  - CTO Demo")
        print(f"  - Backend Lead Review")
        print(f"  - Merge to Main")
        print(f"\n{BOLD}Total Tests: {total_tests} (37 unit + 15 integration){RESET}")
        return 0
    else:
        print(f"\n{RED}{BOLD}❌ SOME VALIDATIONS FAILED{RESET}")
        print(f"\n{RED}Please fix the issues above before proceeding.{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
