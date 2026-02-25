"""
Sprint 205 — LangChain Tool Registry Unit Tests (LT-01 to LT-05).

Tests cover ADR-066 (LangChain Multi-Agent Orchestration) Track B:
  LT-01: gate_status tool — returns GateStatusResult Pydantic schema
  LT-02: submit_evidence tool — returns EvidenceSubmitResult Pydantic schema
  LT-03: read_file tool — authorize_tool_call() is called (LT-03 permission check)
  LT-04: Tool without permission — PermissionDenied raised
  LT-05: All 5 tools have output schemas (Pydantic BaseModel subclasses)

Tests use ToolContext with restrictive AgentToolPermissions to verify
authorize_tool_call() integration without requiring LangChain packages.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from app.services.agent_team.tool_context import (
    AgentToolPermissions,
    PermissionDenied,
    ToolContext,
    ToolPermissionDenied,
    authorize_tool_call,
)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────


def _make_permissive_ctx() -> ToolContext:
    """Build a ToolContext that allows all tools."""
    return ToolContext(
        channel="test",
        sender_id="test-agent",
        origin_conversation_id=uuid4(),
        permissions=AgentToolPermissions(allowed_tools=["*"], denied_tools=[]),
    )


def _make_restricted_ctx(allowed: list[str], denied: list[str] | None = None) -> ToolContext:
    """Build a ToolContext with a specific allowed/denied tool set."""
    return ToolContext(
        channel="test",
        sender_id="restricted-agent",
        origin_conversation_id=uuid4(),
        permissions=AgentToolPermissions(
            allowed_tools=allowed,
            denied_tools=denied or [],
        ),
    )


# ──────────────────────────────────────────────────────────────────────────────
# LT-01: gate_status tool
# ──────────────────────────────────────────────────────────────────────────────


class TestGateStatusTool:
    """LT-01: gate_status returns GateStatusResult with correct schema."""

    def test_gate_status_returns_schema_typed_result(self) -> None:
        """LT-01: _gate_status_fn returns a GateStatusResult Pydantic instance."""
        from app.services.agent_team.langchain_tool_registry import (
            GateStatusResult,
            _gate_status_fn,
        )

        ctx = _make_permissive_ctx()
        result = _gate_status_fn("gate-uuid-123", tool_context=ctx)

        assert isinstance(result, GateStatusResult)
        assert result.gate_id == "gate-uuid-123"
        assert isinstance(result.status, str)

    def test_gate_status_no_context_no_error(self) -> None:
        """LT-01: gate_status with tool_context=None executes without permission error."""
        from app.services.agent_team.langchain_tool_registry import _gate_status_fn

        result = _gate_status_fn("gate-abc", tool_context=None)
        assert result.gate_id == "gate-abc"

    def test_gate_status_result_is_pydantic_model(self) -> None:
        """LT-01: GateStatusResult is a Pydantic BaseModel (LT-05 prerequisite)."""
        from pydantic import BaseModel
        from app.services.agent_team.langchain_tool_registry import GateStatusResult

        assert issubclass(GateStatusResult, BaseModel)


# ──────────────────────────────────────────────────────────────────────────────
# LT-02: submit_evidence tool
# ──────────────────────────────────────────────────────────────────────────────


class TestSubmitEvidenceTool:
    """LT-02: submit_evidence returns EvidenceSubmitResult with correct schema."""

    def test_submit_evidence_returns_schema_typed_result(self) -> None:
        """LT-02: _submit_evidence_fn returns an EvidenceSubmitResult Pydantic instance."""
        from app.services.agent_team.langchain_tool_registry import (
            EvidenceSubmitResult,
            _submit_evidence_fn,
        )

        ctx = _make_permissive_ctx()
        result = _submit_evidence_fn(
            gate_id="gate-xyz",
            evidence_type="TEST_RESULTS",
            content="test coverage 95%",
            tool_context=ctx,
        )

        assert isinstance(result, EvidenceSubmitResult)
        assert result.gate_id == "gate-xyz"
        assert result.status == "queued"
        assert "TEST_RESULTS" in result.message

    def test_evidence_submit_result_is_pydantic_model(self) -> None:
        """LT-02: EvidenceSubmitResult is a Pydantic BaseModel."""
        from pydantic import BaseModel
        from app.services.agent_team.langchain_tool_registry import EvidenceSubmitResult

        assert issubclass(EvidenceSubmitResult, BaseModel)


# ──────────────────────────────────────────────────────────────────────────────
# LT-03: read_file tool — authorize_tool_call() called
# ──────────────────────────────────────────────────────────────────────────────


class TestReadFileTool:
    """LT-03: read_file invokes authorize_tool_call() before executing."""

    def test_read_file_calls_authorize_tool_call(self, tmp_path) -> None:
        """LT-03: authorize_tool_call('read_file', context) is called on execution."""
        from unittest.mock import patch
        from app.services.agent_team.langchain_tool_registry import _read_file_fn

        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")
        ctx = _make_permissive_ctx()

        with patch(
            "app.services.agent_team.langchain_tool_registry.authorize_tool_call"
        ) as mock_auth:
            _read_file_fn(str(test_file), tool_context=ctx)

        mock_auth.assert_called_once_with("read_file", ctx)

    def test_read_file_returns_content(self, tmp_path) -> None:
        """LT-03: _read_file_fn reads file content and returns ReadFileResult."""
        from app.services.agent_team.langchain_tool_registry import ReadFileResult, _read_file_fn

        test_file = tmp_path / "sample.txt"
        test_file.write_text("line1\nline2\nline3")

        ctx = _make_permissive_ctx()
        result = _read_file_fn(str(test_file), tool_context=ctx)

        assert isinstance(result, ReadFileResult)
        assert "line1" in result.content
        assert result.line_count == 3

    def test_read_file_nonexistent_returns_error_message(self, tmp_path) -> None:
        """LT-03: _read_file_fn returns error content for missing file, does not raise."""
        from app.services.agent_team.langchain_tool_registry import _read_file_fn

        result = _read_file_fn("/nonexistent/path/file.txt", tool_context=None)
        assert "Error reading file" in result.content
        assert result.line_count == 0


# ──────────────────────────────────────────────────────────────────────────────
# LT-04: Tool without permission → PermissionDenied raised
# ──────────────────────────────────────────────────────────────────────────────


class TestToolPermissionDenied:
    """LT-04: ToolPermissionDenied raised when context denies the tool."""

    def test_denied_tool_raises_permission_denied(self) -> None:
        """LT-04: authorize_tool_call raises ToolPermissionDenied for denied tools."""
        ctx = _make_restricted_ctx(
            allowed=["*"],
            denied=["execute_command"],
        )

        with pytest.raises(ToolPermissionDenied, match="execute_command"):
            authorize_tool_call("execute_command", ctx)

    def test_not_in_allowed_list_raises_permission_denied(self) -> None:
        """LT-04: Tool not in allowed_tools list raises ToolPermissionDenied."""
        ctx = _make_restricted_ctx(allowed=["gate_status", "read_file"])

        with pytest.raises(ToolPermissionDenied, match="submit_evidence"):
            authorize_tool_call("submit_evidence", ctx)

    def test_permission_denied_is_alias_for_tool_permission_denied(self) -> None:
        """LT-04: PermissionDenied alias equals ToolPermissionDenied."""
        assert PermissionDenied is ToolPermissionDenied

    def test_no_context_no_exception(self) -> None:
        """LT-04: authorize_tool_call with None context never raises."""
        # Should not raise for any tool name when context is None
        authorize_tool_call("execute_command", None)
        authorize_tool_call("any_tool", None)

    def test_gate_status_fn_raises_when_denied(self) -> None:
        """LT-04: _gate_status_fn raises ToolPermissionDenied via authorize_tool_call."""
        from app.services.agent_team.langchain_tool_registry import _gate_status_fn

        ctx = _make_restricted_ctx(allowed=["read_file"])  # gate_status not in list

        with pytest.raises(ToolPermissionDenied):
            _gate_status_fn("gate-123", tool_context=ctx)


# ──────────────────────────────────────────────────────────────────────────────
# LT-05: All 5 tools have Pydantic output schemas
# ──────────────────────────────────────────────────────────────────────────────


class TestAllToolsHaveOutputSchemas:
    """LT-05: All 5 registered tools have Pydantic BaseModel output schemas."""

    def test_all_five_tool_schemas_are_pydantic_models(self) -> None:
        """LT-05: Input + output schemas for all 5 tools are Pydantic BaseModel subclasses."""
        from pydantic import BaseModel
        from app.services.agent_team.langchain_tool_registry import (
            GateStatusInput,
            GateStatusResult,
            SubmitEvidenceInput,
            EvidenceSubmitResult,
            ReadFileInput,
            ReadFileResult,
            SearchInput,
            SearchResult,
            ExecuteCommandInput,
            ExecuteCommandResult,
        )

        schema_pairs = [
            (GateStatusInput, GateStatusResult),
            (SubmitEvidenceInput, EvidenceSubmitResult),
            (ReadFileInput, ReadFileResult),
            (SearchInput, SearchResult),
            (ExecuteCommandInput, ExecuteCommandResult),
        ]

        for input_schema, output_schema in schema_pairs:
            assert issubclass(input_schema, BaseModel), (
                f"{input_schema.__name__} is not a Pydantic BaseModel"
            )
            assert issubclass(output_schema, BaseModel), (
                f"{output_schema.__name__} is not a Pydantic BaseModel"
            )

    def test_registry_tool_names_count_is_five(self) -> None:
        """LT-05: LangChainToolRegistry.TOOL_NAMES contains exactly 5 names."""
        from app.services.agent_team.langchain_tool_registry import LangChainToolRegistry

        assert len(LangChainToolRegistry.TOOL_NAMES) == 5

    def test_registry_tool_names_are_expected(self) -> None:
        """LT-05: TOOL_NAMES matches the 5 documented tool names."""
        from app.services.agent_team.langchain_tool_registry import LangChainToolRegistry

        expected = {
            "gate_status",
            "submit_evidence",
            "read_file",
            "search",
            "execute_command",
        }
        assert set(LangChainToolRegistry.TOOL_NAMES) == expected

    def test_authorize_tool_call_is_exported_from_tool_context(self) -> None:
        """LT-05: authorize_tool_call() is importable from tool_context module."""
        from app.services.agent_team.tool_context import authorize_tool_call  # noqa: F401

        assert callable(authorize_tool_call)
