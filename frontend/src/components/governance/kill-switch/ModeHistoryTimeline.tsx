/**
 * =========================================================================
 * Mode History Timeline Component
 * SDLC Orchestrator - Sprint 113 (Governance UI - Kill Switch Admin)
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Framework: SDLC 6.0.6 Quality Assurance System
 * ADR Reference: ADR-041
 *
 * Purpose: Display timeline of governance mode changes with audit trail
 * =========================================================================
 */

"use client";

import { useState } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useModeHistory } from "@/hooks/useKillSwitch";
import type { GovernanceMode, ModeChangeEntry } from "@/lib/types/kill-switch";

// =============================================================================
// Icons
// =============================================================================

function ClockIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>
  );
}

function ArrowRightIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={2}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3"
      />
    </svg>
  );
}

function BoltIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z"
      />
    </svg>
  );
}

function UserIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z"
      />
    </svg>
  );
}

function ChevronDownIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={2}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="m19.5 8.25-7.5 7.5-7.5-7.5"
      />
    </svg>
  );
}

// =============================================================================
// Utility Functions
// =============================================================================

function getModeColor(mode: GovernanceMode): string {
  const colors: Record<GovernanceMode, string> = {
    OFF: "bg-gray-100 text-gray-700",
    WARNING: "bg-yellow-100 text-yellow-700",
    SOFT: "bg-orange-100 text-orange-700",
    FULL: "bg-green-100 text-green-700",
  };
  return colors[mode];
}

function getTimelineColor(entry: ModeChangeEntry): string {
  if (entry.auto_triggered) return "bg-red-500";
  if (entry.to_mode === "FULL") return "bg-green-500";
  if (entry.to_mode === "OFF") return "bg-gray-500";
  return "bg-blue-500";
}

function formatRelativeTime(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return "Just now";
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
}

// =============================================================================
// Component
// =============================================================================

interface ModeHistoryTimelineProps {
  limit?: number;
  showLoadMore?: boolean;
}

export function ModeHistoryTimeline({
  limit = 10,
  showLoadMore = true,
}: ModeHistoryTimelineProps) {
  const [displayLimit, setDisplayLimit] = useState(limit);
  const [expandedEntry, setExpandedEntry] = useState<string | null>(null);

  const { data: history, isLoading } = useModeHistory({ limit: displayLimit });

  if (isLoading) {
    return (
      <Card>
        <CardContent className="py-8">
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
          </div>
        </CardContent>
      </Card>
    );
  }

  const entries = history?.entries || [];

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ClockIcon className="h-5 w-5 text-purple-600" />
            <CardTitle className="text-lg">Mode History</CardTitle>
          </div>
          {history && (
            <Badge variant="outline">
              {history.total_changes_30d} changes in 30 days
            </Badge>
          )}
        </div>
        <CardDescription>
          Timeline of governance mode changes and rollback events
        </CardDescription>
      </CardHeader>

      <CardContent>
        {entries.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No mode changes recorded yet
          </div>
        ) : (
          <div className="relative">
            {/* Timeline Line */}
            <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200" />

            {/* Timeline Entries */}
            <div className="space-y-4">
              {entries.map((entry) => (
                <div key={entry.id} className="relative pl-10">
                  {/* Timeline Dot */}
                  <div
                    className={`absolute left-2.5 w-3 h-3 rounded-full ${getTimelineColor(
                      entry
                    )} ring-4 ring-white`}
                  />

                  {/* Entry Card */}
                  <div
                    className={`border rounded-lg p-3 ${
                      expandedEntry === entry.id ? "bg-gray-50" : "bg-white"
                    }`}
                  >
                    {/* Header Row */}
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <Badge className={getModeColor(entry.from_mode)}>
                          {entry.from_mode}
                        </Badge>
                        <ArrowRightIcon className="h-4 w-4 text-gray-400" />
                        <Badge className={getModeColor(entry.to_mode)}>
                          {entry.to_mode}
                        </Badge>
                      </div>
                      <span className="text-xs text-gray-500">
                        {formatRelativeTime(entry.changed_at)}
                      </span>
                    </div>

                    {/* Actor and Type */}
                    <div className="flex items-center gap-4 text-sm text-gray-600">
                      <div className="flex items-center gap-1">
                        {entry.auto_triggered ? (
                          <>
                            <BoltIcon className="h-4 w-4 text-red-500" />
                            <span className="text-red-600">Auto-rollback</span>
                          </>
                        ) : (
                          <>
                            <UserIcon className="h-4 w-4" />
                            <span>{entry.changed_by}</span>
                          </>
                        )}
                      </div>
                    </div>

                    {/* Reason (collapsed by default) */}
                    {entry.reason && (
                      <button
                        onClick={() =>
                          setExpandedEntry(
                            expandedEntry === entry.id ? null : entry.id
                          )
                        }
                        className="flex items-center gap-1 text-xs text-gray-500 mt-2 hover:text-gray-700"
                      >
                        <ChevronDownIcon
                          className={`h-3 w-3 transition-transform ${
                            expandedEntry === entry.id ? "rotate-180" : ""
                          }`}
                        />
                        {expandedEntry === entry.id ? "Hide details" : "Show details"}
                      </button>
                    )}

                    {/* Expanded Details */}
                    {expandedEntry === entry.id && (
                      <div className="mt-3 pt-3 border-t space-y-2">
                        <div>
                          <span className="text-xs text-gray-500 block">Reason</span>
                          <p className="text-sm">{entry.reason}</p>
                        </div>
                        {entry.trigger_criteria && entry.trigger_criteria.length > 0 && (
                          <div>
                            <span className="text-xs text-gray-500 block">
                              Trigger Criteria
                            </span>
                            <ul className="text-sm list-disc list-inside">
                              {entry.trigger_criteria.map((c, i) => (
                                <li key={i}>{c}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {entry.duration_in_mode && (
                          <div>
                            <span className="text-xs text-gray-500 block">
                              Duration in Previous Mode
                            </span>
                            <p className="text-sm">{entry.duration_in_mode}</p>
                          </div>
                        )}
                        <div>
                          <span className="text-xs text-gray-500 block">
                            Timestamp
                          </span>
                          <p className="text-sm">
                            {new Date(entry.changed_at).toLocaleString()}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Load More Button */}
            {showLoadMore && entries.length >= displayLimit && (
              <div className="mt-4 text-center">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setDisplayLimit((prev) => prev + 10)}
                >
                  Load More
                </Button>
              </div>
            )}
          </div>
        )}

        {/* Current Mode Summary */}
        {history && (
          <div className="mt-4 pt-4 border-t">
            <div className="flex items-center justify-between text-sm text-gray-600">
              <span>
                Current mode:{" "}
                <Badge className={getModeColor(history.current_mode)}>
                  {history.current_mode}
                </Badge>
              </span>
              <span>
                Since: {new Date(history.current_mode_since).toLocaleDateString()}
              </span>
            </div>
            <div className="text-sm text-gray-500 mt-1">
              Average time in FULL mode: {history.average_time_in_full_mode}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default ModeHistoryTimeline;
