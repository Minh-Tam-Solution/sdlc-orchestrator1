/**
 * =========================================================================
 * CreateSprintDialog - Create New Sprint Dialog
 * SDLC Orchestrator - Sprint 75 Day 4
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 75 Sprint Dashboard UI
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - Create new sprint with required fields
 * - Auto-generate sprint number (immutable per Rule #1)
 * - Set sprint goal, dates, and capacity
 *
 * SDLC 5.1.3 Compliance:
 * - Rule #1: Sprint number auto-generated, immutable
 * - G-Sprint gate: Created with pending status
 * =========================================================================
 */

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Calendar, Target, Users, FileText } from "lucide-react";
import { useCreateSprint, CreateSprintData } from "@/hooks/usePlanning";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

/**
 * Form validation schema
 */
const createSprintSchema = z.object({
  name: z
    .string()
    .min(1, "Sprint name is required")
    .max(255, "Sprint name must be less than 255 characters"),
  goal: z
    .string()
    .max(2000, "Goal must be less than 2000 characters")
    .optional(),
  start_date: z.string().optional(),
  end_date: z.string().optional(),
  capacity_points: z.coerce
    .number()
    .min(0, "Capacity must be positive")
    .max(1000, "Capacity seems too high")
    .optional(),
  team_size: z.coerce
    .number()
    .min(1, "Team size must be at least 1")
    .max(100, "Team size seems too high")
    .optional(),
});

type CreateSprintFormData = z.infer<typeof createSprintSchema>;

/**
 * CreateSprintDialog Props
 */
interface CreateSprintDialogProps {
  projectId: string;
  phaseId?: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

/**
 * CreateSprintDialog Component
 * Dialog for creating a new sprint
 */
export default function CreateSprintDialog({
  projectId,
  phaseId,
  open,
  onOpenChange,
}: CreateSprintDialogProps) {
  const createSprint = useCreateSprint();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CreateSprintFormData>({
    resolver: zodResolver(createSprintSchema),
    defaultValues: {
      name: "",
      goal: "",
      capacity_points: 40,
      team_size: 5,
    },
  });

  /**
   * Handle form submission
   */
  const onSubmit = async (data: CreateSprintFormData) => {
    setIsSubmitting(true);

    try {
      const sprintData: CreateSprintData = {
        project_id: projectId,
        phase_id: phaseId,
        name: data.name,
        goal: data.goal || undefined,
        start_date: data.start_date || undefined,
        end_date: data.end_date || undefined,
        capacity_points: data.capacity_points || undefined,
        team_size: data.team_size || undefined,
      };

      await createSprint.mutateAsync(sprintData);

      // Reset form and close dialog
      reset();
      onOpenChange(false);
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * Handle dialog close
   */
  const handleClose = () => {
    if (!isSubmitting) {
      reset();
      onOpenChange(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Create New Sprint</DialogTitle>
          <DialogDescription>
            Create a new sprint for your project. Sprint numbers are
            auto-generated and immutable (SDLC 5.1.3 Rule #1).
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {/* Sprint Name */}
          <div className="space-y-2">
            <Label htmlFor="name" className="flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Sprint Name *
            </Label>
            <Input
              id="name"
              placeholder="e.g., Sprint 75 - Planning API Validation"
              {...register("name")}
              disabled={isSubmitting}
            />
            {errors.name && (
              <p className="text-sm text-destructive">{errors.name.message}</p>
            )}
          </div>

          {/* Sprint Goal */}
          <div className="space-y-2">
            <Label htmlFor="goal" className="flex items-center gap-2">
              <Target className="w-4 h-4" />
              Sprint Goal
            </Label>
            <Textarea
              id="goal"
              placeholder="What is the main objective of this sprint?"
              rows={3}
              {...register("goal")}
              disabled={isSubmitting}
            />
            {errors.goal && (
              <p className="text-sm text-destructive">{errors.goal.message}</p>
            )}
            <p className="text-xs text-muted-foreground">
              A clear goal helps the team focus on what matters most.
            </p>
          </div>

          {/* Date Range */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="start_date" className="flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                Start Date
              </Label>
              <Input
                id="start_date"
                type="date"
                {...register("start_date")}
                disabled={isSubmitting}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="end_date">End Date</Label>
              <Input
                id="end_date"
                type="date"
                {...register("end_date")}
                disabled={isSubmitting}
              />
            </div>
          </div>

          {/* Capacity and Team Size */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label
                htmlFor="capacity_points"
                className="flex items-center gap-2"
              >
                <Target className="w-4 h-4" />
                Capacity (SP)
              </Label>
              <Input
                id="capacity_points"
                type="number"
                min={0}
                max={1000}
                {...register("capacity_points")}
                disabled={isSubmitting}
              />
              {errors.capacity_points && (
                <p className="text-sm text-destructive">
                  {errors.capacity_points.message}
                </p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="team_size" className="flex items-center gap-2">
                <Users className="w-4 h-4" />
                Team Size
              </Label>
              <Input
                id="team_size"
                type="number"
                min={1}
                max={100}
                {...register("team_size")}
                disabled={isSubmitting}
              />
              {errors.team_size && (
                <p className="text-sm text-destructive">
                  {errors.team_size.message}
                </p>
              )}
            </div>
          </div>

          {/* G-Sprint Gate Info */}
          <div className="rounded-md bg-muted p-3 text-sm">
            <p className="font-medium mb-1">G-Sprint Gate Required</p>
            <p className="text-muted-foreground">
              After creation, you&apos;ll need G-Sprint gate approval (by team
              admin/owner) before the sprint can start. This ensures proper
              planning per SDLC 5.1.3.
            </p>
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Creating..." : "Create Sprint"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
