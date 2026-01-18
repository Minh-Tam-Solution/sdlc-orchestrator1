"""
=========================================================================
AI Council Schemas - Multi-LLM Deliberation Types
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: December 6, 2025
Status: ACTIVE - Sprint 26 Day 1 (AI Council Service)
Authority: Backend Lead + CTO Approved
Foundation: ADR-007 (AI Context Engine), Sprint 26 Plan
Framework: SDLC 4.9.1 Complete Lifecycle

Purpose:
- Pydantic schemas for AI Council requests/responses
- Type definitions for 3-stage deliberation process
- Validation for council mode configuration

Deliberation Stages:
1. Parallel Queries: Query multiple LLMs simultaneously
2. Peer Review: Anonymized ranking of responses
3. Synthesis: Chairman produces final answer

Zero Mock Policy: 100% real implementation
=========================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Enums
# ============================================================================


class CouncilMode(str, Enum):
    """Council execution mode."""

    SINGLE = "single"  # Use single provider (fast, cheap)
    COUNCIL = "council"  # Use 3-stage deliberation (accurate, expensive)
    AUTO = "auto"  # Auto-select based on severity


class DeliberationStage(str, Enum):
    """Stages in council deliberation."""

    STAGE_1_QUERIES = "stage_1_queries"
    STAGE_2_REVIEW = "stage_2_review"
    STAGE_3_SYNTHESIS = "stage_3_synthesis"
    COMPLETE = "complete"
    FAILED = "failed"


class CouncilProvider(str, Enum):
    """AI providers available for council."""

    OLLAMA = "ollama"
    CLAUDE = "claude"
    GPT4 = "gpt4"


# ============================================================================
# Request Schemas
# ============================================================================


class CouncilRequest(BaseModel):
    """Request to generate council recommendation."""

    violation_id: UUID = Field(
        ...,
        description="UUID of the compliance violation to analyze",
    )
    council_mode: CouncilMode = Field(
        default=CouncilMode.AUTO,
        description="Council execution mode",
    )
    providers: Optional[list[CouncilProvider]] = Field(
        default=None,
        description="Specific providers to use (default: all available)",
    )
    timeout_seconds: int = Field(
        default=30,
        ge=5,
        le=120,
        description="Maximum time for council deliberation",
    )

    @field_validator("providers")
    @classmethod
    def validate_providers(cls, v: Optional[list[CouncilProvider]]) -> Optional[list[CouncilProvider]]:
        """Ensure at least 2 providers for council mode."""
        if v is not None and len(v) < 2:
            raise ValueError("Council mode requires at least 2 providers")
        return v


class CouncilBatchRequest(BaseModel):
    """Request to generate council recommendations for multiple violations."""

    violation_ids: list[UUID] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="List of violation IDs to process",
    )
    council_mode: CouncilMode = Field(
        default=CouncilMode.AUTO,
        description="Council execution mode",
    )
    parallel_limit: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Max violations to process in parallel",
    )


# ============================================================================
# Response Schemas - Stage 1: Parallel Queries
# ============================================================================


class AIProviderResponse(BaseModel):
    """Response from a single AI provider."""

    provider: str = Field(..., description="Provider name (ollama, claude, gpt4)")
    model: str = Field(..., description="Model used for generation")
    response: str = Field(..., description="AI-generated recommendation")
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Provider's confidence score (0-100)",
    )
    duration_ms: float = Field(..., description="Response time in milliseconds")
    tokens_used: int = Field(default=0, description="Total tokens consumed")
    cost_usd: float = Field(default=0.0, description="Cost in USD")
    error: Optional[str] = Field(default=None, description="Error message if failed")

    @property
    def is_success(self) -> bool:
        """Check if response was successful."""
        return self.error is None and len(self.response) > 0


class Stage1Result(BaseModel):
    """Result of Stage 1: Parallel Queries."""

    responses: list[AIProviderResponse] = Field(
        ...,
        description="Responses from all queried providers",
    )
    successful_count: int = Field(..., description="Number of successful responses")
    failed_count: int = Field(..., description="Number of failed responses")
    total_duration_ms: float = Field(..., description="Total stage duration")
    total_cost_usd: float = Field(..., description="Total cost for stage")

    @property
    def has_quorum(self) -> bool:
        """Check if we have enough responses for deliberation (2+)."""
        return self.successful_count >= 2


# ============================================================================
# Response Schemas - Stage 2: Peer Review
# ============================================================================


class ResponseRanking(BaseModel):
    """Ranking of a single response by a reviewer."""

    response_id: str = Field(
        ...,
        description="Anonymized response ID (Response A, B, C)",
    )
    rank: int = Field(
        ...,
        ge=1,
        le=5,
        description="Rank position (1 = best)",
    )
    score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Quality score (0-100)",
    )
    reasoning: str = Field(
        ...,
        description="Brief explanation for ranking",
    )


class PeerReview(BaseModel):
    """Peer review from one AI provider."""

    reviewer: str = Field(..., description="Reviewing provider name")
    rankings: list[ResponseRanking] = Field(
        ...,
        description="Rankings of all other responses",
    )
    duration_ms: float = Field(..., description="Review duration")
    cost_usd: float = Field(default=0.0, description="Cost in USD")


class Stage2Result(BaseModel):
    """Result of Stage 2: Peer Review."""

    reviews: list[PeerReview] = Field(
        ...,
        description="All peer reviews",
    )
    aggregated_scores: dict[str, float] = Field(
        ...,
        description="Aggregated scores per response (provider -> avg_score)",
    )
    best_response_id: str = Field(
        ...,
        description="ID of highest-scored response",
    )
    total_duration_ms: float = Field(..., description="Total stage duration")
    total_cost_usd: float = Field(..., description="Total cost for stage")


# ============================================================================
# Response Schemas - Stage 3: Synthesis
# ============================================================================


class FinalSynthesis(BaseModel):
    """Final synthesized answer from chairman."""

    answer: str = Field(..., description="Final synthesized recommendation")
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Final confidence score (0-100)",
    )
    reasoning: str = Field(
        ...,
        description="Chairman's reasoning for synthesis",
    )
    key_points: list[str] = Field(
        default_factory=list,
        description="Key action points extracted",
    )
    dissenting_views: Optional[str] = Field(
        default=None,
        description="Notable disagreements between providers",
    )


class Stage3Result(BaseModel):
    """Result of Stage 3: Synthesis."""

    chairman: str = Field(..., description="Provider acting as chairman")
    synthesis: FinalSynthesis = Field(..., description="Final synthesis")
    duration_ms: float = Field(..., description="Synthesis duration")
    cost_usd: float = Field(default=0.0, description="Cost in USD")


# ============================================================================
# Full Council Response
# ============================================================================


class CouncilDeliberation(BaseModel):
    """Full deliberation record for transparency."""

    stage_1: Stage1Result = Field(..., description="Parallel query results")
    stage_2: Optional[Stage2Result] = Field(
        default=None,
        description="Peer review results (None if skipped)",
    )
    stage_3: Optional[Stage3Result] = Field(
        default=None,
        description="Synthesis results (None if skipped)",
    )


class CouncilResponse(BaseModel):
    """Full response from AI Council."""

    request_id: UUID = Field(..., description="Unique request identifier")
    violation_id: UUID = Field(..., description="Violation that was analyzed")
    mode_used: CouncilMode = Field(
        ...,
        description="Actual mode used (may differ from requested if auto)",
    )
    recommendation: str = Field(..., description="Final recommendation")
    confidence_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Final confidence score (0-100)",
    )
    providers_used: list[str] = Field(
        ...,
        description="List of providers that contributed",
    )
    deliberation: Optional[CouncilDeliberation] = Field(
        default=None,
        description="Full deliberation details (if council mode)",
    )
    total_duration_ms: float = Field(..., description="Total request duration")
    total_cost_usd: float = Field(..., description="Total cost in USD")
    fallback_used: bool = Field(
        default=False,
        description="Whether fallback was triggered",
    )
    fallback_reason: Optional[str] = Field(
        default=None,
        description="Reason for fallback (if applicable)",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Request timestamp",
    )


class CouncilBatchResponse(BaseModel):
    """Response for batch council request."""

    request_id: UUID = Field(..., description="Batch request identifier")
    results: list[CouncilResponse] = Field(
        ...,
        description="Individual results per violation",
    )
    total_violations: int = Field(..., description="Total violations processed")
    successful_count: int = Field(..., description="Successful recommendations")
    failed_count: int = Field(..., description="Failed recommendations")
    total_duration_ms: float = Field(..., description="Total batch duration")
    total_cost_usd: float = Field(..., description="Total batch cost")


# ============================================================================
# Deliberation History
# ============================================================================


class CouncilDeliberationSummary(BaseModel):
    """Summary of a past council deliberation for listing."""

    request_id: UUID = Field(..., description="Request identifier")
    violation_id: UUID = Field(..., description="Violation analyzed")
    mode_used: CouncilMode = Field(..., description="Mode used")
    confidence_score: int = Field(..., description="Final confidence")
    providers_used: list[str] = Field(..., description="Providers used")
    total_duration_ms: float = Field(..., description="Total duration")
    total_cost_usd: float = Field(..., description="Total cost")
    created_at: datetime = Field(..., description="Timestamp")


class CouncilStats(BaseModel):
    """Statistics for council usage."""

    total_requests: int = Field(..., description="Total council requests")
    single_mode_count: int = Field(..., description="Requests using single mode")
    council_mode_count: int = Field(..., description="Requests using council mode")
    average_confidence: float = Field(..., description="Average confidence score")
    average_duration_ms: float = Field(..., description="Average duration")
    total_cost_usd: float = Field(..., description="Total cost")
    by_provider: dict[str, int] = Field(
        ...,
        description="Request count per provider",
    )
    fallback_rate: float = Field(
        ...,
        description="Percentage of requests requiring fallback",
    )


# ============================================================================
# Configuration Schemas
# ============================================================================


class CouncilConfig(BaseModel):
    """Configuration for council behavior."""

    default_mode: CouncilMode = Field(
        default=CouncilMode.AUTO,
        description="Default execution mode",
    )
    auto_council_severities: list[str] = Field(
        default=["critical", "high"],
        description="Severities that trigger council mode in AUTO",
    )
    stage_1_timeout_ms: int = Field(
        default=10000,
        description="Timeout for Stage 1 (parallel queries)",
    )
    stage_2_timeout_ms: int = Field(
        default=8000,
        description="Timeout for Stage 2 (peer review)",
    )
    stage_3_timeout_ms: int = Field(
        default=10000,
        description="Timeout for Stage 3 (synthesis)",
    )
    council_timeout_ms: int = Field(
        default=30000,
        description="Total timeout for council mode",
    )
    min_providers_for_council: int = Field(
        default=2,
        ge=2,
        le=4,
        description="Minimum providers needed for council",
    )
    fallback_to_single_on_timeout: bool = Field(
        default=True,
        description="Fall back to single mode if council times out",
    )


# ============================================================================
# Sprint 77: AI Council Sprint Context Integration
# ============================================================================


class TeamMemberContext(BaseModel):
    """
    Team member context for AI Council decisions.

    Sprint 77 Day 1: AI Council Sprint Context Integration
    """

    user_id: UUID = Field(..., description="Team member UUID")
    full_name: str = Field(..., description="Team member full name")
    role: str = Field(
        default="developer",
        description="Role: developer, tech_lead, pm, qa"
    )
    availability: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Availability factor (0-1, 1=fully available)"
    )
    expertise: list[str] = Field(
        default_factory=list,
        description="Expertise areas (e.g., frontend, backend, security)"
    )
    workload_items: int = Field(
        default=0,
        ge=0,
        description="Number of assigned backlog items"
    )


class BacklogSummary(BaseModel):
    """
    Summary of sprint backlog for AI Council decisions.

    Sprint 77 Day 1: AI Council Sprint Context Integration
    """

    total_items: int = Field(
        default=0,
        ge=0,
        description="Total number of backlog items in sprint"
    )
    completed_items: int = Field(
        default=0,
        ge=0,
        description="Number of completed items"
    )
    blocked_items: int = Field(
        default=0,
        ge=0,
        description="Number of blocked items"
    )
    in_progress_items: int = Field(
        default=0,
        ge=0,
        description="Number of items in progress"
    )
    p0_count: int = Field(
        default=0,
        ge=0,
        description="Total P0 (critical) items"
    )
    p0_completed: int = Field(
        default=0,
        ge=0,
        description="Completed P0 items"
    )
    p1_count: int = Field(
        default=0,
        ge=0,
        description="Total P1 (high) items"
    )
    p1_completed: int = Field(
        default=0,
        ge=0,
        description="Completed P1 items"
    )
    total_points: int = Field(
        default=0,
        ge=0,
        description="Total story points in sprint"
    )
    completed_points: int = Field(
        default=0,
        ge=0,
        description="Completed story points"
    )


class VelocityContext(BaseModel):
    """
    Velocity context for AI Council decisions.

    Sprint 77 Day 1: Velocity metrics from historical sprints
    """

    average: float = Field(
        default=0.0,
        ge=0.0,
        description="Average velocity in story points"
    )
    trend: str = Field(
        default="unknown",
        description="Trend: increasing, decreasing, stable, unknown"
    )
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence score based on data availability"
    )
    sprint_count: int = Field(
        default=0,
        ge=0,
        description="Number of sprints analyzed for velocity"
    )


class SprintHealthContext(BaseModel):
    """
    Sprint health context for AI Council decisions.

    Sprint 77 Day 1: Health indicators for current sprint
    """

    completion_rate: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Completion percentage (0-100)"
    )
    risk_level: str = Field(
        default="low",
        description="Risk level: low, medium, high, critical"
    )
    days_remaining: int = Field(
        default=0,
        ge=0,
        description="Days until sprint end"
    )
    days_elapsed: int = Field(
        default=0,
        ge=0,
        description="Days since sprint start"
    )
    expected_completion: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Expected completion based on time elapsed"
    )
    on_track: bool = Field(
        default=True,
        description="True if sprint is on track"
    )


class CouncilSprintContext(BaseModel):
    """
    Sprint context for AI Council decisions.

    Sprint 77 Day 1: AI Council Sprint Context Integration

    This context enables Council to:
    - Consider sprint velocity when estimating review time
    - Assign reviewers based on team expertise
    - Prioritize decisions based on sprint health
    - Account for blocked items and risk levels
    """

    sprint_id: UUID = Field(..., description="Sprint UUID")
    sprint_number: int = Field(..., ge=1, description="Sprint number (immutable)")
    sprint_name: str = Field(..., description="Sprint name")
    sprint_goal: str = Field(..., description="Sprint goal/objective")
    sprint_status: str = Field(
        default="active",
        description="Sprint status: planning, active, completed"
    )
    team_members: list[TeamMemberContext] = Field(
        default_factory=list,
        description="Team members with availability/expertise"
    )
    velocity: VelocityContext = Field(
        default_factory=VelocityContext,
        description="Velocity metrics from historical sprints"
    )
    health: SprintHealthContext = Field(
        default_factory=SprintHealthContext,
        description="Current sprint health indicators"
    )
    backlog_summary: BacklogSummary = Field(
        default_factory=BacklogSummary,
        description="Summary of sprint backlog"
    )
    g_sprint_passed: bool = Field(
        default=False,
        description="G-Sprint gate passed (SDLC 5.1.3)"
    )
    documentation_overdue: bool = Field(
        default=False,
        description="Documentation deadline exceeded (Rule #2)"
    )


class CouncilDecisionType(str, Enum):
    """Types of decisions AI Council can make."""

    CODE_REVIEW = "code_review"       # Review code changes
    ARCHITECTURE = "architecture"      # Architecture decisions
    SECURITY = "security"             # Security review
    PRIORITIZATION = "prioritization"  # Backlog prioritization
    ESTIMATION = "estimation"          # Story point estimation
    BLOCKER = "blocker"               # Blocker resolution


class CouncilDecisionRequest(BaseModel):
    """
    Council decision request with sprint context.

    Sprint 77 Day 1: AI Council Sprint Context Integration

    This request enables Council to:
    - Consider sprint context in decisions
    - Adjust urgency based on sprint health
    - Recommend reviewers based on team expertise
    """

    decision_type: CouncilDecisionType = Field(
        ...,
        description="Type of decision requested"
    )
    resource_id: UUID = Field(
        ...,
        description="Resource UUID (backlog item, PR, etc.)"
    )
    resource_type: str = Field(
        ...,
        description="Resource type: backlog_item, pull_request, violation"
    )
    requester_id: UUID = Field(
        ...,
        description="User requesting the decision"
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Description of what needs to be decided"
    )
    sprint_context: Optional[CouncilSprintContext] = Field(
        default=None,
        description="Sprint context for informed decisions"
    )
    urgency: str = Field(
        default="normal",
        description="Urgency: low, normal, high, critical"
    )
    timeout_seconds: int = Field(
        default=30,
        ge=5,
        le=120,
        description="Maximum time for council deliberation"
    )


class CouncilDecision(BaseModel):
    """
    Council decision response with sprint-aware recommendations.

    Sprint 77 Day 1: AI Council Sprint Context Integration
    """

    decision_id: UUID = Field(
        default_factory=lambda: uuid4() if uuid4 else None,
        description="Unique decision identifier"
    )
    request_id: UUID = Field(..., description="Original request UUID")
    decision_type: CouncilDecisionType = Field(..., description="Type of decision")
    recommendation: str = Field(..., description="Council recommendation")
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence score (0-100)"
    )
    reasoning: str = Field(..., description="Council reasoning")
    suggested_assignee: Optional[UUID] = Field(
        default=None,
        description="Suggested team member for action"
    )
    urgency_adjusted: str = Field(
        default="normal",
        description="Adjusted urgency based on sprint context"
    )
    sprint_impact: Optional[str] = Field(
        default=None,
        description="Impact assessment on sprint goal"
    )
    action_items: list[str] = Field(
        default_factory=list,
        description="Concrete action items"
    )
    providers_used: list[str] = Field(
        default_factory=list,
        description="AI providers that contributed"
    )
    total_duration_ms: float = Field(..., description="Decision duration in ms")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Decision timestamp"
    )
    sprint_id: Optional[UUID] = Field(
        default=None,
        description="Sprint ID for traceability"
    )


class CouncilDecisionLog(BaseModel):
    """
    Council decision audit log entry.

    Sprint 77 Day 1: Decision logging with sprint reference
    """

    id: UUID = Field(..., description="Log entry UUID")
    decision_id: UUID = Field(..., description="Decision UUID")
    sprint_id: Optional[UUID] = Field(None, description="Sprint UUID")
    project_id: UUID = Field(..., description="Project UUID")
    decision_type: str = Field(..., description="Decision type")
    recommendation_summary: str = Field(..., description="Summary of recommendation")
    confidence: int = Field(..., description="Confidence score")
    urgency: str = Field(..., description="Decision urgency")
    providers_used: list[str] = Field(default_factory=list)
    total_duration_ms: float = Field(..., description="Decision duration")
    requester_id: UUID = Field(..., description="Requester UUID")
    created_at: datetime = Field(..., description="Log timestamp")
