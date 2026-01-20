/**
 * CLI Tokens Hook - SDLC Orchestrator
 *
 * @module frontend/src/hooks/useCliTokens
 * @description TanStack Query hooks for CLI token management (Sprint 85)
 * @sdlc SDLC 5.1.3 Framework - Sprint 85 (CLI Authentication)
 * @status Sprint 85 - CTO APPROVED (January 20, 2026)
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getCliTokens,
  getCliToken,
  createCliToken,
  revokeCliToken,
  refreshCliToken,
  getCliTokenStats,
  getCliSessions,
  revokeCliSession,
  initiateCliLogin,
  verifyCliLogin,
  getCliDevices,
} from "@/lib/api";
import type {
  CliToken,
  CliTokenListParams,
  CreateCliTokenRequest,
  CliTokenStats,
  CliSession,
  CliLoginRequest,
  CliDevice,
} from "@/lib/types/cli-token";

// =============================================================================
// Query Keys
// =============================================================================

export const cliTokenKeys = {
  all: ["cli-tokens"] as const,
  lists: () => [...cliTokenKeys.all, "list"] as const,
  list: (params?: CliTokenListParams) =>
    [...cliTokenKeys.lists(), params] as const,
  details: () => [...cliTokenKeys.all, "detail"] as const,
  detail: (id: string) => [...cliTokenKeys.details(), id] as const,
  stats: () => [...cliTokenKeys.all, "stats"] as const,
  sessions: () => [...cliTokenKeys.all, "sessions"] as const,
  devices: () => [...cliTokenKeys.all, "devices"] as const,
  login: (deviceCode: string) =>
    [...cliTokenKeys.all, "login", deviceCode] as const,
};

// =============================================================================
// Query Hooks
// =============================================================================

/**
 * Fetch list of CLI tokens
 */
export function useCliTokens(params?: CliTokenListParams) {
  return useQuery({
    queryKey: cliTokenKeys.list(params),
    queryFn: () => getCliTokens(params),
    staleTime: 30 * 1000, // 30 seconds
  });
}

/**
 * Fetch single CLI token details
 */
export function useCliToken(tokenId: string) {
  return useQuery({
    queryKey: cliTokenKeys.detail(tokenId),
    queryFn: () => getCliToken(tokenId),
    enabled: !!tokenId,
  });
}

/**
 * Fetch CLI token statistics
 */
export function useCliTokenStats() {
  return useQuery({
    queryKey: cliTokenKeys.stats(),
    queryFn: () => getCliTokenStats(),
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Fetch active CLI sessions
 */
export function useCliSessions() {
  return useQuery({
    queryKey: cliTokenKeys.sessions(),
    queryFn: () => getCliSessions(),
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 60 * 1000, // Refetch every minute
  });
}

/**
 * Fetch registered CLI devices
 */
export function useCliDevices() {
  return useQuery({
    queryKey: cliTokenKeys.devices(),
    queryFn: () => getCliDevices(),
    staleTime: 60 * 1000, // 1 minute
  });
}

// =============================================================================
// Mutation Hooks
// =============================================================================

/**
 * Create a new CLI token
 */
export function useCreateCliToken() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateCliTokenRequest) => createCliToken(data),
    onSuccess: () => {
      // Invalidate token list and stats
      queryClient.invalidateQueries({ queryKey: cliTokenKeys.lists() });
      queryClient.invalidateQueries({ queryKey: cliTokenKeys.stats() });
    },
  });
}

/**
 * Revoke a CLI token
 */
export function useRevokeCliToken() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (tokenId: string) => revokeCliToken(tokenId),
    onSuccess: (_, tokenId) => {
      // Invalidate specific token and lists
      queryClient.invalidateQueries({ queryKey: cliTokenKeys.detail(tokenId) });
      queryClient.invalidateQueries({ queryKey: cliTokenKeys.lists() });
      queryClient.invalidateQueries({ queryKey: cliTokenKeys.stats() });
    },
  });
}

/**
 * Refresh/rotate a CLI token
 */
export function useRefreshCliToken() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ tokenId, extendDays }: { tokenId: string; extendDays?: number }) =>
      refreshCliToken(tokenId, extendDays),
    onSuccess: (_, { tokenId }) => {
      queryClient.invalidateQueries({ queryKey: cliTokenKeys.detail(tokenId) });
      queryClient.invalidateQueries({ queryKey: cliTokenKeys.lists() });
    },
  });
}

/**
 * Revoke a CLI session
 */
export function useRevokeCliSession() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (sessionId: string) => revokeCliSession(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: cliTokenKeys.sessions() });
    },
  });
}

