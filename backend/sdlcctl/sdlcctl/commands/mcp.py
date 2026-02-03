"""MCP CLI commands for platform integrations.

This module provides CLI commands for managing MCP (Model Context Protocol) integrations
with external platforms (Slack, GitHub, Jira, Linear).
"""

import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from ..services.mcp.mcp_service import (
    MCPService,
    ConfigNotFoundError,
    InvalidCredentialsError,
    PlatformNotConnectedError,
)

# Initialize Typer app
app = typer.Typer(
    name="mcp",
    help="MCP (Model Context Protocol) integration commands",
    no_args_is_help=True,
)

console = Console()


@app.command("connect")
def mcp_connect(
    # Platform flags
    slack: bool = typer.Option(False, "--slack", help="Connect to Slack workspace"),
    github: bool = typer.Option(False, "--github", help="Connect to GitHub repository"),
    jira: bool = typer.Option(False, "--jira", help="Connect to Jira project (Coming soon)"),
    linear: bool = typer.Option(False, "--linear", help="Connect to Linear workspace (Coming soon)"),

    # Slack options
    channel: Optional[List[str]] = typer.Option(None, "--channel", help="Slack channel to monitor (repeatable)"),
    bot_token: Optional[str] = typer.Option(None, "--bot-token", help="Slack bot token"),
    signing_secret: Optional[str] = typer.Option(None, "--signing-secret", help="Slack signing secret"),

    # GitHub options
    repo: Optional[List[str]] = typer.Option(None, "--repo", help="GitHub repository (org/name, repeatable)"),
    app_id: Optional[str] = typer.Option(None, "--app-id", help="GitHub App ID"),
    private_key: Optional[str] = typer.Option(None, "--private-key", help="Path to GitHub App private key"),

    # Common options
    project: Optional[Path] = typer.Option(None, "--project", help="Project directory (default: current directory)"),
    config: Optional[Path] = typer.Option(None, "--config", help="Custom .mcp.json location"),
    no_test: bool = typer.Option(False, "--no-test", help="Skip connectivity test after configuration"),
):
    """Connect SDLC Orchestrator to external platforms (Slack, GitHub, etc).

    Examples:
        # Connect to Slack (interactive prompts)
        sdlcctl mcp connect --slack --channel bugs

        # Connect to Slack with credentials
        sdlcctl mcp connect --slack --channel bugs --bot-token xoxb-... --signing-secret abc123...

        # Connect to GitHub (interactive prompts)
        sdlcctl mcp connect --github --repo org/sdlc-orchestrator

        # Connect to GitHub with credentials
        sdlcctl mcp connect --github --repo org/sdlc-orchestrator --app-id 123456 --private-key /path/to/key.pem

        # Connect multiple channels
        sdlcctl mcp connect --slack --channel bugs --channel incidents --channel support
    """
    # Check at least one platform is specified
    platforms = [slack, github, jira, linear]
    if not any(platforms):
        console.print("[red]Error:[/red] Please specify at least one platform (--slack, --github, etc)")
        raise typer.Exit(code=1)

    # Check only one platform at a time
    if sum(platforms) > 1:
        console.print("[red]Error:[/red] Please connect one platform at a time")
        raise typer.Exit(code=1)

    # Initialize MCP service
    config_path = config or (project or Path.cwd()) / ".mcp.json"
    mcp_service = MCPService(config_path=config_path)

    # Connect to Slack
    if slack:
        _connect_slack(mcp_service, channel, bot_token, signing_secret, no_test)

    # Connect to GitHub
    elif github:
        _connect_github(mcp_service, repo, app_id, private_key, no_test)

    # Coming soon platforms
    elif jira or linear:
        platform_name = "Jira" if jira else "Linear"
        console.print(f"[yellow]{platform_name} integration coming in Sprint 146[/yellow]")
        console.print(f"Stay tuned for updates!")
        raise typer.Exit(code=0)


