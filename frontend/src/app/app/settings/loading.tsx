/**
 * Settings Page Loading State
 * @module frontend/landing/src/app/app/settings/loading
 * @status Sprint 64 - Route Group Migration
 */

export default function SettingsLoading() {
  return (
    <div className="space-y-6">
      {/* Page header skeleton */}
      <div>
        <div className="h-9 w-32 bg-gray-200 rounded animate-pulse" />
        <div className="h-5 w-64 bg-gray-200 rounded animate-pulse mt-2" />
      </div>

      {/* Profile Section skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b">
          <div className="h-6 w-24 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-48 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6">
          <div className="flex items-center gap-4">
            <div className="h-16 w-16 bg-gray-200 rounded-full animate-pulse" />
            <div className="space-y-2">
              <div className="h-5 w-32 bg-gray-200 rounded animate-pulse" />
              <div className="h-4 w-48 bg-gray-200 rounded animate-pulse" />
            </div>
          </div>
        </div>
      </div>

      {/* API Keys Section skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b">
          <div className="h-6 w-24 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-64 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6 space-y-4">
          <div className="h-20 bg-gray-200 rounded animate-pulse" />
          <div className="h-10 bg-gray-200 rounded animate-pulse" />
        </div>
      </div>

      {/* GitHub Section skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b">
          <div className="h-6 w-40 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-72 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6">
          <div className="h-20 bg-gray-200 rounded animate-pulse" />
        </div>
      </div>
    </div>
  );
}
