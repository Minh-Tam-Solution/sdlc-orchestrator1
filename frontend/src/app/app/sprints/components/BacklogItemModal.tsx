/**
 * Backlog Item Modal Component - SDLC Orchestrator
 *
 * @module frontend/src/app/app/sprints/components/BacklogItemModal
 * @description Modal dialog for creating and editing backlog items
 * @sdlc SDLC 6.0.6 Framework - Sprint 93 (Planning Hierarchy Part 2)
 * @reference SDLC 6.0.6 Pillar 2: Sprint Planning Governance
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
import type {
  BacklogItem,
  BacklogItemInput,
  BacklogItemUpdateInput,
  BacklogItemType,
  BacklogItemPriority,
  BacklogItemStatus,
} from "@/lib/types/planning";

// =============================================================================
// TYPES
// =============================================================================

interface BacklogItemModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: BacklogItemInput | BacklogItemUpdateInput) => Promise<void>;
  item?: BacklogItem | null;
  projectId: string;
  sprintId?: string | null;
  sprintName?: string;
  mode: "create" | "edit";
  isLoading?: boolean;
}

interface FormData {
  title: string;
  description: string;
  type: BacklogItemType;
  priority: BacklogItemPriority;
  status: BacklogItemStatus;
  story_points: number | null;
  estimated_hours: number | null;
  actual_hours: number | null;
  assignee_id: string;
  labels: string;
  acceptance_criteria: string;
}

interface FormErrors {
  title?: string;
  description?: string;
  type?: string;
  priority?: string;
  story_points?: string;
  estimated_hours?: string;
  actual_hours?: string;
  acceptance_criteria?: string;
}

// =============================================================================
// CONSTANTS
// =============================================================================

const ITEM_TYPES: { value: BacklogItemType; label: string; icon: string }[] = [
  { value: "story", label: "User Story", icon: "📖" },
  { value: "task", label: "Technical Task", icon: "✅" },
  { value: "bug", label: "Bug Fix", icon: "🐛" },
  { value: "spike", label: "Research Spike", icon: "🔬" },
];

const PRIORITIES: { value: BacklogItemPriority; label: string; description: string }[] = [
  { value: "p0", label: "P0 - Critical", description: "Must complete this sprint" },
  { value: "p1", label: "P1 - High", description: "Should complete this sprint" },
  { value: "p2", label: "P2 - Medium", description: "Nice to have" },
  { value: "p3", label: "P3 - Low", description: "Can defer" },
];

const STATUSES: { value: BacklogItemStatus; label: string }[] = [
  { value: "todo", label: "To Do" },
  { value: "in_progress", label: "In Progress" },
  { value: "review", label: "In Review" },
  { value: "done", label: "Done" },
  { value: "carried_over", label: "Carried Over" },
];

const STORY_POINTS = [0, 1, 2, 3, 5, 8, 13, 21];

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Get default form data for create mode
 */
function getDefaultFormData(): FormData {
  return {
    title: "",
    description: "",
    type: "story",
    priority: "p2",
    status: "todo",
    story_points: null,
    estimated_hours: null,
    actual_hours: null,
    assignee_id: "",
    labels: "",
    acceptance_criteria: "",
  };
}

/**
 * Convert BacklogItem to FormData
 */
function itemToFormData(item: BacklogItem): FormData {
  return {
    title: item.title,
    description: item.description || "",
    type: item.type,
    priority: item.priority,
    status: item.status,
    story_points: item.story_points,
    estimated_hours: item.estimated_hours,
    actual_hours: item.actual_hours,
    assignee_id: item.assignee_id || "",
    labels: item.labels.join(", "),
    acceptance_criteria: item.acceptance_criteria || "",
  };
}

/**
 * Parse labels string to array
 */
