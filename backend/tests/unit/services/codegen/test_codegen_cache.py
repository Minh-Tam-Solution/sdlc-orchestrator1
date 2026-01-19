"""
Tests for CodegenCacheService - Sprint 48.

Test coverage for AI code generation caching:
- Cache key generation
- Serialization/deserialization
- Cache hit/miss operations
- Statistics tracking
- Compression

SDLC Stage: 04 - BUILD
Sprint: 48 - Quality Gates + Ollama Optimization + MVP Hardening
Framework: SDLC 5.1.3

Author: Backend Lead
Date: December 23, 2025
"""

import base64
import gzip
import json
import hashlib
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.codegen.codegen_cache import (
    CodegenCacheService,
    CODEGEN_CACHE_PREFIX,
    CODEGEN_CACHE_TTL,
    CODEGEN_CACHE_TTL_MODULES,
    CODEGEN_CACHE_MAX_SIZE,
    codegen_cache,
    get_codegen_cache,
)
from app.services.codegen.base_provider import CodegenSpec, CodegenResult


class TestCodegenCacheService:
    """Test suite for CodegenCacheService."""

    @pytest.fixture
    def mock_cache(self):
        """Create mock cache service."""
        cache = AsyncMock()
        cache.get = AsyncMock(return_value=None)
        cache.set = AsyncMock(return_value=True)
        cache.delete = AsyncMock(return_value=True)
        cache.invalidate_pattern = AsyncMock(return_value=5)
        return cache

    @pytest.fixture
    def cache_service(self, mock_cache):
        """Create cache service with mock."""
        service = CodegenCacheService()
        service._cache = mock_cache
        return service

    @pytest.fixture
    def cache_service_disabled(self):
        """Create disabled cache service."""
        return CodegenCacheService(enabled=False)

    @pytest.fixture
    def cache_service_no_compress(self, mock_cache):
        """Create cache service without compression."""
        service = CodegenCacheService(compress=False)
        service._cache = mock_cache
        return service

    @pytest.fixture
    def sample_spec(self):
        """Create sample CodegenSpec."""
        return CodegenSpec(
            app_blueprint={
                "name": "TestApp",
                "version": "1.0.0",
                "modules": [
                    {
                        "name": "users",
                        "entities": [
                            {"name": "User", "fields": [{"name": "email"}]},
                        ],
                    }
                ],
            },
            language="python",
            framework="fastapi",
            target_module=None,
        )

    @pytest.fixture
    def sample_spec_module(self):
        """Create sample CodegenSpec for single module."""
        return CodegenSpec(
            app_blueprint={"name": "TestApp", "modules": []},
            language="python",
            framework="fastapi",
            target_module="users",
        )

    @pytest.fixture
    def sample_result(self):
        """Create sample CodegenResult."""
        return CodegenResult(
            code="# Generated code\nclass User: pass",
            files={
                "app/models/user.py": "from sqlalchemy import Column\n\nclass User: pass",
                "app/schemas/user.py": "from pydantic import BaseModel\n\nclass UserSchema(BaseModel): pass",
            },
            metadata={"prompt_tokens": 500, "completion_tokens": 1000},
            provider="ollama",
            tokens_used=1500,
            generation_time_ms=2000,
        )


