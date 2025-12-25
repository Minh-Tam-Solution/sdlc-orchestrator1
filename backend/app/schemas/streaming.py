"""
=========================================================================
Streaming Schemas - SSE Event Models for Code Generation
SDLC Orchestrator - Sprint 51A

Version: 1.0.0
Date: December 25, 2025
Status: ACTIVE - Sprint 51A Progressive Code Generation
Authority: Backend Lead + CTO Approved
Foundation: OpenAPI 3.0, Pydantic v2, SSE (Server-Sent Events)
Framework: SDLC 5.1.2 Complete Lifecycle

Purpose:
- SSE event models for streaming code generation
- Real-time file generation progress tracking
- Quality gate streaming results
- Session-based recovery support

Event Types:
- started: Generation session initiated
- file_generating: File generation in progress
- file_generated: Single file completed with content
- quality_started: Quality pipeline initiated
- quality_gate: Individual gate result
- completed: All files generated successfully
- error: Generation failed with recovery option

Zero Mock Policy: Production-ready Pydantic models
=========================================================================
"""

from datetime import datetime
from typing import Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


# =========================================================================
# SSE Event Type Definition
# =========================================================================

StreamEventType = Literal[
    "started",
    "file_generating",
    "file_generated",
    "quality_started",
    "quality_gate",
    "completed",
    "error",
]


# =========================================================================
# Base Stream Event
# =========================================================================


class StreamEvent(BaseModel):
    """
    Base class for all SSE stream events.

    All events include:
    - type: Event type identifier
    - timestamp: ISO 8601 timestamp
    - session_id: Unique session for recovery
    """

    type: StreamEventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: str = Field(..., description="Unique session ID for recovery")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


# =========================================================================
# Generation Lifecycle Events
# =========================================================================


class StartedEvent(StreamEvent):
    """
    Event: Generation started.
    Sent when code generation begins.

    Example:
        {
            "type": "started",
            "timestamp": "2025-12-25T10:30:00Z",
            "session_id": "abc123",
            "model": "qwen2.5-coder:32b",
            "provider": "ollama"
        }
    """

    type: Literal["started"] = "started"
    model: str = Field(..., description="AI model used for generation")
    provider: str = Field(..., description="Provider name (ollama, claude, etc)")


class FileGeneratingEvent(StreamEvent):
    """
    Event: File is being generated.
    Sent when a new file starts generating.

    Example:
        {
            "type": "file_generating",
            "timestamp": "2025-12-25T10:30:02Z",
            "session_id": "abc123",
            "path": "app/main.py"
        }
    """

    type: Literal["file_generating"] = "file_generating"
    path: str = Field(..., description="Relative file path being generated")


class FileGeneratedEvent(StreamEvent):
    """
    Event: File generation complete.
    Sent when a file is fully generated with content.

    Example:
        {
            "type": "file_generated",
            "timestamp": "2025-12-25T10:30:05Z",
            "session_id": "abc123",
            "path": "app/main.py",
            "content": "from fastapi import FastAPI...",
            "lines": 45,
            "language": "python",
            "syntax_valid": true
        }
    """

    type: Literal["file_generated"] = "file_generated"
    path: str = Field(..., description="Relative file path")
    content: str = Field(..., description="Full file content")
    lines: int = Field(..., ge=0, description="Number of lines in file")
    language: str = Field(..., description="Programming language (python, typescript, etc)")
    syntax_valid: Optional[bool] = Field(
        None, description="Syntax validation result (None if not checked)"
    )


# =========================================================================
# Quality Gate Events
# =========================================================================


class QualityStartedEvent(StreamEvent):
    """
    Event: Quality pipeline started.
    Sent when quality gates begin running.

    Example:
        {
            "type": "quality_started",
            "timestamp": "2025-12-25T10:30:15Z",
            "session_id": "abc123"
        }
    """

    type: Literal["quality_started"] = "quality_started"


class QualityGateEvent(StreamEvent):
    """
    Event: Quality gate result.
    Sent for each gate completion.

    Example:
        {
            "type": "quality_gate",
            "timestamp": "2025-12-25T10:30:18Z",
            "session_id": "abc123",
            "gate_number": 1,
            "gate_name": "Syntax",
            "status": "passed",
            "issues": 0,
            "duration_ms": 320
        }
    """

    type: Literal["quality_gate"] = "quality_gate"
    gate_number: int = Field(..., ge=1, le=4, description="Gate number (1-4)")
    gate_name: str = Field(..., description="Gate name (Syntax, Security, Context, Tests)")
    status: Literal["passed", "failed", "skipped"] = Field(..., description="Gate result")
    issues: int = Field(..., ge=0, description="Number of issues found")
    duration_ms: int = Field(..., ge=0, description="Gate execution time in milliseconds")


# =========================================================================
# Completion Events
# =========================================================================


class CompletedEvent(StreamEvent):
    """
    Event: Generation completed.
    Sent when all files are generated.

    Example:
        {
            "type": "completed",
            "timestamp": "2025-12-25T10:30:30Z",
            "session_id": "abc123",
            "total_files": 12,
            "total_lines": 450,
            "duration_ms": 30000,
            "success": true
        }
    """

    type: Literal["completed"] = "completed"
    total_files: int = Field(..., ge=0, description="Total files generated")
    total_lines: int = Field(..., ge=0, description="Total lines of code")
    duration_ms: int = Field(..., ge=0, description="Total generation time in milliseconds")
    success: bool = Field(..., description="Overall generation success")


class ErrorEvent(StreamEvent):
    """
    Event: Error occurred.
    Sent when an error occurs during generation.

    Example:
        {
            "type": "error",
            "timestamp": "2025-12-25T10:30:25Z",
            "session_id": "abc123",
            "message": "Ollama connection timeout",
            "recovery_id": "abc123"
        }
    """

    type: Literal["error"] = "error"
    message: str = Field(..., description="Error message for display")
    recovery_id: Optional[str] = Field(
        None, description="Session ID for partial recovery (if available)"
    )


# =========================================================================
# Union Type for All Events
# =========================================================================

CodegenStreamEvent = Union[
    StartedEvent,
    FileGeneratingEvent,
    FileGeneratedEvent,
    QualityStartedEvent,
    QualityGateEvent,
    CompletedEvent,
    ErrorEvent,
]


# =========================================================================
# Request/Response Models
# =========================================================================


class StreamGenerateRequest(BaseModel):
    """
    Request to start streaming code generation.

    Example:
        {
            "app_blueprint": {
                "app_name": "restaurant_management",
                "domain": "Restaurant Management"
            },
            "language": "python",
            "framework": "fastapi"
        }
    """

    app_blueprint: dict = Field(..., description="Application blueprint from onboarding")
    language: str = Field(default="python", description="Target programming language")
    framework: str = Field(default="fastapi", description="Target framework")


class RecoveryResponse(BaseModel):
    """
    Response for session recovery endpoint.

    Example:
        {
            "session_id": "abc123",
            "files": {"app/main.py": "content..."},
            "partial": true,
            "recovered_at": "2025-12-25T10:35:00Z"
        }
    """

    session_id: str = Field(..., description="Session ID that was recovered")
    files: dict = Field(..., description="Map of path -> content for recovered files")
    partial: bool = Field(..., description="True if only partial results available")
    recovered_at: datetime = Field(
        default_factory=datetime.utcnow, description="Recovery timestamp"
    )
