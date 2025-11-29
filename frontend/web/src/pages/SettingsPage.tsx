/**
 * File: frontend/web/src/pages/SettingsPage.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: November 28, 2025
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 4.9 Complete Lifecycle
 *
 * Description:
 * Settings page for user preferences and integrations.
 * Includes GitHub connection status and account management.
 *
 * SDLC 4.9 Compliance:
 * - Pillar 1: Zero Mock Policy (Real API calls)
 * - Pillar 3: Quality Governance (Type hints, validation)
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'
import DashboardLayout from '@/components/layout/DashboardLayout'
import apiClient from '@/api/client'
import { useAuth } from '@/contexts/AuthContext'
import type { GitHubConnectionStatus } from '@/types/api'

/**
 * Settings page component
 *
 * Features:
 * - GitHub connection status display
 * - Connect/Disconnect GitHub account
 * - User profile information
 * - Rate limit display
 */
export default function SettingsPage() {
  const { user } = useAuth()
  const queryClient = useQueryClient()

  // Fetch GitHub connection status
  const { data: githubStatus, isLoading: isLoadingGitHub } = useQuery<GitHubConnectionStatus>({
    queryKey: ['github-status'],
    queryFn: async () => {
      const response = await apiClient.get<GitHubConnectionStatus>('/github/status')
      return response.data
    },
  })

  // Connect GitHub mutation
  const connectMutation = useMutation({
    mutationFn: async () => {
      const response = await apiClient.get<{ authorization_url: string }>('/github/auth/url')
      return response.data.authorization_url
    },
    onSuccess: (authUrl) => {
      // Redirect to GitHub OAuth
      window.location.href = authUrl
    },
  })

  // Disconnect GitHub mutation
  const disconnectMutation = useMutation({
    mutationFn: async () => {
      await apiClient.delete('/github/disconnect')
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['github-status'] })
    },
  })

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page header */}
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
          <p className="text-muted-foreground">
            Manage your account settings and integrations
          </p>
        </div>

        {/* Profile Section */}
        <Card>
          <CardHeader>
            <CardTitle>Profile</CardTitle>
            <CardDescription>Your account information</CardDescription>
          </CardHeader>
          <CardContent>
            {user ? (
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-primary">
                    <svg className="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-lg font-medium">{user.name || user.email}</p>
                    <p className="text-sm text-muted-foreground">{user.email}</p>
                  </div>
                </div>
                <div className="grid gap-2 text-sm">
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-muted-foreground">User ID</span>
                    <span className="font-mono text-xs">{user.id}</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-muted-foreground">Status</span>
                    <span className={user.is_active ? 'text-green-600' : 'text-red-600'}>
                      {user.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-muted-foreground">Roles</span>
                    <span>{user.roles?.join(', ') || 'User'}</span>
                  </div>
                  {user.last_login_at && (
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Last Login</span>
                      <span>{new Date(user.last_login_at).toLocaleString()}</span>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <p className="text-muted-foreground">Loading profile...</p>
            )}
          </CardContent>
        </Card>

        {/* GitHub Integration Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <svg className="h-6 w-6" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              GitHub Integration
            </CardTitle>
            <CardDescription>
              Connect your GitHub account to sync repositories and create projects
            </CardDescription>
          </CardHeader>
          <CardContent>
            {isLoadingGitHub ? (
              <div className="text-muted-foreground">Loading GitHub status...</div>
            ) : githubStatus?.connected ? (
              <div className="space-y-4">
                {/* Connected status */}
                <div className="flex items-center gap-3 rounded-lg border border-green-200 bg-green-50 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-green-100">
                    <svg className="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-green-800">Connected</p>
                    <p className="text-sm text-green-700">
                      Signed in as <span className="font-semibold">@{githubStatus.github_username}</span>
                    </p>
                  </div>
                  {githubStatus.github_avatar && (
                    <img
                      src={githubStatus.github_avatar}
                      alt={githubStatus.github_username || 'GitHub avatar'}
                      className="h-10 w-10 rounded-full"
                    />
                  )}
                </div>

                {/* Connection details */}
                <div className="grid gap-2 text-sm">
                  {githubStatus.connected_at && (
                    <div className="flex justify-between border-b pb-2">
                      <span className="text-muted-foreground">Connected Since</span>
                      <span>{new Date(githubStatus.connected_at).toLocaleDateString()}</span>
                    </div>
                  )}
                  {githubStatus.scopes && githubStatus.scopes.length > 0 && (
                    <div className="flex justify-between border-b pb-2">
                      <span className="text-muted-foreground">Permissions</span>
                      <span className="text-right">{githubStatus.scopes.join(', ')}</span>
                    </div>
                  )}
                  {githubStatus.rate_limit && (
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">API Rate Limit</span>
                      <span>
                        {githubStatus.rate_limit.remaining} / {githubStatus.rate_limit.limit} remaining
                      </span>
                    </div>
                  )}
                </div>

                {/* Disconnect button */}
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button variant="outline" className="text-red-600 hover:text-red-700">
                      <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Disconnect GitHub
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>Disconnect GitHub Account?</AlertDialogTitle>
                      <AlertDialogDescription>
                        This will remove the connection between your SDLC Orchestrator account and GitHub.
                        Your existing projects will not be affected, but automatic syncing will stop.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                      <AlertDialogAction
                        onClick={() => disconnectMutation.mutate()}
                        disabled={disconnectMutation.isPending}
                        className="bg-red-600 hover:bg-red-700"
                      >
                        {disconnectMutation.isPending ? 'Disconnecting...' : 'Disconnect'}
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            ) : (
              <div className="space-y-4">
                {/* Not connected status */}
                <div className="flex items-center gap-3 rounded-lg border border-gray-200 bg-gray-50 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-200">
                    <svg className="h-6 w-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                    </svg>
                  </div>
                  <div>
                    <p className="font-medium text-gray-800">Not Connected</p>
                    <p className="text-sm text-gray-600">
                      Connect your GitHub account to sync repositories
                    </p>
                  </div>
                </div>

                {/* Benefits list */}
                <div className="rounded-lg border p-4">
                  <p className="font-medium mb-2">Benefits of connecting GitHub:</p>
                  <ul className="space-y-2 text-sm text-muted-foreground">
                    <li className="flex items-center gap-2">
                      <svg className="h-4 w-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      Import repositories as projects
                    </li>
                    <li className="flex items-center gap-2">
                      <svg className="h-4 w-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      Automatic evidence collection from PRs
                    </li>
                    <li className="flex items-center gap-2">
                      <svg className="h-4 w-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      Repository analysis for policy recommendations
                    </li>
                    <li className="flex items-center gap-2">
                      <svg className="h-4 w-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      Webhook integration for real-time updates
                    </li>
                  </ul>
                </div>

                {/* Connect button */}
                <Button
                  onClick={() => connectMutation.mutate()}
                  disabled={connectMutation.isPending}
                  className="w-full"
                >
                  {connectMutation.isPending ? (
                    'Redirecting to GitHub...'
                  ) : (
                    <>
                      <svg className="mr-2 h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                      </svg>
                      Connect GitHub Account
                    </>
                  )}
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Danger Zone */}
        <Card className="border-red-200">
          <CardHeader>
            <CardTitle className="text-red-600">Danger Zone</CardTitle>
            <CardDescription>
              Irreversible actions for your account
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between rounded-lg border border-red-200 p-4">
              <div>
                <p className="font-medium">Delete Account</p>
                <p className="text-sm text-muted-foreground">
                  Permanently delete your account and all associated data
                </p>
              </div>
              <Button variant="outline" className="text-red-600 hover:text-red-700" disabled>
                Delete Account
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}
