"""
Unit Tests for OAuthService

SDLC Stage: 04 - BUILD
Sprint: 59 - OAuth Integration
Framework: SDLC 5.1.2
Epic: Marketing & Growth

Purpose:
Comprehensive unit tests for OAuthService.
Tests OAuth URL generation, PKCE, token exchange, and user info retrieval.

Coverage Target: 90%+
"""

import hashlib
import base64
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import httpx

from app.services.oauth_service import (
    OAuthService,
    OAuthTokens,
    OAuthUserInfo,
    oauth_service,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def oauth_svc():
    """Create a fresh OAuthService instance with mocked settings."""
    with patch("app.services.oauth_service.get_settings") as mock_settings:
        mock_settings.return_value = MagicMock(
            GITHUB_CLIENT_ID="test_github_client_id",
            GITHUB_CLIENT_SECRET="test_github_client_secret",
            GOOGLE_CLIENT_ID="test_google_client_id",
            GOOGLE_CLIENT_SECRET="test_google_client_secret",
        )
        service = OAuthService()
        yield service


@pytest.fixture
def github_user_response():
    """Sample GitHub user API response."""
    return {
        "id": 123456789,
        "login": "testuser",
        "name": "Test User",
        "email": "test@example.com",
        "avatar_url": "https://avatars.githubusercontent.com/u/123456789",
    }


@pytest.fixture
def github_emails_response():
    """Sample GitHub emails API response."""
    return [
        {"email": "secondary@example.com", "primary": False, "verified": True},
        {"email": "primary@example.com", "primary": True, "verified": True},
    ]


@pytest.fixture
def google_userinfo_response():
    """Sample Google userinfo API response."""
    return {
        "id": "google_user_123",
        "email": "test@gmail.com",
        "verified_email": True,
        "name": "Test Google User",
        "picture": "https://lh3.googleusercontent.com/test",
    }


# =============================================================================
# State & PKCE Generation Tests
# =============================================================================


class TestStateGeneration:
    """Tests for CSRF state parameter generation."""

    def test_generate_state_returns_hex_string(self, oauth_svc):
        """State should be a 64-character hex string."""
        state = oauth_svc.generate_state()
        assert len(state) == 64
        # Verify it's valid hex
        int(state, 16)

    def test_generate_state_is_unique(self, oauth_svc):
        """Each state should be unique."""
        states = [oauth_svc.generate_state() for _ in range(100)]
        assert len(set(states)) == 100

    def test_generate_state_is_cryptographically_random(self, oauth_svc):
        """States should not be predictable."""
        state1 = oauth_svc.generate_state()
        state2 = oauth_svc.generate_state()
        # States should be completely different
        assert state1 != state2
        # No common prefix (very unlikely for random data)
        assert state1[:8] != state2[:8]


class TestPKCEGeneration:
    """Tests for PKCE code verifier and challenge generation."""

    def test_generate_code_verifier_length(self, oauth_svc):
        """Code verifier should be 43-128 characters."""
        verifier = oauth_svc.generate_code_verifier()
        assert 43 <= len(verifier) <= 128

    def test_generate_code_verifier_is_url_safe(self, oauth_svc):
        """Code verifier should be URL-safe base64."""
        verifier = oauth_svc.generate_code_verifier()
        # URL-safe base64 only contains A-Z, a-z, 0-9, -, _
        valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")
        assert all(c in valid_chars for c in verifier)

    def test_generate_code_verifier_is_unique(self, oauth_svc):
        """Each code verifier should be unique."""
        verifiers = [oauth_svc.generate_code_verifier() for _ in range(100)]
        assert len(set(verifiers)) == 100

    def test_generate_code_challenge_sha256(self, oauth_svc):
        """Code challenge should be SHA256 hash of verifier."""
        verifier = "test_code_verifier_12345"
        challenge = oauth_svc.generate_code_challenge(verifier)

        # Manually compute expected challenge
        expected_digest = hashlib.sha256(verifier.encode()).digest()
        expected_challenge = base64.urlsafe_b64encode(expected_digest).rstrip(b"=").decode()

        assert challenge == expected_challenge

    def test_generate_code_challenge_no_padding(self, oauth_svc):
        """Code challenge should not have base64 padding."""
        verifier = oauth_svc.generate_code_verifier()
        challenge = oauth_svc.generate_code_challenge(verifier)
        assert "=" not in challenge


# =============================================================================
# GitHub OAuth Tests
# =============================================================================


class TestGitHubAuthURL:
    """Tests for GitHub authorization URL generation."""

    def test_github_auth_url_format(self, oauth_svc):
        """GitHub auth URL should have correct format and parameters."""
        state = "test_state_123"
        redirect_uri = "http://localhost:3000/auth/callback"

        url = oauth_svc.get_github_auth_url(state, redirect_uri)

        assert url.startswith("https://github.com/login/oauth/authorize?")
        assert "client_id=test_github_client_id" in url
        assert f"state={state}" in url
        assert "scope=read%3Auser+user%3Aemail" in url
        assert "allow_signup=true" in url

    def test_github_auth_url_encodes_redirect_uri(self, oauth_svc):
        """Redirect URI should be URL-encoded."""
        state = "test_state"
        redirect_uri = "http://localhost:3000/auth/callback?param=value"

        url = oauth_svc.get_github_auth_url(state, redirect_uri)

        # URL encoding replaces special characters
        assert "redirect_uri=http%3A%2F%2Flocalhost%3A3000" in url


class TestGitHubTokenExchange:
    """Tests for GitHub code → token exchange."""

    @pytest.mark.asyncio
    async def test_exchange_github_code_success(self, oauth_svc):
        """Successful token exchange should return OAuthTokens."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "gho_test_access_token",
            "token_type": "bearer",
        }

        with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            tokens = await oauth_svc.exchange_github_code(
                code="test_auth_code",
                redirect_uri="http://localhost:3000/auth/callback",
            )

            assert isinstance(tokens, OAuthTokens)
            assert tokens.access_token == "gho_test_access_token"
            assert tokens.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_exchange_github_code_http_error(self, oauth_svc):
        """HTTP error should raise ValueError."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"

        with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            with pytest.raises(ValueError, match="GitHub token exchange failed"):
                await oauth_svc.exchange_github_code(
                    code="invalid_code",
                    redirect_uri="http://localhost:3000/auth/callback",
                )

    @pytest.mark.asyncio
    async def test_exchange_github_code_oauth_error(self, oauth_svc):
        """OAuth error in response should raise ValueError."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "error": "bad_verification_code",
            "error_description": "The code passed is incorrect or expired.",
        }

        with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            with pytest.raises(ValueError, match="The code passed is incorrect or expired"):
                await oauth_svc.exchange_github_code(
                    code="expired_code",
                    redirect_uri="http://localhost:3000/auth/callback",
                )


class TestGitHubUserInfo:
    """Tests for GitHub user info retrieval."""

    @pytest.mark.asyncio
    async def test_get_github_user_info_success(self, oauth_svc, github_user_response, github_emails_response):
        """Successful user info retrieval should return OAuthUserInfo."""
        user_response = MagicMock()
        user_response.status_code = 200
        user_response.json.return_value = github_user_response

        emails_response = MagicMock()
        emails_response.status_code = 200
        emails_response.json.return_value = github_emails_response

        with patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock) as mock_get:
            # First call returns user, second call returns emails
            mock_get.side_effect = [user_response, emails_response]

            user_info = await oauth_svc.get_github_user_info("gho_test_token")

            assert isinstance(user_info, OAuthUserInfo)
            assert user_info.provider == "github"
            assert user_info.provider_account_id == "123456789"
            # Should use primary verified email
            assert user_info.email == "primary@example.com"
            assert user_info.name == "Test User"

    @pytest.mark.asyncio
    async def test_get_github_user_info_uses_public_email_fallback(self, oauth_svc, github_user_response):
        """Should use public email if emails endpoint fails."""
        user_response = MagicMock()
        user_response.status_code = 200
        user_response.json.return_value = github_user_response

        emails_response = MagicMock()
        emails_response.status_code = 403  # Forbidden

        with patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = [user_response, emails_response]

            user_info = await oauth_svc.get_github_user_info("gho_test_token")

            # Should fall back to public email
            assert user_info.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_github_user_info_no_email_error(self, oauth_svc):
        """Should raise error if no verified email available."""
        user_response = MagicMock()
        user_response.status_code = 200
        user_response.json.return_value = {
            "id": 123,
            "login": "nomail",
            "email": None,  # No public email
        }

        emails_response = MagicMock()
        emails_response.status_code = 200
        emails_response.json.return_value = []  # No private emails either

        with patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = [user_response, emails_response]

            with pytest.raises(ValueError, match="no verified email"):
                await oauth_svc.get_github_user_info("gho_test_token")


# =============================================================================
# Google OAuth Tests
# =============================================================================


class TestGoogleAuthURL:
    """Tests for Google authorization URL generation."""

    def test_google_auth_url_format(self, oauth_svc):
        """Google auth URL should have correct format and PKCE parameters."""
        state = "test_state_456"
        redirect_uri = "http://localhost:3000/auth/callback"
        code_verifier = "test_verifier_12345678901234567890123456789012"

        url = oauth_svc.get_google_auth_url(state, redirect_uri, code_verifier)

        assert url.startswith("https://accounts.google.com/o/oauth2/v2/auth?")
        assert "client_id=test_google_client_id" in url
        assert f"state={state}" in url
        assert "response_type=code" in url
        assert "scope=openid+email+profile" in url
        assert "code_challenge=" in url
        assert "code_challenge_method=S256" in url
        assert "access_type=offline" in url

    def test_google_auth_url_includes_pkce_challenge(self, oauth_svc):
        """URL should include correct PKCE code challenge."""
        verifier = "test_code_verifier_for_pkce_challenge_test"
        expected_challenge = oauth_svc.generate_code_challenge(verifier)

        url = oauth_svc.get_google_auth_url("state", "http://localhost/callback", verifier)

        assert f"code_challenge={expected_challenge}" in url


class TestGoogleTokenExchange:
    """Tests for Google code → token exchange with PKCE."""

    @pytest.mark.asyncio
    async def test_exchange_google_code_success(self, oauth_svc):
        """Successful token exchange should return OAuthTokens with refresh token."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "ya29.test_access_token",
            "refresh_token": "1//test_refresh_token",
            "expires_in": 3599,
            "token_type": "Bearer",
        }

        with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            tokens = await oauth_svc.exchange_google_code(
                code="test_auth_code",
                redirect_uri="http://localhost:3000/auth/callback",
                code_verifier="test_verifier",
            )

            assert isinstance(tokens, OAuthTokens)
            assert tokens.access_token == "ya29.test_access_token"
            assert tokens.refresh_token == "1//test_refresh_token"
            assert tokens.expires_in == 3599

    @pytest.mark.asyncio
    async def test_exchange_google_code_sends_verifier(self, oauth_svc):
        """Code verifier should be sent in token exchange request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "token", "token_type": "Bearer"}

        with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            await oauth_svc.exchange_google_code(
                code="code",
                redirect_uri="http://localhost/callback",
                code_verifier="my_secret_verifier",
            )

            # Check that code_verifier was in the request data
            call_kwargs = mock_post.call_args
            assert call_kwargs[1]["data"]["code_verifier"] == "my_secret_verifier"

    @pytest.mark.asyncio
    async def test_exchange_google_code_oauth_error(self, oauth_svc):
        """OAuth error should raise ValueError."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "error": "invalid_grant",
            "error_description": "Code was already redeemed.",
        }

        with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            with pytest.raises(ValueError, match="Code was already redeemed"):
                await oauth_svc.exchange_google_code(
                    code="reused_code",
                    redirect_uri="http://localhost/callback",
                    code_verifier="verifier",
                )


