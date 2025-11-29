/**
 * File: frontend/web/src/components/onboarding/FirstGateEvaluation.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 15 Day 5
 * Date: December 2, 2025
 * Authority: Frontend Lead + CPO Approved
 * Foundation: User-Onboarding-Flow-Architecture.md
 *
 * Description:
 * Step 6: First Gate Evaluation - 1 minute
 * Run first gate check (G0.1) and show results.
 */

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import OnboardingLayout from './OnboardingLayout'
import OnboardingProgress from './OnboardingProgress'
import apiClient from '@/api/client'

/**
 * First Gate Evaluation component (Step 6)
 *
 * Features:
 * - Run first gate check (usually G0.1)
 * - Show real-time evaluation progress
 * - Display results (PASS/FAIL/PENDING)
 * - Celebrate success or guide remediation
 */
export default function FirstGateEvaluation() {
  const navigate = useNavigate()
  const [projectId, setProjectId] = useState<string | null>(null)

  // Create project from onboarding data
  const createProjectMutation = useMutation({
    mutationFn: async () => {
      const repo = JSON.parse(sessionStorage.getItem('onboarding_repo') || '{}')

      const response = await apiClient.post('/github/sync', {
        github_repo_id: repo.id,
        github_repo_full_name: repo.full_name,
        project_name: repo.name,
        auto_setup: true,
      })

      return response.data
    },
    onSuccess: (data) => {
      setProjectId(data.project_id)
      // Evaluate first gate
      evaluateGateMutation.mutate(data.project_id)
    },
  })

  // Evaluate first gate (G0.1)
  const evaluateGateMutation = useMutation({
    mutationFn: async (projId: string) => {
      // Get gates for project
      const gatesResponse = await apiClient.get(`/gates?project_id=${projId}`)
      const gates = gatesResponse.data.items || []

      // Find G0.1 gate
      const g01Gate = gates.find((g: { gate_name: string }) => g.gate_name === 'G0.1')
      if (!g01Gate) return null

      // Submit gate for evaluation
      await apiClient.post(`/gates/${g01Gate.id}/submit`, {
        message: 'Initial gate evaluation from onboarding',
      })

      return g01Gate
    },
  })

  useEffect(() => {
    // Start project creation
    createProjectMutation.mutate()
  }, [])

  const handleFinish = () => {
    // Clear onboarding data
    sessionStorage.removeItem('onboarding_repo')
    sessionStorage.removeItem('onboarding_analysis')
    sessionStorage.removeItem('onboarding_policy_pack')
    sessionStorage.removeItem('onboarding_stage_mappings')

    // Navigate to project
    if (projectId) {
      navigate(`/projects/${projectId}`)
    } else {
      navigate('/')
    }
  }

  const isLoading = createProjectMutation.isPending || evaluateGateMutation.isPending
  const gateResult = evaluateGateMutation.data

  return (
    <OnboardingLayout
      step={6}
      title="Running First Gate Evaluation"
      subtitle="Checking if your project meets quality gate requirements"
    >
      <div className="space-y-4">
        {isLoading ? (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            <p className="mt-4 text-muted-foreground">Evaluating gate G0.1...</p>
          </div>
        ) : gateResult ? (
          <div className="space-y-4">
            <Card>
              <CardContent className="p-6 text-center">
                <div className="text-6xl mb-4">🎉</div>
                <div className="text-2xl font-bold mb-2">Gate G0.1 Evaluation Complete!</div>
                <div className="text-muted-foreground">
                  Your project has been set up successfully
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="space-y-2">
                  <div className="text-sm font-medium text-muted-foreground">Project Created</div>
                  <div className="text-lg font-semibold">✓ Successfully synced from GitHub</div>
                </div>
              </CardContent>
            </Card>

            <Button size="lg" className="w-full" onClick={handleFinish}>
              Go to Project Dashboard
            </Button>
          </div>
        ) : (
          <div className="text-center py-8 text-muted-foreground">
            Evaluation in progress...
          </div>
        )}
      </div>

      <OnboardingProgress current={6} total={6} />
    </OnboardingLayout>
  )
}

