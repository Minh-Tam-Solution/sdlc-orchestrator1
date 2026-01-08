/**
 * SOP History Page - Next.js App Router
 * @module frontend/landing/src/app/app/sop-history/page
 * @status Sprint 67 - SOP Migration
 * @description View and manage generated SOPs
 */
"use client";

import { useState } from "react";
import Link from "next/link";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Search,
  Plus,
  FileText,
  ChevronLeft,
  ChevronRight,
  Loader2,
} from "lucide-react";
import { useSOPList } from "@/hooks/useSOP";
import {
  SOP_TYPE_META,
  SOP_STATUS_META,
  type SOPType,
  type SOPStatus,
  type SOPHistoryFilters,
} from "@/lib/types/sop";

export default function SOPHistoryPage() {
  // Filters
  const [filters, setFilters] = useState<SOPHistoryFilters>({
    page: 1,
    page_size: 10,
    sort_by: "created_at",
    sort_order: "desc",
  });

  const [searchInput, setSearchInput] = useState("");

  // Query
  const { data, isLoading, error } = useSOPList(filters);

  const handleSearch = () => {
    setFilters((prev) => ({ ...prev, search: searchInput, page: 1 }));
  };

  const handleTypeFilter = (value: string) => {
    setFilters((prev) => ({
      ...prev,
      sop_type: value === "all" ? undefined : (value as SOPType),
      page: 1,
    }));
  };

  const handleStatusFilter = (value: string) => {
    setFilters((prev) => ({
      ...prev,
      status: value === "all" ? undefined : (value as SOPStatus),
      page: 1,
    }));
  };

  const handlePageChange = (newPage: number) => {
    setFilters((prev) => ({ ...prev, page: newPage }));
  };

  const getStatusBadgeVariant = (status: SOPStatus) => {
    switch (status) {
      case "active":
        return "default";
      case "approved":
        return "secondary";
      case "pending_review":
        return "outline";
      case "draft":
        return "outline";
      case "deprecated":
        return "destructive";
      case "archived":
        return "secondary";
      default:
        return "outline";
    }
  };

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-muted-foreground">
        <Link href="/app" className="hover:text-foreground">
          Dashboard
        </Link>
        <span>/</span>
        <span className="text-foreground">SOP History</span>
      </nav>

      {/* Page header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <FileText className="h-8 w-8" />
            SOP History
          </h1>
          <p className="text-muted-foreground mt-1">
            View and manage all generated Standard Operating Procedures.
          </p>
        </div>
        <Link href="/app/sop-generator">
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            New SOP
          </Button>
        </Link>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-wrap items-center gap-4">
            {/* Search */}
            <div className="flex items-center gap-2 flex-1 min-w-[200px]">
              <Input
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder="Search SOPs..."
                className="max-w-xs"
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              />
              <Button variant="outline" size="icon" onClick={handleSearch}>
                <Search className="h-4 w-4" />
              </Button>
            </div>

            {/* Type filter */}
            <Select
              value={filters.sop_type || "all"}
              onValueChange={handleTypeFilter}
            >
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="All Types" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                {Object.entries(SOP_TYPE_META).map(([key, meta]) => (
                  <SelectItem key={key} value={key}>
                    {meta.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* Status filter */}
            <Select
              value={filters.status || "all"}
              onValueChange={handleStatusFilter}
            >
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="All Statuses" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Statuses</SelectItem>
                {Object.entries(SOP_STATUS_META).map(([key, meta]) => (
                  <SelectItem key={key} value={key}>
                    {meta.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardHeader>
          <CardTitle>SOPs</CardTitle>
          <CardDescription>
            {data ? `${data.total} total SOPs` : "Loading..."}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          ) : error ? (
            <div className="flex items-center justify-center py-12 text-red-500">
              Failed to load SOPs: {error.message}
            </div>
          ) : data && data.items.length > 0 ? (
            <>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Title</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Version</TableHead>
                    <TableHead>Author</TableHead>
                    <TableHead>Created</TableHead>
                    <TableHead>Score</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data.items.map((sop) => (
                    <TableRow key={sop.id}>
                      <TableCell>
                        <Link
                          href={`/app/sop/${sop.id}`}
                          className="font-medium hover:underline"
                        >
                          {sop.title}
                        </Link>
                        {sop.project_name && (
                          <p className="text-xs text-muted-foreground">
                            {sop.project_name}
                          </p>
                        )}
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">
                          {SOP_TYPE_META[sop.sop_type]?.label || sop.sop_type}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge variant={getStatusBadgeVariant(sop.status)}>
                          {SOP_STATUS_META[sop.status]?.label || sop.status}
                        </Badge>
                      </TableCell>
                      <TableCell>{sop.version}</TableCell>
                      <TableCell>{sop.author_name}</TableCell>
                      <TableCell>
                        {new Date(sop.created_at).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <div
                            className="h-2 w-16 rounded-full bg-muted overflow-hidden"
                          >
                            <div
                              className="h-full bg-primary"
                              style={{ width: `${sop.completeness_score}%` }}
                            />
                          </div>
                          <span className="text-xs text-muted-foreground">
                            {sop.completeness_score}%
                          </span>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              {/* Pagination */}
              {data.total_pages > 1 && (
                <div className="flex items-center justify-between mt-4">
                  <p className="text-sm text-muted-foreground">
                    Page {data.page} of {data.total_pages}
                  </p>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handlePageChange(data.page - 1)}
                      disabled={data.page <= 1}
                    >
                      <ChevronLeft className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handlePageChange(data.page + 1)}
                      disabled={data.page >= data.total_pages}
                    >
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
              <FileText className="h-12 w-12 mb-4" />
              <p className="font-medium">No SOPs found</p>
              <p className="text-sm">
                {filters.search || filters.sop_type || filters.status
                  ? "Try adjusting your filters"
                  : "Generate your first SOP to get started"}
              </p>
              {!filters.search && !filters.sop_type && !filters.status && (
                <Link href="/app/sop-generator" className="mt-4">
                  <Button>
                    <Plus className="h-4 w-4 mr-2" />
                    Generate SOP
                  </Button>
                </Link>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
