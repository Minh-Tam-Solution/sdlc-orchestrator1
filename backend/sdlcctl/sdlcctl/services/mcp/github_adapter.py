"""GitHub adapter for MCP integration.

This module provides GitHub platform integration with OAuth, JWT authentication,
webhook signature verification, and issue/PR creation capabilities.
"""

import hashlib
import hmac
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

import jwt
import requests
from rich.console import Console

console = Console()


class GitHubAPIError(Exception):
    """Raised when GitHub API returns an error."""
    pass


class GitHubSignatureError(Exception):
    """Raised when webhook signature verification fails."""
    pass


class GitHubAdapter:
    """GitHub platform adapter for MCP integration.

    This adapter provides methods for GitHub App authentication, OAuth scope verification,
    issue/PR creation, and webhook signature verification.
    """

    def __init__(self, app_id: str, private_key_path: str):
        """Initialize GitHub adapter.

        Args:
            app_id: GitHub App ID
            private_key_path: Path to GitHub App private key (.pem file)
        """
        self.app_id = app_id
        self.private_key_path = private_key_path
        self.api_base_url = "https://api.github.com"
        self._jwt_token: Optional[str] = None
        self._jwt_expires_at: Optional[datetime] = None
        self._installation_token: Optional[str] = None
        self._installation_expires_at: Optional[datetime] = None

    def _load_private_key(self) -> str:
        """Load private key from file.

        Returns:
            Private key content as string

        Raises:
            GitHubAPIError: If private key file cannot be read
        """
        try:
            key_path = Path(self.private_key_path)
            with open(key_path, 'r') as f:
                return f.read()
        except Exception as e:
            raise GitHubAPIError(f"Failed to load private key: {e}")

    def _generate_jwt(self) -> str:
        """Generate JWT token for GitHub App authentication.

        Returns:
            JWT token string

        Raises:
            GitHubAPIError: If JWT generation fails
        """
        # Check if we have a valid cached JWT
        if self._jwt_token and self._jwt_expires_at:
            if datetime.now(timezone.utc) < self._jwt_expires_at:
                return self._jwt_token

        try:
            # Load private key
            private_key = self._load_private_key()

            # Generate JWT with 10 minute expiration (GitHub maximum)
            now = datetime.now(timezone.utc)
            expires_at = now + timedelta(minutes=10)

            payload = {
                "iat": int(now.timestamp()),  # Issued at
                "exp": int(expires_at.timestamp()),  # Expires at
                "iss": self.app_id  # Issuer (GitHub App ID)
            }

            # Sign JWT with RS256 algorithm
            token = jwt.encode(payload, private_key, algorithm="RS256")

            # Cache JWT
            self._jwt_token = token
            self._jwt_expires_at = expires_at

            return token

        except Exception as e:
            raise GitHubAPIError(f"Failed to generate JWT: {e}")

    def authenticate_app(self) -> Dict[str, Any]:
        """Authenticate GitHub App and verify configuration.

        Returns:
            Dictionary containing GitHub App info

        Raises:
            GitHubAPIError: If authentication fails
        """
        try:
            jwt_token = self._generate_jwt()

            response = requests.get(
                f"{self.api_base_url}/app",
                headers={
                    "Authorization": f"Bearer {jwt_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                },
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return {
                "id": data.get("id"),
                "name": data.get("name"),
                "owner": data.get("owner", {}).get("login"),
                "html_url": data.get("html_url")
            }

        except requests.RequestException as e:
            raise GitHubAPIError(f"Failed to authenticate GitHub App: {e}")

    def _get_installation_token(self, owner: str, repo: str) -> str:
        """Get installation access token for a repository.

        Args:
            owner: Repository owner (org or user)
            repo: Repository name

        Returns:
            Installation access token

        Raises:
            GitHubAPIError: If token generation fails
        """
        # Check if we have a valid cached installation token
        if self._installation_token and self._installation_expires_at:
            if datetime.now(timezone.utc) < self._installation_expires_at:
                return self._installation_token

        try:
            jwt_token = self._generate_jwt()

            # Get installation ID for the repository
            response = requests.get(
                f"{self.api_base_url}/repos/{owner}/{repo}/installation",
                headers={
                    "Authorization": f"Bearer {jwt_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                },
                timeout=10
            )
            response.raise_for_status()

            installation_id = response.json().get("id")

            # Create installation access token
            response = requests.post(
                f"{self.api_base_url}/app/installations/{installation_id}/access_tokens",
                headers={
                    "Authorization": f"Bearer {jwt_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                },
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            token = data.get("token")
            expires_at_str = data.get("expires_at")

            # Parse expiration time
            expires_at = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00'))

            # Cache installation token
            self._installation_token = token
            self._installation_expires_at = expires_at

            return token

        except requests.RequestException as e:
            raise GitHubAPIError(f"Failed to get installation token: {e}")

    def verify_oauth_scopes(self, owner: str, repo: str) -> List[str]:
        """Verify OAuth scopes for the GitHub App installation.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            List of granted scopes

        Raises:
            GitHubAPIError: If scope verification fails
        """
        try:
            installation_token = self._get_installation_token(owner, repo)

            # Make a test API call to check scopes
            response = requests.get(
                f"{self.api_base_url}/repos/{owner}/{repo}",
                headers={
                    "Authorization": f"Bearer {installation_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                },
                timeout=10
            )
            response.raise_for_status()

            # Extract scopes from response headers
            scopes_header = response.headers.get("X-OAuth-Scopes", "")
            scopes = [s.strip() for s in scopes_header.split(",") if s.strip()]

            return scopes

        except requests.RequestException as e:
            raise GitHubAPIError(f"Failed to verify OAuth scopes: {e}")

    def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a GitHub issue.

        Args:
            owner: Repository owner
            repo: Repository name
            title: Issue title
            body: Issue body (markdown)
            labels: Optional list of label names
            assignees: Optional list of assignee usernames

        Returns:
            Dictionary containing issue metadata (number, url, etc.)

        Raises:
            GitHubAPIError: If issue creation fails
        """
        try:
            installation_token = self._get_installation_token(owner, repo)

            payload = {
                "title": title,
                "body": body
            }

            if labels:
                payload["labels"] = labels

            if assignees:
                payload["assignees"] = assignees

            response = requests.post(
                f"{self.api_base_url}/repos/{owner}/{repo}/issues",
                headers={
                    "Authorization": f"Bearer {installation_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                },
                json=payload,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return {
                "number": data.get("number"),
                "url": data.get("html_url"),
                "api_url": data.get("url"),
                "state": data.get("state"),
                "created_at": data.get("created_at")
            }

        except requests.RequestException as e:
            raise GitHubAPIError(f"Failed to create issue: {e}")

    def create_pr(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str = "main",
        draft: bool = False
    ) -> Dict[str, Any]:
        """Create a GitHub pull request.

        Args:
            owner: Repository owner
            repo: Repository name
            title: PR title
            body: PR body (markdown)
            head: Branch name to merge from
            base: Branch name to merge into (default: main)
            draft: Create as draft PR (default: False)

        Returns:
            Dictionary containing PR metadata (number, url, etc.)

        Raises:
            GitHubAPIError: If PR creation fails
        """
        try:
            installation_token = self._get_installation_token(owner, repo)

            payload = {
                "title": title,
                "body": body,
                "head": head,
                "base": base,
                "draft": draft
            }

            response = requests.post(
                f"{self.api_base_url}/repos/{owner}/{repo}/pulls",
                headers={
                    "Authorization": f"Bearer {installation_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                },
                json=payload,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return {
                "number": data.get("number"),
                "url": data.get("html_url"),
                "api_url": data.get("url"),
                "state": data.get("state"),
                "draft": data.get("draft"),
                "created_at": data.get("created_at")
            }

        except requests.RequestException as e:
            raise GitHubAPIError(f"Failed to create PR: {e}")

    def verify_webhook_signature(
        self,
        request_body: bytes,
        signature: str,
        webhook_secret: str
    ) -> bool:
        """Verify GitHub webhook signature using HMAC-SHA256.

        This implements GitHub's signature verification as documented at:
        https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries

        Args:
            request_body: Raw request body as bytes
            signature: X-Hub-Signature-256 header value
            webhook_secret: GitHub webhook secret

        Returns:
            True if signature is valid

        Raises:
            GitHubSignatureError: If signature verification fails
        """
        # Extract hash from signature (format: "sha256=...")
        if not signature.startswith('sha256='):
            raise GitHubSignatureError(
                f"Invalid signature format. Expected 'sha256=...', got: {signature[:20]}..."
            )

        provided_hash = signature[7:]  # Remove 'sha256=' prefix

        # Compute HMAC-SHA256 signature
        computed_hash = hmac.new(
            webhook_secret.encode('utf-8'),
            request_body,
            hashlib.sha256
        ).hexdigest()

        # Constant-time comparison to prevent timing attacks
        if not hmac.compare_digest(computed_hash, provided_hash):
            raise GitHubSignatureError(
                f"Signature verification failed. "
                f"Computed hash does not match provided hash"
            )

        return True

    def handle_rate_limit(self, response: requests.Response) -> Optional[Dict[str, Any]]:
        """Handle GitHub API rate limiting.

        Args:
            response: HTTP response from GitHub API

        Returns:
            Dictionary with rate limit info, or None if no rate limit
        """
        if response.status_code == 403:
            # Check if this is a rate limit error
            data = response.json()
            if "rate limit" in data.get("message", "").lower():
                reset_timestamp = int(response.headers.get("X-RateLimit-Reset", 0))
                reset_time = datetime.fromtimestamp(reset_timestamp, tz=timezone.utc)
                wait_seconds = (reset_time - datetime.now(timezone.utc)).total_seconds()

                return {
                    "limit": response.headers.get("X-RateLimit-Limit"),
                    "remaining": response.headers.get("X-RateLimit-Remaining"),
                    "reset": reset_time.isoformat(),
                    "wait_seconds": max(0, int(wait_seconds))
                }

        return None
