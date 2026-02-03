"""Configuration manager for MCP integrations.

This module provides configuration management with AES-256 encryption, environment
variable substitution, and JSON schema validation.
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

from cryptography.fernet import Fernet
from rich.console import Console

console = Console()


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""
    pass


class ConfigEncryptionError(Exception):
    """Raised when encryption/decryption fails."""
    pass


class ConfigManager:
    """Manager for MCP configuration with encryption and validation.

    This manager provides methods for loading, saving, encrypting, and validating
    .mcp.json configuration files.
    """

    # JSON schema for .mcp.json validation
    CONFIG_SCHEMA = {
        "type": "object",
        "required": ["version", "platforms"],
        "properties": {
            "version": {
                "type": "string",
                "pattern": r"^\d+\.\d+\.\d+$"
            },
            "platforms": {
                "type": "object",
                "additionalProperties": {
                    "type": "object",
                    "required": ["enabled", "connected_at"],
                    "properties": {
                        "enabled": {"type": "boolean"},
                        "connected_at": {"type": "string"}
                    }
                }
            }
        }
    }

    def __init__(self, config_path: Path, encryption_key: Optional[str] = None):
        """Initialize config manager.

        Args:
            config_path: Path to .mcp.json configuration file
            encryption_key: Optional encryption key for secrets (base64-encoded)
                           If not provided, will try to load from MCP_ENCRYPTION_KEY env var
        """
        self.config_path = config_path
        self._encryption_key = encryption_key or os.getenv("MCP_ENCRYPTION_KEY")
        self._fernet: Optional[Fernet] = None

        if self._encryption_key:
            try:
                self._fernet = Fernet(self._encryption_key.encode())
            except Exception as e:
                console.print(f"[yellow]Warning:[/yellow] Invalid encryption key: {e}")

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from .mcp.json.

        Returns:
            Configuration dictionary with environment variables substituted

        Raises:
            FileNotFoundError: If configuration file doesn't exist
            ConfigValidationError: If configuration is invalid
        """
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            # Validate schema
            self._validate_schema(config)

            # Substitute environment variables
            config = self._substitute_env_vars(config)

            return config

        except json.JSONDecodeError as e:
            raise ConfigValidationError(
                f"Invalid JSON in configuration file: {e}"
            )

    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to .mcp.json.

        Args:
            config: Configuration dictionary to save

        Raises:
            ConfigValidationError: If configuration is invalid
        """
        # Validate schema before saving
        self._validate_schema(config)

        # Ensure parent directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # Save configuration
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)

    def encrypt_secret(self, plaintext: str) -> str:
        """Encrypt a secret using AES-256.

        Args:
            plaintext: Secret to encrypt

        Returns:
            Encrypted secret (base64-encoded)

        Raises:
            ConfigEncryptionError: If encryption fails or no encryption key available
        """
        if not self._fernet:
            raise ConfigEncryptionError(
                "No encryption key available. Set MCP_ENCRYPTION_KEY environment variable."
            )

        try:
            encrypted = self._fernet.encrypt(plaintext.encode())
            return encrypted.decode()
        except Exception as e:
            raise ConfigEncryptionError(f"Failed to encrypt secret: {e}")

    def decrypt_secret(self, ciphertext: str) -> str:
        """Decrypt a secret using AES-256.

        Args:
            ciphertext: Encrypted secret (base64-encoded)

        Returns:
            Decrypted secret

        Raises:
            ConfigEncryptionError: If decryption fails or no encryption key available
        """
        if not self._fernet:
            raise ConfigEncryptionError(
                "No encryption key available. Set MCP_ENCRYPTION_KEY environment variable."
            )

        try:
            decrypted = self._fernet.decrypt(ciphertext.encode())
            return decrypted.decode()
        except Exception as e:
            raise ConfigEncryptionError(f"Failed to decrypt secret: {e}")

    def _substitute_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Substitute environment variables in configuration.

        Replaces {{ env.VAR_NAME }} placeholders with actual environment variable values.

        Args:
            config: Configuration dictionary

        Returns:
            Configuration with environment variables substituted
        """
        config_str = json.dumps(config)

        # Pattern to match {{ env.VAR_NAME }}
        pattern = r'\{\{\s*env\.(\w+)\s*\}\}'

        def replace_env_var(match):
            var_name = match.group(1)
            value = os.getenv(var_name)

            if value is None:
                console.print(
                    f"[yellow]Warning:[/yellow] Environment variable {var_name} not set"
                )
                return match.group(0)  # Keep placeholder if env var not set

            return value

        config_str = re.sub(pattern, replace_env_var, config_str)
        return json.loads(config_str)

    def _validate_schema(self, config: Dict[str, Any]) -> None:
        """Validate configuration against JSON schema.

        Args:
            config: Configuration dictionary to validate

        Raises:
            ConfigValidationError: If validation fails
        """
        # Check required top-level fields
        if "version" not in config:
            raise ConfigValidationError("Missing required field: version")

        if "platforms" not in config:
            raise ConfigValidationError("Missing required field: platforms")

        # Validate version format
        version_pattern = r'^\d+\.\d+\.\d+$'
        if not re.match(version_pattern, config["version"]):
            raise ConfigValidationError(
                f"Invalid version format: {config['version']}. "
                f"Expected format: X.Y.Z (e.g., 1.0.0)"
            )

        # Validate platforms
        if not isinstance(config["platforms"], dict):
            raise ConfigValidationError(
                f"'platforms' must be an object, got: {type(config['platforms']).__name__}"
            )

        # Validate each platform
        for platform_name, platform_config in config["platforms"].items():
            if not isinstance(platform_config, dict):
                raise ConfigValidationError(
                    f"Platform '{platform_name}' config must be an object"
                )

            # Check required platform fields
            if "enabled" not in platform_config:
                raise ConfigValidationError(
                    f"Platform '{platform_name}' missing required field: enabled"
                )

            if "connected_at" not in platform_config:
                raise ConfigValidationError(
                    f"Platform '{platform_name}' missing required field: connected_at"
                )

            # Validate enabled is boolean
            if not isinstance(platform_config["enabled"], bool):
                raise ConfigValidationError(
                    f"Platform '{platform_name}' field 'enabled' must be boolean"
                )

    def generate_encryption_key(self) -> str:
        """Generate a new AES-256 encryption key.

        Returns:
            Base64-encoded encryption key
        """
        key = Fernet.generate_key()
        return key.decode()

    def update_platform_config(
        self,
        platform: str,
        updates: Dict[str, Any]
    ) -> None:
        """Update configuration for a specific platform.

        Args:
            platform: Platform name (slack, github, etc.)
            updates: Dictionary of fields to update

        Raises:
            FileNotFoundError: If configuration file doesn't exist
            ConfigValidationError: If platform not found
        """
        config = self.load_config()

        if platform not in config.get("platforms", {}):
            raise ConfigValidationError(
                f"Platform '{platform}' not found in configuration"
            )

        # Update platform config
        config["platforms"][platform].update(updates)

        # Save updated config
        self.save_config(config)

    def remove_platform_config(self, platform: str) -> None:
        """Remove configuration for a specific platform.

        Args:
            platform: Platform name to remove

        Raises:
            FileNotFoundError: If configuration file doesn't exist
            ConfigValidationError: If platform not found
        """
        config = self.load_config()

        if platform not in config.get("platforms", {}):
            raise ConfigValidationError(
                f"Platform '{platform}' not found in configuration"
            )

        # Remove platform config
        del config["platforms"][platform]

        # Save updated config
        self.save_config(config)
