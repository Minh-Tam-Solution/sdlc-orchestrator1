"""
Sprint 205 — LangChain Provider Plugin Unit Tests (LC-01 to LC-10).

Tests cover ADR-066 (LangChain Multi-Agent Orchestration) Track A:
  LC-01: AgentInvoker._call_provider() dispatches provider='langchain' to _call_langchain()
  LC-02: Feature flag disabled (LANGCHAIN_ENABLED=false) → AgentInvokerError
  LC-03: Optional dependency guard — module imports without langchain packages
  LC-04: ChatOllama wrapper — non-claude/gpt model routes to Ollama
  LC-05: ChatAnthropic wrapper — model "claude-*" routes to Anthropic
  LC-06: Structured output — with_structured_output(schema) invoked when schema provided
  LC-07: Tool binding — bind_tools() called when tools list is non-empty
  LC-08: Token counting callback — input_tokens + output_tokens populated after invoke
  LC-09: LangChain exception mapping — AuthenticationError classifies as AUTH (ABORT)
  LC-10: Unauthorized tool call via invoke chain → ToolPermissionDenied propagates

LANGCHAIN_ENABLED=false by default in all tests (no real LangChain calls).
LangChain model classes are mocked throughout.
"""

from __future__ import annotations

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ──────────────────────────────────────────────────────────────────────────────
# LC-01: _call_provider() dispatches to _call_langchain()
# ──────────────────────────────────────────────────────────────────────────────


class TestLangChainDispatch:
    """LC-01: AgentInvoker routes provider='langchain' to _call_langchain()."""

    @pytest.mark.asyncio
    async def test_langchain_branch_dispatched(self) -> None:
        """LC-01: _call_provider with provider='langchain' calls _call_langchain()."""
        from app.services.agent_team.agent_invoker import AgentInvoker, ProviderConfig

        invoker = AgentInvoker(
            provider_chain=[ProviderConfig(provider="langchain", model="qwen3:8b")]
        )

        with patch.object(
            invoker, "_call_langchain", new_callable=AsyncMock
        ) as mock_lc:
            mock_lc.return_value = ("response content", 15, 30)

            content, in_tok, out_tok = await invoker._call_provider(
                config=ProviderConfig(provider="langchain", model="qwen3:8b"),
                messages=[{"role": "user", "content": "hello"}],
                system_prompt=None,
                max_tokens=100,
                temperature=0.7,
            )

        mock_lc.assert_called_once()
        assert content == "response content"
        assert in_tok == 15
        assert out_tok == 30

    @pytest.mark.asyncio
    async def test_unknown_provider_raises(self) -> None:
        """LC-01 negative: unknown provider string raises AgentInvokerError."""
        from app.services.agent_team.agent_invoker import AgentInvoker, AgentInvokerError, ProviderConfig

        invoker = AgentInvoker(
            provider_chain=[ProviderConfig(provider="unknown_xyz", model="model")]
        )
        with pytest.raises(AgentInvokerError, match="Unknown provider"):
            await invoker._call_provider(
                config=ProviderConfig(provider="unknown_xyz", model="model"),
                messages=[{"role": "user", "content": "hi"}],
                system_prompt=None,
                max_tokens=100,
                temperature=0.7,
            )


# ──────────────────────────────────────────────────────────────────────────────
# LC-02: Feature flag disabled → AgentInvokerError
# ──────────────────────────────────────────────────────────────────────────────


class TestFeatureFlagDisabled:
    """LC-02: LANGCHAIN_ENABLED=false raises AgentInvokerError."""

    @pytest.mark.asyncio
    async def test_disabled_flag_raises_agent_invoker_error(self) -> None:
        """LC-02: _assert_available raises AgentInvokerError when flag is false."""
        from app.services.agent_team.agent_invoker import AgentInvokerError, ProviderConfig
        from app.services.agent_team.langchain_provider import LangChainProvider

        provider = LangChainProvider(
            config=ProviderConfig(provider="langchain", model="qwen3:8b")
        )

        # Ensure packages appear installed but flag is off
        with patch("app.services.agent_team.langchain_provider._LANGCHAIN_AVAILABLE", True):
            with patch.dict(os.environ, {"LANGCHAIN_ENABLED": "false"}):
                with pytest.raises(AgentInvokerError, match="LANGCHAIN_ENABLED=true"):
                    await provider.invoke(
                        messages=[{"role": "user", "content": "hello"}]
                    )

    @pytest.mark.asyncio
    async def test_empty_langchain_enabled_is_disabled(self) -> None:
        """LC-02: Unset LANGCHAIN_ENABLED env var also disables the provider."""
        from app.services.agent_team.agent_invoker import AgentInvokerError, ProviderConfig
        from app.services.agent_team.langchain_provider import LangChainProvider

        provider = LangChainProvider(
            config=ProviderConfig(provider="langchain", model="qwen3:8b")
        )

        env_without_flag = {k: v for k, v in os.environ.items() if k != "LANGCHAIN_ENABLED"}
        with patch("app.services.agent_team.langchain_provider._LANGCHAIN_AVAILABLE", True):
            with patch.dict(os.environ, env_without_flag, clear=True):
                with pytest.raises(AgentInvokerError, match="LANGCHAIN_ENABLED=true"):
                    await provider.invoke(
                        messages=[{"role": "user", "content": "hello"}]
                    )


