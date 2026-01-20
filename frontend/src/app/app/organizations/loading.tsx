/**
 * Organizations List Loading State
 * @module frontend/src/app/app/organizations/loading
 * @status Sprint 84 - Teams & Organizations UI
 */

export default function OrganizationsLoading() {
  return (
    <div className="space-y-6">
      {/* Header skeleton */}
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <div className="h-8 w-40 rounded bg-gray-200 animate-pulse" />
          <div className="h-4 w-64 rounded bg-gray-200 animate-pulse" />
        </div>
        <div className="h-10 w-36 rounded-lg bg-gray-200 animate-pulse" />
      </div>

      {/* Search skeleton */}
      <div className="h-10 w-64 rounded-lg bg-gray-200 animate-pulse" />

      {/* Cards skeleton */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="rounded-lg border border-gray-200 bg-white p-6 animate-pulse">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-lg bg-gray-200" />
                <div className="space-y-2">
                  <div className="h-4 w-32 rounded bg-gray-200" />
                  <div className="h-3 w-20 rounded bg-gray-200" />
                </div>
              </div>
            </div>
            <div className="mt-4 flex gap-3">
              <div className="h-5 w-16 rounded-full bg-gray-200" />
              <div className="h-5 w-20 rounded bg-gray-200" />
              <div className="h-5 w-20 rounded bg-gray-200" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
