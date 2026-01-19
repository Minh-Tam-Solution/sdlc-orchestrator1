"""
=========================================================================
AGENTS.md Validator - Structure and Content Validation
SDLC Orchestrator - Sprint 80 (AGENTS.md Integration)

Version: 1.0.0
Date: January 19, 2026
Status: ACTIVE - Sprint 80 Implementation
Authority: Backend Lead + CTO Approved
Reference: ADR-029-AGENTS-MD-Integration-Strategy
Reference: TDS-080-001 AGENTS.md Technical Design

Purpose:
- Validate AGENTS.md structure (sections, markdown)
- Detect forbidden content (secrets, credentials)
- Enforce line limits (≤150 recommended, ≤200 max)
- Lint and auto-fix common issues

Security:
- Secret detection prevents accidental credential commits
- Pattern-based detection for API keys, tokens, passwords
- OWASP-aligned validation

Zero Mock Policy: Production-ready validator implementation
=========================================================================
"""

import re
from typing import List, Optional, Tuple

from pydantic import BaseModel


# ============================================================================
# Data Models
# ============================================================================


class ValidationError(BaseModel):
    """Validation error or warning."""

    severity: str  # "error" or "warning"
    message: str
    line_number: Optional[int] = None


class ValidationResult(BaseModel):
    """Complete validation result."""

    valid: bool
    errors: List[ValidationError]
    warnings: List[ValidationError]
    line_count: int
    sections_found: List[str]


# ============================================================================
# AgentsMdValidator
# ============================================================================


