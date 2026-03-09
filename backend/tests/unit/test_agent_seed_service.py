"""
Unit Tests for AgentSeedService — Sprint 225 (SOUL Template Integration).

Tests:
- Seeds correct number of agents per tier (LITE=3, STANDARD=6, PRO=10, ENTERPRISE=13)
- Backward compatibility: tier=None seeds all 12 original core roles
- SOUL prompt used when available, fallback otherwise
- SE4H and Support roles get restricted permissions
- Optional roles never auto-seeded
- soul_version stored in config JSONB
- Fullstack gets low temperature (0.3)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from app.services.agent_team.agent_seed_service import (
    AgentSeedService,
    _CORE_ROLES,
    _ROLE_PROMPTS,
)
from app.services.agent_team.config import ROLE_MODEL_DEFAULTS
from app.services.agent_team.soul_loader import TIER_ROLES, OPTIONAL_ROLES


@pytest.fixture
def db():
    """Create a mock async DB session."""
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.all.return_value = []
    mock_db.execute.return_value = mock_result
    return mock_db


class TestBackwardCompatibility:
    """CTO R4: tier=None seeds all 12 original core roles."""

    @pytest.mark.asyncio
    async def test_tier_none_seeds_12_core_roles(self, db):
        """tier=None seeds exactly 12 core roles (pre-Sprint 225 behavior)."""
        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(uuid4())

        assert len(created) == 12
        roles = {d.sdlc_role for d in created}
        assert roles == _CORE_ROLES

    @pytest.mark.asyncio
    async def test_optional_roles_never_auto_seeded(self, db):
        """Optional roles (writer, sales, cs, itadmin) never appear in any tier."""
        svc = AgentSeedService(db)
        for tier in ["LITE", "STANDARD", "PROFESSIONAL", "ENTERPRISE", None]:
            mock_result = MagicMock()
            mock_result.all.return_value = []
            db.execute.return_value = mock_result
            db.flush.reset_mock()

            created = await svc.seed_project_agents(uuid4(), tier=tier)
            roles = {d.sdlc_role for d in created}
            for optional in OPTIONAL_ROLES:
                assert optional not in roles, (
                    f"Optional role '{optional}' should not be auto-seeded for tier={tier}"
                )


class TestTierFiltering:
    """Tier-based role filtering per SDLC 6.1.2 matrix."""

    @pytest.mark.asyncio
    async def test_lite_seeds_3_roles(self, db):
        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(uuid4(), tier="LITE")
        assert len(created) == 3
        roles = {d.sdlc_role for d in created}
        assert roles == {"assistant", "coder", "tester"}

    @pytest.mark.asyncio
    async def test_standard_seeds_6_roles(self, db):
        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(uuid4(), tier="STANDARD")
        assert len(created) == 6

    @pytest.mark.asyncio
    async def test_professional_seeds_10_roles(self, db):
        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(uuid4(), tier="PROFESSIONAL")
        assert len(created) == 10
        roles = {d.sdlc_role for d in created}
        assert "fullstack" in roles
        assert "devops" in roles
        assert "pjm" in roles
        assert "researcher" in roles

    @pytest.mark.asyncio
    async def test_enterprise_seeds_13_roles(self, db):
        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(uuid4(), tier="ENTERPRISE")
        assert len(created) == 13
        roles = {d.sdlc_role for d in created}
        assert "ceo" in roles
        assert "cpo" in roles
        assert "cto" in roles

    @pytest.mark.asyncio
    async def test_tier_case_insensitive(self, db):
        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(uuid4(), tier="lite")
        assert len(created) == 3

    @pytest.mark.asyncio
    async def test_unknown_tier_falls_back_to_core(self, db):
        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(uuid4(), tier="UNKNOWN")
        assert len(created) == 12


class TestSOULIntegration:
    """SOUL template loading into system_prompt."""

    @pytest.mark.asyncio
    async def test_soul_prompt_used_when_available(self, db):
        """When SOUL template exists, system_prompt contains SOUL content."""
        svc = AgentSeedService(db)
        with patch.object(
            svc._soul_loader, "get_system_prompt", return_value="## Identity\nYou are a test coder."
        ), patch.object(
            svc._soul_loader, "get_soul_version", return_value="1.0.0"
        ):
            created = await svc.seed_project_agents(uuid4())
            coder = next(d for d in created if d.sdlc_role == "coder")
            assert "Identity" in coder.system_prompt
            assert coder.config["soul_source"] == "framework"
            assert coder.config["soul_version"] == "1.0.0"

    @pytest.mark.asyncio
    async def test_fallback_prompt_when_no_soul(self, db):
        """When SOUL template missing, uses basic fallback prompt."""
        svc = AgentSeedService(db)
        with patch.object(
            svc._soul_loader, "get_system_prompt", return_value=None
        ), patch.object(
            svc._soul_loader, "get_soul_version", return_value=None
        ):
            created = await svc.seed_project_agents(uuid4())
            coder = next(d for d in created if d.sdlc_role == "coder")
            assert coder.system_prompt == _ROLE_PROMPTS["coder"]
            assert coder.config["soul_source"] == "fallback"


class TestPermissions:
    """Role permission assignment."""

    @pytest.mark.asyncio
    async def test_se4h_roles_restricted(self, db):
        """SE4H roles (ceo, cpo, cto) get read-only permissions."""
        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(uuid4(), tier="ENTERPRISE")

        for defn in created:
            if defn.sdlc_role in ("ceo", "cpo", "cto"):
                assert defn.max_delegation_depth == 0
                assert defn.can_spawn_subagent is False
                assert "write_file" in defn.denied_tools
                assert defn.allowed_tools == ["read_file", "search", "analyze"]

    @pytest.mark.asyncio
    async def test_se4a_roles_full_permissions(self, db):
        """SE4A roles get full executor permissions."""
        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(uuid4(), tier="PROFESSIONAL")

        for defn in created:
            if defn.sdlc_role in ("coder", "architect", "fullstack"):
                assert defn.allowed_tools == ["*"]
                assert defn.denied_tools == []
                assert defn.max_delegation_depth == 1

    @pytest.mark.asyncio
    async def test_fullstack_low_temperature(self, db):
        """Fullstack gets temperature 0.3 like coder/reviewer/tester."""
        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(uuid4(), tier="PROFESSIONAL")

        fullstack = next(d for d in created if d.sdlc_role == "fullstack")
        assert fullstack.temperature == 0.3


class TestSkipExisting:
    """Existing role skip behavior."""

    @pytest.mark.asyncio
    async def test_skips_existing_roles(self, db):
        mock_result = MagicMock()
        mock_result.all.return_value = [("coder",), ("reviewer",)]
        db.execute.return_value = mock_result

        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(uuid4())

        roles = {d.sdlc_role for d in created}
        assert "coder" not in roles
        assert "reviewer" not in roles
        assert len(created) == 10

    @pytest.mark.asyncio
    async def test_skip_existing_false_seeds_all(self, db):
        mock_result = MagicMock()
        mock_result.all.return_value = [("coder",)]
        db.execute.return_value = mock_result

        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(uuid4(), skip_existing=False)
        assert len(created) == 12

    @pytest.mark.asyncio
    async def test_binds_project_and_team(self, db):
        project_id = uuid4()
        team_id = uuid4()

        svc = AgentSeedService(db)
        created = await svc.seed_project_agents(project_id, team_id=team_id)

        for defn in created:
            assert defn.project_id == project_id
            assert defn.team_id == team_id

    @pytest.mark.asyncio
    async def test_flush_called_when_created(self, db):
        svc = AgentSeedService(db)
        await svc.seed_project_agents(uuid4())
        db.flush.assert_awaited_once()
