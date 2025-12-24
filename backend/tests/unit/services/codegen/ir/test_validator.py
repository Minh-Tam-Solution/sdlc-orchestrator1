"""
Unit tests for IRValidator.

Sprint 46: EP-06 IR-Based Backend Scaffold Generation
ADR-023: IR-Based Deterministic Code Generation

Tests IR validation including:
- Required fields validation
- Naming convention checks
- Semantic constraints
- Normalization

Author: Backend Lead
Date: December 23, 2025
Version: 1.0.0
Status: ACTIVE - Sprint 46 Implementation
"""

import pytest
from typing import Dict, Any

from app.services.codegen.ir.validator import (
    IRValidator,
    IRValidationResult,
    ValidationIssue,
)


class TestIRValidatorBasic:
    """Test basic IRValidator functionality."""

    @pytest.fixture
    def validator(self) -> IRValidator:
        """Create validator without schema files."""
        return IRValidator(schema_dir=None)

    def test_valid_minimal_blueprint(self, validator: IRValidator):
        """Test validation of minimal valid blueprint."""
        blueprint = {
            "name": "Test App",
            "version": "1.0.0",
            "modules": [{
                "name": "items",
                "entities": [{
                    "name": "Item",
                    "fields": [{"name": "title", "type": "string"}]
                }]
            }]
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is True
        assert len([i for i in result.issues if i.severity == "error"]) == 0
        assert result.normalized_ir is not None

    def test_valid_full_blueprint(self, validator: IRValidator):
        """Test validation of full blueprint with all fields."""
        blueprint = {
            "name": "Restaurant Order System",
            "version": "1.0.0",
            "business_domain": "restaurant",
            "database": {
                "type": "postgresql",
                "name": "restaurant_db"
            },
            "modules": [{
                "name": "orders",
                "operations": ["create", "read", "update", "delete", "list"],
                "entities": [{
                    "name": "Order",
                    "table_name": "orders",
                    "fields": [
                        {"name": "table_number", "type": "integer", "required": True},
                        {"name": "status", "type": "string", "required": True, "max_length": 50},
                        {"name": "total", "type": "float"},
                        {"name": "notes", "type": "text"}
                    ]
                }]
            }]
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is True
        assert result.normalized_ir is not None
        assert result.normalized_ir["database"]["type"] == "postgresql"


class TestIRValidatorRequiredFields:
    """Test required field validation."""

    @pytest.fixture
    def validator(self) -> IRValidator:
        return IRValidator(schema_dir=None)

    def test_missing_name(self, validator: IRValidator):
        """Test validation fails when name is missing."""
        blueprint = {
            "version": "1.0.0",
            "modules": [{"name": "items", "entities": []}]
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is False
        assert any("name" in i.path and "missing" in i.message.lower()
                   for i in result.issues)

    def test_missing_version(self, validator: IRValidator):
        """Test validation fails when version is missing."""
        blueprint = {
            "name": "Test App",
            "modules": [{"name": "items", "entities": []}]
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is False
        assert any("version" in i.path for i in result.issues)

    def test_missing_modules(self, validator: IRValidator):
        """Test validation fails when modules is missing."""
        blueprint = {
            "name": "Test App",
            "version": "1.0.0"
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is False
        assert any("modules" in i.path for i in result.issues)

    def test_empty_modules(self, validator: IRValidator):
        """Test validation fails when modules is empty."""
        blueprint = {
            "name": "Test App",
            "version": "1.0.0",
            "modules": []
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is False
        assert any("module" in i.message.lower() for i in result.issues)


class TestIRValidatorVersionFormat:
    """Test version format validation."""

    @pytest.fixture
    def validator(self) -> IRValidator:
        return IRValidator(schema_dir=None)

    def test_valid_semver(self, validator: IRValidator):
        """Test valid semver versions."""
        valid_versions = ["1.0.0", "0.1.0", "10.20.30", "1.0.0-alpha", "1.0.0+build"]

        for version in valid_versions:
            blueprint = {
                "name": "Test",
                "version": version,
                "modules": [{"name": "m", "entities": [{"name": "E", "fields": [{"name": "f", "type": "string"}]}]}]
            }
            result = validator.validate_app_blueprint(blueprint)
            assert result.valid is True, f"Version {version} should be valid"

    def test_invalid_semver(self, validator: IRValidator):
        """Test invalid semver versions."""
        invalid_versions = ["1.0", "v1.0.0", "1", "1.0.0.0"]

        for version in invalid_versions:
            blueprint = {
                "name": "Test",
                "version": version,
                "modules": [{"name": "m", "entities": [{"name": "E", "fields": [{"name": "f", "type": "string"}]}]}]
            }
            result = validator.validate_app_blueprint(blueprint)
            assert any("semver" in i.message.lower() for i in result.issues), \
                f"Version {version} should be invalid"


class TestIRValidatorNamingConventions:
    """Test naming convention validation."""

    @pytest.fixture
    def validator(self) -> IRValidator:
        return IRValidator(schema_dir=None)

    def test_entity_pascal_case_valid(self, validator: IRValidator):
        """Test valid PascalCase entity names."""
        valid_names = ["Order", "OrderItem", "UserProfile", "HTTPRequest"]

        for name in valid_names:
            blueprint = {
                "name": "Test",
                "version": "1.0.0",
                "modules": [{
                    "name": "test",
                    "entities": [{
                        "name": name,
                        "fields": [{"name": "id", "type": "uuid"}]
                    }]
                }]
            }
            result = validator.validate_app_blueprint(blueprint)
            assert result.valid is True, f"Entity name {name} should be valid"

    def test_entity_pascal_case_invalid(self, validator: IRValidator):
        """Test invalid entity names (not PascalCase)."""
        # Note: ALLCAPS like "HTTP" is technically valid PascalCase
        # mixedCase starting lowercase is invalid
        invalid_names = ["order", "order_item", "mixedCase", "lower_case"]

        for name in invalid_names:
            blueprint = {
                "name": "Test",
                "version": "1.0.0",
                "modules": [{
                    "name": "test",
                    "entities": [{
                        "name": name,
                        "fields": [{"name": "id", "type": "uuid"}]
                    }]
                }]
            }
            result = validator.validate_app_blueprint(blueprint)
            assert any("PascalCase" in i.message for i in result.issues), \
                f"Entity name {name} should fail PascalCase check"

    def test_module_snake_case_valid(self, validator: IRValidator):
        """Test valid snake_case module names."""
        valid_names = ["orders", "order_items", "user_profiles"]

        for name in valid_names:
            blueprint = {
                "name": "Test",
                "version": "1.0.0",
                "modules": [{
                    "name": name,
                    "entities": [{"name": "Entity", "fields": [{"name": "f", "type": "string"}]}]
                }]
            }
            result = validator.validate_app_blueprint(blueprint)
            assert result.valid is True, f"Module name {name} should be valid"

    def test_module_snake_case_invalid(self, validator: IRValidator):
        """Test invalid module names (not snake_case)."""
        invalid_names = ["Orders", "orderItems", "Order-Items"]

        for name in invalid_names:
            blueprint = {
                "name": "Test",
                "version": "1.0.0",
                "modules": [{
                    "name": name,
                    "entities": [{"name": "Entity", "fields": [{"name": "f", "type": "string"}]}]
                }]
            }
            result = validator.validate_app_blueprint(blueprint)
            assert any("snake_case" in i.message for i in result.issues), \
                f"Module name {name} should fail snake_case check"

    def test_field_snake_case_valid(self, validator: IRValidator):
        """Test valid snake_case field names."""
        valid_names = ["name", "first_name", "created_at"]

        for name in valid_names:
            blueprint = {
                "name": "Test",
                "version": "1.0.0",
                "modules": [{
                    "name": "test",
                    "entities": [{
                        "name": "Entity",
                        "fields": [{"name": name, "type": "string"}]
                    }]
                }]
            }
            result = validator.validate_app_blueprint(blueprint)
            assert result.valid is True, f"Field name {name} should be valid"


class TestIRValidatorFieldTypes:
    """Test field type validation."""

    @pytest.fixture
    def validator(self) -> IRValidator:
        return IRValidator(schema_dir=None)

    def test_valid_field_types(self, validator: IRValidator):
        """Test all valid field types."""
        valid_types = [
            "string", "text", "integer", "float", "boolean",
            "datetime", "date", "uuid", "json"
        ]

        for field_type in valid_types:
            blueprint = {
                "name": "Test",
                "version": "1.0.0",
                "modules": [{
                    "name": "test",
                    "entities": [{
                        "name": "Entity",
                        "fields": [{"name": "field", "type": field_type}]
                    }]
                }]
            }
            result = validator.validate_app_blueprint(blueprint)
            assert result.valid is True, f"Field type {field_type} should be valid"

    def test_invalid_field_type(self, validator: IRValidator):
        """Test invalid field type."""
        blueprint = {
            "name": "Test",
            "version": "1.0.0",
            "modules": [{
                "name": "test",
                "entities": [{
                    "name": "Entity",
                    "fields": [{"name": "field", "type": "invalid_type"}]
                }]
            }]
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is False
        assert any("invalid" in i.message.lower() and "type" in i.message.lower()
                   for i in result.issues)


class TestIRValidatorNormalization:
    """Test IR normalization."""

    @pytest.fixture
    def validator(self) -> IRValidator:
        return IRValidator(schema_dir=None)

    def test_adds_default_database(self, validator: IRValidator):
        """Test normalization adds default database config."""
        blueprint = {
            "name": "Test App",
            "version": "1.0.0",
            "modules": [{
                "name": "items",
                "entities": [{"name": "Item", "fields": [{"name": "n", "type": "string"}]}]
            }]
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is True
        assert result.normalized_ir["database"]["type"] == "postgresql"
        assert result.normalized_ir["database"]["name"] == "test_app"

    def test_adds_default_operations(self, validator: IRValidator):
        """Test normalization adds default operations."""
        blueprint = {
            "name": "Test",
            "version": "1.0.0",
            "modules": [{
                "name": "items",
                "entities": [{"name": "Item", "fields": [{"name": "n", "type": "string"}]}]
            }]
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is True
        module = result.normalized_ir["modules"][0]
        assert "create" in module["operations"]
        assert "read" in module["operations"]
        assert "update" in module["operations"]
        assert "delete" in module["operations"]
        assert "list" in module["operations"]

    def test_generates_table_name(self, validator: IRValidator):
        """Test normalization generates table name from entity name."""
        blueprint = {
            "name": "Test",
            "version": "1.0.0",
            "modules": [{
                "name": "items",
                "entities": [{"name": "OrderItem", "fields": [{"name": "n", "type": "string"}]}]
            }]
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is True
        entity = result.normalized_ir["modules"][0]["entities"][0]
        assert entity["table_name"] == "order_items"

    def test_adds_id_field(self, validator: IRValidator):
        """Test normalization adds id field if missing."""
        blueprint = {
            "name": "Test",
            "version": "1.0.0",
            "modules": [{
                "name": "items",
                "entities": [{
                    "name": "Item",
                    "fields": [{"name": "name", "type": "string"}]
                }]
            }]
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is True
        fields = result.normalized_ir["modules"][0]["entities"][0]["fields"]
        assert fields[0]["name"] == "id"
        assert fields[0]["type"] == "uuid"
        assert fields[0]["primary"] is True


class TestIRValidatorEdgeCases:
    """Test edge cases and special scenarios."""

    @pytest.fixture
    def validator(self) -> IRValidator:
        return IRValidator(schema_dir=None)

    def test_duplicate_field_names(self, validator: IRValidator):
        """Test validation catches duplicate field names."""
        blueprint = {
            "name": "Test",
            "version": "1.0.0",
            "modules": [{
                "name": "items",
                "entities": [{
                    "name": "Item",
                    "fields": [
                        {"name": "name", "type": "string"},
                        {"name": "name", "type": "string"}
                    ]
                }]
            }]
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is False
        assert any("duplicate" in i.message.lower() for i in result.issues)

    def test_max_length_on_non_string(self, validator: IRValidator):
        """Test warning for max_length on non-string field."""
        blueprint = {
            "name": "Test",
            "version": "1.0.0",
            "modules": [{
                "name": "items",
                "entities": [{
                    "name": "Item",
                    "fields": [
                        {"name": "count", "type": "integer", "max_length": 10}
                    ]
                }]
            }]
        }

        result = validator.validate_app_blueprint(blueprint)

        # Should still be valid but with warning
        assert any("max_length" in i.message and i.severity == "warning"
                   for i in result.issues)

    def test_empty_entity_fields(self, validator: IRValidator):
        """Test validation fails when entity has no fields."""
        blueprint = {
            "name": "Test",
            "version": "1.0.0",
            "modules": [{
                "name": "items",
                "entities": [{
                    "name": "Item",
                    "fields": []
                }]
            }]
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is False
        assert any("field" in i.message.lower() for i in result.issues)

    def test_multiple_modules(self, validator: IRValidator):
        """Test validation of multiple modules."""
        blueprint = {
            "name": "Test",
            "version": "1.0.0",
            "modules": [
                {
                    "name": "products",
                    "entities": [{"name": "Product", "fields": [{"name": "n", "type": "string"}]}]
                },
                {
                    "name": "orders",
                    "entities": [{"name": "Order", "fields": [{"name": "s", "type": "string"}]}]
                }
            ]
        }

        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is True
        assert len(result.normalized_ir["modules"]) == 2
