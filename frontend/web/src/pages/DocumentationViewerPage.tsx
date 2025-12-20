/**
 * File: frontend/web/src/pages/DocumentationViewerPage.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 04 (BUILD)
 * Date: 2025-12-20
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 5.1.1 Complete Lifecycle
 *
 * Description:
 * Documentation viewer page for rendering user support markdown files.
 * Similar to SOPDetailPage markdown rendering approach.
 */

import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from 'react-router-dom'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import DashboardLayout from '@/components/layout/DashboardLayout'
import { ArrowLeft, Download, BookOpen } from 'lucide-react'
import apiClient from '@/api/client'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

/**
 * Markdown renderer component using react-markdown with GitHub Flavored Markdown
 */
function MarkdownContent({ content }: { content: string }) {
  return (
    <div className="prose prose-sm max-w-none dark:prose-invert">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Custom heading styles
          h1: ({ node, ...props }) => (
            <h1 className="text-2xl font-bold mt-6 mb-4 border-b pb-2" {...props} />
          ),
          h2: ({ node, ...props }) => (
            <h2 className="text-xl font-semibold mt-5 mb-3 border-b pb-2" {...props} />
          ),
          h3: ({ node, ...props }) => (
            <h3 className="text-lg font-medium mt-4 mb-2" {...props} />
          ),
          h4: ({ node, ...props }) => (
            <h4 className="text-base font-medium mt-3 mb-2" {...props} />
          ),
          // Custom list styles
          ul: ({ node, ...props }) => (
            <ul className="list-disc ml-6 my-3 space-y-1" {...props} />
          ),
          ol: ({ node, ...props }) => (
            <ol className="list-decimal ml-6 my-3 space-y-1" {...props} />
          ),
          li: ({ node, ...props }) => (
            <li className="my-1" {...props} />
          ),
          // Custom table styles
          table: ({ node, ...props }) => (
            <div className="overflow-x-auto my-4">
              <table className="min-w-full border-collapse border border-border" {...props} />
            </div>
          ),
          thead: ({ node, ...props }) => (
            <thead className="bg-muted" {...props} />
          ),
          th: ({ node, ...props }) => (
            <th className="border border-border px-3 py-2 text-left font-semibold" {...props} />
          ),
          td: ({ node, ...props }) => (
            <td className="border border-border px-3 py-2" {...props} />
          ),
          // Custom code block styles
          code: ({ node, className, children, ...props }) => {
            const isInline = !className
            return isInline ? (
              <code className="bg-muted px-1.5 py-0.5 rounded text-sm font-mono" {...props}>
                {children}
              </code>
            ) : (
              <code className={`block bg-muted p-3 rounded-md font-mono text-sm my-2 overflow-x-auto ${className || ''}`} {...props}>
                {children}
              </code>
            )
          },
          pre: ({ node, ...props }) => (
            <pre className="bg-muted p-3 rounded-md overflow-x-auto my-3" {...props} />
          ),
          // Custom paragraph styles
          p: ({ node, ...props }) => (
            <p className="my-2 leading-relaxed" {...props} />
          ),
          // Custom blockquote styles
          blockquote: ({ node, ...props }) => (
            <blockquote className="border-l-4 border-primary pl-4 italic my-3 text-muted-foreground" {...props} />
          ),
          // Custom link styles
          a: ({ node, ...props }) => (
            <a className="text-primary hover:underline" target="_blank" rel="noopener noreferrer" {...props} />
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}

/**
 * Documentation viewer page
 */
export default function DocumentationViewerPage() {
  const { filename } = useParams<{ filename: string }>()

  // Fetch documentation content
  const { data: content, isLoading, error } = useQuery<string>({
    queryKey: ['documentation', filename],
    queryFn: async () => {
      const response = await apiClient.get(`/docs/user-support/${filename}`, {
        responseType: 'text'
      })
      return response.data
    },
    enabled: !!filename
  })

  // Download handler
  const handleDownload = () => {
    if (!content || !filename) return
    
    const blob = new Blob([content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  // Get document title from filename
  const getTitle = () => {
    if (!filename) return 'Documentation'
    return filename.replace('.md', '').replace(/-/g, ' ')
  }

  return (
    <DashboardLayout>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link to="/support">
              <Button variant="outline" size="sm">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Support
              </Button>
            </Link>
            <div className="flex items-center gap-3">
              <BookOpen className="h-6 w-6 text-primary" />
              <div>
                <h1 className="text-2xl font-bold">{getTitle()}</h1>
                <Badge variant="secondary" className="mt-1">
                  User Documentation
                </Badge>
              </div>
            </div>
          </div>
          <Button variant="outline" size="sm" onClick={handleDownload} disabled={!content}>
            <Download className="h-4 w-4 mr-2" />
            Download
          </Button>
        </div>

        {/* Content */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">
                  SDLC Orchestrator User Support
                </p>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {isLoading && (
              <div className="flex items-center justify-center py-12">
                <div className="flex flex-col items-center gap-4">
                  <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
                  <p className="text-sm text-muted-foreground">Loading documentation...</p>
                </div>
              </div>
            )}

            {error && (
              <div className="text-center py-12">
                <p className="text-red-600 mb-2">Failed to load documentation</p>
                <p className="text-sm text-muted-foreground">
                  {error instanceof Error ? error.message : 'Unknown error occurred'}
                </p>
              </div>
            )}

            {content && !isLoading && !error && (
              <div className="markdown-content">
                <MarkdownContent content={content} />
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}
