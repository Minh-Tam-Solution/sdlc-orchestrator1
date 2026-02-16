/**
 * SAST (Static Application Security Testing) TanStack Query Hooks
 * SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useSAST
 * @description React Query hooks for SAST Scanning API
 * @sdlc SDLC 6.0.6 Universal Framework
 * @status Sprint 69 - CTO Go-Live Requirements
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getSASTScans,
  triggerSASTScan,
  getSASTFindings,
  getSASTScanDetails,
  type SASTScan,
  type SASTFinding,
  type SASTScanListResponse,
} from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";

// Query keys for cache management
export const sastKeys = {
  all: ["sast"] as const,
  scans: () => [...sastKeys.all, "scans"] as const,
  scanList: (projectId: string, options?: { page?: number; page_size?: number }) =>
    [...sastKeys.scans(), projectId, options] as const,
  scanDetail: (scanId: string) => [...sastKeys.scans(), "detail", scanId] as const,
  findings: () => [...sastKeys.all, "findings"] as const,
  findingList: (scanId: string) => [...sastKeys.findings(), scanId] as const,
};

/**
 * Hook to fetch SAST scans for a project
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function useSASTScans(
  projectId: string | undefined,
  options?: { page?: number; page_size?: number }
) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: sastKeys.scanList(projectId || "", options),
    queryFn: () => {
      if (!projectId) {
        throw new Error("Missing project ID");
      }
      return getSASTScans(projectId, options);
    },
    enabled: isAuthenticated && !authLoading && !!projectId,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to fetch details of a specific SAST scan
 * Sprint 69: Detailed scan information
 */
export function useSASTScanDetails(scanId: string | undefined) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: sastKeys.scanDetail(scanId || ""),
    queryFn: () => {
      if (!scanId) {
        throw new Error("Missing scan ID");
      }
      return getSASTScanDetails(scanId);
    },
    enabled: isAuthenticated && !authLoading && !!scanId,
    staleTime: 30 * 1000, // 30 seconds - check for scan completion
    refetchInterval: (query) => {
      // Auto-refresh if scan is still running
      const scan = query.state.data;
      if (scan && (scan.status === "pending" || scan.status === "running")) {
        return 5000; // Refresh every 5 seconds while running
      }
      return false;
    },
  });
}

/**
 * Hook to fetch security findings for a SAST scan
 * Sprint 69: Vulnerability details
 */
export function useSASTFindings(scanId: string | undefined) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: sastKeys.findingList(scanId || ""),
    queryFn: () => {
      if (!scanId) {
        throw new Error("Missing scan ID");
      }
      return getSASTFindings(scanId);
    },
    enabled: isAuthenticated && !authLoading && !!scanId,
    staleTime: 5 * 60 * 1000, // 5 minutes - findings don't change after scan
  });
}

/**
 * Hook to trigger a new SAST scan
 * Sprint 69: On-demand security scanning
 */
export function useTriggerSASTScan() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (projectId: string) => triggerSASTScan(projectId),
    onSuccess: (_, projectId) => {
      // Invalidate scans list for the project
      queryClient.invalidateQueries({
        queryKey: sastKeys.scanList(projectId),
      });
    },
  });
}

/**
 * Hook to invalidate SAST cache
 */
export function useInvalidateSAST() {
  const queryClient = useQueryClient();

  return (projectId?: string) => {
    if (projectId) {
      queryClient.invalidateQueries({
        queryKey: sastKeys.scanList(projectId),
      });
    } else {
      queryClient.invalidateQueries({ queryKey: sastKeys.all });
    }
  };
}

// Export types for use in components
export type { SASTScan, SASTFinding, SASTScanListResponse };
