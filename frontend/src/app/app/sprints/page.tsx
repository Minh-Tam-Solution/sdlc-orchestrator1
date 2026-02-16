/**
 * Sprint Governance Dashboard - SDLC Orchestrator
 *
 * @module frontend/src/app/app/sprints/page
 * @description Main Sprint Governance dashboard showing active sprint, gates, and metrics
 * @sdlc SDLC 6.0.6 Framework - Sprint 87 (Sprint Governance UI)
 * @reference SDLC 6.0.6 Pillar 2: Sprint Planning Governance
 * @status Sprint 87 - Core Feature Implementation
 */

"use client";

import Link from "next/link";
import { useProjects } from "@/hooks/useProjects";
import { useSprintGovernanceDashboard } from "@/hooks/useSprintGovernance";
import { usePlanningHierarchy } from "@/hooks/usePlanningHierarchy";
import { PlanningHierarchyTree } from "./components";
import {
  getSprintStatusColor,
  getGateStatusColor,
  getGateStatusIcon,
  calculateDaysRemaining,
  formatSprintDateRange,
} from "@/lib/types/planning";
import type { GateStatus, SprintStatus } from "@/lib/types/planning";

// =============================================================================
// ICONS
// =============================================================================

function CalendarIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
    </svg>
  );
}

function CheckCircleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
    </svg>
  );
}

function PlusIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
    </svg>
  );
}

function ArrowRightIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
    </svg>
  );
}

function ChartBarIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
    </svg>
  );
}

function ExclamationTriangleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
    </svg>
  );
}

// =============================================================================
// COMPONENTS
// =============================================================================

/**
 * Active Sprint Card - Large card showing current sprint status
 */
function ActiveSprintCard({
  sprint,
}: {
  sprint: {
    id: string;
    name: string;
    number: number;
    goal: string;
    status: string;
    progress_percentage: number;
    days_remaining: number;
    days_total: number;
    g_sprint_status: GateStatus;
    g_sprint_close_status: GateStatus;
    items_by_status: {
      planned: number;
      in_progress: number;
      review: number;
      completed: number;
      carried_over: number;
    };
    story_points: {
      planned: number;
      completed: number;
      remaining: number;
    };
  };
}) {
  return (
    <div className="rounded-xl border border-blue-200 bg-gradient-to-br from-blue-50 to-white p-6 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <span className="text-sm font-medium text-blue-600">Active Sprint</span>
          <h2 className="mt-1 text-xl font-bold text-gray-900">
            Sprint {sprint.number}: {sprint.name}
          </h2>
        </div>
        <Link
          href={`/app/sprints/${sprint.id}`}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          View Details
        </Link>
      </div>

      <p className="mb-4 text-sm text-gray-600">{sprint.goal}</p>

      {/* Progress Bar */}
      <div className="mb-6">
        <div className="mb-2 flex items-center justify-between text-sm">
          <span className="font-medium text-gray-700">
            Day {sprint.days_total - sprint.days_remaining}/{sprint.days_total}
          </span>
          <span className="text-gray-500">{sprint.progress_percentage}% complete</span>
        </div>
        <div className="h-3 w-full overflow-hidden rounded-full bg-gray-200">
          <div
            className="h-3 rounded-full bg-blue-600 transition-all duration-300"
            style={{ width: `${sprint.progress_percentage}%` }}
          />
        </div>
      </div>

      {/* Item Stats */}
      <div className="mb-6 grid grid-cols-4 gap-4">
        <div className="rounded-lg bg-gray-100 p-3 text-center">
          <div className="text-2xl font-bold text-gray-900">{sprint.items_by_status.planned}</div>
          <div className="text-xs text-gray-500">Planned</div>
        </div>
        <div className="rounded-lg bg-blue-100 p-3 text-center">
          <div className="text-2xl font-bold text-blue-700">{sprint.items_by_status.in_progress}</div>
          <div className="text-xs text-blue-600">In Progress</div>
        </div>
        <div className="rounded-lg bg-yellow-100 p-3 text-center">
          <div className="text-2xl font-bold text-yellow-700">{sprint.items_by_status.review}</div>
          <div className="text-xs text-yellow-600">Review</div>
        </div>
        <div className="rounded-lg bg-green-100 p-3 text-center">
          <div className="text-2xl font-bold text-green-700">{sprint.items_by_status.completed}</div>
          <div className="text-xs text-green-600">Completed</div>
        </div>
      </div>

      {/* Gate Status */}
      <div className="flex items-center gap-4 border-t border-gray-200 pt-4">
        <Link
          href={`/app/sprints/${sprint.id}/start-gate`}
          className="flex flex-1 items-center justify-between rounded-lg border border-gray-200 bg-white p-3 hover:bg-gray-50"
        >
          <div className="flex items-center gap-2">
            <span className="text-lg">{getGateStatusIcon(sprint.g_sprint_status)}</span>
            <span className="text-sm font-medium text-gray-700">G-Sprint</span>
          </div>
          <span className={`rounded-full px-2 py-1 text-xs font-medium ${getGateStatusColor(sprint.g_sprint_status)}`}>
            {sprint.g_sprint_status.toUpperCase()}
          </span>
        </Link>

        <Link
          href={`/app/sprints/${sprint.id}/close-gate`}
          className="flex flex-1 items-center justify-between rounded-lg border border-gray-200 bg-white p-3 hover:bg-gray-50"
        >
          <div className="flex items-center gap-2">
            <span className="text-lg">{getGateStatusIcon(sprint.g_sprint_close_status)}</span>
            <span className="text-sm font-medium text-gray-700">G-Sprint-Close</span>
          </div>
          <span className={`rounded-full px-2 py-1 text-xs font-medium ${getGateStatusColor(sprint.g_sprint_close_status)}`}>
            {sprint.g_sprint_close_status.toUpperCase()}
          </span>
        </Link>
      </div>
    </div>
  );
}

