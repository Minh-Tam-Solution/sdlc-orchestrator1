/**
 * Sprint Detail Page - SDLC Orchestrator
 *
 * @module frontend/src/app/app/sprints/[id]/page
 * @description Sprint detail view with gate status, items, and metrics
 * @sdlc SDLC 5.1.3 Framework - Sprint 87 (Sprint Governance UI)
 * @reference SDLC 5.1.3 Pillar 2: Sprint Planning Governance
 * @status Sprint 87 - Core Feature Implementation
 */

"use client";

import { useParams } from "next/navigation";
import Link from "next/link";
import { useSprint, useSprintGovernanceMetrics } from "@/hooks/useSprintGovernance";
import {
  getSprintStatusColor,
  getGateStatusColor,
  getGateStatusIcon,
  formatSprintDateRange,
} from "@/lib/types/planning";
import type { GateStatus, SprintStatus } from "@/lib/types/planning";

// =============================================================================
// ICONS
// =============================================================================

function ArrowLeftIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
    </svg>
  );
}

function CalendarIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
    </svg>
  );
}

function ClockIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
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

function ShieldCheckIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z" />
    </svg>
  );
}

function DocumentTextIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
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
 * Gate Status Card
 */
function GateStatusCard({
  title,
  gateType,
  status,
  sprintId,
  approvedAt,
  approvedBy,
}: {
  title: string;
  gateType: "start" | "close";
  status: GateStatus;
  sprintId: string;
  approvedAt: string | null;
  approvedBy: string | null;
}) {
  const isApproved = status === "passed" || status === "conditional";
  const href = `/app/sprints/${sprintId}/${gateType === "start" ? "start-gate" : "close-gate"}`;

  return (
    <Link
      href={href}
      className="block rounded-xl border border-gray-200 bg-white p-6 transition-shadow hover:shadow-md"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div
            className={`flex h-12 w-12 items-center justify-center rounded-xl ${
              status === "passed"
                ? "bg-green-100"
                : status === "conditional"
                  ? "bg-yellow-100"
                  : status === "failed"
                    ? "bg-red-100"
                    : "bg-gray-100"
            }`}
          >
            <ShieldCheckIcon
              className={`h-6 w-6 ${
                status === "passed"
                  ? "text-green-600"
                  : status === "conditional"
                    ? "text-yellow-600"
                    : status === "failed"
                      ? "text-red-600"
                      : "text-gray-500"
              }`}
            />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">{title}</h3>
            <p className="text-sm text-gray-500">
              {gateType === "start" ? "Sprint Start Gate" : "Sprint Close Gate"}
            </p>
          </div>
        </div>
        <div className="text-right">
          <span className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-sm font-medium ${getGateStatusColor(status)}`}>
            <span>{getGateStatusIcon(status)}</span>
            {status.charAt(0).toUpperCase() + status.slice(1)}
          </span>
          {isApproved && approvedAt && (
            <p className="mt-1 text-xs text-gray-500">
              Approved {new Date(approvedAt).toLocaleDateString()}
              {approvedBy && ` by ${approvedBy}`}
            </p>
          )}
        </div>
      </div>
    </Link>
  );
}

/**
 * Sprint Progress Section
 */
function SprintProgressSection({
  progress,
  daysRemaining,
  daysTotal,
  itemsByStatus,
}: {
  progress: number;
  daysRemaining: number;
  daysTotal: number;
  itemsByStatus: {
    planned: number;
    in_progress: number;
    review: number;
    completed: number;
    carried_over: number;
  };
}) {
  const currentDay = daysTotal - daysRemaining;
  const totalItems =
    itemsByStatus.planned +
    itemsByStatus.in_progress +
    itemsByStatus.review +
    itemsByStatus.completed;

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6">
      <h3 className="mb-4 flex items-center gap-2 text-lg font-semibold text-gray-900">
        <ChartBarIcon className="h-5 w-5 text-gray-500" />
        Sprint Progress
      </h3>

      {/* Timeline Progress */}
      <div className="mb-6">
        <div className="mb-2 flex items-center justify-between text-sm">
          <span className="font-medium text-gray-700">
            Day {currentDay} of {daysTotal}
          </span>
          <span className="text-gray-500">
            {daysRemaining} days remaining
          </span>
        </div>
        <div className="relative h-4 w-full overflow-hidden rounded-full bg-gray-200">
          <div
            className="h-4 rounded-full bg-blue-600 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-xs font-medium text-white drop-shadow">{progress}%</span>
          </div>
        </div>
      </div>

      {/* Items by Status */}
      <div className="grid grid-cols-2 gap-4 md:grid-cols-5">
        <div className="rounded-lg bg-gray-50 p-4 text-center">
          <div className="text-2xl font-bold text-gray-700">{itemsByStatus.planned}</div>
          <div className="text-xs text-gray-500">Planned</div>
        </div>
        <div className="rounded-lg bg-blue-50 p-4 text-center">
          <div className="text-2xl font-bold text-blue-700">{itemsByStatus.in_progress}</div>
          <div className="text-xs text-blue-600">In Progress</div>
        </div>
        <div className="rounded-lg bg-yellow-50 p-4 text-center">
          <div className="text-2xl font-bold text-yellow-700">{itemsByStatus.review}</div>
          <div className="text-xs text-yellow-600">Review</div>
        </div>
        <div className="rounded-lg bg-green-50 p-4 text-center">
          <div className="text-2xl font-bold text-green-700">{itemsByStatus.completed}</div>
          <div className="text-xs text-green-600">Completed</div>
        </div>
        <div className="rounded-lg bg-orange-50 p-4 text-center">
          <div className="text-2xl font-bold text-orange-700">{itemsByStatus.carried_over}</div>
          <div className="text-xs text-orange-600">Carried Over</div>
        </div>
      </div>

      {/* Completion Rate */}
      <div className="mt-4 pt-4 border-t border-gray-100">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600">Completion Rate</span>
          <span className="font-semibold text-gray-900">
            {totalItems > 0 ? Math.round((itemsByStatus.completed / totalItems) * 100) : 0}%
          </span>
        </div>
      </div>
    </div>
  );
}

/**
 * Sprint Metrics Card
 */
function SprintMetricsCard({
  metrics,
}: {
  metrics: {
    velocity: number;
    velocity_trend: number;
    completion_rate: number;
    carry_over_rate: number;
    avg_cycle_time_hours: number;
    bugs_found_in_sprint: number;
    bugs_fixed_in_sprint: number;
  } | null;
}) {
  if (!metrics) return null;

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6">
      <h3 className="mb-4 flex items-center gap-2 text-lg font-semibold text-gray-900">
        <DocumentTextIcon className="h-5 w-5 text-gray-500" />
        Sprint Metrics
      </h3>
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">{metrics.velocity}</div>
          <div className="text-xs text-gray-500">Velocity (SP)</div>
          {metrics.velocity_trend !== 0 && (
            <div className={`text-xs ${metrics.velocity_trend > 0 ? "text-green-600" : "text-red-600"}`}>
              {metrics.velocity_trend > 0 ? "+" : ""}{metrics.velocity_trend}% vs avg
            </div>
          )}
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">{metrics.completion_rate}%</div>
          <div className="text-xs text-gray-500">Completion Rate</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-orange-600">{metrics.carry_over_rate}%</div>
          <div className="text-xs text-gray-500">Carry Over Rate</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-purple-600">{metrics.avg_cycle_time_hours}h</div>
          <div className="text-xs text-gray-500">Avg Cycle Time</div>
        </div>
      </div>
      {(metrics.bugs_found_in_sprint > 0 || metrics.bugs_fixed_in_sprint > 0) && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <div className="flex items-center justify-around text-sm">
            <div className="text-center">
              <span className="font-semibold text-red-600">{metrics.bugs_found_in_sprint}</span>
              <span className="ml-1 text-gray-500">bugs found</span>
            </div>
            <div className="text-center">
              <span className="font-semibold text-green-600">{metrics.bugs_fixed_in_sprint}</span>
              <span className="ml-1 text-gray-500">bugs fixed</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Loading Skeleton
 */
function LoadingSkeleton() {
  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center gap-4">
        <div className="h-8 w-8 animate-pulse rounded bg-gray-200" />
        <div>
          <div className="h-8 w-64 animate-pulse rounded bg-gray-200" />
          <div className="mt-2 h-4 w-48 animate-pulse rounded bg-gray-200" />
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="h-32 animate-pulse rounded-xl bg-gray-200" />
        <div className="h-32 animate-pulse rounded-xl bg-gray-200" />
      </div>
      <div className="h-64 animate-pulse rounded-xl bg-gray-200" />
      <div className="h-48 animate-pulse rounded-xl bg-gray-200" />
    </div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export default function SprintDetailPage() {
  const params = useParams();
  const sprintId = params.id as string;

  const { data: sprint, isLoading, error } = useSprint(sprintId);
  const { data: metrics } = useSprintGovernanceMetrics(sprintId);

  if (isLoading) {
    return <LoadingSkeleton />;
  }

  if (error || !sprint) {
    return (
      <div className="flex min-h-[400px] items-center justify-center p-6">
        <div className="text-center">
          <ExclamationTriangleIcon className="mx-auto h-12 w-12 text-red-500" />
          <h3 className="mt-4 text-lg font-semibold text-gray-900">Sprint Not Found</h3>
          <p className="mt-2 text-sm text-gray-500">
            {error instanceof Error ? error.message : "The sprint could not be loaded."}
          </p>
          <Link
            href="/app/sprints"
            className="mt-4 inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            <ArrowLeftIcon className="h-4 w-4" />
            Back to Sprints
          </Link>
        </div>
      </div>
    );
  }

  const sprintStatus = sprint.status as SprintStatus;
  const gSprintStatus = sprint.g_sprint_status as GateStatus;
  const gSprintCloseStatus = sprint.g_sprint_close_status as GateStatus;

  // Calculate days info
  const startDate = new Date(sprint.start_date);
  const endDate = new Date(sprint.end_date);
  const today = new Date();
  const daysTotal = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));
  const daysRemaining = Math.max(0, Math.ceil((endDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24)));
  const progress = Math.min(100, Math.round(((daysTotal - daysRemaining) / daysTotal) * 100));

  // Items by status from Sprint model
  const itemsByStatus = {
    planned: Math.max(0, sprint.items_total - sprint.items_completed - sprint.items_in_progress - sprint.items_carried_over),
    in_progress: sprint.items_in_progress || 0,
    review: 0, // Review status not tracked separately in Sprint model
    completed: sprint.items_completed || 0,
    carried_over: sprint.items_carried_over || 0,
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-6">
        <Link
          href="/app/sprints"
          className="mb-4 inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700"
        >
          <ArrowLeftIcon className="h-4 w-4" />
          Back to Sprint Governance
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-gray-900">
                Sprint {sprint.number}: {sprint.name}
              </h1>
              <span className={`rounded-full px-3 py-1 text-sm font-medium ${getSprintStatusColor(sprintStatus)}`}>
                {sprint.status}
              </span>
            </div>
            <div className="mt-2 flex items-center gap-4 text-sm text-gray-500">
              <span className="flex items-center gap-1">
                <CalendarIcon className="h-4 w-4" />
                {formatSprintDateRange(sprint.start_date, sprint.end_date)}
              </span>
              <span className="flex items-center gap-1">
                <ClockIcon className="h-4 w-4" />
                {daysRemaining > 0 ? `${daysRemaining} days remaining` : "Sprint ended"}
              </span>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Link
              href={`/app/sprints/${sprintId}/start-gate`}
              className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              G-Sprint Gate
            </Link>
            <Link
              href={`/app/sprints/${sprintId}/close-gate`}
              className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              G-Sprint-Close
            </Link>
          </div>
        </div>
        {sprint.goal && (
          <p className="mt-4 text-gray-600">{sprint.goal}</p>
        )}
      </div>

      {/* Gate Status Cards */}
      <div className="mb-6 grid gap-4 md:grid-cols-2">
        <GateStatusCard
          title="G-Sprint"
          gateType="start"
          status={gSprintStatus}
          sprintId={sprintId}
          approvedAt={sprint.g_sprint_evaluated_at}
          approvedBy={null}
        />
        <GateStatusCard
          title="G-Sprint-Close"
          gateType="close"
          status={gSprintCloseStatus}
          sprintId={sprintId}
          approvedAt={sprint.g_sprint_close_evaluated_at}
          approvedBy={null}
        />
      </div>

      {/* Progress Section */}
      <div className="mb-6">
        <SprintProgressSection
          progress={progress}
          daysRemaining={daysRemaining}
          daysTotal={daysTotal}
          itemsByStatus={itemsByStatus}
        />
      </div>

      {/* Metrics Section */}
      {metrics && (
        <div className="mb-6">
          <SprintMetricsCard metrics={metrics} />
        </div>
      )}

      {/* Story Points Summary */}
      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold text-gray-900">Story Points</h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900">{sprint.story_points_planned || 0}</div>
            <div className="text-sm text-gray-500">Planned</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">{sprint.story_points_completed || 0}</div>
            <div className="text-sm text-gray-500">Completed</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">
              {(sprint.story_points_planned || 0) - (sprint.story_points_completed || 0)}
            </div>
            <div className="text-sm text-gray-500">Remaining</div>
          </div>
        </div>
      </div>
    </div>
  );
}
