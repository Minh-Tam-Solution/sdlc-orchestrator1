/**
 * Policy Detail Page Loading State
 * @module frontend/landing/src/app/app/policies/[id]/loading
 * @status Sprint 65 - Route Group Migration
 */

export default function PolicyDetailLoading() {
  return (
    <div className="space-y-6">
      {/* Breadcrumb skeleton */}
      <div className="flex items-center gap-2">
        <div className="h-4 w-16 bg-gray-200 rounded animate-pulse" />
        <span className="text-muted-foreground">/</span>
        <div className="h-4 w-32 bg-gray-200 rounded animate-pulse" />
      </div>

      {/* Page header skeleton */}
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-3">
            <div className="h-9 w-48 bg-gray-200 rounded animate-pulse" />
            <div className="h-6 w-20 bg-gray-200 rounded-full animate-pulse" />
            <div className="h-5 w-16 bg-gray-200 rounded-full animate-pulse" />
          </div>
          <div className="h-5 w-64 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="h-10 w-28 bg-gray-200 rounded animate-pulse" />
      </div>

      {/* Info grid skeleton */}
      <div className="grid gap-4 md:grid-cols-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-lg border shadow-sm p-6">
            <div className="h-4 w-20 bg-gray-200 rounded animate-pulse mb-2" />
            <div className="h-8 w-24 bg-gray-200 rounded animate-pulse" />
          </div>
        ))}
      </div>

      {/* Rego Code section skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b flex items-center justify-between">
          <div>
            <div className="h-6 w-40 bg-gray-200 rounded animate-pulse" />
            <div className="h-4 w-64 bg-gray-200 rounded animate-pulse mt-2" />
          </div>
          <div className="h-8 w-24 bg-gray-200 rounded animate-pulse" />
        </div>
        <div className="p-6">
          <div className="rounded-lg bg-slate-900 p-4 h-48 animate-pulse" />
        </div>
      </div>

      {/* Policy metadata skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b">
          <div className="h-6 w-40 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-56 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i}>
                  <div className="h-3 w-20 bg-gray-200 rounded animate-pulse mb-1" />
                  <div className="h-5 w-40 bg-gray-200 rounded animate-pulse" />
                </div>
              ))}
            </div>
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i}>
                  <div className="h-3 w-24 bg-gray-200 rounded animate-pulse mb-1" />
                  <div className="h-5 w-32 bg-gray-200 rounded animate-pulse" />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Policy usage skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b">
          <div className="h-6 w-28 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-52 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6">
          <div className="flex flex-col items-center justify-center py-8">
            <div className="h-12 w-12 bg-gray-200 rounded animate-pulse mb-4" />
            <div className="h-5 w-48 bg-gray-200 rounded animate-pulse mb-2" />
            <div className="h-4 w-64 bg-gray-200 rounded animate-pulse mb-4" />
            <div className="h-9 w-24 bg-gray-200 rounded animate-pulse" />
          </div>
        </div>
      </div>
    </div>
  );
}
