/**
 * Planning Hierarchy Types - SDLC Orchestrator
 *
 * @module frontend/src/lib/types/planning
 * @description TypeScript interfaces for Planning Hierarchy (Roadmap → Phase → Sprint → Backlog)
 * @sdlc SDLC 5.1.3 Framework - Sprint 87 (Sprint Governance UI)
 * @status Sprint 87 - Core Feature Implementation
 */

// =============================================================================
// STATUS ENUMS
// =============================================================================

/**
 * Sprint status - lifecycle states
 */
export type SprintStatus =
  | "planned"     // Not started, waiting for G-Sprint gate
  | "active"      // Currently running
  | "closing"     // In close phase (24h documentation window)
  | "closed"      // Successfully completed
  | "cancelled";  // Cancelled before completion

/**
 * Phase status - aggregate of sprints
 */
export type PhaseStatus =
  | "planned"     // No sprints started
  | "active"      // At least one sprint active
  | "completed";  // All sprints completed

/**
 * Gate status - evaluation result
 */
export type GateStatus =
  | "pending"      // Not evaluated yet
  | "evaluating"   // Currently evaluating
  | "passed"       // All mandatory items pass
  | "conditional"  // Pass with waiver for some items
  | "failed";      // Mandatory items failed

/**
 * Backlog item type
 */
export type BacklogItemType =
  | "story"   // User story
  | "task"    // Technical task
  | "bug"     // Bug fix
  | "spike";  // Research/investigation

/**
 * Backlog item priority
 */
export type BacklogItemPriority =
  | "p0"  // Critical - must complete this sprint
  | "p1"  // High - should complete this sprint
  | "p2"  // Medium - nice to have
  | "p3"; // Low - can defer

/**
 * Backlog item status
 */
export type BacklogItemStatus =
  | "todo"          // Not started
  | "in_progress"   // Being worked on
  | "review"        // In code review
  | "done"          // Completed
  | "carried_over"; // Moved to next sprint

// =============================================================================
// ROADMAP TYPES
// =============================================================================

/**
 * Roadmap - 12-month vision with quarterly milestones
 */
