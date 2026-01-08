"use client";

/**
 * System Health Page - Next.js App Router
 * @route /admin/health
 * @status Sprint 68 - Admin Section Migration
 * @description Real-time service monitoring and resource metrics
 */

import { useRouter } from "next/navigation";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import { useSystemHealth } from "@/hooks/useAdmin";
import {
  getMetricColor,
  HEALTH_THRESHOLDS,
  type SystemStatus,
} from "@/lib/types/admin";
import {
  ArrowLeft,
  RefreshCw,
  Activity,
  Cpu,
  HardDrive,
  Database,
  MemoryStick,
  Server,
  CheckCircle,
  AlertTriangle,
  XCircle,
} from "lucide-react";

function StatusIcon({ status }: { status: SystemStatus }) {
  switch (status) {
    case "healthy":
      return <CheckCircle className="h-5 w-5 text-green-600" />;
    case "degraded":
      return <AlertTriangle className="h-5 w-5 text-yellow-600" />;
    case "unhealthy":
      return <XCircle className="h-5 w-5 text-red-600" />;
    default:
      return <Activity className="h-5 w-5 text-gray-400" />;
  }
}

function StatusBadge({ status }: { status: SystemStatus }) {
  const variants: Record<SystemStatus, "default" | "secondary" | "destructive"> = {
    healthy: "default",
    degraded: "secondary",
    unhealthy: "destructive",
  };

  const labels: Record<SystemStatus, string> = {
    healthy: "Healthy",
    degraded: "Degraded",
    unhealthy: "Unhealthy",
  };

  return (
    <Badge variant={variants[status] || "secondary"}>
      {labels[status] || status}
    </Badge>
  );
}

interface MetricCardProps {
  label: string;
  value: number | null;
  icon: React.ReactNode;
  unit?: string;
  showProgress?: boolean;
}

