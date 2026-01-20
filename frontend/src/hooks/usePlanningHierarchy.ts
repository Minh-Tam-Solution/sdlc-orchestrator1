/**
 * Planning Hierarchy Hooks - SDLC Orchestrator
 *
 * @module frontend/src/hooks/usePlanningHierarchy
 * @description TanStack Query hooks for Planning Hierarchy (Roadmap → Phase → Sprint → Backlog)
 * @sdlc SDLC 5.1.3 Framework - Sprint 87 (Sprint Governance UI)
 * @status Sprint 87 - Core Feature Implementation
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getRoadmaps,
  getRoadmap,
  createRoadmap,
  updateRoadmap,
  deleteRoadmap,
  getPhases,
  getPhase,
  createPhase,
  updatePhase,
  deletePhase,
  getSprints,
  getSprint,
  getActiveSprint,
  createSprint,
  updateSprint,
  deleteSprint,
  getBacklogItems,
  getBacklogItem,
  createBacklogItem,
  updateBacklogItem,
  deleteBacklogItem,
  bulkMoveBacklogItems,
  getPlanningHierarchy,
  getActiveSprintDashboard,
} from "@/lib/api";
import type {
  RoadmapInput,
  PhaseInput,
  SprintInput,
  SprintUpdateInput,
  BacklogItemInput,
  BacklogItemUpdateInput,
  BulkMoveItemsInput,
} from "@/lib/types/planning";

// =============================================================================
// QUERY KEYS
// =============================================================================

export const planningKeys = {
  all: ["planning"] as const,
  // Roadmaps
  roadmaps: () => [...planningKeys.all, "roadmaps"] as const,
  roadmapsList: (projectId: string) => [...planningKeys.roadmaps(), "list", projectId] as const,
  roadmapDetail: (id: string) => [...planningKeys.roadmaps(), "detail", id] as const,
  // Phases
  phases: () => [...planningKeys.all, "phases"] as const,
  phasesList: (roadmapId: string) => [...planningKeys.phases(), "list", roadmapId] as const,
  phaseDetail: (id: string) => [...planningKeys.phases(), "detail", id] as const,
  // Sprints
  sprints: () => [...planningKeys.all, "sprints"] as const,
  sprintsList: (params: { projectId?: string; phaseId?: string }) =>
    [...planningKeys.sprints(), "list", params] as const,
  sprintDetail: (id: string) => [...planningKeys.sprints(), "detail", id] as const,
  activeSprint: (projectId: string) => [...planningKeys.sprints(), "active", projectId] as const,
  // Backlog Items
  backlogItems: () => [...planningKeys.all, "backlog"] as const,
  backlogItemsList: (params: { sprintId?: string; projectId?: string }) =>
    [...planningKeys.backlogItems(), "list", params] as const,
  backlogItemDetail: (id: string) => [...planningKeys.backlogItems(), "detail", id] as const,
  // Hierarchy
  hierarchy: (projectId: string) => [...planningKeys.all, "hierarchy", projectId] as const,
  // Dashboard
  activeDashboard: (projectId: string) => [...planningKeys.all, "dashboard", projectId] as const,
};

// =============================================================================
// ROADMAP HOOKS
// =============================================================================

/**
 * Fetch roadmaps for a project
 */
export function useRoadmaps(projectId: string) {
  return useQuery({
    queryKey: planningKeys.roadmapsList(projectId),
    queryFn: () => getRoadmaps(projectId),
    enabled: !!projectId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

/**
 * Fetch single roadmap by ID
 */
export function useRoadmap(id: string) {
  return useQuery({
    queryKey: planningKeys.roadmapDetail(id),
    queryFn: () => getRoadmap(id),
    enabled: !!id,
  });
}

/**
 * Create a new roadmap
 */
export function useCreateRoadmap() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: RoadmapInput) => createRoadmap(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: planningKeys.roadmapsList(variables.project_id),
      });
      queryClient.invalidateQueries({
        queryKey: planningKeys.hierarchy(variables.project_id),
      });
    },
  });
}

