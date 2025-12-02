"""
=========================================================================
Background Jobs Package - SDLC Orchestrator
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.1.0
Date: December 2, 2025
Status: ACTIVE - Sprint 21 Day 2
Authority: Backend Lead + DevOps Lead Approved
Foundation: Sprint 16 Testing & Documentation Plan, Sprint 21 Compliance Scanner
Framework: SDLC 4.9.1 Complete Lifecycle

Purpose:
- Background task definitions (FastAPI BackgroundTasks)
- Scheduled job configurations (APScheduler)
- GitHub sync polling jobs
- Webhook processing jobs
- Compliance scanning jobs

Modules:
- github_sync.py: GitHub repository synchronization jobs
- compliance_scan.py: Compliance scanning jobs (Sprint 21)

Zero Mock Policy: Production-ready implementations
=========================================================================
"""

from app.jobs.github_sync import (
    run_github_sync_job,
    run_webhook_processing_job,
    schedule_project_sync,
    process_webhook_event,
)

from app.jobs.compliance_scan import (
    schedule_compliance_scan,
    run_compliance_scan_job,
    run_daily_compliance_scan,
    process_scan_queue,
    get_scan_job_status,
    get_queue_status,
    register_scheduled_jobs,
)

__all__ = [
    # GitHub Sync Jobs
    "run_github_sync_job",
    "run_webhook_processing_job",
    "schedule_project_sync",
    "process_webhook_event",
    # Compliance Scan Jobs
    "schedule_compliance_scan",
    "run_compliance_scan_job",
    "run_daily_compliance_scan",
    "process_scan_queue",
    "get_scan_job_status",
    "get_queue_status",
    "register_scheduled_jobs",
]