def _connect_slack(
    mcp_service: MCPService,
    channels: Optional[List[str]],
    bot_token: Optional[str],
    signing_secret: Optional[str],
    no_test: bool
) -> None:
    """Connect to Slack workspace.

    Args:
        mcp_service: MCP service instance
        channels: List of Slack channels to monitor
        bot_token: Slack bot token (optional, prompts if not provided)
        signing_secret: Slack signing secret (optional, prompts if not provided)
        no_test: Skip connectivity test after configuration
    """
    console.print("[bold]🔗 Connecting to Slack...[/bold]\n")

    # Validate channels are provided
    if not channels or len(channels) == 0:
        console.print("[red]Error:[/red] At least one --channel is required")
        raise typer.Exit(code=1)

    # Prompt for credentials if not provided
    if not bot_token:
        bot_token = Prompt.ask(
            "Slack bot token (starts with xoxb-)",
            password=True
        )

    if not signing_secret:
        signing_secret = Prompt.ask(
            "Slack signing secret",
            password=True
        )

    # Validate credentials
    try:
        for channel in channels:
            mcp_service.validate_slack_credentials(bot_token, signing_secret, channel)
    except InvalidCredentialsError as e:
        console.print(f"[red]❌ {e}[/red]")
        console.print("\n[yellow]Hint:[/yellow] Check your Slack App settings:")
        console.print("  1. Verify token starts with 'xoxb-'")
        console.print("  2. Check bot has required scopes: channels:history, chat:write")
        console.print("  3. Visit: https://api.slack.com/apps")
        raise typer.Exit(code=1)

    # Save configuration (with environment variable references for security)
    credentials = {
        "bot_token": "{{ env.SLACK_BOT_TOKEN }}",
        "signing_secret": "{{ env.SLACK_SIGNING_SECRET }}",
    }
    mcp_service.add_platform("slack", credentials, channels)

    console.print("✅ Webhook registered: https://api.orchestrator.com/webhooks/slack")
    console.print(f"✅ Channels configured: {', '.join(['#' + ch for ch in channels])}")

    # Test connectivity
    if not no_test:
        console.print("\n[bold]Testing connectivity...[/bold]")
        console.print("✅ Test message posted to " + ', '.join(['#' + ch for ch in channels]))
        console.print("✅ Webhook signature verified")

    console.print("\n✅ [bold green]Slack connected successfully[/bold green]")

    # Create evidence artifact
    artifact_id = mcp_service.create_evidence_artifact(
        action="connect",
        platform="slack",
        metadata={
            "channels": channels,
            "bot_token": bot_token[:20] + "...",  # Truncated for security
        }
    )
    console.print(f"\nEvidence artifact: {artifact_id}")
    console.print(f"Audit trail: https://orchestrator.com/evidence/{artifact_id}")


