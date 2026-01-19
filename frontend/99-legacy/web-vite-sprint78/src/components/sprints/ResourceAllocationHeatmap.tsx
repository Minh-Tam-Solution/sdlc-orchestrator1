/**
 * =========================================================================
 * ResourceAllocationHeatmap - Team Resource Allocation Visualization
 * SDLC Orchestrator - Sprint 78 Day 5
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 78 Frontend Components
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - Visualize team member allocations across sprints
 * - Show capacity utilization as a heatmap
 * - Highlight over-allocated resources (conflicts)
 * - Support allocation conflict detection
 *
 * References:
 * - backend/app/services/resource_allocation_service.py
 * - docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
 * =========================================================================
 */

import { useMemo, useState } from "react";
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
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import {
  useTeamCapacity,
  useAllocationConflicts,
  MemberCapacity,
  AllocationConflict,
} from "@/hooks/usePlanning";
import {
  AlertTriangle,
  Calendar,
  RefreshCw,
  User,
  Users,
  Flame,
  TrendingUp,
} from "lucide-react";
import { cn } from "@/lib/utils";

/** Props for ResourceAllocationHeatmap */
interface ResourceAllocationHeatmapProps {
  /** Team ID to show allocations for */
  teamId: string;
  /** Start date for capacity calculation */
  startDate: string;
  /** End date for capacity calculation */
  endDate: string;
  /** Optional sprint ID to highlight conflicts for */
  sprintId?: string;
}

/** Get heatmap color based on utilization rate */
function getUtilizationColor(rate: number): string {
  if (rate >= 1.2) return "bg-red-500"; // Over 120% - critical
  if (rate >= 1.0) return "bg-orange-500"; // 100-120% - warning
  if (rate >= 0.8) return "bg-green-500"; // 80-100% - optimal
  if (rate >= 0.5) return "bg-blue-400"; // 50-80% - good
  if (rate >= 0.2) return "bg-blue-200"; // 20-50% - light
  return "bg-gray-100"; // Under 20% - minimal
}

/** Get utilization status label */
function getUtilizationStatus(rate: number): {
  label: string;
  variant: "default" | "destructive" | "secondary";
} {
  if (rate >= 1.0)
    return { label: "Over-allocated", variant: "destructive" };
  if (rate >= 0.8)
    return { label: "Optimal", variant: "default" };
  if (rate >= 0.5)
    return { label: "Available", variant: "secondary" };
  return { label: "Under-utilized", variant: "secondary" };
}

/**
 * Resource Allocation Heatmap Component
 * Visualizes team capacity and allocation across time
 */
export default function ResourceAllocationHeatmap({
  teamId,
  startDate,
  endDate,
  sprintId,
}: ResourceAllocationHeatmapProps) {
  const {
    data: capacity,
    isLoading,
    error,
    refetch,
  } = useTeamCapacity(teamId, startDate, endDate);

  const { data: conflicts } = useAllocationConflicts(sprintId || null);

  const [isRefetching, setIsRefetching] = useState(false);

  const handleRefresh = async () => {
    setIsRefetching(true);
    await refetch();
    setIsRefetching(false);
  };

  // Generate weekly breakdown for heatmap
  const weeklyData = useMemo(() => {
    if (!capacity) return [];

    // For now, just show member capacity overview
    // Future: break down by week
    return capacity.member_capacities;
  }, [capacity]);

  // Find members with conflicts
  const conflictedUsers = useMemo(() => {
    if (!conflicts) return new Set<string>();
    return new Set(conflicts.map((c) => c.user_id));
  }, [conflicts]);

  if (isLoading) {
    return <HeatmapSkeleton />;
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-destructive" />
            Error Loading Capacity
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Failed to load team capacity data. Please try again.
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

  if (!capacity) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Users className="w-5 h-5 text-muted-foreground" />
            Resource Allocation
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground py-4 text-center">
            No capacity data available for this team.
          </p>
        </CardContent>
      </Card>
    );
  }

  const utilizationStatus = getUtilizationStatus(capacity.utilization_rate);

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-base flex items-center gap-2">
              <Flame className="w-5 h-5 text-orange-500" />
              Resource Allocation Heatmap
            </CardTitle>
            <CardDescription>
              {capacity.team_name} • {capacity.start_date} to {capacity.end_date}
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
        {/* Team Summary */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <SummaryCard
            icon={Users}
            label="Team Members"
            value={capacity.member_capacities.length.toString()}
          />
          <SummaryCard
            icon={Calendar}
            label="Total Hours"
            value={capacity.total_hours.toString()}
            subValue="capacity"
          />
          <SummaryCard
            icon={TrendingUp}
            label="Allocated"
            value={`${Math.round(capacity.allocated_hours)}h`}
            subValue={`${Math.round(capacity.utilization_rate * 100)}%`}
            className={
              capacity.utilization_rate >= 1.0
                ? "text-red-600"
                : capacity.utilization_rate >= 0.8
                ? "text-green-600"
                : "text-blue-600"
            }
          />
          <div className="p-3 rounded-lg bg-muted">
            <div className="flex items-center gap-1 text-xs text-muted-foreground mb-1">
              Status
            </div>
            <Badge variant={utilizationStatus.variant}>
              {utilizationStatus.label}
            </Badge>
          </div>
        </div>

        {/* Conflicts Alert */}
        {conflicts && conflicts.length > 0 && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center gap-2 text-sm font-medium text-red-700">
              <AlertTriangle className="w-4 h-4" />
              {conflicts.length} Allocation Conflict
              {conflicts.length > 1 ? "s" : ""} Detected
            </div>
            <div className="mt-2 space-y-1">
              {conflicts.slice(0, 3).map((conflict, idx) => (
                <ConflictItem key={idx} conflict={conflict} />
              ))}
              {conflicts.length > 3 && (
                <p className="text-xs text-red-600">
                  +{conflicts.length - 3} more conflicts
                </p>
              )}
            </div>
          </div>
        )}

        {/* Heatmap Legend */}
        <div className="flex items-center gap-2 text-xs">
          <span className="text-muted-foreground">Utilization:</span>
          <div className="flex items-center gap-1">
            <div className="w-4 h-4 rounded bg-gray-100" />
            <span>0%</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-4 h-4 rounded bg-blue-200" />
            <span>20%</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-4 h-4 rounded bg-blue-400" />
            <span>50%</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-4 h-4 rounded bg-green-500" />
            <span>80%</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-4 h-4 rounded bg-orange-500" />
            <span>100%</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-4 h-4 rounded bg-red-500" />
            <span>120%+</span>
          </div>
        </div>

        {/* Member Heatmap */}
        <div className="space-y-2">
          {capacity.member_capacities.map((member) => (
            <MemberRow
              key={member.user_id}
              member={member}
              hasConflict={conflictedUsers.has(member.user_id)}
            />
          ))}
        </div>

        {/* Empty State */}
        {capacity.member_capacities.length === 0 && (
          <p className="text-sm text-muted-foreground py-4 text-center">
            No team members found.
          </p>
        )}
      </CardContent>
    </Card>
  );
}

