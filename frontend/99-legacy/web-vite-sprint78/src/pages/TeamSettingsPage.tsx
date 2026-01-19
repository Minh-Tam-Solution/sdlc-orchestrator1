/**
 * =========================================================================
 * TeamSettingsPage - Team Configuration and Management
 * SDLC Orchestrator - Sprint 72 Day 4
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Status: ACTIVE - Sprint 72 Teams Frontend
 * Authority: Frontend Lead + CTO Approved
 *
 * Purpose:
 * - Edit team name and description
 * - Delete team (danger zone)
 * - Only accessible by owners/admins
 *
 * SASE Compliance:
 * - Only SE4H (Human Coach) owners/admins can access
 * =========================================================================
 */

import { useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { ArrowLeft, Loader2, AlertTriangle } from "lucide-react";
import { useTeam, useUpdateTeam, useDeleteTeam } from "@/hooks/useTeams";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
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
import { Skeleton } from "@/components/ui/skeleton";

/**
 * Team Settings Page
 */
export default function TeamSettingsPage() {
  const { teamId } = useParams<{ teamId: string }>();
  const navigate = useNavigate();
  const { data: team, isLoading } = useTeam(teamId || null);
  const updateTeam = useUpdateTeam(teamId || "");
  const deleteTeam = useDeleteTeam();

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [deleteConfirmation, setDeleteConfirmation] = useState("");

  // Initialize form when team loads
  useState(() => {
    if (team) {
      setName(team.name);
      setDescription(team.description || "");
    }
  });

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name) return;

    try {
      await updateTeam.mutateAsync({
        name,
        description: description || undefined,
      });
    } catch (error) {
      console.error("Failed to update team:", error);
    }
  };

  const handleDelete = async () => {
    if (!teamId || deleteConfirmation !== team?.name) return;

    try {
      await deleteTeam.mutateAsync(teamId);
      navigate("/teams");
    } catch (error) {
      console.error("Failed to delete team:", error);
    }
  };

  if (isLoading) {
    return <SettingsPageSkeleton />;
  }

  if (!team) {
    return (
      <div className="container mx-auto py-6">
        <p>Team not found</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-6 max-w-3xl space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link to={`/teams/${teamId}`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="w-4 h-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Team Settings</h1>
          <p className="text-muted-foreground mt-1">{team.name}</p>
        </div>
      </div>

      {/* General Settings */}
      <Card>
        <CardHeader>
          <CardTitle>General</CardTitle>
          <CardDescription>
            Update your team's name and description
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSave} className="space-y-4">
            {/* Team Name */}
            <div className="space-y-2">
              <Label htmlFor="name">
                Team Name <span className="text-destructive">*</span>
              </Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            {/* Team Slug (read-only) */}
            <div className="space-y-2">
              <Label htmlFor="slug">Team Slug</Label>
              <Input id="slug" value={team.slug} disabled />
              <p className="text-xs text-muted-foreground">
                Slug cannot be changed after creation
              </p>
            </div>

            {/* Description */}
            <div className="space-y-2">
              <Label htmlFor="description">Description (optional)</Label>
              <Textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
              />
            </div>

            {/* Save Button */}
            <div className="flex justify-end">
              <Button type="submit" disabled={updateTeam.isPending}>
                {updateTeam.isPending && (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                )}
                Save Changes
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Danger Zone */}
      <Card className="border-destructive">
        <CardHeader>
          <CardTitle className="text-destructive flex items-center gap-2">
            <AlertTriangle className="w-5 h-5" />
            Danger Zone
          </CardTitle>
          <CardDescription>
            Irreversible and destructive actions
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <h4 className="text-sm font-medium">Delete this team</h4>
              <p className="text-sm text-muted-foreground">
                Once you delete a team, there is no going back. All projects
                will be unassigned from this team.
              </p>
            </div>
            <Button
              variant="destructive"
              onClick={() => setShowDeleteDialog(true)}
            >
              Delete Team
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete team?</AlertDialogTitle>
            <AlertDialogDescription asChild>
              <div className="space-y-3">
                <p>
                  This action <strong>cannot be undone</strong>. This will
                  permanently delete the team and unassign all projects.
                </p>
                <div className="space-y-2">
                  <Label htmlFor="confirm">
                    Type <strong>{team.name}</strong> to confirm
                  </Label>
                  <Input
                    id="confirm"
                    value={deleteConfirmation}
                    onChange={(e) => setDeleteConfirmation(e.target.value)}
                    placeholder={team.name}
                  />
                </div>
              </div>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel onClick={() => setDeleteConfirmation("")}>
              Cancel
            </AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDelete}
              disabled={
                deleteConfirmation !== team.name || deleteTeam.isPending
              }
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              {deleteTeam.isPending && (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              )}
              Delete Team
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
function SettingsPageSkeleton() {
  return (
    <div className="container mx-auto py-6 max-w-3xl space-y-6">
      <div className="flex items-center gap-4">
        <Skeleton className="h-10 w-10" />
        <div className="space-y-2">
          <Skeleton className="h-8 w-48" />
          <Skeleton className="h-4 w-32" />
        </div>
      </div>

      <Card>
        <CardHeader>
          <Skeleton className="h-6 w-32 mb-2" />
          <Skeleton className="h-4 w-64" />
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Skeleton className="h-4 w-20" />
            <Skeleton className="h-10 w-full" />
          </div>
          <div className="space-y-2">
            <Skeleton className="h-4 w-20" />
            <Skeleton className="h-10 w-full" />
          </div>
          <div className="space-y-2">
            <Skeleton className="h-4 w-32" />
            <Skeleton className="h-24 w-full" />
          </div>
          <div className="flex justify-end">
            <Skeleton className="h-10 w-32" />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <Skeleton className="h-6 w-32 mb-2" />
          <Skeleton className="h-4 w-48" />
        </CardHeader>
        <CardContent>
          <Skeleton className="h-20 w-full" />
        </CardContent>
      </Card>
    </div>
  );
}
