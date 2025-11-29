"""
=========================================================================
Unit Tests for GitHub Service - Sprint 16 Day 1
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: December 3, 2025
Status: ACTIVE - Sprint 16 (Testing & Documentation)
Authority: QA Lead + Backend Lead
Foundation: Sprint 16 Plan, GitHub Service Implementation
Framework: SDLC 4.9 Complete Lifecycle

Test Coverage:
- OAuth URL generation
- Token exchange
- Token validation
- Repository operations
- Webhook signature validation
- Rate limiting handling
- Error handling

Zero Mock Policy:
- ✅ External APIs mocked (GitHub API)
- ✅ Internal logic tested with real implementations
- ✅ No TODO placeholders
=========================================================================
"""

import hashlib
import hmac
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from requests import Response
from requests.exceptions import Timeout, RequestException

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend"))

from app.services.github_service import (
    GitHubService,
    GitHubAuthError,
    GitHubRateLimitError,
    GitHubAPIError,
    GITHUB_OAUTH_AUTHORIZE_URL,
    GITHUB_OAUTH_TOKEN_URL,
    DEFAULT_SCOPES,
)


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def github_service():
    """Create GitHubService instance with test credentials."""
    with patch("app.services.github_service.settings") as mock_settings:
        mock_settings.GITHUB_CLIENT_ID = "test_client_id"
        mock_settings.GITHUB_CLIENT_SECRET = "test_client_secret"
        mock_settings.GITHUB_WEBHOOK_SECRET = "test_webhook_secret"

        service = GitHubService()
        service.client_id = "test_client_id"
        service.client_secret = "test_client_secret"
        service.webhook_secret = "test_webhook_secret"
        return service


@pytest.fixture
def mock_user_response():
    """Mock GitHub user response data."""
    return {
        "id": 12345,
        "login": "testuser",
        "email": "test@example.com",
        "name": "Test User",
        "avatar_url": "https://avatars.githubusercontent.com/u/12345",
    }


