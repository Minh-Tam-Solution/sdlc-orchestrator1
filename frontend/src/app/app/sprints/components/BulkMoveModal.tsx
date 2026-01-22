/**
 * Bulk Move Modal Component - SDLC Orchestrator
 *
 * @module frontend/src/app/app/sprints/components/BulkMoveModal
 * @description Modal dialog for moving multiple backlog items to a sprint
 * @sdlc SDLC 5.1.3 Framework - Sprint 93 (Planning Hierarchy Part 2)
 * @reference SDLC 5.1.3 Pillar 2: Sprint Planning Governance
 * @status Sprint 93 - Sprint CRUD & Charts
 */

"use client";

import { useState, useMemo } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import type { BacklogItem, Sprint, BacklogItemStatus } from "@/lib/types/planning";
import { getBacklogItemTypeIcon, getPriorityColor } from "@/lib/types/planning";

// =============================================================================
// TYPES
// =============================================================================

interface BulkMoveModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: { item_ids: string[]; target_sprint_id: string | null; target_status?: BacklogItemStatus }) => Promise<void>;
  selectedItems: BacklogItem[];
  sprints: Sprint[];
  currentSprintId?: string | null;
  isLoading?: boolean;
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Format sprint option label
 */
function formatSprintLabel(sprint: Sprint): string {
  const statusEmoji = {
    planned: "📋",
    active: "🏃",
    closing: "🔒",
    closed: "✅",
    cancelled: "❌",
  };
  return `${statusEmoji[sprint.status] || "📋"} Sprint ${sprint.number}: ${sprint.name}`;
}

/**
 * Get status label
 */
