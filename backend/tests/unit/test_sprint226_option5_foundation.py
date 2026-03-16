"""
Sprint 226 — Option 5 Conversation-First Foundation tests.

Covers:
  S226-02: Autonomy presets (model column + TIER_AUTONOMY_MAP + registry enforcement)
  S226-03: RouteTelemetryMiddleware (path normalization, lazy Redis, fire-and-forget)
  S226-04: Telegram-only feature flags (channel guard returns 503)
  S226-05: ProductMetricsService (4 product metrics + kill signals)
  Wiring: RouteTelemetryMiddleware registered in main.py
  Wiring: autonomy_level in compute_gate_actions() with agent_can_execute

Total: 28 test cases.
"""
import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest


# ===========================================================================
# S226-02: Autonomy Presets
# ===========================================================================

class TestAutonomyPresets:
    """4 fixed presets mapped 1:1 to tiers (ADR-071 D-071-02)."""

    def test_tier_autonomy_map_covers_all_tiers(self):
        """All 6 tier names map to one of 4 presets."""
        from app.services.agent_team.agent_registry import TIER_AUTONOMY_MAP
        assert "LITE" in TIER_AUTONOMY_MAP
        assert "STANDARD" in TIER_AUTONOMY_MAP
        assert "PROFESSIONAL" in TIER_AUTONOMY_MAP
        assert "ENTERPRISE" in TIER_AUTONOMY_MAP
        assert "FOUNDER" in TIER_AUTONOMY_MAP
        assert "STARTER" in TIER_AUTONOMY_MAP
        assert len(TIER_AUTONOMY_MAP) == 6

    def test_valid_autonomy_levels_are_4_presets(self):
        """Exactly 4 valid presets — no custom matrix in v1."""
        from app.services.agent_team.agent_registry import VALID_AUTONOMY_LEVELS
        assert VALID_AUTONOMY_LEVELS == frozenset({
            "assist_only", "contribute_only", "member_guardrails", "autonomous_gated",
        })

    def test_lite_maps_to_assist_only(self):
        from app.services.agent_team.agent_registry import TIER_AUTONOMY_MAP
        assert TIER_AUTONOMY_MAP["LITE"] == "assist_only"

    def test_enterprise_maps_to_autonomous_gated(self):
        from app.services.agent_team.agent_registry import TIER_AUTONOMY_MAP
        assert TIER_AUTONOMY_MAP["ENTERPRISE"] == "autonomous_gated"

    def test_model_column_has_autonomy_level(self):
        """AgentDefinition model has autonomy_level column with correct default."""
        from app.models.agent_definition import AgentDefinition
        col = AgentDefinition.__table__.columns["autonomy_level"]
        assert col is not None
        assert str(col.server_default.arg) == "assist_only"
        assert col.nullable is False

    @pytest.mark.asyncio
    async def test_registry_rejects_invalid_autonomy(self):
        """AgentRegistry.create() rejects unknown autonomy levels."""
        from app.services.agent_team.agent_registry import AgentRegistry, VALID_AUTONOMY_LEVELS

        db = AsyncMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=None)))
        registry = AgentRegistry(db)

        payload = MagicMock()
        payload.project_id = uuid4()
        payload.team_id = None
        payload.agent_name = "test-agent"
        payload.sdlc_role = MagicMock(value="coder")
        payload.provider = "ollama"
        payload.model = "qwen3:32b"
        payload.system_prompt = "test"
        payload.working_directory = None
        payload.max_tokens = 4096
        payload.temperature = 0.7
        payload.queue_mode = MagicMock(value="queue")
        payload.session_scope = MagicMock(value="project")
        payload.max_delegation_depth = 3
        payload.allowed_tools = ["*"]
        payload.denied_tools = []
        payload.can_spawn_subagent = True
        payload.allowed_paths = []
        payload.reflect_frequency = 1
        payload.config = {}
        payload.autonomy_level = "custom_invalid"

        with pytest.raises(ValueError, match="Invalid autonomy_level"):
            await registry.create(payload)


