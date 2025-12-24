"""
IR Processor Base - Abstract base class for code processors.

Sprint 46: EP-06 IR-Based Backend Scaffold Generation
ADR-023: IR-Based Deterministic Code Generation

Provides abstract base class and common functionality for all IR processors.
Each processor transforms part of the IR into generated code files using
Jinja2 templates.

Key Classes:
- GeneratedFile: Single generated file with path and content
- ProcessorResult: Result from processing with files and errors
- IRProcessor: Abstract base class for all processors
- CompositeProcessor: Groups multiple processors together

Design Reference:
    docs/02-design/14-Technical-Specs/IR-Processor-Specification.md

Author: Backend Lead
Date: December 23, 2025
Version: 1.0.0
Status: ACTIVE - Sprint 46 Implementation
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

from pydantic import BaseModel, Field
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound

logger = logging.getLogger(__name__)


class GeneratedFile(BaseModel):
    """
    Single generated file.

    Represents a file that will be written to the output bundle.
    """

    path: str = Field(
        description="Relative path within output bundle (e.g., 'app/main.py')"
    )
    content: str = Field(
        description="File content"
    )
    language: str = Field(
        default="python",
        description="File language for syntax highlighting/validation"
    )


class ProcessorResult(BaseModel):
    """
    Result from an IR processor.

    Contains generated files and any errors encountered.
    """

    success: bool = Field(
        description="Whether processing completed without errors"
    )
    files: List[GeneratedFile] = Field(
        default_factory=list,
        description="List of generated files"
    )
    errors: List[str] = Field(
        default_factory=list,
        description="List of error messages if any"
    )
    warnings: List[str] = Field(
        default_factory=list,
        description="List of warning messages"
    )

    @property
    def file_count(self) -> int:
        """Number of files generated."""
        return len(self.files)

    @property
    def total_lines(self) -> int:
        """Total lines of code generated."""
        return sum(len(f.content.split("\n")) for f in self.files)


class IRProcessor(ABC):
    """
    Abstract base class for IR processors.

    Each processor transforms part of the IR (AppBlueprint) into
    generated code files using Jinja2 templates.

    Subclasses must implement:
    - name property: Processor identifier
    - process method: Main processing logic

    Example implementation:
        class ModelProcessor(IRProcessor):
            @property
            def name(self) -> str:
                return "model"

            def process(self, ir: Dict[str, Any]) -> ProcessorResult:
                files = []
                for entity in self._get_entities(ir):
                    content = self.render_template("model.py.j2", {"entity": entity})
                    files.append(GeneratedFile(path=f"app/models/{entity['table_name']}.py", content=content))
                return ProcessorResult(success=True, files=files)
    """

    # Mapping from IR field types to (SQLAlchemy type, Python type)
    TYPE_MAP: Dict[str, tuple] = {
        "string": ("String", "str"),
        "text": ("Text", "str"),
        "integer": ("Integer", "int"),
        "float": ("Float", "float"),
        "boolean": ("Boolean", "bool"),
        "datetime": ("DateTime", "datetime"),
        "date": ("Date", "date"),
        "uuid": ("UUID", "UUID"),
        "json": ("JSON", "dict"),
    }

    def __init__(self, template_dir: Path):
        """
        Initialize processor with template directory.

        Args:
            template_dir: Path to directory containing Jinja2 templates
        """
        self.template_dir = template_dir
        self._jinja_env: Optional[Environment] = None

    @property
    def jinja_env(self) -> Environment:
        """Lazy-loaded Jinja2 environment."""
        if self._jinja_env is None:
            self._jinja_env = self._create_jinja_env()
        return self._jinja_env

    def _create_jinja_env(self) -> Environment:
        """Create Jinja2 environment with custom filters."""
        env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

        # Add custom filters
        env.filters["snake_case"] = self._to_snake_case
        env.filters["pascal_case"] = self._to_pascal_case
        env.filters["camel_case"] = self._to_camel_case
        env.filters["pluralize"] = self._pluralize
        env.filters["singularize"] = self._singularize
        env.filters["sqlalchemy_type"] = self._to_sqlalchemy_type
        env.filters["python_type"] = self._to_python_type

        # Add globals
        env.globals["type_map"] = self.TYPE_MAP

        return env

    @property
    @abstractmethod
    def name(self) -> str:
        """Processor name for logging and identification."""
        pass

    @abstractmethod
    def process(self, ir: Dict[str, Any]) -> ProcessorResult:
        """
        Process IR and generate files.

        Args:
            ir: Normalized IR (AppBlueprint) from validator

        Returns:
            ProcessorResult with generated files and errors
        """
        pass

    def render_template(
        self,
        template_name: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Render a Jinja2 template with context.

        Args:
            template_name: Template filename (e.g., "main.py.j2")
            context: Template context variables

        Returns:
            Rendered template content

        Raises:
            TemplateNotFound: If template file doesn't exist
        """
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except TemplateNotFound:
            logger.error(f"Template not found: {template_name}")
            raise

    def render_string(
        self,
        template_string: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Render a template string with context.

        Useful for inline templates or testing.

        Args:
            template_string: Jinja2 template as string
            context: Template context variables

        Returns:
            Rendered content
        """
        template = self.jinja_env.from_string(template_string)
        return template.render(**context)

    # ========================================================================
    # Helper Methods for Subclasses
    # ========================================================================

    def _get_all_entities(self, ir: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract all entities from all modules with module metadata."""
        entities = []
        for module in ir.get("modules", []):
            for entity in module.get("entities", []):
                entities.append({
                    **entity,
                    "module_name": module["name"],
                    "module_operations": module.get("operations", [])
                })
        return entities

    def _get_all_modules(self, ir: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract all modules."""
        return ir.get("modules", [])

    def _get_app_name(self, ir: Dict[str, Any]) -> str:
        """Get application name."""
        return ir.get("name", "Generated App")

    def _get_database_config(self, ir: Dict[str, Any]) -> Dict[str, Any]:
        """Get database configuration."""
        return ir.get("database", {"type": "postgresql", "name": "app"})

    # ========================================================================
    # String Transformation Filters
    # ========================================================================

    @staticmethod
    def _to_snake_case(name: str) -> str:
        """Convert to snake_case."""
        import re
        # Handle empty string
        if not name:
            return ""
        # Insert underscore before uppercase letters
        result = re.sub(r"([a-z])([A-Z])", r"\1_\2", name)
        # Replace spaces and dashes with underscores
        result = re.sub(r"[-\s]+", "_", result)
        # Remove non-alphanumeric except underscores
        result = re.sub(r"[^a-zA-Z0-9_]", "", result)
        return result.lower()

    @staticmethod
    def _to_pascal_case(name: str) -> str:
        """Convert to PascalCase."""
        import re
        if not name:
            return ""
        # Split by underscores, spaces, dashes
        words = re.split(r"[-_\s]+", name)
        return "".join(word.capitalize() for word in words)

    @staticmethod
    def _to_camel_case(name: str) -> str:
        """Convert to camelCase."""
        pascal = IRProcessor._to_pascal_case(name)
        if pascal:
            return pascal[0].lower() + pascal[1:]
        return ""

    @staticmethod
    def _pluralize(word: str) -> str:
        """Simple pluralization."""
        if not word:
            return ""
        if word.endswith("s") or word.endswith("x") or word.endswith("ch") or word.endswith("sh"):
            return word + "es"
        elif word.endswith("y") and len(word) > 1 and word[-2] not in "aeiou":
            return word[:-1] + "ies"
        else:
            return word + "s"

    @staticmethod
    def _singularize(word: str) -> str:
        """Simple singularization."""
        if not word:
            return ""
        if word.endswith("ies"):
            return word[:-3] + "y"
        elif word.endswith("es") and (word.endswith("sses") or word.endswith("xes") or word.endswith("ches") or word.endswith("shes")):
            return word[:-2]
        elif word.endswith("s") and not word.endswith("ss"):
            return word[:-1]
        return word

    def _to_sqlalchemy_type(self, ir_type: str) -> str:
        """Convert IR type to SQLAlchemy type."""
        sa_type, _ = self.TYPE_MAP.get(ir_type, ("String", "str"))
        return sa_type

    def _to_python_type(self, ir_type: str) -> str:
        """Convert IR type to Python type."""
        _, py_type = self.TYPE_MAP.get(ir_type, ("String", "str"))
        return py_type


class CompositeProcessor(IRProcessor):
    """
    Composite processor that runs multiple processors in sequence.

    Useful for grouping related processors together.
    """

    def __init__(self, processors: List[IRProcessor], name: str = "composite"):
        """
        Initialize with list of processors.

        Note: Does not call parent __init__ as template_dir is not needed.
        """
        self._processors = processors
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def process(self, ir: Dict[str, Any]) -> ProcessorResult:
        """Run all processors and combine results."""
        all_files: List[GeneratedFile] = []
        all_errors: List[str] = []
        all_warnings: List[str] = []

        for processor in self._processors:
            logger.info(f"Running processor: {processor.name}")
            result = processor.process(ir)
            all_files.extend(result.files)
            all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)

        return ProcessorResult(
            success=len(all_errors) == 0,
            files=all_files,
            errors=all_errors,
            warnings=all_warnings,
        )