# ──────────────────────────────────────────────────────────────────────────────
# LC-03: Optional dependency guard — clean import without packages
# ──────────────────────────────────────────────────────────────────────────────


class TestOptionalDependencyGuard:
    """LC-03: Module imports cleanly; raises AgentInvokerError when unavailable."""

    def test_module_imports_without_langchain_packages(self) -> None:
        """LC-03: langchain_provider module is importable without langchain installed."""
        # If we got here, the import succeeded — test the _LANGCHAIN_AVAILABLE sentinel
        from app.services.agent_team import langchain_provider  # noqa: F401

        # _LANGCHAIN_AVAILABLE is a bool regardless of whether packages are present
        assert isinstance(langchain_provider._LANGCHAIN_AVAILABLE, bool)

    @pytest.mark.asyncio
    async def test_unavailable_packages_raises_agent_invoker_error(self) -> None:
        """LC-03: _LANGCHAIN_AVAILABLE=False raises AgentInvokerError on invoke."""
        from app.services.agent_team.agent_invoker import AgentInvokerError, ProviderConfig
        from app.services.agent_team.langchain_provider import LangChainProvider

        provider = LangChainProvider(
            config=ProviderConfig(provider="langchain", model="qwen3:8b")
        )

        with patch(
            "app.services.agent_team.langchain_provider._LANGCHAIN_AVAILABLE", False
        ):
            with pytest.raises(AgentInvokerError, match="not installed"):
                await provider.invoke(
                    messages=[{"role": "user", "content": "hello"}]
                )


# ──────────────────────────────────────────────────────────────────────────────
# LC-04: ChatOllama wrapper
# LC-05: ChatAnthropic wrapper
# LC-06: Structured output
# LC-07: Tool binding
# LC-08: Token counting callback
# ──────────────────────────────────────────────────────────────────────────────


def _make_mock_ai_message(content: str) -> MagicMock:
    """Build a mock AIMessage-like object returned by langchain model.ainvoke()."""
    msg = MagicMock()
    msg.content = content
    return msg


def _make_mock_model(return_content: str = "test response") -> MagicMock:
    """Build a mock LangChain chat model that returns a predetermined response."""
    model = MagicMock()
    model.bind_tools = MagicMock(return_value=model)
    model.with_structured_output = MagicMock(return_value=model)
    model.ainvoke = AsyncMock(return_value=_make_mock_ai_message(return_content))
    return model


