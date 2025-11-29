/**
 * File: frontend/web/src/components/onboarding/AIAnalysis.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 15 Day 5
 * Date: December 2, 2025
 * Authority: Frontend Lead + CPO Approved
 * Foundation: User-Onboarding-Flow-Architecture.md
 *
 * Description:
 * Step 3: AI Analysis - 2 minutes
 * Analyzes repository structure and provides recommendations.
 */

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import OnboardingLayout from './OnboardingLayout'
import OnboardingProgress from './OnboardingProgress'
import apiClient from '@/api/client'
import { GitHubAnalysisResult } from '@/types/api'

interface RepositoryAnalysis extends GitHubAnalysisResult {
  repository: {
    name: string
    full_name: string
    description: string | null
    language: string | null
  }
  team_size_estimate?: number
  recommendations?: {
    policy_pack: 'lite' | 'standard' | 'enterprise'
    initial_gates: string[]
  }
}

/**
 * AI Analysis component (Step 3)
 *
 * Features:
 * - Repository structure analysis
 * - Project type detection
 * - Team size estimation
 * - Policy pack recommendation
 */
export default function AIAnalysis() {
  const navigate = useNavigate()
  const [repo, setRepo] = useState<any>(null)

  // Get selected repo from sessionStorage
  useEffect(() => {
    const repoData = sessionStorage.getItem('onboarding_repo')
    if (repoData) {
      setRepo(JSON.parse(repoData))
    } else {
      // No repo selected, go back
      navigate('/onboarding/repository')
    }
  }, [navigate])

  // Analyze repository
  const { data: analysis, isLoading } = useQuery<RepositoryAnalysis>({
    queryKey: ['github', 'analyze', repo?.full_name],
    queryFn: async () => {
      if (!repo) return null
      const [owner, repoName] = repo.full_name.split('/')
      const response = await apiClient.get(
        `/github/repositories/${owner}/${repoName}/analyze`
      )
      return response.data
    },
    enabled: !!repo,
  })

  const handleContinue = () => {
    // Store analysis results for next step
    if (analysis) {
      sessionStorage.setItem('onboarding_analysis', JSON.stringify(analysis))
    }
    navigate('/onboarding/policy-pack')
  }

  if (!repo) {
    return null
  }

  return (
    <OnboardingLayout
      step={3}
      title="Analyzing Your Repository"
      subtitle="We're analyzing your project structure to provide personalized recommendations"
    >
      <div className="space-y-4">
        {isLoading ? (
          <div className="space-y-4">
            <div className="text-center py-8">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              <p className="mt-4 text-muted-foreground">Analyzing repository structure...</p>
            </div>
          </div>
        ) : analysis ? (
          <div className="space-y-4">
            <Card>
              <CardContent className="p-4">
                <div className="space-y-3">
                  <div>
                    <div className="text-sm font-medium text-muted-foreground">Project Type</div>
                    <div className="text-lg font-semibold capitalize">
                      {analysis.project_type?.replace('_', ' ') || 'Unknown'}
                    </div>
                  </div>
                  {analysis.team_size_estimate && (
                    <div>
                      <div className="text-sm font-medium text-muted-foreground">
                        Team Size Estimate
                      </div>
                      <div className="text-lg font-semibold">
                        {analysis.team_size_estimate} developers
                      </div>
                    </div>
                  )}
                  {analysis.languages && Object.keys(analysis.languages).length > 0 && (
                    <div>
                      <div className="text-sm font-medium text-muted-foreground">Languages</div>
                      <div className="flex flex-wrap gap-2 mt-1">
                        {Object.entries(analysis.languages)
                          .slice(0, 5)
                          .map(([lang]) => (
                            <span
                              key={lang}
                              className="px-2 py-1 rounded bg-muted text-sm"
                            >
                              {lang}
                            </span>
                          ))}
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="space-y-2">
                  <div className="text-sm font-medium text-muted-foreground">
                    Recommended Policy Pack
                  </div>
                  <div className="text-2xl font-bold capitalize">
                    {analysis.recommended_policy_pack || analysis.recommendations?.policy_pack || 'Standard'}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Based on your project type and team size
                  </div>
                </div>
              </CardContent>
            </Card>

            <Button size="lg" className="w-full" onClick={handleContinue}>
              Continue with Recommendations
            </Button>
          </div>
        ) : (
          <div className="text-center py-8 text-muted-foreground">
            Analysis failed. Please try again.
          </div>
        )}
      </div>

      <OnboardingProgress current={3} total={6} />
    </OnboardingLayout>
  )
}

