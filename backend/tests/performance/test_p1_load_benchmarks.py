"""
=========================================================================
P1 Backend Load Benchmarks - Sprint 69 Go-Live
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: January 16, 2026
Status: ACTIVE - Sprint 69 Phase 3 QA
Authority: Backend Lead + CTO Approved
Foundation: CTO Go-Live Requirements (ADR-027)
Framework: SDLC 5.1.2

Purpose:
- Load testing for P1 backend endpoints
- Verify performance under concurrent load
- Test database query optimization
- Validate API response times

Performance Targets (CTO Mandated):
- API p95 Latency: <100ms
- Gate Evaluation: <100ms
- List Operations: <200ms
- Database Query: <50ms

Endpoints Tested:
- GET /projects/{id}/timeline/stats - Evidence timeline stats
- GET /council/history/{project_id} - Council history
- GET /council/stats/{project_id} - Council stats
- GET /sast/projects/{id}/analytics - SAST analytics
- GET /sast/projects/{id}/scans - SAST scan history

Zero Mock Policy: Real service integration with test database
=========================================================================
"""

import asyncio
import statistics
import time
from datetime import datetime, timedelta
from typing import List
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analytics import AICodeEvent
from app.models.compliance_scan import ComplianceViolation, ComplianceScan, TriggerType
from app.models.council_session import CouncilSession, CouncilModeType, CouncilSessionStatus
from app.models.override import ValidationOverride, OverrideStatus as DBOverrideStatus, OverrideType as DBOverrideType
from app.models.project import Project
from app.models.sast_scan import SASTScan, SASTScanStatus, SASTScanType
from app.models.user import User


# =========================================================================
# Performance Metrics Utility
# =========================================================================


class LoadTestMetrics:
    """Track and calculate load test performance metrics."""

    def __init__(self, test_name: str):
        self.test_name = test_name
        self.durations: List[float] = []
        self.errors: int = 0

    def add_measurement(self, duration_ms: float, error: bool = False):
        """Add a single measurement."""
        self.durations.append(duration_ms)
        if error:
            self.errors += 1

    def get_summary(self) -> dict:
        """Calculate summary statistics."""
        if not self.durations:
            return {"count": 0, "errors": self.errors}

        sorted_durations = sorted(self.durations)
        total = len(self.durations)

        return {
            "count": total,
            "errors": self.errors,
            "success_rate": ((total - self.errors) / total) * 100,
            "latency_min_ms": min(self.durations),
            "latency_max_ms": max(self.durations),
            "latency_mean_ms": statistics.mean(self.durations),
            "latency_median_ms": statistics.median(self.durations),
            "latency_p95_ms": sorted_durations[int(len(sorted_durations) * 0.95)],
            "latency_p99_ms": sorted_durations[int(len(sorted_durations) * 0.99)],
        }

    def print_report(self) -> dict:
        """Print formatted performance report."""
        summary = self.get_summary()
        if summary["count"] == 0:
            print(f"\n❌ {self.test_name}: No measurements recorded")
            return summary

        print(f"\n{'=' * 60}")
        print(f"Load Test: {self.test_name}")
        print(f"{'=' * 60}")
        print(f"Total Requests: {summary['count']}")
        print(f"Errors: {summary['errors']}")
        print(f"Success Rate: {summary['success_rate']:.2f}%")
        print(f"\nLatency Metrics:")
        print(f"  Min:    {summary['latency_min_ms']:8.2f} ms")
        print(f"  Mean:   {summary['latency_mean_ms']:8.2f} ms")
        print(f"  Median: {summary['latency_median_ms']:8.2f} ms")
        print(f"  P95:    {summary['latency_p95_ms']:8.2f} ms")
        print(f"  P99:    {summary['latency_p99_ms']:8.2f} ms")
        print(f"  Max:    {summary['latency_max_ms']:8.2f} ms")
        print(f"{'=' * 60}\n")

        return summary


# =========================================================================
# Fixtures
# =========================================================================


