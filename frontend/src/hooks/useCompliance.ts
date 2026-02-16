/**
 * Compliance TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useCompliance
 * @description React Query hooks for Compliance Scanning API
 * @sdlc SDLC 6.0.6 Universal Framework
 * @status Sprint 69 - CTO Go-Live Requirements
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getComplianceScans,
  triggerComplianceScan,
  getComplianceFindings,
  type ComplianceScan,
  type ComplianceFinding,
  type ComplianceScanListResponse,
} from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";

// Query keys for cache management
export const complianceKeys = {
  all: ["compliance"] as const,
  scans: () => [...complianceKeys.all, "scans"] as const,
  scanList: (projectId: string, options?: { page?: number; page_size?: number }) =>
    [...complianceKeys.scans(), projectId, options] as const,
  findings: () => [...complianceKeys.all, "findings"] as const,
  findingList: (scanId: string) => [...complianceKeys.findings(), scanId] as const,
};

/**
 * Hook to fetch compliance scans for a project
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function useComplianceScans(
  projectId: string | undefined,
  options?: { page?: number; page_size?: number }
) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: complianceKeys.scanList(projectId || "", options),
    queryFn: () => {
      if (!projectId) {
        throw new Error("Missing project ID");
      }
      return getComplianceScans(projectId, options);
    },
    enabled: isAuthenticated && !authLoading && !!projectId,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to fetch findings for a specific scan
 * Sprint 69: Detailed scan results
 */
export function useComplianceFindings(scanId: string | undefined) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: complianceKeys.findingList(scanId || ""),
    queryFn: () => {
      if (!scanId) {
        throw new Error("Missing scan ID");
      }
      return getComplianceFindings(scanId);
    },
    enabled: isAuthenticated && !authLoading && !!scanId,
    staleTime: 5 * 60 * 1000, // 5 minutes - findings don't change after scan
  });
}

/**
 * Hook to trigger a new compliance scan
 * Sprint 69: On-demand scanning
 */
export function useTriggerComplianceScan() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      projectId,
      scanType = "full",
    }: {
      projectId: string;
      scanType?: string;
    }) => triggerComplianceScan(projectId, scanType),
    onSuccess: (_, variables) => {
      // Invalidate scans list for the project
      queryClient.invalidateQueries({
        queryKey: complianceKeys.scanList(variables.projectId),
      });
    },
  });
}

/**
 * Hook to invalidate compliance cache
 */
export function useInvalidateCompliance() {
  const queryClient = useQueryClient();

  return (projectId?: string) => {
    if (projectId) {
      queryClient.invalidateQueries({
        queryKey: complianceKeys.scanList(projectId),
      });
    } else {
      queryClient.invalidateQueries({ queryKey: complianceKeys.all });
    }
  };
}

// Export types for use in components
export type { ComplianceScan, ComplianceFinding, ComplianceScanListResponse };
