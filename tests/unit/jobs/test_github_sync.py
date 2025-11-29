"""
=========================================================================
GitHub Sync Background Jobs Unit Tests
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: November 28, 2025
Status: ACTIVE - Sprint 16 Day 4
Authority: QA Lead + Backend Lead Approved
Foundation: Sprint 16 Testing Plan
Framework: SDLC 4.9 Complete Lifecycle

Purpose:
- Unit tests for github_sync.py background jobs
- Test job queue operations
- Test job status tracking
- Test webhook processing logic

Test Classes:
- TestScheduleProjectSync: Test job scheduling
- TestRunGitHubSyncJob: Test sync job execution (mocked)
- TestProcessWebhookEvent: Test webhook event processing
- TestJobManagement: Test queue stats and cleanup

Zero Mock Policy: Only mock database and external services
=========================================================================
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from app.jobs.github_sync import (
    schedule_project_sync,
    run_github_sync_job,
    process_webhook_event,
    run_webhook_processing_job,
    get_sync_job_status,
    get_pending_sync_jobs,
    get_job_queue_stats,
    clear_completed_jobs,
    run_scheduled_sync_for_stale_projects,
    _sync_queue,
    _webhook_queue,
    _job_status,
)


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture(autouse=True)
def clear_queues():
    """Clear job queues before each test."""
    _sync_queue.clear()
    _webhook_queue.clear()
    _job_status.clear()
    yield
    _sync_queue.clear()
    _webhook_queue.clear()
    _job_status.clear()


@pytest.fixture
def sample_project_id():
    """Generate sample project UUID."""
    return uuid4()


@pytest.fixture
def sample_user_id():
    """Generate sample user UUID."""
    return uuid4()


@pytest.fixture
def sample_webhook_payload():
    """Sample GitHub push webhook payload."""
    return {
        "ref": "refs/heads/main",
        "repository": {
            "id": 123456789,
            "full_name": "developer/my-project",
            "name": "my-project",
            "owner": {"login": "developer"},
            "private": False,
        },
        "sender": {"id": 12345, "login": "developer"},
        "commits": [
            {
                "id": "abc123",
                "message": "feat: Add new feature",
                "modified": ["src/main.py"],
                "added": [],
            }
        ],
        "head_commit": {
            "id": "abc123",
            "message": "feat: Add new feature",
        },
    }


# ============================================================================
# TestScheduleProjectSync
# ============================================================================


class TestScheduleProjectSync:
    """Tests for schedule_project_sync function."""

    @pytest.mark.asyncio
    async def test_schedules_job_with_normal_priority(
        self, sample_project_id, sample_user_id
    ):
        """Test scheduling a sync job with normal priority."""
        result = await schedule_project_sync(
            project_id=sample_project_id,
            user_id=sample_user_id,
            priority="normal",
        )

        assert result["status"] == "queued"
        assert result["project_id"] == str(sample_project_id)
        assert "job_id" in result
        assert result["job_id"].startswith("sync_")
        assert len(_sync_queue) == 1
        assert _sync_queue[0]["priority"] == "normal"

    @pytest.mark.asyncio
    async def test_schedules_job_with_high_priority_first(
        self, sample_project_id, sample_user_id
    ):
        """Test high priority jobs are inserted at front of queue."""
        # Add normal priority job first
        await schedule_project_sync(
            project_id=sample_project_id,
            user_id=sample_user_id,
            priority="normal",
        )

        # Add high priority job
        high_priority_project = uuid4()
        result = await schedule_project_sync(
            project_id=high_priority_project,
            user_id=sample_user_id,
            priority="high",
        )

        assert len(_sync_queue) == 2
        assert _sync_queue[0]["project_id"] == str(high_priority_project)
        assert _sync_queue[0]["priority"] == "high"
        assert _sync_queue[1]["priority"] == "normal"

    @pytest.mark.asyncio
    async def test_tracks_job_status(self, sample_project_id, sample_user_id):
        """Test job status is tracked in _job_status."""
        result = await schedule_project_sync(
            project_id=sample_project_id,
            user_id=sample_user_id,
        )

        job_id = result["job_id"]
        status = get_sync_job_status(job_id)

        assert status is not None
        assert status["status"] == "queued"
        assert status["project_id"] == str(sample_project_id)
        assert status["user_id"] == str(sample_user_id)
        assert "queued_at" in status

    @pytest.mark.asyncio
    async def test_force_flag_is_stored(self, sample_project_id, sample_user_id):
        """Test force flag is stored in job."""
        await schedule_project_sync(
            project_id=sample_project_id,
            user_id=sample_user_id,
            force=True,
        )

        assert _sync_queue[0]["force"] is True

    @pytest.mark.asyncio
    async def test_get_pending_sync_jobs(self, sample_project_id, sample_user_id):
        """Test getting list of pending sync jobs."""
        await schedule_project_sync(
            project_id=sample_project_id,
            user_id=sample_user_id,
        )

        pending = get_pending_sync_jobs()
        assert len(pending) == 1
        assert pending[0]["project_id"] == str(sample_project_id)


# ============================================================================
# TestRunGitHubSyncJob
# ============================================================================


class TestRunGitHubSyncJob:
    """Tests for run_github_sync_job function."""

    @pytest.mark.asyncio
    async def test_processes_empty_queue(self):
        """Test processing empty queue returns zero jobs."""
        result = await run_github_sync_job(max_jobs=10)

        assert result["jobs_processed"] == 0
        assert result["jobs_succeeded"] == 0
        assert result["jobs_failed"] == 0
        assert result["jobs_remaining"] == 0

    @pytest.mark.asyncio
    async def test_respects_max_jobs_limit(self, sample_project_id, sample_user_id):
        """Test max_jobs parameter limits processing."""
        # Queue multiple jobs
        for _ in range(5):
            await schedule_project_sync(
                project_id=uuid4(),
                user_id=sample_user_id,
            )

        # Mock database to fail (simulating no OAuth account)
        with patch("app.jobs.github_sync.AsyncSessionLocal") as mock_session:
            mock_db = AsyncMock()
            mock_result = MagicMock()
            mock_result.scalar_one_or_none.return_value = None
            mock_db.execute = AsyncMock(return_value=mock_result)
            mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_db)
            mock_session.return_value.__aexit__ = AsyncMock()

            result = await run_github_sync_job(max_jobs=2)

        # Should only process 2, leaving 3
        assert result["jobs_processed"] == 2
        assert result["jobs_remaining"] == 3

    @pytest.mark.asyncio
    async def test_handles_missing_oauth_account(
        self, sample_project_id, sample_user_id
    ):
        """Test job processes when OAuth account lookup happens."""
        await schedule_project_sync(
            project_id=sample_project_id,
            user_id=sample_user_id,
        )

        # Note: With proper DB mock, this would fail with "No GitHub connection"
        # For unit test simplicity, we just verify the job processes the queue
        with patch("app.jobs.github_sync.AsyncSessionLocal") as mock_session:
            mock_db = AsyncMock()
            mock_result = MagicMock()
            mock_result.scalar_one_or_none.return_value = None
            mock_db.execute = AsyncMock(return_value=mock_result)

            # Setup async context manager properly
            mock_session_instance = AsyncMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=mock_db)
            mock_session_instance.__aexit__ = AsyncMock(return_value=None)
            mock_session.return_value = mock_session_instance

            result = await run_github_sync_job(max_jobs=1)

        # Job should process the queued item
        assert result["jobs_processed"] == 1
        # Job will fail due to missing OAuth (ValueError raised)
        assert result["jobs_failed"] == 1
        assert len(result["results"]) == 1


# ============================================================================
# TestProcessWebhookEvent
# ============================================================================


class TestProcessWebhookEvent:
    """Tests for process_webhook_event function."""

    @pytest.mark.asyncio
    async def test_queues_valid_webhook(self, sample_webhook_payload):
        """Test valid webhook is queued."""
        with patch("app.jobs.github_sync.github_service") as mock_github:
            mock_github.validate_webhook_signature.return_value = True

            result = await process_webhook_event(
                event_type="push",
                payload=sample_webhook_payload,
                signature="sha256=valid",
            )

        assert result["received"] is True
        assert result["event_type"] == "push"
        assert result["repository"] == "developer/my-project"
        assert "job_id" in result
        assert len(_webhook_queue) == 1

    @pytest.mark.asyncio
    async def test_rejects_invalid_signature(self, sample_webhook_payload):
        """Test webhook with invalid signature is rejected."""
        with patch("app.jobs.github_sync.github_service") as mock_github:
            mock_github.validate_webhook_signature.return_value = False

            result = await process_webhook_event(
                event_type="push",
                payload=sample_webhook_payload,
                signature="sha256=invalid",
            )

        assert result["received"] is False
        assert "Invalid signature" in result["error"]
        assert len(_webhook_queue) == 0

    @pytest.mark.asyncio
    async def test_extracts_repository_info(self, sample_webhook_payload):
        """Test repository info is extracted from payload."""
        with patch("app.jobs.github_sync.github_service") as mock_github:
            mock_github.validate_webhook_signature.return_value = True

            await process_webhook_event(
                event_type="push",
                payload=sample_webhook_payload,
                signature="sha256=valid",
            )

        queued = _webhook_queue[0]
        assert queued["repository"] == "developer/my-project"
        assert queued["repository_id"] == 123456789


# ============================================================================
# TestRunWebhookProcessingJob
# ============================================================================


class TestRunWebhookProcessingJob:
    """Tests for run_webhook_processing_job function."""

    @pytest.mark.asyncio
    async def test_processes_empty_queue(self):
        """Test processing empty webhook queue."""
        result = await run_webhook_processing_job(max_events=10)

        assert result["events_processed"] == 0
        assert result["events_succeeded"] == 0
        assert result["events_failed"] == 0

    @pytest.mark.asyncio
    async def test_skips_webhook_without_linked_project(self, sample_webhook_payload):
        """Test webhook is skipped if no project found."""
        # Queue webhook
        with patch("app.jobs.github_sync.github_service") as mock_github:
            mock_github.validate_webhook_signature.return_value = True
            await process_webhook_event(
                event_type="push",
                payload=sample_webhook_payload,
                signature="sha256=valid",
            )

        # Process with no project in DB
        with patch("app.jobs.github_sync.AsyncSessionLocal") as mock_session:
            mock_db = AsyncMock()
            mock_result = MagicMock()
            mock_result.scalar_one_or_none.return_value = None
            mock_db.execute = AsyncMock(return_value=mock_result)
            mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_db)
            mock_session.return_value.__aexit__ = AsyncMock()

            result = await run_webhook_processing_job(max_events=1)

        assert result["events_processed"] == 1
        assert result["results"][0]["status"] == "skipped"
        assert result["results"][0]["reason"] == "No linked project"


# ============================================================================
# TestJobManagement
# ============================================================================


class TestJobManagement:
    """Tests for job management functions."""

    @pytest.mark.asyncio
    async def test_get_job_queue_stats(self, sample_project_id, sample_user_id):
        """Test getting queue statistics."""
        # Queue some jobs
        await schedule_project_sync(
            project_id=sample_project_id,
            user_id=sample_user_id,
        )

        stats = get_job_queue_stats()

        assert stats["sync_queue_length"] == 1
        assert stats["webhook_queue_length"] == 0
        assert stats["total_jobs_tracked"] == 1
        assert "queued" in stats["jobs_by_status"]

    def test_clear_completed_jobs(self):
        """Test clearing old completed jobs."""
        # Add completed job with old timestamp
        old_time = (datetime.utcnow() - timedelta(hours=48)).isoformat()
        _job_status["old_job"] = {
            "job_id": "old_job",
            "status": "completed",
            "completed_at": old_time,
        }

        # Add recent completed job
        recent_time = datetime.utcnow().isoformat()
        _job_status["recent_job"] = {
            "job_id": "recent_job",
            "status": "completed",
            "completed_at": recent_time,
        }

        # Clear jobs older than 24 hours
        cleared = clear_completed_jobs(older_than_hours=24)

        assert cleared == 1
        assert "old_job" not in _job_status
        assert "recent_job" in _job_status

    def test_get_sync_job_status_not_found(self):
        """Test getting status for non-existent job."""
        status = get_sync_job_status("nonexistent_job")
        assert status is None


# ============================================================================
# TestScheduledSync
# ============================================================================


class TestScheduledSync:
    """Tests for scheduled sync functions."""

    @pytest.mark.asyncio
    async def test_schedules_sync_for_stale_projects(self):
        """Test scheduling sync for stale projects."""
        with patch("app.jobs.github_sync.AsyncSessionLocal") as mock_session:
            # Mock finding stale projects
            mock_db = AsyncMock()
            mock_project = MagicMock()
            mock_project.id = uuid4()
            mock_project.owner_id = uuid4()

            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = [mock_project]
            mock_db.execute = AsyncMock(return_value=mock_result)
            mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_db)
            mock_session.return_value.__aexit__ = AsyncMock()

            result = await run_scheduled_sync_for_stale_projects(
                stale_hours=24,
                max_projects=10,
            )

        assert result["jobs_queued"] == 1
        assert len(_sync_queue) == 1
        assert _sync_queue[0]["priority"] == "low"


# ============================================================================
# Test Event Handlers
# ============================================================================


class TestEventHandlers:
    """Tests for webhook event handler functions."""

    @pytest.mark.asyncio
    async def test_push_event_updates_timestamp(self):
        """Test push event updates project sync timestamp."""
        from app.jobs.github_sync import _handle_push_event

        mock_project = MagicMock()
        mock_project.github_synced_at = None
        mock_db = AsyncMock()

        payload = {
            "ref": "refs/heads/main",
            "commits": [
                {"message": "test", "modified": ["test.py"], "added": []},
            ],
            "head_commit": {"message": "test"},
        }

        result = await _handle_push_event(mock_project, payload, mock_db)

        assert result["action"] == "push_processed"
        assert result["ref"] == "refs/heads/main"
        assert result["commits_count"] == 1
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_push_event_detects_significant_changes(self):
        """Test push event detects significant file changes."""
        from app.jobs.github_sync import _handle_push_event

        mock_project = MagicMock()
        mock_db = AsyncMock()

        # Push with requirements.txt change
        payload = {
            "ref": "refs/heads/main",
            "commits": [
                {"message": "update deps", "modified": ["requirements.txt"], "added": []},
            ],
            "head_commit": {"message": "update deps"},
        }

        result = await _handle_push_event(mock_project, payload, mock_db)

        assert result["needs_full_sync"] is True

    @pytest.mark.asyncio
    async def test_pull_request_event_processing(self):
        """Test PR event processing extracts info correctly."""
        from app.jobs.github_sync import _handle_pull_request_event

        mock_project = MagicMock()
        mock_db = AsyncMock()

        payload = {
            "action": "opened",
            "pull_request": {
                "number": 42,
                "title": "feat: Add new feature",
                "state": "open",
            },
        }

        result = await _handle_pull_request_event(mock_project, payload, mock_db)

        assert result["action"] == "pr_processed"
        assert result["pr_action"] == "opened"
        assert result["pr_number"] == 42
        assert result["pr_title"] == "feat: Add new feature"

    @pytest.mark.asyncio
    async def test_issues_event_processing(self):
        """Test issues event processing."""
        from app.jobs.github_sync import _handle_issues_event

        mock_project = MagicMock()
        mock_db = AsyncMock()

        payload = {
            "action": "opened",
            "issue": {
                "number": 100,
                "title": "Bug: Something broken",
            },
        }

        result = await _handle_issues_event(mock_project, payload, mock_db)

        assert result["action"] == "issue_processed"
        assert result["issue_number"] == 100

    @pytest.mark.asyncio
    async def test_branch_event_processing(self):
        """Test branch create/delete event processing."""
        from app.jobs.github_sync import _handle_branch_event

        mock_project = MagicMock()
        mock_db = AsyncMock()

        payload = {
            "ref_type": "branch",
            "ref": "feature/new-feature",
        }

        result = await _handle_branch_event(
            mock_project, "create", payload, mock_db
        )

        assert result["action"] == "branch_created"
        assert result["ref_type"] == "branch"
        assert result["ref"] == "feature/new-feature"
