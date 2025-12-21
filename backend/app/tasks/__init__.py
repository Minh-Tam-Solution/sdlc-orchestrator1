"""
Background Tasks Package

SDLC Stage: 04 - BUILD
Sprint: 41 - AI Safety Foundation
Framework: SDLC 5.1.1

Purpose:
Scheduled tasks for maintenance, cleanup, and monitoring.

Tasks:
1. analytics_retention.py - Daily cleanup of analytics_events (90-day retention)
2. ... (future tasks)

Usage:
- Cron jobs: See docs/05-operate/03-Runbooks/Analytics-Retention-Cleanup.md
- Manual execution: python -m app.tasks.analytics_retention
"""

from app.tasks.analytics_retention import (
    AnalyticsRetentionTask,
    run_retention_cleanup,
)

__all__ = [
    "AnalyticsRetentionTask",
    "run_retention_cleanup",
]
