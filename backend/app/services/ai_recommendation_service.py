"""
=========================================================================
AI Recommendation Service - Multi-Provider AI with Fallback Chain
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: December 2, 2025
Status: ACTIVE - Sprint 21 Day 3 (AI Integration)
Authority: Backend Lead + CTO Approved
Foundation: ADR-007 (AI Context Engine), FR3 (AI Context Engine)
Framework: SDLC 4.9.1 Complete Lifecycle

Purpose:
- Unified AI recommendation interface
- Fallback chain: Ollama → Claude → GPT-4 → Rule-based
- Cost tracking and budget management
- Request logging and audit trail

Fallback Chain (ADR-007):
1. Ollama (Primary): $50/month, <100ms latency, privacy-first
2. Claude (Fallback 1): $1,000/month, 300ms latency, complex reasoning
3. GPT-4 (Fallback 2): $800/month, 250ms latency, code generation
4. Rule-based (Fallback 3): $0/month, 50ms, static recommendations

Cost Management:
- Monthly budget: $500 (Phase 1)
- Budget alerts: 80%, 90%, 100% thresholds
- Provider-level cost tracking

Zero Mock Policy: 100% real AI implementation
=========================================================================
"""

import logging
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.ai_engine import AIProvider, AIRequest, AIUsageLog
from app.models.compliance_scan import ComplianceViolation
from app.services.ollama_service import OllamaService, create_ollama_service, OllamaError

logger = logging.getLogger(__name__)


# ============================================================================
# AI Provider Types
# ============================================================================


class AIProviderType(str, Enum):
    """Supported AI provider types."""

    OLLAMA = "ollama"
    CLAUDE = "claude"
    GPT4 = "gpt4"
    RULE_BASED = "rule_based"


@dataclass
class AIRecommendationResult:
    """Structured result from AI recommendation."""

    recommendation: str
    provider: str
    model: str
    confidence: int
    duration_ms: float
    tokens_used: int
    cost_usd: float
    fallback_used: bool
    fallback_reason: Optional[str] = None


# ============================================================================
# AI Recommendation Service
# ============================================================================


