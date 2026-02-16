/**
 * Backlog List Component - SDLC Orchestrator
 *
 * @module frontend/src/app/app/sprints/components/BacklogList
 * @description Backlog item list with filtering, sorting, and status management
 * @sdlc SDLC 6.0.6 Framework - Sprint 93 (Planning Hierarchy Part 2)
 * @reference SDLC 6.0.6 Pillar 2: Sprint Planning Governance
 * @status Sprint 93 - Sprint CRUD & Charts
 */

"use client";

import { useState, useMemo } from "react";
import type {
  BacklogItem,
  BacklogItemType,
  BacklogItemPriority,
  BacklogItemStatus,
} from "@/lib/types/planning";
import {
  getBacklogItemTypeIcon,
  getPriorityColor,
} from "@/lib/types/planning";

// =============================================================================
// TYPES
// =============================================================================

interface BacklogListProps {
  items: BacklogItem[];
  onItemClick?: (item: BacklogItem) => void;
  onStatusChange?: (itemId: string, newStatus: BacklogItemStatus) => void;
  onMoveToSprint?: (itemId: string, sprintId: string | null) => void;
  showFilters?: boolean;
  showActions?: boolean;
  emptyMessage?: string;
  className?: string;
  // Multi-select props
  selectable?: boolean;
  selectedIds?: string[];
  onSelectionChange?: (selectedIds: string[]) => void;
}

type SortField = "priority" | "status" | "story_points" | "created_at" | "title";
type SortDirection = "asc" | "desc";

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Get status badge color
 */
function getStatusColor(status: BacklogItemStatus): string {
  const colors: Record<BacklogItemStatus, string> = {
    todo: "bg-gray-100 text-gray-700",
    in_progress: "bg-blue-100 text-blue-700",
    review: "bg-purple-100 text-purple-700",
    done: "bg-green-100 text-green-700",
    carried_over: "bg-orange-100 text-orange-700",
  };
  return colors[status] || "bg-gray-100 text-gray-700";
}

/**
 * Get status label
 */
function getStatusLabel(status: BacklogItemStatus): string {
  const labels: Record<BacklogItemStatus, string> = {
    todo: "To Do",
    in_progress: "In Progress",
    review: "Review",
    done: "Done",
    carried_over: "Carried Over",
  };
  return labels[status] || status;
}

/**
 * Get priority sort order
 */
function getPrioritySortOrder(priority: BacklogItemPriority): number {
  const order: Record<BacklogItemPriority, number> = {
    p0: 0,
    p1: 1,
    p2: 2,
    p3: 3,
  };
  return order[priority] ?? 4;
}

/**
 * Get status sort order
 */
function getStatusSortOrder(status: BacklogItemStatus): number {
  const order: Record<BacklogItemStatus, number> = {
    in_progress: 0,
    review: 1,
    todo: 2,
    carried_over: 3,
    done: 4,
  };
  return order[status] ?? 5;
}

// =============================================================================
// FILTER BAR COMPONENT
// =============================================================================

interface FilterBarProps {
  typeFilter: BacklogItemType | "all";
  setTypeFilter: (type: BacklogItemType | "all") => void;
  priorityFilter: BacklogItemPriority | "all";
  setPriorityFilter: (priority: BacklogItemPriority | "all") => void;
  statusFilter: BacklogItemStatus | "all";
  setStatusFilter: (status: BacklogItemStatus | "all") => void;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
}

function FilterBar({
  typeFilter,
  setTypeFilter,
  priorityFilter,
  setPriorityFilter,
  statusFilter,
  setStatusFilter,
  searchQuery,
  setSearchQuery,
}: FilterBarProps) {
  return (
    <div className="flex flex-wrap items-center gap-3 border-b border-gray-200 px-4 py-3">
      {/* Search */}
      <div className="relative flex-1 min-w-[200px]">
        <input
          type="text"
          placeholder="Search items..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full rounded-md border border-gray-300 px-3 py-1.5 pl-8 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        />
        <svg
          className="absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
          />
        </svg>
      </div>

      {/* Type Filter */}
      <select
        value={typeFilter}
        onChange={(e) => setTypeFilter(e.target.value as BacklogItemType | "all")}
        className="rounded-md border border-gray-300 px-2 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
      >
        <option value="all">All Types</option>
        <option value="story">📖 Story</option>
        <option value="task">✅ Task</option>
        <option value="bug">🐛 Bug</option>
        <option value="spike">🔬 Spike</option>
      </select>

      {/* Priority Filter */}
      <select
        value={priorityFilter}
        onChange={(e) => setPriorityFilter(e.target.value as BacklogItemPriority | "all")}
        className="rounded-md border border-gray-300 px-2 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
      >
        <option value="all">All Priorities</option>
        <option value="p0">P0 - Critical</option>
        <option value="p1">P1 - High</option>
        <option value="p2">P2 - Medium</option>
        <option value="p3">P3 - Low</option>
      </select>

      {/* Status Filter */}
      <select
        value={statusFilter}
        onChange={(e) => setStatusFilter(e.target.value as BacklogItemStatus | "all")}
        className="rounded-md border border-gray-300 px-2 py-1.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
      >
        <option value="all">All Statuses</option>
        <option value="todo">To Do</option>
        <option value="in_progress">In Progress</option>
        <option value="review">Review</option>
        <option value="done">Done</option>
        <option value="carried_over">Carried Over</option>
      </select>
    </div>
  );
}

