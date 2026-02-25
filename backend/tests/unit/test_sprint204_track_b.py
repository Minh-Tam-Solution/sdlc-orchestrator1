"""
Sprint 204 Track B — Human Escalation unit tests.

Covers:
  TB-01  MagicLinkPayload discriminated union (gate_approval + classification)
  TB-02  validate_and_consume(): classification type skips user binding
  TB-03  validate_and_consume(): gate_approval type still enforces binding
  TB-04  validate_and_consume(): classification payload fields populated
  TB-05  generate_classification_token(): stores correct payload in Redis
  TB-06  EscalationService.escalate(): BLPOP resolved by reviewer
  TB-07  EscalationService.escalate(): timeout fallback path
  TB-08  EscalationService.escalate(): Redis BLPOP failure → timeout_fallback
  TB-09  EscalationService.escalate(): corrupt BLPOP value → timeout_fallback
  TB-10  EscalationService._notify_reviewer(): sends Telegram message
  TB-11  EscalationService._notify_reviewer(): skips when no bot_token
  TB-12  EscalationService._log_training_event(): logs JSON with all fields
  TB-13  TeamOrchestrator._escalate_for_classification(): returns human result
  TB-14  TeamOrchestrator._escalate_for_classification(): returns timeout_fallback
  TB-15  TeamOrchestrator._escalate_for_classification(): EscalationService exc → fallback
  TB-16  ESCALATION_TIMEOUT_SECONDS setting default is 300
  TB-17  ESCALATION_REVIEWER_CHAT_ID setting default is empty string
"""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch, call
from uuid import uuid4

import pytest

from app.services.agent_team.escalation_service import EscalationService
from app.services.agent_team.magic_link_service import (
    MagicLinkPayload,
    MagicLinkService,
    MagicLinkToken,
    MagicLinkUserMismatchError,
    MagicLinkExpiredError,
)
from app.services.agent_team.query_classifier import ClassificationResult


# ── Helper factories ──────────────────────────────────────────────────────────

def _gate_payload() -> dict:
    return {
        "payload_type": "gate_approval",
        "gate_id": "gate-uuid",
        "action": "approve",
        "user_id": "user-uuid",
        "idempotency_key": "idem-key",
    }


def _classification_payload() -> dict:
    return {
        "payload_type": "classification",
        "gate_id": "",
        "action": "classify:code",
        "user_id": "",
        "idempotency_key": "idem-key-2",
        "classification_query": "Please fix the bug",
        "classification_options": ["code", "reasoning", "governance", "fast"],
        "conversation_id": "conv-uuid",
    }


def _low_confidence(hint: str | None = None) -> ClassificationResult:
    return ClassificationResult(hint=hint, confidence=0.3, method="none", matches=0)


# ── TB-01: MagicLinkPayload discriminated union ───────────────────────────────

class TestMagicLinkPayloadDiscriminatedUnion:
    """TB-01 — MagicLinkPayload supports both payload_type variants."""

    def test_default_payload_type_is_gate_approval(self) -> None:
        """TB-01a — backward compat: default payload_type='gate_approval'."""
        p = MagicLinkPayload(
            gate_id="gid", action="approve", user_id="uid", idempotency_key="ik"
        )
        assert p.payload_type == "gate_approval"
        assert p.classification_query is None
        assert p.classification_options == ()
        assert p.conversation_id is None

    def test_classification_payload_type_stores_fields(self) -> None:
        """TB-01b — classification variant stores all 4 new fields."""
        p = MagicLinkPayload(
            gate_id="",
            action="classify:code",
            user_id="",
            idempotency_key="ik",
            payload_type="classification",
            classification_query="Fix the bug",
            classification_options=("code", "reasoning", "governance", "fast"),
            conversation_id="conv-123",
        )
        assert p.payload_type == "classification"
        assert p.gate_id == ""
        assert p.classification_query == "Fix the bug"
        assert p.classification_options == ("code", "reasoning", "governance", "fast")
        assert p.conversation_id == "conv-123"

    def test_gate_approval_payload_is_frozen(self) -> None:
        """TB-01c — MagicLinkPayload is frozen (immutable)."""
        p = MagicLinkPayload(
            gate_id="gid", action="approve", user_id="uid", idempotency_key="ik"
        )
        with pytest.raises((AttributeError, TypeError)):
            p.gate_id = "other"  # type: ignore[misc]


# ── TB-02/03: validate_and_consume() user binding checks ─────────────────────

