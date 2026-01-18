/**
 * =========================================================================
 * usePlanning - React Query Hooks for Planning Hierarchy API
 * SDLC Orchestrator - Sprint 75 (Planning API Validation)
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 75 Day 4
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - Connect Planning components to backend Planning API
 * - Fetch roadmaps, phases, sprints, and backlog items
 * - Mutations for CRUD operations
 * - Sprint gate evaluation (G-Sprint / G-Sprint-Close)
 * - Cache invalidation and optimistic updates
 *
 * SDLC 5.1.3 Rules Implemented:
 * - Rule #1: Sprint numbers immutable
 * - Rule #8: P0/P1/P2 priority classification
 * - SE4H Coach: Admin/owner can approve gates
 *
 * References:
 * - backend/app/api/routes/planning.py
 * - backend/app/services/sprint_gate_service.py
 * - docs/04-build/02-Sprint-Plans/SPRINT-75-PLANNING-API-VALIDATION.md
 * =========================================================================
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/api/client";
import { toast } from "@/hooks/useToast";

// ============================================================================
// Types (aligned with backend schemas)
// ============================================================================

/** Sprint status enum */
export type SprintStatus = "planning" | "in_progress" | "completed" | "closed";

/** Gate status enum */
export type GateStatus = "pending" | "approved" | "rejected";

/** Gate type enum */
export type GateType = "g_sprint" | "g_sprint_close";

/** Backlog item type enum */
export type BacklogItemType = "story" | "task" | "bug" | "spike";

/** Backlog item status enum */
export type BacklogItemStatus =
  | "todo"
  | "in_progress"
  | "review"
  | "done"
  | "blocked";

/** Priority level (SDLC 5.1.3 Rule #8) */
export type Priority = "P0" | "P1" | "P2";

/** Roadmap from API */
export interface Roadmap {
  id: string;
  project_id: string;
  name: string;
  description?: string;
  vision?: string;
  start_date?: string;
  end_date?: string;
  review_cadence: string;
  status: string;
  created_by?: string;
  created_at: string;
  updated_at: string;
}

/** Phase from API */
export interface Phase {
  id: string;
  roadmap_id: string;
  number: number;
  name: string;
  theme?: string;
  objective?: string;
  start_date?: string;
  end_date?: string;
  status: string;
  created_at: string;
  updated_at: string;
}

/** Sprint from API */
export interface Sprint {
  id: string;
  project_id: string;
  phase_id?: string;
  number: number;
  name: string;
  goal?: string;
  status: SprintStatus;
  start_date?: string;
  end_date?: string;
  capacity_points?: number;
  team_size?: number;
  g_sprint_status: GateStatus;
  g_sprint_close_status: GateStatus;
  created_by?: string;
  approved_by?: string;
  approved_at?: string;
  closed_by?: string;
  closed_at?: string;
  created_at: string;
  updated_at: string;
}

/** Sprint with details */
export interface SprintWithDetails extends Sprint {
  phase?: Phase;
  backlog_items_count: number;
  completed_items_count: number;
  total_story_points: number;
  completed_story_points: number;
}

/** Sprint Gate Evaluation from API */
export interface SprintGateEvaluation {
  id: string;
  sprint_id: string;
  gate_type: GateType;
  status: GateStatus;
  checklist: Record<string, boolean>;
  evaluated_by?: string;
  evaluated_at?: string;
  notes?: string;
  created_at: string;
}

/** Backlog Item from API */
export interface BacklogItem {
  id: string;
  sprint_id?: string;
  project_id: string;
  type: BacklogItemType;
  title: string;
  description?: string;
  acceptance_criteria?: string;
  priority: Priority;
  story_points?: number;
  status: BacklogItemStatus;
  assignee_id?: string;
  parent_id?: string;
  labels: string[];
  created_by?: string;
  created_at: string;
  updated_at: string;
}

/** Backlog Item with assignee details */
export interface BacklogItemWithDetails extends BacklogItem {
  assignee?: {
    id: string;
    email: string;
    full_name?: string;
    avatar_url?: string;
  };
  children_count: number;
  completed_children_count: number;
}

