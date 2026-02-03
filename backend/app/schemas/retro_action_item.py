"""
=========================================================================
Retrospective Action Item Schemas
SDLC Orchestrator - Sprint 78 Day 1

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 78 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)

Purpose:
- Pydantic schemas for RetroActionItem CRUD operations
- Validation for action item fields
- Response schemas for API endpoints

Design Reference:
docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
=========================================================================
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ============================================================
# Enums as string literals for validation
# ============================================================

VALID_CATEGORIES = [
    "delivery",
    "priority",
    "velocity",
    "planning",
    "scope",
    "blockers",
    "team",
    "general",
]

VALID_PRIORITIES = ["low", "medium", "high"]

VALID_STATUSES = ["open", "in_progress", "completed", "cancelled"]


# ============================================================
# Base Schema
# ============================================================


class RetroActionItemBase(BaseModel):
    """Base schema for RetroActionItem with shared fields."""

    title: str = Field(..., min_length=1, max_length=255, description="Action item title")
    description: Optional[str] = Field(None, description="Detailed description")
    category: str = Field(
        "general",
        description="Category: delivery, priority, velocity, planning, scope, blockers, team, general",
    )
    priority: str = Field("medium", description="Priority: low, medium, high")

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        if v not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of: {', '.join(VALID_CATEGORIES)}")
        return v

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        if v not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of: {', '.join(VALID_PRIORITIES)}")
        return v


# ============================================================
# Create Schema
# ============================================================


class RetroActionItemCreate(RetroActionItemBase):
    """Schema for creating a new RetroActionItem."""

    sprint_id: UUID = Field(..., description="Source sprint ID where action was identified")
    assignee_id: Optional[UUID] = Field(None, description="User ID of assignee")
    due_sprint_id: Optional[UUID] = Field(None, description="Target sprint for completion")


# ============================================================
# Update Schema
# ============================================================


class RetroActionItemUpdate(BaseModel):
    """Schema for updating an existing RetroActionItem."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assignee_id: Optional[UUID] = None
    due_sprint_id: Optional[UUID] = None

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of: {', '.join(VALID_CATEGORIES)}")
        return v

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of: {', '.join(VALID_PRIORITIES)}")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_STATUSES:
            raise ValueError(f"status must be one of: {', '.join(VALID_STATUSES)}")
        return v


# ============================================================
# Response Schemas
# ============================================================


class RetroActionItemResponse(RetroActionItemBase):
    """Response schema for RetroActionItem."""

    id: UUID
    sprint_id: UUID
    status: str
    assignee_id: Optional[UUID] = None
    due_sprint_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class RetroActionItemWithDetails(RetroActionItemResponse):
    """Response schema with related entities."""

    sprint_number: Optional[int] = None
    sprint_name: Optional[str] = None
    assignee_name: Optional[str] = None
    due_sprint_number: Optional[int] = None
    due_sprint_name: Optional[str] = None


class RetroActionItemListResponse(BaseModel):
    """Response schema for listing action items."""

    items: List[RetroActionItemResponse]
    total: int
    page: int = 1
    page_size: int = 20


# ============================================================
# Bulk Operations
# ============================================================


class RetroActionItemBulkCreate(BaseModel):
    """Schema for creating multiple action items at once."""

    sprint_id: UUID
    items: List[RetroActionItemBase]


class RetroActionItemBulkStatusUpdate(BaseModel):
    """Schema for bulk status update."""

    ids: List[UUID]
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in VALID_STATUSES:
            raise ValueError(f"status must be one of: {', '.join(VALID_STATUSES)}")
        return v


# ============================================================
# Statistics Schema
# ============================================================


class RetroActionItemStats(BaseModel):
    """Statistics for retrospective action items."""

    total_items: int = 0
    open_items: int = 0
    in_progress_items: int = 0
    completed_items: int = 0
    cancelled_items: int = 0
    completion_rate: float = 0.0
    by_category: dict = Field(default_factory=dict)
    by_priority: dict = Field(default_factory=dict)
