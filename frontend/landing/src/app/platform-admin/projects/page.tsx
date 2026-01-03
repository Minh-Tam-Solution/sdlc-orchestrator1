/**
 * Projects Page - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/app/(dashboard)/projects/page
 * @description Project list and management page
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 62 - Route Group Migration (Real API)
 */

"use client";

import { useState } from "react";
import Link from "next/link";
import { useProjects, type Project } from "@/hooks/useProjects";

// Icons
function PlusIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
    </svg>
  );
}

function MagnifyingGlassIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
    </svg>
  );
}

function FunnelIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z" />
    </svg>
  );
}

function FolderIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
    </svg>
  );
}

function ChevronRightIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
    </svg>
  );
}

// Gate status badge with real API status
function GateStatusBadge({ status, stage }: { status: string; stage: string }) {
  const statusColors: Record<string, string> = {
    passed: "bg-green-100 text-green-700",
    failed: "bg-red-100 text-red-700",
    pending: "bg-yellow-100 text-yellow-700",
    not_started: "bg-gray-100 text-gray-700",
  };

  const stageLabels: Record<string, string> = {
    "00": "G0",
    "01": "G1",
    "02": "G2",
    "03": "G3",
    "04": "G4",
  };

  const gateLabel = stageLabels[stage] || `Stage ${stage}`;
  const colorClass = statusColors[status] || statusColors.not_started;

  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${colorClass}`}>
      {gateLabel}
    </span>
  );
}

// Progress bar component
function ProgressBar({ progress }: { progress: number }) {
  return (
    <div className="flex items-center gap-2">
      <div className="h-2 flex-1 rounded-full bg-gray-200">
        <div
          className="h-2 rounded-full bg-blue-600 transition-all"
          style={{ width: `${progress}%` }}
        />
      </div>
      <span className="text-xs text-gray-500">{progress}%</span>
    </div>
  );
}

// Format date helper
function formatDate(dateString: string | null): string {
  if (!dateString) return "N/A";
  return new Date(dateString).toLocaleDateString("vi-VN", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

// Project card component with real API data
function ProjectCard({ project }: { project: Project }) {
  return (
    <Link
      href={`/platform-admin/projects/${project.id}`}
      className="group block rounded-lg border border-gray-200 bg-white p-6 transition-all hover:border-blue-300 hover:shadow-md"
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50">
            <FolderIcon className="h-5 w-5 text-blue-600" />
          </div>
          <div>
            <h3 className="font-medium text-gray-900 group-hover:text-blue-600">
              {project.name}
            </h3>
            <p className="text-sm text-gray-500 line-clamp-1">
              {project.description || "No description"}
            </p>
          </div>
        </div>
        <ChevronRightIcon className="h-5 w-5 text-gray-400 group-hover:text-blue-600" />
      </div>

      <div className="mt-4 space-y-2">
        <div className="flex items-center gap-4">
          <GateStatusBadge status={project.gate_status} stage={project.current_stage} />
          <span className="text-sm text-gray-400">
            Updated {formatDate(project.updated_at)}
          </span>
        </div>
        <ProgressBar progress={project.progress} />
      </div>
    </Link>
  );
}

// Loading skeleton for project cards
function ProjectCardSkeleton() {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 animate-pulse">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-lg bg-gray-200" />
          <div className="space-y-2">
            <div className="h-4 w-32 rounded bg-gray-200" />
            <div className="h-3 w-48 rounded bg-gray-200" />
          </div>
        </div>
      </div>
      <div className="mt-4 space-y-2">
        <div className="flex items-center gap-4">
          <div className="h-5 w-12 rounded-full bg-gray-200" />
          <div className="h-3 w-24 rounded bg-gray-200" />
        </div>
        <div className="h-2 rounded-full bg-gray-200" />
      </div>
    </div>
  );
}

export default function ProjectsPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");

  // Fetch projects from API using TanStack Query
  const { data: projects, isLoading, error } = useProjects();

  // Filter projects based on search and status
  const filteredProjects = (projects || []).filter((project) => {
    const matchesSearch =
      project.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (project.description || "").toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus =
      statusFilter === "all" ||
      (statusFilter === "active" && project.gate_status !== "not_started") ||
      (statusFilter === "archived" && project.gate_status === "not_started");
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Projects</h1>
          <p className="mt-1 text-gray-500">
            Quản lý các dự án SDLC của bạn
          </p>
        </div>
        <button className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">
          <PlusIcon className="h-4 w-4" />
          New Project
        </button>
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        {/* Search */}
        <div className="relative flex-1 sm:max-w-sm">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Tìm kiếm dự án..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full rounded-lg border border-gray-300 py-2 pl-10 pr-4 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>

        {/* Status filter */}
        <div className="flex items-center gap-2">
          <FunnelIcon className="h-5 w-5 text-gray-400" />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="archived">Not Started</option>
          </select>
        </div>
      </div>

      {/* Error state */}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm text-red-700">
            Failed to load projects. Please try again later.
          </p>
        </div>
      )}

      {/* Loading state */}
      {isLoading && (
        <div className="grid gap-4 md:grid-cols-2">
          {[1, 2, 3, 4].map((i) => (
            <ProjectCardSkeleton key={i} />
          ))}
        </div>
      )}

      {/* Project grid */}
      {!isLoading && !error && filteredProjects.length > 0 && (
        <div className="grid gap-4 md:grid-cols-2">
          {filteredProjects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      )}

      {/* Empty state */}
      {!isLoading && !error && filteredProjects.length === 0 && (
        <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 p-12">
          <FolderIcon className="h-12 w-12 text-gray-400" />
          <h3 className="mt-4 text-lg font-medium text-gray-900">No projects found</h3>
          <p className="mt-1 text-gray-500">
            {searchQuery
              ? "Try adjusting your search query"
              : "Get started by creating a new project"}
          </p>
          <button className="mt-4 inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">
            <PlusIcon className="h-4 w-4" />
            New Project
          </button>
        </div>
      )}
    </div>
  );
}
