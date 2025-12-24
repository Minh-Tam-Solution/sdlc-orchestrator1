/**
 * File: frontend/web/src/hooks/useOnboarding.ts
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 47
 * Date: December 23, 2025
 * Authority: Frontend Lead + CTO Approved
 * Foundation: Vietnamese Domain Templates + Onboarding IR (EP-06)
 *
 * Description:
 * React Query hooks for Vietnamese SME onboarding wizard API.
 * Provides caching, mutations, and error handling for the 5-step flow.
 */

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/api/client'
import type {
  OnboardingSession,
  DomainOption,
  FeatureOption,
  ScaleOption,
  StartOnboardingRequest,
  SetDomainRequest,
  SetAppNameRequest,
  SetFeaturesRequest,
  SetScaleRequest,
  OnboardingStepResponse,
  OnboardingBlueprintResponse,
} from '@/types/onboarding'

// =========================================================================
// QUERY KEYS
// =========================================================================

export const onboardingKeys = {
  all: ['onboarding'] as const,
  session: (sessionId: string) => [...onboardingKeys.all, 'session', sessionId] as const,
  options: () => [...onboardingKeys.all, 'options'] as const,
  domains: () => [...onboardingKeys.options(), 'domains'] as const,
  features: (domain: string) => [...onboardingKeys.options(), 'features', domain] as const,
  scales: () => [...onboardingKeys.options(), 'scales'] as const,
}

// =========================================================================
// API FUNCTIONS
// =========================================================================

async function startOnboarding(
  request: StartOnboardingRequest
): Promise<OnboardingSession> {
  const { data } = await apiClient.post<OnboardingSession>(
    '/codegen/onboarding/start',
    request
  )
  return data
}

async function getSession(sessionId: string): Promise<OnboardingSession> {
  const { data } = await apiClient.get<OnboardingSession>(
    `/codegen/onboarding/${sessionId}`
  )
  return data
}

async function getDomainOptions(): Promise<DomainOption[]> {
  const { data } = await apiClient.get<DomainOption[]>(
    '/codegen/onboarding/options/domains'
  )
  return data
}

async function getFeatureOptions(domain: string): Promise<FeatureOption[]> {
  const { data } = await apiClient.get<FeatureOption[]>(
    `/codegen/onboarding/options/features/${domain}`
  )
  return data
}

async function getScaleOptions(): Promise<ScaleOption[]> {
  const { data } = await apiClient.get<ScaleOption[]>(
    '/codegen/onboarding/options/scales'
  )
  return data
}

async function setDomain(
  sessionId: string,
  request: SetDomainRequest
): Promise<OnboardingStepResponse> {
  const { data } = await apiClient.post<OnboardingStepResponse>(
    `/codegen/onboarding/${sessionId}/domain`,
    request
  )
  return data
}

async function setAppName(
  sessionId: string,
  request: SetAppNameRequest
): Promise<OnboardingStepResponse> {
  const { data } = await apiClient.post<OnboardingStepResponse>(
    `/codegen/onboarding/${sessionId}/app_name`,
    request
  )
  return data
}

async function setFeatures(
  sessionId: string,
  request: SetFeaturesRequest
): Promise<OnboardingStepResponse> {
  const { data } = await apiClient.post<OnboardingStepResponse>(
    `/codegen/onboarding/${sessionId}/features`,
    request
  )
  return data
}

async function setScale(
  sessionId: string,
  request: SetScaleRequest
): Promise<OnboardingStepResponse> {
  const { data } = await apiClient.post<OnboardingStepResponse>(
    `/codegen/onboarding/${sessionId}/scale`,
    request
  )
  return data
}

async function generateBlueprint(
  sessionId: string
): Promise<OnboardingBlueprintResponse> {
  const { data } = await apiClient.post<OnboardingBlueprintResponse>(
    `/codegen/onboarding/${sessionId}/generate`
  )
  return data
}

// =========================================================================
// HOOKS - QUERIES
// =========================================================================

/**
 * Hook for getting onboarding session
 *
 * @param sessionId - Session ID to fetch
 * @param options - Query options
 *
 * @example
 * ```tsx
 * const { data: session, isLoading } = useOnboardingSession(sessionId)
 * ```
 */
export function useOnboardingSession(
  sessionId: string | null,
  options?: { enabled?: boolean }
) {
  return useQuery({
    queryKey: sessionId ? onboardingKeys.session(sessionId) : ['disabled'],
    queryFn: () => (sessionId ? getSession(sessionId) : Promise.reject('No session ID')),
    enabled: options?.enabled !== false && !!sessionId,
    staleTime: 10_000, // 10 seconds
    gcTime: 5 * 60 * 1000, // 5 minutes
  })
}

/**
 * Hook for getting domain options
 *
 * @example
 * ```tsx
 * const { data: domains } = useDomainOptions()
 * ```
 */
export function useDomainOptions() {
  return useQuery({
    queryKey: onboardingKeys.domains(),
    queryFn: getDomainOptions,
    staleTime: 5 * 60 * 1000, // 5 minutes (options don't change often)
    gcTime: 30 * 60 * 1000, // 30 minutes
  })
}

