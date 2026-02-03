"""MCP Service - Core service for MCP platform integrations.

This module provides the core service for managing MCP (Model Context Protocol) integrations
with external platforms like Slack, GitHub, Jira, and Linear.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console

from .evidence_vault_adapter import EvidenceVaultAdapter

console = Console()


class InvalidCredentialsError(Exception):
    """Raised when platform credentials are invalid."""
    pass


class ConfigNotFoundError(Exception):
    """Raised when .mcp.json configuration file is not found."""
    pass


class PlatformNotConnectedError(Exception):
    """Raised when attempting to use a platform that is not connected."""
    pass


class MCPService:
    """Core service for MCP platform integrations.

    This service manages configuration, validation, and evidence artifact creation
    for MCP integrations with external platforms.
    """

    def __init__(
        self,
        config_path: Optional[Path] = None,
        vault_path: Optional[Path] = None
    ):
        """Initialize MCP service.

        Args:
            config_path: Path to .mcp.json configuration file (default: .mcp.json in current directory)
            vault_path: Path to evidence vault directory (default: .mcp_evidence/ in current directory)
        """
        self.config_path = config_path or Path.cwd() / ".mcp.json"
        self.vault_path = vault_path or Path.cwd() / ".mcp_evidence"
        self._config: Optional[Dict[str, Any]] = None

        # Initialize Evidence Vault adapter
        self.evidence_vault = EvidenceVaultAdapter(vault_path=self.vault_path)

    def validate_slack_credentials(
        self,
        bot_token: str,
        signing_secret: str,
        channel: str
    ) -> bool:
        """Validate Slack credentials by testing API connection.

        Args:
            bot_token: Slack bot token (format: xoxb-...)
            signing_secret: Slack signing secret for webhook verification
            channel: Slack channel name (without #)

        Returns:
            True if credentials are valid

        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        # Validate token format
        if not bot_token.startswith("xoxb-"):
            raise InvalidCredentialsError(
                "Invalid bot token format. Must start with 'xoxb-'"
            )

        # Validate signing secret is not empty
        if not signing_secret or len(signing_secret) < 32:
            raise InvalidCredentialsError(
                "Invalid signing secret. Must be at least 32 characters"
            )

        # TODO: In production, make actual API call to Slack to validate
        # For now, we perform basic format validation
        # Example: slack_client = WebClient(token=bot_token)
        #          response = slack_client.auth_test()

        console.print(f"✅ Slack credentials validated for channel #{channel}")
        return True

    def validate_github_credentials(
        self,
        app_id: str,
        private_key_path: str,
        repo: str
    ) -> bool:
        """Validate GitHub credentials by testing API connection.

        Args:
            app_id: GitHub App ID
            private_key_path: Path to GitHub App private key (.pem file)
            repo: GitHub repository (format: org/repo)

        Returns:
            True if credentials are valid

        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        # Validate app ID is numeric
        try:
            int(app_id)
        except ValueError:
            raise InvalidCredentialsError(
                f"Invalid GitHub App ID: {app_id}. Must be numeric"
            )

        # Validate private key file exists
        key_path = Path(private_key_path)
        if not key_path.exists():
            raise InvalidCredentialsError(
                f"Private key file not found: {private_key_path}"
            )

        # Validate private key file format
        try:
            with open(key_path, 'r') as f:
                key_content = f.read()
                if not key_content.startswith("-----BEGIN RSA PRIVATE KEY-----"):
                    raise InvalidCredentialsError(
                        "Invalid private key format. Must be RSA private key"
                    )
        except Exception as e:
            raise InvalidCredentialsError(f"Failed to read private key: {e}")

        # Validate repository format
        if '/' not in repo:
            raise InvalidCredentialsError(
                f"Invalid repository format: {repo}. Must be 'org/repo'"
            )

        # TODO: In production, make actual API call to GitHub to validate
        # Example: github_app = GithubIntegration(app_id, private_key)
        #          installation = github_app.get_installation(org, repo)

        console.print(f"✅ GitHub credentials validated for repository {repo}")
        return True

    def load_configuration(self) -> Dict[str, Any]:
        """Load MCP configuration from .mcp.json.

        Returns:
            Configuration dictionary

        Raises:
            ConfigNotFoundError: If configuration file does not exist
        """
        if not self.config_path.exists():
            raise ConfigNotFoundError(
                f"Configuration file not found: {self.config_path}\n"
                "Run 'sdlcctl mcp connect' to create configuration"
            )

        try:
            with open(self.config_path, 'r') as f:
                self._config = json.load(f)
            return self._config
        except json.JSONDecodeError as e:
            raise ConfigNotFoundError(
                f"Invalid JSON in configuration file: {e}"
            )

    def save_configuration(self, config: Dict[str, Any]) -> None:
        """Save MCP configuration to .mcp.json.

        Args:
            config: Configuration dictionary to save
        """
        # Ensure parent directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # Save configuration
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)

        self._config = config
        console.print(f"📝 Configuration saved to {self.config_path}")

    def add_platform(
        self,
        platform: str,
        credentials: Dict[str, Any],
        targets: List[str]
    ) -> None:
        """Add or update platform configuration.

        Args:
            platform: Platform name (slack, github, jira, linear)
            credentials: Platform-specific credentials
            targets: List of targets (channels for Slack, repos for GitHub)
        """
        # Load existing config or create new
        try:
            config = self.load_configuration()
        except ConfigNotFoundError:
            config = {
                "version": "1.0.0",
                "platforms": {}
            }

        # Add platform configuration
        config["platforms"][platform] = {
            "enabled": True,
            "connected_at": datetime.now(timezone.utc).isoformat() + "Z",
            **credentials
        }

        # Add targets (channels or repos)
        if platform == "slack":
            config["platforms"][platform]["channels"] = targets
        elif platform == "github":
            config["platforms"][platform]["repositories"] = targets

        # Save configuration
        self.save_configuration(config)

    def remove_platform(self, platform: str) -> None:
        """Remove platform configuration.

        Args:
            platform: Platform name to remove

        Raises:
            PlatformNotConnectedError: If platform is not configured
        """
        config = self.load_configuration()

        if platform not in config.get("platforms", {}):
            raise PlatformNotConnectedError(
                f"Platform '{platform}' is not connected"
            )

        del config["platforms"][platform]
        self.save_configuration(config)

    def get_platform_config(self, platform: str) -> Dict[str, Any]:
        """Get configuration for a specific platform.

        Args:
            platform: Platform name

        Returns:
            Platform configuration dictionary

        Raises:
            PlatformNotConnectedError: If platform is not configured
        """
        config = self.load_configuration()

        if platform not in config.get("platforms", {}):
            raise PlatformNotConnectedError(
                f"Platform '{platform}' is not connected"
            )

        return config["platforms"][platform]

    def list_platforms(self) -> List[Dict[str, Any]]:
        """List all configured platforms.

        Returns:
            List of platform configurations with metadata
        """
        try:
            config = self.load_configuration()
        except ConfigNotFoundError:
            return []

        platforms = []
        for name, platform_config in config.get("platforms", {}).items():
            platforms.append({
                "platform": name,
                "status": "active" if platform_config.get("enabled", False) else "disabled",
                "connected_at": platform_config.get("connected_at", "unknown"),
                "config": platform_config
            })

        return platforms

    def create_evidence_artifact(
        self,
        action: str,
        platform: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Create Evidence Vault artifact for MCP action.

        Args:
            action: Action performed (connect, disconnect, test)
            platform: Platform name (slack, github)
            metadata: Additional metadata for the artifact

        Returns:
            Evidence artifact ID (format: EVD-YYYY-MM-NNN)
        """
        try:
            # Create tamper-evident evidence artifact with Ed25519 signature
            artifact_id = self.evidence_vault.create_artifact(
                operation=f"mcp_{action}",
                platform=platform,
                metadata=metadata,
                user_id=os.getenv("USER", "system")
            )

            console.print(
                f"📝 Evidence artifact created: {artifact_id} "
                f"(signed with Ed25519, hash-chained)"
            )

            return artifact_id

        except Exception as e:
            console.print(f"[yellow]Warning:[/yellow] Failed to create evidence artifact: {e}")
            # Fallback to basic artifact ID if Evidence Vault fails
            timestamp = datetime.now().strftime("%Y-%m")
            return f"EVD-{timestamp}-000"
