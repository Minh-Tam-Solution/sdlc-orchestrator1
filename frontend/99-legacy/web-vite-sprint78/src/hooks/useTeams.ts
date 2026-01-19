/**
 * =========================================================================
 * useTeams - React Query Hooks for Teams & Organizations API
 * SDLC Orchestrator - Sprint 72 (Teams Frontend)
 *
 * Version: 1.0.0
 * Date: January 27, 2026
 * Status: ACTIVE - Sprint 72 Day 1
 * Authority: Frontend Lead + CTO Approved
 *
 * Purpose:
 * - Connect team components to backend Teams API
 * - Fetch teams, organizations, and members
 * - Mutations for CRUD operations
 * - Cache invalidation and optimistic updates
 *
 * References:
 * - backend/app/services/teams_service.py
 * - backend/app/services/organizations_service.py
 * - backend/app/api/routes/teams.py
 * - backend/app/api/routes/organizations.py
 * =========================================================================
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/api/client";
import { toast } from "@/components/ui/use-toast";

// ============================================================================
// Types (aligned with backend schemas)
// ============================================================================

/** Organization plan enum */
export type OrganizationPlan = "free" | "starter" | "pro" | "enterprise";

/** Team member type (SE4H vs SE4A) */
export type MemberType = "human" | "ai_agent";

/** Team role enum */
export type TeamRole = "owner" | "admin" | "member";

/** Organization from API */
export interface Organization {
  id: string;
  name: string;
  slug: string;
  plan: OrganizationPlan;
  settings: {
    require_mfa?: boolean;
    allowed_domains?: string[];
    sase_config?: {
      agentic_maturity?: string;
      se4h_enabled?: boolean;
      se4a_enabled?: boolean;
    };
  };
  created_at: string;
  updated_at: string;
}

/** Team from API */
export interface Team {
  id: string;
  organization_id: string;
  name: string;
  slug: string;
  description?: string;
  settings: {
    sase_config?: {
      agentic_maturity?: string;
      se4h_enabled?: boolean;
      se4a_enabled?: boolean;
    };
  };
  created_at: string;
  updated_at: string;
}

/** Team member from API */
export interface TeamMember {
  id: string;
  team_id: string;
  user_id: string;
  role: TeamRole;
  member_type: MemberType;
  joined_at: string;
  user?: {
    id: string;
    email: string;
    full_name?: string;
    avatar_url?: string;
  };
}

/** Team with members and projects */
export interface TeamWithDetails extends Team {
  members: TeamMember[];
  member_count: number;
  project_count: number;
}

/** Team statistics from API */
export interface TeamStatistics {
  team_id: string;
  team_name: string;
  member_count: number;
  project_count: number;
  active_projects: number;
  agentic_maturity: string;
  se4h_count: number;
  se4a_count: number;
  created_at: string;
  updated_at: string;
}

/** Organization statistics from API */
export interface OrganizationStatistics {
  organization_id: string;
  organization_name: string;
  plan: OrganizationPlan;
  teams_count: number;
  users_count: number;
  agentic_maturity: string;
  require_mfa: boolean;
  allowed_domains: string[];
  created_at: string;
  updated_at: string;
}

// ============================================================================
// Query Keys
// ============================================================================

export const teamsKeys = {
  all: ["teams"] as const,
  lists: () => [...teamsKeys.all, "list"] as const,
  list: (filters: { organizationId?: string }) =>
    [...teamsKeys.lists(), filters] as const,
  details: () => [...teamsKeys.all, "detail"] as const,
  detail: (id: string) => [...teamsKeys.details(), id] as const,
  statistics: (id: string) => [...teamsKeys.detail(id), "statistics"] as const,
};

export const organizationsKeys = {
  all: ["organizations"] as const,
  lists: () => [...organizationsKeys.all, "list"] as const,
  list: (filters: { userId?: string }) =>
    [...organizationsKeys.lists(), filters] as const,
  details: () => [...organizationsKeys.all, "detail"] as const,
  detail: (id: string) => [...organizationsKeys.details(), id] as const,
  statistics: (id: string) =>
    [...organizationsKeys.detail(id), "statistics"] as const,
};

