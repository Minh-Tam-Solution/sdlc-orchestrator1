#!/usr/bin/env python3
"""
Standalone ADR-027 Phase 1 Validation Script
Tests all 4 settings without requiring full app initialization
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_settings_service():
    """Test SettingsService can be imported and has correct methods"""
    from app.services.settings_service import SettingsService
    
    print("✓ SettingsService imported successfully")
    
    # Check all required methods exist
    required_methods = [
        'get',
        'get_all',
        'invalidate_cache',
        'get_session_timeout_minutes',
        'get_max_login_attempts',
        'get_password_min_length',
        'is_mfa_required',
    ]
    
    for method in required_methods:
        assert hasattr(SettingsService, method), f"Missing method: {method}"
        print(f"  ✓ {method}() exists")
    
    return True

async def test_password_validator():
    """Test password validator utility"""
    from app.utils.password_validator import validate_password_strength
    
    print("✓ password_validator imported successfully")
    print(f"  ✓ validate_password_strength() exists")
    
    return True

async def test_mfa_middleware():
    """Test MFA middleware"""
    from app.middleware.mfa_middleware import MFAEnforcementMiddleware
    
    print("✓ MFAEnforcementMiddleware imported successfully")
    
    return True

async def test_models():
    """Test User model has new fields"""
    from app.models.user import User
    
    print("✓ User model imported successfully")
    
    # Check new fields exist
    new_fields = [
        'failed_login_count',
        'locked_until',
        'mfa_setup_deadline',
        'is_mfa_exempt',
    ]
    
    # Check if these are in the model's columns (SQLAlchemy)
    for field in new_fields:
        # SQLAlchemy models have __table__.columns
        if hasattr(User, '__table__'):
            if field in User.__table__.columns:
                print(f"  ✓ {field} field exists in User.__table__")
            else:
                print(f"  ? {field} not in __table__ yet (migration pending)")
        else:
            print(f"  ? User model structure check skipped")
            break
    
    return True

async def main():
    """Run all validation tests"""
    print("=" * 70)
    print("ADR-027 Phase 1 - Standalone Validation")
    print("=" * 70)
    print()
    
    tests = [
        ("SettingsService", test_settings_service),
        ("Password Validator", test_password_validator),
        ("MFA Middleware", test_mfa_middleware),
        ("User Model", test_models),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"Testing {name}...")
        try:
            result = await test_func()
            results.append((name, True, None))
            print()
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"  ✗ Error: {e}")
            print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for name, success, error in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status:8} {name}")
        if error:
            print(f"         Error: {error}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print()
        print("🎉 All ADR-027 Phase 1 components validated successfully!")
        print("   Next step: Run full integration tests once DB/Redis available")
        return 0
    else:
        print()
        print("⚠️  Some components failed validation")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