function MetricCard({
  label,
  value,
  icon,
  unit = "%",
  showProgress = true,
}: MetricCardProps) {
  const getProgressColor = (val: number | null) => {
    if (val === null) return "bg-gray-300";
    if (val >= HEALTH_THRESHOLDS.danger) return "bg-red-500";
    if (val >= HEALTH_THRESHOLDS.warning) return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="text-muted-foreground">{icon}</div>
            <span className="font-medium">{label}</span>
          </div>
          <span className={`text-2xl font-bold ${getMetricColor(value)}`}>
            {value !== null ? `${value.toFixed(1)}${unit}` : "N/A"}
          </span>
        </div>
        {showProgress && value !== null && (
          <div className="relative">
            <Progress value={value} className="h-2" />
            <div
              className={`absolute inset-0 h-2 rounded-full ${getProgressColor(value)}`}
              style={{ width: `${Math.min(value, 100)}%` }}
            />
          </div>
        )}
        {showProgress && (
          <div className="flex justify-between mt-1 text-xs text-muted-foreground">
            <span>0%</span>
            <span className="text-yellow-600">{HEALTH_THRESHOLDS.warning}%</span>
            <span className="text-red-600">{HEALTH_THRESHOLDS.danger}%</span>
            <span>100%</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default function SystemHealthPage() {
  const router = useRouter();

  const { data: health, isLoading, refetch, isFetching } = useSystemHealth();

  const handleRefresh = () => {
    refetch();
  };

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => router.push("/admin")}
              className="h-8 w-8 p-0"
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <h1 className="text-3xl font-bold tracking-tight">System Health</h1>
          </div>
          <p className="text-muted-foreground">
            Real-time service monitoring and resource metrics
          </p>
        </div>
        <div className="flex items-center gap-4">
          {health?.checked_at && (
            <span className="text-sm text-muted-foreground">
              Last checked: {new Date(health.checked_at).toLocaleTimeString()}
            </span>
          )}
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={isFetching}
          >
            <RefreshCw
              className={`h-4 w-4 mr-2 ${isFetching ? "animate-spin" : ""}`}
            />
            Refresh
          </Button>
        </div>
      </div>

      {/* Overall status banner */}
      {isLoading ? (
        <Skeleton className="h-24 w-full" />
      ) : health ? (
        <Card
          className={`${
            health.overall_status === "healthy"
              ? "border-green-500/50 bg-green-50/50"
              : health.overall_status === "degraded"
                ? "border-yellow-500/50 bg-yellow-50/50"
                : "border-red-500/50 bg-red-50/50"
          }`}
        >
          <CardContent className="py-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <StatusIcon status={health.overall_status} />
                <div>
                  <h2 className="text-xl font-semibold">
                    System is{" "}
                    {health.overall_status === "healthy"
                      ? "Operating Normally"
                      : health.overall_status === "degraded"
                        ? "Experiencing Issues"
                        : "Unhealthy"}
                  </h2>
                  <p className="text-sm text-muted-foreground">
                    {health.services.filter((s) => s.status === "healthy").length}{" "}
                    of {health.services.length} services healthy
                  </p>
                </div>
              </div>
              <StatusBadge status={health.overall_status} />
            </div>
          </CardContent>
        </Card>
      ) : null}

      {/* Resource metrics */}
      <div>
        <h2 className="text-lg font-semibold mb-4">Resource Usage</h2>
        {isLoading ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {[1, 2, 3, 4].map((i) => (
              <Card key={i}>
                <CardContent className="pt-6">
                  <Skeleton className="h-24 w-full" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : health?.metrics ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <MetricCard
              label="CPU Usage"
              value={health.metrics.cpu_usage_percent}
              icon={<Cpu className="h-5 w-5" />}
            />
            <MetricCard
              label="Memory Usage"
              value={health.metrics.memory_usage_percent}
              icon={<MemoryStick className="h-5 w-5" />}
            />
            <MetricCard
              label="Disk Usage"
              value={health.metrics.disk_usage_percent}
              icon={<HardDrive className="h-5 w-5" />}
            />
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <div className="text-muted-foreground">
                      <Database className="h-5 w-5" />
                    </div>
                    <span className="font-medium">DB Connections</span>
                  </div>
                  <span className="text-2xl font-bold">
                    {health.metrics.active_connections ?? "N/A"}
                  </span>
                </div>
                <p className="text-sm text-muted-foreground">
                  Active database connections
                </p>
              </CardContent>
            </Card>
          </div>
        ) : null}
      </div>

      {/* Service health */}
      <div>
        <h2 className="text-lg font-semibold mb-4">Service Status</h2>
        {isLoading ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <Card key={i}>
                <CardContent className="pt-6">
                  <Skeleton className="h-20 w-full" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : health?.services && health.services.length > 0 ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {health.services.map((service) => (
              <Card
                key={service.name}
                className={
                  service.status === "healthy"
                    ? "border-green-200"
                    : service.status === "degraded"
                      ? "border-yellow-200"
                      : "border-red-200"
                }
              >
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      <div
                        className={`p-2 rounded-lg ${
                          service.status === "healthy"
                            ? "bg-green-100"
                            : service.status === "degraded"
                              ? "bg-yellow-100"
                              : "bg-red-100"
                        }`}
                      >
                        <Server
                          className={`h-5 w-5 ${
                            service.status === "healthy"
                              ? "text-green-600"
                              : service.status === "degraded"
                                ? "text-yellow-600"
                                : "text-red-600"
                          }`}
                        />
                      </div>
                      <div>
                        <h3 className="font-semibold capitalize">
                          {service.name}
                        </h3>
                        {service.response_time_ms !== null && (
                          <p
                            className={`text-sm ${
                              service.response_time_ms >
                              HEALTH_THRESHOLDS.responseTimeDanger
                                ? "text-red-600"
                                : service.response_time_ms >
                                    HEALTH_THRESHOLDS.responseTimeWarning
                                  ? "text-yellow-600"
                                  : "text-muted-foreground"
                            }`}
                          >
                            {service.response_time_ms}ms response
                          </p>
                        )}
                      </div>
                    </div>
                    <StatusBadge status={service.status} />
                  </div>
                  {Object.keys(service.details).length > 0 && (
                    <div className="mt-3 pt-3 border-t">
                      <p className="text-xs text-muted-foreground mb-1">
                        Details:
                      </p>
                      <pre className="text-xs bg-muted p-2 rounded overflow-auto max-h-20">
                        {JSON.stringify(service.details, null, 2)}
                      </pre>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="py-8 text-center text-muted-foreground">
              No service data available
            </CardContent>
          </Card>
        )}
      </div>

      {/* Auto-refresh notice */}
      <Card className="bg-muted/50">
        <CardContent className="py-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <RefreshCw className="h-4 w-4" />
            <span>Health data auto-refreshes every 30 seconds</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
