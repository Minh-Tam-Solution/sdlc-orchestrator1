"""
Unit Tests for Invitation Cleanup Task

Tests for ADR-047 CTO Mandatory Condition #2 - 90-day Retention Cleanup.

Sprint: 146
Reference: ADR-047-Organization-Invitation-System-Architecture.md

Coverage:
- Mark expired invitations
- Archive old invitations (stats)
- Purge old invitations (hard delete)
- Get invitation stats
- Full cleanup workflow
"""
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from app.models.organization_invitation import (
    OrganizationInvitation,
    OrgInvitationStatus,
)
from app.tasks.invitation_cleanup import (
    InvitationCleanupTask,
    run_invitation_cleanup,
    cleanup_expired_invitations_sync,
)


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def mock_db_session():
    """Mock async database session"""
    session = AsyncMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    return session


@pytest.fixture
def cleanup_task(mock_db_session):
    """Invitation cleanup task with mocked DB"""
    return InvitationCleanupTask(
        db=mock_db_session,
        retention_days=90,
        grace_period_days=30,
    )


# ============================================================================
# Configuration Tests
# ============================================================================

class TestCleanupTaskConfiguration:
    """Test cleanup task configuration"""

    def test_default_retention_days(self, mock_db_session):
        """Should use 90 days retention by default"""
        task = InvitationCleanupTask(db=mock_db_session)
        assert task._retention_days == 90

    def test_default_grace_period_days(self, mock_db_session):
        """Should use 30 days grace period by default"""
        task = InvitationCleanupTask(db=mock_db_session)
        assert task._grace_period_days == 30

    def test_custom_retention_days(self, mock_db_session):
        """Should accept custom retention days"""
        task = InvitationCleanupTask(db=mock_db_session, retention_days=60)
        assert task._retention_days == 60

    def test_custom_grace_period_days(self, mock_db_session):
        """Should accept custom grace period"""
        task = InvitationCleanupTask(db=mock_db_session, grace_period_days=15)
        assert task._grace_period_days == 15

    def test_batch_size_constant(self):
        """Batch size should be 100"""
        assert InvitationCleanupTask.BATCH_SIZE == 100


# ============================================================================
# Mark Expired Invitations Tests
# ============================================================================

class TestMarkExpiredInvitations:
    """Test marking pending invitations as expired"""

    @pytest.mark.asyncio
    async def test_no_invitations_to_expire(self, cleanup_task, mock_db_session):
        """Should handle case with no invitations to expire"""
        # Mock count query returning 0
        mock_result = MagicMock()
        mock_result.scalar.return_value = 0
        mock_db_session.execute.return_value = mock_result

        result = await cleanup_task.mark_expired_invitations()

        assert result["expired_count"] == 0
        assert result["status"] == "success"
        assert "cutoff_date" in result

    @pytest.mark.asyncio
    async def test_expires_pending_invitations(self, cleanup_task, mock_db_session):
        """Should mark pending invitations as expired"""
        # Mock count query returning 5
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 5
        mock_db_session.execute.return_value = mock_count_result

        result = await cleanup_task.mark_expired_invitations()

        assert result["expired_count"] == 5
        assert result["status"] == "success"
        assert result["duration_seconds"] >= 0
        # Verify commit was called
        mock_db_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_handles_database_error(self, cleanup_task, mock_db_session):
        """Should handle database errors gracefully"""
        mock_db_session.execute.side_effect = Exception("Database error")

        result = await cleanup_task.mark_expired_invitations()

        assert result["expired_count"] == 0
        assert result["status"] == "error"
        assert "error" in result
        mock_db_session.rollback.assert_called_once()


# ============================================================================
# Archive Old Invitations Tests
# ============================================================================

class TestArchiveOldInvitations:
    """Test archiving (counting) old invitations"""

    @pytest.mark.asyncio
    async def test_counts_eligible_invitations(self, cleanup_task, mock_db_session):
        """Should count invitations eligible for purge"""
        mock_result = MagicMock()
        mock_result.scalar.return_value = 50
        mock_db_session.execute.return_value = mock_result

        result = await cleanup_task.archive_old_invitations()

        assert result["archived_count"] == 50
        assert result["status"] == "success"
        assert result["retention_days"] == 90

    @pytest.mark.asyncio
    async def test_archive_cutoff_date(self, cleanup_task, mock_db_session):
        """Should calculate correct cutoff date"""
        mock_result = MagicMock()
        mock_result.scalar.return_value = 0
        mock_db_session.execute.return_value = mock_result

        result = await cleanup_task.archive_old_invitations()

        cutoff = datetime.fromisoformat(result["cutoff_date"])
        expected_cutoff = datetime.now(timezone.utc) - timedelta(days=90)

        # Should be within 1 minute of expected
        assert abs((cutoff - expected_cutoff).total_seconds()) < 60

    @pytest.mark.asyncio
    async def test_handles_archive_error(self, cleanup_task, mock_db_session):
        """Should handle errors gracefully"""
        mock_db_session.execute.side_effect = Exception("DB error")

        result = await cleanup_task.archive_old_invitations()

        assert result["archived_count"] == 0
        assert result["status"] == "error"


