"""
=========================================================================
Unit Tests for ContextAuthorityEngineV1
SDLC Orchestrator - Sprint 109 (Vibecoding Index & Stage-Aware Gating)

Version: 1.0.0
Date: January 28, 2026
Status: ACTIVE - Unit Test Coverage
Authority: CTO Directive (P2-P3 Priority)
Framework: SDLC 5.3.0 Quality Assurance System

Coverage Target: 95%+ for context_authority.py

Test Categories:
1. Enums & Constants (8 tests)
2. Data Classes (10 tests)
3. ADR Extraction (10 tests)
4. Module Inference (8 tests)
5. ADR Linkage Check (10 tests)
6. Design Doc Check (8 tests)
7. AGENTS.md Freshness (8 tests)
8. Module Annotation Consistency (8 tests)
9. Full Validation Flow (10 tests)
10. Edge Cases (6 tests)

Total: 86 tests

Zero Mock Policy: Real validation logic, temporary file fixtures
=========================================================================
"""

import os
import pytest
import tempfile
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List
from uuid import uuid4

# Import directly from the module to test
import sys
sys.path.insert(0, "/home/nqh/shared/SDLC-Orchestrator/backend")

from app.services.governance.context_authority import (
    ContextViolationType,
    ViolationSeverity,
    ADRStatus,
    ADR,
    DesignSpec,
    AgentsMdInfo,
    ModuleAnnotation,
    ContextViolation,
    ContextValidationResult,
    CodeSubmission,
    ContextAuthorityEngineV1,
    create_context_authority_engine,
    get_context_authority_engine,
)


# ============================================================================
# CATEGORY 1: Enums & Constants
# ============================================================================


class TestEnums:
    """Test enum definitions and constants."""

    def test_enum_001_violation_types_complete(self):
        """ContextViolationType has all expected values."""
        assert ContextViolationType.ORPHAN_CODE.value == "orphan_code"
        assert ContextViolationType.NO_ADR_LINKAGE.value == "no_adr_linkage"
        assert ContextViolationType.NO_DESIGN_DOC.value == "no_design_doc"
        assert ContextViolationType.STALE_CONTEXT.value == "stale_context"
        assert ContextViolationType.MODULE_MISMATCH.value == "module_mismatch"
        assert ContextViolationType.DEPRECATED_ADR.value == "deprecated_adr"
        assert ContextViolationType.EMPTY_SPEC.value == "empty_spec"

    def test_enum_002_severity_levels(self):
        """ViolationSeverity has ERROR, WARNING, INFO."""
        assert ViolationSeverity.ERROR.value == "error"
        assert ViolationSeverity.WARNING.value == "warning"
        assert ViolationSeverity.INFO.value == "info"

    def test_enum_003_adr_status_complete(self):
        """ADRStatus has all lifecycle states."""
        assert ADRStatus.PROPOSED.value == "proposed"
        assert ADRStatus.ACCEPTED.value == "accepted"
        assert ADRStatus.DEPRECATED.value == "deprecated"
        assert ADRStatus.SUPERSEDED.value == "superseded"

    def test_enum_004_default_paths(self):
        """ContextAuthorityEngineV1 has correct default paths."""
        assert ContextAuthorityEngineV1.DEFAULT_ADR_PATH == "docs/02-design/03-ADRs"
        assert ContextAuthorityEngineV1.DEFAULT_SPEC_PATH == "docs/02-design/specs"
        assert ContextAuthorityEngineV1.DEFAULT_AGENTS_MD == "AGENTS.md"

    def test_enum_005_staleness_threshold(self):
        """Default staleness threshold is 7 days."""
        assert ContextAuthorityEngineV1.AGENTS_MD_STALENESS_DAYS == 7

    def test_enum_006_adr_pattern_regex(self):
        """ADR pattern matches @adr annotations."""
        engine = ContextAuthorityEngineV1()
        pattern = engine.ADR_PATTERN

        assert pattern.search("@adr: ADR-042")
        assert pattern.search("@adr ADR-001")
        assert pattern.search("@ADR: adr-123")
        assert not pattern.search("no annotation here")

    def test_enum_007_module_pattern_regex(self):
        """Module pattern matches @module annotations."""
        engine = ContextAuthorityEngineV1()
        pattern = engine.MODULE_PATTERN

        assert pattern.search("@module: services.auth")
        assert pattern.search("@module governance")
        assert not pattern.search("no module here")

    def test_enum_008_owner_pattern_regex(self):
        """Owner pattern matches @owner annotations."""
        engine = ContextAuthorityEngineV1()
        pattern = engine.OWNER_PATTERN

        assert pattern.search("@owner: backend_team")
        assert pattern.search("@owner @john_doe")
        assert not pattern.search("no owner here")


# ============================================================================
# CATEGORY 2: Data Classes
# ============================================================================


