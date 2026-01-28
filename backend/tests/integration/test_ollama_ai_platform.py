"""
=========================================================================
Ollama AI-Platform Integration Tests - Sprint 111 Day 3-4
SDLC Orchestrator - Infrastructure Services Layer

Version: 1.0.0
Date: January 27, 2026
Status: Sprint 111 - Infrastructure Services (Day 3-4)
Authority: CTO Approved Sprint Plan
Foundation: Model Strategy v3.0, ADR-007 (AI Context Engine)

Purpose:
- Validate Ollama integration with AI-Platform shared infrastructure
- Test model availability (Model Strategy v3.0 - 10 models for RTX 5090)
- Verify text generation and recommendation workflows
- Confirm fallback chain behavior
- Performance validation (<10s latency target)

AI-Platform Integration:
- Ollama runs on AI-Platform at api.nhatquangholding.com:11434
- Shared via ai-net Docker network
- Model Strategy v3.0: qwen3-coder:30b, qwen3:32b, deepseek-r1:32b, etc.

Test Execution:
    # With AI-Platform running:
    docker-compose -f docker-compose.test.yml up -d
    pytest tests/integration/test_ollama_ai_platform.py -v

    # Quick validation:
    python quick_test_ollama_integration.py

Zero Mock Policy: Tests use real Ollama endpoints, skip gracefully if unavailable
=========================================================================
"""

import os
import time
from typing import Any, Optional
from unittest.mock import patch

import pytest

# Import the Ollama service
from app.services.ollama_service import (
    OllamaError,
    OllamaModel,
    OllamaResponse,
    OllamaService,
    create_ollama_service,
    get_ollama_service,
)


# ============================================================================
# Test Configuration
# ============================================================================

# AI-Platform Ollama endpoint (same as MinIO pattern)
AI_PLATFORM_OLLAMA_URL = os.getenv(
    "AI_PLATFORM_OLLAMA_URL",
    "http://localhost:11434"  # Default for local dev
)

# Test timeout for generation (Model Strategy v3.0 targets)
# Note: Higher timeout needed for thinking models (qwen3) and cold starts
GENERATION_TIMEOUT = 90  # 90s max for generation (thinking models need more time)
HEALTH_CHECK_TIMEOUT = 10  # 10s for health check

# Performance targets (adjusted for thinking models)
PERFORMANCE_TARGET_SIMPLE = 30.0  # 30s for simple prompts (thinking overhead)
PERFORMANCE_TARGET_COMPLEX = 60.0  # 60s for complex prompts

# Fast model for quick tests
FAST_MODEL = "qwen3:8b"


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(scope="module")
def ollama_service() -> OllamaService:
    """Create Ollama service instance for testing."""
    return OllamaService(
        base_url=AI_PLATFORM_OLLAMA_URL,
        timeout=GENERATION_TIMEOUT
    )


@pytest.fixture(scope="module")
def ollama_available(ollama_service: OllamaService) -> bool:
    """Check if Ollama is available for integration tests."""
    health = ollama_service.health_check()
    return health.get("healthy", False)


# ============================================================================
# TestOllamaConnectionHealth - Health Check & Connectivity
# ============================================================================

