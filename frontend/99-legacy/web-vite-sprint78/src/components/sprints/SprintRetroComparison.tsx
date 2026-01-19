/**
 * =========================================================================
 * SprintRetroComparison - Sprint-over-Sprint Retrospective Comparison
 * SDLC Orchestrator - Sprint 78 Day 5
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 78 Frontend Components
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - Compare current sprint retrospective with previous sprint
 * - Show metrics improvement/decline (delta)
 * - Track action items completion across sprints
 * - Identify recurring issues
 *
 * References:
 * - backend/app/services/retrospective_service.py
 * - docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
 * =========================================================================
 */

import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import {
  useRetroComparison,
  RetroComparison,
  MetricsDelta,
} from "@/hooks/usePlanning";
import {
  AlertTriangle,
  ArrowDown,
  ArrowRight,
  ArrowUp,
  BarChart3,
  CheckCircle2,
  GitCompare,
  Minus,
  RefreshCw,
  Repeat,
  Target,
  TrendingDown,
  TrendingUp,
} from "lucide-react";
import { cn } from "@/lib/utils";

/** Props for SprintRetroComparison */
interface SprintRetroComparisonProps {
  /** Current sprint ID to compare */
  sprintId: string;
  /** Optional previous sprint ID (auto-detected if not provided) */
  previousSprintId?: string;
}

/** Format delta value with sign */
function formatDelta(value: number, isPercentage = true): string {
  const formatted = isPercentage
    ? `${Math.abs(Math.round(value * 100))}%`
    : Math.abs(value).toString();
  if (value > 0) return `+${formatted}`;
  if (value < 0) return `-${formatted}`;
  return formatted;
}

/** Get delta indicator */
function getDeltaIndicator(
  value: number,
  higherIsBetter = true
): { icon: React.ElementType; color: string } {
  if (value === 0) return { icon: Minus, color: "text-gray-500" };
  const isPositive = higherIsBetter ? value > 0 : value < 0;
  return {
    icon: value > 0 ? TrendingUp : TrendingDown,
    color: isPositive ? "text-green-500" : "text-red-500",
  };
}

/**
 * Sprint Retrospective Comparison Component
 * Compares current and previous sprint metrics
 */
