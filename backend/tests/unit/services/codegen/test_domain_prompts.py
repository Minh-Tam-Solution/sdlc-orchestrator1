"""
Tests for Domain-Aware Prompts.

Sprint 47: Vietnamese Domain Templates + Onboarding IR (EP-06)

Tests:
- DomainPromptBuilder: Domain-specific prompt generation
- CGF integration in prompts
- Vietnamese business context

Author: Backend Lead
Date: December 23, 2025
"""

import pytest
from app.services.codegen.domain_prompts import (
    DomainPromptBuilder,
    DomainPromptContext,
    create_domain_prompt_from_blueprint,
    get_domain_prompt_builder,
)


class TestDomainPromptContext:
    """Tests for DomainPromptContext dataclass."""

    def test_create_context_with_defaults(self):
        """Test context creation with default values."""
        context = DomainPromptContext(
            domain="restaurant",
            app_name="QuanComNgon",
            modules=["menu", "orders"]
        )

        assert context.domain == "restaurant"
        assert context.app_name == "QuanComNgon"
        assert context.scale == "small"
        assert context.cgf_tier == "STANDARD"
        assert context.language == "python"
        assert context.framework == "fastapi"

    def test_create_context_with_custom_values(self):
        """Test context creation with custom values."""
        context = DomainPromptContext(
            domain="hotel",
            app_name="KhachSanHaiAu",
            modules=["rooms", "bookings"],
            scale="medium",
            cgf_tier="PROFESSIONAL",
            language="python",
            framework="fastapi",
            database="postgresql"
        )

        assert context.domain == "hotel"
        assert context.scale == "medium"
        assert context.cgf_tier == "PROFESSIONAL"