// ============================================================================
// API Functions - Teams
// ============================================================================

/** Fetch teams list */
async function fetchTeams(organizationId?: string): Promise<Team[]> {
  const params = new URLSearchParams();
  if (organizationId) {
    params.set("organization_id", organizationId);
  }

  const response = await apiClient.get<Team[]>(`/teams?${params}`);
  return response.data;
}

/** Fetch single team with details */
async function fetchTeam(teamId: string): Promise<TeamWithDetails> {
  const response = await apiClient.get<TeamWithDetails>(`/teams/${teamId}`);
  return response.data;
}

/** Fetch team statistics */
async function fetchTeamStatistics(teamId: string): Promise<TeamStatistics> {
  const response = await apiClient.get<TeamStatistics>(
    `/teams/${teamId}/statistics`
  );
  return response.data;
}

/** Create team */
interface CreateTeamData {
  organization_id: string;
  name: string;
  slug: string;
  description?: string;
}

async function createTeam(data: CreateTeamData): Promise<Team> {
  const response = await apiClient.post<Team>("/teams", data);
  return response.data;
}

/** Update team */
interface UpdateTeamData {
  name?: string;
  slug?: string;
  description?: string;
}

async function updateTeam(
  teamId: string,
  data: UpdateTeamData
): Promise<Team> {
  const response = await apiClient.put<Team>(`/teams/${teamId}`, data);
  return response.data;
}

/** Delete team */
async function deleteTeam(teamId: string): Promise<void> {
  await apiClient.delete(`/teams/${teamId}`);
}

// ============================================================================
// API Functions - Team Members
// ============================================================================

/** Add team member */
interface AddMemberData {
  user_id: string;
  role?: TeamRole;
  member_type?: MemberType;
}

async function addTeamMember(
  teamId: string,
  data: AddMemberData
): Promise<TeamMember> {
  const response = await apiClient.post<TeamMember>(
    `/teams/${teamId}/members`,
    data
  );
  return response.data;
}

/** Remove team member */
async function removeTeamMember(
  teamId: string,
  userId: string
): Promise<void> {
  await apiClient.delete(`/teams/${teamId}/members/${userId}`);
}

/** Update member role */
interface UpdateMemberRoleData {
  role: TeamRole;
}

async function updateTeamMemberRole(
  teamId: string,
  userId: string,
  data: UpdateMemberRoleData
): Promise<TeamMember> {
  const response = await apiClient.patch<TeamMember>(
    `/teams/${teamId}/members/${userId}`,
    data
  );
  return response.data;
}

// ============================================================================
// API Functions - Organizations
// ============================================================================

/** Fetch organizations list */
async function fetchOrganizations(userId?: string): Promise<Organization[]> {
  const params = new URLSearchParams();
  if (userId) {
    params.set("user_id", userId);
  }

  const response = await apiClient.get<Organization[]>(
    `/organizations?${params}`
  );
  return response.data;
}

/** Fetch single organization */
async function fetchOrganization(orgId: string): Promise<Organization> {
  const response = await apiClient.get<Organization>(`/organizations/${orgId}`);
  return response.data;
}

/** Fetch organization statistics */
async function fetchOrganizationStatistics(
  orgId: string
): Promise<OrganizationStatistics> {
  const response = await apiClient.get<OrganizationStatistics>(
    `/organizations/${orgId}/stats`
  );
  return response.data;
}

/** Create organization */
interface CreateOrganizationData {
  name: string;
  slug: string;
  plan?: OrganizationPlan;
}

async function createOrganization(
  data: CreateOrganizationData
): Promise<Organization> {
  const response = await apiClient.post<Organization>("/organizations", data);
  return response.data;
}