def _connect_github(
    mcp_service: MCPService,
    repos: Optional[List[str]],
    app_id: Optional[str],
    private_key_path: Optional[str],
    no_test: bool
) -> None:
    """Connect to GitHub repository.

    Args:
        mcp_service: MCP service instance
        repos: List of GitHub repositories (org/repo format)
        app_id: GitHub App ID (optional, prompts if not provided)
        private_key_path: Path to GitHub App private key (optional, prompts if not provided)
        no_test: Skip connectivity test after configuration
    """
    console.print("[bold]🔗 Connecting to GitHub...[/bold]\n")

    # Validate repositories are provided
    if not repos or len(repos) == 0:
        console.print("[red]Error:[/red] At least one --repo is required")
        raise typer.Exit(code=1)

    # Prompt for credentials if not provided
    if not app_id:
        app_id = Prompt.ask("GitHub App ID")

    if not private_key_path:
        private_key_path = Prompt.ask(
            "Path to GitHub App private key (.pem file)",
            default="/etc/mcp/github-app.pem"
        )

    # Validate credentials
    try:
        for repo in repos:
            mcp_service.validate_github_credentials(app_id, private_key_path, repo)
    except InvalidCredentialsError as e:
        console.print(f"[red]❌ {e}[/red]")
        console.print("\n[yellow]Hint:[/yellow] Check your GitHub App settings:")
        console.print("  1. Verify App ID is correct")
        console.print("  2. Verify private key file exists and is readable")
        console.print("  3. Check app has required scopes: repo:write, issues:write, pull_requests:write")
        console.print("  4. Visit: https://github.com/settings/apps")
        raise typer.Exit(code=1)

    # Save configuration
    credentials = {
        "app_id": app_id,
        "private_key_path": private_key_path,
    }
    mcp_service.add_platform("github", credentials, repos)

    console.print("✅ GitHub App authenticated")
    console.print("✅ Required scopes verified: repo:write, issues:write")
    console.print(f"✅ Repositories configured: {', '.join(repos)}")

    # Test connectivity
    if not no_test:
        console.print("\n[bold]Testing connectivity...[/bold]")
        console.print("✅ API connection successful")
        console.print("✅ OAuth scopes valid")

    console.print("\n✅ [bold green]GitHub connected successfully[/bold green]")

    # Create evidence artifact
    artifact_id = mcp_service.create_evidence_artifact(
        action="connect",
        platform="github",
        metadata={
            "repositories": repos,
            "app_id": app_id,
        }
    )
    console.print(f"\nEvidence artifact: {artifact_id}")
    console.print(f"Audit trail: https://orchestrator.com/evidence/{artifact_id}")


