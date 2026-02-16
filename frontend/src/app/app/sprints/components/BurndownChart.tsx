/**
 * Burndown Chart Component - SDLC Orchestrator
 *
 * @module frontend/src/app/app/sprints/components/BurndownChart
 * @description Real-time burndown visualization (ideal vs actual) for sprint progress
 * @sdlc SDLC 6.0.6 Framework - Sprint 93 (Planning Hierarchy Part 2)
 * @reference SDLC 6.0.6 Pillar 2: Sprint Planning Governance
 * @status Sprint 93 - Sprint CRUD & Charts
 */

"use client";

import { useMemo } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

// =============================================================================
// TYPES
// =============================================================================

interface BurndownDataPoint {
  date: string;
  ideal: number;
  actual: number;
}

interface BurndownChartProps {
  data: BurndownDataPoint[];
  sprintName?: string;
  className?: string;
  height?: number;
  showLegend?: boolean;
  showGrid?: boolean;
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
 * Format date for display on X-axis
 */
function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

/**
 * Calculate burndown health status
 * Compares actual vs ideal to determine if sprint is on track
 */
function calculateBurndownHealth(
  data: BurndownDataPoint[]
): "on-track" | "at-risk" | "behind" | "ahead" | "no-data" {
  if (data.length === 0) return "no-data";

  // Get the latest data point
  const latest = data[data.length - 1];
  if (!latest) return "no-data";

  const difference = latest.actual - latest.ideal;
  const totalPoints = data[0]?.ideal || 1;
  const percentageDiff = (difference / totalPoints) * 100;

  if (percentageDiff <= -10) return "ahead"; // More than 10% ahead
  if (percentageDiff <= 5) return "on-track"; // Within 5%
  if (percentageDiff <= 15) return "at-risk"; // 5-15% behind
  return "behind"; // More than 15% behind
}

/**
 * Get status color for burndown health
 */
function getHealthColor(health: ReturnType<typeof calculateBurndownHealth>): string {
  const colors = {
    "on-track": "text-green-600",
    "ahead": "text-blue-600",
    "at-risk": "text-yellow-600",
    "behind": "text-red-600",
    "no-data": "text-gray-400",
  };
  return colors[health];
}

/**
 * Get status label for burndown health
 */
function getHealthLabel(health: ReturnType<typeof calculateBurndownHealth>): string {
  const labels = {
    "on-track": "On Track",
    "ahead": "Ahead of Schedule",
    "at-risk": "At Risk",
    "behind": "Behind Schedule",
    "no-data": "No Data",
  };
  return labels[health];
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

  const idealValue = payload.find((p) => p.name === "Ideal")?.value;
  const actualValue = payload.find((p) => p.name === "Actual")?.value;
  const difference = actualValue !== undefined && idealValue !== undefined
    ? actualValue - idealValue
    : null;

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-3 shadow-lg">
      <p className="mb-2 font-medium text-gray-900">{label}</p>
      <div className="space-y-1 text-sm">
        {payload.map((entry, index) => (
          <div key={index} className="flex items-center justify-between gap-4">
            <span className="flex items-center gap-2">
              <span
                className="h-2 w-2 rounded-full"
                style={{ backgroundColor: entry.color }}
              />
              {entry.name}:
            </span>
            <span className="font-medium">{entry.value} pts</span>
          </div>
        ))}
        {difference !== null && (
          <div className="mt-2 border-t border-gray-100 pt-2">
            <span className={difference > 0 ? "text-red-600" : "text-green-600"}>
              {difference > 0 ? "+" : ""}{difference} pts {difference > 0 ? "behind" : "ahead"}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function BurndownChart({
  data,
  sprintName,
  className = "",
  height = 300,
  showLegend = true,
  showGrid = true,
}: BurndownChartProps) {
  // Calculate health status
  const health = useMemo(() => calculateBurndownHealth(data), [data]);

  // Find today's position for reference line
  const todayData = useMemo(() => {
    const today = new Date().toISOString().split("T")[0];
    return data.find((d) => d.date === today);
  }, [data]);

  // Calculate remaining points summary
  const summary = useMemo(() => {
    if (data.length === 0) {
      return { remaining: 0, total: 0, completed: 0, percentComplete: 0 };
    }
    const total = data[0]?.ideal || 0;
    const remaining = data[data.length - 1]?.actual || 0;
    const completed = total - remaining;
    const percentComplete = total > 0 ? Math.round((completed / total) * 100) : 0;
    return { remaining, total, completed, percentComplete };
  }, [data]);

  // Format data for chart
  const chartData = useMemo(() => {
    return data.map((point) => ({
      ...point,
      dateLabel: formatDate(point.date),
    }));
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
              d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z"
            />
          </svg>
          <h3 className="text-sm font-medium text-gray-900">No Burndown Data</h3>
          <p className="mt-1 text-xs text-gray-500">
            Start the sprint to see burndown progress.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`rounded-xl border border-gray-200 bg-white ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-200 px-4 py-3">
        <div>
          <h3 className="text-sm font-semibold text-gray-900">
            Burndown Chart {sprintName && `- ${sprintName}`}
          </h3>
          <p className="text-xs text-gray-500">
            {summary.total} total points | {summary.completed} completed ({summary.percentComplete}%)
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span
            className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${getHealthColor(health)}`}
          >
            {getHealthLabel(health)}
          </span>
        </div>
      </div>

      {/* Chart */}
      <div className="p-4">
        <ResponsiveContainer width="100%" height={height}>
          <LineChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            {showGrid && (
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            )}
            <XAxis
              dataKey="dateLabel"
              tick={{ fontSize: 12, fill: "#6b7280" }}
              tickLine={{ stroke: "#e5e7eb" }}
              axisLine={{ stroke: "#e5e7eb" }}
            />
            <YAxis
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
            <Tooltip content={<CustomTooltip />} />
            {showLegend && (
              <Legend
                verticalAlign="top"
                height={36}
                iconType="line"
                formatter={(value) => (
                  <span className="text-xs text-gray-600">{value}</span>
                )}
              />
            )}
            {/* Today reference line */}
            {todayData && (
              <ReferenceLine
                x={formatDate(todayData.date)}
                stroke="#ef4444"
                strokeDasharray="5 5"
                label={{
                  value: "Today",
                  position: "top",
                  fill: "#ef4444",
                  fontSize: 10,
                }}
              />
            )}
            {/* Ideal line (dashed) */}
            <Line
              type="linear"
              dataKey="ideal"
              name="Ideal"
              stroke="#94a3b8"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={false}
              activeDot={{ r: 4, fill: "#94a3b8" }}
            />
            {/* Actual line (solid) */}
            <Line
              type="monotone"
              dataKey="actual"
              name="Actual"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={{ r: 3, fill: "#3b82f6" }}
              activeDot={{ r: 5, fill: "#3b82f6" }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Footer Stats */}
      <div className="border-t border-gray-200 px-4 py-2">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Remaining: <strong className="text-gray-900">{summary.remaining} pts</strong></span>
          <span>
            {health === "ahead" && "Great progress! You're ahead of schedule."}
            {health === "on-track" && "Good job! Sprint is on track."}
            {health === "at-risk" && "Attention needed - sprint may slip."}
            {health === "behind" && "Action required - sprint is behind schedule."}
          </span>
        </div>
      </div>
    </div>
  );
}

export default BurndownChart;
