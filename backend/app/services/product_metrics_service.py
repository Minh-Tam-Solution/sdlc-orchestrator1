"""
Product Metrics Service — Sprint 226, ADR-071 D-071-05.

Replaces delivery-focused metrics with product-focused metrics:
  - Conversation completion rate (≥70% target)
  - Human override rate (≤30% at STANDARD tier)
  - Time-to-gate improvement (≥40% faster vs baseline)
  - Pilot retention (3/3 active end of Week 2)

Kill signal: completion <50% OR retention <2/3 after Week 2 → stop.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import func, select, and_, case
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class ProductMetricsService:
    """Compute product-level success metrics for Option 5 pilot validation."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def time_to_gate_baseline(self, project_id: UUID | None = None) -> dict[str, Any]:
        """
        Baseline: average time from gate evaluated_at → approved_at/rejected_at.

        Returns per-gate-type averages in seconds.
        Must be collected BEFORE pilot begins for comparison.
        """
        from app.models.gate import Gate

        filters = [
            Gate.status.in_(["APPROVED", "REJECTED"]),
            Gate.evaluated_at.isnot(None),
        ]
        if project_id:
            filters.append(Gate.project_id == project_id)

        result = await self.db.execute(
            select(
                Gate.gate_type,
                func.count(Gate.id).label("count"),
                func.avg(
                    func.extract("epoch", Gate.updated_at) - func.extract("epoch", Gate.evaluated_at)
                ).label("avg_seconds"),
                func.min(
                    func.extract("epoch", Gate.updated_at) - func.extract("epoch", Gate.evaluated_at)
                ).label("min_seconds"),
                func.max(
                    func.extract("epoch", Gate.updated_at) - func.extract("epoch", Gate.evaluated_at)
                ).label("max_seconds"),
            )
            .where(and_(*filters))
            .group_by(Gate.gate_type)
        )

        rows = result.all()
        return {
            "baseline_date": datetime.now(timezone.utc).isoformat(),
            "project_id": str(project_id) if project_id else "all",
            "gate_types": [
                {
                    "gate_type": row.gate_type,
                    "count": row.count,
                    "avg_seconds": round(float(row.avg_seconds or 0), 1),
                    "min_seconds": round(float(row.min_seconds or 0), 1),
                    "max_seconds": round(float(row.max_seconds or 0), 1),
                }
                for row in rows
            ],
        }

    async def conversation_completion_rate(
        self,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> dict[str, Any]:
        """
        % of conversations started via chat that completed without unplanned web fallback.

        Target: ≥70%. Kill signal: <50%.
        """
        from app.models.agent_conversation import AgentConversation

        filters = []
        if date_from:
            filters.append(AgentConversation.started_at >= date_from)
        if date_to:
            filters.append(AgentConversation.started_at <= date_to)

        result = await self.db.execute(
            select(
                func.count(AgentConversation.id).label("total"),
                func.count(
                    case(
                        (AgentConversation.status == "completed", AgentConversation.id),
                    )
                ).label("completed"),
                func.count(
                    case(
                        (AgentConversation.status == "error", AgentConversation.id),
                    )
                ).label("errored"),
                func.count(
                    case(
                        (AgentConversation.status == "max_reached", AgentConversation.id),
                    )
                ).label("max_reached"),
            ).where(and_(*filters) if filters else True)
        )

        row = result.one()
        total = row.total or 0
        completed = row.completed or 0
        rate = round((completed / total * 100), 1) if total > 0 else 0.0

        return {
            "period": {
                "from": date_from.isoformat() if date_from else None,
                "to": date_to.isoformat() if date_to else None,
            },
            "total_conversations": total,
            "completed": completed,
            "errored": row.errored or 0,
            "max_reached": row.max_reached or 0,
            "completion_rate_pct": rate,
            "meets_target": rate >= 70.0,
            "kill_signal": rate < 50.0 and total >= 10,
        }

    async def human_override_rate(
        self,
        tier: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> dict[str, Any]:
        """
        % of agent gate actions overridden by human.

        Target: ≤30% at STANDARD tier.
        """
        from app.models.gate_approval import GateApproval

        filters = []
        if date_from:
            filters.append(GateApproval.created_at >= date_from)
        if date_to:
            filters.append(GateApproval.created_at <= date_to)

        result = await self.db.execute(
            select(
                func.count(GateApproval.id).label("total_actions"),
                func.count(
                    case(
                        (GateApproval.source == "agent", GateApproval.id),
                    )
                ).label("agent_actions"),
                func.count(
                    case(
                        (GateApproval.source == "web", GateApproval.id),
                    )
                ).label("human_web_actions"),
                func.count(
                    case(
                        (GateApproval.source == "magic_link", GateApproval.id),
                    )
                ).label("human_magic_link_actions"),
            ).where(and_(*filters) if filters else True)
        )

        row = result.one()
        total = row.total_actions or 0
        agent = row.agent_actions or 0
        human = (row.human_web_actions or 0) + (row.human_magic_link_actions or 0)
        override_rate = round((human / total * 100), 1) if total > 0 else 0.0

        return {
            "tier_filter": tier,
            "total_actions": total,
            "agent_actions": agent,
            "human_overrides": human,
            "override_rate_pct": override_rate,
            "meets_target": override_rate <= 30.0,
        }

    async def pilot_retention(
        self,
        since: datetime | None = None,
    ) -> dict[str, Any]:
        """
        Count distinct users who returned to conversation workflow after first interaction.

        Target: 3/3 active end of Week 2.
        """
        from app.models.agent_conversation import AgentConversation

        filters = []
        if since:
            filters.append(AgentConversation.started_at >= since)

        result = await self.db.execute(
            select(
                func.count(func.distinct(AgentConversation.initiator_id)).label("unique_users"),
            )
            .where(
                and_(
                    AgentConversation.initiator_type == "user",
                    AgentConversation.status.in_(["completed", "active"]),
                    *filters,
                )
            )
        )

        row = result.one()
        active_users = row.unique_users or 0

        return {
            "since": since.isoformat() if since else None,
            "active_users": active_users,
            "target": 3,
            "meets_target": active_users >= 3,
            "kill_signal": active_users < 2,
        }
