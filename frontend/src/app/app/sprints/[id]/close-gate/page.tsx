/**
 * G-Sprint-Close Gate Page - SDLC Orchestrator
 *
 * @module frontend/src/app/app/sprints/[id]/close-gate/page
 * @description G-Sprint-Close gate checklist with 24h documentation deadline
 * @sdlc SDLC 5.1.3 Framework - Sprint 87 (Sprint Governance UI)
 * @reference SDLC 5.1.3 Pillar 2: Sprint Planning Governance
 * @status Sprint 87 - Core Feature Implementation
 */

"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useGSprintCloseGate, useSprint } from "@/hooks/useSprintGovernance";
import {
  getChecklistItemStatusColor,
  getChecklistItemStatusIcon,
  getCategoryDisplayName,
  canApproveGate,
  getGateApprovalMessage,
  calculateGateProgress,
  formatDeadlineCountdown,
  getDeadlineUrgencyColor,
  getDeadlineUrgencyLevel,
} from "@/lib/types/sprint-governance";
import type { ChecklistItemStatus } from "@/lib/types/sprint-governance";
import { getGateStatusColor, getGateStatusIcon } from "@/lib/types/planning";
import type { GateStatus } from "@/lib/types/planning";

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

function CheckIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
    </svg>
  );
}

function XMarkIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
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

function ArrowPathIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
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

function ClockIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
    </svg>
  );
}

// =============================================================================
// COMPONENTS
// =============================================================================

/**
 * Documentation Deadline Timer - 24h Rule Enforcement
 */
