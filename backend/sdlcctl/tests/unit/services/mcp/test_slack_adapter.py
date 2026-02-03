"""Unit tests for Slack adapter."""

import hashlib
import hmac
import time
from unittest.mock import MagicMock, patch

import pytest

from sdlcctl.services.mcp.slack_adapter import (
    SlackAdapter,
    SlackAPIError,
    SlackSignatureError,
)


@pytest.fixture
def slack_adapter():
    """Create SlackAdapter instance for testing."""
    return SlackAdapter(
        bot_token="xoxb-test-token-123",
        signing_secret="test-signing-secret-32-chars-long"
    )


@pytest.fixture
def mock_slack_response():
    """Mock successful Slack API response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}
    return mock_response


class TestSlackAdapter:
    """Tests for SlackAdapter class."""

    def test_init(self):
        """Test SlackAdapter initialization."""
        adapter = SlackAdapter(
            bot_token="xoxb-test",
            signing_secret="secret"
        )

        assert adapter.bot_token == "xoxb-test"
        assert adapter.signing_secret == "secret"
        assert adapter.api_base_url == "https://slack.com/api"

    @patch('sdlcctl.services.mcp.slack_adapter.requests.post')
    def test_validate_bot_token_success(self, mock_post, slack_adapter):
        """Test validating bot token successfully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": True,
            "user": "sdlc-bot",
            "user_id": "U123456",
            "team": "ACME Corp",
            "team_id": "T123456",
            "url": "https://acme.slack.com"
        }
        mock_post.return_value = mock_response

        result = slack_adapter.validate_bot_token()

        assert result["user"] == "sdlc-bot"
        assert result["team"] == "ACME Corp"
        mock_post.assert_called_once()

    @patch('sdlcctl.services.mcp.slack_adapter.requests.post')
    def test_validate_bot_token_invalid(self, mock_post, slack_adapter):
        """Test validating invalid bot token."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": False,
            "error": "invalid_auth"
        }
        mock_post.return_value = mock_response

        with pytest.raises(SlackAPIError) as exc_info:
            slack_adapter.validate_bot_token()

        assert "invalid_auth" in str(exc_info.value)

    def test_verify_webhook_signature_valid(self, slack_adapter):
        """Test verifying valid webhook signature."""
        # Prepare test data
        request_body = '{"type":"event_callback"}'
        timestamp = str(int(time.time()))
        signing_secret = slack_adapter.signing_secret

        # Generate valid signature
        sig_basestring = f"v0:{timestamp}:{request_body}"
        signature = 'v0=' + hmac.new(
            signing_secret.encode('utf-8'),
            sig_basestring.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # Verify signature
        result = slack_adapter.verify_webhook_signature(
            request_body=request_body,
            timestamp=timestamp,
            signature=signature
        )

        assert result is True

    def test_verify_webhook_signature_invalid(self, slack_adapter):
        """Test verifying invalid webhook signature."""
        request_body = '{"type":"event_callback"}'
        timestamp = str(int(time.time()))
        invalid_signature = 'v0=invalid_signature_hash'

        with pytest.raises(SlackSignatureError) as exc_info:
            slack_adapter.verify_webhook_signature(
                request_body=request_body,
                timestamp=timestamp,
                signature=invalid_signature
            )

        assert "Signature verification failed" in str(exc_info.value)

    def test_verify_webhook_signature_old_timestamp(self, slack_adapter):
        """Test verifying signature with old timestamp (replay attack)."""
        request_body = '{"type":"event_callback"}'
        # Timestamp from 10 minutes ago (600 seconds)
        old_timestamp = str(int(time.time()) - 600)
        signing_secret = slack_adapter.signing_secret

        # Generate valid signature for old timestamp
        sig_basestring = f"v0:{old_timestamp}:{request_body}"
        signature = 'v0=' + hmac.new(
            signing_secret.encode('utf-8'),
            sig_basestring.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        with pytest.raises(SlackSignatureError) as exc_info:
            slack_adapter.verify_webhook_signature(
                request_body=request_body,
                timestamp=old_timestamp,
                signature=signature
            )

        assert "Request timestamp too old" in str(exc_info.value)

    @patch('sdlcctl.services.mcp.slack_adapter.requests.get')
    def test_check_channel_access_success(self, mock_get, slack_adapter):
        """Test checking channel access successfully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": True,
            "channels": [
                {
                    "id": "C123456",
                    "name": "bugs",
                    "is_member": True
                }
            ]
        }
        mock_get.return_value = mock_response

        result = slack_adapter.check_channel_access("bugs")

        assert result is True

    @patch('sdlcctl.services.mcp.slack_adapter.requests.get')
    def test_check_channel_access_not_member(self, mock_get, slack_adapter):
        """Test checking channel access when bot is not a member."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": True,
            "channels": [
                {
                    "id": "C123456",
                    "name": "bugs",
                    "is_member": False
                }
            ]
        }
        mock_get.return_value = mock_response

        with pytest.raises(SlackAPIError) as exc_info:
            slack_adapter.check_channel_access("bugs")

        assert "not a member" in str(exc_info.value)

    @patch('sdlcctl.services.mcp.slack_adapter.requests.get')
    def test_check_channel_access_not_found(self, mock_get, slack_adapter):
        """Test checking channel access for non-existent channel."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": True,
            "channels": []
        }
        mock_get.return_value = mock_response

        with pytest.raises(SlackAPIError) as exc_info:
            slack_adapter.check_channel_access("nonexistent")

        assert "not found" in str(exc_info.value)

    @patch('sdlcctl.services.mcp.slack_adapter.requests.post')
    def test_post_message_success(self, mock_post, slack_adapter):
        """Test posting message successfully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": True,
            "ts": "1234567890.123456",
            "channel": "C123456",
            "message": {"text": "Test message"}
        }
        mock_post.return_value = mock_response

        result = slack_adapter.post_message(
            channel="bugs",
            text="Test message"
        )

        assert result["ts"] == "1234567890.123456"
        assert result["channel"] == "C123456"

    @patch('sdlcctl.services.mcp.slack_adapter.requests.post')
    def test_post_message_with_thread(self, mock_post, slack_adapter):
        """Test posting message to a thread."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": True,
            "ts": "1234567890.123457",
            "channel": "C123456"
        }
        mock_post.return_value = mock_response

        result = slack_adapter.post_message(
            channel="bugs",
            text="Reply message",
            thread_ts="1234567890.123456"
        )

        assert result["ts"] == "1234567890.123457"

        # Verify thread_ts was passed in request
        call_args = mock_post.call_args
        assert call_args[1]["json"]["thread_ts"] == "1234567890.123456"

    @patch('sdlcctl.services.mcp.slack_adapter.requests.post')
    def test_post_message_failure(self, mock_post, slack_adapter):
        """Test posting message failure."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": False,
            "error": "channel_not_found"
        }
        mock_post.return_value = mock_response

        with pytest.raises(SlackAPIError) as exc_info:
            slack_adapter.post_message(
                channel="nonexistent",
                text="Test message"
            )

        assert "channel_not_found" in str(exc_info.value)

    @patch('sdlcctl.services.mcp.slack_adapter.requests.get')
    def test_get_thread_context_success(self, mock_get, slack_adapter):
        """Test retrieving thread context successfully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": True,
            "messages": [
                {"text": "First message", "ts": "1234567890.123456"},
                {"text": "Reply", "ts": "1234567890.123457"}
            ],
            "has_more": False
        }
        mock_get.return_value = mock_response

        result = slack_adapter.get_thread_context(
            channel="C123456",
            thread_ts="1234567890.123456"
        )

        assert len(result["messages"]) == 2
        assert result["has_more"] is False

    @patch('sdlcctl.services.mcp.slack_adapter.requests.get')
    def test_get_thread_context_with_limit(self, mock_get, slack_adapter):
        """Test retrieving thread context with custom limit."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": True,
            "messages": [],
            "has_more": True
        }
        mock_get.return_value = mock_response

        slack_adapter.get_thread_context(
            channel="C123456",
            thread_ts="1234567890.123456",
            limit=5
        )

        # Verify limit was passed in request
        call_args = mock_get.call_args
        assert call_args[1]["params"]["limit"] == 5

    def test_handle_rate_limit(self, slack_adapter):
        """Test handling rate limit response."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "60"}

        retry_after = slack_adapter.handle_rate_limit(mock_response)

        assert retry_after == 60

    def test_handle_rate_limit_no_header(self, slack_adapter):
        """Test handling rate limit without Retry-After header."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {}

        retry_after = slack_adapter.handle_rate_limit(mock_response)

        assert retry_after == 60  # Default

    def test_handle_rate_limit_not_rate_limited(self, slack_adapter):
        """Test handling non-rate-limit response."""
        mock_response = MagicMock()
        mock_response.status_code = 200

        retry_after = slack_adapter.handle_rate_limit(mock_response)

        assert retry_after is None
