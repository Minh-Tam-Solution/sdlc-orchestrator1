/**
 * AI Council TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useCouncil
 * @description React Query hooks for AI Council API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 69 - CTO Go-Live Requirements
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getCouncilSessions,
  createCouncilSession,
  getCouncilMessages,
  sendCouncilMessage,
  type CouncilSession,
  type CouncilMessage,
  type CouncilSessionListResponse,
} from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";

// Query keys for cache management
export const councilKeys = {
  all: ["council"] as const,
  sessions: () => [...councilKeys.all, "sessions"] as const,
  sessionList: (projectId: string, options?: { page?: number; page_size?: number }) =>
    [...councilKeys.sessions(), projectId, options] as const,
  messages: () => [...councilKeys.all, "messages"] as const,
  messageList: (sessionId: string) => [...councilKeys.messages(), sessionId] as const,
};

/**
 * Hook to fetch AI Council sessions for a project
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function useCouncilSessions(
  projectId: string | undefined,
  options?: { page?: number; page_size?: number }
) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: councilKeys.sessionList(projectId || "", options),
    queryFn: () => {
      if (!projectId) {
        throw new Error("Missing project ID");
      }
      return getCouncilSessions(projectId, options);
    },
    enabled: isAuthenticated && !authLoading && !!projectId,
    staleTime: 60 * 1000, // 1 minute
  });
}

/**
 * Hook to fetch messages for a council session
 * Sprint 69: Chat history for AI Council
 */
export function useCouncilMessages(sessionId: string | undefined) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: councilKeys.messageList(sessionId || ""),
    queryFn: () => {
      if (!sessionId) {
        throw new Error("Missing session ID");
      }
      return getCouncilMessages(sessionId);
    },
    enabled: isAuthenticated && !authLoading && !!sessionId,
    staleTime: 10 * 1000, // 10 seconds - messages update during active sessions
    refetchInterval: (query) => {
      // Auto-refresh if session is active
      return query.state.data ? 5000 : false;
    },
  });
}

/**
 * Hook to create a new AI Council session
 * Sprint 69: Start new discussion with AI Council
 */
export function useCreateCouncilSession() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ projectId, topic }: { projectId: string; topic: string }) =>
      createCouncilSession(projectId, topic),
    onSuccess: (_, variables) => {
      // Invalidate sessions list for the project
      queryClient.invalidateQueries({
        queryKey: councilKeys.sessionList(variables.projectId),
      });
    },
  });
}

/**
 * Hook to send a message to AI Council
 * Sprint 69: Interactive chat with AI Council
 */
export function useSendCouncilMessage() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ sessionId, content }: { sessionId: string; content: string }) =>
      sendCouncilMessage(sessionId, content),
    onSuccess: (_, variables) => {
      // Invalidate messages for the session
      queryClient.invalidateQueries({
        queryKey: councilKeys.messageList(variables.sessionId),
      });
    },
  });
}

/**
 * Hook to invalidate council cache
 */
export function useInvalidateCouncil() {
  const queryClient = useQueryClient();

  return (projectId?: string) => {
    if (projectId) {
      queryClient.invalidateQueries({
        queryKey: councilKeys.sessionList(projectId),
      });
    } else {
      queryClient.invalidateQueries({ queryKey: councilKeys.all });
    }
  };
}

// Export types for use in components
export type { CouncilSession, CouncilMessage, CouncilSessionListResponse };
