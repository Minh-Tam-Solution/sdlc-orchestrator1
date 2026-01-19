/**
 * =========================================================================
 * SprintsPage - Sprint List and Management
 * SDLC Orchestrator - Sprint 75 Day 4
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 75 Sprint Dashboard UI
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - Display project sprints in responsive grid
 * - Search and filter sprints by status
 * - Create new sprints
 * - Navigate to sprint detail pages
 * - Show G-Sprint/G-Sprint-Close gate status
 *
 * SDLC 5.1.3 Compliance:
 * - Rule #1: Sprint numbers immutable (visual display)
 * - G-Sprint/G-Sprint-Close: Gate status badges
 * - SE4H Coach: Visual indicator for approval needed
 * =========================================================================
 */

import { useState, useMemo } from "react";
import { Link, useSearchParams } from "react-router-dom";
import {
  Plus,
  Search,
  Calendar,
  Target,
  CheckCircle2,
  Clock,
  AlertCircle,
  PlayCircle,
  PauseCircle,
  XCircle,
  Filter,
} from "lucide-react";
import { useProjectSprints, Sprint, SprintStatus, GateStatus } from "@/hooks/usePlanning";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import CreateSprintDialog from "@/components/sprints/CreateSprintDialog";

/**
 * Sprints List Page
 * Shows all sprints for a project with search and filter functionality
 */
export default function SprintsPage() {
  const [searchParams] = useSearchParams();
  const projectId = searchParams.get("project");

  const { data: sprintsData, isLoading } = useProjectSprints(projectId);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<SprintStatus | "all">("all");
  const [showCreateDialog, setShowCreateDialog] = useState(false);

  // Filter sprints by search query and status
  const filteredSprints = useMemo(() => {
    if (!sprintsData?.items) return [];

    return sprintsData.items.filter((sprint) => {
      const matchesSearch =
        sprint.name.toLowerCase().includes(search.toLowerCase()) ||
        sprint.goal?.toLowerCase().includes(search.toLowerCase()) ||
        `S${sprint.number}`.toLowerCase().includes(search.toLowerCase());

      const matchesStatus =
        statusFilter === "all" || sprint.status === statusFilter;

      return matchesSearch && matchesStatus;
    });
  }, [sprintsData?.items, search, statusFilter]);

  // Sort sprints by number (descending - newest first)
  const sortedSprints = useMemo(() => {
    return [...filteredSprints].sort((a, b) => b.number - a.number);
  }, [filteredSprints]);

  // Stats for header
  const stats = useMemo(() => {
    if (!sprintsData?.items) return { total: 0, active: 0, completed: 0 };

    return {
      total: sprintsData.items.length,
      active: sprintsData.items.filter(
        (s) => s.status === "in_progress" || s.status === "planning"
      ).length,
      completed: sprintsData.items.filter(
        (s) => s.status === "completed" || s.status === "closed"
      ).length,
    };
  }, [sprintsData?.items]);

  if (!projectId) {
    return (
      <div className="container mx-auto py-6">
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <AlertCircle className="w-12 h-12 text-muted-foreground mb-4" />
          <h3 className="text-lg font-medium mb-2">No project selected</h3>
          <p className="text-muted-foreground mb-4 max-w-md">
            Please select a project to view its sprints.
          </p>
          <Link to="/projects">
            <Button>Go to Projects</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Sprints</h1>
          <p className="text-muted-foreground mt-1">
            Manage sprints and track progress with G-Sprint gates
          </p>
        </div>
        <Button onClick={() => setShowCreateDialog(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Create Sprint
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Sprints</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active</CardTitle>
            <PlayCircle className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.active}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completed</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.completed}</div>
          </CardContent>
        </Card>
      </div>

      {/* Search and Filter Bar */}
      <div className="flex items-center gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input
            placeholder="Search sprints by name, goal, or number..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10"
          />
        </div>
        <Select
          value={statusFilter}
          onValueChange={(value) =>
            setStatusFilter(value as SprintStatus | "all")
          }
        >
          <SelectTrigger className="w-[180px]">
            <Filter className="w-4 h-4 mr-2" />
            <SelectValue placeholder="Filter by status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Statuses</SelectItem>
            <SelectItem value="planning">Planning</SelectItem>
            <SelectItem value="in_progress">In Progress</SelectItem>
            <SelectItem value="completed">Completed</SelectItem>
            <SelectItem value="closed">Closed</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Sprints Grid */}
      {isLoading ? (
        <SprintsLoadingSkeleton />
      ) : sortedSprints.length === 0 ? (
        <EmptyState
          hasSearch={search.length > 0 || statusFilter !== "all"}
          onCreateClick={() => setShowCreateDialog(true)}
        />
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {sortedSprints.map((sprint) => (
            <SprintCard key={sprint.id} sprint={sprint} />
          ))}
        </div>
      )}

      {/* Create Sprint Dialog */}
      {projectId && (
        <CreateSprintDialog
          projectId={projectId}
          open={showCreateDialog}
          onOpenChange={setShowCreateDialog}
        />
      )}
    </div>
  );
}

