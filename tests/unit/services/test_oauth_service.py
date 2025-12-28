"""Unit Tests for OAuthService

SDLC Orchestrator - Stage 03 (BUILD)
Sprint: 59 - OAuth Integration

Notes:
- External OAuth providers are mocked via `httpx` method patches.
- Tests run under the repo root `pytest.ini` (testpaths=tests).
"""

import hashlib
import base64
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import httpx

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend"))

from app.services.oauth_service import OAuthService, OAuthTokens  # noqa: E402


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
        yield OAuthService()


def test_generate_state_is_hex_and_unique(oauth_svc):
    s1 = oauth_svc.generate_state()
    s2 = oauth_svc.generate_state()
    assert len(s1) == 64
    int(s1, 16)
    assert s1 != s2


def test_pkce_challenge_matches_sha256(oauth_svc):
    verifier = "test_code_verifier_12345"
    challenge = oauth_svc.generate_code_challenge(verifier)

    expected_digest = hashlib.sha256(verifier.encode()).digest()
    expected = base64.urlsafe_b64encode(expected_digest).rstrip(b"=").decode()
    assert challenge == expected


def test_github_auth_url_contains_required_params(oauth_svc):
    url = oauth_svc.get_github_auth_url(state="STATE", redirect_uri="http://localhost:3000/auth/callback")
    assert url.startswith("https://github.com/login/oauth/authorize?")
    assert "client_id=test_github_client_id" in url
    assert "state=STATE" in url


def test_google_auth_url_contains_pkce_params(oauth_svc):
    url = oauth_svc.get_google_auth_url(
        state="STATE",
        redirect_uri="http://localhost:3000/auth/callback",
        code_verifier="verifier",
    )
    assert url.startswith("https://accounts.google.com/o/oauth2/v2/auth?")
    assert "client_id=test_google_client_id" in url
    assert "code_challenge_method=S256" in url


@pytest.mark.asyncio
async def test_exchange_github_code_success(oauth_svc):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "gh_token", "token_type": "bearer"}

    with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        tokens = await oauth_svc.exchange_github_code(code="code", redirect_uri="http://localhost/cb")

    assert isinstance(tokens, OAuthTokens)
    assert tokens.access_token == "gh_token"


@pytest.mark.asyncio
async def test_exchange_google_code_success(oauth_svc):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "access_token": "g_token",
        "refresh_token": "g_refresh",
        "expires_in": 3600,
        "token_type": "bearer",
    }

    with patch.object(httpx.AsyncClient, "post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        tokens = await oauth_svc.exchange_google_code(
            code="code",
            redirect_uri="http://localhost/cb",
            code_verifier="verifier",
        )

    assert tokens.access_token == "g_token"
    assert tokens.refresh_token == "g_refresh"
    assert tokens.expires_in == 3600
