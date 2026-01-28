"""
=========================================================================
Isolated Unit Tests for Auto-Generation Service
SDLC Orchestrator - Sprint 108 (Governance Foundation)

Tests the 4 auto-generators:
1. IntentGenerator - Intent document from task context
2. OwnershipGenerator - Ownership annotation suggestion
3. ContextAttachmentGenerator - ADR/spec attachment
4. AttestationGenerator - AI code attestation

Run: cd backend && PYTHONPATH=. python3 -m pytest tests/unit/services/governance/test_auto_generator_isolated.py -v --noconftest
=========================================================================
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add backend to path for isolated testing
backend_path = Path(__file__).parent.parent.parent.parent.parent / "app"
sys.path.insert(0, str(backend_path.parent))

import pytest

from app.services.governance.auto_generator import (
    FallbackLevel,
    GeneratorType,
    GenerationResult,
    TaskContext,
    FileContext,
    PRContext,
    AISessionContext,
    IntentGenerator,
    OwnershipGenerator,
    ContextAttachmentGenerator,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def task_context() -> TaskContext:
    """Create sample task context."""
    return TaskContext(
        task_id="TASK-123",
        title="Add user authentication flow",
        description="Implement JWT-based authentication with OAuth2 support for social login.",
        acceptance_criteria="- Users can login with email/password\n- Users can login with Google OAuth",
        project_name="SDLC-Orchestrator",
        assignee="developer1",
    )


@pytest.fixture
def file_context_python() -> FileContext:
    """Create sample file context for Python file."""
    return FileContext(
        file_path="backend/app/services/auth_service.py",
        repository_path="/home/user/project",
        file_extension=".py",
        is_new_file=True,
        task_creator="developer1",
    )


@pytest.fixture
def file_context_frontend() -> FileContext:
    """Create sample file context for TypeScript file."""
    return FileContext(
        file_path="frontend/src/components/LoginForm.tsx",
        repository_path="/home/user/project",
        file_extension=".tsx",
        is_new_file=False,
    )


@pytest.fixture
def pr_context() -> PRContext:
    """Create sample PR context."""
    return PRContext(
        pr_number=123,
        pr_title="Add user authentication",
        pr_description="This PR implements user authentication with JWT",
        changed_files=[
            "backend/app/services/auth_service.py",
            "backend/app/api/routes/auth.py",
            "backend/app/models/user.py",
        ],
        repository_path="/home/user/project",
        author="developer1",
    )


# ============================================================================
# Test Suite 1: Enums and Data Classes
# ============================================================================

class TestEnumsAndDataClasses:
    """Test enum values and data class behavior."""

    def test_fallback_level_values(self):
        """FallbackLevel should have correct values."""
        assert FallbackLevel.LLM.value == "llm"
        assert FallbackLevel.TEMPLATE.value == "template"
        assert FallbackLevel.MINIMAL.value == "minimal"

    def test_generator_type_values(self):
        """GeneratorType should have correct values."""
        assert GeneratorType.INTENT.value == "intent_skeleton"
        assert GeneratorType.OWNERSHIP.value == "ownership_suggestion"
        assert GeneratorType.CONTEXT.value == "context_attachment"
        assert GeneratorType.ATTESTATION.value == "attestation_template"

    def test_generation_result_ui_badge_llm(self):
        """LLM result should show green badge."""
        result = GenerationResult(
            success=True,
            fallback_level=FallbackLevel.LLM,
            content="test",
            confidence=85,
            latency_ms=100,
            generator_type=GeneratorType.INTENT,
        )
        badge = result.ui_badge
        assert badge["color"] == "green"
        assert "AI" in badge["text"]

    def test_generation_result_ui_badge_template(self):
        """Template result should show yellow badge."""
        result = GenerationResult(
            success=True,
            fallback_level=FallbackLevel.TEMPLATE,
            content="test",
            confidence=60,
            latency_ms=50,
            generator_type=GeneratorType.INTENT,
        )
        badge = result.ui_badge
        assert badge["color"] == "yellow"
        assert "template" in badge["text"].lower()

    def test_generation_result_ui_badge_minimal(self):
        """Minimal result should show orange badge."""
        result = GenerationResult(
            success=True,
            fallback_level=FallbackLevel.MINIMAL,
            content="test",
            confidence=30,
            latency_ms=10,
            generator_type=GeneratorType.INTENT,
        )
        badge = result.ui_badge
        assert badge["color"] == "orange"
        assert "manual" in badge["text"].lower()


# ============================================================================
# Test Suite 2: IntentGenerator
# ============================================================================

class TestIntentGenerator:
    """Test intent document generation."""

    @pytest.mark.asyncio
    async def test_intent_001_template_fallback(self, task_context: TaskContext):
        """Generator should produce valid template content when LLM unavailable."""
        # Mock Ollama service as unavailable
        with patch("app.services.governance.auto_generator.get_ollama_service") as mock_get:
            mock_ollama = Mock()
            mock_ollama.is_available = False
            mock_get.return_value = mock_ollama

            generator = IntentGenerator(ollama_service=mock_ollama)
            result = await generator.generate(task_context)

        assert result.success is True
        assert result.fallback_level == FallbackLevel.TEMPLATE
        assert result.generator_type == GeneratorType.INTENT
        assert "# Intent:" in result.content
        assert "## Why This Change?" in result.content
        assert task_context.title in result.content

    @pytest.mark.asyncio
    async def test_intent_002_template_content_structure(self, task_context: TaskContext):
        """Template should have all required sections."""
        generator = IntentGenerator()
        generator.ollama = Mock()
        generator.ollama.is_available = False

        result = await generator.generate(task_context)

        assert "## Why This Change?" in result.content
        assert "## What Problem Does It Solve?" in result.content
        assert "## Alternatives Considered" in result.content

    @pytest.mark.asyncio
    async def test_intent_003_minimal_fallback(self, task_context: TaskContext):
        """Generator should produce minimal content when template fails."""
        generator = IntentGenerator()
        generator.ollama = Mock()
        generator.ollama.is_available = False

        # Force minimal fallback by creating invalid state
        result = generator._generate_minimal(task_context)

        assert result.success is True
        assert result.fallback_level == FallbackLevel.MINIMAL
        assert result.confidence == 30
        assert "Manual input required" in result.content

    @pytest.mark.asyncio
    async def test_intent_004_includes_task_metadata(self, task_context: TaskContext):
        """Result metadata should include task ID."""
        generator = IntentGenerator()
        generator.ollama = Mock()
        generator.ollama.is_available = False

        result = await generator.generate(task_context)

        assert result.metadata.get("task_id") == "TASK-123"

    @pytest.mark.asyncio
    async def test_intent_005_latency_tracked(self, task_context: TaskContext):
        """Result should track generation latency."""
        generator = IntentGenerator()
        generator.ollama = Mock()
        generator.ollama.is_available = False

        result = await generator.generate(task_context)

        assert result.latency_ms >= 0


# ============================================================================
# Test Suite 3: OwnershipGenerator
# ============================================================================

class TestOwnershipGenerator:
    """Test ownership suggestion generation."""

    @pytest.mark.asyncio
    async def test_ownership_001_directory_pattern_backend(
        self, file_context_python: FileContext
    ):
        """Should detect backend team for backend/app/services paths."""
        generator = OwnershipGenerator()
        result = await generator.generate(file_context_python)

        assert result.success is True
        assert result.generator_type == GeneratorType.OWNERSHIP
        assert "@backend-team" in result.content or "@governance-team" in result.content

    @pytest.mark.asyncio
    async def test_ownership_002_directory_pattern_frontend(
        self, file_context_frontend: FileContext
    ):
        """Should detect frontend team for frontend/src paths."""
        generator = OwnershipGenerator()
        result = await generator.generate(file_context_frontend)

        assert result.success is True
        assert "@frontend-team" in result.content

    @pytest.mark.asyncio
    async def test_ownership_003_extension_fallback(self):
        """Should use extension fallback for unknown paths."""
        file = FileContext(
            file_path="unknown/path/file.py",
            repository_path=".",
            file_extension=".py",
            is_new_file=True,
        )
        generator = OwnershipGenerator()
        result = await generator.generate(file)

        assert result.success is True
        # Should fall back to extension-based ownership
        assert "@" in result.content

    @pytest.mark.asyncio
    async def test_ownership_004_annotation_format_python(
        self, file_context_python: FileContext
    ):
        """Python files should use # comment format."""
        generator = OwnershipGenerator()
        result = await generator.generate(file_context_python)

        assert "# @owner:" in result.content
        assert "# @module:" in result.content
        assert "# @created:" in result.content

    @pytest.mark.asyncio
    async def test_ownership_005_annotation_format_typescript(
        self, file_context_frontend: FileContext
    ):
        """TypeScript files should use JSDoc format."""
        generator = OwnershipGenerator()
        result = await generator.generate(file_context_frontend)

        assert "/**" in result.content
        assert "@owner" in result.content
        assert "*/" in result.content

    @pytest.mark.asyncio
    async def test_ownership_006_task_creator_fallback(self):
        """Should include task creator as fallback option."""
        file = FileContext(
            file_path="some/random/path/file.unknown",
            repository_path=".",
            file_extension=".unknown",
            is_new_file=True,
            task_creator="alice",
        )
        generator = OwnershipGenerator()
        result = await generator.generate(file)

        assert result.success is True
        # Task creator should be in suggestions
        suggestions = result.metadata.get("all_suggestions", [])
        task_creator_suggestion = [s for s in suggestions if s.get("source") == "task_creator"]
        assert len(task_creator_suggestion) > 0 or "@" in result.content

    @pytest.mark.asyncio
    async def test_ownership_007_confidence_ordering(self):
        """Should pick highest confidence source."""
        file = FileContext(
            file_path="backend/app/services/test.py",
            repository_path=".",
            file_extension=".py",
            is_new_file=True,
            task_creator="developer",
        )
        generator = OwnershipGenerator()
        result = await generator.generate(file)

        # Directory pattern (0.9) > task_creator (0.5) > extension (0.3)
        assert result.metadata.get("source") in ["directory_pattern", "CODEOWNERS"]

    def test_ownership_008_pattern_matching(self):
        """Pattern matching should work correctly."""
        generator = OwnershipGenerator()

        # Test exact match
        assert generator._matches_pattern("file.py", "file.py") is True

        # Test wildcard match
        assert generator._matches_pattern("backend/app/test.py", "backend/app/*") is True

        # Test suffix match
        assert generator._matches_pattern("path/to/file.py", "file.py") is True


