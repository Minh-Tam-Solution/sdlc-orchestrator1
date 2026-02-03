"""Unit tests for GitHub adapter."""

import hashlib
import hmac
import time
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, mock_open, patch

import jwt
import pytest

from sdlcctl.services.mcp.github_adapter import (
    GitHubAdapter,
    GitHubAPIError,
    GitHubSignatureError,
)


@pytest.fixture
def github_adapter(tmp_path):
    """Create GitHubAdapter instance for testing."""
    # Create a temporary private key file
    private_key_path = tmp_path / "github-app.pem"
    private_key_content = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0Z6Rp0Z6Rp0Z6Rp0Z6Rp0Z6Rp0Z6Rp0Z6Rp0Z6Rp0Z6Rp0Z
-----END RSA PRIVATE KEY-----"""
    private_key_path.write_text(private_key_content)

    return GitHubAdapter(
        app_id="123456",
        private_key_path=str(private_key_path)
    )


@pytest.fixture
def mock_jwt_token():
    """Generate a mock JWT token for testing."""
    return "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MDY4MjAwMDAsImV4cCI6MTcwNjgyMDYwMCwiaXNzIjoiMTIzNDU2In0.signature"


@pytest.fixture
def mock_github_response():
    """Mock successful GitHub API response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}
    return mock_response


