"""
=========================================================================
Sprint Template Schemas
SDLC Orchestrator - Sprint 78 Day 4

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 78 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)

Purpose:
- Pydantic schemas for SprintTemplate CRUD operations
- Validation for template configuration
- Response schemas for template listing and detail

Design Reference:
docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
=========================================================================
"""

from datetime import datetime, date
from typing import Optional, List, Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ============================================================
# Constants
# ============================================================

VALID_TEMPLATE_TYPES = ["standard", "feature", "bugfix", "release", "custom"]
VALID_BACKLOG_ITEM_TYPES = ["story", "task", "bug", "spike", "chore"]
VALID_PRIORITIES = ["P0", "P1", "P2", "P3"]


# ============================================================
# Backlog Item Schema (for template structure)
# ============================================================


class BacklogItemTemplate(BaseModel):
    """Schema for a backlog item in the template structure."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Item title",
    )
    type: str = Field(
        "task",
        description="Item type: story, task, bug, spike, chore",
    )
    priority: str = Field(
        "P2",
        description="Priority: P0, P1, P2, P3",
    )
    story_points: int = Field(
        0,
        ge=0,
        le=21,
        description="Story points (0-21)",
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Item description",
    )

    @field_validator("type")
    @classmethod
    def validate_item_type(cls, v: str) -> str:
        if v not in VALID_BACKLOG_ITEM_TYPES:
            raise ValueError(f"type must be one of: {', '.join(VALID_BACKLOG_ITEM_TYPES)}")
        return v

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        if v not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of: {', '.join(VALID_PRIORITIES)}")
        return v


# ============================================================
# Base Schema
# ============================================================


class SprintTemplateBase(BaseModel):
    """Base schema for SprintTemplate with shared fields."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Template name",
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Template description",
    )
    template_type: str = Field(
        "standard",
        description="Type: standard, feature, bugfix, release, custom",
    )
    duration_days: int = Field(
        10,
        ge=1,
        le=30,
        description="Sprint duration in days (1-30)",
    )
    default_capacity_points: int = Field(
        40,
        ge=0,
        le=200,
        description="Default story points capacity",
    )
    gates_enabled: bool = Field(
        True,
        description="Enable G-Sprint/G-Sprint-Close gates",
    )
    goal_template: Optional[str] = Field(
        None,
        max_length=500,
        description="Template for sprint goal",
    )
    is_public: bool = Field(
        False,
        description="Available to all teams",
    )
    is_default: bool = Field(
        False,
        description="Default template for new sprints",
    )

    @field_validator("template_type")
    @classmethod
    def validate_template_type(cls, v: str) -> str:
        if v not in VALID_TEMPLATE_TYPES:
            raise ValueError(f"template_type must be one of: {', '.join(VALID_TEMPLATE_TYPES)}")
        return v


# ============================================================
# Create Schema
# ============================================================


class SprintTemplateCreate(SprintTemplateBase):
    """Schema for creating a new SprintTemplate."""

    team_id: Optional[UUID] = Field(
        None,
        description="Team-specific template (null = org-wide)",
    )
    backlog_structure: Optional[List[BacklogItemTemplate]] = Field(
        None,
        description="Default backlog items",
    )


# ============================================================
# Update Schema
# ============================================================


class SprintTemplateUpdate(BaseModel):
    """Schema for updating an existing SprintTemplate."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    template_type: Optional[str] = None
    duration_days: Optional[int] = Field(None, ge=1, le=30)
    default_capacity_points: Optional[int] = Field(None, ge=0, le=200)
    gates_enabled: Optional[bool] = None
    goal_template: Optional[str] = Field(None, max_length=500)
    is_public: Optional[bool] = None
    is_default: Optional[bool] = None
    backlog_structure: Optional[List[BacklogItemTemplate]] = None

    @field_validator("template_type")
    @classmethod
    def validate_template_type(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_TEMPLATE_TYPES:
            raise ValueError(f"template_type must be one of: {', '.join(VALID_TEMPLATE_TYPES)}")
        return v


# ============================================================
# Response Schemas
# ============================================================


class SprintTemplateResponse(SprintTemplateBase):
    """Response schema for SprintTemplate."""

    id: UUID
    team_id: Optional[UUID] = None
    backlog_structure: Optional[List[dict]] = None
    usage_count: int = 0
    created_by_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class SprintTemplateWithDetails(SprintTemplateResponse):
    """Response schema with additional details."""

    team_name: Optional[str] = None
    created_by_name: Optional[str] = None
    backlog_item_count: int = 0
    total_story_points: int = 0


class SprintTemplateListResponse(BaseModel):
    """Response schema for listing templates."""

    items: List[SprintTemplateResponse]
    total: int
    page: int = 1
    page_size: int = 20


# ============================================================
# Apply Template Schema
# ============================================================


class ApplyTemplateRequest(BaseModel):
    """Schema for applying a template to create a new sprint."""

    project_id: UUID = Field(..., description="Project to create sprint in")
    phase_id: Optional[UUID] = Field(None, description="Phase to assign sprint to")
    start_date: date = Field(..., description="Sprint start date")
    sprint_name: Optional[str] = Field(None, max_length=100, description="Override sprint name")
    goal: Optional[str] = Field(None, max_length=500, description="Override sprint goal")
    team_size: Optional[int] = Field(None, ge=1, le=50, description="Override team size")
    include_backlog: bool = Field(
        True,
        description="Create backlog items from template",
    )


class ApplyTemplateResponse(BaseModel):
    """Response schema after applying a template."""

    sprint_id: UUID
    sprint_number: int
    sprint_name: str
    start_date: date
    end_date: date
    backlog_items_created: int = 0
    template_id: UUID
    template_name: str


# ============================================================
# Template Suggestions
# ============================================================


class TemplateSuggestion(BaseModel):
    """Suggested template based on context."""

    template_id: UUID
    template_name: str
    template_type: str
    match_score: float = Field(..., ge=0, le=1, description="Match score 0-1")
    reason: str


class TemplateSuggestionsResponse(BaseModel):
    """Response with suggested templates."""

    suggestions: List[TemplateSuggestion]
    project_context: dict = Field(default_factory=dict)


# ============================================================
# Bulk Operations
# ============================================================


class SprintTemplateBulkDelete(BaseModel):
    """Schema for bulk deleting templates."""

    ids: List[UUID]


class SprintTemplateBulkResult(BaseModel):
    """Result of bulk operation."""

    success_count: int
    failure_count: int
    errors: List[dict] = []
