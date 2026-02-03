"""Unit tests for Webhook Handler."""

import hashlib
import hmac
import json
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sdlcctl.services.mcp.evidence_vault_adapter import EvidenceVaultAdapter
from sdlcctl.services.mcp.github_adapter import GitHubAdapter
from sdlcctl.services.mcp.slack_adapter import SlackAdapter
from sdlcctl.services.mcp.webhook_handler import (
    PlatformType,
    WebhookError,
    WebhookHandler,
)


@pytest.fixture
def slack_adapter():
    """Create mock Slack adapter."""
    adapter = MagicMock(spec=SlackAdapter)
    adapter.signing_secret = "test-signing-secret-32-chars-long"
    adapter.verify_webhook_signature = MagicMock(return_value=True)
    return adapter


@pytest.fixture
def github_adapter(tmp_path):
    """Create GitHub adapter."""
    private_key_path = tmp_path / "github.pem"
    private_key_path.write_text("-----BEGIN RSA PRIVATE KEY-----\ntest\n-----END RSA PRIVATE KEY-----")

    return GitHubAdapter(
        app_id="123456",
        private_key_path=str(private_key_path)
    )


@pytest.fixture
def evidence_vault(tmp_path):
    """Create Evidence Vault adapter."""
    vault_path = tmp_path / "evidence"
    return EvidenceVaultAdapter(vault_path=vault_path)


@pytest.fixture
def webhook_handler(slack_adapter, github_adapter, evidence_vault):
    """Create WebhookHandler instance."""
    return WebhookHandler(
        slack_adapter=slack_adapter,
        github_adapter=github_adapter,
        evidence_vault=evidence_vault
    )