class TestCacheKeyGeneration(TestCodegenCacheService):
    """Test cache key generation."""

    def test_make_cache_key_format(self, cache_service, sample_spec):
        """Test cache key has correct format."""
        key = cache_service._make_cache_key(sample_spec)

        # Format: codegen:{language}:{framework}:{module}:{blueprint_hash}
        parts = key.split(":")
        assert len(parts) == 5
        assert parts[0] == CODEGEN_CACHE_PREFIX
        assert parts[1] == "python"
        assert parts[2] == "fastapi"
        assert parts[3] == "full"  # No target module
        assert len(parts[4]) == 16  # SHA256 truncated to 16 chars

    def test_make_cache_key_with_module(self, cache_service, sample_spec_module):
        """Test cache key includes module name."""
        key = cache_service._make_cache_key(sample_spec_module)

        parts = key.split(":")
        assert parts[3] == "users"

    def test_make_cache_key_deterministic(self, cache_service, sample_spec):
        """Test same spec produces same key."""
        key1 = cache_service._make_cache_key(sample_spec)
        key2 = cache_service._make_cache_key(sample_spec)

        assert key1 == key2

    def test_make_cache_key_different_for_different_specs(self, cache_service):
        """Test different specs produce different keys."""
        spec1 = CodegenSpec(
            app_blueprint={"name": "App1"},
            language="python",
            framework="fastapi",
        )
        spec2 = CodegenSpec(
            app_blueprint={"name": "App2"},
            language="python",
            framework="fastapi",
        )

        key1 = cache_service._make_cache_key(spec1)
        key2 = cache_service._make_cache_key(spec2)

        assert key1 != key2

    def test_make_cache_key_normalized_json(self, cache_service):
        """Test blueprint is normalized (sorted keys) for consistent hashing."""
        spec1 = CodegenSpec(
            app_blueprint={"b": 2, "a": 1},
            language="python",
            framework="fastapi",
        )
        spec2 = CodegenSpec(
            app_blueprint={"a": 1, "b": 2},
            language="python",
            framework="fastapi",
        )

        key1 = cache_service._make_cache_key(spec1)
        key2 = cache_service._make_cache_key(spec2)

        # Should produce same key due to sorted JSON
        assert key1 == key2


class TestSerialization(TestCodegenCacheService):
    """Test result serialization/deserialization."""

    def test_serialize_result_compressed(self, cache_service, sample_result):
        """Test result serialization with compression."""
        data = cache_service._serialize_result(sample_result)

        # Should be gzip compressed bytes
        assert isinstance(data, bytes)
        # Verify it's compressed by decompressing
        decompressed = gzip.decompress(data)
        parsed = json.loads(decompressed.decode("utf-8"))

        assert parsed["code"] == sample_result.code
        assert parsed["files"] == sample_result.files
        assert parsed["provider"] == "ollama"

    def test_serialize_result_uncompressed(self, cache_service_no_compress, sample_result):
        """Test result serialization without compression."""
        data = cache_service_no_compress._serialize_result(sample_result)

        # Should be plain JSON bytes
        parsed = json.loads(data.decode("utf-8"))
        assert parsed["code"] == sample_result.code

    def test_deserialize_result_compressed(self, cache_service, sample_result):
        """Test result deserialization from compressed data."""
        # First serialize
        data = cache_service._serialize_result(sample_result)

        # Then deserialize
        result = cache_service._deserialize_result(data)

        assert result is not None
        assert result.code == sample_result.code
        assert result.files == sample_result.files
        assert result.provider == sample_result.provider
        assert result.metadata.get("from_cache") is True

    def test_deserialize_result_uncompressed(self, cache_service_no_compress, sample_result):
        """Test result deserialization from uncompressed data."""
        data = cache_service_no_compress._serialize_result(sample_result)
        result = cache_service_no_compress._deserialize_result(data)

        assert result is not None
        assert result.code == sample_result.code

    def test_deserialize_invalid_data_returns_none(self, cache_service):
        """Test deserialization of invalid data returns None."""
        result = cache_service._deserialize_result(b"invalid data")
        assert result is None

    def test_deserialize_corrupted_json_returns_none(self, cache_service):
        """Test deserialization of corrupted JSON returns None."""
        # Create valid gzip but invalid JSON
        invalid_json = gzip.compress(b"not json")
        result = cache_service._deserialize_result(invalid_json)
        assert result is None


