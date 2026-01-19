/**
 * CopyableCodeBlock Component - Next.js App Router
 * @module frontend/landing/src/components/codegen/CopyableCodeBlock
 * @status Sprint 66 - EP-06 Migration
 * @description Lightweight code block with copy-to-clipboard (no heavy syntax highlighter)
 */
"use client";

import { useState, useCallback } from "react";
import { Copy, Check, FileCode, FileJson } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface CopyableCodeBlockProps {
  /** Code content to display */
  code: string;
  /** Programming language for styling (default: 'json') */
  language?: string;
  /** Optional title shown in header bar */
  title?: string;
  /** Maximum height with scroll (default: '400px') */
  maxHeight?: string;
  /** Additional CSS classes */
  className?: string;
  /** Show line numbers (default: true) */
  showLineNumbers?: boolean;
}

/**
 * CopyableCodeBlock Component
 *
 * Lightweight code block with copy functionality.
 * Uses simple pre/code styling without heavy syntax highlighting library.
 * Reduces bundle size by ~250 kB compared to react-syntax-highlighter.
 */
export function CopyableCodeBlock({
  code,
  language = "json",
  title,
  maxHeight = "400px",
  className,
  showLineNumbers = true,
}: CopyableCodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy to clipboard:", err);
    }
  }, [code]);

  const getLanguageIcon = () => {
    switch (language) {
      case "json":
        return <FileJson className="h-4 w-4" />;
      default:
        return <FileCode className="h-4 w-4" />;
    }
  };

  // Split code into lines for line numbers
  const lines = code.split("\n");

  return (
    <div className={cn("rounded-lg border overflow-hidden", className)}>
      {/* Header bar */}
      <div className="flex items-center justify-between px-4 py-2 bg-muted/50 border-b">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          {getLanguageIcon()}
          <span>{title || language.toUpperCase()}</span>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleCopy}
          className="h-8 gap-2"
        >
          {copied ? (
            <>
              <Check className="h-4 w-4 text-green-500" />
              <span className="text-green-500">Copied</span>
            </>
          ) : (
            <>
              <Copy className="h-4 w-4" />
              <span>Copy</span>
            </>
          )}
        </Button>
      </div>

      {/* Code content */}
      <div
        className="overflow-auto bg-slate-900 text-slate-100"
        style={{ maxHeight }}
      >
        <div className="p-4 font-mono text-sm leading-relaxed">
          {showLineNumbers ? (
            <table className="w-full border-collapse">
              <tbody>
                {lines.map((line, i) => (
                  <tr key={i} className="hover:bg-slate-800/50">
                    <td className="pr-4 text-right text-slate-500 select-none w-12 align-top">
                      {i + 1}
                    </td>
                    <td className="whitespace-pre-wrap break-all">{line || " "}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <pre className="whitespace-pre-wrap break-all">{code}</pre>
          )}
        </div>
      </div>
    </div>
  );
}

export default CopyableCodeBlock;