/**
 * Update a roadmap
 */
export function useUpdateRoadmap(id: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Partial<RoadmapInput>) => updateRoadmap(id, data),
    onSuccess: (roadmap) => {
      queryClient.setQueryData(planningKeys.roadmapDetail(id), roadmap);
      queryClient.invalidateQueries({
        queryKey: planningKeys.roadmapsList(roadmap.project_id),
      });
    },
  });
}

/**
 * Delete a roadmap
 */
export function useDeleteRoadmap() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id }: { id: string; projectId: string }) => deleteRoadmap(id),
    onSuccess: (_, { projectId }) => {
      queryClient.invalidateQueries({
        queryKey: planningKeys.roadmapsList(projectId),
      });
      queryClient.invalidateQueries({
        queryKey: planningKeys.hierarchy(projectId),
      });
    },
  });
}

// =============================================================================
// PHASE HOOKS
// =============================================================================

/**
 * Fetch phases for a roadmap
 */
export function usePhases(roadmapId: string) {
  return useQuery({
    queryKey: planningKeys.phasesList(roadmapId),
    queryFn: () => getPhases(roadmapId),
    enabled: !!roadmapId,
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Fetch single phase by ID
 */
export function usePhase(id: string) {
  return useQuery({
    queryKey: planningKeys.phaseDetail(id),
    queryFn: () => getPhase(id),
    enabled: !!id,
  });
}

/**
 * Create a new phase
 */
export function useCreatePhase() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: PhaseInput) => createPhase(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: planningKeys.phasesList(variables.roadmap_id),
      });
    },
  });
}

/**
 * Update a phase
 */
export function useUpdatePhase(id: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Partial<PhaseInput>) => updatePhase(id, data),
    onSuccess: (phase) => {
      queryClient.setQueryData(planningKeys.phaseDetail(id), phase);
      queryClient.invalidateQueries({
        queryKey: planningKeys.phasesList(phase.roadmap_id),
      });
    },
  });
}

/**
 * Delete a phase
 */
export function useDeletePhase() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id }: { id: string; roadmapId: string }) => deletePhase(id),
    onSuccess: (_, { roadmapId }) => {
      queryClient.invalidateQueries({
        queryKey: planningKeys.phasesList(roadmapId),
      });
    },
  });
}

// =============================================================================
// SPRINT HOOKS
// =============================================================================

/**
 * Fetch sprints with optional filters
 */
export function useSprints(params: { projectId?: string; phaseId?: string } = {}) {
  return useQuery({
    queryKey: planningKeys.sprintsList(params),
    queryFn: () => getSprints(params),
    enabled: !!(params.projectId || params.phaseId),
    staleTime: 2 * 60 * 1000, // 2 minutes - sprints change more frequently
  });
}

/**
 * Fetch single sprint by ID
 */
export function useSprint(id: string) {
  return useQuery({
    queryKey: planningKeys.sprintDetail(id),
    queryFn: () => getSprint(id),
    enabled: !!id,
  });
}

/**
 * Fetch active sprint for a project
 */
export function useActiveSprint(projectId: string) {
  return useQuery({
    queryKey: planningKeys.activeSprint(projectId),
    queryFn: () => getActiveSprint(projectId),
    enabled: !!projectId,
    staleTime: 1 * 60 * 1000, // 1 minute - active sprint data should be fresh
  });
}

/**
 * Create a new sprint
 */
export function useCreateSprint() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: SprintInput) => createSprint(data),
    onSuccess: (sprint, variables) => {
      // Invalidate sprint lists
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprintsList({ projectId: variables.project_id }),
      });
      if (variables.phase_id) {
        queryClient.invalidateQueries({
          queryKey: planningKeys.sprintsList({ phaseId: variables.phase_id }),
        });
      }
      // Invalidate hierarchy
      queryClient.invalidateQueries({
        queryKey: planningKeys.hierarchy(variables.project_id),
      });
    },
  });
}

