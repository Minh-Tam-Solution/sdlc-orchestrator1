/**
 * File: frontend/web/src/pages/GatesPage.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Gates list page showing all quality gates across projects.
 */

import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import DashboardLayout from '@/components/layout/DashboardLayout'
import apiClient from '@/api/client'

interface Gate {
  id: string
  name: string
  project_id: string
  project_name: string
  stage: string
  status: 'pending' | 'approved' | 'rejected' | 'in_review'
  created_at: string
  updated_at: string
}

/**
 * Gates page component
 *
 * @returns Gates list with status
 */
export default function GatesPage() {
  // Fetch gates
  const { data: gates, isLoading } = useQuery<Gate[]>({
    queryKey: ['gates'],
    queryFn: async () => {
      try {
        const response = await apiClient.get<Gate[]>('/gates')
        return response.data
      } catch {
        // Return empty array if API not available yet
        return []
      }
    },
  })

  const getStatusColor = (status: Gate['status']) => {
    switch (status) {
      case 'approved':
        return 'bg-green-100 text-green-700'
      case 'rejected':
        return 'bg-red-100 text-red-700'
      case 'in_review':
        return 'bg-blue-100 text-blue-700'
      default:
        return 'bg-yellow-100 text-yellow-700'
    }
  }

  const getStageLabel = (stage: string) => {
    const stages: Record<string, string> = {
      'G0': 'G0 - Problem Definition',
      'G1': 'G1 - Solution Validation',
      'G2': 'G2 - Design Ready',
      'G3': 'G3 - Ship Ready',
      'G4': 'G4 - Launch Ready',
      'G5': 'G5 - Operate Ready',
      'G6': 'G6 - Optimize Ready',
    }
    return stages[stage] || stage
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Gates</h1>
            <p className="text-muted-foreground">
              Review and approve quality gates across all projects
            </p>
          </div>
        </div>

        {/* Gates list */}
        {isLoading ? (
          <div className="text-center text-muted-foreground py-12">Loading gates...</div>
        ) : gates && gates.length > 0 ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {gates.map((gate) => (
              <Link key={gate.id} to={`/gates/${gate.id}`}>
                <Card className="h-full hover:shadow-md transition-shadow cursor-pointer">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="text-lg">{gate.name}</CardTitle>
                        <CardDescription className="mt-1">
                          {gate.project_name}
                        </CardDescription>
                      </div>
                      <span
                        className={`rounded-full px-2 py-1 text-xs font-medium ${getStatusColor(
                          gate.status
                        )}`}
                      >
                        {gate.status}
                      </span>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {/* Stage */}
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">Stage</span>
                        <span className="font-medium">{getStageLabel(gate.stage)}</span>
                      </div>

                      {/* Updated at */}
                      <div className="text-xs text-muted-foreground">
                        Updated {new Date(gate.updated_at).toLocaleDateString()}
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
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <h3 className="text-lg font-medium">No gates yet</h3>
              <p className="text-muted-foreground text-center mt-1">
                Gates will appear here when projects reach quality checkpoints
              </p>
              <Link to="/projects">
                <button className="mt-4 inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90">
                  View Projects
                </button>
              </Link>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  )
}
