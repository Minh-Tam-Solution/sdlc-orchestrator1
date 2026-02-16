"""
MCP Client Service — Sprint 174.

Manages connections to MCP (Model Context Protocol) servers for AI agent
tool integration. Uses AsyncExitStack for proper lifecycle management
of multiple concurrent server connections.

Two Transport Modes:
- stdio: Launches MCP server as subprocess, communicates via stdin/stdout
- SSE: Connects to remote MCP server via Server-Sent Events over HTTP

Source: Anthropic agents/ quickstart (AsyncExitStack pattern)
Framework: SDLC 6.0.5 (11-AUTONOMOUS-CODEGEN-PATTERNS.md, Section 2)
Sprint: 174 — Anthropic Best Practices Integration
ADR: ADR-054-Anthropic-Claude-Code-Best-Practices.md

Usage:
    async with MCPClientService() as mcp:
        await mcp.connect_stdio("filesystem", ["npx", "@mcp/filesystem"])
        await mcp.connect_sse("remote-tools", "http://localhost:8080/sse")
        tools = mcp.get_all_tools()

Author: Sprint 174 Team
Date: February 2026
Status: ACTIVE
"""

import asyncio
import json
import logging
import os
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class MCPServerConfig:
    """Configuration for a single MCP server connection."""

    name: str
    transport: str  # "stdio" or "sse"
    command: Optional[List[str]] = None  # For stdio transport
    url: Optional[str] = None  # For SSE transport
    env: Optional[Dict[str, str]] = None
    timeout: int = 30


@dataclass
class MCPTool:
    """Represents a tool exposed by an MCP server."""

    name: str
    description: str
    input_schema: Dict[str, Any]
    server_name: str


@dataclass
class MCPServerConnection:
    """Active connection to an MCP server."""

    config: MCPServerConfig
    process: Optional[asyncio.subprocess.Process] = None
    tools: List[MCPTool] = field(default_factory=list)
    connected: bool = False
    reader: Optional[asyncio.StreamReader] = None
    writer: Optional[asyncio.StreamWriter] = None


