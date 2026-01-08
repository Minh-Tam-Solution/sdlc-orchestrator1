/**
 * SOP History Loading Skeleton
 * @status Sprint 67 - SOP Migration
 */
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export default function SOPHistoryLoading() {
  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <Skeleton className="h-4 w-40" />

      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <Skeleton className="h-9 w-48" />
          <Skeleton className="h-4 w-80" />
        </div>
        <Skeleton className="h-10 w-28" />
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center gap-4">
            <Skeleton className="h-10 w-64" />
            <Skeleton className="h-10 w-10" />
            <Skeleton className="h-10 w-44" />
            <Skeleton className="h-10 w-44" />
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardHeader>
          <Skeleton className="h-6 w-16" />
          <Skeleton className="h-4 w-32" />
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Header row */}
            <div className="flex items-center gap-4 border-b pb-4">
              {[120, 80, 80, 60, 100, 80, 80].map((w, i) => (
                <Skeleton key={i} className="h-4" style={{ width: w }} />
              ))}
            </div>
            {/* Data rows */}
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex items-center gap-4 py-2">
                {[120, 80, 80, 60, 100, 80, 80].map((w, j) => (
                  <Skeleton key={j} className="h-4" style={{ width: w }} />
                ))}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
