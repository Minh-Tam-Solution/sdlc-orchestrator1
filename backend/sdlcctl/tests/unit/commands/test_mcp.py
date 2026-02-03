"""Unit tests for MCP CLI commands."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from sdlcctl.commands.mcp import app
from sdlcctl.services.mcp.mcp_service import (
    InvalidCredentialsError,
    ConfigNotFoundError,
    PlatformNotConnectedError,
)

runner = CliRunner()


@pytest.fixture
def mock_mcp_service():
    """Mock MCP service for testing."""
    with patch('sdlcctl.commands.mcp.MCPService') as mock:
        service_instance = MagicMock()
        mock.return_value = service_instance
        yield service_instance


@pytest.fixture
def temp_config(tmp_path):
    """Create temporary .mcp.json configuration file."""
    config_path = tmp_path / ".mcp.json"
    config = {
        "version": "1.0.0",
        "platforms": {
            "slack": {
                "enabled": True,
                "channels": ["bugs", "incidents"],
                "bot_token": "{{ env.SLACK_BOT_TOKEN }}",
                "signing_secret": "{{ env.SLACK_SIGNING_SECRET }}",
                "connected_at": "2026-02-02T10:15:00Z"
            },
            "github": {
                "enabled": True,
                "repositories": ["org/sdlc-orchestrator"],
                "app_id": "123456",
                "private_key_path": "/etc/mcp/github-app.pem",
                "connected_at": "2026-02-02T10:16:00Z"
            }
        }
    }
    config_path.write_text(json.dumps(config, indent=2))
    return config_path


class TestMCPConnect:
    """Tests for mcp connect command."""

    def test_connect_slack_interactive(self, mock_mcp_service, tmp_path):
        """Test connecting to Slack with interactive prompts."""
        mock_mcp_service.validate_slack_credentials.return_value = True
        mock_mcp_service.create_evidence_artifact.return_value = "EVD-2026-02-001"

        config_path = tmp_path / ".mcp.json"

        # Simulate interactive prompts
        with patch('sdlcctl.commands.mcp.Prompt.ask') as mock_prompt:
            mock_prompt.side_effect = [
                "xoxb-test-token",  # bot_token
                "test-signing-secret",  # signing_secret
            ]

            result = runner.invoke(app, [
                'connect',
                '--slack',
                '--channel', 'bugs',
                '--config', str(config_path)
            ])

        assert result.exit_code == 0
        assert "Slack connected successfully" in result.output
        assert "EVD-2026-02-001" in result.output

        # Verify service methods were called
        mock_mcp_service.validate_slack_credentials.assert_called_once()
        mock_mcp_service.add_platform.assert_called_once()
        mock_mcp_service.create_evidence_artifact.assert_called_once()

    def test_connect_slack_with_credentials(self, mock_mcp_service, tmp_path):
        """Test connecting to Slack with credentials provided."""
        mock_mcp_service.validate_slack_credentials.return_value = True
        mock_mcp_service.create_evidence_artifact.return_value = "EVD-2026-02-002"

        config_path = tmp_path / ".mcp.json"

        result = runner.invoke(app, [
            'connect',
            '--slack',
            '--channel', 'bugs',
            '--bot-token', 'xoxb-test-token',
            '--signing-secret', 'test-secret',
            '--config', str(config_path)
        ])

        assert result.exit_code == 0
        assert "Slack connected successfully" in result.output

        # Verify credentials were validated
        mock_mcp_service.validate_slack_credentials.assert_called_with(
            'xoxb-test-token',
            'test-secret',
            'bugs'
        )

    def test_connect_slack_invalid_credentials(self, mock_mcp_service, tmp_path):
        """Test connecting to Slack with invalid credentials."""
        mock_mcp_service.validate_slack_credentials.side_effect = InvalidCredentialsError(
            "Invalid bot token format"
        )

        config_path = tmp_path / ".mcp.json"

        with patch('sdlcctl.commands.mcp.Prompt.ask') as mock_prompt:
            mock_prompt.side_effect = [
                "invalid-token",  # bot_token
                "test-secret",  # signing_secret
            ]

            result = runner.invoke(app, [
                'connect',
                '--slack',
                '--channel', 'bugs',
                '--config', str(config_path)
            ])

        assert result.exit_code == 1
        assert "Invalid bot token format" in result.output

    def test_connect_slack_no_channel(self, mock_mcp_service, tmp_path):
        """Test connecting to Slack without specifying channel."""
        config_path = tmp_path / ".mcp.json"

        with patch('sdlcctl.commands.mcp.Prompt.ask') as mock_prompt:
            mock_prompt.side_effect = [
                "xoxb-test-token",
                "test-secret",
            ]

            result = runner.invoke(app, [
                'connect',
                '--slack',
                '--config', str(config_path)
            ])

        assert result.exit_code == 1
        assert "At least one --channel is required" in result.output

    def test_connect_github(self, mock_mcp_service, tmp_path):
        """Test connecting to GitHub."""
        mock_mcp_service.validate_github_credentials.return_value = True
        mock_mcp_service.create_evidence_artifact.return_value = "EVD-2026-02-003"

        config_path = tmp_path / ".mcp.json"

        with patch('sdlcctl.commands.mcp.Prompt.ask') as mock_prompt:
            mock_prompt.side_effect = [
                "123456",  # app_id
                "/etc/mcp/github-app.pem",  # private_key_path
            ]

            result = runner.invoke(app, [
                'connect',
                '--github',
                '--repo', 'org/sdlc-orchestrator',
                '--config', str(config_path)
            ])

        assert result.exit_code == 0
        assert "GitHub connected successfully" in result.output
        assert "EVD-2026-02-003" in result.output

        # Verify service methods were called
        mock_mcp_service.validate_github_credentials.assert_called_once()
        mock_mcp_service.add_platform.assert_called_once()

    def test_connect_no_platform(self, mock_mcp_service):
        """Test connecting without specifying platform."""
        result = runner.invoke(app, ['connect'])

        assert result.exit_code == 1
        assert "Please specify at least one platform" in result.output

    def test_connect_multiple_platforms(self, mock_mcp_service, tmp_path):
        """Test connecting multiple platforms at once (should fail)."""
        config_path = tmp_path / ".mcp.json"

        result = runner.invoke(app, [
            'connect',
            '--slack',
            '--github',
            '--channel', 'bugs',
            '--repo', 'org/test',
            '--config', str(config_path)
        ])

        assert result.exit_code == 1
        assert "Please connect one platform at a time" in result.output


class TestMCPList:
    """Tests for mcp list command."""

    def test_list_platforms(self, mock_mcp_service, temp_config):
        """Test listing configured platforms."""
        mock_mcp_service.list_platforms.return_value = [
            {
                "platform": "slack",
                "status": "active",
                "connected_at": "2026-02-02T10:15:00Z",
                "config": {
                    "channels": ["bugs", "incidents"],
                    "enabled": True
                }
            },
            {
                "platform": "github",
                "status": "active",
                "connected_at": "2026-02-02T10:16:00Z",
                "config": {
                    "repositories": ["org/sdlc-orchestrator"],
                    "enabled": True
                }
            }
        ]

        result = runner.invoke(app, [
            'list',
            '--config', str(temp_config)
        ])

        assert result.exit_code == 0
        assert "MCP Integrations" in result.output
        assert "Slack" in result.output
        assert "Github" in result.output
        assert "2 Integration(s)" in result.output

    def test_list_platforms_porcelain(self, mock_mcp_service, temp_config):
        """Test listing platforms in JSON format."""
        mock_mcp_service.list_platforms.return_value = [
            {
                "platform": "slack",
                "status": "active",
                "connected_at": "2026-02-02T10:15:00Z",
                "config": {
                    "channels": ["bugs"],
                    "enabled": True
                }
            }
        ]

        result = runner.invoke(app, [
            'list',
            '--porcelain',
            '--config', str(temp_config)
        ])

        assert result.exit_code == 0

        # Parse JSON output
        output_json = json.loads(result.output)
        assert output_json["total"] == 1
        assert len(output_json["integrations"]) == 1
        assert output_json["integrations"][0]["platform"] == "slack"

    def test_list_no_config(self, mock_mcp_service, tmp_path):
        """Test listing when no configuration exists."""
        mock_mcp_service.list_platforms.side_effect = ConfigNotFoundError(
            "Configuration file not found"
        )

        config_path = tmp_path / ".mcp.json"

        result = runner.invoke(app, [
            'list',
            '--config', str(config_path)
        ])

        assert result.exit_code == 1
        assert "Configuration file not found" in result.output

    def test_list_empty(self, mock_mcp_service, temp_config):
        """Test listing when no platforms are configured."""
        mock_mcp_service.list_platforms.return_value = []

        result = runner.invoke(app, [
            'list',
            '--config', str(temp_config)
        ])

        assert result.exit_code == 0
        assert "No MCP integrations configured" in result.output


class TestMCPTest:
    """Tests for mcp test command."""

    def test_test_slack(self, mock_mcp_service, temp_config):
        """Test testing Slack integration."""
        mock_mcp_service.get_platform_config.return_value = {
            "channels": ["bugs", "incidents"],
            "enabled": True
        }

        result = runner.invoke(app, [
            'test',
            '--slack',
            '--config', str(temp_config)
        ])

        assert result.exit_code == 0
        assert "Testing Slack integration" in result.output
        assert "All checks passed" in result.output

    def test_test_github(self, mock_mcp_service, temp_config):
        """Test testing GitHub integration."""
        mock_mcp_service.get_platform_config.return_value = {
            "repositories": ["org/sdlc-orchestrator"],
            "enabled": True
        }

        result = runner.invoke(app, [
            'test',
            '--github',
            '--config', str(temp_config)
        ])

        assert result.exit_code == 0
        assert "Testing GitHub integration" in result.output
        assert "All checks passed" in result.output

    def test_test_no_platform(self, mock_mcp_service):
        """Test testing without specifying platform."""
        result = runner.invoke(app, ['test'])

        assert result.exit_code == 1
        assert "Please specify a platform to test" in result.output

    def test_test_not_connected(self, mock_mcp_service, temp_config):
        """Test testing a platform that is not connected."""
        mock_mcp_service.get_platform_config.side_effect = PlatformNotConnectedError(
            "Slack is not connected"
        )

        result = runner.invoke(app, [
            'test',
            '--slack',
            '--config', str(temp_config)
        ])

        assert result.exit_code == 1
        assert "Slack is not connected" in result.output


class TestMCPDisconnect:
    """Tests for mcp disconnect command."""

    def test_disconnect_slack_with_confirmation(self, mock_mcp_service, temp_config):
        """Test disconnecting Slack with confirmation."""
        mock_mcp_service.get_platform_config.return_value = {
            "channels": ["bugs"],
            "enabled": True
        }
        mock_mcp_service.list_platforms.return_value = [
            {"platform": "slack", "status": "active", "connected_at": "2026-02-02T10:15:00Z", "config": {}},
            {"platform": "github", "status": "active", "connected_at": "2026-02-02T10:16:00Z", "config": {}}
        ]
        mock_mcp_service.create_evidence_artifact.return_value = "EVD-2026-02-004"

        with patch('sdlcctl.commands.mcp.Confirm.ask') as mock_confirm:
            mock_confirm.return_value = True

            result = runner.invoke(app, [
                'disconnect',
                '--slack',
                '--config', str(temp_config)
            ])

        assert result.exit_code == 0
        assert "Slack disconnected successfully" in result.output
        assert "EVD-2026-02-004" in result.output

        # Verify service methods were called
        mock_mcp_service.remove_platform.assert_called_once_with("slack")

    def test_disconnect_with_force(self, mock_mcp_service, temp_config):
        """Test disconnecting with --force flag (skip confirmation)."""
        mock_mcp_service.get_platform_config.return_value = {
            "channels": ["bugs"],
            "enabled": True
        }
        mock_mcp_service.create_evidence_artifact.return_value = "EVD-2026-02-005"

        result = runner.invoke(app, [
            'disconnect',
            '--slack',
            '--force',
            '--config', str(temp_config)
        ])

        assert result.exit_code == 0
        assert "Slack disconnected successfully" in result.output

        # Verify confirmation was not asked
        mock_mcp_service.remove_platform.assert_called_once_with("slack")

    def test_disconnect_cancelled(self, mock_mcp_service, temp_config):
        """Test disconnecting when user cancels confirmation."""
        mock_mcp_service.get_platform_config.return_value = {
            "channels": ["bugs"],
            "enabled": True
        }
        mock_mcp_service.list_platforms.return_value = []

        with patch('sdlcctl.commands.mcp.Confirm.ask') as mock_confirm:
            mock_confirm.return_value = False

            result = runner.invoke(app, [
                'disconnect',
                '--slack',
                '--config', str(temp_config)
            ])

        assert result.exit_code == 0
        assert "Cancelled" in result.output

        # Verify platform was not removed
        mock_mcp_service.remove_platform.assert_not_called()

    def test_disconnect_not_connected(self, mock_mcp_service, temp_config):
        """Test disconnecting a platform that is not connected."""
        mock_mcp_service.get_platform_config.side_effect = PlatformNotConnectedError(
            "Slack is not connected"
        )

        result = runner.invoke(app, [
            'disconnect',
            '--slack',
            '--config', str(temp_config)
        ])

        assert result.exit_code == 1
        assert "Slack is not connected" in result.output

    def test_disconnect_no_platform(self, mock_mcp_service):
        """Test disconnecting without specifying platform."""
        result = runner.invoke(app, ['disconnect'])

        assert result.exit_code == 1
        assert "Please specify a platform to disconnect" in result.output
