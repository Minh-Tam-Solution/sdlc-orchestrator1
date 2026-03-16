"""
Unified Command Registry — Single Source of Truth for CLI + OTT.

Sprint 191 (SPRINT-191-UNIFIED-COMMAND-REGISTRY).

Declarative command definitions shared by:
  - OTT channels (chat_command_router.py — LLM function calling)
  - CLI (sdlcctl governance — Typer commands)

Design references:
  - OpenClaw: 56 skills, declarative registration, per-channel command name overrides
  - TinySDLC: In-chat regex commands, @mention routing

Constraints:
  - Maximum 10 commands in registry (Expert 9 correction — prevent unbounded growth)
  - Each command MUST have: name, params, permission, handler, cli_name, ott_aliases
  - Permission matrix reuses existing RBAC scopes
"""

from __future__ import annotations

import dataclasses
from enum import Enum
from typing import Any, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ============================================================================
# Tool Parameter Schemas (Pydantic v2 — moved from chat_command_router.py)
# ============================================================================


class CreateProjectParams(BaseModel):
    """Parameters for create_project command."""

    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, max_length=2000, description="Project description")


class GetGateStatusParams(BaseModel):
    """Parameters for get_gate_status command."""

    project_id: Optional[int] = Field(None, description="Project ID (integer)")
    gate_id: Optional[UUID] = Field(None, description="Gate UUID")


class SubmitEvidenceParams(BaseModel):
    """Parameters for submit_evidence command."""

    gate_id: UUID = Field(..., description="Gate UUID")
    evidence_type: str = Field(
        ..., min_length=1, max_length=50,
        description="Evidence type (e.g., test_report)",
    )
    file_url: str = Field(..., min_length=1, description="URL or path to evidence file")


class RequestApprovalParams(BaseModel):
    """Parameters for request_approval command."""

    gate_id: UUID = Field(..., description="Gate UUID")
    action: Literal["approve", "reject"] = Field(..., description="Approval action")


class ExportAuditParams(BaseModel):
    """Parameters for export_audit command."""

    project_id: int = Field(..., description="Project ID")
    format: Literal["json", "csv"] = Field(default="json", description="Export format")


class UpdateSprintParams(BaseModel):
    """Parameters for update_sprint command (Sprint 194 ENR-01)."""

    project_id: UUID = Field(..., description="Project UUID")


class CloseSprintParams(BaseModel):
    """Parameters for close_sprint command (Sprint 201 B-05)."""

    project_id: UUID = Field(..., description="Project UUID")


class InviteMemberParams(BaseModel):
    """Parameters for invite_member command (Sprint 201 A-05)."""

    team_id: UUID = Field(..., description="Team UUID")
    email: str = Field(..., min_length=3, max_length=255, description="Email address to invite")
    role: str = Field(default="member", description="Team role (member, admin)")


class RunEvalsParams(BaseModel):
    """Parameters for run_evals command (Sprint 202 C-01)."""

    tag: Optional[str] = Field(None, max_length=50, description="Filter eval cases by tag")


class ListNotesParams(BaseModel):
    """Parameters for list_notes command (Sprint 202 C-02)."""

    agent_name: Optional[str] = Field(None, max_length=100, description="Filter notes by agent name")
    note_type: Optional[str] = Field(None, max_length=20, description="Filter by note type")


# Sprint 226 — ADR-071: 5 new commands for conversation-first SDLC workflows


class ListEvidenceParams(BaseModel):
    """Parameters for list_evidence command (Sprint 226)."""

    gate_id: Optional[UUID] = Field(None, description="Filter evidence by gate UUID")
    project_id: Optional[int] = Field(None, description="Filter by project ID")


class EvaluateGateParams(BaseModel):
    """Parameters for evaluate_gate command (Sprint 226)."""

    gate_id: UUID = Field(..., description="Gate UUID to evaluate")


class PlanSprintParams(BaseModel):
    """Parameters for plan_sprint command (Sprint 226)."""

    project_id: UUID = Field(..., description="Project UUID")
    sprint_name: Optional[str] = Field(None, max_length=100, description="Sprint name")
    goal: Optional[str] = Field(None, max_length=500, description="Sprint goal")


class RunQualityCheckParams(BaseModel):
    """Parameters for run_quality_check command (Sprint 226)."""

    project_id: UUID = Field(..., description="Project UUID")
    file_path: Optional[str] = Field(None, description="Specific file to check")


