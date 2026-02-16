/**
 * Gate Detail Page - Next.js App Router
 * @module frontend/landing/src/app/app/gates/[id]/page
 * @status Sprint 64 - Route Group Migration
 * @description Gate detail with approval workflow, exit criteria, and evidence
 */
"use client";

import { use, useState, useRef, useCallback } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useQueryClient, useMutation } from "@tanstack/react-query";
import { useGate, gateKeys } from "@/hooks/useGates";
import { useUploadEvidence } from "@/hooks/useEvidence";
import { useAuth } from "@/hooks/useAuth";
import { approveGate as apiApproveGate, submitGate as apiSubmitGate } from "@/lib/api";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

/**
 * SDLC 6.0.6 Stage Definitions (10 Stages: 00-09)
 */
const SDLC_STAGES = [
  { code: "00", name: "FOUNDATION", description: "Strategic Discovery & Validation" },
  { code: "01", name: "PLANNING", description: "Requirements & User Stories" },
  { code: "02", name: "DESIGN", description: "Architecture & Technical Design" },
  { code: "03", name: "INTEGRATE", description: "API Contracts & Third-party Setup" },
  { code: "04", name: "BUILD", description: "Development & Implementation" },
  { code: "05", name: "TEST", description: "Quality Assurance & Validation" },
  { code: "06", name: "DEPLOY", description: "Release & Deployment" },
  { code: "07", name: "OPERATE", description: "Production Operations & Monitoring" },
  { code: "08", name: "COLLABORATE", description: "Team Coordination & Knowledge" },
  { code: "09", name: "GOVERN", description: "Compliance & Strategic Oversight" },
];

/**
 * Get status badge styling
 */
function getStatusStyle(status: string): string {
  switch (status) {
    case "APPROVED":
      return "bg-green-100 text-green-700 border-green-200";
    case "REJECTED":
      return "bg-red-100 text-red-700 border-red-200";
    case "PENDING_APPROVAL":
      return "bg-yellow-100 text-yellow-700 border-yellow-200";
    case "DRAFT":
      return "bg-blue-100 text-blue-700 border-blue-200";
    default:
      return "bg-gray-100 text-gray-700 border-gray-200";
  }
}

interface PageProps {
  params: { id: string } | Promise<{ id: string }>;
}

