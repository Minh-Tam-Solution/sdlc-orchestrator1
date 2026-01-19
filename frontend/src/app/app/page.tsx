/**
 * Dashboard Home Page - SDLC Orchestrator
 *
 * @module frontend/landing/src/app/(dashboard)/page
 * @description Main dashboard overview with stats and quick actions
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 62 - Route Group Migration (Real API)
 */

"use client";

import { useMemo } from "react";
import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";
import { useProjects } from "@/hooks/useProjects";
import { useGates } from "@/hooks/useGates";
import { useEvidenceList } from "@/hooks/useEvidence";

// Stats card component
function StatsCard({
  title,
  value,
  change,
  changeType,
  icon,
}: {
  title: string;
  value: string;
  change: string;
  changeType: "positive" | "negative" | "neutral";
  icon: React.ReactNode;
}) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6">
      <div className="flex items-center justify-between">
        <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-50">
          {icon}
        </div>
        <span
          className={`text-sm font-medium ${
            changeType === "positive"
              ? "text-green-600"
              : changeType === "negative"
              ? "text-red-600"
              : "text-gray-500"
          }`}
        >
          {change}
        </span>
      </div>
      <div className="mt-4">
        <h3 className="text-sm font-medium text-gray-500">{title}</h3>
        <p className="mt-1 text-2xl font-semibold text-gray-900">{value}</p>
      </div>
    </div>
  );
}

// Quick action button
function QuickAction({
  href,
  title,
  description,
  icon,
}: {
  href: string;
  title: string;
  description: string;
  icon: React.ReactNode;
}) {
  return (
    <Link
      href={href}
      className="flex items-center gap-4 rounded-lg border border-gray-200 bg-white p-4 transition-shadow hover:shadow-md"
    >
      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gray-100">
        {icon}
      </div>
      <div>
        <h3 className="font-medium text-gray-900">{title}</h3>
        <p className="text-sm text-gray-500">{description}</p>
      </div>
    </Link>
  );
}

// Icons
function FolderIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
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

function DocumentIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
    </svg>
  );
}

function CodeBracketIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
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

function ClockIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
    </svg>
  );
}

