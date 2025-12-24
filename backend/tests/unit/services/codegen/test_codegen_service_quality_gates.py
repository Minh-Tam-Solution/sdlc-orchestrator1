"""
Tests for CodegenService Quality Gates Integration - Sprint 48.

Test coverage for quality gate integration in CodegenService:
- generate_with_quality_gates method
- QualityGatedResult handling
- Quality gate pass/fail scenarios
- Blocking behavior

SDLC Stage: 04 - BUILD
Sprint: 48 - Quality Gates + Ollama Optimization + MVP Hardening
Framework: SDLC 5.1.1

Author: Backend Lead
Date: December 23, 2025
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.codegen.codegen_service import (
    CodegenService,
    QualityGatedResult,
    NoProviderAvailableError,
    GenerationError,
)
from app.services.codegen.base_provider import (
    CodegenSpec,
    CodegenResult,
)
from app.services.validators import ValidatorStatus, ValidatorResult


class TestQualityGatedResult:
    """Test QualityGatedResult dataclass."""

    def test_quality_gated_result_creation(self):
        """Test QualityGatedResult creation."""
        result = CodegenResult(
            code="# test",
            files={"test.py": "pass"},
            metadata={},
            provider="ollama",
            tokens_used=100,
            generation_time_ms=500,
        )

        gated = QualityGatedResult(
            result=result,
            quality_passed=True,
            quality_details={"error_count": 0},
            blocked=False,
        )

        assert gated.result == result
        assert gated.quality_passed is True
        assert gated.blocked is False

    def test_quality_gated_result_blocked(self):
        """Test blocked QualityGatedResult."""
        result = CodegenResult(
            code="# test",
            files={},
            metadata={},
            provider="ollama",
            tokens_used=100,
            generation_time_ms=500,
        )

        gated = QualityGatedResult(
            result=result,
            quality_passed=False,
            quality_details={"error_count": 5},
            blocked=True,
        )

        assert gated.quality_passed is False
        assert gated.blocked is True


class TestGenerateWithQualityGates:
    """Test generate_with_quality_gates method."""

    @pytest.fixture
    def mock_registry(self):
        """Create mock provider registry."""
        registry = MagicMock()
        registry.list_all.return_value = ["ollama", "claude"]
        registry.list_available.return_value = ["ollama"]
        registry.get_fallback_chain.return_value = ["ollama", "claude"]
        return registry

    @pytest.fixture
    def mock_provider(self):
        """Create mock provider."""
        provider = AsyncMock()
        provider.name = "ollama"
        provider.is_available = True
        provider.generate = AsyncMock(
            return_value=CodegenResult(
                code="class User: pass",
                files={"app/models/user.py": "class User: pass"},
                metadata={"prompt_tokens": 100, "completion_tokens": 200},
                provider="ollama",
                tokens_used=300,
                generation_time_ms=1000,
            )
        )
        return provider

    @pytest.fixture
    def service(self, mock_registry, mock_provider):
        """Create service with mocked registry."""
        mock_registry.select_provider.return_value = mock_provider
        mock_registry.get.return_value = mock_provider
        mock_registry.__len__ = MagicMock(return_value=2)

        service = CodegenService(custom_registry=mock_registry, auto_register=False)
        return service

    @pytest.fixture
    def sample_spec(self):
        """Create sample CodegenSpec."""
        return CodegenSpec(
            app_blueprint={"name": "TestApp", "modules": []},
            language="python",
            framework="fastapi",
        )

    @pytest.mark.asyncio
    async def test_generate_with_quality_gates_passed(self, service, sample_spec):
        """Test generation with quality gates passing."""
        # Mock quality validator
        mock_validator_result = ValidatorResult(
            validator_name="codegen-quality",
            status=ValidatorStatus.PASSED,
            message="All quality gates passed",
            details={
                "error_count": 0,
                "warning_count": 2,
                "gate_results": {
                    "syntax": "PASS",
                    "security": "PASS",
                },
            },
            duration_ms=50,
            blocking=False,
        )

        with patch(
            "app.services.validators.codegen_quality_validator.CodegenQualityValidator"
        ) as MockValidator:
            mock_instance = MagicMock()
            mock_instance.validate_generated_code = AsyncMock(
                return_value=mock_validator_result
            )
            MockValidator.return_value = mock_instance

            # Also mock cache to avoid actual cache operations
            with patch(
                "app.services.codegen.codegen_cache.get_codegen_cache"
            ) as mock_get_cache:
                mock_cache = AsyncMock()
                mock_cache.get = AsyncMock(return_value=None)
                mock_cache.set = AsyncMock(return_value=True)
                mock_get_cache.return_value = mock_cache

                result = await service.generate_with_quality_gates(
                    spec=sample_spec,
                    enable_security_scan=True,
                    enable_architecture_check=True,
                )

        assert isinstance(result, QualityGatedResult)
        assert result.quality_passed is True
        assert result.blocked is False
        assert result.quality_details["status"] == "passed"

    @pytest.mark.asyncio
    async def test_generate_with_quality_gates_failed(self, service, sample_spec):
        """Test generation with quality gates failing."""
        mock_validator_result = ValidatorResult(
            validator_name="codegen-quality",
            status=ValidatorStatus.FAILED,
            message="Quality gates failed: 3 errors",
            details={
                "error_count": 3,
                "warning_count": 1,
                "gate_results": {
                    "syntax": "PASS",
                    "security": "FAIL",
                },
            },
            duration_ms=100,
            blocking=True,
        )

        with patch(
            "app.services.validators.codegen_quality_validator.CodegenQualityValidator"
        ) as MockValidator:
            mock_instance = MagicMock()
            mock_instance.validate_generated_code = AsyncMock(
                return_value=mock_validator_result
            )
            MockValidator.return_value = mock_instance

            with patch(
                "app.services.codegen.codegen_cache.get_codegen_cache"
            ) as mock_get_cache:
                mock_cache = AsyncMock()
                mock_cache.get = AsyncMock(return_value=None)
                mock_cache.set = AsyncMock(return_value=True)
                mock_get_cache.return_value = mock_cache

                result = await service.generate_with_quality_gates(
                    spec=sample_spec,
                    block_on_failure=True,
                )

        assert result.quality_passed is False
        assert result.blocked is True

    @pytest.mark.asyncio
    async def test_generate_with_quality_gates_no_blocking(self, service, sample_spec):
        """Test generation with quality gates failing but not blocking."""
        mock_validator_result = ValidatorResult(
            validator_name="codegen-quality",
            status=ValidatorStatus.FAILED,
            message="Quality gates failed",
            details={"error_count": 2},
            duration_ms=50,
            blocking=True,
        )

        with patch(
            "app.services.validators.codegen_quality_validator.CodegenQualityValidator"
        ) as MockValidator:
            mock_instance = MagicMock()
            mock_instance.validate_generated_code = AsyncMock(
                return_value=mock_validator_result
            )
            MockValidator.return_value = mock_instance

            with patch(
                "app.services.codegen.codegen_cache.get_codegen_cache"
            ) as mock_get_cache:
                mock_cache = AsyncMock()
                mock_cache.get = AsyncMock(return_value=None)
                mock_cache.set = AsyncMock(return_value=True)
                mock_get_cache.return_value = mock_cache

                result = await service.generate_with_quality_gates(
                    spec=sample_spec,
                    block_on_failure=False,  # Don't block
                )

        # Quality failed but not blocked
        assert result.quality_passed is False
        assert result.blocked is False

    @pytest.mark.asyncio
    async def test_generate_with_quality_gates_security_disabled(
        self, service, sample_spec
    ):
        """Test generation with security scan disabled."""
        mock_validator_result = ValidatorResult(
            validator_name="codegen-quality",
            status=ValidatorStatus.PASSED,
            message="Quality gates passed",
            details={"error_count": 0},
            duration_ms=30,
            blocking=False,
        )

        with patch(
            "app.services.validators.codegen_quality_validator.CodegenQualityValidator"
        ) as MockValidator:
            mock_instance = MagicMock()
            mock_instance.validate_generated_code = AsyncMock(
                return_value=mock_validator_result
            )
            MockValidator.return_value = mock_instance

            with patch(
                "app.services.codegen.codegen_cache.get_codegen_cache"
            ) as mock_get_cache:
                mock_cache = AsyncMock()
                mock_cache.get = AsyncMock(return_value=None)
                mock_cache.set = AsyncMock(return_value=True)
                mock_get_cache.return_value = mock_cache

                await service.generate_with_quality_gates(
                    spec=sample_spec,
                    enable_security_scan=False,
                    enable_architecture_check=False,
                )

            # Verify validator was created with correct options
            MockValidator.assert_called_once_with(
                enable_security_scan=False,
                enable_architecture_check=False,
            )

    @pytest.mark.asyncio
    async def test_generate_with_quality_gates_skipped_status(
        self, service, sample_spec
    ):
        """Test generation when quality gates are skipped."""
        mock_validator_result = ValidatorResult(
            validator_name="codegen-quality",
            status=ValidatorStatus.SKIPPED,
            message="No files to validate",
            details={"files_checked": 0},
            duration_ms=5,
            blocking=False,
        )

        with patch(
            "app.services.validators.codegen_quality_validator.CodegenQualityValidator"
        ) as MockValidator:
            mock_instance = MagicMock()
            mock_instance.validate_generated_code = AsyncMock(
                return_value=mock_validator_result
            )
            MockValidator.return_value = mock_instance

            with patch(
                "app.services.codegen.codegen_cache.get_codegen_cache"
            ) as mock_get_cache:
                mock_cache = AsyncMock()
                mock_cache.get = AsyncMock(return_value=None)
                mock_cache.set = AsyncMock(return_value=True)
                mock_get_cache.return_value = mock_cache

                result = await service.generate_with_quality_gates(spec=sample_spec)

        # Skipped counts as passed
        assert result.quality_passed is True
        assert result.blocked is False

    @pytest.mark.asyncio
    async def test_generate_with_quality_gates_result_contains_details(
        self, service, sample_spec
    ):
        """Test quality details are correctly populated."""
        mock_validator_result = ValidatorResult(
            validator_name="codegen-quality",
            status=ValidatorStatus.PASSED,
            message="All gates passed",
            details={
                "files_checked": 5,
                "error_count": 0,
                "warning_count": 3,
                "gate_results": {
                    "syntax": "PASS",
                    "architecture": "PASS",
                    "security": "PASS",
                },
            },
            duration_ms=150,
            blocking=False,
        )

        with patch(
            "app.services.validators.codegen_quality_validator.CodegenQualityValidator"
        ) as MockValidator:
            mock_instance = MagicMock()
            mock_instance.validate_generated_code = AsyncMock(
                return_value=mock_validator_result
            )
            MockValidator.return_value = mock_instance

            with patch(
                "app.services.codegen.codegen_cache.get_codegen_cache"
            ) as mock_get_cache:
                mock_cache = AsyncMock()
                mock_cache.get = AsyncMock(return_value=None)
                mock_cache.set = AsyncMock(return_value=True)
                mock_get_cache.return_value = mock_cache

                result = await service.generate_with_quality_gates(spec=sample_spec)

        assert "validator" in result.quality_details
        assert result.quality_details["validator"] == "codegen-quality"
        assert "status" in result.quality_details
        assert "message" in result.quality_details
        assert "duration_ms" in result.quality_details
        assert "files_checked" in result.quality_details


class TestGenerateWithCaching:
    """Test generate method with caching (Sprint 48)."""

    @pytest.fixture
    def mock_registry(self):
        """Create mock provider registry."""
        registry = MagicMock()
        registry.list_all.return_value = ["ollama"]
        registry.list_available.return_value = ["ollama"]
        registry.get_fallback_chain.return_value = ["ollama"]
        registry.__len__ = MagicMock(return_value=1)
        return registry

    @pytest.fixture
    def mock_provider(self):
        """Create mock provider."""
        provider = AsyncMock()
        provider.name = "ollama"
        provider.is_available = True
        provider.generate = AsyncMock(
            return_value=CodegenResult(
                code="class User: pass",
                files={"user.py": "class User: pass"},
                metadata={},
                provider="ollama",
                tokens_used=100,
                generation_time_ms=500,
            )
        )
        return provider

    @pytest.fixture
    def service(self, mock_registry, mock_provider):
        """Create service with mocked registry."""
        mock_registry.select_provider.return_value = mock_provider
        service = CodegenService(custom_registry=mock_registry, auto_register=False)
        return service

    @pytest.fixture
    def sample_spec(self):
        """Create sample CodegenSpec."""
        return CodegenSpec(
            app_blueprint={"name": "CachedApp"},
            language="python",
            framework="fastapi",
        )

    @pytest.mark.asyncio
    async def test_generate_cache_hit(self, service, sample_spec):
        """Test generate returns cached result on cache hit."""
        cached_result = CodegenResult(
            code="# Cached code",
            files={"cached.py": "# cached"},
            metadata={"from_cache": True},
            provider="ollama",
            tokens_used=0,
            generation_time_ms=10,  # Fast retrieval
        )

        with patch(
            "app.services.codegen.codegen_cache.get_codegen_cache"
        ) as mock_get_cache:
            mock_cache = AsyncMock()
            mock_cache.get = AsyncMock(return_value=cached_result)
            mock_get_cache.return_value = mock_cache

            result = await service.generate(sample_spec, use_cache=True)

        assert result.metadata.get("from_cache") is True
        # Provider should not be called on cache hit
        mock_get_cache.return_value.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_cache_miss(self, service, mock_registry, sample_spec):
        """Test generate calls provider on cache miss."""
        with patch(
            "app.services.codegen.codegen_cache.get_codegen_cache"
        ) as mock_get_cache:
            mock_cache = AsyncMock()
            mock_cache.get = AsyncMock(return_value=None)  # Cache miss
            mock_cache.set = AsyncMock(return_value=True)
            mock_get_cache.return_value = mock_cache

            result = await service.generate(sample_spec, use_cache=True)

        assert result is not None
        # Cache should be set after generation
        mock_cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_cache_disabled(self, service, mock_registry, sample_spec):
        """Test generate skips cache when disabled."""
        with patch(
            "app.services.codegen.codegen_cache.get_codegen_cache"
        ) as mock_get_cache:
            mock_cache = AsyncMock()
            mock_get_cache.return_value = mock_cache

            result = await service.generate(sample_spec, use_cache=False)

        assert result is not None
        # Cache get/set should not be called
        mock_cache.get.assert_not_called()
        mock_cache.set.assert_not_called()

    @pytest.mark.asyncio
    async def test_generate_cache_error_continues(self, service, sample_spec):
        """Test generate continues if cache operations fail."""
        with patch(
            "app.services.codegen.codegen_cache.get_codegen_cache"
        ) as mock_get_cache:
            mock_cache = AsyncMock()
            mock_cache.get = AsyncMock(side_effect=Exception("Cache error"))
            mock_cache.set = AsyncMock(side_effect=Exception("Cache set error"))
            mock_get_cache.return_value = mock_cache

            # Should not raise, just continue without cache
            result = await service.generate(sample_spec, use_cache=True)

        assert result is not None
        assert result.provider == "ollama"
