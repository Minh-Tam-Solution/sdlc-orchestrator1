"""
Human Escalation Service — Sprint 204 (AD-5, Track B).

When the query classifier's confidence remains < 0.6 after the LLM fallback
(qwen3:8b), the TeamOrchestrator calls ``EscalationService.escalate()`` to
request human classification.

Flow:
  1. Generate 4 single-use Magic Link tokens — one per routing category
     (code / reasoning / governance / fast).
  2. Notify the configured reviewer via Telegram with 4 clickable URLs.
  3. Block on Redis BLPOP ``escalation_result:{conversation_id}``
     for up to ``ESCALATION_TIMEOUT_SECONDS`` (default 300 s).
  4. On reviewer click:
     - The magic-link validation endpoint resolves the token and pushes the
       chosen hint to ``escalation_result:{conversation_id}`` via RPUSH.
     - BLPOP unblocks; return ``ClassificationResult(method="human")``.
  5. On timeout: return ``ClassificationResult(method="timeout_fallback")``
     using the original low-confidence hint as a best guess.
  6. Log the escalation event for human-classification training data (B-05).

Redis key pattern:
  escalation_result:{conversation_id}  →  JSON ``{"hint": "code"}``
  TTL: ESCALATION_TIMEOUT_SECONDS + 60 s buffer (set by RPUSH side)

References:
  - SPRINT-204-CONFIDENCE-ROUTING.md AD-5, Track B
  - FR-047: Magic Link OOB Auth
  - STM-064 C4/C5: OOB Auth Bypass / Race Condition mitigations
"""

from __future__ import annotations

import json
import logging
import os

from app.core.config import settings
from app.services.agent_bridge.telegram_responder import send_progress_message
from app.services.agent_team.magic_link_service import MagicLinkService
from app.services.agent_team.query_classifier import ClassificationResult
from app.utils.redis import get_redis_client

logger = logging.getLogger(__name__)

# Redis key prefix for escalation result payloads (written by magic-link endpoint).
_ESCALATION_KEY_PREFIX = "escalation_result"

# Ordered list of all routing categories presented to the reviewer.
_CLASSIFICATION_HINTS: tuple[str, ...] = ("code", "reasoning", "governance", "fast")

# Category display labels for the Telegram notification.
_HINT_LABELS: dict[str, str] = {
    "code": "💻 Code / Fix / Implement",
    "reasoning": "🧠 Reasoning / Analysis / Explain",
    "governance": "🏛️ Governance / Gate / Sprint",
    "fast": "⚡ Fast / Short / Confirmation",
}


