/**
 * SOP Hooks - Next.js App Router
 * @module frontend/landing/src/hooks/useSOP
 * @status Sprint 67 - SOP Migration
 * @description TanStack Query hooks for SOP management
 * @note Uses httpOnly cookies for auth (Sprint 63 migration)
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "@/hooks/useAuth";
import type {
  GenerateSOPRequest,
  GeneratedSOPResponse,
  SOPSummary,
  SOPDetail,
  SOPListResponse,
  SOPHistoryFilters,
  SOPStatus,
} from "@/lib/types/sop";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Fetch helper with httpOnly cookie auth
 * Sprint 63: Uses credentials: 'include' for httpOnly cookies
 */
async function fetchWithAuth<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    ...options,
    credentials: "include", // Include httpOnly cookies
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

// ============================================
// Query Keys
// ============================================

export const sopKeys = {
  all: ["sop"] as const,
  lists: () => [...sopKeys.all, "list"] as const,
  list: (filters: SOPHistoryFilters) => [...sopKeys.lists(), filters] as const,
  details: () => [...sopKeys.all, "detail"] as const,
  detail: (id: string) => [...sopKeys.details(), id] as const,
};

// ============================================
// Queries
// ============================================

/**
 * Get paginated SOP list
 */
export function useSOPList(filters: SOPHistoryFilters = {}) {
  const { isAuthenticated } = useAuth();

  return useQuery<SOPListResponse>({
    queryKey: sopKeys.list(filters),
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.sop_type) params.append("sop_type", filters.sop_type);
      if (filters.status) params.append("status", filters.status);
      if (filters.project_id) params.append("project_id", filters.project_id);
      if (filters.search) params.append("search", filters.search);
      if (filters.sort_by) params.append("sort_by", filters.sort_by);
      if (filters.sort_order) params.append("sort_order", filters.sort_order);
      if (filters.page) params.append("page", String(filters.page));
      if (filters.page_size) params.append("page_size", String(filters.page_size));

      const queryString = params.toString();
      return fetchWithAuth<SOPListResponse>(
        `/sop/list${queryString ? `?${queryString}` : ""}`
      );
    },
    enabled: isAuthenticated,
  });
}

/**
 * Get SOP detail by ID
 */
export function useSOPDetail(sopId: string | null) {
  const { isAuthenticated } = useAuth();

  return useQuery<SOPDetail>({
    queryKey: sopKeys.detail(sopId || ""),
    queryFn: async () => {
      if (!sopId) throw new Error("SOP ID required");
      return fetchWithAuth<SOPDetail>(`/sop/${sopId}`);
    },
    enabled: !!sopId && isAuthenticated,
  });
}

/**
 * Get recent SOPs for dashboard
 */
export function useRecentSOPs(limit: number = 5) {
  const { isAuthenticated } = useAuth();

  return useQuery<SOPSummary[]>({
    queryKey: [...sopKeys.lists(), "recent", limit],
    queryFn: async () => {
      const response = await fetchWithAuth<SOPListResponse>(
        `/sop/list?sort_by=created_at&sort_order=desc&page_size=${limit}`
      );
      return response.items;
    },
    enabled: isAuthenticated,
  });
}

// ============================================
// Mutations
// ============================================

/**
 * Generate new SOP
 */
export function useGenerateSOP() {
  const { isAuthenticated } = useAuth();
  const queryClient = useQueryClient();

  return useMutation<GeneratedSOPResponse, Error, GenerateSOPRequest>({
    mutationFn: async (request) => {
      if (!isAuthenticated) throw new Error("Not authenticated");
      return fetchWithAuth<GeneratedSOPResponse>("/sop/generate", {
        method: "POST",
        body: JSON.stringify(request),
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: sopKeys.lists() });
    },
  });
}

/**
 * Update SOP status
 */
export function useUpdateSOPStatus(sopId: string) {
  const { isAuthenticated } = useAuth();
  const queryClient = useQueryClient();

  return useMutation<SOPDetail, Error, { status: SOPStatus; comment?: string }>({
    mutationFn: async ({ status, comment }) => {
      if (!isAuthenticated) throw new Error("Not authenticated");
      return fetchWithAuth<SOPDetail>(`/sop/${sopId}/status`, {
        method: "PATCH",
        body: JSON.stringify({ status, comment }),
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: sopKeys.detail(sopId) });
      queryClient.invalidateQueries({ queryKey: sopKeys.lists() });
    },
  });
}

/**
 * Update SOP content
 */
export function useUpdateSOP(sopId: string) {
  const { isAuthenticated } = useAuth();
  const queryClient = useQueryClient();

  return useMutation<
    SOPDetail,
    Error,
    { markdown_content: string; change_summary: string }
  >({
    mutationFn: async ({ markdown_content, change_summary }) => {
      if (!isAuthenticated) throw new Error("Not authenticated");
      return fetchWithAuth<SOPDetail>(`/sop/${sopId}`, {
        method: "PUT",
        body: JSON.stringify({ markdown_content, change_summary }),
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: sopKeys.detail(sopId) });
      queryClient.invalidateQueries({ queryKey: sopKeys.lists() });
    },
  });
}

/**
 * Delete SOP
 */
export function useDeleteSOP() {
  const { isAuthenticated } = useAuth();
  const queryClient = useQueryClient();

  return useMutation<void, Error, string>({
    mutationFn: async (sopId) => {
      if (!isAuthenticated) throw new Error("Not authenticated");
      await fetchWithAuth(`/sop/${sopId}`, { method: "DELETE" });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: sopKeys.lists() });
    },
  });
}

/**
 * Attach evidence to SOP
 */
export function useAttachEvidence(sopId: string) {
  const { isAuthenticated } = useAuth();
  const queryClient = useQueryClient();

  return useMutation<
    SOPDetail,
    Error,
    { evidence_id: string; evidence_type: string }
  >({
    mutationFn: async ({ evidence_id, evidence_type }) => {
      if (!isAuthenticated) throw new Error("Not authenticated");
      return fetchWithAuth<SOPDetail>(`/sop/${sopId}/evidence`, {
        method: "POST",
        body: JSON.stringify({ evidence_id, evidence_type }),
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: sopKeys.detail(sopId) });
    },
  });
}

/**
 * Export SOP to different formats
 */
export function useExportSOP() {
  const { isAuthenticated } = useAuth();

  return useMutation<Blob, Error, { sopId: string; format: "pdf" | "docx" | "md" }>({
    mutationFn: async ({ sopId, format }) => {
      if (!isAuthenticated) throw new Error("Not authenticated");

      const response = await fetch(`${API_BASE}/sop/${sopId}/export?format=${format}`, {
        credentials: "include",
        headers: {
          Accept: format === "pdf" ? "application/pdf" : "application/octet-stream",
        },
      });

      if (!response.ok) {
        throw new Error(`Export failed: HTTP ${response.status}`);
      }

      return response.blob();
    },
  });
}

/**
 * Get SOP types for dropdown
 */
export function useSOPTypes() {
  return useQuery({
    queryKey: [...sopKeys.all, "types"],
    queryFn: async () => {
      return fetchWithAuth<Array<{ key: string; label: string; description: string }>>(
        "/sop/types"
      );
    },
    staleTime: 1000 * 60 * 60, // 1 hour (rarely changes)
  });
}
