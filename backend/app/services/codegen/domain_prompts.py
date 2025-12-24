"""
Domain-Aware Prompts for AI Code Generation.

Sprint 47: Vietnamese Domain Templates + Onboarding IR (EP-06)

This module provides domain-specific prompts for AI code generation,
integrating CGF V2.1 Master Processes and Vietnamese SME context.

Features:
- Domain-specific prompts (F&B, Hospitality, Retail)
- CGF V2.1 Master Process integration
- Vietnamese business context
- Industry-specific best practices

Author: Backend Lead
Date: December 23, 2025
Status: ACTIVE
"""

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .domains.cgf_metadata import (
    get_domain_cgf_mapping,
    get_master_process,
    VIETNAMESE_CI,
)


@dataclass
class DomainPromptContext:
    """
    Context for domain-specific prompt generation.

    Attributes:
        domain: Domain key (restaurant, hotel, retail)
        app_name: Application name
        modules: Selected modules
        scale: Business scale (micro, small, medium, large)
        cgf_tier: CGF tier (LITE, STANDARD, PROFESSIONAL, ENTERPRISE)
        language: Target programming language
        framework: Target framework
    """
    domain: str
    app_name: str
    modules: List[str]
    scale: str = "small"
    cgf_tier: str = "STANDARD"
    language: str = "python"
    framework: str = "fastapi"
    database: str = "postgresql"
    vietnamese_comments: bool = True


