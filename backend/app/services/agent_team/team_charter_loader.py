"""
=========================================================================
TEAM Charter Loader — Sprint 225 (SOUL Template Integration)
SDLC Orchestrator - Framework 6.1.2 Integration

Version: 1.0.0
Date: March 2026
Status: ACTIVE - Sprint 225
Authority: CTO Approved (Sprint 225 Plan)
Reference: SDLC-Enterprise-Framework/05-Templates-Tools/04-SASE-Artifacts/teams/

Purpose:
- Load TEAM charter markdown files from Framework submodule
- Parse YAML frontmatter + markdown sections
- Extract team metadata (name, archetype, mission, leader, members)
- Cache parsed charters in memory
- Enable team preset enrichment with charter data

Zero Mock Policy: Production-ready loader with graceful fallback
=========================================================================
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from app.services.agent_team.soul_loader import _parse_frontmatter, _parse_sections

logger = logging.getLogger(__name__)


# =========================================================================
# Data Classes
# =========================================================================


@dataclass(frozen=True)
class TeamCharter:
    """Parsed TEAM charter with metadata and sections."""

    team: str
    archetype: str
    version: str
    sdlc_framework: str
    mission: str
    leader_role: str
    member_roles: list[str] = field(default_factory=list)
    raw_frontmatter: dict = field(default_factory=dict)


# =========================================================================
# Module-level cache
# =========================================================================

_charter_cache: dict[str, TeamCharter] = {}
_charter_cache_loaded: bool = False


# =========================================================================
# TeamCharterLoader
# =========================================================================


def _default_teams_path() -> Path:
    """Resolve default path to TEAM charters via Framework submodule."""
    from app.core.config import settings

    repo_root = Path(__file__).resolve().parents[4]
    return repo_root / settings.FRAMEWORK_SUBMODULE_PATH / "05-Templates-Tools" / "04-SASE-Artifacts" / "teams"


class TeamCharterLoader:
    """Loads and caches TEAM charter files from Framework submodule.

    Usage:
        loader = TeamCharterLoader()
        charters = loader.load_all()
        dev_team = loader.load_team("dev")
    """

    def __init__(self, teams_path: Path | None = None) -> None:
        self._teams_path = teams_path

    @property
    def teams_path(self) -> Path:
        if self._teams_path is None:
            self._teams_path = _default_teams_path()
        return self._teams_path

    def load_all(self) -> dict[str, TeamCharter]:
        """Scan and parse all TEAM-*.md files. Results are cached.

        Returns:
            Dict mapping team name → TeamCharter.
        """
        global _charter_cache, _charter_cache_loaded

        if _charter_cache_loaded:
            return dict(_charter_cache)

        path = self.teams_path
        if not path.exists():
            logger.warning(
                "TEAM charters directory not found: %s — team presets will use defaults",
                path,
            )
            _charter_cache_loaded = True
            return {}

        team_files = sorted(path.glob("TEAM-*.md"))
        if not team_files:
            logger.warning("No TEAM-*.md files found in %s", path)
            _charter_cache_loaded = True
            return {}

        for team_file in team_files:
            try:
                raw = team_file.read_text(encoding="utf-8")
                frontmatter, markdown = _parse_frontmatter(raw)
                _title, sections = _parse_sections(markdown)

                team_name = frontmatter.get("team", "")
                if not team_name:
                    team_name = team_file.stem.replace("TEAM-", "").lower()

                # Extract mission from ## Mission section
                mission = ""
                leader_role = ""
                member_roles: list[str] = []

                for section in sections:
                    if section.heading == "Mission":
                        mission = section.content.strip()

                    elif section.heading == "Leader":
                        # Parse "**@coder** — Owns..." → "coder"
                        leader_line = section.content.strip().split("\n")[0]
                        if "@" in leader_line:
                            start = leader_line.index("@") + 1
                            end = leader_line.find("*", start)
                            if end == -1:
                                end = leader_line.find(" ", start)
                            if end == -1:
                                end = len(leader_line)
                            leader_role = leader_line[start:end].strip()

                    elif section.heading == "Members":
                        # Parse table rows: | @coder | ... |
                        for line in section.content.split("\n"):
                            line = line.strip()
                            if line.startswith("|") and "@" in line:
                                cells = [c.strip() for c in line.split("|")]
                                for cell in cells:
                                    if cell.startswith("@"):
                                        role = cell[1:].strip()
                                        if role and role not in member_roles:
                                            member_roles.append(role)

                charter = TeamCharter(
                    team=team_name,
                    archetype=frontmatter.get("archetype", ""),
                    version=frontmatter.get("version", "1.0.0"),
                    sdlc_framework=frontmatter.get("sdlc_framework", ""),
                    mission=mission,
                    leader_role=leader_role,
                    member_roles=member_roles,
                    raw_frontmatter=frontmatter,
                )
                _charter_cache[team_name] = charter

            except Exception as e:
                logger.error("Failed to parse TEAM charter %s: %s", team_file.name, e)

        _charter_cache_loaded = True
        logger.info(
            "Loaded %d TEAM charters from %s (teams: %s)",
            len(_charter_cache),
            path,
            ", ".join(sorted(_charter_cache.keys())),
        )

        return dict(_charter_cache)

    def load_team(self, name: str) -> TeamCharter | None:
        """Get a specific team charter by name.

        Args:
            name: Team name (e.g. "dev", "qa", "ops").

        Returns:
            TeamCharter or None if not found.
        """
        self.load_all()
        return _charter_cache.get(name)

    def list_teams(self) -> list[str]:
        """List all available team names."""
        self.load_all()
        return sorted(_charter_cache.keys())


def clear_charter_cache() -> None:
    """Clear the TEAM charter cache. Useful for testing."""
    global _charter_cache, _charter_cache_loaded
    _charter_cache.clear()
    _charter_cache_loaded = False
