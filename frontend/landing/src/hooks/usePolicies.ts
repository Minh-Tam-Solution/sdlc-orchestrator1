/**
 * Policies TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/usePolicies
 * @description React Query hooks for Policies API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 69 - CTO Go-Live Requirements
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getPolicies,
  getPolicy,
  updatePolicy,
  evaluatePolicy,
  getGateEvaluations,
  type Policy,
  type PolicyListResponse,
  type PolicyListOptions,
  type PolicyUpdateRequest,
  type PolicyEvaluationRequest,
  type PolicyEvaluationResult,
  type PolicyEvaluationListResponse,
} from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";

// Query keys for cache management
export const policyKeys = {
  all: ["policies"] as const,
  lists: () => [...policyKeys.all, "list"] as const,
  list: (options?: PolicyListOptions) => [...policyKeys.lists(), options] as const,
  details: () => [...policyKeys.all, "detail"] as const,
  detail: (id: string) => [...policyKeys.details(), id] as const,
};

/**
 * Hook to fetch list of policies with pagination and filters
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function usePolicies(options?: PolicyListOptions) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: policyKeys.list(options),
    queryFn: () => getPolicies(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to fetch policies by stage
 */
export function usePoliciesByStage(stage: string | undefined) {
  return usePolicies(stage && stage !== "all" ? { stage, is_active: true } : { is_active: true });
}

/**
 * Hook to fetch all policies for summary (larger page size)
 */
export function useAllPoliciesSummary() {
  return usePolicies({ page_size: 100, is_active: true });
}

/**
 * Hook to fetch a single policy by ID
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function usePolicy(policyId: string | undefined) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: policyKeys.detail(policyId || ""),
    queryFn: () => {
      if (!policyId) {
        throw new Error("Missing policy ID");
      }
      return getPolicy(policyId);
    },
    enabled: isAuthenticated && !authLoading && !!policyId,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to fetch policy evaluations for a gate
 * Sprint 69: Audit trail for policy compliance
 */
export function useGateEvaluations(gateId: string | undefined) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: [...policyKeys.all, "evaluations", gateId] as const,
    queryFn: () => {
      if (!gateId) {
        throw new Error("Missing gate ID");
      }
      return getGateEvaluations(gateId);
    },
    enabled: isAuthenticated && !authLoading && !!gateId,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to invalidate policies cache
 */
export function useInvalidatePolicies() {
  const queryClient = useQueryClient();

  return () => {
    queryClient.invalidateQueries({ queryKey: policyKeys.all });
  };
}

/**
 * Hook to update a policy
 * Sprint 69: Policy management with version tracking
 */
export function useUpdatePolicy() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      policyId,
      data,
    }: {
      policyId: string;
      data: PolicyUpdateRequest;
    }) => updatePolicy(policyId, data),
    onSuccess: (updatedPolicy) => {
      // Invalidate policies list
      queryClient.invalidateQueries({ queryKey: policyKeys.lists() });
      // Update the specific policy in cache
      queryClient.setQueryData(policyKeys.detail(updatedPolicy.id), updatedPolicy);
    },
  });
}

/**
 * Hook to evaluate a policy against a gate
 * Sprint 69: Real OPA policy evaluation
 */
export function useEvaluatePolicy() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: PolicyEvaluationRequest) => evaluatePolicy(data),
    onSuccess: (_, variables) => {
      // Invalidate evaluations for the gate
      queryClient.invalidateQueries({
        queryKey: [...policyKeys.all, "evaluations", variables.gate_id],
      });
    },
  });
}

// Export types for use in components
export type {
  Policy,
  PolicyListResponse,
  PolicyListOptions,
  PolicyUpdateRequest,
  PolicyEvaluationRequest,
  PolicyEvaluationResult,
  PolicyEvaluationListResponse,
};