@pytest.fixture
def mock_repo_response():
    """Mock GitHub repository response data."""
    return {
        "id": 67890,
        "name": "test-repo",
        "full_name": "testuser/test-repo",
        "description": "A test repository",
        "html_url": "https://github.com/testuser/test-repo",
        "language": "Python",
        "default_branch": "main",
        "private": False,
        "fork": False,
        "stargazers_count": 100,
        "updated_at": "2025-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_repos_list_response(mock_repo_response):
    """Mock GitHub repositories list response."""
    return [mock_repo_response]


# ============================================================================
# OAUTH URL GENERATION TESTS
# ============================================================================


class TestGetAuthorizationUrl:
    """Tests for get_authorization_url method."""

    def test_generates_valid_url_with_required_params(self, github_service):
        """Test OAuth URL generation with required parameters."""
        state = "random_state_123"

        url = github_service.get_authorization_url(state=state)

        assert GITHUB_OAUTH_AUTHORIZE_URL in url
        assert f"client_id={github_service.client_id}" in url
        assert f"state={state}" in url
        assert "scope=" in url

    def test_includes_default_scopes(self, github_service):
        """Test that default scopes are included in URL."""
        url = github_service.get_authorization_url(state="test_state")

        # Default scopes should be included
        expected_scope = " ".join(DEFAULT_SCOPES)
        # URL encoding replaces space with + or %20
        assert "read:user" in url or "read%3Auser" in url

    def test_includes_custom_scopes(self, github_service):
        """Test OAuth URL with custom scopes."""
        custom_scopes = ["repo", "user", "gist"]

        url = github_service.get_authorization_url(
            state="test_state",
            scopes=custom_scopes
        )

        assert "repo" in url
        assert "user" in url
        assert "gist" in url

    def test_includes_redirect_uri_when_provided(self, github_service):
        """Test OAuth URL includes redirect_uri when provided."""
        redirect_uri = "https://example.com/callback"

        url = github_service.get_authorization_url(
            state="test_state",
            redirect_uri=redirect_uri
        )

        assert "redirect_uri=" in url
        assert "example.com" in url

    def test_raises_error_when_client_id_missing(self, github_service):
        """Test that missing client ID raises GitHubAuthError."""
        github_service.client_id = None

        with pytest.raises(GitHubAuthError) as exc_info:
            github_service.get_authorization_url(state="test")

        assert "client ID not configured" in str(exc_info.value)


# ============================================================================
# TOKEN EXCHANGE TESTS
# ============================================================================


class TestExchangeCodeForToken:
    """Tests for exchange_code_for_token method."""

    def test_successful_token_exchange(self, github_service):
        """Test successful OAuth code to token exchange."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "gho_test_token_123",
            "token_type": "bearer",
            "scope": "read:user,user:email,repo",
        }

        with patch("requests.post", return_value=mock_response):
            token_data = github_service.exchange_code_for_token(code="auth_code_123")

        assert "access_token" in token_data
        assert token_data["access_token"] == "gho_test_token_123"
        assert token_data["token_type"] == "bearer"

    def test_exchange_with_redirect_uri(self, github_service):
        """Test token exchange includes redirect_uri in request."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "gho_test"}

        with patch("requests.post", return_value=mock_response) as mock_post:
            github_service.exchange_code_for_token(
                code="auth_code",
                redirect_uri="https://example.com/callback"
            )

        # Verify redirect_uri was passed
        call_kwargs = mock_post.call_args
        assert "redirect_uri" in call_kwargs.kwargs.get("data", {})

    def test_raises_error_on_oauth_error_response(self, github_service):
        """Test that OAuth error response raises GitHubAuthError."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "error": "bad_verification_code",
            "error_description": "The code passed is incorrect or expired.",
        }

        with patch("requests.post", return_value=mock_response):
            with pytest.raises(GitHubAuthError) as exc_info:
                github_service.exchange_code_for_token(code="invalid_code")

        assert "incorrect or expired" in str(exc_info.value)

    def test_raises_error_on_http_error(self, github_service):
        """Test that HTTP error raises GitHubAuthError."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 400
        mock_response.text = "Bad Request"

        with patch("requests.post", return_value=mock_response):
            with pytest.raises(GitHubAuthError) as exc_info:
                github_service.exchange_code_for_token(code="test_code")

        assert "Token exchange failed" in str(exc_info.value)

    def test_raises_error_on_timeout(self, github_service):
        """Test that request timeout raises GitHubAuthError."""
        with patch("requests.post", side_effect=Timeout("Connection timed out")):
            with pytest.raises(GitHubAuthError) as exc_info:
                github_service.exchange_code_for_token(code="test_code")

        assert "timed out" in str(exc_info.value)

    def test_raises_error_on_request_exception(self, github_service):
        """Test that request exception raises GitHubAuthError."""
        with patch("requests.post", side_effect=RequestException("Network error")):
            with pytest.raises(GitHubAuthError) as exc_info:
                github_service.exchange_code_for_token(code="test_code")

        assert "request failed" in str(exc_info.value)

    def test_raises_error_when_credentials_missing(self, github_service):
        """Test that missing credentials raises GitHubAuthError."""
        github_service.client_id = None

        with pytest.raises(GitHubAuthError) as exc_info:
            github_service.exchange_code_for_token(code="test_code")

        assert "credentials not configured" in str(exc_info.value)


# ============================================================================
# TOKEN VALIDATION TESTS
# ============================================================================


class TestValidateAccessToken:
    """Tests for validate_access_token method."""

    def test_valid_token_returns_user_info(self, github_service, mock_user_response):
        """Test that valid token returns user information."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_user_response
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}
        mock_response.text = '{"id": 12345}'

        with patch("requests.request", return_value=mock_response):
            user_info = github_service.validate_access_token("valid_token")

        assert user_info["id"] == 12345
        assert user_info["login"] == "testuser"
        assert user_info["email"] == "test@example.com"

    def test_invalid_token_raises_auth_error(self, github_service):
        """Test that invalid token raises GitHubAuthError."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 401
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}

        with patch("requests.request", return_value=mock_response):
            with pytest.raises(GitHubAuthError) as exc_info:
                github_service.validate_access_token("invalid_token")

        # _make_request raises "Invalid or expired access token" for 401
        assert "Invalid or expired access token" in str(exc_info.value)


