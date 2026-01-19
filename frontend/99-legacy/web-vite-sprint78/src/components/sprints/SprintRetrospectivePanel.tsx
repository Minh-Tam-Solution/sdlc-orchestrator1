/**
 * =========================================================================
 * SprintRetrospectivePanel - Sprint Retrospective Display
 * SDLC Orchestrator - Sprint 77 Day 5
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 77 Frontend & Completion
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - Display auto-generated sprint retrospective
 * - Show "Went Well" and "Needs Improvement" insights
 * - Display action items with owners and status
 * - Metrics summary with completion rate
 *
 * References:
 * - backend/app/services/retrospective_service.py
 * - docs/08-collaborate/01-Sprint-Logs/SPRINT-77-DAY-4-COMPLETE.md
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useSprintRetrospective } from "@/hooks/usePlanning";
import {
  AlertTriangle,
  CheckCircle2,
  ThumbsUp,
  ThumbsDown,
  ListChecks,
  BarChart3,
  TrendingUp,
  TrendingDown,
  Minus,
  User,
  Calendar,
  RefreshCw,
  Sparkles,
} from "lucide-react";
import { cn } from "@/lib/utils";

/** Props for SprintRetrospectivePanel */
interface SprintRetrospectivePanelProps {
  /** Sprint ID to show retrospective for */
  sprintId: string;
}

/**
 * Sprint Retrospective Panel Component
 * Displays AI-generated retrospective with insights and actions
 */
