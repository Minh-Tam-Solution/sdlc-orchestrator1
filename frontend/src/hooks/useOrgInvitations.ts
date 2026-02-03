/**
 * Organization Invitations Hook
 *
 * Sprint: 146 - Organization Access Control
 * Reference: ADR-047-Organization-Invitation-System.md
 *
 * Provides TanStack Query mutations for organization-level invitations.
 * Separate from team invitations (useInvitations.ts).
 *
 * API Endpoints:
 * - POST /organizations/{id}/invitations - Send invitation
 * - POST /org-invitations/{id}/resend - Resend invitation
 * - GET /org-invitations/{token} - Get invitation details (public)
 * - POST /org-invitations/{token}/accept - Accept invitation (auth)
 * - POST /org-invitations/{token}/decline - Decline invitation (public)
 * - GET /organizations/{id}/invitations - List invitations
 * - DELETE /org-invitations/{id} - Cancel invitation
 */

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

/** Organization invitation status */
export type OrgInvitationStatus =
  | "pending"
  | "accepted"
  | "declined"
  | "expired"
  | "cancelled";

/** Organization role (cannot invite as owner) */
export type OrgInvitationRole = "admin" | "member";

/** Organization invitation response */
export interface OrgInvitation {
  id: string;
  organization_id: string;
  invited_email: string;
  role: OrgInvitationRole;
  status: OrgInvitationStatus;
  invited_by: string;
  invited_by_name?: string;
  expires_at: string;
  created_at: string;
  updated_at: string;
  accepted_at?: string;
  declined_at?: string;
  resend_count: number;
  last_resent_at?: string;
}

/** Request to send organization invitation */
export interface SendOrgInvitationRequest {
  invited_email: string;
  role: OrgInvitationRole;
  message?: string;
}

/** Response from send invitation */
export interface SendOrgInvitationResponse {
  id: string;
  organization_id: string;
  invited_email: string;
  role: OrgInvitationRole;
  status: OrgInvitationStatus;
  expires_at: string;
  created_at: string;
}

/** Organization invitation details (public endpoint) */
export interface OrgInvitationDetails {
  id: string;
  organization_id: string;
  organization_name: string;
  organization_slug: string;
  invited_email: string;
  role: OrgInvitationRole;
  status: OrgInvitationStatus;
  invited_by_name: string;
  expires_at: string;
  is_expired: boolean;
}

/** Response from accept invitation */
export interface AcceptOrgInvitationResponse {
  organization_id: string;
  organization_name: string;
  role: OrgInvitationRole;
  redirect_url: string;
}

/** Response from decline invitation */
export interface DeclineOrgInvitationResponse {
  declined_at: string;
}

/** Response from resend invitation */
export interface ResendOrgInvitationResponse {
  id: string;
  resend_count: number;
  last_resent_at: string;
  expires_at: string;
}

/**
 * Hook for managing organization invitations
 *
 * @param organizationId - The organization ID to manage invitations for
 * @returns Invitation data, loading states, errors, and mutation functions
 *
 * @example
 * ```tsx
 * const { sendInvitation, isSending } = useOrgInvitations(orgId);
 *
 * const handleInvite = async () => {
 *   await sendInvitation({
 *     invited_email: "user@example.com",
 *     role: "member",
 *   });
 * };
 * ```
 */
