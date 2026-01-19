/**
 * File: frontend/web/src/pages/SOPDetailPage.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Phase 2-Pilot Week 4 (SE 3.0 Track 1)
 * Date: 2025-01-13
 * Authority: Frontend Lead + CTO Approved
 * Foundation: BRS-PILOT-001, SDLC 5.1.0 Framework
 *
 * Description:
 * SOP Detail page for viewing a single SOP with full content.
 * Includes MRP evidence, VCR submission, and download functionality.
 *
 * M4 Milestone: MRP Working
 */

import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import DashboardLayout from '@/components/layout/DashboardLayout'
import apiClient from '@/api/client'

// ============================================================================
// Types
// ============================================================================

interface GeneratedSOPResponse {
  sop_id: string
  sop_type: string
  title: string
  version: string
  status: string
  created_at: string
  purpose: string
  scope: string
  procedure: string
  roles: string
  quality_criteria: string
  markdown_content: string
  sha256_hash: string
  generation_time_ms: number
  ai_model: string
  mrp_id: string
  completeness_score: number
}

interface MRPResponse {
  mrp_id: string
  brs_id: string
  sop_id: string
  created_at: string
  sop_type: string
  template_used: string
  generation_time_ms: number
  ai_model: string
  ai_provider: string
  sections_present: number
  sections_required: number
  completeness_score: number
  sha256_hash: string
  status: string
}

interface VCRResponse {
  vcr_id: string
  sop_id: string
  mrp_id: string
  decision: string
  reviewer: string
  reviewed_at: string
  comments: string | null
  quality_rating: number | null
  status: string
}

// ============================================================================
// Constants
// ============================================================================

const SOP_TYPE_ICONS: Record<string, string> = {
  deployment: '🚀',
  incident: '🚨',
  change: '📋',
  backup: '💾',
  security: '🔒',
}

const STATUS_COLORS: Record<string, string> = {
  draft: 'bg-gray-100 text-gray-800',
  pending_review: 'bg-amber-100 text-amber-800',
  approved: 'bg-green-100 text-green-800',
  rejected: 'bg-red-100 text-red-800',
  revision_required: 'bg-orange-100 text-orange-800',
}

// ============================================================================
// Markdown Renderer Component
// ============================================================================

function MarkdownContent({ content }: { content: string }) {
  const renderMarkdown = (md: string) => {
    return md.split('\n').map((line, index) => {
      if (line.startsWith('# ')) {
        return (
          <h1 key={index} className="text-2xl font-bold mt-6 mb-4">
            {line.slice(2)}
          </h1>
        )
      }
      if (line.startsWith('## ')) {
        return (
          <h2 key={index} className="text-xl font-semibold mt-5 mb-3 border-b pb-2">
            {line.slice(3)}
          </h2>
        )
      }
      if (line.startsWith('### ')) {
        return (
          <h3 key={index} className="text-lg font-medium mt-4 mb-2">
            {line.slice(4)}
          </h3>
        )
      }
      if (line.startsWith('- ')) {
        return (
          <li key={index} className="ml-6 list-disc">
            {line.slice(2)}
          </li>
        )
      }
      if (line.match(/^\d+\.\s/)) {
        return (
          <li key={index} className="ml-6 list-decimal">
            {line.replace(/^\d+\.\s/, '')}
          </li>
        )
      }
      if (line.startsWith('- [ ]')) {
        return (
          <div key={index} className="ml-6 flex items-center gap-2">
            <input type="checkbox" className="rounded" disabled />
            <span>{line.slice(6)}</span>
          </div>
        )
      }
      if (line.startsWith('- [x]')) {
        return (
          <div key={index} className="ml-6 flex items-center gap-2">
            <input type="checkbox" className="rounded" checked disabled />
            <span className="line-through text-muted-foreground">{line.slice(6)}</span>
          </div>
        )
      }
      if (line.includes('**')) {
        const parts = line.split(/\*\*(.*?)\*\*/g)
        return (
          <p key={index} className="my-1">
            {parts.map((part, i) => (i % 2 === 1 ? <strong key={i}>{part}</strong> : part))}
          </p>
        )
      }
      if (line.startsWith('|')) {
        const cells = line.split('|').filter((c) => c.trim())
        if (line.includes('---')) return null
        return (
          <tr key={index} className="border-b">
            {cells.map((cell, i) => (
              <td key={i} className="px-3 py-2 text-sm">
                {cell.trim()}
              </td>
            ))}
          </tr>
        )
      }
      if (!line.trim()) {
        return <div key={index} className="h-2" />
      }
      return (
        <p key={index} className="my-1">
          {line}
        </p>
      )
    })
  }

  return (
    <div className="prose prose-sm max-w-none dark:prose-invert">{renderMarkdown(content)}</div>
  )
}

