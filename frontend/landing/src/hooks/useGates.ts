/**
 * Gates TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useGates
 * @description React Query hooks for Gates API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 69 - Cookie Auth Migration
 */

import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  getGates,
  getGate,
  type Gate,
  type GateListResponse,
  type GateListOptions,
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

// Export types for use in components
export type { Gate, GateListResponse, GateListOptions };