# ============================================================================
# REPOSITORY OPERATIONS TESTS
# ============================================================================


class TestListRepositories:
    """Tests for list_repositories method."""

    def test_returns_list_of_repos(self, github_service, mock_repos_list_response):
        """Test that list_repositories returns repository list."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_repos_list_response
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}
        mock_response.text = '[{"id": 67890}]'

        with patch("requests.request", return_value=mock_response):
            repos = github_service.list_repositories(access_token="valid_token")

        assert isinstance(repos, list)
        assert len(repos) == 1
        assert repos[0]["id"] == 67890
        assert repos[0]["full_name"] == "testuser/test-repo"

    def test_pagination_params_passed_correctly(self, github_service):
        """Test that pagination parameters are passed to API."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}
        mock_response.text = '[]'

        with patch("requests.request", return_value=mock_response) as mock_request:
            github_service.list_repositories(
                access_token="token",
                visibility="public",
                sort="created",
                direction="asc",
                per_page=50,
                page=2
            )

        call_kwargs = mock_request.call_args
        params = call_kwargs.kwargs.get("params", {})
        assert params["visibility"] == "public"
        assert params["sort"] == "created"
        assert params["direction"] == "asc"
        assert params["per_page"] == 50
        assert params["page"] == 2

    def test_per_page_capped_at_100(self, github_service):
        """Test that per_page is capped at 100 (GitHub API limit)."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}
        mock_response.text = '[]'

        with patch("requests.request", return_value=mock_response) as mock_request:
            github_service.list_repositories(
                access_token="token",
                per_page=200  # Exceeds limit
            )

        call_kwargs = mock_request.call_args
        params = call_kwargs.kwargs.get("params", {})
        assert params["per_page"] == 100  # Should be capped


class TestGetRepository:
    """Tests for get_repository method."""

    def test_returns_repository_details(self, github_service, mock_repo_response):
        """Test that get_repository returns repository details."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_repo_response
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}
        mock_response.text = '{"id": 67890}'

        with patch("requests.request", return_value=mock_response):
            repo = github_service.get_repository(
                access_token="token",
                owner="testuser",
                repo="test-repo"
            )

        assert repo["id"] == 67890
        assert repo["name"] == "test-repo"
        assert repo["language"] == "Python"

    def test_raises_error_for_not_found_repo(self, github_service):
        """Test that non-existent repo raises GitHubAPIError."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 404
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}

        with patch("requests.request", return_value=mock_response):
            with pytest.raises(GitHubAPIError) as exc_info:
                github_service.get_repository(
                    access_token="token",
                    owner="nonexistent",
                    repo="repo"
                )

        assert "not found" in str(exc_info.value)


class TestGetRepositoryContents:
    """Tests for get_repository_contents method."""

    def test_returns_directory_contents(self, github_service):
        """Test that get_repository_contents returns file list."""
        mock_contents = [
            {"name": "README.md", "path": "README.md", "type": "file", "size": 1234},
            {"name": "src", "path": "src", "type": "dir", "size": 0},
        ]

        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_contents
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}
        mock_response.text = '[{"name": "README.md"}]'

        with patch("requests.request", return_value=mock_response):
            contents = github_service.get_repository_contents(
                access_token="token",
                owner="testuser",
                repo="test-repo",
                path=""
            )

        assert len(contents) == 2
        assert contents[0]["name"] == "README.md"
        assert contents[1]["type"] == "dir"

    def test_accepts_ref_parameter(self, github_service):
        """Test that ref parameter is passed to API."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}
        mock_response.text = '[]'

        with patch("requests.request", return_value=mock_response) as mock_request:
            github_service.get_repository_contents(
                access_token="token",
                owner="testuser",
                repo="test-repo",
                path="src",
                ref="develop"
            )

        call_kwargs = mock_request.call_args
        params = call_kwargs.kwargs.get("params", {})
        assert params["ref"] == "develop"


