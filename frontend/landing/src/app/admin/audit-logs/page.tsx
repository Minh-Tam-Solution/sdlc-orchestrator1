"use client";

/**
 * Audit Logs Page - Next.js App Router
 * @route /admin/audit-logs
 * @status Sprint 68 - Admin Section Migration
 * @description Immutable audit trail viewer (SOC 2 CC7.1 compliance)
 * @security Logs are append-only, cannot be modified or deleted
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
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
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { useAuditLogs } from "@/hooks/useAdmin";
import {
  AUDIT_ACTION_META,
  COMMON_AUDIT_ACTIONS,
  formatAuditTimestamp,
  type AuditAction,
} from "@/lib/types/admin";
import {
  ArrowLeft,
  Search,
  ChevronDown,
  ChevronRight,
  Calendar,
  Shield,
} from "lucide-react";

export default function AuditLogsPage() {
  const router = useRouter();

  // Filter state
  const [search, setSearch] = useState("");
  const [actionFilter, setActionFilter] = useState<string>("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [page, setPage] = useState(1);
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());

  const { data: logsData, isLoading } = useAuditLogs({
    page,
    page_size: 50,
    search: search || undefined,
    action: actionFilter || undefined,
    date_from: dateFrom || undefined,
    date_to: dateTo || undefined,
  });

  const toggleExpand = (id: string) => {
    setExpandedRows((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const getActionBadge = (action: string) => {
    const meta = AUDIT_ACTION_META[action as AuditAction];
    if (meta) {
      return (
        <Badge variant="outline" className={meta.color}>
          {meta.label}
        </Badge>
      );
    }
    return <Badge variant="outline">{action}</Badge>;
  };

  const clearFilters = () => {
    setSearch("");
    setActionFilter("");
    setDateFrom("");
    setDateTo("");
    setPage(1);
  };

  const hasFilters = search || actionFilter || dateFrom || dateTo;

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => router.push("/admin")}
              className="h-8 w-8 p-0"
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <h1 className="text-3xl font-bold tracking-tight">Audit Logs</h1>
          </div>
          <p className="text-muted-foreground">
            Immutable system audit trail (SOC 2 CC7.1 compliance)
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Shield className="h-5 w-5 text-green-600" />
          <span className="text-sm text-muted-foreground">
            {logsData?.total ?? 0} total entries
          </span>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
            <div className="relative lg:col-span-2">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search by actor or target..."
                value={search}
                onChange={(e) => {
                  setSearch(e.target.value);
                  setPage(1);
                }}
                className="pl-10"
              />
            </div>

            <Select
              value={actionFilter}
              onValueChange={(value) => {
                setActionFilter(value === "all" ? "" : value);
                setPage(1);
              }}
            >
              <SelectTrigger>
                <SelectValue placeholder="Filter by action" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Actions</SelectItem>
                {COMMON_AUDIT_ACTIONS.map((action) => (
                  <SelectItem key={action} value={action}>
                    {AUDIT_ACTION_META[action]?.label || action}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="date"
                placeholder="From date"
                value={dateFrom}
                onChange={(e) => {
                  setDateFrom(e.target.value);
                  setPage(1);
                }}
                className="pl-10"
              />
            </div>

            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="date"
                placeholder="To date"
                value={dateTo}
                onChange={(e) => {
                  setDateTo(e.target.value);
                  setPage(1);
                }}
                className="pl-10"
              />
            </div>
          </div>

          {hasFilters && (
            <div className="flex justify-end mt-4">
              <Button variant="outline" size="sm" onClick={clearFilters}>
                Clear Filters
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Logs table */}
      <Card>
        <CardHeader>
          <CardTitle>Activity Log</CardTitle>
          <CardDescription>
            Click on a row to view detailed information
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
                <Skeleton key={i} className="h-14 w-full" />
              ))}
            </div>
          ) : logsData?.items && logsData.items.length > 0 ? (
            <>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-8"></TableHead>
                    <TableHead>Timestamp</TableHead>
                    <TableHead>Action</TableHead>
                    <TableHead>Actor</TableHead>
                    <TableHead>Target</TableHead>
                    <TableHead>IP Address</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {logsData.items.map((log) => (
                    <Collapsible
                      key={log.id}
                      open={expandedRows.has(log.id)}
                      onOpenChange={() => toggleExpand(log.id)}
                      asChild
                    >
                      <>
                        <CollapsibleTrigger asChild>
                          <TableRow className="cursor-pointer hover:bg-muted/50">
                            <TableCell>
                              {expandedRows.has(log.id) ? (
                                <ChevronDown className="h-4 w-4" />
                              ) : (
                                <ChevronRight className="h-4 w-4" />
                              )}
                            </TableCell>
                            <TableCell className="text-sm font-mono">
                              {formatAuditTimestamp(log.timestamp)}
                            </TableCell>
                            <TableCell>{getActionBadge(log.action)}</TableCell>
                            <TableCell>
                              <div>
                                <p className="text-sm">
                                  {log.actor_email || "System"}
                                </p>
                              </div>
                            </TableCell>
                            <TableCell>
                              <div>
                                <p className="text-sm font-medium">
                                  {log.target_name || "-"}
                                </p>
                                {log.target_type && (
                                  <p className="text-xs text-muted-foreground">
                                    {log.target_type}
                                  </p>
                                )}
                              </div>
                            </TableCell>
                            <TableCell className="text-sm text-muted-foreground font-mono">
                              {log.ip_address || "-"}
                            </TableCell>
                          </TableRow>
                        </CollapsibleTrigger>
                        <CollapsibleContent asChild>
                          <TableRow className="bg-muted/30">
                            <TableCell colSpan={6} className="py-4">
                              <div className="grid gap-4 md:grid-cols-2">
                                <div>
                                  <h4 className="text-sm font-semibold mb-2">
                                    Event Details
                                  </h4>
                                  <dl className="space-y-1 text-sm">
                                    <div className="flex gap-2">
                                      <dt className="text-muted-foreground min-w-[100px]">
                                        Log ID:
                                      </dt>
                                      <dd className="font-mono text-xs">
                                        {log.id}
                                      </dd>
                                    </div>
                                    <div className="flex gap-2">
                                      <dt className="text-muted-foreground min-w-[100px]">
                                        Actor ID:
                                      </dt>
                                      <dd className="font-mono text-xs">
                                        {log.actor_id || "-"}
                                      </dd>
                                    </div>
                                    <div className="flex gap-2">
                                      <dt className="text-muted-foreground min-w-[100px]">
                                        Target ID:
                                      </dt>
                                      <dd className="font-mono text-xs">
                                        {log.target_id || "-"}
                                      </dd>
                                    </div>
                                  </dl>
                                </div>
                                <div>
                                  <h4 className="text-sm font-semibold mb-2">
                                    Additional Details
                                  </h4>
                                  {Object.keys(log.details).length > 0 ? (
                                    <pre className="text-xs bg-muted p-2 rounded overflow-auto max-h-32">
                                      {JSON.stringify(log.details, null, 2)}
                                    </pre>
                                  ) : (
                                    <p className="text-sm text-muted-foreground">
                                      No additional details
                                    </p>
                                  )}
                                </div>
                              </div>
                            </TableCell>
                          </TableRow>
                        </CollapsibleContent>
                      </>
                    </Collapsible>
                  ))}
                </TableBody>
              </Table>

              {/* Pagination */}
              {logsData.pages > 1 && (
                <div className="flex items-center justify-between mt-4 pt-4 border-t">
                  <div className="text-sm text-muted-foreground">
                    Page {logsData.page} of {logsData.pages} ({logsData.total}{" "}
                    entries)
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setPage((p) => Math.max(1, p - 1))}
                      disabled={page === 1}
                    >
                      Previous
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() =>
                        setPage((p) => Math.min(logsData.pages, p + 1))
                      }
                      disabled={page === logsData.pages}
                    >
                      Next
                    </Button>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-8 text-muted-foreground">
              <p>No audit logs found</p>
              {hasFilters && (
                <p className="text-sm mt-1">
                  Try adjusting your search or filters
                </p>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