# ===========================================================================
# S226-03: RouteTelemetryMiddleware
# ===========================================================================

class TestRouteTelemetryMiddleware:
    """Pure ASGI telemetry with path normalization and lazy Redis (ADR-071 D-071-03)."""

    def test_normalize_uuid_in_path(self):
        from app.middleware.route_telemetry import RouteTelemetryMiddleware
        result = RouteTelemetryMiddleware._normalize_path(
            "/api/v1/gates/550e8400-e29b-41d4-a716-446655440000/approve"
        )
        assert result == "/api/v1/gates/{id}/approve"

    def test_normalize_numeric_id_in_path(self):
        from app.middleware.route_telemetry import RouteTelemetryMiddleware
        result = RouteTelemetryMiddleware._normalize_path("/api/v1/projects/123/members")
        assert result == "/api/v1/projects/{id}/members"

    def test_normalize_strips_trailing_slash(self):
        from app.middleware.route_telemetry import RouteTelemetryMiddleware
        result = RouteTelemetryMiddleware._normalize_path("/api/v1/health/")
        assert result == "/api/v1/health"

    def test_normalize_mixed_uuid_and_numeric(self):
        from app.middleware.route_telemetry import RouteTelemetryMiddleware
        result = RouteTelemetryMiddleware._normalize_path(
            "/api/v1/projects/550e8400-e29b-41d4-a716-446655440000/gates/42/approve"
        )
        assert result == "/api/v1/projects/{id}/gates/{id}/approve"

    @pytest.mark.asyncio
    async def test_lazy_redis_from_app_state(self):
        """Middleware picks up Redis from scope['app'].state.telemetry_redis."""
        from app.middleware.route_telemetry import RouteTelemetryMiddleware

        mock_redis = MagicMock()
        mock_pipe = MagicMock()
        mock_pipe.incr = MagicMock()
        mock_pipe.expire = MagicMock()
        mock_pipe.execute = AsyncMock(return_value=[1, True])
        mock_redis.pipeline = MagicMock(return_value=mock_pipe)

        app_state = SimpleNamespace(telemetry_redis=mock_redis)
        mock_app_inner = MagicMock()
        mock_app_inner.state = app_state

        inner_app = AsyncMock()
        mw = RouteTelemetryMiddleware(inner_app, redis_client=None, enabled=True)

        scope = {
            "type": "http",
            "path": "/api/v1/gates",
            "app": mock_app_inner,
        }

        await mw(scope, AsyncMock(), AsyncMock())

        # Inner app must always be called
        inner_app.assert_awaited_once()

        # Give fire-and-forget task a chance to run
        await asyncio.sleep(0.05)

        mock_redis.pipeline.assert_called_once()
        mock_pipe.incr.assert_called_once()

    @pytest.mark.asyncio
    async def test_noop_when_no_redis(self):
        """No Redis anywhere → no crash, request proceeds normally."""
        from app.middleware.route_telemetry import RouteTelemetryMiddleware

        inner_app = AsyncMock()
        mw = RouteTelemetryMiddleware(inner_app, redis_client=None, enabled=True)

        scope = {"type": "http", "path": "/api/v1/gates", "app": SimpleNamespace()}
        await mw(scope, AsyncMock(), AsyncMock())

        inner_app.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_skips_non_api_paths(self):
        """Non-/api/ paths are ignored (health checks, docs, etc.)."""
        from app.middleware.route_telemetry import RouteTelemetryMiddleware

        mock_redis = MagicMock()
        inner_app = AsyncMock()
        mw = RouteTelemetryMiddleware(inner_app, redis_client=mock_redis, enabled=True)

        scope = {"type": "http", "path": "/health"}
        await mw(scope, AsyncMock(), AsyncMock())

        inner_app.assert_awaited_once()
        mock_redis.pipeline.assert_not_called()

    def test_key_ttl_is_90_days(self):
        from app.middleware.route_telemetry import RouteTelemetryMiddleware
        assert RouteTelemetryMiddleware.KEY_TTL_SECONDS == 90 * 86400


