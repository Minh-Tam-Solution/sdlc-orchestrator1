/**
 * useStreamingGeneration Hook - Next.js App Router
 * @module frontend/landing/src/hooks/useStreamingGeneration
 * @status Sprint 67 - SSE Streaming Implementation
 * @description SSE-based streaming hook for real-time code generation
 * @note Uses httpOnly cookies for auth (Sprint 63 migration)
 */

import { useState, useRef, useCallback } from "react";
import { useQueryClient } from "@tanstack/react-query";
import type {
  GenerationStatus,
  GenerationResult,
  StreamingFile,
  QualityGateStatus,
  CodegenStreamEvent,
  UseStreamingGenerationOptions,
  UseStreamingGenerationReturn,
} from "@/lib/types/streaming";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * useStreamingGeneration Hook
 *
 * Manages SSE connection for real-time code generation.
 * Uses fetch() with ReadableStream for SSE handling.
 * Supports cancellation via AbortController.
 *
 * @example
 * ```tsx
 * const { status, files, startGeneration, cancelGeneration } = useStreamingGeneration({
 *   onFileGenerated: (file) => console.log('Generated:', file.path),
 *   onComplete: (result) => console.log('Done:', result.totalFiles),
 * });
 *
 * // Start generation
 * await startGeneration(sessionId, blueprint);
 *
 * // Cancel if needed
 * cancelGeneration();
 * ```
 */