class AIRecommendationService:
    """
    Unified AI recommendation service with multi-provider fallback.

    Fallback Chain:
    1. Ollama (local, fast, cheap)
    2. Claude (cloud, complex reasoning)
    3. GPT-4 (cloud, code generation)
    4. Rule-based (static, guaranteed)

    Usage:
        service = AIRecommendationService(db)

        # Generate single recommendation
        result = await service.generate_recommendation(
            violation_type="missing_documentation",
            severity="high",
            location="docs/00-Project-Foundation",
            description="Missing required folder"
        )

        # Generate batch recommendations
        results = await service.generate_recommendations_for_violations(
            violations=[violation1, violation2]
        )

        # Check budget
        budget = await service.get_monthly_budget_status()
    """

    def __init__(
        self,
        db: AsyncSession,
        ollama_service: Optional[OllamaService] = None,
    ):
        """
        Initialize AI recommendation service.

        Args:
            db: Database session for logging
            ollama_service: Optional pre-configured Ollama service
        """
        self.db = db
        self.ollama = ollama_service or create_ollama_service(
            base_url=settings.OLLAMA_URL,
            model=settings.OLLAMA_MODEL,
        )

        # Pricing per 1K tokens (USD) - from ADR-007
        self.pricing = {
            AIProviderType.OLLAMA: {"input": 0.0, "output": 0.0},  # Self-hosted
            AIProviderType.CLAUDE: {"input": 0.003, "output": 0.015},  # Claude Sonnet
            AIProviderType.GPT4: {"input": 0.01, "output": 0.03},  # GPT-4 Turbo
            AIProviderType.RULE_BASED: {"input": 0.0, "output": 0.0},  # Free
        }

        # Monthly budget (USD)
        self.monthly_budget = 500.0

        logger.info("AI Recommendation Service initialized with fallback chain")

    # ============================================================================
    # Single Recommendation
    # ============================================================================

    async def generate_recommendation(
        self,
        violation_type: str,
        severity: str,
        location: str,
        description: str,
        context: Optional[dict[str, Any]] = None,
        user_id: Optional[UUID] = None,
        gate_id: Optional[UUID] = None,
        force_provider: Optional[AIProviderType] = None,
    ) -> AIRecommendationResult:
        """
        Generate AI recommendation for a compliance violation.

        Uses fallback chain: Ollama → Claude → GPT-4 → Rule-based

        Args:
            violation_type: Type of violation
            severity: Severity level
            location: File/folder path
            description: Violation description
            context: Additional context
            user_id: User requesting recommendation
            gate_id: Associated gate (optional)
            force_provider: Force specific provider (bypasses fallback)

        Returns:
            AIRecommendationResult with recommendation details

        Example:
            result = await service.generate_recommendation(
                violation_type="missing_documentation",
                severity="high",
                location="docs/00-Project-Foundation",
                description="Missing required folder"
            )
            print(f"Recommendation: {result.recommendation}")
            print(f"Provider: {result.provider} ({result.model})")
        """
        start_time = time.time()
        fallback_used = False
        fallback_reason = None

        # If force_provider specified, use it directly
        if force_provider:
            return await self._generate_with_provider(
                provider=force_provider,
                violation_type=violation_type,
                severity=severity,
                location=location,
                description=description,
                context=context,
                user_id=user_id,
                gate_id=gate_id,
            )

        # Fallback chain
        providers = [
            (AIProviderType.OLLAMA, "Primary provider"),
            (AIProviderType.CLAUDE, "Fallback 1"),
            (AIProviderType.GPT4, "Fallback 2"),
            (AIProviderType.RULE_BASED, "Final fallback"),
        ]

        for provider, description_text in providers:
            try:
                # Check if provider is available
                if provider == AIProviderType.OLLAMA:
                    if not self.ollama.is_available:
                        fallback_reason = "Ollama not available"
                        continue

                elif provider == AIProviderType.CLAUDE:
                    if not settings.ANTHROPIC_API_KEY:
                        fallback_reason = "Anthropic API key not configured"
                        continue

                elif provider == AIProviderType.GPT4:
                    if not settings.OPENAI_API_KEY:
                        fallback_reason = "OpenAI API key not configured"
                        continue

                # Generate recommendation
                result = await self._generate_with_provider(
                    provider=provider,
                    violation_type=violation_type,
                    severity=severity,
                    location=location,
                    description=description,
                    context=context,
                    user_id=user_id,
                    gate_id=gate_id,
                )

                # Update fallback status
                if fallback_used:
                    result.fallback_used = True
                    result.fallback_reason = fallback_reason

                # Log request
                await self._log_request(
                    provider=provider,
                    user_id=user_id,
                    gate_id=gate_id,
                    request_type="VIOLATION_RECOMMENDATION",
                    prompt=f"{violation_type}: {description}",
                    response=result.recommendation,
                    tokens_in=0,  # Estimated
                    tokens_out=result.tokens_used,
                    cost=result.cost_usd,
                    duration_ms=result.duration_ms,
                    status="SUCCESS",
                )

                return result

            except Exception as e:
                logger.warning(f"{description_text} ({provider}) failed: {e}")
                fallback_reason = str(e)
                fallback_used = True
                continue

        # Should never reach here (rule-based always works)
        raise RuntimeError("All AI providers failed (including rule-based)")

    async def _generate_with_provider(
        self,
        provider: AIProviderType,
        violation_type: str,
        severity: str,
        location: str,
        description: str,
        context: Optional[dict[str, Any]] = None,
        user_id: Optional[UUID] = None,
        gate_id: Optional[UUID] = None,
    ) -> AIRecommendationResult:
        """Generate recommendation using specific provider."""
        start_time = time.time()

        if provider == AIProviderType.OLLAMA:
            result = self.ollama.generate_recommendation(
                violation_type=violation_type,
                severity=severity,
                location=location,
                description=description,
                context=context,
            )
            return AIRecommendationResult(
                recommendation=result["recommendation"],
                provider=AIProviderType.OLLAMA.value,
                model=result["model"],
                confidence=result["confidence"],
                duration_ms=result["duration_ms"],
                tokens_used=result["tokens"],
                cost_usd=0.0,  # Self-hosted
                fallback_used=False,
            )

        elif provider == AIProviderType.CLAUDE:
            return await self._generate_with_claude(
                violation_type=violation_type,
                severity=severity,
                location=location,
                description=description,
                context=context,
            )

        elif provider == AIProviderType.GPT4:
            return await self._generate_with_gpt4(
                violation_type=violation_type,
                severity=severity,
                location=location,
                description=description,
                context=context,
            )

        else:  # RULE_BASED
            return self._generate_rule_based(
                violation_type=violation_type,
                severity=severity,
                location=location,
                description=description,
            )

    async def _generate_with_claude(
        self,
        violation_type: str,
        severity: str,
        location: str,
        description: str,
        context: Optional[dict[str, Any]] = None,
    ) -> AIRecommendationResult:
        """Generate recommendation using Claude API."""
        import httpx

        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("Anthropic API key not configured")

        start_time = time.time()

        # Build prompt
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(
            violation_type=violation_type,
            severity=severity,
            location=location,
            description=description,
            context=context,
        )

        # Call Claude API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": settings.ANTHROPIC_API_KEY,
                    "content-type": "application/json",
                    "anthropic-version": "2023-06-01",
                },
                json={
                    "model": "claude-sonnet-4-5-20250929",
                    "max_tokens": 1024,
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": user_prompt}],
                },
                timeout=30.0,
            )
            response.raise_for_status()

            data = response.json()

        # Parse response
        recommendation = data["content"][0]["text"]
        input_tokens = data["usage"]["input_tokens"]
        output_tokens = data["usage"]["output_tokens"]

        # Calculate cost
        cost = (input_tokens / 1000) * 0.003 + (output_tokens / 1000) * 0.015

        duration_ms = (time.time() - start_time) * 1000

        return AIRecommendationResult(
            recommendation=recommendation,
            provider=AIProviderType.CLAUDE.value,
            model="claude-sonnet-4-5-20250929",
            confidence=85,
            duration_ms=duration_ms,
            tokens_used=output_tokens,
            cost_usd=cost,
            fallback_used=False,
        )

    async def _generate_with_gpt4(
        self,
        violation_type: str,
        severity: str,
        location: str,
        description: str,
        context: Optional[dict[str, Any]] = None,
    ) -> AIRecommendationResult:
        """Generate recommendation using GPT-4 API."""
        import httpx

        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")

        start_time = time.time()

        # Build prompt
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(
            violation_type=violation_type,
            severity=severity,
            location=location,
            description=description,
            context=context,
        )

        # Call OpenAI API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4-turbo-preview",
                    "max_tokens": 1024,
                    "temperature": 0.3,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                },
                timeout=30.0,
            )
            response.raise_for_status()

            data = response.json()

        # Parse response
        recommendation = data["choices"][0]["message"]["content"]
        input_tokens = data["usage"]["prompt_tokens"]
        output_tokens = data["usage"]["completion_tokens"]

        # Calculate cost
        cost = (input_tokens / 1000) * 0.01 + (output_tokens / 1000) * 0.03

        duration_ms = (time.time() - start_time) * 1000

        return AIRecommendationResult(
            recommendation=recommendation,
            provider=AIProviderType.GPT4.value,
            model="gpt-4-turbo-preview",
            confidence=80,
            duration_ms=duration_ms,
            tokens_used=output_tokens,
            cost_usd=cost,
            fallback_used=False,
        )

    def _generate_rule_based(
        self,
        violation_type: str,
        severity: str,
        location: str,
        description: str,
    ) -> AIRecommendationResult:
        """Generate rule-based fallback recommendation."""
        # Use Ollama's fallback logic
        result = self.ollama._get_fallback_recommendation(
            violation_type=violation_type,
            severity=severity,
            location=location,
            description=description,
        )

        return AIRecommendationResult(
            recommendation=result["recommendation"],
            provider=AIProviderType.RULE_BASED.value,
            model="rule-based-v1",
            confidence=result["confidence"],
            duration_ms=1.0,  # Very fast
            tokens_used=0,
            cost_usd=0.0,
            fallback_used=True,
            fallback_reason="All AI providers failed, using rule-based fallback",
        )

    def _build_system_prompt(self) -> str:
        """Build system prompt for AI providers."""
        return """You are an expert SDLC 5.1.1 compliance advisor. Your role is to provide actionable recommendations for fixing compliance violations.

SDLC 5.1.1 Framework Overview (10 Stages + Archive):
- Stage 00 FOUNDATION (WHY?): Strategic Discovery & Validation
- Stage 01 PLANNING (WHAT?): Requirements & User Stories
- Stage 02 DESIGN (HOW?): Architecture & Technical Design
- Stage 03 INTEGRATE: API Contracts & Third-party Setup
- Stage 04 BUILD: Development & Implementation
- Stage 05 TEST: Quality Assurance & Validation
- Stage 06 DEPLOY: Release & Deployment
- Stage 07 OPERATE: Production Operations & Monitoring
- Stage 08 COLLABORATE: Team Coordination & Knowledge
- Stage 09 GOVERN: Compliance & Strategic Oversight
- Stage 10 ARCHIVE: Project Archive (Legacy Docs)

Guidelines:
1. Be specific and actionable
2. Provide concrete steps (3-5 bullet points)
3. Reference SDLC 5.1.1 best practices
4. Keep recommendations concise
5. Prioritize quick wins"""

    def _build_user_prompt(
        self,
        violation_type: str,
        severity: str,
        location: str,
        description: str,
        context: Optional[dict[str, Any]] = None,
    ) -> str:
        """Build user prompt with violation details."""
        context = context or {}

        prompt = f"""Fix this SDLC 5.1.1 compliance violation:

**Type**: {violation_type.replace("_", " ").title()}
**Severity**: {severity.upper()}
**Location**: {location}
**Description**: {description}
"""

        if context.get("project_name"):
            prompt += f"\n**Project**: {context['project_name']}"
        if context.get("stage"):
            prompt += f"\n**Stage**: {context['stage']}"

        prompt += "\n\nProvide: root cause (1 sentence), fix steps (3-5 points), prevention (1-2 points)."

        return prompt

    # ============================================================================
    # Batch Recommendations
    # ============================================================================

    async def generate_recommendations_for_violations(
        self,
        violations: list[ComplianceViolation],
        context: Optional[dict[str, Any]] = None,
        user_id: Optional[UUID] = None,
    ) -> list[AIRecommendationResult]:
        """
        Generate recommendations for multiple violations.

        Args:
            violations: List of ComplianceViolation objects
            context: Shared context
            user_id: Requesting user

        Returns:
            List of AIRecommendationResult
        """
        results = []

        for violation in violations:
            result = await self.generate_recommendation(
                violation_type=violation.violation_type,
                severity=violation.severity,
                location=violation.location or "unknown",
                description=violation.description,
                context=context,
                user_id=user_id,
            )
            results.append(result)

        return results

    async def update_violation_with_recommendation(
        self,
        violation_id: UUID,
        user_id: Optional[UUID] = None,
    ) -> ComplianceViolation:
        """
        Generate and update violation with AI recommendation.

        Args:
            violation_id: Violation to update
            user_id: Requesting user

        Returns:
            Updated ComplianceViolation

        Example:
            violation = await service.update_violation_with_recommendation(
                violation_id=violation.id,
                user_id=current_user.id
            )
            print(f"AI recommendation: {violation.ai_recommendation}")
        """
        # Get violation
        result = await self.db.execute(
            select(ComplianceViolation).where(ComplianceViolation.id == violation_id)
        )
        violation = result.scalar_one_or_none()

        if not violation:
            raise ValueError(f"Violation not found: {violation_id}")

        # Generate recommendation
        ai_result = await self.generate_recommendation(
            violation_type=violation.violation_type,
            severity=violation.severity,
            location=violation.location or "unknown",
            description=violation.description,
            user_id=user_id,
        )

        # Update violation
        violation.ai_recommendation = ai_result.recommendation
        violation.ai_provider = ai_result.provider
        violation.ai_confidence = ai_result.confidence

        await self.db.commit()
        await self.db.refresh(violation)

        return violation

    # ============================================================================
    # Request Logging
    # ============================================================================

    async def _log_request(
        self,
        provider: AIProviderType,
        user_id: Optional[UUID],
        gate_id: Optional[UUID],
        request_type: str,
        prompt: str,
        response: str,
        tokens_in: int,
        tokens_out: int,
        cost: float,
        duration_ms: float,
        status: str,
        error_message: Optional[str] = None,
    ) -> None:
        """Log AI request to database for audit and cost tracking."""
        try:
            # Get provider from database (optional)
            provider_result = await self.db.execute(
                select(AIProvider).where(AIProvider.provider_type == provider.value)
            )
            db_provider = provider_result.scalar_one_or_none()

            # Create request record
            ai_request = AIRequest(
                provider_id=db_provider.id if db_provider else None,
                user_id=user_id,
                gate_id=gate_id,
                request_type=request_type,
                prompt=prompt[:5000],  # Truncate long prompts
                response=response[:10000],  # Truncate long responses
                input_tokens=tokens_in,
                output_tokens=tokens_out,
                total_cost=cost,
                response_time_ms=int(duration_ms),
                status=status,
                error_message=error_message,
            )
            self.db.add(ai_request)
            await self.db.flush()

            # Create usage log
            month = datetime.utcnow().strftime("%Y-%m")
            usage_log = AIUsageLog(
                request_id=ai_request.id,
                month=month,
                provider_type=provider.value,
                total_cost=cost,
                input_tokens=tokens_in,
                output_tokens=tokens_out,
            )
            self.db.add(usage_log)

            await self.db.commit()

        except Exception as e:
            logger.error(f"Failed to log AI request: {e}")
            # Don't fail the recommendation if logging fails
            await self.db.rollback()

    # ============================================================================
    # Budget Management
    # ============================================================================

    async def get_monthly_budget_status(self) -> dict[str, Any]:
        """
        Get current month's AI budget status.

        Returns:
            Budget status:
            {
                "month": "2025-12",
                "total_spent": 125.50,
                "budget": 500.0,
                "remaining": 374.50,
                "percentage_used": 25.1,
                "by_provider": {
                    "claude": 100.00,
                    "gpt4": 25.50,
                    "ollama": 0.0
                },
                "alerts": ["warning_80"] if over threshold
            }
        """
        month = datetime.utcnow().strftime("%Y-%m")

        # Query total spent this month
        result = await self.db.execute(
            select(
                AIUsageLog.provider_type,
                func.sum(AIUsageLog.total_cost).label("total_cost"),
            )
            .where(AIUsageLog.month == month)
            .group_by(AIUsageLog.provider_type)
        )
        provider_costs = {row.provider_type: float(row.total_cost) for row in result}

        total_spent = sum(provider_costs.values())
        remaining = self.monthly_budget - total_spent
        percentage_used = (total_spent / self.monthly_budget) * 100

        # Check for alerts
        alerts = []
        if percentage_used >= 100:
            alerts.append("budget_exceeded")
        elif percentage_used >= 90:
            alerts.append("warning_90")
        elif percentage_used >= 80:
            alerts.append("warning_80")

        return {
            "month": month,
            "total_spent": round(total_spent, 2),
            "budget": self.monthly_budget,
            "remaining": round(remaining, 2),
            "percentage_used": round(percentage_used, 1),
            "by_provider": {
                provider: round(cost, 2) for provider, cost in provider_costs.items()
            },
            "alerts": alerts,
        }

    async def get_request_history(
        self,
        user_id: Optional[UUID] = None,
        provider_type: Optional[str] = None,
        limit: int = 100,
    ) -> list[AIRequest]:
        """
        Get AI request history.

        Args:
            user_id: Filter by user
            provider_type: Filter by provider
            limit: Max results

        Returns:
            List of AIRequest objects
        """
        query = select(AIRequest).order_by(AIRequest.created_at.desc()).limit(limit)

        if user_id:
            query = query.where(AIRequest.user_id == user_id)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    # ============================================================================
    # Provider Health
    # ============================================================================

    async def get_providers_status(self) -> dict[str, Any]:
        """
        Get status of all AI providers.

        Returns:
            Provider status:
            {
                "ollama": {"healthy": True, "models": [...]},
                "claude": {"available": True},
                "gpt4": {"available": False},
                "rule_based": {"available": True}
            }
        """
        return {
            "ollama": self.ollama.health_check(),
            "claude": {"available": bool(settings.ANTHROPIC_API_KEY)},
            "gpt4": {"available": bool(settings.OPENAI_API_KEY)},
            "rule_based": {"available": True},
        }


# ============================================================================
# Factory Function
# ============================================================================


def create_ai_recommendation_service(
    db: AsyncSession,
    ollama_service: Optional[OllamaService] = None,
) -> AIRecommendationService:
    """
    Factory function to create AIRecommendationService.

    Args:
        db: Database session
        ollama_service: Optional pre-configured Ollama service

    Returns:
        AIRecommendationService instance

    Example:
        service = create_ai_recommendation_service(db)
        result = await service.generate_recommendation(...)
    """
    return AIRecommendationService(db=db, ollama_service=ollama_service)
