/**
 * Sprint Governance Loading State - SDLC Orchestrator
 *
 * @module frontend/src/app/app/sprints/loading
 * @description Loading skeleton for Sprint Governance dashboard
 * @sdlc SDLC 5.1.3 Framework - Sprint 87
 */

export default function SprintGovernanceLoading() {
  return (
    <div className="p-6">
      {/* Header Skeleton */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <div className="h-8 w-48 animate-pulse rounded bg-gray-200" />
          <div className="mt-2 h-4 w-64 animate-pulse rounded bg-gray-200" />
        </div>
        <div className="flex gap-3">
          <div className="h-10 w-28 animate-pulse rounded-lg bg-gray-200" />
          <div className="h-10 w-32 animate-pulse rounded-lg bg-gray-200" />
        </div>
      </div>

      {/* Active Sprint Card Skeleton */}
      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <div className="h-4 w-24 animate-pulse rounded bg-gray-200" />
            <div className="mt-2 h-6 w-48 animate-pulse rounded bg-gray-200" />
          </div>
          <div className="h-10 w-28 animate-pulse rounded-lg bg-gray-200" />
        </div>
        <div className="mb-4 h-4 w-96 animate-pulse rounded bg-gray-200" />
        <div className="mb-6">
          <div className="mb-2 flex items-center justify-between">
            <div className="h-4 w-20 animate-pulse rounded bg-gray-200" />
            <div className="h-4 w-24 animate-pulse rounded bg-gray-200" />
          </div>
          <div className="h-3 w-full animate-pulse rounded-full bg-gray-200" />
        </div>
        <div className="mb-6 grid grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="rounded-lg bg-gray-100 p-3">
              <div className="mx-auto mb-2 h-8 w-12 animate-pulse rounded bg-gray-200" />
              <div className="mx-auto h-3 w-16 animate-pulse rounded bg-gray-200" />
            </div>
          ))}
        </div>
        <div className="flex gap-4 border-t border-gray-200 pt-4">
          <div className="h-14 flex-1 animate-pulse rounded-lg bg-gray-100" />
          <div className="h-14 flex-1 animate-pulse rounded-lg bg-gray-100" />
        </div>
      </div>

      {/* Upcoming Sprints Skeleton */}
      <div className="mt-8">
        <div className="mb-4 h-6 w-40 animate-pulse rounded bg-gray-200" />
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="rounded-lg border border-gray-200 bg-white p-4">
              <div className="mb-2 flex items-center justify-between">
                <div className="h-5 w-24 animate-pulse rounded bg-gray-200" />
                <div className="h-5 w-16 animate-pulse rounded-full bg-gray-200" />
              </div>
              <div className="mb-2 h-4 w-32 animate-pulse rounded bg-gray-200" />
              <div className="mb-3 h-3 w-40 animate-pulse rounded bg-gray-200" />
              <div className="flex items-center justify-between">
                <div className="h-3 w-24 animate-pulse rounded bg-gray-200" />
                <div className="h-6 w-20 animate-pulse rounded-md bg-gray-200" />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Sprints Skeleton */}
      <div className="mt-8">
        <div className="mb-4 h-6 w-44 animate-pulse rounded bg-gray-200" />
        <div className="space-y-2">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-14 animate-pulse rounded-lg bg-gray-100" />
          ))}
        </div>
      </div>

      {/* Metrics Skeleton */}
      <div className="mt-8">
        <div className="rounded-xl border border-gray-200 bg-white p-6">
          <div className="mb-4 h-6 w-32 animate-pulse rounded bg-gray-200" />
          <div className="grid grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="text-center">
                <div className="mx-auto mb-2 h-8 w-16 animate-pulse rounded bg-gray-200" />
                <div className="mx-auto h-3 w-20 animate-pulse rounded bg-gray-200" />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
