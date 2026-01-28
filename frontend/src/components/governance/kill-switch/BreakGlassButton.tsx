/**
 * =========================================================================
 * Break Glass Button Component
 * SDLC Orchestrator - Sprint 113 (Governance UI - Kill Switch Admin)
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Framework: SDLC 5.3.0 Quality Assurance System
 * ADR Reference: ADR-041
 *
 * Purpose: Emergency governance bypass for P0/P1 incidents
 * =========================================================================
 */

"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import {
  useCreateBreakGlass,
  useBreakGlassAuthorization,
  useBreakGlassRequests,
} from "@/hooks/useKillSwitch";
import type { BreakGlassRequest } from "@/lib/types/kill-switch";

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

// =============================================================================
// Types
// =============================================================================

type IncidentType = "p0" | "p1" | "hotfix" | "other";

interface IncidentOption {
  value: IncidentType;
  label: string;
  description: string;
}

const INCIDENT_OPTIONS: IncidentOption[] = [
  { value: "p0", label: "P0 - Critical", description: "System down, revenue impact" },
  { value: "p1", label: "P1 - High", description: "Major functionality broken" },
  { value: "hotfix", label: "Hotfix", description: "Urgent security/bug patch" },
  { value: "other", label: "Other", description: "Custom emergency reason" },
];

// =============================================================================
// Component
// =============================================================================

interface BreakGlassButtonProps {
  onBreakGlassCreated?: (request: BreakGlassRequest) => void;
  variant?: "default" | "compact";
}

export function BreakGlassButton({
  onBreakGlassCreated,
  variant = "default",
}: BreakGlassButtonProps) {
  const [showModal, setShowModal] = useState(false);
  const [reason, setReason] = useState("");
  const [incidentType, setIncidentType] = useState<IncidentType>("p0");
  const [prNumber, setPrNumber] = useState("");

  const authTier = useBreakGlassAuthorization();
  const createMutation = useCreateBreakGlass();
  const { data: pendingRequests } = useBreakGlassRequests({ status: "pending", limit: 1 });

  const hasPendingRequest = pendingRequests && pendingRequests.length > 0;
  const canRequest = authTier !== null;

  const handleSubmit = async () => {
    if (!reason.trim()) return;

    try {
      const response = await createMutation.mutateAsync({
        reason: reason.trim(),
        pr_number: prNumber ? parseInt(prNumber, 10) : undefined,
        incident_type: incidentType,
      });

      onBreakGlassCreated?.(response.request);
      setShowModal(false);
      setReason("");
      setPrNumber("");
    } catch {
      // Error handled by mutation
    }
  };

  const handleCancel = () => {
    setShowModal(false);
    setReason("");
    setPrNumber("");
  };

  // Compact variant for sidebar/header
  if (variant === "compact") {
    return (
      <>
        <Button
          variant="destructive"
          size="sm"
          onClick={() => setShowModal(true)}
          disabled={!canRequest || hasPendingRequest}
          className="gap-2"
        >
          <ShieldExclamationIcon className="h-4 w-4" />
          Break Glass
        </Button>

        {showModal && (
          <BreakGlassModal
            reason={reason}
            setReason={setReason}
            incidentType={incidentType}
            setIncidentType={setIncidentType}
            prNumber={prNumber}
            setPrNumber={setPrNumber}
            authTier={authTier}
            isPending={createMutation.isPending}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
          />
        )}
      </>
    );
  }

  // Default full-size variant
  return (
    <div className="relative">
      {/* Break Glass Button */}
      <Button
        variant="destructive"
        size="lg"
        onClick={() => setShowModal(true)}
        disabled={!canRequest || hasPendingRequest}
        className="w-full h-16 gap-3 text-lg font-semibold shadow-lg"
      >
        <ShieldExclamationIcon className="h-6 w-6" />
        <span>Emergency: Break Glass</span>
      </Button>

      {/* Pending Request Indicator */}
      {hasPendingRequest && (
        <div className="absolute -top-2 -right-2">
          <Badge className="bg-amber-500 text-white animate-pulse">
            Pending
          </Badge>
        </div>
      )}

      {/* Authorization Info */}
      <div className="mt-2 text-center text-xs text-gray-500">
        {canRequest ? (
          <span>Authorized as {authTier?.toUpperCase()}</span>
        ) : (
          <span>Requires Tech Lead / CTO / CEO authorization</span>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <BreakGlassModal
          reason={reason}
          setReason={setReason}
          incidentType={incidentType}
          setIncidentType={setIncidentType}
          prNumber={prNumber}
          setPrNumber={setPrNumber}
          authTier={authTier}
          isPending={createMutation.isPending}
          onSubmit={handleSubmit}
          onCancel={handleCancel}
        />
      )}
    </div>
  );
}