/** Update organization */
interface UpdateOrganizationData {
  name?: string;
  slug?: string;
  plan?: OrganizationPlan;
}

async function updateOrganization(
  orgId: string,
  data: UpdateOrganizationData
): Promise<Organization> {
  const response = await apiClient.put<Organization>(
    `/organizations/${orgId}`,
    data
  );
  return response.data;
}

// ============================================================================
// React Query Hooks - Teams
// ============================================================================

/**
 * Hook to fetch teams list
 */
export function useTeams(organizationId?: string) {
  return useQuery({
    queryKey: teamsKeys.list({ organizationId }),
    queryFn: () => fetchTeams(organizationId),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 30 * 60 * 1000, // 30 minutes
  });
}

/**
 * Hook to fetch single team with details
 */
export function useTeam(teamId: string | null) {
  return useQuery({
    queryKey: teamsKeys.detail(teamId || ""),
    queryFn: () => fetchTeam(teamId!),
    enabled: !!teamId,
    staleTime: 5 * 60 * 1000,
    gcTime: 30 * 60 * 1000,
  });
}

/**
 * Hook to fetch team statistics
 */
export function useTeamStatistics(teamId: string | null) {
  return useQuery({
    queryKey: teamsKeys.statistics(teamId || ""),
    queryFn: () => fetchTeamStatistics(teamId!),
    enabled: !!teamId,
    staleTime: 5 * 60 * 1000,
    gcTime: 30 * 60 * 1000,
  });
}

/**
 * Hook to create team
 */
