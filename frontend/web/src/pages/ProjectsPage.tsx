/**
 * File: frontend/web/src/pages/ProjectsPage.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Projects list page showing all SDLC projects with their gate status.
 */

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import DashboardLayout from '@/components/layout/DashboardLayout'
import CreateProjectDialog from '@/components/projects/CreateProjectDialog'
import apiClient from '@/api/client'

interface Project {
  id: string
  name: string
  description: string
  current_stage: string
  gate_status: 'passed' | 'failed' | 'pending' | 'not_started'
  progress: number
  created_at: string
  updated_at: string
}

/**
 * Projects page component
 *
 * @returns Projects list with gate status
 */
export default function ProjectsPage() {
  const [createDialogOpen, setCreateDialogOpen] = useState(false)

  // Fetch projects
  const { data: projects, isLoading } = useQuery<Project[]>({
    queryKey: ['projects'],
    queryFn: async () => {
      try {
        const response = await apiClient.get<Project[]>('/projects')
        return response.data
      } catch {
        // Return empty array if API not available yet
        return []
      }
    },
  })

  const getStatusColor = (status: Project['gate_status']) => {
    switch (status) {
      case 'passed':
        return 'bg-green-100 text-green-700'
      case 'failed':
        return 'bg-red-100 text-red-700'
      case 'pending':
        return 'bg-yellow-100 text-yellow-700'
      default:
        return 'bg-gray-100 text-gray-700'
    }
  }

  const getStageLabel = (stage: string) => {
    const stages: Record<string, string> = {
      '00': 'WHY - Foundation',
      '01': 'WHAT - Planning',
      '02': 'HOW - Design',
      '03': 'BUILD - Development',
      '04': 'VERIFY - Testing',
      '05': 'LAUNCH - Deployment',
      '06': 'OPERATE - Maintenance',
      '07': 'OPTIMIZE - Improvement',
      '08': 'SUNSET - End of Life',
      '09': 'ARCHIVE - Documentation',
    }
    return stages[stage] || stage
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Projects</h1>
            <p className="text-muted-foreground">
              Manage your SDLC projects and track gate progress
            </p>
          </div>
          <Button onClick={() => setCreateDialogOpen(true)}>
            <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Project
          </Button>
        </div>

        {/* Create Project Dialog */}
        <CreateProjectDialog
          open={createDialogOpen}
          onOpenChange={setCreateDialogOpen}
        />

        {/* Projects grid */}
        {isLoading ? (
          <div className="text-center text-muted-foreground py-12">Loading projects...</div>
        ) : projects && projects.length > 0 ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {projects.map((project) => (
              <Link key={project.id} to={`/projects/${project.id}`}>
                <Card className="h-full hover:shadow-md transition-shadow cursor-pointer">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="text-lg">{project.name}</CardTitle>
                        <CardDescription className="mt-1 line-clamp-2">
                          {project.description}
                        </CardDescription>
                      </div>
                      <span
                        className={`rounded-full px-2 py-1 text-xs font-medium ${getStatusColor(
                          project.gate_status
                        )}`}
                      >
                        {project.gate_status}
                      </span>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {/* Current stage */}
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">Current Stage</span>
                        <span className="font-medium">{getStageLabel(project.current_stage)}</span>
                      </div>

                      {/* Progress bar */}
                      <div className="space-y-1">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-muted-foreground">Progress</span>
                          <span className="font-medium">{project.progress}%</span>
                        </div>
                        <div className="h-2 w-full rounded-full bg-muted">
                          <div
                            className="h-2 rounded-full bg-primary transition-all"
                            style={{ width: `${project.progress}%` }}
                          />
                        </div>
                      </div>

                      {/* Updated at */}
                      <div className="text-xs text-muted-foreground">
                        Updated {new Date(project.updated_at).toLocaleDateString()}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
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
                  d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
                />
              </svg>
              <h3 className="text-lg font-medium">No projects yet</h3>
              <p className="text-muted-foreground text-center mt-1">
                Get started by creating your first SDLC project
              </p>
              <Button className="mt-4" onClick={() => setCreateDialogOpen(true)}>
                <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Create Project
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  )
}
