"""
Base Domain Template Classes.

Sprint 47: Vietnamese SME Domain Templates
ADR-023: IR-Based Deterministic Code Generation

Provides base classes for domain-specific templates that can be
converted to AppBlueprint/IR format for code generation.

Author: Backend Lead
Date: December 23, 2025
Version: 1.0.0
Status: ACTIVE - Sprint 47 Implementation
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Type
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class FieldType(str, Enum):
    """Supported field types in IR."""
    STRING = "string"
    TEXT = "text"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    DATE = "date"
    UUID = "uuid"
    JSON = "json"


class RelationType(str, Enum):
    """Supported relationship types."""
    ONE_TO_MANY = "one_to_many"
    MANY_TO_ONE = "many_to_one"
    ONE_TO_ONE = "one_to_one"
    MANY_TO_MANY = "many_to_many"


@dataclass
class DomainField:
    """
    Domain field definition with Vietnamese localization.

    Attributes:
        name: Field name in snake_case (English)
        field_type: IR field type
        vietnamese_name: Vietnamese label for UI
        description: Vietnamese description for documentation
        required: Whether field is required
        max_length: Max length for string/text fields
        min_value: Minimum value for numeric fields
        max_value: Maximum value for numeric fields
        default: Default value
        unique: Whether field must be unique
        indexed: Whether field should be indexed
        choices: List of valid choices for enum-like fields
    """
    name: str
    field_type: FieldType
    vietnamese_name: str
    description: str = ""
    required: bool = False
    max_length: Optional[int] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    default: Optional[Any] = None
    unique: bool = False
    indexed: bool = False
    choices: Optional[List[str]] = None

    def to_ir_dict(self) -> Dict[str, Any]:
        """Convert to IR field dictionary."""
        result: Dict[str, Any] = {
            "name": self.name,
            "type": self.field_type.value,
            "required": self.required,
        }

        # Optional attributes
        if self.max_length is not None:
            result["max_length"] = self.max_length
        if self.min_value is not None:
            result["min_value"] = self.min_value
        if self.max_value is not None:
            result["max_value"] = self.max_value
        if self.default is not None:
            result["default"] = self.default
        if self.unique:
            result["unique"] = True
        if self.indexed:
            result["indexed"] = True
        if self.choices:
            result["choices"] = self.choices

        # Vietnamese metadata for UI/docs
        result["_meta"] = {
            "vietnamese_name": self.vietnamese_name,
            "description": self.description,
        }

        return result


@dataclass
class DomainRelationship:
    """
    Domain relationship definition.

    Attributes:
        name: Relationship name (for back_populates)
        target: Target entity name (PascalCase)
        relation_type: Type of relationship
        vietnamese_name: Vietnamese label
        description: Vietnamese description
        cascade: Cascade delete behavior
    """
    name: str
    target: str
    relation_type: RelationType
    vietnamese_name: str
    description: str = ""
    cascade: bool = False

    def to_ir_dict(self) -> Dict[str, Any]:
        """Convert to IR relationship dictionary."""
        return {
            "name": self.name,
            "target": self.target,
            "type": self.relation_type.value,
            "cascade": self.cascade,
            "_meta": {
                "vietnamese_name": self.vietnamese_name,
                "description": self.description,
            },
        }


@dataclass
class DomainEntity:
    """
    Domain entity definition with Vietnamese localization.

    Attributes:
        name: Entity name in PascalCase (English)
        vietnamese_name: Vietnamese name for UI
        description: Vietnamese description
        fields: List of entity fields
        relationships: List of entity relationships
        table_name: Custom table name (auto-generated if not set)
        soft_delete: Whether to use soft delete
        timestamps: Whether to include created_at/updated_at
    """
    name: str
    vietnamese_name: str
    description: str
    fields: List[DomainField] = field(default_factory=list)
    relationships: List[DomainRelationship] = field(default_factory=list)
    table_name: Optional[str] = None
    soft_delete: bool = True
    timestamps: bool = True

    def to_ir_dict(self) -> Dict[str, Any]:
        """Convert to IR entity dictionary."""
        result: Dict[str, Any] = {
            "name": self.name,
            "fields": [f.to_ir_dict() for f in self.fields],
        }

        if self.table_name:
            result["table_name"] = self.table_name

        if self.relationships:
            result["relationships"] = [r.to_ir_dict() for r in self.relationships]

        # Vietnamese metadata
        result["_meta"] = {
            "vietnamese_name": self.vietnamese_name,
            "description": self.description,
            "soft_delete": self.soft_delete,
            "timestamps": self.timestamps,
        }

        return result


@dataclass
class DomainModule:
    """
    Domain module grouping related entities.

    Attributes:
        name: Module name in snake_case
        vietnamese_name: Vietnamese module name
        description: Vietnamese description
        entities: List of entities in this module
        operations: CRUD operations supported
    """
    name: str
    vietnamese_name: str
    description: str
    entities: List[DomainEntity] = field(default_factory=list)
    operations: List[str] = field(default_factory=lambda: [
        "create", "read", "update", "delete", "list"
    ])

    def to_ir_dict(self) -> Dict[str, Any]:
        """Convert to IR module dictionary."""
        return {
            "name": self.name,
            "operations": self.operations,
            "entities": [e.to_ir_dict() for e in self.entities],
            "_meta": {
                "vietnamese_name": self.vietnamese_name,
                "description": self.description,
            },
        }


class DomainTemplate(ABC):
    """
    Abstract base class for domain templates.

    Each domain template provides:
    - Pre-defined entities for the domain
    - Vietnamese localization
    - Industry-specific business logic
    - Validation rules

    Subclasses must implement:
    - domain_name: Unique domain identifier
    - vietnamese_name: Vietnamese domain name
    - description: Vietnamese description
    - get_modules(): Returns list of domain modules
    """

    @property
    @abstractmethod
    def domain_name(self) -> str:
        """Unique domain identifier (e.g., 'restaurant', 'hotel')."""
        pass

    @property
    @abstractmethod
    def vietnamese_name(self) -> str:
        """Vietnamese name for the domain."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Vietnamese description of the domain."""
        pass

    @property
    def version(self) -> str:
        """Template version."""
        return "1.0.0"

    @abstractmethod
    def get_modules(self) -> List[DomainModule]:
        """Get all modules for this domain."""
        pass

    def get_entities(self) -> List[DomainEntity]:
        """Get all entities across all modules."""
        entities = []
        for module in self.get_modules():
            entities.extend(module.entities)
        return entities

    def get_entity_by_name(self, name: str) -> Optional[DomainEntity]:
        """Get entity by name."""
        for entity in self.get_entities():
            if entity.name == name:
                return entity
        return None

    def to_app_blueprint(
        self,
        app_name: str,
        app_version: str = "1.0.0",
        selected_modules: Optional[List[str]] = None,
        selected_entities: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Convert domain template to AppBlueprint format.

        Args:
            app_name: Application name (Vietnamese allowed)
            app_version: Semantic version string
            selected_modules: Optional list of module names to include
            selected_entities: Optional list of entity names to include

        Returns:
            AppBlueprint dictionary ready for IR validation
        """
        modules = self.get_modules()

        # Filter modules if specified
        if selected_modules:
            modules = [m for m in modules if m.name in selected_modules]

        # Filter entities if specified
        if selected_entities:
            for module in modules:
                module.entities = [
                    e for e in module.entities
                    if e.name in selected_entities
                ]
            # Remove empty modules
            modules = [m for m in modules if m.entities]

        blueprint: Dict[str, Any] = {
            "name": app_name,
            "version": app_version,
            "business_domain": self.domain_name,
            "modules": [m.to_ir_dict() for m in modules],
            "_meta": {
                "template_name": self.domain_name,
                "template_version": self.version,
                "vietnamese_name": self.vietnamese_name,
                "description": self.description,
            },
        }

        return blueprint

    def get_quick_start_blueprint(self, app_name: str) -> Dict[str, Any]:
        """
        Get minimal quick-start blueprint with core entities only.

        This is used for fast onboarding - includes only essential entities.
        """
        return self.to_app_blueprint(app_name)


class DomainRegistry:
    """
    Registry for domain templates.

    Provides centralized access to all available domain templates.
    """

    _templates: Dict[str, Type[DomainTemplate]] = {}
    _instances: Dict[str, DomainTemplate] = {}

    @classmethod
    def register(cls, template_class: Type[DomainTemplate]) -> Type[DomainTemplate]:
        """
        Register a domain template class.

        Can be used as a decorator:
            @DomainRegistry.register
            class MyDomainTemplate(DomainTemplate):
                ...
        """
        # Create instance to get domain_name
        instance = template_class()
        cls._templates[instance.domain_name] = template_class
        cls._instances[instance.domain_name] = instance
        logger.info(f"Registered domain template: {instance.domain_name}")
        return template_class

    @classmethod
    def get(cls, domain_name: str) -> Optional[DomainTemplate]:
        """Get domain template by name."""
        return cls._instances.get(domain_name)

    @classmethod
    def get_all(cls) -> Dict[str, DomainTemplate]:
        """Get all registered domain templates."""
        return cls._instances.copy()

    @classmethod
    def list_domains(cls) -> List[Dict[str, str]]:
        """List all available domains with Vietnamese names."""
        return [
            {
                "domain": name,
                "vietnamese_name": template.vietnamese_name,
                "description": template.description,
                "version": template.version,
            }
            for name, template in cls._instances.items()
        ]

    @classmethod
    def get_blueprint(
        cls,
        domain_name: str,
        app_name: str,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Get AppBlueprint for a domain.

        Args:
            domain_name: Domain identifier
            app_name: Application name
            **kwargs: Additional options passed to to_app_blueprint

        Returns:
            AppBlueprint dictionary or None if domain not found
        """
        template = cls.get(domain_name)
        if template:
            return template.to_app_blueprint(app_name, **kwargs)
        return None