class TestValidateAndConsumeBehavior:
    """TB-02/03/04 — validate_and_consume classification vs gate_approval."""

    def _make_service(self, secret: str = "testsecret") -> MagicLinkService:
        return MagicLinkService(
            secret=secret, ttl_seconds=300, frontend_url="http://localhost:3000"
        )

    @pytest.mark.asyncio
    async def test_classification_token_skips_user_binding(self) -> None:
        """TB-02 — classification payload_type bypasses browser_user_id check."""
        service = self._make_service()
        raw = json.dumps(_classification_payload())

        with patch(
            "app.services.agent_team.magic_link_service.get_redis_client"
        ) as mock_redis_factory:
            redis = AsyncMock()
            redis.getdel = AsyncMock(return_value=raw)
            mock_redis_factory.return_value = redis

            # browser_user_id doesn't match token user_id="" → normally would raise
            payload = await service.validate_and_consume(
                signature="a" * 64,
                browser_user_id="any-browser-user",  # mismatch — should NOT raise
            )

        assert payload.payload_type == "classification"
        assert payload.gate_id == ""

    @pytest.mark.asyncio
    async def test_gate_approval_token_enforces_user_binding(self) -> None:
        """TB-03 — gate_approval payload_type raises on user mismatch."""
        service = self._make_service()
        raw = json.dumps(_gate_payload())

        with patch(
            "app.services.agent_team.magic_link_service.get_redis_client"
        ) as mock_redis_factory:
            redis = AsyncMock()
            redis.getdel = AsyncMock(return_value=raw)
            mock_redis_factory.return_value = redis

            with pytest.raises(MagicLinkUserMismatchError):
                await service.validate_and_consume(
                    signature="a" * 64,
                    browser_user_id="wrong-user",
                )

    @pytest.mark.asyncio
    async def test_classification_payload_fields_populated(self) -> None:
        """TB-04 — validate_and_consume returns all classification fields."""
        service = self._make_service()
        raw = json.dumps(_classification_payload())

        with patch(
            "app.services.agent_team.magic_link_service.get_redis_client"
        ) as mock_redis_factory:
            redis = AsyncMock()
            redis.getdel = AsyncMock(return_value=raw)
            mock_redis_factory.return_value = redis

            payload = await service.validate_and_consume(
                signature="a" * 64,
                browser_user_id="",
            )

        assert payload.classification_query == "Please fix the bug"
        assert payload.classification_options == (
            "code", "reasoning", "governance", "fast"
        )
        assert payload.conversation_id == "conv-uuid"
        assert payload.action == "classify:code"


# ── TB-05: generate_classification_token() ───────────────────────────────────

class TestGenerateClassificationToken:
    """TB-05 — generate_classification_token() stores correct Redis payload."""

    @pytest.mark.asyncio
    async def test_stores_classification_payload_type(self) -> None:
        """TB-05a — Redis value includes payload_type='classification'."""
        service = MagicLinkService(
            secret="testsecret", ttl_seconds=300, frontend_url="http://localhost:3000"
        )
        stored_payloads: list[dict] = []

        async def mock_setex(key: str, ttl: int, value: str) -> None:
            stored_payloads.append(json.loads(value))

        with patch(
            "app.services.agent_team.magic_link_service.get_redis_client"
        ) as mock_redis_factory:
            redis = AsyncMock()
            redis.setex = AsyncMock(side_effect=mock_setex)
            mock_redis_factory.return_value = redis

            token = await service.generate_classification_token(
                conversation_id="conv-123",
                query="Help me fix the bug please",
                hint="code",
                reviewer_user_id="",
            )

        assert len(stored_payloads) == 1
        payload = stored_payloads[0]
        assert payload["payload_type"] == "classification"
        assert payload["gate_id"] == ""
        assert payload["action"] == "classify:code"
        assert payload["classification_options"] == [
            "code", "reasoning", "governance", "fast"
        ]
        assert payload["conversation_id"] == "conv-123"

    @pytest.mark.asyncio
    async def test_truncates_query_to_300_chars(self) -> None:
        """TB-05b — generate_classification_token truncates query at 300 chars."""
        service = MagicLinkService(
            secret="testsecret", ttl_seconds=300, frontend_url="http://localhost:3000"
        )
        stored_payloads: list[dict] = []

        async def mock_setex(key: str, ttl: int, value: str) -> None:
            stored_payloads.append(json.loads(value))

        with patch(
            "app.services.agent_team.magic_link_service.get_redis_client"
        ) as mock_redis_factory:
            redis = AsyncMock()
            redis.setex = AsyncMock(side_effect=mock_setex)
            mock_redis_factory.return_value = redis

            long_query = "x" * 500
            await service.generate_classification_token(
                conversation_id="conv-123",
                query=long_query,
                hint="reasoning",
            )

        assert len(stored_payloads[0]["classification_query"]) == 300

    @pytest.mark.asyncio
    async def test_returns_magic_link_token_with_url(self) -> None:
        """TB-05c — generate_classification_token returns MagicLinkToken with URL."""
        service = MagicLinkService(
            secret="testsecret", ttl_seconds=300, frontend_url="http://localhost:3000"
        )

        with patch(
            "app.services.agent_team.magic_link_service.get_redis_client"
        ) as mock_redis_factory:
            redis = AsyncMock()
            redis.setex = AsyncMock(return_value=None)
            mock_redis_factory.return_value = redis

            token = await service.generate_classification_token(
                conversation_id="conv-xyz",
                query="classify me",
                hint="fast",
            )

        assert isinstance(token, MagicLinkToken)
        assert "auth/magic?token=" in token.url
        assert len(token.signature) == 64
        assert token.gate_id == ""
        assert token.action == "classify:fast"


