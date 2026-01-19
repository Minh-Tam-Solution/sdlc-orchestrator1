/**
 * Gates Page - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/app/(dashboard)/gates/page
 * @description Gate management and evaluation page
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 62 - Route Group Migration (Real API)
 */

"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import { useGates, type Gate } from "@/hooks/useGates";

// Gate stage definitions for SDLC 5.0.0
const STAGE_INFO: Record<string, { label: string; fullName: string }> = {
  "00": { label: "WHY", fullName: "G0 - Problem Definition" },
  "01": { label: "WHAT", fullName: "G1 - Solution Validation" },
  "02": { label: "HOW", fullName: "G2 - Design Ready" },
  "03": { label: "INTEGRATE", fullName: "G2.5 - API Ready" },
  "04": { label: "BUILD", fullName: "G3 - Ship Ready" },
  "05": { label: "TEST", fullName: "G3.5 - Test Ready" },
  "06": { label: "DEPLOY", fullName: "G4 - Launch Ready" },
  "07": { label: "OPERATE", fullName: "G4.5 - Ops Ready" },
  "08": { label: "COLLABORATE", fullName: "G5 - Team Ready" },
  "09": { label: "GOVERN", fullName: "G5.5 - Compliance Ready" },
};

// Icons
function ShieldCheckIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z" />
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

function XCircleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
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

function PlayIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
    </svg>
  );
}

// Stage color mapping
const stageColors: Record<string, string> = {
  WHY: "bg-purple-100 text-purple-700",
  WHAT: "bg-indigo-100 text-indigo-700",
  HOW: "bg-blue-100 text-blue-700",
  INTEGRATE: "bg-cyan-100 text-cyan-700",
  BUILD: "bg-green-100 text-green-700",
  TEST: "bg-teal-100 text-teal-700",
  DEPLOY: "bg-yellow-100 text-yellow-700",
  OPERATE: "bg-orange-100 text-orange-700",
  COLLABORATE: "bg-pink-100 text-pink-700",
  GOVERN: "bg-red-100 text-red-700",
};

// Status color mapping
const statusColors: Record<string, string> = {
  DRAFT: "bg-gray-100 text-gray-700",
  PENDING_APPROVAL: "bg-yellow-100 text-yellow-700",
  APPROVED: "bg-green-100 text-green-700",
  REJECTED: "bg-red-100 text-red-700",
};

// Format date helper
function formatDate(dateString: string | null): string {
  if (!dateString) return "N/A";
  return new Date(dateString).toLocaleDateString("vi-VN", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

// Gate card component with real API data
function GateCard({ gate }: { gate: Gate }) {
  const stageInfo = STAGE_INFO[gate.stage] || { label: gate.stage, fullName: gate.gate_name };
  const stageColor = stageColors[stageInfo.label] || stageColors.BUILD;
  const statusColor = statusColors[gate.status] || statusColors.DRAFT;

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50">
            <ShieldCheckIcon className="h-5 w-5 text-blue-600" />
          </div>
          <div>
            <h3 className="font-medium text-gray-900">{gate.gate_name}</h3>
            <p className="text-sm text-gray-500 line-clamp-1">
              {gate.description || "No description"}
            </p>
          </div>
        </div>
        <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${stageColor}`}>
          {stageInfo.label}
        </span>
      </div>

      <div className="mt-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${statusColor}`}>
            {gate.status.replace("_", " ")}
          </span>
          <div className="text-sm">
            <span className="font-medium text-gray-900">{gate.evidence_count}</span>
            <span className="text-gray-500"> evidence</span>
          </div>
          {gate.policy_violations.length > 0 && (
            <div className="text-sm text-red-600">
              {gate.policy_violations.length} violations
            </div>
          )}
        </div>
        <Link
          href={`/app/gates/${gate.id}`}
          className="inline-flex items-center gap-1 rounded-lg border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          <PlayIcon className="h-4 w-4" />
          View
        </Link>
      </div>
    </div>
  );
}

// Gate evaluation row component with real API data
function EvaluationRow({ gate }: { gate: Gate }) {
  const isPassed = gate.status === "APPROVED";
  const isRejected = gate.status === "REJECTED";
  const stageInfo = STAGE_INFO[gate.stage] || { label: gate.stage, fullName: gate.gate_name };

  return (
    <div className="flex items-center justify-between p-4">
      <div className="flex items-center gap-3">
        {isPassed ? (
          <CheckCircleIcon className="h-5 w-5 text-green-500" />
        ) : isRejected ? (
          <XCircleIcon className="h-5 w-5 text-red-500" />
        ) : (
          <ShieldCheckIcon className="h-5 w-5 text-yellow-500" />
        )}
        <div>
          <div className="flex items-center gap-2">
            <span className="font-medium text-gray-900">{gate.gate_name}</span>
            <span className="text-gray-500">-</span>
            <span className="text-gray-700">{stageInfo.label}</span>
          </div>
          <p className="text-sm text-gray-500">
            {gate.approved_at
              ? `Approved on ${formatDate(gate.approved_at)}`
              : `Updated ${formatDate(gate.updated_at)}`}
          </p>
        </div>
      </div>
      <div className="text-right">
        <div className={`text-sm font-medium uppercase ${
          isPassed ? "text-green-600" : isRejected ? "text-red-600" : "text-yellow-600"
        }`}>
          {gate.status.replace("_", " ")}
        </div>
        {gate.approvals.length > 0 && (
          <div className="text-xs text-gray-500">
            {gate.approvals.length} approval{gate.approvals.length > 1 ? "s" : ""}
          </div>
        )}
      </div>
    </div>
  );
}

