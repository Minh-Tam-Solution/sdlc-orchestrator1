/**
 * Planning Status Badge - SDLC Orchestrator
 *
 * @module frontend/src/components/planning/PlanningStatusBadge
 * @description Badge component for displaying planning session status
 * @sdlc SDLC 6.0.6 Framework - Sprint 99 (Planning Sub-agent Part 2)
 */

import { cn } from "@/lib/utils";
import type { PlanningStatus } from "@/lib/types/planning-subagent";

interface PlanningStatusBadgeProps {
  status: PlanningStatus;
  size?: "sm" | "md" | "lg";
  className?: string;
}

/**
 * Get colors for status
 */
function getStatusColors(status: PlanningStatus): {
  bg: string;
  text: string;
  border: string;
} {
  switch (status) {
    case "extracting":
      return {
        bg: "bg-blue-100",
        text: "text-blue-800",
        border: "border-blue-200",
      };
    case "synthesizing":
      return {
        bg: "bg-purple-100",
        text: "text-purple-800",
        border: "border-purple-200",
      };
    case "pending_approval":
      return {
        bg: "bg-yellow-100",
        text: "text-yellow-800",
        border: "border-yellow-200",
      };
    case "approved":
      return {
        bg: "bg-green-100",
        text: "text-green-800",
        border: "border-green-200",
      };
    case "rejected":
      return {
        bg: "bg-red-100",
        text: "text-red-800",
        border: "border-red-200",
      };
    case "expired":
      return {
        bg: "bg-gray-100",
        text: "text-gray-800",
        border: "border-gray-200",
      };
  }
}

/**
 * Get icon for status
 */
function getStatusIcon(status: PlanningStatus): string {
  switch (status) {
    case "extracting":
      return "⟳";
    case "synthesizing":
      return "⚡";
    case "pending_approval":
      return "⏳";
    case "approved":
      return "✓";
    case "rejected":
      return "✗";
    case "expired":
      return "○";
  }
}

/**
 * Get human-readable label for status
 */
function getStatusLabel(status: PlanningStatus): string {
  switch (status) {
    case "extracting":
      return "Extracting";
    case "synthesizing":
      return "Synthesizing";
    case "pending_approval":
      return "Pending Approval";
    case "approved":
      return "Approved";
    case "rejected":
      return "Rejected";
    case "expired":
      return "Expired";
  }
}

export function PlanningStatusBadge({
  status,
  size = "md",
  className,
}: PlanningStatusBadgeProps) {
  const colors = getStatusColors(status);
  const icon = getStatusIcon(status);
  const label = getStatusLabel(status);

  const sizeClasses = {
    sm: "text-xs px-2 py-0.5",
    md: "text-sm px-3 py-1",
    lg: "text-base px-4 py-1.5",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border font-medium",
        colors.bg,
        colors.text,
        colors.border,
        sizeClasses[size],
        className
      )}
    >
      <span className="font-bold">{icon}</span>
      <span>{label}</span>
    </span>
  );
}

export default PlanningStatusBadge;