class TestCacheGet(TestCodegenCacheService):
    """Test cache get operation."""

    @pytest.mark.asyncio
    async def test_get_cache_miss(self, cache_service, mock_cache, sample_spec):
        """Test cache miss returns None."""
        mock_cache.get.return_value = None

        result = await cache_service.get(sample_spec)

        assert result is None
        mock_cache.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_cache_hit(self, cache_service, mock_cache, sample_spec, sample_result):
        """Test cache hit returns result."""
        # Serialize and prepare cached data
        serialized = cache_service._serialize_result(sample_result)
        cached_str = "gzip:" + base64.b64encode(serialized).decode("ascii")
        mock_cache.get.return_value = cached_str

        result = await cache_service.get(sample_spec)

        assert result is not None
        assert result.code == sample_result.code
        assert result.files == sample_result.files
        assert result.metadata.get("from_cache") is True

    @pytest.mark.asyncio
    async def test_get_disabled_returns_none(self, cache_service_disabled, sample_spec):
        """Test disabled cache always returns None."""
        result = await cache_service_disabled.get(sample_spec)
        assert result is None

    @pytest.mark.asyncio
    async def test_get_handles_error(self, cache_service, mock_cache, sample_spec):
        """Test get handles errors gracefully."""
        mock_cache.get.side_effect = Exception("Cache error")

        result = await cache_service.get(sample_spec)

        assert result is None  # Returns None on error


class TestCacheSet(TestCodegenCacheService):
    """Test cache set operation."""

    @pytest.mark.asyncio
    async def test_set_success(self, cache_service, mock_cache, sample_spec, sample_result):
        """Test successful cache set."""
        mock_cache.set.return_value = True

        success = await cache_service.set(sample_spec, sample_result)

        assert success is True
        mock_cache.set.assert_called_once()

        # Verify the stored data format
        call_args = mock_cache.set.call_args
        stored_data = call_args[0][1]  # Second positional arg
        assert stored_data.startswith("gzip:")

    @pytest.mark.asyncio
    async def test_set_disabled_returns_false(self, cache_service_disabled, sample_spec, sample_result):
        """Test disabled cache returns False."""
        success = await cache_service_disabled.set(sample_spec, sample_result)
        assert success is False

    @pytest.mark.asyncio
    async def test_set_with_custom_ttl(self, cache_service, mock_cache, sample_spec, sample_result):
        """Test cache set with custom TTL."""
        custom_ttl = 7200

        await cache_service.set(sample_spec, sample_result, ttl=custom_ttl)

        call_args = mock_cache.set.call_args
        assert call_args[0][2] == custom_ttl  # Third positional arg is TTL

    @pytest.mark.asyncio
    async def test_set_module_uses_shorter_ttl(self, cache_service, mock_cache, sample_spec_module, sample_result):
        """Test module generation uses shorter TTL."""
        await cache_service.set(sample_spec_module, sample_result)

        call_args = mock_cache.set.call_args
        assert call_args[0][2] == CODEGEN_CACHE_TTL_MODULES

    @pytest.mark.asyncio
    async def test_set_too_large_returns_false(self, cache_service_no_compress, mock_cache, sample_spec):
        """Test oversized result is not cached."""
        # Create a large result exceeding max size
        # Without compression, size is more predictable
        large_content = "x" * (CODEGEN_CACHE_MAX_SIZE + 1000)
        large_result = CodegenResult(
            code=large_content,
            files={"large.py": large_content},
            metadata={},
            provider="ollama",
            tokens_used=1000000,
            generation_time_ms=5000,
        )

        success = await cache_service_no_compress.set(sample_spec, large_result)

        assert success is False
        mock_cache.set.assert_not_called()

    @pytest.mark.asyncio
    async def test_set_handles_error(self, cache_service, mock_cache, sample_spec, sample_result):
        """Test set handles errors gracefully."""
        mock_cache.set.side_effect = Exception("Cache error")

        success = await cache_service.set(sample_spec, sample_result)

        assert success is False


class TestCacheInvalidation(TestCodegenCacheService):
    """Test cache invalidation."""

    @pytest.mark.asyncio
    async def test_invalidate_spec(self, cache_service, mock_cache, sample_spec):
        """Test invalidating specific spec."""
        mock_cache.delete.return_value = True

        result = await cache_service.invalidate(sample_spec)

        assert result is True
        mock_cache.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_invalidate_blueprint(self, cache_service, mock_cache):
        """Test invalidating all caches for a blueprint."""
        mock_cache.invalidate_pattern.return_value = 5

        count = await cache_service.invalidate_blueprint("TestApp")

        assert count == 5
        mock_cache.invalidate_pattern.assert_called_once()


