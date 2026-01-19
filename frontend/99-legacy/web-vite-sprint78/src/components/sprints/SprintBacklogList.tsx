/**
 * =========================================================================
 * SprintBacklogList - Sprint Backlog Items Display
 * SDLC Orchestrator - Sprint 75 Day 4
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 75 Sprint Dashboard UI
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - Display backlog items in sprint
 * - Filter by status and priority
 * - Show item details with assignee
 * - Quick status updates
 *
 * SDLC 5.1.3 Compliance:
 * - Rule #8: P0/P1/P2 priority display
 * - Status transitions: todo → in_progress → review → done
 * =========================================================================
 */

import { useState, useMemo } from "react";
import {
  Plus,
  Search,
  Filter,
  CheckCircle2,
  Circle,
  Clock,
  Eye,
  AlertTriangle,
  Bug,
  FileText,
  Lightbulb,
  BookOpen,
} from "lucide-react";
import {
  BacklogItemWithDetails,
  BacklogItemStatus,
  BacklogItemType,
  Priority,
} from "@/hooks/usePlanning";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

/**
 * SprintBacklogList Props
 */
interface SprintBacklogListProps {
  sprintId: string;
  projectId: string;
  items: BacklogItemWithDetails[];
  isLoading: boolean;
}

/**
 * SprintBacklogList Component
 * Displays and manages sprint backlog items
 */