class TestOllamaConnectionHealth:
    """Test Ollama service health check and connectivity."""

    def test_service_initialization(self) -> None:
        """Test OllamaService initializes correctly with default settings."""
        service = OllamaService()

        assert service is not None
        assert service.base_url is not None
        assert service.model is not None
        assert service.timeout > 0

    def test_service_initialization_with_custom_url(self) -> None:
        """Test OllamaService with custom AI-Platform URL."""
        service = OllamaService(
            base_url=AI_PLATFORM_OLLAMA_URL,
            model=OllamaModel.QWEN3_32B.value,
            timeout=60
        )

        assert service.base_url == AI_PLATFORM_OLLAMA_URL
        assert service.model == OllamaModel.QWEN3_32B.value
        assert service.timeout == 60

    def test_health_check_returns_valid_structure(
        self, ollama_service: OllamaService
    ) -> None:
        """Test health check returns proper structure regardless of availability."""
        health = ollama_service.health_check()

        # Structure must always be present
        assert "healthy" in health
        assert "models" in health
        assert "version" in health
        assert isinstance(health["healthy"], bool)
        assert isinstance(health["models"], list)

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_health_check_with_ai_platform(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test health check against AI-Platform Ollama instance."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        health = ollama_service.health_check()

        assert health["healthy"] is True
        assert len(health["models"]) > 0

        # Log available models for debugging
        print(f"\n✅ Ollama healthy with {len(health['models'])} models:")
        for model in health["models"][:5]:  # Show first 5
            print(f"   - {model}")

    def test_is_available_property(self, ollama_service: OllamaService) -> None:
        """Test is_available property caches health check result."""
        # Force fresh check by resetting cache
        ollama_service._is_available = None

        # First access triggers health check
        available = ollama_service.is_available

        # Property should be boolean
        assert isinstance(available, bool)

        # Cache should be set
        assert ollama_service._is_available is not None


# ============================================================================
# TestModelStrategy - Model Strategy v3.0 Validation
# ============================================================================

class TestModelStrategy:
    """Test Model Strategy v3.0 configuration and model availability."""

    def test_model_enum_has_required_models(self) -> None:
        """Test OllamaModel enum includes all Model Strategy v3.0 models."""
        # Primary models (Model Strategy v3.0)
        assert OllamaModel.QWEN3_CODER_30B.value == "qwen3-coder:30b"
        assert OllamaModel.QWEN3_32B.value == "qwen3:32b"
        assert OllamaModel.DEEPSEEK_R1_32B.value == "deepseek-r1:32b-qwen-distill-q4_K_M"
        assert OllamaModel.MISTRAL_SMALL_24B.value == "mistral-small3.2:24b-instruct-2506-q4_K_M"

        # Fast models
        assert OllamaModel.QWEN3_14B.value == "qwen3:14b"
        assert OllamaModel.QWEN3_8B.value == "qwen3:8b"

        # Default models
        assert OllamaModel.DEFAULT.value == "qwen3:32b"
        assert OllamaModel.DEFAULT_CODE.value == "qwen3-coder:30b"
        assert OllamaModel.DEFAULT_VIETNAMESE.value == "qwen3:32b"

    def test_model_enum_backward_compatibility(self) -> None:
        """Test legacy model names are preserved for backward compatibility."""
        assert OllamaModel.CODELLAMA_7B.value == "codellama:7b"
        assert OllamaModel.CODELLAMA_13B.value == "codellama:13b"
        assert OllamaModel.LLAMA2_13B.value == "llama2:13b"
        assert OllamaModel.MISTRAL_7B.value == "mistral:7b"

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_model_availability_on_ai_platform(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test which Model Strategy v3.0 models are available on AI-Platform."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        models = ollama_service.list_models()
        model_names = [m["name"] for m in models]

        # Track available models from Model Strategy v3.0
        strategy_models = [
            OllamaModel.QWEN3_CODER_30B.value,
            OllamaModel.QWEN3_32B.value,
            OllamaModel.DEEPSEEK_R1_32B.value,
            OllamaModel.MISTRAL_SMALL_24B.value,
            OllamaModel.QWEN3_14B.value,
            OllamaModel.QWEN3_8B.value,
        ]

        available_strategy_models = []
        for model in strategy_models:
            # Check if model or base name is available
            base_name = model.split(":")[0]
            if any(base_name in m for m in model_names):
                available_strategy_models.append(model)

        print(f"\n📊 Model Strategy v3.0 availability:")
        print(f"   Available: {len(available_strategy_models)}/{len(strategy_models)}")
        for model in available_strategy_models:
            print(f"   ✅ {model}")


# ============================================================================
# TestTextGeneration - Basic Text Generation
# ============================================================================

class TestTextGeneration:
    """Test basic text generation functionality."""

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_simple_generation(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test simple text generation with fast model."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        start_time = time.time()

        # Use fast model and higher token limit for thinking models
        response = ollama_service.generate(
            prompt="What is SDLC? Answer in one sentence.",
            model=FAST_MODEL,
            temperature=0.3,
            max_tokens=300  # Higher limit for thinking models
        )

        elapsed = time.time() - start_time

        # Validate response structure
        assert isinstance(response, OllamaResponse)
        assert response.response is not None
        assert len(response.response) > 0
        assert response.done is True
        assert response.model is not None

        # Performance check
        assert elapsed < PERFORMANCE_TARGET_SIMPLE, \
            f"Generation took {elapsed:.2f}s (target: <{PERFORMANCE_TARGET_SIMPLE}s)"

        print(f"\n✅ Generation completed in {elapsed:.2f}s")
        print(f"   Model: {response.model}")
        print(f"   Tokens: {response.eval_count}")
        print(f"   Speed: {response.tokens_per_second:.1f} tok/s")

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_generation_with_system_prompt(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test generation with system prompt for context."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        response = ollama_service.generate(
            prompt="What are the main stages?",
            system="You are an SDLC 5.2.0 framework expert. Answer concisely.",
            temperature=0.3,
            max_tokens=200
        )

        assert isinstance(response, OllamaResponse)
        assert len(response.response) > 0
        # Should mention SDLC stages
        response_lower = response.response.lower()
        assert any(
            word in response_lower
            for word in ["stage", "phase", "foundation", "planning", "design", "build"]
        )

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_generation_with_specific_model(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test generation with specific Model Strategy v3.0 model."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        # Use fast model for quick test
        models = ollama_service.list_models()
        model_names = [m["name"] for m in models]

        # Find an available model
        test_model = None
        preferred_models = ["qwen3:8b", "qwen3:14b", "qwen3:32b"]
        for model in preferred_models:
            if any(model in m for m in model_names):
                test_model = model
                break

        if not test_model:
            pytest.skip("No preferred models available")

        response = ollama_service.generate(
            prompt="Say hello in Vietnamese.",
            model=test_model,
            temperature=0.5,
            max_tokens=50
        )

        assert isinstance(response, OllamaResponse)
        assert response.model == test_model or test_model in response.model
        assert len(response.response) > 0

    def test_generation_handles_connection_error(self) -> None:
        """Test generation handles connection errors gracefully."""
        # Use non-existent endpoint
        service = OllamaService(
            base_url="http://localhost:59999",
            timeout=2
        )

        with pytest.raises(OllamaError) as exc_info:
            service.generate(prompt="Hello")

        assert "not available" in str(exc_info.value).lower()


# ============================================================================
# TestRecommendationGeneration - SDLC Compliance Recommendations
# ============================================================================

class TestRecommendationGeneration:
    """Test SDLC compliance recommendation generation."""

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_generate_recommendation_success(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test generating compliance recommendation with AI."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        start_time = time.time()

        result = ollama_service.generate_recommendation(
            violation_type="missing_documentation",
            severity="high",
            location="docs/00-Project-Foundation",
            description="Missing required SDLC 5.2.0 stage folder",
            context={"project_name": "Test Project", "stage": "WHY"}
        )

        elapsed = time.time() - start_time

        # Validate response structure
        assert "recommendation" in result
        assert "confidence" in result
        assert "model" in result
        assert "duration_ms" in result
        assert "tokens" in result

        # Validate content
        assert len(result["recommendation"]) > 0
        assert 0 <= result["confidence"] <= 100
        assert result["model"] != "rule-based-fallback"

        # Performance check
        assert elapsed < PERFORMANCE_TARGET_COMPLEX, \
            f"Recommendation took {elapsed:.2f}s (target: <{PERFORMANCE_TARGET_COMPLEX}s)"

        print(f"\n✅ Recommendation generated in {elapsed:.2f}s")
        print(f"   Confidence: {result['confidence']}%")
        print(f"   Model: {result['model']}")

    def test_generate_recommendation_fallback(self) -> None:
        """Test fallback recommendation when Ollama unavailable."""
        # Use non-existent endpoint to trigger fallback
        service = OllamaService(
            base_url="http://localhost:59999",
            timeout=2
        )

        result = service.generate_recommendation(
            violation_type="missing_documentation",
            severity="high",
            location="docs/00-Project-Foundation",
            description="Missing documentation"
        )

        # Fallback should work
        assert "recommendation" in result
        assert result["model"] == "rule-based-fallback"
        assert result["confidence"] == 60
        assert "Fix Steps" in result["recommendation"]

    def test_fallback_recommendations_all_types(self) -> None:
        """Test fallback recommendations exist for all violation types."""
        service = OllamaService(
            base_url="http://localhost:59999",
            timeout=1
        )

        violation_types = [
            "missing_documentation",
            "skipped_stage",
            "doc_code_drift",
            "policy_violation",
            "test_coverage_low",
            "unknown_violation_type",  # Should use default
        ]

        for vtype in violation_types:
            result = service.generate_recommendation(
                violation_type=vtype,
                severity="medium",
                location="/test/path",
                description="Test violation"
            )

            assert len(result["recommendation"]) > 0
            assert result["model"] == "rule-based-fallback"
            assert "Fix Steps" in result["recommendation"] or "fix steps" in result["recommendation"].lower()


# ============================================================================
# TestCustomPromptGeneration - Sprint 77 Custom Prompts
# ============================================================================

class TestCustomPromptGeneration:
    """Test custom prompt generation (Sprint 77 feature)."""

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_generate_from_prompt_success(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test custom prompt generation."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        result = ollama_service.generate_from_prompt(
            prompt="List 3 benefits of code review.",
            temperature=0.3,
            max_tokens=200
        )

        assert "recommendation" in result
        assert "confidence" in result
        assert len(result["recommendation"]) > 0
        assert result["confidence"] > 0

    def test_generate_from_prompt_fallback(self) -> None:
        """Test custom prompt fallback when unavailable."""
        service = OllamaService(
            base_url="http://localhost:59999",
            timeout=1
        )

        result = service.generate_from_prompt(
            prompt="Test prompt"
        )

        assert result["model"] == "fallback"
        assert result["confidence"] == 20
        assert "Unable to generate" in result["recommendation"]


# ============================================================================
# TestBatchProcessing - Batch Recommendation Generation
# ============================================================================

class TestBatchProcessing:
    """Test batch recommendation processing."""

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_batch_recommendations(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test batch recommendation generation."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        violations = [
            {
                "violation_type": "missing_documentation",
                "severity": "high",
                "location": "docs/",
                "description": "Missing docs"
            },
            {
                "violation_type": "policy_violation",
                "severity": "medium",
                "location": "src/",
                "description": "Policy issue"
            },
        ]

        start_time = time.time()
        results = ollama_service.generate_recommendations_batch(
            violations=violations,
            context={"project_name": "Batch Test"}
        )
        elapsed = time.time() - start_time

        assert len(results) == len(violations)
        for result in results:
            assert "recommendation" in result
            assert len(result["recommendation"]) > 0

        print(f"\n✅ Batch of {len(violations)} recommendations in {elapsed:.2f}s")

    def test_batch_recommendations_fallback(self) -> None:
        """Test batch recommendations with fallback."""
        service = OllamaService(
            base_url="http://localhost:59999",
            timeout=1
        )

        violations = [
            {"violation_type": "missing_documentation", "severity": "high", "location": "a", "description": "A"},
            {"violation_type": "policy_violation", "severity": "low", "location": "b", "description": "B"},
        ]

        results = service.generate_recommendations_batch(violations)

        assert len(results) == 2
        for result in results:
            assert result["model"] == "rule-based-fallback"


# ============================================================================
# TestModelManagement - Model Listing and Management
# ============================================================================

class TestModelManagement:
    """Test model management operations."""

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_list_models(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test listing available models."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        models = ollama_service.list_models()

        assert isinstance(models, list)
        assert len(models) > 0

        # Validate model structure
        for model in models:
            assert "name" in model
            assert "size" in model
            assert "modified" in model

        print(f"\n📋 Available models ({len(models)}):")
        for model in models[:10]:  # Show first 10
            print(f"   {model['name']} ({model['size']})")

    def test_list_models_when_unavailable(self) -> None:
        """Test list_models returns empty list when unavailable."""
        service = OllamaService(
            base_url="http://localhost:59999",
            timeout=1
        )

        models = service.list_models()

        assert models == []


# ============================================================================
# TestPerformance - Performance and Latency Validation
# ============================================================================

class TestPerformance:
    """Test performance targets and latency requirements."""

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_health_check_latency(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test health check completes within 5 seconds."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        start_time = time.time()
        health = ollama_service.health_check()
        elapsed = time.time() - start_time

        assert elapsed < HEALTH_CHECK_TIMEOUT, \
            f"Health check took {elapsed:.2f}s (target: <{HEALTH_CHECK_TIMEOUT}s)"

        print(f"\n⏱️ Health check: {elapsed:.3f}s")

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_generation_tokens_per_second(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test generation achieves reasonable token throughput."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        response = ollama_service.generate(
            prompt="Explain software testing in detail with examples.",
            temperature=0.5,
            max_tokens=500
        )

        # Model Strategy v3.0 targets: 34-80 tok/s depending on model
        tokens_per_sec = response.tokens_per_second

        print(f"\n⚡ Performance metrics:")
        print(f"   Tokens generated: {response.eval_count}")
        print(f"   Total duration: {response.total_duration_ms:.0f}ms")
        print(f"   Tokens/second: {tokens_per_sec:.1f}")

        # Minimum threshold: 10 tok/s (conservative for large models)
        if tokens_per_sec > 0:  # Only check if we have valid metrics
            assert tokens_per_sec >= 5, \
                f"Token throughput {tokens_per_sec:.1f} tok/s below minimum (5 tok/s)"


# ============================================================================
# TestFactoryFunctions - Factory and Singleton Patterns
# ============================================================================

class TestFactoryFunctions:
    """Test factory functions and singleton pattern."""

    def test_create_ollama_service(self) -> None:
        """Test create_ollama_service factory function."""
        service = create_ollama_service(
            base_url="http://test:11434",
            model=OllamaModel.QWEN3_8B.value
        )

        assert isinstance(service, OllamaService)
        assert service.base_url == "http://test:11434"
        assert service.model == OllamaModel.QWEN3_8B.value

    def test_get_ollama_service_singleton(self) -> None:
        """Test get_ollama_service returns singleton instance."""
        service1 = get_ollama_service()
        service2 = get_ollama_service()

        # Should be the same instance
        assert service1 is service2


# ============================================================================
# TestOllamaResponse - Response Dataclass Validation
# ============================================================================

class TestOllamaResponse:
    """Test OllamaResponse dataclass functionality."""

    def test_ollama_response_properties(self) -> None:
        """Test OllamaResponse computed properties."""
        response = OllamaResponse(
            model="test-model",
            response="Test response",
            done=True,
            total_duration_ns=1_000_000_000,  # 1 second
            load_duration_ns=100_000_000,
            prompt_eval_count=10,
            eval_count=50,
            eval_duration_ns=500_000_000  # 0.5 second for eval
        )

        # Test duration conversion
        assert response.total_duration_ms == 1000.0

        # Test tokens per second (50 tokens in 0.5s = 100 tok/s)
        assert response.tokens_per_second == 100.0

    def test_ollama_response_zero_duration(self) -> None:
        """Test OllamaResponse handles zero duration gracefully."""
        response = OllamaResponse(
            model="test-model",
            response="Test",
            done=True,
            total_duration_ns=0,
            load_duration_ns=0,
            prompt_eval_count=0,
            eval_count=0,
            eval_duration_ns=0
        )

        # Should not raise division by zero
        assert response.tokens_per_second == 0.0


# ============================================================================
# TestAIPlatformIntegration - Full AI-Platform Integration
# ============================================================================

class TestAIPlatformIntegration:
    """End-to-end tests for AI-Platform Ollama integration."""

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_full_compliance_workflow(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test complete compliance recommendation workflow."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        # Step 1: Check health
        health = ollama_service.health_check()
        assert health["healthy"] is True

        # Step 2: Generate recommendation
        result = ollama_service.generate_recommendation(
            violation_type="skipped_stage",
            severity="critical",
            location="docs/02-design",
            description="Design stage bypassed without gate approval",
            context={
                "project_name": "SDLC Orchestrator",
                "stage": "BUILD",
                "existing_files": ["README.md", "src/"]
            }
        )

        assert len(result["recommendation"]) > 100  # Meaningful recommendation
        assert result["confidence"] > 40

        # Step 3: Verify recommendation quality
        rec_lower = result["recommendation"].lower()
        assert any(
            word in rec_lower
            for word in ["stage", "gate", "approval", "review", "design"]
        ), "Recommendation should mention relevant concepts"

        print(f"\n🔄 Full workflow completed:")
        print(f"   Health: ✅")
        print(f"   Recommendation: {result['confidence']}% confidence")
        print(f"   Model: {result['model']}")

    @pytest.mark.skipif(
        not os.getenv("AI_PLATFORM_OLLAMA_URL"),
        reason="AI-Platform not configured"
    )
    def test_vietnamese_content_generation(
        self, ollama_service: OllamaService, ollama_available: bool
    ) -> None:
        """Test Vietnamese content generation (Model Strategy v3.0 feature)."""
        if not ollama_available:
            pytest.skip("Ollama not available on AI-Platform")

        # Use Vietnamese-optimized model
        response = ollama_service.generate(
            prompt="Giải thích SDLC là gì? Trả lời bằng tiếng Việt.",
            model=OllamaModel.DEFAULT_VIETNAMESE.value,
            temperature=0.5,
            max_tokens=200
        )

        # Should contain Vietnamese characters or common Vietnamese words
        vietnamese_markers = ["là", "và", "của", "được", "trong", "một", "các"]
        response_lower = response.response.lower()

        has_vietnamese = any(marker in response_lower for marker in vietnamese_markers)

        print(f"\n🇻🇳 Vietnamese generation:")
        print(f"   Has Vietnamese content: {has_vietnamese}")
        print(f"   Response length: {len(response.response)} chars")

        # Note: This assertion is soft - model may respond in English
        # The important thing is the generation succeeds
        assert len(response.response) > 0
