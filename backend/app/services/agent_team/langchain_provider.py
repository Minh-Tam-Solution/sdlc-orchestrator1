"""
=========================================================================
LangChain Provider Plugin — Optional Dependency Guard + Feature Flag.
SDLC Orchestrator - Sprint 205 (LangChain Provider Plugin)

Version: 1.0.0
Date: February 2026
Status: ACTIVE - Sprint 205
Authority: CTO Approved (ADR-066)
Reference: ADR-066-LangChain-Multi-Agent-Orchestration.md

Architecture (D-066-01): LangChain is PROVIDER ONLY.
  - Control Plane (agent_invoker.py) is truth.
  - LangChain handles: model wrappers, structured output, tool binding, token counting.
  - State stays in agent_conversations.metadata_ JSONB (not LangChain memory).
  - LangGraph workflows are Sprint 206 scope — not in this file.

Feature Flag: LANGCHAIN_ENABLED=true (env var) activates this provider.
  - When false (default): raise AgentInvokerError on any langchain provider call.
  - When packages absent (_LANGCHAIN_AVAILABLE=False): same error, clean import.

Optional Dependency Guard (SDLC 6.1.0 §5 pattern — codified Sprint 185):
  - try/except ImportError at module level
  - _LANGCHAIN_AVAILABLE sentinel for runtime checks
  - Module imports cleanly without any LangChain packages installed

Model routing via config.model (D-066-01):
  - "claude-*" → ChatAnthropic (Anthropic API)
  - "gpt-*"    → ChatOpenAI (OpenAI API)
  - else        → ChatOllama (Ollama REST API, default)

Zero Mock Policy: Production-ready LangChain integration
=========================================================================
"""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Optional Dependency Guard (SDLC 6.1.0 §5 pattern — Sprint 185 codified)
# Install: pip install 'langchain-community>=0.3 langchain-anthropic>=0.3
#          langchain-openai>=0.3 langchain-core>=0.3'
# ─────────────────────────────────────────────────────────────────────────────
try:
    from langchain_core.callbacks.base import BaseCallbackHandler
    from langchain_core.messages import (
        AIMessage,
        HumanMessage,
        SystemMessage,
    )
    from langchain_core.outputs import LLMResult
    from langchain_community.chat_models import ChatOllama
    from langchain_anthropic import ChatAnthropic
    from langchain_openai import ChatOpenAI

    _LANGCHAIN_AVAILABLE = True
except ImportError:  # pragma: no cover
    _LANGCHAIN_AVAILABLE = False
    # Minimal stubs so module imports cleanly and tests can construct message
    # objects without the real LangChain packages.  Chat model classes stay
    # None — tests patch them individually via unittest.mock.patch.

    class BaseCallbackHandler:  # type: ignore[no-redef]
        pass

    class LLMResult:  # type: ignore[no-redef]
        def __init__(self, generations=None, **kwargs):
            self.generations = generations or []

    class _LCMessage:
        """Base stub for LangChain message types."""
        def __init__(self, content: str = "", **kwargs):
            self.content = content

    class HumanMessage(_LCMessage):  # type: ignore[no-redef]
        pass

    class SystemMessage(_LCMessage):  # type: ignore[no-redef]
        pass

    class AIMessage(_LCMessage):  # type: ignore[no-redef]
        pass

    ChatOllama = None  # type: ignore[assignment,misc]
    ChatAnthropic = None  # type: ignore[assignment,misc]
    ChatOpenAI = None  # type: ignore[assignment,misc]


def _is_langchain_enabled() -> bool:
    """Return True when LANGCHAIN_ENABLED=true (case-insensitive, default false)."""
    return os.environ.get("LANGCHAIN_ENABLED", "false").lower() == "true"


# ─────────────────────────────────────────────────────────────────────────────
# Token Counting Callback (LC-08)
# ─────────────────────────────────────────────────────────────────────────────


class TokenCounterCallback(BaseCallbackHandler):  # type: ignore[misc]
    """
    LangChain callback that captures token usage from on_llm_end.

    Handles both Ollama (prompt_eval_count/eval_count) and cloud providers
    (input_tokens/output_tokens) metadata keys to produce a unified count.

    Usage:
        counter = TokenCounterCallback()
        model = ChatOllama(..., callbacks=[counter])
        await model.ainvoke(messages)
        print(counter.input_tokens, counter.output_tokens)
    """

    def __init__(self) -> None:
        self.input_tokens: int = 0
        self.output_tokens: int = 0

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:  # type: ignore[override]
        """Accumulate token counts across all generation metadata entries."""
        for gen_list in getattr(response, "generations", []):
            for gen in gen_list:
                info = getattr(gen, "generation_info", {}) or {}
                # Ollama fields (prompt_eval_count / eval_count)
                self.input_tokens += info.get("prompt_eval_count", 0)
                self.output_tokens += info.get("eval_count", 0)
                # Anthropic/OpenAI fields (may appear alongside Ollama)
                self.input_tokens += info.get("input_tokens", 0)
                self.output_tokens += info.get("output_tokens", 0)


# ─────────────────────────────────────────────────────────────────────────────
# LangChainProvider
# ─────────────────────────────────────────────────────────────────────────────