// =============================================================================
// BACKLOG ITEM ROW COMPONENT
// =============================================================================

interface BacklogItemRowProps {
  item: BacklogItem;
  onClick?: (item: BacklogItem) => void;
  onStatusChange?: (itemId: string, newStatus: BacklogItemStatus) => void;
  showActions?: boolean;
  selectable?: boolean;
  isSelected?: boolean;
  onSelect?: (itemId: string, selected: boolean) => void;
}

function BacklogItemRow({ item, onClick, onStatusChange, showActions, selectable, isSelected, onSelect }: BacklogItemRowProps) {
  const [isStatusMenuOpen, setIsStatusMenuOpen] = useState(false);

  const handleStatusChange = (newStatus: BacklogItemStatus) => {
    if (onStatusChange) {
      onStatusChange(item.id, newStatus);
    }
    setIsStatusMenuOpen(false);
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.stopPropagation();
    onSelect?.(item.id, e.target.checked);
  };

  return (
    <div
      className={`
        group flex items-center gap-3 border-b border-gray-100 px-4 py-3
        hover:bg-gray-50 transition-colors
        ${onClick ? "cursor-pointer" : ""}
        ${isSelected ? "bg-blue-50" : ""}
      `}
      onClick={() => onClick?.(item)}
    >
      {/* Checkbox for selection */}
      {selectable && (
        <input
          type="checkbox"
          checked={isSelected}
          onChange={handleCheckboxChange}
          onClick={(e) => e.stopPropagation()}
          className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />
      )}
      {/* Type Icon */}
      <span className="text-lg" title={item.type}>
        {getBacklogItemTypeIcon(item.type)}
      </span>

      {/* Priority Badge */}
      <span
        className={`inline-flex items-center rounded px-1.5 py-0.5 text-xs font-medium ${getPriorityColor(item.priority)}`}
      >
        {item.priority.toUpperCase()}
      </span>

      {/* Title & Description */}
      <div className="flex-1 min-w-0">
        <h4 className="truncate text-sm font-medium text-gray-900">
          {item.title}
        </h4>
        {item.description && (
          <p className="truncate text-xs text-gray-500">{item.description}</p>
        )}
      </div>

      {/* Labels */}
      {item.labels.length > 0 && (
        <div className="hidden items-center gap-1 sm:flex">
          {item.labels.slice(0, 2).map((label, index) => (
            <span
              key={index}
              className="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600"
            >
              {label}
            </span>
          ))}
          {item.labels.length > 2 && (
            <span className="text-xs text-gray-400">+{item.labels.length - 2}</span>
          )}
        </div>
      )}

      {/* Story Points */}
      {item.story_points !== null && (
        <span className="inline-flex items-center justify-center rounded bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700">
          {item.story_points} SP
        </span>
      )}

      {/* Assignee */}
      {item.assignee_name && (
        <span className="hidden items-center gap-1 text-xs text-gray-500 sm:flex">
          <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
          </svg>
          {item.assignee_name}
        </span>
      )}

      {/* Status Badge / Dropdown */}
      <div className="relative">
        {showActions && onStatusChange ? (
          <>
            <button
              onClick={(e) => {
                e.stopPropagation();
                setIsStatusMenuOpen(!isStatusMenuOpen);
              }}
              className={`inline-flex items-center gap-1 rounded px-2 py-0.5 text-xs font-medium ${getStatusColor(item.status)}`}
            >
              {getStatusLabel(item.status)}
              <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
              </svg>
            </button>
            {isStatusMenuOpen && (
              <div className="absolute right-0 top-full z-10 mt-1 w-36 rounded-md border border-gray-200 bg-white py-1 shadow-lg">
                {(["todo", "in_progress", "review", "done", "carried_over"] as BacklogItemStatus[]).map(
                  (status) => (
                    <button
                      key={status}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleStatusChange(status);
                      }}
                      className={`
                        w-full px-3 py-1.5 text-left text-xs hover:bg-gray-50
                        ${item.status === status ? "bg-gray-100 font-medium" : ""}
                      `}
                    >
                      {getStatusLabel(status)}
                    </button>
                  )
                )}
              </div>
            )}
          </>
        ) : (
          <span className={`inline-flex items-center rounded px-2 py-0.5 text-xs font-medium ${getStatusColor(item.status)}`}>
            {getStatusLabel(item.status)}
          </span>
        )}
      </div>
    </div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function BacklogList({
  items,
  onItemClick,
  onStatusChange,
  showFilters = true,
  showActions = true,
  emptyMessage = "No backlog items found",
  className = "",
  selectable = false,
  selectedIds = [],
  onSelectionChange,
}: BacklogListProps) {
  // Filter state
  const [typeFilter, setTypeFilter] = useState<BacklogItemType | "all">("all");
  const [priorityFilter, setPriorityFilter] = useState<BacklogItemPriority | "all">("all");
  const [statusFilter, setStatusFilter] = useState<BacklogItemStatus | "all">("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [sortField, setSortField] = useState<SortField>("priority");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  // Filter and sort items
  const filteredItems = useMemo(() => {
    let result = [...items];

    // Apply filters
    if (typeFilter !== "all") {
      result = result.filter((item) => item.type === typeFilter);
    }
    if (priorityFilter !== "all") {
      result = result.filter((item) => item.priority === priorityFilter);
    }
    if (statusFilter !== "all") {
      result = result.filter((item) => item.status === statusFilter);
    }
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      result = result.filter(
        (item) =>
          item.title.toLowerCase().includes(query) ||
          item.description?.toLowerCase().includes(query) ||
          item.labels.some((label) => label.toLowerCase().includes(query))
      );
    }

    // Apply sorting
    result.sort((a, b) => {
      let comparison = 0;

      switch (sortField) {
        case "priority":
          comparison = getPrioritySortOrder(a.priority) - getPrioritySortOrder(b.priority);
          break;
        case "status":
          comparison = getStatusSortOrder(a.status) - getStatusSortOrder(b.status);
          break;
        case "story_points":
          comparison = (a.story_points || 0) - (b.story_points || 0);
          break;
        case "created_at":
          comparison = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
          break;
        case "title":
          comparison = a.title.localeCompare(b.title);
          break;
      }

      return sortDirection === "asc" ? comparison : -comparison;
    });

    return result;
  }, [items, typeFilter, priorityFilter, statusFilter, searchQuery, sortField, sortDirection]);

  // Summary counts
  const summary = useMemo(() => {
    return {
      total: items.length,
      filtered: filteredItems.length,
      byStatus: {
        todo: items.filter((i) => i.status === "todo").length,
        in_progress: items.filter((i) => i.status === "in_progress").length,
        review: items.filter((i) => i.status === "review").length,
        done: items.filter((i) => i.status === "done").length,
        carried_over: items.filter((i) => i.status === "carried_over").length,
      },
      totalPoints: items.reduce((sum, i) => sum + (i.story_points || 0), 0),
      completedPoints: items
        .filter((i) => i.status === "done")
        .reduce((sum, i) => sum + (i.story_points || 0), 0),
    };
  }, [items, filteredItems]);

  const toggleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  // Selection handlers
  const handleItemSelect = (itemId: string, selected: boolean) => {
    if (!onSelectionChange) return;
    if (selected) {
      onSelectionChange([...selectedIds, itemId]);
    } else {
      onSelectionChange(selectedIds.filter((id) => id !== itemId));
    }
  };

  const handleSelectAll = () => {
    if (!onSelectionChange) return;
    const allFilteredIds = filteredItems.map((item) => item.id);
    const allSelected = allFilteredIds.every((id) => selectedIds.includes(id));
    if (allSelected) {
      // Deselect all filtered items
      onSelectionChange(selectedIds.filter((id) => !allFilteredIds.includes(id)));
    } else {
      // Select all filtered items
      const combinedIds = [...selectedIds, ...allFilteredIds];
      const newSelection = Array.from(new Set(combinedIds));
      onSelectionChange(newSelection);
    }
  };

  const allFilteredSelected = filteredItems.length > 0 && filteredItems.every((item) => selectedIds.includes(item.id));
  const someFilteredSelected = filteredItems.some((item) => selectedIds.includes(item.id));

  return (
    <div className={`rounded-xl border border-gray-200 bg-white ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-200 px-4 py-3">
        <div className="flex items-center gap-3">
          {selectable && (
            <input
              type="checkbox"
              checked={allFilteredSelected}
              ref={(el) => {
                if (el) el.indeterminate = someFilteredSelected && !allFilteredSelected;
              }}
              onChange={handleSelectAll}
              className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              title="Select all visible items"
            />
          )}
          <div>
            <h3 className="text-sm font-semibold text-gray-900">
              Backlog Items
              {selectable && selectedIds.length > 0 && (
                <span className="ml-2 rounded-full bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-700">
                  {selectedIds.length} selected
                </span>
              )}
            </h3>
            <p className="text-xs text-gray-500">
              {summary.filtered} of {summary.total} items | {summary.completedPoints}/{summary.totalPoints} SP
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {/* Sort dropdown */}
          <select
            value={sortField}
            onChange={(e) => setSortField(e.target.value as SortField)}
            className="rounded-md border border-gray-300 px-2 py-1 text-xs focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value="priority">Sort by Priority</option>
            <option value="status">Sort by Status</option>
            <option value="story_points">Sort by Points</option>
            <option value="created_at">Sort by Created</option>
            <option value="title">Sort by Title</option>
          </select>
          <button
            onClick={() => toggleSort(sortField)}
            className="rounded-md border border-gray-300 p-1 hover:bg-gray-50"
            title={sortDirection === "asc" ? "Ascending" : "Descending"}
          >
            <svg
              className={`h-4 w-4 text-gray-500 transition-transform ${sortDirection === "desc" ? "rotate-180" : ""}`}
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 15.75l7.5-7.5 7.5 7.5" />
            </svg>
          </button>
        </div>
      </div>

      {/* Filters */}
      {showFilters && (
        <FilterBar
          typeFilter={typeFilter}
          setTypeFilter={setTypeFilter}
          priorityFilter={priorityFilter}
          setPriorityFilter={setPriorityFilter}
          statusFilter={statusFilter}
          setStatusFilter={setStatusFilter}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
        />
      )}

      {/* Quick Status Summary */}
      <div className="flex items-center gap-4 border-b border-gray-100 px-4 py-2 text-xs">
        <span className="text-gray-500">
          <span className="font-medium text-gray-700">{summary.byStatus.todo}</span> To Do
        </span>
        <span className="text-gray-500">
          <span className="font-medium text-blue-600">{summary.byStatus.in_progress}</span> In Progress
        </span>
        <span className="text-gray-500">
          <span className="font-medium text-purple-600">{summary.byStatus.review}</span> Review
        </span>
        <span className="text-gray-500">
          <span className="font-medium text-green-600">{summary.byStatus.done}</span> Done
        </span>
        {summary.byStatus.carried_over > 0 && (
          <span className="text-gray-500">
            <span className="font-medium text-orange-600">{summary.byStatus.carried_over}</span> Carried Over
          </span>
        )}
      </div>

      {/* Items List */}
      <div className="max-h-[500px] overflow-y-auto">
        {filteredItems.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-center">
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
                d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25ZM6.75 12h.008v.008H6.75V12Zm0 3h.008v.008H6.75V15Zm0 3h.008v.008H6.75V18Z"
              />
            </svg>
            <p className="text-sm text-gray-500">{emptyMessage}</p>
            {(typeFilter !== "all" || priorityFilter !== "all" || statusFilter !== "all" || searchQuery) && (
              <button
                onClick={() => {
                  setTypeFilter("all");
                  setPriorityFilter("all");
                  setStatusFilter("all");
                  setSearchQuery("");
                }}
                className="mt-2 text-xs text-blue-600 hover:text-blue-700"
              >
                Clear filters
              </button>
            )}
          </div>
        ) : (
          filteredItems.map((item) => (
            <BacklogItemRow
              key={item.id}
              item={item}
              onClick={onItemClick}
              onStatusChange={onStatusChange}
              showActions={showActions}
              selectable={selectable}
              isSelected={selectedIds.includes(item.id)}
              onSelect={handleItemSelect}
            />
          ))
        )}
      </div>
    </div>
  );
}

export default BacklogList;