class TestGetRepositoryLanguages:
    """Tests for get_repository_languages method."""

    def test_returns_language_breakdown(self, github_service):
        """Test that get_repository_languages returns language stats."""
        mock_languages = {
            "Python": 123456,
            "TypeScript": 78901,
            "JavaScript": 45678,
        }

        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_languages
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}
        mock_response.text = '{"Python": 123456}'

        with patch("requests.request", return_value=mock_response):
            languages = github_service.get_repository_languages(
                access_token="token",
                owner="testuser",
                repo="test-repo"
            )

        assert languages["Python"] == 123456
        assert "TypeScript" in languages
        assert "JavaScript" in languages


# ============================================================================
# WEBHOOK SIGNATURE VALIDATION TESTS
# ============================================================================


class TestValidateWebhookSignature:
    """Tests for validate_webhook_signature method."""

    def test_valid_signature_returns_true(self, github_service):
        """Test that valid HMAC signature returns True."""
        payload = b'{"action": "created"}'
        secret = github_service.webhook_secret

        # Generate valid signature
        expected_signature = hmac.new(
            key=secret.encode("utf-8"),
            msg=payload,
            digestmod=hashlib.sha256,
        ).hexdigest()
        signature = f"sha256={expected_signature}"

        result = github_service.validate_webhook_signature(payload, signature)

        assert result is True

    def test_invalid_signature_returns_false(self, github_service):
        """Test that invalid signature returns False."""
        payload = b'{"action": "created"}'
        invalid_signature = "sha256=invalid_signature_here"

        result = github_service.validate_webhook_signature(payload, invalid_signature)

        assert result is False

    def test_missing_signature_prefix_returns_false(self, github_service):
        """Test that missing sha256= prefix returns False."""
        payload = b'{"action": "created"}'
        signature_without_prefix = "abc123"

        result = github_service.validate_webhook_signature(payload, signature_without_prefix)

        assert result is False

    def test_empty_signature_returns_false(self, github_service):
        """Test that empty signature returns False."""
        payload = b'{"action": "created"}'

        result = github_service.validate_webhook_signature(payload, "")

        assert result is False

    def test_none_signature_returns_false(self, github_service):
        """Test that None signature returns False."""
        payload = b'{"action": "created"}'

        result = github_service.validate_webhook_signature(payload, None)

        assert result is False

    def test_no_webhook_secret_allows_all(self, github_service):
        """Test that missing webhook secret allows all requests (dev mode)."""
        github_service.webhook_secret = None
        payload = b'{"action": "created"}'

        result = github_service.validate_webhook_signature(payload, "any_signature")

        assert result is True


# ============================================================================
# WEBHOOK EVENT PARSING TESTS
# ============================================================================


