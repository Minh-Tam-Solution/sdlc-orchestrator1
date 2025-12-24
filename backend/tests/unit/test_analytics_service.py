"""
Unit Tests - Analytics Service

SDLC Stage: 04 - BUILD
Sprint: 41 - AI Safety Foundation
Epic: EP-01/EP-02
Framework: SDLC 5.1.1

Purpose:
Unit tests for AnalyticsService covering:
1. User ID hashing (CTO Condition #1)
2. Circuit breaker pattern (CTO Condition #2)
3. Event tracking (dual approach)
4. Metrics calculation

Coverage Target: 95%+

CTO Review: Required before production deployment
"""

import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.analytics_service import (
    AnalyticsService,
    CircuitState,
    analytics_service,
)
from app.models.analytics import AnalyticsEvent


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def mock_settings():
    """Mock settings with analytics configuration."""
    with patch("app.services.analytics_service.settings") as mock_settings:
        mock_settings.MIXPANEL_TOKEN = "test-token-12345"
        mock_settings.ANALYTICS_USER_SALT = "test-salt-secret"
        mock_settings.ANALYTICS_CIRCUIT_BREAKER_THRESHOLD = 5
        mock_settings.ANALYTICS_CIRCUIT_BREAKER_TIMEOUT = 300
        yield mock_settings


@pytest.fixture
def analytics_service_instance(mock_settings):
    """Create fresh AnalyticsService instance for each test."""
    service = AnalyticsService()
    return service


@pytest.fixture
def mock_db():
    """Mock database session."""
    db = AsyncMock(spec=AsyncSession)
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.execute = AsyncMock()
    return db


# ============================================================================
# Test CTO Condition #1: User ID Hashing
# ============================================================================


def test_hash_user_id_consistency(analytics_service_instance):
    """
    Test that same user_id always produces same hash.

    CTO Condition #1: Hashing must be deterministic for Mixpanel distinct_id.
    """
    user_id = uuid4()

    hash1 = analytics_service_instance._hash_user_id(user_id)
    hash2 = analytics_service_instance._hash_user_id(user_id)

    assert hash1 == hash2, "Hash must be deterministic"
    assert len(hash1) == 16, "Hash should be truncated to 16 chars (Mixpanel limit)"
    assert isinstance(hash1, str), "Hash should be string"


def test_hash_user_id_different_users(analytics_service_instance):
    """Test that different user_ids produce different hashes."""
    user1 = uuid4()
    user2 = uuid4()

    hash1 = analytics_service_instance._hash_user_id(user1)
    hash2 = analytics_service_instance._hash_user_id(user2)

    assert hash1 != hash2, "Different users must have different hashes"


def test_hash_user_id_uses_salt(mock_settings):
    """
    Test that hashing uses ANALYTICS_USER_SALT.

    Security: Salt prevents rainbow table attacks.
    """
    user_id = uuid4()

    # Create service with salt
    service_with_salt = AnalyticsService()
    hash_with_salt = service_with_salt._hash_user_id(user_id)

    # Create service without salt
    mock_settings.ANALYTICS_USER_SALT = ""
    service_without_salt = AnalyticsService()
    hash_without_salt = service_without_salt._hash_user_id(user_id)

    # Hashes should differ (salt changes output)
    assert hash_with_salt != hash_without_salt, "Salt must affect hash output"


def test_hash_user_id_warns_if_no_salt(analytics_service_instance, caplog):
    """Test that warning is logged if ANALYTICS_USER_SALT is not configured."""
    with patch("app.services.analytics_service.settings") as mock_settings:
        mock_settings.ANALYTICS_USER_SALT = None

        service = AnalyticsService()
        user_id = uuid4()
        service._hash_user_id(user_id)

        # Check warning was logged
        assert "ANALYTICS_USER_SALT not configured" in caplog.text


# ============================================================================
# Test CTO Condition #2: Circuit Breaker Pattern
# ============================================================================


