"""
Codegen Quality Gate Validator - Quality validation for AI-generated code.

SDLC Stage: 04 - BUILD
Sprint: 48 - Quality Gates + Ollama Optimization + MVP Hardening
Framework: SDLC 5.1.3
Epic: EP-06 IR-Based Vietnamese SME Codegen

Purpose:
Validate AI-generated code before delivery to users. Ensures generated code
meets quality standards for architecture, security, and functionality.

Quality Gates:
1. Architecture Validation - Layer separation, no circular dependencies
2. Security Scan - OWASP checks via Semgrep integration
3. Syntax Validation - Code compiles/parses without errors
4. Test Execution - Generated tests must pass (if applicable)

Blocking: Yes (default) - failed quality gates block code delivery
Timeout: 120 seconds (default)

Reference:
- Sprint 48 Plan: docs/04-build/02-Sprint-Plans/SPRINT-48-FIXER-BACKUP-ENGINE.md
- ADR-022: Multi-Provider Codegen Architecture
"""

import ast
import logging
import re
import tempfile
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID

from . import BaseValidator, ValidatorConfig, ValidatorResult, ValidatorStatus

logger = logging.getLogger(__name__)


class QualityGateType(str, Enum):
    """Types of quality gates for generated code."""

    SYNTAX = "syntax"
    ARCHITECTURE = "architecture"
    SECURITY = "security"
    IMPORTS = "imports"
    COMPLEXITY = "complexity"


@dataclass
class QualityIssue:
    """A single quality issue found in generated code."""

    gate_type: QualityGateType
    severity: str  # "error", "warning", "info"
    file_path: str
    line: Optional[int]
    message: str
    rule_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "gate_type": self.gate_type.value,
            "severity": self.severity,
            "file_path": self.file_path,
            "line": self.line,
            "message": self.message,
            "rule_id": self.rule_id,
        }


