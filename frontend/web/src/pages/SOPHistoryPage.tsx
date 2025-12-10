/**
 * File: frontend/web/src/pages/SOPHistoryPage.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Phase 2-Pilot Week 4 (SE 3.0 Track 1)
 * Date: 2025-01-13
 * Authority: Frontend Lead + CTO Approved
 * Foundation: BRS-PILOT-001, SDLC 5.1.0 Framework
 *
 * Description:
 * SOP History page for viewing all generated SOPs.
 * Includes filtering, pagination, and links to SOP details/MRP evidence.
 *
 * M4 Milestone: MRP Working
 */

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import DashboardLayout from '@/components/layout/DashboardLayout'
import apiClient from '@/api/client'

// ============================================================================
// Types
// ============================================================================

interface SOPListItem {
  sop_id: string
  sop_type: string
  title: string
  status: string
  created_at: string
  completeness_score: number
  has_vcr: boolean
}

interface SOPListResponse {
  items: SOPListItem[]
  total: number
  page: number
  page_size: number
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

const STATUS_VARIANTS: Record<string, 'default' | 'secondary' | 'destructive' | 'outline'> = {
  draft: 'secondary',
  pending_review: 'outline',
  approved: 'default',
  rejected: 'destructive',
  revision_required: 'outline',
}

// ============================================================================
// Main Component
// ============================================================================

export default function SOPHistoryPage() {
  // Filter state
  const [page, setPage] = useState(1)
  const [typeFilter, setTypeFilter] = useState<string>('all')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const pageSize = 20

  // Fetch SOP list
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['sop-list', page, typeFilter, statusFilter],
    queryFn: async () => {
      const params = new URLSearchParams()
      params.append('page', page.toString())
      params.append('page_size', pageSize.toString())
      if (typeFilter !== 'all') params.append('sop_type', typeFilter)
      if (statusFilter !== 'all') params.append('status', statusFilter)

      const response = await apiClient.get<SOPListResponse>(`/sop/list?${params}`)
      return response.data
    },
  })

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

  // Calculate total pages
  const totalPages = data ? Math.ceil(data.total / pageSize) : 0

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">SOP History</h1>
            <p className="text-muted-foreground">
              View all generated SOPs and their MRP evidence (M4)
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="gap-1">
              <span>📊</span>
              {data?.total || 0} SOPs
            </Badge>
            <Link to="/sop-generator">
              <Button>
                <span className="mr-2">➕</span>
                Generate New SOP
              </Button>
            </Link>
          </div>
        </div>

        {/* Filters */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">Filters</CardTitle>
          </CardHeader>
          <CardContent className="flex gap-4">
            <div className="w-48">
              <Select
                value={typeFilter}
                onValueChange={(value) => {
                  setTypeFilter(value)
                  setPage(1)
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="SOP Type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Types</SelectItem>
                  <SelectItem value="deployment">🚀 Deployment</SelectItem>
                  <SelectItem value="incident">🚨 Incident</SelectItem>
                  <SelectItem value="change">📋 Change</SelectItem>
                  <SelectItem value="backup">💾 Backup</SelectItem>
                  <SelectItem value="security">🔒 Security</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="w-48">
              <Select
                value={statusFilter}
                onValueChange={(value) => {
                  setStatusFilter(value)
                  setPage(1)
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="draft">Draft</SelectItem>
                  <SelectItem value="pending_review">Pending Review</SelectItem>
                  <SelectItem value="approved">Approved</SelectItem>
                  <SelectItem value="rejected">Rejected</SelectItem>
                  <SelectItem value="revision_required">Revision Required</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button variant="outline" onClick={() => refetch()}>
              <span className="mr-2">🔄</span>
              Refresh
            </Button>
          </CardContent>
        </Card>

        {/* SOP Table */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <span>📋</span>
              Generated SOPs
            </CardTitle>
            <CardDescription>
              Click on an SOP to view details and MRP evidence
            </CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin text-4xl">⚙️</div>
              </div>
            ) : error ? (
              <div className="flex items-center justify-center h-64 text-destructive">
                <div className="text-center">
                  <div className="text-4xl mb-2">❌</div>
                  <p>Failed to load SOPs</p>
                  <Button variant="outline" onClick={() => refetch()} className="mt-4">
                    Try Again
                  </Button>
                </div>
              </div>
            ) : data?.items.length === 0 ? (
              <div className="flex items-center justify-center h-64 text-muted-foreground">
                <div className="text-center">
                  <div className="text-4xl mb-4">📝</div>
                  <p>No SOPs generated yet</p>
                  <Link to="/sop-generator">
                    <Button className="mt-4">Generate Your First SOP</Button>
                  </Link>
                </div>
              </div>
            ) : (
              <>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-12">Type</TableHead>
                      <TableHead>SOP ID</TableHead>
                      <TableHead>Title</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead className="text-center">Completeness</TableHead>
                      <TableHead className="text-center">VCR</TableHead>
                      <TableHead>Created</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {data?.items.map((sop) => (
                      <TableRow key={sop.sop_id}>
                        <TableCell className="text-center text-lg">
                          {SOP_TYPE_ICONS[sop.sop_type] || '📄'}
                        </TableCell>
                        <TableCell className="font-mono text-xs">
                          {sop.sop_id}
                        </TableCell>
                        <TableCell className="font-medium max-w-xs truncate">
                          {sop.title}
                        </TableCell>
                        <TableCell>
                          <Badge variant={STATUS_VARIANTS[sop.status] || 'secondary'}>
                            {sop.status.replace('_', ' ')}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-center">
                          <span
                            className={
                              sop.completeness_score >= 80
                                ? 'text-green-600'
                                : 'text-amber-600'
                            }
                          >
                            {sop.completeness_score.toFixed(0)}%
                          </span>
                        </TableCell>
                        <TableCell className="text-center">
                          {sop.has_vcr ? (
                            <Badge variant="default">✓</Badge>
                          ) : (
                            <Badge variant="outline">-</Badge>
                          )}
                        </TableCell>
                        <TableCell className="text-sm text-muted-foreground">
                          {formatDate(sop.created_at)}
                        </TableCell>
                        <TableCell className="text-right">
                          <div className="flex justify-end gap-2">
                            <Link to={`/sop/${sop.sop_id}`}>
                              <Button variant="outline" size="sm">
                                View
                              </Button>
                            </Link>
                            <Link to={`/sop/${sop.sop_id}/mrp`}>
                              <Button variant="outline" size="sm">
                                📊 MRP
                              </Button>
                            </Link>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="flex items-center justify-between mt-4 pt-4 border-t">
                    <p className="text-sm text-muted-foreground">
                      Showing {(page - 1) * pageSize + 1} to{' '}
                      {Math.min(page * pageSize, data.total)} of {data.total} SOPs
                    </p>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        disabled={page === 1}
                        onClick={() => setPage(page - 1)}
                      >
                        ← Previous
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        disabled={page === totalPages}
                        onClick={() => setPage(page + 1)}
                      >
                        Next →
                      </Button>
                    </div>
                  </div>
                )}
              </>
            )}
          </CardContent>
        </Card>

        {/* Info Card */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">SASE Level 1 Workflow</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-center gap-8 text-sm">
              <div className="text-center">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-1">
                  📝
                </div>
                <p className="font-medium">BRS</p>
                <p className="text-xs text-muted-foreground">Requirements</p>
              </div>
              <div className="text-muted-foreground">→</div>
              <div className="text-center">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-1">
                  🤖
                </div>
                <p className="font-medium">Generate</p>
                <p className="text-xs text-muted-foreground">AI creates SOP</p>
              </div>
              <div className="text-muted-foreground">→</div>
              <div className="text-center">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-1">
                  📊
                </div>
                <p className="font-medium">MRP</p>
                <p className="text-xs text-muted-foreground">Evidence Pack</p>
              </div>
              <div className="text-muted-foreground">→</div>
              <div className="text-center">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-1">
                  ✅
                </div>
                <p className="font-medium">VCR</p>
                <p className="text-xs text-muted-foreground">Human Review</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}
