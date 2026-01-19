/**
 * StreamingFileList Component - Next.js App Router
 * @module frontend/landing/src/components/codegen/StreamingFileList
 * @status Sprint 67 - SSE Streaming Implementation
 * @description Real-time file tree with generation progress
 */
"use client";

import { useState, useMemo, useCallback } from "react";
import {
  File,
  Folder,
  FolderOpen,
  ChevronRight,
  ChevronDown,
  FileCode,
  FileJson,
  FileText,
  Loader2,
  CheckCircle2,
  XCircle,
} from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { StreamingFile, FileTreeNode } from "@/lib/types/streaming";
import {
  buildFileTree,
  getFileIconColor,
  detectLanguage,
} from "@/lib/types/streaming";

interface StreamingFileListProps {
  /** List of generated files */
  files: StreamingFile[];
  /** Total expected files (for progress) */
  totalExpected?: number;
  /** Whether generation is in progress */
  isGenerating: boolean;
  /** Currently selected file path */
  selectedPath?: string;
  /** Callback when a file is selected */
  onFileSelect?: (file: StreamingFile) => void;
  /** Path of file currently being generated */
  currentGeneratingPath?: string;
  /** Additional CSS classes */
  className?: string;
  /** Show generation stats (default: true) */
  showStats?: boolean;
  /** Start time for duration calculation */
  startTime?: Date;
}

/**
 * Get file icon based on language
 */
function FileIcon({
  language,
  className,
}: {
  language: string;
  className?: string;
}) {
  const colorClass = getFileIconColor(language);

  switch (language) {
    case "python":
    case "typescript":
    case "javascript":
      return <FileCode className={cn("h-4 w-4", colorClass, className)} />;
    case "json":
      return <FileJson className={cn("h-4 w-4", colorClass, className)} />;
    case "markdown":
    case "yaml":
    case "text":
      return <FileText className={cn("h-4 w-4", colorClass, className)} />;
    default:
      return <File className={cn("h-4 w-4", colorClass, className)} />;
  }
}

/**
 * File status icon
 */
function StatusIcon({ status }: { status: StreamingFile["status"] }) {
  switch (status) {
    case "generating":
      return <Loader2 className="h-3 w-3 animate-spin text-blue-500" />;
    case "valid":
      return <CheckCircle2 className="h-3 w-3 text-green-500" />;
    case "error":
      return <XCircle className="h-3 w-3 text-red-500" />;
  }
}

/**
 * Recursive tree node component
 */
function TreeNode({
  node,
  depth,
  selectedPath,
  currentGeneratingPath,
  expandedPaths,
  onToggle,
  onSelect,
}: {
  node: FileTreeNode;
  depth: number;
  selectedPath?: string;
  currentGeneratingPath?: string;
  expandedPaths: Set<string>;
  onToggle: (path: string) => void;
  onSelect: (file: StreamingFile) => void;
}) {
  const isExpanded = expandedPaths.has(node.path);
  const isSelected = selectedPath === node.path;
  const isGenerating = currentGeneratingPath === node.path;

  if (node.isDirectory) {
    return (
      <div>
        <button
          onClick={() => onToggle(node.path)}
          className={cn(
            "flex items-center gap-2 w-full px-2 py-1 text-sm hover:bg-muted/50 rounded-md transition-colors",
            "text-left"
          )}
          style={{ paddingLeft: `${depth * 16 + 8}px` }}
        >
          {isExpanded ? (
            <>
              <ChevronDown className="h-4 w-4 text-muted-foreground" />
              <FolderOpen className="h-4 w-4 text-yellow-500" />
            </>
          ) : (
            <>
              <ChevronRight className="h-4 w-4 text-muted-foreground" />
              <Folder className="h-4 w-4 text-yellow-500" />
            </>
          )}
          <span className="font-medium">{node.name}</span>
        </button>

        {isExpanded && node.children && (
          <div>
            {node.children.map((child) => (
              <TreeNode
                key={child.path}
                node={child}
                depth={depth + 1}
                selectedPath={selectedPath}
                currentGeneratingPath={currentGeneratingPath}
                expandedPaths={expandedPaths}
                onToggle={onToggle}
                onSelect={onSelect}
              />
            ))}
          </div>
        )}
      </div>
    );
  }

  // File node
  const file = node.file!;
  const language = detectLanguage(file.path);

  return (
    <button
      onClick={() => onSelect(file)}
      className={cn(
        "flex items-center gap-2 w-full px-2 py-1 text-sm rounded-md transition-colors",
        "text-left hover:bg-muted/50",
        isSelected && "bg-muted",
        isGenerating && "animate-pulse bg-blue-500/10"
      )}
      style={{ paddingLeft: `${depth * 16 + 8}px` }}
    >
      <div className="w-4" /> {/* Spacer for alignment */}
      <FileIcon language={language} />
      <span className="flex-1 truncate">{node.name}</span>
      <StatusIcon status={file.status} />
      <span className="text-xs text-muted-foreground">{file.lines}L</span>
    </button>
  );
}

/**
 * StreamingFileList Component
 *
 * Displays a file tree with real-time generation progress.
 * Features:
 * - Collapsible folder structure
 * - File status indicators
 * - Generation progress bar
 * - Stats display (files, lines, duration)
 */
