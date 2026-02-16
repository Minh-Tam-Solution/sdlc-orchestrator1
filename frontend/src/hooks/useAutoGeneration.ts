/**
 * =========================================================================
 * Auto-Generation React Query Hooks
 * SDLC Orchestrator - Sprint 113 (Governance UI - Auto-Generation)
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Framework: SDLC 6.0.6 Quality Assurance System
 * ADR Reference: ADR-041
 *
 * Purpose: React Query hooks for auto-generation API operations
 * =========================================================================
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "./useAuth";
import {
  generateIntentSkeleton,
  suggestOwnership,
  suggestOwnershipBatch,
  attachContext,
  preFillAttestation,
  submitAttestation,
  getAttestation,
  getAutoGenerationMetrics,
  getRecentAutoGenerations,
  getAutoGenerationHealth,
} from "@/lib/api";
import type {
  GenerateIntentRequest,
  SuggestOwnershipRequest,
  BatchOwnershipRequest,
  AttachContextRequest,
  PreFillAttestationRequest,
  SubmitAttestationRequest,
} from "@/lib/types/auto-generation";

// =============================================================================
// Query Key Factory
// =============================================================================

export const autoGenerationKeys = {
  all: ["auto-generation"] as const,
  metrics: (options?: { projectId?: string; timeRange?: string }) =>
    [...autoGenerationKeys.all, "metrics", options] as const,
  recent: (options?: { projectId?: string; limit?: number }) =>
    [...autoGenerationKeys.all, "recent", options] as const,
  health: () => [...autoGenerationKeys.all, "health"] as const,
  attestation: (id: string) =>
    [...autoGenerationKeys.all, "attestation", id] as const,
};

// =============================================================================
// Query Hooks
// =============================================================================

/**
 * Hook to get auto-generation usage metrics
 */
export function useAutoGenerationMetrics(options?: {
  projectId?: string;
  timeRange?: string;
}) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: autoGenerationKeys.metrics(options),
    queryFn: () => getAutoGenerationMetrics(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 60 * 1000, // 1 minute
    refetchInterval: 5 * 60 * 1000, // Auto-refresh every 5 minutes
  });
}

/**
 * Hook to get recent auto-generation activity
 */
export function useRecentAutoGenerations(options?: {
  projectId?: string;
  limit?: number;
}) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: autoGenerationKeys.recent(options),
    queryFn: () => getRecentAutoGenerations(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 60 * 1000, // Auto-refresh every minute
  });
}

/**
 * Hook to get auto-generation health status
 */
export function useAutoGenerationHealth() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: autoGenerationKeys.health(),
    queryFn: getAutoGenerationHealth,
    enabled: isAuthenticated && !authLoading,
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 30 * 1000, // Auto-refresh every 30 seconds
  });
}

/**
 * Hook to get attestation by ID
 */
export function useAttestation(attestationId: string) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: autoGenerationKeys.attestation(attestationId),
    queryFn: () => getAttestation(attestationId),
    enabled: isAuthenticated && !authLoading && !!attestationId,
    staleTime: 60 * 1000,
  });
}

// =============================================================================
// Mutation Hooks
// =============================================================================

/**
 * Hook to generate intent skeleton from task
 *
 * Time saved: ~15 min → <1 min
 */
export function useGenerateIntent() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: GenerateIntentRequest) =>
      generateIntentSkeleton(request),
    onSuccess: () => {
      // Invalidate metrics and recent activity
      queryClient.invalidateQueries({
        queryKey: autoGenerationKeys.metrics(),
      });
      queryClient.invalidateQueries({
        queryKey: autoGenerationKeys.recent(),
      });
    },
  });
}

/**
 * Hook to suggest ownership for a file
 *
 * Time saved: ~2 min → <30 sec
 */
export function useSuggestOwnership() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: SuggestOwnershipRequest) => suggestOwnership(request),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: autoGenerationKeys.metrics(),
      });
      queryClient.invalidateQueries({
        queryKey: autoGenerationKeys.recent(),
      });
    },
  });
}

/**
 * Hook to suggest ownership for multiple files (batch)
 */
export function useSuggestOwnershipBatch() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: BatchOwnershipRequest) =>
      suggestOwnershipBatch(request),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: autoGenerationKeys.metrics(),
      });
      queryClient.invalidateQueries({
        queryKey: autoGenerationKeys.recent(),
      });
    },
  });
}

/**
 * Hook to auto-attach context (ADRs, specs) to PR
 *
 * Time saved: ~5 min → automatic
 */
export function useAttachContext() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: AttachContextRequest) => attachContext(request),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: autoGenerationKeys.metrics(),
      });
      queryClient.invalidateQueries({
        queryKey: autoGenerationKeys.recent(),
      });
    },
  });
}

/**
 * Hook to pre-fill AI attestation form
 *
 * Time saved: ~8 min → ~2 min (human confirmation only)
 */
export function usePreFillAttestation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: PreFillAttestationRequest) =>
      preFillAttestation(request),
    onSuccess: (data) => {
      // Pre-populate attestation cache
      queryClient.setQueryData(
        autoGenerationKeys.attestation(data.attestation.id),
        data.attestation
      );
      queryClient.invalidateQueries({
        queryKey: autoGenerationKeys.metrics(),
      });
      queryClient.invalidateQueries({
        queryKey: autoGenerationKeys.recent(),
      });
    },
  });
}

/**
 * Hook to submit completed attestation
 */
export function useSubmitAttestation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: SubmitAttestationRequest) =>
      submitAttestation(request),
    onSuccess: (data) => {
      // Update attestation cache
      queryClient.setQueryData(
        autoGenerationKeys.attestation(data.id),
        data
      );
      queryClient.invalidateQueries({
        queryKey: autoGenerationKeys.metrics(),
      });
    },
  });
}

// =============================================================================
// Utility Hooks
// =============================================================================

/**
 * Hook to get combined auto-generation state
 */
export function useAutoGenerationState() {
  const metrics = useAutoGenerationMetrics();
  const health = useAutoGenerationHealth();
  const recent = useRecentAutoGenerations({ limit: 5 });

  return {
    isLoading: metrics.isLoading || health.isLoading || recent.isLoading,
    isError: metrics.isError || health.isError || recent.isError,
    metrics: metrics.data,
    health: health.data,
    recent: recent.data,
    refetch: () => {
      metrics.refetch();
      health.refetch();
      recent.refetch();
    },
  };
}
