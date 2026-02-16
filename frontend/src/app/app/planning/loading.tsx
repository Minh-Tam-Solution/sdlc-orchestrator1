/**
 * Planning Page Loading State - SDLC Orchestrator
 *
 * @module frontend/src/app/app/planning/loading
 * @description Loading skeleton for Planning Hierarchy page
 * @sdlc SDLC 6.0.6 Framework - Sprint 87
 */

export default function PlanningLoading() {
  return (
    <div className="p-6">
      {/* Header Skeleton */}
      <div className="mb-6">
        <div className="h-8 w-48 animate-pulse rounded bg-gray-200" />
        <div className="mt-2 h-4 w-64 animate-pulse rounded bg-gray-200" />
      </div>

      {/* Stats Skeleton */}
      <div className="mb-6 grid gap-4 md:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-20 animate-pulse rounded-lg bg-gray-200" />
        ))}
      </div>

      {/* Main Content Skeleton */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="h-6 w-32 animate-pulse rounded bg-gray-200" />
          <div className="flex gap-2">
            <div className="h-8 w-20 animate-pulse rounded bg-gray-200" />
            <div className="h-8 w-20 animate-pulse rounded bg-gray-200" />
          </div>
        </div>

        {/* Tree/Timeline Skeleton */}
        <div className="rounded-xl border border-gray-200 bg-white p-4">
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="flex items-center gap-3">
                <div
                  className="h-10 animate-pulse rounded bg-gray-200"
                  style={{ marginLeft: `${(i - 1) * 24}px`, width: `calc(100% - ${(i - 1) * 24}px)` }}
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
