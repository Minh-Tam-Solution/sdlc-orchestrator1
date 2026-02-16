/**
 * =========================================================================
 * CEO Dashboard Page - Executive Governance Intelligence
 * SDLC Orchestrator - Sprint 110 (CEO Dashboard & Observability)
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Framework: SDLC 6.0.6 Quality Assurance System
 *
 * Key Metrics:
 * - Time Saved: 40h → 10h target by Week 8
 * - Auto-Approval Rate: 85% target
 * - Vibecoding Index: <30 average target
 * - False Positive Rate: <10% target
 * =========================================================================
 */

"use client";

import { useState } from "react";
import Link from "next/link";
import {
  useCEODashboardSummary,
  useCEOPendingDecisions,
  useCEOTimeSavedTrend,
  useCEOSystemHealth,
  useResolveCEODecision,
} from "@/hooks/useCEODashboard";
import type {
  TimeRange,
  PendingDecision,
  IndexCategory,
  HealthStatus,
  KillSwitchStatus,
} from "@/lib/types/ceo-dashboard";

// =============================================================================
// Utility Functions
// =============================================================================

function formatHours(hours: number): string {
  return hours.toFixed(1) + "h";
}

function formatPercent(value: number): string {
  return value.toFixed(1) + "%";
}

function getIndexCategoryColor(category: IndexCategory): string {
  switch (category) {
    case "green":
      return "bg-green-100 text-green-800 border-green-200";
    case "yellow":
      return "bg-yellow-100 text-yellow-800 border-yellow-200";
    case "orange":
      return "bg-orange-100 text-orange-800 border-orange-200";
    case "red":
      return "bg-red-100 text-red-800 border-red-200";
    default:
      return "bg-gray-100 text-gray-800 border-gray-200";
  }
}

function getHealthStatusColor(status: HealthStatus): string {
  switch (status) {
    case "excellent":
      return "text-green-600";
    case "good":
      return "text-blue-600";
    case "warning":
      return "text-yellow-600";
    case "critical":
      return "text-red-600";
    default:
      return "text-gray-600";
  }
}

function getKillSwitchColor(status: KillSwitchStatus): string {
  switch (status) {
    case "OFF":
      return "bg-gray-100 text-gray-600";
    case "WARNING":
      return "bg-yellow-100 text-yellow-700";
    case "SOFT":
      return "bg-orange-100 text-orange-700";
    case "FULL":
      return "bg-green-100 text-green-700";
    default:
      return "bg-gray-100 text-gray-600";
  }
}

// =============================================================================
// Icons
// =============================================================================

function ClockIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
    </svg>
  );
}

function ChartPieIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" />
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

function CheckCircleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
    </svg>
  );
}

// ServerIcon - reserved for future system health details view
// eslint-disable-next-line @typescript-eslint/no-unused-vars
function ServerIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 17.25v-.228a4.5 4.5 0 0 0-.12-1.03l-2.268-9.64a3.375 3.375 0 0 0-3.285-2.602H7.923a3.375 3.375 0 0 0-3.285 2.602l-2.268 9.64a4.5 4.5 0 0 0-.12 1.03v.228m19.5 0a3 3 0 0 1-3 3H5.25a3 3 0 0 1-3-3m19.5 0a3 3 0 0 0-3-3H5.25a3 3 0 0 0-3 3m16.5 0h.008v.008h-.008v-.008Zm-3 0h.008v.008h-.008v-.008Z" />
    </svg>
  );
}

function ArrowTrendingUpIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18 9 11.25l4.306 4.306a11.95 11.95 0 0 1 5.814-5.518l2.74-1.22m0 0-5.94-2.281m5.94 2.28-2.28 5.941" />
    </svg>
  );
}

function ArrowTrendingDownIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 6 9 12.75l4.286-4.286a11.948 11.948 0 0 1 4.306 6.43l.776 2.898m0 0 3.182-5.511m-3.182 5.51-5.511-3.181" />
    </svg>
  );
}

// =============================================================================
// Stats Card Component
// =============================================================================

