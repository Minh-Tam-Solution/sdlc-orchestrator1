/**
 * File: frontend/web/src/pages/ProjectDetailPage.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Project detail page showing project info and gates list.
 * Displays SDLC 4.9 stage progression with gate status.
 */

import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import DashboardLayout from '@/components/layout/DashboardLayout'
import CreateGateDialog from '@/components/gates/CreateGateDialog'
import apiClient from '@/api/client'
import type { GateStatusEnum } from '@/types/api'

interface ProjectGate {
  id: string
  gate_name: string
  gate_type: string
  stage: string
  status: GateStatusEnum
  description: string | null
  created_at: string | null
}

interface ProjectDetail {
  id: string
  name: string
  description: string | null
  current_stage: string
  created_at: string | null
  updated_at: string | null
  gates: ProjectGate[]
}

// SDLC 4.9 Stages
const SDLC_STAGES = [
  { code: '00', name: 'WHY', description: 'Problem Definition' },
  { code: '01', name: 'WHAT', description: 'Solution Planning' },
  { code: '02', name: 'HOW', description: 'Architecture & Design' },
  { code: '03', name: 'BUILD', description: 'Development' },
  { code: '04', name: 'VERIFY', description: 'Testing & QA' },
  { code: '05', name: 'SHIP', description: 'Release' },
  { code: '06', name: 'OPERATE', description: 'Production' },
  { code: '07', name: 'OBSERVE', description: 'Monitoring' },
  { code: '08', name: 'LEARN', description: 'Retrospective' },
  { code: '09', name: 'EVOLVE', description: 'Iteration' },
]

/**
 * Get status badge color
 */
function getStatusColor(status: GateStatusEnum): string {
  switch (status) {
    case 'APPROVED':
      return 'bg-green-100 text-green-700'
    case 'REJECTED':
      return 'bg-red-100 text-red-700'
    case 'PENDING_APPROVAL':
      return 'bg-yellow-100 text-yellow-700'
    case 'PENDING':
      return 'bg-blue-100 text-blue-700'
    default:
      return 'bg-gray-100 text-gray-700'
  }
}

/**
 * Project detail page component
 *
 * @returns Project detail with gates list
 */
