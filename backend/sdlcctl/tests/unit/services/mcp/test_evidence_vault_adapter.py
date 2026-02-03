"""Unit tests for Evidence Vault adapter."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from sdlcctl.services.mcp.evidence_vault_adapter import (
    EvidenceVaultAdapter,
    EvidenceVaultError,
)


@pytest.fixture
def vault_path(tmp_path):
    """Create temporary vault path."""
    return tmp_path / "evidence_vault"


@pytest.fixture
def evidence_vault(vault_path):
    """Create EvidenceVaultAdapter instance for testing."""
    return EvidenceVaultAdapter(vault_path=vault_path)


@pytest.fixture
def signed_vault(vault_path):
    """Create EvidenceVaultAdapter with Ed25519 keys."""
    vault = EvidenceVaultAdapter(vault_path=vault_path)
    private_key, public_key, key_id = vault.generate_key_pair()
    return EvidenceVaultAdapter(
        vault_path=vault_path,
        private_key=private_key,
        public_key=public_key,
        key_id=key_id
    )


class TestEvidenceVaultAdapter:
    """Tests for EvidenceVaultAdapter class."""

    def test_init(self, vault_path):
        """Test EvidenceVaultAdapter initialization."""
        vault = EvidenceVaultAdapter(vault_path=vault_path)

        assert vault.vault_path == vault_path
        assert vault.vault_path.exists()
        assert vault._private_key is None
        assert vault._public_key is None

    def test_init_with_keys(self, vault_path):
        """Test EvidenceVaultAdapter initialization with keys."""
        private_key = b"0" * 32
        public_key = b"1" * 32
        key_id = "test-key"

        vault = EvidenceVaultAdapter(
            vault_path=vault_path,
            private_key=private_key,
            public_key=public_key,
            key_id=key_id
        )

        assert vault._private_key == private_key
        assert vault._public_key == public_key
        assert vault._key_id == key_id

    def test_create_artifact_unsigned(self, evidence_vault):
        """Test creating unsigned evidence artifact."""
        artifact_id = evidence_vault.create_artifact(
            operation="mcp_connect",
            platform="slack",
            metadata={"channel": "bugs", "bot_token": "xoxb-***"}
        )

        # Verify artifact ID format
        assert artifact_id.startswith("EVD-")
        assert len(artifact_id) == 15  # EVD-YYYY-MM-NNN

        # Verify artifact file exists
        artifact_file = evidence_vault.vault_path / f"{artifact_id}.json"
        assert artifact_file.exists()

        # Verify artifact content
        with open(artifact_file, 'r') as f:
            artifact = json.load(f)

        assert artifact["artifact_id"] == artifact_id
        assert artifact["operation"] == "mcp_connect"
        assert artifact["platform"] == "slack"
        assert artifact["metadata"]["channel"] == "bugs"
        assert artifact["hash"] is not None
        assert artifact["signature"] is None  # Unsigned
        assert artifact["previous_hash"] is None  # First artifact

    def test_create_artifact_signed(self, signed_vault):
        """Test creating signed evidence artifact."""
        artifact_id = signed_vault.create_artifact(
            operation="mcp_connect",
            platform="github",
            metadata={"app_id": "123456", "repo": "nqh/sdlc-orchestrator"},
            user_id="nqh"
        )

        # Verify artifact exists
        artifact_file = signed_vault.vault_path / f"{artifact_id}.json"
        assert artifact_file.exists()

        # Verify artifact content
        with open(artifact_file, 'r') as f:
            artifact = json.load(f)

        assert artifact["artifact_id"] == artifact_id
        assert artifact["signature"] is not None  # Signed!
        assert len(artifact["signature"]) == 128  # 64 bytes hex = 128 chars
        assert artifact["signer_key_id"] is not None
        assert artifact["user_id"] == "nqh"

    def test_create_artifact_hash_chain(self, signed_vault):
        """Test hash chain linking between artifacts."""
        # Create first artifact
        artifact_id_1 = signed_vault.create_artifact(
            operation="mcp_connect",
            platform="slack",
            metadata={"channel": "bugs"}
        )

        # Create second artifact
        artifact_id_2 = signed_vault.create_artifact(
            operation="mcp_disconnect",
            platform="slack",
            metadata={"channel": "bugs"}
        )

        # Verify first artifact has no previous hash
        artifact_1 = signed_vault.get_artifact(artifact_id_1)
        assert artifact_1["previous_hash"] is None

        # Verify second artifact links to first
        artifact_2 = signed_vault.get_artifact(artifact_id_2)
        assert artifact_2["previous_hash"] == artifact_1["hash"]

    def test_verify_artifact_unsigned(self, evidence_vault):
        """Test verifying unsigned artifact."""
        artifact_id = evidence_vault.create_artifact(
            operation="mcp_test",
            platform="slack",
            metadata={"result": "success"}
        )

        # Verification should pass (hash integrity checked)
        assert evidence_vault.verify_artifact(artifact_id) is True

    def test_verify_artifact_signed(self, signed_vault):
        """Test verifying signed artifact."""
        artifact_id = signed_vault.create_artifact(
            operation="mcp_connect",
            platform="github",
            metadata={"app_id": "123456"}
        )

        # Verification should pass (signature + hash checked)
        assert signed_vault.verify_artifact(artifact_id) is True

    def test_verify_artifact_tampered_hash(self, signed_vault):
        """Test detecting tampered artifact (hash modified)."""
        artifact_id = signed_vault.create_artifact(
            operation="mcp_connect",
            platform="slack",
            metadata={"channel": "bugs"}
        )

        # Tamper with artifact hash
        artifact_file = signed_vault.vault_path / f"{artifact_id}.json"
        with open(artifact_file, 'r') as f:
            artifact = json.load(f)

        artifact["hash"] = "tampered_hash_value"

        with open(artifact_file, 'w') as f:
            json.dump(artifact, f)

        # Verification should fail
        assert signed_vault.verify_artifact(artifact_id) is False

    def test_verify_artifact_tampered_content(self, signed_vault):
        """Test detecting tampered artifact (content modified)."""
        artifact_id = signed_vault.create_artifact(
            operation="mcp_connect",
            platform="slack",
            metadata={"channel": "bugs"}
        )

        # Tamper with artifact content (without updating hash)
        artifact_file = signed_vault.vault_path / f"{artifact_id}.json"
        with open(artifact_file, 'r') as f:
            artifact = json.load(f)

        artifact["metadata"]["channel"] = "tampered"

        with open(artifact_file, 'w') as f:
            json.dump(artifact, f)

        # Verification should fail (hash mismatch)
        assert signed_vault.verify_artifact(artifact_id) is False

    def test_verify_artifact_not_found(self, evidence_vault):
        """Test verifying non-existent artifact."""
        with pytest.raises(EvidenceVaultError) as exc_info:
            evidence_vault.verify_artifact("EVD-2026-02-999")

        assert "not found" in str(exc_info.value)

    def test_get_artifact_success(self, evidence_vault):
        """Test retrieving artifact."""
        artifact_id = evidence_vault.create_artifact(
            operation="mcp_connect",
            platform="slack",
            metadata={"channel": "bugs"}
        )

        artifact = evidence_vault.get_artifact(artifact_id)

        assert artifact["artifact_id"] == artifact_id
        assert artifact["operation"] == "mcp_connect"
        assert artifact["platform"] == "slack"

    def test_get_artifact_not_found(self, evidence_vault):
        """Test retrieving non-existent artifact."""
        with pytest.raises(EvidenceVaultError) as exc_info:
            evidence_vault.get_artifact("EVD-2026-02-999")

        assert "not found" in str(exc_info.value)

    def test_list_artifacts(self, evidence_vault):
        """Test listing artifacts."""
        # Create multiple artifacts
        artifact_ids = []
        for i in range(5):
            artifact_id = evidence_vault.create_artifact(
                operation=f"mcp_test_{i}",
                platform="slack",
                metadata={"test": i}
            )
            artifact_ids.append(artifact_id)

        # List artifacts
        artifacts = evidence_vault.list_artifacts(limit=10)

        assert len(artifacts) == 5
        # Verify sorted by creation time (newest first)
        assert artifacts[0]["artifact_id"] == artifact_ids[-1]

    def test_list_artifacts_limit(self, evidence_vault):
        """Test listing artifacts with limit."""
        # Create 10 artifacts
        for i in range(10):
            evidence_vault.create_artifact(
                operation=f"mcp_test_{i}",
                platform="slack",
                metadata={"test": i}
            )

        # List with limit
        artifacts = evidence_vault.list_artifacts(limit=3)

        assert len(artifacts) == 3

    def test_generate_artifact_id(self, evidence_vault):
        """Test artifact ID generation."""
        # Create first artifact to establish sequence
        artifact_id_1 = evidence_vault.create_artifact(
            operation="test_1",
            platform="slack",
            metadata={}
        )

        artifact_id_2 = evidence_vault.create_artifact(
            operation="test_2",
            platform="slack",
            metadata={}
        )

        # Verify format
        assert artifact_id_1.startswith("EVD-")
        assert len(artifact_id_1) == 15

        # Verify uniqueness (sequential)
        assert artifact_id_1 != artifact_id_2
        # Second artifact should have incremented sequence number
        assert artifact_id_1[:-3] == artifact_id_2[:-3]  # Same YYYY-MM prefix

    def test_generate_key_pair(self, evidence_vault):
        """Test Ed25519 key pair generation."""
        private_key, public_key, key_id = evidence_vault.generate_key_pair()

        assert len(private_key) == 32  # Ed25519 private key is 32 bytes
        assert len(public_key) == 32  # Ed25519 public key is 32 bytes
        assert key_id.startswith("key-")

    def test_sign_and_verify(self, signed_vault):
        """Test Ed25519 signing and verification."""
        # Sign a message
        message_hash = "test_message_hash"
        signature = signed_vault._sign_artifact(message_hash)

        assert len(signature) == 128  # 64 bytes hex

        # Verify signature
        assert signed_vault._verify_signature(message_hash, signature) is True

        # Verify with wrong message
        assert signed_vault._verify_signature("wrong_hash", signature) is False

    def test_verify_chain_integrity(self, signed_vault):
        """Test hash chain verification."""
        # Create chain of 3 artifacts
        artifact_1 = signed_vault.create_artifact(
            operation="mcp_connect",
            platform="slack",
            metadata={"step": 1}
        )

        artifact_2 = signed_vault.create_artifact(
            operation="mcp_test",
            platform="slack",
            metadata={"step": 2}
        )

        artifact_3 = signed_vault.create_artifact(
            operation="mcp_disconnect",
            platform="slack",
            metadata={"step": 3}
        )

        # Verify chain integrity
        assert signed_vault._verify_chain(artifact_1) is True  # Genesis
        assert signed_vault._verify_chain(artifact_2) is True  # Links to 1
        assert signed_vault._verify_chain(artifact_3) is True  # Links to 2

    def test_verify_chain_broken(self, signed_vault):
        """Test detecting broken hash chain."""
        # Create chain
        artifact_1 = signed_vault.create_artifact(
            operation="mcp_connect",
            platform="slack",
            metadata={"step": 1}
        )

        artifact_2 = signed_vault.create_artifact(
            operation="mcp_test",
            platform="slack",
            metadata={"step": 2}
        )

        # Tamper with first artifact hash (break chain)
        artifact_1_file = signed_vault.vault_path / f"{artifact_1}.json"
        with open(artifact_1_file, 'r') as f:
            data = json.load(f)

        data["hash"] = "tampered_hash"

        with open(artifact_1_file, 'w') as f:
            json.dump(data, f)

        # Chain verification should fail for artifact 2
        assert signed_vault._verify_chain(artifact_2) is False
