"""
=========================================================================
Context Cache Commands - CLI Interface for SDLC Context Cache
SDLC Orchestrator - Sprint 174 (Anthropic Best Practices)

Version: 1.0.0
Date: February 2026
Status: ACTIVE - Sprint 174 Implementation
Authority: CTO Approved
Reference: ADR-054-Anthropic-Claude-Code-Best-Practices.md
           10-CLAUDE-MD-STANDARD.md (Section 3.2 Progressive Disclosure)

Purpose:
- Manage the two-layer context cache for AI codegen requests
- Commands: stats, clear, warm
- L1 Cache: Redis (assembled framework context, TTL 1 hour)
- L2 Cache: Anthropic cache_control headers (provider-side, TTL 5 min)

Target Metrics:
- Cache hit rate: >85%
- Cost per request: <$0.002 (cached) vs $0.016 (uncached)
- Context assembly time: <50ms (cached) vs 500ms (uncached)

Zero Mock Policy: Real Redis calls via async client
=========================================================================
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Optional

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

app = typer.Typer(
    name="cache",
    help="Context cache management for AI codegen (Sprint 174)",
    no_args_is_help=True,
)


def _get_project_root() -> str:
    """Resolve project root from env or cwd."""
    return os.environ.get(
        "SDLC_PROJECT_ROOT",
        str(Path.cwd()),
    )


@app.command("stats")
def stats_command(
    output_format: str = typer.Option(
        "text", "--format", "-f",
        help="Output format: text, json",
    ),
) -> None:
    """
    Show context cache statistics.

    Displays L1 (Redis) hit/miss rates, L2 (Anthropic) hint counts,
    and estimated cost savings.

    Example:
        sdlcctl cache stats
        sdlcctl cache stats --format json
    """
    try:
        from app.services.context_cache_service import get_context_cache
    except ImportError:
        console.print(
            "[red]Error:[/red] context_cache_service not available. "
            "Run from project root with backend in PYTHONPATH."
        )
        raise typer.Exit(1)

    cache = get_context_cache()
    stats = cache.get_stats()

    if output_format == "json":
        console.print_json(json.dumps(stats, indent=2))
        return

    # Build stats panel
    hit_rate = stats["hit_rate_percent"]
    hit_color = "green" if hit_rate >= 85 else "yellow" if hit_rate >= 50 else "red"

    info_lines = [
        f"[bold]L1 Cache (Redis):[/bold]",
        f"  Hits:    [green]{stats['l1_hits']}[/green]",
        f"  Misses:  [yellow]{stats['l1_misses']}[/yellow]",
        f"  Hit Rate: [{hit_color}]{hit_rate}%[/{hit_color}]"
        f" {'(target: >85%)' if hit_rate < 85 else ''}",
        f"",
        f"[bold]L2 Cache (Anthropic cache_control):[/bold]",
        f"  Hints Sent: {stats['l2_hints_sent']}",
        f"",
        f"[bold]Totals:[/bold]",
        f"  Requests:    {stats['total_requests']}",
        f"  Bytes Cached: {stats['total_bytes_cached']:,}",
        f"  Errors:      {stats['errors']}",
        f"  Cost Saved:  [green]${stats['total_cost_saved_usd']:.4f}[/green]",
    ]

    console.print(Panel(
        "\n".join(info_lines),
        title="[bold blue]Context Cache Statistics[/bold blue]",
        border_style="blue",
    ))

    if stats["total_requests"] == 0:
        console.print(
            "\n[dim]No requests yet. Cache stats populate "
            "after codegen requests.[/dim]"
        )


@app.command("clear")
def clear_command(
    confirm: bool = typer.Option(
        False, "--yes", "-y",
        help="Skip confirmation prompt",
    ),
    output_format: str = typer.Option(
        "text", "--format", "-f",
        help="Output format: text, json",
    ),
) -> None:
    """
    Clear all context cache entries from Redis.

    Clears L1 (Redis) cache. L2 (Anthropic) cache is managed by
    Anthropic and expires automatically (TTL 5 minutes).

    Example:
        sdlcctl cache clear
        sdlcctl cache clear --yes
    """
    if not confirm:
        confirm = typer.confirm(
            "Clear all context cache entries? "
            "This forces re-assembly on next codegen request."
        )
        if not confirm:
            console.print("[dim]Cancelled.[/dim]")
            raise typer.Exit(0)

    try:
        from app.services.context_cache_service import get_context_cache
    except ImportError:
        console.print(
            "[red]Error:[/red] context_cache_service not available. "
            "Run from project root with backend in PYTHONPATH."
        )
        raise typer.Exit(1)

    cache = get_context_cache()

    try:
        deleted = asyncio.run(cache.invalidate())
    except Exception as e:
        console.print(f"[red]Error:[/red] Cache clear failed: {e}")
        console.print("[dim]Check Redis connection (REDIS_URL env var).[/dim]")
        raise typer.Exit(1)

    if output_format == "json":
        console.print_json(json.dumps({"deleted": deleted}))
        return

    if deleted > 0:
        console.print(
            f"[green]Cleared {deleted} cache entries.[/green]"
        )
    else:
        console.print("[dim]No cache entries found to clear.[/dim]")

    console.print(
        "[dim]L2 (Anthropic) cache expires automatically (TTL 5 min).[/dim]"
    )


@app.command("warm")
def warm_command(
    project_root: Optional[str] = typer.Option(
        None, "--root", "-r",
        help="Project root path (default: cwd or SDLC_PROJECT_ROOT)",
    ),
    output_format: str = typer.Option(
        "text", "--format", "-f",
        help="Output format: text, json",
    ),
) -> None:
    """
    Pre-warm the context cache by assembling framework docs.

    Reads CLAUDE.md and framework documents, assembles context,
    and stores in Redis. Useful before batch codegen operations.

    Example:
        sdlcctl cache warm
        sdlcctl cache warm --root /path/to/project
    """
    effective_root = project_root or _get_project_root()

    try:
        from app.services.context_cache_service import get_context_cache
    except ImportError:
        console.print(
            "[red]Error:[/red] context_cache_service not available. "
            "Run from project root with backend in PYTHONPATH."
        )
        raise typer.Exit(1)

    cache = get_context_cache()

    with console.status("[bold blue]Assembling context...[/bold blue]"):
        try:
            context = asyncio.run(
                cache.get_or_assemble(project_root=effective_root)
            )
        except Exception as e:
            console.print(f"[red]Error:[/red] Context assembly failed: {e}")
            raise typer.Exit(1)

    if output_format == "json":
        console.print_json(json.dumps({
            "context_hash": context.context_hash,
            "source_files": context.source_files,
            "token_estimate": context.token_estimate,
            "size_bytes": context.size_bytes,
            "from_cache": context.from_cache,
        }, indent=2))
        return

    # Build summary
    table = Table(
        title="Context Cache Warm-Up",
        box=box.ROUNDED,
        show_header=True,
    )
    table.add_column("Property", style="cyan", width=20)
    table.add_column("Value", width=50)

    table.add_row("Project Root", effective_root)
    table.add_row("Context Hash", context.context_hash)
    table.add_row("Token Estimate", f"{context.token_estimate:,}")
    table.add_row("Size", f"{context.size_bytes:,} bytes")
    table.add_row(
        "Source",
        "L1 Cache (Redis)" if context.from_cache else "Fresh Assembly",
    )

    source_list = "\n".join(
        f"  {f}" for f in context.source_files
    ) if context.source_files else "  (no files found)"
    table.add_row("Files Loaded", source_list)

    console.print(table)

    if context.from_cache:
        console.print(
            "\n[green]Cache already warm.[/green] "
            "Context was served from Redis."
        )
    else:
        console.print(
            "\n[green]Cache warmed.[/green] "
            "Next codegen request will use cached context."
        )

    # Cost estimate
    tokens_m = context.token_estimate / 1_000_000
    uncached_cost = tokens_m * 3.00
    cached_cost = tokens_m * 0.30
    saving = uncached_cost - cached_cost
    console.print(
        f"\n[dim]Estimated cost per request: "
        f"${cached_cost:.4f} (cached) vs ${uncached_cost:.4f} (uncached) "
        f"= ${saving:.4f} saved[/dim]"
    )
