/**
 * Conformance Score Badge - SDLC Orchestrator
 *
 * @module frontend/src/components/planning/ConformanceScoreBadge
 * @description Badge component for displaying conformance scores (0-100)
 * @sdlc SDLC 5.2.0 Framework - Sprint 99 (Planning Sub-agent Part 2)
 */

import { cn } from "@/lib/utils";
import type { ConformanceLevel } from "@/lib/types/planning-subagent";

interface ConformanceScoreBadgeProps {
  score: number;
  level?: ConformanceLevel;
  size?: "sm" | "md" | "lg";
  showLabel?: boolean;
  className?: string;
}

/**
 * Get conformance level from score
 */
function getConformanceLevel(score: number): ConformanceLevel {
  if (score >= 90) return "EXCELLENT";
  if (score >= 70) return "GOOD";
  if (score >= 50) return "FAIR";
  return "POOR";
}

/**
 * Get colors for conformance level
 */
function getLevelColors(level: ConformanceLevel): {
  bg: string;
  text: string;
  border: string;
} {
  switch (level) {
    case "EXCELLENT":
      return {
        bg: "bg-green-100",
        text: "text-green-800",
        border: "border-green-200",
      };
    case "GOOD":
      return {
        bg: "bg-yellow-100",
        text: "text-yellow-800",
        border: "border-yellow-200",
      };
    case "FAIR":
      return {
        bg: "bg-orange-100",
        text: "text-orange-800",
        border: "border-orange-200",
      };
    case "POOR":
      return {
        bg: "bg-red-100",
        text: "text-red-800",
        border: "border-red-200",
      };
  }
}

/**
 * Get icon for conformance level
 */
function getLevelIcon(level: ConformanceLevel): string {
  switch (level) {
    case "EXCELLENT":
      return "✓";
    case "GOOD":
      return "○";
    case "FAIR":
      return "△";
    case "POOR":
      return "✗";
  }
}

export function ConformanceScoreBadge({
  score,
  level,
  size = "md",
  showLabel = true,
  className,
}: ConformanceScoreBadgeProps) {
  const computedLevel = level || getConformanceLevel(score);
  const colors = getLevelColors(computedLevel);
  const icon = getLevelIcon(computedLevel);

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
      <span>{score}%</span>
      {showLabel && (
        <span className="font-normal capitalize">
          ({computedLevel.toLowerCase()})
        </span>
      )}
    </span>
  );
}

export default ConformanceScoreBadge;
