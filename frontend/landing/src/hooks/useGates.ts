/**
 * Gates TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useGates
 * @description React Query hooks for Gates API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 62 - Route Group Migration
 */

import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  getGates,
  getGate,
  type Gate,
  type GateListResponse,
  type GateListOptions,
} from "@/lib/api";

// Query keys for cache management
export const gateKeys = {
  all: ["gates"] as const,
  lists: () => [...gateKeys.all, "list"] as const,
  list: (options?: GateListOptions) => [...gateKeys.lists(), options] as const,
  details: () => [...gateKeys.all, "detail"] as const,
  detail: (id: string) => [...gateKeys.details(), id] as const,
};

/**
 * Get access token from localStorage
 */
function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

/**
 * Hook to fetch list of gates with pagination and filters
 */
export function useGates(options?: GateListOptions) {
  const accessToken = getAccessToken();

  return useQuery({
    queryKey: gateKeys.list(options),
    queryFn: async () => {
      if (!accessToken) {
        throw new Error("Not authenticated");
      }
      return getGates(accessToken, options);
    },
    enabled: !!accessToken,
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
 */
export function useGate(gateId: string | undefined) {
  const accessToken = getAccessToken();

  return useQuery({
    queryKey: gateKeys.detail(gateId || ""),
    queryFn: async () => {
      if (!accessToken || !gateId) {
        throw new Error("Not authenticated or missing gate ID");
      }
      return getGate(accessToken, gateId);
    },
    enabled: !!accessToken && !!gateId,
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

// Export types for use in components
export type { Gate, GateListResponse, GateListOptions };
