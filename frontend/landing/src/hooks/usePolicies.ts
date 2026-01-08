/**
 * Policies TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/usePolicies
 * @description React Query hooks for Policies API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 69 - Cookie Auth Migration
 */

import { useQuery } from "@tanstack/react-query";
import {
  getPolicies,
  getPolicy,
  type Policy,
  type PolicyListResponse,
  type PolicyListOptions,
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

// Export types for use in components
export type { Policy, PolicyListResponse, PolicyListOptions };
