"""
F&B (Food & Beverage) Domain Template.

Sprint 47: Vietnamese SME Domain Templates
ADR-023: IR-Based Deterministic Code Generation

Domain-specific template for Vietnamese F&B businesses:
- Restaurants (Nhà hàng)
- Cafés (Quán cà phê)
- Bars (Quán bar)
- Food courts (Khu ẩm thực)

Entities:
- Menu/MenuItem: Quản lý thực đơn
- Order/OrderItem: Quản lý đơn hàng
- Table: Quản lý bàn
- Reservation: Quản lý đặt bàn
- Category: Danh mục món ăn
- Staff: Nhân viên phục vụ

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
class FnBDomainTemplate(DomainTemplate):
    """
    F&B Domain Template for Vietnamese restaurants, cafés, and bars.

    Provides complete entity structure for:
    - Menu management (Thực đơn)
    - Order management (Đơn hàng)
    - Table management (Bàn)
    - Reservation management (Đặt bàn)

    Target: Vietnamese SME F&B businesses
    Price tier: Founder Plan ($99/team/month)
    """

    @property
    def domain_name(self) -> str:
        return "restaurant"

    @property
    def vietnamese_name(self) -> str:
        return "Nhà hàng / Quán ăn"

    @property
    def description(self) -> str:
        return (
            "Mẫu ứng dụng quản lý nhà hàng, quán cà phê, quán bar. "
            "Bao gồm quản lý thực đơn, đơn hàng, bàn và đặt bàn."
        )

    def get_modules(self) -> List[DomainModule]:
        """Get all F&B domain modules."""
        return [
            self._create_menu_module(),
            self._create_order_module(),
            self._create_table_module(),
            self._create_reservation_module(),
        ]

    def _create_menu_module(self) -> DomainModule:
        """Create menu management module."""
        # Category entity
        category = DomainEntity(
            name="Category",
            vietnamese_name="Danh mục",
            description="Danh mục phân loại món ăn/đồ uống",
            fields=[
                DomainField(
                    name="name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên danh mục",
                    description="Tên danh mục (VD: Món khai vị, Đồ uống)",
                    required=True,
                    max_length=100,
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
                    name="image_url",
                    field_type=FieldType.STRING,
                    vietnamese_name="Ảnh đại diện",
                    description="URL ảnh đại diện danh mục",
                    max_length=500,
                ),
                DomainField(
                    name="display_order",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Thứ tự hiển thị",
                    description="Thứ tự sắp xếp trên menu",
                    default=0,
                ),
                DomainField(
                    name="is_active",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Đang hoạt động",
                    description="Danh mục có hiển thị trên menu không",
                    default=True,
                ),
            ],
        )

        # MenuItem entity
        menu_item = DomainEntity(
            name="MenuItem",
            vietnamese_name="Món ăn",
            description="Chi tiết từng món trong thực đơn",
            fields=[
                DomainField(
                    name="name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên món",
                    description="Tên món ăn/đồ uống",
                    required=True,
                    max_length=200,
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
                    description="Mô tả chi tiết món ăn, nguyên liệu",
                ),
                DomainField(
                    name="price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá bán",
                    description="Giá bán (VND)",
                    required=True,
                    min_value=0,
                ),
                DomainField(
                    name="original_price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá gốc",
                    description="Giá gốc trước giảm giá (VND)",
                    min_value=0,
                ),
                DomainField(
                    name="image_url",
                    field_type=FieldType.STRING,
                    vietnamese_name="Ảnh món ăn",
                    description="URL ảnh món ăn",
                    max_length=500,
                ),
                DomainField(
                    name="preparation_time",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Thời gian chuẩn bị",
                    description="Thời gian chuẩn bị (phút)",
                    min_value=0,
                    default=15,
                ),
                DomainField(
                    name="calories",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Calo",
                    description="Số calo trong món",
                    min_value=0,
                ),
                DomainField(
                    name="is_vegetarian",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Món chay",
                    description="Có phải món chay không",
                    default=False,
                ),
                DomainField(
                    name="is_spicy",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Món cay",
                    description="Có phải món cay không",
                    default=False,
                ),
                DomainField(
                    name="is_bestseller",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Bán chạy",
                    description="Món bán chạy nhất",
                    default=False,
                ),
                DomainField(
                    name="is_available",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Còn phục vụ",
                    description="Món có sẵn để phục vụ không",
                    default=True,
                ),
                DomainField(
                    name="display_order",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Thứ tự hiển thị",
                    description="Thứ tự sắp xếp trong danh mục",
                    default=0,
                ),
                DomainField(
                    name="category_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Danh mục",
                    description="ID danh mục chứa món này",
                    required=True,
                    indexed=True,
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="category",
                    target="Category",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Thuộc danh mục",
                    description="Món ăn thuộc danh mục nào",
                ),
            ],
        )

        return DomainModule(
            name="menu",
            vietnamese_name="Thực đơn",
            description="Quản lý danh mục và các món trong thực đơn",
            entities=[category, menu_item],
        )

    def _create_order_module(self) -> DomainModule:
        """Create order management module."""
        # Order entity
        order = DomainEntity(
            name="Order",
            vietnamese_name="Đơn hàng",
            description="Đơn hàng của khách",
            fields=[
                DomainField(
                    name="order_number",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã đơn hàng",
                    description="Mã đơn hàng duy nhất (auto-generated)",
                    required=True,
                    max_length=50,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="table_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Bàn",
                    description="ID bàn đặt món",
                    indexed=True,
                ),
                DomainField(
                    name="customer_name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên khách",
                    description="Tên khách hàng (nếu có)",
                    max_length=200,
                ),
                DomainField(
                    name="customer_phone",
                    field_type=FieldType.STRING,
                    vietnamese_name="SĐT khách",
                    description="Số điện thoại khách hàng",
                    max_length=20,
                ),
                DomainField(
                    name="status",
                    field_type=FieldType.STRING,
                    vietnamese_name="Trạng thái",
                    description="Trạng thái đơn hàng",
                    required=True,
                    max_length=50,
                    default="pending",
                    choices=[
                        "pending",      # Chờ xác nhận
                        "confirmed",    # Đã xác nhận
                        "preparing",    # Đang chuẩn bị
                        "ready",        # Sẵn sàng phục vụ
                        "served",       # Đã phục vụ
                        "completed",    # Hoàn thành
                        "cancelled",    # Đã hủy
                    ],
                    indexed=True,
                ),
                DomainField(
                    name="order_type",
                    field_type=FieldType.STRING,
                    vietnamese_name="Loại đơn",
                    description="Loại đơn hàng",
                    required=True,
                    max_length=50,
                    default="dine_in",
                    choices=[
                        "dine_in",      # Tại quán
                        "takeaway",     # Mang đi
                        "delivery",     # Giao hàng
                    ],
                ),
                DomainField(
                    name="subtotal",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tạm tính",
                    description="Tổng tiền trước thuế/phí (VND)",
                    required=True,
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="tax_amount",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Thuế",
                    description="Tiền thuế (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="service_charge",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Phí dịch vụ",
                    description="Phí dịch vụ (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="discount_amount",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giảm giá",
                    description="Số tiền giảm giá (VND)",
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
                    name="payment_method",
                    field_type=FieldType.STRING,
                    vietnamese_name="Phương thức thanh toán",
                    description="Hình thức thanh toán",
                    max_length=50,
                    choices=[
                        "cash",         # Tiền mặt
                        "card",         # Thẻ ngân hàng
                        "momo",         # MoMo
                        "zalopay",      # ZaloPay
                        "vnpay",        # VNPay
                        "bank_transfer",# Chuyển khoản
                    ],
                ),
                DomainField(
                    name="payment_status",
                    field_type=FieldType.STRING,
                    vietnamese_name="Trạng thái thanh toán",
                    description="Đã thanh toán chưa",
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
                    name="notes",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Ghi chú",
                    description="Ghi chú đặc biệt từ khách",
                ),
                DomainField(
                    name="staff_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Nhân viên phục vụ",
                    description="ID nhân viên phục vụ",
                    indexed=True,
                ),
                DomainField(
                    name="ordered_at",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Thời gian đặt",
                    description="Thời gian khách đặt món",
                ),
                DomainField(
                    name="completed_at",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Thời gian hoàn thành",
                    description="Thời gian hoàn thành đơn hàng",
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="table",
                    target="Table",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Bàn",
                    description="Đơn hàng thuộc bàn nào",
                ),
                DomainRelationship(
                    name="items",
                    target="OrderItem",
                    relation_type=RelationType.ONE_TO_MANY,
                    vietnamese_name="Các món",
                    description="Danh sách món trong đơn",
                    cascade=True,
                ),
            ],
        )

        # OrderItem entity
        order_item = DomainEntity(
            name="OrderItem",
            vietnamese_name="Chi tiết đơn hàng",
            description="Từng món trong đơn hàng",
            fields=[
                DomainField(
                    name="order_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Đơn hàng",
                    description="ID đơn hàng",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="menu_item_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Món ăn",
                    description="ID món ăn",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="item_name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên món",
                    description="Tên món tại thời điểm đặt (snapshot)",
                    required=True,
                    max_length=200,
                ),
                DomainField(
                    name="unit_price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Đơn giá",
                    description="Giá tại thời điểm đặt (VND)",
                    required=True,
                    min_value=0,
                ),
                DomainField(
                    name="quantity",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số lượng",
                    description="Số lượng món đặt",
                    required=True,
                    min_value=1,
                    default=1,
                ),
                DomainField(
                    name="subtotal",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Thành tiền",
                    description="Đơn giá x Số lượng (VND)",
                    required=True,
                    min_value=0,
                ),
                DomainField(
                    name="status",
                    field_type=FieldType.STRING,
                    vietnamese_name="Trạng thái",
                    description="Trạng thái món",
                    required=True,
                    max_length=50,
                    default="pending",
                    choices=[
                        "pending",      # Chờ chuẩn bị
                        "preparing",    # Đang chuẩn bị
                        "ready",        # Sẵn sàng
                        "served",       # Đã phục vụ
                        "cancelled",    # Đã hủy
                    ],
                ),
                DomainField(
                    name="notes",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Ghi chú",
                    description="Yêu cầu đặc biệt (ít cay, không hành,...)",
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="order",
                    target="Order",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Thuộc đơn hàng",
                    description="Món thuộc đơn hàng nào",
                ),
                DomainRelationship(
                    name="menu_item",
                    target="MenuItem",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Món ăn",
                    description="Tham chiếu đến món trong menu",
                ),
            ],
        )

        return DomainModule(
            name="orders",
            vietnamese_name="Đơn hàng",
            description="Quản lý đơn hàng và chi tiết món đặt",
            entities=[order, order_item],
        )

    def _create_table_module(self) -> DomainModule:
        """Create table management module."""
        table = DomainEntity(
            name="Table",
            vietnamese_name="Bàn",
            description="Quản lý bàn trong nhà hàng",
            fields=[
                DomainField(
                    name="table_number",
                    field_type=FieldType.STRING,
                    vietnamese_name="Số bàn",
                    description="Số hiệu bàn (VD: A1, B2, VIP1)",
                    required=True,
                    max_length=20,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên bàn",
                    description="Tên mô tả bàn (VD: Bàn cửa sổ)",
                    max_length=100,
                ),
                DomainField(
                    name="capacity",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Sức chứa",
                    description="Số người tối đa",
                    required=True,
                    min_value=1,
                    default=4,
                ),
                DomainField(
                    name="zone",
                    field_type=FieldType.STRING,
                    vietnamese_name="Khu vực",
                    description="Khu vực đặt bàn",
                    max_length=50,
                    choices=[
                        "indoor",       # Trong nhà
                        "outdoor",      # Ngoài trời
                        "vip",          # Phòng VIP
                        "rooftop",      # Sân thượng
                        "garden",       # Sân vườn
                    ],
                    default="indoor",
                ),
                DomainField(
                    name="status",
                    field_type=FieldType.STRING,
                    vietnamese_name="Trạng thái",
                    description="Trạng thái hiện tại của bàn",
                    required=True,
                    max_length=50,
                    default="available",
                    choices=[
                        "available",    # Trống
                        "occupied",     # Có khách
                        "reserved",     # Đã đặt trước
                        "cleaning",     # Đang dọn
                        "unavailable",  # Không khả dụng
                    ],
                    indexed=True,
                ),
                DomainField(
                    name="floor",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Tầng",
                    description="Tầng đặt bàn",
                    default=1,
                ),
                DomainField(
                    name="position_x",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Vị trí X",
                    description="Tọa độ X trên sơ đồ",
                ),
                DomainField(
                    name="position_y",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Vị trí Y",
                    description="Tọa độ Y trên sơ đồ",
                ),
                DomainField(
                    name="qr_code",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã QR",
                    description="Mã QR để khách tự order",
                    max_length=500,
                ),
                DomainField(
                    name="is_active",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Đang hoạt động",
                    description="Bàn có được sử dụng không",
                    default=True,
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="orders",
                    target="Order",
                    relation_type=RelationType.ONE_TO_MANY,
                    vietnamese_name="Đơn hàng",
                    description="Các đơn hàng tại bàn này",
                ),
                DomainRelationship(
                    name="reservations",
                    target="Reservation",
                    relation_type=RelationType.ONE_TO_MANY,
                    vietnamese_name="Đặt bàn",
                    description="Các lượt đặt bàn",
                ),
            ],
        )

        return DomainModule(
            name="tables",
            vietnamese_name="Bàn",
            description="Quản lý bàn và vị trí trong nhà hàng",
            entities=[table],
        )

    def _create_reservation_module(self) -> DomainModule:
        """Create reservation management module."""
        reservation = DomainEntity(
            name="Reservation",
            vietnamese_name="Đặt bàn",
            description="Quản lý đặt bàn trước",
            fields=[
                DomainField(
                    name="reservation_code",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã đặt bàn",
                    description="Mã đặt bàn duy nhất",
                    required=True,
                    max_length=50,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="customer_name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên khách",
                    description="Họ tên người đặt",
                    required=True,
                    max_length=200,
                ),
                DomainField(
                    name="customer_phone",
                    field_type=FieldType.STRING,
                    vietnamese_name="SĐT",
                    description="Số điện thoại liên hệ",
                    required=True,
                    max_length=20,
                    indexed=True,
                ),
                DomainField(
                    name="customer_email",
                    field_type=FieldType.STRING,
                    vietnamese_name="Email",
                    description="Email (tùy chọn)",
                    max_length=200,
                ),
                DomainField(
                    name="table_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Bàn",
                    description="ID bàn được đặt",
                    indexed=True,
                ),
                DomainField(
                    name="party_size",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số khách",
                    description="Số lượng khách",
                    required=True,
                    min_value=1,
                    default=2,
                ),
                DomainField(
                    name="reservation_date",
                    field_type=FieldType.DATE,
                    vietnamese_name="Ngày đặt",
                    description="Ngày dự kiến đến",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="reservation_time",
                    field_type=FieldType.STRING,
                    vietnamese_name="Giờ đặt",
                    description="Giờ dự kiến đến (HH:MM)",
                    required=True,
                    max_length=10,
                ),
                DomainField(
                    name="duration_minutes",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Thời gian dự kiến",
                    description="Thời gian sử dụng bàn (phút)",
                    default=120,
                    min_value=30,
                ),
                DomainField(
                    name="status",
                    field_type=FieldType.STRING,
                    vietnamese_name="Trạng thái",
                    description="Trạng thái đặt bàn",
                    required=True,
                    max_length=50,
                    default="pending",
                    choices=[
                        "pending",      # Chờ xác nhận
                        "confirmed",    # Đã xác nhận
                        "arrived",      # Khách đã đến
                        "completed",    # Hoàn thành
                        "cancelled",    # Đã hủy
                        "no_show",      # Khách không đến
                    ],
                    indexed=True,
                ),
                DomainField(
                    name="special_requests",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Yêu cầu đặc biệt",
                    description="Ghi chú từ khách (sinh nhật, kỷ niệm,...)",
                ),
                DomainField(
                    name="deposit_amount",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền cọc",
                    description="Số tiền đặt cọc (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="deposit_paid",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Đã cọc",
                    description="Đã nhận tiền cọc chưa",
                    default=False,
                ),
                DomainField(
                    name="source",
                    field_type=FieldType.STRING,
                    vietnamese_name="Nguồn đặt",
                    description="Kênh nhận đặt bàn",
                    max_length=50,
                    choices=[
                        "phone",        # Gọi điện
                        "website",      # Website
                        "app",          # Ứng dụng
                        "walk_in",      # Đến trực tiếp
                        "facebook",     # Facebook
                        "zalo",         # Zalo
                    ],
                    default="phone",
                ),
                DomainField(
                    name="confirmed_by",
                    field_type=FieldType.UUID,
                    vietnamese_name="Người xác nhận",
                    description="ID nhân viên xác nhận",
                ),
                DomainField(
                    name="confirmed_at",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Thời gian xác nhận",
                    description="Thời điểm xác nhận đặt bàn",
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="table",
                    target="Table",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Bàn đặt",
                    description="Bàn được đặt trước",
                ),
            ],
        )

        return DomainModule(
            name="reservations",
            vietnamese_name="Đặt bàn",
            description="Quản lý đặt bàn trước và xác nhận",
            entities=[reservation],
        )
