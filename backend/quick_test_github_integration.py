#!/usr/bin/env python3
"""
=========================================================================
Quick GitHub Integration Test - Sprint 111 Day 6
SDLC Orchestrator - Infrastructure Services Layer

Version: 1.0.0
Date: January 28, 2026

Purpose:
- Quick validation of GitHub service integration
- Test without full pytest setup
- Verify OAuth, webhooks, and API operations

Usage:
    # Without GitHub token (logic tests only):
    python quick_test_github_integration.py

    # With GitHub token (live API tests):
    GITHUB_TOKEN=ghp_xxx python quick_test_github_integration.py

Expected Output:
    ✅ Service Initialization: PASSED
    ✅ OAuth URL Generation: PASSED
    ✅ Webhook Signature Validation: PASSED
    ✅ Webhook Event Parsing: PASSED
    ✅ API Error Handling: PASSED
    ⏭️ Live API Test: SKIPPED (no token)

    Summary: 5 passed, 0 failed, 1 skipped
=========================================================================
"""

import hashlib
import hmac
import os
import sys
from typing import Any

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.github_service import (
    GitHubAPIError,
    GitHubAuthError,
    GitHubService,
    github_service,
)


# ============================================================================
# Configuration
# ============================================================================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
WEBHOOK_SECRET = "test_secret_12345"


# ============================================================================
# Test Functions
# ============================================================================

def test_service_initialization() -> tuple[bool, str]:
    """Test 1: Service initializes correctly."""
    try:
        service = GitHubService()

        if not service.base_url:
            return False, "No base URL configured"
        if service.timeout <= 0:
            return False, "Invalid timeout"
        if github_service is None:
            return False, "Global instance not created"

        return True, "Service initialized correctly"

    except Exception as e:
        return False, f"Exception: {str(e)}"


def test_oauth_url_generation() -> tuple[bool, str]:
    """Test 2: OAuth URL generation works."""
    try:
        service = GitHubService()
        service.client_id = "test_client_id"

        auth_url = service.get_authorization_url(
            state="test_state_123",
            redirect_uri="https://app.example.com/callback",
            scopes=["read:user", "repo"]
        )

        if "client_id=test_client_id" not in auth_url:
            return False, "Missing client_id in URL"
        if "state=test_state_123" not in auth_url:
            return False, "Missing state in URL"
        if "redirect_uri=" not in auth_url:
            return False, "Missing redirect_uri in URL"

        return True, "OAuth URL generated correctly"

    except Exception as e:
        return False, f"Exception: {str(e)}"


def test_webhook_signature_validation() -> tuple[bool, str]:
    """Test 3: Webhook signature validation works."""
    try:
        service = GitHubService()
        service.webhook_secret = WEBHOOK_SECRET

        payload = b'{"action": "opened", "number": 1}'
        expected_signature = hmac.new(
            key=WEBHOOK_SECRET.encode("utf-8"),
            msg=payload,
            digestmod=hashlib.sha256
        ).hexdigest()
        valid_signature = f"sha256={expected_signature}"

        # Test valid signature
        if not service.validate_webhook_signature(payload, valid_signature):
            return False, "Valid signature rejected"

        # Test invalid signature
        if service.validate_webhook_signature(payload, "sha256=invalid"):
            return False, "Invalid signature accepted"

        return True, "Signature validation works"

    except Exception as e:
        return False, f"Exception: {str(e)}"


