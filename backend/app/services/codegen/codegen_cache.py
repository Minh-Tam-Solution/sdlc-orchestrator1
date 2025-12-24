"""
Codegen Cache Service - Sprint 48.

Caching layer for AI code generation to reduce latency and costs.
Uses Redis for distributed caching with content-based keys.

SDLC Stage: 04 - BUILD
Sprint: 48 - Quality Gates + Ollama Optimization + MVP Hardening
Framework: SDLC 5.1.1
Epic: EP-06 IR-Based Vietnamese SME Codegen

Features:
- Blueprint-based cache keys (hash of normalized IR)
- Configurable TTL per generation type
- Automatic cache invalidation
- Cache hit/miss metrics
- Memory-efficient storage (compressed)

Target: <3s generation latency (p95) with caching

Author: Backend Lead
Date: December 23, 2025
Status: ACTIVE
"""

import gzip
import hashlib
import json
import logging
import time
from typing import Any, Dict, Optional, Tuple

from app.services.cache_service import (
    CacheService,
    cache_service,
    CACHE_TTL_LONG,
)
from .base_provider import CodegenSpec, CodegenResult

logger = logging.getLogger(__name__)

# Cache configuration
CODEGEN_CACHE_PREFIX = "codegen"
CODEGEN_CACHE_TTL = 3600  # 1 hour default for generated code
CODEGEN_CACHE_TTL_MODULES = 1800  # 30 minutes for single module generation
CODEGEN_CACHE_MAX_SIZE = 500_000  # Max 500KB per cached item

# Metrics tracking
_cache_stats = {
    "hits": 0,
    "misses": 0,
    "errors": 0,
    "bytes_saved": 0,
}


