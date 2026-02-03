"""Unit tests for MCP service."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sdlcctl.services.mcp.mcp_service import (
    MCPService,
    InvalidCredentialsError,
    ConfigNotFoundError,
    PlatformNotConnectedError,
)


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


@pytest.fixture
def temp_private_key(tmp_path):
    """Create temporary private key file."""
    key_path = tmp_path / "github-app.pem"
    key_content = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
-----END RSA PRIVATE KEY-----"""
    key_path.write_text(key_content)
    return key_path


class TestMCPService:
    """Tests for MCPService class."""

    def test_init(self, tmp_path):
        """Test MCPService initialization."""
        config_path = tmp_path / ".mcp.json"
        service = MCPService(config_path=config_path)

        assert service.config_path == config_path
        assert service._config is None

    def test_init_default_path(self):
        """Test MCPService initialization with default path."""
        service = MCPService()

        assert service.config_path == Path.cwd() / ".mcp.json"

    def test_validate_slack_credentials_valid(self):
        """Test validating valid Slack credentials."""
        service = MCPService()

        result = service.validate_slack_credentials(
            bot_token="xoxb-test-token",
            signing_secret="a" * 32,
            channel="bugs"
        )

        assert result is True

    def test_validate_slack_credentials_invalid_token(self):
        """Test validating Slack credentials with invalid token format."""
        service = MCPService()

        with pytest.raises(InvalidCredentialsError) as exc_info:
            service.validate_slack_credentials(
                bot_token="invalid-token",
                signing_secret="a" * 32,
                channel="bugs"
            )

        assert "Invalid bot token format" in str(exc_info.value)

    def test_validate_slack_credentials_invalid_secret(self):
        """Test validating Slack credentials with invalid signing secret."""
        service = MCPService()

        with pytest.raises(InvalidCredentialsError) as exc_info:
            service.validate_slack_credentials(
                bot_token="xoxb-test-token",
                signing_secret="short",
                channel="bugs"
            )

        assert "Invalid signing secret" in str(exc_info.value)

    def test_validate_github_credentials_valid(self, temp_private_key):
        """Test validating valid GitHub credentials."""
        service = MCPService()

        result = service.validate_github_credentials(
            app_id="123456",
            private_key_path=str(temp_private_key),
            repo="org/sdlc-orchestrator"
        )

        assert result is True

    def test_validate_github_credentials_invalid_app_id(self, temp_private_key):
        """Test validating GitHub credentials with invalid app ID."""
        service = MCPService()

        with pytest.raises(InvalidCredentialsError) as exc_info:
            service.validate_github_credentials(
                app_id="invalid-id",
                private_key_path=str(temp_private_key),
                repo="org/sdlc-orchestrator"
            )

        assert "Invalid GitHub App ID" in str(exc_info.value)

    def test_validate_github_credentials_missing_key(self):
        """Test validating GitHub credentials with missing private key."""
        service = MCPService()

        with pytest.raises(InvalidCredentialsError) as exc_info:
            service.validate_github_credentials(
                app_id="123456",
                private_key_path="/nonexistent/key.pem",
                repo="org/sdlc-orchestrator"
            )

        assert "Private key file not found" in str(exc_info.value)

    def test_validate_github_credentials_invalid_key_format(self, tmp_path):
        """Test validating GitHub credentials with invalid key format."""
        service = MCPService()

        # Create invalid key file
        invalid_key_path = tmp_path / "invalid.pem"
        invalid_key_path.write_text("Not a valid private key")

        with pytest.raises(InvalidCredentialsError) as exc_info:
            service.validate_github_credentials(
                app_id="123456",
                private_key_path=str(invalid_key_path),
                repo="org/sdlc-orchestrator"
            )

        assert "Invalid private key format" in str(exc_info.value)

    def test_validate_github_credentials_invalid_repo_format(self, temp_private_key):
        """Test validating GitHub credentials with invalid repo format."""
        service = MCPService()

        with pytest.raises(InvalidCredentialsError) as exc_info:
            service.validate_github_credentials(
                app_id="123456",
                private_key_path=str(temp_private_key),
                repo="invalid-repo"
            )

        assert "Invalid repository format" in str(exc_info.value)

    def test_load_configuration(self, temp_config):
        """Test loading configuration from .mcp.json."""
        service = MCPService(config_path=temp_config)

        config = service.load_configuration()

        assert config["version"] == "1.0.0"
        assert "slack" in config["platforms"]
        assert "github" in config["platforms"]

    def test_load_configuration_not_found(self, tmp_path):
        """Test loading configuration when file doesn't exist."""
        service = MCPService(config_path=tmp_path / "nonexistent.json")

        with pytest.raises(ConfigNotFoundError) as exc_info:
            service.load_configuration()

        assert "Configuration file not found" in str(exc_info.value)

    def test_load_configuration_invalid_json(self, tmp_path):
        """Test loading configuration with invalid JSON."""
        config_path = tmp_path / ".mcp.json"
        config_path.write_text("{ invalid json }")

        service = MCPService(config_path=config_path)

        with pytest.raises(ConfigNotFoundError) as exc_info:
            service.load_configuration()

        assert "Invalid JSON" in str(exc_info.value)

    def test_save_configuration(self, tmp_path):
        """Test saving configuration to .mcp.json."""
        config_path = tmp_path / ".mcp.json"
        service = MCPService(config_path=config_path)

        config = {
            "version": "1.0.0",
            "platforms": {
                "slack": {
                    "enabled": True,
                    "channels": ["bugs"]
                }
            }
        }

        service.save_configuration(config)

        # Verify file was created
        assert config_path.exists()

        # Verify content
        saved_config = json.loads(config_path.read_text())
        assert saved_config == config

    def test_add_platform_slack(self, tmp_path):
        """Test adding Slack platform configuration."""
        config_path = tmp_path / ".mcp.json"
        service = MCPService(config_path=config_path)

        credentials = {
            "bot_token": "{{ env.SLACK_BOT_TOKEN }}",
            "signing_secret": "{{ env.SLACK_SIGNING_SECRET }}",
        }

        service.add_platform("slack", credentials, ["bugs", "incidents"])

        # Verify configuration was saved
        config = service.load_configuration()
        assert "slack" in config["platforms"]
        assert config["platforms"]["slack"]["enabled"] is True
        assert config["platforms"]["slack"]["channels"] == ["bugs", "incidents"]

    def test_add_platform_github(self, tmp_path):
        """Test adding GitHub platform configuration."""
        config_path = tmp_path / ".mcp.json"
        service = MCPService(config_path=config_path)

        credentials = {
            "app_id": "123456",
            "private_key_path": "/etc/mcp/github-app.pem",
        }

        service.add_platform("github", credentials, ["org/sdlc-orchestrator"])

        # Verify configuration was saved
        config = service.load_configuration()
        assert "github" in config["platforms"]
        assert config["platforms"]["github"]["enabled"] is True
        assert config["platforms"]["github"]["repositories"] == ["org/sdlc-orchestrator"]

    def test_add_platform_update_existing(self, temp_config):
        """Test updating existing platform configuration."""
        service = MCPService(config_path=temp_config)

        # Load existing config
        original_config = service.load_configuration()
        assert "slack" in original_config["platforms"]

        # Update Slack with new channels
        credentials = {
            "bot_token": "{{ env.SLACK_BOT_TOKEN }}",
            "signing_secret": "{{ env.SLACK_SIGNING_SECRET }}",
        }
        service.add_platform("slack", credentials, ["bugs", "incidents", "support"])

        # Verify update
        updated_config = service.load_configuration()
        assert updated_config["platforms"]["slack"]["channels"] == ["bugs", "incidents", "support"]

    def test_remove_platform(self, temp_config):
        """Test removing platform configuration."""
        service = MCPService(config_path=temp_config)

        # Remove Slack
        service.remove_platform("slack")

        # Verify removal
        config = service.load_configuration()
        assert "slack" not in config["platforms"]
        assert "github" in config["platforms"]  # GitHub should remain

    def test_remove_platform_not_connected(self, temp_config):
        """Test removing platform that is not connected."""
        service = MCPService(config_path=temp_config)

        with pytest.raises(PlatformNotConnectedError) as exc_info:
            service.remove_platform("jira")

        assert "Platform 'jira' is not connected" in str(exc_info.value)

    def test_get_platform_config(self, temp_config):
        """Test getting platform configuration."""
        service = MCPService(config_path=temp_config)

        slack_config = service.get_platform_config("slack")

        assert slack_config["enabled"] is True
        assert slack_config["channels"] == ["bugs", "incidents"]

    def test_get_platform_config_not_connected(self, temp_config):
        """Test getting platform configuration for non-connected platform."""
        service = MCPService(config_path=temp_config)

        with pytest.raises(PlatformNotConnectedError) as exc_info:
            service.get_platform_config("jira")

        assert "Platform 'jira' is not connected" in str(exc_info.value)

    def test_list_platforms(self, temp_config):
        """Test listing all platforms."""
        service = MCPService(config_path=temp_config)

        platforms = service.list_platforms()

        assert len(platforms) == 2
        assert platforms[0]["platform"] == "slack"
        assert platforms[0]["status"] == "active"
        assert platforms[1]["platform"] == "github"
        assert platforms[1]["status"] == "active"

    def test_list_platforms_empty(self, tmp_path):
        """Test listing platforms when config doesn't exist."""
        service = MCPService(config_path=tmp_path / ".mcp.json")

        platforms = service.list_platforms()

        assert platforms == []

    def test_create_evidence_artifact(self, tmp_path):
        """Test creating Evidence Vault artifact."""
        service = MCPService(config_path=tmp_path / ".mcp.json")

        artifact_id = service.create_evidence_artifact(
            action="connect",
            platform="slack",
            metadata={
                "channels": ["bugs"],
                "bot_token": "xoxb-test-token",
            }
        )

        # Verify artifact ID format
        assert artifact_id.startswith("EVD-")
        assert len(artifact_id) > 10
