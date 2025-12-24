"""
Validation Worker - Background Job Processor

SDLC Stage: 04 - BUILD
Sprint: 42 - AI Detection & Validation Pipeline
Framework: SDLC 5.1.1

Purpose:
Background worker for processing validation queue.
Uses Redis for job queue and async processing.

Architecture:
- Redis BLPOP for blocking queue reads
- Async processing with validation pipeline
- Retry logic with exponential backoff
- Graceful shutdown handling

Queue Format:
- Key: "validation:queue"
- Value: JSON-encoded job data
"""

import asyncio
import json
import logging
import signal
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

logger = logging.getLogger(__name__)

# Import metrics (may fail in test environment)
try:
    from app.middleware.validation_metrics import record_queue_size, record_queue_wait

    METRICS_ENABLED = True
except ImportError:
    METRICS_ENABLED = False


@dataclass
class ValidationJob:
    """Validation job data structure."""

    event_id: UUID
    project_id: UUID
    pr_number: str
    files: List[str]
    diff: str
    queued_at: datetime
    retry_count: int = 0
    max_retries: int = 3

    @classmethod
    def from_dict(cls, data: dict) -> "ValidationJob":
        """Create job from dict."""
        return cls(
            event_id=UUID(data["event_id"]),
            project_id=UUID(data["project_id"]),
            pr_number=data["pr_number"],
            files=data["files"],
            diff=data["diff"],
            queued_at=datetime.fromisoformat(data["queued_at"]),
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
        )

    def to_dict(self) -> dict:
        """Convert job to dict."""
        return {
            "event_id": str(self.event_id),
            "project_id": str(self.project_id),
            "pr_number": self.pr_number,
            "files": self.files,
            "diff": self.diff,
            "queued_at": self.queued_at.isoformat(),
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
        }


class ValidationWorker:
    """
    Background worker for processing validation queue.

    Polls Redis queue for validation jobs and processes them
    using the ValidationPipeline.

    Usage:
        worker = ValidationWorker(redis_client)
        await worker.start()
    """

    QUEUE_KEY = "validation:queue"
    RETRY_QUEUE_KEY = "validation:retry"
    PROCESSING_KEY = "validation:processing"

    def __init__(
        self,
        redis_client: Any,
        batch_size: int = 10,
        poll_interval: float = 1.0,
    ):
        """
        Initialize worker.

        Args:
            redis_client: Async Redis client
            batch_size: Max jobs to process in parallel
            poll_interval: Seconds between queue polls (when empty)
        """
        self.redis = redis_client
        self.batch_size = batch_size
        self.poll_interval = poll_interval
        self._running = False
        self._shutdown_event = asyncio.Event()

    async def start(self):
        """
        Start the worker.

        Runs until shutdown signal received.
        """
        self._running = True
        logger.info("Validation worker starting")

        # Setup graceful shutdown
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, self._handle_shutdown)

        try:
            while self._running:
                await self._process_queue()
        except asyncio.CancelledError:
            logger.info("Validation worker cancelled")
        finally:
            logger.info("Validation worker stopped")

    def stop(self):
        """Stop the worker gracefully."""
        self._running = False
        self._shutdown_event.set()

    def _handle_shutdown(self):
        """Handle shutdown signal."""
        logger.info("Shutdown signal received")
        self.stop()

    async def _process_queue(self):
        """Process jobs from the queue."""
        try:
            # Get queue size for metrics
            if METRICS_ENABLED:
                queue_size = await self.redis.llen(self.QUEUE_KEY)
                record_queue_size(queue_size)

            # Pop job from queue (blocking with timeout)
            result = await self.redis.blpop(
                self.QUEUE_KEY, timeout=int(self.poll_interval)
            )

            if result is None:
                return  # Timeout, no job available

            _, job_data = result
            job = ValidationJob.from_dict(json.loads(job_data))

            # Record queue wait time
            if METRICS_ENABLED:
                wait_time = (datetime.utcnow() - job.queued_at).total_seconds()
                record_queue_wait(wait_time)

            # Process job
            await self._process_job(job)

        except Exception as e:
            logger.error(f"Queue processing error: {e}", exc_info=True)
            await asyncio.sleep(self.poll_interval)

    async def _process_job(self, job: ValidationJob):
        """
        Process a single validation job.

        Args:
            job: Validation job to process
        """
        logger.info(
            f"Processing validation job {job.event_id}",
            extra={
                "event_id": str(job.event_id),
                "pr_number": job.pr_number,
                "retry_count": job.retry_count,
            },
        )

        try:
            # Mark as processing
            await self.redis.hset(
                self.PROCESSING_KEY,
                str(job.event_id),
                json.dumps({"started_at": datetime.utcnow().isoformat()}),
            )

            # Import here to avoid circular imports
            from app.services.validation_pipeline import validation_pipeline

            # Run validation
            result = await validation_pipeline.run(
                event_id=job.event_id,
                project_id=job.project_id,
                pr_number=job.pr_number,
                files=job.files,
                diff=job.diff,
            )

            logger.info(
                f"Validation completed: {result.status.value}",
                extra={
                    "event_id": str(job.event_id),
                    "status": result.status.value,
                    "duration_ms": result.duration_ms,
                },
            )

            # TODO: Update database with result
            # TODO: Post PR comment with result

        except Exception as e:
            logger.error(f"Job processing error: {e}", exc_info=True)

            # Retry if under max retries
            if job.retry_count < job.max_retries:
                job.retry_count += 1
                await self._requeue_job(job)
            else:
                logger.error(
                    f"Job {job.event_id} exceeded max retries, discarding"
                )

        finally:
            # Remove from processing
            await self.redis.hdel(self.PROCESSING_KEY, str(job.event_id))

    async def _requeue_job(self, job: ValidationJob):
        """
        Requeue a job for retry.

        Uses exponential backoff.

        Args:
            job: Job to requeue
        """
        # Calculate backoff delay
        delay = min(2**job.retry_count * 10, 300)  # Max 5 minutes

        logger.info(
            f"Requeuing job {job.event_id} with {delay}s delay",
            extra={
                "event_id": str(job.event_id),
                "retry_count": job.retry_count,
                "delay_seconds": delay,
            },
        )

        # Add to retry queue with delay (using sorted set)
        retry_at = time.time() + delay
        await self.redis.zadd(
            self.RETRY_QUEUE_KEY,
            {json.dumps(job.to_dict()): retry_at},
        )


async def enqueue_validation(
    redis_client: Any,
    event_id: UUID,
    project_id: UUID,
    pr_number: str,
    files: List[str],
    diff: str,
) -> bool:
    """
    Enqueue a validation job.

    Args:
        redis_client: Async Redis client
        event_id: AI code event UUID
        project_id: Project UUID
        pr_number: Pull request number
        files: Changed file paths
        diff: Unified diff

    Returns:
        True if job was queued successfully
    """
    job = ValidationJob(
        event_id=event_id,
        project_id=project_id,
        pr_number=pr_number,
        files=files,
        diff=diff,
        queued_at=datetime.utcnow(),
    )

    try:
        await redis_client.rpush(
            ValidationWorker.QUEUE_KEY,
            json.dumps(job.to_dict()),
        )
        logger.info(f"Queued validation job {event_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to queue validation job: {e}")
        return False
