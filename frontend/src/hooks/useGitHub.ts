/**
 * GitHub TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useGitHub
 * @description React Query hooks for GitHub Integration API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 69 - CTO Go-Live Requirements
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getGitHubConnectionStatus,
  getGitHubRepositories,
  getGitHubPullRequests,
  disconnectGitHub,
  type GitHubConnectionStatus,
  type GitHubRepository,
  type GitHubPullRequest,
} from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";

// Query keys for cache management
export const githubKeys = {
  all: ["github"] as const,
  status: () => [...githubKeys.all, "status"] as const,
  repos: () => [...githubKeys.all, "repos"] as const,
  pulls: () => [...githubKeys.all, "pulls"] as const,
  pullList: (owner: string, repo: string, options?: { state?: string }) =>
    [...githubKeys.pulls(), owner, repo, options] as const,
};

/**
 * Hook to fetch GitHub connection status
 * Sprint 69: Check if user has connected GitHub
 */
export function useGitHubStatus() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: githubKeys.status(),
    queryFn: getGitHubConnectionStatus,
    enabled: isAuthenticated && !authLoading,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: false, // Don't retry if not connected
  });
}

/**
 * Hook to fetch user's GitHub repositories
 * Sprint 69: List repos for project linking
 */
export function useGitHubRepositories() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const { data: status } = useGitHubStatus();

  return useQuery({
    queryKey: githubKeys.repos(),
    queryFn: getGitHubRepositories,
    enabled: isAuthenticated && !authLoading && status?.connected === true,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

/**
 * Hook to fetch pull requests for a repository
 * Sprint 69: PR monitoring and validation
 */
export function useGitHubPullRequests(
  owner: string | undefined,
  repo: string | undefined,
  options?: { state?: "open" | "closed" | "all" }
) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const { data: status } = useGitHubStatus();

  return useQuery({
    queryKey: githubKeys.pullList(owner || "", repo || "", options),
    queryFn: () => {
      if (!owner || !repo) {
        throw new Error("Missing owner or repo");
      }
      return getGitHubPullRequests(owner, repo, options);
    },
    enabled:
      isAuthenticated &&
      !authLoading &&
      status?.connected === true &&
      !!owner &&
      !!repo,
    staleTime: 60 * 1000, // 1 minute - PRs change frequently
  });
}

/**
 * Hook to disconnect GitHub integration
 * Sprint 69: Allow users to unlink GitHub
 */
export function useDisconnectGitHub() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: disconnectGitHub,
    onSuccess: () => {
      // Invalidate all GitHub queries
      queryClient.invalidateQueries({ queryKey: githubKeys.all });
    },
  });
}

/**
 * Hook to invalidate GitHub cache
 */
export function useInvalidateGitHub() {
  const queryClient = useQueryClient();

  return () => {
    queryClient.invalidateQueries({ queryKey: githubKeys.all });
  };
}

// Export types for use in components
export type { GitHubConnectionStatus, GitHubRepository, GitHubPullRequest };