class TestDataClasses:
    """Test data class structures."""

    def test_data_001_adr_defaults(self):
        """ADR has correct defaults."""
        adr = ADR(
            id="ADR-001",
            title="Test Decision",
            status=ADRStatus.ACCEPTED,
            file_path="docs/ADR-001.md",
            content="# Test",
        )
        assert adr.modules == []
        assert adr.tags == []
        assert adr.superseded_by is None

    def test_data_002_design_spec_defaults(self):
        """DesignSpec has correct defaults."""
        spec = DesignSpec(
            task_id="TASK-123",
            file_path="docs/spec.md",
            exists=True,
        )
        assert spec.is_empty is False
        assert spec.word_count == 0

    def test_data_003_agents_md_info_defaults(self):
        """AgentsMdInfo has correct defaults."""
        info = AgentsMdInfo(
            file_path="AGENTS.md",
            exists=True,
        )
        assert info.is_stale is False
        assert info.age_days == 0

    def test_data_004_module_annotation_fields(self):
        """ModuleAnnotation has all required fields."""
        annotation = ModuleAnnotation(
            file_path="backend/app/service.py",
            declared_module="services.auth",
            inferred_module="services.auth",
            matches=True,
            owner="backend_team",
            adr_references=["ADR-001"],
        )
        assert annotation.matches is True
        assert len(annotation.adr_references) == 1

    def test_data_005_context_violation_fields(self):
        """ContextViolation has all fields."""
        violation = ContextViolation(
            type=ContextViolationType.NO_ADR_LINKAGE,
            severity=ViolationSeverity.ERROR,
            message="No ADR linked",
            module="services.auth",
            fix="Add @adr annotation",
            cli_command="sdlcctl adr create",
        )
        assert violation.type == ContextViolationType.NO_ADR_LINKAGE
        assert violation.severity == ViolationSeverity.ERROR

    def test_data_006_validation_result_defaults(self):
        """ContextValidationResult has correct defaults."""
        result = ContextValidationResult(
            valid=True,
        )
        assert result.violations == []
        assert result.warnings == []
        assert result.linked_adrs == []
        assert result.agents_md_fresh is True

    def test_data_007_validation_result_to_dict(self):
        """ContextValidationResult converts to dictionary."""
        result = ContextValidationResult(
            valid=True,
            adr_count=5,
            linked_adrs=["ADR-001", "ADR-002"],
            spec_found=True,
        )
        d = result.to_dict()

        assert d["valid"] is True
        assert d["adr_count"] == 5
        assert "ADR-001" in d["linked_adrs"]
        assert "validated_at" in d

    def test_data_008_code_submission_defaults(self):
        """CodeSubmission has correct defaults."""
        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["file1.py"],
        )
        assert submission.affected_modules == []
        assert submission.is_new_feature is False
        assert submission.task_id is None

    def test_data_009_violation_with_related_adr(self):
        """ContextViolation can reference related ADR."""
        violation = ContextViolation(
            type=ContextViolationType.DEPRECATED_ADR,
            severity=ViolationSeverity.WARNING,
            message="Linked to deprecated ADR",
            related_adr="ADR-042",
        )
        assert violation.related_adr == "ADR-042"

    def test_data_010_adr_with_superseded(self):
        """ADR can track superseded_by reference."""
        adr = ADR(
            id="ADR-001",
            title="Old Decision",
            status=ADRStatus.SUPERSEDED,
            file_path="docs/ADR-001.md",
            content="# Old",
            superseded_by="ADR-002",
        )
        assert adr.status == ADRStatus.SUPERSEDED
        assert adr.superseded_by == "ADR-002"


# ============================================================================
# CATEGORY 3: ADR Extraction
# ============================================================================


class TestADRExtraction:
    """Test ADR extraction logic."""

    @pytest.fixture
    def engine(self) -> ContextAuthorityEngineV1:
        """Create engine instance."""
        return ContextAuthorityEngineV1()

    def test_adr_001_extract_id_from_filename(self, engine):
        """Extract ADR ID from filename."""
        assert engine._extract_adr_id("ADR-042-Multi-Provider") == "ADR-042"
        assert engine._extract_adr_id("adr-001-auth") == "ADR-001"
        assert engine._extract_adr_id("042-some-decision") == "ADR-042"
        assert engine._extract_adr_id("001") == "ADR-001"

    def test_adr_002_extract_id_invalid(self, engine):
        """Return None for invalid filenames."""
        assert engine._extract_adr_id("invalid-file") is None
        assert engine._extract_adr_id("readme") is None
        assert engine._extract_adr_id("") is None

    def test_adr_003_extract_title(self, engine):
        """Extract title from ADR content."""
        content1 = "# ADR-042: Multi-Provider Architecture\n\nContent..."
        assert engine._extract_adr_title(content1) == "ADR-042: Multi-Provider Architecture"

        content2 = "Title: Some Decision\n\nContent..."
        assert engine._extract_adr_title(content2) == "Some Decision"

    def test_adr_004_extract_title_fallback(self, engine):
        """Return 'Unknown' if no title found."""
        content = "No title here\n\nJust content..."
        assert engine._extract_adr_title(content) == "Unknown"

    def test_adr_005_extract_status_accepted(self, engine):
        """Extract ACCEPTED status."""
        content = "Status: Accepted\n\nContent..."
        assert engine._extract_adr_status(content) == ADRStatus.ACCEPTED

        content2 = "status: approved\n\nContent..."
        assert engine._extract_adr_status(content2) == ADRStatus.ACCEPTED

    def test_adr_006_extract_status_deprecated(self, engine):
        """Extract DEPRECATED status."""
        content = "Status: Deprecated\n\nContent..."
        assert engine._extract_adr_status(content) == ADRStatus.DEPRECATED

    def test_adr_007_extract_status_default(self, engine):
        """Default to PROPOSED if no status found."""
        content = "No status here..."
        assert engine._extract_adr_status(content) == ADRStatus.PROPOSED

    def test_adr_008_extract_modules_from_content(self, engine):
        """Extract modules from ADR content."""
        content = """
        # ADR-042

        Affects: [services.auth, services.user, models.user]

        Content...
        """
        modules = engine._extract_adr_modules(content)
        assert "services.auth" in modules
        assert "services.user" in modules

    def test_adr_009_extract_modules_alternative_format(self, engine):
        """Extract modules with 'modules' keyword."""
        content = """
        modules: ["governance", "signals"]

        Content...
        """
        modules = engine._extract_adr_modules(content)
        assert "governance" in modules
        assert "signals" in modules

    def test_adr_010_extract_modules_empty(self, engine):
        """Return empty list if no modules found."""
        content = "No modules section here"
        modules = engine._extract_adr_modules(content)
        assert modules == []


