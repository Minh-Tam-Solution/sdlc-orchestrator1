/**
 * System Settings Hooks - SDLC Orchestrator
 *
 * @module frontend/src/hooks/useSystemSettings
 * @description TanStack Query hooks for System Settings Admin UI
 * @sdlc SDLC 6.0.6 Framework - Sprint 86 Phase 2 (ADR-027)
 * @status Sprint 86 - System Settings Admin UI
 */

"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getSystemSettings,
  getSystemSetting,
  updateSystemSetting,
  rollbackSystemSetting,
} from "@/lib/api";
import type {
  SystemSettingsListResponse,
  SystemSettingItem,
  SystemSettingUpdate,
  SettingCategory,
} from "@/lib/types/system-settings";

// =========================================================================
// Query Keys
// =========================================================================

export const systemSettingsKeys = {
  all: ["system-settings"] as const,
  list: () => [...systemSettingsKeys.all, "list"] as const,
  detail: (key: string) => [...systemSettingsKeys.all, "detail", key] as const,
  category: (category: SettingCategory) =>
    [...systemSettingsKeys.all, "category", category] as const,
};

// =========================================================================
// Query Hooks
// =========================================================================

/**
 * Fetch all system settings grouped by category
 */
export function useSystemSettings() {
  return useQuery<SystemSettingsListResponse, Error>({
    queryKey: systemSettingsKeys.list(),
    queryFn: getSystemSettings,
    staleTime: 5 * 60 * 1000, // 5 minutes (matches Redis cache TTL)
    gcTime: 10 * 60 * 1000, // 10 minutes
  });
}

/**
 * Fetch a specific system setting by key
 */
export function useSystemSetting(key: string) {
  return useQuery<SystemSettingItem, Error>({
    queryKey: systemSettingsKeys.detail(key),
    queryFn: () => getSystemSetting(key),
    enabled: Boolean(key),
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
  });
}

// =========================================================================
// Mutation Hooks
// =========================================================================

/**
 * Update a system setting value
 */
export function useUpdateSystemSetting() {
  const queryClient = useQueryClient();

  return useMutation<
    SystemSettingItem,
    Error,
    { key: string; data: SystemSettingUpdate }
  >({
    mutationFn: ({ key, data }) => updateSystemSetting(key, data),
    onSuccess: (updatedSetting) => {
      // Update the specific setting in cache
      queryClient.setQueryData(
        systemSettingsKeys.detail(updatedSetting.key),
        updatedSetting
      );

      // Invalidate list to refresh all settings
      queryClient.invalidateQueries({
        queryKey: systemSettingsKeys.list(),
      });
    },
  });
}

/**
 * Rollback a system setting to previous value
 */
export function useRollbackSystemSetting() {
  const queryClient = useQueryClient();

  return useMutation<SystemSettingItem, Error, string>({
    mutationFn: (key) => rollbackSystemSetting(key),
    onSuccess: (updatedSetting) => {
      // Update the specific setting in cache
      queryClient.setQueryData(
        systemSettingsKeys.detail(updatedSetting.key),
        updatedSetting
      );

      // Invalidate list to refresh all settings
      queryClient.invalidateQueries({
        queryKey: systemSettingsKeys.list(),
      });
    },
  });
}

// =========================================================================
// Combined Hooks
// =========================================================================

/**
 * Combined hook for System Settings admin page
 */
export function useSystemSettingsAdmin() {
  const settingsQuery = useSystemSettings();
  const updateMutation = useUpdateSystemSetting();
  const rollbackMutation = useRollbackSystemSetting();

  return {
    // Data
    settings: settingsQuery.data,
    securitySettings: settingsQuery.data?.security ?? [],
    limitsSettings: settingsQuery.data?.limits ?? [],
    featureSettings: settingsQuery.data?.features ?? [],
    notificationSettings: settingsQuery.data?.notifications ?? [],
    generalSettings: settingsQuery.data?.general ?? [],
    aiSettings: settingsQuery.data?.ai ?? [],

    // Loading states
    isLoading: settingsQuery.isLoading,
    isUpdating: updateMutation.isPending,
    isRollingBack: rollbackMutation.isPending,

    // Error states
    error: settingsQuery.error,
    updateError: updateMutation.error,
    rollbackError: rollbackMutation.error,

    // Actions
    updateSetting: updateMutation.mutate,
    updateSettingAsync: updateMutation.mutateAsync,
    rollbackSetting: rollbackMutation.mutate,
    rollbackSettingAsync: rollbackMutation.mutateAsync,

    // Refetch
    refetch: settingsQuery.refetch,
  };
}

/**
 * Hook for security settings section
 */
export function useSecuritySettings() {
  const { securitySettings, isLoading, error, updateSetting, isUpdating } =
    useSystemSettingsAdmin();

  return {
    settings: securitySettings,
    isLoading,
    error,
    updateSetting,
    isUpdating,
  };
}

/**
 * Hook for limits settings section
 */
export function useLimitsSettings() {
  const { limitsSettings, isLoading, error, updateSetting, isUpdating } =
    useSystemSettingsAdmin();

  return {
    settings: limitsSettings,
    isLoading,
    error,
    updateSetting,
    isUpdating,
  };
}

/**
 * Hook for feature flags section
 */
export function useFeatureSettings() {
  const { featureSettings, isLoading, error, updateSetting, isUpdating } =
    useSystemSettingsAdmin();

  return {
    settings: featureSettings,
    isLoading,
    error,
    updateSetting,
    isUpdating,
  };
}

/**
 * Hook for AI settings section
 */
export function useAISettings() {
  const { aiSettings, isLoading, error, updateSetting, isUpdating } =
    useSystemSettingsAdmin();

  return {
    settings: aiSettings,
    isLoading,
    error,
    updateSetting,
    isUpdating,
  };
}