/**
 * Sprint Card Component
 * Displays sprint summary with gate status
 */
interface SprintCardProps {
  sprint: Sprint;
}

function SprintCard({ sprint }: SprintCardProps) {
  const statusConfig = getStatusConfig(sprint.status);
  const gSprintConfig = getGateStatusConfig(sprint.g_sprint_status);
  const gSprintCloseConfig = getGateStatusConfig(sprint.g_sprint_close_status);

  // Calculate days remaining/elapsed
  const daysInfo = getDaysInfo(sprint);

  return (
    <Link to={`/sprints/${sprint.id}`} className="block h-full">
      <Card className="h-full hover:shadow-md transition-shadow cursor-pointer">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="shrink-0">
                  S{sprint.number}
                </Badge>
                <Badge
                  variant={statusConfig.variant}
                  className={`shrink-0 ${statusConfig.className}`}
                >
                  {statusConfig.icon}
                  {statusConfig.label}
                </Badge>
              </div>
              <CardTitle className="mt-2 truncate text-lg">
                {sprint.name}
              </CardTitle>
              {sprint.goal && (
                <CardDescription className="mt-1 line-clamp-2">
                  {sprint.goal}
                </CardDescription>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Sprint Progress (placeholder - would need real data) */}
          <div className="space-y-1">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Progress</span>
              <span className="font-medium">0%</span>
            </div>
            <Progress value={0} className="h-2" />
          </div>

          {/* Sprint Info */}
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            {sprint.capacity_points && (
              <div className="flex items-center gap-1.5">
                <Target className="w-4 h-4" />
                <span>{sprint.capacity_points} SP</span>
              </div>
            )}
            {daysInfo && (
              <div className="flex items-center gap-1.5">
                <Clock className="w-4 h-4" />
                <span>{daysInfo}</span>
              </div>
            )}
          </div>

          {/* Gate Status */}
          <div className="flex items-center gap-2 pt-2 border-t">
            <div className="flex items-center gap-1 text-xs">
              <span
                className={`w-2 h-2 rounded-full ${gSprintConfig.dotColor}`}
              />
              <span className="text-muted-foreground">G-Sprint:</span>
              <span className={gSprintConfig.textColor}>
                {gSprintConfig.label}
              </span>
            </div>
            <div className="flex items-center gap-1 text-xs">
              <span
                className={`w-2 h-2 rounded-full ${gSprintCloseConfig.dotColor}`}
              />
              <span className="text-muted-foreground">G-Close:</span>
              <span className={gSprintCloseConfig.textColor}>
                {gSprintCloseConfig.label}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}

/**
 * Get status configuration for display
 */
function getStatusConfig(status: SprintStatus) {
  switch (status) {
    case "planning":
      return {
        label: "Planning",
        variant: "secondary" as const,
        className: "bg-yellow-100 text-yellow-700 border-yellow-200",
        icon: <PauseCircle className="w-3 h-3 mr-1" />,
      };
    case "in_progress":
      return {
        label: "In Progress",
        variant: "default" as const,
        className: "bg-blue-100 text-blue-700 border-blue-200",
        icon: <PlayCircle className="w-3 h-3 mr-1" />,
      };
    case "completed":
      return {
        label: "Completed",
        variant: "default" as const,
        className: "bg-green-100 text-green-700 border-green-200",
        icon: <CheckCircle2 className="w-3 h-3 mr-1" />,
      };
    case "closed":
      return {
        label: "Closed",
        variant: "outline" as const,
        className: "bg-gray-100 text-gray-700 border-gray-200",
        icon: <XCircle className="w-3 h-3 mr-1" />,
      };
    default:
      return {
        label: status,
        variant: "outline" as const,
        className: "",
        icon: null,
      };
  }
}

/**
 * Get gate status configuration for display
 */
function getGateStatusConfig(status: GateStatus) {
  switch (status) {
    case "pending":
      return {
        label: "Pending",
        dotColor: "bg-yellow-500",
        textColor: "text-yellow-600",
      };
    case "approved":
      return {
        label: "Approved",
        dotColor: "bg-green-500",
        textColor: "text-green-600",
      };
    case "rejected":
      return {
        label: "Rejected",
        dotColor: "bg-red-500",
        textColor: "text-red-600",
      };
    default:
      return {
        label: status,
        dotColor: "bg-gray-500",
        textColor: "text-gray-600",
      };
  }
}

/**
 * Calculate days info for sprint
 */
function getDaysInfo(sprint: Sprint): string | null {
  if (!sprint.start_date) return null;

  const startDate = new Date(sprint.start_date);
  const endDate = sprint.end_date ? new Date(sprint.end_date) : null;
  const today = new Date();

  if (sprint.status === "planning") {
    const daysUntilStart = Math.ceil(
      (startDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24)
    );
    if (daysUntilStart > 0) {
      return `Starts in ${daysUntilStart}d`;
    }
  }

  if (sprint.status === "in_progress" && endDate) {
    const daysRemaining = Math.ceil(
      (endDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24)
    );
    if (daysRemaining > 0) {
      return `${daysRemaining}d left`;
    } else if (daysRemaining === 0) {
      return "Ends today";
    } else {
      return `${Math.abs(daysRemaining)}d overdue`;
    }
  }

  if (sprint.status === "completed" || sprint.status === "closed") {
    if (sprint.closed_at) {
      return `Closed ${formatDate(sprint.closed_at)}`;
    }
    if (endDate) {
      return `Ended ${formatDate(sprint.end_date!)}`;
    }
  }

  return null;
}

/**
 * Format date for display
 */
function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });
}