class DomainPromptBuilder:
    """
    Builds domain-specific prompts for AI code generation.

    Integrates CGF V2.1 metadata for industry-aware prompts.

    Example:
        >>> builder = DomainPromptBuilder()
        >>> prompt = builder.build_generation_prompt(
        ...     context=DomainPromptContext(
        ...         domain="restaurant",
        ...         app_name="QuanComNgon",
        ...         modules=["menu", "orders", "tables"]
        ...     ),
        ...     blueprint={"name": "QuanComNgon", ...}
        ... )
    """

    # Domain-specific system prompts
    DOMAIN_SYSTEM_PROMPTS = {
        "restaurant": """Bạn là chuyên gia phát triển phần mềm quản lý nhà hàng/quán ăn cho SME Việt Nam.

Kiến thức chuyên ngành F&B:
- Quy trình Order-to-Cash (MP-002): Nhận đơn → Chế biến → Phục vụ → Thanh toán
- Quản lý thực đơn với biến thể (size, topping, độ ngọt)
- Mã sản phẩm PRD-XXXX theo chuẩn Simplified Code V2.0
- Tích hợp VAT 10% cho hàng hóa, 8% cho dịch vụ ăn uống
- Quản lý bàn (số bàn, sức chứa, trạng thái)
- Hỗ trợ ghi chú đặc biệt (không hành, ít cay, dị ứng)

Best practices cho F&B software:
- Order status: pending → preparing → ready → served → paid
- Kitchen Display System (KDS) integration
- Table turnover optimization
- Combo/Set meal pricing
- Tip calculation (tùy chọn)""",

        "hotel": """Bạn là chuyên gia phát triển phần mềm quản lý khách sạn/lưu trú cho SME Việt Nam.

Kiến thức chuyên ngành Hospitality:
- Quy trình Guest-to-Departure (MP-010): Đặt phòng → Check-in → Lưu trú → Check-out
- Seat-to-Settlement (MP-011): Quản lý dịch vụ phụ trội
- Quản lý loại phòng (Standard, Deluxe, Suite, Family)
- Mã phòng ROOM-XXXX, mã khách GUEST-XXXX
- Tích hợp VAT 10% cho dịch vụ lưu trú
- Quản lý housekeeping status

Best practices cho Hotel PMS:
- Room status: available → reserved → occupied → maintenance → cleaning
- Booking status: confirmed → checked_in → checked_out → cancelled → no_show
- Early check-in / Late check-out handling
- Overbooking management
- Guest history và preferences""",

        "retail": """Bạn là chuyên gia phát triển phần mềm quản lý bán lẻ/cửa hàng cho SME Việt Nam.

Kiến thức chuyên ngành Retail:
- Quy trình Purchase-to-Pay (MP-001): Đặt hàng → Nhập kho → Thanh toán NCC
- Quy trình Order-to-Cash (MP-002): Bán hàng → Xuất kho → Thu tiền
- Quy trình Lead-to-Customer (MP-006): Khách hàng tiềm năng → Khách hàng
- Mã sản phẩm PRD-XXXX, mã khách CUS-XXXX theo Simplified Code V2.0
- Tích hợp VAT 10% (hàng hóa), 8% (dịch vụ), 5% (nông sản)
- Quản lý tồn kho nhiều kho (multi-warehouse)

Best practices cho Retail POS:
- Inventory: FIFO costing theo VAS 02
- Stock movement: purchase → transfer → sale → adjustment
- Customer tiers: bronze → silver → gold → platinum
- Promotion types: discount, voucher, combo, buy-x-get-y
- Barcode/SKU management"""
    }

    # Module-specific instructions
    MODULE_INSTRUCTIONS = {
        "menu": """Module thực đơn:
- Entity: Category (danh mục), MenuItem (món ăn)
- Fields: tên, mô tả, giá, hình ảnh, trạng thái available/unavailable
- Relationships: Category 1-N MenuItem
- API: CRUD + bulk update price, toggle availability""",

        "orders": """Module đơn hàng:
- Entity: Order, OrderItem
- Fields: mã đơn, trạng thái, tổng tiền, giảm giá, khách hàng, ghi chú
- Status flow: pending → confirmed → preparing → ready → completed → cancelled
- API: Create order, update status, add/remove items, apply discount""",

        "tables": """Module bàn:
- Entity: Table
- Fields: số bàn, sức chứa, vị trí, trạng thái
- Status: available → occupied → reserved → maintenance
- API: CRUD + get available tables, assign/release table""",

        "reservations": """Module đặt chỗ:
- Entity: Reservation
- Fields: khách, bàn, thời gian, số người, ghi chú, trạng thái
- Status: pending → confirmed → seated → completed → cancelled → no_show
- API: Create, confirm, cancel, seat guest""",

        "rooms": """Module phòng:
- Entity: RoomType, Room
- Fields: loại phòng, số phòng, tầng, giá, tiện nghi, trạng thái
- Status: available → reserved → occupied → maintenance → cleaning
- API: CRUD + get available rooms, update status""",

        "bookings": """Module đặt phòng:
- Entity: Booking
- Fields: khách, phòng, check-in, check-out, số khách, yêu cầu đặc biệt
- Status: confirmed → checked_in → checked_out → cancelled → no_show
- API: Create, check-in, check-out, extend stay, cancel""",

        "guests": """Module khách hàng khách sạn:
- Entity: Guest
- Fields: họ tên, CCCD/passport, quốc tịch, SĐT, email, lịch sử lưu trú
- Features: VIP flag, preferences, blacklist
- API: CRUD + search, merge duplicates""",

        "billing": """Module thanh toán khách sạn:
- Entity: Billing, BillingItem
- Fields: mã hóa đơn, booking, tổng tiền, thuế VAT, phương thức thanh toán
- Items: room charge, services, minibar, restaurant, laundry
- API: Generate bill, add charge, process payment, refund""",

        "products": """Module sản phẩm:
- Entity: Category, Product
- Fields: mã SP (PRD-XXXX), tên, mô tả, barcode, giá nhập, giá bán, tồn kho
- Categories: hierarchical (parent-child)
- API: CRUD + bulk import, price update, stock sync""",

        "inventory": """Module tồn kho:
- Entity: Warehouse, Inventory, StockMovement
- Fields: kho, sản phẩm, số lượng, giá vốn (FIFO)
- Movement types: purchase, sale, transfer, adjustment, return
- API: Check stock, transfer, adjust, stock take""",

        "sales": """Module bán hàng:
- Entity: Sale, SaleItem
- Fields: mã hóa đơn, khách hàng, sản phẩm, số lượng, giảm giá, VAT
- Payment: cash, card, transfer, e-wallet
- API: Create sale, void, return, daily report""",

        "customers": """Module khách hàng bán lẻ:
- Entity: Customer
- Fields: mã KH (CUS-XXXX), họ tên, SĐT, email, điểm tích lũy, tier
- Tiers: bronze (0), silver (1000), gold (5000), platinum (20000 points)
- API: CRUD + earn/redeem points, tier upgrade"""
    }

    def __init__(self):
        """Initialize prompt builder."""
        pass

    def build_generation_prompt(
        self,
        context: DomainPromptContext,
        blueprint: Dict[str, Any]
    ) -> str:
        """
        Build domain-specific generation prompt.

        Args:
            context: Domain prompt context
            blueprint: AppBlueprint IR

        Returns:
            Formatted prompt for AI code generation
        """
        # Get domain system prompt
        system_prompt = self.DOMAIN_SYSTEM_PROMPTS.get(
            context.domain,
            self._get_generic_system_prompt()
        )

        # Get CGF metadata
        cgf = get_domain_cgf_mapping(context.domain)
        cgf_section = self._build_cgf_section(cgf) if cgf else ""

        # Get module instructions
        module_instructions = self._build_module_instructions(context.modules)

        # Vietnamese business context
        vn_context = self._build_vietnamese_context(context)

        # Blueprint JSON
        blueprint_json = json.dumps(blueprint, indent=2, ensure_ascii=False)

        # Build final prompt
        prompt = f"""{system_prompt}

{cgf_section}

{vn_context}

## App Blueprint (IR Specification)
```json
{blueprint_json}
```

## Module Instructions
{module_instructions}

## Technical Requirements
- **Language**: {context.language}
- **Framework**: {context.framework}
- **Database**: {context.database}
- **CGF Tier**: {context.cgf_tier}
- **Business Scale**: {context.scale}

## Coding Standards
1. Production-ready code (no TODO, no placeholders)
2. Full type hints (Python 3.11+)
3. Proper error handling with Vietnamese error messages
4. Vietnamese comments for complex business logic
5. Follow {context.framework} best practices
6. OWASP security guidelines

## Output Format
Each file starts with `### FILE: path/to/file.ext`
Code in ```{context.language}``` block

### FILE: example/file.py
```{context.language}
# code here
```

Begin generating code:
"""
        return prompt

    def build_enhancement_prompt(
        self,
        context: DomainPromptContext,
        existing_code: str,
        enhancement_request: str
    ) -> str:
        """
        Build prompt for enhancing existing code.

        Args:
            context: Domain prompt context
            existing_code: Existing code to enhance
            enhancement_request: What to add/change

        Returns:
            Formatted enhancement prompt
        """
        system_prompt = self.DOMAIN_SYSTEM_PROMPTS.get(
            context.domain,
            self._get_generic_system_prompt()
        )

        return f"""{system_prompt}

## Existing Code
```{context.language}
{existing_code}
```

## Enhancement Request
{enhancement_request}

## Requirements
1. Preserve existing functionality
2. Add new features cleanly
3. Maintain code style consistency
4. Add Vietnamese comments for new logic
5. Update imports and dependencies as needed

## Output Format
Return the complete enhanced file(s) with `### FILE:` markers.

Begin enhancement:
"""

    def build_validation_prompt(
        self,
        context: DomainPromptContext,
        code: str
    ) -> str:
        """
        Build domain-specific validation prompt.

        Args:
            context: Domain prompt context
            code: Code to validate

        Returns:
            Formatted validation prompt
        """
        domain_checks = self._get_domain_validation_checks(context.domain)

        return f"""Bạn là senior code reviewer chuyên về phần mềm {context.domain} cho SME Việt Nam.

## Code cần review
```{context.language}
{code[:8000]}
```

## Domain: {context.domain}
## Framework: {context.framework}

## Kiểm tra chuyên ngành
{domain_checks}

## Tiêu chí đánh giá chung
1. **Errors** (Lỗi nghiêm trọng): Bugs, security vulnerabilities, logic errors
2. **Warnings** (Cảnh báo): Code smell, performance issues, best practice violations
3. **Suggestions** (Gợi ý): Improvements, refactoring, domain-specific optimizations

## Output Format (JSON only)
```json
{{
  "valid": true/false,
  "score": 0-100,
  "errors": ["Mô tả lỗi bằng tiếng Việt"],
  "warnings": ["Cảnh báo bằng tiếng Việt"],
  "suggestions": ["Gợi ý cải thiện bằng tiếng Việt"],
  "domain_compliance": {{
    "cgf_alignment": true/false,
    "vietnamese_ci": true/false,
    "industry_best_practices": true/false
  }}
}}
```

Chỉ trả về JSON, không có text khác.
"""

    def _get_generic_system_prompt(self) -> str:
        """Get generic system prompt for unknown domains."""
        return """Bạn là chuyên gia phát triển phần mềm quản lý doanh nghiệp cho SME Việt Nam.

Kiến thức chung:
- Quy trình quản lý doanh nghiệp SME
- Tích hợp VAT theo quy định Việt Nam
- Chuẩn mã hóa Simplified Code V2.0
- Best practices cho phần mềm quản lý"""

    def _build_cgf_section(self, cgf) -> str:
        """Build CGF metadata section."""
        if not cgf:
            return ""

        # Get master process details
        mp_details = []
        for mp_id in cgf.master_processes:
            mp = get_master_process(mp_id)
            if mp:
                mp_details.append(f"- **{mp_id}**: {mp.name_vi} ({mp.name})")

        return f"""## CGF V2.1 Compliance
**Master Processes**:
{chr(10).join(mp_details)}

**MDG Compliance**: {', '.join(cgf.mdg_compliance)}

**DAG Levels**: Entity-specific approval levels defined
"""

    def _build_module_instructions(self, modules: List[str]) -> str:
        """Build module-specific instructions."""
        instructions = []
        for module in modules:
            if module in self.MODULE_INSTRUCTIONS:
                instructions.append(self.MODULE_INSTRUCTIONS[module])

        if not instructions:
            return "Follow standard CRUD patterns for all modules."

        return "\n\n".join(instructions)

    def _build_vietnamese_context(self, context: DomainPromptContext) -> str:
        """Build Vietnamese business context section."""
        ci = VIETNAMESE_CI

        vat = ci.get("vat", {})
        bhxh = ci.get("bhxh", {})
        labor = ci.get("labor_code", {})

        vat_info = f"{vat.get('standard_rate', '10%')} standard, {vat.get('reduced_rate', '5%')} reduced"
        bhxh_info = f"{bhxh.get('employee_rate', '8%')} employee, {bhxh.get('employer_rate', '17.5%')} employer"
        hours = labor.get("standard_hours", 48)

        return f"""## Vietnamese Business Context
- **Currency**: VND (Việt Nam Đồng)
- **VAT Rates**: {vat_info}
- **BHXH** (Social Insurance): {bhxh_info}
- **Labor Code**: {hours} hours/week standard
- **Date Format**: DD/MM/YYYY
- **Number Format**: 1.000.000 VNĐ (dots as thousand separators)
"""

    def _get_domain_validation_checks(self, domain: str) -> str:
        """Get domain-specific validation checks."""
        checks = {
            "restaurant": """
- Order status transitions đúng flow
- Menu item availability handling
- Table status management
- VAT calculation cho F&B (8-10%)
- Kitchen order integration ready""",

            "hotel": """
- Booking date validation (check-in < check-out)
- Room availability checking
- Guest ID validation (CCCD/Passport format)
- Billing item tracking
- Housekeeping status sync""",

            "retail": """
- Inventory FIFO costing
- Stock level validation
- Customer point calculation
- VAT handling multi-rate
- Barcode/SKU uniqueness"""
        }

        return checks.get(domain, """
- Business logic correctness
- Data validation
- Error handling
- Security best practices""")


