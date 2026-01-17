/**
 * =========================================================================
 * CreateTeamDialog - Team Creation Modal
 * SDLC Orchestrator - Sprint 72 Day 2
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Status: ACTIVE - Sprint 72 Teams Frontend
 * Authority: Frontend Lead + CTO Approved
 *
 * Purpose:
 * - Form to create new teams
 * - Validates team name and slug
 * - Auto-generates slug from name
 * - Assigns creator as team owner
 * =========================================================================
 */

import { useState, useEffect } from "react";
import { useCreateTeam } from "@/hooks/useTeams";
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
import { Textarea } from "@/components/ui/textarea";
import { Loader2 } from "lucide-react";

interface CreateTeamDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

/**
 * Create Team Dialog Component
 * Modal form for creating a new team
 */
export default function CreateTeamDialog({
  open,
  onOpenChange,
}: CreateTeamDialogProps) {
  const createTeam = useCreateTeam();

  // Form state
  const [name, setName] = useState("");
  const [slug, setSlug] = useState("");
  const [description, setDescription] = useState("");
  const [slugTouched, setSlugTouched] = useState(false);

  // Auto-generate slug from name if not manually edited
  useEffect(() => {
    if (!slugTouched && name) {
      const autoSlug = name
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "");
      setSlug(autoSlug);
    }
  }, [name, slugTouched]);

  // Reset form when dialog closes
  useEffect(() => {
    if (!open) {
      setName("");
      setSlug("");
      setDescription("");
      setSlugTouched(false);
    }
  }, [open]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name || !slug) {
      return;
    }

    // TODO: Get organization_id from user context/store
    const mockOrgId = "00000000-0000-0000-0000-000000000001";

    try {
      await createTeam.mutateAsync({
        name,
        slug,
        description: description || undefined,
        organization_id: mockOrgId,
      });

      onOpenChange(false);
    } catch (error) {
      // Error is handled by the mutation's onError
      console.error("Failed to create team:", error);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Create Team</DialogTitle>
            <DialogDescription>
              Create a new team to organize projects and manage member access.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-4">
            {/* Team Name */}
            <div className="space-y-2">
              <Label htmlFor="name">
                Team Name <span className="text-destructive">*</span>
              </Label>
              <Input
                id="name"
                placeholder="Engineering"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                autoFocus
              />
            </div>

            {/* Team Slug */}
            <div className="space-y-2">
              <Label htmlFor="slug">
                Team Slug <span className="text-destructive">*</span>
              </Label>
              <Input
                id="slug"
                placeholder="engineering"
                value={slug}
                onChange={(e) => {
                  setSlug(e.target.value);
                  setSlugTouched(true);
                }}
                required
                pattern="[a-z0-9-]+"
                title="Lowercase letters, numbers, and hyphens only"
              />
              <p className="text-xs text-muted-foreground">
                Used in URLs. Lowercase letters, numbers, and hyphens only.
              </p>
            </div>

            {/* Description */}
            <div className="space-y-2">
              <Label htmlFor="description">Description (optional)</Label>
              <Textarea
                id="description"
                placeholder="Optional team description..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
              />
            </div>
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={createTeam.isPending}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={createTeam.isPending}>
              {createTeam.isPending && (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              )}
              Create Team
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
