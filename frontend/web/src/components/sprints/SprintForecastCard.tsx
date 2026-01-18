/**
 * =========================================================================
 * SprintForecastCard - Sprint Completion Forecast Display
 * SDLC Orchestrator - Sprint 77 Day 5
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 77 Frontend & Completion
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - Display sprint completion probability
 * - Show risk factors with severity
 * - Display AI-generated recommendations
 * - Burn rate comparison (current vs required)
 *
 * References:
 * - backend/app/services/forecast_service.py
 * - docs/08-collaborate/01-Sprint-Logs/SPRINT-77-DAY-3-COMPLETE.md
 * =========================================================================
 */

import { useMemo } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { useSprintForecast } from "@/hooks/usePlanning";
import {
  AlertTriangle,
  CheckCircle2,
  XCircle,
  TrendingUp,
  Lightbulb,
  Target,
  Calendar,
  Flame,
} from "lucide-react";
import { cn } from "@/lib/utils";

/** Props for SprintForecastCard */
interface SprintForecastCardProps {
  /** Sprint ID to show forecast for */
  sprintId: string;
}

/**
 * Sprint Forecast Card Component
 * Displays completion probability, risks, and recommendations
 */
export default function SprintForecastCard({
  sprintId,
}: SprintForecastCardProps) {
  const { data: forecast, isLoading, error } = useSprintForecast(sprintId);

  // Determine probability color and icon
  const probabilityConfig = useMemo(() => {
    if (!forecast) return null;

    const prob = forecast.probability;
    if (prob >= 80) {
      return {
        color: "text-green-600",
        bgColor: "bg-green-100",
        borderColor: "border-green-200",
        icon: CheckCircle2,
        label: "High Confidence",
      };
    } else if (prob >= 60) {
      return {
        color: "text-yellow-600",
        bgColor: "bg-yellow-100",
        borderColor: "border-yellow-200",
        icon: TrendingUp,
        label: "Moderate",
      };
    } else if (prob >= 40) {
      return {
        color: "text-orange-600",
        bgColor: "bg-orange-100",
        borderColor: "border-orange-200",
        icon: AlertTriangle,
        label: "At Risk",
      };
    } else {
      return {
        color: "text-red-600",
        bgColor: "bg-red-100",
        borderColor: "border-red-200",
        icon: XCircle,
        label: "Critical",
      };
    }
  }, [forecast]);

  if (isLoading) {
    return <ForecastCardSkeleton />;
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-destructive" />
            Error Loading Forecast
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Failed to load forecast data. Please try again.
          </p>
        </CardContent>
      </Card>
    );
  }

  if (!forecast) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Sprint Forecast</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            No forecast data available for this sprint.
          </p>
        </CardContent>
      </Card>
    );
  }

  const ProbIcon = probabilityConfig?.icon || Target;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-base">Sprint Forecast</CardTitle>
            <CardDescription>
              {forecast.days_elapsed} days elapsed | {forecast.days_remaining}{" "}
              days remaining
            </CardDescription>
          </div>
          <Badge
            variant={forecast.on_track ? "default" : "destructive"}
            className={forecast.on_track ? "bg-green-500" : ""}
          >
            {forecast.on_track ? "On Track" : "Off Track"}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Probability Circle */}
        <div
          className={cn(
            "p-6 rounded-lg border text-center",
            probabilityConfig?.bgColor,
            probabilityConfig?.borderColor
          )}
        >
          <div className="flex items-center justify-center gap-2 mb-2">
            <ProbIcon className={cn("w-6 h-6", probabilityConfig?.color)} />
            <span className={cn("text-4xl font-bold", probabilityConfig?.color)}>
              {Math.round(forecast.probability)}%
            </span>
          </div>
          <div className="text-sm font-medium">Completion Probability</div>
          <div className={cn("text-xs mt-1", probabilityConfig?.color)}>
            {probabilityConfig?.label}
          </div>
        </div>

        {/* Progress */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Progress</span>
            <span className="font-medium">
              {forecast.completed_points} / {forecast.total_points} points
            </span>
          </div>
          <Progress
            value={(forecast.completed_points / forecast.total_points) * 100}
            className="h-2"
          />
        </div>

        {/* Burn Rate Comparison */}
        <div className="grid grid-cols-2 gap-4">
          <div className="p-3 rounded-lg bg-muted">
            <div className="flex items-center gap-2 text-xs text-muted-foreground mb-1">
              <Flame className="w-3 h-3" />
              Current Burn Rate
            </div>
            <div className="text-lg font-bold">
              {forecast.current_burn_rate.toFixed(1)}
              <span className="text-xs font-normal text-muted-foreground">
                {" "}
                pts/day
              </span>
            </div>
          </div>
          <div className="p-3 rounded-lg bg-muted">
            <div className="flex items-center gap-2 text-xs text-muted-foreground mb-1">
              <Target className="w-3 h-3" />
              Required Burn Rate
            </div>
            <div className="text-lg font-bold">
              {forecast.required_burn_rate.toFixed(1)}
              <span className="text-xs font-normal text-muted-foreground">
                {" "}
                pts/day
              </span>
            </div>
          </div>
        </div>

        {/* Predicted End Date */}
        {forecast.predicted_end_date && (
          <div className="flex items-center gap-3 p-3 rounded-lg border">
            <Calendar className="w-5 h-5 text-muted-foreground" />
            <div>
              <div className="text-sm font-medium">Predicted End Date</div>
              <div className="text-xs text-muted-foreground">
                {new Date(forecast.predicted_end_date).toLocaleDateString(
                  "en-US",
                  {
                    weekday: "long",
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                  }
                )}
              </div>
            </div>
          </div>
        )}

        {/* Risks */}
        {forecast.risks.length > 0 && (
          <div className="space-y-2">
            <div className="text-sm font-medium flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-orange-500" />
              Risk Factors ({forecast.risks.length})
            </div>
            <div className="space-y-2">
              {forecast.risks.map((risk, index) => (
                <div
                  key={index}
                  className={cn(
                    "p-3 rounded-lg border",
                    risk.severity === "critical" &&
                      "bg-red-50 border-red-200",
                    risk.severity === "high" &&
                      "bg-orange-50 border-orange-200",
                    risk.severity === "medium" &&
                      "bg-yellow-50 border-yellow-200",
                    risk.severity === "low" && "bg-gray-50 border-gray-200"
                  )}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1">
                      <div className="text-sm font-medium">{risk.message}</div>
                      <div className="text-xs text-muted-foreground mt-1">
                        {risk.recommendation}
                      </div>
                    </div>
                    <Badge
                      variant="outline"
                      className={cn(
                        "capitalize text-xs",
                        risk.severity === "critical" && "border-red-500 text-red-600",
                        risk.severity === "high" &&
                          "border-orange-500 text-orange-600",
                        risk.severity === "medium" &&
                          "border-yellow-500 text-yellow-600",
                        risk.severity === "low" && "border-gray-500 text-gray-600"
                      )}
                    >
                      {risk.severity}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recommendations */}
        {forecast.recommendations.length > 0 && (
          <div className="space-y-2">
            <div className="text-sm font-medium flex items-center gap-2">
              <Lightbulb className="w-4 h-4 text-blue-500" />
              Recommendations
            </div>
            <ul className="space-y-2">
              {forecast.recommendations.map((rec, index) => (
                <li
                  key={index}
                  className="text-sm text-muted-foreground flex items-start gap-2"
                >
                  <span className="text-primary mt-0.5">•</span>
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

/**
 * Skeleton loader for forecast card
 */
function ForecastCardSkeleton() {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <Skeleton className="h-5 w-32 mb-2" />
            <Skeleton className="h-4 w-48" />
          </div>
          <Skeleton className="h-6 w-20" />
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <Skeleton className="h-32 w-full rounded-lg" />
        <div className="space-y-2">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-2 w-full" />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Skeleton className="h-20 w-full rounded-lg" />
          <Skeleton className="h-20 w-full rounded-lg" />
        </div>
        <Skeleton className="h-16 w-full rounded-lg" />
      </CardContent>
    </Card>
  );
}