class TestChatOllamaWrapper:
    """LC-04: model without 'claude-' or 'gpt-' in name routes to ChatOllama."""

    @pytest.mark.asyncio
    async def test_ollama_model_uses_chat_ollama(self) -> None:
        """LC-04: ChatOllama is instantiated for non-anthropic, non-openai models."""
        from app.services.agent_team.agent_invoker import ProviderConfig
        from app.services.agent_team.langchain_provider import LangChainProvider

        config = ProviderConfig(provider="langchain", model="qwen3-coder:30b")
        provider = LangChainProvider(config)

        mock_model = _make_mock_model("ollama response")

        with patch("app.services.agent_team.langchain_provider._LANGCHAIN_AVAILABLE", True):
            with patch.dict(os.environ, {"LANGCHAIN_ENABLED": "true"}):
                with patch(
                    "app.services.agent_team.langchain_provider.ChatOllama",
                    return_value=mock_model,
                ) as mock_ollama_cls:
                    content, _, _ = await provider.invoke(
                        messages=[{"role": "user", "content": "write a function"}]
                    )

        mock_ollama_cls.assert_called_once()
        assert content == "ollama response"

    @pytest.mark.asyncio
    async def test_ollama_base_url_from_env(self) -> None:
        """LC-04: OLLAMA_BASE_URL env var is passed to ChatOllama."""
        from app.services.agent_team.agent_invoker import ProviderConfig
        from app.services.agent_team.langchain_provider import LangChainProvider

        config = ProviderConfig(provider="langchain", model="qwen3:8b")
        provider = LangChainProvider(config)

        mock_model = _make_mock_model()

        with patch("app.services.agent_team.langchain_provider._LANGCHAIN_AVAILABLE", True):
            with patch.dict(
                os.environ,
                {"LANGCHAIN_ENABLED": "true", "OLLAMA_BASE_URL": "http://custom:11434"},
            ):
                with patch(
                    "app.services.agent_team.langchain_provider.ChatOllama",
                    return_value=mock_model,
                ) as mock_ollama_cls:
                    await provider.invoke(
                        messages=[{"role": "user", "content": "hi"}]
                    )

        call_kwargs = mock_ollama_cls.call_args.kwargs
        assert call_kwargs.get("base_url") == "http://custom:11434"


class TestChatAnthropicWrapper:
    """LC-05: model with 'claude-' in name routes to ChatAnthropic."""

    @pytest.mark.asyncio
    async def test_anthropic_model_uses_chat_anthropic(self) -> None:
        """LC-05: ChatAnthropic is instantiated for models containing 'claude-'."""
        from app.services.agent_team.agent_invoker import ProviderConfig
        from app.services.agent_team.langchain_provider import LangChainProvider

        config = ProviderConfig(provider="langchain", model="claude-sonnet-4-5")
        provider = LangChainProvider(config)

        mock_model = _make_mock_model("anthropic response")

        with patch("app.services.agent_team.langchain_provider._LANGCHAIN_AVAILABLE", True):
            with patch.dict(
                os.environ,
                {
                    "LANGCHAIN_ENABLED": "true",
                    "ANTHROPIC_API_KEY": "sk-test-key",
                },
            ):
                with patch(
                    "app.services.agent_team.langchain_provider.ChatAnthropic",
                    return_value=mock_model,
                ) as mock_anthropic_cls:
                    content, _, _ = await provider.invoke(
                        messages=[{"role": "user", "content": "explain recursion"}]
                    )

        mock_anthropic_cls.assert_called_once()
        assert content == "anthropic response"

    @pytest.mark.asyncio
    async def test_missing_anthropic_key_raises(self) -> None:
        """LC-05: Missing ANTHROPIC_API_KEY raises RuntimeError."""
        from app.services.agent_team.agent_invoker import ProviderConfig
        from app.services.agent_team.langchain_provider import LangChainProvider

        config = ProviderConfig(provider="langchain", model="claude-opus-4-6")
        provider = LangChainProvider(config)

        env_without_key = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}

        with patch("app.services.agent_team.langchain_provider._LANGCHAIN_AVAILABLE", True):
            with patch.dict(
                os.environ,
                {**env_without_key, "LANGCHAIN_ENABLED": "true"},
                clear=True,
            ):
                with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY not set"):
                    await provider.invoke(
                        messages=[{"role": "user", "content": "hello"}]
                    )


class TestStructuredOutput:
    """LC-06: with_structured_output(schema) invoked when output_schema provided."""

    @pytest.mark.asyncio
    async def test_structured_output_calls_with_structured_output(self) -> None:
        """LC-06: output_schema causes model.with_structured_output() to be called."""
        from pydantic import BaseModel
        from app.services.agent_team.agent_invoker import ProviderConfig
        from app.services.agent_team.langchain_provider import LangChainProvider

        class MySchema(BaseModel):
            answer: str

        config = ProviderConfig(provider="langchain", model="qwen3:8b")
        provider = LangChainProvider(config)

        # Mock structured response (Pydantic model instance)
        mock_response = MySchema(answer="42")
        mock_model = MagicMock()
        mock_model.bind_tools = MagicMock(return_value=mock_model)
        structured_model = MagicMock()
        structured_model.ainvoke = AsyncMock(return_value=mock_response)
        mock_model.with_structured_output = MagicMock(return_value=structured_model)

        with patch("app.services.agent_team.langchain_provider._LANGCHAIN_AVAILABLE", True):
            with patch.dict(os.environ, {"LANGCHAIN_ENABLED": "true"}):
                with patch(
                    "app.services.agent_team.langchain_provider.ChatOllama",
                    return_value=mock_model,
                ):
                    content, _, _ = await provider.invoke(
                        messages=[{"role": "user", "content": "what is the answer?"}],
                        output_schema=MySchema,
                    )

        mock_model.with_structured_output.assert_called_once_with(MySchema)
        # Content should be the JSON serialization of the Pydantic instance
        assert "42" in content