class GetMetricsParams(BaseModel):
    """Parameters for get_metrics command (Sprint 226)."""

    metric_type: Literal["completion", "override", "retention", "baseline"] = Field(
        default="completion", description="Metric type to query",
    )


# ============================================================================
# Tool Name Enum — Bounded Allowlist (T-01)
# ============================================================================


class ToolName(str, Enum):
    """Bounded allowlist of governance tools (T-01)."""

    CREATE_PROJECT = "create_project"
    GET_GATE_STATUS = "get_gate_status"
    SUBMIT_EVIDENCE = "submit_evidence"
    REQUEST_APPROVAL = "request_approval"
    EXPORT_AUDIT = "export_audit"
    UPDATE_SPRINT = "update_sprint"
    CLOSE_SPRINT = "close_sprint"
    INVITE_MEMBER = "invite_member"
    RUN_EVALS = "run_evals"
    LIST_NOTES = "list_notes"
    # Sprint 226 — ADR-071 conversation-first commands
    LIST_EVIDENCE = "list_evidence"
    EVALUATE_GATE = "evaluate_gate"
    PLAN_SPRINT = "plan_sprint"
    RUN_QUALITY_CHECK = "run_quality_check"
    GET_METRICS = "get_metrics"


# ============================================================================
# Command Definition
# ============================================================================

# Maximum number of commands allowed in the registry.
# Sprint 226: raised from 10 → 15 for conversation-first workflows (ADR-071).
MAX_COMMANDS = 15


@dataclasses.dataclass(frozen=True)
class CommandDef:
    """Declarative command definition — single source of truth for CLI + OTT."""

    name: str
    """Canonical command name (matches ToolName value)."""

    description: str
    """English description for help text and LLM prompts."""

    params: type[BaseModel]
    """Pydantic v2 model for parameter validation."""

    permission: str
    """RBAC scope required (e.g., 'governance:read')."""

    handler: str
    """Dotted path to handler (informational — actual dispatch in adapters)."""

    cli_name: str
    """CLI command name for sdlcctl (e.g., 'gate-status')."""

    ott_description: str
    """Description including Vietnamese aliases for LLM function calling."""

    ott_aliases: tuple[str, ...]
    """Vietnamese and English aliases for OTT matching."""

    required_params: tuple[str, ...] = ()
    """Parameter names required in the JSON Schema."""


# ============================================================================
# Governance Commands — 10 Tools (T-01 + Sprint 194 + Sprint 201 + Sprint 202)
# ============================================================================

