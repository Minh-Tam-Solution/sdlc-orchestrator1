/**
 * Sprint Governance Types - SDLC Orchestrator
 *
 * @module frontend/src/lib/types/sprint-governance
 * @description TypeScript interfaces for Sprint Governance (G-Sprint & G-Sprint-Close Gates)
 * @sdlc SDLC 5.1.3 Framework - Sprint 87 (Sprint Governance UI)
 * @reference SDLC 5.1.3 Pillar 2: Sprint Planning Governance
 * @status Sprint 87 - Core Feature Implementation
 */

import type { GateStatus } from "./planning";

// =============================================================================
// GATE TYPES
// =============================================================================

/**
 * Gate type - sprint lifecycle gates (SDLC 5.1.3 Pillar 2)
 */
export type SprintGateType = "start" | "close";

/**
 * Checklist item status
 */
export type ChecklistItemStatus =
  | "pending"   // Not evaluated
  | "pass"      // Item satisfied
  | "fail"      // Item not satisfied
  | "waived";   // Waived by approver

// =============================================================================
// SPRINT GATE TYPES
// =============================================================================

/**
 * Sprint Gate - G-Sprint (start) or G-Sprint-Close (close)
 */
export interface SprintGate {
  id: string;
  sprint_id: string;
  gate_type: SprintGateType;
  status: GateStatus;
  checklist_items: ChecklistItem[];
  items_total: number;
  items_passed: number;
  items_failed: number;
  items_waived: number;
  evaluated_at: string | null;
  evaluated_by: string | null;
  approved_at: string | null;
  approved_by: string | null;
  approved_by_name: string | null;
  waiver_reason: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * Gate checklist item
 */
export interface ChecklistItem {
  id: string;
  gate_id: string;
  name: string;
  description: string;
  category: string;
  is_mandatory: boolean;
  status: ChecklistItemStatus;
  evidence_url: string | null;
  evidence_type: string | null;
  notes: string | null;
  evaluated_at: string | null;
  evaluated_by: string | null;
  waiver_reason: string | null;
  order: number;
}

/**
 * Gate evaluation request
 */
export interface GateEvaluationRequest {
  force_evaluation?: boolean;
  include_optional?: boolean;
}

/**
 * Gate evaluation response
 */
export interface GateEvaluationResponse {
  gate: SprintGate;
  evaluation_summary: {
    total_items: number;
    passed_items: number;
    failed_items: number;
    mandatory_passed: number;
    mandatory_failed: number;
    can_approve: boolean;
    requires_waiver: boolean;
  };
  recommendations: string[];
}

/**
 * Sprint gate approval request (distinct from feature gate approval)
 */
export interface SprintGateApprovalRequest {
  waiver_reason?: string;
  notes?: string;
  waived_items?: string[]; // Item IDs to waive
}

/**
 * Update checklist item request
 */
export interface UpdateChecklistItemRequest {
  status?: ChecklistItemStatus;
  evidence_url?: string;
  notes?: string;
  waiver_reason?: string;
}

// =============================================================================
// G-SPRINT GATE (Sprint Start) - SDLC 5.1.3
// =============================================================================

/**
 * G-Sprint gate checklist categories
 */
export const G_SPRINT_CATEGORIES = [
  "goal",         // Sprint goal defined
  "backlog",      // Backlog items estimated
  "capacity",     // Team capacity confirmed
  "dependencies", // Dependencies identified
  "risks",        // Risks documented
  "prerequisite", // Previous sprint closed
] as const;

export type GSprintCategory = typeof G_SPRINT_CATEGORIES[number];

/**
 * G-Sprint gate standard checklist items (SDLC 5.1.3 spec)
 */
export const G_SPRINT_CHECKLIST_TEMPLATE: Omit<ChecklistItem, "id" | "gate_id" | "status" | "evaluated_at" | "evaluated_by" | "waiver_reason">[] = [
  {
    name: "Sprint Goal Defined",
    description: "A clear, measurable sprint goal has been defined that aligns with phase objectives.",
    category: "goal",
    is_mandatory: true,
    evidence_url: null,
    evidence_type: "text",
    notes: null,
    order: 1,
  },
  {
    name: "Backlog Items Estimated",
    description: "All sprint backlog items have story point estimates and acceptance criteria.",
    category: "backlog",
    is_mandatory: true,
    evidence_url: null,
    evidence_type: "count",
    notes: null,
    order: 2,
  },
  {
    name: "Team Capacity Confirmed",
    description: "Team capacity has been calculated considering holidays, meetings, and other commitments.",
    category: "capacity",
    is_mandatory: true,
    evidence_url: null,
    evidence_type: "number",
    notes: null,
    order: 3,
  },
  {
    name: "Dependencies Identified",
    description: "External dependencies have been identified and mitigation plans are in place.",
    category: "dependencies",
    is_mandatory: true,
    evidence_url: null,
    evidence_type: "list",
    notes: null,
    order: 4,
  },
  {
    name: "Risks Documented",
    description: "Sprint risks have been identified with severity and mitigation strategies.",
    category: "risks",
    is_mandatory: true,
    evidence_url: null,
    evidence_type: "list",
    notes: null,
    order: 5,
  },
  {
    name: "Previous Sprint Closed",
    description: "The previous sprint has been properly closed with all documentation completed.",
    category: "prerequisite",
    is_mandatory: false,
    evidence_url: null,
    evidence_type: "link",
    notes: "Only required if there was a previous sprint",
    order: 6,
  },
];

// =============================================================================
// G-SPRINT-CLOSE GATE (Sprint End) - SDLC 5.1.3
// =============================================================================

/**
 * G-Sprint-Close gate checklist categories
 */
export const G_SPRINT_CLOSE_CATEGORIES = [
  "completion",     // Items completed or justified
  "retrospective",  // Retrospective documented
  "evidence",       // Evidence manifests created
  "dod",            // Definition of Done verified
  "next_sprint",    // Next sprint prepared
] as const;

export type GSprintCloseCategory = typeof G_SPRINT_CLOSE_CATEGORIES[number];

/**
 * G-Sprint-Close gate standard checklist items (SDLC 5.1.3 spec)
 */
export const G_SPRINT_CLOSE_CHECKLIST_TEMPLATE: Omit<ChecklistItem, "id" | "gate_id" | "status" | "evaluated_at" | "evaluated_by" | "waiver_reason">[] = [
  {
    name: "All Items Completed or Justified",
    description: "All backlog items are either completed or have carry-over justification documented.",
    category: "completion",
    is_mandatory: true,
    evidence_url: null,
    evidence_type: "summary",
    notes: null,
    order: 1,
  },
  {
    name: "Sprint Retrospective Documented",
    description: "A sprint retrospective has been conducted and documented with action items.",
    category: "retrospective",
    is_mandatory: true,
    evidence_url: null,
    evidence_type: "document",
    notes: null,
    order: 2,
  },
  {
    name: "Evidence Manifests Created",
    description: "Evidence manifests have been created for all deliverables (code review, tests, deployment).",
    category: "evidence",
    is_mandatory: true,
    evidence_url: null,
    evidence_type: "list",
    notes: null,
    order: 3,
  },
  {
    name: "Definition of Done Verified",
    description: "All completed items meet the Definition of Done criteria.",
    category: "dod",
    is_mandatory: true,
    evidence_url: null,
    evidence_type: "checklist",
    notes: null,
    order: 4,
  },
  {
    name: "Next Sprint Prepared",
    description: "The next sprint has been prepared with initial backlog and G-Sprint gate items ready.",
    category: "next_sprint",
    is_mandatory: false,
    evidence_url: null,
    evidence_type: "link",
    notes: "Optional if this is the last sprint in the phase",
    order: 5,
  },
];

// =============================================================================
// DOCUMENTATION DEADLINE TYPES (24h Rule)
// =============================================================================

/**
 * Documentation deadline status
 */
export interface DocumentationDeadline {
  sprint_id: string;
  sprint_name: string;
  deadline: string;
  hours_remaining: number;
  is_expired: boolean;
  documents_required: DocumentRequirement[];
  documents_submitted: DocumentSubmission[];
  completion_percentage: number;
}

/**
 * Document requirement
 */
export interface DocumentRequirement {
  type: "retrospective" | "evidence_manifest" | "carry_over_justification" | "close_report";
  name: string;
  is_mandatory: boolean;
  submitted: boolean;
}

/**
 * Document submission
 */
export interface DocumentSubmission {
  type: string;
  name: string;
  url: string;
  submitted_at: string;
  submitted_by: string;
}

// =============================================================================
// SPRINT METRICS TYPES
// =============================================================================

/**
 * Sprint metrics for governance
 */
export interface SprintGovernanceMetrics {
  sprint_id: string;
  // Velocity metrics
  velocity: number;
  velocity_trend: number; // percentage change from last 3 sprints
  avg_velocity_3_sprints: number;
  // Completion metrics
  completion_rate: number;
  carry_over_rate: number;
  // Cycle time metrics
  avg_cycle_time_hours: number;
  avg_lead_time_hours: number;
  // Quality metrics
  bugs_found_in_sprint: number;
  bugs_fixed_in_sprint: number;
  // Gate metrics
  g_sprint_pass_rate: number;
  g_sprint_close_pass_rate: number;
  avg_gate_evaluation_time_hours: number;
}

/**
 * Sprint comparison data
 */
export interface SprintComparison {
  sprints: {
    id: string;
    name: string;
    number: number;
    planned_points: number;
    completed_points: number;
    completion_rate: number;
    carry_over_count: number;
    duration_days: number;
    team_size: number;
    g_sprint_status: GateStatus;
    g_sprint_close_status: GateStatus;
  }[];
  averages: {
    planned_points: number;
    completed_points: number;
    completion_rate: number;
    carry_over_count: number;
  };
}

// =============================================================================
// GOVERNANCE DASHBOARD TYPES
// =============================================================================

/**
 * Sprint governance dashboard data
 */
export interface SprintGovernanceDashboard {
  active_sprint: {
    id: string;
    name: string;
    number: number;
    goal: string;
    status: string;
    progress_percentage: number;
    days_remaining: number;
    days_total: number;
    g_sprint_status: GateStatus;
    g_sprint_close_status: GateStatus;
    items_by_status: {
      planned: number;
      in_progress: number;
      review: number;
      completed: number;
      carried_over: number;
    };
    story_points: {
      planned: number;
      completed: number;
      remaining: number;
    };
  } | null;
  upcoming_sprints: {
    id: string;
    name: string;
    number: number;
    start_date: string;
    end_date: string;
    status: string;
    g_sprint_status: GateStatus;
    story_points_planned: number;
  }[];
  recent_sprints: {
    id: string;
    name: string;
    number: number;
    closed_at: string;
    completion_rate: number;
    items_completed: number;
    items_total: number;
    g_sprint_close_status: GateStatus;
  }[];
  metrics: {
    avg_velocity: number;
    avg_completion_rate: number;
    total_sprints_completed: number;
    gates_passed: number;
    gates_failed: number;
  };
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Get gate type display name
 */
export function getGateTypeDisplayName(gateType: SprintGateType): string {
  return gateType === "start" ? "G-Sprint" : "G-Sprint-Close";
}

/**
 * Get checklist item status color
 */
export function getChecklistItemStatusColor(status: ChecklistItemStatus): string {
  const colors: Record<ChecklistItemStatus, string> = {
    pending: "bg-gray-100 text-gray-800",
    pass: "bg-green-100 text-green-800",
    fail: "bg-red-100 text-red-800",
    waived: "bg-yellow-100 text-yellow-800",
  };
  return colors[status] || "bg-gray-100 text-gray-800";
}

/**
 * Get checklist item status icon
 */
export function getChecklistItemStatusIcon(status: ChecklistItemStatus): string {
  const icons: Record<ChecklistItemStatus, string> = {
    pending: "⏳",
    pass: "✅",
    fail: "❌",
    waived: "⚠️",
  };
  return icons[status] || "⏳";
}

/**
 * Check if gate can be approved
 */
export function canApproveGate(gate: SprintGate): boolean {
  const mandatoryFailed = gate.checklist_items.filter(
    (item) => item.is_mandatory && item.status === "fail"
  );
  return mandatoryFailed.length === 0;
}

/**
 * Get gate approval status message
 */
export function getGateApprovalMessage(gate: SprintGate): string {
  const mandatoryFailed = gate.checklist_items.filter(
    (item) => item.is_mandatory && item.status === "fail"
  );
  const optionalFailed = gate.checklist_items.filter(
    (item) => !item.is_mandatory && item.status === "fail"
  );

  if (mandatoryFailed.length > 0) {
    return `${mandatoryFailed.length} mandatory item(s) failed. Gate cannot be approved.`;
  }

  if (optionalFailed.length > 0) {
    return `Gate can be approved. ${optionalFailed.length} optional item(s) pending/failed.`;
  }

  return "All items passed. Gate can be approved.";
}

/**
 * Calculate gate progress percentage
 */
export function calculateGateProgress(gate: SprintGate): number {
  if (gate.items_total === 0) return 0;
  return Math.round(((gate.items_passed + gate.items_waived) / gate.items_total) * 100);
}

/**
 * Format documentation deadline countdown
 */
export function formatDeadlineCountdown(hoursRemaining: number): string {
  if (hoursRemaining <= 0) {
    return "EXPIRED";
  }

  const hours = Math.floor(hoursRemaining);
  const minutes = Math.floor((hoursRemaining - hours) * 60);
  const seconds = Math.floor(((hoursRemaining - hours) * 60 - minutes) * 60);

  return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
}

/**
 * Get deadline urgency level
 */
export function getDeadlineUrgencyLevel(
  hoursRemaining: number
): "safe" | "warning" | "critical" | "expired" {
  if (hoursRemaining <= 0) return "expired";
  if (hoursRemaining <= 2) return "critical";
  if (hoursRemaining <= 8) return "warning";
  return "safe";
}

/**
 * Get deadline urgency color
 */
export function getDeadlineUrgencyColor(hoursRemaining: number): string {
  const level = getDeadlineUrgencyLevel(hoursRemaining);
  const colors: Record<string, string> = {
    safe: "text-green-600 bg-green-50",
    warning: "text-yellow-600 bg-yellow-50",
    critical: "text-red-600 bg-red-50 animate-pulse",
    expired: "text-red-800 bg-red-100",
  };
  return colors[level];
}

/**
 * Get category display name
 */
export function getCategoryDisplayName(category: string): string {
  const names: Record<string, string> = {
    // G-Sprint categories
    goal: "Sprint Goal",
    backlog: "Backlog",
    capacity: "Team Capacity",
    dependencies: "Dependencies",
    risks: "Risks",
    prerequisite: "Prerequisites",
    // G-Sprint-Close categories
    completion: "Completion",
    retrospective: "Retrospective",
    evidence: "Evidence",
    dod: "Definition of Done",
    next_sprint: "Next Sprint",
  };
  return names[category] || category;
}
