"""Unit tests for Config Manager."""

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest
from cryptography.fernet import Fernet

from sdlcctl.services.mcp.config_manager import (
    ConfigEncryptionError,
    ConfigManager,
    ConfigValidationError,
)


@pytest.fixture
def config_path(tmp_path):
    """Create temporary config path."""
    return tmp_path / ".mcp.json"


@pytest.fixture
def encryption_key():
    """Generate encryption key for testing."""
    return Fernet.generate_key().decode()


@pytest.fixture
def valid_config():
    """Create valid configuration."""
    return {
        "version": "1.0.0",
        "platforms": {
            "slack": {
                "enabled": True,
                "connected_at": "2026-02-04T10:00:00Z",
                "bot_token": "{{ env.SLACK_BOT_TOKEN }}",
                "channels": ["bugs", "alerts"]
            },
            "github": {
                "enabled": True,
                "connected_at": "2026-02-04T10:00:00Z",
                "app_id": "123456",
                "repo": "nqh/sdlc-orchestrator"
            }
        }
    }


@pytest.fixture
def config_manager(config_path, encryption_key):
    """Create ConfigManager instance for testing."""
    return ConfigManager(config_path=config_path, encryption_key=encryption_key)


class TestConfigManager:
    """Tests for ConfigManager class."""

    def test_init(self, config_path, encryption_key):
        """Test ConfigManager initialization."""
        manager = ConfigManager(config_path=config_path, encryption_key=encryption_key)

        assert manager.config_path == config_path
        assert manager._encryption_key == encryption_key
        assert manager._fernet is not None

    def test_init_no_encryption_key(self, config_path):
        """Test ConfigManager initialization without encryption key."""
        manager = ConfigManager(config_path=config_path)

        assert manager.config_path == config_path
        assert manager._encryption_key is None
        assert manager._fernet is None

    def test_init_invalid_encryption_key(self, config_path):
        """Test ConfigManager initialization with invalid encryption key."""
        with patch('sdlcctl.services.mcp.config_manager.console.print') as mock_print:
            manager = ConfigManager(config_path=config_path, encryption_key="invalid-key")

            assert manager._fernet is None
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            assert "Warning" in call_args
            assert "Invalid encryption key" in call_args

    def test_load_config_success(self, config_manager, config_path, valid_config):
        """Test loading configuration successfully."""
        # Write config file
        with open(config_path, 'w') as f:
            json.dump(valid_config, f)

        # Set environment variable for substitution
        os.environ['SLACK_BOT_TOKEN'] = 'xoxb-test-token'

        try:
            config = config_manager.load_config()

            assert config["version"] == "1.0.0"
            assert "slack" in config["platforms"]
            assert config["platforms"]["slack"]["bot_token"] == "xoxb-test-token"
        finally:
            del os.environ['SLACK_BOT_TOKEN']

    def test_load_config_file_not_found(self, config_manager):
        """Test loading configuration when file doesn't exist."""
        with pytest.raises(FileNotFoundError) as exc_info:
            config_manager.load_config()

        assert "Configuration file not found" in str(exc_info.value)

    def test_load_config_invalid_json(self, config_manager, config_path):
        """Test loading configuration with invalid JSON."""
        # Write invalid JSON
        with open(config_path, 'w') as f:
            f.write("{invalid json}")

        with pytest.raises(ConfigValidationError) as exc_info:
            config_manager.load_config()

        assert "Invalid JSON" in str(exc_info.value)

    def test_load_config_missing_version(self, config_manager, config_path):
        """Test loading configuration missing version field."""
        config = {"platforms": {}}
        with open(config_path, 'w') as f:
            json.dump(config, f)

        with pytest.raises(ConfigValidationError) as exc_info:
            config_manager.load_config()

        assert "Missing required field: version" in str(exc_info.value)

    def test_load_config_missing_platforms(self, config_manager, config_path):
        """Test loading configuration missing platforms field."""
        config = {"version": "1.0.0"}
        with open(config_path, 'w') as f:
            json.dump(config, f)

        with pytest.raises(ConfigValidationError) as exc_info:
            config_manager.load_config()

        assert "Missing required field: platforms" in str(exc_info.value)

    def test_save_config_success(self, config_manager, config_path, valid_config):
        """Test saving configuration successfully."""
        config_manager.save_config(valid_config)

        assert config_path.exists()

        with open(config_path, 'r') as f:
            saved_config = json.load(f)

        assert saved_config == valid_config

    def test_save_config_creates_directory(self, tmp_path, encryption_key):
        """Test saving configuration creates parent directory."""
        config_path = tmp_path / "subdir" / ".mcp.json"
        manager = ConfigManager(config_path=config_path, encryption_key=encryption_key)

        config = {
            "version": "1.0.0",
            "platforms": {
                "slack": {
                    "enabled": True,
                    "connected_at": "2026-02-04T10:00:00Z"
                }
            }
        }

        manager.save_config(config)

        assert config_path.exists()
        assert config_path.parent.exists()

    def test_save_config_invalid_schema(self, config_manager):
        """Test saving configuration with invalid schema."""
        invalid_config = {
            "version": "1.0.0",
            "platforms": "invalid"  # Should be object
        }

        with pytest.raises(ConfigValidationError) as exc_info:
            config_manager.save_config(invalid_config)

        assert "'platforms' must be an object" in str(exc_info.value)

    def test_encrypt_secret_success(self, config_manager):
        """Test encrypting secret successfully."""
        plaintext = "my-secret-token"

        ciphertext = config_manager.encrypt_secret(plaintext)

        assert ciphertext != plaintext
        assert len(ciphertext) > 0

    def test_encrypt_secret_no_key(self, config_path):
        """Test encrypting secret without encryption key."""
        manager = ConfigManager(config_path=config_path)

        with pytest.raises(ConfigEncryptionError) as exc_info:
            manager.encrypt_secret("my-secret")

        assert "No encryption key available" in str(exc_info.value)

    def test_decrypt_secret_success(self, config_manager):
        """Test decrypting secret successfully."""
        plaintext = "my-secret-token"
        ciphertext = config_manager.encrypt_secret(plaintext)

        decrypted = config_manager.decrypt_secret(ciphertext)

        assert decrypted == plaintext

    def test_decrypt_secret_no_key(self, config_path):
        """Test decrypting secret without encryption key."""
        manager = ConfigManager(config_path=config_path)

        with pytest.raises(ConfigEncryptionError) as exc_info:
            manager.decrypt_secret("encrypted-data")

        assert "No encryption key available" in str(exc_info.value)

    def test_decrypt_secret_invalid_ciphertext(self, config_manager):
        """Test decrypting invalid ciphertext."""
        with pytest.raises(ConfigEncryptionError) as exc_info:
            config_manager.decrypt_secret("invalid-ciphertext")

        assert "Failed to decrypt secret" in str(exc_info.value)

    def test_substitute_env_vars_success(self, config_manager):
        """Test substituting environment variables successfully."""
        config = {
            "version": "1.0.0",
            "platforms": {
                "slack": {
                    "bot_token": "{{ env.SLACK_BOT_TOKEN }}",
                    "signing_secret": "{{ env.SLACK_SIGNING_SECRET }}"
                }
            }
        }

        os.environ['SLACK_BOT_TOKEN'] = 'xoxb-test-token'
        os.environ['SLACK_SIGNING_SECRET'] = 'test-secret'

        try:
            result = config_manager._substitute_env_vars(config)

            assert result["platforms"]["slack"]["bot_token"] == "xoxb-test-token"
            assert result["platforms"]["slack"]["signing_secret"] == "test-secret"
        finally:
            del os.environ['SLACK_BOT_TOKEN']
            del os.environ['SLACK_SIGNING_SECRET']

    def test_substitute_env_vars_missing(self, config_manager):
        """Test substituting missing environment variables."""
        config = {
            "version": "1.0.0",
            "platforms": {
                "slack": {
                    "bot_token": "{{ env.MISSING_VAR }}"
                }
            }
        }

        with patch('sdlcctl.services.mcp.config_manager.console.print') as mock_print:
            result = config_manager._substitute_env_vars(config)

            # Placeholder should remain
            assert "{{ env.MISSING_VAR }}" in str(result)

            # Warning should be printed
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            assert "Warning" in call_args
            assert "MISSING_VAR" in call_args

    def test_validate_schema_valid(self, config_manager, valid_config):
        """Test validating valid schema."""
        # Should not raise exception
        config_manager._validate_schema(valid_config)

    def test_validate_schema_invalid_version_format(self, config_manager):
        """Test validating schema with invalid version format."""
        config = {
            "version": "invalid",
            "platforms": {}
        }

        with pytest.raises(ConfigValidationError) as exc_info:
            config_manager._validate_schema(config)

        assert "Invalid version format" in str(exc_info.value)

    def test_validate_schema_platform_missing_enabled(self, config_manager):
        """Test validating schema with platform missing enabled field."""
        config = {
            "version": "1.0.0",
            "platforms": {
                "slack": {
                    "connected_at": "2026-02-04T10:00:00Z"
                }
            }
        }

        with pytest.raises(ConfigValidationError) as exc_info:
            config_manager._validate_schema(config)

        assert "missing required field: enabled" in str(exc_info.value)

    def test_validate_schema_platform_missing_connected_at(self, config_manager):
        """Test validating schema with platform missing connected_at field."""
        config = {
            "version": "1.0.0",
            "platforms": {
                "slack": {
                    "enabled": True
                }
            }
        }

        with pytest.raises(ConfigValidationError) as exc_info:
            config_manager._validate_schema(config)

        assert "missing required field: connected_at" in str(exc_info.value)

    def test_validate_schema_platform_enabled_not_boolean(self, config_manager):
        """Test validating schema with platform enabled not boolean."""
        config = {
            "version": "1.0.0",
            "platforms": {
                "slack": {
                    "enabled": "yes",  # Should be boolean
                    "connected_at": "2026-02-04T10:00:00Z"
                }
            }
        }

        with pytest.raises(ConfigValidationError) as exc_info:
            config_manager._validate_schema(config)

        assert "field 'enabled' must be boolean" in str(exc_info.value)

    def test_validate_schema_platform_not_object(self, config_manager):
        """Test validating schema with platform not object."""
        config = {
            "version": "1.0.0",
            "platforms": {
                "slack": "invalid"  # Should be object
            }
        }

        with pytest.raises(ConfigValidationError) as exc_info:
            config_manager._validate_schema(config)

        assert "config must be an object" in str(exc_info.value)

    def test_generate_encryption_key(self, config_manager):
        """Test generating encryption key."""
        key = config_manager.generate_encryption_key()

        assert len(key) > 0
        assert isinstance(key, str)

        # Key should be valid Fernet key
        Fernet(key.encode())  # Should not raise exception

    def test_update_platform_config_success(self, config_manager, config_path, valid_config):
        """Test updating platform configuration successfully."""
        # Save initial config
        with open(config_path, 'w') as f:
            json.dump(valid_config, f)

        # Update platform
        updates = {
            "enabled": False,
            "bot_token": "new-token"
        }

        config_manager.update_platform_config("slack", updates)

        # Load and verify
        config = config_manager.load_config()
        assert config["platforms"]["slack"]["enabled"] is False
        assert config["platforms"]["slack"]["bot_token"] == "new-token"

    def test_update_platform_config_not_found(self, config_manager, config_path, valid_config):
        """Test updating non-existent platform configuration."""
        # Save initial config
        with open(config_path, 'w') as f:
            json.dump(valid_config, f)

        with pytest.raises(ConfigValidationError) as exc_info:
            config_manager.update_platform_config("nonexistent", {"enabled": False})

        assert "Platform 'nonexistent' not found" in str(exc_info.value)

    def test_remove_platform_config_success(self, config_manager, config_path, valid_config):
        """Test removing platform configuration successfully."""
        # Save initial config
        with open(config_path, 'w') as f:
            json.dump(valid_config, f)

        config_manager.remove_platform_config("slack")

        # Load and verify
        config = config_manager.load_config()
        assert "slack" not in config["platforms"]
        assert "github" in config["platforms"]

    def test_remove_platform_config_not_found(self, config_manager, config_path, valid_config):
        """Test removing non-existent platform configuration."""
        # Save initial config
        with open(config_path, 'w') as f:
            json.dump(valid_config, f)

        with pytest.raises(ConfigValidationError) as exc_info:
            config_manager.remove_platform_config("nonexistent")

        assert "Platform 'nonexistent' not found" in str(exc_info.value)