function parseLabels(labelsString: string): string[] {
  return labelsString
    .split(",")
    .map((label) => label.trim())
    .filter((label) => label.length > 0);
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function BacklogItemModal({
  open,
  onClose,
  onSubmit,
  item,
  projectId,
  sprintId,
  sprintName,
  mode,
  isLoading = false,
}: BacklogItemModalProps) {
  const isEdit = mode === "edit";

  // Form state
  const [formData, setFormData] = useState<FormData>(getDefaultFormData());
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Initialize form when item changes
  useEffect(() => {
    if (isEdit && item) {
      setFormData(itemToFormData(item));
    } else if (!isEdit) {
      setFormData(getDefaultFormData());
    }
    setErrors({});
  }, [item, isEdit, open]);

  // Handle input changes
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;

    setFormData((prev) => {
      const newData = { ...prev };

      if (name === "story_points") {
        newData.story_points = value === "" ? null : parseInt(value, 10);
      } else if (name === "estimated_hours") {
        newData.estimated_hours = value === "" ? null : parseFloat(value);
      } else if (name === "actual_hours") {
        newData.actual_hours = value === "" ? null : parseFloat(value);
      } else if (name === "type") {
        newData.type = value as BacklogItemType;
      } else if (name === "priority") {
        newData.priority = value as BacklogItemPriority;
      } else if (name === "status") {
        newData.status = value as BacklogItemStatus;
      } else if (name === "title") {
        newData.title = value;
      } else if (name === "description") {
        newData.description = value;
      } else if (name === "assignee_id") {
        newData.assignee_id = value;
      } else if (name === "labels") {
        newData.labels = value;
      } else if (name === "acceptance_criteria") {
        newData.acceptance_criteria = value;
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

    if (!formData.title.trim()) {
      newErrors.title = "Title is required";
    } else if (formData.title.length > 200) {
      newErrors.title = "Title must be less than 200 characters";
    }

    if (formData.description && formData.description.length > 2000) {
      newErrors.description = "Description must be less than 2000 characters";
    }

    if (formData.story_points !== null && (formData.story_points < 0 || formData.story_points > 100)) {
      newErrors.story_points = "Story points must be between 0 and 100";
    }

    if (formData.estimated_hours !== null && formData.estimated_hours < 0) {
      newErrors.estimated_hours = "Estimated hours cannot be negative";
    }

    if (formData.actual_hours !== null && formData.actual_hours < 0) {
      newErrors.actual_hours = "Actual hours cannot be negative";
    }

    if (formData.acceptance_criteria && formData.acceptance_criteria.length > 2000) {
      newErrors.acceptance_criteria = "Acceptance criteria must be less than 2000 characters";
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
      const labels = parseLabels(formData.labels);

      if (isEdit) {
        const updateData: BacklogItemUpdateInput = {
          title: formData.title,
          description: formData.description || undefined,
          type: formData.type,
          priority: formData.priority,
          status: formData.status,
          story_points: formData.story_points ?? undefined,
          estimated_hours: formData.estimated_hours ?? undefined,
          actual_hours: formData.actual_hours ?? undefined,
          assignee_id: formData.assignee_id || undefined,
          labels: labels.length > 0 ? labels : undefined,
          acceptance_criteria: formData.acceptance_criteria || undefined,
        };
        await onSubmit(updateData);
      } else {
        const createData: BacklogItemInput = {
          title: formData.title,
          description: formData.description || undefined,
          project_id: projectId,
          sprint_id: sprintId || undefined,
          type: formData.type,
          priority: formData.priority,
          story_points: formData.story_points ?? undefined,
          estimated_hours: formData.estimated_hours ?? undefined,
          assignee_id: formData.assignee_id || undefined,
          labels: labels.length > 0 ? labels : undefined,
          acceptance_criteria: formData.acceptance_criteria || undefined,
        };
        await onSubmit(createData);
      }
      onClose();
    } catch (error) {
      console.error("Failed to save backlog item:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {isEdit ? "Edit Backlog Item" : "Create Backlog Item"}
          </DialogTitle>
          <DialogDescription>
            {isEdit
              ? "Update the backlog item details below."
              : sprintName
              ? `Add a new item to sprint "${sprintName}".`
              : "Add a new item to the product backlog."}
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Type Selection */}
          <div className="space-y-2">
            <Label>Item Type <span className="text-red-500">*</span></Label>
            <div className="grid grid-cols-4 gap-2">
              {ITEM_TYPES.map((type) => (
                <button
                  key={type.value}
                  type="button"
                  onClick={() => setFormData((prev) => ({ ...prev, type: type.value }))}
                  className={`
                    flex flex-col items-center justify-center rounded-lg border-2 p-3 transition-colors
                    ${formData.type === type.value
                      ? "border-blue-500 bg-blue-50"
                      : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                    }
                  `}
                >
                  <span className="text-xl">{type.icon}</span>
                  <span className="mt-1 text-xs font-medium">{type.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Title */}
          <div className="space-y-2">
            <Label htmlFor="title">
              Title <span className="text-red-500">*</span>
            </Label>
            <Input
              id="title"
              name="title"
              placeholder="e.g., Implement user authentication flow"
              value={formData.title}
              onChange={handleChange}
              className={errors.title ? "border-red-500" : ""}
            />
            {errors.title && (
              <p className="text-xs text-red-500">{errors.title}</p>
            )}
          </div>

          {/* Description */}
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              name="description"
              placeholder="Detailed description of the work to be done..."
              value={formData.description}
              onChange={handleChange}
              rows={3}
              className={errors.description ? "border-red-500" : ""}
            />
            {errors.description && (
              <p className="text-xs text-red-500">{errors.description}</p>
            )}
            <p className="text-xs text-gray-500">
              {formData.description.length}/2000 characters
            </p>
          </div>

          {/* Priority & Status Row */}
          <div className="grid grid-cols-2 gap-4">
            {/* Priority */}
            <div className="space-y-2">
              <Label htmlFor="priority">Priority <span className="text-red-500">*</span></Label>
              <select
                id="priority"
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                {PRIORITIES.map((p) => (
                  <option key={p.value} value={p.value}>
                    {p.label}
                  </option>
                ))}
              </select>
              <p className="text-xs text-gray-500">
                {PRIORITIES.find((p) => p.value === formData.priority)?.description}
              </p>
            </div>

            {/* Status (only in edit mode) */}
            {isEdit && (
              <div className="space-y-2">
                <Label htmlFor="status">Status</Label>
                <select
                  id="status"
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  {STATUSES.map((s) => (
                    <option key={s.value} value={s.value}>
                      {s.label}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>

          {/* Story Points & Hours Row */}
          <div className="grid grid-cols-3 gap-4">
            {/* Story Points */}
            <div className="space-y-2">
              <Label htmlFor="story_points">Story Points</Label>
              <select
                id="story_points"
                name="story_points"
                value={formData.story_points ?? ""}
                onChange={handleChange}
                className={`w-full rounded-md border px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 ${
                  errors.story_points ? "border-red-500" : "border-gray-300"
                }`}
              >
                <option value="">Not estimated</option>
                {STORY_POINTS.map((sp) => (
                  <option key={sp} value={sp}>
                    {sp} SP
                  </option>
                ))}
              </select>
              {errors.story_points && (
                <p className="text-xs text-red-500">{errors.story_points}</p>
              )}
            </div>

            {/* Estimated Hours */}
            <div className="space-y-2">
              <Label htmlFor="estimated_hours">Est. Hours</Label>
              <Input
                id="estimated_hours"
                name="estimated_hours"
                type="number"
                min={0}
                step={0.5}
                placeholder="e.g., 4"
                value={formData.estimated_hours ?? ""}
                onChange={handleChange}
                className={errors.estimated_hours ? "border-red-500" : ""}
              />
              {errors.estimated_hours && (
                <p className="text-xs text-red-500">{errors.estimated_hours}</p>
              )}
            </div>

            {/* Actual Hours (only in edit mode) */}
            {isEdit && (
              <div className="space-y-2">
                <Label htmlFor="actual_hours">Actual Hours</Label>
                <Input
                  id="actual_hours"
                  name="actual_hours"
                  type="number"
                  min={0}
                  step={0.5}
                  placeholder="e.g., 6"
                  value={formData.actual_hours ?? ""}
                  onChange={handleChange}
                  className={errors.actual_hours ? "border-red-500" : ""}
                />
                {errors.actual_hours && (
                  <p className="text-xs text-red-500">{errors.actual_hours}</p>
                )}
              </div>
            )}
          </div>

          {/* Labels */}
          <div className="space-y-2">
            <Label htmlFor="labels">Labels</Label>
            <Input
              id="labels"
              name="labels"
              placeholder="e.g., frontend, authentication, ui (comma-separated)"
              value={formData.labels}
              onChange={handleChange}
            />
            <p className="text-xs text-gray-500">
              Separate multiple labels with commas
            </p>
          </div>

          {/* Acceptance Criteria */}
          <div className="space-y-2">
            <Label htmlFor="acceptance_criteria">Acceptance Criteria</Label>
            <Textarea
              id="acceptance_criteria"
              name="acceptance_criteria"
              placeholder={`Given [context]
When [action]
Then [expected result]

- [ ] Criteria 1
- [ ] Criteria 2`}
              value={formData.acceptance_criteria}
              onChange={handleChange}
              rows={4}
              className={`font-mono text-sm ${errors.acceptance_criteria ? "border-red-500" : ""}`}
            />
            {errors.acceptance_criteria && (
              <p className="text-xs text-red-500">{errors.acceptance_criteria}</p>
            )}
            <p className="text-xs text-gray-500">
              {formData.acceptance_criteria.length}/2000 characters
            </p>
          </div>

          {/* SDLC 6.0.6 Info */}
          <div className="rounded-md border border-gray-200 bg-gray-50 p-3 text-xs text-gray-600">
            <p className="font-medium text-gray-700">SDLC 6.0.6 Guidelines:</p>
            <ul className="mt-1 list-inside list-disc space-y-1">
              <li>P0 items must be addressed within the current sprint</li>
              <li>Story points should follow Fibonacci sequence (1, 2, 3, 5, 8, 13)</li>
              <li>Items {">"} 8 SP should be broken down into smaller tasks</li>
              <li>Acceptance criteria enable G-Sprint-Close validation</li>
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
                <>{isEdit ? "Update Item" : "Create Item"}</>
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

export default BacklogItemModal;
