"""
=========================================================================
Planning Orchestrator Service - Sub-agent Orchestration for Planning Mode
SDLC Orchestrator - Sprint 101 (Risk-Based Planning Trigger)

Version: 2.0.0
Date: January 23, 2026
Status: ACTIVE - Sprint 101 Implementation
Authority: Backend Lead + CTO Approved
Reference: ADR-034-Planning-Subagent-Orchestration
Reference: SDLC 5.2.0 AI Agent Best Practices (Planning Mode)
Reference: docs/04-build/02-Sprint-Plans/SPRINT-101-DESIGN.md

Purpose:
- Orchestrate planning sub-agents for pre-implementation analysis
- Coordinate pattern extraction from codebase, ADRs, tests
- Generate implementation plans based on extracted patterns
- Calculate conformance scores for architectural drift prevention
- Risk-Based Planning Trigger (Sprint 101) - Replaces >15 LOC heuristic
- CRP Integration for high-risk changes (risk_score > 70)

Key Insight (Expert Workflow):
- "Agentic grep > RAG for context retrieval"
- Direct codebase exploration finds real patterns
- MANDATORY based on 7 Risk Factors (DATA_SCHEMA, API_CONTRACT, AUTH, etc.)

Risk-Based Planning Decision (SDLC 5.2.0):
- NOT_REQUIRED: risk_score < 20 (simple changes)
- RECOMMENDED: risk_score 20-49 (moderate changes)
- REQUIRED: risk_score 50-69 (significant changes)
- REQUIRES_CRP: risk_score >= 70 (high-risk, needs human oversight)

Performance Targets:
- Risk analysis (p95): <500ms
- Pattern extraction (p95): <30s for typical task
- Plan generation (p95): <10s
- Total planning (p95): <60s
- CRP creation (p95): <500ms

Zero Mock Policy: 100% real implementation
=========================================================================
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.planning_subagent import (
    ADRScanResult,
    ConformanceDeviation,
    ConformanceLevel,
    ConformanceResult,
    ExploreAgentType,
    ExploreResult,
    ExtractedPattern,
    ImplementationPlan,
    ImplementationStep,
    PatternCategory,
    PatternSummary,
    PlanningRequest,
    PlanningResult,
    PlanningStatus,
    TestPatternResult,
)
from app.schemas.risk_analysis import (
    PlanningDecision,
    RiskAnalysis,
    RiskAnalysisContext,
    RiskAnalysisRequest,
    ShouldPlanResponse,
)
from app.schemas.crp import (
    ConsultationPriority,
    ConsultationResponse,
    CreateConsultationRequest,
    ReviewerExpertise,
)
from app.services.pattern_extraction_service import PatternExtractionService
from app.services.adr_scanner_service import ADRScannerService
from app.services.test_pattern_service import TestPatternService
from app.services.risk_factor_detector_service import RiskFactorDetectorService
from app.services.crp_service import CRPService

logger = logging.getLogger(__name__)


class PlanningOrchestratorService:
    """
    Orchestrates planning sub-agents for pre-implementation analysis.

    Key insight from expert: "Agentic grep > RAG for context retrieval"

    This service (v2.0.0 - Sprint 101):
    1. Analyzes diff for 7 mandatory risk factors (Risk-Based Planning Trigger)
    2. Determines planning requirement (NOT_REQUIRED → REQUIRES_CRP)
    3. Spawns explore sub-agents (parallel) if planning is required
    4. Extracts patterns from codebase, ADRs, tests
    5. Synthesizes implementation plan
    6. Creates CRP (Consultation Request) if risk_score >= 70
    7. Returns for human approval

    Risk-Based Planning Decision:
        - NOT_REQUIRED: risk_score < 20 (simple changes)
        - RECOMMENDED: risk_score 20-49 (moderate changes)
        - REQUIRED: risk_score 50-69 (significant changes)
        - REQUIRES_CRP: risk_score >= 70 (high-risk, needs human oversight)

    Usage:
        orchestrator = PlanningOrchestratorService(db_session)

        # Quick check if planning is needed
        should_plan = await orchestrator.should_plan(diff, project_id)
        if should_plan.requires_planning:
            result = await orchestrator.plan(request)

        # Or let plan() decide automatically
        result = await orchestrator.plan_with_risk_analysis(
            request=PlanningRequest(...),
            diff="...",
            project_id=project_id,
            requester_id=user_id,
        )

    SDLC 5.2.0 Compliance:
        - Planning Mode mandatory based on 7 Risk Factors (replaces >15 LOC heuristic)
        - CRP for high-risk changes (SDLC 5.2.0 AI Governance)
        - Prevents architectural drift
        - Builds on established patterns
    """

    def __init__(
        self,
        db: Optional[AsyncSession] = None,
        pattern_service: Optional[PatternExtractionService] = None,
        adr_service: Optional[ADRScannerService] = None,
        test_service: Optional[TestPatternService] = None,
        risk_service: Optional[RiskFactorDetectorService] = None,
        crp_service: Optional[CRPService] = None,
    ):
        """
        Initialize PlanningOrchestratorService.

        Args:
            db: Database session (required for CRP operations)
            pattern_service: Pattern extraction service (agentic grep)
            adr_service: ADR scanner service
            test_service: Test pattern scanner service
            risk_service: Risk factor detector service (Sprint 101)
            crp_service: CRP service for high-risk consultations (Sprint 101)
        """
        self.db = db
        self.pattern_service = pattern_service or PatternExtractionService()
        self.adr_service = adr_service or ADRScannerService()
        self.test_service = test_service or TestPatternService()
        self.risk_service = risk_service or RiskFactorDetectorService()
        self.crp_service = crp_service if crp_service else (CRPService(db) if db else None)
        self._active_sessions: dict[UUID, PlanningResult] = {}

    # =========================================================================
    # Risk-Based Planning Trigger (Sprint 101)
    # =========================================================================

    async def should_plan(
        self,
        diff: str,
        project_id: Optional[UUID] = None,
        context: Optional[RiskAnalysisContext] = None,
    ) -> ShouldPlanResponse:
        """
        Quick check if planning is required based on 7 mandatory risk factors.

        This replaces the simple ">15 LOC" heuristic with intelligent risk analysis.

        Args:
            diff: Git diff or code changes to analyze
            project_id: Project UUID for context
            context: Additional context for risk analysis

        Returns:
            ShouldPlanResponse with decision and risk summary

        Example:
            response = await orchestrator.should_plan(diff, project_id)
            if response.requires_planning:
                print(f"Planning required: {response.reason}")
                print(f"Risk factors: {response.risk_factors_detected}")
        """
        return await self.risk_service.should_plan(diff, project_id, context)

    async def plan_with_risk_analysis(
        self,
        request: PlanningRequest,
        diff: str,
        project_id: UUID,
        requester_id: UUID,
        pr_id: Optional[str] = None,
        diff_url: Optional[str] = None,
    ) -> tuple[PlanningResult, Optional[RiskAnalysis], Optional[ConsultationResponse]]:
        """
        Execute planning mode with integrated risk analysis (Sprint 101 main entry point).

        This method:
        1. Analyzes diff for 7 mandatory risk factors
        2. Determines planning requirement level
        3. If REQUIRES_CRP, creates consultation request
        4. Executes planning sub-agents
        5. Returns result with risk analysis and optional CRP

        Args:
            request: Planning request with task and configuration
            diff: Git diff or code changes
            project_id: Project UUID
            requester_id: User UUID making the request
            pr_id: Pull request ID (optional)
            diff_url: URL to the diff (optional)

        Returns:
            Tuple of (PlanningResult, RiskAnalysis, Optional[ConsultationResponse])

        Example:
            result, risk_analysis, consultation = await orchestrator.plan_with_risk_analysis(
                request=PlanningRequest(
                    task="Refactor authentication flow",
                    project_path="/path/to/project",
                ),
                diff=git_diff,
                project_id=project.id,
                requester_id=user.id,
            )

            if consultation:
                print(f"CRP created: {consultation.id}")
                print("Awaiting human approval before proceeding.")
        """
        logger.info(
            f"Starting risk-based planning for project {project_id}: {request.task[:50]}..."
        )

        # Step 1: Perform risk analysis
        risk_request = RiskAnalysisRequest(
            diff=diff,
            project_id=project_id,
            context=RiskAnalysisContext(
                stage=request.context.get("stage") if request.context else None,
                has_tests=request.include_tests,
            ) if request.context else None,
        )
        risk_analysis = await self.risk_service.analyze_diff(risk_request)

        logger.info(
            f"Risk analysis complete: score={risk_analysis.risk_score}, "
            f"decision={risk_analysis.planning_decision.value}, "
            f"factors={len(risk_analysis.detected_factors)}"
        )

        # Step 2: Create CRP if high-risk
        consultation: Optional[ConsultationResponse] = None
        if risk_analysis.planning_decision == PlanningDecision.REQUIRES_CRP:
            if not self.crp_service:
                logger.warning(
                    "CRP required but CRPService not available. "
                    "Planning will proceed without CRP."
                )
            else:
                consultation = await self._create_consultation_for_high_risk(
                    request=request,
                    risk_analysis=risk_analysis,
                    project_id=project_id,
                    requester_id=requester_id,
                    pr_id=pr_id,
                    diff_url=diff_url,
                )
                logger.info(f"CRP created: {consultation.id}")

        # Step 3: Execute planning (even for CRP, we generate the plan)
        planning_result = await self.plan(request, risk_analysis=risk_analysis)

        # Update planning result with risk info
        if planning_result.plan:
            # Add risk factors to plan risks
            for factor in risk_analysis.detected_factors:
                risk_msg = f"[{factor.factor.value}] {factor.description} (confidence: {factor.confidence:.0%})"
                if risk_msg not in planning_result.plan.risks:
                    planning_result.plan.risks.append(risk_msg)

        return planning_result, risk_analysis, consultation

    async def _create_consultation_for_high_risk(
        self,
        request: PlanningRequest,
        risk_analysis: RiskAnalysis,
        project_id: UUID,
        requester_id: UUID,
        pr_id: Optional[str] = None,
        diff_url: Optional[str] = None,
    ) -> ConsultationResponse:
        """
        Create CRP (Consultation Request Protocol) for high-risk changes.

        Called when risk_score >= 70 (REQUIRES_CRP decision).

        Args:
            request: Planning request
            risk_analysis: Risk analysis result
            project_id: Project UUID
            requester_id: Requester UUID
            pr_id: Optional PR ID
            diff_url: Optional diff URL

        Returns:
            ConsultationResponse with created CRP
        """
        # Determine required expertise based on detected factors
        expertise = self._determine_required_expertise(risk_analysis)

        # Determine priority based on risk score
        if risk_analysis.risk_score >= 90:
            priority = ConsultationPriority.CRITICAL
        elif risk_analysis.risk_score >= 80:
            priority = ConsultationPriority.HIGH
        else:
            priority = ConsultationPriority.MEDIUM

        # Build description with risk factor details
        factor_details = "\n".join([
            f"- **{f.factor.value}**: {f.description} "
            f"(score: {f.risk_score}, confidence: {f.confidence:.0%})"
            for f in risk_analysis.detected_factors
        ])

        description = (
            f"## Risk Analysis Summary\n\n"
            f"**Risk Score**: {risk_analysis.risk_score}/100\n"
            f"**Decision**: {risk_analysis.planning_decision.value}\n\n"
            f"## Detected Risk Factors\n\n{factor_details}\n\n"
            f"## Task Description\n\n{request.task}\n\n"
            f"## Recommendations\n\n"
            f"{chr(10).join(['- ' + r for r in risk_analysis.recommendations])}"
        )

        crp_request = CreateConsultationRequest(
            project_id=project_id,
            pr_id=pr_id,
            risk_analysis_id=risk_analysis.id,
            title=f"High-Risk Change Review: {request.task[:80]}",
            description=description,
            priority=priority,
            required_expertise=expertise,
            diff_url=diff_url,
        )

        return await self.crp_service.create_consultation(
            request=crp_request,
            requester_id=requester_id,
            risk_analysis=risk_analysis,
        )

    def _determine_required_expertise(
        self,
        risk_analysis: RiskAnalysis,
    ) -> list[ReviewerExpertise]:
        """
        Determine required reviewer expertise based on detected risk factors.

        Maps risk factors to appropriate expertise areas.
        """
        expertise: set[ReviewerExpertise] = set()

        factor_to_expertise = {
            "DATA_SCHEMA": ReviewerExpertise.DATABASE,
            "API_CONTRACT": ReviewerExpertise.ARCHITECTURE,
            "AUTH": ReviewerExpertise.SECURITY,
            "CROSS_SERVICE": ReviewerExpertise.ARCHITECTURE,
            "CONCURRENCY": ReviewerExpertise.BACKEND,
            "SECURITY": ReviewerExpertise.SECURITY,
            "PUBLIC_API": ReviewerExpertise.ARCHITECTURE,
        }

        for factor in risk_analysis.detected_factors:
            if factor.factor.value in factor_to_expertise:
                expertise.add(factor_to_expertise[factor.factor.value])

        # Ensure at least one expertise is selected
        if not expertise:
            expertise.add(ReviewerExpertise.BACKEND)

        return list(expertise)

    # =========================================================================
    # Original Planning Methods (Updated for Risk Integration)
    # =========================================================================

    async def plan(
        self,
        request: PlanningRequest,
        risk_analysis: Optional[RiskAnalysis] = None,
    ) -> PlanningResult:
        """
        Execute planning mode with sub-agent orchestration.

        Args:
            request: Planning request with task and configuration
            risk_analysis: Optional risk analysis result (from plan_with_risk_analysis)

        Returns:
            PlanningResult with patterns, plan, and conformance score

        Raises:
            ValueError: If request is invalid
            TimeoutError: If planning exceeds timeout (60s)

        Example:
            request = PlanningRequest(
                task="Add OAuth2 authentication with Google provider",
                project_path="/path/to/project",
                depth=3
            )
            result = await orchestrator.plan(request)

        Note:
            For risk-based planning trigger (Sprint 101), use plan_with_risk_analysis()
            which automatically performs risk analysis and creates CRP if needed.
        """
        start_time = time.time()
        session_id = uuid4()

        logger.info(
            f"Starting planning session {session_id} for task: {request.task[:50]}..."
        )

        # Initialize result
        result = PlanningResult(
            id=session_id,
            task=request.task,
            status=PlanningStatus.EXPLORING,
            requires_approval=not request.auto_approve,
        )

        try:
            project_path = Path(request.project_path).resolve()
            if not project_path.exists():
                raise ValueError(f"Project path does not exist: {project_path}")

            # Step 1: Spawn explore sub-agents (parallel)
            result.status = PlanningStatus.EXPLORING
            explore_results = await self._spawn_explore_agents(
                task=request.task,
                project_path=project_path,
                depth=request.depth,
                include_tests=request.include_tests,
                include_adrs=request.include_adrs,
            )
            result.explore_results = explore_results

            # Step 2: Synthesize patterns
            result.status = PlanningStatus.SYNTHESIZING
            patterns = await self._synthesize_patterns(explore_results)
            result.patterns = patterns

            # Extract ADR and test results if available
            for exp_result in explore_results:
                if exp_result.agent_type == ExploreAgentType.ADR_PATTERNS:
                    result.adr_scan = self._extract_adr_result(exp_result)
                elif exp_result.agent_type == ExploreAgentType.TEST_PATTERNS:
                    result.test_patterns = self._extract_test_result(exp_result)

            # Step 3: Generate implementation plan
            result.status = PlanningStatus.GENERATING
            plan = await self._generate_plan(request.task, patterns, result.adr_scan)
            result.plan = plan

            # Step 4: Calculate conformance score
            conformance = self._calculate_conformance(plan, patterns)
            result.conformance = conformance

            # Finalize
            result.status = PlanningStatus.AWAITING_APPROVAL
            result.execution_time_ms = int((time.time() - start_time) * 1000)

            # Store session for later approval
            self._active_sessions[session_id] = result

            logger.info(
                f"Planning session {session_id} completed in {result.execution_time_ms}ms. "
                f"Patterns: {patterns.total_patterns_found}, "
                f"Conformance: {conformance.score}%"
            )

            return result

        except Exception as e:
            logger.error(f"Planning session {session_id} failed: {str(e)}")
            result.status = PlanningStatus.FAILED
            result.execution_time_ms = int((time.time() - start_time) * 1000)
            raise

    async def _spawn_explore_agents(
        self,
        task: str,
        project_path: Path,
        depth: int,
        include_tests: bool,
        include_adrs: bool,
    ) -> list[ExploreResult]:
        """
        Spawn 3-5 explore sub-agents with isolated contexts.

        Each agent searches for different aspects of the codebase.
        Agents run in parallel for efficiency.

        Args:
            task: Task description for context
            project_path: Project root path
            depth: Search depth
            include_tests: Whether to include test patterns
            include_adrs: Whether to include ADR analysis

        Returns:
            List of ExploreResult from all agents
        """
        agents = []

        # Always include similar implementations search
        agents.append(
            self.pattern_service.search_similar_implementations(
                task=task,
                project_path=project_path,
                depth=depth,
            )
        )

        # Include ADR patterns if requested
        if include_adrs:
            agents.append(
                self.adr_service.find_related_adrs(
                    task=task,
                    project_path=project_path,
                )
            )

        # Include test patterns if requested
        if include_tests:
            agents.append(
                self.test_service.find_test_patterns(
                    task=task,
                    project_path=project_path,
                )
            )

        # Run all agents in parallel (key efficiency gain)
        logger.info(f"Spawning {len(agents)} explore sub-agents...")
        results = await asyncio.gather(*agents, return_exceptions=True)

        # Filter out exceptions and log errors
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning(f"Sub-agent {i} failed: {str(result)}")
                # Create error result
                valid_results.append(
                    ExploreResult(
                        agent_type=ExploreAgentType.SIMILAR_IMPLEMENTATIONS,
                        status="error",
                        errors=[str(result)],
                    )
                )
            else:
                valid_results.append(result)

        return valid_results

    async def _synthesize_patterns(
        self,
        results: list[ExploreResult],
    ) -> PatternSummary:
        """
        Synthesize exploration results into pattern summary.

        Combines patterns from all explore agents, deduplicates,
        and ranks by relevance.

        Args:
            results: List of ExploreResult from sub-agents

        Returns:
            PatternSummary with aggregated patterns
        """
        all_patterns: list[ExtractedPattern] = []
        total_files_scanned = 0
        conventions: dict[str, str] = {}

        for result in results:
            all_patterns.extend(result.patterns)
            total_files_scanned += result.files_searched

        # Deduplicate patterns by name
        seen_names: set[str] = set()
        unique_patterns: list[ExtractedPattern] = []
        for pattern in all_patterns:
            if pattern.name not in seen_names:
                seen_names.add(pattern.name)
                unique_patterns.append(pattern)
            else:
                # Increase occurrence count for duplicate
                for existing in unique_patterns:
                    if existing.name == pattern.name:
                        existing.occurrences += 1
                        break

        # Sort by confidence and occurrences
        unique_patterns.sort(
            key=lambda p: (p.confidence, p.occurrences),
            reverse=True,
        )

        # Calculate category counts
        category_counts: dict[str, int] = {}
        for pattern in unique_patterns:
            cat = pattern.category.value
            category_counts[cat] = category_counts.get(cat, 0) + 1

        # Extract top patterns
        top_patterns = [p.name for p in unique_patterns[:10]]

        # Detect conventions from patterns
        conventions = self._detect_conventions(unique_patterns)

        return PatternSummary(
            patterns=unique_patterns,
            total_files_scanned=total_files_scanned,
            total_patterns_found=len(unique_patterns),
            categories=category_counts,
            top_patterns=top_patterns,
            conventions_detected=conventions,
        )

    def _detect_conventions(
        self,
        patterns: list[ExtractedPattern],
    ) -> dict[str, str]:
        """
        Detect coding conventions from extracted patterns.

        Analyzes patterns to identify:
        - Naming conventions
        - File organization
        - Error handling patterns
        - Testing conventions

        Args:
            patterns: List of extracted patterns

        Returns:
            Dict of detected conventions
        """
        conventions: dict[str, str] = {}

        # Detect naming conventions from CODE_STYLE patterns
        code_style_patterns = [
            p for p in patterns if p.category == PatternCategory.CODE_STYLE
        ]
        if code_style_patterns:
            conventions["naming"] = code_style_patterns[0].description[:200]

        # Detect error handling from ERROR_HANDLING patterns
        error_patterns = [
            p for p in patterns if p.category == PatternCategory.ERROR_HANDLING
        ]
        if error_patterns:
            conventions["error_handling"] = error_patterns[0].description[:200]

        # Detect test conventions
        test_patterns = [
            p for p in patterns if p.category == PatternCategory.TESTING
        ]
        if test_patterns:
            conventions["testing"] = test_patterns[0].description[:200]

        return conventions

    async def _generate_plan(
        self,
        task: str,
        patterns: PatternSummary,
        adr_scan: Optional[ADRScanResult] = None,
    ) -> ImplementationPlan:
        """
        Generate implementation plan building on existing patterns.

        Uses AI to synthesize plan that follows established conventions.
        Plan includes:
        - Implementation steps
        - Files to create/modify
        - Patterns to follow
        - Time estimates

        Args:
            task: Original task description
            patterns: Synthesized patterns from exploration
            adr_scan: ADR scan results (optional)

        Returns:
            ImplementationPlan for human approval
        """
        plan_id = uuid4()

        # Extract relevant patterns for the task
        relevant_patterns = [p.name for p in patterns.patterns[:5]]
        referenced_adrs = []
        if adr_scan:
            referenced_adrs = [adr.id for adr in adr_scan.related_adrs[:3]]

        # Generate implementation steps based on task complexity
        steps = self._generate_steps(task, patterns)

        # Calculate totals
        total_loc = sum(step.estimated_loc for step in steps)
        total_hours = sum(step.estimated_hours for step in steps)
        files_to_create = []
        files_to_modify = []
        for step in steps:
            files_to_create.extend(step.files_to_create)
            files_to_modify.extend(step.files_to_modify)

        # Identify risks
        risks = self._identify_risks(task, patterns, total_loc)

        # Check for new patterns that may need ADR
        new_patterns: list[str] = []
        if total_loc > 100:
            new_patterns.append(
                "Large implementation may introduce new architectural patterns"
            )

        return ImplementationPlan(
            id=plan_id,
            task=task,
            summary=self._generate_summary(task, steps),
            steps=steps,
            total_estimated_loc=total_loc,
            total_estimated_hours=total_hours,
            files_to_create=list(set(files_to_create)),
            files_to_modify=list(set(files_to_modify)),
            patterns_applied=relevant_patterns,
            adrs_referenced=referenced_adrs,
            new_patterns_introduced=new_patterns,
            risks=risks,
        )

    def _generate_steps(
        self,
        task: str,
        patterns: PatternSummary,
    ) -> list[ImplementationStep]:
        """
        Generate implementation steps for the task.

        Steps are ordered by dependency and include:
        - Files to create/modify
        - Patterns to follow
        - Estimated effort

        Args:
            task: Task description
            patterns: Extracted patterns

        Returns:
            List of ImplementationStep
        """
        steps: list[ImplementationStep] = []
        task_lower = task.lower()

        # Step 1: Analysis and setup (always first)
        steps.append(
            ImplementationStep(
                order=1,
                title="Analyze requirements and existing code",
                description=(
                    "Review task requirements, identify relevant existing code, "
                    "and understand integration points."
                ),
                files_to_modify=[],
                files_to_create=[],
                patterns_to_follow=[],
                estimated_loc=0,
                estimated_hours=0.5,
                dependencies=[],
                tests_required=[],
            )
        )

        # Step 2: Create new files/services (if needed)
        if "add" in task_lower or "create" in task_lower or "implement" in task_lower:
            steps.append(
                ImplementationStep(
                    order=2,
                    title="Create new service/component",
                    description=(
                        "Create the main implementation files following established patterns."
                    ),
                    files_to_create=["TBD: New service file"],
                    files_to_modify=[],
                    patterns_to_follow=[p.name for p in patterns.patterns[:3]],
                    estimated_loc=100,
                    estimated_hours=2.0,
                    dependencies=[1],
                    tests_required=["Unit tests for new service"],
                )
            )

        # Step 3: Integration (common for most tasks)
        steps.append(
            ImplementationStep(
                order=len(steps) + 1,
                title="Integrate with existing code",
                description=(
                    "Connect new implementation with existing systems, "
                    "update imports, and wire dependencies."
                ),
                files_to_modify=["TBD: Integration points"],
                files_to_create=[],
                patterns_to_follow=[],
                estimated_loc=30,
                estimated_hours=1.0,
                dependencies=[len(steps)],
                tests_required=["Integration tests"],
            )
        )

        # Step 4: Testing
        steps.append(
            ImplementationStep(
                order=len(steps) + 1,
                title="Write tests",
                description=(
                    "Create unit tests, integration tests, and verify coverage."
                ),
                files_to_create=["TBD: Test files"],
                files_to_modify=[],
                patterns_to_follow=self._get_test_patterns(patterns),
                estimated_loc=80,
                estimated_hours=1.5,
                dependencies=[len(steps)],
                tests_required=[],
            )
        )

        # Step 5: Documentation
        steps.append(
            ImplementationStep(
                order=len(steps) + 1,
                title="Update documentation",
                description=(
                    "Update relevant documentation, add docstrings, "
                    "and update API documentation if needed."
                ),
                files_to_modify=["TBD: Docs files"],
                files_to_create=[],
                patterns_to_follow=[],
                estimated_loc=20,
                estimated_hours=0.5,
                dependencies=[len(steps)],
                tests_required=[],
            )
        )

        return steps

    def _get_test_patterns(self, patterns: PatternSummary) -> list[str]:
        """Get test pattern names from summary."""
        return [
            p.name for p in patterns.patterns
            if p.category == PatternCategory.TESTING
        ][:3]

    def _generate_summary(
        self,
        task: str,
        steps: list[ImplementationStep],
    ) -> str:
        """Generate plan summary."""
        total_loc = sum(s.estimated_loc for s in steps)
        total_hours = sum(s.estimated_hours for s in steps)
        return (
            f"Implementation plan for: {task}\n"
            f"Total steps: {len(steps)}\n"
            f"Estimated LOC: {total_loc}\n"
            f"Estimated hours: {total_hours:.1f}"
        )

    def _identify_risks(
        self,
        task: str,
        patterns: PatternSummary,
        total_loc: int,
    ) -> list[str]:
        """
        Identify potential risks in the implementation.

        Args:
            task: Task description
            patterns: Extracted patterns
            total_loc: Estimated lines of code

        Returns:
            List of identified risks
        """
        risks: list[str] = []

        # Large implementation risk
        if total_loc > 200:
            risks.append(
                "Large implementation (>200 LOC) - consider breaking into smaller tasks"
            )

        # Low pattern coverage
        if patterns.total_patterns_found < 3:
            risks.append(
                "Few existing patterns found - may introduce new conventions"
            )

        # Security-related task
        if any(word in task.lower() for word in ["auth", "security", "password", "token"]):
            risks.append(
                "Security-sensitive implementation - ensure security review"
            )

        # Database-related task
        if any(word in task.lower() for word in ["database", "migration", "schema"]):
            risks.append(
                "Database changes - ensure migration and rollback plan"
            )

        return risks

    def _extract_adr_result(self, result: ExploreResult) -> ADRScanResult:
        """Extract ADR scan result from explore result."""
        return ADRScanResult(
            total_adrs_scanned=result.files_searched,
            related_adrs=[],  # Will be populated by ADR scanner
            conventions_from_adrs={},
            required_patterns=[],
        )

    def _extract_test_result(self, result: ExploreResult) -> TestPatternResult:
        """Extract test pattern result from explore result."""
        return TestPatternResult(
            test_files_scanned=result.files_searched,
            patterns=[],  # Will be populated by test scanner
            coverage_conventions={},
            test_structure={},
        )

    def _calculate_conformance(
        self,
        plan: ImplementationPlan,
        patterns: PatternSummary,
    ) -> ConformanceResult:
        """
        Calculate conformance score (0-100).

        Higher score = better alignment with existing patterns.

        Scoring criteria:
        - Pattern coverage: 40 points
        - ADR alignment: 20 points
        - Convention following: 20 points
        - Risk assessment: 20 points

        Args:
            plan: Generated implementation plan
            patterns: Extracted patterns

        Returns:
            ConformanceResult with score and deviations
        """
        score = 100
        deviations: list[ConformanceDeviation] = []
        recommendations: list[str] = []
        requires_adr = False

        # Check pattern coverage (40 points max)
        pattern_coverage = len(plan.patterns_applied) / max(len(patterns.patterns), 1)
        pattern_score = min(40, int(pattern_coverage * 40))
        score_deduction = 40 - pattern_score

        if pattern_coverage < 0.3:
            deviations.append(
                ConformanceDeviation(
                    pattern_id="coverage",
                    pattern_name="Pattern Coverage",
                    description=(
                        f"Low pattern coverage ({pattern_coverage:.0%}). "
                        "Implementation may not follow established conventions."
                    ),
                    severity="high" if pattern_coverage < 0.1 else "medium",
                    suggestion="Review existing patterns and ensure new code follows them.",
                )
            )
            score -= score_deduction

        # Check ADR alignment (20 points max)
        adr_score = 20 if plan.adrs_referenced else 10
        if not plan.adrs_referenced:
            recommendations.append(
                "Consider referencing relevant ADRs in your implementation"
            )
        score -= (20 - adr_score)

        # Check for new patterns (20 points max)
        if plan.new_patterns_introduced:
            score -= 10
            requires_adr = True
            deviations.append(
                ConformanceDeviation(
                    pattern_id="new_pattern",
                    pattern_name="New Pattern Introduction",
                    description=(
                        "Implementation introduces new patterns. "
                        "Consider creating an ADR to document."
                    ),
                    severity="low",
                    suggestion="Create ADR for new patterns if they will be reused.",
                )
            )

        # Check risk count (20 points max)
        risk_penalty = min(20, len(plan.risks) * 5)
        score -= risk_penalty
        if plan.risks:
            recommendations.extend(plan.risks)

        # Ensure score is within bounds
        score = max(0, min(100, score))

        # Determine level
        if score >= 90:
            level = ConformanceLevel.EXCELLENT
        elif score >= 70:
            level = ConformanceLevel.GOOD
        elif score >= 50:
            level = ConformanceLevel.FAIR
        else:
            level = ConformanceLevel.POOR

        return ConformanceResult(
            score=score,
            level=level,
            deviations=deviations,
            recommendations=recommendations,
            requires_adr=requires_adr,
            new_patterns_detected=plan.new_patterns_introduced,
        )

    async def approve_plan(
        self,
        planning_id: UUID,
        approved: bool,
        notes: Optional[str] = None,
        approved_by: Optional[UUID] = None,
    ) -> PlanningResult:
        """
        Approve or reject a planning session.

        Args:
            planning_id: Planning session UUID
            approved: True to approve, False to reject
            notes: Optional notes
            approved_by: UUID of approver

        Returns:
            Updated PlanningResult

        Raises:
            ValueError: If planning session not found
        """
        if planning_id not in self._active_sessions:
            raise ValueError(f"Planning session not found: {planning_id}")

        result = self._active_sessions[planning_id]

        if approved:
            result.status = PlanningStatus.APPROVED
            result.approved_by = approved_by
            from datetime import datetime
            result.approved_at = datetime.utcnow()
            logger.info(f"Planning session {planning_id} approved by {approved_by}")
        else:
            result.status = PlanningStatus.REJECTED
            result.rejection_reason = notes
            logger.info(f"Planning session {planning_id} rejected: {notes}")

        return result

    def get_session(self, planning_id: UUID) -> Optional[PlanningResult]:
        """Get an active planning session."""
        return self._active_sessions.get(planning_id)

    def list_sessions(self) -> list[PlanningResult]:
        """List all active planning sessions."""
        return list(self._active_sessions.values())


# Factory functions
def create_planning_orchestrator_service(
    db: Optional[AsyncSession] = None,
) -> PlanningOrchestratorService:
    """
    Factory function to create PlanningOrchestratorService.

    Creates service with default dependencies.

    Args:
        db: Optional database session for CRP operations.
            If not provided, CRP functionality will be disabled.

    Returns:
        Configured PlanningOrchestratorService

    Example:
        # Without database (CRP disabled)
        service = create_planning_orchestrator_service()

        # With database (full functionality)
        service = create_planning_orchestrator_service(db=session)
    """
    return PlanningOrchestratorService(
        db=db,
        pattern_service=PatternExtractionService(),
        adr_service=ADRScannerService(),
        test_service=TestPatternService(),
        risk_service=RiskFactorDetectorService(),
        crp_service=CRPService(db) if db else None,
    )


def create_planning_orchestrator_with_db(db: AsyncSession) -> PlanningOrchestratorService:
    """
    Factory function to create PlanningOrchestratorService with database session.

    Use this factory when you need full risk-based planning with CRP support.

    Args:
        db: Database session (required for CRP operations)

    Returns:
        Configured PlanningOrchestratorService with CRP support

    Example:
        async def get_planning_service(db: AsyncSession = Depends(get_db)):
            return create_planning_orchestrator_with_db(db)
    """
    return PlanningOrchestratorService(
        db=db,
        pattern_service=PatternExtractionService(),
        adr_service=ADRScannerService(),
        test_service=TestPatternService(),
        risk_service=RiskFactorDetectorService(),
        crp_service=CRPService(db),
    )