// =============================================================================
// CLI Login Flow Hooks
// =============================================================================

/**
 * Initiate CLI login (device flow)
 */
export function useInitiateCliLogin() {
  return useMutation({
    mutationFn: () => initiateCliLogin(),
  });
}

/**
 * Poll for CLI login verification
 */
export function useVerifyCliLogin(
  deviceCode: string | null,
  options?: { enabled?: boolean; interval?: number }
) {
  return useQuery({
    queryKey: cliTokenKeys.login(deviceCode || ""),
    queryFn: () => verifyCliLogin(deviceCode!),
    enabled: !!deviceCode && (options?.enabled ?? true),
    refetchInterval: options?.interval ?? 5000, // Poll every 5 seconds
    refetchIntervalInBackground: false,
  });
}

// =============================================================================
// Combined Hooks
// =============================================================================

/**
 * Combined hook for CLI tokens page
 * Returns tokens, stats, and sessions in a single hook
 */
export function useCliTokensDashboard(params?: CliTokenListParams) {
  const tokensQuery = useCliTokens(params);
  const statsQuery = useCliTokenStats();
  const sessionsQuery = useCliSessions();

  return {
    // Tokens
    tokens: tokensQuery.data?.items ?? [],
    totalTokens: tokensQuery.data?.total ?? 0,
    hasMoreTokens: tokensQuery.data?.has_more ?? false,

    // Stats
    stats: statsQuery.data,

    // Sessions
    sessions: sessionsQuery.data ?? [],

    // Loading states
    isLoading:
      tokensQuery.isLoading || statsQuery.isLoading || sessionsQuery.isLoading,
    isLoadingTokens: tokensQuery.isLoading,
    isLoadingStats: statsQuery.isLoading,
    isLoadingSessions: sessionsQuery.isLoading,

    // Error states
    error: tokensQuery.error || statsQuery.error || sessionsQuery.error,

    // Refetch functions
    refetchTokens: tokensQuery.refetch,
    refetchStats: statsQuery.refetch,
    refetchSessions: sessionsQuery.refetch,
    refetchAll: () => {
      tokensQuery.refetch();
      statsQuery.refetch();
      sessionsQuery.refetch();
    },
  };
}

/**
 * Hook for token detail page
 */
export function useCliTokenDetail(tokenId: string) {
  const tokenQuery = useCliToken(tokenId);
  const revokeTokenMutation = useRevokeCliToken();
  const refreshTokenMutation = useRefreshCliToken();

  return {
    token: tokenQuery.data,
    isLoading: tokenQuery.isLoading,
    error: tokenQuery.error,
    refetch: tokenQuery.refetch,

    // Actions
    revoke: () => revokeTokenMutation.mutateAsync(tokenId),
    refresh: (extendDays?: number) =>
      refreshTokenMutation.mutateAsync({ tokenId, extendDays }),

    // Action states
    isRevoking: revokeTokenMutation.isPending,
    isRefreshing: refreshTokenMutation.isPending,
  };
}

// =============================================================================
// Utility Hooks
// =============================================================================

/**
 * Hook to get count of active tokens
 */
export function useActiveTokenCount() {
  const { data: stats } = useCliTokenStats();
  return stats?.active_tokens ?? 0;
}

/**
 * Hook to check if user has any CLI tokens
 */
export function useHasCliTokens() {
  const { data: stats, isLoading } = useCliTokenStats();
  return {
    hasTokens: (stats?.total_tokens ?? 0) > 0,
    isLoading,
  };
}

// =============================================================================
// Prefetch Functions
// =============================================================================

/**
 * Prefetch CLI tokens for page navigation
 */
export function usePrefetchCliTokens() {
  const queryClient = useQueryClient();

  return (params?: CliTokenListParams) => {
    queryClient.prefetchQuery({
      queryKey: cliTokenKeys.list(params),
      queryFn: () => getCliTokens(params),
      staleTime: 30 * 1000,
    });
  };
}

/**
 * Prefetch token detail
 */
export function usePrefetchCliToken() {
  const queryClient = useQueryClient();

  return (tokenId: string) => {
    queryClient.prefetchQuery({
      queryKey: cliTokenKeys.detail(tokenId),
      queryFn: () => getCliToken(tokenId),
      staleTime: 30 * 1000,
    });
  };
}

// =============================================================================
// Type Exports
// =============================================================================

export type {
  CliToken,
  CliTokenListParams,
  CreateCliTokenRequest,
  CliTokenStats,
  CliSession,
  CliLoginRequest,
  CliDevice,
};