class TestGitHubAdapter:
    """Tests for GitHubAdapter class."""

    def test_init(self, tmp_path):
        """Test GitHubAdapter initialization."""
        private_key_path = tmp_path / "test.pem"
        private_key_path.write_text("test key")

        adapter = GitHubAdapter(
            app_id="123456",
            private_key_path=str(private_key_path)
        )

        assert adapter.app_id == "123456"
        assert adapter.private_key_path == str(private_key_path)
        assert adapter.api_base_url == "https://api.github.com"
        assert adapter._jwt_token is None
        assert adapter._jwt_expires_at is None

    def test_load_private_key_success(self, github_adapter):
        """Test loading private key successfully."""
        private_key = github_adapter._load_private_key()

        assert "BEGIN RSA PRIVATE KEY" in private_key
        assert "END RSA PRIVATE KEY" in private_key

    def test_load_private_key_file_not_found(self, tmp_path):
        """Test loading private key when file doesn't exist."""
        adapter = GitHubAdapter(
            app_id="123456",
            private_key_path=str(tmp_path / "nonexistent.pem")
        )

        with pytest.raises(GitHubAPIError) as exc_info:
            adapter._load_private_key()

        assert "Failed to load private key" in str(exc_info.value)

    @patch('sdlcctl.services.mcp.github_adapter.jwt.encode')
    def test_generate_jwt_success(self, mock_jwt_encode, github_adapter):
        """Test JWT generation successfully."""
        mock_jwt_encode.return_value = "mock-jwt-token"

        token = github_adapter._generate_jwt()

        assert token == "mock-jwt-token"
        assert github_adapter._jwt_token == "mock-jwt-token"
        assert github_adapter._jwt_expires_at is not None

        # Verify JWT payload
        call_args = mock_jwt_encode.call_args
        payload = call_args[0][0]
        assert payload["iss"] == "123456"
        assert "iat" in payload
        assert "exp" in payload

    @patch('sdlcctl.services.mcp.github_adapter.jwt.encode')
    def test_generate_jwt_cached(self, mock_jwt_encode, github_adapter):
        """Test JWT caching mechanism."""
        # First call generates JWT
        mock_jwt_encode.return_value = "mock-jwt-token"
        github_adapter._jwt_token = "cached-token"
        github_adapter._jwt_expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)

        token = github_adapter._generate_jwt()

        # Should return cached token without calling encode
        assert token == "cached-token"
        mock_jwt_encode.assert_not_called()

    @patch('sdlcctl.services.mcp.github_adapter.jwt.encode')
    def test_generate_jwt_expired_cache(self, mock_jwt_encode, github_adapter):
        """Test JWT regeneration when cache expired."""
        # Set expired cache
        github_adapter._jwt_token = "expired-token"
        github_adapter._jwt_expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)

        mock_jwt_encode.return_value = "new-jwt-token"

        token = github_adapter._generate_jwt()

        # Should generate new token
        assert token == "new-jwt-token"
        mock_jwt_encode.assert_called_once()

    @patch('sdlcctl.services.mcp.github_adapter.requests.get')
    @patch.object(GitHubAdapter, '_generate_jwt')
    def test_authenticate_app_success(self, mock_generate_jwt, mock_get, github_adapter):
        """Test GitHub App authentication successfully."""
        mock_generate_jwt.return_value = "mock-jwt-token"

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": 123456,
            "name": "SDLC Orchestrator",
            "owner": {"login": "nqh"},
            "html_url": "https://github.com/apps/sdlc-orchestrator"
        }
        mock_get.return_value = mock_response

        result = github_adapter.authenticate_app()

        assert result["id"] == 123456
        assert result["name"] == "SDLC Orchestrator"
        assert result["owner"] == "nqh"
        assert result["html_url"] == "https://github.com/apps/sdlc-orchestrator"

        # Verify API call
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[0][0] == "https://api.github.com/app"
        assert call_args[1]["headers"]["Authorization"] == "Bearer mock-jwt-token"

    @patch('sdlcctl.services.mcp.github_adapter.requests.get')
    @patch.object(GitHubAdapter, '_generate_jwt')
    def test_authenticate_app_failure(self, mock_generate_jwt, mock_get, github_adapter):
        """Test GitHub App authentication failure."""
        import requests
        mock_generate_jwt.return_value = "mock-jwt-token"
        mock_get.side_effect = requests.RequestException("API error")

        with pytest.raises(GitHubAPIError) as exc_info:
            github_adapter.authenticate_app()

        assert "Failed to authenticate GitHub App" in str(exc_info.value)

    @patch('sdlcctl.services.mcp.github_adapter.requests.get')
    @patch('sdlcctl.services.mcp.github_adapter.requests.post')
    @patch.object(GitHubAdapter, '_generate_jwt')
    def test_get_installation_token_success(self, mock_generate_jwt, mock_post, mock_get, github_adapter):
        """Test getting installation token successfully."""
        mock_generate_jwt.return_value = "mock-jwt-token"

        # Mock installation ID retrieval
        mock_get_response = MagicMock()
        mock_get_response.json.return_value = {"id": 789}
        mock_get.return_value = mock_get_response

        # Mock token creation
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {
            "token": "ghs_installation_token",
            "expires_at": "2026-02-04T12:00:00Z"
        }
        mock_post.return_value = mock_post_response

        token = github_adapter._get_installation_token("nqh", "sdlc-orchestrator")

        assert token == "ghs_installation_token"
        assert github_adapter._installation_token == "ghs_installation_token"
        assert github_adapter._installation_expires_at is not None

    @patch('sdlcctl.services.mcp.github_adapter.requests.get')
    @patch('sdlcctl.services.mcp.github_adapter.requests.post')
    @patch.object(GitHubAdapter, '_generate_jwt')
    def test_get_installation_token_cached(self, mock_generate_jwt, mock_post, mock_get, github_adapter):
        """Test installation token caching."""
        # Set cached token
        github_adapter._installation_token = "cached-token"
        github_adapter._installation_expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

        token = github_adapter._get_installation_token("nqh", "sdlc-orchestrator")

        # Should return cached token
        assert token == "cached-token"
        mock_get.assert_not_called()
        mock_post.assert_not_called()

    @patch('sdlcctl.services.mcp.github_adapter.requests.get')
    @patch.object(GitHubAdapter, '_get_installation_token')
    def test_verify_oauth_scopes_success(self, mock_get_token, mock_get, github_adapter):
        """Test OAuth scopes verification successfully."""
        mock_get_token.return_value = "ghs_installation_token"

        mock_response = MagicMock()
        mock_response.headers = {"X-OAuth-Scopes": "repo, issues:write, pull_requests:write"}
        mock_get.return_value = mock_response

        scopes = github_adapter.verify_oauth_scopes("nqh", "sdlc-orchestrator")

        assert scopes == ["repo", "issues:write", "pull_requests:write"]

    @patch('sdlcctl.services.mcp.github_adapter.requests.get')
    @patch.object(GitHubAdapter, '_get_installation_token')
    def test_verify_oauth_scopes_empty(self, mock_get_token, mock_get, github_adapter):
        """Test OAuth scopes verification with no scopes."""
        mock_get_token.return_value = "ghs_installation_token"

        mock_response = MagicMock()
        mock_response.headers = {"X-OAuth-Scopes": ""}
        mock_get.return_value = mock_response

        scopes = github_adapter.verify_oauth_scopes("nqh", "sdlc-orchestrator")

        assert scopes == []

    @patch('sdlcctl.services.mcp.github_adapter.requests.post')
    @patch.object(GitHubAdapter, '_get_installation_token')
    def test_create_issue_success(self, mock_get_token, mock_post, github_adapter):
        """Test creating GitHub issue successfully."""
        mock_get_token.return_value = "ghs_installation_token"

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "number": 42,
            "html_url": "https://github.com/nqh/sdlc-orchestrator/issues/42",
            "url": "https://api.github.com/repos/nqh/sdlc-orchestrator/issues/42",
            "state": "open",
            "created_at": "2026-02-04T10:00:00Z"
        }
        mock_post.return_value = mock_response

        result = github_adapter.create_issue(
            owner="nqh",
            repo="sdlc-orchestrator",
            title="Test issue",
            body="This is a test issue",
            labels=["bug", "P1"],
            assignees=["nqh"]
        )

        assert result["number"] == 42
        assert result["url"] == "https://github.com/nqh/sdlc-orchestrator/issues/42"
        assert result["state"] == "open"

        # Verify API call
        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        assert payload["title"] == "Test issue"
        assert payload["labels"] == ["bug", "P1"]
        assert payload["assignees"] == ["nqh"]

    @patch('sdlcctl.services.mcp.github_adapter.requests.post')
    @patch.object(GitHubAdapter, '_get_installation_token')
    def test_create_issue_failure(self, mock_get_token, mock_post, github_adapter):
        """Test creating GitHub issue failure."""
        import requests
        mock_get_token.return_value = "ghs_installation_token"
        mock_post.side_effect = requests.RequestException("API error")

        with pytest.raises(GitHubAPIError) as exc_info:
            github_adapter.create_issue(
                owner="nqh",
                repo="sdlc-orchestrator",
                title="Test issue",
                body="This is a test issue"
            )

        assert "Failed to create issue" in str(exc_info.value)

    @patch('sdlcctl.services.mcp.github_adapter.requests.post')
    @patch.object(GitHubAdapter, '_get_installation_token')
    def test_create_pr_success(self, mock_get_token, mock_post, github_adapter):
        """Test creating GitHub PR successfully."""
        mock_get_token.return_value = "ghs_installation_token"

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "number": 123,
            "html_url": "https://github.com/nqh/sdlc-orchestrator/pull/123",
            "url": "https://api.github.com/repos/nqh/sdlc-orchestrator/pulls/123",
            "state": "open",
            "draft": False,
            "created_at": "2026-02-04T10:00:00Z"
        }
        mock_post.return_value = mock_response

        result = github_adapter.create_pr(
            owner="nqh",
            repo="sdlc-orchestrator",
            title="Add MCP integration",
            body="This PR adds MCP integration",
            head="feature/mcp",
            base="main",
            draft=False
        )

        assert result["number"] == 123
        assert result["url"] == "https://github.com/nqh/sdlc-orchestrator/pull/123"
        assert result["state"] == "open"
        assert result["draft"] is False

    @patch('sdlcctl.services.mcp.github_adapter.requests.post')
    @patch.object(GitHubAdapter, '_get_installation_token')
    def test_create_pr_draft(self, mock_get_token, mock_post, github_adapter):
        """Test creating draft GitHub PR."""
        mock_get_token.return_value = "ghs_installation_token"

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "number": 124,
            "html_url": "https://github.com/nqh/sdlc-orchestrator/pull/124",
            "url": "https://api.github.com/repos/nqh/sdlc-orchestrator/pulls/124",
            "state": "open",
            "draft": True,
            "created_at": "2026-02-04T10:00:00Z"
        }
        mock_post.return_value = mock_response

        result = github_adapter.create_pr(
            owner="nqh",
            repo="sdlc-orchestrator",
            title="WIP: Add MCP integration",
            body="Work in progress",
            head="feature/mcp",
            base="main",
            draft=True
        )

        assert result["draft"] is True

    def test_verify_webhook_signature_valid(self, github_adapter):
        """Test verifying valid webhook signature."""
        # Prepare test data
        request_body = b'{"action":"opened","issue":{"number":42}}'
        webhook_secret = "test-webhook-secret-32-chars-long"

        # Generate valid signature
        signature_hash = hmac.new(
            webhook_secret.encode('utf-8'),
            request_body,
            hashlib.sha256
        ).hexdigest()
        signature = f'sha256={signature_hash}'

        # Verify signature
        result = github_adapter.verify_webhook_signature(
            request_body=request_body,
            signature=signature,
            webhook_secret=webhook_secret
        )

        assert result is True

    def test_verify_webhook_signature_invalid(self, github_adapter):
        """Test verifying invalid webhook signature."""
        request_body = b'{"action":"opened","issue":{"number":42}}'
        webhook_secret = "test-webhook-secret-32-chars-long"
        invalid_signature = 'sha256=invalid_signature_hash'

        with pytest.raises(GitHubSignatureError) as exc_info:
            github_adapter.verify_webhook_signature(
                request_body=request_body,
                signature=invalid_signature,
                webhook_secret=webhook_secret
            )

        assert "Signature verification failed" in str(exc_info.value)

    def test_verify_webhook_signature_invalid_format(self, github_adapter):
        """Test verifying signature with invalid format."""
        request_body = b'{"action":"opened","issue":{"number":42}}'
        webhook_secret = "test-webhook-secret-32-chars-long"
        invalid_signature = 'md5=invalid_format'

        with pytest.raises(GitHubSignatureError) as exc_info:
            github_adapter.verify_webhook_signature(
                request_body=request_body,
                signature=invalid_signature,
                webhook_secret=webhook_secret
            )

        assert "Invalid signature format" in str(exc_info.value)

    def test_handle_rate_limit_with_header(self, github_adapter):
        """Test handling rate limit with header."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"message": "API rate limit exceeded"}
        mock_response.headers = {
            "X-RateLimit-Limit": "5000",
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(int(time.time()) + 3600)
        }

        result = github_adapter.handle_rate_limit(mock_response)

        assert result is not None
        assert result["limit"] == "5000"
        assert result["remaining"] == "0"
        assert "reset" in result
        assert "wait_seconds" in result

    def test_handle_rate_limit_no_rate_limit(self, github_adapter):
        """Test handling non-rate-limit response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ok": True}

        result = github_adapter.handle_rate_limit(mock_response)

        assert result is None

    def test_handle_rate_limit_403_non_rate_limit(self, github_adapter):
        """Test handling 403 that is not rate limit."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"message": "Forbidden - insufficient permissions"}

        result = github_adapter.handle_rate_limit(mock_response)

        assert result is None
