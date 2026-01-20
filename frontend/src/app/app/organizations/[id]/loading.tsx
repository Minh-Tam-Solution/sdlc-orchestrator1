/**
 * Organization Detail Loading State
 * @module frontend/src/app/app/organizations/[id]/loading
 * @status Sprint 84 - Teams & Organizations UI
 */

export default function OrganizationDetailLoading() {
  return (
    <div className="space-y-6">
      {/* Back link skeleton */}
      <div className="h-5 w-36 rounded bg-gray-200 animate-pulse" />

      {/* Header skeleton */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="h-12 w-12 rounded-lg bg-gray-200 animate-pulse" />
          <div className="space-y-2">
            <div className="h-8 w-48 rounded bg-gray-200 animate-pulse" />
            <div className="h-4 w-24 rounded bg-gray-200 animate-pulse" />
          </div>
        </div>
        <div className="h-10 w-20 rounded-lg bg-gray-200 animate-pulse" />
      </div>

      {/* Stats skeleton */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="rounded-lg border border-gray-200 bg-white p-4 animate-pulse">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-gray-200" />
              <div className="space-y-2">
                <div className="h-6 w-12 rounded bg-gray-200" />
                <div className="h-4 w-20 rounded bg-gray-200" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Plan features skeleton */}
      <div className="rounded-lg border border-gray-200 bg-white p-6 animate-pulse">
        <div className="h-6 w-32 rounded bg-gray-200 mb-4" />
        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-5 rounded bg-gray-200" />
          ))}
        </div>
      </div>

      {/* Teams skeleton */}
      <div className="rounded-lg border border-gray-200 bg-white">
        <div className="flex items-center justify-between border-b border-gray-200 px-6 py-4">
          <div className="h-6 w-24 rounded bg-gray-200 animate-pulse" />
          <div className="h-10 w-28 rounded-lg bg-gray-200 animate-pulse" />
        </div>
        <div className="p-6 space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex items-center gap-4 animate-pulse">
              <div className="h-10 w-10 rounded-lg bg-gray-200" />
              <div className="flex-1 space-y-2">
                <div className="h-4 w-32 rounded bg-gray-200" />
                <div className="h-3 w-48 rounded bg-gray-200" />
              </div>
              <div className="h-5 w-16 rounded-full bg-gray-200" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
