/**
 * =========================================================================
 * Governance Mode Toggle Component
 * SDLC Orchestrator - Sprint 113 (Governance UI - Kill Switch Admin)
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Framework: SDLC 6.0.6 Quality Assurance System
 * ADR Reference: ADR-041
 *
 * Purpose: Toggle governance enforcement mode (OFF/WARNING/SOFT/FULL)
 * =========================================================================
 */

"use client";

import { useState } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  useGovernanceMode,
  useSetGovernanceMode,
  useCanChangeMode,
} from "@/hooks/useKillSwitch";
import type { GovernanceMode } from "@/lib/types/kill-switch";

// =============================================================================
// Icons
// =============================================================================

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

function LockClosedIcon({ className }: { className?: string }) {
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
        d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z"
      />
    </svg>
  );
}

// =============================================================================
// Mode Configuration
// =============================================================================

interface ModeConfig {
  label: string;
  description: string;
  icon: React.ReactNode;
  bgColor: string;
  textColor: string;
  borderColor: string;
}

const MODE_CONFIG: Record<GovernanceMode, ModeConfig> = {
  OFF: {
    label: "Off",
    description: "Governance disabled - All PRs pass without checks",
    icon: <ShieldExclamationIcon className="h-5 w-5" />,
    bgColor: "bg-gray-100",
    textColor: "text-gray-700",
    borderColor: "border-gray-300",
  },
  WARNING: {
    label: "Warning",
    description: "Log violations but allow all PRs to merge",
    icon: <ShieldExclamationIcon className="h-5 w-5" />,
    bgColor: "bg-yellow-50",
    textColor: "text-yellow-700",
    borderColor: "border-yellow-300",
  },
  SOFT: {
    label: "Soft",
    description: "Block critical violations only (Red PRs)",
    icon: <ShieldExclamationIcon className="h-5 w-5" />,
    bgColor: "bg-orange-50",
    textColor: "text-orange-700",
    borderColor: "border-orange-300",
  },
  FULL: {
    label: "Full",
    description: "All violations block - Only Green PRs can merge",
    icon: <CheckCircleIcon className="h-5 w-5" />,
    bgColor: "bg-green-50",
    textColor: "text-green-700",
    borderColor: "border-green-300",
  },
};

const MODES: GovernanceMode[] = ["OFF", "WARNING", "SOFT", "FULL"];

// =============================================================================
// Component
// =============================================================================

interface GovernanceModeToggleProps {
  onModeChanged?: (newMode: GovernanceMode, previousMode: GovernanceMode) => void;
}

