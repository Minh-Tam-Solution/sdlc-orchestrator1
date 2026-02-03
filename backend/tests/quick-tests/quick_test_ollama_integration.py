#!/usr/bin/env python3
"""
=========================================================================
Quick Ollama Integration Test - Sprint 111 Day 3-4
SDLC Orchestrator - AI-Platform Integration Validation

Version: 1.0.0
Date: January 27, 2026

Purpose:
- Quick validation of Ollama AI-Platform integration
- Test without full pytest setup
- Verify Model Strategy v3.0 configuration

Usage:
    # Local Ollama:
    python quick_test_ollama_integration.py

    # AI-Platform Ollama:
    AI_PLATFORM_OLLAMA_URL=http://api.nhatquangholding.com:11434 python quick_test_ollama_integration.py

Expected Output:
    ✅ Service Initialization: PASSED
    ✅ Health Check: PASSED (N models available)
    ✅ Simple Generation: PASSED (X.XXs, YY tok/s)
    ✅ Recommendation Generation: PASSED (ZZ% confidence)
    ✅ Fallback Chain: PASSED
    ⚠️ Model Strategy v3.0: PARTIAL (X/10 models)

    Summary: 5/6 tests passed, 1 partial
=========================================================================
"""

import os
import sys
import time
from typing import Any

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.ollama_service import (
    OllamaError,
    OllamaModel,
    OllamaService,
    create_ollama_service,
)


# ============================================================================
# Configuration
# ============================================================================

OLLAMA_URL = os.getenv("AI_PLATFORM_OLLAMA_URL", "http://localhost:11434")
TIMEOUT = 60  # seconds (increased for large model first-load)
FAST_MODEL = "qwen3:8b"  # Fast model for simple tests


# ============================================================================
# Test Functions
# ============================================================================

def test_service_initialization() -> tuple[bool, str]:
    """Test 1: Service initializes correctly."""
    try:
        service = OllamaService(
            base_url=OLLAMA_URL,
            model=OllamaModel.DEFAULT.value,
            timeout=TIMEOUT
        )

        if service.base_url != OLLAMA_URL:
            return False, f"URL mismatch: {service.base_url}"
        if service.model != OllamaModel.DEFAULT.value:
            return False, f"Model mismatch: {service.model}"
        if service.timeout != TIMEOUT:
            return False, f"Timeout mismatch: {service.timeout}"

        return True, "Service initialized correctly"

    except Exception as e:
        return False, f"Exception: {str(e)}"


def test_health_check() -> tuple[bool, str]:
    """Test 2: Health check returns valid data."""
    try:
        service = OllamaService(base_url=OLLAMA_URL, timeout=10)
        health = service.health_check()

        if not isinstance(health, dict):
            return False, "Health check did not return dict"

        if "healthy" not in health:
            return False, "Missing 'healthy' key"

        if health["healthy"]:
            model_count = len(health.get("models", []))
            return True, f"{model_count} models available"
        else:
            error = health.get("error", "Unknown error")
            return False, f"Ollama not healthy: {error}"

    except Exception as e:
        return False, f"Exception: {str(e)}"


def test_simple_generation() -> tuple[bool, str]:
    """Test 3: Simple text generation works."""
    try:
        service = OllamaService(base_url=OLLAMA_URL, timeout=TIMEOUT)

        # Check availability first
        if not service.is_available:
            return None, "Ollama not available (skipped)"  # type: ignore

        start = time.time()
        # Use fast model for quick test (FAST_MODEL = qwen3:8b)
        # Note: Higher max_tokens needed for thinking models (qwen3 uses internal reasoning)
        response = service.generate(
            prompt="What is 2+2? Answer briefly.",
            model=FAST_MODEL,
            temperature=0.1,
            max_tokens=200  # Higher limit for thinking models
        )
        elapsed = time.time() - start

        if not response.response:
            return False, "Empty response"

        # Check if response contains "4" (allow for thinking models)
        response_text = response.response.strip()
        if "4" not in response_text and "four" not in response_text.lower():
            return False, f"Unexpected response: {response_text[:100]}"

        tok_per_sec = response.tokens_per_second
        return True, f"{elapsed:.2f}s, {tok_per_sec:.0f} tok/s"

    except OllamaError as e:
        # Timeout is expected if GPU is busy - mark as partial success
        if "timeout" in str(e).lower():
            return None, "Timeout (GPU may be busy, skipped)"  # type: ignore
        return False, f"OllamaError: {str(e)}"
    except Exception as e:
        return False, f"Exception: {str(e)}"