class TestToolBinding:
    """LC-07: bind_tools() called when tools list is non-empty."""

    @pytest.mark.asyncio
    async def test_tools_bound_on_model(self) -> None:
        """LC-07: model.bind_tools() is called with the provided tool list."""
        from app.services.agent_team.agent_invoker import ProviderConfig
        from app.services.agent_team.langchain_provider import LangChainProvider

        fake_tool = MagicMock()
        fake_tool.name = "gate_status"

        config = ProviderConfig(provider="langchain", model="qwen3:8b")
        provider = LangChainProvider(config, tools=[fake_tool])

        mock_model = _make_mock_model("tool response")

        with patch("app.services.agent_team.langchain_provider._LANGCHAIN_AVAILABLE", True):
            with patch.dict(os.environ, {"LANGCHAIN_ENABLED": "true"}):
                with patch(
                    "app.services.agent_team.langchain_provider.ChatOllama",
                    return_value=mock_model,
                ):
                    await provider.invoke(
                        messages=[{"role": "user", "content": "use gate_status tool"}]
                    )

        mock_model.bind_tools.assert_called_once_with([fake_tool])

    @pytest.mark.asyncio
    async def test_no_tools_skips_bind(self) -> None:
        """LC-07: model.bind_tools() not called when tools list is empty."""
        from app.services.agent_team.agent_invoker import ProviderConfig
        from app.services.agent_team.langchain_provider import LangChainProvider

        config = ProviderConfig(provider="langchain", model="qwen3:8b")
        provider = LangChainProvider(config, tools=[])

        mock_model = _make_mock_model()

        with patch("app.services.agent_team.langchain_provider._LANGCHAIN_AVAILABLE", True):
            with patch.dict(os.environ, {"LANGCHAIN_ENABLED": "true"}):
                with patch(
                    "app.services.agent_team.langchain_provider.ChatOllama",
                    return_value=mock_model,
                ):
                    await provider.invoke(
                        messages=[{"role": "user", "content": "simple message"}]
                    )

        mock_model.bind_tools.assert_not_called()


class TestTokenCounting:
    """LC-08: input_tokens + output_tokens populated after invoke."""

    def test_token_counter_callback_accumulates_ollama_tokens(self) -> None:
        """LC-08: on_llm_end with Ollama metadata increments token counters."""
        from app.services.agent_team.langchain_provider import TokenCounterCallback

        counter = TokenCounterCallback()

        # Simulate Ollama generation metadata (prompt_eval_count / eval_count)
        gen = MagicMock()
        gen.generation_info = {"prompt_eval_count": 42, "eval_count": 100}
        mock_response = MagicMock()
        mock_response.generations = [[gen]]

        counter.on_llm_end(mock_response)

        assert counter.input_tokens == 42
        assert counter.output_tokens == 100

    def test_token_counter_callback_accumulates_cloud_tokens(self) -> None:
        """LC-08: on_llm_end with cloud metadata (input_tokens/output_tokens)."""
        from app.services.agent_team.langchain_provider import TokenCounterCallback

        counter = TokenCounterCallback()

        gen = MagicMock()
        gen.generation_info = {"input_tokens": 200, "output_tokens": 50}
        mock_response = MagicMock()
        mock_response.generations = [[gen]]

        counter.on_llm_end(mock_response)

        assert counter.input_tokens == 200
        assert counter.output_tokens == 50

    def test_token_counter_empty_generations_no_crash(self) -> None:
        """LC-08: on_llm_end with empty generations list does not raise."""
        from app.services.agent_team.langchain_provider import TokenCounterCallback

        counter = TokenCounterCallback()
        mock_response = MagicMock()
        mock_response.generations = []

        counter.on_llm_end(mock_response)  # Should not raise

        assert counter.input_tokens == 0
        assert counter.output_tokens == 0


