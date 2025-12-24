"""
Unit tests for BundleBuilder.

Sprint 46: EP-06 IR-Based Backend Scaffold Generation
ADR-023: IR-Based Deterministic Code Generation

Tests bundle generation including:
- Full pipeline execution
- Error handling
- Generated file validation

Author: Backend Lead
Date: December 23, 2025
Version: 1.0.0
Status: ACTIVE - Sprint 46 Implementation
"""

import pytest
from pathlib import Path
from typing import Dict, Any

from app.services.codegen.ir.bundle_builder import (
    BundleBuilder,
    GeneratedBundle,
)


class TestBundleBuilderBasic:
    """Test basic BundleBuilder functionality."""

    @pytest.fixture
    def builder(self) -> BundleBuilder:
        """Create BundleBuilder with default templates."""
        template_dir = Path(__file__).parent.parent.parent.parent.parent.parent / \
            "app" / "services" / "codegen" / "templates"
        return BundleBuilder(template_dir=template_dir)

    @pytest.fixture
    def minimal_blueprint(self) -> Dict[str, Any]:
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

    def test_build_minimal_app(self, builder: BundleBuilder, minimal_blueprint: Dict[str, Any]):
        """Test building a minimal application."""
        bundle = builder.build(minimal_blueprint)

        assert bundle.success is True
        assert bundle.app_name == "Test App"
        assert bundle.file_count > 0
        assert bundle.total_lines > 0
        assert len(bundle.errors) == 0

    def test_build_generates_required_files(self, builder: BundleBuilder, minimal_blueprint: Dict[str, Any]):
        """Test that required files are generated."""
        bundle = builder.build(minimal_blueprint)

        file_paths = [f.path for f in bundle.files]

        # Check scaffold files
        assert "app/main.py" in file_paths
        assert "app/core/config.py" in file_paths
        assert "app/core/database.py" in file_paths
        assert "requirements.txt" in file_paths
        assert "Dockerfile" in file_paths
        assert "docker-compose.yml" in file_paths

        # Check model files
        assert "app/models/item.py" in file_paths
        assert "app/schemas/item.py" in file_paths

        # Check endpoint files
        assert "app/api/routes/items.py" in file_paths
        assert "app/services/item_service.py" in file_paths

    def test_build_invalid_blueprint(self, builder: BundleBuilder):
        """Test build fails gracefully for invalid blueprint."""
        invalid_blueprint = {
            "name": "Test",
            # Missing version and modules
        }

        bundle = builder.build(invalid_blueprint)

        assert bundle.success is False
        assert len(bundle.errors) > 0
        assert bundle.file_count == 0

    def test_build_preview(self, builder: BundleBuilder, minimal_blueprint: Dict[str, Any]):
        """Test build_preview returns file info without content."""
        preview = builder.build_preview(minimal_blueprint)

        assert preview["success"] is True
        assert preview["file_count"] > 0
        assert "files" in preview

        for file_info in preview["files"]:
            assert "path" in file_info
            assert "language" in file_info
            assert "lines" in file_info