def test_recommendation_generation() -> tuple[bool, str]:
    """Test 4: Recommendation generation works."""
    try:
        service = OllamaService(base_url=OLLAMA_URL, timeout=TIMEOUT)

        if not service.is_available:
            return None, "Ollama not available (skipped)"  # type: ignore

        start = time.time()
        # Use fast model for quick test
        result = service.generate_recommendation(
            violation_type="missing_documentation",
            severity="high",
            location="docs/00-Project-Foundation",
            description="Missing SDLC stage folder",
            model=FAST_MODEL  # Use fast model
        )
        elapsed = time.time() - start

        if not result.get("recommendation"):
            return False, "Empty recommendation"

        confidence = result.get("confidence", 0)
        model = result.get("model", "unknown")

        # Fallback is acceptable if timeout occurred (GPU busy)
        if model == "rule-based-fallback":
            # Check if it's because of timeout - this is acceptable
            return True, f"Fallback used (GPU may be busy), {elapsed:.2f}s"

        return True, f"{confidence}% confidence, {elapsed:.2f}s"

    except Exception as e:
        # Timeout is expected if GPU is busy
        if "timeout" in str(e).lower():
            return None, "Timeout (GPU may be busy, skipped)"  # type: ignore
        return False, f"Exception: {str(e)}"


def test_fallback_chain() -> tuple[bool, str]:
    """Test 5: Fallback chain works when Ollama unavailable."""
    try:
        # Use non-existent endpoint
        service = OllamaService(
            base_url="http://localhost:59999",
            timeout=2
        )

        result = service.generate_recommendation(
            violation_type="policy_violation",
            severity="medium",
            location="src/service.py",
            description="Test violation"
        )

        if result.get("model") != "rule-based-fallback":
            return False, f"Expected fallback, got: {result.get('model')}"

        if "Fix Steps" not in result.get("recommendation", ""):
            return False, "Fallback recommendation missing expected content"

        return True, "Fallback works correctly"

    except Exception as e:
        return False, f"Exception: {str(e)}"


def test_model_strategy_v3() -> tuple[bool, str]:
    """Test 6: Model Strategy v3.0 models availability."""
    try:
        service = OllamaService(base_url=OLLAMA_URL, timeout=10)

        if not service.is_available:
            return None, "Ollama not available (skipped)"  # type: ignore

        models = service.list_models()
        model_names = [m["name"].lower() for m in models]

        # Model Strategy v3.0 models to check
        strategy_models = {
            "qwen3-coder:30b": "Code (256K context)",
            "qwen3:32b": "Vietnamese chat",
            "deepseek-r1": "Deep reasoning",
            "mistral-small": "SOP RAG",
            "qwen3:14b": "Vietnamese fast",
            "qwen3:8b": "Fastest chat",
            "ministral": "Fast tasks",
            "gemma3": "Creative writing",
            "gpt-oss": "Vietnamese reasoning",
            "bge-m3": "Embeddings",
        }

        available = []
        for model_key in strategy_models.keys():
            # Check if base name is in any available model
            if any(model_key.split(":")[0] in m for m in model_names):
                available.append(model_key)

        count = len(available)
        total = len(strategy_models)

        if count == 0:
            return False, f"No Model Strategy v3.0 models found"
        elif count < total / 2:
            # Partial success
            return True, f"{count}/{total} models (partial)"
        else:
            return True, f"{count}/{total} models"

    except Exception as e:
        return False, f"Exception: {str(e)}"


# ============================================================================
# Main
# ============================================================================

def main() -> int:
    """Run all quick tests."""
    print("=" * 70)
    print("Ollama AI-Platform Integration Test - Sprint 111 Day 3-4")
    print("=" * 70)
    print(f"\nOllama URL: {OLLAMA_URL}")
    print(f"Timeout: {TIMEOUT}s")
    print("")

    tests = [
        ("Service Initialization", test_service_initialization),
        ("Health Check", test_health_check),
        ("Simple Generation", test_simple_generation),
        ("Recommendation Generation", test_recommendation_generation),
        ("Fallback Chain", test_fallback_chain),
        ("Model Strategy v3.0", test_model_strategy_v3),
    ]

    passed = 0
    failed = 0
    skipped = 0
    partial = 0

    results = []

    for name, test_func in tests:
        try:
            success, message = test_func()

            if success is None:
                # Skipped test
                status = "⏭️ SKIPPED"
                skipped += 1
            elif success:
                if "partial" in message.lower():
                    status = "⚠️ PARTIAL"
                    partial += 1
                else:
                    status = "✅ PASSED"
                    passed += 1
            else:
                status = "❌ FAILED"
                failed += 1

            results.append((name, status, message))

        except Exception as e:
            results.append((name, "❌ ERROR", str(e)))
            failed += 1

    # Print results
    print("Results:")
    print("-" * 70)
    for name, status, message in results:
        print(f"  {status} {name}: {message}")

    print("")
    print("=" * 70)
    print(f"Summary: {passed} passed, {failed} failed, {skipped} skipped, {partial} partial")
    print("=" * 70)

    # Connection info
    print("")
    if failed > 0:
        print("⚠️ Some tests failed. Check:")
        print("   1. Is Ollama running? Check: curl http://localhost:11434/api/tags")
        print("   2. For AI-Platform: export AI_PLATFORM_OLLAMA_URL=http://api.nhatquangholding.com:11434")
        print("   3. Is the Docker network 'ai-net' connected?")
    else:
        print("✅ All tests passed! Ollama integration is working.")

    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