/** Sprint statistics */
export interface SprintStatistics {
  sprint_id: string;
  total_items: number;
  completed_items: number;
  in_progress_items: number;
  blocked_items: number;
  total_story_points: number;
  completed_story_points: number;
  completion_rate: number;
  by_priority: {
    P0: { total: number; completed: number };
    P1: { total: number; completed: number };
    P2: { total: number; completed: number };
  };
  by_type: {
    story: number;
    task: number;
    bug: number;
    spike: number;
  };
}

/** Paginated response */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

// ============================================================================
// Query Keys
// ============================================================================

export const planningKeys = {
  all: ["planning"] as const,

  // Roadmaps
  roadmaps: () => [...planningKeys.all, "roadmaps"] as const,
  roadmapsList: (projectId: string) =>
    [...planningKeys.roadmaps(), "list", projectId] as const,
  roadmapDetail: (id: string) =>
    [...planningKeys.roadmaps(), "detail", id] as const,

  // Phases
  phases: () => [...planningKeys.all, "phases"] as const,
  phasesList: (roadmapId: string) =>
    [...planningKeys.phases(), "list", roadmapId] as const,
  phaseDetail: (id: string) => [...planningKeys.phases(), "detail", id] as const,

  // Sprints
  sprints: () => [...planningKeys.all, "sprints"] as const,
  sprintsList: (projectId: string) =>
    [...planningKeys.sprints(), "list", projectId] as const,
  sprintDetail: (id: string) =>
    [...planningKeys.sprints(), "detail", id] as const,
  sprintStatistics: (id: string) =>
    [...planningKeys.sprintDetail(id), "statistics"] as const,
  sprintGates: (id: string) =>
    [...planningKeys.sprintDetail(id), "gates"] as const,

  // Backlog
  backlog: () => [...planningKeys.all, "backlog"] as const,
  backlogList: (filters: { sprintId?: string; projectId?: string }) =>
    [...planningKeys.backlog(), "list", filters] as const,
  backlogDetail: (id: string) =>
    [...planningKeys.backlog(), "detail", id] as const,
};

// ============================================================================
// API Functions - Sprints
// ============================================================================

/** Fetch project sprints list */
async function fetchProjectSprints(
  projectId: string
): Promise<PaginatedResponse<Sprint>> {
  const response = await apiClient.get<PaginatedResponse<Sprint>>(
    `/planning/projects/${projectId}/sprints`
  );
  return response.data;
}

/** Fetch single sprint with details */
async function fetchSprint(sprintId: string): Promise<SprintWithDetails> {
  const response = await apiClient.get<SprintWithDetails>(
    `/planning/sprints/${sprintId}`
  );
  return response.data;
}

/** Fetch sprint statistics */
async function fetchSprintStatistics(
  sprintId: string
): Promise<SprintStatistics> {
  const response = await apiClient.get<SprintStatistics>(
    `/planning/sprints/${sprintId}/statistics`
  );
  return response.data;
}

/** Create sprint */
export interface CreateSprintData {
  project_id: string;
  phase_id?: string;
  number?: number;
  name: string;
  goal?: string;
  start_date?: string;
  end_date?: string;
  capacity_points?: number;
  team_size?: number;
}

async function createSprint(data: CreateSprintData): Promise<Sprint> {
  const response = await apiClient.post<Sprint>("/planning/sprints", data);
  return response.data;
}

/** Update sprint */
export interface UpdateSprintData {
  name?: string;
  goal?: string;
  status?: SprintStatus;
  start_date?: string;
  end_date?: string;
  capacity_points?: number;
  team_size?: number;
}

async function updateSprint(
  sprintId: string,
  data: UpdateSprintData
): Promise<Sprint> {
  const response = await apiClient.put<Sprint>(
    `/planning/sprints/${sprintId}`,
    data
  );
  return response.data;
}

/** Delete sprint */
async function deleteSprint(sprintId: string): Promise<void> {
  await apiClient.delete(`/planning/sprints/${sprintId}`);
}

// ============================================================================
// API Functions - Sprint Gates
// ============================================================================

/** Fetch sprint gates */
async function fetchSprintGates(
  sprintId: string
): Promise<PaginatedResponse<SprintGateEvaluation>> {
  const response = await apiClient.get<PaginatedResponse<SprintGateEvaluation>>(
    `/planning/sprints/${sprintId}/gates`
  );
  return response.data;
}