class TestDomainPromptBuilder:
    """Tests for DomainPromptBuilder."""

    def test_build_restaurant_prompt(self):
        """Test restaurant domain prompt generation."""
        builder = DomainPromptBuilder()
        context = DomainPromptContext(
            domain="restaurant",
            app_name="QuanPhoNgon",
            modules=["menu", "orders", "tables"]
        )
        blueprint = {
            "name": "QuanPhoNgon",
            "version": "1.0.0",
            "modules": []
        }

        prompt = builder.build_generation_prompt(context, blueprint)

        # Check domain-specific content
        assert "nhà hàng" in prompt.lower() or "F&B" in prompt
        assert "Order-to-Cash" in prompt or "MP-002" in prompt
        assert "thực đơn" in prompt.lower() or "menu" in prompt.lower()
        assert "QuanPhoNgon" in prompt

    def test_build_hotel_prompt(self):
        """Test hotel domain prompt generation."""
        builder = DomainPromptBuilder()
        context = DomainPromptContext(
            domain="hotel",
            app_name="DalatHomestay",
            modules=["rooms", "bookings", "guests"]
        )
        blueprint = {
            "name": "DalatHomestay",
            "version": "1.0.0",
            "modules": []
        }

        prompt = builder.build_generation_prompt(context, blueprint)

        # Check hotel-specific content
        assert "khách sạn" in prompt.lower() or "lưu trú" in prompt.lower()
        assert "Guest-to-Departure" in prompt or "MP-010" in prompt or "MP-011" in prompt
        assert "phòng" in prompt.lower()

    def test_build_retail_prompt(self):
        """Test retail domain prompt generation."""
        builder = DomainPromptBuilder()
        context = DomainPromptContext(
            domain="retail",
            app_name="CuaHang365",
            modules=["products", "inventory", "sales"]
        )
        blueprint = {
            "name": "CuaHang365",
            "version": "1.0.0",
            "modules": []
        }

        prompt = builder.build_generation_prompt(context, blueprint)

        # Check retail-specific content
        assert "bán lẻ" in prompt.lower() or "cửa hàng" in prompt.lower()
        assert "Purchase-to-Pay" in prompt or "MP-001" in prompt
        assert "tồn kho" in prompt.lower() or "inventory" in prompt.lower()

    def test_prompt_includes_vietnamese_context(self):
        """Test prompt includes Vietnamese business context."""
        builder = DomainPromptBuilder()
        context = DomainPromptContext(
            domain="restaurant",
            app_name="TestApp",
            modules=["menu"]
        )
        blueprint = {"name": "TestApp", "modules": []}

        prompt = builder.build_generation_prompt(context, blueprint)

        # Check Vietnamese context
        assert "VND" in prompt or "Việt Nam Đồng" in prompt
        assert "VAT" in prompt
        assert "BHXH" in prompt or "Social Insurance" in prompt

    def test_prompt_includes_module_instructions(self):
        """Test prompt includes module-specific instructions."""
        builder = DomainPromptBuilder()
        context = DomainPromptContext(
            domain="restaurant",
            app_name="TestApp",
            modules=["menu", "orders"]
        )
        blueprint = {"name": "TestApp", "modules": []}

        prompt = builder.build_generation_prompt(context, blueprint)

        # Check module instructions
        assert "Category" in prompt or "MenuItem" in prompt
        assert "Order" in prompt or "OrderItem" in prompt

    def test_prompt_includes_technical_requirements(self):
        """Test prompt includes technical requirements."""
        builder = DomainPromptBuilder()
        context = DomainPromptContext(
            domain="retail",
            app_name="TestApp",
            modules=["products"],
            language="python",
            framework="fastapi",
            database="postgresql"
        )
        blueprint = {"name": "TestApp", "modules": []}

        prompt = builder.build_generation_prompt(context, blueprint)

        # Check technical requirements
        assert "python" in prompt.lower()
        assert "fastapi" in prompt.lower()
        assert "postgresql" in prompt.lower()

    def test_prompt_includes_output_format(self):
        """Test prompt includes output format instructions."""
        builder = DomainPromptBuilder()
        context = DomainPromptContext(
            domain="restaurant",
            app_name="TestApp",
            modules=["menu"]
        )
        blueprint = {"name": "TestApp", "modules": []}

        prompt = builder.build_generation_prompt(context, blueprint)

        # Check output format
        assert "### FILE:" in prompt
        assert "```" in prompt

    def test_build_enhancement_prompt(self):
        """Test enhancement prompt generation."""
        builder = DomainPromptBuilder()
        context = DomainPromptContext(
            domain="restaurant",
            app_name="TestApp",
            modules=["menu"]
        )

        existing_code = """
class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price
"""
        enhancement = "Add category field and availability status"

        prompt = builder.build_enhancement_prompt(context, existing_code, enhancement)

        assert "MenuItem" in prompt
        assert "category" in prompt.lower()
        assert "availability" in prompt.lower()
        assert "### FILE:" in prompt

    def test_build_validation_prompt(self):
        """Test validation prompt generation."""
        builder = DomainPromptBuilder()
        context = DomainPromptContext(
            domain="restaurant",
            app_name="TestApp",
            modules=["orders"]
        )

        code = """
def create_order(items, table_id):
    order = Order(status='pending')
    for item in items:
        order.add_item(item)
    return order
"""

        prompt = builder.build_validation_prompt(context, code)

        # Check validation prompt structure
        assert "review" in prompt.lower()
        assert "JSON" in prompt
        assert "errors" in prompt.lower()
        assert "warnings" in prompt.lower()
        assert "suggestions" in prompt.lower()

    def test_validation_prompt_includes_domain_checks(self):
        """Test validation prompt includes domain-specific checks."""
        builder = DomainPromptBuilder()

        # Restaurant domain
        context = DomainPromptContext(
            domain="restaurant",
            app_name="TestApp",
            modules=["orders"]
        )
        prompt = builder.build_validation_prompt(context, "code")
        assert "Order status" in prompt or "VAT" in prompt

        # Hotel domain
        context = DomainPromptContext(
            domain="hotel",
            app_name="TestApp",
            modules=["bookings"]
        )
        prompt = builder.build_validation_prompt(context, "code")
        assert "Booking" in prompt or "check-in" in prompt.lower()

        # Retail domain
        context = DomainPromptContext(
            domain="retail",
            app_name="TestApp",
            modules=["inventory"]
        )
        prompt = builder.build_validation_prompt(context, "code")
        assert "FIFO" in prompt or "Stock" in prompt