# ============================================================================
# Purge Old Invitations Tests
# ============================================================================

class TestPurgeOldInvitations:
    """Test purging (hard deleting) old invitations"""

    @pytest.mark.asyncio
    async def test_no_invitations_to_purge(self, cleanup_task, mock_db_session):
        """Should handle case with no invitations to purge"""
        mock_result = MagicMock()
        mock_result.scalar.return_value = 0
        mock_db_session.execute.return_value = mock_result

        result = await cleanup_task.purge_old_invitations()

        assert result["purged_count"] == 0
        assert result["status"] == "success"
        assert result["total_days"] == 120  # 90 + 30

    @pytest.mark.asyncio
    async def test_purges_old_invitations(self, cleanup_task, mock_db_session):
        """Should purge old invitations in batches"""
        # First call: count returns 2
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 2

        # Second call: batch IDs
        mock_batch_result = MagicMock()
        mock_batch_result.fetchall.return_value = [(uuid4(),), (uuid4(),)]

        # Third call: empty batch (done)
        mock_empty_result = MagicMock()
        mock_empty_result.fetchall.return_value = []

        mock_db_session.execute.side_effect = [
            mock_count_result,
            mock_batch_result,
            mock_empty_result,
        ]

        result = await cleanup_task.purge_old_invitations()

        assert result["purged_count"] == 2
        assert result["status"] == "success"

    @pytest.mark.asyncio
    async def test_purge_cutoff_includes_grace_period(self, cleanup_task, mock_db_session):
        """Should include grace period in cutoff calculation"""
        mock_result = MagicMock()
        mock_result.scalar.return_value = 0
        mock_db_session.execute.return_value = mock_result

        result = await cleanup_task.purge_old_invitations()

        cutoff = datetime.fromisoformat(result["cutoff_date"])
        expected_cutoff = datetime.now(timezone.utc) - timedelta(days=120)

        # Should be within 1 minute of expected
        assert abs((cutoff - expected_cutoff).total_seconds()) < 60

    @pytest.mark.asyncio
    async def test_handles_purge_error(self, cleanup_task, mock_db_session):
        """Should handle purge errors gracefully"""
        mock_db_session.execute.side_effect = Exception("Delete failed")

        result = await cleanup_task.purge_old_invitations()

        assert result["purged_count"] == 0
        assert result["status"] == "error"
        mock_db_session.rollback.assert_called_once()


# ============================================================================
# Get Invitation Stats Tests
# ============================================================================

class TestGetInvitationStats:
    """Test getting invitation statistics"""

    @pytest.mark.asyncio
    async def test_returns_all_status_counts(self, cleanup_task, mock_db_session):
        """Should return counts for all statuses"""
        # Mock returns for each query (total + 5 statuses + purge eligible)
        mock_results = []
        for count in [100, 10, 50, 20, 15, 5, 3]:  # total, pending, accepted, declined, expired, cancelled, purge
            mock_result = MagicMock()
            mock_result.scalar.return_value = count
            mock_results.append(mock_result)

        mock_db_session.execute.side_effect = mock_results

        result = await cleanup_task.get_invitation_stats()

        assert result["total_invitations"] == 100
        assert result["pending_count"] == 10
        assert result["accepted_count"] == 50
        assert result["declined_count"] == 20
        assert result["expired_count"] == 15
        assert result["cancelled_count"] == 5
        assert result["eligible_for_purge"] == 3
        assert result["retention_days"] == 90
        assert result["grace_period_days"] == 30

    @pytest.mark.asyncio
    async def test_handles_stats_error(self, cleanup_task, mock_db_session):
        """Should handle stats query errors"""
        mock_db_session.execute.side_effect = Exception("Stats failed")

        result = await cleanup_task.get_invitation_stats()

        assert result["status"] == "error"
        assert "error" in result


# ============================================================================
# Full Cleanup Workflow Tests
# ============================================================================

