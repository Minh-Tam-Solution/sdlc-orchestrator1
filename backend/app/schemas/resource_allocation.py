"""
=========================================================================
Resource Allocation Schemas
SDLC Orchestrator - Sprint 78 Day 3

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 78 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)

Purpose:
- Pydantic schemas for ResourceAllocation CRUD operations
- Capacity calculation schemas
- Conflict detection response schemas

Design Reference:
docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
=========================================================================
"""

from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ============================================================
# Valid values
# ============================================================

VALID_ROLES = [
    "developer",
    "qa",
    "designer",
    "pm",
    "tech_lead",
    "devops",
    "analyst",
    "other",
]


# ============================================================
# Base Schema
# ============================================================


class ResourceAllocationBase(BaseModel):
    """Base schema for ResourceAllocation with shared fields."""

    allocation_percentage: int = Field(
        100,
        ge=1,
        le=100,
        description="Allocation percentage (1-100)",
    )
    role: str = Field(
        "developer",
        description="Role: developer, qa, designer, pm, tech_lead, devops, analyst, other",
    )
    notes: Optional[str] = Field(None, max_length=500)

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in VALID_ROLES:
            raise ValueError(f"role must be one of: {', '.join(VALID_ROLES)}")
        return v


# ============================================================
# Create Schema
# ============================================================


class ResourceAllocationCreate(ResourceAllocationBase):
    """Schema for creating a new ResourceAllocation."""

    sprint_id: UUID = Field(..., description="Sprint to allocate to")
    user_id: UUID = Field(..., description="User being allocated")
    start_date: Optional[date] = Field(None, description="Start date (defaults to sprint start)")
    end_date: Optional[date] = Field(None, description="End date (defaults to sprint end)")


# ============================================================
# Update Schema
# ============================================================


class ResourceAllocationUpdate(BaseModel):
    """Schema for updating an existing ResourceAllocation."""

    allocation_percentage: Optional[int] = Field(None, ge=1, le=100)
    role: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_ROLES:
            raise ValueError(f"role must be one of: {', '.join(VALID_ROLES)}")
        return v


# ============================================================
# Response Schemas
# ============================================================


class ResourceAllocationResponse(ResourceAllocationBase):
    """Response schema for ResourceAllocation."""

    id: UUID
    sprint_id: UUID
    user_id: UUID
    start_date: date
    end_date: date
    created_by_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ResourceAllocationWithDetails(ResourceAllocationResponse):
    """Response schema with user and sprint details."""

    user_name: Optional[str] = None
    user_email: Optional[str] = None
    sprint_number: Optional[int] = None
    sprint_name: Optional[str] = None
    project_id: Optional[UUID] = None
    project_name: Optional[str] = None


class ResourceAllocationListResponse(BaseModel):
    """Response schema for listing allocations."""

    items: List[ResourceAllocationResponse]
    total: int
    page: int = 1
    page_size: int = 20


# ============================================================
# Capacity Schemas
# ============================================================


class UserCapacity(BaseModel):
    """Capacity information for a single user."""

    user_id: UUID
    user_name: str
    user_email: str
    total_days: int = Field(..., description="Total working days in period")
    allocated_days: float = Field(..., description="Days allocated (considering %)")
    available_days: float = Field(..., description="Available days remaining")
    utilization_rate: float = Field(..., description="Utilization percentage (0-100)")
    allocations: List[ResourceAllocationResponse] = []


class TeamCapacity(BaseModel):
    """Capacity information for a team."""

    team_id: UUID
    team_name: str
    start_date: date
    end_date: date
    total_members: int
    total_capacity_hours: float = Field(..., description="Total team hours")
    allocated_hours: float = Field(..., description="Hours allocated")
    available_hours: float = Field(..., description="Hours remaining")
    utilization_rate: float = Field(..., description="Utilization percentage (0-100)")
    members: List[UserCapacity] = []

    # By role breakdown
    by_role: dict = Field(default_factory=dict, description="Capacity breakdown by role")


class SprintCapacity(BaseModel):
    """Capacity information for a sprint."""

    sprint_id: UUID
    sprint_number: int
    sprint_name: str
    start_date: date
    end_date: date
    team_size: int = Field(..., description="Number of allocated team members")
    total_capacity_hours: float
    allocated_hours: float
    available_hours: float
    utilization_rate: float

    # Breakdown
    by_role: dict = Field(default_factory=dict)
    allocations: List[ResourceAllocationWithDetails] = []


# ============================================================
# Conflict Detection Schemas
# ============================================================


class AllocationConflict(BaseModel):
    """Detected allocation conflict."""

    user_id: UUID
    user_name: str
    conflict_type: str = Field(..., description="Type: over_allocation, double_booking")
    total_allocation: int = Field(..., description="Total allocation percentage")
    conflicting_sprints: List[str] = Field(..., description="Sprint names involved")
    conflicting_dates: str = Field(..., description="Date range of conflict")
    message: str


class ConflictCheckResult(BaseModel):
    """Result of conflict detection check."""

    has_conflicts: bool
    conflicts: List[AllocationConflict] = []
    warnings: List[str] = []


# ============================================================
# Bulk Operations
# ============================================================


class ResourceAllocationBulkCreate(BaseModel):
    """Schema for bulk creating allocations."""

    sprint_id: UUID
    allocations: List[ResourceAllocationBase]
    user_ids: List[UUID] = Field(..., description="Users to allocate")


class ResourceAllocationBulkResult(BaseModel):
    """Result of bulk operation."""

    success_count: int
    failure_count: int
    conflicts: List[AllocationConflict] = []
    errors: List[dict] = []


# ============================================================
# Capacity Forecast
# ============================================================


class CapacityForecast(BaseModel):
    """Capacity forecast for upcoming sprints."""

    forecast_date: date
    sprints: List[SprintCapacity] = []
    recommendations: List[str] = []
    warnings: List[str] = []


class ResourceHeatmapCell(BaseModel):
    """Single cell in resource heatmap."""

    user_id: UUID
    user_name: str
    sprint_id: UUID
    sprint_number: int
    allocation_percentage: int
    role: str
    status: str = Field(..., description="Status: available, partial, full, over_allocated")


class ResourceHeatmap(BaseModel):
    """Resource allocation heatmap data."""

    users: List[dict] = Field(..., description="List of users (rows)")
    sprints: List[dict] = Field(..., description="List of sprints (columns)")
    cells: List[ResourceHeatmapCell] = []
    total_conflicts: int = 0