export function useOrgInvitations(organizationId: string) {
  const queryClient = useQueryClient();

  // Fetch organization invitations
  const {
    data: invitationsData,
    isLoading,
    error,
    refetch,
  } = useQuery<OrgInvitation[]>({
    queryKey: ["org-invitations", organizationId],
    queryFn: async (): Promise<OrgInvitation[]> => {
      const response = await api.get<OrgInvitation[]>(
        `/organizations/${organizationId}/invitations`
      );
      return response.data;
    },
    enabled: !!organizationId,
  });

  // Explicitly type invitations for TanStack Query type inference
  const invitations: OrgInvitation[] = invitationsData ?? [];

  // Send invitation mutation
  const {
    mutateAsync: sendInvitation,
    isPending: isSending,
    error: sendError,
  } = useMutation({
    mutationFn: async (
      data: SendOrgInvitationRequest
    ): Promise<SendOrgInvitationResponse> => {
      const response = await api.post<SendOrgInvitationResponse>(
        `/organizations/${organizationId}/invitations`,
        data
      );
      return response.data;
    },
    onSuccess: () => {
      // Invalidate and refetch invitations list
      queryClient.invalidateQueries({
        queryKey: ["org-invitations", organizationId],
      });
    },
  });

  // Cancel invitation mutation
  const {
    mutateAsync: cancelInvitation,
    isPending: isCanceling,
    error: cancelError,
  } = useMutation({
    mutationFn: async (invitationId: string): Promise<void> => {
      await api.delete(`/org-invitations/${invitationId}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["org-invitations", organizationId],
      });
    },
  });

  // Resend invitation mutation
  const {
    mutateAsync: resendInvitation,
    isPending: isResending,
    error: resendError,
  } = useMutation({
    mutationFn: async (
      invitationId: string
    ): Promise<ResendOrgInvitationResponse> => {
      const response = await api.post<ResendOrgInvitationResponse>(
        `/org-invitations/${invitationId}/resend`
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["org-invitations", organizationId],
      });
    },
  });

  // Accept invitation mutation (for invited user)
  const {
    mutateAsync: acceptInvitation,
    isPending: isAccepting,
    error: acceptError,
  } = useMutation({
    mutationFn: async (token: string): Promise<AcceptOrgInvitationResponse> => {
      const response = await api.post<AcceptOrgInvitationResponse>(
        `/org-invitations/${token}/accept`
      );
      return response.data;
    },
    onSuccess: () => {
      // Invalidate organization membership queries
      queryClient.invalidateQueries({ queryKey: ["organizations"] });
      queryClient.invalidateQueries({ queryKey: ["user-organizations"] });
    },
  });

  // Decline invitation mutation (for invited user - public endpoint)
  const {
    mutateAsync: declineInvitation,
    isPending: isDeclining,
    error: declineError,
  } = useMutation({
    mutationFn: async (
      token: string
    ): Promise<DeclineOrgInvitationResponse> => {
      const response = await api.post<DeclineOrgInvitationResponse>(
        `/org-invitations/${token}/decline`
      );
      return response.data;
    },
  });

  // Get invitation by token (for invited user - public endpoint)
  const getInvitationByToken = async (
    token: string
  ): Promise<OrgInvitationDetails> => {
    const response = await api.get<OrgInvitationDetails>(
      `/org-invitations/${token}`
    );
    return response.data;
  };

  // Computed values
  const pendingInvitations = invitations.filter((i) => i.status === "pending");
  const expiredInvitations = invitations.filter((i) => i.status === "expired");
  const acceptedInvitations = invitations.filter(
    (i) => i.status === "accepted"
  );
  const declinedInvitations = invitations.filter(
    (i) => i.status === "declined"
  );
  const cancelledInvitations = invitations.filter(
    (i) => i.status === "cancelled"
  );

  return {
    // Data
    invitations,
    pendingInvitations,
    expiredInvitations,
    acceptedInvitations,
    declinedInvitations,
    cancelledInvitations,

    // Loading states
    isLoading,
    isSending,
    isCanceling,
    isResending,
    isAccepting,
    isDeclining,

    // Errors
    error,
    sendError,
    cancelError,
    resendError,
    acceptError,
    declineError,

    // Actions
    sendInvitation,
    cancelInvitation,
    resendInvitation,
    acceptInvitation,
    declineInvitation,
    getInvitationByToken,
    refetch,
  };
}

/**
 * Hook for accepting organization invitation from email link
 *
 * @param token - The invitation token from the email link
 * @returns Invitation details query result
 *
 * @example
 * ```tsx
 * // In invitation acceptance page
 * const { data: invitation, isLoading, error } = useAcceptOrgInvitation(token);
 *
 * if (isLoading) return <Spinner />;
 * if (error) return <ErrorMessage />;
 *
 * return <InvitationDetails invitation={invitation} />;
 * ```
 */
export function useAcceptOrgInvitation(token: string | null) {
  return useQuery<OrgInvitationDetails>({
    queryKey: ["org-invitation", token],
    queryFn: async (): Promise<OrgInvitationDetails> => {
      if (!token) throw new Error("No invitation token provided");
      const response = await api.get<OrgInvitationDetails>(
        `/org-invitations/${token}`
      );
      return response.data;
    },
    enabled: !!token,
  });
}

export default useOrgInvitations;
