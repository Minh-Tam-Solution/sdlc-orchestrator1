"""
Unit tests for P0 artifact detection with legacy/non-standard stage names.

Tests fuzzy stage path resolution in P0ArtifactChecker to handle projects
using legacy long-form names (e.g., '02-Design-Architecture' instead of '02-design').

SDLC 6.0.5 Enhancement — Based on Bflow Framework Assessment (Feb 2026).
"""

import tempfile
from pathlib import Path

import pytest

from sdlcctl.validation.p0 import P0ArtifactChecker, P0_ARTIFACTS
from sdlcctl.validation.tier import Tier


class TestP0LegacyStageNames:
    """Test P0 detection with legacy/non-standard stage folder names."""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project with standard SDLC 6.0.5 stage names."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            docs_root = project_root / "docs"
            docs_root.mkdir()
            yield project_root

    def _create_stage_with_readme(self, docs_root: Path, stage_name: str) -> Path:
        """Helper: create a stage folder with a README containing real content."""
        stage_dir = docs_root / stage_name
        stage_dir.mkdir(parents=True, exist_ok=True)
        readme = stage_dir / "README.md"
        readme.write_text(
            f"# Stage {stage_name}\n\n"
            f"This is the entry point for the {stage_name} stage.\n"
            "It contains all relevant documentation for this lifecycle phase.\n"
            "See subdirectories for detailed artifacts and evidence.\n",
            encoding="utf-8",
        )
        return stage_dir

    def test_standard_names_detected(self, temp_project):
        """Test that standard SDLC 6.0.5 names are detected (baseline)."""
        docs = temp_project / "docs"
        for stage_id in ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]:
            from sdlcctl.validation.tier import STAGE_NAMES
            self._create_stage_with_readme(docs, STAGE_NAMES[stage_id])

        checker = P0ArtifactChecker(temp_project, tier=Tier.PROFESSIONAL)
        result = checker.check_all()

        # All README P0 artifacts should be found
        readme_results = {
            k: v for k, v in result.results.items()
            if k.endswith("-README")
        }
        found_readmes = sum(1 for r in readme_results.values() if r.found)
        assert found_readmes == len(readme_results), (
            f"Expected all README P0s found with standard names, "
            f"got {found_readmes}/{len(readme_results)}"
        )

    def test_legacy_long_form_names_detected(self, temp_project):
        """Test P0 READMEs found under legacy long-form stage names (e.g., 02-Design-Architecture)."""
        docs = temp_project / "docs"
        legacy_names = {
            "00": "00-Project-Foundation",
            "01": "01-Planning-Analysis",
            "02": "02-Design-Architecture",
            "03": "03-Development-Implementation",
            "04": "04-Testing-Quality",
            "05": "05-Deployment-Release",
            "06": "06-Operations-Maintenance",
            "07": "07-Integration-APIs",
            "08": "08-Team-Management",
            "09": "09-Executive-Reports",
        }
        for stage_id, name in legacy_names.items():
            self._create_stage_with_readme(docs, name)

        checker = P0ArtifactChecker(temp_project, tier=Tier.PROFESSIONAL)
        result = checker.check_all()

        # All README P0 artifacts should be found via fuzzy resolution
        readme_results = {
            k: v for k, v in result.results.items()
            if k.endswith("-README")
        }
        found_readmes = sum(1 for r in readme_results.values() if r.found)
        assert found_readmes == len(readme_results), (
            f"Expected all README P0s found with legacy names, "
            f"got {found_readmes}/{len(readme_results)}"
        )

        # Each found README should have a "legacy path" issue
        for artifact_id, check_result in readme_results.items():
            if check_result.found:
                legacy_issues = [i for i in check_result.issues if "legacy path" in i.lower()]
                assert len(legacy_issues) > 0, (
                    f"Artifact {artifact_id} found but missing 'legacy path' issue"
                )

    def test_mixed_naming_detected(self, temp_project):
        """Test mixed naming: stages 00-04 standard, stages 05-09 legacy."""
        docs = temp_project / "docs"
        from sdlcctl.validation.tier import STAGE_NAMES

        # Standard names for 00-04
        for stage_id in ["00", "01", "02", "03", "04"]:
            self._create_stage_with_readme(docs, STAGE_NAMES[stage_id])

        # Legacy names for 05-09
        legacy_05_09 = {
            "05": "05-Deployment-Release",
            "06": "06-Operations-Maintenance",
            "07": "07-Integration-APIs",
            "08": "08-Team-Management",
            "09": "09-Executive-Reports",
        }
        for stage_id, name in legacy_05_09.items():
            self._create_stage_with_readme(docs, name)

        checker = P0ArtifactChecker(temp_project, tier=Tier.PROFESSIONAL)
        result = checker.check_all()

        # All README P0 artifacts should be found (100% coverage)
        readme_results = {
            k: v for k, v in result.results.items()
            if k.endswith("-README")
        }
        found_readmes = sum(1 for r in readme_results.values() if r.found)
        assert found_readmes == len(readme_results), (
            f"Expected 100% P0 README coverage with mixed naming, "
            f"got {found_readmes}/{len(readme_results)}"
        )

        # Standard names should have no legacy issues
        for stage_id in ["00", "01", "02", "03", "04"]:
            artifact_id = f"P0-{stage_id}-README"
            if artifact_id in readme_results:
                r = readme_results[artifact_id]
                legacy_issues = [i for i in r.issues if "legacy path" in i.lower()]
                assert len(legacy_issues) == 0, (
                    f"Standard-named {artifact_id} should NOT have legacy path issues"
                )

        # Legacy names should have legacy path warnings
        for stage_id in ["05", "06", "07", "08", "09"]:
            artifact_id = f"P0-{stage_id}-README"
            if artifact_id in readme_results:
                r = readme_results[artifact_id]
                legacy_issues = [i for i in r.issues if "legacy path" in i.lower()]
                assert len(legacy_issues) > 0, (
                    f"Legacy-named {artifact_id} should have legacy path issues"
                )

    def test_sad_found_at_legacy_path(self, temp_project):
        """Test P0 SAD artifact found under 02-Design-Architecture/02-System-Architecture/."""
        docs = temp_project / "docs"
        design_dir = docs / "02-Design-Architecture"
        arch_dir = design_dir / "02-System-Architecture"
        arch_dir.mkdir(parents=True)
        sad = arch_dir / "System-Architecture-Document.md"
        sad.write_text(
            "# System Architecture Document\n\n"
            "This document describes the system architecture for the project.\n"
            "It covers high-level components, data flow, and deployment topology.\n"
            "Version: 1.0.0 | Status: APPROVED\n",
            encoding="utf-8",
        )

        checker = P0ArtifactChecker(temp_project, tier=Tier.PROFESSIONAL)
        result = checker.check_all()

        sad_result = result.results.get("P0-02-SAD")
        assert sad_result is not None, "P0-02-SAD should be checked"
        assert sad_result.found, (
            "P0 SAD should be found at legacy path 02-Design-Architecture/02-System-Architecture/"
        )
        legacy_issues = [i for i in sad_result.issues if "legacy path" in i.lower()]
        assert len(legacy_issues) > 0, "SAD at legacy path should produce legacy path issue"

    def test_stage_path_caching(self, temp_project):
        """Test that stage path resolution is cached (no repeated filesystem scans)."""
        docs = temp_project / "docs"
        self._create_stage_with_readme(docs, "02-Design-Architecture")

        checker = P0ArtifactChecker(temp_project, tier=Tier.PROFESSIONAL)

        # First resolution
        path1 = checker._resolve_stage_path("02")
        assert path1 is not None
        assert path1.name == "02-Design-Architecture"

        # Check cache is populated
        assert "02" in checker._stage_path_cache
        assert checker._stage_path_cache["02"] == path1

        # Second resolution should hit cache
        path2 = checker._resolve_stage_path("02")
        assert path2 == path1

    def test_missing_stage_returns_none(self, temp_project):
        """Test that a missing stage resolves to None."""
        checker = P0ArtifactChecker(temp_project, tier=Tier.PROFESSIONAL)
        result = checker._resolve_stage_path("02")
        assert result is None

    def test_coverage_percent_with_legacy_names(self, temp_project):
        """Test that P0 coverage percentage is correct with legacy names."""
        docs = temp_project / "docs"
        # Create all stages with legacy names
        legacy_names = {
            "00": "00-Project-Foundation",
            "01": "01-Planning-Analysis",
            "02": "02-Design-Architecture",
            "03": "03-Development-Implementation",
            "04": "04-Testing-Quality",
            "05": "05-Deployment-Release",
            "06": "06-Operations-Maintenance",
            "07": "07-Integration-APIs",
            "08": "08-Team-Management",
            "09": "09-Executive-Reports",
        }
        for stage_id, name in legacy_names.items():
            self._create_stage_with_readme(docs, name)

        checker = P0ArtifactChecker(temp_project, tier=Tier.PROFESSIONAL)
        result = checker.check_all()

        # Coverage should be > 0% (was 0% before fuzzy detection)
        assert result.coverage_percent > 0, (
            f"Coverage should be > 0% with legacy names, got {result.coverage_percent}%"
        )
        # All README artifacts should be found
        assert result.artifacts_found > 0, "At least some artifacts should be found"

    def test_enterprise_tier_with_archive(self, temp_project):
        """Test ENTERPRISE tier includes 10-archive README check."""
        docs = temp_project / "docs"
        # Create all stages + archive with legacy names
        for stage_id in range(10):
            sid = f"{stage_id:02d}"
            self._create_stage_with_readme(docs, f"{sid}-Legacy-Name-{sid}")

        # Also create 10-archive
        self._create_stage_with_readme(docs, "10-archive")

        checker = P0ArtifactChecker(temp_project, tier=Tier.ENTERPRISE)
        result = checker.check_all()

        archive_result = result.results.get("P0-10-README")
        assert archive_result is not None, "P0-10-README should be checked for ENTERPRISE"
        assert archive_result.found, "10-archive README should be found"

    def test_no_regression_standard_paths(self, temp_project):
        """Regression test: standard SDLC 6.0.5 paths still work perfectly."""
        docs = temp_project / "docs"
        from sdlcctl.validation.tier import STAGE_NAMES

        # Create full standard structure
        for stage_id in ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]:
            self._create_stage_with_readme(docs, STAGE_NAMES[stage_id])

        # Add SAD at standard path
        arch_dir = docs / "02-design" / "02-System-Architecture"
        arch_dir.mkdir(parents=True)
        (arch_dir / "System-Architecture-Document.md").write_text(
            "# System Architecture Document\n\n"
            "Full architecture documentation for the system.\n"
            "Covers components, data flow, security, and deployment.\n",
            encoding="utf-8",
        )

        # Add FRD at standard path
        req_dir = docs / "01-planning" / "01-Requirements"
        req_dir.mkdir(parents=True)
        (req_dir / "Functional-Requirements-Document.md").write_text(
            "# Functional Requirements Document\n\n"
            "Complete functional requirements for the project.\n"
            "Includes user stories, acceptance criteria, and priorities.\n",
            encoding="utf-8",
        )

        checker = P0ArtifactChecker(temp_project, tier=Tier.PROFESSIONAL)
        result = checker.check_all()

        # No legacy path issues should appear for standard paths
        for artifact_id, check_result in result.results.items():
            if check_result.found:
                legacy_issues = [i for i in check_result.issues if "legacy path" in i.lower()]
                assert len(legacy_issues) == 0, (
                    f"Standard path {artifact_id} should NOT have legacy path issues, "
                    f"but found: {legacy_issues}"
                )