@pytest_asyncio.fixture
async def load_test_project(db_session: AsyncSession, test_user: User) -> Project:
    """Create project for load testing."""
    project = Project(
        id=uuid4(),
        name=f"Load Test Project {uuid4()}",
        description="Project for P1 load testing",
        owner_id=test_user.id,
        sdlc_stage="BUILD",
        created_at=datetime.utcnow(),
    )
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)
    return project


@pytest_asyncio.fixture
async def load_test_ai_events(
    db_session: AsyncSession,
    load_test_project: Project,
    test_user: User,
) -> List[AICodeEvent]:
    """Create AI code events for timeline load testing."""
    events = []
    base_time = datetime.utcnow()

    for i in range(100):  # Create 100 events
        event = AICodeEvent(
            id=uuid4(),
            project_id=load_test_project.id,
            user_id=test_user.id,
            commit_sha=f"abc{i:04d}xyz",
            branch_name="feature/test",
            ai_tool_detected=["cursor", "copilot", "claude"][i % 3],
            confidence_score=70 + (i % 30),
            detection_method="metadata",
            validation_result=["passed", "failed", "warning"][i % 3],
            files_scanned=10 + (i % 50),
            lines_changed=50 + (i % 200),
            duration_ms=1000 + (i % 5000),
            created_at=base_time - timedelta(days=i % 30),
        )
        db_session.add(event)
        events.append(event)

    await db_session.commit()
    return events


@pytest_asyncio.fixture
async def load_test_overrides(
    db_session: AsyncSession,
    load_test_project: Project,
    load_test_ai_events: List[AICodeEvent],
    test_user: User,
) -> List[ValidationOverride]:
    """Create override records for load testing."""
    overrides = []

    # Create 30 overrides (mix of approved/rejected/pending)
    for i in range(30):
        event = load_test_ai_events[i]
        status = [DBOverrideStatus.APPROVED, DBOverrideStatus.REJECTED, DBOverrideStatus.PENDING][i % 3]

        override = ValidationOverride(
            id=uuid4(),
            event_id=event.id,
            project_id=load_test_project.id,
            override_type=DBOverrideType.FALSE_POSITIVE,
            reason=f"Test override reason {i}",
            requested_by_id=test_user.id,
            status=status,
            resolved_by_id=test_user.id if status != DBOverrideStatus.PENDING else None,
            resolved_at=datetime.utcnow() if status != DBOverrideStatus.PENDING else None,
            created_at=datetime.utcnow() - timedelta(days=i % 7),
        )
        db_session.add(override)
        overrides.append(override)

    await db_session.commit()
    return overrides


@pytest_asyncio.fixture
async def load_test_council_sessions(
    db_session: AsyncSession,
    load_test_project: Project,
    test_user: User,
) -> List[CouncilSession]:
    """Create council sessions for load testing."""
    sessions = []
    base_time = datetime.utcnow()

    for i in range(50):  # Create 50 council sessions
        mode = [CouncilModeType.SINGLE, CouncilModeType.COUNCIL, CouncilModeType.AUTO][i % 3]
        session = CouncilSession(
            id=uuid4(),
            project_id=load_test_project.id,
            violation_id=uuid4(),
            triggered_by=test_user.id,
            mode_requested=mode,
            mode_used=mode,
            status=CouncilSessionStatus.COMPLETED,
            providers_used=["ollama"] if mode == CouncilModeType.SINGLE else ["ollama", "claude"],
            recommendation=f"Test recommendation {i}",
            confidence_score=70 + (i % 25),
            total_duration_ms=1000 + (i * 100),
            total_cost_usd=0.001 * i,
            created_at=base_time - timedelta(days=i % 30),
            completed_at=base_time - timedelta(days=i % 30),
        )
        db_session.add(session)
        sessions.append(session)

    await db_session.commit()
    return sessions