export function useStreamingGeneration(
  options: UseStreamingGenerationOptions = {}
): UseStreamingGenerationReturn {
  const queryClient = useQueryClient();

  // State
  const [status, setStatus] = useState<GenerationStatus>("idle");
  const [files, setFiles] = useState<StreamingFile[]>([]);
  const [qualityGates, setQualityGates] = useState<QualityGateStatus[]>([
    { gate_number: 1, gate_name: "Syntax", status: "pending", issues: 0 },
    { gate_number: 2, gate_name: "Security", status: "pending", issues: 0 },
    { gate_number: 3, gate_name: "Context", status: "pending", issues: 0 },
    { gate_number: 4, gate_name: "Tests", status: "pending", issues: 0 },
  ]);
  const [progress, setProgress] = useState(0);
  const [provider, setProvider] = useState<{ model: string; provider: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [currentFile, setCurrentFile] = useState<string | null>(null);

  // Refs
  const abortControllerRef = useRef<AbortController | null>(null);
  const startTimeRef = useRef<Date | null>(null);

  /**
   * Handle incoming SSE event
   */
  const handleEvent = useCallback(
    (event: CodegenStreamEvent) => {
      switch (event.type) {
        case "started": {
          setStatus("generating");
          setProvider({ model: event.model, provider: event.provider });
          startTimeRef.current = new Date();
          break;
        }

        case "file_generating": {
          setCurrentFile(event.path);
          options.onFileGenerating?.(event.path);
          break;
        }

        case "file_generated": {
          const newFile: StreamingFile = {
            path: event.path,
            content: event.content,
            lines: event.lines,
            language: event.language,
            status: event.syntax_valid !== false ? "valid" : "error",
          };

          setFiles((prev) => {
            const existing = prev.findIndex((f) => f.path === event.path);
            if (existing >= 0) {
              const updated = [...prev];
              updated[existing] = newFile;
              return updated;
            }
            return [...prev, newFile];
          });

          setProgress((prev) => Math.min(prev + 5, 80)); // Cap at 80% until quality gates
          setCurrentFile(null);
          options.onFileGenerated?.(newFile);
          break;
        }

        case "quality_started": {
          setStatus("quality_check");
          setProgress(80);
          break;
        }

        case "quality_gate": {
          const gateStatus: QualityGateStatus = {
            gate_number: event.gate_number,
            gate_name: event.gate_name,
            status: event.status,
            issues: event.issues,
            duration_ms: event.duration_ms,
          };

          setQualityGates((prev) =>
            prev.map((g) =>
              g.gate_number === event.gate_number ? gateStatus : g
            )
          );

          // Update progress: 80% + 5% per gate (4 gates = 100%)
          setProgress(80 + event.gate_number * 5);
          options.onQualityGate?.(gateStatus);
          break;
        }

        case "completed": {
          setStatus("completed");
          setProgress(100);

          const result: GenerationResult = {
            success: event.success,
            totalFiles: event.total_files,
            totalLines: event.total_lines,
            durationMs: event.duration_ms,
            qualityGates: qualityGates,
            files: files,
          };

          // Invalidate related queries
          queryClient.invalidateQueries({ queryKey: ["codegen"] });
          options.onComplete?.(result);
          break;
        }

        case "error": {
          setStatus("error");
          setError(event.message);
          options.onError?.(new Error(event.message));
          break;
        }
      }
    },
    [files, qualityGates, queryClient, options]
  );

  /**
   * Parse SSE data from ReadableStream
   */
  const parseSSEData = (data: string): CodegenStreamEvent | null => {
    try {
      return JSON.parse(data) as CodegenStreamEvent;
    } catch {
      console.error("Failed to parse SSE event:", data);
      return null;
    }
  };

  /**
   * Connect to SSE endpoint and process stream
   */
  const connectSSE = useCallback(
    async (url: string, method: "GET" | "POST" = "GET", body?: object) => {
      abortControllerRef.current = new AbortController();

      try {
        const response = await fetch(url, {
          method,
          credentials: "include", // httpOnly cookies (Sprint 63)
          headers: {
            "Content-Type": "application/json",
            Accept: "text/event-stream",
          },
          body: body ? JSON.stringify(body) : undefined,
          signal: abortControllerRef.current.signal,
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const reader = response.body?.getReader();
        if (!reader) {
          throw new Error("No response body");
        }

        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();

          if (done) {
            break;
          }

          buffer += decoder.decode(value, { stream: true });

          // Process complete events (split by double newline)
          const events = buffer.split("\n\n");
          buffer = events.pop() || ""; // Keep incomplete event in buffer

          for (const eventStr of events) {
            if (!eventStr.trim()) continue;

            // Parse SSE format: "data: {...}"
            const lines = eventStr.split("\n");
            for (const line of lines) {
              if (line.startsWith("data: ")) {
                const jsonData = line.slice(6); // Remove "data: " prefix
                const event = parseSSEData(jsonData);
                if (event) {
                  handleEvent(event);
                }
              }
            }
          }
        }
      } catch (err) {
        if (err instanceof Error && err.name === "AbortError") {
          setStatus("cancelled");
          options.onCancel?.();
        } else {
          setStatus("error");
          setError(err instanceof Error ? err.message : "Connection failed");
          options.onError?.(err instanceof Error ? err : new Error("Connection failed"));
        }
      }
    },
    [handleEvent, options]
  );

  /**
   * Start code generation with a blueprint
   */
  const startGeneration = useCallback(
    async (sessionId: string, blueprint: object) => {
      // Reset state
      setStatus("connecting");
      setFiles([]);
      setQualityGates([
        { gate_number: 1, gate_name: "Syntax", status: "pending", issues: 0 },
        { gate_number: 2, gate_name: "Security", status: "pending", issues: 0 },
        { gate_number: 3, gate_name: "Context", status: "pending", issues: 0 },
        { gate_number: 4, gate_name: "Tests", status: "pending", issues: 0 },
      ]);
      setProgress(0);
      setError(null);
      setCurrentFile(null);
      setProvider(null);

      await connectSSE(`${API_BASE}/codegen/generate/stream`, "POST", {
        session_id: sessionId,
        blueprint,
      });
    },
    [connectSSE]
  );

  /**
   * Resume a previously interrupted generation
   */
  const resumeGeneration = useCallback(
    async (sessionId: string) => {
      setStatus("connecting");
      setError(null);

      await connectSSE(`${API_BASE}/codegen/generate/resume/${sessionId}`, "POST");
    },
    [connectSSE]
  );

  /**
   * Cancel ongoing generation
   */
  const cancelGeneration = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
  }, []);

  /**
   * Reset to idle state
   */
  const reset = useCallback(() => {
    cancelGeneration();
    setStatus("idle");
    setFiles([]);
    setQualityGates([
      { gate_number: 1, gate_name: "Syntax", status: "pending", issues: 0 },
      { gate_number: 2, gate_name: "Security", status: "pending", issues: 0 },
      { gate_number: 3, gate_name: "Context", status: "pending", issues: 0 },
      { gate_number: 4, gate_name: "Tests", status: "pending", issues: 0 },
    ]);
    setProgress(0);
    setError(null);
    setCurrentFile(null);
    setProvider(null);
  }, [cancelGeneration]);

  return {
    status,
    files,
    qualityGates,
    progress,
    provider,
    error,
    currentFile,
    startGeneration,
    resumeGeneration,
    cancelGeneration,
    reset,
  };
}

export default useStreamingGeneration;