class TestParseWebhookEvent:
    """Tests for parse_webhook_event method."""

    def test_parses_push_event(self, github_service):
        """Test parsing of push webhook event."""
        payload = {
            "ref": "refs/heads/main",
            "before": "abc123",
            "after": "def456",
            "commits": [{"message": "First commit"}, {"message": "Second commit"}],
            "head_commit": {"message": "Second commit"},
            "repository": {
                "id": 12345,
                "name": "test-repo",
                "full_name": "testuser/test-repo",
                "owner": {"login": "testuser"},
                "private": False,
            },
            "sender": {"id": 67890, "login": "testuser"},
        }

        event = github_service.parse_webhook_event("push", payload)

        assert event["event_type"] == "push"
        assert event["repository"]["id"] == 12345
        assert event["sender"]["login"] == "testuser"
        assert event["data"]["ref"] == "refs/heads/main"
        assert event["data"]["commits"] == 2
        assert event["data"]["head_commit"] == "Second commit"

    def test_parses_pull_request_event(self, github_service):
        """Test parsing of pull_request webhook event."""
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
                "full_name": "testuser/test-repo",
                "owner": {"login": "testuser"},
                "private": False,
            },
            "sender": {"id": 67890, "login": "testuser"},
        }

        event = github_service.parse_webhook_event("pull_request", payload)

        assert event["event_type"] == "pull_request"
        assert event["action"] == "opened"
        assert event["data"]["number"] == 42
        assert event["data"]["title"] == "Add new feature"
        assert event["data"]["head_branch"] == "feature/new"
        assert event["data"]["base_branch"] == "main"

    def test_parses_issues_event(self, github_service):
        """Test parsing of issues webhook event."""
        payload = {
            "action": "opened",
            "issue": {
                "number": 99,
                "title": "Bug report",
                "state": "open",
                "labels": [{"name": "bug"}, {"name": "priority-high"}],
            },
            "repository": {
                "id": 12345,
                "name": "test-repo",
                "full_name": "testuser/test-repo",
                "owner": {"login": "testuser"},
                "private": False,
            },
            "sender": {"id": 67890, "login": "testuser"},
        }

        event = github_service.parse_webhook_event("issues", payload)

        assert event["event_type"] == "issues"
        assert event["action"] == "opened"
        assert event["data"]["number"] == 99
        assert event["data"]["labels"] == ["bug", "priority-high"]

    def test_parses_create_event(self, github_service):
        """Test parsing of create webhook event (branch/tag creation)."""
        payload = {
            "ref": "feature/new-feature",
            "ref_type": "branch",
            "repository": {
                "id": 12345,
                "name": "test-repo",
                "full_name": "testuser/test-repo",
                "owner": {"login": "testuser"},
                "private": False,
            },
            "sender": {"id": 67890, "login": "testuser"},
        }

        event = github_service.parse_webhook_event("create", payload)

        assert event["event_type"] == "create"
        assert event["data"]["ref"] == "feature/new-feature"
        assert event["data"]["ref_type"] == "branch"

    def test_parses_unknown_event_type(self, github_service):
        """Test parsing of unknown event type returns empty data."""
        payload = {
            "repository": {
                "id": 12345,
                "name": "test-repo",
                "full_name": "testuser/test-repo",
                "owner": {"login": "testuser"},
                "private": False,
            },
            "sender": {"id": 67890, "login": "testuser"},
        }

        event = github_service.parse_webhook_event("unknown_event", payload)

        assert event["event_type"] == "unknown_event"
        assert event["data"] == {}


# ============================================================================
# RATE LIMITING TESTS
# ============================================================================


class TestGetRateLimit:
    """Tests for get_rate_limit method."""

    def test_returns_rate_limit_info(self, github_service):
        """Test that get_rate_limit returns rate limit information."""
        mock_rate_limit = {
            "resources": {
                "core": {
                    "limit": 5000,
                    "remaining": 4999,
                    "reset": 1234567890,
                    "used": 1,
                }
            }
        }

        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_rate_limit
        mock_response.headers = {"X-RateLimit-Remaining": "4999"}
        mock_response.text = '{"resources": {}}'

        with patch("requests.request", return_value=mock_response):
            rate_info = github_service.get_rate_limit(access_token="token")

        assert "resources" in rate_info


class TestRateLimitHandling:
    """Tests for rate limit handling in _make_request."""

    def test_raises_rate_limit_error_when_exhausted(self, github_service):
        """Test that exhausted rate limit raises GitHubRateLimitError."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.headers = {
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": "1234567890",
        }
        mock_response.text = '{}'

        with patch("requests.request", return_value=mock_response):
            with pytest.raises(GitHubRateLimitError) as exc_info:
                github_service._make_request(
                    method="GET",
                    endpoint="/test",
                    access_token="token"
                )

        assert "Rate limit exceeded" in str(exc_info.value)

    def test_logs_warning_when_rate_limit_low(self, github_service):
        """Test that low rate limit logs warning but continues."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_response.headers = {
            "X-RateLimit-Remaining": "50",  # Below threshold
            "X-RateLimit-Reset": "1234567890",
        }
        mock_response.text = '{"data": "test"}'

        with patch("requests.request", return_value=mock_response):
            # Should not raise, just log warning
            result = github_service._make_request(
                method="GET",
                endpoint="/test",
                access_token="token"
            )

        assert result["data"] == "test"


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