class TestCacheStatistics(TestCodegenCacheService):
    """Test cache statistics tracking."""

    def test_get_stats_initial(self, cache_service):
        """Test initial stats are zero."""
        cache_service.reset_stats()
        stats = cache_service.get_stats()

        assert stats["hits"] == 0
        assert stats["misses"] == 0
        assert stats["errors"] == 0
        assert stats["total_requests"] == 0
        assert stats["hit_rate_percent"] == 0

    def test_get_stats_hit_rate_calculation(self, cache_service):
        """Test hit rate calculation."""
        # Manipulate module-level stats for testing
        from app.services.codegen import codegen_cache as cache_module

        original_stats = cache_module._cache_stats.copy()
        try:
            cache_module._cache_stats["hits"] = 8
            cache_module._cache_stats["misses"] = 2
            cache_module._cache_stats["errors"] = 0
            cache_module._cache_stats["bytes_saved"] = 10000

            stats = cache_service.get_stats()

            assert stats["hits"] == 8
            assert stats["misses"] == 2
            assert stats["total_requests"] == 10
            assert stats["hit_rate_percent"] == 80.0
        finally:
            cache_module._cache_stats = original_stats

    def test_reset_stats(self, cache_service):
        """Test resetting statistics."""
        cache_service.reset_stats()
        stats = cache_service.get_stats()

        assert stats["hits"] == 0
        assert stats["misses"] == 0


class TestGlobalCacheInstance:
    """Test global cache instance."""

    def test_codegen_cache_is_singleton(self):
        """Test codegen_cache is a singleton."""
        cache1 = get_codegen_cache()
        cache2 = get_codegen_cache()

        assert cache1 is cache2
        assert cache1 is codegen_cache

    def test_codegen_cache_default_config(self):
        """Test default cache configuration."""
        cache = get_codegen_cache()

        assert cache.enabled is True
        assert cache.compress is True
        assert cache.ttl == CODEGEN_CACHE_TTL


class TestCacheConfiguration:
    """Test cache configuration options."""

    def test_cache_ttl_constants(self):
        """Test TTL constants are reasonable."""
        assert CODEGEN_CACHE_TTL == 3600  # 1 hour
        assert CODEGEN_CACHE_TTL_MODULES == 1800  # 30 minutes
        assert CODEGEN_CACHE_MAX_SIZE == 500_000  # 500KB

    def test_cache_prefix(self):
        """Test cache prefix is correct."""
        assert CODEGEN_CACHE_PREFIX == "codegen"

    def test_custom_ttl_initialization(self):
        """Test custom TTL on initialization."""
        service = CodegenCacheService(ttl=7200)
        assert service.ttl == 7200

    def test_disabled_initialization(self):
        """Test disabled cache initialization."""
        service = CodegenCacheService(enabled=False)
        assert service.enabled is False

    def test_no_compression_initialization(self):
        """Test no compression initialization."""
        service = CodegenCacheService(compress=False)
        assert service.compress is False


class TestCacheIntegration(TestCodegenCacheService):
    """Integration-style tests for cache operations."""

    @pytest.mark.asyncio
    async def test_full_cache_cycle(self, cache_service, mock_cache, sample_spec, sample_result):
        """Test full cache cycle: set -> get -> invalidate."""
        # Set
        mock_cache.set.return_value = True
        set_result = await cache_service.set(sample_spec, sample_result)
        assert set_result is True

        # Prepare for get
        serialized = cache_service._serialize_result(sample_result)
        cached_str = "gzip:" + base64.b64encode(serialized).decode("ascii")
        mock_cache.get.return_value = cached_str

        # Get
        get_result = await cache_service.get(sample_spec)
        assert get_result is not None
        assert get_result.code == sample_result.code

        # Invalidate
        mock_cache.delete.return_value = True
        invalidate_result = await cache_service.invalidate(sample_spec)
        assert invalidate_result is True

        # Verify get returns None after invalidation
        mock_cache.get.return_value = None
        final_result = await cache_service.get(sample_spec)
        assert final_result is None