export interface Roadmap {
  id: string;
  name: string;
  description: string | null;
  project_id: string;
  start_date: string;
  end_date: string;
  phases_count: number;
  total_sprints: number;
  completed_sprints: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Roadmap creation/update request
 */
export interface RoadmapInput {
  name: string;
  description?: string;
  project_id: string;
  start_date: string;
  end_date: string;
}

/**
 * Roadmap list response
 */
export interface RoadmapsListResponse {
  roadmaps: Roadmap[];
  total: number;
  page: number;
  page_size: number;
}

// =============================================================================
// PHASE TYPES
// =============================================================================

/**
 * Phase - 4-8 week theme-based grouping of sprints
 */
export interface Phase {
  id: string;
  name: string;
  description: string | null;
  roadmap_id: string;
  start_date: string;
  end_date: string;
  status: PhaseStatus;
  theme: string | null;
  sprints_count: number;
  sprints_completed: number;
  order: number;
  created_at: string;
  updated_at: string;
}

/**
 * Phase creation/update request
 */
export interface PhaseInput {
  name: string;
  description?: string;
  roadmap_id: string;
  start_date: string;
  end_date: string;
  theme?: string;
  order?: number;
}

/**
 * Phases list response
 */
export interface PhasesListResponse {
  phases: Phase[];
  total: number;
}

// =============================================================================
// SPRINT TYPES
// =============================================================================

/**
 * Sprint - 5-10 day committed work cycle (SDLC 5.1.3 Pillar 2)
 */
export interface Sprint {
  id: string;
  name: string;
  number: number;
  goal: string;
  project_id: string;
  phase_id: string | null;
  start_date: string;
  end_date: string;
  status: SprintStatus;
  // Story points metrics
  story_points_planned: number;
  story_points_completed: number;
  story_points_carried_over: number;
  // Item counts
  items_total: number;
  items_completed: number;
  items_in_progress: number;
  items_carried_over: number;
  // Gate statuses (SDLC 5.1.3 Pillar 2)
  g_sprint_status: GateStatus;
  g_sprint_close_status: GateStatus;
  g_sprint_evaluated_at: string | null;
  g_sprint_close_evaluated_at: string | null;
  // 24h documentation deadline
  documentation_deadline: string | null;
  documentation_submitted: boolean;
  // Metadata
  team_capacity: number | null;
  velocity: number | null;
  risks_identified: number;
  dependencies_count: number;
  retrospective_url: string | null;
  created_at: string;
  updated_at: string;
  closed_at: string | null;
}

/**
 * Sprint creation request
 */
export interface SprintInput {
  name: string;
  number: number;
  goal: string;
  project_id: string;
  phase_id?: string;
  start_date: string;
  end_date: string;
  team_capacity?: number;
}

/**
 * Sprint update request
 */
export interface SprintUpdateInput {
  name?: string;
  goal?: string;
  start_date?: string;
  end_date?: string;
  status?: SprintStatus;
  team_capacity?: number;
  retrospective_url?: string;
}

/**
 * Sprints list response
 */
export interface SprintsListResponse {
  sprints: Sprint[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * Sprint with nested backlog items
 */
export interface SprintWithItems extends Sprint {
  items: BacklogItem[];
}

// =============================================================================
// BACKLOG ITEM TYPES
// =============================================================================

/**
 * Backlog item - individual task with hour estimates
 */
export interface BacklogItem {
  id: string;
  title: string;
  description: string | null;
  sprint_id: string | null;
  project_id: string;
  type: BacklogItemType;
  priority: BacklogItemPriority;
  status: BacklogItemStatus;
  story_points: number | null;
  estimated_hours: number | null;
  actual_hours: number | null;
  assignee_id: string | null;
  assignee_name: string | null;
  labels: string[];
  acceptance_criteria: string | null;
  carry_over_reason: string | null;
  order: number;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

/**
 * Backlog item creation request
 */
export interface BacklogItemInput {
  title: string;
  description?: string;
  sprint_id?: string;
  project_id: string;
  type: BacklogItemType;
  priority: BacklogItemPriority;
  story_points?: number;
  estimated_hours?: number;
  assignee_id?: string;
  labels?: string[];
  acceptance_criteria?: string;
}

/**
 * Backlog item update request
 */
export interface BacklogItemUpdateInput {
  title?: string;
  description?: string;
  sprint_id?: string | null;
  type?: BacklogItemType;
  priority?: BacklogItemPriority;
  status?: BacklogItemStatus;
  story_points?: number;
  estimated_hours?: number;
  actual_hours?: number;
  assignee_id?: string | null;
  labels?: string[];
  acceptance_criteria?: string;
  carry_over_reason?: string;
}

/**
 * Backlog items list response
 */
export interface BacklogItemsListResponse {
  items: BacklogItem[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * Bulk move items request (for drag-and-drop)
 */
export interface BulkMoveItemsInput {
  item_ids: string[];
  target_sprint_id: string | null;
  target_status?: BacklogItemStatus;
}

// =============================================================================
// PLANNING HIERARCHY VIEW TYPES
// =============================================================================

/**
 * Full planning hierarchy tree node
 */
export interface PlanningHierarchyNode {
  type: "roadmap" | "phase" | "sprint" | "backlog";
  id: string;
  name: string;
  status?: string;
  start_date?: string;
  end_date?: string;
  children?: PlanningHierarchyNode[];
  metadata?: Record<string, unknown>;
}

/**
 * Planning hierarchy response
 */
export interface PlanningHierarchyResponse {
  project_id: string;
  project_name: string;
  hierarchy: PlanningHierarchyNode[];
  active_sprint_id: string | null;
  total_roadmaps: number;
  total_phases: number;
  total_sprints: number;
  total_items: number;
}

/**
 * Sprint summary for dashboard
 */
export interface SprintSummary {
  id: string;
  name: string;
  number: number;
  status: SprintStatus;
  progress_percentage: number;
  days_remaining: number;
  items_completed: number;
  items_total: number;
  g_sprint_status: GateStatus;
  g_sprint_close_status: GateStatus;
}

/**
 * Active sprint dashboard data
 */
export interface ActiveSprintDashboard {
  sprint: Sprint;
  items_by_status: {
    todo: number;
    in_progress: number;
    review: number;
    done: number;
    carried_over: number;
  };
  burndown_data: {
    date: string;
    ideal: number;
    actual: number;
  }[];
  velocity_trend: {
    sprint_name: string;
    planned: number;
    completed: number;
  }[];
  team_workload: {
    assignee_name: string;
    assigned_points: number;
    completed_points: number;
  }[];
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Get status badge color for sprint status
 */
export function getSprintStatusColor(status: SprintStatus): string {
  const colors: Record<SprintStatus, string> = {
    planned: "bg-gray-100 text-gray-800",
    active: "bg-blue-100 text-blue-800",
    closing: "bg-yellow-100 text-yellow-800",
    closed: "bg-green-100 text-green-800",
    cancelled: "bg-red-100 text-red-800",
  };
  return colors[status] || "bg-gray-100 text-gray-800";
}

/**
 * Get status badge color for gate status
 */
export function getGateStatusColor(status: GateStatus): string {
  const colors: Record<GateStatus, string> = {
    pending: "bg-gray-100 text-gray-800",
    evaluating: "bg-blue-100 text-blue-800",
    passed: "bg-green-100 text-green-800",
    conditional: "bg-yellow-100 text-yellow-800",
    failed: "bg-red-100 text-red-800",
  };
  return colors[status] || "bg-gray-100 text-gray-800";
}

/**
 * Get status icon for gate status
 */
export function getGateStatusIcon(status: GateStatus): string {
  const icons: Record<GateStatus, string> = {
    pending: "⏳",
    evaluating: "🔄",
    passed: "✅",
    conditional: "⚠️",
    failed: "❌",
  };
  return icons[status] || "⏳";
}

/**
 * Get priority color for backlog items
 */
export function getPriorityColor(priority: BacklogItemPriority): string {
  const colors: Record<BacklogItemPriority, string> = {
    p0: "bg-red-100 text-red-800 border-red-200",
    p1: "bg-orange-100 text-orange-800 border-orange-200",
    p2: "bg-blue-100 text-blue-800 border-blue-200",
    p3: "bg-gray-100 text-gray-800 border-gray-200",
  };
  return colors[priority] || "bg-gray-100 text-gray-800";
}

/**
 * Get type icon for backlog items
 */
export function getBacklogItemTypeIcon(type: BacklogItemType): string {
  const icons: Record<BacklogItemType, string> = {
    story: "📖",
    task: "✅",
    bug: "🐛",
    spike: "🔬",
  };
  return icons[type] || "📋";
}

/**
 * Calculate sprint progress percentage
 */
export function calculateSprintProgress(sprint: Sprint): number {
  if (sprint.items_total === 0) return 0;
  return Math.round((sprint.items_completed / sprint.items_total) * 100);
}

/**
 * Calculate days remaining in sprint
 */
export function calculateDaysRemaining(endDate: string): number {
  const end = new Date(endDate);
  const now = new Date();
  const diffTime = end.getTime() - now.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return Math.max(0, diffDays);
}

/**
 * Format sprint date range
 */
export function formatSprintDateRange(startDate: string, endDate: string): string {
  const start = new Date(startDate);
  const end = new Date(endDate);
  const options: Intl.DateTimeFormatOptions = { month: "short", day: "numeric" };

  if (start.getFullYear() !== end.getFullYear()) {
    return `${start.toLocaleDateString("en-US", { ...options, year: "numeric" })} - ${end.toLocaleDateString("en-US", { ...options, year: "numeric" })}`;
  }

  return `${start.toLocaleDateString("en-US", options)} - ${end.toLocaleDateString("en-US", options)}, ${start.getFullYear()}`;
}

/**
 * Check if sprint is overdue (past end date but not closed)
 */
export function isSprintOverdue(sprint: Sprint): boolean {
  if (sprint.status === "closed" || sprint.status === "cancelled") {
    return false;
  }
  const endDate = new Date(sprint.end_date);
  return new Date() > endDate;
}

/**
 * Get documentation deadline status
 */
export function getDocumentationDeadlineStatus(
  deadline: string | null,
  submitted: boolean
): { status: "safe" | "warning" | "critical" | "expired" | "submitted"; hoursRemaining: number } {
  if (submitted) {
    return { status: "submitted", hoursRemaining: 0 };
  }

  if (!deadline) {
    return { status: "safe", hoursRemaining: 24 };
  }

  const deadlineDate = new Date(deadline);
  const now = new Date();
  const hoursRemaining = Math.max(0, (deadlineDate.getTime() - now.getTime()) / (1000 * 60 * 60));

  if (hoursRemaining <= 0) {
    return { status: "expired", hoursRemaining: 0 };
  }
  if (hoursRemaining <= 2) {
    return { status: "critical", hoursRemaining };
  }
  if (hoursRemaining <= 8) {
    return { status: "warning", hoursRemaining };
  }
  return { status: "safe", hoursRemaining };
}