class EscalationService:
    """
    Human classification escalation via Magic Link + Redis BLPOP.

    Usage (called from ``TeamOrchestrator._escalate_for_classification()``):

        service = EscalationService()
        result = await service.escalate(
            conversation_id="uuid",
            query="the ambiguous message text",
            original=ClassificationResult(hint=None, confidence=0.3, method="none"),
            bot_token="telegram-token",
            reviewer_chat_id="123456789",
        )
        # result.method == "human" or "timeout_fallback"
    """

    def __init__(
        self,
        magic_link_service: MagicLinkService | None = None,
        timeout_seconds: int | None = None,
    ) -> None:
        self._magic_link = magic_link_service or MagicLinkService()
        self._timeout = timeout_seconds or settings.ESCALATION_TIMEOUT_SECONDS

    async def escalate(
        self,
        conversation_id: str,
        query: str,
        original: ClassificationResult,
        bot_token: str = "",
        reviewer_chat_id: str = "",
    ) -> ClassificationResult:
        """
        Request human classification for a low-confidence query.

        Args:
            conversation_id: UUID string of the conversation awaiting routing.
            query: The full text of the ambiguous user message.
            original: The best ClassificationResult so far (pre-escalation).
            bot_token: Telegram Bot API token for reviewer notification.
                       Falls back to ``TELEGRAM_BOT_TOKEN`` env var if empty.
            reviewer_chat_id: Telegram chat_id to send the escalation to.
                              Falls back to ``ESCALATION_REVIEWER_CHAT_ID``
                              setting if empty.

        Returns:
            ClassificationResult with method="human" (reviewer responded) or
            method="timeout_fallback" (300 s elapsed, using original hint).
        """
        resolved_bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "")
        resolved_chat_id = reviewer_chat_id or settings.ESCALATION_REVIEWER_CHAT_ID

        # Generate 4 single-use classification tokens — one per routing category.
        links: dict[str, str] = {}
        for hint in _CLASSIFICATION_HINTS:
            try:
                token = await self._magic_link.generate_classification_token(
                    conversation_id=conversation_id,
                    query=query,
                    hint=hint,
                    reviewer_user_id="",  # OTT reviewers may not have browser accounts
                )
                links[hint] = token.url
            except Exception as exc:
                logger.error(
                    "escalation: failed to generate token hint=%s error=%s", hint, exc
                )
                # Continue — other categories may still work.

        logger.info(
            "escalation: generated %d links for conv=%s original_hint=%s confidence=%.2f",
            len(links),
            conversation_id,
            original.hint,
            original.confidence,
        )

        # Notify reviewer via Telegram (non-fatal — escalation still blocks on BLPOP).
        if resolved_bot_token and resolved_chat_id and links:
            await self._notify_reviewer(
                bot_token=resolved_bot_token,
                chat_id=resolved_chat_id,
                conversation_id=conversation_id,
                query=query,
                links=links,
            )

        # Block on Redis BLPOP until reviewer clicks a link or timeout fires.
        redis_key = f"{_ESCALATION_KEY_PREFIX}:{conversation_id}"
        try:
            redis = await get_redis_client()
            result = await redis.blpop(redis_key, timeout=int(self._timeout))
        except Exception as exc:
            logger.error(
                "escalation: Redis BLPOP failed conv=%s error=%s", conversation_id, exc
            )
            return self._timeout_fallback(original)

        if result is None:
            # BLPOP timed out — fall back to LLM best guess.
            logger.warning(
                "escalation: timeout conv=%s after %ds — using original hint=%s",
                conversation_id,
                self._timeout,
                original.hint,
            )
            self._log_training_event(
                conversation_id=conversation_id,
                query=query,
                original=original,
                resolved_hint=None,
                reason="timeout",
            )
            return self._timeout_fallback(original)

        # BLPOP returned: (key_bytes, value_bytes)
        _, raw_value = result
        try:
            data = json.loads(raw_value)
            resolved_hint: str | None = data.get("hint")
        except (json.JSONDecodeError, TypeError) as exc:
            logger.error(
                "escalation: corrupt BLPOP payload conv=%s error=%s", conversation_id, exc
            )
            return self._timeout_fallback(original)

        logger.info(
            "escalation: resolved conv=%s hint=%s (reviewer responded)",
            conversation_id,
            resolved_hint,
        )
        self._log_training_event(
            conversation_id=conversation_id,
            query=query,
            original=original,
            resolved_hint=resolved_hint,
            reason="human",
        )

        return ClassificationResult(
            hint=resolved_hint,
            confidence=0.95,
            method="human",
            matches=0,
        )

    async def _notify_reviewer(
        self,
        bot_token: str,
        chat_id: str,
        conversation_id: str,
        query: str,
        links: dict[str, str],
    ) -> None:
        """Send a Telegram message with 4 classification links to the reviewer."""
        query_preview = query[:200].replace("\n", " ")
        lines = [
            "🤔 *Classification Escalation Required*",
            "",
            f"*Query*: {query_preview}",
            f"*Conversation*: `{conversation_id[:8]}...`",
            "",
            "Please click the correct category link:",
        ]
        for hint in _CLASSIFICATION_HINTS:
            label = _HINT_LABELS.get(hint, hint)
            url = links.get(hint, "")
            if url:
                lines.append(f"{label}: {url}")

        lines.append("")
        lines.append("_(Link expires in 5 minutes, single-use)_")

        await send_progress_message(
            bot_token=bot_token,
            chat_id=chat_id,
            text="\n".join(lines),
        )

    def _timeout_fallback(self, original: ClassificationResult) -> ClassificationResult:
        """Return a timeout_fallback result preserving the original hint."""
        return ClassificationResult(
            hint=original.hint,
            confidence=original.confidence,
            method="timeout_fallback",
            matches=original.matches,
        )

    def _log_training_event(
        self,
        conversation_id: str,
        query: str,
        original: ClassificationResult,
        resolved_hint: str | None,
        reason: str,
    ) -> None:
        """
        Log escalation event for human-classification training data (B-05).

        Structured as a single log line for easy ingestion by offline training
        pipelines. Fields are tab-separated JSON to simplify grep/awk parsing.
        """
        logger.info(
            "escalation_training: %s",
            json.dumps(
                {
                    "event": "human_classification",
                    "conversation_id": conversation_id,
                    "query_preview": query[:200],
                    "original_hint": original.hint,
                    "original_confidence": original.confidence,
                    "original_method": original.method,
                    "resolved_hint": resolved_hint,
                    "reason": reason,
                },
                ensure_ascii=False,
            ),
        )