def test_circuit_breaker_initial_state_closed(analytics_service_instance):
    """Test that circuit breaker starts in CLOSED state."""
    assert analytics_service_instance._circuit_state == CircuitState.CLOSED
    assert analytics_service_instance._failure_count == 0
    assert analytics_service_instance._is_circuit_open() is False


def test_circuit_breaker_opens_after_threshold(analytics_service_instance):
    """
    Test that circuit opens after 5 consecutive failures.

    CTO Condition #2: Circuit opens at threshold to prevent cascading failures.
    """
    threshold = analytics_service_instance._threshold

    # Record failures below threshold
    for _ in range(threshold - 1):
        analytics_service_instance._record_failure()

    assert analytics_service_instance._circuit_state == CircuitState.CLOSED
    assert analytics_service_instance._is_circuit_open() is False

    # Record failure that exceeds threshold
    analytics_service_instance._record_failure()

    assert analytics_service_instance._circuit_state == CircuitState.OPEN
    assert analytics_service_instance._failure_count == threshold
    assert analytics_service_instance._is_circuit_open() is True


def test_circuit_breaker_closes_after_timeout(analytics_service_instance):
    """
    Test that circuit transitions to HALF_OPEN after timeout.

    CTO Condition #2: Auto-recovery after 300 seconds.
    """
    # Open circuit
    for _ in range(5):
        analytics_service_instance._record_failure()

    assert analytics_service_instance._circuit_state == CircuitState.OPEN

    # Simulate timeout elapsed
    analytics_service_instance._last_failure_time = datetime.utcnow() - timedelta(
        seconds=301
    )

    # Check circuit transitions to HALF_OPEN
    is_open = analytics_service_instance._is_circuit_open()

    assert is_open is False, "Circuit should allow request after timeout"
    assert (
        analytics_service_instance._circuit_state == CircuitState.HALF_OPEN
    ), "Circuit should be in HALF_OPEN state"


def test_circuit_breaker_half_open_success_closes(analytics_service_instance):
    """Test that successful request in HALF_OPEN state closes circuit."""
    # Open circuit
    for _ in range(5):
        analytics_service_instance._record_failure()

    # Transition to HALF_OPEN
    analytics_service_instance._circuit_state = CircuitState.HALF_OPEN

    # Record success
    analytics_service_instance._record_success()

    assert analytics_service_instance._circuit_state == CircuitState.CLOSED
    assert analytics_service_instance._failure_count == 0
    assert analytics_service_instance._last_failure_time is None


def test_circuit_breaker_half_open_failure_reopens(analytics_service_instance):
    """Test that failed request in HALF_OPEN state reopens circuit."""
    # Open circuit
    for _ in range(5):
        analytics_service_instance._record_failure()

    # Transition to HALF_OPEN
    analytics_service_instance._circuit_state = CircuitState.HALF_OPEN

    # Record failure
    analytics_service_instance._record_failure()

    assert analytics_service_instance._circuit_state == CircuitState.OPEN


def test_circuit_breaker_status(analytics_service_instance):
    """Test get_circuit_breaker_status() returns correct info."""
    status = analytics_service_instance.get_circuit_breaker_status()

    assert status["state"] == "closed"
    assert status["failure_count"] == 0
    assert status["threshold"] == 5
    assert status["timeout_seconds"] == 300
    assert status["last_failure_time"] is None
    assert status["seconds_until_recovery"] is None


# ============================================================================
# Test Event Tracking
# ============================================================================


@pytest.mark.asyncio
async def test_track_event_success(analytics_service_instance, mock_db):
    """Test successful event tracking to PostgreSQL + Mixpanel."""
    user_id = uuid4()
    event_name = "gate_passed"
    properties = {"gate_id": "G2"}

    with patch("app.services.analytics_service.asyncio.to_thread") as mock_mixpanel:
        mock_mixpanel.return_value = None

        success = await analytics_service_instance.track_event(
            user_id=user_id,
            event_name=event_name,
            properties=properties,
            db=mock_db,
        )

        assert success is True
        mock_db.add.assert_called_once()
        mock_db.commit.assert_awaited_once()
        mock_mixpanel.assert_awaited_once()


