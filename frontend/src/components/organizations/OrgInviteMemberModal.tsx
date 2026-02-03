"use client";

/**
 * Organization Invite Member Modal
 *
 * Sprint: 146 - Organization Access Control
 * Reference: ADR-047-Organization-Invitation-System.md
 *
 * Features:
 * - Send organization invitations (not team invitations)
 * - RBAC: Owner can invite admin/member, Admin can invite member only
 * - Rate limiting feedback (50/hour per org)
 * - SHA256 token security (handled by backend)
 */

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Textarea } from "@/components/ui/textarea";
import { useOrgInvitations } from "@/hooks/useOrgInvitations";

interface OrgInviteMemberModalProps {
  isOpen: boolean;
  onClose: () => void;
  organizationId: string;
  organizationName: string;
  /** Current user's role in the organization */
  currentUserRole: "owner" | "admin" | "member";
}

type OrgRole = "admin" | "member";

const ROLE_DESCRIPTIONS: Record<OrgRole, string> = {
  admin: "Manage organization members, teams, and settings",
  member: "Access organization teams and contribute",
};

export function OrgInviteMemberModal({
  isOpen,
  onClose,
  organizationId,
  organizationName,
  currentUserRole,
}: OrgInviteMemberModalProps) {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState<OrgRole>("member");
  const [message, setMessage] = useState("");
  const [error, setError] = useState<string | null>(null);
  const { sendInvitation, isSending } = useOrgInvitations(organizationId);

  // Only owner can invite admin
  const canInviteAdmin = currentUserRole === "owner";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
      setError("Please enter a valid email address");
      return;
    }

    // Role restriction check
    if (role === "admin" && !canInviteAdmin) {
      setError("Only organization owners can invite admins");
      return;
    }

    try {
      await sendInvitation({
        invited_email: email.trim().toLowerCase(),
        role,
        message: message.trim() || undefined,
      });

      // Success - close modal and reset form
      setEmail("");
      setRole("member");
      setMessage("");
      onClose();
    } catch (err: unknown) {
      const error = err as {
        response?: {
          status?: number;
          data?: {
            detail?: string | { message?: string }
          }
        }
      };

      // Handle specific error cases
      if (error.response?.status === 400) {
        const detail = error.response?.data?.detail;
        const errorMessage = typeof detail === "string"
          ? detail
          : detail?.message || "Invalid request";

        if (errorMessage.includes("already a member")) {
          setError(`${email} is already a member of ${organizationName}`);
        } else if (errorMessage.includes("pending invitation")) {
          setError(`An invitation has already been sent to ${email}`);
        } else {
          setError(errorMessage);
        }
      } else if (error.response?.status === 403) {
        const detail = error.response?.data?.detail;
        const errorMessage = typeof detail === "string"
          ? detail
          : detail?.message || "Permission denied";
        setError(errorMessage);
      } else if (error.response?.status === 409) {
        setError(`${email} is already a member of this organization`);
      } else if (error.response?.status === 429) {
        setError("Rate limit exceeded. Please try again in a few minutes.");
      } else {
        setError("Failed to send invitation. Please try again.");
      }
    }
  };

  const handleClose = () => {
    setEmail("");
    setRole("member");
    setMessage("");
    setError(null);
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Invite to {organizationName}</DialogTitle>
          <DialogDescription>
            Send an invitation to join your organization. They&apos;ll receive
            an email with a link to accept. The invitation expires in 7 days.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            {/* Email Input */}
            <div className="grid gap-2">
              <Label htmlFor="org-email">Email Address</Label>
              <Input
                id="org-email"
                type="email"
                placeholder="colleague@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={isSending}
                autoFocus
                required
              />
            </div>

            {/* Role Selection */}
            <div className="grid gap-2">
              <Label htmlFor="org-role">Role</Label>
              <Select
                value={role}
                onValueChange={(value) => setRole(value as OrgRole)}
                disabled={isSending}
              >
                <SelectTrigger id="org-role">
                  <SelectValue placeholder="Select a role" />
                </SelectTrigger>
                <SelectContent>
                  {canInviteAdmin && (
                    <SelectItem value="admin">
                      <div className="flex flex-col items-start">
                        <div className="font-medium">Admin</div>
                        <div className="text-xs text-muted-foreground">
                          {ROLE_DESCRIPTIONS.admin}
                        </div>
                      </div>
                    </SelectItem>
                  )}
                  <SelectItem value="member">
                    <div className="flex flex-col items-start">
                      <div className="font-medium">Member</div>
                      <div className="text-xs text-muted-foreground">
                        {ROLE_DESCRIPTIONS.member}
                      </div>
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
              <p className="text-sm text-muted-foreground">
                {ROLE_DESCRIPTIONS[role]}
              </p>
              {!canInviteAdmin && (
                <p className="text-xs text-amber-600">
                  Only organization owners can invite admins.
                </p>
              )}
            </div>

            {/* Optional Message */}
            <div className="grid gap-2">
              <Label htmlFor="org-message">
                Personal Message <span className="text-muted-foreground">(optional)</span>
              </Label>
              <Textarea
                id="org-message"
                placeholder="Add a personal note to the invitation..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                disabled={isSending}
                rows={3}
                maxLength={500}
              />
              <p className="text-xs text-muted-foreground">
                {message.length}/500 characters
              </p>
            </div>

            {/* Error Alert */}
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              disabled={isSending}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isSending}>
              {isSending ? (
                <>
                  <svg
                    className="mr-2 h-4 w-4 animate-spin"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Sending...
                </>
              ) : (
                "Send Invitation"
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

export default OrgInviteMemberModal;
