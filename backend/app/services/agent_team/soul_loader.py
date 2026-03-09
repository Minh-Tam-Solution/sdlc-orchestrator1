"""
=========================================================================
SOUL Template Loader — Sprint 225 (SOUL Template Integration)
SDLC Orchestrator - Framework 6.1.2 Integration

Version: 1.0.0
Date: March 2026
Status: ACTIVE - Sprint 225
Authority: CTO Approved (Sprint 225 Plan)
Reference: SDLC-Enterprise-Framework/05-Templates-Tools/04-SASE-Artifacts/souls/

Purpose:
- Load SOUL markdown templates from Framework submodule
- Parse YAML frontmatter + markdown sections
- Extract key behavioral sections into system prompts
- Cache parsed templates in memory
- Provide tier-based role filtering

Design Decision (Option C):
  SOUL content → static system_prompt in AgentDefinition DB
  ContextInjector → appends 7 dynamic sections on every LLM call
  Total token budget: ~8,600 tokens max per invocation

Zero Mock Policy: Production-ready loader with graceful fallback
=========================================================================
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

# =========================================================================
# YAML safe_load — optional dependency guard
# =========================================================================
try:
    import yaml

    _YAML_AVAILABLE = True
except ImportError:  # pragma: no cover
    _YAML_AVAILABLE = False
    yaml = None  # type: ignore[assignment]


# =========================================================================
# Tier Availability Matrix (SDLC 6.1.2)
# =========================================================================
# LITE(3) → STANDARD(6) → PROFESSIONAL(10) → ENTERPRISE(13)
# OPTIONAL roles (writer, sales, cs, itadmin) are NEVER auto-seeded.

TIER_ROLES: dict[str, frozenset[str]] = {
    "LITE": frozenset({"assistant", "coder", "tester"}),
    "STANDARD": frozenset({"assistant", "coder", "tester", "pm", "architect", "reviewer"}),
    "PROFESSIONAL": frozenset({
        "assistant", "coder", "tester", "pm", "architect", "reviewer",
        "devops", "fullstack", "pjm", "researcher",
    }),
    "ENTERPRISE": frozenset({
        "assistant", "coder", "tester", "pm", "architect", "reviewer",
        "devops", "fullstack", "pjm", "researcher",
        "ceo", "cpo", "cto",
    }),
}

OPTIONAL_ROLES: frozenset[str] = frozenset({"writer", "sales", "cs", "itadmin"})


# =========================================================================
# Data Classes
# =========================================================================


@dataclass(frozen=True)
class SOULSection:
    """A single markdown section from a SOUL template."""

    heading: str
    content: str


@dataclass(frozen=True)
class SOULTemplate:
    """Parsed SOUL template with frontmatter metadata and markdown sections."""

    role: str
    category: str
    version: str
    sdlc_framework: str
    sdlc_stages: list[str]
    sdlc_gates: list[str]
    title: str
    sections: list[SOULSection] = field(default_factory=list)
    raw_frontmatter: dict = field(default_factory=dict)


# =========================================================================
# Module-level cache
# =========================================================================

_soul_cache: dict[str, SOULTemplate] = {}
_cache_loaded: bool = False


# =========================================================================
# Parser helpers
# =========================================================================


def _parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter between --- markers.

    Args:
        content: Raw markdown file content.

    Returns:
        Tuple of (frontmatter_dict, remaining_markdown).
    """
    if not content.startswith("---"):
        return {}, content

    end_idx = content.find("---", 3)
    if end_idx == -1:
        return {}, content

    yaml_block = content[3:end_idx].strip()
    remaining = content[end_idx + 3:].strip()

    if not _YAML_AVAILABLE:
        logger.warning("PyYAML not installed — SOUL frontmatter parsing disabled")
        return {}, remaining

    try:
        frontmatter = yaml.safe_load(yaml_block) or {}
    except Exception as e:
        logger.warning("Failed to parse SOUL frontmatter: %s", e)
        frontmatter = {}

    return frontmatter, remaining


def _parse_sections(markdown: str) -> tuple[str, list[SOULSection]]:
    """Parse markdown into H1 title and H2 sections.

    Args:
        markdown: Markdown content after frontmatter.

    Returns:
        Tuple of (title, list_of_sections).
    """
    lines = markdown.split("\n")
    title = ""
    sections: list[SOULSection] = []
    current_heading = ""
    current_lines: list[str] = []

    for line in lines:
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue

        if line.startswith("## "):
            # Flush previous section
            if current_heading:
                sections.append(SOULSection(
                    heading=current_heading,
                    content="\n".join(current_lines).strip(),
                ))
            current_heading = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    # Flush last section
    if current_heading:
        sections.append(SOULSection(
            heading=current_heading,
            content="\n".join(current_lines).strip(),
        ))

    return title, sections


# =========================================================================
# SOULLoaderService
# =========================================================================


def _default_souls_path() -> Path:
    """Resolve default path to SOUL templates via Framework submodule."""
    from app.core.config import settings

    repo_root = Path(__file__).resolve().parents[4]  # backend/app/services/agent_team/ → repo root
    return repo_root / settings.FRAMEWORK_SUBMODULE_PATH / "05-Templates-Tools" / "04-SASE-Artifacts" / "souls"


