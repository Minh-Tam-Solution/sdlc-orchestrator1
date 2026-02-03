"""
Background Tasks Package

SDLC Stage: 04 - BUILD
Sprint: 146 - Organization Access Control
Framework: SDLC 5.3.0

Purpose:
Scheduled tasks for maintenance, cleanup, and monitoring.

Tasks:
1. analytics_retention.py - Daily cleanup of analytics_events (90-day retention)
2. evidence_retention.py - Daily cleanup of evidence files (configurable retention)
3. invitation_cleanup.py - Daily cleanup of organization invitations (90-day retention)

Usage:
- Cron jobs: See docs/05-operate/03-Runbooks/
- Manual execution: python -m app.tasks.<task_name>

Celery Beat Schedule (example):
    beat_schedule = {
        'cleanup-analytics': {
            'task': 'app.tasks.analytics_retention.run_retention_cleanup',
            'schedule': crontab(hour=1, minute=0),  # 1:00 AM UTC
        },
        'cleanup-evidence': {
            'task': 'app.tasks.evidence_retention.run_evidence_retention',
            'schedule': crontab(hour=3, minute=0),  # 3:00 AM UTC
        },
        'cleanup-invitations': {
            'task': 'app.tasks.invitation_cleanup.cleanup_expired_invitations_sync',
            'schedule': crontab(hour=2, minute=0),  # 2:00 AM UTC
        },
    }
"""

from app.tasks.analytics_retention import (
    AnalyticsRetentionTask,
    run_retention_cleanup,
)
from app.tasks.invitation_cleanup import (
    InvitationCleanupTask,
    run_invitation_cleanup,
    cleanup_expired_invitations_sync,
)

__all__ = [
    # Analytics retention
    "AnalyticsRetentionTask",
    "run_retention_cleanup",
    # Invitation cleanup (Sprint 146)
    "InvitationCleanupTask",
    "run_invitation_cleanup",
    "cleanup_expired_invitations_sync",
]
