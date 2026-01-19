/**
 * =========================================================================
 * TeamMembersPage - Team Members Management
 * SDLC Orchestrator - Sprint 72 Day 4
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Status: ACTIVE - Sprint 72 Teams Frontend
 * Authority: Frontend Lead + CTO Approved
 *
 * Purpose:
 * - Display all team members in a table
 * - Invite new members (owners/admins only)
 * - Update member roles (owners only)
 * - Remove members (owners/admins)
 *
 * SASE Compliance:
 * - SE4H (Human Coach): Can manage members
 * - SE4A (AI Agent): Read-only view
 * - CTO R1/R2: AI agents cannot be owner/admin
 * =========================================================================
 */

import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { ArrowLeft, Plus, MoreHorizontal } from "lucide-react";
import {
  useTeam,
  useRemoveTeamMember,
  useUpdateTeamMemberRole,
  TeamRole,
} from "@/hooks/useTeams";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import InviteMemberDialog from "@/components/teams/InviteMemberDialog";

/**
 * Team Members Management Page
 */
export default function TeamMembersPage() {
  const { teamId } = useParams<{ teamId: string }>();
  const { data: team, isLoading } = useTeam(teamId || null);
  const removeMember = useRemoveTeamMember(teamId || "");
  const updateRole = useUpdateTeamMemberRole(teamId || "");

  const [showInviteDialog, setShowInviteDialog] = useState(false);
  const [memberToRemove, setMemberToRemove] = useState<string | null>(null);

  const handleRemoveMember = async () => {
    if (!memberToRemove) return;

    try {
      await removeMember.mutateAsync(memberToRemove);
      setMemberToRemove(null);
    } catch (error) {
      console.error("Failed to remove member:", error);
    }
  };

  const handleRoleChange = async (userId: string, role: TeamRole) => {
    try {
      await updateRole.mutateAsync({ userId, role });
    } catch (error) {
      console.error("Failed to update role:", error);
    }
  };

  if (isLoading) {
    return <MembersPageSkeleton />;
  }

  if (!team) {
    return (
      <div className="container mx-auto py-6">
        <p>Team not found</p>
      </div>
    );
  }

  // Check if current user is owner/admin
  // TODO: Get current user ID from auth context
  const isOwnerOrAdmin = true; // Placeholder

  return (
    <div className="container mx-auto py-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to={`/teams/${teamId}`}>
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-4 h-4" />
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Team Members</h1>
            <p className="text-muted-foreground mt-1">{team.name}</p>
          </div>
        </div>

        {isOwnerOrAdmin && (
          <Button onClick={() => setShowInviteDialog(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Invite Member
          </Button>
        )}
      </div>

      {/* Members Table */}
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Member</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Joined</TableHead>
              {isOwnerOrAdmin && <TableHead className="w-[70px]"></TableHead>}
            </TableRow>
          </TableHeader>
          <TableBody>
            {team.members.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center py-8">
                  <p className="text-muted-foreground">
                    No members yet. Invite members to start collaborating.
                  </p>
                </TableCell>
              </TableRow>
            ) : (
              team.members.map((member) => (
                <TableRow key={member.id}>
                  {/* Member Info */}
                  <TableCell>
                    <div className="flex items-center gap-3">
                      <Avatar className="h-8 w-8">
                        <AvatarImage src={member.user?.avatar_url} />
                        <AvatarFallback>
                          {member.user?.full_name?.[0] ||
                            member.user?.email[0] ||
                            "?"}
                        </AvatarFallback>
                      </Avatar>
                      <div className="min-w-0">
                        <p className="text-sm font-medium truncate">
                          {member.user?.full_name || member.user?.email}
                        </p>
                        <p className="text-xs text-muted-foreground truncate">
                          {member.user?.email}
                        </p>
                      </div>
                    </div>
                  </TableCell>

                  {/* Member Type */}
                  <TableCell>
                    <Badge
                      variant={
                        member.member_type === "ai_agent"
                          ? "secondary"
                          : "outline"
                      }
                    >
                      {member.member_type === "ai_agent"
                        ? "AI Agent"
                        : "Human"}
                    </Badge>
                  </TableCell>

                  {/* Role */}
                  <TableCell>
                    {isOwnerOrAdmin && member.role !== "owner" ? (
                      <Select
                        value={member.role}
                        onValueChange={(newRole) =>
                          handleRoleChange(member.user_id, newRole as TeamRole)
                        }
                        disabled={member.member_type === "ai_agent"}
                      >
                        <SelectTrigger className="w-[120px]">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="member">Member</SelectItem>
                          <SelectItem
                            value="admin"
                            disabled={member.member_type === "ai_agent"}
                          >
                            Admin
                          </SelectItem>
                        </SelectContent>
                      </Select>
                    ) : (
                      <Badge
                        variant={
                          member.role === "owner" ? "default" : "outline"
                        }
                      >
                        {member.role}
                      </Badge>
                    )}
                  </TableCell>

                  {/* Joined Date */}
                  <TableCell className="text-sm text-muted-foreground">
                    {new Date(member.joined_at).toLocaleDateString()}
                  </TableCell>

                  {/* Actions */}
                  {isOwnerOrAdmin && (
                    <TableCell>
                      {member.role !== "owner" && (
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="icon">
                              <MoreHorizontal className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuLabel>Actions</DropdownMenuLabel>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                              className="text-destructive"
                              onClick={() => setMemberToRemove(member.user_id)}
                            >
                              Remove member
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      )}
                    </TableCell>
                  )}
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Invite Member Dialog */}
      <InviteMemberDialog
        teamId={teamId || ""}
        open={showInviteDialog}
        onOpenChange={setShowInviteDialog}
      />

      {/* Remove Member Confirmation */}
      <AlertDialog
        open={!!memberToRemove}
        onOpenChange={(open) => !open && setMemberToRemove(null)}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Remove member?</AlertDialogTitle>
            <AlertDialogDescription>
              This member will lose access to all team projects and resources.
              This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleRemoveMember}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Remove
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}

/**
 * Loading Skeleton
 */
function MembersPageSkeleton() {
  return (
    <div className="container mx-auto py-6 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Skeleton className="h-10 w-10" />
          <div className="space-y-2">
            <Skeleton className="h-8 w-48" />
            <Skeleton className="h-4 w-32" />
          </div>
        </div>
        <Skeleton className="h-10 w-32" />
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Member</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Joined</TableHead>
              <TableHead className="w-[70px]"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {[1, 2, 3].map((i) => (
              <TableRow key={i}>
                <TableCell>
                  <div className="flex items-center gap-3">
                    <Skeleton className="h-8 w-8 rounded-full" />
                    <div className="space-y-1">
                      <Skeleton className="h-4 w-32" />
                      <Skeleton className="h-3 w-40" />
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <Skeleton className="h-5 w-16" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-5 w-20" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-4 w-24" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-8 w-8" />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