// ============================================================================
// Main Component
// ============================================================================

export default function SOPDetailPage() {
  const { sopId } = useParams<{ sopId: string }>()
  const queryClient = useQueryClient()

  // VCR form state
  const [vcrDecision, setVcrDecision] = useState<string>('')
  const [vcrReviewer, setVcrReviewer] = useState('')
  const [vcrComments, setVcrComments] = useState('')
  const [vcrRating, setVcrRating] = useState<string>('')

  // Fetch SOP details
  const {
    data: sop,
    isLoading: sopLoading,
    error: sopError,
  } = useQuery({
    queryKey: ['sop', sopId],
    queryFn: async () => {
      const response = await apiClient.get<GeneratedSOPResponse>(`/sop/${sopId}`)
      return response.data
    },
    enabled: !!sopId,
  })

  // Fetch MRP evidence
  const { data: mrp, isLoading: mrpLoading } = useQuery({
    queryKey: ['mrp', sopId],
    queryFn: async () => {
      const response = await apiClient.get<MRPResponse>(`/sop/${sopId}/mrp`)
      return response.data
    },
    enabled: !!sopId,
  })

  // Fetch VCR if exists
  const { data: vcr } = useQuery({
    queryKey: ['vcr', sopId],
    queryFn: async () => {
      try {
        const response = await apiClient.get<VCRResponse>(`/sop/${sopId}/vcr`)
        return response.data
      } catch {
        return null
      }
    },
    enabled: !!sopId,
  })

  // Submit VCR mutation
  const submitVcrMutation = useMutation({
    mutationFn: async () => {
      const response = await apiClient.post<VCRResponse>(`/sop/${sopId}/vcr`, {
        decision: vcrDecision,
        reviewer: vcrReviewer,
        comments: vcrComments || null,
        quality_rating: vcrRating ? parseInt(vcrRating) : null,
      })
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vcr', sopId] })
      queryClient.invalidateQueries({ queryKey: ['sop', sopId] })
      queryClient.invalidateQueries({ queryKey: ['sop-list'] })
    },
  })

  // Handle download
  const handleDownload = () => {
    if (!sop) return

    const blob = new Blob([sop.markdown_content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${sop.sop_id}.md`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  // Format date
  const formatDate = (isoString: string) => {
    const date = new Date(isoString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  if (sopLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin text-4xl">⚙️</div>
        </div>
      </DashboardLayout>
    )
  }

  if (sopError || !sop) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="text-4xl mb-4">❌</div>
            <p className="text-lg font-medium mb-2">SOP Not Found</p>
            <p className="text-muted-foreground mb-4">The requested SOP does not exist.</p>
            <Link to="/sop-history">
              <Button>Back to SOP History</Button>
            </Link>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-3xl">{SOP_TYPE_ICONS[sop.sop_type] || '📄'}</span>
              <h1 className="text-2xl font-bold tracking-tight">{sop.title}</h1>
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span className="font-mono">{sop.sop_id}</span>
              <span>•</span>
              <span>v{sop.version}</span>
              <span>•</span>
              <Badge className={STATUS_COLORS[sop.status]}>{sop.status.replace('_', ' ')}</Badge>
            </div>
          </div>
          <div className="flex gap-2">
            <Link to="/sop-history">
              <Button variant="outline">
                <span className="mr-2">←</span>
                Back
              </Button>
            </Link>
            <Button variant="outline" onClick={handleDownload}>
              <span className="mr-2">⬇️</span>
              Download .md
            </Button>
          </div>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="content" className="space-y-4">
          <TabsList>
            <TabsTrigger value="content">📄 SOP Content</TabsTrigger>
            <TabsTrigger value="mrp">📊 MRP Evidence</TabsTrigger>
            <TabsTrigger value="vcr">✅ VCR Review</TabsTrigger>
          </TabsList>

          {/* SOP Content Tab */}
          <TabsContent value="content">
            <Card>
              <CardHeader>
                <CardTitle>Generated SOP</CardTitle>
                <CardDescription>
                  Generated on {formatDate(sop.created_at)} using {sop.ai_model}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-[600px] pr-4">
                  <MarkdownContent content={sop.markdown_content} />
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>

          {/* MRP Evidence Tab */}
          <TabsContent value="mrp">
            {mrpLoading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin text-4xl">⚙️</div>
              </div>
            ) : mrp ? (
              <div className="grid gap-4 md:grid-cols-2">
                {/* MRP Overview */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <span>📊</span>
                      MRP Overview
                    </CardTitle>
                    <CardDescription>Merge-Readiness Pack evidence (FR6)</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label className="text-muted-foreground">MRP ID</Label>
                        <p className="font-mono text-sm">{mrp.mrp_id}</p>
                      </div>
                      <div>
                        <Label className="text-muted-foreground">BRS Reference</Label>
                        <p className="font-mono text-sm">{mrp.brs_id}</p>
                      </div>
                      <div>
                        <Label className="text-muted-foreground">Created</Label>
                        <p className="text-sm">{formatDate(mrp.created_at)}</p>
                      </div>
                      <div>
                        <Label className="text-muted-foreground">Status</Label>
                        <Badge variant="outline">{mrp.status}</Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Generation Metrics */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <span>⚡</span>
                      Generation Metrics
                    </CardTitle>
                    <CardDescription>AI generation performance (NFR1)</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label className="text-muted-foreground">AI Provider</Label>
                        <p className="text-sm capitalize">{mrp.ai_provider}</p>
                      </div>
                      <div>
                        <Label className="text-muted-foreground">AI Model</Label>
                        <p className="font-mono text-sm">{mrp.ai_model}</p>
                      </div>
                      <div>
                        <Label className="text-muted-foreground">Generation Time</Label>
                        <p className="text-sm">
                          {(mrp.generation_time_ms / 1000).toFixed(1)}s
                          {mrp.generation_time_ms < 30000 && (
                            <Badge variant="outline" className="ml-2 text-green-600">
                              ✓ NFR1
                            </Badge>
                          )}
                        </p>
                      </div>
                      <div>
                        <Label className="text-muted-foreground">Template</Label>
                        <p className="text-sm">{mrp.template_used}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Quality Metrics */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <span>📋</span>
                      Quality Metrics
                    </CardTitle>
                    <CardDescription>Section completeness (FR2)</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Completeness Score</span>
                      <div className="flex items-center gap-2">
                        <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div
                            className={`h-full ${
                              mrp.completeness_score >= 80 ? 'bg-green-500' : 'bg-amber-500'
                            }`}
                            style={{ width: `${mrp.completeness_score}%` }}
                          />
                        </div>
                        <span
                          className={
                            mrp.completeness_score >= 80 ? 'text-green-600' : 'text-amber-600'
                          }
                        >
                          {mrp.completeness_score.toFixed(0)}%
                        </span>
                      </div>
                    </div>
                    <div>
                      <Label className="text-muted-foreground">Sections</Label>
                      <p className="text-sm">
                        {mrp.sections_present} of {mrp.sections_required} required sections present
                      </p>
                    </div>
                    <div className="text-xs text-muted-foreground">
                      <strong>Required:</strong> Purpose, Scope, Procedure, Roles, Quality Criteria
                    </div>
                  </CardContent>
                </Card>

                {/* Integrity */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <span>🔒</span>
                      Integrity
                    </CardTitle>
                    <CardDescription>SHA256 hash verification (FR5)</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div>
                      <Label className="text-muted-foreground">SHA256 Hash</Label>
                      <p className="font-mono text-xs break-all mt-1 p-2 bg-muted rounded">
                        {mrp.sha256_hash}
                      </p>
                    </div>
                    <p className="text-xs text-muted-foreground mt-2">
                      This hash can be used to verify the SOP content has not been modified.
                    </p>
                  </CardContent>
                </Card>
              </div>
            ) : (
              <Card>
                <CardContent className="flex items-center justify-center h-64">
                  <div className="text-center text-muted-foreground">
                    <div className="text-4xl mb-2">📊</div>
                    <p>No MRP evidence found</p>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* VCR Review Tab */}
          <TabsContent value="vcr">
            <div className="grid gap-4 md:grid-cols-2">
              {/* Existing VCR */}
              {vcr ? (
                <Card className="md:col-span-2">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <span>✅</span>
                      VCR Decision Recorded
                    </CardTitle>
                    <CardDescription>Reviewed by {vcr.reviewer}</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div>
                        <Label className="text-muted-foreground">VCR ID</Label>
                        <p className="font-mono text-sm">{vcr.vcr_id}</p>
                      </div>
                      <div>
                        <Label className="text-muted-foreground">Decision</Label>
                        <Badge
                          variant={vcr.decision === 'approved' ? 'default' : 'destructive'}
                          className="mt-1"
                        >
                          {vcr.decision.replace('_', ' ')}
                        </Badge>
                      </div>
                      <div>
                        <Label className="text-muted-foreground">Reviewed At</Label>
                        <p className="text-sm">{formatDate(vcr.reviewed_at)}</p>
                      </div>
                      <div>
                        <Label className="text-muted-foreground">Quality Rating</Label>
                        <p className="text-sm">
                          {vcr.quality_rating ? `${vcr.quality_rating}/5` : 'Not rated'}
                        </p>
                      </div>
                    </div>
                    {vcr.comments && (
                      <div>
                        <Label className="text-muted-foreground">Comments</Label>
                        <p className="text-sm mt-1 p-3 bg-muted rounded">{vcr.comments}</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ) : (
                <>
                  {/* VCR Form */}
                  <Card className="md:col-span-2">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <span>📝</span>
                        Submit VCR Decision
                      </CardTitle>
                      <CardDescription>
                        Review and approve/reject this SOP (FR7)
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="reviewer">Reviewer Name *</Label>
                          <Input
                            id="reviewer"
                            placeholder="Enter your name"
                            value={vcrReviewer}
                            onChange={(e) => setVcrReviewer(e.target.value)}
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="decision">Decision *</Label>
                          <Select value={vcrDecision} onValueChange={setVcrDecision}>
                            <SelectTrigger>
                              <SelectValue placeholder="Select decision" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="approved">✅ Approved</SelectItem>
                              <SelectItem value="rejected">❌ Rejected</SelectItem>
                              <SelectItem value="revision_required">
                                🔄 Revision Required
                              </SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="rating">Quality Rating (Optional)</Label>
                          <Select value={vcrRating} onValueChange={setVcrRating}>
                            <SelectTrigger>
                              <SelectValue placeholder="Select rating" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="5">⭐⭐⭐⭐⭐ (5 - Excellent)</SelectItem>
                              <SelectItem value="4">⭐⭐⭐⭐ (4 - Good)</SelectItem>
                              <SelectItem value="3">⭐⭐⭐ (3 - Acceptable)</SelectItem>
                              <SelectItem value="2">⭐⭐ (2 - Poor)</SelectItem>
                              <SelectItem value="1">⭐ (1 - Unacceptable)</SelectItem>
                            </SelectContent>
                          </Select>
                          <p className="text-xs text-muted-foreground">NFR2: Target ≥4</p>
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="comments">Comments (Optional)</Label>
                          <Textarea
                            id="comments"
                            placeholder="Add review comments..."
                            value={vcrComments}
                            onChange={(e) => setVcrComments(e.target.value)}
                            className="h-20"
                          />
                        </div>
                      </div>
                      <div className="flex justify-end gap-2">
                        <Button
                          onClick={() => submitVcrMutation.mutate()}
                          disabled={
                            !vcrReviewer || !vcrDecision || submitVcrMutation.isPending
                          }
                        >
                          {submitVcrMutation.isPending ? (
                            <>
                              <span className="animate-spin mr-2">⚙️</span>
                              Submitting...
                            </>
                          ) : (
                            <>
                              <span className="mr-2">✅</span>
                              Submit VCR Decision
                            </>
                          )}
                        </Button>
                      </div>
                      {submitVcrMutation.isError && (
                        <div className="p-3 bg-destructive/10 text-destructive rounded text-sm">
                          Failed to submit VCR. Please try again.
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  )
}
