"""
CGF (Corporate Governance Framework) Metadata.

Sprint 47: Vietnamese SME Domain Templates
Reference: Bflow CGF V2.1, DAG V3.0, Simplified Code V2.0

This module provides CGF metadata for domain templates, including:
- Master Process (MP) mappings
- Master Data Governance (MDG) compliance
- DAG (Delegation of Authority Grid) levels
- Vietnamese Cultural Intelligence (CI) constants

CGF Framework Philosophy:
> "CGF là khung quản trị tổng quát, KHÔNG PHỤ THUỘC vào tools và công nghệ"
> (CGF is a general governance framework, NOT DEPENDENT on tools and technology)

Author: Backend Lead
Date: December 23, 2025
Version: 1.0.0
Status: ACTIVE - Sprint 47 Implementation
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class ProcessTier(str, Enum):
    """Master Process tier classification."""
    TIER_1_CORE = "tier_1_core"         # Mandatory for ALL businesses
    TIER_2_EXTENDED = "tier_2_extended"  # Optional based on company size
    TIER_3_INDUSTRY = "tier_3_industry"  # Industry-specific add-ons


class MDGDomain(str, Enum):
    """Master Data Governance domains (MDG-001 to MDG-005)."""
    ORG_HR = "MDG-001"          # Organization & HR Governance
    PROCUREMENT = "MDG-002"     # Procurement Governance
    PRODUCT_PRICING = "MDG-003" # Product & Pricing Governance
    SITE_LOCATION = "MDG-004"   # Site/Location Master
    INDUSTRY_CLASS = "MDG-005"  # Industry Classification


class DAGLevel(int, Enum):
    """DAG (Delegation of Authority Grid) approval levels."""
    LEVEL_1 = 1  # Staff / Team Member
    LEVEL_2 = 2  # Supervisor / Team Lead
    LEVEL_3 = 3  # Manager / Department Head
    LEVEL_4 = 4  # Director / C-Level
    LEVEL_5 = 5  # Board / CEO


@dataclass
class MasterProcess:
    """
    Master Process definition from CGF V2.1.

    Master Processes are standardized business processes that
    apply across industries with industry-specific variations.
    """
    id: str                     # MP-001, MP-002, etc.
    name: str                   # English name
    name_vi: str                # Vietnamese name
    tier: ProcessTier           # Tier classification
    description: str            # Process description
    kernel: str                 # Process kernel (P2P, O2C, etc.)
    workflows: int              # Number of standard workflows
    industries: List[str]       # Applicable industries
    mdg_integration: List[str]  # MDG dependencies
    vietnamese_ci: Dict         # Vietnamese CI constants


@dataclass
class CGFDomainMapping:
    """
    CGF Domain Mapping for code generation.

    Maps domain templates to CGF Master Processes, MDG, and DAG levels.
    """
    domain: str                          # Domain name (restaurant, hotel, retail)
    master_processes: List[str]          # Primary MPs (e.g., MP-002, MP-010)
    mdg_compliance: List[str]            # Required MDG templates
    dag_levels: Dict[str, DAGLevel]      # Entity → DAG level for CRUD
    vietnamese_ci: Dict                  # Vietnamese CI constants
    code_structure: Dict[str, str]       # Entity → Code format (e.g., PRD-XXXX)


# =============================================================================
# Master Process Registry (CGF V2.1)
# =============================================================================

MASTER_PROCESSES: Dict[str, MasterProcess] = {
    # TIER 1 - CORE (Mandatory)
    "MP-001": MasterProcess(
        id="MP-001",
        name="Procure-to-Pay (P2P)",
        name_vi="Quy trình Mua hàng đến Thanh toán",
        tier=ProcessTier.TIER_1_CORE,
        description="End-to-end procurement process from purchase requisition to payment",
        kernel="P2P",
        workflows=34,
        industries=["all"],
        mdg_integration=["MDG-002", "MDG-004"],
        vietnamese_ci={
            "vat_input": True,
            "supplier_compliance": True,
        },
    ),
    "MP-002": MasterProcess(
        id="MP-002",
        name="Order-to-Cash (O2C)",
        name_vi="Quy trình Đơn hàng đến Thu tiền",
        tier=ProcessTier.TIER_1_CORE,
        description="End-to-end sales process from order to payment collection",
        kernel="O2C",
        workflows=15,
        industries=["all"],
        mdg_integration=["MDG-003", "MDG-004"],
        vietnamese_ci={
            "vat_output": True,
            "e_invoice": True,
        },
    ),
    "MP-003": MasterProcess(
        id="MP-003",
        name="Plan-to-Consume (P2C)",
        name_vi="Quy trình Kế hoạch đến Tiêu thụ",
        tier=ProcessTier.TIER_1_CORE,
        description="Production planning to consumption/delivery",
        kernel="P2C",
        workflows=28,
        industries=["manufacturing", "retail", "restaurant"],
        mdg_integration=["MDG-002", "MDG-003"],
        vietnamese_ci={
            "inventory_vas": True,
            "fifo_costing": True,
        },
    ),
    "MP-004": MasterProcess(
        id="MP-004",
        name="Hire-to-Retire (H2R)",
        name_vi="Quy trình Tuyển dụng đến Nghỉ hưu",
        tier=ProcessTier.TIER_1_CORE,
        description="Complete employee lifecycle management",
        kernel="H2R",
        workflows=18,
        industries=["all"],
        mdg_integration=["MDG-001"],
        vietnamese_ci={
            "labor_code": True,
            "bhxh_employer": "17.5%",
            "bhxh_employee": "8%",
            "severance": True,
        },
    ),
    "MP-005": MasterProcess(
        id="MP-005",
        name="Issue-to-Resolution (I2R)",
        name_vi="Quy trình Vấn đề đến Giải quyết",
        tier=ProcessTier.TIER_1_CORE,
        description="IT service management and issue resolution",
        kernel="I2R",
        workflows=7,
        industries=["all"],
        mdg_integration=["MDG-001"],
        vietnamese_ci={
            "sla_compliance": True,
        },
    ),
    "MP-006": MasterProcess(
        id="MP-006",
        name="Lead-to-Cash (L2C)",
        name_vi="Quy trình Tiềm năng đến Thu tiền",
        tier=ProcessTier.TIER_1_CORE,
        description="CRM process from lead to customer conversion",
        kernel="L2C",
        workflows=22,
        industries=["all"],
        mdg_integration=["MDG-003", "MDG-005"],
        vietnamese_ci={
            "crm_compliance": True,
        },
    ),
    "MP-007": MasterProcess(
        id="MP-007",
        name="Record-to-Report (Close)",
        name_vi="Quy trình Ghi nhận đến Báo cáo",
        tier=ProcessTier.TIER_1_CORE,
        description="Month-end close and financial reporting",
        kernel="R2R",
        workflows=5,
        industries=["all"],
        mdg_integration=["MDG-004"],
        vietnamese_ci={
            "vas_compliance": True,
            "tax_reporting": True,
        },
    ),
    "MP-008": MasterProcess(
        id="MP-008",
        name="Payroll Processing",
        name_vi="Quy trình Xử lý Lương",
        tier=ProcessTier.TIER_1_CORE,
        description="Payroll calculation and disbursement",
        kernel="Payroll",
        workflows=8,
        industries=["all"],
        mdg_integration=["MDG-001"],
        vietnamese_ci={
            "bhxh_employer": "17.5%",
            "bhxh_employee": "8%",
            "pit_withholding": True,
            "labor_code": True,
        },
    ),

    # TIER 2 - EXTENDED (Optional)
    "MP-009": MasterProcess(
        id="MP-009",
        name="Intercompany Processing",
        name_vi="Quy trình Liên công ty",
        tier=ProcessTier.TIER_2_EXTENDED,
        description="Intercompany transactions and reconciliation",
        kernel="INTERCO",
        workflows=10,
        industries=["all"],
        mdg_integration=["MDG-004"],
        vietnamese_ci={
            "transfer_pricing": True,
            "interco_vat": True,
        },
    ),
    "MP-010": MasterProcess(
        id="MP-010",
        name="Source-to-Evaluate (S2E)",
        name_vi="Quy trình Tìm kiếm đến Đánh giá",
        tier=ProcessTier.TIER_2_EXTENDED,
        description="Supplier sourcing and evaluation",
        kernel="S2E",
        workflows=8,
        industries=["all"],
        mdg_integration=["MDG-002"],
        vietnamese_ci={
            "supplier_audit": True,
        },
    ),

    # TIER 3 - INDUSTRY (Add-ons)
    "MP-011": MasterProcess(
        id="MP-011",
        name="Guest-to-Departure (G2D)",
        name_vi="Quy trình Khách đến Trả phòng",
        tier=ProcessTier.TIER_3_INDUSTRY,
        description="Hotel guest journey from check-in to departure",
        kernel="G2D",
        workflows=12,
        industries=["hotel", "hospitality"],
        mdg_integration=["MDG-003", "MDG-005"],
        vietnamese_ci={
            "tourism_regulations": True,
            "vat_hospitality": True,
        },
    ),
    "MP-012": MasterProcess(
        id="MP-012",
        name="Service-to-Settlement (S2S)",
        name_vi="Quy trình Dịch vụ đến Thanh toán",
        tier=ProcessTier.TIER_3_INDUSTRY,
        description="Service delivery to payment settlement",
        kernel="S2S",
        workflows=10,
        industries=["professional_services", "restaurant"],
        mdg_integration=["MDG-003"],
        vietnamese_ci={
            "service_vat": True,
            "contract_compliance": True,
        },
    ),
    "MP-013": MasterProcess(
        id="MP-013",
        name="Material-to-Dispatch (M2D)",
        name_vi="Quy trình Nguyên liệu đến Xuất hàng",
        tier=ProcessTier.TIER_3_INDUSTRY,
        description="Manufacturing from raw materials to dispatch",
        kernel="M2D",
        workflows=15,
        industries=["manufacturing"],
        mdg_integration=["MDG-002", "MDG-003"],
        vietnamese_ci={
            "fifo_costing": True,
            "inventory_vas": True,
        },
    ),
    "MP-014": MasterProcess(
        id="MP-014",
        name="Quality-to-Ship (Q2S)",
        name_vi="Quy trình Chất lượng đến Giao hàng",
        tier=ProcessTier.TIER_3_INDUSTRY,
        description="Quality control to shipping",
        kernel="Q2S",
        workflows=8,
        industries=["manufacturing"],
        mdg_integration=["MDG-003"],
        vietnamese_ci={
            "qc_standards": True,
            "export_compliance": True,
        },
    ),
    "MP-015": MasterProcess(
        id="MP-015",
        name="Reserve-to-Fulfill (R2F)",
        name_vi="Quy trình Đặt chỗ đến Phục vụ",
        tier=ProcessTier.TIER_3_INDUSTRY,
        description="Reservation to service fulfillment",
        kernel="R2F",
        workflows=8,
        industries=["restaurant", "hotel", "professional_services"],
        mdg_integration=["MDG-003", "MDG-005"],
        vietnamese_ci={
            "reservation_law": True,
            "consumer_protection": True,
        },
    ),
}


# =============================================================================
# Domain → CGF Mappings
# =============================================================================

CGF_DOMAIN_MAPPINGS: Dict[str, CGFDomainMapping] = {
    "restaurant": CGFDomainMapping(
        domain="restaurant",
        master_processes=["MP-002", "MP-003", "MP-012", "MP-015"],
        mdg_compliance=["MDG-002", "MDG-003", "MDG-005"],
        dag_levels={
            "MenuItem": DAGLevel.LEVEL_2,    # Supervisor can CRUD menu items
            "Order": DAGLevel.LEVEL_1,       # Staff can create orders
            "Table": DAGLevel.LEVEL_2,       # Supervisor manages tables
            "Reservation": DAGLevel.LEVEL_1, # Staff handles reservations
            "Category": DAGLevel.LEVEL_3,    # Manager approves categories
        },
        vietnamese_ci={
            "vat_rate": "10%",
            "service_charge": "5%",
            "food_safety": True,
            "labor_code": True,
        },
        code_structure={
            "MenuItem": "PRD-XXXX",
            "Category": "CAT-XXXX",
            "Order": "ORD-XXXXXXXX",  # Date-based
            "Table": "TBL-XXX",
            "Reservation": "RSV-XXXXXXXX",
        },
    ),

    "hotel": CGFDomainMapping(
        domain="hotel",
        master_processes=["MP-002", "MP-011", "MP-015"],
        mdg_compliance=["MDG-001", "MDG-003", "MDG-004", "MDG-005"],
        dag_levels={
            "Room": DAGLevel.LEVEL_3,        # Manager manages rooms
            "RoomType": DAGLevel.LEVEL_4,    # Director approves room types
            "Booking": DAGLevel.LEVEL_2,     # Supervisor handles bookings
            "Guest": DAGLevel.LEVEL_1,       # Staff registers guests
            "Billing": DAGLevel.LEVEL_2,     # Supervisor approves billing
            "Service": DAGLevel.LEVEL_3,     # Manager manages services
        },
        vietnamese_ci={
            "vat_rate": "10%",
            "tourism_tax": True,
            "temporary_residence": True,  # Đăng ký tạm trú
            "labor_code": True,
        },
        code_structure={
            "Room": "RM-XXX",
            "RoomType": "RT-XX",
            "Booking": "BKG-XXXXXXXX",
            "Guest": "GST-XXXX",
            "Billing": "INV-XXXXXXXX",
            "Service": "SVC-XXX",
        },
    ),

    "retail": CGFDomainMapping(
        domain="retail",
        master_processes=["MP-001", "MP-002", "MP-003", "MP-006"],
        mdg_compliance=["MDG-002", "MDG-003", "MDG-004", "MDG-005"],
        dag_levels={
            "Product": DAGLevel.LEVEL_2,     # Supervisor manages products
            "Category": DAGLevel.LEVEL_3,    # Manager approves categories
            "Inventory": DAGLevel.LEVEL_2,   # Supervisor manages inventory
            "Warehouse": DAGLevel.LEVEL_4,   # Director approves warehouses
            "StockMovement": DAGLevel.LEVEL_2,  # Supervisor approves movements
            "Sale": DAGLevel.LEVEL_1,        # Staff creates sales
            "SaleItem": DAGLevel.LEVEL_1,    # Staff adds items
            "Customer": DAGLevel.LEVEL_1,    # Staff registers customers
        },
        vietnamese_ci={
            "vat_rate": "10%",
            "e_invoice": True,
            "fifo_costing": True,
            "consumer_protection": True,
        },
        code_structure={
            "Product": "PRD-XXXX",
            "Category": "CAT-XXX",
            "Warehouse": "WH-XX",
            "Inventory": "INV-XXXXXX",
            "StockMovement": "STK-XXXXXXXX",
            "Sale": "SO-XXXXXXXX",
            "Customer": "CUS-XXXX",
        },
    ),
}


# =============================================================================
# Vietnamese Cultural Intelligence (CI) Constants
# =============================================================================

VIETNAMESE_CI = {
    "bhxh": {
        "employer_rate": "17.5%",
        "employee_rate": "8%",
        "breakdown": {
            "social_insurance_employer": "14%",
            "health_insurance_employer": "3%",
            "unemployment_insurance_employer": "0.5%",
            "social_insurance_employee": "8%",
            "health_insurance_employee": "1.5%",
            "unemployment_insurance_employee": "1%",
        },
        "reference": "Decree 58/2020/ND-CP",
    },
    "vat": {
        "standard_rate": "10%",
        "reduced_rate": "5%",
        "zero_rate": "0%",
        "reference": "VAT Law 13/2008, Circular 219/2013",
    },
    "pit": {
        "progressive_rates": [
            {"bracket": "0-5M", "rate": "5%"},
            {"bracket": "5-10M", "rate": "10%"},
            {"bracket": "10-18M", "rate": "15%"},
            {"bracket": "18-32M", "rate": "20%"},
            {"bracket": "32-52M", "rate": "25%"},
            {"bracket": "52-80M", "rate": "30%"},
            {"bracket": ">80M", "rate": "35%"},
        ],
        "reference": "PIT Law 04/2007, Decree 65/2013",
    },
    "currency": {
        "code": "VND",
        "symbol": "₫",
        "thousand_separator": ".",
        "decimal_separator": ",",
        "decimals": 0,
    },
    "labor_code": {
        "reference": "Bộ Luật Lao Động 45/2019/QH14",
        "effective_date": "2021-01-01",
        "standard_hours": 48,
        "overtime_rates": {
            "weekday": "150%",
            "weekend": "200%",
            "holiday": "300%",
        },
    },
}


def get_domain_cgf_mapping(domain: str) -> Optional[CGFDomainMapping]:
    """Get CGF mapping for a domain."""
    return CGF_DOMAIN_MAPPINGS.get(domain)


def get_master_process(mp_id: str) -> Optional[MasterProcess]:
    """Get Master Process by ID."""
    return MASTER_PROCESSES.get(mp_id)


def get_domain_master_processes(domain: str) -> List[MasterProcess]:
    """Get all Master Processes for a domain."""
    mapping = get_domain_cgf_mapping(domain)
    if not mapping:
        return []
    return [
        MASTER_PROCESSES[mp_id]
        for mp_id in mapping.master_processes
        if mp_id in MASTER_PROCESSES
    ]


def get_entity_dag_level(domain: str, entity: str) -> Optional[DAGLevel]:
    """Get DAG approval level for an entity in a domain."""
    mapping = get_domain_cgf_mapping(domain)
    if not mapping:
        return None
    return mapping.dag_levels.get(entity)


def get_entity_code_structure(domain: str, entity: str) -> Optional[str]:
    """Get code structure (e.g., PRD-XXXX) for an entity."""
    mapping = get_domain_cgf_mapping(domain)
    if not mapping:
        return None
    return mapping.code_structure.get(entity)