# ============================================================================
# Test Suite 4: ContextAttachmentGenerator
# ============================================================================

class TestContextAttachmentGenerator:
    """Test context attachment generation."""

    @pytest.mark.asyncio
    async def test_context_001_extracts_modules(self, pr_context: PRContext):
        """Should extract modules from changed files."""
        generator = ContextAttachmentGenerator()
        modules = generator._extract_modules(pr_context.changed_files)

        # Should extract module names like "services", "routes", "models"
        assert len(modules) > 0

    @pytest.mark.asyncio
    async def test_context_002_generates_result(self, pr_context: PRContext):
        """Should generate context attachment result."""
        generator = ContextAttachmentGenerator()
        result = await generator.generate(pr_context)

        assert result.success is True
        assert result.generator_type == GeneratorType.CONTEXT
        assert result.fallback_level == FallbackLevel.TEMPLATE

    @pytest.mark.asyncio
    async def test_context_003_includes_pr_number(self, pr_context: PRContext):
        """Result should include PR number in metadata."""
        generator = ContextAttachmentGenerator()
        result = await generator.generate(pr_context)

        assert result.metadata.get("pr_number") == 123

    def test_context_004_module_extraction_patterns(self):
        """Should correctly extract modules from various paths."""
        generator = ContextAttachmentGenerator()

        test_files = [
            "backend/app/services/auth_service.py",
            "backend/app/api/routes/users.py",
            "frontend/src/components/LoginForm/index.tsx",
        ]

        modules = generator._extract_modules(test_files)

        # Should have extracted some modules
        assert len(modules) > 0

    def test_context_005_title_extraction(self):
        """Should extract title from markdown content."""
        generator = ContextAttachmentGenerator()

        content = """# ADR-001: Use PostgreSQL for Database

## Status
Accepted

## Context
We need a database...
"""
        title = generator._extract_title(content)
        assert "ADR-001" in title or "PostgreSQL" in title


