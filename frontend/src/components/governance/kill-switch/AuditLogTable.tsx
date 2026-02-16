/**
 * =========================================================================
 * Audit Log Table Component
 * SDLC Orchestrator - Sprint 113 (Governance UI - Kill Switch Admin)
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Framework: SDLC 6.0.6 Quality Assurance System
 * ADR Reference: ADR-041
 *
 * Purpose: Display governance audit log with filtering and search
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
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useGovernanceAuditLog } from "@/hooks/useKillSwitch";
import type { AuditEntryType } from "@/lib/types/kill-switch";

// =============================================================================
// Icons
// =============================================================================

function DocumentTextIcon({ className }: { className?: string }) {
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
        d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
      />
    </svg>
  );
}

function MagnifyingGlassIcon({ className }: { className?: string }) {
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
        d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
      />
    </svg>
  );
}

function FunnelIcon({ className }: { className?: string }) {
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
        d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z"
      />
    </svg>
  );
}

// =============================================================================
// Utility Functions
// =============================================================================

function getEntryTypeBadge(type: AuditEntryType) {
  const config: Record<AuditEntryType, { label: string; color: string }> = {
    mode_change: { label: "Mode Change", color: "bg-blue-100 text-blue-700" },
    rollback_triggered: { label: "Rollback", color: "bg-red-100 text-red-700" },
    break_glass_requested: { label: "Break Glass", color: "bg-orange-100 text-orange-700" },
    break_glass_approved: { label: "Approved", color: "bg-green-100 text-green-700" },
    break_glass_rejected: { label: "Rejected", color: "bg-red-100 text-red-700" },
    break_glass_expired: { label: "Expired", color: "bg-gray-100 text-gray-700" },
    kill_switch_check: { label: "Health Check", color: "bg-purple-100 text-purple-700" },
    criteria_violation: { label: "Violation", color: "bg-amber-100 text-amber-700" },
    notification_sent: { label: "Notification", color: "bg-cyan-100 text-cyan-700" },
  };

  const cfg = config[type] || { label: type, color: "bg-gray-100 text-gray-700" };
  return <Badge className={cfg.color}>{cfg.label}</Badge>;
}

function formatTimestamp(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleString();
}

// =============================================================================
// Component
// =============================================================================

interface AuditLogTableProps {
  initialLimit?: number;
}

export function AuditLogTable({ initialLimit = 20 }: AuditLogTableProps) {
  const [filterType, setFilterType] = useState<AuditEntryType | undefined>(undefined);
  const [searchActor, setSearchActor] = useState("");
  const [limit] = useState(initialLimit);
  const [offset, setOffset] = useState(0);

  const { data: auditLog, isLoading } = useGovernanceAuditLog({
    type: filterType,
    actor: searchActor || undefined,
    limit,
    offset,
  });

  const entries = auditLog?.entries || [];
  const hasMore = auditLog?.has_more || false;

  const ENTRY_TYPES: AuditEntryType[] = [
    "mode_change",
    "rollback_triggered",
    "break_glass_requested",
    "break_glass_approved",
    "break_glass_rejected",
    "break_glass_expired",
    "kill_switch_check",
    "criteria_violation",
    "notification_sent",
  ];

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <DocumentTextIcon className="h-5 w-5 text-gray-600" />
            <CardTitle className="text-lg">Audit Log</CardTitle>
          </div>
          {auditLog && (
            <Badge variant="outline">{auditLog.total} entries</Badge>
          )}
        </div>
        <CardDescription>
          Complete audit trail of governance actions and events
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          {/* Search by Actor */}
          <div className="relative flex-1 min-w-[200px]">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Search by actor..."
              value={searchActor}
              onChange={(e) => {
                setSearchActor(e.target.value);
                setOffset(0);
              }}
              className="pl-9"
            />
          </div>

          {/* Filter by Type */}
          <div className="flex items-center gap-2">
            <FunnelIcon className="h-4 w-4 text-gray-400" />
            <select
              value={filterType || ""}
              onChange={(e) => {
                setFilterType((e.target.value as AuditEntryType) || undefined);
                setOffset(0);
              }}
              className="px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Types</option>
              {ENTRY_TYPES.map((type) => (
                <option key={type} value={type}>
                  {type.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Table */}
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
          </div>
        ) : entries.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No audit entries found
          </div>
        ) : (
          <div className="border rounded-lg overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Timestamp</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Actor</TableHead>
                  <TableHead>Action</TableHead>
                  <TableHead className="hidden md:table-cell">Details</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {entries.map((entry) => (
                  <TableRow key={entry.id}>
                    <TableCell className="text-sm text-gray-500 whitespace-nowrap">
                      {formatTimestamp(entry.timestamp)}
                    </TableCell>
                    <TableCell>{getEntryTypeBadge(entry.type)}</TableCell>
                    <TableCell>
                      <div className="text-sm">
                        <div className="font-medium">{entry.actor}</div>
                        <div className="text-gray-500 text-xs">
                          {entry.actor_role}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="text-sm">{entry.action}</TableCell>
                    <TableCell className="hidden md:table-cell">
                      <code className="text-xs bg-gray-100 px-2 py-1 rounded max-w-[200px] truncate block">
                        {JSON.stringify(entry.details).slice(0, 50)}...
                      </code>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}

        {/* Pagination */}
        {entries.length > 0 && (
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-500">
              Showing {offset + 1} - {offset + entries.length} of {auditLog?.total || 0}
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setOffset(Math.max(0, offset - limit))}
                disabled={offset === 0}
              >
                Previous
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setOffset(offset + limit)}
                disabled={!hasMore}
              >
                Next
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default AuditLogTable;
