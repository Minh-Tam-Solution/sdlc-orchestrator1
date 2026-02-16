/**
 * =========================================================================
 * Kill Switch & Governance Mode React Query Hooks
 * SDLC Orchestrator - Sprint 113 (Governance UI - Kill Switch Admin)
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Framework: SDLC 6.0.6 Quality Assurance System
 * ADR Reference: ADR-041
 *
 * Purpose: React Query hooks for kill switch and governance mode operations
 * =========================================================================
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "./useAuth";
import {
  getGovernanceMode,
  setGovernanceMode,
  checkKillSwitch,
  triggerRollback,
  getBreakGlassRequests,
  createBreakGlass,
  resolveBreakGlass,
  getModeHistory,
  getGovernanceAuditLog,
  getKillSwitchDashboard,
} from "@/lib/api";
import type {
  SetGovernanceModeRequest,
  TriggerRollbackRequest,
  CreateBreakGlassRequest,
  ResolveBreakGlassRequest,
  GetAuditLogRequest,
} from "@/lib/types/kill-switch";

// =============================================================================
// Query Key Factory
// =============================================================================

export const killSwitchKeys = {
  all: ["kill-switch"] as const,
  mode: () => [...killSwitchKeys.all, "mode"] as const,
  check: () => [...killSwitchKeys.all, "check"] as const,
  breakGlass: (options?: { status?: string; limit?: number }) =>
    [...killSwitchKeys.all, "break-glass", options] as const,
  modeHistory: (options?: { limit?: number }) =>
    [...killSwitchKeys.all, "mode-history", options] as const,
  auditLog: (options?: GetAuditLogRequest) =>
    [...killSwitchKeys.all, "audit-log", options] as const,
  dashboard: () => [...killSwitchKeys.all, "dashboard"] as const,
};

// =============================================================================
// Query Hooks
// =============================================================================

/**
 * Hook to get current governance mode
 */
export function useGovernanceMode() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: killSwitchKeys.mode(),
    queryFn: getGovernanceMode,
    enabled: isAuthenticated && !authLoading,
    staleTime: 10 * 1000, // 10 seconds - mode can change frequently
    refetchInterval: 30 * 1000, // Auto-refresh every 30 seconds
  });
}

/**
 * Hook to check kill switch criteria
 */
export function useKillSwitchCheck() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: killSwitchKeys.check(),
    queryFn: checkKillSwitch,
    enabled: isAuthenticated && !authLoading,
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 60 * 1000, // Auto-refresh every minute
  });
}

/**
 * Hook to get break glass requests
 */
export function useBreakGlassRequests(options?: {
  status?: string;
  limit?: number;
}) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: killSwitchKeys.breakGlass(options),
    queryFn: () => getBreakGlassRequests(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 30 * 1000, // Auto-refresh for pending requests
  });
}

/**
 * Hook to get governance mode history
 */
export function useModeHistory(options?: { limit?: number }) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: killSwitchKeys.modeHistory(options),
    queryFn: () => getModeHistory(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to get governance audit log
 */
export function useGovernanceAuditLog(options?: GetAuditLogRequest) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: killSwitchKeys.auditLog(options),
    queryFn: () => getGovernanceAuditLog(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 60 * 1000, // Auto-refresh every minute
  });
}

/**
 * Hook to get kill switch admin dashboard data
 */
export function useKillSwitchDashboard() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: killSwitchKeys.dashboard(),
    queryFn: getKillSwitchDashboard,
    enabled: isAuthenticated && !authLoading,
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 30 * 1000, // Auto-refresh every 30 seconds
  });
}

// =============================================================================
// Mutation Hooks
// =============================================================================

/**
 * Hook to set governance mode
 *
 * Requires: CTO or CEO role
 */
export function useSetGovernanceMode() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: SetGovernanceModeRequest) =>
      setGovernanceMode(request),
    onSuccess: () => {
      // Invalidate all kill switch related queries
      queryClient.invalidateQueries({ queryKey: killSwitchKeys.all });
    },
  });
}

/**
 * Hook to trigger governance rollback
 *
 * Requires: CTO or CEO role
 */
export function useTriggerRollback() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: TriggerRollbackRequest) => triggerRollback(request),
    onSuccess: () => {
      // Invalidate all kill switch related queries
      queryClient.invalidateQueries({ queryKey: killSwitchKeys.all });
    },
  });
}

/**
 * Hook to create break glass request
 */
export function useCreateBreakGlass() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: CreateBreakGlassRequest) => createBreakGlass(request),
    onSuccess: () => {
      // Invalidate break glass and audit log
      queryClient.invalidateQueries({
        queryKey: killSwitchKeys.breakGlass(),
      });
      queryClient.invalidateQueries({
        queryKey: killSwitchKeys.auditLog(),
      });
      queryClient.invalidateQueries({
        queryKey: killSwitchKeys.dashboard(),
      });
    },
  });
}

/**
 * Hook to approve or reject break glass request
 */
export function useResolveBreakGlass() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      requestId,
      request,
    }: {
      requestId: string;
      request: ResolveBreakGlassRequest;
    }) => resolveBreakGlass(requestId, request),
    onSuccess: () => {
      // Invalidate all kill switch related queries
      queryClient.invalidateQueries({ queryKey: killSwitchKeys.all });
    },
  });
}

// =============================================================================
// Utility Hooks
// =============================================================================

/**
 * Hook to get combined kill switch state for dashboard
 */
export function useKillSwitchState() {
  const mode = useGovernanceMode();
  const check = useKillSwitchCheck();
  const breakGlass = useBreakGlassRequests({ status: "pending", limit: 5 });
  const history = useModeHistory({ limit: 5 });

  return {
    isLoading:
      mode.isLoading ||
      check.isLoading ||
      breakGlass.isLoading ||
      history.isLoading,
    isError:
      mode.isError || check.isError || breakGlass.isError || history.isError,
    currentMode: mode.data,
    killSwitchStatus: check.data,
    pendingBreakGlass: breakGlass.data,
    recentHistory: history.data,
    refetch: () => {
      mode.refetch();
      check.refetch();
      breakGlass.refetch();
      history.refetch();
    },
  };
}

/**
 * Hook to check if user can change governance mode
 *
 * Returns true if user has CTO or CEO role
 */
export function useCanChangeMode() {
  const { user } = useAuth();

  if (!user) return false;

  // Check for CTO or CEO role
  const allowedRoles = ["cto", "ceo", "admin"];
  return user.roles?.some((role) =>
    allowedRoles.includes(role.toLowerCase())
  ) || user.is_platform_admin;
}

/**
 * Hook to check if user can approve break glass
 *
 * Returns authorization tier if user can approve, null otherwise
 */
export function useBreakGlassAuthorization() {
  const { user } = useAuth();

  if (!user) return null;

  // Check roles in order of tier
  if (user.roles?.some((r) => r.toLowerCase() === "ceo") || user.is_platform_admin) {
    return "ceo" as const;
  }
  if (user.roles?.some((r) => r.toLowerCase() === "cto")) {
    return "cto" as const;
  }
  if (user.roles?.some((r) => r.toLowerCase() === "tech_lead")) {
    return "tech_lead" as const;
  }

  return null;
}
