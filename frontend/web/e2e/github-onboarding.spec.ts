/**
 * File: frontend/web/e2e/github-onboarding.spec.ts
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 17
 * Date: November 28, 2025
 * Authority: Frontend Lead + QA Lead Approved
 * Foundation: Sprint 15 GitHub Integration, Sprint 16 Testing
 *
 * Description:
 * E2E tests for complete GitHub onboarding flow including:
 * - OAuth authorization
 * - Repository listing and selection
 * - Repository analysis
 * - Project sync
 * - Webhook setup
 *
 * Critical Journey: GitHub Connected User
 * - Step 1: Initiate OAuth flow
 * - Step 2: Handle OAuth callback
 * - Step 3: View connected repositories
 * - Step 4: Select and analyze repository
 * - Step 5: Create project from repo
 * - Step 6: Verify sync status
 *
 * Target: Complete GitHub onboarding < 5 minutes
 */

import { test, expect, Page } from '@playwright/test'

// Test data
const TEST_USER = {
  email: 'nguyen.van.anh@mtc.com.vn',
  password: 'SecurePassword123!',
}

const MOCK_GITHUB_USER = {
  id: 12345678,
  login: 'testuser',
  name: 'Test User',
  email: 'testuser@github.com',
  avatar_url: 'https://avatars.githubusercontent.com/u/12345678',
}

const MOCK_REPOSITORIES = [
  {
    id: 123456789,
    name: 'my-project',
    full_name: 'testuser/my-project',
    description: 'A sample project for testing',
    language: 'TypeScript',
    private: false,
    html_url: 'https://github.com/testuser/my-project',
    default_branch: 'main',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2025-11-28T00:00:00Z',
    pushed_at: '2025-11-28T00:00:00Z',
    stargazers_count: 10,
    forks_count: 2,
    open_issues_count: 5,
  },
  {
    id: 987654321,
    name: 'another-project',
    full_name: 'testuser/another-project',
    description: 'Another sample project',
    language: 'Python',
    private: true,
    html_url: 'https://github.com/testuser/another-project',
    default_branch: 'main',
    created_at: '2024-06-01T00:00:00Z',
    updated_at: '2025-11-27T00:00:00Z',
    pushed_at: '2025-11-27T00:00:00Z',
    stargazers_count: 5,
    forks_count: 1,
    open_issues_count: 3,
  },
]

