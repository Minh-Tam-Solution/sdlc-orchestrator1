/**
 * Code Generation Page - Next.js App Router
 * @module frontend/landing/src/app/app/code-generation/page
 * @status Sprint 67 - SSE Streaming Implementation
 * @description EP-06 Code Generation with real SSE streaming
 */
"use client";

import { useEffect, useState, useMemo } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  Play,
  Square,
  RotateCcw,
  Download,
  CheckCircle2,
  XCircle,
  AlertCircle,
} from "lucide-react";
import { useStreamingGeneration } from "@/hooks/useStreamingGeneration";
import { StreamingFileList, CodePreviewPanel } from "@/components/codegen";
import type { AppBlueprint } from "@/lib/types/onboarding";
import type { StreamingFile } from "@/lib/types/streaming";

// Dynamic import for bundle optimization
const BlueprintJsonViewer = dynamic(
  () => import("@/components/codegen/BlueprintJsonViewer").then((mod) => mod.BlueprintJsonViewer),
  {
    loading: () => (
      <div className="h-64 animate-pulse bg-muted rounded-lg flex items-center justify-center">
        <span className="text-muted-foreground">Loading blueprint viewer...</span>
      </div>
    ),
    ssr: false,
  }
);

/**
 * Quality Gate status display
 */
const QUALITY_GATES = [
  { number: 1, name: "Syntax", description: "AST parsing, linting" },
  { number: 2, name: "Security", description: "Semgrep SAST scan" },
  { number: 3, name: "Context", description: "Cross-reference validation" },
  { number: 4, name: "Tests", description: "Automated test execution" },
];