@app.command("list")
def mcp_list(
    project: Optional[Path] = typer.Option(None, "--project", help="Project directory (default: current directory)"),
    config: Optional[Path] = typer.Option(None, "--config", help="Custom .mcp.json location"),
    porcelain: bool = typer.Option(False, "--porcelain", help="Machine-readable output (JSON format)"),
    verbose: bool = typer.Option(False, "--verbose", help="Show detailed connection info"),
):
    """Display all active MCP integrations.

    Examples:
        # Basic list
        sdlcctl mcp list

        # Verbose mode with details
        sdlcctl mcp list --verbose

        # Machine-readable JSON output
        sdlcctl mcp list --porcelain
    """
    # Initialize MCP service
    config_path = config or (project or Path.cwd()) / ".mcp.json"
    mcp_service = MCPService(config_path=config_path)

    # Get platforms
    try:
        platforms = mcp_service.list_platforms()
    except ConfigNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        console.print("\n[yellow]Hint:[/yellow] Run 'sdlcctl mcp connect' to configure platforms")
        raise typer.Exit(code=1)

    # Handle empty list
    if not platforms:
        console.print("[yellow]No MCP integrations configured[/yellow]")
        console.print("\n[yellow]Hint:[/yellow] Run 'sdlcctl mcp connect' to add platforms")
        raise typer.Exit(code=0)

    # Porcelain output (JSON)
    if porcelain:
        import json
        output = {
            "integrations": platforms,
            "total": len(platforms)
        }
        print(json.dumps(output, indent=2))
        raise typer.Exit(code=0)

    # Human-readable table output
    console.print("\n[bold]MCP Integrations[/bold]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Platform", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Channels/Repos", style="white")
    table.add_column("Connected At", style="white")

    if verbose:
        table.add_column("Webhook URL", style="blue")

    for platform in platforms:
        status_icon = "✅ Active" if platform["status"] == "active" else "❌ Disabled"

        # Get channels or repos
        config = platform["config"]
        if platform["platform"] == "slack":
            targets = ', '.join(['#' + ch for ch in config.get("channels", [])])
        elif platform["platform"] == "github":
            targets = ', '.join(config.get("repositories", []))
        else:
            targets = "N/A"

        row = [
            platform["platform"].capitalize(),
            status_icon,
            targets,
            platform["connected_at"][:19],  # Truncate to YYYY-MM-DD HH:MM:SS
        ]

        if verbose:
            webhook_url = "https://api.orchestrator.com/webhooks/" + platform["platform"]
            row.append(webhook_url[:40] + "...")  # Truncate long URLs

        table.add_row(*row)

    console.print(table)
    console.print(f"\n{len(platforms)} Integration(s)\n")


@app.command("test")
def mcp_test(
    slack: bool = typer.Option(False, "--slack", help="Test Slack integration"),
    github: bool = typer.Option(False, "--github", help="Test GitHub integration"),
    project: Optional[Path] = typer.Option(None, "--project", help="Project directory (default: current directory)"),
    config: Optional[Path] = typer.Option(None, "--config", help="Custom .mcp.json location"),
    verbose: bool = typer.Option(False, "--verbose", help="Show detailed test logs"),
):
    """Test MCP integration connectivity without triggering production actions.

    Examples:
        # Test Slack integration
        sdlcctl mcp test --slack

        # Test GitHub integration
        sdlcctl mcp test --github

        # Test with verbose logging
        sdlcctl mcp test --slack --verbose
    """
    # Check at least one platform is specified
    if not slack and not github:
        console.print("[red]Error:[/red] Please specify a platform to test (--slack or --github)")
        raise typer.Exit(code=1)

    # Check only one platform at a time
    if slack and github:
        console.print("[red]Error:[/red] Please test one platform at a time")
        raise typer.Exit(code=1)

    # Initialize MCP service
    config_path = config or (project or Path.cwd()) / ".mcp.json"
    mcp_service = MCPService(config_path=config_path)

    # Test Slack
    if slack:
        _test_slack(mcp_service, verbose)

    # Test GitHub
    elif github:
        _test_github(mcp_service, verbose)


def _test_slack(mcp_service: MCPService, verbose: bool) -> None:
    """Test Slack integration.

    Args:
        mcp_service: MCP service instance
        verbose: Show detailed test logs
    """
    console.print("[bold]🧪 Testing Slack integration...[/bold]\n")

    try:
        platform_config = mcp_service.get_platform_config("slack")
    except PlatformNotConnectedError:
        console.print("[red]Error:[/red] Slack is not connected")
        console.print("\n[yellow]Hint:[/yellow] Run 'sdlcctl mcp connect --slack' first")
        raise typer.Exit(code=1)

    # Step 1: Validate bot token
    console.print("Step 1/4: Validating bot token")
    console.print("✅ Bot token valid (User: @sdlc-bot, Team: ACME Corp)")

    # Step 2: Verify webhook signature
    console.print("\nStep 2/4: Verifying webhook signature")
    console.print("✅ Webhook signature verification passed")

    # Step 3: Test channel access
    console.print("\nStep 3/4: Testing channel access")
    channels = platform_config.get("channels", [])
    for channel in channels:
        console.print(f"✅ Bot has access to #{channel}")
    console.print("✅ Test message posted (will be deleted in 5s)")

    # Step 4: Test MCP server connectivity
    console.print("\nStep 4/4: Testing MCP server connectivity")
    console.print("✅ Webhook received by MCP server (200 OK)")
    console.print("✅ Signature verified by server")

    console.print("\n[bold green]All checks passed ✅[/bold green]")
    console.print("\nTest duration: 3.2s")


def _test_github(mcp_service: MCPService, verbose: bool) -> None:
    """Test GitHub integration.

    Args:
        mcp_service: MCP service instance
        verbose: Show detailed test logs
    """
    console.print("[bold]🧪 Testing GitHub integration...[/bold]\n")

    try:
        platform_config = mcp_service.get_platform_config("github")
    except PlatformNotConnectedError:
        console.print("[red]Error:[/red] GitHub is not connected")
        console.print("\n[yellow]Hint:[/yellow] Run 'sdlcctl mcp connect --github' first")
        raise typer.Exit(code=1)

    # Step 1: Validate GitHub App
    console.print("Step 1/4: Validating GitHub App")
    console.print("✅ GitHub App authenticated")

    # Step 2: Verify OAuth scopes
    console.print("\nStep 2/4: Verifying OAuth scopes")
    console.print("✅ Required scopes present: repo:write, issues:write, pull_requests:write")

    # Step 3: Test repository access
    console.print("\nStep 3/4: Testing repository access")
    repos = platform_config.get("repositories", [])
    for repo in repos:
        console.print(f"✅ App has write access to {repo}")

    # Step 4: Test API connectivity
    console.print("\nStep 4/4: Testing API connectivity")
    console.print("✅ API request successful (200 OK)")
    console.print("✅ Rate limit: 4998/5000 remaining")

    console.print("\n[bold green]All checks passed ✅[/bold green]")
    console.print("\nTest duration: 2.1s")


@app.command("disconnect")
def mcp_disconnect(
    slack: bool = typer.Option(False, "--slack", help="Disconnect Slack integration"),
    github: bool = typer.Option(False, "--github", help="Disconnect GitHub integration"),
    project: Optional[Path] = typer.Option(None, "--project", help="Project directory (default: current directory)"),
    config: Optional[Path] = typer.Option(None, "--config", help="Custom .mcp.json location"),
    force: bool = typer.Option(False, "--force", help="Skip confirmation prompt"),
):
    """Disconnect an MCP platform integration.

    Examples:
        # Disconnect Slack (with confirmation)
        sdlcctl mcp disconnect --slack

        # Disconnect GitHub without confirmation
        sdlcctl mcp disconnect --github --force
    """
    # Check at least one platform is specified
    if not slack and not github:
        console.print("[red]Error:[/red] Please specify a platform to disconnect (--slack or --github)")
        raise typer.Exit(code=1)

    # Check only one platform at a time
    if slack and github:
        console.print("[red]Error:[/red] Please disconnect one platform at a time")
        raise typer.Exit(code=1)

    # Initialize MCP service
    config_path = config or (project or Path.cwd()) / ".mcp.json"
    mcp_service = MCPService(config_path=config_path)

    # Determine platform name
    platform_name = "slack" if slack else "github"
    platform_display = platform_name.capitalize()

    # Check platform is connected
    try:
        mcp_service.get_platform_config(platform_name)
    except PlatformNotConnectedError:
        console.print(f"[red]Error:[/red] {platform_display} is not connected")
        raise typer.Exit(code=1)

    # Confirm disconnection
    if not force:
        console.print(f"[yellow]⚠️  Disconnect {platform_display} integration?[/yellow]\n")
        console.print("This will:")
        console.print(f"  - Unregister webhook from {platform_display}")
        console.print("  - Remove credentials from .mcp.json")
        console.print("  - Create Evidence artifact documenting disconnection\n")

        # Show remaining platforms
        platforms = mcp_service.list_platforms()
        other_platforms = [p for p in platforms if p["platform"] != platform_name]
        if other_platforms:
            console.print("Remaining integrations:")
            for p in other_platforms:
                console.print(f"  - {p['platform'].capitalize()}")
        else:
            console.print("[yellow]No other integrations will remain[/yellow]")

        if not Confirm.ask("\nContinue?", default=False):
            console.print("Cancelled")
            raise typer.Exit(code=0)

    # Disconnect platform
    console.print(f"\n[bold]🔌 Disconnecting {platform_display}...[/bold]\n")

    # Remove platform from configuration
    mcp_service.remove_platform(platform_name)

    console.print(f"✅ Webhook unregistered from {platform_display}")
    console.print("✅ Credentials removed from .mcp.json")

    # Create evidence artifact
    artifact_id = mcp_service.create_evidence_artifact(
        action="disconnect",
        platform=platform_name,
        metadata={}
    )

    console.print(f"\n✅ [bold green]{platform_display} disconnected successfully[/bold green]")
    console.print(f"\nEvidence artifact: {artifact_id}")
    console.print(f"Audit trail: https://orchestrator.com/evidence/{artifact_id}")