/**
 * Upcoming Sprint Card - Smaller card for planned sprints
 */
function UpcomingSprintCard({
  sprint,
}: {
  sprint: {
    id: string;
    name: string;
    number: number;
    start_date: string;
    end_date: string;
    status: string;
    g_sprint_status: GateStatus;
    story_points_planned: number;
  };
}) {
  const daysUntilStart = calculateDaysRemaining(sprint.start_date);
  const sprintStatus = sprint.status as SprintStatus;

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 transition-shadow hover:shadow-md">
      <div className="mb-2 flex items-center justify-between">
        <h3 className="font-semibold text-gray-900">Sprint {sprint.number}</h3>
        <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${getSprintStatusColor(sprintStatus)}`}>
          {sprint.status}
        </span>
      </div>
      <p className="mb-2 text-sm text-gray-600">{sprint.name}</p>
      <div className="mb-3 flex items-center gap-2 text-xs text-gray-500">
        <CalendarIcon className="h-4 w-4" />
        <span>{formatSprintDateRange(sprint.start_date, sprint.end_date)}</span>
      </div>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1 text-xs text-gray-500">
          <span>{sprint.story_points_planned} SP</span>
          <span>•</span>
          <span>{daysUntilStart > 0 ? `Starts in ${daysUntilStart}d` : "Ready to start"}</span>
        </div>
        {sprint.g_sprint_status === "pending" ? (
          <Link
            href={`/app/sprints/${sprint.id}/start-gate`}
            className="rounded-md bg-blue-600 px-3 py-1 text-xs font-medium text-white hover:bg-blue-700"
          >
            Start Sprint
          </Link>
        ) : (
          <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${getGateStatusColor(sprint.g_sprint_status)}`}>
            G-Sprint: {sprint.g_sprint_status}
          </span>
        )}
      </div>
    </div>
  );
}

/**
 * Recent Sprint Row - Compact row for completed sprints
 */
