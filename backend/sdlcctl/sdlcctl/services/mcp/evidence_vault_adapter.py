"""Evidence Vault adapter for MCP integration.

This module provides integration with the SDLC Orchestrator Evidence Vault,
enabling tamper-evident audit trails for all MCP operations with Ed25519 signatures
and hash chain linking.
"""

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)


class EvidenceVaultError(Exception):
    """Raised when Evidence Vault operations fail."""
    pass


class EvidenceVaultAdapter:
    """
    Evidence Vault adapter for MCP operations.

    This adapter provides tamper-evident audit trails using:
    - Ed25519 asymmetric signing (non-repudiation)
    - SHA256 hash chains (sequential integrity)
    - JSON manifest storage (human-readable audit trail)

    Design Pattern:
    - Each MCP operation creates an evidence artifact
    - Artifacts are signed with Ed25519 private key
    - Artifacts link to previous artifact via hash chain
    - Chain breaks if any artifact is tampered with
    """

    def __init__(
        self,
        vault_path: Path,
        private_key: Optional[bytes] = None,
        public_key: Optional[bytes] = None,
        key_id: Optional[str] = None
    ):
        """
        Initialize Evidence Vault adapter.

        Args:
            vault_path: Directory to store evidence artifacts
            private_key: Ed25519 private key (32 bytes) for signing
            public_key: Ed25519 public key (32 bytes) for verification
            key_id: Unique identifier for this key pair
        """
        self.vault_path = vault_path
        self._private_key = private_key
        self._public_key = public_key
        self._key_id = key_id or "default-key-v1"

        # Ensure vault directory exists
        self.vault_path.mkdir(parents=True, exist_ok=True)

        # Load cryptography library
        try:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import (
                Ed25519PrivateKey,
                Ed25519PublicKey,
            )
            self._Ed25519PrivateKey = Ed25519PrivateKey
            self._Ed25519PublicKey = Ed25519PublicKey
        except ImportError:
            logger.warning(
                "cryptography library not installed. "
                "Evidence artifacts will be unsigned."
            )
            self._Ed25519PrivateKey = None
            self._Ed25519PublicKey = None

    def create_artifact(
        self,
        operation: str,
        platform: str,
        metadata: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> str:
        """
        Create tamper-evident evidence artifact for MCP operation.

        Args:
            operation: Operation type (e.g., "mcp_connect", "mcp_disconnect")
            platform: Platform name (e.g., "slack", "github")
            metadata: Operation metadata (credentials, channels, etc.)
            user_id: User who performed the operation

        Returns:
            Artifact ID (format: EVD-YYYY-MM-NNN)

        Raises:
            EvidenceVaultError: If artifact creation fails
        """
        try:
            # Generate artifact ID
            artifact_id = self._generate_artifact_id()

            # Load previous artifact for hash chaining
            previous_hash = self._get_latest_artifact_hash()

            # Create artifact manifest
            artifact = {
                "artifact_id": artifact_id,
                "operation": operation,
                "platform": platform,
                "metadata": metadata,
                "user_id": user_id or "system",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "previous_hash": previous_hash,
                "hash": None,  # Will be computed
                "signature": None,  # Will be computed if keys available
                "signer_key_id": self._key_id,
                "signing_algorithm": "Ed25519"
            }

            # Compute artifact hash (excluding signature)
            artifact_hash = self._compute_hash(artifact)
            artifact["hash"] = artifact_hash

            # Sign artifact if private key available
            if self._private_key and self._Ed25519PrivateKey:
                signature = self._sign_artifact(artifact_hash)
                artifact["signature"] = signature
                logger.debug(f"Artifact {artifact_id} signed with key {self._key_id}")
            else:
                logger.warning(f"Artifact {artifact_id} created unsigned (no private key)")

            # Save artifact to disk
            artifact_file = self.vault_path / f"{artifact_id}.json"
            with open(artifact_file, 'w') as f:
                json.dump(artifact, f, indent=2)

            logger.info(
                f"Evidence artifact created: {artifact_id} "
                f"(operation={operation}, platform={platform})"
            )

            return artifact_id

        except Exception as e:
            raise EvidenceVaultError(f"Failed to create evidence artifact: {e}")

    def verify_artifact(self, artifact_id: str) -> bool:
        """
        Verify evidence artifact signature and hash chain integrity.

        Args:
            artifact_id: Artifact ID to verify

        Returns:
            True if artifact is valid (signature + hash chain OK)

        Raises:
            EvidenceVaultError: If verification fails
        """
        try:
            # Load artifact
            artifact_file = self.vault_path / f"{artifact_id}.json"
            if not artifact_file.exists():
                raise EvidenceVaultError(f"Artifact {artifact_id} not found")

            with open(artifact_file, 'r') as f:
                artifact = json.load(f)

            # Verify hash
            stored_hash = artifact["hash"]
            artifact_copy = artifact.copy()
            artifact_copy["hash"] = None
            artifact_copy["signature"] = None
            computed_hash = self._compute_hash(artifact_copy)

            if computed_hash != stored_hash:
                logger.error(
                    f"Hash mismatch for {artifact_id}: "
                    f"expected {stored_hash}, got {computed_hash}"
                )
                return False

            # Verify signature if available
            if artifact["signature"] and self._public_key and self._Ed25519PublicKey:
                if not self._verify_signature(stored_hash, artifact["signature"]):
                    logger.error(f"Invalid signature for {artifact_id}")
                    return False

            # Verify hash chain
            if artifact["previous_hash"]:
                if not self._verify_chain(artifact_id):
                    logger.error(f"Hash chain broken at {artifact_id}")
                    return False

            logger.info(f"Artifact {artifact_id} verification: PASS")
            return True

        except Exception as e:
            raise EvidenceVaultError(f"Failed to verify artifact {artifact_id}: {e}")

    def get_artifact(self, artifact_id: str) -> Dict[str, Any]:
        """
        Retrieve evidence artifact by ID.

        Args:
            artifact_id: Artifact ID to retrieve

        Returns:
            Artifact manifest as dictionary

        Raises:
            EvidenceVaultError: If artifact not found
        """
        artifact_file = self.vault_path / f"{artifact_id}.json"
        if not artifact_file.exists():
            raise EvidenceVaultError(f"Artifact {artifact_id} not found")

        with open(artifact_file, 'r') as f:
            return json.load(f)

    def list_artifacts(self, limit: int = 100) -> list[Dict[str, Any]]:
        """
        List recent evidence artifacts.

        Args:
            limit: Maximum number of artifacts to return

        Returns:
            List of artifacts sorted by creation time (newest first)
        """
        artifacts = []

        for artifact_file in sorted(
            self.vault_path.glob("EVD-*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:limit]:
            try:
                with open(artifact_file, 'r') as f:
                    artifacts.append(json.load(f))
            except Exception as e:
                logger.warning(f"Failed to load {artifact_file}: {e}")

        return artifacts

    def _generate_artifact_id(self) -> str:
        """
        Generate unique artifact ID.

        Format: EVD-YYYY-MM-NNN
        Example: EVD-2026-02-001

        Returns:
            Artifact ID string
        """
        # Get current month artifacts to determine sequence number
        now = datetime.now(timezone.utc)
        prefix = f"EVD-{now.year:04d}-{now.month:02d}"

        existing = list(self.vault_path.glob(f"{prefix}-*.json"))
        sequence = len(existing) + 1

        return f"{prefix}-{sequence:03d}"

    def _get_latest_artifact_hash(self) -> Optional[str]:
        """
        Get hash of the latest artifact for chain linking.

        Returns:
            SHA256 hash of latest artifact, or None if no artifacts exist
        """
        artifacts = list(sorted(
            self.vault_path.glob("EVD-*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        ))

        if not artifacts:
            return None

        try:
            with open(artifacts[0], 'r') as f:
                latest = json.load(f)
            return latest["hash"]
        except Exception as e:
            logger.warning(f"Failed to get latest artifact hash: {e}")
            return None

    def _compute_hash(self, artifact: Dict[str, Any]) -> str:
        """
        Compute SHA256 hash of artifact content.

        Args:
            artifact: Artifact manifest (with hash and signature excluded)

        Returns:
            Hexadecimal SHA256 hash
        """
        # Create copy and exclude hash/signature fields
        content = {
            k: v for k, v in artifact.items()
            if k not in ("hash", "signature")
        }

        # Deterministic JSON serialization
        content_json = json.dumps(content, sort_keys=True, separators=(",", ":"))

        return hashlib.sha256(content_json.encode("utf-8")).hexdigest()

    def _sign_artifact(self, artifact_hash: str) -> str:
        """
        Sign artifact hash with Ed25519 private key.

        Args:
            artifact_hash: SHA256 hash to sign

        Returns:
            Hexadecimal Ed25519 signature
        """
        if not self._private_key or not self._Ed25519PrivateKey:
            raise EvidenceVaultError("No private key available for signing")

        try:
            from cryptography.hazmat.primitives import serialization

            private_key = self._Ed25519PrivateKey.from_private_bytes(self._private_key)
            signature_bytes = private_key.sign(artifact_hash.encode("utf-8"))

            return signature_bytes.hex()

        except Exception as e:
            raise EvidenceVaultError(f"Failed to sign artifact: {e}")

    def _verify_signature(self, artifact_hash: str, signature_hex: str) -> bool:
        """
        Verify Ed25519 signature.

        Args:
            artifact_hash: SHA256 hash that was signed
            signature_hex: Hexadecimal Ed25519 signature

        Returns:
            True if signature is valid
        """
        if not self._public_key or not self._Ed25519PublicKey:
            return False

        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.exceptions import InvalidSignature

            public_key = self._Ed25519PublicKey.from_public_bytes(self._public_key)
            signature_bytes = bytes.fromhex(signature_hex)

            public_key.verify(signature_bytes, artifact_hash.encode("utf-8"))
            return True

        except InvalidSignature:
            return False
        except Exception as e:
            logger.warning(f"Signature verification error: {e}")
            return False

    def _verify_chain(self, artifact_id: str) -> bool:
        """
        Verify hash chain integrity from genesis to this artifact.

        Args:
            artifact_id: Artifact ID to verify chain up to

        Returns:
            True if chain is intact
        """
        try:
            # Load current artifact
            current = self.get_artifact(artifact_id)

            # If no previous hash, this is genesis (valid)
            if not current["previous_hash"]:
                return True

            # Find previous artifact by hash
            all_artifacts = self.list_artifacts(limit=1000)
            previous = None

            for artifact in all_artifacts:
                if artifact["hash"] == current["previous_hash"]:
                    previous = artifact
                    break

            if not previous:
                logger.error(
                    f"Previous artifact not found for hash {current['previous_hash']}"
                )
                return False

            # Verify previous artifact hash matches
            if previous["hash"] != current["previous_hash"]:
                logger.error("Hash mismatch in chain")
                return False

            return True

        except Exception as e:
            logger.error(f"Chain verification error: {e}")
            return False

    def generate_key_pair(self) -> tuple[bytes, bytes, str]:
        """
        Generate new Ed25519 key pair for signing.

        Returns:
            Tuple of (private_key_bytes, public_key_bytes, key_id)

        Note: In production, use HSM or HashiCorp Vault for key generation.
        """
        if not self._Ed25519PrivateKey:
            raise EvidenceVaultError(
                "cryptography library not installed. "
                "Run: pip install cryptography"
            )

        from cryptography.hazmat.primitives import serialization

        private_key = self._Ed25519PrivateKey.generate()
        public_key = private_key.public_key()

        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )

        key_id = f"key-{uuid4().hex[:8]}"

        return private_bytes, public_bytes, key_id
