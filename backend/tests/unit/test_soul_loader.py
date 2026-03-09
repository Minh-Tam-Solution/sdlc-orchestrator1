"""
Unit Tests for SOULLoaderService — Sprint 225 (SOUL Template Integration).

Tests:
- load_all parses 17 SOUL templates from Framework submodule
- Parse YAML frontmatter correctly
- Extract markdown sections (Identity, Constraints, etc.)
- get_system_prompt formats key sections within max_chars
- Fallback when SOUL file missing
- get_tier_roles returns correct role sets
- Cache behavior (load once, serve from cache)
- clear_cache resets state

Zero Mock Policy: Tests use real SOUL files from Framework submodule
"""

import pytest
from pathlib import Path

from app.services.agent_team.soul_loader import (
    SOULLoaderService,
    SOULTemplate,
    TIER_ROLES,
    OPTIONAL_ROLES,
    clear_cache,
    _parse_frontmatter,
    _parse_sections,
)


# Resolve actual SOUL templates path from repo root
_REPO_ROOT = Path(__file__).resolve().parents[3]  # backend/tests/unit/ → repo root
_SOULS_PATH = _REPO_ROOT / "SDLC-Enterprise-Framework" / "05-Templates-Tools" / "04-SASE-Artifacts" / "souls"


@pytest.fixture(autouse=True)
def reset_cache():
    """Reset SOUL cache before each test."""
    clear_cache()
    yield
    clear_cache()


def _has_soul_files() -> bool:
    """Check if SOUL template files exist (submodule initialized)."""
    return _SOULS_PATH.exists() and any(_SOULS_PATH.glob("SOUL-*.md"))


# Skip all tests if Framework submodule not initialized
pytestmark = pytest.mark.skipif(
    not _has_soul_files(),
    reason="Framework submodule not initialized — SOUL files not available",
)


class TestLoadAll:
    """Tests for SOULLoaderService.load_all()."""

    def test_loads_17_templates(self):
        """Framework 6.1.2 has exactly 17 SOUL templates."""
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        templates = loader.load_all()
        assert len(templates) == 17

    def test_all_roles_present(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        templates = loader.load_all()
        expected_roles = {
            "researcher", "pm", "pjm", "architect", "coder", "reviewer",
            "tester", "devops", "fullstack", "ceo", "cpo", "cto",
            "writer", "sales", "cs", "itadmin", "assistant",
        }
        assert set(templates.keys()) == expected_roles

    def test_templates_have_correct_type(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        templates = loader.load_all()
        for role, template in templates.items():
            assert isinstance(template, SOULTemplate), f"Role '{role}' is not SOULTemplate"


class TestParseFrontmatter:
    """Tests for YAML frontmatter parsing."""

    def test_coder_frontmatter(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        template = loader.get_template("coder")
        assert template is not None
        assert template.role == "coder"
        assert template.category == "executor"
        assert template.sdlc_framework == "6.1.2"

    def test_ceo_frontmatter(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        template = loader.get_template("ceo")
        assert template is not None
        assert template.role == "ceo"

    def test_version_present(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        for role in loader.list_roles():
            template = loader.get_template(role)
            assert template.version, f"Role '{role}' missing version"


class TestExtractSections:
    """Tests for markdown section extraction."""

    def test_coder_has_identity_section(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        template = loader.get_template("coder")
        headings = [s.heading for s in template.sections]
        assert "Identity" in headings

    def test_coder_has_constraints_section(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        template = loader.get_template("coder")
        headings = [s.heading for s in template.sections]
        # May be "Constraints" or "Constraints (SE4A)"
        assert any("Constraints" in h for h in headings)

    def test_sections_have_content(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        template = loader.get_template("coder")
        for section in template.sections:
            assert section.content, f"Section '{section.heading}' has no content"


class TestGetSystemPrompt:
    """Tests for system prompt extraction."""

    def test_returns_string_for_valid_role(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        prompt = loader.get_system_prompt("coder")
        assert prompt is not None
        assert isinstance(prompt, str)
        assert len(prompt) > 100  # Should have substantial content

    def test_returns_none_for_missing_role(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        prompt = loader.get_system_prompt("nonexistent_role")
        assert prompt is None

    def test_respects_max_chars(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        prompt = loader.get_system_prompt("coder", max_chars=500)
        assert prompt is not None
        assert len(prompt) <= 600  # Allow small overshoot for truncation marker

    def test_contains_identity_content(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        prompt = loader.get_system_prompt("coder")
        assert "Identity" in prompt

    def test_default_max_chars_6000(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        prompt = loader.get_system_prompt("coder")
        # Should not exceed 6000 default
        assert len(prompt) <= 6100  # Small buffer for truncation


class TestGetTierRoles:
    """Tests for tier-based role filtering."""

    def test_lite_3_roles(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        roles = loader.get_tier_roles("LITE")
        assert len(roles) == 3
        assert roles == TIER_ROLES["LITE"]

    def test_standard_6_roles(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        roles = loader.get_tier_roles("STANDARD")
        assert len(roles) == 6

    def test_professional_10_roles(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        roles = loader.get_tier_roles("PROFESSIONAL")
        assert len(roles) == 10

    def test_enterprise_13_roles(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        roles = loader.get_tier_roles("ENTERPRISE")
        assert len(roles) == 13

    def test_case_insensitive(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        assert loader.get_tier_roles("lite") == TIER_ROLES["LITE"]

    def test_unknown_tier_empty(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        assert loader.get_tier_roles("UNKNOWN") == frozenset()

    def test_optional_roles_not_in_any_tier(self):
        for tier, roles in TIER_ROLES.items():
            for optional in OPTIONAL_ROLES:
                assert optional not in roles, (
                    f"Optional role '{optional}' should not be in tier '{tier}'"
                )


class TestCache:
    """Tests for caching behavior."""

    def test_load_all_caches_results(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        templates1 = loader.load_all()
        templates2 = loader.load_all()
        assert templates1 == templates2

    def test_clear_cache_resets(self):
        loader = SOULLoaderService(souls_path=_SOULS_PATH)
        loader.load_all()
        clear_cache()
        # After clear, list_roles should still work (triggers reload)
        roles = loader.list_roles()
        assert len(roles) == 17


class TestFallbackPath:
    """Tests for graceful fallback when path doesn't exist."""

    def test_missing_path_returns_empty(self):
        loader = SOULLoaderService(souls_path=Path("/nonexistent/path"))
        templates = loader.load_all()
        assert templates == {}

    def test_missing_path_system_prompt_none(self):
        loader = SOULLoaderService(souls_path=Path("/nonexistent/path"))
        prompt = loader.get_system_prompt("coder")
        assert prompt is None


class TestParseFunctions:
    """Tests for standalone parser functions."""

    def test_parse_frontmatter_no_yaml(self):
        fm, remaining = _parse_frontmatter("# Just a title\nSome content")
        assert fm == {}
        assert "Just a title" in remaining

    def test_parse_frontmatter_valid(self):
        content = "---\nrole: coder\ncategory: executor\n---\n# Title"
        fm, remaining = _parse_frontmatter(content)
        assert fm["role"] == "coder"
        assert fm["category"] == "executor"
        assert "# Title" in remaining

    def test_parse_sections_extracts_h2(self):
        md = "# Title\n\n## Section One\nContent 1\n\n## Section Two\nContent 2"
        title, sections = _parse_sections(md)
        assert title == "Title"
        assert len(sections) == 2
        assert sections[0].heading == "Section One"
        assert sections[1].heading == "Section Two"
