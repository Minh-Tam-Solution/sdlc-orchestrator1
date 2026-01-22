/**
 * Sprint Modal Component - SDLC Orchestrator
 *
 * @module frontend/src/app/app/sprints/components/SprintModal
 * @description Modal dialog for creating and editing sprints
 * @sdlc SDLC 5.1.3 Framework - Sprint 93 (Planning Hierarchy Part 2)
 * @reference SDLC 5.1.3 Pillar 2: Sprint Planning Governance
 * @status Sprint 93 - Sprint CRUD & Charts
 */

"use client";

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import type { Sprint, SprintInput, SprintUpdateInput } from "@/lib/types/planning";

// =============================================================================
// TYPES
// =============================================================================

interface SprintModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: SprintInput | SprintUpdateInput) => Promise<void>;
  sprint?: Sprint | null;
  projectId: string;
  phaseId?: string;
  phaseName?: string;
  mode: "create" | "edit";
  isLoading?: boolean;
}

interface FormData {
  name: string;
  number: number;
  goal: string;
  start_date: string;
  end_date: string;
  team_capacity: number | null;
}

interface FormErrors {
  name?: string;
  number?: string;
  goal?: string;
  start_date?: string;
  end_date?: string;
  team_capacity?: string;
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Format date for input field (YYYY-MM-DD)
 */
function formatDateForInput(dateString?: string | null): string {
  if (!dateString) return "";
  const date = new Date(dateString);
  return date.toISOString().split("T")[0];
}

/**
 * Get default start date (today)
 */
function getDefaultStartDate(): string {
  return new Date().toISOString().split("T")[0];
}

/**
 * Get default end date (10 days from start)
 */
function getDefaultEndDate(startDate: string): string {
  const start = new Date(startDate);
  start.setDate(start.getDate() + 10);
  return start.toISOString().split("T")[0];
}

/**
 * Calculate sprint duration in days
 */
function calculateDuration(startDate: string, endDate: string): number {
  const start = new Date(startDate);
  const end = new Date(endDate);
  const diffTime = end.getTime() - start.getTime();
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function SprintModal({
  open,
  onClose,
  onSubmit,
  sprint,
  projectId,
  phaseId,
  phaseName,
  mode,
  isLoading = false,
}: SprintModalProps) {
  const isEdit = mode === "edit";

  // Form state
  const [formData, setFormData] = useState<FormData>({
    name: "",
    number: 1,
    goal: "",
    start_date: getDefaultStartDate(),
    end_date: getDefaultEndDate(getDefaultStartDate()),
    team_capacity: null,
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Initialize form when sprint changes
  useEffect(() => {
    if (isEdit && sprint) {
      setFormData({
        name: sprint.name,
        number: sprint.number,
        goal: sprint.goal,
        start_date: formatDateForInput(sprint.start_date),
        end_date: formatDateForInput(sprint.end_date),
        team_capacity: sprint.team_capacity,
      });
    } else if (!isEdit) {
      setFormData({
        name: "",
        number: 1,
        goal: "",
        start_date: getDefaultStartDate(),
        end_date: getDefaultEndDate(getDefaultStartDate()),
        team_capacity: null,
      });
    }
    setErrors({});
  }, [sprint, isEdit, open]);

  // Handle input changes
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;

    setFormData((prev) => {
      const newData = { ...prev };

      if (name === "number") {
        newData.number = value === "" ? 0 : parseInt(value, 10);
      } else if (name === "team_capacity") {
        newData.team_capacity = value === "" ? null : parseInt(value, 10);
      } else if (name === "name") {
        newData.name = value;
      } else if (name === "goal") {
        newData.goal = value;
      } else if (name === "start_date") {
        newData.start_date = value;
        // Auto-update end date when start date changes
        if (value) {
          newData.end_date = getDefaultEndDate(value);
        }
      } else if (name === "end_date") {
        newData.end_date = value;
      }

      return newData;
    });

    // Clear error when field is edited
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  // Validate form
  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = "Sprint name is required";
    } else if (formData.name.length > 100) {
      newErrors.name = "Sprint name must be less than 100 characters";
    }

    if (!formData.number || formData.number < 1) {
      newErrors.number = "Sprint number must be at least 1";
    }

    if (!formData.goal.trim()) {
      newErrors.goal = "Sprint goal is required";
    } else if (formData.goal.length > 500) {
      newErrors.goal = "Sprint goal must be less than 500 characters";
    }

    if (!formData.start_date) {
      newErrors.start_date = "Start date is required";
    }

    if (!formData.end_date) {
      newErrors.end_date = "End date is required";
    }

    if (formData.start_date && formData.end_date) {
      const duration = calculateDuration(formData.start_date, formData.end_date);
      if (duration < 5) {
        newErrors.end_date = "Sprint must be at least 5 days (SDLC 5.1.3)";
      } else if (duration > 14) {
        newErrors.end_date = "Sprint should not exceed 14 days (SDLC 5.1.3)";
      }
    }

    if (formData.team_capacity !== null && formData.team_capacity < 0) {
      newErrors.team_capacity = "Team capacity cannot be negative";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      if (isEdit) {
        const updateData: SprintUpdateInput = {
          name: formData.name,
          goal: formData.goal,
          start_date: formData.start_date,
          end_date: formData.end_date,
          team_capacity: formData.team_capacity ?? undefined,
        };
        await onSubmit(updateData);
      } else {
        const createData: SprintInput = {
          name: formData.name,
          number: formData.number,
          goal: formData.goal,
          project_id: projectId,
          phase_id: phaseId,
          start_date: formData.start_date,
          end_date: formData.end_date,
          team_capacity: formData.team_capacity ?? undefined,
        };
        await onSubmit(createData);
      }
      onClose();
    } catch (error) {
      console.error("Failed to save sprint:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const duration = formData.start_date && formData.end_date
    ? calculateDuration(formData.start_date, formData.end_date)
    : 0;

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>
            {isEdit ? "Edit Sprint" : "Create New Sprint"}
          </DialogTitle>
          <DialogDescription>
            {isEdit
              ? "Update the sprint details below."
              : phaseName
              ? `Create a new sprint in phase "${phaseName}".`
              : "Create a new sprint for this project."}
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Sprint Number (Create only) */}
          {!isEdit && (
            <div className="space-y-2">
              <Label htmlFor="number">
                Sprint Number <span className="text-red-500">*</span>
              </Label>
              <Input
                id="number"
                name="number"
                type="number"
                min={1}
                value={formData.number || ""}
                onChange={handleChange}
                className={errors.number ? "border-red-500" : ""}
              />
              {errors.number && (
                <p className="text-xs text-red-500">{errors.number}</p>
              )}
            </div>
          )}

          {/* Sprint Name */}
          <div className="space-y-2">
            <Label htmlFor="name">
              Sprint Name <span className="text-red-500">*</span>
            </Label>
            <Input
              id="name"
              name="name"
              placeholder="e.g., Sprint 93 - Planning Hierarchy"
              value={formData.name}
              onChange={handleChange}
              className={errors.name ? "border-red-500" : ""}
            />
            {errors.name && (
              <p className="text-xs text-red-500">{errors.name}</p>
            )}
          </div>

          {/* Sprint Goal */}
          <div className="space-y-2">
            <Label htmlFor="goal">
              Sprint Goal <span className="text-red-500">*</span>
            </Label>
            <Textarea
              id="goal"
              name="goal"
              placeholder="What will the team commit to achieving this sprint?"
              value={formData.goal}
              onChange={handleChange}
              rows={3}
              className={errors.goal ? "border-red-500" : ""}
            />
            {errors.goal && (
              <p className="text-xs text-red-500">{errors.goal}</p>
            )}
            <p className="text-xs text-gray-500">
              {formData.goal.length}/500 characters
            </p>
          </div>

          {/* Date Range */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="start_date">
                Start Date <span className="text-red-500">*</span>
              </Label>
              <Input
                id="start_date"
                name="start_date"
                type="date"
                value={formData.start_date}
                onChange={handleChange}
                className={errors.start_date ? "border-red-500" : ""}
              />
              {errors.start_date && (
                <p className="text-xs text-red-500">{errors.start_date}</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="end_date">
                End Date <span className="text-red-500">*</span>
              </Label>
              <Input
                id="end_date"
                name="end_date"
                type="date"
                value={formData.end_date}
                onChange={handleChange}
                min={formData.start_date}
                className={errors.end_date ? "border-red-500" : ""}
              />
              {errors.end_date && (
                <p className="text-xs text-red-500">{errors.end_date}</p>
              )}
            </div>
          </div>

          {/* Duration indicator */}
          {duration > 0 && (
            <div className="flex items-center gap-2 rounded-md bg-blue-50 px-3 py-2 text-sm">
              <svg className="h-4 w-4 text-blue-500" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
              <span className="text-blue-700">
                Duration: <strong>{duration} days</strong>
                {duration >= 5 && duration <= 10 && (
                  <span className="ml-1 text-green-600">(Recommended)</span>
                )}
              </span>
            </div>
          )}

          {/* Team Capacity */}
          <div className="space-y-2">
            <Label htmlFor="team_capacity">
              Team Capacity (Story Points)
            </Label>
            <Input
              id="team_capacity"
              name="team_capacity"
              type="number"
              min={0}
              placeholder="e.g., 40"
              value={formData.team_capacity ?? ""}
              onChange={handleChange}
              className={errors.team_capacity ? "border-red-500" : ""}
            />
            {errors.team_capacity && (
              <p className="text-xs text-red-500">{errors.team_capacity}</p>
            )}
            <p className="text-xs text-gray-500">
              Optional. Used for velocity calculation and sprint planning.
            </p>
          </div>

          {/* SDLC 5.1.3 Info */}
          <div className="rounded-md border border-gray-200 bg-gray-50 p-3 text-xs text-gray-600">
            <p className="font-medium text-gray-700">SDLC 5.1.3 Sprint Guidelines:</p>
            <ul className="mt-1 list-inside list-disc space-y-1">
              <li>Sprint duration: 5-10 days (max 14 days)</li>
              <li>G-Sprint gate required before starting</li>
              <li>G-Sprint-Close gate + 24h documentation window on close</li>
            </ul>
          </div>

          <DialogFooter className="gap-2 sm:gap-0">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              disabled={isSubmitting || isLoading}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={isSubmitting || isLoading}
            >
              {isSubmitting || isLoading ? (
                <>
                  <svg className="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  {isEdit ? "Updating..." : "Creating..."}
                </>
              ) : (
                <>{isEdit ? "Update Sprint" : "Create Sprint"}</>
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

export default SprintModal;