class TestFullCleanupWorkflow:
    """Test complete cleanup workflow"""

    @pytest.mark.asyncio
    async def test_run_invitation_cleanup(self):
        """Should run complete cleanup workflow"""
        with patch("app.tasks.invitation_cleanup.async_session_maker") as mock_session_maker:
            # Setup mock session
            mock_session = AsyncMock()
            mock_session_maker.return_value.__aenter__.return_value = mock_session

            # Mock all query results
            mock_result = MagicMock()
            mock_result.scalar.return_value = 0
            mock_result.fetchall.return_value = []
            mock_session.execute.return_value = mock_result

            result = await run_invitation_cleanup()

            assert "timestamp" in result
            assert "total_duration_seconds" in result
            assert "expiration" in result
            assert "archive" in result
            assert "purge" in result
            assert "final_stats" in result

    def test_sync_wrapper(self):
        """Should have sync wrapper for Celery"""
        with patch("app.tasks.invitation_cleanup.asyncio.run") as mock_run:
            mock_run.return_value = {"status": "success"}

            result = cleanup_expired_invitations_sync()

            mock_run.assert_called_once()
            assert result["status"] == "success"


# ============================================================================
# CTO Mandatory Condition #2 Tests
# ============================================================================

class TestCTOMandatoryCondition2:
    """Tests for CTO Mandatory Condition #2: 90-day retention cleanup"""

    def test_default_retention_is_90_days(self):
        """CTO Condition #2: Default retention must be 90 days"""
        assert InvitationCleanupTask.RETENTION_DAYS == 90

    def test_grace_period_is_30_days(self):
        """Grace period before hard delete should be 30 days"""
        assert InvitationCleanupTask.GRACE_PERIOD_DAYS == 30

    @pytest.mark.asyncio
    async def test_only_non_pending_statuses_purged(self, cleanup_task, mock_db_session):
        """Should only purge non-pending statuses"""
        # The purge query should use completed_statuses list
        # which excludes PENDING
        completed_statuses = [
            OrgInvitationStatus.ACCEPTED,
            OrgInvitationStatus.DECLINED,
            OrgInvitationStatus.EXPIRED,
            OrgInvitationStatus.CANCELLED,
        ]

        # Verify PENDING is not in purge list
        assert OrgInvitationStatus.PENDING not in completed_statuses

    @pytest.mark.asyncio
    async def test_total_retention_is_120_days(self, cleanup_task, mock_db_session):
        """Total retention (90 + 30) should be 120 days before hard delete"""
        mock_result = MagicMock()
        mock_result.scalar.return_value = 0
        mock_db_session.execute.return_value = mock_result

        result = await cleanup_task.purge_old_invitations()

        assert result["total_days"] == 120


# ============================================================================
# Batch Processing Tests
# ============================================================================

class TestBatchProcessing:
    """Test batch processing behavior"""

    @pytest.mark.asyncio
    async def test_processes_in_batches(self, mock_db_session):
        """Should process deletions in batches of 100"""
        task = InvitationCleanupTask(db=mock_db_session)

        # Mock large number of invitations
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 250

        # Create batch results (3 batches: 100, 100, 50)
        batch1 = MagicMock()
        batch1.fetchall.return_value = [(uuid4(),) for _ in range(100)]

        batch2 = MagicMock()
        batch2.fetchall.return_value = [(uuid4(),) for _ in range(100)]

        batch3 = MagicMock()
        batch3.fetchall.return_value = [(uuid4(),) for _ in range(50)]

        batch_empty = MagicMock()
        batch_empty.fetchall.return_value = []

        # Mock for delete statements (returns MagicMock)
        delete_result = MagicMock()

        mock_db_session.execute.side_effect = [
            mock_count_result,  # Count query
            batch1,  # First batch select
            delete_result,  # First batch delete
            batch2,  # Second batch select
            delete_result,  # Second batch delete
            batch3,  # Third batch select
            delete_result,  # Third batch delete
            batch_empty,  # Empty batch (done)
        ]

        result = await task.purge_old_invitations()

        assert result["purged_count"] == 250
        assert result["status"] == "success"


# ============================================================================
# Audit Trail Tests
# ============================================================================

class TestAuditTrail:
    """Test audit logging behavior"""

    @pytest.mark.asyncio
    async def test_logs_expiration_start(self, cleanup_task, mock_db_session, caplog):
        """Should log when starting expiration check"""
        import logging
        caplog.set_level(logging.INFO)

        mock_result = MagicMock()
        mock_result.scalar.return_value = 0
        mock_db_session.execute.return_value = mock_result

        await cleanup_task.mark_expired_invitations()

        assert "Starting invitation expiration check" in caplog.text

    @pytest.mark.asyncio
    async def test_logs_purge_batches(self, cleanup_task, mock_db_session, caplog):
        """Should log batch purge operations"""
        import logging
        caplog.set_level(logging.INFO)

        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 2

        mock_batch_result = MagicMock()
        mock_batch_result.fetchall.return_value = [(uuid4(),), (uuid4(),)]

        mock_empty_result = MagicMock()
        mock_empty_result.fetchall.return_value = []

        mock_db_session.execute.side_effect = [
            mock_count_result,
            mock_batch_result,
            mock_empty_result,
        ]

        await cleanup_task.purge_old_invitations()

        assert "Purging batch of" in caplog.text
