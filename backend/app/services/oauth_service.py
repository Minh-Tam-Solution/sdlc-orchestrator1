"""
OAuth Service - GitHub & Google Integration
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: December 27, 2025
Status: Sprint 59 - OAuth Integration
Authority: Backend Lead + CTO Approved
Foundation: OAuth 2.0 with PKCE
Framework: SDLC 5.1.2 Universal Framework

Purpose:
- GitHub OAuth 2.0 integration
- Google OAuth 2.0 integration
- PKCE flow for security
- Token exchange and user info retrieval

Supported Providers:
- GitHub: Authorization Code flow
- Google: Authorization Code flow with PKCE

Security:
- PKCE code verifier (S256)
- State parameter for CSRF protection
- Secure token storage
- No client secrets in frontend

Zero Mock Policy: Production-ready OAuth implementation
"""

import hashlib
import secrets
import base64
from typing import Optional
from urllib.parse import urlencode
import httpx
from pydantic import BaseModel

from app.core.config import get_settings


class OAuthUserInfo(BaseModel):
    """User information from OAuth provider."""

    provider: str
    provider_account_id: str
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None


class OAuthTokens(BaseModel):
    """OAuth tokens from provider."""

    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "bearer"


class OAuthService:
    """
    OAuth 2.0 service for GitHub and Google integration.

    Implements:
    - Authorization URL generation with PKCE
    - Token exchange (code → tokens)
    - User info retrieval
    - Account linking/creation
    """

    def __init__(self):
        self.settings = get_settings()

        # GitHub OAuth endpoints
        self.github_auth_url = "https://github.com/login/oauth/authorize"
        self.github_token_url = "https://github.com/login/oauth/access_token"
        self.github_user_url = "https://api.github.com/user"
        self.github_emails_url = "https://api.github.com/user/emails"

        # Google OAuth endpoints
        self.google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.google_token_url = "https://oauth2.googleapis.com/token"
        self.google_userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"

    def generate_state(self) -> str:
        """
        Generate a cryptographically secure state parameter for CSRF protection.

        Returns:
            32-byte hex string (64 characters)
        """
        return secrets.token_hex(32)

    def generate_code_verifier(self) -> str:
        """
        Generate a PKCE code verifier.

        Returns:
            43-128 character URL-safe string
        """
        return secrets.token_urlsafe(64)[:128]

    def generate_code_challenge(self, code_verifier: str) -> str:
        """
        Generate a PKCE code challenge from the verifier (S256 method).

        Args:
            code_verifier: The code verifier string

        Returns:
            Base64 URL-safe encoded SHA-256 hash
        """
        digest = hashlib.sha256(code_verifier.encode()).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()

    # =========================================================================
    # GitHub OAuth
    # =========================================================================

    def get_github_auth_url(self, state: str, redirect_uri: str) -> str:
        """
        Generate GitHub OAuth authorization URL.

        Args:
            state: CSRF protection state parameter
            redirect_uri: Callback URL after authorization

        Returns:
            Full authorization URL
        """
        params = {
            "client_id": self.settings.GITHUB_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "scope": "read:user user:email",
            "state": state,
            "allow_signup": "true",
        }
        return f"{self.github_auth_url}?{urlencode(params)}"

    async def exchange_github_code(
        self,
        code: str,
        redirect_uri: str,
    ) -> OAuthTokens:
        """
        Exchange GitHub authorization code for access token.

        Args:
            code: Authorization code from GitHub callback
            redirect_uri: Same redirect_uri used in auth request

        Returns:
            OAuthTokens with access_token

        Raises:
            ValueError: If token exchange fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.github_token_url,
                data={
                    "client_id": self.settings.GITHUB_CLIENT_ID,
                    "client_secret": self.settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": redirect_uri,
                },
                headers={"Accept": "application/json"},
            )

            if response.status_code != 200:
                raise ValueError(f"GitHub token exchange failed: {response.text}")

            data = response.json()

            if "error" in data:
                raise ValueError(f"GitHub OAuth error: {data.get('error_description', data['error'])}")

            return OAuthTokens(
                access_token=data["access_token"],
                token_type=data.get("token_type", "bearer"),
            )

    async def get_github_user_info(self, access_token: str) -> OAuthUserInfo:
        """
        Get user information from GitHub API.

        Args:
            access_token: GitHub OAuth access token

        Returns:
            OAuthUserInfo with user details

        Raises:
            ValueError: If user info retrieval fails
        """
        async with httpx.AsyncClient() as client:
            # Get user profile
            user_response = await client.get(
                self.github_user_url,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github.v3+json",
                },
            )

            if user_response.status_code != 200:
                raise ValueError(f"GitHub user info failed: {user_response.text}")

            user_data = user_response.json()

            # Get user emails (public email might be null)
            emails_response = await client.get(
                self.github_emails_url,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github.v3+json",
                },
            )

            email = user_data.get("email")

            if emails_response.status_code == 200:
                emails = emails_response.json()
                # Find primary verified email
                for email_entry in emails:
                    if email_entry.get("primary") and email_entry.get("verified"):
                        email = email_entry["email"]
                        break

            if not email:
                raise ValueError("GitHub account has no verified email address")

            return OAuthUserInfo(
                provider="github",
                provider_account_id=str(user_data["id"]),
                email=email,
                name=user_data.get("name") or user_data.get("login"),
                avatar_url=user_data.get("avatar_url"),
            )

    # =========================================================================
    # Google OAuth
    # =========================================================================

    def get_google_auth_url(
        self,
        state: str,
        redirect_uri: str,
        code_verifier: str,
    ) -> str:
        """
        Generate Google OAuth authorization URL with PKCE.

        Args:
            state: CSRF protection state parameter
            redirect_uri: Callback URL after authorization
            code_verifier: PKCE code verifier

        Returns:
            Full authorization URL
        """
        code_challenge = self.generate_code_challenge(code_verifier)

        params = {
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "access_type": "offline",
            "prompt": "consent",
        }
        return f"{self.google_auth_url}?{urlencode(params)}"

    async def exchange_google_code(
        self,
        code: str,
        redirect_uri: str,
        code_verifier: str,
    ) -> OAuthTokens:
        """
        Exchange Google authorization code for tokens with PKCE.

        Args:
            code: Authorization code from Google callback
            redirect_uri: Same redirect_uri used in auth request
            code_verifier: PKCE code verifier

        Returns:
            OAuthTokens with access_token and refresh_token

        Raises:
            ValueError: If token exchange fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.google_token_url,
                data={
                    "client_id": self.settings.GOOGLE_CLIENT_ID,
                    "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                    "code_verifier": code_verifier,
                },
            )

            if response.status_code != 200:
                raise ValueError(f"Google token exchange failed: {response.text}")

            data = response.json()

            if "error" in data:
                raise ValueError(f"Google OAuth error: {data.get('error_description', data['error'])}")

            return OAuthTokens(
                access_token=data["access_token"],
                refresh_token=data.get("refresh_token"),
                expires_in=data.get("expires_in"),
                token_type=data.get("token_type", "bearer"),
            )

    async def get_google_user_info(self, access_token: str) -> OAuthUserInfo:
        """
        Get user information from Google API.

        Args:
            access_token: Google OAuth access token

        Returns:
            OAuthUserInfo with user details

        Raises:
            ValueError: If user info retrieval fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.google_userinfo_url,
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if response.status_code != 200:
                raise ValueError(f"Google user info failed: {response.text}")

            data = response.json()

            if not data.get("verified_email"):
                raise ValueError("Google account email is not verified")

            return OAuthUserInfo(
                provider="google",
                provider_account_id=data["id"],
                email=data["email"],
                name=data.get("name"),
                avatar_url=data.get("picture"),
            )


# Singleton instance
oauth_service = OAuthService()