# ── TB-06/07/08/09: EscalationService.escalate() ─────────────────────────────

class TestEscalationServiceEscalate:
    """TB-06–09 — EscalationService.escalate() flow variants."""

    def _make_service(self, timeout: int = 5) -> EscalationService:
        mock_magic_link = AsyncMock()
        mock_magic_link.generate_classification_token = AsyncMock(
            return_value=MagicLinkToken(
                signature="a" * 64,
                gate_id="",
                action="classify:code",
                user_id="",
                idempotency_key="ik",
                ttl_seconds=300,
                url="http://localhost:3000/auth/magic?token=" + "a" * 64,
            )
        )
        return EscalationService(
            magic_link_service=mock_magic_link,
            timeout_seconds=timeout,
        )

    @pytest.mark.asyncio
    async def test_blpop_resolved_returns_human_result(self) -> None:
        """TB-06 — BLPOP returns value → ClassificationResult method='human'."""
        service = self._make_service()
        blpop_value = json.dumps({"hint": "code"}).encode()

        with patch(
            "app.services.agent_team.escalation_service.get_redis_client"
        ) as mock_redis_factory, patch(
            "app.services.agent_team.escalation_service.send_progress_message",
            new=AsyncMock(return_value=True),
        ):
            redis = AsyncMock()
            redis.blpop = AsyncMock(return_value=(b"key", blpop_value))
            mock_redis_factory.return_value = redis

            result = await service.escalate(
                conversation_id="conv-123",
                query="ambiguous query",
                original=_low_confidence("reasoning"),
                bot_token="",
                reviewer_chat_id="",
            )

        assert result.method == "human"
        assert result.hint == "code"
        assert result.confidence == 0.95

    @pytest.mark.asyncio
    async def test_blpop_timeout_returns_timeout_fallback(self) -> None:
        """TB-07 — BLPOP returns None (timeout) → method='timeout_fallback'."""
        service = self._make_service(timeout=1)

        with patch(
            "app.services.agent_team.escalation_service.get_redis_client"
        ) as mock_redis_factory, patch(
            "app.services.agent_team.escalation_service.send_progress_message",
            new=AsyncMock(return_value=False),
        ):
            redis = AsyncMock()
            redis.blpop = AsyncMock(return_value=None)
            mock_redis_factory.return_value = redis

            result = await service.escalate(
                conversation_id="conv-456",
                query="still ambiguous",
                original=_low_confidence("reasoning"),
            )

        assert result.method == "timeout_fallback"
        assert result.hint == "reasoning"  # original hint preserved

    @pytest.mark.asyncio
    async def test_redis_blpop_exception_returns_timeout_fallback(self) -> None:
        """TB-08 — Redis BLPOP exception → method='timeout_fallback'."""
        service = self._make_service()

        with patch(
            "app.services.agent_team.escalation_service.get_redis_client"
        ) as mock_redis_factory:
            redis = AsyncMock()
            redis.blpop = AsyncMock(side_effect=ConnectionError("redis down"))
            mock_redis_factory.return_value = redis

            result = await service.escalate(
                conversation_id="conv-789",
                query="query",
                original=_low_confidence("fast"),
            )

        assert result.method == "timeout_fallback"
        assert result.hint == "fast"

    @pytest.mark.asyncio
    async def test_corrupt_blpop_value_returns_timeout_fallback(self) -> None:
        """TB-09 — BLPOP returns corrupt JSON → method='timeout_fallback'."""
        service = self._make_service()

        with patch(
            "app.services.agent_team.escalation_service.get_redis_client"
        ) as mock_redis_factory:
            redis = AsyncMock()
            redis.blpop = AsyncMock(return_value=(b"key", b"not-valid-json{{{"))
            mock_redis_factory.return_value = redis

            result = await service.escalate(
                conversation_id="conv-bad",
                query="query",
                original=_low_confidence("code"),
            )

        assert result.method == "timeout_fallback"
        assert result.hint == "code"


