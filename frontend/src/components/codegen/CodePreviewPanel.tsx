/**
 * CodePreviewPanel Component - Next.js App Router
 * @module frontend/landing/src/components/codegen/CodePreviewPanel
 * @status Sprint 67 - SSE Streaming Implementation
 * @description Lightweight code viewer with search, copy, and download
 * @note No react-syntax-highlighter for bundle optimization (Sprint 66)
 */
"use client";

import { useState, useCallback, useMemo, useRef, useEffect } from "react";
import {
  Copy,
  Check,
  Search,
  Download,
  X,
  ChevronUp,
  ChevronDown,
  Maximize2,
  Minimize2,
  Sun,
  Moon,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { StreamingFile } from "@/lib/types/streaming";
import { getFileIconColor } from "@/lib/types/streaming";

interface CodePreviewPanelProps {
  /** File to display */
  file: StreamingFile | null;
  /** Additional CSS classes */
  className?: string;
  /** Show header bar (default: true) */
  showHeader?: boolean;
  /** Show toolbar with search/copy (default: true) */
  showToolbar?: boolean;
  /** Show line numbers (default: true) */
  showLineNumbers?: boolean;
  /** Maximum height with scroll (default: '500px') */
  maxHeight?: string;
  /** Callback when download is clicked */
  onDownload?: (file: StreamingFile) => void;
  /** Callback when close is clicked */
  onClose?: () => void;
  /** Allow fullscreen mode (default: true) */
  allowFullScreen?: boolean;
  /** Initial theme (default: 'dark') */
  initialTheme?: "dark" | "light";
}

/**
 * CodePreviewPanel Component
 *
 * Displays code with:
 * - Line numbers
 * - Search within code
 * - Copy to clipboard
 * - Download file
 * - Theme toggle (dark/light)
 * - Fullscreen mode
 *
 * Uses lightweight CSS-based styling (no syntax highlighting library).
 */
export function CodePreviewPanel({
  file,
  className,
  showHeader = true,
  showToolbar = true,
  showLineNumbers = true,
  maxHeight = "500px",
  onDownload,
  onClose,
  allowFullScreen = true,
  initialTheme = "dark",
}: CodePreviewPanelProps) {
  const [copied, setCopied] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchOpen, setSearchOpen] = useState(false);
  const [currentMatch, setCurrentMatch] = useState(0);
  const [theme, setTheme] = useState<"dark" | "light">(initialTheme);
  const [isFullScreen, setIsFullScreen] = useState(false);

  const codeRef = useRef<HTMLDivElement>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);

  // Parse lines from content
  const lines = useMemo(() => {
    if (!file?.content) return [];
    return file.content.split("\n");
  }, [file?.content]);

  // Find search matches
  const matches = useMemo(() => {
    if (!searchQuery.trim() || !file?.content) return [];

    const results: { line: number; start: number; end: number }[] = [];
    const query = searchQuery.toLowerCase();

    lines.forEach((line, lineIndex) => {
      let startIndex = 0;
      let index = line.toLowerCase().indexOf(query, startIndex);

      while (index !== -1) {
        results.push({
          line: lineIndex,
          start: index,
          end: index + query.length,
        });
        startIndex = index + 1;
        index = line.toLowerCase().indexOf(query, startIndex);
      }
    });

    return results;
  }, [searchQuery, lines, file?.content]);

  // Copy to clipboard
  const handleCopy = useCallback(async () => {
    if (!file?.content) return;

    try {
      await navigator.clipboard.writeText(file.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  }, [file?.content]);

  // Download file
  const handleDownload = useCallback(() => {
    if (!file || !onDownload) return;
    onDownload(file);
  }, [file, onDownload]);

  // Navigate to match
  const navigateToMatch = useCallback(
    (direction: "next" | "prev") => {
      if (matches.length === 0) return;

      let newIndex = currentMatch;
      if (direction === "next") {
        newIndex = (currentMatch + 1) % matches.length;
      } else {
        newIndex = (currentMatch - 1 + matches.length) % matches.length;
      }

      setCurrentMatch(newIndex);

      // Scroll to match
      const matchLine = matches[newIndex].line;
      const lineElement = codeRef.current?.querySelector(
        `[data-line="${matchLine}"]`
      );
      lineElement?.scrollIntoView({ behavior: "smooth", block: "center" });
    },
    [matches, currentMatch]
  );

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "f") {
        e.preventDefault();
        setSearchOpen(true);
        setTimeout(() => searchInputRef.current?.focus(), 100);
      }
      if (e.key === "Escape") {
        setSearchOpen(false);
        setSearchQuery("");
        if (isFullScreen) setIsFullScreen(false);
      }
      if (e.key === "Enter" && searchOpen) {
        e.preventDefault();
        navigateToMatch(e.shiftKey ? "prev" : "next");
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [searchOpen, navigateToMatch, isFullScreen]);

  // Reset search when file changes
  useEffect(() => {
    setSearchQuery("");
    setCurrentMatch(0);
    setSearchOpen(false);
  }, [file?.path]);

  // Highlight line with matches
  const renderLine = useCallback(
    (line: string, lineIndex: number) => {
      if (!searchQuery.trim()) return line || " ";

      const lineMatches = matches.filter((m) => m.line === lineIndex);
      if (lineMatches.length === 0) return line || " ";

      // Build highlighted line
      const parts: React.ReactNode[] = [];
      let lastEnd = 0;

      lineMatches.forEach((match, i) => {
        // Add text before match
        if (match.start > lastEnd) {
          parts.push(line.slice(lastEnd, match.start));
        }

        // Add highlighted match
        const isCurrentMatch =
          matches.indexOf(match) === currentMatch;
        parts.push(
          <mark
            key={i}
            className={cn(
              "px-0.5 rounded",
              isCurrentMatch
                ? "bg-yellow-400 text-black"
                : "bg-yellow-200/50 text-inherit"
            )}
          >
            {line.slice(match.start, match.end)}
          </mark>
        );

        lastEnd = match.end;
      });

      // Add remaining text
      if (lastEnd < line.length) {
        parts.push(line.slice(lastEnd));
      }

      return parts.length > 0 ? parts : " ";
    },
    [searchQuery, matches, currentMatch]
  );

  if (!file) {
    return (
      <div
        className={cn(
          "flex items-center justify-center h-64 rounded-lg border bg-muted/50",
          className
        )}
      >
        <p className="text-muted-foreground">Select a file to preview</p>
      </div>
    );
  }

  const themeClasses = {
    dark: {
      bg: "bg-slate-900",
      text: "text-slate-100",
      lineNum: "text-slate-500",
      border: "border-slate-700",
      hover: "hover:bg-slate-800/50",
    },
    light: {
      bg: "bg-white",
      text: "text-slate-900",
      lineNum: "text-slate-400",
      border: "border-slate-200",
      hover: "hover:bg-slate-100/50",
    },
  };

  const tc = themeClasses[theme];

  const panelContent = (
    <div
      className={cn(
        "rounded-lg border overflow-hidden flex flex-col",
        isFullScreen && "fixed inset-4 z-50",
        className
      )}
    >
      {/* Header */}
      {showHeader && (
        <div
          className={cn(
            "flex items-center justify-between px-4 py-2 border-b",
            tc.bg,
            tc.border
          )}
        >
          <div className="flex items-center gap-2">
            <span className={cn("font-mono text-sm", tc.text)}>
              {file.path}
            </span>
            <Badge
              variant="outline"
              className={getFileIconColor(file.language)}
            >
              {file.language}
            </Badge>
            <Badge variant="secondary" className="text-xs">
              {file.lines} lines
            </Badge>
            {file.status === "generating" && (
              <Badge className="bg-blue-500 animate-pulse">Generating...</Badge>
            )}
            {file.status === "error" && (
              <Badge variant="destructive">Error</Badge>
            )}
          </div>

          <div className="flex items-center gap-1">
            {onClose && (
              <Button
                variant="ghost"
                size="icon"
                onClick={onClose}
                className="h-8 w-8"
              >
                <X className="h-4 w-4" />
              </Button>
            )}
          </div>
        </div>
      )}

      {/* Toolbar */}
      {showToolbar && (
        <div
          className={cn(
            "flex items-center justify-between px-4 py-2 border-b",
            tc.bg,
            tc.border
          )}
        >
          <div className="flex items-center gap-2">
            {/* Search */}
            {searchOpen ? (
              <div className="flex items-center gap-2">
                <Input
                  ref={searchInputRef}
                  value={searchQuery}
                  onChange={(e) => {
                    setSearchQuery(e.target.value);
                    setCurrentMatch(0);
                  }}
                  placeholder="Search..."
                  className="h-8 w-48"
                />
                {matches.length > 0 && (
                  <span className="text-xs text-muted-foreground">
                    {currentMatch + 1}/{matches.length}
                  </span>
                )}
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => navigateToMatch("prev")}
                  disabled={matches.length === 0}
                  className="h-8 w-8"
                >
                  <ChevronUp className="h-4 w-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => navigateToMatch("next")}
                  disabled={matches.length === 0}
                  className="h-8 w-8"
                >
                  <ChevronDown className="h-4 w-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => {
                    setSearchOpen(false);
                    setSearchQuery("");
                  }}
                  className="h-8 w-8"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            ) : (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSearchOpen(true)}
                className="h-8 gap-2"
              >
                <Search className="h-4 w-4" />
                <span className="text-xs text-muted-foreground">Ctrl+F</span>
              </Button>
            )}
          </div>

          <div className="flex items-center gap-1">
            {/* Theme toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              className="h-8 w-8"
            >
              {theme === "dark" ? (
                <Sun className="h-4 w-4" />
              ) : (
                <Moon className="h-4 w-4" />
              )}
            </Button>

            {/* Fullscreen */}
            {allowFullScreen && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsFullScreen(!isFullScreen)}
                className="h-8 w-8"
              >
                {isFullScreen ? (
                  <Minimize2 className="h-4 w-4" />
                ) : (
                  <Maximize2 className="h-4 w-4" />
                )}
              </Button>
            )}

            {/* Copy */}
            <Button
              variant="ghost"
              size="icon"
              onClick={handleCopy}
              className="h-8 w-8"
            >
              {copied ? (
                <Check className="h-4 w-4 text-green-500" />
              ) : (
                <Copy className="h-4 w-4" />
              )}
            </Button>

            {/* Download */}
            {onDownload && (
              <Button
                variant="ghost"
                size="icon"
                onClick={handleDownload}
                className="h-8 w-8"
              >
                <Download className="h-4 w-4" />
              </Button>
            )}
          </div>
        </div>
      )}

      {/* Code content */}
      <div
        ref={codeRef}
        className={cn("overflow-auto", tc.bg, tc.text)}
        style={{ maxHeight: isFullScreen ? "calc(100vh - 200px)" : maxHeight }}
      >
        <div className="p-4 font-mono text-sm leading-relaxed">
          {showLineNumbers ? (
            <table className="w-full border-collapse">
              <tbody>
                {lines.map((line, i) => (
                  <tr
                    key={i}
                    data-line={i}
                    className={cn(
                      tc.hover,
                      matches.some((m) => m.line === i) && "bg-yellow-900/20"
                    )}
                  >
                    <td
                      className={cn(
                        "pr-4 text-right select-none w-12 align-top",
                        tc.lineNum
                      )}
                    >
                      {i + 1}
                    </td>
                    <td className="whitespace-pre-wrap break-all">
                      {renderLine(line, i)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <pre className="whitespace-pre-wrap break-all">{file.content}</pre>
          )}
        </div>
      </div>
    </div>
  );

  // Render with fullscreen overlay
  if (isFullScreen) {
    return (
      <>
        <div
          className="fixed inset-0 bg-black/50 z-40"
          onClick={() => setIsFullScreen(false)}
        />
        {panelContent}
      </>
    );
  }

  return panelContent;
}

export default CodePreviewPanel;
