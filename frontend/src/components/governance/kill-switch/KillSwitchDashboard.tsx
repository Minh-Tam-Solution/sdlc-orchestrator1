/**
 * =========================================================================
 * Kill Switch Dashboard Component
 * SDLC Orchestrator - Sprint 113 (Governance UI - Kill Switch Admin)
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Framework: SDLC 5.3.0 Quality Assurance System
 * ADR Reference: ADR-041
 *
 * Purpose: Display kill switch criteria, thresholds, and auto-rollback status
 * =========================================================================
 */

"use client";

import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { useKillSwitchCheck, useKillSwitchDashboard } from "@/hooks/useKillSwitch";

// =============================================================================
// Icons
// =============================================================================

function BoltIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z"
      />
    </svg>
  );
}

function ExclamationTriangleIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z"
      />
    </svg>
  );
}

function CheckCircleIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>
  );
}

function ClockIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>
  );
}

function XCircleIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>
  );
}

// =============================================================================
// Utility Functions
// =============================================================================

function getStatusColor(triggered: boolean): string {
  return triggered ? "text-red-600" : "text-green-600";
}

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

function formatMs(value: number): string {
  return `${value.toFixed(0)}ms`;
}

// =============================================================================
// Component
// =============================================================================

interface KillSwitchDashboardProps {
  showHealthIndicators?: boolean;
}

export function KillSwitchDashboard({
  showHealthIndicators = true,
}: KillSwitchDashboardProps) {
  const { data: killSwitchResult, isLoading: isCheckLoading } = useKillSwitchCheck();
  const { data: dashboard, isLoading: isDashboardLoading } = useKillSwitchDashboard();

  const isLoading = isCheckLoading || isDashboardLoading;

  if (isLoading) {
    return (
      <Card>
        <CardContent className="py-8">
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
          </div>
        </CardContent>
      </Card>
    );
  }

  const criteria = killSwitchResult?.current_metrics;
  const shouldTrigger = killSwitchResult?.should_trigger || false;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BoltIcon className="h-5 w-5 text-amber-600" />
            <CardTitle className="text-lg">Kill Switch Status</CardTitle>
          </div>
          <Badge
            className={
              shouldTrigger
                ? "bg-red-100 text-red-700 border-red-200"
                : "bg-green-100 text-green-700 border-green-200"
            }
          >
            {shouldTrigger ? (
              <>
                <ExclamationTriangleIcon className="h-3 w-3 mr-1" />
                Triggered
              </>
            ) : (
              <>
                <CheckCircleIcon className="h-3 w-3 mr-1" />
                Normal
              </>
            )}
          </Badge>
        </div>
        <CardDescription>
          Automatic rollback criteria and current system metrics
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Criteria Gauges */}
        {criteria && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Rejection Rate */}
            <div className="p-4 border rounded-lg space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-medium text-sm">Rejection Rate</span>
                <span className={getStatusColor(criteria.rejection_rate_triggered)}>
                  {criteria.rejection_rate_triggered ? (
                    <XCircleIcon className="h-4 w-4" />
                  ) : (
                    <CheckCircleIcon className="h-4 w-4" />
                  )}
                </span>
              </div>
              <Progress
                value={(criteria.rejection_rate_current / criteria.rejection_rate_threshold) * 100}
                className="h-2"
              />
              <div className="flex justify-between text-xs text-gray-500">
                <span>Current: {formatPercent(criteria.rejection_rate_current)}</span>
                <span>Threshold: {formatPercent(criteria.rejection_rate_threshold)}</span>
              </div>
            </div>

            {/* Latency P95 */}
            <div className="p-4 border rounded-lg space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-medium text-sm">Latency (P95)</span>
                <span className={getStatusColor(criteria.latency_triggered)}>
                  {criteria.latency_triggered ? (
                    <XCircleIcon className="h-4 w-4" />
                  ) : (
                    <CheckCircleIcon className="h-4 w-4" />
                  )}
                </span>
              </div>
              <Progress
                value={
                  (criteria.latency_p95_current_ms / criteria.latency_p95_threshold_ms) * 100
                }
                className="h-2"
              />
              <div className="flex justify-between text-xs text-gray-500">
                <span>Current: {formatMs(criteria.latency_p95_current_ms)}</span>
                <span>Threshold: {formatMs(criteria.latency_p95_threshold_ms)}</span>
              </div>
            </div>

            {/* False Positive Rate */}
            <div className="p-4 border rounded-lg space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-medium text-sm">False Positive Rate</span>
                <span className={getStatusColor(criteria.false_positive_triggered)}>
                  {criteria.false_positive_triggered ? (
                    <XCircleIcon className="h-4 w-4" />
                  ) : (
                    <CheckCircleIcon className="h-4 w-4" />
                  )}
                </span>
              </div>
              <Progress
                value={
                  (criteria.false_positive_current / criteria.false_positive_threshold) * 100
                }
                className="h-2"
              />
              <div className="flex justify-between text-xs text-gray-500">
                <span>Current: {formatPercent(criteria.false_positive_current)}</span>
                <span>Threshold: {formatPercent(criteria.false_positive_threshold)}</span>
              </div>
            </div>

            {/* Developer Complaints */}
            <div className="p-4 border rounded-lg space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-medium text-sm">Developer Complaints</span>
                <span className={getStatusColor(criteria.complaints_triggered)}>
                  {criteria.complaints_triggered ? (
                    <XCircleIcon className="h-4 w-4" />
                  ) : (
                    <CheckCircleIcon className="h-4 w-4" />
                  )}
                </span>
              </div>
              <Progress
                value={
                  (criteria.developer_complaints_current /
                    criteria.developer_complaints_threshold) *
                  100
                }
                className="h-2"
              />
              <div className="flex justify-between text-xs text-gray-500">
                <span>Current: {criteria.developer_complaints_current}</span>
                <span>Threshold: {criteria.developer_complaints_threshold}</span>
              </div>
            </div>
          </div>
        )}

        {/* Triggered Criteria List */}
        {killSwitchResult?.triggered_criteria &&
          killSwitchResult.triggered_criteria.length > 0 && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center gap-2 text-red-700 font-medium mb-2">
                <ExclamationTriangleIcon className="h-5 w-5" />
                Triggered Criteria
              </div>
              <ul className="list-disc list-inside text-sm text-red-600 space-y-1">
                {killSwitchResult.triggered_criteria.map((criteria, idx) => (
                  <li key={idx}>{criteria}</li>
                ))}
              </ul>
              <div className="mt-3 text-sm text-red-600">
                Recommended action:{" "}
                <strong>{killSwitchResult.recommended_action.replace("_", " ")}</strong>
              </div>
            </div>
          )}

        {/* Health Indicators */}
        {showHealthIndicators && dashboard?.health && (
          <div className="border-t pt-4">
            <div className="text-sm font-medium mb-3">Service Health</div>
            <div className="grid grid-cols-3 gap-3">
              {Object.entries(dashboard.health).map(([service, status]) => (
                <div
                  key={service}
                  className="flex items-center gap-2 text-sm"
                >
                  <div
                    className={`h-2 w-2 rounded-full ${
                      status === "healthy"
                        ? "bg-green-500"
                        : status === "degraded"
                        ? "bg-yellow-500"
                        : "bg-red-500"
                    }`}
                  />
                  <span className="capitalize">{service.replace("_", " ")}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Last Check Timestamp */}
        {killSwitchResult?.last_check && (
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <ClockIcon className="h-3 w-3" />
            Last checked: {new Date(killSwitchResult.last_check).toLocaleString()}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default KillSwitchDashboard;