class MCPClientService:
    """
    AsyncExitStack-based MCP client for managing server connections.

    Follows Anthropic agents/ quickstart pattern for lifecycle management.
    Each server connection is registered with the exit stack for proper
    cleanup on shutdown or error.

    Supports two transport modes:
    - stdio: Local subprocess servers (npm packages, Python scripts)
    - SSE: Remote HTTP servers (Server-Sent Events protocol)

    Usage:
        # As async context manager (recommended)
        async with MCPClientService() as mcp:
            await mcp.connect_stdio("fs", ["npx", "@mcp/filesystem", "/tmp"])
            tools = mcp.get_all_tools()

        # Manual lifecycle management
        mcp = MCPClientService()
        await mcp.start()
        try:
            await mcp.connect_stdio("fs", ["npx", "@mcp/filesystem"])
        finally:
            await mcp.stop()
    """

    def __init__(self) -> None:
        self._exit_stack: Optional[AsyncExitStack] = None
        self._connections: Dict[str, MCPServerConnection] = {}
        self._started = False

    async def __aenter__(self) -> "MCPClientService":
        await self.start()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.stop()

    async def start(self) -> None:
        """Initialize the exit stack for managing server lifecycles."""
        if self._started:
            return
        self._exit_stack = AsyncExitStack()
        await self._exit_stack.__aenter__()
        self._started = True
        logger.info("MCP client service started")

    async def stop(self) -> None:
        """Shut down all server connections via exit stack cleanup."""
        if not self._started or not self._exit_stack:
            return

        try:
            await self._exit_stack.__aexit__(None, None, None)
        except Exception as e:
            logger.warning(f"Error during MCP client shutdown: {e}")

        self._connections.clear()
        self._exit_stack = None
        self._started = False
        logger.info("MCP client service stopped")

    async def connect_stdio(
        self,
        name: str,
        command: List[str],
        env: Optional[Dict[str, str]] = None,
        timeout: int = 30,
    ) -> MCPServerConnection:
        """
        Connect to an MCP server via stdio transport.

        Launches the server as a subprocess and communicates via
        stdin/stdout using the MCP JSON-RPC protocol.

        Args:
            name: Unique server name for identification
            command: Command to launch the server (e.g., ["npx", "@mcp/fs"])
            env: Additional environment variables for the subprocess
            timeout: Connection timeout in seconds

        Returns:
            MCPServerConnection with available tools

        Raises:
            ConnectionError: If server fails to start or initialize
        """
        if not self._started:
            raise RuntimeError("MCPClientService not started. Use 'async with' or call start().")

        if name in self._connections:
            logger.warning(f"Server '{name}' already connected, disconnecting first")
            await self.disconnect(name)

        config = MCPServerConfig(
            name=name,
            transport="stdio",
            command=command,
            env=env,
            timeout=timeout,
        )

        # Merge environment variables
        process_env = os.environ.copy()
        if env:
            process_env.update(env)

        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=process_env,
            )

            # Register cleanup with exit stack
            async def cleanup_process() -> None:
                if process.returncode is None:
                    process.terminate()
                    try:
                        await asyncio.wait_for(process.wait(), timeout=5)
                    except asyncio.TimeoutError:
                        process.kill()
                        await process.wait()
                    logger.info(f"MCP server '{name}' (stdio) terminated")

            self._exit_stack.push_async_callback(cleanup_process)  # type: ignore[union-attr]

            conn = MCPServerConnection(
                config=config,
                process=process,
                connected=True,
            )

            # Initialize MCP session — send initialize request
            tools = await self._initialize_stdio_session(conn, timeout)
            conn.tools = tools

            self._connections[name] = conn
            logger.info(
                f"MCP server '{name}' (stdio) connected: "
                f"{len(tools)} tools available"
            )
            return conn

        except FileNotFoundError:
            raise ConnectionError(
                f"MCP server command not found: {command[0]}. "
                f"Ensure the command is installed and in PATH."
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MCP server '{name}': {e}")

    async def connect_sse(
        self,
        name: str,
        url: str,
        timeout: int = 30,
    ) -> MCPServerConnection:
        """
        Connect to an MCP server via SSE (Server-Sent Events) transport.

        Connects to a remote HTTP server that exposes tools via the
        MCP protocol over Server-Sent Events.

        Args:
            name: Unique server name for identification
            url: SSE endpoint URL (e.g., "http://localhost:8080/sse")
            timeout: Connection timeout in seconds

        Returns:
            MCPServerConnection with available tools

        Raises:
            ConnectionError: If server is unreachable or fails to initialize
        """
        if not self._started:
            raise RuntimeError("MCPClientService not started. Use 'async with' or call start().")

        if name in self._connections:
            logger.warning(f"Server '{name}' already connected, disconnecting first")
            await self.disconnect(name)

        config = MCPServerConfig(
            name=name,
            transport="sse",
            url=url,
            timeout=timeout,
        )

        try:
            import httpx

            client = httpx.AsyncClient(timeout=timeout)

            # Register cleanup with exit stack
            async def cleanup_sse() -> None:
                await client.aclose()
                logger.info(f"MCP server '{name}' (SSE) disconnected")

            self._exit_stack.push_async_callback(cleanup_sse)  # type: ignore[union-attr]

            # Test connectivity and fetch tools list
            response = await client.get(url.rstrip("/").replace("/sse", "/tools"))
            response.raise_for_status()

            tools_data = response.json()
            tools = [
                MCPTool(
                    name=t["name"],
                    description=t.get("description", ""),
                    input_schema=t.get("inputSchema", {}),
                    server_name=name,
                )
                for t in tools_data.get("tools", [])
            ]

            conn = MCPServerConnection(
                config=config,
                connected=True,
                tools=tools,
            )

            self._connections[name] = conn
            logger.info(
                f"MCP server '{name}' (SSE) connected at {url}: "
                f"{len(tools)} tools available"
            )
            return conn

        except ImportError:
            raise ConnectionError(
                "httpx package required for SSE transport. "
                "Install with: pip install httpx"
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MCP server '{name}' at {url}: {e}")

    async def disconnect(self, name: str) -> None:
        """Disconnect a specific MCP server by name."""
        conn = self._connections.pop(name, None)
        if conn and conn.process and conn.process.returncode is None:
            conn.process.terminate()
            try:
                await asyncio.wait_for(conn.process.wait(), timeout=5)
            except asyncio.TimeoutError:
                conn.process.kill()
        conn_transport = conn.config.transport if conn else "unknown"
        logger.info(f"MCP server '{name}' ({conn_transport}) disconnected")

    def get_all_tools(self) -> List[MCPTool]:
        """Get all tools from all connected MCP servers."""
        tools: List[MCPTool] = []
        for conn in self._connections.values():
            if conn.connected:
                tools.extend(conn.tools)
        return tools

    def get_tools_for_server(self, name: str) -> List[MCPTool]:
        """Get tools from a specific MCP server."""
        conn = self._connections.get(name)
        if conn and conn.connected:
            return conn.tools
        return []

    def get_connection_status(self) -> Dict[str, Any]:
        """Get status of all MCP server connections."""
        return {
            "started": self._started,
            "server_count": len(self._connections),
            "total_tools": len(self.get_all_tools()),
            "servers": {
                name: {
                    "transport": conn.config.transport,
                    "connected": conn.connected,
                    "tool_count": len(conn.tools),
                    "tools": [t.name for t in conn.tools],
                    "url": conn.config.url,
                    "command": conn.config.command,
                }
                for name, conn in self._connections.items()
            },
        }

    async def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> Any:
        """
        Call a tool on the appropriate MCP server.

        Finds the server that exposes the tool and dispatches the call.

        Args:
            tool_name: Name of the tool to call
            arguments: Tool input arguments

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool is not found on any server
            RuntimeError: If tool call fails
        """
        # Find the server that has this tool
        for conn in self._connections.values():
            for tool in conn.tools:
                if tool.name == tool_name:
                    if conn.config.transport == "stdio":
                        return await self._call_stdio_tool(conn, tool_name, arguments)
                    elif conn.config.transport == "sse":
                        return await self._call_sse_tool(conn, tool_name, arguments)

        available = [t.name for t in self.get_all_tools()]
        raise ValueError(
            f"Tool '{tool_name}' not found. "
            f"Available tools: {available}"
        )

    async def _initialize_stdio_session(
        self,
        conn: MCPServerConnection,
        timeout: int,
    ) -> List[MCPTool]:
        """Send MCP initialize request and list tools via stdio."""
        if not conn.process or not conn.process.stdin or not conn.process.stdout:
            return []

        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "sdlc-orchestrator",
                    "version": "1.0.0",
                },
            },
        }

        try:
            conn.process.stdin.write(
                (json.dumps(init_request) + "\n").encode()
            )
            await conn.process.stdin.drain()

            # Read initialize response
            raw = await asyncio.wait_for(
                conn.process.stdout.readline(),
                timeout=timeout,
            )
            init_response = json.loads(raw.decode().strip())

            # Send initialized notification
            initialized = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
            }
            conn.process.stdin.write(
                (json.dumps(initialized) + "\n").encode()
            )
            await conn.process.stdin.drain()

            # List tools
            list_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
            }
            conn.process.stdin.write(
                (json.dumps(list_request) + "\n").encode()
            )
            await conn.process.stdin.drain()

            raw = await asyncio.wait_for(
                conn.process.stdout.readline(),
                timeout=timeout,
            )
            tools_response = json.loads(raw.decode().strip())

            tools_data = tools_response.get("result", {}).get("tools", [])
            return [
                MCPTool(
                    name=t["name"],
                    description=t.get("description", ""),
                    input_schema=t.get("inputSchema", {}),
                    server_name=conn.config.name,
                )
                for t in tools_data
            ]

        except asyncio.TimeoutError:
            logger.warning(
                f"Timeout initializing MCP server '{conn.config.name}'"
            )
            return []
        except Exception as e:
            logger.warning(
                f"Failed to initialize MCP server '{conn.config.name}': {e}"
            )
            return []

    async def _call_stdio_tool(
        self,
        conn: MCPServerConnection,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> Any:
        """Call a tool via stdio transport."""
        if not conn.process or not conn.process.stdin or not conn.process.stdout:
            raise RuntimeError(f"Server '{conn.config.name}' process not available")

        request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        }

        conn.process.stdin.write(
            (json.dumps(request) + "\n").encode()
        )
        await conn.process.stdin.drain()

        raw = await asyncio.wait_for(
            conn.process.stdout.readline(),
            timeout=conn.config.timeout,
        )
        response = json.loads(raw.decode().strip())

        if "error" in response:
            raise RuntimeError(
                f"Tool call failed: {response['error'].get('message', 'Unknown error')}"
            )

        return response.get("result", {})

    async def _call_sse_tool(
        self,
        conn: MCPServerConnection,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> Any:
        """Call a tool via SSE transport."""
        import httpx

        if not conn.config.url:
            raise RuntimeError(f"Server '{conn.config.name}' has no URL configured")

        base_url = conn.config.url.rstrip("/").replace("/sse", "")

        async with httpx.AsyncClient(timeout=conn.config.timeout) as client:
            response = await client.post(
                f"{base_url}/tools/call",
                json={
                    "name": tool_name,
                    "arguments": arguments,
                },
            )
            response.raise_for_status()
            return response.json()


# Global singleton
_mcp_client: Optional[MCPClientService] = None


def get_mcp_client() -> MCPClientService:
    """Get the global MCP client instance."""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClientService()
    return _mcp_client