export default function SprintBacklogList({
  sprintId: _sprintId,
  projectId: _projectId,
  items,
  isLoading,
}: SprintBacklogListProps) {
  // Note: sprintId and projectId will be used for add/edit operations in future
  void _sprintId;
  void _projectId;
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<BacklogItemStatus | "all">(
    "all"
  );
  const [priorityFilter, setPriorityFilter] = useState<Priority | "all">("all");
  const [typeFilter, setTypeFilter] = useState<BacklogItemType | "all">("all");

  // Filter items
  const filteredItems = useMemo(() => {
    return items.filter((item) => {
      const matchesSearch =
        item.title.toLowerCase().includes(search.toLowerCase()) ||
        item.description?.toLowerCase().includes(search.toLowerCase());

      const matchesStatus =
        statusFilter === "all" || item.status === statusFilter;
      const matchesPriority =
        priorityFilter === "all" || item.priority === priorityFilter;
      const matchesType = typeFilter === "all" || item.type === typeFilter;

      return matchesSearch && matchesStatus && matchesPriority && matchesType;
    });
  }, [items, search, statusFilter, priorityFilter, typeFilter]);

  // Group items by status for summary
  const statusSummary = useMemo(() => {
    return {
      todo: items.filter((i) => i.status === "todo").length,
      in_progress: items.filter((i) => i.status === "in_progress").length,
      review: items.filter((i) => i.status === "review").length,
      done: items.filter((i) => i.status === "done").length,
      blocked: items.filter((i) => i.status === "blocked").length,
    };
  }, [items]);

  if (isLoading) {
    return <BacklogLoadingSkeleton />;
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Sprint Backlog</CardTitle>
            <CardDescription>
              {items.length} items in this sprint
            </CardDescription>
          </div>
          <Button size="sm">
            <Plus className="w-4 h-4 mr-2" />
            Add Item
          </Button>
        </div>

        {/* Status Summary */}
        <div className="flex items-center gap-4 pt-2">
          <StatusBadge status="todo" count={statusSummary.todo} />
          <StatusBadge status="in_progress" count={statusSummary.in_progress} />
          <StatusBadge status="review" count={statusSummary.review} />
          <StatusBadge status="done" count={statusSummary.done} />
          {statusSummary.blocked > 0 && (
            <StatusBadge status="blocked" count={statusSummary.blocked} />
          )}
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Filters */}
        <div className="flex items-center gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search items..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10"
            />
          </div>
          <Select
            value={statusFilter}
            onValueChange={(v) => setStatusFilter(v as BacklogItemStatus | "all")}
          >
            <SelectTrigger className="w-[140px]">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="todo">To Do</SelectItem>
              <SelectItem value="in_progress">In Progress</SelectItem>
              <SelectItem value="review">Review</SelectItem>
              <SelectItem value="done">Done</SelectItem>
              <SelectItem value="blocked">Blocked</SelectItem>
            </SelectContent>
          </Select>
          <Select
            value={priorityFilter}
            onValueChange={(v) => setPriorityFilter(v as Priority | "all")}
          >
            <SelectTrigger className="w-[120px]">
              <SelectValue placeholder="Priority" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Priority</SelectItem>
              <SelectItem value="P0">P0 - Must</SelectItem>
              <SelectItem value="P1">P1 - Should</SelectItem>
              <SelectItem value="P2">P2 - Could</SelectItem>
            </SelectContent>
          </Select>
          <Select
            value={typeFilter}
            onValueChange={(v) => setTypeFilter(v as BacklogItemType | "all")}
          >
            <SelectTrigger className="w-[120px]">
              <SelectValue placeholder="Type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Types</SelectItem>
              <SelectItem value="story">Story</SelectItem>
              <SelectItem value="task">Task</SelectItem>
              <SelectItem value="bug">Bug</SelectItem>
              <SelectItem value="spike">Spike</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Items Table */}
        {filteredItems.length === 0 ? (
          <EmptyBacklog
            hasFilters={
              search !== "" ||
              statusFilter !== "all" ||
              priorityFilter !== "all" ||
              typeFilter !== "all"
            }
          />
        ) : (
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[50px]">Status</TableHead>
                  <TableHead className="w-[60px]">Type</TableHead>
                  <TableHead>Title</TableHead>
                  <TableHead className="w-[80px]">Priority</TableHead>
                  <TableHead className="w-[60px] text-right">SP</TableHead>
                  <TableHead className="w-[120px]">Assignee</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredItems.map((item) => (
                  <TableRow key={item.id} className="cursor-pointer hover:bg-muted/50">
                    <TableCell>
                      <StatusIcon status={item.status} />
                    </TableCell>
                    <TableCell>
                      <TypeIcon type={item.type} />
                    </TableCell>
                    <TableCell>
                      <div className="flex flex-col">
                        <span className="font-medium truncate max-w-[300px]">
                          {item.title}
                        </span>
                        {item.children_count > 0 && (
                          <span className="text-xs text-muted-foreground">
                            {item.completed_children_count}/{item.children_count} subtasks
                          </span>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <PriorityBadge priority={item.priority} />
                    </TableCell>
                    <TableCell className="text-right">
                      {item.story_points || "-"}
                    </TableCell>
                    <TableCell>
                      {item.assignee ? (
                        <div className="flex items-center gap-2">
                          <div className="w-6 h-6 rounded-full bg-muted flex items-center justify-center text-xs font-medium">
                            {getInitials(item.assignee.full_name || item.assignee.email)}
                          </div>
                          <span className="text-sm truncate max-w-[80px]">
                            {item.assignee.full_name || item.assignee.email}
                          </span>
                        </div>
                      ) : (
                        <span className="text-muted-foreground text-sm">Unassigned</span>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

/**
 * Status Icon Component
 */
function StatusIcon({ status }: { status: BacklogItemStatus }) {
  const config = getStatusIconConfig(status);
  return (
    <div className={`flex items-center justify-center ${config.className}`}>
      {config.icon}
    </div>
  );
}

function getStatusIconConfig(status: BacklogItemStatus) {
  switch (status) {
    case "todo":
      return {
        icon: <Circle className="w-4 h-4" />,
        className: "text-gray-400",
      };
    case "in_progress":
      return {
        icon: <Clock className="w-4 h-4" />,
        className: "text-blue-500",
      };
    case "review":
      return {
        icon: <Eye className="w-4 h-4" />,
        className: "text-purple-500",
      };
    case "done":
      return {
        icon: <CheckCircle2 className="w-4 h-4" />,
        className: "text-green-500",
      };
    case "blocked":
      return {
        icon: <AlertTriangle className="w-4 h-4" />,
        className: "text-red-500",
      };
    default:
      return {
        icon: <Circle className="w-4 h-4" />,
        className: "text-gray-400",
      };
  }
}

/**
 * Type Icon Component
 */
function TypeIcon({ type }: { type: BacklogItemType }) {
  const config = getTypeIconConfig(type);
  return (
    <div className={`flex items-center justify-center ${config.className}`}>
      {config.icon}
    </div>
  );
}

function getTypeIconConfig(type: BacklogItemType) {
  switch (type) {
    case "story":
      return {
        icon: <BookOpen className="w-4 h-4" />,
        className: "text-blue-500",
      };
    case "task":
      return {
        icon: <FileText className="w-4 h-4" />,
        className: "text-green-500",
      };
    case "bug":
      return {
        icon: <Bug className="w-4 h-4" />,
        className: "text-red-500",
      };
    case "spike":
      return {
        icon: <Lightbulb className="w-4 h-4" />,
        className: "text-yellow-500",
      };
    default:
      return {
        icon: <FileText className="w-4 h-4" />,
        className: "text-gray-500",
      };
  }
}

/**
 * Priority Badge Component
 */
function PriorityBadge({ priority }: { priority: Priority }) {
  const config = getPriorityConfig(priority);
  return (
    <Badge variant="outline" className={config.className}>
      {priority}
    </Badge>
  );
}

function getPriorityConfig(priority: Priority) {
  switch (priority) {
    case "P0":
      return {
        className: "bg-red-100 text-red-700 border-red-200",
      };
    case "P1":
      return {
        className: "bg-yellow-100 text-yellow-700 border-yellow-200",
      };
    case "P2":
      return {
        className: "bg-gray-100 text-gray-700 border-gray-200",
      };
    default:
      return {
        className: "",
      };
  }
}

/**
 * Status Badge Component for summary
 */
function StatusBadge({
  status,
  count,
}: {
  status: BacklogItemStatus;
  count: number;
}) {
  const config = getStatusBadgeConfig(status);
  return (
    <div className={`flex items-center gap-1.5 text-sm ${config.className}`}>
      {config.icon}
      <span>{config.label}:</span>
      <span className="font-medium">{count}</span>
    </div>
  );
}

function getStatusBadgeConfig(status: BacklogItemStatus) {
  switch (status) {
    case "todo":
      return {
        label: "To Do",
        icon: <Circle className="w-3 h-3" />,
        className: "text-gray-600",
      };
    case "in_progress":
      return {
        label: "In Progress",
        icon: <Clock className="w-3 h-3" />,
        className: "text-blue-600",
      };
    case "review":
      return {
        label: "Review",
        icon: <Eye className="w-3 h-3" />,
        className: "text-purple-600",
      };
    case "done":
      return {
        label: "Done",
        icon: <CheckCircle2 className="w-3 h-3" />,
        className: "text-green-600",
      };
    case "blocked":
      return {
        label: "Blocked",
        icon: <AlertTriangle className="w-3 h-3" />,
        className: "text-red-600",
      };
    default:
      return {
        label: status,
        icon: <Circle className="w-3 h-3" />,
        className: "text-gray-600",
      };
  }
}

/**
 * Get initials from name or email
 */
function getInitials(name: string): string {
  if (!name) return "??";
  const parts = name.split(/[\s@]+/);
  if (parts.length >= 2 && parts[0] && parts[1]) {
    const first = parts[0][0] || "";
    const second = parts[1][0] || "";
    return (first + second).toUpperCase();
  }
  return name.slice(0, 2).toUpperCase();
}

/**
 * Empty Backlog Component
 */
function EmptyBacklog({ hasFilters }: { hasFilters: boolean }) {
  if (hasFilters) {
    return (
      <div className="flex flex-col items-center justify-center py-8 text-center">
        <Filter className="w-10 h-10 text-muted-foreground mb-3" />
        <h3 className="text-base font-medium mb-1">No items match filters</h3>
        <p className="text-sm text-muted-foreground">
          Try adjusting your filters to see more items.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center py-8 text-center">
      <FileText className="w-10 h-10 text-muted-foreground mb-3" />
      <h3 className="text-base font-medium mb-1">No backlog items</h3>
      <p className="text-sm text-muted-foreground mb-4">
        Add items to this sprint from the product backlog.
      </p>
      <Button size="sm">
        <Plus className="w-4 h-4 mr-2" />
        Add Item
      </Button>
    </div>
  );
}

/**
 * Loading Skeleton
 */
function BacklogLoadingSkeleton() {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <Skeleton className="h-6 w-32 mb-2" />
            <Skeleton className="h-4 w-24" />
          </div>
          <Skeleton className="h-9 w-24" />
        </div>
        <div className="flex items-center gap-4 pt-2">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-5 w-20" />
          ))}
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-3">
          <Skeleton className="h-10 flex-1" />
          <Skeleton className="h-10 w-32" />
          <Skeleton className="h-10 w-28" />
          <Skeleton className="h-10 w-28" />
        </div>
        <div className="space-y-2">
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="h-12 w-full" />
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
