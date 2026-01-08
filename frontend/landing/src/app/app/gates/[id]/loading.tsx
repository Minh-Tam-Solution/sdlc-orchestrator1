/**
 * Gate Detail Loading State
 * @module frontend/landing/src/app/app/gates/[id]/loading
 * @status Sprint 64 - Route Group Migration
 */

export default function GateDetailLoading() {
  return (
    <div className="space-y-6">
      {/* Breadcrumb skeleton */}
      <div className="flex items-center gap-2">
        <div className="h-4 w-16 bg-gray-200 rounded animate-pulse" />
        <div className="h-4 w-4 bg-gray-200 rounded animate-pulse" />
        <div className="h-4 w-16 bg-gray-200 rounded animate-pulse" />
        <div className="h-4 w-4 bg-gray-200 rounded animate-pulse" />
        <div className="h-4 w-24 bg-gray-200 rounded animate-pulse" />
      </div>

      {/* Header skeleton */}
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-3">
            <div className="h-9 w-48 bg-gray-200 rounded animate-pulse" />
            <div className="h-7 w-24 bg-gray-200 rounded-full animate-pulse" />
          </div>
          <div className="h-5 w-64 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="flex gap-2">
          <div className="h-10 w-24 bg-gray-200 rounded animate-pulse" />
          <div className="h-10 w-36 bg-gray-200 rounded animate-pulse" />
        </div>
      </div>

      {/* Info grid skeleton */}
      <div className="grid gap-4 md:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-white rounded-lg border p-6">
            <div className="h-4 w-16 bg-gray-200 rounded animate-pulse mb-3" />
            <div className="h-8 w-24 bg-gray-200 rounded animate-pulse" />
            <div className="h-3 w-32 bg-gray-200 rounded animate-pulse mt-2" />
          </div>
        ))}
      </div>

      {/* Exit Criteria skeleton */}
      <div className="bg-white rounded-lg border">
        <div className="p-6 border-b">
          <div className="h-6 w-32 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-64 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6 space-y-3">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="flex items-center justify-between rounded-lg border p-3"
            >
              <div className="flex items-center gap-3">
                <div className="h-6 w-6 bg-gray-200 rounded-full animate-pulse" />
                <div className="h-5 w-48 bg-gray-200 rounded animate-pulse" />
              </div>
              <div className="h-6 w-16 bg-gray-200 rounded-full animate-pulse" />
            </div>
          ))}
        </div>
      </div>

      {/* Approval History skeleton */}
      <div className="bg-white rounded-lg border">
        <div className="p-6 border-b">
          <div className="h-6 w-36 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-48 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6 space-y-4">
          {[1, 2].map((i) => (
            <div
              key={i}
              className="flex items-start justify-between rounded-lg border p-4"
            >
              <div className="flex items-start gap-4">
                <div className="h-10 w-10 bg-gray-200 rounded-full animate-pulse" />
                <div>
                  <div className="h-5 w-32 bg-gray-200 rounded animate-pulse" />
                  <div className="h-4 w-24 bg-gray-200 rounded animate-pulse mt-1" />
                </div>
              </div>
              <div className="text-right">
                <div className="h-6 w-20 bg-gray-200 rounded-full animate-pulse" />
                <div className="h-3 w-24 bg-gray-200 rounded animate-pulse mt-1" />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Actions skeleton */}
      <div className="flex justify-end gap-2">
        <div className="h-10 w-32 bg-gray-200 rounded animate-pulse" />
        <div className="h-10 w-36 bg-gray-200 rounded animate-pulse" />
      </div>
    </div>
  );
}