class TestDomainPromptBuilderModules:
    """Tests for module-specific instructions."""

    def test_menu_module_instructions(self):
        """Test menu module instructions."""
        builder = DomainPromptBuilder()

        assert "menu" in builder.MODULE_INSTRUCTIONS
        instructions = builder.MODULE_INSTRUCTIONS["menu"]

        assert "Category" in instructions
        assert "MenuItem" in instructions

    def test_orders_module_instructions(self):
        """Test orders module instructions."""
        builder = DomainPromptBuilder()

        assert "orders" in builder.MODULE_INSTRUCTIONS
        instructions = builder.MODULE_INSTRUCTIONS["orders"]

        assert "Order" in instructions
        assert "status" in instructions.lower()

    def test_rooms_module_instructions(self):
        """Test rooms module instructions."""
        builder = DomainPromptBuilder()

        assert "rooms" in builder.MODULE_INSTRUCTIONS
        instructions = builder.MODULE_INSTRUCTIONS["rooms"]

        assert "RoomType" in instructions or "Room" in instructions
        assert "available" in instructions.lower()

    def test_products_module_instructions(self):
        """Test products module instructions."""
        builder = DomainPromptBuilder()

        assert "products" in builder.MODULE_INSTRUCTIONS
        instructions = builder.MODULE_INSTRUCTIONS["products"]

        assert "Product" in instructions
        assert "PRD-XXXX" in instructions

    def test_inventory_module_instructions(self):
        """Test inventory module instructions."""
        builder = DomainPromptBuilder()

        assert "inventory" in builder.MODULE_INSTRUCTIONS
        instructions = builder.MODULE_INSTRUCTIONS["inventory"]

        assert "Warehouse" in instructions or "Inventory" in instructions
        assert "FIFO" in instructions


class TestDomainSystemPrompts:
    """Tests for domain system prompts."""

    def test_restaurant_system_prompt(self):
        """Test restaurant system prompt content."""
        builder = DomainPromptBuilder()

        prompt = builder.DOMAIN_SYSTEM_PROMPTS["restaurant"]

        assert "F&B" in prompt or "nhà hàng" in prompt.lower()
        assert "Order-to-Cash" in prompt or "MP-002" in prompt
        assert "VAT" in prompt
        assert "Kitchen" in prompt or "KDS" in prompt

    def test_hotel_system_prompt(self):
        """Test hotel system prompt content."""
        builder = DomainPromptBuilder()

        prompt = builder.DOMAIN_SYSTEM_PROMPTS["hotel"]

        assert "khách sạn" in prompt.lower() or "Hospitality" in prompt
        assert "Guest-to-Departure" in prompt or "MP-010" in prompt
        assert "Check-in" in prompt or "check_in" in prompt.lower()

    def test_retail_system_prompt(self):
        """Test retail system prompt content."""
        builder = DomainPromptBuilder()

        prompt = builder.DOMAIN_SYSTEM_PROMPTS["retail"]

        assert "bán lẻ" in prompt.lower() or "Retail" in prompt
        assert "Purchase-to-Pay" in prompt or "MP-001" in prompt
        assert "FIFO" in prompt


class TestGetDomainPromptBuilder:
    """Tests for singleton pattern."""

    def test_get_singleton_instance(self):
        """Test singleton returns same instance."""
        builder1 = get_domain_prompt_builder()
        builder2 = get_domain_prompt_builder()

        assert builder1 is builder2

    def test_singleton_is_prompt_builder(self):
        """Test singleton is DomainPromptBuilder instance."""
        builder = get_domain_prompt_builder()

        assert isinstance(builder, DomainPromptBuilder)