/** Create gate evaluation */
export interface CreateGateEvaluationData {
  checklist: Record<string, boolean>;
  notes?: string;
}

async function createGateEvaluation(
  sprintId: string,
  gateType: GateType,
  data: CreateGateEvaluationData
): Promise<SprintGateEvaluation> {
  const gateTypeUrl = gateType === "g_sprint" ? "g-sprint" : "g-sprint-close";
  const response = await apiClient.post<SprintGateEvaluation>(
    `/planning/sprints/${sprintId}/gates/${gateTypeUrl}/evaluate`,
    data
  );
  return response.data;
}

/** Submit gate for approval */
async function submitGateApproval(
  gateId: string
): Promise<SprintGateEvaluation> {
  const response = await apiClient.post<SprintGateEvaluation>(
    `/planning/gates/${gateId}/submit`
  );
  return response.data;
}

// ============================================================================
// API Functions - Backlog Items
// ============================================================================

/** Fetch backlog items */
async function fetchBacklogItems(filters: {
  sprintId?: string;
  projectId?: string;
  status?: BacklogItemStatus;
  priority?: Priority;
}): Promise<PaginatedResponse<BacklogItemWithDetails>> {
  const params = new URLSearchParams();
  if (filters.sprintId) params.set("sprint_id", filters.sprintId);
  if (filters.projectId) params.set("project_id", filters.projectId);
  if (filters.status) params.set("status", filters.status);
  if (filters.priority) params.set("priority", filters.priority);

  const response = await apiClient.get<
    PaginatedResponse<BacklogItemWithDetails>
  >(`/planning/backlog?${params}`);
  return response.data;
}

/** Fetch single backlog item */
async function fetchBacklogItem(
  itemId: string
): Promise<BacklogItemWithDetails> {
  const response = await apiClient.get<BacklogItemWithDetails>(
    `/planning/backlog/${itemId}`
  );
  return response.data;
}

/** Create backlog item */
export interface CreateBacklogItemData {
  project_id: string;
  sprint_id?: string;
  type: BacklogItemType;
  title: string;
  description?: string;
  acceptance_criteria?: string;
  priority?: Priority;
  story_points?: number;
  assignee_id?: string;
  parent_id?: string;
  labels?: string[];
}

async function createBacklogItem(
  data: CreateBacklogItemData
): Promise<BacklogItem> {
  const response = await apiClient.post<BacklogItem>("/planning/backlog", data);
  return response.data;
}

/** Update backlog item */
export interface UpdateBacklogItemData {
  title?: string;
  description?: string;
  acceptance_criteria?: string;
  type?: BacklogItemType;
  priority?: Priority;
  story_points?: number;
  status?: BacklogItemStatus;
  assignee_id?: string | null;
  sprint_id?: string | null;
  parent_id?: string | null;
  labels?: string[];
}

async function updateBacklogItem(
  itemId: string,
  data: UpdateBacklogItemData
): Promise<BacklogItem> {
  const response = await apiClient.put<BacklogItem>(
    `/planning/backlog/${itemId}`,
    data
  );
  return response.data;
}

/** Delete backlog item */
async function deleteBacklogItem(itemId: string): Promise<void> {
  await apiClient.delete(`/planning/backlog/${itemId}`);
}

/** Bulk update backlog items */
export interface BulkUpdateBacklogData {
  item_ids: string[];
  status?: BacklogItemStatus;
  priority?: Priority;
  sprint_id?: string | null;
  assignee_id?: string | null;
}

async function bulkUpdateBacklogItems(
  data: BulkUpdateBacklogData
): Promise<{ updated_count: number }> {
  const response = await apiClient.post<{ updated_count: number }>(
    "/planning/backlog/bulk-update",
    data
  );
  return response.data;
}

// ============================================================================
// React Query Hooks - Sprints
// ============================================================================

/**
 * Hook to fetch project sprints list
 */
export function useProjectSprints(projectId: string | null) {
  return useQuery({
    queryKey: planningKeys.sprintsList(projectId || ""),
    queryFn: () => fetchProjectSprints(projectId!),
    enabled: !!projectId,
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 30 * 60 * 1000, // 30 minutes
  });
}

