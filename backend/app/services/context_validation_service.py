"""
=========================================================================
Context Validation Service - AGENTS.md Per-File Context Limits
SDLC Orchestrator - Sprint 103 (Context <60 Lines)

Version: 1.0.0
Date: January 23, 2026
Status: ACTIVE - Sprint 103 Implementation
Authority: Backend Lead + CTO Approved
Reference: docs/04-build/02-Sprint-Plans/SPRINT-103-DESIGN.md
Reference: SDLC Framework 5.2.0, Section 03-AI-GOVERNANCE

Purpose:
- Validate per-file context limits in AGENTS.md (<60 lines)
- Parse AGENTS.md to extract file-specific contexts
- Prevent token bloat in AI workflows
- Generate violation reports for GitHub checks

Why <60 lines per file context?
- Claude/GPT context window optimization
- Prevent "context creep" in agent orchestration
- Force developers to write concise summaries
- Faster agent startup (less reading overhead)

Zero Mock Policy: Production-ready context validation
=========================================================================
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

logger = logging.getLogger(__name__)


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class FileContext:
    """Represents a file context extracted from AGENTS.md."""
    file_path: str
    line_count: int
    content: str
    start_line: int  # Line number in AGENTS.md where context starts
    end_line: int  # Line number in AGENTS.md where context ends


@dataclass
class ContextValidation:
    """Complete context validation result."""
    total_files: int
    passed_files: int
    failed_files: int
    violations: list[FileContext]
    passed_contexts: list[FileContext]
    overall_passed: bool
    validated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def summary(self) -> str:
        """Get human-readable summary."""
        if self.overall_passed:
            return f"✅ All {self.total_files} file contexts are under 60 lines."
        return f"❌ {self.failed_files}/{self.total_files} file contexts exceed 60 lines."


@dataclass
class ContextValidationReport:
    """Full validation report with project context."""
    project_id: Optional[UUID]
    repo_full_name: Optional[str]
    branch: str
    agents_md_path: str
    validation: ContextValidation
    generated_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# Context Validation Service
# ============================================================================


class ContextValidationService:
    """
    Service for validating per-file context limits in AGENTS.md.

    SDLC 5.2.0 Requirement:
    > "Context descriptions MUST remain under 60 lines per file reference
    > to prevent token bloat in AI workflows."
    > — SDLC Framework 5.2.0, Section 03-AI-GOVERNANCE

    This service:
    1. Parses AGENTS.md to extract file-specific contexts
    2. Counts lines per file context (inside code blocks)
    3. Validates against 60-line limit
    4. Generates reports for GitHub checks and CLI

    Usage:
        service = ContextValidationService()
        validation = service.validate_local_agents_md("/path/to/AGENTS.md")
        if not validation.overall_passed:
            print(service.format_violation_report(validation))

    File Context Detection:
        Expected AGENTS.md format:
            ### File: backend/app/main.py
            Lines 1-50
            ```python
            ... (context code)
            ```

        Alternative formats also supported:
            ## backend/app/main.py
            ```python
            ...
            ```
    """

    # SDLC 5.2.0 Context Management Principle: <60 lines for optimal AI effectiveness
    MAX_CONTEXT_LINES = 60

    # Patterns to detect file references in AGENTS.md
    FILE_HEADER_PATTERNS = [
        # ### File: backend/app/main.py
        r'^###\s+File:\s+(.+)$',
        # ## backend/app/main.py
        r'^##\s+([^\s#]+\.[a-z]+)$',
        # **File**: backend/app/main.py
        r'^\*\*File\*\*:\s+(.+)$',
        # - File: backend/app/main.py
        r'^[-*]\s+File:\s+(.+)$',
        # ### `backend/app/main.py`
        r'^###\s+`([^`]+)`$',
    ]

    def __init__(self, github_service=None):
        """
        Initialize ContextValidationService.

        Args:
            github_service: Optional GitHub service for remote validation
        """
        self.github_service = github_service

    # =========================================================================
    # Validation Methods
    # =========================================================================

    def validate_content(self, content: str) -> ContextValidation:
        """
        Validate AGENTS.md content for per-file context limits.

        Args:
            content: AGENTS.md file content

        Returns:
            ContextValidation with violations and passed contexts
        """
        # Parse file contexts
        file_contexts = self._parse_file_contexts(content)

        # Validate each context
        violations = []
        passed = []

        for ctx in file_contexts:
            if ctx.line_count > self.MAX_CONTEXT_LINES:
                violations.append(ctx)
            else:
                passed.append(ctx)

        return ContextValidation(
            total_files=len(file_contexts),
            passed_files=len(passed),
            failed_files=len(violations),
            violations=violations,
            passed_contexts=passed,
            overall_passed=len(violations) == 0,
        )

    def validate_local_agents_md(
        self,
        file_path: str = "AGENTS.md",
    ) -> ContextValidation:
        """
        Validate local AGENTS.md file.

        Args:
            file_path: Path to AGENTS.md file

        Returns:
            ContextValidation result

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self.validate_content(content)

    async def validate_remote_agents_md(
        self,
        repo_full_name: str,
        branch: str = "main",
        agents_md_path: str = "AGENTS.md",
    ) -> ContextValidationReport:
        """
        Validate AGENTS.md from GitHub repository.

        Args:
            repo_full_name: Repository full name (owner/repo)
            branch: Git branch
            agents_md_path: Path to AGENTS.md in repository

        Returns:
            ContextValidationReport with full context

        Raises:
            ValueError: If GitHub service not configured
        """
        if not self.github_service:
            raise ValueError("GitHub service not configured for remote validation")

        # Fetch AGENTS.md from GitHub
        content = await self.github_service.get_file_content(
            repo_full_name,
            agents_md_path,
            branch,
        )

        validation = self.validate_content(content)

        return ContextValidationReport(
            project_id=None,
            repo_full_name=repo_full_name,
            branch=branch,
            agents_md_path=agents_md_path,
            validation=validation,
        )

    # =========================================================================
    # Parsing Methods
    # =========================================================================

    def _parse_file_contexts(self, content: str) -> list[FileContext]:
        """
        Parse AGENTS.md to extract file-specific contexts.

        Detection Strategy:
        1. Look for file header patterns (### File: xxx, ## xxx.py, etc.)
        2. Find associated code blocks (```...```)
        3. Count lines inside code blocks (excluding fence markers)

        Args:
            content: AGENTS.md content

        Returns:
            List of FileContext objects
        """
        file_contexts = []
        lines = content.split('\n')

        current_file = None
        current_context_lines = []
        current_start_line = 0
        in_code_block = False

        for line_num, line in enumerate(lines, start=1):
            # Check for file header patterns
            file_match = self._match_file_header(line)
            if file_match:
                # Save previous file context if exists
                if current_file and current_context_lines:
                    file_contexts.append(FileContext(
                        file_path=current_file,
                        line_count=len(current_context_lines),
                        content='\n'.join(current_context_lines),
                        start_line=current_start_line,
                        end_line=line_num - 1,
                    ))

                # Start new file context
                current_file = file_match.strip()
                current_context_lines = []
                current_start_line = line_num
                in_code_block = False
                continue

            # Track code block boundaries
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            # Collect context lines (inside code blocks only)
            if in_code_block and current_file:
                current_context_lines.append(line)

        # Save last file context
        if current_file and current_context_lines:
            file_contexts.append(FileContext(
                file_path=current_file,
                line_count=len(current_context_lines),
                content='\n'.join(current_context_lines),
                start_line=current_start_line,
                end_line=len(lines),
            ))

        return file_contexts

    def _match_file_header(self, line: str) -> Optional[str]:
        """
        Match line against file header patterns.

        Args:
            line: Line to check

        Returns:
            Matched file path or None
        """
        for pattern in self.FILE_HEADER_PATTERNS:
            match = re.match(pattern, line.strip())
            if match:
                return match.group(1).strip()
        return None

    # =========================================================================
    # Reporting Methods
    # =========================================================================

    def format_violation_report(
        self,
        validation: ContextValidation,
        verbose: bool = False,
    ) -> str:
        """
        Format validation report for GitHub check or CLI output.

        Args:
            validation: ContextValidation result
            verbose: Include passed files in report

        Returns:
            Formatted report string
        """
        if validation.overall_passed:
            report = f"✅ All {validation.total_files} file contexts are under 60 lines."
            if verbose and validation.passed_contexts:
                report += "\n\nFiles analyzed:\n"
                for ctx in validation.passed_contexts:
                    report += f"  - {ctx.file_path}: {ctx.line_count} lines ✅\n"
            return report

        report_lines = [
            f"❌ Context validation failed: {validation.failed_files}/{validation.total_files} files over 60 lines",
            "",
            "Violations:",
        ]

        for ctx in validation.violations:
            report_lines.append(
                f"  - {ctx.file_path}: {ctx.line_count} lines (AGENTS.md L{ctx.start_line})"
            )

        report_lines.extend([
            "",
            "💡 Suggestions:",
            "  - Break large contexts into sub-files (e.g., app/api/users → users_routes, users_schemas)",
            "  - Link to detailed docs instead of embedding full code",
            "  - Use '...existing code...' markers to abbreviate",
            "  - Focus on key APIs and patterns, not full implementations",
        ])

        if verbose and validation.passed_contexts:
            report_lines.extend([
                "",
                "Passed files:",
            ])
            for ctx in validation.passed_contexts:
                report_lines.append(f"  - {ctx.file_path}: {ctx.line_count} lines ✅")

        return '\n'.join(report_lines)

    def format_json_report(self, validation: ContextValidation) -> dict:
        """
        Format validation result as JSON-serializable dict.

        Args:
            validation: ContextValidation result

        Returns:
            Dict suitable for JSON serialization
        """
        return {
            "overall_passed": validation.overall_passed,
            "total_files": validation.total_files,
            "passed_files": validation.passed_files,
            "failed_files": validation.failed_files,
            "max_allowed_lines": self.MAX_CONTEXT_LINES,
            "violations": [
                {
                    "file_path": ctx.file_path,
                    "line_count": ctx.line_count,
                    "start_line": ctx.start_line,
                    "end_line": ctx.end_line,
                    "over_by": ctx.line_count - self.MAX_CONTEXT_LINES,
                }
                for ctx in validation.violations
            ],
            "validated_at": validation.validated_at.isoformat(),
        }

    def format_github_check_output(self, validation: ContextValidation) -> dict:
        """
        Format validation result for GitHub Check Run output.

        Args:
            validation: ContextValidation result

        Returns:
            Dict with title, summary, text for GitHub API
        """
        conclusion = "success" if validation.overall_passed else "failure"

        summary = validation.summary

        # Build detailed text
        text_lines = [
            f"**Files analyzed**: {validation.total_files}",
            f"**Passed**: {validation.passed_files}",
            f"**Failed**: {validation.failed_files}",
            f"**Line limit**: {self.MAX_CONTEXT_LINES} lines per file context",
            "",
        ]

        if validation.violations:
            text_lines.extend([
                "## Violations",
                "",
            ])
            for ctx in validation.violations:
                text_lines.append(
                    f"- `{ctx.file_path}`: {ctx.line_count} lines "
                    f"({ctx.line_count - self.MAX_CONTEXT_LINES} over limit) "
                    f"— AGENTS.md L{ctx.start_line}"
                )

            text_lines.extend([
                "",
                "## Suggestions",
                "",
                "- Break large contexts into sub-files",
                "- Link to detailed docs instead of embedding full code",
                "- Use `...existing code...` markers to abbreviate",
            ])

        return {
            "conclusion": conclusion,
            "output": {
                "title": "AGENTS.md Context Validation",
                "summary": summary,
                "text": '\n'.join(text_lines),
            },
        }


# ============================================================================
# Factory Function
# ============================================================================


def create_context_validation_service(
    github_service=None,
) -> ContextValidationService:
    """
    Factory function to create ContextValidationService.

    Args:
        github_service: Optional GitHub service for remote validation

    Returns:
        Configured ContextValidationService
    """
    return ContextValidationService(github_service=github_service)
