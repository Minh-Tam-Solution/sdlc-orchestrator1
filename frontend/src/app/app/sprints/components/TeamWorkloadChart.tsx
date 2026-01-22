/**
 * Team Workload Chart Component - SDLC Orchestrator
 *
 * @module frontend/src/app/app/sprints/components/TeamWorkloadChart
 * @description Per-assignee workload visualization showing assigned vs completed points
 * @sdlc SDLC 5.1.3 Framework - Sprint 93 (Planning Hierarchy Part 2)
 * @reference SDLC 5.1.3 Pillar 2: Sprint Planning Governance
 * @status Sprint 93 - Sprint CRUD & Charts
 */

"use client";

import { useMemo } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from "recharts";

// =============================================================================
// TYPES
// =============================================================================

interface TeamWorkloadDataPoint {
  assignee_name: string;
  assigned_points: number;
  completed_points: number;
}

interface TeamWorkloadChartProps {
  data: TeamWorkloadDataPoint[];
  className?: string;
  height?: number;
  showLegend?: boolean;
  showGrid?: boolean;
  layout?: "horizontal" | "vertical";
}

interface TooltipPayload {
  value: number;
  name: string;
  color: string;
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Calculate completion percentage for a team member
 */
function calculateCompletionPercentage(assigned: number, completed: number): number {
  if (assigned === 0) return 0;
  return Math.round((completed / assigned) * 100);
}

/**
 * Get workload status based on completion percentage
 */
function getWorkloadStatus(
  assigned: number,
  completed: number
): "complete" | "on-track" | "behind" | "overloaded" | "idle" {
  if (assigned === 0) return "idle";
  const percentage = calculateCompletionPercentage(assigned, completed);
  if (percentage >= 100) return "complete";
  if (percentage >= 70) return "on-track";
  if (percentage >= 40) return "behind";
  return "overloaded";
}

/**
 * Get status color
 */
function getStatusColor(status: ReturnType<typeof getWorkloadStatus>): string {
  const colors = {
    complete: "#10b981",
    "on-track": "#3b82f6",
    behind: "#f59e0b",
    overloaded: "#ef4444",
    idle: "#9ca3af",
  };
  return colors[status];
}

/**
 * Get status badge color
 */
function getStatusBadgeColor(status: ReturnType<typeof getWorkloadStatus>): string {
  const colors = {
    complete: "bg-green-100 text-green-800",
    "on-track": "bg-blue-100 text-blue-800",
    behind: "bg-yellow-100 text-yellow-800",
    overloaded: "bg-red-100 text-red-800",
    idle: "bg-gray-100 text-gray-800",
  };
  return colors[status];
}

/**
 * Get status label
 */
function getStatusLabel(status: ReturnType<typeof getWorkloadStatus>): string {
  const labels = {
    complete: "Complete",
    "on-track": "On Track",
    behind: "Behind",
    overloaded: "Overloaded",
    idle: "Idle",
  };
  return labels[status];
}

/**
 * Calculate team summary metrics
 */
function calculateTeamSummary(data: TeamWorkloadDataPoint[]): {
  totalAssigned: number;
  totalCompleted: number;
  averageCompletion: number;
  teamSize: number;
} {
  const totalAssigned = data.reduce((sum, d) => sum + d.assigned_points, 0);
  const totalCompleted = data.reduce((sum, d) => sum + d.completed_points, 0);
  const averageCompletion = totalAssigned > 0 ? Math.round((totalCompleted / totalAssigned) * 100) : 0;
  const teamSize = data.filter((d) => d.assigned_points > 0).length;

  return { totalAssigned, totalCompleted, averageCompletion, teamSize };
}

// =============================================================================
// CUSTOM TOOLTIP COMPONENT
// =============================================================================

interface CustomTooltipProps {
  active?: boolean;
  payload?: TooltipPayload[];
  label?: string;
}

function CustomTooltip({ active, payload, label }: CustomTooltipProps) {
  if (!active || !payload || !payload.length) {
    return null;
  }

  const assigned = payload.find((p) => p.name === "Assigned")?.value || 0;
  const completed = payload.find((p) => p.name === "Completed")?.value || 0;
  const percentage = calculateCompletionPercentage(assigned, completed);
  const status = getWorkloadStatus(assigned, completed);

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-3 shadow-lg">
      <p className="mb-2 font-medium text-gray-900">{label}</p>
      <div className="space-y-1 text-sm">
        {payload.map((entry, index) => (
          <div key={index} className="flex items-center justify-between gap-4">
            <span className="flex items-center gap-2">
              <span
                className="h-2 w-2 rounded"
                style={{ backgroundColor: entry.color }}
              />
              {entry.name}:
            </span>
            <span className="font-medium">{entry.value} pts</span>
          </div>
        ))}
        <div className="mt-2 border-t border-gray-100 pt-2 flex items-center justify-between">
          <span className={`inline-flex items-center rounded px-1.5 py-0.5 text-xs ${getStatusBadgeColor(status)}`}>
            {getStatusLabel(status)}
          </span>
          <span className="font-medium">{percentage}%</span>
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function TeamWorkloadChart({
  data,
  className = "",
  height = 300,
  showLegend = true,
  showGrid = true,
  layout = "horizontal",
}: TeamWorkloadChartProps) {
  // Calculate summary metrics
  const summary = useMemo(() => calculateTeamSummary(data), [data]);

  // Enrich data with status
  const enrichedData = useMemo(() => {
    return data.map((d) => ({
      ...d,
      status: getWorkloadStatus(d.assigned_points, d.completed_points),
      completion_percentage: calculateCompletionPercentage(d.assigned_points, d.completed_points),
    }));
  }, [data]);

  // Sort by completion percentage (descending)
  const sortedData = useMemo(() => {
    return [...enrichedData].sort((a, b) => b.completion_percentage - a.completion_percentage);
  }, [enrichedData]);

  // Get max value for axis domain
  const maxValue = useMemo(() => {
    const values = data.flatMap((d) => [d.assigned_points, d.completed_points]);
    return Math.max(...values, 10) * 1.1;
  }, [data]);

  if (data.length === 0) {
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
              d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z"
            />
          </svg>
          <h3 className="text-sm font-medium text-gray-900">No Team Data</h3>
          <p className="mt-1 text-xs text-gray-500">
            Assign items to team members to see workload distribution.
          </p>
        </div>
      </div>
    );
  }

  const isVertical = layout === "vertical";

  return (
    <div className={`rounded-xl border border-gray-200 bg-white ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-200 px-4 py-3">
        <div>
          <h3 className="text-sm font-semibold text-gray-900">Team Workload</h3>
          <p className="text-xs text-gray-500">
            {summary.teamSize} member{summary.teamSize !== 1 ? "s" : ""} |{" "}
            {summary.totalCompleted}/{summary.totalAssigned} pts completed
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span
            className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
              summary.averageCompletion >= 80
                ? "bg-green-100 text-green-800"
                : summary.averageCompletion >= 60
                ? "bg-yellow-100 text-yellow-800"
                : "bg-red-100 text-red-800"
            }`}
          >
            {summary.averageCompletion}% avg
          </span>
        </div>
      </div>

      {/* Chart */}
      <div className="p-4">
        <ResponsiveContainer width="100%" height={height}>
          <BarChart
            data={sortedData}
            layout={isVertical ? "vertical" : "horizontal"}
            margin={{ top: 5, right: 20, left: isVertical ? 80 : 0, bottom: 5 }}
          >
            {showGrid && (
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            )}
            {isVertical ? (
              <>
                <XAxis
                  type="number"
                  domain={[0, maxValue]}
                  tick={{ fontSize: 12, fill: "#6b7280" }}
                  tickLine={{ stroke: "#e5e7eb" }}
                  axisLine={{ stroke: "#e5e7eb" }}
                />
                <YAxis
                  type="category"
                  dataKey="assignee_name"
                  tick={{ fontSize: 12, fill: "#6b7280" }}
                  tickLine={{ stroke: "#e5e7eb" }}
                  axisLine={{ stroke: "#e5e7eb" }}
                  width={75}
                />
              </>
            ) : (
              <>
                <XAxis
                  dataKey="assignee_name"
                  tick={{ fontSize: 12, fill: "#6b7280" }}
                  tickLine={{ stroke: "#e5e7eb" }}
                  axisLine={{ stroke: "#e5e7eb" }}
                />
                <YAxis
                  domain={[0, maxValue]}
                  tick={{ fontSize: 12, fill: "#6b7280" }}
                  tickLine={{ stroke: "#e5e7eb" }}
                  axisLine={{ stroke: "#e5e7eb" }}
                  label={{
                    value: "Story Points",
                    angle: -90,
                    position: "insideLeft",
                    style: { textAnchor: "middle", fill: "#6b7280", fontSize: 12 },
                  }}
                />
              </>
            )}
            <Tooltip content={<CustomTooltip />} />
            {showLegend && (
              <Legend
                verticalAlign="top"
                height={36}
                iconType="rect"
                formatter={(value) => (
                  <span className="text-xs text-gray-600">{value}</span>
                )}
              />
            )}
            {/* Assigned bar */}
            <Bar
              dataKey="assigned_points"
              name="Assigned"
              fill="#cbd5e1"
              radius={isVertical ? [0, 4, 4, 0] : [4, 4, 0, 0]}
            />
            {/* Completed bar with color based on status */}
            <Bar
              dataKey="completed_points"
              name="Completed"
              radius={isVertical ? [0, 4, 4, 0] : [4, 4, 0, 0]}
            >
              {sortedData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={getStatusColor(entry.status)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Footer Legend */}
      <div className="border-t border-gray-200 px-4 py-2">
        <div className="flex flex-wrap items-center gap-4 text-xs text-gray-500">
          <span className="font-medium">Status:</span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-2 rounded" style={{ backgroundColor: "#10b981" }} />
            Complete (100%+)
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-2 rounded" style={{ backgroundColor: "#3b82f6" }} />
            On Track (70-99%)
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-2 rounded" style={{ backgroundColor: "#f59e0b" }} />
            Behind (40-69%)
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-2 rounded" style={{ backgroundColor: "#ef4444" }} />
            Overloaded (&lt;40%)
          </span>
        </div>
      </div>
    </div>
  );
}

export default TeamWorkloadChart;