export function StreamingFileList({
  files,
  totalExpected,
  isGenerating,
  selectedPath,
  onFileSelect,
  currentGeneratingPath,
  className,
  showStats = true,
  startTime,
}: StreamingFileListProps) {
  const [expandedPaths, setExpandedPaths] = useState<Set<string>>(
    new Set(["src"]) // Default expand src folder
  );

  // Build file tree
  const fileTree = useMemo(() => buildFileTree(files), [files]);

  // Calculate stats
  const stats = useMemo(() => {
    const totalFiles = files.length;
    const totalLines = files.reduce((sum, f) => sum + f.lines, 0);
    const validFiles = files.filter((f) => f.status === "valid").length;
    const errorFiles = files.filter((f) => f.status === "error").length;

    let duration = 0;
    if (startTime) {
      duration = Math.round((Date.now() - startTime.getTime()) / 1000);
    }

    return { totalFiles, totalLines, validFiles, errorFiles, duration };
  }, [files, startTime]);

  // Progress calculation
  const progress = useMemo(() => {
    if (!totalExpected || totalExpected === 0) return 0;
    return Math.min((files.length / totalExpected) * 100, 100);
  }, [files.length, totalExpected]);

  // Toggle folder expansion
  const handleToggle = useCallback((path: string) => {
    setExpandedPaths((prev) => {
      const next = new Set(prev);
      if (next.has(path)) {
        next.delete(path);
      } else {
        next.add(path);
      }
      return next;
    });
  }, []);

  // Handle file selection
  const handleSelect = useCallback(
    (file: StreamingFile) => {
      onFileSelect?.(file);
    },
    [onFileSelect]
  );

  // Auto-expand parent folders when file is generating
  useMemo(() => {
    if (currentGeneratingPath) {
      const parts = currentGeneratingPath.split("/");
      const paths = parts.slice(0, -1).reduce<string[]>((acc, part, i) => {
        const path = i === 0 ? part : `${acc[i - 1]}/${part}`;
        acc.push(path);
        return acc;
      }, []);

      setExpandedPaths((prev) => {
        const next = new Set(prev);
        paths.forEach((p) => next.add(p));
        return next;
      });
    }
  }, [currentGeneratingPath]);

  return (
    <div className={cn("flex flex-col h-full", className)}>
      {/* Header with stats */}
      {showStats && (
        <div className="px-4 py-3 border-b space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-sm">Generated Files</h3>
            {isGenerating && (
              <Badge variant="outline" className="text-xs animate-pulse">
                <Loader2 className="h-3 w-3 mr-1 animate-spin" />
                Generating...
              </Badge>
            )}
          </div>

          {/* Progress bar */}
          {totalExpected && totalExpected > 0 && (
            <div className="space-y-1">
              <Progress value={progress} className="h-2" />
              <div className="flex justify-between text-xs text-muted-foreground">
                <span>
                  {files.length}/{totalExpected} files
                </span>
                <span>{Math.round(progress)}%</span>
              </div>
            </div>
          )}

          {/* Stats grid */}
          <div className="grid grid-cols-4 gap-2 text-center">
            <div className="bg-muted/50 rounded-md p-2">
              <div className="text-lg font-bold">{stats.totalFiles}</div>
              <div className="text-xs text-muted-foreground">Files</div>
            </div>
            <div className="bg-muted/50 rounded-md p-2">
              <div className="text-lg font-bold">{stats.totalLines}</div>
              <div className="text-xs text-muted-foreground">Lines</div>
            </div>
            <div className="bg-muted/50 rounded-md p-2">
              <div className="text-lg font-bold text-green-600">
                {stats.validFiles}
              </div>
              <div className="text-xs text-muted-foreground">Valid</div>
            </div>
            <div className="bg-muted/50 rounded-md p-2">
              <div className="text-lg font-bold">
                {stats.duration > 0 ? `${stats.duration}s` : "-"}
              </div>
              <div className="text-xs text-muted-foreground">Time</div>
            </div>
          </div>
        </div>
      )}

      {/* File tree */}
      <ScrollArea className="flex-1">
        <div className="p-2">
          {fileTree.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
              {isGenerating ? (
                <>
                  <Loader2 className="h-8 w-8 animate-spin mb-2" />
                  <p className="text-sm">Waiting for files...</p>
                </>
              ) : (
                <>
                  <File className="h-8 w-8 mb-2" />
                  <p className="text-sm">No files generated yet</p>
                </>
              )}
            </div>
          ) : (
            fileTree.map((node) => (
              <TreeNode
                key={node.path}
                node={node}
                depth={0}
                selectedPath={selectedPath}
                currentGeneratingPath={currentGeneratingPath}
                expandedPaths={expandedPaths}
                onToggle={handleToggle}
                onSelect={handleSelect}
              />
            ))
          )}
        </div>
      </ScrollArea>

      {/* Error count */}
      {stats.errorFiles > 0 && (
        <div className="px-4 py-2 border-t bg-red-500/10">
          <div className="flex items-center gap-2 text-sm text-red-600">
            <XCircle className="h-4 w-4" />
            <span>{stats.errorFiles} file(s) with errors</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default StreamingFileList;
