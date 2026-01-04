/**
 * Onboarding Hooks - Next.js App Router
 * @module frontend/landing/src/hooks/useOnboarding
 * @status Sprint 66 - EP-06 Migration
 * @description TanStack Query hooks for Vietnamese SME onboarding wizard
 * @note Uses httpOnly cookies for auth (Sprint 63 migration)
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "@/hooks/useAuth";
import type {
  OnboardingSession,
  DomainOption,
  FeatureOption,
  ScaleOption,
  OnboardingBlueprintResponse,
} from "@/lib/types/onboarding";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Fetch helper with httpOnly cookie auth
 * Sprint 63: Uses credentials: 'include' for httpOnly cookies
 */
async function fetchWithAuth<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    ...options,
    credentials: "include", // Include httpOnly cookies
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Start onboarding session
 */
export function useStartOnboarding() {
  const { isAuthenticated } = useAuth();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (locale: "vi" | "en" = "vi") => {
      if (!isAuthenticated) throw new Error("Not authenticated");
      return fetchWithAuth<OnboardingSession>("/codegen/onboarding/start", {
        method: "POST",
        body: JSON.stringify({ locale }),
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["onboarding"] });
    },
  });
}

/**
 * Get domain options
 */
export function useDomainOptions(sessionId: string | null) {
  const { isAuthenticated } = useAuth();

  return useQuery<DomainOption[]>({
    queryKey: ["onboarding", "domains", sessionId],
    queryFn: async () => {
      return fetchWithAuth<DomainOption[]>("/codegen/onboarding/options/domains");
    },
    enabled: !!sessionId && isAuthenticated,
  });
}

/**
 * Get feature options for a domain
 */
export function useFeatureOptions(sessionId: string | null, domain: string | null) {
  const { isAuthenticated } = useAuth();

  return useQuery<FeatureOption[]>({
    queryKey: ["onboarding", "features", sessionId, domain],
    queryFn: async () => {
      if (!domain) throw new Error("Domain missing");
      return fetchWithAuth<FeatureOption[]>(
        `/codegen/onboarding/options/features/${domain}`
      );
    },
    enabled: !!sessionId && !!domain && isAuthenticated,
  });
}

/**
 * Get scale options
 */
export function useScaleOptions(sessionId: string | null) {
  const { isAuthenticated } = useAuth();

  return useQuery<ScaleOption[]>({
    queryKey: ["onboarding", "scales", sessionId],
    queryFn: async () => {
      return fetchWithAuth<ScaleOption[]>("/codegen/onboarding/options/scales");
    },
    enabled: !!sessionId && isAuthenticated,
  });
}

/**
 * Set domain
 */
export function useSetDomain(sessionId: string | null) {
  const { isAuthenticated } = useAuth();

  return useMutation({
    mutationFn: async (domain: string) => {
      if (!isAuthenticated || !sessionId)
        throw new Error("Not authenticated or session missing");
      return fetchWithAuth(`/codegen/onboarding/${sessionId}/domain`, {
        method: "POST",
        body: JSON.stringify({ domain }),
      });
    },
  });
}

/**
 * Set app name
 */
export function useSetAppName(sessionId: string | null) {
  const { isAuthenticated } = useAuth();

  return useMutation({
    mutationFn: async (appName: string) => {
      if (!isAuthenticated || !sessionId)
        throw new Error("Not authenticated or session missing");
      return fetchWithAuth(`/codegen/onboarding/${sessionId}/app_name`, {
        method: "POST",
        body: JSON.stringify({ app_name: appName }),
      });
    },
  });
}

/**
 * Set features
 */
export function useSetFeatures(sessionId: string | null) {
  const { isAuthenticated } = useAuth();

  return useMutation({
    mutationFn: async (features: string[]) => {
      if (!isAuthenticated || !sessionId)
        throw new Error("Not authenticated or session missing");
      return fetchWithAuth(`/codegen/onboarding/${sessionId}/features`, {
        method: "POST",
        body: JSON.stringify({ features }),
      });
    },
  });
}

/**
 * Set scale
 */
export function useSetScale(sessionId: string | null) {
  const { isAuthenticated } = useAuth();

  return useMutation({
    mutationFn: async (scale: string) => {
      if (!isAuthenticated || !sessionId)
        throw new Error("Not authenticated or session missing");
      return fetchWithAuth(`/codegen/onboarding/${sessionId}/scale`, {
        method: "POST",
        body: JSON.stringify({ scale }),
      });
    },
  });
}

/**
 * Generate blueprint
 */
export function useGenerateBlueprint(sessionId: string | null) {
  const { isAuthenticated } = useAuth();

  return useMutation<OnboardingBlueprintResponse, Error>({
    mutationFn: async () => {
      if (!isAuthenticated || !sessionId)
        throw new Error("Not authenticated or session missing");
      return fetchWithAuth<OnboardingBlueprintResponse>(
        `/codegen/onboarding/${sessionId}/generate`,
        { method: "POST" }
      );
    },
  });
}

/**
 * Combined onboarding wizard hook
 * Manages full onboarding flow with all mutations
 */
export function useOnboardingWizard() {
  const startMutation = useStartOnboarding();

  return {
    startSession: startMutation.mutateAsync,
    isStarting: startMutation.isPending,
    startError: startMutation.error,
  };
}

/**
 * Submit all wizard steps and generate blueprint
 */
export function useSubmitWizard(sessionId: string | null) {
  const { isAuthenticated } = useAuth();

  return useMutation<
    OnboardingBlueprintResponse,
    Error,
    {
      domain: string;
      appName: string;
      features: string[];
      scale: string;
    }
  >({
    mutationFn: async ({ domain, appName, features, scale }) => {
      if (!isAuthenticated || !sessionId) {
        throw new Error("Not authenticated or session missing");
      }

      // Submit all steps sequentially
      await fetchWithAuth(`/codegen/onboarding/${sessionId}/domain`, {
        method: "POST",
        body: JSON.stringify({ domain }),
      });

      await fetchWithAuth(`/codegen/onboarding/${sessionId}/app_name`, {
        method: "POST",
        body: JSON.stringify({ app_name: appName }),
      });

      await fetchWithAuth(`/codegen/onboarding/${sessionId}/features`, {
        method: "POST",
        body: JSON.stringify({ features }),
      });

      await fetchWithAuth(`/codegen/onboarding/${sessionId}/scale`, {
        method: "POST",
        body: JSON.stringify({ scale }),
      });

      // Generate blueprint
      return fetchWithAuth<OnboardingBlueprintResponse>(
        `/codegen/onboarding/${sessionId}/generate`,
        { method: "POST" }
      );
    },
  });
}