class TestErrorHandling:
    """Tests for error handling in _make_request."""

    def test_handles_401_unauthorized(self, github_service):
        """Test that 401 response raises GitHubAuthError."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 401
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}

        with patch("requests.request", return_value=mock_response):
            with pytest.raises(GitHubAuthError) as exc_info:
                github_service._make_request(
                    method="GET",
                    endpoint="/user",
                    access_token="invalid_token"
                )

        assert "Invalid or expired access token" in str(exc_info.value)

    def test_handles_403_forbidden(self, github_service):
        """Test that 403 response raises GitHubAPIError."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 403
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}

        with patch("requests.request", return_value=mock_response):
            with pytest.raises(GitHubAPIError) as exc_info:
                github_service._make_request(
                    method="GET",
                    endpoint="/repos/private/repo",
                    access_token="token"
                )

        assert "Access forbidden" in str(exc_info.value)

    def test_handles_404_not_found(self, github_service):
        """Test that 404 response raises GitHubAPIError."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 404
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}

        with patch("requests.request", return_value=mock_response):
            with pytest.raises(GitHubAPIError) as exc_info:
                github_service._make_request(
                    method="GET",
                    endpoint="/repos/nonexistent/repo",
                    access_token="token"
                )

        assert "not found" in str(exc_info.value)

    def test_handles_server_error(self, github_service):
        """Test that 5xx responses raise GitHubAPIError."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Internal Server Error"}
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}

        with patch("requests.request", return_value=mock_response):
            with pytest.raises(GitHubAPIError) as exc_info:
                github_service._make_request(
                    method="GET",
                    endpoint="/user",
                    access_token="token"
                )

        assert "API error" in str(exc_info.value)

    def test_handles_timeout(self, github_service):
        """Test that timeout raises GitHubAPIError."""
        with patch("requests.request", side_effect=Timeout("Connection timed out")):
            with pytest.raises(GitHubAPIError) as exc_info:
                github_service._make_request(
                    method="GET",
                    endpoint="/user",
                    access_token="token"
                )

        assert "timed out" in str(exc_info.value)

    def test_handles_request_exception(self, github_service):
        """Test that request exception raises GitHubAPIError."""
        with patch("requests.request", side_effect=RequestException("Network error")):
            with pytest.raises(GitHubAPIError) as exc_info:
                github_service._make_request(
                    method="GET",
                    endpoint="/user",
                    access_token="token"
                )

        assert "Request failed" in str(exc_info.value)


# ============================================================================
# EDGE CASES TESTS
# ============================================================================


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_empty_response_body(self, github_service):
        """Test handling of empty response body."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 204  # No Content
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}
        mock_response.text = ""

        with patch("requests.request", return_value=mock_response):
            result = github_service._make_request(
                method="DELETE",
                endpoint="/repos/owner/repo",
                access_token="token"
            )

        assert result is None

    def test_large_repository_list(self, github_service):
        """Test handling of large repository list (100 repos)."""
        large_repo_list = [
            {"id": i, "name": f"repo-{i}", "full_name": f"user/repo-{i}"}
            for i in range(100)
        ]

        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = large_repo_list
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}
        mock_response.text = '[{"id": 0}]'

        with patch("requests.request", return_value=mock_response):
            repos = github_service.list_repositories(access_token="token")

        assert len(repos) == 100

    def test_special_characters_in_repo_name(self, github_service):
        """Test handling of special characters in repository name."""
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "name": "repo-with-dashes_and_underscores"}
        mock_response.headers = {"X-RateLimit-Remaining": "5000"}
        mock_response.text = '{"id": 1}'

        with patch("requests.request", return_value=mock_response) as mock_request:
            github_service.get_repository(
                access_token="token",
                owner="user",
                repo="repo-with-dashes_and_underscores"
            )

        # Verify correct URL was called
        call_args = mock_request.call_args
        assert "repo-with-dashes_and_underscores" in call_args.kwargs["url"]

    def test_unicode_in_commit_message(self, github_service):
        """Test handling of unicode characters in webhook payload."""
        payload = {
            "ref": "refs/heads/main",
            "commits": [{"message": "Fix: Handle émoji 🚀 and special chars éàü"}],
            "head_commit": {"message": "Fix: Handle émoji 🚀 and special chars éàü"},
            "repository": {
                "id": 12345,
                "name": "test-repo",
                "full_name": "testuser/test-repo",
                "owner": {"login": "testuser"},
                "private": False,
            },
            "sender": {"id": 67890, "login": "testuser"},
        }

        event = github_service.parse_webhook_event("push", payload)

        assert "🚀" in event["data"]["head_commit"]
        assert "émoji" in event["data"]["head_commit"]
