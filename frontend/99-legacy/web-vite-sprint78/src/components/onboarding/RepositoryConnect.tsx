/**
 * File: frontend/web/src/components/onboarding/RepositoryConnect.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 15 Day 5
 * Date: December 2, 2025
 * Authority: Frontend Lead + CPO Approved
 * Foundation: User-Onboarding-Flow-Architecture.md
 *
 * Description:
 * Step 2: Connect GitHub Repository - 1 minute
 * Allows users to select a GitHub repository for analysis.
 */

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import OnboardingLayout from './OnboardingLayout'
import OnboardingProgress from './OnboardingProgress'
import apiClient from '@/api/client'
import { GitHubRepository, GitHubRepositoryListResponse } from '@/types/api'

/**
 * Repository Connect component (Step 2)
 *
 * Features:
 * - List user's GitHub repositories
 * - Search and filter repositories
 * - Smart sorting (active + recent first)
 * - Auto-select if only 1 repo
 */
export default function RepositoryConnect() {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [selected, setSelected] = useState<number | null>(null)

  // Fetch repositories
  const { data: repos = [], isLoading } = useQuery<GitHubRepository[]>({
    queryKey: ['github', 'repositories'],
    queryFn: async () => {
      const response = await apiClient.get<GitHubRepositoryListResponse>('/github/repositories')
      // Smart sorting: active + recent first
      const repositories = response.data.repositories || []
      return repositories.sort((a, b) => {
        const scoreA = (a.stargazers_count || 0) * 10 + new Date(a.updated_at || 0).getTime()
        const scoreB = (b.stargazers_count || 0) * 10 + new Date(b.updated_at || 0).getTime()
        return scoreB - scoreA
      })
    },
  })

  // Auto-select if only one repo
  useEffect(() => {
    if (repos.length === 1 && !selected && repos[0]) {
      setSelected(repos[0].id)
    }
  }, [repos, selected])

  const handleContinue = async () => {
    if (!selected) return

    const repo = repos.find((r) => r.id === selected)
    if (!repo) return

    // Store selected repo in sessionStorage for next step
    sessionStorage.setItem('onboarding_repo', JSON.stringify(repo))

    // Navigate to analysis step
    navigate('/onboarding/analyzing')
  }

  const filteredRepos = repos.filter(
    (repo) =>
      repo.name.toLowerCase().includes(search.toLowerCase()) ||
      repo.full_name.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <OnboardingLayout
      step={2}
      title="Connect Your Repository"
      subtitle="We'll analyze your project to recommend the right governance policies"
    >
      <div className="space-y-4">
        <div className="rounded-lg bg-blue-50 dark:bg-blue-950 p-4 text-sm text-blue-900 dark:text-blue-100">
          We only need read access to analyze your project structure
        </div>

        <Input
          placeholder="Search repositories..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <div className="max-h-96 overflow-y-auto space-y-2">
          {isLoading ? (
            <div className="text-center py-8 text-muted-foreground">Loading repositories...</div>
          ) : filteredRepos.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">No repositories found</div>
          ) : (
            filteredRepos.map((repo) => (
              <Card
                key={repo.id}
                className={`cursor-pointer transition-colors ${
                  selected === repo.id
                    ? 'border-primary bg-primary/5'
                    : 'hover:bg-muted'
                }`}
                onClick={() => setSelected(repo.id)}
              >
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="font-medium">{repo.name}</div>
                      <div className="text-sm text-muted-foreground">{repo.full_name}</div>
                      {repo.description && (
                        <div className="text-sm text-muted-foreground mt-1 line-clamp-1">
                          {repo.description}
                        </div>
                      )}
                      <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                        {repo.language && <span>● {repo.language}</span>}
                        {repo.stargazers_count > 0 && <span>⭐ {repo.stargazers_count}</span>}
                        {repo.updated_at && (
                          <span>
                            Updated {new Date(repo.updated_at).toLocaleDateString()}
                          </span>
                        )}
                      </div>
                    </div>
                    {selected === repo.id && (
                      <div className="ml-4 text-primary">✓</div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        <Button
          size="lg"
          className="w-full"
          disabled={!selected || isLoading}
          onClick={handleContinue}
        >
          Continue with Selected Repository
        </Button>
      </div>

      <OnboardingProgress current={2} total={6} />
    </OnboardingLayout>
  )
}