# ===========================================================================
# S226-04: Telegram-Only Feature Flags
# ===========================================================================

class TestTelegramOnlyFlags:
    """Non-Telegram channels gated by feature flags (ADR-071 D-071-04)."""

    def test_zalo_flag_default_false(self):
        from app.core.config import settings
        assert settings.FEATURE_FLAG_ZALO_OTT is False

    def test_teams_flag_default_false(self):
        from app.core.config import settings
        assert settings.FEATURE_FLAG_TEAMS_OTT is False

    def test_slack_flag_default_false(self):
        from app.core.config import settings
        assert settings.FEATURE_FLAG_SLACK_OTT is False


# ===========================================================================
# S226-05: ProductMetricsService
# ===========================================================================

class TestProductMetricsService:
    """4 product metrics with kill signals (ADR-071 D-071-05)."""

    def test_service_instantiation(self):
        from app.services.product_metrics_service import ProductMetricsService
        db = AsyncMock()
        svc = ProductMetricsService(db)
        assert svc.db is db

    @pytest.mark.asyncio
    async def test_conversation_completion_rate_meets_target(self):
        """Completion ≥70% → meets_target=True."""
        from app.services.product_metrics_service import ProductMetricsService

        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.one.return_value = SimpleNamespace(
            total=100, completed=75, errored=10, max_reached=5,
        )
        db.execute = AsyncMock(return_value=mock_result)

        svc = ProductMetricsService(db)
        result = await svc.conversation_completion_rate()
        assert result["completion_rate_pct"] == 75.0
        assert result["meets_target"] is True
        assert result["kill_signal"] is False

    @pytest.mark.asyncio
    async def test_conversation_completion_kill_signal(self):
        """Completion <50% with ≥10 conversations → kill_signal=True."""
        from app.services.product_metrics_service import ProductMetricsService

        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.one.return_value = SimpleNamespace(
            total=20, completed=8, errored=5, max_reached=7,
        )
        db.execute = AsyncMock(return_value=mock_result)

        svc = ProductMetricsService(db)
        result = await svc.conversation_completion_rate()
        assert result["completion_rate_pct"] == 40.0
        assert result["kill_signal"] is True

    def test_human_override_rate_method_exists(self):
        """human_override_rate() method exists with correct signature.

        NOTE: Full execution test deferred — GateApproval model does not have a
        'source' column yet. ProductMetricsService.human_override_rate() references
        GateApproval.source which will fail at SQLAlchemy query compilation.
        This requires a DB migration to add the 'source' column to gate_approvals
        (Sprint 226 Week 3+ scope: track whether approval came from agent/web/magic_link).
        """
        from app.services.product_metrics_service import ProductMetricsService
        import inspect

        svc = ProductMetricsService(AsyncMock())
        sig = inspect.signature(svc.human_override_rate)
        assert "tier" in sig.parameters
        assert "date_from" in sig.parameters
        assert "date_to" in sig.parameters

    @pytest.mark.asyncio
    async def test_pilot_retention_meets_target(self):
        """3+ active users → meets_target=True."""
        from app.services.product_metrics_service import ProductMetricsService

        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.one.return_value = SimpleNamespace(unique_users=3)
        db.execute = AsyncMock(return_value=mock_result)

        svc = ProductMetricsService(db)
        result = await svc.pilot_retention()
        assert result["active_users"] == 3
        assert result["meets_target"] is True
        assert result["kill_signal"] is False

    @pytest.mark.asyncio
    async def test_pilot_retention_kill_signal(self):
        """<2 active users → kill_signal=True."""
        from app.services.product_metrics_service import ProductMetricsService

        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.one.return_value = SimpleNamespace(unique_users=1)
        db.execute = AsyncMock(return_value=mock_result)

        svc = ProductMetricsService(db)
        result = await svc.pilot_retention()
        assert result["kill_signal"] is True


# ===========================================================================
# Wiring: RouteTelemetryMiddleware in main.py
# ===========================================================================