# ============================================================================
# CATEGORY 4: Module Inference
# ============================================================================


class TestModuleInference:
    """Test module inference from file paths."""

    @pytest.fixture
    def engine(self) -> ContextAuthorityEngineV1:
        """Create engine instance."""
        return ContextAuthorityEngineV1()

    def test_module_001_backend_service(self, engine):
        """Infer module from backend service path."""
        path = "backend/app/services/auth/handler.py"
        module = engine._infer_module_from_path(path)
        assert module == "services.auth"

    def test_module_002_frontend_component(self, engine):
        """Infer module from frontend component path."""
        path = "frontend/src/components/Button/Button.tsx"
        module = engine._infer_module_from_path(path)
        assert module == "components.Button"

    def test_module_003_root_file(self, engine):
        """Return 'root' for files at root level."""
        path = "main.py"
        module = engine._infer_module_from_path(path)
        assert module == "root"

    def test_module_004_nested_path(self, engine):
        """Infer module from deeply nested path."""
        path = "backend/app/services/governance/signals/engine.py"
        module = engine._infer_module_from_path(path)
        assert module == "services.governance.signals"

    def test_module_005_strip_prefixes(self, engine):
        """Strip common prefixes (backend, frontend, app, src)."""
        path = "lib/utils/helpers.py"
        module = engine._infer_module_from_path(path)
        assert module == "utils"

    def test_module_006_is_module_file_exact(self, engine):
        """Check exact module match."""
        path = "backend/app/services/auth/handler.py"
        assert engine._is_module_file(path, "services.auth") is True
        assert engine._is_module_file(path, "services.user") is False

    def test_module_007_is_module_file_prefix(self, engine):
        """Check module prefix match."""
        path = "backend/app/services/auth/oauth/google.py"
        # services.auth.oauth should match services.auth prefix
        assert engine._is_module_file(path, "services.auth") is True

    def test_module_008_case_insensitive(self, engine):
        """Module matching is case insensitive."""
        path = "backend/app/Services/Auth/handler.py"
        assert engine._is_module_file(path, "services.auth") is True


# ============================================================================
# CATEGORY 5: ADR Linkage Check
# ============================================================================


