/**
 * Projects TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useProjects
 * @description React Query hooks for Projects API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 62 - Route Group Migration
 */

import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  getProjects,
  getProject,
  type Project,
  type ProjectDetail,
} from "@/lib/api";

// Query keys for cache management
export const projectKeys = {
  all: ["projects"] as const,
  lists: () => [...projectKeys.all, "list"] as const,
  list: (options?: { skip?: number; limit?: number }) =>
    [...projectKeys.lists(), options] as const,
  details: () => [...projectKeys.all, "detail"] as const,
  detail: (id: string) => [...projectKeys.details(), id] as const,
};

/**
 * Get access token from localStorage
 */
function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

/**
 * Hook to fetch list of projects
 */
export function useProjects(options?: { skip?: number; limit?: number }) {
  const accessToken = getAccessToken();

  return useQuery({
    queryKey: projectKeys.list(options),
    queryFn: async () => {
      if (!accessToken) {
        throw new Error("Not authenticated");
      }
      return getProjects(accessToken, options);
    },
    enabled: !!accessToken,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to fetch a single project by ID
 */
export function useProject(projectId: string | undefined) {
  const accessToken = getAccessToken();

  return useQuery({
    queryKey: projectKeys.detail(projectId || ""),
    queryFn: async () => {
      if (!accessToken || !projectId) {
        throw new Error("Not authenticated or missing project ID");
      }
      return getProject(accessToken, projectId);
    },
    enabled: !!accessToken && !!projectId,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to invalidate projects cache
 */
export function useInvalidateProjects() {
  const queryClient = useQueryClient();

  return () => {
    queryClient.invalidateQueries({ queryKey: projectKeys.all });
  };
}

// Export types for use in components
export type { Project, ProjectDetail };