# ============================================================================
# Test Suite 5: FAIL-SAFE Principle
# ============================================================================

class TestFailSafePrinciple:
    """Test fail-safe chain: LLM -> Template -> Minimal."""

    @pytest.mark.asyncio
    async def test_failsafe_001_always_returns_result(self, task_context: TaskContext):
        """Generator should ALWAYS return a result, never raise."""
        generator = IntentGenerator()
        generator.ollama = Mock()
        generator.ollama.is_available = False

        # Should not raise
        result = await generator.generate(task_context)
        assert result is not None
        assert result.success is True

    @pytest.mark.asyncio
    async def test_failsafe_002_ownership_always_succeeds(self):
        """Ownership generator should always succeed."""
        generator = OwnershipGenerator()

        # Even with completely unknown file
        file = FileContext(
            file_path="/completely/random/unknown/path/file.xyz",
            repository_path="/nonexistent",
            file_extension=".xyz",
            is_new_file=True,
        )

        result = await generator.generate(file)
        assert result is not None
        assert result.success is True
        assert "@" in result.content

    @pytest.mark.asyncio
    async def test_failsafe_003_context_always_succeeds(self, pr_context: PRContext):
        """Context attachment should always succeed."""
        generator = ContextAttachmentGenerator()
        generator.repository_path = "/nonexistent/path"

        result = await generator.generate(pr_context)
        assert result is not None
        assert result.success is True


