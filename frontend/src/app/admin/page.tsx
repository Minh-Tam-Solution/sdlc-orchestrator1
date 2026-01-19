"use client";

/**
 * Admin Dashboard Page - Next.js App Router
 * @route /admin
 * @status Sprint 68 - Admin Section Migration
 * @description System-wide statistics and health overview
 * @security Requires is_superuser=true
 */

import { useRouter } from "next/navigation";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useAdminStats, useSystemHealth } from "@/hooks/useAdmin";
import {
  Users,
  UserCheck,
  UserX,
  Shield,
  FolderKanban,
  Zap,
  CheckCircle,
  ClipboardList,
  Settings,
  Activity,
  ChevronRight,
  Cpu,
  HardDrive,
  Database,
  MemoryStick,
} from "lucide-react";

// =========================================================================
// Sub-components
// =========================================================================

interface StatCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon: React.ReactNode;
  onClick?: () => void;
  variant?: "default" | "success" | "warning" | "danger";
  loading?: boolean;
}

function StatCard({
  title,
  value,
  description,
  icon,
  onClick,
  variant = "default",
  loading = false,
}: StatCardProps) {
  const variantClasses = {
    default: "",
    success: "border-green-500/50",
    warning: "border-yellow-500/50",
    danger: "border-red-500/50",
  };

  return (
    <Card
      className={`${onClick ? "cursor-pointer hover:bg-muted/50 transition-colors" : ""} ${variantClasses[variant]}`}
      onClick={onClick}
    >
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <div className="text-muted-foreground">{icon}</div>
      </CardHeader>
      <CardContent>
        {loading ? (
          <Skeleton className="h-8 w-20" />
        ) : (
          <div className="text-2xl font-bold">{value}</div>
        )}
        {description && (
          <p className="text-xs text-muted-foreground">{description}</p>
        )}
      </CardContent>
    </Card>
  );
}

function StatusBadge({ status }: { status: string }) {
  const statusConfig: Record<string, { variant: "default" | "secondary" | "destructive" | "outline"; label: string }> = {
    healthy: { variant: "default", label: "Healthy" },
    degraded: { variant: "secondary", label: "Degraded" },
    unhealthy: { variant: "destructive", label: "Unhealthy" },
  };

  const config = statusConfig[status] ?? { variant: "destructive" as const, label: "Unknown" };

  return <Badge variant={config.variant}>{config.label}</Badge>;
}

interface MetricGaugeProps {
  label: string;
  value: number | null;
  icon: React.ReactNode;
}

function MetricGauge({ label, value, icon }: MetricGaugeProps) {
  const getColor = (val: number | null) => {
    if (val === null) return "text-gray-400";
    if (val >= 90) return "text-red-600";
    if (val >= 70) return "text-yellow-600";
    return "text-green-600";
  };

  return (
    <div className="text-center p-3 rounded-lg bg-muted/50">
      <div className="flex justify-center mb-1 text-muted-foreground">{icon}</div>
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className={`text-lg font-semibold ${getColor(value)}`}>
        {value !== null ? `${value.toFixed(1)}%` : "N/A"}
      </p>
    </div>
  );
}

// =========================================================================
// Main Component
// =========================================================================

