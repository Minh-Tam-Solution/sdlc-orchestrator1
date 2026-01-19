/**
 * Policies Page Loading State
 * @module frontend/landing/src/app/app/policies/loading
 * @status Sprint 65 - Route Group Migration
 */

export default function PoliciesLoading() {
  return (
    <div className="space-y-6">
      {/* Page header skeleton */}
      <div className="flex items-center justify-between">
        <div>
          <div className="h-9 w-32 bg-gray-200 rounded animate-pulse" />
          <div className="h-5 w-64 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="h-10 w-32 bg-gray-200 rounded animate-pulse" />
      </div>

      {/* Policy pack summary skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b">
          <div className="h-6 w-48 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-72 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
            {[...Array(10)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-200 rounded-lg animate-pulse" />
            ))}
          </div>
        </div>
      </div>

      {/* Policy list skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b flex items-center justify-between">
          <div>
            <div className="h-6 w-32 bg-gray-200 rounded animate-pulse" />
            <div className="h-4 w-56 bg-gray-200 rounded animate-pulse mt-2" />
          </div>
          <div className="h-10 w-44 bg-gray-200 rounded animate-pulse" />
        </div>
        <div className="p-6 space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="rounded-lg border p-4">
              <div className="flex items-start justify-between">
                <div className="space-y-2 flex-1">
                  <div className="flex items-center gap-2">
                    <div className="h-5 w-40 bg-gray-200 rounded animate-pulse" />
                    <div className="h-5 w-20 bg-gray-200 rounded animate-pulse" />
                    <div className="h-5 w-16 bg-gray-200 rounded-full animate-pulse" />
                  </div>
                  <div className="h-4 w-full bg-gray-200 rounded animate-pulse" />
                  <div className="h-3 w-48 bg-gray-200 rounded animate-pulse" />
                </div>
                <div className="flex gap-2">
                  <div className="h-8 w-24 bg-gray-200 rounded animate-pulse" />
                  <div className="h-8 w-20 bg-gray-200 rounded animate-pulse" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
