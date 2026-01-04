/**
 * App Builder Loading State
 * @module frontend/landing/src/app/platform-admin/app-builder/loading
 * @status Sprint 66 - EP-06 Migration
 */

export default function AppBuilderLoading() {
  return (
    <div className="space-y-6">
      {/* Breadcrumb skeleton */}
      <div className="flex items-center gap-2">
        <div className="h-4 w-20 bg-gray-200 rounded animate-pulse" />
        <span className="text-muted-foreground">/</span>
        <div className="h-4 w-24 bg-gray-200 rounded animate-pulse" />
      </div>

      {/* Header skeleton */}
      <div>
        <div className="h-9 w-72 bg-gray-200 rounded animate-pulse" />
        <div className="h-5 w-96 bg-gray-200 rounded animate-pulse mt-2" />
      </div>

      {/* Start Session Card skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b">
          <div className="h-6 w-32 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-80 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6">
          <div className="h-10 w-48 bg-gray-200 rounded animate-pulse" />
        </div>
      </div>

      {/* Questionnaire Card skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b">
          <div className="h-6 w-32 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-64 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6 space-y-6">
          {/* Domain field */}
          <div className="space-y-2">
            <div className="h-4 w-16 bg-gray-200 rounded animate-pulse" />
            <div className="h-10 w-full bg-gray-200 rounded animate-pulse" />
          </div>

          {/* App name field */}
          <div className="space-y-2">
            <div className="h-4 w-32 bg-gray-200 rounded animate-pulse" />
            <div className="h-10 w-full bg-gray-200 rounded animate-pulse" />
          </div>

          {/* Features field */}
          <div className="space-y-2">
            <div className="h-4 w-20 bg-gray-200 rounded animate-pulse" />
            <div className="h-40 w-full bg-gray-200 rounded animate-pulse" />
          </div>

          {/* Scale field */}
          <div className="space-y-2">
            <div className="h-4 w-28 bg-gray-200 rounded animate-pulse" />
            <div className="h-10 w-full bg-gray-200 rounded animate-pulse" />
          </div>

          {/* Generate button */}
          <div className="h-10 w-48 bg-gray-200 rounded animate-pulse" />
        </div>
      </div>

      {/* Blueprint Card skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b">
          <div className="h-6 w-48 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-72 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6">
          <div className="h-72 w-full bg-gray-200 rounded animate-pulse" />
        </div>
      </div>
    </div>
  );
}
