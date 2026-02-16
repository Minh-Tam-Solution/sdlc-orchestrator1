/**
 * CLI Tokens Loading Skeleton - SDLC Orchestrator
 *
 * @module frontend/src/app/app/cli-tokens/loading
 * @description Loading skeleton for CLI tokens page
 * @sdlc SDLC 6.0.6 Framework - Sprint 85 (CLI Authentication)
 * @status Sprint 85 - CTO APPROVED (January 20, 2026)
 */

export default function CliTokensLoading() {
  return (
    <div className="space-y-6">
      {/* Header skeleton */}
      <div className="flex items-start justify-between">
        <div>
          <div className="h-8 w-32 bg-gray-200 rounded animate-pulse" />
          <div className="mt-2 h-4 w-64 bg-gray-200 rounded animate-pulse" />
        </div>
        <div className="flex gap-2">
          <div className="h-10 w-24 bg-gray-200 rounded animate-pulse" />
          <div className="h-10 w-32 bg-gray-200 rounded animate-pulse" />
        </div>
      </div>

      {/* Stats skeleton */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-24 rounded-lg border bg-white p-4 animate-pulse">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-gray-200" />
              <div className="space-y-2">
                <div className="h-3 w-16 bg-gray-200 rounded" />
                <div className="h-6 w-12 bg-gray-200 rounded" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick start skeleton */}
      <div className="h-48 rounded-lg bg-gray-800 animate-pulse" />

      {/* Tokens section skeleton */}
      <div>
        <div className="h-6 w-32 bg-gray-200 rounded animate-pulse mb-4" />
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="rounded-lg border bg-white p-4 animate-pulse">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <div className="h-5 w-24 bg-gray-200 rounded" />
                  <div className="h-5 w-16 bg-gray-200 rounded-full" />
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-4 w-48 bg-gray-100 rounded" />
                  <div className="h-4 w-24 bg-gray-100 rounded" />
                  <div className="h-4 w-24 bg-gray-100 rounded" />
                </div>
                <div className="flex gap-1">
                  <div className="h-5 w-16 bg-blue-50 rounded" />
                  <div className="h-5 w-16 bg-blue-50 rounded" />
                  <div className="h-5 w-16 bg-blue-50 rounded" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