def test_webhook_event_parsing() -> tuple[bool, str]:
    """Test 4: Webhook event parsing works."""
    try:
        service = GitHubService()

        # Test push event
        push_payload = {
            "ref": "refs/heads/main",
            "commits": [{"message": "test"}],
            "head_commit": {"message": "test"},
            "repository": {
                "id": 1, "name": "test", "full_name": "owner/test",
                "owner": {"login": "owner"}, "private": False
            },
            "sender": {"id": 1, "login": "user"},
        }

        push_event = service.parse_webhook_event("push", push_payload)
        if push_event["event_type"] != "push":
            return False, "Push event type wrong"
        if push_event["data"]["ref"] != "refs/heads/main":
            return False, "Push ref not parsed"

        # Test PR event
        pr_payload = {
            "action": "opened",
            "pull_request": {
                "number": 42, "title": "Test PR", "state": "open",
                "merged": False, "head": {"ref": "feature"},
                "base": {"ref": "main"}
            },
            "repository": {
                "id": 1, "name": "test", "full_name": "owner/test",
                "owner": {"login": "owner"}, "private": False
            },
            "sender": {"id": 1, "login": "user"},
        }

        pr_event = service.parse_webhook_event("pull_request", pr_payload)
        if pr_event["data"]["number"] != 42:
            return False, "PR number not parsed"

        return True, "Event parsing works (push, PR)"

    except Exception as e:
        return False, f"Exception: {str(e)}"


def test_api_error_handling() -> tuple[bool, str]:
    """Test 5: API error handling works."""
    try:
        service = GitHubService()

        # Test that auth error is raised for invalid token
        try:
            service.validate_access_token("invalid_token")
            return False, "No error for invalid token"
        except GitHubAuthError:
            pass  # Expected
        except GitHubAPIError:
            pass  # Also acceptable

        return True, "Error handling works"

    except Exception as e:
        return False, f"Exception: {str(e)}"


def test_live_api() -> tuple[bool, str]:
    """Test 6: Live API test (requires GITHUB_TOKEN)."""
    if not GITHUB_TOKEN:
        return None, "No GITHUB_TOKEN (skipped)"  # type: ignore

    try:
        service = GitHubService()

        # Validate token
        user = service.validate_access_token(GITHUB_TOKEN)

        if not user.get("login"):
            return False, "No login in user response"

        # Get rate limit
        rate = service.get_rate_limit(GITHUB_TOKEN)

        return True, f"Authenticated as {user['login']}"

    except Exception as e:
        return False, f"Exception: {str(e)}"


# ============================================================================
# Main
# ============================================================================

def main() -> int:
    """Run all quick tests."""
    print("=" * 70)
    print("GitHub Integration Test - Sprint 111 Day 6")
    print("=" * 70)
    print(f"\nGitHub Token: {'Configured' if GITHUB_TOKEN else 'Not configured'}")
    print("")

    tests = [
        ("Service Initialization", test_service_initialization),
        ("OAuth URL Generation", test_oauth_url_generation),
        ("Webhook Signature Validation", test_webhook_signature_validation),
        ("Webhook Event Parsing", test_webhook_event_parsing),
        ("API Error Handling", test_api_error_handling),
        ("Live API Test", test_live_api),
    ]

    passed = 0
    failed = 0
    skipped = 0

    results = []

    for name, test_func in tests:
        try:
            success, message = test_func()

            if success is None:
                status = "⏭️ SKIPPED"
                skipped += 1
            elif success:
                status = "✅ PASSED"
                passed += 1
            else:
                status = "❌ FAILED"
                failed += 1

            results.append((name, status, message))

        except Exception as e:
            results.append((name, "❌ ERROR", str(e)))
            failed += 1

    # Print results
    print("Results:")
    print("-" * 70)
    for name, status, message in results:
        print(f"  {status} {name}: {message}")

    print("")
    print("=" * 70)
    print(f"Summary: {passed} passed, {failed} failed, {skipped} skipped")
    print("=" * 70)

    # Additional info
    print("")
    if failed > 0:
        print("⚠️ Some tests failed. Check the error messages above.")
    elif skipped > 0 and not GITHUB_TOKEN:
        print("💡 To run live API tests, set GITHUB_TOKEN environment variable:")
        print("   export GITHUB_TOKEN=ghp_your_token_here")
        print("   python quick_test_github_integration.py")
    else:
        print("✅ All tests passed! GitHub integration is working.")

    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
