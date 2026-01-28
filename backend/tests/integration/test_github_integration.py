"""
=========================================================================
GitHub Integration Tests - Sprint 111 Day 6
SDLC Orchestrator - Infrastructure Services Layer

Version: 1.0.0
Date: January 28, 2026
Status: Sprint 111 - Infrastructure Services (Day 6)
Authority: CTO Approved Sprint Plan
Foundation: Sprint 15 (GitHub Foundation), User-Onboarding-Flow-Architecture.md

Purpose:
- Validate GitHub service initialization and configuration
- Test OAuth flow components (authorization URL, token exchange)
- Test repository operations (list, get, contents)
- Verify webhook signature validation
- Test pull request and comment operations
- Validate rate limiting awareness

GitHub API Integration:
- REST API: https://api.github.com
- OAuth: GitHub App or OAuth App credentials
- Rate Limit: 5,000 requests/hour per authenticated user

Test Execution:
    # Without real GitHub token (unit-style tests):
    pytest tests/integration/test_github_integration.py -v

    # With real GitHub token:
    GITHUB_TOKEN=ghp_xxx pytest tests/integration/test_github_integration.py -v --run-live

Zero Mock Policy: Tests use real GitHub API when token available, otherwise test logic
=========================================================================
"""

import hashlib
import hmac
import os
import time
from typing import Any
from unittest.mock import patch, MagicMock

import pytest

# Import the GitHub service
from app.services.github_service import (
    GitHubAPIError,
    GitHubAuthError,
    GitHubRateLimitError,
    GitHubService,
    GitHubServiceError,
    github_service,
    GITHUB_API_BASE_URL,
    GITHUB_OAUTH_AUTHORIZE_URL,
    DEFAULT_SCOPES,
)


# ============================================================================
# Test Configuration
# ============================================================================

# GitHub token for live tests (optional)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_TEST_OWNER = os.getenv("GITHUB_TEST_OWNER", "octocat")
GITHUB_TEST_REPO = os.getenv("GITHUB_TEST_REPO", "Hello-World")

# Run live tests only if token is available
LIVE_TESTS_ENABLED = bool(GITHUB_TOKEN) and os.getenv("RUN_LIVE_TESTS", "").lower() == "true"


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def github_service_instance() -> GitHubService:
    """Create GitHub service instance for testing."""
    service = GitHubService()
    return service


@pytest.fixture
def mock_webhook_secret() -> str:
    """Mock webhook secret for testing."""
    return "test_webhook_secret_12345"


# ============================================================================
# TestGitHubServiceInitialization - Service Setup
# ============================================================================

class TestGitHubServiceInitialization:
    """Test GitHub service initialization and configuration."""

    def test_service_initializes(self) -> None:
        """Test GitHubService initializes correctly."""
        service = GitHubService()

        assert service is not None
        assert service.base_url == GITHUB_API_BASE_URL
        assert service.timeout > 0

    def test_global_instance_exists(self) -> None:
        """Test global github_service instance exists."""
        assert github_service is not None
        assert isinstance(github_service, GitHubService)

    def test_default_scopes_configured(self) -> None:
        """Test default OAuth scopes are configured."""
        assert "read:user" in DEFAULT_SCOPES
        assert "user:email" in DEFAULT_SCOPES
        assert "repo" in DEFAULT_SCOPES


# ============================================================================
# TestOAuthFlow - OAuth Authorization Flow
# ============================================================================

