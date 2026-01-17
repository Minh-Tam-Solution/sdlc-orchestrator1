/**
 * Gates TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useGates
 * @description React Query hooks for Gates API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 69 - CTO Go-Live Requirements
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getGates,
  getGate,
  submitGate,
  approveGate,
  getGateApprovals,
  type Gate,
  type GateListResponse,
  type GateListOptions,
  type GateSubmitRequest,
  type GateApprovalRequest,
  type GateApproval,
} from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";

// Query keys for cache management
export const gateKeys = {
  all: ["gates"] as const,
  lists: () => [...gateKeys.all, "list"] as const,
  list: (options?: GateListOptions) => [...gateKeys.lists(), options] as const,
  details: () => [...gateKeys.all, "detail"] as const,
  detail: (id: string) => [...gateKeys.details(), id] as const,
};

/**
 * Hook to fetch list of gates with pagination and filters
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function useGates(options?: GateListOptions) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: gateKeys.list(options),
    queryFn: () => getGates(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to fetch gates by project ID
 */
export function useProjectGates(projectId: string | undefined) {
  return useGates(projectId ? { project_id: projectId } : undefined);
}

/**
 * Hook to fetch gates by stage
 */
export function useGatesByStage(stage: string | undefined) {
  return useGates(stage ? { stage } : undefined);
}

/**
 * Hook to fetch a single gate by ID
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function useGate(gateId: string | undefined) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: gateKeys.detail(gateId || ""),
    queryFn: () => {
      if (!gateId) {
        throw new Error("Missing gate ID");
      }
      return getGate(gateId);
    },
    enabled: isAuthenticated && !authLoading && !!gateId,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to invalidate gates cache
 */
export function useInvalidateGates() {
  const queryClient = useQueryClient();

  return () => {
    queryClient.invalidateQueries({ queryKey: gateKeys.all });
  };
}

/**
 * Hook to fetch gate approval history
 * Sprint 69: Audit trail for gate decisions
 */
export function useGateApprovals(gateId: string | undefined) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: [...gateKeys.details(), gateId, "approvals"] as const,
    queryFn: () => {
      if (!gateId) {
        throw new Error("Missing gate ID");
      }
      return getGateApprovals(gateId);
    },
    enabled: isAuthenticated && !authLoading && !!gateId,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to submit gate for approval
 * Sprint 69: Gate workflow - submit DRAFT → PENDING_APPROVAL
 */
export function useSubmitGate() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      gateId,
      data,
    }: {
      gateId: string;
      data?: GateSubmitRequest;
    }) => submitGate(gateId, data),
    onSuccess: (updatedGate) => {
      // Invalidate gates list
      queryClient.invalidateQueries({ queryKey: gateKeys.lists() });
      // Update the specific gate in cache
      queryClient.setQueryData(gateKeys.detail(updatedGate.id), updatedGate);
    },
  });
}

/**
 * Hook to approve or reject gate (CTO/CPO/CEO only)
 * Sprint 69: Gate workflow - approve/reject PENDING_APPROVAL → APPROVED/REJECTED
 */
export function useApproveGate() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      gateId,
      data,
    }: {
      gateId: string;
      data: GateApprovalRequest;
    }) => approveGate(gateId, data),
    onSuccess: (updatedGate) => {
      // Invalidate gates list
      queryClient.invalidateQueries({ queryKey: gateKeys.lists() });
      // Update the specific gate in cache
      queryClient.setQueryData(gateKeys.detail(updatedGate.id), updatedGate);
      // Invalidate approvals for this gate
      queryClient.invalidateQueries({
        queryKey: [...gateKeys.details(), updatedGate.id, "approvals"],
      });
    },
  });
}

// Export types for use in components
export type {
  Gate,
  GateListResponse,
  GateListOptions,
  GateSubmitRequest,
  GateApprovalRequest,
  GateApproval,
};