# ── TB-10/11: EscalationService Telegram notification ───────────────────────

class TestEscalationServiceNotification:
    """TB-10/11 — Telegram reviewer notification behavior."""

    @pytest.mark.asyncio
    async def test_sends_telegram_when_tokens_and_token_present(self) -> None:
        """TB-10 — Notification sent when bot_token + chat_id + links available."""
        mock_magic_link = AsyncMock()
        mock_magic_link.generate_classification_token = AsyncMock(
            return_value=MagicLinkToken(
                signature="b" * 64,
                gate_id="",
                action="classify:code",
                user_id="",
                idempotency_key="ik",
                ttl_seconds=300,
                url="http://example.com/auth/magic?token=" + "b" * 64,
            )
        )
        service = EscalationService(
            magic_link_service=mock_magic_link, timeout_seconds=1
        )

        with patch(
            "app.services.agent_team.escalation_service.get_redis_client"
        ) as mock_redis_factory, patch(
            "app.services.agent_team.escalation_service.send_progress_message",
            new_callable=AsyncMock,
        ) as mock_send:
            redis = AsyncMock()
            redis.blpop = AsyncMock(return_value=None)
            mock_redis_factory.return_value = redis
            mock_send.return_value = True

            await service.escalate(
                conversation_id="conv-notify",
                query="What should I do?",
                original=_low_confidence(),
                bot_token="bot-token-123",
                reviewer_chat_id="chat-123",
            )

        mock_send.assert_awaited_once()
        args = mock_send.call_args
        assert args.kwargs["bot_token"] == "bot-token-123"
        assert args.kwargs["chat_id"] == "chat-123"
        assert "Classification Escalation" in args.kwargs["text"]

    @pytest.mark.asyncio
    async def test_skips_notification_when_no_bot_token(self) -> None:
        """TB-11 — No Telegram call when bot_token is empty."""
        mock_magic_link = AsyncMock()
        mock_magic_link.generate_classification_token = AsyncMock(
            return_value=MagicLinkToken(
                signature="c" * 64,
                gate_id="",
                action="classify:fast",
                user_id="",
                idempotency_key="ik",
                ttl_seconds=300,
                url="http://example.com/auth/magic?token=" + "c" * 64,
            )
        )
        service = EscalationService(
            magic_link_service=mock_magic_link, timeout_seconds=1
        )

        with patch(
            "app.services.agent_team.escalation_service.get_redis_client"
        ) as mock_redis_factory, patch(
            "app.services.agent_team.escalation_service.send_progress_message",
            new_callable=AsyncMock,
        ) as mock_send:
            redis = AsyncMock()
            redis.blpop = AsyncMock(return_value=None)
            mock_redis_factory.return_value = redis

            await service.escalate(
                conversation_id="conv-no-notify",
                query="query",
                original=_low_confidence(),
                bot_token="",        # empty → skip notification
                reviewer_chat_id="",
            )

        mock_send.assert_not_awaited()


# ── TB-12: Training data logging ──────────────────────────────────────────────

class TestEscalationTrainingLog:
    """TB-12 — EscalationService._log_training_event() structured JSON log."""

    def test_log_training_event_emits_json(self, caplog) -> None:
        """TB-12 — _log_training_event logs structured JSON with all fields."""
        import logging
        service = EscalationService(timeout_seconds=300)

        with caplog.at_level(logging.INFO):
            service._log_training_event(
                conversation_id="conv-train",
                query="Train me",
                original=ClassificationResult(
                    hint="reasoning", confidence=0.45, method="llm", matches=0
                ),
                resolved_hint="code",
                reason="human",
            )

        assert len(caplog.records) >= 1
        last_log = caplog.records[-1].message
        assert "escalation_training" in last_log
        data = json.loads(last_log.split("escalation_training: ", 1)[1])
        assert data["event"] == "human_classification"
        assert data["resolved_hint"] == "code"
        assert data["reason"] == "human"
        assert data["original_method"] == "llm"