export default function CodeGenerationPage() {
  const router = useRouter();

  // Blueprint from app-builder
  const [blueprint, setBlueprint] = useState<AppBlueprint | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);

  // Selected file for preview
  const [selectedFile, setSelectedFile] = useState<StreamingFile | null>(null);

  // SSE streaming hook
  const {
    status,
    files,
    qualityGates,
    progress,
    provider,
    error,
    currentFile,
    startGeneration,
    cancelGeneration,
    reset,
  } = useStreamingGeneration({
    onFileGenerated: (file) => {
      // Auto-select first file
      if (!selectedFile) {
        setSelectedFile(file);
      }
    },
    onComplete: (result) => {
      console.log("Generation complete:", result);
    },
    onError: (err) => {
      console.error("Generation error:", err);
    },
  });

  // Load blueprint from sessionStorage
  useEffect(() => {
    const storedBlueprint = sessionStorage.getItem("appBlueprint");
    const storedSessionId = sessionStorage.getItem("onboardingSessionId");

    if (storedBlueprint) {
      try {
        setBlueprint(JSON.parse(storedBlueprint));
      } catch (e) {
        console.error("Failed to parse blueprint:", e);
      }
    }

    if (storedSessionId) {
      setSessionId(storedSessionId);
    } else {
      // Generate a new session ID if not present
      setSessionId(`session-${Date.now()}`);
    }
  }, []);

  // Start generation
  const handleStartGeneration = async () => {
    if (!blueprint || !sessionId) return;
    reset();
    setSelectedFile(null);
    await startGeneration(sessionId, blueprint);
  };

  // Cancel generation
  const handleCancel = () => {
    cancelGeneration();
  };

  // Reset and start new
  const handleReset = () => {
    reset();
    setSelectedFile(null);
  };

  // Download generated files
  const handleDownload = (file: StreamingFile) => {
    const blob = new Blob([file.content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = file.path.split("/").pop() || "file.txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  // Calculate stats
  const stats = useMemo(() => {
    const totalFiles = files.length;
    const totalLines = files.reduce((sum, f) => sum + f.lines, 0);
    const validFiles = files.filter((f) => f.status === "valid").length;
    const errorFiles = files.filter((f) => f.status === "error").length;
    return { totalFiles, totalLines, validFiles, errorFiles };
  }, [files]);

  // Gate status badge
  const getGateStatusBadge = (gateStatus: string) => {
    switch (gateStatus) {
      case "pending":
        return <Badge variant="outline">Pending</Badge>;
      case "running":
        return <Badge className="bg-blue-100 text-blue-800 animate-pulse">Running...</Badge>;
      case "passed":
        return <Badge className="bg-green-100 text-green-800">Passed</Badge>;
      case "failed":
        return <Badge className="bg-red-100 text-red-800">Failed</Badge>;
      case "skipped":
        return <Badge variant="secondary">Skipped</Badge>;
      default:
        return <Badge variant="outline">{gateStatus}</Badge>;
    }
  };

  // No blueprint state
  if (!blueprint) {
    return (
      <div className="space-y-6">
        <nav className="flex items-center gap-2 text-sm text-muted-foreground">
          <Link href="/app" className="hover:text-foreground">
            Dashboard
          </Link>
          <span>/</span>
          <span className="text-foreground">Code Generation</span>
        </nav>

        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <AlertCircle className="h-16 w-16 text-muted-foreground mb-4" />
            <h2 className="text-xl font-semibold mb-2">No Blueprint Found</h2>
            <p className="text-muted-foreground mb-4 text-center max-w-md">
              You need to generate an AppBlueprint first using the App Builder.
            </p>
            <Button onClick={() => router.push("/app/app-builder")}>
              Go to App Builder
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const isGenerating = status === "connecting" || status === "generating" || status === "quality_check";
  const isComplete = status === "completed";
  const hasError = status === "error";

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-muted-foreground">
        <Link href="/app" className="hover:text-foreground">
          Dashboard
        </Link>
        <span>/</span>
        <Link href="/app/app-builder" className="hover:text-foreground">
          App Builder
        </Link>
        <span>/</span>
        <span className="text-foreground">Code Generation</span>
      </nav>

      {/* Page header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Code Generation</h1>
          <p className="text-muted-foreground mt-1">
            Generate production-ready code from your AppBlueprint with 4-Gate Quality Pipeline.
          </p>
          {provider && (
            <p className="text-sm text-muted-foreground mt-1">
              Provider: {provider.provider} • Model: {provider.model}
            </p>
          )}
        </div>
        <div className="flex items-center gap-2">
          {!isGenerating && !isComplete && (
            <Button onClick={handleStartGeneration} size="lg">
              <Play className="h-4 w-4 mr-2" />
              Start Generation
            </Button>
          )}
          {isGenerating && (
            <Button onClick={handleCancel} variant="destructive" size="lg">
              <Square className="h-4 w-4 mr-2" />
              Cancel
            </Button>
          )}
          {(isComplete || hasError) && (
            <Button onClick={handleReset} variant="outline" size="lg">
              <RotateCcw className="h-4 w-4 mr-2" />
              Start New
            </Button>
          )}
        </div>
      </div>

      {/* Progress bar */}
      {isGenerating && (
        <Card>
          <CardContent className="py-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">
                  {status === "connecting" && "Connecting to server..."}
                  {status === "generating" && `Generating files... ${currentFile || ""}`}
                  {status === "quality_check" && "Running quality gates..."}
                </span>
                <span className="text-sm text-muted-foreground">{progress}%</span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>
          </CardContent>
        </Card>
      )}

      {/* Blueprint Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            {blueprint.app_name_display || blueprint.app_name}
            <Badge variant="outline">{blueprint.sdlc_tier}</Badge>
          </CardTitle>
          <CardDescription>
            {blueprint.domain} • {blueprint.modules?.length || 0} modules •{" "}
            {blueprint.modules?.reduce((sum, m) => sum + (m.entities?.length || 0), 0) || 0} entities
          </CardDescription>
        </CardHeader>
      </Card>

      {/* 4-Gate Quality Pipeline */}
      <Card>
        <CardHeader>
          <CardTitle>4-Gate Quality Pipeline</CardTitle>
          <CardDescription>
            All generated code passes through these quality gates before delivery.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-4 gap-4">
            {QUALITY_GATES.map((gate) => {
              const gateState = qualityGates.find((g) => g.gate_number === gate.number);
              const gateStatus = gateState?.status || "pending";
              return (
                <div
                  key={gate.number}
                  className="p-4 rounded-lg border bg-card text-center"
                >
                  <div className="text-2xl font-bold mb-1">Gate {gate.number}</div>
                  <div className="font-medium">{gate.name}</div>
                  <div className="text-xs text-muted-foreground mb-2">
                    {gate.description}
                  </div>
                  {getGateStatusBadge(gateStatus)}
                  {gateState?.duration_ms && (
                    <div className="text-xs text-muted-foreground mt-1">
                      {gateState.duration_ms}ms
                    </div>
                  )}
                  {gateState?.issues !== undefined && gateState.issues > 0 && (
                    <div className="text-xs text-red-600 mt-1">
                      {gateState.issues} issues
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* File Explorer + Preview */}
      {(files.length > 0 || isGenerating) && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* File List */}
          <Card className="lg:col-span-1">
            <StreamingFileList
              files={files}
              totalExpected={15} // Estimate
              isGenerating={isGenerating}
              selectedPath={selectedFile?.path}
              onFileSelect={setSelectedFile}
              currentGeneratingPath={currentFile || undefined}
              showStats={true}
              startTime={isGenerating ? new Date() : undefined}
            />
          </Card>

          {/* Code Preview */}
          <div className="lg:col-span-2">
            <CodePreviewPanel
              file={selectedFile}
              showHeader={true}
              showToolbar={true}
              showLineNumbers={true}
              maxHeight="600px"
              onDownload={handleDownload}
              onClose={() => setSelectedFile(null)}
              allowFullScreen={true}
              initialTheme="dark"
            />
          </div>
        </div>
      )}

      {/* Error */}
      {hasError && error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="py-4">
            <div className="flex items-center gap-2 text-red-800">
              <XCircle className="h-5 w-5" />
              <span>{error}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Success */}
      {isComplete && (
        <Card className="border-green-200 bg-green-50">
          <CardContent className="py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-green-800">
                <CheckCircle2 className="h-5 w-5" />
                <span className="font-medium">
                  Generation complete! {stats.totalFiles} files, {stats.totalLines} lines of code.
                </span>
              </div>
              <Button variant="outline" disabled>
                <Download className="h-4 w-4 mr-2" />
                Download ZIP (Coming Soon)
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Blueprint Details (Collapsible) */}
      <details className="group">
        <summary className="cursor-pointer list-none">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Blueprint Details</CardTitle>
              <span className="text-muted-foreground group-open:rotate-180 transition-transform">
                ▼
              </span>
            </CardHeader>
          </Card>
        </summary>
        <Card className="mt-2">
          <CardContent className="pt-6">
            <BlueprintJsonViewer blueprint={blueprint} />
          </CardContent>
        </Card>
      </details>
    </div>
  );
}