class TestADRLinkageCheck:
    """Test ADR linkage validation."""

    @pytest.fixture
    def temp_repo(self, tmp_path):
        """Create temporary repository with ADRs."""
        # Create ADR directory
        adr_dir = tmp_path / "docs" / "02-design" / "03-ADRs"
        adr_dir.mkdir(parents=True)

        # Create ADR files
        adr1 = adr_dir / "ADR-001-Auth-Design.md"
        adr1.write_text("""
# ADR-001: Auth Design

Status: Accepted

Affects: [services.auth, models.user]

## Context
Authentication design decisions.
        """)

        adr2 = adr_dir / "ADR-002-Old-Decision.md"
        adr2.write_text("""
# ADR-002: Old Decision

Status: Deprecated

## Context
Old decision that was deprecated.
        """)

        return tmp_path

    @pytest.fixture
    def engine(self, temp_repo) -> ContextAuthorityEngineV1:
        """Create engine instance with temp repo."""
        engine = ContextAuthorityEngineV1(adr_path="docs/02-design/03-ADRs")
        return engine

    @pytest.mark.asyncio
    async def test_linkage_001_load_adrs(self, engine, temp_repo):
        """Load ADRs from repository."""
        await engine._load_adrs(str(temp_repo))
        assert len(engine._adr_cache) == 2
        assert "ADR-001" in engine._adr_cache
        assert "ADR-002" in engine._adr_cache

    @pytest.mark.asyncio
    async def test_linkage_002_find_adrs_for_module(self, engine, temp_repo):
        """Find ADRs that reference a module."""
        await engine._load_adrs(str(temp_repo))

        # services.auth is mentioned in ADR-001
        adrs = await engine._find_adrs_for_module(
            "services.auth",
            [],
            str(temp_repo)
        )
        assert "ADR-001" in adrs

    @pytest.mark.asyncio
    async def test_linkage_003_no_adr_violation(self, engine, temp_repo):
        """Generate violation when no ADR linked."""
        await engine._load_adrs(str(temp_repo))

        # services.payment is not mentioned in any ADR
        violations, linked = await engine._check_adr_linkage(
            ["services.payment"],
            [],
            str(temp_repo),
        )
        assert len(violations) == 1
        assert violations[0].type == ContextViolationType.NO_ADR_LINKAGE
        assert "services.payment" in violations[0].message

    @pytest.mark.asyncio
    async def test_linkage_004_has_adr_no_violation(self, engine, temp_repo):
        """No violation when ADR is linked."""
        await engine._load_adrs(str(temp_repo))

        violations, linked = await engine._check_adr_linkage(
            ["services.auth"],
            [],
            str(temp_repo),
        )
        # No ERROR violations for ADR linkage
        error_violations = [v for v in violations
                          if v.type == ContextViolationType.NO_ADR_LINKAGE]
        assert len(error_violations) == 0
        assert "ADR-001" in linked

    @pytest.mark.asyncio
    async def test_linkage_005_deprecated_adr_warning(self, engine, temp_repo):
        """Generate warning when linking to deprecated ADR."""
        await engine._load_adrs(str(temp_repo))

        # Add a fake ADR reference for deprecated ADR
        engine._adr_cache["ADR-002"].modules = ["services.legacy"]

        violations, _ = await engine._check_adr_linkage(
            ["services.legacy"],
            [],
            str(temp_repo),
        )
        deprecated_warnings = [v for v in violations
                              if v.type == ContextViolationType.DEPRECATED_ADR]
        assert len(deprecated_warnings) == 1
        assert deprecated_warnings[0].severity == ViolationSeverity.WARNING

    @pytest.mark.asyncio
    async def test_linkage_006_violation_includes_fix(self, engine, temp_repo):
        """Violation includes fix suggestion."""
        await engine._load_adrs(str(temp_repo))

        violations, _ = await engine._check_adr_linkage(
            ["services.new"],
            [],
            str(temp_repo),
        )
        assert violations[0].fix is not None
        assert "@adr" in violations[0].fix

    @pytest.mark.asyncio
    async def test_linkage_007_violation_includes_cli(self, engine, temp_repo):
        """Violation includes CLI command."""
        await engine._load_adrs(str(temp_repo))

        violations, _ = await engine._check_adr_linkage(
            ["services.new"],
            [],
            str(temp_repo),
        )
        assert violations[0].cli_command is not None
        assert "sdlcctl adr create" in violations[0].cli_command

    @pytest.mark.asyncio
    async def test_linkage_008_multiple_modules(self, engine, temp_repo):
        """Check multiple modules at once."""
        await engine._load_adrs(str(temp_repo))

        violations, linked = await engine._check_adr_linkage(
            ["services.auth", "services.unknown"],
            [],
            str(temp_repo),
        )
        # One violation for unknown module
        error_violations = [v for v in violations
                          if v.type == ContextViolationType.NO_ADR_LINKAGE]
        assert len(error_violations) == 1
        assert "services.unknown" in error_violations[0].message

    @pytest.mark.asyncio
    async def test_linkage_009_extract_from_file_annotation(self, engine, temp_repo):
        """Extract ADR from @adr annotation in file."""
        # Create a source file with @adr annotation
        src_dir = temp_repo / "backend" / "app" / "services"
        src_dir.mkdir(parents=True)
        src_file = src_dir / "custom.py"
        src_file.write_text("""
\"\"\"
Custom Service

@module: services
@adr: ADR-001
@owner: team
\"\"\"

def main():
    pass
        """)

        await engine._load_adrs(str(temp_repo))

        # Extract annotation
        adrs = await engine._extract_adr_annotation(
            "backend/app/services/custom.py",
            str(temp_repo)
        )
        assert "ADR-001" in adrs

    @pytest.mark.asyncio
    async def test_linkage_010_no_annotation_no_match(self, engine, temp_repo):
        """Return empty list when no annotation found."""
        await engine._load_adrs(str(temp_repo))

        adrs = await engine._extract_adr_annotation(
            "nonexistent.py",
            str(temp_repo)
        )
        assert adrs == []


# ============================================================================
# CATEGORY 6: Design Doc Check
# ============================================================================