class TestGoogleUserInfo:
    """Tests for Google user info retrieval."""

    @pytest.mark.asyncio
    async def test_get_google_user_info_success(self, oauth_svc, google_userinfo_response):
        """Successful user info retrieval should return OAuthUserInfo."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = google_userinfo_response

        with patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            user_info = await oauth_svc.get_google_user_info("ya29.test_token")

            assert isinstance(user_info, OAuthUserInfo)
            assert user_info.provider == "google"
            assert user_info.provider_account_id == "google_user_123"
            assert user_info.email == "test@gmail.com"
            assert user_info.name == "Test Google User"
            assert user_info.avatar_url == "https://lh3.googleusercontent.com/test"

    @pytest.mark.asyncio
    async def test_get_google_user_info_unverified_email_error(self, oauth_svc):
        """Should raise error if Google email is not verified."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "123",
            "email": "unverified@gmail.com",
            "verified_email": False,
        }

        with patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            with pytest.raises(ValueError, match="email is not verified"):
                await oauth_svc.get_google_user_info("test_token")

    @pytest.mark.asyncio
    async def test_get_google_user_info_http_error(self, oauth_svc):
        """HTTP error should raise ValueError."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Invalid token"

        with patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            with pytest.raises(ValueError, match="Google user info failed"):
                await oauth_svc.get_google_user_info("invalid_token")


# =============================================================================
# Singleton Tests
# =============================================================================


class TestSingleton:
    """Tests for OAuth service singleton."""

    def test_singleton_instance_exists(self):
        """oauth_service singleton should be available."""
        assert oauth_service is not None
        assert isinstance(oauth_service, OAuthService)

    def test_singleton_has_endpoints(self):
        """Singleton should have OAuth endpoints configured."""
        assert oauth_service.github_auth_url == "https://github.com/login/oauth/authorize"
        assert oauth_service.google_auth_url == "https://accounts.google.com/o/oauth2/v2/auth"