export default function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [createGateDialogOpen, setCreateGateDialogOpen] = useState(false)

  // Fetch project detail
  const { data: project, isLoading, error } = useQuery<ProjectDetail>({
    queryKey: ['project', id],
    queryFn: async () => {
      const response = await apiClient.get<ProjectDetail>(`/projects/${id}`)
      return response.data
    },
    enabled: !!id,
  })

  // Group gates by stage
  const gatesByStage = project?.gates.reduce<Record<string, ProjectGate[]>>((acc, gate) => {
    const stageGates = acc[gate.stage] ?? []
    stageGates.push(gate)
    acc[gate.stage] = stageGates
    return acc
  }, {}) ?? {}

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center py-12">
          <div className="text-muted-foreground">Loading project...</div>
        </div>
      </DashboardLayout>
    )
  }

  if (error || !project) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center py-12">
          <div className="text-red-500 mb-4">Project not found</div>
          <Link to="/projects">
            <Button variant="outline">Back to Projects</Button>
          </Link>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Link to="/projects" className="hover:text-foreground">
            Projects
          </Link>
          <span>/</span>
          <span className="text-foreground">{project.name}</span>
        </div>

        {/* Project header */}
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">{project.name}</h1>
            <p className="text-muted-foreground mt-1">
              {project.description || 'No description'}
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline">Edit Project</Button>
            <Button onClick={() => setCreateGateDialogOpen(true)}>
              <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Add Gate
            </Button>
          </div>
        </div>

        {/* Create Gate Dialog */}
        {id && (
          <CreateGateDialog
            open={createGateDialogOpen}
            onOpenChange={setCreateGateDialogOpen}
            projectId={id}
          />
        )}

        {/* Project info */}
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Current Stage</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {SDLC_STAGES.find(s => s.code === project.current_stage)?.name || project.current_stage}
              </div>
              <p className="text-xs text-muted-foreground">
                {SDLC_STAGES.find(s => s.code === project.current_stage)?.description}
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Total Gates</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{project.gates.length}</div>
              <p className="text-xs text-muted-foreground">
                {project.gates.filter(g => g.status === 'APPROVED').length} approved
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Created</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {project.created_at ? new Date(project.created_at).toLocaleDateString() : 'N/A'}
              </div>
              <p className="text-xs text-muted-foreground">
                Updated {project.updated_at ? new Date(project.updated_at).toLocaleDateString() : 'N/A'}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* SDLC Stage Timeline */}
        <Card>
          <CardHeader>
            <CardTitle>SDLC 4.9 Stage Timeline</CardTitle>
            <CardDescription>Track progress through all 10 stages</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between overflow-x-auto pb-2">
              {SDLC_STAGES.map((stage, index) => {
                const stageGates = gatesByStage[stage.code] || []
                const hasGates = stageGates.length > 0
                const allApproved = stageGates.length > 0 && stageGates.every(g => g.status === 'APPROVED')
                const hasPending = stageGates.some(g => g.status === 'PENDING' || g.status === 'PENDING_APPROVAL')
                const hasRejected = stageGates.some(g => g.status === 'REJECTED')

                let stageColor = 'bg-gray-200'
                if (allApproved) stageColor = 'bg-green-500'
                else if (hasRejected) stageColor = 'bg-red-500'
                else if (hasPending) stageColor = 'bg-yellow-500'
                else if (hasGates) stageColor = 'bg-blue-500'

                return (
                  <div key={stage.code} className="flex flex-col items-center min-w-[80px]">
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold ${stageColor} ${
                        stageColor === 'bg-gray-200' ? 'text-gray-500' : 'text-white'
                      }`}
                    >
                      {stage.code}
                    </div>
                    <div className="mt-2 text-xs font-medium text-center">{stage.name}</div>
                    <div className="text-xs text-muted-foreground">
                      {stageGates.length > 0 ? `${stageGates.length} gate${stageGates.length > 1 ? 's' : ''}` : '-'}
                    </div>
                    {index < SDLC_STAGES.length - 1 && (
                      <div className="absolute h-0.5 w-8 bg-gray-200 left-full top-4" />
                    )}
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>

        {/* Gates list */}
        <Card>
          <CardHeader>
            <CardTitle>Quality Gates</CardTitle>
            <CardDescription>All gates for this project</CardDescription>
          </CardHeader>
          <CardContent>
            {project.gates.length > 0 ? (
              <div className="space-y-4">
                {project.gates.map((gate) => (
                  <Link
                    key={gate.id}
                    to={`/gates/${gate.id}`}
                    className="block"
                  >
                    <div className="flex items-center justify-between rounded-lg border p-4 hover:bg-muted transition-colors">
                      <div className="flex items-center gap-4">
                        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-primary font-bold">
                          {gate.stage}
                        </div>
                        <div>
                          <p className="font-medium">{gate.gate_name}</p>
                          <p className="text-sm text-muted-foreground">
                            {gate.gate_type} • {SDLC_STAGES.find(s => s.code === gate.stage)?.name}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <span
                          className={`rounded-full px-3 py-1 text-xs font-medium ${getStatusColor(gate.status)}`}
                        >
                          {gate.status}
                        </span>
                        <svg className="h-5 w-5 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-8">
                <svg
                  className="h-12 w-12 text-muted-foreground mb-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                  />
                </svg>
                <h3 className="text-lg font-medium">No gates yet</h3>
                <p className="text-muted-foreground text-center mt-1">
                  Create your first quality gate to start tracking progress
                </p>
                <Button className="mt-4" onClick={() => setCreateGateDialogOpen(true)}>
                  <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  Create Gate
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}