export function useCreateTeam() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createTeam,
    onSuccess: (newTeam) => {
      // Invalidate teams list
      queryClient.invalidateQueries({ queryKey: teamsKeys.lists() });

      toast({
        title: "Team created",
        description: `Team "${newTeam.name}" has been created successfully.`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to create team",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

/**
 * Hook to update team
 */
export function useUpdateTeam(teamId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UpdateTeamData) => updateTeam(teamId, data),
    onSuccess: (updatedTeam) => {
      // Invalidate team detail and lists
      queryClient.invalidateQueries({ queryKey: teamsKeys.detail(teamId) });
      queryClient.invalidateQueries({ queryKey: teamsKeys.lists() });

      toast({
        title: "Team updated",
        description: `Team "${updatedTeam.name}" has been updated successfully.`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to update team",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

/**
 * Hook to delete team
 */
export function useDeleteTeam() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteTeam,
    onSuccess: () => {
      // Invalidate teams list
      queryClient.invalidateQueries({ queryKey: teamsKeys.lists() });

      toast({
        title: "Team deleted",
        description: "The team has been deleted successfully.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to delete team",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

// ============================================================================
// React Query Hooks - Team Members
// ============================================================================

/**
 * Hook to add team member
 */
export function useAddTeamMember(teamId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: AddMemberData) => addTeamMember(teamId, data),
    onSuccess: () => {
      // Invalidate team detail to refresh members list
      queryClient.invalidateQueries({ queryKey: teamsKeys.detail(teamId) });
      queryClient.invalidateQueries({
        queryKey: teamsKeys.statistics(teamId),
      });

      toast({
        title: "Member added",
        description: "Team member has been added successfully.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to add member",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

/**
 * Hook to remove team member
 */
export function useRemoveTeamMember(teamId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (userId: string) => removeTeamMember(teamId, userId),
    onSuccess: () => {
      // Invalidate team detail to refresh members list
      queryClient.invalidateQueries({ queryKey: teamsKeys.detail(teamId) });
      queryClient.invalidateQueries({
        queryKey: teamsKeys.statistics(teamId),
      });

      toast({
        title: "Member removed",
        description: "Team member has been removed successfully.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to remove member",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

/**
 * Hook to update member role
 */
export function useUpdateTeamMemberRole(teamId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ userId, role }: { userId: string; role: TeamRole }) =>
      updateTeamMemberRole(teamId, userId, { role }),
    onSuccess: () => {
      // Invalidate team detail to refresh members list
      queryClient.invalidateQueries({ queryKey: teamsKeys.detail(teamId) });

      toast({
        title: "Role updated",
        description: "Member role has been updated successfully.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to update role",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

// ============================================================================
// React Query Hooks - Organizations
// ============================================================================

/**
 * Hook to fetch organizations list
 */
export function useOrganizations(userId?: string) {
  return useQuery({
    queryKey: organizationsKeys.list({ userId }),
    queryFn: () => fetchOrganizations(userId),
    staleTime: 5 * 60 * 1000,
    gcTime: 30 * 60 * 1000,
  });
}

/**
 * Hook to fetch single organization
 */
export function useOrganization(orgId: string | null) {
  return useQuery({
    queryKey: organizationsKeys.detail(orgId || ""),
    queryFn: () => fetchOrganization(orgId!),
    enabled: !!orgId,
    staleTime: 5 * 60 * 1000,
    gcTime: 30 * 60 * 1000,
  });
}

/**
 * Hook to fetch organization statistics
 */
export function useOrganizationStatistics(orgId: string | null) {
  return useQuery({
    queryKey: organizationsKeys.statistics(orgId || ""),
    queryFn: () => fetchOrganizationStatistics(orgId!),
    enabled: !!orgId,
    staleTime: 5 * 60 * 1000,
    gcTime: 30 * 60 * 1000,
  });
}

/**
 * Hook to create organization
 */
export function useCreateOrganization() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createOrganization,
    onSuccess: (newOrg) => {
      // Invalidate organizations list
      queryClient.invalidateQueries({ queryKey: organizationsKeys.lists() });

      toast({
        title: "Organization created",
        description: `Organization "${newOrg.name}" has been created successfully.`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to create organization",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

/**
 * Hook to update organization
 */
export function useUpdateOrganization(orgId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UpdateOrganizationData) =>
      updateOrganization(orgId, data),
    onSuccess: (updatedOrg) => {
      // Invalidate organization detail and lists
      queryClient.invalidateQueries({
        queryKey: organizationsKeys.detail(orgId),
      });
      queryClient.invalidateQueries({ queryKey: organizationsKeys.lists() });

      toast({
        title: "Organization updated",
        description: `Organization "${updatedOrg.name}" has been updated successfully.`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to update organization",
        description: error.message,
        variant: "destructive",
      });
    },
  });
}

// ============================================================================
// Helper Hooks
// ============================================================================

/**
 * Hook to get current user's team membership
 */
export function useMyTeams() {
  return useTeams();
}

/**
 * Hook to check if user is team owner/admin
 */
export function useIsTeamAdmin(teamId: string | null, userId: string | null) {
  const { data: team } = useTeam(teamId);

  if (!team || !userId) {
    return false;
  }

  const member = team.members.find((m) => m.user_id === userId);
  return member?.role === "owner" || member?.role === "admin";
}

/**
 * Hook to check if user is team owner
 */
export function useIsTeamOwner(teamId: string | null, userId: string | null) {
  const { data: team } = useTeam(teamId);

  if (!team || !userId) {
    return false;
  }

  const member = team.members.find((m) => m.user_id === userId);
  return member?.role === "owner";
}

/**
 * Hook to invalidate teams cache
 */
export function useInvalidateTeamsCache() {
  const queryClient = useQueryClient();

  return {
    invalidateTeam: (teamId: string) => {
      queryClient.invalidateQueries({ queryKey: teamsKeys.detail(teamId) });
    },
    invalidateAllTeams: () => {
      queryClient.invalidateQueries({ queryKey: teamsKeys.all });
    },
    invalidateOrganization: (orgId: string) => {
      queryClient.invalidateQueries({
        queryKey: organizationsKeys.detail(orgId),
      });
    },
    invalidateAllOrganizations: () => {
      queryClient.invalidateQueries({ queryKey: organizationsKeys.all });
    },
  };
}