@pytest.mark.asyncio
async def test_track_event_stores_locally_if_mixpanel_fails(
    analytics_service_instance, mock_db
):
    """
    Test that event is stored in PostgreSQL even if Mixpanel fails.

    Dual Approach: PostgreSQL is source of truth, Mixpanel is enhancement.
    """
    user_id = uuid4()
    event_name = "gate_passed"

    # Simulate Mixpanel failure
    with patch(
        "app.services.analytics_service.asyncio.to_thread",
        side_effect=Exception("Mixpanel API error"),
    ):
        success = await analytics_service_instance.track_event(
            user_id=user_id,
            event_name=event_name,
            properties={},
            db=mock_db,
        )

        # Event should still be stored locally
        assert mock_db.add.called, "Event must be stored in PostgreSQL"
        assert (
            analytics_service_instance._failure_count == 1
        ), "Circuit breaker should record failure"


@pytest.mark.asyncio
async def test_track_event_skips_mixpanel_if_circuit_open(
    analytics_service_instance, mock_db
):
    """
    Test that Mixpanel is skipped when circuit breaker is OPEN.

    CTO Condition #2: Fallback to PostgreSQL-only mode.
    """
    user_id = uuid4()
    event_name = "gate_passed"

    # Open circuit
    for _ in range(5):
        analytics_service_instance._record_failure()

    with patch("app.services.analytics_service.asyncio.to_thread") as mock_mixpanel:
        success = await analytics_service_instance.track_event(
            user_id=user_id,
            event_name=event_name,
            properties={},
            db=mock_db,
        )

        assert success is True, "Event should succeed (stored in PostgreSQL)"
        mock_mixpanel.assert_not_called(), "Mixpanel should be skipped when circuit is OPEN"
        mock_db.add.assert_called_once(), "Event must be stored in PostgreSQL"


@pytest.mark.asyncio
async def test_track_event_without_db_session(analytics_service_instance):
    """Test that track_event works without DB session (Mixpanel-only)."""
    user_id = uuid4()
    event_name = "gate_passed"

    with patch("app.services.analytics_service.asyncio.to_thread") as mock_mixpanel:
        mock_mixpanel.return_value = None

        success = await analytics_service_instance.track_event(
            user_id=user_id,
            event_name=event_name,
            properties={},
            db=None,  # No DB session
        )

        assert success is True
        mock_mixpanel.assert_awaited_once()


@pytest.mark.asyncio
async def test_track_event_disabled_if_no_mixpanel_token(mock_db):
    """Test that analytics is disabled if MIXPANEL_TOKEN not configured."""
    with patch("app.services.analytics_service.settings") as mock_settings:
        mock_settings.MIXPANEL_TOKEN = None

        service = AnalyticsService()
        user_id = uuid4()

        success = await service.track_event(
            user_id=user_id, event_name="test", properties={}, db=mock_db
        )

        assert success is False, "Analytics should be disabled without token"


# ============================================================================
# Test Batch Event Tracking
# ============================================================================


@pytest.mark.asyncio
async def test_track_batch_events_success(analytics_service_instance, mock_db):
    """Test batch event tracking."""
    from app.schemas.analytics import EventCreate

    events = [
        EventCreate(
            user_id=uuid4(), event_name="gate_passed", properties={"gate_id": "G2"}
        ),
        EventCreate(
            user_id=uuid4(),
            event_name="evidence_uploaded",
            properties={"file_size_kb": 1024},
        ),
    ]

    with patch("app.services.analytics_service.asyncio.to_thread") as mock_mixpanel:
        mock_mixpanel.return_value = None

        success_count = await analytics_service_instance.track_batch_events(
            events=events, db=mock_db
        )

        assert success_count == 2, "Both events should succeed"
        assert mock_db.add.call_count == 2, "Both events stored in PostgreSQL"