class TestBundleBuilderMultiModule:
    """Test BundleBuilder with multiple modules."""

    @pytest.fixture
    def builder(self) -> BundleBuilder:
        template_dir = Path(__file__).parent.parent.parent.parent.parent.parent / \
            "app" / "services" / "codegen" / "templates"
        return BundleBuilder(template_dir=template_dir)

    @pytest.fixture
    def multi_module_blueprint(self) -> Dict[str, Any]:
        """Blueprint with multiple modules."""
        return {
            "name": "Restaurant App",
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

    def test_build_multi_module(self, builder: BundleBuilder, multi_module_blueprint: Dict[str, Any]):
        """Test building multi-module application."""
        bundle = builder.build(multi_module_blueprint)

        assert bundle.success is True
        assert bundle.app_name == "Restaurant App"

        file_paths = [f.path for f in bundle.files]

        # Check product module
        assert "app/models/product.py" in file_paths
        assert "app/schemas/product.py" in file_paths
        assert "app/api/routes/products.py" in file_paths
        assert "app/services/product_service.py" in file_paths

        # Check order module
        assert "app/models/order.py" in file_paths
        assert "app/schemas/order.py" in file_paths
        assert "app/api/routes/orders.py" in file_paths
        assert "app/services/order_service.py" in file_paths

    def test_generated_main_includes_all_routers(self, builder: BundleBuilder, multi_module_blueprint: Dict[str, Any]):
        """Test main.py includes all module routers."""
        bundle = builder.build(multi_module_blueprint)

        main_file = bundle.get_file("app/main.py")
        assert main_file is not None
        assert "Restaurant App" in main_file.content


class TestGeneratedBundle:
    """Test GeneratedBundle class."""

    def test_get_file(self):
        """Test getting file by path."""
        from app.services.codegen.ir.processor_base import GeneratedFile

        bundle = GeneratedBundle(
            success=True,
            app_name="Test",
            files=[
                GeneratedFile(path="app/main.py", content="# main"),
                GeneratedFile(path="app/config.py", content="# config"),
            ],
            file_count=2,
            total_lines=2,
        )

        main = bundle.get_file("app/main.py")
        assert main is not None
        assert main.content == "# main"

        missing = bundle.get_file("app/missing.py")
        assert missing is None

    def test_get_files_by_language(self):
        """Test filtering files by language."""
        from app.services.codegen.ir.processor_base import GeneratedFile

        bundle = GeneratedBundle(
            success=True,
            app_name="Test",
            files=[
                GeneratedFile(path="app/main.py", content="# py", language="python"),
                GeneratedFile(path="Dockerfile", content="FROM", language="dockerfile"),
                GeneratedFile(path="app/config.py", content="# py2", language="python"),
            ],
            file_count=3,
            total_lines=3,
        )

        python_files = bundle.get_files_by_language("python")
        assert len(python_files) == 2

        docker_files = bundle.get_files_by_language("dockerfile")
        assert len(docker_files) == 1

    def test_to_dict_for_api(self):
        """Test converting to API response format."""
        from app.services.codegen.ir.processor_base import GeneratedFile

        bundle = GeneratedBundle(
            success=True,
            app_name="Test",
            version="1.0.0",
            files=[
                GeneratedFile(path="app/main.py", content="# main"),
            ],
            file_count=1,
            total_lines=1,
        )

        api_dict = bundle.to_dict_for_api()

        assert api_dict["success"] is True
        assert api_dict["app_name"] == "Test"
        assert "app/main.py" in api_dict["files"]
        assert api_dict["files"]["app/main.py"] == "# main"
        assert "metadata" in api_dict
        assert "generator" in api_dict["metadata"]


class TestBundleBuilderGeneratedCode:
    """Test that generated code is valid."""

    @pytest.fixture
    def builder(self) -> BundleBuilder:
        template_dir = Path(__file__).parent.parent.parent.parent.parent.parent / \
            "app" / "services" / "codegen" / "templates"
        return BundleBuilder(template_dir=template_dir)

    @pytest.fixture
    def simple_blueprint(self) -> Dict[str, Any]:
        return {
            "name": "Simple App",
            "version": "1.0.0",
            "modules": [{
                "name": "users",
                "entities": [{
                    "name": "User",
                    "fields": [
                        {"name": "email", "type": "string", "required": True, "unique": True},
                        {"name": "name", "type": "string", "required": True},
                        {"name": "active", "type": "boolean"},
                    ]
                }]
            }]
        }

    def test_generated_python_compiles(self, builder: BundleBuilder, simple_blueprint: Dict[str, Any]):
        """Test that generated Python code compiles."""
        bundle = builder.build(simple_blueprint)

        python_files = bundle.get_files_by_language("python")
        assert len(python_files) > 0

        for file in python_files:
            # Try to compile each Python file
            try:
                compile(file.content, file.path, "exec")
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {file.path}: {e}")

    def test_model_contains_entity_name(self, builder: BundleBuilder, simple_blueprint: Dict[str, Any]):
        """Test model file contains entity class."""
        bundle = builder.build(simple_blueprint)

        model_file = bundle.get_file("app/models/user.py")
        assert model_file is not None
        assert "class User" in model_file.content
        assert "__tablename__" in model_file.content

    def test_schema_contains_pydantic_models(self, builder: BundleBuilder, simple_blueprint: Dict[str, Any]):
        """Test schema file contains Pydantic models."""
        bundle = builder.build(simple_blueprint)

        schema_file = bundle.get_file("app/schemas/user.py")
        assert schema_file is not None
        assert "class UserCreate" in schema_file.content
        assert "class UserRead" in schema_file.content
        assert "class UserUpdate" in schema_file.content

    def test_route_contains_crud_endpoints(self, builder: BundleBuilder, simple_blueprint: Dict[str, Any]):
        """Test route file contains CRUD endpoints."""
        bundle = builder.build(simple_blueprint)

        route_file = bundle.get_file("app/api/routes/users.py")
        assert route_file is not None
        assert "@router.post" in route_file.content
        assert "@router.get" in route_file.content
        assert "@router.patch" in route_file.content
        assert "@router.delete" in route_file.content

    def test_service_contains_crud_methods(self, builder: BundleBuilder, simple_blueprint: Dict[str, Any]):
        """Test service file contains CRUD methods."""
        bundle = builder.build(simple_blueprint)

        service_file = bundle.get_file("app/services/user_service.py")
        assert service_file is not None
        assert "async def create" in service_file.content
        assert "async def get" in service_file.content
        assert "async def list" in service_file.content
        assert "async def update" in service_file.content
        assert "async def delete" in service_file.content