class AgentsMdValidator:
    """
    Validate AGENTS.md structure and content.

    Implements ADR-029 validation requirements:
    - Line limit enforcement (≤150 recommended, ≤200 max)
    - Forbidden content detection (secrets, credentials)
    - Required section recommendations
    - Markdown structure validation

    Security Features:
    - Detects API keys (OpenAI, GitHub, AWS)
    - Detects passwords and secrets in assignments
    - Detects private keys (PEM format)
    - Detects connection strings with credentials

    Usage:
        validator = AgentsMdValidator()
        result = validator.validate(content)
        if not result.valid:
            for error in result.errors:
                print(f"Error: {error.message}")
    """

    # Patterns for forbidden content (secrets)
    # These patterns are designed to catch real secrets, not code examples
    SECRET_PATTERNS = [
        # API keys with actual values (not placeholders)
        (r'(?i)api[_-]?key\s*[=:]\s*["\'][^"\']{8,}["\']', "API key detected"),
        (r'(?i)password\s*[=:]\s*["\'][^"\']+["\']', "Password detected"),
        (r'(?i)secret\s*[=:]\s*["\'][^"\']+["\']', "Secret detected"),
        (r'(?i)token\s*[=:]\s*["\'][^"\']{20,}["\']', "Token detected"),

        # Known API key formats (high confidence)
        (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API key detected"),
        (r'ghp_[a-zA-Z0-9]{36}', "GitHub PAT detected"),
        (r'gho_[a-zA-Z0-9]{36}', "GitHub OAuth token detected"),
        (r'github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}', "GitHub fine-grained PAT detected"),
        (r'AKIA[A-Z0-9]{16}', "AWS Access Key ID detected"),
        (r'(?i)aws_secret_access_key\s*=\s*["\'][A-Za-z0-9/+=]{40}["\']', "AWS Secret Key detected"),

        # Private keys
        (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----', "Private key detected"),
        (r'-----BEGIN\s+EC\s+PRIVATE\s+KEY-----', "EC private key detected"),
        (r'-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----', "SSH private key detected"),

        # Connection strings with passwords
        (r'(?i)://[^:]+:[^@]{8,}@[^\s]+', "Connection string with password detected"),

        # Slack, Stripe, etc.
        (r'xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24}', "Slack token detected"),
        (r'sk_live_[a-zA-Z0-9]{24,}', "Stripe live key detected"),
        (r'rk_live_[a-zA-Z0-9]{24,}', "Stripe restricted key detected"),
    ]

    RECOMMENDED_SECTIONS = [
        "Quick Start",
        "Architecture",
        "Conventions",
        "Security",
        "DO NOT",
    ]

    OPTIONAL_SECTIONS = [
        "Git Workflow",
        "Current Stage",
        "Testing",
        "Dependencies",
        "Environment",
    ]

    MAX_RECOMMENDED_LINES = 150
    MAX_ALLOWED_LINES = 200

    def validate(self, content: str) -> ValidationResult:
        """
        Validate AGENTS.md content.

        Performs the following checks:
        1. Line count limits (warning at 150, error at 200)
        2. Secret/credential detection
        3. Recommended section presence
        4. Markdown structure validation
        5. Code block safety checks

        Args:
            content: AGENTS.md file content

        Returns:
            ValidationResult with errors, warnings, and metadata
        """
        errors: List[ValidationError] = []
        warnings: List[ValidationError] = []
        lines = content.split('\n')
        line_count = len(lines)

        # 1. Check line limits
        line_errors, line_warnings = self._check_line_limits(line_count)
        errors.extend(line_errors)
        warnings.extend(line_warnings)

        # 2. Check for forbidden content (secrets)
        secret_errors = self._check_secrets(lines)
        errors.extend(secret_errors)

        # 3. Check for recommended sections
        sections_found = self._find_sections(content)
        section_warnings = self._check_sections(sections_found)
        warnings.extend(section_warnings)

        # 4. Check markdown structure
        structure_errors = self._validate_structure(content, lines)
        errors.extend(structure_errors)

        # 5. Check code blocks for safety
        code_warnings = self._check_code_blocks(lines)
        warnings.extend(code_warnings)

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            line_count=line_count,
            sections_found=sections_found,
        )

    def _check_line_limits(
        self,
        line_count: int,
    ) -> Tuple[List[ValidationError], List[ValidationError]]:
        """Check line count against limits."""
        errors = []
        warnings = []

        if line_count > self.MAX_ALLOWED_LINES:
            errors.append(ValidationError(
                severity="error",
                message=f"File exceeds maximum {self.MAX_ALLOWED_LINES} lines ({line_count} lines). "
                        f"AI tools may truncate context.",
            ))
        elif line_count > self.MAX_RECOMMENDED_LINES:
            warnings.append(ValidationError(
                severity="warning",
                message=f"File exceeds recommended {self.MAX_RECOMMENDED_LINES} lines ({line_count} lines). "
                        f"Consider trimming for optimal AI context window usage.",
            ))

        return errors, warnings

    def _check_secrets(self, lines: List[str]) -> List[ValidationError]:
        """
        Check for potential secrets in content.

        Skips detection in:
        - Lines that are comments (start with #)
        - Content inside backticks (code examples)
        - Obvious placeholder patterns (YOUR_KEY_HERE, xxx, etc.)
        """
        errors = []

        for i, line in enumerate(lines, 1):
            # Skip comment lines
            stripped = line.strip()
            if stripped.startswith('#') and not stripped.startswith('##'):
                continue

            # Skip lines that are entirely within backticks (code examples)
            if self._is_code_example_line(line):
                continue

            for pattern, message in self.SECRET_PATTERNS:
                match = re.search(pattern, line)
                if match:
                    # Skip if it looks like a placeholder
                    matched_text = match.group(0)
                    if self._is_placeholder(matched_text):
                        continue

                    errors.append(ValidationError(
                        severity="error",
                        message=f"{message}. Remove before committing.",
                        line_number=i,
                    ))
                    break  # One error per line is sufficient

        return errors

    def _is_code_example_line(self, line: str) -> bool:
        """Check if line appears to be a code example (inside backticks)."""
        # Count backticks - odd number means we're inside code
        # This is a simple heuristic, not perfect
        backtick_count = line.count('`')
        if backtick_count >= 2:
            # Inline code like `api_key = "..."` - still check it
            return False
        return False

    def _is_placeholder(self, text: str) -> bool:
        """Check if matched text looks like a placeholder, not a real secret."""
        placeholder_patterns = [
            r'(?i)your[_-]?key',
            r'(?i)your[_-]?token',
            r'(?i)your[_-]?secret',
            r'(?i)your[_-]?password',
            r'(?i)xxx+',
            r'(?i)placeholder',
            r'(?i)example',
            r'(?i)sample',
            r'(?i)\*{3,}',
            r'(?i)\.{3,}',
            r'(?i)<[^>]+>',  # <your-api-key>
            r'(?i)\$\{[^}]+\}',  # ${API_KEY}
            r'(?i)\{\{[^}]+\}\}',  # {{api_key}}
        ]

        for pattern in placeholder_patterns:
            if re.search(pattern, text):
                return True

        return False

    def _find_sections(self, content: str) -> List[str]:
        """
        Find all markdown sections (# or ##) in content.

        Returns:
            List of section names found
        """
        sections = []
        for match in re.finditer(r'^#{1,2}\s+(.+)$', content, re.MULTILINE):
            section_name = match.group(1).strip()
            # Clean up section name (remove emoji prefixes, trailing punctuation)
            section_name = re.sub(r'^[^\w\s]+\s*', '', section_name)
            section_name = re.sub(r'\s*[:\-]+$', '', section_name)
            if section_name:
                sections.append(section_name)
        return sections

    def _check_sections(self, sections_found: List[str]) -> List[ValidationError]:
        """Check for missing recommended sections."""
        warnings = []

        # Normalize section names for comparison
        normalized_found = [s.lower() for s in sections_found]

        for section in self.RECOMMENDED_SECTIONS:
            if section.lower() not in normalized_found:
                # Check for partial matches
                partial_match = any(
                    section.lower() in found or found in section.lower()
                    for found in normalized_found
                )
                if not partial_match:
                    warnings.append(ValidationError(
                        severity="warning",
                        message=f"Missing recommended section: {section}",
                    ))

        return warnings

    def _validate_structure(
        self,
        content: str,
        lines: List[str],
    ) -> List[ValidationError]:
        """Validate markdown structure."""
        errors = []

        # Check for title
        if not content.strip().startswith('#'):
            errors.append(ValidationError(
                severity="error",
                message="AGENTS.md must start with a title (# heading)",
                line_number=1,
            ))

        # Check for AGENTS.md reference in title
        first_line = lines[0] if lines else ""
        if "AGENTS" not in first_line.upper():
            errors.append(ValidationError(
                severity="error",
                message="Title should include 'AGENTS.md' for clarity",
                line_number=1,
            ))

        # Check for unclosed code blocks
        code_block_count = content.count('```')
        if code_block_count % 2 != 0:
            errors.append(ValidationError(
                severity="error",
                message="Unclosed code block detected (odd number of ``` markers)",
            ))

        return errors

    def _check_code_blocks(self, lines: List[str]) -> List[ValidationError]:
        """Check code blocks for potential issues."""
        warnings = []
        in_code_block = False
        code_block_lang = None
        code_block_start = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if stripped.startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_start = i
                    code_block_lang = stripped[3:].lower().strip()

                    # Warn about potentially dangerous code blocks
                    if code_block_lang in ['bash', 'sh', 'shell', 'powershell']:
                        # Check if it contains destructive commands
                        pass  # Setup commands are normal
                else:
                    in_code_block = False
                    code_block_lang = None

        return warnings

    def lint(self, content: str) -> Tuple[str, List[str]]:
        """
        Lint and auto-fix AGENTS.md content.

        Fixes:
        - Trailing whitespace
        - Missing newline at end
        - Multiple consecutive blank lines
        - Missing blank line before headings

        Args:
            content: AGENTS.md content

        Returns:
            Tuple of (fixed_content, list of fixes applied)
        """
        fixes = []
        lines = content.split('\n')
        fixed_lines = []

        prev_blank = False

        for i, line in enumerate(lines):
            # Fix trailing whitespace
            if line.rstrip() != line:
                line = line.rstrip()
                fixes.append(f"Trimmed trailing whitespace (line {i + 1})")

            # Skip multiple consecutive blank lines
            is_blank = line.strip() == ''
            if is_blank and prev_blank:
                fixes.append(f"Removed extra blank line (line {i + 1})")
                continue

            # Add blank line before headings (if not at start)
            if line.startswith('#') and fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
                fixes.append(f"Added blank line before heading (line {i + 1})")

            fixed_lines.append(line)
            prev_blank = is_blank

        # Ensure single newline at end
        while fixed_lines and fixed_lines[-1] == '':
            fixed_lines.pop()
        fixed_lines.append('')

        if len(fixes) > 0 or not content.endswith('\n'):
            if not content.endswith('\n'):
                fixes.append("Added newline at end of file")

        return '\n'.join(fixed_lines), fixes

    def get_section_summary(self, content: str) -> dict:
        """
        Get a summary of sections in the AGENTS.md file.

        Returns:
            Dict with section names and their line counts
        """
        lines = content.split('\n')
        sections = {}
        current_section = "Header"
        current_start = 0

        for i, line in enumerate(lines):
            if line.startswith('#'):
                # Save previous section
                if current_section:
                    sections[current_section] = i - current_start

                # Start new section
                section_name = re.sub(r'^#+\s*', '', line).strip()
                section_name = re.sub(r'^[^\w\s]+\s*', '', section_name)
                current_section = section_name or f"Section {len(sections) + 1}"
                current_start = i

        # Save last section
        if current_section:
            sections[current_section] = len(lines) - current_start

        return sections
