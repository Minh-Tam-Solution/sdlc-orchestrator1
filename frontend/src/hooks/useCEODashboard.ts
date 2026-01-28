/**
 * =========================================================================
 * CEO Dashboard React Query Hooks
 * SDLC Orchestrator - Sprint 110 (CEO Dashboard & Observability)
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Framework: SDLC 5.3.0 Quality Assurance System
 * =========================================================================
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "./useAuth";
import {
  getCEODashboardSummary,
  getCEOTimeSaved,
  getCEORoutingBreakdown,
  getCEOPendingDecisions,
  getCEOWeeklySummary,
  getCEOTimeSavedTrend,
  getCEOVibecodingTrend,
  getCEOTopRejections,
  getCEOOverrides,
  getCEOSystemHealth,
  resolveCEODecision,
  recordCEOOverride,
  getCEODashboardHealth,
} from "@/lib/api";
import type {
  TimeRange,
  ResolveDecisionRequest,
  RecordOverrideRequest,
} from "@/lib/types/ceo-dashboard";

// Query key factory for cache management
export const ceoDashboardKeys = {
  all: ["ceo-dashboard"] as const,
  summary: (options?: { projectId?: string; timeRange?: TimeRange }) =>
    [...ceoDashboardKeys.all, "summary", options] as const,
  timeSaved: (timeRange?: TimeRange) =>
    [...ceoDashboardKeys.all, "time-saved", timeRange] as const,
  routingBreakdown: (options?: { projectId?: string; timeRange?: TimeRange }) =>
    [...ceoDashboardKeys.all, "routing-breakdown", options] as const,
  pendingDecisions: (options?: { projectId?: string; limit?: number }) =>
    [...ceoDashboardKeys.all, "pending-decisions", options] as const,
  weeklySummary: () => [...ceoDashboardKeys.all, "weekly-summary"] as const,
  timeSavedTrend: () => [...ceoDashboardKeys.all, "time-saved-trend"] as const,
  vibecodingTrend: (projectId?: string) =>
    [...ceoDashboardKeys.all, "vibecoding-trend", projectId] as const,
  topRejections: (options?: { projectId?: string; timeRange?: TimeRange }) =>
    [...ceoDashboardKeys.all, "top-rejections", options] as const,
  overrides: () => [...ceoDashboardKeys.all, "overrides"] as const,
  systemHealth: () => [...ceoDashboardKeys.all, "system-health"] as const,
  health: () => [...ceoDashboardKeys.all, "health"] as const,
};

/**
 * Hook to get complete CEO dashboard summary
 */
export function useCEODashboardSummary(options?: {
  projectId?: string;
  timeRange?: TimeRange;
}) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: ceoDashboardKeys.summary(options),
    queryFn: () => getCEODashboardSummary(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 60 * 1000, // Auto-refresh every minute
  });
}

/**
 * Hook to get CEO time saved metrics
 */
export function useCEOTimeSaved(timeRange: TimeRange = "this_week") {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: ceoDashboardKeys.timeSaved(timeRange),
    queryFn: () => getCEOTimeSaved(timeRange),
    enabled: isAuthenticated && !authLoading,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to get PR routing breakdown
 */
export function useCEORoutingBreakdown(options?: {
  projectId?: string;
  timeRange?: TimeRange;
}) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: ceoDashboardKeys.routingBreakdown(options),
    queryFn: () => getCEORoutingBreakdown(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 60 * 1000,
  });
}

/**
 * Hook to get pending CEO decisions queue
 */
export function useCEOPendingDecisions(options?: {
  projectId?: string;
  limit?: number;
}) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: ceoDashboardKeys.pendingDecisions(options),
    queryFn: () => getCEOPendingDecisions(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 30 * 1000, // 30 seconds - refresh frequently
    refetchInterval: 30 * 1000, // Auto-refresh every 30 seconds
  });
}

/**
 * Hook to get weekly governance summary
 */
export function useCEOWeeklySummary() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: ceoDashboardKeys.weeklySummary(),
    queryFn: getCEOWeeklySummary,
    enabled: isAuthenticated && !authLoading,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

/**
 * Hook to get time saved trend (8 weeks)
 */
export function useCEOTimeSavedTrend() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: ceoDashboardKeys.timeSavedTrend(),
    queryFn: getCEOTimeSavedTrend,
    enabled: isAuthenticated && !authLoading,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

/**
 * Hook to get vibecoding index trend (7 days)
 */
export function useCEOVibecodingTrend(projectId?: string) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: ceoDashboardKeys.vibecodingTrend(projectId),
    queryFn: () => getCEOVibecodingTrend(projectId),
    enabled: isAuthenticated && !authLoading,
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Hook to get top rejection reasons
 */
export function useCEOTopRejections(options?: {
  projectId?: string;
  timeRange?: TimeRange;
}) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: ceoDashboardKeys.topRejections(options),
    queryFn: () => getCEOTopRejections(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Hook to get CEO overrides this week
 */
export function useCEOOverrides() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: ceoDashboardKeys.overrides(),
    queryFn: getCEOOverrides,
    enabled: isAuthenticated && !authLoading,
    staleTime: 60 * 1000,
  });
}

/**
 * Hook to get system health snapshot
 */
export function useCEOSystemHealth() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: ceoDashboardKeys.systemHealth(),
    queryFn: getCEOSystemHealth,
    enabled: isAuthenticated && !authLoading,
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 30 * 1000, // Auto-refresh
  });
}

/**
 * Hook to get CEO dashboard health
 */
export function useCEODashboardHealth() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: ceoDashboardKeys.health(),
    queryFn: getCEODashboardHealth,
    enabled: isAuthenticated && !authLoading,
    staleTime: 60 * 1000,
  });
}

/**
 * Mutation hook to resolve a pending decision
 */
export function useResolveCEODecision() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      submissionId,
      request,
    }: {
      submissionId: string;
      request: ResolveDecisionRequest;
    }) => resolveCEODecision(submissionId, request),
    onSuccess: () => {
      // Invalidate pending decisions and summary
      queryClient.invalidateQueries({ queryKey: ceoDashboardKeys.all });
    },
  });
}

/**
 * Mutation hook to record a CEO override
 */
export function useRecordCEOOverride() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      submissionId,
      request,
    }: {
      submissionId: string;
      request: RecordOverrideRequest;
    }) => recordCEOOverride(submissionId, request),
    onSuccess: () => {
      // Invalidate overrides and summary
      queryClient.invalidateQueries({ queryKey: ceoDashboardKeys.all });
    },
  });
}
