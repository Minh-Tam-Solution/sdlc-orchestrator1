/**
 * Organization Types - Next.js App Router
 * @module frontend/src/lib/types/organization
 * @status Sprint 84 - Teams & Organizations UI
 * @description Type definitions for Organization management
 * @note Based on backend schemas from Sprint 71 (Teams Backend API)
 * @see backend/app/schemas/team.py (OrganizationCreate, OrganizationResponse, etc.)
 */

import type { AgenticMaturity, PaginatedResponse } from "./team";

// =========================================================================
// Organization Plan Types
// =========================================================================

/**
 * Organization pricing plans
 */
export type OrganizationPlan = "free" | "starter" | "pro" | "enterprise";

// =========================================================================
// Organization Settings
// =========================================================================

export interface OrganizationSASEConfig {
  agentic_maturity?: AgenticMaturity;
  mentor_scripts?: string[];
  briefing_templates?: string[];
}

export interface OrganizationSettings {
  default_policy_pack?: string | null;
  require_mfa?: boolean;
  allowed_domains?: string[];
  max_teams?: number | null;
  max_projects_per_team?: number | null;
  branding?: {
    logo_url?: string | null;
    primary_color?: string | null;
    secondary_color?: string | null;
  };
  sase_config?: OrganizationSASEConfig;
}

// =========================================================================
// Organization Model
// =========================================================================

export interface Organization {
  id: string;
  name: string;
  slug: string;
  plan: OrganizationPlan;
  settings: OrganizationSettings;
  teams_count: number;
  users_count: number;
  created_at: string;
  updated_at: string;
}

export interface OrganizationDetail extends Organization {
  is_enterprise: boolean;
  is_paid: boolean;
  require_mfa: boolean;
  allowed_domains: string[];
  agentic_maturity: AgenticMaturity;
}

// =========================================================================
// Organization CRUD Requests
// =========================================================================

export interface OrganizationCreate {
  name: string;
  slug: string;
  plan?: OrganizationPlan;
  settings?: OrganizationSettings;
}

export interface OrganizationUpdate {
  name?: string;
  plan?: OrganizationPlan;
  settings?: Partial<OrganizationSettings>;
}

// =========================================================================
// Organization Statistics
// =========================================================================

export interface OrganizationStatistics {
  organization_id: string;
  organization_name: string;
  plan: OrganizationPlan;
  teams_count: number;
  users_count: number;
  agentic_maturity: AgenticMaturity;
  require_mfa: boolean;
  allowed_domains: string[];
  created_at: string;
  updated_at: string;
}

// =========================================================================
// Paginated Responses
// =========================================================================

export type OrganizationListResponse = PaginatedResponse<Organization>;

// =========================================================================
// Query Parameters
// =========================================================================

export interface OrganizationListParams {
  skip?: number;
  limit?: number;
}

// =========================================================================
// Plan Metadata for UI
// =========================================================================

export const ORGANIZATION_PLAN_META: Record<
  OrganizationPlan,
  { label: string; color: string; description: string; features: string[] }
> = {
  free: {
    label: "Free",
    color: "bg-gray-100 text-gray-800",
    description: "For individuals and small teams getting started",
    features: [
      "Up to 2 teams",
      "Up to 5 members",
      "3 projects per team",
      "Basic governance features",
      "Community support",
    ],
  },
  starter: {
    label: "Starter",
    color: "bg-blue-100 text-blue-800",
    description: "For growing teams with basic governance needs",
    features: [
      "Up to 5 teams",
      "Up to 20 members",
      "10 projects per team",
      "Custom policies",
      "Email support",
    ],
  },
  pro: {
    label: "Pro",
    color: "bg-purple-100 text-purple-800",
    description: "For professional teams requiring advanced features",
    features: [
      "Unlimited teams",
      "Up to 100 members",
      "Unlimited projects",
      "Advanced SASE features",
      "Priority support",
      "Custom integrations",
    ],
  },
  enterprise: {
    label: "Enterprise",
    color: "bg-orange-100 text-orange-800",
    description: "For large organizations with compliance requirements",
    features: [
      "Unlimited everything",
      "SSO/SAML integration",
      "Audit log retention",
      "Dedicated support",
      "SLA guarantee",
      "On-premise option",
    ],
  },
};

// =========================================================================
// Helper Functions
// =========================================================================

/**
 * Check if organization is on a paid plan
 */
export function isPaidPlan(plan: OrganizationPlan): boolean {
  return plan !== "free";
}

/**
 * Check if organization is enterprise
 */
export function isEnterprisePlan(plan: OrganizationPlan): boolean {
  return plan === "enterprise";
}

/**
 * Get plan limits
 */
export function getPlanLimits(plan: OrganizationPlan): {
  maxTeams: number | null;
  maxMembers: number | null;
  maxProjectsPerTeam: number | null;
} {
  switch (plan) {
    case "free":
      return { maxTeams: 2, maxMembers: 5, maxProjectsPerTeam: 3 };
    case "starter":
      return { maxTeams: 5, maxMembers: 20, maxProjectsPerTeam: 10 };
    case "pro":
      return { maxTeams: null, maxMembers: 100, maxProjectsPerTeam: null };
    case "enterprise":
      return { maxTeams: null, maxMembers: null, maxProjectsPerTeam: null };
    default:
      return { maxTeams: 2, maxMembers: 5, maxProjectsPerTeam: 3 };
  }
}

/**
 * Format organization slug from name
 */
export function formatOrgSlug(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .substring(0, 100);
}

/**
 * Get plan badge color class
 */
export function getPlanBadgeClass(plan: OrganizationPlan): string {
  return ORGANIZATION_PLAN_META[plan]?.color ?? "bg-gray-100 text-gray-800";
}

/**
 * Check if organization can add more teams
 */
export function canAddTeam(org: Organization): boolean {
  const limits = getPlanLimits(org.plan);
  if (limits.maxTeams === null) return true;
  return org.teams_count < limits.maxTeams;
}

/**
 * Check if organization can add more members
 */
export function canAddMember(org: Organization): boolean {
  const limits = getPlanLimits(org.plan);
  if (limits.maxMembers === null) return true;
  return org.users_count < limits.maxMembers;
}

/**
 * Get upgrade recommendation if at limit
 */
export function getUpgradeRecommendation(org: Organization): OrganizationPlan | null {
  const limits = getPlanLimits(org.plan);

  if (limits.maxTeams !== null && org.teams_count >= limits.maxTeams) {
    return getNextPlan(org.plan);
  }
  if (limits.maxMembers !== null && org.users_count >= limits.maxMembers) {
    return getNextPlan(org.plan);
  }

  return null;
}

/**
 * Get next tier plan
 */
export function getNextPlan(currentPlan: OrganizationPlan): OrganizationPlan | null {
  const planOrder: OrganizationPlan[] = ["free", "starter", "pro", "enterprise"];
  const currentIndex = planOrder.indexOf(currentPlan);

  if (currentIndex === -1 || currentIndex >= planOrder.length - 1) {
    return null;
  }

  return planOrder[currentIndex + 1];
}
