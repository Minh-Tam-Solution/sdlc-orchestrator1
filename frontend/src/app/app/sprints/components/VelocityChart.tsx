/**
 * Velocity Chart Component - SDLC Orchestrator
 *
 * @module frontend/src/app/app/sprints/components/VelocityChart
 * @description Multi-sprint velocity comparison chart (planned vs completed story points)
 * @sdlc SDLC 6.0.6 Framework - Sprint 93 (Planning Hierarchy Part 2)
 * @reference SDLC 6.0.6 Pillar 2: Sprint Planning Governance
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
  ReferenceLine,
} from "recharts";

// =============================================================================
// TYPES
// =============================================================================

interface VelocityDataPoint {
  sprint_name: string;
  planned: number;
  completed: number;
}

interface VelocityChartProps {
  data: VelocityDataPoint[];
  className?: string;
  height?: number;
  showLegend?: boolean;
  showGrid?: boolean;
  showAverage?: boolean;
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
 * Calculate average velocity from completed points
 */
function calculateAverageVelocity(data: VelocityDataPoint[]): number {
  if (data.length === 0) return 0;
  const totalCompleted = data.reduce((sum, d) => sum + d.completed, 0);
  return Math.round(totalCompleted / data.length);
}

/**
 * Calculate completion rate (percentage of planned that was completed)
 */
function calculateCompletionRate(data: VelocityDataPoint[]): number {
  if (data.length === 0) return 0;
  const totalPlanned = data.reduce((sum, d) => sum + d.planned, 0);
  const totalCompleted = data.reduce((sum, d) => sum + d.completed, 0);
  if (totalPlanned === 0) return 0;
  return Math.round((totalCompleted / totalPlanned) * 100);
}

/**
 * Calculate velocity trend (improving, stable, declining)
 */
function calculateVelocityTrend(
  data: VelocityDataPoint[]
): "improving" | "stable" | "declining" | "insufficient" {
  if (data.length < 3) return "insufficient";

  // Compare last 3 sprints
  const recentThree = data.slice(-3);
  const velocities = recentThree.map((d) => d.completed);

  // Calculate trend using simple linear regression
  const n = velocities.length;
  const sumX = (n * (n - 1)) / 2;
  const sumY = velocities.reduce((a, b) => a + b, 0);
  const sumXY = velocities.reduce((sum, y, i) => sum + i * y, 0);
  const sumX2 = velocities.reduce((sum, _, i) => sum + i * i, 0);

  const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);

  if (slope > 1) return "improving";
  if (slope < -1) return "declining";
  return "stable";
}

/**
 * Get trend color
 */
function getTrendColor(trend: ReturnType<typeof calculateVelocityTrend>): string {
  const colors = {
    improving: "text-green-600",
    stable: "text-blue-600",
    declining: "text-red-600",
    insufficient: "text-gray-400",
  };
  return colors[trend];
}

/**
 * Get trend label
 */
function getTrendLabel(trend: ReturnType<typeof calculateVelocityTrend>): string {
  const labels = {
    improving: "Improving",
    stable: "Stable",
    declining: "Declining",
    insufficient: "Need More Data",
  };
  return labels[trend];
}

/**
 * Get trend icon
 */
function getTrendIcon(trend: ReturnType<typeof calculateVelocityTrend>): string {
  const icons = {
    improving: "↑",
    stable: "→",
    declining: "↓",
    insufficient: "~",
  };
  return icons[trend];
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

  const planned = payload.find((p) => p.name === "Planned")?.value || 0;
  const completed = payload.find((p) => p.name === "Completed")?.value || 0;
  const completionRate = planned > 0 ? Math.round((completed / planned) * 100) : 0;

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
        <div className="mt-2 border-t border-gray-100 pt-2">
          <span className={completionRate >= 80 ? "text-green-600" : completionRate >= 60 ? "text-yellow-600" : "text-red-600"}>
            {completionRate}% completion rate
          </span>
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function VelocityChart({
  data,
  className = "",
  height = 300,
  showLegend = true,
  showGrid = true,
  showAverage = true,
}: VelocityChartProps) {
  // Calculate metrics
  const metrics = useMemo(() => ({
    averageVelocity: calculateAverageVelocity(data),
    completionRate: calculateCompletionRate(data),
    trend: calculateVelocityTrend(data),
  }), [data]);

  // Get max value for Y-axis domain
  const maxValue = useMemo(() => {
    const values = data.flatMap((d) => [d.planned, d.completed]);
    return Math.max(...values, 10) * 1.1; // Add 10% padding
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
              d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 1.5m-.5-1.5h-9.5m0 0-.5 1.5m.75-9 3-3 2.148 2.148A12.061 12.061 0 0 1 16.5 7.605"
            />
          </svg>
          <h3 className="text-sm font-medium text-gray-900">No Velocity Data</h3>
          <p className="mt-1 text-xs text-gray-500">
            Complete at least one sprint to see velocity trends.
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
          <h3 className="text-sm font-semibold text-gray-900">Velocity Chart</h3>
          <p className="text-xs text-gray-500">
            {data.length} sprint{data.length !== 1 ? "s" : ""} | Avg: {metrics.averageVelocity} pts/sprint
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span
            className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium ${getTrendColor(metrics.trend)}`}
          >
            {getTrendIcon(metrics.trend)} {getTrendLabel(metrics.trend)}
          </span>
        </div>
      </div>

      {/* Chart */}
      <div className="p-4">
        <ResponsiveContainer width="100%" height={height}>
          <BarChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            {showGrid && (
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            )}
            <XAxis
              dataKey="sprint_name"
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
            {/* Average velocity reference line */}
            {showAverage && metrics.averageVelocity > 0 && (
              <ReferenceLine
                y={metrics.averageVelocity}
                stroke="#10b981"
                strokeDasharray="5 5"
                label={{
                  value: `Avg: ${metrics.averageVelocity}`,
                  position: "right",
                  fill: "#10b981",
                  fontSize: 10,
                }}
              />
            )}
            {/* Planned bar (lighter color) */}
            <Bar
              dataKey="planned"
              name="Planned"
              fill="#cbd5e1"
              radius={[4, 4, 0, 0]}
            />
            {/* Completed bar (solid color) */}
            <Bar
              dataKey="completed"
              name="Completed"
              fill="#3b82f6"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Footer Stats */}
      <div className="border-t border-gray-200 px-4 py-2">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>
            Overall Completion:{" "}
            <strong
              className={
                metrics.completionRate >= 80
                  ? "text-green-600"
                  : metrics.completionRate >= 60
                  ? "text-yellow-600"
                  : "text-red-600"
              }
            >
              {metrics.completionRate}%
            </strong>
          </span>
          <span>
            {metrics.trend === "improving" && "Team velocity is improving over time."}
            {metrics.trend === "stable" && "Team velocity is consistent and predictable."}
            {metrics.trend === "declining" && "Review capacity - velocity is declining."}
            {metrics.trend === "insufficient" && "Complete 3+ sprints for trend analysis."}
          </span>
        </div>
      </div>
    </div>
  );
}

export default VelocityChart;