/**
 * Empty State Component
 * Shows when no sprints exist or search returns no results
 */
interface EmptyStateProps {
  hasSearch: boolean;
  onCreateClick: () => void;
}

function EmptyState({ hasSearch, onCreateClick }: EmptyStateProps) {
  if (hasSearch) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center">
        <Search className="w-12 h-12 text-muted-foreground mb-4" />
        <h3 className="text-lg font-medium mb-2">No sprints found</h3>
        <p className="text-muted-foreground mb-4 max-w-md">
          No sprints match your search criteria. Try a different search term or
          filter.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="rounded-full bg-muted p-4 mb-4">
        <Calendar className="w-12 h-12 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-medium mb-2">No sprints yet</h3>
      <p className="text-muted-foreground mb-6 max-w-md">
        Create your first sprint to start planning your development work. Each
        sprint requires G-Sprint approval before starting.
      </p>
      <Button onClick={onCreateClick}>
        <Plus className="w-4 h-4 mr-2" />
        Create your first sprint
      </Button>
    </div>
  );
}

/**
 * Loading Skeleton Component
 * Shows while sprints data is loading
 */
function SprintsLoadingSkeleton() {
  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <Card key={i}>
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2 mb-2">
              <Skeleton className="h-5 w-12" />
              <Skeleton className="h-5 w-24" />
            </div>
            <Skeleton className="h-6 w-3/4" />
            <Skeleton className="h-4 w-full mt-2" />
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-1">
              <div className="flex items-center justify-between">
                <Skeleton className="h-4 w-16" />
                <Skeleton className="h-4 w-8" />
              </div>
              <Skeleton className="h-2 w-full" />
            </div>
            <div className="flex items-center justify-between">
              <Skeleton className="h-4 w-16" />
              <Skeleton className="h-4 w-20" />
            </div>
            <div className="flex items-center gap-2 pt-2 border-t">
              <Skeleton className="h-4 w-24" />
              <Skeleton className="h-4 w-24" />
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