# ── TB-13/14/15: TeamOrchestrator._escalate_for_classification() ─────────────

class TestTeamOrchestratorEscalation:
    """TB-13–15 — _escalate_for_classification() on TeamOrchestrator."""

    def _make_orchestrator(self) -> Any:
        """Build a minimal TeamOrchestrator with mocked services."""
        from app.services.agent_team.team_orchestrator import TeamOrchestrator

        orch = TeamOrchestrator.__new__(TeamOrchestrator)
        # Minimal attribute stubs needed by the method
        return orch

    def _make_message(self, content: str = "ambiguous?") -> MagicMock:
        msg = MagicMock()
        msg.content = content
        msg.id = uuid4()
        return msg

    def _make_conversation(self) -> MagicMock:
        conv = MagicMock()
        conv.id = uuid4()
        return conv

    @pytest.mark.asyncio
    async def test_returns_human_result_when_resolved(self) -> None:
        """TB-13 — _escalate_for_classification() returns human result."""
        orch = self._make_orchestrator()
        human_result = ClassificationResult(
            hint="code", confidence=0.95, method="human", matches=0
        )

        with patch(
            "app.services.agent_team.team_orchestrator.EscalationService"
        ) as MockEscalation:
            instance = AsyncMock()
            instance.escalate = AsyncMock(return_value=human_result)
            MockEscalation.return_value = instance

            result = await orch._escalate_for_classification(
                message=self._make_message(),
                conversation=self._make_conversation(),
                original=_low_confidence(),
            )

        assert result.method == "human"
        assert result.hint == "code"
        assert result.confidence == 0.95

    @pytest.mark.asyncio
    async def test_returns_timeout_fallback_on_timeout(self) -> None:
        """TB-14 — _escalate_for_classification() returns timeout_fallback."""
        orch = self._make_orchestrator()
        timeout_result = ClassificationResult(
            hint="reasoning", confidence=0.3, method="timeout_fallback", matches=0
        )

        with patch(
            "app.services.agent_team.team_orchestrator.EscalationService"
        ) as MockEscalation:
            instance = AsyncMock()
            instance.escalate = AsyncMock(return_value=timeout_result)
            MockEscalation.return_value = instance

            result = await orch._escalate_for_classification(
                message=self._make_message(),
                conversation=self._make_conversation(),
                original=_low_confidence("reasoning"),
            )

        assert result.method == "timeout_fallback"
        assert result.hint == "reasoning"

    @pytest.mark.asyncio
    async def test_escalation_service_exception_returns_fallback(self) -> None:
        """TB-15 — EscalationService raises → _escalate_for_classification returns fallback."""
        orch = self._make_orchestrator()
        original = _low_confidence("code")

        with patch(
            "app.services.agent_team.team_orchestrator.EscalationService"
        ) as MockEscalation:
            instance = AsyncMock()
            instance.escalate = AsyncMock(side_effect=RuntimeError("escalation broke"))
            MockEscalation.return_value = instance

            result = await orch._escalate_for_classification(
                message=self._make_message(),
                conversation=self._make_conversation(),
                original=original,
            )

        assert result.method == "timeout_fallback"
        assert result.hint == "code"  # original hint preserved
        assert result.confidence == original.confidence


# ── TB-16/17: Settings ────────────────────────────────────────────────────────

class TestEscalationSettings:
    """TB-16/17 — ESCALATION_TIMEOUT_SECONDS + ESCALATION_REVIEWER_CHAT_ID defaults."""

    def test_escalation_timeout_default_is_300(self) -> None:
        """TB-16 — ESCALATION_TIMEOUT_SECONDS defaults to 300 seconds."""
        from app.core.config import settings
        assert settings.ESCALATION_TIMEOUT_SECONDS == 300

    def test_escalation_reviewer_chat_id_default_is_empty(self) -> None:
        """TB-17 — ESCALATION_REVIEWER_CHAT_ID defaults to empty string."""
        from app.core.config import settings
        assert settings.ESCALATION_REVIEWER_CHAT_ID == ""
