"""
Pilot Tracking Service - Sprint 49.

Manages pilot program tracking, TTFV measurement, and satisfaction surveys.

SDLC Stage: 04 - BUILD
Sprint: 49 - EP-06 Pilot Execution + Metrics Hardening
Framework: SDLC 5.1.1

Key Features:
1. Participant management (invite, activate, track)
2. Session tracking with TTFV calculation
3. Satisfaction survey collection
4. Daily metrics aggregation
5. CEO dashboard KPI reporting

Target Metrics:
- 10 Vietnamese SME founders
- TTFV < 30 minutes (1800 seconds)
- Satisfaction score 8/10
- Quality gate pass rate 95%+
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import Integer, and_, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pilot_tracking import (
    PilotParticipant,
    PilotSession,
    PilotSatisfactionSurvey,
    PilotDailyMetrics,
    PilotStatus,
    PilotDomain,
    OnboardingStage,
)
from app.models.user import User

logger = logging.getLogger(__name__)

# Sprint 49 Target Constants
TTFV_TARGET_SECONDS = 1800  # 30 minutes
SATISFACTION_TARGET = 8  # 8/10
QUALITY_GATE_PASS_TARGET = 0.95  # 95%
PILOT_TARGET_COUNT = 10


class PilotTrackingService:
    """
    Service for managing pilot program tracking.

    Handles participant lifecycle, TTFV measurement, and KPI reporting.
    """

    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        self.db = db

    # =========================================================================
    # Participant Management
    # =========================================================================

    async def register_participant(
        self,
        user_id: UUID,
        domain: Optional[str] = None,
        company_name: Optional[str] = None,
        company_size: Optional[str] = None,
        referral_source: Optional[str] = None,
    ) -> PilotParticipant:
        """
        Register a new pilot participant.

        Args:
            user_id: User UUID
            domain: Business domain (fnb, hospitality, retail)
            company_name: Company/business name
            company_size: Size category (micro, small, medium)
            referral_source: How they joined the pilot

        Returns:
            New or existing PilotParticipant
        """
        # Check if already registered
        result = await self.db.execute(
            select(PilotParticipant).where(PilotParticipant.user_id == user_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            logger.info(f"Participant already registered: {user_id}")
            return existing

        participant = PilotParticipant(
            user_id=user_id,
            status=PilotStatus.REGISTERED.value,
            domain=domain,
            company_name=company_name,
            company_size=company_size,
            referral_source=referral_source,
            registered_at=datetime.now(timezone.utc),
        )

        self.db.add(participant)
        await self.db.commit()
        await self.db.refresh(participant)

        logger.info(f"Registered new pilot participant: {participant.id}")
        return participant

    async def get_participant(self, user_id: UUID) -> Optional[PilotParticipant]:
        """Get participant by user ID."""
        result = await self.db.execute(
            select(PilotParticipant).where(PilotParticipant.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_participant_by_id(self, participant_id: UUID) -> Optional[PilotParticipant]:
        """Get participant by participant ID."""
        result = await self.db.execute(
            select(PilotParticipant).where(PilotParticipant.id == participant_id)
        )
        return result.scalar_one_or_none()

    async def update_participant_status(
        self, participant_id: UUID, status: PilotStatus
    ) -> Optional[PilotParticipant]:
        """Update participant status."""
        participant = await self.get_participant_by_id(participant_id)
        if not participant:
            return None

        participant.status = status.value

        # Track activation
        if status == PilotStatus.ACTIVE and not participant.activated_at:
            participant.activated_at = datetime.now(timezone.utc)

        await self.db.commit()
        await self.db.refresh(participant)

        logger.info(f"Updated participant {participant_id} status to {status.value}")
        return participant

    async def list_participants(
        self,
        status: Optional[PilotStatus] = None,
        domain: Optional[PilotDomain] = None,
        limit: int = 100,
    ) -> List[PilotParticipant]:
        """List pilot participants with optional filters."""
        stmt = select(PilotParticipant)

        if status:
            stmt = stmt.where(PilotParticipant.status == status.value)
        if domain:
            stmt = stmt.where(PilotParticipant.domain == domain.value)

        stmt = stmt.order_by(PilotParticipant.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # =========================================================================
    # Session Tracking (TTFV)
    # =========================================================================

    async def start_session(
        self,
        participant_id: UUID,
        onboarding_session_id: Optional[str] = None,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> PilotSession:
        """
        Start a new pilot session (TTFV timer begins).

        Args:
            participant_id: Pilot participant UUID
            onboarding_session_id: Links to OnboardingSession
            user_agent: Browser user agent
            ip_address: Client IP

        Returns:
            New PilotSession
        """
        session = PilotSession(
            participant_id=participant_id,
            onboarding_session_id=onboarding_session_id,
            started_at=datetime.now(timezone.utc),
            current_stage=OnboardingStage.STARTED.value,
            stage_history=[{
                "stage": OnboardingStage.STARTED.value,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }],
            user_agent=user_agent,
            ip_address=ip_address,
        )

        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)

        # Update participant session count
        participant = await self.get_participant_by_id(participant_id)
        if participant:
            participant.total_sessions = (participant.total_sessions or 0) + 1
            await self.db.commit()

        logger.info(f"Started pilot session {session.id} for participant {participant_id}")
        return session

    async def update_session_stage(
        self,
        session_id: UUID,
        stage: OnboardingStage,
        metadata: Optional[Dict[str, Any]] = None,
        domain: Optional[str] = None,
        app_name: Optional[str] = None,
        selected_features: Optional[List[str]] = None,
        scale: Optional[str] = None,
    ) -> Optional[PilotSession]:
        """
        Update session to a new stage.

        Args:
            session_id: Session UUID
            stage: New stage
            metadata: Optional stage-specific data

        Returns:
            Updated PilotSession
        """
        result = await self.db.execute(
            select(PilotSession).where(PilotSession.id == session_id)
        )
        session = result.scalar_one_or_none()

        if not session:
            return None

        now = datetime.now(timezone.utc)

        if domain is not None:
            session.domain = domain
        if app_name is not None:
            session.app_name = app_name
        if selected_features is not None:
            session.selected_features = selected_features
        if scale is not None:
            session.scale = scale

        session.current_stage = stage.value

        # Update stage history
        history = session.stage_history or []
        history.append({
            "stage": stage.value,
            "timestamp": now.isoformat(),
            "metadata": metadata,
        })
        session.stage_history = history

        # Set stage-specific timestamps
        stage_timestamps = {
            OnboardingStage.DOMAIN_SELECTED: "domain_selected_at",
            OnboardingStage.APP_NAMED: "app_named_at",
            OnboardingStage.FEATURES_SELECTED: "features_selected_at",
            OnboardingStage.SCALE_SELECTED: "scale_selected_at",
            OnboardingStage.BLUEPRINT_GENERATED: "blueprint_generated_at",
            OnboardingStage.CODE_GENERATING: "code_generation_started_at",
            OnboardingStage.CODE_GENERATED: "code_generation_completed_at",
            OnboardingStage.QUALITY_GATE_PASSED: "quality_gate_passed_at",
            OnboardingStage.DEPLOYED: "deployed_at",
        }

        if stage in stage_timestamps:
            setattr(session, stage_timestamps[stage], now)

        # If quality gate passed, calculate TTFV
        if stage == OnboardingStage.QUALITY_GATE_PASSED:
            session.update_ttfv()
            session.completed_at = now

            # Update participant metrics
            await self._update_participant_on_completion(session)

        await self.db.commit()
        await self.db.refresh(session)

        logger.info(f"Session {session_id} progressed to stage {stage.value}")
        return session

    async def record_generation_result(
        self,
        session_id: UUID,
        provider: str,
        generation_time_ms: int,
        tokens_used: int,
        files_generated: int,
        lines_of_code: int,
        quality_gate_passed: bool,
        quality_gate_score: Optional[float] = None,
        quality_gate_details: Optional[Dict] = None,
    ) -> Optional[PilotSession]:
        """
        Record code generation results for a session.

        Args:
            session_id: Session UUID
            provider: AI provider used (ollama, claude, etc)
            generation_time_ms: Time taken for generation
            tokens_used: Total tokens consumed
            files_generated: Number of files generated
            lines_of_code: Total lines of code
            quality_gate_passed: Whether quality gate passed
            quality_gate_score: Quality score (0-100)
            quality_gate_details: Detailed quality results

        Returns:
            Updated PilotSession
        """
        session = await self.get_session(session_id)

        if not session:
            return None

        session.generation_provider = provider
        session.generation_time_ms = generation_time_ms
        session.tokens_used = tokens_used
        session.files_generated = files_generated
        session.lines_of_code = lines_of_code
        session.quality_gate_passed = quality_gate_passed
        session.quality_gate_score = quality_gate_score
        session.quality_gate_details = quality_gate_details

        # Update stage based on quality gate result
        if quality_gate_passed:
            await self.db.flush()
            return await self.update_session_stage(
                session_id,
                OnboardingStage.QUALITY_GATE_PASSED,
                metadata={"source": "generation_result"},
            )

        session.current_stage = OnboardingStage.CODE_GENERATED.value
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def record_session_error(
        self,
        session_id: UUID,
        error: Dict[str, Any],
    ) -> Optional[PilotSession]:
        """Record an error during session."""
        session = await self.get_session(session_id)

        if not session:
            return None

        errors = session.errors or []
        errors.append({
            **error,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        session.errors = errors
        session.error_count = len(errors)

        await self.db.commit()
        return session

    async def abandon_session(self, session_id: UUID) -> Optional[PilotSession]:
        """Mark session as abandoned."""
        session = await self.get_session(session_id)

        if not session:
            return None

        session.abandoned_at = datetime.now(timezone.utc)
        await self.db.commit()

        logger.info(f"Session {session_id} marked as abandoned at stage {session.current_stage}")
        return session

    async def get_session(self, session_id: UUID) -> Optional[PilotSession]:
        """Get session by ID."""
        result = await self.db.execute(select(PilotSession).where(PilotSession.id == session_id))
        return result.scalar_one_or_none()

    async def get_participant_sessions(
        self,
        participant_id: UUID,
        limit: int = 10,
    ) -> List[PilotSession]:
        """Get sessions for a participant."""
        stmt = (
            select(PilotSession)
            .where(PilotSession.participant_id == participant_id)
            .order_by(PilotSession.started_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def _update_participant_on_completion(self, session: PilotSession) -> None:
        """Update participant metrics when session completes."""
        participant = await self.get_participant_by_id(session.participant_id)
        if not participant:
            return

        # Update generation counts
        participant.total_generations = (participant.total_generations or 0) + 1
        if session.quality_gate_passed:
            participant.successful_generations = (participant.successful_generations or 0) + 1
            participant.quality_gate_passes = (participant.quality_gate_passes or 0) + 1
        else:
            participant.quality_gate_failures = (participant.quality_gate_failures or 0) + 1

        # Update TTFV metrics
        if session.ttfv_seconds:
            if not participant.best_ttfv_seconds or session.ttfv_seconds < participant.best_ttfv_seconds:
                participant.best_ttfv_seconds = session.ttfv_seconds

            # Calculate average TTFV
            total = participant.successful_generations or 1
            current_avg = participant.avg_ttfv_seconds or session.ttfv_seconds
            participant.avg_ttfv_seconds = int(
                (current_avg * (total - 1) + session.ttfv_seconds) / total
            )

        # Activate participant if first successful generation
        if participant.status != PilotStatus.ACTIVE.value and session.quality_gate_passed:
            participant.status = PilotStatus.ACTIVE.value
            participant.activated_at = datetime.now(timezone.utc)

        # No commit here; caller owns transaction.

    # =========================================================================
    # Satisfaction Surveys
    # =========================================================================

    async def submit_satisfaction_survey(
        self,
        participant_id: UUID,
        session_id: Optional[UUID],
        overall_score: int,
        would_recommend: Optional[bool] = None,
        ease_of_use_score: Optional[int] = None,
        code_quality_score: Optional[int] = None,
        speed_score: Optional[int] = None,
        what_went_well: Optional[str] = None,
        what_needs_improvement: Optional[str] = None,
        feature_requests: Optional[str] = None,
        bugs_reported: Optional[str] = None,
        feedback_context: str = "post_generation",
    ) -> PilotSatisfactionSurvey:
        """
        Submit a satisfaction survey.

        Args:
            participant_id: Participant UUID
            session_id: Related session UUID (optional)
            overall_score: Overall satisfaction (1-10)
            would_recommend: NPS indicator
            ease_of_use_score: Ease of use rating (1-10)
            code_quality_score: Code quality rating (1-10)
            speed_score: Speed rating (1-10)
            what_went_well: Positive feedback
            what_needs_improvement: Improvement suggestions
            feature_requests: Requested features
            bugs_reported: Reported bugs
            feedback_context: Context (post_generation, weekly, exit)

        Returns:
            New PilotSatisfactionSurvey
        """
        survey = PilotSatisfactionSurvey(
            participant_id=participant_id,
            session_id=session_id,
            overall_score=overall_score,
            would_recommend=would_recommend,
            ease_of_use_score=ease_of_use_score,
            code_quality_score=code_quality_score,
            speed_score=speed_score,
            what_went_well=what_went_well,
            what_needs_improvement=what_needs_improvement,
            feature_requests=feature_requests,
            bugs_reported=bugs_reported,
            feedback_context=feedback_context,
            submitted_at=datetime.now(timezone.utc),
        )

        self.db.add(survey)
        await self.db.commit()
        await self.db.refresh(survey)

        # Update participant satisfaction
        participant = await self.get_participant_by_id(participant_id)
        if participant:
            participant.latest_satisfaction_score = overall_score
            participant.would_recommend = would_recommend
            await self.db.commit()

        logger.info(f"Satisfaction survey submitted: {survey.id}, score: {overall_score}")
        return survey

    # =========================================================================
    # Metrics & Reporting
    # =========================================================================

    async def get_pilot_summary(self) -> Dict[str, Any]:
        """
        Get overall pilot program summary for CEO dashboard.

        Returns:
            Dict with key pilot metrics
        """
        now = datetime.now(timezone.utc)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Participant counts
        total_participants = (
            await self.db.execute(select(func.count(PilotParticipant.id)))
        ).scalar_one() or 0
        active_participants = (
            await self.db.execute(
                select(func.count(PilotParticipant.id)).where(
                    PilotParticipant.status == PilotStatus.ACTIVE.value
                )
            )
        ).scalar_one() or 0

        # Session metrics
        total_sessions = (
            await self.db.execute(select(func.count(PilotSession.id)))
        ).scalar_one() or 0
        completed_sessions = (
            await self.db.execute(
                select(func.count(PilotSession.id)).where(PilotSession.completed_at.isnot(None))
            )
        ).scalar_one() or 0

        # TTFV metrics
        ttfv_stats_row = (
            await self.db.execute(
                select(
                    func.avg(PilotSession.ttfv_seconds).label("avg"),
                    func.min(PilotSession.ttfv_seconds).label("min"),
                    func.percentile_cont(0.5).within_group(PilotSession.ttfv_seconds).label("p50"),
                    func.percentile_cont(0.9).within_group(PilotSession.ttfv_seconds).label("p90"),
                ).where(PilotSession.ttfv_seconds.isnot(None))
            )
        ).one_or_none()

        ttfv_target_met = (
            await self.db.execute(
                select(func.count(PilotSession.id)).where(PilotSession.ttfv_target_met == True)
            )
        ).scalar_one() or 0

        # Quality gate metrics
        quality_stats_row = (
            await self.db.execute(
                select(
                    func.count(PilotSession.id).label("total"),
                    func.sum(cast(PilotSession.quality_gate_passed == True, Integer)).label("passed"),
                ).where(PilotSession.quality_gate_passed.isnot(None))
            )
        ).one()

        quality_total = int(quality_stats_row.total or 0)
        quality_passed = int(quality_stats_row.passed or 0)
        quality_gate_rate = (quality_passed / quality_total * 100) if quality_total > 0 else 0

        # Satisfaction metrics
        satisfaction_avg = (
            await self.db.execute(select(func.avg(PilotSatisfactionSurvey.overall_score)))
        ).scalar_one() or 0

        recommend_count = (
            await self.db.execute(
                select(func.count(PilotSatisfactionSurvey.id)).where(
                    PilotSatisfactionSurvey.would_recommend == True
                )
            )
        ).scalar_one() or 0

        # Domain breakdown
        domain_stats = (
            await self.db.execute(
                select(PilotParticipant.domain, func.count(PilotParticipant.id)).group_by(
                    PilotParticipant.domain
                )
            )
        ).all()

        ttfv_avg = None
        ttfv_min = None
        ttfv_p50 = None
        ttfv_p90 = None
        if ttfv_stats_row:
            ttfv_avg = int(ttfv_stats_row.avg) if ttfv_stats_row.avg else None
            ttfv_min = ttfv_stats_row.min
            ttfv_p50 = int(ttfv_stats_row.p50) if ttfv_stats_row.p50 else None
            ttfv_p90 = int(ttfv_stats_row.p90) if ttfv_stats_row.p90 else None

        return {
            "summary": {
                "participants": {
                    "total": total_participants,
                    "target": PILOT_TARGET_COUNT,
                    "active": active_participants,
                    "progress_percent": (total_participants / PILOT_TARGET_COUNT * 100) if PILOT_TARGET_COUNT > 0 else 0,
                },
                "sessions": {
                    "total": total_sessions,
                    "completed": completed_sessions,
                    "completion_rate": (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0,
                },
            },
            "ttfv": {
                "target_seconds": TTFV_TARGET_SECONDS,
                "target_minutes": TTFV_TARGET_SECONDS // 60,
                "avg_seconds": ttfv_avg,
                "min_seconds": ttfv_min,
                "p50_seconds": ttfv_p50,
                "p90_seconds": ttfv_p90,
                "target_met_count": ttfv_target_met,
                "target_met_percent": (ttfv_target_met / completed_sessions * 100) if completed_sessions > 0 else 0,
                "status": "on_track" if (ttfv_p90 or 9999) <= TTFV_TARGET_SECONDS else "needs_attention",
            },
            "quality": {
                "target_percent": QUALITY_GATE_PASS_TARGET * 100,
                "actual_percent": round(quality_gate_rate, 1),
                "total_evaluated": quality_total,
                "passed": quality_passed,
                "status": "on_track" if quality_gate_rate >= QUALITY_GATE_PASS_TARGET * 100 else "needs_attention",
            },
            "satisfaction": {
                "target": SATISFACTION_TARGET,
                "avg_score": round(satisfaction_avg, 1),
                "would_recommend_count": recommend_count,
                "status": "on_track" if satisfaction_avg >= SATISFACTION_TARGET else "needs_attention",
            },
            "domains": {
                domain: count for domain, count in domain_stats
            },
            "overall_status": self._calculate_overall_status(
                total_participants, ttfv_p90, quality_gate_rate, satisfaction_avg
            ),
            "generated_at": now.isoformat(),
        }

    def _calculate_overall_status(
        self,
        participants: int,
        ttfv_p90: Optional[float],
        quality_rate: float,
        satisfaction: float,
    ) -> str:
        """Calculate overall pilot status."""
        score = 0
        max_score = 4

        # Participant progress (25%)
        if participants >= PILOT_TARGET_COUNT:
            score += 1
        elif participants >= PILOT_TARGET_COUNT * 0.5:
            score += 0.5

        # TTFV (25%)
        if ttfv_p90 and ttfv_p90 <= TTFV_TARGET_SECONDS:
            score += 1
        elif ttfv_p90 and ttfv_p90 <= TTFV_TARGET_SECONDS * 1.5:
            score += 0.5

        # Quality gate (25%)
        if quality_rate >= QUALITY_GATE_PASS_TARGET * 100:
            score += 1
        elif quality_rate >= QUALITY_GATE_PASS_TARGET * 100 * 0.9:
            score += 0.5

        # Satisfaction (25%)
        if satisfaction >= SATISFACTION_TARGET:
            score += 1
        elif satisfaction >= SATISFACTION_TARGET * 0.9:
            score += 0.5

        percentage = score / max_score * 100

        if percentage >= 90:
            return "excellent"
        elif percentage >= 75:
            return "on_track"
        elif percentage >= 50:
            return "needs_attention"
        else:
            return "at_risk"

    async def aggregate_daily_metrics(self, date: datetime) -> PilotDailyMetrics:
        """
        Aggregate metrics for a specific day.

        Args:
            date: Date to aggregate

        Returns:
            PilotDailyMetrics for the day
        """
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        # Check if already exists
        existing = (
            await self.db.execute(select(PilotDailyMetrics).where(PilotDailyMetrics.date == start))
        ).scalar_one_or_none()

        if existing:
            metrics = existing
        else:
            metrics = PilotDailyMetrics(date=start)
            self.db.add(metrics)

        # Participant metrics
        metrics.total_participants = (
            await self.db.execute(select(func.count(PilotParticipant.id)))
        ).scalar_one() or 0
        metrics.active_participants = (
            await self.db.execute(
                select(func.count(PilotParticipant.id)).where(
                    PilotParticipant.status == PilotStatus.ACTIVE.value
                )
            )
        ).scalar_one() or 0
        metrics.new_participants = (
            await self.db.execute(
                select(func.count(PilotParticipant.id)).where(
                    and_(
                        PilotParticipant.registered_at >= start,
                        PilotParticipant.registered_at < end,
                    )
                )
            )
        ).scalar_one() or 0

        # Session metrics for the day
        day_sessions_stmt = select(PilotSession).where(
            and_(
                PilotSession.started_at >= start,
                PilotSession.started_at < end,
            )
        )

        metrics.total_sessions = (
            await self.db.execute(select(func.count(PilotSession.id)).where(
                and_(
                    PilotSession.started_at >= start,
                    PilotSession.started_at < end,
                )
            ))
        ).scalar_one() or 0

        metrics.completed_sessions = (
            await self.db.execute(select(func.count(PilotSession.id)).where(
                and_(
                    PilotSession.started_at >= start,
                    PilotSession.started_at < end,
                    PilotSession.completed_at.isnot(None),
                )
            ))
        ).scalar_one() or 0

        metrics.abandoned_sessions = (
            await self.db.execute(select(func.count(PilotSession.id)).where(
                and_(
                    PilotSession.started_at >= start,
                    PilotSession.started_at < end,
                    PilotSession.abandoned_at.isnot(None),
                )
            ))
        ).scalar_one() or 0

        # TTFV metrics
        ttfv_values = list(
            (
                await self.db.execute(
                    select(PilotSession.ttfv_seconds).where(
                        and_(
                            PilotSession.started_at >= start,
                            PilotSession.started_at < end,
                            PilotSession.ttfv_seconds.isnot(None),
                        )
                    )
                )
            ).scalars().all()
        )

        if ttfv_values:
            ttfv_values.sort()
            metrics.ttfv_avg_seconds = int(sum(ttfv_values) / len(ttfv_values))
            metrics.ttfv_min_seconds = min(ttfv_values)
            metrics.ttfv_p50_seconds = ttfv_values[len(ttfv_values) // 2]
            metrics.ttfv_p90_seconds = ttfv_values[int(len(ttfv_values) * 0.9)]
            metrics.ttfv_target_met_count = sum(1 for v in ttfv_values if v <= TTFV_TARGET_SECONDS)
            metrics.ttfv_target_met_percent = metrics.ttfv_target_met_count / len(ttfv_values) * 100

        # Generation metrics
        metrics.total_generations = (
            await self.db.execute(select(func.count(PilotSession.id)).where(
                and_(
                    PilotSession.started_at >= start,
                    PilotSession.started_at < end,
                    PilotSession.quality_gate_passed.isnot(None),
                )
            ))
        ).scalar_one() or 0
        metrics.successful_generations = (
            await self.db.execute(select(func.count(PilotSession.id)).where(
                and_(
                    PilotSession.started_at >= start,
                    PilotSession.started_at < end,
                    PilotSession.quality_gate_passed == True,
                )
            ))
        ).scalar_one() or 0
        metrics.failed_generations = metrics.total_generations - metrics.successful_generations

        if metrics.total_generations > 0:
            metrics.generation_success_rate = metrics.successful_generations / metrics.total_generations * 100

        # Quality gate metrics
        metrics.quality_gates_evaluated = metrics.total_generations
        metrics.quality_gates_passed = metrics.successful_generations
        if metrics.quality_gates_evaluated > 0:
            metrics.quality_gate_pass_rate = metrics.quality_gates_passed / metrics.quality_gates_evaluated * 100

        # Satisfaction metrics
        metrics.feedback_count = (
            await self.db.execute(select(func.count(PilotSatisfactionSurvey.id)).where(
                and_(
                    PilotSatisfactionSurvey.submitted_at >= start,
                    PilotSatisfactionSurvey.submitted_at < end,
                )
            ))
        ).scalar_one() or 0
        avg_score = (
            await self.db.execute(select(func.avg(PilotSatisfactionSurvey.overall_score)).where(
                and_(
                    PilotSatisfactionSurvey.submitted_at >= start,
                    PilotSatisfactionSurvey.submitted_at < end,
                )
            ))
        ).scalar_one()
        metrics.avg_satisfaction_score = float(avg_score) if avg_score else None

        metrics.would_recommend_count = (
            await self.db.execute(select(func.count(PilotSatisfactionSurvey.id)).where(
                and_(
                    PilotSatisfactionSurvey.submitted_at >= start,
                    PilotSatisfactionSurvey.submitted_at < end,
                    PilotSatisfactionSurvey.would_recommend == True,
                )
            ))
        ).scalar_one() or 0
        if metrics.feedback_count > 0:
            metrics.would_recommend_percent = metrics.would_recommend_count / metrics.feedback_count * 100

        # Token/cost metrics
        tokens = (
            await self.db.execute(select(func.sum(PilotSession.tokens_used)).where(
                and_(
                    PilotSession.started_at >= start,
                    PilotSession.started_at < end,
                )
            ))
        ).scalar_one()
        metrics.total_tokens_used = tokens or 0

        # Domain breakdown
        domain_counts = (
            await self.db.execute(
                select(PilotSession.domain, func.count(PilotSession.id))
                .where(
                    and_(
                        PilotSession.started_at >= start,
                        PilotSession.started_at < end,
                    )
                )
                .group_by(PilotSession.domain)
            )
        ).all()

        for domain, count in domain_counts:
            if domain == PilotDomain.FNB.value:
                metrics.fnb_sessions = count
            elif domain == PilotDomain.HOSPITALITY.value:
                metrics.hospitality_sessions = count
            elif domain == PilotDomain.RETAIL.value:
                metrics.retail_sessions = count

        await self.db.commit()
        await self.db.refresh(metrics)

        logger.info(f"Aggregated daily metrics for {start.date()}")
        return metrics


def get_pilot_tracking_service(db: AsyncSession) -> PilotTrackingService:
    """Factory function to create PilotTrackingService."""
    return PilotTrackingService(db)
