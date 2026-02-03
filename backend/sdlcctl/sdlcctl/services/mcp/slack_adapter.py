"""Slack adapter for MCP integration.

This module provides Slack platform integration with HMAC-SHA256 webhook signature
verification, bot token validation, and message posting capabilities.
"""

import hashlib
import hmac
import time
from typing import Dict, Optional, Any

import requests
from rich.console import Console

console = Console()


class SlackAPIError(Exception):
    """Raised when Slack API returns an error."""
    pass


class SlackSignatureError(Exception):
    """Raised when webhook signature verification fails."""
    pass


class SlackAdapter:
    """Slack platform adapter for MCP integration.

    This adapter provides methods for validating Slack credentials, verifying webhook
    signatures, and posting messages to Slack channels.
    """

    def __init__(self, bot_token: str, signing_secret: str):
        """Initialize Slack adapter.

        Args:
            bot_token: Slack bot token (format: xoxb-...)
            signing_secret: Slack signing secret for webhook verification
        """
        self.bot_token = bot_token
        self.signing_secret = signing_secret
        self.api_base_url = "https://slack.com/api"

    def validate_bot_token(self) -> Dict[str, Any]:
        """Validate Slack bot token by calling auth.test API.

        Returns:
            Dictionary containing auth info (user, team, etc.)

        Raises:
            SlackAPIError: If token is invalid or API call fails
        """
        try:
            response = requests.post(
                f"{self.api_base_url}/auth.test",
                headers={
                    "Authorization": f"Bearer {self.bot_token}",
                    "Content-Type": "application/json"
                },
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            if not data.get("ok"):
                error = data.get("error", "unknown_error")
                raise SlackAPIError(f"Authentication failed: {error}")

            return {
                "user": data.get("user"),
                "user_id": data.get("user_id"),
                "team": data.get("team"),
                "team_id": data.get("team_id"),
                "url": data.get("url")
            }

        except requests.RequestException as e:
            raise SlackAPIError(f"Failed to validate bot token: {e}")

    def verify_webhook_signature(
        self,
        request_body: str,
        timestamp: str,
        signature: str
    ) -> bool:
        """Verify Slack webhook signature using HMAC-SHA256.

        This implements Slack's signature verification as documented at:
        https://api.slack.com/authentication/verifying-requests-from-slack

        Args:
            request_body: Raw request body as string
            timestamp: X-Slack-Request-Timestamp header value
            signature: X-Slack-Signature header value

        Returns:
            True if signature is valid

        Raises:
            SlackSignatureError: If signature verification fails or timestamp is too old
        """
        # Replay attack prevention: Reject old requests (>5 minutes)
        current_time = int(time.time())
        request_time = int(timestamp)

        if abs(current_time - request_time) > 300:  # 5 minutes
            raise SlackSignatureError(
                f"Request timestamp too old. "
                f"Current: {current_time}, Request: {request_time}, "
                f"Difference: {abs(current_time - request_time)}s (max: 300s)"
            )

        # Compute HMAC-SHA256 signature
        sig_basestring = f"v0:{timestamp}:{request_body}"
        computed_signature = 'v0=' + hmac.new(
            self.signing_secret.encode('utf-8'),
            sig_basestring.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # Constant-time comparison to prevent timing attacks
        if not hmac.compare_digest(computed_signature, signature):
            raise SlackSignatureError(
                f"Signature verification failed. "
                f"Expected signature starting with 'v0=', got: {signature[:20]}..."
            )

        return True

    def check_channel_access(self, channel: str) -> bool:
        """Check if bot has access to a Slack channel.

        Args:
            channel: Channel name (without #) or channel ID

        Returns:
            True if bot has access to the channel

        Raises:
            SlackAPIError: If API call fails or bot doesn't have access
        """
        try:
            # First, get list of channels bot is member of
            response = requests.get(
                f"{self.api_base_url}/conversations.list",
                headers={
                    "Authorization": f"Bearer {self.bot_token}",
                    "Content-Type": "application/json"
                },
                params={
                    "types": "public_channel,private_channel",
                    "exclude_archived": True
                },
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            if not data.get("ok"):
                error = data.get("error", "unknown_error")
                raise SlackAPIError(f"Failed to list channels: {error}")

            # Check if channel exists in the list
            channels = data.get("channels", [])
            for ch in channels:
                if ch.get("name") == channel or ch.get("id") == channel:
                    # Check if bot is member
                    if ch.get("is_member"):
                        return True
                    else:
                        raise SlackAPIError(
                            f"Bot is not a member of #{channel}. "
                            f"Invite bot with: /invite @sdlc-bot"
                        )

            # Channel not found
            raise SlackAPIError(
                f"Channel #{channel} not found or bot doesn't have access"
            )

        except requests.RequestException as e:
            raise SlackAPIError(f"Failed to check channel access: {e}")

    def post_message(
        self,
        channel: str,
        text: str,
        thread_ts: Optional[str] = None
    ) -> Dict[str, Any]:
        """Post a message to a Slack channel.

        Args:
            channel: Channel name (without #) or channel ID
            text: Message text to post
            thread_ts: Optional thread timestamp to reply to a thread

        Returns:
            Dictionary containing message metadata (ts, channel, etc.)

        Raises:
            SlackAPIError: If message posting fails
        """
        try:
            payload = {
                "channel": channel if channel.startswith("C") else f"#{channel}",
                "text": text
            }

            if thread_ts:
                payload["thread_ts"] = thread_ts

            response = requests.post(
                f"{self.api_base_url}/chat.postMessage",
                headers={
                    "Authorization": f"Bearer {self.bot_token}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            if not data.get("ok"):
                error = data.get("error", "unknown_error")
                raise SlackAPIError(f"Failed to post message: {error}")

            return {
                "ts": data.get("ts"),
                "channel": data.get("channel"),
                "message": data.get("message")
            }

        except requests.RequestException as e:
            raise SlackAPIError(f"Failed to post message: {e}")

    def get_thread_context(
        self,
        channel: str,
        thread_ts: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Retrieve conversation history from a Slack thread.

        Args:
            channel: Channel ID
            thread_ts: Thread timestamp
            limit: Maximum number of messages to retrieve (default: 10)

        Returns:
            Dictionary containing thread messages and metadata

        Raises:
            SlackAPIError: If API call fails
        """
        try:
            response = requests.get(
                f"{self.api_base_url}/conversations.replies",
                headers={
                    "Authorization": f"Bearer {self.bot_token}",
                    "Content-Type": "application/json"
                },
                params={
                    "channel": channel,
                    "ts": thread_ts,
                    "limit": limit
                },
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            if not data.get("ok"):
                error = data.get("error", "unknown_error")
                raise SlackAPIError(f"Failed to get thread context: {error}")

            messages = data.get("messages", [])
            return {
                "messages": messages,
                "has_more": data.get("has_more", False),
                "response_metadata": data.get("response_metadata", {})
            }

        except requests.RequestException as e:
            raise SlackAPIError(f"Failed to get thread context: {e}")

    def handle_rate_limit(self, response: requests.Response) -> Optional[int]:
        """Handle Slack API rate limiting.

        Args:
            response: HTTP response from Slack API

        Returns:
            Number of seconds to wait before retrying, or None if no rate limit
        """
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                return int(retry_after)
            return 60  # Default: wait 1 minute

        return None
