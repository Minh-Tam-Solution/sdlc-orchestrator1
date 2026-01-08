/**
 * Code Generation Loading State
 * @module frontend/landing/src/app/app/code-generation/loading
 * @status Sprint 66 - EP-06 Migration
 */

export default function CodeGenerationLoading() {
  return (
    <div className="space-y-6">
      {/* Breadcrumb skeleton */}
      <div className="flex items-center gap-2">
        <div className="h-4 w-20 bg-gray-200 rounded animate-pulse" />
        <span className="text-muted-foreground">/</span>
        <div className="h-4 w-24 bg-gray-200 rounded animate-pulse" />
        <span className="text-muted-foreground">/</span>
        <div className="h-4 w-32 bg-gray-200 rounded animate-pulse" />
      </div>

      {/* Header skeleton */}
      <div className="flex items-start justify-between">
        <div>
          <div className="h-9 w-48 bg-gray-200 rounded animate-pulse" />
          <div className="h-5 w-80 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="h-10 w-36 bg-gray-200 rounded animate-pulse" />
      </div>

      {/* Blueprint Summary skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6">
          <div className="h-6 w-48 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-64 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
      </div>

      {/* Quality Gates skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b">
          <div className="h-6 w-48 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-72 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6">
          <div className="grid grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="p-4 rounded-lg border text-center">
                <div className="h-8 w-16 bg-gray-200 rounded animate-pulse mx-auto mb-2" />
                <div className="h-5 w-20 bg-gray-200 rounded animate-pulse mx-auto mb-1" />
                <div className="h-3 w-24 bg-gray-200 rounded animate-pulse mx-auto mb-2" />
                <div className="h-5 w-16 bg-gray-200 rounded-full animate-pulse mx-auto" />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Blueprint Details skeleton */}
      <div className="bg-white rounded-lg border shadow-sm">
        <div className="p-6 border-b">
          <div className="h-6 w-40 bg-gray-200 rounded animate-pulse" />
        </div>
        <div className="p-6">
          <div className="h-64 bg-gray-200 rounded animate-pulse" />
        </div>
      </div>
    </div>
  );
}
