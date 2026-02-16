/**
 * Codegen Page - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/app/app/codegen/page
 * @description EP-06 IR-Based Code Generation interface
 * @sdlc SDLC 6.0.6 Universal Framework
 * @status Sprint 69 - Zero Mock Policy Compliance
 */

"use client";

import { useState } from "react";
import {
  useCodegenTemplates,
  useCodegenSessions,
  useCreateCodegenSession,
} from "@/hooks/useCodegen";

// Icons
function CodeBracketIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
    </svg>
  );
}

function SparklesIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
    </svg>
  );
}

function CheckCircleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
    </svg>
  );
}

function XCircleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
    </svg>
  );
}

function ArrowPathIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
    </svg>
  );
}

function ClockIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
    </svg>
  );
}

function EyeIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
    </svg>
  );
}

// Status badge
function StatusBadge({ status }: { status: string }) {
  const config: Record<string, { bg: string; text: string; icon: React.ReactNode }> = {
    completed: {
      bg: "bg-green-100",
      text: "text-green-700",
      icon: <CheckCircleIcon className="h-4 w-4" />,
    },
    validating: {
      bg: "bg-yellow-100",
      text: "text-yellow-700",
      icon: <ArrowPathIcon className="h-4 w-4 animate-spin" />,
    },
    pending: {
      bg: "bg-gray-100",
      text: "text-gray-700",
      icon: <ClockIcon className="h-4 w-4" />,
    },
    failed: {
      bg: "bg-red-100",
      text: "text-red-700",
      icon: <XCircleIcon className="h-4 w-4" />,
    },
  };

  const { bg, text, icon } = config[status] || config.pending;

  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium ${bg} ${text}`}>
      {icon}
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
}

// Quality score
function QualityScore({ score }: { score: number | null }) {
  if (score === null) {
    return <span className="text-sm text-gray-400">—</span>;
  }

  const color =
    score >= 90 ? "text-green-600" : score >= 70 ? "text-yellow-600" : "text-red-600";

  return (
    <span className={`text-lg font-bold ${color}`}>
      {score}%
    </span>
  );
}

// Gate progress
function GateProgress({ passed, total }: { passed: number; total: number }) {
  const gates = ["Syntax", "Security", "Context", "Tests"];

  return (
    <div className="flex items-center gap-1">
      {gates.map((gate, index) => (
        <div
          key={gate}
          className={`h-2 w-6 rounded-full ${
            index < passed ? "bg-green-500" : "bg-gray-200"
          }`}
          title={`${gate}: ${index < passed ? "Passed" : "Pending"}`}
        />
      ))}
      <span className="ml-2 text-xs text-gray-500">
        {passed}/{total}
      </span>
    </div>
  );
}

// Loading skeleton
function LoadingSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="h-8 w-48 bg-gray-200 rounded" />
      <div className="grid gap-4 md:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-24 bg-gray-200 rounded-lg" />
        ))}
      </div>
      <div className="h-32 bg-gray-200 rounded-lg" />
      <div className="h-64 bg-gray-200 rounded-lg" />
    </div>
  );
}

// Error display
function ErrorDisplay({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-center">
      <XCircleIcon className="mx-auto h-12 w-12 text-red-400" />
      <h3 className="mt-2 text-lg font-medium text-red-800">Failed to load codegen data</h3>
      <p className="mt-1 text-sm text-red-600">{message}</p>
      <button
        onClick={onRetry}
        className="mt-4 rounded-md bg-red-100 px-4 py-2 text-sm font-medium text-red-700 hover:bg-red-200"
      >
        Retry
      </button>
    </div>
  );
}

// Empty state
function EmptyState() {
  return (
    <div className="rounded-lg border-2 border-dashed border-gray-200 p-12 text-center">
      <CodeBracketIcon className="mx-auto h-12 w-12 text-gray-400" />
      <h3 className="mt-2 text-lg font-medium text-gray-900">No generations yet</h3>
      <p className="mt-1 text-sm text-gray-500">
        Select a template above and click &quot;New Generation&quot; to get started
      </p>
    </div>
  );
}

export default function CodegenPage() {
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
  const [showNewModal, setShowNewModal] = useState(false);
  const [generationName, setGenerationName] = useState("");
  const [generationSpec, setGenerationSpec] = useState("");

  // TanStack Query hooks - Real API data
  const {
    data: templates,
    isLoading: templatesLoading,
    error: templatesError,
    refetch: refetchTemplates,
  } = useCodegenTemplates();

  const {
    data: sessionsData,
    isLoading: sessionsLoading,
    error: sessionsError,
    refetch: refetchSessions,
  } = useCodegenSessions({ page: 1, page_size: 20 });

  const createMutation = useCreateCodegenSession();

  const sessions = sessionsData?.sessions || [];

  // Calculate stats from real data
  const stats = {
    total: sessionsData?.total || 0,
    successRate: sessions.length > 0
      ? Math.round((sessions.filter(s => s.status === "completed").length / sessions.length) * 100)
      : 0,
    avgDuration: sessions.length > 0
      ? (sessions.reduce((sum, s) => sum + parseFloat(s.duration.replace("s", "") || "0"), 0) / sessions.length).toFixed(1)
      : "0",
    avgScore: sessions.filter(s => s.quality_score !== null).length > 0
      ? Math.round(
          sessions
            .filter(s => s.quality_score !== null)
            .reduce((sum, s) => sum + (s.quality_score || 0), 0) /
          sessions.filter(s => s.quality_score !== null).length
        )
      : 0,
  };

  const handleNewGeneration = () => {
    if (!selectedTemplate) {
      alert("Please select a template first");
      return;
    }
    setShowNewModal(true);
  };

  const handleSubmitGeneration = async () => {
    if (!generationName.trim()) {
      alert("Please enter a name");
      return;
    }

    try {
      await createMutation.mutateAsync({
        name: generationName,
        template_id: selectedTemplate!,
        specification: generationSpec || undefined,
      });

      setShowNewModal(false);
      setGenerationName("");
      setGenerationSpec("");

      // Refetch sessions to show new generation
      refetchSessions();
    } catch (error) {
      console.error("Failed to create generation:", error);
      alert("Failed to create generation. Please try again.");
    }
  };

  const isLoading = templatesLoading || sessionsLoading;
  const error = templatesError || sessionsError;

  if (isLoading) {
    return <LoadingSkeleton />;
  }

  if (error) {
    return (
      <ErrorDisplay
        message={error instanceof Error ? error.message : "Unknown error"}
        onRetry={() => {
          refetchTemplates();
          refetchSessions();
        }}
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Code Generation</h1>
          <p className="mt-1 text-gray-500">
            EP-06 IR-Based Codegen with 4-Gate Quality Pipeline
          </p>
        </div>
        <button
          onClick={handleNewGeneration}
          disabled={createMutation.isPending}
          className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          <SparklesIcon className="h-4 w-4" />
          {createMutation.isPending ? "Creating..." : "New Generation"}
        </button>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50">
              <CodeBracketIcon className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
              <p className="text-sm text-gray-500">Total Generations</p>
            </div>
          </div>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-50">
              <CheckCircleIcon className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.successRate}%</p>
              <p className="text-sm text-gray-500">Success Rate</p>
            </div>
          </div>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-50">
              <ClockIcon className="h-5 w-5 text-purple-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.avgDuration}s</p>
              <p className="text-sm text-gray-500">Avg Generation</p>
            </div>
          </div>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-50">
              <SparklesIcon className="h-5 w-5 text-orange-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.avgScore}%</p>
              <p className="text-sm text-gray-500">Avg Quality Score</p>
            </div>
          </div>
        </div>
      </div>

      {/* Templates */}
      <div>
        <h2 className="mb-3 text-lg font-semibold text-gray-900">Templates</h2>
        <div className="grid gap-3 md:grid-cols-4">
          {templates && templates.length > 0 ? (
            templates.map((template) => (
              <button
                key={template.id}
                onClick={() => setSelectedTemplate(template.id)}
                className={`rounded-lg border p-4 text-left transition-all hover:border-blue-300 hover:shadow-sm ${
                  selectedTemplate === template.id
                    ? "border-blue-500 bg-blue-50"
                    : "border-gray-200 bg-white"
                }`}
              >
                <p className="font-medium text-gray-900">{template.name}</p>
                <p className="mt-1 text-sm text-gray-500">{template.description}</p>
              </button>
            ))
          ) : (
            <p className="col-span-4 text-center text-gray-500 py-4">No templates available</p>
          )}
        </div>
      </div>

      {/* Recent generations */}
      <div>
        <h2 className="mb-3 text-lg font-semibold text-gray-900">Recent Generations</h2>
        {sessions.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="overflow-hidden rounded-lg border border-gray-200 bg-white">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                    Generation
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                    Template
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                    Quality Gates
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                    Score
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 bg-white">
                {sessions.map((session) => (
                  <tr key={session.id} className="hover:bg-gray-50">
                    <td className="whitespace-nowrap px-6 py-4">
                      <div>
                        <p className="font-medium text-gray-900">{session.name}</p>
                        <p className="text-xs text-gray-500">
                          {session.project} &bull; {session.duration}
                        </p>
                      </div>
                    </td>
                    <td className="whitespace-nowrap px-6 py-4">
                      <p className="text-sm text-gray-900">{session.template}</p>
                      <p className="text-xs text-gray-500">{session.provider}</p>
                    </td>
                    <td className="whitespace-nowrap px-6 py-4">
                      <StatusBadge status={session.status} />
                    </td>
                    <td className="whitespace-nowrap px-6 py-4">
                      <GateProgress
                        passed={session.gates_passed}
                        total={session.gates_total}
                      />
                    </td>
                    <td className="whitespace-nowrap px-6 py-4">
                      <QualityScore score={session.quality_score} />
                    </td>
                    <td className="whitespace-nowrap px-6 py-4 text-right">
                      <button className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600">
                        <EyeIcon className="h-5 w-5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* 4-Gate Pipeline visualization */}
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <h2 className="mb-4 text-lg font-semibold text-gray-900">4-Gate Quality Pipeline</h2>
        <div className="flex items-center justify-between">
          {[
            { name: "Gate 1: Syntax", desc: "ast.parse, ruff, tsc", time: "<5s" },
            { name: "Gate 2: Security", desc: "Semgrep SAST", time: "<10s" },
            { name: "Gate 3: Context", desc: "5 CTX checks", time: "<10s" },
            { name: "Gate 4: Tests", desc: "Dockerized pytest", time: "<60s" },
          ].map((gate, index) => (
            <div key={gate.name} className="flex items-center">
              <div className="flex flex-col items-center">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
                  <span className="text-lg font-bold text-blue-600">{index + 1}</span>
                </div>
                <p className="mt-2 text-sm font-medium text-gray-900">{gate.name}</p>
                <p className="text-xs text-gray-500">{gate.desc}</p>
                <p className="text-xs text-blue-600">{gate.time}</p>
              </div>
              {index < 3 && (
                <div className="mx-4 h-0.5 w-16 bg-gray-200" />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* New Generation Modal */}
      {showNewModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-lg rounded-lg bg-white p-6 shadow-xl">
            <h3 className="text-lg font-semibold text-gray-900">New Code Generation</h3>
            <p className="mt-1 text-sm text-gray-500">
              Template: {templates?.find(t => t.id === selectedTemplate)?.name || selectedTemplate}
            </p>

            <div className="mt-4 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Generation Name
                </label>
                <input
                  type="text"
                  value={generationName}
                  onChange={(e) => setGenerationName(e.target.value)}
                  placeholder="e.g., UserAuthService"
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Specification (optional)
                </label>
                <textarea
                  value={generationSpec}
                  onChange={(e) => setGenerationSpec(e.target.value)}
                  placeholder="Describe what you want to generate..."
                  rows={4}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>
            </div>

            <div className="mt-6 flex justify-end gap-3">
              <button
                onClick={() => setShowNewModal(false)}
                disabled={createMutation.isPending}
                className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={handleSubmitGeneration}
                disabled={createMutation.isPending}
                className="inline-flex items-center gap-2 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
              >
                {createMutation.isPending ? (
                  <>
                    <ArrowPathIcon className="h-4 w-4 animate-spin" />
                    Creating...
                  </>
                ) : (
                  <>
                    <SparklesIcon className="h-4 w-4" />
                    Generate Code
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
