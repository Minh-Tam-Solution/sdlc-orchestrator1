"""
Unit tests for IR-based codegen API endpoints.

Sprint 46: EP-06 IR-Based Backend Scaffold Generation
ADR-023: IR-Based Deterministic Code Generation

Tests API endpoints:
- POST /codegen/ir/generate
- POST /codegen/ir/validate

Author: Backend Lead
Date: December 23, 2025
Version: 1.0.0
Status: ACTIVE - Sprint 46 Implementation
"""

import pytest
from typing import Dict, Any


@pytest.fixture
def minimal_blueprint() -> Dict[str, Any]:
    """Minimal valid blueprint."""
    return {
        "name": "Test App",
        "version": "1.0.0",
        "modules": [{
            "name": "items",
            "entities": [{
                "name": "Item",
                "fields": [
                    {"name": "name", "type": "string", "required": True},
                    {"name": "description", "type": "text"}
                ]
            }]
        }]
    }


@pytest.fixture
def restaurant_blueprint() -> Dict[str, Any]:
    """Restaurant app blueprint for testing."""
    return {
        "name": "Restaurant Management",
        "version": "1.0.0",
        "business_domain": "restaurant",
        "modules": [
            {
                "name": "products",
                "operations": ["create", "read", "list", "update", "delete"],
                "entities": [{
                    "name": "Product",
                    "fields": [
                        {"name": "name", "type": "string", "required": True, "max_length": 100},
                        {"name": "price", "type": "float", "required": True},
                        {"name": "description", "type": "text"},
                        {"name": "active", "type": "boolean"}
                    ]
                }]
            },
            {
                "name": "orders",
                "operations": ["create", "read", "list", "update"],
                "entities": [{
                    "name": "Order",
                    "fields": [
                        {"name": "table_number", "type": "integer", "required": True},
                        {"name": "status", "type": "string", "required": True},
                        {"name": "total", "type": "float"},
                        {"name": "notes", "type": "text"}
                    ]
                }]
            }
        ]
    }


class TestIRValidateEndpoint:
    """Test /codegen/ir/validate endpoint logic."""

    def test_validate_valid_blueprint(self, minimal_blueprint: Dict[str, Any]):
        """Test validation of valid blueprint."""
        from app.services.codegen.ir import IRValidator

        validator = IRValidator()
        result = validator.validate_app_blueprint(minimal_blueprint)

        assert result.valid is True
        assert len(result.issues) == 0
        assert result.normalized_ir is not None
        assert result.normalized_ir["name"] == "Test App"

    def test_validate_invalid_blueprint_missing_name(self):
        """Test validation fails for missing name."""
        from app.services.codegen.ir import IRValidator

        blueprint = {
            "version": "1.0.0",
            "modules": [{
                "name": "test",
                "entities": [{
                    "name": "Test",
                    "fields": [{"name": "id", "type": "uuid"}]
                }]
            }]
        }

        validator = IRValidator()
        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is False
        error_messages = [i.message for i in result.issues]
        assert any("name" in msg.lower() for msg in error_messages)

    def test_validate_invalid_entity_name(self):
        """Test validation fails for invalid entity name."""
        from app.services.codegen.ir import IRValidator

        blueprint = {
            "name": "Test",
            "version": "1.0.0",
            "modules": [{
                "name": "test",
                "entities": [{
                    "name": "invalid_name",  # Should be PascalCase
                    "fields": [{"name": "id", "type": "uuid"}]
                }]
            }]
        }

        validator = IRValidator()
        result = validator.validate_app_blueprint(blueprint)

        assert result.valid is False

    def test_validation_normalizes_blueprint(self, minimal_blueprint: Dict[str, Any]):
        """Test that validation normalizes the blueprint."""
        from app.services.codegen.ir import IRValidator

        validator = IRValidator()
        result = validator.validate_app_blueprint(minimal_blueprint)

        assert result.valid is True
        normalized = result.normalized_ir

        # Check default values were applied
        assert "database" in normalized
        assert normalized["database"]["type"] == "postgresql"

        # Check entity has table_name
        entity = normalized["modules"][0]["entities"][0]
        assert "table_name" in entity
        assert entity["table_name"] == "items"