export default function GateDetailPage({ params }: PageProps) {
  // Handle both sync and async params (Next.js 14 compatibility)
  const resolvedParams = params instanceof Promise ? use(params) : params;
  const { id } = resolvedParams;
  const router = useRouter();
  const queryClient = useQueryClient();
  const { user } = useAuth();
  const { data: gate, isLoading, error } = useGate(id);

  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editForm, setEditForm] = useState({
    gate_name: "",
    description: "",
    stage: "",
  });

  // Upload evidence state
  const [uploadModalOpen, setUploadModalOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadType, setUploadType] = useState("DOCUMENTATION");
  const [uploadDescription, setUploadDescription] = useState("");
  const [uploadError, setUploadError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Upload mutation
  const uploadMutation = useUploadEvidence();

  // Submit gate for approval - uses apiSubmitGate with auto-refresh token (Sprint 136)
  const submitMutation = useMutation({
    mutationFn: async () => {
      console.log("[Gate Submit] Starting submit request:", { gateId: id });
      const result = await apiSubmitGate(id as string, { message: "Submitting for approval" });
      console.log("[Gate Submit] Success:", result);
      return result;
    },
    onSuccess: (data) => {
      queryClient.setQueryData(gateKeys.detail(id as string), data);
      queryClient.invalidateQueries({ queryKey: gateKeys.lists() });
    },
    onError: (error: Error) => {
      console.error("[Gate Submit] Mutation error:", error);
      if (typeof window !== "undefined") {
        alert(`Error: ${error.message}`);
      }
    },
  });

  // Approve/reject gate - uses apiApproveGate with auto-refresh token (Sprint 136)
  const approveMutation = useMutation({
    mutationFn: async (approved: boolean) => {
      console.log("[Gate Approval] Starting approval request:", { gateId: id, approved });
      // Use API function with auto-refresh token support
      const result = await apiApproveGate(id as string, {
        approved,
        comments: approved ? "Approved" : "Rejected",
      });
      console.log("[Gate Approval] Success:", result);
      return result;
    },
    onSuccess: (data) => {
      console.log("[Gate Approval] Mutation success, updating cache with:", data);
      // Directly update cache with returned data (immediate UI update)
      queryClient.setQueryData(gateKeys.detail(id as string), data);
      // Also invalidate to ensure fresh data on next fetch
      queryClient.invalidateQueries({ queryKey: gateKeys.lists() });
      queryClient.invalidateQueries({ queryKey: gateKeys.detail(id as string) });
      // Show success toast
      if (typeof window !== "undefined") {
        alert(data.status === "APPROVED" ? "Gate approved successfully!" : "Gate rejected");
      }
    },
    onError: (error: Error) => {
      console.error("[Gate Approval] Mutation error:", error);
      // Show error to user
      if (typeof window !== "undefined") {
        alert(`Error: ${error.message}`);
      }
    },
  });

  // Delete gate
  const deleteMutation = useMutation({
    mutationFn: async () => {
      const token = localStorage.getItem("access_token");
      if (!token) throw new Error("Not authenticated");

      const response = await fetch(`${API_BASE_URL}/gates/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        credentials: "include",
      });
      if (!response.ok) throw new Error("Failed to delete gate");
    },
    onSuccess: () => {
      router.push("/app/gates");
    },
  });

  // Update gate
  const updateMutation = useMutation({
    mutationFn: async (data: { gate_name: string; description: string; stage: string }) => {
      const response = await fetch(`${API_BASE_URL}/gates/${id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Failed to update gate" }));
        throw new Error(error.detail || "Failed to update gate");
      }
      return response.json();
    },
    onSuccess: (data) => {
      setEditDialogOpen(false);
      queryClient.setQueryData(gateKeys.detail(id as string), data);
      queryClient.invalidateQueries({ queryKey: gateKeys.lists() });
    },
  });

  // Open edit dialog with current values
  const handleOpenEdit = () => {
    if (gate) {
      setEditForm({
        gate_name: gate.gate_name,
        description: gate.description || "",
        stage: gate.stage,
      });
      setEditDialogOpen(true);
    }
  };

  // Handle file selection for upload
  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
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

    try {
      setUploadError(null);
      await uploadMutation.mutateAsync({
        data: {
          gate_id: id,
          evidence_type: uploadType,
          description: uploadDescription || selectedFile.name,
        },
        file: selectedFile,
      });

      // Success - close modal and reset
      setUploadModalOpen(false);
      setSelectedFile(null);
      setUploadDescription("");
      setUploadType("DOCUMENTATION");
      // Refresh gate data to update evidence count
      queryClient.invalidateQueries({ queryKey: gateKeys.detail(id as string) });
    } catch (err) {
      setUploadError(err instanceof Error ? err.message : "Upload failed");
    }
  }, [selectedFile, uploadType, uploadDescription, uploadMutation, id, queryClient]);

  // Close upload modal
  const handleCloseUploadModal = useCallback(() => {
    setUploadModalOpen(false);
    setSelectedFile(null);
    setUploadDescription("");
    setUploadError(null);
    setUploadType("DOCUMENTATION");
  }, []);

  // Evidence type options
  const evidenceTypes = [
    { value: "DESIGN_DOCUMENT", label: "Design Documents" },
    { value: "TEST_RESULTS", label: "Test Results" },
    { value: "CODE_REVIEW", label: "Code Reviews" },
    { value: "DEPLOYMENT_PROOF", label: "Deployment Proofs" },
    { value: "DOCUMENTATION", label: "Documentation" },
    { value: "COMPLIANCE", label: "Compliance" },
  ];

  // Format file size
  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  // Check if user can approve
  const canApprove = user?.is_superuser || user?.roles?.some((r: string) =>
    ["CTO", "CPO", "CEO", "Admin", "Platform Admin"].includes(r)
  );

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="h-8 w-48 bg-gray-200 rounded animate-pulse" />
        <div className="grid gap-4 md:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-white rounded-lg border p-6">
              <div className="h-4 w-20 bg-gray-200 rounded animate-pulse mb-2" />
              <div className="h-8 w-24 bg-gray-200 rounded animate-pulse" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error || !gate) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <div className="text-red-500 mb-4">Gate not found</div>
        <Link href="/app/gates">
          <Button variant="outline">Back to Gates</Button>
        </Link>
      </div>
    );
  }

  const stage = SDLC_STAGES.find((s) => s.code === gate.stage);

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Link href="/app/projects" className="hover:text-foreground">
          Projects
        </Link>
        <span>/</span>
        <Link
          href={`/app/projects/${gate.project_id}`}
          className="hover:text-foreground"
        >
          Project
        </Link>
        <span>/</span>
        <span className="text-foreground">{gate.gate_name}</span>
      </div>

      {/* Gate header */}
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight">{gate.gate_name}</h1>
            <span
              className={`rounded-full px-3 py-1 text-sm font-medium border ${getStatusStyle(gate.status)}`}
            >
              {gate.status}
            </span>
          </div>
          <p className="text-muted-foreground mt-1">
            {gate.gate_type} - Stage {gate.stage} ({stage?.name})
          </p>
        </div>
        <div className="flex gap-2">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline">
                <svg
                  className="mr-2 h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"
                  />
                </svg>
                Options
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={handleOpenEdit}>
                <svg
                  className="mr-2 h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                  />
                </svg>
                Edit Gate
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                className="text-red-600 focus:text-red-600"
                onClick={() => setDeleteDialogOpen(true)}
              >
                <svg
                  className="mr-2 h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
                Delete Gate
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {gate.status === "DRAFT" && (
            <Button
              onClick={() => submitMutation.mutate()}
              disabled={submitMutation.isPending}
            >
              {submitMutation.isPending ? "Submitting..." : "Submit for Approval"}
            </Button>
          )}

          {gate.status === "PENDING_APPROVAL" && canApprove && (
            <>
              <Button
                variant="outline"
                onClick={() => approveMutation.mutate(false)}
                disabled={approveMutation.isPending}
                className="text-red-600 hover:text-red-700"
              >
                {approveMutation.isPending ? "Processing..." : "Reject"}
              </Button>
              <Button
                onClick={() => approveMutation.mutate(true)}
                disabled={approveMutation.isPending}
                className="bg-green-600 hover:bg-green-700"
              >
                {approveMutation.isPending ? "Approving..." : "Approve"}
              </Button>
            </>
          )}
        </div>
      </div>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Gate</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to delete &quot;{gate.gate_name}&quot;? This action
              cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => deleteMutation.mutate()}
              className="bg-red-600 hover:bg-red-700"
            >
              {deleteMutation.isPending ? "Deleting..." : "Delete"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Edit Gate Dialog */}
      <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Edit Gate</DialogTitle>
            <DialogDescription>
              Update gate information. Click save when you&apos;re done.
            </DialogDescription>
          </DialogHeader>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              updateMutation.mutate(editForm);
            }}
            className="space-y-4"
          >
            <div className="space-y-2">
              <Label htmlFor="gate_name">Gate Name</Label>
              <Input
                id="gate_name"
                value={editForm.gate_name}
                onChange={(e) =>
                  setEditForm((prev) => ({ ...prev, gate_name: e.target.value }))
                }
                placeholder="e.g., G0.1 Problem Definition"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="stage">Stage</Label>
              <Select
                value={editForm.stage}
                onValueChange={(value) =>
                  setEditForm((prev) => ({ ...prev, stage: value }))
                }
              >
                <SelectTrigger id="stage">
                  <SelectValue placeholder="Select a stage" />
                </SelectTrigger>
                <SelectContent>
                  {SDLC_STAGES.map((stage) => (
                    <SelectItem key={stage.code} value={stage.code}>
                      {stage.code} - {stage.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={editForm.description}
                onChange={(e) =>
                  setEditForm((prev) => ({ ...prev, description: e.target.value }))
                }
                placeholder="Gate description..."
                rows={3}
              />
            </div>
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setEditDialogOpen(false)}
              >
                Cancel
              </Button>
              <Button type="submit" disabled={updateMutation.isPending}>
                {updateMutation.isPending ? "Saving..." : "Save Changes"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Gate info grid */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Stage</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stage?.name || gate.stage}</div>
            <p className="text-xs text-muted-foreground">{stage?.description}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Gate Type</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{gate.gate_type}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Evidence</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{gate.evidence_count}</div>
            <p className="text-xs text-muted-foreground">files attached</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Created</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-lg font-bold">
              {new Date(gate.created_at).toLocaleDateString()}
            </div>
            <p className="text-xs text-muted-foreground">
              {new Date(gate.created_at).toLocaleTimeString()}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Description */}
      {gate.description && (
        <Card>
          <CardHeader>
            <CardTitle>Description</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">{gate.description}</p>
          </CardContent>
        </Card>
      )}

      {/* Exit Criteria */}
      <Card>
        <CardHeader>
          <CardTitle>Exit Criteria</CardTitle>
          <CardDescription>
            Requirements that must be met to pass this gate
          </CardDescription>
        </CardHeader>
        <CardContent>
          {gate.exit_criteria && gate.exit_criteria.length > 0 ? (
            <div className="space-y-3">
              {gate.exit_criteria.map((criterion, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between rounded-lg border p-3"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`h-6 w-6 rounded-full flex items-center justify-center ${
                        criterion.status === "met"
                          ? "bg-green-100 text-green-600"
                          : criterion.status === "not_met"
                          ? "bg-red-100 text-red-600"
                          : "bg-gray-100 text-gray-600"
                      }`}
                    >
                      {criterion.status === "met" ? (
                        <svg
                          className="h-4 w-4"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                      ) : criterion.status === "not_met" ? (
                        <svg
                          className="h-4 w-4"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M6 18L18 6M6 6l12 12"
                          />
                        </svg>
                      ) : (
                        <svg
                          className="h-4 w-4"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                          />
                        </svg>
                      )}
                    </div>
                    <span className="font-medium">{criterion.criterion}</span>
                  </div>
                  <span
                    className={`rounded-full px-2 py-1 text-xs font-medium ${
                      criterion.status === "met"
                        ? "bg-green-100 text-green-700"
                        : criterion.status === "not_met"
                        ? "bg-red-100 text-red-700"
                        : "bg-gray-100 text-gray-700"
                    }`}
                  >
                    {criterion.status}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-muted-foreground text-center py-4">
              No exit criteria defined
            </p>
          )}
        </CardContent>
      </Card>

      {/* Approval History */}
      <Card>
        <CardHeader>
          <CardTitle>Approval History</CardTitle>
          <CardDescription>Track approval workflow progress</CardDescription>
        </CardHeader>
        <CardContent>
          {gate.approvals && gate.approvals.length > 0 ? (
            <div className="space-y-4">
              {gate.approvals.map((approval) => (
                <div
                  key={approval.id}
                  className="flex items-start justify-between rounded-lg border p-4"
                >
                  <div className="flex items-start gap-4">
                    <div
                      className={`h-10 w-10 rounded-full flex items-center justify-center ${
                        approval.is_approved
                          ? "bg-green-100 text-green-600"
                          : "bg-red-100 text-red-600"
                      }`}
                    >
                      {approval.is_approved ? (
                        <svg
                          className="h-5 w-5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                      ) : (
                        <svg
                          className="h-5 w-5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M6 18L18 6M6 6l12 12"
                          />
                        </svg>
                      )}
                    </div>
                    <div>
                      <p className="font-medium">
                        {approval.approved_by_name || "Unknown"}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {approval.approved_by_role || "Reviewer"}
                      </p>
                      {approval.comments && (
                        <p className="text-sm mt-1">&quot;{approval.comments}&quot;</p>
                      )}
                    </div>
                  </div>
                  <div className="text-right">
                    <span
                      className={`rounded-full px-2 py-1 text-xs font-medium ${
                        approval.is_approved
                          ? "bg-green-100 text-green-700"
                          : "bg-red-100 text-red-700"
                      }`}
                    >
                      {approval.is_approved ? "Approved" : "Rejected"}
                    </span>
                    <p className="text-xs text-muted-foreground mt-1">
                      {new Date(approval.approved_at).toLocaleString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-muted-foreground text-center py-4">
              No approvals yet
            </p>
          )}
        </CardContent>
      </Card>

      {/* Policy Violations */}
      {gate.policy_violations && gate.policy_violations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-red-600">Policy Violations</CardTitle>
            <CardDescription>Issues that must be resolved</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {gate.policy_violations.map((violation, index) => (
                <div
                  key={index}
                  className="flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-3"
                >
                  <svg
                    className="h-5 w-5 text-red-500 mt-0.5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                    />
                  </svg>
                  <div>
                    <p className="font-medium text-red-700">{violation.message}</p>
                    <p className="text-sm text-red-600">
                      Policy: {violation.policy_code || violation.policy_id}
                    </p>
                    <p className="text-xs text-red-500 mt-1">
                      {new Date(violation.evaluated_at).toLocaleString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Actions */}
      <div className="flex justify-end gap-2">
        <Link href={`/app/projects/${gate.project_id}`}>
          <Button variant="outline">Back to Project</Button>
        </Link>
        <Button variant="outline" onClick={() => setUploadModalOpen(true)}>
          <svg
            className="mr-2 h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
            />
          </svg>
          Upload Evidence
        </Button>
      </div>

      {/* Upload Evidence Modal */}
      {uploadModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
            {/* Modal Header */}
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Upload Evidence</h2>
              <button
                onClick={handleCloseUploadModal}
                className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
              >
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
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
                    <svg className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                    </svg>
                    <span className="text-sm font-medium text-gray-900 truncate max-w-xs">
                      {selectedFile.name}
                    </span>
                    <span className="text-xs text-gray-500">
                      ({formatFileSize(selectedFile.size)})
                    </span>
                  </div>
                ) : (
                  <div>
                    <svg className="h-8 w-8 text-gray-400 mx-auto mb-2" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
                    </svg>
                    <p className="text-sm text-gray-600">Click to select file</p>
                    <p className="text-xs text-gray-400 mt-1">Max 50MB</p>
                  </div>
                )}
              </button>
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
                {evidenceTypes.map((type) => (
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
                value={uploadDescription}
                onChange={(e) => setUploadDescription(e.target.value)}
                placeholder="Add a description for this evidence..."
                rows={3}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>

            {/* Actions */}
            <div className="flex gap-3">
              <button
                onClick={handleCloseUploadModal}
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
                    <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Uploading...
                  </>
                ) : (
                  <>
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
                    </svg>
                    Upload
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
