"""
Hospitality Domain Template.

Sprint 47: Vietnamese SME Domain Templates
ADR-023: IR-Based Deterministic Code Generation

Domain-specific template for Vietnamese hospitality businesses:
- Hotels (Khách sạn)
- Homestays (Homestay / Nhà nghỉ)
- Resorts (Resort)
- Serviced apartments (Căn hộ dịch vụ)

Entities:
- Room: Quản lý phòng
- RoomType: Loại phòng
- Booking: Đặt phòng
- Guest: Khách hàng
- Billing: Hóa đơn/Thanh toán
- Service: Dịch vụ bổ sung

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
class HospitalityDomainTemplate(DomainTemplate):
    """
    Hospitality Domain Template for Vietnamese hotels and homestays.

    Provides complete entity structure for:
    - Room management (Phòng)
    - Booking management (Đặt phòng)
    - Guest management (Khách hàng)
    - Billing management (Thanh toán)

    Target: Vietnamese SME hospitality businesses
    Price tier: Founder Plan ($99/team/month)
    """

    @property
    def domain_name(self) -> str:
        return "hotel"

    @property
    def vietnamese_name(self) -> str:
        return "Khách sạn / Homestay"

    @property
    def description(self) -> str:
        return (
            "Mẫu ứng dụng quản lý khách sạn, homestay, resort. "
            "Bao gồm quản lý phòng, đặt phòng, khách hàng và thanh toán."
        )

    def get_modules(self) -> List[DomainModule]:
        """Get all hospitality domain modules."""
        return [
            self._create_room_module(),
            self._create_booking_module(),
            self._create_guest_module(),
            self._create_billing_module(),
        ]

    def _create_room_module(self) -> DomainModule:
        """Create room management module."""
        # RoomType entity
        room_type = DomainEntity(
            name="RoomType",
            vietnamese_name="Loại phòng",
            description="Phân loại phòng theo tiện nghi và giá",
            fields=[
                DomainField(
                    name="name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên loại phòng",
                    description="VD: Phòng Standard, Deluxe, Suite",
                    required=True,
                    max_length=100,
                ),
                DomainField(
                    name="code",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã loại phòng",
                    description="Mã ngắn (VD: STD, DLX, SUI)",
                    required=True,
                    max_length=20,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="description",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Mô tả",
                    description="Mô tả chi tiết tiện nghi phòng",
                ),
                DomainField(
                    name="base_price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá cơ bản",
                    description="Giá phòng/đêm (VND)",
                    required=True,
                    min_value=0,
                ),
                DomainField(
                    name="weekend_price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá cuối tuần",
                    description="Giá phòng cuối tuần/đêm (VND)",
                    min_value=0,
                ),
                DomainField(
                    name="holiday_price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá lễ",
                    description="Giá phòng ngày lễ/đêm (VND)",
                    min_value=0,
                ),
                DomainField(
                    name="max_occupancy",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số người tối đa",
                    description="Số khách tối đa/phòng",
                    required=True,
                    min_value=1,
                    default=2,
                ),
                DomainField(
                    name="max_adults",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số người lớn",
                    description="Số người lớn tối đa",
                    min_value=1,
                    default=2,
                ),
                DomainField(
                    name="max_children",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số trẻ em",
                    description="Số trẻ em tối đa",
                    min_value=0,
                    default=1,
                ),
                DomainField(
                    name="bed_type",
                    field_type=FieldType.STRING,
                    vietnamese_name="Loại giường",
                    description="Loại giường trong phòng",
                    max_length=100,
                    choices=[
                        "single",       # Giường đơn
                        "double",       # Giường đôi
                        "twin",         # 2 giường đơn
                        "queen",        # Giường Queen
                        "king",         # Giường King
                        "bunk",         # Giường tầng
                    ],
                ),
                DomainField(
                    name="room_size",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Diện tích",
                    description="Diện tích phòng (m²)",
                    min_value=0,
                ),
                DomainField(
                    name="amenities",
                    field_type=FieldType.JSON,
                    vietnamese_name="Tiện nghi",
                    description="Danh sách tiện nghi (WiFi, AC, TV,...)",
                ),
                DomainField(
                    name="images",
                    field_type=FieldType.JSON,
                    vietnamese_name="Hình ảnh",
                    description="Danh sách URL ảnh phòng",
                ),
                DomainField(
                    name="is_active",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Đang hoạt động",
                    description="Loại phòng có đang kinh doanh không",
                    default=True,
                ),
            ],
        )

        # Room entity
        room = DomainEntity(
            name="Room",
            vietnamese_name="Phòng",
            description="Phòng cụ thể trong khách sạn",
            fields=[
                DomainField(
                    name="room_number",
                    field_type=FieldType.STRING,
                    vietnamese_name="Số phòng",
                    description="Số hiệu phòng (VD: 101, 201A)",
                    required=True,
                    max_length=20,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="room_type_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Loại phòng",
                    description="ID loại phòng",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="floor",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Tầng",
                    description="Tầng đặt phòng",
                    required=True,
                    min_value=0,
                ),
                DomainField(
                    name="building",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tòa nhà",
                    description="Tên tòa nhà/khu vực (nếu có nhiều)",
                    max_length=50,
                ),
                DomainField(
                    name="status",
                    field_type=FieldType.STRING,
                    vietnamese_name="Trạng thái",
                    description="Trạng thái hiện tại của phòng",
                    required=True,
                    max_length=50,
                    default="available",
                    choices=[
                        "available",    # Trống sẵn sàng
                        "occupied",     # Có khách
                        "reserved",     # Đã đặt
                        "cleaning",     # Đang dọn
                        "maintenance",  # Bảo trì
                        "out_of_order", # Hỏng
                    ],
                    indexed=True,
                ),
                DomainField(
                    name="housekeeping_status",
                    field_type=FieldType.STRING,
                    vietnamese_name="Trạng thái dọn phòng",
                    description="Tình trạng vệ sinh phòng",
                    max_length=50,
                    default="clean",
                    choices=[
                        "clean",        # Sạch
                        "dirty",        # Chưa dọn
                        "inspected",    # Đã kiểm tra
                        "in_progress",  # Đang dọn
                    ],
                ),
                DomainField(
                    name="view_type",
                    field_type=FieldType.STRING,
                    vietnamese_name="Hướng view",
                    description="Hướng nhìn của phòng",
                    max_length=50,
                    choices=[
                        "city",         # View thành phố
                        "sea",          # View biển
                        "mountain",     # View núi
                        "garden",       # View vườn
                        "pool",         # View hồ bơi
                        "none",         # Không có view
                    ],
                ),
                DomainField(
                    name="notes",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Ghi chú",
                    description="Ghi chú về phòng",
                ),
                DomainField(
                    name="is_smoking",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Phòng hút thuốc",
                    description="Phòng cho phép hút thuốc không",
                    default=False,
                ),
                DomainField(
                    name="is_active",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Đang hoạt động",
                    description="Phòng có đang kinh doanh không",
                    default=True,
                ),
                DomainField(
                    name="last_cleaned_at",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Dọn lần cuối",
                    description="Thời điểm dọn phòng gần nhất",
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="room_type",
                    target="RoomType",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Loại phòng",
                    description="Phòng thuộc loại nào",
                ),
                DomainRelationship(
                    name="bookings",
                    target="Booking",
                    relation_type=RelationType.ONE_TO_MANY,
                    vietnamese_name="Đặt phòng",
                    description="Các lượt đặt phòng này",
                ),
            ],
        )

        return DomainModule(
            name="rooms",
            vietnamese_name="Phòng",
            description="Quản lý loại phòng và phòng cụ thể",
            entities=[room_type, room],
        )

    def _create_booking_module(self) -> DomainModule:
        """Create booking management module."""
        booking = DomainEntity(
            name="Booking",
            vietnamese_name="Đặt phòng",
            description="Quản lý đặt phòng của khách",
            fields=[
                DomainField(
                    name="booking_code",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã đặt phòng",
                    description="Mã đặt phòng duy nhất",
                    required=True,
                    max_length=50,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="guest_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Khách hàng",
                    description="ID khách đặt phòng",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="room_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Phòng",
                    description="ID phòng được đặt",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="check_in_date",
                    field_type=FieldType.DATE,
                    vietnamese_name="Ngày nhận phòng",
                    description="Ngày dự kiến nhận phòng",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="check_out_date",
                    field_type=FieldType.DATE,
                    vietnamese_name="Ngày trả phòng",
                    description="Ngày dự kiến trả phòng",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="actual_check_in",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Giờ nhận thực tế",
                    description="Thời điểm khách nhận phòng thực tế",
                ),
                DomainField(
                    name="actual_check_out",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Giờ trả thực tế",
                    description="Thời điểm khách trả phòng thực tế",
                ),
                DomainField(
                    name="num_adults",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số người lớn",
                    description="Số người lớn",
                    required=True,
                    min_value=1,
                    default=1,
                ),
                DomainField(
                    name="num_children",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số trẻ em",
                    description="Số trẻ em",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="status",
                    field_type=FieldType.STRING,
                    vietnamese_name="Trạng thái",
                    description="Trạng thái đặt phòng",
                    required=True,
                    max_length=50,
                    default="pending",
                    choices=[
                        "pending",      # Chờ xác nhận
                        "confirmed",    # Đã xác nhận
                        "checked_in",   # Đã nhận phòng
                        "checked_out",  # Đã trả phòng
                        "cancelled",    # Đã hủy
                        "no_show",      # Khách không đến
                    ],
                    indexed=True,
                ),
                DomainField(
                    name="room_rate",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá phòng/đêm",
                    description="Giá phòng mỗi đêm (VND)",
                    required=True,
                    min_value=0,
                ),
                DomainField(
                    name="total_nights",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số đêm",
                    description="Tổng số đêm lưu trú",
                    required=True,
                    min_value=1,
                ),
                DomainField(
                    name="room_total",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền phòng",
                    description="Tổng tiền phòng (VND)",
                    required=True,
                    min_value=0,
                ),
                DomainField(
                    name="extra_charges",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Phụ thu",
                    description="Phụ thu (giường phụ, người thêm,...)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="services_total",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền dịch vụ",
                    description="Tổng tiền dịch vụ sử dụng",
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
                    name="tax_amount",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Thuế",
                    description="Tiền thuế (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="grand_total",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tổng cộng",
                    description="Tổng tiền thanh toán (VND)",
                    required=True,
                    min_value=0,
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
                    description="Kênh nhận đặt phòng",
                    max_length=50,
                    choices=[
                        "direct",       # Trực tiếp
                        "website",      # Website
                        "phone",        # Điện thoại
                        "booking_com",  # Booking.com
                        "agoda",        # Agoda
                        "traveloka",    # Traveloka
                        "airbnb",       # Airbnb
                        "other_ota",    # OTA khác
                    ],
                    default="direct",
                ),
                DomainField(
                    name="special_requests",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Yêu cầu đặc biệt",
                    description="Ghi chú yêu cầu từ khách",
                ),
                DomainField(
                    name="internal_notes",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Ghi chú nội bộ",
                    description="Ghi chú dành cho nhân viên",
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="guest",
                    target="Guest",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Khách hàng",
                    description="Khách đặt phòng",
                ),
                DomainRelationship(
                    name="room",
                    target="Room",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Phòng",
                    description="Phòng được đặt",
                ),
                DomainRelationship(
                    name="billing",
                    target="Billing",
                    relation_type=RelationType.ONE_TO_ONE,
                    vietnamese_name="Hóa đơn",
                    description="Hóa đơn thanh toán",
                ),
            ],
        )

        return DomainModule(
            name="bookings",
            vietnamese_name="Đặt phòng",
            description="Quản lý đặt phòng và check-in/check-out",
            entities=[booking],
        )

    def _create_guest_module(self) -> DomainModule:
        """Create guest management module."""
        guest = DomainEntity(
            name="Guest",
            vietnamese_name="Khách hàng",
            description="Thông tin khách lưu trú",
            fields=[
                DomainField(
                    name="guest_code",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã khách",
                    description="Mã khách hàng duy nhất",
                    required=True,
                    max_length=50,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="full_name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Họ tên",
                    description="Họ tên đầy đủ",
                    required=True,
                    max_length=200,
                    indexed=True,
                ),
                DomainField(
                    name="phone",
                    field_type=FieldType.STRING,
                    vietnamese_name="Số điện thoại",
                    description="Số điện thoại liên hệ",
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
                    name="id_type",
                    field_type=FieldType.STRING,
                    vietnamese_name="Loại giấy tờ",
                    description="Loại giấy tờ tùy thân",
                    max_length=50,
                    choices=[
                        "cmnd",         # CMND
                        "cccd",         # CCCD
                        "passport",     # Hộ chiếu
                        "driver_license", # Bằng lái xe
                    ],
                ),
                DomainField(
                    name="id_number",
                    field_type=FieldType.STRING,
                    vietnamese_name="Số giấy tờ",
                    description="Số CMND/CCCD/Hộ chiếu",
                    max_length=50,
                    indexed=True,
                ),
                DomainField(
                    name="nationality",
                    field_type=FieldType.STRING,
                    vietnamese_name="Quốc tịch",
                    description="Quốc tịch",
                    max_length=100,
                    default="Việt Nam",
                ),
                DomainField(
                    name="date_of_birth",
                    field_type=FieldType.DATE,
                    vietnamese_name="Ngày sinh",
                    description="Ngày tháng năm sinh",
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
                    name="address",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Địa chỉ",
                    description="Địa chỉ thường trú",
                ),
                DomainField(
                    name="company",
                    field_type=FieldType.STRING,
                    vietnamese_name="Công ty",
                    description="Tên công ty (nếu đi công tác)",
                    max_length=200,
                ),
                DomainField(
                    name="vip_level",
                    field_type=FieldType.STRING,
                    vietnamese_name="Hạng VIP",
                    description="Cấp độ khách VIP",
                    max_length=20,
                    choices=[
                        "normal",       # Thường
                        "silver",       # Bạc
                        "gold",         # Vàng
                        "platinum",     # Bạch kim
                    ],
                    default="normal",
                ),
                DomainField(
                    name="total_stays",
                    field_type=FieldType.INTEGER,
                    vietnamese_name="Số lần lưu trú",
                    description="Tổng số lần đã lưu trú",
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
                    name="preferences",
                    field_type=FieldType.JSON,
                    vietnamese_name="Sở thích",
                    description="Sở thích của khách (phòng không hút thuốc,...)",
                ),
                DomainField(
                    name="notes",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Ghi chú",
                    description="Ghi chú về khách",
                ),
                DomainField(
                    name="is_blacklisted",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Danh sách đen",
                    description="Khách có trong danh sách đen không",
                    default=False,
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="bookings",
                    target="Booking",
                    relation_type=RelationType.ONE_TO_MANY,
                    vietnamese_name="Đặt phòng",
                    description="Các lần đặt phòng của khách",
                ),
            ],
        )

        return DomainModule(
            name="guests",
            vietnamese_name="Khách hàng",
            description="Quản lý thông tin và lịch sử khách hàng",
            entities=[guest],
        )

    def _create_billing_module(self) -> DomainModule:
        """Create billing management module."""
        # Billing entity
        billing = DomainEntity(
            name="Billing",
            vietnamese_name="Hóa đơn",
            description="Hóa đơn thanh toán của khách",
            fields=[
                DomainField(
                    name="invoice_number",
                    field_type=FieldType.STRING,
                    vietnamese_name="Số hóa đơn",
                    description="Số hóa đơn duy nhất",
                    required=True,
                    max_length=50,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="booking_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Đặt phòng",
                    description="ID booking liên quan",
                    required=True,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="guest_id",
                    field_type=FieldType.UUID,
                    vietnamese_name="Khách hàng",
                    description="ID khách thanh toán",
                    required=True,
                    indexed=True,
                ),
                DomainField(
                    name="room_charges",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền phòng",
                    description="Tổng tiền phòng (VND)",
                    required=True,
                    min_value=0,
                ),
                DomainField(
                    name="service_charges",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền dịch vụ",
                    description="Tổng tiền dịch vụ (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="minibar_charges",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền minibar",
                    description="Tiền đồ uống minibar (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="laundry_charges",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền giặt ủi",
                    description="Tiền dịch vụ giặt ủi (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="restaurant_charges",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền nhà hàng",
                    description="Tiền ăn uống tại nhà hàng (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="other_charges",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Phí khác",
                    description="Các khoản phí khác (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="subtotal",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tạm tính",
                    description="Tổng trước thuế/giảm giá (VND)",
                    required=True,
                    min_value=0,
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
                    name="tax_percent",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="% Thuế",
                    description="Phần trăm thuế VAT",
                    min_value=0,
                    default=10,
                ),
                DomainField(
                    name="tax_amount",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tiền thuế",
                    description="Tiền thuế (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="grand_total",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Tổng cộng",
                    description="Tổng tiền thanh toán (VND)",
                    required=True,
                    min_value=0,
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
                    name="balance_due",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Còn nợ",
                    description="Số tiền còn phải trả (VND)",
                    min_value=0,
                    default=0,
                ),
                DomainField(
                    name="payment_status",
                    field_type=FieldType.STRING,
                    vietnamese_name="Trạng thái",
                    description="Trạng thái thanh toán",
                    required=True,
                    max_length=50,
                    default="unpaid",
                    choices=[
                        "unpaid",       # Chưa thanh toán
                        "partial",      # Thanh toán một phần
                        "paid",         # Đã thanh toán đủ
                        "refunded",     # Đã hoàn tiền
                    ],
                    indexed=True,
                ),
                DomainField(
                    name="payment_method",
                    field_type=FieldType.STRING,
                    vietnamese_name="Hình thức thanh toán",
                    description="Phương thức thanh toán",
                    max_length=50,
                    choices=[
                        "cash",         # Tiền mặt
                        "card",         # Thẻ
                        "bank_transfer",# Chuyển khoản
                        "momo",         # MoMo
                        "vnpay",        # VNPay
                        "ota",          # OTA thu hộ
                    ],
                ),
                DomainField(
                    name="paid_at",
                    field_type=FieldType.DATETIME,
                    vietnamese_name="Ngày thanh toán",
                    description="Thời điểm thanh toán đủ",
                ),
                DomainField(
                    name="notes",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Ghi chú",
                    description="Ghi chú hóa đơn",
                ),
            ],
            relationships=[
                DomainRelationship(
                    name="booking",
                    target="Booking",
                    relation_type=RelationType.ONE_TO_ONE,
                    vietnamese_name="Đặt phòng",
                    description="Booking liên quan",
                ),
                DomainRelationship(
                    name="guest",
                    target="Guest",
                    relation_type=RelationType.MANY_TO_ONE,
                    vietnamese_name="Khách hàng",
                    description="Khách thanh toán",
                ),
            ],
        )

        # Service entity
        service = DomainEntity(
            name="Service",
            vietnamese_name="Dịch vụ",
            description="Dịch vụ bổ sung trong khách sạn",
            fields=[
                DomainField(
                    name="name",
                    field_type=FieldType.STRING,
                    vietnamese_name="Tên dịch vụ",
                    description="Tên dịch vụ",
                    required=True,
                    max_length=200,
                ),
                DomainField(
                    name="code",
                    field_type=FieldType.STRING,
                    vietnamese_name="Mã dịch vụ",
                    description="Mã dịch vụ",
                    required=True,
                    max_length=50,
                    unique=True,
                    indexed=True,
                ),
                DomainField(
                    name="category",
                    field_type=FieldType.STRING,
                    vietnamese_name="Danh mục",
                    description="Loại dịch vụ",
                    max_length=50,
                    choices=[
                        "spa",          # Spa & Massage
                        "laundry",      # Giặt ủi
                        "transport",    # Đưa đón
                        "tour",         # Tour du lịch
                        "restaurant",   # Nhà hàng
                        "minibar",      # Minibar
                        "parking",      # Đỗ xe
                        "other",        # Khác
                    ],
                ),
                DomainField(
                    name="description",
                    field_type=FieldType.TEXT,
                    vietnamese_name="Mô tả",
                    description="Mô tả chi tiết dịch vụ",
                ),
                DomainField(
                    name="price",
                    field_type=FieldType.FLOAT,
                    vietnamese_name="Giá",
                    description="Giá dịch vụ (VND)",
                    required=True,
                    min_value=0,
                ),
                DomainField(
                    name="unit",
                    field_type=FieldType.STRING,
                    vietnamese_name="Đơn vị",
                    description="Đơn vị tính (lần, giờ, kg,...)",
                    max_length=50,
                    default="lần",
                ),
                DomainField(
                    name="is_active",
                    field_type=FieldType.BOOLEAN,
                    vietnamese_name="Đang hoạt động",
                    description="Dịch vụ có đang cung cấp không",
                    default=True,
                ),
            ],
        )

        return DomainModule(
            name="billing",
            vietnamese_name="Thanh toán",
            description="Quản lý hóa đơn và dịch vụ bổ sung",
            entities=[billing, service],
        )
