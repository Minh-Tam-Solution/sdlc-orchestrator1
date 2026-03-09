"""
=========================================================================
Agent Seed Service — Sprint 225 (SOUL Template Integration)
SDLC Orchestrator - Framework 6.1.2 Alignment

Version: 2.0.0 (Sprint 225 — upgraded from Sprint 194 GAP-01)
Date: March 2026
Status: ACTIVE - Sprint 225
Authority: CTO Approved (Sprint 225 Plan)

Purpose:
- Seed default AgentDefinition records for a project per tier
- Load rich SOUL templates as system_prompt (replacing 1-sentence basic prompts)
- Enforce tier-based role filtering (LITE/STANDARD/PROFESSIONAL/ENTERPRISE)
- Prevent OPTIONAL roles from being auto-seeded (require explicit creation)
- Store SOUL traceability metadata in config JSONB field

Tier Availability Matrix (SDLC 6.1.2):
  LITE:         assistant, coder, tester (3)
  STANDARD:     + pm, architect, reviewer (6)
  PROFESSIONAL: + devops, fullstack, pjm, researcher (10)
  ENTERPRISE:   + ceo, cpo, cto (13)
  OPTIONAL:     writer, sales, cs, itadmin (never auto-seeded)

Backward Compatibility (CTO R4):
  tier=None → seeds all 12 original core roles (pre-Sprint 225 behavior)

Usage:
    svc = AgentSeedService(db)
    created = await svc.seed_project_agents(project_id, tier="PROFESSIONAL")

Zero Mock Policy: Production-ready seeding with SOUL templates
=========================================================================
"""

import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent_definition import AgentDefinition
from app.services.agent_team.config import (
    ROLE_MODEL_DEFAULTS,
    SUPPORT_CONSTRAINTS,
)
from app.services.agent_team.soul_loader import (
    OPTIONAL_ROLES,
    TIER_ROLES,
    SOULLoaderService,
)

logger = logging.getLogger(__name__)

# Fallback system prompt templates (used when SOUL template not available).
_ROLE_PROMPTS: dict[str, str] = {
    "researcher": (
        "You are an SDLC Researcher agent. Gather requirements, analyse market data, "
        "and produce evidence-backed findings. Output structured summaries."
    ),
    "pm": (
        "You are an SDLC Project Manager agent. Decompose user stories into tasks, "
        "track sprint progress, and ensure traceability from requirements to delivery."
    ),
    "pjm": (
        "You are an SDLC Program Manager agent. Coordinate cross-team dependencies, "
        "manage roadmap milestones, and report escalation risks."
    ),
    "architect": (
        "You are an SDLC Architect agent. Design system architecture, review ADRs, "
        "validate non-functional requirements, and enforce design principles."
    ),
    "coder": (
        "You are an SDLC Coder agent. Write production-ready code following Zero Mock "
        "Policy. Include type hints, error handling, and docstrings. Run linting before output."
    ),
    "reviewer": (
        "You are an SDLC Code Reviewer agent. Review code for correctness, security, "
        "performance, and SDLC compliance. Provide actionable feedback with line references."
    ),
    "tester": (
        "You are an SDLC Tester agent. Write unit, integration, and E2E tests. "
        "Target 95%+ coverage. Follow Arrange-Act-Assert pattern."
    ),
    "devops": (
        "You are an SDLC DevOps agent. Manage CI/CD pipelines, Docker configurations, "
        "infrastructure-as-code, and deployment procedures."
    ),
    "fullstack": (
        "You are an SDLC Fullstack Developer agent. Implement both frontend and backend "
        "features. Follow component patterns and API contracts."
    ),
    "ceo": (
        "You are an SDLC CEO Coach. Provide strategic guidance on product-market fit, "
        "business priorities, and investment decisions. Read-only analysis."
    ),
    "cpo": (
        "You are an SDLC CPO Coach. Advise on product strategy, user experience, "
        "feature prioritisation, and customer feedback analysis. Read-only analysis."
    ),
    "cto": (
        "You are an SDLC CTO Coach. Review architecture decisions, technology choices, "
        "security posture, and engineering quality. Read-only analysis."
    ),
    "writer": (
        "You are an SDLC Technical Writer agent. Create documentation, user guides, "
        "API references, and runbooks. Read-only advisory."
    ),
    "sales": (
        "You are an SDLC Sales Advisor agent. Provide market analysis, pricing strategy, "
        "and customer engagement insights. Read-only advisory."
    ),
    "cs": (
        "You are an SDLC Customer Success agent. Advise on user onboarding, support "
        "workflows, and customer satisfaction metrics. Read-only advisory."
    ),
    "itadmin": (
        "You are an SDLC IT Admin agent. Advise on infrastructure, server management, "
        "and deployment operations. Read-only advisory."
    ),
    "assistant": (
        "You are an SDLC Router assistant. Help users find the right agent or workflow "
        "for their task. Provide navigation and quick answers."
    ),
}

