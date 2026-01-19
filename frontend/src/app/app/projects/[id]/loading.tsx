/**
 * Project Detail Loading State
 * @module frontend/landing/src/app/app/projects/[id]/loading
 * @status Sprint 64 - Route Group Migration
 */

export default function ProjectDetailLoading() {
  return (
    <div className="space-y-6">
      {/* Breadcrumb skeleton */}
      <div className="flex items-center gap-2">
        <div className="h-4 w-20 bg-gray-200 rounded animate-pulse" />
        <div className="h-4 w-4 bg-gray-200 rounded animate-pulse" />
        <div className="h-4 w-32 bg-gray-200 rounded animate-pulse" />
      </div>

      {/* Title skeleton */}
      <div>
        <div className="h-10 w-64 bg-gray-200 rounded animate-pulse" />
        <div className="h-5 w-96 bg-gray-200 rounded animate-pulse mt-2" />
      </div>

      {/* Stats cards skeleton */}
      <div className="grid gap-4 md:grid-cols-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-white rounded-lg border p-6">
            <div className="h-4 w-24 bg-gray-200 rounded animate-pulse mb-3" />
            <div className="h-8 w-20 bg-gray-200 rounded animate-pulse" />
            <div className="h-3 w-32 bg-gray-200 rounded animate-pulse mt-2" />
          </div>
        ))}
      </div>

      {/* Timeline skeleton */}
      <div className="bg-white rounded-lg border">
        <div className="p-6 border-b">
          <div className="h-6 w-48 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-64 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6">
          <div className="flex gap-4 overflow-x-auto">
            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((i) => (
              <div key={i} className="flex flex-col items-center min-w-[80px]">
                <div className="w-10 h-10 bg-gray-200 rounded-full animate-pulse" />
                <div className="h-3 w-16 bg-gray-200 rounded animate-pulse mt-2" />
                <div className="h-3 w-10 bg-gray-200 rounded animate-pulse mt-1" />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Gates list skeleton */}
      <div className="bg-white rounded-lg border">
        <div className="p-6 border-b">
          <div className="h-6 w-32 bg-gray-200 rounded animate-pulse" />
          <div className="h-4 w-48 bg-gray-200 rounded animate-pulse mt-2" />
        </div>
        <div className="p-6 space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex items-center gap-4 p-4 border rounded-lg">
              <div className="w-10 h-10 bg-gray-200 rounded-full animate-pulse" />
              <div className="flex-1">
                <div className="h-5 w-32 bg-gray-200 rounded animate-pulse" />
                <div className="h-4 w-48 bg-gray-200 rounded animate-pulse mt-1" />
              </div>
              <div className="h-6 w-20 bg-gray-200 rounded-full animate-pulse" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
