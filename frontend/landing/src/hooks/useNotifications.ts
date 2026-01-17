/**
 * Notifications TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useNotifications
 * @description React Query hooks for Notifications API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 69 - CTO Go-Live Requirements
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getNotifications,
  markNotificationRead,
  markAllNotificationsRead,
  getNotificationSettings,
  updateNotificationSettings,
  type Notification,
  type NotificationListResponse,
  type NotificationSettings,
  type NotificationListOptions,
} from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";

// Query keys for cache management
export const notificationKeys = {
  all: ["notifications"] as const,
  lists: () => [...notificationKeys.all, "list"] as const,
  list: (options?: NotificationListOptions) =>
    [...notificationKeys.lists(), options] as const,
  settings: () => [...notificationKeys.all, "settings"] as const,
  unreadCount: () => [...notificationKeys.all, "unread"] as const,
};

/**
 * Hook to fetch list of notifications
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function useNotifications(options?: NotificationListOptions) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: notificationKeys.list(options),
    queryFn: () => getNotifications(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 30 * 1000, // 30 seconds - notifications should refresh frequently
    refetchInterval: 60 * 1000, // Auto-refresh every minute
  });
}

/**
 * Hook to fetch unread notification count
 * Sprint 69: Lightweight query for notification badge
 */
export function useUnreadNotificationCount() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: notificationKeys.unreadCount(),
    queryFn: async () => {
      const response = await getNotifications({ unread_only: true, page_size: 1 });
      return response.unread_count;
    },
    enabled: isAuthenticated && !authLoading,
    staleTime: 30 * 1000,
    refetchInterval: 60 * 1000,
  });
}

/**
 * Hook to fetch notification settings
 * Sprint 69: User notification preferences
 */
export function useNotificationSettings() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: notificationKeys.settings(),
    queryFn: getNotificationSettings,
    enabled: isAuthenticated && !authLoading,
    staleTime: 5 * 60 * 1000, // 5 minutes - settings don't change often
  });
}

/**
 * Hook to mark a single notification as read
 * Sprint 69: Optimistic update for better UX
 */
export function useMarkNotificationRead() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (notificationId: string) => markNotificationRead(notificationId),
    onSuccess: () => {
      // Invalidate notifications list to refetch
      queryClient.invalidateQueries({ queryKey: notificationKeys.lists() });
      queryClient.invalidateQueries({ queryKey: notificationKeys.unreadCount() });
    },
  });
}

/**
 * Hook to mark all notifications as read
 * Sprint 69: Bulk operation for clearing notifications
 */
export function useMarkAllNotificationsRead() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: markAllNotificationsRead,
    onSuccess: () => {
      // Invalidate all notification queries
      queryClient.invalidateQueries({ queryKey: notificationKeys.all });
    },
  });
}

/**
 * Hook to update notification settings
 * Sprint 69: Save user preferences
 */
export function useUpdateNotificationSettings() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (settings: Partial<NotificationSettings>) =>
      updateNotificationSettings(settings),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: notificationKeys.settings() });
    },
  });
}

/**
 * Hook to invalidate notifications cache
 */
export function useInvalidateNotifications() {
  const queryClient = useQueryClient();

  return () => {
    queryClient.invalidateQueries({ queryKey: notificationKeys.all });
  };
}

// Export types for use in components
export type {
  Notification,
  NotificationListResponse,
  NotificationSettings,
  NotificationListOptions,
};
