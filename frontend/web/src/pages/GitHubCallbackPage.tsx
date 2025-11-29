/**
 * File: frontend/web/src/pages/GitHubCallbackPage.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 15 Day 5
 * Date: December 2, 2025
 * Authority: Frontend Lead + CPO Approved
 * Foundation: User-Onboarding-Flow-Architecture.md
 *
 * Description:
 * GitHub OAuth callback page.
 * Handles GitHub OAuth redirect, exchanges code for tokens, and redirects to onboarding.
 */

import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Card, CardContent } from '@/components/ui/card'
import apiClient, { setTokens } from '@/api/client'

/**
 * GitHub OAuth callback page
 *
 * Flow:
 * 1. GitHub redirects here with ?code=...&state=...
 * 2. Exchange code for JWT tokens via backend
 * 3. Store tokens in AuthContext
 * 4. Redirect to onboarding step 2 (repository selection)
 */
export default function GitHubCallbackPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const queryClient = useQueryClient()
  const [error, setError] = useState<string | null>(null)

  // Exchange OAuth code for tokens
  const callbackMutation = useMutation({
    mutationFn: async () => {
      const code = searchParams.get('code')
      const state = searchParams.get('state')

      if (!code || !state) {
        throw new Error('Missing code or state parameter')
      }

      const response = await apiClient.post('/github/callback', {
        code,
        state,
      })

      return response.data
    },
    onSuccess: (data) => {
      // Store JWT tokens
      if (data.access_token && data.refresh_token) {
        setTokens(data.access_token, data.refresh_token)

        // Invalidate user query to fetch user data
        queryClient.invalidateQueries({ queryKey: ['user', 'me'] })

        // Redirect to onboarding step 2 (repository selection)
        navigate('/onboarding/repository')
      } else {
        setError('Failed to receive tokens from server')
      }
    },
    onError: (err: Error) => {
      console.error('GitHub OAuth callback error:', err)
      setError(err.message || 'Failed to connect GitHub account')
    },
  })

  useEffect(() => {
    // Trigger OAuth callback on mount
    callbackMutation.mutate()
  }, [])

  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardContent className="p-6 text-center">
            <div className="text-2xl mb-4">❌</div>
            <div className="text-lg font-semibold mb-2">GitHub Connection Failed</div>
            <div className="text-muted-foreground mb-4">{error}</div>
            <button
              onClick={() => navigate('/onboarding/login')}
              className="text-primary hover:underline"
            >
              Try again
            </button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardContent className="p-6 text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary mb-4"></div>
          <div className="text-lg font-semibold mb-2">Connecting GitHub...</div>
          <div className="text-sm text-muted-foreground">
            Please wait while we connect your GitHub account
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
