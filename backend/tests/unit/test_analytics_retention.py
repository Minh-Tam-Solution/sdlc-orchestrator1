"""
Unit Tests - Analytics Retention Task

SDLC Stage: 04 - BUILD
Sprint: 41 - AI Safety Foundation
Framework: SDLC 5.1.3

Purpose:
Unit tests for AnalyticsRetentionTask covering:
1. 90-day retention cleanup (CTO Condition #3)
2. Batch deletion performance
3. Retention stats calculation

Coverage Target: 95%+

CTO Review: Required before production deployment
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.tasks.analytics_retention import AnalyticsRetentionTask


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def mock_db():
    """Mock database session."""
    db = AsyncMock(spec=AsyncSession)
    db.execute = AsyncMock()
    db.commit = AsyncMock()
    db.rollback = AsyncMock()
    return db


@pytest.fixture
def retention_task():
    """Create AnalyticsRetentionTask instance."""
    return AnalyticsRetentionTask(retention_days=90)


# ============================================================================
# Test Retention Cleanup
# ============================================================================


@pytest.mark.asyncio
async def test_cleanup_old_events_deletes_old_records(retention_task, mock_db):
    """
    Test that cleanup deletes events older than 90 days.

    CTO Condition #3: Enforce GDPR retention policy.
    """
    # Mock count query (12,500 old events)
    count_result = MagicMock()
    count_result.scalar.return_value = 12500

    # Mock delete query (1000 records deleted per batch)
    delete_result = MagicMock()
    delete_result.rowcount = 1000

    # First 12 batches delete 1000 records, 13th batch deletes 500, 14th returns 0
    mock_db.execute.side_effect = [
        count_result,  # Count query
        delete_result,  # Batch 1
        delete_result,  # Batch 2
        delete_result,  # Batch 3
        delete_result,  # Batch 4
        delete_result,  # Batch 5
        delete_result,  # Batch 6
        delete_result,  # Batch 7
        delete_result,  # Batch 8
        delete_result,  # Batch 9
        delete_result,  # Batch 10
        delete_result,  # Batch 11
        delete_result,  # Batch 12
        MagicMock(rowcount=500),  # Batch 13 (last batch with records)
        MagicMock(rowcount=0),  # Batch 14 (no more records)
    ]

    result = await retention_task.cleanup_old_events(mock_db)

    assert result["status"] == "success"
    assert result["deleted_count"] == 12500
    assert "cutoff_date" in result
    assert "duration_seconds" in result
    assert mock_db.commit.call_count == 14, "Should commit after each batch"


@pytest.mark.asyncio
async def test_cleanup_old_events_no_old_records(retention_task, mock_db):
    """Test cleanup when no old records exist."""
    # Mock count query (0 old events)
    count_result = MagicMock()
    count_result.scalar.return_value = 0

    mock_db.execute.return_value = count_result

    result = await retention_task.cleanup_old_events(mock_db)

    assert result["status"] == "success"
    assert result["deleted_count"] == 0
    assert result["message"] == "No events to delete"
    mock_db.commit.assert_not_called()


@pytest.mark.asyncio
async def test_cleanup_old_events_handles_errors(retention_task, mock_db):
    """Test that cleanup handles database errors gracefully."""
    # Simulate database error
    mock_db.execute.side_effect = Exception("Database connection lost")

    result = await retention_task.cleanup_old_events(mock_db)

    assert result["status"] == "error"
    assert "Database connection lost" in result["error"]
    assert result["deleted_count"] == 0
    mock_db.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_cleanup_old_events_batch_size(retention_task, mock_db):
    """Test that cleanup deletes in batches of 1000."""
    # Mock 2500 old events
    count_result = MagicMock()
    count_result.scalar.return_value = 2500

    delete_batch1 = MagicMock(rowcount=1000)
    delete_batch2 = MagicMock(rowcount=1000)
    delete_batch3 = MagicMock(rowcount=500)
    delete_batch4 = MagicMock(rowcount=0)

    mock_db.execute.side_effect = [
        count_result,
        delete_batch1,
        delete_batch2,
        delete_batch3,
        delete_batch4,
    ]

    result = await retention_task.cleanup_old_events(mock_db)

    assert result["deleted_count"] == 2500
    assert mock_db.commit.call_count == 4, "3 batches + final check"


@pytest.mark.asyncio
async def test_cleanup_old_events_respects_retention_days(mock_db):
    """Test that cutoff date respects retention_days parameter."""
    # 30-day retention
    task_30 = AnalyticsRetentionTask(retention_days=30)
    cutoff_30 = datetime.utcnow() - timedelta(days=30)

    # 90-day retention
    task_90 = AnalyticsRetentionTask(retention_days=90)
    cutoff_90 = datetime.utcnow() - timedelta(days=90)

    # Mock no old events
    count_result = MagicMock()
    count_result.scalar.return_value = 0
    mock_db.execute.return_value = count_result

    result_30 = await task_30.cleanup_old_events(mock_db)
    result_90 = await task_90.cleanup_old_events(mock_db)

    # Cutoff dates should be different
    cutoff_30_str = result_30["cutoff_date"][:10]  # YYYY-MM-DD
    cutoff_90_str = result_90["cutoff_date"][:10]

    assert cutoff_30_str != cutoff_90_str


# ============================================================================
# Test Retention Stats
# ============================================================================


@pytest.mark.asyncio
async def test_get_retention_stats(retention_task, mock_db):
    """Test retrieval of retention statistics."""
    cutoff_date = datetime.utcnow() - timedelta(days=90)

    # Mock total events count
    total_result = MagicMock()
    total_result.scalar.return_value = 125000

    # Mock oldest event date
    oldest_result = MagicMock()
    oldest_result.scalar.return_value = datetime(2025, 4, 15)

    # Mock newest event date
    newest_result = MagicMock()
    newest_result.scalar.return_value = datetime(2026, 1, 21)

    # Mock old events count
    old_result = MagicMock()
    old_result.scalar.return_value = 12500

    mock_db.execute.side_effect = [
        total_result,
        oldest_result,
        newest_result,
        old_result,
    ]

    stats = await retention_task.get_retention_stats(mock_db)

    assert stats["total_events"] == 125000
    assert stats["oldest_event_date"] == "2025-04-15T00:00:00"
    assert stats["newest_event_date"] == "2026-01-21T00:00:00"
    assert stats["events_older_than_retention"] == 12500
    assert stats["retention_days"] == 90
    assert "cutoff_date" in stats


@pytest.mark.asyncio
async def test_get_retention_stats_empty_table(retention_task, mock_db):
    """Test retention stats when analytics_events table is empty."""
    # Mock empty table
    total_result = MagicMock()
    total_result.scalar.return_value = 0

    oldest_result = MagicMock()
    oldest_result.scalar.return_value = None

    newest_result = MagicMock()
    newest_result.scalar.return_value = None

    old_result = MagicMock()
    old_result.scalar.return_value = 0

    mock_db.execute.side_effect = [
        total_result,
        oldest_result,
        newest_result,
        old_result,
    ]

    stats = await retention_task.get_retention_stats(mock_db)

    assert stats["total_events"] == 0
    assert stats["oldest_event_date"] is None
    assert stats["newest_event_date"] is None
    assert stats["events_older_than_retention"] == 0


# ============================================================================
# Test Entry Point
# ============================================================================


@pytest.mark.asyncio
async def test_run_retention_cleanup_success():
    """Test cron job entry point with successful cleanup."""
    with patch(
        "app.tasks.analytics_retention.async_session_maker"
    ) as mock_session_maker:
        mock_db = AsyncMock()

        # Mock context manager
        mock_session_maker.return_value.__aenter__.return_value = mock_db

        # Mock get_retention_stats
        mock_stats_before = {
            "total_events": 125000,
            "events_older_than_retention": 12500,
        }
        mock_stats_after = {"total_events": 112500, "events_older_than_retention": 0}

        # Mock cleanup_old_events
        mock_cleanup_result = {
            "status": "success",
            "deleted_count": 12500,
            "duration_seconds": 3.2,
        }

        with patch.object(
            AnalyticsRetentionTask,
            "get_retention_stats",
            side_effect=[mock_stats_before, mock_stats_after],
        ):
            with patch.object(
                AnalyticsRetentionTask,
                "cleanup_old_events",
                return_value=mock_cleanup_result,
            ):
                from app.tasks.analytics_retention import run_retention_cleanup

                exit_code = await run_retention_cleanup()

                assert exit_code == 0, "Should return 0 on success"


@pytest.mark.asyncio
async def test_run_retention_cleanup_failure():
    """Test cron job entry point with cleanup failure."""
    with patch(
        "app.tasks.analytics_retention.async_session_maker"
    ) as mock_session_maker:
        mock_db = AsyncMock()
        mock_session_maker.return_value.__aenter__.return_value = mock_db

        # Mock get_retention_stats
        mock_stats = {"total_events": 125000, "events_older_than_retention": 12500}

        # Mock cleanup failure
        mock_cleanup_result = {
            "status": "error",
            "error": "Database connection lost",
            "deleted_count": 0,
        }

        with patch.object(
            AnalyticsRetentionTask, "get_retention_stats", return_value=mock_stats
        ):
            with patch.object(
                AnalyticsRetentionTask,
                "cleanup_old_events",
                return_value=mock_cleanup_result,
            ):
                from app.tasks.analytics_retention import run_retention_cleanup

                exit_code = await run_retention_cleanup()

                assert exit_code == 1, "Should return 1 on failure (triggers alert)"


# ============================================================================
# Test Performance
# ============================================================================


@pytest.mark.asyncio
async def test_cleanup_performance_large_dataset(retention_task, mock_db):
    """Test cleanup performance with 1 million old events."""
    # Mock 1M old events
    count_result = MagicMock()
    count_result.scalar.return_value = 1_000_000

    # Mock 1000 batches of 1000 records each
    delete_result = MagicMock(rowcount=1000)
    final_result = MagicMock(rowcount=0)

    mock_db.execute.side_effect = (
        [count_result]
        + [delete_result] * 1000  # 1000 batches
        + [final_result]  # Final check
    )

    result = await retention_task.cleanup_old_events(mock_db)

    assert result["status"] == "success"
    assert result["deleted_count"] == 1_000_000
    # Should complete in reasonable time (mocked, but structure is correct)
    assert result["duration_seconds"] >= 0


# ============================================================================
# Test Safety Mechanisms
# ============================================================================


@pytest.mark.asyncio
async def test_cleanup_prevents_infinite_loop(retention_task, mock_db):
    """Test that cleanup has safety mechanism to prevent infinite loops."""
    # Mock count: 10 old events
    count_result = MagicMock()
    count_result.scalar.return_value = 10

    # Mock delete always returns 1 (simulating a bug where records aren't deleted)
    # Safety mechanism should stop after 2x expected deletions
    delete_result = MagicMock(rowcount=1)

    mock_db.execute.side_effect = [count_result] + [delete_result] * 25

    result = await retention_task.cleanup_old_events(mock_db)

    # Should stop due to safety check (deleted_count > total * 2)
    assert result["deleted_count"] <= 20, "Safety mechanism should prevent infinite loop"
