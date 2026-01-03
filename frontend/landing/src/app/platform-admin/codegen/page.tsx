/**
 * Codegen Page - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/app/platform-admin/codegen/page
 * @description EP-06 IR-Based Code Generation interface
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 61 - Frontend Platform Consolidation (Spike)
 */

"use client";

import { useState } from "react";

// Mock data for spike - will be replaced with TanStack Query
const mockCodegenSessions = [
  {
    id: "cg-001",
    name: "UserAuthService",
    project: "BFlow Platform",
    template: "FastAPI Service",
    status: "completed",
    quality_score: 94,
    provider: "Ollama (qwen3-coder:30b)",
    gates_passed: 4,
    gates_total: 4,
    created_at: "2025-12-28T11:30:00Z",
    duration: "12.3s",
  },
  {
    id: "cg-002",
    name: "ProductCatalogAPI",
    project: "MTEP Dashboard",
    template: "CRUD Endpoint",
    status: "validating",
    quality_score: null,
    provider: "Claude (claude-sonnet-4-5)",
    gates_passed: 2,
    gates_total: 4,
    created_at: "2025-12-28T10:45:00Z",
    duration: "8.7s",
  },
  {
    id: "cg-003",
    name: "NotificationWorker",
    project: "NQH-Bot",
    template: "Background Job",
    status: "failed",
    quality_score: 67,
    provider: "Ollama (qwen3-coder:30b)",
    gates_passed: 2,
    gates_total: 4,
    created_at: "2025-12-27T16:20:00Z",
    duration: "15.1s",
  },
  {
    id: "cg-004",
    name: "ReportGenerator",
    project: "SOP Generator",
    template: "Vietnamese Domain",
    status: "completed",
    quality_score: 98,
    provider: "Ollama (qwen3-coder:30b)",
    gates_passed: 4,
    gates_total: 4,
    created_at: "2025-12-27T14:10:00Z",
    duration: "9.8s",
  },
];

const templates = [
  { id: "fastapi", name: "FastAPI Service", description: "Full CRUD service with auth" },
  { id: "crud", name: "CRUD Endpoint", description: "Single resource endpoint" },
  { id: "worker", name: "Background Job", description: "Async task worker" },
  { id: "vietnam", name: "Vietnamese Domain", description: "E-commerce, HRM, CRM" },
];

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
    failed: {
      bg: "bg-red-100",
      text: "text-red-700",
      icon: <XCircleIcon className="h-4 w-4" />,
    },
  };

  const { bg, text, icon } = config[status] || config.validating;

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

export default function CodegenPage() {
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Code Generation</h1>
          <p className="mt-1 text-gray-500">
            EP-06 IR-Based Codegen với 4-Gate Quality Pipeline
          </p>
        </div>
        <button className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">
          <SparklesIcon className="h-4 w-4" />
          New Generation
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
              <p className="text-2xl font-bold text-gray-900">156</p>
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
              <p className="text-2xl font-bold text-gray-900">89%</p>
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
              <p className="text-2xl font-bold text-gray-900">11.2s</p>
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
              <p className="text-2xl font-bold text-gray-900">92%</p>
              <p className="text-sm text-gray-500">Avg Quality Score</p>
            </div>
          </div>
        </div>
      </div>

      {/* Templates */}
      <div>
        <h2 className="mb-3 text-lg font-semibold text-gray-900">Templates</h2>
        <div className="grid gap-3 md:grid-cols-4">
          {templates.map((template) => (
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
          ))}
        </div>
      </div>

      {/* Recent generations */}
      <div>
        <h2 className="mb-3 text-lg font-semibold text-gray-900">Recent Generations</h2>
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
              {mockCodegenSessions.map((session) => (
                <tr key={session.id} className="hover:bg-gray-50">
                  <td className="whitespace-nowrap px-6 py-4">
                    <div>
                      <p className="font-medium text-gray-900">{session.name}</p>
                      <p className="text-xs text-gray-500">
                        {session.project} • {session.duration}
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
    </div>
  );
}