GOVERNANCE_COMMANDS: list[CommandDef] = [
    CommandDef(
        name="create_project",
        description="Create a new SDLC project",
        params=CreateProjectParams,
        permission="projects:write",
        handler="project_service.create_project",
        cli_name="create-project",
        ott_description=(
            "Create a new SDLC project. "
            "Use when user says 'tạo dự án', 'create project', etc."
        ),
        ott_aliases=("tạo dự án", "create project"),
        required_params=("name",),
    ),
    CommandDef(
        name="get_gate_status",
        description="Get quality gate status for a project",
        params=GetGateStatusParams,
        permission="governance:read",
        handler="gate_service.get_gate_status",
        cli_name="gate-status",
        ott_description=(
            "Get quality gate status for a project. "
            "Use when user says 'gate status', 'trạng thái gate', 'check gate', etc."
        ),
        ott_aliases=("gate status", "trạng thái gate", "check gate"),
        required_params=(),
    ),
    CommandDef(
        name="submit_evidence",
        description="Submit evidence for a quality gate",
        params=SubmitEvidenceParams,
        permission="governance:write",
        handler="evidence_service.submit_evidence",
        cli_name="submit-evidence",
        ott_description=(
            "Submit evidence for a quality gate. "
            "Use when user says 'upload evidence', 'nộp bằng chứng', 'submit', etc."
        ),
        ott_aliases=("nộp bằng chứng", "submit evidence", "upload evidence"),
        required_params=("gate_id", "evidence_type", "file_url"),
    ),
    CommandDef(
        name="request_approval",
        description="Request approval or rejection for a quality gate",
        params=RequestApprovalParams,
        permission="governance:approve",
        handler="gate_service.request_approval",
        cli_name="request-approval",
        ott_description=(
            "Request approval or rejection for a quality gate. "
            "Use when user says 'approve', 'reject', 'duyệt', 'từ chối', etc."
        ),
        ott_aliases=("approve", "reject", "duyệt", "từ chối"),
        required_params=("gate_id", "action"),
    ),
    CommandDef(
        name="export_audit",
        description="Export audit log for a project",
        params=ExportAuditParams,
        permission="governance:read",
        handler="audit_service.export_audit",
        cli_name="export-audit",
        ott_description=(
            "Export audit log for a project. "
            "Use when user says 'export audit', 'xuất báo cáo', 'compliance report', etc."
        ),
        ott_aliases=("export audit", "xuất báo cáo", "compliance report"),
        required_params=("project_id",),
    ),
    CommandDef(
        name="update_sprint",
        description="Regenerate and push CURRENT-SPRINT.md for the active sprint",
        params=UpdateSprintParams,
        permission="governance:write",
        handler="sprint_command_handler.handle_update_sprint",
        cli_name="update-sprint",
        ott_description=(
            "Update CURRENT-SPRINT.md for the active sprint. "
            "Use when user says 'update sprint', 'cập nhật sprint', "
            "'refresh sprint file', etc."
        ),
        ott_aliases=("update sprint", "cập nhật sprint", "refresh sprint"),
        required_params=("project_id",),
    ),
    CommandDef(
        name="close_sprint",
        description="Close the active sprint and run G-Sprint-Close verification",
        params=CloseSprintParams,
        permission="governance:write",
        handler="sprint_governance_handler.handle_close_sprint",
        cli_name="close-sprint",
        ott_description=(
            "Close the active sprint with G-Sprint-Close verification. "
            "Use when user says 'close sprint', 'đóng sprint', "
            "'kết thúc sprint', 'finish sprint', etc."
        ),
        ott_aliases=(
            "close sprint", "đóng sprint", "kết thúc sprint", "finish sprint",
        ),
        required_params=("project_id",),
    ),
    CommandDef(
        name="invite_member",
        description="Invite a team member via email",
        params=InviteMemberParams,
        permission="projects:admin",
        handler="team_invite_handler.handle_invite_member",
        cli_name="invite-member",
        ott_description=(
            "Invite a new team member via email. "
            "Use when user says 'invite', 'mời thành viên', "
            "'add member', 'thêm thành viên', etc."
        ),
        ott_aliases=(
            "invite", "mời", "mời thành viên", "add member", "thêm thành viên",
        ),
        required_params=("team_id", "email"),
    ),
    CommandDef(
        name="run_evals",
        description="Run automated eval suite for agent governance responses",
        params=RunEvalsParams,
        permission="governance:read",
        handler="eval_scorer.run_suite",
        cli_name="run-evals",
        ott_description=(
            "Run the automated evaluation suite for agent responses. "
            "Use when user says 'run evals', 'chạy đánh giá', "
            "'evaluate agents', 'kiểm tra chất lượng', etc."
        ),
        ott_aliases=(
            "run evals", "chạy đánh giá", "evaluate agents",
            "kiểm tra chất lượng",
        ),
        required_params=(),
    ),
    CommandDef(
        name="list_notes",
        description="List saved agent notes (cross-session memory)",
        params=ListNotesParams,
        permission="governance:read",
        handler="note_service.list_notes",
        cli_name="list-notes",
        ott_description=(
            "List agent's saved structured notes. "
            "Use when user says 'list notes', 'xem ghi chú', "
            "'show notes', 'ghi chú agent', etc."
        ),
        ott_aliases=(
            "list notes", "xem ghi chú", "show notes", "ghi chú agent",
        ),
        required_params=(),
    ),
    # ── Sprint 226 — ADR-071 Conversation-First Commands ──────────────
    CommandDef(
        name="list_evidence",
        description="List evidence artifacts for a gate or project",
        params=ListEvidenceParams,
        permission="governance:read",
        handler="evidence_service.list_evidence",
        cli_name="list-evidence",
        ott_description=(
            "List evidence for a gate or project. "
            "Use when user says 'list evidence', 'xem bằng chứng', 'evidence status', etc."
        ),
        ott_aliases=("list evidence", "xem bằng chứng", "evidence status"),
        required_params=(),
    ),
    CommandDef(
        name="evaluate_gate",
        description="Trigger gate evaluation (OPA policy check)",
        params=EvaluateGateParams,
        permission="governance:write",
        handler="gate_service.evaluate_gate",
        cli_name="evaluate-gate",
        ott_description=(
            "Evaluate a quality gate. "
            "Use when user says 'evaluate gate', 'đánh giá gate', 'check gate quality', etc."
        ),
        ott_aliases=("evaluate gate", "đánh giá gate", "check gate quality"),
        required_params=("gate_id",),
    ),
    CommandDef(
        name="plan_sprint",
        description="Create or plan a sprint for a project",
        params=PlanSprintParams,
        permission="governance:write",
        handler="planning_service.plan_sprint",
        cli_name="plan-sprint",
        ott_description=(
            "Plan a new sprint for a project. "
            "Use when user says 'plan sprint', 'lên kế hoạch sprint', 'tạo sprint', etc."
        ),
        ott_aliases=("plan sprint", "lên kế hoạch sprint", "tạo sprint"),
        required_params=("project_id",),
    ),
    CommandDef(
        name="run_quality_check",
        description="Run quality pipeline (SAST + tests) on project code",
        params=RunQualityCheckParams,
        permission="governance:write",
        handler="codegen_service.run_quality_check",
        cli_name="quality-check",
        ott_description=(
            "Run quality checks (SAST, tests) on project code. "
            "Use when user says 'run tests', 'chạy kiểm tra', 'quality check', 'SAST scan', etc."
        ),
        ott_aliases=("run tests", "chạy kiểm tra", "quality check", "SAST scan"),
        required_params=("project_id",),
    ),
    CommandDef(
        name="get_metrics",
        description="Get product metrics (completion rate, override rate, retention)",
        params=GetMetricsParams,
        permission="governance:read",
        handler="product_metrics_service.get_metrics",
        cli_name="get-metrics",
        ott_description=(
            "Get pilot product metrics. "
            "Use when user says 'metrics', 'số liệu', 'dashboard metrics', 'KPI', etc."
        ),
        ott_aliases=("metrics", "số liệu", "dashboard metrics", "KPI"),
        required_params=(),
    ),
]