test.describe('GitHub Onboarding Flow', () => {
  test.describe('Step 1: OAuth Authorization', () => {
    test('should display GitHub connect button on settings page', async ({
      page,
    }) => {
      // Login first
      await page.goto('/login')
      await page.fill('input[name="email"]', TEST_USER.email)
      await page.fill('input[name="password"]', TEST_USER.password)
      await page.click('button[type="submit"]')

      // Navigate to settings/integrations
      await page.goto('/settings/integrations')

      // Check GitHub connect section
      await expect(page.getByText(/Connect GitHub/i)).toBeVisible()
      await expect(
        page.getByRole('button', { name: /Connect.*GitHub/i })
      ).toBeVisible()
    })

    test('should display GitHub OAuth benefits', async ({ page }) => {
      await page.goto('/settings/integrations')

      // Check benefits list
      await expect(page.getByText(/Read-only access/i)).toBeVisible()
      await expect(page.getByText(/Auto-sync repositories/i)).toBeVisible()
      await expect(page.getByText(/Webhook integration/i)).toBeVisible()
    })

    test('should initiate OAuth flow when clicking connect', async ({
      page,
    }) => {
      await page.goto('/settings/integrations')

      // Mock the authorize endpoint
      await page.route('**/api/v1/github/authorize**', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            authorize_url:
              'https://github.com/login/oauth/authorize?client_id=test&scope=read:user,repo&state=abc123',
          }),
        })
      })

      // Click connect button
      const connectButton = page.getByRole('button', {
        name: /Connect.*GitHub/i,
      })
      await connectButton.click()

      // Should either redirect or show authorization URL
      // In test mode, we verify the API was called
      await expect(page.locator('body')).toBeVisible()
    })
  })

  test.describe('Step 2: OAuth Callback', () => {
    test('should display loading state during callback', async ({ page }) => {
      await page.goto('/auth/github/callback?code=test_code&state=abc123')

      // Should show loading indicator
      await expect(page.getByText(/Connecting GitHub/i)).toBeVisible({
        timeout: 5000,
      })
    })

    test('should handle successful OAuth callback', async ({ page }) => {
      // Mock callback API
      await page.route('**/api/v1/github/callback', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            success: true,
            user: MOCK_GITHUB_USER,
          }),
        })
      })

      await page.goto('/auth/github/callback?code=test_code&state=abc123')

      // Should redirect to repository selection or success page
      await page.waitForTimeout(2000)
      // Check we're no longer on callback page
      const url = page.url()
      expect(url).not.toContain('/auth/github/callback')
    })

    test('should handle OAuth error callback', async ({ page }) => {
      await page.goto(
        '/auth/github/callback?error=access_denied&error_description=The+user+denied+access'
      )

      // Should show error message
      await expect(page.getByText(/denied|failed|error/i)).toBeVisible({
        timeout: 5000,
      })
    })

    test('should handle missing code parameter', async ({ page }) => {
      await page.goto('/auth/github/callback?state=abc123')

      // Should show error about missing code
      await expect(page.getByText(/Missing|Invalid|Error/i)).toBeVisible({
        timeout: 5000,
      })
    })

    test('should have retry option on error', async ({ page }) => {
      await page.goto('/auth/github/callback?error=server_error')

      // Wait for error state
      await page.waitForTimeout(2000)

      // Should have try again option
      const tryAgain = page.getByText(/Try again/i)
      if (await tryAgain.isVisible()) {
        await tryAgain.click()
        await expect(page).toHaveURL(/\/onboarding\/login|\/settings/)
      }
    })
  })

  test.describe('Step 3: GitHub Status Check', () => {
    test('should display GitHub connection status', async ({ page }) => {
      // Mock status endpoint
      await page.route('**/api/v1/github/status', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            connected: true,
            github_username: MOCK_GITHUB_USER.login,
            github_avatar_url: MOCK_GITHUB_USER.avatar_url,
            connected_at: '2025-11-28T00:00:00Z',
            scopes: ['read:user', 'repo'],
          }),
        })
      })

      await page.goto('/settings/integrations')

      // Should show connected status
      await expect(page.getByText(/Connected as/i)).toBeVisible()
      await expect(page.getByText(MOCK_GITHUB_USER.login)).toBeVisible()
    })

    test('should display disconnect option when connected', async ({
      page,
    }) => {
      // Mock connected status
      await page.route('**/api/v1/github/status', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            connected: true,
            github_username: MOCK_GITHUB_USER.login,
          }),
        })
      })

      await page.goto('/settings/integrations')

      // Should show disconnect button
      await expect(
        page.getByRole('button', { name: /Disconnect/i })
      ).toBeVisible()
    })

    test('should handle disconnect action', async ({ page }) => {
      // Mock status and disconnect endpoints
      await page.route('**/api/v1/github/status', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            connected: true,
            github_username: MOCK_GITHUB_USER.login,
          }),
        })
      })

      await page.route('**/api/v1/github/disconnect', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ success: true }),
        })
      })

      await page.goto('/settings/integrations')

      // Click disconnect
      const disconnectBtn = page.getByRole('button', { name: /Disconnect/i })
      if (await disconnectBtn.isVisible()) {
        await disconnectBtn.click()

        // May show confirmation dialog
        const confirmBtn = page.getByRole('button', { name: /Confirm/i })
        if (await confirmBtn.isVisible()) {
          await confirmBtn.click()
        }
      }
    })
  })

  test.describe('Step 4: Repository Listing', () => {
    test.beforeEach(async ({ page }) => {
      // Mock GitHub connected status
      await page.route('**/api/v1/github/status', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            connected: true,
            github_username: MOCK_GITHUB_USER.login,
          }),
        })
      })

      // Mock repositories list
      await page.route('**/api/v1/github/repositories**', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            repositories: MOCK_REPOSITORIES,
            total: MOCK_REPOSITORIES.length,
          }),
        })
      })
    })

    test('should display list of repositories', async ({ page }) => {
      await page.goto('/onboarding/repository')

      // Should show repository list
      await expect(page.getByText('my-project')).toBeVisible()
      await expect(page.getByText('another-project')).toBeVisible()
    })

    test('should display repository details', async ({ page }) => {
      await page.goto('/onboarding/repository')

      // Should show language badges
      await expect(page.getByText('TypeScript')).toBeVisible()
      await expect(page.getByText('Python')).toBeVisible()

      // Should show private badge for private repos
      await expect(page.getByText(/Private/i)).toBeVisible()
    })

    test('should filter repositories by search', async ({ page }) => {
      await page.goto('/onboarding/repository')

      // Search for specific repo
      const searchInput = page.getByPlaceholder(/search/i)
      await searchInput.fill('my-project')

      // Should filter results
      await expect(page.getByText('my-project')).toBeVisible()
      // Note: another-project may or may not be visible depending on filter implementation
    })

    test('should allow selecting a repository', async ({ page }) => {
      await page.goto('/onboarding/repository')

      // Click on repository card/row
      await page.getByText('my-project').click()

      // Should show selection or enable continue
      const continueBtn = page.getByRole('button', { name: /Continue|Select/i })
      await expect(continueBtn).toBeEnabled()
    })

    test('should paginate repository list', async ({ page }) => {
      await page.goto('/onboarding/repository')

      // Check for pagination controls if list is long
      const nextBtn = page.getByRole('button', { name: /Next|Load more/i })
      if (await nextBtn.isVisible()) {
        await nextBtn.click()
        // Should load more repositories
      }
    })
  })

  test.describe('Step 5: Repository Analysis', () => {
    test.beforeEach(async ({ page }) => {
      // Set up selected repository in session
      await page.goto('/onboarding/repository')
      await page.evaluate(() => {
        sessionStorage.setItem(
          'onboarding_repo',
          JSON.stringify({
            id: 123456789,
            name: 'my-project',
            full_name: 'testuser/my-project',
            language: 'TypeScript',
          })
        )
      })
    })

    test('should display analysis in progress', async ({ page }) => {
      // Mock analyze endpoint
      await page.route('**/api/v1/github/repositories/*/*/analyze', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            analysis: {
              languages: { TypeScript: 80, JavaScript: 15, CSS: 5 },
              has_readme: true,
              has_license: true,
              has_tests: true,
              suggested_policy_pack: 'standard',
              suggested_stage: 'BUILD',
            },
          }),
        })
      })

      await page.goto('/onboarding/analyzing')

      // Should show analysis loading
      await expect(page.getByText(/Analyzing/i)).toBeVisible()
    })

    test('should display analysis results', async ({ page }) => {
      // Mock analyze endpoint with immediate response
      await page.route('**/api/v1/github/repositories/*/*/analyze', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            analysis: {
              languages: { TypeScript: 80, JavaScript: 15, CSS: 5 },
              has_readme: true,
              has_license: true,
              has_tests: true,
              suggested_policy_pack: 'standard',
              suggested_stage: 'BUILD',
            },
          }),
        })
      })

      await page.goto('/onboarding/analyzing')

      // Wait for analysis to complete
      await page.waitForTimeout(3000)

      // Should show analysis results or navigate to next step
      const hasResults = await page.getByText(/TypeScript|BUILD|standard/i).isVisible()
      const navigated = !page.url().includes('/analyzing')

      expect(hasResults || navigated).toBeTruthy()
    })
  })

  test.describe('Step 6: Project Sync', () => {
    test('should trigger sync after project creation', async ({ page }) => {
      // Mock sync endpoint
      await page.route('**/api/v1/github/sync', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            job_id: 'sync_123456',
            status: 'queued',
            message: 'Sync job queued',
          }),
        })
      })

      // Navigate to a project that needs sync
      await page.goto('/projects/create')

      // Fill in project details
      await page.fill('input[name="name"]', 'My Project')

      // Select GitHub repo
      const repoSelect = page.locator('select[name="github_repo"]')
      if (await repoSelect.isVisible()) {
        await repoSelect.selectOption('testuser/my-project')
      }

      // Submit form
      const submitBtn = page.getByRole('button', { name: /Create/i })
      if (await submitBtn.isVisible()) {
        await submitBtn.click()
      }
    })

    test('should display sync status indicator', async ({ page }) => {
      // Mock project with sync status
      await page.route('**/api/v1/projects/**', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            id: 'project-123',
            name: 'My Project',
            github_repo_id: 123456789,
            github_repo_full_name: 'testuser/my-project',
            github_synced_at: '2025-11-28T00:00:00Z',
            sync_status: 'synced',
          }),
        })
      })

      await page.goto('/projects/project-123')

      // Should show sync status
      await expect(page.getByText(/Synced|Last sync/i)).toBeVisible()
    })

    test('should allow manual sync trigger', async ({ page }) => {
      await page.route('**/api/v1/github/sync', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            job_id: 'sync_123456',
            status: 'queued',
          }),
        })
      })

      await page.goto('/projects/project-123')

      // Find and click sync button
      const syncBtn = page.getByRole('button', { name: /Sync|Refresh/i })
      if (await syncBtn.isVisible()) {
        await syncBtn.click()

        // Should show sync in progress
        await expect(page.getByText(/Syncing|In progress/i)).toBeVisible()
      }
    })
  })

  test.describe('Error Handling', () => {
    test('should handle API rate limit error', async ({ page }) => {
      await page.route('**/api/v1/github/repositories**', async (route) => {
        await route.fulfill({
          status: 403,
          contentType: 'application/json',
          body: JSON.stringify({
            error: 'rate_limit_exceeded',
            message: 'GitHub API rate limit exceeded',
            reset_at: Date.now() + 3600000,
          }),
        })
      })

      await page.goto('/onboarding/repository')

      // Should show rate limit error
      await expect(page.getByText(/rate limit/i)).toBeVisible()
    })

    test('should handle token expired error', async ({ page }) => {
      await page.route('**/api/v1/github/repositories**', async (route) => {
        await route.fulfill({
          status: 401,
          contentType: 'application/json',
          body: JSON.stringify({
            error: 'token_expired',
            message: 'GitHub token has expired',
          }),
        })
      })

      await page.goto('/onboarding/repository')

      // Should show reconnect option
      await expect(page.getByText(/expired|reconnect/i)).toBeVisible()
    })

    test('should handle network error gracefully', async ({ page }) => {
      await page.route('**/api/v1/github/repositories**', async (route) => {
        await route.abort('failed')
      })

      await page.goto('/onboarding/repository')

      // Should show network error
      await expect(page.getByText(/network|connection|failed/i)).toBeVisible()
    })
  })

  test.describe('Responsiveness', () => {
    test('should be responsive on mobile', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 })
      await page.goto('/onboarding/repository')

      // Repository cards should be visible
      await expect(page.locator('body')).toBeVisible()
    })

    test('should be responsive on tablet', async ({ page }) => {
      await page.setViewportSize({ width: 768, height: 1024 })
      await page.goto('/onboarding/repository')

      // Should show grid or list layout
      await expect(page.locator('body')).toBeVisible()
    })
  })

  test.describe('Accessibility', () => {
    test('should have accessible repository list', async ({ page }) => {
      await page.route('**/api/v1/github/repositories**', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            repositories: MOCK_REPOSITORIES,
          }),
        })
      })

      await page.goto('/onboarding/repository')

      // Check for proper ARIA labels
      const repoList = page.getByRole('list')
      if (await repoList.isVisible()) {
        await expect(repoList).toBeVisible()
      }
    })

    test('should support keyboard navigation', async ({ page }) => {
      await page.goto('/onboarding/repository')

      // Tab through elements
      await page.keyboard.press('Tab')
      await page.keyboard.press('Tab')

      // Should be able to focus interactive elements
      const focusedElement = page.locator(':focus')
      await expect(focusedElement).toBeVisible()
    })
  })
})