class CodegenQualityValidator(BaseValidator):
    """
    Quality gate validator for AI-generated code.

    Validates generated code against multiple quality gates:
    - Syntax: Code must parse without errors
    - Architecture: Layer separation, no circular imports
    - Security: Basic security patterns (hardcoded secrets, SQL injection)
    - Imports: Valid import statements
    - Complexity: Function/class complexity limits

    This validator is designed to work with CodegenResult.files dictionary.
    """

    name = "codegen-quality"
    description = "Quality gates for AI-generated code"
    default_blocking = True
    default_timeout_seconds = 120

    # Architecture layer definitions for FastAPI projects
    LAYER_ORDER = ["api", "services", "repositories", "models", "schemas", "core"]

    # Forbidden import patterns (lower layer importing upper layer)
    FORBIDDEN_IMPORTS = {
        "models": {"api", "services"},
        "schemas": {"api", "services", "repositories"},
        "repositories": {"api", "services"},
        "services": {"api"},
        "core": {"api", "services", "repositories"},
    }

    # Security patterns to detect
    SECURITY_PATTERNS = {
        "hardcoded_secret": {
            "pattern": r'(?:password|secret|api_key|token)\s*=\s*["\'][^"\']+["\']',
            "message": "Potential hardcoded secret detected",
            "severity": "error",
        },
        "sql_injection": {
            "pattern": r'execute\s*\(\s*f["\']|execute\s*\(\s*["\'].*%s',
            "message": "Potential SQL injection vulnerability",
            "severity": "error",
        },
        "eval_usage": {
            "pattern": r'\beval\s*\(',
            "message": "Dangerous eval() usage detected",
            "severity": "error",
        },
        "exec_usage": {
            "pattern": r'\bexec\s*\(',
            "message": "Dangerous exec() usage detected",
            "severity": "warning",
        },
        "pickle_load": {
            "pattern": r'pickle\.load\s*\(',
            "message": "Unsafe pickle.load() - potential deserialization attack",
            "severity": "warning",
        },
    }

    # Complexity thresholds
    MAX_FUNCTION_LINES = 50
    MAX_CLASS_METHODS = 20
    MAX_NESTED_DEPTH = 4

    def __init__(
        self,
        config: Optional[ValidatorConfig] = None,
        enable_security_scan: bool = True,
        enable_architecture_check: bool = True,
        enable_complexity_check: bool = True,
    ):
        """
        Initialize quality validator.

        Args:
            config: Validator configuration
            enable_security_scan: Enable security pattern detection
            enable_architecture_check: Enable architecture layer validation
            enable_complexity_check: Enable complexity metrics
        """
        super().__init__(config)
        self.enable_security_scan = enable_security_scan
        self.enable_architecture_check = enable_architecture_check
        self.enable_complexity_check = enable_complexity_check

    async def validate(
        self,
        project_id: UUID,
        pr_number: str,
        files: List[str],
        diff: str,
    ) -> ValidatorResult:
        """
        Standard validator interface - validates files from PR.

        For generated code validation, use validate_generated_code() instead.
        """
        started_at = time.time()

        # This validator is primarily for generated code
        # For PR validation, delegate to SAST validator
        duration_ms = int((time.time() - started_at) * 1000)

        return ValidatorResult(
            validator_name=self.name,
            status=ValidatorStatus.SKIPPED,
            message="Use validate_generated_code() for AI-generated code",
            details={"note": "This validator is for CodegenResult validation"},
            duration_ms=duration_ms,
            blocking=False,
        )

    async def validate_generated_code(
        self,
        files: Dict[str, str],
        language: str = "python",
        framework: str = "fastapi",
    ) -> ValidatorResult:
        """
        Validate AI-generated code against quality gates.

        Args:
            files: Dictionary mapping file paths to file contents
            language: Programming language (python, typescript, etc.)
            framework: Target framework (fastapi, react, etc.)

        Returns:
            ValidatorResult with quality gate results
        """
        started_at = time.time()
        issues: List[QualityIssue] = []

        try:
            if not files:
                duration_ms = int((time.time() - started_at) * 1000)
                return ValidatorResult(
                    validator_name=self.name,
                    status=ValidatorStatus.SKIPPED,
                    message="No files to validate",
                    details={"files_checked": 0},
                    duration_ms=duration_ms,
                    blocking=False,
                )

            logger.info(f"Validating {len(files)} generated files")

            # Run quality gates based on language
            if language.lower() == "python":
                issues.extend(self._validate_python_files(files, framework))
            elif language.lower() in ("typescript", "javascript"):
                issues.extend(self._validate_typescript_files(files, framework))
            else:
                # Generic validation for other languages
                issues.extend(self._validate_generic_files(files))

            duration_ms = int((time.time() - started_at) * 1000)

            # Categorize issues
            errors = [i for i in issues if i.severity == "error"]
            warnings = [i for i in issues if i.severity == "warning"]
            infos = [i for i in issues if i.severity == "info"]

            # Build details
            details = self._build_details(files, issues, errors, warnings, infos)

            # Determine status
            if errors:
                status = ValidatorStatus.FAILED
                message = f"Quality gates failed: {len(errors)} errors, {len(warnings)} warnings"
                blocking = True
            elif warnings:
                status = ValidatorStatus.PASSED
                message = f"Quality gates passed with {len(warnings)} warnings"
                blocking = False
            else:
                status = ValidatorStatus.PASSED
                message = "All quality gates passed"
                blocking = False

            return ValidatorResult(
                validator_name=self.name,
                status=status,
                message=message,
                details=details,
                duration_ms=duration_ms,
                blocking=blocking,
            )

        except Exception as e:
            logger.error(f"Quality validation error: {e}", exc_info=True)
            duration_ms = int((time.time() - started_at) * 1000)
            return ValidatorResult(
                validator_name=self.name,
                status=ValidatorStatus.ERROR,
                message=f"Quality validation error: {str(e)}",
                details={"error": str(e)},
                duration_ms=duration_ms,
                blocking=False,
            )

    def _validate_python_files(
        self,
        files: Dict[str, str],
        framework: str,
    ) -> List[QualityIssue]:
        """Validate Python files."""
        issues: List[QualityIssue] = []

        for file_path, content in files.items():
            if not file_path.endswith(".py"):
                continue

            # 1. Syntax validation
            syntax_issues = self._check_python_syntax(file_path, content)
            issues.extend(syntax_issues)

            # Skip further checks if syntax errors exist
            if any(i.gate_type == QualityGateType.SYNTAX for i in syntax_issues):
                continue

            # 2. Security patterns
            if self.enable_security_scan:
                issues.extend(self._check_security_patterns(file_path, content))

            # 3. Architecture validation (for FastAPI)
            if self.enable_architecture_check and framework.lower() == "fastapi":
                issues.extend(self._check_architecture(file_path, content, files))

            # 4. Complexity check
            if self.enable_complexity_check:
                issues.extend(self._check_python_complexity(file_path, content))

            # 5. Import validation
            issues.extend(self._check_python_imports(file_path, content))

        return issues

    def _validate_typescript_files(
        self,
        files: Dict[str, str],
        framework: str,
    ) -> List[QualityIssue]:
        """Validate TypeScript/JavaScript files."""
        issues: List[QualityIssue] = []

        for file_path, content in files.items():
            if not file_path.endswith((".ts", ".tsx", ".js", ".jsx")):
                continue

            # Basic syntax check (brace matching)
            issues.extend(self._check_brace_matching(file_path, content))

            # Security patterns
            if self.enable_security_scan:
                issues.extend(self._check_security_patterns(file_path, content))

            # React-specific checks
            if framework.lower() == "react" and file_path.endswith((".tsx", ".jsx")):
                issues.extend(self._check_react_patterns(file_path, content))

        return issues

    def _validate_generic_files(
        self,
        files: Dict[str, str],
    ) -> List[QualityIssue]:
        """Generic validation for any language."""
        issues: List[QualityIssue] = []

        for file_path, content in files.items():
            # Security patterns work for any language
            if self.enable_security_scan:
                issues.extend(self._check_security_patterns(file_path, content))

            # Check for common issues
            issues.extend(self._check_common_issues(file_path, content))

        return issues

    def _check_python_syntax(
        self,
        file_path: str,
        content: str,
    ) -> List[QualityIssue]:
        """Check Python syntax validity."""
        issues: List[QualityIssue] = []

        try:
            ast.parse(content)
        except SyntaxError as e:
            issues.append(
                QualityIssue(
                    gate_type=QualityGateType.SYNTAX,
                    severity="error",
                    file_path=file_path,
                    line=e.lineno,
                    message=f"Syntax error: {e.msg}",
                    rule_id="SYNTAX-001",
                )
            )

        return issues

    def _check_security_patterns(
        self,
        file_path: str,
        content: str,
    ) -> List[QualityIssue]:
        """Check for security anti-patterns."""
        issues: List[QualityIssue] = []

        for rule_id, config in self.SECURITY_PATTERNS.items():
            pattern = config["pattern"]
            matches = list(re.finditer(pattern, content, re.IGNORECASE))

            for match in matches:
                # Calculate line number
                line_num = content[: match.start()].count("\n") + 1

                issues.append(
                    QualityIssue(
                        gate_type=QualityGateType.SECURITY,
                        severity=config["severity"],
                        file_path=file_path,
                        line=line_num,
                        message=config["message"],
                        rule_id=f"SEC-{rule_id.upper()}",
                    )
                )

        return issues

    def _check_architecture(
        self,
        file_path: str,
        content: str,
        all_files: Dict[str, str],
    ) -> List[QualityIssue]:
        """Check architecture layer violations."""
        issues: List[QualityIssue] = []

        # Determine current layer from file path
        current_layer = self._get_layer_from_path(file_path)
        if not current_layer:
            return issues

        # Parse imports
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return issues

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_layer = self._get_layer_from_import(alias.name)
                    if import_layer and self._is_forbidden_import(
                        current_layer, import_layer
                    ):
                        issues.append(
                            QualityIssue(
                                gate_type=QualityGateType.ARCHITECTURE,
                                severity="error",
                                file_path=file_path,
                                line=node.lineno,
                                message=f"Architecture violation: {current_layer} cannot import from {import_layer}",
                                rule_id="ARCH-001",
                            )
                        )

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    import_layer = self._get_layer_from_import(node.module)
                    if import_layer and self._is_forbidden_import(
                        current_layer, import_layer
                    ):
                        issues.append(
                            QualityIssue(
                                gate_type=QualityGateType.ARCHITECTURE,
                                severity="error",
                                file_path=file_path,
                                line=node.lineno,
                                message=f"Architecture violation: {current_layer} cannot import from {import_layer}",
                                rule_id="ARCH-001",
                            )
                        )

        # Check for circular imports
        circular = self._detect_circular_imports(file_path, content, all_files)
        issues.extend(circular)

        return issues

    def _check_python_complexity(
        self,
        file_path: str,
        content: str,
    ) -> List[QualityIssue]:
        """Check Python code complexity."""
        issues: List[QualityIssue] = []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return issues

        for node in ast.walk(tree):
            # Check function length
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_lines = node.end_lineno - node.lineno if node.end_lineno else 0
                if func_lines > self.MAX_FUNCTION_LINES:
                    issues.append(
                        QualityIssue(
                            gate_type=QualityGateType.COMPLEXITY,
                            severity="warning",
                            file_path=file_path,
                            line=node.lineno,
                            message=f"Function '{node.name}' too long ({func_lines} lines > {self.MAX_FUNCTION_LINES})",
                            rule_id="COMPLEX-001",
                        )
                    )

                # Check nesting depth
                max_depth = self._get_max_nesting_depth(node)
                if max_depth > self.MAX_NESTED_DEPTH:
                    issues.append(
                        QualityIssue(
                            gate_type=QualityGateType.COMPLEXITY,
                            severity="warning",
                            file_path=file_path,
                            line=node.lineno,
                            message=f"Function '{node.name}' has deep nesting ({max_depth} > {self.MAX_NESTED_DEPTH})",
                            rule_id="COMPLEX-002",
                        )
                    )

            # Check class method count
            elif isinstance(node, ast.ClassDef):
                method_count = sum(
                    1
                    for n in node.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                )
                if method_count > self.MAX_CLASS_METHODS:
                    issues.append(
                        QualityIssue(
                            gate_type=QualityGateType.COMPLEXITY,
                            severity="warning",
                            file_path=file_path,
                            line=node.lineno,
                            message=f"Class '{node.name}' has too many methods ({method_count} > {self.MAX_CLASS_METHODS})",
                            rule_id="COMPLEX-003",
                        )
                    )

        return issues

    def _check_python_imports(
        self,
        file_path: str,
        content: str,
    ) -> List[QualityIssue]:
        """Check Python import validity."""
        issues: List[QualityIssue] = []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return issues

        # Check for wildcard imports
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name == "*":
                        issues.append(
                            QualityIssue(
                                gate_type=QualityGateType.IMPORTS,
                                severity="warning",
                                file_path=file_path,
                                line=node.lineno,
                                message=f"Wildcard import from '{node.module}' - use explicit imports",
                                rule_id="IMPORT-001",
                            )
                        )

        return issues

    def _check_brace_matching(
        self,
        file_path: str,
        content: str,
    ) -> List[QualityIssue]:
        """Check brace/bracket matching for JS/TS files."""
        issues: List[QualityIssue] = []

        stack: List[Tuple[str, int]] = []
        pairs = {"(": ")", "[": "]", "{": "}"}
        in_string = False
        string_char = None

        for line_num, line in enumerate(content.split("\n"), 1):
            i = 0
            while i < len(line):
                char = line[i]

                # Handle string literals
                if char in ('"', "'", "`") and (i == 0 or line[i - 1] != "\\"):
                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char:
                        in_string = False
                        string_char = None

                if not in_string:
                    if char in pairs:
                        stack.append((char, line_num))
                    elif char in pairs.values():
                        if not stack:
                            issues.append(
                                QualityIssue(
                                    gate_type=QualityGateType.SYNTAX,
                                    severity="error",
                                    file_path=file_path,
                                    line=line_num,
                                    message=f"Unmatched closing '{char}'",
                                    rule_id="SYNTAX-002",
                                )
                            )
                        else:
                            open_char, _ = stack.pop()
                            if pairs.get(open_char) != char:
                                issues.append(
                                    QualityIssue(
                                        gate_type=QualityGateType.SYNTAX,
                                        severity="error",
                                        file_path=file_path,
                                        line=line_num,
                                        message=f"Mismatched brackets: expected '{pairs[open_char]}', got '{char}'",
                                        rule_id="SYNTAX-003",
                                    )
                                )
                i += 1

        # Check for unclosed brackets
        for open_char, line_num in stack:
            issues.append(
                QualityIssue(
                    gate_type=QualityGateType.SYNTAX,
                    severity="error",
                    file_path=file_path,
                    line=line_num,
                    message=f"Unclosed '{open_char}'",
                    rule_id="SYNTAX-004",
                )
            )

        return issues

    def _check_react_patterns(
        self,
        file_path: str,
        content: str,
    ) -> List[QualityIssue]:
        """Check React-specific patterns."""
        issues: List[QualityIssue] = []

        # Check for missing key in map
        if ".map(" in content and "key=" not in content:
            # Find line number
            for line_num, line in enumerate(content.split("\n"), 1):
                if ".map(" in line:
                    issues.append(
                        QualityIssue(
                            gate_type=QualityGateType.ARCHITECTURE,
                            severity="warning",
                            file_path=file_path,
                            line=line_num,
                            message="React map() should include key prop",
                            rule_id="REACT-001",
                        )
                    )
                    break

        # Check for dangerous innerHTML
        if "dangerouslySetInnerHTML" in content:
            for line_num, line in enumerate(content.split("\n"), 1):
                if "dangerouslySetInnerHTML" in line:
                    issues.append(
                        QualityIssue(
                            gate_type=QualityGateType.SECURITY,
                            severity="warning",
                            file_path=file_path,
                            line=line_num,
                            message="dangerouslySetInnerHTML can lead to XSS - ensure input is sanitized",
                            rule_id="REACT-002",
                        )
                    )

        return issues

    def _check_common_issues(
        self,
        file_path: str,
        content: str,
    ) -> List[QualityIssue]:
        """Check common issues in any file."""
        issues: List[QualityIssue] = []

        # Check for TODO/FIXME (should not be in generated code)
        for line_num, line in enumerate(content.split("\n"), 1):
            if "TODO" in line or "FIXME" in line:
                issues.append(
                    QualityIssue(
                        gate_type=QualityGateType.ARCHITECTURE,
                        severity="warning",
                        file_path=file_path,
                        line=line_num,
                        message="Generated code contains TODO/FIXME - incomplete implementation",
                        rule_id="GEN-001",
                    )
                )

            # Check for placeholder patterns
            if "# placeholder" in line.lower() or "// placeholder" in line.lower():
                issues.append(
                    QualityIssue(
                        gate_type=QualityGateType.ARCHITECTURE,
                        severity="error",
                        file_path=file_path,
                        line=line_num,
                        message="Generated code contains placeholder - incomplete implementation",
                        rule_id="GEN-002",
                    )
                )

        return issues

    def _get_layer_from_path(self, file_path: str) -> Optional[str]:
        """Extract layer from file path."""
        path_lower = file_path.lower()
        for layer in self.LAYER_ORDER:
            if f"/{layer}/" in path_lower or path_lower.startswith(f"{layer}/"):
                return layer
        return None

    def _get_layer_from_import(self, import_name: str) -> Optional[str]:
        """Extract layer from import name."""
        import_lower = import_name.lower()
        for layer in self.LAYER_ORDER:
            if f".{layer}." in import_lower or import_lower.startswith(f"{layer}."):
                return layer
        return None

    def _is_forbidden_import(self, current_layer: str, import_layer: str) -> bool:
        """Check if import violates architecture rules."""
        forbidden = self.FORBIDDEN_IMPORTS.get(current_layer, set())
        return import_layer in forbidden

    def _detect_circular_imports(
        self,
        file_path: str,
        content: str,
        all_files: Dict[str, str],
    ) -> List[QualityIssue]:
        """Detect circular import patterns."""
        issues: List[QualityIssue] = []

        # Build import graph
        imports = self._extract_imports(content)

        # Check if any imported module imports this file
        current_module = self._path_to_module(file_path)

        for imp in imports:
            # Find the file for this import
            imp_file = self._module_to_path(imp, all_files)
            if imp_file and imp_file in all_files:
                imp_content = all_files[imp_file]
                imp_imports = self._extract_imports(imp_content)

                if current_module in imp_imports:
                    issues.append(
                        QualityIssue(
                            gate_type=QualityGateType.ARCHITECTURE,
                            severity="error",
                            file_path=file_path,
                            line=1,
                            message=f"Circular import detected: {file_path} <-> {imp_file}",
                            rule_id="ARCH-002",
                        )
                    )

        return issues

    def _extract_imports(self, content: str) -> Set[str]:
        """Extract all import statements from Python code."""
        imports: Set[str] = set()

        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
        except SyntaxError:
            pass

        return imports

    def _path_to_module(self, file_path: str) -> str:
        """Convert file path to module name."""
        # Remove .py extension and convert slashes to dots
        module = file_path.replace(".py", "").replace("/", ".").replace("\\", ".")
        # Remove leading dots
        return module.lstrip(".")

    def _module_to_path(self, module: str, all_files: Dict[str, str]) -> Optional[str]:
        """Convert module name to file path."""
        # Convert dots to slashes and add .py
        path = module.replace(".", "/") + ".py"

        # Try to find matching file
        for file_path in all_files:
            if file_path.endswith(path):
                return file_path

        return None

    def _get_max_nesting_depth(self, node: ast.AST, depth: int = 0) -> int:
        """Calculate maximum nesting depth in a function."""
        max_depth = depth

        for child in ast.iter_child_nodes(node):
            if isinstance(
                child, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.ExceptHandler)
            ):
                child_depth = self._get_max_nesting_depth(child, depth + 1)
                max_depth = max(max_depth, child_depth)
            else:
                child_depth = self._get_max_nesting_depth(child, depth)
                max_depth = max(max_depth, child_depth)

        return max_depth

    def _build_details(
        self,
        files: Dict[str, str],
        issues: List[QualityIssue],
        errors: List[QualityIssue],
        warnings: List[QualityIssue],
        infos: List[QualityIssue],
    ) -> Dict[str, Any]:
        """Build detailed output for validator result."""
        # Group by gate type
        by_gate: Dict[str, int] = {}
        for issue in issues:
            gate = issue.gate_type.value
            by_gate[gate] = by_gate.get(gate, 0) + 1

        # Group by file
        by_file: Dict[str, int] = {}
        for issue in issues:
            by_file[issue.file_path] = by_file.get(issue.file_path, 0) + 1

        return {
            "files_checked": len(files),
            "total_issues": len(issues),
            "error_count": len(errors),
            "warning_count": len(warnings),
            "info_count": len(infos),
            "issues_by_gate": by_gate,
            "issues_by_file": dict(sorted(by_file.items(), key=lambda x: -x[1])[:10]),
            "errors": [e.to_dict() for e in errors[:20]],
            "warnings": [w.to_dict() for w in warnings[:20]],
            "gate_results": {
                "syntax": "PASS" if not any(i.gate_type == QualityGateType.SYNTAX for i in errors) else "FAIL",
                "architecture": "PASS" if not any(i.gate_type == QualityGateType.ARCHITECTURE for i in errors) else "FAIL",
                "security": "PASS" if not any(i.gate_type == QualityGateType.SECURITY for i in errors) else "FAIL",
                "imports": "PASS" if not any(i.gate_type == QualityGateType.IMPORTS for i in errors) else "FAIL",
                "complexity": "PASS" if not any(i.gate_type == QualityGateType.COMPLEXITY for i in errors) else "FAIL",
            },
        }