class SOULLoaderService:
    """Loads and caches SOUL role templates from Framework submodule.

    Usage:
        loader = SOULLoaderService()
        templates = loader.load_all()
        prompt = loader.get_system_prompt("coder", max_chars=6000)
    """

    def __init__(self, souls_path: Path | None = None) -> None:
        self._souls_path = souls_path

    @property
    def souls_path(self) -> Path:
        if self._souls_path is None:
            self._souls_path = _default_souls_path()
        return self._souls_path

    def load_all(self) -> dict[str, SOULTemplate]:
        """Scan and parse all SOUL-*.md files. Results are cached.

        Returns:
            Dict mapping role name → SOULTemplate.
        """
        global _soul_cache, _cache_loaded

        if _cache_loaded:
            return dict(_soul_cache)

        path = self.souls_path
        if not path.exists():
            logger.warning(
                "SOUL templates directory not found: %s — agents will use basic prompts",
                path,
            )
            _cache_loaded = True
            return {}

        soul_files = sorted(path.glob("SOUL-*.md"))
        if not soul_files:
            logger.warning("No SOUL-*.md files found in %s", path)
            _cache_loaded = True
            return {}

        for soul_file in soul_files:
            try:
                raw = soul_file.read_text(encoding="utf-8")
                frontmatter, markdown = _parse_frontmatter(raw)
                title, sections = _parse_sections(markdown)

                role = frontmatter.get("role", "")
                if not role:
                    # Derive from filename: SOUL-coder.md → coder
                    role = soul_file.stem.replace("SOUL-", "").lower()

                template = SOULTemplate(
                    role=role,
                    category=frontmatter.get("category", ""),
                    version=frontmatter.get("version", "1.0.0"),
                    sdlc_framework=frontmatter.get("sdlc_framework", ""),
                    sdlc_stages=frontmatter.get("sdlc_stages", []),
                    sdlc_gates=frontmatter.get("sdlc_gates", []),
                    title=title,
                    sections=sections,
                    raw_frontmatter=frontmatter,
                )
                _soul_cache[role] = template

            except Exception as e:
                logger.error("Failed to parse SOUL template %s: %s", soul_file.name, e)

        _cache_loaded = True
        logger.info(
            "Loaded %d SOUL templates from %s (roles: %s)",
            len(_soul_cache),
            path,
            ", ".join(sorted(_soul_cache.keys())),
        )

        return dict(_soul_cache)

    def get_template(self, role: str) -> SOULTemplate | None:
        """Get parsed SOUL template for a role.

        Args:
            role: SDLC role name (e.g. "coder", "architect").

        Returns:
            SOULTemplate or None if not found.
        """
        self.load_all()
        return _soul_cache.get(role)

    def get_system_prompt(self, role: str, *, max_chars: int = 6000) -> str | None:
        """Extract system prompt from SOUL template.

        Extracts Identity + Constraints + Communication + Gate Responsibilities
        sections in document order, truncating at max_chars with WARNING log.

        Args:
            role: SDLC role name.
            max_chars: Maximum characters for extracted prompt (~1,500 tokens at 4 chars/token).

        Returns:
            Formatted system prompt string, or None if no SOUL template found.
        """
        template = self.get_template(role)
        if template is None:
            return None

        # Priority sections to extract (in document order)
        priority_headings = {
            "Identity",
            "Constraints",
            "Constraints (SE4A)",
            "Constraints (SE4H)",
            "Constraints (Router)",
            "Communication Patterns",
            "Communication",
            "Gate Responsibilities",
            "Design-First Gate (MANDATORY — ABSOLUTE PROHIBITION)",
        }

        parts: list[str] = []
        total_chars = 0

        for section in template.sections:
            # Check if section heading matches any priority heading
            if not any(section.heading.startswith(ph) for ph in priority_headings):
                continue

            section_text = f"## {section.heading}\n{section.content}"
            section_len = len(section_text)

            if total_chars + section_len > max_chars:
                remaining = max_chars - total_chars
                if remaining > 100:  # Only add if meaningful content fits
                    parts.append(section_text[:remaining] + "\n[...truncated]")
                    logger.warning(
                        "SOUL prompt for role '%s' truncated at %d chars (max_chars=%d)",
                        role,
                        max_chars,
                        max_chars,
                    )
                break

            parts.append(section_text)
            total_chars += section_len

        if not parts:
            # Fallback: use Identity section raw if no priority sections matched
            for section in template.sections:
                if section.heading == "Identity":
                    return section.content[:max_chars]
            return None

        return "\n\n".join(parts)

    def get_soul_version(self, role: str) -> str | None:
        """Get SOUL template version for a role."""
        template = self.get_template(role)
        return template.version if template else None

    def list_roles(self) -> list[str]:
        """List all available SOUL roles."""
        self.load_all()
        return sorted(_soul_cache.keys())

    def get_tier_roles(self, tier: str) -> frozenset[str]:
        """Return the set of roles available at a given tier.

        Args:
            tier: One of LITE, STANDARD, PROFESSIONAL, ENTERPRISE (case-insensitive).

        Returns:
            Frozenset of role names. Returns empty set for unknown tier.
        """
        return TIER_ROLES.get(tier.upper(), frozenset())


def clear_cache() -> None:
    """Clear the SOUL template cache. Useful for testing."""
    global _soul_cache, _cache_loaded
    _soul_cache.clear()
    _cache_loaded = False