export default function AdminDashboardPage() {
  const router = useRouter();

  const { data: stats, isLoading: statsLoading } = useAdminStats();
  const { data: health, isLoading: healthLoading } = useSystemHealth();

  const adminActions = [
    {
      title: "User Management",
      description: "Manage user accounts and permissions",
      icon: <Users className="h-5 w-5" />,
      href: "/admin/users",
    },
    {
      title: "Audit Logs",
      description: "View system audit trail",
      icon: <ClipboardList className="h-5 w-5" />,
      href: "/admin/audit-logs",
    },
    {
      title: "System Settings",
      description: "Configure system parameters",
      icon: <Settings className="h-5 w-5" />,
      href: "/admin/settings",
    },
    {
      title: "System Health",
      description: "Monitor service status and metrics",
      icon: <Activity className="h-5 w-5" />,
      href: "/admin/health",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Admin Dashboard</h1>
          <p className="text-muted-foreground">
            System-wide statistics and health overview
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">System Status:</span>
          {healthLoading ? (
            <Skeleton className="h-6 w-20" />
          ) : (
            <StatusBadge status={health?.overall_status || "unknown"} />
          )}
        </div>
      </div>

      {/* User stats grid */}
      <div>
        <h2 className="text-lg font-semibold mb-4">User Statistics</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <StatCard
            title="Total Users"
            value={stats?.total_users ?? 0}
            description="All registered users"
            onClick={() => router.push("/admin/users")}
            icon={<Users className="h-4 w-4" />}
            loading={statsLoading}
          />
          <StatCard
            title="Active Users"
            value={stats?.active_users ?? 0}
            description="Users with is_active=true"
            variant="success"
            icon={<UserCheck className="h-4 w-4 text-green-600" />}
            loading={statsLoading}
          />
          <StatCard
            title="Inactive Users"
            value={stats?.inactive_users ?? 0}
            description="Deactivated accounts"
            variant={stats?.inactive_users && stats.inactive_users > 0 ? "warning" : "default"}
            icon={<UserX className="h-4 w-4" />}
            loading={statsLoading}
          />
          <StatCard
            title="Superusers"
            value={stats?.superusers ?? 0}
            description="Admin accounts"
            icon={<Shield className="h-4 w-4" />}
            loading={statsLoading}
          />
        </div>
      </div>

      {/* Project stats grid */}
      <div>
        <h2 className="text-lg font-semibold mb-4">Project Statistics</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <StatCard
            title="Total Projects"
            value={stats?.total_projects ?? 0}
            description="All projects in system"
            onClick={() => router.push("/app/projects")}
            icon={<FolderKanban className="h-4 w-4" />}
            loading={statsLoading}
          />
          <StatCard
            title="Active Projects"
            value={stats?.active_projects ?? 0}
            description="Projects with active gates"
            variant="success"
            icon={<Zap className="h-4 w-4 text-green-600" />}
            loading={statsLoading}
          />
          <StatCard
            title="Total Gates"
            value={stats?.total_gates ?? 0}
            description="All quality gates"
            onClick={() => router.push("/app/gates")}
            icon={<CheckCircle className="h-4 w-4" />}
            loading={statsLoading}
          />
        </div>
      </div>

      {/* Quick actions and system health */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Quick actions */}
        <Card>
          <CardHeader>
            <CardTitle>Admin Actions</CardTitle>
            <CardDescription>Quick access to admin functions</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {adminActions.map((action) => (
                <div
                  key={action.href}
                  className="flex items-center gap-3 rounded-lg border p-3 hover:bg-muted transition-colors cursor-pointer"
                  onClick={() => router.push(action.href)}
                >
                  <div className="text-muted-foreground">{action.icon}</div>
                  <div className="flex-1">
                    <p className="font-medium">{action.title}</p>
                    <p className="text-sm text-muted-foreground">
                      {action.description}
                    </p>
                  </div>
                  <ChevronRight className="h-4 w-4 text-muted-foreground" />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* System health overview */}
        <Card>
          <CardHeader>
            <CardTitle>System Health</CardTitle>
            <CardDescription>
              Service status overview
              {health?.checked_at && (
                <span className="ml-2 text-xs">
                  (Last checked: {new Date(health.checked_at).toLocaleTimeString()})
                </span>
              )}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {healthLoading ? (
              <div className="space-y-3">
                {[1, 2, 3].map((i) => (
                  <Skeleton key={i} className="h-10 w-full" />
                ))}
              </div>
            ) : health?.services && health.services.length > 0 ? (
              <div className="space-y-3">
                {health.services.map((service) => (
                  <div
                    key={service.name}
                    className="flex items-center justify-between border-b pb-2 last:border-0"
                  >
                    <div className="flex items-center gap-2">
                      <div
                        className={`h-2 w-2 rounded-full ${
                          service.status === "healthy"
                            ? "bg-green-500"
                            : service.status === "degraded"
                              ? "bg-yellow-500"
                              : "bg-red-500"
                        }`}
                      />
                      <span className="font-medium capitalize">{service.name}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      {service.response_time_ms !== null && (
                        <span className="text-xs text-muted-foreground">
                          {service.response_time_ms}ms
                        </span>
                      )}
                      <StatusBadge status={service.status} />
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-muted-foreground py-4">
                No service data available
              </div>
            )}

            {/* System metrics */}
            {health?.metrics && (
              <div className="mt-4 pt-4 border-t">
                <h4 className="text-sm font-medium mb-3">Resource Usage</h4>
                <div className="grid grid-cols-2 gap-3">
                  <MetricGauge
                    label="CPU"
                    value={health.metrics.cpu_usage_percent}
                    icon={<Cpu className="h-4 w-4" />}
                  />
                  <MetricGauge
                    label="Memory"
                    value={health.metrics.memory_usage_percent}
                    icon={<MemoryStick className="h-4 w-4" />}
                  />
                  <MetricGauge
                    label="Disk"
                    value={health.metrics.disk_usage_percent}
                    icon={<HardDrive className="h-4 w-4" />}
                  />
                  <div className="text-center p-3 rounded-lg bg-muted/50">
                    <div className="flex justify-center mb-1 text-muted-foreground">
                      <Database className="h-4 w-4" />
                    </div>
                    <p className="text-xs text-muted-foreground">DB Connections</p>
                    <p className="text-lg font-semibold">
                      {health.metrics.active_connections ?? "N/A"}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
