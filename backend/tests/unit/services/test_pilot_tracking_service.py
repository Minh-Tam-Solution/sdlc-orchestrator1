"""Unit tests for PilotTrackingService - Sprint 49.

PilotTrackingService is implemented with SQLAlchemy AsyncSession. These tests
remain true unit tests by using a mocked async DB session (no real Postgres
required), while still exercising the async code paths.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.models.pilot_tracking import OnboardingStage, PilotDomain, PilotParticipant, PilotSession, PilotStatus
from app.services.pilot_tracking_service import (
    PILOT_TARGET_COUNT,
    QUALITY_GATE_PASS_TARGET,
    SATISFACTION_TARGET,
    TTFV_TARGET_SECONDS,
    PilotTrackingService,
    get_pilot_tracking_service,
)


class _FakeScalars:
    def __init__(self, items):
        self._items = items

    def all(self):
        return self._items


class _FakeResult:
    def __init__(
        self,
        *,
        scalar_one_or_none=None,
        scalar_one=None,
        one_or_none=None,
        one=None,
        all_rows=None,
        scalars_items=None,
    ):
        self._scalar_one_or_none = scalar_one_or_none
        self._scalar_one = scalar_one
        self._one_or_none = one_or_none
        self._one = one
        self._all_rows = all_rows if all_rows is not None else []
        self._scalars_items = scalars_items if scalars_items is not None else []

    def scalar_one_or_none(self):
        return self._scalar_one_or_none

    def scalar_one(self):
        return self._scalar_one

    def one_or_none(self):
        return self._one_or_none

    def one(self):
        return self._one

    def all(self):
        return self._all_rows

    def scalars(self):
        return _FakeScalars(self._scalars_items)


@pytest.fixture
def mock_db():
    db = MagicMock()
    db.execute = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.flush = AsyncMock()
    db.add = MagicMock()
    return db


@pytest.fixture
def service(mock_db) -> PilotTrackingService:
    return PilotTrackingService(mock_db)


class TestConstants:
    def test_ttfv_target_is_30_minutes(self):
        assert TTFV_TARGET_SECONDS == 1800

    def test_satisfaction_target_is_8(self):
        assert SATISFACTION_TARGET == 8

    def test_quality_gate_target_is_95_percent(self):
        assert QUALITY_GATE_PASS_TARGET == 0.95

    def test_pilot_target_is_10_participants(self):
        assert PILOT_TARGET_COUNT == 10


class TestParticipantManagement:
    @pytest.mark.asyncio
    async def test_register_new_participant(self, service: PilotTrackingService, mock_db):
        user_id = uuid4()
        mock_db.execute.return_value = _FakeResult(scalar_one_or_none=None)

        participant = await service.register_participant(
            user_id=user_id,
            domain=PilotDomain.FNB.value,
            company_name="Test Restaurant",
            company_size="small",
            referral_source="nqh_network",
        )

        assert participant.user_id == user_id
        assert participant.status == PilotStatus.REGISTERED.value
        assert participant.domain == PilotDomain.FNB.value
        mock_db.add.assert_called_once()
        mock_db.commit.assert_awaited()
        mock_db.refresh.assert_awaited()

    @pytest.mark.asyncio
    async def test_register_existing_participant_returns_existing(self, service: PilotTrackingService, mock_db):
        existing = PilotParticipant(id=uuid4(), user_id=uuid4())
        mock_db.execute.return_value = _FakeResult(scalar_one_or_none=existing)

        result = await service.register_participant(user_id=existing.user_id)
        assert result is existing
        mock_db.add.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_participant_by_user_id(self, service: PilotTrackingService, mock_db):
        participant = PilotParticipant(id=uuid4(), user_id=uuid4())
        mock_db.execute.return_value = _FakeResult(scalar_one_or_none=participant)

        result = await service.get_participant(participant.user_id)
        assert result is participant

    @pytest.mark.asyncio
    async def test_get_participant_not_found_returns_none(self, service: PilotTrackingService, mock_db):
        mock_db.execute.return_value = _FakeResult(scalar_one_or_none=None)
        result = await service.get_participant(uuid4())
        assert result is None


class TestParticipantStatus:
    @pytest.mark.asyncio
    async def test_update_status_to_active_sets_activated_at(self, service: PilotTrackingService, mock_db):
        participant = PilotParticipant(id=uuid4(), user_id=uuid4(), status=PilotStatus.REGISTERED.value)
        service.get_participant_by_id = AsyncMock(return_value=participant)

        updated = await service.update_participant_status(participant.id, PilotStatus.ACTIVE)
        assert updated is participant
        assert updated.status == PilotStatus.ACTIVE.value
        assert updated.activated_at is not None
        mock_db.commit.assert_awaited()
        mock_db.refresh.assert_awaited()

    @pytest.mark.asyncio
    async def test_update_status_not_found_returns_none(self, service: PilotTrackingService, mock_db):
        service.get_participant_by_id = AsyncMock(return_value=None)
        updated = await service.update_participant_status(uuid4(), PilotStatus.ACTIVE)
        assert updated is None
        mock_db.commit.assert_not_awaited()


class TestListParticipants:
    @pytest.mark.asyncio
    async def test_list_all_participants(self, service: PilotTrackingService, mock_db):
        p1 = PilotParticipant(id=uuid4(), user_id=uuid4())
        p2 = PilotParticipant(id=uuid4(), user_id=uuid4())
        mock_db.execute.return_value = _FakeResult(scalars_items=[p1, p2])

        participants = await service.list_participants(limit=100)
        assert participants == [p1, p2]

    @pytest.mark.asyncio
    async def test_list_participants_with_filters(self, service: PilotTrackingService, mock_db):
        p = PilotParticipant(id=uuid4(), user_id=uuid4(), status=PilotStatus.ACTIVE.value, domain=PilotDomain.FNB.value)
        mock_db.execute.return_value = _FakeResult(scalars_items=[p])

        participants = await service.list_participants(status=PilotStatus.ACTIVE, domain=PilotDomain.FNB)
        assert len(participants) == 1
        assert participants[0].status == PilotStatus.ACTIVE.value
        assert participants[0].domain == PilotDomain.FNB.value


class TestSessionLifecycle:
    @pytest.mark.asyncio
    async def test_start_session_creates_session_and_increments_count(self, service: PilotTrackingService, mock_db):
        participant = PilotParticipant(id=uuid4(), user_id=uuid4(), total_sessions=0)
        service.get_participant_by_id = AsyncMock(return_value=participant)

        # start_session doesn't execute any selects; it only adds+commit+refresh and then calls get_participant_by_id
        session = await service.start_session(participant_id=participant.id)

        assert session.participant_id == participant.id
        assert session.current_stage == OnboardingStage.STARTED.value
        assert session.stage_history and session.stage_history[0]["stage"] == OnboardingStage.STARTED.value
        assert participant.total_sessions == 1
        mock_db.add.assert_called_once()
        mock_db.commit.assert_awaited()
        mock_db.refresh.assert_awaited()

    @pytest.mark.asyncio
    async def test_update_stage_sets_timestamp_and_history(self, service: PilotTrackingService, mock_db):
        session = PilotSession(
            id=uuid4(),
            participant_id=uuid4(),
            onboarding_session_id=str(uuid4()),
            started_at=datetime.now(timezone.utc),
            current_stage=OnboardingStage.STARTED.value,
            stage_history=[],
        )
        mock_db.execute.return_value = _FakeResult(scalar_one_or_none=session)

        updated = await service.update_session_stage(
            session_id=session.id,
            stage=OnboardingStage.APP_NAMED,
            metadata={"app_name": "My App"},
        )

        assert updated is session
        assert session.current_stage == OnboardingStage.APP_NAMED.value
        assert session.app_named_at is not None
        assert session.stage_history[-1]["stage"] == OnboardingStage.APP_NAMED.value
        mock_db.commit.assert_awaited()
        mock_db.refresh.assert_awaited()

    @pytest.mark.asyncio
    async def test_quality_gate_passed_calls_participant_update(self, service: PilotTrackingService, mock_db):
        session = PilotSession(
            id=uuid4(),
            participant_id=uuid4(),
            onboarding_session_id=str(uuid4()),
            started_at=datetime.now(timezone.utc) - timedelta(minutes=10),
            current_stage=OnboardingStage.STARTED.value,
            stage_history=[],
        )
        mock_db.execute.return_value = _FakeResult(scalar_one_or_none=session)
        service._update_participant_on_completion = AsyncMock()

        updated = await service.update_session_stage(session_id=session.id, stage=OnboardingStage.QUALITY_GATE_PASSED)

        assert updated is session
        assert session.quality_gate_passed_at is not None
        assert session.ttfv_seconds is not None
        assert session.completed_at is not None
        service._update_participant_on_completion.assert_awaited_once()


class TestGenerationAndErrors:
    @pytest.mark.asyncio
    async def test_record_generation_result_quality_gate_passed_delegates_to_stage_update(
        self, service: PilotTrackingService, mock_db
    ):
        session = PilotSession(
            id=uuid4(),
            participant_id=uuid4(),
            onboarding_session_id=str(uuid4()),
            started_at=datetime.now(timezone.utc),
            current_stage=OnboardingStage.STARTED.value,
            stage_history=[],
        )
        service.get_session = AsyncMock(return_value=session)
        service.update_session_stage = AsyncMock(return_value=session)

        result = await service.record_generation_result(
            session_id=session.id,
            provider="ollama",
            generation_time_ms=5000,
            tokens_used=1500,
            files_generated=10,
            lines_of_code=500,
            quality_gate_passed=True,
            quality_gate_score=95.5,
            quality_gate_details={"syntax": "pass", "security": "pass"},
        )

        assert result is session
        mock_db.flush.assert_awaited()
        service.update_session_stage.assert_awaited()

    @pytest.mark.asyncio
    async def test_record_generation_result_not_found_returns_none(self, service: PilotTrackingService):
        service.get_session = AsyncMock(return_value=None)
        result = await service.record_generation_result(
            session_id=uuid4(),
            provider="ollama",
            generation_time_ms=5000,
            tokens_used=1500,
            files_generated=10,
            lines_of_code=500,
            quality_gate_passed=True,
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_record_session_error_increments_count(self, service: PilotTrackingService, mock_db):
        session = PilotSession(
            id=uuid4(),
            participant_id=uuid4(),
            onboarding_session_id=str(uuid4()),
            started_at=datetime.now(timezone.utc),
            current_stage=OnboardingStage.STARTED.value,
            stage_history=[],
            errors=[],
            error_count=0,
        )
        service.get_session = AsyncMock(return_value=session)

        updated = await service.record_session_error(
            session_id=session.id,
            error={"type": "generation_failed", "message": "Ollama timeout"},
        )

        assert updated is session
        assert session.error_count == 1
        assert session.errors[-1]["type"] == "generation_failed"
        mock_db.commit.assert_awaited()


class TestSatisfactionSurvey:
    @pytest.mark.asyncio
    async def test_submit_survey_updates_participant(self, service: PilotTrackingService, mock_db):
        participant = PilotParticipant(id=uuid4(), user_id=uuid4())
        service.get_participant_by_id = AsyncMock(return_value=participant)

        survey = await service.submit_satisfaction_survey(
            participant_id=participant.id,
            session_id=None,
            overall_score=9,
            would_recommend=True,
            ease_of_use_score=8,
            code_quality_score=9,
            speed_score=10,
            what_went_well="Rất nhanh và tiện lợi",
            what_needs_improvement="Thêm template cho quán cafe",
        )

        assert survey.overall_score == 9
        assert participant.latest_satisfaction_score == 9
        assert participant.would_recommend is True
        mock_db.add.assert_called_once()
        mock_db.commit.assert_awaited()


class TestPilotSummary:
    @pytest.mark.asyncio
    async def test_get_pilot_summary_structure_and_targets(self, service: PilotTrackingService, mock_db):
        # get_pilot_summary makes multiple db.execute() calls; provide deterministic empty values.
        mock_db.execute.side_effect = [
            _FakeResult(scalar_one=0),  # total_participants
            _FakeResult(scalar_one=0),  # active_participants
            _FakeResult(scalar_one=0),  # total_sessions
            _FakeResult(scalar_one=0),  # completed_sessions
            _FakeResult(one_or_none=None),  # ttfv_stats_row
            _FakeResult(scalar_one=0),  # ttfv_target_met
            _FakeResult(one=SimpleNamespace(total=0, passed=0)),  # quality_stats_row
            _FakeResult(scalar_one=0),  # satisfaction_avg
            _FakeResult(scalar_one=0),  # recommend_count
            _FakeResult(all_rows=[]),  # domain_stats
        ]

        summary = await service.get_pilot_summary()

        assert "summary" in summary
        assert "ttfv" in summary
        assert "quality" in summary
        assert "satisfaction" in summary
        assert "domains" in summary
        assert "overall_status" in summary
        assert "generated_at" in summary

        assert summary["summary"]["participants"]["target"] == PILOT_TARGET_COUNT
        assert summary["ttfv"]["target_seconds"] == TTFV_TARGET_SECONDS
        assert summary["quality"]["target_percent"] == QUALITY_GATE_PASS_TARGET * 100
        assert summary["satisfaction"]["target"] == SATISFACTION_TARGET


class TestOverallStatusCalculation:
    def test_excellent_status_all_targets_met(self, service: PilotTrackingService):
        status = service._calculate_overall_status(
            participants=10,
            ttfv_p90=1500,
            quality_rate=96,
            satisfaction=8.5,
        )
        assert status == "excellent"

    def test_on_track_status_most_targets_met(self, service: PilotTrackingService):
        status = service._calculate_overall_status(
            participants=8,
            ttfv_p90=1600,
            quality_rate=94,
            satisfaction=8.0,
        )
        assert status == "on_track"

    def test_needs_attention_status_some_targets_missed(self, service: PilotTrackingService):
        status = service._calculate_overall_status(
            participants=5,
            ttfv_p90=2500,
            quality_rate=86,
            satisfaction=7.5,
        )
        assert status == "needs_attention"

    def test_at_risk_status_most_targets_missed(self, service: PilotTrackingService):
        status = service._calculate_overall_status(
            participants=2,
            ttfv_p90=3000,
            quality_rate=70,
            satisfaction=5.0,
        )
        assert status == "at_risk"


class TestModelTTFV:
    def test_calculate_ttfv_none_if_no_quality_gate_passed(self):
        session = PilotSession(
            id=uuid4(),
            participant_id=uuid4(),
            onboarding_session_id=str(uuid4()),
            started_at=datetime.now(timezone.utc),
            current_stage=OnboardingStage.STARTED.value,
            stage_history=[],
        )
        assert session.calculate_ttfv() is None

    def test_calculate_ttfv_seconds(self):
        start = datetime.now(timezone.utc) - timedelta(minutes=5)
        session = PilotSession(
            id=uuid4(),
            participant_id=uuid4(),
            onboarding_session_id=str(uuid4()),
            started_at=start,
            current_stage=OnboardingStage.QUALITY_GATE_PASSED.value,
            stage_history=[],
            quality_gate_passed_at=datetime.now(timezone.utc),
        )

        ttfv = session.calculate_ttfv()
        assert ttfv is not None
        assert 0 < ttfv <= 600

    def test_update_ttfv_sets_target_met_true_under_30_min(self):
        session = PilotSession(
            id=uuid4(),
            participant_id=uuid4(),
            onboarding_session_id=str(uuid4()),
            started_at=datetime.now(timezone.utc) - timedelta(minutes=25),
            current_stage=OnboardingStage.QUALITY_GATE_PASSED.value,
            stage_history=[],
            quality_gate_passed_at=datetime.now(timezone.utc),
        )

        session.update_ttfv()
        assert session.ttfv_target_met is True

    def test_update_ttfv_sets_target_met_false_over_30_min(self):
        session = PilotSession(
            id=uuid4(),
            participant_id=uuid4(),
            onboarding_session_id=str(uuid4()),
            started_at=datetime.now(timezone.utc) - timedelta(minutes=35),
            current_stage=OnboardingStage.QUALITY_GATE_PASSED.value,
            stage_history=[],
            quality_gate_passed_at=datetime.now(timezone.utc),
        )

        session.update_ttfv()
        assert session.ttfv_target_met is False


class TestFactoryFunction:
    def test_get_pilot_tracking_service(self):
        db = MagicMock()
        svc = get_pilot_tracking_service(db)
        assert isinstance(svc, PilotTrackingService)
