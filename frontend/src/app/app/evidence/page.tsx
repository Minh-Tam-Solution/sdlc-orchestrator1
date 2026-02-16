/**
 * Evidence Vault Page - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/app/app/evidence/page
 * @description Evidence management and audit trail
 * @sdlc SDLC 6.0.6 Universal Framework
 * @status Sprint 62 - Route Group Migration (Real API)
 */

"use client";

import { useState, useMemo, useRef, useCallback } from "react";
import { useEvidenceList, useUploadEvidence, useDownloadEvidence, type Evidence } from "@/hooks/useEvidence";
import { useGates } from "@/hooks/useGates";

// Evidence type options for filter
const evidenceTypes = [
  { value: "all", label: "All Types" },
  { value: "DESIGN_DOCUMENT", label: "Design Documents" },
  { value: "TEST_RESULTS", label: "Test Results" },
  { value: "CODE_REVIEW", label: "Code Reviews" },
  { value: "DEPLOYMENT_PROOF", label: "Deployment Proofs" },
  { value: "DOCUMENTATION", label: "Documentation" },
  { value: "COMPLIANCE", label: "Compliance" },
];

// Icons
function DocumentIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
    </svg>
  );
}

function ArrowUpTrayIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
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

function ShieldCheckIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z" />
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

function ArrowDownTrayIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
    </svg>
  );
}

function XMarkIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
    </svg>
  );
}

function SpinnerIcon({ className }: { className?: string }) {
  return (
    <svg className={`animate-spin ${className}`} fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
    </svg>
  );
}

// Integrity status badge
function IntegrityBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    valid: "bg-green-100 text-green-700",
    pending: "bg-yellow-100 text-yellow-700",
    failed: "bg-red-100 text-red-700",
  };

  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${styles[status] || styles.pending}`}>
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
}

// Evidence type badge
function TypeBadge({ type }: { type: string }) {
  const styles: Record<string, string> = {
    DESIGN_DOCUMENT: "bg-purple-100 text-purple-700",
    TEST_RESULTS: "bg-cyan-100 text-cyan-700",
    CODE_REVIEW: "bg-blue-100 text-blue-700",
    DEPLOYMENT_PROOF: "bg-green-100 text-green-700",
    DOCUMENTATION: "bg-indigo-100 text-indigo-700",
    COMPLIANCE: "bg-orange-100 text-orange-700",
  };

  const labels: Record<string, string> = {
    DESIGN_DOCUMENT: "Design",
    TEST_RESULTS: "Test",
    CODE_REVIEW: "Review",
    DEPLOYMENT_PROOF: "Deploy",
    DOCUMENTATION: "Docs",
    COMPLIANCE: "Compliance",
  };

  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${styles[type] || "bg-gray-100 text-gray-700"}`}>
      {labels[type] || type}
    </span>
  );
}