/**
 * Hook to fetch single sprint with details
 */
export function useSprint(sprintId: string | null) {
  return useQuery({
    queryKey: planningKeys.sprintDetail(sprintId || ""),
    queryFn: () => fetchSprint(sprintId!),
    enabled: !!sprintId,
    staleTime: 5 * 60 * 1000,
    gcTime: 30 * 60 * 1000,
  });
}

/**
 * Hook to fetch sprint statistics
 */
export function useSprintStatistics(sprintId: string | null) {
  return useQuery({
    queryKey: planningKeys.sprintStatistics(sprintId || ""),
    queryFn: () => fetchSprintStatistics(sprintId!),
    enabled: !!sprintId,
    staleTime: 2 * 60 * 1000, // 2 minutes (more dynamic)
    gcTime: 10 * 60 * 1000,
  });
}

/**
 * Hook to create sprint
 */
export function useCreateSprint() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createSprint,
    onSuccess: (newSprint) => {
      // Invalidate sprints list
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprintsList(newSprint.project_id),
      });

      toast({
        title: "Sprint created",
        description: `Sprint "${newSprint.name}" has been created successfully.`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to create sprint",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

/**
 * Hook to update sprint
 */
export function useUpdateSprint(sprintId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UpdateSprintData) => updateSprint(sprintId, data),
    onSuccess: (updatedSprint) => {
      // Invalidate sprint detail and lists
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprintDetail(sprintId),
      });
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprintsList(updatedSprint.project_id),
      });

      toast({
        title: "Sprint updated",
        description: `Sprint "${updatedSprint.name}" has been updated successfully.`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to update sprint",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

/**
 * Hook to delete sprint
 */
export function useDeleteSprint() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteSprint,
    onSuccess: () => {
      // Invalidate all sprints lists
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprints(),
      });

      toast({
        title: "Sprint deleted",
        description: "The sprint has been deleted successfully.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to delete sprint",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

// ============================================================================
// React Query Hooks - Sprint Gates
// ============================================================================

/**
 * Hook to fetch sprint gates
 */
export function useSprintGates(sprintId: string | null) {
  return useQuery({
    queryKey: planningKeys.sprintGates(sprintId || ""),
    queryFn: () => fetchSprintGates(sprintId!),
    enabled: !!sprintId,
    staleTime: 2 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
  });
}

/**
 * Hook to create gate evaluation
 */
export function useCreateGateEvaluation(
  sprintId: string,
  gateType: GateType
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateGateEvaluationData) =>
      createGateEvaluation(sprintId, gateType, data),
    onSuccess: () => {
      // Invalidate sprint gates and detail
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprintGates(sprintId),
      });
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprintDetail(sprintId),
      });

      const gateLabel = gateType === "g_sprint" ? "G-Sprint" : "G-Sprint-Close";
      toast({
        title: "Gate evaluation created",
        description: `${gateLabel} evaluation has been created.`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to create gate evaluation",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

/**
 * Hook to submit gate for approval
 * Note: Only team admin/owner can approve (SE4H Coach rule)
 */
export function useSubmitGateApproval(sprintId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: submitGateApproval,
    onSuccess: (result) => {
      // Invalidate sprint gates and detail
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprintGates(sprintId),
      });
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprintDetail(sprintId),
      });

      if (result.status === "approved") {
        toast({
          title: "Gate approved",
          description: "The sprint gate has been approved successfully.",
        });
      }
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to submit gate",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

// ============================================================================
// React Query Hooks - Backlog Items
// ============================================================================

/**
 * Hook to fetch backlog items
 */
export function useBacklogItems(filters: {
  sprintId?: string;
  projectId?: string;
  status?: BacklogItemStatus;
  priority?: Priority;
}) {
  return useQuery({
    queryKey: planningKeys.backlogList(filters),
    queryFn: () => fetchBacklogItems(filters),
    enabled: !!(filters.sprintId || filters.projectId),
    staleTime: 2 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
  });
}

/**
 * Hook to fetch single backlog item
 */
export function useBacklogItem(itemId: string | null) {
  return useQuery({
    queryKey: planningKeys.backlogDetail(itemId || ""),
    queryFn: () => fetchBacklogItem(itemId!),
    enabled: !!itemId,
    staleTime: 2 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
  });
}