assert len(GOVERNANCE_COMMANDS) <= MAX_COMMANDS, (
    f"Registry exceeds {MAX_COMMANDS} command limit "
    f"(has {len(GOVERNANCE_COMMANDS)})"
)


# ============================================================================
# Public API
# ============================================================================


def get_commands() -> list[CommandDef]:
    """Return all registered governance commands."""
    return list(GOVERNANCE_COMMANDS)


def get_command(name: str) -> CommandDef | None:
    """Look up a command by canonical name."""
    for cmd in GOVERNANCE_COMMANDS:
        if cmd.name == name:
            return cmd
    return None


def to_tool_schemas() -> dict[str, type[BaseModel]]:
    """Generate ToolName → Pydantic model mapping (replaces _TOOL_SCHEMAS).

    Used by chat_command_router.py for Pydantic validation of LLM tool calls.
    """
    return {cmd.name: cmd.params for cmd in GOVERNANCE_COMMANDS}


def to_ollama_tools() -> list[dict[str, Any]]:
    """Generate Ollama /api/chat tool definitions (replaces OLLAMA_TOOLS).

    Produces JSON Schema format compatible with Ollama's function calling.
    """
    tools: list[dict[str, Any]] = []
    for cmd in GOVERNANCE_COMMANDS:
        schema = cmd.params.model_json_schema()
        properties: dict[str, Any] = {}
        for prop_name, prop_schema in schema.get("properties", {}).items():
            prop_def: dict[str, Any] = {}
            # Map JSON Schema types
            if "type" in prop_schema:
                prop_def["type"] = prop_schema["type"]
            elif "anyOf" in prop_schema:
                # Optional fields: pick the non-null type
                for variant in prop_schema["anyOf"]:
                    if variant.get("type") != "null":
                        prop_def.update(variant)
                        break
            if "format" in prop_schema:
                prop_def["format"] = prop_schema["format"]
            if "enum" in prop_schema:
                prop_def["enum"] = prop_schema["enum"]
            if "description" in prop_schema:
                prop_def["description"] = prop_schema["description"]
            elif prop_name in ("description",):
                prop_def["description"] = f"{prop_name.replace('_', ' ').title()}"
            properties[prop_name] = prop_def

        tools.append({
            "type": "function",
            "function": {
                "name": cmd.name,
                "description": cmd.ott_description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": list(cmd.required_params),
                },
            },
        })
    return tools