class CodegenCacheService:
    """
    Caching service for code generation results.

    Uses content-based hashing for cache keys:
    - Hash of normalized blueprint JSON
    - Language and framework in key
    - Target module (if specified)

    Cache entries include:
    - Generated code files
    - Token usage metadata
    - Generation time (for comparison)

    Usage:
        cache = CodegenCacheService()
        result = await cache.get(spec)
        if result:
            return result  # Cache hit

        # Generate code
        result = await provider.generate(spec)

        # Cache for next time
        await cache.set(spec, result)
    """

    def __init__(
        self,
        ttl: int = CODEGEN_CACHE_TTL,
        enabled: bool = True,
        compress: bool = True,
    ):
        """
        Initialize codegen cache service.

        Args:
            ttl: Default time-to-live in seconds
            enabled: Whether caching is enabled
            compress: Whether to compress cached content
        """
        self.ttl = ttl
        self.enabled = enabled
        self.compress = compress
        self._cache = cache_service

    def _make_cache_key(self, spec: CodegenSpec) -> str:
        """
        Generate cache key from CodegenSpec.

        Key format: codegen:{language}:{framework}:{module}:{blueprint_hash}

        Args:
            spec: CodegenSpec for generation

        Returns:
            Cache key string
        """
        # Normalize and hash blueprint
        blueprint_str = json.dumps(
            spec.app_blueprint,
            sort_keys=True,
            ensure_ascii=False,
        )
        blueprint_hash = hashlib.sha256(blueprint_str.encode()).hexdigest()[:16]

        # Build key parts
        parts = [
            CODEGEN_CACHE_PREFIX,
            spec.language.lower(),
            spec.framework.lower(),
            spec.target_module or "full",
            blueprint_hash,
        ]

        return ":".join(parts)

    def _serialize_result(self, result: CodegenResult) -> bytes:
        """
        Serialize CodegenResult for caching.

        Args:
            result: CodegenResult to serialize

        Returns:
            Serialized bytes (optionally compressed)
        """
        data = {
            "code": result.code,
            "files": result.files,
            "metadata": result.metadata,
            "provider": result.provider,
            "tokens_used": result.tokens_used,
            "generation_time_ms": result.generation_time_ms,
            "cached_at": time.time(),
        }

        json_str = json.dumps(data, ensure_ascii=False)
        json_bytes = json_str.encode("utf-8")

        if self.compress:
            return gzip.compress(json_bytes)
        return json_bytes

    def _deserialize_result(self, data: bytes) -> Optional[CodegenResult]:
        """
        Deserialize cached data to CodegenResult.

        Args:
            data: Cached bytes

        Returns:
            CodegenResult or None if deserialization fails
        """
        try:
            # Decompress if needed
            if self.compress:
                json_bytes = gzip.decompress(data)
            else:
                json_bytes = data

            json_str = json_bytes.decode("utf-8")
            cached = json.loads(json_str)

            # Reconstruct CodegenResult
            result = CodegenResult(
                code=cached["code"],
                files=cached["files"],
                metadata={
                    **cached.get("metadata", {}),
                    "from_cache": True,
                    "cached_at": cached.get("cached_at"),
                    "original_generation_time_ms": cached.get("generation_time_ms"),
                },
                provider=cached["provider"],
                tokens_used=cached.get("tokens_used", 0),
                generation_time_ms=0,  # Will be set to cache retrieval time
            )

            return result

        except Exception as e:
            logger.warning(f"Failed to deserialize cached result: {e}")
            return None

    async def get(self, spec: CodegenSpec) -> Optional[CodegenResult]:
        """
        Get cached generation result.

        Args:
            spec: CodegenSpec to look up

        Returns:
            Cached CodegenResult or None if not found
        """
        if not self.enabled:
            return None

        start_time = time.time()
        cache_key = self._make_cache_key(spec)

        try:
            # Get from cache
            cached_data = await self._cache.get(cache_key)

            if cached_data is None:
                _cache_stats["misses"] += 1
                logger.debug(f"Codegen cache MISS: {cache_key}")
                return None

            # Handle both string and bytes data
            if isinstance(cached_data, str):
                # Data was stored as string (base64 or JSON)
                if cached_data.startswith("gzip:"):
                    # Compressed data stored as base64
                    import base64
                    data_bytes = base64.b64decode(cached_data[5:])
                else:
                    # Try to parse as JSON directly
                    data_bytes = cached_data.encode("utf-8")
            else:
                data_bytes = cached_data

            result = self._deserialize_result(data_bytes)

            if result:
                # Update metrics
                retrieval_time_ms = int((time.time() - start_time) * 1000)
                result.generation_time_ms = retrieval_time_ms

                _cache_stats["hits"] += 1
                _cache_stats["bytes_saved"] += len(data_bytes)

                logger.info(
                    f"Codegen cache HIT: {cache_key} "
                    f"({len(result.files)} files, {retrieval_time_ms}ms)"
                )

                return result

            return None

        except Exception as e:
            _cache_stats["errors"] += 1
            logger.warning(f"Codegen cache get error: {e}")
            return None

    async def set(
        self,
        spec: CodegenSpec,
        result: CodegenResult,
        ttl: Optional[int] = None,
    ) -> bool:
        """
        Cache generation result.

        Args:
            spec: CodegenSpec used for generation
            result: CodegenResult to cache
            ttl: Optional TTL override

        Returns:
            True if cached successfully
        """
        if not self.enabled:
            return False

        cache_key = self._make_cache_key(spec)

        try:
            # Serialize result
            data_bytes = self._serialize_result(result)

            # Check size limit
            if len(data_bytes) > CODEGEN_CACHE_MAX_SIZE:
                logger.warning(
                    f"Codegen result too large to cache: {len(data_bytes)} bytes "
                    f"(max: {CODEGEN_CACHE_MAX_SIZE})"
                )
                return False

            # Store as base64 string for JSON compatibility
            import base64
            data_str = "gzip:" + base64.b64encode(data_bytes).decode("ascii")

            # Determine TTL
            cache_ttl = ttl or (
                CODEGEN_CACHE_TTL_MODULES if spec.target_module
                else self.ttl
            )

            # Set in cache
            success = await self._cache.set(cache_key, data_str, cache_ttl)

            if success:
                logger.info(
                    f"Codegen cache SET: {cache_key} "
                    f"({len(data_bytes)} bytes, TTL: {cache_ttl}s)"
                )

            return success

        except Exception as e:
            _cache_stats["errors"] += 1
            logger.warning(f"Codegen cache set error: {e}")
            return False

    async def invalidate(self, spec: CodegenSpec) -> bool:
        """
        Invalidate cached result for a spec.

        Args:
            spec: CodegenSpec to invalidate

        Returns:
            True if deleted
        """
        cache_key = self._make_cache_key(spec)
        return await self._cache.delete(cache_key)

    async def invalidate_blueprint(self, blueprint_name: str) -> int:
        """
        Invalidate all caches for a blueprint.

        Args:
            blueprint_name: App blueprint name

        Returns:
            Number of keys deleted
        """
        pattern = f"{CODEGEN_CACHE_PREFIX}:*"
        return await self._cache.invalidate_pattern(pattern)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dict with hit/miss counts and hit rate
        """
        total = _cache_stats["hits"] + _cache_stats["misses"]
        hit_rate = (_cache_stats["hits"] / total * 100) if total > 0 else 0

        return {
            "hits": _cache_stats["hits"],
            "misses": _cache_stats["misses"],
            "errors": _cache_stats["errors"],
            "total_requests": total,
            "hit_rate_percent": round(hit_rate, 2),
            "bytes_saved": _cache_stats["bytes_saved"],
        }

    def reset_stats(self) -> None:
        """Reset cache statistics."""
        global _cache_stats
        _cache_stats = {
            "hits": 0,
            "misses": 0,
            "errors": 0,
            "bytes_saved": 0,
        }


# Global cache instance
codegen_cache = CodegenCacheService()


def get_codegen_cache() -> CodegenCacheService:
    """Get the global codegen cache instance."""
    return codegen_cache
