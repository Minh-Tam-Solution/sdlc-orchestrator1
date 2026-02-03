"""MCP (Model Context Protocol) integration services.

This package provides services for integrating SDLC Orchestrator with external platforms
(Slack, GitHub, Jira, Linear) for automated bug triage and AI-assisted workflows.
"""

from .mcp_service import MCPService

__all__ = ["MCPService"]
