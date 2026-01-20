/**
 * Sprint Governance Hooks - SDLC Orchestrator
 *
 * @module frontend/src/hooks/useSprintGovernance
 * @description TanStack Query hooks for Sprint Governance (G-Sprint & G-Sprint-Close Gates)
 * @sdlc SDLC 5.1.3 Framework - Sprint 87 (Sprint Governance UI)
 * @reference SDLC 5.1.3 Pillar 2: Sprint Planning Governance
 * @status Sprint 87 - Core Feature Implementation
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getSprintGate,
  getSprintGateChecklist,
  evaluateSprintGate,
  approveSprintGate,
  updateChecklistItem,
  getDocumentationDeadline,
  getSprintGovernanceMetrics,
  getSprintComparison,
  getSprintGovernanceDashboard,
} from "@/lib/api";
import type {
  SprintGateType,
  SprintGateApprovalRequest,
  UpdateChecklistItemRequest,
} from "@/lib/types/sprint-governance";

// =============================================================================
// QUERY KEYS
// =============================================================================

export const sprintGovernanceKeys = {
  all: ["sprint-governance"] as const,
  // Gates
  gates: () => [...sprintGovernanceKeys.all, "gates"] as const,
  gate: (sprintId: string, gateType: SprintGateType) =>
    [...sprintGovernanceKeys.gates(), sprintId, gateType] as const,
  checklist: (sprintId: string, gateType: SprintGateType) =>
    [...sprintGovernanceKeys.all, "checklist", sprintId, gateType] as const,
  // Documentation
  documentation: () => [...sprintGovernanceKeys.all, "documentation"] as const,
  deadline: (sprintId: string) =>
    [...sprintGovernanceKeys.documentation(), "deadline", sprintId] as const,
  // Metrics
  metrics: () => [...sprintGovernanceKeys.all, "metrics"] as const,
  sprintMetrics: (sprintId: string) =>
    [...sprintGovernanceKeys.metrics(), sprintId] as const,
  comparison: (sprintIds: string[]) =>
    [...sprintGovernanceKeys.metrics(), "comparison", sprintIds] as const,
  // Dashboard
  dashboard: (projectId: string) =>
    [...sprintGovernanceKeys.all, "dashboard", projectId] as const,
};

// =============================================================================
// GATE HOOKS
// =============================================================================

/**
 * Fetch sprint gate (G-Sprint or G-Sprint-Close)
 */
export function useSprintGate(sprintId: string, gateType: SprintGateType) {
  return useQuery({
    queryKey: sprintGovernanceKeys.gate(sprintId, gateType),
    queryFn: () => getSprintGate(sprintId, gateType),
    enabled: !!sprintId && !!gateType,
    staleTime: 1 * 60 * 1000, // 1 minute - gate status can change
  });
}

/**
 * Fetch gate checklist items
 */
export function useSprintGateChecklist(sprintId: string, gateType: SprintGateType) {
  return useQuery({
    queryKey: sprintGovernanceKeys.checklist(sprintId, gateType),
    queryFn: () => getSprintGateChecklist(sprintId, gateType),
    enabled: !!sprintId && !!gateType,
    staleTime: 30 * 1000, // 30 seconds - checklist may be updated frequently
  });
}

/**
 * Evaluate sprint gate
 */
export function useEvaluateSprintGate(sprintId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      gateType,
      forceEvaluation = false,
    }: {
      gateType: SprintGateType;
      forceEvaluation?: boolean;
    }) => evaluateSprintGate(sprintId, gateType, { force_evaluation: forceEvaluation }),
    onSuccess: (result, { gateType }) => {
      // Update gate data
      queryClient.setQueryData(
        sprintGovernanceKeys.gate(sprintId, gateType),
        result.gate
      );
      // Invalidate checklist
      queryClient.invalidateQueries({
        queryKey: sprintGovernanceKeys.checklist(sprintId, gateType),
      });
    },
  });
}

/**
 * Approve sprint gate
 */