// Loading skeleton
function GateCardSkeleton() {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 animate-pulse">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-lg bg-gray-200" />
          <div className="space-y-2">
            <div className="h-4 w-32 rounded bg-gray-200" />
            <div className="h-3 w-48 rounded bg-gray-200" />
          </div>
        </div>
        <div className="h-5 w-16 rounded-full bg-gray-200" />
      </div>
      <div className="mt-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="h-5 w-20 rounded bg-gray-200" />
          <div className="h-4 w-16 rounded bg-gray-200" />
        </div>
        <div className="h-8 w-16 rounded bg-gray-200" />
      </div>
    </div>
  );
}

export default function GatesPage() {
  const [selectedStage, setSelectedStage] = useState<string>("all");

  // Fetch gates from API using TanStack Query
  const { data: gatesResponse, isLoading, error } = useGates({ page_size: 100 });

  // Calculate stats from real data
  const stats = useMemo(() => {
    const gates = gatesResponse?.items || [];
    const total = gates.length;
    const approved = gates.filter((g) => g.status === "APPROVED").length;
    const passRate = total > 0 ? Math.round((approved / total) * 100) : 0;
    return { total, approved, passRate };
  }, [gatesResponse]);

  // Filter gates by stage
  const filteredGates = useMemo(() => {
    const gates = gatesResponse?.items || [];
    if (selectedStage === "all") return gates;
    const stageLabel = selectedStage;
    return gates.filter((gate) => {
      const stageInfo = STAGE_INFO[gate.stage];
      return stageInfo?.label === stageLabel;
    });
  }, [gatesResponse, selectedStage]);

  // Get recent gates (last 5, sorted by updated_at)
  const recentGates = useMemo(() => {
    const gates = gatesResponse?.items || [];
    return [...gates]
      .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
      .slice(0, 5);
  }, [gatesResponse]);

  // Available stages for filter
  const stages = ["all", "WHY", "WHAT", "HOW", "BUILD", "TEST", "DEPLOY"];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Quality Gates</h1>
          <p className="mt-1 text-gray-500">
            Đánh giá và quản lý các cổng chất lượng SDLC
          </p>
        </div>
        <div className="flex items-center gap-2">
          <ChartBarIcon className="h-5 w-5 text-gray-400" />
          <span className="text-sm text-gray-500">Overall pass rate:</span>
          <span className="text-lg font-semibold text-green-600">{stats.passRate}%</span>
        </div>
      </div>

      {/* Stage filter */}
      <div className="flex flex-wrap gap-2">
        {stages.map((stage) => (
          <button
            key={stage}
            onClick={() => setSelectedStage(stage)}
            className={`rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
              selectedStage === stage
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            {stage === "all" ? "All Stages" : stage}
          </button>
        ))}
      </div>

      {/* Error state */}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm text-red-700">
            Failed to load gates. Please try again later.
          </p>
        </div>
      )}

      {/* Loading state */}
      {isLoading && (
        <div className="grid gap-4 lg:grid-cols-2">
          {[1, 2, 3, 4].map((i) => (
            <GateCardSkeleton key={i} />
          ))}
        </div>
      )}

      {/* Gates grid */}
      {!isLoading && !error && filteredGates.length > 0 && (
        <div className="grid gap-4 lg:grid-cols-2">
          {filteredGates.map((gate) => (
            <GateCard key={gate.id} gate={gate} />
          ))}
        </div>
      )}

      {/* Empty state */}
      {!isLoading && !error && filteredGates.length === 0 && (
        <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 p-12">
          <ShieldCheckIcon className="h-12 w-12 text-gray-400" />
          <h3 className="mt-4 text-lg font-medium text-gray-900">No gates found</h3>
          <p className="mt-1 text-gray-500">
            {selectedStage !== "all"
              ? "Try selecting a different stage"
              : "Create a project to start with quality gates"}
          </p>
        </div>
      )}

      {/* Recent evaluations */}
      {!isLoading && recentGates.length > 0 && (
        <div>
          <h2 className="mb-4 text-lg font-semibold text-gray-900">
            Recent Gate Activity
          </h2>
          <div className="rounded-lg border border-gray-200 bg-white">
            <div className="divide-y divide-gray-200">
              {recentGates.map((gate) => (
                <EvaluationRow key={gate.id} gate={gate} />
              ))}
            </div>
            <div className="border-t border-gray-200 p-4">
              <Link
                href="/app/gates"
                className="text-sm font-medium text-blue-600 hover:text-blue-700"
              >
                View all gates →
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