export function GovernanceModeToggle({ onModeChanged }: GovernanceModeToggleProps) {
  const { data: modeStatus, isLoading } = useGovernanceMode();
  const setModeMutation = useSetGovernanceMode();
  const canChange = useCanChangeMode();

  const [selectedMode, setSelectedMode] = useState<GovernanceMode | null>(null);
  const [reason, setReason] = useState("");
  const [showConfirmation, setShowConfirmation] = useState(false);

  const currentMode = modeStatus?.mode || "OFF";

  const handleModeSelect = (mode: GovernanceMode) => {
    if (!canChange) return;
    if (mode === currentMode) return;

    setSelectedMode(mode);
    setShowConfirmation(true);
  };

  const handleConfirm = async () => {
    if (!selectedMode) return;

    try {
      await setModeMutation.mutateAsync({
        mode: selectedMode,
        reason: reason || `Mode changed to ${selectedMode}`,
        notify_stakeholders: true,
      });

      onModeChanged?.(selectedMode, currentMode);
      setShowConfirmation(false);
      setSelectedMode(null);
      setReason("");
    } catch {
      // Error handled by mutation
    }
  };

  const handleCancel = () => {
    setShowConfirmation(false);
    setSelectedMode(null);
    setReason("");
  };

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

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <LockClosedIcon className="h-5 w-5 text-blue-600" />
            <CardTitle className="text-lg">Governance Mode</CardTitle>
          </div>
          <Badge className={`${MODE_CONFIG[currentMode].bgColor} ${MODE_CONFIG[currentMode].textColor}`}>
            {MODE_CONFIG[currentMode].label} Mode
          </Badge>
        </div>
        <CardDescription>
          Control how governance rules are enforced across all repositories
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Mode Selection Grid */}
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          {MODES.map((mode) => {
            const config = MODE_CONFIG[mode];
            const isSelected = mode === currentMode;
            const isPending = mode === selectedMode;

            return (
              <button
                key={mode}
                onClick={() => handleModeSelect(mode)}
                disabled={!canChange || setModeMutation.isPending}
                className={`
                  relative p-4 rounded-lg border-2 transition-all
                  ${isSelected ? `${config.borderColor} ${config.bgColor}` : "border-gray-200 bg-white"}
                  ${isPending && !isSelected ? "ring-2 ring-blue-500" : ""}
                  ${canChange ? "hover:border-gray-300 cursor-pointer" : "opacity-60 cursor-not-allowed"}
                `}
              >
                <div className="flex flex-col items-center gap-2">
                  <div className={isSelected ? config.textColor : "text-gray-400"}>
                    {config.icon}
                  </div>
                  <span className={`font-medium ${isSelected ? config.textColor : "text-gray-600"}`}>
                    {config.label}
                  </span>
                </div>
                {isSelected && (
                  <div className="absolute top-2 right-2">
                    <CheckCircleIcon className={`h-4 w-4 ${config.textColor}`} />
                  </div>
                )}
              </button>
            );
          })}
        </div>

        {/* Current Mode Description */}
        <div className={`p-3 rounded-lg ${MODE_CONFIG[currentMode].bgColor}`}>
          <p className={`text-sm ${MODE_CONFIG[currentMode].textColor}`}>
            {MODE_CONFIG[currentMode].description}
          </p>
        </div>

        {/* Authorization Warning */}
        {!canChange && (
          <div className="flex items-center gap-2 text-sm text-amber-600 bg-amber-50 p-3 rounded-lg">
            <LockClosedIcon className="h-4 w-4" />
            <span>CTO or CEO authorization required to change governance mode</span>
          </div>
        )}

        {/* Last Changed Info */}
        {modeStatus && (
          <div className="text-sm text-gray-500">
            Last changed by <strong>{modeStatus.changed_by}</strong> on{" "}
            {new Date(modeStatus.last_changed).toLocaleDateString()} at{" "}
            {new Date(modeStatus.last_changed).toLocaleTimeString()}
            {modeStatus.change_reason && (
              <span className="block mt-1 text-gray-400">
                Reason: {modeStatus.change_reason}
              </span>
            )}
          </div>
        )}

        {/* Confirmation Dialog */}
        {showConfirmation && selectedMode && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              <h3 className="text-lg font-semibold mb-2">Confirm Mode Change</h3>
              <p className="text-gray-600 mb-4">
                Change governance mode from{" "}
                <strong className={MODE_CONFIG[currentMode].textColor}>
                  {MODE_CONFIG[currentMode].label}
                </strong>{" "}
                to{" "}
                <strong className={MODE_CONFIG[selectedMode].textColor}>
                  {MODE_CONFIG[selectedMode].label}
                </strong>
                ?
              </p>

              <div className="space-y-3 mb-4">
                <Label htmlFor="reason">Reason for change (required)</Label>
                <Textarea
                  id="reason"
                  placeholder="Enter reason for mode change..."
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                />
              </div>

              <div className="flex gap-2 justify-end">
                <Button variant="outline" onClick={handleCancel}>
                  Cancel
                </Button>
                <Button
                  onClick={handleConfirm}
                  disabled={!reason.trim() || setModeMutation.isPending}
                >
                  {setModeMutation.isPending ? "Changing..." : "Confirm Change"}
                </Button>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default GovernanceModeToggle;