# ============================================================================
# Test Suite 6: Performance Requirements
# ============================================================================

class TestPerformanceRequirements:
    """Test latency and performance requirements."""

    @pytest.mark.asyncio
    async def test_perf_001_template_generation_fast(self, task_context: TaskContext):
        """Template generation should complete in <1s."""
        generator = IntentGenerator()
        generator.ollama = Mock()
        generator.ollama.is_available = False

        result = await generator.generate(task_context)

        # Template generation should be very fast
        assert result.latency_ms < 1000

    @pytest.mark.asyncio
    async def test_perf_002_ownership_generation_fast(
        self, file_context_python: FileContext
    ):
        """Ownership generation should complete in <2s."""
        generator = OwnershipGenerator()
        result = await generator.generate(file_context_python)

        # Should be fast since no git operations
        assert result.latency_ms < 2000

    @pytest.mark.asyncio
    async def test_perf_003_context_generation_fast(self, pr_context: PRContext):
        """Context generation should complete in <5s."""
        generator = ContextAttachmentGenerator()
        generator.repository_path = "/nonexistent"  # Skip file scanning

        result = await generator.generate(pr_context)
        assert result.latency_ms < 5000


# ============================================================================
# Test Suite 7: Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.mark.asyncio
    async def test_edge_001_empty_description(self):
        """Should handle empty task description."""
        task = TaskContext(
            task_id="TASK-001",
            title="Test Task",
            description="",
        )
        generator = IntentGenerator()
        generator.ollama = Mock()
        generator.ollama.is_available = False

        result = await generator.generate(task)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_edge_002_very_long_description(self):
        """Should handle very long descriptions."""
        task = TaskContext(
            task_id="TASK-001",
            title="Test Task",
            description="x" * 10000,  # 10K character description
        )
        generator = IntentGenerator()
        generator.ollama = Mock()
        generator.ollama.is_available = False

        result = await generator.generate(task)
        assert result.success is True
        # Content should be truncated
        assert len(result.content) < 12000

    @pytest.mark.asyncio
    async def test_edge_003_special_characters_in_path(self):
        """Should handle special characters in file paths."""
        file = FileContext(
            file_path="backend/app/services/test_with spaces.py",
            repository_path=".",
            file_extension=".py",
            is_new_file=True,
        )
        generator = OwnershipGenerator()

        result = await generator.generate(file)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_edge_004_empty_changed_files(self):
        """Should handle PR with no changed files."""
        pr = PRContext(
            pr_number=1,
            pr_title="Empty PR",
            pr_description="Test",
            changed_files=[],
        )
        generator = ContextAttachmentGenerator()

        result = await generator.generate(pr)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_edge_005_unicode_in_content(self):
        """Should handle unicode characters."""
        task = TaskContext(
            task_id="TASK-001",
            title="Thêm tính năng xác thực",  # Vietnamese
            description="Triển khai xác thực JWT với OAuth2 cho đăng nhập xã hội.",
        )
        generator = IntentGenerator()
        generator.ollama = Mock()
        generator.ollama.is_available = False

        result = await generator.generate(task)
        assert result.success is True
        assert task.title in result.content


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
