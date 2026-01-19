/**
 * File: frontend/web/src/components/codegen/CopyableCodeBlock.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 49
 * Date: December 24, 2025
 * Authority: Frontend Lead + CTO Approved
 * Foundation: EP-06 Code Generation Page (Code-Generation-Page-Specification.md)
 *
 * Description:
 * Reusable code block component with syntax highlighting and copy-to-clipboard.
 * ChatGPT/IDE-style presentation with header bar and copy button.
 */

import { useState, useCallback } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { Copy, Check, FileCode, FileJson } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface CopyableCodeBlockProps {
  /** Code content to display */
  code: string
  /** Programming language for syntax highlighting (default: 'json') */
  language?: string
  /** Optional title shown in header bar */
  title?: string
  /** Maximum height with scroll (default: '400px') */
  maxHeight?: string
  /** Additional CSS classes */
  className?: string
  /** Show line numbers (default: true) */
  showLineNumbers?: boolean
}

/**
 * CopyableCodeBlock Component
 *
 * Displays code with syntax highlighting and a copy-to-clipboard button.
 * Styled similar to ChatGPT/VS Code code blocks.
 *
 * @example
 * <CopyableCodeBlock
 *   code={JSON.stringify(blueprint, null, 2)}
 *   language="json"
 *   title="AppBlueprint"
 * />
 */
export function CopyableCodeBlock({
  code,
  language = 'json',
  title,
  maxHeight = '400px',
  className,
  showLineNumbers = true,
}: CopyableCodeBlockProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      // Reset after 2 seconds
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy to clipboard:', err)
    }
  }, [code])

  // Get appropriate icon based on language
  const getLanguageIcon = () => {
    switch (language) {
      case 'json':
        return <FileJson className="h-4 w-4" />
      default:
        return <FileCode className="h-4 w-4" />
    }
  }

  return (
    <div className={cn('rounded-lg border overflow-hidden', className)}>
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
              <span className="text-green-500">Đã copy</span>
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
        className="overflow-auto"
        style={{ maxHeight }}
      >
        <SyntaxHighlighter
          language={language}
          style={oneDark}
          showLineNumbers={showLineNumbers}
          customStyle={{
            margin: 0,
            borderRadius: 0,
            fontSize: '13px',
            lineHeight: '1.5',
          }}
          codeTagProps={{
            style: {
              fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace',
            },
          }}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  )
}

export default CopyableCodeBlock