@pytest.mark.asyncio
async def test_track_batch_events_partial_success(analytics_service_instance, mock_db):
    """Test batch event tracking with partial failures."""
    from app.schemas.analytics import EventCreate

    events = [
        EventCreate(user_id=uuid4(), event_name="event1", properties={}),
        EventCreate(user_id=uuid4(), event_name="event2", properties={}),
    ]

    # First event succeeds, second fails
    with patch(
        "app.services.analytics_service.asyncio.to_thread",
        side_effect=[None, Exception("Mixpanel error")],
    ):
        success_count = await analytics_service_instance.track_batch_events(
            events=events, db=mock_db
        )

        assert success_count == 1, "Only first event should succeed"


# ============================================================================
# Test Metrics Calculation
# ============================================================================


@pytest.mark.asyncio
async def test_get_daily_active_users(analytics_service_instance, mock_db):
    """Test DAU metrics calculation."""
    # Mock database query result
    mock_result = MagicMock()
    mock_result.all.return_value = [
        MagicMock(date="2026-01-06", dau=45),
        MagicMock(date="2026-01-07", dau=52),
    ]
    mock_db.execute.return_value = mock_result

    dau_data = await analytics_service_instance.get_daily_active_users(mock_db, days=30)

    assert "2026-01-06" in dau_data
    assert dau_data["2026-01-06"] == 45
    assert dau_data["2026-01-07"] == 52
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_ai_safety_metrics(analytics_service_instance, mock_db):
    """Test AI Safety metrics calculation."""
    # Mock events
    mock_event1 = MagicMock()
    mock_event1.properties = {
        "result": "passed",
        "duration_ms": 1000,
        "ai_tool": "claude-code",
    }

    mock_event2 = MagicMock()
    mock_event2.properties = {
        "result": "failed",
        "duration_ms": 1500,
        "ai_tool": "cursor",
    }

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_event1, mock_event2]
    mock_db.execute.return_value = mock_result

    metrics = await analytics_service_instance.get_ai_safety_metrics(mock_db, days=7)

    assert metrics["total_validations"] == 2
    assert metrics["pass_rate"] == 0.5, "1 passed / 2 total = 50%"
    assert metrics["avg_duration_ms"] == 1250, "(1000 + 1500) / 2 = 1250"
    assert "claude-code" in metrics["top_tools"]
    assert metrics["top_tools"]["claude-code"] == 1


# ============================================================================
# Test Edge Cases
# ============================================================================


def test_hash_user_id_with_none_salt(analytics_service_instance):
    """Test hashing when salt is None (should use empty string)."""
    with patch("app.services.analytics_service.settings") as mock_settings:
        mock_settings.ANALYTICS_USER_SALT = None

        service = AnalyticsService()
        user_id = uuid4()
        hash_result = service._hash_user_id(user_id)

        assert isinstance(hash_result, str)
        assert len(hash_result) == 16


@pytest.mark.asyncio
async def test_track_event_with_empty_properties(analytics_service_instance, mock_db):
    """Test event tracking with no properties."""
    user_id = uuid4()
    event_name = "user_login"

    with patch("app.services.analytics_service.asyncio.to_thread") as mock_mixpanel:
        mock_mixpanel.return_value = None

        success = await analytics_service_instance.track_event(
            user_id=user_id, event_name=event_name, properties=None, db=mock_db
        )

        assert success is True


@pytest.mark.asyncio
async def test_track_event_with_large_properties(analytics_service_instance, mock_db):
    """Test event tracking with large properties JSON."""
    user_id = uuid4()
    event_name = "test_event"
    large_properties = {f"key_{i}": f"value_{i}" for i in range(100)}

    with patch("app.services.analytics_service.asyncio.to_thread") as mock_mixpanel:
        mock_mixpanel.return_value = None

        success = await analytics_service_instance.track_event(
            user_id=user_id,
            event_name=event_name,
            properties=large_properties,
            db=mock_db,
        )

        assert success is True


# ============================================================================
# Test Singleton Instance
# ============================================================================


def test_analytics_service_singleton():
    """Test that analytics_service is a singleton instance."""
    from app.services.analytics_service import analytics_service

    assert analytics_service is not None
    assert isinstance(analytics_service, AnalyticsService)