/**
 * Hook for getting feature options for a domain
 *
 * @param domain - Domain key
 * @param options - Query options
 *
 * @example
 * ```tsx
 * const { data: features } = useFeatureOptions('restaurant')
 * ```
 */
export function useFeatureOptions(
  domain: string | null,
  options?: { enabled?: boolean }
) {
  return useQuery({
    queryKey: domain ? onboardingKeys.features(domain) : ['disabled'],
    queryFn: () => (domain ? getFeatureOptions(domain) : Promise.reject('No domain')),
    enabled: options?.enabled !== false && !!domain,
    staleTime: 5 * 60 * 1000,
    gcTime: 30 * 60 * 1000,
  })
}

/**
 * Hook for getting scale options
 *
 * @example
 * ```tsx
 * const { data: scales } = useScaleOptions()
 * ```
 */
export function useScaleOptions() {
  return useQuery({
    queryKey: onboardingKeys.scales(),
    queryFn: getScaleOptions,
    staleTime: 5 * 60 * 1000,
    gcTime: 30 * 60 * 1000,
  })
}

// =========================================================================
// HOOKS - MUTATIONS
// =========================================================================

/**
 * Hook for starting new onboarding session
 *
 * @example
 * ```tsx
 * const { mutate: start, isLoading } = useStartOnboarding()
 *
 * const handleStart = () => {
 *   start({ locale: 'vi' }, {
 *     onSuccess: (session) => setSessionId(session.session_id)
 *   })
 * }
 * ```
 */
export function useStartOnboarding() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: startOnboarding,
    onSuccess: (session) => {
      queryClient.setQueryData(onboardingKeys.session(session.session_id), session)
    },
  })
}

/**
 * Hook for setting domain selection
 */
export function useSetDomain(sessionId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (request: SetDomainRequest) => setDomain(sessionId, request),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: onboardingKeys.session(sessionId) })
    },
  })
}

/**
 * Hook for setting app name
 */
export function useSetAppName(sessionId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (request: SetAppNameRequest) => setAppName(sessionId, request),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: onboardingKeys.session(sessionId) })
    },
  })
}

/**
 * Hook for setting features
 */
export function useSetFeatures(sessionId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (request: SetFeaturesRequest) => setFeatures(sessionId, request),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: onboardingKeys.session(sessionId) })
    },
  })
}

/**
 * Hook for setting scale
 */
export function useSetScale(sessionId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (request: SetScaleRequest) => setScale(sessionId, request),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: onboardingKeys.session(sessionId) })
    },
  })
}

/**
 * Hook for generating blueprint from completed session
 */
export function useGenerateBlueprint(sessionId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: () => generateBlueprint(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: onboardingKeys.session(sessionId) })
    },
  })
}

// =========================================================================
// COMBINED HOOK
// =========================================================================

/**
 * Combined hook for full onboarding wizard flow
 *
 * @param sessionId - Current session ID (null if not started)
 *
 * @example
 * ```tsx
 * const {
 *   session,
 *   domains,
 *   features,
 *   scales,
 *   start,
 *   setDomain,
 *   setAppName,
 *   setFeatures,
 *   setScale,
 *   generate,
 *   isLoading,
 * } = useOnboardingWizard(sessionId)
 * ```
 */
export function useOnboardingWizard(sessionId: string | null) {
  const sessionQuery = useOnboardingSession(sessionId)
  const domainsQuery = useDomainOptions()
  const featuresQuery = useFeatureOptions(sessionQuery.data?.domain ?? null)
  const scalesQuery = useScaleOptions()

  const startMutation = useStartOnboarding()
  const domainMutation = useSetDomain(sessionId ?? '')
  const appNameMutation = useSetAppName(sessionId ?? '')
  const featuresMutation = useSetFeatures(sessionId ?? '')
  const scaleMutation = useSetScale(sessionId ?? '')
  const generateMutation = useGenerateBlueprint(sessionId ?? '')

  const isLoading =
    sessionQuery.isLoading ||
    domainsQuery.isLoading ||
    startMutation.isPending ||
    domainMutation.isPending ||
    appNameMutation.isPending ||
    featuresMutation.isPending ||
    scaleMutation.isPending ||
    generateMutation.isPending

  return {
    // Data
    session: sessionQuery.data,
    domains: domainsQuery.data,
    features: featuresQuery.data,
    scales: scalesQuery.data,

    // Mutations
    start: startMutation.mutateAsync,
    setDomain: domainMutation.mutateAsync,
    setAppName: appNameMutation.mutateAsync,
    setFeatures: featuresMutation.mutateAsync,
    setScale: scaleMutation.mutateAsync,
    generate: generateMutation.mutateAsync,

    // State
    isLoading,
    isSessionLoading: sessionQuery.isLoading,
    isOptionsLoading: domainsQuery.isLoading || scalesQuery.isLoading,

    // Errors
    sessionError: sessionQuery.error,
    startError: startMutation.error,
    generateError: generateMutation.error,

    // Generation result
    blueprint: generateMutation.data?.blueprint,
    blueprintStats: generateMutation.data?.stats,
  }
}
