import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export default function HealthLoading() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Skeleton className="h-8 w-8" />
            <Skeleton className="h-9 w-40" />
          </div>
          <Skeleton className="h-5 w-72" />
        </div>
        <div className="flex items-center gap-4">
          <Skeleton className="h-5 w-40" />
          <Skeleton className="h-9 w-24" />
        </div>
      </div>

      {/* Status banner */}
      <Skeleton className="h-24 w-full" />

      {/* Resource metrics */}
      <div>
        <Skeleton className="h-6 w-32 mb-4" />
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <Card key={i}>
              <CardContent className="pt-6">
                <Skeleton className="h-24 w-full" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Service health */}
      <div>
        <Skeleton className="h-6 w-32 mb-4" />
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Card key={i}>
              <CardContent className="pt-6">
                <Skeleton className="h-20 w-full" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
