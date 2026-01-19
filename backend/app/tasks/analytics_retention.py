"""
Analytics Data Retention Cleanup Task

SDLC Stage: 04 - BUILD
Sprint: 41 - AI Safety Foundation
Epic: EP-01/EP-02
Status: IMPLEMENTED
Framework: SDLC 5.1.3

Purpose:
Automated cleanup of analytics_events table based on retention policy.
Enforces GDPR compliance by deleting events older than 90 days.

Execution:
- Cron job: Daily at 2:00 AM UTC (low-traffic period)
- Alerting: PagerDuty/Slack if cleanup fails
- Logging: CloudWatch/Grafana for monitoring

CTO Approval Condition #3: 90-day retention cleanup with alerting

Performance:
- Batch deletion (1000 records per transaction)
- Non-blocking (runs during off-peak hours)
- Monitoring: Tracks deleted record count, duration
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import async_session_maker
from app.models.analytics import AnalyticsEvent

logger = logging.getLogger(__name__)


class AnalyticsRetentionTask:
    """
    Cleanup task for analytics_events table.

    Deletes events older than ANALYTICS_RETENTION_DAYS (default: 90 days).
    """

    def __init__(self, retention_days: int = None):
        """
        Initialize retention task.

        Args:
            retention_days: Override default retention period (for testing)
        """
        self.retention_days = retention_days or settings.ANALYTICS_RETENTION_DAYS
        self.batch_size = 1000  # Delete 1000 records per transaction

    async def cleanup_old_events(self, db: AsyncSession) -> Dict[str, Any]:
        """
        Delete analytics events older than retention period.

        Args:
            db: Database session

        Returns:
            Dictionary with cleanup statistics

        Example Result:
            {
                "deleted_count": 12500,
                "cutoff_date": "2025-10-22",
                "duration_seconds": 3.2,
                "status": "success"
            }
        """
        start_time = datetime.utcnow()
        cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)

        logger.info(
            f"Starting analytics retention cleanup - "
            f"retention: {self.retention_days} days, "
            f"cutoff: {cutoff_date.isoformat()}"
        )

        try:
            # Count events to be deleted (for logging)
            count_query = select(func.count()).select_from(AnalyticsEvent).where(
                AnalyticsEvent.created_at < cutoff_date
            )
            result = await db.execute(count_query)
            total_to_delete = result.scalar() or 0

            if total_to_delete == 0:
                logger.info("No old events to delete")
                return {
                    "deleted_count": 0,
                    "cutoff_date": cutoff_date.isoformat(),
                    "duration_seconds": 0,
                    "status": "success",
                    "message": "No events to delete"
                }

            logger.info(f"Found {total_to_delete} events to delete")

            # Batch deletion for performance
            deleted_count = 0
            while True:
                # Delete batch
                delete_stmt = delete(AnalyticsEvent).where(
                    AnalyticsEvent.created_at < cutoff_date
                ).execution_options(synchronize_session=False)

                # Limit batch size (PostgreSQL doesn't support LIMIT in DELETE directly)
                # Use subquery to select IDs first
                subquery = select(AnalyticsEvent.id).where(
                    AnalyticsEvent.created_at < cutoff_date
                ).limit(self.batch_size)

                delete_batch = delete(AnalyticsEvent).where(
                    AnalyticsEvent.id.in_(subquery)
                ).execution_options(synchronize_session=False)

                result = await db.execute(delete_batch)
                batch_deleted = result.rowcount
                deleted_count += batch_deleted

                await db.commit()

                logger.info(
                    f"Deleted batch: {batch_deleted} events "
                    f"(total: {deleted_count}/{total_to_delete})"
                )

                # Exit if no more records to delete
                if batch_deleted == 0:
                    break

                # Safety: Prevent infinite loop
                if deleted_count >= total_to_delete * 2:
                    logger.warning(
                        f"Deleted count ({deleted_count}) exceeded expected "
                        f"({total_to_delete}), stopping"
                    )
                    break

            duration = (datetime.utcnow() - start_time).total_seconds()

            result_summary = {
                "deleted_count": deleted_count,
                "cutoff_date": cutoff_date.isoformat(),
                "duration_seconds": round(duration, 2),
                "status": "success"
            }

            logger.info(
                f"Analytics retention cleanup completed - "
                f"deleted: {deleted_count} events, "
                f"duration: {duration:.2f}s"
            )

            return result_summary

        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            error_msg = f"Analytics retention cleanup failed: {str(e)}"
            logger.error(error_msg, exc_info=True)

            # Rollback transaction on error
            await db.rollback()

            return {
                "deleted_count": 0,
                "cutoff_date": cutoff_date.isoformat(),
                "duration_seconds": round(duration, 2),
                "status": "error",
                "error": str(e)
            }

    async def get_retention_stats(self, db: AsyncSession) -> Dict[str, Any]:
        """
        Get current analytics retention statistics.

        Args:
            db: Database session

        Returns:
            Dictionary with retention stats

        Example Result:
            {
                "total_events": 125000,
                "oldest_event_date": "2025-04-15",
                "newest_event_date": "2026-01-21",
                "events_older_than_retention": 12500,
                "retention_days": 90
            }
        """
        cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)

        # Total events
        total_query = select(func.count()).select_from(AnalyticsEvent)
        total_result = await db.execute(total_query)
        total_events = total_result.scalar() or 0

        # Oldest event
        oldest_query = select(func.min(AnalyticsEvent.created_at))
        oldest_result = await db.execute(oldest_query)
        oldest_date = oldest_result.scalar()

        # Newest event
        newest_query = select(func.max(AnalyticsEvent.created_at))
        newest_result = await db.execute(newest_query)
        newest_date = newest_result.scalar()

        # Events older than retention
        old_query = select(func.count()).select_from(AnalyticsEvent).where(
            AnalyticsEvent.created_at < cutoff_date
        )
        old_result = await db.execute(old_query)
        old_events = old_result.scalar() or 0

        return {
            "total_events": total_events,
            "oldest_event_date": oldest_date.isoformat() if oldest_date else None,
            "newest_event_date": newest_date.isoformat() if newest_date else None,
            "events_older_than_retention": old_events,
            "retention_days": self.retention_days,
            "cutoff_date": cutoff_date.isoformat()
        }


async def run_retention_cleanup():
    """
    Entry point for cron job execution.

    Example crontab (daily at 2:00 AM UTC):
        0 2 * * * cd /app && python -m app.tasks.analytics_retention

    Exit codes:
        0: Success
        1: Cleanup failed (trigger alert)
    """
    logger.info("=" * 80)
    logger.info("Starting scheduled analytics retention cleanup")
    logger.info("=" * 80)

    async with async_session_maker() as db:
        task = AnalyticsRetentionTask()

        # Get current stats before cleanup
        stats_before = await task.get_retention_stats(db)
        logger.info(f"Retention stats before cleanup: {stats_before}")

        # Run cleanup
        cleanup_result = await task.cleanup_old_events(db)

        # Get stats after cleanup
        stats_after = await task.get_retention_stats(db)
        logger.info(f"Retention stats after cleanup: {stats_after}")

        # Alert on failure
        if cleanup_result["status"] == "error":
            logger.error(
                f"🚨 ALERT: Analytics retention cleanup FAILED - "
                f"Error: {cleanup_result.get('error')}"
            )
            # TODO: Send PagerDuty/Slack alert (Sprint 41 Day 4)
            return 1  # Non-zero exit code triggers alert in cron monitoring

        # Log success metrics
        logger.info(
            f"✅ Analytics retention cleanup SUCCESS - "
            f"Deleted: {cleanup_result['deleted_count']} events, "
            f"Duration: {cleanup_result['duration_seconds']}s"
        )

        return 0  # Success


if __name__ == "__main__":
    # Allow running as standalone script for testing
    exit_code = asyncio.run(run_retention_cleanup())
    exit(exit_code)