class TestPromptCGFIntegration:
    """Tests for CGF integration in prompts."""

    def test_restaurant_cgf_processes(self):
        """Test restaurant prompt includes CGF processes."""
        builder = DomainPromptBuilder()
        context = DomainPromptContext(
            domain="restaurant",
            app_name="TestRestaurant",
            modules=["menu", "orders"]
        )
        blueprint = {"name": "TestRestaurant", "modules": []}

        prompt = builder.build_generation_prompt(context, blueprint)

        # Should include CGF section
        assert "CGF" in prompt or "Master Process" in prompt

    def test_hotel_cgf_processes(self):
        """Test hotel prompt includes CGF processes."""
        builder = DomainPromptBuilder()
        context = DomainPromptContext(
            domain="hotel",
            app_name="TestHotel",
            modules=["rooms", "bookings"]
        )
        blueprint = {"name": "TestHotel", "modules": []}

        prompt = builder.build_generation_prompt(context, blueprint)

        # Should include hospitality processes
        assert "MP-" in prompt  # Any master process

    def test_retail_cgf_processes(self):
        """Test retail prompt includes CGF processes."""
        builder = DomainPromptBuilder()
        context = DomainPromptContext(
            domain="retail",
            app_name="TestStore",
            modules=["products", "sales"]
        )
        blueprint = {"name": "TestStore", "modules": []}

        prompt = builder.build_generation_prompt(context, blueprint)

        # Should include retail processes
        assert "MP-" in prompt


class TestCreateDomainPromptFromBlueprint:
    """Tests for create_domain_prompt_from_blueprint helper function."""

    def test_create_prompt_from_restaurant_blueprint(self):
        """Test prompt creation from restaurant blueprint."""
        blueprint = {
            "name": "QuanPhoHaNoi",
            "domain": "restaurant",
            "version": "1.0.0",
            "scale": "small",
            "cgf_tier": "STANDARD",
            "modules": [
                {"name": "menu"},
                {"name": "orders"},
                {"name": "tables"}
            ]
        }

        prompt = create_domain_prompt_from_blueprint(blueprint)

        assert "QuanPhoHaNoi" in prompt
        assert "nhà hàng" in prompt.lower() or "F&B" in prompt
        assert "menu" in prompt.lower() or "thực đơn" in prompt.lower()

    def test_create_prompt_from_hotel_blueprint(self):
        """Test prompt creation from hotel blueprint."""
        blueprint = {
            "name": "KhachSanDaNang",
            "domain": "hotel",
            "version": "1.0.0",
            "modules": [
                {"name": "rooms"},
                {"name": "bookings"}
            ]
        }

        prompt = create_domain_prompt_from_blueprint(blueprint)

        assert "KhachSanDaNang" in prompt
        assert "khách sạn" in prompt.lower() or "Hospitality" in prompt

    def test_create_prompt_auto_detects_domain(self):
        """Test prompt auto-detects domain from blueprint."""
        blueprint = {
            "name": "TestRetail",
            "domain": "retail",
            "modules": [{"name": "products"}]
        }

        prompt = create_domain_prompt_from_blueprint(blueprint)

        assert "bán lẻ" in prompt.lower() or "Retail" in prompt

    def test_create_prompt_with_custom_framework(self):
        """Test prompt with custom language/framework settings."""
        blueprint = {
            "name": "TestApp",
            "domain": "restaurant",
            "modules": []
        }

        prompt = create_domain_prompt_from_blueprint(
            blueprint,
            language="python",
            framework="fastapi",
            database="postgresql"
        )

        assert "python" in prompt.lower()
        assert "fastapi" in prompt.lower()
        assert "postgresql" in prompt.lower()

    def test_create_prompt_with_empty_modules(self):
        """Test prompt with empty modules list."""
        blueprint = {
            "name": "EmptyApp",
            "domain": "restaurant",
            "modules": []
        }

        prompt = create_domain_prompt_from_blueprint(blueprint)

        assert "EmptyApp" in prompt
        # Should still have domain-specific content
        assert "nhà hàng" in prompt.lower() or "F&B" in prompt

    def test_create_prompt_defaults_to_generic_domain(self):
        """Test prompt defaults to generic when domain not specified."""
        blueprint = {
            "name": "GenericApp",
            "modules": []
        }

        prompt = create_domain_prompt_from_blueprint(blueprint)

        assert "GenericApp" in prompt
        # Generic domain uses default SME prompt
        assert "SME" in prompt or "doanh nghiệp" in prompt.lower()
