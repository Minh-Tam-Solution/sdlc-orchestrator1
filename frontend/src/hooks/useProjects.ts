/**
 * Projects TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useProjects
 * @description React Query hooks for Projects API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 69 - Cookie Auth Migration
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getProjects,
  getProject,
  createProject,
  type Project,
  type ProjectDetail,
  type CreateProjectRequest,
  type CreateProjectResponse,
} from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";

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
 * Hook to fetch list of projects
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function useProjects(options?: { skip?: number; limit?: number }) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: projectKeys.list(options),
    queryFn: () => getProjects(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to fetch a single project by ID
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function useProject(projectId: string | undefined) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: projectKeys.detail(projectId || ""),
    queryFn: () => {
      if (!projectId) {
        throw new Error("Missing project ID");
      }
      return getProject(projectId);
    },
    enabled: isAuthenticated && !authLoading && !!projectId,
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

/**
 * Hook to create a new project
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function useCreateProject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateProjectRequest): Promise<CreateProjectResponse> => {
      return createProject(data);
    },
    onSuccess: () => {
      // Invalidate projects list to refetch
      queryClient.invalidateQueries({ queryKey: projectKeys.all });
    },
  });
}

// Export types for use in components
export type { Project, ProjectDetail, CreateProjectRequest, CreateProjectResponse };