# Singleton instance
_prompt_builder: Optional[DomainPromptBuilder] = None


def get_domain_prompt_builder() -> DomainPromptBuilder:
    """Get singleton DomainPromptBuilder instance."""
    global _prompt_builder
    if _prompt_builder is None:
        _prompt_builder = DomainPromptBuilder()
    return _prompt_builder


def create_domain_prompt_from_blueprint(
    blueprint: Dict[str, Any],
    domain: Optional[str] = None,
    language: str = "python",
    framework: str = "fastapi",
    database: str = "postgresql",
) -> str:
    """
    Create domain-aware generation prompt from AppBlueprint IR.

    This is the main entry point for integrating domain prompts
    with the Ollama provider and onboarding flow.

    Args:
        blueprint: AppBlueprint IR dictionary
        domain: Domain key (auto-detect from blueprint if not provided)
        language: Target programming language
        framework: Target framework
        database: Target database

    Returns:
        Formatted prompt for AI code generation

    Example:
        >>> blueprint = {
        ...     "name": "QuanPhoNgon",
        ...     "domain": "restaurant",
        ...     "version": "1.0.0",
        ...     "modules": [{"name": "menu"}, {"name": "orders"}]
        ... }
        >>> prompt = create_domain_prompt_from_blueprint(blueprint)
    """
    # Auto-detect domain from blueprint
    if domain is None:
        domain = blueprint.get("domain", "generic")

    # Extract modules
    modules = [m.get("name", "") for m in blueprint.get("modules", [])]

    # Determine scale and CGF tier
    scale = blueprint.get("scale", "small")
    cgf_tier = blueprint.get("cgf_tier", "STANDARD")

    # Create context
    context = DomainPromptContext(
        domain=domain,
        app_name=blueprint.get("name", "App"),
        modules=modules,
        scale=scale,
        cgf_tier=cgf_tier,
        language=language,
        framework=framework,
        database=database,
    )

    # Build and return prompt
    builder = get_domain_prompt_builder()
    return builder.build_generation_prompt(context, blueprint)