function DeadlineTimer({ hoursRemaining }: { hoursRemaining: number }) {
  const [displayTime, setDisplayTime] = useState(hoursRemaining);
  const urgencyLevel = getDeadlineUrgencyLevel(displayTime);
  const urgencyColor = getDeadlineUrgencyColor(displayTime);

  useEffect(() => {
    setDisplayTime(hoursRemaining);

    // Update every second for real-time countdown
    const interval = setInterval(() => {
      setDisplayTime((prev) => Math.max(0, prev - 1 / 3600));
    }, 1000);

    return () => clearInterval(interval);
  }, [hoursRemaining]);

  return (
    <div className={`rounded-xl border-2 p-6 ${urgencyLevel === "expired" ? "border-red-300 bg-red-50" : urgencyLevel === "critical" ? "border-red-200 bg-red-50" : urgencyLevel === "warning" ? "border-yellow-200 bg-yellow-50" : "border-green-200 bg-green-50"}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className={`flex h-12 w-12 items-center justify-center rounded-full ${urgencyLevel === "expired" || urgencyLevel === "critical" ? "bg-red-100" : urgencyLevel === "warning" ? "bg-yellow-100" : "bg-green-100"}`}>
            <ClockIcon className={`h-6 w-6 ${urgencyLevel === "expired" || urgencyLevel === "critical" ? "text-red-600" : urgencyLevel === "warning" ? "text-yellow-600" : "text-green-600"}`} />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">24h Documentation Deadline</h3>
            <p className="text-sm text-gray-500">
              {urgencyLevel === "expired"
                ? "Deadline has passed. Documentation must be submitted."
                : "Complete all documentation before the deadline."}
            </p>
          </div>
        </div>
        <div className="text-right">
          <div className={`font-mono text-3xl font-bold ${urgencyColor}`}>
            {formatDeadlineCountdown(displayTime)}
          </div>
          <div className="text-sm text-gray-500">
            {urgencyLevel === "expired" ? "OVERDUE" : "remaining"}
          </div>
        </div>
      </div>

      {urgencyLevel === "critical" && (
        <div className="mt-4 rounded-lg bg-red-100 p-3">
          <div className="flex items-center gap-2">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-600" />
            <p className="text-sm font-medium text-red-700">
              Critical: Less than 2 hours remaining! Complete documentation immediately.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Checklist Item Row
 */
function ChecklistItemRow({
  item,
  onStatusChange,
  isUpdating,
}: {
  item: {
    id: string;
    name: string;
    description: string;
    category: string;
    is_mandatory: boolean;
    status: ChecklistItemStatus;
    evidence_url: string | null;
    notes: string | null;
  };
  onStatusChange: (itemId: string, status: ChecklistItemStatus) => void;
  isUpdating: boolean;
}) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className={`rounded-lg border ${item.is_mandatory ? "border-red-200 bg-red-50/30" : "border-gray-200 bg-white"}`}>
      <div
        className="flex items-center justify-between p-4 cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center gap-3">
          <span>{getChecklistItemStatusIcon(item.status)}</span>
          <div>
            <div className="flex items-center gap-2">
              <h4 className="font-medium text-gray-900">{item.name}</h4>
              {item.is_mandatory && (
                <span className="rounded-full bg-red-100 px-2 py-0.5 text-xs font-medium text-red-700">
                  Required
                </span>
              )}
            </div>
            <p className="text-sm text-gray-500">{getCategoryDisplayName(item.category)}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={`rounded-full px-3 py-1 text-sm font-medium ${getChecklistItemStatusColor(item.status)}`}>
            {item.status.charAt(0).toUpperCase() + item.status.slice(1)}
          </span>
          <svg
            className={`h-5 w-5 text-gray-400 transition-transform ${isExpanded ? "rotate-180" : ""}`}
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
          </svg>
        </div>
      </div>

      {isExpanded && (
        <div className="border-t border-gray-100 px-4 py-4">
          <p className="mb-4 text-sm text-gray-600">{item.description}</p>

          {item.evidence_url && (
            <div className="mb-4">
              <label className="text-xs font-medium text-gray-500">Evidence</label>
              <a
                href={item.evidence_url}
                target="_blank"
                rel="noopener noreferrer"
                className="block text-sm text-blue-600 hover:underline"
              >
                {item.evidence_url}
              </a>
            </div>
          )}

          {item.notes && (
            <div className="mb-4">
              <label className="text-xs font-medium text-gray-500">Notes</label>
              <p className="text-sm text-gray-700">{item.notes}</p>
            </div>
          )}

          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-500">Set Status:</span>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onStatusChange(item.id, "pass");
              }}
              disabled={isUpdating}
              className={`flex items-center gap-1 rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
                item.status === "pass"
                  ? "bg-green-600 text-white"
                  : "bg-green-100 text-green-700 hover:bg-green-200"
              }`}
            >
              <CheckIcon className="h-4 w-4" />
              Pass
            </button>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onStatusChange(item.id, "fail");
              }}
              disabled={isUpdating}
              className={`flex items-center gap-1 rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
                item.status === "fail"
                  ? "bg-red-600 text-white"
                  : "bg-red-100 text-red-700 hover:bg-red-200"
              }`}
            >
              <XMarkIcon className="h-4 w-4" />
              Fail
            </button>
            {!item.is_mandatory && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onStatusChange(item.id, "waived");
                }}
                disabled={isUpdating}
                className={`flex items-center gap-1 rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
                  item.status === "waived"
                    ? "bg-yellow-600 text-white"
                    : "bg-yellow-100 text-yellow-700 hover:bg-yellow-200"
                }`}
              >
                Waive
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Gate Progress Bar
 */
function GateProgressBar({ progress, status }: { progress: number; status: GateStatus }) {
  return (
    <div className="mb-4">
      <div className="mb-2 flex items-center justify-between text-sm">
        <span className="font-medium text-gray-700">Gate Progress</span>
        <span className="text-gray-500">{progress}% complete</span>
      </div>
      <div className="h-3 w-full overflow-hidden rounded-full bg-gray-200">
        <div
          className={`h-3 rounded-full transition-all duration-300 ${
            status === "passed"
              ? "bg-green-600"
              : status === "conditional"
                ? "bg-yellow-600"
                : status === "failed"
                  ? "bg-red-600"
                  : "bg-blue-600"
          }`}
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
}

/**
 * Approval Panel
 */
function ApprovalPanel({
  gate,
  onApprove,
  onEvaluate,
  isApproving,
  isEvaluating,
  isDeadlineExpired,
}: {
  gate: {
    status: GateStatus;
    items_passed: number;
    items_failed: number;
    items_waived: number;
    items_total: number;
    checklist_items: Array<{ is_mandatory: boolean; status: string }>;
  };
  onApprove: (waiverReason?: string) => void;
  onEvaluate: () => void;
  isApproving: boolean;
  isEvaluating: boolean;
  isDeadlineExpired: boolean;
}) {
  const [waiverReason, setWaiverReason] = useState("");
  const gateCanBeApproved = canApproveGate(gate as Parameters<typeof canApproveGate>[0]) && !isDeadlineExpired;
  const approvalMessage = getGateApprovalMessage(gate as Parameters<typeof getGateApprovalMessage>[0]);

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6">
      <h3 className="mb-4 flex items-center gap-2 text-lg font-semibold text-gray-900">
        <ShieldCheckIcon className="h-5 w-5 text-gray-500" />
        Gate Approval
      </h3>

      {/* Stats */}
      <div className="mb-4 grid grid-cols-4 gap-4">
        <div className="text-center">
          <div className="text-xl font-bold text-green-600">{gate.items_passed}</div>
          <div className="text-xs text-gray-500">Passed</div>
        </div>
        <div className="text-center">
          <div className="text-xl font-bold text-red-600">{gate.items_failed}</div>
          <div className="text-xs text-gray-500">Failed</div>
        </div>
        <div className="text-center">
          <div className="text-xl font-bold text-yellow-600">{gate.items_waived}</div>
          <div className="text-xs text-gray-500">Waived</div>
        </div>
        <div className="text-center">
          <div className="text-xl font-bold text-gray-600">{gate.items_total}</div>
          <div className="text-xs text-gray-500">Total</div>
        </div>
      </div>

      {/* Deadline Warning */}
      {isDeadlineExpired && (
        <div className="mb-4 rounded-lg bg-red-100 p-4">
          <div className="flex items-center gap-2">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-600" />
            <p className="text-sm font-medium text-red-700">
              Documentation deadline has passed. Gate cannot be approved until documentation is submitted.
            </p>
          </div>
        </div>
      )}

      {/* Approval Status */}
      <div className={`mb-4 rounded-lg p-4 ${gateCanBeApproved ? "bg-green-50" : "bg-red-50"}`}>
        <div className="flex items-center gap-2">
          {gateCanBeApproved ? (
            <CheckIcon className="h-5 w-5 text-green-600" />
          ) : (
            <ExclamationTriangleIcon className="h-5 w-5 text-red-600" />
          )}
          <p className={`text-sm font-medium ${gateCanBeApproved ? "text-green-700" : "text-red-700"}`}>
            {isDeadlineExpired ? "Documentation deadline expired. Submit documentation first." : approvalMessage}
          </p>
        </div>
      </div>

      {/* Waiver Reason */}
      {!gateCanBeApproved && gate.items_waived > 0 && !isDeadlineExpired && (
        <div className="mb-4">
          <label className="mb-1 block text-sm font-medium text-gray-700">
            Waiver Reason (optional)
          </label>
          <textarea
            value={waiverReason}
            onChange={(e) => setWaiverReason(e.target.value)}
            className="w-full rounded-lg border border-gray-300 p-3 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            rows={3}
            placeholder="Explain why items are being waived..."
          />
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-3">
        <button
          onClick={onEvaluate}
          disabled={isEvaluating}
          className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          <ArrowPathIcon className={`h-4 w-4 ${isEvaluating ? "animate-spin" : ""}`} />
          Re-evaluate
        </button>
        <button
          onClick={() => onApprove(waiverReason || undefined)}
          disabled={isApproving || !gateCanBeApproved}
          className="flex items-center gap-2 rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isApproving ? (
            <ArrowPathIcon className="h-4 w-4 animate-spin" />
          ) : (
            <CheckIcon className="h-4 w-4" />
          )}
          Close Sprint
        </button>
      </div>
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
        <div className="h-6 w-32 animate-pulse rounded bg-gray-200" />
      </div>
      <div className="h-32 animate-pulse rounded-xl bg-gray-200" />
      <div className="h-24 animate-pulse rounded-xl bg-gray-200" />
      <div className="space-y-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-20 animate-pulse rounded-lg bg-gray-200" />
        ))}
      </div>
    </div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export default function GSprintCloseGatePage() {
  const params = useParams();
  const router = useRouter();
  const sprintId = params.id as string;

  const { data: sprint } = useSprint(sprintId);
  const {
    gate,
    checklist,
    hoursRemaining,
    isDeadlineExpired,
    isLoading,
    isEvaluating,
    isApproving,
    isUpdatingItem,
    error,
    evaluate,
    approve,
    updateItem,
  } = useGSprintCloseGate(sprintId);

  if (isLoading) {
    return <LoadingSkeleton />;
  }

  if (error || !gate) {
    return (
      <div className="flex min-h-[400px] items-center justify-center p-6">
        <div className="text-center">
          <ExclamationTriangleIcon className="mx-auto h-12 w-12 text-red-500" />
          <h3 className="mt-4 text-lg font-semibold text-gray-900">Error Loading Gate</h3>
          <p className="mt-2 text-sm text-gray-500">
            {error instanceof Error ? error.message : "The G-Sprint-Close gate could not be loaded."}
          </p>
          <Link
            href={`/app/sprints/${sprintId}`}
            className="mt-4 inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            <ArrowLeftIcon className="h-4 w-4" />
            Back to Sprint
          </Link>
        </div>
      </div>
    );
  }

  const gateStatus = gate.status as GateStatus;
  const progress = calculateGateProgress(gate);

  const handleStatusChange = async (itemId: string, status: ChecklistItemStatus) => {
    try {
      await updateItem(itemId, { status });
    } catch {
      // Error handling is done in the mutation
    }
  };

  const handleApprove = async (waiverReason?: string) => {
    try {
      await approve({ waiver_reason: waiverReason });
      router.push(`/app/sprints/${sprintId}`);
    } catch {
      // Error handling is done in the mutation
    }
  };

  const handleEvaluate = async () => {
    try {
      await evaluate(true);
    } catch {
      // Error handling is done in the mutation
    }
  };

  // Group checklist items by category
  const itemsByCategory = (checklist || []).reduce<Record<string, NonNullable<typeof checklist>>>(
    (acc, item) => {
      const category = item.category;
      if (!acc[category]) {
        acc[category] = [];
      }
      acc[category].push(item);
      return acc;
    },
    {}
  );

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-6">
        <Link
          href={`/app/sprints/${sprintId}`}
          className="mb-4 inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700"
        >
          <ArrowLeftIcon className="h-4 w-4" />
          Back to Sprint {sprint?.number}
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">G-Sprint-Close Gate</h1>
            <p className="mt-1 text-sm text-gray-500">
              SDLC 5.1.3 Pillar 2 - Sprint Close Gate with 24h Documentation Rule
            </p>
          </div>
          <span className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium ${getGateStatusColor(gateStatus)}`}>
            <span>{getGateStatusIcon(gateStatus)}</span>
            {gateStatus.charAt(0).toUpperCase() + gateStatus.slice(1)}
          </span>
        </div>
      </div>

      {/* 24h Documentation Deadline Timer */}
      <div className="mb-6">
        <DeadlineTimer hoursRemaining={hoursRemaining} />
      </div>

      {/* Progress */}
      <div className="mb-6 rounded-xl border border-gray-200 bg-white p-6">
        <GateProgressBar progress={progress} status={gateStatus} />
        <p className="text-sm text-gray-600">
          Complete all checklist items and documentation within 24 hours to close the sprint.
        </p>
      </div>

      {/* Checklist Items by Category */}
      <div className="mb-6 space-y-6">
        {Object.entries(itemsByCategory).map(([category, items]) => (
          <div key={category}>
            <h2 className="mb-3 text-lg font-semibold text-gray-900">
              {getCategoryDisplayName(category)}
            </h2>
            <div className="space-y-3">
              {(items || []).map((item) => (
                <ChecklistItemRow
                  key={item.id}
                  item={item}
                  onStatusChange={handleStatusChange}
                  isUpdating={isUpdatingItem}
                />
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Approval Panel */}
      {gate && (
        <ApprovalPanel
          gate={gate}
          onApprove={handleApprove}
          onEvaluate={handleEvaluate}
          isApproving={isApproving}
          isEvaluating={isEvaluating}
          isDeadlineExpired={isDeadlineExpired}
        />
      )}
    </div>
  );
}
