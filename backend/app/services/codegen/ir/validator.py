"""
IR Validator - JSON Schema validation for AppBlueprint.

Sprint 46: EP-06 IR-Based Backend Scaffold Generation
ADR-023: IR-Based Deterministic Code Generation

Validates IR (Intermediate Representation) against JSON schemas before
processing. Ensures AppBlueprint structure is correct and applies
default values for normalization.

Key Features:
- Required fields validation (name, version, modules)
- Naming conventions (PascalCase for entities, snake_case for fields)
- Semantic constraints (at least one module, field per entity)
- Auto-normalization (defaults, table names, id fields)

Design Reference:
    docs/02-design/14-Technical-Specs/IR-Processor-Specification.md

Author: Backend Lead
Date: December 23, 2025
Version: 1.0.0
Status: ACTIVE - Sprint 46 Implementation
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import re
import logging

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ValidationIssue(BaseModel):
    """Single validation issue."""

    path: str = Field(description="JSON path to the issue location")
    message: str = Field(description="Human-readable error message")
    severity: str = Field(
        default="error",
        description="Issue severity: error, warning, info"
    )


class IRValidationResult(BaseModel):
    """Result of IR validation."""

    valid: bool = Field(description="Whether the IR passed validation")
    issues: List[ValidationIssue] = Field(
        default_factory=list,
        description="List of validation issues found"
    )
    normalized_ir: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Normalized IR with defaults applied (only if valid)"
    )


class IRValidator:
    """
    Validates IR (Intermediate Representation) against JSON schemas.

    This validator checks AppBlueprint structures for:
    - Required fields presence
    - Field type correctness
    - Naming conventions (PascalCase for entities, snake_case for fields)
    - Semantic constraints (at least one module, at least one field per entity)

    Example:
        validator = IRValidator(schema_dir=Path("schemas/"))
        result = validator.validate_app_blueprint({
            "name": "My App",
            "version": "1.0.0",
            "modules": [...]
        })

        if result.valid:
            normalized_ir = result.normalized_ir
        else:
            for issue in result.issues:
                print(f"{issue.path}: {issue.message}")
    """

    # Valid field types in IR
    VALID_FIELD_TYPES = {
        "string", "text", "integer", "float", "boolean",
        "datetime", "date", "uuid", "json"
    }

    # Valid CRUD operations
    VALID_OPERATIONS = {
        "create", "read", "update", "delete", "list", "search"
    }

    # Business domains
    VALID_DOMAINS = {
        "restaurant", "hotel", "retail", "healthcare",
        "education", "logistics", "custom"
    }

    # Database types
    VALID_DB_TYPES = {"postgresql", "mysql", "sqlite"}

    def __init__(self, schema_dir: Optional[Path] = None):
        """
        Initialize validator.

        Args:
            schema_dir: Optional directory containing JSON schemas.
                       If provided, will load schemas from files.
                       Otherwise uses built-in validation rules.
        """
        self.schema_dir = schema_dir
        self._schemas: Dict[str, dict] = {}

        if schema_dir and schema_dir.exists():
            self._load_schemas()

    def _load_schemas(self) -> None:
        """Load JSON schemas from schema directory."""
        schema_files = [
            "app_blueprint.schema.json",
            "module_spec.schema.json",
            "data_model.schema.json",
            "page_spec.schema.json"
        ]

        for filename in schema_files:
            path = self.schema_dir / filename
            if path.exists():
                try:
                    with open(path, encoding="utf-8") as f:
                        name = filename.replace(".schema.json", "")
                        self._schemas[name] = json.load(f)
                        logger.debug(f"Loaded schema: {name}")
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to load schema {filename}: {e}")

    def validate_app_blueprint(
        self,
        blueprint: Dict[str, Any]
    ) -> IRValidationResult:
        """
        Validate an AppBlueprint against schema.

        This method performs comprehensive validation including:
        1. Required fields check (name, version, modules)
        2. Version format validation (semver)
        3. Module validation (name, entities, operations)
        4. Entity validation (name, fields, relationships)
        5. Field validation (name, type, constraints)

        Args:
            blueprint: Raw AppBlueprint dictionary

        Returns:
            IRValidationResult with valid status, issues, and normalized IR

        Example:
            result = validator.validate_app_blueprint({
                "name": "Restaurant App",
                "version": "1.0.0",
                "modules": [{
                    "name": "orders",
                    "entities": [{
                        "name": "Order",
                        "fields": [{"name": "status", "type": "string"}]
                    }]
                }]
            })
        """
        issues: List[ValidationIssue] = []

        try:
            # Validate top-level required fields
            issues.extend(self._validate_required_fields(blueprint))

            # Validate version format
            issues.extend(self._validate_version(blueprint.get("version")))

            # Validate business domain if provided
            if "business_domain" in blueprint:
                issues.extend(self._validate_domain(blueprint["business_domain"]))

            # Validate database config if provided
            if "database" in blueprint:
                issues.extend(self._validate_database(blueprint["database"]))

            # Validate modules
            modules = blueprint.get("modules", [])
            if not modules:
                issues.append(ValidationIssue(
                    path="modules",
                    message="At least one module is required"
                ))
            else:
                for i, module in enumerate(modules):
                    module_issues = self._validate_module(module, f"modules[{i}]")
                    issues.extend(module_issues)

            # If any errors, return invalid result
            if any(i.severity == "error" for i in issues):
                return IRValidationResult(
                    valid=False,
                    issues=issues,
                    normalized_ir=None
                )

            # Normalize and return
            normalized = self._normalize_blueprint(blueprint)
            return IRValidationResult(
                valid=True,
                issues=[i for i in issues if i.severity != "error"],
                normalized_ir=normalized
            )

        except Exception as e:
            logger.exception(f"Validation error: {e}")
            return IRValidationResult(
                valid=False,
                issues=[ValidationIssue(
                    path="",
                    message=f"Validation failed: {str(e)}"
                )]
            )

    def _validate_required_fields(
        self,
        blueprint: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """Validate required top-level fields."""
        issues = []

        required_fields = ["name", "version", "modules"]
        for field in required_fields:
            if field not in blueprint:
                issues.append(ValidationIssue(
                    path=field,
                    message=f"Required field '{field}' is missing"
                ))
            elif not blueprint[field]:
                issues.append(ValidationIssue(
                    path=field,
                    message=f"Required field '{field}' cannot be empty"
                ))

        # Validate name format
        name = blueprint.get("name", "")
        if name and not self._is_valid_app_name(name):
            issues.append(ValidationIssue(
                path="name",
                message=f"App name must be 1-100 characters, alphanumeric with spaces allowed: {name}",
                severity="warning"
            ))

        return issues

    def _validate_version(self, version: Optional[str]) -> List[ValidationIssue]:
        """Validate version is semver format."""
        issues = []

        if version:
            semver_pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?(\+[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?$"
            if not re.match(semver_pattern, version):
                issues.append(ValidationIssue(
                    path="version",
                    message=f"Version must be semver format (e.g., 1.0.0), got: {version}"
                ))

        return issues

    def _validate_domain(self, domain: str) -> List[ValidationIssue]:
        """Validate business domain."""
        issues = []

        if domain not in self.VALID_DOMAINS:
            issues.append(ValidationIssue(
                path="business_domain",
                message=f"Invalid domain '{domain}'. Valid: {sorted(self.VALID_DOMAINS)}",
                severity="warning"
            ))

        return issues

    def _validate_database(self, database: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate database configuration."""
        issues = []

        db_type = database.get("type")
        if db_type and db_type not in self.VALID_DB_TYPES:
            issues.append(ValidationIssue(
                path="database.type",
                message=f"Invalid database type '{db_type}'. Valid: {sorted(self.VALID_DB_TYPES)}"
            ))

        return issues

    def _validate_module(
        self,
        module: Dict[str, Any],
        path_prefix: str
    ) -> List[ValidationIssue]:
        """Validate a module specification."""
        issues = []

        # Required: name
        if "name" not in module:
            issues.append(ValidationIssue(
                path=f"{path_prefix}.name",
                message="Module must have a name"
            ))
        else:
            name = module["name"]
            if not self._is_snake_case(name):
                issues.append(ValidationIssue(
                    path=f"{path_prefix}.name",
                    message=f"Module name must be snake_case, got: {name}"
                ))

        # Required: entities
        entities = module.get("entities", [])
        if not entities:
            issues.append(ValidationIssue(
                path=f"{path_prefix}.entities",
                message="Module must have at least one entity"
            ))
        else:
            for i, entity in enumerate(entities):
                entity_issues = self._validate_entity(
                    entity,
                    f"{path_prefix}.entities[{i}]"
                )
                issues.extend(entity_issues)

        # Optional: operations
        operations = module.get("operations", [])
        for op in operations:
            if op not in self.VALID_OPERATIONS:
                issues.append(ValidationIssue(
                    path=f"{path_prefix}.operations",
                    message=f"Invalid operation '{op}'. Valid: {sorted(self.VALID_OPERATIONS)}",
                    severity="warning"
                ))

        return issues

    def _validate_entity(
        self,
        entity: Dict[str, Any],
        path_prefix: str
    ) -> List[ValidationIssue]:
        """Validate an entity/data model specification."""
        issues = []

        # Required: name
        if "name" not in entity:
            issues.append(ValidationIssue(
                path=f"{path_prefix}.name",
                message="Entity must have a name"
            ))
        else:
            name = entity["name"]
            if not self._is_pascal_case(name):
                issues.append(ValidationIssue(
                    path=f"{path_prefix}.name",
                    message=f"Entity name must be PascalCase, got: {name}"
                ))

        # Optional: table_name
        table_name = entity.get("table_name")
        if table_name and not self._is_snake_case(table_name):
            issues.append(ValidationIssue(
                path=f"{path_prefix}.table_name",
                message=f"Table name must be snake_case, got: {table_name}",
                severity="warning"
            ))

        # Required: fields
        fields = entity.get("fields", [])
        if not fields:
            issues.append(ValidationIssue(
                path=f"{path_prefix}.fields",
                message="Entity must have at least one field"
            ))
        else:
            field_names = set()
            for i, field in enumerate(fields):
                field_issues = self._validate_field(
                    field,
                    f"{path_prefix}.fields[{i}]"
                )
                issues.extend(field_issues)

                # Check for duplicate field names
                field_name = field.get("name")
                if field_name:
                    if field_name in field_names:
                        issues.append(ValidationIssue(
                            path=f"{path_prefix}.fields[{i}].name",
                            message=f"Duplicate field name: {field_name}"
                        ))
                    field_names.add(field_name)

        # Optional: relationships
        for i, rel in enumerate(entity.get("relationships", [])):
            rel_issues = self._validate_relationship(
                rel,
                f"{path_prefix}.relationships[{i}]"
            )
            issues.extend(rel_issues)

        return issues

    def _validate_field(
        self,
        field: Dict[str, Any],
        path_prefix: str
    ) -> List[ValidationIssue]:
        """Validate a field specification."""
        issues = []

        # Required: name
        if "name" not in field:
            issues.append(ValidationIssue(
                path=f"{path_prefix}.name",
                message="Field must have a name"
            ))
        else:
            name = field["name"]
            if not self._is_snake_case(name):
                issues.append(ValidationIssue(
                    path=f"{path_prefix}.name",
                    message=f"Field name must be snake_case, got: {name}"
                ))

        # Required: type
        if "type" not in field:
            issues.append(ValidationIssue(
                path=f"{path_prefix}.type",
                message="Field must have a type"
            ))
        else:
            field_type = field["type"]
            if field_type not in self.VALID_FIELD_TYPES:
                issues.append(ValidationIssue(
                    path=f"{path_prefix}.type",
                    message=f"Invalid field type '{field_type}'. Valid: {sorted(self.VALID_FIELD_TYPES)}"
                ))

        # Optional: max_length (only for string/text)
        max_length = field.get("max_length")
        if max_length is not None:
            if field.get("type") not in {"string", "text"}:
                issues.append(ValidationIssue(
                    path=f"{path_prefix}.max_length",
                    message="max_length only applies to string/text types",
                    severity="warning"
                ))
            elif not isinstance(max_length, int) or max_length < 1:
                issues.append(ValidationIssue(
                    path=f"{path_prefix}.max_length",
                    message=f"max_length must be positive integer, got: {max_length}"
                ))

        return issues

    def _validate_relationship(
        self,
        rel: Dict[str, Any],
        path_prefix: str
    ) -> List[ValidationIssue]:
        """Validate a relationship specification."""
        issues = []

        valid_types = {"one_to_many", "many_to_one", "one_to_one", "many_to_many"}

        if "type" not in rel:
            issues.append(ValidationIssue(
                path=f"{path_prefix}.type",
                message="Relationship must have a type"
            ))
        elif rel["type"] not in valid_types:
            issues.append(ValidationIssue(
                path=f"{path_prefix}.type",
                message=f"Invalid relationship type. Valid: {sorted(valid_types)}"
            ))

        if "target" not in rel:
            issues.append(ValidationIssue(
                path=f"{path_prefix}.target",
                message="Relationship must have a target entity"
            ))

        return issues

    def _normalize_blueprint(
        self,
        blueprint: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Normalize blueprint by applying defaults.

        This ensures consistent structure for downstream processors.
        """
        normalized = blueprint.copy()

        # Set database defaults
        if "database" not in normalized:
            normalized["database"] = {
                "type": "postgresql",
                "name": self._to_snake_case(blueprint["name"])
            }
        else:
            if "type" not in normalized["database"]:
                normalized["database"]["type"] = "postgresql"
            if "name" not in normalized["database"]:
                normalized["database"]["name"] = self._to_snake_case(blueprint["name"])

        # Normalize modules
        normalized["modules"] = []
        for module in blueprint.get("modules", []):
            norm_module = module.copy()

            # Set default operations
            if "operations" not in norm_module:
                norm_module["operations"] = ["create", "read", "update", "delete", "list"]

            # Normalize entities
            norm_module["entities"] = []
            for entity in module.get("entities", []):
                norm_entity = entity.copy()

                # Generate table_name if not provided
                if "table_name" not in norm_entity:
                    norm_entity["table_name"] = self._to_table_name(entity["name"])

                # Add id field if not present
                field_names = {f.get("name") for f in entity.get("fields", [])}
                if "id" not in field_names:
                    norm_entity["fields"] = [
                        {"name": "id", "type": "uuid", "required": True, "primary": True}
                    ] + entity.get("fields", [])
                else:
                    norm_entity["fields"] = entity.get("fields", [])

                # Normalize field defaults
                for field in norm_entity["fields"]:
                    if "required" not in field:
                        field["required"] = False
                    if "unique" not in field:
                        field["unique"] = False
                    if "indexed" not in field:
                        field["indexed"] = False

                norm_module["entities"].append(norm_entity)

            normalized["modules"].append(norm_module)

        return normalized

    # ========================================================================
    # Helper Methods
    # ========================================================================

    def _is_pascal_case(self, name: str) -> bool:
        """Check if name is PascalCase."""
        if not name:
            return False
        # Must start with uppercase, contain only alphanumeric
        return bool(re.match(r"^[A-Z][a-zA-Z0-9]*$", name))

    def _is_snake_case(self, name: str) -> bool:
        """Check if name is snake_case."""
        if not name:
            return False
        return bool(re.match(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$", name))

    def _is_valid_app_name(self, name: str) -> bool:
        """Check if app name is valid (alphanumeric with spaces)."""
        if not name or len(name) > 100:
            return False
        return bool(re.match(r"^[a-zA-Z0-9][a-zA-Z0-9 _-]*$", name))

    def _to_snake_case(self, name: str) -> str:
        """Convert name to snake_case."""
        # Remove special chars, convert spaces/dashes to underscores
        result = re.sub(r"[^a-zA-Z0-9]", "_", name)
        # Insert underscore before uppercase letters
        result = re.sub(r"([a-z])([A-Z])", r"\1_\2", result)
        # Collapse multiple underscores and lowercase
        result = re.sub(r"_+", "_", result).lower().strip("_")
        return result or "app"

    def _to_table_name(self, entity_name: str) -> str:
        """Convert PascalCase entity name to plural snake_case table name."""
        # PascalCase -> snake_case
        snake = self._to_snake_case(entity_name)
        # Simple pluralization (add 's')
        if snake.endswith("s") or snake.endswith("x") or snake.endswith("ch"):
            return snake + "es"
        elif snake.endswith("y"):
            return snake[:-1] + "ies"
        else:
            return snake + "s"