/**
 * Update a sprint
 */
export function useUpdateSprint(id: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: SprintUpdateInput) => updateSprint(id, data),
    onSuccess: (sprint) => {
      queryClient.setQueryData(planningKeys.sprintDetail(id), sprint);
      // Invalidate sprint lists
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprintsList({ projectId: sprint.project_id }),
      });
      // Invalidate active sprint if this is the active one
      if (sprint.status === "active") {
        queryClient.invalidateQueries({
          queryKey: planningKeys.activeSprint(sprint.project_id),
        });
      }
    },
  });
}

/**
 * Delete a sprint
 */
export function useDeleteSprint() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id }: { id: string; projectId: string }) => deleteSprint(id),
    onSuccess: (_, { projectId }) => {
      queryClient.invalidateQueries({
        queryKey: planningKeys.sprintsList({ projectId }),
      });
      queryClient.invalidateQueries({
        queryKey: planningKeys.hierarchy(projectId),
      });
    },
  });
}

// =============================================================================
// BACKLOG ITEM HOOKS
// =============================================================================

/**
 * Fetch backlog items with optional filters
 */
export function useBacklogItems(params: { sprintId?: string; projectId?: string } = {}) {
  return useQuery({
    queryKey: planningKeys.backlogItemsList(params),
    queryFn: () => getBacklogItems(params),
    enabled: !!(params.sprintId || params.projectId),
    staleTime: 1 * 60 * 1000, // 1 minute
  });
}

/**
 * Fetch single backlog item by ID
 */
export function useBacklogItem(id: string) {
  return useQuery({
    queryKey: planningKeys.backlogItemDetail(id),
    queryFn: () => getBacklogItem(id),
    enabled: !!id,
  });
}

/**
 * Create a new backlog item
 */
export function useCreateBacklogItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: BacklogItemInput) => createBacklogItem(data),
    onSuccess: (item, variables) => {
      // Invalidate backlog lists
      queryClient.invalidateQueries({
        queryKey: planningKeys.backlogItemsList({ projectId: variables.project_id }),
      });
      if (variables.sprint_id) {
        queryClient.invalidateQueries({
          queryKey: planningKeys.backlogItemsList({ sprintId: variables.sprint_id }),
        });
        // Update sprint item counts
        queryClient.invalidateQueries({
          queryKey: planningKeys.sprintDetail(variables.sprint_id),
        });
      }
    },
  });
}

/**
 * Update a backlog item
 */
export function useUpdateBacklogItem(id: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: BacklogItemUpdateInput) => updateBacklogItem(id, data),
    onSuccess: (item) => {
      queryClient.setQueryData(planningKeys.backlogItemDetail(id), item);
      // Invalidate relevant lists
      queryClient.invalidateQueries({
        queryKey: planningKeys.backlogItemsList({ projectId: item.project_id }),
      });
      if (item.sprint_id) {
        queryClient.invalidateQueries({
          queryKey: planningKeys.backlogItemsList({ sprintId: item.sprint_id }),
        });
        queryClient.invalidateQueries({
          queryKey: planningKeys.sprintDetail(item.sprint_id),
        });
      }
    },
  });
}

/**
 * Delete a backlog item
 */
export function useDeleteBacklogItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
    }: {
      id: string;
      projectId: string;
      sprintId?: string;
    }) => deleteBacklogItem(id),
    onSuccess: (_, { projectId, sprintId }) => {
      queryClient.invalidateQueries({
        queryKey: planningKeys.backlogItemsList({ projectId }),
      });
      if (sprintId) {
        queryClient.invalidateQueries({
          queryKey: planningKeys.backlogItemsList({ sprintId }),
        });
        queryClient.invalidateQueries({
          queryKey: planningKeys.sprintDetail(sprintId),
        });
      }
    },
  });
}