class TestDesignDocCheck:
    """Test design document reference validation."""

    @pytest.fixture
    def temp_repo(self, tmp_path):
        """Create temporary repository."""
        spec_dir = tmp_path / "docs" / "02-design" / "specs"
        spec_dir.mkdir(parents=True)
        return tmp_path

    @pytest.fixture
    def engine(self) -> ContextAuthorityEngineV1:
        """Create engine instance."""
        return ContextAuthorityEngineV1(spec_path="docs/02-design/specs")

    @pytest.mark.asyncio
    async def test_design_001_no_spec_file(self, engine, temp_repo):
        """Generate violation when spec file missing."""
        violations = await engine._check_design_doc_reference(
            "TASK-123",
            str(temp_repo)
        )
        assert len(violations) == 1
        assert violations[0].type == ContextViolationType.NO_DESIGN_DOC
        assert violations[0].severity == ViolationSeverity.ERROR

    @pytest.mark.asyncio
    async def test_design_002_spec_file_exists(self, engine, temp_repo):
        """No violation when spec file exists."""
        spec_dir = temp_repo / "docs" / "02-design" / "specs"
        spec_file = spec_dir / "TASK-456-spec.md"
        # Content must be >100 chars to not be considered empty
        spec_file.write_text("# Design Spec\n\n## Overview\n\nThis is a meaningful design document with enough content to pass validation. It includes a proper overview section and meaningful technical details about the implementation approach.")

        violations = await engine._check_design_doc_reference(
            "TASK-456",
            str(temp_repo)
        )
        assert len(violations) == 0

    @pytest.mark.asyncio
    async def test_design_003_empty_spec_warning(self, engine, temp_repo):
        """Generate warning when spec file is empty."""
        spec_dir = temp_repo / "docs" / "02-design" / "specs"
        spec_file = spec_dir / "TASK-789-spec.md"
        spec_file.write_text("# TODO")  # Less than 100 chars

        violations = await engine._check_design_doc_reference(
            "TASK-789",
            str(temp_repo)
        )
        assert len(violations) == 1
        assert violations[0].type == ContextViolationType.EMPTY_SPEC
        assert violations[0].severity == ViolationSeverity.WARNING

    @pytest.mark.asyncio
    async def test_design_004_lowercase_task_id(self, engine, temp_repo):
        """Match lowercase task ID pattern."""
        spec_dir = temp_repo / "docs" / "02-design" / "specs"
        spec_file = spec_dir / "task-100-spec.md"
        # Content must be >100 chars to not be considered empty
        spec_file.write_text("# Design Spec for Task 100\n\n## Overview\n\nThis is a meaningful design document with enough content to pass the validation threshold. It includes technical details and implementation approach for the feature.")

        violations = await engine._check_design_doc_reference(
            "TASK-100",
            str(temp_repo)
        )
        assert len(violations) == 0

    @pytest.mark.asyncio
    async def test_design_005_underscore_format(self, engine, temp_repo):
        """Match underscore format (TASK_123)."""
        spec_dir = temp_repo / "docs" / "02-design" / "specs"
        spec_file = spec_dir / "TASK_200-spec.md"
        # Content must be >100 chars to not be considered empty
        spec_file.write_text("# Design Spec for Task 200\n\n## Overview\n\nThis is a meaningful design document with enough content to pass the validation threshold. It includes technical details and implementation approach for the feature.")

        violations = await engine._check_design_doc_reference(
            "TASK-200",
            str(temp_repo)
        )
        assert len(violations) == 0

    @pytest.mark.asyncio
    async def test_design_006_violation_includes_fix(self, engine, temp_repo):
        """Violation includes fix suggestion."""
        violations = await engine._check_design_doc_reference(
            "TASK-999",
            str(temp_repo)
        )
        assert violations[0].fix is not None
        assert "TASK-999" in violations[0].fix

    @pytest.mark.asyncio
    async def test_design_007_violation_includes_cli(self, engine, temp_repo):
        """Violation includes CLI command."""
        violations = await engine._check_design_doc_reference(
            "TASK-999",
            str(temp_repo)
        )
        assert violations[0].cli_command is not None
        assert "sdlcctl spec create" in violations[0].cli_command

    @pytest.mark.asyncio
    async def test_design_008_spec_dir_missing(self, engine, tmp_path):
        """Handle missing spec directory gracefully."""
        # tmp_path has no spec directory
        violations = await engine._check_design_doc_reference(
            "TASK-111",
            str(tmp_path)
        )
        assert len(violations) == 1
        assert violations[0].type == ContextViolationType.NO_DESIGN_DOC


# ============================================================================
# CATEGORY 7: AGENTS.md Freshness
# ============================================================================


class TestAgentsMdFreshness:
    """Test AGENTS.md freshness validation."""

    @pytest.fixture
    def engine(self) -> ContextAuthorityEngineV1:
        """Create engine instance."""
        return ContextAuthorityEngineV1(staleness_days=7)

    @pytest.mark.asyncio
    async def test_agents_001_missing_file(self, engine, tmp_path):
        """Generate info when AGENTS.md missing."""
        violations = await engine._check_agents_md_freshness(str(tmp_path))
        assert len(violations) == 1
        assert violations[0].type == ContextViolationType.STALE_CONTEXT
        assert violations[0].severity == ViolationSeverity.INFO

    @pytest.mark.asyncio
    async def test_agents_002_fresh_file(self, engine, tmp_path):
        """No violation when AGENTS.md is fresh."""
        agents_file = tmp_path / "AGENTS.md"
        agents_file.write_text("# Project Context")

        violations = await engine._check_agents_md_freshness(str(tmp_path))
        assert len(violations) == 0

    @pytest.mark.asyncio
    async def test_agents_003_stale_file_warning(self, engine, tmp_path):
        """Generate warning when AGENTS.md is stale."""
        agents_file = tmp_path / "AGENTS.md"
        agents_file.write_text("# Old Context")

        # Set modification time to 10 days ago
        old_time = datetime.now() - timedelta(days=10)
        os.utime(agents_file, (old_time.timestamp(), old_time.timestamp()))

        violations = await engine._check_agents_md_freshness(str(tmp_path))
        assert len(violations) == 1
        assert violations[0].type == ContextViolationType.STALE_CONTEXT
        assert violations[0].severity == ViolationSeverity.WARNING
        assert "10 days old" in violations[0].message

    @pytest.mark.asyncio
    async def test_agents_004_custom_staleness_days(self, tmp_path):
        """Respect custom staleness threshold."""
        engine = ContextAuthorityEngineV1(staleness_days=3)

        agents_file = tmp_path / "AGENTS.md"
        agents_file.write_text("# Context")

        # Set modification time to 5 days ago
        old_time = datetime.now() - timedelta(days=5)
        os.utime(agents_file, (old_time.timestamp(), old_time.timestamp()))

        violations = await engine._check_agents_md_freshness(str(tmp_path))
        assert len(violations) == 1
        assert "threshold: 3" in violations[0].message

    @pytest.mark.asyncio
    async def test_agents_005_exactly_threshold(self, engine, tmp_path):
        """File exactly at threshold is not stale."""
        agents_file = tmp_path / "AGENTS.md"
        agents_file.write_text("# Context")

        # Set modification time to exactly 7 days ago
        old_time = datetime.now() - timedelta(days=7)
        os.utime(agents_file, (old_time.timestamp(), old_time.timestamp()))

        violations = await engine._check_agents_md_freshness(str(tmp_path))
        # Exactly 7 days is not > 7, so should be ok
        assert len(violations) == 0

    @pytest.mark.asyncio
    async def test_agents_006_violation_includes_fix(self, engine, tmp_path):
        """Missing AGENTS.md violation includes fix."""
        violations = await engine._check_agents_md_freshness(str(tmp_path))
        assert violations[0].fix is not None
        assert "AGENTS.md" in violations[0].fix

    @pytest.mark.asyncio
    async def test_agents_007_violation_includes_cli(self, engine, tmp_path):
        """Stale AGENTS.md violation includes CLI command."""
        agents_file = tmp_path / "AGENTS.md"
        agents_file.write_text("# Old Context")
        old_time = datetime.now() - timedelta(days=10)
        os.utime(agents_file, (old_time.timestamp(), old_time.timestamp()))

        violations = await engine._check_agents_md_freshness(str(tmp_path))
        assert violations[0].cli_command is not None
        assert "sdlcctl agents" in violations[0].cli_command

    @pytest.mark.asyncio
    async def test_agents_008_custom_path(self, tmp_path):
        """Support custom AGENTS.md path."""
        engine = ContextAuthorityEngineV1(agents_md_path="docs/AGENTS.md")

        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        agents_file = docs_dir / "AGENTS.md"
        agents_file.write_text("# Context")

        violations = await engine._check_agents_md_freshness(str(tmp_path))
        assert len(violations) == 0