export function useApproveSprintGate(sprintId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      gateType,
      data,
    }: {
      gateType: SprintGateType;
      data?: SprintGateApprovalRequest;
    }) => approveSprintGate(sprintId, gateType, data),
    onSuccess: (gate, { gateType }) => {
      // Update gate data
      queryClient.setQueryData(
        sprintGovernanceKeys.gate(sprintId, gateType),
        gate
      );
      // Invalidate sprint detail (status may have changed)
      queryClient.invalidateQueries({
        queryKey: ["planning", "sprints", "detail", sprintId],
      });
    },
  });
}

/**
 * Update checklist item
 */
export function useUpdateChecklistItem(sprintId: string, gateType: SprintGateType) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      itemId,
      data,
    }: {
      itemId: string;
      data: UpdateChecklistItemRequest;
    }) => updateChecklistItem(sprintId, gateType, itemId, data),
    onSuccess: () => {
      // Invalidate checklist
      queryClient.invalidateQueries({
        queryKey: sprintGovernanceKeys.checklist(sprintId, gateType),
      });
      // Invalidate gate (status may have changed)
      queryClient.invalidateQueries({
        queryKey: sprintGovernanceKeys.gate(sprintId, gateType),
      });
    },
  });
}

// =============================================================================
// DOCUMENTATION DEADLINE HOOKS
// =============================================================================

/**
 * Fetch documentation deadline for sprint close
 */
export function useDocumentationDeadline(sprintId: string) {
  return useQuery({
    queryKey: sprintGovernanceKeys.deadline(sprintId),
    queryFn: () => getDocumentationDeadline(sprintId),
    enabled: !!sprintId,
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 60 * 1000, // Auto-refresh every minute for countdown
  });
}

/**
 * Real-time documentation deadline with countdown
 */
export function useDocumentationDeadlineCountdown(sprintId: string) {
  const deadline = useDocumentationDeadline(sprintId);

  // Calculate hours remaining (client-side for real-time updates)
  const calculateHoursRemaining = () => {
    if (!deadline.data?.deadline) return 24;
    const deadlineDate = new Date(deadline.data.deadline);
    const now = new Date();
    const hoursRemaining = Math.max(
      0,
      (deadlineDate.getTime() - now.getTime()) / (1000 * 60 * 60)
    );
    return hoursRemaining;
  };

  return {
    ...deadline,
    hoursRemaining: calculateHoursRemaining(),
    isExpired: deadline.data?.is_expired || calculateHoursRemaining() <= 0,
    completionPercentage: deadline.data?.completion_percentage || 0,
  };
}

// =============================================================================
// METRICS HOOKS
// =============================================================================

/**
 * Fetch sprint governance metrics
 */
