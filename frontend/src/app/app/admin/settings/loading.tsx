/**
 * Admin Settings Loading Skeleton - SDLC Orchestrator
 *
 * @module frontend/src/app/app/admin/settings/loading
 * @description Loading state for Admin System Settings page
 * @sdlc SDLC 5.1.3 Framework - Sprint 86 Phase 2 (ADR-027)
 */

export default function AdminSettingsLoading() {
  return (
    <div className="p-6 max-w-5xl mx-auto animate-pulse">
      {/* Header Skeleton */}
      <div className="mb-6">
        <div className="h-8 w-48 bg-gray-200 rounded mb-2" />
        <div className="h-4 w-96 bg-gray-100 rounded" />
      </div>

      {/* Info Banner Skeleton */}
      <div className="mb-6 bg-blue-50 border border-blue-100 rounded-lg p-3">
        <div className="h-4 w-full bg-blue-100 rounded" />
      </div>

      {/* Category Tabs Skeleton */}
      <div className="flex gap-2 mb-6">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-10 w-28 bg-gray-200 rounded-lg" />
        ))}
      </div>

      {/* Settings Panel Skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-4 border-b bg-gray-50">
          <div className="h-5 w-24 bg-gray-200 rounded mb-1" />
          <div className="h-4 w-64 bg-gray-100 rounded" />
        </div>

        <div className="p-4 space-y-4">
          {[1, 2, 3, 4].map((i) => (
            <div
              key={i}
              className="flex items-center justify-between py-4 border-b border-gray-100 last:border-b-0"
            >
              <div className="flex-1 space-y-2">
                <div className="flex items-center gap-2">
                  <div className="h-5 w-40 bg-gray-200 rounded" />
                  <div className="h-4 w-16 bg-gray-100 rounded" />
                </div>
                <div className="h-4 w-80 bg-gray-100 rounded" />
                <div className="h-3 w-48 bg-gray-50 rounded" />
              </div>
              <div className="flex items-center gap-3">
                <div className="h-8 w-24 bg-gray-200 rounded-lg" />
                <div className="h-4 w-12 bg-gray-100 rounded" />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer Skeleton */}
      <div className="mt-6">
        <div className="h-4 w-64 bg-gray-100 rounded" />
      </div>
    </div>
  );
}
