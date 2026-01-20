/**
 * Team Detail Loading State
 * @module frontend/src/app/app/teams/[id]/loading
 * @status Sprint 84 - Teams & Organizations UI
 */

export default function TeamDetailLoading() {
  return (
    <div className="space-y-6">
      {/* Back link skeleton */}
      <div className="h-5 w-24 rounded bg-gray-200 animate-pulse" />

      {/* Header skeleton */}
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <div className="h-8 w-48 rounded bg-gray-200 animate-pulse" />
          <div className="h-4 w-64 rounded bg-gray-200 animate-pulse" />
          <div className="h-5 w-20 rounded-full bg-gray-200 animate-pulse" />
        </div>
        <div className="flex gap-2">
          <div className="h-10 w-20 rounded-lg bg-gray-200 animate-pulse" />
          <div className="h-10 w-20 rounded-lg bg-gray-200 animate-pulse" />
        </div>
      </div>

      {/* Stats skeleton */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
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

      {/* Members table skeleton */}
      <div className="rounded-lg border border-gray-200 bg-white">
        <div className="flex items-center justify-between border-b border-gray-200 px-6 py-4">
          <div className="h-6 w-36 rounded bg-gray-200 animate-pulse" />
          <div className="h-10 w-32 rounded-lg bg-gray-200 animate-pulse" />
        </div>
        <div className="p-6 space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex items-center gap-4 animate-pulse">
              <div className="h-8 w-8 rounded-full bg-gray-200" />
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