# ============================================================================
# CATEGORY 8: Module Annotation Consistency
# ============================================================================


class TestModuleAnnotationConsistency:
    """Test module annotation consistency validation."""

    @pytest.fixture
    def engine(self) -> ContextAuthorityEngineV1:
        """Create engine instance."""
        return ContextAuthorityEngineV1()

    @pytest.fixture
    def temp_repo(self, tmp_path):
        """Create temporary repository with source files."""
        src_dir = tmp_path / "backend" / "app" / "services" / "auth"
        src_dir.mkdir(parents=True)
        return tmp_path

    @pytest.mark.asyncio
    async def test_consistency_001_matching_annotation(self, engine, temp_repo):
        """No violation when annotation matches directory."""
        src_dir = temp_repo / "backend" / "app" / "services" / "auth"
        src_file = src_dir / "handler.py"
        src_file.write_text("""
\"\"\"
Auth Handler

@module: services.auth
\"\"\"

def main():
    pass
        """)

        violations = await engine._check_module_annotation_consistency(
            ["backend/app/services/auth/handler.py"],
            str(temp_repo)
        )
        assert len(violations) == 0

    @pytest.mark.asyncio
    async def test_consistency_002_mismatched_annotation(self, engine, temp_repo):
        """Generate violation when annotation doesn't match."""
        src_dir = temp_repo / "backend" / "app" / "services" / "auth"
        src_file = src_dir / "handler.py"
        src_file.write_text("""
\"\"\"
Auth Handler

@module: services.user
\"\"\"

def main():
    pass
        """)

        violations = await engine._check_module_annotation_consistency(
            ["backend/app/services/auth/handler.py"],
            str(temp_repo)
        )
        assert len(violations) == 1
        assert violations[0].type == ContextViolationType.MODULE_MISMATCH
        assert violations[0].severity == ViolationSeverity.ERROR

    @pytest.mark.asyncio
    async def test_consistency_003_no_annotation_ok(self, engine, temp_repo):
        """No violation when no @module annotation."""
        src_dir = temp_repo / "backend" / "app" / "services" / "auth"
        src_file = src_dir / "handler.py"
        src_file.write_text("""
\"\"\"
Auth Handler (no module annotation)
\"\"\"

def main():
    pass
        """)

        violations = await engine._check_module_annotation_consistency(
            ["backend/app/services/auth/handler.py"],
            str(temp_repo)
        )
        assert len(violations) == 0

    @pytest.mark.asyncio
    async def test_consistency_004_skip_non_code_files(self, engine, temp_repo):
        """Skip non-Python/TypeScript files."""
        docs_dir = temp_repo / "docs"
        docs_dir.mkdir()
        doc_file = docs_dir / "readme.md"
        doc_file.write_text("# Readme")

        violations = await engine._check_module_annotation_consistency(
            ["docs/readme.md"],
            str(temp_repo)
        )
        assert len(violations) == 0

    @pytest.mark.asyncio
    async def test_consistency_005_typescript_file(self, engine, temp_repo):
        """Check TypeScript files."""
        src_dir = temp_repo / "frontend" / "src" / "components"
        src_dir.mkdir(parents=True)
        ts_file = src_dir / "Button.tsx"
        ts_file.write_text("""
/**
 * Button Component
 *
 * @module: components
 */

export const Button = () => <button>Click</button>;
        """)

        violations = await engine._check_module_annotation_consistency(
            ["frontend/src/components/Button.tsx"],
            str(temp_repo)
        )
        assert len(violations) == 0

    @pytest.mark.asyncio
    async def test_consistency_006_violation_includes_fix(self, engine, temp_repo):
        """Violation includes fix suggestion."""
        src_dir = temp_repo / "backend" / "app" / "services" / "auth"
        src_file = src_dir / "handler.py"
        src_file.write_text("""
\"\"\"
@module: wrong.module
\"\"\"
        """)

        violations = await engine._check_module_annotation_consistency(
            ["backend/app/services/auth/handler.py"],
            str(temp_repo)
        )
        assert violations[0].fix is not None
        assert "@module" in violations[0].fix

    @pytest.mark.asyncio
    async def test_consistency_007_case_insensitive(self, engine, temp_repo):
        """Module matching is case insensitive."""
        src_dir = temp_repo / "backend" / "app" / "services" / "auth"
        src_file = src_dir / "handler.py"
        src_file.write_text("""
\"\"\"
@module: Services.Auth
\"\"\"
        """)

        violations = await engine._check_module_annotation_consistency(
            ["backend/app/services/auth/handler.py"],
            str(temp_repo)
        )
        assert len(violations) == 0

    @pytest.mark.asyncio
    async def test_consistency_008_multiple_files(self, engine, temp_repo):
        """Check multiple files at once."""
        src_dir = temp_repo / "backend" / "app" / "services" / "auth"

        # Matching file
        src_file1 = src_dir / "handler.py"
        src_file1.write_text("\"\"\"@module: services.auth\"\"\"")

        # Mismatched file
        src_file2 = src_dir / "utils.py"
        src_file2.write_text("\"\"\"@module: wrong.module\"\"\"")

        violations = await engine._check_module_annotation_consistency(
            [
                "backend/app/services/auth/handler.py",
                "backend/app/services/auth/utils.py",
            ],
            str(temp_repo)
        )
        assert len(violations) == 1
        assert "utils.py" in violations[0].file_path