/**
 * Bulk move backlog items (drag and drop)
 */
export function useBulkMoveBacklogItems() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ projectId, data }: { projectId: string; data: BulkMoveItemsInput }) =>
      bulkMoveBacklogItems(projectId, data),
    onSuccess: (_, { projectId, data }) => {
      // Invalidate all backlog lists for the project
      queryClient.invalidateQueries({
        queryKey: planningKeys.backlogItemsList({ projectId }),
      });
      // Invalidate the target sprint
      if (data.target_sprint_id) {
        queryClient.invalidateQueries({
          queryKey: planningKeys.backlogItemsList({ sprintId: data.target_sprint_id }),
        });
        queryClient.invalidateQueries({
          queryKey: planningKeys.sprintDetail(data.target_sprint_id),
        });
      }
    },
  });
}

// =============================================================================
// HIERARCHY & DASHBOARD HOOKS
// =============================================================================

/**
 * Fetch full planning hierarchy for a project
 */
export function usePlanningHierarchy(projectId: string) {
  return useQuery({
    queryKey: planningKeys.hierarchy(projectId),
    queryFn: () => getPlanningHierarchy(projectId),
    enabled: !!projectId,
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Fetch active sprint dashboard data
 */
export function useActiveSprintDashboard(projectId: string) {
  return useQuery({
    queryKey: planningKeys.activeDashboard(projectId),
    queryFn: () => getActiveSprintDashboard(projectId),
    enabled: !!projectId,
    staleTime: 1 * 60 * 1000, // 1 minute - dashboard should be fresh
    refetchInterval: 60 * 1000, // Auto-refresh every minute
  });
}

// =============================================================================
// COMBINED HOOKS
// =============================================================================

/**
 * Combined hook for sprint management operations
 */
export function useSprintManagement(projectId: string) {
  const queryClient = useQueryClient();
  const sprints = useSprints({ projectId });
  const activeSprint = useActiveSprint(projectId);
  const createMutation = useCreateSprint();
  const updateMutation = useUpdateSprint(activeSprint.data?.id || "");
  const deleteMutation = useDeleteSprint();

  return {
    // Data
    sprints: sprints.data?.sprints || [],
    activeSprint: activeSprint.data,
    // Loading states
    isLoading: sprints.isLoading || activeSprint.isLoading,
    isCreating: createMutation.isPending,
    isUpdating: updateMutation.isPending,
    isDeleting: deleteMutation.isPending,
    // Error states
    error: sprints.error || activeSprint.error,
    // Mutations
    createSprint: createMutation.mutateAsync,
    updateSprint: (sprintId: string, data: SprintUpdateInput) =>
      updateSprint(sprintId, data).then((sprint) => {
        queryClient.invalidateQueries({ queryKey: planningKeys.sprintsList({ projectId }) });
        return sprint;
      }),
    deleteSprint: (sprintId: string) =>
      deleteMutation.mutateAsync({ id: sprintId, projectId }),
    // Refresh
    refetch: () => {
      sprints.refetch();
      activeSprint.refetch();
    },
  };
}

/**
 * Combined hook for backlog management
 */
export function useBacklogManagement(projectId: string, sprintId?: string) {
  const items = useBacklogItems({ projectId, sprintId });
  const createMutation = useCreateBacklogItem();
  const bulkMoveMutation = useBulkMoveBacklogItems();

  return {
    // Data
    items: items.data?.items || [],
    total: items.data?.total || 0,
    // Loading states
    isLoading: items.isLoading,
    isCreating: createMutation.isPending,
    isMoving: bulkMoveMutation.isPending,
    // Error
    error: items.error,
    // Mutations
    createItem: createMutation.mutateAsync,
    bulkMove: (data: BulkMoveItemsInput) =>
      bulkMoveMutation.mutateAsync({ projectId, data }),
    // Refresh
    refetch: items.refetch,
  };
}
