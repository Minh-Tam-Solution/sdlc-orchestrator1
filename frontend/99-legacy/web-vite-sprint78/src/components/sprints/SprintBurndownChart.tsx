/**
 * =========================================================================
 * SprintBurndownChart - Sprint Burndown Visualization
 * SDLC Orchestrator - Sprint 77 Day 5
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 77 Frontend & Completion
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - Display sprint burndown chart with ideal vs actual lines
 * - Show remaining story points over time
 * - Visual progress indicator
 * - Responsive and accessible
 *
 * References:
 * - backend/app/services/burndown_service.py
 * - docs/08-collaborate/01-Sprint-Logs/SPRINT-77-DAY-2-COMPLETE.md
 * =========================================================================
 */

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
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { useSprintBurndown } from "@/hooks/usePlanning";
import { TrendingDown, TrendingUp, Minus, AlertTriangle } from "lucide-react";
import { Badge } from "@/components/ui/badge";

/** Props for SprintBurndownChart */
interface SprintBurndownChartProps {
  /** Sprint ID to show burndown for */
  sprintId: string;
  /** Optional height for the chart */
  height?: number;
}

/**
 * Sprint Burndown Chart Component
 * Displays burndown with ideal line, actual line, and today marker
 */
export default function SprintBurndownChart({
  sprintId,
  height = 300,
}: SprintBurndownChartProps) {
  const { data: burndown, isLoading, error } = useSprintBurndown(sprintId);

  // Calculate trend indicator
  const trend = useMemo(() => {
    if (!burndown || burndown.data_points.length < 2) {
      return { status: "unknown", icon: Minus, color: "text-gray-500" };
    }

    const lastPoint = burndown.data_points[burndown.data_points.length - 1];
    if (!lastPoint) {
      return { status: "unknown", icon: Minus, color: "text-gray-500" };
    }

    const idealRemaining = lastPoint.ideal_remaining;
    const actualRemaining = lastPoint.actual_remaining;

    if (actualRemaining === null || actualRemaining === undefined) {
      return { status: "unknown", icon: Minus, color: "text-gray-500" };
    }

    const diff = actualRemaining - idealRemaining;
    const percentDiff = (diff / burndown.total_points) * 100;

    if (percentDiff <= -10) {
      return {
        status: "ahead",
        icon: TrendingDown,
        color: "text-green-600",
        label: "Ahead of schedule",
      };
    } else if (percentDiff >= 10) {
      return {
        status: "behind",
        icon: TrendingUp,
        color: "text-red-600",
        label: "Behind schedule",
      };
    } else {
      return {
        status: "on_track",
        icon: Minus,
        color: "text-blue-600",
        label: "On track",
      };
    }
  }, [burndown]);

  // Format chart data
  const chartData = useMemo(() => {
    if (!burndown) return [];

    return burndown.data_points.map((point) => ({
      date: new Date(point.date).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
      }),
      fullDate: point.date,
      ideal: point.ideal_remaining,
      actual: point.actual_remaining,
      completed: point.completed_points,
    }));
  }, [burndown]);

  // Find today's index for reference line
  const todayIndex = useMemo(() => {
    if (!burndown) return -1;
    const todayStr = new Date().toISOString().split("T")[0];
    if (!todayStr) return -1;
    return burndown.data_points.findIndex((p) => p.date >= todayStr);
  }, [burndown]);

  if (isLoading) {
    return <BurndownChartSkeleton height={height} />;
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-destructive" />
            Error Loading Burndown
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Failed to load burndown chart data. Please try again.
          </p>
        </CardContent>
      </Card>
    );
  }

  if (!burndown) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Sprint Burndown</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            No burndown data available for this sprint.
          </p>
        </CardContent>
      </Card>
    );
  }

  const TrendIcon = trend.icon;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-base">Sprint Burndown</CardTitle>
            <CardDescription>
              {burndown.total_points} total points |{" "}
              {burndown.remaining_points} remaining
            </CardDescription>
          </div>
          <Badge variant="outline" className={trend.color}>
            <TrendIcon className="w-3 h-3 mr-1" />
            {trend.label || trend.status}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={height}>
          <LineChart
            data={chartData}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 12 }}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              tick={{ fontSize: 12 }}
              tickLine={false}
              axisLine={false}
              domain={[0, "dataMax + 5"]}
              label={{
                value: "Story Points",
                angle: -90,
                position: "insideLeft",
                style: { textAnchor: "middle", fontSize: 12 },
              }}
            />
            <Tooltip
              content={({ active, payload, label }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-popover border rounded-lg shadow-lg p-3">
                      <p className="font-medium text-sm">{label}</p>
                      {payload.map((entry, index) => (
                        <p
                          key={index}
                          className="text-sm"
                          style={{ color: entry.color }}
                        >
                          {entry.name}: {entry.value ?? "N/A"} pts
                        </p>
                      ))}
                    </div>
                  );
                }
                return null;
              }}
            />
            <Legend />

            {/* Ideal burndown line */}
            <Line
              type="linear"
              dataKey="ideal"
              name="Ideal"
              stroke="hsl(var(--muted-foreground))"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={false}
              activeDot={false}
            />

            {/* Actual burndown line */}
            <Line
              type="monotone"
              dataKey="actual"
              name="Actual"
              stroke="hsl(var(--primary))"
              strokeWidth={2}
              dot={{ fill: "hsl(var(--primary))", strokeWidth: 2 }}
              activeDot={{ r: 6 }}
              connectNulls
            />

            {/* Today marker */}
            {todayIndex >= 0 && todayIndex < chartData.length && (
              <ReferenceLine
                x={chartData[todayIndex]?.date}
                stroke="hsl(var(--destructive))"
                strokeWidth={2}
                strokeDasharray="3 3"
                label={{
                  value: "Today",
                  position: "top",
                  fill: "hsl(var(--destructive))",
                  fontSize: 11,
                }}
              />
            )}
          </LineChart>
        </ResponsiveContainer>

        {/* Summary stats */}
        <div className="mt-4 grid grid-cols-3 gap-4 pt-4 border-t">
          <div className="text-center">
            <div className="text-2xl font-bold text-primary">
              {burndown.completed_points}
            </div>
            <div className="text-xs text-muted-foreground">Completed</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-600">
              {burndown.remaining_points}
            </div>
            <div className="text-xs text-muted-foreground">Remaining</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">
              {Math.round(
                (burndown.completed_points / burndown.total_points) * 100
              )}
              %
            </div>
            <div className="text-xs text-muted-foreground">Progress</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

/**
 * Skeleton loader for burndown chart
 */
function BurndownChartSkeleton({ height }: { height: number }) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <Skeleton className="h-5 w-32 mb-2" />
            <Skeleton className="h-4 w-48" />
          </div>
          <Skeleton className="h-6 w-24" />
        </div>
      </CardHeader>
      <CardContent>
        <Skeleton className="w-full" style={{ height }} />
        <div className="mt-4 grid grid-cols-3 gap-4 pt-4 border-t">
          {[1, 2, 3].map((i) => (
            <div key={i} className="text-center">
              <Skeleton className="h-8 w-12 mx-auto mb-1" />
              <Skeleton className="h-3 w-16 mx-auto" />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