# ============================================================================
# CATEGORY 9: Full Validation Flow
# ============================================================================


class TestFullValidationFlow:
    """Test complete validation workflow."""

    @pytest.fixture
    def temp_repo(self, tmp_path):
        """Create fully structured temporary repository."""
        # ADRs
        adr_dir = tmp_path / "docs" / "02-design" / "03-ADRs"
        adr_dir.mkdir(parents=True)
        adr = adr_dir / "ADR-001-Governance.md"
        adr.write_text("""
# ADR-001: Governance Design

Status: Accepted

Affects: [governance, signals]

Content...
        """)

        # Specs
        spec_dir = tmp_path / "docs" / "02-design" / "specs"
        spec_dir.mkdir(parents=True)

        # AGENTS.md
        agents = tmp_path / "AGENTS.md"
        agents.write_text("# Project Context\n\nThis is the AGENTS.md file.")

        # Source files
        src_dir = tmp_path / "backend" / "app" / "services" / "governance"
        src_dir.mkdir(parents=True)
        src_file = src_dir / "signals.py"
        src_file.write_text("""
\"\"\"
Signals Engine

@module: services.governance
@adr: ADR-001
\"\"\"

def calculate():
    pass
        """)

        return tmp_path

    @pytest.fixture
    def engine(self) -> ContextAuthorityEngineV1:
        """Create engine instance."""
        return ContextAuthorityEngineV1()

    @pytest.mark.asyncio
    async def test_flow_001_valid_submission(self, engine, temp_repo):
        """Fully valid submission passes."""
        await engine.initialize(str(temp_repo))

        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["backend/app/services/governance/signals.py"],
            affected_modules=["governance"],
            is_new_feature=False,
        )

        result = await engine.validate_context(submission)

        assert result.valid is True
        assert len(result.violations) == 0
        assert result.agents_md_fresh is True

    @pytest.mark.asyncio
    async def test_flow_002_missing_adr_linkage(self, engine, temp_repo):
        """Submission with orphan module fails."""
        await engine.initialize(str(temp_repo))

        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["backend/app/services/new/service.py"],
            affected_modules=["services.new"],  # Not in any ADR
            is_new_feature=False,
        )

        result = await engine.validate_context(submission)

        assert result.valid is False
        assert any(v.type == ContextViolationType.NO_ADR_LINKAGE
                  for v in result.violations)

    @pytest.mark.asyncio
    async def test_flow_003_new_feature_missing_spec(self, engine, temp_repo):
        """New feature without spec fails."""
        await engine.initialize(str(temp_repo))

        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["backend/app/services/new.py"],
            affected_modules=["governance"],  # Has ADR
            is_new_feature=True,
            task_id="TASK-999",  # No spec for this task
        )

        result = await engine.validate_context(submission)

        assert result.valid is False
        assert result.spec_found is False
        assert any(v.type == ContextViolationType.NO_DESIGN_DOC
                  for v in result.violations)

    @pytest.mark.asyncio
    async def test_flow_004_new_feature_with_spec(self, engine, temp_repo):
        """New feature with spec passes."""
        # Create spec with >100 chars content
        spec_dir = temp_repo / "docs" / "02-design" / "specs"
        spec = spec_dir / "TASK-100-spec.md"
        spec.write_text("# Design Spec for Task 100\n\n## Overview\n\nThis is a meaningful design document with enough content to pass the validation threshold. It includes technical details and implementation approach for the feature.")

        await engine.initialize(str(temp_repo))

        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["backend/app/services/governance/signals.py"],
            affected_modules=["governance"],
            is_new_feature=True,
            task_id="TASK-100",
            repo_path=str(temp_repo),  # Provide repo path for validation
        )

        result = await engine.validate_context(submission)

        assert result.valid is True
        assert result.spec_found is True

    @pytest.mark.asyncio
    async def test_flow_005_stale_agents_warning(self, engine, temp_repo):
        """Stale AGENTS.md generates warning."""
        # Make AGENTS.md stale
        agents = temp_repo / "AGENTS.md"
        old_time = datetime.now() - timedelta(days=10)
        os.utime(agents, (old_time.timestamp(), old_time.timestamp()))

        await engine.initialize(str(temp_repo))

        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["backend/app/services/governance/signals.py"],
            affected_modules=["governance"],
            repo_path=str(temp_repo),  # Provide repo path for validation
        )

        result = await engine.validate_context(submission)

        # Still valid (warning, not error)
        assert result.valid is True
        assert result.agents_md_fresh is False
        assert len(result.warnings) > 0

    @pytest.mark.asyncio
    async def test_flow_006_result_to_dict(self, engine, temp_repo):
        """Result converts to dictionary."""
        await engine.initialize(str(temp_repo))

        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["backend/app/services/governance/signals.py"],
            affected_modules=["governance"],
        )

        result = await engine.validate_context(submission)
        d = result.to_dict()

        assert "valid" in d
        assert "violations" in d
        assert "warnings" in d
        assert "validated_at" in d

    @pytest.mark.asyncio
    async def test_flow_007_linked_adrs_tracked(self, engine, temp_repo):
        """Linked ADRs are tracked in result."""
        await engine.initialize(str(temp_repo))

        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["backend/app/services/governance/signals.py"],
            affected_modules=["governance"],
        )

        result = await engine.validate_context(submission)

        assert len(result.linked_adrs) > 0
        assert "ADR-001" in result.linked_adrs

    @pytest.mark.asyncio
    async def test_flow_008_adr_count_accurate(self, engine, temp_repo):
        """ADR count reflects loaded ADRs."""
        await engine.initialize(str(temp_repo))

        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=[],
            affected_modules=[],
        )

        result = await engine.validate_context(submission)

        assert result.adr_count == 1  # One ADR in temp_repo

    @pytest.mark.asyncio
    async def test_flow_009_multiple_violations(self, engine, temp_repo):
        """Multiple violations collected."""
        await engine.initialize(str(temp_repo))

        # Create mismatched module file
        src_dir = temp_repo / "backend" / "app" / "services" / "new"
        src_dir.mkdir(parents=True)
        src_file = src_dir / "service.py"
        src_file.write_text("\"\"\"@module: wrong.module\"\"\"")

        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=["backend/app/services/new/service.py"],
            affected_modules=["services.orphan"],  # No ADR
            is_new_feature=True,
            task_id="TASK-MISSING",  # No spec
        )

        result = await engine.validate_context(submission)

        assert result.valid is False
        # Multiple violations: orphan code, no spec, module mismatch
        assert len(result.violations) >= 2

    @pytest.mark.asyncio
    async def test_flow_010_empty_submission(self, engine, temp_repo):
        """Empty submission passes."""
        await engine.initialize(str(temp_repo))

        submission = CodeSubmission(
            submission_id=uuid4(),
            project_id=uuid4(),
            changed_files=[],
            affected_modules=[],
        )

        result = await engine.validate_context(submission)

        assert result.valid is True


