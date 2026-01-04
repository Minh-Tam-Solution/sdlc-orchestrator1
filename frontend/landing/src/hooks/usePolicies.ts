/**
 * Policies TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/usePolicies
 * @description React Query hooks for Policies API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 65 - Route Group Migration
 */

import { useQuery } from "@tanstack/react-query";
import {
  getPolicies,
  getPolicy,
  type Policy,
  type PolicyListResponse,
  type PolicyListOptions,
} from "@/lib/api";

// Query keys for cache management
export const policyKeys = {
  all: ["policies"] as const,
  lists: () => [...policyKeys.all, "list"] as const,
  list: (options?: PolicyListOptions) => [...policyKeys.lists(), options] as const,
  details: () => [...policyKeys.all, "detail"] as const,
  detail: (id: string) => [...policyKeys.details(), id] as const,
};

/**
 * Get access token from localStorage
 */
function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

/**
 * Hook to fetch list of policies with pagination and filters
 */
export function usePolicies(options?: PolicyListOptions) {
  const accessToken = getAccessToken();

  return useQuery({
    queryKey: policyKeys.list(options),
    queryFn: async () => {
      if (!accessToken) {
        throw new Error("Not authenticated");
      }
      return getPolicies(accessToken, options);
    },
    enabled: !!accessToken,
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
 */
export function usePolicy(policyId: string | undefined) {
  const accessToken = getAccessToken();

  return useQuery({
    queryKey: policyKeys.detail(policyId || ""),
    queryFn: async () => {
      if (!accessToken || !policyId) {
        throw new Error("Not authenticated or missing policy ID");
      }
      return getPolicy(accessToken, policyId);
    },
    enabled: !!accessToken && !!policyId,
    staleTime: 60 * 1000, // 1 minute
  });
}

// Export types for use in components
export type { Policy, PolicyListResponse, PolicyListOptions };
