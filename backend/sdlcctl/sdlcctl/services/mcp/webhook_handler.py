"""Webhook Handler for MCP integrations.

This module provides a unified webhook handler for processing incoming webhooks
from Slack, GitHub, and other platforms with signature verification and event routing.
"""

import json
import logging
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from rich.console import Console

from .evidence_vault_adapter import EvidenceVaultAdapter
from .github_adapter import GitHubAdapter, GitHubSignatureError
from .slack_adapter import SlackAdapter, SlackSignatureError

console = Console()
logger = logging.getLogger(__name__)


class PlatformType(str, Enum):
    """Supported platform types."""
    SLACK = "slack"
    GITHUB = "github"


class WebhookError(Exception):
    """Raised when webhook processing fails."""
    pass


class WebhookHandler:
    """
    Unified webhook handler for MCP integrations.

    This handler provides:
    - Signature verification for all platforms
    - Event routing to registered handlers
    - Evidence artifact creation for audit trail
    - Error handling and retry logic
    """

    def __init__(
        self,
        slack_adapter: Optional[SlackAdapter] = None,
        github_adapter: Optional[GitHubAdapter] = None,
        evidence_vault: Optional[EvidenceVaultAdapter] = None
    ):
        """
        Initialize webhook handler.

        Args:
            slack_adapter: Slack adapter for signature verification
            github_adapter: GitHub adapter for signature verification
            evidence_vault: Evidence vault for audit trail
        """
        self.slack_adapter = slack_adapter
        self.github_adapter = github_adapter
        self.evidence_vault = evidence_vault

        # Event handlers registry
        self._handlers: Dict[PlatformType, Dict[str, Callable]] = {
            PlatformType.SLACK: {},
            PlatformType.GITHUB: {}
        }

    def register_handler(
        self,
        platform: PlatformType,
        event_type: str,
        handler: Callable[[Dict[str, Any]], None]
    ) -> None:
        """
        Register event handler for specific platform and event type.

        Args:
            platform: Platform type (slack, github)
            event_type: Event type (e.g., "message", "issue", "pull_request")
            handler: Callable that processes the event
        """
        if platform not in self._handlers:
            self._handlers[platform] = {}

        self._handlers[platform][event_type] = handler
        logger.info(f"Registered handler for {platform}/{event_type}")

    def handle_slack_webhook(
        self,
        request_body: str,
        timestamp: str,
        signature: str
    ) -> Dict[str, Any]:
        """
        Handle incoming Slack webhook.

        Args:
            request_body: Raw request body as string
            timestamp: X-Slack-Request-Timestamp header value
            signature: X-Slack-Signature header value

        Returns:
            Processing result dictionary

        Raises:
            WebhookError: If webhook processing fails
        """
        try:
            # Verify signature
            if not self.slack_adapter:
                raise WebhookError("Slack adapter not configured")

            try:
                self.slack_adapter.verify_webhook_signature(
                    request_body=request_body,
                    timestamp=timestamp,
                    signature=signature
                )
            except SlackSignatureError as e:
                raise WebhookError(f"Slack signature verification failed: {e}")

            # Parse event
            try:
                event_data = json.loads(request_body)
            except json.JSONDecodeError as e:
                raise WebhookError(f"Invalid JSON in request body: {e}")

            # Handle URL verification challenge (Slack setup)
            if event_data.get("type") == "url_verification":
                return {
                    "challenge": event_data.get("challenge"),
                    "status": "url_verified"
                }

            # Extract event type
            event_type = event_data.get("event", {}).get("type", "unknown")

            # Create evidence artifact
            if self.evidence_vault:
                artifact_id = self.evidence_vault.create_artifact(
                    operation="webhook_received",
                    platform="slack",
                    metadata={
                        "event_type": event_type,
                        "team_id": event_data.get("team_id"),
                        "event_id": event_data.get("event_id"),
                        "timestamp": timestamp
                    }
                )
                logger.info(f"Evidence artifact created: {artifact_id}")

            # Route to handler
            result = self._route_event(
                platform=PlatformType.SLACK,
                event_type=event_type,
                event_data=event_data
            )

            return {
                "status": "processed",
                "event_type": event_type,
                "result": result
            }

        except WebhookError:
            raise
        except Exception as e:
            raise WebhookError(f"Failed to process Slack webhook: {e}")

    def handle_github_webhook(
        self,
        request_body: bytes,
        signature: str,
        webhook_secret: str,
        event_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle incoming GitHub webhook.

        Args:
            request_body: Raw request body as bytes
            signature: X-Hub-Signature-256 header value
            webhook_secret: GitHub webhook secret for verification
            event_type: X-GitHub-Event header value

        Returns:
            Processing result dictionary

        Raises:
            WebhookError: If webhook processing fails
        """
        try:
            # Verify signature
            if not self.github_adapter:
                raise WebhookError("GitHub adapter not configured")

            try:
                self.github_adapter.verify_webhook_signature(
                    request_body=request_body,
                    signature=signature,
                    webhook_secret=webhook_secret
                )
            except GitHubSignatureError as e:
                raise WebhookError(f"GitHub signature verification failed: {e}")

            # Parse event
            try:
                event_data = json.loads(request_body.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                raise WebhookError(f"Invalid JSON in request body: {e}")

            # Extract event details
            event_type = event_type or event_data.get("action", "unknown")
            repository = event_data.get("repository", {}).get("full_name", "unknown")

            # Create evidence artifact
            if self.evidence_vault:
                artifact_id = self.evidence_vault.create_artifact(
                    operation="webhook_received",
                    platform="github",
                    metadata={
                        "event_type": event_type,
                        "repository": repository,
                        "sender": event_data.get("sender", {}).get("login"),
                        "action": event_data.get("action")
                    }
                )
                logger.info(f"Evidence artifact created: {artifact_id}")

            # Route to handler
            result = self._route_event(
                platform=PlatformType.GITHUB,
                event_type=event_type,
                event_data=event_data
            )

            return {
                "status": "processed",
                "event_type": event_type,
                "repository": repository,
                "result": result
            }

        except WebhookError:
            raise
        except Exception as e:
            raise WebhookError(f"Failed to process GitHub webhook: {e}")

    def _route_event(
        self,
        platform: PlatformType,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> Optional[Any]:
        """
        Route event to registered handler.

        Args:
            platform: Platform type (slack, github)
            event_type: Event type
            event_data: Event payload

        Returns:
            Handler result, or None if no handler registered
        """
        handlers = self._handlers.get(platform, {})
        handler = handlers.get(event_type)

        if handler:
            logger.info(f"Routing {platform}/{event_type} to registered handler")
            try:
                return handler(event_data)
            except Exception as e:
                logger.error(f"Handler error for {platform}/{event_type}: {e}")
                raise WebhookError(f"Handler failed: {e}")
        else:
            logger.warning(
                f"No handler registered for {platform}/{event_type}. "
                f"Event will be logged but not processed."
            )
            return None

    def handle_slack_message(self, event_data: Dict[str, Any]) -> None:
        """
        Default handler for Slack messages.

        This is an example handler that logs the message.
        Override by registering custom handler.

        Args:
            event_data: Slack event data
        """
        event = event_data.get("event", {})
        channel = event.get("channel")
        user = event.get("user")
        text = event.get("text")

        logger.info(f"Slack message from {user} in {channel}: {text}")

        # Example: Echo bot
        if self.slack_adapter and text and not event.get("bot_id"):
            try:
                self.slack_adapter.post_message(
                    channel=channel,
                    text=f"Echo: {text}"
                )
            except Exception as e:
                logger.error(f"Failed to send echo message: {e}")

    def handle_github_issue(self, event_data: Dict[str, Any]) -> None:
        """
        Default handler for GitHub issues.

        This is an example handler that logs the issue event.
        Override by registering custom handler.

        Args:
            event_data: GitHub event data
        """
        action = event_data.get("action")
        issue = event_data.get("issue", {})
        issue_number = issue.get("number")
        issue_title = issue.get("title")
        repository = event_data.get("repository", {}).get("full_name")

        logger.info(
            f"GitHub issue {action}: #{issue_number} '{issue_title}' "
            f"in {repository}"
        )

        # Example: Auto-label P0 issues
        if "P0" in issue_title and action == "opened":
            logger.info(f"Detected P0 issue #{issue_number}, should add label")

    def handle_github_pull_request(self, event_data: Dict[str, Any]) -> None:
        """
        Default handler for GitHub pull requests.

        This is an example handler that logs the PR event.
        Override by registering custom handler.

        Args:
            event_data: GitHub event data
        """
        action = event_data.get("action")
        pr = event_data.get("pull_request", {})
        pr_number = pr.get("number")
        pr_title = pr.get("title")
        repository = event_data.get("repository", {}).get("full_name")

        logger.info(
            f"GitHub PR {action}: #{pr_number} '{pr_title}' "
            f"in {repository}"
        )

        # Example: Auto-comment on draft PRs
        if pr.get("draft") and action == "opened":
            logger.info(f"Detected draft PR #{pr_number}, should add comment")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get webhook handler statistics.

        Returns:
            Statistics dictionary with handler counts
        """
        stats = {
            "handlers": {},
            "platforms": list(self._handlers.keys())
        }

        for platform, handlers in self._handlers.items():
            stats["handlers"][platform.value] = {
                "count": len(handlers),
                "event_types": list(handlers.keys())
            }

        return stats
