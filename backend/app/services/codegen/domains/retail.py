"""
Retail Domain Template.

Sprint 47: Vietnamese SME Domain Templates
ADR-023: IR-Based Deterministic Code Generation
Reference: Bflow CGF V2.1 (Corporate Governance Framework)

Domain-specific template for Vietnamese retail businesses:
- Shops (Cửa hàng)
- Stores (Siêu thị)
- E-commerce (Thương mại điện tử)
- Wholesale (Bán sỉ)

CGF Process Integration:
- MP-002 Order-to-Cash (O2C): Đơn hàng đến Thu tiền
- MP-006 Lead-to-Customer (L2C): Tiềm năng đến Khách hàng
- MDG-003 Product & Pricing Governance
- MDP-005 Customer Master

Entities:
- Product: Quản lý sản phẩm
- Category: Danh mục sản phẩm
- Inventory: Quản lý tồn kho
- Sale/SaleItem: Bán hàng
- Customer: Khách hàng

Author: Backend Lead
Date: December 23, 2025
Version: 1.0.0
Status: ACTIVE - Sprint 47 Implementation
"""

from typing import List

from .base import (
    DomainTemplate,
    DomainModule,
    DomainEntity,
    DomainField,
    DomainRelationship,
    DomainRegistry,
    FieldType,
    RelationType,
)