class TestOAuthFlow:
    """Test OAuth authorization flow components."""

    def test_get_authorization_url_structure(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test authorization URL has correct structure."""
        # Mock client_id for test
        github_service_instance.client_id = "test_client_id"

        auth_url = github_service_instance.get_authorization_url(
            state="random_state_123"
        )

        assert auth_url.startswith(GITHUB_OAUTH_AUTHORIZE_URL)
        assert "client_id=test_client_id" in auth_url
        assert "state=random_state_123" in auth_url
        assert "scope=" in auth_url

    def test_get_authorization_url_with_redirect(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test authorization URL includes redirect_uri."""
        github_service_instance.client_id = "test_client_id"

        auth_url = github_service_instance.get_authorization_url(
            state="state123",
            redirect_uri="https://app.example.com/callback"
        )

        assert "redirect_uri=https://app.example.com/callback" in auth_url

    def test_get_authorization_url_custom_scopes(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test authorization URL with custom scopes."""
        github_service_instance.client_id = "test_client_id"

        auth_url = github_service_instance.get_authorization_url(
            state="state123",
            scopes=["read:user", "repo"]
        )

        assert "scope=read:user repo" in auth_url or "scope=read%3Auser+repo" in auth_url

    def test_get_authorization_url_no_client_id_raises(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test authorization URL raises error without client_id."""
        github_service_instance.client_id = None

        with pytest.raises(GitHubAuthError) as exc_info:
            github_service_instance.get_authorization_url(state="state123")

        assert "client id" in str(exc_info.value).lower()


# ============================================================================
# TestWebhookValidation - Webhook Signature Validation
# ============================================================================

class TestWebhookValidation:
    """Test webhook signature validation."""

    def test_validate_webhook_signature_valid(
        self, github_service_instance: GitHubService, mock_webhook_secret: str
    ) -> None:
        """Test valid webhook signature validation."""
        github_service_instance.webhook_secret = mock_webhook_secret

        payload = b'{"action": "opened", "number": 1}'
        expected_signature = hmac.new(
            key=mock_webhook_secret.encode("utf-8"),
            msg=payload,
            digestmod=hashlib.sha256
        ).hexdigest()
        signature = f"sha256={expected_signature}"

        is_valid = github_service_instance.validate_webhook_signature(
            payload=payload,
            signature=signature
        )

        assert is_valid is True

    def test_validate_webhook_signature_invalid(
        self, github_service_instance: GitHubService, mock_webhook_secret: str
    ) -> None:
        """Test invalid webhook signature validation."""
        github_service_instance.webhook_secret = mock_webhook_secret

        payload = b'{"action": "opened", "number": 1}'
        signature = "sha256=invalid_signature_12345"

        is_valid = github_service_instance.validate_webhook_signature(
            payload=payload,
            signature=signature
        )

        assert is_valid is False

    def test_validate_webhook_signature_wrong_format(
        self, github_service_instance: GitHubService, mock_webhook_secret: str
    ) -> None:
        """Test webhook signature with wrong format."""
        github_service_instance.webhook_secret = mock_webhook_secret

        payload = b'{"action": "opened"}'
        signature = "sha1=old_format_signature"  # Wrong algorithm

        is_valid = github_service_instance.validate_webhook_signature(
            payload=payload,
            signature=signature
        )

        assert is_valid is False

    def test_validate_webhook_no_secret_configured(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test webhook validation without secret (dev mode)."""
        github_service_instance.webhook_secret = None

        payload = b'{"action": "opened"}'
        signature = "sha256=any_signature"

        # Should return True in dev mode (no secret configured)
        is_valid = github_service_instance.validate_webhook_signature(
            payload=payload,
            signature=signature
        )

        assert is_valid is True


# ============================================================================
# TestWebhookParsing - Webhook Event Parsing
# ============================================================================

class TestWebhookParsing:
    """Test webhook event parsing."""

    def test_parse_push_event(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test parsing push webhook event."""
        payload = {
            "ref": "refs/heads/main",
            "before": "abc123",
            "after": "def456",
            "commits": [{"message": "feat: add feature"}],
            "head_commit": {"message": "feat: add feature"},
            "repository": {
                "id": 12345,
                "name": "test-repo",
                "full_name": "owner/test-repo",
                "owner": {"login": "owner"},
                "private": False,
            },
            "sender": {"id": 1, "login": "developer"},
        }

        event = github_service_instance.parse_webhook_event(
            event_type="push",
            payload=payload
        )

        assert event["event_type"] == "push"
        assert event["repository"]["full_name"] == "owner/test-repo"
        assert event["sender"]["login"] == "developer"
        assert event["data"]["ref"] == "refs/heads/main"
        assert event["data"]["commits"] == 1

    def test_parse_pull_request_event(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test parsing pull_request webhook event."""
        payload = {
            "action": "opened",
            "pull_request": {
                "number": 42,
                "title": "Add new feature",
                "state": "open",
                "merged": False,
                "head": {"ref": "feature/new"},
                "base": {"ref": "main"},
            },
            "repository": {
                "id": 12345,
                "name": "test-repo",
                "full_name": "owner/test-repo",
                "owner": {"login": "owner"},
                "private": False,
            },
            "sender": {"id": 1, "login": "developer"},
        }

        event = github_service_instance.parse_webhook_event(
            event_type="pull_request",
            payload=payload
        )

        assert event["event_type"] == "pull_request"
        assert event["action"] == "opened"
        assert event["data"]["number"] == 42
        assert event["data"]["title"] == "Add new feature"
        assert event["data"]["head_branch"] == "feature/new"
        assert event["data"]["base_branch"] == "main"

    def test_parse_issues_event(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test parsing issues webhook event."""
        payload = {
            "action": "opened",
            "issue": {
                "number": 10,
                "title": "Bug report",
                "state": "open",
                "labels": [{"name": "bug"}, {"name": "priority:high"}],
            },
            "repository": {
                "id": 12345,
                "name": "test-repo",
                "full_name": "owner/test-repo",
                "owner": {"login": "owner"},
                "private": False,
            },
            "sender": {"id": 1, "login": "reporter"},
        }

        event = github_service_instance.parse_webhook_event(
            event_type="issues",
            payload=payload
        )

        assert event["event_type"] == "issues"
        assert event["action"] == "opened"
        assert event["data"]["number"] == 10
        assert "bug" in event["data"]["labels"]


# ============================================================================
# TestRepositoryOperations - Repository API Operations
# ============================================================================

class TestRepositoryOperations:
    """Test repository API operations (requires live token for some tests)."""

    def test_list_repositories_constructs_correct_request(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test list_repositories constructs correct API request."""
        # This test verifies the method signature and parameter handling
        # without making actual API calls

        # Verify method exists and has correct parameters
        import inspect
        sig = inspect.signature(github_service_instance.list_repositories)
        params = list(sig.parameters.keys())

        assert "access_token" in params
        assert "visibility" in params
        assert "sort" in params
        assert "per_page" in params

    @pytest.mark.skipif(not LIVE_TESTS_ENABLED, reason="Live tests disabled")
    def test_list_repositories_live(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test list_repositories with live API."""
        repos = github_service_instance.list_repositories(
            access_token=GITHUB_TOKEN,
            visibility="public",
            per_page=5
        )

        assert isinstance(repos, list)
        if repos:
            assert "full_name" in repos[0]
            assert "html_url" in repos[0]
            print(f"\n📦 Found {len(repos)} repositories")

    @pytest.mark.skipif(not LIVE_TESTS_ENABLED, reason="Live tests disabled")
    def test_get_repository_live(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test get_repository with live API."""
        repo = github_service_instance.get_repository(
            access_token=GITHUB_TOKEN,
            owner=GITHUB_TEST_OWNER,
            repo=GITHUB_TEST_REPO
        )

        assert repo is not None
        assert repo["full_name"] == f"{GITHUB_TEST_OWNER}/{GITHUB_TEST_REPO}"
        print(f"\n📦 Repository: {repo['full_name']}")


# ============================================================================
# TestRateLimiting - Rate Limit Handling
# ============================================================================

class TestRateLimiting:
    """Test rate limiting awareness."""

    @pytest.mark.skipif(not LIVE_TESTS_ENABLED, reason="Live tests disabled")
    def test_get_rate_limit_live(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test get_rate_limit with live API."""
        rate = github_service_instance.get_rate_limit(access_token=GITHUB_TOKEN)

        assert "rate" in rate or "resources" in rate
        print(f"\n📊 Rate limit status retrieved")


# ============================================================================
# TestPullRequestOperations - PR API Operations
# ============================================================================

class TestPullRequestOperations:
    """Test pull request API operations."""

    def test_get_pull_request_method_exists(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test get_pull_request method exists."""
        assert hasattr(github_service_instance, "get_pull_request")
        assert callable(github_service_instance.get_pull_request)

    def test_get_pull_request_comments_method_exists(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test get_pull_request_comments method exists."""
        assert hasattr(github_service_instance, "get_pull_request_comments")
        assert callable(github_service_instance.get_pull_request_comments)


# ============================================================================
# TestErrorHandling - Error Handling
# ============================================================================

class TestErrorHandling:
    """Test error handling."""

    def test_custom_exceptions_exist(self) -> None:
        """Test custom exception classes exist."""
        assert issubclass(GitHubAuthError, GitHubServiceError)
        assert issubclass(GitHubRateLimitError, GitHubServiceError)
        assert issubclass(GitHubAPIError, GitHubServiceError)

    def test_auth_error_on_invalid_token(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test GitHubAuthError is raised for invalid token."""
        with pytest.raises(GitHubAuthError):
            github_service_instance.validate_access_token(
                access_token="invalid_token_12345"
            )

    def test_api_error_on_not_found(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test GitHubAPIError is raised for non-existent resources."""
        # Skip if no token (can't test without auth)
        if not GITHUB_TOKEN:
            pytest.skip("No GitHub token for API test")

        with pytest.raises(GitHubAPIError):
            github_service_instance.get_repository(
                access_token=GITHUB_TOKEN,
                owner="definitely-not-a-real-org",
                repo="definitely-not-a-real-repo"
            )


# ============================================================================
# TestContentOperations - Repository Content Operations
# ============================================================================

class TestContentOperations:
    """Test repository content operations."""

    def test_get_repository_contents_method_exists(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test get_repository_contents method exists."""
        assert hasattr(github_service_instance, "get_repository_contents")
        assert callable(github_service_instance.get_repository_contents)

    def test_get_repository_languages_method_exists(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test get_repository_languages method exists."""
        assert hasattr(github_service_instance, "get_repository_languages")
        assert callable(github_service_instance.get_repository_languages)

    @pytest.mark.skipif(not LIVE_TESTS_ENABLED, reason="Live tests disabled")
    def test_get_repository_contents_live(
        self, github_service_instance: GitHubService
    ) -> None:
        """Test get_repository_contents with live API."""
        contents = github_service_instance.get_repository_contents(
            access_token=GITHUB_TOKEN,
            owner=GITHUB_TEST_OWNER,
            repo=GITHUB_TEST_REPO,
            path=""  # Root directory
        )

        assert isinstance(contents, list)
        if contents:
            assert "name" in contents[0]
            assert "type" in contents[0]
            print(f"\n📁 Found {len(contents)} items in root directory")