function StatCard({
  title,
  value,
  subtitle,
  icon,
  trend,
  trendDirection,
  status,
}: {
  title: string;
  value: string;
  subtitle?: string;
  icon: React.ReactNode;
  trend?: string;
  trendDirection?: "up" | "down" | "stable";
  status?: "success" | "warning" | "error" | "info";
}) {
  const statusColors = {
    success: "border-l-green-500",
    warning: "border-l-yellow-500",
    error: "border-l-red-500",
    info: "border-l-blue-500",
  };

  return (
    <div
      className={`rounded-lg border border-gray-200 bg-white p-6 border-l-4 ${
        status ? statusColors[status] : "border-l-gray-200"
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-50">
          {icon}
        </div>
        {trend && (
          <div className="flex items-center gap-1">
            {trendDirection === "up" ? (
              <ArrowTrendingUpIcon className="h-4 w-4 text-green-500" />
            ) : trendDirection === "down" ? (
              <ArrowTrendingDownIcon className="h-4 w-4 text-red-500" />
            ) : null}
            <span
              className={`text-sm font-medium ${
                trendDirection === "up"
                  ? "text-green-600"
                  : trendDirection === "down"
                  ? "text-red-600"
                  : "text-gray-500"
              }`}
            >
              {trend}
            </span>
          </div>
        )}
      </div>
      <div className="mt-4">
        <h3 className="text-sm font-medium text-gray-500">{title}</h3>
        <p className="mt-1 text-2xl font-semibold text-gray-900">{value}</p>
        {subtitle && <p className="mt-1 text-xs text-gray-400">{subtitle}</p>}
      </div>
    </div>
  );
}

// =============================================================================
// Vibecoding Index Gauge Component
// =============================================================================

function VibecodingGauge({ value, category }: { value: number; category: IndexCategory }) {
  const rotation = (value / 100) * 180 - 90; // -90 to 90 degrees

  return (
    <div className="flex flex-col items-center">
      <div className="relative h-32 w-64 overflow-hidden">
        {/* Background arc */}
        <div className="absolute inset-0 flex items-end justify-center">
          <div className="h-32 w-64 rounded-t-full bg-gradient-to-r from-green-400 via-yellow-400 via-orange-400 to-red-500 opacity-20" />
        </div>
        {/* Needle */}
        <div className="absolute bottom-0 left-1/2 h-28 w-1 origin-bottom -translate-x-1/2">
          <div
            className="h-full w-full bg-gray-800 transition-transform duration-500"
            style={{ transform: `rotate(${rotation}deg)` }}
          />
        </div>
        {/* Center circle */}
        <div className="absolute bottom-0 left-1/2 h-4 w-4 -translate-x-1/2 translate-y-1/2 rounded-full bg-gray-800" />
      </div>
      {/* Value display */}
      <div className="mt-2 text-center">
        <span className="text-3xl font-bold text-gray-900">{value.toFixed(0)}</span>
        <span className="ml-1 text-sm text-gray-500">/ 100</span>
      </div>
      <span
        className={`mt-2 rounded-full px-3 py-1 text-sm font-medium capitalize ${getIndexCategoryColor(
          category
        )}`}
      >
        {category}
      </span>
    </div>
  );
}

// =============================================================================
// Pending Decision Card Component
// =============================================================================

function PendingDecisionCard({
  decision,
  onResolve,
}: {
  decision: PendingDecision;
  onResolve: (id: string, action: "approved" | "rejected") => void;
}) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span
              className={`rounded-full px-2 py-0.5 text-xs font-medium capitalize ${getIndexCategoryColor(
                decision.category
              )}`}
            >
              {decision.category}
            </span>
            <span className="text-xs text-gray-400">
              {decision.vibecoding_index.toFixed(0)} score
            </span>
          </div>
          <h4 className="mt-2 font-medium text-gray-900 line-clamp-1">
            #{decision.pr_number}: {decision.pr_title}
          </h4>
          <p className="mt-1 text-sm text-gray-500">{decision.project_name}</p>
          <p className="mt-1 text-xs text-gray-400">
            Submitted by {decision.submitter} - Waiting {decision.waiting_hours.toFixed(1)}h
          </p>
        </div>
      </div>

      {/* Top contributors */}
      {decision.top_contributors.length > 0 && (
        <div className="mt-3 border-t border-gray-100 pt-3">
          <p className="text-xs font-medium text-gray-500 mb-1">Top Contributors:</p>
          <div className="flex flex-wrap gap-1">
            {decision.top_contributors.slice(0, 3).map((c, i) => (
              <span
                key={i}
                className="rounded bg-gray-100 px-2 py-0.5 text-xs text-gray-600"
              >
                {c.signal}: {c.contribution.toFixed(0)}%
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="mt-4 flex gap-2">
        <button
          onClick={() => onResolve(decision.id, "approved")}
          className="flex-1 rounded-md bg-green-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-green-700 transition-colors"
        >
          Approve
        </button>
        <button
          onClick={() => onResolve(decision.id, "rejected")}
          className="flex-1 rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700 transition-colors"
        >
          Reject
        </button>
      </div>
    </div>
  );
}

// =============================================================================
// System Health Card Component
// =============================================================================

function SystemHealthCard({
  uptime,
  latency,
  killSwitch,
  status,
  alerts,
}: {
  uptime: number;
  latency: number;
  killSwitch: KillSwitchStatus;
  status: HealthStatus;
  alerts: number;
}) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">System Health</h3>
        <span className={`capitalize font-medium ${getHealthStatusColor(status)}`}>
          {status}
        </span>
      </div>

      <div className="space-y-4">
        {/* Uptime */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Uptime</span>
          <span className="font-medium text-gray-900">{formatPercent(uptime)}</span>
        </div>
        <div className="h-2 rounded-full bg-gray-100">
          <div
            className="h-full rounded-full bg-green-500 transition-all"
            style={{ width: `${uptime}%` }}
          />
        </div>

        {/* Latency */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">API Latency (p95)</span>
          <span
            className={`font-medium ${
              latency < 100 ? "text-green-600" : latency < 200 ? "text-yellow-600" : "text-red-600"
            }`}
          >
            {latency.toFixed(0)}ms
          </span>
        </div>

        {/* Kill Switch */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Kill Switch</span>
          <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${getKillSwitchColor(killSwitch)}`}>
            {killSwitch}
          </span>
        </div>

        {/* Active Alerts */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Active Alerts</span>
          <span
            className={`font-medium ${
              alerts === 0 ? "text-green-600" : alerts < 3 ? "text-yellow-600" : "text-red-600"
            }`}
          >
            {alerts}
          </span>
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// Time Saved Chart Component
// =============================================================================

function TimeSavedChart({
  data,
}: {
  data: Array<{
    week: number;
    time_saved_hours: number;
    baseline_hours: number;
    target_hours: number;
  }>;
}) {
  const maxValue = Math.max(...data.map((d) => d.baseline_hours), 40);

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Time Saved Trend (8 Weeks)</h3>

      <div className="flex items-end gap-2 h-48">
        {data.map((point, index) => {
          const savedHeight = (point.time_saved_hours / maxValue) * 100;
          const targetHeight = (point.target_hours / maxValue) * 100;

          return (
            <div key={index} className="flex-1 flex flex-col items-center">
              <div className="relative w-full h-40 flex items-end justify-center gap-1">
                {/* Saved bar */}
                <div
                  className="w-3 bg-green-500 rounded-t transition-all"
                  style={{ height: `${savedHeight}%` }}
                  title={`Saved: ${point.time_saved_hours.toFixed(1)}h`}
                />
                {/* Target line */}
                <div
                  className="absolute w-full border-t-2 border-dashed border-blue-400"
                  style={{ bottom: `${targetHeight}%` }}
                />
              </div>
              <span className="mt-2 text-xs text-gray-500">W{point.week}</span>
            </div>
          );
        })}
      </div>

      <div className="mt-4 flex items-center justify-center gap-6">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-500 rounded" />
          <span className="text-xs text-gray-500">Time Saved</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 border-t-2 border-dashed border-blue-400" />
          <span className="text-xs text-gray-500">Target</span>
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// Loading Skeleton
// =============================================================================

function DashboardSkeleton() {
  return (
    <div className="animate-pulse space-y-6">
      {/* Stats grid */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="rounded-lg border border-gray-200 bg-white p-6">
            <div className="h-12 w-12 rounded-lg bg-gray-200" />
            <div className="mt-4 space-y-2">
              <div className="h-4 w-24 rounded bg-gray-200" />
              <div className="h-8 w-16 rounded bg-gray-200" />
            </div>
          </div>
        ))}
      </div>

      {/* Content grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 rounded-lg border border-gray-200 bg-white p-6">
          <div className="h-6 w-48 rounded bg-gray-200 mb-4" />
          <div className="h-48 rounded bg-gray-100" />
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <div className="h-6 w-32 rounded bg-gray-200 mb-4" />
          <div className="h-32 w-32 mx-auto rounded-full bg-gray-100" />
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// Main Page Component
// =============================================================================

export default function CEODashboardPage() {
  const [timeRange, setTimeRange] = useState<TimeRange>("this_week");

  // Fetch dashboard data
  const { data: summary, isLoading: summaryLoading, error: summaryError } = useCEODashboardSummary({
    timeRange,
  });
  const { data: pendingDecisions, isLoading: pendingLoading } = useCEOPendingDecisions({ limit: 6 });
  const { data: timeSavedTrend } = useCEOTimeSavedTrend();
  const { data: systemHealth } = useCEOSystemHealth();

  // Mutation for resolving decisions
  const resolveDecision = useResolveCEODecision();

  const handleResolveDecision = (submissionId: string, decision: "approved" | "rejected") => {
    resolveDecision.mutate({
      submissionId,
      request: { decision },
    });
  };

  if (summaryLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">CEO Dashboard</h1>
            <p className="text-sm text-gray-500">Executive Governance Intelligence</p>
          </div>
        </div>
        <DashboardSkeleton />
      </div>
    );
  }

  if (summaryError) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-6">
        <div className="flex items-center gap-3">
          <ExclamationTriangleIcon className="h-6 w-6 text-red-500" />
          <div>
            <h3 className="font-medium text-red-800">Failed to load dashboard</h3>
            <p className="text-sm text-red-600">Please try refreshing the page.</p>
          </div>
        </div>
      </div>
    );
  }

  const timeSaved = summary?.executive_summary?.time_saved;
  const routing = summary?.executive_summary?.routing_breakdown;
  const weekly = summary?.weekly_summary;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">CEO Dashboard</h1>
          <p className="text-sm text-gray-500">Executive Governance Intelligence</p>
        </div>
        <div className="flex items-center gap-4">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value as TimeRange)}
            className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
          >
            <option value="today">Today</option>
            <option value="this_week">This Week</option>
            <option value="last_7_days">Last 7 Days</option>
            <option value="last_30_days">Last 30 Days</option>
          </select>
          <Link
            href="/app/gates"
            className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            View All Gates
          </Link>
        </div>
      </div>

      {/* Executive Summary Stats */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Time Saved This Week"
          value={timeSaved ? formatHours(timeSaved.time_saved_hours) : "0h"}
          subtitle={timeSaved ? `Target: ${formatHours(timeSaved.target_hours)}` : undefined}
          icon={<ClockIcon className="h-6 w-6 text-blue-600" />}
          trend={timeSaved ? `${timeSaved.time_saved_percent.toFixed(0)}%` : undefined}
          trendDirection={timeSaved?.on_track ? "up" : "down"}
          status={timeSaved?.on_track ? "success" : "warning"}
        />
        <StatCard
          title="Auto-Approval Rate"
          value={routing ? formatPercent(routing.auto_approval_rate) : "0%"}
          subtitle="Target: 85%"
          icon={<CheckCircleIcon className="h-6 w-6 text-green-600" />}
          trend={routing?.trend}
          trendDirection={routing && routing.auto_approval_rate >= 85 ? "up" : "down"}
          status={routing && routing.auto_approval_rate >= 85 ? "success" : "warning"}
        />
        <StatCard
          title="Pending Your Review"
          value={String(summary?.executive_summary?.pending_count || 0)}
          subtitle="Orange + Red PRs"
          icon={<ExclamationTriangleIcon className="h-6 w-6 text-orange-600" />}
          status={summary?.executive_summary?.pending_count === 0 ? "success" : "warning"}
        />
        <StatCard
          title="Vibecoding Index Avg"
          value={weekly ? weekly.vibecoding_index_avg.toFixed(0) : "0"}
          subtitle="Target: <30"
          icon={<ChartPieIcon className="h-6 w-6 text-purple-600" />}
          status={weekly && weekly.vibecoding_index_avg < 30 ? "success" : weekly && weekly.vibecoding_index_avg < 60 ? "warning" : "error"}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Time Saved Trend */}
        <div className="lg:col-span-2">
          {timeSavedTrend && timeSavedTrend.length > 0 ? (
            <TimeSavedChart data={timeSavedTrend} />
          ) : (
            <div className="rounded-lg border border-gray-200 bg-white p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Time Saved Trend</h3>
              <div className="h-48 flex items-center justify-center text-gray-400">
                No trend data available yet
              </div>
            </div>
          )}
        </div>

        {/* Vibecoding Index Gauge */}
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
            Vibecoding Index
          </h3>
          {weekly ? (
            <VibecodingGauge
              value={weekly.vibecoding_index_avg}
              category={
                weekly.vibecoding_index_avg <= 30
                  ? "green"
                  : weekly.vibecoding_index_avg <= 60
                  ? "yellow"
                  : weekly.vibecoding_index_avg <= 80
                  ? "orange"
                  : "red"
              }
            />
          ) : (
            <div className="h-40 flex items-center justify-center text-gray-400">
              No data
            </div>
          )}
        </div>
      </div>

      {/* Pending Decisions & System Health */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Pending Decisions Queue */}
        <div className="lg:col-span-2">
          <div className="rounded-lg border border-gray-200 bg-white p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Pending Your Decision
              </h3>
              {pendingDecisions && pendingDecisions.length > 0 && (
                <span className="rounded-full bg-orange-100 px-2 py-1 text-xs font-medium text-orange-700">
                  {pendingDecisions.length} pending
                </span>
              )}
            </div>

            {pendingLoading ? (
              <div className="animate-pulse space-y-3">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="h-24 rounded-lg bg-gray-100" />
                ))}
              </div>
            ) : pendingDecisions && pendingDecisions.length > 0 ? (
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                {pendingDecisions.map((decision) => (
                  <PendingDecisionCard
                    key={decision.id}
                    decision={decision}
                    onResolve={handleResolveDecision}
                  />
                ))}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <CheckCircleIcon className="h-12 w-12 text-green-500 mb-3" />
                <p className="text-gray-600">All caught up!</p>
                <p className="text-sm text-gray-400">No pending decisions require your attention.</p>
              </div>
            )}
          </div>
        </div>

        {/* System Health */}
        {systemHealth && (
          <SystemHealthCard
            uptime={systemHealth.uptime_percent}
            latency={systemHealth.api_latency_p95_ms}
            killSwitch={systemHealth.kill_switch_status}
            status={systemHealth.overall_status}
            alerts={systemHealth.alerts_active}
          />
        )}
      </div>

      {/* Weekly Summary */}
      {weekly && (
        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Weekly Summary</h3>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 lg:grid-cols-6">
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-900">{weekly.total_submissions}</p>
              <p className="text-sm text-gray-500">Total Submissions</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-900">{formatPercent(weekly.compliance_pass_rate)}</p>
              <p className="text-sm text-gray-500">First Pass Rate</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-900">{weekly.total_rejections}</p>
              <p className="text-sm text-gray-500">Rejections</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-900">{formatPercent(weekly.false_positive_rate)}</p>
              <p className="text-sm text-gray-500">False Positive Rate</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-900">{weekly.ceo_overrides}</p>
              <p className="text-sm text-gray-500">CEO Overrides</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-900">
                {weekly.developer_satisfaction_nps !== null
                  ? weekly.developer_satisfaction_nps.toFixed(0)
                  : "N/A"}
              </p>
              <p className="text-sm text-gray-500">Dev NPS</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
