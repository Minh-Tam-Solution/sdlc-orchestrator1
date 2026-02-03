"""
Unit tests for E2EExecutionStore service.

Sprint 140 Day 3: Integration Tests
Tests for Redis-backed execution state management.

Test Coverage:
- CRUD operations (create, get, update, delete)
- Status updates and results storage
- List executions with filters
- Fallback to in-memory when Redis unavailable
- TTL and serialization
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from app.services.e2e_execution_store import (
    E2EExecutionStore,
    ExecutionStatus,
    get_execution_store,
    EXECUTION_TTL_SECONDS,
)


class TestE2EExecutionStoreCreate:
    """Test execution creation operations."""

    @pytest.mark.asyncio
    async def test_create_execution_success(self):
        """Test creating execution record with all fields."""
        # ARRANGE
        store = E2EExecutionStore()
        execution_id = str(uuid4())
        project_id = str(uuid4())
        user_id = str(uuid4())

        # ACT
        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None  # Force in-memory fallback
            result = await store.create_execution(
                execution_id=execution_id,
                project_id=project_id,
                user_id=user_id,
                runner="newman",
                test_suite_path="/tests/collection.json",
                environment="staging",
                environment_variables={"API_KEY": "test-key"},
                timeout_seconds=300,
            )

        # ASSERT
        assert result["id"] == execution_id
        assert result["project_id"] == project_id
        assert result["user_id"] == user_id
        assert result["runner"] == "newman"
        assert result["status"] == ExecutionStatus.QUEUED
        assert result["test_suite_path"] == "/tests/collection.json"
        assert result["environment"] == "staging"
        assert result["environment_variables"] == {"API_KEY": "test-key"}
        assert result["timeout_seconds"] == 300
        assert result["created_at"] is not None
        assert result["started_at"] is None
        assert result["completed_at"] is None
        assert result["results"] is None

    @pytest.mark.asyncio
    async def test_create_execution_with_redis(self):
        """Test creating execution stores in Redis."""
        # ARRANGE
        store = E2EExecutionStore()
        execution_id = str(uuid4())
        project_id = str(uuid4())
        user_id = str(uuid4())

        mock_redis = AsyncMock()
        mock_redis.set = AsyncMock()
        mock_redis.zadd = AsyncMock()

        # ACT
        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_get_redis:
            mock_get_redis.return_value = mock_redis
            result = await store.create_execution(
                execution_id=execution_id,
                project_id=project_id,
                user_id=user_id,
                runner="pytest",
                test_suite_path="/tests/",
            )

        # ASSERT
        assert mock_redis.set.called
        # Verify TTL is set
        call_args = mock_redis.set.call_args
        assert call_args.kwargs.get("ex") == EXECUTION_TTL_SECONDS
        # Verify indexes are updated
        assert mock_redis.zadd.call_count == 2  # user index + project index

    @pytest.mark.asyncio
    async def test_create_execution_default_values(self):
        """Test creating execution with default values."""
        # ARRANGE
        store = E2EExecutionStore()
        execution_id = str(uuid4())

        # ACT
        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            result = await store.create_execution(
                execution_id=execution_id,
                project_id="proj-1",
                user_id="user-1",
                runner="newman",
                test_suite_path="/tests/",
            )

        # ASSERT
        assert result["environment"] is None
        assert result["environment_variables"] == {}
        assert result["timeout_seconds"] == 300


class TestE2EExecutionStoreGet:
    """Test execution retrieval operations."""

    @pytest.mark.asyncio
    async def test_get_execution_from_memory(self):
        """Test getting execution from in-memory store."""
        # ARRANGE
        store = E2EExecutionStore()
        execution_id = str(uuid4())

        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            await store.create_execution(
                execution_id=execution_id,
                project_id="proj-1",
                user_id="user-1",
                runner="newman",
                test_suite_path="/tests/",
            )

            # ACT
            result = await store.get_execution(execution_id)

        # ASSERT
        assert result is not None
        assert result["id"] == execution_id
        assert result["runner"] == "newman"

    @pytest.mark.asyncio
    async def test_get_execution_not_found(self):
        """Test getting non-existent execution returns None."""
        # ARRANGE
        store = E2EExecutionStore()

        # ACT
        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            result = await store.get_execution("non-existent-id")

        # ASSERT
        assert result is None

    @pytest.mark.asyncio
    async def test_get_execution_from_redis(self):
        """Test getting execution from Redis."""
        # ARRANGE
        store = E2EExecutionStore()
        execution_id = str(uuid4())
        stored_data = {
            "id": execution_id,
            "status": "queued",
            "runner": "pytest",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        mock_redis = AsyncMock()
        mock_redis.get = AsyncMock(return_value=store._serialize(stored_data))

        # ACT
        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_get_redis:
            mock_get_redis.return_value = mock_redis
            result = await store.get_execution(execution_id)

        # ASSERT
        assert result is not None
        assert result["id"] == execution_id
        assert result["runner"] == "pytest"


class TestE2EExecutionStoreUpdate:
    """Test execution update operations."""

    @pytest.mark.asyncio
    async def test_update_status_to_running(self):
        """Test updating execution status to running."""
        # ARRANGE
        store = E2EExecutionStore()
        execution_id = str(uuid4())
        started_at = datetime.now(timezone.utc)

        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            await store.create_execution(
                execution_id=execution_id,
                project_id="proj-1",
                user_id="user-1",
                runner="newman",
                test_suite_path="/tests/",
            )

            # ACT
            result = await store.update_status(
                execution_id,
                ExecutionStatus.RUNNING,
                started_at=started_at,
            )

        # ASSERT
        assert result is not None
        assert result["status"] == ExecutionStatus.RUNNING
        assert result["started_at"] == started_at

    @pytest.mark.asyncio
    async def test_update_status_to_failed_with_error(self):
        """Test updating execution status to failed with error message."""
        # ARRANGE
        store = E2EExecutionStore()
        execution_id = str(uuid4())
        completed_at = datetime.now(timezone.utc)
        error_msg = "Test execution timed out"

        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            await store.create_execution(
                execution_id=execution_id,
                project_id="proj-1",
                user_id="user-1",
                runner="newman",
                test_suite_path="/tests/",
            )

            # ACT
            result = await store.update_status(
                execution_id,
                ExecutionStatus.FAILED,
                completed_at=completed_at,
                error=error_msg,
            )

        # ASSERT
        assert result is not None
        assert result["status"] == ExecutionStatus.FAILED
        assert result["completed_at"] == completed_at
        assert result["error"] == error_msg

    @pytest.mark.asyncio
    async def test_update_status_not_found(self):
        """Test updating non-existent execution returns None."""
        # ARRANGE
        store = E2EExecutionStore()

        # ACT
        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            result = await store.update_status(
                "non-existent-id",
                ExecutionStatus.RUNNING,
            )

        # ASSERT
        assert result is None


class TestE2EExecutionStoreResults:
    """Test execution results operations."""

    @pytest.mark.asyncio
    async def test_set_results_success(self):
        """Test setting execution results."""
        # ARRANGE
        store = E2EExecutionStore()
        execution_id = str(uuid4())
        results = {
            "total_tests": 10,
            "passed": 8,
            "failed": 2,
            "skipped": 0,
            "pass_rate": 80.0,
            "duration_seconds": 45.5,
        }

        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            await store.create_execution(
                execution_id=execution_id,
                project_id="proj-1",
                user_id="user-1",
                runner="newman",
                test_suite_path="/tests/",
            )

            # ACT
            result = await store.set_results(execution_id, results)

        # ASSERT
        assert result is not None
        assert result["results"] == results
        assert result["status"] == ExecutionStatus.COMPLETED
        assert result["completed_at"] is not None

    @pytest.mark.asyncio
    async def test_set_results_not_found(self):
        """Test setting results for non-existent execution."""
        # ARRANGE
        store = E2EExecutionStore()

        # ACT
        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            result = await store.set_results("non-existent-id", {"passed": 5})

        # ASSERT
        assert result is None


class TestE2EExecutionStoreList:
    """Test execution list operations."""

    @pytest.mark.asyncio
    async def test_list_executions_by_user(self):
        """Test listing executions filtered by user."""
        # ARRANGE
        store = E2EExecutionStore()
        user_id = "user-1"

        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            # Create 3 executions for user-1
            for i in range(3):
                await store.create_execution(
                    execution_id=f"exec-{i}",
                    project_id="proj-1",
                    user_id=user_id,
                    runner="newman",
                    test_suite_path="/tests/",
                )
            # Create 1 execution for user-2
            await store.create_execution(
                execution_id="exec-other",
                project_id="proj-1",
                user_id="user-2",
                runner="newman",
                test_suite_path="/tests/",
            )

            # ACT
            results = await store.list_executions(user_id=user_id)

        # ASSERT
        assert len(results) == 3
        for exec in results:
            assert exec["user_id"] == user_id

    @pytest.mark.asyncio
    async def test_list_executions_with_limit(self):
        """Test listing executions with limit."""
        # ARRANGE
        store = E2EExecutionStore()
        user_id = "user-1"

        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            for i in range(10):
                await store.create_execution(
                    execution_id=f"exec-{i}",
                    project_id="proj-1",
                    user_id=user_id,
                    runner="newman",
                    test_suite_path="/tests/",
                )

            # ACT
            results = await store.list_executions(user_id=user_id, limit=5)

        # ASSERT
        assert len(results) == 5

    @pytest.mark.asyncio
    async def test_list_executions_by_project(self):
        """Test listing executions filtered by project."""
        # ARRANGE
        store = E2EExecutionStore()
        project_id = "proj-target"

        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            # Create executions for target project
            for i in range(2):
                await store.create_execution(
                    execution_id=f"exec-target-{i}",
                    project_id=project_id,
                    user_id="user-1",
                    runner="newman",
                    test_suite_path="/tests/",
                )
            # Create execution for other project
            await store.create_execution(
                execution_id="exec-other",
                project_id="proj-other",
                user_id="user-1",
                runner="newman",
                test_suite_path="/tests/",
            )

            # ACT
            results = await store.list_executions(project_id=project_id)

        # ASSERT
        assert len(results) == 2
        for exec in results:
            assert exec["project_id"] == project_id


class TestE2EExecutionStoreDelete:
    """Test execution delete operations."""

    @pytest.mark.asyncio
    async def test_delete_execution_success(self):
        """Test deleting execution."""
        # ARRANGE
        store = E2EExecutionStore()
        execution_id = str(uuid4())

        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            await store.create_execution(
                execution_id=execution_id,
                project_id="proj-1",
                user_id="user-1",
                runner="newman",
                test_suite_path="/tests/",
            )

            # Verify exists
            assert await store.get_execution(execution_id) is not None

            # ACT
            result = await store.delete_execution(execution_id)

        # ASSERT
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_execution_not_found(self):
        """Test deleting non-existent execution."""
        # ARRANGE
        store = E2EExecutionStore()

        # ACT
        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None
            result = await store.delete_execution("non-existent-id")

        # ASSERT
        assert result is False


class TestE2EExecutionStoreStats:
    """Test execution statistics operations."""

    @pytest.mark.asyncio
    async def test_get_stats_by_user(self):
        """Test getting execution statistics."""
        # ARRANGE
        store = E2EExecutionStore()
        user_id = "user-1"

        with patch.object(store, "_get_redis", new_callable=AsyncMock) as mock_redis:
            mock_redis.return_value = None

            # Create executions with various statuses
            exec1 = await store.create_execution(
                execution_id="exec-1",
                project_id="proj-1",
                user_id=user_id,
                runner="newman",
                test_suite_path="/tests/",
            )
            await store.update_status("exec-1", ExecutionStatus.COMPLETED)

            await store.create_execution(
                execution_id="exec-2",
                project_id="proj-1",
                user_id=user_id,
                runner="newman",
                test_suite_path="/tests/",
            )
            await store.update_status("exec-2", ExecutionStatus.FAILED)

            await store.create_execution(
                execution_id="exec-3",
                project_id="proj-1",
                user_id=user_id,
                runner="newman",
                test_suite_path="/tests/",
            )
            # exec-3 stays QUEUED

            # ACT
            stats = await store.get_stats(user_id=user_id)

        # ASSERT
        assert stats["total"] == 3
        assert stats["completed"] == 1
        assert stats["failed"] == 1
        assert stats["queued"] == 1


class TestE2EExecutionStoreSerialization:
    """Test serialization and deserialization."""

    def test_serialize_datetime(self):
        """Test datetime serialization."""
        # ARRANGE
        store = E2EExecutionStore()
        data = {
            "id": "test-id",
            "created_at": datetime(2026, 2, 12, 10, 30, 0, tzinfo=timezone.utc),
        }

        # ACT
        serialized = store._serialize(data)

        # ASSERT
        assert "2026-02-12" in serialized
        assert "10:30:00" in serialized

    def test_deserialize_datetime(self):
        """Test datetime deserialization."""
        # ARRANGE
        store = E2EExecutionStore()
        json_str = '{"id": "test-id", "created_at": "2026-02-12T10:30:00+00:00", "status": "queued"}'

        # ACT
        result = store._deserialize(json_str)

        # ASSERT
        assert isinstance(result["created_at"], datetime)
        assert result["status"] == ExecutionStatus.QUEUED


class TestE2EExecutionStoreFallback:
    """Test Redis fallback behavior."""

    @pytest.mark.asyncio
    async def test_fallback_to_memory_on_redis_failure(self):
        """Test fallback to in-memory store when Redis fails."""
        # ARRANGE
        store = E2EExecutionStore()
        execution_id = str(uuid4())

        # Mock Redis to raise exception
        async def mock_get_redis():
            raise Exception("Redis connection failed")

        with patch.object(store, "_get_redis", mock_get_redis):
            store._redis_available = False  # Force fallback

            # ACT - should not raise
            result = await store.create_execution(
                execution_id=execution_id,
                project_id="proj-1",
                user_id="user-1",
                runner="newman",
                test_suite_path="/tests/",
            )

        # ASSERT
        assert result is not None
        assert result["id"] == execution_id
        # Verify stored in memory
        assert execution_id in store._memory_store


class TestGetExecutionStore:
    """Test singleton pattern for execution store."""

    @pytest.mark.asyncio
    async def test_get_execution_store_singleton(self):
        """Test get_execution_store returns same instance."""
        # ACT
        with patch("app.services.e2e_execution_store._execution_store", None):
            store1 = await get_execution_store()
            store2 = await get_execution_store()

        # ASSERT
        assert store1 is store2
