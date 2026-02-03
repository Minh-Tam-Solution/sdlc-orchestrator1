"""
=========================================================================
Sprint Dependency Schemas
SDLC Orchestrator - Sprint 78 Day 2

Version: 1.0.0
Date: January 18, 2026
Status: ACTIVE - Sprint 78 Implementation
Authority: Backend Lead + CTO Approved
Framework: SDLC 5.1.3 P2 (Sprint Planning Governance)

Purpose:
- Pydantic schemas for SprintDependency CRUD operations
- Validation for dependency types and statuses
- Response schemas for dependency graph visualization

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

VALID_DEPENDENCY_TYPES = ["blocks", "requires", "related"]
VALID_DEPENDENCY_STATUSES = ["pending", "active", "resolved", "cancelled"]


# ============================================================
# Base Schema
# ============================================================


class SprintDependencyBase(BaseModel):
    """Base schema for SprintDependency with shared fields."""

    dependency_type: str = Field(
        "related",
        description="Type: blocks, requires, related",
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Description of the dependency",
    )

    @field_validator("dependency_type")
    @classmethod
    def validate_dependency_type(cls, v: str) -> str:
        if v not in VALID_DEPENDENCY_TYPES:
            raise ValueError(f"dependency_type must be one of: {', '.join(VALID_DEPENDENCY_TYPES)}")
        return v


# ============================================================
# Create Schema
# ============================================================


class SprintDependencyCreate(SprintDependencyBase):
    """Schema for creating a new SprintDependency."""

    source_sprint_id: UUID = Field(..., description="Sprint that depends on another")
    target_sprint_id: UUID = Field(..., description="Sprint being depended on")

    @field_validator("target_sprint_id")
    @classmethod
    def validate_not_self_reference(cls, v: UUID, info) -> UUID:
        source_id = info.data.get("source_sprint_id")
        if source_id and v == source_id:
            raise ValueError("A sprint cannot depend on itself")
        return v


# ============================================================
# Update Schema
# ============================================================


class SprintDependencyUpdate(BaseModel):
    """Schema for updating an existing SprintDependency."""

    dependency_type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

    @field_validator("dependency_type")
    @classmethod
    def validate_dependency_type(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_DEPENDENCY_TYPES:
            raise ValueError(f"dependency_type must be one of: {', '.join(VALID_DEPENDENCY_TYPES)}")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_DEPENDENCY_STATUSES:
            raise ValueError(f"status must be one of: {', '.join(VALID_DEPENDENCY_STATUSES)}")
        return v


# ============================================================
# Response Schemas
# ============================================================


class SprintDependencyResponse(SprintDependencyBase):
    """Response schema for SprintDependency."""

    id: UUID
    source_sprint_id: UUID
    target_sprint_id: UUID
    status: str
    created_by_id: Optional[UUID] = None
    resolved_by_id: Optional[UUID] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class SprintDependencyWithDetails(SprintDependencyResponse):
    """Response schema with related sprint details."""

    source_sprint_number: Optional[int] = None
    source_sprint_name: Optional[str] = None
    source_project_id: Optional[UUID] = None
    source_project_name: Optional[str] = None

    target_sprint_number: Optional[int] = None
    target_sprint_name: Optional[str] = None
    target_project_id: Optional[UUID] = None
    target_project_name: Optional[str] = None

    is_cross_project: bool = False


class SprintDependencyListResponse(BaseModel):
    """Response schema for listing dependencies."""

    items: List[SprintDependencyResponse]
    total: int
    page: int = 1
    page_size: int = 20


# ============================================================
# Graph Visualization Schemas
# ============================================================


class DependencyGraphNode(BaseModel):
    """Node in dependency graph (represents a sprint)."""

    id: str = Field(..., description="Sprint UUID as string")
    label: str = Field(..., description="Display label (e.g., 'Sprint 74')")
    sprint_number: int
    sprint_name: str
    status: str
    project_id: str
    project_name: Optional[str] = None

    # Visual metadata
    has_blocking_dependency: bool = False
    is_blocked: bool = False


class DependencyGraphEdge(BaseModel):
    """Edge in dependency graph (represents a dependency)."""

    id: str = Field(..., description="Dependency UUID as string")
    source: str = Field(..., description="Source sprint UUID")
    target: str = Field(..., description="Target sprint UUID")
    dependency_type: str
    status: str
    description: Optional[str] = None

    # Visual metadata
    is_blocking: bool = False
    is_cross_project: bool = False


class DependencyGraph(BaseModel):
    """Complete dependency graph for visualization."""

    nodes: List[DependencyGraphNode]
    edges: List[DependencyGraphEdge]
    total_sprints: int = 0
    total_dependencies: int = 0
    blocking_dependencies: int = 0
    cross_project_dependencies: int = 0


# ============================================================
# Analysis Schemas
# ============================================================


class CircularDependencyError(BaseModel):
    """Error response for circular dependency detection."""

    message: str = "Circular dependency detected"
    cycle_path: List[str] = Field(..., description="UUIDs forming the cycle")
    cycle_description: str = Field(..., description="Human-readable cycle path")


class CriticalPathItem(BaseModel):
    """Item in critical path analysis."""

    sprint_id: UUID
    sprint_number: int
    sprint_name: str
    project_name: str
    dependencies_count: int
    blocking_count: int
    depth: int = Field(..., description="Depth in dependency chain")


class DependencyAnalysis(BaseModel):
    """Analysis of dependency structure."""

    total_dependencies: int = 0
    blocking_dependencies: int = 0
    cross_project_dependencies: int = 0
    pending_dependencies: int = 0
    resolved_dependencies: int = 0

    # Critical path analysis
    critical_path: List[CriticalPathItem] = []
    max_depth: int = 0

    # Risk indicators
    has_circular_risk: bool = False
    high_dependency_sprints: List[str] = Field(
        default_factory=list,
        description="Sprint IDs with >3 dependencies",
    )


# ============================================================
# Bulk Operations
# ============================================================


class SprintDependencyBulkResolve(BaseModel):
    """Schema for bulk resolving dependencies."""

    ids: List[UUID]


class SprintDependencyBulkResult(BaseModel):
    """Result of bulk operation."""

    success_count: int
    failure_count: int
    errors: List[dict] = []