// =============================================================================
// Break Glass Modal
// =============================================================================

interface BreakGlassModalProps {
  reason: string;
  setReason: (reason: string) => void;
  incidentType: IncidentType;
  setIncidentType: (type: IncidentType) => void;
  prNumber: string;
  setPrNumber: (pr: string) => void;
  authTier: "tech_lead" | "cto" | "ceo" | null;
  isPending: boolean;
  onSubmit: () => void;
  onCancel: () => void;
}

function BreakGlassModal({
  reason,
  setReason,
  incidentType,
  setIncidentType,
  prNumber,
  setPrNumber,
  authTier,
  isPending,
  onSubmit,
  onCancel,
}: BreakGlassModalProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-lg w-full mx-4">
        {/* Header */}
        <div className="flex items-center gap-3 mb-4">
          <div className="h-10 w-10 rounded-full bg-red-100 flex items-center justify-center">
            <ExclamationTriangleIcon className="h-6 w-6 text-red-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-red-900">
              Break Glass Request
            </h3>
            <p className="text-sm text-gray-600">
              Emergency bypass of governance controls
            </p>
          </div>
        </div>

        {/* Warning */}
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
          <div className="flex items-start gap-2">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-600 mt-0.5" />
            <div className="text-sm text-red-700">
              <p className="font-medium">This action will:</p>
              <ul className="list-disc list-inside mt-1 space-y-0.5">
                <li>Immediately disable governance checks</li>
                <li>Notify CTO and CEO via Slack</li>
                <li>Create permanent audit log entry</li>
                <li>Auto-revert after 4 hours if not renewed</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Form */}
        <div className="space-y-4">
          {/* Incident Type */}
          <div>
            <Label className="block mb-2">Incident Type</Label>
            <div className="grid grid-cols-2 gap-2">
              {INCIDENT_OPTIONS.map((option) => (
                <button
                  key={option.value}
                  onClick={() => setIncidentType(option.value)}
                  className={`p-3 border rounded-lg text-left transition-colors ${
                    incidentType === option.value
                      ? "border-red-500 bg-red-50"
                      : "border-gray-200 hover:border-gray-300"
                  }`}
                >
                  <div className="font-medium text-sm">{option.label}</div>
                  <div className="text-xs text-gray-500">{option.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Reason */}
          <div>
            <Label htmlFor="break-glass-reason">
              Reason for Emergency Bypass *
            </Label>
            <Textarea
              id="break-glass-reason"
              placeholder="Describe the incident requiring governance bypass..."
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              className="mt-1"
              rows={3}
            />
          </div>

          {/* PR Number (optional) */}
          <div>
            <Label htmlFor="pr-number">Related PR Number (optional)</Label>
            <input
              id="pr-number"
              type="text"
              placeholder="e.g., 1234"
              value={prNumber}
              onChange={(e) => setPrNumber(e.target.value.replace(/\D/g, ""))}
              className="mt-1 w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-500"
            />
          </div>

          {/* Authorization Display */}
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <ClockIcon className="h-4 w-4" />
            <span>
              Authorization tier: <strong className="capitalize">{authTier}</strong>
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-2 justify-end mt-6">
          <Button variant="outline" onClick={onCancel}>
            Cancel
          </Button>
          <Button
            variant="destructive"
            onClick={onSubmit}
            disabled={!reason.trim() || isPending}
          >
            {isPending ? (
              <>
                <span className="animate-spin mr-2">...</span>
                Creating...
              </>
            ) : (
              <>
                <ShieldExclamationIcon className="h-4 w-4 mr-2" />
                Confirm Break Glass
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}

export default BreakGlassButton;