export function useSprintGovernanceMetrics(sprintId: string) {
  return useQuery({
    queryKey: sprintGovernanceKeys.sprintMetrics(sprintId),
    queryFn: () => getSprintGovernanceMetrics(sprintId),
    enabled: !!sprintId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

/**
 * Fetch sprint comparison data
 */
export function useSprintComparison(sprintIds: string[]) {
  return useQuery({
    queryKey: sprintGovernanceKeys.comparison(sprintIds),
    queryFn: () => getSprintComparison(sprintIds),
    enabled: sprintIds.length > 0,
    staleTime: 5 * 60 * 1000,
  });
}

// =============================================================================
// DASHBOARD HOOKS
// =============================================================================

/**
 * Fetch sprint governance dashboard data
 */
export function useSprintGovernanceDashboard(projectId: string) {
  return useQuery({
    queryKey: sprintGovernanceKeys.dashboard(projectId),
    queryFn: () => getSprintGovernanceDashboard(projectId),
    enabled: !!projectId,
    staleTime: 1 * 60 * 1000, // 1 minute
    refetchInterval: 60 * 1000, // Auto-refresh every minute
  });
}

// =============================================================================
// COMBINED HOOKS
// =============================================================================

/**
 * Combined hook for G-Sprint gate management
 */
export function useGSprintGate(sprintId: string) {
  const gate = useSprintGate(sprintId, "start");
  const checklist = useSprintGateChecklist(sprintId, "start");
  const evaluateMutation = useEvaluateSprintGate(sprintId);
  const approveMutation = useApproveSprintGate(sprintId);
  const updateItemMutation = useUpdateChecklistItem(sprintId, "start");

  return {
    // Data
    gate: gate.data,
    checklist: checklist.data,
    // Loading states
    isLoading: gate.isLoading || checklist.isLoading,
    isEvaluating: evaluateMutation.isPending,
    isApproving: approveMutation.isPending,
    isUpdatingItem: updateItemMutation.isPending,
    // Error states
    error: gate.error || checklist.error,
    // Mutations
    evaluate: (forceEvaluation?: boolean) =>
      evaluateMutation.mutateAsync({ gateType: "start", forceEvaluation }),
    approve: (data?: SprintGateApprovalRequest) =>
      approveMutation.mutateAsync({ gateType: "start", data }),
    updateItem: (itemId: string, data: UpdateChecklistItemRequest) =>
      updateItemMutation.mutateAsync({ itemId, data }),
    // Refresh
    refetch: () => {
      gate.refetch();
      checklist.refetch();
    },
  };
}

/**
 * Combined hook for G-Sprint-Close gate management
 */
export function useGSprintCloseGate(sprintId: string) {
  const gate = useSprintGate(sprintId, "close");
  const checklist = useSprintGateChecklist(sprintId, "close");
  const deadline = useDocumentationDeadlineCountdown(sprintId);
  const evaluateMutation = useEvaluateSprintGate(sprintId);
  const approveMutation = useApproveSprintGate(sprintId);
  const updateItemMutation = useUpdateChecklistItem(sprintId, "close");

  return {
    // Data
    gate: gate.data,
    checklist: checklist.data,
    deadline: deadline.data,
    hoursRemaining: deadline.hoursRemaining,
    isDeadlineExpired: deadline.isExpired,
    // Loading states
    isLoading: gate.isLoading || checklist.isLoading,
    isEvaluating: evaluateMutation.isPending,
    isApproving: approveMutation.isPending,
    isUpdatingItem: updateItemMutation.isPending,
    // Error states
    error: gate.error || checklist.error,
    // Mutations
    evaluate: (forceEvaluation?: boolean) =>
      evaluateMutation.mutateAsync({ gateType: "close", forceEvaluation }),
    approve: (data?: SprintGateApprovalRequest) =>
      approveMutation.mutateAsync({ gateType: "close", data }),
    updateItem: (itemId: string, data: UpdateChecklistItemRequest) =>
      updateItemMutation.mutateAsync({ itemId, data }),
    // Refresh
    refetch: () => {
      gate.refetch();
      checklist.refetch();
      deadline.refetch();
    },
  };
}

/**
 * Combined hook for full sprint governance management
 */
export function useSprintGovernanceAdmin(projectId: string, sprintId?: string) {
  const dashboard = useSprintGovernanceDashboard(projectId);

  // Get active sprint ID from dashboard if not provided
  const activeSprintId = sprintId || dashboard.data?.active_sprint?.id;

  // Only fetch gate data if we have a sprint ID
  const gSprint = useGSprintGate(activeSprintId || "");
  const gSprintClose = useGSprintCloseGate(activeSprintId || "");
  const metrics = useSprintGovernanceMetrics(activeSprintId || "");

  return {
    // Dashboard data
    dashboard: dashboard.data,
    activeSprint: dashboard.data?.active_sprint,
    upcomingSprints: dashboard.data?.upcoming_sprints || [],
    recentSprints: dashboard.data?.recent_sprints || [],
    overallMetrics: dashboard.data?.metrics,
    // Gate data
    gSprint: {
      ...gSprint,
      enabled: !!activeSprintId,
    },
    gSprintClose: {
      ...gSprintClose,
      enabled: !!activeSprintId,
    },
    // Sprint metrics
    metrics: metrics.data,
    // Loading states
    isLoading: dashboard.isLoading,
    isLoadingGates: gSprint.isLoading || gSprintClose.isLoading,
    // Error
    error: dashboard.error,
    // Refresh all
    refetchAll: () => {
      dashboard.refetch();
      if (activeSprintId) {
        gSprint.refetch();
        gSprintClose.refetch();
        metrics.refetch();
      }
    },
  };
}
