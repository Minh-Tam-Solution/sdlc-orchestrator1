/**
 * Organizations TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/src/hooks/useOrganizations
 * @description React Query hooks for Organizations API
 * @sdlc SDLC 5.1.3 Framework - Sprint 84 (Teams & Organizations UI)
 * @status Sprint 84 - CTO APPROVED (January 20, 2026)
 * @see backend/app/api/routes/organizations.py (5 endpoints)
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getOrganizations,
  getOrganization,
  createOrganization,
  updateOrganization,
  getOrganizationStats,
  type Organization,
  type OrganizationCreate,
  type OrganizationUpdate,
  type OrganizationListResponse,
  type OrganizationListParams,
  type OrganizationStatistics,
} from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";
import { teamKeys } from "./useTeams";

// =============================================================================
// Query Keys for Cache Management
// =============================================================================

export const organizationKeys = {
  all: ["organizations"] as const,
  lists: () => [...organizationKeys.all, "list"] as const,
  list: (params?: OrganizationListParams) => [...organizationKeys.lists(), params] as const,
  details: () => [...organizationKeys.all, "detail"] as const,
  detail: (id: string) => [...organizationKeys.details(), id] as const,
  stats: (id: string) => [...organizationKeys.detail(id), "stats"] as const,
};

// =============================================================================
// Organization Query Hooks
// =============================================================================

/**
 * Hook to fetch list of organizations user has access to
 * Sprint 84: GET /organizations - Paginated list
 */
export function useOrganizations(params?: OrganizationListParams) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: organizationKeys.list(params),
    queryFn: () => getOrganizations(params),
    enabled: isAuthenticated && !authLoading,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to fetch a single organization by ID
 * Sprint 84: GET /organizations/{org_id}
 */
export function useOrganization(orgId: string | undefined) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: organizationKeys.detail(orgId || ""),
    queryFn: () => {
      if (!orgId) {
        throw new Error("Missing organization ID");
      }
      return getOrganization(orgId);
    },
    enabled: isAuthenticated && !authLoading && !!orgId,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to fetch organization statistics
 * Sprint 84: GET /organizations/{org_id}/stats
 */
export function useOrganizationStats(orgId: string | undefined) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: organizationKeys.stats(orgId || ""),
    queryFn: () => {
      if (!orgId) {
        throw new Error("Missing organization ID");
      }
      return getOrganizationStats(orgId);
    },
    enabled: isAuthenticated && !authLoading && !!orgId,
    staleTime: 30 * 1000, // 30 seconds (stats change more frequently)
  });
}

// =============================================================================
// Organization Mutation Hooks
// =============================================================================

/**
 * Hook to create a new organization
 * Sprint 84: POST /organizations
 */
export function useCreateOrganization() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: OrganizationCreate) => createOrganization(data),
    onSuccess: () => {
      // Invalidate organizations list to refetch
      queryClient.invalidateQueries({ queryKey: organizationKeys.all });
    },
  });
}

/**
 * Hook to update an organization
 * Sprint 84: PATCH /organizations/{org_id} - Member required
 */
export function useUpdateOrganization(orgId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: OrganizationUpdate) => updateOrganization(orgId, data),
    onSuccess: (updatedOrg) => {
      // Update cache with new organization data
      queryClient.setQueryData(organizationKeys.detail(orgId), updatedOrg);
      // Invalidate lists to reflect changes
      queryClient.invalidateQueries({ queryKey: organizationKeys.lists() });
      // Also invalidate teams since they belong to organization
      queryClient.invalidateQueries({ queryKey: teamKeys.all });
    },
  });
}

// =============================================================================
// Cache Invalidation Utilities
// =============================================================================

/**
 * Hook to invalidate all organizations cache
 */
export function useInvalidateOrganizations() {
  const queryClient = useQueryClient();

  return () => {
    queryClient.invalidateQueries({ queryKey: organizationKeys.all });
  };
}

/**
 * Hook to invalidate specific organization cache
 */
export function useInvalidateOrganization(orgId: string) {
  const queryClient = useQueryClient();

  return () => {
    queryClient.invalidateQueries({ queryKey: organizationKeys.detail(orgId) });
    queryClient.invalidateQueries({ queryKey: organizationKeys.stats(orgId) });
    // Also invalidate teams filtered by this organization
    queryClient.invalidateQueries({
      queryKey: teamKeys.list({ organization_id: orgId }),
    });
  };
}

// =============================================================================
// Prefetch Utilities
// =============================================================================

/**
 * Prefetch organization data for navigation optimization
 */
export function usePrefetchOrganization() {
  const queryClient = useQueryClient();

  return (orgId: string) => {
    queryClient.prefetchQuery({
      queryKey: organizationKeys.detail(orgId),
      queryFn: () => getOrganization(orgId),
      staleTime: 60 * 1000,
    });
  };
}

/**
 * Prefetch organization stats for navigation optimization
 */
export function usePrefetchOrganizationStats() {
  const queryClient = useQueryClient();

  return (orgId: string) => {
    queryClient.prefetchQuery({
      queryKey: organizationKeys.stats(orgId),
      queryFn: () => getOrganizationStats(orgId),
      staleTime: 30 * 1000,
    });
  };
}

// =============================================================================
// Combined Hooks
// =============================================================================

/**
 * Hook to get organization with its teams
 * Useful for organization detail page
 */
export function useOrganizationWithTeams(orgId: string | undefined) {
  const orgQuery = useOrganization(orgId);
  const statsQuery = useOrganizationStats(orgId);

  return {
    organization: orgQuery.data,
    stats: statsQuery.data,
    isLoading: orgQuery.isLoading || statsQuery.isLoading,
    isError: orgQuery.isError || statsQuery.isError,
    error: orgQuery.error || statsQuery.error,
  };
}

// =============================================================================
// Type Exports
// =============================================================================

export type {
  Organization,
  OrganizationCreate,
  OrganizationUpdate,
  OrganizationListResponse,
  OrganizationListParams,
  OrganizationStatistics,
};