function RecentSprintRow({
  sprint,
}: {
  sprint: {
    id: string;
    name: string;
    number: number;
    closed_at: string;
    completion_rate: number;
    items_completed: number;
    items_total: number;
    g_sprint_close_status: GateStatus;
  };
}) {
  const closedDate = new Date(sprint.closed_at).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });

  return (
    <Link
      href={`/app/sprints/${sprint.id}`}
      className="flex items-center justify-between rounded-lg border border-gray-100 bg-gray-50 px-4 py-3 transition-colors hover:bg-gray-100"
    >
      <div className="flex items-center gap-4">
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-100">
          <CheckCircleIcon className="h-4 w-4 text-green-600" />
        </div>
        <div>
          <span className="font-medium text-gray-900">Sprint {sprint.number}</span>
          <span className="ml-2 text-sm text-gray-500">{sprint.name}</span>
        </div>
      </div>
      <div className="flex items-center gap-4 text-sm">
        <span className="text-gray-500">{closedDate}</span>
        <span className="font-medium text-gray-700">
          {sprint.items_completed}/{sprint.items_total} items
        </span>
        <span
          className={`font-bold ${
            sprint.completion_rate >= 90 ? "text-green-600" : sprint.completion_rate >= 70 ? "text-yellow-600" : "text-red-600"
          }`}
        >
          {sprint.completion_rate}%
        </span>
        <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${getGateStatusColor(sprint.g_sprint_close_status)}`}>
          {getGateStatusIcon(sprint.g_sprint_close_status)}
        </span>
        <ArrowRightIcon className="h-4 w-4 text-gray-400" />
      </div>
    </Link>
  );
}

/**
 * Metrics Summary Card
 */
function MetricsSummary({
  metrics,
}: {
  metrics: {
    avg_velocity: number;
    avg_completion_rate: number;
    total_sprints_completed: number;
    gates_passed: number;
    gates_failed: number;
  };
}) {
  const gatePassRate =
    metrics.gates_passed + metrics.gates_failed > 0
      ? Math.round((metrics.gates_passed / (metrics.gates_passed + metrics.gates_failed)) * 100)
      : 0;

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6">
      <h3 className="mb-4 flex items-center gap-2 text-lg font-semibold text-gray-900">
        <ChartBarIcon className="h-5 w-5 text-gray-500" />
        Sprint Metrics
      </h3>
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">{metrics.avg_velocity}</div>
          <div className="text-xs text-gray-500">Avg Velocity</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">{metrics.avg_completion_rate}%</div>
          <div className="text-xs text-gray-500">Avg Completion</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-purple-600">{metrics.total_sprints_completed}</div>
          <div className="text-xs text-gray-500">Sprints Done</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-indigo-600">{gatePassRate}%</div>
          <div className="text-xs text-gray-500">Gate Pass Rate</div>
        </div>
      </div>
    </div>
  );
}

/**
 * Empty State Component
 */
function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 py-16">
      <CalendarIcon className="mb-4 h-12 w-12 text-gray-400" />
      <h3 className="mb-2 text-lg font-semibold text-gray-900">No Active Sprint</h3>
      <p className="mb-6 max-w-sm text-center text-sm text-gray-500">
        Create your first sprint to start tracking progress with SDLC 6.0.6 Sprint Governance.
      </p>
      <button className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">
        <PlusIcon className="h-4 w-4" />
        Create Sprint
      </button>
    </div>
  );
}

/**
 * Loading Skeleton
 */
function LoadingSkeleton() {
  return (
    <div className="space-y-6">
      <div className="h-64 animate-pulse rounded-xl bg-gray-200" />
      <div className="grid grid-cols-3 gap-4">
        <div className="h-32 animate-pulse rounded-lg bg-gray-200" />
        <div className="h-32 animate-pulse rounded-lg bg-gray-200" />
        <div className="h-32 animate-pulse rounded-lg bg-gray-200" />
      </div>
      <div className="h-24 animate-pulse rounded-xl bg-gray-200" />
    </div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export default function SprintGovernanceDashboard() {
  // Get first project for now (project selector can be added later)
  const { data: projects, isLoading: isLoadingProjects } = useProjects();
  const firstProject = projects?.[0];

  const {
    data: dashboard,
    isLoading: isLoadingDashboard,
    error,
  } = useSprintGovernanceDashboard(firstProject?.id || "");

  // Get planning hierarchy for tree view
  const { data: hierarchy } = usePlanningHierarchy(firstProject?.id || "");

  const isLoading = isLoadingProjects || isLoadingDashboard;

  if (isLoading) {
    return (
      <div className="p-6">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Sprint Governance</h1>
            <p className="text-sm text-gray-500">SDLC 6.0.6 Pillar 2 - Sprint Planning Governance</p>
          </div>
        </div>
        <LoadingSkeleton />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-[400px] items-center justify-center p-6">
        <div className="text-center">
          <ExclamationTriangleIcon className="mx-auto h-12 w-12 text-red-500" />
          <h3 className="mt-4 text-lg font-semibold text-gray-900">Error Loading Dashboard</h3>
          <p className="mt-2 text-sm text-gray-500">
            {error instanceof Error ? error.message : "Failed to load sprint data"}
          </p>
        </div>
      </div>
    );
  }

  if (!firstProject) {
    return (
      <div className="flex min-h-[400px] items-center justify-center p-6">
        <div className="text-center">
          <CalendarIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-4 text-lg font-semibold text-gray-900">No Projects Found</h3>
          <p className="mt-2 text-sm text-gray-500">Create a project first to manage sprints.</p>
          <Link
            href="/app/projects"
            className="mt-4 inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Go to Projects
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Sprint Governance</h1>
          <p className="text-sm text-gray-500">
            SDLC 6.0.6 Pillar 2 - Sprint Planning Governance • {firstProject.name}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            href="/app/planning"
            className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <CalendarIcon className="h-4 w-4" />
            Planning
          </Link>
          <button className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">
            <PlusIcon className="h-4 w-4" />
            New Sprint
          </button>
        </div>
      </div>

      {/* Active Sprint or Empty State */}
      {dashboard?.active_sprint ? (
        <ActiveSprintCard sprint={dashboard.active_sprint} />
      ) : (
        <EmptyState />
      )}

      {/* Upcoming Sprints */}
      {dashboard?.upcoming_sprints && dashboard.upcoming_sprints.length > 0 && (
        <div className="mt-8">
          <h2 className="mb-4 text-lg font-semibold text-gray-900">Upcoming Sprints</h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {dashboard.upcoming_sprints.map((sprint) => (
              <UpcomingSprintCard key={sprint.id} sprint={sprint} />
            ))}
          </div>
        </div>
      )}

      {/* Recent Sprints */}
      {dashboard?.recent_sprints && dashboard.recent_sprints.length > 0 && (
        <div className="mt-8">
          <h2 className="mb-4 text-lg font-semibold text-gray-900">Recently Completed</h2>
          <div className="space-y-2">
            {dashboard.recent_sprints.map((sprint) => (
              <RecentSprintRow key={sprint.id} sprint={sprint} />
            ))}
          </div>
        </div>
      )}

      {/* Metrics Summary */}
      {dashboard?.metrics && (
        <div className="mt-8">
          <MetricsSummary metrics={dashboard.metrics} />
        </div>
      )}

      {/* Planning Hierarchy Preview */}
      {hierarchy?.hierarchy && hierarchy.hierarchy.length > 0 && (
        <div className="mt-8">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Planning Hierarchy</h2>
            <Link
              href="/app/planning"
              className="text-sm font-medium text-blue-600 hover:text-blue-700"
            >
              View Full Hierarchy →
            </Link>
          </div>
          <PlanningHierarchyTree
            hierarchy={hierarchy.hierarchy}
            activeSprintId={hierarchy.active_sprint_id}
            projectName={firstProject?.name}
            defaultExpanded={false}
          />
        </div>
      )}
    </div>
  );
}
