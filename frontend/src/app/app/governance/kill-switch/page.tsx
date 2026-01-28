/**
 * =========================================================================
 * Kill Switch Admin Page
 * SDLC Orchestrator - Sprint 113 (Governance UI - Kill Switch Admin)
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Framework: SDLC 5.3.0 Quality Assurance System
 * ADR Reference: ADR-041
 *
 * Purpose: Kill switch administration with mode toggle, dashboard, and audit
 * =========================================================================
 */

"use client";

import { useRouter } from "next/navigation";
import {
  GovernanceModeToggle,
  KillSwitchDashboard,
  ModeHistoryTimeline,
  BreakGlassButton,
  AuditLogTable,
} from "@/components/governance";

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

function ArrowLeftIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={2}
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18"
      />
    </svg>
  );
}

function ShieldExclamationIcon({ className }: { className?: string }) {
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
        d="M12 9v3.75m0-10.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.75c0 5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.57-.598-3.75h-.152c-3.196 0-6.1-1.25-8.25-3.286Zm0 13.036h.008v.008H12v-.008Z"
      />
    </svg>
  );
}

// =============================================================================
// Page Component
// =============================================================================

export default function KillSwitchPage() {
  const router = useRouter();

  const handleModeChanged = (
    newMode: "OFF" | "WARNING" | "SOFT" | "FULL",
    previousMode: "OFF" | "WARNING" | "SOFT" | "FULL"
  ) => {
    console.log(`Mode changed from ${previousMode} to ${newMode}`);
    // Could trigger notifications or other side effects
  };

  const handleBreakGlassCreated = (request: { incident_type: string; reason: string }) => {
    console.log(`Break glass requested: ${request.incident_type} - ${request.reason}`);
    // Trigger emergency notifications
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => router.push("/app/governance")}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeftIcon className="h-5 w-5 text-gray-600" />
              </button>
              <div className="flex items-center gap-3">
                <BoltIcon className="h-8 w-8 text-amber-600" />
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    Kill Switch Admin
                  </h1>
                  <p className="text-sm text-gray-500">
                    Governance mode control and emergency bypass
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Warning Banner */}
      <div className="bg-amber-50 border-b border-amber-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <div className="flex items-center gap-3 text-amber-800">
            <ShieldExclamationIcon className="h-5 w-5" />
            <span className="text-sm">
              <strong>CTO/CEO Authorization Required:</strong> Mode changes and
              break glass activations are logged and require executive approval.
            </span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Top Row: Mode Toggle + Dashboard */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <GovernanceModeToggle onModeChanged={handleModeChanged} />
          <KillSwitchDashboard showHealthIndicators={true} />
        </div>

        {/* Middle Row: Timeline + Break Glass */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="lg:col-span-2">
            <ModeHistoryTimeline limit={10} showLoadMore={true} />
          </div>
          <div>
            <BreakGlassButton
              onBreakGlassCreated={handleBreakGlassCreated}
            />
          </div>
        </div>

        {/* Bottom Row: Audit Log */}
        <div>
          <AuditLogTable initialLimit={20} />
        </div>
      </main>
    </div>
  );
}
