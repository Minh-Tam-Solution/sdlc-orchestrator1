"""
Integration Tests Conftest - Sprint 111 Infrastructure Services

Minimal conftest for integration tests that doesn't load the full app.
These tests focus on external service integration (MinIO, Ollama, etc.)
"""

import os
import sys

import pytest

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def pytest_configure(config):
    """Configure pytest for integration tests."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )


@pytest.fixture(scope="session")
def integration_test_env():
    """Fixture to provide integration test environment info."""
    return {
        "ai_platform_ollama_url": os.getenv("AI_PLATFORM_OLLAMA_URL", "http://localhost:11434"),
        "ai_platform_minio_url": os.getenv("AI_PLATFORM_MINIO_URL", "http://localhost:9000"),
    }