# Default max_tokens per role category.
_ROLE_MAX_TOKENS: dict[str, int] = {
    "researcher": 8192,
    "pm": 4096,
    "pjm": 4096,
    "architect": 8192,
    "coder": 16384,
    "reviewer": 8192,
    "tester": 8192,
    "devops": 4096,
    "fullstack": 16384,
    "ceo": 4096,
    "cpo": 4096,
    "cto": 4096,
    "writer": 8192,
    "sales": 4096,
    "cs": 4096,
    "itadmin": 4096,
    "assistant": 2048,
}

# Original 12 core roles (pre-Sprint 225) for backward compatibility when tier=None
_CORE_ROLES: frozenset[str] = frozenset({
    "researcher", "pm", "pjm", "architect", "coder", "reviewer",
    "tester", "devops", "ceo", "cpo", "cto", "assistant",
})

# Roles that get read-only constraints (SE4H + Support)
_READONLY_ROLES: frozenset[str] = frozenset({
    "ceo", "cpo", "cto", "writer", "sales", "cs", "itadmin",
})


class AgentSeedService:
    """Seeds default agent definitions for a project with SOUL templates and tier filtering."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self._soul_loader = SOULLoaderService()

    async def seed_project_agents(
        self,
        project_id: UUID,
        *,
        team_id: UUID | None = None,
        tier: str | None = None,
        skip_existing: bool = True,
    ) -> list[AgentDefinition]:
        """
        Create agent definitions for a project based on tier and SOUL templates.

        Args:
            project_id: Target project UUID.
            team_id: Optional team binding.
            tier: Policy pack tier (LITE/STANDARD/PROFESSIONAL/ENTERPRISE).
                  None = backward-compatible: seeds all 12 original core roles.
            skip_existing: If True, skip roles that already have a definition.

        Returns:
            List of newly created AgentDefinition records.
        """
        # Determine which roles to seed
        if tier is not None:
            allowed_roles = TIER_ROLES.get(tier.upper(), frozenset())
            if not allowed_roles:
                logger.warning(
                    "Unknown tier '%s' — falling back to core roles", tier,
                )
                allowed_roles = _CORE_ROLES
        else:
            # Backward compatibility: seed all 12 original core roles
            allowed_roles = _CORE_ROLES

        # Never auto-seed optional roles
        allowed_roles = allowed_roles - OPTIONAL_ROLES

        existing_roles: set[str] = set()
        if skip_existing:
            result = await self.db.execute(
                select(AgentDefinition.sdlc_role).where(
                    AgentDefinition.project_id == project_id,
                    AgentDefinition.is_active.is_(True),
                )
            )
            existing_roles = {row[0] for row in result.all()}

        created: list[AgentDefinition] = []

        for role, model_cfg in ROLE_MODEL_DEFAULTS.items():
            if role not in allowed_roles:
                continue
            if role in existing_roles:
                logger.debug("Skipping role %s — already exists for project %s", role, project_id)
                continue

            # Try SOUL template first, fall back to basic prompt
            soul_prompt = self._soul_loader.get_system_prompt(role, max_chars=6000)
            soul_version = self._soul_loader.get_soul_version(role)
            system_prompt = soul_prompt or _ROLE_PROMPTS.get(role, "")

            # Build config JSONB with SOUL traceability
            config: dict = {}
            if soul_prompt:
                config["soul_version"] = soul_version or "1.0.0"
                config["soul_source"] = "framework"
            else:
                config["soul_source"] = "fallback"

            # Determine tool permissions based on role type
            is_readonly = role in _READONLY_ROLES

            definition = AgentDefinition(
                project_id=project_id,
                team_id=team_id,
                agent_name=role,
                sdlc_role=role,
                provider=model_cfg["provider"],
                model=model_cfg["model"],
                system_prompt=system_prompt,
                max_tokens=_ROLE_MAX_TOKENS.get(role, 4096),
                temperature=0.3 if role in ("coder", "reviewer", "tester", "fullstack") else 0.7,
                queue_mode="queue",
                session_scope="per-sender",
                max_delegation_depth=0 if is_readonly else 1,
                can_spawn_subagent=not is_readonly and role != "assistant",
                allowed_tools=(
                    SUPPORT_CONSTRAINTS["allowed_tools"]
                    if is_readonly
                    else ["*"]
                ),
                denied_tools=(
                    SUPPORT_CONSTRAINTS["denied_tools"]
                    if is_readonly
                    else []
                ),
                allowed_paths=[],
                is_active=True,
                config=config,
            )
            self.db.add(definition)
            created.append(definition)

        if created:
            await self.db.flush()
            logger.info(
                "Seeded %d agent definitions for project %s (tier=%s, roles: %s)",
                len(created),
                project_id,
                tier or "default",
                ", ".join(d.sdlc_role for d in created),
            )

        return created
