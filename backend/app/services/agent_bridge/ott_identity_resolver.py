"""
OTT Identity Resolver — map external channel sender_id to internal User UUID.

Sprint 209 — Dogfooding fix: Telegram sender_id (numeric) must resolve to
internal User UUID before any governance command that checks project membership.

Resolution chain (D-068-01):
    1. oauth_accounts: provider='{channel}', provider_account_id='{sender_id}'
    2. OTT_GATEWAY_USER_ID env var (self-hosted fallback — single operator)
    3. None (anonymous — governance commands blocked, prompt to /link)

Architecture:
    Lives in agent_bridge/ (channel abstraction), NOT agent_team/ (multi-agent).
    Redis cache (5-min TTL) avoids repeated DB lookups per message.
"""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

_CACHE_TTL = 3600  # 60 minutes (CTO M1: identity rarely changes)
_CACHE_KEY = "ott:identity:{channel}:{sender_id}"


async def resolve_ott_user_id(
    channel: str,
    sender_id: str,
    redis: Any,
    db: Any | None = None,
) -> str | None:
    """
    Resolve OTT channel sender_id to internal User UUID.

    Args:
        channel: OTT channel ('telegram', 'zalo', etc.)
        sender_id: External sender ID (e.g., Telegram numeric user ID)
        redis: Redis client for caching
        db: Optional AsyncSession for oauth_accounts lookup

    Returns:
        Internal User UUID string, or None if no mapping found.
    """
    if not sender_id:
        return None

    # Fast path: already a UUID (web/CLI user)
    if _is_uuid_like(sender_id):
        return sender_id

    # Check Redis cache first
    cache_key = _CACHE_KEY.format(channel=channel, sender_id=sender_id)
    try:
        cached = await redis.get(cache_key)
        if cached:
            return cached if cached != "__none__" else None
    except Exception:
        pass  # Cache miss — continue to DB

    # Priority 1: oauth_accounts lookup
    if db is not None:
        try:
            from sqlalchemy import select
            from app.models.user import OAuthAccount

            stmt = select(OAuthAccount.user_id).where(
                OAuthAccount.provider == channel,
                OAuthAccount.provider_account_id == sender_id,
            )
            result = await db.execute(stmt)
            row = result.scalar_one_or_none()
            if row:
                user_id = str(row)
                await _cache_set(redis, cache_key, user_id)
                logger.info(
                    "ott_identity: resolved %s:%s → %s (oauth_accounts)",
                    channel, sender_id, user_id,
                )
                return user_id
        except Exception as exc:
            logger.warning(
                "ott_identity: oauth_accounts lookup failed %s:%s error=%s",
                channel, sender_id, str(exc),
            )

    # Priority 2: OTT_GATEWAY_USER_ID env var (self-hosted single operator)
    gateway_user = os.getenv("OTT_GATEWAY_USER_ID", "")
    if gateway_user and _is_uuid_like(gateway_user):
        await _cache_set(redis, cache_key, gateway_user)
        logger.info(
            "ott_identity: resolved %s:%s → %s (OTT_GATEWAY_USER_ID)",
            channel, sender_id, gateway_user,
        )
        return gateway_user

    # Priority 3: No mapping — cache negative result
    await _cache_set(redis, cache_key, "__none__")
    logger.info(
        "ott_identity: no mapping for %s:%s",
        channel, sender_id,
    )
    return None


def _is_uuid_like(value: str) -> bool:
    """Quick check if string looks like a UUID (contains hyphens, 36 chars)."""
    return len(value) == 36 and value.count("-") == 4


async def _cache_set(redis: Any, key: str, value: str) -> None:
    """Set cache with TTL, ignoring errors."""
    try:
        await redis.setex(key, _CACHE_TTL, value)
    except Exception:
        pass
