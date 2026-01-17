/**
 * Codegen TanStack Query Hooks - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/hooks/useCodegen
 * @description React Query hooks for Codegen API
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 69 - Zero Mock Policy Compliance
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getCodegenTemplates,
  getCodegenSessions,
  createCodegenSession,
  type CodegenTemplate,
  type CodegenSession,
  type CodegenSessionListResponse,
  type CreateCodegenRequest,
  type CodegenListOptions,
} from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";

// Query keys for cache management
export const codegenKeys = {
  all: ["codegen"] as const,
  templates: () => [...codegenKeys.all, "templates"] as const,
  sessions: () => [...codegenKeys.all, "sessions"] as const,
  sessionList: (options?: CodegenListOptions) =>
    [...codegenKeys.sessions(), "list", options] as const,
  session: (id: string) => [...codegenKeys.sessions(), "detail", id] as const,
};

/**
 * Hook to fetch codegen templates
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function useCodegenTemplates() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: codegenKeys.templates(),
    queryFn: getCodegenTemplates,
    enabled: isAuthenticated && !authLoading,
    staleTime: 5 * 60 * 1000, // 5 minutes (templates rarely change)
  });
}

/**
 * Hook to fetch codegen session history
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function useCodegenSessions(options?: CodegenListOptions) {
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  return useQuery({
    queryKey: codegenKeys.sessionList(options),
    queryFn: () => getCodegenSessions(options),
    enabled: isAuthenticated && !authLoading,
    staleTime: 30 * 1000, // 30 seconds (sessions can change frequently)
    refetchInterval: 30 * 1000, // Auto-refresh every 30s for active sessions
  });
}

/**
 * Hook to create a new codegen session
 * Sprint 69: Uses httpOnly cookie auth (credentials: "include")
 */
export function useCreateCodegenSession() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: CreateCodegenRequest) => createCodegenSession(request),
    onSuccess: () => {
      // Invalidate sessions list to show new session
      queryClient.invalidateQueries({ queryKey: codegenKeys.sessions() });
    },
  });
}

/**
 * Hook to invalidate codegen cache
 */
export function useInvalidateCodegen() {
  const queryClient = useQueryClient();

  return () => {
    queryClient.invalidateQueries({ queryKey: codegenKeys.all });
  };
}

// Re-export types for convenience
export type { CodegenTemplate, CodegenSession, CodegenSessionListResponse };
