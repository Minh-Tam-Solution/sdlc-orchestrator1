/**
 * File: frontend/web/src/types/onboarding.ts
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 47
 * Date: December 23, 2025
 * Authority: Frontend Lead + CTO Approved
 * Foundation: Vietnamese Domain Templates + Onboarding IR (EP-06)
 *
 * Description:
 * TypeScript types for Vietnamese SME onboarding wizard API.
 * Supports F&B, Hospitality, and Retail domains.
 */

/**
 * Onboarding session state from API
 */
export interface OnboardingSession {
  session_id: string
  current_step: OnboardingStep
  completed_steps: OnboardingStep[]
  domain: string | null
  app_name: string | null
  app_name_display: string | null
  features: string[]
  scale: string | null
  has_blueprint: boolean
  locale: 'vi' | 'en'
}

/**
 * Onboarding wizard steps
 */
export type OnboardingStep =
  | 'welcome'
  | 'domain'
  | 'app_name'
  | 'features'
  | 'scale'
  | 'confirm'
  | 'complete'

/**
 * Domain option from API
 */
export interface DomainOption {
  key: string
  name: string
  name_en: string
  description: string
  icon: string
  example_apps: string[]
}

/**
 * Feature option from API
 */
export interface FeatureOption {
  key: string
  name: string
  description: string
}

/**
 * Scale option from API
 */
export interface ScaleOption {
  key: string
  label: string
  employee_min: number
  employee_max: number
  cgf_tier: string
}

/**
 * Request to start onboarding session
 */
export interface StartOnboardingRequest {
  locale?: 'vi' | 'en'
}

/**
 * Request to set domain
 */
export interface SetDomainRequest {
  domain: string
}

/**
 * Request to set app name
 */
export interface SetAppNameRequest {
  app_name: string
}

/**
 * Request to set features
 */
export interface SetFeaturesRequest {
  features: string[]
}

/**
 * Request to set scale
 */
export interface SetScaleRequest {
  scale: string
}

/**
 * Response from step update
 */
export interface OnboardingStepResponse {
  success: boolean
  error: string | null
  next_step: OnboardingStep | null
  data: Record<string, unknown>
}

/**
 * Response from blueprint generation
 */
export interface OnboardingBlueprintResponse {
  success: boolean
  errors: string[]
  blueprint: AppBlueprint | null
  stats: {
    modules_count?: number
    entities_count?: number
    endpoints_count?: number
    generation_time_ms?: number
  }
}

/**
 * AppBlueprint IR structure (simplified for frontend)
 */
export interface AppBlueprint {
  name: string
  version: string
  domain?: string
  modules: AppModule[]
  _onboarding?: {
    domain: string
    scale: string
    cgf_tier: string
    features: string[]
    locale: string
    generated_at: string
  }
  _cgf?: {
    master_processes: string[]
    mdg_compliance: string[]
    dag_levels: Record<string, string>
  }
}

/**
 * Module in AppBlueprint
 */
export interface AppModule {
  name: string
  entities?: AppEntity[]
  endpoints?: AppEndpoint[]
}

/**
 * Entity in module
 */
export interface AppEntity {
  name: string
  fields?: AppField[]
}

/**
 * Field in entity
 */
export interface AppField {
  name: string
  type: string
  required?: boolean
}

/**
 * Endpoint in module
 */
export interface AppEndpoint {
  path: string
  method: string
  name: string
}

/**
 * Vietnamese labels for UI
 */
export const STEP_LABELS_VI: Record<OnboardingStep, string> = {
  welcome: 'Chào mừng',
  domain: 'Chọn ngành',
  app_name: 'Tên ứng dụng',
  features: 'Tính năng',
  scale: 'Quy mô',
  confirm: 'Xác nhận',
  complete: 'Hoàn tất',
}

/**
 * English labels for UI
 */
export const STEP_LABELS_EN: Record<OnboardingStep, string> = {
  welcome: 'Welcome',
  domain: 'Select Industry',
  app_name: 'App Name',
  features: 'Features',
  scale: 'Scale',
  confirm: 'Confirm',
  complete: 'Complete',
}

/**
 * Domain icons mapping
 */
export const DOMAIN_ICONS: Record<string, string> = {
  restaurant: '🍜',
  hotel: '🏨',
  retail: '🛒',
}

/**
 * Scale tier colors
 */
export const SCALE_TIER_COLORS: Record<string, string> = {
  LITE: 'bg-gray-100 text-gray-800',
  STANDARD: 'bg-blue-100 text-blue-800',
  PROFESSIONAL: 'bg-purple-100 text-purple-800',
  ENTERPRISE: 'bg-amber-100 text-amber-800',
}
