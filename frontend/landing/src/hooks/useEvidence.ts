/**
 * Evidence TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useEvidence
 * @description React Query hooks for Evidence API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 62 - Route Group Migration
 */

import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  getEvidenceList,
  getEvidence,
  type Evidence,
  type EvidenceListResponse,
  type EvidenceListOptions,
} from "@/lib/api";

// Query keys for cache management
export const evidenceKeys = {
  all: ["evidence"] as const,
  lists: () => [...evidenceKeys.all, "list"] as const,
  list: (options?: EvidenceListOptions) =>
    [...evidenceKeys.lists(), options] as const,
  details: () => [...evidenceKeys.all, "detail"] as const,
  detail: (id: string) => [...evidenceKeys.details(), id] as const,
};

/**
 * Get access token from localStorage
 */
function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

/**
 * Hook to fetch list of evidence with pagination and filters
 */
export function useEvidenceList(options?: EvidenceListOptions) {
  const accessToken = getAccessToken();

  return useQuery({
    queryKey: evidenceKeys.list(options),
    queryFn: async () => {
      if (!accessToken) {
        throw new Error("Not authenticated");
      }
      return getEvidenceList(accessToken, options);
    },
    enabled: !!accessToken,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to fetch evidence by gate ID
 */
export function useGateEvidence(gateId: string | undefined) {
  return useEvidenceList(gateId ? { gate_id: gateId } : undefined);
}

/**
 * Hook to fetch evidence by type
 */
export function useEvidenceByType(evidenceType: string | undefined) {
  return useEvidenceList(evidenceType ? { evidence_type: evidenceType } : undefined);
}

/**
 * Hook to fetch a single evidence item by ID
 */
export function useEvidence(evidenceId: string | undefined) {
  const accessToken = getAccessToken();

  return useQuery({
    queryKey: evidenceKeys.detail(evidenceId || ""),
    queryFn: async () => {
      if (!accessToken || !evidenceId) {
        throw new Error("Not authenticated or missing evidence ID");
      }
      return getEvidence(accessToken, evidenceId);
    },
    enabled: !!accessToken && !!evidenceId,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to invalidate evidence cache
 */
export function useInvalidateEvidence() {
  const queryClient = useQueryClient();

  return () => {
    queryClient.invalidateQueries({ queryKey: evidenceKeys.all });
  };
}

// Export types for use in components
export type { Evidence, EvidenceListResponse, EvidenceListOptions };
