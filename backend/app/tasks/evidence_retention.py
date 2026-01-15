"""
=========================================================================
Evidence Retention Cleanup Task
ADR-027 Phase 3 - Lifecycle Setting: evidence_retention_days
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: 2026-01-15
Status: ACTIVE - ADR-027 Phase 3 (Lifecycle)
Authority: Backend Lead + CTO Approved
Ticket: SDLC-ADR027-601

Purpose:
Automated cleanup and archival of evidence files based on retention policy.
Enforces compliance by soft-deleting evidence older than configured retention days.

Architecture:
1. Reads evidence_retention_days from SettingsService (database-driven)
2. Soft-deletes evidence records (sets deleted_at timestamp)
3. Optionally purges MinIO files for evidence beyond grace period
4. Maintains audit log for all retention actions

Execution:
- Cron job: Daily at 3:00 AM UTC (after analytics cleanup at 2:00 AM)
- Alerting: PagerDuty/Slack if cleanup fails
- Logging: CloudWatch/Grafana for monitoring

Performance:
- Batch processing (100 records per transaction)
- Non-blocking (runs during off-peak hours)
- Monitoring: Tracks archived count, purged count, duration

Zero Mock Policy: 100% real implementation
=========================================================================
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_maker
from app.models.gate_evidence import GateEvidence
from app.services.minio_service import minio_service
from app.services.settings_service import SettingsService

logger = logging.getLogger(__name__)


class EvidenceRetentionTask:
    """
    Cleanup task for gate_evidence table and MinIO storage.

    Evidence Lifecycle (ADR-027 Phase 3):
    1. Active: Evidence < retention_days old
    2. Archived: Evidence >= retention_days (soft-deleted, files retained)
    3. Purged: Evidence >= retention_days + grace_period (files deleted)

    The retention period is read from database via SettingsService,
    allowing runtime configuration without restarting the application.
    """

    # Grace period before purging MinIO files after soft-delete
    GRACE_PERIOD_DAYS = 30

    # Batch size for database operations
    BATCH_SIZE = 100

    def __init__(
        self,
        db: AsyncSession,
        retention_days: int | None = None,
        grace_period_days: int | None = None,
    ):
        """
        Initialize evidence retention task.

        Args:
            db: Database session
            retention_days: Override retention period (for testing)
            grace_period_days: Override grace period (for testing)
        """
        self.db = db
        self._retention_days = retention_days
        self._grace_period_days = grace_period_days or self.GRACE_PERIOD_DAYS

    async def _get_retention_days(self) -> int:
        """
        Get retention days from SettingsService or use override.

        Returns:
            Number of days to retain evidence before archival
        """
        if self._retention_days is not None:
            return self._retention_days

        settings_service = SettingsService(self.db)
        return await settings_service.get_evidence_retention_days()

    async def archive_old_evidence(self) -> dict[str, Any]:
        """
        Soft-delete evidence older than retention period.

        This marks evidence as deleted (sets deleted_at) but retains
        the actual files in MinIO for the grace period.

        Returns:
            Dictionary with archival statistics:
            {
                "archived_count": 125,
                "cutoff_date": "2025-01-15T00:00:00",
                "retention_days": 365,
                "duration_seconds": 2.5,
                "status": "success"
            }
        """
        start_time = datetime.utcnow()
        retention_days = await self._get_retention_days()
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)

        logger.info(
            f"Starting evidence archival - "
            f"retention: {retention_days} days, "
            f"cutoff: {cutoff_date.isoformat()}"
        )

        try:
            # Count evidence to be archived (active evidence older than cutoff)
            count_query = (
                select(func.count())
                .select_from(GateEvidence)
                .where(
                    GateEvidence.uploaded_at < cutoff_date,
                    GateEvidence.deleted_at.is_(None),  # Only active evidence
                )
            )
            result = await self.db.execute(count_query)
            total_to_archive = result.scalar() or 0

            if total_to_archive == 0:
                logger.info("No evidence to archive")
                return {
                    "archived_count": 0,
                    "cutoff_date": cutoff_date.isoformat(),
                    "retention_days": retention_days,
                    "duration_seconds": 0,
                    "status": "success",
                    "message": "No evidence to archive",
                }

            logger.info(f"Found {total_to_archive} evidence records to archive")

            # Batch soft-delete for performance
            archived_count = 0
            while archived_count < total_to_archive:
                # Select batch of IDs to archive
                subquery = (
                    select(GateEvidence.id)
                    .where(
                        GateEvidence.uploaded_at < cutoff_date,
                        GateEvidence.deleted_at.is_(None),
                    )
                    .limit(self.BATCH_SIZE)
                )

                # Update batch (soft-delete)
                update_stmt = (
                    update(GateEvidence)
                    .where(GateEvidence.id.in_(subquery))
                    .values(deleted_at=datetime.utcnow())
                    .execution_options(synchronize_session=False)
                )

                result = await self.db.execute(update_stmt)
                batch_archived = result.rowcount
                archived_count += batch_archived

                await self.db.commit()

                logger.info(
                    f"Archived batch: {batch_archived} evidence "
                    f"(total: {archived_count}/{total_to_archive})"
                )

                # Exit if no more records
                if batch_archived == 0:
                    break

            duration = (datetime.utcnow() - start_time).total_seconds()

            result_summary = {
                "archived_count": archived_count,
                "cutoff_date": cutoff_date.isoformat(),
                "retention_days": retention_days,
                "duration_seconds": round(duration, 2),
                "status": "success",
            }

            logger.info(
                f"Evidence archival completed - "
                f"archived: {archived_count} records, "
                f"duration: {duration:.2f}s"
            )

            return result_summary

        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            error_msg = f"Evidence archival failed: {str(e)}"
            logger.error(error_msg, exc_info=True)

            await self.db.rollback()

            return {
                "archived_count": 0,
                "cutoff_date": cutoff_date.isoformat(),
                "retention_days": retention_days,
                "duration_seconds": round(duration, 2),
                "status": "error",
                "error": str(e),
            }

    async def purge_expired_evidence(self) -> dict[str, Any]:
        """
        Permanently delete evidence files that have been archived beyond grace period.

        Evidence is purged when:
        - It has been soft-deleted (deleted_at is not None)
        - deleted_at is older than grace_period_days

        Returns:
            Dictionary with purge statistics:
            {
                "purged_count": 50,
                "files_deleted": 48,
                "files_failed": 2,
                "cutoff_date": "2024-12-15T00:00:00",
                "grace_period_days": 30,
                "duration_seconds": 5.2,
                "status": "success"
            }
        """
        start_time = datetime.utcnow()
        grace_cutoff = datetime.utcnow() - timedelta(days=self._grace_period_days)

        logger.info(
            f"Starting evidence purge - "
            f"grace_period: {self._grace_period_days} days, "
            f"cutoff: {grace_cutoff.isoformat()}"
        )

        try:
            # Find evidence to purge (soft-deleted beyond grace period)
            purge_query = select(GateEvidence).where(
                GateEvidence.deleted_at.is_not(None),
                GateEvidence.deleted_at < grace_cutoff,
            )
            result = await self.db.execute(purge_query)
            evidence_to_purge = result.scalars().all()

            if not evidence_to_purge:
                logger.info("No evidence to purge")
                return {
                    "purged_count": 0,
                    "files_deleted": 0,
                    "files_failed": 0,
                    "cutoff_date": grace_cutoff.isoformat(),
                    "grace_period_days": self._grace_period_days,
                    "duration_seconds": 0,
                    "status": "success",
                    "message": "No evidence to purge",
                }

            logger.info(f"Found {len(evidence_to_purge)} evidence records to purge")

            # Track file deletion results
            files_deleted = 0
            files_failed = 0
            purged_ids = []

            for evidence in evidence_to_purge:
                # Delete file from MinIO
                if evidence.s3_key:
                    try:
                        minio_service.delete_file(evidence.s3_key)
                        files_deleted += 1
                        logger.debug(f"Deleted MinIO file: {evidence.s3_key}")
                    except Exception as file_err:
                        files_failed += 1
                        logger.warning(
                            f"Failed to delete MinIO file {evidence.s3_key}: {file_err}"
                        )
                        # Continue with database deletion even if file delete fails
                        # (file may have been manually deleted already)

                purged_ids.append(evidence.id)

            # Hard-delete records from database
            if purged_ids:
                delete_stmt = delete(GateEvidence).where(
                    GateEvidence.id.in_(purged_ids)
                )
                await self.db.execute(delete_stmt)
                await self.db.commit()

            duration = (datetime.utcnow() - start_time).total_seconds()

            result_summary = {
                "purged_count": len(purged_ids),
                "files_deleted": files_deleted,
                "files_failed": files_failed,
                "cutoff_date": grace_cutoff.isoformat(),
                "grace_period_days": self._grace_period_days,
                "duration_seconds": round(duration, 2),
                "status": "success" if files_failed == 0 else "partial",
            }

            logger.info(
                f"Evidence purge completed - "
                f"purged: {len(purged_ids)} records, "
                f"files_deleted: {files_deleted}, "
                f"files_failed: {files_failed}, "
                f"duration: {duration:.2f}s"
            )

            return result_summary

        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            error_msg = f"Evidence purge failed: {str(e)}"
            logger.error(error_msg, exc_info=True)

            await self.db.rollback()

            return {
                "purged_count": 0,
                "files_deleted": 0,
                "files_failed": 0,
                "cutoff_date": grace_cutoff.isoformat(),
                "grace_period_days": self._grace_period_days,
                "duration_seconds": round(duration, 2),
                "status": "error",
                "error": str(e),
            }

    async def get_retention_stats(self) -> dict[str, Any]:
        """
        Get current evidence retention statistics.

        Returns:
            Dictionary with retention stats:
            {
                "total_evidence": 5000,
                "active_evidence": 4800,
                "archived_evidence": 180,
                "evidence_due_for_archive": 20,
                "evidence_due_for_purge": 10,
                "oldest_evidence_date": "2024-01-15T10:30:00",
                "newest_evidence_date": "2026-01-15T08:15:00",
                "retention_days": 365,
                "grace_period_days": 30
            }
        """
        retention_days = await self._get_retention_days()
        archive_cutoff = datetime.utcnow() - timedelta(days=retention_days)
        purge_cutoff = datetime.utcnow() - timedelta(days=self._grace_period_days)

        # Total evidence
        total_query = select(func.count()).select_from(GateEvidence)
        total_result = await self.db.execute(total_query)
        total_evidence = total_result.scalar() or 0

        # Active evidence (not soft-deleted)
        active_query = (
            select(func.count())
            .select_from(GateEvidence)
            .where(GateEvidence.deleted_at.is_(None))
        )
        active_result = await self.db.execute(active_query)
        active_evidence = active_result.scalar() or 0

        # Archived evidence (soft-deleted)
        archived_query = (
            select(func.count())
            .select_from(GateEvidence)
            .where(GateEvidence.deleted_at.is_not(None))
        )
        archived_result = await self.db.execute(archived_query)
        archived_evidence = archived_result.scalar() or 0

        # Due for archive (active but older than retention)
        due_archive_query = (
            select(func.count())
            .select_from(GateEvidence)
            .where(
                GateEvidence.uploaded_at < archive_cutoff,
                GateEvidence.deleted_at.is_(None),
            )
        )
        due_archive_result = await self.db.execute(due_archive_query)
        due_for_archive = due_archive_result.scalar() or 0

        # Due for purge (archived beyond grace period)
        due_purge_query = (
            select(func.count())
            .select_from(GateEvidence)
            .where(
                GateEvidence.deleted_at.is_not(None),
                GateEvidence.deleted_at < purge_cutoff,
            )
        )
        due_purge_result = await self.db.execute(due_purge_query)
        due_for_purge = due_purge_result.scalar() or 0

        # Oldest evidence
        oldest_query = select(func.min(GateEvidence.uploaded_at))
        oldest_result = await self.db.execute(oldest_query)
        oldest_date = oldest_result.scalar()

        # Newest evidence
        newest_query = select(func.max(GateEvidence.uploaded_at))
        newest_result = await self.db.execute(newest_query)
        newest_date = newest_result.scalar()

        return {
            "total_evidence": total_evidence,
            "active_evidence": active_evidence,
            "archived_evidence": archived_evidence,
            "evidence_due_for_archive": due_for_archive,
            "evidence_due_for_purge": due_for_purge,
            "oldest_evidence_date": oldest_date.isoformat() if oldest_date else None,
            "newest_evidence_date": newest_date.isoformat() if newest_date else None,
            "retention_days": retention_days,
            "grace_period_days": self._grace_period_days,
            "archive_cutoff_date": archive_cutoff.isoformat(),
            "purge_cutoff_date": purge_cutoff.isoformat(),
        }


async def run_evidence_retention():
    """
    Entry point for cron job execution.

    Performs two-phase cleanup:
    1. Archive: Soft-delete evidence older than retention_days
    2. Purge: Hard-delete evidence archived beyond grace period

    Example crontab (daily at 3:00 AM UTC):
        0 3 * * * cd /app && python -m app.tasks.evidence_retention

    Exit codes:
        0: Success (both phases completed)
        1: Partial failure (one phase failed)
        2: Complete failure (both phases failed)
    """
    logger.info("=" * 80)
    logger.info("Starting scheduled evidence retention cleanup")
    logger.info("=" * 80)

    async with async_session_maker() as db:
        task = EvidenceRetentionTask(db)

        # Get current stats before cleanup
        stats_before = await task.get_retention_stats()
        logger.info(f"Retention stats before cleanup: {stats_before}")

        # Phase 1: Archive old evidence
        archive_result = await task.archive_old_evidence()
        archive_success = archive_result["status"] == "success"

        # Phase 2: Purge expired evidence
        purge_result = await task.purge_expired_evidence()
        purge_success = purge_result["status"] in ("success", "partial")

        # Get stats after cleanup
        stats_after = await task.get_retention_stats()
        logger.info(f"Retention stats after cleanup: {stats_after}")

        # Determine exit code
        if archive_success and purge_success:
            logger.info(
                f"✅ Evidence retention cleanup SUCCESS - "
                f"Archived: {archive_result['archived_count']}, "
                f"Purged: {purge_result['purged_count']}"
            )
            return 0
        elif archive_success or purge_success:
            logger.warning(
                f"⚠️ Evidence retention cleanup PARTIAL - "
                f"Archive: {archive_result['status']}, "
                f"Purge: {purge_result['status']}"
            )
            return 1
        else:
            logger.error(
                f"🚨 ALERT: Evidence retention cleanup FAILED - "
                f"Archive error: {archive_result.get('error')}, "
                f"Purge error: {purge_result.get('error')}"
            )
            return 2


if __name__ == "__main__":
    # Allow running as standalone script for testing
    exit_code = asyncio.run(run_evidence_retention())
    exit(exit_code)