# ============================================================================
# CATEGORY 10: Edge Cases
# ============================================================================


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.fixture
    def engine(self) -> ContextAuthorityEngineV1:
        """Create engine instance."""
        return ContextAuthorityEngineV1()

    def test_edge_001_factory_functions(self):
        """Factory functions work correctly."""
        engine1 = create_context_authority_engine()
        engine2 = get_context_authority_engine()

        assert engine1 is not None
        assert engine2 is not None

    def test_edge_002_custom_paths(self):
        """Engine accepts custom paths."""
        engine = ContextAuthorityEngineV1(
            adr_path="custom/adr",
            spec_path="custom/specs",
            agents_md_path="docs/AGENTS.md",
            staleness_days=14,
        )
        assert engine.adr_path == "custom/adr"
        assert engine.spec_path == "custom/specs"
        assert engine.staleness_days == 14

    @pytest.mark.asyncio
    async def test_edge_003_nonexistent_repo(self, engine):
        """Handle nonexistent repository gracefully."""
        await engine._load_adrs("/nonexistent/path")
        assert len(engine._adr_cache) == 0

    @pytest.mark.asyncio
    async def test_edge_004_unreadable_file(self, engine, tmp_path):
        """Handle unreadable files gracefully."""
        violations = await engine._check_module_annotation_consistency(
            ["nonexistent.py"],
            str(tmp_path)
        )
        assert len(violations) == 0

    def test_edge_005_empty_adr_cache(self):
        """Empty ADR cache is handled."""
        engine = ContextAuthorityEngineV1()
        assert len(engine._adr_cache) == 0

    @pytest.mark.asyncio
    async def test_edge_006_special_characters_in_path(self, engine, tmp_path):
        """Handle special characters in paths."""
        src_dir = tmp_path / "backend" / "app" / "services-v2"
        src_dir.mkdir(parents=True)
        src_file = src_dir / "handler_v2.py"
        src_file.write_text("# No module annotation")

        violations = await engine._check_module_annotation_consistency(
            ["backend/app/services-v2/handler_v2.py"],
            str(tmp_path)
        )
        # Should not crash
        assert isinstance(violations, list)


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