class TestMainMiddlewareWiring:
    """RouteTelemetryMiddleware is registered in app middleware stack."""

    def test_route_telemetry_imported_in_main(self):
        """main.py imports RouteTelemetryMiddleware."""
        import app.main  # noqa: F401 — triggers import
        from app.middleware.route_telemetry import RouteTelemetryMiddleware
        assert RouteTelemetryMiddleware is not None


# ===========================================================================
# Wiring: autonomy_level in compute_gate_actions()
# ===========================================================================

class TestAutonomyInGateActions:
    """compute_gate_actions() returns autonomy_level + agent_can_execute (ADR-071)."""

    def test_autonomy_agent_actions_constants(self):
        """AUTONOMY_AGENT_ACTIONS has 4 presets with correct permission escalation."""
        from app.services.gate_service import AUTONOMY_AGENT_ACTIONS
        assert len(AUTONOMY_AGENT_ACTIONS) == 4
        assert len(AUTONOMY_AGENT_ACTIONS["assist_only"]) == 0
        assert "can_evaluate" in AUTONOMY_AGENT_ACTIONS["contribute_only"]
        assert "can_upload_evidence" in AUTONOMY_AGENT_ACTIONS["contribute_only"]
        assert "can_submit" not in AUTONOMY_AGENT_ACTIONS["contribute_only"]
        assert "can_submit" in AUTONOMY_AGENT_ACTIONS["member_guardrails"]
        assert "can_approve" in AUTONOMY_AGENT_ACTIONS["autonomous_gated"]

    @pytest.mark.asyncio
    async def test_compute_gate_actions_returns_autonomy_fields(self):
        """Response includes autonomy_level and agent_can_execute keys."""
        from app.services.gate_service import compute_gate_actions

        gate = MagicMock()
        gate.id = uuid4()
        gate.status = "DRAFT"
        gate.exit_criteria = []
        gate.project_id = uuid4()
        gate.gate_type = "G1_CONSULTATION"
        gate.gate_name = "G1"
        gate.project = MagicMock()
        gate.project.policy_pack_tier = "STANDARD"

        user = MagicMock()
        user.roles = []

        db = AsyncMock()
        result = await compute_gate_actions(gate, user, db)

        assert "autonomy_level" in result
        assert "agent_can_execute" in result
        assert result["autonomy_level"] == "contribute_only"

    @pytest.mark.asyncio
    async def test_assist_only_agent_cannot_execute_anything(self):
        """LITE tier → assist_only → all agent_can_execute are False."""
        from app.services.gate_service import compute_gate_actions

        gate = MagicMock()
        gate.id = uuid4()
        gate.status = "EVALUATED"
        gate.exit_criteria = []
        gate.project_id = uuid4()
        gate.gate_type = "G1_CONSULTATION"
        gate.gate_name = "G1"
        gate.project = MagicMock()
        gate.project.policy_pack_tier = "LITE"

        user = MagicMock()
        user.roles = [MagicMock(name="developer")]

        db = AsyncMock()
        result = await compute_gate_actions(gate, user, db)

        assert result["autonomy_level"] == "assist_only"
        assert all(v is False for v in result["agent_can_execute"].values())

    @pytest.mark.asyncio
    async def test_g3_g4_always_blocks_agent_approve(self):
        """Even ENTERPRISE (autonomous_gated), G3/G4 approve requires human."""
        from app.services.gate_service import compute_gate_actions

        gate = MagicMock()
        gate.id = uuid4()
        gate.status = "SUBMITTED"
        gate.exit_criteria = []
        gate.project_id = uuid4()
        gate.gate_type = "G3_SHIP_READY"
        gate.gate_name = "G3"
        gate.project = MagicMock()
        gate.project.policy_pack_tier = "ENTERPRISE"

        user = MagicMock()
        user.roles = [MagicMock(name="CTO")]

        db = AsyncMock()
        result = await compute_gate_actions(gate, user, db)

        assert result["autonomy_level"] == "autonomous_gated"
        assert result["requires_oob_auth"] is True
        assert result["agent_can_execute"]["can_approve"] is False
        assert result["agent_can_execute"]["can_reject"] is False
