"""
Unit Tests for TeamCharterLoader — Sprint 225 (SOUL Template Integration).

Tests:
- load_all parses 10 TEAM charters from Framework submodule
- Parse leader_role correctly from markdown
- Parse member_roles from table
- Fallback when path doesn't exist

Zero Mock Policy: Tests use real TEAM charter files from Framework submodule
"""

import pytest
from pathlib import Path

from app.services.agent_team.team_charter_loader import (
    TeamCharterLoader,
    TeamCharter,
    clear_charter_cache,
)


_REPO_ROOT = Path(__file__).resolve().parents[3]
_TEAMS_PATH = _REPO_ROOT / "SDLC-Enterprise-Framework" / "05-Templates-Tools" / "04-SASE-Artifacts" / "teams"


@pytest.fixture(autouse=True)
def reset_cache():
    """Reset TEAM charter cache before each test."""
    clear_charter_cache()
    yield
    clear_charter_cache()


def _has_team_files() -> bool:
    return _TEAMS_PATH.exists() and any(_TEAMS_PATH.glob("TEAM-*.md"))


pytestmark = pytest.mark.skipif(
    not _has_team_files(),
    reason="Framework submodule not initialized — TEAM files not available",
)


class TestLoadAll:
    """Tests for TeamCharterLoader.load_all()."""

    def test_loads_10_charters(self):
        """Framework 6.1.2 has exactly 10 TEAM charters."""
        loader = TeamCharterLoader(teams_path=_TEAMS_PATH)
        charters = loader.load_all()
        assert len(charters) == 10

    def test_all_teams_present(self):
        loader = TeamCharterLoader(teams_path=_TEAMS_PATH)
        charters = loader.load_all()
        expected_teams = {
            "advisory", "business", "design", "dev", "engineering",
            "executive", "fullstack", "ops", "planning", "qa",
        }
        assert set(charters.keys()) == expected_teams

    def test_charters_have_correct_type(self):
        loader = TeamCharterLoader(teams_path=_TEAMS_PATH)
        charters = loader.load_all()
        for name, charter in charters.items():
            assert isinstance(charter, TeamCharter), f"Team '{name}' is not TeamCharter"


class TestParseLeaderRole:
    """Tests for leader role extraction."""

    def test_dev_team_leader_is_coder(self):
        loader = TeamCharterLoader(teams_path=_TEAMS_PATH)
        charter = loader.load_team("dev")
        assert charter is not None
        assert charter.leader_role == "coder"

    def test_qa_team_has_leader(self):
        loader = TeamCharterLoader(teams_path=_TEAMS_PATH)
        charter = loader.load_team("qa")
        assert charter is not None
        assert charter.leader_role  # Should have a leader


class TestParseMemberRoles:
    """Tests for member roles extraction from table."""

    def test_dev_team_has_members(self):
        loader = TeamCharterLoader(teams_path=_TEAMS_PATH)
        charter = loader.load_team("dev")
        assert charter is not None
        assert len(charter.member_roles) >= 1
        assert "coder" in charter.member_roles

    def test_member_roles_are_strings(self):
        loader = TeamCharterLoader(teams_path=_TEAMS_PATH)
        for name in loader.list_teams():
            charter = loader.load_team(name)
            for role in charter.member_roles:
                assert isinstance(role, str)


class TestMission:
    """Tests for mission extraction."""

    def test_dev_team_has_mission(self):
        loader = TeamCharterLoader(teams_path=_TEAMS_PATH)
        charter = loader.load_team("dev")
        assert charter is not None
        assert charter.mission  # Should have non-empty mission


class TestFallbackPath:
    """Tests for graceful fallback when path doesn't exist."""

    def test_missing_path_returns_empty(self):
        loader = TeamCharterLoader(teams_path=Path("/nonexistent/path"))
        charters = loader.load_all()
        assert charters == {}

    def test_missing_team_returns_none(self):
        loader = TeamCharterLoader(teams_path=Path("/nonexistent/path"))
        charter = loader.load_team("dev")
        assert charter is None


class TestCache:
    """Tests for caching behavior."""

    def test_load_all_caches_results(self):
        loader = TeamCharterLoader(teams_path=_TEAMS_PATH)
        charters1 = loader.load_all()
        charters2 = loader.load_all()
        assert charters1 == charters2

    def test_clear_cache_resets(self):
        loader = TeamCharterLoader(teams_path=_TEAMS_PATH)
        loader.load_all()
        clear_charter_cache()
        teams = loader.list_teams()
        assert len(teams) == 10
