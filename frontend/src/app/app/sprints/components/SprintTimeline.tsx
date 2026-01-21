/**
 * Sprint Timeline (Gantt-style) - SDLC Orchestrator
 *
 * @module frontend/src/app/app/sprints/components/SprintTimeline
 * @description Gantt-style timeline visualization of sprints within phases
 * @sdlc SDLC 5.1.3 Framework - Sprint 87 (Days 6-7: Planning Hierarchy Visualization)
 * @reference SDLC 5.1.3 Pillar 2: Sprint Planning Governance
 * @status Sprint 87 - Core Feature Implementation
 */

"use client";

import { useMemo } from "react";
import Link from "next/link";
import type { SprintStatus, GateStatus } from "@/lib/types/planning";
import { getGateStatusIcon } from "@/lib/types/planning";

// =============================================================================
// TYPES
// =============================================================================

interface SprintTimelineProps {
  sprints: SprintForTimeline[];
  startDate?: Date;
  endDate?: Date;
  activeSprintId?: string | null;
  className?: string;
}

interface SprintForTimeline {
  id: string;
  name: string;
  number: number;
  status: SprintStatus | string;
  start_date: string;
  end_date: string;
  phase_id?: string | null;
  phase_name?: string;
  g_sprint_status?: GateStatus;
  g_sprint_close_status?: GateStatus;
  story_points_planned?: number;
  story_points_completed?: number;
  items_completed?: number;
  items_total?: number;
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Calculate the position and width of a sprint bar on the timeline
 */
function calculateSprintPosition(
  sprintStart: Date,
  sprintEnd: Date,
  timelineStart: Date,
  timelineEnd: Date
): { left: number; width: number } {
  const totalDays = Math.ceil((timelineEnd.getTime() - timelineStart.getTime()) / (1000 * 60 * 60 * 24));
  const startOffset = Math.ceil((sprintStart.getTime() - timelineStart.getTime()) / (1000 * 60 * 60 * 24));
  const duration = Math.ceil((sprintEnd.getTime() - sprintStart.getTime()) / (1000 * 60 * 60 * 24));

  return {
    left: Math.max(0, (startOffset / totalDays) * 100),
    width: Math.max(1, Math.min(100 - (startOffset / totalDays) * 100, (duration / totalDays) * 100)),
  };
}

/**
 * Generate week markers for the timeline
 */
function generateWeekMarkers(startDate: Date, endDate: Date): { date: Date; label: string }[] {
  const markers: { date: Date; label: string }[] = [];
  const current = new Date(startDate);

  // Start from the beginning of the week
  current.setDate(current.getDate() - current.getDay());

  while (current <= endDate) {
    markers.push({
      date: new Date(current),
      label: current.toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    });
    current.setDate(current.getDate() + 7);
  }

  return markers;
}

/**
 * Get bar color based on sprint status
 */
function getBarColor(status: SprintStatus | string, isActive: boolean): string {
  if (isActive) {
    return "bg-gradient-to-r from-blue-500 to-blue-600 shadow-md";
  }

  switch (status) {
    case "active":
      return "bg-blue-500";
    case "closing":
      return "bg-yellow-500";
    case "closed":
      return "bg-green-500";
    case "cancelled":
      return "bg-red-400";
    case "planned":
    default:
      return "bg-gray-400";
  }
}

/**
 * Calculate progress percentage for the sprint bar
 */
function calculateProgress(sprint: SprintForTimeline): number {
  if (sprint.items_total && sprint.items_total > 0) {
    return Math.round(((sprint.items_completed || 0) / sprint.items_total) * 100);
  }
  if (sprint.story_points_planned && sprint.story_points_planned > 0) {
    return Math.round(((sprint.story_points_completed || 0) / sprint.story_points_planned) * 100);
  }
  return 0;
}

// =============================================================================
// SPRINT BAR COMPONENT
// =============================================================================

interface SprintBarProps {
  sprint: SprintForTimeline;
  position: { left: number; width: number };
  isActive: boolean;
}

function SprintBar({ sprint, position, isActive }: SprintBarProps) {
  const progress = calculateProgress(sprint);
  const status = sprint.status as SprintStatus;

  return (
    <Link
      href={`/app/sprints/${sprint.id}`}
      className="group absolute h-7 cursor-pointer transition-transform hover:scale-y-125"
      style={{
        left: `${position.left}%`,
        width: `${position.width}%`,
        minWidth: "60px",
      }}
      title={`Sprint ${sprint.number}: ${sprint.name}`}
    >
      {/* Background Bar */}
      <div
        className={`
          relative h-full overflow-hidden rounded
          ${getBarColor(status, isActive)}
          ${isActive ? "ring-2 ring-blue-300 ring-offset-1" : ""}
        `}
      >
        {/* Progress Overlay */}
        {status === "active" && progress > 0 && (
          <div
            className="absolute inset-y-0 left-0 bg-white/20"
            style={{ width: `${progress}%` }}
          />
        )}

        {/* Content */}
        <div className="flex h-full items-center justify-between gap-1 px-2">
          <span className="truncate text-xs font-medium text-white">
            S{sprint.number}
          </span>

          {/* Gate Status Icons */}
          <div className="hidden items-center gap-0.5 group-hover:flex">
            {sprint.g_sprint_status && (
              <span className="text-[10px]" title={`G-Sprint: ${sprint.g_sprint_status}`}>
                {getGateStatusIcon(sprint.g_sprint_status)}
              </span>
            )}
            {sprint.g_sprint_close_status && (
              <span className="text-[10px]" title={`G-Sprint-Close: ${sprint.g_sprint_close_status}`}>
                {getGateStatusIcon(sprint.g_sprint_close_status)}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Tooltip on Hover */}
      <div className="pointer-events-none absolute left-1/2 top-full z-50 mt-1 hidden -translate-x-1/2 rounded bg-gray-900 px-2 py-1 text-xs text-white shadow-lg group-hover:block">
        <div className="whitespace-nowrap font-medium">Sprint {sprint.number}: {sprint.name}</div>
        <div className="whitespace-nowrap text-gray-300">
          {new Date(sprint.start_date).toLocaleDateString()} -{" "}
          {new Date(sprint.end_date).toLocaleDateString()}
        </div>
        {sprint.story_points_planned !== undefined && (
          <div className="whitespace-nowrap text-gray-300">
            {sprint.story_points_completed || 0}/{sprint.story_points_planned} SP
          </div>
        )}
      </div>
    </Link>
  );
}

// =============================================================================
// TODAY MARKER COMPONENT
// =============================================================================

function TodayMarker({
  timelineStart,
  timelineEnd,
}: {
  timelineStart: Date;
  timelineEnd: Date;
}) {
  const today = new Date();

  if (today < timelineStart || today > timelineEnd) {
    return null;
  }

  const totalDays = Math.ceil((timelineEnd.getTime() - timelineStart.getTime()) / (1000 * 60 * 60 * 24));
  const offset = Math.ceil((today.getTime() - timelineStart.getTime()) / (1000 * 60 * 60 * 24));
  const left = (offset / totalDays) * 100;

  return (
    <div
      className="absolute bottom-0 top-0 z-10 w-0.5 bg-red-500"
      style={{ left: `${left}%` }}
    >
      <div className="absolute -top-1 left-1/2 -translate-x-1/2 rounded bg-red-500 px-1 py-0.5 text-[10px] font-medium text-white">
        Today
      </div>
    </div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function SprintTimeline({
  sprints,
  startDate,
  endDate,
  activeSprintId,
  className = "",
}: SprintTimelineProps) {
  // Calculate timeline bounds
  const { timelineStart, timelineEnd, weekMarkers } = useMemo(() => {
    if (sprints.length === 0) {
      const now = new Date();
      const start = startDate || new Date(now.setMonth(now.getMonth() - 1));
      const end = endDate || new Date(now.setMonth(now.getMonth() + 3));
      return {
        timelineStart: start,
        timelineEnd: end,
        weekMarkers: generateWeekMarkers(start, end),
      };
    }

    // Find min and max dates from sprints
    const dates = sprints.flatMap((s) => [new Date(s.start_date), new Date(s.end_date)]);
    const minDate = startDate || new Date(Math.min(...dates.map((d) => d.getTime())));
    const maxDate = endDate || new Date(Math.max(...dates.map((d) => d.getTime())));

    // Add padding
    minDate.setDate(minDate.getDate() - 7);
    maxDate.setDate(maxDate.getDate() + 14);

    return {
      timelineStart: minDate,
      timelineEnd: maxDate,
      weekMarkers: generateWeekMarkers(minDate, maxDate),
    };
  }, [sprints, startDate, endDate]);

  // Group sprints by phase
  const sprintsByPhase = useMemo(() => {
    const groups: Record<string, SprintForTimeline[]> = {};

    for (const sprint of sprints) {
      const phaseKey = sprint.phase_id || "unassigned";
      if (!groups[phaseKey]) {
        groups[phaseKey] = [];
      }
      groups[phaseKey].push(sprint);
    }

    // Sort sprints within each group by start date
    for (const key of Object.keys(groups)) {
      groups[key] = groups[key].sort(
        (a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime()
      );
    }

    return groups;
  }, [sprints]);

  if (sprints.length === 0) {
    return (
      <div className={`rounded-xl border border-dashed border-gray-300 bg-gray-50 p-8 ${className}`}>
        <div className="flex flex-col items-center justify-center text-center">
          <svg
            className="mb-3 h-10 w-10 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z"
            />
          </svg>
          <h3 className="text-sm font-medium text-gray-900">No Sprints to Display</h3>
          <p className="mt-1 text-xs text-gray-500">
            Create sprints to see them on the timeline.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`rounded-xl border border-gray-200 bg-white ${className}`}>
      {/* Header */}
      <div className="border-b border-gray-200 px-4 py-3">
        <h3 className="text-sm font-semibold text-gray-900">Sprint Timeline</h3>
        <p className="text-xs text-gray-500">
          {timelineStart.toLocaleDateString("en-US", { month: "long", year: "numeric" })} -{" "}
          {timelineEnd.toLocaleDateString("en-US", { month: "long", year: "numeric" })}
        </p>
      </div>

      {/* Timeline Content */}
      <div className="overflow-x-auto">
        <div className="min-w-[600px] p-4">
          {/* Week Headers */}
          <div className="relative mb-2 h-6 border-b border-gray-100">
            {weekMarkers.map((marker, index) => {
              const totalDays = Math.ceil(
                (timelineEnd.getTime() - timelineStart.getTime()) / (1000 * 60 * 60 * 24)
              );
              const offset = Math.ceil(
                (marker.date.getTime() - timelineStart.getTime()) / (1000 * 60 * 60 * 24)
              );
              const left = (offset / totalDays) * 100;

              return (
                <div
                  key={index}
                  className="absolute text-xs text-gray-400"
                  style={{ left: `${left}%` }}
                >
                  <div className="h-2 w-px bg-gray-200" />
                  <span className="ml-1 whitespace-nowrap">{marker.label}</span>
                </div>
              );
            })}
          </div>

          {/* Sprint Rows by Phase */}
          <div className="space-y-4">
            {Object.entries(sprintsByPhase).map(([phaseId, phaseSprints]) => {
              const phaseName = phaseSprints[0]?.phase_name || "Unassigned";
              const phaseCount = Object.keys(sprintsByPhase).length;

              return (
                <div key={phaseId}>
                  {/* Phase Label */}
                  {phaseCount > 1 && (
                    <div className="mb-1 text-xs font-medium text-gray-600">{phaseName}</div>
                  )}

                  {/* Sprint Bars */}
                  <div className="relative h-10 rounded bg-gray-50">
                    <TodayMarker timelineStart={timelineStart} timelineEnd={timelineEnd} />

                    {phaseSprints.map((sprint) => {
                      const position = calculateSprintPosition(
                        new Date(sprint.start_date),
                        new Date(sprint.end_date),
                        timelineStart,
                        timelineEnd
                      );

                      return (
                        <SprintBar
                          key={sprint.id}
                          sprint={sprint}
                          position={position}
                          isActive={sprint.id === activeSprintId}
                        />
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="border-t border-gray-200 px-4 py-2">
        <div className="flex flex-wrap items-center gap-4 text-xs text-gray-500">
          <span className="font-medium">Status:</span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-4 rounded bg-gray-400" />
            Planned
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-4 rounded bg-blue-500" />
            Active
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-4 rounded bg-yellow-500" />
            Closing
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-4 rounded bg-green-500" />
            Closed
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-0.5 bg-red-500" />
            Today
          </span>
        </div>
      </div>
    </div>
  );
}

export default SprintTimeline;