/** Summary card component */
function SummaryCard({
  icon: Icon,
  label,
  value,
  subValue,
  className,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
  subValue?: string;
  className?: string;
}) {
  return (
    <div className="p-3 rounded-lg bg-muted">
      <div className="flex items-center gap-1 text-xs text-muted-foreground mb-1">
        <Icon className="w-3 h-3" />
        {label}
      </div>
      <div className={cn("text-lg font-bold", className)}>{value}</div>
      {subValue && (
        <div className="text-xs text-muted-foreground">{subValue}</div>
      )}
    </div>
  );
}

/** Conflict item component */
function ConflictItem({ conflict }: { conflict: AllocationConflict }) {
  return (
    <div className="text-xs text-red-600">
      <span className="font-medium">{conflict.user_name}</span>:{" "}
      {Math.round(conflict.total_allocation)}% allocation from{" "}
      {new Date(conflict.conflict_start).toLocaleDateString()} to{" "}
      {new Date(conflict.conflict_end).toLocaleDateString()}
    </div>
  );
}

/** Member row with heatmap cell */
function MemberRow({
  member,
  hasConflict,
}: {
  member: MemberCapacity;
  hasConflict: boolean;
}) {
  const utilizationColor = getUtilizationColor(member.utilization_rate);

  return (
    <TooltipProvider>
      <div
        className={cn(
          "flex items-center gap-3 p-2 rounded-lg border",
          hasConflict ? "border-red-300 bg-red-50" : "border-transparent"
        )}
      >
        {/* User info */}
        <div className="flex items-center gap-2 w-40">
          <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center">
            <User className="w-4 h-4 text-muted-foreground" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-medium truncate">
              {member.user_name}
            </div>
            <div className="text-xs text-muted-foreground">
              {member.allocations.length} sprint
              {member.allocations.length !== 1 ? "s" : ""}
            </div>
          </div>
        </div>

        {/* Utilization bar */}
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <div className="flex-1 h-6 bg-muted rounded-full overflow-hidden">
              <div
                className={cn("h-full transition-all", utilizationColor)}
                style={{
                  width: `${Math.min(member.utilization_rate * 100, 100)}%`,
                }}
              />
            </div>
            <div className="w-16 text-right text-sm font-medium">
              {Math.round(member.utilization_rate * 100)}%
            </div>
          </div>
        </div>

        {/* Capacity info */}
        <Tooltip>
          <TooltipTrigger asChild>
            <div className="text-xs text-muted-foreground w-24 text-right">
              {Math.round(member.allocated_hours)}/{member.total_hours}h
            </div>
          </TooltipTrigger>
          <TooltipContent>
            <div className="text-xs">
              <p>
                <strong>Total Capacity:</strong> {member.total_hours}h
              </p>
              <p>
                <strong>Allocated:</strong> {Math.round(member.allocated_hours)}h
              </p>
              <p>
                <strong>Available:</strong> {Math.round(member.available_hours)}h
              </p>
            </div>
          </TooltipContent>
        </Tooltip>

        {/* Conflict indicator */}
        {hasConflict && (
          <Tooltip>
            <TooltipTrigger>
              <AlertTriangle className="w-4 h-4 text-red-500" />
            </TooltipTrigger>
            <TooltipContent>
              <p className="text-xs">Over-allocated across sprints</p>
            </TooltipContent>
          </Tooltip>
        )}
      </div>
    </TooltipProvider>
  );
}

/** Skeleton loader for heatmap */
function HeatmapSkeleton() {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <Skeleton className="h-5 w-48 mb-2" />
            <Skeleton className="h-4 w-64" />
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
        <div className="space-y-2">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-12 w-full rounded-lg" />
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