export default function SprintRetroComparison({
  sprintId,
  previousSprintId,
}: SprintRetroComparisonProps) {
  const {
    data: comparison,
    isLoading,
    error,
    refetch,
  } = useRetroComparison(sprintId, previousSprintId);

  const [isRefetching, setIsRefetching] = useState(false);

  const handleRefresh = async () => {
    setIsRefetching(true);
    await refetch();
    setIsRefetching(false);
  };

  if (isLoading) {
    return <ComparisonSkeleton />;
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-destructive" />
            Error Loading Comparison
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Failed to load retrospective comparison. Please try again.
          </p>
          <Button
            variant="outline"
            size="sm"
            className="mt-3"
            onClick={handleRefresh}
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Retry
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (!comparison) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <GitCompare className="w-5 h-5 text-muted-foreground" />
            Sprint Comparison
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground py-4 text-center">
            No comparison data available.
          </p>
        </CardContent>
      </Card>
    );
  }

  const { current, previous, metrics_delta, action_items_completed, recurring_issues } =
    comparison;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-base flex items-center gap-2">
              <GitCompare className="w-5 h-5 text-blue-500" />
              Sprint Comparison
            </CardTitle>
            <CardDescription>
              Sprint {current.sprint_number}
              {previous && (
                <>
                  {" "}
                  vs Sprint {previous.sprint_number}
                </>
              )}
            </CardDescription>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleRefresh}
            disabled={isRefetching}
          >
            <RefreshCw
              className={cn("w-4 h-4", isRefetching && "animate-spin")}
            />
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* No Previous Sprint */}
        {!previous && (
          <div className="p-4 bg-muted/50 rounded-lg text-center">
            <p className="text-sm text-muted-foreground">
              This is the first sprint - no previous data for comparison.
            </p>
          </div>
        )}

        {/* Metrics Comparison */}
        {previous && metrics_delta && (
          <>
            {/* Delta Summary Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <DeltaCard
                label="Completion Rate"
                currentValue={current.metrics.completion_rate}
                delta={metrics_delta.completion_rate_change}
                isPercentage
                higherIsBetter
              />
              <DeltaCard
                label="Velocity"
                currentValue={current.metrics.completed_points}
                previousValue={previous.metrics.completed_points}
                delta={metrics_delta.velocity_change}
                isPercentage={false}
                higherIsBetter
                suffix=" SP"
              />
              <DeltaCard
                label="P0 Completion"
                currentValue={current.metrics.p0_completion_rate}
                delta={metrics_delta.p0_completion_change}
                isPercentage
                higherIsBetter
              />
              <DeltaCard
                label="Blocked Items"
                currentValue={current.metrics.blocked_items}
                previousValue={previous.metrics.blocked_items}
                delta={metrics_delta.blocked_items_change}
                isPercentage={false}
                higherIsBetter={false}
                suffix=""
              />
            </div>

            {/* Side-by-Side Comparison */}
            <div className="grid md:grid-cols-2 gap-4">
              {/* Current Sprint */}
              <div className="p-4 rounded-lg border bg-card">
                <h4 className="font-medium text-sm mb-3 flex items-center gap-2">
                  <Target className="w-4 h-4 text-blue-500" />
                  Sprint {current.sprint_number} (Current)
                </h4>
                <div className="space-y-3">
                  <MetricRow
                    label="Committed"
                    value={`${current.metrics.committed_points} SP`}
                  />
                  <MetricRow
                    label="Completed"
                    value={`${current.metrics.completed_points} SP`}
                  />
                  <MetricRow
                    label="Completion"
                    value={`${Math.round(current.metrics.completion_rate * 100)}%`}
                  />
                  <MetricRow
                    label="P0 Items"
                    value={`${current.metrics.p0_completed}/${current.metrics.p0_total}`}
                  />
                  <MetricRow
                    label="Velocity Trend"
                    value={current.metrics.velocity_trend}
                    className="capitalize"
                  />
                </div>
              </div>

              {/* Previous Sprint */}
              <div className="p-4 rounded-lg border bg-muted/50">
                <h4 className="font-medium text-sm mb-3 flex items-center gap-2 text-muted-foreground">
                  <Target className="w-4 h-4" />
                  Sprint {previous.sprint_number} (Previous)
                </h4>
                <div className="space-y-3">
                  <MetricRow
                    label="Committed"
                    value={`${previous.metrics.committed_points} SP`}
                  />
                  <MetricRow
                    label="Completed"
                    value={`${previous.metrics.completed_points} SP`}
                  />
                  <MetricRow
                    label="Completion"
                    value={`${Math.round(previous.metrics.completion_rate * 100)}%`}
                  />
                  <MetricRow
                    label="P0 Items"
                    value={`${previous.metrics.p0_completed}/${previous.metrics.p0_total}`}
                  />
                  <MetricRow
                    label="Velocity Trend"
                    value={previous.metrics.velocity_trend}
                    className="capitalize"
                  />
                </div>
              </div>
            </div>

            {/* Action Items Progress */}
            <div className="p-4 rounded-lg border">
              <h4 className="font-medium text-sm mb-3 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-green-500" />
                Action Items from Previous Sprint
              </h4>
              {previous.action_items.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  No action items from previous sprint.
                </p>
              ) : (
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Completed</span>
                    <span className="font-medium">
                      {action_items_completed} / {previous.action_items.length}
                    </span>
                  </div>
                  <Progress
                    value={
                      (action_items_completed / previous.action_items.length) *
                      100
                    }
                    className="h-2"
                  />
                  <p className="text-xs text-muted-foreground">
                    {Math.round(
                      (action_items_completed / previous.action_items.length) *
                        100
                    )}
                    % of action items were addressed this sprint
                  </p>
                </div>
              )}
            </div>

            {/* Recurring Issues */}
            {recurring_issues.length > 0 && (
              <div className="p-4 rounded-lg border border-orange-200 bg-orange-50">
                <h4 className="font-medium text-sm mb-3 flex items-center gap-2 text-orange-700">
                  <Repeat className="w-4 h-4" />
                  Recurring Issues ({recurring_issues.length})
                </h4>
                <p className="text-xs text-orange-600 mb-2">
                  These issues appeared in both sprints and need attention:
                </p>
                <ul className="space-y-1">
                  {recurring_issues.map((issue, idx) => (
                    <li
                      key={idx}
                      className="text-sm text-orange-700 flex items-start gap-2"
                    >
                      <AlertTriangle className="w-3 h-3 mt-1 flex-shrink-0" />
                      {issue}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}

        {/* Current Sprint Summary */}
        <div className="p-4 rounded-lg bg-muted/50">
          <h4 className="font-medium text-sm mb-2">Summary</h4>
          <p className="text-sm text-muted-foreground">{current.summary}</p>
        </div>
      </CardContent>
    </Card>
  );
}

/** Delta metric card */
function DeltaCard({
  label,
  currentValue,
  previousValue,
  delta,
  isPercentage,
  higherIsBetter,
  suffix = "",
}: {
  label: string;
  currentValue: number;
  previousValue?: number;
  delta: number;
  isPercentage: boolean;
  higherIsBetter: boolean;
  suffix?: string;
}) {
  const indicator = getDeltaIndicator(delta, higherIsBetter);
  const Icon = indicator.icon;

  const displayValue = isPercentage
    ? `${Math.round(currentValue * 100)}%`
    : `${currentValue}${suffix}`;

  return (
    <div className="p-3 rounded-lg bg-muted">
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs text-muted-foreground">{label}</span>
        <Icon className={cn("w-3 h-3", indicator.color)} />
      </div>
      <div className="text-lg font-bold">{displayValue}</div>
      <div className={cn("text-xs", indicator.color)}>
        {formatDelta(delta, isPercentage)}
      </div>
    </div>
  );
}

/** Metric row component */
function MetricRow({
  label,
  value,
  className,
}: {
  label: string;
  value: string;
  className?: string;
}) {
  return (
    <div className="flex items-center justify-between text-sm">
      <span className="text-muted-foreground">{label}</span>
      <span className={cn("font-medium", className)}>{value}</span>
    </div>
  );
}

/** Skeleton loader for comparison */
function ComparisonSkeleton() {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <Skeleton className="h-5 w-40 mb-2" />
            <Skeleton className="h-4 w-56" />
          </div>
          <Skeleton className="h-8 w-8" />
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-20 w-full rounded-lg" />
          ))}
        </div>
        <div className="grid md:grid-cols-2 gap-4">
          <Skeleton className="h-40 w-full rounded-lg" />
          <Skeleton className="h-40 w-full rounded-lg" />
        </div>
        <Skeleton className="h-24 w-full rounded-lg" />
      </CardContent>
    </Card>
  );
}
