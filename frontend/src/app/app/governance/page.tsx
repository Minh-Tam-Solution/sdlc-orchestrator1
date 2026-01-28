/**
 * =========================================================================
 * Governance Dashboard Page
 * SDLC Orchestrator - Sprint 113 (Governance UI)
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Framework: SDLC 5.3.0 Quality Assurance System
 * ADR Reference: ADR-041
 *
 * Purpose: Main governance dashboard with auto-generation tools
 * =========================================================================
 */

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  IntentGeneratorCard,
  OwnershipSuggestionsCard,
  ContextAttachmentsCard,
  AttestationFormCard,
} from "@/components/governance";

// =============================================================================
// Icons
// =============================================================================

function ShieldCheckIcon({ className }: { className?: string }) {
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
        d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z"
      />
    </svg>
  );
}

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

function SparklesIcon({ className }: { className?: string }) {
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
        d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z"
      />
    </svg>
  );
}

function ArrowRightIcon({ className }: { className?: string }) {
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
        d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3"
      />
    </svg>
  );
}

// =============================================================================
// Page Component
// =============================================================================

export default function GovernancePage() {
  const router = useRouter();
  const [projectId] = useState("proj-001"); // TODO: Get from context
  const [repoId] = useState("repo-001"); // TODO: Get from context
  const [prNumber] = useState(123); // TODO: Get from URL params
  const [taskId] = useState("TASK-001"); // TODO: Get from task context
  const [submissionId] = useState("submission-001"); // TODO: Get from context

  // Sample data for demonstration
  const [taskTitle] = useState("Implement Governance Feature");
  const [taskDescription] = useState("Add governance compliance checks to the PR workflow");
  const [filePaths] = useState([
    "backend/app/services/governance/stage_gating.py",
    "backend/app/services/governance/signals_engine.py",
    "frontend/src/components/governance/index.ts",
  ]);
  const [changedFiles] = useState([
    "backend/app/services/governance/stage_gating.py",
    "backend/app/services/governance/signals_engine.py",
  ]);
  const [aiSessionId] = useState("ai-session-001");

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <ShieldCheckIcon className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Governance Dashboard
                </h1>
                <p className="text-sm text-gray-500">
                  Auto-generation tools to reduce compliance friction
                </p>
              </div>
            </div>
            <button
              onClick={() => router.push("/app/governance/kill-switch")}
              className="flex items-center gap-2 px-4 py-2 bg-amber-100 text-amber-700 rounded-lg hover:bg-amber-200 transition-colors"
            >
              <BoltIcon className="h-5 w-5" />
              Kill Switch Admin
              <ArrowRightIcon className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <SparklesIcon className="h-5 w-5" />
              <span className="font-medium">Auto-Generation Layer</span>
            </div>
            <div className="flex items-center gap-8 text-sm">
              <div>
                <span className="opacity-75">Target Friction:</span>
                <span className="ml-2 font-bold">&lt;5 min per PR</span>
              </div>
              <div>
                <span className="opacity-75">Previous:</span>
                <span className="ml-2 font-bold">~30 min per PR</span>
              </div>
              <div className="bg-white/20 px-3 py-1 rounded-full">
                <span className="font-bold">80%+ time savings</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Intent Generator */}
          <IntentGeneratorCard
            taskId={taskId}
            taskTitle={taskTitle}
            taskDescription={taskDescription}
            onIntentGenerated={(intent) => {
              console.log("Intent generated:", intent.content.slice(0, 100));
            }}
          />

          {/* Ownership Suggestions */}
          <OwnershipSuggestionsCard
            filePaths={filePaths}
            repoId={repoId}
            projectId={projectId}
            onOwnershipAccepted={(acceptedFiles) => {
              console.log("Ownership accepted for:", acceptedFiles);
            }}
          />

          {/* Context Attachments */}
          <ContextAttachmentsCard
            prNumber={prNumber}
            repoId={repoId}
            projectId={projectId}
            changedFiles={changedFiles}
            onContextAttached={(attachmentIds) => {
              console.log("Attached:", attachmentIds);
            }}
          />

          {/* Attestation Form */}
          <AttestationFormCard
            submissionId={submissionId}
            aiSessionId={aiSessionId}
            prNumber={prNumber}
            filePaths={filePaths}
            onAttestationSubmitted={(attestation) => {
              console.log("Attestation submitted:", attestation.id);
            }}
          />
        </div>

        {/* Quick Stats */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg border p-4">
            <div className="text-sm text-gray-500">Intents Auto-Generated</div>
            <div className="text-2xl font-bold text-gray-900">142</div>
            <div className="text-xs text-green-600">+12 this week</div>
          </div>
          <div className="bg-white rounded-lg border p-4">
            <div className="text-sm text-gray-500">Ownership Suggestions</div>
            <div className="text-2xl font-bold text-gray-900">89%</div>
            <div className="text-xs text-green-600">acceptance rate</div>
          </div>
          <div className="bg-white rounded-lg border p-4">
            <div className="text-sm text-gray-500">Context Attachments</div>
            <div className="text-2xl font-bold text-gray-900">256</div>
            <div className="text-xs text-green-600">auto-attached</div>
          </div>
          <div className="bg-white rounded-lg border p-4">
            <div className="text-sm text-gray-500">AI Attestations</div>
            <div className="text-2xl font-bold text-gray-900">98</div>
            <div className="text-xs text-green-600">compliant</div>
          </div>
        </div>
      </main>
    </div>
  );
}