export default function SprintRetrospectivePanel({
  sprintId,
}: SprintRetrospectivePanelProps) {
  const {
    data: retrospective,
    isLoading,
    error,
    refetch,
  } = useSprintRetrospective(sprintId);
  const [isRefetching, setIsRefetching] = useState(false);

  const handleRefresh = async () => {
    setIsRefetching(true);
    await refetch();
    setIsRefetching(false);
  };

  if (isLoading) {
    return <RetrospectivePanelSkeleton />;
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-destructive" />
            Error Loading Retrospective
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Failed to load retrospective data. Please try again.
          </p>
          <Button variant="outline" size="sm" className="mt-3" onClick={handleRefresh}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Retry
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (!retrospective) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Sprint Retrospective</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            No retrospective data available for this sprint.
          </p>
        </CardContent>
      </Card>
    );
  }

  const { metrics } = retrospective;

  // Determine completion rating
  const completionRating = getCompletionRating(metrics.completion_rate);

  // Velocity trend icon
  const VelocityIcon =
    metrics.velocity_trend === "improving"
      ? TrendingUp
      : metrics.velocity_trend === "declining"
      ? TrendingDown
      : Minus;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-base flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-purple-500" />
              Sprint Retrospective
            </CardTitle>
            <CardDescription>
              Auto-generated on{" "}
              {new Date(retrospective.generated_at).toLocaleString()}
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
        {/* Summary */}
        <div
          className={cn(
            "p-4 rounded-lg border",
            completionRating.bgColor,
            completionRating.borderColor
          )}
        >
          <div className="text-lg font-medium">{retrospective.summary}</div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <MetricCard
            icon={BarChart3}
            label="Completion"
            value={`${Math.round(metrics.completion_rate * 100)}%`}
            subValue={`${metrics.completed_points}/${metrics.committed_points} pts`}
            className={completionRating.className}
          />
          <MetricCard
            icon={CheckCircle2}
            label="P0 Completion"
            value={`${Math.round(metrics.p0_completion_rate * 100)}%`}
            subValue={`${metrics.p0_completed}/${metrics.p0_total} items`}
            className={
              metrics.p0_completion_rate === 1
                ? "text-green-600"
                : "text-orange-600"
            }
          />
          <MetricCard
            icon={VelocityIcon}
            label="Velocity Trend"
            value={metrics.velocity_trend}
            subValue=""
            className={
              metrics.velocity_trend === "improving"
                ? "text-green-600"
                : metrics.velocity_trend === "declining"
                ? "text-red-600"
                : "text-gray-600"
            }
          />
          <MetricCard
            icon={AlertTriangle}
            label="Blocked Items"
            value={metrics.blocked_items.toString()}
            subValue={`${metrics.items_added_mid_sprint} added mid-sprint`}
            className={
              metrics.blocked_items > 0 ? "text-red-600" : "text-green-600"
            }
          />
        </div>

        {/* Tabs for Insights and Actions */}
        <Tabs defaultValue="insights" className="space-y-4">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="insights" className="flex items-center gap-2">
              <ThumbsUp className="w-4 h-4" />
              Insights ({retrospective.went_well.length + retrospective.needs_improvement.length})
            </TabsTrigger>
            <TabsTrigger value="actions" className="flex items-center gap-2">
              <ListChecks className="w-4 h-4" />
              Actions ({retrospective.action_items.length})
            </TabsTrigger>
          </TabsList>

          {/* Insights Tab */}
          <TabsContent value="insights" className="space-y-4">
            {/* Went Well */}
            <div className="space-y-2">
              <div className="text-sm font-medium flex items-center gap-2 text-green-600">
                <ThumbsUp className="w-4 h-4" />
                What Went Well ({retrospective.went_well.length})
              </div>
              {retrospective.went_well.length === 0 ? (
                <p className="text-sm text-muted-foreground py-2">
                  No positive insights identified.
                </p>
              ) : (
                <div className="space-y-2">
                  {retrospective.went_well.map((insight, index) => (
                    <InsightCard
                      key={index}
                      insight={insight}
                      type="positive"
                    />
                  ))}
                </div>
              )}
            </div>

            {/* Needs Improvement */}
            <div className="space-y-2">
              <div className="text-sm font-medium flex items-center gap-2 text-orange-600">
                <ThumbsDown className="w-4 h-4" />
                Needs Improvement ({retrospective.needs_improvement.length})
              </div>
              {retrospective.needs_improvement.length === 0 ? (
                <p className="text-sm text-muted-foreground py-2">
                  No improvement areas identified.
                </p>
              ) : (
                <div className="space-y-2">
                  {retrospective.needs_improvement.map((insight, index) => (
                    <InsightCard
                      key={index}
                      insight={insight}
                      type="negative"
                    />
                  ))}
                </div>
              )}
            </div>
          </TabsContent>

          {/* Actions Tab */}
          <TabsContent value="actions" className="space-y-2">
            {retrospective.action_items.length === 0 ? (
              <p className="text-sm text-muted-foreground py-4 text-center">
                No action items generated.
              </p>
            ) : (
              <div className="space-y-2">
                {retrospective.action_items.map((action, index) => (
                  <ActionCard key={index} action={action} />
                ))}
              </div>
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}

/** Metric card component */
function MetricCard({
  icon: Icon,
  label,
  value,
  subValue,
  className,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
  subValue: string;
  className?: string;
}) {
  return (
    <div className="p-3 rounded-lg bg-muted">
      <div className="flex items-center gap-1 text-xs text-muted-foreground mb-1">
        <Icon className="w-3 h-3" />
        {label}
      </div>
      <div className={cn("text-lg font-bold capitalize", className)}>{value}</div>
      {subValue && (
        <div className="text-xs text-muted-foreground">{subValue}</div>
      )}
    </div>
  );
}

/** Insight card component */
function InsightCard({
  insight,
  type,
}: {
  insight: {
    category: string;
    title: string;
    description: string;
    impact: string;
  };
  type: "positive" | "negative";
}) {
  return (
    <div
      className={cn(
        "p-3 rounded-lg border",
        type === "positive"
          ? "bg-green-50 border-green-200"
          : "bg-orange-50 border-orange-200"
      )}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1">
          <div className="font-medium text-sm">{insight.title}</div>
          <div className="text-xs text-muted-foreground mt-1">
            {insight.description}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="text-xs capitalize">
            {insight.category}
          </Badge>
          <Badge
            variant={
              insight.impact === "high"
                ? "destructive"
                : insight.impact === "medium"
                ? "default"
                : "secondary"
            }
            className="text-xs capitalize"
          >
            {insight.impact}
          </Badge>
        </div>
      </div>
    </div>
  );
}

/** Action card component */
function ActionCard({
  action,
}: {
  action: {
    id: string;
    description: string;
    owner: string | null;
    due_date: string | null;
    status: string;
    priority: string;
  };
}) {
  const statusConfig = {
    pending: { color: "bg-yellow-100 text-yellow-700", icon: AlertTriangle },
    in_progress: { color: "bg-blue-100 text-blue-700", icon: RefreshCw },
    done: { color: "bg-green-100 text-green-700", icon: CheckCircle2 },
  };

  const config = statusConfig[action.status as keyof typeof statusConfig] || statusConfig.pending;
  const StatusIcon = config.icon;

  return (
    <div className="p-3 rounded-lg border bg-card">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-start gap-3 flex-1">
          <StatusIcon className={cn("w-4 h-4 mt-0.5", config.color.split(" ")[1])} />
          <div className="flex-1">
            <div className="text-sm">{action.description}</div>
            <div className="flex items-center gap-3 mt-2 text-xs text-muted-foreground">
              {action.owner && (
                <span className="flex items-center gap-1">
                  <User className="w-3 h-3" />
                  {action.owner}
                </span>
              )}
              {action.due_date && (
                <span className="flex items-center gap-1">
                  <Calendar className="w-3 h-3" />
                  {new Date(action.due_date).toLocaleDateString()}
                </span>
              )}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Badge
            variant={
              action.priority === "high"
                ? "destructive"
                : action.priority === "medium"
                ? "default"
                : "secondary"
            }
            className="text-xs capitalize"
          >
            {action.priority}
          </Badge>
          <Badge variant="outline" className={cn("text-xs capitalize", config.color)}>
            {action.status.replace("_", " ")}
          </Badge>
        </div>
      </div>
    </div>
  );
}

/** Get completion rating config based on percentage */
function getCompletionRating(rate: number) {
  if (rate >= 0.9) {
    return {
      bgColor: "bg-green-50",
      borderColor: "border-green-200",
      className: "text-green-600",
    };
  } else if (rate >= 0.8) {
    return {
      bgColor: "bg-blue-50",
      borderColor: "border-blue-200",
      className: "text-blue-600",
    };
  } else if (rate >= 0.7) {
    return {
      bgColor: "bg-yellow-50",
      borderColor: "border-yellow-200",
      className: "text-yellow-600",
    };
  } else {
    return {
      bgColor: "bg-red-50",
      borderColor: "border-red-200",
      className: "text-red-600",
    };
  }
}

/**
 * Skeleton loader for retrospective panel
 */
function RetrospectivePanelSkeleton() {
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
        <Skeleton className="h-16 w-full rounded-lg" />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-20 w-full rounded-lg" />
          ))}
        </div>
        <Skeleton className="h-10 w-full" />
        <div className="space-y-2">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-20 w-full rounded-lg" />
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
