"""
=========================================================================
Background Jobs Package - SDLC Orchestrator
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: November 28, 2025
Status: ACTIVE - Sprint 16 Day 4
Authority: Backend Lead + DevOps Lead Approved
Foundation: Sprint 16 Testing & Documentation Plan
Framework: SDLC 4.9 Complete Lifecycle

Purpose:
- Background task definitions (FastAPI BackgroundTasks)
- Scheduled job configurations
- GitHub sync polling jobs
- Webhook processing jobs

Modules:
- github_sync.py: GitHub repository synchronization jobs
- scheduled.py: Scheduled job configurations (APScheduler)

Zero Mock Policy: Production-ready implementations
=========================================================================
"""

from app.jobs.github_sync import (
    run_github_sync_job,
    run_webhook_processing_job,
    schedule_project_sync,
    process_webhook_event,
)

__all__ = [
    "run_github_sync_job",
    "run_webhook_processing_job",
    "schedule_project_sync",
    "process_webhook_event",
]