class TestIRGenerateEndpoint:
    """Test /codegen/ir/generate endpoint logic."""

    def test_generate_minimal_app(self, minimal_blueprint: Dict[str, Any]):
        """Test generating minimal application."""
        from pathlib import Path
        from app.services.codegen.ir import BundleBuilder, IRValidator

        # Validate first
        validator = IRValidator()
        validation = validator.validate_app_blueprint(minimal_blueprint)
        assert validation.valid is True

        # Generate
        template_dir = Path(__file__).parent.parent.parent.parent / \
            "app" / "services" / "codegen" / "templates"
        builder = BundleBuilder(template_dir=template_dir)
        bundle = builder.build(validation.normalized_ir)

        assert bundle.success is True
        assert bundle.file_count > 0
        assert bundle.app_name == "Test App"

    def test_generate_restaurant_app(self, restaurant_blueprint: Dict[str, Any]):
        """Test generating restaurant application with multiple modules."""
        from pathlib import Path
        from app.services.codegen.ir import BundleBuilder, IRValidator

        # Validate first
        validator = IRValidator()
        validation = validator.validate_app_blueprint(restaurant_blueprint)
        assert validation.valid is True

        # Generate
        template_dir = Path(__file__).parent.parent.parent.parent / \
            "app" / "services" / "codegen" / "templates"
        builder = BundleBuilder(template_dir=template_dir)
        bundle = builder.build(validation.normalized_ir)

        assert bundle.success is True
        assert bundle.file_count > 20  # Should generate many files

        # Check module-specific files exist
        file_paths = [f.path for f in bundle.files]
        assert "app/models/product.py" in file_paths
        assert "app/models/order.py" in file_paths
        assert "app/api/routes/products.py" in file_paths
        assert "app/api/routes/orders.py" in file_paths

    def test_generate_preview_mode(self, minimal_blueprint: Dict[str, Any]):
        """Test preview mode returns file list without content."""
        from pathlib import Path
        from app.services.codegen.ir import BundleBuilder, IRValidator

        validator = IRValidator()
        validation = validator.validate_app_blueprint(minimal_blueprint)

        template_dir = Path(__file__).parent.parent.parent.parent / \
            "app" / "services" / "codegen" / "templates"
        builder = BundleBuilder(template_dir=template_dir)
        preview = builder.build_preview(validation.normalized_ir)

        assert preview["success"] is True
        assert preview["file_count"] > 0
        assert "files" in preview

        # Preview files should have path but no content
        for file_info in preview["files"]:
            assert "path" in file_info
            assert "lines" in file_info

    def test_generated_python_compiles(self, minimal_blueprint: Dict[str, Any]):
        """Test that generated Python code compiles."""
        from pathlib import Path
        from app.services.codegen.ir import BundleBuilder, IRValidator

        validator = IRValidator()
        validation = validator.validate_app_blueprint(minimal_blueprint)

        template_dir = Path(__file__).parent.parent.parent.parent / \
            "app" / "services" / "codegen" / "templates"
        builder = BundleBuilder(template_dir=template_dir)
        bundle = builder.build(validation.normalized_ir)

        python_files = bundle.get_files_by_language("python")
        assert len(python_files) > 0

        for file in python_files:
            try:
                compile(file.content, file.path, "exec")
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {file.path}: {e}")


class TestIRGenerateResponseFormat:
    """Test response format matches API schema."""

    def test_response_has_required_fields(self, minimal_blueprint: Dict[str, Any]):
        """Test response contains all required fields."""
        from pathlib import Path
        from app.services.codegen.ir import BundleBuilder, IRValidator

        validator = IRValidator()
        validation = validator.validate_app_blueprint(minimal_blueprint)

        template_dir = Path(__file__).parent.parent.parent.parent / \
            "app" / "services" / "codegen" / "templates"
        builder = BundleBuilder(template_dir=template_dir)
        bundle = builder.build(validation.normalized_ir)

        # Simulate API response format
        api_response = bundle.to_dict_for_api()

        assert "success" in api_response
        assert "app_name" in api_response
        assert "files" in api_response
        assert "metadata" in api_response

    def test_metadata_contains_generator_info(self, minimal_blueprint: Dict[str, Any]):
        """Test metadata contains generator information."""
        from pathlib import Path
        from app.services.codegen.ir import BundleBuilder, IRValidator

        validator = IRValidator()
        validation = validator.validate_app_blueprint(minimal_blueprint)

        template_dir = Path(__file__).parent.parent.parent.parent / \
            "app" / "services" / "codegen" / "templates"
        builder = BundleBuilder(template_dir=template_dir)
        bundle = builder.build(validation.normalized_ir)

        api_response = bundle.to_dict_for_api()
        metadata = api_response.get("metadata", {})

        assert "generator" in metadata
        assert "SDLC Orchestrator" in metadata["generator"]