@DomainRegistry.register
class RetailDomainTemplate(DomainTemplate):
    """
    Retail Domain Template for Vietnamese shops and e-commerce.

    Provides complete entity structure for:
    - Product management (Sản phẩm)
    - Inventory management (Tồn kho)
    - Sales management (Bán hàng)
    - Customer management (Khách hàng)

    CGF Compliance:
    - Follows MDG-003 Product & Pricing Governance
    - Integrates with MP-002 Order-to-Cash (O2C)
    - Supports Vietnamese tax (VAT) and invoicing

    Target: Vietnamese SME retail businesses
    Price tier: Founder Plan ($99/team/month)
    """

    @property
    def domain_name(self) -> str:
        return "retail"

    @property
    def vietnamese_name(self) -> str:
        return "Bán lẻ / Thương mại"

    @property
    def description(self) -> str:
        return (
            "Mẫu ứng dụng quản lý cửa hàng, siêu thị, thương mại điện tử. "
            "Bao gồm quản lý sản phẩm, tồn kho, bán hàng và khách hàng."
        )

    def get_modules(self) -> List[DomainModule]:
        """Get all retail domain modules."""
        return [
            self._create_product_module(),
            self._create_inventory_module(),
            self._create_sale_module(),
            self._create_customer_module(),
        ]

    def _create_product_module(self) -> DomainModule:
        """Create product management module (MDG-003 compliant)."""
        # Category entity
        category = DomainEntity(
            name="Category",
            vietnamese_name="Danh mục",
            description="Danh mục phân loại sản phẩm",
            fields=[
                DomainField(
                    name="name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên danh mục",
                    description="Tên danh mục sản phẩm",
                    required=True,
                    max_length=100,
                ),
                DomainField(
                    name="code",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã danh mục",
                    description="Mã danh mục (VD: ELEC, CLOTH)",
                    required=True,
                    max_length=20,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="slug",
                    field_type=FieldType.STRING,
                    vietnamese_name="Slug",
                    description="URL-friendly identifier",
                    required=True,
                    max_length=100,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="description",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Mô tả",
                    description="Mô tả chi tiết danh mục",
                ),
                DomainField(
                    name="parent_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Danh mục cha",
                    description="ID danh mục cha (nếu có)",
                    indexed=True,
                ),
                DomainField(
                    name="image_url",
                    field_type=FieldType.STRING,
                    vietnamese_name="Ảnh đại diện",
                    description="URL ảnh danh mục",
                    max_length=500,
                ),
                DomainField(
                    name="display_order",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Thứ tự hiển thị",
                    description="Thứ tự sắp xếp",
                    default=0,
                ),
                DomainField(
                    name="is_active",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Đang hoạt động",
                    description="Danh mục có hiển thị không",
                    default=True,
                ),
            ],
        )

        # Product entity (PRD-XXXX - Simplified Code V2.0)
        product = DomainEntity(
            name="Product",
            vietnamese_name="Sản phẩm",
            description="Chi tiết sản phẩm - tuân thủ MDG-003",
            fields=[
                DomainField(
                    name="sku",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã SKU",
                    description="Mã sản phẩm duy nhất (PRD-XXXX)",
                    required=True,
                    max_length=50,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="barcode",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã vạch",
                    description="Mã vạch sản phẩm (EAN-13, UPC)",
                    max_length=50,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên sản phẩm",
                    description="Tên sản phẩm",
                    required=True,
                    max_length=200,
                    indexed=True,
                ),
                DomainField(
                    name="slug",
                    field_type=FieldType.STRING,
                    vietnamese_name="Slug",
                    description="URL-friendly identifier",
                    required=True,
                    max_length=200,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="description",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Mô tả",
                    description="Mô tả chi tiết sản phẩm",
                ),
                DomainField(
                    name="short_description",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mô tả ngắn",
                    description="Mô tả ngắn gọn cho listing",
                    max_length=500,
                ),
                DomainField(
                    name="category_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Danh mục",
                    description="ID danh mục chứa sản phẩm",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="brand",
                    field_type=FieldType.STRING,
                    vietnamese_name="Thương hiệu",
                    description="Tên thương hiệu",
                    max_length=100,
                    indexed=True,
                ),
                DomainField(
                    name="unit",
                    field_type=FieldType.STRING,
                    vietnamese_name="Đơn vị tính",
                    description="Đơn vị tính (cái, kg, lít,...)",
                    required=True,
                    max_length=20,
                    default="cái",
                ),
                DomainField(
                    name="cost_price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá vốn",
                    description="Giá nhập/giá vốn (VND)",
                    min_value=0,
                ),
                DomainField(
                    name="selling_price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá bán",
                    description="Giá bán lẻ (VND)",
                    required=True,
                    min_value=0,
                ),
                DomainField(
                    name="compare_price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá so sánh",
                    description="Giá gốc trước giảm giá (VND)",
                    min_value=0,
                ),
                DomainField(
                    name="wholesale_price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá sỉ",
                    description="Giá bán sỉ (VND)",
                    min_value=0,
                ),
                DomainField(
                    name="vat_rate",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Thuế suất VAT",
                    description="Thuế suất VAT (%, VD: 10)",
                    min_value=0,
                    max_value=100,
                    default=10,
                ),
                DomainField(
                    name="weight",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Trọng lượng",
                    description="Trọng lượng sản phẩm (gram)",
                    min_value=0,
                ),
                DomainField(
                    name="length",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Chiều dài",
                    description="Chiều dài (cm)",
                    min_value=0,
                ),
                DomainField(
                    name="width",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Chiều rộng",
                    description="Chiều rộng (cm)",
                    min_value=0,
                ),
                DomainField(
                    name="height",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Chiều cao",
                    description="Chiều cao (cm)",
                    min_value=0,
                ),
                DomainField(
                    name="images",
                    field_type=FieldType.JSON,
                    vietnamese_name="Hình ảnh",
                    description="Danh sách URL ảnh sản phẩm",
                ),
                DomainField(
                    name="attributes",
                    field_type=FieldType.JSON,
                    vietnamese_name="Thuộc tính",
                    description="Thuộc tính sản phẩm (màu, size,...)",
                ),
                DomainField(
                    name="is_active",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Đang kinh doanh",
                    description="Sản phẩm có đang bán không",
                    default=True,
                ),
                DomainField(
                    name="is_featured",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Nổi bật",
                    description="Sản phẩm nổi bật",
                    default=False,
                ),
                DomainField(
                    name="min_order_qty",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="SL đặt tối thiểu",
                    description="Số lượng đặt tối thiểu",
                    min_value=1,
                    default=1,
                ),
                DomainField(
                    name="max_order_qty",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="SL đặt tối đa",
                    description="Số lượng đặt tối đa (0 = không giới hạn)",
                    min_value=0,
                    default=0,
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="category",
                    target="Category",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Danh mục",
                    description="Sản phẩm thuộc danh mục nào",
                ),
                DomainRelationship(
                    name="inventory",
                    target="Inventory",
                    relation_type=RelationType.ONE_TO_MANY,
                    vietnamese_name="Tồn kho",
                    description="Tồn kho sản phẩm tại các kho",
                ),
            ],
        )

        return DomainModule(
            name="products",
            vietnamese_name="Sản phẩm",
            description="Quản lý danh mục và sản phẩm - MDG-003 compliant",
            entities=[category, product],
        )

    def _create_inventory_module(self) -> DomainModule:
        """Create inventory management module."""
        # Warehouse entity
        warehouse = DomainEntity(
            name="Warehouse",
            vietnamese_name="Kho hàng",
            description="Kho lưu trữ hàng hóa",
            fields=[
                DomainField(
                    name="code",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã kho",
                    description="Mã kho duy nhất",
                    required=True,
                    max_length=20,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên kho",
                    description="Tên kho hàng",
                    required=True,
                    max_length=100,
                ),
                DomainField(
                    name="address",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Địa chỉ",
                    description="Địa chỉ kho hàng",
                ),
                DomainField(
                    name="phone",
                    field_type=FieldType.STRING,
                    vietnamese_name="Điện thoại",
                    description="Số điện thoại liên hệ",
                    max_length=20,
                ),
                DomainField(
                    name="manager_name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Thủ kho",
                    description="Tên người quản lý kho",
                    max_length=100,
                ),
                DomainField(
                    name="warehouse_type",
                    field_type=FieldType.STRING,
                    vietnamese_name="Loại kho",
                    description="Loại kho hàng",
                    max_length=50,
                    choices=[
                        "main",         # Kho chính
                        "branch",       # Kho chi nhánh
                        "transit",      # Kho trung chuyển
                        "return",       # Kho hàng trả
                    ],
                    default="main",
                ),
                DomainField(
                    name="is_active",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Đang hoạt động",
                    description="Kho có đang hoạt động không",
                    default=True,
                ),
            ],
        )

        # Inventory entity
        inventory = DomainEntity(
            name="Inventory",
            vietnamese_name="Tồn kho",
            description="Số lượng tồn kho sản phẩm theo kho",
            fields=[
                DomainField(
                    name="product_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Sản phẩm",
                    description="ID sản phẩm",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="warehouse_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Kho",
                    description="ID kho hàng",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="quantity",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số lượng tồn",
                    description="Số lượng tồn kho hiện tại",
                    required=True,
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="reserved_quantity",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số lượng giữ",
                    description="Số lượng đang giữ cho đơn hàng",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="available_quantity",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số lượng khả dụng",
                    description="Số lượng có thể bán (tồn - giữ)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="min_stock",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Tồn tối thiểu",
                    description="Số lượng tồn tối thiểu (cảnh báo)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="max_stock",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Tồn tối đa",
                    description="Số lượng tồn tối đa",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="reorder_point",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Điểm đặt hàng",
                    description="Mức tồn kho cần đặt hàng thêm",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="unit_cost",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá vốn đơn vị",
                    description="Giá vốn bình quân (FIFO/WAC)",
                    min_value=0,
                ),
                DomainField(
                    name="total_value",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá trị tồn kho",
                    description="Tổng giá trị tồn kho (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="location",
                    field_type=FieldType.STRING,
                    vietnamese_name="Vị trí",
                    description="Vị trí trong kho (kệ, ô)",
                    max_length=50,
                ),
                DomainField(
                    name="last_counted_at",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Kiểm kê lần cuối",
                    description="Thời điểm kiểm kê gần nhất",
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="product",
                    target="Product",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Sản phẩm",
                    description="Sản phẩm tồn kho",
                ),
                DomainRelationship(
                    name="warehouse",
                    target="Warehouse",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Kho",
                    description="Kho chứa hàng",
                ),
            ],
        )

        # StockMovement entity
        stock_movement = DomainEntity(
            name="StockMovement",
            vietnamese_name="Phiếu xuất nhập kho",
            description="Ghi nhận xuất nhập kho",
            fields=[
                DomainField(
                    name="movement_code",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã phiếu",
                    description="Mã phiếu xuất/nhập kho",
                    required=True,
                    max_length=50,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="movement_type",
                    field_type=FieldType.STRING,
                    vietnamese_name="Loại phiếu",
                    description="Loại xuất/nhập",
                    required=True,
                    max_length=50,
                    choices=[
                        "purchase_in",      # Nhập mua
                        "sale_out",         # Xuất bán
                        "return_in",        # Nhập trả hàng
                        "return_out",       # Xuất trả NCC
                        "transfer_in",      # Nhập chuyển kho
                        "transfer_out",     # Xuất chuyển kho
                        "adjustment_in",    # Điều chỉnh tăng
                        "adjustment_out",   # Điều chỉnh giảm
                        "damage_out",       # Xuất hàng hỏng
                    ],
                    indexed=True,
                ),
                DomainField(
                    name="product_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Sản phẩm",
                    description="ID sản phẩm",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="warehouse_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Kho",
                    description="ID kho hàng",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="quantity",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số lượng",
                    description="Số lượng xuất/nhập",
                    required=True,
                ),
                DomainField(
                    name="unit_cost",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Đơn giá",
                    description="Đơn giá xuất/nhập",
                    min_value=0,
                ),
                DomainField(
                    name="total_value",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Thành tiền",
                    description="Tổng giá trị (VND)",
                    min_value=0,
                ),
                DomainField(
                    name="reference_type",
                    field_type=FieldType.STRING,
                    vietnamese_name="Loại chứng từ",
                    description="Loại chứng từ liên quan",
                    max_length=50,
                    choices=[
                        "purchase_order",   # Đơn mua hàng
                        "sale_order",       # Đơn bán hàng
                        "transfer",         # Phiếu chuyển kho
                        "adjustment",       # Phiếu điều chỉnh
                    ],
                ),
                DomainField(
                    name="reference_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Mã chứng từ",
                    description="ID chứng từ liên quan",
                    indexed=True,
                ),
                DomainField(
                    name="notes",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Ghi chú",
                    description="Ghi chú phiếu",
                ),
                DomainField(
                    name="movement_date",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Ngày xuất/nhập",
                    description="Thời điểm xuất/nhập kho",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="created_by",
                    field_type=FieldType.UUID,
                    vietnamese_name="Người tạo",
                    description="ID người tạo phiếu",
                ),
            ],
        )

        return DomainModule(
            name="inventory",
            vietnamese_name="Tồn kho",
            description="Quản lý kho hàng và xuất nhập kho",
            entities=[warehouse, inventory, stock_movement],
        )

    def _create_sale_module(self) -> DomainModule:
        """Create sales management module (MP-002 O2C compliant)."""
        # Sale entity
        sale = DomainEntity(
            name="Sale",
            vietnamese_name="Đơn bán hàng",
            description="Đơn bán hàng - tuân thủ MP-002 O2C",
            fields=[
                DomainField(
                    name="order_number",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã đơn hàng",
                    description="Mã đơn bán hàng duy nhất",
                    required=True,
                    max_length=50,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="customer_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Khách hàng",
                    description="ID khách hàng",
                    indexed=True,
                ),
                DomainField(
                    name="customer_name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên khách",
                    description="Tên khách hàng (snapshot)",
                    max_length=200,
                ),
                DomainField(
                    name="customer_phone",
                    field_type=FieldType.STRING,
                    vietnamese_name="SĐT khách",
                    description="Số điện thoại khách",
                    max_length=20,
                ),
                DomainField(
                    name="customer_email",
                    field_type=FieldType.STRING,
                    vietnamese_name="Email khách",
                    description="Email khách hàng",
                    max_length=200,
                ),
                DomainField(
                    name="shipping_address",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Địa chỉ giao hàng",
                    description="Địa chỉ giao hàng",
                ),
                DomainField(
                    name="billing_address",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Địa chỉ xuất hóa đơn",
                    description="Địa chỉ xuất hóa đơn",
                ),
                DomainField(
                    name="warehouse_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Kho xuất",
                    description="ID kho xuất hàng",
                    indexed=True,
                ),
                DomainField(
                    name="channel",
                    field_type=FieldType.STRING,
                    vietnamese_name="Kênh bán",
                    description="Kênh bán hàng",
                    max_length=50,
                    choices=[
                        "pos",          # Tại cửa hàng
                        "website",      # Website
                        "shopee",       # Shopee
                        "lazada",       # Lazada
                        "tiki",         # Tiki
                        "facebook",     # Facebook
                        "zalo",         # Zalo
                        "phone",        # Điện thoại
                    ],
                    default="pos",
                    indexed=True,
                ),
                DomainField(
                    name="status",
                    field_type=FieldType.STRING,
                    vietnamese_name="Trạng thái",
                    description="Trạng thái đơn hàng",
                    required=True,
                    max_length=50,
                    default="draft",
                    choices=[
                        "draft",        # Nháp
                        "confirmed",    # Đã xác nhận
                        "processing",   # Đang xử lý
                        "shipped",      # Đã giao hàng
                        "delivered",    # Đã nhận hàng
                        "completed",    # Hoàn thành
                        "cancelled",    # Đã hủy
                        "returned",     # Đã trả hàng
                    ],
                    indexed=True,
                ),
                DomainField(
                    name="subtotal",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tạm tính",
                    description="Tổng tiền hàng trước giảm giá (VND)",
                    required=True,
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="discount_percent",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="% Giảm giá",
                    description="Phần trăm giảm giá",
                    min_value=0,
                    max_value=100,
                    default=0,
                ),
                DomainField(
                    name="discount_amount",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền giảm",
                    description="Số tiền giảm giá (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="coupon_code",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã giảm giá",
                    description="Mã coupon áp dụng",
                    max_length=50,
                ),
                DomainField(
                    name="shipping_fee",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Phí vận chuyển",
                    description="Phí giao hàng (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="tax_amount",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền thuế",
                    description="Tiền thuế VAT (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="total",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tổng cộng",
                    description="Tổng tiền thanh toán (VND)",
                    required=True,
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="paid_amount",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Đã thanh toán",
                    description="Số tiền đã thanh toán (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="payment_status",
                    field_type=FieldType.STRING,
                    vietnamese_name="Trạng thái thanh toán",
                    description="Tình trạng thanh toán",
                    required=True,
                    max_length=50,
                    default="unpaid",
                    choices=[
                        "unpaid",       # Chưa thanh toán
                        "partial",      # Thanh toán một phần
                        "paid",         # Đã thanh toán
                        "refunded",     # Đã hoàn tiền
                    ],
                    indexed=True,
                ),
                DomainField(
                    name="payment_method",
                    field_type=FieldType.STRING,
                    vietnamese_name="Phương thức thanh toán",
                    description="Hình thức thanh toán",
                    max_length=50,
                    choices=[
                        "cash",         # Tiền mặt
                        "card",         # Thẻ
                        "bank_transfer",# Chuyển khoản
                        "momo",         # MoMo
                        "zalopay",      # ZaloPay
                        "vnpay",        # VNPay
                        "cod",          # COD
                    ],
                ),
                DomainField(
                    name="shipping_method",
                    field_type=FieldType.STRING,
                    vietnamese_name="Phương thức giao hàng",
                    description="Hình thức giao hàng",
                    max_length=50,
                    choices=[
                        "pickup",       # Nhận tại cửa hàng
                        "standard",     # Giao hàng tiêu chuẩn
                        "express",      # Giao nhanh
                        "same_day",     # Giao trong ngày
                    ],
                    default="standard",
                ),
                DomainField(
                    name="shipping_carrier",
                    field_type=FieldType.STRING,
                    vietnamese_name="Đơn vị vận chuyển",
                    description="Đơn vị giao hàng",
                    max_length=100,
                    choices=[
                        "self",         # Tự giao
                        "ghn",          # GHN
                        "ghtk",         # GHTK
                        "vnpost",       # VNPost
                        "jt",           # J&T
                        "ninja_van",    # Ninja Van
                    ],
                ),
                DomainField(
                    name="tracking_number",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã vận đơn",
                    description="Mã tracking vận chuyển",
                    max_length=100,
                ),
                DomainField(
                    name="notes",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Ghi chú",
                    description="Ghi chú đơn hàng",
                ),
                DomainField(
                    name="internal_notes",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Ghi chú nội bộ",
                    description="Ghi chú dành cho nhân viên",
                ),
                DomainField(
                    name="invoice_number",
                    field_type=FieldType.STRING,
                    vietnamese_name="Số hóa đơn",
                    description="Số hóa đơn VAT (nếu xuất)",
                    max_length=50,
                    indexed=True,
                ),
                DomainField(
                    name="invoice_date",
                    field_type=FieldType.DATE,
                    vietnamese_name="Ngày hóa đơn",
                    description="Ngày xuất hóa đơn VAT",
                ),
                DomainField(
                    name="order_date",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Ngày đặt hàng",
                    description="Thời điểm đặt hàng",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="shipped_at",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Ngày giao hàng",
                    description="Thời điểm giao hàng",
                ),
                DomainField(
                    name="delivered_at",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Ngày nhận hàng",
                    description="Thời điểm khách nhận hàng",
                ),
                DomainField(
                    name="sales_person_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Nhân viên bán hàng",
                    description="ID nhân viên bán",
                    indexed=True,
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="customer",
                    target="Customer",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Khách hàng",
                    description="Khách mua hàng",
                ),
                DomainRelationship(
                    name="items",
                    target="SaleItem",
                    relation_type=RelationType.ONE_TO_MANY,
                    vietnamese_name="Sản phẩm",
                    description="Danh sách sản phẩm trong đơn",
                    cascade=True,
                ),
            ],
        )

        # SaleItem entity
        sale_item = DomainEntity(
            name="SaleItem",
            vietnamese_name="Chi tiết đơn hàng",
            description="Từng sản phẩm trong đơn bán hàng",
            fields=[
                DomainField(
                    name="sale_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Đơn hàng",
                    description="ID đơn bán hàng",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="product_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Sản phẩm",
                    description="ID sản phẩm",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="product_sku",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã SKU",
                    description="Mã sản phẩm tại thời điểm bán",
                    required=True,
                    max_length=50,
                ),
                DomainField(
                    name="product_name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên sản phẩm",
                    description="Tên sản phẩm tại thời điểm bán",
                    required=True,
                    max_length=200,
                ),
                DomainField(
                    name="unit_price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Đơn giá",
                    description="Giá bán tại thời điểm (VND)",
                    required=True,
                    min_value=0,
                ),
                DomainField(
                    name="quantity",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số lượng",
                    description="Số lượng mua",
                    required=True,
                    min_value=1,
                    default=1,
                ),
                DomainField(
                    name="discount_percent",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="% Giảm giá",
                    description="Phần trăm giảm giá dòng",
                    min_value=0,
                    max_value=100,
                    default=0,
                ),
                DomainField(
                    name="discount_amount",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền giảm",
                    description="Số tiền giảm giá dòng (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="subtotal",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Thành tiền",
                    description="Đơn giá x Số lượng - Giảm giá (VND)",
                    required=True,
                    min_value=0,
                ),
                DomainField(
                    name="vat_rate",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Thuế suất",
                    description="Thuế suất VAT (%)",
                    min_value=0,
                    max_value=100,
                    default=10,
                ),
                DomainField(
                    name="vat_amount",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền thuế",
                    description="Tiền thuế VAT dòng (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="cost_price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá vốn",
                    description="Giá vốn sản phẩm (VND)",
                    min_value=0,
                ),
                DomainField(
                    name="notes",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Ghi chú",
                    description="Ghi chú cho dòng sản phẩm",
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="sale",
                    target="Sale",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Đơn hàng",
                    description="Thuộc đơn hàng nào",
                ),
                DomainRelationship(
                    name="product",
                    target="Product",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Sản phẩm",
                    description="Sản phẩm bán",
                ),
            ],
        )

        return DomainModule(
            name="sales",
            vietnamese_name="Bán hàng",
            description="Quản lý đơn bán hàng - MP-002 O2C compliant",
            entities=[sale, sale_item],
        )

    def _create_customer_module(self) -> DomainModule:
        """Create customer management module (MDP-005 compliant)."""
        customer = DomainEntity(
            name="Customer",
            vietnamese_name="Khách hàng",
            description="Thông tin khách hàng - tuân thủ MDP-005",
            fields=[
                DomainField(
                    name="customer_code",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã khách hàng",
                    description="Mã khách hàng duy nhất (CUS-XXXX)",
                    required=True,
                    max_length=50,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="customer_type",
                    field_type=FieldType.STRING,
                    vietnamese_name="Loại khách",
                    description="Loại khách hàng",
                    required=True,
                    max_length=50,
                    choices=[
                        "individual",   # Cá nhân
                        "company",      # Doanh nghiệp
                    ],
                    default="individual",
                ),
                DomainField(
                    name="full_name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Họ tên / Tên công ty",
                    description="Họ tên hoặc tên công ty",
                    required=True,
                    max_length=200,
                    indexed=True,
                ),
                DomainField(
                    name="phone",
                    field_type=FieldType.STRING,
                    vietnamese_name="Số điện thoại",
                    description="Số điện thoại chính",
                    required=True,
                    max_length=20,
                    indexed=True,
                ),
                DomainField(
                    name="email",
                    field_type=FieldType.STRING,
                    vietnamese_name="Email",
                    description="Địa chỉ email",
                    max_length=200,
                    indexed=True,
                ),
                DomainField(
                    name="tax_code",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã số thuế",
                    description="Mã số thuế (cho doanh nghiệp)",
                    max_length=20,
                    indexed=True,
                ),
                DomainField(
                    name="company_name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên công ty",
                    description="Tên công ty (cho xuất hóa đơn)",
                    max_length=200,
                ),
                DomainField(
                    name="address",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Địa chỉ",
                    description="Địa chỉ liên hệ",
                ),
                DomainField(
                    name="city",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tỉnh/Thành phố",
                    description="Tỉnh/Thành phố",
                    max_length=100,
                ),
                DomainField(
                    name="district",
                    field_type=FieldType.STRING,
                    vietnamese_name="Quận/Huyện",
                    description="Quận/Huyện",
                    max_length=100,
                ),
                DomainField(
                    name="ward",
                    field_type=FieldType.STRING,
                    vietnamese_name="Phường/Xã",
                    description="Phường/Xã",
                    max_length=100,
                ),
                DomainField(
                    name="date_of_birth",
                    field_type=FieldType.DATE,
                    vietnamese_name="Ngày sinh",
                    description="Ngày sinh (cá nhân)",
                ),
                DomainField(
                    name="gender",
                    field_type=FieldType.STRING,
                    vietnamese_name="Giới tính",
                    description="Giới tính",
                    max_length=20,
                    choices=[
                        "male",         # Nam
                        "female",       # Nữ
                        "other",        # Khác
                    ],
                ),
                DomainField(
                    name="customer_group",
                    field_type=FieldType.STRING,
                    vietnamese_name="Nhóm khách hàng",
                    description="Phân loại khách hàng",
                    max_length=50,
                    choices=[
                        "retail",       # Khách lẻ
                        "wholesale",    # Khách sỉ
                        "vip",          # Khách VIP
                        "agent",        # Đại lý
                    ],
                    default="retail",
                    indexed=True,
                ),
                DomainField(
                    name="loyalty_points",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Điểm tích lũy",
                    description="Điểm thưởng hiện có",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="total_orders",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Tổng đơn hàng",
                    description="Tổng số đơn hàng đã mua",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="total_spent",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tổng chi tiêu",
                    description="Tổng chi tiêu (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="average_order_value",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá trị TB/đơn",
                    description="Giá trị trung bình mỗi đơn (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="credit_limit",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Hạn mức công nợ",
                    description="Hạn mức công nợ tối đa (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="current_debt",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Công nợ hiện tại",
                    description="Công nợ đang có (VND)",
                    default=0,
                ),
                DomainField(
                    name="payment_terms",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Kỳ hạn thanh toán",
                    description="Số ngày được nợ",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="source",
                    field_type=FieldType.STRING,
                    vietnamese_name="Nguồn khách hàng",
                    description="Kênh đến với cửa hàng",
                    max_length=50,
                    choices=[
                        "walk_in",      # Đến trực tiếp
                        "referral",     # Giới thiệu
                        "facebook",     # Facebook
                        "google",       # Google
                        "shopee",       # Shopee
                        "lazada",       # Lazada
                        "other",        # Khác
                    ],
                ),
                DomainField(
                    name="notes",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Ghi chú",
                    description="Ghi chú về khách hàng",
                ),
                DomainField(
                    name="is_active",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Đang hoạt động",
                    description="Khách hàng có đang active không",
                    default=True,
                ),
                DomainField(
                    name="first_order_at",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Đơn hàng đầu tiên",
                    description="Thời điểm mua hàng lần đầu",
                ),
                DomainField(
                    name="last_order_at",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Đơn hàng gần nhất",
                    description="Thời điểm mua hàng gần nhất",
                    indexed=True,
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="sales",
                    target="Sale",
                    relation_type=RelationType.ONE_TO_MANY,
                    vietnamese_name="Đơn hàng",
                    description="Các đơn hàng của khách",
                ),
            ],
        )

        return DomainModule(
            name="customers",
            vietnamese_name="Khách hàng",
            description="Quản lý thông tin khách hàng - MDP-005 compliant",
            entities=[customer],
        )