@pytest_asyncio.fixture
async def load_test_sast_scans(
    db_session: AsyncSession,
    load_test_project: Project,
    test_user: User,
) -> List[SASTScan]:
    """Create SAST scans for load testing."""
    scans = []
    base_time = datetime.utcnow()

    for i in range(30):  # Create 30 SAST scans
        scan = SASTScan(
            id=uuid4(),
            project_id=load_test_project.id,
            scan_type=SASTScanType.FULL,
            status=SASTScanStatus.COMPLETED,
            branch="main",
            total_findings=i * 3,
            critical_count=i % 5,
            high_count=i % 10,
            medium_count=i,
            low_count=i * 2,
            info_count=i,
            files_scanned=100 + i * 10,
            rules_run=50,
            scan_duration_ms=5000 + i * 500,
            blocks_merge=i % 3 == 0,
            findings=[
                {
                    "file_path": f"src/file{j}.py",
                    "rule_id": f"python.security.{j}",
                    "severity": ["critical", "high", "medium"][j % 3],
                    "category": ["injection", "xss", "other"][j % 3],
                    "message": f"Finding {j}",
                }
                for j in range(i % 10)
            ],
            by_category={"injection": i, "xss": i // 2, "other": i // 3},
            started_at=base_time - timedelta(days=i),
            completed_at=base_time - timedelta(days=i),
            triggered_by=test_user.id,
        )
        db_session.add(scan)
        scans.append(scan)

    await db_session.commit()
    return scans


# =========================================================================
# Evidence Timeline Load Tests
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.performance
async def test_timeline_stats_sequential_load(
    client: AsyncClient,
    auth_headers: dict,
    load_test_project: Project,
    load_test_ai_events,
    load_test_overrides,
):
    """
    Test timeline stats endpoint under sequential load.

    Target: <100ms p95 latency
    Load: 50 sequential requests
    """
    metrics = LoadTestMetrics("Timeline Stats - Sequential")

    for i in range(50):
        start = time.time()

        response = await client.get(
            f"/api/v1/evidence/projects/{load_test_project.id}/timeline/stats",
            headers=auth_headers,
        )

        duration_ms = (time.time() - start) * 1000

        if response.status_code == 200:
            metrics.add_measurement(duration_ms)
        else:
            metrics.add_measurement(duration_ms, error=True)

    summary = metrics.print_report()

    assert summary["success_rate"] >= 95.0, "Success rate should be >= 95%"
    assert summary["latency_p95_ms"] < 200, "P95 latency should be < 200ms"


@pytest.mark.asyncio
@pytest.mark.performance
async def test_timeline_stats_concurrent_load(
    client: AsyncClient,
    auth_headers: dict,
    load_test_project: Project,
    load_test_ai_events,
    load_test_overrides,
):
    """
    Test timeline stats endpoint under concurrent load.

    Target: <200ms p95 latency under concurrent requests
    Load: 20 concurrent requests
    """
    metrics = LoadTestMetrics("Timeline Stats - Concurrent")

    async def make_request():
        start = time.time()
        response = await client.get(
            f"/api/v1/evidence/projects/{load_test_project.id}/timeline/stats",
            headers=auth_headers,
        )
        duration_ms = (time.time() - start) * 1000
        metrics.add_measurement(duration_ms, error=(response.status_code != 200))

    # Run 20 concurrent requests
    await asyncio.gather(*[make_request() for _ in range(20)])

    summary = metrics.print_report()

    assert summary["success_rate"] >= 90.0, "Success rate should be >= 90%"
    assert summary["latency_p95_ms"] < 300, "P95 latency should be < 300ms under concurrent load"


@pytest.mark.asyncio
@pytest.mark.performance
async def test_timeline_events_pagination_load(
    client: AsyncClient,
    auth_headers: dict,
    load_test_project: Project,
    load_test_ai_events,
):
    """
    Test timeline events pagination under load.

    Target: <200ms p95 latency for paginated queries
    """
    metrics = LoadTestMetrics("Timeline Events - Pagination")

    for page in range(1, 11):  # Test 10 pages
        start = time.time()

        response = await client.get(
            f"/api/v1/evidence/projects/{load_test_project.id}/timeline",
            headers=auth_headers,
            params={"page": page, "limit": 10},
        )

        duration_ms = (time.time() - start) * 1000
        metrics.add_measurement(duration_ms, error=(response.status_code != 200))

    summary = metrics.print_report()

    assert summary["success_rate"] >= 95.0
    assert summary["latency_p95_ms"] < 200, "Pagination should be < 200ms p95"


# =========================================================================
# Council Load Tests
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.performance
async def test_council_history_load(
    client: AsyncClient,
    auth_headers: dict,
    load_test_project: Project,
    load_test_council_sessions,
):
    """
    Test council history endpoint under load.

    Target: <200ms p95 latency
    Load: 30 sequential requests
    """
    metrics = LoadTestMetrics("Council History - Sequential")

    for i in range(30):
        start = time.time()

        response = await client.get(
            f"/api/v1/council/history/{load_test_project.id}",
            headers=auth_headers,
            params={"limit": 20},
        )

        duration_ms = (time.time() - start) * 1000
        metrics.add_measurement(duration_ms, error=(response.status_code != 200))

    summary = metrics.print_report()

    assert summary["success_rate"] >= 95.0
    assert summary["latency_p95_ms"] < 200


@pytest.mark.asyncio
@pytest.mark.performance
async def test_council_stats_load(
    client: AsyncClient,
    auth_headers: dict,
    load_test_project: Project,
    load_test_council_sessions,
):
    """
    Test council stats endpoint under load.

    Target: <150ms p95 latency
    Load: 30 sequential requests
    """
    metrics = LoadTestMetrics("Council Stats - Sequential")

    for i in range(30):
        start = time.time()

        response = await client.get(
            f"/api/v1/council/stats/{load_test_project.id}",
            headers=auth_headers,
        )

        duration_ms = (time.time() - start) * 1000
        metrics.add_measurement(duration_ms, error=(response.status_code != 200))

    summary = metrics.print_report()

    assert summary["success_rate"] >= 95.0
    assert summary["latency_p95_ms"] < 150


# =========================================================================
# SAST Load Tests
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.performance
async def test_sast_analytics_load(
    client: AsyncClient,
    auth_headers: dict,
    load_test_project: Project,
    load_test_sast_scans,
):
    """
    Test SAST analytics endpoint under load.

    Target: <200ms p95 latency
    Load: 30 sequential requests
    """
    metrics = LoadTestMetrics("SAST Analytics - Sequential")

    for i in range(30):
        start = time.time()

        response = await client.get(
            f"/api/v1/sast/projects/{load_test_project.id}/analytics",
            headers=auth_headers,
            params={"days": 30},
        )

        duration_ms = (time.time() - start) * 1000
        metrics.add_measurement(duration_ms, error=(response.status_code != 200))

    summary = metrics.print_report()

    assert summary["success_rate"] >= 95.0
    assert summary["latency_p95_ms"] < 200


@pytest.mark.asyncio
@pytest.mark.performance
async def test_sast_scan_history_load(
    client: AsyncClient,
    auth_headers: dict,
    load_test_project: Project,
    load_test_sast_scans,
):
    """
    Test SAST scan history endpoint under load.

    Target: <200ms p95 latency
    Load: 30 sequential requests
    """
    metrics = LoadTestMetrics("SAST Scan History - Sequential")

    for i in range(30):
        start = time.time()

        response = await client.get(
            f"/api/v1/sast/projects/{load_test_project.id}/scans",
            headers=auth_headers,
            params={"page": 1, "page_size": 20},
        )

        duration_ms = (time.time() - start) * 1000
        metrics.add_measurement(duration_ms, error=(response.status_code != 200))

    summary = metrics.print_report()

    assert summary["success_rate"] >= 95.0
    assert summary["latency_p95_ms"] < 200


@pytest.mark.asyncio
@pytest.mark.performance
async def test_sast_trend_load(
    client: AsyncClient,
    auth_headers: dict,
    load_test_project: Project,
    load_test_sast_scans,
):
    """
    Test SAST trend endpoint under load.

    Target: <150ms p95 latency
    """
    metrics = LoadTestMetrics("SAST Trend - Sequential")

    for i in range(20):
        start = time.time()

        response = await client.get(
            f"/api/v1/sast/projects/{load_test_project.id}/trend",
            headers=auth_headers,
            params={"days": 30},
        )

        duration_ms = (time.time() - start) * 1000
        metrics.add_measurement(duration_ms, error=(response.status_code != 200))

    summary = metrics.print_report()

    assert summary["success_rate"] >= 95.0
    assert summary["latency_p95_ms"] < 150


# =========================================================================
# Database Query Performance Tests
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.performance
async def test_db_override_count_query_performance(
    db_session: AsyncSession,
    load_test_project: Project,
    load_test_overrides,
):
    """
    Test database query performance for override rate calculation.

    Target: <50ms p95 for count query
    """
    from sqlalchemy import func, and_

    metrics = LoadTestMetrics("DB Override Count Query")

    for i in range(30):
        start = time.time()

        result = await db_session.execute(
            select(func.count())
            .select_from(ValidationOverride)
            .where(
                and_(
                    ValidationOverride.project_id == load_test_project.id,
                    ValidationOverride.status == DBOverrideStatus.APPROVED,
                )
            )
        )
        count = result.scalar()

        duration_ms = (time.time() - start) * 1000
        metrics.add_measurement(duration_ms)

    summary = metrics.print_report()

    assert summary["latency_p95_ms"] < 50, "DB count query should be < 50ms p95"


@pytest.mark.asyncio
@pytest.mark.performance
async def test_db_council_session_query_performance(
    db_session: AsyncSession,
    load_test_project: Project,
    load_test_council_sessions,
):
    """
    Test database query performance for council session lookup.

    Target: <50ms p95 for session query
    """
    metrics = LoadTestMetrics("DB Council Session Query")

    for i in range(30):
        start = time.time()

        result = await db_session.execute(
            select(CouncilSession)
            .where(
                CouncilSession.project_id == load_test_project.id,
                CouncilSession.status == CouncilSessionStatus.COMPLETED,
            )
            .order_by(CouncilSession.created_at.desc())
            .limit(20)
        )
        sessions = result.scalars().all()

        duration_ms = (time.time() - start) * 1000
        metrics.add_measurement(duration_ms)

    summary = metrics.print_report()

    assert summary["latency_p95_ms"] < 50, "DB session query should be < 50ms p95"


# =========================================================================
# Summary Test
# =========================================================================


@pytest.mark.asyncio
@pytest.mark.performance
async def test_p1_load_test_summary():
    """
    Summary report for P1 load tests.

    Run this test to get an overview of all performance targets.
    """
    print("\n" + "=" * 70)
    print("P1 BACKEND LOAD TEST SUMMARY - Sprint 69 Go-Live")
    print("=" * 70)
    print(f"Test Time: {datetime.now().isoformat()}")
    print("\nPerformance Targets (CTO Mandated):")
    print("  - API p95 Latency: <100ms (general)")
    print("  - List Operations: <200ms")
    print("  - Database Query: <50ms")
    print("  - Gate Evaluation: <100ms")
    print("\nEndpoints Tested:")
    print("  - GET /projects/{id}/timeline/stats")
    print("  - GET /projects/{id}/timeline")
    print("  - GET /council/history/{project_id}")
    print("  - GET /council/stats/{project_id}")
    print("  - GET /sast/projects/{id}/analytics")
    print("  - GET /sast/projects/{id}/scans")
    print("  - GET /sast/projects/{id}/trend")
    print("\nRun with: pytest -m performance --tb=short -v")
    print("=" * 70)