function getStatusLabel(status: BacklogItemStatus): string {
  const labels: Record<BacklogItemStatus, string> = {
    todo: "To Do",
    in_progress: "In Progress",
    review: "In Review",
    done: "Done",
    carried_over: "Carried Over",
  };
  return labels[status] || status;
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function BulkMoveModal({
  open,
  onClose,
  onSubmit,
  selectedItems,
  sprints,
  currentSprintId,
  isLoading = false,
}: BulkMoveModalProps) {
  const [targetSprintId, setTargetSprintId] = useState<string | null>(null);
  const [targetStatus, setTargetStatus] = useState<BacklogItemStatus | "keep">("keep");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Filter out closed/cancelled sprints and current sprint
  const availableSprints = useMemo(() => {
    return sprints.filter(
      (sprint) =>
        sprint.status !== "closed" &&
        sprint.status !== "cancelled" &&
        sprint.id !== currentSprintId
    );
  }, [sprints, currentSprintId]);

  // Calculate summary stats
  const summary = useMemo(() => {
    const totalPoints = selectedItems.reduce((sum, item) => sum + (item.story_points || 0), 0);
    const byType = {
      story: selectedItems.filter((i) => i.type === "story").length,
      task: selectedItems.filter((i) => i.type === "task").length,
      bug: selectedItems.filter((i) => i.type === "bug").length,
      spike: selectedItems.filter((i) => i.type === "spike").length,
    };
    return { totalPoints, byType };
  }, [selectedItems]);

  // Handle form submission
  const handleSubmit = async () => {
    if (targetSprintId === null && selectedItems.length > 0) {
      // Moving to backlog (no sprint)
    }

    setIsSubmitting(true);

    try {
      await onSubmit({
        item_ids: selectedItems.map((item) => item.id),
        target_sprint_id: targetSprintId,
        target_status: targetStatus === "keep" ? undefined : targetStatus,
      });
      onClose();
    } catch (error) {
      console.error("Failed to move items:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Reset state when modal opens
  const handleOpenChange = (isOpen: boolean) => {
    if (!isOpen) {
      setTargetSprintId(null);
      setTargetStatus("keep");
      onClose();
    }
  };

  if (selectedItems.length === 0) {
    return null;
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Move {selectedItems.length} Items</DialogTitle>
          <DialogDescription>
            Select a target sprint to move the selected backlog items.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          {/* Selected Items Summary */}
          <div className="rounded-lg border border-gray-200 bg-gray-50 p-4">
            <h4 className="mb-2 text-sm font-medium text-gray-700">Selected Items</h4>
            <div className="flex flex-wrap gap-3 text-sm">
              <span className="text-gray-600">
                <span className="font-semibold text-gray-900">{selectedItems.length}</span> items
              </span>
              <span className="text-gray-300">|</span>
              <span className="text-gray-600">
                <span className="font-semibold text-blue-600">{summary.totalPoints}</span> story points
              </span>
            </div>
            <div className="mt-2 flex flex-wrap gap-2">
              {summary.byType.story > 0 && (
                <span className="inline-flex items-center gap-1 rounded-full bg-blue-100 px-2 py-0.5 text-xs text-blue-700">
                  📖 {summary.byType.story} stories
                </span>
              )}
              {summary.byType.task > 0 && (
                <span className="inline-flex items-center gap-1 rounded-full bg-green-100 px-2 py-0.5 text-xs text-green-700">
                  ✅ {summary.byType.task} tasks
                </span>
              )}
              {summary.byType.bug > 0 && (
                <span className="inline-flex items-center gap-1 rounded-full bg-red-100 px-2 py-0.5 text-xs text-red-700">
                  🐛 {summary.byType.bug} bugs
                </span>
              )}
              {summary.byType.spike > 0 && (
                <span className="inline-flex items-center gap-1 rounded-full bg-purple-100 px-2 py-0.5 text-xs text-purple-700">
                  🔬 {summary.byType.spike} spikes
                </span>
              )}
            </div>
          </div>

          {/* Item Preview List */}
          <div className="max-h-[200px] overflow-y-auto rounded-lg border border-gray-200">
            {selectedItems.map((item) => (
              <div
                key={item.id}
                className="flex items-center gap-2 border-b border-gray-100 px-3 py-2 last:border-b-0"
              >
                <span className="text-sm">{getBacklogItemTypeIcon(item.type)}</span>
                <span
                  className={`inline-flex items-center rounded px-1.5 py-0.5 text-xs font-medium ${getPriorityColor(item.priority)}`}
                >
                  {item.priority.toUpperCase()}
                </span>
                <span className="flex-1 truncate text-sm text-gray-700">{item.title}</span>
                {item.story_points !== null && (
                  <span className="text-xs text-blue-600">{item.story_points} SP</span>
                )}
              </div>
            ))}
          </div>

          {/* Target Sprint Selection */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              Target Sprint <span className="text-red-500">*</span>
            </label>
            <select
              value={targetSprintId || ""}
              onChange={(e) => setTargetSprintId(e.target.value || null)}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="">📦 Product Backlog (No Sprint)</option>
              {availableSprints.map((sprint) => (
                <option key={sprint.id} value={sprint.id}>
                  {formatSprintLabel(sprint)}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500">
              Select a sprint or move items back to the product backlog.
            </p>
          </div>

          {/* Target Status Selection (Optional) */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              Update Status (Optional)
            </label>
            <select
              value={targetStatus}
              onChange={(e) => setTargetStatus(e.target.value as BacklogItemStatus | "keep")}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="keep">Keep current status</option>
              <option value="todo">{getStatusLabel("todo")}</option>
              <option value="in_progress">{getStatusLabel("in_progress")}</option>
              <option value="review">{getStatusLabel("review")}</option>
              <option value="done">{getStatusLabel("done")}</option>
              <option value="carried_over">{getStatusLabel("carried_over")}</option>
            </select>
            <p className="text-xs text-gray-500">
              Optionally update the status of all selected items.
            </p>
          </div>

          {/* Warning for active sprint */}
          {targetSprintId && availableSprints.find((s) => s.id === targetSprintId)?.status === "active" && (
            <div className="flex items-start gap-2 rounded-lg border border-yellow-200 bg-yellow-50 p-3">
              <svg
                className="mt-0.5 h-4 w-4 flex-shrink-0 text-yellow-600"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z"
                />
              </svg>
              <div className="text-xs text-yellow-700">
                <p className="font-medium">Moving to active sprint</p>
                <p>These items will be added to the currently running sprint. Make sure the team has capacity.</p>
              </div>
            </div>
          )}

          {/* SDLC 5.1.3 Guidelines */}
          <div className="rounded-md border border-gray-200 bg-gray-50 p-3 text-xs text-gray-600">
            <p className="font-medium text-gray-700">SDLC 5.1.3 Guidelines:</p>
            <ul className="mt-1 list-inside list-disc space-y-1">
              <li>Items moved to an active sprint require G-Sprint re-evaluation</li>
              <li>Moved items retain their original estimates unless updated</li>
              <li>Use &quot;Carried Over&quot; status for items from previous sprints</li>
            </ul>
          </div>
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
            onClick={handleSubmit}
            disabled={isSubmitting || isLoading}
          >
            {isSubmitting || isLoading ? (
              <>
                <svg className="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Moving...
              </>
            ) : (
              <>Move {selectedItems.length} Items</>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default BulkMoveModal;
