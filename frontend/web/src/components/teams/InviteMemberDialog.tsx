/**
 * =========================================================================
 * InviteMemberDialog - Member Invitation Modal
 * SDLC Orchestrator - Sprint 72 Day 4
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Status: ACTIVE - Sprint 72 Teams Frontend
 * Authority: Frontend Lead + CTO Approved
 *
 * Purpose:
 * - Form to invite new members to team
 * - Select member role and type
 * - SASE compliance validation
 *
 * CTO R1/R2 Enforcement:
 * - AI agents cannot be owner/admin
 * =========================================================================
 */

import { useState, useEffect } from "react";
import { useAddTeamMember, TeamRole, MemberType } from "@/hooks/useTeams";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";

interface InviteMemberDialogProps {
  teamId: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

/**
 * Invite Member Dialog Component
 */
export default function InviteMemberDialog({
  teamId,
  open,
  onOpenChange,
}: InviteMemberDialogProps) {
  const addMember = useAddTeamMember(teamId);

  // Form state
  const [userId, setUserId] = useState("");
  const [role, setRole] = useState<TeamRole>("member");
  const [memberType, setMemberType] = useState<MemberType>("human");

  // SASE compliance validation
  const isInvalidCombination =
    memberType === "ai_agent" && (role === "owner" || role === "admin");

  // Reset form when dialog closes
  useEffect(() => {
    if (!open) {
      setUserId("");
      setRole("member");
      setMemberType("human");
    }
  }, [open]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!userId || isInvalidCombination) {
      return;
    }

    try {
      await addMember.mutateAsync({
        user_id: userId,
        role,
        member_type: memberType,
      });

      onOpenChange(false);
    } catch (error) {
      console.error("Failed to add member:", error);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Invite Member</DialogTitle>
            <DialogDescription>
              Add a new member to your team. They'll get access to all team
              projects.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-4">
            {/* User ID */}
            <div className="space-y-2">
              <Label htmlFor="userId">
                User ID <span className="text-destructive">*</span>
              </Label>
              <Input
                id="userId"
                placeholder="00000000-0000-0000-0000-000000000000"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                required
                autoFocus
              />
              <p className="text-xs text-muted-foreground">
                Enter the user's UUID. In production, this would be a user
                search/autocomplete.
              </p>
            </div>

            {/* Member Type */}
            <div className="space-y-2">
              <Label htmlFor="memberType">Member Type</Label>
              <Select
                value={memberType}
                onValueChange={(value) => setMemberType(value as MemberType)}
              >
                <SelectTrigger id="memberType">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="human">
                    Human (SE4H - Agent Coach)
                  </SelectItem>
                  <SelectItem value="ai_agent">
                    AI Agent (SE4A - Agent Executor)
                  </SelectItem>
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground">
                SE4H (Human Coach) or SE4A (AI Agent) per SDLC 5.1.2
              </p>
            </div>

            {/* Role */}
            <div className="space-y-2">
              <Label htmlFor="role">Role</Label>
              <Select
                value={role}
                onValueChange={(value) => setRole(value as TeamRole)}
              >
                <SelectTrigger id="role">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="member">Member</SelectItem>
                  <SelectItem
                    value="admin"
                    disabled={memberType === "ai_agent"}
                  >
                    Admin
                  </SelectItem>
                  <SelectItem
                    value="owner"
                    disabled={memberType === "ai_agent"}
                  >
                    Owner
                  </SelectItem>
                </SelectContent>
              </Select>
              {memberType === "ai_agent" && (
                <p className="text-xs text-muted-foreground">
                  AI agents can only be members (CTO R1/R2)
                </p>
              )}
            </div>

            {/* SASE Compliance Warning */}
            {isInvalidCombination && (
              <Alert variant="destructive">
                <AlertDescription>
                  AI agents cannot be owners or admins (CTO R1/R2). Please
                  select "Member" role or change type to "Human".
                </AlertDescription>
              </Alert>
            )}
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={addMember.isPending}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={addMember.isPending || isInvalidCombination}
            >
              {addMember.isPending && (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              )}
              Invite Member
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