class TestWebhookHandler:
    """Tests for WebhookHandler class."""

    def test_init(self, slack_adapter, github_adapter, evidence_vault):
        """Test WebhookHandler initialization."""
        handler = WebhookHandler(
            slack_adapter=slack_adapter,
            github_adapter=github_adapter,
            evidence_vault=evidence_vault
        )

        assert handler.slack_adapter == slack_adapter
        assert handler.github_adapter == github_adapter
        assert handler.evidence_vault == evidence_vault

    def test_register_handler(self, webhook_handler):
        """Test registering event handler."""
        def custom_handler(event_data):
            return {"processed": True}

        webhook_handler.register_handler(
            platform=PlatformType.SLACK,
            event_type="message",
            handler=custom_handler
        )

        assert "message" in webhook_handler._handlers[PlatformType.SLACK]
        assert webhook_handler._handlers[PlatformType.SLACK]["message"] == custom_handler

    def test_handle_slack_url_verification(self, webhook_handler):
        """Test Slack URL verification challenge."""
        request_body = json.dumps({
            "type": "url_verification",
            "challenge": "test_challenge_123"
        })
        timestamp = str(int(time.time()))
        signature = "v0=test_signature"

        result = webhook_handler.handle_slack_webhook(
            request_body=request_body,
            timestamp=timestamp,
            signature=signature
        )

        assert result["challenge"] == "test_challenge_123"
        assert result["status"] == "url_verified"

    def test_handle_slack_message_event(self, webhook_handler):
        """Test handling Slack message event."""
        request_body = json.dumps({
            "type": "event_callback",
            "team_id": "T123456",
            "event_id": "Ev123456",
            "event": {
                "type": "message",
                "channel": "C123456",
                "user": "U123456",
                "text": "Hello world"
            }
        })
        timestamp = str(int(time.time()))
        signature = "v0=test_signature"

        result = webhook_handler.handle_slack_webhook(
            request_body=request_body,
            timestamp=timestamp,
            signature=signature
        )

        assert result["status"] == "processed"
        assert result["event_type"] == "message"

    def test_handle_slack_webhook_signature_failure(self, webhook_handler):
        """Test Slack webhook with invalid signature."""
        # Mock signature verification to raise exception
        webhook_handler.slack_adapter.verify_webhook_signature.side_effect = Exception("Invalid signature")

        request_body = json.dumps({"type": "event_callback"})
        timestamp = str(int(time.time()))
        signature = "v0=invalid"

        with pytest.raises(WebhookError) as exc_info:
            webhook_handler.handle_slack_webhook(
                request_body=request_body,
                timestamp=timestamp,
                signature=signature
            )

        # Error message includes "Failed to process Slack webhook"
        assert "slack webhook" in str(exc_info.value).lower()

    def test_handle_slack_webhook_invalid_json(self, webhook_handler):
        """Test Slack webhook with invalid JSON."""
        request_body = "{invalid json}"
        timestamp = str(int(time.time()))
        signature = "v0=test_signature"

        with pytest.raises(WebhookError) as exc_info:
            webhook_handler.handle_slack_webhook(
                request_body=request_body,
                timestamp=timestamp,
                signature=signature
            )

        assert "Invalid JSON" in str(exc_info.value)

    def test_handle_slack_webhook_no_adapter(self, evidence_vault):
        """Test Slack webhook without adapter configured."""
        handler = WebhookHandler(evidence_vault=evidence_vault)

        with pytest.raises(WebhookError) as exc_info:
            handler.handle_slack_webhook(
                request_body="{}",
                timestamp=str(int(time.time())),
                signature="v0=test"
            )

        assert "not configured" in str(exc_info.value)

    def test_handle_github_issue_event(self, webhook_handler):
        """Test handling GitHub issue event."""
        request_body = json.dumps({
            "action": "opened",
            "issue": {
                "number": 42,
                "title": "Test issue"
            },
            "repository": {
                "full_name": "nqh/sdlc-orchestrator"
            },
            "sender": {
                "login": "nqh"
            }
        }).encode("utf-8")

        webhook_secret = "test-webhook-secret"

        # Generate valid signature
        signature = "sha256=" + hmac.new(
            webhook_secret.encode("utf-8"),
            request_body,
            hashlib.sha256
        ).hexdigest()

        result = webhook_handler.handle_github_webhook(
            request_body=request_body,
            signature=signature,
            webhook_secret=webhook_secret,
            event_type="issues"
        )

        assert result["status"] == "processed"
        assert result["event_type"] == "issues"  # X-GitHub-Event header value
        assert result["repository"] == "nqh/sdlc-orchestrator"

    def test_handle_github_pull_request_event(self, webhook_handler):
        """Test handling GitHub pull request event."""
        request_body = json.dumps({
            "action": "opened",
            "pull_request": {
                "number": 123,
                "title": "Add MCP integration",
                "draft": False
            },
            "repository": {
                "full_name": "nqh/sdlc-orchestrator"
            },
            "sender": {
                "login": "nqh"
            }
        }).encode("utf-8")

        webhook_secret = "test-webhook-secret"

        # Generate valid signature
        signature = "sha256=" + hmac.new(
            webhook_secret.encode("utf-8"),
            request_body,
            hashlib.sha256
        ).hexdigest()

        result = webhook_handler.handle_github_webhook(
            request_body=request_body,
            signature=signature,
            webhook_secret=webhook_secret,
            event_type="pull_request"
        )

        assert result["status"] == "processed"
        assert result["event_type"] == "pull_request"  # X-GitHub-Event header value

    def test_handle_github_webhook_signature_failure(self, webhook_handler):
        """Test GitHub webhook with invalid signature."""
        request_body = b'{"action":"opened"}'
        invalid_signature = "sha256=invalid_hash"
        webhook_secret = "test-secret"

        with pytest.raises(WebhookError) as exc_info:
            webhook_handler.handle_github_webhook(
                request_body=request_body,
                signature=invalid_signature,
                webhook_secret=webhook_secret
            )

        assert "signature verification failed" in str(exc_info.value).lower()

    def test_handle_github_webhook_invalid_json(self, webhook_handler):
        """Test GitHub webhook with invalid JSON."""
        request_body = b'{invalid json}'
        webhook_secret = "test-secret"

        # Generate signature for invalid JSON
        signature = "sha256=" + hmac.new(
            webhook_secret.encode("utf-8"),
            request_body,
            hashlib.sha256
        ).hexdigest()

        with pytest.raises(WebhookError) as exc_info:
            webhook_handler.handle_github_webhook(
                request_body=request_body,
                signature=signature,
                webhook_secret=webhook_secret
            )

        assert "Invalid JSON" in str(exc_info.value)

    def test_handle_github_webhook_no_adapter(self, evidence_vault):
        """Test GitHub webhook without adapter configured."""
        handler = WebhookHandler(evidence_vault=evidence_vault)

        with pytest.raises(WebhookError) as exc_info:
            handler.handle_github_webhook(
                request_body=b"{}",
                signature="sha256=test",
                webhook_secret="test"
            )

        assert "not configured" in str(exc_info.value)

    def test_route_event_with_handler(self, webhook_handler):
        """Test routing event to registered handler."""
        handled_data = []

        def custom_handler(event_data):
            handled_data.append(event_data)
            return {"success": True}

        webhook_handler.register_handler(
            platform=PlatformType.SLACK,
            event_type="message",
            handler=custom_handler
        )

        event_data = {"type": "message", "text": "test"}
        result = webhook_handler._route_event(
            platform=PlatformType.SLACK,
            event_type="message",
            event_data=event_data
        )

        assert result == {"success": True}
        assert handled_data[0] == event_data

    def test_route_event_without_handler(self, webhook_handler):
        """Test routing event without registered handler."""
        result = webhook_handler._route_event(
            platform=PlatformType.SLACK,
            event_type="unknown_event",
            event_data={}
        )

        # Should return None (event logged but not processed)
        assert result is None

    def test_route_event_handler_error(self, webhook_handler):
        """Test routing event when handler raises exception."""
        def failing_handler(event_data):
            raise ValueError("Handler error")

        webhook_handler.register_handler(
            platform=PlatformType.SLACK,
            event_type="message",
            handler=failing_handler
        )

        with pytest.raises(WebhookError) as exc_info:
            webhook_handler._route_event(
                platform=PlatformType.SLACK,
                event_type="message",
                event_data={}
            )

        assert "Handler failed" in str(exc_info.value)

    def test_evidence_artifact_creation(self, webhook_handler):
        """Test evidence artifact creation during webhook processing."""
        request_body = json.dumps({
            "type": "event_callback",
            "team_id": "T123456",
            "event_id": "Ev123456",
            "event": {"type": "message"}
        })
        timestamp = str(int(time.time()))
        signature = "v0=test_signature"

        result = webhook_handler.handle_slack_webhook(
            request_body=request_body,
            timestamp=timestamp,
            signature=signature
        )

        # Verify evidence artifact was created
        artifacts = webhook_handler.evidence_vault.list_artifacts(limit=10)
        assert len(artifacts) >= 1
        assert artifacts[0]["operation"] == "webhook_received"
        assert artifacts[0]["platform"] == "slack"

    def test_get_stats(self, webhook_handler):
        """Test getting handler statistics."""
        # Register some handlers
        webhook_handler.register_handler(
            PlatformType.SLACK,
            "message",
            lambda x: None
        )
        webhook_handler.register_handler(
            PlatformType.GITHUB,
            "issues",
            lambda x: None
        )

        stats = webhook_handler.get_stats()

        assert "handlers" in stats
        assert "platforms" in stats
        assert stats["handlers"]["slack"]["count"] == 1
        assert "message" in stats["handlers"]["slack"]["event_types"]
        assert stats["handlers"]["github"]["count"] == 1
        assert "issues" in stats["handlers"]["github"]["event_types"]