// Stats loading skeleton
function StatsCardSkeleton() {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 animate-pulse">
      <div className="flex items-center justify-between">
        <div className="h-12 w-12 rounded-lg bg-gray-200" />
        <div className="h-4 w-16 rounded bg-gray-200" />
      </div>
      <div className="mt-4 space-y-2">
        <div className="h-3 w-20 rounded bg-gray-200" />
        <div className="h-6 w-12 rounded bg-gray-200" />
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const { user } = useAuth();

  // Fetch real data from API
  const { data: projects, isLoading: projectsLoading } = useProjects();
  const { data: gatesResponse, isLoading: gatesLoading } = useGates({ page_size: 100 });
  const { data: evidenceResponse, isLoading: evidenceLoading } = useEvidenceList({ page_size: 100 });

  // Calculate stats from real data
  const stats = useMemo(() => {
    const projectCount = projects?.length || 0;
    const gates = gatesResponse?.items || [];
    const gateCount = gates.length;
    const evidenceCount = evidenceResponse?.total || 0;
    const approvedGates = gates.filter((g) => g.status === "APPROVED").length;
    const passRate = gateCount > 0 ? Math.round((approvedGates / gateCount) * 100) : 0;

    return {
      projectCount,
      gateCount,
      evidenceCount,
      passRate,
    };
  }, [projects, gatesResponse, evidenceResponse]);

  const isLoading = projectsLoading || gatesLoading || evidenceLoading;

  return (
    <div className="space-y-6">
      {/* Welcome section */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Xin chào, {user?.name || "User"}!
        </h1>
        <p className="mt-1 text-gray-500">
          Đây là tổng quan về các dự án và hoạt động của bạn.
        </p>
      </div>

      {/* Stats grid */}
      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <StatsCardSkeleton key={i} />
          ))}
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <StatsCard
            title="Projects"
            value={stats.projectCount.toString()}
            change="Active projects"
            changeType="neutral"
            icon={<FolderIcon className="h-6 w-6 text-blue-600" />}
          />
          <StatsCard
            title="Gate Evaluations"
            value={stats.gateCount.toString()}
            change="Total gates"
            changeType="neutral"
            icon={<ShieldCheckIcon className="h-6 w-6 text-blue-600" />}
          />
          <StatsCard
            title="Evidence Items"
            value={stats.evidenceCount.toString()}
            change="Uploaded evidence"
            changeType="neutral"
            icon={<DocumentIcon className="h-6 w-6 text-blue-600" />}
          />
          <StatsCard
            title="Pass Rate"
            value={`${stats.passRate}%`}
            change={stats.passRate >= 90 ? "Excellent" : stats.passRate >= 70 ? "Good" : "Needs attention"}
            changeType={stats.passRate >= 90 ? "positive" : stats.passRate >= 70 ? "neutral" : "negative"}
            icon={<CheckCircleIcon className="h-6 w-6 text-blue-600" />}
          />
        </div>
      )}

      {/* Quick actions */}
      <div>
        <h2 className="mb-4 text-lg font-semibold text-gray-900">Quick Actions</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <QuickAction
            href="/app/projects"
            title="View Projects"
            description="Manage your SDLC projects"
            icon={<FolderIcon className="h-5 w-5 text-gray-600" />}
          />
          <QuickAction
            href="/app/gates"
            title="Evaluate Gate"
            description="Run a gate evaluation"
            icon={<ShieldCheckIcon className="h-5 w-5 text-gray-600" />}
          />
          <QuickAction
            href="/app/codegen"
            title="App Builder"
            description="Generate code with AI"
            icon={<CodeBracketIcon className="h-5 w-5 text-gray-600" />}
          />
        </div>
      </div>

      {/* Recent activity - real data from gates */}
      <div>
        <h2 className="mb-4 text-lg font-semibold text-gray-900">Recent Activity</h2>
        <div className="rounded-lg border border-gray-200 bg-white">
          {gatesLoading ? (
            <div className="divide-y divide-gray-200">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center justify-between p-4 animate-pulse">
                  <div className="flex items-center gap-3">
                    <div className="h-8 w-8 rounded-full bg-gray-200" />
                    <div className="space-y-1">
                      <div className="h-4 w-32 rounded bg-gray-200" />
                      <div className="h-3 w-24 rounded bg-gray-200" />
                    </div>
                  </div>
                  <div className="h-3 w-16 rounded bg-gray-200" />
                </div>
              ))}
            </div>
          ) : (gatesResponse?.items || []).length > 0 ? (
            <div className="divide-y divide-gray-200">
              {(gatesResponse?.items || [])
                .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
                .slice(0, 5)
                .map((gate) => {
                  const isApproved = gate.status === "APPROVED";
                  const isRejected = gate.status === "REJECTED";
                  const statusText = isApproved
                    ? `Gate ${gate.gate_name} approved`
                    : isRejected
                    ? `Gate ${gate.gate_name} rejected`
                    : `Gate ${gate.gate_name} updated`;

                  return (
                    <div key={gate.id} className="flex items-center justify-between p-4">
                      <div className="flex items-center gap-3">
                        <div
                          className={`flex h-8 w-8 items-center justify-center rounded-full ${
                            isApproved
                              ? "bg-green-100"
                              : isRejected
                              ? "bg-red-100"
                              : "bg-yellow-100"
                          }`}
                        >
                          {isApproved ? (
                            <CheckCircleIcon className="h-4 w-4 text-green-600" />
                          ) : isRejected ? (
                            <ShieldCheckIcon className="h-4 w-4 text-red-600" />
                          ) : (
                            <ClockIcon className="h-4 w-4 text-yellow-600" />
                          )}
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-900">{statusText}</p>
                          <p className="text-xs text-gray-500">Stage {gate.stage}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-1 text-xs text-gray-400">
                        <ClockIcon className="h-3 w-3" />
                        <span>{formatRelativeTime(gate.updated_at)}</span>
                      </div>
                    </div>
                  );
                })}
            </div>
          ) : (
            <div className="p-8 text-center text-gray-500">
              <ShieldCheckIcon className="mx-auto h-8 w-8 text-gray-300" />
              <p className="mt-2 text-sm">No recent activity</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Helper to format relative time
function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return "Just now";
  if (diffMins < 60) return `${diffMins} min ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? "s" : ""} ago`;
  if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? "s" : ""} ago`;
  return date.toLocaleDateString("vi-VN", { month: "short", day: "numeric" });
}