# ──────────────────────────────────────────────────────────────────────────────
# LC-09: LangChain exception mapping → AUTH classification
# ──────────────────────────────────────────────────────────────────────────────


class TestLangChainExceptionMapping:
    """LC-09: LangChain exceptions classify to the correct FailoverReason."""

    def test_authentication_error_classifies_as_auth(self) -> None:
        """LC-09: AuthenticationError class name → FailoverReason.AUTH → ABORT."""
        from app.services.agent_team.failover_classifier import (
            FailoverClassifier,
            FailoverReason,
            FailoverAction,
        )

        # Simulate LangChain AuthenticationError without importing langchain
        class AuthenticationError(Exception):
            pass

        err = AuthenticationError("Invalid API key")
        reason = FailoverClassifier.classify_exception(err)
        action = FailoverClassifier.get_action(reason)

        assert reason == FailoverReason.AUTH
        assert action == FailoverAction.ABORT

    def test_rate_limit_error_classifies_as_rate_limit(self) -> None:
        """LC-09: RateLimitError class name → FailoverReason.RATE_LIMIT → FALLBACK."""
        from app.services.agent_team.failover_classifier import (
            FailoverClassifier,
            FailoverReason,
            FailoverAction,
        )

        class RateLimitError(Exception):
            pass

        err = RateLimitError("Too many requests")
        reason = FailoverClassifier.classify_exception(err)
        action = FailoverClassifier.get_action(reason)

        assert reason == FailoverReason.RATE_LIMIT
        assert action == FailoverAction.FALLBACK

    def test_api_timeout_error_classifies_as_timeout(self) -> None:
        """LC-09: APITimeoutError class name → FailoverReason.TIMEOUT → FALLBACK."""
        from app.services.agent_team.failover_classifier import (
            FailoverClassifier,
            FailoverReason,
            FailoverAction,
        )

        class APITimeoutError(Exception):
            pass

        err = APITimeoutError("Request timed out")
        reason = FailoverClassifier.classify_exception(err)
        action = FailoverClassifier.get_action(reason)

        assert reason == FailoverReason.TIMEOUT
        assert action == FailoverAction.FALLBACK

    def test_bad_request_error_classifies_as_format(self) -> None:
        """LC-09: BadRequestError class name → FailoverReason.FORMAT → RETRY."""
        from app.services.agent_team.failover_classifier import (
            FailoverClassifier,
            FailoverReason,
            FailoverAction,
        )

        class BadRequestError(Exception):
            pass

        err = BadRequestError("Invalid message format")
        reason = FailoverClassifier.classify_exception(err)
        action = FailoverClassifier.get_action(reason)

        assert reason == FailoverReason.FORMAT
        assert action == FailoverAction.RETRY


# ──────────────────────────────────────────────────────────────────────────────
# LC-10: Unauthorized tool call → ToolPermissionDenied propagates
# ──────────────────────────────────────────────────────────────────────────────


class TestUnauthorizedToolCall:
    """LC-10: invoke chain raises ToolPermissionDenied for unauthorized tools."""

    @pytest.mark.asyncio
    async def test_permission_denied_propagates_through_invoke(self) -> None:
        """LC-10: ToolPermissionDenied from authorize_tool_call() is not swallowed."""
        from app.services.agent_team.agent_invoker import ProviderConfig
        from app.services.agent_team.langchain_provider import LangChainProvider
        from app.services.agent_team.tool_context import ToolPermissionDenied

        config = ProviderConfig(provider="langchain", model="qwen3:8b")
        provider = LangChainProvider(config)

        # Simulate model.ainvoke raising ToolPermissionDenied (tool guard fires)
        permission_error = ToolPermissionDenied("Tool 'execute_command' not authorized")
        mock_model = MagicMock()
        mock_model.bind_tools = MagicMock(return_value=mock_model)
        mock_model.with_structured_output = MagicMock(return_value=mock_model)
        mock_model.ainvoke = AsyncMock(side_effect=permission_error)

        with patch("app.services.agent_team.langchain_provider._LANGCHAIN_AVAILABLE", True):
            with patch.dict(os.environ, {"LANGCHAIN_ENABLED": "true"}):
                with patch(
                    "app.services.agent_team.langchain_provider.ChatOllama",
                    return_value=mock_model,
                ):
                    with pytest.raises(ToolPermissionDenied, match="not authorized"):
                        await provider.invoke(
                            messages=[{"role": "user", "content": "run a command"}]
                        )