class LangChainProvider:
    """
    LangChain provider plugin for AgentInvoker._call_langchain().

    Wraps ChatOllama / ChatAnthropic / ChatOpenAI behind a uniform
    (content, input_tokens, output_tokens) interface compatible with the
    existing AgentInvoker failover chain.

    Model selection based on config.model name (D-066-01):
      - "claude-*" → ChatAnthropic (requires ANTHROPIC_API_KEY)
      - "gpt-*"    → ChatOpenAI   (requires OPENAI_API_KEY)
      - else        → ChatOllama   (default, uses OLLAMA_BASE_URL env var)

    Optional capabilities via constructor args:
      - tools:         List of LangChain StructuredTool instances (bind_tools)
      - output_schema: Pydantic model class (with_structured_output)
    """

    def __init__(
        self,
        config: Any,
        tools: list[Any] | None = None,
    ) -> None:
        """
        Args:
            config: ProviderConfig from agent_invoker (provider, model, timeout_seconds).
            tools:  Optional list of LangChain StructuredTool instances for bind_tools().
        """
        self.config = config
        self.tools = tools or []

    def _assert_available(self) -> None:
        """
        Guard: raise AgentInvokerError when LangChain is unavailable or disabled.

        Called at the start of invoke() so errors surface early with clear messages.
        """
        # Import here to avoid circular dependency (agent_invoker imports us)
        from app.services.agent_team.agent_invoker import AgentInvokerError

        if not _LANGCHAIN_AVAILABLE:
            raise AgentInvokerError(
                "LangChain packages not installed. "
                "Install: pip install 'langchain-community>=0.3 langchain-anthropic>=0.3 "
                "langchain-openai>=0.3 langchain-core>=0.3'"
            )
        if not _is_langchain_enabled():
            raise AgentInvokerError(
                "LangChain provider disabled. "
                "Set LANGCHAIN_ENABLED=true to enable."
            )

    def _build_model(
        self,
        max_tokens: int,
        temperature: float,
        callback: "TokenCounterCallback",
    ) -> Any:
        """
        Build the appropriate LangChain chat model and configure callbacks.

        Model backend is selected by config.model:
          - "claude-*" → ChatAnthropic
          - "gpt-*"    → ChatOpenAI
          - else        → ChatOllama (local Ollama server)

        Returns the model with tools bound (if any were provided to constructor).

        Raises:
            RuntimeError: If required API key env var is missing.
        """
        model_name = self.config.model
        timeout = self.config.timeout_seconds
        callbacks = [callback]

        if "claude-" in model_name:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError("ANTHROPIC_API_KEY not set for ChatAnthropic")
            model = ChatAnthropic(  # type: ignore[misc]
                model=model_name,
                api_key=api_key,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=timeout,
                callbacks=callbacks,
            )
        elif "gpt-" in model_name:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY not set for ChatOpenAI")
            model = ChatOpenAI(  # type: ignore[misc]
                model=model_name,
                openai_api_key=api_key,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=timeout,
                callbacks=callbacks,
            )
        else:
            # Default: ChatOllama (Ollama REST API)
            ollama_base_url = os.environ.get(
                "OLLAMA_BASE_URL", "http://api.nhatquangholding.com:11434"
            )
            model = ChatOllama(  # type: ignore[misc]
                model=model_name,
                base_url=ollama_base_url,
                num_predict=max_tokens,
                temperature=temperature,
                timeout=timeout,
                callbacks=callbacks,
            )

        # Bind tools for tool-calling support (B3 from sprint plan)
        if self.tools:
            model = model.bind_tools(self.tools)

        return model

    def _build_messages(
        self,
        messages: list[dict[str, Any]],
        system_prompt: str | None,
    ) -> list[Any]:
        """
        Convert OpenAI-format message dicts to LangChain message objects.

        Supports roles: "system", "user" (default), "assistant".
        A leading system_prompt argument is inserted before message history.
        """
        lc_messages: list[Any] = []
        if system_prompt:
            lc_messages.append(SystemMessage(content=system_prompt))
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                lc_messages.append(SystemMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))
            else:
                lc_messages.append(HumanMessage(content=content))
        return lc_messages

    async def invoke(
        self,
        messages: list[dict[str, Any]],
        system_prompt: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        output_schema: Any | None = None,
    ) -> tuple[str, int, int]:
        """
        Invoke the LangChain model and return (content, input_tokens, output_tokens).

        Compatible with AgentInvoker._call_provider() return type so it can
        be used as a drop-in provider branch.

        Args:
            messages:      Conversation messages in OpenAI format (role/content dicts).
            system_prompt: Optional system instruction string.
            max_tokens:    Maximum tokens to generate.
            temperature:   Sampling temperature (0.0–1.0).
            output_schema: Optional Pydantic model class for structured output (LC-06).
                           When provided, model.with_structured_output(schema) is used
                           and content is the JSON serialization of the Pydantic instance.

        Returns:
            (content: str, input_tokens: int, output_tokens: int)

        Raises:
            AgentInvokerError: LangChain unavailable or LANGCHAIN_ENABLED=false.
            RuntimeError:      API key missing or model build failure.
        """
        self._assert_available()

        counter = TokenCounterCallback()
        model = self._build_model(max_tokens, temperature, counter)

        # Apply structured output if schema provided (LC-06)
        if output_schema is not None:
            model = model.with_structured_output(output_schema)

        lc_messages = self._build_messages(messages, system_prompt)

        # Invoke asynchronously via LangChain's ainvoke
        response = await model.ainvoke(lc_messages)

        # Extract content string
        if output_schema is not None:
            # Structured output: response is a Pydantic model instance
            if hasattr(response, "model_dump_json"):
                content = response.model_dump_json()
            else:
                content = str(response)
        else:
            # Regular chat output: response is AIMessage
            content = response.content if hasattr(response, "content") else str(response)

        logger.info(
            "TRACE_LANGCHAIN provider=langchain model=%s "
            "in=%d out=%d",
            self.config.model,
            counter.input_tokens,
            counter.output_tokens,
        )

        return content, counter.input_tokens, counter.output_tokens