/**
 * Hook to create backlog item
 */
export function useCreateBacklogItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createBacklogItem,
    onSuccess: (newItem) => {
      // Invalidate backlog lists
      queryClient.invalidateQueries({
        queryKey: planningKeys.backlog(),
      });

      // Invalidate sprint statistics if assigned to sprint
      if (newItem.sprint_id) {
        queryClient.invalidateQueries({
          queryKey: planningKeys.sprintStatistics(newItem.sprint_id),
        });
      }

      toast({
        title: "Backlog item created",
        description: `"${newItem.title}" has been created.`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to create backlog item",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

/**
 * Hook to update backlog item
 */
export function useUpdateBacklogItem(itemId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UpdateBacklogItemData) => updateBacklogItem(itemId, data),
    onSuccess: (updatedItem) => {
      // Invalidate backlog detail and lists
      queryClient.invalidateQueries({
        queryKey: planningKeys.backlogDetail(itemId),
      });
      queryClient.invalidateQueries({
        queryKey: planningKeys.backlog(),
      });

      // Invalidate sprint statistics
      if (updatedItem.sprint_id) {
        queryClient.invalidateQueries({
          queryKey: planningKeys.sprintStatistics(updatedItem.sprint_id),
        });
      }

      toast({
        title: "Backlog item updated",
        description: `"${updatedItem.title}" has been updated.`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to update backlog item",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

/**
 * Hook to delete backlog item
 */
export function useDeleteBacklogItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteBacklogItem,
    onSuccess: () => {
      // Invalidate backlog lists
      queryClient.invalidateQueries({
        queryKey: planningKeys.backlog(),
      });

      toast({
        title: "Backlog item deleted",
        description: "The item has been deleted successfully.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to delete backlog item",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

/**
 * Hook to bulk update backlog items
 */
export function useBulkUpdateBacklogItems() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: bulkUpdateBacklogItems,
    onSuccess: (result) => {
      // Invalidate backlog lists
      queryClient.invalidateQueries({
        queryKey: planningKeys.backlog(),
      });

      toast({
        title: "Backlog items updated",
        description: `${result.updated_count} items have been updated.`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to update backlog items",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

// ============================================================================
// Helper Hooks
// ============================================================================

/**
 * Hook to get sprint progress percentage
 */
export function useSprintProgress(sprintId: string | null) {
  const { data: stats } = useSprintStatistics(sprintId);

  if (!stats || stats.total_items === 0) {
    return 0;
  }

  return Math.round((stats.completed_items / stats.total_items) * 100);
}

/**
 * Hook to check if sprint is ready for G-Sprint gate
 */
export function useIsSprintReadyForGSprint(sprintId: string | null) {
  const { data: sprint } = useSprint(sprintId);

  if (!sprint) {
    return false;
  }

  return (
    sprint.status === "planning" &&
    sprint.g_sprint_status === "pending" &&
    sprint.goal &&
    sprint.capacity_points &&
    sprint.capacity_points > 0
  );
}

/**
 * Hook to check if sprint is ready for G-Sprint-Close gate
 */
export function useIsSprintReadyForGSprintClose(sprintId: string | null) {
  const { data: sprint } = useSprint(sprintId);
  const { data: stats } = useSprintStatistics(sprintId);

  if (!sprint || !stats) {
    return false;
  }

  // Sprint must be completed and have no blocked items
  return (
    sprint.status === "completed" &&
    sprint.g_sprint_status === "approved" &&
    sprint.g_sprint_close_status === "pending" &&
    stats.blocked_items === 0
  );
}

/**
 * Hook to invalidate planning cache
 */
export function useInvalidatePlanningCache() {
  const queryClient = useQueryClient();

  return {
    invalidateSprint: (sprintId: string) => {
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprintDetail(sprintId),
      });
    },
    invalidateProjectSprints: (projectId: string) => {
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprintsList(projectId),
      });
    },
    invalidateBacklog: () => {
      queryClient.invalidateQueries({
        queryKey: planningKeys.backlog(),
      });
    },
    invalidateAllPlanning: () => {
      queryClient.invalidateQueries({
        queryKey: planningKeys.all,
      });
    },
  };
}