// Format date
function formatDate(dateString: string | null): string {
  if (!dateString) return "N/A";
  return new Date(dateString).toLocaleDateString("vi-VN", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// Format file size
function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

// Loading skeleton for table rows
function TableRowSkeleton() {
  return (
    <tr className="animate-pulse">
      <td className="whitespace-nowrap px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded bg-gray-200" />
          <div className="space-y-1">
            <div className="h-4 w-32 rounded bg-gray-200" />
            <div className="h-3 w-16 rounded bg-gray-200" />
          </div>
        </div>
      </td>
      <td className="whitespace-nowrap px-6 py-4">
        <div className="h-5 w-16 rounded-full bg-gray-200" />
      </td>
      <td className="whitespace-nowrap px-6 py-4">
        <div className="h-5 w-12 rounded-full bg-gray-200" />
      </td>
      <td className="whitespace-nowrap px-6 py-4">
        <div className="space-y-1">
          <div className="h-4 w-24 rounded bg-gray-200" />
          <div className="h-3 w-20 rounded bg-gray-200" />
        </div>
      </td>
      <td className="whitespace-nowrap px-6 py-4 text-right">
        <div className="flex items-center justify-end gap-2">
          <div className="h-8 w-8 rounded bg-gray-200" />
          <div className="h-8 w-8 rounded bg-gray-200" />
        </div>
      </td>
    </tr>
  );
}

export default function EvidencePage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [selectedEvidence, setSelectedEvidence] = useState<Evidence | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadType, setUploadType] = useState("DOCUMENTATION");
  const [selectedGateId, setSelectedGateId] = useState("");
  const [description, setDescription] = useState("");
  const [uploadError, setUploadError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Fetch gates for the dropdown
  const { data: gatesResponse } = useGates({ page_size: 100 });

  // Fetch evidence from API using TanStack Query
  const { data: evidenceResponse, isLoading, error, refetch } = useEvidenceList({
    evidence_type: typeFilter !== "all" ? typeFilter : undefined,
    page_size: 100,
  });

  // Upload mutation
  const uploadMutation = useUploadEvidence();

  // Download mutation
  const downloadMutation = useDownloadEvidence();

  // Handle download
  const handleDownload = useCallback((evidenceId: string) => {
    downloadMutation.mutate(evidenceId);
  }, [downloadMutation]);

  // Handle file selection
  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Check file size (max 50MB)
      if (file.size > 50 * 1024 * 1024) {
        setUploadError("File size must be less than 50MB");
        return;
      }
      setSelectedFile(file);
      setUploadError(null);
    }
  }, []);

  // Handle upload
  const handleUpload = useCallback(async () => {
    if (!selectedFile) {
      setUploadError("Please select a file");
      return;
    }

    if (!selectedGateId) {
      setUploadError("Please select a gate");
      return;
    }

    try {
      setUploadError(null);
      await uploadMutation.mutateAsync({
        data: {
          gate_id: selectedGateId,
          evidence_type: uploadType,
          description: description || selectedFile.name,
        },
        file: selectedFile,
      });

      // Success - close modal and reset
      setIsUploadModalOpen(false);
      setSelectedFile(null);
      setDescription("");
      setUploadType("DOCUMENTATION");
      setSelectedGateId("");
      refetch();
    } catch (err) {
      setUploadError(err instanceof Error ? err.message : "Upload failed. Please try again.");
    }
  }, [selectedFile, selectedGateId, uploadType, description, uploadMutation, refetch]);

  // Reset modal state
  const handleCloseModal = useCallback(() => {
    setIsUploadModalOpen(false);
    setSelectedFile(null);
    setDescription("");
    setUploadError(null);
    setUploadType("DOCUMENTATION");
    setSelectedGateId("");
  }, []);

  // Calculate stats from real data
  const stats = useMemo(() => {
    const items = evidenceResponse?.items || [];
    const total = evidenceResponse?.total || 0;
    const valid = items.filter((e) => e.integrity_status === "valid").length;
    const pending = items.filter((e) => e.integrity_status === "pending").length;
    const failed = items.filter((e) => e.integrity_status === "failed").length;
    return { total, valid, pending, failed };
  }, [evidenceResponse]);

  // Filter evidence based on search
  const filteredEvidence = useMemo(() => {
    const items = evidenceResponse?.items || [];
    if (!searchQuery) return items;
    return items.filter(
      (item) =>
        item.file_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.uploaded_by_name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [evidenceResponse, searchQuery]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Evidence Vault</h1>
          <p className="mt-1 text-gray-500">
            Quản lý và theo dõi bằng chứng cho các gate
          </p>
        </div>
        <button
          onClick={() => setIsUploadModalOpen(true)}
          className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          <ArrowUpTrayIcon className="h-4 w-4" />
          Upload Evidence
        </button>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50">
              <DocumentIcon className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
              <p className="text-sm text-gray-500">Total Evidence</p>
            </div>
          </div>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-50">
              <ShieldCheckIcon className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.valid}</p>
              <p className="text-sm text-gray-500">Verified</p>
            </div>
          </div>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-yellow-50">
              <DocumentIcon className="h-5 w-5 text-yellow-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.pending}</p>
              <p className="text-sm text-gray-500">Pending Check</p>
            </div>
          </div>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-red-50">
              <DocumentIcon className="h-5 w-5 text-red-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.failed}</p>
              <p className="text-sm text-gray-500">Failed Integrity</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        {/* Search */}
        <div className="relative flex-1 sm:max-w-sm">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Tìm kiếm evidence..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full rounded-lg border border-gray-300 py-2 pl-10 pr-4 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>

        {/* Type filter */}
        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          {evidenceTypes.map((type) => (
            <option key={type.value} value={type.value}>
              {type.label}
            </option>
          ))}
        </select>
      </div>

      {/* Error state */}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm text-red-700">
            Failed to load evidence. Please try again later.
          </p>
        </div>
      )}

      {/* Evidence table */}
      <div className="overflow-hidden rounded-lg border border-gray-200 bg-white">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                Evidence
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                Type
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                Integrity
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                Uploaded
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 bg-white">
            {/* Loading state */}
            {isLoading && (
              <>
                <TableRowSkeleton />
                <TableRowSkeleton />
                <TableRowSkeleton />
                <TableRowSkeleton />
              </>
            )}

            {/* Data rows */}
            {!isLoading &&
              filteredEvidence.map((item: Evidence) => (
                <tr key={item.id} className="hover:bg-gray-50">
                  <td className="whitespace-nowrap px-6 py-4">
                    <div className="flex items-center gap-3">
                      <DocumentIcon className="h-8 w-8 text-gray-400" />
                      <div>
                        <p className="font-medium text-gray-900 max-w-xs truncate">
                          {item.file_name}
                        </p>
                        <p className="text-xs text-gray-500">
                          {formatFileSize(item.file_size)}
                        </p>
                      </div>
                    </div>
                  </td>
                  <td className="whitespace-nowrap px-6 py-4">
                    <TypeBadge type={item.evidence_type} />
                  </td>
                  <td className="whitespace-nowrap px-6 py-4">
                    <IntegrityBadge status={item.integrity_status} />
                  </td>
                  <td className="whitespace-nowrap px-6 py-4">
                    <p className="text-sm text-gray-900">{item.uploaded_by_name}</p>
                    <p className="text-xs text-gray-500">{formatDate(item.uploaded_at)}</p>
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => setSelectedEvidence(item)}
                        className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
                        title="View details"
                      >
                        <EyeIcon className="h-5 w-5" />
                      </button>
                      <button
                        onClick={() => handleDownload(item.id)}
                        disabled={downloadMutation.isPending}
                        className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600 disabled:opacity-50"
                        title="Download"
                      >
                        <ArrowDownTrayIcon className="h-5 w-5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      {/* Empty state */}
      {!isLoading && !error && filteredEvidence.length === 0 && (
        <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 p-12">
          <DocumentIcon className="h-12 w-12 text-gray-400" />
          <h3 className="mt-4 text-lg font-medium text-gray-900">No evidence found</h3>
          <p className="mt-1 text-gray-500">
            {searchQuery
              ? "Try adjusting your search query"
              : "Upload evidence to get started"}
          </p>
        </div>
      )}

      {/* Upload Modal */}
      {isUploadModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
            {/* Modal Header */}
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Upload Evidence</h2>
              <button
                onClick={handleCloseModal}
                className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
              >
                <XMarkIcon className="h-5 w-5" />
              </button>
            </div>

            {/* Error Message */}
            {uploadError && (
              <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-3">
                <p className="text-sm text-red-700">{uploadError}</p>
              </div>
            )}

            {/* File Input */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select File
              </label>
              <input
                ref={fileInputRef}
                type="file"
                onChange={handleFileSelect}
                className="hidden"
                accept=".pdf,.doc,.docx,.xls,.xlsx,.png,.jpg,.jpeg,.txt,.md,.json,.yaml,.yml"
              />
              <button
                onClick={() => fileInputRef.current?.click()}
                className="w-full rounded-lg border-2 border-dashed border-gray-300 p-4 text-center hover:border-blue-500 hover:bg-blue-50 transition-colors"
              >
                {selectedFile ? (
                  <div className="flex items-center justify-center gap-2">
                    <DocumentIcon className="h-6 w-6 text-blue-600" />
                    <span className="text-sm font-medium text-gray-900 truncate max-w-xs">
                      {selectedFile.name}
                    </span>
                    <span className="text-xs text-gray-500">
                      ({formatFileSize(selectedFile.size)})
                    </span>
                  </div>
                ) : (
                  <div>
                    <ArrowUpTrayIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-600">Click to select file</p>
                    <p className="text-xs text-gray-400 mt-1">Max 50MB</p>
                  </div>
                )}
              </button>
            </div>

            {/* Gate Selector */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Gate <span className="text-red-500">*</span>
              </label>
              <select
                value={selectedGateId}
                onChange={(e) => setSelectedGateId(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option value="">-- Select a gate --</option>
                {gatesResponse?.items?.map((gate) => (
                  <option key={gate.id} value={gate.id}>
                    {gate.gate_name} ({gate.stage})
                  </option>
                ))}
              </select>
            </div>

            {/* Evidence Type */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Evidence Type
              </label>
              <select
                value={uploadType}
                onChange={(e) => setUploadType(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                {evidenceTypes.filter(t => t.value !== "all").map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Description */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description (optional)
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Add a description for this evidence..."
                rows={3}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>

            {/* Actions */}
            <div className="flex gap-3">
              <button
                onClick={handleCloseModal}
                className="flex-1 rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleUpload}
                disabled={!selectedFile || uploadMutation.isPending}
                className="flex-1 inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {uploadMutation.isPending ? (
                  <>
                    <SpinnerIcon className="h-4 w-4" />
                    Uploading...
                  </>
                ) : (
                  <>
                    <ArrowUpTrayIcon className="h-4 w-4" />
                    Upload
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Evidence Detail Modal */}
      {selectedEvidence && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-lg rounded-lg bg-white p-6 shadow-xl">
            {/* Modal Header */}
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Evidence Details</h2>
              <button
                onClick={() => setSelectedEvidence(null)}
                className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
              >
                <XMarkIcon className="h-5 w-5" />
              </button>
            </div>

            {/* Evidence Info */}
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-500">File Name</label>
                <p className="mt-1 text-sm text-gray-900">{selectedEvidence.file_name}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-500">Evidence Type</label>
                  <p className="mt-1 text-sm text-gray-900">{selectedEvidence.evidence_type}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-500">File Size</label>
                  <p className="mt-1 text-sm text-gray-900">{formatFileSize(selectedEvidence.file_size)}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-500">Gate ID</label>
                  <p className="mt-1 text-sm text-gray-900 font-mono text-xs">{selectedEvidence.gate_id}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-500">Integrity Status</label>
                  <p className="mt-1">
                    <IntegrityBadge status={selectedEvidence.integrity_status} />
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-500">Uploaded By</label>
                  <p className="mt-1 text-sm text-gray-900">{selectedEvidence.uploaded_by_name}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-500">Uploaded At</label>
                  <p className="mt-1 text-sm text-gray-900">{formatDate(selectedEvidence.uploaded_at)}</p>
                </div>
              </div>

              {selectedEvidence.description && (
                <div>
                  <label className="block text-sm font-medium text-gray-500">Description</label>
                  <p className="mt-1 text-sm text-gray-900">{selectedEvidence.description}</p>
                </div>
              )}

              {selectedEvidence.sha256_hash && (
                <div>
                  <label className="block text-sm font-medium text-gray-500">SHA256 Hash</label>
                  <p className="mt-1 text-xs font-mono text-gray-600 break-all bg-gray-50 p-2 rounded">
                    {selectedEvidence.sha256_hash}
                  </p>
                </div>
              )}
            </div>

            {/* Actions */}
            <div className="mt-6 flex gap-3">
              <button
                onClick={() => setSelectedEvidence(null)}
                className="flex-1 rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Close
              </button>
              <button
                onClick={() => {
                  handleDownload(selectedEvidence.id);
                  setSelectedEvidence(null);
                }}
                disabled={downloadMutation.isPending}
                className="flex-1 inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
              >
                <ArrowDownTrayIcon className="h-4 w-4" />
                Download
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
